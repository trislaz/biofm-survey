---
id: vqdna-unleashing-the-power-2024
title: 'VQDNA: Unleashing the Power of Vector Quantization for Multi-Species Genomic
  Sequence Modeling'
authors:
- Siyuan Li
- Zedong Wang
- Zicheng Liu
- Di Wu
- Cheng Tan
- Jiangbin Zheng
- Yufei Huang
- Stan Z. Li
year: 2024
venue: null
arxiv: '2405.10812'
doi: null
url: https://arxiv.org/abs/2405.10812v2
pdf_path: papers/vqdna-unleashing-the-power-2024.pdf
md_path: papers/md/vqdna-unleashing-the-power-2024.md
modalities:
- dna
status: extracted
evidence_quality: high
tags:
- tokenizer
- vector-quantization
- codebook-learning
- genome-language-model
- masked-language-modeling
parameters: 103_000_000
training_tokens: 262_000_000_000
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:46+00:00'
updated_at: '2026-04-22T20:28:12+00:00'
---

## TL;DR

VQDNA replaces hand-crafted DNA tokenization (k-mer, BPE) with a learnable VQ-VAE codebook, training an end-to-end genome vocabulary. The Hierarchical Residual Quantization (HRQ) variant stacks coarse-to-fine codebooks across encoder layers, exponentially growing effective vocabulary while keeping codebook sizes small. With only ~103 M params (86 M BERT encoder + 17 M tokenizer), VQDNA (HRQ) ranks #1 across 32 genome downstream tasks, beating NT-2500M (2.5 B params) and DNABERT-2.

## Model

- **Architecture**: 3-stage pipeline:
  1. **Stage 1 – VQ tokenizer training**: ConvNeXt-style encoder (6 residual blocks, D=384) + symmetric decoder. Stem: 1D conv (kernel 5, stride 1) projecting one-hot nucleotides → 256 dims → LayerNorm + GELU. Each residual block: depth-wise conv (kernel 7) + 2 FC layers (4× inverted bottleneck). Output sequence length = input length.
  2. **Stage 2 – Masked code modeling**: BERT-Base Transformer encoder pre-trained with MLM (25% masking) on VQ-tokenized embeddings. Codebook is frozen.
  3. **Stage 3 – Fine-tuning**: LoRA fine-tuning of the pre-trained Transformer + MLP head per downstream task.
- **VQ-VAE tokenizer**: codebook C of K=512 entries, each e(k) ∈ ℝ^384. Nearest-neighbor lookup with straight-through estimator (STE). Codebook updated via EMA (Eq. 4), not gradient.
- **HRQ tokenizer**: hierarchy of codebooks at encoder layers 3 and 6 (N=2 quantization layers in practice). Layer-n codebook has 2^n · K entries (i.e., layer-3: 2K=768 codes; layer-6: 4K=1536 codes if K=384). Hierarchical input H^(n) = 2·Z^(n) − e(M^(n-1)), maintaining scale consistency across layers. Final embedding = average of all hierarchical quantized embeddings.
- **Total params**: VQDNA (VQVAE) = 86 M + 16 M = 102 M; VQDNA (HRQ) = 86 M + 17 M = 103 M.
- **FLOPs** (at seq len 512): VQVAE 1.1 + 0.5 = 1.6 GFLOPs; HRQ 1.1 + 0.6 = 1.7 GFLOPs.

## Data

- **Pre-training corpus** (same as DNABERT-2): human genome (2.75 B nucleotide bases) + multi-species genome (32.49 B nucleotide bases) = ~262 B training tokens (Table 2).
- **Downstream evaluation**: 32 datasets — GUE benchmark (28 datasets) + 3 EEP datasets + 1 species classification dataset. Tasks: Epigenetic Mark Prediction (EMP, yeast), TFP (mouse & human), Covid Variants Classification (CVC), Promoter Detection (PD), Core Promoter Detection (CPD), Splice Site Prediction (SSP), Editing Efficiency Prediction (EEP). Input lengths range from 63 to 32k nucleotides.

## Training Recipe

1. **Stage 1** (tokenizer): 1 epoch, AdamW, lr=1e-4 with cosine schedule, batch size 1024, 8× A100 GPUs. Loss = L_CE(reconstruction) + β·L_commit (β=0.5). Codebook updated by EMA, not by L_code gradient.
2. **Stage 2** (MLM pre-training): 500k steps, 25% random masking, lr=5e-4 cosine, batch size 2048, 8× A100 GPUs. Codebook frozen.
3. **Stage 3** (fine-tuning): AdamW + LoRA on Transformer encoder, task-specific MLP head. Follows GUE benchmark evaluation protocol. 3 trials averaged.
- Framework: PyTorch + HuggingFace Transformers, NVIDIA A100 GPUs.
- Exact GPU-hours / total FLOPs not reported.

## Key Ablations & Design Choices

### Tokenizer comparisons (Table 1 — CVC task, most informative)
| Tokenizer | Token Usage (%) | Linear Probe F1 | Fine-tune F1 |
|---|---|---|---|
| DNABERT 6-mer | 47 | 23.54 | 55.50 |
| NT-2500M 6-mer (non-overlap) | 47 | 23.54 | 66.73 |
| HyenaDNA one-hot | 100 | 5.47 | 54.10 |
| DNABERT-2 BPE (6-mer) | 99 | 36.53 | 71.02 |
| VQDNA VQVAE | 100 | 44.76 | 73.16 |
| VQDNA HRQ | 100 | **48.87** | **74.32** |

