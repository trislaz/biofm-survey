---
id: character-level-tokenizations-as-2024
title: Character-level Tokenizations as Powerful Inductive Biases for RNA Foundational
  Models
authors:
- Adrián Morales-Pastor
- Raquel Vázquez-Reza
- Miłosz Wieczór
- Clàudia Valverde
- Manel Gil-Sorribes
- Bertran Miquel-Oliver
- Álvaro Ciudad
- Alexis Molina
year: 2024
venue: null
arxiv: '2411.11808'
doi: null
url: https://arxiv.org/abs/2411.11808v1
pdf_path: papers/character-level-tokenizations-as-2024.pdf
md_path: papers/md/character-level-tokenizations-as-2024.md
modalities:
- rna
status: extracted
evidence_quality: medium-high
tags:
- tokenization
- character-level
- GBST
- learnable-tokenization
- BERT
- scaling-laws
- foundation-model
- ablation
- parameter-efficiency
parameters: 8M / 33M / 50M / 100M / 150M / 650M (suite)
training_tokens: '~31M ncRNA seqs from RNAcentral (~5.1B tokens); extended +31M coding
  seqs from RefSeq (~62M seqs total). Scaling expts: 2.4B–24.8B tokens.'
training_compute: Scaling plateau ~1e16 FLOPs. N_opt ∝ C^0.2279, D_opt ∝ C^0.7720.
references_chased: false
added_at: '2026-04-22T19:36:49+00:00'
updated_at: '2026-04-22T20:17:57+00:00'
is_fm: false
fm_classification_reason: Methodology study on tokenization for RNA FMs; not a released
  FM.
---

## TL;DR

ChaRNABERT replaces fixed RNA tokenizers (single-nucleotide, k-mer, codon) with GBST (Gradient-Based Subsequence Tokenization)—a learnable, differentiable soft-tokenizer over character inputs. A 50M-param BERT+GBST model matches or beats RiNALMo (650M) on 8/13 BEACON tasks and outperforms it on RNA-RBP (F1 0.833 vs 0.831) and aptamer-protein interaction (F1 0.791 vs 0.744). Core claim: tokenizer design is a stronger lever than parameter count for RNA FMs.

## Model

**Architecture**: Modified GBST (from Charformer, Tay et al. 2022) feeding a bidirectional BERT encoder. Key change vs original GBST: no downsampling (preserves nucleotide-level resolution). GBST enumerates candidate subsequence blocks up to max block size M via sliding-window offsets (analogous to ORFs), scores them with a learned scoring network, and forms latent representations via softmax-weighted sum over block candidates. Position-wise score calibration via pseudo-self-attention over block probabilities.

**Architectural improvements over vanilla BERT**: SwiGLU nonlinearities, RoPE, QKNorm (reduces training instability / loss spikes), FlashAttention 2. Context window up to 8190 nucleotides.

**Model sizes** (all 20 heads):

| Params | Layers | d_model |
|--------|--------|---------|
| 8M     | 6      | 320     |
| 33M    | 12     | 480     |
| 50M    | 15     | 500     |
| 100M   | 23     | 600     |
| 150M   | 30     | 640     |
| 650M   | 33     | 1280    |

## Data

- **Non-coding**: ~31M sequences from RNAcentral (miRNA, snRNA, snoRNA, tRNA, rRNA, lncRNA, piRNA, siRNA).
- **Extended (coding+non-coding)**: +31M coding sequences from RefSeq → ~62M total sequences.
- **Scaling experiments**: Subsets from MARS database — 15M / 66M / 100M / 150M sequences → 2.4B / 10.9B / 16.5B / 24.8B tokens respectively.

## Training Recipe

