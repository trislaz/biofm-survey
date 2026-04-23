---
id: endowing-protein-language-models-2024
title: Endowing Protein Language Models with Structural Knowledge
authors:
- Dexiong Chen
- Philip Hartout
- Paolo Pellizzoni
- Carlos Oliver
- Karsten Borgwardt
year: 2024
venue: null
arxiv: '2401.14819'
doi: null
url: https://arxiv.org/abs/2401.14819v1
pdf_path: papers/endowing-protein-language-models-2024.pdf
md_path: papers/md/endowing-protein-language-models-2024.md
modalities:
- protein-sequence
- protein-structure
status: extracted
evidence_quality: medium
tags: [structure-aware, graph-transformer, parameter-efficient, ESM-2, GNN, masked-language-modeling]
parameters: "1137M (650M-base PST; 486M trainable structure extractors). Also 8M/35M/150M base variants."
training_tokens: "542K protein structures (AlphaFold SwissProt subset)"
training_compute: "~10 hours per model on 4× H100 GPUs"
references_chased: false
added_at: '2026-04-22T19:36:52+00:00'
updated_at: '2026-04-22T20:19:38+00:00'
---

## TL;DR

Protein Structure Transformer (PST) augments pretrained ESM-2 by injecting lightweight 2-layer GIN structure extractors into every self-attention block. Pretrained on only 542K AlphaFold SwissProt structures with MLM, PST consistently outperforms ESM-2 on protein function prediction (EC, GO, fold classification, ProteinShake, zero-shot VEP) with fixed representations + linear/MLP head. Structural benefit is largest for small models and tapers at scale; training only structure extractors (freezing ESM-2 backbone) matches full fine-tuning.

## Model

- **Architecture**: ESM-2 backbone + per-layer structure extractor modules. Each extractor is a 2-layer GIN (Graph Isomorphism Network) that takes residue embeddings + protein graph and produces structural embeddings. These are linearly projected and added to Q, K, V matrices before self-attention (Eq. 5). Linear projections Ws initialized to zero so PST = ESM-2 at init.
- **Protein graph**: ε-neighborhood graph, 8Å threshold on Cα distances, no edge attributes (distance features hurt downstream despite helping pretraining).
- **Variants built on**: esm2_t6_8M, esm2_t12_35M, esm2_t30_150M, esm2_t33_650M. PST roughly doubles parameter count of base ESM-2 (e.g., 650M → 1137M total, 486M trainable structure extractor params).
- **Downstream**: Fixed representations (per-layer concatenation of mean-pooled residue embeddings) + MLP (multilabel) or linear head (multiclass). No fine-tuning of representations needed.

## Data

- **Pretraining**: AlphaFold SwissProt subset — 542,378 predicted structures. Same MLM objective as ESM-2.
- **Downstream benchmarks**:
  - DeepFRI EC/GO datasets (538 EC classes, GO terms 50–5000 training samples, 95% sequence identity split; 15.5K/1.7K/1.9K train/val/test for EC).
  - Fold classification (Hou et al., 2018): 12,312 train; Fold/Superfamily/Family splits.
  - ProteinShake (Kucera et al., 2023): EC, GO, Pfam, SCOP, binding site (structure-based splits).
  - 38 deep mutational scanning datasets (Riesselman et al., 2018) for zero-shot VEP.

## Training Recipe

- **Pretraining**: AdamW, linear warmup + inverse sqrt decay. Per-model hyperparams:
  - 8M: lr=3e-4, batch=128, 50 epochs, 5 warmup
  - 35M: lr=1e-4, batch=64, 20 epochs, 5 warmup
  - 150M: lr=5e-5, batch=16, 10 epochs, 1 warmup
  - 650M: lr=3e-5, batch=12, 5 epochs, 1 warmup
- Each model pretrained ~10 hours on 4× H100 GPUs. Initialized from pretrained ESM-2 weights; structure extractors random (θ) / zero (Ws).
- **Downstream heads**: MLP (3 layers, hidden/2 each layer, dropout 0/0.5), 100 epochs, BCE loss, AdamW, ReduceLROnPlateau (factor 0.5, patience 5). Classification heads fine-tuned on 20 GiB H100 MIGs.

## Key Ablations & Design Choices

