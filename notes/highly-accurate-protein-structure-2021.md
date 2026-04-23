---
id: highly-accurate-protein-structure-2021
title: Highly accurate protein structure prediction with AlphaFold
authors:
- John Jumper
- Richard Evans
- Alexander Pritzel
- Tim Green
- Michael Figurnov
- Olaf Ronneberger
- Kathryn Tunyasuvunakool
- Russ Bates
- Augustin Žídek
- Anna Potapenko
- Alex Bridgland
- Clemens Meyer
- Simon A. A. Kohl
- Andrew J. Ballard
- Andrew Cowie
- Bernardino Romera-Paredes
- Stanislav Nikolov
- Rishub Jain
- Jonas Adler
- Trevor Back
- Stig Petersen
- David Reiman
- Ellen Clancy
- Michal Zielinski
- Martin Steinegger
- Michalina Pacholska
- Tamas Berghammer
- Sebastian Bodenstein
- David Silver
- Oriol Vinyals
- Andrew W. Senior
- Koray Kavukcuoglu
- Pushmeet Kohli
- Demis Hassabis
year: 2021
venue: Nature
arxiv: null
doi: 10.1038/s41586-021-03819-2
url: https://www.nature.com/articles/s41586-021-03819-2
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/highly-accurate-protein-structure-2021.md
modalities:
- protein-structure
status: extracted
evidence_quality: abstract+repo
tags:
- evoformer
- invariant-point-attention
- recycling
- MSA
- structure-prediction
- self-distillation
- end-to-end
- FAPE-loss
- triangle-attention
- equivariant
- CASP14
parameters: ~93M
training_tokens: null
training_compute: ~1e23 FLOPs (≈20 exaFLOP/s-days)
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

AlphaFold2 is an end-to-end neural network that predicts all-atom protein 3D structures from amino-acid sequence and MSAs with near-experimental accuracy. It dominated CASP14 (median backbone RMSD 0.96 Å vs 2.8 Å for the next-best method; median GDT 92.4). The architecture centres on the **Evoformer** trunk (48 blocks of interleaved MSA-row/column attention and pair-representation triangle updates) followed by a **structure module** built on Invariant Point Attention (IPA) that outputs per-residue rigid-body frames. **Recycling** (3 passes through the full network) and **self-distillation** on ~350 k Uniclust30 predictions further boost accuracy. With ~93 M parameters and ~20 exaFLOP/s-days of training on 128 TPUv3 cores, AlphaFold2 set a new paradigm for computational structural biology and earned the 2024 Nobel Prize in Chemistry.

## Model

- **Input**: primary sequence + MSA (from Jackhmmer on UniRef90/MGnify, HHBlits on BFD/Uniclust30) + optional homologous templates from PDB70.
- **Evoformer trunk** (48 blocks):
  - MSA representation: N_seq × N_res × c_m (c_m = 256). Row-wise gated self-attention with pair bias, column-wise gated self-attention.
  - Pair representation: N_res × N_res × c_z (c_z = 128). Triangle multiplicative updates (outgoing & incoming edges), triangle self-attention (starting & ending nodes), transition blocks.
  - Outer-product mean: projects MSA representation into pair representation every block (continuous communication).
  - Very deep MSAs (>2048 seqs at inference) handled via extra-MSA stack (4 blocks operating on a subsample, feeding into pair representation).
- **Structure module** (8 layers, weight-shared):
  - Operates on a "residue gas" of N_res independent rigid-body frames (rotation + translation) initialized at the origin/identity.
  - **Invariant Point Attention (IPA)**: augments standard multi-head attention with 3D query/key/value points in each residue's local frame; invariant to global rotation/translation.
  - Updates single representation → equivariant backbone frame update → side-chain torsion (χ) prediction.
  - Outputs: all heavy-atom 3D coordinates, per-residue pLDDT confidence, pairwise aligned error (PAE) for pTM models.
