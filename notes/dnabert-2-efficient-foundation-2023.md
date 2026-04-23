---
id: dnabert-2-efficient-foundation-2023
title: 'DNABERT-2: Efficient Foundation Model and Benchmark For Multi-Species Genome'
authors:
- Zhihan Zhou
- Yanrong Ji
- Weijian Li
- Pratik Dutta
- Ramana Davuluri
- Han Liu
year: 2023
venue: null
arxiv: '2306.15006'
doi: null
url: https://arxiv.org/abs/2306.15006v2
pdf_path: papers/dnabert-2-efficient-foundation-2023.pdf
md_path: papers/md/dnabert-2-efficient-foundation-2023.md
modalities:
- dna
status: extracted
evidence_quality: full-text
tags: ["mlm", "byte-pair-encoding", "alibi", "flash-attention", "lora", "geglu", "multispecies", "genome-benchmark"]
parameters: 117000000
training_tokens: 262000000000
training_compute: null
references_chased: false
added_at: '2026-04-22T19:50:40+00:00'
updated_at: '2026-04-22T19:54:12+00:00'
---

## TL;DR

DNABERT-2 is a 117M-parameter multi-species genome foundation model that replaces k-mer tokenization with Byte Pair Encoding (BPE), achieving comparable performance to the 2.5B-parameter Nucleotide Transformer (NT-2500M-multi) with 21× fewer parameters and ~92× less GPU time. It uses a Transformer Encoder backbone with ALiBi positional biases (enabling arbitrary-length extrapolation), FlashAttention, and GEGLU activations. The paper also introduces the Genome Understanding Evaluation (GUE) benchmark: 36 datasets across 9 tasks, 4 species, input lengths 70–10,000. DNABERT-2 achieves 66.80 average score on GUE (vs. 66.93 for NT-2500M-multi at 2537M params).

## Model

- **Architecture**: Transformer Encoder (BERT-style), adapted from the original DNABERT architecture.
- **Parameters**: 117M (vs. 86–89M for DNABERT variants, 480M–2537M for Nucleotide Transformer variants).
- **Positional encoding**: Attention with Linear Biases (ALiBi) — replaces learned positional embeddings; enables extrapolation to sequences much longer than the 128-token training length (tested up to 10,000 bp).
- **Attention**: FlashAttention for IO-aware exact attention computation (reduced HBM reads/writes).
- **Activation**: GEGLU (variant of GLU) replaces ReLU in FFN.
- **Tokenizer**: SentencePiece BPE with vocabulary size 4096 (=2^12). Average token length ~5 nucleotides; sequences compressed ~5× relative to raw nucleotide length.
- **Context length at pretraining**: 128 tokens (~640 bp equivalent given ~5× compression). At fine-tuning/inference: arbitrary length via ALiBi.
- **Fine-tuning**: Standard full fine-tuning for DNABERT-2; LoRA (r=8, alpha=16, dropout=0.05) used for NT baselines due to their size.

## Data

- **Human genome dataset**: GRCh38/hg38 human reference genome, 2.75B nucleotide bases (same as original DNABERT).
- **Multi-species genome dataset**: 135 species across 7 categories (fungi, invertebrate, vertebrate, bacteria, etc.), totaling 32.49B nucleotide bases (~12× human genome). Categories include mammals (e.g., human, mouse, buffalo), bacteria, fungi, invertebrates, vertebrates, plants, and others.
- **Preprocessing**: All sequences containing N removed; only A, T, C, G retained.
- **Deduplication/filtering**: Not explicitly described beyond N-filtering.
- **Final model (DNABERT-2)**: Pretrained on multi-species genome dataset (32.49B bases). The paper also trains a human-only variant for ablation.
- **Benchmark (GUE)**: 28 datasets across 7 tasks (input ≤1000 bp): Core Promoter Detection (human), Transcription Factor Prediction (human & mouse), Promoter Detection (human), Splice Site Detection (human), Epigenetic Marks Prediction (yeast), Covid Variant Classification (virus). GUE+ adds 8 datasets with 5,000–10,000 bp inputs: Enhancer-Promoter Interaction (human), Species Classification (fungi, virus). 4 species total. Data sources: EPDnew, ENCODE ChIP-seq, Ensembl GRCh38, GISAID EpiCoV, GenBank.
- **Splits**: Explicit train/dev/test splits defined for all 36 datasets.

## Training Recipe

