---
id: llava-med-training-a-2023
title: 'LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine
  in One Day'
authors:
- Chunyuan Li
- Cliff Wong
- Sheng Zhang
- Naoto Usuyama
- Haotian Liu
- Jianwei Yang
- Tristan Naumann
- Hoifung Poon
- Jianfeng Gao
year: 2023
venue: null
arxiv: '2306.00890'
doi: null
url: https://arxiv.org/abs/2306.00890v1
pdf_path: papers/llava-med-training-a-2023.pdf
md_path: papers/md/llava-med-training-a-2023.md
modalities:
- multimodal
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T20:59:06+00:00'
updated_at: '2026-04-22T21:03:38+00:00'
is_fm: true
fm_classification_reason: 'LLaVA-Med: pretrained/aligned biomedical multimodal LM.'
---

## Abstract (from arxiv)

Conversational generative AI has demonstrated remarkable promise for empowering biomedical practitioners, but current investigations focus on unimodal text. Multimodal conversational AI has seen rapid progress by leveraging billions of image-text pairs from the public web, but such general-domain vision-language models still lack sophistication in understanding and conversing about biomedical images. In this paper, we propose a cost-efficient approach for training a vision-language conversational assistant that can answer open-ended research questions of biomedical images. The key idea is to leverage a large-scale, broad-coverage biomedical figure-caption dataset extracted from PubMed Central, use GPT-4 to self-instruct open-ended instruction-following data from the captions, and then fine-tune a large general-domain vision-language model using a novel curriculum learning method. Specifically, the model first learns to align biomedical vocabulary using the figure-caption pairs as is, then learns to master open-ended conversational semantics using GPT-4 generated instruction-following data, broadly mimicking how a layperson gradually acquires biomedical knowledge. This enables us to train a Large Language and Vision Assistant for BioMedicine (LLaVA-Med) in less than 15 hours (with eight A100s). LLaVA-Med exhibits excellent multimodal conversational capability and can follow open-ended instruction to assist with inquiries about a biomedical image. On three standard biomedical visual question answering datasets, LLaVA-Med outperforms previous supervised state-of-the-art on certain metrics. To facilitate biomedical multimodal research, we will release our instruction-following data and the LLaVA-Med model.

## Ablations (Rev 4)

| # | Axis | Variants compared | Setting / metric | Result | Take-away |
|---|------|-------------------|------------------|--------|-----------|
| 1 | Domain adaptation | LLaVA vs LLaVA-Med (60K-IM) | Multimodal chat, GPT-4 relative score (Overall) | 38.4 → 52.7 | Biomedical curriculum tuning yields large gains over general-domain LLaVA, especially zero-shot. |
| 2 | Curriculum stage | Stage 1 only vs Stage 1+2 (60K-IM) | Chat Overall score | 24.8 → 52.7 | Stage 1 (caption alignment) alone collapses instruction-following; Stage 2 instruction-tuning is essential. |
| 3 | Instruction-data scale | 10K vs 60K vs 60K-IM | Chat Overall score | 43.5 / 49.8 / 52.7 | Performance improves monotonically with more self-instruct data. |
| 4 | Inline-mention (IM) context in self-instruct | 60K (no IM) vs 60K-IM | Chat Overall + averaged zero-shot/fine-tuned VQA | 60K-IM best on average | Using PubMed inline mentions as external knowledge during GPT-4 self-instruct improves data quality. |
| 5 | Vision encoder init | General CLIP vs BioMed CLIP | Fine-tuned VQA accuracy (VQA-RAD / SLAKE / PathVQA) | 61.5/84.2/83.1 → 64.8/83.1/87.1 | BioMed CLIP encoder gives a small but consistent boost over general-domain CLIP. |
| 6 | LM initialization | From LLaVA vs from Vicuna | Fine-tuned VQA accuracy | 61.5/84.2/83.1 vs 64.4/82.0/84.7 | Init choice has only minor effect; both work. |
| 7 | LM size | 7B vs 13B | Zero-shot + fine-tuned VQA | 13B > 7B overall | Scaling LM improves both zero-shot and fine-tuned performance (cost/quality trade-off). |
| 8 | Downstream fine-tune length | 3 vs 9 epochs (after 3-epoch Stage 2) | Fine-tuned VQA | 9 epochs > 3 epochs | Longer downstream fine-tuning helps, especially with shorter Stage-2 checkpoints. |

**Top take-away (8 ablations):** the two-stage curriculum is the dominant lever — Stage-2 instruction tuning on GPT-4-generated, inline-mention-grounded biomedical data (60K-IM) drives the chat score from 24.8 (Stage 1 only) to 52.7, dwarfing the gains from encoder choice, LM init, or model scaling.
