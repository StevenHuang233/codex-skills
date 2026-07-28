---
name: six-part-paper-review
description: "Read and synthesize one or many academic papers into six connected sections: problem background, motivation, core idea, implementation-level method, experiments and what they demonstrate, and conclusion. Use for PDFs, arXiv or DOI links, publication lists, researcher homepages, mixed paper collections, multilingual summaries, or existing paper summaries that need evidence-grounded rewriting. Supports single-paper and resumable batch workflows, main-text cutoffs, evidence maps, method traces, equations, structured JSON, and LaTeX/PDF delivery."
---

# Six-Part Paper Review

Reconstruct each paper as a causal explanation, not a translation or collage of source sentences.

## Core output

Produce these six connected sections in every requested output language:

1. **Problem background** — Define the task, setting, and importance without introducing the paper's solution.
2. **Motivation** — Identify the specific limitation, missing capability, or contradiction that creates the research need.
3. **Core idea** — State one decisive conceptual move in plain language and explain why it closes the motivation gap.
4. **Method** — Trace inputs to outputs in execution order. Explain each major stage's input, transformation, output, downstream consumer, and purpose. Cover data construction, objectives, training, inference, and essential equations when applicable.
5. **Experiments** — Explain datasets or scenarios, baselines, metrics, principal results, ablations, and what each result supports.
6. **Conclusion** — State what the paper establishes, its significance, and evidence-supported limitations.

Keep the original paper title. Preserve model, dataset, benchmark, metric, variable, and equation names when translation would reduce precision. Add a clickable arXiv link when available; otherwise use an official paper page or DOI.

## Resolve the run

1. Count and normalize the requested papers before drafting.
2. Resolve output language from the user's explicit request. Otherwise use the user's language. Support one or more BCP-47 language tags such as `en`, `zh-CN`, `ja`, or `de`.
3. Use direct mode for one paper. Use a manifest and resumable batches for collections when durable artifacts are useful.
4. Default to batches of five papers for collections, but reduce the batch size when papers are long or equation-heavy. Never concatenate an entire large collection into one prompt.
5. Treat a requested pilot as a pilot. Use five methodologically diverse papers unless the user specifies another count.

Read [references/input-and-batching.md](references/input-and-batching.md) for multi-paper, mixed-source, deduplication, batching, and resume rules. Run `scripts/init_review_job.py` when a deterministic manifest is useful.

## Workflow

### 1. Resolve sources

Prefer author-hosted or official PDFs, then arXiv, proceedings or journal PDFs, reliable repositories, abstracts, and metadata. Record title, authors, year, venue, categories, identifiers, source URL, and local path. Do not silently omit or merge unresolved items.

### 2. Read the available evidence

For a reliable PDF, read the complete main text from abstract through conclusion or limitations and stop before appendices, supplementary material, acknowledgements, or references unless the user explicitly changes the cutoff.

Read in this order:

1. Abstract and introduction for task, scope, terminology, and claimed contribution.
2. Related work for the exact prior limitation.
3. Technical sections for representations, stages, interfaces, algorithms, objectives, training, and inference.
4. Experiments for setup, baselines, metrics, results, ablations, robustness, and efficiency.
5. Discussion, limitations, and conclusion for claim boundaries.

Use text extraction for coverage and rendered PDF pages or TeX source for layout-dependent equations, algorithms, figures, and tables. Read [references/evidence-and-cutoff.md](references/evidence-and-cutoff.md) whenever source quality or the main-text boundary is ambiguous.

### 3. Grade evidence

Assign exactly one level:

- `fulltext`: reliable main text was read through the cutoff.
- `abstract`: only a reliable abstract was available.
- `metadata`: only bibliographic metadata was verified.

Never infer unavailable method or experimental details. State the limitation for `abstract`; mark technical content unavailable for `metadata`.

### 4. Build the evidence packet

Before prose, build and retain:

- an evidence map from every six-part claim to section, page or locator, equation or table when relevant;
- a method trace: `input -> representation/preprocessing -> core stages -> objective or decision rule -> inference -> output`;
- an experiment trace linking each test to its result and interpretation;
- a terminology map for multilingual output.

Reject headers, footers, reference entries, caption-only fragments, corrupted formulas, and claims about baselines mistakenly attributed to the paper.

### 5. Draft from the packet

Draft all six sections from the same evidence packet so they form one causal chain. Do not preserve source paragraph order or translate sentence by sentence.

- Rewrite Idea if it is merely a contribution list or module inventory.
- Rewrite Method if a technical reader cannot follow one input through the major stages or understand training and inference.
- Introduce every essential formula in prose, define non-obvious symbols, and explain its operational role.
- Interpret every reported number. Experiments must answer both "what was done" and "what it demonstrates."
- Adapt the six-part semantics for surveys, theory, benchmarks, systems, and position papers without inventing a conventional training experiment.

Read [references/multilingual-output.md](references/multilingual-output.md) when output differs from the paper language or includes multiple languages.

### 6. Persist and validate

For structured runs, write the versioned record in [references/output-schema.md](references/output-schema.md). Keep one record per normalized paper and checkpoint after every batch.

Run:

```powershell
python scripts/validate_six_part_json.py reviews.json
```

Use `--expected-count N`, `--target-language TAG`, and `--require-provenance` when applicable. Fix errors and review every warning. For multi-file runs, merge only validated batches with `scripts/merge_review_batches.py`.

Read [references/quality-gates.md](references/quality-gates.md) before final delivery.

### 7. Deliver the requested artifact

Return the requested subset of JSON, Markdown, LaTeX, PDF, or DOCX. For LaTeX/PDF, use Unicode-capable typesetting, structural headings, visible source links, stable equation layout, and render-inspect-iterate QA. Preserve source JSON and editable files so a collection can resume without regenerating completed papers.

## Failure boundaries

- Do not claim full-text reading from snippets or an abstract.
- Do not fill missing evidence from domain knowledge.
- Do not treat fluent translation as synthesis.
- Do not name a component without explaining what it consumes, does, produces, and enables.
- Do not let one missing paper block a collection; record its status and continue with resolvable papers.
- Do not regenerate validated completed batches unless the user requests a revision or the schema changes.
