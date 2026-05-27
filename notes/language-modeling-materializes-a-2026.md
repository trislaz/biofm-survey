---
id: language-modeling-materializes-a-2026
title: Language Modeling Materializes a World Model of Protein Biology
authors: []
year: 2026
venue: Biohub preprint
arxiv: null
doi: null
url: https://biohub.ai/papers/esm_protein.pdf?__clerk_synced=true
pdf_path: null
md_path: null
modalities:
- protein-sequence
- protein-structure
- dna
- small-molecule
- multimodal
status: extracted
evidence_quality: abstract+repo
tags:
- protein-language-model
- ESMC
- ESMFold2
- protein-structure
- sparse-autoencoders
- atlas
- inverse-folding
parameters: ESMC 300M/600M/6B; ESMFold2 built on ESMC 6B
training_tokens: ESMC 6B reported at 6.2T tokens
training_compute: null
references_chased: false
added_at: '2026-05-27T15:49:29+00:00'
updated_at: '2026-05-27T15:49:29+00:00'
---

## TL;DR

This Biohub preprint introduces a successor stack to the ESM-2/ESM-3 line: **ESMC**, a scaled sequence-only protein language model; **ESMFold2**, a diffusion-based structure predictor and inverse-folding/design system built on ESMC representations; and an expanded **ESM Atlas** with billions of proteins and more than a billion predicted structures. The central claim is that large protein language models materialize a useful "world model" of protein biology: sequence-only pretraining yields representations that support structure prediction, inverse design, sparse-autoencoder interpretation, and atlas-scale annotation. It is distinct from the earlier ESM-3 paper ("Simulating 500 million years of evolution...") despite sharing the ESM lineage.

## Model

- **ESMC family**: Sequence-only Transformer protein language models at roughly 300M, 600M, and 6B parameters.
- **ESMFold2**: Structure-prediction and design model that conditions on ESMC 6B representations and uses a diffusion-style structure generation/prediction head.
- **Inputs beyond proteins**: ESMFold2 extends the folding/design setting to biomolecular complexes, including protein, DNA (including modifications), and ligand / CCD-code conditioning.
- **ESM Atlas**: Atlas-scale deployment of ESMC/ESMFold2 over billions of proteins, with more than one billion predicted structures reported for the 2026 release.
- **Interpretability layer**: Sparse autoencoders trained on ESMC 6B internal activations expose thousands of human-annotated features for motifs, folds, localization signals, domains, and functional signatures.

## Data

- **Pretraining data**: Protein sequence corpora at metagenomic scale, continuing the UniRef/MGnify-heavy ESM recipe.
- **Training scale**: ESMC 6B is reported with **6.2 trillion protein tokens**.
- **Atlas scale**: ESM Atlas is expanded to roughly **6.8B proteins**, with **>1B** ESMFold2-predicted structures.
- **Structure/design data**: ESMFold2 uses protein structure supervision and supports complex conditioning over proteins, DNA, and ligands.

## Training Recipe

- **ESMC objective**: Sequence-only protein language modeling, optimized for representations that scale with data and parameter count.
- **ESMC curriculum**: The public ESM3/ESMC documentation describes the 6B sequence model using a two-stage context-length/data-mix curriculum: a short-context, metagenomic-heavy warmup followed by a longer-context stage.
- **ESMFold2 objective**: Diffusion-style structure prediction/generation conditioned on ESMC representations and optional biomolecular context.
- **Interpretability**: Sparse autoencoders are trained post hoc on ESMC 6B activations rather than as part of the base model objective.

## Key Ablations & Design Choices

