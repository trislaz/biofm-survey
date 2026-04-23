# Bio-Foundation-Model Survey — Guidebook for Practitioners

## Scope & Method

This guidebook distils practical design rules from **85 fully extracted papers** spanning DNA, RNA, protein (sequence & structure), single-cell transcriptomics, computational pathology, cell-painting / high-content microscopy, mass-spectrometry proteomics, small-molecule chemistry, multimodal medical imaging, and biomedical text.
REV 3 added ~36 pre-2023 "anchor" papers to correct a 2023-2026 recency bias in earlier revisions, ensuring that foundational contributions (AlphaFold 2, ESM-1b, scVI, DNABERT, etc.) are properly represented alongside more recent work. ← REV 3

## Executive Summary — Top-10 Practitioner Take-aways

1. **Tokenization is a first-class design axis.**
   Overlapping k-mer tokenization launched the DNA-as-language paradigm [dnabert-pre-trained-bidirectional-2021] but introduces k-mer leakage; byte-level tokenization removes this entirely and enables multi-kingdom modelling at the cost of longer sequences [sequence-modeling-and-design-2024].
   For single-cell data, rank-value encoding [transfer-learning-enables-predictions-2023] and expression-binning [scgpt-toward-building-a-2024] each outperform naïve count vectors. ← REV 3

2. **Architecture must match the inductive bias of the modality.**
   Structure prediction requires specialised blocks — Evoformer + IPA in AlphaFold 2 [highly-accurate-protein-structure-2021], three-track networks in RoseTTAFold [accurate-prediction-of-protein-2021] — while sequence-only tasks are well-served by standard Transformers or, at byte level, by state-space hybrids (StripedHyena) [sequence-modeling-and-design-2024]. ← REV 3

3. **Data diversity beats data volume.**
   ESM-1b showed that UniRef50 (diverse, clustered) outperforms larger but redundant corpora [biological-structure-and-function-2021];
   GearNet demonstrated that 805K AlphaFold-predicted structures can match sequence models pretrained on billions of tokens [protein-representation-learning-by-2022]. ← REV 3

4. **Scaling laws hold but saturate at different rates per modality.**
   ESM-2 contact precision rises from 15.9 % (8 M params) to 54.5 % (15 B) without saturation [evolutionary-scale-prediction-of-2023];
   ProtTrans showed training longer beats scaling wider (T5-XL-U50 3 B > T5-XXL 11 B) [prottrans-towards-cracking-the-2020]. ← REV 3

5. **MSA-free structure prediction is viable.**
   ESMFold [evolutionary-scale-prediction-of-2023], OmegaFold [high-resolution-de-novo-2022], and HelixFold-Single [helixfold-single-msa-free-2022] achieve near-AlphaFold 2 accuracy at 60–500× speed-up, especially on orphan proteins without deep alignments. ← REV 3

6. **Distillation from AlphaFold predictions is a general-purpose data multiplier.**
   AlphaFold 2's own self-distillation added +1.8 GDT [highly-accurate-protein-structure-2021];
   ESM-IF trained on 12 M AF2-predicted structures gained +10 pp sequence recovery [learning-inverse-folding-from-2022];
   HelixFold-Single distilled ~1 M AF2 labels to bootstrap PLM-based folding [helixfold-single-msa-free-2022]. ← REV 3

7. **Hierarchical aggregation matters for whole-slide pathology.**
   HIPT's three-stage ViT (256→4096→WSI) with DINO achieves AUC 0.952 vs 0.786 without hierarchical pretraining [scaling-vision-transformers-to-2022];
   GigaPath scales to 1.3 B tiles using DINOv2 + LongNet [a-whole-slide-foundation]. ← REV 3

8. **Evaluation benchmarks set the research agenda — and their biases persist.**
   TAPE [evaluating-protein-transfer-learning-2019] canonised five protein tasks;
   attention-as-contacts [transformer-protein-language-models-2021] showed attention maps encode structural information, spawning a sub-field. ← REV 3

9. **Lightweight fine-tuning unlocks large frozen models.**
   NT showed IA3 tuning (0.1 % params) matches full fine-tuning [the-nucleotide-transformer-building-2024];
   UNI 8-shot matches competitors at 128-shot (16× label efficiency) [a-general-purpose-self-2023];
   CLAM trains only ~800 K attention-pooling params atop a frozen ResNet50 [data-efficient-and-weakly-2020]. ← REV 3

10. **Generative design is moving from proof-of-concept to experimental validation.**
    ESM-design achieved 67 % wet-lab success (152/228 designs) using frozen ESM-2 + MCMC, with 35 designs having no natural homologs [language-models-generalize-beyond-2022];
    ProtGPT2 generates novel topologies at 87.6 % globularity [protgpt2-is-a-deep]. ← REV 3

---

## Design-Choice Axes

### Tokenization & Vocabulary

**Nucleotide sequences.**

- DNABERT-1 introduced overlapping k-mer (k = 3–6) tokenization for DNA, treating each k-mer as a word and using a stride-1 sliding window [dnabert-pre-trained-bidirectional-2021].
  While effective, overlapping k-mers leak positional information across tokens. ← REV 3
- The Nucleotide Transformer adopted non-overlapping 6-mers across multi-species genomes [the-nucleotide-transformer-building-2024]. ← REV 3
- DNABERT-2 replaced k-mers with BPE, unifying the vocabulary automatically and outperforming k-mer on 21/28 genomic tasks with 3–4× lower FLOPs `[dnabert-2-efficient-foundation-2023]`.
  Vocabulary size is non-monotonic: 4,096 BPE tokens is the sweet spot for DNA.
- At the extreme, Evo operates on raw single-nucleotide tokens (byte-level), eliminating tokenization artefacts entirely but requiring 131 k-token context windows [sequence-modeling-and-design-2024].
- Learnable VQ tokenization (VQDNA-HRQ) achieves 2× the linear-probe F1 of BPE and ranks #1 across 32 tasks with 103M params `[vqdna-unleashing-the-power-2024]`.
- GBST (learnable soft tokenizer) enables an 8M-param RNA model to match a 650M fixed-tokenizer model on specific tasks `[character-level-tokenizations-as-2024]`.

**Protein sequences.**

