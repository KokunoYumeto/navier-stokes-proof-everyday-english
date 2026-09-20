#!/usr/bin/env python3
"""Run every Everyday English range audit and apply cross-range gates.

Exit status 0 means pass, 1 means fail, and 2 means pending.  A pass is
possible only when every faithful-edition range passes and global first-use,
ID, reference, and supersession checks also close.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from audit_everyday_range import EXPECTED_RANGES, ROOT, LoadedRow, audit_range, sha256_bytes, sha256_path


TARGET_ORDER_RE = re.compile(r"^EE-(?:TGT|ADD)-P([0-9]{3})-([0-9]{3})$")


def _live(rows: Iterable[LoadedRow]) -> list[LoadedRow]:
    return [row for row in rows if row.schema_valid and row.data.get("status") != "superseded"]


def _record_location(row: LoadedRow, range_value: str) -> dict[str, Any]:
    return {
        "range": range_value,
        "path": row.path.as_posix(),
        "line": row.line,
        "record_id": row.data.get("id"),
    }


def _target_order(identifier: str) -> tuple[int, int, int]:
    match = TARGET_ORDER_RE.fullmatch(identifier)
    if match is None:
        return (10**9, 10**9, 10**9)
    kind = 0 if identifier.startswith("EE-TGT-") else 1
    return int(match.group(1)), int(match.group(2)), kind


def audit_all(root: Path | str = ROOT, ranges: Iterable[str] = EXPECTED_RANGES) -> dict[str, Any]:
    root = Path(root).resolve()
    ranges = tuple(ranges)
    range_reports: list[dict[str, Any]] = []
    contexts: dict[str, dict[str, Any]] = {}
    global_issues: list[dict[str, Any]] = []
    global_pending: list[dict[str, Any]] = []

    if ranges == EXPECTED_RANGES:
        # Fixed enumeration prevents a missing faithful section or target range
        # from disappearing merely because a directory listing omitted it.
        expected_source_names = {f"{range_value}.tex" for range_value in EXPECTED_RANGES}
        source_dir = root / "reconstruction" / "sections"
        observed_source_names = {path.name for path in source_dir.glob("pp[0-9][0-9][0-9]-[0-9][0-9][0-9].tex")} if source_dir.is_dir() else set()
        missing_sources = sorted(expected_source_names - observed_source_names)
        extra_sources = sorted(observed_source_names - expected_source_names)
        if missing_sources:
            global_issues.append({"code": "global-source-ranges-missing", "message": "Faithful-edition source ranges are missing.", "files": missing_sources})
        if extra_sources:
            global_issues.append({"code": "global-source-ranges-extra", "message": "Unexpected faithful range filenames make ownership ambiguous.", "files": extra_sources})

    for range_value in ranges:
        report, context = audit_range(range_value, root)
        range_reports.append(report)
        contexts[range_value] = context

    record_locations: defaultdict[str, list[tuple[str, LoadedRow]]] = defaultdict(list)
    target_locations: defaultdict[str, list[str]] = defaultdict(list)
    addition_locations: defaultdict[str, list[str]] = defaultdict(list)
    all_rows_with_range: list[tuple[str, LoadedRow]] = []
    for range_value in ranges:
        context = contexts[range_value]
        for rows in context["records"].values():
            for row in rows:
                if row.schema_valid:
                    all_rows_with_range.append((range_value, row))
                    identifier = row.data.get("id")
                    if isinstance(identifier, str):
                        record_locations[identifier].append((range_value, row))
        for target_id in context["target_ids"]:
            target_locations[target_id].append(range_value)
        for addition_id in context["addition_ids"]:
            addition_locations[addition_id].append(range_value)

    for identifier, locations in sorted(record_locations.items()):
        if len(locations) > 1:
            global_issues.append({
                "code": "global-duplicate-record-id",
                "message": "Record ID is duplicated across range ledgers.",
                "record_id": identifier,
                "locations": [_record_location(row, range_value) for range_value, row in locations],
            })
    for identifier, locations in sorted(target_locations.items()):
        if len(locations) > 1:
            global_issues.append({"code": "global-duplicate-target-id", "message": "EESegment target ID occurs in more than one range.", "target_id": identifier, "ranges": locations})
    for identifier, locations in sorted(addition_locations.items()):
        if len(locations) > 1:
            global_issues.append({"code": "global-duplicate-addition-id", "message": "EEAddition target ID occurs in more than one range.", "target_id": identifier, "ranges": locations})

    record_by_id = {identifier: locations[0][1] for identifier, locations in record_locations.items() if len(locations) == 1}
    for range_value, row in all_rows_with_range:
        supersession = row.data.get("supersession", {})
        for relation, reverse in (("supersedes", "superseded_by"), ("superseded_by", "supersedes")):
            for linked_id in supersession.get(relation, []):
                linked = record_by_id.get(linked_id)
                if linked is None:
                    global_issues.append({"code": "global-supersession-reference", "message": "Supersession link cites no unique record.", **_record_location(row, range_value), "relation": relation, "linked_id": linked_id})
                    continue
                if row.data.get("id") not in linked.data.get("supersession", {}).get(reverse, []):
                    global_issues.append({"code": "global-supersession-reciprocity", "message": "Supersession links must be reciprocal.", **_record_location(row, range_value), "relation": relation, "linked_id": linked_id})

    all_target_ids = set(target_locations) | set(addition_locations)
    all_segment_ids = set(target_locations)
    all_addition_ids = set(addition_locations)
    first_use_rows: list[tuple[str, LoadedRow]] = []
    segment_rows: list[tuple[str, LoadedRow]] = []
    for range_value in ranges:
        first_use_rows.extend((range_value, row) for row in _live(contexts[range_value]["records"].get("FIRST_USE_CANDIDATES.jsonl", [])))
        segment_rows.extend((range_value, row) for row in _live(contexts[range_value]["records"].get("SEGMENTS.jsonl", [])))

    first_use_record_ids = {row.data.get("id") for _, row in first_use_rows}
    valid_inline_articulation_ids: set[str] = set()
    for range_value, row in first_use_rows:
        data = row.data
        articulation = data.get("inline_articulation")
        if not isinstance(articulation, dict):
            continue
        target = articulation.get("target", {})
        target_id = target.get("target_id")
        valid = True
        if target_id != data.get("local_first_target_id"):
            global_issues.append({
                "code": "global-first-use-inline-target",
                "message": "Inline articulation must cite the candidate's exact local-first EESegment.",
                **_record_location(row, range_value),
                "expected": data.get("local_first_target_id"),
                "observed": target_id,
            })
            valid = False
        owners = target_locations.get(target_id, [])
        if owners != [range_value]:
            global_issues.append({
                "code": "global-first-use-inline-segment",
                "message": "Inline articulation must cite one live EESegment in its own range.",
                **_record_location(row, range_value),
                "target_id": target_id,
                "owners": owners,
            })
            valid = False
            environment = None
        else:
            environment = contexts[range_value].get("target_environments", {}).get(target_id)
        expected_path = contexts[range_value].get("target_path")
        if target.get("path") != expected_path:
            global_issues.append({
                "code": "global-first-use-inline-path",
                "message": "Inline articulation target path is stale or false.",
                **_record_location(row, range_value),
                "expected": expected_path,
                "observed": target.get("path"),
            })
            valid = False
        expected_file_hash = contexts[range_value].get("target_file_sha256")
        if expected_file_hash is not None and target.get("file_sha256") != expected_file_hash:
            global_issues.append({
                "code": "global-first-use-inline-file-hash",
                "message": "Inline articulation target file SHA-256 is stale or false.",
                **_record_location(row, range_value),
                "expected": target.get("file_sha256"),
                "observed": expected_file_hash,
            })
            valid = False
        if environment is not None:
            if target.get("body_sha256") != environment.body_sha256:
                global_issues.append({
                    "code": "global-first-use-inline-body-hash",
                    "message": "Inline articulation EESegment body SHA-256 is stale or false.",
                    **_record_location(row, range_value),
                    "target_id": target_id,
                    "expected": target.get("body_sha256"),
                    "observed": environment.body_sha256,
                })
                valid = False
            quote = target.get("exact_quote")
            quote_hash = sha256_bytes(quote.encode("utf-8")) if isinstance(quote, str) else None
            if quote_hash != target.get("exact_quote_sha256"):
                global_issues.append({
                    "code": "global-first-use-inline-quote-hash",
                    "message": "Inline articulation exact-quote SHA-256 is stale or false.",
                    **_record_location(row, range_value),
                    "target_id": target_id,
                    "expected": target.get("exact_quote_sha256"),
                    "observed": quote_hash,
                })
                valid = False
            occurrence_count = environment.body.count(quote) if isinstance(quote, str) and quote else 0
            if occurrence_count != 1:
                global_issues.append({
                    "code": "global-first-use-inline-exact-quote",
                    "message": "Inline articulation exact_quote must occur exactly once in its cited live EESegment body.",
                    **_record_location(row, range_value),
                    "target_id": target_id,
                    "occurrences": occurrence_count,
                })
                valid = False
        coverage = articulation.get("coverage", {})
        coverage_results = {
            name: coverage.get(name, {}).get("result") if isinstance(coverage.get(name), dict) else None
            for name in ("meaning", "notation", "proof_job", "prerequisites")
        }
        if coverage_results["meaning"] != "pass" or coverage_results["proof_job"] != "pass":
            valid = False
        if coverage_results["notation"] not in {"pass", "not_applicable"}:
            valid = False
        if coverage_results["prerequisites"] not in {"pass", "not_applicable"}:
            valid = False
        if data.get("prerequisite_concepts") and coverage_results["prerequisites"] != "pass":
            valid = False
        if valid and data.get("status") == "pass" and isinstance(data.get("id"), str):
            valid_inline_articulation_ids.add(data["id"])

    for range_value, row in segment_rows:
        for index, term in enumerate(row.data.get("retained_technical_terms", [])):
            candidate_id = term.get("first_use_candidate_id")
            addition_id = term.get("explanation_addition_id")
            available = term.get("first_use_explanation_available")
            if candidate_id is not None and candidate_id not in first_use_record_ids:
                global_issues.append({"code": "global-term-first-use-reference", "message": "Retained technical term cites no live first-use candidate record.", **_record_location(row, range_value), "term_index": index, "candidate_id": candidate_id})
            inline_available = candidate_id in valid_inline_articulation_ids
            if available is True:
                if addition_id is not None and addition_id not in all_addition_ids:
                    global_issues.append({"code": "global-term-addition-reference", "message": "Term cites no live teaching addition.", **_record_location(row, range_value), "term_index": index, "addition_id": addition_id})
                elif addition_id is None and not inline_available:
                    global_issues.append({"code": "global-term-explanation-reference", "message": "Term says its first-use explanation is available but cites neither a live teaching addition nor a candidate with valid inline articulation.", **_record_location(row, range_value), "term_index": index, "candidate_id": candidate_id})
            elif addition_id is not None:
                global_issues.append({"code": "global-term-addition-contradiction", "message": "Term cites a teaching addition while declaring that its first-use explanation is unavailable.", **_record_location(row, range_value), "term_index": index, "addition_id": addition_id})
            elif inline_available:
                global_issues.append({"code": "global-term-inline-contradiction", "message": "Term cites valid inline articulation while declaring that its first-use explanation is unavailable.", **_record_location(row, range_value), "term_index": index, "candidate_id": candidate_id})
            if available is False:
                if row.data.get("status") == "pass":
                    global_issues.append({"code": "global-term-explanation-gap", "message": "A passing segment may not leave a retained technical term's first-use explanation unavailable.", **_record_location(row, range_value), "term_index": index, "term": term.get("term")})
                else:
                    global_pending.append({"code": "global-term-explanation-pending", "message": "A retained technical term still lacks its first-use explanation.", **_record_location(row, range_value), "term_index": index, "term": term.get("term")})

    concepts_by_range: Counter[tuple[str, str]] = Counter()
    concept_groups: defaultdict[str, list[tuple[str, LoadedRow]]] = defaultdict(list)
    for range_value, row in first_use_rows:
        data = row.data
        concept = data.get("concept", "")
        normalized = " ".join(concept.casefold().split()) if isinstance(concept, str) else ""
        concepts_by_range[(range_value, normalized)] += 1
        concept_groups[normalized].append((range_value, row))
        proposed = data.get("proposed_addition_id")
        if proposed is not None and proposed not in all_addition_ids:
            global_issues.append({"code": "global-first-use-addition", "message": "First-use candidate cites no live teaching addition anywhere in the edition.", **_record_location(row, range_value), "addition_id": proposed})
        local_target = data.get("local_first_target_id")
        local_order = _target_order(local_target) if isinstance(local_target, str) else (10**9, 10**9, 10**9)
        for reuse_id in data.get("later_reuse_ids", []):
            if reuse_id not in all_segment_ids:
                global_issues.append({"code": "global-first-use-reuse", "message": "Later-reuse ID names no live EESegment.", **_record_location(row, range_value), "reuse_id": reuse_id})
            elif _target_order(reuse_id) <= local_order:
                global_issues.append({"code": "global-first-use-reuse-order", "message": "A later-reuse ID is not later than the candidate occurrence.", **_record_location(row, range_value), "reuse_id": reuse_id})
        resolution = data.get("global_resolution", {}).get("status")
        if resolution == "unresolved":
            global_pending.append({"code": "global-first-use-unresolved", "message": "A first-use candidate still awaits root resolution.", **_record_location(row, range_value), "concept": concept})

    for (range_value, normalized), count in sorted(concepts_by_range.items()):
        if normalized and count > 1:
            global_issues.append({"code": "global-first-use-local-duplicate", "message": "A range has more than one local-first candidate for the same normalized concept.", "range": range_value, "concept": normalized, "count": count})

    for normalized, members in sorted(concept_groups.items()):
        if not normalized:
            continue
        confirmed = [(range_value, row) for range_value, row in members if row.data.get("global_resolution", {}).get("status") == "confirmed_first"]
        unresolved = [(range_value, row) for range_value, row in members if row.data.get("global_resolution", {}).get("status") == "unresolved"]
        if unresolved:
            continue
        if len(confirmed) != 1:
            global_issues.append({
                "code": "global-first-use-cardinality",
                "message": "Each resolved concept needs exactly one globally confirmed first candidate.",
                "concept": normalized,
                "confirmed_record_ids": [row.data.get("id") for _, row in confirmed],
            })
            continue
        earliest = min(members, key=lambda pair: _target_order(pair[1].data.get("local_first_target_id", "")))
        if confirmed[0][1].data.get("id") != earliest[1].data.get("id"):
            global_issues.append({
                "code": "global-first-use-order",
                "message": "Confirmed global first use is not the earliest candidate in manuscript order.",
                "concept": normalized,
                "confirmed": confirmed[0][1].data.get("id"),
                "earliest": earliest[1].data.get("id"),
            })
        confirmed_row = confirmed[0][1]
        if (
            confirmed_row.data.get("proposed_addition_id") is None
            and confirmed_row.data.get("id") not in valid_inline_articulation_ids
        ):
            global_issues.append({
                "code": "global-first-use-no-explanation",
                "message": "A confirmed first use needs either a live teaching addition or an exact, current inline articulation that covers meaning, notation, proof job, and prerequisites.",
                "concept": normalized,
                **_record_location(confirmed_row, confirmed[0][0]),
            })

    for range_value in ranges:
        for path_text, expected_hash in contexts[range_value].get("file_snapshots", {}).items():
            path = Path(path_text)
            if not path.is_file():
                global_issues.append({"code": "global-file-changed-during-audit", "message": "An audited file disappeared before the aggregate audit finished.", "range": range_value, "path": path_text})
            else:
                observed_hash = sha256_path(path)
                if observed_hash != expected_hash:
                    global_issues.append({"code": "global-file-changed-during-audit", "message": "An audited file changed before the aggregate audit finished.", "range": range_value, "path": path_text, "expected": expected_hash, "observed": observed_hash})

    range_statuses = Counter(report["status"] for report in range_reports)
    if global_issues or range_statuses["fail"]:
        status = "fail"
    elif global_pending or range_statuses["pending"]:
        status = "pending"
    else:
        status = "pass"
    return {
        "schema": "navier-stokes-everyday-all-audit/v1",
        "status": status,
        "expected_ranges": len(ranges),
        "range_status_counts": {key: range_statuses[key] for key in ("pass", "pending", "fail")},
        "ranges": range_reports,
        "global_counts": {
            "record_ids": len(record_locations),
            "ee_segment_ids": len(target_locations),
            "ee_addition_ids": len(addition_locations),
            "first_use_candidates_live": len(first_use_rows),
        },
        "global_pending": global_pending,
        "global_issues": global_issues,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    report = audit_all(args.root)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return {"pass": 0, "fail": 1, "pending": 2}[report["status"]]


if __name__ == "__main__":
    raise SystemExit(main())
