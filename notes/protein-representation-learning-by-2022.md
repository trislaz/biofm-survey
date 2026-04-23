---
id: protein-representation-learning-by-2022
title: Protein Representation Learning by Geometric Structure Pretraining
authors:
- Zuobai Zhang
- Minghao Xu
- Arian Jamasb
- Vijil Chenthamarakshan
- Aurelie Lozano
- Payel Das
- Jian Tang
year: 2022
venue: ICLR 2023
arxiv: '2203.06125'
doi: null
url: https://arxiv.org/abs/2203.06125v5
pdf_path: papers/protein-representation-learning-by-2022.pdf
md_path: papers/md/protein-representation-learning-by-2022.md
modalities:
- protein-structure
status: extracted
evidence_quality: full-text
tags:
- SSL
- contrastive
- distance
- angle-prediction
- dihedral-prediction
- masked-inverse-folding
- self-prediction
- GNN
- relational-message-passing
- edge-message-passing
- protein-function
- fold-classification
parameters: 42000000
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T21:55:34+00:00'
updated_at: '2026-04-22T21:55:38+00:00'
is_fm: true
fm_classification_reason: 'GearNet: self-supervised pretrained protein structure encoder.'
---

## TL;DR

GearNet is a relational graph neural network for protein structure representation learning. It introduces edge message passing on residue graphs and five self-supervised pretraining objectives (multiview contrastive learning + four self-prediction tasks). Pretrained on only 805K AlphaFold-predicted structures, GearNet matches or beats sequence-based models (ESM-1b, ProtBERT-BFD) pretrained on 24M–2.1B sequences across EC, GO, fold, and reaction benchmarks.

## Model

- **GearNet** (GeomEtry-Aware Relational Graph Neural Network): residue-level relational GNN operating on protein 3D structure graphs.
- Graph construction uses three edge types: sequential edges (within distance 2 in sequence, 5 subtypes by relative position), radius edges (Euclidean < 10 Å), and K-nearest-neighbor edges (k=10). Long-range filter removes spatial edges between residues with sequence distance < 5. Total 7 edge types.
- Node features: one-hot residue type (21-dim). Edge features: concat of node features, edge type one-hot, sequential distance, Euclidean distance.
- **Relational graph convolutional layer**: separate kernel matrix W_r per edge type (Eq. 1), with batch norm, ReLU, and residual connections.
- **GearNet-Edge**: adds a sparse edge message passing layer on the line graph of the residue graph. Edge-edge interactions are typed by discretized angles between adjacent edges (8 bins over [0, π]). First work to use edge message passing for macromolecular representation learning.
- **GearNet-IEConv / GearNet-Edge-IEConv**: augmented with a simplified IEConv layer for better fold classification.
- Architecture: 6 relational GCN layers, 512 hidden dim. GearNet-Edge has **42M parameters** (Table 3).
- E(3)-invariant by construction (distances + angles only).

## Data

- **Pretraining**: AlphaFold Protein Structure Database v1 (365K proteome-wide) + v2 (440K Swiss-Prot) = **805K predicted structures** total. CC-BY 4.0 license.
- **Downstream benchmarks**:
  - Enzyme Commission (EC): 15,550 / 1,729 / 1,919 train/val/test; 538 binary tasks.
  - Gene Ontology (GO-BP, GO-MF, GO-CC): 29,898 / 3,322 / 3,415.
  - Fold Classification (SCOPe 1.75): 12,312 / 736 / 718–1,272 across three splits (Fold, Superfamily, Family).
  - Reaction Classification: 29,215 / 2,562 / 5,651; 384 classes.
- Also tested pretraining on PDB alone (305K experimentally-determined chains) with comparable results (Table 8).

## Training Recipe

- **Pretraining**: Adam optimizer, lr=0.001, 50 epochs on 4× Tesla A100 GPUs.
  - Multiview Contrast: subsequence crop length 50, subspace radius 15, edge mask rate 0.15, temperature τ=0.07, batch size 96 (GearNet-Edge) / 24 (GearNet-Edge-IEConv).
  - Self-prediction tasks: 256 sampled pairs (Distance), 512 sampled items (Residue Type, Angle, Dihedral); batch 128 / 96 (GearNet-Edge).
- **Fine-tuning**: 200 epochs (EC, GO) / 300 epochs (Fold, Reaction). Adam lr=1e-4 (EC, GO) or SGD lr=1e-3 + weight decay 5e-4 (Fold, Reaction). Batch size 2 per GPU. ReduceLROnPlateau (EC, GO) / StepLR (Fold, Reaction). Hidden representations from all 6 layers concatenated for prediction via 3-layer MLP.
- Best from-scratch model selected for pretraining: GearNet-Edge (EC, GO, Reaction), GearNet-Edge-IEConv (Fold).

