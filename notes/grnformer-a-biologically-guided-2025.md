---
id: grnformer-a-biologically-guided-2025
title: 'GRNFormer: A Biologically-Guided Framework for Integrating Gene Regulatory
  Networks into RNA Foundation Models'
authors:
- Mufan Qiu
- Xinyu Hu
- Fengwei Zhan
- Sukwon Yun
- Jie Peng
- Ruichen Zhang
- Bhavya Kailkhura
- Jiekun Yang
- Tianlong Chen
year: 2025
venue: null
arxiv: '2503.01682'
doi: null
url: https://arxiv.org/abs/2503.01682v1
pdf_path: papers/grnformer-a-biologically-guided-2025.pdf
md_path: papers/md/grnformer-a-biologically-guided-2025.md
modalities:
- scrna
- epigenome
- interactome
status: extracted
evidence_quality: medium
tags:
- gene-regulatory-network
- adapter
- graph-neural-network
- cross-attention
- multi-omics-integration
- drug-response
- perturbation-prediction
parameters: null
training_tokens: null
training_compute: 8×A100 GPUs (full pretraining on SEA-AD)
references_chased: false
added_at: '2026-04-22T19:36:49+00:00'
updated_at: '2026-04-22T20:20:32+00:00'
is_fm: false
fm_classification_reason: Adapter framework injecting GRNs into existing scRNA FMs;
  not a standalone FM.
---

## TL;DR

GRNFormer is a **framework/adapter** (not a standalone FM) that injects multi-scale Gene Regulatory Networks (GRNs), inferred from paired scATAC-seq + scRNA-seq via SCENIC+, into existing RNA foundation models (scGPT, scFoundation, scPaLM). It uses a GraphSAGE encoder for GRN structure + cross-attention fusion with expression embeddings, plus a biologically-informed co-expression edge perturbation strategy. Pretrained on SEA-AD (113K cells, 18,984 genes). Gains: +3.6% PCC drug response, +9.6% AUC single-cell drug classification, +1.1% avg PCC_delta gene perturbation over baselines.

## Model

- **Type**: Framework/adapter on top of existing scRNA FMs; not a new foundation model per se.
- **Backbone FMs supported**: scGPT (decoder-only), scFoundation (encoder-decoder, 768 hidden), scPaLM (encoder-decoder, pathway-aware).
- **GRN encoder**: GraphSAGE with fixed-size neighborhood sampling. Processes cell-specific and cell-type-specific GRNs separately, combines via element-wise sum → `h_struct`.
- **Fusion**: Multi-head cross-attention layer replaces final transformer layer. Query = expression embedding from backbone FM, Key/Value = structural embedding from GNN. Produces `h_fusion`.
- **Final output**: `h_combined = h_expr + β · h_fusion`, fed to decoder.
- **Edge perturbation**: Replaces α=20% of GRN edges with co-expression links (genes co-expressed in same cell, eq. 3) rather than random edges.
- **Cross-modality inference**: For single-modality scRNA-seq downstream data, uses reference mapping (nearest-neighbor in pretrained FM embedding space) to assign precomputed GRNs from paired multi-omic reference.

## Data

