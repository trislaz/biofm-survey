---
id: evaluating-computational-pathology-foundation-2024
title: Evaluating Computational Pathology Foundation Models for Prostate Cancer Grading
  under Distribution Shifts
authors:
- Fredrik K. Gustafsson
- Mattias Rantalainen
year: 2024
venue: null
arxiv: '2410.06723'
doi: null
url: https://arxiv.org/abs/2410.06723v1
pdf_path: papers/evaluating-computational-pathology-foundation-2024.pdf
md_path: papers/md/evaluating-computational-pathology-foundation-2024.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: medium
tags:
- evaluation
- robustness
- distribution-shift
- prostate-cancer
- weakly-supervised
- UNI
- CONCH
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:15+00:00'
updated_at: '2026-04-22T20:19:52+00:00'
is_fm: false
fm_classification_reason: Evaluation of existing pathology FMs under shifts.
---

## TL;DR

Benchmarks two pathology FMs (UNI, CONCH) as frozen feature extractors for prostate cancer ISUP grading on PANDA (10,616 WSIs, 2 sites). Both outperform ImageNet-pretrained ResNet-50 in-distribution, but performance collapses under cross-site distribution shift (UNI-ABMIL: 0.888→0.247 kappa; CONCH-ABMIL: 0.866→0.024 kappa). Key message: large-scale FM pretraining does **not** guarantee downstream robustness to common distribution shifts (scanner/staining differences). This is an **evaluation paper**, not a new FM.

## Model

No new model proposed. Evaluates existing FMs as **frozen patch-level feature extractors** within three WSI-level ISUP grade classifiers:

1. **ABMIL** — attention-based MIL aggregator + linear head (trainable). Based on CLAM implementation. AdamW, cosine LR, max 20 epochs, early stopping.
2. **MeanFeature** — mean-pool patch features → FC+dropout+ReLU → linear head (trainable).
3. **kNN** — mean-pool patch features → k=5 nearest neighbors (no trainable params; directly probes FM quality).

Feature extractors evaluated:
- **UNI** [Chen et al. 2024]: ViT-Large, DINOv2, ~100M tissue patches from >100k WSIs (20 cancer types). Output dim=1024.
- **CONCH** [Lu et al. 2024]: ViT-Base, iBOT pretrain on 16M patches from >21k WSIs, then CoCa vision-language pretrain on >1.1M image-caption pairs from PubMed. Output dim=512.
- **Resnet-IN** (baseline): ResNet-50, ImageNet pretrained. Output dim=1024.

Patches: 256×256 at 20× magnification, tissue-segmented via CLAM.

## Data

**PANDA dataset** (public, Kaggle): 10,616 prostate biopsy WSIs with ISUP grade labels (0–5), from 2,113 patients. Two sites:
- **Radboud** (Netherlands): 4,999 WSIs, 3DHistech scanner, ~uniform grade distribution.
- **Karolinska** (Sweden): 5,434 WSIs, Leica/Hamamatsu scanners, heavily left-skewed grade distribution.

Subsets created for controlled experiments:
- Radboud-U (3,996 WSIs) and Karolinska-U (1,506 WSIs): perfectly uniform label distributions.
- Radboud-L (2,484 WSIs, left-skewed) and Radboud-R (2,515 WSIs, right-skewed): label shift experiments.
- Radboud-Subsets-Dev (varying 2%–100%) + Radboud-Subsets-Test (1,000 WSIs): data scaling experiments.
- Karolinska-1k-Test (1,000 WSIs): held-out test for mixed-site training experiments (0%–100% Karolinska in training).

Evaluation: quadratic weighted Cohen's kappa (primary), MAE (secondary). 10-fold cross-validation (80/10/10 train/val/test).

## Training Recipe

Not applicable — no new FM trained. Downstream classifiers (ABMIL, MeanFeature) use AdamW optimizer, cosine LR schedule, max 20 epochs with early stopping on val loss. Hyperparams follow UNI paper's weakly-supervised slide classification setup. Feature extractors are **frozen** throughout.

## Key Ablations & Design Choices

### In-distribution performance (PANDA, 10-fold CV)
| Model | ABMIL κ | MeanFeature κ | kNN κ |
|---|---|---|---|
| UNI | **0.888±0.013** | 0.845±0.020 | 0.727±0.018 |
| CONCH | 0.866±0.009 | 0.777±0.019 | 0.690±0.021 |
| Resnet-IN | 0.773±0.013 | 0.610±0.030 | 0.613±0.016 |

### Cross-site distribution shift (Radboud→Karolinska, OOD)
| Model | ABMIL κ | MeanFeature κ | kNN κ |
|---|---|---|---|
| UNI | 0.247±0.138 | **0.489±0.059** | 0.214±0.037 |
| CONCH | 0.024±0.018 | 0.026±0.015 | 0.208±0.012 |
| Resnet-IN | 0.185±0.041 | 0.216±0.023 | 0.070±0.013 |

