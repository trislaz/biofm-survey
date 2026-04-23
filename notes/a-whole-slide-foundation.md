---
id: a-whole-slide-foundation
title: A whole-slide foundation model for digital pathology from real-world data
authors: []
year: 2024
venue: Nature
arxiv: null
doi: 10.1038/s41586-024-07441-w
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/a-whole-slide-foundation.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: full-text
tags:
- foundation-model
- self-supervised
- DINOv2
- LongNet
- ViT-giant
- computational-pathology
- whole-slide-modelling
- masked-autoencoder
- vision-language
- CLIP
- open-weight
parameters: ~1.13B tile encoder (ViT-giant, 1536-d) + ~86M slide encoder (LongNet
  12L 768d); small variant 23M
training_tokens: 1.3B image tiles (tile SSL) + 171k slides × 30 epochs (slide SSL)
training_compute: 3,072 A100 GPU-hours (slide encoder only); tile encoder compute
  not reported
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'Prov-GigaPath: whole-slide pathology foundation model.'
---

## TL;DR

Prov-GigaPath is an open-weight whole-slide pathology foundation model pretrained on 1.3 billion 256×256 tiles from 171,189 H&E/IHC slides (Providence health network, 30k+ patients, 31 tissue types). The GigaPath architecture combines a ViT-giant tile encoder (DINOv2 SSL) with a LongNet-based slide encoder (masked-autoencoder SSL) that handles up to ~70k tiles per slide via dilated self-attention. SOTA on 25/26 tasks (17 pathomics + 9 subtyping), with significant gains on 18. Vision–language extension (CLIP with pathology reports + PubMedBERT) achieves SOTA zero-shot subtyping and first-ever zero-shot gene mutation prediction.

## Model

- **Name:** Prov-GigaPath (architecture: GigaPath).
- **Tile encoder:** ViT-giant/14 with DINOv2 self-supervised learning. Output: 1536-d embedding per 256×256 tile (resized to 224×224 at inference). ~1.13B parameters.
- **Slide encoder:** LongNet with dilated self-attention + masked autoencoder pretraining. 12 layers, 768 hidden dim, input dim 1536. ~86M parameters. Serialises tiles in row-major order; tile coordinates discretised on a 256-cell grid (dgrid=256, ngrid=1000).
- **Downstream head:** Softmax ABMIL attention over contextualised tile embeddings → slide embedding → task-specific classifier.
- **Small variant:** 23M parameters (presumably ViT-small tile encoder); also outperforms prior SOTA.
- **Inference speed:** ~0.7 s per WSI (0.4 s tile encoding + 0.3 s LongNet).
- **Vision–language extension:** CLIP contrastive alignment of Prov-GigaPath (visual) + PubMedBERT (text) on 17,383 slide–report pairs cleaned with GPT-3.5.

## Data

- **Prov-Path (pretraining):**
  - Source: Providence health network, 28 cancer centres, real-world clinical data.
  - 1,384,860,229 (1.3B) tiles of 256×256 at 20× (0.5 µm/px).
  - 171,189 H&E + IHC pathology slides.
  - >30,000 patients, 31 major tissue types.
  - >5× TCGA in tiles, >2× in patients.
  - Includes histopathology findings, cancer staging, genomic mutation profiles, pathology reports.
  - Max tiles per slide: 70,121.
- **Vision–language pairs:** 17,383 WSI–report pairs from Prov-Path. Reports cleaned via GPT-3.5 in-context learning (4 manually cleaned exemplars).
- **Evaluation benchmarks:**
  - Providence: 17 pathomics tasks (18-biomarker pan-cancer, LUAD 5-gene, pan-cancer 5-gene, TMB) + 9 cancer subtyping tasks (NSCLC, BRCA, RCC, COADREAD, HB, DIFG, OVT, CNS, EGC).
  - TCGA: LUAD 5-gene mutation (out-of-distribution test).
  - New colorectal cohort (403 patients, post-March 2023, temporal OOD).
- **Preprocessing:** Otsu thresholding at downsampled resolution → resize to 0.5 µm/px → 256×256 crop → discard tiles with <10% tissue. Parallelised on up to 200 nodes (32 CPU, 256 GB RAM), ~157 hours.

## Training Recipe

- **Stage 1 — Tile-level SSL (DINOv2):**
  - Data: all 1.3B tiles, each tile = one instance.
  - Architecture: ViT-giant/14 with standard DINOv2 settings.
  - LR: 4×10⁻³ (base). Batch size: 12 per GPU, 384 effective.
  - Compute: not reported.
