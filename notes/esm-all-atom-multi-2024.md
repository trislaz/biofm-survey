---
id: esm-all-atom-multi-2024
title: 'ESM All-Atom: Multi-scale Protein Language Model for Unified Molecular Modeling'
authors:
- Kangjie Zheng
- Siyu Long
- Tianyu Lu
- Junwei Yang
- Xinyu Dai
- Ming Zhang
- Zaiqing Nie
- Wei-Ying Ma
- Hao Zhou
year: 2024
venue: null
arxiv: '2403.12995'
doi: null
url: https://arxiv.org/abs/2403.12995v4
pdf_path: papers/esm-all-atom-multi-2024.pdf
md_path: papers/md/esm-all-atom-multi-2024.md
modalities:
- protein-sequence
- protein-structure
- small-molecule
status: extracted
evidence_quality: medium
tags:
- multi-scale
- code-switching
- unified-molecular-modeling
- protein-molecule-interaction
- position-encoding
parameters: 35M
training_tokens: null
training_compute: 16xA100 3 days
references_chased: false
added_at: '2026-04-22T19:36:52+00:00'
updated_at: '2026-04-22T20:19:46+00:00'
is_fm: true
fm_classification_reason: 'ESM-AA: new pretrained multi-scale protein/molecule FM.'
---

## TL;DR

ESM-AA extends ESM-2 to jointly handle protein residues and small-molecule atoms in a single 35M-parameter Transformer by "code-switching": randomly unzipping 1% of residues into their constituent atoms during pre-training and using a multi-scale position encoding (RoPE for residues, Gaussian-kernel 3D distance matrices for atoms). Pre-trained on 8M AlphaFoldDB proteins + 19M molecules (209M conformations) with MLM + pair-wise distance recovery, ESM-AA achieves SOTA on enzyme-substrate affinity regression (MSE 0.607 vs 0.642 baseline) and drug-target affinity (MSE 0.196 vs 0.219) while preserving ESM-2-level protein understanding (SS3, contact prediction). It eliminates the need for separate protein and molecule encoders.

## Model

- **Architecture**: 12-layer Transformer, 20 attention heads, d_model=480, FFN=1920, 35M parameters. Initialized from ESM-2 35M checkpoint.
- **Multi-scale Position Encoding (MSPE)**: Two components: (1) Residue-scale PE — RoPE inherited from ESM-2; atoms from an unzipped residue share the parent residue's RoPE index; small-molecule atoms get RoPE(0). (2) Atom-scale PE — Euclidean distance matrix between atoms passed through Gaussian kernels, added as bias in self-attention (à la Uni-Mol/Zhou et al. 2023). Residue-residue pairs get 0 atom-scale bias.
- **Code-switch sequences**: Randomly unzip residues into ordered constituent atoms (PDB atom order). Unzipped residue token is retained alongside its atoms to enable residue–atom alignment learning. Max sequence length extended from 1024 (ESM-2) to 2048.
- **Inputs**: Either a protein (code-switch sequence) or a small molecule (atom sequence with 3D coordinates). Not paired protein–molecule data during pre-training.

## Data

- **Protein**: AlphaFoldDB — 8M sequences+structures with pLDDT>90 (AlphaFold2-predicted).
- **Molecule**: 19M molecules, 209M conformations generated via ETKDG + MMFF (from Uni-Mol / Zhou et al. 2023).
- Mixed into a single training set; each batch item is either a protein or a molecule (not paired).
- **Downstream**: KM (11.7K enzyme-substrate pairs), Davis (30K drug-target pairs), ESP (68.8K enzyme-substrate classification), MoleculeNet (QM7/8/9, HIV, BACE, BBBP, TOX21, PCBA, SIDER, MUV), TAPE protein tasks (SSP, contact prediction), DUD-E virtual screening, protein function annotation (EC, GO).

## Training Recipe

- **Objectives**: (1) Multi-scale MLM — mask 15% of tokens (both residues and atoms), predict masked types. Loss weight 4.0, cross-entropy. (2) Pair-wise Distance Recovery (PDR) — corrupt atom coordinates by noise within ε=1Å, recover ground-truth Euclidean distances between atom pairs within the same residue. Loss weight 10.0, SmoothL1.
- **Unzip ratio**: 1.0% of residues unzipped → sequence ~1.08× longer on average.
- **Optimizer**: Adam (β1=0.9, β2=0.98), polynomial LR decay from 4e-4 to 4e-5, warmup 5K steps.
- **Training**: 300K steps, max 256K tokens/batch, 16× NVIDIA A100, ~3 days.
- **Initialization**: ESM-2 35M checkpoint loaded; only sinusoidal PE replaced by RoPE + atom-scale bias.
- **Fine-tuning**: Encoders frozen (ProSmith framework); fusion block is a 6-layer Transformer (d=768). Unzip turned off at fine-tuning time.

