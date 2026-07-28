# Output schema

Use this structure for batch processing and deterministic validation:

```json
{
  "papers": [
    {
      "title": "Original English title",
      "authors": ["Author One", "Author Two"],
      "year": 2026,
      "venue": "Venue or status",
      "categories": ["Category"],
      "source_url": "https://arxiv.org/abs/0000.00000",
      "evidence": "fulltext",
      "summary": {
        "background": "One coherent paragraph.",
        "motivation": "One coherent paragraph.",
        "idea": "One coherent paragraph stating the reconstructed core insight in fresh language.",
        "method": "A connected implementation-level explanation; may contain valid LaTeX equations and compact numbered stages.",
        "experiments": "One coherent paragraph.",
        "conclusion": "One coherent paragraph."
      }
    }
  ]
}
```

Valid evidence values are `fulltext`, `abstract`, and `metadata`.

For a LaTeX deliverable, keep the same ordering. A minimal per-paper structure is:

```latex
\subsection{Original English title}
\noindent\textbf{Source:} \href{https://arxiv.org/abs/0000.00000}{arXiv}
\quad \textbf{Evidence:} fulltext

\subsubsection*{问题背景}
...
\subsubsection*{Motivation｜为什么要解决}
...
\subsubsection*{Idea｜核心思想}
...
\subsubsection*{Method｜实现流程}
... 公式、符号定义和流程解释 ...
\subsubsection*{实验｜做了什么、说明什么}
...
\subsubsection*{结论}
...
```
