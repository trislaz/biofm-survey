---
id: phikon-v2-a-large-2024
title: Phikon-v2, A large and public feature extractor for biomarker prediction
authors:
- Alexandre Filiot
- Paul Jacob
- Alice Mac Kain
- Charlie Saillard
year: 2024
venue: null
arxiv: '2409.09173'
doi: null
url: https://arxiv.org/abs/2409.09173v1
pdf_path: papers/phikon-v2-a-large-2024.pdf
md_path: papers/md/phikon-v2-a-large-2024.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: medium
tags:
- self-supervised-learning
- DINOv2
- pathology-foundation-model
- ViT-L
- biomarker-prediction
- benchmarking
- ensembling
- computational-pathology
parameters: '307M'
training_tokens: '456M tiles (400M seen at released ckpt)'
training_compute: '11k GPU-hours (128× V100-32GB, 83h wall)'
references_chased: false
added_at: '2026-04-22T19:37:16+00:00'
updated_at: '2026-04-22T20:24:16+00:00'
---

## TL;DR

Phikon-v2 is a ViT-L/16 (307M params) trained with DINOv2 on PANCAN-XL, a public dataset of 456M histology tiles (58.4k WSIs, 30+ cancer sites). Released at iteration 100k (400M tiles seen). Benchmarked on 8 slide-level tasks against 14 other pathology feature extractors; performs on par with proprietary-data FMs (GigaPath, H-Optimus-0, UNI). Key findings: DINOv2 scales better than iBOT for joint model+data scaling; ViT-L+ models form a clear performance tier; a specialized 13× smaller iBOT model beats all FMs on MSI; ensembling 25 ABMIL models yields +1.75 AUC over one-shot retraining (p<0.001). Publicly released under non-commercial license.

## Model

- **Architecture**: ViT-L/16 (24 layers, 16 heads, embedding dim 1024, patch size 16) — 307M parameters.
- **SSL method**: DINOv2 (extension of iBOT with multi-crop, masked image modeling, and DINO head). No registers.
- **Output**: 1024-dim CLS token embedding per 224×224 tile at 20× magnification (0.5 µm/px).
- **Released checkpoint**: iteration 100,000 out of 250,000 (early stop; 400M tiles seen ≈ 93% of dataset).
- **Availability**: Hugging Face (`owkin/phikon-v2`), non-commercial license.

## Data

- **PANCAN-XL**: 58,359 WSIs from 132 public + 4 internal datasets; 456M tiles at 20× (224×224 px, 0.5 µm/px). 30+ cancer sites + normal tissues.
- **Sources**: TCGA (29.5k), GTEx (13.3k), CPTAC (6.2k), plus many smaller cohorts. 31% fresh-frozen, 69% FFPE.
- **Site distribution skew**: 34% from just Breast/Lung/Colorectal; ~55% from 6 sites (+ Brain, Kidney, Uterus).
- **Preprocessing**: U-Net tissue segmentation at 2.5×; tiles extracted at 20× with ≥60% tissue threshold.
- **Downstream evaluation**: 8 slide-level tasks (METASTASIS, MSI, HER2, ER, PR, IDH1, ISUP, RCC) across 5 cancer sites. External validation cohorts only — no data contamination.

## Training Recipe

- **Method**: DINOv2 self-supervised (student-teacher, multi-crop with 2 global 224px + 8 local 96px crops).
- **Optimizer**: Adam (β=0.9, 0.999); batch size 4096; cosine LR schedule, base LR 4e-3 → 1e-6.
- **Warmup**: 25k iterations (LR); 75k iterations (teacher temperature 0.04→0.4).
- **Total**: 250k iterations; ~1B images seen (≈2× dataset). Released at 100k iterations.
- **Compute**: 32 nodes × 4 V100-32GB = 128 GPUs; 83 hours wall time; 11k GPU-hours; 0.38 tCO₂eq.
- **Masking**: iBOT mask ratio 0.1–0.5, sample prob 0.5. Stochastic dropout 0.3. FP16.
- **Downstream protocol**: Freeze encoder → ABMIL (164k params, 1-layer gated attention, dim 128). 5-fold CV × 5 seeds = 25 models ensembled. Adam, LR 1e-3, batch 16, 100 epochs, BCE/CE loss. 5,000 tiles per WSI (400 for ISUP).

## Key Ablations & Design Choices

