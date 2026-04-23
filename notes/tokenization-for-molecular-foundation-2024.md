---
id: tokenization-for-molecular-foundation-2024
title: Tokenization for Molecular Foundation Models
authors:
- Alexius Wadell
- Anoushka Bhutani
- Venkatasubramanian Viswanathan
year: 2024
venue: null
arxiv: '2409.15370'
doi: null
url: https://arxiv.org/abs/2409.15370v3
pdf_path: papers/tokenization-for-molecular-foundation-2024.pdf
md_path: papers/md/tokenization-for-molecular-foundation-2024.md
modalities:
- small-molecule
status: extracted
evidence_quality: high
tags:
- tokenization
- ablation
- smiles
- selfies
- n-gram-proxy
- open-vocabulary
- cheminformatics
parameters: 25M  # per encoder (excl. embeddings); 18 RoBERTa variants trained
training_tokens: ~245M molecules (30k steps × batch 8192) for each encoder; 1.6B SMILES for n-gram models
training_compute: 2×A100 per pretrain; 1×A40 per finetune
references_chased: false
added_at: '2026-04-22T19:42:21+00:00'
updated_at: '2026-04-22T20:26:47+00:00'
---

## TL;DR

Systematic evaluation of 34 tokenizers (19 chemistry-specific) for molecular foundation models on SMILES representations. Proposes two new tokenizers—Smirk (character-level over OpenSMILES glyphs, 165 tokens, 100% coverage) and Smirk-GPE (BPE on top of Smirk, ~2.3k tokens)—and validates them with 18 RoBERTa encoders and n-gram proxy models. Key finding: existing Atom-wise tokenizers have large coverage gaps (UNK freq up to ~50% on tmQM); Smirk/Smirk-GPE eliminate UNK tokens with negligible quality cost and gains on harder tasks. N-gram cross-entropy is a reliable low-cost proxy for transformer downstream performance (ρ = 0.67–0.80 rank correlation across 6 MoleculeNet/tmQM tasks).

## Model

- **Architecture**: RoBERTa-PreLayerNorm (encoder-only), 8 layers, 8 attention heads, hidden 512, intermediate 2048, max seq len 2048.
- **Parameters**: ~25M per model (excluding embeddings).
- **Objective**: Masked Language Modeling (MLM).
- **N-gram proxy**: 1- to 5-gram models with add-one smoothing; bidirectional variant using joint preceding/succeeding context (2n−2 total context).
- **Number of models trained**: 18 RoBERTa encoders (11 tokenizers × 3 molecular encodings: canonical SMILES, SMILES, SELFIES; not all combinations).

## Data

- **Pretraining**: Enamine REAL Space — >50B synthetically accessible molecules; used ~262M molecules for Smirk-GPE training; pretrain split 80/10/10.
- **Downstream**: MoleculeNet (6 regression + 7 classification tasks) and tmQM (108k transition-metal complexes). tmQM has richer bracketed-atom diversity (elements, chirality).
- **N-gram training corpus**: 1.6B SMILES from REAL Space.

## Training Recipe

- **Pretrain**: 30,000 steps, effective batch size 8192, 2×A100 GPUs. LR = 1.6×10⁻⁴ (FusedLamb optimizer). Validation CE every 12 steps on 98,304 molecules. Total ~245M molecules seen.
- **Finetune**: 100,000 steps, effective batch size 128, 1×A40 GPU. AdamW, LR = 1.6×10⁻⁴. Two-layer task head on CLS embedding. Convergence typically before 100k steps (except QM9). Checkpoint selection: lowest validation loss.
- **Molecular encoding**: canonical SMILES (via RDKit) or SELFIES, generated on-the-fly; transcoding failures backfilled.

## Key Ablations & Design Choices

### Tokenizer coverage (34 tokenizers benchmarked)

| Tokenizer class | # evaluated | OpenSMILES coverage | UNK freq (MoleculeNet) | UNK freq (tmQM) |
|---|---|---|---|---|
| Smirk | 2 | 100% | 0% | 0% |
| Smirk-GPE | 2 | 100% | 0% | 0% |
| NLP (GPT-4o, LLaMA, Gemma, etc.) | 10 | 100% (by construction) | 0% | 0% |
| ChemBERTa (BPE) | 1 | 100% | 0% | 0% |
| TransPolymer (RoBERTa BPE) | 1 | 100% | 0% | 0% |
| Atom-wise (MoLFormer, SMI-TED, MolGPT, etc.) | 9 | partial (<3k vocab) | non-negligible | non-negligible |
| SPE / APE | 3 | partial | 18.9% | ~50% |
| SELFormer / ReactionT5 | 2 | incomplete (missing U/u) | non-negligible | non-negligible |

- Atom-wise tokenizers would need >28 trillion tokens for full OpenSMILES coverage; current ones have <3k tokens.

### Intrinsic tokenizer metrics (fertility, imbalance D, normalized entropy η, UNK frequency)

- **Fertility**: Smirk has higher fertility (longer sequences) than Atom-wise due to decomposing bracketed atoms (≥2 extra tokens per bracket). Smirk-GPE compresses back. SPE/APE have lowest fertility.
- **Normalized entropy (η)**: SPE/APE score highest (~good). NLP BPE tokenizers score poorly (η ≈ 25%). Chemistry-specific tokenizers cluster similarly (~50%).
- **Imbalance (D)**: All schemes ≈ 50%, except Smirk-GPE on tmQM (merges learned on REAL Space did not generalise).
- **UNK frequency**: Discriminating metric. All closed-vocabulary chemistry tokenizers emit UNK at non-negligible rates. Smirk, Smirk-GPE, and NLP tokenizers: 0%.

