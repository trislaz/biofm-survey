---
id: protgpt2-is-a-deep
title: ProtGPT2 is a deep unsupervised language model for protein design
authors: []
year: 2022
venue: Nature Communications
arxiv: null
doi: 10.1038/s41467-022-32007-7
url: https://huggingface.co/nferruz/ProtGPT2
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/protgpt2-is-a-deep.md
modalities:
- protein-sequence
status: extracted
evidence_quality: full-text
tags:
- autoregressive
- generative
- de-novo
- protein-design
- decoder-only
- transformer
parameters: 738M
training_tokens: not-reported
training_compute: not-reported
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'ProtGPT2: pretrained generative protein LM.'
---

## TL;DR

ProtGPT2 is a 738M-parameter autoregressive (GPT2-large architecture) language model trained on ~45M UniRef50 protein sequences. It generates de novo protein sequences displaying natural amino acid propensities, ~88% globular content, and well-ordered predicted structures (validated by AlphaFold, Rosetta, and MD). Generated sequences are distantly related to natural proteins and explore previously unseen regions of protein space, including novel topologies. No wet-lab validation is presented.

## Model

- **Architecture:** Decoder-only Transformer matching GPT2-large (36 layers, d_model=1280, 738M parameters)
- **Tokeniser:** BPE with 50,256 tokens (trained on Swiss-Prot 2021_04, ~0.5M sequences); average token ≈ 4 amino acids
- **Positional encoding:** Learned positional embeddings (as in GPT2)
- **Context length:** 512 tokens (main model); a 1024-token variant was also prepared but results use 512
- **Objective:** Causal language modelling (next-token prediction, negative log-likelihood)
- **Inference:** Top-k sampling (k=950), repetition penalty 1.2, default temperature and top_p=1.0

## Data

- **Training corpus:** UniRef50 v2021_04 — 49,874,565 sequences clustered at 50% identity from UniProt
- **Split:** 90/10 random → 44.88M training, 4.99M validation
- **No functional annotations used** (fully unsupervised)
- **Tokenizer trained on Swiss-Prot** (~0.5M sequences), separate from training data

## Training Recipe

- **Optimizer:** Adam (β₁=0.9, β₂=0.999), learning rate 1e-3
- **Batch size:** 65,536 tokens/batch (128 GPUs × 512 tokens); per-device batch size 8, effective global batch 1024 sequences
- **Hardware:** 128 × NVIDIA A100 GPUs
- **Wall time:** 4 days
- **Parallelism:** DeepSpeed
- **Weight initialisation:** GPT2-large architecture downloaded from HuggingFace; weights **re-initialised** before training (trained from scratch)
- **Number of epochs / total training tokens:** Not reported

## Key Ablations & Design Choices

| Choice | Alternatives explored | Outcome |
|---|---|---|
| Sampling strategy | Greedy, beam search (beams 50–100), top-k (250–1000), top-p (0.7–1.0) | Greedy/beam → repetitive sequences; top-k=950 + rep. penalty 1.2 best matches natural AA propensities |
| Repetition penalty | 1.1–3.0 (step 0.1) | 1.2 optimal (consistent with other generative models) |
| UniRef50 vs UniRef100 | Cited ESM work showing UR50 improves generalisation | Chose UR50 |
| Block size | 512 vs 1024 tokens | Results reported for 512; 1024 also prepared but not shown |

## Reported Insights

- **Globularity:** 87.6% of generated sequences predicted globular by IUPred3, matching 88.4% in natural sequences
- **Secondary structure:** α-helix 48.6%, β-sheet 39.7%, coil 11.7% (natural: 45.2%, 41.9%, 12.9%)
- **Homology:** 93% of ProtGPT2 sequences have HHblits hits above the HSSP curve in Uniclust30 (vs 96.2% natural, 7% random); high-identity matches (>90%) are short (<15 aa), indicating novelty not memorisation
- **AlphaFold pLDDT:** Mean 63.2 (best of 5); 37% >70 pLDDT (natural: 75.3 mean, 66% >70; random: 44 mean)
- **Rosetta energy:** −1.73 REU/residue (natural −1.90; random −0.13)
- **MD simulations:** Mean RMSD 3.12 Å vs 2.93 Å natural (p=0.39 Mann–Whitney); random 9.41 Å
- **Novel topologies:** Protein 4266 has no matching PDB topology (DALI Z-score 5.4)
- **Functional hotspot preservation:** Despite ~30% identity, binding-site residues are conserved in generated sequences (FAD-binding, phosphodiesterase active site examples)
- **Protein space bridging:** ProtGPT2 sequences connect separate islands in the protein structure similarity network

