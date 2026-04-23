---
id: multimodal-3d-genome-pre-2025
title: Multimodal 3D Genome Pre-training
authors:
- Minghao Yang
- Pengteng Li
- Yan Liang
- Qianyi Cai
- Zhihang Zheng
- Shichen Zhang
- Pengfei Zhang
- Zhi-An Huang
- Hui Xiong
year: 2025
venue: null
arxiv: '2504.09060'
doi: null
url: https://arxiv.org/abs/2504.09060v2
pdf_path: papers/multimodal-3d-genome-pre-2025.pdf
md_path: papers/md/multimodal-3d-genome-pre-2025.md
modalities:
- epigenome
- interactome
status: extracted
evidence_quality: high
tags:
- foundation-model
- 3d-genome
- hi-c
- chromatin
- self-supervised
- contrastive-learning
- multimodal-fusion
- pre-training
- cross-modal-mapping
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:08+00:00'
updated_at: '2026-04-22T20:23:01+00:00'
is_fm: true
fm_classification_reason: Self-supervised pretraining for 3D-genome multimodal FM.
---

## TL;DR

MIX-HIC is the first multimodal foundation model for 3D genomics, integrating Hi-C contact maps and epigenomic tracks (ATAC-seq, DNase-seq) via self-supervised pre-training on 1.28M paired samples across 4 cell lines. Uses dual Transformer encoders with cross-modal interaction (contrastive + orthogonal loss) and cross-modal mapping blocks to learn modal-invariant and modal-specific representations. Achieves SOTA on Hi-C prediction, chromatin loop detection, and CAGE-seq expression prediction, and can infer missing Hi-C modality from epigenomic tracks alone.

## Model

- **Name**: MIX-HIC
- **Architecture**: Dual-encoder Transformer. Hi-C encoder: ViT-style, patches 2×2 from 50×50 contact maps → 3 cascaded encoder layers (each = T=2 Transformer blocks + downsampling) → bottleneck. Epigenomic encoder: 4 conv layers + max-pooling → 3 cascaded Transformer encoder layers → bottleneck. Feature dim C=128 (Hi-C/loop tasks) or 256 (CAGE-seq).
- **Cross-modal interaction block**: 4 independent dense networks produce modal-invariant and modal-specific representations from each modality. Regularized by contrastive loss (SimCLR-style, τ=0.07) and orthogonal loss (inner product minimization between invariant and specific features).
- **Cross-modal mapping block**: 1D adaptive pooling + dense layers to map one modality's concatenated representation to the other's sequence length. Trained with L2 mapping loss. Enables missing-modality inference at test time.
- **Modality fusion (fine-tuning)**: T=2 contact-map-grounded fusion blocks (self-attention on epigenomic queries, cross-attention with Hi-C keys/values, FFN).
- **Task decoders**: Binary classification head (loop detection), regression with U-Net-like skip connections (CAGE-seq), outer-product feature reconstruction (Hi-C map prediction).
- **Parameters**: Not reported. Architecture is relatively compact (T=2 blocks per layer, 4 encoder layers, C=128/256).
- **Three model variants**: MIX-HIC-Bimodal (both inputs), MIX-HIC-NonPre (no pre-training), MIX-HIC-Infer (epigenomic-only with inferred Hi-C).

## Data

- **Pre-training**: 1,275,948 paired samples (Hi-C + epigenomic tracks) from 4 cell lines: HepG2 (38.5K), HCT116 (189K), IMR90 (317K), WTC11 (732K). Filtered ~30% low-signal windows (<10% non-zero Hi-C contacts). Human genome hg38 assembly.
- **Input representation**: Hi-C contact maps = 50×50 matrices at 5kb resolution (250kb genomic windows). Epigenomic tracks = 5,000-length sequences (two 250kb regions averaged over 100bp bins, concatenated; 2 channels: ATAC-seq + DNase-seq). KR normalization for Hi-C, RPGC normalization for epigenomic tracks, log-transformed.
- **Downstream evaluation**: GM12878 and K562 cell lines. Hi-C prediction (~16K/15K samples), chromatin loop detection (1.34M/138K positive loops from ChIA-PET + matched negatives), CAGE-seq expression (~16K/15K samples). Train/val/test split by chromosome (chr10,11 = val; chr3,13,17 = test).
- **Sources**: 4DN Data Portal (Hi-C), ENCODE Portal (ATAC-seq, DNase-seq, CAGE-seq, CTCF ChIA-PET).

## Training Recipe

- **Pre-training**: 500 epochs, lr=1e-5, batch size=256, AdamW (β1=0.9, β2=0.999). Loss = L_con + L_orth + L_mapping. Single Tesla A100 GPU.
- **Fine-tuning**: max 200 epochs, early stopping patience=20, batch size=64, AdamW. Lr=1e-4 for CAGE-seq, 1e-5 for Hi-C/loops. C=256 for CAGE-seq, C=128 for Hi-C/loops.
- **Loss functions**: MSE for Hi-C prediction and CAGE-seq regression; BCE for loop detection.
- **Normalization**: KR for Hi-C, RPGC for epigenomic, log(x+1) transform on both.

