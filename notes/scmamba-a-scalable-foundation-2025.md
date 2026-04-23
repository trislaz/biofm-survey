---
id: scmamba-a-scalable-foundation-2025
title: 'scMamba: A Scalable Foundation Model for Single-Cell Multi-Omics Integration
  Beyond Highly Variable Feature Selection'
authors:
- Zhen Yuan
- Shaoqing Jiao
- Yihang Xiao
- Jiajie Peng
year: 2025
venue: null
arxiv: '2506.20697'
doi: null
url: https://arxiv.org/abs/2506.20697v1
pdf_path: papers/scmamba-a-scalable-foundation-2025.pdf
md_path: papers/md/scmamba-a-scalable-foundation-2025.md
modalities:
- scrna
- single-cell-multiomics
status: extracted
evidence_quality: medium
tags:
- mamba
- ssm
- state-space-duality
- contrastive-learning
- patch-tokenization
- multi-omics-integration
- scRNA-seq
- scATAC-seq
- CITE-seq
parameters: null  # not reported in paper
training_tokens: null  # not reported
training_compute: null  # not reported
references_chased: false
added_at: '2026-04-22T19:37:14+00:00'
updated_at: '2026-04-22T20:25:51+00:00'
---

## TL;DR

scMamba is a Mamba2-based (state-space duality) foundation model for single-cell multi-omics integration (scRNA-seq + scATAC-seq, or + protein). It replaces the standard gene-as-token approach with a **patch-based cell tokenization** strategy (genomic regions as tokens, cells as sentences), enabling processing of all genes/peaks without HVG/HVP selection. Two modality-specific encoders are trained with a contrastive loss + cosine-similarity regularization. On multiple benchmarks it outperforms scCLIP, GLUE, CVQVAE, SCALEX, scVI, Harmony, and Scanorama, with >10% average improvement in overall integration score and near-linear runtime/memory scaling to 377k cells.

## Model

- **Architecture**: Two modality-specific encoders (one for scRNA-seq, one for scATAC-seq/protein), each a stack of L identical scMamba blocks.
- **scMamba block**: alternating Mamba2 layer + MLP, each preceded by residual connection + LayerNorm (pre-norm, distinct from standard Transformer post-norm).
- **Core operator**: State Space Duality (SSD) algorithm from Mamba2 (Dao & Gu, 2024). Simplifies state transition matrix A to scalar × identity → connection to linear attention with a 1-semiseparable causal mask L; no softmax.
- **Cell tokenization**: genes/peaks ordered by genomic coordinate → partitioned into fixed-size patches (each = a genomic region). Patches linearly projected (W ∈ R^{P×D}), plus learnable 1D positional embeddings (à la ViT).
- **Cell representation**: last token of the encoder output (causal aggregation), fed through modality-specific MLP head → cell embedding.
- **Training objective**: L = λ_con · L_con + λ_sim · L_sim. L_con is CLIP-style symmetric contrastive loss over (RNA, ATAC) pairs; L_sim is mean (1 − cosine similarity) over positive pairs.
- **No** prior HVG/HVP selection required; operates on full feature set.
- **Parameter count**: not reported.
- **Expression encoding**: non-zero RNA/protein values binned into B relative intervals across cells; ATAC binarised.

## Data

- **Training & eval datasets** (self-supervised per-dataset, no large-scale pretraining corpus):
  - SHARE-seq BMMC: 78,520 cells; 51,862 genes + 173,026 peaks (GEO GSE207308)
  - Human brain: 105,332 cells; 36,601 genes + 140,614 peaks (GEO GSE214637)
  - 10x Multiome PBMC: 9,631 cells; 29,095 genes + 107,194 peaks
  - Human fetal atlas: 377,134 cells; 36,601 genes + 1,154,464 peaks
  - CITE-seq BMMC S1: 11,126 cells; 13,953 genes + 134 proteins
  - CITE-seq BMMC S4: 15,499 cells; 13,953 genes + 134 proteins
  - 10x Multiome BMMC: 69,249 cells; 20,000 genes + 100,000-dim ATAC bins
  - Brain 3k (single-omics RNA): 3,233 cells; 36,601 genes
- Model is trained self-supervised on each dataset individually (no pre-training on external atlas).

## Training Recipe

- **Pre-training paradigm**: Self-supervised contrastive learning on paired multi-omics data.
- **Loss**: Symmetric contrastive (CLIP-style) + cosine similarity regularisation (λ_con, λ_sim balance the two).
- **Preprocessing**: RNA normalised per-cell + log1p; ATAC binarised; protein used raw. Expression values binned for RNA/protein.
- **Hyperparameters**: Not reported in main text (embedding dim D, number of layers L, patch size P, learning rate, optimizer, batch size, epochs not specified — presumably in supplementary/code).
- **Hardware / compute**: Not reported.
- **No large-scale pre-training**: the model is trained from scratch on each evaluation dataset.

## Key Ablations & Design Choices (MOST IMPORTANT — esp. SSM vs Transformer)

