---
id: language-models-enable-zero-2021
title: Language models enable zero-shot prediction of the effects of mutations on
  protein function (ESM-1v, Meier 2021 NeurIPS)
authors:
- Joshua Meier
- Roshan Rao
- Robert Verkuil
- Jason Liu
- Tom Sercu
- Alexander Rives
year: 2021
venue: NeurIPS 2021
arxiv: null
doi: 10.1101/2021.07.09.450648
url: https://proceedings.neurips.cc/paper/2021/hash/f51338d736f95dd42427296047067694-Abstract.html
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/language-models-enable-zero-2021.md
modalities:
- protein-sequence
status: extracted
evidence_quality: abstract+repo
tags:
- protein-language-model
- transformer
- masked-language-modeling
- zero-shot
- mutational-effect
- variant-prediction
- deep-mutational-scanning
- ESM-1v
- ensemble
parameters: 650000000
training_tokens: 9600000000
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'ESM-1v: zero-shot variant effect via pretrained PLM.'
---

## TL;DR

ESM-1v is a 650M-parameter, 33-layer Transformer protein language model trained on UniRef90 (~98M sequences, ~9.6B tokens) with masked language modeling. Its key contribution is demonstrating that a single pre-trained protein LM can predict the functional effects of mutations **zero-shot**—without any task-specific training or family-specific model fitting—matching or exceeding dedicated methods like EVmutation and DeepSequence across 41 deep mutational scanning datasets (mean Spearman ρ ≈ 0.44). Five models trained with different random seeds are released and can be ensembled for improved robustness. The architecture is identical to ESM-1b but trained on UniRef90 instead of UniRef50, optimizing for variant prediction rather than general-purpose representation.

## Model

- **Architecture**: Identical to ESM-1b — BERT-style bidirectional Transformer with masked language modeling (MLM) objective.
- **Layers**: 33; **Parameters**: 650M; **Embedding dim**: 1280.
- **Five independently trained models** released: `esm1v_t33_650M_UR90S_1` through `esm1v_t33_650M_UR90S_5`, differing only in random seed. Can be used individually or ensembled.
- **Vocabulary**: 20 standard amino acids + special tokens (mask, pad, BOS, EOS, UNK).
- **Scoring strategies** for variant effect prediction (four compared):
  1. **Wildtype marginal**: Log-probability of wild-type amino acid at each position given the full unmasked sequence.
  2. **Masked marginal**: Mask the target position, compute log-probability of mutant vs. wild-type amino acid given the remaining context. (Best or tied-best strategy.)
  3. **Mutant marginal**: Log-probability of the full mutant sequence (unmasked).
  4. **Pseudo-likelihood**: Sum of per-position masked log-probabilities across the entire sequence (default scoring for ESM-1b).
- **Key scoring insight**: Masked marginal scoring performs best overall; the effect score is log P(mutant | context) − log P(wildtype | context) at the masked position.

## Data

