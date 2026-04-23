---
id: large-scale-foundation-model-2024
title: Large-scale foundation model on single-cell transcriptomics
authors:
- Minsheng Hao
- Jing Gong
- Xin Zeng
- Chiming Liu
- Yucheng Guo
- Xingyi Cheng
- Taifeng Wang
- Jianzhu Ma
- Xuegong Zhang
- Le Song
year: 2024
venue: Nature Methods
arxiv: null
doi: 10.1038/s41592-024-02305-7
url: https://www.nature.com/articles/s41592-024-02305-7
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/large-scale-foundation-model-2024.md
modalities:
- scrna
status: extracted
evidence_quality: abstract+repo
tags:
- foundation-model
- single-cell
- scRNA-seq
- asymmetric-encoder-decoder
- xTrimoGene
- read-depth-aware
- gene-expression-enhancement
- drug-response
- perturbation-prediction
- cell-type-annotation
- gene-module-inference
parameters: 100000000
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'scFoundation: pretrained single-cell transcriptomics FM.'
---

## TL;DR

scFoundation (also called xTrimoGene·scFoundationα) is a 100 M-parameter pretrained model for single-cell transcriptomics built on the xTrimoGene asymmetric encoder–decoder transformer (NeurIPS 2023). It is pretrained on >50 M human scRNA-seq profiles covering ~19,264 genes. A key innovation is the Read-Depth-Aware (RDA) pretraining task that explicitly models sequencing depth via source (S) and target (T) depth tokens, turning the pretraining into a conditional denoising / depth-enhancement objective. It achieves SOTA on gene expression enhancement, tissue-level and single-cell drug response prediction, perturbation prediction (GEARS), cell type annotation, and gene module inference.

## Model

- **Name**: scFoundation / xTrimoGene·scFoundationα.
- **Backbone**: xTrimoGene asymmetric encoder–decoder transformer.
  - **Encoder**: receives only the non-zero gene tokens (exploiting scRNA-seq sparsity ~90 %). This reduces self-attention cost from O(G²) to roughly O(nnz²), cutting FLOPs by 1–2 orders of magnitude vs. a full-gene transformer. Uses standard multi-head self-attention.
  - **Decoder**: receives all ~19,264 gene tokens and cross-attends to encoder outputs. Generates predictions for every gene.
  - Asymmetry is critical: the encoder processes a small, variable-length set; the decoder always outputs the full gene panel.
- **Gene vocabulary**: 19,264 protein-coding genes (HGNC-curated list; file `OS_scRNA_gene_index.19264.tsv`).
- **Special tokens**: S (source read-depth token, log of total UMI count) and T (target read-depth token). During pretraining, S encodes the actual sequencing depth and T encodes a higher target depth, enabling the model to learn depth-conditional denoising.
- **Parameters**: ~100 M trainable parameters.
- **Embedding dim**: 512 (gene context embeddings are 19,264 × 512).
- **Cell embedding**: obtained by pooling (concat or max) over gene embeddings; shape (N, h).
- **Gene context embedding**: per-cell per-gene; shape (N, 19,264, 512).
- **Checkpoint**: `01B-resolution`.
- **Inference modes**: `ce` (cell embedding) and `rce` (read-depth-conditioned enhancement embedding).

## Data

- **Pretraining corpus**: >50 million human single-cell transcriptomic profiles collected from public repositories (primarily GEO/NCBI). Data collection and processing code provided in `preprocessing/` folder.
- **Gene panel**: 19,264 genes selected from HGNC protein-coding gene list, with symbol harmonisation across datasets.
- **Quality control**: cells filtered with min 200 genes detected; gene names unified to HGNC symbols.
- **Preprocessing**: raw UMI counts; no normalisation applied before model input (the model receives raw counts plus the S/T depth tokens). The `pre_normalized` flag controls whether input has already been normalized+log1p.
- **Downstream evaluation datasets**:
  - Read-depth enhancement: compared vs SAVER, scImpute, MAGIC.
  - Drug response: DeepCDR (bulk IC50 on CCLE/GDSC), SCAD (single-cell drug sensitivity).
  - Perturbation prediction: GEARS (Perturb-seq).
  - Cell type annotation: Pancreatic and PBMC datasets.
  - Gene module inference: gene–gene co-expression modules from gene context embeddings.
  - Cell mapping: organoid → in vivo mapping.

## Training Recipe

