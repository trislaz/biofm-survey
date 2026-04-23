---
id: learning-from-protein-structure-2020
title: Learning from Protein Structure with Geometric Vector Perceptrons
authors:
- Bowen Jing
- Stephan Eismann
- Patricia Suriana
- Raphael J. L. Townshend
- Ron Dror
year: 2020
venue: ICLR 2021
arxiv: '2009.01411'
doi: null
url: https://arxiv.org/abs/2009.01411v3
pdf_path: papers/learning-from-protein-structure-2020.pdf
md_path: papers/md/learning-from-protein-structure-2020.md
modalities:
- protein-structure
status: extracted
evidence_quality: full-text
tags:
- GNN
- equivariant
- geometric
- message-passing
- protein-design
- model-quality-assessment
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T21:55:39+00:00'
updated_at: '2026-04-22T21:55:41+00:00'
---

## TL;DR

GVP-GNN introduces **Geometric Vector Perceptrons** — a drop-in replacement for MLPs in GNN message-passing layers that operates on tuples of scalar features (s ∈ ℝⁿ) and 3D vector features (V ∈ ℝ^{ν×3}). The vector pathway is SE(3)-equivariant (rotations/reflections), enabling direct geometric reasoning without reducing geometry to hand-crafted scalar invariants. Evaluated on two protein-structure tasks — computational protein design (CPD) and model quality assessment (MQA) — GVP-GNN sets new SOTA on CATH 4.2 (perplexity 5.29 vs 6.55 for Structured GNN) and CASP 11-13 MQA benchmarks. Not a foundation model; a task-specific architecture contribution.

## Model

- **Architecture**: Message-passing GNN with GVP layers replacing standard dense/MLP layers.
- **GVP layer**: Takes (s, V) → (s′, V′). Two linear transforms W_h, W_m on vectors; L2 norms of transformed vectors are concatenated with scalar features before a scalar linear transform W_m and nonlinearity σ. Vectors are scaled element-wise by σ⁺(‖·‖₂). An extra projection W_µ controls output vector dimensionality independently.
- **Equivariance**: Vector outputs are equivariant and scalar outputs are invariant under arbitrary rotations/reflections in ℝ³ (proved). Universal approximation of continuous rotation-invariant scalar functions (proved, for ν ≥ 3).
- **Graph construction**: Protein backbone represented as k=30 nearest-neighbor graph over Cα atoms. Node features: sin/cos of dihedral angles (φ, ψ, ω), forward/reverse unit vectors, imputed Cβ direction, one-hot amino-acid identity. Edge features: unit direction vector, Gaussian RBF distance encoding (16 centres, 0–20 Å), sinusoidal positional encoding of sequence separation.
- **Propagation**: 3 graph propagation layers (message = 3-layer GVP on concat(h_v^j, h_e^{j→i}); aggregation = mean + residual + LayerNorm + Dropout), interleaved with 2-layer GVP feed-forward blocks with residual connections.
- **CPD head**: Autoregressive masked encoder-decoder (3 encoder + 3 decoder propagation steps) → 20-way softmax via final GVP.
- **MQA head**: Node-wise GVP → scalar → global mean pooling → dense feed-forward → scalar regression.
- **Hidden dims**: 16 vector + 100 scalar channels (nodes/hidden); 1 vector + 32 scalar channels (edges).
- **Parameter count**: Not reported for real tasks. Synthetic-task variant: 22k params (vs 59k CNN, 40k GNN).
- **Vector-specific techniques**: Vector dropout (drops entire vector channels, not coordinates); vector layer norm (scale by RMS norm, no learnable params); standard layer norm on scalar channels.

## Data

| Dataset | Task | Split | Structures | Targets/Proteins |
|---------|------|-------|------------|------------------|
| CATH 4.2 (Ingraham et al. 2019) | CPD | Train / Val / Test | 18,204 / 608 / 1,120 | Partitioned by CATH class (40% non-redundancy) |
| TS50 (Li et al. 2014) | CPD | Test only | 50 | Filtered CATH train/val to <30% seq similarity |
| CASP 5-10 | MQA | Train + Val | 79,200 candidate structures | 528 targets (480 train / 48 val); 150 candidates/target; includes natives |
| CASP 11 | MQA | Test | 1,680 (stage 1) + 12,450 (stage 2) | 84 / 83 targets |
| CASP 12 | MQA | Test | 800 (stage 1) + 5,950 (stage 2) | 40 targets |
| CASP 13 | MQA | Test | 1,472 (stage 2) | 20 targets |

No pre-training; models are trained from scratch on each task.

## Training Recipe

- **Framework**: TensorFlow 2.1
- **Optimizer**: Adam
- **Loss (CPD)**: Cross-entropy / negative log-likelihood
- **Loss (MQA)**: Huber absolute loss + Huber pairwise ranking loss (pairs of candidates for same target); pairwise term also improves global correlation
- **Batching**: Group structures by size; max 1,800 residues/batch (CPD), 3,000 residues/batch (MQA)
- **Epochs**: Max 100
- **Hardware**: Single NVIDIA Titan X GPU; ~2 days per task; GPU memory (not compute) is the bottleneck
- **Hyperparameter search**: 70 runs total; tuned learning rate (10⁻⁴–10⁻³), dropout (10⁻⁴–10⁻¹), propagation layers (3–6), MQA pairwise loss weight (0–2)
- **Code**: https://github.com/drorlab/gvp

## Key Ablations & Design Choices