- Most protein LMs use single-amino-acid tokens (20 standard + special tokens), as established by ESM-1b [biological-structure-and-function-2021] and the TAPE benchmark suite [evaluating-protein-transfer-learning-2019]. ← REV 3
- ProtGPT2 explored BPE over amino acids (average token ≈ 4 residues), offering subword compression analogous to NLP practice [protgpt2-is-a-deep]. ← REV 3
- ProtTrans compared six architectures and found that tokenization interacts with model family — T5-XL-U50 on UniRef50 was optimal [prottrans-towards-cracking-the-2020]. ← REV 3
- Ankh uses partial de-masking (merging consecutive unmasked tokens on the output side) for +3.9 pp average improvement `[ankh-optimized-protein-language-2023]`.

**Single-cell RNA.**

Tokenization of expression profiles is an active design axis with four competing strategies:

- **scBERT:** treats each gene as a token and bins expression into five discrete levels [scbert-as-a-large-2022]. ← REV 3
- **Geneformer:** replaces raw counts with rank-value encoding — genes ranked by expression relative to corpus-wide medians, converting a continuous vector into an ordered sequence [transfer-learning-enables-predictions-2023]. ← REV 3
- **scGPT:** uses finer 51-bin value discretization and sorts genes by expression level, applying generative attention masking [scgpt-toward-building-a-2024]. ← REV 3
- **scFoundation:** introduces read-depth-aware (RDA) tokenization to decouple biological signal from sequencing depth [large-scale-foundation-model-2024]. ← REV 3

**Small molecules.**

- ChemBERTa applied RoBERTa-style BPE directly to SMILES strings, pretraining on up to 10 M PubChem compounds [chemberta-large-scale-self-2020].
  Performance scaled with pretraining data size (100 K→10 M) but did not surpass graph-based methods (D-MPNN), suggesting SMILES linearisation may lose structural information. ← REV 3
- Open-vocabulary tokenizers (Smirk, Smirk-GPE) eliminate UNK tokens that plague chemistry-specific tokenizers (up to 50% UNK rate on diverse datasets) `[tokenization-for-molecular-foundation-2024]`.

**Biomedical text.**

- BioBERT demonstrated that continued pretraining of BERT_BASE on PubMed + PMC abstracts yields +12.24 % MRR on BioASQ QA, establishing the domain-adaptation paradigm for biomedical NLP [biobert-a-pre-trained-2019]. ← REV 3

**Recommendation:** For DNA, use BPE (~4k vocab) or learnable VQ; avoid fixed k-mer.
For RNA, prefer single-nucleotide tokenization or GBST for extreme parameter efficiency.
For proteins, character-level with partial de-masking is well-validated.
For single-cell, rank-value (Geneformer) or expression binning (scGPT) depending on task.
For molecules, use open-vocabulary tokenizers to avoid UNK-induced information loss.

### Architecture Family

**Standard Transformers** dominate sequence modelling.
ESM-1b (650 M, 33 layers) [biological-structure-and-function-2021], ESM-2 (up to 15 B) [evolutionary-scale-prediction-of-2023], and ProtTrans (up to 11 B T5-XXL) [prottrans-towards-cracking-the-2020] all use conventional encoder or encoder-decoder Transformers.
ProteinBERT showed that a lightweight dual local-global architecture (16 M params) can match TAPE baselines at 2.4× fewer parameters via joint sequence + GO-annotation pretraining [proteinbert-a-universal-deep]. ← REV 3

**Axial / structured attention.**

- MSA Transformer applies row + column axial attention across aligned sequences, with tied row attention as the critical innovation — achieving 57.4 % top-L long-range contacts vs 41.1 % for ESM-1b at 6.5× fewer parameters [msa-transformer-2021]. ← REV 3

**State-space hybrids.**

- Evo's 7 B StripedHyena interleaves state-space layers with attention, enabling 131 k-token byte-level context on prokaryotic genomes.
  A pure Transformer++ of similar size was substantially worse at byte-level resolution [sequence-modeling-and-design-2024].
- Caduceus (1.9M params, Mamba) beats NT-v2 (500M) on long-range VEP `[caduceus-bi-directional-equivariant-2024]`.
- HyenaDNA achieves SOTA on 12/18 NT benchmarks with 1,500× fewer parameters `[hyenadna-long-range-genomic-2023]`.

**CNN + Transformer hybrids.**

- Enformer combines convolutional stem layers with transformer blocks to achieve 200 kb receptive fields for gene expression prediction, outperforming pure CNNs (Basenji2) across all model sizes [effective-gene-expression-prediction-2021]. ← REV 3
- Borzoi extends this to 524 kb with U-Net upsampling to reach 32 bp resolution [predicting-rna-seq-coverage-2023]. ← REV 3

**Structure-prediction architectures.**

- AlphaFold 2 introduced the Evoformer (48 blocks of row/column gated self-attention + pair bias) coupled with an Invariant Point Attention (IPA) structure module and 3-pass recycling [highly-accurate-protein-structure-2021]. ← REV 3
- RoseTTAFold uses a three-track (1D sequence / 2D distance / 3D coordinate) architecture with SE(3)-equivariant layers, enabling complex prediction from monomer inputs alone [accurate-prediction-of-protein-2021]. ← REV 3
- OmegaFold replaces MSA with a 66-layer Gated Attention Unit (GAU) PLM feeding into GeoFormer + IPA [high-resolution-de-novo-2022]. ← REV 3
- HelixFold-Single uses a DeBERTa-based PLM coupled to AF2's structure module [helixfold-single-msa-free-2022]. ← REV 3

**Geometric GNNs for protein structure.**

- GVP (Geometric Vector Perceptrons) introduced SE(3)-equivariant vector features, reducing perplexity from 6.55 (Structured GNN) to 5.29; removing vector channels degrades performance by 38–47 % [learning-from-protein-structure-2020]. ← REV 3
- GearNet added relational graph construction + edge message passing, showing that 805 K AlphaFold structures match sequence models trained on 24 M–2.1 B sequences for structure-based tasks [protein-representation-learning-by-2022]. ← REV 3

**Pathology architectures.**

- CLAM introduced attention-based MIL pooling + instance-level clustering on frozen ResNet50 features (~800 K trainable params), achieving AUC > 0.95 as a canonical baseline [data-efficient-and-weakly-2020]. ← REV 3
- HIPT uses a three-stage hierarchical ViT (256→4096→WSI) with DINO self-supervised pretraining [scaling-vision-transformers-to-2022]. ← REV 3
- GigaPath scales to ViT-giant (1.13 B) tiles + LongNet slide aggregation (86 M), with DINOv2 > SimCLR > MAE for tile encoding [a-whole-slide-foundation]. ← REV 3

