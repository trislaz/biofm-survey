---
id: systematic-evaluation-of-single-2026
title: Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals
  Attention Captures Co-Expression Rather Than Unique Regulatory Signal
authors:
- Ihor Kendiukhov
year: 2026
venue: null
arxiv: '2602.17532'
doi: null
url: https://arxiv.org/abs/2602.17532v1
pdf_path: papers/systematic-evaluation-of-single-2026.pdf
md_path: papers/md/systematic-evaluation-of-single-2026.md
modalities:
- scrna
- interactome
status: extracted
evidence_quality: high
tags:
- evaluation-framework
- interpretability
- attention-analysis
- gene-regulatory-network
- perturbation-prediction
- causal-ablation
- benchmarking
- scGPT
- geneformer
- CSSI
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:10+00:00'
updated_at: '2026-04-22T20:26:39+00:00'
---

## TL;DR

Rigorous **evaluation framework** (37 analyses, 153 statistical tests) for mechanistic interpretability of single-cell FMs (scGPT, Geneformer V2-316M). Main finding: attention patterns encode structured biological info (PPIs in early layers, TF regulation in late layers) but provide **no incremental value** for perturbation prediction over trivial gene-level baselines (variance/mean/dropout achieve AUROC 0.81–0.88 vs. 0.70 for attention/correlation edges). Pairwise edge scores add zero predictive contribution; causal ablation of "regulatory" heads causes no degradation. Constructive contribution: **Cell-State Stratified Interpretability (CSSI)** improves attention-derived GRN recovery up to 1.85× by controlling heterogeneity-driven dilution.

## Model

- **Not a new model.** This is a benchmark/evaluation paper assessing existing scFMs.
- **Models evaluated**: scGPT (gene-token transformer, autoregressive); Geneformer V2-316M (BERT-style, 18 layers × 18 heads = 324 heads, rank-based tokenisation); Geneformer V1-10M (6 layers × 4 heads, used for multi-model comparison).
- **Key methodological contribution**: CSSI (Cell-State Stratified Interpretability) — partitions cells into K strata via Leiden clustering on k-NN graphs from model embeddings, computes per-stratum Spearman correlations for each TF–target pair, aggregates via max (CSSI-max) or mean (CSSI-mean). Optimal K = 5–7 strata.
- **Evaluation framework** has 5 interlocking test families:
  1. Trivial-baseline comparison (univariate gene-level features vs. pairwise edges)
  2. Conditional incremental-value testing (cross-perturbation, cross-gene, joint splits; LR + GBDT)
  3. Expression residualisation + propensity matching (isolate edge-specific signal)
  4. Causal ablation with fidelity diagnostics (head masking, uniform attention replacement, MLP ablation)
  5. Cross-context replication (4 cell types, 2 perturbation modalities)

## Data

- **Perturbation datasets**:
  - Replogle CRISPRi K562: >640,000 cells, 2,024 perturbed genes, n=280 evaluable perturbations (primary)
  - Replogle CRISPRi RPE1: n=1,251 evaluable perturbations (replication)
  - Adamson CRISPRa K562: n=77 perturbations
  - Shifrut T-cell CRISPRi: n=7 perturbations (underpowered)
  - Tian iPSC neurons: n=7 perturbations (underpowered)
- **GRN reference databases**: TRRUST, DoRothEA, STRING (PPI)
- **CSSI validation**: DLPFC brain scRNA-seq (Maynard et al., 497 cells); Tabula Sapiens kidney (controlled-composition experiments)
- **scGPT scaling**: Archived kidney scaling runs — 3 model tiers (small/medium/large) × 3 seeds × 3 cell counts (200/1,000/3,000)

## Training Recipe

- **N/A** — evaluation paper. No new model training.
- CSSI requires only Leiden clustering on model embeddings + per-stratum Spearman correlations — no training loop.
- Perturbation-first evaluation: N_ctrl = 2,000 control cells, HVG = 2,000 (K562) or 3,309 (RPE1). LFC thresholds varied across 27 sensitivity conditions.

