---
id: scaling-vision-transformers-to-2022
title: Scaling Vision Transformers to Gigapixel Images via Hierarchical Self-Supervised
  Learning
authors:
- Richard J. Chen
- Chengkuan Chen
- Yicong Li
- Tiffany Y. Chen
- Andrew D. Trister
- Rahul G. Krishnan
- Faisal Mahmood
year: 2022
venue: CVPR
arxiv: '2206.02647'
doi: null
url: https://arxiv.org/abs/2206.02647v1
pdf_path: papers/scaling-vision-transformers-to-2022.pdf
md_path: papers/md/scaling-vision-transformers-to-2022.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: full-text
tags:
- foundation-model
- self-supervised
- DINO
- hierarchical
- gigapixel
- vision-transformer
- computational-pathology
- whole-slide-modelling
- multiple-instance-learning
- knowledge-distillation
parameters: <10M total; 505k trainable at fine-tune (ViT_WSI-4096 only)
training_tokens: 104M 256×256 patches (Stage 1) + 408k 4096×4096 regions (Stage 2)
training_compute: not reported
references_chased: false
added_at: '2026-04-22T21:55:21+00:00'
updated_at: '2026-04-22T21:55:26+00:00'
---

## TL;DR

HIPT (Hierarchical Image Pyramid Transformer) is a three-stage ViT architecture that models gigapixel whole-slide images by exploiting their natural hierarchical structure: [16×16] cells → [256×256] patches → [4096×4096] regions → slide. Each aggregation stage uses a small ViT block, and the first two stages are pretrained with DINO self-supervised learning on 10,678 TCGA WSIs (33 cancer types). At fine-tuning only a lightweight slide-level ViT (~505k params) is trained. HIPT achieves SOTA on cancer subtyping and survival prediction, and self-supervised ViTs learn interpretable morphological phenotypes (cells, stroma, tumour cellularity) without labels.

## Model

- **Name:** HIPT — Hierarchical Image Pyramid Transformer.
- **ViT₂₅₆-16 (cell-level):** Vanilla ViT that patches 256×256 images into 256 [16×16] tokens + learnable [CLS]. Output: 384-d [CLS]₂₅₆ embedding. MHSA with h=6 heads.
- **ViT₄₀₉₆-256 (patch-level):** Takes 256 [CLS]₂₅₆ tokens from non-overlapping 256×256 patches within a 4096×4096 region. n=4 layers, h=3 heads, d=192. Output: 192-d [CLS]₄₀₉₆.
- **ViT_WSI-4096 (region-level / slide-level):** Aggregates [CLS]₄₀₉₆ tokens across the whole slide. n=2 layers, h=3 heads, d=192. M ranges 1–256. No positional embeddings (due to irregular tissue segmentation).
- **Total parameters:** <10M (paper claim). Trainable at fine-tuning: 505,204 (ViT_WSI-4096 only; ViT₂₅₆-16 and ViT₄₀₉₆-256 are frozen).
- **Downstream:** Fine-tuned ViT_WSI-4096 output → task-specific classifier for subtyping or survival prediction.
- **Key design insight:** Sequence length is always M=256 at each stage (cell and patch level), making self-attention tractable at each hierarchy level; geometric reduction by factor 256 at each stage.

## Data

- **Pretraining:**
  - Source: TCGA (The Cancer Genome Atlas), 33 cancer types.
  - 10,678 FFPE H&E-stained diagnostic WSIs at 20× (≈0.5 µm/px).
  - 408,218 non-overlapping 4096×4096 regions (~38 regions per slide) for Stage 2 pretraining.
  - 104M 256×256 patches for Stage 1 pretraining.
  - Total storage: 7.7 TB.
  - Tissue segmentation via TIA Toolbox with QC to discard background-heavy regions.
- **Evaluation:**
  - Slide-level classification: BRCA subtyping (IDC vs ILC, n≈1038), NSCLC subtyping (LUAD vs LUSC, n≈1008), RCC subtyping (3-class, n≈918). 10-fold CV.
  - Survival prediction: IDC, CRC, CCRCC, PRCC, LUAD, STAD. Cross-validated c-Index.
  - Data efficiency experiments at 25% and 100% training data.
  - Patch-level: CRC-100K, BCSS, BreastPathQ (KNN evaluation).

## Training Recipe

- **Stage 1 — ViT₂₅₆-16 (DINO):**
  - Data: 104M 256×256 patches from TCGA.
  - DINO student-teacher knowledge distillation; student ϕ_s256, teacher ϕ_t256.
  - 400,000 iterations, AdamW, batch size 256, base LR 0.0005.
  - 10-epoch warmup → cosine LR decay.
  - Data augmentation: 8 local views (96×96 crops, passed through student) + 2 global views (224×224 crops, passed through teacher); horizontal flips, colour jittering, solarising on one global view.
- **Stage 2 — ViT₄₀₉₆-256 (DINO):**
  - Data: 408,218 4096×4096 regions; ViT₂₅₆-16 frozen, [CLS]₂₅₆ tokens pre-extracted and rearranged as 16×16×384 2D feature grid.
  - 200,000 iterations; same DINO recipe.
  - Local-global crops: [6×6] and [14×14] on the 16×16 feature grid (matching the scale of [96×96] and [224×224] for 256×256 inputs).
  - Standard dropout p=0.10 on all views.
- **Fine-tuning:**
  - ViT₂₅₆-16 and ViT₄₀₉₆-256 pretrained and frozen.
  - Only ViT_WSI-4096 trained: 20 epochs, Adam, batch size 1 with 32 gradient accumulation steps, LR 0.01.
  - Survival loss: cross-entropy survival loss (Zadeh & Schmidt).

