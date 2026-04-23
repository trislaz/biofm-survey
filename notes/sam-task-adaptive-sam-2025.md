---
id: sam-task-adaptive-sam-2025
title: 'SAM$^{*}$: Task-Adaptive SAM with Physics-Guided Rewards'
authors:
- Kamyar Barakati
- Utkarsh Pratiush
- Sheryl L. Sanchez
- Aditya Raghavan
- Delia J. Milliron
- Mahshid Ahmadi
- Philip D. Rack
- Sergei V. Kalinin
year: 2025
venue: null
arxiv: '2509.07047'
doi: null
url: https://arxiv.org/abs/2509.07047v1
pdf_path: papers/sam-task-adaptive-sam-2025.pdf
md_path: papers/md/sam-task-adaptive-sam-2025.md
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
updated_at: '2026-04-22T20:25:28+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Image segmentation is a critical task in microscopy, essential for accurately analyzing and interpreting complex visual data. This task can be performed using custom models trained on domain-specific datasets, transfer learning from pre-trained models, or foundational models that offer broad applicability. However, foundational models often present a considerable number of non-transparent tuning parameters that require extensive manual optimization, limiting their usability for real-time streaming data analysis. Here, we introduce a reward function-based optimization to fine-tune foundational models and illustrate this approach for SAM (Segment Anything Model) framework by Meta. The reward functions can be constructed to represent the physics of the imaged system, including particle size distributions, geometries, and other criteria. By integrating a reward-driven optimization framework, we enhance SAM's adaptability and performance, leading to an optimized variant, SAM$^{*}$, that better aligns with the requirements of diverse segmentation tasks and particularly allows for real-time streaming data segmentation. We demonstrate the effectiveness of this approach in microscopy imaging, where precise segmentation is crucial for analyzing cellular structures, material interfaces, and nanoscale features.
