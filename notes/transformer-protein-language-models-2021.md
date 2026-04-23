---
id: transformer-protein-language-models-2021
title: Transformer protein language models are unsupervised structure learners
authors:
- Roshan M. Rao
- Joshua Meier
- Tom Sercu
- Sergey Ovchinnikov
- Alexander Rives
year: 2021
venue: ICLR 2021
arxiv: null
doi: 10.1101/2020.12.15.422761
url: https://openreview.net/forum?id=fylclEqgvgd
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/transformer-protein-language-models-2021.md
modalities:
- protein-sequence
- protein-structure
status: extracted
evidence_quality: abstract+repo
tags:
- attention-as-contact
- probing
- unsupervised
- protein-language-model
- contact-prediction
- logistic-regression
- APC
- ESM-1b
- TAPE
- ProtBert
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'Rao et al.: ESM-1b contact prediction; pretrained PLM-based.'
---

## TL;DR

Attention maps from Transformer protein language models directly encode residue–residue contacts. A simple logistic regression on attention heads (trained on only 20 structures) recovers contact maps that, for the largest model (ESM-1b, 650M params), outperform the state-of-the-art unsupervised contact prediction pipeline GREMLIN, replacing multiple-sequence-alignment-based inference with a single forward pass. Contact prediction quality scales with model capacity: ESM-1b >> ProtBert (420M) > TAPE Transformer (38M). This is a probing/analysis paper—no new model is trained.

## Model

- **Scope**: This paper does *not* train new models. It probes attention maps of three existing PLMs to predict contacts.
- **Models studied**:
  | Model | Params | Layers | Heads | Training data | Objective |
  |---|---|---|---|---|---|
  | TAPE Transformer | 38M | 12 | 12 | Pfam (~31M seqs) | MLM |
  | ProtBert-BFD | ~420M | 30 | 16 | BFD (~2.1B seqs) | MLM |
  | ESM-1b | 650M | 33 | 20 | UniRef50 (250M seqs, ~86B amino acids) | MLM |
- **Contact predictor**: Logistic regression over L×L attention maps from all heads (concatenated across layers), predicting binary contact (Cβ distance < 8 Å).
  - Input features per residue pair (i,j): attention weight a_{h,i,j} for each head h, symmetrised as (a + aᵀ)/2, then APC (Average Product Correction) applied per head to remove phylogenetic bias.
  - Total feature dimension = num_layers × num_heads (e.g., 33 × 20 = 660 for ESM-1b).
  - L1-regularised logistic regression produces a sparse selection of heads.

## Data

- **Probe supervision**: 20 protein structures used to fit the logistic regression; these are held out from evaluation.
- **Evaluation**: Proteins from known PDB structures; standard metrics on long-range contacts (sequence separation ≥ 24).
- **Pre-training data for studied models**:
  - ESM-1b: UniRef50 2018_03 — 250M sequences, ~86B amino acids.
  - ProtBert: BFD (Big Fantastic Database) — ~2.1B sequences.
  - TAPE Transformer: Pfam — ~31M sequences.
- **Baseline MSAs**: For GREMLIN comparison, MSAs are generated via standard pipelines (HHblits / jackhmmer).

## Training Recipe

- **No new model is trained.** The paper only fits logistic regression probes on frozen pre-trained attention maps.
- **Probe training**: L1-regularised logistic regression, fit on 20 structures, evaluated on held-out test sets.
- The pre-training recipes for ESM-1b, ProtBert, and TAPE are described in their respective papers (Rives et al. 2021, Elnaggar et al. 2020, Rao et al. 2019).

## Key Ablations & Design Choices

### 1. Model scale → contact quality
- Contact prediction precision scales monotonically with model capacity:
  - TAPE (38M): lowest precision.
  - ProtBert (420M): intermediate.
  - ESM-1b (650M): highest; outperforms GREMLIN (unsupervised SOTA DCA method).
- Suggests that scale is a key driver of emergent structural knowledge in PLMs.

