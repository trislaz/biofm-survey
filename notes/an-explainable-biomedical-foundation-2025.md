---
id: an-explainable-biomedical-foundation-2025
title: An Explainable Biomedical Foundation Model via Large-Scale Concept-Enhanced
  Vision-Language Pre-training
authors:
- Yuxiang Nie
- Sunan He
- Yequan Bie
- Yihui Wang
- Zhixuan Chen
- Shu Yang
- Zhiyuan Cai
- Hongmei Wang
- Xi Wang
- Luyang Luo
- Mingxiang Wu
- Xian Wu
- Ronald Cheong Kin Chan
- Yuk Ming Lau
- Yefeng Zheng
- Pranav Rajpurkar
- Hao Chen
year: 2025
venue: null
arxiv: '2501.15579'
doi: null
url: https://arxiv.org/abs/2501.15579v2
pdf_path: papers/an-explainable-biomedical-foundation-2025.pdf
md_path: papers/md/an-explainable-biomedical-foundation-2025.md
modalities:
- multimodal
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:13+00:00'
updated_at: '2026-04-22T20:17:05+00:00'
is_fm: true
fm_classification_reason: Concept-enhanced vision-language pretraining at scale; new
  biomedical FM.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

The clinical adoption of artificial intelligence (AI) in medical imaging requires models that are both diagnostically accurate and interpretable to clinicians. While current multimodal biomedical foundation models prioritize performance, their black-box nature hinders explaining the decision-making process in clinically meaningful concepts. Here, we present ConceptCLIP, the first explainable biomedical foundation model that achieves state-of-the-art diagnostic accuracy while delivering human-interpretable explanations across diverse imaging modalities. We curate MedConcept-23M, the largest pre-training dataset comprising 23 million image-text-concept triplets across diverse medical modalities, where clinical concepts are derived from the Unified Medical Language System. Leveraging this dataset, we develop ConceptCLIP through a novel dual-alignment approach that simultaneously learns global image-text representations and fine-grained region-concept associations for precise and interpretable medical image analysis. We curate the most extensive evaluation benchmark for multimodal biomedical foundation models, covering 52 clinical tasks spanning 10 imaging modalities. Extensive experiments demonstrate that ConceptCLIP outperforms existing state-of-the-art multimodal biomedical foundation models. Importantly, ConceptCLIP demonstrates superior diagnostic performance while providing human-understandable explanations validated by clinical experts. As the first precise and interpretable biomedical foundation model, ConceptCLIP represents a critical milestone toward the widespread clinical adoption of AI, thereby advancing trustworthy AI in medicine.

## Ablations (Rev 4)

Source: Extended Data Table A15 (zero-shot AUC %, 95% CI in parentheses); narrative summary in main text (p. 7) attributes overall gain to two components — RC-Align loss in pre-training (+3.76%, P<0.001) and top-K local region info at inference (+1.78%, P<0.001). Fig. 4(d) provides an additional ablation showing local alignment at inference improves concept-annotation over no-local-alignment baselines.

| Variant | SIIM-ACR | Covid-CXR2 | VinDr-Mammo | BrainTumorCT | Δ vs full (avg) |
|---|---|---|---|---|---|
| ConceptCLIP w/o RC-Align (no concept-enhanced pre-training loss) | 80.86 (77.87, 83.83) | 80.07 (78.16, 81.77) | 47.72 (43.73, 51.18) | 84.90 (82.42, 87.17) | −3.94 |
| ConceptCLIP w/o Local Info. (no top-K local region info at inference) | 81.24 (78.54, 84.04) | 79.67 (77.98, 81.51) | 50.75 (47.41, 54.19) | 90.43 (88.35, 92.28) | −1.78 |
| ConceptCLIP (full) | 83.05 (80.40, 85.63) | 81.77 (80.19, 83.35) | 51.78 (48.25, 55.05) | 92.60 (90.76, 94.20) | — |

Take-away: Both components matter, but the pre-training-side RC-Align loss is the dominant driver (~2× the inference-time local-info contribution); the largest single-dataset hit when removing RC-Align is on BrainTumorCT (−7.7 AUC), indicating concept-grounded pre-training is especially important for cross-modality transfer beyond CXR.
