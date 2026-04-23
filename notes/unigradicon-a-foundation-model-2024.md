---
id: unigradicon-a-foundation-model-2024
title: 'uniGradICON: A Foundation Model for Medical Image Registration'
authors:
- Lin Tian
- Hastings Greer
- Roland Kwitt
- Francois-Xavier Vialard
- Raul San Jose Estepar
- Sylvain Bouix
- Richard Rushmore
- Marc Niethammer
year: 2024
venue: null
arxiv: '2403.05780'
doi: null
url: https://arxiv.org/abs/2403.05780v1
pdf_path: papers/unigradicon-a-foundation-model-2024.pdf
md_path: papers/md/unigradicon-a-foundation-model-2024.md
modalities:
- imaging-pathology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T20:50:54+00:00'
updated_at: '2026-04-22T20:52:46+00:00'
---

## Abstract (from arxiv)

Conventional medical image registration approaches directly optimize over the parameters of a transformation model. These approaches have been highly successful and are used generically for registrations of different anatomical regions. Recent deep registration networks are incredibly fast and accurate but are only trained for specific tasks. Hence, they are no longer generic registration approaches. We therefore propose uniGradICON, a first step toward a foundation model for registration providing 1) great performance \emph{across} multiple datasets which is not feasible for current learning-based registration methods, 2) zero-shot capabilities for new registration tasks suitable for different acquisitions, anatomical regions, and modalities compared to the training dataset, and 3) a strong initialization for finetuning on out-of-distribution registration tasks. UniGradICON unifies the speed and accuracy benefits of learning-based registration algorithms with the generic applicability of conventional non-deep-learning approaches. We extensively trained and evaluated uniGradICON on twelve different public datasets. Our code and the uniGradICON model are available at https://github.com/uncbiag/uniGradICON.
