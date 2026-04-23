---
id: interpretable-rna-foundation-model-2022
title: Interpretable RNA Foundation Model from Unannotated Data for Highly Accurate
  RNA Structure and Function Predictions
authors:
- Jiayang Chen
- Zhihang Hu
- Siqi Sun
- Qingxiong Tan
- Yixuan Wang
- Qinze Yu
- Licheng Zong
- Liang Hong
- Jin Xiao
- Tao Shen
- Irwin King
- Yu Li
year: 2022
venue: null
arxiv: '2204.00300'
doi: null
url: https://arxiv.org/abs/2204.00300v5
pdf_path: papers/interpretable-rna-foundation-model-2022.pdf
md_path: papers/md/interpretable-rna-foundation-model-2022.md
modalities:
- rna
status: extracted
evidence_quality: full-text
tags:
- foundation-model
- rna
- bert
- masked-language-modeling
- self-supervised
- secondary-structure
- 3d-structure
- rna-protein-interaction
- gene-expression
parameters: ~99M (12-layer BERT, 640 hidden, 20 heads; not explicitly stated, estimated
  from architecture)
training_tokens: 23.7M ncRNA sequences from RNAcentral
training_compute: 8×A100-80GB GPUs for 1 month
references_chased: false
added_at: '2026-04-22T21:55:27+00:00'
updated_at: '2026-04-22T21:55:33+00:00'
is_fm: true
fm_classification_reason: 'RNA-FM: pretrained RNA LM.'
---

## TL;DR

RNA-FM is a BERT-style masked language model pre-trained on 23.7 million non-coding RNA sequences from RNAcentral via self-supervised learning (15% token masking). It uses 12 transformer encoder blocks with 640 hidden dimensions and 20 attention heads. The learned L×640 embeddings capture structural, functional, and evolutionary information without any labels. Downstream, RNA-FM improves RNA secondary structure prediction (F1 +3.6 over UFold on ArchiveII600), 3D closeness prediction (33% Top-L precision improvement over RNAcontact), SARS-CoV-2 evolution modelling, protein-RNA interaction prediction, and 5′ UTR gene expression regulation.

## Model

- **Name**: RNA-FM
- **Architecture**: BERT-style bidirectional transformer encoder; 12 transformer blocks, 640 hidden size, 20 multi-head self-attention heads. Layer normalization and residual connections before/after every block
- **Vocabulary**: 16 nucleotide tokens (A, C, G, U, R, Y, K, M, S, W, B, D, H, V, N, −) + 4 functional identifiers (including [MASK])
- **Input**: Raw RNA nucleotide sequence (max length 1,024 during training)
- **Output**: L×640 embedding matrix per sequence. A Softmax head over the 20-token vocabulary during pre-training
- **Parameters**: Not explicitly stated. 12 layers × 640 hidden × 20 heads implies ~99M parameters (comparable to ESM-1b 12-layer variant)
- **Downstream modules**: Simple task-specific heads—ResNet32 (32 blocks, filter size 64) for 2D structure prediction tasks; U-Net for distance map prediction; CNN (PrismNet) for protein-RNA interaction; 1D CNN for MRL prediction. Two schemes: (1) feature-based (frozen RNA-FM) and (2) fine-tuning (joint training)

## Data

- **Pre-training**: 23.7M non-coding RNA sequences from RNAcentral (27M total, de-duplicated at 100% identity via CD-HIT-EST → "RNAcentral100"). Covers all ncRNA types across 47 databases. T→U replacement applied. Sequences capped at 1,024 tokens during training
- **Secondary structure benchmarks**: RNAStralign (37,149 structures, 8 types), ArchiveII (3,975 structures, 10 types), bpRNA-1m (13,419 sequences after 80% identity filtering, split TR0/VL0/TS0)
- **3D closeness / distance**: 221 training + 80 test RNA 3D structures from non-redundant PDB set (Leontis & Zirbel v3.99); length 32–1,000 nt, >80% redundancy removed
- **Protein-RNA interaction**: HeLa cell dataset from PrismNet, 17 RNA-binding proteins
- **Gene expression / MRL**: 83,919 synthetic human 5′ UTRs (75 lengths) with mean ribosome load labels, plus 7,600 real human 5′ UTRs

