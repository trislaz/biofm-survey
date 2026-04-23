---
id: informing-acquisition-functions-via-2025
title: Informing Acquisition Functions via Foundation Models for Molecular Discovery
authors:
- Qi Chen
- Fabio Ramos
- Alán Aspuru-Guzik
- Florian Shkurti
year: 2025
venue: null
arxiv: '2512.13935'
doi: null
url: https://arxiv.org/abs/2512.13935v1
pdf_path: papers/informing-acquisition-functions-via-2025.pdf
md_path: papers/md/informing-acquisition-functions-via-2025.md
modalities:
- small-molecule
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:21+00:00'
updated_at: '2026-04-22T20:21:51+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Bayesian Optimization (BO) is a key methodology for accelerating molecular discovery by estimating the mapping from molecules to their properties while seeking the optimal candidate. Typically, BO iteratively updates a probabilistic surrogate model of this mapping and optimizes acquisition functions derived from the model to guide molecule selection. However, its performance is limited in low-data regimes with insufficient prior knowledge and vast candidate spaces. Large language models (LLMs) and chemistry foundation models offer rich priors to enhance BO, but high-dimensional features, costly in-context learning, and the computational burden of deep Bayesian surrogates hinder their full utilization. To address these challenges, we propose a likelihood-free BO method that bypasses explicit surrogate modeling and directly leverages priors from general LLMs and chemistry-specific foundation models to inform acquisition functions. Our method also learns a tree-structured partition of the molecular search space with local acquisition functions, enabling efficient candidate selection via Monte Carlo Tree Search. By further incorporating coarse-grained LLM-based clustering, it substantially improves scalability to large candidate sets by restricting acquisition function evaluations to clusters with statistically higher property values. We show through extensive experiments and ablations that the proposed method substantially improves scalability, robustness, and sample efficiency in LLM-guided BO for molecular discovery.
