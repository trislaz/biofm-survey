---
id: effective-gene-expression-prediction-2021
title: Effective gene expression prediction from sequence by integrating long-range
  interactions
authors:
- Žiga Avsec
- Vikram Agarwal
- Daniel Visentin
- Joseph R. Ledsam
- Agnieszka Grabska-Barwinska
- Kyle R. Taylor
- Yannis Assael
- John Jumper
- Pushmeet Kohli
- David R. Kelley
year: 2021
venue: Nature Methods
arxiv: null
doi: 10.1038/s41592-021-01252-x
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/effective-gene-expression-prediction-2021.md
modalities:
- epigenome
status: extracted
evidence_quality: full-text
tags:
- transformer
- self-attention
- long-range-interactions
- relative-positional-encoding
- attention-pooling
- convolutional-stem
- multitask
- gene-expression-prediction
- variant-effect-prediction
- enhancer-promoter
- DNA-sequence
- regulatory-genomics
parameters: 249000000
training_tokens: null
training_compute: 3-days-64xTPUv3
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

Enformer is a hybrid CNN-transformer model for predicting 5,313 epigenomic and transcriptional tracks at 128-bp resolution from 200 kb of input DNA sequence. By replacing the dilated convolutions of Basenji2 with 11 self-attention transformer blocks, it extends the effective receptive field from 20 kb to 100 kb, capturing 84% of known enhancer–gene pairs (vs 47% at 20 kb). This yields mean CAGE gene-expression correlation of 0.85 (vs 0.81 for Basenji2), closing one-third of the gap to the experimental ceiling of 0.94. The larger receptive field also improves variant effect prediction (eQTLs, MPRA saturation mutagenesis) and enables enhancer prioritization from sequence alone competitive with the ABC score that uses experimental Hi-C and H3K27ac data.

## Model

