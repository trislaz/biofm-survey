---
id: cell2text-multimodal-llm-for-2025
title: 'Cell2Text: Multimodal LLM for Generating Single-Cell Descriptions from RNA-Seq
  Data'
authors:
- Oussama Kharouiche
- Aris Markogiannakis
- Xiao Fei
- Michail Chatzianastasis
- Michalis Vazirgiannis
year: 2025
venue: null
arxiv: '2509.24840'
doi: null
url: https://arxiv.org/abs/2509.24840v2
pdf_path: papers/cell2text-multimodal-llm-for-2025.pdf
md_path: papers/md/cell2text-multimodal-llm-for-2025.md
modalities:
- scrna
- multimodal
status: extracted
evidence_quality: medium
tags:
- scRNA-seq
- multimodal-generation
- cell-annotation
- geneformer
- llm-decoder
- gene-level-embeddings
- ontology-evaluation
parameters: "~1.3B (Llama-1B variant) / ~4.3B (Gemma-4B variant); encoder Geneformer-V2-316M frozen"
training_tokens: null
training_compute: "8x V100 32GB (Llama); 8x A100 80GB (Gemma); 2-3 epochs"
references_chased: false
added_at: '2026-04-22T19:37:11+00:00'
updated_at: '2026-04-22T20:17:40+00:00'
---

## TL;DR

Cell2Text bridges frozen Geneformer-V2-316M **gene-level** embeddings (no CLS pooling) to instruction-tuned LLMs (Llama-3.2-1B / Gemma3-4B) via a 2-layer MLP adapter, trained on 1M CELLxGENE cells paired with structured text (cell type, tissue, disease, top-2 Hallmark pathways). Generates natural-language cell descriptions; classification labels extracted via regex. Outperforms Geneformer+linear-head on cell-type accuracy by ~10 pp (77.8% vs 67.3%) and achieves BioBERT-F1 > 93.9%. Full fine-tuning ≫ LoRA; Gemma-4B ≈ Llama-1B full FT.

## Model

- **Encoder**: Geneformer-V2-316M (transformer, pre-trained on ~30M single-cell transcriptomes, masked gene prediction). Context length 4096 genes. **Frozen** throughout.
- **Adapter**: 2-layer feedforward + non-linear activation, projects each gene embedding from Geneformer dim → LLM embedding dim. L2-normalized output. Trainable.
- **Decoder**: Instruction-tuned LLM (Llama-3.2-1B-Instruct or Gemma3-4B-it). Input = system prompt + projected gene embeddings sequence. Either full fine-tuned or LoRA (rank 256, α=512, attention modules only).
- Gene-level embedding strategy: each of N gene embeddings (up to 4096) is individually projected and fed as a token sequence to the LLM, preserving per-gene information instead of pooling to a single cell vector.

## Data

- **Source**: CELLxGENE Census, 1M cells, 7,331 donors, 783 cell types, 347 tissue types, 128 diseases.
- **Sampling**: Composite multi-objective stratification to boost diversity (Shannon diversity: cell-type 0.747→0.843, tissue 0.611→0.704, disease 0.348→0.496). Excluded Smart-seq family, niche protocols, targeted assays.
- **Text targets**: Structured descriptions combining (1) Cell Ontology (OBO) definitions for cell type, (2) tissue/disease/donor metadata, (3) top-2 enriched Hallmark pathways from pySCENIC (AUCell, 34 retained pathways after 0.5% prevalence filter, from MSigDB 50 Hallmark set).
- **Split**: Donor-level 80/10/10 (no donor leakage).
- **Tokenization stats**: Gene sequences avg 1843 Geneformer tokens; text descriptions avg 104 Llama tokens.

## Training Recipe

| Variant | LLM | Hardware | LR | Scheduler | Epochs | Batch (eff.) | Tuning |
|---|---|---|---|---|---|---|---|
| Cell2Text-Llama-1B-LoRA | Llama-3.2-1B-Instruct | 8× V100 32GB | 2e-4 | StepLR γ=0.98 | 3 | 128 (2/GPU × 8 accum) | LoRA r=256, α=512, attn only |
| Cell2Text-Llama-1B | Llama-3.2-1B-Instruct | 8× V100 32GB | 2e-4 | StepLR γ=0.98 | 2 | 192 (3/GPU × 8 accum) | Full FT |
| Cell2Text-Gemma-4B | Gemma3-4B-it | 8× A100 80GB | 5e-5 | StepLR γ=0.98 | 3 | 128 (2/GPU × 8 accum) | Full FT |

Optimizer: Adam. Geneformer encoder frozen in all variants. Adapter always trainable.

## Key Ablations & Design Choices

1. **Gene-level vs cell-level embeddings**: Core novelty. Instead of pooling Geneformer output to a single CLS vector (as in Geneformer+Head baselines), each gene's contextualized embedding is projected and fed as a separate token to the LLM. Authors argue this preserves granular transcriptional information. The +10 pp cell-type accuracy gain over Geneformer+Head suggests the LLM can leverage per-gene context better than a linear head on a pooled representation.

