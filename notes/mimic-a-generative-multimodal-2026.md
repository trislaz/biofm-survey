---
id: mimic-a-generative-multimodal-2026
title: 'MIMIC: A Generative Multimodal Foundation Model for Biomolecules'
authors:
- Siavash Golkar
- Jake Kovalic
- Irina Espejo Morales
- Samuel Sledzieski
- Minhuan Li
- Ksenia Sokolova
- Geraud Krawezik
- Alberto Bietti
- Claudia Skok Gibbs
- Roman Klypa
- Shengwei Xiong
- Francois Lanusse
- Liam Parker
- Kyunghyun Cho
- Miles Cranmer
- Tom Hehir
- Michael McCabe
- Lucas Meyer
- Rudy Morel
- Payel Mukhopadhyay
- Mariel Pettee
- Helen Qu
- Jeff Shen
- David Fouhey
- Hadi Sotoudeh
- Vikram Mulligan
- Pilar Cossio
- Sonya M. Hanson
- Alisha N. Jones
- Olga G. Troyanskaya
- Shirley Ho
year: 2026
venue: null
arxiv: '2604.24506'
doi: null
url: https://arxiv.org/abs/2604.24506
pdf_path: null
md_path: null
modalities:
- dna
- multimodal
- protein-sequence
- protein-structure
- rna
status: extracted
evidence_quality: abstract+repo
tags:
- multimodal
- encoder-decoder
- generative
- any-to-any
- split-track-architecture
- register-token-compression
- curriculum-context-length
- rna-splicing
- protein-design
- modality-dropout
- masked-reconstruction
- semantic-conditioning
- isoform-aware
parameters: ~1B
training_tokens: 13M RNA transcripts + 15.5M proteins + >4B NL tokens; 6000+ organisms
  (LORE dataset)
training_compute: null
references_chased: false
added_at: '2026-04-29T21:20:26+00:00'
updated_at: '2026-04-29T21:20:26+00:00'
is_fm: true
fm_classification_reason: 'MIMIC: generative multimodal FM for biomolecules trained
  on the LORE dataset.'
---

## TL;DR

MIMIC is a ~1B-parameter generative multimodal foundation model for biomolecules, trained on the newly curated LORE (Linked Omics and Representation) dataset that aligns nucleic acid, protein, evolutionary, structural, regulatory, and semantic/contextual modalities. The model uses a split-track encoder-decoder architecture: each biological modality occupies its own encoder track with localized positional encoding, and register tokens compress per-track representations into a shared global context used by a generative decoder. Training supports arbitrary subsets of observed modalities (modality dropout), allowing "any-to-any" inference: condition on any partial molecular state (e.g., DNA sequence + structure) and generate or reconstruct missing components. MIMIC achieves state-of-the-art (SOTA) RNA splicing prediction with isoform-aware generative inference, demonstrates constrained protein design by conditioning on binding-site geometry and surface chemistry, and supports assay-dependent RNA chemical probing via semantic/experimental context conditioning.

## Model

- **Architecture**: Split-track encoder-decoder Transformer (~1B parameters). Each modality (DNA/RNA sequence, protein sequence, protein structure, evolutionary profile, regulatory signals, natural-language context) has a dedicated encoder track with its own localized positional encoding.
- **Register-token compression**: A set of register tokens aggregate the per-track representations into a compact global molecular context, which is passed to the cross-attention layers of the generative decoder.
- **Decoder**: Autoregressive/generative decoder that reconstructs or generates missing components of the molecular state conditioned on the compressed multimodal context.
- **Context length**: Curriculum scaling during training from 1,000 up to 10,000 tokens.
- **Input modalities**: Nucleic acid sequence (DNA/RNA), protein sequence, protein 3D structure (geometric/surface), evolutionary signals (multiple sequence alignment features), regulatory annotations, and natural-language / experimental context.
- **Output**: Reconstruction or de novo generation of any unobserved modality sub-state (sequence, structure, etc.).

## Data

- **LORE dataset** (curated for this work): Aligns six modality types — nucleic acid sequence, protein sequence, evolutionary profiles, 3D structure, regulatory signals, and semantic/experimental context — into partially observed biomolecular state examples anchored at the transcript and protein level.
  - 13 million RNA transcripts
  - 15.5 million proteins
  - >4 billion natural-language tokens
  - >6,000 organisms represented
- **Downstream benchmarks**: RNA splicing prediction (SOTA vs prior DL models), protein structure and design (PD-L1 and hACE2 binding-site constrained design), RNA chemical probing (assay-dependent DMS/SHAPE modeling), and generic RNA/protein representation transfer tasks.

## Training Recipe