- **Stage 2 — Slide-level SSL (LongNet + MAE):**
  - Tile encoder frozen; only slide encoder trained.
  - LR: 5×10⁻⁴. Batch size: 4 per GPU.
  - Epochs: 30 (first epoch = warmup).
  - Augmentations: cropping ratio 0.875, random translation (uniform), horizontal flip (p=0.5).
  - Compute: 16 nodes × 4 A100-80GB = 64 GPUs, ~2 days = **3,072 A100 GPU-hours**.
- **Stage 3 — Vision–language (CLIP, optional):**
  - 17,383 slide–report pairs.
  - Visual encoder: Prov-GigaPath. Text encoder: PubMedBERT (text-embedding-ada-002 used for report embeddings during cleaning).
  - LR: 5×10⁻⁴. Batch size: 32. Epochs: 10 (100-iteration warmup).
  - Both visual and text encoder trained. OpenCLIP codebase.
- **Downstream fine-tuning:**
  - Tile encoder frozen; LongNet slide encoder fine-tuned.
  - Mutation tasks: LR 2×10⁻³, WD 0.01, batch 1 with 32 gradient accumulation steps, 20 epochs, 10-fold CV.
  - Subtyping tasks: LR 4×10⁻³, WD 0.001, layer-wise LR decay 0.9, 20 epochs, 10-fold CV.

## Key Ablations & Design Choices (quantitative)

1. **LongNet pretraining vs random init slide encoder:** Average subtyping AUROC 0.903 → 0.886 (P < 2.0×10⁻³). Pretraining the slide encoder is critical.
2. **Frozen vs unfrozen LongNet at fine-tuning:** Comparable performance on subtyping — pretraining already captures high-quality representations.
3. **LongNet slide encoder vs ABMIL-only aggregation:** LongNet significantly better (P < 0.012), confirming value of modelling long-range dependencies.
4. **Tile-level SSL method:** DINOv2 > SimCLR > MAE for tile pretraining (Supplementary Fig. 4).
5. **Prov-Path vs TCGA pretraining (same GigaPath architecture):** Prov-Path substantially better on TCGA LUAD 5-gene test, despite TCGA being in-distribution for TCGA-pretrained models (Extended Data Fig. 6).
6. **GigaPath vs HIPT (both on Prov-Path):** GigaPath outperforms, validating the LongNet aggregation over HIPT's hierarchical 4096×4096 ViT (Extended Data Figs. 7–8).
7. **Self-supervised vs supervised ImageNet baseline:** SSL foundation models >> task-specific supervised models (Supplementary Fig. 4).
8. **Headline results:**
   - 25/26 tasks SOTA; significant improvement on 18/26.
   - EGFR mutation (TCGA): +23.5% AUROC, +66.4% AUPRC vs REMEDIS (second-best, pretrained on TCGA).
   - Pan-cancer 18 biomarkers: +3.3% macro-AUROC, +8.9% macro-AUPRC.
   - LUAD 5-gene: 0.626 average macro-AUROC (P < 0.01 vs all baselines).
   - TMB prediction: 0.708 AUROC.
   - Cancer subtyping: best on all 9 types, significant on 6.
   - Zero-shot NSCLC/COADREAD subtyping & 6-gene mutation prediction: SOTA vs MI-Zero, BiomedCLIP, PLIP (P < 0.001 on mutations).

## Reported Insights

- **Real-world data scale matters:** Prov-Path (1.3B tiles, 171k slides) enables generalisation even to TCGA-distribution data where competing models were pretrained.
- **Whole-slide context is key:** LongNet's dilated attention over up to ~70k tiles captures global morphological patterns that tile-level models miss; biggest gains on mutation prediction (requires global tumour composition).
- **Temporal OOD robustness:** Post-March-2023 colorectal cohort shows no significant performance drop vs training-period data.
- **Vision–language potential:** Slide-level CLIP alignment with real-world pathology reports outperforms tile-level VLMs (MI-Zero, PLIP, BiomedCLIP), especially for mutation prediction — first zero-shot gene mutation prediction in pathology.
- **Limitations acknowledged:** (1) Variable performance across tasks — mutation prediction harder than subtyping. (2) Single magnification (20×); higher magnification may improve detail at cost of 4× compute. (3) Tile encoder frozen during slide encoder pretraining (memory constraint). (4) Vision–language far from conversational clinical assistant. (5) Scaling laws partially observed but not systematically validated.

## References Worth Chasing (≤15 bio-FM refs)

