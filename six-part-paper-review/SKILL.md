---
name: six-part-paper-review
description: "Read and synthesize academic papers into six clear narrative sections: problem background, motivation, core idea, implementation-level method, experiments and what they demonstrate, and conclusion. Use when Codex receives paper PDFs, arXiv/DOI links, publication lists, researcher-homepage papers, or an existing paper-summary document that needs to be rewritten for comprehension. Supports five-paper pilot batches, reading all main-text content before appendices/references, equations and executable method flows, evidence grading, clickable source links, batch consistency checks, and LaTeX-to-PDF delivery."
---

# Six-Part Paper Review

Produce readable paper summaries grounded in the paper itself. Treat the six-part structure as a causal explanation reconstructed from the whole paper, not six translated excerpts. The reader should understand both why the work exists and how the proposed system or argument actually operates without reopening the paper for basic clarification.

## Required output structure

Write each part as a logically connected narrative rather than a list of extracted claims. Use one coherent paragraph for Background, Motivation, Idea, Experiments, and Conclusion. Method may contain displayed equations or compact numbered stages when they materially improve understanding, but connect them with explanatory prose so the section still reads as one argument.

1. **问题背景 / Problem background** — Explain the task, setting, and why the broad problem matters. Do not introduce the paper's solution yet.
2. **Motivation** — State the concrete limitation, missing capability, or contradiction in prior approaches. Make the transition from background to research need explicit.
3. **Idea** — Reconstruct the single central conceptual move: what representation, decomposition, learning signal, system design, or theoretical perspective makes the proposed solution possible, and why that move addresses the Motivation. Explain it in original plain language before introducing module names. Do not use a contribution list or a paraphrase of the abstract as the Idea.
4. **Method** — Explain how the Idea is realized at implementation level. Start with inputs and desired outputs, then walk through the actual execution or training sequence in causal order. For each important stage, identify what enters, what transformation is performed, what is produced, and how the result is consumed next. Explain module interactions, data construction, objectives, inference, optimization, and special handling when present. Include essential equations, defining every symbol and explaining what the equation accomplishes; omit decorative equations that do not help reconstruct the method.
5. **Experiments** — State what was evaluated: datasets or scenarios, baselines, metrics, major quantitative/qualitative results, ablations, and what each result supports. Never list numbers without interpreting them.
6. **Conclusion** — State what the paper establishes, its practical or scientific significance, and any material limitation supported by the paper.

Keep the original English title. Add a clickable arXiv link when an arXiv version exists; otherwise use the official proceedings page or DOI.

## Pilot before a large batch

When the user requests a sample, prototype, or quality check for a larger collection, summarize exactly five representative papers unless the user specifies another number. Select papers that expose methodological diversity rather than simply taking the first five. Complete and render the five-paper PDF before scaling up. Use the pilot to check depth, terminology, equation rendering, page density, and whether Idea and Method are clearly distinguished. Do not silently expand a requested pilot into the full collection.

## Workflow

### 1. Establish scope and sources

- Resolve the requested paper list before summarizing.
- Deduplicate by normalized title, DOI, or arXiv ID while retaining all source categories.
- Prefer sources in this order: author-provided PDF, arXiv, official proceedings/journal PDF, reliable open repository, abstract-only record, metadata-only record.
- Record title, authors, year, venue, categories, arXiv/DOI, source URL, and local PDF path.
- Do not silently omit papers. Report unresolved or unavailable sources.

### 2. Read the whole main text

For every available PDF, read from the abstract through the conclusion and stop before appendices, supplementary material, acknowledgements, or references. Include limitations/discussion when they appear before that cutoff.

Read in this order:

1. Abstract and introduction for the task, gap, claimed contributions, and terminology.
2. Related work for the exact limitation relative to prior approaches.
3. Method sections for components, algorithms, data flow, training and inference procedures, objectives, notation, and implementation choices.
4. Experimental sections for datasets, baselines, metrics, results, ablations, robustness, and efficiency.
5. Discussion, limitations, and conclusion for the scope of supported claims.

Use PDF text extraction for coverage and page rendering for figures, tables, equations, algorithms, or layout-dependent evidence. Cross-check broken equation extraction against the rendered page or the paper's TeX source when available. Do not infer method details from the abstract if the full text is available.

### 3. Grade the evidence

Assign one evidence level per paper:

- `fulltext`: a reliable PDF was read through the main-text cutoff.
- `abstract`: a reliable abstract was available but the main text was not.
- `metadata`: only title/authors/venue or equivalent bibliographic data was verified.

For `abstract`, summarize only claims present in the abstract and state the limitation. For `metadata`, do not infer the six parts from the title; explicitly mark each part as unavailable pending the paper text.

Read [references/evidence-and-cutoff.md](references/evidence-and-cutoff.md) when PDF structure is ambiguous or the extraction crosses into appendices/references.

### 4. Build an evidence map before drafting

For each part, retain the supporting section, page, equation/algorithm, figure/table if relevant, and the exact claim it supports. Use the abstract and introduction to establish the high-level story, but reconstruct Idea and Method primarily from the technical sections. Build a method trace before drafting: `input -> preprocessing/representation -> core stages -> objective or decision rule -> inference/output`. If the paper has multiple branches, show where they split and recombine.

