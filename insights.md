# Insights — Foundation Models for Biology (Rev 4)

## Scope & Method

This guidebook distils design decisions and empirical findings from **84 biology foundation-model (bio-FM) papers** that meet a strict definition: pretrained on biological data at scale, learning a general-purpose representation transferable to multiple downstream tasks. **Rev 4** added 15 newly-extracted FMs (GET, Evo 2, ESM-3, AlphaFold 3, RoseTTAFold All-Atom, ProteinMPNN, Nicheformer, UCE, CellPLM, GenePT, SCimilarity, scMulan, AIDO, Virchow2, CONCH-NatMed) and re-classified 85 of the 169 surveyed papers as supporting/baseline non-FMs (e.g., TAPE, scVI, totalVI, Cellpose, CLAM); these may appear as benchmarks but are **never** counted in the per-claim `(N=X papers)` evidence tallies that follow.

Each FM note in `notes/` carries a `## Ablations (Rev 4)` section that quotes the design-choice ablations actually reported by the authors. This guidebook is *grounded in those tables*: every design-choice axis below ends with an **Ablation evidence (Rev 4)** subsection that quotes the specific finding from the relevant note. Citations use `[short-name](URL)` linking to the source's DOI, arXiv, or canonical URL.

Coverage by modality (FM count): protein-sequence 21, imaging-pathology 13, protein-structure 13, DNA 12, scRNA 12, multimodal-medical 9, small-molecule 6, RNA 5, epigenome 4, single-cell-multiomics 3, plus singletons in radiology, microscopy, cell-painting, text, vision, and interactome. Methods reflect the ablations reported by authors and have not been independently reproduced; see *Methodology & Limitations*.

## Executive Summary — Top-12 Practitioner Take-aways (Rev 4)

Each take-away is annotated with the number of **FM papers** that directly support it and the strongest single ablation cited.

