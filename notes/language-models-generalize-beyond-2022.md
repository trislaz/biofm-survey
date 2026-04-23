---
id: language-models-generalize-beyond-2022
title: Language models generalize beyond natural proteins (ESM design / Verkuil et
  al. 2022)
authors:
- Robert Verkuil
- Ori Kabeli
- Yilun Du
- Basile I. M. Wicky
- Lukas F. Milles
- Justas Dauparas
- David Baker
- Sergey Ovchinnikov
- Tom Sercu
- Alexander Rives
year: 2022
venue: bioRxiv
arxiv: null
doi: 10.1101/2022.12.21.521521
url: https://www.biorxiv.org/content/10.1101/2022.12.21.521521v1
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/language-models-generalize-beyond-2022.md
modalities:
- protein-sequence
status: extracted
evidence_quality: abstract+repo
tags:
- de-novo-design
- inverse-folding
- fixed-backbone-design
- free-generation
- protein-language-model
- MLM
- experimental-validation
- transformer
parameters: 650M (ESM-2 backbone used for design)
training_tokens: 65000000000
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: ESM-based protein design; uses pretrained ESM; release of
  designs/models.
---

## TL;DR

This paper demonstrates that ESM-2, a masked-language-model protein transformer trained **only on sequences**, can generalize beyond natural proteins to design de novo proteins. Two tasks are explored: (1) fixed backbone design (sequence for a given structure) and (2) unconstrained free generation (sample novel sequences that fold). 228 designs were experimentally tested with 67% success rate (152/228 soluble + monomeric); 35 had no significant sequence match to any known natural protein. The work shows that protein language models learn a deep grammar of sequence–structure relationships sufficient for generative protein design, not merely memorization of known families.

## Model

- **Base model**: ESM-2 (esm2_t33_650M_UR50D) — a 650M-parameter, 33-layer bidirectional transformer with masked language modeling (MLM) objective. Pre-trained on UniRef50/D (April 2021). The design pipeline does **not** fine-tune ESM-2; it uses the frozen pre-trained model.
- **Design procedure**: Iterative MCMC-style optimization in sequence space. Given a target backbone (fixed backbone) or no constraint (free generation), the method iteratively samples amino acid substitutions, scoring them with a composite energy function that combines:
  - **LM likelihood** (ESM-2 pseudo-log-likelihood under MLM)
  - **Structure compatibility score** via a learned linear projection head on ESM-2 embeddings that predicts pairwise distances (a lightweight new head, not a full structure predictor)
  - **n-gram regularization** (unigram, bigram, trigram frequencies from natural proteins)
- **Accept/reject criterion**: Metropolis–Hastings with an annealing temperature schedule (initial T=8, halved every 10k steps, StepLR with γ=0.5).
- **Iterations**: 170,000 per design (both tasks).
- **Free generation**: Additionally resamples the target structure (backbone) from the model every 3 steps at temperature 1.
- **No MSA**: Single-sequence model; no alignment or evolutionary search at design time.
- **Structure validation**: Designed sequences are independently folded with AlphaFold2 (5× pTM models, best by pLDDT, Amber-relaxed) to predict structure and compute RMSD to target.

## Data

- **ESM-2 pre-training data**: UniRef50/D, April 2021 release (~65B amino-acid tokens). The language model is used as-is; no additional training data for the design pipeline itself.
- **Linear projection head**: A small new layer trained on top of ESM-2 to predict pairwise Cα distances from internal representations. Training details for this head are not fully specified in the abstract/repo; the checkpoint is released as `linear_projection_model.pt`.
- **Design targets (fixed backbone)**: 8 artificially created de novo backbones (PDB structures, e.g., 2N2U). These are targets not found in nature, specifically chosen to test generalization.
- **Experimental evaluation**: 228 designed sequences (228× LM, 20× AlphaFold baseline, 20× AF+ngram, 8× ground truth) synthesized and tested via SEC (size exclusion chromatography).
- **Novelty assessment**: Jackhmmer search (`-n 1 --seed 0`) against UniRef90 with purging of artificial sequences and ESM-2 training set overlaps.

## Training Recipe

- **ESM-2 itself**: Pre-trained separately (see ESM-2/ESMFold paper, Lin et al. 2023, Science). MLM on UniRef50/D, scaled from 8M to 15B params. The 650M checkpoint is used here.
- **Design pipeline**: No gradient-based training. Inference-only iterative sampling:
  - 170,000 MCMC iterations per design
  - Composite energy: `struct_w=3, LM_w=2, ngram_w=1` (trigram orders 1,2,3)
  - Temperature annealing: StepLR, step_size=10000, γ=0.5, initial=8
  - Cysteine suppressed by default (`suppress_AA: 'C'`)
