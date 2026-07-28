#!/usr/bin/env python3
"""Merge validated review batches while preserving manifest order."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_collection(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {"papers": payload}
    if not isinstance(payload, dict) or not isinstance(payload.get("papers"), list):
        raise ValueError(f"{path}: expected a list or an object containing a papers list")
    return payload


def identity(paper: dict[str, Any]) -> str:
    if paper.get("paper_id"):
        return str(paper["paper_id"])
    identifiers = paper.get("identifiers") or {}
    if identifiers.get("arxiv"):
        return f"arxiv:{identifiers['arxiv']}"
    if identifiers.get("doi"):
        return f"doi:{identifiers['doi']}"
    return "title:" + "".join(character.lower() for character in str(paper.get("title") or "") if character.isalnum())


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output_json", type=Path)
    parser.add_argument("batch_json", nargs="+", type=Path)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    merged: dict[str, dict[str, Any]] = {}
    target_languages: list[str] = []
    content_scope = "main_text"
    for path in args.batch_json:
        payload = load_collection(path)
        content_scope = str(payload.get("content_scope") or content_scope)
        for language in payload.get("target_languages") or []:
            if language not in target_languages:
                target_languages.append(language)
        for paper in payload["papers"]:
            if not isinstance(paper, dict):
                raise ValueError(f"{path}: paper record is not an object")
            key = identity(paper)
            if key in merged:
                raise ValueError(f"duplicate paper across batches: {key}")
            merged[key] = paper

    if args.manifest:
        manifest = load_collection(args.manifest)
        order = [identity(paper) for paper in manifest["papers"]]
        missing = [key for key in order if key not in merged]
        extras = [key for key in merged if key not in set(order)]
        if missing:
            raise ValueError(f"manifest papers missing from batches: {missing}")
        if extras:
            raise ValueError(f"batch papers missing from manifest: {extras}")
        papers = [merged[key] for key in order]
        target_languages = list(manifest.get("target_languages") or target_languages)
        content_scope = str(manifest.get("content_scope") or content_scope)
    else:
        papers = sorted(merged.values(), key=lambda paper: (paper.get("ordinal") is None, paper.get("ordinal", 0)))

    output = {
        "schema_version": "2.0",
        "content_scope": content_scope,
        "target_languages": target_languages,
        "papers": papers,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"papers": len(papers), "output": str(args.output_json)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
