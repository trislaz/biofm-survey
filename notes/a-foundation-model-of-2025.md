---
id: a-foundation-model-of-2025
title: A foundation model of transcription across human cell types
authors:
- Xi Fu
- Shentong Mo
- Alejandro Buendia
- Anouchka P. Laurent
- Anqi Shao
- Maria del Mar Alvarez-Torres
- Tianji Yu
- Jimin Tan
- Jiayu Su
- Romella Sagatelian
- Adolfo A. Ferrando
- Alberto Ciccia
- Yanyan Lan
- David M. Owens
- Teresa Palomero
- Eric P. Xing
- Raul Rabadan
year: 2025
venue: Nature
arxiv: null
doi: 10.1038/s41586-024-08391-z
url: https://www.nature.com/articles/s41586-024-08391-z
pdf_path: null
md_path: papers/md/a-foundation-model-of-2025.md
modalities:
- epigenome
status: extracted
evidence_quality: full-text
tags:
- transformer
- regulatory-genomics
- chromatin-accessibility
- gene-expression-prediction
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: Added in rev4 missing-FM brainstorm; canonical bio-FM.
---

## TL;DR

GET (General Expression Transformer) is a foundation model for cell-type-conditioned transcriptional regulation. It combines DNA sequence motif features with assay for transposase-accessible chromatin using sequencing (ATAC-seq) context to predict gene expression and regulatory activity across 213 human fetal and adult cell types, including held-out cell types and new assay platforms. The key design signal for this survey is that motif-masked self-supervised pretraining and cell-type/accessibility conditioning make the model much more transferable than fine-tuning from scratch: in the reported fetal astrocyte holdout, pretraining raises expression-prediction Pearson r from 0.60 to 0.94.

## Model

- **Name**: GET (General Expression Transformer).
- **Architecture**: Region-wise transformer over peak-by-motif regulatory tokens, with attention/Jacobian analyses used to infer enhancer-gene links and transcription factor interactions.
- **Input**: DNA sequence-derived motif information plus assay for transposase-accessible chromatin using sequencing (ATAC-seq) accessibility for a target cell type or condition.
- **Output**: Gene expression and regulatory activity scores; downstream analyses use model sensitivities to nominate cis-regulatory elements, enhancer-gene links, and transcription factor-transcription factor networks.
- **Adaptation**: Uses low-rank adaptation (LoRA) for efficient fine-tuning on new assays or disease datasets.
- **Parameters**: Not reported in the survey source note.

## Data

- **Training scope**: Human fetal and adult cell types, centred on chromatin accessibility atlases and DNA sequence motif features.
- **Scale**: 213 human cell types are reported for the main model setting.
- **Evaluation settings**: Leave-one-cell-type and leave-one-chromosome prediction, new adult cell types, glioblastoma (GBM) 10x Multiome transfer, lentiviral massively parallel reporter assay (lentiMPRA) regulatory activity, and CRISPR interference (CRISPRi) enhancer-gene benchmarks.

## Training Recipe

- **Pretraining objective**: Motif-masked self-supervised learning over regulatory regions.
- **Fine-tuning**: Supervised expression/accessibility adaptation, including binary ATAC-seq (BATAC), quantitative ATAC-seq (QATAC), and LoRA fine-tuning for new datasets.
- **Generalization protocol**: The paper stresses held-out cell types, held-out chromosomes, held-out motifs, and one-shot transfer to new assay/platform contexts rather than random-region-only validation.

## Key Ablations & Design Choices

| Design choice | Finding |
|---|---|
| Motif-masked pretraining | The full pretrained GET model substantially outperforms fine-tuning only on held-out fetal astrocytes (Pearson r 0.94 vs 0.60), making self-supervised pretraining the central transfer lever. |
| Region-wise transformer | GET outperforms multilayer perceptron (MLP), convolutional neural network (CNN), CatBoost, support vector machine (SVM), random forest, and linear-regression baselines under matched inputs. |
| Cell-type/accessibility conditioning | Conditioning on the target cellular context lets the model transfer to adult or disease cell types rather than acting as a sequence-only predictor. |
| Quantitative accessibility | Quantitative ATAC-seq fine-tuning improves over binary ATAC-seq fine-tuning for expression transfer. |
| One-shot adaptation | One glioblastoma sample is enough for LoRA adaptation to exceed 0.9 Pearson r on held-out patients, compared with 0.67 without fine-tuning. |

## Reported Insights

- **Pretraining is the main quality lever**: Motif-masked pretraining is not just a warm start; it changes cross-cell-type generalization.
- **Regulatory grammar is interpretable**: Attention/Jacobian analyses are used to derive enhancer-gene links and transcription factor interaction hypotheses, including distal regulatory regions.
- **Measured accessibility remains valuable**: Combining predicted expression with K562 chromatin accessibility improves lentiMPRA agreement over GET expression alone.
- **Cell-type transfer is practical**: The model is designed for new cell types and platforms via small amounts of adaptation data rather than complete retraining.

## Ablations (Rev 4)

Source: Nature DOI 10.1038/s41586-024-08391-z.

