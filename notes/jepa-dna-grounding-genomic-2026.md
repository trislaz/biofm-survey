---
id: jepa-dna-grounding-genomic-2026
title: 'JEPA-DNA: Grounding Genomic Foundation Models through Joint-Embedding Predictive
  Architectures'
authors:
- Ariel Larey
- Elay Dahan
- Amit Bleiweiss
- Raizy Kellerman
- Guy Leib
- Omri Nayshool
- Dan Ofer
- Tal Zinger
- Dan Dominissini
- Gideon Rechavi
- Nicole Bussola
- Simon Lee
- Shane O'Connell
- Dung Hoang
- Marissa Wirth
- Alexander W. Charney
- Nati Daniel
- Yoli Shavit
year: 2026
venue: null
arxiv: '2602.17162'
doi: null
url: https://arxiv.org/abs/2602.17162v1
pdf_path: papers/jepa-dna-grounding-genomic-2026.pdf
md_path: papers/md/jepa-dna-grounding-genomic-2026.md
modalities:
- dna
status: extracted
evidence_quality: low
tags:
- jepa
- self-supervised
- representation-learning
- continual-pretraining
- genomic-foundation-model
- vicreg
- linear-probing
- zero-shot
parameters: '117M'
training_tokens: '7.6B bp'
training_compute: '2x NVIDIA GPUs, 5 epochs (FLOPs not reported)'
references_chased: false
added_at: '2026-04-22T19:36:44+00:00'
updated_at: '2026-04-22T20:22:09+00:00'
---

## TL;DR

JEPA-DNA adds a Joint-Embedding Predictive Architecture branch to standard GFM pre-training (MLM or NTP). A context encoder processes masked DNA; an EMA-updated target encoder processes unmasked DNA; a lightweight predictor predicts the target [CLS] latent from the context. Combined loss = MLM/NTP + cosine-similarity JEPA + VICReg variance/covariance regularisation. Tested as continual pre-training on DNABERT-2 (117M). Consistent gains on linear probing (+0.1–6.0% AUROC across GUE & VariantBenchmarks) and zero-shot variant effect prediction (+3–7% AUROC on BEND, TraitGym, ClinVar). First application of JEPA to genomic sequences. Proof-of-concept only: single backbone, no ablations on loss components, no confidence intervals.

## Model

- **Backbone (context encoder Eθ):** DNABERT-2 — 12-layer Transformer Encoder, hidden dim 768, 12 attention heads, ~117M params. BPE tokenisation, 512-token context window.
- **Target encoder (Eθ̄):** Structural duplicate of context encoder; weights updated via EMA of θ (momentum 0.996 → 1.0 over training). Processes full unmasked sequence.
- **Predictor head (Pϕ):** 3-layer Transformer Encoder, reduced latent dim 384, 3 attention heads. Pre-norm architecture, GELU activations, frozen sinusoidal positional embeddings. Input projected from 768→384; output [CLS] projected back 384→768 for loss.
- **Aggregation:** Prepend learnable [CLS] token (encoder-style) or append [EOS] token (decoder/SSM-style). JEPA loss supervises this global token.
- **Architecture-agnostic:** Compatible with Transformer Encoders (MLM), Transformer Decoders (NTP), SSMs, and Long-Convolution backbones (e.g. HyenaDNA).

## Data

- **Pre-training corpus:** Subset of DNABERT-2 training data.
  - Human reference genome GRCh38 + 5 model organisms (mouse, zebrafish, fruitfly, nematode, thale cress).
  - Filtered to valid nucleotides (A/T/C/G), chunked into fixed-length segments with 50% overlap.
  - ~4.76M training sequences, ~7.6B base pairs total.
- **Downstream benchmarks (supervised, linear probing):**
  - GUE: TF binding (100 bp), promoter prediction (300 bp), splice site prediction (400 bp).
  - VariantBenchmarks: coding/non-coding pathogenicity, expression effect, common vs rare, meQTL, sQTL (1024 bp).
  - LRB: causal eQTL (12 000 bp).
- **Downstream benchmarks (zero-shot):**
  - BEND: expression effect, disease variant (512 bp).
  - TraitGym: complex traits, Mendelian traits (4096 bp).
  - Song-Lab ClinVar (5994 bp), LRB pathogenic OMIM (12 000 bp).

## Training Recipe

- **Hardware:** 2× NVIDIA GPUs, DataParallel, FlashAttention.
- **Initialisation:** Both encoders from pre-trained DNABERT-2; predictor from scratch (truncated normal σ=0.02, zero biases).
- **Masking:** Span-based; 1–3 contiguous target regions per sequence, covering 20–40% of sequence length (higher than standard MLM 15%).
- **Multi-phase schedule (continual pre-training):**
  - Phase 1 — Predictor warmup: encoder frozen, 1 000 steps, lr = 1×10⁻⁵ (predictor only).
  - Phase 2 — Full training: encoder unfrozen, linear warmup 500 steps from 3×10⁻⁶ → 5×10⁻⁶, cosine decay to 1×10⁻⁶.
- **Optimiser:** SGD with momentum 0.9, weight decay 0.01, batch size 32, gradient accumulation 4 steps (effective batch 128).
- **Duration:** 5 epochs.
- **EMA schedule:** Momentum 0.996 → 1.0.
- **Total loss:** L_total = λ₁·L_llm + λ₂·L_jepa + λ₃·L_var + λ₄·L_cov.
  - L_llm: standard MLM cross-entropy on masked positions.
  - L_jepa: 1 − cosine_similarity(Pϕ(h_cls), z_target) where z_target = target encoder [CLS].
  - L_var: hinge variance loss (VICReg-style), weight = 25.0, threshold γ = 1.0. Computed in eval mode (no dropout/random masking) on uniform-length batches to avoid spurious variance.
  - L_cov: off-diagonal covariance penalty, weight = 0.5.