- **Objective**: Masked Language Modeling (MLM), 15% mask ratio. Independent token masking (not span masking as in original DNABERT). BPE naturally creates a span-prediction-like effect since masked tokens cover variable numbers of nucleotides.
- **Tokenizer**: SentencePiece BPE, vocab size 4096.
- **Batch size**: 4096.
- **Max sequence length**: 128 tokens.
- **Optimizer**: AdamW (β₁=0.9, β₂=0.98, ε=1e-6, weight decay=1e-5).
- **Learning rate schedule**: Linear warmup from 0 to 5e-4 over first 30,000 steps, then linear decay to 0 over remaining 470,000 steps.
- **Total steps**: 500,000.
- **Total training tokens**: 262B (batch_size 4096 × seq_len 128 × 500,000 steps = 262.1B tokens).
- **Hardware**: 8× NVIDIA RTX 2080Ti GPUs.
- **Wall-clock time**: ~14 days on 8× RTX 2080Ti. Compared to NT-2500M-multi: ~28 days on 128× A100 (estimated ~92× more GPU time).
- **Libraries**: HuggingFace Transformers, MosaicML Composer.
- **Further pretraining (DNABERT-2♦)**: Additional MLM on GUE training sets combined; batch size 32, max seq len 128, lr 5e-5, 100,000 steps → 0.41B tokens (0.08% of total pretraining tokens).

## Key Ablations & Design Choices

### Tokenization: BPE vs. k-mer (Table 10, Appendix A.6)
- **What was varied**: Tokenization method (BPE vs. 6-mer), with same architecture, data, hyperparameters.
- **Setup**: Both variants trained on same data, same architecture, batch size 4096, max seq len 128, 120,000 steps. 6-mer chosen to match BPE vocab size (4096 vs. 4101 tokens).
- **What was measured**: GUE benchmark performance (28 datasets).
- **Result**: BPE wins on 21/28 datasets. Average score: BPE 65.33 vs. k-mer 60.92 (+4.41 absolute). BPE also 3–4× less computational cost than overlapping k-mer.

### Vocabulary size (Figure 3, Section 3.1)
- **What was varied**: BPE vocabulary size from 2^5 to 2^15 (8 configurations).
- **What was measured**: Average token length, sequence compression ratio, model performance on GUE.
- **Key findings**: Larger vocab → longer average tokens → shorter sequences → lower compute. But performance does not monotonically increase with vocab size (sparse embedding updates at very large vocab). Vocab size 2^12=4096 chosen as best trade-off.
- **Three variants pretrained for detailed comparison**: vocab 2^5, 2^12, 2^15, each with batch size 2048 for 150,000 steps.

### Relative FLOPs comparison (Table 3)
- **DNABERT-2 (117M, BPE)**: 1.00× FLOPs (baseline).
- **DNABERT 3-mer (86M, overlapping k-mer)**: 3.27× FLOPs.
- **DNABERT 4/5/6-mer**: ~3.25–3.26× FLOPs.
- **NT-500M**: 3.19× FLOPs.
- **NT-2500M**: 19.44× FLOPs.
- FLOPs evaluated on 500-bp input sequences.

### Multi-species vs. human-only pretraining (Tables 3, 4)
- Multi-species models (NT-2500M-multi, DNABERT-2) dominate non-human genome tasks (Epigenetic Marks on yeast, TF on mouse, Covid variant on virus).
- NT-2500M-1000g (human-only, 2537M params, 300B tokens) performs ~on par with DNABERT 3-mer (86M, 122B tokens), demonstrating sample inefficiency of non-overlapping k-mer tokenization.
- Multi-species pretraining does not compromise human genome task performance.

### Further pretraining (DNABERT-2♦, Table 3)
- Additional in-domain MLM on GUE training data (0.41B tokens, negligible overhead).
- Boosts average score from 66.80 → 67.77 (+0.97 absolute).
- Top-2 count increases from 8|4 to 11|10 across 28 datasets.
- Does not uniformly improve all tasks; task-specific further pretraining may be needed.

### Comparison with HyenaDNA and CNN (Table 9, Appendix A.5)
- DNABERT-2 consistently outperforms HyenaDNA (convolutional, long-range) and CNN baselines on all GUE tasks.
- DNABERT-2 without pretraining also included; pretraining provides massive gains (e.g., EMP H3: 57.36 → 78.27).

### Long-sequence extrapolation (Table 5, GUE+)
- DNABERT-2 pretrained on 128-token (~700 bp) sequences, but fine-tuned/evaluated on 5,000–10,000 bp.
- Outperforms NT-2500M-multi on all GUE+ datasets (e.g., EPI: 76.21–92.90 vs. 61.91–86.48).
- DNABERT (6-mer) fails on most EPI datasets due to 512-token input limit.
- Demonstrates ALiBi's extrapolation capability.