- **Recycling**: output pair representation, single representation, and predicted coordinates are fed back as input for 3 recycling iterations (total network is applied 3×). Contributes markedly to accuracy.
- **Ensembling** (CASP14 config): 8 model ensembles (monomer_casp14 preset); default monomer preset uses no ensembling for efficiency.
- **Post-prediction relaxation**: Amber99sb force-field gradient descent (OpenMM) to fix stereochemical violations; does not improve GDT/lDDT.
- **Parameters**: ~93 M per model. 5 CASP14 models + 5 pTM models + 5 multimer models released.
- **Framework**: TensorFlow + Sonnet (JAX port in OpenFold).

## Data

- **Training structures**: PDB as of 2018-04-30 (CASP14 models); v2.3.0 retrained with cutoff 2021-09-30 (~30% more data, 4× more cryo-EM structures).
- **MSA databases** (at both training and inference):
  - UniRef90 v2020_01
  - BFD (Big Fantastic Database): 65.98 M protein families, 2.2 B sequences from UniProt, metagenomes, metatranscriptomes; custom-built, ~1.8 TB.
  - Uniclust30 v2018_08
  - MGnify v2018_12
- **Template database**: PDB70 (May 2020) searched with HHSearch.
- **Self-distillation set**: ~350 k diverse sequences from Uniclust30, predicted by a trained AlphaFold model, filtered to high-confidence predictions.
- **Total genetic database download**: ~2.6 TB uncompressed (556 GB download).

## Training Recipe

- **Hardware**: 128 TPUv3 cores.
- **Initial training**: ~10 M samples of 256-residue crops from PDB chains. Trained for ~100 k steps with the initial learning rate 1e-3, Adam optimizer.
- **Fine-tuning**: longer crops (384 residues for v2.0; 640 for v2.3.0 multimer), PDB + self-distillation mixture, violation loss added, full-chain FAPE. ~50 k additional steps.
- **Recycling**: 3 iterations during training (stochastic; uniform random number of recycles 0–3 with loss on final output only to save memory).
- **Total training compute**: ~20 exaFLOP/s-days (~1.7 × 10²³ FLOPs). Approximately a few hundred thousand TPUv3 core-hours.
- **Training duration**: approximately 1–2 weeks wall-clock for initial training; a few days for fine-tuning.
- **Loss functions**:
  - **FAPE** (Frame Aligned Point Error): clamped L1 on atom positions under all residue-local frame alignments. Primary structure loss; source of chirality.
  - **Auxiliary heads**: distogram loss (binned Cβ distances, cross-entropy), masked MSA loss (BERT-style prediction of masked residues), experimentally-resolved head, pLDDT head, pTM head (pTM models only).
  - **Violation loss** (fine-tuning only): penalizes steric clashes, bond length/angle violations.
  - **Intermediate losses**: structure module losses applied at each of 8 layers (intermediate supervision) weighted by 0.5.
- **Self-distillation procedure**: train model on PDB → predict structures for ~350 k Uniclust30 sequences → filter to high confidence → retrain from scratch on PDB + distilled data with augmentation (crop, MSA subsampling). Effective use of unlabelled protein sequences.
- **Masked MSA objective**: jointly trained with structure loss (not pre-trained); randomly mask/mutate MSA residues, predict original identity. Encourages learning phylogenetic/covariation patterns.
- **Inference**: ~1 GPU-minute per model for 384 residues on A100. 3 recycling iterations default; v2.3.0 supports up to 20 with early stopping.

## Key Ablations & Design Choices

The paper's Fig. 4a and Supplementary Methods 1.13 report extensive ablations on CASP14 (87 domains, GDT) and a PDB test set (2,261 chains with ≤30% template coverage, lDDT-Cα). All ablations are differences from a 3-seed baseline average.

