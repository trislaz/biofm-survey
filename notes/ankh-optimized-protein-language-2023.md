---
id: ankh-optimized-protein-language-2023
title: 'Ankh: Optimized Protein Language Model Unlocks General-Purpose Modelling'
authors:
- Ahmed Elnaggar
- Hazem Essam
- Wafaa Salah-Eldin
- Walid Moustafa
- Mohamed Elkerdawy
- Charlotte Rochereau
- Burkhard Rost
year: 2023
venue: null
arxiv: '2301.06568'
doi: null
url: https://arxiv.org/abs/2301.06568v1
pdf_path: papers/ankh-optimized-protein-language-2023.pdf
md_path: papers/md/ankh-optimized-protein-language-2023.md
modalities:
- protein-sequence
status: extracted
evidence_quality: full-text
tags:
- encoder-decoder
- T5-architecture
- protein-language-model
- masking-ablation
- knowledge-guided-optimization
- TPU-v4
- Flax-JAX
- protein-variant-generation
- embedding-transfer
- computational-efficiency
parameters: null
training_tokens: 14000000000
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:59+00:00'
updated_at: '2026-04-22T20:17:11+00:00'
---

## TL;DR

Ankh is a T5-based encoder-decoder protein language model that achieves SOTA on a broad suite of structure and function benchmarks with <10% of the pre-training parameters and <30% of the embedding dimension of ESM-2 (15B). The paper's core contribution is a systematic ablation of 23 experiments across masking strategy, masking probability, encoder-decoder layer ratio, depth-vs-width, activation function, relative positional embeddings, weight tying, and pre-training dataset. Two models are released: Ankh large (emb 1536, 48-enc/24-dec) and Ankh base (emb 768, 48-enc/24-dec). Average downstream improvement over prior SOTA is +4.8% (large) / +3.4% (base). The paper also demonstrates auto-regressive fine-tuning for family-based protein variant generation and MLM-based one-shot generation.

## Model

- **Architecture**: Encoder-decoder transformer (T5-style) with Gated-GELU activation.
- **Ankh large**: embedding dim 1536, 16 attention heads, 3840 FF dim, 48 encoder + 24 decoder layers, relative positional embedding with offset 128 and dim 64.
- **Ankh base**: embedding dim 768, 12 attention heads, 3072 FF dim, 48 encoder + 24 decoder layers, same positional embedding.
- Exact parameter counts not stated; described as <10% of ESM-2 (15B) for pre-training and <7% for inference (encoder-only). Embedding dim is <30% of ESM-2 (15B)'s 5120.
- Masking: 1-gram span partial de-masking at 20% masking probability — consecutive unmasked tokens merged into a single target token.
- Downstream model: ConvBERT layer → linear layer, using last-hidden-state embeddings (not attention maps). Global max pooling for protein-level tasks.
- Pre-trained in Flax/JAX; released on HuggingFace for JAX/TF/PyTorch.

## Data

- **Pre-training**: UniRef50 (45M proteins, 14B residues, 16 GB). Tokenized character-level with single-space delimiters. Chosen over UniRef90 (144M proteins, 49B residues) and UniRef100 (216M proteins, 88B residues) based on ProtTrans results showing higher-quality, lower-redundancy data is superior.
- **Downstream benchmarks** (7 tasks): SSP (NetSurfP-2.0; test on CB513, TS115, CASP12, CASP14), Contact Prediction (ProteinNet CASP12 + CASP14 FM), Fold Prediction (DeepSF, 1194 folds), Fluorescence Prediction (TAPE split of Sarkisyan), Solubility Prediction (DeepSol), GB1 Fitness Prediction (FLIP), Localization Prediction (DeepLoc, 10 classes), Embedding-based Annotation Transfer (EAT; CATH v4.3).
- **Generation**: MDH family (16,706 sequences from ProteinGAN dataset) for High-N; SARS-CoV-2 nanobodies from CoV-AbDab (post-June 2022) for One-N.

## Training Recipe

