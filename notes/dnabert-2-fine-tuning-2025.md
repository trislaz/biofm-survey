---
id: dnabert-2-fine-tuning-2025
title: 'DNABERT-2: Fine-Tuning a Genomic Language Model for Colorectal Gene Enhancer
  Classification'
authors:
- Darren King
- Yaser Atlasi
- Gholamreza Rafiee
year: 2025
venue: null
arxiv: '2509.25274'
doi: null
url: https://arxiv.org/abs/2509.25274v1
pdf_path: papers/dnabert-2-fine-tuning-2025.pdf
md_path: papers/md/dnabert-2-fine-tuning-2025.md
modalities:
- dna
status: extracted
evidence_quality: full-text
tags:
- fine-tuning
- bpe
- enhancer-classification
- colorectal-cancer
- optuna-hpo
- binary-classification
- threshold-tuning
parameters: 117M
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:46+00:00'
updated_at: '2026-04-22T19:46:08+00:00'
is_fm: false
fm_classification_reason: Fine-tuning DNABERT-2 for enhancer classification; application
  paper.
---

## TL;DR

This paper fine-tunes the pre-trained DNABERT-2-117M genomic language model for binary classification of normal vs. tumour-associated gene enhancers in colorectal tissue. The authors assemble a balanced corpus of ~2.34M 1 kb enhancer sequences from ChIP-seq data (hg19), apply summit-centred extraction with three-layer deduplication (within-class, cross-class, reverse-complement collapse), and use Optuna-based hyperparameter optimisation (50 trials) to configure fine-tuning with a 4,096-term BPE vocabulary and 232-token context. On a 350 k held-out test set the model achieves PR-AUC 0.759, ROC-AUC 0.743, and best F1 0.704 at an optimised threshold of 0.359, outperforming the CNN-based EnhancerNet baseline in recall and threshold-independent ranking but underperforming in point accuracy (0.682 vs 0.72). This is an application/fine-tuning study, not a new foundation model.

## Model

- **Base model**: DNABERT-2-117M (pre-trained, not retrained here). Transformer with BPE tokenisation, ALiBi positional encoding, FlashAttention (though FlashAttention was disabled in this study due to dependency issues).
- **Fine-tuning head**: 2-label binary classification head added on top.
- **Vocabulary**: 4,096 BPE tokens (chosen empirically).
- **Context length**: 232 tokens per sequence (empirically chosen for 1 kb DNA windows).
- **Dropout (tuned via Optuna)**: hidden_dropout_prob=0.072, attention_probs_dropout_prob=0.020, classifier_dropout=0.066.

## Data

- **Source**: Colorectal cancer and normal tissue enhancer annotations (ENCODE narrowPeak BED files) from the Atlasi Lab, Queen's University Belfast. Originally 125 cancer + 204 normal samples with 6.83M total enhancer regions.
- **Filtering**: Samples with <5,000 enhancers excluded; class-balanced at the sequence level.
- **Final corpus**: ~1,375,056 normal + ~1,375,063 tumour enhancer sequences (≈2.34M total, balanced).
- **Sequence extraction**: 1 kb fixed windows, summit-centred, from hg19 reference genome (pyfaidx). Only canonical chromosomes (1–22, X, Y, M). Edge effects handled by N-padding.
- **Deduplication**: Three layers — (1) within-class duplicates removed, (2) cross-class collisions removed symmetrically, (3) reverse-complement equivalence enforced (enhancers are unstranded).
- **Split**: Stratified by class. Test set = 350,742 sequences; HPO used 100k train / 40k val subsets.

## Training Recipe

- **Objective**: Binary cross-entropy (2-label classification with label smoothing = 0.026).
- **Tokeniser**: BPE, 4,096-term vocabulary (DNABERT-2 default).
- **Optimiser**: AdamW (PyTorch), lr = 9.02 × 10⁻⁶, weight decay = 3.8 × 10⁻⁶, ε = 1.37 × 10⁻⁹, β₂ = 0.993.
- **Schedule**: Cosine LR decay with warmup_ratio = 0.066.
- **Batch size**: Per-device 384, gradient accumulation → effective batch size 4,096.
- **Epochs**: 5 (converged by epoch 4; best checkpoint selected by validation PR-AUC).
- **Regularisation**: Label smoothing 0.026, gradient clipping (max_grad_norm = 1.43), model-level dropout (see above).
- **Hardware**: NVIDIA B200 GPU (180 GB VRAM), 28 vCPU RunPod VM, mixed precision bf16 + tf32.
- **HPO**: Optuna TPE sampler with multivariate sampling + Median Pruner. 50 trials (20 completed, 30 pruned). Each trial limited to 1,000 steps with eval every 200 steps. Converged within 10–15 trials.
- **Wall-clock**: Not precisely reported; authors note HPO "often spanned several days" and full fine-tuning required "lengthy runtimes".

## Key Ablations & Design Choices