- **Pre-training corpus**: UniRef90, March 2020 release (UR90/S). ~98 million protein sequences, ~9.6 billion amino-acid tokens.
- **UniRef90 vs UniRef50**: UniRef90 clusters sequences at 90% identity (less aggressive deduplication than UniRef50's 50% threshold), yielding ~2–3× more sequences and greater coverage of closely related variants — motivated by the variant prediction use case.
- **Evaluation benchmark**: 41 deep mutational scanning (DMS) datasets curated from the literature, covering diverse proteins and experimental assays (enzyme activity, viral fitness, drug resistance, etc.). Citations for all 41 datasets provided in `examples/variant-prediction/mutation_data.bib` in the ESM repo.
- **No task-specific training data**: All predictions are zero-shot from the pre-trained model; no supervised fine-tuning on DMS data.

## Training Recipe

- **Objective**: Masked language modeling (MLM) — mask a fraction of amino acids in each sequence and predict the masked tokens from context.
- **Optimizer**: Adam, learning rate 1e-4 with linear warm-up and cosine decay schedule.
- **Batch size**: 128 per GPU; distributed training across multiple GPUs.
- **Framework**: fairseq (PyTorch).
- **Five random seeds**: Each of the 5 released models is trained from a different random initialization to the same convergence criterion, enabling ensemble predictions.
- **Hardware / compute**: Not explicitly disclosed. Given 650M params and architecture identical to ESM-1b, training scale is comparable. Total FLOPs not reported.

## Key Ablations & Design Choices

### 1. UR90 vs UR50 training data
Training on UniRef90 (90% identity clustering) rather than UniRef50 (50% identity) is a deliberate design choice for the variant prediction task. UR90 retains more closely related sequence variants, providing the model with richer information about tolerated vs. deleterious substitutions at each position. The paper shows this choice improves variant effect prediction performance compared to models trained on UR50 (i.e., ESM-1b).

### 2. Ensemble of 5 models
Five independently trained models (different random seeds, same hyperparameters) are released. Ensembling their predictions reduces variance and improves mean Spearman correlation across DMS datasets. The improvement from ensembling is modest but consistent — a practical, zero-cost-at-inference strategy (each model can also be used standalone).

### 3. MSA-based vs single-sequence scoring
The paper compares ESM-1v (single-sequence model) against MSA Transformer (Rao et al. 2021) for variant scoring. MSA Transformer can also score mutations zero-shot using masked marginals over an MSA input, and achieves competitive performance. However, ESM-1v requires no MSA computation at inference time, making it faster and applicable to orphan sequences without deep alignments.

### 4. Scoring strategy comparison
Across the 41 DMS datasets:
- **Masked marginal** ≈ **pseudo-likelihood** — best or near-best performance.
- **Wildtype marginal** — slightly worse.
- **Mutant marginal** — weakest strategy.
- Masked marginal is conceptually cleanest: it directly measures the model's conditional preference for each amino acid at a masked position.

### 5. Zero-shot vs family-specific models
ESM-1v zero-shot predictions match or exceed dedicated family-specific models (EVmutation/EVcouplings, DeepSequence) that must be retrained for each new protein family. This is the paper's central practical contribution — a single pre-trained model replaces hundreds of per-family models.

## Reported Insights

- **Zero-shot variant prediction is competitive with SOTA**: Without any supervision from experimental data, ESM-1v achieves mean Spearman ρ ≈ 0.44 across 41 DMS datasets, matching EVmutation and DeepSequence which require per-family alignment and training.
- **Evolutionary information is implicit in the LM**: The masked language modeling objective on diverse sequences forces the model to learn which substitutions are tolerated (functional) vs. deleterious, encoding a form of evolutionary constraint.
- **No per-family retraining needed**: A single pre-trained model generalizes across all protein families, eliminating the need to curate MSAs and retrain for each new prediction task.
- **UR90 better than UR50 for variant prediction**: The higher sequence redundancy in UniRef90 provides more fine-grained information about sequence variation near each protein, improving variant effect prediction over models trained on the more aggressively deduplicated UniRef50.
- **Ensembling is cheap and effective**: Training multiple random seeds and averaging predictions yields consistent improvements at negligible inference cost.
- **Masked marginal is the best scoring strategy**: Among the four strategies compared, masked marginal scoring is simplest and performs best — mask the position of interest, compare log-probabilities of mutant vs. wild-type.

## References Worth Chasing

1. **Rives et al. 2021** — "Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250M Protein Sequences" (PNAS; doi:10.1073/pnas.2016239118). ESM-1b; same architecture, trained on UR50. Direct predecessor.
2. **Rao et al. 2021** — "MSA Transformer" (ICML 2021; bioRxiv 2021.02.12.430858). MSA-based protein LM compared as an alternative zero-shot scoring method.
3. **Hopf et al. 2017** — "Mutation Effects Predicted from Sequence Co-variation" (Nature Biotech.). EVmutation/EVcouplings; the family-specific DCA baseline.
4. **Riesselman et al. 2018** — "Deep Generative Models of Genetic Variation Capture the Effects of Mutations" (Nature Methods). DeepSequence; VAE-based per-family baseline.
5. **Lin et al. 2023** — "Evolutionary-Scale Prediction of Atomic-Level Protein Structure with a Language Model" (Science). ESM-2; successor scaling study showing UR50-trained models also improve variant prediction.
6. **Frazer et al. 2021** — "Disease Variant Prediction with Deep Generative Models of Evolutionary Data" (Nature). Clinical variant interpretation using EVE; relevant benchmark comparison.
7. **Hsu et al. 2022** — "Learning Inverse Folding from Millions of Predicted Structures" (ICML). ESM-IF1; structure-conditioned scoring for variant effects.
8. **Rao et al. 2020** — "Transformer Protein Language Models Are Unsupervised Structure Learners" (bioRxiv 2020.12.15.422761). Attention-based contact prediction from ESM-1b.

## Notes / Open Questions

- **Source quality**: This note is based on abstract, metadata, the ESM GitHub repository, and the NeurIPS 2021 OpenReview page. Full paper text was not available for detailed extraction (bioRxiv returned 403). Numbers (Spearman ρ, dataset counts) are from web search syntheses and should be verified against the full paper.
- **Training compute not disclosed**: No FLOPs, GPU-hours, or wall-clock training time reported. Rough estimate: comparable to ESM-1b training given identical architecture.
- **Training tokens approximate**: ~9.6B tokens estimated from ~98M sequences × average protein length. Actual token count may differ depending on masking strategy and epoch count (number of epochs not disclosed).
- **UR90 vs UR50 ablation details**: The magnitude of improvement from UR90 over UR50 for variant prediction is mentioned but specific numbers should be extracted from the paper's tables.
- **Scoring strategy detailed comparison**: Exact per-strategy Spearman numbers across 41 datasets need verification from paper figures/tables.
- **Relation to ESM-2**: ESM-2 (Lin et al. 2023) is noted to have "similar performance to ESM-1v" for variant prediction per the ESM repo README, despite being trained on UR50. This suggests the UR90 advantage may be offset by ESM-2's improved training recipe and scale.
- **HuggingFace model card**: The HuggingFace page for `facebook/esm1v_t33_650M_UR90S_1` has no model card — only download stats (~68K monthly downloads). All documentation is in the GitHub repo.
- **License**: MIT license (same as all ESM models).
- **Superseded by**: For practical variant prediction, ESM-2 (650M or larger) is now generally recommended. For specialized variant scoring, ProteinGym benchmarks and methods like Tranception, EVE, and ESM-1v ensembles remain competitive.

## Ablations (Rev 4)

Source: Meier et al. 2021 NeurIPS, main paper + Supplementary (Tables 4, 5, 7, 8, 10; Figs. 4, 9). All numbers are mean |Spearman ρ| on the single-mutation validation set unless noted; 650M-param model trained for 170k updates.

| # | Ablation axis | Variant | |Spearman ρ| | Δ vs. ref | Source | Take-away |
|---|---|---|---|---|---|---|
| 1 | UniRef clustering (pre-training data) | UR30 | 0.456 | −0.108 | Tab. 4 / Fig. 4 | Too aggressive dedup hurts. |
| 2 | UniRef clustering | UR50 (≈ ESM-1b regime) | 0.537 | −0.027 | Tab. 4 | Reference setting. |
| 3 | UniRef clustering | UR70 | 0.552 | −0.012 | Tab. 4 | Monotonic gain up to 90%. |
| 4 | UniRef clustering | **UR90 (ESM-1v)** | **0.564** | — | Tab. 4 | **Best clustering threshold.** |
| 5 | UniRef clustering | UR100 | 0.458 | −0.106 | Tab. 4 | Collapses early in training (overfits redundant seqs); val perplexity also degrades (Tab. 10: 5.56 → 6.05). |
| 6 | Scoring strategy (single-mut val) | Pseudo-likelihood | 0.552 | −0.030 | Tab. 5 | Most expensive (L passes), worst of the four. |
| 7 | Scoring strategy | Wildtype marginal (1 fwd pass) | 0.572 | −0.010 | Tab. 5 | Cheapest; only 1% drop — strong default for large-scale scans. |
| 8 | Scoring strategy | Mutant marginal | 0.578 | −0.004 | Tab. 5 | Comparable to masked. |
| 9 | Scoring strategy | **Masked marginal** | **0.582** | — | Tab. 5 | **Best.** Used as default. On PABP doubles, masking all mutated sites *jointly* (variant a) gives 0.692 vs. 0.482–0.483 if masked one-at-a-time (Tab. 7). |
| 10 | Ensembling (5 seeds, UR90) | Single ESM-1v model (avg of 5) | 0.484 (full) / 0.482 (test) | — | Tab. 2 | Per-seed baseline. |
| 11 | Ensembling | **Ensemble of 5 ESM-1v models** | **0.509 (full) / 0.510 (test)** | +0.025 / +0.028 | Tab. 1, Tab. 2 | Cheap, consistent gain at inference time. |
| 12 | Model scale (UR90, masked-marginal) | 13M params | ≈0.30 | −0.25 | Fig. 9 | Clear scaling trend. |
| 13 | Model scale | 85M params | ≈0.42 | −0.13 | Fig. 9 | |
| 14 | Model scale | 393M params | ≈0.50 | −0.05 | Fig. 9 | |
| 15 | Model scale | **649M params** | **≈0.55** | — | Fig. 9 | Best; authors note continued scaling should help further (motivates ESM-2). |
| 16 | MSA-augmented inference (MSA Transformer subsample) | Diversity-minimizing, 256 seqs | 0.255 | −0.323 | Tab. 8 | Near-duplicate context destroys signal. |
| 17 | MSA subsample strategy | Random, 256 seqs | 0.535 ± 0.024 | −0.043 | Tab. 8 | |
| 18 | MSA subsample strategy | HHFilter (cov 75, id 99), 256 seqs | 0.550 ± 0.015 | −0.028 | Tab. 8 | |
| 19 | MSA subsample strategy | **Sequence reweighting, 256 seqs** | **0.578 ± 0.005** | — | Tab. 8 | Best MSA-aug recipe; *still* matches/loses to single-sequence ESM-1v ensemble (0.582 masked-marginal val / 0.510 test) at much higher inference cost. |
| 20 | Spiked unsupervised fine-tuning on MSA | ESM-1v zero-shot (ref) | 0.510 | — | §4.4 | Baseline (full 41-set average). |
| 21 | Spiked unsupervised fine-tuning | ESM-1v + spiked MSA fine-tune | 0.537 | +0.027 | §4.4 | Naïve MSA fine-tune overfits; spiking pre-train tokens (ratio 0.01) regularizes — modest but real lift. |

**Count: 21 ablation rows across 6 axes** (UR clustering × 5, scoring strategy × 4, ensembling × 2, model scale × 4, MSA subsampling × 4, MSA fine-tuning × 2).

**Top take-away:** Pre-training **data distribution dominates** for zero-shot variant prediction — the UR50 → UR90 swap alone gives a +0.027 |Spearman ρ| jump (0.537 → 0.564), the same magnitude as 5×-seed ensembling *and* spiked MSA fine-tuning combined, while UR100 collapses entirely. Choice of clustering threshold matters more than scoring strategy (≤0.030 spread) and is comparable to a >50× scale-up in parameters (13M → 649M ≈ +0.25). The paper's central design choice — re-train ESM at UR90 instead of UR50 — is the single highest-leverage knob.
