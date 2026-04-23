---
id: transfer-learning-enables-predictions-2023
title: Transfer learning enables predictions in network biology
authors: []
year: 2023
venue: Nature
arxiv: null
doi: 10.1038/s41586-023-06139-9
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/transfer-learning-enables-predictions-2023.md
modalities:
- scrna
status: extracted
evidence_quality: full-text
tags:
- rank-encoding
- Genecorpus-30M
- MLM
- in-silico-perturbation
- gene-network
- transfer-learning
parameters: ~10M
training_tokens: ~45B (estimated; ~29.9M cells × ~1.5k genes/cell)
training_compute: ~3 days on 12× V100-32GB (3 nodes × 4 GPUs, DeepSpeed)
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'Geneformer: pretrained single-cell transcriptomics FM.'
---

## TL;DR

Geneformer is a ~10M-parameter transformer encoder pretrained with masked language modelling (MLM) on Genecorpus-30M (~30M human scRNA-seq transcriptomes). Each cell is represented as a sequence of gene tokens **rank-ordered** by expression normalised against corpus-wide medians, discarding absolute counts. Pretraining alone learns gene-network hierarchy (visible in attention weights). Fine-tuning on small labelled sets boosts predictions for dosage sensitivity, bivalent chromatin, TF regulatory range, and network centrality. An *in-silico deletion/activation* strategy enables zero-shot disease modelling; experimentally validated therapeutic targets for dilated cardiomyopathy (GSN, PLN) and a novel dosage-sensitive gene (TEAD4).

## Model

| Property | Value |
|---|---|
| Architecture | Transformer encoder (BERT-style) |
| Layers | 6 |
| Hidden dim | 256 |
| Attention heads | 4 per layer |
| FFN inner dim | 512 |
| Max input length | 2 048 tokens (covers 93% of cells) |
| Vocabulary | 25 424 protein-coding/miRNA genes + 2 special tokens (pad, mask) |
| Activation | ReLU |
| Dropout | 0.02 (all FC layers and attention) |
| Parameters | ~10M (estimated from architecture) |
| Positional encoding | Learned (standard BERT-style) |

Input representation: **rank-value encoding** — genes are ranked by expression within each cell, normalised by the gene's nonzero median expression across Genecorpus-30M. This deprioritises housekeeping genes and up-ranks context-specific TFs. Cell embeddings are the mean of per-gene embeddings from the penultimate layer (256-d).

## Data

**Genecorpus-30M** pretraining corpus:

- 29.9M human single-cell transcriptomes (27.4M pass QC) from 561 datasets.
- Broad tissue coverage (40+ organ categories); excludes malignant cells and immortalised lines.
- Droplet-based platforms only (for count-unit comparability).
- QC filters: total counts within 3 SD of dataset mean; mito reads within 3 SD; ≥7 detected protein-coding/miRNA genes.
- Stored as rank-value-encoded tokens in HuggingFace Datasets (Apache Arrow); space-efficient (only detected genes stored).

Fine-tuning datasets (all small, task-specific):

| Task | Cells | Source |
|---|---|---|
| Dosage sensitivity (TF) | 10 000 random | Genecorpus-30M |
| Bivalent chromatin (ESC) | ~15 000 ESCs | Gifford lab |
| TF regulatory range | ~34 000 iPSC→CM | Seidman lab |
| N1 network centrality | ~30 000 ECs (Heart Atlas); as few as 884 | Heart Atlas / aortic aneurysm |
| Cardiomyopathy classification | ~29 patient hearts | Hubner lab |

## Training Recipe

### Pretraining

- **Objective**: Masked language modelling — 15% of gene tokens masked per cell; predict masked gene identity from context.
- **Optimiser**: AdamW (weight decay 0.001).
- **LR schedule**: Linear warmup (10 000 steps) then linear decay; max LR 1e-3.
- **Batch size**: 12.
- **Epochs**: 3.
- **Hardware**: 3 nodes × 4 NVIDIA V100-32GB = 12 GPUs.
- **Wall time**: ~3 days.
- **Distributed strategy**: DeepSpeed ZeRO (parameter, gradient, and optimizer-state partitioning; CPU offload).
- **Efficiency trick**: Dynamic length-grouped padding — megabatch sampled, sorted by length descending, then dynamically padded per minibatch → **29.4× speedup** over naive padding.

### Fine-tuning

- Initialise from pretrained weights; add one task-specific classification head.
- **Hyperparameters** (same for all tasks): max LR 5e-5, linear warmup (500 steps), AdamW (weight decay 0.001), batch size 12.
- **Epochs**: 1 (to avoid overfitting).
- **Layer freezing**: More layers frozen when task is closer to pretraining objective; more layers unfrozen for distant tasks.
- **Evaluation**: 5-fold cross-validation (80/20 gene-label split) for gene-classification tasks.

