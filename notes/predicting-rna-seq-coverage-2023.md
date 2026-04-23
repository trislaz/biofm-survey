---
id: predicting-rna-seq-coverage-2023
title: Predicting RNA-seq coverage from DNA sequence as a unifying model of gene regulation
authors:
- Johannes Linder
- Divyanshi Srivastava
- Han Yuan
- Vikram Agarwal
- David R. Kelley
year: 2023
venue: Nature Genetics (2025)
arxiv: null
doi: 10.1038/s41588-024-02053-6
url: https://www.nature.com/articles/s41588-024-02053-6
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/predicting-rna-seq-coverage-2023.md
modalities:
- epigenome
- rna
parameters: ~250M (full model; not explicitly stated — comparable to Enformer; ablation
  mini models ~30M)
training_tokens: ~10K coverage tracks (7,611 human + 2,608 mouse) × tiled 524 kb genome
  windows
training_compute: ~25 days per replicate on 2× NVIDIA A100 (40 GB); 4 replicates trained
status: extracted
evidence_quality: abstract+repo
tags:
- RNA-seq
- long-context
- multi-task
- genomics
- U-Net
- transformer
- variant-effect-prediction
- splicing
- polyadenylation
- Enformer-extension
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'Borzoi: large pretrained sequence-to-coverage model, widely
  used as backbone.'
---

## TL;DR

Borzoi is a convolutional + transformer + U-Net model from Calico (Linder & Kelley) that extends Enformer to predict **RNA-seq coverage at 32 bp resolution** from **524 kb input DNA sequences**. By training jointly on RNA-seq, CAGE, DNase-seq, ATAC-seq and ChIP-seq across human and mouse, it learns transcription, splicing, and polyadenylation in a single unified model — no gene annotations needed at inference. It matches or outperforms specialised models (Enformer for eQTLs, Pangolin for sQTLs, APARENT2 for paQTLs) and enables attribution-based discovery of tissue-specific regulatory motifs. Published as preprint Aug 2023; Nature Genetics Jan 2025.

## Model

- **Name**: Borzoi
- **Architecture**: Conv tower → 8-layer transformer (self-attention with relative positional encodings at 128 bp resolution) → 2-stage U-Net upsampling back to 32 bp resolution.
  - Initial conv: 512 filters, kernel 15, pool 2.
  - Residual tower: 6 blocks, filters 608→1536 (divisible by 32), kernel 5, pool 2 each.
  - Transformer: 8 heads, key size 64, 32 position features, dropout 0.2.
  - Two U-Net conv blocks (kernel 3): upsample 128→64→32 bp by combining transformer output with skip connections from the conv tower.
  - Final conv: 1920 filters, dropout 0.1.
  - Species-specific heads: softplus activation, 7,611 human outputs / 2,608 mouse outputs.
- **Input**: 524,288 bp one-hot encoded DNA (A/C/G/T).
- **Output**: 6,144 bins × N tracks at 32 bp resolution (central 196,608 bp after cropping 5,120 bins per side).
- **Key simplifications vs Enformer**: max pooling (not attention pooling), single conv per residual block (not two), 8 transformer layers (not 11), central-mask-only relative position embeddings.
- **Framework**: TensorFlow 2.15.

## Data

- **RNA-seq**: 867 human + 278 mouse coverage tracks from ENCODE (diverse tissues/cell types/developmental stages). 89 additional GTEx tracks (recount3, 30 meta-tissues, k-means selected replicates).
- **CAGE**: FANTOM5 stranded tracks (forward + anti-sense).
- **DNase-seq / ChIP-seq**: ENCODE + Epigenomics Roadmap.
- **ATAC-seq**: pseudo-bulk scATAC-seq from CATlas.
- **Total output tracks**: 7,611 human + 2,608 mouse = 10,219.
- **Genome tiling**: 524 kb windows tiled across hg38 (human) and mm10 (mouse); 8-fold random partition of sequences, 6 folds train / 1 val / 1 test; orthologous regions in same partition.
- **RNA-seq normalisation**: bin values raised to 3/4 power; if still >384 after that, additional sqrt on residual ("squashed scale"). Limits contribution of highly-expressed genes.

## Training Recipe

