---
id: perturbdiff-functional-diffusion-for-2026
title: 'PerturbDiff: Functional Diffusion for Single-Cell Perturbation Modeling'
authors:
- Xinyu Yuan
- Xixian Liu
- Ya Shi Zhang
- Zuobai Zhang
- Hongyu Guo
- Jian Tang
year: 2026
venue: null
arxiv: '2602.19685'
doi: null
url: https://arxiv.org/abs/2602.19685
pdf_path: null
md_path: null
modalities:
- scrna
status: extracted
evidence_quality: abstract+repo
tags:
- single-cell-perturbation
- diffusion
- virtual-cells
- distribution-level-generation
- hilbert-space
- pretraining-finetuning
parameters: null
training_tokens: CellxGene pretraining plus PBMC, Tahoe100M, and Replogle finetuning/evaluation datasets
training_compute: null
references_chased: false
added_at: '2026-05-19T10:51:33+00:00'
updated_at: '2026-05-19T10:51:33+00:00'
is_fm: true
fm_classification_reason: Introduces a pretrained and finetuned single-cell perturbation model for virtual-cell response simulation.
---

## TL;DR

PerturbDiff is a diffusion-based single-cell RNA sequencing (scRNA-seq) perturbation model for simulating virtual-cell responses. Instead of generating individual cells directly, it embeds whole cell populations as probability distributions in a Hilbert space and runs diffusion at the distribution level, so responses conditioned on the same observed cell type and perturbation can vary across latent factors such as microenvironment and batch effects. The released code describes large-scale pretraining on CellxGene-derived data followed by finetuning and sampling on peripheral blood mononuclear cell (PBMC), Tahoe100M, and Replogle perturbation benchmarks.

## Model

- **Architecture**: Conditional diffusion model with a Cross-DiT-style backbone for single-cell perturbation response generation.
- **Representation level**: Models probability distributions over cell populations rather than a deterministic map from one cell or one condition to one response.
- **Conditioning**: Uses covariate encoders for perturbation, cell type, and batch-style metadata, with conditional sampling from trained checkpoints.
- **Goal**: Predict perturbed scRNA-seq response populations from unpaired control and perturbed measurements.

## Data

- **Pretraining**: CellxGene-derived merged single-cell data are listed in the public repository's data layout for pretraining.
- **Finetuning and evaluation**: PBMC cytokine perturbation data, Tahoe100M perturbation data, and Replogle perturbation data are listed as supported finetuning and sampling scenarios.
- **Task setting**: Single-cell perturbation prediction where destructive sequencing prevents observing the same cell before and after perturbation.

## Training Recipe

- **Objective**: Diffusion training over distribution-level representations of cell populations.
- **Workflow**: Train from scratch on individual datasets or pretrain on multi-source single-cell data and finetune on PBMC, Tahoe100M, or Replogle.
- **Sampling**: Conditional sampling from released checkpoints to generate perturbation response distributions.

## Key Ablations & Design Choices

1. **Distribution-level generation**: The central design choice is to diffuse over population distributions in a Hilbert-space formulation rather than model only individual-cell transitions.
2. **Latent response variability**: PerturbDiff explicitly targets the one-to-many nature of perturbation responses caused by hidden factors, avoiding collapse to a single average target distribution for each observed condition.
3. **Pretraining plus finetuning**: The released workflow supports both dataset-specific training and pretrained checkpoint finetuning, positioning the model as a virtual-cell foundation model for perturbation response simulation.

## Reported Insights

- The paper reports state-of-the-art (SOTA) single-cell response prediction and substantially better generalization to unseen perturbations than prior methods.
- Distribution-level diffusion is a promising design for perturbation modeling when observed metadata do not fully determine the target response population.
- The method is most directly relevant to the survey's single-cell foundation-model axis, especially virtual-cell and perturbation-response models.

## Caveats

- Publicly accessible metadata did not expose parameter counts or training compute, so those fields are left unknown.
- The note is based on the arXiv abstract and the public code repository rather than a locally converted full-text paper.

## Sources

- Paper: [arXiv:2602.19685](https://arxiv.org/abs/2602.19685)
- Project/code: [DeepGraphLearning/PerturbDiff](https://github.com/DeepGraphLearning/PerturbDiff)
