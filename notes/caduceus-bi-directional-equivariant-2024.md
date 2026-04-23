---
id: caduceus-bi-directional-equivariant-2024
title: 'Caduceus: Bi-Directional Equivariant Long-Range DNA Sequence Modeling'
authors:
- Yair Schiff
- Chia-Hsiang Kao
- Aaron Gokaslan
- Tri Dao
- Albert Gu
- Volodymyr Kuleshov
year: 2024
venue: null
arxiv: '2403.03234'
doi: null
url: https://arxiv.org/abs/2403.03234v2
pdf_path: papers/caduceus-bi-directional-equivariant-2024.pdf
md_path: papers/md/caduceus-bi-directional-equivariant-2024.md
modalities:
- dna
status: extracted
evidence_quality: full-text
tags:
- mamba
- ssm
- rc-equivariant
- bidirectional
- long-context
- dna-language-model
- variant-effect-prediction
parameters: 1.9M (Caduceus-PS/Ph); range 470k–1.9M across configs
training_tokens: ~35B nucleotide tokens (HG38 human reference genome)
training_compute: null
references_chased: false
added_at: '2026-04-22T19:58:54+00:00'
updated_at: '2026-04-22T20:02:47+00:00'
is_fm: true
fm_classification_reason: 'Caduceus: pretrained long-range DNA FM.'
---

## TL;DR

Caduceus is the first family of **RC-equivariant, bi-directional, long-range DNA language models** built on the Mamba (selective SSM) backbone. Two architectural innovations — **BiMamba** (parameter-efficient bidirectional Mamba) and **MambaDNA** (RC-equivariant Mamba via channel-split + shared weights) — are combined with equivariant embedding and LM head layers. Despite having only ~1.9M parameters, Caduceus matches or outperforms Transformer-based DNA models with 100–500M parameters on downstream tasks, especially long-range variant effect prediction (VEP) where it beats 10× larger models. Two variants are offered: Caduceus-PS (parameter sharing for full RC equivariance throughout training) and Caduceus-Ph (post-hoc RC conjoining at inference only).

## Model

- **Backbone**: Mamba (selective SSM with input-dependent B, C, Δ; associative-scan parallel training).
- **BiMamba**: Bidirectional extension of Mamba — runs forward + reversed copy with *shared* projection weights (in-proj, out-proj); outputs are flipped and summed. No parameter overhead vs. unidirectional.
- **MambaDNA**: Wraps a (Bi)Mamba block with RC equivariance. Input is channel-split in half; one half is RC-transformed; both halves pass through the *same* Mamba; RC is applied again to the second half before concatenation. Proven RC-equivariant (Theorem 3.1).
- **Caduceus-PS**: Stack of MambaDNA(BiMamba) blocks + RC-equivariant token embedding + RC-equivariant LM head. Full RC equivariance throughout forward pass (Theorem 4.1). Trained with MLM; no RC data augmentation needed.
- **Caduceus-Ph**: Stack of BiMamba blocks (no MambaDNA wrapper). RC equivariance achieved via RC data augmentation during pretraining + post-hoc conjoining (average forward & RC predictions) at inference.
- Character-level (single nucleotide) tokenization; vocabulary = {A, C, G, T, MASK}.
- Largest config: 16 layers, hidden dim 256, seq len 131k → ~1.9M params.

## Data

- **Pre-training**: Human reference genome HG38 (GRCh37/38). Training split = 34,021 segments extended to max 1,048,576 (2²⁰) bp, totaling ~35B nucleotide tokens.
- **Downstream benchmarks**:
  1. Genomics Benchmarks (8 regulatory element classification tasks, 200–2k bp).
  2. Nucleotide Transformer tasks (18 datasets: histone markers, regulatory annotation, splice sites).
  3. Variant Effect Prediction (VEP) — SNP effect on gene expression, stratified by distance to nearest TSS (0–30k, 30–100k, >100k bp).

## Training Recipe