| Variable | Settings | Metric / dataset | Result | Conclusion |
|---|---|---|---|---|
| Pretraining stage | Full GET (pretrain + fine-tune) vs fine-tune only | Pearson r, expression on left-out fetal astrocytes | 0.94 vs 0.60 (Ext. Data Fig. 2d) | Self-supervised motif-masked pretraining is essential for cross-cell-type generalization |
| Model architecture | GET vs multilayer perceptron (MLP) / convolutional neural network (CNN) / CatBoost / support vector machine (SVM) / random forest / linear regression (same input, same epochs) | Expression prediction, leave-out astrocytes / leave-out chromosome 11 | GET best in both settings (Ext. Data Fig. 2e,f) | Region-wise transformer attention beats simpler machine learning baselines on the same features |
| Leave-out chromosome | Each of 22 autosomes held out independently | Pearson r, fetal astrocytes / GBM tumour / K562 OmniATAC | Mean r = 0.78 (0.73–0.84) / 0.75 (0.68–0.81) / 0.81 (0.72–0.84) | Performance is consistent across chromosomes; no single chromosome drives results |
| Leave-out motifs (input feature ablation) | Hold out 1, 2, 3, 4, 10, 20 random motifs from input and observation | Pearson/Spearman of accessibility counts per million on knockout peaks, K562 chromosome 14 | Robust up to 10 motifs; large degradation at 20 motifs | Model is not over-reliant on any small set of motifs; redundancy across motif clusters |
| assay for transposase-accessible chromatin using sequencing (ATAC-seq) quantization for fine-tuning | Binary ATAC-seq (BATAC)→BATAC vs BATAC→quantitative ATAC-seq (QATAC) vs QATAC→QATAC (LoRA, K562 cap analysis of gene expression (CAGE)) | K562 CAGE Pearson, leave-out chromosome 14 | QATAC fine-tuning improves over BATAC; QATAC-pretrained base further helps | Quantitative accessibility signal during fine-tuning improves transfer to new assays |
| Fetal-only vs fetal+adult pretraining atlas | Train on fetal-only (Domcke) vs fetal+adult (Zhang) peak set | Expression prediction and regulatory analysis | "Comparable" performance | Model is robust to the choice of peak/atlas source |
| Pretraining domain transfer | Fetal-only pretrain → predict adult cell types | R² across diverse adult cell types | 0.53 vs baseline 0.33 (corresponding fetal cell type) | Pretraining transfers across developmental stage, not just within-atlas |
| One-shot vs zero-shot fine-tuning on new dataset | Fine-tune on 1 GBM patient vs no fine-tuning | Pearson r on 16 held-out GBM patients | >0.9 vs 0.67 | Single-sample fine-tuning yields large gains on new platforms (10× multiome) |
| lentiMPRA scoring components | GET expression only vs GET expression × K562 ATAC-seq vs Enformer | Pearson r / regression slope on lentiMPRA log2(RNA/DNA), K562 | r = 0.45, slope 0.38 (GET only); r = 0.55, slope 0.63 (GET + ATAC-seq); Enformer r = 0.44, slope 0.14 | Combining GET prediction with measured accessibility outperforms heavily-supervised Enformer at zero-shot regulatory activity |
| Enhancer-gene scoring components | GET Jacobian alone vs Jacobian + chromatin accessibility × Powerlaw vs Jacobian × Powerlaw vs activity-by-contact (ABC) Powerlaw / Enformer / HyenaDNA / DeepSEA | Area under the precision-recall curve (AUPRC) on fetal erythroblast fetal hemoglobin (HbF) enhancers and K562 CRISPR interference (CRISPRi) (Fig. 3d, 1,000-bootstrap 95% confidence interval) | GET (Jacobian × Powerlaw) and GET (Jacobian + chromatin accessibility × Powerlaw) top performers, especially for distal (>100 kb) interactions | Combining attention-derived Jacobian with a learned distance prior gives best long-range enhancer-gene predictions |

**Design-choice take-aways:**
- Self-supervised motif-masked pretraining across many cell types is the single biggest design lever — removing it collapses leave-out performance from r=0.94 to 0.60.
- The peak × motif tokenization plus region-wise attention beats simpler machine learning baselines on identical inputs, validating the architecture (not just the data).
- The model is robust to atlas choice and to dropping individual motifs, but benefits from quantitative (vs binary) ATAC-seq during fine-tuning and from multiplying the attention-based Jacobian with a learned 1D-distance "Powerlaw" prior for distal enhancer-gene calls.
- Even single-sample LoRA fine-tuning suffices to adapt GET to new platforms/diseased cells (zero-shot 0.67 → one-shot >0.9 on GBM), making the FM practical for new datasets.

## References Worth Chasing

- Enformer — sequence-to-expression transformer baseline for regulatory genomics.
- Borzoi — long-context sequence-to-RNA coverage model that extends the Enformer lineage.
- Activity-by-contact models — enhancer-gene linking baseline combined with distance priors.
- Glioblastoma 10x Multiome datasets — stress test for one-shot disease/platform adaptation.

## Notes / Open Questions

- Parameter count, training compute, and token-equivalent scale are not stated in the survey source note.
- The strongest claims are in cell-type-conditioned regulatory-genomics settings; GET should not be treated as a general DNA language model for sequence-only tasks.
