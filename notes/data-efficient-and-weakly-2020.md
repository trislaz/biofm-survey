---
id: data-efficient-and-weakly-2020
title: Data Efficient and Weakly Supervised Computational Pathology on Whole Slide
  Images
authors:
- Ming Y. Lu
- Drew F. K. Williamson
- Tiffany Y. Chen
- Richard J. Chen
- Matteo Barbieri
- Faisal Mahmood
year: 2020
venue: null
arxiv: '2004.09666'
doi: null
url: https://arxiv.org/abs/2004.09666v2
pdf_path: papers/data-efficient-and-weakly-2020.pdf
md_path: papers/md/data-efficient-and-weakly-2020.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: full-text
tags:
- mil
- weakly-supervised
- computational-pathology
- attention-pooling
- wsi-classification
- not-a-foundation-model
parameters: ~800K (CLAM head only; excludes frozen ResNet50 encoder ~23M)
training_tokens: null
training_compute: 2× NVIDIA 2080 Ti per experiment; hours-scale per task
references_chased: false
added_at: '2026-04-22T21:55:48+00:00'
updated_at: '2026-04-22T21:55:53+00:00'
is_fm: false
fm_classification_reason: 'CLAM: MIL aggregator on frozen ResNet, not a pretrained
  FM.'
---

## TL;DR

CLAM is a **MIL (Multiple Instance Learning) aggregation framework** for weakly-supervised WSI classification — **not a foundation model**. It replaces max-pooling with attention-based pooling and adds an instance-level clustering auxiliary task to improve data efficiency. A frozen, ImageNet-pretrained ResNet50 extracts 1024-d patch features; CLAM's small trainable head (~800 K params) learns to aggregate them into slide-level predictions. Achieves >0.95 AUC on three pathology tasks (RCC subtyping, NSCLC subtyping, lymph node metastasis) with only slide-level labels and moderate dataset sizes (≤2 K slides). Highly influential as the canonical MIL baseline that later pathology FMs (HIPT, CONCH, UNI, etc.) build upon or compare against.

## Model

**Architecture type:** MIL aggregator (slide-level classifier), not a self-supervised or generative foundation model.

**Feature extractor (frozen):** ResNet50 pretrained on ImageNet. Adaptive mean-spatial pooling after 3rd residual block → 1024-d patch embedding. Patches are 256×256 pixels at 20× or 40× magnification.

**CLAM head (trainable):**
- FC compression layer W₁ ∈ R^{512×1024} → 512-d patch representation hₖ.
- Shared attention backbone: Uₐ ∈ R^{256×512}, Vₐ ∈ R^{256×512} (gated attention).
- n parallel attention branches Wₐ,ₘ ∈ R^{1×256} (one per class) → per-class attention scores.
- Attention-weighted pooling → n class-specific slide-level representations (512-d each).
- n parallel classifiers Wc,m ∈ R^{1×512} → slide scores, softmax for probabilities.
- n instance-level clustering layers W_inst,m ∈ R^{2×512} (binary cluster prediction).

**Approximate parameter count (CLAM head, n=3):** FC1 ≈ 524 K + attention backbone ≈ 262 K + per-class heads ≈ 5 K ≈ **~791 K trainable params**. ResNet50 encoder (~23 M) is frozen.

## Data

| Dataset | Source | # WSIs | # Cases | Magnification | Task |
|---|---|---|---|---|---|
| TCGA-Kidney (KICH+KIRC+KIRP) | Public | 884 | 846 | 20× | RCC 3-class subtyping |
| TCGA-Lung + CPTAC-Lung | Public | 1,967 | 1,227 | 20× | NSCLC 2-class subtyping |
| Camelyon16 + Camelyon17 | Public | 899 | 370 | 40× | Lymph node met detection |
| BWH independent test sets | In-house | 135 + 131 + 133 | — | 20×/40× | Same tasks (external val) |
| BWH biopsy sets | In-house | 110 + 92 | — | 20× | Resection→biopsy transfer |
| BWH cellphone sets | In-house | 135 + 131 FOV sets | — | 20× | WSI→CPI transfer |

All training uses only public data; BWH cohorts are held-out for independent evaluation.

## Training Recipe

> **Note:** CLAM is a MIL aggregator trained with standard supervised objectives on slide-level labels — not a self-supervised FM. There is no pretraining stage for the CLAM head; the ResNet50 encoder is used as-is from ImageNet.

1. **WSI preprocessing pipeline:** (a) Automated tissue segmentation (HSV saturation thresholding + morphological closing). (b) Exhaustive 256×256 patching within segmented contours. (c) One-time feature extraction via frozen ResNet50 → 1024-d vectors, batch size 128/GPU. Reduces data ~200×.
2. **Training the CLAM head:** Features streamed from SSD. Batch size = 1 slide. Multinomial sampling inversely proportional to class frequency (class balancing).
3. **Loss:** L_total = 0.7 × L_slide (cross-entropy) + 0.3 × L_patch (smooth top-1 SVM, margin α=1.0, temperature τ=1.0). Instance-level clustering uses B=8 most/least attended patches per class.
4. **Mutual exclusivity assumption:** For subtyping, highly attended patches from out-of-class branches are labelled as false positives (extra negative supervision). Not used for binary cancer-vs-normal.
5. **Optimizer:** Adam, LR 2e-4, L2 weight decay 1e-5.
6. **Epochs / stopping:** Min 50, max 200, early stopping patience = 20 epochs on validation loss.
7. **Evaluation:** 10-fold Monte Carlo cross-validation (80/10/10 train/val/test by case). Best val-loss model tested once.
8. **Hardware:** 2× NVIDIA 2080 Ti GPUs per experiment (10 total available). Feature extraction on P100s (GCP) or 2080 Ti. Training on thousands of WSIs completes in hours.