- **Objective**: MLM (BERT-style: 15% masked — 80% [MASK], 10% random, 10% unchanged). Caduceus-Ph also uses RC data augmentation; Caduceus-PS does not (equivariance is built-in).
- **Optimizer**: Adam with β₁=0.95, β₂=0.9; cosine LR decay; LR = 8e-3.
- **Batch**: Constant token budget per batch = 2²⁰ tokens (e.g., batch 1024 × seqlen 1k, or batch 8 × seqlen 131k).
- **Schedule**: 10K gradient updates for 1k & 32k seqlen; 50K updates for 131k seqlen.
- **Fine-tuning**: Mean-pooled final hidden state → task head. Early stopping on validation metric. 5-fold or 10-fold CV depending on benchmark.
- **VEP**: Frozen embeddings (1536 bp window around SNP) → SVM with RBF kernel.
- **Hardware**: Mix of 3090, A5000, A6000, V100, A100 GPUs (no specific compute budget reported).

## Key Ablations & Design Choices

1. **Mamba vs. Hyena (NTP pre-training)**: Mamba achieves lower cross-entropy loss than HyenaDNA at comparable model size and sequence length across 1k, 32k, and 131k contexts (Fig. 3a). Mamba is also more robust to higher learning rates.
2. **BiMamba weight-sharing vs. naive bidirectional**: Sharing projection weights allows 2× depth at same param count. Deeper tied models consistently achieve better MLM loss than shallower untied ones (Fig. 3b).
3. **RC equivariance improves pre-training**: RC-equivariant LM (Caduceus-PS) achieves better MLM loss than non-equivariant BiMamba across all sequence lengths (Fig. 3c).
4. **Genomics Benchmarks (Table 1, ~470k params)**: Caduceus-Ph is best on 5/8 tasks; Caduceus-PS best on 2/8. Both consistently beat Mamba (unidirectional) and HyenaDNA baselines. E.g., Human Enhancer Ensembl: Caduceus-PS 0.900 vs. HyenaDNA 0.849.
5. **Nucleotide Transformer tasks (Table 2, 1.9M params)**: Caduceus-Ph (<2M params) beats Enformer (252M), DNABERT-2 (117M), and NT-v2 (500M) on 8/18 tasks. Outperforms similarly-sized HyenaDNA (1.6M) on nearly all histone & regulatory annotation tasks. HyenaDNA slightly better on splice sites.
6. **VEP long-range (Fig. 4)**: Caduceus-PS (1.9M) outperforms NT-v2 (500M) and even Enformer (252M, supervised) at TSS distances >100k bp. The advantage grows with distance to TSS, demonstrating the value of bidirectionality + RC equivariance for long-range tasks.
7. **PS vs. Ph**: Post-hoc conjoining (Ph) often matches or beats parameter-sharing (PS) on short-range tasks (consistent with Zhou et al. 2021), but PS excels on long-range VEP. Both consistently outperform the ablation "Caduceus w/o equiv."

## Reported Insights

- RC equivariance is a powerful inductive bias for DNA modeling — it improves both pre-training loss and downstream performance without adding parameters.
- Bidirectionality is critical for genomic tasks where both upstream and downstream context matter; MLM pre-training (vs. NTP) naturally leverages this.
- Mamba's selective SSM is strictly better than Hyena as a sequence backbone for genomic LMs (lower loss, more robust to hyperparameters).
- Character-level tokenization is preferred over k-mer schemes because k-mer tokenization is fragile to single-nucleotide changes (important for VEP).
- Pre-trained DNA LMs implicitly learn evolutionary conservation signals, making them strong unsupervised variant effect predictors via embedding extraction + simple classifiers (SVM).
- The advantage of Caduceus over larger Transformer models is most pronounced on long-range tasks (>100k bp), exactly where quadratic attention scaling becomes prohibitive.

## References Worth Chasing