- **Optimiser**: Adam (β₁=0.9, β₂=0.999), LR 6×10⁻⁵ with 20K step warm-up.
- **Batch size**: 2 (split across 2 GPUs).
- **Loss**: Poisson multinomial — decomposed into magnitude (Poisson on summed coverage) + shape (multinomial on normalised profile), with 5× weight on shape term. Global gradient clip norm 0.15.
- **Augmentation**: reverse complement + random shift ±3 bp.
- **Regularisation**: L2 weight decay 2×10⁻⁸, dropout 0.2 (transformer) / 0.1 (final conv), batch-sync normalisation (momentum 0.9).
- **Duration**: ~25 days per replicate on 2× NVIDIA A100 (40 GB RAM). Epochs 130–180, patience 30.
- **Ensemble**: 4 replicates with random init + training order; ensemble average generally improves performance.
- **Multi-species**: alternating human/mouse batches, swapping species-specific head.

## Key Ablations & Design Choices

| Design choice | Finding |
|---|---|
| **RNA-seq only vs + DNase/ATAC/ChIP** | Adding epigenomic assays consistently improved RNA-seq test accuracy, eQTL classification, and enhancer-gene linking. |
| **Human-only vs + mouse** | Adding mouse data improved eQTL predictions and test accuracy. |
| **With vs without U-Net** | U-Net upsampling (128→32 bp) essential for splice-site resolution; without it, exon boundaries blurred. |
| **Longer context (524 kb vs Enformer 196 kb)** | Enables scoring of distal enhancers up to 262 kb from TSS (vs Enformer's ~100 kb effective range). Borzoi achieves higher AUPRC for enhancer-gene linking at all distances. |
| **Poisson multinomial loss** | Decomposition into magnitude + shape (5× shape weight) boosts performance vs standard Poisson. |
| **Ensemble (4 replicates)** | Ensemble mean Pearson R = 0.75 on RNA-seq test bins vs 0.74 single replicate; gene-level R = 0.87 vs 0.86. |
| **Mini Borzoi (~30M params)** | Used for ablation grid; trained on RTX 4090 / TITAN RTX with 393 kb input, 4 attention heads. |

## Reported Insights

- **Test performance**: bin-level Pearson R = 0.75 (RNA-seq, ensemble), gene-level R = 0.87; tissue-specific residual expression R = 0.58.
- **eQTL classification**: mean AUROC 0.794 across GTEx tissues (Enformer: 0.747); mean effect-size Spearman R = 0.334 (Enformer: 0.227).
- **sQTL classification**: competitive with Pangolin; Borzoi better at close-to-junction variants (≤200 bp), Pangolin better at de-novo splice-gain farther away; ensemble of both superior.
- **paQTL classification**: AUPRC 0.64–0.74; outperforms APARENT2; ensemble with APARENT2+Saluki best.
- **Tissue-specific TF motifs**: attribution-based MoDISco recovers known tissue regulators (SPI1 for blood, HNF4A for liver, MYOD1 for muscle, SOX9/REST for brain).
- **Alternative TSS and APA**: accurately predicts tissue-specific TSS usage ratios (Spearman R = 0.85) and distal-to-proximal polyadenylation ratios (R = 0.81).
- **Limitation**: alternative splicing across tissues not well captured; model tends to predict average RNA-seq shape. mRNA half-life determinants not found in attributions.
- **Variant scoring in unseen loci**: performance "only marginally affected by whether or not the variant occurs in genomic sequences seen during training".

## References Worth Chasing

- **Enformer** (Avsec et al., Nat Methods 2021) — predecessor architecture, 196 kb context, CAGE/ChIP/DNase.
- **Pangolin** (Zeng & Li, Genome Biol 2022) — specialised splice-variant predictor, useful comparator for sQTL tasks.
- **APARENT2** (Linder et al., Genome Biol 2022) — polyadenylation variant effect model from same first author.
- **Saluki** (Agarwal & Kelley, Genome Biol 2022) — mRNA degradation rate prediction.
- **CATlas** (Zhang et al., Cell 2021) — scATAC-seq atlas used for ATAC training data.
- **BPNet** (Avsec et al., Nat Genet 2021) — profile prediction with Poisson multinomial loss decomposition.
- **Borzoi-paper repo** (github.com/calico/borzoi-paper) — full replication scripts for training, evaluation, data processing.

## Ablations (Rev 4)

Conducted on a "mini-Borzoi" (~30M params, 393,192 bp input, 4 attention heads) so the full ablation grid would fit on RTX 4090 / TITAN RTX hardware. Each condition trained for 2 CV folds (4 for the all-features baseline); 30–90 days per run. Reported in Methods §"Model ablation experiments" and Supplementary Figs 7a–c (RNA-seq accuracy + enhancer–gene linking) and 9d (eQTL classification).

| # | Ablation axis | Conditions compared | Finding (Rev 4) |
|---|---|---|---|
| 1 | **Auxiliary assays vs RNA-only** | Multispecies (CAGE+DNase+ATAC+ChIP+RNA) vs Multispecies (D/A/RNA) vs Multispecies (RNA) | Adding DNase/ATAC (and further CAGE/ChIP) to RNA-seq consistently improved RNA-seq test accuracy, eQTL classification, and CRISPR enhancer–gene linking AUPRC. Strongest single contributors are DNase + ATAC. |
| 2 | **Multispecies vs human-only** | Multispecies (full) vs Human (full); same comparison for D/A/RNA and RNA-only subsets | Including mouse training data substantially improved eQTL effect-size Spearman R and held-out RNA-seq accuracy at matched data composition. |
| 3 | **U-Net hourglass vs no U-Net** | Multispecies (full, 32 bp output via U-Net) vs Multispecies (No U-Net, 128 bp output) | U-Net upsampling from 128 → 32 bp is required for splice-site-resolution coverage; without it exon boundaries are blurred and gene-level shape correlation degrades. Architecture-only ablation. |
| 4 | **Cell-line scope** | K562 (full) vs K562 (D/A/RNA) vs K562 (RNA) | Within a single cell line the same ordering holds: auxiliary assays > D/A/RNA > RNA-only — ruling out that the multispecies/multi-assay gains come purely from cross-tissue diversity. |
| 5 | **GTEx-only RNA training** | Human (GTEx RNA) vs Human (full) | Restricting to 89 GTEx RNA tracks alone underperforms the full ENCODE+GTEx multi-assay setup, motivating the heterogeneous track set. |
| 6 | **Context length (524 kb vs 196 kb)** | Borzoi (524 kb, 32 bp) vs Enformer (196 kb, 128 bp) on enhancer–gene linking and eQTLs (Figs 4c–d, 5b–d) | Borzoi achieves higher AUPRC at every TSS-distance bin (incl. 98–262 kb, unreachable by Enformer) and higher eQTL AUROC (0.794 vs 0.747) and effect-size Spearman R (0.334 vs 0.227). |
| 7 | **eQTL aggregation statistic** | Differential log-sum across exons vs L2 norm of differential coverage (Fig 5b) | L2 norm beats the original sum statistic (AUROC 0.794 vs 0.772 with the same Borzoi ensemble); Borzoi+sum still beats Enformer+sum. |
| 8 | **Ensembling (4 replicates)** | Single replicate vs 4-replicate ensemble | Modest but consistent gains: bin-level R 0.74 → 0.75 (RNA-seq), gene-level R 0.86 → 0.87, eQTL Spearman 0.292 → 0.334. |

**Count: 8 ablation axes.**

**Top take-away:** the biggest single quality lever is **co-training on epigenomic assays (DNase/ATAC, plus CAGE/ChIP) alongside RNA-seq** — it improves RNA-seq prediction itself, eQTL discrimination, and enhancer–gene linking, and the effect replicates within a single cell line (K562). Mouse data and the U-Net hourglass are necessary complements (mouse for variant-effect generalisation, U-Net for sub-128 bp splice resolution), but the multi-assay choice is what makes Borzoi a unifying regulatory model rather than just an Enformer-with-RNA-seq.

## Notes / Open Questions

- Exact full-model parameter count not explicitly stated in paper or repo; likely ~250M based on architecture similarity to Enformer. Mini ablation models are ~30M.
- Training data is multiple TB (requester-pays GCS bucket `gs://borzoi-paper/data`); full reproduction is expensive.
- 4 replicate model weights publicly available as .h5 files; mini-Borzoi collection also released for modality-specific subsets.
- The published version (Nat Genet, Jan 2025) adds intronic polyadenylation QTL analysis and additional ablations vs the 2023 preprint.
- Future directions mentioned: megabase-scale context with efficient attention, ribosome profiling / CLIP-seq training data, personal genome training with GTEx genotypes.
- Code depends on three Calico repos: `borzoi`, `baskerville` (model engine), `westminster` (training orchestration). TF 2.15 + Python 3.10.
