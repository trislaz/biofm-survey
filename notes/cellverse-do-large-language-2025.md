---
id: cellverse-do-large-language-2025
title: 'CellVerse: Do Large Language Models Really Understand Cell Biology?'
authors:
- Fan Zhang
- Tianyu Liu
- Zhihong Zhu
- Hao Wu
- Haixin Wang
- Donghao Zhou
- Yefeng Zheng
- Kun Wang
- Xian Wu
- Pheng-Ann Heng
year: 2025
venue: null
arxiv: '2505.07865'
doi: null
url: https://arxiv.org/abs/2505.07865v1
pdf_path: papers/cellverse-do-large-language-2025.pdf
md_path: papers/md/cellverse-do-large-language-2025.md
modalities:
- scrna
- single-cell-multiomics
- epigenome
status: extracted
evidence_quality: medium
tags:
- benchmark
- single-cell
- LLM-evaluation
- cell-type-annotation
- drug-response-prediction
- perturbation-analysis
- multi-omics
- question-answering
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:14+00:00'
updated_at: '2026-04-22T20:17:52+00:00'
---

## TL;DR

CellVerse is a **benchmark** (not a model) that evaluates 14 LLMs (160M–671B) on language-centric single-cell biology QA tasks spanning four multi-omics types (scRNA-seq, CITE-seq, ASAP-seq, scATAC-seq) and three task levels (cell type annotation, drug response prediction, perturbation analysis). Key finding: specialist models (C2S-Pythia) fail entirely; generalist LLMs show preliminary but far-from-satisfactory understanding—e.g., best CTA accuracy is only 42 % on scRNA-seq, and drug response prediction does not significantly beat random guessing.

## Model

No new model is proposed. The paper benchmarks **14 existing LLMs**:
- **Specialist**: C2S-Pythia-160M, C2S-Pythia-410M, C2S-Pythia-1B (fine-tuned on cell2sentence data).
- **Generalist open-source**: Qwen-2.5 (7B/32B/72B), Llama-3.3-70B, DeepSeek-V3, DeepSeek-R1.
- **Generalist closed-source**: GPT-4, GPT-4o-mini, GPT-4o, GPT-4.1-mini, GPT-4.1.

Inference uses vLLM for open-source models and official APIs for closed-source models. All questions are converted to **multiple-choice** format because open-ended generation was unreliable.

## Data

**CellVerse benchmark dataset** — five sub-datasets from four single-cell multi-omics modalities:

| Dataset | Modality | Genes | Cell types / classes | Task(s) |
|---|---|---|---|---|
| MS brain (Schirmer 2019) | scRNA-seq | 3,000 | 18 cell types | CTA |
| PBMC (Mimitou 2021) | CITE-seq | 17,441 | 7 cell types | CTA |
| PBMC (Mimitou 2021) | ASAP-seq | 17,441 | 9 cell types | CTA |
| Cancer drug response (Aissa 2021) | scRNA-seq | 18,380 | 2 responses (sensitive/resistant) | DRP |
| K562 CRISPR (Adamson 2016) | scATAC-seq | 5,060 | binary (yes/no, up/down) | PSA, PDA |

Single-cell data is converted to natural language via **cell2sentence** (C2S; gene names ranked by expression) for cell/drug tasks, and via **gene regulatory networks** (GRN, Wilcoxon test p < 0.05, log₂FC > 0.5) for perturbation tasks.

## Training Recipe

Not applicable — this is a benchmark paper. No training is performed. All LLMs are evaluated in **zero-shot** and **few-shot** (in-context learning) settings without any fine-tuning on CellVerse.

## Key Ablations & Design Choices

1. **Multiple-choice vs. open-ended**: All tasks converted to closed-set multiple-choice because LLMs fail to produce reliable predictions in open-ended format.
2. **Context length scaling** (Fig 5): Including more gene names in cell sentences helps GPT-4 family but **not** DeepSeek family — DeepSeek already reasons well with short contexts, and extra low-expression genes may add noise.
3. **Few-shot in-context learning** (Fig 6, Obs 5): Few-shot examples do **not** consistently improve performance and can even degrade it. Hypothesis: noise in single-cell data makes noisy examples harmful → sample quality > sample quantity.
4. **Specialist vs. generalist** (Obs 1): C2S-Pythia models (trained specifically on single-cell tasks) fail completely (0 % accuracy on all leaderboards), exhibiting hallucination. Generalist LLMs with larger capacity perform much better despite zero task-specific training.
5. **Scaling law holds** (Obs 2): Performance positively correlates with model size. DeepSeek and GPT-4 families dominate leaderboards; top models always from one of these two families.
6. **Error taxonomy** (Fig 7): DeepSeek-R1 errors decompose into reasoning errors (~49 %), misclassification (~49 %), and factual errors (~2–10 %, more frequent in gene-level tasks).

## Reported Insights

- **Best CTA accuracies**: scRNA-seq 42.38 % (DeepSeek-R1), CITE-seq 61.43 % (GPT-4.1), ASAP-seq 29.33 % (GPT-4.1-mini) — substantial room for improvement.
- **Drug response prediction**: best 55 % (GPT-4.1-mini) — no significant improvement over random guessing (50 %).
- **Perturbation significance**: best 76.67 % (multiple models) — some models (Qwen) simply predict "No" for everything, exploiting class imbalance.
- **Perturbation direction**: best 62.96 % (DeepSeek-R1) — most models fail to beat random (50 %).
- GPT-4 frequently refuses to answer drug response and perturbation tasks (0 % accuracy).
- LLMs perform better on perturbation significance than direction, as expected.
- DeepSeek-R1 and GPT-4.1 produce explicit chain-of-thought reasoning trajectories that are interpretable.

## References Worth Chasing

- **Cell2Sentence** (Levine et al., 2024): core tokenization method converting cells to gene-name sentences.
- **C2S-Scale** (Rizvi et al., 2025): scaling C2S-Pythia to 1B parameters for single-cell analysis.
- **scGPT** (Cui et al., 2024): foundation model for single-cell multi-omics.
- **scBERT/GeneFormer** (mentioned in related work): alternative single-cell foundation models.
- **Galactica** (Taylor et al., 2022): LLM for science, relevant baseline for scientific QA.

## Notes / Open Questions

- This is purely a benchmark/evaluation paper — no new architecture or training recipe to extract.
- The C2S tokenization loses magnitude information (only ranks are kept) — is this a fundamental bottleneck?
- Drug response prediction at 55 % accuracy is essentially random — is the QA framing fundamentally inadequate for this task, or is it a data/prompt issue?
- The paper tests only English gene-name-based representations; alternative tokenization strategies (e.g., learned embeddings, numerical expression values) are not explored.
- Future work plans to scale CellVerse and build on it for next-generation single-cell analysis paradigm.
