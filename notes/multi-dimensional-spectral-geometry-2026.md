---
id: multi-dimensional-spectral-geometry-2026
title: Multi-Dimensional Spectral Geometry of Biological Knowledge in Single-Cell
  Transformer Representations
authors:
- Ihor Kendiukhov
year: 2026
venue: null
arxiv: '2602.22247'
doi: null
url: https://arxiv.org/abs/2602.22247v1
pdf_path: papers/multi-dimensional-spectral-geometry-2026.pdf
md_path: papers/md/multi-dimensional-spectral-geometry-2026.md
modalities:
- interactome
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:10+00:00'
updated_at: '2026-04-22T20:22:57+00:00'
is_fm: false
fm_classification_reason: Analysis of single-cell transformer representations; not
  a model.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Single-cell foundation models such as scGPT learn high-dimensional gene representations, but what biological knowledge these representations encode remains unclear. We systematically decode the geometric structure of scGPT internal representations through 63 iterations of automated hypothesis screening (183 hypotheses tested), revealing that the model organizes genes into a structured biological coordinate system rather than an opaque feature space. The dominant spectral axis separates genes by subcellular localization, with secreted proteins at one pole and cytosolic proteins at the other. Intermediate transformer layers transiently encode mitochondrial and ER compartments in a sequence that mirrors the cellular secretory pathway. Orthogonal axes encode protein-protein interaction networks with graded fidelity to experimentally measured interaction strength (Spearman rho = 1.000 across n = 5 STRING confidence quintiles, p = 0.017). In a compact six-dimensional spectral subspace, the model distinguishes transcription factors from their target genes (AUROC = 0.744, all 12 layers significant). Early layers preserve which specific genes regulate which targets, while deeper layers compress this into a coarser regulator versus regulated distinction. Repression edges are geometrically more prominent than activation edges, and B-cell master regulators BATF and BACH2 show convergence toward the B-cell identity anchor PAX5 across transformer depth. Cell-type marker genes cluster with high fidelity (AUROC = 0.851). Residual-stream geometry encodes biological structure complementary to attention patterns. These results indicate that biological transformers learn an interpretable internal model of cellular organization, with implications for regulatory network inference, drug target prioritization, and model auditing.
