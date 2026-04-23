---
id: the-nucleotide-transformer-building-2024
title: 'The Nucleotide Transformer: Building and Evaluating Robust Foundation Models
  for Human Genomics'
authors: []
year: 2024
venue: Nature Methods
arxiv: null
doi: 10.1038/s41592-024-02523-z
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/the-nucleotide-transformer-building-2024.md
modalities:
- dna
status: extracted
evidence_quality: full-text
tags:
- encoder-only
- BERT
- MLM
- k-mer
- 6-mer-tokenization
- multi-species
- scaling
- parameter-efficient-fine-tuning
- IA3
- zero-shot-variant-scoring
- rotary-embeddings
- genomics-benchmark
parameters: 50M/100M/250M/500M/2.5B
training_tokens: 50B–1T (model-dependent; v1-500M 50B, v1-2.5B 300B, v2-50M/100M 300B,
  v2-250M 800B, v2-500M 900B)
training_compute: 128×A100 for 28 days (v1 2.5B); 8×A100 for 1 day (v1/v2 ≤500M)
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'Nucleotide Transformer: family of pretrained genomic FMs.'
---

## TL;DR

Family of BERT-style encoder-only DNA transformers (50M–2.5B params) pre-trained with 6-mer masked language modelling on human-reference, 1000 Genomes multi-individual, and 850-species multispecies datasets. Multispecies 2.5B is the best v1 model. NT-v2 adds RoPE, SwiGLU, removes bias/dropout, doubles context to 12 kb; the v2-250M matches or beats the 2.5B with 10× fewer parameters. Evaluated on a curated 18-task benchmark; parameter-efficient fine-tuning (IA3, 0.1% params) consistently outperforms extensive probing. Zero-shot embedding distances score variant pathogenicity without any labelled data.

## Model

| Attribute | v1 | v2 |
|---|---|---|
| Architecture | Encoder-only transformer (BERT) | Same, with architectural improvements |
| Sizes | 500M, 2.5B | 50M, 100M, 250M, 500M |
| Tokenization | 6-mer (vocab 4,104: 4,096 6-mers + 5 single-nt + 3 special) | Same |
| Positional encoding | Learned, max 1,000 tokens | Rotary (RoPE), per attention layer |
| Context length | 6 kb (1,000 tokens) | 12 kb (2,048 tokens) |
| Activations | GELU in MLP | SwiGLU (gated linear units + swish) |
| Biases / dropout | Present | Removed |
| Objective | MLM — 15% masking (80% [MASK], 10% random, 10% unchanged) | Same |
| Loss | Cross-entropy at masked positions | Same |
| Optimizer | Adam (β₁=0.9, β₂=0.999, ε=1e-8), warmup 16k steps → sqrt decay | Same schedule; batch size increased to 512 |

Effective batch size throughout: ~1 M tokens per step.

## Data

Three pre-training corpora:

1. **Human reference genome** (GRCh38/hg38) — 3.2 B nucleotides.
2. **1000 Genomes (1000G)** — 3,202 phased human genomes from 27 populations; 20.5 T nucleotides total; 125 M mutations (111 M SNPs, 14 M indels). Mutations are injected on-the-fly by sampling a random individual per chunk.
3. **Multispecies** — 850 species across diverse phyla (archaea, fungi, mammals, vertebrates, invertebrates, bacteria subset; no plants/viruses); 174 B nucleotides. Includes 11 model organisms.

Sequences are split into overlapping 6,100-nt chunks (50-nt overlap). A random start offset (0–100) is applied per epoch as data augmentation.

**Downstream benchmark**: 18 curated tasks — 10 histone marks (K562, ENCODE), 3 promoter tasks (EPD), 2 enhancer tasks (ENCODE SCREEN), 3 splice-site tasks (GENCODE v44). Balanced, small-sized (≤30k train, ≤3k test), 10-fold cross-validation. MCC as primary metric.

## Training Recipe

