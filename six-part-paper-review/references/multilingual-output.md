# Multilingual output

Read this file when the requested output language differs from the paper language or when more than one output language is requested.

## Language selection

1. Follow explicit language requests.
2. Otherwise use the language of the user's request.
3. Represent languages with BCP-47 tags such as `en`, `zh-CN`, `zh-TW`, `ja`, `ko`, `de`, or `fr`.
4. When several languages are requested, list one primary language first and keep the same paper order in every language.

## Shared evidence, separate prose

Build one language-neutral evidence map, method trace, and experiment trace. Generate each language version from this shared packet. Do not independently reinterpret the paper for each language.

Prefer direct synthesis in the target language. If translation is necessary, translate the synthesized meaning rather than source sentences, then verify the translation against the shared evidence packet.

## Terminology

- Keep the original paper title unless the user requests a translated subtitle.
- Preserve equations, variables, model names, benchmark names, dataset names, metric names, code identifiers, and URLs.
- Define abbreviations on first use in each language.
- Maintain a per-paper terminology map for recurring technical terms.
- Use established field terminology when available; avoid literal translations that change technical meaning.

## Cross-language consistency

Check that every language version has:

- the same evidence level and claim boundary;
- the same central Idea;
- the same method stages and equation meanings;
- the same experimental numbers and interpretations;
- the same limitations.

Language versions may differ in sentence structure and explanatory detail needed for fluency, but they must not introduce different scientific claims.