- **Optimizer**: Adafactor with linear scheduler, warm-up 10k steps, no weight decay.
- **Learning rate**: 0.002 (large), 0.004 (base); baseline experiments used 0.01.
- **Batch size**: global 1024 (large) / 1536 (base); local 16 (large) / 24 (base).
- **Epochs**: 68 for both final models (ablation experiments used 2 epochs each). Total tokens seen ≈ 68 × 14B = ~952B.
- **Max length**: 512 tokens during pre-training.
- **Hardware**: Google TPU v4-128 pods (128 cores; each host: 8 cores, 16 GiB HBM per core, 120 CPU cores, 400 GB RAM). TPU v4 delivers ~2.2× speedup vs v3. JAX provides ~1.4× speedup vs PyTorch on TPU pods.
- **Downstream**: AdamW optimizer, lr 0.001, 5 epochs, batch 16, on single A100 GPU. ConvBERT top model with 4 attention heads, dropout 0.2, kernel size 7.
- **Generation fine-tuning**: Encoder frozen, decoder fine-tuned for 2 epochs, lr 3e-4, Adam (eps 1e-8), beam search (10 beams), temperature logit warping.

## Key Ablations & Design Choices

All ablation experiments trained for 2 epochs on UniRef50 with ~same total parameter count. Metrics: SSP (Q3/Q8 on CASP12, TS115, CB513), Contact Prediction (L/1, L/5), Subcellular Localization, Fold Prediction, plus Avg and Median across all tasks.

### 1. Masking Strategy (Exps 0–6, Table 3)
- **Baseline (Exp 0)**: Random 15% token masking, full sequence reconstruction. Avg 64.0%, Med 68.9%.
- **Exp 1** (mask every unique 1-gram at least once, full reconstruction): Avg 65.0%, Med 69.9%.
- **Exp 2** (3-gram token masking + full reconstruction): performance dropped across all tasks. Avg 58.1%.
- **Exp 3** (mask unique 1-grams, reconstruct only masked tokens): worst performer. Avg 56.1%.
- **Exp 4** ★ (1-gram span partial de-masking — merge consecutive unmasked tokens into single target): **best**. Avg 67.9%, Med 71.8%. +3.9 pp over baseline.
- **Exp 5** (Exp 1 + span partial de-masking): reduced performance. Avg 63.5%.
- **Exp 6** (merge consecutive masked tokens into single target): Avg 65.4%, not proceeded with.
- **Insight**: Reconstructing unmasked tokens as merged spans reduces computational cost and improves representations. Partial de-masking on the output side is critical; on the input side, token identity must be preserved.

### 2. Masking Probability (Exps 7–9, Table 4)
Starting from Exp 4 (1-gram span partial de-masking):
- **10% (Exp 7)**: worst. Avg 66.7%.
- **15% (Exp 4, default)**: best on LocP, FolP, some SSP datasets. Avg 67.9%.
- **20% (Exp 8)** ★: chosen as compromise. Avg 67.1%. Slightly lower than 15% but more balanced.
- **30% (Exp 9)**: best on all contact prediction tasks + CASP12 SSP. Avg 67.0%.
- **Insight**: 20% selected for generalization across diverse tasks despite not being numerically top on every individual task. Task-specific tuning of masking probability could help.

### 3. Encoder-Decoder Layer Ratio (Exps 10–12, Table 5)
Total 72 layers fixed; varying enc/dec split from Exp 8:
- **54-enc / 18-dec (Exp 10)**: Avg 67.7%. Best on CP L/5 (39.5%).
- **48-enc / 24-dec (Exp 11)** ★: Avg 67.8%, Med 72.3%. Best on SSP Q8, FolP, LocP.
- **24-enc / 48-dec (Exp 12)**: Avg 66.8%. Worst overall.
- **Insight**: Larger encoder extracts richer embeddings; retaining adequate decoder layers matters for generation tasks. 2:1 ratio enc:dec chosen for balance.

### 4. Depth vs. Width (Exp 13, Table 6)
- **Exp 13**: embedding dim 768→1024, layers 48/24→24/12 (keeping ~same params). Avg 67.4%, fluctuating results.
- Not proceeded with. Ankh base defined as the 768-dim variant.
- **Insight**: Simply trading depth for width without activation function change is not beneficial.

