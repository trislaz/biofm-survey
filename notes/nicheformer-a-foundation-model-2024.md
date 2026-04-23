---
id: nicheformer-a-foundation-model-2024
title: 'Nicheformer: a foundation model for single-cell and spatial omics'
authors: []
year: 2024
venue: null
arxiv: null
doi: 10.1101/2024.04.15.589472
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/nicheformer-a-foundation-model-2024.md
modalities:
- scrna
status: abstract-only
evidence_quality: abstract+metadata
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: Added in rev4 missing-FM brainstorm; canonical bio-FM.
---

## Ablations (Rev 4)

Sources: Schaar, Tejada-Lapuerta et al., *Nature Methods* 2025 (s41592-025-02814-z) — main text + Extended Data Figs. 1–8 + Supp. Note 1; GitHub `theislab/nicheformer` (`_train.py`, `_fine_tune.py`); preprint biorxiv 2024.04.15.589472 inaccessible (Cloudflare 403), so peer-reviewed version used as primary.

| # | Axis | Variants compared | Setup | Result | Take-away |
|---|------|-------------------|-------|--------|-----------|
| 1 | Pretraining modality mix | dissociated-only (1× and 3× spatial volume) vs joint dissociated+spatial | Same arch / token budget; eval on spatial downstream tasks (niche, region, density) | Dissociated-only models underperform across all downstream tasks even with 3× more cells (ANOVA, FDR-adj.; Ext. Data Fig. 2a,b) | Spatial pretraining data is non-substitutable — scale of dissociated cells alone cannot recover spatial variation |
| 2 | Cross-species pretraining | human-only vs mouse-only vs both, equal cell counts | Joint vocab of 20,310 ortholog+species tokens; eval per-organism | Single-organism models fail on missing organism; both-species best (Ext. Data Fig. 2c) | Diversity > raw count; orthology-aligned multi-species pretraining is required |
| 3 | Model size / hyperparams | smaller depth/width variants vs final 12-layer × 16-head, d=512, FFN=1024 (49.3 M params) | MLM pretraining; downstream macro-F1 | Final config wins; smaller models lose on niche/region tasks (Ext. Data Fig. 2c, Supp. Table 1) | Capacity matters at SpatialCorpus-110M scale |
| 4 | Rank tokenizer robustness | Full gene panel vs simulated incomplete panels (random gene drop) | Perturb input rank sequence; compare embeddings | Embeddings stable under panel reduction (Ext. Data Fig. 1a,b) | Rank-based encoding tolerates the limited-gene reality of MERFISH/Xenium/CosMx |
| 5 | Transfer regime | Linear probe (frozen) vs full fine-tune vs PCA / scVI / Geneformer / scGPT / UCE / CellPLM probes | Held-out MERFISH brain, CosMx liver, CosMx/Xenium lung, Xenium colon | Fine-tune > linear probe > all baselines on niche+region; linear probe already ≥ baselines on brain (Fig. 4b, Ext. Data Fig. 6) | Embedding alone is competitive; fine-tuning closes remaining gap, esp. on under-represented tissues |
| 6 | Pretraining-data subset size | Full vs 1% vs 3% dissociated subsamples | Liver downstream (under-represented tissue) | 1% subset slightly beat 3% subset; both better than expected on liver linear-probe drop (Supp. Note 1) | "Compute per sample" effect: more passes over fewer cells can beat more cells with fewer passes |
| 7 | Tissue-balanced extended pretraining | Base Nicheformer vs base + extra liver pretraining | CosMx human liver niche prediction | Extended pretraining recovers linear-probe gap vs scVI/PCA on liver (Ext. Data Fig. 8f) | Targeted continued pretraining is the recommended fix for under-represented tissues |
| 8 | Baseline embedding source | scVI / PCA trained on **full SpatialCorpus 1% subset** vs **only target dataset training split** | Linear probe on niche/region | Target-dataset-trained baselines stronger; PCA with many PCs ≈ Nicheformer linear probe on region, still < fine-tune (Ext. Data Fig. 7a,b) | Naïve large-corpus scVI/PCA is not a free win — Nicheformer's gain comes from joint multimodal pretraining, not just data scale |

**Count: 8 ablation axes.**

**Top take-away:** The single most-emphasized finding is **#1**: jointly pretraining on dissociated + spatial transcriptomics is irreplaceable — adding 3× more dissociated cells does *not* substitute for spatial data on any spatial downstream task, establishing that modality diversity (not just cell count) is the dominant scaling axis for spatially-aware single-cell foundation models.
