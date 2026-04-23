---
id: vitally-consistent-scaling-biological-2024
title: 'ViTally Consistent: Scaling Biological Representation Learning for Cell Microscopy'
authors:
- Kian Kenyon-Dean
- Zitong Jerry Wang
- John Urbanik
- Konstantin Donhauser
- Jason Hartford
- Saber Saberian
- Nil Sahin
- Ihab Bendidi
- Safiye Celik
- Marta Fay
- Juan Sebastian Rodriguez Vera
- Imran S Haque
- Oren Kraus
year: 2024
venue: null
arxiv: '2411.02572'
doi: null
url: https://arxiv.org/abs/2411.02572v2
pdf_path: papers/vitally-consistent-scaling-biological-2024.pdf
md_path: papers/md/vitally-consistent-scaling-biological-2024.md
modalities:
- imaging-microscopy
status: extracted
evidence_quality: high
tags:
- scaling-laws
- vision-transformer
- masked-autoencoder
- cell-microscopy
- data-curation
- intermediate-layers
- biological-representation
parameters: '1.9B (MAE-G/8); 307M (MAE-L/8); 25M (CA-MAE-S/16)'
training_tokens: '>8B image crops (MAE-G/8, 500 epochs over 16M images)'
training_compute: '48000 H100 GPU-hours (MAE-G/8); 15360 H100 GPU-hours (MAE-L/8); 400 A100 GPU-hours (CA-MAE-S/16)'
references_chased: false
added_at: '2026-04-22T19:42:01+00:00'
updated_at: '2026-04-22T20:28:09+00:00'
---

## TL;DR

Largest cell-microscopy foundation model: 1.9B-param ViT-G/8 MAE trained on 8B+ crops from a curated 16M-image dataset (Phenoprints-16M). Three-part recipe: (1) aggressive data curation (93M→16M images, 5× reduction, better diversity), (2) scaling parameters 307M→1.9B, (3) block-search via linear probes to select optimal intermediate layer (block 38/48 > final block). Result: 60% improvement in linear separability of genetic perturbations over prior SOTA MAE-L/8, +21% KS replicate consistency, +48% CM consistency. Strong linear scaling-law between training FLOPs and biological recall/consistency across all benchmarks (Appendix A.10).

## Model

- **Architecture**: ViT-G/8 (Zhai et al. 2022 scaling recipe), 1,860M parameters, 48 transformer blocks, model dim 1664, patch size 8×8.
- **Pre-training objective**: Masked Autoencoder (MAE) with 75% mask ratio, standard MAE decoder. Loss = L2 MSE + Fourier-domain reconstruction loss (weight α=0.01).
- **Input**: 256×256×6 (H×W×C) Cell Painting microscopy image crops (6-channel fluorescence).
- **Inference representation**: Intermediate block b*=38 (out of 48) selected via linear-probe search; NOT the final block.
- **Comparison models** (Table 4):
  - CA-MAE-S/16: 25M params, 12 blocks, dim 384, trained on RxRx3.
  - MAE-L/8 (prior SOTA): 307M params, 24 blocks, dim 1024, trained on RPI-93M or Phenoprints-16M.
  - Dino-V2 baselines: ViT-S/14 (25M), ViT-L/14 (307M), ViT-G/14 (1,100M) — natural images.
  - ViT-L/16 MAE (ImageNet-21k): 307M.

## Data

- **Phenoprints-16M**: 16M curated Cell Painting microscopy images, derived from 93M by aggressive filtering:
  1. Quality filters (focus, dead cells, artifacts).
  2. Remove missing/ambiguous perturbation metadata; require ≥3 experiments and ≥20 wells per perturbation.
  3. Under-sample controls (10% positive controls, 30% negative controls).
  4. Filter using perturbation consistency test (p<0.01 in either MAE-L/8 or WSL model) — keep only perturbations inducing consistent morphological change.
- **Result**: 5× fewer images but higher phenotypic diversity. Despite smaller size, leads to better downstream performance when combined with longer training (500 epochs).
- **RPI-93M**: Prior dataset (Kraus et al. 2024), 93M images, used for MAE-L/8 baseline.
- **RxRx3**: Whole-genome CRISPR knockout screen, 17,063 genes × 6 sgRNAs, HUVEC cells, 2.2M wells (used for evaluation; 80M forward passes per model).
- **RxRx3-core**: Public benchmark subset — 735 knockouts, 1,674 compounds × 8 concentrations, 222,601 wells.
- **JUMP-CP**: External validation dataset from different labs/assay protocols, ~8,000 gene knockouts.

## Training Recipe