## Key Ablations & Design Choices (MOST IMPORTANT, quantitative)

All ablations on Enzyme-Substrate Affinity Regression (ESAR) unless noted:

| Ablation | MSE (Δ) | R² (Δ) |
|---|---|---|
| Full ESM-AA | **0.627** | **0.546** |
| w/o Atom-scale PE (ASPE) | 0.639 (+0.012) | 0.537 (−0.009) |
| w/o Residue-scale PE (RSPE) | 0.676 (+0.049) | 0.511 (−0.035) |
| w/o MLM Loss | 0.642 (+0.015) | 0.535 (−0.011) |
| w/o PDR Loss | 0.645 (+0.018) | 0.533 (−0.013) |
| w/o Molecule Data | 0.648 (+0.021) | 0.531 (−0.015) |
| w/o Protein Data | 0.708 (+0.081) | 0.487 (−0.059) |
| w/o Unzip Operation | 0.638 (+0.011) | 0.538 (−0.008) |

- **RSPE >> ASPE** in importance (Δ MSE +0.049 vs +0.012), confirming residue-level context is the dominant signal.
- **Removing protein data** is far more damaging than removing molecule data (+0.081 vs +0.021 MSE), because unzip alone provides some atomic information.
- **PDR slightly more important than MLM** for atom-scale tasks (+0.018 vs +0.015), attributed to structural information being more critical than atom type.
- **Unified model always beats separate encoders**: ESM-AA₃₅M for both protein+molecule outperforms ESM-2₂₃₅M + Uni-Mol₄₈M (ESAR MSE 0.607 vs 0.642; DTA MSE 0.196 vs 0.219), even though the baseline uses 283M total params vs 35M.
- **Protein understanding preserved**: SS3 accuracy ESM-AA 0.79 vs ESM-2 0.80 (CB513); contact prediction long-range P@L/5 ESM-AA 0.48 vs ESM-2 0.49 — negligible degradation.
- **Molecular benchmarks**: ESM-AA competitive with Uni-Mol on MoleculeNet (QM7 MAE 60.9 vs 58.9; BACE AUC 83.5 vs 83.2; SIDER AUC 63.6 vs 57.7).
- **Virtual screening** (DUD-E zero-shot): ESM-AA AUROC 80.02% vs DrugCLIP 81.72%, beating Glide-SP (76.70%) and Vina (71.70%).

## Reported Insights

- Code-switching (borrowing from multilingual NLP) is an effective metaphor: treating residue-scale and atom-scale as two "languages" enables aligned multi-scale representation learning.
- A single unified encoder for proteins and molecules produces better-aligned embedding spaces (shown via PCA visualization) than combining two separate pre-trained encoders, even when the separate encoders are individually larger.
- The unzip operation is the critical bridge — without it, molecule data alone cannot teach the model atom-scale protein knowledge.
- PDR within residues (not across residues) avoids introducing inter-residue interactions dissimilar to small molecules.
- The approach is compatible with any ESM-family checkpoint; loading a larger ESM-2 should further improve protein understanding.

## References Worth Chasing

- ESM-2 (Lin et al., 2022b / 2023, doi:10.1126/science.ade2574) — base PLM architecture and checkpoint
- Uni-Mol (Zhou et al., 2023, ICLR) — 3D molecular pre-training framework, molecule data source, atom-scale PE design
- ProSmith (Kroll et al., 2023b) — multimodal protein-molecule interaction benchmark framework
- AlphaFold2 (Jumper et al., 2021, doi:10.1038/s41586-021-03819-2) — structure source for protein pre-training data
- RoPE / RoFormer (Su et al., 2021, arXiv:2104.09864) — rotary position embedding used for residue-scale PE
- ESM-1b / ESM (Rives et al., 2021, PNAS) — foundational protein language model
- GET (Kong et al., 2023) — equivariant bi-level attention for unified multi-scale molecular modeling
- DrugCLIP (Gao et al., 2024) — contrastive protein-molecule representation for virtual screening
- GearNet (Zhang et al., 2022, arXiv:2203.06125) — geometric structure pre-training for protein representation
- LM-Design (Verkuil et al., 2022) — protein design with language models
- ProtGPT2 (Ferruz et al., 2022) — autoregressive protein generation
- ProGen2 (Nijkamp et al., 2022, arXiv:2206.13517) — scaling protein language models
- MSA Transformer (Rao et al., 2021) — extending MLM to MSA data
- DeepDTA (Öztürk et al., 2018) — classic drug-target affinity baseline

## Notes / Open Questions

