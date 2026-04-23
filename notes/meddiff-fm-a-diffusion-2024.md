---
id: meddiff-fm-a-diffusion-2024
title: 'MedDiff-FM: A Diffusion-based Foundation Model for Versatile Medical Image
  Applications'
authors:
- Yongrui Yu
- Yannian Gu
- Shaoting Zhang
- Xiaofan Zhang
year: 2024
venue: null
arxiv: '2410.15432'
doi: null
url: https://arxiv.org/abs/2410.15432v3
pdf_path: papers/meddiff-fm-a-diffusion-2024.pdf
md_path: papers/md/meddiff-fm-a-diffusion-2024.md
modalities:
- imaging-radiology
status: extracted
evidence_quality: medium
tags:
- diffusion-model
- 3d-ct
- foundation-model
- controlnet
- multi-task
- denoising
- anomaly-detection
- image-synthesis
- super-resolution
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:06+00:00'
updated_at: '2026-04-22T20:22:39+00:00'
---

## TL;DR

MedDiff-FM is a 3D DDPM pre-trained on 5,376 CT volumes (head/neck, chest, abdomen) that handles multi-level (image + patch) inputs with 3D position embeddings and region/anatomy conditions. Zero-shot: denoising (DiffPIR), anomaly detection, synthesis. Fine-tuned via ControlNet: super-resolution, lesion generation, lesion inpainting. Beats MAISI on conditional CT synthesis and SOTA on BMAD liver anomaly detection.

## Model

- **Architecture**: 3D conditional UNet (DDPM). Channels=32, 1 residual block, spatial transformer at 16³ resolution. Cosine noise schedule, T=1000 timesteps.
- **Patch size**: 128×128×128. Multi-level inputs: image-level (resize to patch size) or patch-level (random crop then resize). Equal probability among 3 ops.
- **Conditioning**: (1) coarse region class c_r (HaN / chest / abdomen), (2) fine-grained anatomy masks c_a from TotalSegmentator (118 classes incl. body via thresholding), (3) 3D position embedding p_e using NeRF-style sinusoidal encoding of normalized pixel coordinates in [-1,1].
- **Fine-tuning**: ControlNet adds task-specific target condition c_t (e.g., LR image for SR, lesion mask for generation). Locked + trainable copy connected via zero-conv.
- **Inference**: Patch-based sliding window with overlapping windows + smoothed noise estimates to remove boundary artifacts.
- **Parameter count**: Not reported.

## Data

- **Pre-training**: 12 public CT datasets, 5,376 volumes total — 362 HaN (StructSeg, INSTANCE2022, HaN-Seg, SegRap2023), 1,040 chest (SegTHOR, CT-RATE subset of 1000), 1,732 abdomen (AbdomenCT-1K, AMOS22, BTCV, CHAOS, WORD), 2,242 whole-body (TotalSegmentator, AutoPET). 90% train / 5% val / 5% test.
- **Preprocessing**: Resample to 1mm isotropic; whole-body CTs split into HaN/chest/abdomen by TotalSegmentator masks; region-specific HU windowing (HaN: W400/L50, chest: W1800/L-500, abdomen: W360/L60); normalize to [-1,1].
- **Downstream datasets**: Mayo 2016 (denoising, 10 patients), BMAD Liver CT (anomaly det., 3201 slices), RPLHR-CT (SR, 250 cases), MSD-Lung/MSD-Liver/MED-LN/ABD-LN (lesion gen/inpainting, 63–131 cases each). 80/20 splits for fine-tuning tasks.

## Training Recipe

- **Loss**: L1 on predicted noise.
- **Optimizer**: Adam, lr=1e-4, batch size 1, 4 gradient accumulation steps (effective batch 4).
- **Pre-training**: ~150 epochs on NVIDIA RTX 3090 GPUs (count not stated).
- **ControlNet fine-tuning**: ~10k steps per task.
- **Denoising inference (DiffPIR)**: σ_n estimated from non-test data (~0.15 for Mayo quarter-dose); λ=10; starts from intermediate t_start derived from noise level.
- **Anomaly detection inference**: Fixed forward-diffusion step t=950 on masked abnormal image; reconstruct healthy; threshold anomaly map.
- **Super-resolution inference**: DiffPIR with σ_n=1.0, λ=1, sf=5 in depth, 100 NFEs uniform skipping from T.

