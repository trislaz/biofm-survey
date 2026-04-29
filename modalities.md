# Bio-FM Survey — Per-Modality Index

Total papers: **142**

Status breakdown:
- `extracted`: 82
- `converted`: 42
- `abstract-only`: 9
- `fetched`: 5
- `seed`: 4

## DNA (1 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2025 | [BioReason: Incentivizing Multimodal Biological Reasoning within a DNA-LLM Model](notes/bioreason-incentivizing-multimodal-biological-2025.md) | `extracted` | ~5B (Evo2-1B + Qwen3-4B; DNA encoder frozen, only LLM + projection trained) | — | multimodal, DNA-LLM, variant-effect-prediction, biological-reasoning |

## cell-profiling (1 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2025 | [CellPainTR: Generalizable Representation Learning for Cross-Dataset Cell Painting Analysis](notes/cellpaintr-generalizable-representation-learning-2025.md) | `extracted` | — | — | transformer, hyena-operator, cell-painting, batch-correction |

## dna (20 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Alignment or Integration? Rethinking Multimodal Fusion in DNA-language Foundation Models](notes/alignment-or-integration-rethinking-2026.md) | `converted` | — | — |  |
| 2026 | [How Private Are DNA Embeddings? Inverting Foundation Model Representations of Genomic Sequences](notes/how-private-are-dna-2026.md) | `seed` | — | — |  |
| 2026 | [JEPA-DNA: Grounding Genomic Foundation Models through Joint-Embedding Predictive Architectures](notes/jepa-dna-grounding-genomic-2026.md) | `extracted` | 117M | 7.6B bp | jepa, self-supervised, representation-learning, continual-pretraining |
| 2026 | [Poisoning the Genome: Targeted Backdoor Attacks on DNA Foundation Models](notes/poisoning-the-genome-targeted-2026.md) | `converted` | — | — |  |
| 2025 | [A Phylogenetic Approach to Genomic Language Modeling](notes/a-phylogenetic-approach-to-2025.md) | `extracted` | 83000000 | — | genomic-language-model, phylogenetics, variant-effect-prediction, convolutional |
| 2025 | [CodonMoE: DNA Language Models for mRNA Analyses](notes/codonmoe-dna-language-models-2025.md) | `extracted` | 7.5M (HyenaDNA+CodonMoE-pro); adapter adds 3.4–76.2M on top of backbone | — | mixture-of-experts, adapter, codon-level, cross-modality |
| 2025 | [DNABERT-2: Fine-Tuning a Genomic Language Model for Colorectal Gene Enhancer Classification](notes/dnabert-2-fine-tuning-2025.md) | `extracted` | 117M | — | fine-tuning, bpe, enhancer-classification, colorectal-cancer |
| 2025 | [Genome modeling and design across all domains of life with Evo 2](notes/genome-modeling-and-design-2025.md) | `abstract-only` | — | — |  |
| 2025 | [Human Genome Book: Words, Sentences and Paragraphs](notes/human-genome-book-words-2025.md) | `extracted` | 117M | — | genomics, language-transfer, cross-lingual, genome-segmentation |
| 2024 | [Caduceus: Bi-Directional Equivariant Long-Range DNA Sequence Modeling](notes/caduceus-bi-directional-equivariant-2024.md) | `extracted` | 1.9M (Caduceus-PS/Ph); range 470k–1.9M across configs | ~35B nucleotide tokens (HG38 human reference genome) | mamba, ssm, rc-equivariant, bidirectional |
| 2024 | [dnaGrinder: a lightweight and high-capacity genomic foundation model](notes/dnagrinder-a-lightweight-and-2024.md) | `extracted` | 63.6M | 69.5B | encoder-only, genomics, efficient, long-context |
| 2024 | [Efficient and Scalable Fine-Tune of Language Models for Genome Understanding](notes/efficient-and-scalable-fine-2024.md) | `converted` | — | — |  |
| 2024 | [PhyloGen: Language Model-Enhanced Phylogenetic Inference via Graph Structure Generation](notes/phylogen-language-model-enhanced-2024.md) | `extracted` | — | — | phylogenetics, variational-inference, graph-neural-network, tree-structure-generation |
| 2024 | [Recent advances in deep learning and language models for studying the microbiome](notes/recent-advances-in-deep-2024.md) | `converted` | — | — |  |
| 2024 | [Sequence modeling and design from molecular to genome scale with Evo](notes/sequence-modeling-and-design-2024.md) | `extracted` | 7B | 340B | StripedHyena, long-context, genome-scale, byte-level-tokenization |
| 2024 | [The Nucleotide Transformer: Building and Evaluating Robust Foundation Models for Human Genomics](notes/the-nucleotide-transformer-building-2024.md) | `extracted` | 50M/100M/250M/500M/2.5B | 50B–1T (model-dependent; v1-500M 50B, v1-2.5B 300B, v2-50M/100M 300B, v2-250M 800B, v2-500M 900B) | encoder-only, BERT, MLM, k-mer |
| 2024 | [VQDNA: Unleashing the Power of Vector Quantization for Multi-Species Genomic Sequence Modeling](notes/vqdna-unleashing-the-power-2024.md) | `extracted` | 103000000 | 262000000000 | tokenizer, vector-quantization, codebook-learning, genome-language-model |
| 2023 | [DNABERT-2: Efficient Foundation Model and Benchmark For Multi-Species Genome](notes/dnabert-2-efficient-foundation-2023.md) | `extracted` | 117000000 | 262000000000 | mlm, byte-pair-encoding, alibi, flash-attention |
| 2023 | [HyenaDNA: Long-Range Genomic Sequence Modeling at Single Nucleotide Resolution](notes/hyenadna-long-range-genomic-2023.md) | `extracted` | 6.6M (largest); suite from 0.44M to 6.6M | up to ~2T tokens (1M context × 10–20k steps) | hyena, long-context, single-nucleotide, implicit-convolution |
| 2021 | [DNABERT: pre-trained Bidirectional Encoder Representations from Transformers model for DNA-language in genome](notes/dnabert-pre-trained-bidirectional-2021.md) | `extracted` | 110000000 | 122000000000 | mlm, k-mer-tokenization, 6-mer, overlapping-k-mer |

