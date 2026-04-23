---
id: virchow-a-million-slide-2023
title: 'Virchow: A Million-Slide Digital Pathology Foundation Model'
authors:
- Eugene Vorontsov
- Alican Bozkurt
- Adam Casson
- George Shaikovski
- Michal Zelechowski
- Siqi Liu
- Kristen Severson
- Eric Zimmermann
- James Hall
- Neil Tenenholtz
- Nicolo Fusi
- Philippe Mathieu
- Alexander van Eck
- Donghun Lee
- Julian Viret
- Eric Robert
- Yi Kan Wang
- Jeremy D. Kunz
- Matthew C. H. Lee
- Jan Bernhard
- Ran A. Godrich
- Gerard Oakley
- Ewan Millar
- Matthew Hanna
- Juan Retamero
- William A. Moye
- Razik Yousfi
- Christopher Kanan
- David Klimstra
- Brandon Rothrock
- Thomas J. Fuchs
year: 2023
venue: null
arxiv: '2309.07778'
doi: null
url: https://arxiv.org/abs/2309.07778v5
pdf_path: papers/virchow-a-million-slide-2023.pdf
md_path: papers/md/virchow-a-million-slide-2023.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: high
tags:
- foundation-model
- self-supervised
- DINOv2
- ViT-H
- computational-pathology
- pan-cancer
- biomarker-prediction
- MIL
- scaling
parameters: 632000000
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:16+00:00'
updated_at: '2026-04-22T20:28:05+00:00'
is_fm: true
fm_classification_reason: 'Virchow: pathology FM.'
---

## TL;DR

First million-scale pathology foundation model. ViT-H/14 (632 M params) trained with DINOv2 on 1.5 M H&E WSIs (~2 B tiles) from MSKCC. Sets SOTA on pan-cancer detection (0.949 AUC across 17 cancer types, 0.937 on 7 rare), biomarker prediction (ColonMSI 0.972, BladderFGFR 0.902, LungEGFR 0.853), and all tile-level linear-probing benchmarks. Key message: data scale (1.5 M WSIs vs ≤100 k prior art) and model scale (632 M vs ≤307 M) both matter; gains hold on OOD external data and rare cancers.

## Model

- **Architecture:** ViT-H/14 (Vision Transformer "Huge"), 632 M parameters.
- **Embedding:** Concatenation of CLS token + mean of 256 patch tokens → 2,560-dim per 224×224 tile.
- **Pre-training algorithm:** DINOv2 (student–teacher self-supervised learning with masked image modelling regulariser).
- **Input:** 224×224 pixel tiles at 20× magnification (0.5 mpp).
- **Downstream:** Tile embeddings aggregated via Agata (attention-based MIL) for slide-level tasks; linear probing for tile-level tasks.

## Data

- **Source:** Memorial Sloan Kettering Cancer Center (MSKCC), single institution.
- **Scale:** 1,488,550 H&E-stained WSIs, 119,629 patients, 208,815 cases, 392,268 specimens, 1,207,837 blocks → ~2 B tiles.
- **Composition:** Cancer 38 %, Precursor 8 %, Benign 24.6 %, Unknown 29.4 %; Biopsy 63 %, Resection 37 %.
- **Tissue diversity:** 17 high-level tissue groups (breast 24.9 %, skin 18.4 %, GI upper 16.1 %, colon 6.1 %, lung 5.5 %, prostate 3.7 %, etc.).
- **Scanner:** Leica, scanned at 20× / 0.5 mpp.
- **Tile extraction:** Non-overlapping 224×224 tiles, ≥25 % tissue foreground (HSV thresholding).

## Training Recipe

- **Optimizer:** AdamW (β₁=0.9, β₂=0.999), float16 precision.
- **LR warmup:** 495,000 iterations (vs DINOv2 default 100 k).
- **Teacher temperature:** 0.04 → 0.07 ramp over 186,000 iterations.
- **Prototypes:** 131,072 (matching the projection head dimensionality).
- **Batch construction:** 1 WSI per GPU, 256 random foreground tiles per WSI.
- **Default DINOv2 hyperparameters** used except for the above changes.
- **Compute:** Not reported (number of GPUs, wall-clock time, total FLOPs not disclosed).

## Key Ablations & Design Choices (MOST IMPORTANT, quantitative)