### Short-sequence limitation (Section 5.3)
- DNABERT variants (overlapping k-mer) win on Core Promoter Detection (70 bp input) despite overall lower scores.
- BPE compresses 70 bp to ~15 tokens, potentially losing information. Overlapping k-mer retains more info at short lengths despite inefficiency.

## Reported Insights

1. **k-mer tokenization is fundamentally flawed**: Overlapping k-mer leaks masked token information (adjacent tokens reveal the mask); non-overlapping k-mer produces drastically different tokenizations for near-identical sequences (1 bp shift changes all tokens).
2. **BPE is well-suited for genome sequences**: It prevents information leakage, reduces sequence length ~5×, and naturally creates a span-prediction-like MLM objective (since BPE tokens cover variable nucleotide counts).
3. **Vocabulary size matters non-monotonically**: Larger vocab improves compute efficiency but hurts performance due to sparse embedding updates. 4096 is the sweet spot.
4. **Multi-species pretraining is critical**: Models trained on multi-species data excel on cross-species tasks without sacrificing human genome performance.
5. **Efficiency gains are multiplicative**: BPE tokenization (3–4× fewer FLOPs than overlapping k-mer) + smaller model (21× fewer params than NT-2500M) + ALiBi (no input length limit) = comparable SOTA performance at ~92× less GPU cost.
6. **Short sequences remain challenging** for non-overlapping tokenization methods (BPE or non-overlapping k-mer) due to aggressive compression.
7. **Further pretraining on domain data** provides cheap but meaningful gains.

## References Worth Chasing

- DNABERT (Ji et al., 2021) — original genome foundation model using overlapping k-mer tokenization; direct predecessor.
- Nucleotide Transformer (Dalla-Torre et al., 2023) — 500M–2500M param genome FMs with non-overlapping k-mer; main baseline.
- HyenaDNA (Nguyen et al., 2024) — long-range genomic sequence modeling at single nucleotide resolution using convolutions; alternative architecture.
- Geneformer / Transfer learning enables predictions in network biology (Theodoris et al., 2023) — gene network prediction FM.
- ALiBi / Train short, test long (Press et al., 2021, arXiv:2108.12409) — positional bias method enabling length extrapolation.
- FlashAttention (Dao et al., 2022) — IO-aware exact attention; key efficiency component.
- LoRA (Hu et al., 2021) — parameter-efficient fine-tuning; used for large baselines.
- GLU Variants Improve Transformer (Shazeer, 2020) — GEGLU activation used in DNABERT-2.
- SentencePiece (Kudo & Richardson, 2018) — language-independent subword tokenizer framework.
- BPE / Neural machine translation of rare words with subword units (Sennrich et al., 2016) — foundational BPE tokenization paper.
- Effective gene expression prediction from sequence (Avsec et al., 2021) — Enformer; relevant genomics FM.
- RoFormer / Rotary position embedding (Su et al., 2021, arXiv:2104.09864) — alternative positional encoding compared against.
- EN-TEx resource of multi-tissue personal epigenomes (Rozowsky et al., 2023) — variant effect prediction application.

## Notes / Open Questions

1. **No explicit deduplication** of pretraining data described; unclear if the 32.49B bases contain redundancy across species or within genomes.
2. **Tokenizer training corpus** not clearly specified — was BPE trained on the full multi-species dataset or a subset?
3. **Architecture details are sparse**: Number of layers, hidden dimension, attention heads, and FFN dimension are not explicitly stated in the paper. The 117M parameter count and "adapted from BERT" description suggest ~12 layers, ~768 hidden, ~12 heads, but this is not confirmed.
4. **No explicit compute budget** (FLOPs or GPU-hours) is given for DNABERT-2 pretraining itself; the "92× less" claim is relative to NT-2500M-multi and uses an estimated GPU-time method from OpenAI.
5. **GUE benchmark calibration** involved iterative filtering of datasets to achieve "moderate difficulty" — this introduces selection bias and may favor certain model architectures.
6. **Short-sequence performance gap** is acknowledged but not resolved; BPE's ~5× compression may discard positional information critical for sub-100 bp tasks.
7. **LoRA vs. full fine-tuning** comparison is confounded: DNABERT-2 uses full fine-tuning while NT baselines use LoRA. Though preliminary experiments (Table 8) show LoRA slightly outperforms reported NT results, the comparison is not fully apples-to-apples.
8. **No evaluation on variant effect prediction** or other established genomics benchmarks (e.g., CADD, DeepSEA tasks) beyond GUE.
