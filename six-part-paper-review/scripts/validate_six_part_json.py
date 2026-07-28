import argparse
import json
import re
import sys
from pathlib import Path


PARTS = ("background", "motivation", "idea", "method", "experiments", "conclusion")
VALID_EVIDENCE = {"fulltext", "abstract", "metadata"}
SUSPICIOUS = re.compile(
    r"(?:自动翻译失败|�|\\text|\\boxed|参考文献|附录|图\s*\d+|表\s*\d+|"
    r"第\s*\d+(?:\.\d+)*\s*节|\b(?:Figure|Fig\.|Table|Appendix|References)\s*\d*)",
    re.I,
)


def normalized(text):
    return re.sub(r"\W+", "", (text or "").lower())


def main():
    parser = argparse.ArgumentParser(description="Validate six-part paper-summary JSON.")
    parser.add_argument("json_path")
    parser.add_argument("--min-chars", type=int, default=35)
    parser.add_argument("--min-idea-chars", type=int, default=60)
    parser.add_argument("--min-method-chars", type=int, default=150)
    parser.add_argument("--expected-count", type=int)
    args = parser.parse_args()

    path = Path(args.json_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    papers = data.get("papers") if isinstance(data, dict) else data
    if not isinstance(papers, list):
        raise SystemExit("ERROR: root must be a list or an object containing a 'papers' list")

    errors = []
    warnings = []
    if args.expected_count is not None and len(papers) != args.expected_count:
        errors.append(f"expected {args.expected_count} papers, found {len(papers)}")
    seen_titles = {}
    for index, paper in enumerate(papers, 1):
        title = str(paper.get("title") or "").strip()
        label = f"paper {index}: {title or '<missing title>'}"
        if not title:
            errors.append(f"{label}: missing title")
        key = normalized(title)
        if key and key in seen_titles:
            warnings.append(f"{label}: duplicate normalized title; first seen at {seen_titles[key]}")
        elif key:
            seen_titles[key] = index

        review = paper.get("sixpart_review") or {}
        evidence = paper.get("evidence") or paper.get("evidence_level") or review.get("evidence")
        if evidence not in VALID_EVIDENCE:
            errors.append(f"{label}: invalid evidence {evidence!r}")

        public_source = paper.get("public_source") or {}
        source_url = str(
            paper.get("source_url") or public_source.get("source_url") or public_source.get("pdf_url") or ""
        ).strip()
        if not source_url:
            warnings.append(f"{label}: missing source_url")
        elif not re.match(r"https?://", source_url):
            errors.append(f"{label}: source_url is not HTTP(S)")

        summary = paper.get("summary") or review.get("zh") or {}
        values = []
        for part in PARTS:
            value = str(summary.get(part) or "").strip()
            values.append(value)
            if not value:
                errors.append(f"{label}: missing {part}")
                continue
            if evidence != "metadata" and len(value) < args.min_chars:
                warnings.append(f"{label}: short {part} paragraph ({len(value)} chars)")
            if evidence == "fulltext" and part == "idea" and len(value) < args.min_idea_chars:
                warnings.append(
                    f"{label}: idea may be too shallow ({len(value)} chars; target >= {args.min_idea_chars})"
                )
            if evidence == "fulltext" and part == "method" and len(value) < args.min_method_chars:
                warnings.append(
                    f"{label}: method may lack implementation detail "
                    f"({len(value)} chars; target >= {args.min_method_chars})"
                )
            if SUSPICIOUS.search(value):
                warnings.append(f"{label}: suspicious extraction fragment in {part}")

        normalized_values = [normalized(value) for value in values if value]
        if len(normalized_values) != len(set(normalized_values)):
            warnings.append(f"{label}: repeated six-part paragraphs")

    print(f"papers={len(papers)} errors={len(errors)} warnings={len(warnings)}")
    for item in errors:
        print("ERROR:", item)
    for item in warnings:
        print("WARNING:", item)
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