1. **Data scale is the dominant lever.** Virchow (1.5 M WSIs) vs UNI/RudolfV (~100 k WSIs) vs Phikon (6 k WSIs, TCGA-only): pan-cancer AUC 0.949 vs 0.930 (Phikon) vs 0.904 (CTransPath). Rare-cancer AUC 0.937 vs lower for all baselines. External/OOD AUC drop only –0.006 for Virchow vs –0.008 (Phikon) and –0.016 (CTransPath).
2. **Model scale matters alongside data.** ViT-H 632 M > ViT-B 86 M (Phikon) > SwinT 28 M (CTransPath). The NatImg baseline (1.1 B params, 142 M natural images) is strong on tile tasks but still loses to Virchow on all 6 benchmarks, confirming in-domain data value.
3. **Embedding design: CLS + mean patch tokens.** 2,560-dim (1,280 CLS ∥ 1,280 mean-patch) used for Virchow. Phikon uses CLS only; CTransPath uses mean of all tokens. No explicit ablation on this choice but it consistently outperforms.
4. **Stain robustness.** On CRC benchmark, Virchow's weighted-F1 drops only −0.005 between stain-normalized and unnormalised test sets, indicating learned stain invariance.
5. **SSL algorithm choice.** Authors discuss DINO vs MAE vs contrastive (SIMCLR, MoCo). Prior work (Kang et al., 2023) found no clear best on 37 k WSIs, but DINO-family most often top. MAE embeddings require additional finetuning step and yield worse linear probing.
6. **Biomarker prediction.** Virchow > Phikon > CTransPath on all three biomarkers: ColonMSI 0.972 vs 0.957 vs 0.970; BladderFGFR 0.902 vs 0.886 vs 0.882; LungEGFR 0.853 vs 0.821 vs 0.807. Gains most pronounced on LungEGFR (+3.2 pp over Phikon).
7. **Tile-level linear probing.** Virchow top-1 on all 6 tasks (WILDS, CRC, CRC-no-norm, PanMSK, PCam, MHIST). Phikon ties top-1 twice.
8. **Unsupervised feature semantics.** PCA on patch tokens separates malignant epithelium, inflammatory, and miscellaneous cells in CoNSeP without any supervision — emergent property analogous to DINOv2 on natural images.

## Reported Insights

- Single-institution data (MSKCC) at million-scale is sufficient for OOD generalisation — external data AUC drop is minimal (−0.006).
- Rare cancers (25 % of evaluation) benefit most from scale: cervix detection improves from 0.753 (CTransPath) → 0.810 (Phikon) → 0.875 (Virchow).
- Color/stain augmentation from natural-image DINOv2 defaults transfers well; no domain-specific augmentation needed at this data scale.
- Extended LR warmup (495 k iterations, 5× default) was necessary — likely due to the long-tailed distribution of pathology features.
- Tile-level foundation model + attention-based MIL aggregator is a viable architecture for clinical-grade pan-cancer detection.
- **Limitations acknowledged:** Single institution, single scanner type (Leica), tile-level only (no native slide-level model), no deep aggregator architecture search.

## References Worth Chasing (15 bio-FM refs)

1. **DINOv2** — Oquab et al., 2023 (arXiv 2304.07193) — core SSL algorithm.
2. **UNI** — Chen et al., 2023 (arXiv 2308.15474) — 100 k WSI ViT-L DINOv2 pathology FM.
3. **RudolfV** — Dippel et al., 2024 — 103 k WSI ViT-L DINOv2 pathology FM.
4. **Campanella et al., 2023** (arXiv 2310.07033) — 3 B tiles / 400 k WSIs, ViT-S DINO, health-system scale.
5. **Phikon** — Filiot et al., 2023 — ViT-B 86 M, iBOT, TCGA-only baseline.
6. **CTransPath** — Wang et al., 2022 — SwinT 28 M, MoCoV3, first pathology FM.
7. **HIPT** — Chen et al., 2022 (CVPR) — hierarchical ViT, DINO, gigapixel slide-level SSL.
8. **Ciga et al., 2022** — SIMCLR pathology FM, data augmentation ablations.
9. **Lunit / Kang et al., 2023** (CVPR) — benchmark of 4 SSL algorithms on 37 k WSIs.
10. **Remedis** — Azizi et al., 2023 — ResNet-152, SIMCLR, diagnostic imaging.
11. **PLIP** — Huang et al., 2023 — vision-language pathology FM (CLIP, medical Twitter).
12. **CONCH** — Lu et al., 2023 (arXiv 2307.12914) — vision-language pathology FM.
13. **Agata** — Raciti et al., 2022 — attention-based MIL aggregator used for downstream.
14. **Campanella et al., 2019** (Nature Medicine) — clinical-grade weakly-supervised pathology.
15. **iBOT** — Zhou et al., 2021 — online tokenizer SSL, basis of Phikon training.

