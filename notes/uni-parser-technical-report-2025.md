---
id: uni-parser-technical-report-2025
title: Uni-Parser Technical Report
authors:
- Xi Fang
- Haoyi Tao
- Shuwen Yang
- Chaozheng Huang
- Suyang Zhong
- Haocheng Lu
- Han Lyu
- Junjie Wang
- Xinyu Li
- Linfeng Zhang
- Guolin Ke
year: 2025
venue: null
arxiv: '2512.15098'
doi: null
url: https://arxiv.org/abs/2512.15098v4
pdf_path: papers/uni-parser-technical-report-2025.pdf
md_path: papers/md/uni-parser-technical-report-2025.md
modalities:
- imaging-pathology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:16+00:00'
updated_at: '2026-04-22T20:27:48+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

This technical report introduces Uni-Parser, an industrial-grade document parsing engine tailored for scientific literature and patents, delivering high throughput, robust accuracy, and cost efficiency. Unlike pipeline-based document parsing methods, Uni-Parser employs a modular, loosely coupled multi-expert architecture that preserves fine-grained cross-modal alignments across text, equations, tables, figures, and chemical structures, while remaining easily extensible to emerging modalities. The system incorporates adaptive GPU load balancing, distributed inference, dynamic module orchestration, and configurable modes that support either holistic or modality-specific parsing. Optimized for large-scale cloud deployment, Uni-Parser achieves a processing rate of up to 20 PDF pages per second on 8 x NVIDIA RTX 4090D GPUs, enabling cost-efficient inference across billions of pages. This level of scalability facilitates a broad spectrum of downstream applications, ranging from literature retrieval and summarization to the extraction of chemical structures, reaction schemes, and bioactivity data, as well as the curation of large-scale corpora for training next-generation large language models and AI4Science models.