## epigenome (8 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2025 | [A foundation model of transcription across human cell types](notes/a-foundation-model-of-2025.md) | `fetched` | — | — |  |
| 2025 | [CellVerse: Do Large Language Models Really Understand Cell Biology?](notes/cellverse-do-large-language-2025.md) | `extracted` | — | — | benchmark, single-cell, LLM-evaluation, cell-type-annotation |
| 2025 | [GRNFormer: A Biologically-Guided Framework for Integrating Gene Regulatory Networks into RNA Foundation Models](notes/grnformer-a-biologically-guided-2025.md) | `extracted` | — | — | gene-regulatory-network, adapter, graph-neural-network, cross-attention |
| 2025 | [Multimodal 3D Genome Pre-training](notes/multimodal-3d-genome-pre-2025.md) | `extracted` | — | — | foundation-model, 3d-genome, hi-c, chromatin |
| 2025 | [Multimodal Modeling of CRISPR-Cas12 Activity Using Foundation Models and Chromatin Accessibility Data](notes/multimodal-modeling-of-crispr-2025.md) | `extracted` | — | — | crispr, cas12, gRNA-activity-prediction, transfer-learning |
| 2024 | [Transformer-based Single-Cell Language Model: A Survey](notes/transformer-based-single-cell-2024.md) | `extracted` | — | — | survey, transformer, single-cell, foundation-model |
| 2023 | [Predicting RNA-seq coverage from DNA sequence as a unifying model of gene regulation](notes/predicting-rna-seq-coverage-2023.md) | `extracted` | ~250M (full model; not explicitly stated — comparable to Enformer; ablation mini models ~30M) | ~10K coverage tracks (7,611 human + 2,608 mouse) × tiled 524 kb genome windows | RNA-seq, long-context, multi-task, genomics |
| 2021 | [Effective gene expression prediction from sequence by integrating long-range interactions](notes/effective-gene-expression-prediction-2021.md) | `extracted` | 249000000 | — | transformer, self-attention, long-range-interactions, relative-positional-encoding |

## imaging-cell (2 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2025 | [CellPainTR: Generalizable Representation Learning for Cross-Dataset Cell Painting Analysis](notes/cellpaintr-generalizable-representation-learning-2025.md) | `extracted` | — | — | transformer, hyena-operator, cell-painting, batch-correction |
| 2025 | [Sparse Mixture-of-Experts for Multi-Channel Imaging: Are All Channel Interactions Required?](notes/sparse-mixture-of-experts-2025.md) | `extracted` | ~22M | — | mixture-of-experts, vision-transformer, multi-channel-imaging, sparse-attention |

## imaging-microscopy (6 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Elucidating the Design Space of Flow Matching for Cellular Microscopy](notes/elucidating-the-design-space-2026.md) | `extracted` | 700M | — | ablation-study, flow-matching, generative-model, cell-microscopy |
| 2026 | [Revisiting foundation models for cell instance segmentation](notes/revisiting-foundation-models-for-2026.md) | `extracted` | — | — | benchmark, instance-segmentation, cell-segmentation, SAM |
| 2025 | [SAM$^{*}$: Task-Adaptive SAM with Physics-Guided Rewards](notes/sam-task-adaptive-sam-2025.md) | `converted` | — | — |  |
| 2025 | [Segment Anything for Cell Tracking](notes/segment-anything-for-cell-2025.md) | `converted` | — | — |  |
| 2025 | [Sparse Mixture-of-Experts for Multi-Channel Imaging: Are All Channel Interactions Required?](notes/sparse-mixture-of-experts-2025.md) | `extracted` | ~22M | — | mixture-of-experts, vision-transformer, multi-channel-imaging, sparse-attention |
| 2024 | [ViTally Consistent: Scaling Biological Representation Learning for Cell Microscopy](notes/vitally-consistent-scaling-biological-2024.md) | `extracted` | 1.9B (MAE-G/8); 307M (MAE-L/8); 25M (CA-MAE-S/16) | >8B image crops (MAE-G/8, 500 epochs over 16M images) | scaling-laws, vision-transformer, masked-autoencoder, cell-microscopy |