## Notes / Open Questions

- **No training compute reported** — GPU count, wall-clock time, and total FLOPs are absent; hard to place on scaling-law curves.
- **No training_tokens equivalent** — ~2 B tiles stated, but number of epochs / total tokens seen during training is unclear.
- **Single institution** — all 1.5 M WSIs from MSKCC; multi-site pre-training could unlock further OOD gains.
- **Aggregator not deeply explored** — Agata is fixed across all experiments; the paper explicitly notes that aggregator architecture search is out of scope.
- **v5 of the arXiv** — the paper self-describes as a "live paper" with ongoing updates; check for newer versions.
- **Virchow 2** — follow-up work expected from Paige; check for successor model and whether scaling trends continue.

## Ablations (Rev 4)

Note: The paper does not present a dedicated controlled-ablation section (no swap-in/out of single design choices on Virchow itself). Reported "ablations" are (a) one stain-normalization robustness test on Virchow, and (b) cross-model comparisons that vary data scale, model scale, and SSL recipe simultaneously — included here as quasi-ablations.

| # | Axis varied | Setting (vs Virchow ViT-H/14, 1.5 M WSIs, DINOv2) | Benchmark / Metric | Result | Δ vs Virchow | Source |
|---|---|---|---|---|---|---|
| 1 | Stain normalization (test-time) | Train norm → test no-norm (CRC-NoNorm) | CRC weighted F1 | 0.968 | −0.005 | Tab. A4, §2.3 |
| 2 | Data scale + model scale | Phikon (TCGA 6 k WSIs, ViT-B 86 M, iBOT) | PanMSK weighted F1 | 0.923 | −0.027 | Tab. A4 |
| 3 | Data scale + model scale | CTransPath (15 k WSIs, SwinT 28 M, MoCoV3) | PanMSK weighted F1 | 0.897 | −0.053 | Tab. A4 |
| 4 | In-domain vs natural-image pretraining | NatImg (1.1 B params, 142 M ImageNet-22k images, DINOv2) | PanMSK weighted F1 | 0.883 | −0.067 | Tab. A4 |
| 5 | In-domain vs natural-image pretraining | NatImg | MHIST weighted F1 | 0.827 | −0.008 | Tab. A4 |
| 6 | Vision-language vs SSL | PLIP (CLIP on pathology image-text) | PanMSK weighted F1 | 0.862 | −0.088 | Tab. A4 |
| 7 | SSL algorithm + scale | DINO_p=8 (TCGA + internal, 49 M params) | PanMSK weighted F1 | 0.903 | −0.047 | Tab. A4 |
| 8 | Cross-site OOD (aggregator) | Pan-cancer eval on external institutions | AUC drop from internal | −0.006 | (Phikon −0.008, CTransPath −0.016) | Fig. 2b, §2.1 |
| 9 | OOD tile distribution shift | WILDS (unseen hospital) | weighted F1 | 0.970 | tied with Phikon (0.971) | Tab. A4 |
| 10 | Embedding pooling (qualitative) | CLS ∥ mean(patch tokens) → 2,560-dim | CoNSeP PCA cell-type separation | Emergent semantic clusters | n/a (no quantitative ablation) | Fig. 3d, §2.3 |
| 11 | LR warmup length | 495 k iters (≈5× DINOv2 default 100 k) | Training stability | Required for convergence at this scale | not quantified | §4.2 |

Top take-away: **In-domain pathology data scale is the single largest lever** — going from natural-image DINOv2 (1.1 B params, 142 M images) to Virchow (632 M params, 1.5 M WSIs / ~2 B tiles) gains +0.067 weighted F1 on PanMSK and +0.041 on CRC, and the gap widens further on small-scale pathology FMs (Phikon, CTransPath). Stain-normalization removal costs only −0.005 F1, confirming that million-scale in-domain SSL also confers stain robustness almost "for free."
