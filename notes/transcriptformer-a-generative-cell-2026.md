---
id: transcriptformer-a-generative-cell-2026
title: 'TranscriptFormer: A generative cell atlas across 1.5 billion years of evolution'
authors:
- James D. Pearce
- Sara E. Simmonds
- Gita Mahmoudabadi
- Lakshmi Krishnan
- Giovanni Palla
- Ana-Maria Istrate
- Alexander Tarashansky
- Benjamin Nelson
- Omar Valenzuela
- Donghui Li
- Stephen R. Quake
- Theofanis Karaletsos
year: 2026
venue: Science
arxiv: null
doi: 10.1126/science.aec8514
url: https://www.science.org/doi/10.1126/science.aec8514
pdf_path: null
md_path: null
modalities:
- scrna
status: extracted
evidence_quality: abstract+metadata
tags:
- transformer
- autoregressive
- cross-species
- single-cell-transcriptomics
- zero-shot-transfer
parameters: 368M/444M/542M trainable (variant-dependent) + frozen protein embeddings
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-05-08T10:23:23+00:00'
updated_at: '2026-05-08T10:58:10+00:00'
is_fm: true
fm_classification_reason: 'TranscriptFormer: pretrained generative single-cell transcriptome foundation model.'
---

## TL;DR

TranscriptFormer is a transformer-based generative foundation model family for single-cell RNA sequencing (scRNA-seq) data across species. The public model release describes three variants trained on up to 112 million cells spanning 12 species across ~1.53 billion years of evolution, with strong zero-shot transfer claims for cross-species cell-type annotation and human disease-state identification. The Science paper URL is in this note, and current extraction is based on the official model repository summary and the linked preprint metadata because the Science and bioRxiv domains were not reachable from this execution environment.

## Model

- **Family**: TranscriptFormer (TF-Sapiens, TF-Exemplar, TF-Metazoa).
- **Core design**: autoregressive transformer model that jointly models genes and expression counts per cell.
- **Reported parameter scales**:
  - **TF-Sapiens**: 368 million trainable parameters (+61 million non-trainable).
  - **TF-Metazoa**: 444 million trainable (+633 million non-trainable).
  - **TF-Exemplar**: 542 million trainable (+282 million non-trainable).
- **Embedding strategy**: uses frozen pretrained protein embeddings (Evolutionary Scale Modeling 2, ESM-2) as part of the model input stack.

## Data

- **Maximum pretraining scale**: 112 million single-cell transcriptomes.
- **Species coverage (largest variant)**: 12 species including six vertebrates, four invertebrates, one fungus, and one protist.
- **Temporal span**: 1.53 billion years of evolution (as reported in the release summary).

## Training Recipe

- **Objective family**: generative autoregressive modeling over cell transcriptome sequences.
- **Variants**:
  - Human-only model (TF-Sapiens).
  - Human + four model organisms (TF-Exemplar).
  - Full cross-species model across 12 species (TF-Metazoa).
- **Training-token and compute budgets**: not disclosed in the accessible sources used for this extraction.

## Key Ablations & Design Choices

Accessible sources (official README + model release notes) emphasize cross-species transfer and variant scaling, but do not expose a full ablation table in the retrieved content.

- **Scale/coverage design choice**: comparing human-only vs few-species vs 12-species variants is the primary reported experimental axis.
- **Generalization design choice**: explicit support for out-of-distribution species via pretrained embedding extensions is part of the released inference pipeline.
- **Evidence gap**: detailed controlled ablation numbers were not available in the reachable sources in this environment.

## Reported Insights

- A generative transcriptome foundation model can transfer cell-type representations across distant species.
- Cross-species training appears to improve zero-shot transfer breadth relative to human-only training.
- The model family is positioned as a reusable backbone for embedding extraction and downstream cell-state inference.

## Notes / Open Questions

- The Science DOI page and bioRxiv full text were not directly reachable from this environment (domain-resolution failures), so this note is based on official repository statements and linked metadata rather than a full manuscript PDF parse.
- Once direct paper access is available, this note should be upgraded with:
  - explicit benchmark tables,
  - architecture hyperparameters,
  - and controlled ablations with exact metrics.

## Sources

- Science DOI landing page: <https://www.science.org/doi/10.1126/science.aec8514>
- Official model repository: <https://github.com/czi-ai/transcriptformer>
- Linked preprint in official repository: <https://www.biorxiv.org/content/10.1101/2025.04.25.650731v2>

## Issue Q&A

> **Q** ([#7](https://github.com/trislaz/biofm-survey/issues/7)): Please add this FM: https://www.science.org/doi/10.1126/science.aec8514. **A**: Added and expanded with extracted analysis from reachable official sources (Science DOI metadata + model repository + linked preprint), with limitations documented for direct manuscript download in this environment ([note](https://github.com/trislaz/biofm-survey/blob/main/notes/transcriptformer-a-generative-cell-2026.md)).
