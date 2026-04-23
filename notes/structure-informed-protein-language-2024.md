---
id: structure-informed-protein-language-2024
title: Structure-Informed Protein Language Model
authors:
- Zuobai Zhang
- Jiarui Lu
- Vijil Chenthamarakshan
- Aurélie Lozano
- Payel Das
- Jian Tang
year: 2024
venue: null
arxiv: '2402.05856'
doi: null
url: https://arxiv.org/abs/2402.05856v1
pdf_path: papers/structure-informed-protein-language-2024.pdf
md_path: papers/md/structure-informed-protein-language-2024.md
modalities:
- protein-sequence
status: extracted
evidence_quality: medium
tags:
- protein-language-model
- fine-tuning
- remote-homology
- knowledge-distillation
- ESM-2
parameters: 650M
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:52+00:00'
updated_at: '2026-04-22T20:26:29+00:00'
---

## TL;DR

Fine-tunes ESM-2 models (8M–650M) on a remote homology detection task (SCOPe fold classification) to inject structural knowledge into protein language models without requiring 3D structures at inference. Consistently improves EC and GO function annotation; gains on mutant fitness tasks depend on whether the targeted property is structure-related.

## Model

- **Architecture**: ESM-2 transformer (unchanged architecture) with an added MLP classification head for fold prediction during structure-informed training. Head is discarded at inference; the fine-tuned encoder is the deliverable.
- **Variants tested**: ESM-2-{8, 35, 150, 650}M; 3B and 15B excluded due to compute constraints.
- **Inference input**: protein sequence only (no structure needed).

## Data

- **Structure-informed training**: SCOPe 1.75 remote homology detection dataset (Hou et al., 2018). 12,312 genetically distinct domain sequences (<95% identity), 1,195 fold classes.
- **Downstream evaluation**:
  - Function annotation: EC number and GO (BP, MF, CC) prediction (Gligorijević et al., 2021), split at 95% sequence identity.
  - Localization: Subcellular and Binary localization (Almagro Armenteros et al., 2017).
  - Mutant fitness: β-lactamase, Fluorescence, Stability, AAV, GB1, Thermostability (from PEER and FLIP benchmarks).
  - Retrieval-based EC annotation: Swiss-Prot (227,363 sequences), NEW-392, Price-149 test sets.

## Training Recipe

- Fine-tune ESM-2 encoder + MLP head on SCOPe fold classification (cross-entropy loss).
- 50 epochs, Adam optimizer, batch size 8.
- Learning rates: 1e-5 for ESM-2 backbone, 1e-4 for classification head (preserves pre-trained representations).
- Downstream evaluation: freeze encoder, train 2-layer MLP predictor for 100 epochs per task.

## Key Ablations & Design Choices

- **Predictor-based evaluation**: Structure-informed models (suffix "-S") consistently improve EC (+4–11 pts Fmax) and GO-BP across all model sizes. GO-MF also improves. However, GO-CC, Subloc, and Binloc degrade — protein structure has little bearing on cellular location.
- **Mutant fitness tasks**: Mixed results. β-lactamase and GB1 sometimes improve, but Fluorescence and Stability can degrade. Whether structure-informed training helps depends on whether the property is structure-determined.
- **Retrieval-based evaluation**: Using ESM embeddings as similarity retrievers (top-5 cosine similarity, suffix "-R"/"-RS"), structure-informed models consistently improve across all function annotation tasks and model sizes — stronger and more uniform gains than predictor-based.
- **Practical EC annotation**: ESM-2-650M-R already surpasses CLEAN on NEW-392 (F1) without any supervised training on the dataset. ESM-2-650M-RS further improves and beats CLEAN on the harder Price-149 set.
- **Scaling**: Benefits are consistent across 8M → 650M, with no sign of saturation — larger models benefit proportionally.
- **UMAP visualisation**: After structure-informed training, embeddings show improved separability of SCOPe folds, confirming structural knowledge injection.

## Reported Insights

- Structure-aware training helps most when the downstream task is directly linked to protein structure (e.g., catalytic function, enzyme classification).
- For properties weakly related to structure (localization, some fitness landscapes driven by sequence-level epistasis), structure-informed training can hurt.
- Remote homology detection is a lightweight proxy for structural supervision — avoids the computational cost of structure prediction at training time and removes the need for structures at inference.
- Retrieval-based methods benefit more uniformly from structure-informed representations than predictor-based methods.

## References Worth Chasing

- Zhang et al. 2023a — systematic study of joint sequence-structure representation learning (same group, deeper exploration of the design space).
- Su et al. 2023 — SaProt: structure-aware vocabulary approach (alternative paradigm for injecting structure).
- Yu et al. 2023 — CLEAN: contrastive learning for enzyme annotation (competitive baseline).
- Hou et al. 2018 — DeepSF fold classification dataset used for training.

## Notes / Open Questions

- Only tested up to ESM-2-650M; unclear how much the 3B/15B models would benefit or whether diminishing returns set in.
- The remote homology task uses SCOPe folds as labels — gains may be bounded by SCOPe's coverage and classification granularity.
- No comparison with other structural distillation methods (e.g., contrastive learning on predicted structures or structure-aware vocabularies).
- Training is very lightweight (50 epochs on ~12K sequences); opens the question of whether more structural data or tasks would yield larger gains.