### Evoformer components
- **No templates**: −0.3 GDT (CASP14), −0.4 lDDT (PDB). Templates help modestly; the network can largely recover without them.
- **No extra MSA stack**: −1.3 GDT, −0.4 lDDT. The extra MSA stack for very deep MSAs is moderately important.
- **No outer-product mean** (MSA→pair): not individually ablated but the continuous outer-product-every-block design replaced the single-shot approach in earlier architectures.
- **Triangle attention only (no multiplicative update)**: high-accuracy structures still achievable; combination of both yields best results.
- **Triangle multiplicative update only (no attention)**: also produces high-accuracy structures independently.

### Structure module & loss
- **No IPA (standard attention only)**: significant accuracy drop. IPA's spatial/locality bias is critical for iterative structure refinement.
- **No recycling**: −3.1 GDT (CASP14), −1.8 lDDT (PDB). One of the largest single-component ablation effects.
- **No intermediate structure module losses**: −0.5 GDT, −0.5 lDDT. Intermediate supervision at each layer matters.
- **No FAPE (use distogram loss only)**: large accuracy drop; end-to-end structure prediction via FAPE is essential.
- **No violation loss**: stereochemical violations increase but GDT/lDDT largely unaffected; fine-tuning loss is for physical correctness.

### Training procedure
- **No self-distillation**: −1.8 GDT (CASP14), −2.0 lDDT (PDB). Self-distillation from unlabelled sequences is one of the most impactful training choices.
- **No masked MSA loss**: −0.2 GDT, −0.5 lDDT. BERT-style auxiliary objective has modest but consistent benefit.
- **Crop size**: larger crops (384→640 in v2.3.0) improve accuracy on large complexes significantly.

### MSA depth sensitivity
- Accuracy degrades sharply when median MSA depth falls below ~30 sequences (N_eff); above ~100 sequences, diminishing returns. Threshold effect: MSA is needed to coarsely find the correct fold; refinement is less MSA-dependent.
- Removing BFD: −0.4 GDT; removing MGnify: −0.7 GDT; removing both: −6.1 GDT.

### Ensembling
- 8-model ensemble (monomer_casp14): +0.1 GDT over single model — 8× compute for negligible gain. Default preset uses a single model.

## Reported Insights

- **Near-experimental accuracy**: median backbone RMSD 0.96 Å on CASP14 (carbon atom width ≈ 1.4 Å). All-atom RMSD 1.5 Å. Best on 88/97 CASP14 targets.
- **Iterative refinement trajectories**: separate structure modules trained at each Evoformer block reveal a smooth trajectory (192 intermediate structures over 4 recycles × 48 blocks). Easy proteins converge early; hard proteins (e.g., SARS-CoV-2 ORF8) search and rearrange over many layers.
- **Structural hypothesis emerges early**: a concrete structural hypothesis arises in early Evoformer blocks and is continuously refined.
- **pLDDT as reliable confidence**: pLDDT ≈ lDDT-Cα (Pearson r = 0.76 on full chains). Enables filtering predictions by confidence.
- **Limitation — heterotypic contacts**: accuracy degrades for proteins whose shape depends on inter-chain contacts (bridging domains in complexes). Addressed by AlphaFold-Multimer.
- **Physical knowledge without physics**: AlphaFold builds hydrogen bonds, handles missing ligands, resolves homomers without explicit physics-based energy functions — learned from PDB data alone.
- **Proteome-scale prediction**: companion paper (Tunyasuvunakool et al. 2021) applies AlphaFold to the entire human proteome. AlphaFold Protein Structure Database covers >200 M structures.
- **2024 Nobel Prize in Chemistry**: Demis Hassabis and John Jumper shared one half "for protein structure prediction."

## References Worth Chasing

