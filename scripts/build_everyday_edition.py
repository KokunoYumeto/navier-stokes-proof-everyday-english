#!/usr/bin/env python3
"""Build and inspect the Everyday English Edition without publishing it.

The default profile is provisional. It can exercise the complete local toolchain
while the translation is still being written, but its receipts cannot be used as
final QA or publication acceptance. The final profile fails closed on the
translation audit, unresolved references, layout overflow, and EPUBCheck.
"""

from __future__ import annotations

import argparse
import contextlib
import datetime as dt
import hashlib
import html as html_stdlib
import importlib.metadata
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import shutil
import signal
import subprocess
import sys
import tempfile
import textwrap
import urllib.parse
import zipfile
from collections import Counter, defaultdict
from typing import Any, Iterable, Sequence


ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "everyday" / "build-config.json"
EPUBCHECK_LOCK_PATH = ROOT / "everyday" / "epubcheck-lock.json"
TMP_ROOT = ROOT / "tmp" / "build" / "everyday-english"
CONFIG = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
EPUBCHECK_LOCK = json.loads(EPUBCHECK_LOCK_PATH.read_text(encoding="utf-8"))
OUTPUT_ROOT = ROOT / CONFIG["outputs"]["root"]
PDF_OUTPUT = OUTPUT_ROOT / CONFIG["outputs"]["pdf"]
HTML_OUTPUT = OUTPUT_ROOT / CONFIG["outputs"]["html"]
EPUB_OUTPUT = OUTPUT_ROOT / CONFIG["outputs"]["epub"]
RECEIPTS = OUTPUT_ROOT / CONFIG["outputs"]["receipts"]
LOGS = RECEIPTS / "logs"


class BuildError(RuntimeError):
    """A fail-closed build or validation error."""


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def rel(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return resolved.name


def sanitize(text: str) -> str:
    """Remove machine-specific account and project prefixes from recorded text."""
    replacements = {
        str(ROOT.resolve()): "${PROJECT_ROOT}",
        ROOT.resolve().as_posix(): "${PROJECT_ROOT}",
        str(Path.home().resolve()): "${USER_HOME}",
        Path.home().resolve().as_posix(): "${USER_HOME}",
    }
    result = text
    for source, replacement in sorted(replacements.items(), key=lambda item: len(item[0]), reverse=True):
        result = result.replace(source, replacement)
        wrapped = re.compile("".join(re.escape(character) + r"(?:\r?\n)?" for character in source))
        result = wrapped.sub(lambda _match: replacement, result)
    return result


def write_bytes(path: Path, payload: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".next")
    temporary.write_bytes(payload)
    temporary.replace(path)


def write_text(path: Path, text: str) -> None:
    write_bytes(path, text.replace("\r\n", "\n").encode("utf-8"))


def write_json(path: Path, value: Any) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


def file_record(path: Path, *, base: Path = ROOT) -> dict[str, Any]:
    try:
        name = path.resolve().relative_to(base.resolve()).as_posix()
    except ValueError:
        name = path.name
    return {"path": name, "bytes": path.stat().st_size, "sha256": sha256_path(path)}


def ensure_child(parent: Path, child: Path) -> None:
    parent_resolved = parent.resolve()
    child_resolved = child.resolve()
    try:
        child_resolved.relative_to(parent_resolved)
    except ValueError as exc:
        raise BuildError(f"Refusing a path outside {rel(parent)}: {sanitize(str(child_resolved))}") from exc


def reset_dir(path: Path) -> None:
    ensure_child(TMP_ROOT, path)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True)


def stable_environment() -> dict[str, str]:
    environment = os.environ.copy()
    environment["SOURCE_DATE_EPOCH"] = str(CONFIG["source_date_epoch"])
    environment["FORCE_SOURCE_DATE"] = "1"
    environment["TZ"] = "UTC"
    environment["PYTHONHASHSEED"] = "0"
    return environment


def display_command(arguments: Sequence[str]) -> list[str]:
    return [sanitize(str(argument)) for argument in arguments]


def terminate_process_tree(process: subprocess.Popen[str]) -> None:
    if process.poll() is not None:
        return
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    else:
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)


