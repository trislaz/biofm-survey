---
id: a-deep-generative-model-2017
title: A deep generative model for gene expression profiles from single-cell RNA sequencing
authors:
- Romain Lopez
- Jeffrey Regier
- Michael Cole
- Michael Jordan
- Nir Yosef
year: 2017
venue: null
arxiv: '1709.02082'
doi: null
url: https://arxiv.org/abs/1709.02082v4
pdf_path: papers/a-deep-generative-model-2017.pdf
md_path: papers/md/a-deep-generative-model-2017.md
modalities:
- scrna
status: extracted
evidence_quality: full-text
tags:
- vae
- scRNA-seq
- zero-inflated-negative-binomial
- variational-inference
- imputation
- differential-expression
- dimensionality-reduction
parameters: not reported
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T21:55:20+00:00'
updated_at: '2026-04-22T21:55:20+00:00'
---

## TL;DR

scVI (Single-cell Variational Inference) is a deep generative model for scRNA-seq data that uses a variational autoencoder with a zero-inflated negative binomial observation model. It explicitly models technical dropout and batch effects via latent variables and neural-network-parameterized conditional distributions, enabling scalable probabilistic inference. The model scales to 1.3 million cells (training in <2 hours on one GPU) while methods like ZIFA and ZINB-WaVE fail at 100k cells, and outperforms them on held-out likelihood, imputation, clustering, and differential expression tasks.

## Model

Architecture is a VAE. The **encoder** maps observed gene expression x_n (plus optional batch covariates γ_n) to a Gaussian variational posterior q(z_n | x_n) with diagonal covariance over a 10-dimensional latent space. The **decoder** consists of two neural networks with shared weights: f_w (parameterizes Gamma-distributed expression levels) and f_h (parameterizes Bernoulli dropout indicators). Each decoder network has 3 fully connected layers with 128 nodes each, using ReLU, exponential, and linear activations, with dropout regularization and batch normalization. The generative model factorizes as: z_n ~ N(0,I), w_ng ~ Gamma(f_w(z_n, γ_n)), y_ng ~ Poisson(w_ng), h_ng ~ Bernoulli(f_h(z_n, γ_n)), with x_ng = y_ng if h_ng=0, else 0. The conditional distribution p(x_ng | z_n) is a zero-inflated negative binomial (ZINB). Total parameter count is not reported; the architecture is small (order of tens of thousands of parameters given 128-node layers and weight sharing).

## Data

Three datasets used for benchmarking:
1. **10x Genomics 1.3M brain cells** (E18 mice): up to 1.3M cells, 720 sampled variable genes. Subsampled to 4k, 10k, and 100k for comparisons. Used for held-out likelihood and imputation tasks.
2. **Mouse cortex** (Zeisel et al. 2015): 3,005 cells, 7 cell types, 558 variable genes. Used for clustering (silhouette) evaluation.
3. **PBMC** (Zheng et al. 2017): 12,039 peripheral blood mononuclear cells, 10,310 sampled genes, with Seurat-based cell classification. Used for clustering with batch/QC correction and differential expression.

No explicit description of train/test splits beyond "held-out subset" for the brain cells dataset. Variable gene selection follows prior work. SCONE used to select factors of unwanted variation for PBMC data. No multi-species mixing. No deduplication described.

## Training Recipe

- **Objective**: Maximize the ELBO (variational lower bound). Discrete latent variables h, w, y are analytically marginalized out so the bound is continuous and end-to-end differentiable.
- **Optimization**: Stochastic backpropagation (reparameterization trick).
- **Framework**: TensorFlow.
- **Tokenizer**: N/A (continuous gene expression input, not tokenized).
- **Batch size**: Not reported.
- **Optimizer / schedule**: Not reported.
- **Hardware**: Single GPU (unspecified model).
- **Wall-clock**: <2 hours for the full 1.3M cell dataset on one GPU. ZIFA and ZINB-WaVE require >20 min for 10k cells and OOM at 100k cells on 32 GB RAM.
- **Total tokens/steps**: Not reported.

## Key Ablations & Design Choices

**1. Scalability comparison (Table 1 — Marginal log-likelihood on held-out brain cells, 720 genes):**

| Method | 4k cells | 10k cells | 100k cells |
|---|---|---|---|
| FA | -1178.2 | -1177.3 | -1169.8 |
| ZIFA | -1250.9 | -1250.7 | NA (OOM) |
| ZINB-WaVE | -1166.3 | -1164.4 | NA (OOM) |
| **scVI** | **-1159.9** | **-1147.8** | **-1128.7** |

scVI wins at all scales. Its advantage grows with dataset size (gap vs. ZINB-WaVE: 6.4 at 4k → 16.6 at 10k). ZIFA and ZINB-WaVE cannot run at 100k cells.

**2. Imputation of zero-inflated entries (Table 2 — 10k brain cells):**

| Method | Imputation error (abs) | Identification of zeroed-out (cross-entropy) |
|---|---|---|
| ZIFA | 3.00 | 1.955 |
| MAGIC | 1.806 | NA |
| ZINB-WaVE | 1.053 | 1.366 |
| **scVI** | **1.048** | **0.742** |

scVI essentially ties ZINB-WaVE on imputation error (1.048 vs 1.053) but dramatically outperforms on dropout identification (0.742 vs 1.366, ~46% lower cross-entropy).

