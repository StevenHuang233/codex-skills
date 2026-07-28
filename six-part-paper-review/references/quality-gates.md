# Quality gates

## Per-paper content

- Background defines the task and setting without presenting the solution.
- Motivation identifies a specific gap and is not a copy of Background.
- Idea states one central conceptual move in fresh language, explains why it closes the stated gap, and is not an abstract/contribution-list paraphrase.
- Method traces input to output in causal order. Every major stage states its input, transformation, output, downstream consumer, and purpose.
- Method covers training objectives and inference behavior when applicable, includes essential equations, defines their symbols, and interprets what each equation controls.
- A technically literate reader can reconstruct the main algorithm or system flow from the Method without reopening the paper.
- Experiments names evaluation scope, reports the main result, and interprets what it supports.
- Conclusion matches the evidence and does not introduce a new method/result.

## Extraction contamination

Reject or rewrite text containing:

- `Figure`, `Fig.`, `Table`, `Sec.`, `Appendix`, page numbers, or running titles embedded mid-sentence;
- corrupted formula symbols, unexplained LaTeX commands, table rows, or more numeric tokens than prose; clean essential formulas are permitted and encouraged in Method;
- references, acknowledgements, grant numbers, or author biographies;
- phrases that clearly describe a baseline or related work as the proposed method.

## Synthesis checks

- Compare the draft against its evidence map, not by preserving the source's sentence order.
- Flag long sequences that mirror the wording or clause order of the abstract, introduction, or method section.
- Flag Idea paragraphs dominated by architecture/module names.
- Flag Method sections that name components without explaining their interfaces and transformations.
- Flag formulas with undefined symbols or no prose explaining their operational role.
- Check that Background -> Motivation -> Idea -> Method forms one causal chain without duplicated sentences.

## Batch checks

- Count input papers, unique normalized titles, and outputs.
- Count evidence levels.
- Flag any missing six-part field or paragraph under roughly 35 Chinese characters, unless evidence is metadata-only.
- Flag translation failures, replacement characters, mojibake, and repeated paragraphs.
- Flag missing source URLs and non-clickable arXiv links.
- Sample papers from the start, middle, end, every category, and every evidence level.
- For a requested pilot, verify that the output contains exactly five representative papers unless the user requested a different count.

## LaTeX/PDF checks

- Use structural LaTeX headings for categories, papers, and six-part sections.
- Avoid a paper title as the last line of a page.
- Avoid forcing a nearly empty continuation page; tighten consistent spacing or let the next paper flow naturally.
- Compile with XeLaTeX or LuaLaTeX and check the log for missing glyphs, overfull boxes, undefined references, and malformed links.
- Render every PDF page and check glyphs, equation clipping, overlap, excessive blank space, header/footer consistency, and clickable link presentation.