- **Vocabulary size (4,096 BPE tokens)**: Chosen empirically; no explicit ablation over alternative vocab sizes is reported. The paper contrasts BPE against DNABERT's fixed k-mer tokenisation (which has a much larger token set with redundancy).
- **Context length (232 tokens)**: "Chosen empirically" for 1 kb input windows. No ablation table comparing alternative context lengths is provided; the choice is presented as a design decision balancing sequence coverage and compute.
- **Threshold optimisation**: The single most impactful post-hoc choice. At naïve threshold 0.5: F1 = 0.657, precision = 0.731, recall = 0.594. At optimised threshold 0.359: F1 = 0.704 (+7.2%), precision = 0.609 (−16.7%), recall = 0.835 (+40.6%). The study uses threshold-swept PR-AUC as the primary HPO objective rather than fixed-threshold F1.
- **Optuna HPO convergence**: 50 trials, 20 completed, 30 pruned. Rapid convergence within first 10–15 trials; improvements incremental thereafter. Search space included batch size (256–768), lr (5e-6 to 5e-4), weight decay (1e-6 to 5e-2), warmup ratio (0.04–0.12), scheduler type (linear vs cosine), gradient clipping (0.5–2.0), label smoothing (0–0.10), multiple dropout rates.
- **Sequence length (1 kb windows)**: Justified by 95th-percentile enhancer peak lengths of 961 bp (tumour) and 992 bp (normal); ensures inclusion of enhancer core plus flanking context.
- **Deduplication strategy**: Three-layer deduplication (within-class, cross-class, reverse-complement) was critical for preventing over-representation and label leakage given the scale of the dataset.
- **FlashAttention**: Could NOT be enabled due to dependency issues, "likely reducing efficiency". No quantitative comparison with/without.
- **DNABERT-2 vs EnhancerNet (CNN)**: On the same dataset — EnhancerNet with one-hot encoding achieved accuracy 0.72; DNABERT-2 at default threshold achieved accuracy 0.682. However, DNABERT-2 achieved PR-AUC 0.758 (not reported for EnhancerNet), recall 0.835 vs 0.72 (EnhancerNet, k=4), demonstrating superior threshold-independent ranking and sensitivity at the cost of lower point accuracy and precision.

## Reported Insights

- BPE tokenisation combined with transformer attention captures both motif-like features and longer-range sequence context, improving ranking ability and recall relative to fixed k-mer/CNN approaches.
- Threshold tuning is essential: the default 0.5 threshold substantially under-performs the optimised 0.359 threshold, especially for recall.
- Tumour enhancers are consistently easier to detect than normal ones (tumour-sensitivity bias), observed in both DNABERT-2 and EnhancerNet.
- The model's precision remains modest (~0.61), highlighting a tendency to over-call tumour sequences.
- DNABERT-2 outputs are "relatively well-calibrated" and can be integrated into probabilistic frameworks without extensive post-hoc calibration.
- Smart engineering (BPE + ALiBi + efficient attention) can yield competitive performance with far fewer parameters than brute-force scaling (DNABERT-2 vs Nucleotide Transformer: ~21× fewer params, ~92× less GPU time in pre-training, per original DNABERT-2 paper).

## References Worth Chasing

- DNABERT-2: Efficient Foundation Model and Benchmark For Multi-Species Genome (arXiv:2306.15006) — the underlying foundation model being fine-tuned.
- DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome (doi:10.1093/bioinformatics/btab083) — first-gen gLM predecessor.
- Nucleotide Transformer: building and evaluating robust foundation models for human genomes (doi:10.1038/s41592-024-02523-z) — billion-parameter gLM comparison point.
- LOGO / Integrating convolution and self-attention improves language model of human genome (doi:10.1093/nar/gkac326) — lightweight ALBERT-based gLM with CNN module.
- Attention Is All You Need (arXiv:1706.03762) — foundational transformer architecture.
- AlphaFold / Highly accurate protein structure prediction (doi:10.1038/s41586-021-03819-2) — major bio-FM reference.
- PEDLA: predicting enhancers with a deep learning-based algorithmic framework (doi:10.1038/srep28517) — earlier deep-learning enhancer prediction.
- Enhancer reprogramming in tumor progression (doi:10.1007/s00018-018-2820-1) — biological context for enhancer dysregulation in cancer.
- Analysis of the landscape of human enhancer sequences in biological databases (doi:10.1016/j.csbj.2022.05.045) — enhancer length distribution reference.
- Large language models and their applications in bioinformatics (doi:10.1016/j.csbj.2024.09.031) — survey of LLMs in bioinformatics.
- Enhancer: AI for predicting gene enhancer functionality (Allen et al., EMBC 2025) — the EnhancerNet baseline this paper compares against.

## Notes / Open Questions

- **Not a foundation model paper**: This is a fine-tuning application study. No new pre-training is performed; all pre-trained weights come from the public DNABERT-2-117M checkpoint.
- **No formal ablation tables**: Key design choices (vocab size, context length) are described as "empirically chosen" but no systematic ablation results are provided. The paper would be stronger with a vocab-size sweep or context-length comparison.
- **FlashAttention disabled**: The authors could not enable FlashAttention due to dependency issues, which may have affected training efficiency and possibly model quality — this is not quantified.
- **Limited evaluation metrics overlap with baseline**: EnhancerNet reported accuracy/recall/specificity; DNABERT-2 reports PR-AUC/ROC-AUC/F1. Direct comparison is therefore confounded by metric choice. The authors acknowledge this but do not re-evaluate EnhancerNet under the same metrics.
- **No cross-dataset or cross-tissue validation**: All data from a single lab/protocol. Generalisability is unknown.
- **Precision remains weak** (~0.61), limiting practical clinical utility without further improvements.
- **Training tokens / compute not reported**: Total tokens processed during fine-tuning and wall-clock time are not precisely quantified.
- **Single classification task**: Only binary normal-vs-tumour on colorectal tissue; no multi-class, multi-tissue, or regression formulations explored.
