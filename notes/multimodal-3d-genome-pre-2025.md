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
