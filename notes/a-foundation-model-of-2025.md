---
id: a-foundation-model-of-2025
title: A foundation model of transcription across human cell types
authors: []
year: 2025
venue: null
arxiv: null
doi: 10.1038/s41586-024-08391-z
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/a-foundation-model-of-2025.md
modalities:
- epigenome
status: fetched
evidence_quality: full-text
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: Added in rev4 missing-FM brainstorm; canonical bio-FM.
---

## Ablations (Rev 4)

| Variable | Settings | Metric / dataset | Result | Conclusion |
|---|---|---|---|---|
| Pretraining stage | Full GET (pretrain + fine-tune) vs fine-tune only | Pearson r, expression on left-out fetal astrocytes | 0.94 vs 0.60 (Ext. Data Fig. 2d) | Self-supervised motif-masked pretraining is essential for cross-cell-type generalization |
| Model architecture | GET vs MLP / CNN / CatBoost / SVM / Random Forest / Linear Regression (same input, same epochs) | Expression prediction, leave-out astrocytes & leave-out chr11 | GET best in both settings (Ext. Data Fig. 2e,f) | Region-wise transformer attention beats simpler ML on the same features |
| Leave-out chromosome | Each of 22 autosomes held out independently | Pearson r, fetal astrocytes / GBM tumour / K562 OmniATAC | Mean r = 0.78 (0.73–0.84) / 0.75 (0.68–0.81) / 0.81 (0.72–0.84) | Performance is consistent across chromosomes; no single chromosome drives results |
| Leave-out motifs (input feature ablation) | Hold out 1, 2, 3, 4, 10, 20 random motifs from input + observation | Pearson/Spearman of aCPM on knockout peaks, K562 chr14 | Robust up to 10 motifs; large degradation at 20 motifs | Model is not over-reliant on any small set of motifs; redundancy across motif clusters |
| ATAC quantization for fine-tuning | BATAC→BATAC vs BATAC→QATAC vs QATAC→QATAC (LoRA, K562 CAGE) | K562 CAGE Pearson, leave-out chr14 | QATAC fine-tuning improves over BATAC; QATAC-pretrained base further helps | Quantitative aCPM signal during fine-tuning improves transfer to new assays |
| Fetal-only vs fetal+adult pretraining atlas | Train on fetal-only (Domcke) vs fetal+adult (Zhang) peak set | Expression prediction & regulatory analysis | "Comparable" performance | Model is robust to the choice of peak/atlas source |
| Pretraining domain transfer | Fetal-only pretrain → predict adult cell types | R² across diverse adult cell types | 0.53 vs baseline 0.33 (corresponding fetal cell type) | Pretraining transfers across developmental stage, not just within-atlas |
| One-shot vs zero-shot fine-tuning on new dataset | Fine-tune on 1 GBM patient vs no fine-tuning | Pearson r on 16 held-out GBM patients | >0.9 vs 0.67 | Single-sample fine-tuning yields large gains on new platforms (10× multiome) |
| LentiMPRA scoring components | GET expression only vs GET expression × K562 ATAC vs Enformer | Pearson r / regression slope on lentiMPRA log2(RNA/DNA), K562 | r = 0.45, slope 0.38 (GET only); r = 0.55, slope 0.63 (GET + ATAC); Enformer r = 0.44, slope 0.14 | Combining GET prediction with measured accessibility outperforms heavily-supervised Enformer at zero-shot regulatory activity |
| Enhancer–gene scoring components | GET Jacobian alone vs Jacobian + DNase/ATAC × Powerlaw vs Jacobian × Powerlaw vs ABC Powerlaw / Enformer / HyenaDNA / DeepSEA | AUPRC on fetal erythroblast HbF enhancers and K562 CRISPRi (Fig. 3d, 1,000-bootstrap 95% CI) | GET (Jacobian × Powerlaw) and GET (Jacobian + DNase × Powerlaw) top performers, especially for distal (>100 kb) interactions | Combining attention-derived Jacobian with a learned distance prior gives best long-range enhancer–gene predictions |

**Design-choice take-aways:**
- Self-supervised motif-masked pretraining across many cell types is the single biggest design lever — removing it collapses leave-out performance from r=0.94 to 0.60.
- The peak × motif tokenization plus region-wise attention beats simpler ML baselines on identical inputs, validating the architecture (not just the data).
- The model is robust to atlas choice and to dropping individual motifs, but benefits from quantitative (vs binary) ATAC during fine-tuning and from multiplying the attention-based Jacobian with a learned 1D-distance "Powerlaw" prior for distal enhancer–gene calls.
- Even single-sample LoRA fine-tuning suffices to adapt GET to new platforms/diseased cells (zero-shot 0.67 → one-shot >0.9 on GBM), making the FM practical for new datasets.

