---
id: high-resolution-de-novo-2022
title: High-resolution de novo structure prediction from primary sequence
authors:
- Ruidong Wu
- Fan Ding
- Rui Wang
- Rui Shen
- Xiwen Zhang
- Shitong Luo
- Chenpeng Su
- Zuofan Wu
- Qi Xie
- Bonnie Berger
- Jianzhu Ma
- Jian Peng
year: 2022
venue: bioRxiv
arxiv: null
doi: 10.1101/2022.07.21.500999
url: https://www.biorxiv.org/content/10.1101/2022.07.21.500999v1
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/high-resolution-de-novo-2022.md
modalities:
- protein-structure
- protein-sequence
status: extracted
evidence_quality: abstract+repo
tags:
- MSA-free
- PLM
- protein-language-model
- single-sequence-structure-prediction
- Gated-Attention-Unit
- RoPE
- GeoFormer
- IPA
- recycling
- orphan-proteins
- antibody-structure
parameters: 670000000
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

OmegaFold is the first computational method to predict high-resolution protein 3D structure from a single amino acid sequence without multiple sequence alignments (MSAs). It combines OmegaPLM, a 66-layer Gated Attention Unit protein language model (~670M params) pre-trained with masked language modelling on protein sequences, with a 50-block geometry-inspired transformer (GeoFormer) and an IPA-based structure module. OmegaFold outperforms RoseTTAFold and achieves accuracy comparable to AlphaFold2 on recently released PDB structures, while being especially effective on orphan proteins and antibodies where MSAs are noisy or unavailable.

## Model

- **Architecture**: Two-stage pipeline — (1) OmegaPLM produces per-residue node embeddings and pairwise edge representations; (2) GeoFormer refines these into 3D coordinates via a structure module.
- **OmegaPLM** (protein language model):
  - 66 GAU (Gated Attention Unit) layers — each layer projects input (dim 1280) into gates (dim 2560), values (dim 2560), and attention base (dim 256) via a single SiLU-gated linear projection.
  - Single-head attention with RoPE (Rotary Position Embeddings) for positional encoding.
  - Relative position embedding with 129 bins.
  - Token dropout scaling from ESM-1b (Rives et al. 2021).
  - Masked ratio: 12% during pre-training.
  - Vocabulary: 23 tokens (21 amino acids + mask + padding).
  - Output: per-residue node representations (dim 1280) and pairwise edge attention maps (66 layers → dim 66).
  - **~670M parameters** (dominated by the 66 GAU layers).
- **GeoFormer** (geometry-aware transformer):
  - 50 blocks; node_dim=256, edge_dim=128.
  - Each block: row self-attention with edge bias (8 heads, head_dim=32), column attention, node transition (4× expansion, ReLU), outer product mean (proj_dim=32), 2× geometric triangle attention (4 heads, head_dim=32), edge transition.
  - Final linear projection: node_dim 256 → struct node_dim 384.
- **Structure Module** (IPA-like, AlphaFold2-style):
  - 8 IPA iterations, 12 heads, 4 point queries, 8 point values, 16 scalar queries/values.
  - 3 transition layers, 2 residual blocks, hidden_dim=128.
  - Predicts all-atom coordinates and backbone frames.
- **Confidence Head**: Predicts per-residue pLDDT-like confidence scores stored as B-factors.
- **Recycling**: Multiple forward passes through GeoFormer + Structure Module; previous node/edge representations, coordinates, and frames are fed back. Best result selected by confidence score.
- **Model 2 variant** (Dec 2022 release): Uses `struct_embedder=True` — adds structural feature embedding from previous cycle predictions. Same architecture otherwise.

## Data

- **PLM pre-training**: OmegaPLM pre-trained on large-scale protein sequence databases with masked language modelling (12% masking). Training set likely UniRef50 (~53M sequences) or similar non-redundant protein sequence database. Exact dataset and size not disclosed in the preprint or repo.
- **Structure training**: GeoFormer and structure module trained on experimental structures from the PDB. Exact training set composition and cutoff date not disclosed; PDB circa 2022 contains ~170K non-redundant chains.
- **Evaluation**: Tested on recently released PDB structures (post-training cutoff) to avoid data leakage. Specific benchmarks on orphan proteins (no characterized protein family) and antibodies (fast-evolving, noisy MSAs).

## Training Recipe

- **PLM pre-training**: Masked language modelling with 12% masking ratio. Exact optimizer, learning rate, batch size, hardware, and training duration not disclosed in preprint or repo.
- **Structure training**: Supervised on PDB structures. Training details (optimizer, schedule, augmentation) not disclosed.
- **Inference optimizations** (from repo):
  - Sharded execution via `--subbatch_size` for memory–compute trade-off.
  - Sequences up to 4096 residues on A100 80GB with subbatch_size=448.
  - Configurable `--num_cycle` for quality–speed trade-off.
  - Supports A100 GPU, MPS (Apple Silicon), CPU.