- **Hardware**: Cambridge-1 Nvidia supercomputer.
- **v1 2.5B**: 16 nodes × 8 A100 = 128 GPUs, 28 days, 300 B tokens.
- **v1 500M**: 1 node (8 GPUs), 1 day, 50 B tokens.
- **v2 50M/100M**: 1 node, 1 day, 300 B tokens.
- **v2 250M/500M**: 1 node, trained up to 1 T tokens (Chinchilla-inspired); best checkpoints at 800 B and 900 B tokens respectively.
- **Fine-tuning**: 1 node (8 A100s); ~20 min for 500M, ~50 min for 2.5B. IA3 parameter-efficient method — only 0.1% of model params are trainable.
- **Probing**: embeddings precomputed on 8 GPUs (2 days), then 760 k downstream models fitted on 3,000 CPUs (2.5 days).
- Framework: JAX with pmap / NCCL.

## Key Ablations & Design Choices

### Scaling (model size & tokens)

- Larger models consistently outperform smaller ones on 18-task benchmark.
- v2-50M matches v1-500M → **50× parameter reduction** with better architecture + data.
- v2-250M achieves best overall performance (avg MCC 0.769), beating v1-2.5B with **10× fewer params**.
- Longer training matters: v2-250M overtakes v2-500M only after 900 B tokens, showing diminishing returns require patience.

### Species coverage vs. intra-species diversity

- **Multispecies 2.5B > 1000G 2.5B** on most human-derived tasks — diverse cross-species sequences teach conserved functional elements.
- 1000G (intra-species diversity) gave limited gains over the single human reference genome, suggesting naïvely mixing nearly-identical human haplotypes is suboptimal.
- **Task-dependent best model**: multispecies best for pathogenic variant prioritization (ClinVar AUC 0.80); human-trained models best for eQTL/meQTL scoring.

### Fine-tuning vs. probing

- IA3 fine-tuning matched or outperformed baseline BPNet in 18/18 tasks (matched 6, exceeded 12).
- IA3 outperformed exhaustive probing while using **fewer compute resources**.
- Best probing layer is model- and task-dependent; **never the final layer**; up to 38% relative MCC gap between best and worst layer.
- Full fine-tuning (all params) adds only ~3% over IA3 for enhancer activity; negligible for chromatin/splicing.
- Fine-tuning exhibits lower variance → more robust.

### Tokenization

- 6-mer chosen as trade-off between sequence length and embedding granularity; reported as achieving highest performance vs. other k values (details in supplementary).

## Reported Insights

- **Unsupervised genomic element detection**: attention heads specialise on exons (72 significant heads in Multispecies 2.5B), introns (117), TF binding sites (74), enhancers, promoters. Embeddings separate intergenic/intronic/coding/UTR regions without labels.
- **Token reconstruction** across chr22 recovers splice donor/acceptor sites, polyA signals, CTCF binding sites. Correlates with experimental saturation mutagenesis of MST1R exon 11 (PCC = 0.44).
- **Zero-shot variant scoring**: cosine similarity in embedding space correlates with variant severity (r² ≈ −0.30 to −0.35, P < 6.55 × 10⁻¹⁸⁶). ClinVar pathogenic variant AUC = 0.80; eQTL/meQTL AUC 0.70–0.73.
- **Supervised baselines comparison**: Multispecies 2.5B closely matches DeepSEA (−1% avg AUC), matches SpliceAI-10k at 6 kb context, close to DeepSTARR (−4% developmental, +1% housekeeping enhancer correlation). v2-500M at 12 kb surpasses SpliceAI-10k (top-k accuracy 96%).
- **TF motif mutagenesis**: fine-tuned model predicts experimental TF motif mutation effects comparably to DeepSTARR; superior for Dref motif.

## References Worth Chasing

- **IA3 parameter-efficient fine-tuning**: ref [35] (Liu et al.) — enables 0.1% trainable params.
- **Chinchilla scaling laws**: ref [45] (Hoffmann et al.) — motivation for extended v2 training schedules.
- **DNABERT-2**: ref [23] — BPE tokenization alternative; 117M params.
- **HyenaDNA**: ref [25] — single-nucleotide tokenization, long context (up to 1M bp).
- **Enformer**: ref [19] — 200 kb context, conv+transformer, supervised pre-training on gene expression.
- **BPNet**: ref [9] — strong supervised convolutional baseline (121k–28M params).
- **DeepSEA**: ref [10] — 919 chromatin profile prediction benchmark.
- **SpliceAI**: ref [36] — state-of-the-art splice site prediction; 15 kb input.
- **DeepSTARR**: ref [12] — enhancer activity prediction benchmark.
- **Protein LM precedents**: ESM refs [3–5] — inspired DNA MLM approach.