## Key Ablations & Design Choices (MOST IMPORTANT)

1. **Theorem 1 (information gap)**: Perfect bimodal alignment loses modal-specific information; prediction error increases by ≥Γ_q. Motivates separating modal-invariant from modal-specific features rather than naïve alignment.
2. **Loss ablation (Table 5, chromatin loop AUROC)**:
   - L_con only: 0.914/0.910 (GM12878/K562)
   - +L_orth: 0.918/0.916 (+~0.5%)
   - +L_mapping: 0.921/0.919 (full model). Orthogonal loss critical for feature diversity; mapping loss modest but enables missing-modality inference.
3. **Modality ablation (Table 6)**: Pre-trained bimodal > non-pre-trained bimodal > single-modality. Non-pre-trained bimodal can underperform single Hi-C (K562 loops: 0.886 vs 0.907), showing naive fusion hurts without proper pre-training. Inferred Hi-C from epigenomic tracks improves over epigenomic-only (e.g., Hi-C prediction R²: 0.872 vs 0.848 on GM12878).
4. **Hyperparameter sensitivity (Figures 7-8)**: T=2 Transformer blocks optimal across tasks; C=128 best for Hi-C/loops, C=256 for CAGE-seq. Model robust to parameter variations — "sweet spot" with moderate capacity avoids overfitting on small downstream datasets.
5. **Orthogonal constraint validation (Table 9)**: Inner products between invariant/specific features drop from ~1.0 to ~1e-5 with constraint, confirming near-orthogonal separation.
6. **Few-shot (Figure 4)**: With 10% training data, MIX-HIC-Bimodal matches full-data SOTA (AUROC ~0.9). Pre-training provides strong data efficiency.
7. **Cross-cell-type generalization (Figure 5)**: Performance drops on out-of-distribution cell lines but MIX-HIC-Bimodal maintains superiority, indicating robust transfer.
8. **Noise robustness (Table 11)**: At 70% contact perturbation, Peakachu drops to 0.509 AUROC (near random); MIX-HIC retains 0.875. Pre-training on 1M+ samples learns robust representations.
9. **In silico perturbation (Table 10)**: Attenuating epigenomic signals at CTCF loop anchors systematically reduces loop recall (100% → 0%), confirming model is biologically grounded.

## Reported Insights

- First multimodal foundation model for 3D genomics; establishes new paradigm integrating Hi-C and epigenomic data.
- Largest paired 3D genome dataset to date (1.28M samples).
- Cross-modal mapping enables practical use when Hi-C data is unavailable (common due to high sequencing costs).
- Best gains in Hi-C contact map prediction (+9.3% R² over runner-up), moderate in CAGE-seq (+3-4.3%), consistent in loop detection (+2-4% F1).
- Model predictions are mechanistically grounded in biologically relevant epigenomic features (CTCF perturbation experiment).
- Accepted at NeurIPS 2025.

## References Worth Chasing

- **Epiphany** (Yang et al., 2023): Hi-C prediction from 1D epigenomic signals only — direct predecessor for the epigenomic-only paradigm.
- **EPCOT** (Zhang et al., 2023): Generalizable framework for epigenome/chromatin/transcriptome prediction — key multi-task baseline.
- **GraphReg** (Karbalayghareh et al., 2022): Graph attention networks integrating epigenomic tracks + Hi-C for expression prediction.
- **C.Origami** (Tan et al., 2023): Cell-type-specific 3D chromatin prediction — multimodal but DNA-sequence-dependent.
- **VQDNA** (Li et al., 2024): Adaptive tokenization for DNA via VQ codebooks — relevant genomic FM.
- **RefHiC** (Zhang & Blanchette, 2023): Contrastive pre-training for Hi-C, but limited to small-scale.

## Notes / Open Questions

- Total parameter count not reported; architecture seems relatively small (T=2 per layer, C=128/256). Scaling behavior unknown.
- Only 2 epigenomic tracks used (ATAC-seq, DNase-seq); authors acknowledge future work to incorporate histone marks, methylation, etc.
- Pre-training on 4 cell lines only; generalization to diverse tissues/conditions untested beyond GM12878/K562 fine-tuning.
- No DNA sequence input — unlike EPCOT/C.Origami. Trade-off: simpler input but potentially missing sequence-level regulatory grammar.
- Code available: https://github.com/myang998/MIX-HIC

## Ablations (Rev 4)

