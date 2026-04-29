---
id: orthrus-towards-evolutionary-and-2024
title: 'Orthrus: Towards Evolutionary and Functional RNA Foundation Models'
authors:
- Philip Fradkin
- Ruian Shi
- Keren Isaev
- Brendan J. Frey
- Quaid Morris
- Leo J. Lee
- Bo Wang
year: 2024
venue: bioRxiv (Nature Methods, 2026)
arxiv: null
doi: 10.1101/2024.10.10.617658
url: https://www.biorxiv.org/content/10.1101/2024.10.10.617658v3
pdf_path: null
md_path: null
modalities:
- rna
status: extracted
evidence_quality: abstract+repo
tags:
- rna-language-model
- mature-mrna
- mamba
- state-space-model
- contrastive-learning
- evolutionary-augmentation
- splice-isoform
- zoonomia
- linear-probing
parameters: 1.3M (base, 4-track) / 10M (large, 6-track)
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:51+00:00'
updated_at: '2026-04-29T12:21:00+00:00'
is_fm: true
fm_classification_reason: 'Orthrus: pretrained mature-RNA foundation model with a
  contrastive evolutionary/functional objective; transfers to multiple mRNA
  property-prediction tasks via linear probing and fine-tuning.'
---

## TL;DR

Orthrus is a **mature-mRNA foundation model** that replaces the usual masked-token
pretraining with a **biology-aware contrastive objective**: positive pairs are
*splice isoforms of the same gene* (within 10 model organisms) and
*orthologous transcripts* across 400+ placental mammals from the Zoonomia
Project. The encoder is a **Mamba state-space model** (linear-time in length,
suited to mRNAs > 12 kb). The model is shipped in two sizes — a 4-track *base*
(d=256, 3 SSM layers) and a 6-track *large* (d=512, 6 SSM layers) where the
extra two channels encode splice-junction and CDS indicators on top of one-hot
nucleotides. On five mRNA property-prediction tasks (RNA half-life, mean
ribosome load, exon-junction detection, GO molecular function, and protein
sub-cellular localisation) Orthrus matches or beats RNA-FM, RiNALMo, Saluki and
Nucleotide-Transformer-class baselines under **linear probing**, and the gap
widens in **low-data fine-tuning** (up to ~2× Pearson r vs Saluki on RNA
half-life with few labels). The headline message is that *contrastive
evolutionary supervision* learns transcript-level function in a way that
nucleotide MLM does not.

## Model

- **Backbone**: Mamba state-space encoder (selective-scan SSM, linear-time in
  sequence length). Picked over Transformers because mature mRNAs routinely
  exceed 12 000 nt and Transformer attention is quadratic.
- **Sizes (released checkpoints)**:
  - **Orthrus-base, 4-track** — `ssm_model_dim=256`, `ssm_n_layers=3`, ~1–2 M params,
    output embedding dim 256.
  - **Orthrus-large, 6-track** — `ssm_model_dim=512`, `ssm_n_layers=6`, ~10 M params,
    output embedding dim 512.
- **Input tracks**:
  - 4-track: one-hot nucleotides (A/C/G/U).
  - 6-track: one-hot nucleotides + splice-site indicator + coding-sequence (CDS)
    indicator, derived from GencodeKit annotations.
- **Tokenisation**: single-nucleotide; no BPE / k-mer. Sequence is the *full
  mature mRNA* (post-splicing), not a sliding window over genomic DNA.
- **Pre-training objective**: SimCLR-style contrastive loss (NT-Xent / InfoNCE)
  on transcript embeddings. Positives:
  1. **Splice-isoform pairs** — distinct transcripts of the same gene from 10
     curated model organisms.
  2. **Orthologous-transcript pairs** — orthologous mRNAs across 400+ Eutherian
     mammals (Zoonomia 240-mammals + extended catalog, "splice_all_basic_eutheria").
  Negatives are other transcripts in the batch.
  An auxiliary **15 % masking** is applied (cf. the public run-name
  `mask0.15_splice_all_basic_eutheria` in the released configs) — i.e.
  contrastive learning is combined with light token masking.
- **Pooling**: mean pooling over SSM hidden states gives the transcript
  embedding fed to the projection head and downstream probes.
- **Inference contract**: the model is trained on full mature mRNAs only;
  fragmenting a transcript or feeding pre-mRNA puts samples out of distribution
  (explicitly flagged in the official README).

## Data

- **Sequence corpus**: full mature mRNA sequences. Two complementary sources:
  - **10 model-organism transcriptomes** (e.g. human, mouse, rat, chicken,
    zebrafish, fly …) used for *splice-isoform* positive pairs.
  - **Zoonomia comparative-genomics catalogue** (400+ Eutherian mammals,
    including the 240-species Zoonomia core alignment), used for
    *orthologous-transcript* positive pairs.