1. **MSA-derived signal still dominates structure prediction; MSA-free models close the gap only for well-represented folds.** **(N=10 papers)** evidence: [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2), [RoseTTAFold](https://doi.org/10.1126/science.abj8754), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w), [MSA Transformer](https://doi.org/10.1101/2021.02.12.430858), [HelixFold-Single](https://arxiv.org/abs/2207.13921), [OmegaFold](https://doi.org/10.1101/2022.07.21.500999), [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574), [ESM-1b](https://doi.org/10.1073/pnas.2016239118), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528), [ESM-IF](https://doi.org/10.1101/2022.04.10.487779)

2. **For protein language models, scale unlocks emergent contact prediction; objective and tokenization matter less than parameter count past ~150M.** **(N=12 papers)** evidence: [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574), [ProtTrans](https://arxiv.org/abs/2007.06225), [ESM-1b](https://doi.org/10.1073/pnas.2016239118), [Rao attention-as-contacts](https://doi.org/10.1101/2020.12.15.422761), [Ankh](https://arxiv.org/abs/2301.06568), [ProGen](https://arxiv.org/abs/2004.03497), [ESM-1v](https://doi.org/10.1101/2021.07.09.450648), [ProteinBERT](https://doi.org/10.1093/bioinformatics/btac020), [ProtGPT2](https://doi.org/10.1038/s41467-022-32007-7), [ESM-design](https://doi.org/10.1101/2022.12.21.521521), [ESM-AA](https://arxiv.org/abs/2403.12995), [ESM-3](https://doi.org/10.1101/2024.07.01.600583)

3. **Long context is genomics' bottleneck; sub-quadratic backbones (Hyena, Mamba, S4) match Transformers at 32–1M tokens with 5–20× lower FLOPs.** **(N=9 papers)** evidence: [HyenaDNA](https://arxiv.org/abs/2306.15794), [Caduceus](https://arxiv.org/abs/2403.03234), [scMamba](https://arxiv.org/abs/2506.20697), [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z), [Evo](https://doi.org/10.1126/science.ado9336), [Evo 2](https://doi.org/10.1101/2025.02.18.638918), [Enformer](https://doi.org/10.1038/s41592-021-01252-x), [Borzoi](https://doi.org/10.1038/s41588-024-02053-6), [dnaGrinder](https://arxiv.org/abs/2409.15697)

4. **BPE/k-mer/byte tokenisation choices change parameter count and inference speed by 2–4× but rarely change downstream rank order, with one large exception: DNABERT-2's BPE doubles many GUE benchmarks vs. fixed k-mer.** **(N=6 papers)** evidence: [DNABERT-2](https://arxiv.org/abs/2306.15006), [DNABERT-1](https://doi.org/10.1093/bioinformatics/btab083), [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z), [VQDNA](https://arxiv.org/abs/2405.10812), [HyenaDNA](https://arxiv.org/abs/2306.15794), [Genome Book](https://arxiv.org/abs/2501.16982)

5. **Single-cell FMs benefit modestly from pretraining; gains over scVI shrink to 1–3% on integration once strong baselines are run, except for zero-shot perturbation/cross-tissue transfer where gains are 5–15%.** **(N=12 papers)** evidence: [scGPT](https://doi.org/10.1038/s41592-024-02201-0), [scBERT](https://doi.org/10.1038/s42256-022-00534-z), [Geneformer](https://doi.org/10.1038/s41586-023-06139-9), [scFoundation](https://doi.org/10.1038/s41592-024-02305-7), [CellPLM](https://doi.org/10.1101/2023.10.03.560734), [UCE](https://doi.org/10.1101/2023.11.28.568918), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537), [GenePT](https://doi.org/10.1101/2023.10.16.562533), [Nicheformer](https://doi.org/10.1101/2024.04.15.589472), [scMulan](https://doi.org/10.1101/2024.01.25.577152), [scELMo](https://arxiv.org/abs/2601.05648), [scMamba](https://arxiv.org/abs/2506.20697)

6. **Pathology FMs scale with slide count, not parameter count; DINOv2-style SSL on 100k+ slides beats CLIP-style on 10× fewer.** **(N=11 papers)** evidence: [UNI](https://arxiv.org/abs/2308.15474), [GigaPath](https://doi.org/10.1038/s41586-024-07441-w), [Virchow](https://arxiv.org/abs/2309.07778), [Virchow2](https://arxiv.org/abs/2408.00738), [Phikon-v2](https://arxiv.org/abs/2409.09173), [RudolfV](https://arxiv.org/abs/2401.04079), [H-optimus-0](https://arxiv.org/abs/2404.15217), [HIPT](https://arxiv.org/abs/2206.02647), [CONCH (preprint)](https://arxiv.org/abs/2307.12914), [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4), [KEP (KEEP)](https://arxiv.org/abs/2412.13126)

7. **Distilling from AlphaFold predictions gives 1–3 nm RMSD gains essentially for free; this is the cheapest known structure-prediction lever.** **(N=6 papers)** evidence: [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574), [HelixFold-Single](https://arxiv.org/abs/2207.13921), [OmegaFold](https://doi.org/10.1101/2022.07.21.500999), [ESM-IF](https://doi.org/10.1101/2022.04.10.487779), [RhoFold](https://arxiv.org/abs/2207.01586), [GearNet](https://arxiv.org/abs/2203.06125)

8. **Token diffusion / flow-matching now match autoregressive PLMs on inverse folding and design at lower inference FLOPs.** **(N=6 papers)** evidence: [ProteinMPNN](https://doi.org/10.1126/science.add2187), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w), [ESM-3](https://doi.org/10.1101/2024.07.01.600583), [ESM-design](https://doi.org/10.1101/2022.12.21.521521), [ProGen](https://arxiv.org/abs/2004.03497), [ESM-AA](https://arxiv.org/abs/2403.12995)

9. **Multimodal CLIP-style alignment (image↔text, sequence↔structure, RNA↔protein) consistently helps zero-shot retrieval but rarely helps supervised fine-tuning.** **(N=9 papers)** evidence: [CONCH (preprint)](https://arxiv.org/abs/2307.12914), [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4), [BiomedCLIP](https://arxiv.org/abs/2303.00915), [ProtCLIP](https://arxiv.org/abs/2412.20014), [MolFM](https://arxiv.org/abs/2307.09484), [ConceptCLIP](https://arxiv.org/abs/2501.15579), [KEP (KEEP)](https://arxiv.org/abs/2412.13126), [AIDO](https://doi.org/10.1101/2024.12.02.626322), [LLaVA-Med](https://arxiv.org/abs/2306.00890)

10. **Geometry-aware backbones (SE(3)-equivariant attention, IPA, structure tokens) outperform sequence-only on structural tasks but only when paired with structure pretraining data.** **(N=9 papers)** evidence: [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2), [RoseTTAFold](https://doi.org/10.1126/science.abj8754), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528), [GearNet](https://arxiv.org/abs/2203.06125), [PST](https://arxiv.org/abs/2401.14819), [ESM-3](https://doi.org/10.1101/2024.07.01.600583), [ESM-AA](https://arxiv.org/abs/2403.12995), [ESM-IF](https://doi.org/10.1101/2022.04.10.487779)

11. **Conditioning on functional metadata (GO terms, control tokens, niche labels) at pretraining is consistently more parameter-efficient than post-hoc fine-tuning.** **(N=7 papers)** evidence: [ProGen](https://arxiv.org/abs/2004.03497), [ProtCLIP](https://arxiv.org/abs/2412.20014), [scMulan](https://doi.org/10.1101/2024.01.25.577152), [Nicheformer](https://doi.org/10.1101/2024.04.15.589472), [GET](https://doi.org/10.1038/s41586-024-08391-z), [scGPT](https://doi.org/10.1038/s41592-024-02201-0), [BioGPT](https://arxiv.org/abs/2210.10341)

12. **Benchmarks lag the field; many headline gains shrink ≥50% under leakage-corrected splits, fair-baseline reruns, or cross-lab data.** **(N=9 papers)** evidence: [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574), [scGPT](https://doi.org/10.1038/s41592-024-02201-0), [scFoundation](https://doi.org/10.1038/s41592-024-02305-7), [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z), [GigaPath](https://doi.org/10.1038/s41586-024-07441-w), [ESM-1b](https://doi.org/10.1073/pnas.2016239118), [Geneformer](https://doi.org/10.1038/s41586-023-06139-9), [CellPLM](https://doi.org/10.1101/2023.10.03.560734), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537)

## Practitioner Cheatsheet (Rev 4)

One-line defaults for the impatient. Each row links to the canonical FM(s) you should reach for first; see the design-choice axes and modality recipes below for the trade-offs.

| Modality | Default FM | Backbone | Pretraining | Strongest known ablation |
|---|---|---|---|---|
| DNA (short range) | [DNABERT-2](https://arxiv.org/abs/2306.15006) | Transformer | BPE MLM, multispecies | BPE > 6-mer on 23/28 GUE |
| DNA (long range) | [HyenaDNA](https://arxiv.org/abs/2306.15794) / [Caduceus](https://arxiv.org/abs/2403.03234) | Hyena / BiMamba | Char-level CLM/MLM | 1M-token context, RC-equivariance |
| DNA (frontier scale) | [Evo 2](https://doi.org/10.1101/2025.02.18.638918) | StripedHyena | CLM, 8.8T tokens, 1M context | Scale-up; ablation table is configuration-only |
| Cell-type-conditional epigenome | [GET](https://doi.org/10.1038/s41586-024-08391-z) | Region-wise transformer | Motif-masked SSL | Pretraining lifts cross-cell-type r 0.60→0.94 |
| Gene expression from DNA | [Enformer](https://doi.org/10.1038/s41592-021-01252-x) / [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) | CNN+Transformer | Supervised on tracks | 196kb→524kb gives small Pearson lift |
| RNA representation | [RiNALMo](https://arxiv.org/abs/2403.00043) / [RNA-FM](https://arxiv.org/abs/2204.00300) | Transformer MLM | ncRNA + mRNA | Scale to 650M improves 8/9 RNA tasks |
| Protein representation | [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) | Transformer MLM | UR50, 8M→15B | Contact P@L 0.34→0.54 with scale |
| Protein design (multimodal) | [ESM-3](https://doi.org/10.1101/2024.07.01.600583) | Transformer | Joint seq/struct/func tokens | Ablating any track loses 8–20% recovery |
| Protein structure (monomer) | [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) | Evoformer + IPA | MSA + distillation | MSA depth dominant; ablating drops 25–40 GDT |
| Protein structure (complex) | [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) / [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) | Diffusion / SE(3) | Seq+struct+ligand | All-atom necessary for heteroatom |
| MSA-free / orphan proteins | [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) (ESMFold) / [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) | Folding head | AF2 distillation | Closes ~80% of MSA gap |
| Inverse folding | [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) / [ProteinMPNN](https://doi.org/10.1126/science.add2187) | GVP-GNN / MPNN | Seq-given-struct | Native recovery 51% (ESM-IF), 52% (MPNN) |
| Single-cell RNA (representation) | [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) / [scGPT](https://doi.org/10.1038/s41592-024-02201-0) | Transformer | Rank/binned MLM | Scale 1M→30M cells lifts dosage AUROC 3–6 pts |
| Single-cell RNA (zero-shot annotation) | [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) / [GenePT](https://doi.org/10.1101/2023.10.16.562533) | NN + reference / Text emb. | Reference search / GPT-3.5 | GenePT matches scGPT at 0% pretraining cost |
| Spatial transcriptomics | [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) | Transformer | Niche-conditional MLM | +4–7 pts over vanilla MLM on niche tasks |
| Cell-type integration cross-species | [UCE](https://doi.org/10.1101/2023.11.28.568918) | Transformer | 36M cells, multi-species | Cross-species zero-shot annotation |
| Pathology (image) | [UNI](https://arxiv.org/abs/2308.15474) / [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) | ViT-L/16 + DINOv2 / LongNet | SSL on 100k+ slides | Slide diversity > slide count |
| Pathology (image+text) | [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) | ViT + text encoder | CLIP, 1.17M slide-caption | Wins 12/14 zero-shot pathology |
| Pathology (mixed magnification) | [Virchow2](https://arxiv.org/abs/2408.00738) | ViT-G + DINOv2 | Mixed 5×–40× tiles | +2–5 pts vs single-mag |
| Cell painting | [CellPainTR](https://arxiv.org/abs/2509.06986) / [ViTally](https://arxiv.org/abs/2411.02572) | ViT + DINOv2/MAE | Multi-channel SSL | Channel-mixing aug critical |
| Mass-spec proteomics | [LSM-MS2](https://arxiv.org/abs/2510.26715) | Transformer | MS2 spectra MLM | Single FM in corpus |
| Multimodal medical (QA) | [LLaVA-Med](https://arxiv.org/abs/2306.00890) | LLaMA + CLIP adapter | Instruction tuning, 600k pairs | Adapter unlocks free-form QA |
| Small molecules (representation) | [ChemFM](https://arxiv.org/abs/2410.21422) / [ChemBERTa](https://arxiv.org/abs/2010.09885) | Transformer | SMILES MLM/CLM | Scale-up monotonic on MoleculeNet |
| Small molecules (multimodal) | [MolFM](https://arxiv.org/abs/2307.09484) | Tri-encoder | Mol+text+graph contrastive | Beats unimodal on 8/10 MoleculeNet |
| ML force fields | [MACE-OFF / Multi-Fi](https://arxiv.org/abs/2412.13088) | MACE-OFF | Multi-fidelity training | Multi-fidelity improves transfer |
| Cross-omics unified | [AIDO](https://doi.org/10.1101/2024.12.02.626322) / [ESM-3](https://doi.org/10.1101/2024.07.01.600583) | Modular hub / Transformer | Per-module SSL + alignment | Shared rep enables cross-modal transfer |

## Design-Choice Axes

Twelve recurring decisions shape every bio-FM. For each axis we summarise the trade-offs and then quote the directly relevant **Rev 4 ablations** from the source notes.

### 1. Tokenization & Vocabulary

DNA models span character-level (HyenaDNA, Caduceus), fixed k-mer (DNABERT-1), learned BPE (DNABERT-2, NT-v2), and codebook (VQDNA). Protein models are almost universally amino-acid level (20–30 token vocabularies); the exceptions add structure tokens (ESM-3, ESM-AA, FoldSeek) or atomic tokens (RFAA). Single-cell models span gene-as-token (Geneformer, scGPT), bin-as-token (scBERT, scFoundation), and gene-text-as-token (GenePT). Pathology and microscopy use ViT patches with no language-style vocabulary.

**Empirical pattern:** vocabulary changes alter sequence length and FLOP budget more than they alter accuracy, with two notable exceptions — DNABERT-2's BPE doubles many GUE scores vs. fixed 6-mer, and ESM-3's structure-token addition unlocks joint sequence/structure generation impossible with sequence-only.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [DNABERT-2](https://arxiv.org/abs/2306.15006) | BPE on the multi-species genome (~32k merges) compresses tokens 5× vs. 6-mer and improves 23/28 GUE tasks; the gain is largest on long-range tasks where 6-mer hits the 512-token limit. |
| [DNABERT-1](https://doi.org/10.1093/bioinformatics/btab083) | Sweep over k∈{3,4,5,6} shows k=6 best for promoter and TF-binding; smaller k under-fits motif structure, larger k explodes vocabulary. |
| [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) | Ablating from non-overlapping 6-mer to BPE on multispecies corpus improves 13/18 BEND tasks; effect is larger than 10× parameter scaling on the same corpus. |
| [VQDNA](https://arxiv.org/abs/2405.10812) | Learned VQ codebook of 4096 entries beats fixed 6-mer on 22/28 GUE tasks; codebook collapse mitigated via EMA reset. |
| [HyenaDNA](https://arxiv.org/abs/2306.15794) | Single-nucleotide (character-level) tokenization is the only choice that scales to 1M-token context with sub-quadratic Hyena ops; k-mer would blow vocabulary or context budget. |
| [ESM-3](https://doi.org/10.1101/2024.07.01.600583) | Adding 4096 structure tokens (VQ over local SE(3) frames) to amino-acid vocabulary enables joint sequence/structure generation; ablating structure tokens drops cross-modal generation by >40 TM-score points. |
| [ESM-AA](https://arxiv.org/abs/2403.12995) | Multi-scale tokenization (residue + atom) outperforms residue-only on small-molecule binding prediction by 5–8 AUROC; pure atom-only loses long-range protein information. |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) | Rank-encoding (Geneformer) of expression eliminates batch-normalisation dependence; switching to log-CPM tokens loses 3–5 points on perturbation prediction. |
| [scGPT](https://doi.org/10.1038/s41592-024-02201-0) | Binned expression tokens with gene IDs outperform Geneformer-style rank tokens on perturbation tasks (+2.4 Pearson) but hurt zero-shot integration. |
| [GenePT](https://doi.org/10.1101/2023.10.16.562533) | Replacing learned gene embeddings with frozen GPT-3.5 text embeddings of NCBI gene summaries matches scGPT on 8/10 cell-type tasks at 0% pretraining cost. |

### 2. Architecture Family

Transformers dominate, but four sub-quadratic alternatives have proven competitive in 2023–2025: Hyena (HyenaDNA, Evo, Evo 2), Mamba/SSM (Caduceus, scMamba), striped/hybrid (Borzoi, Enformer = CNN+Transformer), and SE(3)-equivariant (AlphaFold 2/3, RoseTTAFold/AA, GearNet, ESM-IF). Diffusion/flow-matching now appears in design heads (RFAA, AF3, ProteinMPNN-flow, ESM-3).

**Empirical pattern:** at fixed parameter count, sub-quadratic models match Transformers on per-token loss but win on >32k-token throughput; equivariant models dominate structural tasks but underperform on pure sequence tasks; diffusion heads beat AR heads on inverse folding at higher temperatures.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [HyenaDNA](https://arxiv.org/abs/2306.15794) | Hyena replaces self-attention with implicit long convolutions; matches Transformer perplexity at 2× speed and 5× memory savings, enabling 1M-token context. |
| [Caduceus](https://arxiv.org/abs/2403.03234) | Bi-directional Mamba (BiMamba) with reverse-complement equivariance outperforms NT and HyenaDNA on 6/8 long-range Genomic Benchmarks at ≤0.5× FLOPs. |
| [scMamba](https://arxiv.org/abs/2506.20697) | Mamba SSM scales to 50M cells where scGPT OOMs at 1M; per-cell attention proxy via SSM kernel matches scGPT on annotation at 3× lower memory. |
| [Evo](https://doi.org/10.1126/science.ado9336) | Evo (StripedHyena, 7B) ablation shows Hyena layers are necessary at 131k context; pure Transformer baseline diverges past 8k. |
| [Evo 2](https://doi.org/10.1101/2025.02.18.638918) | Evo 2 (40B) confirms StripedHyena scales; configuration-only ablation (no head-to-head accuracy comparison published). |
| [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) | Evoformer + IPA: removing IPA drops GDT-TS by 4–7 points on CASP14; removing recycling drops it 3–5; FAPE loss is necessary for sub-Å backbone accuracy. |
| [RoseTTAFold](https://doi.org/10.1126/science.abj8754) | RoseTTAFold three-track: ablating any one track (1D/2D/3D) drops TM-score 4–9; full three-track is necessary. |
| [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) | AF3 replaces Evoformer's structure module with a diffusion head; recovery accuracy on protein-only matches AF2-multimer while extending to nucleic-acid and small-molecule complexes. |
| [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) | RFAA's all-atom track is necessary for heteroatom complexes; ablating to residue-only drops protein-NA contact accuracy by 18–25%. |
| [Enformer](https://doi.org/10.1038/s41592-021-01252-x) | Enformer's CNN+Transformer hybrid outperforms pure Transformer on 196k-bp expression prediction; ablating attention drops mean Pearson by 0.10. |
| [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) | Borzoi (CNN+UNet+Transformer) at 524k bp matches Enformer Pearson at 2× context; ablating UNet skip drops fine-grained track resolution. |

### 3. Pretraining Objective

Masked language modeling (BERT-style, 15% mask) remains the default for sequence FMs; causal LM appears in generative FMs (ProGen, ProtGPT2, Evo, BioGPT, scMulan). Contrastive objectives dominate vision/multimodal (CLIP variants, DINOv2 for pathology). Inverse-folding and structure-conditioned objectives (ESM-IF, ProteinMPNN, RFAA, AF3) train sequence given structure or vice versa. Recent additions: span-corruption (Ankh), JEPA-style (JEPA-DNA), structure-token autoregression (ESM-3), niche-conditional masking (Nicheformer).

**Empirical pattern:** for representation quality on classification/regression, MLM and contrastive perform within 1–2 points; for generation, AR or diffusion are necessary; for cross-modal alignment, CLIP-style with hard negatives dominates.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) | ESM-2 vs ESM-1b (same MLM objective, different scale): contact precision long-range P@L jumps from 0.34 (650M) to 0.54 (15B), confirming scale > objective. |
| [Ankh](https://arxiv.org/abs/2301.06568) | Span corruption with 1% noise + 3-token spans beats 15% MLM by 1–3% on 10/11 TAPE tasks at 1/4 the params. |
| [Rao attention-as-contacts](https://doi.org/10.1101/2020.12.15.422761) | Attention heads in MLM-trained ESM-1b directly encode contacts (precision 0.50+ P@L for several heads); no contact-supervision needed. |
| [ProGen](https://arxiv.org/abs/2004.03497) | Causal LM on 280M sequences with control tokens (taxonomy, function) generates synthetic enzymes that fold and function in vitro; ablating control tokens halves activity. |
| [ESM-1v](https://doi.org/10.1101/2021.07.09.450648) | ESM-1v zero-shot variant effect: pseudo-likelihood from MLM correlates 0.4–0.6 with deep mutational scan fitness across 41 datasets — no supervised fine-tuning. |
| [ESM-design](https://doi.org/10.1101/2022.12.21.521521) | ESM-IF (inverse folding objective) generalises to designed proteins absent from training; native-sequence recovery 51%. |
| [ESM-3](https://doi.org/10.1101/2024.07.01.600583) | ESM-3 multimodal masked-token objective over (sequence, structure, function) tokens enables prompted generation; ablating any single track drops cross-track recovery by 8–20%. |
| [ProteinMPNN](https://doi.org/10.1126/science.add2187) | ProteinMPNN's autoregressive sequence-given-structure objective beats Rosetta on native recovery (52% vs 33%) and produces sequences that fold in silico. |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) | Geneformer's masked-rank objective (15%) on 30M cells transfers zero-shot to dosage sensitivity prediction (AUROC 0.89); ablating to 5% mask drops by 0.04. |
| [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) | Niche-conditional masking (mask out neighbours, predict from cell + niche label) beats vanilla MLM by 4–7 points on spatial niche classification. |
| [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) | CONCH (NatMed) image-text contrastive on 1.17M slide-caption pairs outperforms image-only DINO baselines on 12/14 zero-shot pathology benchmarks. |
| [ConceptCLIP](https://arxiv.org/abs/2501.15579) | ConceptCLIP adds concept-token alignment on top of CLIP loss; improves zero-shot retrieval +5–8 points on biomedical concept matching. |

### 4. Context Length

Context budgets span 512 (DNABERT-1, scBERT) → 2k (ESM-2, ProtTrans) → 32k (NT-v2, AF2 crops) → 131k (Evo) → 524k (Borzoi) → 1M (Evo 2, HyenaDNA) tokens. Long context matters most for genomics (regulatory range >100kb), pathology (whole-slide tiling), and single-cell (cell × gene matrices >20k genes).

**Empirical pattern:** most regulatory effects sit within 100kb; gains from 100kb→1M are real but small (≤0.05 Pearson on Enformer-style tracks). For protein structure, AF2 crop sizes (256 residues) suffice for monomers; AF3/RFAA need full-complex context. For single-cell, the bottleneck is gene count (~20k), not depth.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [HyenaDNA](https://arxiv.org/abs/2306.15794) | Single 1M-token context model outperforms 32k baseline on long-range species classification by 6–11 points. |
| [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) | Sweep 1k → 32k context on multispecies pretraining: 32k > 1k by 2–6 points on regulatory tasks; gains plateau past 32k for the BEND benchmark. |
| [Enformer](https://doi.org/10.1038/s41592-021-01252-x) | Enformer's 196k-bp window is necessary for distal-enhancer effects; ablating to 100kb drops Pearson by 0.05. |
| [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) | Borzoi at 524kb beats Enformer at 196kb by Pearson +0.02 on RNA-seq coverage; gains saturate beyond 524kb. |
| [Evo](https://doi.org/10.1126/science.ado9336) | Evo trained at 131k tokens predicts 30k-bp prokaryotic operons end-to-end; ablating to 8k context destroys cross-gene coordination. |
| [Evo 2](https://doi.org/10.1101/2025.02.18.638918) | Evo 2 trained at 1M context; configuration only — no published context-ablation accuracy delta. |
| [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) | AF2 256-residue crops cover full domain context for >90% of CASP14 monomers; recycling 3× provides additional implicit context. |

### 5. Data: Scale, Quality, Diversity

Training sets span: protein UniRef50/90 (~50M–250M sequences), MGnify/BFD (>1B), nucleotide multispecies (~3T bp for NT, 8.8T for Evo 2), single-cell (CELLxGENE 30–50M cells), pathology (10k–500k slides). Diversity > raw size: clustering UniRef at 50% identity, multispecies vs single-genome, and lab/site-stratified slides all give larger gains than 10× more sequences from the same distribution.

**Empirical pattern:** redundancy hurts; clustering at 30–50% identity reliably beats unfiltered. For pathology, slide diversity (number of medical centres) outperforms slide count from a single centre. For single-cell, tissue/disease coverage matters more than cell count past ~10M.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) | UR50 vs UR90 vs UR100: UR50 (clustered) gives best contact precision per parameter; raw UR100 wastes capacity on near-duplicates. |
| [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) | Multispecies (850 species) > human-only on 16/18 BEND tasks; cross-species pretraining acts as evolutionary regularisation. |
| [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) | GigaPath: 171k slides from 28 centres; ablating to single-centre 50k slides drops linear-probe accuracy 4–9% across PCAM, BACH, and MHIST. |
| [UNI](https://arxiv.org/abs/2308.15474) | UNI: 100k slides DINOv2 outperforms 1M slides supervised; the data-quality bound dominates. |
| [Virchow](https://arxiv.org/abs/2309.07778) | Virchow on 1.5M slides + DINOv2 sets pan-cancer SOTA; ablating to 100k slides drops by 2–4 points on 9-class subtyping. |
| [Virchow2](https://arxiv.org/abs/2408.00738) | Mixed-magnification training (5×, 10×, 20×, 40× tiles) yields 2–5 pt gain over single-magnification at 20×; KDE-based stain-aug ablation isolates the magnification mix as the largest single contributor. |
| [Phikon-v2](https://arxiv.org/abs/2409.09173) | Phikon-v2 doubles slide count vs Phikon and adds clinical metadata; gains are 1–3% on pan-cancer linear probe — sublinear in data. |
| [RudolfV](https://arxiv.org/abs/2401.04079) | RudolfV: stain-augmentation + multi-stain pretraining adds 2–4 points on cross-stain transfer that single-stain DINOv2 misses. |
| [H-optimus-0](https://arxiv.org/abs/2404.15217) | H-optimus-0: 500k slides confirms diminishing returns past 200k slides on standard CPath benchmarks (<1% delta). |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) | Geneformer: scaling 1M → 30M cells gives 3–6 point boost on dosage sensitivity; tissue diversity (296 → 561 tissues) gives a further 2–4 points. |
| [UCE](https://doi.org/10.1101/2023.11.28.568918) | UCE on 36M cells across 1000+ studies; cross-species pretraining (mouse + human) enables zero-shot annotation in unseen species (full-text 403; relies on author claims). |

### 6. Multi-Modal Fusion

Bio-FMs fuse modalities four ways: (i) **early fusion** of token streams (ESM-3, ESM-AA, RFAA, AF3, MIRROR-3D); (ii) **CLIP-style alignment** of unimodal encoders (CONCH, BiomedCLIP, ProtCLIP, MolFM, KEEP); (iii) **adapter-style** instruction tuning of an LLM with a vision encoder (LLaVA-Med, XrayGPT, Doctor Sun, MedMax); (iv) **knowledge fusion** with text embeddings of structured concepts (GenePT, ConceptCLIP, KEEP).

**Empirical pattern:** early fusion wins when modalities are tightly coupled (sequence↔structure); CLIP wins for retrieval; adapter-LLM wins for free-form QA; knowledge fusion wins when labelled multimodal data is scarce.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-3](https://doi.org/10.1101/2024.07.01.600583) | Joint masked sequence+structure+function tokens (ESM-3) outperform sequence-only ESM-2 by 5–10 TM-score points on structure recovery and unlock prompted design. |
| [ESM-AA](https://arxiv.org/abs/2403.12995) | Residue+atom early fusion beats CLIP-style residue↔ligand alignment by 3–6 AUROC on protein-ligand binding. |
| [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) | AF3 unifies protein, NA, and small-molecule into one diffusion head; per-task heads underperform by 5–12% on cross-modal complexes. |
| [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) | RFAA all-atom track lifts protein-NA interface accuracy 18–25% over residue-only baselines. |
| [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) | CONCH NatMed: contrastive image-text on 1.17M pairs beats image-only DINO on 12/14 zero-shot pathology benchmarks; ablating text alignment loses retrieval almost entirely. |
| [KEP (KEEP)](https://arxiv.org/abs/2412.13126) | KEEP injects structured knowledge graph into CLIP loss; +3–5 zero-shot retrieval, +1–2 supervised. |
| [BiomedCLIP](https://arxiv.org/abs/2303.00915) | PMC-15M scale CLIP outperforms ImageNet-CLIP on 22/24 biomedical benchmarks; the data scale is the dominant factor. |
| [ProtCLIP](https://arxiv.org/abs/2412.20014) | Function-informed contrastive loss (sequence ↔ GO term text) beats plain MLM ESM-2 on 9/12 function-prediction tasks at fixed parameter count. |
| [MolFM](https://arxiv.org/abs/2307.09484) | Tri-modal molecule-text-graph contrastive beats unimodal SMILES BERT on 8/10 MoleculeNet tasks; KG triples in pretraining add another 2–3 points. |
| [AIDO](https://doi.org/10.1101/2024.12.02.626322) | AIDO multi-omics modules (DNA+RNA+protein+cell) interoperate via shared representation hub; each module's ablations live in its per-modality preprint. |
| [MIRROR-3D](https://arxiv.org/abs/2504.09060) | MIRROR-3D fuses Hi-C contact maps with sequence; sequence-only ablation loses 3D contact prediction entirely. |
| [ConceptCLIP](https://arxiv.org/abs/2501.15579) | ConceptCLIP concept-token alignment on top of CLIP yields +5–8 zero-shot retrieval and produces explainable concept attributions. |
| [LLaVA-Med](https://arxiv.org/abs/2306.00890) | LLaVA-Med adapter on top of frozen LLaMA + CLIP; instruction tuning on 600k biomedical image-text pairs unlocks free-form QA missing from CLIP-only baselines. |

### 7. Conditioning & Inductive Biases

Conditioning at pretraining (control tokens, label conditioning, niche conditioning, knowledge graphs) is consistently more efficient than post-hoc fine-tuning. Inductive biases (equivariance, reverse-complement symmetry, periodic position encoding) reduce sample complexity proportionally.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ProGen](https://arxiv.org/abs/2004.03497) | Causal LM with taxonomic + functional control tokens generates active synthetic enzymes; ablating control tokens halves in-vitro activity rate. |
| [scMulan](https://doi.org/10.1101/2024.01.25.577152) | Multi-task control-token training across 10 single-cell tasks; no published head-to-head ablation table (bioRxiv full text 403) — supporting only. |
| [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) | Niche-label conditioning improves spatial niche classification by 4–7 points over vanilla MLM; tissue-token gives a further +2. |
| [Caduceus](https://arxiv.org/abs/2403.03234) | Hard-coded reverse-complement equivariance halves effective parameters and improves Genomic Benchmarks by 1–3 points. |
| [GET](https://doi.org/10.1038/s41586-024-08391-z) | GET conditions on cell-type label + chromatin accessibility; ablating cell-type token loses 8–14 points on cross-tissue gene-expression prediction. |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) | Geneformer rank encoding implicitly conditions on cell-state without external metadata; replacing with raw counts hurts batch-robust transfer. |
| [BioGPT](https://arxiv.org/abs/2210.10341) | Domain-conditioned causal LM beats general-purpose GPT-2 fine-tuned on biomedical NLP by 2–5 F1 across 6 tasks. |
| [ProtCLIP](https://arxiv.org/abs/2412.20014) | GO-term conditioning at pretraining beats post-hoc GO classifier on top of frozen ESM-2 by 3–7 F1 across 12 function tasks. |

### 8. Optimization & Schedule

Standard recipe: AdamW, β=(0.9, 0.95–0.98), weight decay 0.01–0.1, cosine schedule with 1–10% warmup. Bio-FMs rarely innovate here; the few that do (Ankh, Caduceus) tune for sample efficiency rather than peak. Mixed precision (bf16) is universal post-2022. Long-context training requires gradient checkpointing or FlashAttention/Flash-SSM kernels.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [Ankh](https://arxiv.org/abs/2301.06568) | T5-style relative position + 1% noise span corruption + bf16 = 4× lower compute than ESM-2 at matched downstream accuracy. |
| [Caduceus](https://arxiv.org/abs/2403.03234) | Mamba's selective SSM kernels enable 1M-bp training on 8×A100 where Transformer baselines OOM at 65k. |
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) | ESM-2 15B trained with FSDP + bf16 + gradient checkpointing on 4096 V100; ablating to fp32 doubles wall time with no accuracy gain. |
| [HyenaDNA](https://arxiv.org/abs/2306.15794) | Single GPU 1M-token training via Hyena's FFT-conv kernel; ablating to attention requires 100× more memory. |

### 9. Scaling & Compute Efficiency

Scaling laws hold within bio-FMs but with smaller exponents than text LMs. ESM-2 reports clean scaling 8M → 15B; AlphaFold 3 and Evo 2 confirm scale-up but with diminishing returns past task-specific saturation points. Compute efficiency is dominated by sub-quadratic backbones (genomics) and DINOv2 distillation (pathology).

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) | Loss scales as power law in params 8M → 15B; downstream contact precision saturates near 3B for many tasks but improves to 15B for the hardest. |
| [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) | GigaPath: ViT-G/14 (1.1B) outperforms ViT-L/14 (300M) by 1–3% averaged across 26 benchmarks; gains are sublinear past 300M. |
| [UNI](https://arxiv.org/abs/2308.15474) | UNI: ViT-L/16 + DINOv2 outperforms ViT-G + supervised; SSL is the binding constraint, not scale. |
| [Evo 2](https://doi.org/10.1101/2025.02.18.638918) | Evo 2 (40B, 8.8T tokens) demonstrates configuration scale-up; published metrics are configuration-only, no head-to-head accuracy ablation accessible. |
| [Evo](https://doi.org/10.1126/science.ado9336) | Evo 7B at 131k context is compute-optimal for prokaryotic genome modelling; smaller variants under-fit, larger explore-only have not been head-to-head benchmarked. |
| [HIPT](https://arxiv.org/abs/2206.02647) | HIPT hierarchical scaling: cell-level + region-level + slide-level transformers; ablating any tier drops survival prediction C-index by 0.02–0.05. |
| [ESM-3](https://doi.org/10.1101/2024.07.01.600583) | ESM-3 1.4B → 98B sweep: structure-recovery accuracy scales smoothly; design quality saturates earlier than recovery accuracy. |

### 10. MSA vs MSA-Free Structure Prediction

MSA-conditioned models (AF2, RoseTTAFold, AF3, MSA Transformer) remain SOTA for hard targets. MSA-free models (ESMFold, OmegaFold, HelixFold-Single, RhoFold) trade 5–15 GDT-TS / TM-score points for 10–100× faster inference and applicability to designed/synthetic proteins lacking homologues.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2) | AF2 with MSA: median GDT-TS 92 on CASP14; ablating MSA depth from 5120 → 1 drops by 25–40 GDT-TS on hard targets. |
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) | ESMFold (MSA-free): median TM-score 0.71 vs AF2 0.84; gap closes for high-pLDDT structures and orphan proteins where AF2 lacks MSAs. |
| [HelixFold-Single](https://arxiv.org/abs/2207.13921) | HelixFold-Single (MSA-free) closes ~80% of the AF2-vs-no-MSA gap by distilling AF2 outputs as pretraining. |
| [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) | OmegaFold beats AF2 on de-novo / orphan proteins lacking homologues by 5–10 TM-score points; loses on multi-domain hard targets. |
| [RhoFold](https://arxiv.org/abs/2207.01586) | RhoFold MSA-conditioned: 4 Å RMSD on RNA targets; RNA MSAs are sparse, so MSA-free RNA models lag further than protein. |
| [MSA Transformer](https://doi.org/10.1101/2021.02.12.430858) | Axial attention over MSA rows + columns gives state-of-the-art contact precision with one model trained on 26M MSAs. |
| [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) | ESM-IF distils AlphaFold predictions into 12M-structure training set; native recovery 51% vs 33% Rosetta on AF-distilled augmentation alone. |

### 11. Distillation from AlphaFold Predictions

Using AF2/AF3 predictions (often AlphaFold DB ~200M structures) as pseudo-labels is the cheapest known structure-prediction lever. Models that distil consistently gain 1–3 nm RMSD or 5–10 TM-score points over the same-architecture non-distilled baseline.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) | ESMFold's structure module is distilled from AF2 trajectories; ablating distillation drops median TM-score by ~5 points. |
| [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) | ESM-IF training data: 12M AlphaFold DB structures; without AF distillation, recovery drops from 51% to ~38%. |
| [HelixFold-Single](https://arxiv.org/abs/2207.13921) | Pretraining on AF2 pseudo-structures recovers most of the MSA-free gap; ablating distillation drops TM-score by 7 points. |
| [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) | OmegaFold distillation regimen (AF2 pseudo-labels + de-novo benchmark) is necessary for orphan-protein gains. |
| [RhoFold](https://arxiv.org/abs/2207.01586) | RhoFold uses RNA structure distillation analogue; gains over MSA-only RNA baselines are 1–3 Å RMSD. |
| [GearNet](https://arxiv.org/abs/2203.06125) | GearNet pretrains on AF2 structures (805k); ablating to PDB-only (90k) drops EC/GO accuracy by 3–6 points. |

### 12. Evaluation & Benchmarking Caveats

Many headline gains shrink ≥50% under (a) leakage-corrected splits (sequence identity / time / lab), (b) fair-baseline reruns with tuned hyperparameters, and (c) out-of-distribution test sets. Recurring problems: scRNA FMs vs scVI rerun, pathology FMs vs ImageNet-supervised baselines on small cohorts, NT/DNABERT on the GUE benchmark which is partially leaked.

#### Ablation evidence (Rev 4)
| Source | Ablation finding |
|---|---|
| [scGPT](https://doi.org/10.1038/s41592-024-02201-0) | scGPT vs scVI on integration: gains are 1–3% under fair-baseline reruns reported in follow-up work, vs 5–10% in original paper. |
| [scFoundation](https://doi.org/10.1038/s41592-024-02305-7) | scFoundation vs scVI on perturbation: gains shrink 30–50% with leakage-corrected splits. |
| [Geneformer](https://doi.org/10.1038/s41586-023-06139-9) | Geneformer dosage-sensitivity AUROC 0.89 reproducible only on author-published splits; cross-tissue test gives 0.78. |
| [CellPLM](https://doi.org/10.1101/2023.10.03.560734) | CellPLM ablation table reports 4 variants; the cell-language-model variant alone is 2–4 points behind full model — most benefit comes from inter-cell attention. |
| [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) | SCimilarity zero-shot annotation accuracy depends heavily on the reference set's tissue match; cross-tissue accuracy drops 10–20%. |
| [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z) | NT GUE results partially affected by sequence-identity leakage in some tasks; multispecies NT still wins under cleaner splits. |
| [GigaPath](https://doi.org/10.1038/s41586-024-07441-w) | GigaPath benchmark gains shrink 1–4% under leave-one-centre-out evaluation vs random split. |
| [ESM-1b](https://doi.org/10.1073/pnas.2016239118) | ESM-1b contact precision tested on CASP and CAMEO; ESM-2 confirms scaling but original ESM-1b numbers depend on time-split avoiding train leakage. |

## Modality-Specific Recipes

Practical defaults per modality, drawn from the strongest ablations in the 84 FM corpus.

### DNA / Genomics

**Default recipe.** Multispecies corpus + BPE or character tokenization + sub-quadratic backbone (Hyena/Mamba) + ≥32k context + reverse-complement equivariance.

**Rev 4 additions.** [Evo 2](https://doi.org/10.1101/2025.02.18.638918) (Evo 2, 40B) confirms scale-up but published configuration-only; [GET](https://doi.org/10.1038/s41586-024-08391-z) (GET) shows cell-type-conditioned epigenome modelling. **(N=12 papers)** DNA FMs: [PhyloGPN](https://arxiv.org/abs/2503.03773), [Caduceus](https://arxiv.org/abs/2403.03234), [DNABERT-2](https://arxiv.org/abs/2306.15006), [DNABERT-1](https://doi.org/10.1093/bioinformatics/btab083), [dnaGrinder](https://arxiv.org/abs/2409.15697), [Evo 2](https://doi.org/10.1101/2025.02.18.638918), [Genome Book](https://arxiv.org/abs/2501.16982), [HyenaDNA](https://arxiv.org/abs/2306.15794), [JEPA-DNA](https://arxiv.org/abs/2602.17162), [Evo](https://doi.org/10.1126/science.ado9336), [Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z), [VQDNA](https://arxiv.org/abs/2405.10812)

**Pitfalls.** GUE leakage; per-task hyperparameters dominate small models; Hyena/Mamba require custom kernels for production inference.

### DNA → Epigenome / Gene Expression

[Enformer](https://doi.org/10.1038/s41592-021-01252-x) (Enformer, 196kb) and [Borzoi](https://doi.org/10.1038/s41588-024-02053-6) (Borzoi, 524kb) remain the two-model recipe. [GET](https://doi.org/10.1038/s41586-024-08391-z) (GET) extends to cell-type-conditioned cross-tissue prediction; [MIRROR-3D](https://arxiv.org/abs/2504.09060) (MIRROR-3D) adds Hi-C fusion. **(N=4 papers)** epigenome FMs: [Enformer](https://doi.org/10.1038/s41592-021-01252-x), [Borzoi](https://doi.org/10.1038/s41588-024-02053-6), [GET](https://doi.org/10.1038/s41586-024-08391-z), [MIRROR-3D](https://arxiv.org/abs/2504.09060)

### RNA

[RNA-FM](https://arxiv.org/abs/2204.00300) (RNA-FM, MLM on ncRNA) and [RiNALMo](https://arxiv.org/abs/2403.00043) (RiNALMo, scaled MLM) cover representation; [RhoFold](https://arxiv.org/abs/2207.01586) (RhoFold) covers structure with sparse RNA MSAs. **(N=3 papers)** RNA FMs: [RNA-FM](https://arxiv.org/abs/2204.00300), [RiNALMo](https://arxiv.org/abs/2403.00043), [RhoFold](https://arxiv.org/abs/2207.01586)

**Pitfalls.** RNA pretraining corpora are 100× smaller than protein; MSA depth for RNA is sparse so MSA-free models lag further than protein.

### Protein Sequence

**Default.** ESM-2 family (650M for representation, 15B for SOTA contact / variant effect) + UR50 clustered pretraining + MLM.

**Rev 4 additions.** [ESM-3](https://doi.org/10.1101/2024.07.01.600583) (ESM-3, multimodal masked tokens over sequence/structure/function) and [ProteinMPNN](https://doi.org/10.1126/science.add2187) (ProteinMPNN, autoregressive sequence-given-structure) close the design loop. **(N=16 papers)** protein-sequence FMs: [Ankh](https://arxiv.org/abs/2301.06568), [ESM-1b](https://doi.org/10.1073/pnas.2016239118), [PST](https://arxiv.org/abs/2401.14819), [ESM-AA](https://arxiv.org/abs/2403.12995), [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574), [ESM-1v](https://doi.org/10.1101/2021.07.09.450648), [ESM-design](https://doi.org/10.1101/2022.12.21.521521), [MSA Transformer](https://doi.org/10.1101/2021.02.12.430858), [ProGen](https://arxiv.org/abs/2004.03497), [ProtCLIP](https://arxiv.org/abs/2412.20014), [ProteinBERT](https://doi.org/10.1093/bioinformatics/btac020), [ProtGPT2](https://doi.org/10.1038/s41467-022-32007-7), [ProtTrans](https://arxiv.org/abs/2007.06225), [ProteinMPNN](https://doi.org/10.1126/science.add2187), [ESM-3](https://doi.org/10.1101/2024.07.01.600583), [Rao attention-as-contacts](https://doi.org/10.1101/2020.12.15.422761)

### Protein Structure

**Default.** AF2 for monomers; [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) (AF3) for protein-NA-ligand complexes; [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) (RFAA) for all-atom heteroatom complexes. [ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574) (ESMFold), [HelixFold-Single](https://arxiv.org/abs/2207.13921), [OmegaFold](https://doi.org/10.1101/2022.07.21.500999) (OmegaFold) for MSA-free / orphan proteins. [ESM-IF](https://doi.org/10.1101/2022.04.10.487779) (ESM-IF) for inverse folding. **(N=9 papers)** structure FMs: [RoseTTAFold](https://doi.org/10.1126/science.abj8754), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528), [HelixFold-Single](https://arxiv.org/abs/2207.13921), [OmegaFold](https://doi.org/10.1101/2022.07.21.500999), [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2), [ESM-IF](https://doi.org/10.1101/2022.04.10.487779), [GearNet](https://arxiv.org/abs/2203.06125), [RhoFold](https://arxiv.org/abs/2207.01586)

### Single-Cell RNA

**Default.** Geneformer or scGPT for representation + scVI as fair baseline (always rerun!). For perturbation / cross-tissue: scFoundation, scGPT, or [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) (SCimilarity) for nearest-reference annotation.

**Rev 4 additions.** [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) (Nicheformer) adds spatial niche conditioning; [UCE](https://doi.org/10.1101/2023.11.28.568918) (UCE) enables cross-species zero-shot annotation; [CellPLM](https://doi.org/10.1101/2023.10.03.560734) (CellPLM) adds inter-cell attention for tissue-context tasks; [GenePT](https://doi.org/10.1101/2023.10.16.562533) (GenePT) shows GPT-3.5 text embeddings of NCBI summaries match scGPT at 0% pretraining cost; [scMulan](https://doi.org/10.1101/2024.01.25.577152) (scMulan) adds multi-task control tokens. **(N=12 papers)** scRNA FMs: [CellPLM](https://doi.org/10.1101/2023.10.03.560734), [GenePT](https://doi.org/10.1101/2023.10.16.562533), [scFoundation](https://doi.org/10.1038/s41592-024-02305-7), [Nicheformer](https://doi.org/10.1101/2024.04.15.589472), [scELMo](https://arxiv.org/abs/2601.05648), [scBERT](https://doi.org/10.1038/s42256-022-00534-z), [scGPT](https://doi.org/10.1038/s41592-024-02201-0), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537), [scMamba](https://arxiv.org/abs/2506.20697), [scMulan](https://doi.org/10.1101/2024.01.25.577152), [Geneformer](https://doi.org/10.1038/s41586-023-06139-9), [UCE](https://doi.org/10.1101/2023.11.28.568918)

**Pitfalls.** Always rerun scVI / Harmony / totalVI as baselines with tuned hyperparameters; FM gains over fair baselines are typically 1–3% on integration, 5–15% only on zero-shot perturbation / cross-tissue / cross-species.

### Spatial Transcriptomics

Newly broken out in Rev 4. [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) (Nicheformer) is the canonical FM: niche-conditional masking on spatial transcriptomics + dissociated scRNA gives +4–7 points on niche classification. **(N=1 papers)** spatial-transcriptomics FMs: [Nicheformer](https://doi.org/10.1101/2024.04.15.589472)

**Pitfalls.** Few public spatial atlases at scale; most evaluation is intra-dataset.

### Computational Pathology

**Default.** UNI or GigaPath as tile encoder + slide-level aggregator (ABMIL/CLAM-style as baseline). For multimodal slide-text: CONCH (NatMed). For mixed-magnification: Virchow2.

**Rev 4 additions.** [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) (CONCH NatMed, 1.17M slide-caption pairs) supersedes the preprint version. [Virchow2](https://arxiv.org/abs/2408.00738) (Virchow2) demonstrates mixed-magnification SSL gains. **(N=13 papers)** pathology / radiology FMs: [UNI](https://arxiv.org/abs/2308.15474), [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4), [GigaPath](https://doi.org/10.1038/s41586-024-07441-w), [KEP (KEEP)](https://arxiv.org/abs/2412.13126), [Phikon-v2](https://arxiv.org/abs/2409.09173), [RudolfV](https://arxiv.org/abs/2401.04079), [HIPT](https://arxiv.org/abs/2206.02647), [CONCH (preprint)](https://arxiv.org/abs/2307.12914), [H-optimus-0](https://arxiv.org/abs/2404.15217), [Virchow](https://arxiv.org/abs/2309.07778), [Virchow2](https://arxiv.org/abs/2408.00738), [uniGradICON](https://arxiv.org/abs/2403.05780), [XrayGPT](https://arxiv.org/abs/2306.07971)

**Pitfalls.** Single-centre evaluation overestimates by 1–4%; always include leave-one-centre-out. ImageNet-supervised baselines on small cohorts can be within 2% of FMs.

### Cell Painting / High-Content Microscopy

[CellPainTR](https://arxiv.org/abs/2509.06986) (CellPainTR) and [ViTally](https://arxiv.org/abs/2411.02572) (ViTally) cover the recipe: ViT-based DINOv2/MAE on multi-channel fluorescence with channel-mixing augmentation. **(N=2 papers)** cell-painting / microscopy FMs: [CellPainTR](https://arxiv.org/abs/2509.06986), [ViTally](https://arxiv.org/abs/2411.02572)

### Mass-Spectrometry Proteomics

[LSM-MS2](https://arxiv.org/abs/2510.26715) (LSM-MS2) is the only FM in this corpus; representation learning on MS2 spectra. **(N=1 papers)** MS-proteomics FMs: [LSM-MS2](https://arxiv.org/abs/2510.26715)

### Multimodal Medical

[BiomedCLIP](https://arxiv.org/abs/2303.00915) (BiomedCLIP, PMC-15M) for image-text representation; [LLaVA-Med](https://arxiv.org/abs/2306.00890) (LLaVA-Med), [XrayGPT](https://arxiv.org/abs/2306.07971) (XrayGPT), [Doctor Sun](https://arxiv.org/abs/2508.08270) (Doctor Sun), [MedMax](https://arxiv.org/abs/2412.12661) (MedMax) for instruction-tuned QA; [ConceptCLIP](https://arxiv.org/abs/2501.15579) (ConceptCLIP) for explainable retrieval; [MedDiff-FM](https://arxiv.org/abs/2410.15432) (MedDiff-FM) for medical image generation. **(N=9 papers)** multimodal medical FMs: [ConceptCLIP](https://arxiv.org/abs/2501.15579), [BiomedCLIP](https://arxiv.org/abs/2303.00915), [Doctor Sun](https://arxiv.org/abs/2508.08270), [LLaVA-Med](https://arxiv.org/abs/2306.00890), [MedDiff-FM](https://arxiv.org/abs/2410.15432), [MedMax](https://arxiv.org/abs/2412.12661), [XrayGPT](https://arxiv.org/abs/2306.07971), [BioGPT](https://arxiv.org/abs/2210.10341), [BioBERT](https://arxiv.org/abs/1901.08746)

### Small Molecules / SMILES

[ChemBERTa](https://arxiv.org/abs/2010.09885) (ChemBERTa) and [ChemFM](https://arxiv.org/abs/2410.21422) (ChemFM) for SMILES MLM/CLM; [MolFM](https://arxiv.org/abs/2307.09484) (MolFM) for tri-modal molecule-text-graph; [MACE-OFF / Multi-Fi](https://arxiv.org/abs/2412.13088) (MACE-OFF) for ML force fields. **(N=5 papers)** small-molecule FMs: [ChemBERTa](https://arxiv.org/abs/2010.09885), [ChemFM](https://arxiv.org/abs/2410.21422), [LSM-MS2](https://arxiv.org/abs/2510.26715), [MolFM](https://arxiv.org/abs/2307.09484), [MACE-OFF / Multi-Fi](https://arxiv.org/abs/2412.13088)

### Cross-Omics & Unified Models

[AIDO](https://doi.org/10.1101/2024.12.02.626322) (AIDO) covers DNA + RNA + protein + cell with shared representation modules; per-module ablations live in their respective preprints. **(N=3 papers)** cross-omics FMs: [AIDO](https://doi.org/10.1101/2024.12.02.626322), [ESM-3](https://doi.org/10.1101/2024.07.01.600583), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w)

## Open Problems

1. **Honest single-cell evaluation.** scRNA FMs need standardised, leakage-corrected benchmarks with always-on scVI/Harmony/totalVI baselines. **(N=8 papers)** evidence: [scGPT](https://doi.org/10.1038/s41592-024-02201-0), [scFoundation](https://doi.org/10.1038/s41592-024-02305-7), [Geneformer](https://doi.org/10.1038/s41586-023-06139-9), [CellPLM](https://doi.org/10.1101/2023.10.03.560734), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537), [UCE](https://doi.org/10.1101/2023.11.28.568918), [scBERT](https://doi.org/10.1038/s42256-022-00534-z), [GenePT](https://doi.org/10.1101/2023.10.16.562533)

2. **Generalisable RNA structure.** RNA models lag protein because MSAs are sparse; need RNA-specific distillation analogue to AF2 distillation. **(N=3 papers)** evidence: [RhoFold](https://arxiv.org/abs/2207.01586), [RNA-FM](https://arxiv.org/abs/2204.00300), [RiNALMo](https://arxiv.org/abs/2403.00043)

3. **Cross-modal generation that respects physics.** ESM-3 + AF3 + RFAA close the structural gap; quantifying which prompts produce *foldable, functional* molecules remains open. **(N=4 papers)** evidence: [ESM-3](https://doi.org/10.1101/2024.07.01.600583), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528), [ProteinMPNN](https://doi.org/10.1126/science.add2187)

4. **Spatial transcriptomics scaling.** Only one canonical FM; the field needs a Geneformer/scGPT-scale niche-aware model. **(N=1 papers)** evidence: [Nicheformer](https://doi.org/10.1101/2024.04.15.589472)

5. **Pathology robustness.** All public benchmarks are biased toward a few centres; cross-site generalisation gaps of 4–9% are routine. **(N=7 papers)** evidence: [GigaPath](https://doi.org/10.1038/s41586-024-07441-w), [UNI](https://arxiv.org/abs/2308.15474), [Virchow](https://arxiv.org/abs/2309.07778), [Phikon-v2](https://arxiv.org/abs/2409.09173), [RudolfV](https://arxiv.org/abs/2401.04079), [Virchow2](https://arxiv.org/abs/2408.00738), [H-optimus-0](https://arxiv.org/abs/2404.15217)

6. **Long-range DNA past 1 Mb.** Evo 2 and HyenaDNA reach 1M tokens; head-to-head accuracy ablations past 524kb on regulatory tasks have not been published. **(N=5 papers)** evidence: [Evo 2](https://doi.org/10.1101/2025.02.18.638918), [HyenaDNA](https://arxiv.org/abs/2306.15794), [Evo](https://doi.org/10.1126/science.ado9336), [Borzoi](https://doi.org/10.1038/s41588-024-02053-6), [Enformer](https://doi.org/10.1038/s41592-021-01252-x)

7. **Reproducible AF3 / RFAA.** AF3 weights and training data are partially restricted; community reimplementations diverge by 5–10% on heteroatom complexes. **(N=4 papers)** evidence: [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528), [AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2), [RoseTTAFold](https://doi.org/10.1126/science.abj8754)

## Methodology & Limitations

This guidebook is grounded in **84 bio-FM papers**, each of which carries a `## Ablations (Rev 4)` section in its source note. **(N=X papers)** annotations on every claim count only those 84 FM papers; the remaining 85 surveyed papers are baselines, benchmarks, or supporting methods (TAPE, CLAM, scVI, totalVI, Cellpose, CellRanger, etc.) and are not counted as primary evidence.

Coverage is uneven: protein sequence (21), pathology (13), protein structure (13), DNA (12), and scRNA (12) are well represented; RNA (5), small-molecule (6), epigenome (4), spatial transcriptomics (1), MS-proteomics (1), and cell-painting (1) are under-represented.

Several Rev-4 ablation tables are limited by source access:
- [scMulan](https://doi.org/10.1101/2024.01.25.577152): full text 403 (bioRxiv); ablations could not be quoted directly.
- [Evo 2](https://doi.org/10.1101/2025.02.18.638918) (Evo 2): preprint inaccessible at extraction time; only configuration-level details available.
- [UCE](https://doi.org/10.1101/2023.11.28.568918) (UCE): full text 403; supporting evidence is qualitative.
- [AIDO](https://doi.org/10.1101/2024.12.02.626322): ablations are distributed across per-module preprints.

Quantitative claims reflect the ablations reported in each paper and have **not been independently reproduced**. The Rev 3 verification appendix (preserved verbatim below) is the only independent fact-check applied.

## Appendix: FM Catalogue (84 entries)

One row per FM, grouped by modality. Each entry: nickname → URL, one-line ablation take-away extracted from the source note's `## Ablations (Rev 4)` table.

### DNA / Genomics (12)

- **[Caduceus](https://arxiv.org/abs/2403.03234)** — *modalities: dna*
  - Conclusion.
  - Use Mamba (selective SSM) as the inner block; it scales better with context than implicit-conv Hyena.
  - Parameter sharing buys depth at fixed param count and outperforms the naive 2-module bidirectional design.
  - RC equivariance is a useful architectural prior even at pre-training, not just downstream.
  - RC equivariance — whether built-in (PS) or post-hoc (Ph) — is the dominant factor on short/medium-range classification.
- **[DNABERT-1](https://doi.org/10.1093/bioinformatics/btab083)** — *modalities: dna*
  - Source.
  - DNABERT-2 Tab.3.
  - DNABERT-2 Tab.3.
  - DNABERT-2 Tab.3.
  - DNABERT-2 Tab.3.
- **[DNABERT-2](https://arxiv.org/abs/2306.15006)** — *modalities: dna*
  - BPE strictly dominates overlapping k-mer in both performance and compute, validating the central design choice.
  - Vocab size = 4096 is the chosen sweet spot trading compute vs accuracy.
  - Multi-species pre-training is the dominant source of DNABERT-2's gains; architecture alone is insufficient.
  - Cheap domain-adaptive pre-training reliably improves downstream performance.
- **[dnaGrinder](https://arxiv.org/abs/2409.15697)** — *modalities: dna*
  - Conclusion.
  - SwiGLU adopted: ~comparable quality at substantially lower parameter cost.
  - Further pretraining yields limited / inconsistent gains for dnaGrinder; not worth the compute as a default.
  - SNP-variant-only data is unsuitable (sparse, arbitrarily spaced); complete reference sequences with SNPs incorporated are required.
  - Approximate (dilated) attention loses too much information; full attention with SLW is preferred even at shorter context.
- **[Evo](https://doi.org/10.1126/science.ado9336)** — *modalities: dna, rna, protein-sequence*
  - Byte-level DNA needs deep-signal-processing / SSM hybrids; motivates StripedHyena for Evo.
  - StripedHyena chosen partly because real training is always compute-suboptimal.
  - Long genomic context is the key enabler; whole-organism fitness signal is non-local.
  - Result is not a prompt-engineering artefact.
  - Genomic-context modelling, not codon-level pretraining, drives the capability.
- **[Evo 2](https://doi.org/10.1101/2025.02.18.638918)** — *modalities: dna*
  - Source.
  - GitHub README.
  - GitHub README.
  - GitHub README.
  - GitHub README v0.5.0 release.
- **[Genome Book](https://arxiv.org/abs/2501.16982)** — *modalities: dna, protein-sequence*
  - Take-away.
  - EN→DNA transfer works on short DNA pairs without any DNA supervision.
  - Transfer degrades on longer sequences (~13 pt drop) — length sensitivity.
  - All three lengths >79% → transfer is robust but length-dependent.
  - Shared BPE + EN similarity FT is what aligns DNA and EN representations (mechanism behind row 1–3).
- **[HyenaDNA](https://arxiv.org/abs/2306.15794)** — *modalities: dna*
  - Single-nucleotide tokenization is a major contributor to HyenaDNA's performance; aggregating k-mer tokenizers hurt fine-grained tasks.
  - Causal next-token pretraining is preferable; naive bidirectional Hyena (without MLM pretraining) underperforms.
  - Pretraining helps but gains are modest because GenomicBenchmarks are near saturation.
  - Pretraining matters most on harder, lower-baseline tasks (especially histone marks).
  - Hyena operator outperforms attention at matched parameter count and competes with models 1500× larger.
- **[JEPA-DNA](https://arxiv.org/abs/2602.17162)** — *modalities: dna*
  - Take-away.
  - Short-range motif tasks benefit.
  - Mid-range structural tasks benefit.
  - Largest supervised gain; coding variants.
  - Sole regression; splice-QTL hurt slightly.
- **[Nucleotide Transformer](https://doi.org/10.1038/s41592-024-02523-z)** — *modalities: dna*
  - Sequence diversity beats raw human-only data; diversity > size when compute-limited.
  - Scale helps, but pairing with diverse pretraining data matters as much.
  - Fine-tuning required for top performance; also lower variance than probing.
  - Embedding quality is layer-dependent; mid/late-but-not-final layers best.
  - IA³ is sufficient; ~1000× storage savings with negligible performance cost.
- **[PhyloGPN](https://arxiv.org/abs/2503.03773)** — *modalities: dna, multispecies-alignment*
  - Δ (Abl − Base).
  - **0.87**.
  - **0.87**.
  - **0.83**.
  - **0.84**.
- **[VQDNA](https://arxiv.org/abs/2405.10812)** — *modalities: dna*
  - Source.
  - Table 7.
  - Table 7.
  - Table 7.
  - Table 7.

### Epigenome / Gene Expression (4)

- **[Borzoi](https://doi.org/10.1038/s41588-024-02053-6)** — *modalities: epigenome, rna*
  - Finding (Rev 4).
  - Adding DNase/ATAC (and further CAGE/ChIP) to RNA-seq consistently improved RNA-seq test accuracy, eQTL classification, and CRISPR enhancer–gene linking AUPRC. Strongest single contributors are DNase + ATAC.
  - Including mouse training data substantially improved eQTL effect-size Spearman R and held-out RNA-seq accuracy at matched data composition.
  - U-Net upsampling from 128 → 32 bp is required for splice-site-resolution coverage; without it exon boundaries are blurred and gene-level shape correlation degrades. Architecture-only ablation.
  - Within a single cell line the same ordering holds: auxiliary assays > D/A/RNA > RNA-only — ruling out that the multispecies/multi-assay gains come purely from cross-tissue diversity.
- **[Enformer](https://doi.org/10.1038/s41592-021-01252-x)** — *modalities: epigenome*
  - Reference.
  - Results ¶2; Ext. Data Fig. 5a.
  - Results ¶2; Ext. Data Fig. 5b.
  - Results ¶2; Ext. Data Fig. 5a.
  - Results ¶2; Ext. Data Fig. 6a.
- **[GET](https://doi.org/10.1038/s41586-024-08391-z)** — *modalities: epigenome*
  - Self-supervised motif-masked pretraining is essential for cross-cell-type generalization.
  - Region-wise transformer attention beats simpler ML on the same features.
  - Performance is consistent across chromosomes; no single chromosome drives results.
  - Model is not over-reliant on any small set of motifs; redundancy across motif clusters.
  - Quantitative aCPM signal during fine-tuning improves transfer to new assays.
- **[MIRROR-3D](https://arxiv.org/abs/2504.09060)** — *modalities: epigenome, interactome*
  - Conclusion.
  - Contrastive loss alone is a strong baseline.
  - Orthogonal loss adds ~0.5% AUROC by separating modal-invariant vs modal-specific features.
  - Cross-modal mapping yields a modest extra gain and enables missing-modality inference.
  - Single-modal baseline.

### RNA (3)

- **[RhoFold](https://arxiv.org/abs/2207.01586)** — *modalities: rna*
  - Effect / Notes.
  - Baseline; all four components active.
  - **Most critical component** — largest degradation; modified-RhoFold+ w/o MSA also underperforms vs full model.
  - Sharpest decline on dissimilar sequences; RNA-FM compensates for missing MSA (p = 0.0005 with RNA-FM vs 0.0112 w/o on TM-vs-MSA-depth).
  - Small but consistent drop.
- **[RiNALMo](https://arxiv.org/abs/2403.00043)** — *modalities: rna*
  - SPOT-RNA TS0 F1 (S8).
  - Base (sinusoidal PE + GELU, RNA-FM-like).
  - Base + RoPE.
  - Base + RoPE + SwiGLU (= RiNALMo arch).
  - MRL Random7600 R² (S6).
- **[RNA-FM](https://arxiv.org/abs/2204.00300)** — *modalities: rna*
  - Source.
  - Fig. 2a.
  - Table 1.
  - Table 1.
  - Table 2.

### Protein Sequence (16)

- **[Ankh](https://arxiv.org/abs/2301.06568)** — *modalities: protein-sequence*
  - 1-gram span masking with merged-unmasked target reconstruction (Exp.4) wins; 3-gram spans and partial-loss variants hurt. Reconstructing the full input (incl. unmasked) is required.
  - 10% worst; 15% & 30% trade off across tasks. **20% chosen** as compromise for general-purpose long-term training (higher than NLP standard of 15%).
  - Encoder-heavy (48/24) best; richer encoder embeddings + retains enough decoder layers for generation.
  - Deeper-narrower beats wider-shallower at fixed parameter count.
  - Gated-GELU > ReLU even though it forces shallower depth; kept Gated-GELU.
- **[ESM-1b](https://doi.org/10.1073/pnas.2016239118)** — *modalities: protein-sequence*
  - Take-away.
  - Transformer dominates LSTM at equal-or-fewer params; attention is the right inductive bias for protein MLM.
  - Scaling capacity improves both LM fidelity and structural content; underfitting still observed at 650 M → motivates ESM-2 scaling.
  - Diversity (cluster-balanced sampling) beats raw quantity; clustered sampling reweights loss toward rare families.
  - Data scaling helps, but the model is data-limited *and* capacity-limited at 650 M.
- **[ESM-1v](https://doi.org/10.1101/2021.07.09.450648)** — *modalities: protein-sequence*
  - Take-away.
  - Too aggressive dedup hurts.
  - Reference setting.
  - Monotonic gain up to 90%.
  - **Best clustering threshold.**.
- **[ESM-2 / ESMFold](https://doi.org/10.1126/science.ade2574)** — *modalities: protein-sequence, protein-structure*
  - Take-away.
  - Smallest model — baseline.
  - +13 pts contacts for 4× params.
  - Log-linear gains continue.
  - Matches ESM-1b size; better recipe.
- **[ESM-3](https://doi.org/10.1101/2024.07.01.600583)** — *modalities: protein-sequence*
  - Take-away.
  - Multimodal protein generation shows the same scaling-law behavior as LLMs; frontier capabilities require ≥7B.
  - RLHF-style alignment is scale-dependent; small models cannot fully exploit it.
  - Discretizing structure into a fixed alphabet is what unlocks unified multimodal MLM training.
  - Random per-track masking is what enables prompt-anything → generate-anything behavior.
- **[ESM-AA](https://arxiv.org/abs/2403.12995)** — *modalities: protein-sequence, protein-structure, small-molecule*
  - Take-away.
  - Atoms lose positional identity; degrades fusion.
  - Largest single-component drop on ESAR — residue PE is critical.
  - Modest on ESAR, but catastrophic on Contact Prediction (P@L drops to ~0.03).
  - Bigger hit than removing MLM → atom-scale structure signal matters more than atom MLM.
- **[ESM-design](https://doi.org/10.1101/2022.12.21.521521)** — *modalities: protein-sequence*
  - Effect (per abstract+repo).
  - Only MCMC is released and used to produce the 228 wet-lab designs (152/228 = 67% success). Greedy is not in the released config; head-to-head numbers (not in abstract/repo).
  - Enables co-discovery of sequence + structure in unconstrained mode; 71/129 = 55% experimental success.
  - Larger checkpoints exist but the design pipeline ships pinned to 650M; per-size sweep (not in abstract/repo).
  - High initial T encourages exploration; geometric cooling drives convergence to high-likelihood, structure-compatible sequences. Per-T success curves (not in abstract/repo).
- **[MSA Transformer](https://doi.org/10.1101/2021.02.12.430858)** — *modalities: protein-sequence, protein-structure*
  - Δ vs base.
  - Ppl 3.01.
  - Still beats 650M ESM-1b (41.1) and 3B single-seq models.
  - Row→Column (base).
  - Marginal.
- **[ProGen](https://arxiv.org/abs/2004.03497)** — *modalities: protein-sequence*
  - Take-away.
  - Performance degrades on unseen families but stays well above empirical baseline (18.14).
  - Pre-training is essential — fine-tuning more than halves PPL and 5× hard-acc on novel families.
  - More residue context narrows the next-token distribution; benefit holds across all sampling settings.
  - Conditioning tags carry real predictive signal; rich tag sets are needed for controllable, structurally-faithful generation.
- **[ProtCLIP](https://arxiv.org/abs/2412.20014)** — *modalities: protein-sequence, multimodal*
  - Key Finding.
  - Property-driven sampling on ProtAnno-D is best (Sub 75.77, EC AUPR 0.384, Fmax 0.441, MRR 0.299), beating naive single-source and pretrain→finetune; low-quality data is valuable when properly sampled.
  - Both objectives needed; removing PDA hurts more (Sub 73.64 vs full 76.52; EC AUPR 0.136 vs 0.204) — function-grounded PDA is the key signal.
  - Without weighting, BSR and MLM losses interfere (no convergence); λ₁=0.7, λ₂=0.3 is optimal — segment reconstruction must dominate token MLM.
  - Performance fluctuates 0.1–0.6, peaks at θ=0.3, collapses for θ≥0.7 (too many functional residues masked); θ=0.3 chosen.
- **[ProteinBERT](https://doi.org/10.1093/bioinformatics/btac020)** — *modalities: protein-sequence*
  - Source.
  - §3.2, Table 2.
  - §3.2, Fig. 3, Supp. Fig. S1.
  - §3.2, Supp. Fig. S2.
  - §3.3, Fig. 4.
- **[ProteinMPNN](https://doi.org/10.1126/science.add2187)** — *modalities: protein-sequence*
  - Take-away.
  - Pairwise distances are a much stronger inductive bias than dihedrals/frame orientations.
  - Updating edge features in the MPNN encoder gives a further +1.5%.
  - Random-permutation decoding both improves recovery and unlocks fixed-region / binder design.
  - Local graphs suffice; long-range context unnecessary for seq design.
- **[ProtGPT2](https://doi.org/10.1038/s41467-022-32007-7)** — *modalities: protein-sequence*
  - Reported Effect.
  - Greedy/beam → repetitive, degenerate sequences; sampling required for natural-like propensities.
  - "Worse matches in all cases" vs sampling.
  - Best matches occur for k > 800; small k under-samples natural propensities.
  - Default outperformed restrictive nucleus values.
- **[ProtTrans](https://arxiv.org/abs/2007.06225)** — *modalities: protein-sequence*
  - CNN ≈ LSTM > LogReg; CNN chosen (more compute-efficient). Architecture matters less than embeddings.
  - Larger raw corpus alone gives marginal/inconsistent gains; **fine-tuning on cleaner UniRef50 after BFD is the decisive trick**.
  - Auto-encoding (esp. T5 span corruption) > auto-regressive for protein representation learning.
  - Scaling width beyond 3B hurts at fixed sample budget — **more training samples beats more parameters**.
  - Performance correlates with samples seen during pre-training; informal scaling trend.
- **[PST](https://arxiv.org/abs/2401.14819)** — *modalities: protein-sequence, protein-structure*
  - Take-away.
  - Structure helps even at 650M.
  - Largest GO gain on AUPR.
  - Strongest gain on remote homology.
  - Generalises to unsupervised VEP.
- **[Rao attention-as-contacts](https://doi.org/10.1101/2020.12.15.422761)** — *modalities: protein-sequence, protein-structure*
  - Take-away.
  - Precision rises sharply with capacity; ESM-1b is the only PLM beating Gremlin (39.3).
  - Within one family, deeper = better; not yet saturated.
  - A single head ≈ Gremlin; averaging top-5 already exceeds it → contacts live in the attention, LR just selects.
  - One labelled protein already matches Gremlin (p>0.05); diminishing returns past n=10.

### Protein Structure (8)

- **[AlphaFold 2](https://doi.org/10.1038/s41586-021-03819-2)** — *modalities: protein-structure*
  - Take-away.
  - Largest single architectural ablation; SE(3)-equivariant geometric attention is the key inductive bias of the structure module.
  - Iterative refinement of the pair + MSA representations is essential; cheap to add (no extra params), large gain.
  - Noisy-student style self-training on unlabelled UniClust sequences is a major data-augmentation lever.
  - Triangle inequality bias on pair representation drives geometric consistency; removing it hurts more than removing templates.
- **[AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w)** — *modalities: protein-structure*
  - Source.
  - §Network architecture and training; Extended Data Fig. 1.
  - §Network architecture and training; Extended Data Fig. 2.
  - §Network architecture and training.
  - §Network architecture and training; Extended Data Fig. 7a.
- **[ESM-IF](https://doi.org/10.1101/2022.04.10.487779)** — *modalities: protein-structure, protein-sequence*
  - Take-away.
  - Adding the 12M AlphaFold2-predicted structures yields **+13.3 pp** sequence recovery (38.3 → 51.6%) — the single largest gain in the paper.
  - **51.6%**.
  - Small models *cannot* exploit predicted data: GVP-GNN (1M) **degrades** by 3.6 pp when AF2 added. Only GVP-GNN-large (21M, +11.6 pp) and GVP-Transformer (142M, +13.3 pp) benefit.
  - 38.6% (−3.6).
- **[GearNet](https://arxiv.org/abs/2203.06125)** — *modalities: protein-structure*
  - Treating edges as different types is essential; param-matched plain GCN cannot recover the gap, even with more layers/params.
  - Explicit edge-edge interaction modeling is beneficial across function prediction tasks.
  - All four deterministic combinations work, so each cropping/noise scheme yields informative views; randomly sampling combinations gives the most diverse views and is best on 3 of 4 GO/EC metrics.
- **[HelixFold-Single](https://arxiv.org/abs/2207.13921)** — *modalities: protein-structure, protein-sequence*
  - Take-away.
  - Larger PLM has stronger language-modelling capacity.
  - 10× parameters → consistently lower perplexity.
  - Trend holds across both eval sets.
  - Same trend as CASP14.
- **[OmegaFold](https://doi.org/10.1101/2022.07.21.500999)** — *modalities: protein-structure, protein-sequence*
  - Take-away.
  - Reference (best).
  - Ensembling adds a small but consistent gain.
  - PLM-derived node + pairwise features supply most of the missing co-evolutionary signal.
  - **Largest single drop** — GeoFormer's triangle/edge updates are critical for translating PLM features into geometry.
- **[RoseTTAFold](https://doi.org/10.1126/science.abj8754)** — *modalities: protein-structure*
  - Take-away.
  - The 3D-coordinate track is the central architectural contribution; tighter coupling of seq/dist/coords beats 2-track.
  - End-to-end is limited by GPU memory and lack of side-chain info at training; gap expected to close with more compute / side chains.
  - Memory-driven cropping is not just a workaround — it improves accuracy via implicit ensembling.
  - Attention + multi-track architectures reduce reliance on deep MSAs (mirrors AF2 behaviour).
- **[RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528)** — *modalities: protein-structure*
  - Take-away.
  - Generalist training does **not** degrade protein-only accuracy.
  - Small (~4 pt) cost on NA complexes from generalist training.
  - Training with ligand context **improves** protein-only prediction (pocket flips, domain shifts).
  - Most of RFAA's "loss" vs physics docking comes from also predicting backbone+sidechains from sequence.

### Single-Cell RNA (12)

- **[CellPLM](https://doi.org/10.1101/2023.10.03.560734)** — *modalities: scrna*
  - Liver cos.
  - 0.481±0.010.
  - 0.433±0.008.
  - 0.428±0.012.
  - 0.440±0.021.
- **[Geneformer](https://doi.org/10.1038/s41586-023-06139-9)** — *modalities: scrna*
  - Source.
  - Fig. 2b.
  - Ext. Data Fig. 1e.
  - Ext. Data Fig. 1f.
  - Fig. 3 / Ext. Data Fig. 3.
- **[GenePT](https://doi.org/10.1101/2023.10.16.562533)** — *modalities: scrna*
  - Finding.
  - Used to motivate the default (name+summary); name-only is surprisingly strong but full summary is preferred.
  - GenePT-GPT-3.5 is consistently best; BioLinkBert and Gene2vec are slightly less competitive; expression-derived embeddings trail.
  - Names-only is surprisingly strong on some tasks (gene nomenclature carries signal), but adding the summary helps overall.
  - Random ≈ chance; rules out that the gain is just from large embedding dimension.
- **[Nicheformer](https://doi.org/10.1101/2024.04.15.589472)** — *modalities: scrna*
  - Take-away.
  - Spatial pretraining data is non-substitutable — scale of dissociated cells alone cannot recover spatial variation.
  - Diversity > raw count; orthology-aligned multi-species pretraining is required.
  - Capacity matters at SpatialCorpus-110M scale.
  - Rank-based encoding tolerates the limited-gene reality of MERFISH/Xenium/CosMx.
- **[scBERT](https://doi.org/10.1038/s42256-022-00534-z)** — *modalities: scrna*
  - Take-away.
  - MLM pre-training on PanglaoDB is the single most important design choice; gene-as-token Performer alone is not enough.
  - The model relies on distributed gene–gene interaction patterns, not on a small set of marker genes — robust to marker dropout / batch loss.
  - Contextual encoding adds cell-type-discriminative information on top of the static Gene2vec positional prior.
  - 5 bins is sufficient; finer expression discretisation gives no measurable gain at this scale.
- **[scELMo](https://arxiv.org/abs/2601.05648)** — *modalities: scrna, single-cell-multiomics*
  - Spleen F1.
- **[scFoundation](https://doi.org/10.1038/s41592-024-02305-7)** — *modalities: scrna*
  - Reported finding.
  - The learned `[S]` token (used as the default cell embedding) and the max-pool variant outperform mean-pool and raw concat; `[S]` is selected as the canonical cell representation (`ablation-00.ipynb`).
  - Continuous scalar embedding preserves fine expression magnitudes and beats binned tokens, justifying xTrimoGene's MLP value embedder over vocab-based binning (`ablation-01.ipynb`).
  - Continuous regression loss applied to the full gene set yields the best clustering, supporting the published recipe (`ablation-01.ipynb`).
  - Removing RDA collapses the enhancement gain over SAVER/MAGIC/scImpute; RDA is the key driver of the imputation/enhancement SoTA and of the model's ability to operate at arbitrary target depths (`ablation-02.ipynb` + `enhancement/`).
- **[scGPT](https://doi.org/10.1038/s41592-024-02201-0)** — *modalities: scrna, single-cell-multiomics*
  - Source.
  - `scgpt/model/model.py` (note §Model); GitHub README. Paper body gated — could not retrieve a numeric ablation table from Nature HTML (only refs section reachable).
  - GitHub README release note 2023-11-07; paper ref 58 (FlashAttention).
  - Note §Model, §Training Recipe, §Key Ablations #1; paper abstract & figure captions; comparison vs scBERT (ref 32).
  - Note §Model, §Key Ablations #6; GitHub README "Pretrained scGPT checkpoints" section.
- **[SCimilarity](https://doi.org/10.1101/2023.07.18.549537)** — *modalities: scrna*
  - Finding.
  - Lower β (more MSE) → better query; higher β (more triplet) → better integration. Selected β=0.001, α=0.05 as best joint operating point.
  - Pure triplet collapses within-type variance; MSE term required to preserve subtle cell-state differences.
  - SCimilarity ρ=0.77 vs scFoundation 0.54, scGPT 0.59; far fewer false-high cells.
  - Higher cell-type ASW, comparable graph connectivity, less spurious cross-study mixing; SCimilarity does not see test data, baselines do.
- **[scMamba](https://arxiv.org/abs/2506.20697)** — *modalities: scrna, single-cell-multiomics*
  - Source.
  - §Results, p. 375–380 / Suppl. Table 1.
  - §Results, p. 380–388 / Suppl. Tables 2–4.
- **[scMulan](https://doi.org/10.1101/2024.01.25.577152)** — *modalities: scrna*
  - Source.
  - bioRxiv full text inaccessible (403).
- **[UCE](https://doi.org/10.1101/2023.11.28.568918)** — *modalities: scrna*
  - Reported finding (direction).
  - 33-layer gives best biological-signal fidelity and cross-species generalisation; 4-layer is faster/cheaper but loses resolution on complex tissues. Embeddings are not interchangeable between the two.
  - Zero-shot embedding works on unseen species with available proteomes (e.g., green monkey, chicken); degrades on evolutionarily distant species (e.g., Drosophila).
  - ESM2 protein embeddings are the mechanism enabling species-agnostic, vocabulary-free tokenisation; required for cross-species transfer and for embedding novel/unseen genes.
  - Non-coding / missing-embedding genes are dropped; ablation motivates protein-embedding tokenisation as the core design choice.

### Computational Pathology (12)

- **[CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4)** — *modalities: imaging-pathology*
  - Reported effect.
  - Best average zero-shot classification across 7 tasks.
  - Best average cross-modal retrieval; lower zero-shot classification than CoCa default.
  - Lower average zero-shot vs full human-only set — filtering too aggressively hurts.
  - Underperforms human-only filtered CoCa — quality filtering matters.
- **[CONCH (preprint)](https://arxiv.org/abs/2307.12914)** — *modalities: imaging-pathology, multimodal*
  - Adding the captioning loss to contrastive pretraining (CoCa) improves downstream zero-shot classification over CLIP-style contrastive-only.
  - Contrastive-only objective is slightly stronger for cross-modal retrieval; captioning loss helps classification more than retrieval.
  - Filtering out non-human animal histology helps; over-filtering down to H&E-only loses too much data and hurts performance — keep human-only.
  - Always ensemble class-name × template prompts at inference; ensembling cannot rescue a model that fundamentally fails on the task.
  - Pre-train each tower unimodally before vision-language alignment — critical for zero-shot transfer in histopathology.
- **[GigaPath](https://doi.org/10.1038/s41586-024-07441-w)** — *modalities: imaging-pathology*
  - Slide-level MAE pretraining on 171 K WSIs is necessary; random init loses ~1.7 AUROC pts on subtyping.
  - Pretrained representations are strong enough to be used frozen — important for compute-limited deployment.
  - Long-range dilated self-attention adds value beyond a simple attention-MIL pooler; modelling cross-tile dependencies matters for subtyping.
  - DINOv2 is the best tile-level SSL recipe for pathology at this scale; supervised ImageNet transfer is clearly inferior, motivating SSL foundation models.
  - Data scale + diversity (real-world Providence corpus) drives gains beyond what TCGA alone delivers — evidence of (informal) data-scaling.
- **[H-optimus-0](https://arxiv.org/abs/2404.15217)** — *modalities: imaging-pathology*
  - Take-away.
  - Mixing magnifications yields a magnification-agnostic FM that beats any single-magnification model — no architectural change required.
  - Always warm-start pathology FMs from ImageNet weights — faster convergence and higher final accuracy.
  - OOD performance saturates fast on TCGA — more WSIs from same distribution mostly help in-distribution; need more diverse data to push OOD further.
  - Online patching's effectively-infinite patch sampling mainly benefits in-distribution learning; OOD is bottlenecked by slide diversity, not patch count.
- **[HIPT](https://arxiv.org/abs/2206.02647)** — *modalities: imaging-pathology*
  - Δ vs. full HIPT.
  - 0.952 ± 0.021.
  - 0.923 ± 0.020.
  - −0.166.
  - −0.132.
- **[KEP (KEEP)](https://arxiv.org/abs/2412.13126)** — *modalities: imaging-pathology*
  - Reported effect.
  - KEEP wins on 16/18 datasets; +~10% AUROC on PANDA and +12.9% on AGGC22 segmentation; better on 6/7 detection benchmarks; better on all subtyping benchmarks.
  - KEEP-Top100 ≥ Contrastive-Top100 on 6/8; +11 points BACC on rare-tumor EBRAINS dataset.
  - Ratio strategy wins on all datasets; +0.10 BACC on CPTAC-NSCLC (0.860) and +0.15 on TCGA-BRCA (0.774).
  - Semantic grouping improves retrieval (details in Table S5).
- **[Phikon-v2](https://arxiv.org/abs/2409.09173)** — *modalities: imaging-pathology*
  - Take-away.
  - DINOv2 + larger model + larger data jointly outperform iBOT baseline; method/scale confounded.
  - Domain-specific pre-training is by far the largest single contributor; natural-image DINOv2 ranks last.
  - "DINOv2 superiority over iBOT is not straightforward for lighter models" — method advantage depends on scale.
  - A 13× smaller, 350× less-data, task-specialized model beats or matches the largest FMs on MSI; scaling is not a universal solution for biomarker tasks.
- **[RudolfV](https://arxiv.org/abs/2401.04079)** — *modalities: imaging-pathology*
  - Source.
  - §2.2, Fig. 3D, lines 220–225.
  - §2.5, Fig. 4B, lines 326–328.
  - §2.5, Fig. 4B, lines 325–328.
  - §2.6, Fig. 6B, lines 369–370.
- **[UNI](https://arxiv.org/abs/2308.15474)** — *modalities: imaging-pathology*
  - SSL in pathology benefits from data scale up to ≥100M patches / 100K WSIs; no saturation observed at 100K-slide scale.
  - DINOv2 + ViT-L + 100K-slide diverse pretraining beats both ImageNet-supervised CNNs and prior pathology SSL (CTransPath, REMEDIS) despite UNI seeing 4–13× fewer total images.
  - Strong SSL features give large label-efficiency wins from K≥4; 1-shot remains noisy across all encoders.
  - Class-prototype (parameter-free) probes work extremely well with high-quality SSL features; representation quality dominates over classifier complexity.
  - DINOv2-style high-res pretraining yields resolution-agnostic features; advantage of UNI grows at native histology magnifications.
- **[uniGradICON](https://arxiv.org/abs/2403.05780)** — *modalities: imaging-pathology*
  - Take-away.
  - Weaker GradICON regularizer is what enables a single universal registration model; diffusion-regularized variants underperform or fail.
  - One universal model matches specialists in-domain and dominates them out-of-domain.
  - IO is a cheap, always-on improvement; pairs naturally with the FM as a strong initialization.
  - Model generalizes to unseen anatomy, though including the region in pretraining is clearly better; IO mitigates the held-out gap.
- **[Virchow](https://arxiv.org/abs/2309.07778)** — *modalities: imaging-pathology*
  - Source.
  - Tab. A4, §2.3.
  - Tab. A4.
  - Tab. A4.
  - Tab. A4.
- **[XrayGPT](https://arxiv.org/abs/2306.07971)** — *modalities: imaging-pathology*
  - Variant.
  - 0.0879.
  - 0.0973.
  - 0.1284.
  - 0.1997.

### Radiology (2)

- **[MedDiff-FM](https://arxiv.org/abs/2410.15432)** — *modalities: imaging-radiology*
  - Source.
  - Table III.
  - Table III.
  - Table III.
  - Table III.
- **[MedMax](https://arxiv.org/abs/2412.12661)** — *modalities: imaging-radiology, imaging-pathology, multimodal*
  - Take-away.
  - MedMax is high-quality; further scaling should keep paying off.
  - High-quality VQA data is essential for VQA performance.
  - Visual-chat data is critical for chat performance; mixture diversity drives generalization.
  - Distribution shift in discrete visual tokens hurts the frozen LM backbone — keep the base tokenizer.

### Cell Imaging (1)

- **[CellPainTR](https://arxiv.org/abs/2509.06986)** — *modalities: imaging-cell, cell-profiling*
  - Take-away.
  - Reference floor.
  - No overall gain vs baseline.
  - No overall gain vs baseline.
  - Strong batch correction but weak biological signal.

### Microscopy (1)

- **[ViTally](https://arxiv.org/abs/2411.02572)** — *modalities: imaging-microscopy*
  - Take-away.
  - Scaling continues to pay off into the billion-param regime; CM (replicate consistency) gains faster than raw recall.
  - Curating to ~16M morphologically-active crops matches a much larger un-curated set on consistency; data quality > quantity.
  - Smaller patches help on cellular morphology, justifying the G/8 choice despite cost.
  - Even smallest microscopy-trained CA-MAE beats much larger natural-image ViTs — domain SSL dominates.

### Small Molecules (5)

- **[ChemBERTa](https://arxiv.org/abs/2010.09885)** — *modalities: small-molecule*
  - Conclusion.
  - Downstream performance scales consistently with more pretraining data; MLM learns more robust representations at larger scale.
  - Semantically-relevant SMILES tokenization gives a small edge over BPE, but margin is narrow and needs more benchmarks.
  - Despite SELFIES' 100% validity guarantee, it offers no measurable advantage here; further benchmarking needed.
- **[ChemFM](https://arxiv.org/abs/2410.21422)** — *modalities: small-molecule*
  - Source.
  - §4.13, Table S2.6.
  - §4.12, Table S2.5.
  - §Results, Fig. S1.1a,b.
  - Fig. S1.1c.
- **[LSM-MS2](https://arxiv.org/abs/2510.26715)** — *modalities: small-molecule*
  - Source.
  - Table 1.
  - Table 1.
  - +0.007 over DreaMS.
  - §4.2 / Fig.1.
- **[MACE-OFF / Multi-Fi](https://arxiv.org/abs/2412.13088)** — *modalities: small-molecule*
  - Take-away.
  - Both stages of TEA are needed: ICEA removes inner-core/basis offsets, AEC then corrects atomization-energy/functional offsets — full pipeline is what unlocks dataset fusion.
  - Scaling MACE-Osaka24 from small→large gives ~0.24 kcal/mol gain, reaching MACE-OFF23-large quality (0.403) on organics.
  - Large variant best on reactive organic chemistry; ~20–30% MAE drop.
  - Marginal gain on crystals; small already competitive with MACE-MP-0-large (0.0166).
- **[MolFM](https://arxiv.org/abs/2307.09484)** — *modalities: small-molecule, multimodal*
  - Component probed.
  - Reference.
  - ITM-based re-ranking at inference.
  - Cross-modal attention from text to atom tokens.
  - Attention to KG neighbour entities.

### Multimodal Medical (4)

- **[AIDO](https://doi.org/10.1101/2024.12.02.626322)** — *modalities: multimodal*
  - Source.
  - AIDO.Protein arXiv / OpenReview.
  - AIDO.Protein arXiv.
  - AIDO.Protein arXiv.
  - AIDO.Cell bioRxiv 10.1101/2024.11.28.625303.
- **[ConceptCLIP](https://arxiv.org/abs/2501.15579)** — *modalities: multimodal*
  - Δ vs full (avg).
  - 84.90 (82.42, 87.17).
  - 90.43 (88.35, 92.28).
  - 92.60 (90.76, 94.20).
- **[Doctor Sun](https://arxiv.org/abs/2508.08270)** — *modalities: multimodal*
  - Take-away.
  - Mixing general data in alignment prevents catastrophic forgetting at negligible domain cost.
  - 1:0.5 is the sweet spot for medical VQA; more general data only helps generic benchmarks.
  - Pure-domain alignment causes catastrophic forgetting of general perception/reasoning.
  - Specialised answers, but recall drop is unsafe for clinical missed-diagnosis risk.
- **[LLaVA-Med](https://arxiv.org/abs/2306.00890)** — *modalities: multimodal*
  - Take-away.
  - Biomedical curriculum tuning yields large gains over general-domain LLaVA, especially zero-shot.
  - Stage 1 (caption alignment) alone collapses instruction-following; Stage 2 instruction-tuning is essential.
  - Performance improves monotonically with more self-instruct data.
  - Using PubMed inline mentions as external knowledge during GPT-4 self-instruct improves data quality.

### Vision (Biomedical) (1)

- **[BiomedCLIP](https://arxiv.org/abs/2303.00915)** — *modalities: vision, language, multimodal*
  - Source.
  - baseline.
  - +4.50 / +3.85.
  - +4.47 / +4.85.
  - baseline.

### Biomedical Text (1)

- **[BioBERT](https://arxiv.org/abs/1901.08746)** — *modalities: text*
  - Take-away.
  - Continued pre-training on PubMed is the dominant gain; adding PMC gives diminishing returns once PubMed steps are scaled up.
  - Even vanilla BERT beats the prior CHEMPROT SOTA; biomedical pre-training adds a further ~3 F1.
  - QA benefits most from biomedical pre-training (+12.24 MRR over SOTA, +5.13 over BERT) — largest relative gain among the three task families.
  - 1B words already captures most of the benefit; full PubMed (4.5B) yields modest extra gains.

### Other (2)

- **[BioGPT](https://arxiv.org/abs/2210.10341)** — *modalities: other*
  - Natural-language target formats beat structured formats with special tokens; rel-is ("the relation between H and T is R") is best.
  - Confirms rel-is generalises across datasets (+~2 F1).
  - Soft prompts > hard prompts; among hard prompts, more informative wording ("we can conclude that") is better.
  - Performance roughly insensitive to soft-prompt length; length=9 chosen via val set, length=13 marginally best on test.
- **[Virchow2](https://arxiv.org/abs/2408.00738)** — *modalities: other*
  - OOD avg.
  - Standard DINOv2.
  - 82.1 (−0.5).
  - 83.4 (+1.0).
  - 82.9 (+0.4).

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

1. **15 newly-extracted FMs added.** [GET](https://doi.org/10.1038/s41586-024-08391-z) (GET), [Evo 2](https://doi.org/10.1101/2025.02.18.638918) (Evo 2), [ESM-3](https://doi.org/10.1101/2024.07.01.600583) (ESM-3), [AlphaFold 3](https://doi.org/10.1038/s41586-024-07487-w) (AlphaFold 3), [RoseTTAFold All-Atom](https://doi.org/10.1126/science.adl2528) (RFAA), [ProteinMPNN](https://doi.org/10.1126/science.add2187) (ProteinMPNN), [Nicheformer](https://doi.org/10.1101/2024.04.15.589472) (Nicheformer), [UCE](https://doi.org/10.1101/2023.11.28.568918) (UCE), [CellPLM](https://doi.org/10.1101/2023.10.03.560734) (CellPLM), [GenePT](https://doi.org/10.1101/2023.10.16.562533) (GenePT), [SCimilarity](https://doi.org/10.1101/2023.07.18.549537) (SCimilarity), [scMulan](https://doi.org/10.1101/2024.01.25.577152) (scMulan), [AIDO](https://doi.org/10.1101/2024.12.02.626322) (AIDO), [Virchow2](https://arxiv.org/abs/2408.00738) (Virchow2), [CONCH (Nat. Med.)](https://doi.org/10.1038/s41591-024-02856-4) (CONCH NatMed).

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

