---
id: boosting-in-silicon-directed-2025
title: Boosting In-Silicon Directed Evolution with Fine-Tuned Protein Language Model
  and Tree Search
authors:
- Yaodong Yang
- Yang Wang
- Jinpeng Li
- Pei Guo
- Da Han
- Guangyong Chen
- Pheng-Ann Heng
year: 2025
venue: null
arxiv: '2511.09900'
doi: null
url: https://arxiv.org/abs/2511.09900v4
pdf_path: papers/boosting-in-silicon-directed-2025.pdf
md_path: papers/md/boosting-in-silicon-directed-2025.md
modalities:
- protein-sequence
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:52+00:00'
updated_at: '2026-04-22T20:17:36+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Protein evolution through amino acid mutations is a cornerstone of life sciences. Recent advances in protein language models have shown rich evolutionary patterns, offering unprecedented potential for in-silicon directed evolution. However, existing directed evolution methods largely rely on heuristic evolution strategies and have yet to efficiently integrate the transformative protein language models with advanced optimization techniques, such as reinforcement learning, to adaptively learn superior evolution policies. To bridge this gap, we propose AlphaDE, a novel framework that evolves protein sequences by harnessing the innovative paradigms of large language models, such as fine-tuning and test-time inference. First, AlphaDE fine-tunes pretrained protein language models using masked language modeling on homologous protein sequences to activate the evolutionary plausibility of the interested protein family. Second, AlphaDE introduces test-time inference based on Monte Carlo tree search, which effectively evolves proteins with evolutionary guidance from the fine-tuned protein language model. Extensive benchmark experiments show that AlphaDE remarkably outperforms previous state-of-the-art methods even with few-shot fine-tuning. A case study further demonstrates that AlphaDE supports condensing the protein sequence space of avGFP through computational evolution.
