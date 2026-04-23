---
id: aido-accurate-model-of-2024
title: 'AIDO: Accurate model of biology through a foundation model of DNA, RNA and
  protein'
authors: []
year: 2024
venue: null
arxiv: null
doi: 10.1101/2024.12.02.626322
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/aido-accurate-model-of-2024.md
modalities:
- multimodal
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

Ablation evidence is not in the umbrella AIDO bioRxiv (10.1101/2024.12.02.626322), which is a system overview. The substantive ablations live in the per-module preprints (AIDO.Protein, AIDO.Cell) and the GenBio AIDO PDF. Summarised below.

| # | Module | Ablation axis | Compared variants | Reported effect | Source |
|---|--------|---------------|-------------------|-----------------|--------|
| 1 | AIDO.Protein-16B | FFN block: dense vs sparse MoE | Dense 16B FFN vs MoE (8 experts, top-2) | MoE matches/beats dense at ~28% active params (~4.5B/16B); enables 16B scale at roughly half the per-token FLOPs | AIDO.Protein arXiv / OpenReview |
| 2 | AIDO.Protein-16B | Number of experts / top-k routing | Varying experts and top-k around the 8/top-2 Mixtral-style choice | 8 experts, top-2 best trade-off between specialisation and compute; experts visibly specialise on distinct sequence motifs | AIDO.Protein arXiv |
| 3 | AIDO.Protein-16B | Pretraining data: UniRef90 only vs UniRef90+ColabFoldDB then UR90 fine-tune | Single-corpus vs 1.2T-AA mixed pretraining + 100B-AA UR90 refinement | Mixed pretraining + UR90 refinement gives best ProteinGym DMS / structure-conditioned generation; near MSA-based SOTA without alignments | AIDO.Protein arXiv |
| 4 | AIDO.Cell (3M→650M→100M public) | Read-Depth-Aware (RDA) objective | Standard masked expression vs RDA (downsample reads, predict full-depth) | RDA improves zero-shot clustering, perturbation prediction and robustness across tissues; removing RDA degrades generalisation | AIDO.Cell bioRxiv 10.1101/2024.11.28.625303 |
| 5 | AIDO.Cell | Model scale | 3M / 10M / 100M / 650M dense BERT-style encoders, full transcriptome context | Monotonic improvement with scale on cell-type / perturbation benchmarks; transcriptome-scale context (no HVG selection) needed to realise gains | AIDO.Cell bioRxiv |
| 6 | AIDO.Cell | Expression encoding | Continuous regression vs auto-discretised tokens | Auto-discretisation of continuous counts outperforms naive continuous targets and enables MLM-style training | AIDO.Cell bioRxiv |
| 7 | AIDO system | Module composition | Single-modality FM vs connected multi-module AIDO stack (DNA/RNA/Protein/Structure/Cell) | Hierarchical representation passing across modules is the system's design claim; quantitative cross-module ablations not yet reported in v1 preprint | AIDO umbrella bioRxiv 10.1101/2024.12.02.626322 |

Notes: Rows 1–3 are extracted from the AIDO.Protein paper and HF model card; rows 4–6 from the AIDO.Cell paper; row 7 flags a gap in the umbrella paper. OpenAlex abstract for this DOI is mismatched (returns an unrelated 11βHSD1 cardiology paper), so module-level preprints are the authoritative source for ablations.
