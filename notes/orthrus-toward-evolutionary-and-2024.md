---
id: orthrus-toward-evolutionary-and-2024
title: 'Orthrus: Towards Evolutionary and Functional RNA Foundation Models'
authors:
- Philip Fradkin
- Ruian Shi
- Keren Isaev
- Brendan J. Frey
- Quaid Morris
- Leo J. Lee
- Bo Wang
year: 2024
venue: null
arxiv: null
doi: 10.1101/2024.10.10.617658
url: https://www.biorxiv.org/content/10.1101/2024.10.10.617658v1
pdf_path: null
md_path: null
modalities:
- rna
status: seed
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-29T12:08:51+00:00'
updated_at: null
is_fm: true
fm_classification_reason: 'Orthrus: pretrained mature-RNA foundation model with contrastive
  evolutionary/functional objective.'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from biorxiv)

Orthrus is a foundation model for mature RNA property prediction. It uses a Mamba
encoder backbone trained with a novel contrastive learning objective that leverages
biological augmentations: embedding similarity is maximized between curated pairs
of RNA transcripts derived from (a) splice isoforms within 10 model organisms and
(b) orthologous genes across 400+ mammalian species from the Zoonomia Project.
The resulting latent space clusters RNA sequences by functional and evolutionary
similarity. Orthrus outperforms existing genomic foundation models on five mRNA
property-prediction tasks (including RNA half-life, mean ribosome load, and
exon-junction detection), and is notably data-efficient, requiring substantially
less fine-tuning data than baselines. The model is highlighted for its ability to
capture divergent biological functions of individual transcript isoforms.

Code: https://github.com/bowang-lab/Orthrus
