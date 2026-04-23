---
id: a-general-purpose-self-2023
title: A General-Purpose Self-Supervised Model for Computational Pathology
authors:
- Richard J. Chen
- Tong Ding
- Ming Y. Lu
- Drew F. K. Williamson
- Guillaume Jaume
- Bowen Chen
- Andrew Zhang
- Daniel Shao
- Andrew H. Song
- Muhammad Shaban
- Mane Williams
- Anurag Vaidya
- Sharifa Sahai
- Lukas Oldenburg
- Luca L. Weishaupt
- Judy J. Wang
- Walt Williams
- Long Phi Le
- Georg Gerber
- Faisal Mahmood
year: 2023
venue: null
arxiv: '2308.15474'
doi: null
url: https://arxiv.org/abs/2308.15474v1
pdf_path: papers/a-general-purpose-self-2023.pdf
md_path: papers/md/a-general-purpose-self-2023.md
modalities:
- imaging-pathology
status: extracted
evidence_quality: full-text
tags:
- vision-transformer
- DINOv2
- self-supervised
- computational-pathology
- ViT-Large
- tile-encoder
- foundation-model
- linear-probing
- few-shot
- data-scaling
parameters: 303000000
training_tokens: 100130900
training_compute: null
references_chased: false
added_at: '2026-04-22T21:55:57+00:00'
updated_at: '2026-04-22T21:55:57+00:00'
is_fm: true
fm_classification_reason: 'UNI: large self-supervised pathology foundation model.'
---

## TL;DR

UNI is a ViT-Large/16 (≈303M params) pretrained with DINOv2 on **Mass-100K**: 100,130,900 H&E tissue patches (256×256 + 512×512 at 20×) from 100,426 diagnostic WSIs across 20 organ types (MGH, BWH, GTEx — no TCGA/CPTAC). Evaluated on 33 clinical CPath tasks spanning ROI classification, segmentation, retrieval, and slide-level MIL. Outperforms CTransPath (Swin-T, 28M params, TCGA+PAIP) and REMEDIS (ResNet-152×2, 232M params, TCGA) despite seeing 4–13× fewer images during pretraining (≈384M images seen vs 1.56B CTransPath, 50B REMEDIS). Demonstrates data-scaling laws in CPath, resolution-agnostic classification, and prompt-based slide classification using ROI-level class prototypes.

## Model

- **Architecture**: ViT-Large/16 (plain, non-hierarchical). Patch token size 16×16. Input 224×224 (standard) or higher via positional-embedding interpolation. Output: 1024-dim [CLS] embedding.
- **Parameters**: ≈303M (standard ViT-L). Paper reports baselines explicitly (ResNet-50 8.5M, CTransPath 28.3M, REMEDIS 232.2M) but uses canonical ViT-L size.
- **SSL algorithm**: DINOv2 (student-teacher distillation + iBOT masked-image-modeling). Default config 1 (tied head weights, teacher softmax-centering); adds KoLeo regularizer, FlashAttention, stochastic depth, FSDP.
- **No fine-tuning labels**: model used frozen as feature extractor in most evaluations.

## Data

- **Mass-100K** (pretraining):
  - 100,426 diagnostic H&E WSIs, 20 major tissue types.
  - Sources: BWH + MGH (in-house FFPE, incl. renal/cardiac transplant), GTEx (24,782 non-cancerous autopsy WSIs).
  - Deliberately excludes TCGA, CPTAC, PAIP to allow unbiased evaluation on public benchmarks.
  - 75,832,905 patches at 256×256 px (20×) + 24,297,995 patches at 512×512 px (20×, for high-res fine-tuning) → **100,130,900 total patches**.
  - ≈800 patches sampled per WSI via CLAM tissue segmentation.
- **Mass-22K** (scaling subset): 16,059,454 patches from 21,444 WSIs (BWH only).
- **Mass-1K** (scaling subset): 1,064,615 patches from 1,404 WSIs.
- **Downstream evaluation**: 33 tasks across 15 slide-level + 10 ROI-level + 8 SegPath segmentation tasks. Key benchmarks: CAMELYON16, PANDA, BRACS, EBRAINS, TCGA-NSCLC/RCC (with external CPTAC/DHMC test sets), OncoTree-43/108.

## Training Recipe