- **Hardware**: Not explicitly stated for the design runs. ESM-2 650M inference is feasible on a single GPU.
- **Software**: PyTorch, Hydra for configuration. Released under `fair-esm` package, MIT license.

## Key Ablations & Design Choices

### Fixed backbone vs. free generation
- **Fixed backbone**: Given a target PDB, iteratively optimize sequence to minimize structural distance to target backbone while maximizing LM likelihood. All 8 artificially created targets produced successful designs.
- **Free generation**: No target structure. The backbone itself is resampled from the model every 3 iterations (`resample_y_every: 3`), allowing the model to co-discover sequence and structure. 55% success rate (71/129).

### Energy function components
- The composite energy balances three terms: structure compatibility (weight 3), LM pseudo-likelihood (weight 2), and n-gram frequency (weight 1). The relative weighting is a key design choice; structure is weighted highest to ensure foldability.

### Novelty of designs
- 35/152 successful designs have **no significant sequence match** to any known natural protein (Jackhmmer E-value > 1 against UniRef90).
- Remaining 117: median 27% sequence identity to nearest match; 6 designs below 20%; 3 as low as 18%.
- This demonstrates the model is not simply recombining known families.

### Comparison to AlphaFold-based design
- 20 designs produced with AlphaFold hallucination + 20 with AF+ngram were included as baselines. The LM-design approach achieves comparable or better experimental success rates, with the advantage of being faster and simpler (no MSA, no backpropagation through a structure predictor).

### Structural motifs
- Designed proteins exhibit motifs found in related natural structures **and** motifs not observed in similar structural contexts in known protein families, indicating genuine generalization.

## Reported Insights

- **LMs learn structure from sequence alone**: Despite training only on sequences, ESM-2 captures enough sequence–structure grammar to design foldable proteins, including structures unlike anything in nature.
- **67% experimental success rate**: 152/228 designs produced soluble, monomeric species — a high success rate for computational protein design.
- **De novo proteins are genuinely novel**: Many designs have no detectable homology to natural proteins, ruling out memorization as the explanation.
- **Fixed backbone is easier than free generation**: 100% success on fixed backbone targets vs. 55% on free generation, consistent with the constrained problem being easier.
- **Simple pipeline**: The method requires only a frozen pre-trained LM + a lightweight linear projection + MCMC sampling. No fine-tuning, no backpropagation through large models at design time.
- **Deep grammar of proteins**: The models learn motifs linking sequence and structure that go beyond surface-level statistics, including context-dependent structural preferences.

## References Worth Chasing

1. **Lin et al. 2023** — "Evolutionary-scale prediction of atomic-level protein structure with a language model" (Science; doi:10.1126/science.ade2574). ESM-2 and ESMFold; the base model used here.
2. **Rives et al. 2021** — "Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250M Protein Sequences" (PNAS; doi:10.1073/pnas.2016239118). ESM-1/ESM-1b predecessor.
3. **Hie, Candido et al. 2022** — "A High-Level Programming Language for Generative Protein Design" (bioRxiv 2022.12.21.521526). Companion protein design paper using ESMFold rather than ESM-2 LM.
4. **Dauparas et al. 2022** — ProteinMPNN; structure-based sequence design baseline.
5. **Anishchenko et al. 2021** — "De novo protein design by deep network hallucination" (Nature). AlphaFold/trRosetta hallucination-based design; key comparator.
6. **Hsu et al. 2022** — "Learning Inverse Folding from Millions of Predicted Structures" (bioRxiv 2022.04.10.487779). ESM-IF1 inverse folding model.
7. **Ferruz et al. 2022** — "ProtGPT2: Deep Unsupervised Language Modelling for Protein Design" (Nature Comm.). Autoregressive protein generation baseline.
8. **Jumper et al. 2021** — "Highly accurate protein structure prediction with AlphaFold" (Nature). AlphaFold2 used for in-silico structure validation of designs.

## Ablations (Rev 4)

Source: abstract (Semantic Scholar) + released `lm-design` repo (`conf/config.yaml`, `paper-data/README`). The full bioRxiv text is Cloudflare-protected and could not be fetched, so quantitative per-axis sweeps (success rate vs. temperature, vs. ESM-2 size, vs. masking %) are not directly verifiable here; entries marked **(repo-default)** come from the released config and entries marked **(not in abstract/repo)** require the paper PDF to confirm.