- **Objective**: MLM + UL2 masking (S-denoising = short-span MLM, X-denoising = long-span, R-denoising = autoregressive). Shared g-mask token. Sampled per-step.
- **Precision**: BF16.
- **Distribution**: DeepSpeed + ZeRO.
- **Context**: up to 8192 nucleotides.
- **All model sizes trained on both** non-coding-only and coding+non-coding datasets.
- **Downstream fine-tuning**: Task-specific heads on top of frozen/fine-tuned CRB. Early stopping on smoothed validation loss (EMA α=0.1, patience 50k steps). Class-weighted loss for imbalanced tasks.

## Key Ablations & Design Choices

### GBST vs single-nucleotide Embedding (EM) — MLM loss

**5M model (final loss, lower is better)**:

| LR    | EM    | GBST  | Δ       |
|-------|-------|-------|---------|
| 5e-4  | 0.508 | 0.498 | −0.010  |
| 1e-4  | 0.580 | 0.537 | −0.043  |
| 5e-5  | 0.639 | 0.581 | −0.058  |

→ GBST wins at all LRs; advantage grows at lower LRs.

**50M model**:

| LR    | EM    | GBST  | Δ       |
|-------|-------|-------|---------|
| 5e-4  | 3.516 | 19.52 | both unstable |
| 1e-4  | 0.437 | 0.434 | −0.003  |
| 5e-5  | 0.469 | 0.450 | −0.019  |

→ Marginal GBST advantage at stable LRs; both highly unstable at 5e-4.

**100M model**:

| LR    | EM    | GBST  | Δ       |
|-------|-------|-------|---------|
| 1e-4  | 0.446 | 0.454 | +0.008 (EM slightly better) |
| 5e-5  | 0.465 | 0.460 | −0.005  |
| 1e-5  | 0.640 | 0.577 | −0.063  |

→ Mixed at 100M: EM edges GBST at high LR; GBST wins at low LR. GBST more robust to LR choice.

### Context window (2048 / 4096 / 8192)

U-shaped curve for both tokenizations — optimal model size ~30–50M params regardless of window. EM benefits from smaller windows (2048/4096 < 8192 in loss). GBST performance more stable across window sizes — tokenizer absorbs some context-length sensitivity.

### Data scaling (2.4B → 24.8B tokens)

"Visible but not substantial" impact on loss for both GBST and EM. U-shaped saturation at 30–50M params persists across all dataset sizes. Conclusion: model architecture/tokenizer matters more than raw data volume in this regime.

### Scaling laws (Chinchilla-style fit)

- N_opt ∝ C^0.2279 (model size scales sublinearly with compute).
- D_opt ∝ C^0.7720 (tokens scale superlinearly — should invest more in data than params).
- Improvements plateau ~10^16 FLOPs.
- Saturation at 30–50M params for RNA, much earlier than protein (ESM) or NLP.

### BEACON benchmark — GBST-50M vs RiNALMo-650M (13× fewer params)

| Task   | Metric | CRB-50M       | RiNALMo-650M  | Winner       |
|--------|--------|---------------|---------------|--------------|
| SSP    | F1     | 0.66±0.06     | 0.72±0.01     | RiNALMo      |
| CMP    | P@L    | 0.59±0.01     | 0.49±0.06     | **CRB** (+15% from 33→50M) |
| DMP    | R²     | 0.61±0.02     | 0.59±0.04     | **CRB**      |
| SSI    | F1     | 0.43±0.00     | 0.39±0.01     | **CRB**      |
| SPL    | R²     | 0.94±0.00     | 0.96±0.01     | RiNALMo      |
| APA    | ACC    | 0.83±0.00     | 0.82±0.01     | **CRB**      |
| NcRNA  | ACC    | 0.96±0.01     | 0.98±0.01     | RiNALMo      |
| Modif  | AUC    | 0.95±0.00     | 0.76±0.09     | **CRB** (large gap) |
| MRL    | R²     | 0.90±0.00     | 0.86±0.01     | **CRB**      |
| VDP    | MCRMSE | 0.25±0.00     | 0.23±0.01     | **CRB** (lower=better) |
| PRS    | R²     | 0.45±0.01     | 0.47±0.02     | RiNALMo      |
| CRI-On | SC     | 0.35±0.00     | 0.39±0.07     | RiNALMo      |
| CRI-Off| SC     | 0.11±0.01     | 0.01±0.04     | **CRB**      |

