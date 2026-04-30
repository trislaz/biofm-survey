# Insights — Foundation Models for Biology (2026 Practitioner Refresh)

## Scope & Method

This guidebook distils design decisions and empirical findings from **86 biology foundation-model (bio-FM) papers** that meet a strict definition: pretrained on biological data at scale, learning a general-purpose representation transferable to multiple downstream tasks. **Rev 4** added 15 newly-extracted FMs (GET, Evo 2, ESM-3, AlphaFold 3, RoseTTAFold All-Atom, ProteinMPNN, Nicheformer, UCE, CellPLM, GenePT, SCimilarity, scMulan, AIDO, Virchow2, CONCH-NatMed); the 2026 practitioner refresh folds in newer DNA/RNA/multimodal evidence from JEPA-DNA, Orthrus, MIMIC, scELMo, and scMamba. The remaining 57 surveyed papers are supporting/baseline non-FMs (e.g., TAPE, scVI, totalVI, Cellpose, CLAM); these may appear as benchmarks but are **never** counted in the per-claim `(N=X papers)` evidence tallies that follow.

Each FM note in `notes/` carries a `## Ablations (Rev 4)` section that quotes the design-choice ablations actually reported by the authors. This guidebook is *grounded in those tables*: every design-choice axis below ends with an **Ablation evidence (Rev 4)** subsection that quotes the specific finding from the relevant note. Citations use `[short-name](URL)` linking to the source's DOI, arXiv, or canonical URL.

Coverage by modality (FM count, multi-label): protein-sequence 22, protein-structure 14, imaging-pathology 13, DNA 13, scRNA 12, multimodal 10, RNA 7, small-molecule 6, epigenome 4, single-cell-multiomics 3, plus low-count radiology, microscopy, cell-painting, biomedical text, vision, interactome, and other modalities. Methods reflect the ablations reported by authors and have not been independently reproduced; see *Methodology & Limitations*.

## Executive Summary — Top-12 Practitioner Take-aways (2026 refresh)

Each take-away is annotated with the number of **FM papers** that directly support it and the strongest single ablation cited. The update keeps mature, reproducible defaults where old FMs still win (AlphaFold 2/3, ESM-2, DNABERT-2, UNI/GigaPath) while promoting new FMs only where they change an actionable default.

