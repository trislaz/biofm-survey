---
id: towards-large-scale-training-2024
title: Towards Large-Scale Training of Pathology Foundation Models
authors:
- kaiko. ai
- Nanne Aben
- Edwin D. de Jong
- Ioannis Gatopoulos
- Nicolas Känzig
- Mikhail Karasikov
- Axel Lagré
- Roman Moser
- Joost van Doorn
- Fei Tang
year: 2024
venue: null
arxiv: '2404.15217'
doi: null
url: https://arxiv.org/abs/2404.15217v1
pdf_path: papers/towards-large-scale-training-2024.pdf
md_path: papers/md/towards-large-scale-training-2024.md
modalities:
- imaging-pathology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T20:52:51+00:00'
updated_at: '2026-04-22T20:56:29+00:00'
---

## Abstract (from arxiv)

Driven by the recent advances in deep learning methods and, in particular, by the development of modern self-supervised learning algorithms, increased interest and efforts have been devoted to build foundation models (FMs) for medical images. In this work, we present our scalable training pipeline for large pathology imaging data, and a comprehensive analysis of various hyperparameter choices and training techniques for building pathology FMs. We release and make publicly available the first batch of our pathology FMs (https://github.com/kaiko-ai/towards_large_pathology_fms) trained on open-access TCGA whole slide images, a commonly used collection of pathology images. The experimental evaluation shows that our models reach state-of-the-art performance on various patch-level downstream tasks, ranging from breast cancer subtyping to colorectal nuclear segmentation. Finally, to unify the evaluation approaches used in the field and to simplify future comparisons of different FMs, we present an open-source framework (https://github.com/kaiko-ai/eva) designed for the consistent evaluation of pathology FMs across various downstream tasks.
