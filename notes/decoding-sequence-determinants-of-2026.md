---
id: decoding-sequence-determinants-of-2026
title: Decoding sequence determinants of gene expression in diverse cellular and disease states
authors:
- Avantika Lal
- Alexander Karollus
- Laura Gunsalus
- David Garfield
- Surag Nair
- Alex M. Tseng
- M. Grace Gordon
- John D. Blischak
- Bryce Van de Geijn
- Tushar Bhangale
- Jenna L. Collier
- Nathaniel Diamant
- Tommaso Biancalani
- Hector Corrada Bravo
- Gabriele Scalia
- Gokcen Eraslan
year: 2026
venue: Nature Methods
arxiv: null
doi: 10.1038/s41592-026-03102-0
url: https://www.nature.com/articles/s41592-026-03102-0
pdf_path: null
md_path: null
modalities:
- dna
- epigenome
- scrna
status: extracted
evidence_quality: abstract+repo
tags:
- decima
- regulatory-genomics
- gene-expression-prediction
- single-cell-transcriptomics
- cell-type-conditioning
- disease-state-conditioning
- variant-effect-prediction
- regulatory-element-design
- borzoi-initialized
parameters: not disclosed; Borzoi-initialized backbone likely comparable to Borzoi-scale models
training_tokens: more than 22 million single-cell or single-nucleus RNA-seq profiles
training_compute: null
references_chased: false
added_at: '2026-05-27T09:34:12+00:00'
updated_at: '2026-05-27T09:34:12+00:00'
is_fm: true
fm_classification_reason: 'Decima: Borzoi-initialized sequence-to-expression foundation model trained on >22M single-cell/single-nucleus profiles for cell-type- and condition-specific regulatory prediction.'
---

## TL;DR

Decima extends sequence-to-expression modeling from bulk or assay-track prediction toward **cell type- and condition-specific expression prediction from DNA sequence**. The Nature Methods article was not directly reachable from this environment, so this note uses the linked bioRxiv preprint metadata and official Genentech code/repository. Accessible sources describe a model trained on more than 22 million single-cell or single-nucleus RNA-seq profiles that predicts expression for unseen genes from surrounding DNA sequence, supports cell-type/disease-state regulatory interpretation, scores non-coding variant effects at cellular resolution, and designs regulatory DNA elements with context-specific functions.

## Model

- **Name**: Decima.
- **Task**: predict cell type- and condition-specific gene expression from the DNA sequence around a gene.
- **Backbone**: official code defines `DecimaModel` as a Borzoi-style convolutional + transformer embedding initialized from Borzoi weights, with the output head replaced for Decima tasks.
- **Input representation**: one-hot DNA sequence plus an added gene-mask channel in the public model implementation.
- **Output**: task-specific expression predictions; the public Lightning wrapper applies an exponential activation and exposes variant-effect prediction by subtracting alternative-allele predictions from reference-allele predictions.
- **Weights/code**: trained model weights are advertised through Zenodo, and the official package is published as `decima`.

## Data

- **Training scale**: more than 22 million single-cell or single-nucleus RNA-seq profiles.
- **Biological scope**: multiple cell types, cellular states, tissues, and disease contexts.
- **Evaluation/use cases reported in accessible summaries**:
  - prediction of expression for unseen genes using DNA sequence,
  - discovery of cis-regulatory mechanisms for cell-type-specific expression,
  - cell-type-resolved non-coding variant-effect prediction,
  - design of regulatory elements with tuned context-specific activity.

## Training Recipe

- **Initialization**: public code initializes the embedding from Borzoi human checkpoints by default, making Decima a single-cell-conditioned continuation of the Enformer/Borzoi sequence-to-function lineage rather than a from-scratch DNA language model.
- **Loss family**: the public Lightning wrapper uses a task-wise Poisson-multinomial loss with a disease log-fold-change metric, consistent with count/profile prediction rather than masked-token pretraining.
- **Optimizer in public defaults**: Adam with learning rate `4e-5`, batch size `4`, mixed precision, and gradient accumulation support.
- **Compute budget**: not disclosed in the accessible sources used for this extraction.

## Key Ablations & Design Choices

Accessible sources did not expose a numeric ablation table, so the evidence below is qualitative and should not be counted as a Rev 4-style ablation update until the full manuscript is parsed.

| Design choice | Finding / rationale from accessible sources |
|---|---|
| Borzoi initialization | Decima reuses a long-context Borzoi-style sequence backbone and changes the head for single-cell expression tasks, suggesting that existing sequence-to-coverage models are useful initialization for cell-state-specific regulatory prediction. |
| Single-cell training targets | Training on >22M sc/snRNA-seq profiles moves sequence-to-expression prediction from bulk tracks toward cell-type and disease-state outputs. |
| Gene-mask channel | Public code adds a fifth input channel for a gene mask, making the target gene explicit inside the surrounding DNA context. |
| Cellular-condition resolution | Reported applications focus on cell-type-specific cis-regulatory interpretation and non-coding variant effects rather than average expression alone. |

## Reported Insights

- **Sequence-to-function models can become cellular-context models**: using large single-cell atlases as targets lets a DNA sequence model predict expression in specific cell types and disease states rather than only aggregate epigenomic/RNA-seq tracks.
- **Borzoi-style long-context backbones are reusable infrastructure**: Decima's public implementation starts from Borzoi weights and replaces the head, supporting the broader insight that regulatory genomics FMs can be adapted by changing conditioning/targets instead of rebuilding the sequence encoder.
- **Variant-effect prediction needs cellular resolution**: Decima is positioned to score non-coding variants in the cell types or disease contexts where regulatory effects matter.
- **Regulatory design becomes context-specific**: the reported design use case is not generic enhancer activity but DNA elements tuned for selected cellular contexts.

## References Worth Chasing

- Borzoi — direct architectural/initialization predecessor for sequence-to-RNA-coverage prediction.
- Enformer — earlier long-range sequence-to-expression transformer lineage.
- GET — complementary cell-type-conditioned regulatory model using accessibility/motif features rather than DNA-only sequence prediction.
- Large single-cell atlases used as training targets for cell-state- and disease-state-specific expression.

## Notes / Open Questions

- Direct Nature Methods access failed in this environment, and bioRxiv full text retrieval also failed; this note should be upgraded once the full article can be parsed.
- Exact architecture hyperparameters, task count, train/validation splits, numeric benchmark results, and controlled ablations are not recorded here unless visible in the public code or accessible abstracts.
- It remains important to compare Decima against Borzoi/Enformer/GET under matched cell-type and variant-effect benchmarks to separate gains from single-cell target scale versus architecture/initialization.

## Sources

- Nature Methods article: <https://www.nature.com/articles/s41592-026-03102-0>
- Open preprint: <https://www.biorxiv.org/content/10.1101/2024.10.09.617507v3>
- Official model repository: <https://github.com/Genentech/decima>
- Official applications repository: <https://github.com/Genentech/decima-applications>
- Model weights record: <https://zenodo.org/records/15092691>
