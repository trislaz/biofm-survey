---
id: rudolfv-a-foundation-model-2024
title: 'RudolfV: A Foundation Model by Pathologists for Pathologists'
authors:
- Jonas Dippel
- Barbara Feulner
- Tobias Winterhoff
- Timo Milbich
- Stephan Tietz
- Simon Schallenberg
- Gabriel Dernbach
- Andreas Kunft
- Simon Heinke
- Marie-Lisa Eich
- Julika Ribbat-Idel
- Rosemarie Krupar
- Philipp Anders
- Niklas Prenißl
- Philipp Jurmeister
- David Horst
- Lukas Ruff
- Klaus-Robert Müller
- Frederick Klauschen
- Maximilian Alber
year: 2024
venue: null
arxiv: '2401.04079'
doi: null
url: https://arxiv.org/abs/2401.04079v4
pdf_path: papers/rudolfv-a-foundation-model-2024.pdf
md_path: papers/md/rudolfv-a-foundation-model-2024.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: medium
tags:
- pathology-fm
- dinov2
- self-supervised
- vit
- data-curation
- ihc
- rare-disease
parameters: 304M
training_tokens: null
training_compute: 16xA100-40GB_625k-iters
references_chased: false
added_at: '2026-04-22T19:37:15+00:00'
updated_at: '2026-04-22T20:25:23+00:00'
---

## TL;DR

RudolfV is a ViT-L/14 pathology foundation model (304M params) trained with DINOv2 on 134k slides (34k cases) from 15+ labs, 58 tissue types, and 129 staining modalities. Its key contribution is systematic incorporation of pathologist domain knowledge into data curation (slide grouping, tissue clustering) and training (stain augmentation). Outperforms UNI (trained on similar data scale) on 10/12 benchmarks and Virchow (10× more data, 2× params) on 2/3 benchmarks, demonstrating that expert-guided data curation can substitute for raw data scale.

## Model

