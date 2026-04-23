---
id: accurate-structure-prediction-of-2024
title: Accurate structure prediction of biomolecular interactions with AlphaFold 3
authors: []
year: 2024
venue: null
arxiv: null
doi: 10.1038/s41586-024-07487-w
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/accurate-structure-prediction-of-2024.md
modalities:
- protein-structure
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

AF3 reports comparatively few formal ablation tables; most evidence is qualitative/architectural justifications and Extended Data figures. Ablation-style findings extracted from the main text and Methods:

| # | Ablation / variant | Setting | Effect | Source |
|---|---|---|---|---|
| 1 | Cross-distillation from AlphaFold-Multimer v2.3 predictions | Enrich training set with AFM-predicted structures whose disordered regions are extended loops | "Greatly reduced" hallucination of compact structure in disordered regions; improves CAID 2 disorder benchmark | §Network architecture and training; Extended Data Fig. 1 |
| 2 | Fine-tuning with larger crop sizes (384 → 640 → 768 tokens) | Two sequential fine-tuning stages after initial training | Improves all metrics; especially large uplift on protein–protein interfaces | §Network architecture and training; Extended Data Fig. 2 |
| 3 | Removing structure module complexity (frames, torsions, equivariance) → diffusion module on raw atom coords | Replace AF2 structure module with standard diffusion; no rotational/translational equivariance; no torsion parametrization; no violation losses | "Only a modest effect on prediction accuracy" (observed in AF2); allows handling of arbitrary ligands without special casing; high-noise denoising captures global structure, low-noise captures local stereochemistry | §Network architecture and training |
| 4 | De-emphasized MSA stack (4 pair-weighted-averaging blocks vs full evoformer) | Pairformer (48 blocks) operates only on pair + single rep; MSA representation discarded after trunk | Maintains accuracy; AF3 shows similar MSA-depth dependence to AFM v2.3 (shallow MSAs still hurt) | §Network architecture and training; Extended Data Fig. 7a |
| 5 | Diffusion "rollout" for confidence-head training | Mini full-structure rollout with larger step size during training to enable PAE/pLDDT/PDE supervision | Required because per-step diffusion training cannot regress final-structure error directly; yields well-calibrated confidences | §Network architecture and training; Fig. 2c |
| 6 | Multi-seed sampling (5 seeds × 5 diffusion samples = 25) | Used at inference instead of diffusion guidance to enforce chirality / avoid clashes | Achieves correct chirality and high-quality stereochemistry without explicit guidance terms | §Inference regime; §PoseBusters |
| 7 | Pocket-conditioned AF3 variant | Fine-tuned with extra token feature marking pocket residues within 6 Å of a ligand entity | Boosts protein–ligand docking accuracy when pocket info is provided (matches/exceeds methods that exploit pocket info) | §PoseBusters; Extended Data Fig. 4a |
| 8 | Earlier training cut-off (30 Sep 2019) AF3 model | Same architecture, retrained with earlier PDB cut-off for PoseBusters | Still beats Vina (P = 2.27 × 10⁻¹³) and RoseTTAFold All-Atom (P = 4.45 × 10⁻²⁵) blind; isolates leakage as a confound | §Accuracy across complex types; §PoseBusters |
| 9 | Adaptive training-set sampling probabilities + early stopping on weighted metric mix | Some capabilities saturate / overfit early while others undertrain | Per-set sampling reweighting and weighted-metric early stopping recover best joint checkpoint (Supplementary Table 7) | §Network architecture and training |

### Take-aways

- **Top take-away:** AF3's biggest empirically validated design choice is **cross-distillation on AlphaFold-Multimer predictions** to suppress diffusion-induced hallucination in disordered regions — without it, the generative diffusion backbone produces plausible-looking but spurious compact structure, and disorder-prediction (CAID 2) accuracy drops substantially.
- Generative diffusion can replace the equivariant structure module with **no meaningful accuracy loss** while removing torsion parametrization, violation losses, and equivariance machinery — a strong "less is more" signal for general-molecule modeling.
- MSAs can be deeply de-emphasized in the trunk (single-pass pair-weighted averaging, 4 blocks) yet **MSA depth still bottlenecks accuracy**, indicating the trunk simplification did not eliminate evolutionary dependence.
- Large-crop fine-tuning is disproportionately important for **interface** quality vs intra-chain quality, consistent with interfaces requiring longer-range context.
- Stereochemical correctness (chirality, clash-free) is achieved by **sample-and-rank over 25 diffusion samples**, not by physics-based guidance — a pragmatic substitute for inductive bias.
- Pocket-conditioning via a single binary token feature is enough to match pocket-aware docking baselines, suggesting modest conditioning suffices when the backbone model is strong.

