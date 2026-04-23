---
id: enhancing-the-efficiency-of-2024
title: Enhancing the efficiency of protein language models with minimal wet-lab data
  through few-shot learning
authors:
- Ziyi Zhou
- Liang Zhang
- Yuanxi Yu
- Mingchen Li
- Liang Hong
- Pan Tan
year: 2024
venue: null
arxiv: '2402.02004'
doi: null
url: https://arxiv.org/abs/2402.02004v1
pdf_path: papers/enhancing-the-efficiency-of-2024.pdf
md_path: papers/md/enhancing-the-efficiency-of-2024.md
modalities:
- protein-sequence
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:52+00:00'
updated_at: '2026-04-22T20:19:40+00:00'
is_fm: false
fm_classification_reason: Few-shot fine-tuning method on PLMs; no new pretrained FM.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Accurately modeling the protein fitness landscapes holds great importance for protein engineering. Recently, due to their capacity and representation ability, pre-trained protein language models have achieved state-of-the-art performance in predicting protein fitness without experimental data. However, their predictions are limited in accuracy as well as interpretability. Furthermore, such deep learning models require abundant labeled training examples for performance improvements, posing a practical barrier. In this work, we introduce FSFP, a training strategy that can effectively optimize protein language models under extreme data scarcity. By combining the techniques of meta-transfer learning, learning to rank, and parameter-efficient fine-tuning, FSFP can significantly boost the performance of various protein language models using merely tens of labeled single-site mutants from the target protein. The experiments across 87 deep mutational scanning datasets underscore its superiority over both unsupervised and supervised approaches, revealing its potential in facilitating AI-guided protein design.
