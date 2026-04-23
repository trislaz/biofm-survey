---
id: msa-transformer-2021
title: MSA Transformer
authors:
- Roshan M. Rao
- Jason Liu
- Robert Verkuil
- Joshua Meier
- John Canny
- Pieter Abbeel
- Tom Sercu
- Alexander Rives
year: 2021
venue: ICML 2021
arxiv: null  # bioRxiv only; no arxiv ID
doi: 10.1101/2021.02.12.430858
url: https://proceedings.mlr.press/v139/rao21a.html
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/msa-transformer-2021.md
modalities:
- protein-sequence
- protein-structure
parameters: 100M
training_tokens: null  # not explicitly reported; trained on ~26M MSAs from UniRef50
training_compute: ~21500 V100 GPU-hours  # 128 V100 GPUs × 7 days
tags:
- MSA
- axial-attention
- tied-row-attention
- contact-prediction
- masked-language-model
- protein-language-model
- unsupervised-structure-learning
status: extracted
evidence_quality: abstract+repo
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

MSA Transformer is a 100M-parameter protein language model that operates on multiple sequence alignments (MSAs) rather than single sequences. It interleaves row attention (across positions within each sequence) and column attention (across sequences at each position) in an axial-attention design, trained with masked language modelling on ~26M UniRef50 MSAs. Its unsupervised contact predictions (from attention maps alone) surpass Potts/GREMLIN by ~15 pp in top-L long-range precision and approach supervised methods like trRosetta, with far greater parameter efficiency than single-sequence models (ESM-1b: 650M params achieves lower contact precision).

## Model