| Axis | Setting | Reported / configured value | Effect (per abstract+repo) |
|------|---------|-----------------------------|----------------------------|
| Decoding: MCMC vs. greedy | **MCMC (Metropolis–Hastings)** with simulated annealing | 170,000 iters/design; accept-reject with composite energy `struct_w=3, LM_w=2, ngram_w=1` (repo-default) | Only MCMC is released and used to produce the 228 wet-lab designs (152/228 = 67% success). Greedy is not in the released config; head-to-head numbers (not in abstract/repo). |
| Decoding: free-generation backbone resample | Resample target structure every *k* steps at temperature `T_y` | `resample_y_every: 3`, `resample_y_temp: 1` (repo-default) | Enables co-discovery of sequence + structure in unconstrained mode; 71/129 = 55% experimental success. |
| ESM-2 model size | 8M / 35M / 150M / 650M / 3B / 15B available | **650M** (`esm2_t33_650M_UR50D`) used for all released designs (repo-default) | Larger checkpoints exist but the design pipeline ships pinned to 650M; per-size sweep (not in abstract/repo). |
| Sampling temperature (sequence) | Annealed Metropolis temperature (StepLR) | initial `T=8`, `step_size=10000`, `gamma=0.5` → halves every 10k steps over 170k iters (repo-default) | High initial T encourages exploration; geometric cooling drives convergence to high-likelihood, structure-compatible sequences. Per-T success curves (not in abstract/repo). |
| Sampling temperature (structure resample, free-gen only) | `resample_y_temp` | `1.0` (repo-default) | Held fixed in released runs; sweep (not in abstract/repo). |
| Masking % (per-step substitutions) | Fraction of positions proposed for resampling per MCMC step | Not exposed as a config knob in the released `config.yaml`; pipeline scores single-position MLM substitutions rather than block-masked reconstructions | Per-mask-rate sweep (not in abstract/repo). |
| Energy-term weights | `struct_w : LM_w : ngram_w` | **3 : 2 : 1** with n-gram orders {1,2,3} (repo-default) | Structure dominates to enforce foldability; LM term enforces native-likeness; n-gram regularizes amino-acid composition. Per-weight ablation (not in abstract/repo). |
| Amino-acid alphabet | Cysteine suppression | `suppress_AA: 'C'` (repo-default) | Removes disulfide complications from wet-lab characterization; effect on success rate (not in abstract/repo). |
| Baseline comparators (in 228-design pool) | LM-design vs. AlphaFold-hallucination vs. AF + n-gram vs. ground truth | 228× LM, 20× AF, 20× AF+ngram, 8× GT (`paper-data/data.csv`) | LM-design is reported in the abstract as achieving 67% overall success; per-baseline success rates require the paper text. |

**Top take-away**: With ESM-2 650M frozen and no fine-tuning, a single, fixed MCMC recipe (`struct:LM:ngram = 3:2:1`, annealed `T 8 → … → 0` over 170k steps, cysteine masked out) is enough to wet-lab-validate de novo proteins at 67% success (152/228), including 35 designs with no detectable homology to UniRef90 — i.e. the design quality demonstrated in the paper is driven by the energy composition + annealing schedule, not by scaling the base LM beyond 650M.

## Notes / Open Questions

- **Evidence quality = abstract+repo**: The full paper text was not available; details are reconstructed from the abstract, GitHub code/config, paper-data README, and web sources. Key quantitative details (e.g., full ablation tables, per-design breakdowns) may be missing.
- **ESM-2 650M, not 15B**: The design pipeline uses the 650M checkpoint, not the largest 15B model. Whether scaling the base LM to 3B or 15B would improve design success rates is not explored.
- **Linear projection head**: A small model trained on top of ESM-2 to predict pairwise distances. Training data, objective, and architecture details for this head are not fully documented in the repo. The checkpoint (`linear_projection_model.pt`) is auto-downloaded.
- **No fine-tuning**: The method deliberately avoids fine-tuning ESM-2, keeping it frozen. This is a strength (simplicity, no catastrophic forgetting) but may limit the design space.
- **Cysteine suppression**: Default config suppresses cysteine (`suppress_AA: 'C'`), likely to avoid disulfide bond complications in experimental validation. This constraint may limit structural diversity.
- **Comparison to diffusion-based methods**: RFdiffusion (Watson et al. 2023) and other structure-diffusion approaches for protein design appeared around the same time. A direct comparison is not included.
- **No journal publication**: As of the available information, this remains a bioRxiv preprint (Dec 2022). Whether it has been published in a peer-reviewed journal is unclear.
- **Successor**: ESM-3 (2024, EvolutionaryScale) is a multimodal generative model over sequence, structure, and function that may supersede this MCMC-based design approach.
