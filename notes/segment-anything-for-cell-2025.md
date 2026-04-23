---
id: segment-anything-for-cell-2025
title: Segment Anything for Cell Tracking
authors:
- Zhu Chen
- Mert Edgü
- Er Jin
- Johannes Stegmaier
year: 2025
venue: null
arxiv: '2509.09943'
doi: null
url: https://arxiv.org/abs/2509.09943v1
pdf_path: papers/segment-anything-for-cell-2025.pdf
md_path: papers/md/segment-anything-for-cell-2025.md
modalities:
- imaging-microscopy
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:01+00:00'
updated_at: '2026-04-22T20:25:54+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Tracking cells and detecting mitotic events in time-lapse microscopy image sequences is a crucial task in biomedical research. However, it remains highly challenging due to dividing objects, low signal-tonoise ratios, indistinct boundaries, dense clusters, and the visually similar appearance of individual cells. Existing deep learning-based methods rely on manually labeled datasets for training, which is both costly and time-consuming. Moreover, their generalizability to unseen datasets remains limited due to the vast diversity of microscopy data. To overcome these limitations, we propose a zero-shot cell tracking framework by integrating Segment Anything 2 (SAM2), a large foundation model designed for general image and video segmentation, into the tracking pipeline. As a fully-unsupervised approach, our method does not depend on or inherit biases from any specific training dataset, allowing it to generalize across diverse microscopy datasets without finetuning. Our approach achieves competitive accuracy in both 2D and large-scale 3D time-lapse microscopy videos while eliminating the need for dataset-specific adaptation.