## References Worth Chasing

- **ProGen (Madani et al.):** Autoregressive protein generation with conditional tags (refs 19–21)
- **RITA (Hesslow et al.):** Autoregressive Transformer for proteins (ref 22)
- **DARK (Moffat et al.):** Autoregressive model sampling dark proteome (ref 23)
- **ESM (Rives et al.):** BERT-style protein LMs; showed UR50 improves generalisation (ref 10)
- **ProtTrans (Elnaggar et al.):** Large-scale protein Transformers (ref 11)
- **Holtzman et al.:** Sampling strategies — "The Curious Case of Neural Text Degeneration" (ref 32)

## Notes / Open Questions

- Number of training epochs and total tokens processed are **not reported**, making compute estimates uncertain. Rough estimate: 128 A100s × 4 days ≈ 4.4×10⁷ GPU-seconds.
- The paper is entirely computational; **no wet-lab experimental validation** of generated sequences.
- Fine-tuning on specific families is mentioned as straightforward but not demonstrated.
- Conditional generation (e.g., with functional tags) is listed as future work and later pursued in ZymCTRL and other follow-ups.
- BPE tokenizer learns sub-word units (avg 4 aa) rather than single amino acids — impact on generation quality vs single-token AA models is not ablated.

## Ablations (Rev 4)

Re-extraction focused exclusively on systematic sweeps and design-choice comparisons reported in the paper. ProtGPT2 contains **no architectural or training-data ablations**; all reported sweeps are *inference-time decoding* studies, evaluated by amino-acid-frequency match to UniRef50 (1M reference sequences, 100 generated sequences per parameter set).

| # | Axis | Range / Variants Swept | Step | Selection Metric | Winning Setting | Reported Effect |
|---|---|---|---|---|---|---|
| 1 | Decoding family | Greedy vs Beam search vs Random sampling (top-k) | — | AA-frequency match + qualitative repetitiveness (Fig. 1e–h) | Random top-k sampling | Greedy/beam → repetitive, degenerate sequences; sampling required for natural-like propensities |
| 2 | Beam width (beam search) | 50 → 100 beams | 1 | AA-frequency match | None — discarded | "Worse matches in all cases" vs sampling |
| 3 | top-k | 250 → 1000 | 50 | AA-frequency match (top-7 AAs) | **k = 950** | Best matches occur for k > 800; small k under-samples natural propensities |
| 4 | top-p (nucleus) | 0.7 → 1.0 | 0.05 | AA-frequency match | **top_p = 1.0** (default) | Default outperformed restrictive nucleus values |
| 5 | Repetition penalty | 1.1 → 3.0 | 0.1 | AA-frequency match | **1.2** | Consistent with prior generative-model findings (refs 33, 34); higher values degrade match |
| 6 | Temperature | (default only — varied implicitly) | — | AA-frequency match | **default (1.0)** | Not independently swept; held at default once k/penalty fixed |
| 7 | Context window for generation | 250-token sliding window during sampling | — | Sequence completeness (truncation filtering) | 250 tokens | 100k generated → 29,876 untruncated → 10k subsampled |
| 8 | Block size (training) | 512 vs 1024 tokens | — | (Not reported quantitatively) | **512** | 1024-token variant prepared but results not shown |

**Count: 8 ablation axes** (5 fully quantitative inference sweeps + 1 decoding-family comparison + 1 generation-window choice + 1 partially-explored training block size).

**Top take-away:** ProtGPT2's only systematic ablations are over *decoding hyperparameters*, not model or data design. The dominant finding is that **aggressive random sampling (top-k = 950, repetition penalty = 1.2, top-p = 1.0)** is required to recover natural amino-acid propensities — greedy and beam search collapse into repetitive sequences regardless of model quality, and small top-k values bias the output away from natural composition. No architectural, data-scale, tokenizer, or context-length ablations are reported.