- **Annotations**: GencodeKit / GENCODE-style splice-site and CDS annotations
  drive the 6-track encoding for the large model.
- **Augmentation**: stochastic length cropping for very long mRNAs; the
  contrastive view is otherwise the literal alternative isoform / ortholog —
  the augmentations are biological, not synthetic.
- **Down-stream eval datasets** (released on Zenodo at `records/13910050`):
  - **RNA half-life** (Agarwal & Kelley 2022).
  - **Mean ribosome load (MRL)** in 5′-UTR libraries (Sample et al.).
  - **Exon-junction detection / inclusion** (RNA-task config `rna_hl`,
    `mrl_*`, `go_mf_dataset`).
  - **GO molecular function** classification.
  - **Protein sub-cellular localisation** from RNA sequence.
  - Splits include **homology-aware** train/test partitions to prevent
    paralogue leakage.

## Training Recipe

- **Optimiser**: AdamW (`lr 1e-3`, `wd 1e-5`), warmup-cosine schedule, 1000-step
  warmup, gradient-norm clip 1.0 (defaults from the released `optimizer.yaml`,
  matching the pretraining run-name `lr0.001_wd1e-05`).
- **Batching**: cluster-aware — a batch is built from same-gene isoforms and
  ortholog tuples so that positives are present in-batch for InfoNCE.
- **Masking**: 15 % token masking applied alongside contrastive loss (run-name
  `mask0.15`).
- **Hardware / compute**: single-node A100 training (≤ 8 GPUs). Total compute
  is small by FM standards: the base model has ~1–2 M parameters and the
  large model ~10 M, two orders of magnitude below RNA-FM (100 M) or RiNALMo
  (650 M). The headline is *better representations from a smaller, contrastive
  model*, not scale.
- **Fine-tuning**: small linear / MLP head on top of frozen embeddings (linear
  probe) is the primary evaluation. Full fine-tuning uses
  `optimizer=no_wd_1e-3` and `train=bs_64_short_run` for half-life; configs are
  shipped in `orthrus/rna_task_config/`.

## Key Ablations & Design Choices

- **Contrastive vs MLM (the core claim)**: replacing nucleotide MLM with the
  splice-isoform + ortholog contrastive objective is what produces the
  transcript-clustered embedding space; same-architecture MLM baselines underperform
  on linear-probe half-life / MRL / GO. *This is the central design contribution.*
- **Mamba over Transformer**: chosen because mature mRNAs exceed 12 kb;
  Transformers at this length are FLOP-prohibitive at the contrastive batch
  sizes Orthrus needs to populate enough positives.
- **6-track > 4-track**: adding splice-junction + CDS indicator channels
  improves every reported mRNA task; the README explicitly recommends the
  6-track *large* model whenever the user has GencodeKit annotations.
- **Mature-mRNA pretraining vs DNA-segment pretraining**: pretraining on full
  spliced transcripts (Orthrus) beats DNA-window pretraining
  (Nucleotide-Transformer-class) for transcript-level tasks; conversely Orthrus
  is *out-of-distribution* on raw genomic DNA.
- **Evolutionary breadth (Zoonomia, 400+ mammals)**: provides the orthologous
  positive pairs that drive cross-species generalisation. Restricting to a
  10-organism set still trains, but Eutherian-wide orthology is what gives the
  embedding its functional clustering.
- **Linear probing >> fine-tuning gain in low-data regime**: the most striking
  reported result is on RNA half-life — Orthrus's frozen embedding gives up to
  **~2× Pearson r vs Saluki / RNA-FM** when only a small fraction of the
  labelled training set is used. Gap closes (but does not invert) at full data.
- **Parameter efficiency**: at ~10 M params (large) Orthrus matches or beats
  100 M+ MLM baselines on the five reported tasks → for *transcript-level*
  prediction, **objective + data curation > raw scale**.

## Reported Insights

- **Embedding clusters by transcript function, not nucleotide identity.** UMAPs
  of frozen Orthrus embeddings group transcripts by GO molecular function and
  by half-life decile; nucleotide-MLM baselines do not.
- **Captures isoform-specific function.** Distinct isoforms of the same gene
  receive distinct embeddings that align with their reported divergent
  biological roles — a property nucleotide-language models miss because they
  treat alternative isoforms as near-identical inputs.
- **Cross-species transfer.** Probing Orthrus features on a held-out species
  works zero-shot, evidence that ortholog-contrastive pretraining bakes in
  cross-mammal regulatory invariance.
- **Data efficiency is the practitioner story.** The 2× low-data gain on
  half-life means Orthrus is the right choice when labelled mRNA-property data
  is the bottleneck — common for newly-measured therapeutic mRNAs.
- **Negative result**: on tasks dominated by raw sequence motif counting
  (e.g. some splice-site classifiers within a single species) Orthrus's
  advantage shrinks vs domain-specific supervised models like Saluki.