## Key Ablations & Design Choices

Five SSL objectives compared head-to-head on all benchmarks:

| Method | EC (Fmax) | GO-BP | GO-MF | GO-CC | Fold Avg. | Reaction |
|---|---|---|---|---|---|---|
| No pretraining (GearNet-Edge) | 0.810 | 0.403 | 0.580 | 0.450 | 69.9 | 86.6 |
| Residue Type Prediction | 0.843 | 0.430 | 0.604 | 0.465 | 73.0 | 86.6 |
| Distance Prediction | 0.839 | 0.448 | 0.616 | 0.464 | 74.6 | 87.5 |
| Angle Prediction | 0.853 | 0.458 | 0.625 | 0.473 | 77.4 | 86.8 |
| Dihedral Prediction | 0.859 | 0.458 | 0.626 | 0.465 | 75.9 | 87.0 |
| **Multiview Contrast** | **0.874** | **0.490** | **0.654** | **0.488** | **78.1** | **87.5** |

Additional ablations:
- **Relational conv. matters**: removing it (shared kernel across edge types) drops EC from 0.810 → 0.752 at same depth, and worse with more layers (0.744 at 10 layers / 60M params).
- **Edge message passing**: consistent improvements across all tasks (GearNet → GearNet-Edge).
- **IEConv layer**: critical for fold classification (+4.3 pt avg accuracy) but marginal on function prediction.
- **Augmentation combinations** (Table 3 right): all four deterministic cropping+noise combos effective; random sampling over them yields best diversity.
- **Cropping size** (Figure 2): subsequence 50 residues and subspace radius 15 Å optimal; too large makes contrastive task trivial.
- **Pretraining dataset robustness** (Table 8): AlphaFold v1 only, v2 only, combined, or PDB all yield similar EC results — method is not sensitive to dataset choice.
- **Backbone generality** (Table 9): pretraining also improves EGNN backbone (EC 0.640 → 0.761 with Distance Prediction).

## Reported Insights

1. Structure-based pretraining on 805K structures matches sequence-based models pretrained on 24M–2.1B sequences, demonstrating an order-of-magnitude better data efficiency.
2. Multiview Contrastive Learning is the best pretraining objective (best on 7/8 benchmarks), framing biologically meaningful substructure co-occurrence as a contrastive signal.
3. Edge message passing (modeling edge-edge interactions via the line graph) is novel for macromolecular GNNs and gives consistent gains, inspired by AlphaFold2's triangle attention.
4. Combining ESM-1b sequence representations as node features with GearNet structure encoder achieves best-of-both-worlds (Table 10: EC Fmax 0.883), but no structure pretraining was applied to the combined model.
5. Neural + retrieval ensemble (GearNet + Foldseek) boosts EC Fmax to 0.903 (Table 11).
6. Learned representations enable competitive protein structure search on SCOPe40, outperforming DALI on average (Table 12).
7. Self-prediction tasks that capture local geometry (angles, dihedrals) outperform global (random dihedral sampling drops EC from 0.859 to 0.821).

## References Worth Chasing

- **Hermosilla & Ropinski 2022** — Contrastive representation learning for 3D protein structures (concurrent structure-based pretraining work, IEConv baseline).
- **Chen et al. 2022 (Structure-aware protein SSL)** — Concurrent self-prediction pretraining on structures.
- **Guo et al. 2022** — Concurrent denoising score matching pretraining on protein structures.
- **Rives et al. 2021 (ESM-1b)** — Primary sequence-based baseline; 650M-param Transformer pretrained on 24M sequences.
- **Klicpera et al. 2020 (DimeNet)** — Directional message passing for molecules; inspiration for angle-based edge interactions.
- **Jumper et al. 2021 (AlphaFold2)** — Triangle attention in Evoformer; inspiration for edge message passing.
- **You et al. 2020** — Graph contrastive learning with augmentations (general GNN pretraining framework).

## Notes / Open Questions

- Parameter count (42M for GearNet-Edge) is modest; paper was written before AlphaFold DB scaled to 200M+ structures. Scaling behavior unknown.
- Training compute not reported beyond "4× A100 GPUs, 50 epochs." No wall-clock time or FLOPs given.
- Pretraining used AlphaFold-predicted (not experimental) structures; comparable results on PDB suggest robustness to prediction noise.
- Combined ESM-1b+GearNet was not pretrained with structure-based SSL — a natural follow-up.
- No MSA-based baselines included (authors cite computational burden and inferior function prediction per Hu et al. 2022).
- Multiview Contrast augmentations (subsequence/subspace cropping + edge masking) are protein-specific; transferability of these ideas to other biomolecular graphs is unexplored.
- The venue is ICLR 2023 (published as a conference paper), despite the arxiv year being 2022.

