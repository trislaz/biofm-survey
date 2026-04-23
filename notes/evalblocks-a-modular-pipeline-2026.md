---
id: evalblocks-a-modular-pipeline-2026
title: 'EvalBlocks: A Modular Pipeline for Rapidly Evaluating Foundation Models in
  Medical Imaging'
authors:
- Jan Tagscherer
- Sarah de Boer
- Lena Philipp
- Fennie van der Graaf
- Dré Peeters
- Joeran Bosma
- Lars Leijten
- Bogdan Obreja
- Ewoud Smit
- Alessa Hering
year: 2026
venue: null
arxiv: '2601.03811'
doi: null
url: https://arxiv.org/abs/2601.03811v2
pdf_path: papers/evalblocks-a-modular-pipeline-2026.pdf
md_path: papers/md/evalblocks-a-modular-pipeline-2026.md
modalities:
- imaging-radiology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:06+00:00'
updated_at: '2026-04-22T20:19:49+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Developing foundation models in medical imaging requires continuous monitoring of downstream performance. Researchers are burdened with tracking numerous experiments, design choices, and their effects on performance, often relying on ad-hoc, manual workflows that are inherently slow and error-prone. We introduce EvalBlocks, a modular, plug-and-play framework for efficient evaluation of foundation models during development. Built on Snakemake, EvalBlocks supports seamless integration of new datasets, foundation models, aggregation methods, and evaluation strategies. All experiments and results are tracked centrally and are reproducible with a single command, while efficient caching and parallel execution enable scalable use on shared compute infrastructure. Demonstrated on five state-of-the-art foundation models and three medical imaging classification tasks, EvalBlocks streamlines model evaluation, enabling researchers to iterate faster and focus on model innovation rather than evaluation logistics. The framework is released as open source software at https://github.com/DIAGNijmegen/eval-blocks.
