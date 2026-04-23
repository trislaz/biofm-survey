---
id: xraygpt-chest-radiographs-summarization-2023
title: 'XrayGPT: Chest Radiographs Summarization using Medical Vision-Language Models'
authors:
- Omkar Thawakar
- Abdelrahman Shaker
- Sahal Shaji Mullappilly
- Hisham Cholakkal
- Rao Muhammad Anwer
- Salman Khan
- Jorma Laaksonen
- Fahad Shahbaz Khan
year: 2023
venue: null
arxiv: '2306.07971'
doi: null
url: https://arxiv.org/abs/2306.07971v2
pdf_path: papers/xraygpt-chest-radiographs-summarization-2023.pdf
md_path: papers/md/xraygpt-chest-radiographs-summarization-2023.md
modalities:
- imaging-pathology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T20:56:34+00:00'
updated_at: '2026-04-22T20:59:01+00:00'
is_fm: true
fm_classification_reason: 'XrayGPT: pretrained/aligned biomedical VL model for chest
  X-rays.'
---

## Abstract (from arxiv)

The latest breakthroughs in large vision-language models, such as Bard and GPT-4, have showcased extraordinary abilities in performing a wide range of tasks. Such models are trained on massive datasets comprising billions of public image-text pairs with diverse tasks. However, their performance on task-specific domains, such as radiology, is still under-investigated and potentially limited due to a lack of sophistication in understanding biomedical images. On the other hand, conversational medical models have exhibited remarkable success but have mainly focused on text-based analysis. In this paper, we introduce XrayGPT, a novel conversational medical vision-language model that can analyze and answer open-ended questions about chest radiographs. Specifically, we align both medical visual encoder (MedClip) with a fine-tuned large language model (Vicuna), using a simple linear transformation. This alignment enables our model to possess exceptional visual conversation abilities, grounded in a deep understanding of radiographs and medical domain knowledge. To enhance the performance of LLMs in the medical context, we generate ~217k interactive and high-quality summaries from free-text radiology reports. These summaries serve to enhance the performance of LLMs through the fine-tuning process. Our approach opens up new avenues the research for advancing the automated analysis of chest radiographs. Our open-source demos, models, and instruction sets are available at: https://github.com/mbzuai-oryx/XrayGPT.

## Ablations (Rev 4)

Progressive component addition over MiniGPT-4 baseline (Zhu et al., 2023), evaluated on MIMIC-CXR test set with ROUGE.

| Variant | R-1 | R-2 | R-L |
|---|---|---|---|
| Baseline (MiniGPT-4) | 0.1313 | 0.0221 | 0.0879 |
| + MedCLIP (swap visual encoder) | 0.1517 | 0.0308 | 0.0973 |
| + MedVicuna (LLM tuned on 100k medical dialogues) | 0.2099 | 0.0551 | 0.1284 |
| + RadVicuna (further tuned on 20k radiology dialogues) — full XrayGPT | 0.3213 | 0.0912 | 0.1997 |

Complementary GPT-judge eval: XrayGPT preferred 82% vs baseline 6%.

**Take-away:** Domain adaptation of the LLM dominates the gains — swapping CLIP→MedCLIP only adds ~2 R-1 points, while medical+radiology-specific Vicuna fine-tuning adds ~17 more, yielding the full +19 R-1 absolute improvement over MiniGPT-4.