## Key Ablations & Design Choices

**Finding 1 — Trivial baselines dominate (both K562 and RPE1)**:
| Feature | K562 AUROC | RPE1 AUROC |
|---|---|---|
| Variance | 0.881 | 0.866 |
| Mean expression | ~0.84 | 0.851 |
| Dropout rate | ~0.81 | 0.797 |
| Attention (best layer) | 0.704 (L13) | 0.747 |
| Correlation | 0.703 | 0.658 |
| Gene-only logistic reg. | 0.895 | 0.942 |

→ Gene-level features massively outperform all pairwise edge scores (p < 10⁻¹²).

**Finding 2 — Zero incremental value from edges**:
- K562: Gene-only AUROC = 0.895 [0.884, 0.905]; +attention → ΔAUROC = −0.0004; +correlation → ΔAUROC = −0.002.
- RPE1: Gene-only AUROC = 0.942; +attention → ΔAUROC = +0.0001 (functionally zero).
- Robust across cross-gene splits, joint splits, LR vs. GBDT, AUROC/AUPRC/top-k recall. 559,720 observations → >99% power to detect ΔAUROC = 0.005.

**Finding 3 — Causal ablation shows distributed redundancy** (Geneformer V2-316M, K562):
- Ablating top-5/10/20/50 TRRUST-ranked heads: AUROC unchanged (0.701–0.704, all p > 0.10).
- Ablating 20 *random* heads: significant drop (0.697, p < 10⁻⁸) → "regulatory" heads are *less* causally important than random heads.
- Uniform attention replacement on top heads: no effect.
- MLP ablation at L15, L13–L15: exactly baseline (0.704).
- Intervention-fidelity checks confirm all interventions materially perturb representations (cosine distance 0.023–0.190).

**Finding 4 — Context-dependent attention–correlation relationship**:
| Context | Attention vs. Correlation | p |
|---|---|---|
| K562 CRISPRi (n=280) | Equal (0.704 vs. 0.703) | 0.73 |
| K562 CRISPRa (n=77) | Attention worse (0.55 vs. 0.65) | <10⁻⁶ |
| RPE1 CRISPRi (n=1,251) | Attention better (0.748 vs. 0.658) | <10⁻¹⁰ |
| iPSC neurons (n=7) | Trending attention better | 0.078 |
| T cells (n=7) | No difference | 0.81 |

→ But in *all* contexts, confound decomposition reveals the same pattern: gene-level features dominate, edges add nothing.

**Finding 5 — Attention-specific scaling failure + CSSI remedy**:
- Top-K F1 for attention-derived GRN recovery degrades with cell count (9/9 runs, sign test p = 0.002). Continuous AUROC improves (metric-dependent).
- Correlation edges are stable → degradation is attention-specific heterogeneity dilution.
- CSSI-max improves GRN recovery up to 1.85× (DLPFC brain data, optimal K = 5–7).
- Null tests with random strata confirm no false-positive inflation.

**Finding 6 — Expression residualisation asymmetry**:
- K562: Attention loses ~76% of TRRUST signal under residualisation (AUROC 0.66 → 0.54); correlation retains ~91% (0.63 → 0.62).
- RPE1: Attention loses ~88% (0.722 → 0.527); correlation *increases* (0.656 → 0.692, suppressor effect).
- → Attention-derived regulatory signal is substantially more expression-confounded than correlation.

**Finding 7 — Biological layer hierarchy** (real, but non-incremental):
- Early layers: PPI-enriched (STRING AUROC = 0.64 at L0; ρ = −0.61 with depth).
- Late layers: TF regulation-enriched (TRRUST AUROC = 0.75 at L15; ρ = +0.51 with depth).
- Anti-correlated layer profiles (ρ = −0.55, p = 0.019).
- Survives expression residualisation (97% signal retained) — but provides no incremental value for perturbation prediction.

## Reported Insights

