---
id: dnabert-pre-trained-bidirectional-2021
title: 'DNABERT: pre-trained Bidirectional Encoder Representations from Transformers
  model for DNA-language in genome'
authors:
- Yanrong Ji
- Zhihan Zhou
- Han Liu
- Ramana V Davuluri
year: 2021
venue: Bioinformatics
arxiv: null
doi: 10.1093/bioinformatics/btab083
url: https://doi.org/10.1093/bioinformatics/btab083
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/dnabert-pre-trained-bidirectional-2021.md
modalities:
- dna
status: extracted
evidence_quality: abstract+repo
tags: ["mlm", "k-mer-tokenization", "6-mer", "overlapping-k-mer", "bert-base", "human-genome", "attention-visualization", "motif-discovery", "snp-analysis"]
parameters: 110000000
training_tokens: 122000000000
training_compute: null
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

DNABERT is the first BERT-style pre-trained foundation model for DNA sequences, treating genomic sequences as a natural language by tokenizing them into overlapping k-mers. It uses a standard BERT-base architecture (12 layers, 768 hidden, 12 heads, ~86–89M params depending on k) pre-trained with masked language modeling on the human reference genome (GRCh38, 2.75B nucleotide bases). Four variants (k=3,4,5,6) are provided. DNABERT demonstrates strong transfer to promoter prediction, transcription factor binding site prediction, and splice site prediction, and introduces attention-based visualization for motif discovery and SNP effect analysis.

## Model

- **Architecture**: BERT-base (BertForMaskedLM). Same hidden dimensions across all k-mer variants.
  - Hidden size: 768
  - Attention heads: 12
  - Layers: 12
  - FFN intermediate size: 3072
  - Max position embeddings: 512
  - Activation: GELU
  - Dropout: 0.1 (attention & hidden)
- **Parameters**: ~86M (k=3,4), ~87M (k=5), ~89M (k=6). Differences are entirely due to vocabulary/embedding size.
- **Tokenizer**: Overlapping k-mer with stride 1. For a sequence of length L, produces L−k+1 tokens. Vocabulary sizes: 69 (k=3, = 4³+5 special), 261 (k=4), 1029 (k=5), 4101 (k=6, = 4⁶+5 special).
- **Context length**: 512 k-mer tokens (≈512+k−1 nucleotides, e.g. 517 bp for k=6).
- **Positional encoding**: Learned positional embeddings (standard BERT).
- **Variants released**: DNABERT-3, DNABERT-4, DNABERT-5, DNABERT-6 (on HuggingFace as zhihan1996/DNA_bert_{3,4,5,6}).

## Data

- **Pre-training data**: Human reference genome GRCh38/hg38 only, comprising 2.75B nucleotide bases. Sequences with N removed; only A, T, C, G retained.
- **Training tokens**: ~122B tokens (reported by DNABERT-2 paper, Table 3; consistent across all k-mer variants since overlapping tokenization yields ≈L tokens per sequence regardless of k).
- **Downstream tasks** (from repo and DNABERT-2 benchmark):
  - Promoter prediction (core promoter detection, 70 bp; promoter detection, 300 bp)
  - Transcription factor binding site prediction (100 bp, human)
  - Splice site prediction (400 bp)
- **No multi-species data**: Pre-training is human-only. DNABERT-2 later showed multi-species pre-training is critical for cross-species generalization.

## Training Recipe

- **Objective**: Masked Language Modeling (MLM). Contiguous span masking of k tokens to mitigate information leakage from overlapping k-mers. Mask probability: 0.025 (per the repo sample script; low because spans are masked, not individual tokens).
- **Optimizer**: Adam with β₁=0.9, β₂=0.98, ε=1e-6, weight decay=0.01.
- **Learning rate**: 4e-4 with 10,000 warmup steps.
- **Batch size**: Effective batch ~2000 (8 GPUs × 10 per-GPU batch × 25 gradient accumulation steps).
- **Sequence length**: 512 k-mer tokens (block_size=512).
- **Total steps**: 200,000.
- **Hardware**: 8× NVIDIA GeForce RTX 2080 Ti (11 GB each). Distributed training.
- **Mixed precision**: Optional fp16 via NVIDIA Apex.
- **Codebase**: Extended from HuggingFace Transformers, adapted for DNA.
- **Fine-tuning recipe** (from repo): lr=2e-4, 5 epochs, batch size 32, warmup 10%, hidden dropout 0.1, weight decay 0.01.

## Key Ablations & Design Choices

