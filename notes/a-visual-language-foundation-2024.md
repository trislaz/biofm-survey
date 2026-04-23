---
id: a-visual-language-foundation-2024
title: A visual-language foundation model for computational pathology (CONCH)
authors: []
year: 2024
venue: null
arxiv: null
doi: 10.1038/s41591-024-02856-4
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/a-visual-language-foundation-2024.md
modalities:
- imaging-pathology
status: fetched
evidence_quality: full-text
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

Source: main text §"CONCH pretraining ablations" (p. ~81 discussion + Extended Data Fig. 10 caption, lines 81 & 257–259 of source MD). Two ablation axes were studied: (1) data filtering / pretraining objective and (2) domain-specific unimodal pretraining of the vision and text encoders. Metrics: zero-shot subtyping/grading (balanced accuracy; Cohen's κ for DHMC LUAD; quadratically weighted κ for SICAP) on 7 datasets, plus cross-modal retrieval on 3 image–text pair datasets.

| # | Axis | Variant | Setup | Reported effect |
|---|------|---------|-------|-----------------|
| 1 | Data filtering / objective | CONCH (CoCa, human-only, n=1,170,647) | Default model — CoCa objective on human-only filtered pairs | Best average zero-shot classification across 7 tasks |
| 2 | Data filtering / objective | CLIP, human-only (n=1,170,647) | Same data, CLIP objective instead of CoCa | Best average cross-modal retrieval; lower zero-shot classification than CoCa default |
| 3 | Data filtering / objective | H&E-only subset (n=457,372) | Restrict pretraining pairs to H&E images | Lower average zero-shot vs full human-only set — filtering too aggressively hurts |
| 4 | Data filtering / objective | Full unfiltered dataset (n=1,786,362) | No human/quality filtering | Underperforms human-only filtered CoCa — quality filtering matters |
| 5 | Unimodal pretraining | CONCH — No vision pretraining | Replace histopathology-SSL image encoder with ImageNet-pretrained encoder | Drop in zero-shot classification and retrieval — largest degradation among ablations |
| 6 | Unimodal pretraining | CONCH — No language pretraining | Randomly initialize text encoder instead of pathology-text pretraining | Drop in zero-shot classification and retrieval (smaller than vision ablation) |
| 7 | Unimodal pretraining | CONCH (full unimodal pretraining) | Vision SSL on histopath + LM pretraining on pathology text before contrastive align | Best across both zero-shot classification and retrieval — confirms value of domain-specific unimodal pretraining |

### Take-aways

- **Domain-specific unimodal pretraining is the single most impactful design choice**: ablating vision SSL pretraining (swap to ImageNet) causes the largest performance drop, and ablating language pretraining also degrades zero-shot classification and retrieval — authors highlight this as the most notable finding (lines 81, 259).
- **Caption-quality filtering beats raw scale**: human-curated (n≈1.17M) outperforms full unfiltered (n≈1.79M); restricting further to H&E-only (n≈0.46M) hurts — there is a sweet spot in filtering.
- **Objective choice is task-dependent**: CoCa wins on zero-shot classification on average, while pure CLIP wins on cross-modal retrieval — the captioning loss in CoCa trades a bit of retrieval alignment for stronger classification representations.
- **Limitation of the ablation**: only one pretraining scale is explored; no ablation over compute, encoder size, or prompt-ensemble strategy alongside these axes.

