---
id: joint-probabilistic-modeling-of-2021
title: Joint probabilistic modeling of single-cell multi-omic data with totalVI
authors:
- Adam Gayoso
- Zoë Steier
- Romain Lopez
- Jeffrey Regier
- Kristopher L. Nazor
- Aaron Streets
- Nir Yosef
year: 2021
venue: Nature Methods
arxiv: null
doi: 10.1038/s41592-020-01050-x
url: https://www.nature.com/articles/s41592-020-01050-x
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/joint-probabilistic-modeling-of-2021.md
modalities:
- single-cell-multiomics
status: extracted
evidence_quality: abstract+repo
tags:
- VAE
- CITE-seq
- protein-RNA
- variational-inference
- batch-correction
- negative-binomial
- scvi-tools
- multi-modal
- probabilistic-model
parameters: ~1M
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

totalVI (total Variational Inference) is a conditional VAE for end-to-end joint analysis of paired single-cell RNA + surface protein data (CITE-seq). It extends the scVI framework to model both modalities simultaneously via a shared latent space, treating RNA counts with a negative-binomial likelihood and protein counts with a negative-binomial *mixture* that explicitly disentangles foreground signal from antibody background. The model handles batch effects, missing proteins across panels, normalization, dimensionality reduction, imputation, and differential expression within a single probabilistic framework. Released as part of scvi-tools (PyTorch). Not a foundation model in the LLM sense — it is a task-specific probabilistic model (~1M params) trained per dataset, but it is foundational infrastructure for the single-cell multi-omics field and a precursor to later single-cell FMs.

## Model

- **Architecture**: Conditional variational autoencoder (CVAE). Encoder and decoder are fully-connected neural networks (not transformers).
- **Latent space**: Shared low-dimensional representation z ∈ ℝ^d (default d=20) capturing joint RNA+protein cell state, with a standard Normal prior.
- **RNA generative model**: Gene expression x_ng ~ NegativeBinomial(l_n · ρ_ng, θ_g), where ρ_n = f_ρ(z_n, s_n) is decoded from z and batch covariate s, and l_n is library size (observed or latent).
- **Protein generative model**: Uses a two-component NegBin mixture per protein to separate foreground (biologically meaningful) from background (ambient/non-specific antibody binding):
  - β_nt ~ LogNormal(c_t, d_t) — background intensity (prior params learned via GMM initialization)
  - v_nt ~ Bernoulli(π_nt) — background indicator
  - y_nt ~ NegBin(v·β + (1-v)·β·α, φ_t) — observed protein count
  - π_n = h_π(z_n, s_n), α_n = g_α(z_n, s_n) are neural network outputs
- **Inference model**: Factored approximate posterior q(β, z, l | x, y, s) with three encoder networks for z, l, and β respectively.
- **Batch handling**: Batch covariate s_n is concatenated with z as input to all decoder networks, enabling counterfactual predictions across batches.
- **Missing proteins**: Supports datasets with heterogeneous antibody panels (proteins measured in some batches but not others); missing protein likelihoods are marginalized.
- **Parameters**: ~1M (typical for scVI-family models; exact count depends on number of genes/proteins and hidden layer sizes; default: 1 hidden layer of 128 units in encoder/decoder).

## Data

- **Input**: Paired CITE-seq data — a UMI count matrix X (N cells × G genes) and a protein abundance matrix Y (N cells × T proteins), plus optional batch covariates S.
- **Key datasets in paper**:
  - **SLN-all**: Murine spleen and lymph node immune cells, 8 batches from 4 donors × 2 tissues, ~115 surface proteins, generated for this paper (GEO: GSE150599). The largest and most central evaluation dataset.
  - **PBMC5k, PBMC10k, MALT**: Public 10X Genomics CITE-seq datasets with 14–17 proteins; used for model evaluation.
- **Scale**: Datasets range from ~5K–30K cells with 4,000 highly variable genes and 14–115 proteins. Not large-scale by modern standards.
- **Preprocessing**: Standard scRNA-seq filtering (min counts, min genes); highly variable gene selection; no gene normalization (raw UMI counts are input to the model).

## Training Recipe

- **Objective**: Evidence lower bound (ELBO) with KL warmup — the KL term weight is linearly annealed from 0 to 1 over initial epochs to avoid posterior collapse.
- **Optimizer**: Adam.
- **Training**: Trained per dataset (not pre-trained/fine-tuned). Typical training: 400 epochs, ~5–15 minutes on a single GPU for datasets of ~10K–30K cells.
- **Hardware**: Single GPU sufficient (NVIDIA GPU recommended). Scalable to >1M cells with minibatch stochastic variational inference.
- **Protein background prior initialization**: A two-component GMM is fit per protein per batch to initialize the background prior parameters (c_t, d_t). Can be disabled with `empirical_protein_background_prior=False`.
- **Software**: PyTorch, released via scvi-tools (`pip install scvi-tools`). Uses PyTorch Lightning for training loop. Integrates with AnnData/Scanpy ecosystem.
- **Reproducibility**: Code at https://github.com/YosefLab/totalVI_reproducibility (archived on Zenodo: doi:10.5281/zenodo.4330368).