From Table 4 (CPD on CATH 4.2 All; MQA on CASP 11/12 Stage 2):

| Variant | CPD Perplexity ↓ | CPD Recovery ↑ | MQA CASP11-S2 Glob/Per | MQA CASP12-S2 Glob/Per |
|---------|------------------|----------------|------------------------|------------------------|
| **GVP-GNN (full)** | **5.29** | **40.2%** | **0.87 / 0.45** | **0.82 / 0.62** |
| MLP layer (replace GVP) | 7.76 | 30.6% | 0.84 / 0.36 | 0.79 / 0.59 |
| Only scalars (no vectors) | 7.31 | 32.4% | 0.84 / 0.38 | 0.83 / 0.59 |
| Only vectors (no scalars) | 11.05 | 23.2% | 0.56 / 0.16 | 0.57 / 0.39 |
| No W_µ projection | 5.85 | 37.1% | 0.86 / 0.41 | 0.81 / 0.60 |
| Structured GNN (baseline) | 6.55 | 37.3% | — | — |
| GraphQA (baseline) | — | — | 0.82 / 0.38 | 0.81 / 0.61 |

**Key takeaways**:
- Removing direct geometric (vector) access (MLP layer or only-scalars) degrades CPD perplexity by 38–47% — geometric reasoning is critical.
- Only-vectors is worst: eliminates scalar inputs (torsion angles, AA identity) and loses the approximation guarantee that requires scalar+vector coupling.
- Dual scalar/vector design is essential — without either pathway, the model falls below Structured GNN on CPD and only matches GraphQA on MQA.
- W_µ projection contributes a modest but consistent improvement across all metrics.
- DimeNet (SO(3)-invariant GNN for small molecules) fails to scale to protein graphs (CASP11-S2 global 0.61 vs GVP-GNN 0.87) due to edge-pair message passing cost.

Synthetic tasks (Table 5, 22k params): GVP-GNN achieves 0.206 MSE on geometric task (vs CNN 0.319, GNN 0.871) and 0.106 on relational task (vs GNN 0.128, CNN 0.532), and 0.155 on combined (vs GNN 0.421, CNN 0.522) — confirming it unifies geometric + relational reasoning.

## Reported Insights

- **Geometric + relational unification**: The core thesis is that protein-structure learning requires both geometric reasoning (shape, orientations) and relational reasoning (residue-residue interactions). GVP-GNN is the first architecture to address both simultaneously via equivariant vector features in a GNN.
- **Efficiency of absolute orientation**: Encoding one absolute orientation per node (3 vectors) is more efficient than encoding all pairwise relative orientations, and enables direct propagation of geometric features across the graph without local-to-global coordinate transforms.
- **Lightweight equivariance**: GVP offers a computationally cheaper alternative to irreducible-representation-based SO(3) equivariant convolutions (e.g., Tensor Field Networks, Cormorant), making it practical for large biomolecules.
- **Learned vector features are interpretable**: Visualized intermediate vector channels in the MQA model appear to capture meaningful structural properties (e.g., pointing toward protein center, along helix axes, outward/inward from surface).
- **Pairwise MQA loss helps global correlation**: Adding a pairwise ranking loss term to the absolute Huber loss improves global correlation, likely because the larger number of possible pairs acts as regularization.

## References Worth Chasing

- **Ingraham et al. 2019** — Structured Transformer for graph-based protein design; provides the CATH 4.2 benchmark and autoregressive formulation used here.
- **Baldassarre et al. 2020** — GraphQA: GNN baseline for MQA; provides CASP benchmark data.
- **Thomas et al. 2018** — Tensor Field Networks: SO(3)-equivariant convolutions on point clouds; theoretical predecessor for equivariant geometric reasoning.
- **Eismann et al. 2020** — Hierarchical rotation-equivariant networks for protein complexes; related work from same lab using irreducible representations.
- **Klicpera et al. 2019** — DimeNet: directional message passing for molecular graphs; compared unfavorably on proteins due to scaling issues.
- **Strokach et al. 2020** — ProteinSolver: GNN for CPD and mutation stability; alternative graph-based approach.

## Notes / Open Questions

- **Not a foundation model**: GVP-GNN is a task-specific supervised architecture, not a pre-trained/fine-tuned foundation model. No self-supervised pre-training or transfer learning. Relevant to the survey as an influential architecture component adopted by later protein foundation models.
- **Parameter count not reported** for the real-task models (only 22k for the synthetic variant). The hidden dimensions (16 vec + 100 scalar nodes, 1 vec + 32 scalar edges, 3 propagation layers) suggest a relatively small model, likely in the low hundreds of thousands of parameters.
- **Backbone-only representation**: Side chains are not modeled (unknown in CPD, and MQA benchmark is backbone-only). Limits applicability to tasks involving side-chain geometry.
- **No sequence information in MQA**: The MQA model uses only structure, yet outperforms ProQ3D which additionally uses sequence profiles — suggesting strong geometric inductive bias.
- **Follow-up work**: GVP has been widely adopted — notably in GVP-Transformer (Jing et al. 2021, NeurIPS) which adds Transformer attention, and integrated into ESM-IF (Hsu et al. 2022) for inverse folding. Worth tracking the lineage.
- **k=30 neighbors**: The choice of 30 nearest neighbors (~13 Å radius) is notably large; no ablation on k is provided.
- **TensorFlow implementation**: Original code in TF 2.1; community PyTorch reimplementations exist (e.g., PyG-based). The GitHub repo is https://github.com/drorlab/gvp.