1. **DINOv2** — Oquab et al., 2023 — tile-level SSL backbone (ref 24).
2. **LongNet** — Ding et al., 2023 — dilated attention for ultra-long sequences, slide encoder core (ref 5).
3. **HIPT** — Chen et al., 2022 (CVPR) — hierarchical ViT for gigapixel pathology, main baseline (ref 35).
4. **CTransPath** — Wang et al., 2022 — CNN + SwinTransformer, MoCoV3, pathology FM baseline (ref 41).
5. **REMEDIS** — Azizi et al., 2023 — ResNet-152 SimCLR on 50M TCGA tiles, medical imaging FM (ref 42).
6. **MI-Zero** — Lu et al., 2023 — pathology VLM, PubMedBERT, zero-shot transfer baseline (ref 7).
7. **PLIP** — Huang et al., 2023 — pathology vision-language FM from Twitter image–text (ref 8).
8. **BiomedCLIP** — Zhang et al., 2023 — 15M biomedical image-caption pairs, CLIP-style FM (ref 50).
9. **PubMedBERT** — Gu et al., 2021 — biomedical domain-specific BERT, text encoder (ref 29).
10. **MAE** — He et al., 2022 — masked autoencoder, basis for slide-level pretraining (ref 45).
11. **SimCLR** — Chen et al., 2020 — contrastive learning baseline (ref 26).
12. **LLaVA-Med** — Li et al., 2023 — multimodal medical LLM, cited as future direction (ref 52).
13. **Transformer** — Vaswani et al., 2017 — foundational architecture (ref 44).
14. **ABMIL / MIL** — Ilse et al., 2018 — attention-based multiple instance learning aggregation (ref 4).
15. **Campanella et al., 2019** (Nat Med) — clinical-grade weakly-supervised pathology (ref 14).

## Notes / Open Questions

- **Tile encoder compute not reported** — only slide encoder training cost (3,072 A100-h) is given; tile-level DINOv2 pretraining on 1.3B tiles likely dominates total compute but is unstated.
- **Exact parameter count not in paper** — ViT-giant inferred from 1536-d output and HuggingFace model card (`gigapath_slide_enc12l768d`); paper only states "23M" for the small variant.
- **Single health system** — all pretraining data from Providence; cross-system pretraining could improve diversity. Compare Virchow (single institution MSKCC) for similar trade-off.
- **No end-to-end pretraining** — tile encoder frozen during slide-level MAE; authors note this is suboptimal and plan joint training with larger GPU clusters.
- **No scaling-law analysis** — paper observes larger data/model helps (Prov-Path > TCGA, GigaPath > HIPT) but does not systematically vary model size or data size.
- **Vision–language is preliminary** — 17k WSI–report pairs is small; zero-shot mutation prediction is novel but absolute performance still limited.
- **Open weights** — code and model available on HuggingFace (prov-gigapath/prov-gigapath), Apache 2.0 license, research-use only.

## Verification (Rev 3)

Each claim from `insights.md` tagged `[a-whole-slide-foundation]` is checked against the PMC full text (`papers/md/a-whole-slide-foundation.md`).

| # | insights.md line | Claim (paraphrased) | Verdict | Evidence / notes |
|---|---|---|---|---|
| 1 | L35 | "GigaPath scales to 1.3 B tiles using DINOv2 + LongNet" | **supported** | Paper abstract: "pretrained on 1.3 billion 256 × 256 pathology image tiles"; architecture confirmed as DINOv2 tile encoder + LongNet slide encoder (Main §2, Methods). |
| 2 | L137 | "ViT-giant (1.13 B params) + LongNet slide aggregation (86 M); DINOv2 > SimCLR > MAE for tile encoding" | **partial** | DINOv2 > SimCLR > MAE confirmed (paper cites Supplementary Fig. 4). ViT-giant architecture and LongNet confirmed. However, the specific parameter counts (1.13 B tile encoder, 86 M slide encoder) are **not stated in the paper text**; they are inferred from the ViT-giant spec and the HuggingFace model card. |
| 3 | L209 | "GigaPath \| Pathology \| 131 k tiles per WSI \| LongNet dilated attention" | **unsupported** | The paper states the maximum tiles per WSI is **70,121** ("as many as 70,121 in the Providence data", Main §2). The figure "131 k" does not appear anywhere in the paper and overstates the max context by ~1.9×. LongNet dilated attention is correct. |
| 4 | L243 | "GigaPath ingested 1.3 B tiles from 171 K slides" | **supported** | Paper: "1,384,860,229 image tiles from 171,189 whole slides" (abstract, Main §2, Methods). |
| 5 | L256 | "Late-fusion … GigaPath uses separate tile (ViT-giant) and slide (LongNet) encoders aggregated only at the final classification layer" | **partial** | The two-encoder architecture is correct. However, labelling it "late fusion" is misleading: (a) both encoders operate on the same modality (pathology images at different scales), not separate modalities; (b) the LongNet slide encoder **contextualises** tile embeddings before the ABMIL aggregation layer, so fusion is not deferred to the decision layer — it is a hierarchical encoder, not a late-fusion design. |
| 6 | L310 | "GigaPath trains on 1.3 B tiles with ViT-giant (1.13 B params), showing DINOv2 > SimCLR > MAE" | **partial** | 1.3 B tiles, ViT-giant, DINOv2 > SimCLR > MAE all confirmed. The 1.13 B parameter count is not in the paper (see claim 2). |
| 7 | L542–543 | "ViT-giant tiles (1.13 B) + LongNet slide encoder (86 M) on 1.3 B tiles from 171 K slides; DINOv2 > SimCLR > MAE; LongNet significantly outperforms ABMIL-only" | **partial** | Data scale, architecture, DINOv2 ranking, and LongNet vs ABMIL (P < 0.012) all confirmed. Parameter counts (1.13 B, 86 M) not in paper text (inferred from model card). |

