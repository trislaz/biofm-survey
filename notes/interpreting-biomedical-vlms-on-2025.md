---
id: interpreting-biomedical-vlms-on-2025
title: 'Interpreting Biomedical VLMs on High-Imbalance Out-of-Distributions: An Insight
  into BiomedCLIP on Radiology'
authors:
- Nafiz Sadman
- Farhana Zulkernine
- Benjamin Kwan
year: 2025
venue: null
arxiv: '2506.14136'
doi: null
url: https://arxiv.org/abs/2506.14136v1
pdf_path: papers/interpreting-biomedical-vlms-on-2025.pdf
md_path: papers/md/interpreting-biomedical-vlms-on-2025.md
modalities:
- multimodal
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:17+00:00'
updated_at: '2026-04-22T20:21:58+00:00'
is_fm: false
fm_classification_reason: Interpretability of BiomedCLIP on radiology OOD.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

In this paper, we construct two research objectives: i) explore the learned embedding space of BiomedCLIP, an open-source large vision language model, to analyse meaningful class separations, and ii) quantify the limitations of BiomedCLIP when applied to a highly imbalanced, out-of-distribution multi-label medical dataset. We experiment on IU-xray dataset, which exhibits the aforementioned criteria, and evaluate BiomedCLIP in classifying images (radiographs) in three contexts: zero-shot inference, full finetuning, and linear probing. The results show that the model under zero-shot settings over-predicts all labels, leading to poor precision and inter-class separability. Full fine-tuning improves classification of distinct diseases, while linear probing detects overlapping features. We demonstrate visual understanding of the model using Grad-CAM heatmaps and compare with 15 annotations by a radiologist. We highlight the need for careful adaptations of the models to foster reliability and applicability in a real-world setting. The code for the experiments in this work is available and maintained on GitHub.
