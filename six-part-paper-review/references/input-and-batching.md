# Input, batching, and recovery

Read this file for two or more papers, publication pages, mixed sources, or resumable jobs.

## Accepted inputs

- one local PDF or one paper URL;
- several PDFs, arXiv URLs, DOI URLs, or proceedings pages;
- JSON or CSV metadata lists;
- an author or lab publication page;
- an existing summary document paired with source papers.

Normalize each item into a paper record with `title`, `authors`, `year`, `venue`, `categories`, `identifiers`, `source_url`, and `local_pdf_path` when known.

## Deduplication

Use this identity order:

1. normalized arXiv ID;
2. normalized DOI;
3. normalized title plus first author;
4. normalized title alone, with a warning if author data conflicts.

Merge categories and alternate source URLs. Preserve the best source and record alternates. Never silently merge papers with materially different titles, authors, or years.

## Execution modes

- **One paper:** read and deliver directly; a manifest is optional.
- **Two to five papers:** one batch by default; still process papers sequentially within the task.
- **Six to twenty-five papers:** default to batches of five and checkpoint each batch.
- **More than twenty-five papers:** create a manifest, run a representative pilot when quality has not already been established, then use resumable batches.

Reduce batch size for long, mathematical, multimodal, or extraction-damaged papers. Batch size controls recovery units, not summary depth.

## Context discipline

Do not concatenate every full text into one prompt. For each paper:

1. load metadata and its own source material;
2. read the complete selected scope;
3. build its evidence packet;
4. draft and validate its review;
5. release unnecessary raw context before the next paper when the environment permits.

## Manifest and states

Use `scripts/init_review_job.py` to create a deterministic job manifest from a JSON paper list. Paper states are:

- `pending`;
- `source_resolved`;
- `evidence_ready`;
- `drafted`;
- `validated`;
- `unavailable`;
- `failed`.

Resume from the first non-validated paper. Do not regenerate `validated` items unless their source, requested language, content scope, or schema version changed.

## Batch artifacts

Name batch files with stable ordinal ranges, for example `batch_0001_0005.json`. Store the original order in `ordinal` and a stable `paper_id`. Merge batches using the manifest order, not filesystem timestamps.

Record unavailable papers rather than dropping them. A missing source should not block other papers.
