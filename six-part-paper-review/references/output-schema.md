# Versioned output schema

Read this file when producing JSON, resumable batches, multiple output languages, or provenance-rich reviews.

## Collection envelope

```json
{
  "schema_version": "2.0",
  "content_scope": "main_text",
  "target_languages": ["zh-CN"],
  "papers": []
}
```

Use BCP-47 language tags. `content_scope` is normally `main_text`; use `main_text_and_appendices` only when requested.

## Paper record

```json
{
  "paper_id": "arxiv:2501.01234",
  "ordinal": 1,
  "title": "Original English Title",
  "authors": ["Author One", "Author Two"],
  "year": 2025,
  "venue": "Venue or status",
  "categories": ["Category"],
  "identifiers": {
    "arxiv": "2501.01234",
    "doi": ""
  },
  "source_url": "https://arxiv.org/abs/2501.01234",
  "evidence_level": "fulltext",
  "status": "validated",
  "evidence_map": {
    "background": [
      {
        "id": "bg1",
        "section": "Introduction",
        "page": 2,
        "locator": "paragraph beginning ...",
        "claim": "The task and why it matters.",
        "source_scope": "main_text"
      }
    ],
    "motivation": [],
    "idea": [],
    "method": [],
    "experiments": [],
    "conclusion": []
  },
  "method_trace": [
    {
      "order": 1,
      "stage": "Representation construction",
      "input": "Raw input",
      "operation": "Transformation performed",
      "output": "Intermediate representation",
      "consumer": "Next stage",
      "purpose": "Why this stage is needed",
      "evidence_refs": ["m1"]
    }
  ],
  "experiment_trace": [
    {
      "what_was_tested": "Main comparison or ablation",
      "result": "Observed result",
      "interpretation": "What the result supports",
      "evidence_refs": ["exp1"]
    }
  ],
  "terminology": {
    "GraphRAG": "GraphRAG"
  },
  "reviews": {
    "zh-CN": {
      "background": "One coherent paragraph.",
      "motivation": "One coherent paragraph.",
      "idea": "One coherent paragraph.",
      "method": "Implementation-level explanation with essential equations when useful.",
      "experiments": "One coherent paragraph.",
      "conclusion": "One coherent paragraph."
    }
  }
}
```

Valid evidence levels are `fulltext`, `abstract`, and `metadata`. Valid terminal statuses are `validated`, `unavailable`, and `failed`.

An `unavailable` or `failed` record may omit `reviews`, `evidence_map`, and traces, but it must include `unavailable_reason` or `error`. Keep it in the collection so counts and ordering remain auditable.

## Multilingual rules

Put every requested language under `reviews` using the exact language tag listed in `target_languages`. All language versions must express the same supported claims. Keep one shared evidence map, method trace, experiment trace, and terminology map rather than duplicating provenance by language.

## Backward compatibility

The validator also accepts legacy records containing:

```json
{
  "evidence": "fulltext",
  "summary": {
    "background": "...",
    "motivation": "...",
    "idea": "...",
    "method": "...",
    "experiments": "...",
    "conclusion": "..."
  }
}
```

Legacy input remains readable, but use schema `2.0` for new resumable or multilingual jobs.