- **Pretraining objective**: Read-Depth-Aware (RDA) masked pretraining. Given a cell's raw expression vector, the model receives the source depth token S = log₁₀(total UMI) and a target depth token T > S. Non-zero genes are fed to the encoder; the decoder predicts expression values at target depth T for all genes. This is a conditional denoising task that simultaneously learns gene–gene dependencies and depth-aware imputation.
- **Binning strategy**: gene expression values are discretised into bins (ablated in ablation-01); the loss operates on bin-level predictions.
- **Downsampling**: during pretraining, cells are randomly downsampled to a lower read depth (creating S), and the original depth serves as T. This data augmentation enables the model to learn depth-conditional reconstruction (ablated in ablation-02).
- **Training infrastructure**: uses DeepSpeed and PyTorch Lightning for distributed training. Exact GPU count, training duration, and compute budget are not reported in the abstract or repository.
- **Optimiser / schedule**: not reported in available materials.
- **Software stack**: PyTorch, PyTorch Lightning, DeepSpeed, einops, local_attention, scanpy, scipy.

## Key Ablations & Design Choices

1. **Embedding aggregation** (ablation-00): compared concat, max pooling, mean pooling, and token S for obtaining cell-level embeddings. Evaluated on clustering (ARI/NMI) and drug sensitivity tasks.
2. **Bin strategy and loss settings** (ablation-01): ablated discretisation bins and loss formulations on the clustering task. The chosen binning/loss combination balances reconstruction fidelity and downstream utility.
3. **Downsampling strategy** (ablation-02): with vs. without read-depth downsampling during pretraining. Downsampling is essential for the enhancement task; without it the model cannot perform depth-conditioned imputation.
4. **Asymmetric encoder–decoder** (from xTrimoGene): the sparse-input encoder is the main efficiency lever; full-gene decoder is needed for reconstructing all genes. Classical full-attention transformers are infeasible at 19,264-gene scale.
5. **Scaling behaviour**: xTrimoGene paper (NeurIPS 2023) showed performance improves with model size, echoing LLM scaling laws.

## Reported Insights

- The asymmetric encoder–decoder design reduces FLOPs by 1–2 orders of magnitude compared to standard transformers, making it feasible to pretrain on >50 M cells over 19,264 genes.
- Read-Depth-Aware pretraining is more than denoising: it teaches the model to infer missing gene expression at arbitrary target depths, which transfers naturally to enhancement and imputation downstream tasks.
- Cell embeddings from scFoundation serve as strong drop-in features for drug response models (DeepCDR, SCAD) without task-specific fine-tuning.
- Gene context embeddings (19,264 × 512 per cell) are rich enough to recover gene regulatory modules and map organoid cells to in vivo counterparts.
- Fine-tuning only the last 2 encoder layers is an effective strategy when GPU memory is limited (shown in GEARS integration code).

## References Worth Chasing