- **SSL method**: DINOv2 (self-distillation [CLS] cross-entropy + iBOT masked-patch reconstruction).
- **Hardware**: 4 nodes × 8 × 80GB NVIDIA A100 GPUs (32 GPUs total), multi-node DDP + FSDP.
- **Schedule**: 125,000 iterations total; cosine LR schedule. LR: 0 → 2e-3 (warmup over 12,500 iters) → 1e-6. Warmup teacher temperature: 37,500 iters. Freeze last layer: 1,250 iters.
- **Batch size**: 3,072 (total across GPUs).
- **High-resolution fine-tuning**: last 12,500 iterations (10% of training) on 512×512 patches.
- **Total images seen**: 3,072 × 125,000 = **384M** — substantially fewer than CTransPath (1.56B) and REMEDIS (50B).
- **Software**: PyTorch 2.0, Timm 0.9.2, original DINOv2 codebase.

## Key Ablations & Design Choices

**Data scaling (most important result)**:
- On OncoTree-43 (43-class cancer type, 5,564 WSIs): Mass-1K → Mass-22K → Mass-100K yields +4.2% top-1 accuracy and +3.6% top-5 accuracy (both p < 0.05).
- On OncoTree-108 (108-class, most label-complex CPath task): consistent scaling trend; UNI achieves top-5 accuracy 93.8% and AUROC 0.976, outperforming REMEDIS by +6.3% and +0.022.
- Despite 4–13× fewer images seen, UNI outperforms CTransPath and REMEDIS. Evidence that data diversity (20 organs, in-house + GTEx) matters more than raw epoch count.

**DINOv2 vs alternatives**:
- Authors chose DINOv2 specifically for superior linear-probe performance (frozen feature extractor is critical for MIL workflows). Other ViT SSL methods (MAE, I-JEPA) have better fine-tuning but worse linear probe.
- Default DINOv2 config 1 used (omits head-weight untying and Sinkhorn-Knopp centering).

**Slide-level classification (ABMIL, 15 tasks)**:
- UNI outperforms all baselines across 15 slide-level tasks. Larger margins on diagnostically complex tasks.
- NSCLC subtyping (TCGA→CPTAC): 88.9% balanced accuracy. RCC subtyping: 96.3%. CAMELYON16: 95.7%.
- Data contamination analysis: REMEDIS drops from 97.3% (TCGA internal) to 79.0% (CPTAC external) on RCC; UNI maintains 94.7% → 96.3%. Strong evidence that TCGA-pretrained models exhibit transductive bias.

**ROI classification (linear probe, 10 tasks)**:
- Overall improvements: +19.9% vs ResNet-50, +9.5% vs CTransPath, +7.7% vs REMEDIS.
- KNN probing confirms representation quality advantage.

**Resolution agnosticism**:
- BRCA subtyping (BACH): UNI at 1344² outperforms CTransPath by +25.0% linear probe.
- Multi-resolution positional-embedding interpolation enables inference at arbitrary resolutions without retraining.

**Few-shot efficiency**:
- ROI: 8-shot UNI (SimpleShot) consistently exceeds 128–256-shot performance of next-best model (16–32× label efficiency).
- Slide: 4-shot UNI outperforms 32-shot REMEDIS on EBRAINS brain tumor subtyping.
- PANDA ISUP grading: UNI is 2× label-efficient across all few-shot settings.

**Segmentation (SegPath, 8 cell types)**:
- Despite ViT-L lacking hierarchical inductive biases, UNI + ViT-Adapter + Mask2Former outperforms REMEDIS on epithelial (dice 0.827, +0.003), smooth muscle (0.690, +0.016), RBC (0.803). Gains modest compared to classification tasks.

**MI-SimpleShot (prompt-based slide classification)**:
- Uses ROI-level class prototypes (averaged features) instead of textual prompts for topK pooling.
- With ≤4 slides/class, MI-SimpleShot outperforms trained ABMIL.
- NSCLC subtyping: 90.2% balanced accuracy (using all training slides), +5.7% over next-best.

## Reported Insights

- Data diversity (20 organs, non-cancer tissue from GTEx) is more valuable for generalization than training duration. UNI sees 4–13× fewer images than competitors yet outperforms.
- TCGA data contamination is a real concern: models pretrained on TCGA show inflated in-domain performance that drops substantially on external test sets. Authors recommend separating pretraining and evaluation data sources.
- Plain ViT architectures are competitive with hierarchical backbones (Swin, ResNet) even on dense prediction, though segmentation gains are smaller.
- ViT-Giant was considered but deemed out of scope due to compute requirements.
- UNI is unimodal (vision-only); multimodal extension explored in concurrent CONCH work (ref 27).

## References Worth Chasing

