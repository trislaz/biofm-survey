---
id: instructplm-mu-1-hour-2025
title: 'InstructPLM-mu: 1-Hour Fine-Tuning of ESM2 Beats ESM3 in Protein Mutation
  Predictions'
authors:
- Junde Xu
- Yapin Shi
- Lijun Lang
- Taoyong Cui
- Zhiming Zhang
- Guangyong Chen
- Jiezhong Qiu
- Pheng-Ann Heng
year: 2025
venue: null
arxiv: '2510.03370'
doi: null
url: https://arxiv.org/abs/2510.03370v3
pdf_path: papers/instructplm-mu-1-hour-2025.pdf
md_path: papers/md/instructplm-mu-1-hour-2025.md
modalities:
- protein-sequence
- protein-structure
status: extracted
evidence_quality: medium
tags:
- protein-mutation-prediction
- fine-tuning
- multimodal-fusion
- parameter-efficient
- zero-shot
- ESM2
- LoRA
parameters: 35M / 150M / 650M (ESM2 backbone scales)
training_tokens: null
training_compute: ~1 hour on 4×A100 (fine-tuning 150M backbone)
references_chased: false
added_at: '2026-04-22T19:36:52+00:00'
updated_at: '2026-04-22T20:21:53+00:00'
is_fm: false
fm_classification_reason: 1-hour fine-tuning recipe of ESM2; not a new pretrained
  FM.
---

## TL;DR

InstructPLM-mu is a multimodal fine-tuning framework that injects protein structure embeddings into a pretrained sequence-only PLM (ESM2) via three fusion strategies. The best variant—Token-wise Concat with LoRA+Adapter tuning—matches or beats ESM3 on zero-shot mutation-effect prediction (Spearman 0.469 vs 0.468) after only ~1 hour of fine-tuning on 4×A100 GPUs, compared to months of from-scratch training for competitors.

## Model

- **Architecture**: ESM2 backbone (transformer, masked LM) + frozen structure encoder (ESM-IF or ProteinMPNN) + learned MLP projector that maps structure embeddings to sequence embedding space.
- **Fusion strategies compared**: (1) Cross Attention—adds a cross-attn sublayer in the final transformer block; (2) Channel-wise Concat—element-wise addition of structure and sequence embeddings before the transformer; (3) Token-wise Concat (best)—structure tokens appended as extra input tokens sharing position indices with sequence tokens, doubling sequence length.
- **Fine-tuning recipes**: Adapter-only (~1% params), LoRA+Adapter (5–10% params, best for Token-wise), Full Fine-tune (100%).
- **Backbone scales**: ESM2-35M, ESM2-150M (flagship), ESM2-650M.
- **Structure encoders**: ESM-IF (142M, best single encoder) and ProteinMPNN; combining both hurts slightly.
- **Inference**: zero-shot mutation scoring via masked marginals (no task-specific supervision).

## Data

- **Fine-tuning**: CATH 4.3 — 22,727 train / 2,525 validation protein structures (9:1 split). Sequences cropped to max 512 tokens.
- **Evaluation**: ProteinGym benchmark — 201 deep-mutational-scanning assays (≤1,000 residues), covering Activity (39), Binding (12), Expression (16), Fitness (69), Stability (66).
- **No task-specific labeled data**; fine-tuning uses MLM on wild-type sequences with structural context.

## Training Recipe

- Objective: masked language modeling on protein sequence branch; structure tokens remain unmasked.
- Optimizer: Adam, lr = 1e-4, weight decay = 0.1, 100 warm-up steps.
- Batch size 256, 20 epochs.
- LoRA rank 32, α = 256, applied to every linear layer; backbone weights frozen; projector + LoRA adapters trained jointly.
- Hardware: 4× NVIDIA A100 GPUs; ~1 hour for the 150M backbone.
- Checkpoint selection: validation loss on CATH 4.3.

## Key Ablations & Design Choices

1. **Fusion strategy matters most**: Token-wise Concat (0.469) > Cross Attention (0.440) ≈ Channel-wise Concat (0.435). Token-wise enables bidirectional self-attention between structure and sequence tokens, giving the model flexibility to attend or ignore structural cues per context.
2. **More tunable parameters ≠ better**: LoRA+Adapter (5–10%) beats Full Fine-tune and Adapter-only for Token-wise. For Channel-wise, full fine-tuning at 650M scale catastrophically collapses to near-zero (0.029), showing severe forgetting.
3. **Scaling behaviour depends on tuning recipe**: Adapter-only shows clean monotonic scaling (35M→150M→650M). LoRA+Adapter and Full Fine-tune show unstable or stagnating gains at larger scales—larger pretrained backbones already have enough capacity and are more prone to forgetting with aggressive updates.
4. **MLP projector depth**: 2-layer, 3-layer, 4-layer MLPs yield essentially identical results; shallow is sufficient. Default: 3 layers with GELU + LayerNorm.
5. **Structure encoder**: ESM-IF alone > ProteinMPNN alone > naïve concatenation of both. Encoders carry overlapping/conflicting signals when simply concatenated.
6. **Multimodal fine-tuning >> scaling sequence-only models**: All three fusion methods beat ESM2 at every scale (including ESM2-3B at 0.421), showing structure injection is more effective than simply enlarging the backbone.

## Reported Insights

- Token-wise Concat matches ESM3 (0.469 vs 0.468) despite ESM3 being trained from scratch with far greater resources; ProSST (0.506) and S3F (0.473) still outperform, but they use even more modalities or months of training.
- Largest relative gains are on Stability (+18.1%) and Binding (+12.2%).
- InstructPLM-mu boosts the standalone ESM-IF encoder on 4/5 functional categories, suggesting sequence and structure features reinforce each other.
- The biggest improvements come on assays where baseline ESM2 performed poorly, while high-performing assays are maintained.

## References Worth Chasing

- **ESM3** (Hayes et al., 2025) — the from-scratch multimodal PLM that InstructPLM-mu matches.
- **SaProt** (Su et al., 2023) — structure-aware vocabulary approach for PLMs.
- **ProSST** (Li et al., 2024b) — quantized structure + disentangled attention; current top performer on ProteinGym.
- **S3F** (Zhang et al., 2024) — multi-scale representation with surface modality.
- **InstructPLM** (Qiu et al., 2024) — predecessor framework for aligning PLMs with structure instructions.
- **ProteinGym** (Notin et al., 2023) — the benchmark used.
- **DeepStack** (Meng et al., 2024) — injecting vision features into multiple LLM layers; inspiration for fusion design.

## Notes / Open Questions

- Paper is a preprint (no peer review yet). Results are on ProteinGym only; generalization to other tasks (e.g., design, binding affinity regression) untested.
- No explicit total parameter count for the full InstructPLM-mu system (backbone + encoder + projector + LoRA). The "35M/150M/650M" refers only to the ESM2 backbone.
- Training token count not reported; can be estimated as ~22,727 sequences × 512 tokens × 20 epochs ≈ 233M tokens.
- Catastrophic collapse of Channel-wise Concat + Full Fine-tune at 650M scale is striking and deserves further investigation.
- Code and checkpoints promised but not yet released at time of writing.