## imaging-pathology (19 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Enabling clinical use of foundation models in histopathology](notes/enabling-clinical-use-of-2026.md) | `converted` | — | — |  |
| 2026 | [Revisiting foundation models for cell instance segmentation](notes/revisiting-foundation-models-for-2026.md) | `extracted` | — | — | benchmark, instance-segmentation, cell-segmentation, SAM |
| 2025 | [Reusable specimen-level inference in computational pathology](notes/reusable-specimen-level-inference-2025.md) | `converted` | — | — |  |
| 2025 | [Uni-Parser Technical Report](notes/uni-parser-technical-report-2025.md) | `converted` | — | — |  |
| 2025 | [Unifying Multiple Foundation Models for Advanced Computational Pathology](notes/unifying-multiple-foundation-models-2025.md) | `converted` | — | — |  |
| 2024 | [A visual-language foundation model for computational pathology (CONCH)](notes/a-visual-language-foundation-2024.md) | `fetched` | — | — |  |
| 2024 | [A whole-slide foundation model for digital pathology from real-world data](notes/a-whole-slide-foundation.md) | `extracted` | ~1.13B tile encoder (ViT-giant, 1536-d) + ~86M slide encoder (LongNet 12L 768d); small variant 23M | 1.3B image tiles (tile SSL) + 171k slides × 30 epochs (slide SSL) | foundation-model, self-supervised, DINOv2, LongNet |
| 2024 | [Evaluating Computational Pathology Foundation Models for Prostate Cancer Grading under Distribution Shifts](notes/evaluating-computational-pathology-foundation-2024.md) | `extracted` | — | — | evaluation, robustness, distribution-shift, prostate-cancer |
| 2024 | [Knowledge-enhanced Pretraining for Vision-language Pathology Foundation Model on Cancer Diagnosis](notes/knowledge-enhanced-pretraining-for-2024.md) | `extracted` | — | — | vision-language, knowledge-graph, contrastive-learning, zero-shot |
| 2024 | [MedMax: Mixed-Modal Instruction Tuning for Training Biomedical Assistants](notes/medmax-mixed-modal-instruction-2024.md) | `extracted` | 7000000000 | 1700000000 | instruction-tuning, mixed-modal, lora, dataset |
| 2024 | [Phikon-v2, A large and public feature extractor for biomarker prediction](notes/phikon-v2-a-large-2024.md) | `extracted` | 307M | 456M tiles (400M seen at released ckpt) | self-supervised-learning, DINOv2, pathology-foundation-model, ViT-L |
| 2024 | [RudolfV: A Foundation Model by Pathologists for Pathologists](notes/rudolfv-a-foundation-model-2024.md) | `extracted` | 304M | — | pathology-fm, dinov2, self-supervised, vit |
| 2024 | [Towards Large-Scale Training of Pathology Foundation Models](notes/towards-large-scale-training-2024.md) | `converted` | — | — |  |
| 2024 | [uniGradICON: A Foundation Model for Medical Image Registration](notes/unigradicon-a-foundation-model-2024.md) | `converted` | — | — |  |
| 2023 | [A General-Purpose Self-Supervised Model for Computational Pathology](notes/a-general-purpose-self-2023.md) | `extracted` | 303000000 | 100130900 | vision-transformer, DINOv2, self-supervised, computational-pathology |
| 2023 | [Towards a Visual-Language Foundation Model for Computational Pathology](notes/towards-a-visual-language-2023.md) | `extracted` | ~ViT-B/16 image encoder (~86M) + 12-layer text encoder + 12-layer multimodal decoder (768-d, 3072 hidden); total estimated ~300M | 1.17M image-caption pairs (human-only), 40 epochs; unimodal image pretrain on 16M tiles, 80 epochs; unimodal text pretrain on ~1M pathology texts, 15k steps | CoCa, contrastive-VL, path-text-pairs, vision-language |
| 2023 | [Virchow: A Million-Slide Digital Pathology Foundation Model](notes/virchow-a-million-slide-2023.md) | `extracted` | 632000000 | — | foundation-model, self-supervised, DINOv2, ViT-H |
| 2023 | [XrayGPT: Chest Radiographs Summarization using Medical Vision-Language Models](notes/xraygpt-chest-radiographs-summarization-2023.md) | `converted` | — | — |  |
| 2022 | [Scaling Vision Transformers to Gigapixel Images via Hierarchical Self-Supervised Learning](notes/scaling-vision-transformers-to-2022.md) | `extracted` | <10M total; 505k trainable at fine-tune (ViT_WSI-4096 only) | 104M 256×256 patches (Stage 1) + 408k 4096×4096 regions (Stage 2) | foundation-model, self-supervised, DINO, hierarchical |

## imaging-radiology (6 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [EvalBlocks: A Modular Pipeline for Rapidly Evaluating Foundation Models in Medical Imaging](notes/evalblocks-a-modular-pipeline-2026.md) | `converted` | — | — |  |
| 2024 | [A Survey on Trustworthiness in Foundation Models for Medical Image Analysis](notes/a-survey-on-trustworthiness-2024.md) | `converted` | — | — |  |
| 2024 | [FedFMS: Exploring Federated Foundation Models for Medical Image Segmentation](notes/fedfms-exploring-federated-foundation-2024.md) | `converted` | — | — |  |
| 2024 | [MedDiff-FM: A Diffusion-based Foundation Model for Versatile Medical Image Applications](notes/meddiff-fm-a-diffusion-2024.md) | `extracted` | — | — | diffusion-model, 3d-ct, foundation-model, controlnet |
| 2024 | [MedMax: Mixed-Modal Instruction Tuning for Training Biomedical Assistants](notes/medmax-mixed-modal-instruction-2024.md) | `extracted` | 7000000000 | 1700000000 | instruction-tuning, mixed-modal, lora, dataset |
| 2023 | [Empirical Analysis of a Segmentation Foundation Model in Prostate Imaging](notes/empirical-analysis-of-a-2023.md) | `converted` | — | — |  |

## interactome (4 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Multi-Dimensional Spectral Geometry of Biological Knowledge in Single-Cell Transformer Representations](notes/multi-dimensional-spectral-geometry-2026.md) | `converted` | — | — |  |
| 2026 | [Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals Attention Captures Co-Expression Rather Than Unique Regulatory Signal](notes/systematic-evaluation-of-single-2026.md) | `extracted` | — | — | evaluation-framework, interpretability, attention-analysis, gene-regulatory-network |
| 2025 | [GRNFormer: A Biologically-Guided Framework for Integrating Gene Regulatory Networks into RNA Foundation Models](notes/grnformer-a-biologically-guided-2025.md) | `extracted` | — | — | gene-regulatory-network, adapter, graph-neural-network, cross-attention |
| 2025 | [Multimodal 3D Genome Pre-training](notes/multimodal-3d-genome-pre-2025.md) | `extracted` | — | — | foundation-model, 3d-genome, hi-c, chromatin |

## language (1 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2023 | [BiomedCLIP: a multimodal biomedical foundation model pretrained from fifteen million scientific image-text pairs](notes/biomedclip-a-multimodal-biomedical-2023.md) | `extracted` | ~86M vision + ~110M text (ViT-B/16 + PubMedBERT) | 15M image-text pairs (PMC-15M), 32 epochs | contrastive-learning, CLIP, biomedical-vision-language, domain-adaptation |