- DINOv2: Learning Robust Visual Features without Supervision (arXiv:2304.07193) — core SSL algorithm used
- Towards a Visual-Language Foundation Model for Computational Pathology (arXiv:2307.12914) — concurrent CONCH work by same group, multimodal extension
- A Cookbook of Self-Supervised Learning (arXiv:2304.12210) — comprehensive SSL survey used as methodological guide
- Emerging Properties in Self-Supervised Vision Transformers [DINO] (ICCV 2021) — predecessor of DINOv2, student-teacher framework
- iBOT: Image BERT Pre-Training with Online Tokenizer (ICLR 2022) — masked image modeling component of DINOv2
- Transformer-Based Unsupervised Contrastive Learning for Histopathological Image Classification [CTransPath] (Medical Image Analysis 2022) — key baseline, Swin-T/14 pretrained on TCGA+PAIP
- Robust and Data-Efficient Generalization of Self-Supervised Machine Learning for Diagnostic Imaging [REMEDIS] (Nature BME 2023) — key baseline, ResNet-152×2 pretrained on TCGA via SimCLR
- Scaling Vision Transformers to Gigapixel Images via Hierarchical Self-Supervised Learning [HIPT] (CVPR 2022) — predecessor work from same group, hierarchical ViT for WSIs
- Visual Language Pretrained Multiple Instance Zero-Shot Transfer for Histopathology Images [MI-Zero] (CVPR 2023) — text-prompted zero-shot slide classification, precursor to CONCH
- Data Efficient and Weakly Supervised Computational Pathology on Whole Slide Images [CLAM] (Nature BME 2020) — MIL framework used for all slide-level evaluations
- An Image Is Worth 16x16 Words: Transformers for Image Recognition at Scale [ViT] (ICLR 2021) — ViT-L architecture origin
- Giga-SSL: Self-Supervised Learning for Gigapixel Images (CVPR 2023) — alternative SSL approach for WSIs at full resolution
- On the Opportunities and Risks of Foundation Models (arXiv:2108.07258) — foundation model framing
- Self-Supervised Attention-Based Deep Learning for Pan-Cancer Mutation Prediction from Histopathology (NPJ Precision Oncology 2023) — downstream application of SSL encoders

## Notes / Open Questions

- Parameter count is never stated explicitly in the paper; ≈303M inferred from ViT-L/16 standard configuration. Confirm against model checkpoint.
- The paper was posted in 2023 but published in Nature Medicine 2024 — the published version may contain additional data (e.g., ViT-Giant experiments, updated benchmarks).
- No FLOPs or wall-clock training time reported. 32×A100 for 125K iterations at batch 3072 is substantial but unquantified.
- `training_tokens` field stores total unique patches (100.13M), not total images seen during training (384M). The two differ because each patch is seen ~3.8 epochs on average.
- Mass-100K is not public (in-house MGH/BWH data); model weights released on Hugging Face but data cannot be reproduced.
- Modality is imaging-pathology only; the arxiv frontmatter previously listed scrna but the paper contains no scRNA-seq data or experiments.
- ViT-Giant is explicitly mentioned as a desirable but compute-limited future direction.
- How does UNI compare to later models (Virchow, Prov-GigaPath, CONCH) that were published after this preprint?

## Verification (Rev 3)

Each cited claim in `insights.md` is checked against the source paper.