- **Optimizer**: Lion (Chen et al. 2023), betas (0.9, 0.95), weight decay 0.05.
- **LR schedule**: One-cycle cosine decay, 10% linear warm-up.
- **MAE-G/8**: LR 3e-5, global batch size 8192, stochastic depth 0.6, 500 epochs, 256 H100 GPUs, >1 week, 48,000 H100 GPU-hours. Multiple restarts due to cluster issues.
- **MAE-L/8 (PP-16M)**: LR 3e-5, global batch size 16384, stochastic depth 0.3, 500 epochs, 128 H100 GPUs, 15,360 H100 GPU-hours.
- **CA-MAE-S/16 (RxRx3)**: LR 1e-4, global batch size 2048, stochastic depth 0.1, 100 epochs, 16 A100 GPUs, 400 A100 GPU-hours.
- All models: 75% mask ratio, standard MAE decoder, L2 loss + Fourier loss (α=0.01), LayerScale (Dehghani et al. 2023).
- Validation reconstruction loss was still decreasing at end of MAE-G/8 training → model not yet saturated.

## Key Ablations & Design Choices

### Scaling law: FLOPs vs. biological benchmarks (Appendix A.10, Figure 8)
- **Very strong linear correlation** between log training FLOPs and all downstream biological benchmarks (relationship recall, replicate consistency, linear probes).
- Extends prior scaling findings (Kraus et al. 2023) from <1B into the billion-parameter regime.
- Models in the scaling curve: CA-MAE-S/16 (400 A100-h) → MAE-L/8 RPI-93M (~similar to 15k H100-h) → MAE-L/8 PP-16M (15,360 H100-h) → MAE-G/8 PP-16M (48,000 H100-h).

### Model scaling: 307M → 1.9B parameters (Table 1)
- **MAE-L/8 (PP-16M) final block**: Recall 44.4%, KS 0.59, CM 16.2.
- **MAE-G/8 (PP-16M) final block**: Recall 45.4%, KS 0.60, CM 16.4.
- **MAE-G/8 trimmed (b*=38)**: Recall 45.4±0.15%, KS **0.63**, CM **18.2**.
- vs. prior SOTA MAE-L/8 (RPI-93M, b=24): Recall 44.4%, KS 0.52, CM 12.3.
- **Improvement over prior SOTA**: z-score of improvement = 5.21 for recall; KS +21% (0.52→0.63); CM +48% (12.3→18.2).

### Data curation: RPI-93M vs. Phenoprints-16M (Table 1, same MAE-L/8 architecture)
- MAE-L/8 on RPI-93M (b=24): Recall 44.4%, KS 0.52, CM 12.3.
- MAE-L/8 on PP-16M (b=24): Recall 44.4%, KS **0.59**, CM **16.2**.
- MAE-L/8 on PP-16M trimmed (b*=20): Recall 44.7%, KS 0.59, CM 16.2.
- Curated data (5× smaller) **matches or exceeds** the larger uncurated dataset on all metrics, especially replicate consistency (+13% KS, +32% CM).
- MAE-L/8 on RPI-93M trimmed (b*=15): Recall 44.3%, KS 0.57, CM 15.2 — trimming also helps on uncurated data.

### Intermediate block selection (block search) — most novel finding
- For MAE-G/8: best block b*=38 out of 48 (79% depth).
  - RxRx1 balanced accuracy: 0.51 at b*=38 vs. 0.47 at b=48 (+8.5%).
  - 60% better than MAE-L/8+ final block on RxRx1 linear separability.
  - Anax balanced accuracy: 0.32 at b*=38 vs. 0.305 at b=48 (+5%).
- For MAE-L/8 (PP-16M): b*=20 out of 24.
- For MAE-L/8 (RPI-93M): b*=15 out of 24.
- For CA-MAE-S/16: b*=12 (out of 12, i.e., final block is best for small model).
- **Natural image models show same pattern** (stronger):
  - Dino-V2 ViT-G/14: b*=16 out of 40 (40% depth!). Final block (b=40) performs **worse than untrained ViT-S**.
  - Dino-V2 ViT-L/14: b*=12 out of 24.
  - Dino-V2 ViT-S/14: b*=5 out of 12.
  - ViT-L/16 MAE (ImageNet): b*=11 out of 24 — 27% better than final block.
- **Proxy task correlation**: Anax linear probe accuracy correlates with whole-genome StringDB recall at Spearman ρ=0.97 and replicate consistency at ρ=0.91 (Figure 4). This enables cheap block search without expensive whole-genome evaluation.
- Untrained ViT-S does NOT show the parabolic block pattern → it is a learned phenomenon, not architectural.