**Massive performance collapse**: UNI-ABMIL drops from 0.888 to 0.247 κ across sites. CONCH-ABMIL drops to **0.024** — essentially random — and is **outperformed by Resnet-IN** under shift.

### Uniform-label subsets (Radboud-U→Karolinska-U)
Controlling for label shift still shows large drops: UNI-ABMIL 0.843→0.459, CONCH-ABMIL 0.818→0.206. Image data shift dominates over label shift.

### Label distribution shift (Radboud-L→Radboud-R)
Relatively small drops: UNI-ABMIL 0.826→0.739, CONCH-ABMIL 0.805→0.712. Confirms label shift is a minor issue vs. scanner/staining shift.

### Data scaling (training set size)
- More Radboud training data improves ID performance but can **degrade** OOD (Karolinska) performance — overfitting to single site.
- Adding even small amounts of target-site data (1–5% Karolinska) rapidly improves OOD generalization to near-100%-Karolinska levels.

### Aggregation method matters
ABMIL > MeanFeature > kNN in most settings. Trainable ABMIL aggregator provides clear benefit. Under OOD shift, MeanFeature with UNI (0.489 κ) surprisingly outperforms ABMIL (0.247 κ), suggesting ABMIL may overfit more to site-specific patterns.

### UNI vs CONCH
UNI (vision-only) outperforms CONCH (vision-language) in almost all settings, including OOD. This contradicts benchmarking by Neidlinger & El Nahhas et al. [32] where CONCH was superior. CONCH is particularly fragile under distribution shift.

## Reported Insights

1. Pathology FMs (UNI, CONCH) strongly outperform ImageNet baseline in-distribution but absolute OOD performance can be "far from satisfactory."
2. Large, varied pretraining data does **not** guarantee downstream robustness — downstream data quality/diversity is still crucial.
3. Vision-only UNI > vision-language CONCH overall; CONCH more sensitive to distribution shift.
4. Label distribution shifts are a smaller problem than scanner/staining image data shifts.
5. Adding small proportions of target-site training data rapidly recovers OOD performance.
6. More single-site training data can paradoxically hurt OOD generalization (site overfitting).
7. Authors recommend future work with ≥3 sites and evaluation of other FMs (Virchow, GigaPath, H-optimus-0, Hibou).

## References Worth Chasing

1. **UNI** — Chen et al., "Towards a general-purpose foundation model for computational pathology," *Nature Medicine* 2024 [9]
2. **CONCH** — Lu et al., "A visual-language foundation model for computational pathology," *Nature Medicine* 2024 [29]
3. **Virchow2** — Zimmermann et al., "Scaling self-supervised mixed magnification models in pathology," arXiv 2408.00738, 2024 [49]
4. **Virchow** — Vorontsov et al., "A foundation model for clinical-grade computational pathology and rare cancers detection," *Nature Medicine* 2024 [43]
5. **GigaPath** — Xu et al., "A whole-slide foundation model for digital pathology from real-world data," *Nature* 2024 [46]
6. **H-optimus-0** — Saillard et al., 2024 [39]
7. **Hibou** — Nechaev et al., "A family of foundational vision transformers for pathology," arXiv 2024 [31]
8. **Phikon** — Filiot et al., "Scaling self-supervised learning for histopathology with masked image modeling," medRxiv 2023 [16]
9. Neidlinger & El Nahhas et al., "Benchmarking foundation models as feature extractors for weakly-supervised computational pathology," arXiv 2408.15823, 2024 [32]
10. Wölflein et al., "Benchmarking pathology feature extractors for whole slide image classification," arXiv 2024 [45]
11. Campanella et al., "A clinical benchmark of public self-supervised pathology foundation models," arXiv 2024 [8]
12. **CLAM** — Lu et al., "Data-efficient and weakly supervised computational pathology on whole-slide images," *Nature BME* 2021 [28]
13. **DINOv2** — Oquab et al., "Learning robust visual features without supervision," *TMLR* 2024 [34]
14. **PANDA** — Bulten et al., "Artificial intelligence for diagnosis and Gleason grading of prostate cancer," *Nature Medicine* 2022 [6]
15. Aben et al., "Towards large-scale training of pathology foundation models," arXiv 2024 [1]

## Notes / Open Questions

- This is a **benchmarking/evaluation paper**, not a new FM. No model parameters or training compute to report.
- Only one downstream task (ISUP grading) on one dataset (PANDA) with two sites — limited generalizability of conclusions.
- Surprising that CONCH (VL model) underperforms UNI (vision-only) — may be task/data specific; CONCH's ViT-B is also smaller than UNI's ViT-L.
- The MeanFeature > ABMIL result under OOD shift (for UNI) is intriguing — suggests attention-based aggregation may overfit to site-specific patch patterns.
- No evaluation of more recent FMs (Virchow2, GigaPath, H-optimus-0) — acknowledged as future work.
- Would be valuable to see results with domain adaptation or test-time augmentation strategies.
- The 0.024 kappa for CONCH-ABMIL under shift is striking — nearly zero agreement, raising questions about what site-specific features CONCH latches onto.