- **Architecture**: ViT-L/14 with registers (DINOv2 framework)
- **Parameters**: 304M (vs Virchow's 632M)
- **Embeddings**: Final foundation model embeddings defined following Virchow's approach
- **Initialization**: Distilled DINOv2 pretrained on LVD-142M (natural images), shown to improve performance
- **Framework**: DINOv2 with iBOT-style online tokenizer and register tokens

## Data

- **Scale**: 133,998 slides, 34,103 cases → 1.25 billion patches (256×256 px at 0.5 mpp)
- **Sources**: 81% from proprietary archive (15+ EU/US labs), 19% from TCGA
- **Tissue diversity**: 58 tissue types across 14 organ systems
- **Staining diversity**: 129 unique staining types — H&E (68%), IHC (15%), other/special stains (17%). First pathology FM to include IHC and special stains in SSL training
- **Scanners**: 6 scanner types (Roche Ventana DP600, Leica Aperio GT 450, 3DHISTECH PANNORAMIC 1000, etc.) at 20×/40×/80× magnification
- **Preparation**: FFPE and fresh-frozen samples
- **Key differentiator**: Multi-stain, multi-lab diversity rather than raw scale

## Training Recipe

1. **Patch extraction**: Tissue boundaries detected with in-house model → 1.25B patches at 256×256 px, 0.5 mpp
2. **Slide-level grouping**: Pathologists + computational scientists assign slides to 31 groups based on lab, tissue type, disease, staining — maximize within-group homogeneity, between-group heterogeneity. Non-H&E groups upsampled
3. **Patch-level clustering**: 36 standard CV image features (RGB/LAB/HSV/HED statistics) extracted per patch → subsample 500 patches/slide → k-means (k=100) → propagate labels via kNN to all 1.25B patches → pathologists merge 100 clusters into 9 interpretable tissue clusters with sampling weights. No deep features used (computational efficiency)
4. **Stain augmentation**: Per slide, compute staining statistics. At each training step, randomly transfer color profile from a different slide in the batch using Reinhard color transfer
5. **Additional augmentations**: 90° rotations, horizontal/vertical flips (histology has no canonical orientation); removed solarization from DINOv2 defaults
6. **Optimizer**: Cosine LR schedule (2e-4 → 0), 100k warmup steps, weight decay schedule 0.04 → 0.2
7. **Hardware**: 16× A100-40GB GPUs, batch size 960, 625k iterations

## Key Ablations & Design Choices (MOST IMPORTANT)

- **Data curation > data scale**: RudolfV with 134k slides outperforms UNI (100k slides, same framework) on 10/12 benchmarks and 27/31 datasets, and Virchow (1.5M slides, 2× params) on 2/3 benchmarks — evidence that pathologist-guided curation is more valuable than brute-force scale
- **ImageNet initialization matters**: Initializing from distilled DINOv2 (natural images) shown to improve performance over random init in smaller experimental setups
- **Stain augmentation for robustness**: Transferring stain/scanner color profiles between patches during training discourages the model from exploiting staining/scanner artifacts ("Clever Hans" effects). Qualitative PCA analysis shows approximately stain-invariant and scanner-invariant representations
- **Slide grouping + tissue clustering**: Balancing sampling across 31 slide groups and 9 tissue clusters addresses heavy-tailed disease distribution in pathology — rare diseases get adequate representation during training
- **Simple patch features for clustering**: Used 36 handcrafted image features (color statistics) instead of deep network features for patch clustering — much cheaper computationally, still effective
- **Removed solarization**: Following prior work on histopathology augmentations
- **Cross-tissue generalization**: TME cell classifier trained on NSCLC only generalizes to other indications (65.5% bal. acc. with RudolfV vs 36.2% without FM), confirming cross-tissue pattern learning
- **Foundation model choice matters for finetuning**: 22.9% relative improvement when finetuning RudolfV encoder vs frozen linear probing — model's intrinsic parameter structure strongly influences subsequent learning
- **IHC inclusion is beneficial**: First FM to include IHC stains in SSL training and evaluation; outperforms on novel IHC benchmarks (21.6% avg improvement in IHC cell classification)
- **No ablation table isolating individual contributions**: Paper does not provide controlled ablations separating the effect of grouping, clustering, stain augmentation, and data diversity — overall approach is evaluated as a package

## Reported Insights

- Pathology data has a heavy-tailed disease distribution; balanced sampling with domain expertise addresses this without requiring massive datasets
- Foundation models learn cross-staining morphological concepts (same tissue stained H&E and IHC shows consistent PCA components)
- Scanner invariance is achievable: same tissue scanned by 4 different scanners yields approximately identical learned representations
- Reference case search for rare diseases is enabled by FMs: 41% top-1 and 67% top-10 accuracy for 178 rare GI disease cases (vs 0%/1.7% with ImageNet ResNet-50)
- Performance plateau observed for "easier" tasks (tissue segmentation) across FMs — differentiation comes on harder tasks (cell classification, rare disease retrieval, IHC scoring)
- Named after Rudolf Virchow, pioneer of modern pathology, whose institute the data partially originates from

## References Worth Chasing

- **UNI** (Chen et al., 2024, ref [19]): General-purpose pathology FM, 100k slides, DINOv2 — main comparable baseline
- **Virchow** (Vorontsov et al., 2023, ref [20]): 1.5M slide pathology FM, ViT-H, DINOv2 — larger scale comparison
- **Phikon** (Filiot et al., 2023, ref [18]): iBOT-based pathology FM, 6k slides — smaller scale reference
- **PRISM** (Shaikovski et al., 2024, ref [21]): Multi-modal generative FM for histopathology
- **Pluto** (Juyal et al., 2024, ref [39]): Novel pretraining methods for pathology
- **DINOv2** (Oquab et al., 2023, ref [8]): Core SSL framework used
- **Vo et al., 2024** (ref [37]): Automatic data curation for SSL using clustering — related approach in natural images

## Notes / Open Questions

- No model weights publicly released (Aignostics proprietary)
- Training data is largely proprietary (81% from internal archive) — reproducibility is limited
- No controlled ablations isolating each design choice (grouping, clustering, stain aug, init, diversity) — hard to attribute gains to specific components
- Missing cytopathology and hematopathology data (acknowledged limitation)
- How does the approach scale to larger models (ViT-H, ViT-G) and larger datasets?
- Comparison to Virchow limited to 3 benchmarks due to availability constraints
- Evidence quality rated "medium": strong benchmark suite but proprietary data/models and no isolated ablations

## Abstract (from arxiv)

Artificial intelligence has started to transform histopathology impacting clinical diagnostics and biomedical research. However, while many computational pathology approaches have been proposed, most current AI models are limited with respect to generalization, application variety, and handling rare diseases. Recent efforts introduced self-supervised foundation models to address these challenges, yet existing approaches do not leverage pathologist knowledge by design. In this study, we present a novel approach to designing foundation models for computational pathology, incorporating pathologist expertise, semi-automated data curation, and a diverse dataset from over 15 laboratories, including 58 tissue types, and encompassing 129 different histochemical and immunohistochemical staining modalities. We demonstrate that our model "RudolfV" surpasses existing state-of-the-art foundation models across different benchmarks focused on tumor microenvironment profiling, biomarker evaluation, and reference case search while exhibiting favorable robustness properties. Our study shows how domain-specific knowledge can increase the efficiency and performance of pathology foundation models and enable novel application areas.