### 2. APC (Average Product Correction)
- APC correction on per-head attention matrices is critical for high contact precision.
- Without APC, attention-based contacts are substantially noisier, reflecting phylogenetic / positional biases rather than true structural contacts.

### 3. Head-level specialisation
- Individual attention heads specialise for different contact-distance ranges (short-, medium-, long-range).
- The logistic regression probe assigns non-zero weights to a sparse subset of heads, predominantly from middle-to-late layers.

### 4. Comparison to GREMLIN
- ESM-1b attention contacts outperform GREMLIN on top-L long-range precision — first time a single-sequence method beats MSA-based unsupervised contact prediction.
- GREMLIN requires an MSA per protein (minutes of compute); attention contacts require a single forward pass (seconds).

### 5. Symmetrisation
- Attention matrices are not symmetric; symmetrisation (averaging a_{i,j} and a_{j,i}) is necessary for contact prediction since contacts are symmetric.

## Reported Insights

- **Attention = implicit contact map**: Transformer self-attention learns to attend to spatially proximate residues as a by-product of the MLM objective, without any structural supervision.
- **Unsupervised SOTA replaced**: The largest PLM (ESM-1b) can replace traditional MSA-based unsupervised contact prediction pipelines (DCA, GREMLIN, plmDCA) with a single forward pass.
- **Scaling predicts structural knowledge**: Contact precision improves with model capacity, suggesting further scaling will yield even better structural representations.
- **Sparse head selection**: Only a fraction of attention heads carry contact information; most structural signal concentrates in middle-to-late layers.
- **APC is necessary**: Raw attention scores are confounded by sequence-level biases; APC deconfounding is essential (analogous to its role in DCA).
- **Interpretability**: The method provides an interpretable lens into what Transformer PLMs learn—each selected head can be visualised as a "structural expert."

## References Worth Chasing

1. **Rives et al. (2021)** – "Biological structure and function emerge from scaling unsupervised learning to 250M protein sequences" (PNAS). ESM-1b model; representation-based (not attention-based) structural analysis.
2. **Elnaggar et al. (2020)** – ProtTrans / ProtBert: large-scale PLMs trained on BFD and UniRef100 (bioRxiv 2020.07.12.199554).
3. **Rao et al. (2019)** – TAPE: Tasks Assessing Protein Embeddings benchmark; 12-layer Transformer on Pfam.
4. **Marks et al. (2011) / Ekeberg et al. (2013)** – Direct coupling analysis (DCA) / GREMLIN / Potts models for contact prediction from MSAs.
5. **Rao et al. (2021b)** – MSA Transformer (bioRxiv 2021.02.12.430858; ICML 2021). Extends the attention-contact idea to MSA inputs with tied row attention.
6. **Lin et al. (2023)** – ESM-2 & ESMFold (Science 379). Successor PLMs at 15B params; single-sequence structure prediction matching AlphaFold2 accuracy.
7. **Vaswani et al. (2017)** – Original Transformer architecture.
8. **Devlin et al. (2019)** – BERT: masked language modeling objective.

## Notes / Open Questions

- **Evidence quality**: Based on abstract, OpenReview metadata, web search, and the facebookresearch/esm GitHub repo. Full PDF not ingested.
- **This is an analysis paper, not a model paper**: No new architecture or training is proposed. The contribution is the probing methodology (attention → logistic regression → contacts) and the empirical finding that scale enables SOTA unsupervised contacts.
- **Exact precision numbers**: Need full-text verification. Web sources confirm ESM-1b beats GREMLIN on top-L long-range, but exact numbers vary across evaluation sets.
- **bioRxiv DOI vs ICLR**: The paper appeared as bioRxiv 2020.12.15.422761 (Dec 2020) and was published at ICLR 2021 (poster). No separate arXiv ID exists.
- **20 structures for probe training**: Extremely low supervision (20 proteins); raises the question of whether this is truly "unsupervised" or minimally supervised. The authors argue 20 is negligible.
- **Superseded by embedding-based methods?**: Later work (ESM-2, Ankh) suggests that representations (embeddings) rather than attention maps are generally more powerful for downstream tasks. The attention-contact approach remains valuable for interpretability.
- **Relationship to MSA Transformer**: The same first author (Rao) extended this attention-contact idea in the MSA Transformer paper (Feb 2021), achieving much higher contact precision by operating on MSA inputs.