### k-mer length comparison (k=3,4,5,6)
- Four model variants trained with identical architecture except vocabulary size.
- On the GUE benchmark (reported in DNABERT-2 paper, Table 3): DNABERT-3 performs best (61.62 avg), followed by DNABERT-6 (60.51), DNABERT-4 (61.14), DNABERT-5 (60.05).
- DNABERT-6 is the most commonly used variant in practice (highest HuggingFace downloads: ~70K/month).
- Trade-off: larger k → richer per-token context but larger vocabulary, more redundancy in overlapping tokens, and more information leakage in MLM.

### Overlapping k-mer tokenization
- Stride-1 sliding window produces L−k+1 tokens from a length-L sequence. Adjacent tokens share k−1 characters.
- **Information leakage problem**: In MLM, adjacent unmasked tokens can entirely or partially reveal a masked token. To mitigate this, DNABERT masks contiguous spans of k tokens rather than random individual tokens.
- **Computational cost**: Tokenized sequence is nearly as long as the raw nucleotide sequence (no compression), leading to ~3.25× more FLOPs than BPE-based methods (DNABERT-2, Table 3).
- DNABERT-2 later showed BPE tokenization wins on 21/28 GUE datasets over 6-mer with a +4.41 absolute score improvement.

### Attention visualization for motif discovery
- Attention scores from the fine-tuned model are used to identify important nucleotide positions.
- Attention-highlighted regions align with known transcription factor binding motifs.
- Provides interpretability via attention-based motif analysis (with code for generating WebLogo plots).

### SNP / genomic variant analysis
- Mutation effect prediction by comparing model predictions before and after nucleotide substitution.
- Outputs mutation effect scores (difference and log odds ratio) for each variant.

## Reported Insights

1. **DNA can be modeled as natural language**: Treating k-mers as "words" and genome sequences as "sentences" enables transfer of NLP pre-training to genomics.
2. **Pre-training transfers well across tasks**: A single pre-trained DNABERT model fine-tunes effectively for promoter prediction, TF binding, and splice site prediction.
3. **Attention captures biological motifs**: Attention weights in fine-tuned models highlight known TF binding motifs, providing interpretability.
4. **k-mer choice matters but no single k dominates**: Different k values suit different downstream tasks; k=3 slightly best overall on GUE but k=6 is most popular in practice.
5. **Overlapping k-mer tokenization has fundamental drawbacks** (identified retrospectively by DNABERT-2): information leakage during MLM and computational inefficiency from near-zero sequence compression.

## References Worth Chasing

- DNABERT-2 (Zhou et al., 2023, arXiv:2306.15006) — successor replacing k-mer with BPE; 117M params; introduces GUE benchmark; accepted at ICLR 2024.
- Nucleotide Transformer (Dalla-Torre et al., 2023, arXiv:2301.11270) — 500M–2.5B param genome FMs with non-overlapping k-mer tokenization.
- HyenaDNA (Nguyen et al., 2023, arXiv:2306.15794) — sub-quadratic long-range genomic model at single-nucleotide resolution.
- BERT (Devlin et al., 2019) — original BERT architecture that DNABERT adapts.
- Enformer (Avsec et al., 2021, doi:10.1038/s41592-021-01252-x) — gene expression prediction from sequence with long-range context.
- Caduceus (Schiff et al., 2024) — bidirectional equivariant Mamba-based DNA model.
- VQDNA (Hao et al., 2024) — vector-quantized DNA tokenization approach.

## Notes / Open Questions

1. **Abstract-only source quality**: The full paper text was behind a paywall (403 from OUP). Details above are sourced from the GitHub repo (config files, training scripts, README) and the DNABERT-2 paper's comparison tables.
2. **Training token count (122B)** is taken from DNABERT-2 Table 3. The repo sample script suggests ~204.8B tokens (2000 batch × 512 seq × 200K steps), but actual training may have used different hyperparameters.
3. **No multi-species pre-training**: Human genome only (2.75B bases). DNABERT-2 showed this limits cross-species generalization.
4. **Low mask ratio (2.5%)**: The repo script uses mlm_probability=0.025 instead of the typical 15%, likely compensating for span masking of k contiguous tokens.
5. **512-token context limit**: Learned positional embeddings restrict maximum input length; DNABERT-XL (concatenating predictions from overlapping windows) was a crude workaround. DNABERT-2 solved this with ALiBi.
6. **Parameter count inconsistency**: The DNABERT-2 paper reports 86–89M depending on k; other sources (HyenaDNA) cite ~110M. The config files confirm BERT-base dimensions (12L/768H/12A/3072I), which yields ~86M non-embedding params + embedding params that vary by vocab size. The 110M figure may include all parameters or may be rounded.
7. **No standardized benchmark at the time**: Downstream evaluation used custom task-specific datasets; the GUE benchmark was only introduced with DNABERT-2.
8. **Widely adopted despite limitations**: DNABERT-6 has ~70K monthly HuggingFace downloads as of 2025, indicating continued community use despite known tokenization drawbacks.
