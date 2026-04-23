---
id: transformer-based-single-cell-2024
title: 'Transformer-based Single-Cell Language Model: A Survey'
authors:
- Wei Lan
- Guohang He
- Mingyang Liu
- Qingfeng Chen
- Junyue Cao
- Wei Peng
year: 2024
venue: null
arxiv: '2407.13205'
doi: null
url: https://arxiv.org/abs/2407.13205v1
pdf_path: papers/transformer-based-single-cell-2024.pdf
md_path: papers/md/transformer-based-single-cell-2024.md
modalities:
- scrna
- single-cell-multiomics
- epigenome
status: extracted
evidence_quality: low
tags:
- survey
- transformer
- single-cell
- foundation-model
- review
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:11+00:00'
updated_at: '2026-04-22T20:26:52+00:00'
---

## TL;DR

Survey of transformer-based language models for single-cell data analysis. Categorizes models into single-cell language models (transCluster, scTransSort, CIForm, STGRNS, T-GEM, PROTRAIT, TransformerST, scMVP, scMoFormer, DeepMAPS, MarsGT) and single-cell large language models (scBERT, scFoundation, scGPT, CellPLM, tGPT, Cell2Sentence). Reviews downstream tasks: batch correction, cell clustering, cell type annotation, gene regulatory network inference, and perturbation response. Not a primary contribution — purely a literature review.

## Model

This is a **survey paper** and does not propose a new model. It reviews two categories of transformer-based single-cell models:

1. **Single-cell language models** (task-specific, not pre-trained at scale):
   - *Transcriptomics*: transCluster, scTransSort, CIForm, STGRNS, T-GEM
   - *Spatial/epigenomics*: PROTRAIT (scATAC-seq), TransformerST (spatial transcriptomics)
   - *Multi-omics*: scMVP (scRNA+scATAC), scMoFormer (scRNA+proteomics), DeepMAPS (heterogeneous graph transformer), MarsGT (extends DeepMAPS)

2. **Single-cell large language models** (pre-trained at scale):
   - scBERT: BERT-based, uses Performer for long sequences (>16k genes), gene2vec embeddings, ~first scRNA pre-trained model
   - scFoundation: ~100M parameters, asymmetric encoder-decoder, read-depth-aware pre-training
   - scGPT: GPT-inspired, generative pre-training on >33M cells, Flash-Attention, first SC foundation model with generative pre-training
   - CellPLM: first to consider cell-cell relationships, uses Flowformer variant, incorporates spatial transcriptomics
   - tGPT: autoregressive, uses gene expression ranking instead of raw values, 8 transformer layers
   - Cell2Sentence: fine-tuned GPT-2, converts gene expression to text sequences of gene names ordered by expression rank

## Data

The survey catalogs datasets used across downstream tasks:
- **Batch correction**: HCA, COVID-19, PBMC 10, Perirhinal Cortex
- **Cell clustering**: Paired-seq, SNARE-seq, HCA, HCL, TCGA, Macaque Retina, GTEx, Tabula Muris
- **Cell type annotation**: Shao, Baron, Muraro, Segerstolpe, Xin, sci-ATAC human atlas, hPancreas, multiple sclerosis, tumor-infiltrating myeloid
- **Gene network inference**: Reactome, DoRothEA, TRRUSTv2, Immune Human, ChIP-Atlas
- **Perturbation prediction**: Dixit, Adamson, Norman

Pre-training data for large models: scGPT used >33M cells; scFoundation uses large-scale scRNA-seq.

## Training Recipe

Not applicable — this is a survey. The paper describes training approaches of the reviewed models:
- **Pre-training objectives**: masked language modeling (scBERT), generative pre-training (scGPT), read-depth-aware prediction (scFoundation), unsupervised autoregressive next-gene prediction (tGPT)
- **Efficient attention**: Performer linear attention (scBERT), Flash-Attention (scGPT), Flowformer (CellPLM)
- **Input representations**: gene2vec embeddings (scBERT), value binning (scGPT), gene expression ranking (tGPT, Cell2Sentence), one-hot + motif embeddings (PROTRAIT), heterogeneous graphs (DeepMAPS, MarsGT, scMoFormer)
- **Fine-tuning**: most large models fine-tune on downstream tasks; scGPT and CellPLM attempt zero-shot settings with mixed results

