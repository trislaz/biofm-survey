# survey-bio-fm

An **exhaustive, evolvable survey of bio-foundation models** across all biological
modalities (DNA, RNA, protein, proteomics, epigenome, interactome, single-cell,
imaging — pathology / cell / microscopy, multimodal combinations).

The survey is built to answer:

> **What are the most impactful design choices for training bio-foundation models?**

**👉 The synthesis lives in [`insights.md`](./insights.md)** — a guidebook
organised by design-choice axis (tokenisation, architecture, objective, context
length, data, multimodal fusion, conditioning, optimisation, scaling, evaluation
caveats) plus modality-specific "would-build-today" recipes.

Current state: **142 papers (85 bio-FMs + 57 FM-related support papers)** across
DNA, RNA, protein, scRNA, single-cell-multiomics, imaging-pathology,
cell-painting, mass-spec proteomics, multimodal medical, small molecules, and more.

---

## 💬 Contributing via GitHub Issues

**You can interact with this survey using GitHub issues!** A Copilot agent
monitors issues and can:

- **🔍 Answer questions** — Ask about a specific paper, design choice, or
  insight. Example: *"What does Orthrus say about contrastive vs MLM for RNA?"*
- **📄 Request a paper addition** — Ask to add a new bio-FM paper to the survey.
  Example: *"Please add arXiv:2501.12345 to the survey"*
- **🔄 Challenge an insight** — Point out new evidence that updates an existing
  finding. Example: *"Is the MLM-vs-AR insight still valid given paper X?"*

Answers are recorded in the [`qa/`](./qa/) folder for future reference, and
brief inline annotations are added to the relevant documents.

---

Output artifacts (committed):

- `notes/<id>.md` — one structured markdown note per paper (YAML frontmatter +
  TL;DR / Model / Data / Training Recipe / **Key Ablations & Design Choices** /
  Reported Insights / References-worth-chasing / Notes).
- `index.json` — flat machine-readable index of all papers (regenerated).
- `modalities.md` — per-modality summary table (regenerated).
- `insights.md` — the **guidebook** organized by design-choice axis (regenerated).

Non-committed (gitignored):

- `papers/` — downloaded PDFs.
- `papers/md/` — docling-converted markdown of the PDFs (what extraction agents
  read).
- `.cache/` — search results, reference triage outputs.

## Setup

```bash
cd survey-bio-fm
just env                # uv sync --all-extras (installs docling)
```

GPU is highly recommended for docling's VLM pipeline; on CPU the script falls back
to plain docling, then to `pdfplumber` / `pypdf`.

## Quality gates

```bash
just format    # ruff format
just lint      # ruff check --fix
just types     # pyright
just check     # all of the above
just test      # pytest
```

## Adding a new bio-FM paper

**Preferred method: open a GitHub issue.** Simply create an issue with the
paper's arXiv ID, DOI, or title — a Copilot agent will pick it up, add the
paper, extract structured information, update insights if warranted, and
submit a PR. Example issue title:

> *"Add paper: arXiv:2501.12345 — Orthrus RNA foundation model"*

### Manual method (local development)

If you're working locally, you can also add a paper directly:

```bash
cd survey-bio-fm
just add --arxiv 2501.12345           # or --doi 10.1038/...  or --url https://...
just consolidate                      # regenerate index.json, modalities.md, insights.md
```

Under the hood `add_paper.py`:

1. Resolves metadata (arxiv / Crossref).
2. Downloads the PDF to `papers/<id>.pdf`.
3. Converts to markdown at `papers/md/<id>.md` (docling VLM → docling → pdfplumber → pypdf).
4. Spawns an opus-4.6 extraction agent that fills `notes/<id>.md` per
   `schema/paper.schema.json`.
5. (Optional) `just refs <id>` chases that paper's references for further
   candidates.

## Pipeline overview

```
search_seeds  →  fetch_paper (pdf + md)  →  chase_refs ↺  →  extract_paper  →  consolidate
                                            ↑___________________________|
```

All per-paper steps are **idempotent** — they skip work for papers already at the
target `status`. Reference-chasing and extraction are dispatched as **parallel
opus-4.6 background agents** in batches.

## Schema

See `schema/paper.schema.json` for the per-paper YAML-frontmatter schema. Status
values:

- `seed` — only title + arxiv/doi known.
- `fetched` — PDF downloaded.
- `converted` — markdown produced.
- `extracted` — full note populated.
- `abstract-only` / `paywalled-no-mirror` — limited evidence; flagged as such in
  the consolidated guidebook.
- `extraction-failed` — see `notes/<id>.md` for the failure reason.

## Project conventions

Follows the parent monorepo's conventions:

- Python 3.11, `uv` for env management, `just` for automation.
- Ruff (format + lint), Pyright (types), pytest.
- Type-annotated functions, `pathlib.Path` for paths, small focused functions.