## Training Recipe

- **Pre-training objective**: Masked language modeling (MLM). 15% of tokens randomly selected; 80% replaced with [MASK], 10% random token, 10% unchanged. Cross-entropy loss on masked positions
- **Hardware**: 8× NVIDIA A100 GPUs (80 GB each), trained for 1 month
- **Optimizer / schedule**: Inverse square-root learning rate schedule; base LR 0.0001, weight decay 0.01, 10,000 warm-up steps
- **Max sequence length**: 1,024 tokens
- **Downstream fine-tuning**: Task-specific; e.g. ResNet32 for 2D structure tasks, transfer learning (initializing ResNet32 from secondary structure task for 3D closeness) significantly boosts small-dataset performance

## Key Ablations & Design Choices (quantitative)

1. **Pre-trained vs random embeddings**: UMAP visualizations show pre-trained RNA-FM produces clear clusters by RNA type (structure/function), while random initialization gives vague clusters and one-hot encoding shows no structure. Quantitatively, RNA-FM embeddings capture evolutionary trends via trajectory inference on lncRNA subsets
2. **RNA-FM vs UFold on secondary structure**: RNA-FM achieves F1=0.941 vs UFold F1=0.905 on ArchiveII600 (+3.6 points). On bpRNA TS0: F1=0.704 vs 0.654 (+5.0 points). RNA-FM matches or exceeds UFold on 85.5% of instances
3. **RNA-FM vs MSA features on 3D closeness**: Single ResNet32 with RNA-FM embeddings achieves Long-Range Top-L precision=0.53 vs RNAcontact ensemble of 100 models at 0.33 (+20 points). With transfer learning: 0.66 (+33 points). RNA-FM with transfer learning exceeds MSA covariance+PETfold on 77.5% of instances
4. **RNA-FM embedding vs secondary structure for distance prediction**: RNA-FM+Seq achieves MSE=0.0322 vs SS+Seq MSE=0.0387 (−17%); RNA-FM+Seq better on 94.2% of instances. Standalone RNA-FM (MSE=0.0353) already beats SS+Seq (MSE=0.0387)
5. **Protein-RNA interaction (feature-based)**: RNA-FM+Seq mean AUPRC=0.824 vs Seq-only 0.815 (+0.009); comparable to real in-vivo secondary structure features (RealSS+Seq: 0.833). RNA-FM+Seq outperforms RealSS+Seq on nearly half of the 17 RBPs
6. **Gene expression / MRL prediction**: RNA-FM embedding alone achieves R²=0.876 on Random7600 vs Seq R²=0.860. Combining all features (Seq+SS+3DS+RNA-FM): R²=0.882 (Random) and R²=0.824 (Human), best across all configurations
7. **Structure vs length encoding**: RNA-FM embeddings cluster by structure/function rather than sequence length—RNAs with different lengths but similar functions group together

## Reported Insights

- RNA-FM is the first self-supervised foundation model for non-coding RNA, demonstrating that a single pre-trained model can improve diverse downstream structural and functional tasks simultaneously
- Embeddings implicitly encode evolutionary information: trajectory inference on lncRNA embeddings recapitulates known species evolutionary timelines without any evolutionary features during training
- SARS-CoV-2 genome-level embeddings (via sliding window + averaging) correctly recapitulate the Alpha→Delta→Omicron evolutionary trajectory, suggesting regulatory elements carry viral evolution signals
- RNA-FM eliminates the need for time-consuming MSA generation while matching or exceeding MSA-based features on multiple tasks
- Structural improvements are larger than functional ones; authors hypothesize distribution mismatch between ncRNA pre-training data and functional task data (e.g., 5′ UTR is mRNA, not ncRNA)
- Transfer learning (initializing downstream module from a related task) is critical for small datasets—adds +20 points on 3D closeness Top-L precision

## References Worth Chasing (≤15 bio-FM refs)

