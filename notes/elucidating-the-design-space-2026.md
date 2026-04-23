---
id: elucidating-the-design-space-2026
title: Elucidating the Design Space of Flow Matching for Cellular Microscopy
authors:
- Charles Jones
- Emmanuel Noutahi
- Jason Hartford
- Cian Eastwood
year: 2026
venue: null
arxiv: '2603.26790'
doi: null
url: https://arxiv.org/abs/2603.26790v1
pdf_path: papers/elucidating-the-design-space-2026.pdf
md_path: papers/md/elucidating-the-design-space-2026.md
modalities:
- imaging-microscopy
- small-molecule
status: extracted
evidence_quality: high
tags:
- ablation-study
- flow-matching
- generative-model
- cell-microscopy
- virtual-screening
- design-space
- diffusion-transformer
parameters: 700M
training_tokens: null
training_compute: 986 ExaFLOPs (≈1 ZettaFLOP, pretrained variant)
references_chased: false
added_at: '2026-04-22T19:42:01+00:00'
updated_at: '2026-04-22T20:19:23+00:00'
is_fm: false
fm_classification_reason: Flow matching design-space study for cellular microscopy.
---

## TL;DR

Largest-scale ablation of flow matching for cell-microscopy generative modelling. Systematically tests conditioning, interpolants, data coupling, architecture, and pretraining. Finds domain-specific intuitions (control→perturbed flows, optimal-transport coupling) are unnecessary or harmful. Develops a simple recipe scaled to ~700M params / 1 ZettaFLOP, achieving 2× FID and 10× KID improvements over prior SOTA on RxRx1. Fine-tunes with MolGPS molecular embeddings for SOTA virtual screening of unseen molecules on BBBC021.

## Model

- **Architecture**: Microscopy Transformer (MiT-XL/2) — a modified DiT-XL/2 (28 depth, 16 heads, 1152 hidden dim, patch size 2) with three stabilisation changes: (1) long-range U-Net-style skip connections, (2) RMSNorm replacing LayerNorm, (3) 10% dropout after attention projection layer.
- **Parameters**: ~700M (excluding conditioning layers). ~1 TFLOP per forward pass per 96×96×6 image.
- **Baseline compared**: ADM U-Net (50M params, 200 GFLOPs/image) — same as CellFlux.
- **Conditioning**: one-hot perturbation label + one-hot experiment label (captures batch effects). Classifier-free guidance with 0.15 drop probability per label. No gene2vec or other external embeddings at base training.
- **Flow**: Gaussian noise → all-data (N→D); controls treated as another perturbation class. Continuous-time velocity prediction with linear interpolant.
- **Solver**: Dormand-Prince 5th-order Runge-Kutta (DoPri5), ~300 NFE; power-function EMA (σ_rel=0.01).
- **For unseen molecules**: freeze base model, train a 100M-param transformer adaptor (6 depth, 6 heads, 1152 hidden) to map molecular embeddings (Morgan fingerprints or MolGPS 3B graph transformer) into conditioning space. AdaLN modulation layers remain unfrozen.

## Data

- **RxRx1** (Sypetkowski et al. 2023): 170,943 images of U2OS cells, 1071 SiRNA gene knockdowns across 3 experiments, 96×96×6 cell-painting channels. Validation: 2942 held-out images (100 perturbations). Only ~200 control images per experiment.
- **Phenoprints** (Kenyon-Dean et al. 2025): ~600k biological perturbations applied to 10B cells across 12M well images. Used for pretraining.
- **BBBC021** (Ljosa et al. 2012): 96k crops at 96×96×3 from 113 small-molecule perturbations on MCF7 cells. Seen split: 5237 images (18 compounds). Unseen split: 1979 images (8 compounds).
- Preprocessing: illumination correction, nuclear-centred 96×96 crops, uniform dequantisation U(0, 1/256), random horizontal+vertical flipping.

## Training Recipe

- Optimiser: Adam (lr=1e-4, β1=0.9, β2=0.999, ε=1e-8), constant LR schedule, gradient norm clipping 0.5.
- Precision: BF16.
- Global batch size: 256.
- **RxRx1 base (ADM ablations)**: 100k steps on 8×H100 (~80 H100-hours for Config B). 15.7 ExaFLOPs for Configs B-E.
- **RxRx1 MiT-XL/2 (Config F)**: 150k steps on 16×H100 (~500 H100-hours), 118 ExaFLOPs.
- **Pretraining (Config G)**: 1M steps on 32×H100 on Phenoprints (~4k H100-hours), then 250k finetune steps on RxRx1 on 16×H100. Total 986 ExaFLOPs ≈ 1 ZettaFLOP. Two orders of magnitude more compute than prior SOTA.
- **BBBC021**: MiT-XL/2 from scratch, 100k steps on 16×H100.
- **Adaptor fine-tuning (unseen molecules)**: 10k steps on 8×H100, batch 16/GPU.
- EMA: power-function EMA with σ_rel=0.01.
- Guidance: CFG strength 1.0 (no guidance) best for N→D configs; 2.0 best for C→P.

