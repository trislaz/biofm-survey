---
id: universal-cell-embeddings-a-2023
title: 'Universal Cell Embeddings: a foundation model for cell biology'
authors: []
year: 2023
venue: null
arxiv: null
doi: 10.1101/2023.11.28.568918
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/universal-cell-embeddings-a-2023.md
modalities:
- scrna
status: abstract-only
evidence_quality: abstract+metadata
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: Added in rev4 missing-FM brainstorm; canonical bio-FM.
---

## Ablations (Rev 4)

Sources: bioRxiv preprint (2023.11.28.568918) abstract+metadata; GitHub `snap-stanford/UCE` README; CZI Virtual Cells model card. Direct full-text fetch was blocked (HTTP 403); details below are the ablation axes the paper exposes via released artefacts and reported headline findings — exact metric values require the supplement.

| # | Ablation axis | Variants compared | Reported finding (direction) |
|---|---|---|---|
| 1 | Model depth / size | 4-layer (~tens of M params) vs 33-layer (~650M params) Transformer | 33-layer gives best biological-signal fidelity and cross-species generalisation; 4-layer is faster/cheaper but loses resolution on complex tissues. Embeddings are not interchangeable between the two. |
| 2 | Training species coverage | Trained on 8 species (Integrated Mega-scale Atlas, ~36M cells) vs held-out species | Zero-shot embedding works on unseen species with available proteomes (e.g., green monkey, chicken); degrades on evolutionarily distant species (e.g., Drosophila). |
| 3 | Gene-token representation | ESM2 protein-sequence embeddings as gene tokens vs gene-ID / learned-vocabulary baselines | ESM2 protein embeddings are the mechanism enabling species-agnostic, vocabulary-free tokenisation; required for cross-species transfer and for embedding novel/unseen genes. |
| 4 | Gene-set inclusion | Only protein-coding genes with available ESM2 embeddings | Non-coding / missing-embedding genes are dropped; ablation motivates protein-embedding tokenisation as the core design choice. |
| 5 | Batch / dataset integration | UCE zero-shot vs scVI, scArches, Geneformer, scGPT (integration & cell-type benchmarks) | UCE clusters by biology rather than batch without any fine-tuning; reported to match or exceed supervised integration baselines on bio-conservation while requiring no per-dataset training. |

Count: 5 ablation axes captured.

Top take-away: UCE's headline ablation is the **ESM2 protein-embedding gene tokenizer combined with scale (33-layer / ~650M params)** — together they enable a single frozen model to embed cells from unseen species and datasets zero-shot, which is the property that distinguishes UCE from prior scRNA foundation models (Geneformer, scGPT) that rely on a fixed gene vocabulary.

