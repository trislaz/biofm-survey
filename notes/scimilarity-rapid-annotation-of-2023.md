---
id: scimilarity-rapid-annotation-of-2023
title: 'scimilarity: rapid annotation of cell types in human scRNA-seq via cell similarity'
authors: []
year: 2023
venue: null
arxiv: null
doi: 10.1101/2023.07.18.549537
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/scimilarity-rapid-annotation-of-2023.md
modalities:
- scrna
status: abstract-only
evidence_quality: abstract+metadata
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: Added in rev4 missing-FM brainstorm; canonical bio-FM.
---

## Ablations (Rev 4)

Source: Nature version (s41586-024-08411-y), Methods + Extended Data Fig. 2–4. The bioRxiv v1 preprint is Cloudflare-blocked; content drawn from the peer-reviewed equivalent describing the same ablation grid.

| # | Ablation | Variants tested | Metric(s) | Finding |
|---|----------|-----------------|-----------|---------|
| 1 | Loss-function grid (triplet vs MSE weight β, margin α) | 18 combinations of β ∈ {1.0…0.001} and α | Query Spearman ρ vs gene-signature score; integration ASW/NMI/ARI/graph connectivity | Lower β (more MSE) → better query; higher β (more triplet) → better integration. Selected β=0.001, α=0.05 as best joint operating point. |
| 2 | Pure triplet loss (β=1.0) | β=1.0 vs mixed | Query fidelity to subtle expression patterns | Pure triplet collapses within-type variance; MSE term required to preserve subtle cell-state differences. |
| 3 | SCimilarity vs other foundation models for query | scFoundation, scGPT | Spearman ρ to gene-signature retrieval score | SCimilarity ρ=0.77 vs scFoundation 0.54, scGPT 0.59; far fewer false-high cells. |
| 4 | SCimilarity vs dedicated integration methods | Harmony, scVI, scanorama, scArches on 2 kidney + 2 PBMC + 2 lung + all 15 held-out datasets | Cell-type ASW, batch ASW, NMI, ARI, graph connectivity | Higher cell-type ASW, comparable graph connectivity, less spurious cross-study mixing; SCimilarity does not see test data, baselines do. |
| 5 | Negative control: distinct populations from different studies | B cells vs Treg from two datasets | Cluster mixing | SCimilarity / Harmony / scArches keep them separate; scanorama and scVI incorrectly merge. |
| 6 | Single-cell vs single-nucleus generalization | Matched sc/sn on same human samples (Slyper 2020) | Pairwise embedding distance | nuc–cell only slightly larger than nuc–nuc and cell–cell. |
| 7 | Cross-platform generalization (trained 10x only) | 10x v2/v3, CEL-Seq2, Drop-Seq, Seq-well, SMART-Seq2, InDrops | Within-platform NN distance, annotation precision | All platforms embed effectively; Seq-well and SMART-Seq2 slightly worse; only rare cDCs/pDCs lose precision. |
| 8 | Annotation method comparison on healthy kidney | scANVI, CellTypist, TOSICA (each trained on the dataset) vs single pretrained SCimilarity | % match to author labels | SCimilarity 86.5% vs scANVI 85.2%, TOSICA 87.2%, CellTypist 90.4% — competitive without per-dataset training. |
| 9 | Outlier / confidence calibration | In-vivo holdout vs in-vitro and under-represented tissues (stomach, fetal gut, bladder) | % cells with SCimilarity score <50 | 79.5% in-vivo holdout cells confidently represented; 43.8% in-vitro flagged low-confidence (in-vitro absent from training), confirming score behaves as OOD detector. |

**Count: 9 ablations.**

**Top take-away:** the β (triplet vs MSE) sweep is the central design ablation — query and integration objectives are antagonistic, and a strongly MSE-weighted hybrid (β=0.001) is what lets a single pretrained model beat both other scRNA foundation models on query fidelity (ρ 0.77 vs 0.54–0.59) and dedicated integration tools on cell-type coherence, without fine-tuning.