**Asymmetric encoder-decoder.**

- scFoundation's xTrimoGene uses a large encoder with a small decoder, with a sparse attention encoder that reduces FLOPs by 1–2 orders of magnitude for gene expression modelling [large-scale-foundation-model-2024]. ← REV 3

**MoE (Mixture of Experts).**

- Sparse MoE for multi-channel microscopy cuts attention FLOPs by ~50% with only −1.7% accuracy; top-k=2 is the sweet spot `[sparse-mixture-of-experts-2025]`.
- CodonMoE adapts DNA backbones to mRNA with expert routing outperforming dense layers at matched parameters `[codonmoe-dna-language-models-2025]`.

**Recommendation:** Use encoder-only Transformers with ALiBi + SwiGLU for short-to-medium-range classification.
Use Mamba/Hyena SSMs for long-range genomics (>10k bp).
Use encoder-decoder for joint understanding + generation.
For structure prediction, specialised architectures (Evoformer, 3-track) remain necessary.
For structure encoding, geometric GNNs (GVP, GearNet) are parameter-efficient alternatives.

### Pretraining Objective

**Masked language modelling (MLM)** remains the dominant pretraining objective for sequence models:

- Used by ESM-1b/ESM-2 [biological-structure-and-function-2021] [evolutionary-scale-prediction-of-2023], DNABERT [dnabert-pre-trained-bidirectional-2021], RNA-FM [interpretable-rna-foundation-model-2022], and scBERT [scbert-as-a-large-2022]. ← REV 3
- ESM-1v demonstrated that the masked marginal scoring strategy (averaging over all possible masked positions) gives the best zero-shot variant prediction (Spearman ρ ≈ 0.44) [language-models-enable-zero-2021]. ← REV 3
- Geneformer uses rank-value MLM where tokens represent gene expression ranks rather than nucleotides [transfer-learning-enables-predictions-2023]. ← REV 3

**Autoregressive (next-token prediction).**

- ProtGPT2 showed decoder-only generation of plausible protein sequences (87.6 % globular) [protgpt2-is-a-deep]. ← REV 3
- Evo extended this to byte-level DNA with cross-modal generation (protein–RNA codesign) [sequence-modeling-and-design-2024].
- scGPT applies a modified autoregressive objective with generative attention masking where genes are sorted by expression [scgpt-toward-building-a-2024].

**Structure-specific losses.**

- AlphaFold 2 uses FAPE (frame-aligned point error) loss and a masked-MSA auxiliary loss; recycling is critical (no recycling = −3.1 GDT). FAPE removal also substantially degrades accuracy [highly-accurate-protein-structure-2021]. ← REV 3 (verified)

**Supervised regression.**

- Enformer uses Poisson NLL over binned epigenomic/expression tracks [effective-gene-expression-prediction-2021]. ← REV 3
- Borzoi extends to a Poisson multinomial objective for RNA-seq coverage at 32 bp resolution [predicting-rna-seq-coverage-2023]. ← REV 3

**Generative latent-variable models.**

- scVI introduced a VAE with zero-inflated negative binomial (ZINB) likelihood for scRNA-seq, scaling to 1.3 M cells in < 2 h on GPU — at a time when ZIFA and ZINB-WaVE failed above 100 K cells [a-deep-generative-model-2017]. ← REV 3
- totalVI extended this with a conditional VAE for joint RNA + protein (CITE-seq) modelling, using an NB mixture for protein background correction [joint-probabilistic-modeling-of-2021]. ← REV 3

**Multi-objective pretraining.**

- ProteinBERT jointly optimises MLM and Gene Ontology (GO) annotation prediction through a dual-stream architecture [proteinbert-a-universal-deep]. ← REV 3
- scGPT adds MVC (masked value classification), ECS (elastic cell similarity), and DAB (domain-adaptive batching) fine-tuning objectives [scgpt-toward-building-a-2024].

**Contrastive objectives.**

- GearNet showed that multiview contrastive learning (cropping different substructures of the same protein) is the best self-supervised objective for protein structure encoders, outperforming reconstruction-based alternatives [protein-representation-learning-by-2022]. ← REV 3
- CONCH uses CoCa-style contrastive + captioning learning across histology images and pathology text [towards-a-visual-language-2023]. ← REV 3
- JEPA, phylogenetic losses, and contrastive objectives (ProtCLIP) address weaknesses of standard MLM (granularity trap, lack of global semantics) `[jepa-dna-grounding-genomic-2026, a-phylogenetic-approach-to-2025, protclip-function-informed-protein-2024]`.

**Domain-adapted continued pretraining.**

- BioBERT demonstrated that continued MLM on in-domain corpora (PubMed + PMC) is essential — general-domain BERT under-performs by large margins on biomedical NER, relation extraction, and QA [biobert-a-pre-trained-2019]. ← REV 3

### Context Length

| Model | Modality | Effective context | How |
|---|---|---|---|
| Enformer [effective-gene-expression-prediction-2021] | DNA→epigenome | 200 kb (≈ 200 k nt) | CNN stem + transformer | ← REV 3
| Borzoi [predicting-rna-seq-coverage-2023] | DNA→RNA-seq | 524 kb | U-Net upsampling over Enformer-like | ← REV 3
| Evo [sequence-modeling-and-design-2024] | DNA (byte) | 131 k tokens | StripedHyena SSM + attn |
| Caduceus | DNA | 131 k tokens | BiMamba |
| DNABERT-2 | DNA (BPE) | 128 k BPE tokens | ALiBi |
| NT [the-nucleotide-transformer-building-2024] | DNA (6-mer) | 12 k 6-mers ≈ 72 k nt | Learned positional embeddings | ← REV 3
| AF2 [highly-accurate-protein-structure-2021] | Protein + MSA | training: 256 → 384/640 residue crops; inference: full-length (recycled) | Evoformer crops + recycling | ← REV 3 (verified)
| DNABERT-1 [dnabert-pre-trained-bidirectional-2021] | DNA (k-mer) | 512 k-mers | BERT positional embeddings | ← REV 3
| GigaPath [a-whole-slide-foundation] | Pathology | 131 k tiles per WSI | LongNet dilated attention |

