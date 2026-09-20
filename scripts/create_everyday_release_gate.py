#!/usr/bin/env python3
"""Create the final release receipts after the root every-page review is recorded."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Iterable, Sequence

from jsonschema import Draft202012Validator, FormatChecker

import stage_everyday_english_repository as stage


ROOT = stage.ROOT
SCAN_PATH = ROOT / "evidence" / "build" / "EVERYDAY_ENGLISH_RELEASE_SCANS.json"
QA_PATH = ROOT / "evidence" / "build" / "EVERYDAY_ENGLISH_FINAL_QA.json"
SCAN_SCHEMA_PATH = ROOT / "evidence" / "schemas" / "EVERYDAY_RELEASE_SCANS.schema.json"
QA_SCHEMA_PATH = ROOT / "evidence" / "schemas" / "EVERYDAY_FINAL_QA.schema.json"
VISUAL_PACKAGE_ROOT = ROOT / "evidence" / "build" / stage.EXPECTED_QA_ID
VISUAL_SUMMARY_PATH = VISUAL_PACKAGE_ROOT / "QA_SUMMARY.json"
VISUAL_PROPOSAL_PATH = VISUAL_PACKAGE_ROOT / "ledger" / "visual_qa.proposed.json"
VISUAL_MANIFEST_PATH = VISUAL_PACKAGE_ROOT / "FILES.sha256"
VISUAL_LEDGER_PATH = ROOT / "evidence" / "ledgers" / "visual_qa.jsonl"

BUILD_RECEIPT_PATH = stage.OUTPUT_ROOT / "receipts" / "build-receipt.json"
CHECKS_PATH = stage.OUTPUT_ROOT / "receipts" / "checks.json"
PDF_RECEIPT_PATH = stage.OUTPUT_ROOT / "receipts" / "pdf-build.json"
HTML_RECEIPT_PATH = stage.OUTPUT_ROOT / "receipts" / "html-build.json"
EPUB_RECEIPT_PATH = stage.OUTPUT_ROOT / "receipts" / "epub-build.json"
DEPENDENCIES_PATH = stage.OUTPUT_ROOT / "receipts" / "dependencies.json"
AUDIT_PATH = stage.OUTPUT_ROOT / "receipts" / "logs" / "content-audit.json"
EPUBCHECK_LOCK_PATH = ROOT / "everyday" / "epubcheck-lock.json"

PDF_PATH = stage.OUTPUT_ROOT / "pdf" / "everyday-english-edition.pdf"
HTML_PATH = stage.OUTPUT_ROOT / "html" / "index.html"
EPUB_PATH = stage.OUTPUT_ROOT / "epub" / "everyday-english-edition.epub"

CHECK_KEYS = (
    "blank_pages",
    "clipped_pages",
    "broken_layout_pages",
    "bad_glyph_pages",
    "missing_figure_pages",
    "unreadable_figure_labels",
)
SCAN_ORDER = ("disallowed_token", "authorial_we", "local_path_leaks")


class GateError(RuntimeError):
    """A required release fact is absent or does not match its recorded bytes."""


def require_equal(observed: Any, expected: Any, label: str) -> None:
    if observed != expected:
        raise GateError(f"{label} differs: expected {expected!r}, observed {observed!r}")


def require_zero(observed: Any, label: str) -> None:
    if observed != 0:
        raise GateError(f"{label} must be zero; observed {observed!r}")


def parse_timestamp(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise GateError(f"{label} is missing")
    normalized = value[:-1] + "+00:00" if value.endswith("Z") else value
    try:
        parsed = dt.datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise GateError(f"{label} is not an ISO 8601 date-time: {value!r}") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise GateError(f"{label} must include a time-zone offset")
    return value


def load_schema(path: Path) -> dict[str, Any]:
    schema = stage.read_json(path)
    Draft202012Validator.check_schema(schema)
    return schema


def validate_against_schema(value: dict[str, Any], schema_path: Path, label: str) -> None:
    schema = load_schema(schema_path)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(value), key=lambda item: list(item.absolute_path))
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.absolute_path) or "<root>"
        raise GateError(f"{label} fails its schema at {location}: {first.message}")


def reduced_file_record(record: dict[str, Any]) -> dict[str, Any]:
    return {key: record[key] for key in ("path", "bytes", "sha256")}


def verify_file_record(path: Path, record: dict[str, Any], label: str) -> None:
    observed = stage.file_record(stage.require_file(path))
    require_equal(reduced_file_record(record), observed, label)


def output_record(build: dict[str, Any], path: Path) -> dict[str, Any]:
    relative = path.relative_to(ROOT).as_posix()
    records = build.get("outputs")
    if not isinstance(records, list):
        raise GateError("The final build receipt has no outputs array")
    matches = [item for item in records if isinstance(item, dict) and item.get("path") == relative]
    if len(matches) != 1:
        raise GateError(f"The final build receipt must name {relative} exactly once")
    verify_file_record(path, matches[0], f"final build output {relative}")
    return reduced_file_record(matches[0])


def verify_visual_manifest() -> None:
    path = stage.require_file(VISUAL_MANIFEST_PATH)
    seen: set[str] = set()
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        parts = line.split("  ", 1)
        if len(parts) != 2 or not stage.SHA256_RE.fullmatch(parts[0]):
            raise GateError(f"Invalid visual package manifest row {number}")
        digest, relative = parts
        if relative in seen:
            raise GateError(f"Duplicate visual package manifest path: {relative}")
        seen.add(relative)
        target = VISUAL_PACKAGE_ROOT / Path(relative)
        stage.require_file(target)
        require_equal(stage.sha256_path(target), digest, f"visual package manifest SHA-256 for {relative}")
    if not seen:
        raise GateError("The visual package manifest has no entries")


def verify_visual_package(pdf_record: dict[str, Any], page_count: int) -> None:
    summary = stage.read_json(VISUAL_SUMMARY_PATH)
    require_equal(summary.get("schema"), "navier-stokes-everyday-visual-qa-package/v1", "visual package schema")
    require_equal(summary.get("qa_id"), stage.EXPECTED_QA_ID, "visual package ID")
    require_equal(summary.get("status"), "pending_root_inspection", "visual package machine status")
    require_equal(summary.get("human_visual_inspection"), None, "visual package human review marker")
    require_equal(summary.get("inspection_completed_at"), None, "visual package review time marker")
    require_equal(summary.get("pdf"), pdf_record, "visual package PDF")

    automated = summary.get("automated_summary")
    if not isinstance(automated, dict):
        raise GateError("The visual package has no automated summary")
    require_equal(automated.get("pages"), page_count, "visual package page count")
    require_equal(automated.get("renders"), page_count, "visual package render count")
    require_equal(automated.get("contact_sheets"), 21, "visual package contact-sheet count")
    require_equal(automated.get("automated_blank_pages"), [], "automated blank-page findings")
    require_equal(automated.get("edge_guard_pages"), [], "automated edge findings")

    sheets = summary.get("contact_sheets")
    if not isinstance(sheets, list) or len(sheets) != 21:
        raise GateError("The visual package must contain exactly 21 contact-sheet records")
    covered: list[int] = []
    for index, sheet in enumerate(sheets, start=1):
        if not isinstance(sheet, dict):
            raise GateError(f"Contact-sheet record {index} is not an object")
        require_equal(sheet.get("sheet"), index, f"contact-sheet number {index}")
        pages = sheet.get("pages")
        if not isinstance(pages, list):
            raise GateError(f"Contact-sheet record {index} has no page list")
        covered.extend(pages)
        file_value = sheet.get("file")
        if not isinstance(file_value, dict):
            raise GateError(f"Contact-sheet record {index} has no file record")
        relative = file_value.get("path")
        if not isinstance(relative, str):
            raise GateError(f"Contact-sheet record {index} has no file path")
        verify_file_record(ROOT / Path(relative), file_value, f"contact-sheet file {index}")
    require_equal(covered, list(range(1, page_count + 1)), "visual package page coverage")

    proposal = stage.read_json(VISUAL_PROPOSAL_PATH)
    require_equal(proposal.get("id"), stage.EXPECTED_QA_ID, "proposed visual record ID")
    require_equal(proposal.get("record_type"), "everyday_english_final_visual_qa", "proposed visual record type")
    require_equal(proposal.get("status"), "pending_root_inspection", "proposed visual record status")
    require_equal(proposal.get("pdf_path"), pdf_record["path"], "proposed visual PDF path")
    require_equal(proposal.get("pdf_sha256"), pdf_record["sha256"], "proposed visual PDF SHA-256")
    require_equal(proposal.get("covered_pages"), [1, page_count], "proposed visual page coverage")
    require_equal(proposal.get("inspected_pages"), 0, "proposed visual inspected-page count")
    require_equal(proposal.get("inspection"), None, "proposed visual review marker")
    require_equal(proposal.get("inspection_completed_at"), None, "proposed visual review time marker")
    require_equal(proposal.get("checks"), None, "proposed visual findings marker")
    require_equal(proposal.get("contact_sheets"), sheets, "proposed visual contact sheets")
    verify_visual_manifest()


def load_root_visual_record(pdf_record: dict[str, Any], page_count: int) -> tuple[dict[str, Any], str]:
    verify_visual_package(pdf_record, page_count)
    rows = stage.read_jsonl(VISUAL_LEDGER_PATH)
    matches = [row for row in rows if row.get("id") == stage.EXPECTED_QA_ID]
    if not matches:
        raise GateError(
            f"The root every-page record {stage.EXPECTED_QA_ID} is not in "
            "evidence/ledgers/visual_qa.jsonl"
        )
    if len(matches) != 1:
        raise GateError(f"The visual ledger contains {len(matches)} records named {stage.EXPECTED_QA_ID}")
    record = matches[0]
    require_equal(record.get("record_type"), "everyday_english_final_visual_qa", "root visual record type")
    require_equal(record.get("status"), "pass", "root visual record status")
    require_equal(record.get("pdf_path"), pdf_record["path"], "root visual PDF path")
    require_equal(record.get("pdf_sha256"), pdf_record["sha256"], "root visual PDF SHA-256")
    require_equal(record.get("inspected_pages"), page_count, "root visual inspected-page count")
    require_equal(record.get("covered_pages"), [1, page_count], "root visual page coverage")
    inspection = record.get("inspection")
    if not isinstance(inspection, str) or "root" not in inspection or "every_page" not in inspection:
        raise GateError("The visual record must identify root every-page review")
    checks = record.get("checks")
    if not isinstance(checks, dict):
        raise GateError("The root visual record has no findings object")
    if set(checks) != set(CHECK_KEYS):
        raise GateError(f"The root visual findings must contain exactly: {', '.join(CHECK_KEYS)}")
    for key in CHECK_KEYS:
        require_zero(checks.get(key), f"root visual finding {key}")
    if "contact_sheets" in record:
        proposal = stage.read_json(VISUAL_PROPOSAL_PATH)
        require_equal(record["contact_sheets"], proposal["contact_sheets"], "root visual contact sheets")
    timestamp = parse_timestamp(record.get("inspection_completed_at"), "root visual review time")
    return record, timestamp


def target_manuscript_paths() -> list[Path]:
    return [ROOT / "everyday" / "main.tex"] + [
        ROOT / "everyday" / "sections" / f"{name}.tex" for name in stage.EXPECTED_RANGES
    ]


def public_release_text_paths() -> list[Path]:
    return [
        stage.TEMPLATE_ROOT / "README.md",
        stage.TEMPLATE_ROOT / "LICENSE-NOTICE.md",
        stage.TEMPLATE_ROOT / "PAGES.json",
        HTML_PATH,
    ]


def path_leak_text_paths() -> list[Path]:
    excluded = {SCAN_PATH.resolve(), QA_PATH.resolve()}
    candidates: set[Path] = set()
    for path, _ in stage.active_release_files():
        if path.resolve() in excluded:
            continue
        stage.require_file(path)
        candidates.add(path.resolve())
    for base in (stage.TEMPLATE_ROOT, stage.OUTPUT_ROOT):
        for path in base.rglob("*"):
            if path.is_file() and path.resolve() not in excluded:
                candidates.add(path.resolve())
    return [path for path in sorted(candidates, key=lambda item: item.as_posix()) if stage.read_text_if_supported(path) is not None]


def find_matches(text: str, scan_name: str) -> int:
    if scan_name == "disallowed_token":
        pattern = re.compile(rf"\b{re.escape(stage.DISALLOWED_TOKEN)}\b", re.IGNORECASE)
        return len(pattern.findall(text))
    if scan_name == "authorial_we":
        return len(stage.AUTHORIAL_PRONOUN.findall(text))
    if scan_name == "local_path_leaks":
        return sum(len(pattern.findall(text)) for pattern in stage.ABSOLUTE_PATH_PATTERNS)
    raise GateError(f"Unknown scan: {scan_name}")


def build_scan_receipt(generated_at: str) -> dict[str, Any]:
    target = [stage.require_file(path).resolve() for path in target_manuscript_paths()]
    public = [stage.require_file(path).resolve() for path in public_release_text_paths()]
    path_scope = path_leak_text_paths()
    assignments: dict[Path, set[str]] = {}
    for path in target + public:
        assignments.setdefault(path, set()).update(("disallowed_token", "authorial_we"))
    for path in path_scope:
        assignments.setdefault(path, set()).add("local_path_leaks")

    findings: list[dict[str, Any]] = []
    records: list[dict[str, Any]] = []
    counts = {name: 0 for name in SCAN_ORDER}
    for path in sorted(assignments, key=lambda item: item.as_posix()):
        text = stage.read_text_if_supported(path)
        if text is None:
            raise GateError(f"A release scan path is not readable text: {path}")
        names = [name for name in SCAN_ORDER if name in assignments[path]]
        for name in names:
            matches = find_matches(text, name)
            counts[name] += matches
            if matches:
                findings.append({
                    "path": path.relative_to(ROOT).as_posix(),
                    "scan": name,
                    "matches": matches,
                })
        record = stage.file_record(path)
        record["scans"] = names
        records.append(record)
    if findings:
        preview = json.dumps(findings[:20], ensure_ascii=False, sort_keys=True)
        raise GateError(f"Release scans found blocked text: {preview}")

    receipt = {
        "schema": "navier-stokes-everyday-release-scans/v1",
        "status": "pass",
        "generated_at": generated_at,
        "scopes": {
            "target_manuscript": [path.relative_to(ROOT).as_posix() for path in target],
            "public_release_text": [path.relative_to(ROOT).as_posix() for path in public],
            "path_leak_text": [path.relative_to(ROOT).as_posix() for path in path_scope],
        },
        "disallowed_token": {"status": "pass", "matches": counts["disallowed_token"]},
        "authorial_we": {"status": "pass", "matches": counts["authorial_we"]},
        "local_path_leaks": {"status": "pass", "matches": counts["local_path_leaks"]},
        "files": records,
    }
    validate_against_schema(receipt, SCAN_SCHEMA_PATH, "release scan receipt")
    return receipt


def json_bytes(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode("utf-8")


def record_for_bytes(path: Path, payload: bytes) -> dict[str, Any]:
    return {
        "path": path.relative_to(ROOT).as_posix(),
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
    }


def verified_component(path: Path, build: dict[str, Any], name: str) -> dict[str, Any]:
    record = stage.file_record(stage.require_file(path))
    components = build.get("component_receipts")
    if not isinstance(components, dict) or name not in components:
        raise GateError(f"The final build receipt does not bind {name}")
    require_equal(components[name], record, f"final build component {name}")
    return record


def build_final_qa(scan_payload: bytes) -> dict[str, Any]:
    build = stage.read_json(BUILD_RECEIPT_PATH)
    require_equal(build.get("schema"), "navier-stokes-everyday-build-receipt/v1", "final build schema")
    require_equal(build.get("profile"), "final", "final build profile")
    require_equal(build.get("status"), "pass", "final build status")
    require_equal(build.get("notice"), None, "final build notice")
    require_equal(build.get("final_qa_claimed"), True, "final build QA marker")
    require_equal(build.get("publication_performed"), False, "final build publication marker")

    pdf = output_record(build, PDF_PATH)
    html = output_record(build, HTML_PATH)
    epub = output_record(build, EPUB_PATH)
    checks_record = verified_component(CHECKS_PATH, build, "checks.json")
    pdf_receipt_record = verified_component(PDF_RECEIPT_PATH, build, "pdf-build.json")
    verified_component(HTML_RECEIPT_PATH, build, "html-build.json")
    epub_receipt_record = verified_component(EPUB_RECEIPT_PATH, build, "epub-build.json")
    dependencies_record = verified_component(DEPENDENCIES_PATH, build, "dependencies.json")

    checks = stage.read_json(CHECKS_PATH)
    require_equal(checks.get("profile"), "final", "final checks profile")
    require_equal(checks.get("status"), "pass", "final checks status")
    page_count = checks.get("pdf", {}).get("page_count")
    if not isinstance(page_count, int) or page_count < 166:
        raise GateError(f"The final PDF page count is invalid: {page_count!r}")
    for key in ("latex_cross_references", "pdf", "html", "epub"):
        item = checks.get(key)
        if not isinstance(item, dict) or item.get("status") != "pass" or item.get("issues") not in (None, []):
            raise GateError(f"The final checks do not pass without issues: {key}")

    root_visual, accepted_at = load_root_visual_record(pdf, page_count)

    pdf_receipt = stage.read_json(PDF_RECEIPT_PATH)
    require_equal(pdf_receipt.get("profile"), "final", "PDF receipt profile")
    require_equal(pdf_receipt.get("status"), "pass", "PDF receipt status")
    require_equal(pdf_receipt.get("byte_identical"), True, "PDF deterministic result")
    require_equal(pdf_receipt.get("deterministic_rebuilds"), 2, "PDF rebuild count")
    require_equal(pdf_receipt.get("page_count"), page_count, "PDF receipt page count")
    require_equal(pdf_receipt.get("output"), pdf, "PDF receipt output")
    for index, run in enumerate(pdf_receipt.get("runs", [])):
        counts = run.get("log_counts") if isinstance(run, dict) else None
        if not isinstance(counts, dict):
            raise GateError(f"PDF run {index} has no log counts")
        for key in ("undefined_references", "undefined_citations", "overfull_boxes"):
            require_zero(counts.get(key), f"PDF run {index} {key}")

    html_receipt = stage.read_json(HTML_RECEIPT_PATH)
    require_equal(html_receipt.get("profile"), "final", "HTML receipt profile")
    require_equal(html_receipt.get("status"), "pass", "HTML receipt status")
    html_runs = html_receipt.get("runs")
    if not isinstance(html_runs, list) or len(html_runs) != 2:
        raise GateError("The HTML receipt must contain two checked builds")
    for index, run in enumerate(html_runs):
        validation = run.get("validation") if isinstance(run, dict) else None
        if not isinstance(validation, dict):
            raise GateError(f"HTML run {index} has no validation result")
        require_equal(validation.get("status"), "pass", f"HTML run {index} validation status")
        require_equal(validation.get("issues"), [], f"HTML run {index} validation issues")

    dependencies = stage.read_json(DEPENDENCIES_PATH)
    tool = dependencies.get("tools", {}).get("epubcheck")
    if not isinstance(tool, dict) or tool.get("available") is not True:
        raise GateError("The dependency receipt does not show EPUBCheck as available")
    provenance = tool.get("provenance")
    if not isinstance(provenance, dict):
        raise GateError("The EPUBCheck dependency record has no provenance")
    runtime_hash = provenance.get("runtime_jar_sha256")
    if not isinstance(runtime_hash, str) or not stage.SHA256_RE.fullmatch(runtime_hash):
        raise GateError("The EPUBCheck runtime SHA-256 is invalid")
    lock = stage.read_json(EPUBCHECK_LOCK_PATH)
    require_equal(lock.get("version"), "5.4.0", "EPUBCheck lock version")
    runtime_path = ROOT / Path(lock["runtime_jar"])
    stage.require_file(runtime_path)
    require_equal(stage.sha256_path(runtime_path), runtime_hash, "EPUBCheck runtime SHA-256")

    epub_receipt = stage.read_json(EPUB_RECEIPT_PATH)
    require_equal(epub_receipt.get("profile"), "final", "EPUB receipt profile")
    require_equal(epub_receipt.get("status"), "pass", "EPUB receipt status")
    require_equal(epub_receipt.get("byte_identical_after_canonical_packaging"), True, "EPUB deterministic result")
    require_equal(epub_receipt.get("deterministic_rebuilds"), 2, "EPUB rebuild count")
    require_equal(epub_receipt.get("validation", {}).get("status"), "pass", "EPUB internal validation")
    require_equal(epub_receipt.get("output"), epub, "EPUB receipt output")
    epubcheck = epub_receipt.get("epubcheck")
    if not isinstance(epubcheck, dict):
        raise GateError("The EPUB receipt has no EPUBCheck result")
    require_equal(epubcheck.get("status"), "pass", "EPUBCheck result")
    require_zero(epubcheck.get("exit_code"), "EPUBCheck exit code")
    require_equal(epubcheck.get("timed_out"), False, "EPUBCheck timeout marker")

    audit_record = stage.file_record(stage.require_file(AUDIT_PATH))
    audit = stage.read_json(AUDIT_PATH)
    require_equal(audit.get("status"), "pass", "Everyday audit status")
    require_equal(audit.get("expected_ranges"), 29, "Everyday audit range count")
    require_equal(audit.get("global_issues"), [], "Everyday audit issues")
    require_equal(audit.get("global_pending"), [], "Everyday audit pending work")
    audit_counts = audit.get("range_status_counts")
    if not isinstance(audit_counts, dict):
        raise GateError("The Everyday audit has no range counts")
    require_equal(audit_counts, {"fail": 0, "pass": 29, "pending": 0}, "Everyday audit range counts")

    cross_counts = checks.get("latex_cross_references", {}).get("counts")
    if not isinstance(cross_counts, dict):
        raise GateError("The final checks have no LaTeX cross-reference counts")

    scan_record = record_for_bytes(SCAN_PATH, scan_payload)
    ledger_record = stage.file_record(VISUAL_LEDGER_PATH)
    lock_record = stage.file_record(EPUBCHECK_LOCK_PATH)
    qa = {
        "schema": "navier-stokes-everyday-final-qa/v1",
        "receipt_id": stage.EXPECTED_QA_ID,
        "edition": stage.EXPECTED_TITLE,
        "status": "pass",
        "accepted_at": accepted_at,
        "final_build": {
            "profile": "final",
            "status": "pass",
            "receipt": stage.file_record(BUILD_RECEIPT_PATH),
        },
        "artifacts": {
            "pdf": {**pdf, "page_count": page_count},
            "html": {**html, "validator_status": "pass", "direct_index_path": "docs/index.html"},
            "epub": epub,
        },
        "visual_qa": {
            "record_id": root_visual["id"],
            "status": "pass",
            "scope": "every-page",
            "inspected_pages": root_visual["inspected_pages"],
            "ledger": ledger_record,
        },
        "html_validation": {"status": "pass", "receipt": checks_record},
        "epubcheck": {
            "status": "pass",
            "version": "5.4.0",
            "runtime_jar_sha256": runtime_hash,
            "lock": lock_record,
            "dependencies_receipt": dependencies_record,
            "epub_receipt": epub_receipt_record,
        },
        "everyday_audit": {
            "status": "pass",
            "range_count": 29,
            "failed_ranges": 0,
            "pending_ranges": 0,
            "receipt": audit_record,
        },
        "scans": {
            "receipt": scan_record,
            "disallowed_token": {"status": "pass", "matches": 0},
            "authorial_we": {"status": "pass", "matches": 0},
            "local_path_leaks": {"status": "pass", "matches": 0},
        },
        "structure": {
            "unresolved_references": 0,
            "unresolved_citations": 0,
            "overfull_boxes": 0,
            "checks_receipt": checks_record,
            "pdf_receipt": pdf_receipt_record,
        },
        "publication_performed": False,
    }
    validate_against_schema(qa, QA_SCHEMA_PATH, "final QA receipt")
    stage.validate_output_manifest()
    return qa


def assemble_receipts() -> tuple[dict[str, Any], bytes, dict[str, Any], bytes]:
    build = stage.read_json(BUILD_RECEIPT_PATH)
    pdf = output_record(build, PDF_PATH)
    checks = stage.read_json(CHECKS_PATH)
    page_count = checks.get("pdf", {}).get("page_count")
    if not isinstance(page_count, int):
        raise GateError("The final checks have no PDF page count")
    _, generated_at = load_root_visual_record(pdf, page_count)
    scans = build_scan_receipt(generated_at)
    scan_payload = json_bytes(scans)
    qa = build_final_qa(scan_payload)
    qa_payload = json_bytes(qa)
    return scans, scan_payload, qa, qa_payload


def write_if_allowed(path: Path, payload: bytes, replace: bool) -> str:
    if path.exists():
        existing = path.read_bytes()
        if existing == payload:
            return "unchanged"
        if not replace:
            raise GateError(f"Refusing to replace a different receipt without --replace: {path.relative_to(ROOT)}")
    temporary = path.with_name(path.name + ".next")
    if temporary.exists():
        temporary.unlink()
    temporary.write_bytes(payload)
    os.replace(temporary, path)
    return "written"


def schema_status() -> dict[str, Any]:
    load_schema(SCAN_SCHEMA_PATH)
    load_schema(QA_SCHEMA_PATH)
    return {
        "status": "pass",
        "schemas": [
            SCAN_SCHEMA_PATH.relative_to(ROOT).as_posix(),
            QA_SCHEMA_PATH.relative_to(ROOT).as_posix(),
        ],
        "publication_performed": False,
    }


def main(argv: Sequence[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("check-schemas", "status", "write"))
    parser.add_argument("--replace", action="store_true", help="Replace different existing receipt files.")
    args = parser.parse_args(argv)
    try:
        if args.command == "check-schemas":
            result = schema_status()
        else:
            scans, scan_payload, qa, qa_payload = assemble_receipts()
            if args.command == "status":
                result = {
                    "status": "ready",
                    "scan_receipt": record_for_bytes(SCAN_PATH, scan_payload),
                    "final_qa": record_for_bytes(QA_PATH, qa_payload),
                    "accepted_at": qa["accepted_at"],
                    "files_scanned": len(scans["files"]),
                    "publication_performed": False,
                }
            else:
                scan_action = write_if_allowed(SCAN_PATH, scan_payload, args.replace)
                qa_action = write_if_allowed(QA_PATH, qa_payload, args.replace)
                stage.validate_release_gate()
                result = {
                    "status": "pass",
                    "scan_receipt": {**stage.file_record(SCAN_PATH), "action": scan_action},
                    "final_qa": {**stage.file_record(QA_PATH), "action": qa_action},
                    "publication_performed": False,
                }
    except (GateError, stage.StageError, OSError, ValueError, KeyError) as exc:
        result = {
            "status": "blocked",
            "command": args.command,
            "message": str(exc),
            "publication_performed": False,
        }
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
