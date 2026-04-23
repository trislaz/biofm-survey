---
id: biomedclip-a-multimodal-biomedical-2023
title: 'BiomedCLIP: a multimodal biomedical foundation model pretrained from fifteen
  million scientific image-text pairs'
authors:
- Sheng Zhang
- Yanbo Xu
- Naoto Usuyama
- Hanwen Xu
- Jaspreet Bagga
- Robert Tinn
- Sam Preston
- Rajesh Rao
- Mu Wei
- Naveen Valluri
- Cliff Wong
- Andrea Tupini
- Yu Wang
- Matt Mazzola
- Swadheen Shukla
- Lars Liden
- Jianfeng Gao
- Angela Crabtree
- Brian Piening
- Carlo Bifulco
- Matthew P. Lungren
- Tristan Naumann
- Sheng Wang
- Hoifung Poon
year: 2023
venue: null
arxiv: '2303.00915'
doi: null
url: https://arxiv.org/abs/2303.00915v3
pdf_path: papers/biomedclip-a-multimodal-biomedical-2023.pdf
md_path: papers/md/biomedclip-a-multimodal-biomedical-2023.md
modalities:
- vision
- language
- multimodal
status: extracted
evidence_quality: full-text
tags:
- contrastive-learning
- CLIP
- biomedical-vision-language
- domain-adaptation
- open-access
parameters: ~86M vision + ~110M text (ViT-B/16 + PubMedBERT)
training_tokens: 15M image-text pairs (PMC-15M), 32 epochs
training_compute: up to 16× NVIDIA A100 GPUs
references_chased: false
added_at: '2026-04-22T19:42:13+00:00'
updated_at: '2026-04-22T20:17:29+00:00'
is_fm: true
fm_classification_reason: 'BiomedCLIP: pretrained biomedical VL FM.'
---

## TL;DR

BiomedCLIP is a CLIP-style contrastive vision-language model pretrained on PMC-15M (15M biomedical image-caption pairs from 4.4M PubMed Central articles). It adapts CLIP to biomedicine by swapping the text encoder to PubMedBERT, extending context to 256 tokens, and using ViT-B/16 at 224px. It sets SOTA on cross-modal retrieval, zero-shot classification (PCam, LC25000, TCGA-TIL, RSNA), and medical VQA (VQA-RAD, SLAKE), even beating radiology-specific models like BioViL on RSNA with only 10% labeled data.

## Model

- **Architecture**: Dual-encoder CLIP (InfoNCE contrastive loss).
  - **Image encoder**: ViT-B/16 (86M params, 768-d hidden, patch size 16×16), initialized from ImageNet-pretrained weights. Input resolution 224×224.
  - **Text encoder**: PubMedBERT (domain-specific BERT pretrained on PubMed), replacing GPT-2. WordPiece tokenizer (30k vocab) instead of BPE (50k). Context length extended from 77 → 256 tokens.
- Learnable temperature τ in InfoNCE loss.
- Linear projection on top of each encoder to shared embedding space.
- Patch dropout used for training efficiency.
- Implementation based on OpenCLIP; gradient checkpointing + AMP (bfloat16); sharding contrastive loss across GPUs.

## Data

- **PMC-15M**: 15,282,336 image-caption pairs extracted from 4.4M PubMed Central Open Access articles (as of June 2022). Publicly available, no privacy issues.
  - Images span 30+ biomedical types: radiology (X-ray, CT, MRI, ultrasound), digital pathology, microscopy (light, electron), statistical figures, flowcharts, chemical structures, etc.
  - Median image size well above 224×224; median caption length well above 77 tokens — motivating architecture changes.
  - Processed via Azure Databricks / Apache Spark.
- **PMC-Fine-Grained-46M**: 46M image-text pairs created by splitting composite figures into sub-figures and incorporating in-line text references. Used only for distribution analysis in this paper.
- **Train / Val / Test split**: 13.9M train, 13.6k val, 725,739 test (for retrieval).
- Prior biomedical datasets are orders of magnitude smaller: MIMIC-CXR 377k, CheXpert 224k, ROCO 88k, ARCH 7.5k.

