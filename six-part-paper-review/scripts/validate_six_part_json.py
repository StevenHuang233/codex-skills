#!/usr/bin/env python3
"""Validate legacy and schema-2.0 six-part paper-review JSON."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


PARTS = ("background", "motivation", "idea", "method", "experiments", "conclusion")
VALID_EVIDENCE = {"fulltext", "abstract", "metadata"}
VALID_STATUS = {
    "pending",
    "source_resolved",
    "evidence_ready",
    "drafted",
    "validated",
    "unavailable",
    "failed",
}
TRACE_FIELDS = ("stage", "input", "operation", "output", "consumer", "purpose")
SUSPICIOUS = re.compile(
    r"(?:\ufffd|automated translation failed|figure\s*\d+\s*:|table\s*\d+\s*:|"
    r"references\s*$|appendix\s+[a-z0-9]+|acknowledg(?:e)?ments|"
    r"[锟鈥銆]{3,}|(?:figure|fig\.|table|sec\.)\s*\d+\s+(?:shows?|presents?))",
    re.IGNORECASE | re.MULTILINE,
)


def normalized(text: str) -> str:
    return re.sub(r"\W+", "", (text or "").lower())


def nonspace_length(text: str) -> int:
    return len(re.sub(r"\s+", "", text or ""))


def paper_identity(paper: dict[str, Any]) -> str:
    if paper.get("paper_id"):
        return str(paper["paper_id"])
    identifiers = paper.get("identifiers") or {}
    if identifiers.get("arxiv"):
        return "arxiv:" + re.sub(r"v\d+$", "", str(identifiers["arxiv"]).lower())
    if identifiers.get("doi"):
        return "doi:" + str(identifiers["doi"]).lower()
    return "title:" + normalized(str(paper.get("title") or ""))


def summary_views(
    paper: dict[str, Any], envelope_languages: list[str]
) -> tuple[dict[str, dict[str, Any]], bool]:
    reviews = paper.get("reviews")
    if isinstance(reviews, dict):
        return {str(language): value for language, value in reviews.items() if isinstance(value, dict)}, False
    legacy = paper.get("summary") or (paper.get("sixpart_review") or {}).get("zh")
    if isinstance(legacy, dict):
        language = envelope_languages[0] if envelope_languages else "und"
        return {language: legacy}, True
    return {}, False


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_path", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--target-language", action="append", dest="target_languages")
    parser.add_argument("--min-section-chars", type=int, default=35)
    parser.add_argument("--min-idea-chars", type=int, default=80)
    parser.add_argument("--min-method-chars", type=int, default=220)
    parser.add_argument("--require-provenance", action="store_true")
    args = parser.parse_args()

    payload = json.loads(args.json_path.read_text(encoding="utf-8"))
    papers = payload.get("papers") if isinstance(payload, dict) else payload
    if not isinstance(papers, list):
        raise SystemExit("ERROR: root must be a list or an object containing a 'papers' list")

    envelope_languages = []
    if isinstance(payload, dict):
        envelope_languages = [str(tag) for tag in payload.get("target_languages") or []]
    requested_languages = args.target_languages or envelope_languages
    errors: list[str] = []
    warnings: list[str] = []

    if args.expected_count is not None and len(papers) != args.expected_count:
        errors.append(f"expected {args.expected_count} papers, found {len(papers)}")

    seen: dict[str, int] = {}
    for index, raw in enumerate(papers, 1):
        if not isinstance(raw, dict):
            errors.append(f"paper {index}: record is not an object")
            continue
        paper = raw
        title = str(paper.get("title") or "").strip()
        label = f"paper {index}: {title or '<missing title>'}"
        if not title:
            errors.append(f"{label}: missing title")
        identity = paper_identity(paper)
        if identity in seen:
            errors.append(f"{label}: duplicate identity; first seen at paper {seen[identity]}")
        else:
            seen[identity] = index

        review_container = paper.get("sixpart_review") or {}
        evidence = paper.get("evidence_level") or paper.get("evidence") or review_container.get("evidence")
        if evidence not in VALID_EVIDENCE:
            errors.append(f"{label}: invalid evidence level {evidence!r}")

        status = paper.get("status")
        if status is not None and status not in VALID_STATUS:
            errors.append(f"{label}: invalid status {status!r}")

        public = paper.get("public_source") or {}
        source_url = str(
            paper.get("source_url") or public.get("source_url") or public.get("pdf_url") or ""
        ).strip()
        if not source_url:
            warnings.append(f"{label}: missing source_url")
        elif not re.match(r"https?://", source_url):
            errors.append(f"{label}: source_url is not HTTP(S)")

        views, legacy = summary_views(paper, envelope_languages)
        if status in {"unavailable", "failed"} and not views:
            reason = str(paper.get("unavailable_reason") or paper.get("error") or "").strip()
            if not reason:
                errors.append(f"{label}: terminal status {status!r} requires unavailable_reason or error")
            continue
        if legacy:
            warnings.append(f"{label}: legacy summary schema; provenance and multilingual checks are limited")
        if not views:
            errors.append(f"{label}: missing reviews/summary")
            continue

        for language in requested_languages:
            if language not in views:
                errors.append(f"{label}: missing requested language {language!r}")

        for language, summary in views.items():
            values: list[str] = []
            for part in PARTS:
                value = str(summary.get(part) or "").strip()
                values.append(value)
                part_label = f"{label} [{language}] {part}"
                if not value:
                    errors.append(f"{part_label}: missing text")
                    continue
                length = nonspace_length(value)
                if evidence != "metadata" and length < args.min_section_chars:
                    warnings.append(f"{part_label}: short section ({length} non-space chars)")
                if evidence == "fulltext" and part == "idea" and length < args.min_idea_chars:
                    warnings.append(f"{part_label}: idea may be shallow ({length} chars)")
                if evidence == "fulltext" and part == "method" and length < args.min_method_chars:
                    warnings.append(f"{part_label}: method may lack implementation detail ({length} chars)")
                if SUSPICIOUS.search(value):
                    warnings.append(f"{part_label}: suspicious extraction or mojibake fragment")
            comparable = [normalized(value) for value in values if value]
            if len(comparable) != len(set(comparable)):
                warnings.append(f"{label} [{language}]: repeated six-part sections")

        evidence_map = paper.get("evidence_map")
        method_trace = paper.get("method_trace")
        experiment_trace = paper.get("experiment_trace")
        if evidence == "fulltext":
            missing_provenance: list[str] = []
            if not isinstance(evidence_map, dict):
                missing_provenance.append("evidence_map")
            else:
                missing_parts = [part for part in PARTS if not evidence_map.get(part)]
                if missing_parts:
                    missing_provenance.append("evidence_map sections: " + ", ".join(missing_parts))
            if not isinstance(method_trace, list) or not method_trace:
                missing_provenance.append("method_trace")
            if not isinstance(experiment_trace, list) or not experiment_trace:
                missing_provenance.append("experiment_trace")
            for item in missing_provenance:
                target = errors if args.require_provenance else warnings
                target.append(f"{label}: missing {item}")

        if isinstance(method_trace, list):
            evidence_ids = set()
            if isinstance(evidence_map, dict):
                for entries in evidence_map.values():
                    if isinstance(entries, list):
                        evidence_ids.update(str(entry.get("id")) for entry in entries if isinstance(entry, dict) and entry.get("id"))
            for stage_index, stage in enumerate(method_trace, 1):
                if not isinstance(stage, dict):
                    errors.append(f"{label}: method_trace stage {stage_index} is not an object")
                    continue
                for field in TRACE_FIELDS:
                    if not str(stage.get(field) or "").strip():
                        errors.append(f"{label}: method_trace stage {stage_index} missing {field}")
                refs = [str(ref) for ref in stage.get("evidence_refs") or []]
                if args.require_provenance and not refs:
                    errors.append(f"{label}: method_trace stage {stage_index} missing evidence_refs")
                unknown = [ref for ref in refs if ref not in evidence_ids]
                if unknown:
                    errors.append(f"{label}: method_trace stage {stage_index} has unknown refs {unknown}")

    print(f"papers={len(papers)} errors={len(errors)} warnings={len(warnings)}")
    for item in errors:
        print("ERROR:", item)
    for item in warnings:
        print("WARNING:", item)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
