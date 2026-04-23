---
id: scgpt-toward-building-a-2024
title: 'scGPT: toward building a foundation model for single-cell multi-omics using
  generative AI'
authors:
- Haotian Cui
- Chloe Wang
- Hassaan Maan
- Kuan Pang
- Fengning Luo
- Nan Duan
- Bo Wang
year: 2024
venue: Nature Methods
arxiv: null
doi: 10.1038/s41592-024-02201-0
url: https://www.nature.com/articles/s41592-024-02201-0
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/scgpt-toward-building-a-2024.md
modalities:
- scrna
- single-cell-multiomics
status: extracted
evidence_quality: abstract+repo
tags:
- foundation-model
- single-cell
- generative
- gene-token
- value-binning
- transformer-encoder
- generative-attention-masking
- masked-value-prediction
- contrastive-cell-embedding
- transfer-learning
- cell-type-annotation
- batch-integration
- perturbation-prediction
- gene-network-inference
- multi-omic-integration
parameters: "~51M (whole-human model; 12 transformer layers, d_model=512, 8 heads, d_hid=512, vocab ~60K genes)"
training_tokens: "33M cells from CELLxGENE Census (human normal); organ-specific models up to 13.2M cells"
training_compute: null
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

scGPT is a transformer-based foundation model for single-cell biology, pretrained on ~33 million human cells from the CELLxGENE Census. It treats each cell as a "sentence" of gene tokens ordered by expression value, using a novel **generative attention masking** scheme that enables autoregressive-style prediction over genes sorted by expression—despite using an encoder architecture. The model (~51M parameters; 12 layers, d_model=512, 8 heads) learns joint gene and cell representations via multiple self-supervised objectives: masked value prediction, contrastive cell embedding (CCE), elastic cell similarity (ECS), and domain-adversarial training (DAB). After fine-tuning, scGPT achieves strong performance on cell type annotation, multi-batch integration, multi-omic integration, perturbation response prediction, and gene regulatory network inference. Published in Nature Methods (2024).

## Model

- **Name**: scGPT (single-cell Generative Pre-trained Transformer)
- **Architecture**: Transformer encoder (`TransformerEncoder` / `TransformerEncoderLayer` in PyTorch) with generative attention masking. Despite the "GPT" name, the backbone is bidirectional; the generative aspect comes from a custom attention mask during pretraining that orders genes by expression value, allowing each gene to attend only to genes with higher expression—mimicking autoregressive factorization
- **Hyperparameters (whole-human model)**: 12 layers, d_model=512, 8 attention heads, d_hid=512 (feedforward dim), ~60K gene vocabulary → ~51M parameters total
- **Input representation**: Each gene is a token. Gene identity is embedded via a learned `GeneEncoder` (nn.Embedding). Expression values are encoded via either: (1) `ContinuousValueEncoder` (MLP mapping scalar → d_model), (2) `CategoryValueEncoder` (binned into n_bins=51 discrete bins, then embedded), or (3) scaling mode (multiply gene embedding by value). Gene + value embeddings are summed (or multiplied in scaling mode)
- **Cell embedding**: Obtained from CLS token (default), average pooling, or weighted pooling over gene token representations
- **Output heads**: (1) `ExprDecoder` for masked gene expression prediction, (2) `ClsDecoder` for cell type classification, (3) `MVCDecoder` for masked value prediction conditioned on cell embedding, (4) `AdversarialDiscriminator` with gradient reversal for batch correction
- **Special tokens**: `<pad>`, `<cls>`, `<eoc>` (end-of-cell)
- **Flash attention**: Optional integration via `FlashMHA` for efficiency
- **Organ-specific models**: brain (13.2M cells), blood (10.3M), heart (1.8M), lung (2.1M), kidney (814K), pan-cancer (5.7M cells)

## Data