## Key Ablations & Design Choices

- **Incremental component ablation (Table III)**: Patch-level DDPM baseline → +multi-level integration → +position coordinates → +position embedding. Each step improves overall FID (0.1096→0.0819→0.0667→0.0655) and Dice (0.6466→0.7844→0.8141→0.8183). Multi-level integration gives the largest single jump; position embedding adds smaller but consistent gains.
- **Multi-level input strategy**: Randomly choosing among resize-to-patch, crop-2x-then-resize, and crop-to-patch with equal probability is critical for handling diverse CT resolutions/spacings.
- **Position embedding vs raw coordinates**: Sinusoidal (NeRF-style) encoding of 3D coordinates outperforms raw coordinate channels, improving FID and Dice across all regions.
- **Region + anatomy conditioning**: Coarse region labels plus fine-grained TotalSegmentator masks let a single model span head-to-abdomen while capturing organ-specific intensity patterns.
- **Zero-shot vs fine-tuned**: Denoising and anomaly detection work well zero-shot (leveraging the learned prior); super-resolution needs ControlNet fine-tuning because multi-level inputs change the input distribution.
- **Fine-tuning from pre-trained vs from scratch (Tables VIII–IX)**: Fine-tuned MedDiff-FM substantially outperforms training from scratch on lesion generation Dice (e.g., MED-LN: 0.22 vs 0.01), especially with limited data, confirming transfer value.
- **Lesion inpainting reuse**: The lesion generation ControlNet generalises to inpainting via RePaint without additional fine-tuning.

## Reported Insights

- A single diffusion FM covering multiple anatomical regions can outperform region-specific models by sharing clinical priors.
- Multi-level (image + patch) processing is essential for 3D medical images where voxel dimensions are large but diffusion models have limited receptive fields.
- DiffPIR-based plug-and-play denoising achieves SSIM gains (+0.059) exceeding supervised methods (RED-CNN +0.051, CTformer +0.052) without any task-specific training on Mayo 2016.
- Anomaly detection with MedDiff-FM reaches 0.8525 image AUROC on BMAD liver, far above prior best (SimpleNet 0.7228), benefiting from the large pre-training data.
- Super-resolution performance is somewhat limited by the approximation of the real degradation operator in DiffPIR.
- Mediastinal lymph node generation is notably hard; only pre-trained + fine-tuned model succeeds (Dice 0.22 vs 0.01 from scratch).

## References Worth Chasing

- **MAISI** (Guo et al., WACV 2025) [32]: Competing 3D CT generation FM; produces high-res volumes across body regions.
- **Patch Diffusion** (Wang et al., NeurIPS 2024) [20]: Patch coordinate conditioning for efficient diffusion training; MedDiff-FM extends this to 3D.
- **DiffPIR** (Zhu et al., CVPR 2023) [39]: Plug-and-play diffusion-based image restoration; used here for denoising and SR.
- **ControlNet** (Zhang et al., ICCV 2023) [23]: Task-specific fine-tuning via locked/trainable copies + zero-conv.
- **DiffTumor** (Chen et al., CVPR 2024) [2]: Tumor synthesis on healthy organs; compared for lesion inpainting.
- **TotalSegmentator** (Wasserthal et al., 2023) [37]: Provides the 117-class anatomy masks used as conditions.
- **BMAD** [56]: Benchmark for medical anomaly detection, used for liver CT evaluation.

## Notes / Open Questions

- No total parameter count is reported; architecture is relatively lightweight (32 channels, 1 res block) but exact size is unknown.
- Training compute (GPU-hours, FLOPs) not disclosed; only hardware (RTX 3090) and epochs (~150) mentioned.
- Only CT modality explored; authors suggest extension to MRI/PET as future work.
- Patch-based sliding window inference is computationally expensive; authors mention consistency models as a potential acceleration.
- Evaluation relies heavily on proxy metrics (Dice via TotalSegmentator, segmentation-based lesion Dice); no reader study or clinical validation.
- The 5% held-out test set for synthesis partially overlaps in distribution with training; external validation on unseen institutions would strengthen claims.
- No comparison with latent diffusion approaches for 3D medical imaging.
