---
id: cellpaintr-generalizable-representation-learning-2025
title: 'CellPainTR: Generalizable Representation Learning for Cross-Dataset Cell Painting
  Analysis'
authors:
- Cedric Caruzzo
- Jong Chul Ye
year: 2025
venue: null
arxiv: '2509.06986'
doi: null
url: https://arxiv.org/abs/2509.06986v1
pdf_path: papers/cellpaintr-generalizable-representation-learning-2025.pdf
md_path: papers/md/cellpaintr-generalizable-representation-learning-2025.md
modalities:
- imaging-cell
- cell-profiling
status: extracted
evidence_quality: full-text
tags:
- transformer
- hyena-operator
- cell-painting
- batch-correction
- contrastive-learning
- representation-learning
- OOD-generalization
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:18+00:00'
updated_at: '2026-04-22T20:17:42+00:00'
is_fm: true
fm_classification_reason: 'CellPainTR: self-supervised pretrained transformer for
  Cell Painting.'
---

## TL;DR

CellPainTR is a Transformer-based model (4 Bidirectional Hyena layers, d_model=256) that learns batch-corrected, generalizable representations of Cell Painting morphological features (CellProfiler feature vectors, not raw images). It uses learnable source-context tokens to condition on data provenance and a 3-stage training curriculum (self-supervised masked feature prediction → intra-source contrastive → inter-source contrastive). On the JUMP cpg-0016 dataset it achieves Overall 0.60 vs 0.56 (Harmony/Baseline) and 0.54 (ComBat). On a fully unseen OOD dataset (Bray et al.) with only 275/4765 features available, it scores Overall 0.40 vs 0.26 (Baseline/ComBat) without any fine-tuning.

## Model

- **Architecture**: Transformer encoder with 4 stacked Bidirectional Hyena operator layers (near-linear complexity, replacing quadratic self-attention). d_model = 256; 3 recurrences per Hyena layer.
- **Input**: CellProfiler morphological feature vectors (4,765 features from JUMP). Each feature is independently linearly projected to d_model via a per-feature Linear Adaptor (Eq. 6). Feature Context Embeddings (learnable, per-feature) replace positional encoding (Eq. 7).
- **Special tokens**: A learnable `[SRC]` source-context token (from a codebook of K sources) is prepended alongside a `[CLS]` token. The `[CLS]` output (256-dim) is the final cell-profile embedding.
- **Output**: 256-dimensional cell profile embedding.
- **Parameter count**: Not reported explicitly. Model is relatively small (4 layers, d_model=256).

## Data

- **In-distribution**: JUMP Cell Painting consortium 'cpg-0016' dataset — >100k compound and genetic perturbations from multiple sources. Compound-only perturbations used; supervised stages further curated to compounds with known MoA.
- **OOD evaluation**: Bray et al. (2017) dataset — entirely unseen during training, different lab, older CellProfiler version (1,383 features vs 4,765). Only 275 overlapping features; remaining zero-padded.
- **Preprocessing**: zero imputation for NaN/inf → per-plate MAD normalization against negative controls (DMSO) → clipping to [0.01, 0.99] quantile range.

## Training Recipe

Three-stage curriculum, all using AdamW optimizer:

1. **Step 1 — Self-supervised pre-training (CWMM)**: Channel-Wise Masked Morphology. Random masking of feature groups (grouped by channel × compartment) with mask probability ∈ [0.05, 0.4]. MSE reconstruction loss. LR=1e-4, batch size=16. Uses all compound data.
2. **Step 2 — Intra-source supervised fine-tuning**: Supervised contrastive loss (SupCon, τ=0.1) on InChIKey labels + CWMM loss, equal weight (Eq. 10). Each batch from a single source only. LR=1e-5, batch size=32. Uses curated compounds with known MoA.
3. **Step 3 — Inter-source supervised fine-tuning**: SupCon loss only (no CWMM). Batches now mix multiple sources; source-context tokens optimized. LR=1e-5, batch size=64, τ=0.1.

## Key Ablations & Design Choices

- **Training stage ablation** (Table 1, in-distribution JUMP):
  - CellPainTR(1) (CWMM only): BatchCorr agg=0.75, BioMetrics agg=0.33, Overall=0.54 — strong batch correction, weak bio signal.
  - CellPainTR(2) (+intra-source SupCon): BatchCorr=0.68, BioMetrics=0.49, Overall=0.58 — Silh. Label jumps 0.52→0.70; batch correction capacity drops.
  - CellPainTR (full, +inter-source): BatchCorr=0.76, BioMetrics=0.45, Overall=0.60 — recovers batch correction while maintaining bio quality. Best overall.
- **OOD ablation** (Table 2, Bray et al.):
  - CellPainTR(1): Overall=0.35; CellPainTR(2): 0.39; CellPainTR (full): 0.40.
  - All CellPainTR stages outperform baselines (Baseline/ComBat/Harmony all ≤0.26) even with 275/4765 features and zero fine-tuning.