1. **BERT** (ref [38], Devlin et al. 2018): Direct architectural basis for RNA-FM
2. **ESM-1b** (ref [66], Rives et al. 2021): Protein foundation model inspiring RNA-FM's approach; analogous self-supervised strategy on 250M protein sequences
3. **SPOT-RNA** (ref [28], Singh et al. 2019): Key baseline for secondary structure prediction using 2D deep neural networks + transfer learning
4. **UFold** (ref [32], Fu et al. 2021): SOTA secondary structure predictor incorporating prior pairing knowledge; main competitor
5. **RNAcontact** (ref [34], Sun et al. 2021): 3D closeness prediction via deep residual networks; main baseline for 3D contact tasks
6. **PrismNet** (ref [36], Sun et al. 2021): Protein-RNA interaction predictor using in-vivo RNA structures; downstream framework adopted
7. **AlphaFold** (ref [52], AlQuraishi 2019 / Jumper et al.): Protein structure prediction inspiring RNA 3D structure work
8. **trRosetta** (ref [51], Yang et al. 2020): Protein distance/orientation prediction; inspiration for RNA distance prediction task
9. **ARES** (ref [10], Townshend et al. 2021): Geometric deep learning for RNA structure scoring
10. **LinearFold** (ref [19], Huang et al. 2019): Efficient thermodynamic RNA folding baseline
11. **RNAcentral** (ref [67], 2021): Source database for pre-training data (27M→23.7M sequences)

## Notes / Open Questions

- Exact parameter count is never stated; 12-layer / 640-hidden / 20-head BERT-style architecture suggests ~99M parameters, but this is an estimate
- Max sequence length is 1,024 tokens during training; for longer sequences (e.g., SARS-CoV-2 genome at ~30K nt), a sliding-window + averaging strategy is used—this is ad hoc and likely loses long-range information
- Functional task improvements are notably smaller than structural ones; pre-training on ncRNA may not transfer as well to mRNA-related tasks (5′ UTR, coding regions)
- No ablation on model size (number of layers, hidden dims); unclear how much of the performance comes from architecture scale vs. pre-training data
- No comparison with protein-RNA co-training approaches or multi-modal models
- Published as arXiv preprint (2022); later extended into RhoFold+ (Nature Methods 2024) which builds RNA-FM into a full end-to-end 3D structure prediction pipeline
- Code and weights at https://github.com/ml4bio/RNA-FM; web server at https://proj.cse.cuhk.edu.hk/rnafm/

## Ablations (Rev 4)

The paper has no dedicated "ablation" section; ablations are conducted per-task by swapping the input feature(s) into the same downstream architecture. The studies below isolate the contribution of the RNA-FM embedding versus sequence one-hot, MSA-derived features, predicted/real secondary structure, and transfer learning.

