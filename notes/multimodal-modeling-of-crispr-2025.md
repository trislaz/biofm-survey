---
id: multimodal-modeling-of-crispr-2025
title: Multimodal Modeling of CRISPR-Cas12 Activity Using Foundation Models and Chromatin
  Accessibility Data
authors:
- Azim Dehghani Amirabad
- Yanfei Zhang
- Artem Moskalev
- Sowmya Rajesh
- Tommaso Mansi
- Shuwei Li
- Mangal Prakash
- Rui Liao
year: 2025
venue: null
arxiv: '2506.11182'
doi: null
url: https://arxiv.org/abs/2506.11182v1
pdf_path: papers/multimodal-modeling-of-crispr-2025.pdf
md_path: papers/md/multimodal-modeling-of-crispr-2025.md
modalities:
- rna
- epigenome
status: extracted
evidence_quality: peer-reviewed
tags:
- crispr
- cas12
- gRNA-activity-prediction
- transfer-learning
- probing
- chromatin-accessibility
- multimodal-fusion
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:49+00:00'
updated_at: '2026-04-22T20:23:03+00:00'
---

## TL;DR

Cas-FM uses frozen RNA-FM embeddings (a transcriptomic foundation model) as input to a lightweight CNN regressor for CRISPR-Cas12 gRNA on-target activity prediction, outperforming all baselines including DeepCpf1 (Spearman ρ=0.76 vs 0.71). Adding binary chromatin accessibility (ATAC-seq) as a second modality via element-wise multiplication further boosts performance to ρ=0.78. Key finding: domain-aligned FM pre-training (RNA-FM on transcriptomes) massively outperforms genomic DNA FM (DNABERT-2, ρ=0.49), and frozen probing suffices without fine-tuning.

## Model

- **Name**: Cas-FM (RNA-FM) / Cas-FM-CA (RNA-FM) for the multimodal variant.
- **Backbone**: RNA-FM (Chen et al., 2022) — transformer trained on transcriptomic sequences; produces 640-dim per-token embeddings. Weights are completely frozen (probing setup). Also evaluated DNABERT-2 (Zhou et al., 2024) trained on genomic DNA, which performed much worse (ρ=0.49).
- **Downstream head**: Lightweight CNN regressor adopted from DeepCpf1 (Kim et al., 2018b): Conv1D (kernel=5, 80 filters, ReLU) → AvgPool1D (pool=2) → Flatten → Dense(80) → Dense(40) → Dense(40), with dropout=0.3 between layers.
- **Chromatin encoder** (multimodal variant): Binary ATAC-seq accessibility label → Dense(40, ReLU) → element-wise multiplication with sequence features.
- **Output**: Single scalar — predicted gRNA cleavage efficiency (indel frequency).

## Data

- **Training**: HT1-1 split from Kim et al. (2018a) — ~15,000 synthetic gRNA-target constructs with experimentally measured Cas12a (Cpf1) cleavage efficiencies in HEK293T cells (lentiviral delivery, deep sequencing readout).
- **Test**: HT1-2 split — 1,290 gRNAs (same source).
- **Sequence context**: Core 20-nt gRNA extended to 34-nt or 50-nt windows centered on cleavage site. Best performance at 34-nt.
- **Chromatin accessibility**: ATAC-seq for HEK293T (GEO: GSM2902624), aligned to hg38 with Bowtie2, peaks called with MACS2, binarized at normalized signal threshold 0.001 per gRNA target locus.

## Training Recipe

- 100 epochs, Adam optimizer, lr=5×10⁻⁵, batch size 32.
- MSE loss; early stopping patience=10; ReduceLROnPlateau (patience=5, factor=0.1).
- Model selection on validation loss; final evaluation by Spearman rank correlation on held-out test set.
- FM backbone is completely frozen — only the CNN head and chromatin encoder are trained.

## Key Ablations & Design Choices

- **RNA-FM >> DNABERT-2**: RNA-FM (ρ=0.76) massively outperforms DNABERT-2 (ρ=0.49) despite both being nucleotide FMs. Attributed to RNA-FM's transcriptomic pre-training better matching gRNA modality.
- **FM embeddings >> all classical baselines**: RNA-FM probing beats handcrafted features (CINDEL ρ=0.61), one-hot linear models (Lasso ρ=0.64), boosted trees (ρ=0.66), and DeepCpf1 (ρ=0.71) which uses the same CNN architecture with one-hot input.
- **Sequence context length**: 34-nt is optimal; 20-nt (core guide only) too short (misses flanking info), 50-nt introduces noise. Consistent for both backbones.
- **Chromatin accessibility adds orthogonal signal**: Binary CA via element-wise multiplication improves RNA-FM from ρ=0.76 → ρ=0.78. Epigenomic context captures physical accessibility of the target site, complementary to sequence features.
- **Probing suffices**: No fine-tuning of the FM backbone needed; frozen embeddings + small CNN head work well on ~15K training examples.

## Reported Insights

- General-purpose RNA FMs transfer to out-of-distribution gRNA sequences (30–50 nt) despite never seeing such short sequences during pre-training.
- Domain alignment matters more than model scale: RNA-FM (transcriptomic) >> DNABERT-2 (genomic DNA) for gRNA prediction.
- Epigenomic context provides biologically meaningful complementary information: open chromatin → more accessible to Cas12 → higher cleavage efficiency.
- Moderate sequence context (34-nt) balances capturing local cleavage-relevant features (PAM-adjacent nucleotide preferences) vs. avoiding noise from irrelevant flanking sequence.

## References Worth Chasing

- **RNA-FM** (Chen et al., 2022) — backbone that works best; transcriptomic FM.
- **DNABERT-2** (Zhou et al., 2024) — DNA FM that fails here; interesting contrast case.
- **DeepCpf1** (Kim et al., 2018b) — SOTA baseline with same CNN architecture; provides the dataset.
- **gRNA-FM** (Zhou et al., 2023) — FM for Cas9 gRNA design (different system, not Cas12 activity).
- **Prakash et al., 2024** — bridging biomolecular modalities; related probing methodology.

## Notes / Open Questions

- Only one cell line (HEK293T) and one Cas12 variant tested — cross-cell-line and cross-enzyme generalization is unknown.
- No fine-tuning of the FM backbone explored — could improve results further, especially with adapter methods.
- Binary chromatin accessibility is very coarse — continuous ATAC-seq signal or additional epigenomic marks (histone modifications, methylation) could help more.
- DNABERT-2's poor performance (ρ=0.49) is striking and under-analyzed — is it tokenization (BPE vs. character-level), pre-training distribution, or embedding dimensionality?
- Relatively small dataset (~15K training examples) — unclear how the approach scales with larger CRISPR screens.
- The paper claims ICML 2025 but the contribution is primarily empirical application of existing FMs to a specific prediction task, with no new architecture or pre-training methodology.
