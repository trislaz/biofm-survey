---
id: unigradicon-a-foundation-model-2024
title: 'uniGradICON: A Foundation Model for Medical Image Registration'
authors:
- Lin Tian
- Hastings Greer
- Roland Kwitt
- Francois-Xavier Vialard
- Raul San Jose Estepar
- Sylvain Bouix
- Richard Rushmore
- Marc Niethammer
year: 2024
venue: null
arxiv: '2403.05780'
doi: null
url: https://arxiv.org/abs/2403.05780v1
pdf_path: papers/unigradicon-a-foundation-model-2024.pdf
md_path: papers/md/unigradicon-a-foundation-model-2024.md
modalities:
- imaging-pathology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T20:50:54+00:00'
updated_at: '2026-04-22T20:52:46+00:00'
is_fm: true
fm_classification_reason: 'uniGradICON: pretrained foundation model for medical image
  registration.'
---

## Abstract (from arxiv)

Conventional medical image registration approaches directly optimize over the parameters of a transformation model. These approaches have been highly successful and are used generically for registrations of different anatomical regions. Recent deep registration networks are incredibly fast and accurate but are only trained for specific tasks. Hence, they are no longer generic registration approaches. We therefore propose uniGradICON, a first step toward a foundation model for registration providing 1) great performance \emph{across} multiple datasets which is not feasible for current learning-based registration methods, 2) zero-shot capabilities for new registration tasks suitable for different acquisitions, anatomical regions, and modalities compared to the training dataset, and 3) a strong initialization for finetuning on out-of-distribution registration tasks. UniGradICON unifies the speed and accuracy benefits of learning-based registration algorithms with the generic applicability of conventional non-deep-learning approaches. We extensively trained and evaluated uniGradICON on twelve different public datasets. Our code and the uniGradICON model are available at https://github.com/uncbiag/uniGradICON.

## Ablations (Rev 4)

| # | Ablation | Setup | Key result | Take-away |
|---|----------|-------|------------|-----------|
| 1 | Regularizer choice (GradICON vs diffusion) | Universal VoxelMorph-SVF trained on same composite dataset vs uniGradICON | uniGradICON beats universal VoxelMorph across COPDGene/OAI/HCP/L2R-Abdomen (e.g. DICE 68.9 vs 55.0 on OAI; 76.2 vs 44.2 on HCP); LapIRN-based universal model failed to train | Weaker GradICON regularizer is what enables a single universal registration model; diffusion-regularized variants underperform or fail |
| 2 | Universal vs task-specific training | uniGradICON vs GradICON-lung/knee/brain (each trained on one dataset) evaluated cross-dataset | Task-specific GradICON-lung collapses off-domain (DICE 38.0 OAI, 18.1 L2R-Abd); uniGradICON stays on par with each specialist on its own domain (e.g. 76.2 vs 78.7 HCP) | One universal model matches specialists in-domain and dominates them out-of-domain |
| 3 | Instance Optimization (IO) at test time | uniGradICON zero-shot vs uniGradICON+IO on all in- and out-of-distribution tasks | IO consistently improves: COPDGene mTRE 2.26→1.40, L2R-Abdomen DICE 48.3→52.2, L2R-NLST mTRE 2.07→1.77, L2R-CTMR DICE 50.0→66.8 | IO is a cheap, always-on improvement; pairs naturally with the FM as a strong initialization |
| 4 | Leave-one-region-out (Type 2 generalization) | Retrain uniGradICON without L2R-Abdomen, test on L2R-Abdomen | DICE 25.9→34.1 zero-shot (drop vs full model) but still > SyN; IO recovers most of the gap toward Top-5 Learn2Reg | Model generalizes to unseen anatomy, though including the region in pretraining is clearly better; IO mitigates the held-out gap |
| 5 | Unseen modality combinations (Type 3) | Zero-shot on L2R-CBCT (CT–CBCT) and L2R-CTMR (CT–MRI), neither modality pairing in training | L2R-CBCT DICE within Top-5 Learn2Reg (57.0 zero-shot, 59.9 IO); L2R-CTMR weaker (50.0 zero-shot, 66.8 IO) vs Top-1 75 | Generalizes well when unseen modality is visually close to training CTs; struggles more on truly cross-modal (MR↔CT) without finetuning |
| 6 | Finetuning on target task | uniGradICON finetuned on L2R-CBCT, with/without IO | DICE 57.0 (zero-shot) → 60.3 (finetune) → 63.7 (finetune+IO), surpassing Top-1 (63.2) | FM serves as a strong initialization; finetune+IO beats task-specific Learn2Reg winners |

**Top take-away:** The choice of the GradICON regularizer (Ablation 1) is the load-bearing decision — it is what makes a *single* universal registration network trainable across heterogeneous anatomies and modalities, whereas matched-capacity diffusion-regularized (VoxelMorph) and LapIRN universal variants either underperform substantially or fail to train at all.