1. **MSA-derived signal still dominates structure prediction; MSA-free models close the gap only for well-represented folds.** **(N=10 papers)** evidence: [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md)), [RoseTTAFold](https://doi.org/10.1126/science.abj8754) ([note](notes/accurate-prediction-of-protein-2021.md)), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)), [MSA Transformer](https://doi.org/10.1101/2021.02.12.430858) ([note](notes/msa-transformer-2021.md)), [HelixFold-Single](https://arxiv.org/abs/2207.13921) ([note](notes/helixfold-single-msa-free-2022.md)), [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) ([note](notes/high-resolution-de-novo-2022.md)), [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)), [ESM-1b](https://doi.org/10.1073/pnas.2016239118) ([note](notes/biological-structure-and-function-2021.md)), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)), [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md))

2. **For protein language models, scale unlocks emergent contact prediction; objective and tokenization matter less than parameter count past ~150M.** **(N=12 papers)** evidence: [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)), [ProtTrans](https://arxiv.org/abs/2007.06225) ([note](notes/prottrans-towards-cracking-the-2020.md)), [ESM-1b](https://doi.org/10.1073/pnas.2016239118) ([note](notes/biological-structure-and-function-2021.md)), [Rao attention-as-contacts](https://doi.org/10.1101/2020.12.15.422761) ([note](notes/transformer-protein-language-models-2021.md)), [Ankh](https://arxiv.org/abs/2301.06568) ([note](notes/ankh-optimized-protein-language-2023.md)), [ProGen](https://arxiv.org/abs/2004.03497) ([note](notes/progen-language-modeling-for-2020.md)), [ESM-1v](https://doi.org/10.1101/2021.07.09.450648) ([note](notes/language-models-enable-zero-2021.md)), [ProteinBERT](https://doi.org/10.1093/bioinformatics/btac020) ([note](notes/proteinbert-a-universal-deep.md)), [ProtGPT2](https://doi.org/10.1038/s41467-022-32007-7) ([note](notes/protgpt2-is-a-deep.md)), [ESM-design](https://doi.org/10.1101/2022.12.21.521521) ([note](notes/language-models-generalize-beyond-2022.md)), [ESM-AA](https://arxiv.org/abs/2403.12995) ([note](notes/esm-all-atom-multi-2024.md)), [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md))

3. **Long context is the sequence-modelling bottleneck; sub-quadratic backbones (Hyena, Mamba/state-space models, S4) match Transformers at 32k–1M tokens with 5–20× lower FLOPs, and now extend from DNA into RNA and single-cell.** **(N=10 papers)** evidence: [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)), [Caduceus](https://arxiv.org/abs/2403.03234) ([note](notes/caduceus-bi-directional-equivariant-2024.md)), [scMamba](https://arxiv.org/abs/2506.20697) ([note](notes/scmamba-a-scalable-foundation-2025.md)), [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)), [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md)), [Evo](https://doi.org/10.1126/science.ado9336) ([note](notes/sequence-modeling-and-design-2024.md)), [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)), [Enformer](https://doi.org/10.1038/s41592-021-01252-x) ([note](notes/effective-gene-expression-prediction-2021.md)), [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) ([note](notes/predicting-rna-seq-coverage-2023.md)), [dnaGrinder](https://arxiv.org/abs/2409.15697) ([note](notes/dnagrinder-a-lightweight-and-2024.md))

4. **Tokenisation and biological inductive bias often beat raw scale outside proteins: use BPE/vector-quantised DNA tokens when context is short, but prefer evolutionary/splicing contrastive RNA objectives or Joint-Embedding Predictive Architecture (JEPA)-style continual pretraining when labels are scarce.** **(N=8 papers)** evidence: [DNABERT-2](https://arxiv.org/abs/2306.15006) ([note](notes/dnabert-2-efficient-foundation-2023.md)), [DNABERT-1](https://doi.org/10.1093/bioinformatics/btab083) ([note](notes/dnabert-pre-trained-bidirectional-2021.md)), [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md)), [VQDNA](https://arxiv.org/abs/2405.10812) ([note](notes/vqdna-unleashing-the-power-2024.md)), [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)), [Genome Book](https://arxiv.org/abs/2501.16982) ([note](notes/human-genome-book-words-2025.md)), [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)), [JEPA-DNA](https://arxiv.org/abs/2602.17162) ([note](notes/jepa-dna-grounding-genomic-2026.md))

5. **Single-cell FMs benefit modestly from pretraining; gains over scVI shrink to 1–3% on integration once strong baselines are run, except for zero-shot perturbation/cross-tissue transfer where gains are 5–15%.** **(N=12 papers)** evidence: [scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md)), [scBERT](https://doi.org/10.1038/s42256-022-00534-z) ([note](notes/scbert-as-a-large-2022.md)), [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)), [scFoundation](https://doi.org/10.1038/s41592-024-02305-7) ([note](notes/large-scale-foundation-model-2024.md)), [CellPLM](https://doi.org/10.1101/2023.10.03.560734) ([note](notes/cellplm-pre-training-of-2023.md)), [UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md)), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md)), [GenePT](https://doi.org/10.1101/2023.10.16.562533) ([note](notes/genept-a-simple-but-2023.md)), [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)), [scMulan](https://doi.org/10.1101/2024.01.25.577152) ([note](notes/scmulan-a-multitask-generative-2024.md)), [scELMo](https://arxiv.org/abs/2601.05648) ([note](notes/open-world-knowledge-aided-2026.md)), [scMamba](https://arxiv.org/abs/2506.20697) ([note](notes/scmamba-a-scalable-foundation-2025.md))

6. **Pathology FMs scale with slide count, not parameter count; DINOv2-style SSL on 100k+ slides beats CLIP-style on 10× fewer.** **(N=11 papers)** evidence: [UNI](https://arxiv.org/abs/2308.15474) ([note](notes/a-general-purpose-self-2023.md)), [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md)), [Virchow](https://arxiv.org/abs/2309.07778) ([note](notes/virchow-a-million-slide-2023.md)), [Virchow2](https://arxiv.org/abs/2408.00738) ([note](notes/virchow2-scaling-self-supervised-2024.md)), [Phikon-v2](https://arxiv.org/abs/2409.09173) ([note](notes/phikon-v2-a-large-2024.md)), [RudolfV](https://arxiv.org/abs/2401.04079) ([note](notes/rudolfv-a-foundation-model-2024.md)), [H-optimus-0](https://arxiv.org/abs/2404.15217) ([note](notes/towards-large-scale-training-2024.md)), [HIPT](https://arxiv.org/abs/2206.02647) ([note](notes/scaling-vision-transformers-to-2022.md)), [CONCH (preprint)](https://arxiv.org/abs/2307.12914) ([note](notes/towards-a-visual-language-2023.md)), [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md)), [KEP (KEEP)](https://arxiv.org/abs/2412.13126) ([note](notes/knowledge-enhanced-pretraining-for-2024.md))

7. **Distilling from AlphaFold predictions gives 1–3 nm RMSD gains essentially for free; this is the cheapest known structure-prediction lever.** **(N=6 papers)** evidence: [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)), [HelixFold-Single](https://arxiv.org/abs/2207.13921) ([note](notes/helixfold-single-msa-free-2022.md)), [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) ([note](notes/high-resolution-de-novo-2022.md)), [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md)), [RhoFold](https://arxiv.org/abs/2207.01586) ([note](notes/accurate-rna-3d-structure-2022.md)), [GearNet](https://arxiv.org/abs/2203.06125) ([note](notes/protein-representation-learning-by-2022.md))

8. **For design, use generative models matched to the constraint: token diffusion / flow-matching for structure-conditioned proteins, and modality-dropout reconstruction for any-to-any biomolecular conditioning.** **(N=7 papers)** evidence: [ProteinMPNN](https://doi.org/10.1126/science.add2187) ([note](notes/robust-deep-learning-based-2022.md)), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)), [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)), [MIMIC](https://arxiv.org/abs/2604.24506) ([note](notes/mimic-a-generative-multimodal-2026.md)), [ESM-design](https://doi.org/10.1101/2022.12.21.521521) ([note](notes/language-models-generalize-beyond-2022.md)), [ProGen](https://arxiv.org/abs/2004.03497) ([note](notes/progen-language-modeling-for-2020.md)), [ESM-AA](https://arxiv.org/abs/2403.12995) ([note](notes/esm-all-atom-multi-2024.md))

9. **Multimodal alignment is task-specific: CLIP-style alignment helps zero-shot retrieval, adapter-style alignment helps free-form QA, and split-track generative alignment helps conditional prediction/design.** **(N=10 papers)** evidence: [CONCH (preprint)](https://arxiv.org/abs/2307.12914) ([note](notes/towards-a-visual-language-2023.md)), [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md)), [BiomedCLIP](https://arxiv.org/abs/2303.00915) ([note](notes/biomedclip-a-multimodal-biomedical-2023.md)), [ProtCLIP](https://arxiv.org/abs/2412.20014) ([note](notes/protclip-function-informed-protein-2024.md)), [MolFM](https://arxiv.org/abs/2307.09484) ([note](notes/molfm-a-multimodal-molecular-2023.md)), [ConceptCLIP](https://arxiv.org/abs/2501.15579) ([note](notes/an-explainable-biomedical-foundation-2025.md)), [KEP (KEEP)](https://arxiv.org/abs/2412.13126) ([note](notes/knowledge-enhanced-pretraining-for-2024.md)), [AIDO](https://doi.org/10.1101/2024.12.02.626322) ([note](notes/aido-accurate-model-of-2024.md)), [MIMIC](https://arxiv.org/abs/2604.24506) ([note](notes/mimic-a-generative-multimodal-2026.md)), [LLaVA-Med](https://arxiv.org/abs/2306.00890) ([note](notes/llava-med-training-a-2023.md))

10. **Geometry-aware backbones (SE(3)-equivariant attention, IPA, structure tokens) outperform sequence-only on structural tasks but only when paired with structure pretraining data.** **(N=9 papers)** evidence: [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md)), [RoseTTAFold](https://doi.org/10.1126/science.abj8754) ([note](notes/accurate-prediction-of-protein-2021.md)), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)), [GearNet](https://arxiv.org/abs/2203.06125) ([note](notes/protein-representation-learning-by-2022.md)), [PST](https://arxiv.org/abs/2401.14819) ([note](notes/endowing-protein-language-models-2024.md)), [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)), [ESM-AA](https://arxiv.org/abs/2403.12995) ([note](notes/esm-all-atom-multi-2024.md)), [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md))

11. **Conditioning on functional, spatial, evolutionary, or experimental metadata during pretraining is more parameter-efficient than post-hoc fine-tuning; treat metadata as a first-class modality, not a label file.** **(N=9 papers)** evidence: [ProGen](https://arxiv.org/abs/2004.03497) ([note](notes/progen-language-modeling-for-2020.md)), [ProtCLIP](https://arxiv.org/abs/2412.20014) ([note](notes/protclip-function-informed-protein-2024.md)), [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)), [MIMIC](https://arxiv.org/abs/2604.24506) ([note](notes/mimic-a-generative-multimodal-2026.md)), [scMulan](https://doi.org/10.1101/2024.01.25.577152) ([note](notes/scmulan-a-multitask-generative-2024.md)), [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)), [GET](https://doi.org/10.1038/s41586-024-08391-z) ([note](notes/a-foundation-model-of-2025.md)), [scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md)), [BioGPT](https://arxiv.org/abs/2210.10341) ([note](notes/biogpt-generative-pre-trained-2022.md))

12. **Benchmarks lag the field; many headline gains shrink ≥50% under leakage-corrected splits, fair-baseline reruns, or cross-lab data.** **(N=9 papers)** evidence: [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)), [scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md)), [scFoundation](https://doi.org/10.1038/s41592-024-02305-7) ([note](notes/large-scale-foundation-model-2024.md)), [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md)), [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md)), [ESM-1b](https://doi.org/10.1073/pnas.2016239118) ([note](notes/biological-structure-and-function-2021.md)), [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)), [CellPLM](https://doi.org/10.1101/2023.10.03.560734) ([note](notes/cellplm-pre-training-of-2023.md)), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md))

## Practitioner Cheatsheet (2026 refresh)

One-line defaults for the impatient. Each row links to the canonical FM(s) you should reach for first; see the design-choice axes and modality recipes below for the trade-offs.

| Modality | Default FM | Backbone | Pretraining | Strongest known ablation |
|---|---|---|---|---|
| DNA (short range) | [DNABERT-2](https://arxiv.org/abs/2306.15006) ([note](notes/dnabert-2-efficient-foundation-2023.md)) (+ [JEPA-DNA](https://arxiv.org/abs/2602.17162) ([note](notes/jepa-dna-grounding-genomic-2026.md)) for variant-effect continual pretraining) | Transformer | BPE MLM, multispecies; optional JEPA branch | BPE > 6-mer on 23/28 GUE; JEPA-DNA adds +3–7% zero-shot variant AUROC |
| DNA (long range) | [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)) / [Caduceus](https://arxiv.org/abs/2403.03234) ([note](notes/caduceus-bi-directional-equivariant-2024.md)) | Hyena / BiMamba | Char-level CLM/MLM | 1M-token context, RC-equivariance |
| DNA (frontier scale) | [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)) | StripedHyena | CLM, 8.8T tokens, 1M context | Scale-up; ablation table is configuration-only |
| Cell-type-conditional epigenome | [GET](https://doi.org/10.1038/s41586-024-08391-z) ([note](notes/a-foundation-model-of-2025.md)) | Region-wise transformer | Motif-masked SSL | Pretraining lifts cross-cell-type r 0.60→0.94 |
| Gene expression from DNA | [Enformer](https://doi.org/10.1038/s41592-021-01252-x) ([note](notes/effective-gene-expression-prediction-2021.md)) / [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) ([note](notes/predicting-rna-seq-coverage-2023.md)) | CNN+Transformer | Supervised on tracks | 196kb→524kb gives small Pearson lift |
| RNA representation | [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)) / [RiNALMo](https://arxiv.org/abs/2403.00043) ([note](notes/rinalmo-general-purpose-rna-2024.md)) | Mamba contrastive / Transformer MLM | Mature mRNA orthology+splicing / ncRNA+mRNA | Orthrus contrastive learning (CL) Z-score 0.90 vs MLM 0.71; RiNALMo scale improves 8/9 RNA tasks |
| Protein representation | [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) | Transformer MLM | UR50, 8M→15B | Contact P@L 0.34→0.54 with scale |
| Protein design (multimodal) | [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)) | Transformer | Joint seq/struct/func tokens | Ablating any track loses 8–20% recovery |
| Protein structure (monomer) | [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md)) | Evoformer + IPA | MSA + distillation | MSA depth dominant; ablating drops 25–40 GDT |
| Protein structure (complex) | [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)) / [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)) | Diffusion / SE(3) | Seq+struct+ligand | All-atom necessary for heteroatom |
| MSA-free / orphan proteins | [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) (ESMFold) / [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) ([note](notes/high-resolution-de-novo-2022.md)) | Folding head | AF2 distillation | Closes ~80% of MSA gap |
| Inverse folding | [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md)) / [ProteinMPNN](https://doi.org/10.1126/science.add2187) ([note](notes/robust-deep-learning-based-2022.md)) | GVP-GNN / MPNN | Seq-given-struct | Native recovery 51% (ESM-IF), 52% (MPNN) |
| Single-cell RNA (representation) | [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)) / [scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md)) | Transformer | Rank/binned MLM | Scale 1M→30M cells lifts dosage AUROC 3–6 pts |
| Single-cell RNA (zero-shot annotation) | [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md)) / [GenePT](https://doi.org/10.1101/2023.10.16.562533) ([note](notes/genept-a-simple-but-2023.md)) | NN + reference / Text emb. | Reference search / GPT-3.5 | GenePT matches scGPT at 0% pretraining cost |
| Spatial transcriptomics | [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)) | Transformer | Niche-conditional MLM | +4–7 pts over vanilla MLM on niche tasks |
| Cell-type integration cross-species | [UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md)) | Transformer | 36M cells, multi-species | Cross-species zero-shot annotation |
| Single-cell multiomics at scale | [scMamba](https://arxiv.org/abs/2506.20697) ([note](notes/scmamba-a-scalable-foundation-2025.md)) / [scELMo](https://arxiv.org/abs/2601.05648) ([note](notes/open-world-knowledge-aided-2026.md)) | Mamba / knowledge-aided Transformer | Raw genes+peaks / open-world gene knowledge | scMamba scales to 50M cells where scGPT runs out of memory |
| Pathology (image) | [UNI](https://arxiv.org/abs/2308.15474) ([note](notes/a-general-purpose-self-2023.md)) / [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md)) | ViT-L/16 + DINOv2 / LongNet | SSL on 100k+ slides | Slide diversity > slide count |
| Pathology (image+text) | [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md)) | ViT + text encoder | CLIP, 1.17M slide-caption | Wins 12/14 zero-shot pathology |
| Pathology (mixed magnification) | [Virchow2](https://arxiv.org/abs/2408.00738) ([note](notes/virchow2-scaling-self-supervised-2024.md)) | ViT-G + DINOv2 | Mixed 5×–40× tiles | +2–5 pts vs single-mag |
| Cell painting | [CellPainTR](https://arxiv.org/abs/2509.06986) ([note](notes/cellpaintr-generalizable-representation-learning-2025.md)) / [ViTally](https://arxiv.org/abs/2411.02572) ([note](notes/vitally-consistent-scaling-biological-2024.md)) | ViT + DINOv2/MAE | Multi-channel SSL | Channel-mixing aug critical |
| Mass-spec proteomics | [LSM-MS2](https://arxiv.org/abs/2510.26715) ([note](notes/lsm-ms2-a-foundation-2025.md)) | Transformer | MS2 spectra MLM | Single FM in corpus |
| Multimodal medical (QA) | [LLaVA-Med](https://arxiv.org/abs/2306.00890) ([note](notes/llava-med-training-a-2023.md)) | LLaMA + CLIP adapter | Instruction tuning, 600k pairs | Adapter unlocks free-form QA |
| Small molecules (representation) | [ChemFM](https://arxiv.org/abs/2410.21422) ([note](notes/chemfm-as-a-scaling-2024.md)) / [ChemBERTa](https://arxiv.org/abs/2010.09885) ([note](notes/chemberta-large-scale-self-2020.md)) | Transformer | SMILES MLM/CLM | Scale-up monotonic on MoleculeNet |
| Small molecules (multimodal) | [MolFM](https://arxiv.org/abs/2307.09484) ([note](notes/molfm-a-multimodal-molecular-2023.md)) | Tri-encoder | Mol+text+graph contrastive | Beats unimodal on 8/10 MoleculeNet |
| ML force fields | [MACE-OFF / Multi-Fi](https://arxiv.org/abs/2412.13088) ([note](notes/taming-multi-domain-fidelity-2024.md)) | MACE-OFF | Multi-fidelity training | Multi-fidelity improves transfer |
| Cross-omics unified | [MIMIC](https://arxiv.org/abs/2604.24506) ([note](notes/mimic-a-generative-multimodal-2026.md)) / [AIDO](https://doi.org/10.1101/2024.12.02.626322) ([note](notes/aido-accurate-model-of-2024.md)) / [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)) | Split-track encoder-decoder / modular hub / Transformer | Modality-dropout reconstruction + per-module alignment | Multimodal conditioning beats sequence-only; shared rep enables cross-modal transfer |

## Design-Choice Axes

Twelve recurring decisions shape every bio-FM. For each axis we summarise the trade-offs and then quote the directly relevant **Rev 4 ablations** from the source notes.

### 1. Tokenization & Vocabulary

DNA models span character-level (HyenaDNA, Caduceus), fixed k-mer (DNABERT-1), learned BPE (DNABERT-2, NT-v2), and codebook (VQDNA). Protein models are almost universally amino-acid level (20–30 token vocabularies); the exceptions add structure tokens (ESM-3, ESM-AA, FoldSeek) or atomic tokens (RFAA). Single-cell models span gene-as-token (Geneformer, scGPT), bin-as-token (scBERT, scFoundation), and gene-text-as-token (GenePT). Pathology and microscopy use ViT patches with no language-style vocabulary.

**Empirical pattern:** vocabulary changes alter sequence length and FLOP budget more than they alter accuracy, with two notable exceptions — DNABERT-2's BPE doubles many GUE scores vs. fixed 6-mer, and ESM-3's structure-token addition unlocks joint sequence/structure generation impossible with sequence-only.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [DNABERT-2](https://arxiv.org/abs/2306.15006) ([note](notes/dnabert-2-efficient-foundation-2023.md)) | BPE on the multi-species genome (~32k merges) compresses tokens 5× vs. 6-mer and improves 23/28 GUE tasks; the gain is largest on long-range tasks where 6-mer hits the 512-token limit. |
| [DNABERT-1](https://doi.org/10.1093/bioinformatics/btab083) ([note](notes/dnabert-pre-trained-bidirectional-2021.md)) | Sweep over k∈{3,4,5,6} shows k=6 best for promoter and TF-binding; smaller k under-fits motif structure, larger k explodes vocabulary. |
| [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md)) | Ablating from non-overlapping 6-mer to BPE on multispecies corpus improves 13/18 BEND tasks; effect is larger than 10× parameter scaling on the same corpus. |
| [VQDNA](https://arxiv.org/abs/2405.10812) ([note](notes/vqdna-unleashing-the-power-2024.md)) | Learned VQ codebook of 4096 entries beats fixed 6-mer on 22/28 GUE tasks; codebook collapse mitigated via EMA reset. |
| [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)) | Single-nucleotide (character-level) tokenization is the only choice that scales to 1M-token context with sub-quadratic Hyena ops; k-mer would blow vocabulary or context budget. |
| [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)) | Adding 4096 structure tokens (VQ over local SE(3) frames) to amino-acid vocabulary enables joint sequence/structure generation; ablating structure tokens drops cross-modal generation by >40 TM-score points. |
| [ESM-AA](https://arxiv.org/abs/2403.12995) ([note](notes/esm-all-atom-multi-2024.md)) | Multi-scale tokenization (residue + atom) outperforms residue-only on small-molecule binding prediction by 5–8 AUROC; pure atom-only loses long-range protein information. |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)) | Rank-encoding (Geneformer) of expression eliminates batch-normalisation dependence; switching to log-CPM tokens loses 3–5 points on perturbation prediction. |
| [scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md)) | Binned expression tokens with gene IDs outperform Geneformer-style rank tokens on perturbation tasks (+2.4 Pearson) but hurt zero-shot integration. |
| [GenePT](https://doi.org/10.1101/2023.10.16.562533) ([note](notes/genept-a-simple-but-2023.md)) | Replacing learned gene embeddings with frozen GPT-3.5 text embeddings of NCBI gene summaries matches scGPT on 8/10 cell-type tasks at 0% pretraining cost. |

### 2. Architecture Family

Transformers dominate, but four sub-quadratic alternatives have proven competitive in 2023–2025: Hyena (HyenaDNA, Evo, Evo 2), Mamba/SSM (Caduceus, scMamba), striped/hybrid (Borzoi, Enformer = CNN+Transformer), and SE(3)-equivariant (AlphaFold 2/3, RoseTTAFold/AA, GearNet, ESM-IF). Diffusion/flow-matching now appears in design heads (RFAA, AF3, ProteinMPNN-flow, ESM-3).

**Empirical pattern:** at fixed parameter count, sub-quadratic models match Transformers on per-token loss but win on >32k-token throughput; equivariant models dominate structural tasks but underperform on pure sequence tasks; diffusion heads beat AR heads on inverse folding at higher temperatures.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)) | Hyena replaces self-attention with implicit long convolutions; matches Transformer perplexity at 2× speed and 5× memory savings, enabling 1M-token context. |
| [Caduceus](https://arxiv.org/abs/2403.03234) ([note](notes/caduceus-bi-directional-equivariant-2024.md)) | Bi-directional Mamba (BiMamba) with reverse-complement equivariance outperforms NT and HyenaDNA on 6/8 long-range Genomic Benchmarks at ≤0.5× FLOPs. |
| [scMamba](https://arxiv.org/abs/2506.20697) ([note](notes/scmamba-a-scalable-foundation-2025.md)) | Mamba SSM scales to 50M cells where scGPT OOMs at 1M; per-cell attention proxy via SSM kernel matches scGPT on annotation at 3× lower memory. |
| [Evo](https://doi.org/10.1126/science.ado9336) ([note](notes/sequence-modeling-and-design-2024.md)) | Evo (StripedHyena, 7B) ablation shows Hyena layers are necessary at 131k context; pure Transformer baseline diverges past 8k. |
| [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)) | Evo 2 (40B) confirms StripedHyena scales; configuration-only ablation (no head-to-head accuracy comparison published). |
| [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md)) | Evoformer + IPA: removing IPA drops GDT-TS by 4–7 points on CASP14; removing recycling drops it 3–5; FAPE loss is necessary for sub-Å backbone accuracy. |
| [RoseTTAFold](https://doi.org/10.1126/science.abj8754) ([note](notes/accurate-prediction-of-protein-2021.md)) | RoseTTAFold three-track: ablating any one track (1D/2D/3D) drops TM-score 4–9; full three-track is necessary. |
| [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)) | AF3 replaces Evoformer's structure module with a diffusion head; recovery accuracy on protein-only matches AF2-multimer while extending to nucleic-acid and small-molecule complexes. |
| [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)) | RFAA's all-atom track is necessary for heteroatom complexes; ablating to residue-only drops protein-NA contact accuracy by 18–25%. |
| [Enformer](https://doi.org/10.1038/s41592-021-01252-x) ([note](notes/effective-gene-expression-prediction-2021.md)) | Enformer's CNN+Transformer hybrid outperforms pure Transformer on 196k-bp expression prediction; ablating attention drops mean Pearson by 0.10. |
| [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) ([note](notes/predicting-rna-seq-coverage-2023.md)) | Borzoi (CNN+UNet+Transformer) at 524k bp matches Enformer Pearson at 2× context; ablating UNet skip drops fine-grained track resolution. |
| [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)) | Mamba (10.1M) outperforms matched CNN-RNN (Saluki-like) and dilated CNN on aggregate mRNA property Z-score by +1.13 and +1.43 respectively; linear memory scaling enables long mature RNA handling. |

### 3. Pretraining Objective

Masked language modeling (BERT-style, 15% mask) remains the default for sequence FMs; causal LM appears in generative FMs (ProGen, ProtGPT2, Evo, BioGPT, scMulan). Contrastive objectives dominate vision/multimodal (CLIP variants, DINOv2 for pathology) and now also RNA (Orthrus). Inverse-folding and structure-conditioned objectives (ESM-IF, ProteinMPNN, RFAA, AF3) train sequence given structure or vice versa. Recent additions: span-corruption (Ankh), JEPA-style (JEPA-DNA), structure-token autoregression (ESM-3), niche-conditional masking (Nicheformer), contrastive with biological augmentations (Orthrus), **modality-dropout generative reconstruction** — condition on any observed subset of modalities and reconstruct the rest (MIMIC).

**Empirical pattern:** for representation quality on classification/regression, MLM and contrastive perform within 1–2 points on protein, but contrastive with biological augmentations significantly outperforms MLM on RNA (Orthrus: CL Z-score 0.90 vs MLM 0.71); for generation, AR or diffusion are necessary; for cross-modal alignment, CLIP-style with hard negatives dominates; for unified representation+generation across many modalities, modality-dropout reconstruction (MIMIC) enables any-to-any inference without task-specific fine-tuning.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) | ESM-2 vs ESM-1b (same MLM objective, different scale): contact precision long-range P@L jumps from 0.34 (650M) to 0.54 (15B), confirming scale > objective. |
| [Ankh](https://arxiv.org/abs/2301.06568) ([note](notes/ankh-optimized-protein-language-2023.md)) | Span corruption with 1% noise + 3-token spans beats 15% MLM by 1–3% on 10/11 TAPE tasks at 1/4 the params. |
| [Rao attention-as-contacts](https://doi.org/10.1101/2020.12.15.422761) ([note](notes/transformer-protein-language-models-2021.md)) | Attention heads in MLM-trained ESM-1b directly encode contacts (precision 0.50+ P@L for several heads); no contact-supervision needed. |
| [ProGen](https://arxiv.org/abs/2004.03497) ([note](notes/progen-language-modeling-for-2020.md)) | Causal LM on 280M sequences with control tokens (taxonomy, function) generates synthetic enzymes that fold and function in vitro; ablating control tokens halves activity. |
| [ESM-1v](https://doi.org/10.1101/2021.07.09.450648) ([note](notes/language-models-enable-zero-2021.md)) | ESM-1v zero-shot variant effect: pseudo-likelihood from MLM correlates 0.4–0.6 with deep mutational scan fitness across 41 datasets — no supervised fine-tuning. |
| [ESM-design](https://doi.org/10.1101/2022.12.21.521521) ([note](notes/language-models-generalize-beyond-2022.md)) | ESM-IF (inverse folding objective) generalises to designed proteins absent from training; native-sequence recovery 51%. |
| [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)) | ESM-3 multimodal masked-token objective over (sequence, structure, function) tokens enables prompted generation; ablating any single track drops cross-track recovery by 8–20%. |
| [ProteinMPNN](https://doi.org/10.1126/science.add2187) ([note](notes/robust-deep-learning-based-2022.md)) | ProteinMPNN's autoregressive sequence-given-structure objective beats Rosetta on native recovery (52% vs 33%) and produces sequences that fold in silico. |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)) | Geneformer's masked-rank objective (15%) on 30M cells transfers zero-shot to dosage sensitivity prediction (AUROC 0.89); ablating to 5% mask drops by 0.04. |
| [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)) | Niche-conditional masking (mask out neighbours, predict from cell + niche label) beats vanilla MLM by 4–7 points on spatial niche classification. |
| [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md)) | CONCH (NatMed) image-text contrastive on 1.17M slide-caption pairs outperforms image-only DINO baselines on 12/14 zero-shot pathology benchmarks. |
| [ConceptCLIP](https://arxiv.org/abs/2501.15579) ([note](notes/an-explainable-biomedical-foundation-2025.md)) | ConceptCLIP adds concept-token alignment on top of CLIP loss; improves zero-shot retrieval +5–8 points on biomedical concept matching. |
| [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)) | Contrastive learning with biological augmentations (splice isoforms + 400+ mammalian orthologs) beats MLM on aggregate mRNA property Z-score (0.90 vs 0.71); joint CL+MLM gives best result. Removing orthology augmentation drops Z-score by 0.11; masking-only drops by 0.55. |
| [MIMIC](https://arxiv.org/abs/2604.24506) ([note](notes/mimic-a-generative-multimodal-2026.md)) | Modality-dropout generative reconstruction (condition on any subset of 6 modalities, reconstruct held-out ones): multimodal conditioning consistently outperforms sequence-only reconstruction; isoform-aware generative inference beats discriminative splice prediction. Demonstrates that a single generative objective over partially-observed multimodal inputs can unify representation learning, prediction, and design. |

### 4. Context Length

Context budgets span 512 (DNABERT-1, scBERT) → 2k (ESM-2, ProtTrans) → 32k (NT-v2, AF2 crops) → 131k (Evo) → 524k (Borzoi) → 1M (Evo 2, HyenaDNA) tokens. Long context matters most for genomics (regulatory range >100kb), pathology (whole-slide tiling), and single-cell (cell × gene matrices >20k genes).

**Empirical pattern:** most regulatory effects sit within 100kb; gains from 100kb→1M are real but small (≤0.05 Pearson on Enformer-style tracks). For protein structure, AF2 crop sizes (256 residues) suffice for monomers; AF3/RFAA need full-complex context. For single-cell, the bottleneck is gene count (~20k), not depth.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)) | Single 1M-token context model outperforms 32k baseline on long-range species classification by 6–11 points. |
| [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md)) | Sweep 1k → 32k context on multispecies pretraining: 32k > 1k by 2–6 points on regulatory tasks; gains plateau past 32k for the BEND benchmark. |
| [Enformer](https://doi.org/10.1038/s41592-021-01252-x) ([note](notes/effective-gene-expression-prediction-2021.md)) | Enformer's 196k-bp window is necessary for distal-enhancer effects; ablating to 100kb drops Pearson by 0.05. |
| [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) ([note](notes/predicting-rna-seq-coverage-2023.md)) | Borzoi at 524kb beats Enformer at 196kb by Pearson +0.02 on RNA-seq coverage; gains saturate beyond 524kb. |
| [Evo](https://doi.org/10.1126/science.ado9336) ([note](notes/sequence-modeling-and-design-2024.md)) | Evo trained at 131k tokens predicts 30k-bp prokaryotic operons end-to-end; ablating to 8k context destroys cross-gene coordination. |
| [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)) | Evo 2 trained at 1M context; configuration only — no published context-ablation accuracy delta. |
| [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md)) | AF2 256-residue crops cover full domain context for >90% of CASP14 monomers; recycling 3× provides additional implicit context. |

### 5. Data: Scale, Quality, Diversity

Training sets span: protein UniRef50/90 (~50M–250M sequences), MGnify/BFD (>1B), nucleotide multispecies (~3T bp for NT, 8.8T for Evo 2), single-cell (CELLxGENE 30–50M cells), pathology (10k–500k slides). Diversity > raw size: clustering UniRef at 50% identity, multispecies vs single-genome, and lab/site-stratified slides all give larger gains than 10× more sequences from the same distribution.

**Empirical pattern:** redundancy hurts; clustering at 30–50% identity reliably beats unfiltered. For pathology, slide diversity (number of medical centres) outperforms slide count from a single centre. For single-cell, tissue/disease coverage matters more than cell count past ~10M.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) | UR50 vs UR90 vs UR100: UR50 (clustered) gives best contact precision per parameter; raw UR100 wastes capacity on near-duplicates. |
| [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md)) | Multispecies (850 species) > human-only on 16/18 BEND tasks; cross-species pretraining acts as evolutionary regularisation. |
| [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md)) | GigaPath: 171k slides from 28 centres; ablating to single-centre 50k slides drops linear-probe accuracy 4–9% across PCAM, BACH, and MHIST. |
| [UNI](https://arxiv.org/abs/2308.15474) ([note](notes/a-general-purpose-self-2023.md)) | UNI: 100k slides DINOv2 outperforms 1M slides supervised; the data-quality bound dominates. |
| [Virchow](https://arxiv.org/abs/2309.07778) ([note](notes/virchow-a-million-slide-2023.md)) | Virchow on 1.5M slides + DINOv2 sets pan-cancer state-of-the-art (SOTA); ablating to 100k slides drops by 2–4 points on 9-class subtyping. |
| [Virchow2](https://arxiv.org/abs/2408.00738) ([note](notes/virchow2-scaling-self-supervised-2024.md)) | Mixed-magnification training (5×, 10×, 20×, 40× tiles) yields 2–5 pt gain over single-magnification at 20×; KDE-based stain-aug ablation isolates the magnification mix as the largest single contributor. |
| [Phikon-v2](https://arxiv.org/abs/2409.09173) ([note](notes/phikon-v2-a-large-2024.md)) | Phikon-v2 doubles slide count vs Phikon and adds clinical metadata; gains are 1–3% on pan-cancer linear probe — sublinear in data. |
| [RudolfV](https://arxiv.org/abs/2401.04079) ([note](notes/rudolfv-a-foundation-model-2024.md)) | RudolfV: stain-augmentation + multi-stain pretraining adds 2–4 points on cross-stain transfer that single-stain DINOv2 misses. |
| [H-optimus-0](https://arxiv.org/abs/2404.15217) ([note](notes/towards-large-scale-training-2024.md)) | H-optimus-0: 500k slides confirms diminishing returns past 200k slides on standard CPath benchmarks (<1% delta). |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)) | Geneformer: scaling 1M → 30M cells gives 3–6 point boost on dosage sensitivity; tissue diversity (296 → 561 tissues) gives a further 2–4 points. |
| [UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md)) | UCE on 36M cells across 1000+ studies; cross-species pretraining (mouse + human) enables zero-shot annotation in unseen species (full-text 403; relies on author claims). |
| [MIMIC](https://arxiv.org/abs/2604.24506) ([note](notes/mimic-a-generative-multimodal-2026.md)) | LORE dataset: curated alignment of 6 modalities (nucleic acid sequence, protein sequence, 3D structure, evolutionary profiles, regulatory signals, NL context) across 6,000+ organisms (13M RNA transcripts, 15.5M proteins, >4B NL tokens). Cross-organism, cross-modality alignment enables multimodal conditioning that consistently improves over single-modality baselines; demonstrates that curated multimodal alignment across diverse organisms is feasible and effective at scale. |

### 6. Multi-Modal Fusion

Bio-FMs fuse modalities five ways: (i) **early fusion** of token streams (ESM-3, ESM-AA, RFAA, AF3, MIRROR-3D); (ii) **CLIP-style alignment** of unimodal encoders (CONCH, BiomedCLIP, ProtCLIP, MolFM, KEEP); (iii) **adapter-style** instruction tuning of an LLM with a vision encoder (LLaVA-Med, XrayGPT, Doctor Sun, MedMax); (iv) **knowledge fusion** with text embeddings of structured concepts (GenePT, ConceptCLIP, KEEP); (v) **split-track generative encoder-decoder with modality dropout** for any-to-any inference (MIMIC).

**Empirical pattern:** early fusion wins when modalities are tightly coupled (sequence↔structure); CLIP wins for retrieval; adapter-LLM wins for free-form QA; knowledge fusion wins when labelled multimodal data is scarce; split-track generative models (MIMIC) enable any-to-any inference and constrained design across the full biomolecular spectrum.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)) | Joint masked sequence+structure+function tokens (ESM-3) outperform sequence-only ESM-2 by 5–10 TM-score points on structure recovery and unlock prompted design. |
| [ESM-AA](https://arxiv.org/abs/2403.12995) ([note](notes/esm-all-atom-multi-2024.md)) | Residue+atom early fusion beats CLIP-style residue↔ligand alignment by 3–6 AUROC on protein-ligand binding. |
| [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)) | AF3 unifies protein, NA, and small-molecule into one diffusion head; per-task heads underperform by 5–12% on cross-modal complexes. |
| [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)) | RFAA all-atom track lifts protein-NA interface accuracy 18–25% over residue-only baselines. |
| [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md)) | CONCH NatMed: contrastive image-text on 1.17M pairs beats image-only DINO on 12/14 zero-shot pathology benchmarks; ablating text alignment loses retrieval almost entirely. |
| [KEP (KEEP)](https://arxiv.org/abs/2412.13126) ([note](notes/knowledge-enhanced-pretraining-for-2024.md)) | KEEP injects structured knowledge graph into CLIP loss; +3–5 zero-shot retrieval, +1–2 supervised. |
| [BiomedCLIP](https://arxiv.org/abs/2303.00915) ([note](notes/biomedclip-a-multimodal-biomedical-2023.md)) | PMC-15M scale CLIP outperforms ImageNet-CLIP on 22/24 biomedical benchmarks; the data scale is the dominant factor. |
| [ProtCLIP](https://arxiv.org/abs/2412.20014) ([note](notes/protclip-function-informed-protein-2024.md)) | Function-informed contrastive loss (sequence ↔ GO term text) beats plain MLM ESM-2 on 9/12 function-prediction tasks at fixed parameter count. |
| [MolFM](https://arxiv.org/abs/2307.09484) ([note](notes/molfm-a-multimodal-molecular-2023.md)) | Tri-modal molecule-text-graph contrastive beats unimodal SMILES BERT on 8/10 MoleculeNet tasks; KG triples in pretraining add another 2–3 points. |
| [AIDO](https://doi.org/10.1101/2024.12.02.626322) ([note](notes/aido-accurate-model-of-2024.md)) | AIDO multi-omics modules (DNA+RNA+protein+cell) interoperate via shared representation hub; each module's ablations live in its per-modality preprint. |
| [MIRROR-3D](https://arxiv.org/abs/2504.09060) ([note](notes/multimodal-3d-genome-pre-2025.md)) | MIRROR-3D fuses Hi-C contact maps with sequence; sequence-only ablation loses 3D contact prediction entirely. |
| [ConceptCLIP](https://arxiv.org/abs/2501.15579) ([note](notes/an-explainable-biomedical-foundation-2025.md)) | ConceptCLIP concept-token alignment on top of CLIP yields +5–8 zero-shot retrieval and produces explainable concept attributions. |
| [LLaVA-Med](https://arxiv.org/abs/2306.00890) ([note](notes/llava-med-training-a-2023.md)) | LLaVA-Med adapter on top of frozen LLaMA + CLIP; instruction tuning on 600k biomedical image-text pairs unlocks free-form QA missing from CLIP-only baselines. |
| [MIMIC](https://arxiv.org/abs/2604.24506) ([note](notes/mimic-a-generative-multimodal-2026.md)) | Split-track encoder-decoder with modality dropout (MIMIC): multimodal conditioning (sequence + structure + evolutionary + regulatory) consistently outperforms sequence-only reconstruction; isoform-aware generative inference improves RNA splicing SOTA beyond discriminative baselines. |

### 7. Conditioning & Inductive Biases

Conditioning at pretraining (control tokens, label conditioning, niche conditioning, knowledge graphs) is consistently more efficient than post-hoc fine-tuning. Inductive biases (equivariance, reverse-complement symmetry, periodic position encoding) reduce sample complexity proportionally.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ProGen](https://arxiv.org/abs/2004.03497) ([note](notes/progen-language-modeling-for-2020.md)) | Causal LM with taxonomic + functional control tokens generates active synthetic enzymes; ablating control tokens halves in-vitro activity rate. |
| [scMulan](https://doi.org/10.1101/2024.01.25.577152) ([note](notes/scmulan-a-multitask-generative-2024.md)) | Multi-task control-token training across 10 single-cell tasks; no published head-to-head ablation table (bioRxiv full text 403) — supporting only. |
| [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)) | Niche-label conditioning improves spatial niche classification by 4–7 points over vanilla MLM; tissue-token gives a further +2. |
| [Caduceus](https://arxiv.org/abs/2403.03234) ([note](notes/caduceus-bi-directional-equivariant-2024.md)) | Hard-coded reverse-complement equivariance halves effective parameters and improves Genomic Benchmarks by 1–3 points. |
| [GET](https://doi.org/10.1038/s41586-024-08391-z) ([note](notes/a-foundation-model-of-2025.md)) | GET conditions on cell-type label + chromatin accessibility; ablating cell-type token loses 8–14 points on cross-tissue gene-expression prediction. |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)) | Geneformer rank encoding implicitly conditions on cell-state without external metadata; replacing with raw counts hurts batch-robust transfer. |
| [BioGPT](https://arxiv.org/abs/2210.10341) ([note](notes/biogpt-generative-pre-trained-2022.md)) | Domain-conditioned causal LM beats general-purpose GPT-2 fine-tuned on biomedical NLP by 2–5 F1 across 6 tasks. |
| [ProtCLIP](https://arxiv.org/abs/2412.20014) ([note](notes/protclip-function-informed-protein-2024.md)) | GO-term conditioning at pretraining beats post-hoc GO classifier on top of frozen ESM-2 by 3–7 F1 across 12 function tasks. |
| [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)) | Biological augmentations (splice isoforms + cross-species orthologs) as contrastive pairs outperform sequence-level augmentations (masking only) by Z-score +0.55; evolutionary conservation as inductive bias > reconstruction. |
| [MIMIC](https://arxiv.org/abs/2604.24506) ([note](notes/mimic-a-generative-multimodal-2026.md)) | Experimental/semantic context as a conditioning modality (MIMIC): using natural-language experimental context (e.g., DMS vs SHAPE, MgCl₂ concentration) as a condition enables assay-dependent RNA chemical probing predictions, rather than collapsing to an average over experimental variation — a design not present in prior RNA FMs. Demonstrates that free-form semantic/experimental metadata can function as a first-class conditioning modality. |

### 8. Optimization & Schedule

Standard recipe: AdamW, β=(0.9, 0.95–0.98), weight decay 0.01–0.1, cosine schedule with 1–10% warmup. Bio-FMs rarely innovate here; the few that do (Ankh, Caduceus) tune for sample efficiency rather than peak. Mixed precision (bf16) is universal post-2022. Long-context training requires gradient checkpointing or FlashAttention/Flash-SSM kernels.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [Ankh](https://arxiv.org/abs/2301.06568) ([note](notes/ankh-optimized-protein-language-2023.md)) | T5-style relative position + 1% noise span corruption + bf16 = 4× lower compute than ESM-2 at matched downstream accuracy. |
| [Caduceus](https://arxiv.org/abs/2403.03234) ([note](notes/caduceus-bi-directional-equivariant-2024.md)) | Mamba's selective SSM kernels enable 1M-bp training on 8×A100 where Transformer baselines OOM at 65k. |
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) | ESM-2 15B trained with FSDP + bf16 + gradient checkpointing on 4096 V100; ablating to fp32 doubles wall time with no accuracy gain. |
| [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)) | Single GPU 1M-token training via Hyena's FFT-conv kernel; ablating to attention requires 100× more memory. |

### 9. Scaling & Compute Efficiency

Scaling laws hold within bio-FMs but with smaller exponents than text LMs. ESM-2 reports clean scaling 8M → 15B; AlphaFold 3 and Evo 2 confirm scale-up but with diminishing returns past task-specific saturation points. Compute efficiency is dominated by sub-quadratic backbones (genomics) and DINOv2 distillation (pathology).

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) | Loss scales as power law in params 8M → 15B; downstream contact precision saturates near 3B for many tasks but improves to 15B for the hardest. |
| [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md)) | GigaPath: ViT-G/14 (1.1B) outperforms ViT-L/14 (300M) by 1–3% averaged across 26 benchmarks; gains are sublinear past 300M. |
| [UNI](https://arxiv.org/abs/2308.15474) ([note](notes/a-general-purpose-self-2023.md)) | UNI: ViT-L/16 + DINOv2 outperforms ViT-G + supervised; SSL is the binding constraint, not scale. |
| [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)) | Evo 2 (40B, 8.8T tokens) demonstrates configuration scale-up; published metrics are configuration-only, no head-to-head accuracy ablation accessible. |
| [Evo](https://doi.org/10.1126/science.ado9336) ([note](notes/sequence-modeling-and-design-2024.md)) | Evo 7B at 131k context is compute-optimal for prokaryotic genome modelling; smaller variants under-fit, larger explore-only have not been head-to-head benchmarked. |
| [HIPT](https://arxiv.org/abs/2206.02647) ([note](notes/scaling-vision-transformers-to-2022.md)) | HIPT hierarchical scaling: cell-level + region-level + slide-level transformers; ablating any tier drops survival prediction C-index by 0.02–0.05. |
| [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)) | ESM-3 1.4B → 98B sweep: structure-recovery accuracy scales smoothly; design quality saturates earlier than recovery accuracy. |
| [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)) | Orthrus (10.1M params) matches or outperforms Evo 2 (7B) on 7 mRNA property tasks via contrastive pretraining with biological augmentations — 700× fewer parameters; biological inductive bias > raw scale for RNA. |

### 10. MSA vs MSA-Free Structure Prediction

MSA-conditioned models (AF2, RoseTTAFold, AF3, MSA Transformer) remain SOTA for hard targets. MSA-free models (ESMFold, OmegaFold, HelixFold-Single, RhoFold) trade 5–15 GDT-TS / TM-score points for 10–100× faster inference and applicability to designed/synthetic proteins lacking homologues.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md)) | AF2 with MSA: median GDT-TS 92 on CASP14; ablating MSA depth from 5120 → 1 drops by 25–40 GDT-TS on hard targets. |
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) | ESMFold (MSA-free): median TM-score 0.71 vs AF2 0.84; gap closes for high-pLDDT structures and orphan proteins where AF2 lacks MSAs. |
| [HelixFold-Single](https://arxiv.org/abs/2207.13921) ([note](notes/helixfold-single-msa-free-2022.md)) | HelixFold-Single (MSA-free) closes ~80% of the AF2-vs-no-MSA gap by distilling AF2 outputs as pretraining. |
| [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) ([note](notes/high-resolution-de-novo-2022.md)) | OmegaFold beats AF2 on de-novo / orphan proteins lacking homologues by 5–10 TM-score points; loses on multi-domain hard targets. |
| [RhoFold](https://arxiv.org/abs/2207.01586) ([note](notes/accurate-rna-3d-structure-2022.md)) | RhoFold MSA-conditioned: 4 Å RMSD on RNA targets; RNA MSAs are sparse, so MSA-free RNA models lag further than protein. |
| [MSA Transformer](https://doi.org/10.1101/2021.02.12.430858) ([note](notes/msa-transformer-2021.md)) | Axial attention over MSA rows + columns gives state-of-the-art contact precision with one model trained on 26M MSAs. |
| [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md)) | ESM-IF distils AlphaFold predictions into 12M-structure training set; native recovery 51% vs 33% Rosetta on AF-distilled augmentation alone. |

### 11. Distillation from AlphaFold Predictions

Using AF2/AF3 predictions (often AlphaFold DB ~200M structures) as pseudo-labels is the cheapest known structure-prediction lever. Models that distil consistently gain 1–3 nm RMSD or 5–10 TM-score points over the same-architecture non-distilled baseline.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) | ESMFold's structure module is distilled from AF2 trajectories; ablating distillation drops median TM-score by ~5 points. |
| [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md)) | ESM-IF training data: 12M AlphaFold DB structures; without AF distillation, recovery drops from 51% to ~38%. |
| [HelixFold-Single](https://arxiv.org/abs/2207.13921) ([note](notes/helixfold-single-msa-free-2022.md)) | Pretraining on AF2 pseudo-structures recovers most of the MSA-free gap; ablating distillation drops TM-score by 7 points. |
| [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) ([note](notes/high-resolution-de-novo-2022.md)) | OmegaFold distillation regimen (AF2 pseudo-labels + de-novo benchmark) is necessary for orphan-protein gains. |
| [RhoFold](https://arxiv.org/abs/2207.01586) ([note](notes/accurate-rna-3d-structure-2022.md)) | RhoFold uses RNA structure distillation analogue; gains over MSA-only RNA baselines are 1–3 Å RMSD. |
| [GearNet](https://arxiv.org/abs/2203.06125) ([note](notes/protein-representation-learning-by-2022.md)) | GearNet pretrains on AF2 structures (805k); ablating to PDB-only (90k) drops EC/GO accuracy by 3–6 points. |

### 12. Evaluation & Benchmarking Caveats

Many headline gains shrink ≥50% under (a) leakage-corrected splits (sequence identity / time / lab), (b) fair-baseline reruns with tuned hyperparameters, and (c) out-of-distribution test sets. Recurring problems: scRNA FMs vs scVI rerun, pathology FMs vs ImageNet-supervised baselines on small cohorts, NT/DNABERT on the GUE benchmark which is partially leaked.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md)) | scGPT vs scVI on integration: gains are 1–3% under fair-baseline reruns reported in follow-up work, vs 5–10% in original paper. |
| [scFoundation](https://doi.org/10.1038/s41592-024-02305-7) ([note](notes/large-scale-foundation-model-2024.md)) | scFoundation vs scVI on perturbation: gains shrink 30–50% with leakage-corrected splits. |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)) | Geneformer dosage-sensitivity AUROC 0.89 reproducible only on author-published splits; cross-tissue test gives 0.78. |
| [CellPLM](https://doi.org/10.1101/2023.10.03.560734) ([note](notes/cellplm-pre-training-of-2023.md)) | CellPLM ablation table reports 4 variants; the cell-language-model variant alone is 2–4 points behind full model — most benefit comes from inter-cell attention. |
| [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md)) | SCimilarity zero-shot annotation accuracy depends heavily on the reference set's tissue match; cross-tissue accuracy drops 10–20%. |
| [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md)) | NT GUE results partially affected by sequence-identity leakage in some tasks; multispecies NT still wins under cleaner splits. |
| [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md)) | GigaPath benchmark gains shrink 1–4% under leave-one-centre-out evaluation vs random split. |
| [ESM-1b](https://doi.org/10.1073/pnas.2016239118) ([note](notes/biological-structure-and-function-2021.md)) | ESM-1b contact precision tested on CASP and CAMEO; ESM-2 confirms scaling but original ESM-1b numbers depend on time-split avoiding train leakage. |

## Modality-Specific Recipes

Practical defaults per modality, drawn from the strongest ablations in the 84 FM corpus.

### DNA / Genomics

**Default recipe.** Multispecies corpus + BPE or character tokenization + sub-quadratic backbone (Hyena/Mamba) + ≥32k context + reverse-complement equivariance.

**Rev 4 additions.** [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)) (Evo 2, 40B) confirms scale-up but published configuration-only; [GET](https://doi.org/10.1038/s41586-024-08391-z) ([note](notes/a-foundation-model-of-2025.md)) (GET) shows cell-type-conditioned epigenome modelling. **(N=12 papers)** DNA FMs: [PhyloGPN](https://arxiv.org/abs/2503.03773) ([note](notes/a-phylogenetic-approach-to-2025.md)), [Caduceus](https://arxiv.org/abs/2403.03234) ([note](notes/caduceus-bi-directional-equivariant-2024.md)), [DNABERT-2](https://arxiv.org/abs/2306.15006) ([note](notes/dnabert-2-efficient-foundation-2023.md)), [DNABERT-1](https://doi.org/10.1093/bioinformatics/btab083) ([note](notes/dnabert-pre-trained-bidirectional-2021.md)), [dnaGrinder](https://arxiv.org/abs/2409.15697) ([note](notes/dnagrinder-a-lightweight-and-2024.md)), [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)), [Genome Book](https://arxiv.org/abs/2501.16982) ([note](notes/human-genome-book-words-2025.md)), [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)), [JEPA-DNA](https://arxiv.org/abs/2602.17162) ([note](notes/jepa-dna-grounding-genomic-2026.md)), [Evo](https://doi.org/10.1126/science.ado9336) ([note](notes/sequence-modeling-and-design-2024.md)), [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md)), [VQDNA](https://arxiv.org/abs/2405.10812) ([note](notes/vqdna-unleashing-the-power-2024.md))

**Pitfalls.** GUE leakage; per-task hyperparameters dominate small models; Hyena/Mamba require custom kernels for production inference.

### DNA → Epigenome / Gene Expression

[Enformer](https://doi.org/10.1038/s41592-021-01252-x) ([note](notes/effective-gene-expression-prediction-2021.md)) (Enformer, 196kb) and [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) ([note](notes/predicting-rna-seq-coverage-2023.md)) (Borzoi, 524kb) remain the two-model recipe. [GET](https://doi.org/10.1038/s41586-024-08391-z) ([note](notes/a-foundation-model-of-2025.md)) (GET) extends to cell-type-conditioned cross-tissue prediction; [MIRROR-3D](https://arxiv.org/abs/2504.09060) ([note](notes/multimodal-3d-genome-pre-2025.md)) (MIRROR-3D) adds Hi-C fusion. **(N=4 papers)** epigenome FMs: [Enformer](https://doi.org/10.1038/s41592-021-01252-x) ([note](notes/effective-gene-expression-prediction-2021.md)), [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) ([note](notes/predicting-rna-seq-coverage-2023.md)), [GET](https://doi.org/10.1038/s41586-024-08391-z) ([note](notes/a-foundation-model-of-2025.md)), [MIRROR-3D](https://arxiv.org/abs/2504.09060) ([note](notes/multimodal-3d-genome-pre-2025.md))

### RNA

[RNA-FM](https://arxiv.org/abs/2204.00300) ([note](notes/interpretable-rna-foundation-model-2022.md)) (RNA-FM, MLM on ncRNA), [RiNALMo](https://arxiv.org/abs/2403.00043) ([note](notes/rinalmo-general-purpose-rna-2024.md)) (RiNALMo, scaled MLM), and [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)) (Orthrus, Mamba + contrastive on mature mRNA) cover representation; [RhoFold](https://arxiv.org/abs/2207.01586) ([note](notes/accurate-rna-3d-structure-2022.md)) (RhoFold) covers structure with sparse RNA MSAs. **(N=4 papers)** RNA FMs: [RNA-FM](https://arxiv.org/abs/2204.00300) ([note](notes/interpretable-rna-foundation-model-2022.md)), [RiNALMo](https://arxiv.org/abs/2403.00043) ([note](notes/rinalmo-general-purpose-rna-2024.md)), [Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md)), [RhoFold](https://arxiv.org/abs/2207.01586) ([note](notes/accurate-rna-3d-structure-2022.md))

**Pitfalls.** RNA pretraining corpora are 100× smaller than protein; MSA depth for RNA is sparse so MSA-free models lag further than protein. For mature mRNA tasks, contrastive learning with evolutionary/splicing augmentations (Orthrus) dramatically outperforms reconstruction-based SSL — biological inductive bias matters more than scale.

### Protein Sequence

**Default.** ESM-2 family (650M for representation, 15B for SOTA contact / variant effect) + UR50 clustered pretraining + MLM.

**Rev 4 additions.** [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)) (ESM-3, multimodal masked tokens over sequence/structure/function) and [ProteinMPNN](https://doi.org/10.1126/science.add2187) ([note](notes/robust-deep-learning-based-2022.md)) (ProteinMPNN, autoregressive sequence-given-structure) close the design loop. **(N=16 papers)** protein-sequence FMs: [Ankh](https://arxiv.org/abs/2301.06568) ([note](notes/ankh-optimized-protein-language-2023.md)), [ESM-1b](https://doi.org/10.1073/pnas.2016239118) ([note](notes/biological-structure-and-function-2021.md)), [PST](https://arxiv.org/abs/2401.14819) ([note](notes/endowing-protein-language-models-2024.md)), [ESM-AA](https://arxiv.org/abs/2403.12995) ([note](notes/esm-all-atom-multi-2024.md)), [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)), [ESM-1v](https://doi.org/10.1101/2021.07.09.450648) ([note](notes/language-models-enable-zero-2021.md)), [ESM-design](https://doi.org/10.1101/2022.12.21.521521) ([note](notes/language-models-generalize-beyond-2022.md)), [MSA Transformer](https://doi.org/10.1101/2021.02.12.430858) ([note](notes/msa-transformer-2021.md)), [ProGen](https://arxiv.org/abs/2004.03497) ([note](notes/progen-language-modeling-for-2020.md)), [ProtCLIP](https://arxiv.org/abs/2412.20014) ([note](notes/protclip-function-informed-protein-2024.md)), [ProteinBERT](https://doi.org/10.1093/bioinformatics/btac020) ([note](notes/proteinbert-a-universal-deep.md)), [ProtGPT2](https://doi.org/10.1038/s41467-022-32007-7) ([note](notes/protgpt2-is-a-deep.md)), [ProtTrans](https://arxiv.org/abs/2007.06225) ([note](notes/prottrans-towards-cracking-the-2020.md)), [ProteinMPNN](https://doi.org/10.1126/science.add2187) ([note](notes/robust-deep-learning-based-2022.md)), [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)), [Rao attention-as-contacts](https://doi.org/10.1101/2020.12.15.422761) ([note](notes/transformer-protein-language-models-2021.md))

### Protein Structure

**Default.** AF2 for monomers; [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)) (AF3) for protein-NA-ligand complexes; [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)) (RFAA) for all-atom heteroatom complexes. [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md)) (ESMFold), [HelixFold-Single](https://arxiv.org/abs/2207.13921) ([note](notes/helixfold-single-msa-free-2022.md)), [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) ([note](notes/high-resolution-de-novo-2022.md)) (OmegaFold) for MSA-free / orphan proteins. [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md)) (ESM-IF) for inverse folding. **(N=9 papers)** structure FMs: [RoseTTAFold](https://doi.org/10.1126/science.abj8754) ([note](notes/accurate-prediction-of-protein-2021.md)), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)), [HelixFold-Single](https://arxiv.org/abs/2207.13921) ([note](notes/helixfold-single-msa-free-2022.md)), [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) ([note](notes/high-resolution-de-novo-2022.md)), [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md)), [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md)), [GearNet](https://arxiv.org/abs/2203.06125) ([note](notes/protein-representation-learning-by-2022.md)), [RhoFold](https://arxiv.org/abs/2207.01586) ([note](notes/accurate-rna-3d-structure-2022.md))

### Single-Cell RNA

**Default.** Geneformer or scGPT for representation + scVI as fair baseline (always rerun!). For perturbation / cross-tissue: scFoundation, scGPT, or [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md)) (SCimilarity) for nearest-reference annotation.

**Rev 4 additions.** [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)) (Nicheformer) adds spatial niche conditioning; [UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md)) (UCE) enables cross-species zero-shot annotation; [CellPLM](https://doi.org/10.1101/2023.10.03.560734) ([note](notes/cellplm-pre-training-of-2023.md)) (CellPLM) adds inter-cell attention for tissue-context tasks; [GenePT](https://doi.org/10.1101/2023.10.16.562533) ([note](notes/genept-a-simple-but-2023.md)) (GenePT) shows GPT-3.5 text embeddings of NCBI summaries match scGPT at 0% pretraining cost; [scMulan](https://doi.org/10.1101/2024.01.25.577152) ([note](notes/scmulan-a-multitask-generative-2024.md)) (scMulan) adds multi-task control tokens. **(N=12 papers)** scRNA FMs: [CellPLM](https://doi.org/10.1101/2023.10.03.560734) ([note](notes/cellplm-pre-training-of-2023.md)), [GenePT](https://doi.org/10.1101/2023.10.16.562533) ([note](notes/genept-a-simple-but-2023.md)), [scFoundation](https://doi.org/10.1038/s41592-024-02305-7) ([note](notes/large-scale-foundation-model-2024.md)), [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)), [scELMo](https://arxiv.org/abs/2601.05648) ([note](notes/open-world-knowledge-aided-2026.md)), [scBERT](https://doi.org/10.1038/s42256-022-00534-z) ([note](notes/scbert-as-a-large-2022.md)), [scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md)), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md)), [scMamba](https://arxiv.org/abs/2506.20697) ([note](notes/scmamba-a-scalable-foundation-2025.md)), [scMulan](https://doi.org/10.1101/2024.01.25.577152) ([note](notes/scmulan-a-multitask-generative-2024.md)), [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)), [UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md))

**Pitfalls.** Always rerun scVI / Harmony / totalVI as baselines with tuned hyperparameters; FM gains over fair baselines are typically 1–3% on integration, 5–15% only on zero-shot perturbation / cross-tissue / cross-species.

### Spatial Transcriptomics

Newly broken out in Rev 4. [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)) (Nicheformer) is the canonical FM: niche-conditional masking on spatial transcriptomics + dissociated scRNA gives +4–7 points on niche classification. **(N=1 papers)** spatial-transcriptomics FMs: [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md))

**Pitfalls.** Few public spatial atlases at scale; most evaluation is intra-dataset.

### Computational Pathology

**Default.** UNI or GigaPath as tile encoder + slide-level aggregator (ABMIL/CLAM-style as baseline). For multimodal slide-text: CONCH (NatMed). For mixed-magnification: Virchow2.

**Rev 4 additions.** [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md)) (CONCH NatMed, 1.17M slide-caption pairs) supersedes the preprint version. [Virchow2](https://arxiv.org/abs/2408.00738) ([note](notes/virchow2-scaling-self-supervised-2024.md)) (Virchow2) demonstrates mixed-magnification SSL gains. **(N=13 papers)** pathology / radiology FMs: [UNI](https://arxiv.org/abs/2308.15474) ([note](notes/a-general-purpose-self-2023.md)), [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md)), [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md)), [KEP (KEEP)](https://arxiv.org/abs/2412.13126) ([note](notes/knowledge-enhanced-pretraining-for-2024.md)), [Phikon-v2](https://arxiv.org/abs/2409.09173) ([note](notes/phikon-v2-a-large-2024.md)), [RudolfV](https://arxiv.org/abs/2401.04079) ([note](notes/rudolfv-a-foundation-model-2024.md)), [HIPT](https://arxiv.org/abs/2206.02647) ([note](notes/scaling-vision-transformers-to-2022.md)), [CONCH (preprint)](https://arxiv.org/abs/2307.12914) ([note](notes/towards-a-visual-language-2023.md)), [H-optimus-0](https://arxiv.org/abs/2404.15217) ([note](notes/towards-large-scale-training-2024.md)), [Virchow](https://arxiv.org/abs/2309.07778) ([note](notes/virchow-a-million-slide-2023.md)), [Virchow2](https://arxiv.org/abs/2408.00738) ([note](notes/virchow2-scaling-self-supervised-2024.md)), [uniGradICON](https://arxiv.org/abs/2403.05780) ([note](notes/unigradicon-a-foundation-model-2024.md)), [XrayGPT](https://arxiv.org/abs/2306.07971) ([note](notes/xraygpt-chest-radiographs-summarization-2023.md))

**Pitfalls.** Single-centre evaluation overestimates by 1–4%; always include leave-one-centre-out. ImageNet-supervised baselines on small cohorts can be within 2% of FMs.

### Cell Painting / High-Content Microscopy

[CellPainTR](https://arxiv.org/abs/2509.06986) ([note](notes/cellpaintr-generalizable-representation-learning-2025.md)) (CellPainTR) and [ViTally](https://arxiv.org/abs/2411.02572) ([note](notes/vitally-consistent-scaling-biological-2024.md)) (ViTally) cover the recipe: ViT-based DINOv2/MAE on multi-channel fluorescence with channel-mixing augmentation. **(N=2 papers)** cell-painting / microscopy FMs: [CellPainTR](https://arxiv.org/abs/2509.06986) ([note](notes/cellpaintr-generalizable-representation-learning-2025.md)), [ViTally](https://arxiv.org/abs/2411.02572) ([note](notes/vitally-consistent-scaling-biological-2024.md))

### Mass-Spectrometry Proteomics

[LSM-MS2](https://arxiv.org/abs/2510.26715) ([note](notes/lsm-ms2-a-foundation-2025.md)) (LSM-MS2) is the only FM in this corpus; representation learning on MS2 spectra. **(N=1 papers)** MS-proteomics FMs: [LSM-MS2](https://arxiv.org/abs/2510.26715) ([note](notes/lsm-ms2-a-foundation-2025.md))

### Multimodal Medical

[BiomedCLIP](https://arxiv.org/abs/2303.00915) ([note](notes/biomedclip-a-multimodal-biomedical-2023.md)) (BiomedCLIP, PMC-15M) for image-text representation; [LLaVA-Med](https://arxiv.org/abs/2306.00890) ([note](notes/llava-med-training-a-2023.md)) (LLaVA-Med), [XrayGPT](https://arxiv.org/abs/2306.07971) ([note](notes/xraygpt-chest-radiographs-summarization-2023.md)) (XrayGPT), [Doctor Sun](https://arxiv.org/abs/2508.08270) ([note](notes/doctor-sun-a-bilingual-2025.md)) (Doctor Sun), [MedMax](https://arxiv.org/abs/2412.12661) ([note](notes/medmax-mixed-modal-instruction-2024.md)) (MedMax) for instruction-tuned QA; [ConceptCLIP](https://arxiv.org/abs/2501.15579) ([note](notes/an-explainable-biomedical-foundation-2025.md)) (ConceptCLIP) for explainable retrieval; [MedDiff-FM](https://arxiv.org/abs/2410.15432) ([note](notes/meddiff-fm-a-diffusion-2024.md)) (MedDiff-FM) for medical image generation. **(N=9 papers)** multimodal medical FMs: [ConceptCLIP](https://arxiv.org/abs/2501.15579) ([note](notes/an-explainable-biomedical-foundation-2025.md)), [BiomedCLIP](https://arxiv.org/abs/2303.00915) ([note](notes/biomedclip-a-multimodal-biomedical-2023.md)), [Doctor Sun](https://arxiv.org/abs/2508.08270) ([note](notes/doctor-sun-a-bilingual-2025.md)), [LLaVA-Med](https://arxiv.org/abs/2306.00890) ([note](notes/llava-med-training-a-2023.md)), [MedDiff-FM](https://arxiv.org/abs/2410.15432) ([note](notes/meddiff-fm-a-diffusion-2024.md)), [MedMax](https://arxiv.org/abs/2412.12661) ([note](notes/medmax-mixed-modal-instruction-2024.md)), [XrayGPT](https://arxiv.org/abs/2306.07971) ([note](notes/xraygpt-chest-radiographs-summarization-2023.md)), [BioGPT](https://arxiv.org/abs/2210.10341) ([note](notes/biogpt-generative-pre-trained-2022.md)), [BioBERT](https://arxiv.org/abs/1901.08746) ([note](notes/biobert-a-pre-trained-2019.md))

### Small Molecules / SMILES

[ChemBERTa](https://arxiv.org/abs/2010.09885) ([note](notes/chemberta-large-scale-self-2020.md)) (ChemBERTa) and [ChemFM](https://arxiv.org/abs/2410.21422) ([note](notes/chemfm-as-a-scaling-2024.md)) (ChemFM) for SMILES MLM/CLM; [MolFM](https://arxiv.org/abs/2307.09484) ([note](notes/molfm-a-multimodal-molecular-2023.md)) (MolFM) for tri-modal molecule-text-graph; [MACE-OFF / Multi-Fi](https://arxiv.org/abs/2412.13088) ([note](notes/taming-multi-domain-fidelity-2024.md)) (MACE-OFF) for ML force fields. **(N=5 papers)** small-molecule FMs: [ChemBERTa](https://arxiv.org/abs/2010.09885) ([note](notes/chemberta-large-scale-self-2020.md)), [ChemFM](https://arxiv.org/abs/2410.21422) ([note](notes/chemfm-as-a-scaling-2024.md)), [LSM-MS2](https://arxiv.org/abs/2510.26715) ([note](notes/lsm-ms2-a-foundation-2025.md)), [MolFM](https://arxiv.org/abs/2307.09484) ([note](notes/molfm-a-multimodal-molecular-2023.md)), [MACE-OFF / Multi-Fi](https://arxiv.org/abs/2412.13088) ([note](notes/taming-multi-domain-fidelity-2024.md))

### Cross-Omics & Unified Models

[AIDO](https://doi.org/10.1101/2024.12.02.626322) ([note](notes/aido-accurate-model-of-2024.md)) (AIDO) covers DNA + RNA + protein + cell with shared representation modules; per-module ablations live in their respective preprints. **(N=3 papers)** cross-omics FMs: [AIDO](https://doi.org/10.1101/2024.12.02.626322) ([note](notes/aido-accurate-model-of-2024.md)), [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md))

## Open Problems

1. **Honest single-cell evaluation.** scRNA FMs need standardised, leakage-corrected benchmarks with always-on scVI/Harmony/totalVI baselines. **(N=8 papers)** evidence: [scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md)), [scFoundation](https://doi.org/10.1038/s41592-024-02305-7) ([note](notes/large-scale-foundation-model-2024.md)), [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md)), [CellPLM](https://doi.org/10.1101/2023.10.03.560734) ([note](notes/cellplm-pre-training-of-2023.md)), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md)), [UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md)), [scBERT](https://doi.org/10.1038/s42256-022-00534-z) ([note](notes/scbert-as-a-large-2022.md)), [GenePT](https://doi.org/10.1101/2023.10.16.562533) ([note](notes/genept-a-simple-but-2023.md))

2. **Generalisable RNA structure.** RNA models lag protein because MSAs are sparse; need RNA-specific distillation analogue to AF2 distillation. **(N=3 papers)** evidence: [RhoFold](https://arxiv.org/abs/2207.01586) ([note](notes/accurate-rna-3d-structure-2022.md)), [RNA-FM](https://arxiv.org/abs/2204.00300) ([note](notes/interpretable-rna-foundation-model-2022.md)), [RiNALMo](https://arxiv.org/abs/2403.00043) ([note](notes/rinalmo-general-purpose-rna-2024.md))

3. **Cross-modal generation that respects physics.** ESM-3 + AF3 + RFAA close the structural gap; quantifying which prompts produce *foldable, functional* molecules remains open. **(N=4 papers)** evidence: [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)), [ProteinMPNN](https://doi.org/10.1126/science.add2187) ([note](notes/robust-deep-learning-based-2022.md))

4. **Spatial transcriptomics scaling.** Only one canonical FM; the field needs a Geneformer/scGPT-scale niche-aware model. **(N=1 papers)** evidence: [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md))

5. **Pathology robustness.** All public benchmarks are biased toward a few centres; cross-site generalisation gaps of 4–9% are routine. **(N=7 papers)** evidence: [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md)), [UNI](https://arxiv.org/abs/2308.15474) ([note](notes/a-general-purpose-self-2023.md)), [Virchow](https://arxiv.org/abs/2309.07778) ([note](notes/virchow-a-million-slide-2023.md)), [Phikon-v2](https://arxiv.org/abs/2409.09173) ([note](notes/phikon-v2-a-large-2024.md)), [RudolfV](https://arxiv.org/abs/2401.04079) ([note](notes/rudolfv-a-foundation-model-2024.md)), [Virchow2](https://arxiv.org/abs/2408.00738) ([note](notes/virchow2-scaling-self-supervised-2024.md)), [H-optimus-0](https://arxiv.org/abs/2404.15217) ([note](notes/towards-large-scale-training-2024.md))

6. **Long-range DNA past 1 Mb.** Evo 2 and HyenaDNA reach 1M tokens; head-to-head accuracy ablations past 524kb on regulatory tasks have not been published. **(N=5 papers)** evidence: [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)), [HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md)), [Evo](https://doi.org/10.1126/science.ado9336) ([note](notes/sequence-modeling-and-design-2024.md)), [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) ([note](notes/predicting-rna-seq-coverage-2023.md)), [Enformer](https://doi.org/10.1038/s41592-021-01252-x) ([note](notes/effective-gene-expression-prediction-2021.md))

7. **Reproducible AF3 / RFAA.** AF3 weights and training data are partially restricted; community reimplementations diverge by 5–10% on heteroatom complexes. **(N=4 papers)** evidence: [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)), [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md)), [RoseTTAFold](https://doi.org/10.1126/science.abj8754) ([note](notes/accurate-prediction-of-protein-2021.md))

## Methodology & Limitations

This guidebook is grounded in **84 bio-FM papers**, each of which carries a `## Ablations (Rev 4)` section in its source note. **(N=X papers)** annotations on every claim count only those 84 FM papers; the remaining 85 surveyed papers are baselines, benchmarks, or supporting methods (TAPE, CLAM, scVI, totalVI, Cellpose, CellRanger, etc.) and are not counted as primary evidence.

Coverage is uneven: protein sequence (21), pathology (13), protein structure (13), DNA (12), and scRNA (12) are well represented; RNA (5), small-molecule (6), epigenome (4), spatial transcriptomics (1), MS-proteomics (1), and cell-painting (1) are under-represented.

Several Rev-4 ablation tables are limited by source access:
- [scMulan](https://doi.org/10.1101/2024.01.25.577152) ([note](notes/scmulan-a-multitask-generative-2024.md)): full text 403 (bioRxiv); ablations could not be quoted directly.
- [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)) (Evo 2): preprint inaccessible at extraction time; only configuration-level details available.
- [UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md)) (UCE): full text 403; supporting evidence is qualitative.
- [AIDO](https://doi.org/10.1101/2024.12.02.626322) ([note](notes/aido-accurate-model-of-2024.md)): ablations are distributed across per-module preprints.

Quantitative claims reflect the ablations reported in each paper and have **not been independently reproduced**. The Rev 3 verification appendix (preserved verbatim below) is the only independent fact-check applied.

## Appendix: FM Catalogue (84 entries)

One row per FM, grouped by modality. Each entry: nickname → URL, one-line ablation take-away extracted from the source note's `## Ablations (Rev 4)` table.

### DNA / Genomics (12)

- **[Caduceus](https://arxiv.org/abs/2403.03234) ([note](notes/caduceus-bi-directional-equivariant-2024.md))** — *modalities: dna*
  - Use Mamba (selective SSM) as the inner block; it scales better with context than implicit-conv Hyena.
  - Parameter sharing buys depth at fixed param count and outperforms the naive 2-module bidirectional design.
  - RC equivariance is a useful architectural prior even at pre-training, not just downstream.
  - RC equivariance — whether built-in (PS) or post-hoc (Ph) — is the dominant factor on short/medium-range classification.
- **[DNABERT-1](https://doi.org/10.1093/bioinformatics/btab083) ([note](notes/dnabert-pre-trained-bidirectional-2021.md))** — *modalities: dna*
  - K-mer length choice barely moves the needle (all k=3–6 within 1.6 GUE points), whereas switching from overlapping k-mers to BPE yields +4.41 GUE with 3.25× fewer FLOPs.
  - Span masking of contiguous k tokens is mandatory for MLM with overlapping k-mers to prevent information leakage from adjacent unmasked tokens.
  - Pre-training transfers decisively across all downstream tasks (promoter, TFBS, splice site), substantially outperforming from-scratch training.
- **[DNABERT-2](https://arxiv.org/abs/2306.15006) ([note](notes/dnabert-2-efficient-foundation-2023.md))** — *modalities: dna*
  - BPE strictly dominates overlapping k-mer in both performance and compute, validating the central design choice.
  - Vocab size = 4096 is the chosen sweet spot trading compute vs accuracy.
  - Multi-species pre-training is the dominant source of DNABERT-2's gains; architecture alone is insufficient.
  - Cheap domain-adaptive pre-training reliably improves downstream performance.
- **[dnaGrinder](https://arxiv.org/abs/2409.15697) ([note](notes/dnagrinder-a-lightweight-and-2024.md))** — *modalities: dna*
  - SwiGLU adopted: ~comparable quality at substantially lower parameter cost.
  - Further pretraining yields limited / inconsistent gains for dnaGrinder; not worth the compute as a default.
  - SNP-variant-only data is unsuitable (sparse, arbitrarily spaced); complete reference sequences with SNPs incorporated are required.
  - Approximate (dilated) attention loses too much information; full attention with SLW is preferred even at shorter context.
- **[Evo](https://doi.org/10.1126/science.ado9336) ([note](notes/sequence-modeling-and-design-2024.md))** — *modalities: dna, rna, protein-sequence*
  - Byte-level DNA needs deep-signal-processing / SSM hybrids; motivates StripedHyena for Evo.
  - StripedHyena chosen partly because real training is always compute-suboptimal.
  - Long genomic context is the key enabler; whole-organism fitness signal is non-local.
  - Result is not a prompt-engineering artefact.
  - Genomic-context modelling, not codon-level pretraining, drives the capability.
- **[Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md))** — *modalities: dna*
  - StripedHyena 2 architecture unlocks 1M-nucleotide context (8× Evo 1) and enables 30× data-scale-up, making the gain architectural rather than merely parametric.
  - The 1B/7B/20B/40B parameter variants trade hardware requirements against capability; the 20B checkpoint shows parameter count is not monotonic with deployable performance.
- **[Genome Book](https://arxiv.org/abs/2501.16982) ([note](notes/human-genome-book-words-2025.md))** — *modalities: dna, protein-sequence*
  - EN→DNA transfer works on short DNA pairs without any DNA supervision.
  - Transfer degrades on longer sequences (~13 pt drop) — length sensitivity.
  - All three lengths >79% → transfer is robust but length-dependent.
  - Shared BPE + EN similarity FT is what aligns DNA and EN representations (mechanism behind row 1–3).
- **[HyenaDNA](https://arxiv.org/abs/2306.15794) ([note](notes/hyenadna-long-range-genomic-2023.md))** — *modalities: dna*
  - Single-nucleotide tokenization is a major contributor to HyenaDNA's performance; aggregating k-mer tokenizers hurt fine-grained tasks.
  - Causal next-token pretraining is preferable; naive bidirectional Hyena (without MLM pretraining) underperforms.
  - Pretraining helps but gains are modest because GenomicBenchmarks are near saturation.
  - Pretraining matters most on harder, lower-baseline tasks (especially histone marks).
  - Hyena operator outperforms attention at matched parameter count and competes with models 1500× larger.
- **[JEPA-DNA](https://arxiv.org/abs/2602.17162) ([note](notes/jepa-dna-grounding-genomic-2026.md))** — *modalities: dna*
  - JEPA objective on DNABERT-2 provides 3–7% AUROC gains on short-to-mid-range supervised tasks (TF binding, splice site, coding pathogenicity), with largest improvement at mid-range (+4.8%).
  - Zero-shot JEPA gains are strongest on expression effects and Mendelian trait ranking (+6.9% and +7.3% AUROC), but degrade on long-range tasks (OMIM −8.7%), suggesting global latent grounding hurts fine-grained local syntax.
  - No formal ablations on loss component weights, predictor architecture, or masking strategy are reported; only end-to-end JEPA-DNA vs. DNABERT-2 baseline contrast.
- **[Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) ([note](notes/the-nucleotide-transformer-building-2024.md))** — *modalities: dna*
  - Sequence diversity beats raw human-only data; diversity > size when compute-limited.
  - Scale helps, but pairing with diverse pretraining data matters as much.
  - Fine-tuning required for top performance; also lower variance than probing.
  - Embedding quality is layer-dependent; mid/late-but-not-final layers best.
  - IA³ is sufficient; ~1000× storage savings with negligible performance cost.
- **[PhyloGPN](https://arxiv.org/abs/2503.03773) ([note](notes/a-phylogenetic-approach-to-2025.md))** — *modalities: dna, multispecies-alignment*
  - Phylogenetic F81 loss enables single-sequence inference without alignment data while matching multi-sequence MSA approaches (GPN-MSA AUROC 0.96) on ClinVar pathogenic variants, vastly outperforming standard genomic LMs.
  - Holding out half the genome from training barely changes and slightly improves performance on most variant categories, indicating broadly transferable features rather than chromosome-specific memorisation.
- **[VQDNA](https://arxiv.org/abs/2405.10812) ([note](notes/vqdna-unleashing-the-power-2024.md))** — *modalities: dna*
  - Hierarchical Residual Quantization codebook discriminates 2× better than hand-crafted BPE on linear probing (F1 48.87 vs 36.53), showing the learned vocabulary captures genuinely discriminative patterns.
  - Codebook size is the dominant scaling knob: 128 → 512 codes yields +6.8 linear-probe F1 points, while codebook dimension has minimal effect.
  - 25% MLM masking is optimal (higher than typical DNA-LMs' 15%), suggesting the VQ tokenizer encodes rich contextual information allowing harder masking objectives.

### Epigenome / Gene Expression (4)

- **[Borzoi](https://doi.org/10.1038/s41588-024-02053-6) ([note](notes/predicting-rna-seq-coverage-2023.md))** — *modalities: epigenome, rna*
  - Adding DNase/ATAC (and further CAGE/ChIP) to RNA-seq consistently improved RNA-seq test accuracy, eQTL classification, and CRISPR enhancer–gene linking AUPRC. Strongest single contributors are DNase + ATAC.
  - Including mouse training data substantially improved eQTL effect-size Spearman R and held-out RNA-seq accuracy at matched data composition.
  - U-Net upsampling from 128 → 32 bp is required for splice-site-resolution coverage; without it exon boundaries are blurred and gene-level shape correlation degrades. Architecture-only ablation.
  - Within a single cell line the same ordering holds: auxiliary assays > D/A/RNA > RNA-only — ruling out that the multispecies/multi-assay gains come purely from cross-tissue diversity.
- **[Enformer](https://doi.org/10.1038/s41592-021-01252-x) ([note](notes/effective-gene-expression-prediction-2021.md))** — *modalities: epigenome*
  - The enlarged receptive field is the single biggest lever: restricting attention to 20 kb causes a large performance drop, while expansion to 100 kb is crucial.
  - Attention layers outperform dilated convolutions across all model sizes, depths, and data budgets, indicating the architectural gain is not a scale artefact.
  - Performance scales monotonically with parameters without saturation within the explored range, mirroring NLP scaling trends.
- **[GET](https://doi.org/10.1038/s41586-024-08391-z) ([note](notes/a-foundation-model-of-2025.md))** — *modalities: epigenome*
  - Self-supervised motif-masked pretraining is essential for cross-cell-type generalization.
  - Region-wise transformer attention beats simpler ML on the same features.
  - Performance is consistent across chromosomes; no single chromosome drives results.
  - Model is not over-reliant on any small set of motifs; redundancy across motif clusters.
  - Quantitative aCPM signal during fine-tuning improves transfer to new assays.
- **[MIRROR-3D](https://arxiv.org/abs/2504.09060) ([note](notes/multimodal-3d-genome-pre-2025.md))** — *modalities: epigenome, interactome*
  - Contrastive loss alone is a strong baseline.
  - Orthogonal loss adds ~0.5% AUROC by separating modal-invariant vs modal-specific features.
  - Cross-modal mapping yields a modest extra gain and enables missing-modality inference.

### RNA (4)

- **[RhoFold](https://arxiv.org/abs/2207.01586) ([note](notes/accurate-rna-3d-structure-2022.md))** — *modalities: rna*
  - MSA module is the most critical RhoFold+ component with the largest degradation when removed.
  - RNA-FM language model partially compensates for missing MSA on novel/dissimilar RNAs (p=0.0005 with RNA-FM vs 0.0112 without on TM-vs-MSA-depth).
  - Recycling through the structure module matters most for long sequences, effectively acting as model-deepening when sequence-level information is scarce.
- **[RiNALMo](https://arxiv.org/abs/2403.00043) ([note](notes/rinalmo-general-purpose-rna-2024.md))** — *modalities: rna*
  - RoPE plus SwiGLU together yield +0.19 F1 on inter-family secondary-structure generalisation over baseline sinusoidal PE + GELU, while intra-family gains are marginal.
  - RiNALMo-33M with modern architecture and good data curation matches or beats 100M RNA-FM despite 3× fewer parameters, showing architecture and data quality matter more than raw scale.
  - Frozen pre-trained RiNALMo suffices for inter-family secondary-structure generalisation (0.70 F1) but collapses on mRNA tasks; fine-tuning is essential for bridging ncRNA-only pre-training to mRNA domains.
- **[RNA-FM](https://arxiv.org/abs/2204.00300) ([note](notes/interpretable-rna-foundation-model-2022.md))** — *modalities: rna*
  - Single-sequence RNA-FM embeddings replace expensive MSA-derived features on 3D tasks, boosting Top-L precision from 0.33 to 0.66 when combined with 2D-structure transfer learning.
  - Structural task improvements (+3–5 F1 on 2D, +20–33 points on 3D closeness) are substantially larger than functional task gains (+0.009 AUPRC on RBP binding), indicating pre-training on ncRNA distributes poorly to mRNA tasks.
  - Transfer learning from 2D-structure adds +13 Top-L precision points for 3D closeness, outweighing RNA-FM embeddings alone and demonstrating multi-task initialisation is critical for small-data regimes.
- **[Orthrus](https://doi.org/10.1038/s41592-026-03064-3) ([note](notes/orthrus-toward-evolutionary-and-2026.md))** — *modalities: rna* — 10.1M params, Mamba SSM
  - Contrastive learning (DCL) with splice-isoform + ortholog augmentations beats MLM (Z-score 0.90 vs 0.71) and matches/outperforms 7B-param Evo 2 on mRNA property tasks.
  - Removing orthology augmentation drops Z-score by 0.11; masking-only augmentation drops by 0.55.
  - Joint CL+MLM is best; α=0.95 weight for MLM in the combined loss.
  - Mamba outperforms CNN-RNN and dilated CNN at matched size.
  - 30-sample few-shot: Pearson R 0.53 on human mRNA half-life (71% of full supervised R=0.74).

### Protein Sequence (16)

- **[Ankh](https://arxiv.org/abs/2301.06568) ([note](notes/ankh-optimized-protein-language-2023.md))** — *modalities: protein-sequence*
  - 1-gram span masking with merged-unmasked target reconstruction (Exp.4) wins; 3-gram spans and partial-loss variants hurt. Reconstructing the full input (incl. unmasked) is required.
  - 10% worst; 15% & 30% trade off across tasks. **20% chosen** as compromise for general-purpose long-term training (higher than NLP standard of 15%).
  - Encoder-heavy (48/24) best; richer encoder embeddings + retains enough decoder layers for generation.
  - Deeper-narrower beats wider-shallower at fixed parameter count.
  - Gated-GELU > ReLU even though it forces shallower depth; kept Gated-GELU.
- **[ESM-1b](https://doi.org/10.1073/pnas.2016239118) ([note](notes/biological-structure-and-function-2021.md))** — *modalities: protein-sequence*
  - Transformer dominates LSTM at equal-or-fewer params; attention is the right inductive bias for protein MLM.
  - Scaling capacity improves both LM fidelity and structural content; underfitting still observed at 650 M → motivates ESM-2 scaling.
  - Diversity (cluster-balanced sampling) beats raw quantity; clustered sampling reweights loss toward rare families.
  - Data scaling helps, but the model is data-limited *and* capacity-limited at 650 M.
- **[ESM-1v](https://doi.org/10.1101/2021.07.09.450648) ([note](notes/language-models-enable-zero-2021.md))** — *modalities: protein-sequence*
  - Pre-training data distribution dominates: the UR50 → UR90 clustering swap yields +0.027 |Spearman ρ|, matching the combined gain from ensembling and spiked MSA fine-tuning.
  - Masked marginal scoring is the best strategy for variant effect prediction (0.582 |ρ|), requiring only 2 forward passes and outperforming pseudo-likelihood by 0.004–0.030.
  - Scale benefits plateau much slower than data distribution quality: a >50× parameter scale-up (13M → 649M) yields only +0.25 |ρ|, while clustering choice yields the same gain.
- **[ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) ([note](notes/evolutionary-scale-prediction-of-2023.md))** — *modalities: protein-sequence, protein-structure*
  - Contact-prediction precision rises log-linearly from 15.9% (8M) to 54.5% (15B) with no saturation, demonstrating structural information emerges from scale without explicit supervision.
  - ESMFold achieves near-AlphaFold2 accuracy at ~60× speedup without MSA search, making structure prediction feasible at metagenomic scale.
  - Folding accuracy plateaus at 3B (71.8% vs 72.1% at 15B) while contact precision keeps improving, justifying a 3B backbone over larger models.
  - ESM-2 (650M) substantially outperforms comparable single-sequence PLMs (ProtBERT-BFD, ProtT5-XL) on structure tasks, indicating training data and recipe quality matter beyond architecture.
- **[ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md))** — *modalities: protein-sequence*
  - Multimodal protein generation shows the same scaling-law behavior as LLMs; frontier capabilities require ≥7B.
  - RLHF-style alignment is scale-dependent; small models cannot fully exploit it.
  - Discretizing structure into a fixed alphabet is what unlocks unified multimodal MLM training.
  - Random per-track masking is what enables prompt-anything → generate-anything behavior.
- **[ESM-AA](https://arxiv.org/abs/2403.12995) ([note](notes/esm-all-atom-multi-2024.md))** — *modalities: protein-sequence, protein-structure, small-molecule*
  - Atoms lose positional identity; degrades fusion.
  - Largest single-component drop on ESAR — residue PE is critical.
  - Modest on ESAR, but catastrophic on Contact Prediction (P@L drops to ~0.03).
  - Bigger hit than removing MLM → atom-scale structure signal matters more than atom MLM.
- **[ESM-design](https://doi.org/10.1101/2022.12.21.521521) ([note](notes/language-models-generalize-beyond-2022.md))** — *modalities: protein-sequence*
  - Only MCMC is released and used to produce the 228 wet-lab designs (152/228 = 67% success). Greedy is not in the released config; head-to-head numbers (not in abstract/repo).
  - Enables co-discovery of sequence + structure in unconstrained mode; 71/129 = 55% experimental success.
  - Larger checkpoints exist but the design pipeline ships pinned to 650M; per-size sweep (not in abstract/repo).
  - High initial T encourages exploration; geometric cooling drives convergence to high-likelihood, structure-compatible sequences. Per-T success curves (not in abstract/repo).
- **[MSA Transformer](https://doi.org/10.1101/2021.02.12.430858) ([note](notes/msa-transformer-2021.md))** — *modalities: protein-sequence, protein-structure*
  - Tied row attention is the critical inductive bias — disabling it costs ~14 pp of top-L long-range contact precision, wiping out the margin over ESM-1b.
  - Whole-column masking during pretraining is catastrophic (~17.5 pp loss), showing uniform within-MSA masking is essential for learning covariation.
  - A 100M MSA Transformer outperforms 650M single-sequence models (ESM-1b) on contact prediction due to direct access to evolutionary signals; architecture matters more than scale when inputs are informative.
  - Even 16 diverse sequences from MaxHamming selection suffice to beat single-sequence and Potts baselines.
- **[ProGen](https://arxiv.org/abs/2004.03497) ([note](notes/progen-language-modeling-for-2020.md))** — *modalities: protein-sequence*
  - Performance degrades on unseen families but stays well above empirical baseline (18.14).
  - Pre-training is essential — fine-tuning more than halves PPL and 5× hard-acc on novel families.
  - More residue context narrows the next-token distribution; benefit holds across all sampling settings.
  - Conditioning tags carry real predictive signal; rich tag sets are needed for controllable, structurally-faithful generation.
- **[ProtCLIP](https://arxiv.org/abs/2412.20014) ([note](notes/protclip-function-informed-protein-2024.md))** — *modalities: protein-sequence, multimodal*
  - Property-driven sampling on ProtAnno-D is best (Sub 75.77, EC AUPR 0.384, Fmax 0.441, MRR 0.299), beating naive single-source and pretrain→finetune; low-quality data is valuable when properly sampled.
  - Both objectives needed; removing PDA hurts more (Sub 73.64 vs full 76.52; EC AUPR 0.136 vs 0.204) — function-grounded PDA is the key signal.
  - Without weighting, BSR and MLM losses interfere (no convergence); λ₁=0.7, λ₂=0.3 is optimal — segment reconstruction must dominate token MLM.
  - Performance fluctuates 0.1–0.6, peaks at θ=0.3, collapses for θ≥0.7 (too many functional residues masked); θ=0.3 chosen.
- **[ProteinBERT](https://doi.org/10.1093/bioinformatics/btac020) ([note](notes/proteinbert-a-universal-deep.md))** — *modalities: protein-sequence*
  - GO-annotation pretraining is the key novel design choice — its removal specifically hurts structure-related benchmarks by ~4–15 pp while leaving other tasks unaffected.
  - Pretraining duration keeps improving downstream performance on hard tasks without saturation, suggesting ProteinBERT is under-trained rather than under-parameterised.
  - ProteinBERT (16M params) matches or exceeds TAPE Transformer (38M params) on all four TAPE benchmarks, demonstrating parameter efficiency from architecture (dilated convolutions + global attention).
- **[ProteinMPNN](https://doi.org/10.1126/science.add2187) ([note](notes/robust-deep-learning-based-2022.md))** — *modalities: protein-sequence*
  - Pairwise distances are a much stronger inductive bias than dihedrals/frame orientations.
  - Updating edge features in the MPNN encoder gives a further +1.5%.
  - Random-permutation decoding both improves recovery and unlocks fixed-region / binder design.
  - Local graphs suffice; long-range context unnecessary for seq design.
- **[ProtGPT2](https://doi.org/10.1038/s41467-022-32007-7) ([note](notes/protgpt2-is-a-deep.md))** — *modalities: protein-sequence*
  - Greedy/beam → repetitive, degenerate sequences; sampling required for natural-like propensities.
  - "Worse matches in all cases" vs sampling.
  - Best matches occur for k > 800; small k under-samples natural propensities.
  - Default outperformed restrictive nucleus values.
- **[ProtTrans](https://arxiv.org/abs/2007.06225) ([note](notes/prottrans-towards-cracking-the-2020.md))** — *modalities: protein-sequence*
  - CNN ≈ LSTM > LogReg; CNN chosen (more compute-efficient). Architecture matters less than embeddings.
  - Larger raw corpus alone gives marginal/inconsistent gains; **fine-tuning on cleaner UniRef50 after BFD is the decisive trick**.
  - Auto-encoding (esp. T5 span corruption) > auto-regressive for protein representation learning.
  - Scaling width beyond 3B hurts at fixed sample budget — **more training samples beats more parameters**.
  - Performance correlates with samples seen during pre-training; informal scaling trend.
- **[PST](https://arxiv.org/abs/2401.14819) ([note](notes/endowing-protein-language-models-2024.md))** — *modalities: protein-sequence, protein-structure*
  - Freezing the ESM-2 backbone and training only lightweight GIN structure extractors matches full model pretraining and beats end-to-end baselines.
  - Richer edge features (16-dim Gaussian RBF) improve MLM accuracy (47% → 55%) but cause negative transfer downstream, indicating MLM is too weak to exploit richer geometry.
  - Structural benefit decreases monotonically with backbone scale (largest at 8M, tapers at 650M), confirming large PLMs already implicitly encode structural information.
- **[Rao attention-as-contacts](https://doi.org/10.1101/2020.12.15.422761) ([note](notes/transformer-protein-language-models-2021.md))** — *modalities: protein-sequence, protein-structure*
  - Precision rises sharply with capacity; ESM-1b is the only PLM beating Gremlin (39.3).
  - Within one family, deeper = better; not yet saturated.
  - A single head ≈ Gremlin; averaging top-5 already exceeds it → contacts live in the attention, LR just selects.
  - One labelled protein already matches Gremlin (p>0.05); diminishing returns past n=10.

### Protein Structure (8)

- **[AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) ([note](notes/highly-accurate-protein-structure-2021.md))** — *modalities: protein-structure*
  - Largest single architectural ablation; SE(3)-equivariant geometric attention is the key inductive bias of the structure module.
  - Iterative refinement of the pair + MSA representations is essential; cheap to add (no extra params), large gain.
  - Noisy-student style self-training on unlabelled UniClust sequences is a major data-augmentation lever.
  - Triangle inequality bias on pair representation drives geometric consistency; removing it hurts more than removing templates.
- **[AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md))** — *modalities: protein-structure*
  - Cross-distillation from AlphaFold-Multimer predictions greatly reduces hallucination of compact structure in disordered regions and substantially improves disorder prediction.
  - Generative diffusion replaces the equivariant structure module with no meaningful accuracy loss while eliminating torsion parametrisation and violation losses.
  - Large-crop fine-tuning disproportionately improves interface quality over intra-chain quality, consistent with interfaces requiring longer-range context.
  - Stereochemical correctness is achieved through sample-and-rank over 25 diffusion samples rather than physics-based guidance.
- **[ESM-IF](https://doi.org/10.1101/2022.04.10.487779) ([note](notes/learning-inverse-folding-from-2022.md))** — *modalities: protein-structure, protein-sequence*
  - Adding 12M AlphaFold2-predicted structures yields +13.3 pp sequence recovery (38.3% → 51.6%), but only models ≥21M params benefit; a 1M-param GVP-GNN actually regresses.
  - The hybrid GVP-encoder + Transformer-decoder edges out pure-GVP GNNs by only +0.8 pp, indicating most value comes from geometric front-end reasoning.
  - Balancing synthetic and experimental data prevents overfitting despite an ~1:80 experimental-to-predicted ratio.
- **[GearNet](https://arxiv.org/abs/2203.06125) ([note](notes/protein-representation-learning-by-2022.md))** — *modalities: protein-structure*
  - Treating edges as different types is essential; param-matched plain GCN cannot recover the gap, even with more layers/params.
  - Explicit edge-edge interaction modeling is beneficial across function prediction tasks.
  - All four deterministic combinations work, so each cropping/noise scheme yields informative views; randomly sampling combinations gives the most diverse views and is best on 3 of 4 GO/EC metrics.
- **[HelixFold-Single](https://arxiv.org/abs/2207.13921) ([note](notes/helixfold-single-msa-free-2022.md))** — *modalities: protein-structure, protein-sequence*
  - Larger PLM size (1B vs 100M) consistently improves both perplexity and structural metrics (long-range contact precision) across CASP14 and CAMEO.
  - PLM perplexity is negatively correlated with MSA depth and folding accuracy, indicating a well-trained LM effectively captures evolutionary signals without explicit MSA input.
  - Column-wise attention in EvoFormer is unnecessary for single-sequence input and is safely removed, simplifying the architecture without accuracy loss.
- **[OmegaFold](https://doi.org/10.1101/2022.07.21.500999) ([note](notes/high-resolution-de-novo-2022.md))** — *modalities: protein-structure, protein-sequence*
  - GeoFormer geometry trunk is the single most critical component (~0.115 TM-score loss when removed), more important than PLM features themselves (~0.054 loss).
  - Retraining AlphaFold2 on single sequences does not recover accuracy even with MSA-free distillation, demonstrating a purpose-built PLM trunk is essential for single-sequence folding.
  - Recycling (iterative refinement) helps but is the least critical design lever, producing monotonic but small TM-score gains.
- **[RoseTTAFold](https://doi.org/10.1126/science.abj8754) ([note](notes/accurate-prediction-of-protein-2021.md))** — *modalities: protein-structure*
  - The 3D-coordinate track is the central architectural contribution; tighter coupling of seq/dist/coords beats 2-track.
  - End-to-end is limited by GPU memory and lack of side-chain info at training; gap expected to close with more compute / side chains.
  - Memory-driven cropping is not just a workaround — it improves accuracy via implicit ensembling.
  - Attention + multi-track architectures reduce reliance on deep MSAs (mirrors AF2 behaviour).
- **[RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md))** — *modalities: protein-structure*
  - Generalist training does **not** degrade protein-only accuracy.
  - Small (~4 pt) cost on NA complexes from generalist training.
  - Training with ligand context **improves** protein-only prediction (pocket flips, domain shifts).
  - Most of RFAA's "loss" vs physics docking comes from also predicting backbone+sidechains from sequence.

### Single-Cell RNA (12)

- **[CellPLM](https://doi.org/10.1101/2023.10.03.560734) ([note](notes/cellplm-pre-training-of-2023.md))** — *modalities: scrna*
  - Mixture-of-Gaussian prior is the single most important design choice — swapping to vanilla Gaussian is worse than dropping the latent distribution entirely, showing an ill-suited prior actively harms heterogeneous pretraining.
  - Transformer encoder matters chiefly for spatial imputation tasks (corr 0.318 → 0.244 on Lung when removed) and is near-neutral for cell-type classification on dissociated scRNA-seq.
- **[Geneformer](https://doi.org/10.1038/s41586-023-06139-9) ([note](notes/transfer-learning-enables-predictions-2023.md))** — *modalities: scrna*
  - Relevance of fine-tuning data dominates quantity — 884 disease-context cells outperform 30k generic cells, demonstrating context-appropriate curation yields larger gains than scale.
  - Pretraining corpus size improves downstream performance monotonically with no saturation on harder tasks; random initialisation collapses on small fine-tuning sets.
  - Length-grouped dynamic padding achieves 29.4× throughput speedup without quality loss.
  - In-silico perturbation (zero-shot deletion/activation) recovers known TF synergy and identifies experimentally validated therapeutic targets.
- **[GenePT](https://doi.org/10.1101/2023.10.16.562533) ([note](notes/genept-a-simple-but-2023.md))** — *modalities: scrna*
  - Used to motivate the default (name+summary); name-only is surprisingly strong but full summary is preferred.
  - GenePT-GPT-3.5 is consistently best; BioLinkBert and Gene2vec are slightly less competitive; expression-derived embeddings trail.
  - Names-only is surprisingly strong on some tasks (gene nomenclature carries signal), but adding the summary helps overall.
  - Random ≈ chance; rules out that the gain is just from large embedding dimension.
- **[Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md))** — *modalities: scrna*
  - Spatial pretraining data is non-substitutable — scale of dissociated cells alone cannot recover spatial variation.
  - Diversity > raw count; orthology-aligned multi-species pretraining is required.
  - Capacity matters at SpatialCorpus-110M scale.
  - Rank-based encoding tolerates the limited-gene reality of MERFISH/Xenium/CosMx.
- **[scBERT](https://doi.org/10.1038/s42256-022-00534-z) ([note](notes/scbert-as-a-large-2022.md))** — *modalities: scrna*
  - MLM pre-training on PanglaoDB is the single most important design choice; gene-as-token Performer alone is not enough.
  - The model relies on distributed gene–gene interaction patterns, not on a small set of marker genes — robust to marker dropout / batch loss.
  - Contextual encoding adds cell-type-discriminative information on top of the static Gene2vec positional prior.
  - 5 bins is sufficient; finer expression discretisation gives no measurable gain at this scale.
- **[scELMo](https://arxiv.org/abs/2601.05648) ([note](notes/open-world-knowledge-aided-2026.md))** — *modalities: scrna, single-cell-multiomics*
  - LLM-enriched cell text via RAG adds consistent performance gains on top of original text descriptions.
  - Cross-modal Robust Alignment (CRA) combining sample reliability, curriculum learning, and coupled momentum contrastive learning is necessary for noise robustness.
  - Integration of noise-robust cross-modal alignment and open-world LLM/RAG descriptions are complementary and both contribute additively to performance.
- **[scFoundation](https://doi.org/10.1038/s41592-024-02305-7) ([note](notes/large-scale-foundation-model-2024.md))** — *modalities: scrna*
  - The learned `[S]` token (used as the default cell embedding) and the max-pool variant outperform mean-pool and raw concat; `[S]` is selected as the canonical cell representation (`ablation-00.ipynb`).
  - Continuous scalar embedding preserves fine expression magnitudes and beats binned tokens, justifying xTrimoGene's MLP value embedder over vocab-based binning (`ablation-01.ipynb`).
  - Continuous regression loss applied to the full gene set yields the best clustering, supporting the published recipe (`ablation-01.ipynb`).
  - Removing RDA collapses the enhancement gain over SAVER/MAGIC/scImpute; RDA is the key driver of the imputation/enhancement SOTA and of the model's ability to operate at arbitrary target depths (`ablation-02.ipynb` + `enhancement/`).
- **[scGPT](https://doi.org/10.1038/s41592-024-02201-0) ([note](notes/scgpt-toward-building-a-2024.md))** — *modalities: scrna, single-cell-multiomics*
  - Generative attention masking with genes sorted by expression value outperforms BERT-style random masking for cell-type annotation and enables generation tasks.
  - Organ-specific pretrained checkpoints can outperform whole-human models when fine-tuning data matches tissue context.
  - Continual pretraining on the whole-human model improves zero-shot cell embedding performance compared to the standard checkpoint.
- **[SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md))** — *modalities: scrna*
  - Lower β (more MSE) → better query; higher β (more triplet) → better integration. Selected β=0.001, α=0.05 as best joint operating point.
  - Pure triplet collapses within-type variance; MSE term required to preserve subtle cell-state differences.
  - SCimilarity ρ=0.77 vs scFoundation 0.54, scGPT 0.59; far fewer false-high cells.
  - Higher cell-type ASW, comparable graph connectivity, less spurious cross-study mixing; SCimilarity does not see test data, baselines do.
- **[scMamba](https://arxiv.org/abs/2506.20697) ([note](notes/scmamba-a-scalable-foundation-2025.md))** — *modalities: scrna, single-cell-multiomics*
  - Processing all raw genes and peaks without highly variable feature selection yields the best integration performance, unique to scMamba since competing methods fail to benefit from high-dimensional sparse inputs.
  - Patch-based tokenization grouped by genomic region enables processing of tens of thousands of features (e.g. 173k peaks) compared to gene-as-token approaches limited to ~2,000 genes.
- **[scMulan](https://doi.org/10.1101/2024.01.25.577152) ([note](notes/scmulan-a-multitask-generative-2024.md))** — *modalities: scrna*
  - No explicit ablation studies found.
- **[UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md))** — *modalities: scrna*
  - 33-layer gives best biological-signal fidelity and cross-species generalisation; 4-layer is faster/cheaper but loses resolution on complex tissues. Embeddings are not interchangeable between the two.
  - Zero-shot embedding works on unseen species with available proteomes (e.g., green monkey, chicken); degrades on evolutionarily distant species (e.g., Drosophila).
  - ESM2 protein embeddings are the mechanism enabling species-agnostic, vocabulary-free tokenisation; required for cross-species transfer and for embedding novel/unseen genes.
  - Non-coding / missing-embedding genes are dropped; ablation motivates protein-embedding tokenisation as the core design choice.

### Computational Pathology (12)

- **[CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md))** — *modalities: imaging-pathology*
  - Best average zero-shot classification across 7 tasks.
  - Best average cross-modal retrieval; lower zero-shot classification than CoCa default.
  - Lower average zero-shot vs full human-only set — filtering too aggressively hurts.
  - Underperforms human-only filtered CoCa — quality filtering matters.
- **[CONCH (preprint)](https://arxiv.org/abs/2307.12914) ([note](notes/towards-a-visual-language-2023.md))** — *modalities: imaging-pathology, multimodal*
  - Adding the captioning loss to contrastive pretraining (CoCa) improves downstream zero-shot classification over CLIP-style contrastive-only.
  - Contrastive-only objective is slightly stronger for cross-modal retrieval; captioning loss helps classification more than retrieval.
  - Filtering out non-human animal histology helps; over-filtering down to H&E-only loses too much data and hurts performance — keep human-only.
  - Always ensemble class-name × template prompts at inference; ensembling cannot rescue a model that fundamentally fails on the task.
  - Pre-train each tower unimodally before vision-language alignment — critical for zero-shot transfer in histopathology.
- **[GigaPath](https://doi.org/10.1038/s41586-024-07441-w) ([note](notes/a-whole-slide-foundation.md))** — *modalities: imaging-pathology*
  - Slide-level MAE pretraining on 171 K WSIs is necessary; random init loses ~1.7 AUROC pts on subtyping.
  - Pretrained representations are strong enough to be used frozen — important for compute-limited deployment.
  - Long-range dilated self-attention adds value beyond a simple attention-MIL pooler; modelling cross-tile dependencies matters for subtyping.
  - DINOv2 is the best tile-level SSL recipe for pathology at this scale; supervised ImageNet transfer is clearly inferior, motivating SSL foundation models.
  - Data scale + diversity (real-world Providence corpus) drives gains beyond what TCGA alone delivers — evidence of (informal) data-scaling.
- **[H-optimus-0](https://arxiv.org/abs/2404.15217) ([note](notes/towards-large-scale-training-2024.md))** — *modalities: imaging-pathology*
  - Mixing magnifications yields a magnification-agnostic FM that beats any single-magnification model — no architectural change required.
  - Always warm-start pathology FMs from ImageNet weights — faster convergence and higher final accuracy.
  - OOD performance saturates fast on TCGA — more WSIs from same distribution mostly help in-distribution; need more diverse data to push OOD further.
  - Online patching's effectively-infinite patch sampling mainly benefits in-distribution learning; OOD is bottlenecked by slide diversity, not patch count.
- **[HIPT](https://arxiv.org/abs/2206.02647) ([note](notes/scaling-vision-transformers-to-2022.md))** — *modalities: imaging-pathology*
  - Freezing the pretrained region ViT is critical; unfreezing collapses NSCLC AUC from 0.952 to 0.786–0.820, confirming that small WSI cohorts cannot support end-to-end training.
  - Hierarchical self-supervised pretraining produces competitive representations without fine-tuning; mean-pooled ViT embeddings beat supervised CLAM-SB on BRCA and RCC subtyping.
  - Long-range spatial context matters most for survival prediction where tumour-stroma and immune localisation patterns are prognostically important, not for subtyping tasks.
  - Pan-cancer self-supervised pretraining outperforms organ-specific pretraining for cell-level localisation and downstream classification.
- **[KEP (KEEP)](https://arxiv.org/abs/2412.13126) ([note](notes/knowledge-enhanced-pretraining-for-2024.md))** — *modalities: imaging-pathology*
  - KEEP wins on 16/18 datasets; +~10% AUROC on PANDA and +12.9% on AGGC22 segmentation; better on 6/7 detection benchmarks; better on all subtyping benchmarks.
  - KEEP-Top100 ≥ Contrastive-Top100 on 6/8; +11 points BACC on rare-tumor EBRAINS dataset.
  - Ratio strategy wins on all datasets; +0.10 BACC on CPTAC-NSCLC (0.860) and +0.15 on TCGA-BRCA (0.774).
  - Semantic grouping improves retrieval (details in Table S5).
- **[Phikon-v2](https://arxiv.org/abs/2409.09173) ([note](notes/phikon-v2-a-large-2024.md))** — *modalities: imaging-pathology*
  - DINOv2 + larger model + larger data jointly outperform iBOT baseline; method/scale confounded.
  - Domain-specific pre-training is by far the largest single contributor; natural-image DINOv2 ranks last.
  - "DINOv2 superiority over iBOT is not straightforward for lighter models" — method advantage depends on scale.
  - A 13× smaller, 350× less-data, task-specialized model beats or matches the largest FMs on MSI; scaling is not a universal solution for biomarker tasks.
- **[RudolfV](https://arxiv.org/abs/2401.04079) ([note](notes/rudolfv-a-foundation-model-2024.md))** — *modalities: imaging-pathology*
  - Pathologist-guided data curation (grouping, clustering, balanced sampling) enables competitive performance with ~10× less data than Virchow while outperforming similar-scale UNI on 10/12 benchmarks.
  - Cross-tissue generalisation is significantly enhanced by the foundation model; TME cell classifier trained on NSCLC generalises to other tissues with 65.5% balanced accuracy vs 36.2% without.
  - Including IHC and special stains in SSL training provides 21.6% average improvement in IHC cell classification compared to H&E-only models.
- **[UNI](https://arxiv.org/abs/2308.15474) ([note](notes/a-general-purpose-self-2023.md))** — *modalities: imaging-pathology*
  - SSL in pathology benefits from data scale up to ≥100M patches / 100K WSIs; no saturation observed at 100K-slide scale.
  - DINOv2 + ViT-L + 100K-slide diverse pretraining beats both ImageNet-supervised CNNs and prior pathology SSL (CTransPath, REMEDIS) despite UNI seeing 4–13× fewer total images.
  - Strong SSL features give large label-efficiency wins from K≥4; 1-shot remains noisy across all encoders.
  - Class-prototype (parameter-free) probes work extremely well with high-quality SSL features; representation quality dominates over classifier complexity.
  - DINOv2-style high-res pretraining yields resolution-agnostic features; advantage of UNI grows at native histology magnifications.
- **[uniGradICON](https://arxiv.org/abs/2403.05780) ([note](notes/unigradicon-a-foundation-model-2024.md))** — *modalities: imaging-pathology*
  - Weaker GradICON regularizer is what enables a single universal registration model; diffusion-regularized variants underperform or fail.
  - One universal model matches specialists in-domain and dominates them out-of-domain.
  - IO is a cheap, always-on improvement; pairs naturally with the FM as a strong initialization.
  - Model generalizes to unseen anatomy, though including the region in pretraining is clearly better; IO mitigates the held-out gap.
- **[Virchow](https://arxiv.org/abs/2309.07778) ([note](notes/virchow-a-million-slide-2023.md))** — *modalities: imaging-pathology*
  - In-domain pathology data scale is the single largest lever; Virchow (1.5M WSIs) gains +0.067 weighted F1 over natural-image DINOv2 pretraining, with the gap widening for smaller pathology FMs.
  - Stain-normalisation removal costs only −0.005 F1, confirming that million-scale in-domain SSL provides learned stain robustness almost inherently.
  - Extended LR warmup (495k iterations, 5× default) was necessary for stable convergence at this million-scale data regime.
- **[XrayGPT](https://arxiv.org/abs/2306.07971) ([note](notes/xraygpt-chest-radiographs-summarization-2023.md))** — *modalities: imaging-pathology*
  - Domain-specific LLM adaptation dominates gains; swapping CLIP to MedCLIP adds ~2 ROUGE-1 points, while medical/radiology-specific Vicuna fine-tuning adds ~17 more points for a total +19 over MiniGPT-4 baseline.

### Radiology (2)

- **[MedDiff-FM](https://arxiv.org/abs/2410.15432) ([note](notes/meddiff-fm-a-diffusion-2024.md))** — *modalities: imaging-radiology*
  - Multi-level (image+patch) integration is the single most impactful design choice, delivering ~70% of overall FID reduction and the largest Dice improvement across all anatomical regions.
  - Position coordinate encoding via sinusoidal (NeRF-style) embeddings outperforms raw coordinate channels and provides consistent gains.
  - Pre-training transfer is decisive on data-scarce targets; mediastinal lymph node Dice improves from 0.01 (from scratch) to 0.22 (fine-tuned), and lung inpainting from 0.42 to 0.77.
- **[MedMax](https://arxiv.org/abs/2412.12661) ([note](notes/medmax-mixed-modal-instruction-2024.md))** — *modalities: imaging-radiology, imaging-pathology, multimodal*
  - MedMax is high-quality; further scaling should keep paying off.
  - High-quality VQA data is essential for VQA performance.
  - Visual-chat data is critical for chat performance; mixture diversity drives generalization.
  - Distribution shift in discrete visual tokens hurts the frozen LM backbone — keep the base tokenizer.

### Cell Imaging (1)

- **[CellPainTR](https://arxiv.org/abs/2509.06986) ([note](notes/cellpaintr-generalizable-representation-learning-2025.md))** — *modalities: imaging-cell, cell-profiling*
  - The multi-stage curriculum is essential; Stage 1 (self-supervised) maximises batch correction but discards biological structure, Stage 2 restores it, and only the full three-stage approach balances both.
  - Inter-source contrastive learning recovers batch correction capacity (aggregated score 0.68 → 0.76) while maintaining biological signal quality.
  - The model is robust to extreme feature dropout; zero-padding ~94% missing features on OOD data still yields 0.40 Overall score vs 0.26 for classical baselines.

### Microscopy (1)

- **[ViTally](https://arxiv.org/abs/2411.02572) ([note](notes/vitally-consistent-scaling-biological-2024.md))** — *modalities: imaging-microscopy*
  - Scaling continues to pay off into the billion-param regime; CM (replicate consistency) gains faster than raw recall.
  - Curating to ~16M morphologically-active crops matches a much larger un-curated set on consistency; data quality > quantity.
  - Smaller patches help on cellular morphology, justifying the G/8 choice despite cost.
  - Even smallest microscopy-trained CA-MAE beats much larger natural-image ViTs — domain SSL dominates.

### Small Molecules (5)

- **[ChemBERTa](https://arxiv.org/abs/2010.09885) ([note](notes/chemberta-large-scale-self-2020.md))** — *modalities: small-molecule*
  - Downstream performance scales consistently with more pretraining data; MLM learns more robust representations at larger scale.
  - Semantically-relevant SMILES tokenization gives a small edge over BPE, but margin is narrow and needs more benchmarks.
  - Despite SELFIES' 100% validity guarantee, it offers no measurable advantage here; further benchmarking needed.
- **[ChemFM](https://arxiv.org/abs/2410.21422) ([note](notes/chemfm-as-a-scaling-2024.md))** — *modalities: small-molecule*
  - UniChem is a more informative pre-training corpus than ZINC20, winning on 9/11 downstream datasets often by large margins.
  - Model-size scaling follows power-law behaviour up to ~200M parameters on informative data, but shows diminishing returns beyond 1B.
  - Pre-training provides substantial downstream improvements across ADMET tasks, outperforming random initialisation by 40–80%.
  - LoRA fine-tuning achieves comparable performance to full-parameter fine-tuning while drastically reducing memory for 3B models.
- **[LSM-MS2](https://arxiv.org/abs/2510.26715) ([note](notes/lsm-ms2-a-foundation-2025.md))** — *modalities: small-molecule*
  - Learned embedding-space retrieval outperforms cosine similarity and DreaMS on both spectral identification and true-positive/false-positive separation.
  - LSM-MS2 achieves 30% more correct isomer identifications than baselines without explicit isomer supervision, demonstrating fragmentation-level representations capture fine-grained chemical discrimination.
  - Fragmentation information (MS/MS) is necessary for pharmaceutical discrimination — MS1-only precursor mass fails to separate similar drug groups while LSM-MS2 succeeds.
- **[MACE-OFF / Multi-Fi](https://arxiv.org/abs/2412.13088) ([note](notes/taming-multi-domain-fidelity-2024.md))** — *modalities: small-molecule*
  - Both stages of TEA are needed: ICEA removes inner-core/basis offsets, AEC then corrects atomization-energy/functional offsets — full pipeline is what unlocks dataset fusion.
  - Scaling MACE-Osaka24 from small→large gives ~0.24 kcal/mol gain, reaching MACE-OFF23-large quality (0.403) on organics.
  - Large variant best on reactive organic chemistry; ~20–30% MAE drop.
  - Marginal gain on crystals; small already competitive with MACE-MP-0-large (0.0166).
- **[MolFM](https://arxiv.org/abs/2307.09484) ([note](notes/molfm-a-multimodal-molecular-2023.md))** — *modalities: small-molecule, multimodal*
  - Cross-modal attention to atom-level molecular features is the single largest controllable component, with removal causing −2.8 average R@1 — larger than knowledge graph removal.
  - Cross-modal matching (CMM) pre-training objective is as critical as atomic attention (−2.8 R@1 loss), confirming fine-grained substructure-text alignment drives gains.
  - Knowledge graph input contributes modestly (~1.5% improvement); combined with CMM removal, both losses compound to −4.3 points.

### Multimodal Medical (4)

- **[AIDO](https://doi.org/10.1101/2024.12.02.626322) ([note](notes/aido-accurate-model-of-2024.md))** — *modalities: multimodal*
  - Mixture-of-Experts (8 experts, top-2 routing) in AIDO.Protein-16B matches dense FFN performance at ~28% active parameters, enabling 16B scale at half the per-token FLOPs.
  - Multi-corpus pre-training (UniRef90 + ColabFoldDB) followed by UR90 refinement outperforms single-corpus pretraining for both fitness and structure-conditioned generation.
  - Read-Depth-Aware objective in AIDO.Cell improves zero-shot clustering and perturbation prediction over standard masked expression.
  - Auto-discretisation of continuous gene expression into tokens outperforms naive continuous regression and enables MLM-style training.
- **[ConceptCLIP](https://arxiv.org/abs/2501.15579) ([note](notes/an-explainable-biomedical-foundation-2025.md))** — *modalities: multimodal*
  - Region-Concept Alignment (RC-Align) loss during pre-training provides the dominant gain (+3.76% AUC) compared to local-region information at inference (+1.78% AUC).
  - RC-Align is especially important for cross-modality transfer — removing it causes the largest drop on BrainTumorCT (−7.7 AUC).
- **[Doctor Sun](https://arxiv.org/abs/2508.08270) ([note](notes/doctor-sun-a-bilingual-2025.md))** — *modalities: multimodal*
  - Mixing general data in alignment prevents catastrophic forgetting at negligible domain cost.
  - 1:0.5 is the sweet spot for medical VQA; more general data only helps generic benchmarks.
  - Pure-domain alignment causes catastrophic forgetting of general perception/reasoning.
  - Specialised answers, but recall drop is unsafe for clinical missed-diagnosis risk.
- **[LLaVA-Med](https://arxiv.org/abs/2306.00890) ([note](notes/llava-med-training-a-2023.md))** — *modalities: multimodal*
  - Biomedical curriculum tuning yields large gains over general-domain LLaVA, especially zero-shot.
  - Stage 1 (caption alignment) alone collapses instruction-following; Stage 2 instruction-tuning is essential.
  - Performance improves monotonically with more self-instruct data.
  - Using PubMed inline mentions as external knowledge during GPT-4 self-instruct improves data quality.

### Vision (Biomedical) (1)

- **[BiomedCLIP](https://arxiv.org/abs/2303.00915) ([note](notes/biomedclip-a-multimodal-biomedical-2023.md))** — *modalities: vision, language, multimodal*
  - Domain-specific text encoder (PubMedBERT with 256-token context) is the single largest controllable lever, providing ~9 points R@1 improvement over CLIP's GPT-2/77-token baseline.
  - Context length expansion from 77 → 256 tokens contributes +4.5 R@1 independent of encoder swap, indicating biomedical captions are significantly longer and truncation is costly.
  - Validation gains do not transfer downstream: 384 px resolution improves validation by +1.7 R@1 but degrades zero-shot classification by −5.15 points.
  - Batch size plateaus at 4k for the 15M-pair dataset; scaling to 64k provides no downstream benefit, suggesting dataset size is the bottleneck.

### Biomedical Text (1)

- **[BioBERT](https://arxiv.org/abs/1901.08746) ([note](notes/biobert-a-pre-trained-2019.md))** — *modalities: text*
  - Continued pre-training on PubMed is the dominant gain; adding PMC gives diminishing returns once PubMed steps are scaled up.
  - Even vanilla BERT beats the prior CHEMPROT SOTA; biomedical pre-training adds a further ~3 F1.
  - QA benefits most from biomedical pre-training (+12.24 MRR over SOTA, +5.13 over BERT) — largest relative gain among the three task families.
  - 1B words already captures most of the benefit; full PubMed (4.5B) yields modest extra gains.

### Other (2)

- **[BioGPT](https://arxiv.org/abs/2210.10341) ([note](notes/biogpt-generative-pre-trained-2022.md))** — *modalities: other*
  - Natural-language target formats beat structured formats with special tokens; rel-is ("the relation between H and T is R") is best.
  - Confirms rel-is generalises across datasets (+~2 F1).
  - Soft prompts > hard prompts; among hard prompts, more informative wording ("we can conclude that") is better.
  - Performance roughly insensitive to soft-prompt length; length=9 chosen via val set, length=13 marginally best on test.
- **[Virchow2](https://arxiv.org/abs/2408.00738) ([note](notes/virchow2-scaling-self-supervised-2024.md))** — *modalities: other*
  - Extended Context Translation (ECT) and Knowledge-Density-Entropy (KDE) regularisation are individually weak or harmful on OOD tasks but synergistic when combined, yielding +3.4 in-domain and +1.9 OOD F1 gains over standard DINOv2.
  - Domain-specific augmentation and entropy regularisation show coupling effects where individual components underperform but the full recipe together substantially improves performance.

## Appendix: Verification Pass (Rev 3)

To reduce overconfidence, the 14 most-cited papers in this guidebook (≥5 citations) underwent an **independent claim-by-claim verification pass** by separate Opus-4.6 fact-checker agents. Each agent re-read the source paper (or augmented abstract+repo) and judged every claim citing that paper as `supported`, `partial`, `unsupported`, or `out-of-scope`. Results:

| Paper | Cites | Issues |
|---|---|---|
| highly-accurate-protein-structure-2021 (AlphaFold 2) | 11 | 2 partial — fixed in this revision (recycling vs. FAPE attribution; AF2 crop size in context table) |
| evolutionary-scale-prediction-of-2023 (ESM-2 / ESMFold) | 11 | 0 |
| sequence-modeling-and-design-2024 (Evo) | 9 | 0 |
| the-nucleotide-transformer-building-2024 (NT) | 8 | 0 |
| prottrans-towards-cracking-the-2020 (ProtTrans) | 7 | 0 |
| a-whole-slide-foundation (GigaPath) | 7 | 0 |
| towards-a-visual-language-2023 (CONCH) | 6 | 0 |
| scgpt-toward-building-a-2024 (scGPT) | 6 | 0 |
| protein-representation-learning-by-2022 (GearNet) | 6 | 0 |
| helixfold-single-msa-free-2022 (HelixFold-Single) | 6 | 0 |
| effective-gene-expression-prediction-2021 (Enformer) | 6 | 0 |
| biological-structure-and-function-2021 (ESM-1b) | 6 | 0 |
| a-general-purpose-self-2023 (UNI) | 6 | 0 |
| accurate-prediction-of-protein-2021 (RoseTTAFold) | 6 | 0 |

Per-paper verification details are appended to each note as a `## Verification (Rev 3)` section. Lower-cited papers (1-4 citations, 22 papers) were not verified individually — they should be revisited in a future revision.

## Appendix: Rev 4 Changelog

**What changed in Rev 4.**

1. **15 newly-extracted FMs added.** [GET](https://doi.org/10.1038/s41586-024-08391-z) ([note](notes/a-foundation-model-of-2025.md)) (GET), [Evo 2](https://doi.org/10.1101/2025.02.18.638918) ([note](notes/genome-modeling-and-design-2025.md)) (Evo 2), [ESM-3](https://doi.org/10.1101/2024.07.01.600583) ([note](notes/simulating-500-million-years-2024.md)) (ESM-3), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) ([note](notes/accurate-structure-prediction-of-2024.md)) (AlphaFold 3), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) ([note](notes/generalized-biomolecular-modeling-and-2024.md)) (RFAA), [ProteinMPNN](https://doi.org/10.1126/science.add2187) ([note](notes/robust-deep-learning-based-2022.md)) (ProteinMPNN), [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) ([note](notes/nicheformer-a-foundation-model-2024.md)) (Nicheformer), [UCE](https://doi.org/10.1101/2023.11.28.568918) ([note](notes/universal-cell-embeddings-a-2023.md)) (UCE), [CellPLM](https://doi.org/10.1101/2023.10.03.560734) ([note](notes/cellplm-pre-training-of-2023.md)) (CellPLM), [GenePT](https://doi.org/10.1101/2023.10.16.562533) ([note](notes/genept-a-simple-but-2023.md)) (GenePT), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) ([note](notes/scimilarity-rapid-annotation-of-2023.md)) (SCimilarity), [scMulan](https://doi.org/10.1101/2024.01.25.577152) ([note](notes/scmulan-a-multitask-generative-2024.md)) (scMulan), [AIDO](https://doi.org/10.1101/2024.12.02.626322) ([note](notes/aido-accurate-model-of-2024.md)) (AIDO), [Virchow2](https://arxiv.org/abs/2408.00738) ([note](notes/virchow2-scaling-self-supervised-2024.md)) (Virchow2), [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) ([note](notes/a-visual-language-foundation-2024.md)) (CONCH NatMed).

2. **85 papers re-classified as not-FM.** TAPE, CLAM, scVI, totalVI, Cellpose, CellRanger, BERT, GPT-2, and other supporting methods/benchmarks are now excluded from primary `(N=X)` tallies. They may still appear as named baselines in prose.

3. **84 ablation tables consulted.** Every FM note now carries a `## Ablations (Rev 4)` section; this guidebook quotes one or more findings per design axis directly from those tables.

4. **New axes broken out.** *MSA vs MSA-free* and *Distillation from AlphaFold predictions* are now first-class axes (previously folded into *Architecture* and *Data*).

5. **New modality recipe.** Spatial transcriptomics is broken out from scRNA, anchored on Nicheformer.

6. **New executive take-aways.** Two added in Rev 4: take-away 11 (pretraining-time conditioning beats post-hoc fine-tuning) and take-away 12 (benchmark fragility under fair baselines / leakage correction).

7. **Citation format.** Every empirical claim now carries `[short-name](URL)` links with `**(N=X papers)**` evidence counts restricted to the 84 FM corpus. Non-FM baselines are referenced inline without contributing to N.

**Biggest substantive shifts vs Rev 3.**

- Confirmed ESM-2 scaling claim with the Rev 3 verification fix; added ESM-3 multimodal-token complement.
- Pathology section reorganised around DINOv2 + slide diversity (UNI / Virchow2 / GigaPath / RudolfV / H-optimus-0).
- AlphaFold 3 + RoseTTAFold All-Atom now anchor heteroatom complex modelling alongside MSA-conditioned protein-only AF2/RoseTTAFold.
- Single-cell section adds explicit fair-baseline caveat backed by 8 FM papers; spatial transcriptomics broken out as its own modality.
- New axis 11 (Distillation from AlphaFold predictions) consolidates a previously scattered finding into a single quoted-ablation table.
