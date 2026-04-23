---
id: rinalmo-general-purpose-rna-2024
title: 'RiNALMo: General-Purpose RNA Language Models Can Generalize Well on Structure
  Prediction Tasks'
authors:
- Rafael Josip Penić
- Tin Vlašić
- Roland G. Huber
- Yue Wan
- Mile Šikić
year: 2024
venue: null
arxiv: '2403.00043'
doi: null
url: https://arxiv.org/abs/2403.00043v2
pdf_path: papers/rinalmo-general-purpose-rna-2024.pdf
md_path: papers/md/rinalmo-general-purpose-rna-2024.md
modalities:
- rna
status: extracted
evidence_quality: medium
tags:
- rna-language-model
- masked-language-modeling
- secondary-structure
- generalization
- transformer-encoder
parameters: 650M
training_tokens: null
training_compute: 7xA100-80GB-2weeks
references_chased: false
added_at: '2026-04-22T19:36:51+00:00'
updated_at: '2026-04-22T20:25:17+00:00'
---

## TL;DR

650M-parameter BERT-style RNA language model pre-trained with MLM on 36M non-coding RNA sequences. Uses modern architectural improvements (RoPE, SwiGLU, FlashAttention-2). Largest RNA LM at time of publication. Key result: strong inter-family generalization on secondary structure prediction where other DL methods fail. Also SOTA on intra-family secondary structure, multi-species splice-site, and mean ribosome loading prediction.

## Model

- **Architecture**: Encoder-only Transformer (BERT-style), 33 Transformer blocks, 20 attention heads, embedding dim 1280, FFN hidden dim 3413
- **Parameters**: 650M (also trained 150M and 33M variants for ablation)
- **Positional encoding**: Rotary Position Embedding (RoPE) — replaces absolute positional encoding
- **Activation**: SwiGLU (replaces GELU)
- **Attention**: FlashAttention-2 for efficiency
- **Normalization**: Pre-layer norm (inside residual blocks)
- **Tokenization**: Single-nucleotide tokens; U→T replacement; vocabulary includes A/C/T/G + ambiguity codes + special tokens (CLS, EOS, PAD, MASK)
- **Max sequence length**: 1024 tokens during pre-training (longer sequences randomly cropped per epoch; CLS/EOS tokens dropped for cropped sequences to signal cropping)
- **Pre-training objective**: Masked Language Modeling (MLM) — 15% tokens selected; of those 80% masked, 10% random replacement, 10% unchanged

## Data

- **Pre-training corpus**: 36M unique non-coding RNA sequences from RNAcentral, Rfam, nt, and Ensembl databases
- **Preprocessing pipeline**: Remove sequences <16 or >8192 nt → deduplicate with seqkit rmdup → cluster with mmseqs easy-linclust (--min-seq-id 0.7, -c 0.8) → 17M clusters
- **Diversity strategy**: Each training batch samples one sequence per cluster; each epoch sees 17M samples with a new random seed
- **Storage**: LMDB for fast random access
- **Comparison**: RNA-FM used only RNAcentral (23.7M) without clustering; Uni-RNA used 1B sequences but is not publicly available

## Training Recipe

- **Hardware**: 7× A100 80GB GPUs, 2 weeks
- **Batch size**: 192 per GPU (total effective batch ≈1344)
- **LR schedule**: Cosine annealing with linear warm-up; warm-up from 1e-7 to 5e-5 over 2000 steps; min LR 1e-5
- **Gradient clipping**: Norm clipped to 1.0
- **Training tokens**: Not explicitly stated (17M samples/epoch × 1024 max length; exact epoch count not given)

## Key Ablations & Design Choices

- **RoPE vs absolute positional encoding**: Ablation shows RoPE improves downstream performance (details in supplementary)
- **SwiGLU vs GELU**: Ablation shows SwiGLU is more effective (details in supplementary)
- **Model scaling (33M → 150M → 650M)**: Larger models achieve lower perplexity and better downstream performance; scaling clearly helps
- **Cluster-based sampling**: Ensures sequence diversity per batch; contributes to generalization — this is a key design choice differentiating from RNA-FM
- **Cropping signal**: Dropping CLS/EOS for cropped sequences implicitly tells the model the sequence is a fragment — borrowed from ESM
- **Data curation vs raw scale**: 36M curated + clustered sequences outperform approaches using either less data (RNA-FM, 23.7M without clustering) or much more data (Uni-RNA, 1B sequences) — curation quality matters
- **Fine-tuning strategy**: Gradual parameter unfreezing — first train prediction head only, then progressively unfreeze LM layers every 3 epochs
- **Inter-family generalization**: The central finding. DL methods for secondary structure prediction don't generalize across RNA families (Szikszai et al. 2022). RiNALMo overcomes this with pre-trained representations, outperforming thermodynamic methods (RNAstructure, CONTRAfold) on 8/9 families. Only fails on telomerase RNA (longest family; unclear why)

## Reported Insights

- t-SNE of CLS embeddings shows clean clustering by RNA family, confirming structural info is captured in representation
- Telomerase RNA remains a challenge — longest sequences, overlapping embedding cluster with SRP RNA
- RiNALMo generalizes to mRNA tasks (splice-site, MRL) despite pre-training exclusively on ncRNA — representation transfers across RNA types
- Outperforms SpliceBERT (specialized for pre-mRNA) on splice-site prediction, suggesting general pre-training > domain-specific pre-training at sufficient scale
- MRL: Generalizes from random 5'UTR training data to human 5'UTR evaluation

## References Worth Chasing

- **Szikszai et al. 2022** (ref 38): "DL models for RNA secondary structure prediction probably do not generalize across families" — the problem RiNALMo addresses
- **RNA-FM** (Chen et al. 2022, ref 20): Main baseline; 100M params, RNAcentral only
- **Uni-RNA** (Wang et al. 2023, ref 21): 25M–400M params, 1B sequences, not public; reported scaling plateau at 400M
- **ESM-2** (Lin et al. 2023, ref 11): Protein LM that inspires the architecture and cropping strategy
- **SpliceBERT** (Chen et al. 2023, ref 25): Domain-specific RNA LM for splicing

## Notes / Open Questions

- Training token count not explicitly reported; can be estimated as ~17M seqs/epoch × avg_length but total epochs unclear
- Supplementary ablation results (RoPE, SwiGLU, smaller models) referenced but not included in main paper — would be important for a full comparison
- Uni-RNA claimed scaling plateau at 400M params — RiNALMo at 650M contradicts this, suggesting architecture/data quality matter more than raw parameter count
- No comparison with DNA foundation models that could also handle RNA sequences
- Code and weights publicly available at github.com/lbcb-sci/RiNALMo and Zenodo
