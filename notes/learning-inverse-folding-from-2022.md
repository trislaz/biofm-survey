---
id: learning-inverse-folding-from-2022
title: Learning inverse folding from millions of predicted structures (ESM-IF1, Hsu 2022 ICML)
authors:
- Chloe Hsu
- Robert Verkuil
- Jason Liu
- Zeming Lin
- Brian Hie
- Tom Sercu
- Adam Lerer
- Alexander Rives
year: 2022
venue: ICML 2022
arxiv: null
doi: 10.1101/2022.04.10.487779
url: https://proceedings.mlr.press/v162/hsu22a.html
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/learning-inverse-folding-from-2022.md
modalities:
- protein-structure
- protein-sequence
status: extracted
evidence_quality: abstract+repo
tags:
- inverse-folding
- distillation
- AlphaFold-data
- GVP
- transformer
- protein-design
- structure-conditioned-generation
- span-masking
parameters: 142M
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

ESM-IF1 (GVPTransformer) is a structure-conditioned sequence design model that tackles the inverse protein folding problem: given backbone atom coordinates, predict a compatible amino-acid sequence. The key insight is massively augmenting training data with ~12M AlphaFold2-predicted structures from UniRef50, increasing available structures by nearly three orders of magnitude over PDB alone. The model—a GVP encoder feeding a Transformer decoder—achieves 51% native sequence recovery on structurally held-out CATH backbones (72% on buried residues), a ~10 pp jump over prior methods. It generalizes to complex design, partial structures, binding interfaces, and multi-state design. Part of Meta FAIR's ESM family.

## Model

- **Name**: ESM-IF1 (also called GVPTransformer)
- **Pretrained checkpoint**: `esm_if1_gvp4_t16_142M_UR50`
- **Architecture**: Encoder–decoder.
  - **Encoder**: 4 Geometric Vector Perceptron (GVP) layers that process backbone geometry in an SE(3)-invariant manner, producing per-residue scalar + vector representations.
  - **Decoder**: 16-layer autoregressive Transformer that generates amino-acid sequences conditioned on the encoder output.
  - Total: 20 layers.
- **Parameters**: ~142M (model name convention; GitHub table lists 124M—may reflect different counting of embeddings).
- **Embedding dimension**: 512.
- **Input**: Backbone atom coordinates (N, CA, C) per residue; shape L × 3 × 3. Edges defined by a distance cutoff (graph neighbours).
- **Output**: Categorical distribution over 20 amino acids per residue (autoregressive, left-to-right).
- **Span masking**: Model also trained with randomly masked backbone regions (`np.inf` coordinates), enabling sequence prediction for partially resolved or designed structures.
- **Multi-chain support**: Can condition on the full multi-chain complex backbone while designing a target chain.

## Data

- **Experimental structures**: CATH v4.3 domain structures (topology-level split for train/val/test). ~30K experimental domains from the PDB.
- **AlphaFold2-predicted structures**: ~12M structures predicted for UniRef50 sequences using AlphaFold2. This augments training data by ~3 orders of magnitude over PDB alone.
- **Data split**: CATH topology-level structural holdout. Test/validation sets consist of CATH topologies unseen during training, preventing structural leakage.
- **Data download**: CATH backbone coordinates and splits available at `https://dl.fbaipublicfiles.com/fair-esm/data/cath4.3_topologysplit_202206/`.

## Training Recipe

- **Objective**: Cross-entropy loss over amino-acid classes per residue (autoregressive sequence generation conditioned on structure).
- **Span masking**: During training, random spans of backbone coordinates are masked (set to inf) to teach robustness to incomplete structures.
- **Optimizer**: Adam (lr ≈ 5e-4, weight decay ≈ 0.01 per web sources; exact hyperparameters not fully disclosed in paper).
- **Batch size**: ~64 (web sources).
- **Training schedule**: Linear warmup followed by cosine decay; trained for ~400K updates (web sources; not confirmed in paper).
- **Mixed precision**: FP16 training reported.
- **Hardware**: Reported use of 8 × NVIDIA V100 GPUs (web sources; paper does not specify).
- **Software**: PyTorch; released via `fair-esm` pip package and PyTorch Hub.
- **Key distillation aspect**: The 12M predicted structures are themselves outputs of AlphaFold2—so ESM-IF1 effectively distills structural knowledge from AF2 into a much smaller sequence-design model.

## Key Ablations & Design Choices

### 12M predicted structures vs. PDB-only
The defining contribution. Training on CATH experimental structures alone yields ~41% sequence recovery; adding 12M AlphaFold2-predicted structures boosts this to ~51%, a gain of ~10 percentage points. This demonstrates that predicted structures, despite being noisy, provide massive data augmentation benefit for inverse folding.