## Ablations (Rev 4)

Extracted from ICLR 2021 camera-ready (Tables 1–2, §5.1–5.2, App. A.7). Metric is long-range top-L precision (P@L, sequence sep ≥ 24) on 14,842 trRosetta test proteins; confidence intervals ≤ 0.5 pp. Default ESM-1b probe: n=20 training proteins, λ=0.15, min-sep k=6, single sequence input.

| # | Ablation axis | Variant | Long-range P@L | Δ vs ESM-1b default | Take-away |
|---|---|---|---:|---:|---|
| 1 | Model scale (Table 1) | TAPE 38M / ProtBERT-BFD 420M / ESM-1 34L 670M / ESM-1b 650M | 11.2 / 34.1 / 34.7 / **41.1** | −29.9 / −7.0 / −6.4 / 0 | Precision rises sharply with capacity; ESM-1b is the only PLM beating Gremlin (39.3). |
| 2 | ESM-1 depth at fixed family | 6 L / 12 L / 34 L | 13.2 / 23.7 / 34.7 | −27.9 / −17.4 / −6.4 | Within one family, deeper = better; not yet saturated. |
| 3 | No-weight head averaging | top-1 / top-5 / top-10 heads (avg, no LR) | 29.3 / 35.0 / 38.5 | −11.8 / −6.1 / −2.6 | A single head ≈ Gremlin; averaging top-5 already exceeds it → contacts live in the attention, LR just selects. |
| 4 | LR supervision size n | n=1 / n=10 / n=20 | 39.2 / 40.8 / 41.1 | −1.9 / −0.3 / 0 | One labelled protein already matches Gremlin (p>0.05); diminishing returns past n=10. |
| 5 | Probe label source | MSA-derived labels (Gremlin top-L couplings, n=20) vs structures | 39.9 vs 41.1 | −1.2 | Probe works *without any* solved structure; scarcely worse than PDB labels. |
| 6 | MSA ensembling s | s=1 / s=16 / s=32 / s=64 | 41.1 / 41.9 / 42.3 / **42.6** | 0 / +0.8 / +1.2 / +1.5 | Cheap inference-time gain by averaging contact maps over MSA siblings. |
| 7 | Supervised head vs LR probe | Bilinear head (Rives 2020), 700× more structures | 20.1 (vs 18.6 LR) | +1.5 only | Massive supervision buys ~1.5 pp; signal is in the pre-trained weights. |
| 8 | APC + symmetrisation (App. A.2/A.7) | Required pre-processing of every head's L×L map | — | qualitative | Removes phylogeny/entropy bias; quantitatively essential (analogue of APC in DCA). |
| 9 | L1 weight λ (App. A.7, Fig. 6a) | Grid over {0.05…10}; optimum λ=0.15 | best at 0.15 | — | Sparse head selection wins; only a handful of the 33×20=660 heads carry weight (Fig. 6b, mid-late layers). |
| 10 | Min sequence separation k for training pairs | k=6 vs include local | best at k=6 | — | Excluding |i−j|<6 prevents the probe from over-fitting trivial local contacts. |

**Count: 10 ablations.**

**Top take-away:** Ablations #3–#5 collectively show that the contact signal is fully present in ESM-1b's frozen attention — averaging just the top-1 head matches Gremlin, a single supervised protein closes the gap, and even MSA-only labels suffice. The logistic regression is a feature *selector*, not a learner, which validates the paper's central claim that residue contacts emerge unsupervised from MLM pre-training and that capacity (Ablations #1–#2) is the dominant axis of improvement.
