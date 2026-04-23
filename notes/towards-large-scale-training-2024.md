---
id: towards-large-scale-training-2024
title: Towards Large-Scale Training of Pathology Foundation Models
authors:
- kaiko. ai
- Nanne Aben
- Edwin D. de Jong
- Ioannis Gatopoulos
- Nicolas Känzig
- Mikhail Karasikov
- Axel Lagré
- Roman Moser
- Joost van Doorn
- Fei Tang
year: 2024
venue: null
arxiv: '2404.15217'
doi: null
url: https://arxiv.org/abs/2404.15217v1
pdf_path: papers/towards-large-scale-training-2024.pdf
md_path: papers/md/towards-large-scale-training-2024.md
modalities:
- imaging-pathology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T20:52:51+00:00'
updated_at: '2026-04-22T20:56:29+00:00'
is_fm: true
fm_classification_reason: kaiko.ai pathology FMs released on TCGA.
---

## Abstract (from arxiv)

Driven by the recent advances in deep learning methods and, in particular, by the development of modern self-supervised learning algorithms, increased interest and efforts have been devoted to build foundation models (FMs) for medical images. In this work, we present our scalable training pipeline for large pathology imaging data, and a comprehensive analysis of various hyperparameter choices and training techniques for building pathology FMs. We release and make publicly available the first batch of our pathology FMs (https://github.com/kaiko-ai/towards_large_pathology_fms) trained on open-access TCGA whole slide images, a commonly used collection of pathology images. The experimental evaluation shows that our models reach state-of-the-art performance on various patch-level downstream tasks, ranging from breast cancer subtyping to colorectal nuclear segmentation. Finally, to unify the evaluation approaches used in the field and to simplify future comparisons of different FMs, we present an open-source framework (https://github.com/kaiko-ai/eva) designed for the consistent evaluation of pathology FMs across various downstream tasks.

## Ablations (Rev 4)

| # | Axis varied | Setup | Variants compared | Metric / tasks | Result | Take-away |
|---|---|---|---|---|---|---|
| 1 | Pre-training magnification | ViT-S16, DINO, 100 epochs, TCGA, randomly initialized (Table II, §II-C) | 40×, 20×, 10×, 5×, {20,40}×, {5,10,20,40}× | Linear probing on BACH, CRC, MHIST, PCam/val, PCam/test | All-four mix wins on 4/5 tasks (e.g. BACH 0.753 vs best single 0.685 @20×; MHIST 0.771 vs 0.746); 20× best among single magnifications | Mixing magnifications yields a magnification-agnostic FM that beats any single-magnification model — no architectural change required |
| 2 | Backbone initialization | ViT-S16, DINO, 120 epochs (§II-B, Fig. 1) | Random init vs ImageNet-pretrained init | Linear probing curves on BACH, PCam, TP53 | ImageNet-init converges much faster and reaches a higher plateau; from-scratch lags throughout | Always warm-start pathology FMs from ImageNet weights — faster convergence and higher final accuracy |
| 3 | Training set size (# WSIs) | ViT-S16, DINO, 100 epochs, TCGA FFPE subsets (Table III, §II-D.1) | No-train, 1%, 10%, 30%, 100% of TCGA WSIs | Linear probing balanced acc on BACH, CRC, MHIST, PCam, TP53 | Strong gains 0%→1% (e.g. PCam 0.728→0.871); 30% nearly matches 100% on OOD tasks; only TP53 (ID) keeps improving (0.560→0.621) | OOD performance saturates fast on TCGA — more WSIs from same distribution mostly help in-distribution; need more diverse data to push OOD further |
| 4 | Number of distinct training patches | ViT-S16, DINO, 100 epochs, full TCGA, patches cached after N samples (Table IV, §II-D.2) | 0, 10, 10², 10³, 10⁴, ∞ unique patches | Linear probing on BACH, CRC, MHIST, PCam, TP53 | OOD saturates by ~10³ patches; ID TP53 grows monotonically with #patches (0.529→0.621) | Online patching's effectively-infinite patch sampling mainly benefits in-distribution learning; OOD is bottlenecked by slide diversity, not patch count |
| 5 | SSL algorithm: DINO vs DINOv2 | ViT-S16, single A100-80GB, matched batch size 256, 100 epochs (Appendix B, Fig. 4) | DINO vs DINOv2 (with patch-level obj., Sinkhorn-Knopp, KoLeo) | BACH/PCam linear probing curves + ODCorr on TCGA | No significant downstream difference on BACH/PCam; DINOv2 yields better off-diagonal correlation but at higher compute cost; ViT-L14 (DINOv2) only matches ViT-S16 (DINO) | On TCGA-scale data, DINOv2's extra complexity does not pay off downstream — stick with DINO unless scaling data well beyond TCGA |
| 6 | Model size scaling | DINO/DINOv2 on TCGA (Table I, §II-A) | ViT-S16, ViT-B8, ViT-L14 | PCam etc. | Limited gains: PCam 0.893 (S16) → 0.921 (B8) → 0.898 (L14) | TCGA is likely too small / insufficiently diverse to benefit large models; scaling model without scaling data plateaus or regresses |
| 7 | ViT patch size | DINO/DINOv2 on TCGA (§II-A) | patch size 16 vs 14 vs 8 | Patch-level + segmentation downstream | ViT-B8 and ViT-S8 dominate segmentation, beating ViT-L14 despite fewer params | Smaller ViT patch size matters more than model size for dense pathology tasks |

**Count: 7 ablations.**

**Top take-away:** On TCGA, the performance ceiling is set by **data diversity**, not by model size or SSL algorithm — mixing magnifications and warm-starting from ImageNet give the largest, cheapest wins, while scaling model capacity (B8→L14) or upgrading DINO→DINOv2 yields little, and OOD accuracy saturates with only ~30% of WSIs / ~10³ unique patches. The clear next lever is broader, multi-source slide collections rather than bigger backbones.
