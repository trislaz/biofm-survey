---
id: unifying-multiple-foundation-models-2025
title: Unifying Multiple Foundation Models for Advanced Computational Pathology
authors:
- Wenhui Lei
- Yusheng Tan
- Anqi Li
- Hanyu Chen
- Hengrui Tian
- Ruiying Li
- Zhengqun Jiang
- Fang Yan
- Xiaofan Zhang
- Shaoting Zhang
year: 2025
venue: null
arxiv: '2503.00736'
doi: null
url: https://arxiv.org/abs/2503.00736v4
pdf_path: papers/unifying-multiple-foundation-models-2025.pdf
md_path: papers/md/unifying-multiple-foundation-models-2025.md
modalities:
- imaging-pathology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:15+00:00'
updated_at: '2026-04-22T20:27:43+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Foundation models have substantially advanced computational pathology by learning transferable visual representations from large histological datasets, yet their performance varies widely across tasks due to differences in training data composition and reliance on proprietary datasets that cannot be cumulatively expanded. Existing efforts to combine foundation models through offline distillation partially mitigate this issue but require dedicated distillation data and repeated retraining to integrate new models. Here we present Shazam, an online integration model that adaptively combines multiple pretrained pathology foundation models within a unified and scalable representation learning paradigm. Our findings show that fusing multi-level features through adaptive expert weighting and online distillation enables efficient consolidation of complementary model strengths without additional pretraining. Across spatial transcriptomics prediction, survival prognosis, tile-level classification, and visual question answering, Shazam consistently outperforms strong individual models, demonstrating that online model integration provides a practical and extensible strategy for advancing computational pathology.
