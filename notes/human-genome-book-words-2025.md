---
id: human-genome-book-words-2025
title: 'Human Genome Book: Words, Sentences and Paragraphs'
authors:
- Wang Liang
year: 2025
venue: null
arxiv: '2501.16982'
doi: null
url: https://arxiv.org/abs/2501.16982v1
pdf_path: papers/human-genome-book-words-2025.pdf
md_path: papers/md/human-genome-book-words-2025.md
modalities:
- dna
- protein-sequence
status: extracted
evidence_quality: low
tags:
- genomics
- language-transfer
- cross-lingual
- genome-segmentation
- GPT-2
- BPE-tokenizer
parameters: 117M
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:00+00:00'
updated_at: '2026-04-22T20:21:36+00:00'
---

## TL;DR

Trains a GPT-2 Small (~117M params) from scratch on English + DNA + protein data with a shared 100K BPE tokenizer, fine-tunes on English semantic similarity (PAWSX) to enable cross-lingual transfer from English to DNA, then further fine-tunes for sentence splitting, paragraph segmentation, and summarization using English-only datasets. Applies these models to segment the human genome (GRCh38.p14) into hierarchical "words," "sentences," and "paragraphs," producing a structured genomic "book." Transfer to DNA is validated only for sequence similarity judgment (79–92% accuracy); segmentation/summarization transfer is hypothesised but not directly verified.

## Model

- **Architecture**: GPT-2 Small — 12 Transformer layers, 768 hidden units, 12 attention heads, max sequence length 1024.
- **Parameters**: ~117 million.
- **Tokenizer**: BPE trained from scratch on 2 GB each of DNA, protein, and English data → ~100K token vocabulary.
- **Model family**:
  - `gpt2-gene-eng` — base pre-trained model (English + DNA + protein).
  - `gpt2-gene-eng-ft` — fine-tuned on PAWSX English similarity for cross-lingual transfer.
  - `gene_eng_gpt2_para_seg` — paragraph segmentation model (fine-tuned from gpt2-gene-eng-ft on Wikipedia paragraph data).
  - `gene_eng_gpt2_summary` — summarisation model (fine-tuned from gpt2-gene-eng-ft on Amazon review titles).
  - Sentence splitting uses gpt2-gene-eng-ft directly (predicts period token).

## Data

- **BPE tokenizer training**: 2 GB DNA (multi-organism genomes) + 2 GB protein (UniProt) + 2 GB English (OpenWebText) = 6 GB.
- **Pre-training**: 10 GB DNA (300–1000 bp fragments from model organisms, following DNABERT approach) + 10 GB protein (Swiss-Prot + TrEMBL) + 10 GB English (OpenWebText + Wikipedia) = 30 GB total.
- **Fine-tuning (transfer)**: PAWSX English semantic similarity dataset.
- **Fine-tuning (paragraph segmentation)**: Wikipedia with `<p_end>` paragraph markers.
- **Fine-tuning (summarisation)**: Amazon English Review Dataset (review → title).
- **Genome processed**: GRCh38.p14 human reference genome (primarily Chromosome 1 demonstrated).

## Training Recipe

1. Train BPE tokenizer on mixed 6 GB corpus → 100K vocab.
2. Pre-train GPT-2 Small from scratch on 30 GB mixed DNA/protein/English, single NVIDIA 4090, mixed-precision, 3–5 epochs, dynamic learning rate → `gpt2-gene-eng`.
3. Classification fine-tune on PAWSX English similarity (classification head, 2-class) → `gpt2-gene-eng-ft`. Validates transfer: 79–92% accuracy on DNA similarity benchmarks.
4. Further fine-tune from `gpt2-gene-eng-ft` on Wikipedia paragraph segmentation (causal LM, predicting `<p_end>` token), AdamW, lr = 5e-5, cross-entropy → `gene_eng_gpt2_para_seg`.
5. Further fine-tune from `gpt2-gene-eng-ft` on Amazon reviews summarisation ("[Original Text] TL;DR: [Summary]" format, causal LM) → `gene_eng_gpt2_summary`.
6. Apply models to GRCh38.p14: split chromosome into ~10 MB parts → paragraph segmentation → sentence splitting → tokenisation. Hierarchical clustering of paragraph embeddings produces Sections and Chapters. Summaries generate titles at each level.
7. DNA-to-English translation via nearest-neighbour lookup in embedding space (last hidden layer of gpt2-gene-eng-ft); ~19K DNA terms mapped to ~600 unique English words.

## Key Ablations & Design Choices (MOST IMPORTANT)

- **Unified BPE tokenizer across modalities** is identified as a critical prerequisite for cross-lingual transfer (following multilingual NLP literature).
- **Transfer validation is partial**: only sequence similarity judgment is directly tested (79–92% accuracy on DNA150s/DNA150/DNA50). Segmentation and summarisation transfer to DNA is assumed but **not verified** — the paper explicitly states these are hypothetical transfers.
- **Strategy 1 for segmentation** (predict next-token paragraph marker via causal LM) chosen over Strategy 2 (binary classification at each position) for simplicity.
- **PCA visualisation** (Fig. 3) shows DNA and English word vectors overlap more after fine-tuning, providing qualitative evidence for transfer.
- **Dynamic masking at inference** for summarisation: constrains output tokens to DNA-relevant vocabulary by setting irrelevant token scores to -inf.
- **Hierarchical genome structure**: 3 levels (Chapters → Sections → Paragraphs) built via dynamic clustering of paragraph embeddings; depth chosen to match typical book structure (~38 chapters for Chr1 Part 1).
- No comparison against existing genomic segmentation methods or biological ground truth (e.g., gene boundaries, TADs).

## Reported Insights

- English language capabilities transfer to DNA sequences when using a shared BPE tokenizer and fine-tuning on similarity tasks (accuracy 79–92%).
- The constructed genomic "book" for Chromosome 1 Part 1 yields 15,238 paragraphs → 503 sections → 38 chapters.
- DNA-to-English vocabulary mapping: ~19,000 DNA words map to only ~600 unique English words, based on embedding-space cosine similarity (structural, not semantic).
- Potential applications proposed: fast hierarchical DNA search, genome unique identifiers (fault-tolerant to point mutations), genome data compression.
- The paper is explicitly "illustrative" and acknowledges no definitive biological interpretations are provided.

## References Worth Chasing

- Ref 30: Liang W, "Can linguists better understand DNA?" (arXiv:2412.07678, 2024) — predecessor work validating NL-to-DNA transfer.
- Ref 1: Sanabria et al., "The human genome's vocabulary as proposed by GROVER" (bioRxiv 2023) — DNA vocabulary via language model.
- Ref 12: Nguyen et al., Evo (Science 2024) — genome-scale sequence modelling.
- Ref 25: Yuan et al., "How Vocabulary Sharing Facilitates Multilingualism in LLaMA?" — multilingual transfer mechanics.

## Notes / Open Questions

- Evidence quality is low: the core claim (NLP abilities transfer to DNA for segmentation/summarisation) is not empirically validated beyond similarity judgment. No downstream biological evaluation is provided.
- Only Chromosome 1 results are shown in detail; generalisability to the full genome is unclear.
- The DNA-to-English mapping is purely geometric (embedding cosine similarity) and explicitly disclaimed as non-semantic — limited interpretive value.
- Single GPU (4090) training with a 117M-param model is very small by current genomic FM standards; unclear how this scales.
- No comparison to established DNA segmentation baselines (e.g., gene annotation, repeat masking, chromatin domain callers).
- GitHub: https://github.com/maris205/genome_book