## Key Ablations & Design Choices

1. **Hierarchical pretraining is critical:** HIPT with ViT₄₀₉₆-256 pretrained+frozen (505k params) achieves 0.952 AUC on NSCLC (100% data). Without pretraining (3.39M trainable params), AUC drops to 0.786–0.820 due to overfitting on small WSI datasets.
2. **Freezing prevents overfitting:** Unfreezing ViT₄₀₉₆-256 during fine-tuning degrades performance (0.952→0.820 on NSCLC 100%), even though the model is small (3.39M params). WSI datasets have only 100–1000 slides.
3. **Attention pooling baseline:** Replacing ViT aggregation with simple attention pooling (no self-attention between tokens) gives 0.928 on NSCLC — better than unfrozen ViT, worse than frozen pretrained HIPT.
4. **KNN self-supervised evaluation:** Mean ViT₄₀₉₆-256 embeddings outperform supervised CLAM-SB on BRCA and RCC subtyping without any labels, demonstrating strong unsupervised representations.
5. **Pan-cancer vs organ-specific pretraining (ViT₂₅₆-16):** Pan-cancer pretraining gives better cell localisation (tumour, lymphocytes) than BRCA-only pretraining, with similar patch-level classification performance.
6. **Feature concatenation across ViT layers:** Concatenating [CLS] from last 4 stages of ViT₂₅₆-16 (1536-d) gives no improvement over last-stage only (384-d).
7. **Context matters for survival:** Largest performance gains over baselines appear in survival prediction tasks (e.g., IDC c-Index 0.634 vs 0.534 for GCN-MIL), where long-range spatial dependencies (tumour-immune localisation) are prognostically important.

## Reported Insights

- **Hierarchical structure as inductive bias:** WSIs have a fixed scale at a given magnification, creating a natural part-whole hierarchy (cells → patches → regions) that can be exploited by recursive ViT aggregation. This is distinct from natural images where scale invariance is needed.
- **Self-supervised ViTs learn interpretable morphology:** ViT₂₅₆-16 attention heads separate three phenotype groups (stroma/blood, cells, white spaces). ViT₄₀₉₆-256 heads capture tumour-stroma interface vs high tumour cellularity. Hierarchical attention maps combine these for fine-grained tumour localisation.
- **Analogy to NLP:** HIPT is motivated by hierarchical document representations (character → word → sentence → paragraph). The recursive ViT structure mirrors approaches like HIBERT for long-document modelling.
- **Limitations acknowledged:** (1) Cannot pretrain the slide-level aggregation layer (too few WSI data points for DINO). (2) End-to-end hierarchical pretraining intractable on commercial workstations. (3) TCGA-only data; evaluation lacks independent test cohorts. (4) TCGA overrepresents European ancestry. (5) [4096×4096] patching excludes some slides with limited tissue content.

## References Worth Chasing

1. **DINO** — Caron et al., 2021 — self-supervised ViT via knowledge distillation; core pretraining method [14].
2. **CLAM** — Lu et al., 2020 (Nat Biomed Eng) — data-efficient weakly-supervised MIL with attention; main baseline [54].
3. **HIBERT** — Zhang et al., 2019 — hierarchical pre-training of bidirectional transformers for documents; architecture inspiration [84].
4. **DS-MIL** — Li et al., 2021 — dual-stream multi-scale MIL with self-supervised contrastive learning [46].
5. **TransMIL** — Shao et al., 2021 — Transformer-based correlated MIL [66].
6. **ViT** — Dosovitskiy et al., 2021 — Vision Transformer; base architecture [24].
7. **Swin Transformer** — Liu et al., 2021 — hierarchical ViT with shifted windows; multiscale comparator [52].
8. **BEiT** — Bao et al., 2022 — BERT pretraining for image transformers; alternative SSL approach mentioned [6].
9. **MAE** — He et al., 2021 — masked autoencoders; future direction for hierarchical pretraining [34].
10. **NesT** — Zhang et al., 2022 — Nested Hierarchical Transformer; related hierarchical architecture [85].
11. **Hierarchical Perceiver** — Carreira et al., 2022 — similar partition-and-aggregate approach [15].
12. **Campanella et al., 2019** (Nat Med) — clinical-grade weakly-supervised pathology at scale [13].
13. **ABMIL** — Ilse et al., 2018 — attention-based MIL; foundational aggregation baseline [39].
14. **GCN-MIL** — Zhao et al., 2020 — graph convolution for slide-level prediction [86].

## Notes / Open Questions

- **Total parameter count ambiguous:** Paper states "<10M total" but ViT₂₅₆-16 alone with d=384 and multiple layers is likely >5M; the <10M claim may refer to the aggregation stages (ViT₄₀₉₆-256 + ViT_WSI-4096) only, or to a smaller-than-standard ViT₂₅₆-16 variant.
- **Training compute not reported:** No GPU-hours or wall-clock time given for either Stage 1 (400k iters, batch 256) or Stage 2 (200k iters).
- **TCGA-only pretraining and evaluation:** No independent test cohorts; potential data leakage concern. Later works (Prov-GigaPath, UNI) showed TCGA-pretrained models underperform on external data.
- **Slide-level aggregation not pretrained:** Only two stages of DINO pretraining; the ViT_WSI-4096 is trained from scratch during fine-tuning due to insufficient number of WSI data points for DINO.
- **Superseded by later pathology FMs:** Prov-GigaPath (2024) explicitly ablates GigaPath vs HIPT and shows LongNet aggregation with DINOv2 tile encoder outperforms HIPT. UNI, Virchow, CONCH have since raised the bar. HIPT remains an important architectural milestone.
- **Code available:** https://github.com/mahmoodlab/HIPT
