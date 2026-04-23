---
id: scbert-as-a-large-2022
title: 'scBERT: a large-scale pretrained deep language model for cell type annotation
  of single-cell RNA-seq data'
authors:
- Fan Yang
- Wenchuan Wang
- Fang Wang
- Yuan Fang
- Duyu Tang
- Junzhou Huang
- Hui Lu
- Jianhua Yao
year: 2022
venue: Nature Machine Intelligence
arxiv: null
doi: 10.1038/s42256-022-00534-z
url: https://github.com/TencentAILabHealthcare/scBERT
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/scbert-as-a-large-2022.md
modalities:
- scrna
status: extracted
evidence_quality: abstract+repo
tags:
- Performer
- gene-token
- expression-binning
- Gene2vec
- cell-type-annotation
- masked-language-model
- single-cell
parameters: ~10M
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'scBERT: pretrained single-cell transcriptomics FM.'
---

## TL;DR

scBERT is a Performer-based language model for cell-type annotation of scRNA-seq data that treats each gene as a token and discretises expression values into bins. Pre-trained with masked language modelling on ~1M+ human cells from PanglaoDB, it learns gene–gene interaction patterns without explicit batch-effect correction or marker-gene lists. The pre-trained encoder is fine-tuned with a lightweight classification head for cell-type prediction, achieving competitive or superior accuracy versus existing methods (scNym, ACTINN, Cell BLAST, etc.) on benchmarks including Zheng68K PBMCs, cross-platform pancreatic islet datasets, and multi-organ atlases, while also supporting novel cell-type detection via probability thresholding.

## Model

