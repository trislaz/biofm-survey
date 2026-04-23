---
id: alphafold-distillation-for-protein-2022
title: AlphaFold Distillation for Protein Design
authors:
- Igor Melnyk
- Aurelie Lozano
- Payel Das
- Vijil Chenthamarakshan
year: 2022
venue: null
arxiv: '2210.03488'
doi: null
url: https://arxiv.org/abs/2210.03488v2
pdf_path: papers/alphafold-distillation-for-protein-2022.pdf
md_path: papers/md/alphafold-distillation-for-protein-2022.md
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
updated_at: '2026-04-22T20:16:38+00:00'
is_fm: false
fm_classification_reason: Distillation/regularization technique using AF, not a new
  pretrained FM.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Inverse protein folding, the process of designing sequences that fold into a specific 3D structure, is crucial in bio-engineering and drug discovery. Traditional methods rely on experimentally resolved structures, but these cover only a small fraction of protein sequences. Forward folding models like AlphaFold offer a potential solution by accurately predicting structures from sequences. However, these models are too slow for integration into the optimization loop of inverse folding models during training. To address this, we propose using knowledge distillation on folding model confidence metrics, such as pTM or pLDDT scores, to create a faster and end-to-end differentiable distilled model. This model can then be used as a structure consistency regularizer in training the inverse folding model. Our technique is versatile and can be applied to other design tasks, such as sequence-based protein infilling. Experimental results show that our method outperforms non-regularized baselines, yielding up to 3% improvement in sequence recovery and up to 45% improvement in protein diversity while maintaining structural consistency in generated sequences. Code is available at https://github.com/IBM/AFDistill