- **Pre-training (whole-human)**: ~33 million normal human cells from the CELLxGENE Census, spanning diverse tissues and cell types. Vocabulary of ~60K gene names
- **Gene selection**: Highly variable genes (HVG) filtering; fine-tuning examples use n_hvg=1,200
- **Preprocessing pipeline**: (1) filter genes by counts ≥3, (2) optionally filter cells, (3) normalize total to 10,000, (4) log1p transform, (5) subset to HVG, (6) bin expression values into 51 discrete bins
- **Downstream benchmarks**: Multiple scRNA-seq datasets for cell type annotation (e.g., PBMC 10K), multi-batch integration, perturbation prediction (Norman et al. CRISPR screen data), gene regulatory network inference, multi-omic integration (scRNA-seq + scATAC-seq)

## Training Recipe

- **Pre-training objective**: Generative attention masking—genes sorted by expression value, each gene predicts its expression conditioned on genes with higher expression. Combined with masked value prediction (random 40% masking at fine-tuning)
- **Multi-task fine-tuning losses**: (1) Masked MSE loss on expression values, (2) negative log-Bernoulli for explicit zero probability modeling, (3) MVC (masked value prediction for cell embedding), (4) ECS (elastic cell similarity, threshold=0.8), (5) DAB (domain-adversarial batch correction via gradient reversal)
- **Optimizer**: Adam, lr=1e-4, eps=1e-4 (with AMP) or 1e-8
- **Scheduler**: StepLR with gamma=0.9 per epoch
- **Batch size**: 64 (fine-tuning); per-sequence batch sampling with domain-specific batch normalization (DSBN)
- **Mixed precision**: Automatic Mixed Precision (AMP) enabled by default
- **Fine-tuning**: 30 epochs for integration tasks; model config loaded from pretrained args.json

## Key Ablations & Design Choices

1. **Gene ordering by expression**: The generative attention masking sorts genes by expression value, creating a natural ordering for autoregressive modeling of gene expression. This is a key design departure from BERT-style random masking (used by scBERT) and enables generation of full expression profiles
2. **Value binning (n_bins=51)**: Expression values are discretized into 51 bins for the category input embedding mode; this provides a trade-off between resolution and vocabulary size
3. **Explicit zero probability**: A separate Bernoulli head models whether each gene has zero expression, addressing the extreme sparsity of scRNA-seq data (dropout/zero-inflation)
4. **Domain-specific batch normalization (DSBN)**: Separate batch-norm statistics per dataset/batch, combined with adversarial training (DAB), for robust batch effect removal during integration tasks
5. **Cell embedding via CLS token**: A special CLS token aggregates cell-level information, enabling cell-level tasks (classification, similarity) alongside gene-level tasks (expression prediction)
6. **Organ-specific vs whole-human pretraining**: Multiple pretrained checkpoints available; whole-human recommended by default, organ-specific models can outperform when fine-tuning data matches tissue context
7. **Continual pretraining**: A separate checkpoint for zero-shot cell embedding tasks, obtained via continual pretraining of the whole-human model

## Reported Insights

- scGPT demonstrates that the "language model" analogy (genes as words, cells as sentences) is productive for single-cell biology, with generative pretraining being a key distinction from masked-only approaches
- The model effectively distills biological insights: gene embeddings capture functional relationships, cell embeddings capture cell type identity
- Transfer learning from the pretrained model substantially improves performance on all downstream tasks compared to training from scratch
- The reference mapping feature enables similarity search across all 33M pretrained cells using FAISS, with <1 second latency for 10K query cells on GPU and <1GB memory for the full index
- scGPT handles multi-omic data (scRNA-seq + scATAC-seq) through its flexible gene token framework

## References Worth Chasing

1. **Geneformer** (Theodoris et al. 2023, Nature): Another single-cell FM using rank-value encoding; key comparison point for cell-level transfer learning
2. **scBERT** (Yang et al. 2022, Nature Machine Intelligence): BERT-style masked LM for cell type annotation on scRNA-seq; direct competitor with different masking approach
3. **scVI** (Lopez et al. 2018, Nature Methods): Variational inference framework for scRNA-seq; standard baseline for batch integration
4. **Attention Is All You Need** (Vaswani et al. 2017, NeurIPS): Transformer architecture foundation
5. **GPT-3 / GPT-4** (Brown et al. 2020; OpenAI 2023): Generative pretraining inspiration
6. **Enformer** (Avsec et al. 2021, Nature Methods): Genomic sequence → expression prediction; different modality but related transfer learning idea
7. **scGen** (Lotfollahi et al. 2019, Nature Methods): Perturbation response prediction baseline
8. **CPA** (Lotfollahi et al. 2023, Molecular Systems Biology): Compositional perturbation autoencoder; perturbation prediction baseline
9. **scGLUE** (Cao & Gao 2022, Nature Biotechnology): Graph-linked embedding for multi-omic integration; key competitor
10. **scMoMat** (Zhang et al. 2023, Nature Communications): Mosaic integration baseline