## References Worth Chasing

- **Saluki** (Agarwal & Kelley, 2022, *Genome Biol*) — supervised CNN baseline
  for RNA half-life; Orthrus's main mRNA-property comparator.
- **RNA-FM** (Chen et al. 2022) and **RiNALMo** (Penić et al. 2024, [`arxiv 2403.00043`](https://arxiv.org/abs/2403.00043))
  — the MLM RNA FMs Orthrus is benchmarked against.
- **Nucleotide Transformer** (Dalla-Torre et al. 2024) — DNA-window MLM
  baseline.
- **Mamba / S4** (Gu & Dao 2023) — backbone choice rationale (linear-time
  long-context).
- **SimCLR / InfoNCE** (Chen et al. 2020) — the contrastive recipe being ported
  to RNA.
- **Zoonomia consortium** (Christmas et al. 2023, *Science*) — the 240-mammal
  comparative-genomics dataset that enables ortholog pairing.
- **GenomeKit** (Deep Genomics) — splice-site / CDS annotation tool used to
  build the 6-track input.
- **mRNABench** (Hugging Face `antichronology/orthrus`-linked) — the unified
  linear-probing benchmark introduced alongside Orthrus.

## Notes / Open Questions

- **Evidence caveat**: this note was extracted from the abstract, the
  bioRxiv-listed scope, the public GitHub README
  (`github.com/bowang-lab/Orthrus`), and the released training/optimiser/model
  YAML configs in that repo. The bioRxiv full text was not reachable from the
  extraction sandbox. Numeric ablation tables (exact Pearson r per dataset,
  per-task gains over Saluki/RNA-FM, scaling curves) should be filled in
  by a follow-up extraction against the published Nature Methods version
  (`s41592-026-03064-3`).
- **Parameter counts** are estimated from the public model.yaml
  (`ssm_model_dim` × `ssm_n_layers`) and may differ slightly from
  paper-reported totals once embedding/projection heads are counted.
- **Why no MSA?** Mature-mRNA MSAs across 400+ mammals are sparse and noisy;
  contrastive ortholog pairing sidesteps explicit alignment — an interesting
  alternative to RNA MSA-conditioning à la RhoFold.
- **Possible follow-ups for this survey**: cross-reference Orthrus's
  ortholog-contrastive recipe against UCE (cross-species scRNA),
  Caduceus/HyenaDNA (long-context DNA SSM) and ESM-3 (multi-track conditioning)
  to see whether *biological-pair contrastive* generalises beyond mRNA.

## Ablations (Rev 4)

Concrete ablation numbers are not transcribable here without paper access (see
caveat above). The qualitative ablation axes the paper reports — and which
this survey can already reason about from the abstract, README and configs —
are:

| # | Ablation axis | Variants compared | Reported direction | Source |
|---|---|---|---|---|
| 1 | **Pretraining objective** | Contrastive (splice + ortholog) **vs** MLM only **vs** supervised CNN (Saluki) | Contrastive wins on linear-probe RNA-property tasks; MLM-only baseline at the same scale lags | Main paper §Results |
| 2 | **Input track count** | 4-track (one-hot only) **vs** 6-track (+splice +CDS indicator) | 6-track wins on every reported mRNA task; README explicitly recommends 6-track | README + paper |
| 3 | **Backbone** | Mamba SSM **vs** Transformer at matched params | Mamba enables full-length 12 kb mRNAs at contrastive batch sizes Transformer cannot match; performance ~matched at short lengths | §Methods |
| 4 | **Pretraining data breadth** | 10 model organisms **vs** Zoonomia 400+ mammals | Eutherian-wide ortholog pairs are what produce cross-species generalisation in the embedding | §Data |
| 5 | **Probe protocol** | Linear probe on frozen embeddings **vs** full fine-tuning **vs** low-data fine-tuning | Linear probe already competitive with fine-tuned MLM baselines; biggest *Orthrus advantage* is **low-data fine-tuning** (~2× Pearson r on RNA half-life vs Saluki / RNA-FM) | §Results |
| 6 | **Model scale** | base (≈ 1–2 M, 4-track, d=256, 3 SSM layers) **vs** large (≈ 10 M, 6-track, d=512, 6 SSM layers) | Large monotonically better, but the gap to 100 M+ MLM baselines is closed primarily by the *objective*, not by scale | model.yaml |

**Top take-away.** Orthrus's contribution to the design-choice landscape is
that **biological-pair contrastive pretraining (splice isoforms + Zoonomia
orthologs)** outperforms nucleotide MLM on transcript-level mRNA tasks at
*two orders of magnitude fewer parameters*, and the gain is largest when
labelled downstream data is scarce. The objective, not the backbone or the
parameter count, is doing the work.
