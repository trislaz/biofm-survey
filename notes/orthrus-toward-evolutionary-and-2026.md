---
id: orthrus-toward-evolutionary-and-2026
title: 'Orthrus: toward evolutionary and functional RNA foundation models'
authors: []
year: 2026
venue: null
arxiv: null
doi: 10.1038/s41592-026-03064-3
url: null
pdf_path: null
md_path: papers/md/orthrus-toward-evolutionary-and-2026.md
modalities:
- rna
status: extracted
evidence_quality: full-text
tags: ["contrastive-learning", "mamba", "ssm", "mature-rna", "orthology", "splicing-isoforms", "dcl-loss", "linear-probing", "few-shot", "zoonomia"]
parameters: "10.1M"
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: "Mamba-based RNA FM with contrastive self-supervised pretraining on mature mRNA."
---

## TL;DR

Orthrus is a Mamba-based mature RNA foundation model pretrained with a biologically motivated contrastive learning objective that maximizes embedding similarity between splice isoforms (10 species) and orthologous transcripts (400+ mammalian species from Zoonomia). With only 10.1M parameters, Orthrus outperforms or matches models 700× larger (e.g. Evo2 7B) on mRNA property prediction via simple linear probing, surpasses supervised Ab initio baselines on all evaluated tasks, and achieves strong few-shot performance (30 labeled examples → Pearson R 0.53 on human mRNA half-life, 71% of full supervised R=0.74). The key novelty is replacing reconstruction-based SSL (MLM/NTP) with a contrastive objective using evolution and splicing as biologically grounded augmentations.

## Model

- **Architecture**: Mamba (selective state space model), chosen for linear memory scaling O(n) with sequence length, variable motif spacing, and context filtering.
- **Variants**:
  - **Orthrus Small**: 1.3M parameters, Mamba encoder.
  - **Orthrus**: 10.1M parameters, Mamba encoder, contrastive-only.
  - **Orthrus MLM**: 10.1M parameters, Mamba encoder, joint contrastive + MLM objective.
- **Input representation**: 6-track mature RNA — 4 one-hot nucleotide tracks + splice-site indicator track + CDS codon-start indicator track.
- **Context length**: Handles mRNA sequences up to ~12,000+ nt (mature RNA lengths), enabled by Mamba's linear memory scaling.
- **Projection head**: MLP projector g_θ used during pretraining (discarded for downstream); Mamba encoder f_θ outputs used as embeddings.
- **Downstream**: Linear probe or full fine-tuning on top of frozen/unfrozen Mamba encoder embeddings.

## Data

- **Pretraining dataset**: 32M unique transcripts, 887M unique positive contrastive pairs.
- **Splicing augmentations**: Alternative splice isoforms from GENCODE and RefSeq across 10 metazoan organisms (human, mouse, chicken, C. elegans, chimpanzee, cow, dog, fruit fly, rat, zebrafish).
- **Orthology augmentations**: Orthologous transcripts from 400+ mammalian species in Zoonomia TOGA resource, mapped to human and mouse annotations via coding-sequence alignment + neighboring intronic/intergenic regions.
- **Naive orthology**: Transcripts pooled by consistent gene names across species.
- **UTR chimera transform**: Because Zoonomia orthologs lack UTRs, a UTR_combination_transform attaches UTRs from a splice isoform to the CDS of the ortholog to prevent the model from ignoring UTR importance.
- **Downstream evaluation datasets**: mRNA half-life (10,432 human + 11,008 mouse), MRL (12,459 isoforms from 7,815 genes), protein localization (10,409 genes, 12 subcellular locations), GO terms, eCLIP binding (168 RBPs, K562 + HepG2), mRNA subcellular localization (Ietswaart et al. and Fazal et al. APEX-seq).
- **Splitting**: Train/val/test split based on sequence homology to prevent data leakage.

## Training Recipe

