# Evidence levels and main-text cutoff

Read this file when source quality, version selection, or the main-text boundary is uncertain.

## Source hierarchy

1. Author-hosted or official open PDF
2. arXiv PDF matching normalized title and authors
3. Official proceedings or journal PDF
4. Reliable institutional or open repository copy
5. Publisher, Crossref, OpenAlex, or equivalent abstract
6. Bibliographic metadata only

Prefer the latest author or arXiv version unless the user requests the accepted or camera-ready version. Do not promote snippets to `abstract` or an abstract to `fulltext`.

## Main-text cutoff

For the default `main_text` scope, stop at the earliest reliable back-matter marker after the conclusion:

- `Appendix`, `Appendices`, or a lettered appendix heading;
- `Supplementary Material`;
- acknowledgements following the conclusion;
- `References` or `Bibliography`;
- clearly labeled appendix-only proofs, prompts, hyperparameters, or additional experiments.

Confirm ambiguous boundaries visually. Two-column extraction may place a running title or appendix heading inside conclusion text. If an appendix begins on the same page, keep only text before the marker.

If the user explicitly requests appendices or supplementary material, record `content_scope: main_text_and_appendices` and label appendix-derived evidence in the evidence map.

## Evidence packet

Create stable evidence IDs such as `bg1`, `mot1`, `idea1`, `m1`, `exp1`, and `con1`. Each item should contain:

- `id`;
- `section`;
- `claim` supported by the source;
- `page` when reliably known;
- `locator` such as equation, algorithm, figure, table, or paragraph cue when useful;
- `source_scope`: `main_text`, `appendix`, `abstract`, or `metadata`.

For `abstract`, use only abstract claims and explicitly mark unverified implementation and experimental details. For `metadata`, do not infer six-part content from the title.

## Contamination rejection

Reject or repair:

- running headers, footers, author biographies, grant text, and references;
- captions without explanatory prose;
- table rows or corrupted formulas extracted as sentences;
- related-work claims presented as the reviewed paper's method;
- appendix-only facts when the selected scope excludes appendices.