CRB-8M already competitive: beats RiNALMo on APA (0.83 vs 0.82), Modif (0.94 vs 0.76), VDP (0.25 vs 0.23), CRI-Off (0.11 vs 0.01).

### Extended tasks — GBST enables extreme parameter efficiency

- **CLIP RNA-RBP interaction** (5-class): CRB-8M F1=0.833 vs RiNALMo-650M F1=0.831 (81× fewer params, statistically significant). LSTM 0.719, CNN 0.770.
- **Aptamer-protein interaction** (TAD): CRB-50M F1=0.791 vs RiNALMo F1=0.744 (stat. sig.). Protein side encoded with ESM-650M (frozen).

### Coding vs non-coding pretraining data

Adding coding sequences to pretraining hurts CLIP RNA-RBP performance (stat. sig. for 33M and 50M models) but helps aptamer-protein interaction. Task-dependent tradeoff.

### Model size impact on downstream tasks

Scaling from 8M→50M: marginal for most tasks. Notable exception: Contact Map Prediction gains ~15% from 33M→50M. CRISPR off-target: non-monotonic (33M worst, 8M and 50M better). No stat. sig. changes in mean performance across task categories between 8M and 50M.

## Reported Insights

1. **Learnable tokenization > fixed tokenization for RNA**. GBST removes arbitrary assumptions of nucleotide/codon/k-mer groupings; the model discovers optimal sub-sequence units from data.
2. **RNA scaling laws differ from protein/NLP**: saturation at 30–50M params is much earlier than ESM or GPT. Tokens should be scaled faster than params (D_opt ∝ C^0.77).
3. **Parameter efficiency**: GBST compensates for parameter count — 8M GBST model can beat 650M EM model on specific tasks.
4. **UL2 masking** (S+X+R denoising) chosen over plain MLM for versatility but paper does not ablate MLM vs UL2 in this version (promised for future work).
5. **No downsampling in GBST** (unlike Charformer) is critical for nucleotide-resolution downstream tasks.

## References Worth Chasing

- **Charformer** (Tay et al., 2022) — original GBST for NLP; ChaRNABERT adapts this to bio.
- **RiNALMo** (Penić et al., 2024) — main baseline; 650M RNA FM using k-mer embeddings + secondary structure annotations.
- **BEACON** (Ren et al., 2024a) — benchmark used for 13 RNA tasks.
- **UL2** (Tay et al., 2023) — unified masking paradigm.
- **Serrano et al. (2024)** — "Are protein language models compute optimal?" — protein scaling law reference.
- **Hoffmann et al. (2022)** — Chinchilla scaling laws, methodology followed here.
- **BigRNA** (Celaj et al., 2023) — multi-omics RNA FM, different approach (genomic context).

## Notes / Open Questions

- **Preprint v1** — authors explicitly state 150M and 650M downstream results + MLM vs UL2 ablation coming in future versions.
- The GBST advantage on MLM loss is clear at small scale but inconsistent at 100M — is the tokenizer's inductive bias most valuable in low-data/low-param regimes?
- No comparison against BPE or SentencePiece tokenizers — only GBST vs single-nucleotide embedding. Missing k-mer baselines directly (RiNALMo uses k-mer but architecture also differs).
- Scaling law fit uses limited data points (6 model sizes × 4 dataset sizes) — exponents should be treated as rough.
- Weights for 8M only released; larger models "upon request" — limits reproducibility.
- Aptamer task uses ESM-650M for protein side — protein encoder quality confounds RNA model evaluation.
- CRISPR off-target non-monotonic behavior unexplained — could be overfitting artifact at 33M.