### RxRx3-core compound-gene activity prediction (Table 3, Figure 5)
- Random baseline: Avg. precision 0.222.
- CellProfiler: 0.274 (z=2.55).
- CA-MAE-S/16: 0.273 (z=2.90).
- MAE-L/8 RPI-93M: 0.290 (z=3.77); trimmed: 0.299 (z=4.49).
- MAE-G/8 PP-16M: 0.302 (z=4.79); **trimmed: 0.309 (z=5.38)**.
- MAE-G/8 trimmed gives **42% relative improvement** over prior SOTA (z-score 3.77→5.38).

### External generalization: JUMP-CP (Table 2, completely different labs/protocols)
- CellProfiler: StringDB recall 0.191.
- CA-MAE-S/16: 0.214.
- MAE-L/8 RPI-93M: 0.226.
- MAE-G/8 trimmed: **0.235**.
- Trend holds on external data; absolute recall is lower than RxRx3.

### Dino-V2 on microscopy: failed (§A.9, Table 6)
- ViT-L/16 trained from scratch on RxRx3 and ViT-L/8 fine-tuned from MAE-L/8 both showed significant overfitting from start.
- Both underperformed CellProfiler and CA-MAE-S/16 on RxRx3-core (z-scores 2.13 and 1.76 vs. 2.90).
- Dino pretraining recipe does not transfer to microscopy data without significant modifications.

### Channel-agnostic vs. standard MAE (§3.2)
- 8×8 patch size MAEs perform ≥ 16×16 channel-agnostic variants for consistent 6-channel data.
- Opted for standard (non-channel-agnostic) MAEs for MAE-L/8 and MAE-G/8 since they require fewer tokens at inference.

## Reported Insights

1. **Scaling laws extend to billion-parameter regime** for cell microscopy MAEs — strong linear trend between FLOPs and all biological benchmarks.
2. **Data quality > data quantity**: 5× smaller curated dataset outperforms larger uncurated one, suggesting iterative curation (use best model to select data for next model) is viable.
3. **Intermediate blocks are universally better** than final blocks for biological tasks — true for MAEs trained on microscopy AND Dino-V2/MAE trained on natural images. Larger models benefit more.
4. **Cheap proxy for expensive benchmarks**: Anax linear probe (40 classes, small subset) correlates ρ=0.97 with whole-genome relationship recall, enabling efficient model/block selection.
5. **Validation loss still decreasing** at end of MAE-G/8 training → further parameter/compute scaling likely to yield continued improvements.
6. **MAE >> Dino-V2 for microscopy** — Dino recipe doesn't work on this data domain; MAEs are more robust SSL method for experimental microscopy.
7. Post-processing matters: TVN batch correction + chromosome arm bias correction are applied before evaluation.

## References Worth Chasing

- Kraus et al. 2024 — "Masked autoencoders for microscopy are scalable learners of cellular biology" (CVPR 2024). Prior SOTA, original scaling-law observation for MAEs on microscopy.
- Kraus et al. 2023 — NeurIPS GenBio workshop version. First scaling curve for MAEs on biological data.
- Celik et al. 2024 — "Building, benchmarking, and exploring perturbative maps" (PLOS Comp Bio). Defines the relationship recall benchmark and perturbation consistency framework.
- Alkin et al. 2024 — "MIM-Refiner" — intermediate block selection for MAEs, reports ViT-L/H k-NN accuracy peaks at intermediate layers.
- Dehghani et al. 2023 — "Scaling vision transformers to 22 billion parameters" (ICML). ViT-G architecture recipe, LayerScale.
- Sorscher et al. 2022 — "Beyond neural scaling laws: beating power law scaling via data pruning." Data curation theory.
- Fay et al. 2023 — RxRx3 dataset paper.
- Kraus et al. 2025 — RxRx3-core public benchmark.

## Notes / Open Questions

- **Not saturated**: Validation loss still improving at 500 epochs — how far does the scaling law extend? What happens at 10B+ params or with even more aggressively curated data?
- **Iterative curation loop**: Authors suggest using each generation's best model to curate data for the next — a biological-data analog of curriculum/data-mixing strategies in LLMs. Not yet validated beyond one iteration.
- **Block search is a post-hoc trick**: The optimal block depends on the downstream task proxy; it's unclear if a single b* generalizes across all possible biological tasks.
- **Dino failure is unexplained**: Authors could not find an effective recipe. Theoretical arguments that MAE ≈ contrastive learning exist but empirical gap is large.
- **Only Cell Painting data**: All training/eval is on 6-channel Cell Painting. Generalization to other microscopy modalities (brightfield, H&E, confocal) is untested.
- **No absolute accuracy reported on whole-genome recall** — only relative recall percentages at 5th/95th percentile thresholds of cosine similarity, making cross-paper comparison difficult.
- **Code**: https://github.com/recursionpharma/maes_microscopy. Weights for CA-MAE-S/16 at https://huggingface.co/recursionpharma/OpenPhenom. MAE-G/8 weights not publicly released.