**3. Clustering recovery — Mouse cortex (Table 3 — Silhouette, 3005 cells, 7 types):**

| Method | Silhouette |
|---|---|
| FA | 0.208 |
| ZIFA | 0.202 |
| ZINB-WaVE | 0.260 |
| **scVI** | **0.285** |

scVI achieves highest silhouette (+0.025 over ZINB-WaVE, +9.6% relative).

**4. Batch/QC correction — PBMC (Table 4 — 12,039 cells):**

| Method | Silhouette ↑ | QC correlation ↓ |
|---|---|---|
| PCA | 0.314 | 0.381 |
| PCA (normalized) | 0.321 | 0.169 |
| scVI (no covariates) | 0.375 | 0.366 |
| **scVI (with covariates)** | **0.379** | **0.157** |

Adding batch covariates to scVI reduces QC correlation from 0.366 → 0.157 (57% drop) with no loss in silhouette (0.375 → 0.379), demonstrating effective disentanglement of technical variation.

**5. Latent space point-estimate variant (Section 3.3):** For clustering, z_n is treated as a parameter to estimate (MAP) rather than a latent variable with a distribution, maximizing mutual information between z_n and x_n (following InfoVAE). This modification is specific to the clustering benchmark.

**6. Differential expression (Figure 2 — PBMC, B cells vs. Dendritic cells):**
scVI's Bayesian hypothesis test yields higher reproducibility correlation with bulk array ground truth (~0.265) vs. DESeq2 (~0.215), an improvement of ~0.05 in correlation with ground-truth rankings via the IDR model.

## Reported Insights

- The ZINB observation model is well-matched to single-cell RNA-seq data because it captures both over-dispersion (negative binomial) and technical dropout (zero-inflation).
- Stochastic optimization (mini-batch SGD via the reparameterization trick) is critical for scalability; batch optimization methods (ZIFA, ZINB-WaVE) cannot scale beyond ~10k cells.
- Explicitly modeling batch effects and QC covariates as inputs to the decoder allows the latent space to encode only biological variation, improving both clustering quality and technical-noise removal simultaneously.
- The generative model naturally supports Bayesian differential expression testing, which shows better reproducibility with bulk RNA-seq ground truth than frequentist methods (DESeq2).
- Analytically marginalizing out discrete latent variables (h, w, y) keeps the ELBO differentiable, avoiding discrete-variable inference challenges.

## References Worth Chasing

- ZIFA: Dimensionality reduction for zero-inflated single-cell gene expression analysis (Pierson & Yau 2015) — direct baseline, zero-inflated factor analysis for scRNA-seq
- ZINB-WaVE: A general and flexible method for signal extraction from single-cell RNA-seq data (Risso et al. 2017, bioRxiv) — strongest non-neural baseline, ZINB-based
- MAGIC: A diffusion-based imputation method reveals gene-gene interactions in single-cell RNA-sequencing data (van Dijk et al. 2017, bioRxiv) — imputation baseline using diffusion on kNN graphs
- Auto-Encoding Variational Bayes (Kingma & Welling, ICLR 2014) — foundational VAE paper underpinning scVI's architecture
- InfoVAE: Information maximizing variational autoencoders (Zhao et al., arXiv:1706.02262) — motivates the MAP variant used for clustering
- Variational inference: A review for statisticians (Blei et al. 2017) — theoretical grounding for the inference procedure
- Interpretable dimensionality reduction of single cell transcriptome data with deep generative models (Ding et al. 2017, bioRxiv) — concurrent neural-network approach to scRNA-seq
- Using neural networks for reducing the dimensions of single-cell RNA-Seq data (Lin et al. 2017) — concurrent neural-network approach
- DESeq2: Moderated estimation of fold change and dispersion for RNA-seq data (Love et al. 2014) — standard DE testing baseline
- SCONE: Single Cell Overview of Normalized Expression data (Cole & Risso 2016) — normalization/QC selection tool used in the pipeline
- Dirichlet process mixture model for correcting technical variation in single-cell gene expression data (Prabhakaran et al. 2016) — related correction method

## Notes / Open Questions

- **No explicit parameter count** reported. Architecture is very small by modern standards (~tens of thousands of parameters); this is a task-specific generative model, not a foundation model in the modern sense.
- **Limited benchmarking scope**: Only three datasets are used, all mouse/human. No cross-species generalization tested.
- **Variable gene selection** relies on external methods (sampling "variable genes"); the model doesn't operate on the full transcriptome by default.
- **The held-out evaluation metric** (marginal log-likelihood) is computed conditional on a latent representation learned for held-out data, which conflates generative model quality with encoder quality.
- **Imputation evaluation** uses synthetic zeros generated according to ZIFA's dropout model, which may favor models with similar zero-inflation assumptions (like scVI).
- **Differential expression evaluation** uses a single bulk array reference with n=10 per group; reproducibility is quantified via IDR correlation, which is somewhat unconventional and hard to interpret in absolute terms.
- **Hyperparameter sensitivity** not explored: latent dimension fixed at 10, network width at 128, depth at 3 layers — no ablation on these choices.
- This is an early "deep learning for scRNA-seq" paper (2018 conference version). The later Nature Methods 2018 paper (scVI) substantially expands the evaluation. The scvi-tools ecosystem grew from this work.
