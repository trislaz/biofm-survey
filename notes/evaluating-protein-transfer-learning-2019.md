---
id: evaluating-protein-transfer-learning-2019
title: Evaluating Protein Transfer Learning with TAPE
authors:
- Roshan Rao
- Nicholas Bhattacharya
- Neil Thomas
- Yan Duan
- Xi Chen
- John Canny
- Pieter Abbeel
- Yun S. Song
year: 2019
venue: null
arxiv: '1906.08230'
doi: null
url: https://arxiv.org/abs/1906.08230v1
pdf_path: papers/evaluating-protein-transfer-learning-2019.pdf
md_path: papers/md/evaluating-protein-transfer-learning-2019.md
modalities:
- protein-sequence
status: extracted
evidence_quality: full-text
tags:
- benchmark
- transfer-learning
- protein-representation
- self-supervised
- architecture-comparison
parameters: ~38M (each of Transformer, LSTM, ResNet matched to ~38M)
training_tokens: ~32M protein domain sequences (Pfam)
training_compute: 4× NVIDIA V100 GPUs for 1 week per model
references_chased: false
added_at: '2026-04-22T21:55:16+00:00'
updated_at: '2026-04-22T21:55:19+00:00'
is_fm: false
fm_classification_reason: 'TAPE: benchmark, not a model.'
---

## TL;DR

TAPE (Tasks Assessing Protein Embeddings) is a benchmark suite of five biologically relevant semi-supervised tasks for evaluating protein sequence representations. The paper compares three canonical architectures (Transformer, LSTM, ResNet; all ~38M parameters) plus two prior methods (Bepler supervised LSTM, UniRep mLSTM), all pretrained on Pfam (~31M domains). Self-supervised pretraining helps nearly all models on all tasks, sometimes more than doubling performance. However, alignment-based non-neural features still beat learned representations on structure prediction tasks. No single architecture wins across all tasks, motivating multi-task benchmarking. This is primarily a benchmark/comparison paper, not a single-model contribution.

## Model

Five pretrained architectures are compared:

| Architecture | Type | Key Hyperparams | Params | Pretraining Loss |
|---|---|---|---|---|
| Transformer | Attention-based | 12 layers, hidden 512, 8 heads | ~38M | Masked-token prediction |
| LSTM | Recurrent (ELMo-style) | Two 3-layer biLSTMs, 1024 hidden | ~38M | Next-token prediction (forward + reverse) |
| ResNet | Dilated convolutional | 35 residual blocks, 2 conv layers each, 256 filters, kernel 9, dilation 2 | ~38M | Masked-token prediction |
| Bepler LSTM | Recurrent | 2-layer biLM + 3×512 biLSTMs | Not stated (different) | Next-token prediction + supervised (contact + homology) |
| UniRep mLSTM | Multiplicative LSTM | 1900 hidden units, unidirectional | Not stated | Next-token prediction |

All three main models (Transformer, LSTM, ResNet) were deliberately matched to ~38M parameters for fair comparison.

Downstream supervised heads vary by task:
- **Sequence-to-sequence tasks** (SS, Contact): NetSurfP-2.0-style CNN+biLSTM (SS) or 2D residual CNN with 30 blocks (Contact).
- **Sequence classification** (Remote Homology, Fluorescence, Stability): Attention-weighted mean pooling → 512-unit dense layer → ReLU → linear output.

## Data

**Pretraining corpus:** Pfam (31M protein domains, 32.2M training sequences after splitting). Standard 25-character amino acid alphabet. Test split: ~95/5 random split for in-distribution, plus ~1% fully held-out families (6 clans + 6 families) for OOD evaluation.

**Downstream tasks (5):**

