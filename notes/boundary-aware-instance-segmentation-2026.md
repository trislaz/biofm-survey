---
id: boundary-aware-instance-segmentation-2026
title: Boundary-Aware Instance Segmentation in Microscopy Imaging
authors:
- Thomas Mendelson
- Joshua Francois
- Galit Lahav
- Tammy Riklin-Raviv
year: 2026
venue: null
arxiv: '2603.21206'
doi: null
url: https://arxiv.org/abs/2603.21206v1
pdf_path: papers/boundary-aware-instance-segmentation-2026.pdf
md_path: papers/md/boundary-aware-instance-segmentation-2026.md
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
updated_at: '2026-04-22T20:17:38+00:00'
is_fm: false
fm_classification_reason: Supervised instance segmentation method; no pretraining
  at scale.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Accurate delineation of individual cells in microscopy videos is essential for studying cellular dynamics, yet separating touching or overlapping instances remains a persistent challenge. Although foundation-model for segmentation such as SAM have broadened the accessibility of image segmentation, they still struggle to separate nearby cell instances in dense microscopy scenes without extensive prompting. We propose a prompt-free, boundary-aware instance segmentation framework that predicts signed distance functions (SDFs) instead of binary masks, enabling smooth and geometry-consistent modeling of cell contours. A learned sigmoid mapping converts SDFs into probability maps, yielding sharp boundary localization and robust separation of adjacent instances. Training is guided by a unified Modified Hausdorff Distance (MHD) loss that integrates region- and boundary-based terms. Evaluations on both public and private high-throughput microscopy datasets demonstrate improved boundary accuracy and instance-level performance compared to recent SAM-based and foundation-model approaches. Source code is available at: https://github.com/ThomasMendelson/BAISeg.git
