---
id: proteinbert-a-universal-deep
title: 'ProteinBERT: a universal deep-learning model of protein sequence and function'
authors: []
year: 2022
venue: Bioinformatics
arxiv: null
doi: 10.1093/bioinformatics/btac020
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/proteinbert-a-universal-deep.md
modalities:
- protein-sequence
status: extracted
evidence_quality: full-text
tags:
- local-global-architecture
- GO-term-prediction
- protein-function-prediction
- denoising-autoencoder
- convolutional
- global-attention
- efficient
- transfer-learning
parameters: 16M
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'ProteinBERT: pretrained protein LM.'
---

## TL;DR

ProteinBERT is a compact (~16M params) protein language model with a novel dual local/global architecture, pretrained on ~106M UniRef90 sequences with a joint task: masked language modeling + Gene Ontology (GO) annotation prediction. It replaces self-attention with linear-complexity global attention and uses dilated convolutions for local context, enabling intact processing of very long sequences. Achieves near-SOTA on TAPE benchmarks despite being ~2–200× smaller than competitors (TAPE Transformer 38M, ProtT5-XL 3B). Pretrained on a single GPU in 28 days; fine-tuning takes ~14 min per task.

## Model

- **Architecture**: Denoising autoencoder with two parallel representation paths—local and global.
- **Local path**: 3D tensor (B × L × 128). Each transformer-like block applies narrow 1D convolution (kernel 9, no dilation) + wide 1D convolution (kernel 9, dilation 5) + position-wise FC layer. Receptive field after 6 blocks: 241 tokens.
- **Global path**: 2D tensor (B × 512). Two FC layers per block with layer normalisation.
- **Inter-path communication**: (1) *Global attention* (local → global): single query from global rep attends to all local positions; 4 heads per block, d_key = 64, d_value = 128; linear complexity. (2) *Broadcast FC* (global → local): global vector projected to d_local and replicated across L positions.
- **Depth**: 6 transformer-like blocks; 24 global attention heads total.
- **No positional embeddings**; position information from convolutions + START/END tokens. Avoids length-generalisation failures of learned positional embeddings.
- **No dropout or regularisation** in the pretrained model (dropout added only in the fine-tuning output layer).
- **Activations**: GELU throughout.
- **Input encoding**: 26 amino-acid tokens + 8943-dim binary GO annotation vector.
- **Output**: per-position token probabilities (26-way softmax) + per-annotation probabilities (8943-way sigmoid).
- **Parameters**: ~16M (cf. TAPE Transformer ~38M, ESM-1b ~650M, ProtT5-XL 3B).
- **Sequence-length agnostic**: same weights handle any sequence length; trained at 128, 512, 1024 and tested up to 16 384.

## Data

- **Pretraining corpus**: ~106M proteins from UniProtKB/UniRef90 (non-redundant clusters at ≥90% sequence identity), covering the entire tree of life.
- **GO annotations**: 8943 most frequent GO terms (each occurring ≥100 times in UniRef90). ~46M proteins had ≥1 annotation (~2.3 annotations/protein on average).
- **Leakage prevention**: GO annotations removed for ~600K proteins with ≥40% BLASTP similarity to any benchmark test-set record.
- **Benchmarks** (9 tasks): 4 from TAPE (secondary structure 3-class, remote homology, fluorescence, stability) + 5 new (signal peptide, major PTMs, neuropeptide cleavage, disorder, fold class). Tasks span local and global labels, continuous/binary/categorical outputs.

## Training Recipe

- **Dual pretraining tasks**: (1) Sequence denoising—5% random token replacement. (2) GO annotation recovery—25% removal of true annotations, 0.01% random false annotations added; 50% of samples receive all-zero annotation input.
- **Loss**: categorical cross-entropy (sequence) + binary cross-entropy (GO annotations), summed.
- **Sequence-length cycling**: alternate between 128, 512, 1024 tokens every 15 min to avoid overfitting to a single length.
- **Hardware**: single Nvidia Quadro RTX 5000 GPU.
- **Duration**: 28 days; ~670M records processed (~6.4 epochs over ~106M proteins); 280 proteins/sec.
- **Fine-tuning protocol**: (1) freeze pretrained layers, train new FC output layer ≤40 epochs; (2) unfreeze all layers, train ≤40 epochs; (3) 1 final epoch at larger sequence length. LR reduction on plateau + early stopping. Average fine-tuning: ~14 min on single GPU.
- **Framework**: TensorFlow / Keras.

## Key Ablations & Design Choices

| Choice | Result |
|---|---|
| With vs without pretraining | Major gains on most benchmarks; secondary structure +4 pp accuracy, remote homology +22 pp accuracy (Table 2) |
| GO annotation pretraining task | Benefits secondary structure, remote homology, fold classes (Supp. Fig. S2); other tasks unaffected |
| Pretraining duration scaling | LM loss keeps improving; GO loss saturates; downstream tasks (secondary structure, remote homology) improve with more pretraining without saturation (Fig. 3) |
| Sequence length 128 vs 512/1024 during pretraining | 128 slightly worse; 512 and 1024 similar (Fig. 2) |
| Generalisation across lengths at inference | Modest decrease for very long sequences; some tasks actually improve at longer lengths (Fig. 4) |
| ProteinBERT (16M) vs TAPE Transformer (38M) | Comparable or better on all four TAPE benchmarks despite ~2.4× fewer params |
| ProteinBERT (16M) vs ProtT5-XL (3B) | ProtT5 outperforms on secondary structure (Q3 81.2 vs 76.1) but uses ~190× more params |