## Key Ablations & Design Choices

### 1. Flow construction: C→P vs N→D vs N↔D
The most impactful finding. All on ADM, 15.7 ExaFLOPs unless noted:
| Config | Flow | FID↓ | KID(×10³)↓ |
|--------|------|------|------------|
| A | C→P (control→perturbed) | 29.5 | 14.0 |
| B (undertrained, 3.93 ExaFLOPs) | N→D | 12.3 | 3.90 |
| B | N→D (noise→data) | 9.90 | 1.52 |
| C | N↔D (counterfactual) | 13.4 | 1.14 |
**Verdict**: N→D dominates. C→P prone to overfitting due to limited controls (~160 per experiment in train split). Undertrained N→D still beats fully trained C→P. N↔D gives slightly better KID but worse FID. CellFlux's claim that noise-to-data is inappropriate for batch effects is refuted — conditioning on experiment label suffices.

### 2. Optimal transport coupling
| Config | OT | FID↓ | KID(×10³)↓ |
|--------|-----|------|------------|
| B (N→D) | ✗ | 9.90 | 1.52 |
| D (N→D) | ✓ | 10.5 | 1.61 |
| C (N↔D) | ✗ | 13.4 | 1.14 |
| E (N↔D) | ✓ | 13.6 | 2.15 |
**Verdict**: OT coupling provides no benefit and slightly hurts. No meaningful reduction in NFE with adaptive DoPri5 solver either, contradicting the motivation of straighter paths.

### 3. Interpolant choice (all N→D, guidance 1.0)
| Interpolant | FID↓ | KID(×10³)↓ |
|-------------|------|------------|
| Linear | 9.90 | 1.52 |
| Variance preserving | 9.99 | 1.42 |
| Brownian bridge k=0.1 | 14.5 | 6.58 |
| Brownian bridge k=0.5 | 103 | 90.2 |
| Brownian bridge k=1.0 | 180 | 172 |
**Verdict**: Linear interpolant best. Variance-preserving comparable. Brownian bridge catastrophically degrades with increasing noise scale.

### 4. Conditioning simplification
gene2vec embeddings (CellFlux) → one-hot perturbation + one-hot experiment label. FID improved from 33.0 (CellFlux) to 29.5 (Config A) while matching other training aspects. Experiment-label conditioning is a sufficient statistic for batch effects; control images provide no additional information about them.

### 5. Architecture scaling: ADM → MiT-XL/2
| Model | Params | GFLOPs/img | FID↓ | KID(×10³)↓ |
|-------|--------|------------|------|------------|
| ADM (Config B) | 50M | 200 | 9.90 | 1.52 |
| MiT-XL/2 (best config) | 700M | 1000 | 9.07 | 0.84 |
**Verdict**: 14× more params → modest but consistent improvement.

### 6. Pixel-space DiT stabilisation (Table 6)
Tested on DiT-B/2 (all unstable by default within 100k steps):
- **Failed to stabilise**: reduced LR (1e-5), AdamW weight decay (0.01), warmup+inv-sqrt decay, Adam β2=0.995, MLP dropout, RMSNorm alone, block skip, block skip + DropPath, RMSNorm + AdaRMS.
- **Stabilised**: attention dropout (but reduced throughput), projection dropout (10%), long-range skip connections.
- **Final recipe**: projection dropout + long-range skip connections + RMSNorm (for memory/throughput, not stability).

### 7. Pretraining on Phenoprints
| Variant | ExaFLOPs | FID↓ | KID(×10³)↓ |
|---------|----------|------|------------|
| No pretraining | 118 | 9.07 | 0.84 |
| With pretraining | 986 | 9.00 | 0.74 |
**Verdict**: Modest improvement despite 8× more compute. Authors flag this as evidence that RxRx1 benchmark is saturating.

### 8. Guidance strength sweep (extended Table 4)
- C→P (Config A): best at 2.0 (FID 29.5).
- N→D (Config B): best at 1.0 (FID 9.90); guidance hurts.
- N→D+OT (Config D): best at 1.5 (FID 10.5).
- MiT-XL/2: best at 1.0 (FID 9.07); guidance hurts slightly.
- Pretrained MiT-XL/2: best at 1.0 (FID 9.00).
- Using guidance ≠ 1.0 roughly doubles NFE due to two forward passes per step.