1. **Senior et al. 2020** — "Improved protein structure prediction using potentials from deep learning" (Nature 577). AlphaFold1 / CASP13 predecessor.
2. **Tunyasuvunakool et al. 2021** — "Highly accurate protein structure prediction for the human proteome" (Nature). Companion paper; proteome-scale deployment.
3. **Evans et al. 2022** — "Protein complex prediction with AlphaFold-Multimer" (bioRxiv 2021.10.04.463034). Extension to protein complexes.
4. **Rao et al. 2021** — "MSA Transformer" (ICML). MSA-based protein LM; AlphaFold trains masked MSA loss jointly (not pre-trained), unlike MSA Transformer.
5. **Rives et al. 2021** — "Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250M Protein Sequences" (PNAS). ESM-1b; representation learning baseline.
6. **Lin et al. 2023** — "Evolutionary-scale prediction of atomic-level protein structure with a language model" (Science). ESMFold; single-sequence folding competitor using ESM-2 + AF2-style structure module.
7. **Baek et al. 2021** — "Accurate prediction of protein structures and interactions using a three-track neural network" (Science). RoseTTAFold; concurrent end-to-end structure predictor.
8. **Abramson et al. 2024** — "Accurate structure prediction of biomolecular interactions with AlphaFold 3" (Nature). AlphaFold3; successor with diffusion-based structure module.
9. **AlQuraishi 2019** — "End-to-end differentiable learning of protein structure" (Cell Systems). RGNN; early end-to-end structure prediction.
10. **Mirdita et al. 2022** — "ColabFold: Making Protein Folding Accessible to All" (Nature Methods). Community integration; MMseqs2 for fast MSA.
11. **Ahdritz et al. 2022** — "OpenFold: Retraining AlphaFold2 yields new insights into its learning mechanisms and capacity for generalization" (bioRxiv). Open-source JAX/PyTorch reimplementation with training code.
12. **Weigt et al. 2009** — "Identification of direct residue contacts in protein–protein interaction by message passing" (PNAS). Direct coupling analysis; evolutionary covariation foundation.
13. **Vaswani et al. 2017** — "Attention Is All You Need" (NeurIPS). Transformer architecture underlying Evoformer.
14. **Xie et al. 2020** — "Self-training with noisy student improves ImageNet classification" (CVPR). Noisy-student self-distillation inspiration.
15. **Steinegger & Söding 2018** — "Clustering huge protein sequence sets in linear time" (Nature Comm.). MMseqs2/Linclust; basis for BFD construction.

## Notes / Open Questions

- **Parameters ~93 M**: relatively modest by LLM standards; architectural inductive biases (Evoformer, IPA, FAPE, recycling) are the main drivers rather than scale.
- **Not a foundation model in the LLM sense**: AlphaFold2 is a task-specific supervised model (structure prediction), not a general-purpose pre-trained representation. No pre-training on unsupervised sequence data (masked MSA loss is auxiliary, not pre-trained). Contrast with ESM-2 or ProtTrans.
- **MSA dependency**: requires MSA search at inference (seconds to minutes), unlike single-sequence models (ESMFold, OmegaFold). This is both a strength (leverages evolutionary information) and limitation (orphan proteins, speed).
- **Training data modesty**: trained only on ~170 k PDB structures + ~350 k distilled. No massive sequence corpus for pre-training.
- **OpenFold** (Ahdritz et al.) provides the community with fully open training code and reproduces AF2 results, enabling further research on training dynamics and generalization.
- **Self-distillation is under-explored**: the procedure of predicting structures for unlabelled sequences and retraining is highly effective (+1.8 GDT) but the optimal filtering threshold, dataset size, and iterative distillation remain open.
- **Recycling mechanism**: related to iterative refinement in computer vision; the stochastic recycling schedule during training (uniform random 0–3 recycles) is a practical trick to reduce memory. v2.3.0 supports up to 20 recycles with early stopping.
- **License**: code Apache 2.0; model weights CC BY 4.0. Fully open weights and inference code; training code not released (OpenFold fills this gap).
- **Successor**: AlphaFold3 (2024) replaces Evoformer with simpler Pairformer, adds diffusion-based structure generation, and extends to DNA/RNA/ligands/ions.