| Task | Category | Train | Test | Metric | Split Strategy |
|---|---|---|---|---|---|
| Secondary Structure | Structure | 8,678 | 513 (CB513) | Accuracy (Q3) | 25% seq-identity filter |
| Contact Prediction | Structure | 25,299 | 40 (CASP12) | Precision @ L/5 (med+long range) | 30% seq-identity filter (ProteinNet) |
| Remote Homology | Evolutionary | 12,312 | 718 (fold-level) | Classification accuracy | Held-out superfamilies |
| Fluorescence | Engineering | 21,446 | 27,217 | Spearman ρ | Hamming distance ≥4 from parent GFP |
| Stability | Engineering | 53,679 | 12,839 | Spearman ρ | 1-Hamming neighbors of top candidates |

## Training Recipe

**Self-supervised pretraining:**
- Hardware: 4× NVIDIA V100 GPUs (AWS)
- Duration: 1 week per model
- Optimizer: Adam, LR = 1e-3 with linear warm-up
- Dropout: 10%
- Variable batch sizes depending on protein length and model memory requirements
- Transformer & ResNet: masked-token prediction; LSTM: next-token prediction (bidirectional)

**Supervised fine-tuning:**
- Hardware: 2× NVIDIA Titan Xp (or Titan RTX for contact prediction)
- Convergence criterion: no improvement in validation accuracy for 10 epochs
- Optimizer: Adam, LR = 1e-4 with linear warm-up, 10% dropout
- Full backpropagation through pretrained encoder (no frozen layers)
- Memory-saving gradients (gradient checkpointing) used for contact prediction

## Key Ablations & Design Choices

### Self-supervised pretraining vs. no pretraining
Pretraining improves nearly all model–task combinations (Table 2). Highlights:
- **Transformer on Fluorescence:** 0.22 → 0.68 Spearman ρ (3× improvement)
- **Transformer on Stability:** −0.06 → 0.73 (from anti-correlated to strong)
- **LSTM on Remote Homology:** 0.12 → 0.26 (>2× on fold-level)
- **ResNet on Stability:** 0.61 → 0.73
- Exception: ResNet on Fluorescence sees minimal gain (0.21 pretrained vs. −0.28 no-pretrain, still poor)

### Architecture comparison across tasks
No single architecture dominates:
- **SS prediction:** LSTM and ResNet tie at 0.75 (pretrained); Transformer worst at 0.73
- **Contact prediction:** LSTM best at 0.39; Transformer 0.36; ResNet 0.29
- **Remote Homology:** LSTM best at 0.26; UniRep 0.23; Transformer 0.21; ResNet 0.17
- **Fluorescence:** Transformer 0.68, LSTM 0.67, UniRep 0.67; ResNet only 0.21
- **Stability:** Transformer 0.73, ResNet 0.73, UniRep 0.73; LSTM 0.69

Key insight: performance on a single task does not capture a model's full strengths — e.g., ResNet ties for best on SS but is worst on Fluorescence.

### Supervised pretraining (Bepler) vs. self-supervised
Bepler's supervised pretraining (on contact prediction + remote homology labels) matches or slightly beats self-supervised on contact prediction (0.40 vs. 0.39 LSTM) but underperforms self-supervised on remote homology (0.17 vs. 0.26) and fluorescence (0.33 vs. 0.67). The supervised pretraining data had to be filtered by sequence identity for fair comparison, reducing it by 75%, likely hurting this baseline.

### Learned features vs. alignment-based features
Alignment-based (HMM/PSSM) features substantially outperform all learned representations on:
- **SS:** 0.80 alignment vs. 0.75 best learned
- **Contact:** 0.64 alignment vs. 0.39 best learned (huge gap)
- **Remote Homology:** alignment (0.09) loses to learned (0.26) — learned features excel here

Alignment features not applicable to engineering tasks (Fluorescence, Stability) because all variants differ by single mutations, so alignments return identical features.

State-of-the-art methods with alignment inputs do even better: NetSurfP-2.0 = 85% SS accuracy, RaptorX = 0.69 contact precision, DeepSF = 41% homology accuracy — far above TAPE's best learned models.

