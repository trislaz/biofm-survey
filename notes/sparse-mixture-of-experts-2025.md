---
id: sparse-mixture-of-experts-2025
title: 'Sparse Mixture-of-Experts for Multi-Channel Imaging: Are All Channel Interactions
  Required?'
authors:
- Sukwon Yun
- Heming Yao
- Burkhard Hoeckendorf
- David Richmond
- Aviv Regev
- Russell Littman
year: 2025
venue: null
arxiv: '2511.17400'
doi: null
url: https://arxiv.org/abs/2511.17400v1
pdf_path: papers/sparse-mixture-of-experts-2025.pdf
md_path: papers/md/sparse-mixture-of-experts-2025.md
modalities:
- imaging-cell
- imaging-microscopy
status: extracted
evidence_quality: low
tags:
- mixture-of-experts
- vision-transformer
- multi-channel-imaging
- sparse-attention
- efficiency
parameters: ~22M
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:18+00:00'
updated_at: '2026-04-22T20:26:00+00:00'
is_fm: false
fm_classification_reason: MoE methodology for multi-channel imaging.
---

## TL;DR

MoE-ViT treats each channel in multi-channel images (e.g., cell painting) as a sparse MoE expert and routes each patch to only its top-k most relevant channels, reducing cross-channel attention from O(N²C²) to O(N²Ck). On JUMP-CP (8-channel microscopy) and So2Sat (18-channel satellite), it matches or beats dense channel-wise ViTs while cutting attention FLOPs by ~50%. This is a proof-of-concept workshop paper (NeurIPS 2025 AI4Science), not a foundation model per se, but directly relevant to efficient multi-channel biological image encoders.

## Model

- **Architecture**: ViT-Small backbone with standard Transformer encoder, where Multi-Head Attention is replaced by a "Multi-Head Channel MoE" module.
- **Channel-as-expert**: Each imaging channel is treated as one MoE expert. A lightweight single-layer FFN router per Transformer layer produces softmax scores over channels for each patch token, then selects top-k channels.
- **Cross-attention**: Patches routed to a given channel serve as Query; all patches natively belonging to that channel serve as Key/Value via channel-specific K,V projection matrices. Shared Q projection across channels.
- **Aggregation**: Each patch's output is the router-weighted average of the cross-attention outputs from its selected expert channels.
- **Parameters**: ViT-Small backbone (~21–22M activated params at top-k=1; up to ~46M at top-k=C due to channel-specific K,V projections). MoE-ViT adds channel-specific K,V projections and the router; all other Transformer modules are unchanged.
- **Regularization**: Standard MoE load-balancing / importance losses to prevent routing collapse.

## Data

| Dataset | Domain | Channels | Image size | Train / Val / Test | Task | Classes |
|---------|--------|----------|------------|-------------------|------|---------|
| JUMP-CP (plate BR00116991) | Cell painting microscopy | 8 (5 fluorescence + 3 brightfield) | 224×224 | 127k / 45k / 45k | Treatment classification | 161 |
| So2Sat | Satellite imagery | 18 (8 Sentinel-1 + 10 Sentinel-2) | 32×32 | 352k / — / 24k | Climate zone classification | 17 |

No pre-training; models trained from scratch in supervised setting for 100 epochs with AdamW. Hierarchical Channel Sampling (HCS) used during training for all models.

## Training Recipe

- Backbone: ViT-Small (patch 16 for JUMP-CP, patch 8 for So2Sat).
- Optimizer: AdamW.
- Epochs: 100.
- Training regime: Supervised from scratch (no self-supervised pre-training).
- HCS (Hierarchical Channel Sampling) from Channel-ViT applied during training for all models including baselines.
- No other hyperparameter details disclosed.

## Key Ablations & Design Choices

1. **Top-k sweep (most important result)**:
   - JUMP-CP: top-k=1 → 64.06% acc / 2.33 GFLOPs; top-k=2 → 66.44% / 2.81 GFLOPs; top-k=C(=8) → 70.16% / 5.65 GFLOPs. Baselines ChAda-ViT=68.16%, DiChaViT=68.49%, both at 5.65 GFLOPs.
   - So2Sat: top-k=1 → 63.12% / 0.35 GFLOPs; top-k=2 → 64.66% / 0.36 GFLOPs. ChAda-ViT=63.94%, DiChaViT=63.80%, both at 0.47 GFLOPs.
   - **Top-k=2 is the sweet spot**: ~50% attention FLOP reduction on JUMP-CP with only −1.7% accuracy; on So2Sat it actually *improves* accuracy (+0.72%) with 23% fewer FLOPs.

2. **Full-channel MoE (top-k=C) beats baselines**: When all channels are active, channel-specific K,V projections still help (+1.67% on JUMP-CP over DiChaViT) — the MoE parameterization itself (not just sparsity) adds representational value.

3. **Patch size ablation**: Reducing patch size from 16→8 on JUMP-CP increases attention GFLOPs ~8× (2.81→22.61 at top-k=2). The efficiency gains of MoE routing are most pronounced for larger images / smaller patches (more spatial tokens).

4. **Dataset dependency**: Efficiency gains scale with spatial resolution. JUMP-CP (224²) benefits more from sparsity than So2Sat (32²).

## Reported Insights

- Not all cross-channel interactions are necessary; sparse routing suffices and can even improve performance by reducing noise from irrelevant channels.
- The channel-specific expert parameterization (separate K,V per channel) independently boosts accuracy even at full channel count, suggesting the MoE factorization adds useful inductive bias.
- FLOPs savings scale with spatial resolution (N²), making the approach increasingly attractive for high-resolution biological images (e.g., digital pathology).
- Random channel sub-sampling (HCS) is inferior to learned routing because it ignores patch-level channel relevance.

## References Worth Chasing

- **Channel-ViT** (Bao et al., ICLR 2024): Original channel-wise tokenization for ViTs — the baseline architecture that MoE-ViT modifies.
- **ChAda-ViT** (Bourriez et al., CVPR 2024): Channel-adaptive attention with self-supervised pretraining for heterogeneous microscopy images.
- **DiChaViT** (Pham & Plummer, NeurIPS 2024): Enhances intra/inter-channel feature diversity in channel-wise ViTs.
- **JUMP-CP dataset** (Chandrasekaran et al., bioRxiv 2023): Large-scale cell painting morphological profiling dataset.
- **V-MoE** (Riquelme et al., NeurIPS 2021): Scaling vision with sparse MoE — the vision MoE baseline this work draws from.

## Notes / Open Questions

- This is a **workshop paper** (NeurIPS 2025 AI4Science), not a full conference paper — proof-of-concept level evidence only.
- No wall-clock time or GPU memory comparisons — only theoretical GFLOPs reported. Authors acknowledge hardware-aware optimization is future work.
- Only two datasets tested; no biological downstream tasks beyond classification (e.g., no morphological profiling, no retrieval, no generative tasks).
- The router is a single linear layer — would deeper / more expressive routers help?
- How does this interact with self-supervised pre-training (e.g., DINO, MAE)? The paper only evaluates supervised training.
- Potential synergy: combining patch-level sparsity (selecting spatial regions) with channel-level sparsity (this work) for doubly-sparse attention.
- Authors from Genentech / Aviv Regev lab — signals interest in applying this to large-scale biological imaging pipelines.
