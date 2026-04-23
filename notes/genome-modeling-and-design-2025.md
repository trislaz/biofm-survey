---
id: genome-modeling-and-design-2025
title: Genome modeling and design across all domains of life with Evo 2
authors: []
year: 2025
venue: null
arxiv: null
doi: 10.1101/2025.02.18.638918
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/genome-modeling-and-design-2025.md
modalities:
- dna
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

Source: arcinstitute.org/news/blog/evo2 (blog post), github.com/ArcInstitute/evo2 (README/checkpoints). biorxiv preprint page returned 403; ablation numerics not directly extracted. Entries below are configuration variants released as checkpoints, not head-to-head accuracy ablations (those live in the preprint, which was inaccessible).

| # | Axis | Variant | Setting / Result | Source |
|---|------|---------|------------------|--------|
| 1 | Model scale | evo2_1b_base | 1B params, 8K context, requires FP8 (Hopper) | GitHub README |
| 2 | Model scale | evo2_7b / evo2_7b_base | 7B params; 1M ctx (long) and 8K ctx (base); runs in bf16 without Transformer Engine on any supported GPU | GitHub README |
| 3 | Model scale | evo2_40b / evo2_40b_base | 40B params; 1M ctx and 8K ctx; needs multi-H100 + FP8 | GitHub README |
| 4 | Model scale (post-hoc) | evo2_20b | 20B params, 1M ctx; reported "40B-level performance with double the speed" | GitHub README v0.5.0 release |
| 5 | Context length | 8K vs 262K vs 1M | Released as separate checkpoints (`*_base`=8K, `evo2_7b_262k`=262K, `evo2_7b`/`evo2_40b`=1M); architecture (StripedHyena 2) enables 8× more nucleotides per context vs Evo 1 | GitHub README; blog |
| 6 | Tokenizer | Single-nucleotide (byte-level) | Models DNA at single-nucleotide resolution; 8.8T training tokens on OpenGenome2 (blog cites 9.3T nt across 128k genomes) | GitHub README; blog |
| 7 | Architecture | StripedHyena 2 vs Transformer | StripedHyena 2 (convolutional multi-hybrid) chosen to scale to 1M-nt context; sister ML paper "Systems and Algorithms for Convolutional Multi-Hybrid LMs at Scale" | Blog |
| 8 | Embedding layer | Final vs intermediate | "Intermediate embeddings work better than final embeddings" for downstream tasks | GitHub README (Embeddings section) |
| 9 | Training data scope | +Eukaryotes vs Evo 1 (prokaryote-only) | Evo 2 adds humans, plants, eukaryotes, metagenomes (128k genomes) → 30× more training data than Evo 1 | Blog |
| 10 | Safety filtering | Pathogen exclusion | Human/complex-organism pathogens excluded from base dataset; model declines productive queries about them | Blog |

Count: 10 ablation/variant rows.

Top take-away: Evo 2's headline scaling story is **architectural, not just parametric** — moving to StripedHyena 2 is what unlocks the 1M-nucleotide context (8× Evo 1) and the 30× data scale-up; the 1B/7B/20B/40B checkpoints exist primarily to trade FP8/H100 hardware requirements against capability, with the 20B release showing parameter count is not monotonic with deployable performance.
