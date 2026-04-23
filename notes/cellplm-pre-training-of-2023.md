---
id: cellplm-pre-training-of-2023
title: 'CellPLM: pre-training of cell language model beyond single cells'
authors: []
year: 2023
venue: null
arxiv: null
doi: 10.1101/2023.10.03.560734
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/cellplm-pre-training-of-2023.md
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

Source: ICLR 2024 camera-ready, Appendix I, Table 10. Three ablations on two tasks (cell-type classification: MS, hPancreas — F1 / precision; spatial imputation: Lung, Liver — Pearson corr / cosine).

| Variant | MS F1 | MS prec | hPanc F1 | hPanc prec | Lung corr | Lung cos | Liver corr | Liver cos |
|---|---|---|---|---|---|---|---|---|
| CellPLM (full) | 0.766±0.007 | 0.803±0.008 | 0.749±0.010 | 0.753±0.010 | 0.318±0.015 | 0.481±0.011 | 0.328±0.011 | 0.481±0.010 |
| w/o Mixture of Gaussian (single Gaussian prior, scVI-style) | 0.737±0.042 | 0.766±0.069 | 0.711±0.025 | 0.701±0.025 | 0.258±0.011 | 0.449±0.005 | 0.232±0.013 | 0.433±0.008 |
| w/o Latent Distribution (deterministic MAE) | 0.750±0.024 | 0.809±0.032 | 0.733±0.034 | 0.731±0.033 | 0.262±0.011 | 0.449±0.008 | 0.246±0.017 | 0.428±0.012 |
| w/o Transformer Encoder (MLP, 85M→50M params) | 0.750±0.050 | 0.794±0.074 | 0.751±0.010 | 0.750±0.012 | 0.244±0.016 | 0.443±0.008 | 0.250±0.032 | 0.440±0.021 |

Take-away: the **Mixture-of-Gaussian prior is the single most important design choice** — swapping it for a vanilla Gaussian is *worse than dropping the latent distribution entirely* (e.g., Liver corr 0.232 vs 0.246), confirming that an ill-suited prior actively harms heterogeneous multi-donor/multi-platform pre-training. The transformer encoder matters chiefly for **spatial imputation** (corr 0.318→0.244 on Lung), where cell–cell relations are exploitable, and is near-neutral for cell-type classification on dissociated scRNA-seq.

