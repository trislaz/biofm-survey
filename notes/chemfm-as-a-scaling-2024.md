---
id: chemfm-as-a-scaling-2024
title: ChemFM as a Scaling Law Guided Foundation Model Pre-trained on Informative
  Chemicals
authors:
- Feiyang Cai
- Katelin Zacour
- Tianyu Zhu
- Tzuen-Rong Tzeng
- Yongping Duan
- Ling Liu
- Srikanth Pilla
- Gang Li
- Feng Luo
year: 2024
venue: null
arxiv: '2410.21422'
doi: null
url: https://arxiv.org/abs/2410.21422v3
pdf_path: null
md_path: null
modalities:
- small-molecule
status: seed
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:21+00:00'
updated_at: null
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Traditional AI methods often rely on task-specific model designs and training, which constrain both the scalability of model size and generalization across different tasks. Here, we introduce ChemFM, a large foundation model specifically developed for chemicals. By conducting a series of scaling experiments, we identify UniChem as the informative molecular database for pre-training the foundation model. ChemFM comprises 3 billion parameters and is pre-trained on 178 million molecules using self-supervised causal language modeling to extract generalizable molecular representations. This model can be adapted to diverse downstream chemical applications using either full-parameter or parameter-efficient fine-tuning methods. ChemFM consistently outperforms state-of-the-art task-specific AI models across all tested tasks. Notably, it achieves up to 67.48% performance improvement across 34 property prediction benchmarks, up to 33.80% reduction in mean average deviation between conditioned and actual properties of generated molecules in conditional molecular generation tasks, and up to 3.7% top-1 accuracy improvement across 4 reaction prediction datasets. Moreover, ChemFM demonstrates its superior performance in predicting antibiotic activity and cytotoxicity, highlighting its potential to advance the discovery of novel antibiotics. Furthermore, we demonstrate that, as a foundation model, ChemFM exhibits strong data efficiency, requiring significantly fewer labeled training samples to achieve state-of-the-art performance. We anticipate that ChemFM will significantly advance chemistry research by providing a foundation model capable of effectively generalizing across a broad range of tasks with minimal additional training.
