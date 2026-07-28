# Evidence levels and main-text cutoff

## Source hierarchy

1. Author-hosted or official open PDF
2. arXiv PDF matching the normalized title/authors
3. Official proceedings or journal PDF
4. Reliable repository copy
5. Publisher/OpenAlex abstract
6. Bibliographic metadata only

Do not promote an abstract-only source to `fulltext` because a search result contains snippets.

## Detecting the cutoff

Stop at the earliest reliable back-matter marker after the conclusion:

- `Appendix`, `Supplementary Material`, or lettered appendix headings;
- `Acknowledgements` when it follows the conclusion;
- `References` or `Bibliography`;
- a new section whose content clearly consists of proofs, prompts, hyperparameters, or additional experiments labeled as appendix material.

Confirm ambiguous cutoffs visually. Two-column extraction may place a running title or appendix heading inside the conclusion text.

## Evidence discipline

- `fulltext`: cite and summarize main-text claims. Appendix material may be consulted only when the user explicitly asks for it.
- `abstract`: use only the abstract's claims. Say that implementation and experimental details could not be independently verified.
- `metadata`: state that no reliable summary can be produced without guessing.

If a paper has multiple versions, prefer the latest author/arXiv version unless the user asks for the accepted or camera-ready version.