**Summary:** 2 supported, 4 partial (parameter counts sourced from model card, not paper; or architectural characterisation imprecise), 1 unsupported (131 k max tiles should be ~70 k).

## Ablations (Rev 4)

Ablations reported in the paper (Main §"Comparison on cancer subtyping" L65, Supplementary Figs. 4–5, Extended Data Figs. 6–8) on cancer subtyping (avg AUROC over 9 cancer types, n=10 runs) and gene-mutation prediction.

| # | Component varied | Variant | Baseline | Δ / metric | Significance | Source | Take-away |
|---|---|---|---|---|---|---|---|
| 1 | Slide-encoder pretraining | LongNet randomly initialised | LongNet pretrained on Prov-Path | AUROC 0.886 vs **0.903** (−0.017) | P < 2.0 × 10⁻³ | Main §L65, Supp. Fig. 5 | Slide-level MAE pretraining on 171 K WSIs is necessary; random init loses ~1.7 AUROC pts on subtyping. |
| 2 | LongNet fine-tuning regime | Frozen vs unfrozen during downstream training | — | "comparable" (no significant gap) | n.s. | Main §L65, Supp. Fig. 5 | Pretrained representations are strong enough to be used frozen — important for compute-limited deployment. |
| 3 | Slide aggregator | ABMIL only (drop LongNet) | LongNet + ABMIL head | LongNet > ABMIL on average AUROC | P < 0.012 | Main §L65, Supp. Fig. 5 | Long-range dilated self-attention adds value beyond a simple attention-MIL pooler; modelling cross-tile dependencies matters for subtyping. |
| 4 | Tile-encoder SSL objective | SimCLR; MAE; SL-ImageNet (supervised) | DINOv2 | DINOv2 > SimCLR > MAE > SL-ImageNet | reported as significant | Main §L53, §L83, Supp. Fig. 4 | DINOv2 is the best tile-level SSL recipe for pathology at this scale; supervised ImageNet transfer is clearly inferior, motivating SSL foundation models. |
| 5 | Tile-encoder pretraining data | Same GigaPath arch pretrained on TCGA (~29 K slides) | Pretrained on Prov-Path (171 K slides, 1.3 B tiles) | Substantial drop on TCGA LUAD 5-gene mutation | reported as substantial (no exact P) | Main §L53, §L83, Ext. Data Fig. 6 | Data scale + diversity (real-world Providence corpus) drives gains beyond what TCGA alone delivers — evidence of (informal) data-scaling. |
| 6 | Slide-level architecture | HIPT (hierarchical ViT) trained on Prov-Path | GigaPath (LongNet) trained on Prov-Path | GigaPath > HIPT | reported as significant | Main §L53, §L83, Ext. Data Figs. 7–8 | At matched data, LongNet's dilated long-context attention outperforms HIPT's hierarchical pooling for whole-slide modelling. |

**Count:** 6 ablation comparisons (3 from Supp. Fig. 5 in-text; 1 tile-SSL sweep from Supp. Fig. 4; 2 data/architecture comparisons from Ext. Data Figs. 6–8).

**Top take-away:** The single most informative ablation is #1 — pretraining the LongNet slide encoder on Prov-Path lifts mean subtyping AUROC from 0.886 to 0.903 (P < 2 × 10⁻³), directly justifying the costly second-stage WSI-level MAE (3,072 A100 GPU-hours). Combined with #3 (LongNet > ABMIL), this establishes that *both* slide-level pretraining *and* long-context attention — not just a strong tile encoder — are required to reach GigaPath's reported performance.