The trend is clear: effective context has grown from 512 tokens (DNABERT-1, 2021) through 200 kb (Enformer, 2021) to 524 kb (Borzoi, 2023), driven by hybrid architectures rather than pure Transformer scaling.
For genomic regulation, Borzoi's 524 kb captures distal enhancers that Enformer's 200 kb cannot [predicting-rna-seq-coverage-2023]. ← REV 3

### Data: Scale, Quality, Diversity

**Diversity > redundancy.**

- ESM-1b established that training on UniRef50 (clustered, diverse) outperforms larger but more redundant corpora; even at 650 M parameters, the model was still underfitting [biological-structure-and-function-2021]. ← REV 3
- ESM-1v confirmed that UniRef90 is better than UniRef50 for variant-effect prediction, where close homologs carry more signal [language-models-enable-zero-2021]. ← REV 3
- De-duplication, diversity balancing, and curation consistently outperform raw scale — 5× smaller curated datasets match or beat uncurated ones `[ankh-optimized-protein-language-2023, vitally-consistent-scaling-biological-2024]`.

**Unprecedented scale.**

- ProtTrans trained on up to 393 B tokens from BFD using 5,616 GPUs on Summit, the largest protein pretraining at the time [prottrans-towards-cracking-the-2020]. ← REV 3
- The Nucleotide Transformer trained on multi-species genomes totalling 3.2 B nucleotides, with 850 genomes at 6-mer granularity [the-nucleotide-transformer-building-2024]. ← REV 3

**Structure-prediction data.**

- AlphaFold 2 used self-distillation: training on ~350 K of its own high-confidence predictions added +1.8 GDT over PDB-only training [highly-accurate-protein-structure-2021]. ← REV 3
- ESM-IF showed that training inverse folding on 12 M AlphaFold-predicted structures (CATH-mapped) gained +10 pp sequence recovery over PDB-only (< 40 K structures), with data scale dominating over architecture choices [learning-inverse-folding-from-2022]. ← REV 3
- GearNet demonstrated 805 K AlphaFold structures match protein sequence models pretrained on 24 M–2.1 B sequences for structure-aware tasks [protein-representation-learning-by-2022]. ← REV 3

**Single-cell data.**

- scFoundation pretrains on > 50 M cells across 19,264 genes [large-scale-foundation-model-2024].
- Geneformer uses 30 M Genecorpus cells with rank-value encoding [transfer-learning-enables-predictions-2023]. ← REV 3
- scGPT uses 33 M cells [scgpt-toward-building-a-2024].
- scVI scaled to 1.3 M cells in 2017, when competing methods could not exceed 100 K [a-deep-generative-model-2017]. ← REV 3

**Pathology data.**

- UNI trained on 100 M patches from 100 K WSIs, with 8-shot UNI matching 128-shot competitors — a 16× label-efficiency gain attributed to pretraining data scale [a-general-purpose-self-2023]. ← REV 3
- GigaPath ingested 1.3 B tiles from 171 K slides [a-whole-slide-foundation]. ← REV 3
- CONCH curated 1.17 M image–caption pairs for vision-language pretraining [towards-a-visual-language-2023]. ← REV 3

**Molecule data.**

- ChemBERTa released a 77 M PubChem SMILES dataset and showed pretraining performance scales from 100 K to 10 M compounds [chemberta-large-scale-self-2020]. ← REV 3

### Multi-Modal Fusion

- Early-fusion (interleaving tokens from different modalities in a single sequence) works when modalities share a natural ordering — Evo interleaves DNA, protein, and RNA tokens for cross-modal generation [sequence-modeling-and-design-2024].
- For histology + text, CONCH applies CoCa-style joint contrastive + captioning, requiring unimodal pre-initialisation of both towers for best results [towards-a-visual-language-2023]. ← REV 3
- totalVI fuses scRNA-seq and surface protein (CITE-seq) data via a conditional VAE with modality-specific decoders, learning a shared latent space [joint-probabilistic-modeling-of-2021]. ← REV 3
- RoseTTAFold's three-track architecture (1D/2D/3D) is itself a multi-modal fusion strategy, passing information between sequence, pairwise distance, and 3D coordinate representations at every block [accurate-prediction-of-protein-2021]. ← REV 3
- Late-fusion typically aggregates modality-specific encoders at the decision level — e.g., GigaPath uses separate tile (ViT-giant) and slide (LongNet) encoders aggregated only at the final classification layer [a-whole-slide-foundation].
- Frozen encoder + learned projection + LLM decoder is a reliable pattern for biomedical multimodal models; cross-attention > concatenation `[bioreason-incentivizing-multimodal-biological-2025, molfm-a-multimodal-molecular-2023]`.

### Conditioning & Inductive Biases

**Equivariance.**

- GVP introduced SE(3)-equivariant geometric vector perceptrons for protein structures; removing vector channels degraded performance by 38–47 % across tasks [learning-from-protein-structure-2020]. ← REV 3
- AlphaFold 2's IPA module enforces SE(3) equivariance in the structure module [highly-accurate-protein-structure-2021]. ← REV 3
- RC-equivariant models (Caduceus) improve pretraining loss and downstream VEP with zero parameter overhead `[caduceus-bi-directional-equivariant-2024]`.

**Positional encoding.**

- Enformer designed a custom relative positional encoding scheme for genomic distances [effective-gene-expression-prediction-2021]. ← REV 3
- Nucleotide Transformer uses learned positional embeddings at the 6-mer level [the-nucleotide-transformer-building-2024]. ← REV 3
- scBERT replaces standard positional embeddings with Gene2vec — pretrained gene-identity embeddings that encode functional similarity [scbert-as-a-large-2022]. ← REV 3
- ALiBi is best for RNA (top-1 on 7/13 BEACON tasks) and enables length extrapolation `[beacon-benchmark-for-comprehensive-2024, dnabert-2-efficient-foundation-2023]`.

**Recycling.**

- AlphaFold 2 uses 3-pass recycling where outputs are fed back as inputs; no recycling degrades accuracy by −3.1 GDT [highly-accurate-protein-structure-2021]. ← REV 3

**Attention-as-structure.**

- Transformer attention maps in protein LMs encode residue contacts: ESM-1b's attention beats GREMLIN on unsupervised contact prediction, with APC (average product correction) identified as critical for extracting this signal [transformer-protein-language-models-2021]. ← REV 3

### Optimization & Schedule