### 5. Activation Function (Exps 14–15, Table 7)
Tested replacing Gated-GELU with ReLU (enables deeper models due to fewer params per layer):
- **Exp 14** (ReLU, 62-enc/11-dec, dim 768): Avg 65.3%.
- **Exp 15** (ReLU, 48-enc/24-dec, dim 768): Avg 66.3%.
- **Gated-GELU (Exp 11)**: Avg 67.8%.
- **Insight**: Gated-GELU consistently superior despite forcing shallower architectures to stay within parameter budget. +1.5–2.5 pp over ReLU alternatives.

### 6. Relative Positional Embedding (Exps 16–21, Table 8)
Varying embedding offset and embedding dimension from Exp 11 (offset=128, dim=32):
- **Exp 16** (offset=256, dim=32): Avg 67.7%.
- **Exp 17** (offset=64, dim=32): Avg 68.2%. Smaller offset helps.
- **Exp 18** (offset=64, dim=64): Avg 63.7% (but note FolP drop to 48.4%).
- **Exp 19** (offset=64, dim=16): Avg 67.8%.
- **Exp 20** ★ (offset=128, dim=64): **best**. Avg 68.6%, Med 72.2%. FolP 51.8% (best across all experiments).
- **Exp 21** (offset=256, dim=128): Avg 67.8%. CP best (L/1 25.2%, L/5 41.3%) but inconsistent.
- **Insight**: Doubling the embedding dimension to 64 with offset 128 gives best generalization. Ankh large doubles embedding dim to 1536 based on this "doubles are better" pattern.

### 7. Weight Tying (Exp 22, Table 9)
- **Exp 22** (tied embedding + decoder weights): Avg 67.6% vs Exp 20's 68.6%.
- Not proceeded with. Input-output type mismatch (due to span masking/de-masking) makes tying counterproductive.

### 8. Pre-training Dataset (Exp 23, Table 10)
- **UniRef90 (Exp 23, 1 epoch)**: Avg 67.2%.
- **UniRef50 (Exp 20, 2 epochs)** ★: Avg 68.6%.
- **Insight**: Higher-quality, lower-redundancy UniRef50 remains superior. Note: UniRef90 trained 1 epoch vs UniRef50's 2 epochs (argued as roughly equivalent in tokens seen).

### Final Model Benchmarks (Table 1)
| Task | Ankh large | Ankh base | ProtT5 | ESM-2(15B) |
|------|-----------|-----------|--------|------------|
| SSP CASP12 (Q3) | 83.8% | 80.8% | 83.4% | 83.2% |
| SSP CASP14 (Q3) | 77.6% | 76.8% | 74.1% | 76.8% |
| CP ProteinNet L/1 | 49.0% | 43.2% | 44.7% | 33.3% |
| CP CASP14 L/1 | 30.2% | 28.8% | 26.9% | 25.9% |
| EAT | 71.7% | 74.8% | 71.0% | 65.4% |
| FolP | 61.1% | 58.8% | 57.6% | 56.7% |
| FluP (Spearman) | 0.62 | 0.61 | 0.58 | 0.55 |
| SolP | 76.4% | 74.2% | 74.4% | 60.4% |
| GB1P (Spearman) | 0.84 | 0.85 | 0.78 | 0.57 |
| LocP | 83.2% | 81.4% | 83.2% | 81.8% |
| **Avg** | **71.4%** | **70.0%** | **69.3%** | **66.6%** |

Embedding-based predictions consistently outperform attention-based predictions for contact prediction across all models, contradicting ESM family findings.

## Reported Insights

- **Bigger ≠ better**: ESM-2 (15B) did not outperform smaller ESM family models on all tasks and showed inconsistent results across runs. Ankh surpasses it with ~10× fewer parameters.
- **Data quality > data quantity**: UniRef50 (45M seqs) outperforms UniRef90 (144M seqs) due to lower redundancy and higher diversity per cluster.
- **Embeddings > attention maps**: Contextualized embeddings from the last hidden layer are superior to attention maps for contact prediction, even for ESM models where attention was previously reported as the better indicator.
- **Partial de-masking**: Reconstructing only non-trivial (masked) output tokens while merging unmasked spans reduces compute and improves representation quality.
- **Encoder-heavy architecture**: A 2:1 encoder-to-decoder ratio yields richer embeddings while preserving generation capability.
- **Generation**: Auto-regressive fine-tuning (encoder frozen, decoder fine-tuned) enables family-based variant generation. Temperature controls exploration-exploitation: t=1.0 is conservative, t=2.0 introduces more diversity including rare functional families. MSE of Shannon entropy between generated and natural sets: 0.1, 0.09, 0.08 for t=1.0, 1.5, 2.0.
- **One-shot generation**: MLM with 40–50% masking probability generates structurally similar variants (RMSD <1.5Å) with sequence identity as low as 80%. 50% masking shows steeper negative Pearson correlation (more sequence context → better structural preservation).
- **Gated-GELU worth the parameter cost**: Despite requiring shallower models to stay within parameter budget, Gated-GELU consistently outperforms ReLU by 1.5–2.5 pp.

