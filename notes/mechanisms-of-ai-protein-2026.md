---
id: mechanisms-of-ai-protein-2026
title: Mechanisms of AI Protein Folding in ESMFold
authors:
- Kevin Lu
- Jannik Brinkmann
- Stefan Huber
- Aaron Mueller
- Yonatan Belinkov
- David Bau
- Chris Wendler
year: 2026
venue: null
arxiv: '2602.06020'
doi: null
url: https://arxiv.org/abs/2602.06020v2
pdf_path: papers/mechanisms-of-ai-protein-2026.pdf
md_path: papers/md/mechanisms-of-ai-protein-2026.md
modalities:
- protein-structure
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:03+00:00'
updated_at: '2026-04-22T20:22:36+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

How do protein structure prediction models fold proteins? We investigate this question by tracing how ESMFold folds a beta hairpin, a prevalent structural motif. Through counterfactual interventions on model latents, we identify two computational stages in the folding trunk. In the first stage, early blocks initialize pairwise biochemical signals: residue identities and associated biochemical features such as charge flow from sequence representations into pairwise representations. In the second stage, late blocks develop pairwise spatial features: distance and contact information accumulate in the pairwise representation. We demonstrate that the mechanisms underlying structural decisions of ESMFold can be localized, traced through interpretable representations, and manipulated with strong causal effects.