| # | insights.md location | Claim | Verdict | Detail |
|---|---|---|---|---|
| 1 | L43 | "UNI 8-shot matches competitors at 128-shot (16× label efficiency)" under the heading "Lightweight fine-tuning unlocks large frozen models" | **partial** | The 8-shot / 128-shot / 16× figure is accurate (paper §Few-shot ROI classification: "UNI consistently exceeds the 128-shot and 256-shot performance of the next best-performing model on many tasks (16–32× label efficiency)"). However, UNI's few-shot evaluation uses SimpleShot (frozen features + nearest centroid), which is not fine-tuning. Categorising this under "lightweight fine-tuning" is a framing error. |
| 2 | L242 | "UNI trained on 100 M patches from 100 K WSIs, with 8-shot UNI matching 128-shot competitors — a 16× label-efficiency gain attributed to pretraining data scale" | **partial** | Training data size (100 M patches, 100 K WSIs) and the 16× figure are supported. The attribution solely to "pretraining data scale" oversimplifies: the paper attributes the advantage to both data scale/diversity AND the DINOv2 SSL method's representation quality. The 16× claim comes from ROI-level SimpleShot, not the data-scaling ablation (which reports OT-43/OT-108 accuracy gains across Mass-1K/22K/100K). |
| 3 | L309 | "UNI demonstrates clear data-scaling: 100 M patches from 100 K slides produce an encoder that needs only 8 labelled examples to match competitors using 128, yielding 16× label efficiency" | **partial** | Conflates two distinct experiments. Data-scaling laws are demonstrated via Mass-1K → Mass-22K → Mass-100K on OT-43/OT-108 (§Pretraining scaling laws). The 16× label efficiency is from SimpleShot ROI few-shot evaluation (§Few-shot ROI classification), comparing UNI against different models, not across data scales. Both findings are individually supported but the sentence implies one causes the other directly. |
| 4 | L362 | "UNI acknowledges a TCGA contamination concern — many pathology benchmarks use TCGA data, which was also used for pretraining" | **partial** | UNI itself deliberately excludes TCGA/CPTAC/PAIP from pretraining to enable unbiased evaluation. The paper highlights TCGA contamination as a problem in competing models (CTransPath, REMEDIS) and shows their performance drops on external test sets (e.g. REMEDIS RCC: 97.3% TCGA → 79.0% CPTAC). The phrasing "which was also used for pretraining" is ambiguous — it was used for competitors' pretraining, not UNI's. |
| 5 | L530–531 | "UNI (ViT-L/16, 303 M, DINOv2) trained on 100 M patches from 100 K WSIs. Data-scaling laws: 8-shot UNI > 128-shot competitors (16× label efficiency). TCGA contamination concern." | **partial** | Architecture, SSL method, and training data are supported. 303 M is inferred from standard ViT-L/16 (not stated explicitly in the paper). Same conflation of data-scaling with 16× few-shot as claim #3. Same TCGA contamination nuance as claim #4. |
| 6 | L591 | "UNI acknowledges TCGA contamination" | **supported** | The paper devotes a full subsection to analysing TCGA data contamination in CPath (§Weakly-supervised slide classification). Phrasing is accurate at this level of brevity. |

### Summary

All six citations refer to genuine findings in the paper. The core quantitative claims (100 M patches, 100 K WSIs, 16–32× label efficiency, TCGA contamination analysis) are well-supported. Two recurring issues reduce several verdicts to **partial**:

1. **Conflation of data-scaling and few-shot results.** The paper's data-scaling ablation (Mass-1K/22K/100K on OT-43/108) and the 16× few-shot label efficiency (SimpleShot ROI evaluation) are independent experiments; insights sometimes merge them into a single causal claim.
2. **TCGA contamination framing.** UNI is the model that *avoids* TCGA contamination by design; it identifies the problem in competitors. Several insights are ambiguous about which model is contaminated.

## Ablations (Rev 4)

