---
id: fedfms-exploring-federated-foundation-2024
title: 'FedFMS: Exploring Federated Foundation Models for Medical Image Segmentation'
authors:
- Yuxi Liu
- Guibo Luo
- Yuesheng Zhu
year: 2024
venue: null
arxiv: '2403.05408'
doi: null
url: https://arxiv.org/abs/2403.05408v2
pdf_path: papers/fedfms-exploring-federated-foundation-2024.pdf
md_path: papers/md/fedfms-exploring-federated-foundation-2024.md
modalities:
- imaging-radiology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:06+00:00'
updated_at: '2026-04-22T20:20:03+00:00'
is_fm: false
fm_classification_reason: Federated training methodology using SAM; no new pretrained
  FM.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Medical image segmentation is crucial for clinical diagnosis. The Segmentation Anything Model (SAM) serves as a powerful foundation model for visual segmentation and can be adapted for medical image segmentation. However, medical imaging data typically contain privacy-sensitive information, making it challenging to train foundation models with centralized storage and sharing. To date, there are few foundation models tailored for medical image deployment within the federated learning framework, and the segmentation performance, as well as the efficiency of communication and training, remain unexplored. In response to these issues, we developed Federated Foundation models for Medical image Segmentation (FedFMS), which includes the Federated SAM (FedSAM) and a communication and training-efficient Federated SAM with Medical SAM Adapter (FedMSA). Comprehensive experiments on diverse datasets are conducted to investigate the performance disparities between centralized training and federated learning across various configurations of FedFMS. The experiments revealed that FedFMS could achieve performance comparable to models trained via centralized training methods while maintaining privacy. Furthermore, FedMSA demonstrated the potential to enhance communication and training efficiency. Our model implementation codes are available at https://github.com/LIU-YUXI/FedFMS.
