---
id: doctor-sun-a-bilingual-2025
title: 'Doctor Sun: A Bilingual Multimodal Large Language Model for Biomedical AI'
authors:
- Dong Xue
- Ziyao Shao
- Zhaoyang Duan
- Fangzhou Liu
- Bing Li
- Zhongheng Zhang
year: 2025
venue: null
arxiv: '2508.08270'
doi: null
url: https://arxiv.org/abs/2508.08270v2
pdf_path: papers/doctor-sun-a-bilingual-2025.pdf
md_path: papers/md/doctor-sun-a-bilingual-2025.md
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
updated_at: '2026-04-22T20:19:12+00:00'
is_fm: true
fm_classification_reason: 'Doctor Sun: pretrained/aligned bilingual biomedical multimodal
  LLM.'
---

## TL;DR

_(seed — not yet extracted)_

## Ablations (Rev 4)

| # | Ablation | Setup | Key result | Take-away |
|---|---|---|---|---|
| 1 | Feature-alignment data mix E1 (domain-only, 1:0) vs E2 (1:1 domain:general) | Hold instruction-tuning constant; eval on VQA-RAD, Path-VQA, MMBench | E2 variants average ~+123% on MMBench vs E1 (e.g. E1-V4 MMBench 31.4 → E2-V4 52.6) with domain perf preserved | Mixing general data in alignment prevents catastrophic forgetting at negligible domain cost |
| 2 | Instruction-tuning ratio V1 (1:0) → V2 (1:0.2) → V3 (1:0.5) → V4 (1:1) | 4 ratios × 2 alignment settings = 8 variants | V3 (1:0.5) wins 11/20 medical VQA metrics; V4 best on general MMBench (52.6) | 1:0.5 is the sweet spot for medical VQA; more general data only helps generic benchmarks |
| 3 | Domain-only feature alignment (E1) | Compare E1 vs E2 on F1/BLEU-1 | E1 yields +2.3% domain F1/BLEU but collapses on MMBench (~1.9–31.4) | Pure-domain alignment causes catastrophic forgetting of general perception/reasoning |
| 4 | Domain-only instruction tuning (V1) | V1 vs V2–V4 | V1 has highest BLEU-1/F1 but lowest recall and MMBench | Specialised answers, but recall drop is unsafe for clinical missed-diagnosis risk |
| 5 | Final Doctor Sun config (E2 align + V3 IT, "Doc-S") vs LLaVA-Med, RadFM | Zero-shot, 3 VQA benchmarks | Doc-S best overall: VQA-RAD F1 0.501 vs RadFM 0.442/LLa-M 0.069; Path-VQA F1 0.310; MMBench 53.6 | Chosen mixing ratios beat both medical baselines without task-specific finetuning |
| 6 | Two-stage hybrid training (LLM backbone): stage1 vs stage2 | BBH, C-Eval, MBPP, CMB | Stage2 lifts BBH 0.401 → 0.559 (+39%), CMB 0.371 → 0.415; C-Eval/MBPP roughly flat | Second stage primarily boosts reasoning; knowledge accumulates rather than superimposes |
| 7 | Medical LLM backbone vs peer medical LLMs | CMB benchmark | Doctor Sun 0.415 > DISC-MedLLM 0.398 > Mixtral-8x7B 0.363 > HuatuoGPT 0.320 > Bentsao 0.204 | Two-stage hybrid training yields SOTA Chinese medical knowledge among comparable medical LLMs |

**Count:** 7 ablation conditions reported (8 data-mix variants in Table 4 collapsed into axis-wise ablations 1–2, plus stage and baseline comparisons).

**Top take-away:** Mixing general with domain data is essential at *both* training stages — 1:1 in feature alignment and 1:0.5 in instruction tuning jointly avoid catastrophic forgetting (>100% MMBench gain) while preserving domain F1/BLEU; pure-domain training tanks general perception and recall, the latter being clinically unsafe.

## Abstract (from arxiv)

Large multimodal models (LMMs) have demonstrated significant potential in providing innovative solutions for various biomedical tasks, including pathology analysis, radiology report generation, and biomedical assistance. However, the existing multimodal biomedical AI is typically based on foundation LLMs, thus hindering the understanding of intricate medical concepts with limited medical training data. Moreover, recent LLaVA-induced medical LMMs struggle to effectively capture the intricate relationship between the texts and the images. Therefore, we introduce Doctor Sun, a large multimodal generative model specialized in medicine, developed to encode, integrate, and interpret diverse biomedical data modalities such as text and images. In particular, Doctor Sun integrates a pre-trained vision encoder with a medical LLM and conducts two-stage training on various medical datasets, focusing on feature alignment and instruction tuning. Moreover, we release SunMed-VL, a wide-range bilingual medical multimodal dataset, along with all associated models, code, and resources, to freely support the advancement of biomedical multimodal research.
