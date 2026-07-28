# Codex Skills

Reusable skills for Codex.

## Included skill

### `six-part-paper-review`

Reads academic papers and reconstructs each paper as six connected sections:

1. problem background;
2. motivation;
3. core idea;
4. implementation-level method, including essential equations;
5. experiments and what they demonstrate;
6. conclusion.

It supports five-paper pilot batches, evidence grading, main-text cutoffs before appendices and references, clickable arXiv links, JSON quality checks, and LaTeX-to-PDF delivery.

## Install

Copy the skill directory into your Codex skills directory:

```text
~/.codex/skills/six-part-paper-review
```

Restart Codex after installation so the skill is discovered.

## Contents

- `SKILL.md`: core workflow and output requirements.
- `agents/openai.yaml`: UI metadata.
- `references/`: evidence, schema, and quality-gate guidance.
- `scripts/validate_six_part_json.py`: deterministic summary-batch validator.
