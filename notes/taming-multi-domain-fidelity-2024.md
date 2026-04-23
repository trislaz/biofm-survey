---
id: taming-multi-domain-fidelity-2024
title: 'Taming Multi-Domain, -Fidelity Data: Towards Foundation Models for Atomistic
  Scale Simulations'
authors:
- Tomoya Shiota
- Kenji Ishihara
- Tuan Minh Do
- Toshio Mori
- Wataru Mizukami
year: 2024
venue: null
arxiv: '2412.13088'
doi: null
url: https://arxiv.org/abs/2412.13088v2
pdf_path: papers/taming-multi-domain-fidelity-2024.pdf
md_path: papers/md/taming-multi-domain-fidelity-2024.md
modalities:
- small-molecule
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:21+00:00'
updated_at: '2026-04-22T20:26:44+00:00'
is_fm: true
fm_classification_reason: MACE-style multi-domain pretraining toward atomistic FMs;
  releases pretrained model.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Machine learning interatomic potentials (MLIPs) are changing atomistic simulations in the field of chemistry and materials science. However, constructing a single universal MLIP that can accurately model molecular and crystalline systems remains challenging. A central obstacle is the integration of diverse datasets generated under different computational conditions. We present Total Energy Alignment (TEA), which is an approach that enables the seamless integration of heterogeneous quantum chemical datasets without redundant calculations. Using TEA, we trained MACE-Osaka24, the first open-source MLIP model based on a unified dataset covering molecular and crystalline systems. This universal model displays strong performances across diverse chemical systems, exhibiting similar or improved accuracies in predicting organic reaction barriers compared to those of specialized models, while effectively maintaining state-of-the-art accuracies for inorganic systems. These advancements pave the way for accelerated discoveries in the fields of chemistry and materials science via genuine foundation models for chemistry.

## Ablations (Rev 4)

> Note: paper has no dedicated "Ablations" section. The following are the ablation-style comparisons reported (TEA pipeline stages, model-size variants, and cross-architecture generalisation).

| # | Ablation axis | Variants compared | Benchmark / metric | Result | Take-away |
|---|---|---|---|---|---|
| 1 | TEA pipeline stage | (a) raw multi-fidelity QM9 (no TEA) → (b) +ICEA only → (c) +ICEA+AEC | QM9 PBE/PW vs ωB97M-D3(BJ) total-energy parity (RMSE, eV; R²) | (a) huge offset, R²≈low; (b) energies brought onto common scale; (c) RMSE = 0.8388 eV, R² = 0.9965 | Both stages of TEA are needed: ICEA removes inner-core/basis offsets, AEC then corrects atomization-energy/functional offsets — full pipeline is what unlocks dataset fusion |
| 2 | Model size (MACE-Osaka24) | small vs large | Biaryl-torsion barrier MAE (kcal/mol) vs CCSD(T1)* | small 0.695 → large 0.457 | Scaling MACE-Osaka24 from small→large gives ~0.24 kcal/mol gain, reaching MACE-OFF23-large quality (0.403) on organics |
| 3 | Model size (MACE-Osaka24) | small vs large | Transition1x reaction-energy / barrier MAE (eV) | small 0.336 / 0.457 → large 0.265 / 0.404 | Large variant best on reactive organic chemistry; ~20–30% MAE drop |
| 4 | Model size (MACE-Osaka24) | small vs large | Bulk-crystal lattice constant MAE (Å) vs PBE | small 0.0166 → large 0.0148 | Marginal gain on crystals; small already competitive with MACE-MP-0-large (0.0166) |
| 5 | Model size (MACE-Osaka24) | small vs large | HEA-NP geometry RMSD (Å) / CO adsorption RMSE (eV) | small 0.154 / 0.152 → large 0.156 / 0.341 | **Inverse scaling**: small beats large on out-of-domain HEA NP catalysis (CO adsorption: 0.152 vs 0.341 eV); larger model overfits or loses inorganic balance |
| 6 | Liquid-water RDF (size effect) | Osaka24-small-D3(BJ) vs Osaka24-large-D3(BJ) | O–O RDF vs PBE-D3(BJ) reference | large reproduces MACE-MP-0-D3(BJ) RDF; small sits between MP-0 and OFF23 | Dynamic-property fidelity depends on architecture+dataset balance, not just dataset size; large is needed for water RDF |
| 7 | Architecture generalisation of TEA | MACE vs M3GNet trained on TEA-aligned data (Appendix F) | training-set fit | M3GNet trained on the unified dataset converges and yields valid predictions | TEA is architecture-agnostic — benefits are not specific to MACE |
| 8 | TEA vs no-TEA training (implicit) | Multi-domain MACE-Osaka24 (TEA-merged molecular+crystalline) vs domain-specialist baselines (MACE-MP-0 inorganic-only, MACE-OFF23 organic-only) | All benchmarks above | Osaka24 matches or beats each specialist on its own domain (e.g. Transition1x: Osaka24-large 0.265 eV vs MP-0-large 0.519 eV reaction MAE; HEA NP RMSD: Osaka24-small 0.154 Å vs MP-0-small 0.259 Å) | Training on TEA-merged multi-domain data does **not** degrade in-domain accuracy and can actually improve it — i.e. negative-transfer feared from naive dataset mixing is removed by TEA |

**Count: 8 ablation-style comparisons.**

**Top take-away:** TEA's two stages (ICEA + AEC) are jointly necessary to fuse multi-fidelity datasets (RMSE 0.8388 eV; R² 0.9965 on QM9), and once they are applied, training a single MACE on the merged molecular+crystalline corpus matches or beats domain-specialist baselines on every benchmark — i.e. dataset unification via energy alignment removes the usual negative-transfer penalty of multi-domain MLIP training, without any architecture change.
