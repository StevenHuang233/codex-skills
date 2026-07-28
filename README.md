# Codex Skills

Reusable Agent Skills for Codex and compatible clients.

## `six-part-paper-review`

An evidence-grounded workflow for synthesizing one or many academic papers into six connected sections:

1. problem background;
2. motivation;
3. core idea;
4. implementation-level method and essential equations;
5. experiments and what they demonstrate;
6. conclusion.

The skill supports:

- one paper, small collections, and resumable large batches;
- PDFs, arXiv/DOI links, publication lists, and researcher homepages;
- one or several BCP-47 output languages;
- evidence levels, persisted evidence maps, method traces, and experiment traces;
- versioned JSON with backward-compatible validation;
- LaTeX/PDF or other requested delivery formats.

## Install

Copy `six-part-paper-review` into a supported skills directory, or install it from this repository with a compatible skill installer. In Codex, user-scoped skills are commonly stored under `$HOME/.agents/skills`, while repository-scoped skills can live under `.agents/skills`.

The skill follows the [Agent Skills specification](https://agentskills.io/specification) and OpenAI's current [skills guidance](https://developers.openai.com/codex/skills).

## Deterministic helpers

```text
scripts/init_review_job.py          Create a deduplicated, resumable manifest.
scripts/validate_six_part_json.py   Validate legacy and schema-2.0 reviews.
scripts/merge_review_batches.py     Merge validated batches in manifest order.
```