## Key Ablations & Design Choices

### Protein background mixture model
The defining design choice: modeling protein counts as a mixture of background and foreground negative binomials. This explicitly accounts for ambient antibody signal and non-specific binding — a known problem in CITE-seq that simpler models (like treating protein as just another count modality) fail to capture. The paper shows this produces better calibrated posterior predictive distributions vs. scVI (RNA-only) or factor analysis baselines.

### Joint vs. separate modeling
totalVI's joint latent space outperforms analyzing RNA and protein separately or with simple concatenation approaches. The shared z enables information transfer between modalities — e.g., protein signal can inform cell-type identification even when RNA signal is ambiguous.

### Comparison with WNN (Seurat v4)
totalVI and WNN (Weighted Nearest Neighbor, Stuart et al. 2019 / Seurat v4) are the two main approaches for CITE-seq integration. totalVI is fully probabilistic; WNN is algorithmic. totalVI provides uncertainty estimates, differential expression, and counterfactual predictions that WNN does not.

### Posterior predictive checks
Extensive use of posterior predictive checks to validate model fit — comparing coefficient of variation and distributional statistics of generated vs. observed data. This is a hallmark of the Bayesian approach in the scVI family.

### Missing protein handling
totalVI can integrate batches where different protein panels were measured, marginalizing over missing protein likelihoods. This is practically important as antibody panels vary across experiments.

## Reported Insights

- **Protein background is critical**: Ignoring the background component leads to substantial artifacts in protein-based analyses. The mixture model effectively separates signal from noise.
- **RNA-protein correlation is complex**: The paper finds that RNA and protein levels for the same gene are only weakly correlated (consistent with known post-transcriptional regulation), but totalVI's joint latent space captures the shared biological variation.
- **Batch correction**: totalVI corrects for batch effects in both RNA and protein simultaneously through the conditional generative model, outperforming separate batch correction of each modality.
- **Downstream tasks**: A single trained model supports dimensionality reduction, visualization, clustering, differential expression (both RNA and protein), data integration, and imputation — no separate methods needed.
- **Scalability**: scvi-tools implementation scales to >1M cells with GPU acceleration and minibatch training.

## References Worth Chasing

1. **Lopez et al. 2018** — "Deep Generative Modeling for Single-Cell Transcriptomics" (Nature Methods; doi:10.1038/s41592-018-0229-2). scVI — the direct predecessor; totalVI extends its RNA-only VAE to joint RNA+protein.
2. **Stoeckius et al. 2017** — "Simultaneous Epitope and Transcriptome Measurement in Single Cells" (Nature Methods; doi:10.1038/nmeth.4380). Original CITE-seq technology paper.
3. **Stuart et al. 2019** — "Comprehensive Integration of Single-Cell Data" (Cell; doi:10.1016/j.cell.2019.05.031). Seurat v3/WNN; main alternative approach for multi-modal single-cell integration.
4. **Gayoso et al. 2022** — "A Python Library for Probabilistic Analysis of Single-Cell Omics Data" (Nature Biotechnology; doi:10.1038/s41587-021-01206-w). scvi-tools software paper; the framework totalVI lives in.
5. **Boyeau et al. 2019** — "Deep Generative Models for Detecting Differential Expression in Single Cells" (bioRxiv; doi:10.1101/794289). Differential expression methodology used in totalVI.
6. **Argelaguet et al. 2018** — "Multi-Omics Factor Analysis (MOFA)" (Mol. Sys. Biol.). Alternative multi-omics integration approach (factor analysis based).
7. **Kingma & Welling 2014** — "Auto-Encoding Variational Bayes" (ICLR). Foundation VAE paper underlying the methodology.

## Notes / Open Questions

- **Not a foundation model**: totalVI is trained per dataset, not pre-trained on large corpora. It is a task-specific probabilistic model. However, it is foundational *infrastructure* in the single-cell field — part of the scvi-tools ecosystem that later influenced single-cell foundation models like scVI-based pretraining, scGPT, and scTab.
- **Exact parameter count not reported**: The paper does not state the total parameter count. With default architecture (128-unit hidden layers, 20-dim latent space, ~4000 genes + ~100 proteins), the model has on the order of ~1M parameters.
- **Training compute negligible by FM standards**: Training takes minutes on a single GPU — orders of magnitude cheaper than modern foundation models.
- **Protein panel size limitation**: CITE-seq typically measures tens to a few hundred surface proteins (vs. ~20,000 genes for RNA). The protein modality is much lower-dimensional.
- **Successor work**: MultiVI (Ashuach et al. 2023) extends the totalVI framework to handle unpaired multi-modal data (CITE-seq + scATAC-seq). scvi-tools continues active development under the scverse project.
- **License**: scvi-tools is BSD-3-Clause licensed.