## Notes / Open Questions

- Context length remains limited (6–12 kb) vs. Enformer's 200 kb needed for distal regulatory elements. Quadratic attention cost is the bottleneck; paper flags this as key future direction.
- HyenaDNA long-context models (32 kb+) degrade on the benchmark — why? Is there a sweet spot between context length and representation quality?
- 1000G intra-species diversity gave surprisingly little benefit. The on-the-fly mutation injection strategy may be insufficient; better haplotype encoding could help.
- No multi-omics or protein-level integration — DNA sequences only.
- Supplementary Tables 1–12 contain detailed per-model architecture specs, per-task breakdowns, and attention analysis (not fully available in PMC text).
- Interactive leaderboard: https://huggingface.co/spaces/InstaDeepAI/nucleotide_transformer_benchmark
- Code and models available on HuggingFace (InstaDeepAI org).

## Verification (Rev 3)

Eight claims referencing `[the-nucleotide-transformer-building-2024]` were found in `insights.md`. Each is judged against the PMC full text below.

| # | insights.md line | Claim (paraphrased) | Verdict | Rationale |
|---|---|---|---|---|
| 1 | L42 | IA3 tuning (0.1 % params) matches full fine-tuning | **supported** | Paper: "no significant improvement in chromatin and splicing predictions, and only a modest 3 % enhancement in enhancer activity predictions" with full fine-tuning vs IA3 (§Results, ¶ additional tasks). 0.1 % figure confirmed in Methods §Fine-tuning. |
| 2 | L60 | NT adopted non-overlapping 6-mers across multi-species genomes | **supported** | Tokenizer is greedy left-to-right 6-mer (Methods §Data preparation): "convert the sequence starting from the left, matching six-mer tokens when possible." Multispecies dataset confirmed (850 species, 174 B nt). |
| 3 | L206 | NT context = "12 k 6-mers ≈ 72 k nt"; positional encoding = "Learned positional embeddings" | **unsupported** | Context is 2,048 tokens (v2) ≈ 12 kb, NOT 12 k 6-mers (which would be ≈72 k nt). v1 max is 1,000 tokens ≈ 6 kb. Positional encoding is learned for v1 only; v2 uses rotary embeddings (RoPE). Both sub-claims are wrong for v2. |
| 4 | L225 | NT trained on multi-species genomes totalling 3.2 B nucleotides, 850 genomes | **unsupported** | 3.2 B nt is the **human reference genome** size (Methods §Human reference dataset). The multispecies corpus is 850 species / **174 B** nucleotides (Methods §Multispecies dataset). The claim conflates two different datasets. |
| 5 | L270 | NT uses learned positional embeddings at the 6-mer level | **partial** | True for v1 ("learnable positional encoding layer that accepts a maximum of 1,000 tokens"). v2 replaced these with rotary embeddings (RoPE) applied at each attention layer (Methods §Architecture). Claim omits the v1/v2 distinction. |
| 6 | L303 | v2-250 M matches v1-2.5 B at 10× fewer params "through distillation" and IA3 | **partial** | 10× reduction and IA3 (0.1 % params) are correct. However, the paper never mentions distillation. The gain came from architectural improvements (RoPE, SwiGLU, no bias/dropout) plus extended training (800 B tokens). "Distillation" is fabricated. |
| 7 | L368 | NT achieves competitive zero-shot variant scoring from 6-mer representations | **supported** | Paper reports zero-shot AUCs 0.70–0.80 across eQTL/meQTL/ClinVar/HGMD; cosine similarity r² −0.30 to −0.35 with variant severity (P < 6.55 × 10⁻¹⁸⁶). Described as "competitive" with supervised methods. |
| 8 | L393 | "The distilled v2-250 M matches v1-2.5 B, and IA3 … matches full fine-tuning" | **partial** | Same distillation error as #6 — v2-250 M was trained from scratch, not distilled. IA3 ≈ full fine-tuning is correct (see #1). |