- ESM-2 used Adam with linear warmup + cosine decay, standard across most protein LMs [evolutionary-scale-prediction-of-2023].
- ProtTrans demonstrated that extending training duration is more important than increasing model width — T5-XL-U50 (3 B, trained longer on UniRef50) outperformed T5-XXL (11 B, standard schedule) on secondary structure prediction [prottrans-towards-cracking-the-2020]. ← REV 3
- ProteinBERT trained on a single GPU for 28 days, achieving competitive results at 16 M parameters — demonstrating that carefully designed small models can be practical alternatives when compute is limited [proteinbert-a-universal-deep]. ← REV 3
- HIPT showed that freezing pretrained ViTs prevents overfitting on the small labelled slide-level datasets typical of pathology, while end-to-end fine-tuning degrades performance [scaling-vision-transformers-to-2022]. ← REV 3
- CONCH requires unimodal pre-initialisation (separate image and text pretraining) before vision-language alignment for best results [towards-a-visual-language-2023]. ← REV 3

### Scaling & Compute Efficiency

**Protein sequence scaling laws.**

- ESM-2 established the clearest scaling law in biology: unsupervised contact prediction precision rises monotonically from 15.9 % (8 M params) to 54.5 % (15 B params), with no sign of saturation at 15 B.
  ESMFold (structure prediction from the 15 B LM) is 60× faster than AlphaFold 2 because it eliminates MSA search [evolutionary-scale-prediction-of-2023]. ← REV 3

**Training efficiency > model size.**

- ProtTrans showed T5-XL-U50 (3 B, trained longer) outperforms T5-XXL (11 B, standard schedule), and was the first PLM to match MSA-based secondary structure prediction without MSAs [prottrans-towards-cracking-the-2020]. ← REV 3

**Efficient small models.**

- NT v2-250 M matches v1-2.5 B at 10× fewer parameters through distillation and IA3 fine-tuning (0.1 % params) [the-nucleotide-transformer-building-2024]. ← REV 3
- ProteinBERT matches TAPE benchmarks at 16 M params (2.4× fewer than baselines) on a single GPU [proteinbert-a-universal-deep]. ← REV 3
- dnaGrinder (63.6M) matches both DNABERT-2 (117M) and NT-2500M (2.5B) at 40× fewer params `[dnagrinder-a-lightweight-and-2024]`.

**Pathology data scaling.**

- UNI demonstrates clear data-scaling: 100 M patches from 100 K slides produce an encoder that needs only 8 labelled examples to match competitors using 128, yielding 16× label efficiency [a-general-purpose-self-2023]. ← REV 3
- GigaPath trains on 1.3 B tiles with ViT-giant (1.13 B params), showing DINOv2 > SimCLR > MAE for self-supervised tile encoding [a-whole-slide-foundation]. ← REV 3

**scRNA compute.**

- scFoundation's xTrimoGene sparse encoder reduces FLOPs by 1–2 orders of magnitude vs dense attention, enabling pretraining on > 50 M cells and 19,264 genes without prohibitive cost [large-scale-foundation-model-2024]. ← REV 3
- scVI scaled to 1.3 M cells in < 2 h on a single GPU, at a time when competing methods could not exceed 100 K cells [a-deep-generative-model-2017]. ← REV 3

**Scaling saturation differences across modalities.**

- RNA FMs saturate at ~30–50M params `[character-level-tokenizations-as-2024]`.
- Pathology and microscopy FMs show log-linear scaling into billions `[vitally-consistent-scaling-biological-2024]`.
- Protein LMs show diminishing returns beyond ~1B for some tasks but not for contacts (ESM-2 unsaturated at 15B) [evolutionary-scale-prediction-of-2023]. ← REV 3

### MSA vs MSA-Free Structure Prediction ← REV 3

MSA-based methods (AlphaFold 2 [highly-accurate-protein-structure-2021], RoseTTAFold [accurate-prediction-of-protein-2021]) achieve the highest accuracy (median RMSD 0.96 Å on CASP14 for AF2) but require expensive database searches.
Three MSA-free alternatives have emerged:

| Method | PLM basis | Speed-up vs AF2 | CASP14-level accuracy |
|---|---|---|---|
| ESMFold [evolutionary-scale-prediction-of-2023] | ESM-2 15 B | 60× | TM ~0.90 (single seq) |
| OmegaFold [high-resolution-de-novo-2022] | 670 M GAU PLM | ~10× | TM ~0.93 |
| HelixFold-Single [helixfold-single-msa-free-2022] | 1.18 B DeBERTa PLM | 500× | Competitive |

MSA Transformer shows MSAs still add value when available: its tied row attention achieves 57.4 % long-range contacts vs 41.1 % for ESM-1b (single-sequence) at 6.5× fewer parameters [msa-transformer-2021].

The practical implication: use MSA-free methods for throughput-sensitive applications (screening, design) and MSA-based methods for high-accuracy single-target prediction. ← REV 3

### Distillation from AlphaFold Predictions ← REV 3

A recurring strategy is treating AlphaFold's predicted structures as pseudo-labelled training data:

- **Self-distillation (AF2→AF2):** AlphaFold 2 trains on ~350 K of its own high-confidence predictions, adding +1.8 GDT [highly-accurate-protein-structure-2021].
- **Inverse folding (AF2→ESM-IF):** Training ESM-IF on 12 M CATH-mapped AF2 structures gained +10 pp sequence recovery vs PDB-only (<40 K), with data scale dominating architecture [learning-inverse-folding-from-2022].
- **MSA-free folding (AF2→HelixFold-Single):** Distillation from ~1 M AF2 predictions bootstraps a PLM-only folding model, achieving 500× speed-up [helixfold-single-msa-free-2022].
- **Structure SSL (AF2→GearNet):** 805 K AlphaFold structures enable GearNet to match sequence models pretrained on orders-of-magnitude more sequence data [protein-representation-learning-by-2022].

This pattern suggests a general recipe: use the best available structure predictor to generate pseudo-labelled structures, then train lighter or differently-purposed models on those predictions. ← REV 3

### Evaluation & Benchmarking Caveats

**Benchmark provenance.**

- TAPE [evaluating-protein-transfer-learning-2019] established the first standardised protein representation benchmark (5 tasks, 3 architectures at 38 M params), finding that self-supervised pretraining is broadly beneficial but no single architecture dominates — and that alignment-derived features still beat learned features on structure tasks. ← REV 3

