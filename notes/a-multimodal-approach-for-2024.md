---
id: a-multimodal-approach-for-2024
title: A Multimodal Approach For Endoscopic VCE Image Classification Using BiomedCLIP-PubMedBERT
authors:
- Nagarajan Ganapathy
- Podakanti Satyajith Chary
- Teja Venkata Ramana Kumar Pithani
- Pavan Kavati
- Arun Kumar S
year: 2024
venue: null
arxiv: '2410.19944'
doi: null
url: https://arxiv.org/abs/2410.19944v3
pdf_path: papers/a-multimodal-approach-for-2024.pdf
md_path: papers/md/a-multimodal-approach-for-2024.md
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
updated_at: '2026-04-22T20:16:45+00:00'
is_fm: false
fm_classification_reason: Application of BiomedCLIP-PubMedBERT to VCE images; no new
  pretrained FM.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

This Paper presents an advanced approach for fine-tuning BiomedCLIP PubMedBERT, a multimodal model, to classify abnormalities in Video Capsule Endoscopy (VCE) frames, aiming to enhance diagnostic efficiency in gastrointestinal healthcare. By integrating the PubMedBERT language model with a Vision Transformer (ViT) to process endoscopic images, our method categorizes images into ten specific classes: angioectasia, bleeding, erosion, erythema, foreign body, lymphangiectasia, polyp, ulcer, worms, and normal. Our workflow incorporates image preprocessing and fine-tunes the BiomedCLIP model to generate high-quality embeddings for both visual and textual inputs, aligning them through similarity scoring for classification. Performance metrics, including classification, accuracy, recall, and F1 score, indicate the models strong ability to accurately identify abnormalities in endoscopic frames, showing promise for practical use in clinical diagnostics.