2. **Full fine-tuning vs LoRA**: Full FT of Llama-1B beats LoRA by ~6 pp on cell type (76.9% vs 70.9%), ~5 pp on tissue, ~5 pp on disease. LoRA even underperforms the Geneformer+Head baseline on tissue (68.0% vs 68.5%) and disease (72.7% vs 74.1%). PageRank similarity: full FT 85.3% vs LoRA 75.6% (LoRA worse than Geneformer+Head 80.6%).

3. **Model scale (1B vs 4B)**: Gemma-4B vs Llama-1B full FT are very close: cell type 77.8% vs 76.9%, tissue 73.0% vs 73.4%, disease 77.3% vs 77.8%. Text generation quality nearly identical (BioBERT-F1: 93.93 vs 93.90). Diminishing returns from 1B→4B for this task, though Gemma uses a different architecture (hybrid sliding-window/global attention).

4. **Generative vs discriminative**: Cell2Text (generative, regex-parsed labels) outperforms Geneformer+Head (discriminative) on cell type (+10.6 pp), tissue (+4.5 pp), disease (+3.8 pp). Suggests text generation objective induces richer representations than classification-head training.

5. **PageRank ontology-aware evaluation**: When Cell2Text misclassifies, predictions tend to be ontologically close (parent/sibling cell types). Average PageRank similarity: 85.6% (Gemma-4B) vs 80.6% (Geneformer+Head), confirming biologically coherent errors.

6. **Pathway classification**: Cell2Text competitive but does not dominate: LGBM ensemble (44.1% subset accuracy, 60.4% Jaccard) > Cell2Text-Llama-1B (42.3%, 58.8%) > Geneformer+Head (40.1%, 57.2%). The LGBM uses 34 independent binary classifiers—purpose-built for the task—while Cell2Text treats it as a text generation side-effect.

7. **Text quality**: Exact match rates low (5.8–7.0%) as expected for generative paraphrasing, but BLEU-4 ~77, ROUGE-L ~82, BioBERT-F1 >93.9%, indicating high semantic fidelity. Structured prompts with system message help format consistency.

## Reported Insights

- Training to generate coherent text descriptions produces richer cell representations than traditional classification heads, even when evaluated on classification accuracy.
- Gene-level (not pooled) embeddings are critical; the LLM decoder acts as a flexible aggregation mechanism over per-gene signals.
- Ontology-aware evaluation (PageRank similarity) reveals that accuracy understates model quality: "misses" are often biologically sensible (e.g., CD4+ T-cell predicted as T-cell).
- LoRA is insufficient for this cross-modal alignment task; full fine-tuning of the LLM is needed to properly adapt to the gene-embedding input modality.
- Scaling LLM from 1B to 4B yields marginal gains, suggesting the bottleneck is elsewhere (data, encoder, or adapter capacity).

## References Worth Chasing

1. **Geneformer** (Theodoris et al., 2023) — encoder used; 30M cell pre-training, transfer learning in network biology.
2. **Geneformer-V2** (Chen et al., 2024) — quantized multi-task, context-specific gene network dynamics; the actual 316M model used.
3. **scGPT** (Cui et al., 2024) — decoder-only single-cell FM; compared architecturally.
4. **Cell2Sentence** (Levine et al., 2024) — prior art converting gene expression to text (top-100 gene names); Cell2Text improves upon this.
5. **Cell2Sentence-Scale** (Rizvi et al., 2025) — scaling C2S approach; direct predecessor.
6. **CellWhisperer** (Schaefer et al., 2024) — CLIP-style contrastive alignment of gene expression + text; uses bulk RNA-seq not scRNA.
7. **scBERT** (Yang et al., 2022) — BERT-style single-cell encoder.
8. **scCello** (Yuan et al., 2024) — Cell Ontology-guided transcriptome FM; ontology similarity for contrastive learning (Cell2Text uses it for evaluation instead).
9. **Prot2Text** (Abdine et al., 2024) — protein sequence → text generation with GNNs + transformers; architectural inspiration.
10. **Prot2Text-V2** (Fei et al., 2025) — multimodal contrastive alignment for protein function prediction.
11. **ChatNT** (de Almeida et al., 2025) — multimodal conversational agent for DNA/RNA/protein; same cross-modal generation paradigm.
12. **CELLxGENE Census** (Program et al., 2024) — data source, single-cell data platform.
13. **pySCENIC** (Aibar et al., 2017) — pathway activity scoring used for generating training text targets.

## Notes / Open Questions

- No pre-training of the adapter or LLM on unlabeled scRNA-seq; purely supervised fine-tuning on structured text. This limits scalability to labeled data availability.
- The text targets are **template-generated** from metadata + ontology definitions + pySCENIC pathways—not free-form expert annotations. Quality ceiling is bounded by metadata completeness and pySCENIC accuracy.
- No comparison with CellWhisperer or Cell2Sentence baselines despite being the most relevant prior work; only Geneformer+Head and LightGBM baselines.
- Donor-level split is good practice but cell-type distribution across donors is not discussed—potential for some rare types to appear only in train or test.
- Unclear how well this generalizes to novel cell types truly absent from training (zero-shot). The 783 cell types are all seen during training.
- 4096-gene context limit from Geneformer may lose low-expression genes; authors argue "highest-expressed genes include most of the biological information" but this is unvalidated.
- No ablation on adapter architecture (depth, width, normalization) or on number of genes in the input sequence.
- Arxiv preprint (2509.24840), not peer-reviewed.