- **Objective**: Decoupled Contrastive Learning (DCL) loss with temperature τ = 0.1. Optionally combined with MLM (15% random masking, cross-entropy over masked positions).
- **Joint loss**: L_total = (1 − α) · L_CL + α · L_MLM, with α = 0.95 (higher weight to MLM based on empirical loss-norm analysis).
- **Augmentation weighting**: Orthology augmentation weight w_i = 0.8; all others w_i = 1.0.
- **Masking augmentation**: 30% of input sequence masked as a data augmentation (distinct from MLM's 15%).
- **Positive pair sampling**: Per epoch, one positive sample y_j randomly drawn from the augmentation set (splice isoforms + orthologs) of each reference transcript x_j.
- **Tokenizer**: Character-level (one-hot nucleotide encoding, not BPE).
- **Hardware / wall-clock / optimizer / schedule / batch size / total steps**: Not explicitly reported in the available text. Larger batch sizes noted as beneficial for contrastive learning.

## Key Ablations & Design Choices (MOST IMPORTANT)

All ablations use Z-score normalization across 10 independent runs and 13 model configurations for cross-task comparability. Statistical significance assessed via one-sided Welch's t-test (p > 0.05 → not significantly different from top model).

- **Training objective (CL vs MLM vs CL+MLM)**:
  - CL alone: aggregate Z-score = 0.90
  - MLM alone (matched arch & data): aggregate Z-score = 0.71
  - CL + MLM (Orthrus MLM): further improves over CL alone → best overall.
  - MLM is on par with CL on 2 tasks but significantly declines on RNA-centric benchmarks (mRNA half-life, MRL).
  - Conclusion: CL captures mRNA-metabolism-relevant signals better; MLM adds complementary local nucleotide-level patterns.

- **Augmentation set**:
  - Splicing + Orthology + Masking (full): best performance.
  - Orthology included: Z-score = −0.11.
  - Masking only (no orthology): Z-score = −0.55.
  - Conclusion: Orthologous transcripts provide a substantial boost; evolutionary signal is key.

- **Architecture**:
  - Mamba 10.1M: aggregate Z-score = 0.90.
  - Mamba Small 1.3M: aggregate Z-score = 0.72.
  - Saluki-like (larger CNN-RNN): Z-score = −0.23.
  - Dilated CNN: Z-score = −0.53.
  - Conclusion: Mamba significantly outperforms parameter-matched baselines; scaling from 1.3M → 10.1M consistently helps.

- **Parameter scaling in other models**: For Nucleotide Transformer, increasing params does not consistently help, but switching from 1000-genomes to multi-species pretraining does → evolutionary information matters more than raw scale.

- **Few-shot fine-tuning**:
  - 30 training samples: Orthrus achieves Pearson R = 0.53 on human mRNA half-life (71% of supervised R = 0.74).
  - 100–300 samples: maintains competitive performance vs Ab initio trained on full data.
  - Ab initio methods are "ineffective" in low-data regime.

- **Linear probing vs supervised baselines**:
  - Orthrus linear probe matches or exceeds Ab initio supervised models (CNN-RNN Saluki or dilated CNN) on ALL evaluated tasks.
  - Human mRNA half-life: Orthrus MLM is the only self-supervised model to match supervised Pearson R = 0.71.

- **Orthrus vs Evo2**: Orthrus outperforms or matches Evo2 (7B params) on 7 tasks with 700× fewer parameters.

## Ablations (Rev 4)

| Variable | Settings | Metric/dataset | Result | Conclusion |
|---|---|---|---|---|
| Training objective | CL alone | Aggregate Z-score (8 tasks) | 0.90 | CL is the strongest single objective |
| Training objective | MLM alone (matched) | Aggregate Z-score | 0.71 | Inferior to CL, especially on mRNA HL and MRL |
| Training objective | CL + MLM | Aggregate Z-score | > 0.90 (best) | Complementary signals from both objectives |
| Augmentation | Spl + Orth + Msk (full) | Aggregate Z-score | Best | All augmentation sources contribute |
| Augmentation | With orthology | Aggregate Z-score | −0.11 | Orthology crucial for performance |
| Augmentation | Masking only | Aggregate Z-score | −0.55 | Masking alone is insufficient |
| Architecture | Mamba 10.1M | Aggregate Z-score | 0.90 | Best architecture |
| Architecture | Mamba 1.3M (Small) | Aggregate Z-score | 0.72 | Scaling helps within Mamba |
| Architecture | Saluki-like (CNN-RNN) | Aggregate Z-score | −0.23 | Mamba >> CNN-RNN |
| Architecture | Dilated CNN | Aggregate Z-score | −0.53 | Worst among tested |
| Model scale | Orthrus 10.1M vs Evo2 7B | 7 mRNA property tasks | Orthrus matches/outperforms | 700× fewer params, same or better perf |
| Data regime | 30 labeled samples | Human mRNA HL (Pearson R) | 0.53 (71% of supervised 0.74) | Excellent few-shot transfer |
| Linear probe | Orthrus MLM | Human mRNA HL (Pearson R) | 0.71 | Only SSL model matching supervised ceiling |

### Take-aways

- Contrastive learning with biologically meaningful augmentations (splicing + orthology) is far more effective than reconstruction-based SSL (MLM/NTP) for mature RNA representation, especially on mRNA-metabolism tasks.
- Evolutionary augmentations from 400+ mammalian species provide the single largest augmentation-side improvement.
- Mamba is the superior architecture for RNA sequences due to linear memory scaling, variable motif spacing, and context filtering — significantly outperforming matched CNN/CNN-RNN baselines.
- Joint CL + MLM captures complementary information (global functional similarity + local nucleotide patterns).
- The approach is extremely parameter-efficient: 10.1M parameters suffice to beat 7B-parameter models and supervised baselines.
- Diminishing returns from scale alone in reconstruction-based models (e.g. Nucleotide Transformer, HyenaDNA) — biological inductive bias is more important than raw parameter count.

## Reported Insights

- ~90% of the human genome lacks evidence of negative selection; reconstruction-based SSL wastes capacity reconstructing uninformative tokens. Contrastive learning sidesteps this by operating on functionally related sequence pairs.
- High mutual information across genomes of the same species limits effective dataset scaling for reconstruction methods; orthology-based augmentation is a better scaling strategy.
- Contrastive learning learns to disentangle shared functional information from sequence-specific "style" (aligned with theoretical work on contrastive representations).
- Orthrus similarity between isoforms directly correlates with shared protein domains (median Spearman ρ = 0.37, Pearson R = 0.45), significantly higher than baseline metrics (transcript length, sequence overlap).
- Despite training to cluster isoforms, Orthrus preserves transcript-specific functional information — it can predict fitness impact of exon skipping events and distinguish functionally divergent isoforms (BCL2L1 pro- vs anti-apoptotic; OAS1 p42 vs p46).
- UTR chimera transform is necessary to prevent the model from learning to ignore UTR regions (since Zoonomia orthologs lack UTRs).

## References Worth Chasing

- Evo2 [19] — 7B-parameter genomic FM; main scale-based competitor.
- Saluki [7] (Agarwal & Kelley 2022) — Supervised CNN-RNN for mRNA half-life; key benchmark model.
- HyenaDNA [14] — Long-range genomic FM using Hyena architecture; evaluated as baseline.
- Nucleotide Transformer [29] — Transformer-based genomic FM; ablated for multi-species vs single-species pretraining.
- Mamba [33] (Gu & Dao) — SSM architecture paper underlying Orthrus.
- Zoonomia Project / TOGA [32] — 400+ mammalian genomes resource providing orthology data.
- mRNA-Bench [70] — Benchmark suite for mRNA property prediction (eCLIP, localization tasks).
- GENCODE [38] / RefSeq [39] — Splice isoform annotation sources.
- Decoupled Contrastive Learning (DCL) [42] — Contrastive loss variant used in Orthrus.
- SimCLR / Barlow Twins [31] — Contrastive learning frameworks inspiring the approach.
- S4 [60] — Predecessor SSM architecture to Mamba.
- Chen et al. on contrastive disentangling [53] — Theoretical justification for why CL captures functional invariances.
- DNABERT / DNABERT-2 [12] — Genomic BERT-style FM; evaluated as baseline.
- Caduceus [16–18] — Other genomic FMs compared against.
- ENCODE / eCLIP [71, 72] — Source of RBP binding data used in evaluation.

## Notes / Open Questions

- **Training details missing**: Batch size, optimizer, learning rate schedule, total training steps/epochs, hardware, and wall-clock time are not reported in the main text (referenced as Appendix A.3 which is not available in the markdown).
- **Training tokens not reported**: Total tokens seen during pretraining is not stated; only 32M unique transcripts and 887M positive pairs are given.
- **No explicit test on non-mammalian generalization**: Pretrained on metazoan + mammalian data; unclear how well representations transfer to plants, fungi, prokaryotes.
- **Contrastive collapse risk**: The paper does not discuss whether the model suffers from representation collapse or how DCL specifically mitigates it beyond citing the original DCL paper.
- **α = 0.95 for MLM weighting**: This means MLM dominates the joint loss numerically — somewhat surprising given CL is framed as the key innovation. The justification is "empirical analysis of loss norms" without further detail.
- **Isoform clustering is qualitative**: BCL2L1 and OAS1 case studies are compelling but anecdotal; no systematic quantitative evaluation of isoform-level functional annotation accuracy.
- **Evaluation scope**: All downstream tasks are mRNA-centric; no evaluation on non-coding RNA tasks (lncRNA, miRNA function prediction).
- **Comparison fairness**: Orthrus uses a 6-track input (including splice site and CDS annotations) while most baselines use raw nucleotide sequence only — this auxiliary annotation may contribute to performance advantage.