## Verification (Rev 3)

Six claims referencing `[protein-representation-learning-by-2022]` found in `insights.md`.

| # | Line | Claim (paraphrased) | Verdict | Rationale |
|---|------|----------------------|---------|-----------|
| 1 | 19 | "805K AlphaFold structures match sequence models pretrained on **billions of tokens**" | **supported** | Paper: GearNet pretrained on 805K structures matches ESM-1b (24M seqs) and ProtBERT-BFD (2.1B seqs). "Billions of tokens" is a loose synonym for 2.1B sequences but substantively correct (Table 2, §5.2). |
| 2 | 131 | "Relational graph + edge message passing; 805K AF structures match sequence models trained on 24M–2.1B sequences for structure-based tasks" | **supported** | Numbers 805K, 24M, 2.1B all match paper (§5.1, Table 2). Relational graph conv and edge message passing are the two key architectural contributions (§3.1–3.2). |
| 3 | 189 | "Multiview contrastive learning is the best SSL objective for protein structure encoders, outperforming **reconstruction-based** alternatives" | **partial** | Multiview Contrast is best on 7/8 benchmarks — correct (Table 2, §5.2). However, the four alternatives are **self-prediction** tasks (masked residue type, distance, angle, dihedral), not "reconstruction-based" in the conventional sense (e.g., autoencoders). The paper terms them "self-prediction methods" (§4.2). |
| 4 | 231 | "805K AlphaFold structures match sequence models pretrained on 24M–2.1B sequences for structure-aware tasks" | **supported** | Same evidence as Claim 2. Paper states: "pretrained with an order of magnitude less data, our model can achieve comparable or even better results" (§5.2). |
| 5 | 345 | "805K AlphaFold structures enable GearNet to match sequence models pretrained on orders-of-magnitude more sequence data" | **supported** | 805K vs 24M (~30×) and vs 2.1B (~2600×). Paper uses singular "an order of magnitude" but the range spans 1.5–3.4 orders; the plural form is defensible. |
| 6 | 485 | "GearNet with edge message passing on 805K AF structures matches sequence models at orders-of-magnitude more data" | **supported** | Same evidence as Claim 5; adds edge message passing attribution which is accurate (GearNet-Edge is the pretrained model for EC/GO/Reaction). |

**Summary:** 5 supported, 1 partial (Claim 3 — "reconstruction-based" should read "self-prediction").

## Ablations (Rev 4)

| Variable | Settings | Metric | Result | Conclusion |
|---|---|---|---|---|
| Relational graph convolution (GearNet-Edge encoder) | GearNet-Edge (6 layers, 42M params, w/ rel. conv.) vs. plain GCN baselines (single shared kernel) at 6/8/10 layers (23M/39M/60M) | Fmax on EC | 0.810 (rel. conv.) vs. 0.752 / 0.754 / 0.744 (no rel. conv., increasing depth) | Treating edges as different types is essential; param-matched plain GCN cannot recover the gap, even with more layers/params. |
| Edge message passing (Table 2 reference) | GearNet vs. GearNet-Edge (adds edge-level message passing) | Fmax on EC/GO function tasks | Consistent improvement after enabling edge message passing | Explicit edge-edge interaction modeling is beneficial across function prediction tasks. |
| Multiview Contrast augmentation: cropping × noise (deterministic vs. random) | Random sampling (default) vs. four deterministic combos: {subsequence, subspace} × {identity, random edge masking} | Fmax on EC / GO-BP / GO-MF / GO-CC | Random: **0.874 / 0.490 / 0.654 / 0.488**; subseq+identity 0.866/0.477/0.627/0.473; subspace+identity 0.872/0.480/0.640/0.468; subseq+edgemask 0.869/0.484/0.641/0.471; subspace+edgemask 0.876/0.481/0.645/0.470 | All four deterministic combinations work, so each cropping/noise scheme yields informative views; randomly sampling combinations gives the most diverse views and is best on 3 of 4 GO/EC metrics. |

**Take-aways:**
- Relational (edge-typed) convolution is the single most impactful architectural choice: +~0.06 Fmax on EC over a parameter-matched plain GCN, an effect that does not close with extra depth.
- Edge message passing gives a smaller but consistent additional gain on function tasks, justifying the GearNet-Edge variant as the default pretraining backbone.
- Multiview Contrast is robust to the specific augmentation choice (any cropping × noise combo trains usefully); the win from random sampling comes from view diversity rather than any single augmentation, supporting the contrastive-learning rationale.
