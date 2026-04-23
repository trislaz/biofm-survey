---
id: knowledge-enhanced-pretraining-for-2024
title: Knowledge-enhanced Pretraining for Vision-language Pathology Foundation Model
  on Cancer Diagnosis
authors:
- Xiao Zhou
- Luoyi Sun
- Dexuan He
- Wenbin Guan
- Ge Wang
- Ruifen Wang
- Lifeng Wang
- Xiaojun Yuan
- Xin Sun
- Ya Zhang
- Kun Sun
- Yanfeng Wang
- Weidi Xie
year: 2024
venue: null
arxiv: '2412.13126'
doi: null
url: https://arxiv.org/abs/2412.13126v2
pdf_path: papers/knowledge-enhanced-pretraining-for-2024.pdf
md_path: papers/md/knowledge-enhanced-pretraining-for-2024.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: high
tags:
- vision-language
- knowledge-graph
- contrastive-learning
- zero-shot
- cancer-diagnosis
- pathology-foundation-model
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:15+00:00'
updated_at: '2026-04-22T20:22:31+00:00'
---

## TL;DR

KEEP is a vision-language pathology foundation model that injects structured disease knowledge (a KG of 11,454 diseases) into contrastive pre-training. It reorganises noisy image-text pairs from OpenPath+Quilt1M into 143K semantically structured groups aligned with disease ontology hierarchies, and uses metric-learning–based semantic alignment with false-negative elimination. Evaluated zero-shot on 18 public WSI benchmarks (>14K WSIs) and 4 in-house rare cancer datasets, KEEP consistently outperforms CONCH, MUSK, PLIP, and CHIEF, with particularly large gains on rare cancer subtyping (+8.5 BACC over CONCH on EBRAINS).

## Model

- **Name**: KEEP (KnowledgE-Enhanced Pathology)
- **Architecture**: Dual-encoder vision-language model
  - **Vision encoder**: ViT-L/16, initialised from UNI (self-supervised pathology FM)
  - **Text encoder**: PubMedBERT architecture (embedding dim 768), first pre-trained on a disease knowledge graph via AdaSP metric learning, then used as the text branch during VL alignment
- **Parameters**: Not explicitly reported. ViT-L/16 ≈ 307M + PubMedBERT ≈ 110M → ~417M total (estimated)
- **Input**: 224×224 pathology tile images + text prompts
- **Inference**: Zero-shot tile-level classification; WSI-level predictions via tumor-ratio aggregation (non-parametric, no MIL training needed)

## Data

- **Knowledge graph**: 11,454 disease entities with 139,143 attributes (14,303 definitions, 15,938 hypernym relations, 108,902 synonyms) sourced from Disease Ontology (DO) and UMLS
- **Image-text pairs**: OpenPath (~208K pairs) + Quilt1M (~1M pairs), filtered and reorganised into **143,000 semantic groups** using:
  1. YOLOv8 fine-tuned on 1K manually annotated images to crop/filter non-pathology images (99.9% purity)
  2. SpaCy NER + UMLS entity matching to discard captions without medical entities
  3. UNI embeddings to cluster visually similar images (threshold 0.95)
  4. MI-Zero embeddings to select the most representative caption per group
  5. Token-set IoU >0.9 merging across groups
- **Evaluation**: 18 public WSI benchmarks (>14K WSIs) across segmentation (CAMELYON16, PANDA, AGGC22), detection (7 CPTAC datasets), subtyping (TCGA-BRCA/NSCLC/RCC/ESCA/Brain, CPTAC-NSCLC, UBC-OCEAN, EBRAINS); 4 in-house rare cancer datasets (926 WSIs: nephroblastoma, neuroblastoma, hepatoblastoma, medulloblastoma); 14 tile-level classification datasets; 4 cross-modal retrieval datasets

## Training Recipe

1. **Stage 1 — Knowledge Encoding** (disease KG → text encoder):
   - Architecture: PubMedBERT, embedding dim 768
   - Loss: AdaSP metric learning (least-hard positive + hardest negative mining)
   - Temperature τ = 0.04
   - Batch: 256 (32 disease entities × 8 attributes each)
   - Training: 100 epochs, max LR 3×10⁻⁵, 4× A100 GPUs

2. **Stage 2 — Vision-Language Pre-training**:
   - Vision encoder: ViT-L/16 (init from UNI), text encoder: from Stage 1
   - Input: 224×224 tiles (random-cropped from 512×512)
   - Loss: Semantic-level contrastive with least-hard positive mining, hardest negative mining, and false-negative elimination via hypernym path reachability
   - Caption augmentation: 50% probability of randomly dropping 40% of words; disease names replaced with templated prompts or hierarchical disease chains
   - Batch: 128 (32 semantic groups × 4 image-text pairs)
   - Temperature τ = 0.04
   - Training: 10 epochs, max LR 1×10⁻⁵, **1× A100 GPU**

