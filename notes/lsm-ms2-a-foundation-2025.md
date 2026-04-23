---
id: lsm-ms2-a-foundation-2025
title: 'LSM-MS2: A Foundation Model Bridging Spectral Identification and Biological
  Interpretation'
authors:
- Gabriel Asher
- Devesh Shah
- Amy A. Caudy
- Luke Ferro
- Lea Amar
- Ana S. H. Costa
- Thomas Patton
- Niall O'Connor
- Jennifer M. Campbell
- Jack Geremia
year: 2025
venue: null
arxiv: '2510.26715'
doi: null
url: https://arxiv.org/abs/2510.26715v1
pdf_path: papers/lsm-ms2-a-foundation-2025.pdf
md_path: papers/md/lsm-ms2-a-foundation-2025.md
modalities:
- small-molecule
status: extracted
evidence_quality: medium
tags:
- foundation-model
- transformer
- mass-spectrometry
- metabolomics
- spectral-identification
- embedding
- retrieval
- contrastive-learning
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:05+00:00'
updated_at: '2026-04-22T20:22:34+00:00'
is_fm: true
fm_classification_reason: 'LSM-MS2: pretrained foundation model for mass spectrometry.'
---

## TL;DR

Transformer-based foundation model for tandem mass spectrometry (MS/MS) trained on millions of spectra. Learns a semantic chemical embedding space via contrastive separation. SOTA on spectral identification (MassSpecGym Top-1 Acc 0.739 vs 0.726 DreaMS), +30% on isomeric discrimination, +42% true positives on NIST plasma. Embeddings transfer to biological tasks (septic shock prediction F1 0.80, cystic fibrosis cohort separation) without spectral annotation. Proprietary model from Matterworks; architecture/param details withheld.

## Model

- **Architecture**: Transformer-based (details not disclosed; patented as "Large Spectral Model for MS2").
- **Input**: Raw MS/MS spectra (precursor + fragment ions with m/z and intensity).
- **Output**: Fixed-dimensional spectral embeddings in a learned chemical space.
- **Training objective**: Maximise separation in spectral space — contrastive/metric-learning style (exact loss not specified).
- **Inference modes**: (1) Embedding-based retrieval against a reference library for spectral identification; (2) sample-level aggregation of per-spectrum embeddings for downstream biological modelling.
- **Parameter count**: Not reported.

## Data

- **Pretraining corpus**: "Millions of MS/MS spectra" (exact count not given).
- **Reference library** (used for retrieval eval): ~1.8 M spectra, 99 K unique analytes, curated from NIST23, MSnLib, GNPS, MoNA, MassBank + internal Matterworks data. Analytes defined by 2D InChIKey (stereoisomers merged).
- **Evaluation benchmarks**:
  - MassSpecGym: 225,832 spectra / 28,923 analytes (public).
  - MWX-Isomers: 61 isomers across 22 groups (internal).
  - NIST SRM 1950 dilution series: 84 human plasma samples, 7 dilutions, RP+HILIC ± modes (internal).
  - Biological: antipsychotic overdose (80 mouse plasma), septic shock (ED serum, ~4 classes), cystic fibrosis (24 CF + 26 controls).
- **Instruments**: Thermo Orbitrap Exploris 120/240, Orbitrap Astral; HILIC & RP LC; positive/negative ionization.

## Training Recipe

- Contrastive/metric-learning pretraining on millions of spectra to learn a chemical embedding space.
- No explicit isomer-focused contrastive supervision — isomeric discrimination emerges from the general objective.
- Specific optimizer, schedule, batch size, augmentation, and epochs are **not disclosed**.
- Model is patented (PCT/US2024/038722); prior generation described in ChemRxiv preprint (Asher et al., 2024).

## Key Ablations & Design Choices (MOST IMPORTANT)

