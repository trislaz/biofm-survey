---
id: differential-attention-augmented-biomedclip-2026
title: Differential Attention-Augmented BiomedCLIP with Asymmetric Focal Optimization
  for Imbalanced Multi-Label Video Capsule Endoscopy Classification
authors:
- Podakanti Satyajith Chary
- Nagarajan Ganapathy
year: 2026
venue: null
arxiv: '2603.17879'
doi: null
url: https://arxiv.org/abs/2603.17879v1
pdf_path: papers/differential-attention-augmented-biomedclip-2026.pdf
md_path: papers/md/differential-attention-augmented-biomedclip-2026.md
modalities:
- multimodal
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:17+00:00'
updated_at: '2026-04-22T20:19:08+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

This work presents a multi-label classification framework for video capsule endoscopy (VCE) that addresses the extreme class imbalance inherent in the Galar dataset through a combination of architectural and optimization-level strategies. Our approach modifies BiomedCLIP, a biomedical vision-language foundation model, by replacing its standard multi-head self-attention with a differential attention mechanism that computes the difference between two softmax attention maps to suppress attention noise. To counteract the skewed label distribution, where pathological findings constitute less than 0.1% of all annotated frames, a sqrt-frequency weighted sampler, asymmetric focal loss, mixup regularization, and per-class threshold optimization are employed. Temporal coherence is enforced through median-filter smoothing and gap merging prior to event-level JSON generation. On the held-out RARE-VISION test set comprising three NaviCam examinations (161,025 frames), the pipeline achieves an overall temporal mAP@0.5 of 0.2456 and mAP@0.95 of 0.2353, with total inference completed in approximately 8.6 minutes on a single GPU.