- **Architecture**: PerformerLM — a Transformer variant using FAVOR+ (Fast Attention Via positive Orthogonal Random features) for linear-complexity self-attention, enabling processing of ~16,907-length sequences (one token per gene).
- **Tokenisation**: Gene-as-token. Each of 16,906 human genes is a token position; the raw expression value is discretised into bins (default 5 bins → `num_tokens = 7` including mask and padding classes).
- **Embedding dimension**: 200.
- **Depth**: 6 Performer encoder layers.
- **Attention heads**: 10 (all global; `local_attn_heads = 0`).
- **Positional / gene embedding**: Gene2vec (Du et al. 2019) embeddings (200-d per gene, pre-trained on gene co-expression) used as position embeddings (`g2v_position_emb = True`), encoding gene identity rather than sequential position.
- **Parameters**: ~10M estimated (token embedding 7×200 + Gene2vec 16,907×200 ≈ 3.4M + 6 Performer blocks ≈ 2.9M + output projection). Some secondary sources cite ~30M; exact count not reported.
- **Fine-tuning head**: Conv2d(1,1,(1,200)) → ReLU → FC(16907→512) → FC(512→128) → FC(128→num_classes). Only the last 2 encoder layers + final norm are unfrozen during fine-tuning.
- **Code**: [github.com/TencentAILabHealthcare/scBERT](https://github.com/TencentAILabHealthcare/scBERT) (PyTorch, `performer_pytorch`).

## Data

- **Pre-training corpus**: PanglaoDB (Franzén et al. 2019) — a curated aggregation of published single-cell RNA-seq datasets.
  - File: `panglao_human.h5ad` (human cells only).
  - Estimated >1M cells (exact count not stated in code/README).
- **Gene set**: 16,906 genes after filtering by NCBI Gene database (Jan 2020 update); unmatched and duplicated genes removed.
- **Pre-processing**: `scanpy.pp.normalize_total` + `scanpy.pp.log1p`, then expression values discretised into bins.
- **Fine-tuning datasets**: Zheng68K (PBMCs), Baron/Muraro/Segerstolpe/Xin (pancreas), MacParland (liver), Litviňuková/Tucker (heart), Lukassen (COVID-19 lung), He et al. (HCA 15 organs; GSE159929).
- **Train/val split**: 95/5 for pre-training; 80/20 stratified for fine-tuning.

## Training Recipe

- **Pre-training objective**: Masked Language Modelling (MLM).
  - Mask probability: 15%.
  - Of masked tokens: 90% replaced with `[MASK]`, 10% kept unchanged, 0% random replacement.
- **Optimiser**: Adam, LR = 1×10⁻⁴.
- **Scheduler**: CosineAnnealingWarmupRestarts (first_cycle_steps=15, warmup_steps=5, cycle_mult=2, gamma=0.9, min_lr=1×10⁻⁶).
- **Batch size**: 3 per GPU × gradient accumulation 60 = effective batch 180 per GPU.
- **Epochs**: up to 100 (default), with early stopping on validation loss.
- **Distributed**: PyTorch DDP with NCCL backend (number of GPUs not specified).
- **Gradient clipping**: max norm 100 (pre-training), max norm 1×10⁶ (fine-tuning).
- **Fine-tuning**: Same optimiser/scheduler; cross-entropy loss with optional class weighting; patience-10 early stopping on validation accuracy.

## Key Ablations & Design Choices

| Design choice | Result / rationale |
|---|---|
| **Performer vs standard Transformer** | Standard self-attention is O(n²) which is infeasible for n ≈ 16,907 gene tokens; Performer's FAVOR+ gives O(n) complexity, enabling whole-transcriptome input |
| **Gene2vec positional embeddings** | Encodes gene identity via pre-trained co-expression embeddings rather than ordinal position; ablation shows improved performance (pos_embed default True) |
| **Expression binning (5 bins)** | Converts continuous expression to discrete tokens; hyperparameter range [5, 7, 9]; default 5 bins balances resolution and vocabulary size |
| **Embedding dim [100, 200]** | Default 200; wider embedding captures richer gene representations |
| **Depth [4, 6, 8] / Heads [8, 10, 20]** | Default depth=6, heads=10; hyperparameter table provided in README |
| **Partial unfreezing for fine-tuning** | Only last 2 encoder layers + norm unfrozen; prevents catastrophic forgetting with limited labelled data |
| **Novel cell-type detection** | Threshold on maximum softmax probability (default 0.5) to assign "unassigned" label; simple but effective approach |

## Reported Insights

- Pre-training on large unlabelled scRNA-seq data provides a general understanding of gene–gene interactions that transfers across tissues and platforms, reducing sensitivity to batch effects without explicit correction.
- The gene-as-token approach naturally handles variable gene sets across datasets by selecting the intersection of genes, avoiding the need for imputation or gene-set alignment.
- scBERT outperforms marker-gene-based (SCINA, CellAssign, scSorter), correlation-based (scmap, SciBet), and supervised DL methods (ACTINN, scNym) on intra-dataset and cross-dataset benchmarks.
- Attention weights can be interpreted to identify genes contributing to cell-type decisions, providing biological interpretability.
- The model can detect novel/unseen cell types by thresholding prediction confidence, a practical feature for exploratory single-cell studies.
- On the Zheng68K PBMC dataset, scBERT achieves improved accuracy and macro-F1 over baselines, particularly on rare cell types where other methods struggle.

## References Worth Chasing

1. **Choromanski et al. (2021)** – "Rethinking Attention with Performers" (ICLR 2021); the FAVOR+ mechanism enabling linear-complexity attention used in scBERT.
2. **Du et al. (2019)** – "Gene2vec: distributed representation of genes based on co-expression" (BMC Genomics 20); pre-trained gene embeddings used as positional encoding.
3. **Franzén et al. (2019)** – "PanglaoDB: a web server for exploration of mouse and human single-cell RNA sequencing data" (Database 2019); the pre-training corpus.
4. **Devlin et al. (2019)** – BERT; the pre-train + fine-tune paradigm that scBERT adapts to single-cell biology.
5. **Theislab/scGPT (Cui et al. 2024)** – scGPT; successor single-cell foundation model using autoregressive + masked objectives, larger scale.
6. **Abdelaal et al. (2019)** – Benchmark comparison of automatic cell identification methods for scRNA-seq (Genome Biol. 20).
7. **Yang et al. (2022)** – Preprint bioRxiv 10.1101/2021.12.05.471261 (v1 Dec 2021); contains additional method details not in the published version.

## Ablations (Rev 4)

Source: Extended Data Fig. 1 ("system analysis of the architecture design of scBERT") of the Nature MI paper (Yang et al. 2022) plus the hyperparameter sweep table in the GitHub README. Quantitative numbers below come from the paper's Source Data for ED Fig. 1; where the published figure reports box plots without a single tabulated value, the entry summarises the qualitative direction.

| # | Ablation / variation | Setting compared | Benchmark | Metric | Result | Take-away |
|---|---|---|---|---|---|---|
| 1 | Pre-training vs random init | scBERT pre-trained on ~1M PanglaoDB cells vs same architecture with randomly initialised weights | Zheng68K (5-fold CV) | Accuracy & macro-F1 | Pre-trained > random init by a clear margin on both metrics (ED Fig. 1a box plots) | MLM pre-training on PanglaoDB is the single most important design choice; gene-as-token Performer alone is not enough |
| 2 | Marker-gene robustness | Progressive deletion of canonical marker genes from the input (0% / 10% / 50% / 100% removed) | Zheng68K (5-fold CV) | Accuracy | scBERT remains above the best non-FM baseline (green dashed line in ED Fig. 1b) even with 100% of marker genes removed | The model relies on distributed gene–gene interaction patterns, not on a small set of marker genes — robust to marker dropout / batch loss |
| 3 | Gene embedding type (qualitative) | Gene2vec co-expression embedding vs scBERT contextual embedding for an alpha-specific gene (LOXL4) on Muraro pancreas | UMAP of cell-type separation | Visual cluster separation | Gene2vec alone fails to separate alpha cells; scBERT embedding cleanly separates alpha from beta/delta/gamma (ED Fig. 1c) | Contextual encoding adds cell-type-discriminative information on top of the static Gene2vec positional prior |
| 4 | Number of expression bins | bins ∈ {5, 7, 9} (default 5) | Zheng68K (5-fold CV) | Accuracy / F1 | Performance flat across the range (ED Fig. 1e, top-left) | 5 bins is sufficient; finer expression discretisation gives no measurable gain at this scale |
| 5 | Embedding dimension | dim ∈ {100, 200} (default 200) | Zheng68K (5-fold CV) | Accuracy / F1 | 200 ≳ 100, small but consistent gain (ED Fig. 1e, top-right) | Wider token embedding helps marginally; not a major lever |
| 6 | Number of attention heads | heads ∈ {8, 10, 20} (default 10) | Zheng68K (5-fold CV) | Accuracy / F1 | Performance largely insensitive (ED Fig. 1e, bottom-left) | 10 heads is a safe default; head count is not a critical hyperparameter |
| 7 | Number of Performer encoder layers | depth ∈ {4, 6, 8} (default 6) | Zheng68K (5-fold CV) | Accuracy / F1 | Performance largely insensitive (ED Fig. 1e, bottom-right) | Going deeper than 6 layers does not help on this annotation task — model is bottlenecked by data/objective, not capacity |
| 8 | Attention interpretability check | Element-wise mean of attention matrices across heads/layers | Pre-trained scBERT (no fine-tune) | Heatmap visualisation | Average attention is non-uniform and concentrates on biologically meaningful gene sets (ED Fig. 1d) | Performer attention is not collapsed/uniform — supports the downstream attention-based marker-gene interpretation in the main paper |

**Count: 8 ablations / sensitivity analyses.**

**Top take-away:** Pre-training on PanglaoDB is the dominant driver of scBERT's accuracy (Ablation 1), and the resulting representation is robust enough that removing 100% of canonical marker genes still beats every non-foundation baseline (Ablation 2) — whereas standard architectural knobs (depth, heads, embedding dim, bin count) barely move the needle. The story is "data + MLM objective matter; transformer hyperparameters don't."

## Notes / Open Questions

- **Evidence quality**: abstract + GitHub repo (README + full source code for `pretrain.py` and `finetune.py`). Full paper text not ingested (Nature MI paywall); specific ablation numbers and benchmark tables need verification from the PDF.
- **Parameter count uncertainty**: Architecture (dim=200, depth=6, 16906-gene vocabulary) suggests ~10M parameters; some secondary sources report ~30M. The discrepancy may stem from including the fine-tuning head or a larger undocumented configuration. Worth verifying from the paper.
- **Training compute**: Not reported anywhere. The DDP setup suggests multi-GPU training but number of GPUs and wall-clock time are unspecified.
- **Training token count**: Not reported. Could be estimated as num_cells × 16,906 genes × num_epochs, but neither cell count nor actual epochs used are documented.
- **PanglaoDB size**: The database aggregates >4.5M cells (Franzén 2019), but the `panglao_human.h5ad` subset size is not specified. Different versions of PanglaoDB may contain different cell counts.
- **Comparison to scGPT**: scGPT (2024) uses a similar gene-as-token paradigm but with generative pre-training and much larger scale (~51M params, 33M cells). How does scBERT compare on the same benchmarks?
- **Performer vs Flash Attention**: With modern efficient attention implementations (FlashAttention), would a standard Transformer with gene-level tokens now be feasible and potentially outperform the Performer approximation?
- **Expression binning granularity**: Only 5–9 bins are explored; continuous value embedding (as in scGPT) might preserve more expression information. Is binning a bottleneck?