3. **Downstream zero-shot WSI inference**:
   - Tiles 256×256 (or 224×224 for segmentation) at 20× magnification
   - 50 text prompts ensembled per task via unsupervised prompt screening (ranking by discriminability + range consistency)
   - Cancer detection / subtyping via tumor-ratio aggregation (ratio of tumour tiles to total tiles)
   - Post-processing: morphological opening for segmentation

## Key Ablations & Design Choices (MOST IMPORTANT)

1. **Knowledge enhancement vs naïve contrastive** (same backbone, no KG): Knowledge yields avg +7.3% segmentation AUROC, +7.2% subtyping BACC across all WSI tasks; +11 pts on EBRAINS rare brain tumours. Validated on 16/18 WSI datasets.
2. **Tumor-ratio aggregation vs Top-100 pooling** (CONCH/MI-Zero strategy): KEEP-Ratio beats KEEP-Top100 on all datasets; +10 BACC on CPTAC-NSCLC, +15 on TCGA-BRCA.
3. **Semantic groups vs image-text pairs**: Grouping improves cross-modal retrieval.
4. **Caption augmentation** (random word dropout + template paraphrasing): Improves performance vs no augmentation.
5. **Loss function variants**: Least-hard positive + hardest negative (KEEP's choice) outperforms other combinations (hardest-hardest, least-least, hardest-least).
6. **KG ablation — removing non-cancer diseases**: Avg -1.1% detection, -2.5% subtyping, suggesting broader ontology helps generalisation.
7. **KG ablation — removing disease relationships**: -3.4% subtyping (no effect on detection), confirming inter-disease hierarchy matters for fine-grained tasks.
8. **Text encoder ablation**: PubMedBERT without knowledge pre-training, Clinical-Longformer, and OpenAI text-embedding-3-large all significantly worse than knowledge-enhanced encoder. LLM embeddings worst, showing general-purpose LM representations fail at fine-grained biomedical discrimination.
9. **False-negative elimination**: Hypernym-path reachability check prevents semantically related groups from being treated as negatives.
10. **Vision encoder init**: UNI provides a strong pathology-specific starting point for ViT-L/16.

## Reported Insights

- Vision-language models (KEEP, CONCH, MUSK) dramatically outperform vision-only models (CHIEF) on zero-shot cancer detection because they use predicted labels rather than aggregated tile features
- KEEP's zero-shot performance exceeds 1–8 shot performance of all other foundation models on both detection and subtyping
- Rare cancer subtyping (EBRAINS 30 subtypes) is where knowledge injection helps most: KEEP 0.456 BACC vs CONCH 0.371
- Molecular subtyping (IDH-wt vs IDH-mut) remains challenging because morphological phenotypes are poorly defined
- Prompt sensitivity is a real limitation; the unsupervised prompt screening approach (Eq. 15) is a practical mitigation
- Multi-modal extensions (genomic/epigenomic) acknowledged as promising future direction

## References Worth Chasing

- **CONCH** (Lu et al., 2024, Nat Med): Main baseline; VL pathology FM with naïve contrastive learning
- **UNI** (Chen et al., 2024, Nat Med): Self-supervised pathology FM used to initialise KEEP's vision encoder
- **MUSK** (Xiang et al., 2025, Nature): VL pathology FM for precision oncology
- **CHIEF** (Wang et al., 2024, Nature): Vision-only pathology FM with MIL
- **Virchow2** (Zimmermann et al., 2024): Self-supervised mixed-magnification pathology model
- **AdaSP loss** (Zhou et al., 2023, CVPR): Adaptive sparse pairwise loss used for metric learning
- **BioCLIP** (Stevens et al., 2024, CVPR): Hierarchical knowledge chain approach that inspired KEEP's KG encoding

## Notes / Open Questions

- Total parameter count never explicitly stated; the ~417M estimate assumes no shared parameters and standard ViT-L/16 + PubMedBERT sizes
- Training is remarkably lightweight: Stage 2 uses only **1× A100** for 10 epochs — significantly cheaper than CONCH or MUSK
- Training compute and token counts are not reported
- The 143K semantic groups are derived from ~1.2M original pairs after heavy filtering; effective data scale is modest
- All WSI evaluation is zero-shot or few-shot; no end-to-end WSI-level training is performed
- The unsupervised prompt screening requires unlabelled tile images from target distribution, which is a mild assumption but not strictly zero-shot
- Code available at MAGIC-AI4Med/KEEP (MIT License); weights on HuggingFace at Astaxanthin/KEEP