**PST vs ESM-2 (fixed representations, 650M base)**:
- EC Fmax 0.899 vs 0.892; AUPR 0.918 vs 0.910.
- GO-BP Fmax 0.513 vs 0.509; AUPR 0.371 vs 0.355.
- GO-MF Fmax 0.686 vs 0.686 (tied); AUPR 0.637 vs 0.629.
- GO-CC Fmax 0.541 vs 0.529.
- Fold classification ACC: Fold 40.9 vs 39.7; Superfamily 83.6 vs 80.4; Family 99.4 vs 98.8.
- ProteinShake EC ACC 0.883 vs 0.858; GO Fmax 0.650 vs 0.648; ProteinFamily ACC 0.704 vs 0.698; BindingSite MCC 0.436 vs 0.431; StructuralClass ACC 0.797 vs 0.791.
- Zero-shot VEP mean |ρ| 0.501 vs 0.489.

**PST vs end-to-end baselines (Table 1)**:
- PST (fixed repr) outperforms ESM-1b-GearNetMVC (end-to-end) on EC (0.899 vs 0.894), GO-MF (0.686 vs 0.684).
- PST fine-tuned: EC 0.897, GO-BP 0.489 — fine-tuning does not improve over fixed representations.

**Edge attributes (distance info as 16-dim Gaussian RBF)**:
- Pretraining accuracy improves (47% → 55% for 6-layer) but downstream performance degrades on all ProteinShake tasks — negative transfer. Suggests MLM objective is too simple for richer structural features.

**Pretraining strategy (Fig. 4)**:
- "Struct Only" (freeze ESM-2, train only structure extractors) ≈ "Full" model update across all tasks and model sizes.
- "Struct Only + Seq" (average structure and sequence representations at inference by bypassing extractors) further improves on multiple tasks.

**Model size scaling (Fig. 3)**:
- PST improvement over ESM-2 is largest at small model sizes (8M, 35M) and diminishes at 650M. Large PLMs implicitly capture structural information (Anfinsen's principle), so explicit structure helps most when model capacity is limited.

## Reported Insights

- Structural information is already partially encoded in large PLMs; explicit structure injection is most valuable for parameter-constrained settings.
- The MLM objective may be insufficient to exploit rich geometric features (edge distances); more nuanced pretraining objectives needed for advanced structural inputs.
- Fixed representations from PST are competitive or superior to end-to-end fine-tuned models, saving substantial computation.
- PST can dual-purpose: extract structure-aware or pure sequence representations from a single model (Struct Only strategy).

## References Worth Chasing

1. **ESM-2** — Lin et al., 2023b. Science. Evolutionary-scale prediction of atomic-level protein structure with a language model.
2. **ESM-1b** — Rives et al., 2021. PNAS. Biological structure and function emerge from scaling unsupervised learning to 250M protein sequences.
3. **GearNet / ESM-GearNet** — Zhang et al., 2022 (ICLR); Zhang et al., 2023b (ICLR MLDD). Structure pretraining and joint sequence-structure learning.
4. **Structure-Aware Transformer (SAT)** — Chen et al., 2022 (ICML). Graph transformers with structure extractors — direct architectural ancestor.
5. **DeepFRI** — Gligorijević et al., 2021. Nature Comms. Structure-based protein function prediction with GCNs.
6. **LM-GVP** — Wang et al., 2022. Scientific Reports. Sequence+structure deep learning for protein property prediction.
7. **AlphaFold** — Jumper et al., 2021. Nature. Highly accurate protein structure prediction.
8. **Ankh** — Elnaggar et al., 2023. Optimized protein language model.
9. **ProtBERT-BFD** — Elnaggar et al., 2021. ProtTrans self-supervised protein LMs.
10. **xTrimoPGLM** — Chen et al., 2023. Unified 100B-scale protein pre-trained transformer.
11. **GIN** — Xu et al., 2018 (ICLR). How Powerful are Graph Neural Networks?
12. **ProteinShake** — Kucera et al., 2023 (NeurIPS). Datasets and benchmarks for deep learning on protein structures.
13. **Meier et al., 2021** — NeurIPS. Zero-shot mutation effect prediction with language models.
14. **GVP** — Jing et al., 2020 (ICLR). Learning from protein structure with geometric vector perceptrons.

## Notes / Open Questions

- Only pretrained on 542K structures; AlphaFoldDB has 200M+ — significant scaling opportunity untested.
- No experiments on ESM-2 3B or 15B variants (did not fit in GPU VRAM).
- Fine-tuning PST representations surprisingly does not help over frozen representations — why?
- Edge attribute negative transfer is intriguing; would contrastive or denoising objectives help?
- No protein-protein interaction or ligand design tasks evaluated.
- Structure inputs come from AlphaFold predictions; unclear how robust to prediction errors or experimental structures with missing residues.
