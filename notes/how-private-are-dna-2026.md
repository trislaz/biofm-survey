---
id: how-private-are-dna-2026
title: How Private Are DNA Embeddings? Inverting Foundation Model Representations
  of Genomic Sequences
authors:
- Sofiane Ouaari
- Jules Kreuer
- Nico Pfeifer
year: 2026
venue: null
arxiv: '2603.06950'
doi: null
url: https://arxiv.org/abs/2603.06950v1
pdf_path: null
md_path: null
modalities:
- dna
status: seed
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:44+00:00'
updated_at: null
is_fm: false
fm_classification_reason: Privacy/inversion study of DNA embeddings.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

DNA foundation models have become transformative tools in bioinformatics and healthcare applications. Trained on vast genomic datasets, these models can be used to generate sequence embeddings, dense vector representations that capture complex genomic information. These embeddings are increasingly being shared via Embeddings-as-a-Service (EaaS) frameworks to facilitate downstream tasks, while supposedly protecting the privacy of the underlying raw sequences. However, as this practice becomes more prevalent, the security of these representations is being called into question. This study evaluates the resilience of DNA foundation models to model inversion attacks, whereby adversaries attempt to reconstruct sensitive training data from model outputs. In our study, the model's output for reconstructing the DNA sequence is a zero-shot embedding, which is then fed to a decoder. We evaluated the privacy of three DNA foundation models: DNABERT-2, Evo 2, and Nucleotide Transformer v2 (NTv2). Our results show that per-token embeddings allow near-perfect sequence reconstruction across all models. For mean-pooled embeddings, reconstruction quality degrades as sequence length increases, though it remains substantially above random baselines. Evo 2 and NTv2 prove to be most vulnerable, especially for shorter sequences with reconstruction similarities > 90%, while DNABERT-2's BPE tokenization provides the greatest resilience. We found that the correlation between embedding similarity and sequence similarity was a key predictor of reconstruction success. Our findings emphasize the urgent need for privacy-aware design in genomic foundation models prior to their widespread deployment in EaaS settings. Training code, model weights and evaluation pipeline are released on: https://github.com/not-a-feature/DNA-Embedding-Inversion.