| Variable | Settings | Metric / dataset | Result | Conclusion |
|---|---|---|---|---|
| Pretraining data scale | Mass-1K (1M patches / 1,404 WSIs); Mass-22K (16M / 21,444); Mass-100K (100M / 100,426) — same ViT-L/16 + DINOv2 | Top-1 acc on OT-43 (43-class cancer) and OT-108 (108-class OncoTree), in-house BWH WSIs | OT-43: +4.2% (1K→22K) and +3.6% (22K→100K) top-1 (both p<0.05); monotonic gains on OT-108 too | SSL in pathology benefits from data scale up to ≥100M patches / 100K WSIs; no saturation observed at 100K-slide scale |
| Pretrained encoder (controlled comparison) | UNI (ViT-L/16, DINOv2, Mass-100K) vs ResNet-50 (IN-1K) vs CTransPath (Swin, TCGA+PAIP) vs REMEDIS (ResNet-152, TCGA) | OT-43 top-5 / AUROC; 15 slide-tasks bal-acc; 10 ROI linear-probe; 8 SegPath dice | OT-43: 93.8% top-5, 0.976 AUROC (+6.3% / +0.022 over REMEDIS); ROI linear probe avg: +19.9% / +9.5% / +7.7% over RN50/CTransPath/REMEDIS; SegPath epithelial/SM/RBC dice 0.827/0.690/0.803 (+0.003/+0.016 over REMEDIS) | DINOv2 + ViT-L + 100K-slide diverse pretraining beats both ImageNet-supervised CNNs and prior pathology SSL (CTransPath, REMEDIS) despite UNI seeing 4–13× fewer total images |
| Few-shot label efficiency (slide MIL) | K ∈ {1,2,4,8,16,32} slides/class, ABMIL on frozen features; 5 runs; UNI vs RN50/CTransPath/REMEDIS | Bal-acc on 15 slide tasks (CAMELYON16, PANDA, EBRAINS, NSCLC, RCC, …) | UNI 4-shot ≥ next-best 32-shot on most tasks (≥8× label-eff); on EBRAINS UNI 4-shot ≈ REMEDIS 32-shot; 1-shot UNI sometimes worse than baselines (e.g. BRACS, glioma IDH1) | Strong SSL features give large label-efficiency wins from K≥4; 1-shot remains noisy across all encoders |
| Few-shot label efficiency (ROI SimpleShot) | K ∈ {1,2,…,256}/class as nearest-prototype; 1000 runs | Bal-acc on PRAD (AGGC), UniToPatho, pan-cancer TCGA, etc. | UNI 8-shot ≥ next-best 128- or 256-shot (16–32× label-eff); UNI std 0.32–1.59% at 256-shot; lowest UNI 32-shot run > best CTransPath run on PRAD | Class-prototype (parameter-free) probes work extremely well with high-quality SSL features; representation quality dominates over classifier complexity |
| Image resolution / magnification sensitivity | Resize-and-crop ROIs to 224², 448², 896², 1344²/1792² (BRCA-BACH; CRC polyp UniToPatho), linear and KNN probing | Bal-acc, BRCA subtyping (BACH); CRC polyp (UniToPatho) | At 224²: UNI > CTransPath by +5.0% (linear) / +15.0% (KNN) on BACH; at 1344²: +25.0% linear (p<0.05). Margins widen with resolution | DINOv2-style high-res pretraining yields resolution-agnostic features; advantage of UNI grows at native histology magnifications |
| Probing protocol | Linear probe vs KNN probe on frozen features | 10 ROI tasks, all encoders | UNI leads under both; gap larger under KNN, indicating cleaner embedding geometry | UNI's features are linearly separable AND metric-meaningful — important for retrieval / prototyping use cases |
| In-domain vs out-of-domain eval (data contamination) | TCGA-internal test fold vs external cohort (CPTAC/DHMC/EBRAINS); UNI vs CTransPath vs REMEDIS | Bal-acc on NSCLC, RCC, glioma IDH1, glioma histomolecular | REMEDIS RCC: 97.3% (TCGA) → 79.0% (CPTAC); UNI: 94.7% → 96.3%. Glioma IDH1: CTransPath 89.1→83.6, REMEDIS 81.9→79.2, UNI 80.8→85.6 | TCGA-pretrained encoders are optimistically biased on TCGA-derived benchmarks; out-of-domain generalization is the right metric for pathology FMs |
| Slide classifier head | MI-SimpleShot (prototype, 0 trainable params) vs ABMIL (trainable MIL); K ∈ {1,2,4,8,16,32} slides/class | Bal-acc on NSCLC and RCC subtyping (TCGA→CPTAC) | MI-SimpleShot > ABMIL at K=1,2,4; comparable at higher K. UNI MI-SimpleShot has 8× label-efficiency over other encoders' MI-SimpleShot | In very-low-label regimes, parameter-free prototype classifiers outperform trainable MIL — over-parameterised heads overfit when shots are scarce |

**Design-choice take-aways from this paper's ablations:**
- **Scale of diverse pretraining slides matters more than total image count**: Mass-100K (100K WSIs across 20 organs) beats CTransPath/REMEDIS despite those models seeing 4–13× more total images — slide diversity > raw image volume.
- **DINOv2 + ViT-L is the right recipe for pathology SSL** at this scale — same architecture, same data, but DINOv2 self-distillation + masked-image-modeling yields large gains over MoCo/SimCLR-style baselines.
- **Avoid TCGA in pretraining if you want to evaluate on TCGA-derived benchmarks**: data contamination inflates in-domain numbers by 10–18 pts (e.g. REMEDIS RCC 97→79 across domain shift), so OOD eval is mandatory.
- **Frozen + prototype/KNN probes are sufficient** for strong few-shot performance — UNI's 8-shot SimpleShot beats competitors' 128/256-shot, suggesting the encoder, not the head, drives label efficiency.
- **Pretrain at multiple resolutions** (DINOv2's high-res stage) to get resolution-agnostic features that work from 224² up to 1344²+ — pathology tasks are magnification-sensitive.
- **Plain ViT-L still trails hierarchical backbones on dense prediction** (segmentation gains are smaller than classification gains) — future bio-FMs may want hierarchical / adapter designs for segmentation.