- **Architecture**: Transformer with axial (factored) attention; each of 12 blocks contains a row-attention layer and a column-attention layer.
- **Row attention**: Self-attention across residue positions within each sequence. Uses **tied row attention**: a single attention map is shared across all MSA rows, enforcing a consistent contact structure across the alignment and improving generalisation.
- **Column attention**: Self-attention across sequences at each aligned position; captures evolutionary covariation signals (analogous to what Potts models fit per-family).
- **Embedding dimension**: 768.
- **Parameters**: ~100M (12 layers × row+column attention + FFN).
- **Positional encoding**: Learnable positional embeddings encoding both sequence position and MSA row index.
- **Contact prediction**: Derived from a simple linear combination of attention heads (no supervised head); symmetrised row-attention maps yield residue-residue contact probabilities.
- **Released checkpoints**: ESM-MSA-1 (original, has a bug in positional embeddings) and **ESM-MSA-1b** (fixed; recommended). Same architecture, retrained.
- **Code**: `esm.pretrained.esm_msa1b_t12_100M_UR50S()` via `pip install fair-esm` ([github.com/facebookresearch/esm](https://github.com/facebookresearch/esm)).

## Data

- **Pre-training corpus**: Multiple sequence alignments constructed from **UniRef50** clusters using HHblits.
- **Number of MSAs**: ~26 million alignments.
- **Average MSA depth**: ~1,192 sequences per alignment (before subsampling).
- **Training subsampling**: Each MSA is randomly subsampled to **128 sequences** per batch element during training.
- **Sequence length**: Cropped/padded to **512 residues** (columns).
- **Vocabulary**: 33 tokens (20 standard amino acids + gap + special tokens).

## Training Recipe

- **Objective**: Masked language modelling (MLM)—~15% of amino acid tokens in randomly selected MSA rows are masked; the model predicts their identity using both within-sequence and cross-sequence context.
- **Hardware**: 128 NVIDIA V100 GPUs.
- **Training duration**: ~7 days (~21,500 V100 GPU-hours).
- **Optimiser / schedule**: Not fully detailed in the published paper; follows standard BERT-style MLM training conventions.
- **MSA sampling strategy**: At each training step, a random subset of 128 rows is drawn from the full MSA for each family, providing regularisation and diversity.

## Key Ablations & Design Choices

| Design choice | Result |
|---|---|
| **Tied vs untied row attention** | Tied row attention outperforms untied on contact prediction; sharing the attention map across MSA rows enforces a globally consistent contact structure and reduces overfitting |
| **Axial (row+column) vs full 2D attention** | Full attention has O(M²L²) cost and is computationally infeasible for typical MSA sizes; axial reduces to O(ML²) + O(LM²) with comparable or better performance |
| **Row-only or column-only attention** | Both are necessary; removing either degrades contact prediction substantially |
| **MSA depth subsampling (128 vs deeper)** | Model is robust to reduced MSA depth; performance degrades gracefully with fewer sequences, outperforming Potts models especially on shallow alignments |
| **MSA Transformer (100M) vs ESM-1b (650M)** | MSA Transformer achieves higher contact precision with 6.5× fewer parameters by leveraging MSA co-evolution directly |
| **Unsupervised vs supervised contact** | Unsupervised MSA Transformer approaches trRosetta (supervised, 36–61 residual blocks) without using any structural labels |

## Reported Insights

- A single model trained across protein families transfers co-evolutionary reasoning that Potts/GREMLIN must re-learn per family, yielding large gains on shallow MSAs where per-family statistical power is low.
- Tied row attention is the key architectural choice for contact prediction—it constrains the model to learn a single contact structure shared across all alignment rows.
- Attention-head contact maps are interpretable: specific heads specialise for short-, medium-, and long-range contacts.
- The model is far more parameter-efficient than single-sequence language models for structure-related tasks because MSA input provides direct evolutionary signal.
- Column attention enables the model to learn amino-acid substitution patterns and conservation directly from the alignment, complementing the structural signal from row attention.
- Top-L long-range contact precision: **57.4%** (ESM-MSA-1b, "Large valid" set), vs 41.1% for ESM-1b (single-sequence) and ~42% for Potts/GREMLIN.

## References Worth Chasing

1. **Rives et al. (2021)** – ESM-1b; single-sequence protein language model at 650M params (PNAS 118(15)).
2. **Rao et al. (2020)** – "Transformer protein language models are unsupervised structure learners"; self-attention contact maps (bioRxiv 2020.12.15.422761).
3. **Jumper et al. (2021)** – AlphaFold2; end-to-end structure prediction using MSA + pair representations (Nature 596).
4. **Baek et al. (2021)** – RoseTTAFold; three-track network for structure prediction (Science 373).
5. **Ekeberg et al. (2013)** – GREMLIN / Potts models for direct coupling analysis from MSAs.
6. **Yang et al. (2020)** – trRosetta; supervised contact/distance prediction from MSAs.
7. **Ho et al. (2019)** – Axial attention / axial-transformer; factored attention for images that inspired the MSA architecture.
8. **Lin et al. (2023)** – ESM-2 & ESMFold; successor single-sequence models that match MSA-based accuracy without alignment (Science 379).
9. **Meier et al. (2021)** – ESM-1v; variant-effect prediction from ESM-1b architecture on UniRef90.

## Notes / Open Questions

- **Evidence quality**: abstract + GitHub repo + ICML proceedings metadata. Full PDF not ingested; exact training hyperparameters (LR, warmup, batch size) need verification from the paper or supplementary.
- The bioRxiv DOI (10.1101/2021.02.12.430858) covers both v1 (Feb 2021) and the ICML camera-ready (v2, Jun 2021). No separate arXiv ID exists for this paper.
- ESM-MSA-1 had a positional-embedding bug; ESM-MSA-1b is the corrected release (Jul 2021). All reported numbers should use ESM-MSA-1b.
- Training-token count is not directly reported; it could be estimated from ~26M MSAs × 128 sampled rows × 512 positions × num_epochs, but epoch count is unspecified.
- The ~21,500 GPU-hour figure comes from secondary sources and should be verified against the paper's appendix.
- How does MSA Transformer compare to AlphaFold2's Evoformer, which also uses axial attention on MSAs but with additional pair representations and recycling?
- Scaling behaviour is unexplored—would a larger MSA Transformer (e.g., 650M params) further improve over ESM-1b, or are returns diminishing once MSA signal is captured?
- ESM-2/ESMFold (Lin et al., 2023) later showed that sufficiently large single-sequence models can match MSA-based accuracy—does this obsolete the MSA Transformer approach, or do MSAs remain valuable for specific tasks (e.g., variant-effect prediction, shallow families)?