- **Architecture**: 7 convolutional blocks with attention pooling → 11 transformer blocks → cropping layer → 2 organism-specific pointwise-convolution heads (human 5,313 tracks, mouse 1,643 tracks).
- **Input**: One-hot encoded DNA, 196,608 bp (A/C/G/T/N). Output: 896 bins × 128-bp resolution = 114,688 bp central region. Cropping removes 320 positions (40,960 bp) per side.
- **Channels**: 1,536 (2× Basenji2's 768).
- **MHA**: 8 heads per layer, key/query size 64, value size 192. Global (not local) attention over the full 1,536-position sequence after conv pooling.
- **Positional encoding**: Custom relative positional basis functions (exponential, central mask, gamma), each in symmetric f(|x|) and asymmetric sign(x)·f(|x|) forms. 192 basis functions total (64 per class, 32 symmetric + 32 asymmetric each). Injected via Transformer-XL-style relative attention.
- **Attention pooling**: Replaces max pooling; uses learned softmax-weighted sum over pooling windows (size 2, stride 2), initialized to approximate max pooling.
- **Dropout**: 0.01 for positional encoding features, 0.05 for final attention matrix.
- **Parameters**: ~249M (estimated from architecture specs and public code; not explicitly stated in paper).
- **Output activation**: Softplus for Poisson targets.

## Data

- **Genome splits**: Bipartite graph of 1-Mb regions from human (hg38) and mouse (mm10), edges from syntenic alignment; connected components partitioned into train/val/test.
  - Human: 34,021 train / 2,213 val / 1,937 test sequences.
  - Mouse: 29,295 train / 2,209 val / 2,017 test sequences.
- **Human tracks (5,313)**: 2,131 TF ChIP-seq, 1,860 histone-modification ChIP-seq, 684 DNase-seq/ATAC-seq, 638 CAGE.
- **Mouse tracks (1,643)**: 308 TF ChIP-seq, 750 histone-modification ChIP-seq, 228 DNase-seq/ATAC-seq, 357 CAGE.
- **Input extension**: 196,608 bp (extended from Basenji2's 131,072 bp).
- **Data augmentation**: Random shift up to ±3 bp, reverse complement with reversed targets.
- **Evaluation datasets**: CRISPRi enhancer assays (Gasperini et al., Fulco et al.), GTEx eQTLs (v7a for SLDP, v8 for fine-mapping), CAGI5 saturation mutagenesis MPRAs.

## Training Recipe

- **Hardware**: 64 TPU v3 cores, ~3 days.
- **Batch size**: 64 (1 per core). Alternating human and mouse batches.
- **Steps**: 150,000 (joint human+mouse), then 30,000 fine-tuning steps on human only.
- **Optimizer**: Adam (Sonnet v2), lr 0.0005 (main) / 0.0001 (fine-tuning), β₁=0.9, β₂=0.999, ε=1e-8.
- **LR schedule**: Linear warmup from 0 to target over first 5,000 steps.
- **Gradient clipping**: Max global norm 0.2.
- **Batch norm**: Statistics aggregated across all 64 replicas, momentum 0.9.
- **Loss**: Poisson negative log-likelihood (same as Basenji2).
- **Test-time augmentation**: Average predictions from 8 randomly augmented sequences (≤3 bp shifts + reverse complement).
- **Ablation models**: 768 channels (half), 131 kb input, batch 32 on 32 TPU v3 cores, 500,000 steps, best checkpoint by val Spearman on CAGE TSS every 1,000 steps. Dilated-conv variants used lr 0.02 without warmup.

## Key Ablations & Design Choices

### 1. Attention vs Dilated Convolutions (Extended Data Fig. 5a)
- Attention layers outperformed dilated convolutions across **all** model sizes, numbers of layers, and training data sizes when both used the same total compute.
- This is the core architectural contribution: attention enables effective long-range information flow that dilated convolutions cannot match even with many successive layers.

### 2. Global vs Local Attention / Receptive Field (Extended Data Fig. 5b)
- Replacing global attention with local attention (restricting receptive field to Basenji2's 20 kb) caused a **large performance drop**, confirming that the 100-kb receptive field is critical.
- Receptive field expansion from 20 kb to 100 kb increases the fraction of captured enhancer–gene pairs from 47% to 84% (based on high-confidence pairs from Fulco et al.).

### 3. Custom Relative Positional Encodings (Extended Data Fig. 6)
- Three basis function classes (exponential, central mask, gamma) with symmetric + asymmetric versions outperform both standard relative basis functions (Transformer-XL) and absolute positional encodings.
- Asymmetric (directional) basis functions help distinguish upstream vs downstream of TSS.
- The multi-scale design (exponential decay for proximal, gamma for distal) enables the model to differentially weight proximal and distal regulatory elements.

### 4. Scaling (Extended Data Fig. 5a)
- Increasing model parameters consistently improved performance, echoing NLP scaling trends.
- Enformer uses 2× channels (1,536 vs 768) relative to Basenji2.

### 5. Attention Pooling vs Max Pooling
- Attention pooling (learned softmax-weighted sum) replaces max pooling in convolutional blocks. Initialization approximates max pooling (w = 2×I), with slight performance gain over random or zero initialization.

### 6. Input Sequence Length
- 196,608 bp (1.5× Basenji2's 131,072 bp) to match the expanded receptive field.

## Reported Insights

- **Long-range regulation is learnable from sequence**: The model attends to CRISPRi-validated enhancers >20 kb away and correctly predicts their cell-type-specific contribution scores. Contribution scores correlate with H3K27ac marks at enhancers.
- **Insulator/TAD boundary awareness**: Attention is significantly higher at TAD boundaries and significantly lower across them, recapitulating biological compartmentalization without explicit 3D structure training. CTCF motifs are a key signal.
- **Enhancer prioritization from sequence alone**: Enformer contribution scores (gradient×input, attention, ISM) match or exceed the ABC score (which uses experimental H3K27ac and Hi-C data) for CRISPRi-validated enhancer–gene pair classification.
- **Variant effect prediction**: Improved SLDP concordance with GTEx eQTLs (max Z-score 6.9 vs 6.3 for Basenji2). Fine-mapped eQTL classification auROC 0.747 vs 0.729. Improvement consistent across all TSS-distance bins.
- **Saturation mutagenesis**: Best average correlation across all 15 CAGI5 loci, outperforming the competition winner (P=0.002). Training-free variant scoring (cell-matched CAGE/DNase features summarized by first PC) performs comparably to lasso-trained approach.
- **Cell-type specificity**: Cell-type-specific contribution scores yield better enhancer prioritization than cell-type-agnostic ones, confirming the model uses different enhancer signals per cell type.
- **Experimental ceiling**: Estimated at 0.94 Pearson r from CAGE replicate concordance. Enformer closes 1/3 of the gap from Basenji2 (0.81 → 0.85 of 0.94).
- **Paths forward noted by authors**: Higher-resolution targets, more organisms, 3D genome structure integration, representation learning for unseen cell types, efficient transformers for further scaling.

## References Worth Chasing

- Basenji2 (Kelley 2020, Genome Res) — predecessor architecture using dilated convolutions; same training data/evaluation framework
- ExPecto (Zhou et al. 2018, Nature Genetics) — sequence-based gene expression prediction using 20-kb context and linear models on deep-learning features
- Basenji1 (Kelley et al. 2018, Genome Res) — original deep CNN for gene expression from sequence
- DeepSEA / Beluga (Zhou & Troyanskaya 2015, Nature Methods; Zhou et al. 2019) — early deep learning for variant effect; Beluga variant used in ExPecto
- ABC model (Fulco et al. 2019, Nature Genetics) — activity-by-contact model for enhancer–gene linking using H3K27ac + Hi-C
- Gasperini et al. 2019 (Cell) — large-scale CRISPRi enhancer screen in K562 used for enhancer prioritization benchmarking
- Vaswani et al. 2017 (NeurIPS) — original Transformer architecture
- Dai et al. 2019 (ACL) — Transformer-XL with relative positional encodings, basis for Enformer's positional scheme
- SLDP (Reshef et al. 2018, Nature Genetics) — signed LD profile regression for variant annotation concordance with GWAS
- SuSiE (Wang et al. 2020, JRSS-B) — fine-mapping method used for GTEx causal variant identification
- Akita (Fudenberg et al. 2020, Nature Methods) — predicting 3D chromatin contacts from sequence; mentioned as complementary
- Sei (Chen et al. 2022, Nature Genetics) — sequence-based regulatory model, potential downstream comparison
- Xpresso (Agarwal & Shendure 2020) — gene expression from promoter sequence features
- BPNet (Avsec et al. 2021, Nature Genetics) — base-resolution deep learning for TF binding from same senior author

## Notes / Open Questions

- **Parameter count not reported**: The paper never states total parameters. ~249M is estimated from public code (github.com/deepmind/deepmind-research/tree/master/enformer). The paper only notes "twice as many channels" as Basenji2.
- **Training tokens not reported**: Can be estimated as ~1.9T bases (150k steps × 64 batch × 196,608 bp) plus ~0.4T for fine-tuning, but this conflates nucleotide-level input with the model's effective 128-bp bin resolution.
- **No explicit compute budget**: "approximately 3 days" on 64 TPU v3 cores is the only statement. Total FLOPs not disclosed.
- **Causal vs correlational improvements**: The paper attributes gains to the larger receptive field, but the model also has 2× channels, 1.5× input length, and attention pooling. The ablation isolating attention vs dilated convolutions (Extended Data Fig. 5) controls for model size but does not fully disentangle the other changes.
- **Generalization to unseen cell types**: A key limitation acknowledged by the authors — Enformer can only predict for cell types and assays present in training data. No zero-shot cell-type transfer.
- **Quadratic attention complexity**: The 1,536-position sequence length (after conv pooling) is feasible but limits further resolution increases. Authors note efficient transformers as a future direction.
- **CRISPRi benchmarks limited to K562**: Both Gasperini and Fulco datasets are from K562 cells. Enhancer prioritization generalization to other cell types is untested.
- **Fine-tuning only on human**: After joint training, the model is fine-tuned on human data only. Mouse-specific performance after fine-tuning is not reported.
- **No pre-training objective innovation**: Uses same Poisson NLL as Basenji2. The contribution is purely architectural (transformer blocks, attention pooling, positional encoding, larger receptive field).

## Verification (Rev 3)

Source: `papers/md/effective-gene-expression-prediction-2021.md` (PMC full text).

| # | insights.md line | Claim (paraphrased) | Verdict | Rationale |
|---|---|---|---|---|
| 1 | 118 | "Enformer combines convolutional stem + transformer blocks to achieve **200 kb receptive fields**, outperforming pure CNNs (Basenji2) across all model sizes" | **partial** | Architecture and superiority over dilated convolutions "across all model sizes, numbers of layers, and numbers of training data points" confirmed (§ Results ¶2). However, *200 kb* is the **input** sequence length (196,608 bp); the paper consistently states the effective receptive field is **100 kb** ("reaching distal regulatory elements up to 100 kb away", Abstract & Fig. 1a). |
| 2 | 174 | "Enformer uses Poisson NLL over binned epigenomic/expression tracks" | **supported** | "trained… using the same Poisson negative log-likelihood loss function as Basenji2" (Methods, ¶1); 128-bp bins confirmed throughout. |
| 3 | 201 (table) | "Enformer \| DNA→epigenome \| **200 kb (≈ 200 k nt)** \| CNN stem + transformer" | **partial** | Column header is "Effective context". The 200 kb figure is the raw input window; the paper's stated effective reach is 100 kb. Modality and architecture are correct. |
| 4 | 269 | "Enformer designed a custom relative positional encoding scheme for genomic distances" | **supported** | Three custom basis function classes (exponential, central mask, gamma) with symmetric + asymmetric versions, injected via Transformer-XL-style relative attention (Methods, ¶ Positional encoding; Extended Data Fig. 6). |
| 5a | 409 | "Gene expression correlation reached 0.85, closing roughly 1/3 of the gap to the 0.94 **inter-individual** ceiling" | **partial** | Numbers correct: "correlation from 0.81 to 0.85, one-third of the way toward the experimental-level accuracy of 0.94" (Discussion). However the paper calls this an "experimental-level accuracy… estimated from replicates" (CAGE replicate concordance), not an "inter-individual" ceiling. |
| 5b | 410 | "Attention > dilated convolutions at all model sizes" | **supported** | "Attention layers outperformed dilated convolutions across all model sizes, numbers of layers, and numbers of training data points" (Results ¶2). |
| 5c | 411 | "Custom relative positional encoding was **critical**" | **partial** | Paper says "noticeable performance improvement" (Results ¶2), not "critical". The word "crucial" is reserved for the larger receptive field, not the positional encoding per se. |
| 6 | 604 | "Enformer's expression correlation **plateaus** at 0.85 vs a 0.94 ceiling" | **partial** | Numbers correct. However the paper does not claim a plateau — it notes "increasing the number of parameters improved model performance" and lists multiple promising paths for further improvement (Discussion). "Plateaus" is an unsupported editorial characterisation. |

**Summary**: 3 supported, 5 partial, 0 unsupported, 0 out-of-scope.
Recurring issue: the "200 kb" figure is the input length, not the effective receptive field (100 kb). The "inter-individual" ceiling label and "plateaus" wording are not in the source.
