#!/usr/bin/env python3
"""Fail-closed audit for one Everyday English translation range.

Exit status 0 means pass, 1 means fail, and 2 means pending.  The module uses
only the Python standard library and exposes ``audit_range`` for the aggregate
auditor and the isolated fixture test.
"""

from __future__ import annotations

import argparse
import bisect
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parent.parent
EXPECTED_RANGES = tuple(f"pp{first:03d}-{first + 5:03d}" for first in range(1, 163, 6)) + (
    "pp163-164",
    "pp165-166",
)
LEDGERS = {
    "SEGMENTS.jsonl": ("SEGMENTS.schema.json", "segment"),
    "CHANGES.jsonl": ("CHANGES.schema.json", "change"),
    "ADDITIONS.jsonl": ("ADDITIONS.schema.json", "addition"),
    "MATHEMATICS.jsonl": ("MATHEMATICS.schema.json", "mathematics"),
    "FIRST_USE_CANDIDATES.jsonl": ("FIRST_USE_CANDIDATES.schema.json", "first_use_candidate"),
}
REQUIRED_SCHEMA_FIELDS = {
    "segment": {
        "id", "record_type", "status", "pdf_pages", "source", "target", "relation",
        "mathematical_content", "decoding_burdens", "consequential_choices", "discourse_job",
        "predicted_comprehension_mechanism", "academic_register_knowledge_removed",
        "retained_technical_terms", "risks", "checks_performed", "alternatives_considered",
        "same_meaning", "checks", "supersession",
    },
    "change": {
        "id", "record_type", "status", "pdf_pages", "source_segment_ids",
        "target_segment_ids", "change_kind", "exact_change", "reason",
        "rejected_alternatives", "canon_support", "canon_gap", "mathematical_risk",
        "validation_outcome", "supersession",
    },
    "addition": {
        "id", "record_type", "status", "pdf_pages", "target", "placement",
        "source_dependencies", "mathematical_claim_map", "proof_records", "notation_checks",
        "scope_checks", "defines_concept", "accepting_examples", "rejecting_examples",
        "does_not_claim", "supersession",
    },
    "mathematics": {
        "id", "record_type", "status", "pdf_pages", "target_ids", "claims", "definitions",
        "formulas", "dependencies", "source_authorities", "bidirectional_coverage",
        "formula_marker_identity", "checks", "lean_mapping", "lean_coverage_gap",
        "supersession",
    },
    "first_use_candidate": {
        "id", "record_type", "status", "pdf_pages", "concept", "local_first_target_id",
        "source_locator", "prerequisite_concepts", "earlier_occurrence_check",
        "proposed_addition_id", "later_reuse_ids", "global_resolution", "supersession",
    },
}
RANGE_RE = re.compile(r"^pp([0-9]{3})-([0-9]{3})$")
TARGET_ID_RE = re.compile(r"^EE-TGT-P([0-9]{3})-([0-9]{3})$")
ADDITION_ID_RE = re.compile(r"^EE-ADD-P([0-9]{3})-([0-9]{3})$")
NS_ID_RE = re.compile(r"^NS-F-P([0-9]{3})-([0-9]{3})$")
DISPLAY_ENVS = ("equation", "equation*", "align", "align*", "gather", "gather*", "multline", "multline*")


@dataclass(frozen=True)
class LoadedRow:
    path: Path
    line: int
    data: dict[str, Any]
    schema_valid: bool


@dataclass(frozen=True)
class TargetEnvironment:
    kind: str
    target_id: str
    title: str | None
    body: str
    body_sha256: str
    start: int
    end: int
    page: int | None


@dataclass(frozen=True)
class MathMarker:
    macro: str
    marker_id: str
    page: int
    ordinal: int
    start: int
    end: int
    marker_kind: str | None
    printed_number: str | None
    math_text: str
    math_sha256: str


class Findings:
    def __init__(self) -> None:
        self.issues: list[dict[str, Any]] = []
        self.pending: list[dict[str, Any]] = []

    def fail(self, code: str, message: str, **context: Any) -> None:
        item: dict[str, Any] = {"code": code, "message": message}
        item.update(context)
        self.issues.append(item)

    def defer(self, code: str, message: str, **context: Any) -> None:
        item: dict[str, Any] = {"code": code, "message": message}
        item.update(context)
        self.pending.append(item)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def _reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate object key {key!r}")
        result[key] = value
    return result


def _reject_json_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number {value}")


def parse_json(text: str) -> Any:
    return json.loads(
        text,
        object_pairs_hook=_reject_duplicate_keys,
        parse_constant=_reject_json_constant,
    )


def read_utf8(path: Path) -> tuple[bytes, str]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("UTF-8 BOM is not permitted")
    return raw, raw.decode("utf-8")


def _schema_type_matches(value: Any, expected: str) -> bool:
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    return False


def _resolve_local_ref(reference: str, root_schema: dict[str, Any]) -> dict[str, Any]:
    if not reference.startswith("#/"):
        raise ValueError(f"only local schema references are supported: {reference!r}")
    node: Any = root_schema
    for raw_part in reference[2:].split("/"):
        part = raw_part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            raise ValueError(f"unresolved schema reference {reference!r}")
        node = node[part]
    if not isinstance(node, dict):
        raise ValueError(f"schema reference does not name an object: {reference!r}")
    return node