## Key Ablations & Design Choices (quantitative)

| Comparison | RCC (AUC) | NSCLC (AUC) | LN Met (AUC) | Setting |
|---|---|---|---|---|
| CLAM (100% train) | 0.991 | 0.956 | 0.953 | Cross-val |
| MIL/mMIL (100% train) | ~comparable | −3–5% | Frequently fails (<0.5) | Cross-val |
| CLAM (25% train) → RCC | 0.94+ | — | — | Cross-val |
| CLAM (50% train) → NSCLC | — | ~0.95 | — | Cross-val |
| CLAM (100%) on independent test | 0.973 | 0.975 | 0.934 | BWH external |
| CLAM (25%) independent, RCC | +14.5% over mMIL | — | +30.1% over MIL | BWH external |

**Attention pooling vs max pooling:** Attention pooling uses gradient from all patches (weighted); max pooling uses only one patch per slide → much less efficient supervision, MIL often fails to converge on lymph node task.

**Instance-level clustering:** Adds auxiliary supervision via pseudo-labels from attention scores, refines patch-level feature space; contributes to data efficiency improvement.

**Domain transfer without fine-tuning:**
- Resection → biopsy: NSCLC AUC 0.902, RCC AUC 0.951.
- WSI → cellphone: NSCLC AUC 0.873, RCC AUC 0.921.
- Drops of ~0.05–0.10 AUC relative to WSI performance, but still clinically useful.

**Ensemble (10 cross-val models averaged):** Improves robustness; trivial compute cost since feature extraction is shared.

## Reported Insights

- Attention-based pooling provides much richer gradient signal than max-pooling MIL, enabling learning from far fewer slides.
- CLAM can identify tumor–normal boundaries without ever seeing normal slides or pixel annotations — attention heatmaps align with pathologist annotations and IHC staining.
- Instance-level clustering with mutual exclusivity assumption provides extra regularisation signal that is especially valuable in low-data regimes.
- Model confidence is well-calibrated: higher for correct predictions, decreases gracefully with less training data (not overconfident).
- Feature extraction bottleneck (ResNet50 ImageNet) is the main representational limitation — later works (HIPT, UNI, CONCH, Virchow) replace this with pathology-specific foundation models.
- Working in the extracted feature space (not pixel space) makes training on thousands of gigapixel slides feasible on consumer GPUs in hours.

## References Worth Chasing (≤15 bio-FM refs)

1. **Campanella et al. (2019)** — Clinical-grade MIL on 44K WSIs; the MIL baseline CLAM improves upon. *Nat Med* 25, 1301–1309.
2. **Ilse et al. (2018)** — Attention-based deep MIL; the attention pooling mechanism CLAM extends. *ICML 2018*.
3. **Coudray et al. (2018)** — NSCLC classification & mutation prediction from histology; patch-level supervised baseline. *Nat Med* 24, 1559.
4. **Bejnordi et al. (2017)** — Camelyon16 challenge; diagnostic assessment of DL for lymph node mets. *JAMA* 318, 2199.
5. **Mobadersany et al. (2018)** — Histology + genomics integration with CNNs for outcome prediction. *PNAS* 115, E2970.
6. **Kather et al. (2019)** — DL predicts MSI directly from histology. *Nat Med* 25, 1054.
7. **Bulten et al. (2020)** — Automated Gleason grading with DL. *Lancet Oncol*.
8. **Saltz et al. (2018)** — TIL spatial organization via DL on pathology images. *Cell Reports* 23, 181.
9. **LeCun, Bengio & Hinton (2015)** — Deep learning review. *Nature* 521, 436.
10. **Berrada et al. (2018)** — Smooth top-k SVM loss used for instance-level clustering. *ICLR 2018*.
11. **Litjens et al. (2018)** — Camelyon dataset (1399 H&E sentinel lymph node sections). *GigaScience*.
12. **Esteva et al. (2017)** — Dermatologist-level skin cancer classification. *Nature* 542, 115.

## Notes / Open Questions

- **CLAM is not a foundation model.** It is a task-specific MIL aggregation method that sits on top of a frozen ImageNet encoder. Its relevance to the bio-FM survey is as a widely-adopted **downstream evaluation framework** and as the architectural ancestor of pathology FM pipelines (feature extractor → MIL aggregator).
- The ResNet50-ImageNet feature extractor is the obvious bottleneck — would pathology-pretrained encoders (e.g., CTransPath, UNI, CONCH, Virchow) substantially change the data-efficiency story?
- No self-supervised or domain-specific pretraining is performed; all representation quality comes from ImageNet transfer.
- Mutual exclusivity assumption for subtyping is elegant but breaks for multi-label or mixed-histology scenarios.
- Instance-level clustering pseudo-labels are inherently noisy — the smooth SVM loss with margin is the mechanism to handle this, but no explicit analysis of pseudo-label quality is provided.
- Code released at https://github.com/mahmoodlab/CLAM under GPL v3 — became the de facto MIL codebase for computational pathology.
- Published 2020 (arXiv), Nature Medicine 2021. Cited >2000 times; foundational reference for any pathology FM evaluation.