## multimodal (13 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Differential Attention-Augmented BiomedCLIP with Asymmetric Focal Optimization for Imbalanced Multi-Label Video Capsule Endoscopy Classification](notes/differential-attention-augmented-biomedclip-2026.md) | `converted` | — | — |  |
| 2025 | [An Explainable Biomedical Foundation Model via Large-Scale Concept-Enhanced Vision-Language Pre-training](notes/an-explainable-biomedical-foundation-2025.md) | `converted` | — | — |  |
| 2025 | [Cell2Text: Multimodal LLM for Generating Single-Cell Descriptions from RNA-Seq Data](notes/cell2text-multimodal-llm-for-2025.md) | `extracted` | ~1.3B (Llama-1B variant) / ~4.3B (Gemma-4B variant); encoder Geneformer-V2-316M frozen | — | scRNA-seq, multimodal-generation, cell-annotation, geneformer |
| 2025 | [Doctor Sun: A Bilingual Multimodal Large Language Model for Biomedical AI](notes/doctor-sun-a-bilingual-2025.md) | `converted` | — | — |  |
| 2025 | [Interpreting Biomedical VLMs on High-Imbalance Out-of-Distributions: An Insight into BiomedCLIP on Radiology](notes/interpreting-biomedical-vlms-on-2025.md) | `converted` | — | — |  |
| 2024 | [A Multimodal Approach For Endoscopic VCE Image Classification Using BiomedCLIP-PubMedBERT](notes/a-multimodal-approach-for-2024.md) | `converted` | — | — |  |
| 2024 | [AIDO: Accurate model of biology through a foundation model of DNA, RNA and protein](notes/aido-accurate-model-of-2024.md) | `abstract-only` | — | — |  |
| 2024 | [MedMax: Mixed-Modal Instruction Tuning for Training Biomedical Assistants](notes/medmax-mixed-modal-instruction-2024.md) | `extracted` | 7000000000 | 1700000000 | instruction-tuning, mixed-modal, lora, dataset |
| 2024 | [ProtCLIP: Function-Informed Protein Multi-Modal Learning](notes/protclip-function-informed-protein-2024.md) | `extracted` | — | — | contrastive-learning, protein-text-alignment, function-prediction, segment-wise-objectives |
| 2023 | [BiomedCLIP: a multimodal biomedical foundation model pretrained from fifteen million scientific image-text pairs](notes/biomedclip-a-multimodal-biomedical-2023.md) | `extracted` | ~86M vision + ~110M text (ViT-B/16 + PubMedBERT) | 15M image-text pairs (PMC-15M), 32 epochs | contrastive-learning, CLIP, biomedical-vision-language, domain-adaptation |
| 2023 | [LLaVA-Med: Training a Large Language-and-Vision Assistant for Biomedicine in One Day](notes/llava-med-training-a-2023.md) | `converted` | — | — |  |
| 2023 | [MolFM: A Multimodal Molecular Foundation Model](notes/molfm-a-multimodal-molecular-2023.md) | `extracted` | ~138M total (structure 1.8M + text 61.8M + KG 12.6M + multimodal encoder 61.8M) | — | knowledge-graph, contrastive-learning, cross-modal-retrieval, molecule-captioning |
| 2023 | [Towards a Visual-Language Foundation Model for Computational Pathology](notes/towards-a-visual-language-2023.md) | `extracted` | ~ViT-B/16 image encoder (~86M) + 12-layer text encoder + 12-layer multimodal decoder (768-d, 3072 hidden); total estimated ~300M | 1.17M image-caption pairs (human-only), 40 epochs; unimodal image pretrain on 16M tiles, 80 epochs; unimodal text pretrain on ~1M pathology texts, 15k steps | CoCa, contrastive-VL, path-text-pairs, vision-language |

## multispecies-alignment (1 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2025 | [A Phylogenetic Approach to Genomic Language Modeling](notes/a-phylogenetic-approach-to-2025.md) | `extracted` | 83000000 | — | genomic-language-model, phylogenetics, variant-effect-prediction, convolutional |

## other (2 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2024 | [Virchow2: Scaling Self-Supervised Mixed Magnification Models in Pathology](notes/virchow2-scaling-self-supervised-2024.md) | `converted` | — | — |  |
| 2022 | [BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation and Mining](notes/biogpt-generative-pre-trained-2022.md) | `extracted` | 347000000 | 104900000000 | autoregressive, byte-pair, soft-prompt, causal-lm |