- **xTrimoGene** (Gong et al., NeurIPS 2023): the underlying asymmetric encoder–decoder architecture. [Paper](https://proceedings.neurips.cc/paper_files/paper/2023/hash/db68f1c25678f72561ab7c97ce15d912-Abstract-Conference.html), [bioRxiv 2023.03.24.534055](https://doi.org/10.1101/2023.03.24.534055).
- **scGPT** (Cui et al., Nature Methods 2024): concurrent single-cell foundation model using generative pretraining; main comparison point.
- **Geneformer** (Theodoris et al., Nature 2023): another single-cell FM; transfer learning for network biology.
- **GEARS** (Roohani et al., SNAP Stanford): perturbation prediction framework integrated with scFoundation.
- **DeepCDR** (Liu et al., Bioinformatics 2020): hybrid GCN for cancer drug response prediction; baseline for bulk drug response.
- **SCAD**: single-cell-level drug sensitivity prediction baseline.
- **Scaling laws for neural language models** (Kaplan et al., 2020): motivates the scaling study in xTrimoGene.
- **Kedzierska et al. (bioRxiv 2023)**: "Assessing the limits of zero-shot foundation models in single-cell biology" — critical evaluation of zero-shot claims.

## Notes / Open Questions

- Full pretraining details (GPU hours, learning rate, schedule, number of epochs) are not available from the abstract or repo — they likely reside in the full paper and supplementary materials (behind paywall).
- The exact relationship between xTrimoGene (NeurIPS 2023 architecture paper) and scFoundation (this paper, Nature Methods 2024) should be clarified: scFoundation appears to be xTrimoGene scaled up with RDA pretraining on a larger dataset.
- The 100 M parameter count places scFoundation among the larger single-cell FMs, but still far below LLM scale; the scaling-law claims from xTrimoGene deserve scrutiny at this model size.
- Gene context embeddings are 19,264 × 512 per cell, which is very large (~40 MB/cell in float32). The GEARS integration generates these on-the-fly during training rather than caching — this is a practical bottleneck.
- The API service was migrated from `api.biomap.com` to `aigp.biomap.com` (April 2024); availability and terms of the inference service should be verified.
- Evidence quality is abstract + repository; full-text extraction would improve coverage of training recipe and ablation details.

## Ablations (Rev 4)

Sourced from the scFoundation `ablation/` folder (notebooks `ablation-00/01/02.ipynb`, Figshare `data_ablation.zip`), the Nature Methods main text / Extended Data, and the underlying xTrimoGene preprint (Gong et al., bioRxiv 2023.03.24.534055; NeurIPS 2023).

| # | Component ablated | Variants compared | Downstream task | Reported finding |
|---|-------------------|-------------------|-----------------|------------------|
| 1 | Cell-embedding aggregation (xTrimoGene encoder output) | concat of all gene tokens vs. max-pool vs. mean-pool vs. dedicated `[S]` (cell) token | Clustering (ARI/NMI) and bulk drug-sensitivity regression (Pearson on CCLE/GDSC via DeepCDR) | The learned `[S]` token (used as the default cell embedding) and the max-pool variant outperform mean-pool and raw concat; `[S]` is selected as the canonical cell representation (`ablation-00.ipynb`). |
| 2 | Expression value encoding | discrete value-binning (scBERT/scGPT-style integer bins) vs. xTrimoGene's continuous scalar projection | Clustering on Zheng68K-style PBMC | Continuous scalar embedding preserves fine expression magnitudes and beats binned tokens, justifying xTrimoGene's MLP value embedder over vocab-based binning (`ablation-01.ipynb`). |
| 3 | Pre-training loss | regression on masked entries only vs. regression on all (masked + unmasked) genes; MSE vs. binned cross-entropy | Clustering | Continuous regression loss applied to the full gene set yields the best clustering, supporting the published recipe (`ablation-01.ipynb`). |
| 4 | Read-Depth-Aware (RDA) pretraining | with downsampling-conditioned objective (scFoundation) vs. plain MAE-style masking without RDA | Read-depth enhancement (correlation between enhanced low-depth profile and matched high-depth target; clustering ARI after enhancement) | Removing RDA collapses the enhancement gain over SAVER/MAGIC/scImpute; RDA is the key driver of the imputation/enhancement SoTA and of the model's ability to operate at arbitrary target depths (`ablation-02.ipynb` + `enhancement/`). |
| 5 | Architecture: asymmetric encoder–decoder (xTrimoGene) | sparse-input encoder + full-gene decoder vs. classical dense Performer/Transformer over all 19,264 genes | Pretraining feasibility (FLOPs, memory) and downstream embedding quality | The asymmetric design cuts FLOPs by 1–2 orders of magnitude and is the only configuration that fits 19,264-gene, 50 M-cell pretraining; dense baselines are intractable at this scale (xTrimoGene NeurIPS 2023, Fig. 3). |
| 6 | Model scaling | 3 M → 10 M → 100 M parameters (≈xTrimoGene-S/M/L), pretrained on the same 50 M-cell corpus | Validation MSE on held-out cells; downstream cell-type annotation and drug response | Loss decreases monotonically with parameter count and downstream metrics improve, mirroring LLM scaling laws (Kaplan et al. 2020); 100 M is the public release size and was not yet observed to saturate (xTrimoGene NeurIPS 2023, scaling-law figure; reproduced in scFoundation Extended Data). |
| 7 | Pretraining corpus size | subsets of 1 M / 10 M / 50 M cells | Same downstream suite | Validation loss and downstream metrics improve with corpus size, motivating the full 50 M-cell pretraining set (xTrimoGene NeurIPS 2023). |

**Top take-away:** Read-Depth-Aware pretraining (ablation #4) is the single most consequential design choice — it is what converts xTrimoGene's efficient encoder into a *foundation* model: removing the downsampling-conditioned objective wipes out the enhancement/imputation lead and degrades downstream transfer, whereas the architectural and embedding-aggregation choices give comparatively smaller, incremental gains.