**Attention probing.**

- The attention-as-contacts paradigm [transformer-protein-language-models-2021] showed that protein LM attention maps encode residue–residue contacts, with ESM-1b beating GREMLIN.
  This spawned a sub-field of mechanistic interpretation but also raised concerns about circular reasoning when attention is both the evaluation metric and the training signal. ← REV 3

**Data contamination.**

- UNI acknowledges a TCGA contamination concern — many pathology benchmarks use TCGA data, which was also used for pretraining [a-general-purpose-self-2023]. ← REV 3
- Train/test leakage, benchmark saturation, and distribution shift collapse can invalidate entire model comparisons `[evaluating-computational-pathology-foundation-2024, systematic-evaluation-of-single-2026]`.

**Zero-shot as evaluation.**

- ESM-1v showed masked marginal scoring gives Spearman ρ ≈ 0.44 for variant-effect prediction without any labelled data [language-models-enable-zero-2021]. ← REV 3
- NT achieves competitive zero-shot variant scoring from 6-mer representations [the-nucleotide-transformer-building-2024]. ← REV 3
- This paradigm is increasingly used as an intrinsic evaluation of representation quality.

**Pathology evaluation hierarchy.**

- Patch-level accuracy does not predict slide-level diagnostic performance.
- CLAM showed that attention-based MIL with instance clustering (no slide-level labels for instances) achieves AUC > 0.95 on slide-level tasks [data-efficient-and-weakly-2020]. ← REV 3
- HIPT's hierarchical aggregation improved survival prediction AUC from 0.786 to 0.952 over flat attention [scaling-vision-transformers-to-2022]. ← REV 3

**Intermediate layer extraction.**

- Block search yields up to 60% improvement in biological recall for large models — final layers are often not the best for downstream extraction `[vitally-consistent-scaling-biological-2024]`.

---

## Modality-Specific Recipes

### DNA / Genomics

The DNA modality has evolved rapidly across three tokenization eras:

**DNABERT-1** (2021) pioneered the DNA-as-language paradigm using overlapping k-mers (k = 3–6) on human-only data, training an 86–89 M BERT model.
Retrospective analysis identified k-mer leakage (positional information bleed) as a limitation [dnabert-pre-trained-bidirectional-2021]. ← REV 3

**Nucleotide Transformer** (2024) scaled to multi-species data (850 genomes), used non-overlapping 6-mers, and produced a 50 M–2.5 B parameter family.
The distilled v2-250 M matches v1-2.5 B, and IA3 fine-tuning (0.1 % trainable params) matches full fine-tuning [the-nucleotide-transformer-building-2024]. ← REV 3

**DNABERT-2** moved to BPE tokenization, removing k-mer artefacts while matching NT-2500M at 117M params `[dnabert-2-efficient-foundation-2023]`.

**Evo** (2024) pushed to byte-level tokenization on a 7 B StripedHyena with 131 k context, trained on prokaryotic genomes.
It is the first LM to perform protein–RNA codesign in a single forward pass, and showed Transformer++ substantially underperforms the SSM hybrid at byte-level DNA [sequence-modeling-and-design-2024].

**Caduceus** introduced bidirectional Mamba (BiMamba) for reverse-complement equivariance `[caduceus-bi-directional-equivariant-2024]`.

**Recipe:** Start with DNABERT-2 or NT-v2 for standard regulatory-genomics tasks.
Use Evo for long-range prokaryotic or generative applications requiring > 100 k context.
Use Caduceus when RC equivariance is critical.

### DNA → Epigenome / Gene Expression

**Enformer** (2021) combined CNN stem + transformer to achieve 200 kb receptive fields, predicting 5,313 epigenomic tracks.
Gene expression correlation reached 0.85, closing roughly 1/3 of the gap to the 0.94 inter-individual ceiling.
Attention > dilated convolutions at all model sizes.
Custom relative positional encoding was critical [effective-gene-expression-prediction-2021]. ← REV 3

**Borzoi** (2023) extended to 524 kb input and 32 bp resolution via U-Net upsampling, adding RNA-seq coverage as a multi-task target.
eQTL AUROC improved from 0.747 (Enformer) to 0.794 [predicting-rna-seq-coverage-2023]. ← REV 3

**Recipe:** Use Borzoi when distal regulatory elements (enhancers > 200 kb away) or RNA-seq prediction at base-resolution are needed; Enformer remains a strong and lighter default.

### RNA

**RNA-FM** (2022) is a 99 M BERT trained on 23.7 M ncRNA sequences from RNAcentral.
It achieves F1 +3.6 over UFold on secondary structure prediction and eliminates the need for MSA computation on RNA tasks [interpretable-rna-foundation-model-2022]. ← REV 3

RNA-FM, Uni-RNA, and RiNALMo share the pattern of masked-nucleotide pretraining on non-coding RNAs.
Uni-RNA scales to ~1 B parameters; RiNALMo uses RoPE and achieves strong results on BEACON benchmarks.

**Recipe:** For ncRNA tasks (secondary structure, family classification), start with RNA-FM.
For broader RNA (including mRNA), consider Uni-RNA or RiNALMo at larger scale.

### Protein Sequence

The protein sequence modality has the deepest model lineage, spanning four generations:

**Generation 1 — Establishing the paradigm (2019–2020).**

- TAPE [evaluating-protein-transfer-learning-2019] benchmarked three architectures (LSTM, Transformer, ResNet) at 38 M params, finding self-supervised pretraining broadly beneficial but no single winner — and alignment features still dominated on structure tasks. ← REV 3
- ProtTrans [prottrans-towards-cracking-the-2020] scaled to 11 B (T5-XXL) on 393 B tokens using 5,616 GPUs, finding that training duration matters more than model width (T5-XL-U50 3 B > T5-XXL 11 B).
  ProtTrans was first to match MSA-based secondary structure prediction without MSAs. ← REV 3

**Generation 2 — ESM scaling (2021).**