### Geometric input processing (GVP)
GVP layers provide SE(3)-invariant featurization of backbone geometry, operating on both scalar and vector channels. This is critical for generalizing across orientations and conformations without data-augmentation tricks. The GVP encoder is adapted from Jing et al. (2021).

### Autoregressive decoder vs. non-autoregressive
The model uses an autoregressive Transformer decoder. This naturally captures inter-residue dependencies in designed sequences (e.g., hydrophobic packing patterns).

### Span masking for partial structures
Training with random coordinate masking enables the model to handle partially resolved or intentionally masked backbone regions at inference time—useful for de novo design where only part of the scaffold is specified.

### Multi-chain conditioning
Conditioning on the full multi-chain complex backbone often reduces perplexity and increases sequence recovery compared to single-chain input, though performance varies by target.

### Temperature sampling
Lower sampling temperatures (e.g., T = 1e-6) maximize native sequence recovery; higher temperatures (T = 1) yield more diverse designs. A failure mode at high temperature is long repeated amino-acid stretches (e.g., EEEEEEEE).

## Reported Insights

- **Data scale dominates**: The single biggest improvement comes from augmenting training data with predicted structures, not from architectural innovations. This is a strong argument for "data engineering" in structural biology ML.
- **Buried vs. exposed residues**: 72% recovery for buried residues vs. 51% overall, reflecting that core packing is more constrained by backbone geometry than surface residues.
- **Generalization beyond CATH domains**: The model transfers to protein complex design, binding interface design, multi-state design, and partially masked structures despite being trained primarily on single-domain CATH structures.
- **Sequence scoring**: Conditional log-likelihoods from ESM-IF1 can score mutant sequences given a structure, providing a structure-aware fitness landscape complementary to sequence-only models like ESM-1v.
- **Encoder as structure representation**: The GVP encoder output (L × 512) can serve as a general-purpose structure representation for downstream tasks.

## References Worth Chasing

1. **Jing et al. 2021** — "Learning from Protein Structure with Geometric Vector Perceptrons" (ICLR 2021). The GVP-GNN architecture that provides the invariant encoder in ESM-IF1.
2. **Ingraham et al. 2019** — "Generative Models for Graph-Based Protein Design" (NeurIPS 2019). Structured Transformer baseline for inverse folding; input pipeline adapted from this work.
3. **Jumper et al. 2021** — "Highly accurate protein structure prediction with AlphaFold" (Nature). AlphaFold2; source of the 12M predicted structures used for training.
4. **Dauparas et al. 2022** — "Robust deep learning–based protein sequence design using ProteinMPNN" (Science). Key concurrent/competitor inverse folding model (message-passing, not GVP+Transformer).
5. **Lin et al. 2023** — "Evolutionary-scale prediction of atomic-level protein structure with a language model" (Science). ESM-2/ESMFold; sibling model in the ESM family.
6. **Rives et al. 2021** — "Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250M Protein Sequences" (PNAS). ESM-1; foundational work for ESM model family.
7. **Verkuil, Kabeli et al. 2022** — "Language Models Generalize Beyond Natural Proteins" (bioRxiv). Downstream protein design with ESM-2, building on ESM-IF1 ideas.

## Notes / Open Questions

- **Parameter count discrepancy**: The model checkpoint is named `esm_if1_gvp4_t16_142M_UR50` (suggesting 142M parameters) but the GitHub table lists 124M. Likely difference in counting embedding layers or tied weights.
- **Training hyperparameters not fully disclosed**: The ICML paper (PMLR v162, pp. 8946–8970) does not include a complete hyperparameter table. Values for optimizer, LR, batch size, and schedule come from web sources and should be verified against supplementary material.
- **Training compute not reported**: No FLOPs or GPU-hours budget is disclosed. Given 142M params and 12M structures, training is relatively modest compared to ESM-2 (15B).
- **No arXiv ID**: The paper was posted on bioRxiv (10.1101/2022.04.10.487779) and published at ICML 2022, but does not have a standard arXiv identifier.
- **Comparison with ProteinMPNN**: Dauparas et al. (2022, Science) introduced ProteinMPNN around the same time, achieving comparable or better sequence recovery with a message-passing approach. Direct head-to-head comparison on the same benchmarks would be valuable.
- **Repository archived**: The `facebookresearch/esm` repository was archived on Aug 1, 2024. ESM-IF1 remains usable but receives no further updates.
- **Successor**: ESM-3 (2024, EvolutionaryScale) is a multimodal generative model over sequence, structure, and function that may subsume ESM-IF1's capabilities.
- **License**: ESM-IF1 released under MIT license. Requires PyTorch Geometric dependency for GVP layers.