## Verification (Rev 3)

- **[supported]** "Structure prediction requires specialised blocks — Evoformer + IPA in AlphaFold 2" (insights L15) — Paper describes the Evoformer trunk (48 blocks) and IPA-based structure module as core architectural contributions (Fig. 1e, Methods).
- **[supported]** "AlphaFold 2's own self-distillation added +1.8 GDT" (insights L29) — Ablation Table: "No self-distillation: −1.8 GDT (CASP14), −2.0 lDDT (PDB)" (Suppl. Methods 1.13, Fig. 4a).
- **[supported]** "Evoformer (48 blocks of row/column gated self-attention + pair bias) coupled with an Invariant Point Attention (IPA) structure module and 3-pass recycling" (insights L123) — Matches paper: 48 Evoformer blocks, row-wise gated self-attention with pair bias, column-wise gated self-attention, IPA in 8-layer structure module, 3 recycling iterations (Methods, Suppl. Methods 1.6–1.8).
- **[partial]** "AlphaFold 2 requires both FAPE loss and a masked-MSA auxiliary loss; removing either substantially degrades accuracy (no recycling = −3.1 GDT)" (insights L170) — FAPE removal does cause a large accuracy drop (Suppl. Methods 1.13). However, masked-MSA removal is only −0.2 GDT/−0.5 lDDT (modest, not "substantial"). The −3.1 GDT figure is for no recycling, not for either loss — it is miscited as a parenthetical to the FAPE/masked-MSA claim.
- **[partial]** "AF2 | Protein + MSA | ~1500 residues (cropped) | Evoformer crops + recycling" (insights L207) — Training uses 256-residue crops (initial) and 384/640 (fine-tuning); at inference, full-length proteins are processed (demonstrated on 2,180 residues, Fig. 1d). The "~1500" figure is not stated in the paper; no hard crop at inference.
- **[supported]** "AlphaFold 2 used self-distillation: training on ~350 K of its own high-confidence predictions added +1.8 GDT over PDB-only training" (insights L229) — Same as L29; confirmed by ablation (Suppl. Methods 1.13).
- **[supported]** "AlphaFold 2's IPA module enforces SE(3) equivariance in the structure module" (insights L264) — IPA computes SE(3)-invariant attention weights in residue-local frames, enabling equivariant backbone frame updates (Suppl. Methods 1.8.2). The structure module output is equivariant by construction through IPA.
- **[supported]** "AlphaFold 2 uses 3-pass recycling where outputs are fed back as inputs; no recycling degrades accuracy by −3.1 GDT" (insights L276) — Paper: 3 recycling iterations; ablation: "No recycling: −3.1 GDT (CASP14)" (Suppl. Methods 1.13, Fig. 4a).
- **[supported]** "MSA-based methods … achieve the highest accuracy (median RMSD 0.96 Å on CASP14 for AF2)" (insights L325) — Paper: "median backbone accuracy of 0.96 Å r.m.s.d.95" (Main text, Fig. 1a).
- **[supported]** "Self-distillation (AF2→AF2): AlphaFold 2 trains on ~350 K of its own high-confidence predictions, adding +1.8 GDT" (insights L342) — Same ablation as L29/L229; confirmed.
- **[supported]** "AlphaFold 2 achieved median RMSD 0.96 Å on CASP14, using Evoformer (48 blocks) + IPA structure module + 3-pass recycling. Critical ablations: self-distillation on 350 K predictions (+1.8 GDT), FAPE loss (essential), recycling (+3.1 GDT). 93 M params." (insights L465–466) — All sub-claims verified: RMSD 0.96 Å (Fig. 1a), 48 Evoformer blocks, IPA, 3-pass recycling, self-distillation +1.8 GDT, FAPE essential, recycling +3.1 GDT, ~93 M parameters (Suppl. Methods 1.13).
