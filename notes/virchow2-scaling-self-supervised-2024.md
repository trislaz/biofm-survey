---
id: virchow2-scaling-self-supervised-2024
title: 'Virchow2: Scaling Self-Supervised Mixed Magnification Models in Pathology'
authors:
- Eric Zimmermann
- Eugene Vorontsov
- Julian Viret
- Adam Casson
- Michal Zelechowski
- George Shaikovski
- Neil Tenenholtz
- James Hall
- David Klimstra
- Razik Yousfi
- Thomas Fuchs
- Nicolo Fusi
- Siqi Liu
- Kristen Severson
year: 2024
venue: null
arxiv: '2408.00738'
doi: null
url: https://arxiv.org/abs/2408.00738v3
pdf_path: papers/virchow2-scaling-self-supervised-2024.pdf
md_path: papers/md/virchow2-scaling-self-supervised-2024.md
modalities:
- other
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-23T09:52:50+00:00'
updated_at: '2026-04-23T09:52:53+00:00'
is_fm: true
fm_classification_reason: Added in rev4 missing-FM brainstorm; canonical bio-FM.
---

## Abstract (from arxiv)

Foundation models are rapidly being developed for computational pathology applications. However, it remains an open question which factors are most important for downstream performance with data scale and diversity, model size, and training algorithm all playing a role. In this work, we propose algorithmic modifications, tailored for pathology, and we present the result of scaling both data and model size, surpassing previous studies in both dimensions. We introduce three new models: Virchow2, a 632 million parameter vision transformer, Virchow2G, a 1.9 billion parameter vision transformer, and Virchow2G Mini, a 22 million parameter distillation of Virchow2G, each trained with 3.1 million histopathology whole slide images, with diverse tissues, originating institutions, and stains. We achieve state of the art performance on 12 tile-level tasks, as compared to the top performing competing models. Our results suggest that data diversity and domain-specific methods can outperform models that only scale in the number of parameters, but, on average, performance benefits from the combination of domain-specific methods, data scale, and model scale.

## Ablations (Rev 4)

Setup: ViT-B/16, DINOv2 variants, 1.5M MSKCC WSI (Virchow-v1 set), 115M tiles, 16×V100, linear-probe weighted F1 (×100) on 3 in-domain (PanMSK 20/10/5×) and 5 OOD tile tasks (PCam, CRC, TILS, MHIST, MIDOG). Axes ablated: ECT (extended context translation, replaces crop-and-resize), KDE (vMF kernel density entropy regularizer, replaces KoLeo), and -SOL (removing solarization). Results from Tables A5–A6 (concatenated [CLS]+patch embedding).

| Variant | PanMSK 20× | PanMSK 10× | PanMSK 5× | ID avg | PCam | CRC | TILS | MHIST | MIDOG | OOD avg |
|---|---|---|---|---|---|---|---|---|---|---|
| Standard DINOv2 | 86.0 | 88.8 | 89.0 | 87.9 | 83.6 | 94.0 | 92.5 | 79.4 | 63.0 | 82.5 |
| +ECT | 86.5 (+0.5) | 89.4 (+0.6) | 89.9 (+0.9) | 88.6 (+0.7) | 84.9 (+1.3) | 93.3 (−0.7) | 92.6 (+0.1) | 76.2 (−3.2) | 63.6 (+0.6) | 82.1 (−0.5) |
| +KDE | 88.0 (+2.0) | 90.1 (+1.3) | 90.0 (+1.1) | 89.4 (+1.5) | 84.1 (+0.6) | 94.9 (+0.9) | 93.3 (+0.8) | 78.3 (−1.0) | 66.5 (+3.5) | 83.4 (+1.0) |
| −SOL | 87.1 (+1.1) | 89.2 (+0.3) | 89.0 (—) | 89.4 (+1.5) | 84.8 (+1.3) | 93.8 (−0.2) | 92.7 (+0.2) | 77.2 (−2.2) | 65.9 (+2.9) | 82.9 (+0.4) |
| +ECT, +KDE | 89.6 (+3.6) | 92.1 (+3.2) | 92.2 (+3.2) | 91.3 (+3.4) | 86.7 (+3.1) | 95.3 (+1.3) | 93.0 (+0.5) | 80.3 (+0.9) | 66.5 (+3.6) | 84.4 (+1.9) |
| +ECT, +KDE, −SOL | **89.9 (+3.9)** | **92.4 (+3.6)** | **93.3 (+4.3)** | **91.9 (+4.0)** | 86.7 (+3.2) | **95.8 (+1.8)** | 93.2 (+0.7) | 79.2 (−0.2) | 66.3 (+3.4) | 84.3 (+1.8) |

Number of ablated configurations: **6** (1 baseline + 5 modifications). Additional [CLS]-only embedding variants in Tables A7–A8 show the same trend with larger gains (ID +6.7, OOD +2.6 at full stack), indicating the modifications particularly improve the [CLS] token quality.

**Top take-away:** ECT and KDE are individually weak or even harmful on OOD (ECT alone: −0.5 OOD avg), but **synergistic** when combined — together they yield +3.4 ID / +1.9 OOD F1 over standard DINOv2, with removing solarization adding a further small ID boost. Domain-specific augmentation + entropy regularization couplings matter more than either change alone, motivating the full recipe used to scale Virchow2/Virchow2G.