- Mamba: Linear-Time Sequence Modeling with Selective State Spaces (arXiv:2312.00752) — core SSM backbone
- HyenaDNA: Long-Range Genomic Sequence Modeling at Single Nucleotide Resolution (Nguyen et al., 2023) — main SSM-based DNA LM baseline
- The Nucleotide Transformer: Building and Evaluating Robust Foundation Models for Human Genomics (Dalla-Torre et al., 2023, bioRxiv 2023-01) — Transformer DNA FM, benchmark source
- Effective Gene Expression Prediction from Sequence by Integrating Long-Range Interactions (Avsec et al., 2021, Nature Methods) — Enformer, VEP dataset source
- DNABERT-2: Efficient Foundation Model and Benchmark for Multi-Species Genome (Zhou et al., 2023) — Transformer DNA LM with BPE tokenization
- DNABERT: Pre-trained Bidirectional Encoder Representations from Transformers Model for DNA-Language in Genome (Ji et al., 2021) — early k-mer Transformer DNA LM
- DNA Language Models Are Powerful Predictors of Genome-Wide Variant Effects (Benegas et al., 2023b, PNAS) — GPN, unsupervised VEP via DNA LMs
- Reverse-Complement Equivariant Networks for DNA Sequences (Zhou et al., 2021) — RC parameter sharing & post-hoc conjoining foundations
- Technical Note on Reverse-Complement Equivariance (Mallet & Vert, 2021) — group-theoretic formalization of RC equivariance
- Learning Important Features Through Propagating Activation Differences (Shrikumar et al., 2017) — RC parameter sharing for convolutions (DeepLIFT)
- GENA-LM: A Family of Open-Source Foundational Models for Long DNA Sequences (Fishman et al., 2023, bioRxiv) — BigBird-based DNA LM scaling context
- Efficiently Modeling Long Sequences with Structured State Spaces — S4 (Gu et al., 2021a, arXiv:2111.00396) — foundational SSM work
- BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding (Devlin et al., 2018, arXiv:1810.04805) — MLM pre-training recipe adopted
- Hungry Hungry Hippos: Towards Language Modeling with State Space Models (Dao et al., 2022, arXiv:2212.14052) — H3 SSM architecture

## Notes / Open Questions

- **No multi-species pretraining**: Caduceus is trained only on HG38 human genome. Multi-species pretraining (as in NT-v2) could boost conservation-aware representations.
- **Scale ceiling unclear**: Largest model is only 1.9M params / 16 layers. How do BiMamba/MambaDNA scale to 100M+ parameters? Do the gains from RC equivariance persist at scale?
- **No RNA or protein tasks**: Modality is strictly DNA. Could MambaDNA-style equivariance be extended to RNA secondary structure or other modalities?
- **Compute not reported**: Training budget (GPU-hours) is not disclosed, making cost-efficiency comparisons difficult.
- **Post-hoc conjoining vs. parameter sharing**: Ph often wins on short-range tasks, PS wins on long-range. The paper does not deeply analyze *why* — is this an optimization issue (PS doubles hidden dim, complicating training) or a fundamental architectural trade-off?
- **VEP evaluation uses frozen embeddings + SVM**: End-to-end fine-tuning on VEP is not explored. Would Caduceus still dominate with gradient-based fine-tuning on long-range VEP?
- **Comparison fairness**: Caduceus uses 131k context for VEP while NT-v2 uses only 12k (its training context). A fairer comparison would require retraining NT-v2 at longer contexts.
- **Concurrent work**: Zhu et al. (2024) independently proposed bidirectional Mamba — comparison not provided.

## Ablations (Rev 4)

The paper does not use the word "ablation" but presents several controlled architecture-variant comparisons (§5.1 "Effect of …" and the `Caduceus w/o Equiv.` column in Table 1). Below are all such comparisons.