1. **Embedding retrieval vs. generative identification**: LSM-MS2 frames identification as nearest-neighbour retrieval in embedding space rather than generative structure prediction. All methods share the same reference library and retrieval pipeline, isolating algorithmic/training differences.
2. **Library-constrained ceiling**: On MassSpecGym, maximum achievable accuracy is 0.785 (per-spectrum). LSM-MS2 reaches 0.739 = 94% of ceiling, capturing 22% of the remaining gap over DreaMS.
3. **False-positive separation**: AUC for TP vs FP score distributions: Cosine 0.950, DreaMS 0.965, LSM-MS2 0.972. LSM-MS2's score distribution is smoother and more concentrated, enabling more reliable thresholding.
4. **Isomeric discrimination without explicit supervision**: 30% more isomers correctly identified than baselines; balanced per-group accuracy (10% gain on grouped metric). Leucine/isoleucine pair: mean top-1 acc 0.48 (balanced) vs baselines which are asymmetrically biased.
5. **Low-concentration robustness**: On NIST dilution series, LSM-MS2 maintains precision as dilution increases (p < 0.001 at 1:80, 1:120, 1:160 via Welch's t-test). +42% true positives, +33% precision globally vs Cosine Similarity.
6. **Sample-level biological embeddings**: Per-spectrum embeddings aggregated (method unspecified) into sample-level representations. Simple downstream ML on these embeddings matches or approaches task-specific pipelines built on identified metabolite panels (septic shock F1 0.80 vs 0.84 original; analysis time <1 hr vs days).
7. **Cosine Similarity ablation**: MZmine Cosine Similarity tested with 1–5 minimum matched signals. Increasing matched signals reduces both TPs and FPs; LSM-MS2 dominates across all configurations.
8. **MS1-only baseline**: Precursor m/z binned vectors fail to separate pharmacodynamically similar drug groups (CPZ/PER, OLA/CLO); LSM-MS2 MS/MS embeddings succeed, confirming fragmentation information is critical.

## Reported Insights

- Over 87% of spectra in GNPS remain unidentified; library-based approaches have hit a practical ceiling.
- A well-learned embedding space enables both identification and biological interpretation without manual annotation.
- Fragmentation-level (MS2) information is necessary for fine-grained discrimination — MS1 precursor mass alone is insufficient.
- Unsupervised UMAP of LSM-MS2 embeddings reveals biologically meaningful structure (drug mechanism clusters, disease vs control) without any labelled training.
- Reversed-phase positive-mode LC-MS captures strongest CF-vs-control metabolic signal, guiding experimental design.

## References Worth Chasing

- **DreaMS** (Bushuiev et al., Nat Biotech 2025) — closest SOTA competitor; self-supervised pretraining on MS/MS.
- **Casanova** (Yilmaz et al., ICML 2022) — transformer for de novo peptide sequencing; proteomics-only.
- **ICEBERG** (Goldman et al., Anal Chem 2024) — autoregressive fragmentation graph generation.
- **MassSpecGym** (Bushuiev et al., NeurIPS 2024) — public MS/MS benchmark.
- **Sanders et al. 2025** (arXiv 2505.10848) — Casanova applied to biological problems.
- **LSM-MS2 v1** (Asher et al., ChemRxiv 2024, doi:10.26434/chemrxiv-2024-k06gb-v3) — prior generation.

## Notes / Open Questions

- Architecture and parameter count are proprietary — hard to compare compute/scale with DreaMS or Casanova.
- Training data composition (public vs internal split) unclear; internal spectra may give an unfair advantage on internal benchmarks.
- MWX-Isomers and NIST dilution benchmarks are internal and not independently reproducible.
- Aggregation strategy from per-spectrum to sample-level embeddings is not described; this is a key design choice for downstream bio tasks.
- No generative capability yet (planned as future work).
- All authors are employees/shareholders of Matterworks, Inc. — potential conflict of interest.
- evidence_quality set to `medium`: public MassSpecGym benchmark is solid, but isomer and NIST benchmarks are internal; model is closed-source; ablations are limited to baseline comparisons rather than architectural choices.

## Ablations (Rev 4)

Note: paper exposes **no architectural/training ablations** (model is proprietary). All "ablations" below are baseline/configuration comparisons that isolate where LSM-MS2's lift comes from.

| # | Ablation / Comparison | Setting | Metric | Baseline → LSM-MS2 | Δ | Source |
|---|---|---|---|---|---|---|
| 1 | Retrieval method (vs Cosine Sim.) | MassSpecGym, per-spectrum | Top-1 Acc | 0.725 → 0.739 | +1.4 pp (22% of gap to 0.785 ceiling) | Table 1 |
| 2 | Retrieval method (vs DreaMS SOTA) | MassSpecGym, per-spectrum | Top-1 Acc / Top-1 MCES | 0.726 → 0.739 / 3.52 → 3.31 | +1.3 pp / −0.21 (closer chem. space) | Table 1 |
| 3 | TP-vs-FP score separation | MassSpecGym | ROC AUC | Cosine 0.950, DreaMS 0.965 → 0.972 | +0.007 over DreaMS | §4.1 |
| 4 | Isomer discrimination (no explicit isomer supervision) | MWX-Isomers, 61 isomers / 22 groups | per-analyte top-1 | baselines → LSM-MS2 | +30% analytes correct, +10% balanced group acc | §4.2 / Fig.1 |
| 5 | Leucine/Isoleucine balance | MWX-Isomers pair | mean top-1 acc | asymmetric baselines → 0.48 balanced | qualitative balance gain | §4.2 |
| 6 | NIST plasma global ID | NIST SRM 1950, optimal F1 thresh. | TP / Precision / F1 | 125 / 24.3% / 26.1% → 178 / 32.4% / 35.9% | +42.4% TP, +33.3% Prec., +37.5% F1 | Table 2 |
| 7 | Low-concentration robustness | NIST dilution series | Precision @ 1:80, 1:120, 1:160 | Cosine → LSM-MS2 | sig. higher (p<0.001 Welch's t) | §4.3 / App. D |
| 8 | Cosine Sim. min-matched-signals sweep (only true ablation) | NIST, MZmine, n=1–5 matched peaks | TP & spurious hits vs threshold | LSM-MS2 dominates **all 5** configs | n/a | App. D.4 / Fig.15–16 |
| 9 | MS1-only (precursor m/z bin vector) baseline | Antipsychotic overdose, UMAP | qualitative cluster separation | fails CPZ/PER & OLA/CLO → LSM-MS2 separates all | confirms MS2 fragmentation is essential | §5.1 / Fig.5 |
| 10 | Embedding pipeline vs identified-metabolite pipeline | Septic shock, ED serum | Macro F1 / time | original 0.84 / days → 0.80 / <1 hr | −0.04 F1, ~100× faster, no annotation | §5.2 |

**Top take-away:** No architectural ablation is reported; the only true hyperparameter ablation (Cosine Similarity min-matched-signals 1–5, App. D.4) shows LSM-MS2 dominates every Cosine configuration — i.e. its NIST gain (+42% TP, +33% precision) is **not** an artefact of a weak baseline. The MS1-only UMAP baseline (Fig. 5) further isolates that the lift comes specifically from learned MS2 fragmentation representations, not precursor mass.