- **Training compute**: Not reported. Web sources suggest 8× A100 GPUs for the 670M model, but this is unverified.

## Key Ablations & Design Choices

- **MSA-free prediction**: Core design choice — replace MSA-derived co-evolutionary signal with PLM-learned representations. OmegaPLM embeddings + pairwise attention maps serve as a learned substitute for MSA statistics.
- **GAU over standard multi-head attention**: OmegaPLM uses Gated Attention Units (single-headed with gated values) rather than standard multi-head self-attention, following the FLASH architecture. This provides efficient sequence modelling with linear-like scaling properties.
- **RoPE positional encoding**: Uses rotary position embeddings for length generalization, unlike absolute or learned positional encodings.
- **GeoFormer vs Evoformer**: Replaces AlphaFold2's Evoformer (which processes MSA rows/columns) with GeoFormer that operates on single-sequence node + pairwise edge representations. Geometric triangle attention replaces MSA-derived triangular update operations.
- **Recycling strategy**: Iterates the full GeoFormer + structure module, selecting the cycle with highest confidence. This mirrors AlphaFold2's recycling but operates on PLM features instead of MSA features.
- **Depth of PLM (66 layers)**: Unusually deep for a protein language model (ESM-2 650M uses 33 layers). The extra depth produces richer pairwise attention maps (66-dim edge features).

## Reported Insights

- **Single-sequence prediction is competitive**: OmegaFold achieves TM-scores comparable to AlphaFold2 (~0.93 median vs ~0.96) and outperforms RoseTTAFold on recently released structures — demonstrating MSAs are not strictly necessary.
- **Orphan protein strength**: Proteins without detectable homologs (no MSA available) are predicted with high accuracy, filling a critical gap in structural biology.
- **Antibody performance**: Antibodies with noisy MSAs due to rapid somatic hypermutation are handled better by single-sequence prediction than MSA-based methods.
- **PLM captures co-evolutionary information implicitly**: The masked language model objective learns residue co-variation patterns from sequences alone, effectively learning the physics of protein folding without explicit evolutionary input.
- **Speed advantage**: Orders of magnitude faster than MSA-based methods since no database search (JackHMMER/HHblits) is required at inference time.

## References Worth Chasing

- ESM-1b: Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250M Protein Sequences (Rives et al. 2021, PNAS) — token dropout scaling used in OmegaPLM
- ESMFold: Language Models of Protein Sequences at the Scale of Evolution Enable Accurate Structure Prediction (Lin et al. 2023, Science) — concurrent MSA-free structure prediction using ESM-2
- AlphaFold2: Highly Accurate Protein Structure Prediction with AlphaFold (Jumper et al. 2021, Nature) — architecture inspiration (IPA, recycling)
- FLASH / GAU: Transformer Quality in Linear Time (Hua et al. 2022, ICML) — Gated Attention Unit architecture used in OmegaPLM
- RoFormer: Enhanced Transformer with Rotary Position Embedding (Su et al. 2021) — RoPE used in OmegaPLM
- RoseTTAFold: Accurate Prediction of Protein Structures and Interactions Using a Three-Track Neural Network (Baek et al. 2021, Science) — primary MSA-based baseline
- ProtTrans: Toward Understanding the Language of Life Through Self-Supervised Learning (Elnaggar et al. 2022, TPAMI) — early PLM for proteins

## Notes / Open Questions

- **Abstract+repo evidence only**: The biorxiv preprint is a short paper with limited methodological detail. Architecture is primarily reconstructed from the released code (`config.py`, `omegaplm.py`, `geoformer.py`, `model.py`). A full-text reading would likely clarify training data and procedure.
- **Training data not disclosed**: Neither the preprint nor the repo specify the exact pre-training corpus for OmegaPLM. UniRef50 is the most commonly assumed source based on web reports, but this is unconfirmed.
- **Training compute unknown**: No GPU hours, wall-clock time, or FLOP counts are reported anywhere.
- **Parameter count is approximate**: ~670M is derived from architecture analysis of the 66 GAU layers (each ~10.2M params). The GeoFormer and structure module add ~20–30M, giving a total of ~700M. Published estimates range from 668M to 670M.
- **Self-distillation**: Some web sources mention self-distillation techniques similar to AlphaFold2, but this is not confirmed from abstract or repo code.
- **No comparison with ESMFold**: OmegaFold and ESMFold were concurrent works (both 2022). Direct head-to-head comparison only appears in subsequent benchmark papers.
- **Model 2 improvements unclear**: The Dec 2022 Model 2 release enables `struct_embedder=True` but no paper or blog post details the architectural change or benchmark improvements.
- **Published in Nature Computational Science (2024)**: The preprint was eventually published as a journal article — full-text may contain additional details not in the biorxiv version.