def schema_errors(
    value: Any,
    schema: dict[str, Any],
    root_schema: dict[str, Any] | None = None,
    location: str = "$",
) -> list[str]:
    root_schema = root_schema or schema
    if "$ref" in schema:
        try:
            referred = _resolve_local_ref(schema["$ref"], root_schema)
        except ValueError as exc:
            return [f"{location}: {exc}"]
        return schema_errors(value, referred, root_schema, location)

    if "oneOf" in schema:
        branches = [schema_errors(value, branch, root_schema, location) for branch in schema["oneOf"]]
        if sum(not branch_errors for branch_errors in branches) != 1:
            return [f"{location}: value must satisfy exactly one oneOf branch"]
    if "anyOf" in schema:
        branches = [schema_errors(value, branch, root_schema, location) for branch in schema["anyOf"]]
        if all(branch_errors for branch_errors in branches):
            return [f"{location}: value does not satisfy any anyOf branch"]

    errors: list[str] = []
    expected_type = schema.get("type")
    if expected_type is not None:
        types = expected_type if isinstance(expected_type, list) else [expected_type]
        if not any(_schema_type_matches(value, item) for item in types):
            return [f"{location}: expected type {' or '.join(types)}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{location}: expected constant {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: value {value!r} is not in the allowed enumeration")

    if isinstance(value, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in value:
                errors.append(f"{location}: missing required property {key!r}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{location}: unexpected property {key!r}")
        for key, subschema in properties.items():
            if key in value:
                errors.extend(schema_errors(value[key], subschema, root_schema, f"{location}.{key}"))

    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: expected at least {schema['minItems']} items")
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            errors.append(f"{location}: expected at most {schema['maxItems']} items")
        if schema.get("uniqueItems"):
            rendered = [json.dumps(item, ensure_ascii=False, sort_keys=True, separators=(",", ":")) for item in value]
            if len(rendered) != len(set(rendered)):
                errors.append(f"{location}: array items are not unique")
        if isinstance(schema.get("items"), dict):
            for index, item in enumerate(value):
                errors.extend(schema_errors(item, schema["items"], root_schema, f"{location}[{index}]"))

    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{location}: string is shorter than {schema['minLength']}")
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            errors.append(f"{location}: string is longer than {schema['maxLength']}")
        if "pattern" in schema:
            try:
                matched = re.search(schema["pattern"], value)
            except re.error as exc:
                errors.append(f"{location}: invalid schema pattern: {exc}")
            else:
                if matched is None:
                    errors.append(f"{location}: string does not match {schema['pattern']!r}")

    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{location}: value is less than {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{location}: value is greater than {schema['maximum']}")
    return errors


def load_schemas(root: Path, findings: Findings) -> dict[str, dict[str, Any]]:
    schemas: dict[str, dict[str, Any]] = {}
    for ledger_name, (schema_name, record_type) in LEDGERS.items():
        path = root / "evidence" / "schemas" / schema_name
        if not path.is_file():
            findings.fail("missing-schema", "Required record schema is missing.", path=path.as_posix())
            continue
        try:
            _, text = read_utf8(path)
            schema = parse_json(text)
        except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
            findings.fail("invalid-schema-json", "Schema is not strict UTF-8 JSON.", path=path.as_posix(), detail=str(exc))
            continue
        if not isinstance(schema, dict):
            findings.fail("invalid-schema-root", "Schema root must be an object.", path=path.as_posix())
            continue
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            findings.fail("schema-draft", "Schema must identify JSON Schema draft 2020-12.", path=path.as_posix())
        if schema.get("type") != "object" or schema.get("additionalProperties") is not False:
            findings.fail("schema-fail-closed-root", "Record schema root must be an object with additionalProperties false.", path=path.as_posix())
        const = schema.get("properties", {}).get("record_type", {}).get("const")
        if const != record_type:
            findings.fail("schema-record-type", "Schema record_type identity is wrong.", path=path.as_posix(), expected=record_type, observed=const)
        required = set(schema.get("required", []))
        missing_required = sorted(REQUIRED_SCHEMA_FIELDS[record_type] - required)
        if missing_required:
            findings.fail("schema-required-fields", "Schema omits protocol-required fields.", path=path.as_posix(), fields=missing_required)
        schemas[ledger_name] = schema
    return schemas


def load_jsonl(path: Path, schema: dict[str, Any], findings: Findings) -> list[LoadedRow]:
    try:
        raw, text = read_utf8(path)
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        findings.fail("jsonl-encoding", "Ledger is not strict UTF-8 without a BOM.", path=path.as_posix(), detail=str(exc))
        return []
    if not raw:
        return []
    rows: list[LoadedRow] = []
    for line_number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            findings.fail("jsonl-blank-line", "A nonempty JSONL file may not contain blank lines.", path=path.as_posix(), line=line_number)
            continue
        try:
            value = parse_json(line)
        except (ValueError, json.JSONDecodeError) as exc:
            findings.fail("jsonl-json", "JSONL line is invalid JSON.", path=path.as_posix(), line=line_number, detail=str(exc))
            continue
        if not isinstance(value, dict):
            findings.fail("jsonl-object", "Every JSONL line must be one object.", path=path.as_posix(), line=line_number)
            continue
        errors = schema_errors(value, schema)
        for error in errors:
            findings.fail("schema-validation", "Record does not satisfy its JSON Schema.", path=path.as_posix(), line=line_number, detail=error)
        rows.append(LoadedRow(path, line_number, value, not errors))
    return rows


def mask_tex_comments(text: str) -> str:
    chars = list(text)
    index = 0
    while index < len(chars):
        if chars[index] == "%":
            slash_count = 0
            probe = index - 1
            while probe >= 0 and chars[probe] == "\\":
                slash_count += 1
                probe -= 1
            if slash_count % 2 == 0:
                while index < len(chars) and chars[index] not in "\r\n":
                    chars[index] = " "
                    index += 1
                continue
        index += 1
    return "".join(chars)


def _skip_space(text: str, index: int) -> int:
    while index < len(text) and text[index].isspace():
        index += 1
    return index


def _parse_braced(text: str, opening: int) -> tuple[int, int, int]:
    if opening >= len(text) or text[opening] != "{":
        raise ValueError("expected an opening brace")
    depth = 0
    for index in range(opening, len(text)):
        char = text[index]
        slash_count = 0
        probe = index - 1
        while probe >= 0 and text[probe] == "\\":
            slash_count += 1
            probe -= 1
        escaped = slash_count % 2 == 1
        if char == "{" and not escaped:
            depth += 1
        elif char == "}" and not escaped:
            depth -= 1
            if depth == 0:
                return opening + 1, index, index + 1
    raise ValueError("unclosed braced argument")


def page_markers(masked: str) -> list[tuple[int, int]]:
    return [(match.start(), int(match.group(1))) for match in re.finditer(r"\\NSPage\{([0-9]{3})\}", masked)]


def page_at_offset(markers: list[tuple[int, int]], offset: int) -> int | None:
    offsets = [item[0] for item in markers]
    index = bisect.bisect_right(offsets, offset) - 1
    return markers[index][1] if index >= 0 else None


def parse_target_environments(text: str, kind: str, markers: list[tuple[int, int]], findings: Findings, path: Path) -> list[TargetEnvironment]:
    masked = mask_tex_comments(text)
    begin_pattern = re.compile(rf"\\begin\s*\{{\s*{re.escape(kind)}\s*\}}")
    end_pattern = re.compile(rf"\\end\s*\{{\s*{re.escape(kind)}\s*\}}")
    environments: list[TargetEnvironment] = []
    cursor = 0
    while True:
        begin = begin_pattern.search(masked, cursor)
        if begin is None:
            break
        try:
            arg_start = _skip_space(masked, begin.end())
            id_inner_start, id_inner_end, after_id = _parse_braced(masked, arg_start)
            target_id = text[id_inner_start:id_inner_end]
            title: str | None = None
            after_args = after_id
            if kind == "EEAddition":
                title_open = _skip_space(masked, after_id)
                title_start, title_end, after_args = _parse_braced(masked, title_open)
                title = text[title_start:title_end]
        except ValueError as exc:
            findings.fail("target-environment-open", "Malformed target environment opening.", path=path.as_posix(), environment=kind, line=text.count("\n", 0, begin.start()) + 1, detail=str(exc))
            cursor = begin.end()
            continue
        end = end_pattern.search(masked, after_args)
        nested = begin_pattern.search(masked, after_args)
        if end is None:
            findings.fail("target-environment-close", "Target environment has no closing command.", path=path.as_posix(), environment=kind, target_id=target_id)
            break
        if nested is not None and nested.start() < end.start():
            findings.fail("target-environment-nesting", "Target environments of the same kind may not nest.", path=path.as_posix(), environment=kind, target_id=target_id)
        body = text[after_args:end.start()]
        environments.append(
            TargetEnvironment(
                kind=kind,
                target_id=target_id,
                title=title,
                body=body,
                body_sha256=sha256_bytes(body.encode("utf-8")),
                start=begin.start(),
                end=end.end(),
                page=page_at_offset(markers, begin.start()),
            )
        )
        cursor = end.end()
    unmatched_ends = len(list(end_pattern.finditer(masked))) - len(environments)
    if unmatched_ends:
        findings.fail("target-environment-balance", "Target environment begin/end counts differ.", path=path.as_posix(), environment=kind, unmatched_ends=unmatched_ends)
    return environments


def _capture_display(text: str, masked: str, start: int) -> tuple[str, int]:
    start = _skip_space(masked, start)
    if masked.startswith(r"\[", start):
        closing = masked.find(r"\]", start + 2)
        if closing < 0:
            raise ValueError("unclosed \\[ display")
        end = closing + 2
        return text[start:end], end
    opening = re.compile(r"\\begin\s*\{\s*(equation\*?|align\*?|gather\*?|multline\*?)\s*\}").match(masked, start)
    if opening is None:
        raise ValueError("NSFormula is not followed by a recognized display environment")
    environment = opening.group(1)
    token_pattern = re.compile(rf"\\(begin|end)\s*\{{\s*{re.escape(environment)}\s*\}}")
    depth = 0
    for token in token_pattern.finditer(masked, start):
        if token.group(1) == "begin":
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return text[start:token.end()], token.end()
    raise ValueError(f"unclosed {environment} display")


def parse_math_markers(text: str, findings: Findings, path: Path) -> list[MathMarker]:
    masked = mask_tex_comments(text)
    markers = page_markers(masked)
    result: list[MathMarker] = []
    macro_pattern = re.compile(r"\\(NSi|NSFormula)(?![A-Za-z@])")
    for match in macro_pattern.finditer(masked):
        argument_count = 2 if match.group(1) == "NSi" else 3
        cursor = match.end()
        arguments: list[str] = []
        try:
            for _ in range(argument_count):
                cursor = _skip_space(masked, cursor)
                inner_start, inner_end, cursor = _parse_braced(masked, cursor)
                arguments.append(text[inner_start:inner_end])
        except ValueError as exc:
            findings.fail("math-marker-parse", "Malformed NS mathematics marker.", path=path.as_posix(), line=text.count("\n", 0, match.start()) + 1, detail=str(exc))
            continue
        id_match = NS_ID_RE.fullmatch(arguments[0])
        if id_match is None:
            findings.fail("math-marker-id", "Mathematics marker has an invalid NS-F ID.", path=path.as_posix(), marker_id=arguments[0])
            continue
        actual_page = page_at_offset(markers, match.start())
        encoded_page = int(id_match.group(1))
        if actual_page != encoded_page:
            findings.fail("math-marker-page", "Mathematics marker ID page does not match its NSPage position.", path=path.as_posix(), marker_id=arguments[0], encoded_page=encoded_page, actual_page=actual_page)
        if match.group(1) == "NSi":
            math_text = arguments[1]
            marker_kind = None
            printed_number = None
            end = cursor
        else:
            marker_kind = arguments[1]
            printed_number = arguments[2]
            if marker_kind != "display":
                findings.fail("display-marker-kind", "NSFormula kind must remain 'display'.", path=path.as_posix(), marker_id=arguments[0], observed=marker_kind)
            try:
                math_text, end = _capture_display(text, masked, cursor)
            except ValueError as exc:
                findings.fail("display-parse", "Could not bind NSFormula to its display.", path=path.as_posix(), marker_id=arguments[0], detail=str(exc))
                math_text = ""
                end = cursor
        result.append(
            MathMarker(
                macro=match.group(1),
                marker_id=arguments[0],
                page=encoded_page,
                ordinal=int(id_match.group(2)),
                start=match.start(),
                end=end,
                marker_kind=marker_kind,
                printed_number=printed_number,
                math_text=math_text,
                math_sha256=sha256_bytes(math_text.encode("utf-8")),
            )
        )
    return result


def _blank_ranges(text: str, ranges: Iterable[tuple[int, int]]) -> str:
    chars = list(text)
    for start, end in ranges:
        for index in range(max(0, start), min(len(chars), end)):
            if chars[index] not in "\r\n":
                chars[index] = " "
    return "".join(chars)


def _all_display_ranges(masked: str) -> list[tuple[int, int]]:
    ranges: list[tuple[int, int]] = []
    cursor = 0
    bracket_open = re.compile(r"\\\[")
    env_open = re.compile(r"\\begin\s*\{\s*(equation\*?|align\*?|gather\*?|multline\*?)\s*\}")
    while cursor < len(masked):
        bracket = bracket_open.search(masked, cursor)
        environment = env_open.search(masked, cursor)
        candidates = [item for item in (bracket, environment) if item is not None]
        if not candidates:
            break
        opening = min(candidates, key=lambda item: item.start())
        if opening.re is bracket_open:
            closing = masked.find(r"\]", opening.end())
            if closing < 0:
                break
            ranges.append((opening.start(), closing + 2))
            cursor = closing + 2
        else:
            env = opening.group(1)
            close = re.compile(rf"\\end\s*\{{\s*{re.escape(env)}\s*\}}").search(masked, opening.end())
            if close is None:
                break
            ranges.append((opening.start(), close.end()))
            cursor = close.end()
    return ranges


def _whole_environment_ranges(masked: str, environment_name: str) -> list[tuple[int, int]]:
    opening = re.compile(rf"\\begin\s*\{{\s*{re.escape(environment_name)}\s*\}}")
    closing = re.compile(rf"\\end\s*\{{\s*{re.escape(environment_name)}\s*\}}")
    ranges: list[tuple[int, int]] = []
    cursor = 0
    while True:
        begin = opening.search(masked, cursor)
        if begin is None:
            break
        end = closing.search(masked, begin.end())
        if end is None:
            break
        ranges.append((begin.start(), end.end()))
        cursor = end.end()
    return ranges


def find_unwrapped_prose(text: str, environments: list[TargetEnvironment]) -> list[dict[str, Any]]:
    masked = mask_tex_comments(text)
    ranges = [(env.start, env.end) for env in environments]
    ranges.extend(_all_display_ranges(masked))
    # Reference entries are bibliography data, explicitly exempt from prose
    # wrapping.  A heading or explanatory paragraph outside this environment
    # remains visible to the prose detector.
    ranges.extend(_whole_environment_ranges(masked, "thebibliography"))
    # Inline mathematics and marker metadata are non-prose.
    dummy = Findings()
    for marker in parse_math_markers(text, dummy, Path("<target>")):
        ranges.append((marker.start, marker.end))
    residual = _blank_ranges(masked, ranges)
    # Inline TeX math which is not an NS marker is still pure mathematics.
    residual = re.sub(r"\$\$(?:.|\r|\n)*?\$\$", lambda m: " " * len(m.group(0)), residual)
    residual = re.sub(r"(?<!\\)\$(?:\\.|[^$])*?(?<!\\)\$", lambda m: " " * len(m.group(0)), residual)
    # Commands whose arguments are structural data rather than rendered prose.
    data_command = re.compile(r"\\(?:NSPage|NSFormula|label|ref|eqref|cref|Cref|pageref|cite|citep|citet|bibitem|url|href|input|include|includegraphics|NSFigurePlaceholder|tag|bibliography|bibliographystyle|setcounter|setlength|addcontentsline|markboth|thispagestyle)\b")
    chars = list(residual)
    for command in data_command.finditer(residual):
        cursor = command.end()
        end = cursor
        # Remove optional and braced arguments, tolerating nested braced groups.
        while True:
            cursor = _skip_space(residual, cursor)
            if cursor < len(residual) and residual[cursor] == "[":
                closing = residual.find("]", cursor + 1)
                if closing < 0:
                    break
                cursor = closing + 1
                end = cursor
                continue
            if cursor < len(residual) and residual[cursor] == "{":
                try:
                    _, _, cursor = _parse_braced(residual, cursor)
                except ValueError:
                    break
                end = cursor
                continue
            break
        for index in range(command.start(), end):
            if chars[index] not in "\r\n":
                chars[index] = " "
    residual = "".join(chars)
    residual = re.sub(r"\\(?:begin|end)\s*\{[^{}]*\}", " ", residual)
    residual = re.sub(r"\[[^\]]*\]", " ", residual)
    residual = re.sub(r"\\[A-Za-z@]+\*?|\\.", " ", residual)
    residual = residual.replace("\\", " ")
    findings: list[dict[str, Any]] = []
    for line_number, line in enumerate(residual.splitlines(), start=1):
        structural_tokens = {"em", "ex", "pt", "cm", "mm", "in", "bp", "pc", "dd", "sp", "fil", "fill", "filll"}
        words = [
            word for word in re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ]{2,}", line)
            if word.casefold() not in structural_tokens and not re.fullmatch(r"[lcrpmb]+", word, re.IGNORECASE)
        ]
        if words:
            findings.append({"line": line_number, "tokens": words[:8], "text": line.strip()[:200]})
    return findings


def body_has_prose(body: str) -> bool:
    masked = mask_tex_comments(body)
    masked = re.sub(r"\$\$(?:.|\r|\n)*?\$\$", " ", masked)
    masked = re.sub(r"(?<!\\)\$(?:\\.|[^$])*?(?<!\\)\$", " ", masked)
    masked = re.sub(r"\\[A-Za-z@]+\*?|\\.", " ", masked)
    return re.search(r"[A-Za-zÀ-ÖØ-öø-ÿ]{2,}", masked) is not None


def exact_line_span(raw: bytes, start: int, end: int) -> bytes:
    lines = raw.splitlines(keepends=True)
    if start < 1 or end < start or end > len(lines):
        raise ValueError(f"line span {start}-{end} is outside 1-{len(lines)}")
    return b"".join(lines[start - 1:end])


def line_pages(text: str) -> list[int | None]:
    result: list[int | None] = []
    current: int | None = None
    for line in mask_tex_comments(text).splitlines(keepends=True):
        marker = re.search(r"\\NSPage\{([0-9]{3})\}", line)
        if marker:
            current = int(marker.group(1))
        result.append(current)
    if text and not text.endswith(("\n", "\r")) and not result:
        result.append(current)
    return result


def _record_location(row: LoadedRow) -> dict[str, Any]:
    return {"path": row.path.as_posix(), "line": row.line, "record_id": row.data.get("id")}


def _live(rows: Iterable[LoadedRow]) -> list[LoadedRow]:
    return [row for row in rows if row.schema_valid and row.data.get("status") != "superseded"]


def _check_ordered_pages(row: LoadedRow, first: int, last: int, findings: Findings) -> None:
    pages = row.data.get("pdf_pages")
    if not isinstance(pages, list) or any(not isinstance(page, int) for page in pages):
        return
    if pages != sorted(pages) or len(pages) != len(set(pages)):
        findings.fail("record-page-order", "pdf_pages must be strictly increasing.", **_record_location(row), observed=pages)
    outside = [page for page in pages if page < first or page > last]
    if outside:
        findings.fail("record-range-ownership", "Record cites a PDF page outside its owned range.", **_record_location(row), pages=outside)


def _walk_results(value: Any, location: str = "$") -> Iterable[tuple[str, str]]:
    if isinstance(value, dict):
        for key, child in value.items():
            child_location = f"{location}.{key}"
            if key in {"result", "outcome", "identity_result"} and isinstance(child, str):
                yield child_location, child
            yield from _walk_results(child, child_location)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from _walk_results(child, f"{location}[{index}]")


def _check_record_status(row: LoadedRow, findings: Findings) -> None:
    if not row.schema_valid:
        return
    status = row.data.get("status")
    if status == "superseded":
        if not row.data.get("supersession", {}).get("superseded_by"):
            findings.fail("superseded-without-successor", "A superseded record must name its successor.", **_record_location(row))
        return
    if row.data.get("supersession", {}).get("superseded_by"):
        findings.fail("live-record-has-successor", "A live record may not name a superseding record.", **_record_location(row))
    if status == "fail":
        findings.fail("record-fail", "A live evidence record is explicitly failed.", **_record_location(row))
    elif status == "pending":
        findings.defer("record-pending", "A live evidence record is pending.", **_record_location(row))
    elif status == "pass":
        for location, result in _walk_results(row.data):
            if result in {"pending", "fail", "unresolved"}:
                findings.fail("pass-record-unresolved-check", "A pass record contains a non-passing check.", **_record_location(row), check=location, observed=result)


def _check_canon_support(container: dict[str, Any], row: LoadedRow, accepted_ids: set[str], findings: Findings, label: str) -> None:
    support = container.get("canon_support")
    gap = container.get("canon_gap")
    if not isinstance(support, list):
        return
    has_gap = isinstance(gap, str) and bool(gap.strip())
    if support and has_gap:
        findings.fail("canon-support-and-gap", "Canon support and a canon gap may not both be asserted.", **_record_location(row), field=label)
    elif not support and not has_gap:
        findings.fail("canon-unaccounted", "Consequential wording needs checked canon support or an explicit fail-closed gap.", **_record_location(row), field=label)
    elif not support:
        if row.data.get("status") == "pass":
            findings.fail("pass-with-canon-gap", "A pass record may not contain an unresolved canon gap.", **_record_location(row), field=label)
        else:
            findings.defer("canon-gap", "Canon support is unresolved.", **_record_location(row), field=label, gap=gap)
    for item in support:
        if isinstance(item, dict) and item.get("passage_id") not in accepted_ids:
            findings.fail("unknown-canon-passage", "Canon support cites an ID absent from the checked routing index.", **_record_location(row), field=label, passage_id=item.get("passage_id"))


def load_canon_ids(root: Path, findings: Findings) -> set[str]:
    path = root / "evidence" / "canon" / "CANON_ROUTING_INDEX.json"
    if not path.is_file():
        findings.fail("missing-canon-index", "Checked canon routing index is missing.", path=path.as_posix())
        return set()
    try:
        _, text = read_utf8(path)
        data = parse_json(text)
    except (OSError, UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        findings.fail("invalid-canon-index", "Canon routing index is not strict JSON.", path=path.as_posix(), detail=str(exc))
        return set()
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        findings.fail("invalid-canon-entries", "Canon routing index lacks an entries array.", path=path.as_posix())
        return set()
    ids = [entry.get("canon_id") for entry in entries if isinstance(entry, dict)]
    if any(not isinstance(item, str) for item in ids) or len(ids) != len(entries):
        findings.fail("invalid-canon-id", "Every canon entry needs a string canon_id.", path=path.as_posix())
    duplicates = sorted(item for item, count in Counter(ids).items() if count > 1 and isinstance(item, str))
    if duplicates:
        findings.fail("duplicate-canon-id", "Canon routing index contains duplicate IDs.", path=path.as_posix(), ids=duplicates)
    declared = data.get("counts", {}).get("accepted_passages") if isinstance(data, dict) else None
    if declared != len(entries):
        findings.fail("canon-count", "Canon accepted-passages count does not match entries.", path=path.as_posix(), declared=declared, observed=len(entries))
    control = data.get("source_corpus", {}).get("control_status", {}) if isinstance(data, dict) else {}
    expected_control = {"build_report": "pass", "canon_report": "pass", "reference_layers_report": "pass"}
    if control != expected_control:
        findings.fail("canon-control-status", "Canon routing index is not bound to passing corpus control reports.", path=path.as_posix(), expected=expected_control, observed=control)
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            continue
        basis = entry.get("selection_basis", {})
        expected_basis = {
            "in_checked_canon_manifest": True,
            "source_pool_status": "included",
            "verified_direct_human_language": True,
            "positive_reference_layer_member": True,
        }
        if basis != expected_basis:
            findings.fail("canon-selection-basis", "Canon entry lacks the complete accepted human-passage selection basis.", path=path.as_posix(), entry=index, canon_id=entry.get("canon_id"), expected=expected_basis, observed=basis)
    return {item for item in ids if isinstance(item, str)}


def _safe_relative_path(root: Path, value: Any) -> Path | None:
    if not isinstance(value, str) or not value or "\\" in value:
        return None
    candidate = Path(value)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    resolved = (root / candidate).resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def _check_file_authority(root: Path, path_value: Any, hash_value: Any, row: LoadedRow, findings: Findings, label: str, require_hash: bool = True) -> None:
    path = _safe_relative_path(root, path_value)
    if path is None:
        findings.fail("authority-path", "Authority path is not a safe canonical relative path.", **_record_location(row), field=label, observed=path_value)
        return
    if not path.is_file():
        findings.fail("authority-file-missing", "Authority file is missing.", **_record_location(row), field=label, authority_path=str(path_value))
        return
    if hash_value is None:
        if require_hash:
            findings.fail("authority-hash-missing", "A live passing authority needs its current file SHA-256.", **_record_location(row), field=label, authority_path=str(path_value))
        return
    observed = sha256_path(path)
    if observed != hash_value:
        findings.fail("authority-hash", "Authority file SHA-256 is stale or false.", **_record_location(row), field=label, authority_path=str(path_value), expected=hash_value, observed=observed)


def _check_span(raw: bytes, text: str, span: dict[str, Any], row: LoadedRow, findings: Findings, label: str) -> tuple[int, int] | None:
    start = span.get("line_start")
    end = span.get("line_end")
    if not isinstance(start, int) or not isinstance(end, int):
        return None
    try:
        selected = exact_line_span(raw, start, end)
    except ValueError as exc:
        findings.fail("source-span-bounds", "Source line span is invalid.", **_record_location(row), field=label, detail=str(exc))
        return None
    observed = sha256_bytes(selected)
    if observed != span.get("span_sha256"):
        findings.fail("source-span-hash", "Source line-span SHA-256 is stale or false.", **_record_location(row), field=label, expected=span.get("span_sha256"), observed=observed)
    return start, end


def _id_page_ordinal(identifier: str, pattern: re.Pattern[str]) -> tuple[int, int] | None:
    match = pattern.fullmatch(identifier)
    return (int(match.group(1)), int(match.group(2))) if match else None


def _check_inline_articulation(
    row: LoadedRow,
    target_rel: str,
    target_file_hash: str | None,
    segment_env_by_id: dict[str, TargetEnvironment],
    findings: Findings,
) -> bool:
    """Validate exact in-segment first-use articulation evidence.

    The returned value is true only when the locator and quote are current and
    every required coverage decision is closed strongly enough to count as an
    available explanation.
    """
    data = row.data
    articulation = data.get("inline_articulation")
    if not isinstance(articulation, dict):
        return False
    target = articulation.get("target", {})
    valid = True
    if target.get("path") != target_rel:
        findings.fail(
            "first-use-inline-path",
            "Inline first-use articulation must name its owned target range.",
            **_record_location(row),
            expected=target_rel,
            observed=target.get("path"),
        )
        valid = False
    if target_file_hash is not None and target.get("file_sha256") != target_file_hash:
        findings.fail(
            "first-use-inline-file-hash",
            "Inline first-use target file SHA-256 is stale or false.",
            **_record_location(row),
            expected=target.get("file_sha256"),
            observed=target_file_hash,
        )
        valid = False
    target_id = target.get("target_id")
    local_first_target_id = data.get("local_first_target_id")
    if target_id != local_first_target_id:
        findings.fail(
            "first-use-inline-target",
            "Inline articulation must cite the candidate's exact local-first EESegment.",
            **_record_location(row),
            expected=local_first_target_id,
            observed=target_id,
        )
        valid = False
    environment = segment_env_by_id.get(target_id)
    if environment is None:
        findings.fail(
            "first-use-inline-segment",
            "Inline articulation cites no live EESegment.",
            **_record_location(row),
            target_id=target_id,
        )
        valid = False
    else:
        if target.get("body_sha256") != environment.body_sha256:
            findings.fail(
                "first-use-inline-body-hash",
                "Inline articulation EESegment body SHA-256 is stale or false.",
                **_record_location(row),
                target_id=target_id,
                expected=target.get("body_sha256"),
                observed=environment.body_sha256,
            )
            valid = False
        quote = target.get("exact_quote")
        quote_hash = sha256_bytes(quote.encode("utf-8")) if isinstance(quote, str) else None
        if quote_hash != target.get("exact_quote_sha256"):
            findings.fail(
                "first-use-inline-quote-hash",
                "Inline articulation exact-quote SHA-256 is stale or false.",
                **_record_location(row),
                target_id=target_id,
                expected=target.get("exact_quote_sha256"),
                observed=quote_hash,
            )
            valid = False
        occurrence_count = environment.body.count(quote) if isinstance(quote, str) and quote else 0
        if occurrence_count != 1:
            findings.fail(
                "first-use-inline-exact-quote",
                "Inline articulation exact_quote must occur exactly once in its cited live EESegment body.",
                **_record_location(row),
                target_id=target_id,
                occurrences=occurrence_count,
            )
            valid = False

    coverage = articulation.get("coverage", {})
    required_results = {
        name: coverage.get(name, {}).get("result") if isinstance(coverage.get(name), dict) else None
        for name in ("meaning", "notation", "proof_job", "prerequisites")
    }
    for name in ("meaning", "proof_job"):
        if required_results[name] != "pass":
            if data.get("status") == "pass":
                findings.fail(
                    "first-use-inline-required-coverage",
                    "A passing inline articulation must positively cover meaning and proof job.",
                    **_record_location(row),
                    coverage=name,
                    observed=required_results[name],
                )
            valid = False
    for name in ("notation", "prerequisites"):
        if required_results[name] not in {"pass", "not_applicable"}:
            valid = False
    prerequisites = data.get("prerequisite_concepts", [])
    if prerequisites and required_results["prerequisites"] != "pass":
        if data.get("status") == "pass":
            findings.fail(
                "first-use-inline-prerequisite-coverage",
                "A candidate with named prerequisite concepts must positively cover their needed relation.",
                **_record_location(row),
                observed=required_results["prerequisites"],
            )
        valid = False
    return valid and data.get("status") == "pass"


def _check_gapless_target_ids(environments: list[TargetEnvironment], pattern: re.Pattern[str], findings: Findings, label: str) -> None:
    parsed: list[tuple[int, int, str]] = []
    for environment in environments:
        item = _id_page_ordinal(environment.target_id, pattern)
        if item is None:
            findings.fail("target-id-format", f"{label} has an invalid target ID.", target_id=environment.target_id)
            continue
        page, ordinal = item
        parsed.append((page, ordinal, environment.target_id))
        if environment.page != page:
            findings.fail("target-id-page", f"{label} ID page does not match its NSPage position.", target_id=environment.target_id, encoded_page=page, actual_page=environment.page)
    ids = [item[2] for item in parsed]
    duplicates = sorted(identifier for identifier, count in Counter(ids).items() if count > 1)
    if duplicates:
        findings.fail("duplicate-target-id", f"{label} target IDs are duplicated.", ids=duplicates)
    if [(page, ordinal) for page, ordinal, _ in parsed] != sorted((page, ordinal) for page, ordinal, _ in parsed):
        findings.fail("target-id-order", f"{label} target IDs are not in physical page and visual order.", ids=ids)
    by_page: defaultdict[int, list[int]] = defaultdict(list)
    for page, ordinal, _ in parsed:
        by_page[page].append(ordinal)
    for page, ordinals in sorted(by_page.items()):
        expected = list(range(1, len(ordinals) + 1))
        if ordinals != expected:
            findings.fail("target-id-gap", f"{label} ordinals are not gapless on a page.", page=page, observed=ordinals, expected=expected)


def _range_bounds(range_value: str) -> tuple[int, int]:
    match = RANGE_RE.fullmatch(range_value)
    if match is None:
        raise ValueError("range must have the form ppAAA-BBB")
    first, last = int(match.group(1)), int(match.group(2))
    if first > last:
        raise ValueError("range start exceeds range end")
    return first, last


def audit_range(range_value: str, root: Path | str = ROOT) -> tuple[dict[str, Any], dict[str, Any]]:
    root = Path(root).resolve()
    findings = Findings()
    try:
        first, last = _range_bounds(range_value)
    except ValueError as exc:
        findings.fail("range-syntax", str(exc), range=range_value)
        report = {"schema": "navier-stokes-everyday-range-audit/v1", "range": range_value, "status": "fail", "counts": {}, "pending": findings.pending, "issues": findings.issues}
        return report, {"records": {}, "target_ids": set(), "addition_ids": set()}
    if range_value not in EXPECTED_RANGES:
        findings.fail("range-ownership", "Range is not one of the faithful-edition production ranges.", range=range_value)

    schemas = load_schemas(root, findings)
    accepted_canon_ids = load_canon_ids(root, findings)
    source_rel = f"reconstruction/sections/{range_value}.tex"
    target_rel = f"everyday/sections/{range_value}.tex"
    source_path = root / source_rel
    target_path = root / target_rel
    evidence_dir = root / "evidence" / "translation" / range_value
    report_path = evidence_dir / "REPORT.md"
    report_snapshot: str | None = None

    source_raw = b""
    source_text = ""
    source_markers: list[MathMarker] = []
    source_page_positions: list[tuple[int, int]] = []
    source_prose_lines: list[int] = []
    if not source_path.is_file():
        findings.fail("source-missing", "Faithful source range is missing.", path=source_path.as_posix())
    else:
        try:
            source_raw, source_text = read_utf8(source_path)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            findings.fail("source-encoding", "Faithful source range is not strict UTF-8.", path=source_path.as_posix(), detail=str(exc))
        else:
            source_masked = mask_tex_comments(source_text)
            source_page_positions = page_markers(source_masked)
            observed_pages = [page for _, page in source_page_positions]
            expected_pages = list(range(first, last + 1))
            if observed_pages != expected_pages:
                findings.fail("source-page-order", "Faithful source NSPage markers do not match the owned range.", path=source_path.as_posix(), expected=expected_pages, observed=observed_pages)
            source_markers = parse_math_markers(source_text, findings, source_path)
            for display_start, display_end in _all_display_ranges(source_masked):
                if not any(marker.macro == "NSFormula" and marker.start < display_start and marker.end >= display_end for marker in source_markers):
                    findings.fail("source-unmarked-display", "Faithful source contains a display not bound to one NSFormula marker.", path=source_path.as_posix(), line=source_text.count("\n", 0, display_start) + 1)
            source_prose_lines = [item["line"] for item in find_unwrapped_prose(source_text, [])]

    target_raw = b""
    target_text = ""
    target_markers: list[MathMarker] = []
    segment_envs: list[TargetEnvironment] = []
    addition_envs: list[TargetEnvironment] = []
    target_page_positions: list[tuple[int, int]] = []
    teaching_display_hashes: list[str] = []
    if not target_path.is_file():
        findings.defer("target-missing", "Everyday English target range has not been created.", path=target_path.as_posix())
    else:
        try:
            target_raw, target_text = read_utf8(target_path)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            findings.fail("target-encoding", "Target range is not strict UTF-8.", path=target_path.as_posix(), detail=str(exc))
        else:
            target_masked = mask_tex_comments(target_text)
            target_page_positions = page_markers(target_masked)
            observed_pages = [page for _, page in target_page_positions]
            expected_pages = list(range(first, last + 1))
            source_pages = [page for _, page in source_page_positions]
            if observed_pages != expected_pages or (source_pages and observed_pages != source_pages):
                findings.fail("target-page-order", "Target NSPage markers must exactly match source and range order.", path=target_path.as_posix(), expected=expected_pages, source=source_pages, observed=observed_pages)
            segment_envs = parse_target_environments(target_text, "EESegment", target_page_positions, findings, target_path)
            addition_envs = parse_target_environments(target_text, "EEAddition", target_page_positions, findings, target_path)
            _check_gapless_target_ids(segment_envs, TARGET_ID_RE, findings, "EESegment")
            _check_gapless_target_ids(addition_envs, ADDITION_ID_RE, findings, "EEAddition")
            all_envs = sorted(segment_envs + addition_envs, key=lambda item: item.start)
            for previous, current in zip(all_envs, all_envs[1:]):
                if current.start < previous.end:
                    findings.fail("target-environment-overlap", "EESegment and EEAddition environments may not overlap or nest.", first_id=previous.target_id, second_id=current.target_id)
            for environment in all_envs:
                if not body_has_prose(environment.body):
                    findings.fail("empty-prose-environment", "A target prose environment contains no detectable prose.", target_id=environment.target_id)
            unwrapped = find_unwrapped_prose(target_text, all_envs)
            if unwrapped:
                findings.fail("unwrapped-target-prose", "Detectable target prose remains outside EESegment/EEAddition.", path=target_path.as_posix(), occurrences=unwrapped[:20], omitted=max(0, len(unwrapped) - 20))
            target_markers = parse_math_markers(target_text, findings, target_path)
            for display_start, display_end in _all_display_ranges(target_masked):
                marked = any(marker.macro == "NSFormula" and marker.start < display_start and marker.end >= display_end for marker in target_markers)
                teaching = any(environment.start <= display_start and display_end <= environment.end for environment in addition_envs)
                if not marked and not teaching:
                    findings.fail("target-unmarked-display", "A target display is neither the exact display following an NSFormula marker nor teaching inside EEAddition.", path=target_path.as_posix(), line=target_text.count("\n", 0, display_start) + 1)
                elif teaching and not marked:
                    teaching_display_hashes.append(sha256_bytes(target_text[display_start:display_end].encode("utf-8")))
            unmarked_inline_lines = sorted({
                target_text.count("\n", 0, match.start()) + 1
                for match in re.finditer(r"(?<!\\)\$|\\\(", target_masked)
                if not any(environment.start <= match.start() < environment.end for environment in addition_envs)
            })
            if unmarked_inline_lines:
                findings.fail("target-unmarked-inline-math", "Raw target inline mathematics is not a preserved NSi marker or teaching inside EEAddition.", path=target_path.as_posix(), lines=unmarked_inline_lines[:100], omitted=max(0, len(unmarked_inline_lines) - 100))

    if source_text and target_text:
        source_ids = [(item.macro, item.marker_id) for item in source_markers]
        target_ids = [(item.macro, item.marker_id) for item in target_markers]
        if source_ids != target_ids:
            findings.fail("ns-marker-order", "Target NS-F marker kind, ID, multiplicity, or order differs from source.", expected=source_ids, observed=target_ids)
        for label, marker_list in (("source", source_markers), ("target", target_markers)):
            duplicates = sorted(identifier for identifier, count in Counter(item.marker_id for item in marker_list).items() if count > 1)
            if duplicates:
                findings.fail("duplicate-ns-marker", "NS-F marker IDs must occur exactly once.", file_kind=label, ids=duplicates)
        source_by_id = {item.marker_id: item for item in source_markers}
        target_by_id = {item.marker_id: item for item in target_markers}
        for marker_id in sorted(source_by_id.keys() & target_by_id.keys()):
            source_marker = source_by_id[marker_id]
            target_marker = target_by_id[marker_id]
            if source_marker.macro != target_marker.macro:
                continue
            if source_marker.macro == "NSi" and source_marker.math_text != target_marker.math_text:
                findings.fail("inline-math-identity", "NSi mathematical argument is not byte-identical to source.", marker_id=marker_id, source_sha256=source_marker.math_sha256, target_sha256=target_marker.math_sha256)
            if source_marker.macro == "NSFormula":
                if (source_marker.marker_kind, source_marker.printed_number) != (target_marker.marker_kind, target_marker.printed_number):
                    findings.fail("display-marker-arguments", "NSFormula non-ID arguments differ from source.", marker_id=marker_id, source=[source_marker.marker_kind, source_marker.printed_number], target=[target_marker.marker_kind, target_marker.printed_number])
                if source_marker.math_text != target_marker.math_text:
                    findings.fail("display-math-identity", "Marked display environment is not byte-identical to source.", marker_id=marker_id, source_sha256=source_marker.math_sha256, target_sha256=target_marker.math_sha256)

    if not report_path.is_file():
        findings.defer("report-missing", "Range REPORT.md has not been created.", path=report_path.as_posix())
    else:
        report_hash_before = sha256_path(report_path)
        report_snapshot = report_hash_before
        try:
            _, report_text = read_utf8(report_path)
        except (OSError, UnicodeDecodeError, ValueError) as exc:
            findings.fail("report-encoding", "Range REPORT.md is not strict UTF-8.", path=report_path.as_posix(), detail=str(exc))
        else:
            if not report_text.strip() or range_value not in report_text:
                findings.fail("report-content", "Range REPORT.md must be nonempty and identify its exact range.", path=report_path.as_posix(), range=range_value)
        if not report_path.is_file() or sha256_path(report_path) != report_hash_before:
            findings.fail("report-changed-during-audit", "Range REPORT.md changed while the audit was reading it.", path=report_path.as_posix())

    rows_by_ledger: dict[str, list[LoadedRow]] = {}
    ledger_present: dict[str, bool] = {}
    ledger_snapshots: dict[str, str] = {}
    for ledger_name, (_, _) in LEDGERS.items():
        path = evidence_dir / ledger_name
        ledger_present[ledger_name] = path.is_file()
        if not path.is_file():
            findings.defer("ledger-missing", "Required range ledger has not been created.", path=path.as_posix())
            rows_by_ledger[ledger_name] = []
            continue
        schema = schemas.get(ledger_name)
        if schema is None:
            rows_by_ledger[ledger_name] = []
            continue
        ledger_hash_before = sha256_path(path)
        rows_by_ledger[ledger_name] = load_jsonl(path, schema, findings)
        ledger_hash_after = sha256_path(path) if path.is_file() else None
        if ledger_hash_after != ledger_hash_before:
            findings.fail("ledger-changed-during-audit", "Range ledger changed while the audit was reading it.", path=path.as_posix())
        elif ledger_hash_after is not None:
            ledger_snapshots[path.as_posix()] = ledger_hash_after

    all_rows = [row for rows in rows_by_ledger.values() for row in rows]
    valid_rows = [row for row in all_rows if row.schema_valid]
    record_ids = [row.data.get("id") for row in valid_rows if isinstance(row.data.get("id"), str)]
    duplicates = sorted(identifier for identifier, count in Counter(record_ids).items() if count > 1)
    if duplicates:
        findings.fail("duplicate-record-id", "Range record IDs must be unique across all ledgers.", ids=duplicates)
    for row in valid_rows:
        _check_ordered_pages(row, first, last, findings)
        _check_record_status(row, findings)

    segment_rows = _live(rows_by_ledger["SEGMENTS.jsonl"])
    change_rows = _live(rows_by_ledger["CHANGES.jsonl"])
    addition_rows = _live(rows_by_ledger["ADDITIONS.jsonl"])
    mathematics_rows = _live(rows_by_ledger["MATHEMATICS.jsonl"])
    first_use_rows = _live(rows_by_ledger["FIRST_USE_CANDIDATES.jsonl"])

    for row in segment_rows:
        for index, choice in enumerate(row.data.get("consequential_choices", [])):
            if isinstance(choice, dict):
                _check_canon_support(choice, row, accepted_canon_ids, findings, f"consequential_choices[{index}]")
    for row in change_rows:
        _check_canon_support(row.data, row, accepted_canon_ids, findings, "change")

    source_file_hash = sha256_bytes(source_raw) if source_raw else None
    target_file_hash = sha256_bytes(target_raw) if target_raw else None
    source_line_page_map = line_pages(source_text) if source_text else []
    segment_env_by_id = {environment.target_id: environment for environment in segment_envs}
    addition_env_by_id = {environment.target_id: environment for environment in addition_envs}
    segment_records_by_target: defaultdict[str, list[LoadedRow]] = defaultdict(list)
    addition_records_by_target: defaultdict[str, list[LoadedRow]] = defaultdict(list)

    source_starts_in_target_order: list[int] = []
    source_span_records: list[tuple[int, int, LoadedRow]] = []
    for row in segment_rows:
        data = row.data
        source = data["source"]
        target = data["target"]
        target_id = target["target_id"]
        segment_records_by_target[target_id].append(row)
        if source.get("path") != source_rel:
            findings.fail("segment-source-path", "Segment source path must name its owned faithful range.", **_record_location(row), expected=source_rel, observed=source.get("path"))
        if source_file_hash is not None and source.get("file_sha256") != source_file_hash:
            findings.fail("segment-source-file-hash", "Segment faithful-source file hash is stale or false.", **_record_location(row), expected=source.get("file_sha256"), observed=source_file_hash)
        span = _check_span(source_raw, source_text, source, row, findings, "source") if source_raw else None
        if span:
            start, end = span
            source_starts_in_target_order.append(start)
            source_span_records.append((start, end, row))
            touched_pages = sorted({page for page in source_line_page_map[start - 1:end] if page is not None})
            if touched_pages != data.get("pdf_pages"):
                findings.fail("segment-source-pages", "Segment pdf_pages do not equal the pages touched by its source span.", **_record_location(row), expected=touched_pages, observed=data.get("pdf_pages"))
        if target.get("path") != target_rel:
            findings.fail("segment-target-path", "Segment target path must name its owned target range.", **_record_location(row), expected=target_rel, observed=target.get("path"))
        if target_file_hash is not None and target.get("file_sha256") != target_file_hash:
            findings.fail("segment-target-file-hash", "Segment target file hash is stale or false.", **_record_location(row), expected=target.get("file_sha256"), observed=target_file_hash)
        environment = segment_env_by_id.get(target_id)
        if environment is None:
            findings.fail("segment-record-without-target", "Live segment record names no live EESegment.", **_record_location(row), target_id=target_id)
        else:
            if target.get("body_sha256") != environment.body_sha256:
                findings.fail("segment-target-body-hash", "EESegment body hash is stale or false.", **_record_location(row), target_id=target_id, expected=target.get("body_sha256"), observed=environment.body_sha256)
            if environment.page not in data.get("pdf_pages", []):
                findings.fail("segment-target-page", "EESegment physical page is absent from record pdf_pages.", **_record_location(row), target_id=target_id, target_page=environment.page)
        if target_id not in data.get("relation", {}).get("linked_target_ids", []):
            findings.fail("segment-relation-link", "Segment relation must include its own target ID.", **_record_location(row), target_id=target_id)
        relation = data.get("relation", {})
        if relation.get("kind") == "split" and len(relation.get("linked_target_ids", [])) < 2:
            findings.fail("split-relation", "A split relation must name every linked target and therefore at least two.", **_record_location(row))
        if relation.get("kind") == "merged" and len(relation.get("linked_source_ids", [])) < 2:
            findings.fail("merged-relation", "A merged relation must name every linked source and therefore at least two.", **_record_location(row))

    if source_starts_in_target_order != sorted(source_starts_in_target_order):
        findings.fail("segment-source-order", "Live segment source spans move backwards relative to target order.", observed=source_starts_in_target_order)
    if target_text and ledger_present["SEGMENTS.jsonl"]:
        ledger_target_order = [row.data["target"]["target_id"] for row in segment_rows]
        environment_target_order = [environment.target_id for environment in segment_envs]
        if ledger_target_order != environment_target_order:
            findings.fail("segment-ledger-order", "Live segment records must occur in exact EESegment target order.", expected=environment_target_order, observed=ledger_target_order)
        for target_id in segment_env_by_id:
            count = len(segment_records_by_target[target_id])
            if count != 1:
                findings.fail("segment-record-coverage", "Every EESegment needs exactly one live segment record.", target_id=target_id, observed=count)
        uncovered_lines: list[int] = []
        for line_number in source_prose_lines:
            covering = [(start, end, row) for start, end, row in source_span_records if start <= line_number <= end]
            if not covering:
                uncovered_lines.append(line_number)
            elif len(covering) > 1 and not all(item[2].data.get("relation", {}).get("kind") == "split" for item in covering):
                findings.fail(
                    "source-prose-overlap",
                    "A detectable source-prose line is covered more than once without every covering record declaring a split.",
                    line=line_number,
                    record_ids=[item[2].data.get("id") for item in covering],
                )
        if uncovered_lines:
            findings.defer(
                "source-prose-uncovered",
                "Detectable source-prose lines are not yet bound to any live EESegment record.",
                path=source_path.as_posix(),
                lines=uncovered_lines[:100],
                omitted=max(0, len(uncovered_lines) - 100),
            )

    all_target_ids_local = set(segment_env_by_id) | set(addition_env_by_id)
    for row in addition_rows:
        data = row.data
        target = data["target"]
        target_id = target["target_id"]
        addition_records_by_target[target_id].append(row)
        if target.get("path") != target_rel:
            findings.fail("addition-target-path", "Addition target path must name its owned target range.", **_record_location(row), expected=target_rel, observed=target.get("path"))
        if target_file_hash is not None and target.get("file_sha256") != target_file_hash:
            findings.fail("addition-target-file-hash", "Addition target file hash is stale or false.", **_record_location(row), expected=target.get("file_sha256"), observed=target_file_hash)
        environment = addition_env_by_id.get(target_id)
        if environment is None:
            findings.fail("addition-record-without-target", "Live addition record names no live EEAddition.", **_record_location(row), target_id=target_id)
        else:
            if target.get("body_sha256") != environment.body_sha256:
                findings.fail("addition-target-body-hash", "EEAddition body hash is stale or false.", **_record_location(row), target_id=target_id, expected=target.get("body_sha256"), observed=environment.body_sha256)
            if target.get("title") != environment.title:
                findings.fail("addition-title", "EEAddition title differs from its evidence record.", **_record_location(row), target_id=target_id, expected=target.get("title"), observed=environment.title)
            if environment.page not in data.get("pdf_pages", []):
                findings.fail("addition-target-page", "EEAddition physical page is absent from record pdf_pages.", **_record_location(row), target_id=target_id, target_page=environment.page)
        placement = data.get("placement", {})
        anchors = [placement.get("after_target_id"), placement.get("before_target_id")]
        if all(anchor is None for anchor in anchors):
            findings.fail("addition-placement", "Teaching addition needs an exact before or after placement anchor.", **_record_location(row))
        for anchor in anchors:
            if anchor is not None and anchor not in all_target_ids_local:
                findings.fail("addition-placement-anchor", "Teaching-addition placement anchor is not a live local target.", **_record_location(row), anchor=anchor)
        target_environment_by_id = segment_env_by_id | addition_env_by_id
        after_environment = target_environment_by_id.get(placement.get("after_target_id"))
        before_environment = target_environment_by_id.get(placement.get("before_target_id"))
        if environment is not None and after_environment is not None and after_environment.end > environment.start:
            findings.fail("addition-after-order", "EEAddition is not physically after its recorded after_target_id.", **_record_location(row), target_id=target_id, anchor=after_environment.target_id)
        if environment is not None and before_environment is not None and environment.end > before_environment.start:
            findings.fail("addition-before-order", "EEAddition is not physically before its recorded before_target_id.", **_record_location(row), target_id=target_id, anchor=before_environment.target_id)
        dependency_ids = [item.get("dependency_id") for item in data.get("source_dependencies", [])]
        if len(dependency_ids) != len(set(dependency_ids)):
            findings.fail("addition-dependency-id", "Teaching-addition dependency IDs must be unique.", **_record_location(row))
        for index, dependency in enumerate(data.get("source_dependencies", [])):
            require_hash = data.get("status") == "pass"
            _check_file_authority(root, dependency.get("path"), dependency.get("file_sha256"), row, findings, f"source_dependencies[{index}]", require_hash)
        claim_ids = [claim.get("claim_id") for claim in data.get("mathematical_claim_map", [])]
        if len(claim_ids) != len(set(claim_ids)):
            findings.fail("addition-claim-id", "Teaching-addition claim IDs must be unique.", **_record_location(row))
        for claim in data.get("mathematical_claim_map", []):
            missing = sorted(set(claim.get("source_dependency_ids", [])) - set(dependency_ids))
            if missing:
                findings.fail("addition-claim-dependency", "Teaching claim cites an absent dependency.", **_record_location(row), claim_id=claim.get("claim_id"), missing=missing)
        proved_claims = {claim_id for proof in data.get("proof_records", []) for claim_id in proof.get("claim_ids", [])}
        if set(claim_ids) != proved_claims:
            findings.fail("addition-proof-coverage", "Proof records must cover exactly every teaching claim.", **_record_location(row), claims=sorted(set(claim_ids)), proved=sorted(proved_claims))
        if data.get("defines_concept") and (not data.get("accepting_examples") or not data.get("rejecting_examples")):
            findings.fail("addition-definition-examples", "A concept-defining addition needs both accepting and rejecting examples.", **_record_location(row))
    if target_text and ledger_present["ADDITIONS.jsonl"]:
        ledger_addition_order = [row.data["target"]["target_id"] for row in addition_rows]
        environment_addition_order = [environment.target_id for environment in addition_envs]
        if ledger_addition_order != environment_addition_order:
            findings.fail("addition-ledger-order", "Live addition records must occur in exact EEAddition target order.", expected=environment_addition_order, observed=ledger_addition_order)
        for target_id in addition_env_by_id:
            count = len(addition_records_by_target[target_id])
            if count != 1:
                findings.fail("addition-record-coverage", "Every EEAddition needs exactly one live addition record.", target_id=target_id, observed=count)

    live_segment_ids = set(segment_records_by_target)
    for row in change_rows:
        referenced_targets = row.data.get("target_segment_ids", [])
        missing = sorted(set(referenced_targets) - live_segment_ids)
        if missing:
            findings.fail("change-target-reference", "Change record cites a target without a live segment record.", **_record_location(row), missing=missing)
        linked_sources = {
            source_id
            for target_id in referenced_targets
            for segment_row in segment_records_by_target.get(target_id, [])
            for source_id in segment_row.data.get("relation", {}).get("linked_source_ids", [])
        }
        unknown_sources = sorted(set(row.data.get("source_segment_ids", [])) - linked_sources)
        if unknown_sources:
            findings.fail("change-source-reference", "Change record source IDs are not linked by its affected segment records.", **_record_location(row), missing=unknown_sources)
        linked_pages = {
            page
            for target_id in referenced_targets
            for segment_row in segment_records_by_target.get(target_id, [])
            for page in segment_row.data.get("pdf_pages", [])
        }
        if not set(row.data.get("pdf_pages", [])).issubset(linked_pages):
            findings.fail("change-page-reference", "Change record cites pages outside its affected segment records.", **_record_location(row), allowed=sorted(linked_pages), observed=row.data.get("pdf_pages"))
    if ledger_present["CHANGES.jsonl"] and ledger_present["SEGMENTS.jsonl"]:
        changed_ids = {target_id for row in change_rows for target_id in row.data.get("target_segment_ids", [])}
        for target_id in sorted(live_segment_ids - changed_ids):
            findings.fail("change-coverage", "Every live target segment needs at least one live change record, including retention.", target_id=target_id)

    math_target_coverage: Counter[str] = Counter()
    math_formula_entries: defaultdict[str, list[tuple[LoadedRow, dict[str, Any]]]] = defaultdict(list)
    teaching_formula_hashes: list[str] = []
    for row in mathematics_rows:
        data = row.data
        referenced_targets = data.get("target_ids", [])
        missing_targets = sorted(set(referenced_targets) - all_target_ids_local)
        if missing_targets:
            findings.fail("mathematics-target-reference", "Mathematics record cites no live local target.", **_record_location(row), missing=missing_targets)
        math_target_coverage.update(referenced_targets)
        linked_pages = {
            page
            for target_id in referenced_targets
            for target_row in segment_records_by_target.get(target_id, []) + addition_records_by_target.get(target_id, [])
            for page in target_row.data.get("pdf_pages", [])
        }
        if not set(data.get("pdf_pages", [])).issubset(linked_pages):
            findings.fail("mathematics-page-reference", "Mathematics record cites pages outside its linked targets.", **_record_location(row), allowed=sorted(linked_pages), observed=data.get("pdf_pages"))
        authority_ids = [item.get("authority_id") for item in data.get("source_authorities", [])]
        if len(authority_ids) != len(set(authority_ids)):
            findings.fail("mathematics-authority-id", "Mathematics authority IDs must be unique within a record.", **_record_location(row))
        for index, authority in enumerate(data.get("source_authorities", [])):
            require_hash = data.get("status") == "pass"
            _check_file_authority(root, authority.get("path"), authority.get("file_sha256"), row, findings, f"source_authorities[{index}]", require_hash)
        authority_set = set(authority_ids)
        for collection_name in ("claims", "definitions", "dependencies"):
            for item in data.get(collection_name, []):
                missing = sorted(set(item.get("source_authority_ids", [])) - authority_set)
                if missing:
                    findings.fail("mathematics-authority-reference", "Mathematical item cites an absent source authority.", **_record_location(row), collection=collection_name, missing=missing)
        formulas = data.get("formulas", [])
        listed_marker_ids = data.get("formula_marker_identity", {}).get("marker_ids", [])
        formula_marker_ids = [formula.get("marker_id") for formula in formulas]
        if listed_marker_ids != formula_marker_ids:
            findings.fail("mathematics-marker-list", "formula_marker_identity.marker_ids must exactly equal formulas order.", **_record_location(row), expected=formula_marker_ids, observed=listed_marker_ids)
        if any(isinstance(marker_id, str) and marker_id.startswith("NS-F-") for marker_id in formula_marker_ids) and data.get("formula_marker_identity", {}).get("result") != "pass":
            findings.fail("mathematics-marker-result", "A mathematics record containing source NS-F markers must pass formula-marker identity.", **_record_location(row), observed=data.get("formula_marker_identity", {}).get("result"))
        formula_ids = [formula.get("formula_id") for formula in formulas]
        if len(formula_ids) != len(set(formula_ids)):
            findings.fail("mathematics-formula-id", "Formula record IDs must be unique within a mathematics record.", **_record_location(row))
        for formula in formulas:
            marker_id = formula.get("marker_id")
            if isinstance(marker_id, str) and marker_id.startswith("NS-F-"):
                math_formula_entries[marker_id].append((row, formula))
            elif formula.get("kind") == "teaching" and isinstance(formula.get("target_tex_sha256"), str):
                teaching_formula_hashes.append(formula["target_tex_sha256"])

    if ledger_present["MATHEMATICS.jsonl"]:
        for target_id in sorted(all_target_ids_local):
            if math_target_coverage[target_id] < 1:
                findings.fail("mathematics-coverage", "Every target segment and teaching addition needs a live mathematics record.", target_id=target_id)
        source_by_id = {marker.marker_id: marker for marker in source_markers}
        target_by_id = {marker.marker_id: marker for marker in target_markers}
        for marker_id in sorted(source_by_id):
            entries = math_formula_entries.get(marker_id, [])
            if len(entries) != 1:
                findings.fail("mathematics-formula-coverage", "Every source NS-F marker needs exactly one live formula evidence entry.", marker_id=marker_id, observed=len(entries))
                continue
            row, formula = entries[0]
            source_marker = source_by_id[marker_id]
            target_marker = target_by_id.get(marker_id)
            expected_kind = "inline" if source_marker.macro == "NSi" else "display"
            if formula.get("kind") != expected_kind:
                findings.fail("mathematics-formula-kind", "Formula evidence kind disagrees with its marker macro.", **_record_location(row), marker_id=marker_id, expected=expected_kind, observed=formula.get("kind"))
            if formula.get("source_tex_sha256") != source_marker.math_sha256:
                findings.fail("mathematics-source-formula-hash", "Formula evidence source hash is stale or false.", **_record_location(row), marker_id=marker_id, expected=source_marker.math_sha256, observed=formula.get("source_tex_sha256"))
            if target_marker is not None and formula.get("target_tex_sha256") != target_marker.math_sha256:
                findings.fail("mathematics-target-formula-hash", "Formula evidence target hash is stale or false.", **_record_location(row), marker_id=marker_id, expected=target_marker.math_sha256, observed=formula.get("target_tex_sha256"))
            if formula.get("identity_result") != "pass":
                if formula.get("identity_result") == "pending":
                    findings.defer("mathematics-formula-pending", "Formula identity evidence is pending.", **_record_location(row), marker_id=marker_id)
                else:
                    findings.fail("mathematics-formula-result", "Source formula identity is not passed.", **_record_location(row), marker_id=marker_id, observed=formula.get("identity_result"))
        extra = sorted(set(math_formula_entries) - set(source_by_id))
        if extra:
            findings.fail("mathematics-extra-ns-marker", "Mathematics ledger cites NS-F markers absent from the owned source range.", marker_ids=extra)
        missing_teaching_displays = Counter(teaching_display_hashes) - Counter(teaching_formula_hashes)
        if missing_teaching_displays:
            findings.fail("mathematics-teaching-display-coverage", "Every unmarked display inside EEAddition needs a live teaching-formula entry with its exact target hash.", missing_hash_counts=dict(sorted(missing_teaching_displays.items())))

    valid_inline_articulation_record_ids: set[str] = set()
    for row in first_use_rows:
        data = row.data
        locator = data.get("source_locator", {})
        if data.get("pdf_pages") != [locator.get("pdf_page")]:
            findings.fail("first-use-record-pages", "First-use record pdf_pages must be the singleton exact source-locator page.", **_record_location(row), expected=[locator.get("pdf_page")], observed=data.get("pdf_pages"))
        if locator.get("path") != source_rel:
            findings.fail("first-use-source-path", "First-use locator must name its owned faithful range.", **_record_location(row), expected=source_rel, observed=locator.get("path"))
        if source_file_hash is not None and locator.get("file_sha256") != source_file_hash:
            findings.fail("first-use-source-file-hash", "First-use source file hash is stale or false.", **_record_location(row), expected=locator.get("file_sha256"), observed=source_file_hash)
        span = _check_span(source_raw, source_text, locator, row, findings, "source_locator") if source_raw else None
        if span:
            start, end = span
            selected = exact_line_span(source_raw, start, end).decode("utf-8")
            if locator.get("exact_text") not in selected:
                findings.fail("first-use-exact-text", "First-use exact_text does not occur in its bound source span.", **_record_location(row))
            pages = sorted({page for page in source_line_page_map[start - 1:end] if page is not None})
            if locator.get("pdf_page") not in pages:
                findings.fail("first-use-source-page", "First-use locator page does not match its source span.", **_record_location(row), source_pages=pages, observed=locator.get("pdf_page"))
        local_target_id = data.get("local_first_target_id")
        if local_target_id not in segment_env_by_id:
            findings.fail("first-use-target", "First-use candidate cites no live local EESegment.", **_record_location(row), target_id=local_target_id)
        inline_valid = _check_inline_articulation(
            row,
            target_rel,
            target_file_hash,
            segment_env_by_id,
            findings,
        )
        if inline_valid and isinstance(data.get("id"), str):
            valid_inline_articulation_record_ids.add(data["id"])
        proposed = data.get("proposed_addition_id")
        if proposed is not None and proposed not in addition_env_by_id:
            if data.get("status") == "pass":
                findings.fail("first-use-addition", "Passing first-use candidate cites no live proposed addition.", **_record_location(row), addition_id=proposed)
            else:
                findings.defer("first-use-addition-pending", "Proposed first-use addition is not yet live.", **_record_location(row), addition_id=proposed)
        earlier = data.get("earlier_occurrence_check", {}).get("result")
        global_status = data.get("global_resolution", {}).get("status")
        resolved_by = data.get("global_resolution", {}).get("resolved_by")
        if earlier == "unresolved" or global_status == "unresolved":
            if data.get("status") == "pass":
                findings.fail("first-use-pass-unresolved", "A pass first-use record may not leave manuscript order or global resolution unresolved.", **_record_location(row))
            else:
                findings.defer("first-use-unresolved", "Root has not completed global first-use resolution.", **_record_location(row))
        if global_status in {"confirmed_first", "not_first"} and not (isinstance(resolved_by, str) and resolved_by.strip()):
            findings.fail("first-use-resolver", "A resolved global first-use result must identify the root resolver or receipt.", **_record_location(row))
        if global_status == "confirmed_first" and earlier != "no":
            findings.fail("first-use-confirmed-earlier", "A globally confirmed first use must have an earlier-occurrence result of 'no'.", **_record_location(row), observed=earlier)
        if global_status == "not_first" and earlier != "yes":
            findings.fail("first-use-not-first-earlier", "A non-first candidate must identify an earlier occurrence.", **_record_location(row), observed=earlier)
        if global_status == "confirmed_first" and proposed is None and not inline_valid:
            findings.fail(
                "first-use-explanation-missing",
                "A globally confirmed first use needs either a live teaching addition or exact passing inline-articulation evidence.",
                **_record_location(row),
            )
        elif global_status == "unresolved" and proposed is None and data.get("inline_articulation") is None:
            findings.defer(
                "first-use-explanation-pending",
                "The unresolved first-use candidate has not yet identified a teaching addition or exact inline articulation.",
                **_record_location(row),
            )

    if source_file_hash is not None and (not source_path.is_file() or sha256_path(source_path) != source_file_hash):
        findings.fail("source-changed-during-audit", "Faithful source bytes changed while the range audit was running.", path=source_path.as_posix())
    if target_file_hash is not None and (not target_path.is_file() or sha256_path(target_path) != target_file_hash):
        findings.fail("target-changed-during-audit", "Target bytes changed while the range audit was running.", path=target_path.as_posix())

    status = "fail" if findings.issues else ("pending" if findings.pending else "pass")
    counts = {
        "source_pages": len(source_page_positions),
        "target_pages": len(target_page_positions),
        "source_ns_markers": len(source_markers),
        "target_ns_markers": len(target_markers),
        "ee_segments": len(segment_envs),
        "ee_additions": len(addition_envs),
        "segment_records_live": len(segment_rows),
        "change_records_live": len(change_rows),
        "addition_records_live": len(addition_rows),
        "mathematics_records_live": len(mathematics_rows),
        "first_use_candidates_live": len(first_use_rows),
    }
    report = {
        "schema": "navier-stokes-everyday-range-audit/v1",
        "range": range_value,
        "status": status,
        "counts": counts,
        "pending": findings.pending,
        "issues": findings.issues,
    }
    context = {
        "records": rows_by_ledger,
        "target_ids": set(segment_env_by_id),
        "addition_ids": set(addition_env_by_id),
        "target_order": [environment.target_id for environment in sorted(segment_envs, key=lambda item: item.start)],
        "target_environments": segment_env_by_id,
        "target_path": target_rel,
        "target_file_sha256": target_file_hash,
        "valid_inline_articulation_record_ids": valid_inline_articulation_record_ids,
        "file_snapshots": {
            **ledger_snapshots,
            **({source_path.as_posix(): source_file_hash} if source_file_hash is not None else {}),
            **({target_path.as_posix(): target_file_hash} if target_file_hash is not None else {}),
            **({report_path.as_posix(): report_snapshot} if report_snapshot is not None else {}),
        },
    }
    return report, context


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("range", help="owned range, for example pp001-006")
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    report, _ = audit_range(args.range, args.root)
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"pass": 0, "fail": 1, "pending": 2}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