- **Source-context token proxy strategy**: For OOD, the most metadata-similar JUMP source token ('Source 10') is used as proxy — no retraining needed.
- **Hyena operator choice**: Bidirectional Hyena enables near-linear complexity for the ~4,765-token feature sequence, making the Transformer feasible. Removes causal constraint (non-sequential biological features).
- **Feature mismatch handling**: Zero-padding for missing features at test time (275→4,765) — model is robust to ~94% feature dropout.

## Reported Insights

- Classical batch correction methods (ComBat, Harmony) are static correctors that must be re-run from scratch when new data arrives; CellPainTR is a reusable, forward-pass model.
- There is an inherent trade-off between batch correction and biological signal preservation; the 3-stage curriculum systematically navigates this.
- High Graph Connectivity scores for uncorrected baselines are misleading — batch effects create artificially distinct per-batch clusters that inflate the metric.
- Operating on CellProfiler feature space (rather than raw images) provides biological interpretability anchor.
- Authors position CellPainTR as a "Cell-BERT" proof-of-concept for cumulative cellular morphology atlases.

## References Worth Chasing

- **Arevalo et al. 2024** — Benchmark for evaluating batch correction in image-based cell profiling (Nature Communications); metrics protocol used here.
- **Oh et al. 2023 (scHyena)** — Foundation model for single-cell RNA-seq using Bidirectional Hyena; architectural inspiration for CellPainTR.
- **Seal et al. 2024** — Feature context embedding approach for Cell Painting (BioMorph features).
- **Kraus et al. 2024** — Masked autoencoders for microscopy (MAE-based, operates on raw images; contrasts with CellPainTR's feature-space approach).
- **Chandrasekaran et al. 2023** — JUMP Cell Painting dataset documentation.
- **Poli et al. 2023** — Hyena Hierarchy (original Hyena operator paper).

## Notes / Open Questions

- No explicit parameter count reported; the model appears small (4 layers, 256-dim) but exact number is unclear.
- Proxy-based source token assignment for OOD is manual (metadata matching); authors acknowledge need for automatic source inference.
- Evaluation limited to ComBat, Harmony, Sphering baselines — no comparison with other deep-learning methods (e.g., scVI, MAE-based approaches).
- The trade-off between batch correction and bio signal is task-dependent; optimal curriculum stage may vary by downstream application.
- Code available at https://github.com/CellPainTR/CellPainTR — worth checking for architecture details and parameter count.
- Only compound perturbations used for training/eval; generalization to genetic perturbations (ORF, CRISPR) not tested.

## Ablations (Rev 4)

Source: §4.4 "Ablation Study: Dissecting the Training Stages" (Table 1, in-distribution benchmark). Each row is a successive training stage of the same model; baselines (no model / ComBat / Harmony) included for reference.

| Variant | Training stage / change | Graph Conn. | Silh. Batch | Batch Corr. (agg.) | Leiden NMI | Leiden ARI | Silh. Label | mAP | Bio Metrics (agg.) | Overall | Take-away |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Baseline (raw) | No correction | 0.12 | 0.58 | 0.63 | 0.08 | 0.01 | 0.18 | 0.05 | 0.08 | 0.26 | Reference floor. |
| ComBat | Classical batch correction | 0.08 | 0.65 | 0.54 | 0.09 | 0.01 | 0.27 | 0.05 | 0.11 | 0.26 | No overall gain vs baseline. |
| Harmony | Classical batch correction | 0.11 | 0.58 | 0.61 | 0.08 | 0.01 | 0.18 | 0.05 | 0.08 | 0.25 | No overall gain vs baseline. |
| CellPainTR (1) | Stage 1 only: self-supervised pre-training (masked feature reconstruction) | 0.15 | 0.76 | 0.82 | 0.08 | 0.01 | 0.34 | 0.05 | 0.12 | 0.35 | Strong batch correction but weak biological signal. |
| CellPainTR (2) | + Stage 2: intra-source contrastive learning | 0.32 | 0.82 | 0.82 | 0.13 | 0.02 | 0.36 | 0.06 | 0.14 | 0.39 | Boosts bio metrics (Silh. Label 0.52→0.70 per text) at slight cost to batch correction. |
| CellPainTR (full) | + Stage 3: inter-source contrastive learning | 0.32 | 0.82 | 0.85 | 0.16 | 0.03 | 0.33 | 0.07 | 0.15 | 0.40 | Best overall — recovers batch correction (0.76 agg per text) while keeping bio signal. |

**Count:** 6 ablation/comparison rows (3 training-stage ablations + 3 baseline references).

**Top take-away:** The multi-stage curriculum is essential and exposes a fundamental trade-off — Stage 1 (SSL) maximizes batch correction but discards biological structure; Stage 2 (intra-source contrastive) reverses the trade-off; only the full three-stage curriculum (adding inter-source contrastive) strikes the balance, yielding the best overall score (0.40) and showing that no single objective alone is sufficient.
