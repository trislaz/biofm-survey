---
id: a-phylogenetic-approach-to-2025
title: A Phylogenetic Approach to Genomic Language Modeling
authors:
- Carlos Albors
- Jianan Canal Li
- Gonzalo Benegas
- Chengzhong Ye
- Yun S. Song
year: 2025
venue: null
arxiv: '2503.03773'
doi: null
url: https://arxiv.org/abs/2503.03773v2
pdf_path: papers/a-phylogenetic-approach-to-2025.pdf
md_path: papers/md/a-phylogenetic-approach-to-2025.md
modalities:
- dna
- multispecies-alignment
status: extracted
evidence_quality: full-text
tags:
- genomic-language-model
- phylogenetics
- variant-effect-prediction
- convolutional
- reverse-complement-equivariant
- transfer-learning
parameters: 83000000
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:46+00:00'
updated_at: '2026-04-22T20:17:15+00:00'
---

## TL;DR

PhyloGPN is an 83 M-parameter CNN (adapted from ByteNet/CARP) that models nucleotide evolution on phylogenetic trees using 447-species mammalian whole-genome alignments during training, but requires only a single human DNA sequence at inference. A novel F81-phylogenetic loss replaces standard masked-LM. It matches GPN-MSA on ClinVar pathogenic-vs-benign (AUROC 0.96) while vastly outperforming all other gLMs (Nucleotide Transformer 0.61, Caduceus 0.64, HyenaDNA 0.49). On BEND Disease VEP it achieves 0.98 AUROC (+0.21 over next-best). It wins 5/7 BEND tasks among gLMs.

## Model

- **Name:** PhyloGPN (Phylogenetics-based Genomic Pre-trained Network)
- **Architecture:** 40-block ByteNet-style CNN adapted from CARP, with reverse-complement equivariant (RCE) convolutions; no padding in conv layers so each layer reduces length by kernel-size − 1.
- **Parameters:** ~83 M (free parameters are half the weights+biases due to RCE parametrization, plus layer-norm params).
- **Receptive field:** 481 bp; expanded variant PhyloGPN-X pools embeddings over 5,521 positions → effective receptive field of 6,001 bp using a fixed random projection matrix.
- **Embedding dim:** 960.
- **Output:** Per-position F81 nucleotide substitution model parameters (θ_A, θ_C, θ_G, θ_T).

## Data

- **Training sequences:** Human reference genome GRCh38 (autosomal + X + Y chromosomes, primary assembly only).
- **Alignment:** Zoonomia Consortium whole-genome alignment of 447 placental mammalian species (241 original + additional primates).
- **Items:** Each training item is a 481 bp window from human centered at position i, plus aligned nucleotides y^(i) from other species + the corresponding subtree T^(i).
- **Batching:** 12 MSAs (~10 kb each, merged from contiguous alignment blocks) per batch. Autosomal positions sampled 4×, X chromosome 3×, Y chromosome 1× per epoch to equalize male/female genotype weight.

## Training Recipe

- **Loss:** Phylogenetic F81 log-likelihood of aligned nucleotides conditioned on the reference nucleotide state (Eq. 4), stabilised via a sigmoid lower-bound on transition probabilities to avoid double-exponential overflow (Eq. 5).
- **Optimizer:** AdamW, fixed learning rate 1 × 10⁻⁵, no weight decay, PyTorch defaults for other params.
- **Hardware:** 4 × NVIDIA A100 GPUs.
- **Duration:** 18 epochs.
- **No curriculum, no masking, no dropout mentioned.**

## Key Ablations & Design Choices

