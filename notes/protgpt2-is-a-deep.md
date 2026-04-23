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