### Why Mamba2 / SSD over Transformer?
- The SSD algorithm draws a formal connection between SSMs and attention: the output can be written as y = Mx where M = L ⊙ (CB⊤), with L a 1-semiseparable causal mask. This is linear attention **without softmax**.
- **No softmax** avoids the "attention sink" phenomenon (Xiao et al. 2023; Darcet et al. 2023) — attention concentrates on a few tokens. The mask L provides variable weighting without this collapse.
- **Computational efficiency**: SSD simplifies the state transition matrix A → scalar × I, yielding efficient training/inference that scales near-linearly (demonstrated up to 300k cells in Fig 3c where runtime and memory scale linearly).
- **No explicit ablation comparing Mamba2 vs Transformer encoder** is reported in this paper. The architectural choice is motivated by efficiency and the SSD–attention duality argument, but there is no head-to-head swap experiment.

### Key ablation: raw features vs. HVG/HVP selection
- Using all genes and peaks is strictly better than selecting 4k HVGs + 8k HVPs or 8k HVGs + 16k HVPs (Supplementary Table 1). Other methods (except scCLIP, which improves slightly) do not benefit from more features.
- This validates the core claim: scMamba's patch tokenization + Mamba2 encoder can exploit full-dimensional sparse data where Transformer-based / VAE baselines cannot.

### Contrastive loss ablation
- The paper introduces cosine similarity regularisation (L_sim) on top of standard contrastive loss (L_con). The discussion states it improves alignment, but a formal ablation table is not provided in the main text.

### Patch-based tokenization vs. gene-as-token
- Prior single-cell foundation models (scGPT, scBERT, scFoundation) treat each gene as a token, limiting inputs to ~2,000 genes.
- Patch tokenization groups features by genomic region, preserving positional information and enabling processing of tens of thousands of features (e.g., 173k peaks).

### Cell representation: last token vs. CLS / mean pooling
- Causal mask means only the last token has access to all preceding tokens. Last-token representation is used (no CLS token appended).

## Reported Insights

- scMamba achieves >10% average improvement in overall integration score across all benchmark datasets.
- ~90% improvement in matching score vs. CVQVAE at single-cell alignment.
- Runtime and memory scale near-linearly to 300k cells; GLUE requires ~55 h and 268 GB for 300k cells, while scMamba is dramatically cheaper.
- Cell type annotation: outperforms scGPT and CellPLM on accuracy, precision, recall, F1 across CITE-seq and Brain datasets.
- Trajectory conservation: highest scores on 10x Multiome BMMC erythroid differentiation trajectory.
- Pre-norm (LayerNorm before Mamba2/MLP) is used instead of post-norm, claimed to improve efficiency via adaptive input scaling.

## References Worth Chasing

- **Dao & Gu (2024)** — "Transformers are SSMs" (arXiv 2405.21060): the core Mamba2/SSD algorithm this model builds on.
- **scCLIP (Xiong et al., NeurIPS 2023 workshop)** — closest baseline; also uses contrastive learning for scRNA+scATAC but with a Transformer.
- **GLUE (Cao & Gao, 2022, Nature Biotechnology)** — graph-linked embedding with adversarial training; strong but computationally expensive baseline.
- **CVQVAE (Liu et al., 2022, PMLR)** — cross-trained VQ-VAE; second-best on some metrics.
- **scGPT (Cui et al., 2024, Nature Methods)** — Transformer-based single-cell FM; compared on annotation.
- **CellPLM (Wen et al., 2023)** — another cell FM; compared on annotation.
- **ViM (Zhu et al., 2024)** — Vision Mamba; inspiration for patch tokenization + positional embeddings.

## Notes / Open Questions

- **No head-to-head SSM vs. Transformer ablation**: the paper motivates Mamba2 on efficiency + SSD–attention duality, but never swaps the encoder backbone to a standard Transformer to quantify the architecture effect. This is the biggest gap for the survey's "architecture choice" angle.
- **No pre-training at scale**: despite being called a "foundation model," scMamba is trained from scratch on each downstream dataset. There is no large-scale pre-training corpus or transfer learning evaluation.
- **Parameter count / hyperparameters not reported** in the main text — embedding dim D, number of layers L, patch size P, learning rate, optimizer, batch size, and epochs are not specified.
- **Training compute not reported** — no GPU type, wall-clock training time, or FLOPs estimates.
- **Contrastive loss ablation**: L_sim (cosine regularisation) is described but a clean ablation (L_con only vs. L_con + L_sim) is not shown in the main text.
- **Single-omics generalisation**: the paper shows one cross-modal transfer experiment (multi-omics reference → scRNA-only query for brain 3k), but broader single-omics fine-tuning or zero-shot transfer is not explored.
- **Causal mask direction**: genes/peaks are ordered by genomic coordinate and processed causally (left→right). No bidirectional variant (cf. Vision Mamba) is explored; effect of ordering direction is unknown.
- Evidence quality rated **medium**: strong benchmark coverage (7 baselines × 8 datasets) with appropriate metrics, but missing ablation depth (no backbone swap, no hyperparameter sensitivity) and no pre-training at scale.