## Key Ablations & Design Choices

### Rank-value encoding

- Genes ranked by within-cell expression normalised by corpus-wide nonzero median → nonparametric, robust to batch effects.
- TFs normalised by statistically lower factor (higher rank); housekeeping genes deprioritised.
- Limitation acknowledged: discards precise transcript-count information.

### Pretraining corpus scale

- Larger, more diverse pretraining corpora consistently improve downstream fine-tuning performance (Fig. 2b), even with fixed fine-tuning data size.
- 15% masking marginally better than 5% or 30% (Extended Data Fig. 1e).
- Including/excluding fine-tuning cells in pretraining corpus makes no difference to downstream classification (separate objectives; Extended Data Fig. 1f).

### In-silico deletion / activation

- **Deletion**: Remove gene from rank encoding; measure cosine-similarity shift in cell or gene embeddings.
- **Activation**: Move gene to front of rank encoding.
- **Combinatorial**: Deleting GATA4 + TBX5 together impacts co-bound targets more than the sum of individual deletions (synergy detected).
- Applied zero-shot (no fine-tuning) for dosage-sensitivity screening and with fine-tuned disease classifier for therapeutic target discovery.

### Fine-tuning ablations

- Minimum fine-tuning data: ~5 000 ECs retain near-full performance for N1 centrality; 884 disease-relevant ECs outperform 30 000 generic ECs — **relevance of fine-tuning data matters more than quantity**.
- Single fine-tuning epoch suffices; same hyperparameters across all tasks (intentionally un-tuned to show generality).

### Batch integration & context awareness

- Pretrained embeddings robust to sequencing platform, preservation method, patient variability (Extended Data Fig. 2a).
- Fine-tuned model integrates platforms (Drop-seq vs DroNc-seq) better than ComBat or Harmony (Extended Data Fig. 4).
- In-silico reprogramming (adding OSKM to front of encoding) shifts gene embeddings toward iPSC state, demonstrating context-awareness.

### Attention-weight analysis

- 20% of attention heads significantly attend to TFs over other genes (self-supervised).
- Early layers survey diverse gene ranks; middle layers attend broadly; final layers focus on highest-ranked (most cell-state-defining) genes.

## Reported Insights

- Geneformer encodes gene-network hierarchy in attention weights without any supervision — centrality-driven heads emerge naturally.
- Dosage-sensitivity predictions: AUC 0.91; 96% concordance with Collins et al. high-confidence neurodevelopmental genes in fetal cerebral cells; context-dependent for moderate-confidence genes.
- Bivalent chromatin: AUC 0.93 (bivalent vs unmethylated); generalises genome-wide from only 56 conserved training loci.
- TF regulatory range (long vs short): significant boost over alternatives (which are near-random).
- N1 network centrality: AUC 0.81.
- Disease modelling: 90% accuracy classifying cardiomyopathy subtypes; in-silico treatment identifies GSN and PLN as dilated cardiomyopathy targets — CRISPR KO in TTN+/− iPSC microtissues significantly improves contractile stress. Novel gene TEAD4 validated as dosage-sensitive in cardiac development.

## References Worth Chasing

- **Collins et al. (ref 22)**: CNV analysis of 753K individuals for dosage-sensitive neurodevelopmental genes — ground-truth for Geneformer dosage predictions.
- **Theodoris et al. 2017 (refs 4, 5)**: NOTCH1-dependent gene network mapping in cardiac valve disease — prior work by same group establishing network-correcting therapy concept.
- **Chen et al. (ref 31)**: Systematic integration of TF-binding and expression for long- vs short-range regulatory classification — fine-tuning labels source.
- **DeepSpeed (refs 9, 10)**: Distributed training framework enabling large-scale pretraining.
- **Svensson et al. 2020 (ref 154)**: Database of scRNA-seq datasets — resource for corpus assembly.

## Notes / Open Questions

- **Parameter count not stated**: ~10M estimated from architecture; paper never reports it explicitly.
- **No held-out pretraining perplexity reported** on the full corpus; only small-scale (100K cell) pretraining evaluation loss shown.
- Rank-value encoding discards absolute expression — unclear how much information is lost for tasks where expression magnitude matters (e.g., dosage effects).
- All fine-tuning uses intentionally un-tuned hyperparameters; reported numbers are likely a **lower bound** on achievable performance.
- Only human data; no cross-species generalisation tested.
- Model is relatively small (~10M params, 6 layers) compared to later scRNA FMs (scGPT, scFoundation). Depth limited by data size at the time.
- In-silico perturbation assumes removing/adding a gene from the rank encoding faithfully models biological loss/gain-of-function — a strong simplifying assumption.
- Cell embeddings are simple mean-pooling of gene embeddings; no [CLS] token or learnt aggregation.