| # | Variable ablated | Settings compared | Metric / Dataset | Key results | Conclusion |
|---|------------------|-------------------|------------------|-------------|------------|
| 1 | Inner sequence-mixer backbone | **Mamba** vs **HyenaDNA** (same param budget, MLM pre-training, seq lengths 1k → 131k) | MLM cross-entropy on HG38 (Fig 3a) | Mamba achieves strictly lower CE than HyenaDNA at every sequence length tested | Use Mamba (selective SSM) as the inner block; it scales better with context than implicit-conv Hyena. |
| 2 | How to make Mamba bi-directional | **BiMamba w/ parameter sharing** (Eq. 4, weight-tied fwd/RC projections, deeper) vs **naive bi-Mamba** (independent fwd + reverse Mamba modules, half depth, same params) | MLM CE on HG38, seq lengths 1k → 131k (Fig 3b) | Weight-tied/deeper BiMamba reaches lower pre-training loss across all lengths | Parameter sharing buys depth at fixed param count and outperforms the naive 2-module bidirectional design. |
| 3 | Reverse-complement equivariance in the LM | **RC-equivariant Caduceus-PS** vs **non-equivariant** (BiMamba only) | MLM CE on HG38, seq lengths 1k → 131k (Fig 3c) | Equivariant variant has lower MLM loss at every length | RC equivariance is a useful architectural prior even at pre-training, not just downstream. |
| 4 | RC-equivariance mechanism on downstream classification | **Caduceus w/o Equiv.** vs **Caduceus-Ph** (post-hoc conjoining, RC data aug.) vs **Caduceus-PS** (parameter sharing) — all ≈470k params, 4 layers | Top-1 accuracy on 8 Genomics Benchmark tasks (Table 1, 5-fold CV) | Caduceus-Ph or -PS wins all 8 tasks vs w/o Equiv. Examples: Human Enhancer Ensembl 0.883 → 0.893 (Ph) / 0.900 (PS); Mouse Enhancers 0.770 → 0.793 (PS); Human Regulatory 0.872 → 0.881 (Ph) | RC equivariance — whether built-in (PS) or post-hoc (Ph) — is the dominant factor on short/medium-range classification. |
| 5 | Built-in vs post-hoc RC equivariance | **Caduceus-PS** (parameter sharing during training+inference) vs **Caduceus-Ph** (BiMamba + RC data-aug at training, average fwd+RC at inference) | Genomics Benchmark (Table 1) and Nucleotide Transformer 18 tasks (Table 2) | Ph wins more Genomics Benchmark tasks (5/8 ties or wins); on NT both are competitive with the 500M Nucleotide Transformer-v2 at <0.5% of its params | Ph is a surprisingly strong, simpler baseline; PS is preferable when the downstream task itself depends on RC symmetry. |
| 6 | Sequence range / RC equivariance for long-range VEP | **Caduceus-PS / -Ph / w/o Equiv. (131k bp ctx)** vs **HyenaDNA (160k)**, **NT-v2 500M (12k)**, **Enformer (196k)** — frozen embeddings + RBF-SVM, stratified by distance to nearest TSS | AUROC on Avsec et al. variant-effect-on-expression task, 3 strata: 0–30k, 30–100k, >100k bp (Fig 4, Table 7) | Caduceus-PS leads at >100k bp, surpassing NT-v2 (≈250× larger) and Enformer; gap to non-equivariant Caduceus widens with TSS distance | RC-equivariant parameter sharing is the decisive ingredient for long-range variant effect prediction; advantage over non-equivariant SSM grows with range. |
| 7 | RC data augmentation for HyenaDNA pre-training (per-task baseline tuning) | RC aug. **on** vs **off** during HyenaDNA pre-training, picked per Genomics Benchmark task (Table 4) | Top-1 accuracy, 5-fold CV | Best setting splits 4–4 across the 8 tasks (e.g., Human-vs-Worm prefers RC aug; Mouse Enhancers prefers no aug) | RC data augmentation alone is task-dependent and brittle — motivates a built-in equivariant inductive bias instead. |

### Design take-aways from the ablations
- **Mamba > Hyena** as the inner DNA sequence mixer at matched parameter count (ablation 1).
- **Weight-tied BiMamba > naive bidirectional Mamba** — share parameters and spend the saved capacity on depth (ablation 2).
- **RC equivariance helps even at pre-training**, not just on downstream RC-symmetric tasks (ablation 3).
- **Either flavor of RC equivariance (PS or Ph) beats no equivariance** on every Genomics Benchmark task (ablation 4); post-hoc Ph is a strong, cheaper baseline (ablation 5).
- **Parameter-sharing PS dominates at long range**: at >100k bp from the TSS for variant-effect prediction, Caduceus-PS beats Enformer and the 500M NT-v2 despite being orders of magnitude smaller (ablation 6).
- **RC data augmentation alone is unreliable** and task-specific; an equivariant architecture removes that hyperparameter (ablation 7).
