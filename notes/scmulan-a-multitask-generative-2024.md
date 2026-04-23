---
id: scmulan-a-multitask-generative-2024
title: 'scMulan: a multitask generative pre-trained language model for single-cell
  analysis'
authors: []
year: 2024
venue: null
arxiv: null
doi: 10.1101/2024.01.25.577152
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/scmulan-a-multitask-generative-2024.md
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

Full text on bioRxiv (`v1.full`, `v1.full.pdf`, and `early/2024/01/29/...full.pdf`) returned HTTP 403 (Cloudflare challenge); the Springer RECOMB 2024 chapter page exposes only the abstract; the GitHub repo (`SuperBianC/scMulan`) and the OpenAlex/Semantic Scholar abstracts contain no ablation reporting. No ablation experiments could be extracted from accessible sources.

| # | Component ablated | Setting / variant | Metric | Result | Δ vs. full | Source |
|---|-------------------|-------------------|--------|--------|-----------|--------|
| — | not retrievable   | —                 | —      | —      | —         | bioRxiv full text inaccessible (403) |

**Count:** 0 ablations extractable from open sources.

**Top take-away:** scMulan's ablation evidence is locked behind the bioRxiv full text (Cloudflare-gated) and is not surfaced in the Springer chapter abstract, the GitHub README, or indexed metadata; a Rev 5 pass should obtain the PDF directly (e.g., institutional access or author site) before any ablation-based claims are made about the contribution of the c-sentence format, task-token conditioning, or the 100M-cell pre-training corpus.