def run_command(
    arguments: Sequence[str],
    *,
    cwd: Path,
    timeout: int,
    environment: dict[str, str] | None = None,
) -> dict[str, Any]:
    creationflags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    process = subprocess.Popen(
        list(arguments),
        cwd=cwd,
        env=environment or stable_environment(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        creationflags=creationflags,
        start_new_session=os.name != "nt",
    )
    timed_out = False
    try:
        output, _ = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        terminate_process_tree(process)
        output, _ = process.communicate()
    return {
        "command": display_command(arguments),
        "cwd": rel(cwd),
        "exit_code": process.returncode,
        "timed_out": timed_out,
        "output": sanitize(output),
    }


def require_tool(name: str) -> str:
    resolved = shutil.which(name)
    if resolved is None:
        raise BuildError(f"Required command is missing: {name}")
    return resolved


def version_probe(name: str, arguments: Sequence[str]) -> dict[str, Any]:
    resolved = shutil.which(name)
    if resolved is None:
        return {"available": False, "command": name, "version": None}
    result = run_command([resolved, *arguments], cwd=ROOT, timeout=30)
    lines = [line.strip() for line in result["output"].splitlines() if line.strip()]
    return {
        "available": result["exit_code"] == 0,
        "command": Path(resolved).name,
        "version": " | ".join(lines[:3]) if lines else None,
        "exit_code": result["exit_code"],
    }


def epubcheck_command() -> list[str] | None:
    installed = shutil.which("epubcheck")
    if installed:
        return [installed]
    java = shutil.which("java")
    runtime = ROOT / PurePosixPath(EPUBCHECK_LOCK["runtime_jar"])
    if java and runtime.is_file():
        return [java, "-jar", str(runtime)]
    return None


def epubcheck_probe() -> dict[str, Any]:
    command = epubcheck_command()
    archive = ROOT / "tmp" / "dependencies" / EPUBCHECK_LOCK["archive"]["name"]
    runtime = ROOT / PurePosixPath(EPUBCHECK_LOCK["runtime_jar"])
    provenance = {
        "locked_version": EPUBCHECK_LOCK["version"],
        "release_page": EPUBCHECK_LOCK["release_page"],
        "archive_url": EPUBCHECK_LOCK["archive"]["url"],
        "archive_bytes": EPUBCHECK_LOCK["archive"]["bytes"],
        "archive_sha256": EPUBCHECK_LOCK["archive"]["sha256"],
        "archive_present": archive.is_file(),
        "runtime_jar": EPUBCHECK_LOCK["runtime_jar"],
        "runtime_jar_sha256": sha256_path(runtime) if runtime.is_file() else None,
        "fetch_command": "powershell -NoProfile -ExecutionPolicy Bypass -File scripts/fetch_epubcheck.ps1",
    }
    if archive.is_file():
        provenance["archive_verified"] = (
            archive.stat().st_size == int(EPUBCHECK_LOCK["archive"]["bytes"])
            and sha256_path(archive) == EPUBCHECK_LOCK["archive"]["sha256"]
        )
    else:
        provenance["archive_verified"] = False
    if command is None:
        return {"available": False, "command": "epubcheck", "version": None, "provenance": provenance}
    result = run_command([*command, "--version"], cwd=ROOT, timeout=120)
    lines = [line.strip() for line in result["output"].splitlines() if line.strip()]
    observed = " | ".join(lines[:3]) if lines else None
    available = result["exit_code"] == 0 and EPUBCHECK_LOCK["version"] in (observed or "")
    return {
        "available": available,
        "command": display_command(command),
        "version": observed,
        "exit_code": result["exit_code"],
        "provenance": provenance,
    }


def dependency_report() -> dict[str, Any]:
    tools = {
        "pdflatex": version_probe("pdflatex", ["--version"]),
        "make4ht": version_probe("make4ht", ["--version"]),
        "pandoc": version_probe("pandoc", ["--version"]),
        "pdfinfo": version_probe("pdfinfo", ["-v"]),
        "pdftoppm": version_probe("pdftoppm", ["-v"]),
        "xmllint": version_probe("xmllint", ["--version"]),
        "epubcheck": epubcheck_probe(),
        "tex4ebook": version_probe("tex4ebook", ["--version"]),
        "linkchecker": version_probe("linkchecker", ["--version"]),
    }
    modules = {}
    for name in ("lxml", "latex2mathml", "pypdf"):
        try:
            modules[name] = {"available": True, "version": importlib.metadata.version(name)}
        except importlib.metadata.PackageNotFoundError:
            modules[name] = {"available": False, "version": None}
    required = ["pdflatex", "pandoc", "pdfinfo"]
    missing_required = [name for name in required if not tools[name]["available"]]
    if not modules["lxml"]["available"]:
        missing_required.append("python:lxml")
    if not modules["latex2mathml"]["available"]:
        missing_required.append("python:latex2mathml")
    optional_missing = [
        name for name in ("pdftoppm", "xmllint", "epubcheck", "tex4ebook", "linkchecker")
        if not tools[name]["available"]
    ]
    report = {
        "schema": "navier-stokes-everyday-dependencies/v1",
        "profile": "local",
        "python": {"version": sys.version.split()[0], "implementation": sys.implementation.name},
        "tools": tools,
        "python_modules": modules,
        "missing_required": missing_required,
        "missing_optional": optional_missing,
        "notes": {
            "epubcheck": "Required by the final profile. Provisional builds use the internal EPUB structure, XML, image-alternative, and link checks when it is unavailable.",
            "linkchecker": "The internal checker closes local HTML and EPUB links. It does not make network requests for external links.",
            "make4ht": "Detected for reference but not used. The reproducible web route uses Pandoc with native MathML because the installed TeX4ht route does not finish this book in a practical validation window.",
            "tex4ebook": "Not used. EPUB 3 is built from the checked HTML with Pandoc and then repacked deterministically.",
        },
        "status": "pass" if not missing_required else "fail",
    }
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    write_json(RECEIPTS / "dependencies.json", report)
    return report


INPUT_RE = re.compile(r"\\input\{sections/(pp\d{3}-\d{3})\}")


def main_ranges(main_text: str) -> list[str]:
    return INPUT_RE.findall(main_text)


def input_paths(target: str) -> list[Path]:
    if target not in {"pdf", "html"}:
        raise BuildError(f"Unknown snapshot target: {target}")
    main_path = ROOT / CONFIG["entrypoint"]
    main_text = main_path.read_text(encoding="utf-8-sig")
    observed = main_ranges(main_text)
    expected = CONFIG["expected_ranges"]
    if observed != expected:
        raise BuildError(f"main.tex range order differs from build-config.json: {observed}")
    paths = [
        CONFIG_PATH,
        main_path,
    ]
    if target == "pdf":
        paths.extend(
            [
                ROOT / CONFIG["pdf_style"],
                ROOT / "reconstruction" / "ns-edition.sty",
            ]
        )
    else:
        paths.extend([ROOT / CONFIG["web_style"], ROOT / CONFIG["web_css"]])
    paths.extend(ROOT / "everyday" / "sections" / f"{name}.tex" for name in expected)
    for number in range(1, 7):
        suffix = "pdf" if target == "pdf" else "svg"
        paths.append(ROOT / "reconstruction" / "assets" / "figures" / f"figure-{number}.{suffix}")
    section_text = "\n".join(
        (ROOT / "everyday" / "sections" / f"{name}.tex").read_text(encoding="utf-8-sig")
        for name in expected
    )
    image_references = re.findall(r"\\includegraphics(?:\[[^]]*\])?\{([^{}]+)\}", section_text)
    for reference in image_references:
        source = (ROOT / "everyday" / PurePosixPath(reference)).resolve()
        if target == "html" and source.suffix.lower() == ".pdf":
            source = source.with_suffix(".svg")
        paths.append(source)
    unique = sorted(set(path.resolve() for path in paths), key=lambda path: path.as_posix())
    missing = [sanitize(str(path)) for path in unique if not path.is_file()]
    if missing:
        raise BuildError(f"Required build inputs are missing: {missing}")
    return unique


def make_snapshot(destination: Path, target: str) -> list[dict[str, Any]]:
    reset_dir(destination)
    records: list[dict[str, Any]] = []
    source_hashes: dict[Path, str] = {}
    for source in input_paths(target):
        relative = source.relative_to(ROOT.resolve())
        payload = source.read_bytes()
        digest = sha256_bytes(payload)
        source_hashes[source] = digest
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(payload)
        records.append({"path": relative.as_posix(), "bytes": len(payload), "sha256": digest})
    changed = [rel(path) for path, digest in source_hashes.items() if sha256_path(path) != digest]
    if changed:
        raise BuildError(f"Build inputs changed while the snapshot was made: {changed}")
    return records


def provisional_pdf_metadata(main_path: Path, profile: str) -> None:
    if profile != "provisional":
        return
    text = main_path.read_text(encoding="utf-8-sig")
    marker = "\\usepackage{ee-edition}"
    if text.count(marker) != 1:
        raise BuildError("Could not place the provisional PDF metadata in the snapshot main.tex")
    addition = (
        marker
        + "\n\\hypersetup{pdfsubject={Provisional local build; not final QA or publication},"
        + "pdfkeywords={provisional, local build, do not publish}}"
    )
    main_path.write_text(text.replace(marker, addition, 1), encoding="utf-8", newline="\n")


PDF_BREAK_BEFORE_FORMULAS = (
    "NS-F-P035-041",
    "NS-F-P096-022",
    "NS-F-P136-001",
)

PDF_BOOKMARK_MATH = {
    "NS-F-P150-015": "p(s,1) + p(s,2) squared divided by p(s,1) > 2",
}


def apply_pdf_layout_hints(snapshot: Path) -> list[dict[str, str]]:
    """Add PDF-only layout and bookmark hints without changing manuscript bytes."""
    section_root = snapshot / "everyday" / "sections"
    applied: list[dict[str, str]] = []
    for identifier in PDF_BREAK_BEFORE_FORMULAS:
        token = rf"\NSi{{{identifier}}}{{"
        matches: list[Path] = []
        for path in sorted(section_root.glob("pp*.tex")):
            text = path.read_text(encoding="utf-8-sig")
            if token in text:
                matches.extend([path] * text.count(token))
        if len(matches) != 1:
            raise BuildError(f"Expected one PDF layout-hint target for {identifier}; found {len(matches)}")
        path = matches[0]
        text = path.read_text(encoding="utf-8-sig")
        path.write_text(
            text.replace(token, rf"\linebreak[4]{token}", 1),
            encoding="utf-8",
            newline="\n",
        )
        applied.append(
            {
                "formula_id": identifier,
                "section": path.relative_to(snapshot).as_posix(),
                "hint": r"\linebreak[4] before the unchanged inline formula",
            }
        )
    for identifier, bookmark_text in PDF_BOOKMARK_MATH.items():
        token = rf"\NSi{{{identifier}}}{{"
        matches: list[Path] = []
        for path in sorted(section_root.glob("pp*.tex")):
            text = path.read_text(encoding="utf-8-sig")
            if token in text:
                matches.extend([path] * text.count(token))
        if len(matches) != 1:
            raise BuildError(f"Expected one PDF bookmark-hint target for {identifier}; found {len(matches)}")
        path = matches[0]
        text = path.read_text(encoding="utf-8-sig")
        start = text.index(token)
        cursor = start + len(token)
        depth = 1
        while cursor < len(text) and depth:
            if text[cursor] == "{":
                depth += 1
            elif text[cursor] == "}":
                depth -= 1
            cursor += 1
        if depth:
            raise BuildError(f"Unbalanced PDF bookmark-hint target for {identifier}")
        visible = text[start:cursor]
        replacement = rf"\texorpdfstring{{{visible}}}{{{bookmark_text}}}"
        path.write_text(
            text[:start] + replacement + text[cursor:],
            encoding="utf-8",
            newline="\n",
        )
        applied.append(
            {
                "formula_id": identifier,
                "section": path.relative_to(snapshot).as_posix(),
                "hint": "PDF bookmark text for unchanged heading mathematics",
            }
        )
    return applied


def parse_pdf_log(log_text: str) -> dict[str, Any]:
    patterns = {
        "latex_errors": r"! LaTeX Error|Fatal error occurred|Emergency stop",
        "undefined_references": r"Reference .+ undefined|There were undefined references",
        "undefined_citations": r"Citation .+ undefined|There were undefined citations",
        "labels_changed": r"Label\(s\) may have changed|Rerun to get cross-references right",
        "multiply_defined": r"multiply defined",
        "duplicate_destinations": r"destination with the same identifier|duplicate destination",
        "overfull_boxes": r"Overfull \\[hv]box",
        "underfull_boxes": r"Underfull \\[hv]box",
        "missing_characters": r"Missing character:",
        "pdf_string_warnings": r"Token not allowed in a PDF string",
    }
    return {key: len(re.findall(pattern, log_text, flags=re.IGNORECASE)) for key, pattern in patterns.items()}


def pdf_page_count(path: Path) -> tuple[int, str]:
    command = require_tool("pdfinfo")
    result = run_command([command, path.name], cwd=path.parent, timeout=60)
    if result["exit_code"] != 0:
        raise BuildError("pdfinfo could not inspect the PDF")
    match = re.search(r"^Pages:\s+(\d+)\s*$", result["output"], flags=re.MULTILINE)
    if match is None:
        raise BuildError("pdfinfo did not report a page count")
    return int(match.group(1)), result["output"]


def build_pdf(profile: str) -> dict[str, Any]:
    require_tool("pdflatex")
    stage = TMP_ROOT / "pdf"
    reset_dir(stage)
    snapshot = stage / "snapshot"
    input_records = make_snapshot(snapshot, "pdf")
    provisional_pdf_metadata(snapshot / "everyday" / "main.tex", profile)
    layout_hints = apply_pdf_layout_hints(snapshot)
    runs = []
    produced: list[Path] = []
    log_payloads: list[str] = []
    for run_name in ("pass-a", "pass-b"):
        run_root = stage / run_name
        source_root = run_root / "source"
        output_dir = run_root / "out"
        shutil.copytree(snapshot, source_root)
        output_dir.mkdir(parents=True)
        command = [
            require_tool("pdflatex"),
            "-interaction=nonstopmode",
            "-halt-on-error",
            "-file-line-error",
            "-no-shell-escape",
            "-recorder",
            "-jobname=" + CONFIG["job_name"],
            "-output-directory=../../out",
            "main.tex",
        ]
        pass_records = []
        combined = []
        for pass_number in range(1, int(CONFIG["pdf_passes"]) + 1):
            result = run_command(
                command,
                cwd=source_root / "everyday",
                timeout=int(CONFIG["timeouts_seconds"]["pdf_pass"]),
            )
            combined.append(f"===== pass {pass_number} =====\n{result['output']}")
            pass_records.append({key: result[key] for key in ("command", "cwd", "exit_code", "timed_out")})
            if result["timed_out"] or result["exit_code"] != 0:
                write_text(LOGS / f"pdf-{run_name}.console.txt", "\n".join(combined))
                raise BuildError(f"pdflatex failed during {run_name}, pass {pass_number}")
        console = "\n".join(combined)
        write_text(LOGS / f"pdf-{run_name}.console.txt", console)
        pdf_path = output_dir / f"{CONFIG['job_name']}.pdf"
        log_path = output_dir / f"{CONFIG['job_name']}.log"
        if not pdf_path.is_file() or not log_path.is_file():
            raise BuildError(f"pdflatex did not produce the expected PDF and log during {run_name}")
        log_text = sanitize(log_path.read_text(encoding="utf-8", errors="replace"))
        write_text(LOGS / f"pdf-{run_name}.log", log_text)
        counts = parse_pdf_log(log_text)
        fatal_keys = (
            "latex_errors",
            "undefined_references",
            "undefined_citations",
            "labels_changed",
            "multiply_defined",
            "duplicate_destinations",
            "missing_characters",
        )
        if any(counts[key] for key in fatal_keys):
            raise BuildError(f"The {run_name} PDF log contains release-blocking findings: {counts}")
        produced.append(pdf_path)
        log_payloads.append(log_text)
        runs.append(
            {
                "name": run_name,
                "passes": pass_records,
                "pdf": file_record(pdf_path, base=run_root),
                "log_counts": counts,
                "console_log": rel(LOGS / f"pdf-{run_name}.console.txt"),
                "tex_log": rel(LOGS / f"pdf-{run_name}.log"),
            }
        )
    hashes = [sha256_path(path) for path in produced]
    if len(set(hashes)) != 1:
        raise BuildError(f"The two clean PDF builds differ: {hashes}")
    final_counts = parse_pdf_log(log_payloads[-1])
    if profile == "final" and final_counts["overfull_boxes"]:
        raise BuildError("The final profile requires zero overfull boxes")
    page_count, info = pdf_page_count(produced[-1])
    if page_count < 166:
        raise BuildError(f"The PDF has {page_count} pages, fewer than the 166 source-page anchors")
    PDF_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(produced[-1], PDF_OUTPUT)
    write_text(LOGS / "pdfinfo.txt", info)
    receipt = {
        "schema": "navier-stokes-everyday-pdf-build/v1",
        "profile": profile,
        "status": "provisional_pass" if profile == "provisional" else "pass",
        "notice": CONFIG["provisional_notice"] if profile == "provisional" else None,
        "entrypoint": CONFIG["entrypoint"],
        "inputs": input_records,
        "snapshot_layout_hints": layout_hints,
        "runs": runs,
        "deterministic_rebuilds": 2,
        "byte_identical": True,
        "page_count": page_count,
        "output": file_record(PDF_OUTPUT),
        "pdfinfo_log": rel(LOGS / "pdfinfo.txt"),
        "limitations": (
            "This build tests the pipeline only. It does not replace the single full-book QA pass or rendered-page acceptance."
            if profile == "provisional" else None
        ),
    }
    write_json(RECEIPTS / "pdf-build.json", receipt)
    return receipt


WEB_PREAMBLE = r"""\documentclass[10pt]{article}
\usepackage{amsmath,amssymb,amsthm,mathtools,mathrsfs,hyperref,graphicx}
\newtheorem{theorem}{Theorem}[section]
\newtheorem{proposition}[theorem]{Proposition}
\newtheorem{lemma}[theorem]{Lemma}
\newtheorem{corollary}[theorem]{Corollary}
\newtheorem{claim}[theorem]{Claim}
\theoremstyle{definition}
\newtheorem{definition}[theorem]{Definition}
\newtheorem{construction}[theorem]{Construction}
\theoremstyle{remark}
\newtheorem{remark}[theorem]{Remark}
\newtheorem{notation}[theorem]{Notation}
\newcommand{\NSPage}[1]{\hypertarget{source-page-#1}{}}
\newcommand{\NSi}[2]{\hypertarget{formula-#1}{}\ensuremath{#2}}
\newcommand{\NSFormula}[3]{\hypertarget{formula-#1}{}}
\newcommand{\R}{\mathbb{R}}
\newcommand{\T}{\mathbb{T}}
\newcommand{\N}{\mathbb{N}}
\newcommand{\Z}{\mathbb{Z}}
\newcommand{\supp}{\operatorname{supp}}
\newcommand{\divergence}{\operatorname{div}}
\newcommand{\curl}{\operatorname{curl}}
\newcommand{\sgn}{\operatorname{sgn}}
\newcommand{\Id}{\operatorname{Id}}
"""


def source_document_text(source_root: Path) -> str:
    main_path = source_root / "everyday" / "main.tex"
    main_text = main_path.read_text(encoding="utf-8-sig")
    ranges = main_ranges(main_text)
    if ranges != CONFIG["expected_ranges"]:
        raise BuildError("The web source range order differs from build-config.json")

    def expand(match: re.Match[str]) -> str:
        range_name = match.group(1)
        section_path = source_root / "everyday" / "sections" / f"{range_name}.tex"
        return section_path.read_text(encoding="utf-8-sig")

    begin = main_text.find(r"\begin{document}")
    end = main_text.rfind(r"\end{document}")
    if begin < 0 or end <= begin:
        raise BuildError("The web build could not locate the document body")
    body = main_text[begin + len(r"\begin{document}"):end]
    expanded = INPUT_RE.sub(expand, body)
    if INPUT_RE.search(expanded):
        raise BuildError("One or more section inputs were not expanded")
    return expanded


def source_anchor_inventory(source_root: Path) -> dict[str, Any]:
    text = strip_tex_comments(source_document_text(source_root))
    labels = re.findall(r"\\label\{([^{}]+)\}", text)
    formulas = re.findall(r"\\NS(?:i|Formula)\{(NS-F-P\d{3}-\d{3})\}", text)
    pages = re.findall(r"\\NSPage\{(\d{3})\}", text)
    segments = re.findall(r"\\begin\{EESegment\}\{([^{}]+)\}", text)
    figures = re.findall(r"\\NSFigurePlaceholder\{([^{}]+)\}", text)
    bibitems = re.findall(r"\\bibitem(?:\[[^]]*\])?\{([^{}]+)\}", text)
    collections = {
        "labels": labels,
        "formulas": formulas,
        "pages": pages,
        "segments": segments,
        "figures": figures,
        "bibitems": bibitems,
    }
    duplicates = {
        name: sorted(value for value, count in Counter(values).items() if count > 1)
        for name, values in collections.items()
    }
    duplicates = {name: values for name, values in duplicates.items() if values}
    if duplicates:
        raise BuildError(f"Duplicate web anchor sources: {duplicates}")
    return collections


def citation_markup(keys: list[str], numbers: dict[str, int], note: str | None) -> str:
    linked = []
    for key in keys:
        if key not in numbers:
            raise BuildError(f"Citation has no bibliography item: {key}")
        linked.append(rf"\hyperlink{{bib-{key}}}{{{numbers[key]}}}")
    content = ", ".join(linked)
    if note:
        content += ", " + note
    return "[" + content + "]"


def prepare_web_source(source_root: Path) -> tuple[str, dict[str, Any]]:
    text = source_document_text(source_root)
    inventory = source_anchor_inventory(source_root)
    # These two TeX groups only localize the symbol-table font and spacing in
    # the PDF. Pandoc delays every tabular inside the group until \endgroup and
    # then keeps only the last table. Removing the formatting-only group from
    # the web input lets all six source-page table blocks be converted in place.
    if text.count(r"\begingroup") != 1 or text.count(r"\endgroup") != 1:
        raise BuildError("The web source no longer has the expected symbol-table formatting group")
    text = text.replace(r"\begingroup", "", 1).replace(r"\endgroup", "", 1)
    symbol_table_groups: list[str] = []

    def symbol_table_group_row(match: re.Match[str]) -> str:
        title = match.group(1)
        symbol_table_groups.append(title)
        # Pandoc drops a whole LaTeX tabular when it contains \multicolumn.
        # Give it three ordinary cells here; postprocessing restores a single
        # semantic row header spanning all three columns.
        return rf"\textbf{{{title}}} & {{}} & {{}} \\"

    text = re.sub(
        r"\\multicolumn\{3\}\{@\{\}l\}\{\\textbf\{([^{}]+)\}\}\\\\",
        symbol_table_group_row,
        text,
    )
    if len(symbol_table_groups) != 6:
        raise BuildError(
            f"Expected six group headings in the source-page 19--23 symbol tables; found {len(symbol_table_groups)}"
        )
    # Pandoc discards content placed between \begin{enumerate} and the first
    # \item. Two source-page markers occur there. Move each marker just inside
    # the first item so its position in the reading order stays unchanged.
    text, moved_list_page_anchors = re.subn(
        r"(\\begin\{enumerate\}(?:\[[^]\r\n]*\])?\s*)(\\NSPage\{\d{3}\}%?\s*)(\\item\b)",
        lambda match: match.group(1) + match.group(3) + "\n" + match.group(2),
        text,
    )
    if moved_list_page_anchors != 2:
        raise BuildError(
            f"Expected two source-page markers before first list items; found {moved_list_page_anchors}"
        )
    labels = inventory["labels"]
    label_numbers: dict[str, str] = {}
    allowed_prefixes = {"cor", "def", "eq", "fig", "lem", "prop", "rem", "sec", "tab", "thm"}
    figure_labels = [label for label in labels if label.startswith("fig:")]
    table_labels = [label for label in labels if label.startswith("tab:")]
    figure_label_numbers = {label: str(index) for index, label in enumerate(figure_labels, start=1)}
    table_label_numbers = {label: str(index) for index, label in enumerate(table_labels, start=1)}
    for label in labels:
        if ":" not in label:
            raise BuildError(f"A label does not use the expected prefix separator: {label}")
        prefix, number = label.split(":", 1)
        if prefix not in allowed_prefixes or not number:
            raise BuildError(f"A label cannot be converted into a web reference: {label}")
        if prefix == "fig":
            label_numbers[label] = figure_label_numbers[label]
        elif prefix == "tab":
            label_numbers[label] = table_label_numbers[label]
        else:
            label_numbers[label] = number

    equation_tags = re.findall(r"\\tag\{([^{}]+)\}", text)
    equation_label_numbers = [label.split(":", 1)[1] for label in labels if label.startswith("eq:")]
    if Counter(equation_tags) != Counter(equation_label_numbers):
        raise BuildError("Equation tags and equation-label numbers differ")

    segment_starts = len(re.findall(r"\\begin\{EESegment\}\{", text))
    segment_ends = text.count(r"\end{EESegment}")
    if segment_starts != segment_ends:
        raise BuildError("EESegment boundaries are not balanced")
    text = re.sub(
        r"\\begin\{EESegment\}\{([^{}]+)\}",
        lambda match: rf"\hypertarget{{{match.group(1)}}}{{}}",
        text,
    )
    text = text.replace(r"\end{EESegment}", "")

    addition_starts = len(re.findall(r"\\begin\{EEAddition\}", text))
    addition_ends = text.count(r"\end{EEAddition}")
    if addition_starts != addition_ends:
        raise BuildError("EEAddition boundaries are not balanced")
    text, additions = re.subn(
        r"\\begin\{EEAddition\}\{([^{}]+)\}\{([^{}]+)\}",
        lambda match: (
            rf"\begin{{quotation}}\hypertarget{{{match.group(1)}}}{{}}"
            rf"\textbf{{Everyday English note: {match.group(2)}}}\par"
        ),
        text,
    )
    if additions != addition_starts:
        raise BuildError("An EEAddition title contains unsupported nested braces")
    text = text.replace(r"\end{EEAddition}", r"\end{quotation}")

    edition_images: list[dict[str, str]] = []

    def edition_image_markup(match: re.Match[str]) -> str:
        options = match.group(1) or ""
        reference = PurePosixPath(match.group(2))
        if not reference.as_posix().startswith("illustrations/"):
            return match.group(0)
        source_reference = reference.with_suffix(".svg") if reference.suffix.lower() == ".pdf" else reference
        source = source_root / "everyday" / source_reference
        if not source.is_file():
            raise BuildError(f"The web counterpart for an edition illustration is missing: {source_reference}")
        target = PurePosixPath("assets") / "illustrations" / source_reference.name
        edition_images.append(
            {"source": source_reference.as_posix(), "target": target.as_posix()}
        )
        return rf"\includegraphics{options}{{{target.as_posix()}}}"

    text = re.sub(
        r"\\includegraphics(\[[^]]*\])?\{([^{}]+)\}",
        edition_image_markup,
        text,
    )

    configured_figures = CONFIG["figures"]
    used_figures: list[str] = []

    def figure_markup(match: re.Match[str]) -> str:
        figure_id = match.group(1)
        filename = configured_figures.get(figure_id)
        if filename is None:
            raise BuildError(f"No SVG web asset is configured for {figure_id}")
        used_figures.append(figure_id)
        return rf"\includegraphics[width=0.96\linewidth]{{assets/figures/{filename}}}"

    text = re.sub(r"\\NSFigurePlaceholder\{([^{}]+)\}", figure_markup, text)
    if sorted(used_figures) != sorted(configured_figures):
        raise BuildError("The web figure use does not match build-config.json")

    bibitems = inventory["bibitems"]
    bib_numbers = {key: index for index, key in enumerate(bibitems, start=1)}

    def cite_markup(match: re.Match[str]) -> str:
        note = match.group(1)
        keys = [part.strip() for part in match.group(2).split(",") if part.strip()]
        return citation_markup(keys, bib_numbers, note)

    text = re.sub(r"\\cite(?:\[([^]]*)\])?\{([^{}]+)\}", cite_markup, text)

    def reference_markup(match: re.Match[str]) -> str:
        command = match.group(1)
        keys = [part.strip() for part in match.group(2).split(",") if part.strip()]
        rendered = []
        for key in keys:
            if key not in label_numbers:
                raise BuildError(f"Reference has no label: {key}")
            number = label_numbers[key]
            if command == "eqref":
                number = f"({number})"
            rendered.append(rf"\hyperlink{{{key}}}{{{number}}}")
        return ", ".join(rendered)

    text = re.sub(r"\\(eqref|ref)\{([^{}]+)\}", reference_markup, text)

    moved_equation_labels = 0

    def move_equation_label(match: re.Match[str]) -> str:
        nonlocal moved_equation_labels
        environment = match.group(1)
        contents = match.group(2)
        equation_labels = re.findall(r"\\label\{(eq:[^{}]+)\}", contents)
        if not equation_labels:
            return match.group(0)
        if len(equation_labels) != 1:
            raise BuildError("A numbered display contains more than one equation label")
        label = equation_labels[0]
        contents = re.sub(r"\\label\{eq:[^{}]+\}", "", contents, count=1)
        moved_equation_labels += 1
        return rf"\hypertarget{{{label}}}{{}}\begin{{{environment}}}{contents}\end{{{environment}}}"

    text = re.sub(
        r"\\begin\{(equation|align)\}([\s\S]*?)\\end\{\1\}",
        move_equation_label,
        text,
    )
    if moved_equation_labels != len(equation_label_numbers):
        raise BuildError(
            f"Only {moved_equation_labels} of {len(equation_label_numbers)} equation labels were moved outside their displays"
        )
    text = re.sub(
        r"\\label\{([^{}]+)\}",
        lambda match: rf"\hypertarget{{{match.group(1)}}}{{}}",
        text,
    )
    text = re.sub(
        r"\\begin\{thebibliography\}\{[^{}]+\}",
        lambda _: r"\section*{References}\begin{enumerate}",
        text,
    )

    def bibitem_markup(match: re.Match[str]) -> str:
        key = match.group(1)
        if key not in bib_numbers:
            raise BuildError(f"Unexpected bibliography item: {key}")
        return rf"\item \hypertarget{{bib-{key}}}{{}}"

    text = re.sub(r"\\bibitem(?:\[[^]]*\])?\{([^{}]+)\}", bibitem_markup, text)
    text = text.replace(r"\end{thebibliography}", r"\end{enumerate}")
    text = text.replace(r"\rule[0.5ex]{2em}{0.4pt}", "---")

    forbidden = {
        "EESegment-start": r"\\begin\{EESegment\}",
        "EESegment-end": r"\\end\{EESegment\}",
        "EEAddition-start": r"\\begin\{EEAddition\}",
        "EEAddition-end": r"\\end\{EEAddition\}",
        "figure-placeholder": r"\\NSFigurePlaceholder\{",
        "label": r"\\label\{",
        "reference": r"\\(?:ref|eqref)\{",
        "citation": r"\\cite(?:\[[^]]*\])?\{",
        "bibliography-item": r"\\bibitem(?:\[[^]]*\])?\{",
    }
    remaining = [name for name, pattern in forbidden.items() if re.search(pattern, text)]
    if remaining:
        raise BuildError(f"Unsupported web source commands remain: {remaining}")

    generated = WEB_PREAMBLE + "\n\\begin{document}\n" + text + "\n\\end{document}\n"
    report = {
        "labels": len(labels),
        "equation_tags": len(equation_tags),
        "bibliography_items": len(bibitems),
        "figures": len(used_figures),
        "segments": len(inventory["segments"]),
        "formula_anchors": len(inventory["formulas"]),
        "source_page_anchors": len(inventory["pages"]),
        "symbol_table_groups": symbol_table_groups,
        "list_page_anchors_moved_inside_first_item": moved_list_page_anchors,
        "edition_images": edition_images,
        "label_numbers": label_numbers,
        "inventory": inventory,
    }
    return generated, report


def normalized_text(element: Any) -> str:
    return " ".join(element.text_content().split())


def class_tokens(element: Any) -> set[str]:
    return set((element.get("class") or "").split())


def normalize_visible_name_punctuation(document: Any) -> int:
    """Render TeX's double hyphen as the intended en dash in screen text."""

    old = "Navier--Stokes"
    new = "Navier–Stokes"
    replacements = 0
    for element in document.iter():
        local_name = str(element.tag).rsplit("}", 1)[-1]
        if element.text and local_name != "annotation":
            replacements += element.text.count(old)
            element.text = element.text.replace(old, new)
        if element.tail:
            replacements += element.tail.count(old)
            element.tail = element.tail.replace(old, new)
    return replacements


def nearest_figure(element: Any) -> Any | None:
    current = element.getparent()
    while current is not None:
        if current.tag == "figure" or "figure" in class_tokens(current):
            return current
        current = current.getparent()
    return None


MATHML_NAMESPACE = "http://www.w3.org/1998/Math/MathML"


def wrap_mathml_semantics(math: Any, source: str) -> Any:
    from lxml import etree

    children = list(math)
    for child in children:
        math.remove(child)
    semantics = etree.SubElement(math, f"{{{MATHML_NAMESPACE}}}semantics")
    for child in children:
        semantics.append(child)
    annotation = etree.SubElement(semantics, f"{{{MATHML_NAMESPACE}}}annotation")
    annotation.set("encoding", "application/x-tex")
    annotation.text = source
    math.set("display", "block")
    return math


def fallback_mathml(source: str) -> Any:
    from latex2mathml.converter import convert
    from lxml import etree

    original = source.strip()
    latex = original
    if latex.startswith("$$") and latex.endswith("$$"):
        latex = latex[2:-2].strip()
    environment_match = re.fullmatch(
        r"\\begin\{(equation|align)\}([\s\S]*?)\\end\{\1\}",
        latex,
    )
    environment = environment_match.group(1) if environment_match else None
    body = environment_match.group(2) if environment_match else latex
    body = re.sub(r"\\tag\{[^{}]+\}", "", body)
    body = body.replace(r"\notag", "")

    if environment == "align":
        math = etree.Element(f"{{{MATHML_NAMESPACE}}}math", nsmap={None: MATHML_NAMESPACE})
        math.set("display", "block")
        semantics = etree.SubElement(math, f"{{{MATHML_NAMESPACE}}}semantics")
        table = etree.SubElement(semantics, f"{{{MATHML_NAMESPACE}}}mtable")
        rows = [row.strip() for row in re.split(r"\\\\(?:\[[^]]*\])?", body) if row.strip()]
        for row in rows:
            table_row = etree.SubElement(table, f"{{{MATHML_NAMESPACE}}}mtr")
            cells = row.split("&")
            for cell in cells:
                table_cell = etree.SubElement(table_row, f"{{{MATHML_NAMESPACE}}}mtd")
                converted = etree.fromstring(convert(cell.strip(), display="inline").encode("utf-8"))
                for child in list(converted):
                    table_cell.append(child)
        annotation = etree.SubElement(semantics, f"{{{MATHML_NAMESPACE}}}annotation")
        annotation.set("encoding", "application/x-tex")
        annotation.text = latex
        return math

    converted = etree.fromstring(convert(body.strip(), display="block").encode("utf-8"))
    return wrap_mathml_semantics(converted, latex)


def postprocess_html(
    raw_html: Path,
    destination: Path,
    snapshot: Path,
    profile: str,
    web_report: dict[str, Any],
) -> dict[str, Any]:
    from lxml import etree
    from lxml import html as lxml_html

    parser = lxml_html.HTMLParser(encoding="utf-8")
    document = lxml_html.parse(str(raw_html), parser).getroot()
    document.set("lang", CONFIG["language"])
    document.set("{http://www.w3.org/XML/1998/namespace}lang", CONFIG["language"])
    head = document.find("head")
    body = document.find("body")
    if head is None or body is None:
        raise BuildError("Pandoc output lacks a head or body element")
    title = head.find("title")
    if title is None:
        title = etree.SubElement(head, "title")
    title.text = CONFIG["title"]
    for old in head.xpath("./meta[@name='description' or @name='generator'] | ./style | ./link[@rel='stylesheet']"):
        old.getparent().remove(old)
    description = etree.SubElement(head, "meta")
    description.set("name", "description")
    description.set("content", "A complete mathematics-preserving edition in Everyday English.")
    css_link = etree.SubElement(head, "link")
    css_link.set("rel", "stylesheet")
    css_link.set("href", "accessibility.css")

    original_children = list(body)
    for child in original_children:
        body.remove(child)
    skip = etree.SubElement(body, "a")
    skip.set("class", "skip-link")
    skip.set("href", "#main-content")
    skip.text = "Skip to the proof"
    header = etree.SubElement(body, "header")
    heading = etree.SubElement(header, "h1")
    heading.text = CONFIG["title"]
    if profile == "provisional":
        status = etree.SubElement(header, "p")
        status.set("class", "build-status")
        status.set("role", "status")
        status.text = CONFIG["provisional_notice"]
    main = etree.SubElement(body, "main")
    main.set("id", "main-content")
    for child in original_children:
        main.append(child)
    footer = etree.SubElement(body, "footer")
    footer.text = (
        "Provisional local build. Exact file hashes and validation results are stored with the build receipts."
        if profile == "provisional"
        else "Exact file hashes and validation results are stored with the build receipts."
    )

    # Pandoc copies a formula marker from a section heading into the generated
    # contents list. Keep the formula there, but let only the real heading own
    # the stable formula ID.
    toc_formula_ids_removed = 0
    for clone in document.xpath("//*[@id='TOC']//*[@id]"):
        if (clone.get("id") or "").startswith("formula-"):
            clone.attrib.pop("id", None)
            toc_formula_ids_removed += 1

    for anchor in document.xpath("//*[@name and not(@id)]"):
        anchor.set("id", anchor.get("name"))

    label_numbers = web_report["label_numbers"]
    section_numbers = 0
    theorem_numbers = 0
    figure_numbers = 0
    theorem_names = {
        "cor": ("corollary", "Corollary"),
        "def": ("definition", "Definition"),
        "lem": ("lemma", "Lemma"),
        "prop": ("proposition", "Proposition"),
        "rem": ("remark", "Remark"),
        "thm": ("theorem", "Theorem"),
    }
    for anchor in document.xpath("//*[@id]"):
        identifier = anchor.get("id") or ""
        tokens = class_tokens(anchor)
        if identifier.startswith("source-page-"):
            tokens.add("source-page-marker")
            anchor.set("role", "doc-pagebreak")
            anchor.set("aria-label", "Source page " + identifier.rsplit("-", 1)[-1].lstrip("0"))
        elif identifier.startswith("EE-TGT-"):
            tokens.add("ee-segment-anchor")
            anchor.set("aria-hidden", "true")
        elif identifier.startswith("formula-"):
            tokens.add("formula-anchor")
            anchor.set("aria-hidden", "true")
        elif identifier in label_numbers or identifier.startswith("bib-"):
            tokens.add("cross-reference-anchor")
            anchor.set("aria-hidden", "true")
        if tokens:
            anchor.set("class", " ".join(sorted(tokens)))

        if identifier.startswith("sec:") and identifier in label_numbers:
            heading = anchor.getprevious()
            if heading is not None and heading.tag in {"h2", "h3", "h4", "h5", "h6"}:
                number = label_numbers[identifier]
                heading.set("data-number", number)
                number_spans = heading.xpath(
                    ".//span[contains(concat(' ', normalize-space(@class), ' '), ' header-section-number ')]"
                )
                if number_spans:
                    number_spans[0].text = number
                section_numbers += 1

        prefix = identifier.split(":", 1)[0]
        if prefix in theorem_names and identifier in label_numbers:
            expected_class, display_name = theorem_names[prefix]
            container = anchor
            while container is not None and expected_class not in class_tokens(container):
                container = container.getparent()
            if container is not None:
                heading_marks = container.xpath(".//*[self::strong or self::em][1]")
                if heading_marks:
                    heading_marks[0].text = f"{display_name} {label_numbers[identifier]}"
                    theorem_numbers += 1

        if identifier.startswith("fig:") and identifier in label_numbers:
            container = anchor
            while container is not None and container.tag != "figure":
                container = container.getparent()
            if container is not None:
                captions = container.xpath(".//figcaption")
                if captions:
                    caption = captions[-1]
                    existing_text = caption.text
                    caption.text = None
                    number = etree.Element("strong")
                    number.text = f"Figure {label_numbers[identifier]}. "
                    number.tail = existing_text
                    caption.insert(0, number)
                    figure_numbers += 1

    expected_sections = sum(1 for label in label_numbers if label.startswith("sec:"))
    expected_theorems = sum(1 for label in label_numbers if label.split(":", 1)[0] in theorem_names)
    expected_figures = sum(1 for label in label_numbers if label.startswith("fig:"))
    if section_numbers != expected_sections:
        raise BuildError(f"Only {section_numbers} of {expected_sections} section numbers were corrected in HTML")
    if theorem_numbers != expected_theorems:
        raise BuildError(f"Only {theorem_numbers} of {expected_theorems} theorem numbers were corrected in HTML")
    if figure_numbers != expected_figures:
        raise BuildError(f"Only {figure_numbers} of {expected_figures} figure numbers were added in HTML")

    raw_math_converted = 0
    raw_math_nodes = document.xpath(
        "//*[self::span and contains(concat(' ', normalize-space(@class), ' '), ' math ') "
        "and contains(concat(' ', normalize-space(@class), ' '), ' display ')]"
    )
    for raw_math in raw_math_nodes:
        source = raw_math.text_content()
        try:
            math = fallback_mathml(source)
        except Exception as exc:
            raise BuildError(f"The MathML fallback could not convert a display: {source[:120]!r}") from exc
        math.tail = raw_math.tail
        raw_math.getparent().replace(raw_math, math)
        raw_math_converted += 1

    equation_numbers = 0
    for math in document.xpath("//*[local-name()='math' and @display='block']"):
        annotations = math.xpath(".//*[local-name()='annotation' and @encoding='application/x-tex']/text()")
        if not annotations:
            continue
        tag = re.search(r"\\tag\{([^{}]+)\}", annotations[0])
        if tag is None:
            continue
        container = math.getparent()
        position = container.index(math)
        following_text = math.tail
        math.tail = None
        equation = etree.Element("span")
        equation.set("class", "equation-block")
        equation.set("role", "group")
        equation.set("aria-label", f"Equation {tag.group(1)}")
        container.remove(math)
        equation.append(math)
        number = etree.Element("span")
        number.set("class", "equation-number")
        number.set("aria-label", f"Equation {tag.group(1)}")
        number.text = f"({tag.group(1)})"
        equation.append(number)
        equation.tail = following_text
        container.insert(position, equation)
        equation_numbers += 1
    if equation_numbers != web_report["equation_tags"]:
        raise BuildError(
            f"Only {equation_numbers} of {web_report['equation_tags']} equation numbers were rendered in HTML"
        )

    name_punctuation_replacements = normalize_visible_name_punctuation(document)

    output_dir = destination.parent
    figure_output = output_dir / "assets" / "figures"
    figure_output.mkdir(parents=True, exist_ok=True)
    figures = 0
    configured_by_name = {filename: figure_id for figure_id, filename in CONFIG["figures"].items()}
    edition_by_target = {item["target"]: item for item in web_report["edition_images"]}
    copied_figures: set[str] = set()
    copied_editions: set[str] = set()
    for image in document.xpath("//img"):
        source_value = urllib.parse.unquote(image.get("src") or "")
        filename = PurePosixPath(source_value).name
        figure_id = configured_by_name.get(filename)
        edition_item = edition_by_target.get(PurePosixPath(source_value).as_posix())
        if figure_id is None and edition_item is None:
            continue
        if edition_item is not None:
            source = snapshot / "everyday" / PurePosixPath(edition_item["source"])
            target = output_dir / PurePosixPath(edition_item["target"])
            target.parent.mkdir(parents=True, exist_ok=True)
            data_attribute = "data-edition-illustration"
            data_value = Path(edition_item["source"]).stem
            copied_editions.add(edition_item["target"])
        else:
            source = snapshot / "reconstruction" / "assets" / "figures" / filename
            target = figure_output / filename
            data_attribute = "data-source-figure"
            data_value = figure_id or ""
            copied_figures.add(data_value)
        if not source.is_file():
            raise BuildError(f"A web figure asset is missing: {source_value}")
        shutil.copyfile(source, target)
        container = nearest_figure(image)
        caption = None
        if container is not None:
            if container.tag != "figure":
                container.tag = "figure"
            captions = container.xpath(
                ".//*[self::figcaption or contains(concat(' ', normalize-space(@class), ' '), ' caption ')]"
            )
            if captions:
                caption = captions[-1]
                caption.tag = "figcaption"
        if caption is not None:
            alt = normalized_text(caption)
        elif figure_id is not None:
            alt = f"Original paper {figure_id}."
        else:
            raise BuildError(f"An edition illustration has no caption: {source_value}")
        image.set("src", PurePosixPath(source_value).as_posix())
        image.set("alt", alt)
        image.set(data_attribute, data_value)
        image.set("loading", "lazy")
        figures += 1
    if copied_figures != set(CONFIG["figures"]):
        raise BuildError(f"The HTML figure set is incomplete: {sorted(copied_figures)}")
    if copied_editions != set(edition_by_target):
        raise BuildError(f"The HTML edition-illustration set is incomplete: {sorted(copied_editions)}")

    tables = document.xpath("//table")
    symbol_table_groups = set(web_report["symbol_table_groups"])
    restored_symbol_group_rows = 0
    for table in tables:
        rows = table.xpath(".//tr")
        if not rows:
            table.set("role", "presentation")
            continue
        first_cells = rows[0].xpath("./th|./td")
        first_text = " ".join(normalized_text(cell) for cell in first_cells)
        if "Symbol" in first_text and "Meaning" in first_text:
            for cell in first_cells:
                cell.tag = "th"
                cell.set("scope", "col")
        elif not table.xpath(".//th"):
            table.set("role", "presentation")
        for row in rows:
            cells = row.xpath("./th|./td")
            texts = [normalized_text(cell) for cell in cells]
            if len(cells) == 3 and texts[0] in symbol_table_groups and not texts[1] and not texts[2]:
                cells[0].tag = "th"
                cells[0].set("scope", "rowgroup")
                cells[0].set("colspan", "3")
                cells[0].set("class", "symbol-group-heading")
                row.remove(cells[1])
                row.remove(cells[2])
                restored_symbol_group_rows += 1
    if restored_symbol_group_rows != len(symbol_table_groups):
        raise BuildError(
            "Not every symbol-table group heading became a spanning semantic row header"
        )

    math_nodes = document.xpath("//*[local-name()='math']")
    for math in math_nodes:
        math.set("role", "math")

    payload = etree.tostring(
        document,
        encoding="utf-8",
        method="html",
        doctype="<!DOCTYPE html>",
        pretty_print=False,
    )
    text_payload = sanitize(payload.decode("utf-8"))
    write_text(destination, text_payload)
    shutil.copyfile(snapshot / CONFIG["web_css"], output_dir / "accessibility.css")
    return {
        "figures": figures,
        "mathml_elements": len(math_nodes),
        "tables": len(tables),
        "symbol_table_group_rows": restored_symbol_group_rows,
        "equation_numbers": equation_numbers,
        "name_punctuation_replacements": name_punctuation_replacements,
        "section_numbers": section_numbers,
        "theorem_numbers": theorem_numbers,
        "fallback_mathml_displays": raw_math_converted,
        "toc_formula_ids_removed": toc_formula_ids_removed,
    }


def build_html(profile: str) -> dict[str, Any]:
    require_tool("pandoc")
    stage = TMP_ROOT / "html"
    reset_dir(stage)
    snapshot = stage / "snapshot"
    input_records = make_snapshot(snapshot, "html")
    generated_text, web_report = prepare_web_source(snapshot)
    generated = stage / "expanded-web.tex"
    write_text(generated, generated_text)
    runs = []
    rendered_roots: list[Path] = []
    tree_hashes: list[list[tuple[str, str]]] = []
    for run_name in ("pass-a", "pass-b"):
        raw_html = stage / f"{run_name}.raw.html"
        rendered_root = stage / "rendered" / run_name
        destination = rendered_root / "index.html"
        command = [
            require_tool("pandoc"),
            generated.name,
            "--from=latex+raw_tex",
            "--to=html5",
            "--standalone",
            "--mathml",
            "--toc",
            "--toc-depth=3",
            "--number-sections",
            "--shift-heading-level-by=1",
            "--wrap=none",
            "--metadata=pagetitle:" + CONFIG["title"],
            "--output=" + raw_html.name,
        ]
        result = run_command(
            command,
            cwd=stage,
            timeout=int(CONFIG["timeouts_seconds"]["html"]),
        )
        console_log = LOGS / f"html-{run_name}.console.txt"
        write_text(console_log, result["output"])
        if result["timed_out"] or result["exit_code"] != 0 or not raw_html.is_file():
            raise BuildError(f"Pandoc did not complete the semantic HTML build during {run_name}")
        postprocess = postprocess_html(raw_html, destination, snapshot, profile, web_report)
        checks = validate_html(destination, expected=web_report["inventory"])
        if checks["status"] != "pass":
            raise BuildError(f"HTML validation failed during {run_name}: {checks['issues'][:10]}")
        output_files = sorted(path for path in rendered_root.rglob("*") if path.is_file())
        tree_hash = [
            (path.relative_to(rendered_root).as_posix(), sha256_path(path))
            for path in output_files
        ]
        tree_hashes.append(tree_hash)
        rendered_roots.append(rendered_root)
        runs.append(
            {
                "name": run_name,
                "command": {key: result[key] for key in ("command", "cwd", "exit_code", "timed_out")},
                "console_log": rel(console_log),
                "postprocess": postprocess,
                "validation": checks,
                "outputs": [file_record(path, base=rendered_root) for path in output_files],
            }
        )
    if tree_hashes[0] != tree_hashes[1]:
        raise BuildError("The two clean HTML builds differ")
    if HTML_OUTPUT.parent.exists():
        ensure_child(OUTPUT_ROOT, HTML_OUTPUT.parent)
        shutil.rmtree(HTML_OUTPUT.parent)
    shutil.copytree(rendered_roots[-1], HTML_OUTPUT.parent)
    output_files = sorted(path for path in HTML_OUTPUT.parent.rglob("*") if path.is_file())
    receipt = {
        "schema": "navier-stokes-everyday-html-build/v1",
        "profile": profile,
        "status": "provisional_pass" if profile == "provisional" else "pass",
        "notice": CONFIG["provisional_notice"] if profile == "provisional" else None,
        "inputs": input_records,
        "generated_entrypoint_sha256": sha256_path(generated),
        "source_conversion": {
            key: value for key, value in web_report.items() if key not in {"inventory", "label_numbers"}
        },
        "runs": runs,
        "deterministic_rebuilds": 2,
        "byte_identical_output_trees": True,
        "outputs": [file_record(path) for path in output_files],
        "formula_access": "Native MathML is retained, and each formula keeps its TeX source in a MathML annotation. No separately checked spoken rendering is claimed.",
    }
    write_json(RECEIPTS / "html-build.json", receipt)
    return receipt


def canonicalize_epub(source: Path, destination: Path) -> dict[str, int]:
    timestamp = tuple(int(part) for part in CONFIG["publication_date"].split("-")) + (0, 0, 0)
    with zipfile.ZipFile(source, "r") as incoming:
        names = incoming.namelist()
        if "mimetype" not in names:
            raise BuildError("Pandoc EPUB lacks the required mimetype entry")
        records = {name: incoming.read(name) for name in names if not name.endswith("/")}
    repaired_symbol_group_headers = 0
    symbol_group_cell = re.compile(
        r'<td(?P<attrs>(?=[^>]*\bclass="[^"]*\bsymbol-group-heading\b)[^>]*)>'
        r'(?P<body>.*?)</td>',
        flags=re.DOTALL,
    )
    for name, payload in list(records.items()):
        if not name.lower().endswith((".xhtml", ".html", ".htm")):
            continue
        text = payload.decode("utf-8")
        text, count = symbol_group_cell.subn(
            lambda match: f"<th{match.group('attrs')}>{match.group('body')}</th>",
            text,
        )
        repaired_symbol_group_headers += count
        records[name] = text.encode("utf-8")
    if repaired_symbol_group_headers != 5:
        raise BuildError(
            "Expected Pandoc to turn five later symbol-group headers into table cells; "
            f"found {repaired_symbol_group_headers}"
        )
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_name(destination.name + ".next")
    with zipfile.ZipFile(temporary, "w") as outgoing:
        mime_info = zipfile.ZipInfo("mimetype", date_time=timestamp)
        mime_info.compress_type = zipfile.ZIP_STORED
        mime_info.external_attr = 0o100644 << 16
        outgoing.writestr(mime_info, records.pop("mimetype"))
        for name in sorted(records):
            info = zipfile.ZipInfo(name, date_time=timestamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            info.flag_bits |= 0x800
            outgoing.writestr(info, records[name], compresslevel=9)
    temporary.replace(destination)
    return {"symbol_group_headers_restored": repaired_symbol_group_headers}


def build_epub(profile: str) -> dict[str, Any]:
    require_tool("pandoc")
    if not HTML_OUTPUT.is_file():
        build_html(profile)
    stage = TMP_ROOT / "epub"
    reset_dir(stage)
    runs = []
    canonical_paths = []
    for run_name in ("pass-a", "pass-b"):
        raw = stage / f"{run_name}.raw.epub"
        canonical = stage / f"{run_name}.epub"
        command = [
            require_tool("pandoc"),
            "index.html",
            "--from=html",
            "--to=epub3",
            "--mathml",
            "--toc",
            "--toc-depth=3",
            "--epub-chapter-level=2",
            "--css=accessibility.css",
            "--metadata=title:" + CONFIG["title"],
            "--metadata=lang:" + CONFIG["language"],
            "--metadata=identifier:" + CONFIG["identifier"],
            "--metadata=date:" + CONFIG["publication_date"],
            "--output=" + str(raw),
        ]
        result = run_command(
            command,
            cwd=HTML_OUTPUT.parent,
            timeout=int(CONFIG["timeouts_seconds"]["epub"]),
        )
        write_text(LOGS / f"epub-{run_name}.console.txt", result["output"])
        if result["timed_out"] or result["exit_code"] != 0 or not raw.is_file():
            raise BuildError(f"Pandoc failed to build EPUB during {run_name}")
        canonicalization = canonicalize_epub(raw, canonical)
        canonical_paths.append(canonical)
        runs.append(
            {
                "name": run_name,
                "command": {key: result[key] for key in ("command", "cwd", "exit_code", "timed_out")},
                "console_log": rel(LOGS / f"epub-{run_name}.console.txt"),
                "canonicalization": canonicalization,
                "canonical_output": file_record(canonical, base=stage),
            }
        )
    hashes = [sha256_path(path) for path in canonical_paths]
    if len(set(hashes)) != 1:
        raise BuildError(f"The two canonical EPUB builds differ: {hashes}")
    EPUB_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(canonical_paths[-1], EPUB_OUTPUT)
    validation = validate_epub(EPUB_OUTPUT)
    if validation["status"] != "pass":
        raise BuildError(f"EPUB validation failed: {validation['issues'][:10]}")
    epubcheck = epubcheck_command()
    epubcheck_result = None
    if epubcheck:
        probe = epubcheck_probe()
        if not probe["available"]:
            raise BuildError("The locked EPUBCheck runtime did not pass its version probe")
        check_result = run_command([*epubcheck, EPUB_OUTPUT.name], cwd=EPUB_OUTPUT.parent, timeout=300)
        write_text(LOGS / "epubcheck.console.txt", check_result["output"])
        epubcheck_result = {
            key: check_result[key] for key in ("command", "cwd", "exit_code", "timed_out")
        }
        epubcheck_result.update(
            {
                "available": True,
                "status": "pass" if check_result["exit_code"] == 0 and not check_result["timed_out"] else "fail",
                "version": probe["version"],
                "provenance": probe["provenance"],
            }
        )
        epubcheck_result["console_log"] = rel(LOGS / "epubcheck.console.txt")
        if check_result["timed_out"] or check_result["exit_code"] != 0:
            raise BuildError("EPUBCheck reported an error")
    elif profile == "final" and CONFIG["final_requirements"]["epubcheck_must_be_available"]:
        raise BuildError("The final profile requires EPUBCheck, but epubcheck is not installed")
    receipt = {
        "schema": "navier-stokes-everyday-epub-build/v1",
        "profile": profile,
        "status": "provisional_pass" if profile == "provisional" else "pass",
        "notice": CONFIG["provisional_notice"] if profile == "provisional" else None,
        "source_html": file_record(HTML_OUTPUT),
        "runs": runs,
        "deterministic_rebuilds": 2,
        "byte_identical_after_canonical_packaging": True,
        "validation": validation,
        "epubcheck": epubcheck_result or {"available": False, "status": "not_run"},
        "output": file_record(EPUB_OUTPUT),
        "limitations": (
            "EPUBCheck is unavailable. Internal EPUB 3 structure, XML, metadata, image-alternative, and link checks passed."
            if not epubcheck else None
        ),
    }
    write_json(RECEIPTS / "epub-build.json", receipt)
    return receipt


def strip_tex_comments(text: str) -> str:
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in text.splitlines())


def latex_cross_reference_check() -> dict[str, Any]:
    main_path = ROOT / CONFIG["entrypoint"]
    main_text = strip_tex_comments(main_path.read_text(encoding="utf-8-sig"))
    ranges = main_ranges(main_text)
    combined = [main_text]
    for range_name in ranges:
        combined.append(
            strip_tex_comments(
                (ROOT / "everyday" / "sections" / f"{range_name}.tex").read_text(encoding="utf-8-sig")
            )
        )
    text = "\n".join(combined)
    labels = re.findall(r"\\label\{([^{}]+)\}", text)
    label_counts = Counter(labels)
    references = []
    for match in re.finditer(r"\\(?:eqref|ref|pageref|autoref|cref|Cref)\{([^{}]+)\}", text):
        references.extend(part.strip() for part in match.group(1).split(",") if part.strip())
    bibitems = re.findall(r"\\bibitem(?:\[[^]]*\])?\{([^{}]+)\}", text)
    bib_counts = Counter(bibitems)
    citations = []
    for match in re.finditer(r"\\cite(?:\[[^]]*\])?\{([^{}]+)\}", text):
        citations.extend(part.strip() for part in match.group(1).split(",") if part.strip())
    declared_figures = re.findall(r"\\NSDeclareFigure\{([^{}]+)\}\{([^{}]+)\}", main_text)
    used_figures = re.findall(r"\\NSFigurePlaceholder\{([^{}]+)\}", text)
    page_markers = [int(value) for value in re.findall(r"\\NSPage\{(\d{3})\}", text)]
    formula_ids = re.findall(r"\\NS(?:i|Formula)\{(NS-F-P\d{3}-\d{3})\}", text)
    issues: list[dict[str, Any]] = []
    if ranges != CONFIG["expected_ranges"]:
        issues.append({"code": "range-order", "observed": ranges})
    duplicates = sorted(label for label, count in label_counts.items() if count > 1)
    if duplicates:
        issues.append({"code": "duplicate-label", "labels": duplicates})
    missing_references = sorted(set(references) - set(labels))
    if missing_references:
        issues.append({"code": "unresolved-reference", "labels": missing_references})
    duplicate_bibitems = sorted(item for item, count in bib_counts.items() if count > 1)
    if duplicate_bibitems:
        issues.append({"code": "duplicate-bibitem", "keys": duplicate_bibitems})
    missing_citations = sorted(set(citations) - set(bibitems))
    if missing_citations:
        issues.append({"code": "unresolved-citation", "keys": missing_citations})
    declaration_ids = [item[0] for item in declared_figures]
    missing_figures = sorted(set(used_figures) - set(declaration_ids))
    unused_figures = sorted(set(declaration_ids) - set(used_figures))
    if missing_figures:
        issues.append({"code": "undeclared-figure", "ids": missing_figures})
    if unused_figures:
        issues.append({"code": "unused-figure", "ids": unused_figures})
    if page_markers != list(range(1, 167)):
        issues.append({"code": "source-page-order", "count": len(page_markers)})
    duplicate_formulas = sorted(identifier for identifier, count in Counter(formula_ids).items() if count > 1)
    if duplicate_formulas:
        issues.append({"code": "duplicate-formula-id", "ids": duplicate_formulas[:50], "count": len(duplicate_formulas)})
    return {
        "status": "pass" if not issues else "fail",
        "counts": {
            "ranges": len(ranges),
            "labels": len(labels),
            "references": len(references),
            "bibitems": len(bibitems),
            "citations": len(citations),
            "figures_declared": len(declared_figures),
            "figures_used": len(used_figures),
            "source_page_markers": len(page_markers),
            "formula_markers": len(formula_ids),
        },
        "external_links_checked_online": False,
        "issues": issues,
    }


def url_target(href: str, current: Path, root: Path) -> tuple[Path, str] | None:
    parsed = urllib.parse.urlsplit(href)
    if parsed.scheme or parsed.netloc:
        return None
    path_text = urllib.parse.unquote(parsed.path)
    target = current if not path_text else (current.parent / path_text)
    return target.resolve(), urllib.parse.unquote(parsed.fragment)


def validate_html(path: Path, expected: dict[str, Any] | None = None) -> dict[str, Any]:
    from lxml import html as lxml_html

    issues: list[dict[str, Any]] = []
    parser = lxml_html.HTMLParser(encoding="utf-8")
    document = lxml_html.parse(str(path), parser).getroot()
    ids = [value for value in document.xpath("//*[@id]/@id") if value]
    id_set = set(ids)
    duplicate_ids = sorted(value for value, count in Counter(ids).items() if count > 1)
    if duplicate_ids:
        issues.append({"code": "duplicate-html-id", "ids": duplicate_ids[:100]})
    if document.get("lang") != CONFIG["language"]:
        issues.append({"code": "html-language"})
    titles = document.xpath("/html/head/title/text()")
    if titles != [CONFIG["title"]]:
        issues.append({"code": "html-title", "observed": titles})
    if len(document.xpath("//main[@id='main-content']")) != 1:
        issues.append({"code": "html-main"})
    if len(document.xpath("//h1")) != 1:
        issues.append({"code": "html-h1", "count": len(document.xpath('//h1'))})
    source_pages = sorted(
        int(value.rsplit("-", 1)[-1])
        for value in ids
        if re.fullmatch(r"source-page-\d{3}", value)
    )
    if source_pages != list(range(1, 167)):
        issues.append({"code": "html-source-pages", "observed": len(source_pages)})
    if expected is not None:
        expected_ids = set(expected["labels"])
        expected_ids.update("formula-" + value for value in expected["formulas"])
        expected_ids.update("source-page-" + value for value in expected["pages"])
        expected_ids.update(expected["segments"])
        expected_ids.update("bib-" + value for value in expected["bibitems"])
        missing_ids = sorted(expected_ids - id_set)
        if missing_ids:
            issues.append(
                {"code": "html-source-anchor", "count": len(missing_ids), "ids": missing_ids[:100]}
            )
    math_count = len(document.xpath("//*[local-name()='math']"))
    if math_count == 0:
        issues.append({"code": "html-mathml-missing"})
    images = document.xpath("//img")
    for image in images:
        alt = image.get("alt")
        if alt is None or not alt.strip():
            issues.append({"code": "image-alt", "src": image.get("src")})
        source = image.get("src")
        if source:
            target = url_target(source, path, path.parent)
            if target is not None and not target[0].is_file():
                issues.append({"code": "image-file", "src": source})
    for table in document.xpath("//table"):
        if table.get("role") != "presentation" and not table.xpath(".//th"):
            issues.append({"code": "table-header"})
    link_count = 0
    external_count = 0
    id_cache: dict[Path, set[str]] = {path.resolve(): set(ids)}
    for element in document.xpath("//*[@href]"):
        href = element.get("href") or ""
        if not href or href.startswith(("mailto:", "tel:", "data:")):
            continue
        parsed = urllib.parse.urlsplit(href)
        if parsed.scheme in {"http", "https"} or parsed.netloc:
            external_count += 1
            continue
        link_count += 1
        target_data = url_target(href, path, path.parent)
        if target_data is None:
            continue
        target, fragment = target_data
        if not target.is_file():
            issues.append({"code": "local-link-file", "href": href})
            continue
        if fragment:
            if target not in id_cache:
                target_doc = lxml_html.parse(str(target), parser).getroot()
                id_cache[target] = set(target_doc.xpath("//*[@id]/@id"))
            if fragment not in id_cache[target]:
                issues.append({"code": "local-link-fragment", "href": href})
    raw = path.read_text(encoding="utf-8")
    if re.search(r"file:/{2,3}|(?<![A-Za-z0-9_])[A-Za-z]:[\\/]", raw):
        issues.append({"code": "machine-path-leak"})
    leaked_commands = sorted(
        set(re.findall(r"\\(?:NSi|NSFormula|NSPage|NSFigurePlaceholder|EESegment|EEAddition)\b", raw))
    )
    if leaked_commands:
        issues.append({"code": "unconverted-source-command", "commands": leaked_commands})
    return {
        "status": "pass" if not issues else "fail",
        "counts": {
            "ids": len(ids),
            "links_local": link_count,
            "links_external_not_fetched": external_count,
            "images": len(images),
            "mathml_elements": math_count,
            "tables": len(document.xpath("//table")),
            "source_pages": len(source_pages),
            "formula_anchors": sum(value.startswith("formula-") for value in ids),
            "segment_anchors": sum(value.startswith("EE-TGT-") for value in ids),
        },
        "issues": issues,
    }


def validate_epub(path: Path) -> dict[str, Any]:
    from lxml import etree

    issues: list[dict[str, Any]] = []
    with zipfile.ZipFile(path, "r") as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if not infos or infos[0].filename != "mimetype" or infos[0].compress_type != zipfile.ZIP_STORED:
            issues.append({"code": "epub-mimetype-order"})
        if "mimetype" not in names or archive.read("mimetype") != b"application/epub+zip":
            issues.append({"code": "epub-mimetype-value"})
        if "META-INF/container.xml" not in names:
            issues.append({"code": "epub-container-missing"})
            return {"status": "fail", "counts": {"entries": len(names)}, "issues": issues}
        try:
            container = etree.fromstring(archive.read("META-INF/container.xml"))
        except etree.XMLSyntaxError as exc:
            issues.append({"code": "epub-container-xml", "message": str(exc)})
            return {"status": "fail", "counts": {"entries": len(names)}, "issues": issues}
        rootfiles = container.xpath("//*[local-name()='rootfile']/@full-path")
        if len(rootfiles) != 1 or rootfiles[0] not in names:
            issues.append({"code": "epub-rootfile", "observed": rootfiles})
            return {"status": "fail", "counts": {"entries": len(names)}, "issues": issues}
        opf_name = rootfiles[0]
        opf = etree.fromstring(archive.read(opf_name))
        title = opf.xpath("string(//*[local-name()='metadata']/*[local-name()='title'][1])")
        language = opf.xpath("string(//*[local-name()='metadata']/*[local-name()='language'][1])")
        identifier = opf.xpath("string(//*[local-name()='metadata']/*[local-name()='identifier'][1])")
        if title != CONFIG["title"]:
            issues.append({"code": "epub-title", "observed": title})
        if language != CONFIG["language"]:
            issues.append({"code": "epub-language", "observed": language})
        if identifier != CONFIG["identifier"]:
            issues.append({"code": "epub-identifier", "observed": identifier})
        opf_dir = PurePosixPath(opf_name).parent
        manifest_items = opf.xpath("//*[local-name()='manifest']/*[local-name()='item']")
        manifest_by_id = {item.get("id"): item for item in manifest_items}
        for item in manifest_items:
            resolved = (opf_dir / PurePosixPath(urllib.parse.unquote(item.get("href", "")))).as_posix()
            if resolved not in names:
                issues.append({"code": "epub-manifest-file", "href": item.get("href")})
        for itemref in opf.xpath("//*[local-name()='spine']/*[local-name()='itemref']"):
            if itemref.get("idref") not in manifest_by_id:
                issues.append({"code": "epub-spine-idref", "idref": itemref.get("idref")})
        nav_items = [item for item in manifest_items if "nav" in (item.get("properties") or "").split()]
        if len(nav_items) != 1:
            issues.append({"code": "epub-navigation", "count": len(nav_items)})
        xhtml_names = [name for name in names if name.lower().endswith((".xhtml", ".html", ".htm"))]
        ids_by_file: dict[str, set[str]] = {}
        documents: dict[str, Any] = {}
        for name in xhtml_names:
            try:
                document = etree.fromstring(archive.read(name))
                documents[name] = document
                ids_by_file[name] = set(document.xpath("//*[@id]/@id"))
            except etree.XMLSyntaxError as exc:
                issues.append({"code": "epub-xhtml-xml", "file": name, "message": str(exc)})
        image_count = 0
        math_count = 0
        link_count = 0
        for name, document in documents.items():
            for image in document.xpath("//*[local-name()='img']"):
                image_count += 1
                if not (image.get("alt") or "").strip():
                    issues.append({"code": "epub-image-alt", "file": name, "src": image.get("src")})
            math_count += len(document.xpath("//*[local-name()='math']"))
            for element in document.xpath("//*[@href]"):
                href = element.get("href") or ""
                parsed = urllib.parse.urlsplit(href)
                if parsed.scheme or parsed.netloc or href.startswith(("mailto:", "tel:")):
                    continue
                link_count += 1
                target_path = PurePosixPath(name) if not parsed.path else PurePosixPath(name).parent / urllib.parse.unquote(parsed.path)
                normalized = posixpath.normpath(target_path.as_posix())
                if normalized not in names:
                    issues.append({"code": "epub-link-file", "file": name, "href": href})
                elif parsed.fragment and parsed.fragment not in ids_by_file.get(normalized, set()):
                    issues.append({"code": "epub-link-fragment", "file": name, "href": href})
        if math_count == 0:
            issues.append({"code": "epub-mathml-missing"})
    return {
        "status": "pass" if not issues else "fail",
        "counts": {
            "entries": len(names),
            "manifest_items": len(manifest_items),
            "xhtml_documents": len(xhtml_names),
            "images": image_count,
            "mathml_elements": math_count,
            "links_local": link_count,
        },
        "issues": issues,
    }


def content_audit(profile: str) -> dict[str, Any]:
    if profile == "final":
        report_path = ROOT / "evidence" / "translation" / "FINAL_AGGREGATE_AUDIT.json"
        first_use_path = ROOT / "evidence" / "translation" / "FIRST_USE_FINALIZATION.json"
        if not report_path.is_file() or not first_use_path.is_file():
            raise BuildError("The final profile requires the frozen whole-book audit and first-use receipt")
        try:
            report = json.loads(report_path.read_text(encoding="utf-8-sig"))
            first_use = json.loads(first_use_path.read_text(encoding="utf-8-sig"))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            raise BuildError(f"The frozen content-audit evidence is unreadable: {error}") from error
        if (
            report.get("schema") != "navier-stokes-everyday-all-audit/v1"
            or report.get("status") != "pass"
            or report.get("expected_ranges") != 29
            or report.get("global_issues")
            or report.get("global_pending")
            or report.get("range_status_counts") != {"fail": 0, "pass": 29, "pending": 0}
        ):
            raise BuildError("The frozen whole-book audit is not a complete pass")
        ranges = first_use.get("ranges")
        if not isinstance(ranges, dict) or len(ranges) != 29:
            raise BuildError("The first-use receipt does not cover all 29 ranges")
        verified_files = 0
        for range_name, receipt in sorted(ranges.items()):
            source = ROOT / "reconstruction" / "sections" / f"{range_name}.tex"
            target = ROOT / "everyday" / "sections" / f"{range_name}.tex"
            if sha256_path(source) != receipt.get("source_sha256"):
                raise BuildError(f"Source bytes changed after the whole-book audit: {range_name}")
            if sha256_path(target) != receipt.get("target_sha256"):
                raise BuildError(f"Target bytes changed after the whole-book audit: {range_name}")
            verified_files += 2
            ledger_hashes = receipt.get("ledger_sha256")
            if not isinstance(ledger_hashes, dict):
                raise BuildError(f"Missing ledger hashes in the first-use receipt: {range_name}")
            ledger_root = ROOT / "evidence" / "translation" / range_name
            for name, expected_hash in sorted(ledger_hashes.items()):
                if sha256_path(ledger_root / name) != expected_hash:
                    raise BuildError(f"Evidence bytes changed after the whole-book audit: {range_name}/{name}")
                verified_files += 1
            if sha256_path(ledger_root / "REPORT.md") != receipt.get("report_sha256"):
                raise BuildError(f"Range report changed after the whole-book audit: {range_name}")
            verified_files += 1
        write_text(LOGS / "content-audit.json", report_path.read_text(encoding="utf-8-sig"))
        return {
            "mode": "verified_frozen_final_audit",
            "reported_status": "pass",
            "report": file_record(report_path),
            "first_use_receipt": file_record(first_use_path),
            "verified_files": verified_files,
            "command": None,
        }

    script = ROOT / "scripts" / "audit_everyday_all.py"
    result = run_command(
        [sys.executable, script.name],
        cwd=script.parent,
        timeout=int(CONFIG["timeouts_seconds"]["audit"]),
    )
    write_text(LOGS / "content-audit.json", result["output"])
    status = "unreadable"
    with contextlib.suppress(json.JSONDecodeError):
        status = json.loads(result["output"])["status"]
    record = {
        "command": {key: result[key] for key in ("command", "cwd", "exit_code", "timed_out")},
        "reported_status": status,
        "report": rel(LOGS / "content-audit.json"),
    }
    if profile == "final" and CONFIG["final_requirements"]["content_audit_must_pass"] and status != "pass":
        raise BuildError(f"The final profile requires a passing content audit; observed {status}")
    return record


def run_checks(profile: str) -> dict[str, Any]:
    latex = latex_cross_reference_check()
    html_check = (
        validate_html(HTML_OUTPUT, expected=source_anchor_inventory(ROOT))
        if HTML_OUTPUT.is_file()
        else {"status": "not_built", "issues": []}
    )
    epub_check = validate_epub(EPUB_OUTPUT) if EPUB_OUTPUT.is_file() else {"status": "not_built", "issues": []}
    pdf_check: dict[str, Any]
    if PDF_OUTPUT.is_file():
        pages, info = pdf_page_count(PDF_OUTPUT)
        pdf_check = {"status": "pass" if pages >= 166 else "fail", "page_count": pages}
        write_text(LOGS / "pdfinfo-check.txt", info)
    else:
        pdf_check = {"status": "not_built"}
    audit = content_audit(profile)
    structural_statuses = [latex["status"], html_check["status"], epub_check["status"], pdf_check["status"]]
    blocking = [status for status in structural_statuses if status not in {"pass", "not_built"}]
    status = "fail" if blocking else ("provisional_pass" if profile == "provisional" else "pass")
    report = {
        "schema": "navier-stokes-everyday-build-checks/v1",
        "profile": profile,
        "status": status,
        "latex_cross_references": latex,
        "pdf": pdf_check,
        "html": html_check,
        "epub": epub_check,
        "content_audit": audit,
        "external_network_links": "Recorded but not fetched. The reproducible build is offline and closes every local link.",
        "limitations": (
            "This is a provisional pipeline check. It is not the single full-book QA pass."
            if profile == "provisional" else None
        ),
    }
    write_json(RECEIPTS / "checks.json", report)
    if status == "fail":
        raise BuildError("One or more structural build checks failed")
    return report


def aggregate_receipt(profile: str) -> dict[str, Any]:
    names = ["dependencies.json", "pdf-build.json", "html-build.json", "epub-build.json", "checks.json"]
    records = {}
    for name in names:
        path = RECEIPTS / name
        if path.is_file():
            records[name] = file_record(path)
    outputs = [path for path in (PDF_OUTPUT, HTML_OUTPUT, EPUB_OUTPUT) if path.is_file()]
    receipt = {
        "schema": "navier-stokes-everyday-build-receipt/v1",
        "profile": profile,
        "status": "provisional_pass" if profile == "provisional" else "pass",
        "notice": CONFIG["provisional_notice"] if profile == "provisional" else None,
        "outputs": [file_record(path) for path in outputs],
        "component_receipts": records,
        "publication_performed": False,
        "translation_evidence_modified": False,
        "final_qa_claimed": False if profile == "provisional" else True,
    }
    write_json(RECEIPTS / "build-receipt.json", receipt)
    return receipt


def write_manifest() -> dict[str, Any]:
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    json_manifest = RECEIPTS / "MANIFEST.json"
    text_manifest = RECEIPTS / "MANIFEST.sha256"
    external_qa_logs = {
        RECEIPTS / "qa-http.stderr.txt",
        RECEIPTS / "qa-http.stdout.txt",
    }
    included = sorted(
        path for path in OUTPUT_ROOT.rglob("*")
        if path.is_file() and path not in {json_manifest, text_manifest, *external_qa_logs}
    )
    entries = [file_record(path, base=OUTPUT_ROOT) for path in included]
    machine = {
        "schema": "navier-stokes-everyday-exact-byte-manifest/v1",
        "root": CONFIG["outputs"]["root"],
        "self_exclusions": [
            "receipts/MANIFEST.json",
            "receipts/MANIFEST.sha256"
        ],
        "entries": entries,
    }
    write_json(json_manifest, machine)
    manifest_inputs = included + [json_manifest]
    manifest_inputs.sort(key=lambda path: path.relative_to(OUTPUT_ROOT).as_posix())
    lines = ["# SHA-256, byte length, and output-root-relative path. This manifest excludes itself."]
    for path in manifest_inputs:
        record = file_record(path, base=OUTPUT_ROOT)
        lines.append(f"{record['sha256']}\t{record['bytes']}\t{record['path']}")
    write_text(text_manifest, "\n".join(lines) + "\n")
    verification = verify_manifest(text_manifest)
    if verification["status"] != "pass":
        raise BuildError(f"Manifest verification failed: {verification['issues']}")
    return {
        "manifest": file_record(text_manifest),
        "machine_manifest": file_record(json_manifest),
        "entries": len(manifest_inputs),
        "verification": verification,
    }


def verify_manifest(path: Path) -> dict[str, Any]:
    issues = []
    rows = [line for line in path.read_text(encoding="utf-8").splitlines() if line and not line.startswith("#")]
    for number, line in enumerate(rows, start=2):
        parts = line.split("\t")
        if len(parts) != 3:
            issues.append({"line": number, "code": "manifest-row"})
            continue
        expected_hash, expected_bytes, relative = parts
        target = OUTPUT_ROOT / PurePosixPath(relative)
        ensure_child(OUTPUT_ROOT, target)
        if not target.is_file():
            issues.append({"line": number, "code": "manifest-file", "path": relative})
            continue
        if target.stat().st_size != int(expected_bytes) or sha256_path(target) != expected_hash:
            issues.append({"line": number, "code": "manifest-bytes", "path": relative})
    return {"status": "pass" if not issues else "fail", "checked": len(rows), "issues": issues}


def all_build(profile: str) -> dict[str, Any]:
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    dependencies = dependency_report()
    if dependencies["status"] != "pass":
        raise BuildError(f"Required dependencies are missing: {dependencies['missing_required']}")
    pdf = build_pdf(profile)
    html = build_html(profile)
    epub = build_epub(profile)
    checks = run_checks(profile)
    aggregate = aggregate_receipt(profile)
    manifest = write_manifest()
    return {
        "profile": profile,
        "pdf": pdf["output"],
        "html": next(item for item in html["outputs"] if item["path"].endswith("index.html")),
        "epub": epub["output"],
        "checks": checks["status"],
        "receipt": file_record(RECEIPTS / "build-receipt.json"),
        "manifest": manifest,
        "aggregate": aggregate["status"],
    }


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "command",
        choices=("doctor", "pdf", "html", "epub", "check", "manifest", "all"),
        help="Pipeline stage to run.",
    )
    parser.add_argument(
        "--profile",
        choices=("provisional", "final"),
        default="provisional",
        help="Provisional is the safe default while the edition is unfinished.",
    )
    args = parser.parse_args(argv)
    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    RECEIPTS.mkdir(parents=True, exist_ok=True)
    LOGS.mkdir(parents=True, exist_ok=True)
    try:
        if args.command == "doctor":
            result = dependency_report()
            exit_code = 0 if result["status"] == "pass" else 1
        elif args.command == "pdf":
            result = build_pdf(args.profile)
            exit_code = 0
        elif args.command == "html":
            result = build_html(args.profile)
            exit_code = 0
        elif args.command == "epub":
            result = build_epub(args.profile)
            exit_code = 0
        elif args.command == "check":
            result = run_checks(args.profile)
            exit_code = 0
        elif args.command == "manifest":
            result = write_manifest()
            exit_code = 0
        else:
            result = all_build(args.profile)
            exit_code = 0
    except BuildError as exc:
        failure = {
            "schema": "navier-stokes-everyday-build-failure/v1",
            "command": args.command,
            "profile": args.profile,
            "status": "fail",
            "message": sanitize(str(exc)),
            "publication_performed": False,
            "translation_evidence_modified": False,
        }
        write_json(RECEIPTS / "last-failure.json", failure)
        print(json.dumps(failure, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    failure_path = RECEIPTS / "last-failure.json"
    if failure_path.exists():
        failure_path.unlink()
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