- Attention in scFMs captures **co-expression**, not unique regulatory signal. Pretraining objectives reward co-expression patterns, not causal structure.
- Multi-model convergence (scGPT + Geneformer achieve similar near-random unstratified GRN recovery despite different architectures) → reflects optimisation landscape, not model-specific limitation.
- The attention-as-explanation debate from NLP (Jain & Wallace 2019, Serrano & Smith 2019) applies directly to biological FMs.
- Perturbation-predictive computation likely resides in the value/FFN pathway rather than learnable attention patterns — contrasts with NLP where specific heads encode syntactic/semantic functions.
- Raw performance comparisons between edge-scoring methods are misleading without confound controls.
- Recommendations: (i) apply trivial-baseline + incremental-value tests before claiming pairwise signal; (ii) report both thresholded and continuous metrics; (iii) use CSSI for heterogeneous populations; (iv) validate causal claims with ablation + fidelity diagnostics.

## References Worth Chasing

1. **scGPT** — Cui et al., 2024. Nature Methods. Gene-token transformer FM for scRNA-seq.
2. **Geneformer** — Theodoris et al., 2023. Nature. BERT-style rank-based FM for network biology.
3. **Replogle et al., 2022** — Genome-scale CRISPRi Perturb-seq (K562/RPE1, 2,024 genes). Primary perturbation dataset.
4. **Jain & Wallace, 2019** — Attention is not Explanation. NLP analog of this paper's findings.
5. **Serrano & Smith, 2019** — Is Attention Interpretable? Further NLP attention critique.
6. **Adamson et al., 2016** — CRISPRa perturbation dataset.
7. **Shifrut et al., 2018** — T-cell CRISPRi perturbation dataset.
8. **TRRUST** — Han et al., 2018. Nucleic Acids Research. Curated TF–target database used as GRN reference.
9. **DoRothEA** — Garcia-Alonso et al., 2019. Genome Research. TF regulon resource.
10. **STRING** — Szklarczyk et al., 2021. Nucleic Acids Research. PPI database used for layer-specific characterisation.
11. **scFoundation** (Hao et al., 2024) — Mentioned as untested architecture for future work.
12. **Pratapa et al., 2020** — GRN inference benchmarking framework (BEELINE).
13. **Conmy et al., 2023** — Automated circuit discovery in LLMs (NLP mech. interp. method applied here).

## Notes / Open Questions

- **This is an evaluation/benchmarking paper**, not a model paper. Its value is the reusable framework and the strong negative result about attention-based interpretability in scFMs.
- **Evidence quality rated high**: 37 analyses, 153 statistical tests with BH FDR correction (63/95 = 66% remain significant), 4 cell types, 2 perturbation modalities, 3 complementary causal ablation methods, extensive sensitivity analyses (27 parameter combinations). Convergent evidence across multiple independent test families.
- **Causal ablation limited to Geneformer**: scGPT's autoregressive architecture lacks a head-mask interface, so ablation results are single-architecture.
- **No decisive positive control**: No demonstration that the pipeline *can* recover known causal regulatory structure in a realistic perturbation setting. Authors argue no gold-standard exists at genome scale, and provide internal calibrations (wide dynamic range, asymmetric residualisation, per-TF bootstrap detecting 7/18 TFs with above-chance signal).
- **CSSI addresses recoverability, not predictive validity**: CSSI improves GRN recovery against curated references (TRRUST), but the gap between recoverability and perturbation-outcome predictive validity is unresolved.
- **Implications for the survey**: This paper is highly relevant as a methodological counterpoint to scFM papers claiming attention-derived regulatory networks. Any survey section on scFM interpretability should cite this framework. Also relevant to the broader question of what FMs actually learn vs. what correlational statistics already provide.
- **Interesting for future directions**: intervention-aware pretraining (on perturbation data), hybrid architectures (FM embeddings → GRN modules), CSSI + conformal prediction sets.
- **Complements GRNFormer (grnformer-a-biologically-guided-2025)**: GRNFormer injects external GRNs into scFMs; this paper shows the FMs themselves don't encode recoverable regulatory structure in attention, which motivates external GRN integration approaches like GRNFormer.
