# Quality gates

Read this file before finalizing any paper or collection.

## Per-paper semantics

- Background defines task and setting without presenting the solution.
- Motivation identifies a concrete prior gap and differs from Background.
- Idea states one conceptual move in fresh language and explains why it closes that gap.
- Method traces input to output in causal order. Every major stage identifies input, transformation, output, consumer, and purpose.
- Method covers objectives, training, and inference when applicable. Essential equations define symbols and explain operational roles.
- Experiments identify evaluation scope, main results, ablations when present, and what each result supports.
- Conclusion stays within the evidence and introduces no new result.

## Provenance

- Every full-text section has at least one relevant evidence-map entry.
- Every method-trace stage references method evidence.
- Every experiment-trace item connects a test, result, and interpretation.
- Related-work claims are not attributed to the reviewed method.
- Appendix evidence is absent unless `content_scope` includes appendices.

## Synthesis

- Background -> Motivation -> Idea -> Method forms one causal chain.
- Idea is not an abstract paraphrase, contribution list, or module inventory.
- Method explains interfaces and transformations rather than listing components.
- No paragraph preserves long source clause sequences or merely translates them.
- Repeated claims across sections are removed.

## Extraction hygiene

Reject or repair running titles, page headers, author footers, references, acknowledgements, grant text, caption-only fragments, table rows used as prose, corrupted equations, replacement characters, and mojibake.

## Collection checks

- Input count, unique-paper count, output count, and unavailable count reconcile.
- Every normalized paper appears exactly once and retains its original ordinal.
- Every requested language exists for every completed paper.
- Source URLs are present and arXiv links are clickable when available.
- Validated batches are not silently regenerated.
- Sample the start, middle, end, every category, every evidence level, and every target language.

## Paper-type adaptation

- **Benchmark or dataset:** explain construction, coverage, evaluation protocol, reliability checks, and what the benchmark reveals.
- **Survey:** explain scope, taxonomy, comparison framework, synthesis, and coverage limits.
- **Theory:** explain assumptions, theorem claims, proof strategy, and empirical validation if present.
- **Systems:** explain architecture, interfaces, execution, scalability, reliability, and deployment evidence.
- **Position:** distinguish the argument and supporting evidence from controlled experiments.

## Artifact checks

For LaTeX/PDF, compile until links and references stabilize, inspect logs for missing glyphs and overflow, render every page, and inspect equations, headings, page breaks, spacing, and link wrapping. For DOCX, use the relevant document render-and-inspect workflow.
