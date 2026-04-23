---
id: medmax-mixed-modal-instruction-2024
title: 'MedMax: Mixed-Modal Instruction Tuning for Training Biomedical Assistants'
authors:
- Hritik Bansal
- Daniel Israel
- Siyan Zhao
- Shufan Li
- Tung Nguyen
- Aditya Grover
year: 2024
venue: null
arxiv: '2412.12661'
doi: null
url: https://arxiv.org/abs/2412.12661v2
pdf_path: papers/medmax-mixed-modal-instruction-2024.pdf
md_path: papers/md/medmax-mixed-modal-instruction-2024.md
modalities:
- imaging-radiology
- imaging-pathology
- multimodal
status: extracted
evidence_quality: medium
tags:
- instruction-tuning
- mixed-modal
- lora
- dataset
- vqa
- image-generation
- biomedical-assistant
parameters: 7_000_000_000
training_tokens: 1_700_000_000
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:13+00:00'
updated_at: '2026-04-22T20:22:44+00:00'
---

## TL;DR

MedMax is a 1.47M-instance multimodal biomedical instruction-tuning dataset spanning VQA, interleaved image-text generation, captioning, image generation, visual chat, and report understanding across radiology and histopathology. Fine-tuning Anole-7B (Chameleon-7B variant) with LoRA on MedMax yields +26% over base Chameleon and +18.3% over GPT-4o averaged across 12 VQA benchmarks. Key contribution is the dataset itself and a novel MedMax-Instruct subset for interleaved text-image generation, plus a unified evaluation suite.

## Model

- **Base model**: Anole-7B, an instantiation of Chameleon-7B that unlocks mixed-modal (text+image) output by selectively fine-tuning output embeddings of image tokens on LAION images.
- **Architecture**: Autoregressive mixed-modal transformer; text encoded as BPE tokens, images encoded as 1024 discrete tokens via VQGAN encoder.
- **Fine-tuning**: LoRA (r=16, α=16, dropout=0.05) applied to {q, k, v, o, up, down, gate} projection matrices → 40M trainable parameters out of 7B total.
- **Total parameters**: 7B (base); 40M updated during instruction tuning.

## Data

- **MedMax dataset**: 1.47M instances, 725K unique images, 947K unique words, 1.7B multimodal discrete tokens.
- **Task breakdown**:
  - Visual chat: 686K instances (LLaVA-Med-IT 76K, PubMedVision-IT 504K, Quilt-Instruct 107K).
  - Image captioning + generation: 320K instances (160K each; sources: LLaVA-Med-PMC 37K, PMC-OA 83K, Quilt 100K, PubMedVision-Alignment 100K).
  - VQA: 284K instances (VQA-RAD, SLAKE, PathVQA, PMC-VQA, OmniMedVQA 81K train split).
  - Report understanding: 92K instances (MIMIC-CXR chest radiograph-report pairs; half for report generation, half for radiograph generation).
  - MedMax-Instruct (interleaved generation): 88K instances, generated via GPT-4o from filtered PMC-OA + Quilt image-caption pairs.
- **Domains**: Radiology, histopathology, pathology, diverse biomedical.
- **Knowledge bases**: PubMed Central papers, YouTube videos (Quilt), MIMIC-CXR clinical reports.
- **Quality filtering**: BioMedCLIPScore to remove statistical figures from PMC data; GPT-4o-mini to filter low-quality captions; removal of multi-image instances.

## Training Recipe

1. Start from Anole-7B (Chameleon-7B with image-generation unlocked).
2. LoRA fine-tuning on full MedMax (1.47M instances, 1.7B tokens).
3. 3 epochs, cosine LR schedule, peak LR=1e-4, warmup ratio=0.1, batch size=8.
4. Hardware: 8× Nvidia L40S GPUs (46 GB VRAM each).
5. Loss computed only on the response portion of each instruction-response pair.
6. MedMax-Instruct data generation cost: ~$500 for GPT-4o API calls.

## Key Ablations & Design Choices

- **Data scaling** (§6.1): VQA performance monotonically increases from 25% → 50% → 75% → 100% of MedMax data. Dataset is high-quality; more data = better.
- **Task ablation** (§6.2): Removing VQA data → −23% on VQA tasks; removing visual chat data → −17% on visual chat tasks. Task-specific data in the mixture is essential.
- **Finetuned VQGAN encoder** (§6.3): Fine-tuning VQGAN on 300K biomedical images (8 epochs) improved reconstruction loss (8.1→7.8) but **hurt** downstream VQA by ~3%. Cause: distribution shift in discrete visual tokens relative to what the base model was pretrained on. Original VQGAN tokens are better aligned with base model representations. This is a cautionary finding for domain-adapting visual tokenizers in discrete multimodal models.
- **Unified model vs. task-specific**: MedMax is competitive with task-specific LLaVA-Med fine-tuning on VQA-RAD, SLAKE, PathVQA — one model can replace multiple specialized ones.
- **Design choice**: Used LoRA instead of full fine-tuning, targeting all major projection matrices (40M params / 7B total).

## Reported Insights

- Mixed-modal models (native image+text generation) can be effectively adapted to biomedicine via instruction tuning despite large distribution shift from natural images.
- MedMax-7B achieves 65.5% avg across 12 VQA tasks vs. GPT-4o at 47.2% and base Chameleon at 39.4%.
- 99.5% accuracy on OmniMedVQA (in-distribution), showing near-ceiling when exposed to similar training data.
- Generated biomedical images have meaningful BioMedCLIPScore improvements (up to +100% on PMC-OA generation) but still produce textual artifacts in images.
- Interleaved text-image generation for biomedical reports is a novel capability not addressed by prior datasets.
- The model is a research prototype; authors caution against clinical deployment.

## References Worth Chasing

- **Chameleon** (Meta, 2024) — base mixed-modal model architecture.
- **Anole** (Chern et al., 2024) — the actual base model used (unlocks image generation from Chameleon).
- **PubMedVision** (Zhang et al.) — GPT-4V-denoised biomedical alignment data, large portion of MedMax.
- **Quilt-1M / Quilt-LLaVA** (Ikezogwo et al., 2024; Seyfioglu et al., 2024) — histopathology data from YouTube.
- **LLaVA-Med** (Li et al., 2024) — predecessor biomedical VL model and data source.
- **Transfusion** (Zhou et al., 2024) — alternative mixed-modal training objective (diffusion + autoregressive).

## Notes / Open Questions

- Training compute (FLOPs) not reported; only hardware described (8× L40S). Training duration not stated.
- Base model parameter count is 7B, but only 40M LoRA parameters are updated — unclear how much headroom full fine-tuning would give.
- The VQGAN ablation finding (domain-adapted tokenizer hurts performance) is surprising and underexplored — could be specific to LoRA or to the small scale of VQGAN fine-tuning.
- Multi-image reasoning explicitly left for future work due to Chameleon's limited context length (1024 tokens per image is expensive).
- Evaluation uses GPT-4o-mini as judge for open-ended VQA — introduces LLM-judge bias.
- $500 GPT-4o cost for MedMax-Instruct is notably cheap; scalability claim is credible.