## Reported Insights

- GO annotation prediction is a protein-specific pretraining signal unavailable in NLP; teaches the model diverse functions (subcellular localisation, biochemical roles, pathways).
- Non-redundant UniRef90 is preferable to full UniProt for pretraining: eliminates organism-sampling bias (e.g., >1M HIV-1 sequences in UniProt for only 9 real proteins).
- Global attention (linear complexity) enables processing sequences of tens of thousands of residues intact, unlike quadratic self-attention.
- Omitting positional embeddings—relying on convolutions + START/END tokens—avoids length-generalisation failures observed with learned positional embeddings.
- Model is extremely frugal: single-GPU pretraining (28 days) vs 4 GPUs / 3.5 weeks (UniRep) vs thousands of GPUs/TPUs (ProtTrans).
- Transfer-learning benefit is task-dependent: harder tasks (secondary structure, remote homology) benefit most from longer pretraining.
- Global attention yields simpler interpretability (2D attention map) than self-attention (3D); fine-tuning on signal peptide visibly shifts attention to cleavage sites (Fig. 5).

## References Worth Chasing

1. **ESM (Rives et al., 2021)** – 650M param protein LM; pretrained on ~250M sequences; main large-scale competitor.
2. **ProtTrans / ProtT5-XL (Elnaggar et al., 2021)** – 3B param model; trained on supercomputer; outperforms ProteinBERT on secondary structure.
3. **TAPE (Rao et al., 2019)** – Standardised protein benchmarks; 38M param BERT baseline.
4. **UniRep (Alley et al., 2019)** – LSTM-based protein LM; 4 GPUs / 3.5 weeks.
5. **BERT (Devlin et al., 2018)** – Architectural inspiration; ProteinBERT modifies the Transformer design.
6. **Gene Ontology (Ashburner et al., 2000)** – Source of ~45K function terms; 8943 used for pretraining.
7. **UniRef90 (Suzek et al., 2007)** – Non-redundant clustering at 90% identity; pretraining corpus.
8. **MSA Transformer (Rao et al., 2021)** – Protein-centric pretraining via MSA; mixed results noted.
9. **UDSMProt (Strodthoff et al., 2020)** – Another protein language model compared in background.

## Notes / Open Questions

- Training tokens not directly reported; ~670M records × variable length (128/512/1024) gives a rough estimate of ~200–400B tokens depending on length distribution.
- Training FLOPs not reported; 28 GPU-days on RTX 5000 (~11.2 TFLOPS FP32) gives an upper bound of ~2.7 × 10^19 FLOPs.
- Contact prediction excluded because the model produces no pairwise outputs—a fundamental architectural limitation.
- No direct comparison to ESM at time of publication due to lack of comparable published results on the same benchmarks.
- The paper predicts larger ProteinBERT variants should improve; unclear if this was ever explored.
- GO annotation quality and coverage are uneven across organisms; potential bias in the pretraining task.
- The 40% BLASTP similarity threshold for leakage prevention is conservative but principled.

## Ablations (Rev 4)

| # | Ablation | Setup | Finding | Source |
|---|----------|-------|---------|--------|
| 1 | Pretraining vs no pretraining | Train ProteinBERT from scratch on each downstream task vs fine-tune from the pretrained checkpoint | Pretraining yields large gains on most of the 9 benchmarks (Table 2); a few tasks are unaffected | §3.2, Table 2 |
| 2 | Pretraining duration | Fine-tune from 371 snapshots taken along the pretraining trajectory; measure downstream test performance | Performance improves monotonically with more pretraining on harder tasks (secondary structure, remote homology) with no saturation; some tasks plateau early or do not benefit | §3.2, Fig. 3, Supp. Fig. S1 |
| 3 | GO-annotation pretraining task | Pretrain with vs without the dual GO-annotation denoising objective (sequence-only MLM baseline) | Removing GO hurts secondary structure, remote homology, and fold-class benchmarks; other tasks are largely insensitive | §3.2, Supp. Fig. S2 |
| 4 | Input sequence length generalisation | Evaluate fine-tuned models at input lengths 512 → 16 384 on 4 benchmarks with long test proteins | Performance degrades only modestly at longer lengths; sometimes improves (e.g. 16 384 on Major PTMs), confirming length-agnostic architecture works | §3.3, Fig. 4 |
| 5 | Effect of fine-tuning on global attention | Compare 24 global-attention head maps before vs after fine-tuning on signal-peptide task for two proteins | Fine-tuning chiefly modifies the last (6th) global attention block; head #1 sharpens onto the cleavage-site region in positives | §3.4, Fig. 5 |

**Top take-away:** The GO-annotation denoising auxiliary task is the key novel design choice — its removal specifically hurts structure-related benchmarks (secondary structure, remote homology, fold classes), while pretraining length keeps paying off on the hardest tasks without saturating, suggesting ProteinBERT is under-trained rather than under-parameterised.
