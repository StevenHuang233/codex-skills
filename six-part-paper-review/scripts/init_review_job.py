#!/usr/bin/env python3
"""Create a deterministic, resumable paper-review job manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any


def normalize_text(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", (value or "").lower())


def normalize_arxiv(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^arxiv:\s*", "", value)
    value = re.sub(r"v\d+$", "", value)
    return value


def normalize_doi(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", value)
    return re.sub(r"^doi:\s*", "", value)


def identifiers(paper: dict[str, Any]) -> dict[str, str]:
    source = paper.get("identifiers") or {}
    public = paper.get("public_source") or {}
    arxiv = normalize_arxiv(
        source.get("arxiv")
        or paper.get("arxiv")
        or public.get("arxiv_id")
        or (public.get("id") if str(public.get("id", "")).startswith("arxiv:") else "")
    )
    doi = normalize_doi(source.get("doi") or paper.get("doi") or public.get("doi") or "")
    return {"arxiv": arxiv, "doi": doi}


def as_list(value: Any) -> list[Any]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def paper_key(paper: dict[str, Any]) -> str:
    ids = identifiers(paper)
    if ids["arxiv"]:
        return f"arxiv:{ids['arxiv']}"
    if ids["doi"]:
        return f"doi:{ids['doi']}"
    title = normalize_text(str(paper.get("title") or ""))
    authors = as_list(paper.get("authors"))
    first_author = normalize_text(str(authors[0])) if authors else ""
    if not title:
        raise ValueError("paper is missing a title and stable identifier")
    return f"title:{title}:{first_author}" if first_author else f"title:{title}"


def merge_unique(existing: list[Any], incoming: list[Any]) -> list[Any]:
    return list(dict.fromkeys([*existing, *incoming]))


def canonical_paper(paper: dict[str, Any], ordinal: int) -> dict[str, Any]:
    ids = identifiers(paper)
    public = paper.get("public_source") or {}
    pdf = paper.get("fulltext_pdf") or {}
    return {
        "paper_id": paper_key(paper),
        "ordinal": ordinal,
        "title": str(paper.get("title") or "").strip(),
        "authors": as_list(paper.get("authors")),
        "year": paper.get("year"),
        "venue": str(paper.get("venue") or ""),
        "categories": as_list(paper.get("categories")),
        "identifiers": ids,
        "source_url": str(
            paper.get("source_url")
            or public.get("source_url")
            or public.get("url")
            or public.get("pdf_url")
            or ""
        ),
        "local_pdf_path": str(paper.get("local_pdf_path") or pdf.get("path") or ""),
        "status": "pending",
        "batch_id": "",
    }


def load_papers(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    papers = payload.get("papers") if isinstance(payload, dict) else payload
    if not isinstance(papers, list):
        raise ValueError("input must be a JSON list or an object containing a 'papers' list")
    if not papers:
        raise ValueError("input contains no papers")
    if not all(isinstance(item, dict) for item in papers):
        raise ValueError("every paper must be a JSON object")
    return papers


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    parser.add_argument("output_json", type=Path)
    parser.add_argument(
        "--target-language",
        action="append",
        dest="target_languages",
        help="BCP-47 output language tag; repeat for multiple languages",
    )
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument(
        "--content-scope",
        choices=("main_text", "main_text_and_appendices"),
        default="main_text",
    )
    args = parser.parse_args()

    if args.batch_size < 1:
        raise SystemExit("ERROR: --batch-size must be at least 1")
    target_languages = args.target_languages or ["en"]
    if any(not re.fullmatch(r"[A-Za-z]{2,8}(?:-[A-Za-z0-9]{1,8})*", tag) for tag in target_languages):
        raise SystemExit("ERROR: invalid BCP-47-like target language tag")

    raw_papers = load_papers(args.input_json)
    deduped: list[dict[str, Any]] = []
    by_key: dict[str, dict[str, Any]] = {}
    duplicate_count = 0
    for raw in raw_papers:
        key = paper_key(raw)
        if key in by_key:
            duplicate_count += 1
            existing = by_key[key]
            existing["categories"] = merge_unique(existing["categories"], as_list(raw.get("categories")))
            candidate_url = str(raw.get("source_url") or (raw.get("public_source") or {}).get("source_url") or "")
            if not existing["source_url"] and candidate_url:
                existing["source_url"] = candidate_url
            continue
        record = canonical_paper(raw, len(deduped) + 1)
        by_key[key] = record
        deduped.append(record)

    batches: list[dict[str, Any]] = []
    for start in range(0, len(deduped), args.batch_size):
        group = deduped[start : start + args.batch_size]
        batch_id = f"batch_{group[0]['ordinal']:04d}_{group[-1]['ordinal']:04d}"
        for paper in group:
            paper["batch_id"] = batch_id
        batches.append(
            {
                "batch_id": batch_id,
                "ordinals": [paper["ordinal"] for paper in group],
                "paper_ids": [paper["paper_id"] for paper in group],
                "status": "pending",
            }
        )

    digest_basis = "\n".join(paper["paper_id"] for paper in deduped)
    job_id = "review-" + hashlib.sha256(digest_basis.encode("utf-8")).hexdigest()[:12]
    manifest = {
        "schema_version": "2.0",
        "job_id": job_id,
        "content_scope": args.content_scope,
        "target_languages": target_languages,
        "batch_size": args.batch_size,
        "input_count": len(raw_papers),
        "unique_count": len(deduped),
        "duplicate_count": duplicate_count,
        "papers": deduped,
        "batches": batches,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "job_id": job_id,
                "input": len(raw_papers),
                "unique": len(deduped),
                "duplicates": duplicate_count,
                "batches": len(batches),
                "output": str(args.output_json),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