### 9. Molecular embeddings for unseen perturbations (BBBC021)
| Conditioning | Seen FID↓ | Seen KID(×10³)↓ | Unseen FID↓ | Unseen KID(×10³)↓ |
|-------------|-----------|-----------------|-------------|-------------------|
| One-hot | 4.03 | 0.31 | N/A | N/A |
| Unconditional | 4.63 | 0.68 | 22.7 | 13.5 |
| Morgan fingerprints | 4.16 | 0.18 | 19.9 | 12.0 |
| MolGPS (3B graph transformer) | 4.12 | 0.16 | 18.5 | 9.95 |
**Verdict**: MolGPS best. Unconditional sampling (no molecule info at all) beats most prior methods on unseen — evidence that base model quality (ε_base) compensates for poor conditioning (ε_G). Gap between seen and unseen much smaller than between methods, suggesting molecular representations are the main bottleneck for virtual screening.

### 10. Overall comparison with prior SOTA (RxRx1)
| Method | FID↓ | KID(×10³)↓ | ExaFLOPs |
|--------|------|------------|----------|
| PhenDiff | 65.9 | 51.9 | 0.96 |
| IMPA | 41.6 | 29.1 | 0.39 |
| CellFlux | 33.0 | 23.8 | 7.83 |
| CellFluxV2 | 19.0 | 9.30 | 6.89 |
| Ours (best) | 9.07 | 0.84 | 118 |
| Ours (pretrained) | 9.00 | 0.74 | 986 |

## Reported Insights

1. **Domain-specific methods are unnecessary**: C→P flows, OT coupling, and gene2vec conditioning — all intuitive for microscopy — provide no benefit over standard generative modelling practices (N→D, independent coupling, one-hot + experiment label).
2. **Prior models were poorly trained**: simple recipe fixes (N→D flow, proper conditioning, sufficient training) yield 2× FID and 10× KID over CellFlux with matched compute.
3. **Two-task error decomposition**: virtual screening error ≤ ε_base (generative model error on seen perturbations) + U·ε_G (perturbation encoder error). These can be optimised independently.
4. **Molecular representations are the bottleneck**: even unconditional sampling beats most prior methods on unseen molecules, indicating base model quality compensates. The gap between Morgan fingerprints and MolGPS is modest, suggesting current molecular encoders limit virtual screening more than generative model quality.
5. **RxRx1 and BBBC021 are saturating**: pretraining on 10B cells / 600k perturbations yields only marginal improvement on RxRx1. Authors recommend RxRx3 as a more challenging benchmark.
6. **Pixel-space DiT training is unstable**: optimizer tuning alone cannot fix it; architectural changes (long-range skip connections, projection dropout) are necessary.

## References Worth Chasing

1. **CellFlux** (Zhang et al. 2025) — prior SOTA flow matching for microscopy, C→P flow.
2. **CellFluxV2** (Zhang et al. 2026) — concurrent work, DiT-XL/2 latent diffusion for microscopy.
3. **IMPA** (Palma et al. 2025) — StarGAN-based perturbation effect prediction.
4. **PhenDiff** (Bourou et al. 2024) — diffusion for counterfactual microscopy.
5. **MolGPS** (Sypetkowski et al. 2024) — 3B graph transformer for molecular representation learning.
6. **Phenoprints / ViTally** (Kenyon-Dean et al. 2025) — large-scale microscopy dataset and representation learning.
7. **CellFlow** (Klein et al. 2025) — flow matching for single-cell transcriptomics perturbation modelling.
8. **MorphoDiff** (Navidi et al. 2025) — diffusion for cellular morphology.
9. **DiT** (Peebles & Xie 2023) — scalable diffusion transformers.
10. **EDM / Karras et al. 2022** — elucidating design space of diffusion (natural images); direct inspiration.
11. **Karras et al. 2024** — improved training dynamics of diffusion models (power-function EMA, schedules).
12. **SiT** (Ma et al. 2024) — flow and diffusion with scalable interpolant transformers.
13. **MetaFlow Matching** (Atanackovic et al. 2025) — distributional embeddings for generalising across populations.
14. **STATE** (Adduri et al. 2025) — predicting cellular responses to perturbation with transcriptomics.
15. **Virtual Cells** (Noutahi et al. 2025) — virtual cell vision paper from Valence Labs.

## Notes / Open Questions

- Code released at github.com/valence-labs/microscopy-flow-matching.
- The theoretical error decomposition (Prop 3.1) is clean but relies on Lipschitz assumption on generator H and coverage assumption — practical tightness unclear.
- Benchmark saturation is a real concern: all the heavy pretraining investment yields <1 FID point on RxRx1. RxRx3 experiments would strengthen claims.
- Adaptor architecture (100M params, 6-layer MiT) for molecular conditioning is itself quite large — ablation over adaptor size not provided.
- No comparison with latent diffusion (VAE-based) approach for MiT — CellFluxV2 uses latent DiT and achieves 19.0 FID with less compute; would MiT in latent space do even better?
- Qualitative biological validation (Aurora kinase inhibitor AZ841) is encouraging but limited to one compound.
- Only cell-painting (fluorescence microscopy) modality tested; generalisability to brightfield or other imaging unclear.
- FID/KID are computed in RGB space after a fixed 6→3 channel projection — information loss may mask channel-specific quality differences.
