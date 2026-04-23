---
id: chemfm-as-a-scaling-2024
title: ChemFM as a Scaling Law Guided Foundation Model Pre-trained on Informative
  Chemicals
authors:
- Feiyang Cai
- Katelin Zacour
- Tianyu Zhu
- Tzuen-Rong Tzeng
- Yongping Duan
- Ling Liu
- Srikanth Pilla
- Gang Li
- Feng Luo
year: 2024
venue: null
arxiv: '2410.21422'
doi: null
url: https://arxiv.org/abs/2410.21422v3
pdf_path: null
md_path: null
modalities:
- small-molecule
status: seed
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:21+00:00'
updated_at: null
is_fm: true
fm_classification_reason: 'ChemFM: pretrained chemistry FM with scaling laws.'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Traditional AI methods often rely on task-specific model designs and training, which constrain both the scalability of model size and generalization across different tasks. Here, we introduce ChemFM, a large foundation model specifically developed for chemicals. By conducting a series of scaling experiments, we identify UniChem as the informative molecular database for pre-training the foundation model. ChemFM comprises 3 billion parameters and is pre-trained on 178 million molecules using self-supervised causal language modeling to extract generalizable molecular representations. This model can be adapted to diverse downstream chemical applications using either full-parameter or parameter-efficient fine-tuning methods. ChemFM consistently outperforms state-of-the-art task-specific AI models across all tested tasks. Notably, it achieves up to 67.48% performance improvement across 34 property prediction benchmarks, up to 33.80% reduction in mean average deviation between conditioned and actual properties of generated molecules in conditional molecular generation tasks, and up to 3.7% top-1 accuracy improvement across 4 reaction prediction datasets. Moreover, ChemFM demonstrates its superior performance in predicting antibiotic activity and cytotoxicity, highlighting its potential to advance the discovery of novel antibiotics. Furthermore, we demonstrate that, as a foundation model, ChemFM exhibits strong data efficiency, requiring significantly fewer labeled training samples to achieve state-of-the-art performance. We anticipate that ChemFM will significantly advance chemistry research by providing a foundation model capable of effectively generalizing across a broad range of tasks with minimal additional training.

## Ablations (Rev 4)

| # | Ablation | Setup | Variants compared | Key result | Source |
|---|----------|-------|-------------------|-----------|--------|
| 1 | Pre-training corpus (informativeness) | 1B model, identical config/steps, fine-tuned on 11 MoleculeNet datasets | UniChem (178M mols) vs ZINC20 (1.8B mols) | UniChem wins on 9/11 datasets, often by large margins (BACE ROC-AUC 0.857 vs 0.457; MUV PRC-AUC 0.122 vs 0.033; HIV 0.785 vs 0.721); ties on ClinTox/FreeSolv | §4.13, Table S2.6 |
| 2 | Effect of pre-training | ChemFM-3B fine-tuned on 22 ADMET tasks | Pre-trained weights vs random init (same FT recipe) | Pre-training improves nearly every task, e.g. Lipophilicity MAE 0.460 vs 0.779; Clearance_Hepatocyte Spearman 0.495 vs 0.208; CYP2D6 PRC-AUC 0.704 vs 0.576 | §4.12, Table S2.5 |
| 3 | Model-size scaling on UniChem | Pre-training validation loss across sizes | ~10M → 200M → 1B (ChemFM-1B) → 3B (ChemFM-3B) | Power-law fit holds up to ~200M; loss begins deviating below the extrapolated power law at 1B/3B → diminishing returns from further scale | §Results, Fig. S1.1a,b |
| 4 | Model-size scaling on ZINC20 | Same protocol on ZINC20 | 10M–200M+ params | Validation loss saturates beyond ~60M params → ZINC20 is information-limited | Fig. S1.1c |
| 5 | Model size on downstream | 1B vs 3B fine-tuned on MoleculeNet (11) and ADMET (22) | ChemFM-1B vs ChemFM-3B (both UniChem-pretrained) | 3B ≥ 1B on the large majority of tasks (e.g. PCBA PRC-AUC 0.346 vs 0.322; FreeSolv RMSE 0.830 vs 0.906) | Table S2.6, S2.5 |
| 6 | Fine-tuning strategy | Adaptation of ChemFM-3B to downstream tasks | Full-parameter FT vs LoRA (rank 4, 32-bit) | LoRA matches full FT while drastically cutting GPU memory, enabling 1B/3B FT on commodity hardware | §Results / §4 (LoRA) |