## Training Recipe

- **Optimizer**: AdamW (β₁=0.9, β₂=0.98, eps=1e-6, weight decay 0.2).
- **LR schedule**: Cosine decay, peak LR 5e-4, 2000 warmup steps.
- **Epochs**: 32 (final model); 8 epochs used for ablation sweeps.
- **Batch size**: 4096 (selected after ablation; 64k tried but gains didn't transfer downstream).
- **Hardware**: Up to 16× NVIDIA A100 or 16× V100 GPUs, PyTorch DDP.
- **Precision**: Automatic mixed precision (bfloat16 when supported).
- **Augmentation**: RandomResizedCrop; standard ImageNet normalization (mean/std).
- **Random seed**: 0.
- Validation: every epoch.

## Key Ablations & Design Choices

1. **Text encoder swap (GPT-2 → PubMedBERT, context 77)**:
   - Loss 0.6626 → 0.5776; img2txt R@1 64.53 → 69.03%; txt2img R@1 63.56 → 67.41% (Supp. Table 1, 8 epochs).

2. **Context length (77 → 256 tokens, with PubMedBERT)**:
   - Loss 0.5776 → 0.4807; img2txt R@1 69.03 → 73.50%; txt2img R@1 67.41 → 72.26% (Supp. Table 1, 8 epochs).

3. **Vision encoder scale (ViT-S → ViT-M → ViT-B, all /16)**:
   - ViT-S/16 (22M): img2txt R@1 69.45; ViT-M/16 (39M): 71.85; ViT-B/16 (86M): 73.50 (Supp. Table 2, 8 epochs). Larger = better.

4. **Vision encoder init (random vs. ImageNet-pretrained)**:
   - Random: loss 0.3814, img2txt R@1 83.15; ImageNet: loss 0.3819, img2txt R@1 82.90 (Supp. Table 3). Near-identical validation, but ImageNet init gives more stable downstream performance. Authors chose ImageNet init.

5. **Image resolution (224 vs. 384)**:
   - 384px: loss 0.3406, img2txt R@1 84.63 (vs. 82.90 at 224px), 1.92× training time (Supp. Table 4).
   - But **downstream zero-shot** degraded: mean accuracy 75.52 → 70.37 across 5 datasets; PCam 73.41 → 67.15 (Supp. Table 5). Upsampling low-res images (PCam 96×96) introduces noise. Authors chose 224px.

6. **Batch size (2k vs. 4k vs. 4k→64k)**:
   - 2k: img2txt R@1 79.69; 4k: 82.90 (Supp. Table 6).
   - 4k→64k schedule: img2txt R@1 83.98 → 87.32 (Supp. Table 7) on validation, but gain didn't transfer to downstream tasks. Authors chose constant 4k.

7. **Domain-specific pretraining is essential** (Supp. Table 8):
   - OpenAI CLIP ViT-B/16 (no biomed): img2txt R@1 11.82 on PMC val.
   - Continual-pretrained BiomedCLIP ViT-B/16-GPT/77 on PMC-15M: 81.57.
   - BiomedCLIP ViT-B/16-BERT/256: 82.90 — best overall.

8. **Downstream SOTA**:
   - Cross-modal retrieval: text-to-image R@1 59.60 vs. CLIP 1.00, PubMedCLIP 8.48; image-to-text R@1 60.00 vs. CLIP 0.79.
   - Zero-shot classification mean: BiomedCLIP best across PCam, LC25000-Lung, LC25000-Colon, TCGA-TIL, RSNA.
   - RSNA linear probe: BiomedCLIP at 10%-shot already beats BioViL at 100%-shot.
   - VQA-RAD overall: BiomedCLIP 72.10 vs. PubMedCLIP 69.20; comparable to Med-PaLM M (562B).

## Reported Insights

- Diverse biomedical pretraining data yields positive transfer even to narrow domains — BiomedCLIP beats radiology-specific BioViL on RSNA pneumonia detection despite having fewer radiology-specific pairs.
- PubMedCLIP (continual pretraining on only 80k radiology pairs) actually performs worse than general CLIP on biomedical retrieval, likely due to catastrophic forgetting on small data.
- Biomedical captions are much longer than web captions (90th percentile > 256 tokens); ignoring this (CLIP's 77-token limit) leaves significant signal on the table.
- PLIP (pathology-specific, pretrained on Twitter data) performs poorly on PCam — highlighting coverage gaps in social media sourced data.
- PMC-15M can serve as a privacy-preserving proxy for proprietary patient data: retrieve similar public images and query external models on those instead.
- Composite figures make up ~50% of PMC-15M; splitting them (PMC-Fine-Grained-46M) is identified as future work for finer-grained pretraining.

## References Worth Chasing

- **PubMedBERT** [24] (Gu et al., 2021) — domain-specific LM pretraining baseline and text encoder init.
- **OpenCLIP** [64] (Ilharco et al., 2021) — implementation backbone; reproducible scaling laws.
- **BioViL** [22] (Boecking et al., 2022) — radiology-specific CLIP competitor beaten here.
- **PLIP** [7] (Huang et al., 2023) — pathology VLP from Twitter data; complementary data source.
- **LLaVA-Med** [38] (Li et al., 2024) — uses BiomedCLIP as vision encoder; achieves highest VQA scores.
- **ConVIRT** [34] (Zhang et al., 2020) — pioneered contrastive medical image-text pretraining.
- **ELEVATER** [33] (Li et al., 2022) — evaluation toolkit used for downstream benchmarking.
- **Scaling CLIP via masking** [32] (Li et al., 2022) — patch dropout strategy adopted for efficiency.

## Notes / Open Questions

- Largest vision encoder explored is only ViT-B/16; ViT-L/H/G untested due to compute constraints. How much headroom remains?
- 224px resolution chosen despite 384px improving val metrics, because downstream zero-shot degraded. This suggests eval protocol and input distribution mismatch matter a lot — warrants deeper investigation.
- PMC-Fine-Grained-46M (sub-figure splitting + in-line references) was created but never used for pretraining — a clear next step.
- No comparison with BLIP/BLIP-2 generative VLP approaches; the paper focuses purely on contrastive dual-encoder models.
- Training compute not precisely reported (no GPU-hours or FLOPs); only "up to 16 A100s" mentioned.
- WordPiece (30k) vs. BPE (50k) confounded with PubMedBERT vs. GPT-2 swap — individual contribution of tokenizer change is not isolated.
- The paper uses OpenAI CLIP as continual-pretraining init for some variants but trains from ImageNet init for the best model — the comparison could be more systematic.

## Ablations (Rev 4)

Validation metrics on PMC-15M (img2txt / txt2img R@1, %); downstream zero-shot mean accuracy where noted. All ablations from the Supplementary Note (Tables S1–S8).

| # | Axis varied | Setting | Val loss ↓ | img2txt R@1 | txt2img R@1 | Downstream (mean) | Δ vs. prev row | Source |
|---|---|---|---|---|---|---|---|---|
| 1 | Text encoder + tokenizer + ctx | GPT-2 / BPE-50k / ctx 77 (CLIP default) | 0.6626 | 64.53 | 63.56 | — | baseline | S1 |
| 2 | Text encoder + tokenizer | PubMedBERT / WordPiece-30k / ctx 77 | 0.5776 | 69.03 | 67.41 | — | +4.50 / +3.85 | S1 |
| 3 | Context length | PubMedBERT / WordPiece-30k / ctx 256 | 0.4807 | 73.50 | 72.26 | — | +4.47 / +4.85 | S1 |
| 4 | Vision scale | ViT-S/16 (22M, dim 384) | 0.5342 | 69.45 | 68.02 | — | baseline | S2 |
| 5 | Vision scale | ViT-M/16 (39M, dim 512) | 0.5063 | 71.85 | 70.22 | — | +2.40 / +2.20 | S2 |
| 6 | Vision scale | ViT-B/16 (86M, dim 768) | 0.4807 | 73.50 | 72.26 | — | +1.65 / +2.04 | S2 |
| 7 | Vision init | ViT-B/16 random init | 0.3814 | 83.15 | 81.75 | — | baseline | S3 |
| 8 | Vision init | ViT-B/16 ImageNet-pretrained | 0.3819 | 82.90 | 81.86 | — | ≈0 (val) but more stable downstream | S3 |
| 9 | Image resolution | 224 px (1.00× train time) | 0.3819 | 82.90 | 81.86 | 75.52 | baseline | S4/S5 |
| 10 | Image resolution | 384 px (1.92× train time) | 0.3406 | 84.63 | 83.56 | 70.37 | +1.73 val / **−5.15 downstream** | S4/S5 |
| 11 | Batch size (8 ep) | 2k | — | 79.69 | 78.43 | — | baseline | S6 |
| 12 | Batch size (8 ep) | 4k | — | 82.90 | 81.86 | — | +3.21 / +3.43 | S6 |
| 13 | Batch schedule (40 ep) | constant 4k | — | 83.98 | 82.71 | — | baseline | S7 |
| 14 | Batch schedule (40 ep) | 4k → 64k (after 8 ep) | — | 87.32 | 86.66 | no downstream gain | +3.34 val only | S7 |
| 15 | End-to-end config | OpenAI CLIP RN50-224-GPT/77, WIT-400M only | — | 10.31 | 10.38 | — | baseline (no biomed pretraining) | S8 |
| 16 | End-to-end config | CLIP RN50 init → continual on PMC-15M | — | 81.17 | 80.17 | — | +70.86 / +69.79 | S8 |
| 17 | End-to-end config | CLIP ViT-B/16 init → continual on PMC-15M | — | 81.57 | 80.89 | — | +0.40 / +0.72 | S8 |
| 18 | End-to-end config (final) | ViT-B/16 (ImageNet) + PubMedBERT/256, PMC-15M | — | **82.90** | **81.86** | — | +1.33 / +0.97 | S8 |

### Take-aways

1. **Domain-specific text stack is the single largest controllable lever.** Swapping GPT-2/BPE/77-token for PubMedBERT/WordPiece/256-token lifts R@1 by ~9 points on each retrieval direction (rows 1→3) — bigger than any vision-side change tested.
2. **Context length matters as much as the encoder swap.** Going from 77 → 256 tokens alone gives +4.47 / +4.85 R@1 (rows 2→3); biomedical captions are long and truncation is costly.
3. **Validation gains do not always transfer downstream.** 384 px improves val by +1.7 R@1 but *drops* zero-shot mean by 5.15 pts (rows 9→10), driven mainly by PCam (96 px native). Pretraining-resolution / downstream-resolution mismatch dominates over raw resolution.
4. **Batch size has a clear plateau around 4k for PMC-15M.** Scaling 4k → 64k still improves validation (+3.3 R@1) but yields no downstream benefit (row 14), suggesting the 15M-pair dataset is the bottleneck — consistent with CLIP needing 400M pairs for 64k batches.
5. **Vision scaling helps monotonically up to ViT-B/16** (+4.05 / +4.24 R@1 from S→B, rows 4→6), but the largest tested model is still only ViT-B; head-room for L/H/G is unexplored.
6. **ImageNet vs. random init is a wash on validation but improves downstream stability** (rows 7–8) — the authors keep ImageNet init for that practical reason, not for a metric gain.
7. **Continual pretraining from OpenAI CLIP ≈ training from ImageNet+PubMedBERT init** for the final R@1 (rows 17 vs. 18: 81.57/80.89 vs. 82.90/81.86), so the biomedical text encoder contributes the remaining ~1 point edge in the chosen recipe.