1. **DINOv2 vs iBOT scaling**: Phikon (ViT-B, iBOT, 43M tiles) → Phikon-v2 (ViT-L, DINOv2, 456M tiles) = +1.9 AUC mean (p<1e-4). Joint 4× model + 10× data scaling works better with DINOv2 than iBOT. However, DINOv2 slightly hurt a ViT-B on MSI vs iBOT, suggesting DINOv2 advantage is not universal for smaller models.
2. **ViT-L+ tier**: Top-5 models are all ViT-L or larger (GigaPath 0.883, Phikon-v2 0.874, UNI 0.873, H-Optimus-0 0.867, Virchow2 0.865 mean AUC). Fisher-combined p-values confirm this tier is statistically separated from ViT-B models.
3. **Specialized vs general FM (MSI)**: iBOT ViT-B trained on 4M TCGA-COAD tiles (13× smaller, 350× less data) beats all FMs on MSI across 3 external cohorts (avg 0.944 vs GigaPath 0.939, H-Optimus-0 0.938, Phikon-v2 0.931). Scaling is not the systematic solution for biomarker prediction.
4. **Ensembling vs one-shot retraining**: 25-model ensemble yields +1.75 AUC across all extractors and tasks (p<0.001). Per-model improvement significant for 14/16 extractors (p<0.0001 for most).
5. **Task inconsistency**: Rankings are unstable across tasks. Phikon-v2 excels on MSI but poor on IDH1; GigaPath/UNI strong on Bcnb but weaker on Herohe; H-Optimus-0 worst on IDH1 (0.790). CTransPath (28M) matches GigaPath on IDH1 (0.895).
6. **In-domain vs out-of-domain**: DINOv2 ViT-L ImageNet baseline (same arch, natural images) is last with 0.757 mean AUC — in-domain SSL clearly dominant even for 30× smaller models.
7. **Early checkpoint**: Released at 100k/250k iterations. Implies full training may not improve or may overfit; authors chose based on "iterative findings."

## Reported Insights

- Statistical margins between top FMs are mostly non-significant; single-task comparisons are unreliable for ranking.
- Pre-training data composition influence on downstream is poorly understood (Phikon without brain data beats Phikon-v2 on IDH1 by +1.1%).
- Robustness to slide preparation/acquisition shifts is under-explored and critical for clinical deployment.
- Organ- and task-specific fine-tuning or distillation of FMs may be more impactful than further scaling.
- Evaluation should use multiple external cohorts per task with Fisher-combined p-values rather than single-cohort comparisons.

## References Worth Chasing

1. **DINOv2** [1] — Oquab et al. 2024. SSL method used for Phikon-v2 and most SOTA path FMs.
2. **GigaPath** [2/37] — Xu et al. Nature 2024. ViT-g (1.1B) on 1.3B tiles; top performer in benchmark.
3. **H-Optimus-0** [3] — Saillard et al. 2024. ViT-g (1.1B) on 500k WSIs; Bioptimus.
4. **UNI** [10] — Chen et al. Nature Medicine 2024. ViT-L DINOv2 on 100k WSIs (100M tiles); general-purpose path FM.
5. **Virchow** [8/55] — Vorontsov et al. 2024. ViT-H (632M) on 1.5M slides from MSKCC.
6. **Virchow2** [11] — Zimmermann et al. 2024. ViT-H/G multi-resolution on 3.1M WSIs.
7. **Phikon (v1)** [13] — Filiot et al. medRxiv 2023. ViT-B iBOT on 43M TCGA tiles; predecessor.
8. **iBOT** [12] — Zhou et al. 2022. Image BERT pre-training with online tokenizer; predecessor SSL method.
9. **CONCH** [58] — Lu et al. Nature Medicine 2024. iBOT→CoCa vision-language path FM.
10. **CTransPath** [46] — Wang et al. MIA 2022. Swin-T (28M) MoCo-v3; surprisingly competitive.
11. **Campanella et al. clinical benchmark** [38] — 2024. Shows smaller models on par with large FMs on biomarker tasks.
12. **Kaiko.ai** [36] — 2024. DINO ViT-B/S on TCGA; found no DINOv2 benefit over DINO at tile-level.
13. **PathDINO-512** [41] — Alfasly et al. 2024. 9M param ViT competitive with much larger FMs on WSI retrieval.
14. **REMEDIS** [33] — Azizi et al. Nature BME 2023. ResNet-152×2 SimCLR on 50M tiles.
15. **Jaume et al. (MADELEINE)** [44] — 2024. Multistain pretraining; ABMIL baseline reference.

## Notes / Open Questions

- Released checkpoint is early (100k/250k iters); no ablation on checkpoint selection or continued training benefit.
- iBOT-only scaling on PANCAN-XL was not tested — the DINOv2 vs iBOT comparison confounds method with data/model scale.
- No tile-level or linear probing evaluation; all results are WSI-level ABMIL.
- 4 internal (private) datasets included in PANCAN-XL despite "publicly available" framing.
- Non-commercial license limits clinical deployment.
- Would be interesting to see distillation from ViT-L to ViT-S/B for efficiency.
- Carbon footprint is modest (0.38 tCO₂eq) compared to Virchow/GigaPath scale.
