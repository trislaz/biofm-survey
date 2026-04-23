---
id: scdrugmap-benchmarking-large-foundation-2025
title: 'scDrugMap: Benchmarking Large Foundation Models for Drug Response Prediction'
authors:
- Qing Wang
- Yining Pan
- Minghao Zhou
- Zijia Tang
- Yanfei Wang
- Guangyu Wang
- Qianqian Song
year: 2025
venue: null
arxiv: '2505.05612'
doi: null
url: https://arxiv.org/abs/2505.05612v1
pdf_path: papers/scdrugmap-benchmarking-large-foundation-2025.pdf
md_path: papers/md/scdrugmap-benchmarking-large-foundation-2025.md
modalities:
- scrna
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:11+00:00'
updated_at: '2026-04-22T20:25:32+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Drug resistance presents a major challenge in cancer therapy. Single cell profiling offers insights into cellular heterogeneity, yet the application of large-scale foundation models for predicting drug response in single cell data remains underexplored. To address this, we developed scDrugMap, an integrated framework featuring both a Python command-line interface and a web server for drug response prediction. scDrugMap evaluates a wide range of foundation models, including eight single-cell models and two large language models, using a curated dataset of over 326,000 cells in the primary collection and 18,800 cells in the validation set, spanning 36 datasets and diverse tissue and cancer types. We benchmarked model performance under pooled-data and cross-data evaluation settings, employing both layer freezing and Low-Rank Adaptation (LoRA) fine-tuning strategies. In the pooled-data scenario, scFoundation achieved the best performance, with mean F1 scores of 0.971 (layer freezing) and 0.947 (fine-tuning), outperforming the lowest-performing model by over 50%. In the cross-data setting, UCE excelled post fine-tuning (mean F1: 0.774), while scGPT led in zero-shot learning (mean F1: 0.858). Overall, scDrugMap provides the first large-scale benchmark of foundation models for drug response prediction in single-cell data and serves as a user-friendly, flexible platform for advancing drug discovery and translational research.
