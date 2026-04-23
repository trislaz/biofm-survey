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