- **Pretraining**: SEA-AD (Seattle Alzheimer's Disease Brain Cell Atlas) multiome — 113,209 cells from 28 donors, paired scRNA-seq (18,984 protein-coding genes) + scATAC-seq (chromatin accessibility).
- **GRN construction**: SCENIC+ pipeline → eRegulons (TF–enhancer–target gene triplets). Uses pycisTopic for candidate enhancers, pycisTarget for TF-motif enrichment (32,765 motifs from 29 collections, NES>3.0, FDR<0.1), GRNBoost2 for regression importance. Enhancer-gene links within ±150kb, Pearson |r|>0.03.
- **Single-cell GRNs**: AUCell activity scoring → Gaussian mixture thresholding (bimodal: intersection; skewed: µ+2σ).
- **Downstream benchmarks**:
  - Gene perturbation: Adamson (68,603 cells, 5,060 genes, 87 perturbations), Dixit (44,735 cells, 5,012 genes), Norman (91,205 cells, 5,045 genes, 131 gene pairs + 105 singles).
  - Drug response: CCLE (947 cell lines, 24 drugs, 1,651 genes), GDSC (969 cell lines, 297 compounds, ~22K genes).
  - Single-cell drug classification: 4 drugs (Sorafenib, NVP-TAE684, PLX4720, Etoposide) per scFoundation protocol.

## Training Recipe

- **Pretraining objective**: Masked language modeling (masked gene expression reconstruction), same as backbone FM's native objective.
- **scGPT/scPaLM backbone**: Full pretraining from scratch on SEA-AD multiome data.
- **scFoundation backbone**: Continued pretraining from official checkpoint (plug-and-play validation).
- **Hyperparameters**: Backbone-specific (optimizer, LR, batch size from original implementations). Not further specified.
- **Hardware**: 8×A100 GPUs.
- **Fine-tuning**: scGPT allows full parameter updates; scFoundation freezes most layers due to GPU memory constraints (this likely explains its lower perturbation prediction performance).

## Key Ablations & Design Choices

**GRN type ablation** (backbone: scGPT, drug response PCC):
| GRN variant | PCC |
|---|---|
| No GRN | 0.875 ± 0.010 |
| Random GRN | 0.892 ± 0.006 |
| Cell-type specific | 0.901 ± 0.003 |
| Cell-specific | 0.902 ± 0.002 |
| **Hybrid (both)** | **0.906 ± 0.002** |

→ Even random GRNs help (+1.7%), but biologically grounded GRNs are better. Hybrid combining both scales is best.

**Edge perturbation** (backbone: scPaLM):
| Strategy | Drug PCC | Drug Class. AUC |
|---|---|---|
| No augmentation | 0.867 ± 0.006 | 0.545 ± 0.118 |
| Random perturbation | 0.877 ± 0.002 | 0.558 ± 0.113 |
| **Co-expression guided** | **0.884 ± 0.004** | **0.561 ± 0.105** |

→ Random perturbation can degrade performance; co-expression guided is +1.6% over baseline in drug response.

**GNN architecture** (backbone: scFoundation):
| GNN | Drug PCC | Drug Class. AUC |
|---|---|---|
| GCN | 0.881 ± 0.007 | 0.675 ± 0.014 |
| GIN | 0.876 ± 0.006 | 0.623 ± 0.138 |
| **GraphSAGE** | **0.888 ± 0.002** | **0.743 ± 0.155** |

→ GraphSAGE best due to fixed-size neighbor sampling handling degree imbalance (TF avg degree 81.3 vs other genes avg degree 1.3).

**Attention analysis**: TF enrichment ratio ρ = 2.011 — model attends ~2× more to TF nodes than non-TF nodes, aligning with biological regulatory importance.

**Key result summary across tasks**:
| Task | Backbone | Baseline | +GRN | Δ |
|---|---|---|---|---|
| Gene perturb. (avg PCC_delta) | scGPT | 0.381 | 0.393 | +1.2% |
| Gene perturb. (avg PCC_delta) | scFoundation | 0.326 | 0.337 | +1.1% |
| Drug response (PCC) | scGPT | 0.875 | 0.906 | +3.1% |
| Drug class. (avg AUC) | scGPT | 0.459 | 0.581 | +12.2% |
| Drug class. (avg AUC) | scFoundation | 0.712 | 0.743 | +3.1% |

## Reported Insights

- ~40% of genes lack reliable regulatory links in GRNs → topological imbalance is a first-class problem.
- Naive fusion (concat/add) of GRN embeddings with expression features amplifies information asymmetry; cross-attention is needed.
- Co-expression edges are biologically plausible augmentation since co-expressed genes in the same cell likely share functional relationships.
- scFoundation's frozen layers during fine-tuning limit adaptability to perturbation patterns vs. scGPT's full fine-tuning.
- Reference mapping enables GRN integration even for single-modality downstream datasets.
- The framework is architecture-agnostic (validated on 3 backbone FMs).

## References Worth Chasing

1. **scGPT** — Cui et al., 2024. Nature Methods. Generative pretraining FM for scRNA-seq.
2. **scFoundation** — Hao et al., 2024. Nature Methods. Large-scale FM with RDA pretraining on 50M+ cells.
3. **scPaLM** — Chen et al., 2024. ICML workshop. Pathway-aware single-cell language model.
4. **Geneformer** — Theodoris et al., 2023. Nature. Transfer learning FM for network biology.
5. **SCENIC+** — Bravo González-Blas et al., 2023. Nature Methods. Multi-omic eRegulon inference pipeline.
6. **SCENIC** — Aibar et al., 2017. Nature Methods. Single-cell regulatory network inference.
7. **GEARS** — Roohani et al., 2022. Multi-gene perturbation prediction.
8. **GRNBoost2** — Moerman et al., 2019. Bioinformatics. Efficient GRN inference.
9. **GET** — Fu et al., 2025. Nature. Foundation model of transcription across human cell types (pseudobulk chromatin profiles).
10. **DeepCDR** — Liu et al., 2020. Bioinformatics. Hybrid GCN for cancer drug response prediction.
11. **SCAD** — Zheng et al., 2023. Advanced Science. Single-cell drug response annotation from bulk RNA-seq.
12. **scCLIP** — Xiong et al., 2023. Multi-modal single-cell contrastive learning.
13. **GraphSAGE** — Hamilton et al., 2017. NeurIPS. Inductive representation learning on large graphs.
14. **Yuan & Duren, 2024** — Nature Biotechnology. GRN inference from single-cell multiome using atlas-scale external data.

## Notes / Open Questions

- **Not a standalone FM**: GRNFormer is an adapter/plug-in framework, not a new foundation model. Its value is in the GRN integration methodology rather than new pretraining at scale.
- **Limited pretraining data**: Only 113K cells from one brain atlas (SEA-AD). Unclear how GRN quality/transferability scales to other tissues/diseases.
- **No parameter counts reported** for the adapter components (GraphSAGE encoder, cross-attention layer).
- **Variance in drug classification** is high (e.g., scFoundation+GRN AUC 0.743 ± 0.155), suggesting instability across drugs.
- **Reference mapping assumption**: Quality of GRN transfer to single-modality downstream data depends on embedding-space neighbor quality — not validated rigorously.
- **Dependency on SCENIC+/motif databases**: Performance ceiling tied to completeness of existing motif collections (32,765 motifs). Under-studied TFs/cell types may not benefit.
- **Evidence quality rated medium**: Single pretraining dataset, no external replication, modest gains on perturbation prediction (+1.1%), high variance on some tasks. Ablations are informative but all on same data splits.