- ESM-1b (650 M) established that internal representations linearly correlate with 3D structure (ECE), with diversity (UniRef50) outperforming quantity [biological-structure-and-function-2021]. ← REV 3
- ESM-1v specialised for variant-effect prediction on UniRef90, achieving zero-shot Spearman ρ ≈ 0.44 via masked marginal scoring [language-models-enable-zero-2021]. ← REV 3
- MSA Transformer (100 M) showed alignment-aware axial attention achieves 57.4 % long-range contacts at 6.5× fewer params than ESM-1b [msa-transformer-2021]. ← REV 3
- ProteinBERT demonstrated that compact dual-stream design (16 M params) with GO pretraining matches TAPE baselines on a single GPU [proteinbert-a-universal-deep]. ← REV 3
- Attention-as-contacts [transformer-protein-language-models-2021] showed ESM-1b attention maps encode residue contacts, beating GREMLIN unsupervised (APC correction critical). ← REV 3

**Generation 3 — Scaling to 15 B (2023).**

- ESM-2 [evolutionary-scale-prediction-of-2023] defined the scaling law: contact precision 15.9 % → 54.5 % (8 M → 15 B).
  ESMFold achieves 60× speed-up over AF2 without MSA. Still not saturated at 15 B.

**Generation 4 — Design (2022+).**

- ESM-design [language-models-generalize-beyond-2022] used frozen ESM-2 + MCMC for de novo design with 67 % experimental success (152/228), including 35 designs with no natural homologs. ← REV 3
- ProtGPT2 [protgpt2-is-a-deep] was the first decoder-only PLM for protein design (738 M GPT-2 on UniRef50), generating novel topologies at 87.6 % globularity using BPE tokenization (avg 4 aa/token). ← REV 3
- Ankh (encoder-decoder, 1.5B) uses partial de-masking and 2:1 encoder/decoder ratio for +3.9 pp improvement `[ankh-optimized-protein-language-2023]`.

**Recipe:** Use ESM-2 (650 M or 3 B) as the default sequence encoder.
For variant prediction, try ESM-1v zero-shot scoring first.
For high-throughput design, ESM-design or ProtGPT2.
For MSA-exploiting tasks with available alignments, MSA Transformer remains most parameter-efficient.

### Protein Structure

**AlphaFold 2** [highly-accurate-protein-structure-2021] achieved median RMSD 0.96 Å on CASP14, using Evoformer (48 blocks) + IPA structure module + 3-pass recycling.
Critical ablations: self-distillation on 350 K predictions (+1.8 GDT), FAPE loss (essential), recycling (+3.1 GDT). 93 M params. ← REV 3

**RoseTTAFold** [accurate-prediction-of-protein-2021] introduced the three-track (1D/2D/3D) architecture with SE(3)-equivariant layers.
The 3D track enables complex prediction from monomer training alone; discontinuous cropping improves accuracy. ← REV 3

**MSA-free alternatives** (see dedicated subsection above):

- OmegaFold [high-resolution-de-novo-2022] — 670 M, TM ~0.93, strong on orphan proteins/antibodies. ← REV 3
- HelixFold-Single [helixfold-single-msa-free-2022] — 1.18 B, 500× faster, PLM perplexity correlates with TM-score. ← REV 3
- ESMFold [evolutionary-scale-prediction-of-2023] — 60× faster, no MSA needed. ← REV 3

**Inverse folding.**

- ESM-IF [learning-inverse-folding-from-2022] (142 M GVP + Transformer) predicts sequences from structures.
  Training on 12 M AF2-predicted structures yields +10 pp recovery vs PDB-only. Data scale dominates architecture. ← REV 3

**Structure encoders.**

- GVP [learning-from-protein-structure-2020] introduced equivariant vector features (ppl 5.29 vs 6.55 Structured GNN). ← REV 3
- GearNet [protein-representation-learning-by-2022] with edge message passing on 805 K AF structures matches sequence models at orders-of-magnitude more data. ← REV 3

**Attention-as-contacts.**

- PLM attention maps encode residue contacts; ESM-1b surpasses GREMLIN unsupervised, with APC correction critical [transformer-protein-language-models-2021]. ← REV 3

**Recipe:** Use AlphaFold 2 (or AF3) for single high-accuracy predictions.
For throughput-sensitive screening, use ESMFold or OmegaFold.
For inverse folding / design, ESM-IF with AF2-predicted training structures.
For structure-aware representation learning, GearNet + AF structures is competitive and compute-efficient.

### Single-Cell RNA

The scRNA modality has seen rapid evolution from domain-specific probabilistic models to transformer-based foundation models:

**Probabilistic foundations (2017–2021).**

- scVI [a-deep-generative-model-2017] introduced VAE + ZINB likelihood for scRNA-seq, scaling to 1.3 M cells when competitors failed at 100 K. It founded the scvi-tools ecosystem. ← REV 3
- totalVI [joint-probabilistic-modeling-of-2021] extended to joint RNA + protein (CITE-seq) modelling via conditional VAE with NB mixture protein decoder. ← REV 3

**Transformer era (2022–2024).**

- scBERT [scbert-as-a-large-2022] (~10 M, Performer): genes as tokens, 5-bin expression discretization, Gene2vec positional embeddings, MLM on PanglaoDB. ← REV 3
- Geneformer [transfer-learning-enables-predictions-2023] (~10 M): rank-value encoding, AUC 0.91 for dosage sensitivity, in-silico perturbation on 30 M cells. ← REV 3
- scGPT [scgpt-toward-building-a-2024] (~51 M): 51-bin value discretization, generative masking, MVC/ECS/DAB fine-tuning, 33 M cells. ← REV 3
- scFoundation [large-scale-foundation-model-2024] (100 M, xTrimoGene): read-depth-aware pretraining, sparse encoder (1–2 OOM FLOP reduction), >50 M cells, 19,264 genes. ← REV 3

**Recipe:** For batch correction and integration, scVI/totalVI remain production-grade and interpretable.
For transfer learning (cell-type annotation, perturbation prediction), start with Geneformer or scGPT with fine-tuning.
For maximum scale and gene-level resolution, scFoundation's asymmetric architecture offers the best compute–quality trade-off.

### Computational Pathology

**Foundational baselines.**

- CLAM [data-efficient-and-weakly-2020] demonstrated attention-based MIL pooling + instance clustering on frozen ResNet50 features (~800 K trainable params), achieving AUC > 0.95.
  Not a foundation model per se, but the canonical MIL baseline against which all foundation models are compared. ← REV 3

**Hierarchical pretraining.**

- HIPT [scaling-vision-transformers-to-2022] introduced three-stage hierarchical ViT (256→4096→WSI) with DINO self-supervised pretraining on 10,678 TCGA WSIs.
  Hierarchical pretraining is critical: AUC 0.952 vs 0.786 without. Freezing pretrained features prevents overfitting. ← REV 3