| # | Task / dataset | Variant (input → downstream) | Metric | Δ vs. baseline | Source |
|---|---|---|---|---|---|
| A1 | Embedding quality (RNA Atlas, RNAcentral100) | Pre-trained RNA-FM vs. random-init RNA-FM vs. one-hot (UMAP) | Cluster separation by RNA type | Pre-trained → clear type clusters; random → vague; one-hot → no structure | Fig. 2a |
| A2 | 2D structure (ArchiveII600) | RNA-FM+ResNet32 vs. UFold | F1 | 0.941 vs. 0.905 (+0.036); wins on 85.5% of instances | Table 1 |
| A3 | 2D structure (bpRNA TS0) | RNA-FM+ResNet32 vs. UFold | F1 | 0.704 vs. 0.654 (+0.050) | Table 1 |
| A4 | 3D closeness (RNAcontact TE80, long-range Top-L) | (a) Seq+RNAcontact 100-ensemble; (b) RNA-FM+Seq+ResNet32; (c) (b)+transfer learning from 2D-structure task | Top-L precision | 0.33 → 0.53 (+20 pts) → 0.66 (+33 pts); transfer-learnt model wins on 77.5% of instances vs. MSA-cov+PETfold-SS | Table 2 |
| A5 | 3D distance (RNAcontact TE80, U-Net) | Seq / SS+Seq / SS+Cov+Seq / RNA-FM / RNA-FM+Seq / RNA-FM+Cov+Seq | MSE ↓ | 0.0615 / 0.0387 / 0.0338 / 0.0353 / 0.0322 / 0.0319; RNA-FM alone already beats SS+Seq; RNA-FM+Seq wins on 94.2% of instances | Table 3 |
| A6 | RBP-RNA interaction (HeLa, 17 RBPs, CNN) | Seq / RNA-FM+Seq / RealSS+Seq (in-vivo icSHAPE) | Mean AUPRC | 0.815 / 0.824 / 0.833; RNA-FM+Seq beats Seq on 16/17 RBPs and matches RealSS+Seq on ~½ | Table 4 |
| A7 | 5′ UTR MRL (Random7600) | Seq / Seq+SS / RNA-FM / 3DS / Seq+SS+RNA-FM / Seq+SS+3DS+RNA-FM | R² ↑ | 0.860 / 0.866 / 0.876 / 0.864 / 0.876 / 0.882 (best) | Table 5 |
| A8 | 5′ UTR MRL (Human7600, OOD) | same set as A7 | R² ↑ | 0.814 / 0.820 / 0.816 / 0.813 / 0.811 / 0.824 (best); RNA-FM alone underperforms Seq+SS, multi-feature combo recovers SOTA | Table 5 |
| A9 | SARS-CoV-2 evolution | Genome-level RNA-FM embeddings (sliding-window avg), no fine-tuning | Trajectory inference vs. FastME phylogeny | Recovers Alpha→Delta→Omicron 21K→21L without labels | Fig. 4d–e |
| A10 | RNA 3D reconstruction (PDB TS1, 3dRNA pipeline) | RNA-FM-predicted SS vs. UFold SS vs. ground-truth SS | RMSD (Å) ↓ | 7.91 vs. 25.70 vs. 13.96 (RNA-FM beats even ground-truth SS, indicating 3dRNA-stage error dominates) | Suppl. Table 5 / Fig. 3d |

### Take-aways

1. **Single-sequence RNA-FM embeddings replace MSA-derived features.** On 3D closeness (A4) and 3D distance (A5), RNA-FM alone matches or beats MSA covariance + secondary-structure stacks, eliminating the costly MSA search step — this is the strongest practical result and the main reason RNA-FM works as a "foundation" feature extractor.
2. **Gains are large on structural tasks, marginal on functional tasks.** +3–5 F1 on 2D, +20–33 pts Top-L on 3D closeness, but only +0.009 mean AUPRC on RBP binding (A6) and +0.01–0.02 R² on MRL (A7/A8); the Human7600 OOD set (A8) shows RNA-FM alone is *worse* than Seq+SS, hinting at distribution mismatch (ncRNA pre-training → mRNA 5′ UTR).
3. **Transfer learning is essential for small-data 3D tasks.** Initializing the ResNet32 from the 2D-structure task adds +13 Top-L precision points on top of RNA-FM features (A4: 0.53 → 0.66), more than the gain from adding RNA-FM itself.
4. **Pre-training matters, not just architecture.** Random-init RNA-FM produces no meaningful UMAP structure (A1); the gain is attributable to MLM pre-training on 23.7M ncRNA, not to BERT capacity alone.
5. **Combining RNA-FM with explicit structural features still helps on functional tasks.** Best MRL numbers (A7/A8) come from Seq+SS+3DS+RNA-FM, suggesting RNA-FM embeddings are complementary to — not a replacement for — explicit predicted structure on downstream functional readouts.
6. **Notable missing ablations.** No model-scale ablation (layers, hidden, heads), no tokenizer ablation, no pre-training-data-size ablation, no masking-rate sweep, no comparison to a protein-LM-style scaling curve. The whole-genome SARS-CoV-2 result (A9) relies on an ad-hoc sliding-window average that is itself never ablated.

**Top take-away:** RNA-FM's single-sequence embeddings replace expensive MSA-derived features on RNA 3D structural tasks (Top-L precision 0.33 → 0.66 on RNAcontact TE80, +33 pts over the 100-model RNAcontact ensemble) — but only when paired with transfer learning from the 2D-structure task; gains shrink to <2 R² points on functional 5′ UTR readouts where the ncRNA pre-training distribution no longer matches.

