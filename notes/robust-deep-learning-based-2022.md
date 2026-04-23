---
id: robust-deep-learning-based-2022
title: Robust deep learning-based protein sequence design using ProteinMPNN
authors: []
year: 2022
venue: null
arxiv: null
doi: 10.1126/science.add2187
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/robust-deep-learning-based-2022.md
modalities:
- protein-sequence
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

| # | Ablation | Variants | Metric | Result | Take-away |
|---|----------|----------|--------|--------|-----------|
| 1 | Backbone input features | dihedrals only (baseline) → +inter-atomic N/Cα/C/O/virtual-Cβ distances (exp 1) | CATH single-chain seq recovery | 41.2% → 49.0% | Pairwise distances are a much stronger inductive bias than dihedrals/frame orientations. |
| 2 | Edge updates in encoder | node-only → node + edge updates (exp 2 vs 3, combined w/ feat. above) | Seq recovery | up to 50.5% | Updating edge features in the MPNN encoder gives a further +1.5%. |
| 3 | Decoding order | fixed N→C → random order-agnostic autoregressive (exp 4) | Seq recovery | modest gain (→ ~52.4% native monomers) | Random-permutation decoding both improves recovery and unlocks fixed-region / binder design. |
| 4 | k-nearest-Cα neighbors | k ∈ {16, 24, 32, 48, 64} (Fig. S1A) | Seq recovery | saturates at k=32–48 | Local graphs suffice; long-range context unnecessary for seq design. |
| 5 | Homomer symmetry coupling | unconstrained / averaged probabilities / averaged logits (Fig. S1C) | Median seq recovery (homomers) | 52% / 53% / 55% | Tying via averaged logits is the best symmetry-aware decoding scheme. |
| 6 | Gaussian backbone noise during training | std = 0.0, 0.02, 0.1, 0.2, 0.3 Å (Fig. 2C, Table 1) | Recovery on PDB vs AF models; AF-predicted fold accuracy from designed seq | Noise lowers PDB recovery but raises recovery on AF models; 0.3 Å model yields 2–3× more designs with AF lDDT-Cα ≥ 90/95 | **Adding noise (~0.1–0.3 Å) trades a small native-recovery loss for sequences that map far more robustly back to the target structure — the design-relevant metric.** |
| 7 | Sampling temperature | low → high (Fig. 2D, S3A) | Diversity vs recovery | Big diversity gain, tiny recovery drop; mean log-prob correlates with recovery | Sample at higher T to diversify, then rank by ProteinMPNN log-prob. |