**Tile-level foundation models.**

- UNI [a-general-purpose-self-2023] (ViT-L/16, 303 M, DINOv2) trained on 100 M patches from 100 K WSIs.
  Data-scaling laws: 8-shot UNI > 128-shot competitors (16× label efficiency). TCGA contamination concern. ← REV 3
- Virchow scales to ViT-H with 1.5 M+ slides.
- Phikon-v2 shows DINOv2 >> iBOT > DINO for pathology tile encoding `[phikon-v2-a-large-2024]`.

**Vision-language.**

- CONCH [towards-a-visual-language-2023] (~300 M, CoCa) trained on 1.17 M image–caption pairs.
  Enables zero-shot WSI classification (90 % NSCLC, 89.3 % RCC). Unimodal pre-initialisation critical. ← REV 3

**Slide-level encoding.**

- GigaPath [a-whole-slide-foundation] uses ViT-giant tiles (1.13 B) + LongNet slide encoder (86 M) on 1.3 B tiles from 171 K slides.
  DINOv2 > SimCLR > MAE for tiles; LongNet significantly outperforms ABMIL-only aggregation. ← REV 3

**Recipe:** Start with UNI or Virchow tile encoders (frozen) + attention MIL (CLAM-style) for standard classification.
For survival prediction or multi-resolution tasks, HIPT-style hierarchical aggregation.
For zero-shot or text-guided tasks, CONCH.
For whole-slide encoding at scale, GigaPath's LongNet.

### Cell Painting / High-Content Microscopy

This subfield primarily uses CNN or ViT encoders pretrained with contrastive or MAE objectives on cell images.
Models remain smaller (< 100 M) than pathology counterparts, reflecting smaller dataset sizes.
Domain-specific augmentations (channel dropout, illumination correction) are more important than architecture choice.
Sparse MoE for multi-channel microscopy cuts attention FLOPs by ~50% with only −1.7% accuracy `[sparse-mixture-of-experts-2025]`.

### Mass-Spectrometry Proteomics

Still early-stage for foundation models. Current approaches use task-specific architectures:
Casanovo (de novo sequencing), Prosit (spectrum prediction).
Transfer learning from protein sequence LMs (ESM-2 embeddings as features) is an emerging strategy but under-validated.

### Multimodal Medical

Models like BiomedCLIP, LLaVA-Med, and Med-PaLM M fuse radiology images with clinical text using CLIP-style contrastive pretraining or instruction tuning.
CONCH [towards-a-visual-language-2023] demonstrates this paradigm for histopathology specifically. ← REV 3
Data curation (quality of image–text pairs) dominates architecture choice.

### Small Molecules / SMILES

**ChemBERTa** [chemberta-large-scale-self-2020] (6-layer RoBERTa, ~83 M) pretrained on SMILES strings from PubChem.
Performance scaled with data (100 K→10 M compounds) but did not surpass graph-based D-MPNN, suggesting SMILES linearisation loses 3D structural information. ← REV 3

MolBERT, Uni-Mol, and 3D-aware approaches (using conformer ensembles as input) generally outperform SMILES-only models on property prediction.
Graph neural networks (SchNet, DimeNet++) remain competitive for 3D-dependent tasks.

**Recipe:** For property prediction, consider graph-based or 3D-aware methods over SMILES-only.
For generative chemistry (molecule design), SMILES-based autoregressive models remain popular.
ChemBERTa is a reasonable SMILES baseline.

---

## Open Problems

1. **Cross-modal transfer.**
   Can a genomic LM pretrained on DNA improve protein structure prediction, or vice versa?
   Evo's protein–RNA codesign [sequence-modeling-and-design-2024] and RoseTTAFold's 3D-track cross-prediction [accurate-prediction-of-protein-2021] are early evidence, but systematic benchmarking is lacking.

2. **Benchmark saturation and contamination.**
   TAPE [evaluating-protein-transfer-learning-2019] benchmarks are nearly saturated.
   UNI acknowledges TCGA contamination [a-general-purpose-self-2023].
   New benchmarks must be curated with strict temporal splits. ← REV 3

3. **Clinical validation.**
   Few bio-FMs have progressed from benchmark to clinical deployment.
   Pathology models (UNI, Virchow, GigaPath) are closest, but prospective studies are scarce.

4. **Tokenization convergence.**
   DNA tokenization has no consensus (k-mers → BPE → bytes);
   scRNA tokenization is even less settled (bins vs ranks vs raw).
   Systematic comparisons controlling for architecture and data are needed. ← REV 3

5. **Scaling ceilings.**
   ESM-2 is not saturated at 15 B [evolutionary-scale-prediction-of-2023], but Enformer's expression correlation plateaus at 0.85 vs a 0.94 ceiling [effective-gene-expression-prediction-2021].
   Understanding modality-specific scaling ceilings could redirect compute budgets. ← REV 3

6. **AlphaFold distillation limits.**
   Self-distillation and pseudo-labelling from AF2 predictions have become standard (AF2→AF2, AF2→ESM-IF, AF2→HelixFold-Single, AF2→GearNet), but error propagation and coverage biases in AF2's training distribution remain under-studied. ← REV 3

7. **Equivariance vs data augmentation.**
   GVP's built-in SE(3) equivariance [learning-from-protein-structure-2020] is elegant but hard to scale;
   data-augmented non-equivariant models sometimes match. The trade-off is unresolved.

8. **Privacy and data governance.**
   Patient-derived scRNA and pathology data face regulatory constraints that limit data pooling.
   Federated learning for bio-FMs is under-explored.

## Methodology & Limitations

This guidebook synthesises **85 fully extracted papers** selected via keyword search, citation tracking, and expert nomination.
REV 3 specifically added ~36 pre-2023 "anchor" papers (DNABERT-1, ESM-1b, AlphaFold 2, scVI, CLAM, TAPE, BioBERT, etc.) to correct a 2023-2026 recency bias in earlier revisions, ensuring foundational design decisions are properly attributed. ← REV 3

Coverage is uneven: protein sequence and structure are over-represented relative to RNA, metabolomics, and clinical integration.
Papers were extracted by a single annotator with spot-check verification; errors of omission or interpretation are possible.
Quantitative claims reflect the ablations reported in each paper and have not been independently reproduced.


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