| Variable | Settings | Metric/dataset | Result | Conclusion |
|---|---|---|---|---|
| Loss terms (Table 5) | L_con only | AUROC, chromatin loop detection (GM12878 / K562) | 0.9136 / 0.9099 | Contrastive loss alone is a strong baseline. |
| Loss terms (Table 5) | L_con + L_orth | AUROC, chromatin loop detection (GM12878 / K562) | 0.9183 / 0.9156 | Orthogonal loss adds ~0.5% AUROC by separating modal-invariant vs modal-specific features. |
| Loss terms (Table 5) | L_con + L_orth + L_mapping (full) | AUROC, chromatin loop detection (GM12878 / K562) | 0.9209 / 0.9194 | Cross-modal mapping yields a modest extra gain and enables missing-modality inference. |
| Modality (Table 6) — Hi-C contact map prediction | Epi only, no pre-training | R² (GM12878 / K562) | 0.8481 / 0.7709 | Single-modal baseline. |
| Modality (Table 6) — Hi-C contact map prediction | Epi + inferred Hi-C, pre-trained | R² (GM12878 / K562) | 0.8724 / 0.8001 | Cross-modal mapping recovers Hi-C information, improving over epi-only. |
| Modality (Table 6) — Chromatin loop detection | Epi only, no pre-training | AUROC (GM12878 / K562) | 0.8236 / 0.8054 | Epi-only baseline. |
| Modality (Table 6) — Chromatin loop detection | Epi + inferred Hi-C, pre-trained | AUROC (GM12878 / K562) | 0.8494 / 0.8226 | Inferred Hi-C still helps when true Hi-C absent. |
| Modality (Table 6) — Chromatin loop detection | Hi-C only, no pre-training | AUROC (GM12878 / K562) | 0.9065 / 0.9072 | Hi-C alone is the strongest unimodal signal for loops. |
| Modality (Table 6) — Chromatin loop detection | Inferred Epi + Hi-C, pre-trained | AUROC (GM12878 / K562) | 0.9135 / 0.9159 | Pre-training + inferred epi outperforms Hi-C alone. |
| Modality (Table 6) — Chromatin loop detection | Bimodal, no pre-training | AUROC (GM12878 / K562) | 0.9091 / 0.8859 | Naïve bimodal underperforms unimodal Hi-C on K562 due to heterogeneity. |
| Modality (Table 6) — Chromatin loop detection | Bimodal, pre-trained (full) | AUROC (GM12878 / K562) | 0.9209 / 0.9194 | Pre-training is essential to make bimodal fusion beneficial. |
| Modality (Table 6) — CAGE-seq expression | Epi only, no pre-training | R² (GM12878 / K562) | 0.8514 / 0.8710 | Epi-only baseline. |
| Modality (Table 6) — CAGE-seq expression | Epi + inferred Hi-C, pre-trained | R² (GM12878 / K562) | 0.8684 / 0.8870 | Inferred Hi-C improves expression prediction. |
| Modality (Table 6) — CAGE-seq expression | Bimodal, no pre-training | R² (GM12878 / K562) | 0.8614 / 0.8755 | Bimodal without pre-training gives only marginal gains. |
| Modality (Table 6) — CAGE-seq expression | Bimodal, pre-trained (full) | R² (GM12878 / K562) | 0.8833 / 0.9077 | Pre-trained bimodal best across all three tasks. |
| Feature dimension C (Fig. 7) | C ∈ {64, 128, 256} | Hi-C contact map & chromatin loops vs CAGE-seq (GM12878, K562) | C=128 best for Hi-C / loops; C=256 best for CAGE-seq | Moderate width is optimal; performance robust to choice. |
| Transformer depth T (Fig. 8) | T ∈ {2, 4, 8} | All 3 downstream tasks (GM12878, K562) | T=2 most robust across tasks | Shallow encoder/decoder suffices; deeper risks overfitting on task-specific fine-tuning data. |
| Orthogonal constraint (Table 9) | With vs without L_orth | Inner product of modal-invariant vs modal-specific features (GM12878, K562) | With: ≤3e−3; Without: up to 1.42 (Hi-C, GM12878) | Orthogonal loss yields near-orthogonal representations, validating Theorem 1 (rigid alignment is harmful; promote diversity instead). |
| In silico CTCF anchor perturbation (Table 10) | Down-sample epi signal at anchors at ratio 0.0/0.5/0.7/0.8/0.9 | Recall of 118 CTCF-mediated K562 loops (MIX-HIC-InferMap) | 100% / 98% / 61% / 15% / 0% | Loop predictions are mechanistically driven by epigenomic signal at anchors — biologically grounded. |

### Take-aways

- **Pre-training is the load-bearing component**: bimodal fusion *without* pre-training can underperform unimodal Hi-C (e.g., K562 loops 0.8859 vs 0.9072), but bimodal *with* pre-training is best on every task — pre-training, not multimodality per se, drives the gains.
- Orthogonal constraint contributes a small AUROC bump (~0.5%) but a large representational effect (inner products drop ~3 orders of magnitude), supporting the diversity-not-strict-alignment thesis.
- Cross-modal mapping is more valuable for *practical deployment* (imputing missing Hi-C) than for benchmark headroom — gains over L_con+L_orth are modest (~0.3%).
- Architecture is in a "sweet spot" at C≈128, T=2: shallow and narrow, indicating data — not parameters — is currently the bottleneck.
- Biological grounding is empirically demonstrated: attenuating CTCF-anchor epigenomic peaks monotonically destroys loop recall.