- **Generalization ablation (§4.3, Fig. 6, Table S2):** Model trained only on odd chromosomes + X for 2 epochs vs. epoch-1 full checkpoint evaluated on even chromosomes + Y. Ablated model performs comparably (overall ClinVar AUROC 0.87 vs. 0.85), demonstrating PhyloGPN generalises to unseen genomic regions rather than memorising.
- **PhyloGPN vs. PhyloGPN-X (Table 2):** Expanding receptive field to 6,001 bp improves Gene Finding MCC 0.43 → 0.69 but degrades Enhancer Annotation AUPRC 0.04 → 0.01 (under-powered BEND classifier with hidden-size 2; expanding to 32 recovers 0.03).
- **ClinVar pathogenic vs. benign (Fig. 3a, Table 1):** PhyloGPN AUROC 0.96, matching GPN-MSA 0.96; Caduceus 0.64, NT 0.61, HyenaDNA 0.49.
- **OMIM regulatory variants (Fig. 3b):** PhyloGPN outperforms all single-sequence baselines at every MAF threshold but GPN-MSA still leads by a wide margin.
- **DMS ranking (Fig. 4, Table S1):** PhyloGPN best among single-sequence gLMs on 24/25 proteins (Spearman up to 0.50); GPN-MSA often better.
- **BEND Disease VEP:** PhyloGPN AUROC 0.98 vs. Nucleotide Transformer 0.77 (+0.21).
- **BEND Chromatin Accessibility:** PhyloGPN 0.86 AUROC, surpassing all gLMs and Expert Method (Basset 0.85).
- **Expression VEP weakness:** PhyloGPN embedding cosine-distance AUROC only 0.46, but LLR-based evaluation gives 0.53 (vs. NT's 0.36), suggesting the limitation is in the cosine-distance metric, not the representation.
- **Conditioning on reference nucleotide (Eq. 4):** Required to avoid model over-weighting the center nucleotide (which appears in both x and y).
- **Stable upper-bound loss (Eq. 5):** Sigmoid lower-bound on α(t) avoids numerical overflow from double exponential in F81 transition probability.

## Reported Insights

- Standard gLMs (masked-LM on genomes) are far weaker than protein LMs at identifying deleterious variants; the phylogenetic loss closes this gap.
- Explicitly modelling phylogenetic correlations lets the model use closely-related primate genomes (excluded by GPN-MSA) without learning to simply copy aligned nucleotides.
- Alignment data used only at training time → model generalises to any species or poorly-aligned regions at inference.
- Larger whole-genome alignments (more distantly-related vertebrates) are expected to improve coding-variant prediction where GPN-MSA currently leads.
- More expressive substitution models (e.g., GTR) and gene-tree-aware training could further improve performance.

## References Worth Chasing

- **Benegas et al. 2025 (ref 1):** GPN-MSA — the MSA-based gLM that PhyloGPN aims to match/surpass; Nature Biotechnology.
- **Benegas et al. 2025 (ref 2):** Benchmarking DNA sequence models for causal regulatory variant prediction — follow-up work from same lab.
- **Benegas, Ye, Albors et al. 2025 (ref 3):** Survey "Genomic language models: opportunities and challenges" — Trends in Genetics.
- **Yang et al. / CARP (ref 41):** Convolutional architecture ancestor (protein LM from which PhyloGPN is adapted).
- **Marin et al. 2024 / BEND (ref 22):** The benchmark suite used for embedding evaluation (ICLR 2024).
- **Zoonomia Consortium alignment (ref 44 + ref 20):** 241-mammal + primate extension to 447 species; the key data resource.

## Notes / Open Questions

- Training tokens / FLOPs not reported; 18 epochs over ~3 billion human-genome positions × 481 bp windows is the approximate scale, but exact token count is unclear for a CNN sliding-window setup.
- No comparison to Evo, Enformer, or newer SSM-based genomic models.
- PhyloGPN-X's random-projection pooling (Eq. 6) is ad-hoc; learned pooling or attention might improve.
- Only mammalian alignment used; the paper notes that adding vertebrate genomes (as GPN-MSA does) could close the remaining gap on coding variants.
- Enhancer Annotation task result (AUPRC 0.04) may be dominated by the weak BEND classifier rather than representation quality.