## Ablations (Rev 4)

| # | Ablation / variable | Variants compared | Metric | Result | Source |
|---|---|---|---|---|---|
| 1 | Pretraining corpus size | Subsets of Genecorpus-30M up to full 30M cells, fixed fine-tune set | Downstream classification accuracy (dosage sensitivity, bivalent chromatin, long-range TF) | Monotonic gain with corpus size; full corpus best across all 3 tasks | Fig. 2b |
| 2 | MLM masking ratio | 5% vs **15%** vs 30% | Pretraining val loss / downstream acc | 15% marginally best; 5% under-trains, 30% destabilises | Ext. Data Fig. 1e |
| 3 | Overlap of fine-tune cells in pretrain corpus | Included vs excluded | Downstream classification acc | No measurable difference — objectives are independent | Ext. Data Fig. 1f |
| 4 | Pretraining vs random init | Pretrained Geneformer vs from-scratch fine-tune | AUC across 4 gene-classification tasks | Pretrained substantially > scratch on every task; gap widens as fine-tune set shrinks | Fig. 3 / Ext. Data Fig. 3 |
| 5 | Fine-tune sample size | 30k generic ECs vs 5k ECs vs **884 disease-relevant ECs** | N1 centrality AUC | 884 relevant > 30k generic; 5k retains near-full perf → **relevance ≫ quantity** | Fig. 4 |
| 6 | Layer-freezing schedule | Vary # frozen transformer layers per task | Downstream acc | Freeze more for tasks close to MLM (gene-level); unfreeze more for distant tasks (cell/disease) | Methods |
| 7 | Fine-tune epochs | 1 vs >1 epoch | Val acc | 1 epoch optimal; more epochs overfit on small labelled sets | Methods |
| 8 | Fine-tune hyperparams | Single fixed recipe (LR 5e-5, bs 12, AdamW) across all tasks | Acc vs per-task tuning | Intentionally un-tuned; reported numbers are a lower bound on achievable performance | Methods |
| 9 | Batch / platform integration | Geneformer (zero-shot + fine-tuned) vs ComBat vs Harmony | Drop-seq ↔ DroNc-seq mixing | Fine-tuned Geneformer integrates better than ComBat/Harmony; pretrained embeddings already platform-robust | Ext. Data Fig. 2a, 4 |
| 10 | Length-grouped dynamic padding | Naive pad-to-max vs megabatch length-sorted dynamic pad | Throughput | **29.4× speedup** with no quality loss | Methods |
| 11 | In-silico perturbation: zero-shot vs fine-tuned | Pretrained-only vs disease-fine-tuned classifier for target discovery | Hit recovery (GSN, PLN, TEAD4) | Zero-shot suffices for dosage screens; fine-tuned needed for disease-specific therapeutic targets | Figs. 5–6 |
| 12 | Combinatorial in-silico deletion | Single (GATA4) + single (TBX5) vs joint deletion | Δ cosine on co-bound targets | Joint > sum of singles → model captures synergistic TF interactions | Fig. 5 |
| 13 | Cell-embedding aggregation | Mean-pool of penultimate gene embeddings (no [CLS]) | Downstream cell-level tasks | Simple mean works; no dedicated [CLS] token used or compared | Methods (open question) |

### Take-aways

- **Top take-away: relevance of fine-tuning data dominates quantity** — 884 disease-context ECs beat 30k generic ECs (ablation 5). This is the strongest practical lesson: curate, don't just scale, the labelled set.
- Pretraining scale matters monotonically (1); pretraining itself is the dominant contributor (4) — random init collapses on small fine-tune sets.
- Recipe choices (15% mask, 1 epoch, fixed LR) are mostly first-order insensitive; the paper deliberately under-tunes to demonstrate generality, so reported AUCs are a lower bound (2, 7, 8).
- Engineering wins are large and orthogonal to modelling: dynamic length-grouped padding gives a 29.4× throughput boost (10).
- In-silico perturbation is validated as a usable interface: zero-shot for screening, fine-tuned for therapeutic targets, and combinatorial deletions recover known TF synergy (11, 12).
- Open ablation gaps: no [CLS]-vs-mean aggregation comparison (13), no architecture-size sweep, and no cross-species transfer test.