## Notes / Open Questions

- Despite the "GPT" name, the architecture uses `TransformerEncoder` (bidirectional), not a causal decoder. The "generative" aspect is entirely in the attention masking strategy during pretraining, not in the architecture itself
- The 51M parameter count is modest by LLM standards; no scaling experiments reported (e.g., larger d_model, more layers)
- Training compute is not reported in the paper or repo
- The value binning approach (51 bins) is a crude discretization of continuous expression; unclear how sensitive results are to bin count
- Gene ordering by expression creates a strong inductive bias; unclear how this interacts with dropout zeros vs. true biological zeros
- The pretraining code with generative attention masking was listed on the GitHub TODO but the full pretraining pipeline details are limited in the public repo
- Max sequence length limited by HVG selection (~1,200–2,000 genes out of ~20K); not truly genome-wide
- Code: https://github.com/bowang-lab/scGPT | Docs: https://scgpt.readthedocs.io | PyPI: `pip install scgpt`
- Pretrained weights: Available via Google Drive links in the repo (not on HuggingFace Hub as of last check, though HuggingFace integration branch exists)

## Verification (Rev 3)

Sources: note front-matter & body, `papers/md/scgpt-toward-building-a-2024.md` (abstract only — no body text), GitHub README (bowang-lab/scGPT, fetched live).

| # | insights.md line | Claim (paraphrased) | Verdict | Rationale |
|---|---|---|---|---|
| 1 | 12 | Expression-binning [scGPT] outperforms naïve count vectors | **partial** | 51-bin discretization confirmed (note §Model, §Data). However, no specific ablation of binning-vs-raw-counts is reported; "outperforms naïve count vectors" is an editorial inference from overall model performance. |
| 2 | 80 | scGPT uses finer 51-bin value discretization, sorts genes by expression level, applies generative attention masking | **supported** | All three sub-claims directly confirmed: 51-bin CategoryValueEncoder (note §Model), gene ordering by expression (note §Key Ablations #1), generative attention masking (note §Model, §Training Recipe). |
| 3 | 166 | scGPT applies a modified autoregressive objective with generative attention masking where genes are sorted by expression | **supported** | Note §Model: "custom attention mask … orders genes by expression value, allowing each gene to attend only to genes with higher expression—mimicking autoregressive factorization." Note §Training Recipe confirms. |
| 4 | 185 | scGPT adds MVC (masked value classification), ECS (elastic cell similarity), and DAB (domain-adaptive batching) fine-tuning objectives | **partial** | MVC, ECS, DAB confirmed as fine-tuning objectives (note §Training Recipe). Two acronym expansions are wrong: MVC = masked value **prediction** (not classification; note §Model: "MVCDecoder for masked value prediction conditioned on cell embedding"); DAB = domain-**adversarial** batch correction (not "domain-adaptive batching"; note: "AdversarialDiscriminator with gradient reversal"). |
| 5 | 237 | scGPT uses 33 M cells | **supported** | Note front-matter: "33M cells from CELLxGENE Census (human normal)." GitHub README: "Pretrained on 33 million normal human cells." |
| 6 | 509 | scGPT (~51 M): 51-bin value discretization, generative masking, MVC/ECS/DAB fine-tuning, 33 M cells | **supported** | Every sub-claim confirmed: ~51 M params (note §Model), 51-bin (note §Data), generative masking (note §Training Recipe), MVC/ECS/DAB (note §Training Recipe), 33 M cells (note §Data, GitHub). Acronym expansions are not spelled out here, so the mis-expansion issue from claim 4 does not apply. |