**Summary**: 3 supported, 3 partial, 2 unsupported. Key recurring errors: (a) the word "distillation" is used but never appears in the paper — v2 gains come from architecture + longer training; (b) the multispecies dataset size is 174 B nt, not 3.2 B nt; (c) the context-length table entry overstates by ~6× and misattributes the positional encoding scheme.

## Ablations (Rev 4)
| Variable | Settings | Metric / dataset | Result | Conclusion |
|---|---|---|---|---|
| Pre-training dataset | Human ref vs 1000G (3,202 human) vs Multispecies (850 species) | Avg MCC over 18 downstream tasks (fine-tuned) | Multispecies 2.5B matches/outperforms 1000G 2.5B on most human-derived tasks; both beat Human ref 500M | Sequence diversity beats raw human-only data; diversity > size when compute-limited |
| Model size (NT-v1) | 500M (Human ref, 1000G) vs 2.5B (1000G, Multispecies) | Avg MCC over 18 tasks | Larger consistently > smaller within same dataset; 2.5B Multispecies best of v1 | Scale helps, but pairing with diverse pretraining data matters as much |
| Adaptation strategy | Probing (10 layers × LR/MLP) vs IA³ parameter-efficient fine-tuning | # of 18 tasks ≥ BPNet baseline | Probing matched/beat 13/18; fine-tuning matched/beat 18/18 | Fine-tuning required for top performance; also lower variance than probing |
| Probing layer choice | All layers of NT models | Best vs worst layer MCC (e.g., enhancer-types task) | Up to 38% relative gap; final layer never optimal | Embedding quality is layer-dependent; mid/late-but-not-final layers best |
| IA³ vs full fine-tuning | 0.1% params (IA³) vs 100% params | Chromatin (DeepSEA), splicing (SpliceAI), enhancer (DeepSTARR) (Supp Fig 2) | No significant gain on chromatin/splicing; +3% on enhancer activity | IA³ is sufficient; ~1000× storage savings with negligible performance cost |
| Architecture upgrades (NT-v2) | +RoPE, +SwiGLU, −MLP biases, −dropout, 12 kb context, 1T tokens | Avg MCC over 18 tasks | 50M v2 ≈ 500M v1 and 1000G 2.5B v1; 250M v2 = 0.769 (best, 10× smaller than 2.5B) | Modern transformer recipe + longer training yields ≥50× parameter efficiency |
| Pre-training token budget (NT-v2) | Up to 1T tokens (250M & 500M) | Avg MCC vs tokens seen (Fig 5b) | 250M only surpasses 500M after ~900B tokens | Longer training disproportionately helps smaller models; token budget matters more than parameter count past a point |
| Context length (downstream) | NT 2.5B (6 kb) vs SpliceAI-10k (15 kb) | Splice site top-k acc / PR-AUC | NT matches SpliceAI-10k overall; beats SpliceAI when both restricted to 6 kb input | Pretraining can compensate for shorter context vs supervised long-context baseline |
| Zero-shot variant score type | Cosine sim, dot-product, L1, L2, loss-based | Correlation w/ Ensembl severity; AUC on eQTL/meQTL/ClinVar/HGMD | Cosine: highest severity corr (r² −0.30 to −0.35, P<6.55e-186); dot-product: AUC 0.73 (eQTL) / 0.71 (meQTL), ≈ fine-tuned | Score choice materially changes utility; dot-product competitive with fine-tuning for QTL prioritization |

**Design-choice take-aways:**
- Pretraining-data diversity (multispecies) gives more bang-per-parameter than scaling on a single-species corpus.
- A modern transformer recipe (RoPE + SwiGLU + no-bias/dropout) plus a larger token budget beats raw parameter count by ~10–50×.
- Parameter-efficient fine-tuning (IA³, 0.1% params) is sufficient — full fine-tuning rarely justifies its compute/storage cost.
- Always probe multiple intermediate layers; the final layer is consistently suboptimal.
- For variant prioritization, score selection (cosine vs dot-product) matters as much as fine-tuning.