### Language modeling perplexity vs. downstream performance
Lower LM perplexity does NOT reliably predict better downstream performance (replicating Rives et al. finding). The Transformer has the best perplexity on held-out families but is not uniformly the best downstream.

### In-distribution vs. OOD generalization (LM)
All models show a consistent drop from random-split to held-out-family evaluation (e.g., Transformer accuracy 0.45 → 0.30), confirming OOD challenge for unseen protein families.

## Reported Insights

1. **Self-supervised pretraining is broadly beneficial** for protein sequence models, improving nearly all architecture–task combinations, sometimes more than doubling performance.
2. **No single architecture dominates** across all five tasks — multi-task benchmarking is essential for evaluating protein representations.
3. **Alignment-based features still outperform learned features** on structure prediction tasks (SS, Contact), suggesting significant room for improvement in learned representations.
4. **Learned features outperform alignment on remote homology detection**, indicating self-supervised models capture evolutionary signals that alignment misses across large evolutionary distances.
5. **LM perplexity is not a reliable proxy** for downstream task performance.
6. **Bimodal distribution matters** (Fluorescence): models can distinguish bright vs. dark proteins but cannot rank within the dark mode.
7. **Pretraining helps long-range contacts** more than short-range, but alignment features still produce much sharper contact maps.
8. **The gap between learned and SOTA methods** (which combine alignment + architecture tricks) is large — e.g., 75% vs. 85% for SS, 0.39 vs. 0.69 for contacts.

## References Worth Chasing

1. **Rives et al. 2019** [31] — Scaling unsupervised learning to 250M protein sequences (ESM precursor); reports SS & contact transfer learning
2. **Bepler & Berger 2019** [11] — Supervised pretraining with structural information for protein embeddings
3. **Alley et al. 2019 (UniRep)** [12] — mLSTM-based protein representations for rational engineering
4. **Heinzinger et al. 2019 (SeqVec)** [30] — ELMo-style deep learning of protein sequences
5. **Riesselman et al. 2018 (DeepSequence)** [32] — VAEs on aligned families for mutation effect prediction
6. **Devlin et al. 2018 (BERT)** [6] — Masked-token prediction paradigm transferred to proteins
7. **Peters et al. 2018 (ELMo)** [5] — Contextualised word representations (inspiration for protein LSTMs)
8. **AlQuraishi 2019 (ProteinNet)** [27] — Standardised dataset for ML-based protein structure prediction
9. **Klausen et al. 2019 (NetSurfP-2.0)** [36] — SOTA SS prediction with alignment inputs + multi-task training
10. **Ma et al. 2015 (RaptorX)** [53] — SOTA contact prediction integrating evolutionary coupling + supervised learning
11. **Hou et al. 2017 (DeepSF)** [40] — Deep CNN for fold recognition (source of homology dataset)
12. **Sarkisyan et al. 2016** [43] — GFP fitness landscape via deep mutational scanning (fluorescence data source)
13. **Rocklin et al. 2017** [45] — Massively parallel protein stability design (stability data source)
14. **Yang et al. 2018** [33] — Learned protein embeddings for ML; related protein engineering approach

## Notes / Open Questions

- TAPE is a benchmark paper, not a single foundation model — its value is the standardised evaluation framework and the empirical comparison.
- The ~38M parameter budget is small by modern standards; scaling laws are not explored.
- Training compute (1 week on 4× V100) is modest; larger-scale pretraining (cf. ESM) may change conclusions.
- Alignment-based features are not applicable to protein engineering tasks, so the comparison is incomplete in that domain.
- Bepler supervised pretraining was handicapped by 75% data reduction due to sequence-identity filtering needed for fair evaluation.
- No exploration of pretraining data scale effects or curriculum — all models see the same Pfam corpus.
- The paper does not discuss model ensembling, multi-task pretraining losses, or structural pretraining objectives beyond Bepler's.
- The 25-character amino acid alphabet is standard but the paper does not explore BPE or other tokenisations.
- Code and data publicly available at https://github.com/songlab-cal/tape — useful for reproduction.