## References Worth Chasing

- ProtTrans: Towards Cracking the Language of Life's Code (arXiv:2007.06225) — basis for Ankh's design decisions; T5 encoder-decoder shown superior to encoder-only and decoder-only PLMs
- Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250M Protein Sequences (doi:10.1073/pnas.2016239118) — ESM-1b, 650M param PLM, key baseline
- Language Models of Protein Sequences at the Scale of Evolution Enable Accurate Structure Prediction (bioRxiv, Lin et al. 2022) — ESM-2 family up to 15B, main scaling competitor
- RITA: A Study on Scaling Up Generative Protein Sequence Models (arXiv:2205.05789) — scaling laws for autoregressive PLMs, 85M–1.2B
- ProGen2: Exploring the Boundaries of Protein Language Models (arXiv:2206.13517) — suite of PLMs up to 6.4B, scaling baseline
- ProGen: Language Modeling for Protein Generation (arXiv:2004.03497) — early autoregressive protein generation
- BERTology Meets Biology: Interpreting Attention in Protein Language Models (arXiv:2006.15222) — attention interpretability in PLMs
- Transformer Protein Language Models Are Unsupervised Structure Learners (Rao et al., bioRxiv 2020) — attention-based contact prediction (contradicted by Ankh's embedding results)
- Evaluating Protein Transfer Learning with TAPE (NeurIPS 2019) — standard benchmark used in Ankh evaluation
- PEER: A Comprehensive and Multi-Task Benchmark for Protein Sequence Understanding (arXiv:2206.02096) — comprehensive PLM benchmark
- FLIP: Benchmark Tasks in Fitness Landscape Inference for Proteins (bioRxiv 2021) — fitness prediction benchmark (GB1 task)
- Expanding Functional Protein Sequence Spaces Using Generative Adversarial Networks (Nature MI, 2021) — ProteinGAN, generation baseline for MDH
- Modeling Aspects of the Language of Life Through Transfer-Learning Protein Sequences (BMC Bioinf, 2019) — early PLM transfer learning
- Exploring the Limits of Transfer Learning with a Unified Text-to-Text Transformer (JMLR 2020) — T5 architecture foundation
- ColabFold: Making Protein Folding Accessible to All (Nature Methods 2022) — structure prediction tool used for generation evaluation

## Notes / Open Questions

- **No explicit parameter count reported**: Paper only provides relative comparisons (<10% of ESM-2 15B for training, <7% for inference). From architecture specs, Ankh large is roughly ~1–1.5B total parameters (estimated).
- **Training compute not reported**: TPU v4-128 pods used, but total wall-clock time and FLOPs not disclosed.
- **Ablation limitation**: Changing activation function also changes the viable depth/width trade-off. The paper acknowledges that Gated-GELU's higher parameter demand prevented testing some depth/width combos, creating a confound between activation and architecture ablations.
- **No ablation on vocabulary/tokenization**: Character-level tokenization with 25 amino acids was fixed; no BPE or other tokenization strategies explored.
- **Two-epoch ablation training**: All design decisions made after only 2 epochs of training. It is unclear whether rankings would hold after longer training (the final models trained for 68 epochs).
- **Downstream evaluation uses unified settings**: While this enables fair comparison, it likely underestimates all models' potential with task-specific tuning.
- **No comparison with AlphaFold or MSA-based methods**: Evaluation is purely single-sequence PLM comparison.
- **Generation evaluation is qualitative-heavy**: Shannon entropy MSE, CATH domain counts, and visual RMSD plots, but no standard generation metrics (perplexity, FID-equivalent, etc.).