**Key insight**: VQ tokenizers achieve 100% token usage (no codebook collapse) while dramatically improving linear-probe discriminability — HRQ's linear probe F1 (48.87) is 2× the best hand-crafted tokenizer (BPE at 36.53), indicating the codebook learns genuinely discriminative patterns, not just compression.

### Codebook size (Table 7 — CVC dataset, reconstruction accuracy / linear F1)
| Code size | VQVAE Rec/Lin | HRQ Rec/Lin |
|---|---|---|
| 128 | 98.2 / 42.1 | 98.4 / 42.8 |
| 256 | 98.8 / 43.6 | 99.1 / 47.7 |
| **512** | **99.5 / 44.8** | **99.6 / 48.9** |
| 1024 | 99.6 / 44.5 | 99.8 / 48.2 |

512 is optimal — 1024 slightly hurts linear probe due to codebook sparsity.

### Codebook dimension (Table 8)
| Dim | VQVAE Rec/Lin | HRQ Rec/Lin |
|---|---|---|
| 256 | 99.4 / 44.3 | 99.5 / 48.2 |
| **384** | **99.5 / 44.8** | **99.6 / 48.9** |
| 768 | 99.6 / 44.6 | 99.6 / 48.9 |

Dimension has small effect; 384 chosen for efficiency.

### Masking ratio (Table 9 — H3 MCC / CVC F1)
| Mask ratio | VQVAE H3/CVC | HRQ H3/CVC |
|---|---|---|
| 15% | 77.9 / 72.6 | 78.3 / 73.7 |
| 20% | 78.3 / 73.4 | 78.8 / 74.2 |
| **25%** | **78.6 / 73.2** | **79.2 / 74.3** |
| 30% | 77.4 / 73.0 | 78.6 / 73.9 |

25% masking is best — higher than typical NLP (15%). Authors hypothesize VQ tokenizer encodes rich contextual information, allowing harder MLM objectives.

### HRQ vs VQVAE across all tasks
HRQ consistently outperforms VQVAE (average rank 1 vs 2, Table 2). The hierarchical design lets coarse codebook capture global semantic structure while fine codebook captures local motifs (UMAP in Fig. 5 shows intra/inter-lineage clustering of SARS-CoV-2 variants).

### Long-sequence scaling (Table 6 — Species Classification, Top-1 Acc)
| Method | 1k | 20k | 32k |
|---|---|---|---|
| HyenaDNA | 61.13 | 87.42 | 93.42 |
| DNABERT-2 | 61.04 | 86.83 | 99.28 |
| VQDNA (HRQ) | **61.57** | **88.05** | **99.46** |

VQDNA (HRQ) beats both at 32k. HyenaDNA can scale to 450k (99.40) but OOM for Transformer-based models. At 32k, VQDNA already surpasses HyenaDNA's 450k accuracy.

## Reported Insights

- The 4-letter DNA alphabet is fundamentally limited for VQ codebook learning — HRQ's hierarchical decomposition is key to overcoming this.
- VQ tokenizer implicitly captures inter-sequence context (whole input affects codebook optimization), unlike k-mer/BPE which only consider intra-sequence statistics.
- SARS-CoV-2 analysis (Fig. 5): HRQ embeddings cluster variants by lineage, with biologically related variants (Delta → Lambda mutation) appearing closer in embedding space. Layer-3 (coarse) codebook captures lineage-level semantics; layer-6 (fine) codebook captures mutation-level differences.
- Additional training stage cost is the main trade-off — Stage 1 tokenizer training adds compute overhead.
- Model scale has not been pushed to maximum; authors note scaling up with linear attention + larger genomic databases as future work.

## References Worth Chasing

- **DNABERT-2** (Zhou et al., 2024, ICLR) — the BPE tokenization baseline and source of the pre-training recipe/data.
- **Nucleotide Transformers** (Dalla-Torre et al., 2023) — 500M–2.5B param genome models, multi-species pre-training.
- **HyenaDNA** (Nguyen et al., 2023) — long-range genomic modeling up to 450k, subquadratic attention alternative.
- **Residual Quantization** (Lee et al., 2022, CVPR) — the RQ technique that HRQ extends from single-input to hierarchical multi-input.
- **VQ-VAE** (Van Den Oord et al., 2017) — cornerstone VQ method.
- **GUE benchmark** (Zhou et al., 2024) — the 28-dataset genome evaluation benchmark used throughout.
- **BEND benchmark** (Marin et al., 2024, ICLR) — alternative genome benchmark mentioned in related work.

## Notes / Open Questions

- **Compute cost not reported**: total GPU-hours / FLOPs budget for Stage 1 + Stage 2 not given. The extra tokenizer training stage is acknowledged as a limitation but not quantified.
- **Tokenizer is task-agnostic**: same frozen VQ codebook used across all 32 tasks — strong evidence the vocabulary captures general genomic patterns.
- **No comparison with byte-level / character-level Transformer baselines** (e.g., no direct comparison with a BERT trained on raw nucleotide tokens without any tokenizer).
- **HRQ uses only 2 quantization layers** in practice (at layers 3 and 6 of a 6-layer encoder) — deeper hierarchies not explored.
- **Sequence length limited to 32k** due to Transformer quadratic attention — not competitive with HyenaDNA on 250k+ sequences. Linear attention extensions mentioned as future work.
- **RNA/protein transfer not explored** — framework is conceptually applicable but only validated on DNA.
- **Venue**: ICML 2024 (Proceedings of the 41st International Conference on Machine Learning).