## protein-sequence (26 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2025 | [Boosting In-Silicon Directed Evolution with Fine-Tuned Protein Language Model and Tree Search](notes/boosting-in-silicon-directed-2025.md) | `converted` | — | — |  |
| 2025 | [Human Genome Book: Words, Sentences and Paragraphs](notes/human-genome-book-words-2025.md) | `extracted` | 117M | — | genomics, language-transfer, cross-lingual, genome-segmentation |
| 2025 | [InstructPLM-mu: 1-Hour Fine-Tuning of ESM2 Beats ESM3 in Protein Mutation Predictions](notes/instructplm-mu-1-hour-2025.md) | `extracted` | 35M / 150M / 650M (ESM2 backbone scales) | — | protein-mutation-prediction, fine-tuning, multimodal-fusion, parameter-efficient |
| 2024 | [Endowing Protein Language Models with Structural Knowledge](notes/endowing-protein-language-models-2024.md) | `extracted` | 1137M (650M-base PST; 486M trainable structure extractors). Also 8M/35M/150M base variants. | 542K protein structures (AlphaFold SwissProt subset) | structure-aware, graph-transformer, parameter-efficient, ESM-2 |
| 2024 | [Enhancing the efficiency of protein language models with minimal wet-lab data through few-shot learning](notes/enhancing-the-efficiency-of-2024.md) | `converted` | — | — |  |
| 2024 | [ESM All-Atom: Multi-scale Protein Language Model for Unified Molecular Modeling](notes/esm-all-atom-multi-2024.md) | `extracted` | 35M | — | multi-scale, code-switching, unified-molecular-modeling, protein-molecule-interaction |
| 2024 | [ProtCLIP: Function-Informed Protein Multi-Modal Learning](notes/protclip-function-informed-protein-2024.md) | `extracted` | — | — | contrastive-learning, protein-text-alignment, function-prediction, segment-wise-objectives |
| 2024 | [Sequence modeling and design from molecular to genome scale with Evo](notes/sequence-modeling-and-design-2024.md) | `extracted` | 7B | 340B | StripedHyena, long-context, genome-scale, byte-level-tokenization |
| 2024 | [Simulating 500 million years of evolution with a language model (ESM-3)](notes/simulating-500-million-years-2024.md) | `abstract-only` | — | — |  |
| 2024 | [Structure-Informed Protein Language Model](notes/structure-informed-protein-language-2024.md) | `extracted` | 650M | — | protein-language-model, fine-tuning, remote-homology, knowledge-distillation |
| 2023 | [Ankh: Optimized Protein Language Model Unlocks General-Purpose Modelling](notes/ankh-optimized-protein-language-2023.md) | `extracted` | — | 14000000000 | encoder-decoder, T5-architecture, protein-language-model, masking-ablation |
| 2023 | [Evolutionary-scale prediction of atomic-level protein structure with a language model (ESM-2 / ESMFold)](notes/evolutionary-scale-prediction-of-2023.md) | `extracted` | 8M/35M/150M/650M/3B/15B | 65000000000 | scaling-laws, MLM, atomic-structure, protein-language-model |
| 2022 | [HelixFold-Single: MSA-free Protein Structure Prediction by Using Protein Language Model as an Alternative](notes/helixfold-single-msa-free-2022.md) | `extracted` | 1180000000.0 | — | MSA-free, distillation, protein-language-model, DeBERTa |
| 2022 | [High-resolution de novo structure prediction from primary sequence](notes/high-resolution-de-novo-2022.md) | `extracted` | 670000000 | — | MSA-free, PLM, protein-language-model, single-sequence-structure-prediction |
| 2022 | [Language models generalize beyond natural proteins (ESM design / Verkuil et al. 2022)](notes/language-models-generalize-beyond-2022.md) | `extracted` | 650M (ESM-2 backbone used for design) | 65000000000 | de-novo-design, inverse-folding, fixed-backbone-design, free-generation |
| 2022 | [Learning inverse folding from millions of predicted structures (ESM-IF1, Hsu 2022 ICML)](notes/learning-inverse-folding-from-2022.md) | `extracted` | 142M | — | inverse-folding, distillation, AlphaFold-data, GVP |
| 2022 | [ProteinBERT: a universal deep-learning model of protein sequence and function](notes/proteinbert-a-universal-deep.md) | `extracted` | 16M | — | local-global-architecture, GO-term-prediction, protein-function-prediction, denoising-autoencoder |
| 2022 | [ProtGPT2 is a deep unsupervised language model for protein design](notes/protgpt2-is-a-deep.md) | `extracted` | 738M | not-reported | autoregressive, generative, de-novo, protein-design |
| 2022 | [Robust deep learning-based protein sequence design using ProteinMPNN](notes/robust-deep-learning-based-2022.md) | `fetched` | — | — |  |
| 2021 | [Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences](notes/biological-structure-and-function-2021.md) | `extracted` | 650000000 | 86000000000 | protein-language-model, transformer, masked-language-modeling, unsupervised-representation-learning |
| 2021 | [Language models enable zero-shot prediction of the effects of mutations on protein function (ESM-1v, Meier 2021 NeurIPS)](notes/language-models-enable-zero-2021.md) | `extracted` | 650000000 | 9600000000 | protein-language-model, transformer, masked-language-modeling, zero-shot |
| 2021 | [MSA Transformer](notes/msa-transformer-2021.md) | `extracted` | 100M | — | MSA, axial-attention, tied-row-attention, contact-prediction |
| 2021 | [Transformer protein language models are unsupervised structure learners](notes/transformer-protein-language-models-2021.md) | `extracted` | — | — | attention-as-contact, probing, unsupervised, protein-language-model |
| 2020 | [ProGen: Language Modeling for Protein Generation](notes/progen-language-modeling-for-2020.md) | `extracted` | 1.2B | — | protein-generation, conditional-language-model, autoregressive-transformer, controllable-generation |
| 2020 | [ProtTrans: Towards Cracking the Language of Life's Code Through Self-Supervised Deep Learning and High Performance Computing](notes/prottrans-towards-cracking-the-2020.md) | `extracted` | up to 11B (ProtT5-XXL); ProtT5-XL 3B; ProtBert/ProtXLNet/ProtAlbert ~40M; ProtTXL-BFD 562M; ProtElectra 420M | up to 393B amino-acid tokens (BFD); UniRef100 88B; UniRef50 14B | arch-comparison, scaling, T5-XL, BERT |
| 2019 | [Evaluating Protein Transfer Learning with TAPE](notes/evaluating-protein-transfer-learning-2019.md) | `extracted` | ~38M (each of Transformer, LSTM, ResNet matched to ~38M) | ~32M protein domain sequences (Pfam) | benchmark, transfer-learning, protein-representation, self-supervised |

## protein-structure (21 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Mechanisms of AI Protein Folding in ESMFold](notes/mechanisms-of-ai-protein-2026.md) | `converted` | — | — |  |
| 2025 | [InstructPLM-mu: 1-Hour Fine-Tuning of ESM2 Beats ESM3 in Protein Mutation Predictions](notes/instructplm-mu-1-hour-2025.md) | `extracted` | 35M / 150M / 650M (ESM2 backbone scales) | — | protein-mutation-prediction, fine-tuning, multimodal-fusion, parameter-efficient |
| 2025 | [Inverse problems with experiment-guided AlphaFold](notes/inverse-problems-with-experiment-2025.md) | `converted` | — | — |  |
| 2025 | [Precision Design of Cyclic Peptides using AlphaFold](notes/precision-design-of-cyclic-2025.md) | `converted` | — | — |  |
| 2025 | [Quantifying the Role of OpenFold Components in Protein Structure Prediction](notes/quantifying-the-role-of-2025.md) | `converted` | — | — |  |
| 2024 | [Accurate structure prediction of biomolecular interactions with AlphaFold 3](notes/accurate-structure-prediction-of-2024.md) | `fetched` | — | — |  |
| 2024 | [AlphaFold two years on: validation and impact](notes/alphafold-two-years-on-2024.md) | `converted` | — | — |  |
| 2024 | [Endowing Protein Language Models with Structural Knowledge](notes/endowing-protein-language-models-2024.md) | `extracted` | 1137M (650M-base PST; 486M trainable structure extractors). Also 8M/35M/150M base variants. | 542K protein structures (AlphaFold SwissProt subset) | structure-aware, graph-transformer, parameter-efficient, ESM-2 |
| 2024 | [ESM All-Atom: Multi-scale Protein Language Model for Unified Molecular Modeling](notes/esm-all-atom-multi-2024.md) | `extracted` | 35M | — | multi-scale, code-switching, unified-molecular-modeling, protein-molecule-interaction |
| 2024 | [Generalized biomolecular modeling and design with RoseTTAFold All-Atom](notes/generalized-biomolecular-modeling-and-2024.md) | `abstract-only` | — | — |  |
| 2023 | [Evolutionary-scale prediction of atomic-level protein structure with a language model (ESM-2 / ESMFold)](notes/evolutionary-scale-prediction-of-2023.md) | `extracted` | 8M/35M/150M/650M/3B/15B | 65000000000 | scaling-laws, MLM, atomic-structure, protein-language-model |
| 2022 | [AlphaFold Distillation for Protein Design](notes/alphafold-distillation-for-protein-2022.md) | `converted` | — | — |  |
| 2022 | [HelixFold-Single: MSA-free Protein Structure Prediction by Using Protein Language Model as an Alternative](notes/helixfold-single-msa-free-2022.md) | `extracted` | 1180000000.0 | — | MSA-free, distillation, protein-language-model, DeBERTa |
| 2022 | [High-resolution de novo structure prediction from primary sequence](notes/high-resolution-de-novo-2022.md) | `extracted` | 670000000 | — | MSA-free, PLM, protein-language-model, single-sequence-structure-prediction |
| 2022 | [Learning inverse folding from millions of predicted structures (ESM-IF1, Hsu 2022 ICML)](notes/learning-inverse-folding-from-2022.md) | `extracted` | 142M | — | inverse-folding, distillation, AlphaFold-data, GVP |
| 2022 | [Protein Representation Learning by Geometric Structure Pretraining](notes/protein-representation-learning-by-2022.md) | `extracted` | 42000000 | — | SSL, contrastive, distance, angle-prediction |
| 2021 | [Accurate prediction of protein structures and interactions using a three-track neural network](notes/accurate-prediction-of-protein-2021.md) | `extracted` | — | — | protein-structure-prediction, three-track-network, SE3-equivariant, attention |
| 2021 | [Highly accurate protein structure prediction with AlphaFold](notes/highly-accurate-protein-structure-2021.md) | `extracted` | ~93M | — | evoformer, invariant-point-attention, recycling, MSA |
| 2021 | [MSA Transformer](notes/msa-transformer-2021.md) | `extracted` | 100M | — | MSA, axial-attention, tied-row-attention, contact-prediction |
| 2021 | [Transformer protein language models are unsupervised structure learners](notes/transformer-protein-language-models-2021.md) | `extracted` | — | — | attention-as-contact, probing, unsupervised, protein-language-model |
| 2020 | [Learning from Protein Structure with Geometric Vector Perceptrons](notes/learning-from-protein-structure-2020.md) | `extracted` | — | — | GNN, equivariant, geometric, message-passing |

## proteomics (1 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [SpecBridge: Bridging Mass Spectrometry and Molecular Representations via Cross-Modal Alignment](notes/specbridge-bridging-mass-spectrometry-2026.md) | `seed` | — | — |  |

## rna (11 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Orthrus: toward evolutionary and functional RNA foundation models](notes/orthrus-toward-evolutionary-and-2026.md) | `extracted` | 10.1M | — | contrastive-learning, mamba, ssm, mature-rna |
| 2025 | [CodonMoE: DNA Language Models for mRNA Analyses](notes/codonmoe-dna-language-models-2025.md) | `extracted` | 7.5M (HyenaDNA+CodonMoE-pro); adapter adds 3.4–76.2M on top of backbone | — | mixture-of-experts, adapter, codon-level, cross-modality |
| 2025 | [Multimodal Modeling of CRISPR-Cas12 Activity Using Foundation Models and Chromatin Accessibility Data](notes/multimodal-modeling-of-crispr-2025.md) | `extracted` | — | — | crispr, cas12, gRNA-activity-prediction, transfer-learning |
| 2025 | [SAE-RNA: A Sparse Autoencoder Model for Interpreting RNA Language Model Representations](notes/sae-rna-a-sparse-2025.md) | `converted` | — | — |  |
| 2024 | [BEACON: Benchmark for Comprehensive RNA Tasks and Language Models](notes/beacon-benchmark-for-comprehensive-2024.md) | `extracted` | — | — | benchmark, rna-language-model, tokenization, positional-encoding |
| 2024 | [Character-level Tokenizations as Powerful Inductive Biases for RNA Foundational Models](notes/character-level-tokenizations-as-2024.md) | `extracted` | 8M / 33M / 50M / 100M / 150M / 650M (suite) | ~31M ncRNA seqs from RNAcentral (~5.1B tokens); extended +31M coding seqs from RefSeq (~62M seqs total). Scaling expts: 2.4B–24.8B tokens. | tokenization, character-level, GBST, learnable-tokenization |
| 2024 | [RiNALMo: General-Purpose RNA Language Models Can Generalize Well on Structure Prediction Tasks](notes/rinalmo-general-purpose-rna-2024.md) | `extracted` | 650M | — | rna-language-model, masked-language-modeling, secondary-structure, generalization |
| 2024 | [Sequence modeling and design from molecular to genome scale with Evo](notes/sequence-modeling-and-design-2024.md) | `extracted` | 7B | 340B | StripedHyena, long-context, genome-scale, byte-level-tokenization |
| 2023 | [Predicting RNA-seq coverage from DNA sequence as a unifying model of gene regulation](notes/predicting-rna-seq-coverage-2023.md) | `extracted` | ~250M (full model; not explicitly stated — comparable to Enformer; ablation mini models ~30M) | ~10K coverage tracks (7,611 human + 2,608 mouse) × tiled 524 kb genome windows | RNA-seq, long-context, multi-task, genomics |
| 2022 | [Accurate RNA 3D structure prediction using a language model-based deep learning approach](notes/accurate-rna-3d-structure-2022.md) | `extracted` | — | ~23.7M sequences (RNA-FM pre-training) | rna-structure-prediction, foundation-model, language-model, alphafold-inspired |
| 2022 | [Interpretable RNA Foundation Model from Unannotated Data for Highly Accurate RNA Structure and Function Predictions](notes/interpretable-rna-foundation-model-2022.md) | `extracted` | ~99M (12-layer BERT, 640 hidden, 20 heads; not explicitly stated, estimated from architecture) | 23.7M ncRNA sequences from RNAcentral | foundation-model, rna, bert, masked-language-modeling |

## scrna (21 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Open World Knowledge Aided Single-Cell Foundation Model with Robust Cross-Modal Cell-Language Pre-training](notes/open-world-knowledge-aided-2026.md) | `seed` | — | — |  |
| 2026 | [Sparse autoencoders reveal organized biological knowledge but minimal regulatory logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT](notes/sparse-autoencoders-reveal-organized-2026.md) | `converted` | — | — |  |
| 2026 | [Systematic Evaluation of Single-Cell Foundation Model Interpretability Reveals Attention Captures Co-Expression Rather Than Unique Regulatory Signal](notes/systematic-evaluation-of-single-2026.md) | `extracted` | — | — | evaluation-framework, interpretability, attention-analysis, gene-regulatory-network |
| 2025 | [Cell2Text: Multimodal LLM for Generating Single-Cell Descriptions from RNA-Seq Data](notes/cell2text-multimodal-llm-for-2025.md) | `extracted` | ~1.3B (Llama-1B variant) / ~4.3B (Gemma-4B variant); encoder Geneformer-V2-316M frozen | — | scRNA-seq, multimodal-generation, cell-annotation, geneformer |
| 2025 | [CellVerse: Do Large Language Models Really Understand Cell Biology?](notes/cellverse-do-large-language-2025.md) | `extracted` | — | — | benchmark, single-cell, LLM-evaluation, cell-type-annotation |
| 2025 | [GRNFormer: A Biologically-Guided Framework for Integrating Gene Regulatory Networks into RNA Foundation Models](notes/grnformer-a-biologically-guided-2025.md) | `extracted` | — | — | gene-regulatory-network, adapter, graph-neural-network, cross-attention |
| 2025 | [scDrugMap: Benchmarking Large Foundation Models for Drug Response Prediction](notes/scdrugmap-benchmarking-large-foundation-2025.md) | `converted` | — | — |  |
| 2025 | [scMamba: A Scalable Foundation Model for Single-Cell Multi-Omics Integration Beyond Highly Variable Feature Selection](notes/scmamba-a-scalable-foundation-2025.md) | `extracted` | — | — | mamba, ssm, state-space-duality, contrastive-learning |
| 2025 | [Towards Applying Large Language Models to Complement Single-Cell Foundation Models](notes/towards-applying-large-language-2025.md) | `converted` | — | — |  |
| 2024 | [Large-scale foundation model on single-cell transcriptomics](notes/large-scale-foundation-model-2024.md) | `extracted` | 100000000 | — | foundation-model, single-cell, scRNA-seq, asymmetric-encoder-decoder |
| 2024 | [Nicheformer: a foundation model for single-cell and spatial omics](notes/nicheformer-a-foundation-model-2024.md) | `abstract-only` | — | — |  |
| 2024 | [scGPT: toward building a foundation model for single-cell multi-omics using generative AI](notes/scgpt-toward-building-a-2024.md) | `extracted` | ~51M (whole-human model; 12 transformer layers, d_model=512, 8 heads, d_hid=512, vocab ~60K genes) | 33M cells from CELLxGENE Census (human normal); organ-specific models up to 13.2M cells | foundation-model, single-cell, generative, gene-token |
| 2024 | [scInterpreter: Training Large Language Models to Interpret scRNA-seq Data for Cell Type Annotation](notes/scinterpreter-training-large-language-2024.md) | `converted` | — | — |  |
| 2024 | [scMulan: a multitask generative pre-trained language model for single-cell analysis](notes/scmulan-a-multitask-generative-2024.md) | `abstract-only` | — | — |  |
| 2024 | [Transformer-based Single-Cell Language Model: A Survey](notes/transformer-based-single-cell-2024.md) | `extracted` | — | — | survey, transformer, single-cell, foundation-model |
| 2023 | [CellPLM: pre-training of cell language model beyond single cells](notes/cellplm-pre-training-of-2023.md) | `abstract-only` | — | — |  |
| 2023 | [GenePT: a simple but effective foundation model for genes and cells using ChatGPT](notes/genept-a-simple-but-2023.md) | `fetched` | — | — |  |
| 2023 | [scimilarity: rapid annotation of cell types in human scRNA-seq via cell similarity](notes/scimilarity-rapid-annotation-of-2023.md) | `abstract-only` | — | — |  |
| 2023 | [Transfer learning enables predictions in network biology](notes/transfer-learning-enables-predictions-2023.md) | `extracted` | ~10M | ~45B (estimated; ~29.9M cells × ~1.5k genes/cell) | rank-encoding, Genecorpus-30M, MLM, in-silico-perturbation |
| 2023 | [Universal Cell Embeddings: a foundation model for cell biology](notes/universal-cell-embeddings-a-2023.md) | `abstract-only` | — | — |  |
| 2022 | [scBERT: a large-scale pretrained deep language model for cell type annotation of single-cell RNA-seq data](notes/scbert-as-a-large-2022.md) | `extracted` | ~10M | — | Performer, gene-token, expression-binning, Gene2vec |

## single-cell-multiomics (5 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [Open World Knowledge Aided Single-Cell Foundation Model with Robust Cross-Modal Cell-Language Pre-training](notes/open-world-knowledge-aided-2026.md) | `seed` | — | — |  |
| 2025 | [CellVerse: Do Large Language Models Really Understand Cell Biology?](notes/cellverse-do-large-language-2025.md) | `extracted` | — | — | benchmark, single-cell, LLM-evaluation, cell-type-annotation |
| 2025 | [scMamba: A Scalable Foundation Model for Single-Cell Multi-Omics Integration Beyond Highly Variable Feature Selection](notes/scmamba-a-scalable-foundation-2025.md) | `extracted` | — | — | mamba, ssm, state-space-duality, contrastive-learning |
| 2024 | [scGPT: toward building a foundation model for single-cell multi-omics using generative AI](notes/scgpt-toward-building-a-2024.md) | `extracted` | ~51M (whole-human model; 12 transformer layers, d_model=512, 8 heads, d_hid=512, vocab ~60K genes) | 33M cells from CELLxGENE Census (human normal); organ-specific models up to 13.2M cells | foundation-model, single-cell, generative, gene-token |
| 2024 | [Transformer-based Single-Cell Language Model: A Survey](notes/transformer-based-single-cell-2024.md) | `extracted` | — | — | survey, transformer, single-cell, foundation-model |

## small-molecule (11 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2026 | [A Systematic Survey and Benchmark of Deep Learning for Molecular Property Prediction in the Foundation Model Era](notes/a-systematic-survey-and-2026.md) | `converted` | — | — |  |
| 2026 | [Elucidating the Design Space of Flow Matching for Cellular Microscopy](notes/elucidating-the-design-space-2026.md) | `extracted` | 700M | — | ablation-study, flow-matching, generative-model, cell-microscopy |
| 2025 | [Informing Acquisition Functions via Foundation Models for Molecular Discovery](notes/informing-acquisition-functions-via-2025.md) | `converted` | — | — |  |
| 2025 | [LSM-MS2: A Foundation Model Bridging Spectral Identification and Biological Interpretation](notes/lsm-ms2-a-foundation-2025.md) | `extracted` | — | — | foundation-model, transformer, mass-spectrometry, metabolomics |
| 2025 | [Unveiling Latent Knowledge in Chemistry Language Models through Sparse Autoencoders](notes/unveiling-latent-knowledge-in-2025.md) | `converted` | — | — |  |
| 2024 | [ChemFM as a Scaling Law Guided Foundation Model Pre-trained on Informative Chemicals](notes/chemfm-as-a-scaling-2024.md) | `seed` | — | — |  |
| 2024 | [ESM All-Atom: Multi-scale Protein Language Model for Unified Molecular Modeling](notes/esm-all-atom-multi-2024.md) | `extracted` | 35M | — | multi-scale, code-switching, unified-molecular-modeling, protein-molecule-interaction |
| 2024 | [Taming Multi-Domain, -Fidelity Data: Towards Foundation Models for Atomistic Scale Simulations](notes/taming-multi-domain-fidelity-2024.md) | `converted` | — | — |  |
| 2024 | [Tokenization for Molecular Foundation Models](notes/tokenization-for-molecular-foundation-2024.md) | `extracted` | 25M | ~245M molecules (30k steps × batch 8192) for each encoder; 1.6B SMILES for n-gram models | tokenization, ablation, smiles, selfies |
| 2023 | [MolFM: A Multimodal Molecular Foundation Model](notes/molfm-a-multimodal-molecular-2023.md) | `extracted` | ~138M total (structure 1.8M + text 61.8M + KG 12.6M + multimodal encoder 61.8M) | — | knowledge-graph, contrastive-learning, cross-modal-retrieval, molecule-captioning |
| 2020 | [ChemBERTa: Large-Scale Self-Supervised Pretraining for Molecular Property Prediction](notes/chemberta-large-scale-self-2020.md) | `extracted` | not reported (estimated ~83M from RoBERTa config: 6 layers, 12 heads, 768 hidden) | not reported (largest run: 10M SMILES × 3 epochs) | transformer, RoBERTa, SMILES, SELFIES |

## text (2 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2025 | [BioReason: Incentivizing Multimodal Biological Reasoning within a DNA-LLM Model](notes/bioreason-incentivizing-multimodal-biological-2025.md) | `extracted` | ~5B (Evo2-1B + Qwen3-4B; DNA encoder frozen, only LLM + projection trained) | — | multimodal, DNA-LLM, variant-effect-prediction, biological-reasoning |
| 2019 | [BioBERT: a pre-trained biomedical language representation model for biomedical text mining](notes/biobert-a-pre-trained-2019.md) | `extracted` | 110000000 | 98300000000 | continued-pretraining, domain-adaptation, masked-lm, wordpiece |

## vision (1 papers)

| Year | Title | Status | Params | Tokens | Tags |
|------|-------|--------|--------|--------|------|
| 2023 | [BiomedCLIP: a multimodal biomedical foundation model pretrained from fifteen million scientific image-text pairs](notes/biomedclip-a-multimodal-biomedical-2023.md) | `extracted` | ~86M vision + ~110M text (ViT-B/16 + PubMedBERT) | 15M image-text pairs (PMC-15M), 32 epochs | contrastive-learning, CLIP, biomedical-vision-language, domain-adaptation |
