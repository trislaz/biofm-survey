---
id: open-world-knowledge-aided-2026
title: Open World Knowledge Aided Single-Cell Foundation Model with Robust Cross-Modal
  Cell-Language Pre-training
authors:
- Haoran Wang
- Xuanyi Zhang
- Shuangsang Fang
- Longke Ran
- Ziqing Deng
- Yong Zhang
- Yuxiang Li
- Shaoshuai Li
year: 2026
venue: null
arxiv: '2601.05648'
doi: null
url: https://arxiv.org/abs/2601.05648v1
pdf_path: null
md_path: null
modalities:
- scrna
- single-cell-multiomics
status: seed
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:11+00:00'
updated_at: null
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Recent advancements in single-cell multi-omics, particularly RNA-seq, have provided profound insights into cellular heterogeneity and gene regulation. While pre-trained language model (PLM) paradigm based single-cell foundation models have shown promise, they remain constrained by insufficient integration of in-depth individual profiles and neglecting the influence of noise within multi-modal data. To address both issues, we propose an Open-world Language Knowledge-Aided Robust Single-Cell Foundation Model (OKR-CELL). It is built based on a cross-modal Cell-Language pre-training framework, which comprises two key innovations: (1) leveraging Large Language Models (LLMs) based workflow with retrieval-augmented generation (RAG) enriches cell textual descriptions using open-world knowledge; (2) devising a Cross-modal Robust Alignment (CRA) objective that incorporates sample reliability assessment, curriculum learning, and coupled momentum contrastive learning to strengthen the model's resistance to noisy data. After pretraining on 32M cell-text pairs, OKR-CELL obtains cutting-edge results across 6 evaluation tasks. Beyond standard benchmarks such as cell clustering, cell-type annotation, batch-effect correction, and few-shot annotation, the model also demonstrates superior performance in broader multi-modal applications, including zero-shot cell-type annotation and bidirectional cell-text retrieval.
