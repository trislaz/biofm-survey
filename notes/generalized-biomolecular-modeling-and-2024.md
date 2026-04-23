---
id: generalized-biomolecular-modeling-and-2024
title: Generalized biomolecular modeling and design with RoseTTAFold All-Atom
authors: []
year: 2024
venue: null
arxiv: null
doi: 10.1126/science.adl2528
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/generalized-biomolecular-modeling-and-2024.md
modalities:
- protein-structure
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

Note: the Science paper does not present a classical component-level ablation in the main text, and the Cloudflare-gated supplement (Science + bioRxiv) was inaccessible at extraction time; the GitHub repo contains only inference docs. The table below captures the comparison/sensitivity analyses in the main text that play the role of ablations (multimodal vs unimodal baseline, with/without bound input, in/out of training distribution). Source: Krishna et al., *Science* 2024 (10.1126/science.adl2528), author-accepted manuscript via White Rose eprints.

| # | Variant / condition | Setting (vs reference) | Benchmark | Metric | Result | Take-away |
|---|---|---|---|---|---|---|
| 1 | Multimodal RFAA vs protein-only AF2 | adds NA / ligand / metal / PTM tokens | Protein-only structure prediction | median GDT | 85 vs 86 | Generalist training does **not** degrade protein-only accuracy |
| 2 | Multimodal RFAA vs RFNA (protein-NA specialist) | adds ligand/metal/PTM tokens | Protein–nucleic-acid complexes | median all-atom LDDT | 0.74 vs 0.78 | Small (~4 pt) cost on NA complexes from generalist training |
| 3 | RFAA (ligand-aware training) vs RF2 (no-ligand training) | training-data ablation | Recent PDB protein-ligand set, both confident (PAEi<10, pLDDT>0.8) | protein structure accuracy | RFAA > RF2 (Fig S4A) | Training with ligand context **improves** protein-only prediction (pocket flips, domain shifts) |
| 4 | Sequence-only input vs bound crystal + pocket given | input ablation (RFAA vs Vina with bound input) | PDB post-cutoff docking | <2 Å ligand-RMSD success | 42% (RFAA, seq-only) vs 52% (Vina, bound) | Most of RFAA's "loss" vs physics docking comes from also predicting backbone+sidechains from sequence |
| 5 | RFAA vs DiffDock | both deep-learning, RFAA seq-only, DiffDock bound | PDB post-cutoff docking | <2 Å ligand-RMSD success | 42% vs 38% | RFAA matches/exceeds DL docker despite harder task |
| 6 | RFAA vs AutoDock Vina server | head-to-head on CAMEO | CAMEO docking (149 interfaces) | <2 Å ligand-RMSD success | 32% vs 8% | Large gap over classical pipeline in fully-blind setting |
| 7 | Sequence homology to training: in vs out | BLAST e-value ≤1 vs >1 | 5,421 recent PDB complexes | <2 Å success | 35% vs 24% | Real but modest generalization drop on novel sequences |
| 8 | Ligand similarity to training: in vs out | Tanimoto ≥0.5 vs <0.5 | 1,310 ligand clusters | <2 Å success | 19% vs 14% | Generalizes to chemically novel ligands with ~5 pt drop |
| 9 | High vs low confidence filtering | PAE interaction <10 filter | CAMEO | success rate within filter | 77% of 43% confident hits <2 Å | Confidence head is well-calibrated → useful for triage |
| 10 | Native vs Tanimoto-nearest decoy ligand | input ablation (replace ligand) | PoseBusters | % cases native PAEi < decoy PAEi | 75.1% | Network discriminates real binders from look-alikes without explicit training |
| 11 | Rosetta ΔG bucket of native complex | physics-based stratification | 940 recent PDB cases | <2 Å success per bucket | 50% / 25% / 22% (<−30 / −30…0 / >0 REU) | Accuracy tracks physical interaction energy → model has learned interaction physics |

Top take-away: RFAA's headline result is a **generalist-vs-specialist near-tie** — adding small molecules, metals, NA, and PTMs costs ≤1 GDT vs AF2 on proteins and ~4 LDDT vs RFNA on protein–NA, while *adding* the ligand-aware training actually **improves** protein-only structure prediction over RF2 in the binding-site region; the gap to physics-based docking (Vina with bound input) is mostly an input-ablation artifact, not a modeling-quality gap.