## Key Ablations & Design Choices

The survey highlights several critical design decisions across models:

1. **Handling long sequences**: scRNA-seq data has ~20,000 genes, exceeding standard transformer limits. scBERT uses Performer (linear attention via low-rank random feature mapping); scGPT uses Flash-Attention; scFoundation uses asymmetric encoder-decoder (only encodes non-zero/non-masked genes, reducing cost).

2. **Gene expression representation**: Raw values (most models) vs. binned values (scGPT) vs. expression ranking (tGPT, Cell2Sentence). Ranking avoids batch-effect interference from HVGs but may lose information from lowly expressed genes.

3. **Graph-based vs. sequence-based**: DeepMAPS/MarsGT use heterogeneous graph transformers on cell-gene matrices with subgraph sampling and shared parameters. Sequence-based models treat genes as tokens. Graph approaches better capture regulatory networks.

4. **Cell-cell relationships**: CellPLM is the first to explicitly model cell-cell relationships by incorporating spatial transcriptomics data and position embeddings in the encoder. Other models treat cells independently.

5. **Zero-shot vs. fine-tuning**: scGPT shows competitive performance in low-data fine-tuning but struggles in zero-shot batch correction. CellPLM achieves strong zero-shot clustering (best ARI/NMI vs. PCA, Geneformer, scGPT). Pre-trained models generally need fine-tuning.

6. **Subgraph sampling**: DeepMAPS uses sparse-based feature selection; MarsGT uses probability-based sampling to select genes/regulatory regions associated with rare cells — important for rare cell type discovery.

## Reported Insights

- Transformer-based SC models outperform traditional methods across most downstream tasks but are still early-stage.
- Benchmark studies [106-108] reveal that different models perform best on different tasks — no single model dominates all benchmarks.
- scGPT shows strong gene function prediction even without fine-tuning but weak zero-shot batch correction.
- Pre-training helps interpretability: scGPT captures complex gene relationships, generates gene networks through zero-shot learning (HLA gene network, CD gene networks).
- Overfitting risk is significant: single-cell data is diverse and imbalanced across types; GAN-based data augmentation suggested as mitigation.
- Computational cost remains a major challenge, especially for multi-omics pre-training; RNN-transformer hybrids proposed as future direction.
- Interpretability is a strength of attention-based models (gene weight assignment via attention) but "black-box" nature still limits clinical application.

## References Worth Chasing

- **scGPT** (ref [39]): first generative pre-trained SC foundation model, >33M cells, multiple downstream tasks
- **scFoundation** (ref [38]): 100M param model with read-depth-aware training
- **scBERT** (ref [36]): first BERT-based SC pre-training model, Performer attention
- **CellPLM** (ref [41]): first to model cell-cell relationships, Flowformer
- **Geneformer** (referenced in comparisons): notable baseline not detailed in this survey
- **Benchmark papers** [106-108]: independent evaluations of SC foundation models — critical for understanding real-world performance vs. claims
- **GEARS** (ref [98]): perturbation prediction method combined with scFoundation

## Notes / Open Questions

- This survey is from a regional university group (Guangxi University) and may not cover all relevant work comprehensively (e.g., Geneformer gets only passing mention, UCE is absent).
- Evidence quality is low: the paper is a narrative review without systematic methodology, no meta-analysis, no inclusion/exclusion criteria.
- The paper was submitted to an unspecified ACM conference (placeholder venue metadata), raising questions about peer review status.
- Missing from the survey: protein language models (ESM, ProtTrans), spatial-only foundation models, and newer entries like UCE and GeneCompass.
- The categorization of "language model" vs. "large language model" is based solely on whether pre-training is used, which is non-standard terminology.
- No discussion of tokenization strategies in depth (e.g., how gene expression values are discretized/binned varies significantly across models and impacts performance).
- The survey would benefit from a systematic comparison table of model architectures, parameter counts, and pre-training data sizes — only partial information is provided.
