---
id: inverse-problems-with-experiment-2025
title: Inverse problems with experiment-guided AlphaFold
authors:
- Advaith Maddipatla
- Nadav Bojan Sellam
- Meital Bojan
- Sanketh Vedula
- Paul Schanda
- Ailie Marx
- Alex M. Bronstein
year: 2025
venue: null
arxiv: '2502.09372'
doi: null
url: https://arxiv.org/abs/2502.09372v2
pdf_path: papers/inverse-problems-with-experiment-2025.pdf
md_path: papers/md/inverse-problems-with-experiment-2025.md
modalities:
- protein-structure
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:03+00:00'
updated_at: '2026-04-22T20:22:08+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Proteins exist as a dynamic ensemble of multiple conformations, and these motions are often crucial for their functions. However, current structure prediction methods predominantly yield a single conformation, overlooking the conformational heterogeneity revealed by diverse experimental modalities. Here, we present a framework for building experiment-grounded protein structure generative models that infer conformational ensembles consistent with measured experimental data. The key idea is to treat state-of-the-art protein structure predictors (e.g., AlphaFold3) as sequence-conditioned structural priors, and cast ensemble modeling as posterior inference of protein structures given experimental measurements. Through extensive real-data experiments, we demonstrate the generality of our method to incorporate a variety of experimental measurements. In particular, our framework uncovers previously unmodeled conformational heterogeneity from crystallographic densities, and generates high-accuracy NMR ensembles orders of magnitude faster than the status quo. Notably, we demonstrate that our ensembles outperform AlphaFold3 and sometimes better fit experimental data than publicly deposited structures to the Protein Data Bank (PDB). We believe that this approach will unlock building predictive models that fully embrace experimentally observed conformational diversity.