| # | Axis varied | Setting | Finding | Take-away |
|---|---|---|---|---|
| 1 | ESMC scale | 300M vs 600M vs 6B | Contact/structure-relevant representations continue improving through 6B; the 6B model exceeds earlier ESM-2 baselines on reported contact metrics. | Sequence-only protein scaling remains unsaturated. |
| 2 | Folding architecture | ESMFold / ESMFold2-style structure module vs diffusion-based ESMFold2 | The new diffusion head is positioned as better suited for structure prediction and inversion/design than the original ESMFold module. | ESMC supplies the representation; the generative head determines whether it is usable for design. |
| 3 | Context/data curriculum | Short-context metagenomic-heavy warmup followed by longer-context training | The curriculum is used to make trillion-token training practical before the expensive long-context phase. | Context length is a compute allocation choice, not only a modeling choice. |
| 4 | Representation analysis | Raw activations vs sparse-autoencoder features | SAE features are interpretable as domains, motifs, localization, fold/function concepts, and other biological signatures. | Mechanistic tools can turn opaque PLM activations into surveyable biological concepts. |
| 5 | Atlas deployment | Sequence embeddings only vs structure prediction at atlas scale | ESMFold2 enables a structure-first view over more than a billion predicted proteins. | Foundation models become biological infrastructure when paired with atlas-scale inference. |
| 6 | Inverse design validation | ESMFold2 inversion for therapeutic-target minibinders | Reported wet-lab validation includes de novo minibinders with nanomolar affinities for multiple targets. | The stack moves beyond representation learning into experimentally testable design. |

**Count:** 6 ablation/design rows.

## Reported Insights

- **Protein sequence LMs still scale**: ESMC indicates that protein sequence-only scaling remains productive beyond ESM-2, even before adding structure/function tracks as in ESM-3.
- **Structure prediction and design are now coupled**: ESMFold2 is not only a predictor but also supports inverse folding/design workflows, making the representation-action loop tighter than in ESM-2/ESMFold.
- **World-model framing**: The paper argues that ESMC internal states encode reusable biological abstractions, evidenced by structure prediction, atlas search, design, and sparse-autoencoder features.
- **Interpretability becomes practical at model scale**: SAE features give a path to inspect large PLMs for human-recognizable protein biology rather than only benchmarking downstream accuracy.
- **Atlas-scale inference changes the utility curve**: The value of a foundation model is amplified by embedding and folding billions of proteins, not just by per-protein accuracy.

## References Worth Chasing

1. **Rives et al. 2021** — "Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250M Protein Sequences" (PNAS; doi:10.1073/pnas.2016239118). ESM-1b predecessor.
2. **Lin et al. 2023** — "Evolutionary-scale prediction of atomic-level protein structure with a language model" (Science; doi:10.1126/science.ade2574). ESM-2/ESMFold baseline and direct predecessor.
3. **Hayes et al. 2025** — "Simulating 500 million years of evolution with a language model" (Science; doi:10.1126/science.ads0018). ESM-3 multimodal sequence/structure/function model; distinct from the Biohub PDF URL in this issue.
4. **Hsu et al. 2022** — "Learning inverse folding from millions of predicted structures" (ICML / bioRxiv 2022.04.10.487779). ESM-IF1 inverse-folding predecessor.
5. **Dauparas et al. 2022** — "Robust deep learning-based protein sequence design using ProteinMPNN" (Science; doi:10.1126/science.add2187). Strong inverse-folding/design baseline.
6. **van Kempen et al. 2023** — "Fast and accurate protein structure search with Foldseek" (Nature Biotechnology). Relevant to atlas-scale structure search.

## Notes / Open Questions

- **Author list and DOI**: The issue URL points directly to the Biohub-hosted PDF; the complete citable metadata was not available through the accessible web endpoints during this update, so authors and DOI are left unset rather than guessed.
- **Relationship to ESM-3**: The filename `esm_protein.pdf` is easy to confuse with ESM-3. The current Biohub PDF is the later ESMC/ESMFold2/Atlas paper, while ESM-3 is already represented in `notes/simulating-500-million-years-2024.md`.
- **Public checkpoint coverage**: Public ESM releases may not include every production model described in the paper; verify which ESMC/ESMFold2 weights are open before treating the stack as fully reproducible.
- **Compute disclosure**: The 6.2T-token scale is documented, but exact FLOPs and training hardware for every ESMC/ESMFold2 component should be verified against the final citable manuscript.
