# Skill: Add a Paper to the Bio-FM Survey

## When to Use

Use this skill when asked to add a new paper to the bio-foundation model survey.
This includes requests like:
- "Add paper X to the survey"
- "Include this new FM paper"
- "Add arXiv:XXXX.XXXXX"
- "Add DOI:10.xxxx/xxxxx"

---

## Prerequisites

- Working directory: the survey repo root (contains `Justfile`, `notes/`, `src/`)
- Python environment: `uv sync --all-extras` (or `just env`)

---

## Step-by-Step Workflow

### 1. Identify the Paper Source

Determine if you have an **arXiv ID** or a **DOI**:
- arXiv: e.g., `2306.15006`
- DOI: e.g., `10.1038/s41592-026-03064-3`

### 2. Add the Paper Stub

**If arXiv ID is available** (preferred — fetches abstract + PDF automatically):
```bash
uv run -- python -m survey_bio_fm.scripts.add_paper \
  --arxiv <ARXIV_ID> \
  --modality <MODALITY>
```

**If only DOI is available** (fetches via OpenAlex + Europe PMC):
```bash
uv run -- python -m survey_bio_fm.scripts.add_via_pmc \
  --doi "<DOI>" \
  --title "<Full Paper Title>" \
  --year <YEAR> \
  --modality <MODALITY>
```

This creates:
- `notes/<slug>.md` — note stub with YAML frontmatter
- `papers/md/<slug>.md` — converted full text (if available)

The command prints the paper slug, e.g., `orthrus-toward-evolutionary-and-2026`.

### 3. Verify Full Text Was Fetched

Check the evidence quality:
```bash
grep 'evidence_quality' notes/<slug>.md
```

If only `abstract-only` or `metadata-only`, try fetching manually:
- Check if there's a PMC ID for the paper (search `https://pmc.ncbi.nlm.nih.gov`)
- Try fetching the bioRxiv XML directly
- For arXiv papers: fetch `https://arxiv.org/html/<arxiv_id>` for HTML full text
- As a last resort, web-fetch the paper's abstract page

> **Note**: `papers/` and `papers/md/` are **gitignored** and only available
> locally. When running as a cloud agent, fetch paper content from the web
> using the arXiv ID, DOI, or URL from the note's frontmatter.

### 4. Extract Structured Information

Read the paper's full text (from `papers/md/<slug>.md` if running locally, or
fetched from the web if running as a cloud agent) and edit `notes/<slug>.md`
to replace the body with these **exact sections** (H2 headings):

```markdown
## TL;DR
One paragraph (3-5 sentences). What is this model? What's novel?

## Model
Architecture, size, parameter count, context length, key components.

## Data
Pre-training datasets (names, sizes, sources), preprocessing, deduplication,
filtering, multi-species/strain mixing, splits.

## Training Recipe
Objective (MLM/CLM/contrastive/diffusion/...), tokenizer, batch size,
optimizer, schedule, total tokens/steps, hardware, wall-clock time.

## Key Ablations & Design Choices (MOST IMPORTANT)
Extract EVERY ablation table or design comparison reported. For each:
what was varied, what was measured, what won, by how much.
Be quantitative. This is the most important section.

## Ablations (Rev 4)
Structured table format:

| Variable | Settings | Metric/dataset | Result | Conclusion |
|----------|----------|---------------|--------|------------|
| ... | ... | ... | ... | ... |

### Take-aways
- Bullet points summarising the key ablation findings.

## Reported Insights
Authors' own takeaways about what mattered for performance.

## References Worth Chasing
Up to 15 references that are bio-FM papers worth surveying.
Format: `- <title> (<arxiv/doi>) — why relevant`

## Notes / Open Questions
Unclear claims, weak evaluations, gaps.
```

### 5. Update Frontmatter

Ensure these frontmatter fields are set correctly:

```yaml
modalities:           # One or more from VALID_MODALITIES (see below)
parameters:           # e.g., "117M", "3B" (null if not reported)
training_tokens:      # e.g., "300B tokens" (null if not reported)
training_compute:     # e.g., "64x A100 for 3 days" (null if not reported)
tags:                 # Technical keywords, e.g., [mamba, contrastive, long-context]
evidence_quality:     # "full-text", "abstract+repo", or "abstract-only"
status:               # Set to "extracted"
is_fm:                # true if this paper introduces/trains a bio-FM, false otherwise
fm_classification_reason:  # One-line reason for the classification
```

### 6. Consolidate

Rebuild the index and modality listings:
```bash
just consolidate
```

### 7. Optionally Rebuild HTML Site

```bash
just build-html
```

### 8. Commit

```bash
git add notes/<slug>.md index.json modalities.md
git commit -m "feat: add <Paper Name> to survey"
```

---

## Valid Modalities

```
dna, rna, scrna, single-cell-multiomics, protein-sequence, protein-structure,
proteomics, epigenome, interactome, imaging-pathology, imaging-radiology,
imaging-microscopy, imaging-cell, small-molecule, multimodal, other
```

**Common mappings**:
- Genomic language models → `dna`
- RNA structure/function models → `rna`
- Single-cell RNA-seq models → `scrna`
- Protein language models (sequence) → `protein-sequence`
- Protein structure prediction → `protein-structure`
- Pathology whole-slide models → `imaging-pathology`
- Cell painting / microscopy → `imaging-cell` or `imaging-microscopy`
- Models spanning multiple modalities → list each + `multimodal`

---

## Quality Checklist

Before considering a paper fully added, verify:

- [ ] TL;DR is concise (3-5 sentences) and captures what's novel
- [ ] Model section has architecture + parameter count
- [ ] Data section lists specific datasets and sizes
- [ ] Training Recipe has objective, optimizer, hardware, duration
- [ ] Key Ablations section extracts ALL reported ablations with numbers
- [ ] Ablations (Rev 4) table is present with structured columns
- [ ] `is_fm` is set correctly with a reason
- [ ] `modalities` uses valid values from the list above
- [ ] `status` is set to `extracted`
- [ ] `just consolidate` has been run

---

## FM Classification Guide

**Mark `is_fm: true` when the paper**:
- Pre-trains a model on large-scale biological data
- The model is designed to be general-purpose (fine-tuned for multiple tasks)
- Examples: ESM-2, scGPT, Enformer, DNABERT-2, Virchow, Evo

**Mark `is_fm: false` when the paper**:
- Evaluates or benchmarks existing FMs (e.g., TAPE, BEACON)
- Fine-tunes a pre-existing FM for a specific task
- Is a survey or review of FMs
- Analyses FM representations (e.g., sparse autoencoders on ESM)
- Is a single-task model, not pre-trained for general use

**Do NOT add papers that are**:
- Unrelated to foundation models in biology
- Generic ML methods (pruning, RL for aviation, etc.)
- Off-topic (astronomy, electricity, education, etc.)

---

## Example: Adding Orthrus

```bash
# 1. Add paper stub
uv run -- python -m survey_bio_fm.scripts.add_via_pmc \
  --doi "10.1038/s41592-026-03064-3" \
  --title "Orthrus: toward evolutionary and functional RNA foundation models" \
  --year 2026 --modality rna

# 2. If only metadata fetched, manually fetch PMC full text
#    (check PMC ID from the paper's DOI page)

# 3. Read papers/md/orthrus-toward-evolutionary-and-2026.md
# 4. Edit notes/orthrus-toward-evolutionary-and-2026.md with structured sections
# 5. Set is_fm: true, status: extracted
# 6. Consolidate
just consolidate

# 7. Commit
git add -A && git commit -m "feat: add Orthrus RNA FM to survey"
```
