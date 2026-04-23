---
id: cents-generating-synthetic-electricity-2025
title: 'CENTS: Generating synthetic electricity consumption time series for rare and
  unseen scenarios'
authors:
- Michael Fuest
- Alfredo Cuesta
- Kalyan Veeramachaneni
year: 2025
venue: null
arxiv: '2501.14426'
doi: null
url: https://arxiv.org/abs/2501.14426v3
pdf_path: papers/cents-generating-synthetic-electricity-2025.pdf
md_path: papers/md/cents-generating-synthetic-electricity-2025.md
modalities:
- protein-structure
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:00+00:00'
updated_at: '2026-04-22T20:17:54+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Recent breakthroughs in large-scale generative modeling have demonstrated the potential of foundation models in domains such as natural language, computer vision, and protein structure prediction. However, their application in the energy and smart grid sector remains limited due to the scarcity and heterogeneity of high-quality data. In this work, we propose a method for creating high-fidelity electricity consumption time series data for rare and unseen context variables (e.g. location, building type, photovoltaics). Our approach, Context Encoding and Normalizing Time Series Generation, or CENTS, includes three key innovations: (i) A context normalization approach that enables inverse transformation for time series context variables unseen during training, (ii) a novel context encoder to condition any state-of-the-art time-series generator on arbitrary numbers and combinations of context variables, (iii) a framework for training this context encoder jointly with a time-series generator using an auxiliary context classification loss designed to increase expressivity of context embeddings and improve model performance. We further provide a comprehensive overview of different evaluation metrics for generative time series models. Our results highlight the efficacy of the proposed method in generating realistic household-level electricity consumption data, paving the way for training larger foundation models in the energy domain on synthetic as well as real-world data.