- **Downstream linear probing:** Frozen encoder, linear head on [CLS], AdamW lr=3×10⁻⁵, weight decay 0.01, batch 32, 3 epochs. For variant tasks: concat reference + variant [CLS] embeddings.

## Key Ablations & Design Choices (MOST IMPORTANT)

**JEPA vs MLM-only (DNABERT-2 baseline) — Linear probing (AUROC):**

| Task | DNABERT-2 | JEPA-DNA | Δ AUROC |
|---|---|---|---|
| GUE TF Binding | 0.783 | 0.808 | **+3.2%** |
| GUE Promoter | 0.916 | 0.925 | +1.0% |
| GUE Splice Site | 0.623 | 0.653 | **+4.8%** |
| VB Coding Pathogenicity | 0.569 | 0.603 | **+6.0%** |
| VB Non-coding Pathogenicity | 0.590 | 0.593 | +0.5% |
| VB Expression Effect | 0.627 | 0.633 | +1.0% |
| VB meQTL | 0.563 | 0.586 | **+4.1%** |
| VB sQTL | 0.567 | 0.564 | −0.5% |
| LRB Causal eQTL | 0.704 | 0.705 | +0.1% |

**JEPA vs MLM-only — Zero-shot (AUROC):**

| Task | DNABERT-2 | JEPA-DNA | Δ AUROC |
|---|---|---|---|
| BEND Expression Effect | 0.490 | 0.524 | **+6.9%** |
| BEND Disease Variant | 0.498 | 0.512 | ~0 |
| TraitGym Complex | 0.499 | 0.491 | ~0 |
| TraitGym Mendelian | 0.507 | 0.544 | **+7.3%** |
| Song-Lab ClinVar | 0.528 | 0.544 | **+3.0%** |
| LRB Pathogenic OMIM | 0.495 | 0.452 | −8.7% (worse) |

**Key design choices:**
- Span masking (20–40%) vs standard random token masking (15%): authors chose span masking aligned with I-JEPA protocol in vision; no ablation comparing the two.
- Re-masking strategy: predictor receives context encoder outputs but with masked positions replaced by [MASK] embedding, preventing trivial identity mapping.
- Predictor warmup phase (1 000 steps, encoder frozen): prevents early instability; no ablation on its necessity.
- VICReg regularisation (variance weight 25.0, covariance weight 0.5): prevents representation collapse; variance computed in eval mode to avoid dropout/padding artifacts. No ablation on weights.
- SGD (not Adam): notable choice for continual pre-training; no ablation vs Adam.
- **No ablation on individual loss components (L_jepa, L_var, L_cov independently).** Authors acknowledge this as future work.
- **No from-scratch training results** — only continual pre-training on DNABERT-2 shown despite claiming from-scratch capability.
- **No comparison across architectures** — only DNABERT-2 tested despite claiming compatibility with SSMs/decoders.

## Reported Insights

- "Granularity trap": MLM/NTP objectives over-allocate capacity to high-frequency noise (repetitive elements, neutral polymorphisms) and under-represent global functional context.
- JEPA latent prediction forces the model to capture functional semantics invariant to low-level sequence noise.
- Largest zero-shot gains on expression effects (+6.9%) and Mendelian traits (+7.3%) suggest JEPA improves functional variant discrimination.
- sQTL and pathogenic OMIM show no improvement or degradation — possibly tasks requiring fine-grained local syntax rather than global semantics.
- Linear probing results confirm features are more linearly separable with JEPA-DNA, suggesting better-structured representation space.

## References Worth Chasing

- **LLM-JEPA** [14] (Huang, LeCun, Balestriero, 2025): JEPA for natural language — direct inspiration for coupling token recovery with sequence-level latent grounding.
- **GeneJEPA** [8] (Litman et al., 2025): JEPA for single-cell transcriptomics (gene expression vectors) — only prior JEPA in biology, but operates on tabular gene sets not sequences.
- **I-JEPA** [13] (Assran et al., 2023): Original JEPA for vision — source of span masking and EMA target encoder design.
- **VICReg** [15] (Bardes, Ponce, LeCun, 2021): Variance-Invariance-Covariance regularisation framework adopted for collapse prevention.
- **VariantBenchmarks** [23] (Medvedev et al., 2025): Benchmark suite used; also introduces BioToken/BioFM tokenisation.
- **TraitGym** [26] (Benegas, Eraslan, Song, 2025): Zero-shot variant effect benchmark.
- **LRB** [24] (Trop et al., 2025): Long-range genomic benchmark for long-context evaluation.

## Notes / Open Questions

- **Evidence quality is low:** Single backbone (DNABERT-2), no ablations on loss components or hyperparameters, no confidence intervals, no statistical significance tests. Authors explicitly acknowledge all of these as future work.
- **Absolute zero-shot performance is near-random** for most tasks (AUROC ~0.49–0.54), so relative gains may not be practically meaningful.
- **sQTL degradation (−0.5%) and OMIM degradation (−8.7%):** When might global latent grounding hurt? Tasks requiring precise local syntax?
- **SGD choice is unusual** for Transformer continual pre-training — was Adam tested and worse, or just not tried?
- **Predictor architecture under-explored:** 3-layer, 384-dim is just one design point; no sweep reported.
- **How do loss weights (λ₁–λ₄) interact?** Variance weight is 50× covariance weight — is this critical?
- **From-scratch training gap:** Paper claims JEPA-DNA works from scratch but shows zero from-scratch results.
- **Multi-architecture gap:** Claims compatibility with SSMs/decoders but only tests Transformer Encoder.
- NVIDIA affiliations (first authors) — may see follow-up at scale with more architectures.
