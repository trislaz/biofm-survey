---
id: protclip-function-informed-protein-2024
title: 'ProtCLIP: Function-Informed Protein Multi-Modal Learning'
authors:
- Hanjing Zhou
- Mingze Yin
- Wei Wu
- Mingyang Li
- Kun Fu
- Jintai Chen
- Jian Wu
- Zheng Wang
year: 2024
venue: null
arxiv: '2412.20014'
doi: null
url: https://arxiv.org/abs/2412.20014v1
pdf_path: papers/protclip-function-informed-protein-2024.pdf
md_path: papers/md/protclip-function-informed-protein-2024.md
modalities:
- protein-sequence
- multimodal
status: extracted
evidence_quality: medium
tags:
- contrastive-learning
- protein-text-alignment
- function-prediction
- segment-wise-objectives
- noisy-label-learning
parameters: null  # ESM-2-650M + PubMedBERT (~110M) + cross-attn/MLP heads; total not stated
training_tokens: null  # 251.5M protein-text pairs; token count not reported
training_compute: 10000 V100 GPU-hours
references_chased: false
added_at: '2026-04-22T19:37:10+00:00'
updated_at: '2026-04-22T20:24:35+00:00'
---

## TL;DR

ProtCLIP is a CLIP-style protein–biotext contrastive model that improves on prior protein-text alignment work with (1) a large-scale 251.5M-pair dataset (ProtAnno-D) with a property-driven sampling strategy to handle noisy machine annotations, and (2) two novel segment-wise pre-training objectives (BSR for static functional segments, PDA for dynamic functional segments) that inject fine-grained function information beyond the standard global contrastive loss. SOTA on 22 benchmarks across 5 task types.

## Model

- **Architecture**: Dual-encoder (CLIP-style). Protein encoder = ESM-2-650M; biotext encoder = PubMedBERT. Both initialized from pre-trained checkpoints.
- **Additional modules**: Cross-attention module + MLP reconstruction head for Biotext-guided Static Segment Reconstruction (BSR); prototype memory bank for Property-grouped Dynamic Segment Alignment (PDA).
- **Four pre-training objectives** jointly optimized:
  1. **L_GC** – global contrastive loss (standard InfoNCE).
  2. **L_BSR** – masks 15% of protein sequence as contiguous static segments (length 5–10), reconstructs via cross-attention with biotext (cross-entropy).
  3. **L_PDA** – computes similarity between each residue and 4 property prototypes, thresholds (θ=0.3) to form dynamic segments, contrasts these with property descriptions.
  4. **L_MLM** – standard masked language modeling on protein tokens (15% mask rate) to preserve unimodal knowledge.
- **Overall loss**: L = L_GC + λ₁·L_BSR + λ₂·L_MLM + L_PDA, with λ₁=0.7, λ₂=0.3.
- **Parameters**: Not explicitly stated; sum of ESM-2-650M (~650M) + PubMedBERT (~110M) + auxiliary heads.

## Data

- **ProtAnno-S**: 0.5M manually reviewed protein-biotext pairs from SwissProt (higher quality).
- **ProtAnno-D**: 251.5M computationally analyzed protein-biotext pairs from trEMBL (noisier).
- **Source**: UniProt (SwissProt + trEMBL). Each pair aligns a protein sequence with concatenated textual descriptions of 4 properties: Protein Name, Function, Subcellular Location, Similarity.
- **Property-driven sampling**: Entries with confidence C=4,5 and coverage R=1/4,2/4 are discarded. Remaining entries are sampled with probability P ∝ C^{−3} · √R · N per cluster, balancing quality and quantity.
- Pre-training uses ProtAnno-D with this sampling strategy.

## Training Recipe

- **Hardware**: 64× Tesla V100 GPUs, 10,000 GPU-hours total.
- **Optimizer**: Adam, lr = 1e-5, weight decay = 0.
- **Batch size**: 2048 (pre-training), 512 (downstream fine-tuning).
- **Hyperparameters**: θ = 0.3 (PDA threshold), λ₁ = 0.7, λ₂ = 0.3.
- **Framework**: PyTorch.

## Key Ablations & Design Choices

- **Data strategy matters most**: Single-dataset training < pretrain-then-finetune < ProtAnno-D with property-driven sampling. Shows noisy data has value when properly sampled (Table 6).
- **Both segment objectives essential**: Removing PDA causes a larger drop than removing BSR, indicating dynamic segment alignment is the more impactful objective (Table 7).
- **L_BSR vs L_MLM interference**: Without loss weighting, segment-level and token-level reconstruction losses interfere and training diverges. Setting λ₁=0.7, λ₂=0.3 resolves this (Figure 5).
- **Loss weight sweep**: λ₁=0.7 is optimal across location classification benchmarks (Figure 6).
- **Threshold θ**: θ=0.3 is optimal for PDA; θ≥0.7 causes dramatic performance drop because too many functional residues are discarded (Appendix C.4).
- **Ablations use ESM-2-150M** (smaller encoder) evaluated on Sub, EC, Prot2MF.

## Reported Insights

- ProtCLIP sets SOTA on all 22 benchmarks across 5 task types: protein classification (59.9% ↑ GO-CC, 39.7% ↑ GO-BP), mutation effect prediction, cross-modal transformation (75% avg ↑), semantic similarity inference, and PPI prediction.
- The function-informed paradigm (capturing static and dynamic functional segments) is key to bridging the gap between protein-text and image-text foundation models.
- Large-scale noisy protein annotations (251.5M pairs) are valuable when combined with property-driven sampling—contradicting prior claims that "data quality is more important than quantity."
- Property-grouped dynamic segments decouple multi-property alignment, mitigating mutual interference across attribute domains.

## References Worth Chasing

- **ProtST** (Xu et al. 2023) – predecessor multi-modal protein-text model; ProtCLIP's primary baseline.
- **BioBridge** (Wang et al. 2024) – bridge module between protein, molecule, and text models; strong cross-modal transformation baseline.
- **ESM-2** (Lin et al. 2023) – protein language model used as the protein encoder backbone.
- **ProteinCLIP** (Wu, Chang, Zou 2024) – concurrent protein-text CLIP work.
- **OntoProtein** (Zhang et al. 2022) – knowledge-graph-enhanced protein representations.

## Notes / Open Questions

- Total parameter count is not reported; would be ~760M+ based on component sizes.
- No discussion of computational cost at inference time or embedding dimensionality.
- The 4 selected properties (Name, Function, Location, Similarity) seem somewhat arbitrary; effect of property selection not ablated.
- Evaluation uses ESM-2-650M for the main model but ablations use ESM-2-150M—unclear how findings transfer across scales.
- No comparison with structure-aware protein models (e.g., those using 3D coordinates).
- ProtAnno dataset availability/release status not clarified in the paper.