### N-gram cross-entropy as proxy for transformer performance

- N-gram cross-entropy and information loss are **linearly predictive** of downstream transformer performance.
- Spearman rank correlations (ρ) between n-gram estimates and transformer metrics:
  - tmQM MAE: ρ = 0.786 (R² = 0.335)
  - QM9 MAE: ρ = 0.667 (R² = 0.783)
  - Lipophilicity RMSE: ρ = 0.800 (R² = 0.741)
  - HIV AUROC: ρ = 0.750 (R² = 0.758)
  - ToxCast AUROC: ρ = 0.700 (R² = 0.654)
  - ClinTox AUROC: ρ = 0.800 (R² = 0.577)
- Finetuned n-gram variant reduced effect-size variance but did not shift expectation.

### Tokenizer effect sizes on downstream tasks (fixed-effects model, relative to Atom-wise + SMILES baseline)

- **SPE/APE**: Negative effect on both pretraining CE and downstream tasks. High intrinsic metric scores are misleading because of coverage gaps.
- **Smirk**: Positive effect on pretraining CE and tmQM downstream performance; similar to Atom-wise on MoleculeNet tasks.
- **Smirk-GPE**: Similar direction to Smirk; compresses sequences, mitigating fertility regression.
- **SELFIES encoding**: Choice of molecular encoding (SMILES vs SELFIES) had negligible impact on downstream performance. 54% of tmQM molecules could not be transcoded to SELFIES (enhanced stereochemistry).
- **BPE (NLP-style)**: On par with chemistry-specific tokenizers for downstream quality, with advantage of zero UNK tokens.

### Information loss from UNK tokens (KL-divergence analysis)

- MoLFormer: 0.1 nats/molecule info loss on MoleculeNet, but **40.3 nats/molecule on tmQM**.
- Open-vocabulary tokenizers (Smirk, Smirk-GPE, NLP) mitigate this degradation across both datasets.
- Tokenizers with robust dataset coverage: information loss minimal. Limited coverage → substantial losses, especially on chemically diverse datasets (tmQM).

### Smirk-GPE vocabulary training

- Trained on 262M molecules from REAL Space; target 50k tokens but training halted at **2.3k tokens** after exhausting all possible merges.
- Variant Smirk-GPE (NMB) excluded bracket merges; similar results.
- Impact of vocabulary size and corpus size not explored.

### Ambiguity issues in existing tokenizers

- ChemBERTa conflates Sc (sulfur-carbon bond) with [Sc] (scandium); similarly [Cn] (copernicium) vs Cn. >500k occurrences of this ambiguity in PubChem.
- OH in [OH] (oxygen-hydrogen) vs [C@OH1] (octahedral chiral center) conflated by BPE tokenizers.

## Reported Insights

1. Open-vocabulary tokenization is essential for robust molecular FMs; closed-vocabulary chemistry-specific tokenizers inadvertently obscure atom-level information.
2. N-gram models are a valid, low-cost proxy for evaluating tokenizer impact—directionally consistent with transformer pretraining and downstream effects.
3. Intrinsic metrics (fertility, η, D) fail to capture coverage issues; UNK frequency is the most discriminating intrinsic metric.
4. Current benchmarks (MoleculeNet) lack chemical diversity; tmQM partially addresses this but more diverse benchmarks are needed (isotopes, charged species, quadruple bonds).
5. Chemistry-specific tokenizers may yield more robust models (lower cross-entropy generalisation gap) but not necessarily higher quality on current benchmarks.
6. Smirk improves interpretability by exposing bracketed-atom sub-structure to attention maps.

## References Worth Chasing

- Li & Fourches 2021 — SMILES Pair Encoding (SPE) (ref 40)
- Leon et al. 2024 — Atom Pair Encoding (APE), comparing SMILES vs SELFIES tokenization (ref 41)
- Goldman et al. 2024 — Unpacking Tokenization; correlation of compression and model performance (ref 46)
- Lindsey et al. 2024 — Tokenizer choice in genomic models (attention + state-space) (ref 51)
- Chithrananda et al. 2020 — ChemBERTa; Atom-wise vs BPE on ToxCast (ref 17)
- Ross et al. 2022 — MoLFormer (ref 16)
- Soares et al. 2024 — SMI-TED large encoder-decoder family (ref 13)

## Notes / Open Questions

- The paper focuses on encoder-only (RoBERTa) models; results may differ for decoder-only or encoder-decoder architectures.
- Smirk-GPE merges did not generalise from REAL Space to tmQM (imbalance spike); transfer of learned merges across chemical domains is an open question.
- Only 30k pretrain steps with batch 8192 (~245M molecules); this is a small-scale regime. Scaling behaviour of tokenizer choice is unexplored.
- The sole UNK token for Smirk across 2.1B molecules was [te] (invalid per OpenSMILES, present in HIV dataset)—practical coverage is near-perfect.
- No exploration of tokenizer impact on generative (decoder) models or molecular generation quality.
- Quadruple bonds, many isotopes, and rare charged species are absent from all current corpora—tokenizer coverage advantages remain untested at scale for these.
