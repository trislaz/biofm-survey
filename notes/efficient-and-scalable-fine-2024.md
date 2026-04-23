---
id: efficient-and-scalable-fine-2024
title: Efficient and Scalable Fine-Tune of Language Models for Genome Understanding
authors:
- Huixin Zhan
- Ying Nian Wu
- Zijun Zhang
year: 2024
venue: null
arxiv: '2402.08075'
doi: null
url: https://arxiv.org/abs/2402.08075v1
pdf_path: papers/efficient-and-scalable-fine-2024.pdf
md_path: papers/md/efficient-and-scalable-fine-2024.md
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
updated_at: '2026-04-22T20:19:16+00:00'
is_fm: false
fm_classification_reason: Fine-tuning method for genome LMs; not a new FM.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Although DNA foundation models have advanced the understanding of genomes, they still face significant challenges in the limited scale and diversity of genomic data. This limitation starkly contrasts with the success of natural language foundation models, which thrive on substantially larger scales. Furthermore, genome understanding involves numerous downstream genome annotation tasks with inherent data heterogeneity, thereby necessitating more efficient and robust fine-tuning methods tailored for genomics. Here, we present \textsc{Lingo}: \textsc{L}anguage prefix f\textsc{In}e-tuning for \textsc{G}en\textsc{O}mes. Unlike DNA foundation models, \textsc{Lingo} strategically leverages natural language foundation models' contextual cues, recalibrating their linguistic knowledge to genomic sequences. \textsc{Lingo} further accommodates numerous, heterogeneous downstream fine-tune tasks by an adaptive rank sampling method that prunes and stochastically reintroduces pruned singular vectors within small computational budgets. Adaptive rank sampling outperformed existing fine-tuning methods on all benchmarked 14 genome understanding tasks, while requiring fewer than 2\% of trainable parameters as genomic-specific adapters. Impressively, applying these adapters on natural language foundation models matched or even exceeded the performance of DNA foundation models. \textsc{Lingo} presents a new paradigm of efficient and scalable genome understanding via genomic-specific adapters on language models.
