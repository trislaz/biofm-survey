---
id: specbridge-bridging-mass-spectrometry-2026
title: 'SpecBridge: Bridging Mass Spectrometry and Molecular Representations via Cross-Modal
  Alignment'
authors:
- Yinkai Wang
- Yan Zhou Chen
- Xiaohui Chen
- Li-Ping Liu
- Soha Hassoun
year: 2026
venue: null
arxiv: '2601.17204'
doi: null
url: https://arxiv.org/abs/2601.17204v3
pdf_path: null
md_path: null
modalities:
- proteomics
status: seed
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:05+00:00'
updated_at: null
is_fm: false
fm_classification_reason: Cross-modal alignment using frozen ChemBERTa + DreaMS; no
  new FM.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Small-molecule identification from tandem mass spectrometry (MS/MS) remains a bottleneck in untargeted settings where spectral libraries are incomplete. While deep learning offers a solution, current approaches typically fall into two extremes: explicit generative models that construct molecular graphs atom-by-atom, or joint contrastive models that learn cross-modal subspaces from scratch. We introduce SpecBridge, a novel implicit alignment framework that treats structure identification as a geometric alignment problem. SpecBridge fine-tunes a self-supervised spectral encoder (DreaMS) to project directly into the latent space of a frozen molecular foundation model (ChemBERTa), and then performs retrieval by cosine similarity to a fixed bank of precomputed molecular embeddings. Across MassSpecGym, Spectraverse, and MSnLib benchmarks, SpecBridge improves top-1 retrieval accuracy by roughly 20-25% relative to strong neural baselines, while keeping the number of trainable parameters small. These results suggest that aligning to frozen foundation models is a practical, stable alternative to designing new architectures from scratch. The code for SpecBridge is released at https://github.com/HassounLab/SpecBridge.