Reject candidate evidence that contains:

- page headers, author footers, section-title fragments, or reference entries;
- figure/table captions without an explanatory sentence;
- corrupted formulas or table rows extracted as prose; preserve a clean formula when it is essential to the method;
- claims from related work presented as the paper's own method/result;
- appendix-only implementation details when the requested cutoff is before the appendix.

### 5. Draft for comprehension

- Use short technical explanations with explicit causal transitions.
- Synthesize across sections. First decide what the paper means, then explain it in fresh language. Do not translate sentence by sentence, preserve the paper's paragraph order by default, or stitch together lightly paraphrased source sentences.
- Test the Idea with this question: could a reader state the paper's one decisive insight without naming its modules? If not, rewrite it at the conceptual level.
- Test the Method with these questions: could a technically literate reader trace one input through every major stage, explain the role of each component, and understand the training objective or inference rule? If not, return to the method, algorithm, and equation pages.
- Introduce every key formula in prose, write it in valid LaTeX, define all non-obvious symbols immediately after it, and explain the causal or optimization role of the formula. Never paste a formula without interpretation.
- When exact low-level details appear only in an excluded appendix, state that the main text does not specify them instead of guessing or reading beyond the requested cutoff.
- Define abbreviations on first use.
- Keep model, benchmark, and metric names in English when translation would reduce precision.
- Translate `LLM` as `大语言模型`, `agent` as `智能体`, and retain `token` in English unless the user asks otherwise.
- Avoid sentence-by-sentence bilingual mirroring unless requested; it makes long compendia difficult to read.
- Remove redundant claims across Background, Motivation, Idea, and Conclusion.
- When machine translation is used, manually correct technical terms and grammatical breaks.

### 6. Validate every paper and the batch

Read [references/quality-gates.md](references/quality-gates.md) before finalizing a batch.

If producing the JSON schema described in [references/output-schema.md](references/output-schema.md), run:

```powershell
python scripts/validate_six_part_json.py summaries.json --expected-count 5
```

Use `--expected-count` only when the requested count is known. Fix all errors. Review warnings involving shallow Idea/Method sections, short paragraphs, suspicious PDF fragments, repeated sections, missing links, or weak experimental evidence. Character thresholds are triage signals, not substitutes for semantic review.

### 7. Deliver LaTeX and PDF

Use LaTeX as the primary editable source and compile a PDF:

- Use XeLaTeX or LuaLaTeX with Chinese-capable fonts; prefer `ctexart` for Chinese summaries.
- Load `hyperref` and render the title or a visible `arXiv` label as a clickable `https://arxiv.org/abs/...` link.
- Put the original English title, authors/year/venue when known, evidence level, and source link before the six sections.
- Use `\section` for categories, `\subsection` for papers, and unnumbered six-part subheadings below each paper. Keep prose primary; use `enumerate` only inside Method when the algorithm genuinely has ordered stages.
- Typeset important equations with `equation`, `aligned`, or `align`; keep notation definitions next to the equation and avoid lines that overflow the text block.
- Escape metadata and prose characters that are special in LaTeX. Preserve intentional math commands.
- Compile until cross-references and links stabilize. Treat warnings about missing glyphs, overfull boxes, undefined references, and malformed links as defects to fix.
- Render every PDF page to images and inspect for broken Chinese glyphs, clipped equations, overflow, excessive blank space, awkward headings, and unreadable link wrapping. Use the PDF skill's render-inspect-iterate workflow.
- Deliver both the `.tex` source and compiled `.pdf`. Preserve earlier documents and save the rewrite under new filenames unless explicitly told to replace them.

## Failure rules

- Never claim to have read a full paper when only the abstract or metadata was available.
- Never fill missing method or experiment details from general domain knowledge.
- Never substitute fluent translation for synthesis. Shared terminology and unavoidable factual phrases are acceptable; sentence structure and explanatory organization must be newly constructed around the six-part causal story.
- Never present module names as an explanation of the method. State what each module consumes, does, produces, and why it is needed.
- Never treat a benchmark construction paper as if it must contain a conventional model-training experiment.
- For surveys, summarize taxonomy, coverage, comparative analysis, and synthesis instead of inventing a single controlled experiment.
- For theory papers, emphasize assumptions, theorem claims, proof structure, and empirical validation if present.
- For position papers, distinguish argument/evidence from experimental results.

## Output check

Before delivery, confirm:

- all scoped papers are present once;
- every paper has all six paragraphs;
- every paragraph is readable and supported at its evidence level;
- every Idea states one conceptual mechanism and explicitly closes the gap identified in Motivation;
- every full-text Method traces inputs to outputs, explains implementation stages and component interfaces, and includes/interprets essential objectives or equations when the paper uses them;
- no section is a sentence-by-sentence translation, abstract paraphrase, or collage of source sentences;
- the Experiments paragraph answers both “做了什么” and “说明了什么”;
- no corrupted formula, caption, header, reference, or appendix fragment remains;
- every available arXiv link is clickable;
- unavailable sources are disclosed rather than guessed;
- the final `.tex` compiles reproducibly and the PDF passed visual render QA.
