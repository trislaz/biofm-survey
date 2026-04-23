---
id: phylogen-language-model-enhanced-2024
title: 'PhyloGen: Language Model-Enhanced Phylogenetic Inference via Graph Structure
  Generation'
authors:
- ChenRui Duan
- Zelin Zang
- Siyuan Li
- Yongjie Xu
- Stan Z. Li
year: 2024
venue: null
arxiv: '2412.18827'
doi: null
url: https://arxiv.org/abs/2412.18827v1
pdf_path: papers/phylogen-language-model-enhanced-2024.pdf
md_path: papers/md/phylogen-language-model-enhanced-2024.md
modalities:
- dna
status: extracted
evidence_quality: medium
tags:
- phylogenetics
- variational-inference
- graph-neural-network
- tree-structure-generation
- DNABERT2
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:46+00:00'
updated_at: '2026-04-22T20:24:20+00:00'
---

## TL;DR

PhyloGen frames phylogenetic inference as conditional tree-structure generation, using DNABERT2 embeddings of raw (unaligned) DNA sequences to jointly optimise topology and branch lengths via variational inference. Three modules—Feature Extraction (frozen DNABERT2), PhyloTree Construction (Neighbor-Joining on latent distances), and PhyloTree Structure Modeling (Tree Encoder/Decoder + DGCNN for branch lengths)—plus a learned Scoring Function for gradient stability. Achieves state-of-the-art MLL and ELBO on all 8 benchmarks (27–64 taxa) at NeurIPS 2024, without requiring aligned sequences or pre-generated topologies.

## Model

