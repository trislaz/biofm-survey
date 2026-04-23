"""Prompt templates for opus sub-agents (extraction & reference triage)."""

from __future__ import annotations

EXTRACTION_PROMPT = """You are a domain expert performing a literature survey of bio-foundation models.

Your task: read the paper markdown at `{md_path}` and produce a structured note at
`{note_path}` for the paper with id `{paper_id}` (title: "{title}").

The repository root is `{repo_root}`. The note file already exists with YAML
frontmatter (created by the pipeline). You MUST:

1. Read `{md_path}` in full (use multiple `view` calls if large).
2. Edit `{note_path}` so the YAML frontmatter has correct values for:
   - `modalities` (one or more of: dna, rna, protein-sequence, protein-structure,
     proteomics, epigenome, interactome, scrna, single-cell-multiomics,
     imaging-cell, imaging-pathology, imaging-microscopy, imaging-radiology,
     small-molecule, multimodal, other)
   - `parameters` (e.g. "117M", "3B"), `training_tokens`, `training_compute`
     (any of these may be left null if not reported)
   - `tags` (short technical keywords: e.g. ["mlm", "byte-pair", "long-context"])
   - `evidence_quality`: "full-text" if you fully read the paper; "abstract+repo"
     if only abstract+code; "abstract-only" if even less.
   - `status`: set to "extracted" on success.
3. Replace the markdown body with these sections (use exactly these H2 headings):

   ## TL;DR
   One paragraph (3-5 sentences). What is this model, what's novel?

   ## Model
   Architecture, size, parameter count, context length, key components.

   ## Data
   Pretraining datasets (names, sizes, sources), preprocessing, deduplication,
   filtering, multi-species/strain mixing, splits.

   ## Training Recipe
   Objective (MLM/CLM/contrastive/diffusion/span-corruption/...), tokenizer,
   batch size, optimizer, schedule, total tokens / steps, hardware, wall-clock.

   ## Key Ablations & Design Choices
   THIS IS THE MOST IMPORTANT SECTION. Extract every ablation table or design
   comparison reported. For each: what was varied, what was measured, what won,
   by how much. Be quantitative where possible. Bullet points are fine.

   ## Reported Insights
   Authors' own takeaways about what mattered for performance.

   ## References Worth Chasing
   List up to 15 references that look like other bio-FM papers worth surveying.
   Format as bullets: `- <title> (<arxiv id or doi if visible>) — why relevant`.

   ## Notes / Open Questions
   Anything unclear, weak claims, evaluation pitfalls, gaps.

4. Do NOT remove or rename frontmatter fields you don't change.
5. Do NOT modify any file other than `{note_path}`.

Be concise but technically dense. Quote numbers (params, FLOPs, tokens) when
reported. If you cannot read the markdown (file missing or empty), set
`status: extraction-failed` and write a one-line failure reason in the body.
"""


REF_CHASE_PROMPT = """You are helping build an exhaustive survey of bio-foundation models.

Read the paper markdown at `{md_path}` for paper `{paper_id}` (title: "{title}").
Identify references that are themselves *bio-foundation model papers* across
ANY modality (DNA, RNA, protein, proteomics, epigenome, interactome, scRNA,
imaging — pathology / cell / microscopy, multimodal). Exclude application
papers, benchmarks, and non-FM methods.

When in doubt about a reference, briefly look up its abstract (web_fetch on
arxiv/biorxiv abstract page) and decide based on whether it pretrains a
foundation model on biological data.

Write your output as a JSON array to `{out_path}` with this schema:

[
  {{
    "title": "...",
    "arxiv": "2306.15006" | null,
    "doi": "10.1038/..." | null,
    "url": "https://..." | null,
    "modalities": ["dna", ...],
    "why": "one-sentence justification"
  }},
  ...
]

Only include high-confidence bio-FM references. Aim for 5-30 entries depending
on the paper. After writing the file, also update `{note_path}` frontmatter to
set `references_chased: true`.
"""


def render_extraction_prompt(
    *, paper_id: str, title: str, md_path: str, note_path: str, repo_root: str
) -> str:
    return EXTRACTION_PROMPT.format(
        paper_id=paper_id,
        title=title,
        md_path=md_path,
        note_path=note_path,
        repo_root=repo_root,
    )


def render_ref_chase_prompt(
    *, paper_id: str, title: str, md_path: str, note_path: str, out_path: str
) -> str:
    return REF_CHASE_PROMPT.format(
        paper_id=paper_id,
        title=title,
        md_path=md_path,
        note_path=note_path,
        out_path=out_path,
    )
