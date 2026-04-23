---
id: alignment-or-integration-rethinking-2026
title: Alignment or Integration? Rethinking Multimodal Fusion in DNA-language Foundation
  Models
authors:
- Yanan Li
- Christina Yi Jin
- Yuan Jin
- Manli Luo
- Tie Xu
- Shuai Jiao
- Wei He
- Qing Zhang
year: 2026
venue: null
arxiv: '2602.12286'
doi: null
url: https://arxiv.org/abs/2602.12286v1
pdf_path: papers/alignment-or-integration-rethinking-2026.pdf
md_path: papers/md/alignment-or-integration-rethinking-2026.md
modalities:
- dna
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:44+00:00'
updated_at: '2026-04-22T20:16:26+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Fusing DNA foundation models with large language models (LLMs) for DNA-language reasoning raises a fundamental question: at what level should genomic sequences and natural language interact? Most existing approaches encode DNA sequences and text separately and rely on embedding-level alignment to connect the two modalities. Such late-stage fusion compresses rich genomic sequences into fixed representations, limiting the model's ability to reason over fine-grained, token-level genomic structure. In this work, we propose two new methods for DNA-language fusion, i.e., a semantic alignment method SeqCLIP and a vocabulary-level integration method OneVocab. SeqCLIP strengthens embedding-level alignment via sequence-level contrastive pre-training, and OneVocab directly integrates genomic $k$-mers into the language model's existing vocabulary. Comprehensive experiments on classification and reasoning tasks show that, while various alignment strategies improve embedding-level fusion, early vocabulary-level integration yields more expressive and effective representations for DNA-language modeling.
