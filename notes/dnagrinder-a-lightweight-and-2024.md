---
id: dnagrinder-a-lightweight-and-2024
title: 'dnaGrinder: a lightweight and high-capacity genomic foundation model'
authors:
- Qihang Zhao
- Chi Zhang
- Weixiong Zhang
year: 2024
venue: null
arxiv: '2409.15697'
doi: null
url: https://arxiv.org/abs/2409.15697v1
pdf_path: papers/dnagrinder-a-lightweight-and-2024.pdf
md_path: papers/md/dnagrinder-a-lightweight-and-2024.md
modalities:
- dna
status: extracted
evidence_quality: high
tags:
- encoder-only
- genomics
- efficient
- long-context
- alibi
- flash-attention
- swiglu
- bpe
- mlm
parameters: 63.6M
training_tokens: 69.5B
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:44+00:00'
updated_at: '2026-04-22T20:19:10+00:00'
---

## TL;DR

dnaGrinder is a 63.6M-parameter encoder-only genomic foundation model that matches or beats much larger models (NT-2500M, DNABERT-2) on 30 downstream tasks while being ~40× smaller. Key ingredients: ALiBi positional bias, Flash Attention 2, SwiGLU, memory-efficient BPE, sequence length warmup, and a carefully de-duplicated multispecies pretraining corpus. Trained on only 69.5B tokens (vs 300B for NT-v2). Handles >140K tokens on a single 80 GB GPU.

## Model

- **Architecture**: Encoder-only transformer (BERT-style), 12 layers.
- **Parameters**: 63.6M.
- **Tokenizer**: Memory-Efficient BPE (ME-BPE) with vocabulary size 4,096. Compresses ~5 bp per token. Iterative vocabulary construction across file splits to stay within memory.
- **Positional encoding**: ALiBi (Attention with Linear Biases) — no learned/rotary positional embeddings. Enables strong extrapolation: pretrained on 12K bp sequences, infers on 120K+ bp.
- **Attention**: Flash Attention 2 with unpadding.
- **Activation**: SwiGLU (chosen over GEGLU to keep parameters at 63.6M vs 110M with GEGLU).
- **Dropout**: Removed entirely.
- **Pretraining objective**: Masked Language Modeling (MLM) with 15% mask ratio and dynamic masking.
- **Max pretraining sequence length**: 2,314 tokens (~12,000 bp).

## Data

- **Human Reference Genome** (GRCh38.p14): soft-masked assembly used to filter repetitive regions; non-repeat content retained (~50% per chromosome). First genomic FM to explicitly remove repeats from pretraining data.
- **1000 Genome Project**: 3,202 samples; SNVs, INDELs, and structural variants (DELs, INSs, DUPs, INVs) — both maternal and paternal alleles incorporated (unlike NT which uses one).
- **Multispecies reference genomes**: 794 species from NCBI (bacteria, fungi, invertebrates, protozoa, vertebrates). Human genome is 2.7% of multispecies set.
- **Data augmentation**: Overlapping 12,200 bp segments with random 200 bp offset extraction; variant locus replacement from 1000G.
- **Effective pretraining tokens**: 69.5B tokens consumed (out of a potential 300B token augmented set), sufficient due to sequence length warmup.

## Training Recipe

- **Hardware**: 8× H100 GPUs.
- **Pretraining steps**: 119,000 steps.
- **Batch size**: 256; max sequence length 2,314 tokens.
- **Optimizer**: AdamW (β₁=0.9, β₂=0.98, ε=1e-6, weight decay 1e-5).
- **Learning rate schedule**: Linear warmup 0→4e-4 over first 16K steps, then cosine annealing.
- **Sequence Length Warmup (SLW)**: Sequences sorted by token count (ascending); simpler/shorter sequences trained first. First encoder-based model to use SLW. Reduces padding waste and improves stability.
- **Further pretraining**: Optional; 31K steps on a single A800 GPU (batch size 32, max seq len 2,241, lr 5e-5) on all downstream datasets (GUE + GUE-plus). Mixed results — slight improvements on 4/10 yeast epigenetic tasks, slight declines on 6/10.
- **Fine-tuning**: Two linear layers with LayerNorm, GELU, dropout 0.1. Learning rates searched in [1e-5, 7e-5] across 20 values × 5 random seeds = 100 runs per task.
- **Compute**: Not explicitly stated (8×H100 for 119K steps; wall-clock time not reported).