- **Objective**: Masked multimodal reconstruction — arbitrarily mask/drop one or more modality tracks and train the decoder to reconstruct them via cross-entropy on discrete tokens (sequence) or equivalent losses for structural/regulatory outputs.
- **Modality dropout**: At each training step, a random subset of modalities is observed; the model conditions on the observed subset and reconstructs the held-out modalities. This forces the model to learn shared representations across all modality combinations.
- **Curriculum context length**: Training starts with shorter context windows (~1k tokens) and progressively scales to ~10k tokens.
- **Positional encoding**: Localized per-track positional encoding (not global absolute positional encoding); this keeps within-track sequence order while being agnostic to how tracks are combined.
- **Register tokens**: Compress per-track encoder outputs into a fixed-size global context vector for efficient cross-attention in the decoder.

## Key Ablations & Design Choices

1. **Multimodal vs. sequence-only conditioning**: Providing additional modalities (structure, regulatory signals, evolutionary context) consistently improves sequence reconstruction accuracy over sequence-alone inputs. This is the core ablation validating the multimodal approach.
2. **Modality dropout generalization**: Graceful degradation — performance decreases as fewer modalities are provided at inference, but the model is robust and never collapses to random when one modality is absent. This contrasts with earlier multimodal models that require all modalities at inference.
3. **Isoform-aware generative inference for splicing**: Instead of single-label splice-site classification, MIMIC's generative formulation samples over isoform distributions, yielding additional performance gains over the discriminative baseline. This is a key design differentiation from SpliceAI-style models.
4. **Semantic conditioning for assay-dependent modeling**: Using natural-language or structured experimental context as a conditioning modality allows MIMIC to distinguish assay-dependent RNA chemical probing signals (e.g., DMS vs SHAPE at different MgCl₂ concentrations), rather than averaging over experimental variation — a design not present in prior RNA FMs.
5. **Split-track vs. single unified sequence**: Separate encoder tracks per modality (rather than concatenating all modalities into one sequence) allow localized positional encoding within each modality and better handling of modality-specific tokenizations.
6. **Clinical RNA editing design**: For the HBB splice-disrupting mutation, MIMIC uses evolutionary and structural signals to propose minimal corrective edits that restore splicing without reverting the original mutation — demonstrating that multimodal conditioning enables biologically constrained design beyond sequence-level optimization.

## Reported Insights

- Multimodal conditioning consistently and significantly outperforms sequence-only baselines on both reconstruction and downstream prediction tasks.
- MIMIC achieves SOTA on RNA splicing prediction; the isoform-aware generative inference further improves over standard discriminative splice prediction.
- The joint generative framework unifies representation learning, conditional prediction, and constrained design within a single model — a paradigm shift from task-specific fine-tuning of unimodal models.
- Protein design conditioned on binding-site shape and surface chemistry (PD-L1, hACE2) produces diverse sequences with strong in-silico binding support.
- Semantic/experimental context conditioning enables modeling of assay-dependent RNA structure probing.
- Modality dropout during training enables robust "any-to-any" inference at test time with arbitrary missing modalities.

## References Worth Chasing

1. **SpliceAI** (Jaganathan et al. 2019, Cell): Deep residual network for splice-site prediction; key baseline for MIMIC's splicing benchmark.
2. **Enformer** (Avsec et al. 2021, Nature Methods): Sequence-to-regulatory-signal model; complementary to MIMIC's regulatory track.
3. **ESM-2 / ESM3** (Lin et al. 2023; Hayes et al. 2024): Protein LMs; baselines for MIMIC's protein-sequence track.
4. **AlphaFold 2/3** (Jumper et al. 2021; Abramson et al. 2024): Protein structure prediction; relevant for MIMIC's structure conditioning track.
5. **RiNALMo** (Penić et al. 2024): Large RNA LM; comparison for MIMIC's RNA representation tasks.
6. **Evo** (Nguyen et al. 2024): DNA/genomic FM; related long-range genomic context modeling.
7. **Register tokens in ViT** (Darcet et al. 2023, arXiv:2309.16588): Conceptual source for register-token compression used in MIMIC.
8. **Polymathic AI** (McCabe et al. 2023): Multi-domain foundation model concept applied to physics; MIMIC extends this paradigm to biomolecules.

## Notes / Open Questions

- Code, model weights, and dataset preparation scripts are being prepared for public release (MIT license); not yet available as of April 2026.
- Affiliations: Polymathic AI, Flatiron Institute (Center for Computational Biology & Center for Computational Astrophysics), New York University, Princeton University, University of Cambridge, among others.
- No scaling experiments (parameter count variation) reported in the preprint; the ~1B model is the single released configuration.
- Training compute details not reported.
- The LORE dataset curation pipeline (alignment of heterogeneous modalities into partially observed molecular state examples) is a significant methodological contribution in itself; full details in the paper's Methods section.
- Potential limitation: conditioning on structure requires predicted or experimental structures, which may not be available for all genes/proteins at inference time; modality dropout training mitigates this.
- Link: https://arxiv.org/abs/2604.24506 | GitHub: https://github.com/PolymathicAI/MIMIC