- Model is very small (35M); no scaling experiments reported. How does performance change with ESM-2 650M or 3B initialization?
- Only 1% unzip ratio used; the paper does not systematically ablate this hyperparameter.
- Pre-training does **not** use paired protein–molecule data; the alignment emerges purely from shared architecture + code-switching. Would contrastive protein–molecule pairs further improve?
- Fine-tuning freezes encoders; it's unclear how much unfreezing or LoRA-style adaptation would help.
- No comparison against recent structure-aware PLMs like ESM-IF or ProteinMPNN.
- Coordinate noise ε=1Å for PDR — sensitivity to this threshold not explored.
- The approach processes proteins as 1D sequences with optional atom unzipping; it does not model full 3D protein structure at inference time (unzip is off during fine-tuning).

## Ablations (Rev 4)

Main ablation (Table 3) on Enzyme-Substrate Affinity Regression (ESAR); deltas relative to full ESM-AA (MSE 0.627, R² 0.546). Lower MSE / higher R² is better.

| # | Variant | MSE ↓ (Δ) | R² ↑ (Δ) | Scope | Take-away |
|---|---------|-----------|----------|-------|-----------|
| 1 | w/o ASPE (atom-scale position encoding) | 0.639 (+0.012) | 0.537 (-0.009) | ESAR | Atoms lose positional identity; degrades fusion. |
| 2 | w/o RSPE (residue-scale RoPE) | 0.676 (+0.049) | 0.511 (-0.035) | ESAR | Largest single-component drop on ESAR — residue PE is critical. |
| 3 | w/o MLM loss | 0.642 (+0.015) | 0.535 (-0.011) | ESAR | Modest on ESAR, but catastrophic on Contact Prediction (P@L drops to ~0.03). |
| 4 | w/o PDR loss (pairwise distance recovery) | 0.645 (+0.018) | 0.533 (-0.013) | ESAR | Bigger hit than removing MLM → atom-scale structure signal matters more than atom MLM. |
| 5 | w/o molecule data | 0.648 (+0.021) | 0.531 (-0.015) | ESAR | Unzip op partially compensates by giving model atomic exposure. |
| 6 | w/o protein data | 0.708 (+0.081) | 0.487 (-0.059) | ESAR | Worst overall — protein knowledge is the dominant pillar. |
| 7 | w/o unzip operation | 0.638 (+0.011) | 0.538 (-0.008) | ESAR | Smallest ESAR hit, but devastating for molecule-only tasks (BACE 83.5→61.6). |
| 8 | Encoder combo: ESM-2 + Uni-Mol (no ESM-AA) | 0.642 (+0.035 vs unified) | 0.536 (-0.024) | ESAR / App. G Tab. 11 | Two separate SOTA models < one unified ESM-AA. |
| 9 | Encoder combo: ESM-AA (protein) + Uni-Mol (molecule) | 0.638 (+0.031) | 0.539 (-0.021) | ESAR / App. G | Even partial use of ESM-AA helps via implicit alignment. |
| 10 | Encoder combo: ESM-2 (protein) + ESM-AA (molecule) | 0.622 (+0.015) | 0.550 (-0.010) | ESAR / App. G | Same conclusion — unified ESM-AA on both sides wins. |
| 11 | w/o RSPE — Contact Prediction | P@L long-range 0.02 vs 0.29 | — | App. G Tab. 12 | Removing residue PE collapses long-range contact signal. |
| 12 | w/o MLM — Contact Prediction | P@L long-range 0.03 vs 0.29 | — | App. G Tab. 12 | MLM is the *primary* driver of protein semantic learning. |
| 13 | w/o ASPE — Molecule tasks (BACE/BBBP/MUV/HIV) | BACE 73.99 vs 83.5 | — | App. G Tab. 13 | Atom PE is the unique atom identifier; biggest molecule-side drop alongside w/o Unzip. |
| 14 | w/o Unzip — Molecule tasks | BACE 61.57 vs 83.5; MUV 59.59 vs 76.2 | — | App. G Tab. 13 | Unzip is essential for atom-scale representation despite being optional at fine-tune. |

**Count: 14 ablation conditions** across one main table (7 component knock-outs on ESAR) and three appendix tables (encoder combinations, protein-only contact prediction, molecule-only property prediction).

**Top take-away:** No single component dominates universally — *which* component matters most depends on the downstream scale. On the joint protein-molecule ESAR task, **removing protein pre-training data is by far the worst (+0.081 MSE)**, confirming protein knowledge is the backbone. But the component-level story is task-dependent: **RSPE + MLM are indispensable for residue-scale tasks** (long-range contact P@L collapses to ~0.02–0.03 without them), while **ASPE + the Unzip operation are indispensable for atom-scale molecular tasks** (BACE drops ~22 points without Unzip). The PDR loss matters more than atom-MLM, showing that *structural* atom signal beats *categorical* atom signal. Finally, App. G Table 11 shows a unified ESM-AA encoder on both modalities beats any combination of separately pre-trained ESM-2 + Uni-Mol — validating the central thesis that joint multi-scale pre-training is more than the sum of its parts.