## Key Ablations & Design Choices (MOST IMPORTANT)

1. **SwiGLU vs GEGLU**: GEGLU inflates parameters from 63M to 110M; SwiGLU achieves comparable performance with roughly half the gate parameters. Chosen for parameter efficiency.
2. **ALiBi vs RoPE/Sinusoidal**: ALiBi enables extrapolation from 12K bp pretraining to 120K+ bp inference with stable perplexity. RoPE decays beyond 4K–6K positions. dnaGrinder achieves 100% species classification at 120K bp; HyenaDNA (160K) gets 64.22%; DNABERT-2 and NT models OOM at batch=1.
3. **Sequence Length Warmup**: First use in encoder-based models. Organizes training by species (ascending token count). Model converges with only 69.5B tokens instead of the full 300B augmented set — a ~4.3× data efficiency gain.
4. **Repeat removal from human genome**: Filtering repetitive regions (~50% of genome) prevents redundant training and improves learning of informative patterns. First genomic FM to do this.
5. **Dual-allele variant incorporation**: Using both maternal and paternal variants from 1000G (including SVs >50 bp, not just SNVs/INDELs) increases diversity vs single-allele approaches (NT).
6. **Flash Attention 2 vs Flash Attention Triton** (used by DNABERT-2): 2× faster, better inference for short queries.
7. **Further pretraining limited benefit**: Only marginal gains on some tasks; average MCC actually decreased by ~0.12 across 10 yeast epigenetic tasks. Suggests the base pretraining already captures sufficient task-relevant features.
8. **Dilated attention (negative result)**: Early experiment with dilated attention scaled to 400K bp but failed to learn meaningful features (low MLM accuracy). Approximated attention loses critical information.
9. **SNP-only pretraining (negative result)**: Training on isolated SNP variant data (without full sequences) failed to generalize across chromosomes — model overfit to single chromosome distributions.

## Reported Insights

- BERT-family models are sensitive to fine-tuning learning rate; 0.1×10⁻⁵ changes lead to significantly different results. Extensive hyperparameter search (100 runs/task) is necessary.
- Large models (NT-2500M) converge to local minima easily in some tasks, struggling to pass 50% accuracy even with LoRA; small models can be more trainable.
- Covid variant classification is hard for all models (distribution mismatch with pretraining); dnaGrinder and DNABERT-2 converge after 1–2 runs while others often fail.
- On 30 tasks, dnaGrinder ranks 1st in 11 and 2nd in 12; average score 73.01 (vs DNABERT-2: 70.86, NT-2500M: 68.32).
- ME-BPE compresses ~5 bp/token; on a 12 GB GPU (RTX 4070), handles 17K+ tokens; on 80 GB GPU (H100/A800), handles 140K+ tokens.

## References Worth Chasing

- **DNABERT-2** (Zhou et al., ICLR 2024): Main comparison baseline; GUE benchmark source.
- **Nucleotide Transformer** (Dalla-Torre et al., 2023): Multi-species pretraining and v2 scaling-law-driven models.
- **HyenaDNA** (Nguyen et al., NeurIPS 2023): Decoder-only DNA model with SLW; long-context comparison.
- **ALiBi** (Press et al., 2021): Positional bias method enabling length extrapolation.
- **Sequence Length Warmup** (Li et al., NeurIPS 2022): Stability-efficiency tradeoff in GPT training; adapted here for encoders.
- **GenBench** (Liu et al., 2024): Systematic genomic FM evaluation benchmark.

## Notes / Open Questions

- Training compute (GPU-hours/FLOPs for pretraining) not reported; only relative FLOPs for inference on a short benchmark sequence are given.
- The 100-run hyperparameter search per task (20 lr × 5 seeds) makes fair comparison tricky — results are best-of-100 rather than expected performance.
- No code or model weights released at time of writing (arXiv v1, Sep 2024).
- Unclear how ME-BPE vocabulary quality degrades with very large numbers of file splits or highly divergent species.
- Further pretraining hurt more tasks than it helped — suggests potential overfitting or distribution shift from downstream data mixing.
