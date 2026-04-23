---
id: towards-applying-large-language-2025
title: Towards Applying Large Language Models to Complement Single-Cell Foundation
  Models
authors:
- Steven Palayew
- Bo Wang
- Gary Bader
year: 2025
venue: null
arxiv: '2507.10039'
doi: null
url: https://arxiv.org/abs/2507.10039v1
pdf_path: papers/towards-applying-large-language-2025.pdf
md_path: papers/md/towards-applying-large-language-2025.md
modalities:
- scrna
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:11+00:00'
updated_at: '2026-04-22T20:26:49+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Single-cell foundation models such as scGPT represent a significant advancement in single-cell omics, with an ability to achieve state-of-the-art performance on various downstream biological tasks. However, these models are inherently limited in that a vast amount of information in biology exists as text, which they are unable to leverage. There have therefore been several recent works that propose the use of LLMs as an alternative to single-cell foundation models, achieving competitive results. However, there is little understanding of what factors drive this performance, along with a strong focus on using LLMs as an alternative, rather than complementary approach to single-cell foundation models. In this study, we therefore investigate what biological insights contribute toward the performance of LLMs when applied to single-cell data, and introduce scMPT; a model which leverages synergies between scGPT, and single-cell representations from LLMs that capture these insights. scMPT demonstrates stronger, more consistent performance than either of its component models, which frequently have large performance gaps between each other across datasets. We also experiment with alternate fusion methods, demonstrating the potential of combining specialized reasoning models with scGPT to improve performance. This study ultimately showcases the potential for LLMs to complement single-cell foundation models and drive improvements in single-cell analysis.