- **Architecture**: Three-module pipeline:
  1. **Feature Extraction**: Frozen DNABERT2 (pre-trained genomic LM) encodes raw DNA sequences into 768-d embeddings; no fine-tuning mentioned.
  2. **PhyloTree Construction**: MLP maps embeddings → latent (µ, σ); reparameterised z* used to compute XOR-based distance matrix D; Neighbor-Joining algorithm produces initial topology τ(z*).
  3. **PhyloTree Structure Modeling**: (a) Topology learning via Tree Encoder R and Tree Decoder Q with variational inference; (b) Branch-length learning via linear-time dual-pass traversal (postorder + preorder), DGCNN edge-convolution (F=768 → F'=100), and MLP reparameterisation of branch lengths.
- **Scoring Function S**: FC-layer MLP on leaf-node latent embeddings; jointly optimised with ELBO to provide auxiliary gradient signal for stable convergence.
- **Loss**: L_total = −L_multi-sample(Q, R) + L(S) + L_KL, with multi-sample ELBO (K Monte Carlo samples).
- **Parameter count**: Not reported. Backbone is DNABERT2 (~117M); PhyloGen-specific modules (MLPs, Tree Encoder/Decoder, DGCNN) are small but unquantified.
- **Inference**: End-to-end; no evolutionary model (JC, GTR) needed; accepts unaligned, variable-length sequences.

## Data

- **Benchmarks**: 8 real-world datasets (DS1–DS8) from Lakner et al., covering 27–64 species and 378–2520 alignment sites. Sources include Hedges et al., Garey et al., Yang & Yoder, Henk et al., Lakner et al., Zhang & Blackwell, Yoder & Yang, Rossman et al.
- **Input**: Raw DNA sequences (not required to be aligned to equal length).
- **Robustness tests**: Node deletion (−4 species) and node addition (+4 species) on DS1.
- **No pre-training data for PhyloGen itself**; DNABERT2 was pre-trained on multi-species genomes (see DNABERT2 paper).

## Training Recipe

- Optimiser: Adam.
- Framework: PyTorch.
- Training details deferred to Appendix E (not fully available in extracted text); specific LR, batch size, epochs not stated in main paper.
- Multi-sample ELBO with K samples from variational distributions.
- End-to-end stochastic gradient descent through reparameterisation trick for both topology latent z and branch lengths.
- Training times on DS1 robustness settings: ~6.5 h for full model (vs 18+ h for PhyloGFN, 6–15 h for GeoPhy variants).

## Key Ablations & Design Choices

1. **KL loss removal (w/o KL)**: ELBO drops from −7005.98 → −7017.57; MLL drops from −6910.02 → −6917.34 on DS1. KL regularisation is key for avoiding overfitting and stabilising training.
2. **Scoring Function removal (w/o S)**: ELBO −7011.94, MLL −6919.39. Larger MLL degradation than ELBO degradation, suggesting S mainly helps likelihood estimation quality rather than bound tightness.
3. **Feature extraction ablation (One-Hot vs DNABERT2)**: One-hot leaf-node encoding yields the worst MLL by a large margin — confirms DNABERT2 embeddings are essential for capturing evolutionary signal.
4. **Distance matrix choice**: Replacing the XOR-based latent distance D with Euclidean or cosine distance greatly degrades MLL. The designed distance captures nucleotide mismatches more effectively.
5. **Hidden dimension (768 → 64)**: Reducing hidden dims lowers MLL but convergence remains stable — model is somewhat robust to capacity reduction.
6. **Layer normalisation removal (w/o LN)**: Lowers MLL, confirming LN aids training dynamics.
7. **Scoring Function architecture (FC vs MLP-2 vs MLP-3)**: All track ELBO similarly (cosine similarity > 0.8); FC chosen for closest alignment. Number of MLP layers has little impact.
8. **Robustness to data perturbation**: PhyloGen shows small positive Δ in ELBO/MLL after node addition/deletion, while baselines (GeoPhy, PhyloGFN) show large negative Δ — substantially more robust.
9. **Topological diversity**: Simpson's Diversity Index 0.89 (vs MrBayes 0.87, GeoPhy 0.36); Top Frequency 0.008 (vs 0.27, 0.80); 149 distinct topologies in top-95% (vs 42, 11). PhyloGen explores topology space more broadly than baselines.
10. **Joint vs separate optimisation**: Unlike prior VI methods (ARTree, GeoPhy) that optimise topology and branch lengths separately, PhyloGen's joint optimisation yields best MLL/ELBO across all 8 datasets.

## Reported Insights

- Framing phylogenetic inference as conditional graph-structure generation (rather than learning from pre-generated topologies) removes the bottleneck of MCMC-generated candidates.
- Pre-trained genomic LM embeddings capture long-range sequence dependencies that one-hot or hand-crafted features miss, enabling topology inference from unaligned sequences.
- The auxiliary Scoring Function provides complementary gradient information to ELBO, smoothing optimisation landscape without adding significant compute.
- Bipartition frequency distributions closely match MrBayes gold standard, validating biological plausibility of generated trees.
- Computational efficiency is competitive: ~6.5 h vs 18+ h for PhyloGFN on comparable settings.

## References Worth Chasing

- **DNABERT2** (Zhou et al., 2023; ref [49]) — the frozen backbone providing genomic embeddings.
- **ARTree** (Xie & Zhang, 2024; ref [36]) — strongest baseline; deep autoregressive phylogenetic model.
- **GeoPhy** (Mimori & Hamada, 2024; ref [22]) — continuous geometric space approach to tree topologies.
- **PhyloGFN** (Zhou et al., 2023; ref [48]) — GFlowNet-based phylogenetic inference.
- **VBPI-GNN** (Zhang, 2023; ref [44]) — GNN-enhanced variational Bayesian phylogenetic inference.
- **DGCNN** (Wang et al., 2019; ref [35]) — dynamic graph CNN used for branch-length feature enhancement.

## Notes / Open Questions

- Paper does not report total parameter count for PhyloGen-specific modules; only the DNABERT2 backbone size is known (~117M from original paper).
- No training token count or compute budget reported.
- Datasets are small (27–64 taxa); scalability to larger phylogenies (hundreds/thousands of species) is acknowledged as future work.
- The NJ algorithm used for initial topology construction is computationally intensive and may become a bottleneck at scale; authors mention exploring parallel processing.
- Extension to protein and single-cell data is listed as future work but not demonstrated.
- Whether DNABERT2 is frozen or fine-tuned is not fully explicit, though the paper says "pre-trained" and does not mention fine-tuning the LM.
