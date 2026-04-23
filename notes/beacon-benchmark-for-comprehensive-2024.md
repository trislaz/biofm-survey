---
id: beacon-benchmark-for-comprehensive-2024
title: 'BEACON: Benchmark for Comprehensive RNA Tasks and Language Models'
authors:
- Yuchen Ren
- Zhiyuan Chen
- Lifeng Qiao
- Hongtai Jing
- Yuchen Cai
- Sheng Xu
- Peng Ye
- Xinzhu Ma
- Siqi Sun
- Hongliang Yan
- Dong Yuan
- Wanli Ouyang
- Xihui Liu
year: 2024
venue: null
arxiv: '2406.10391'
doi: null
url: https://arxiv.org/abs/2406.10391v2
pdf_path: papers/beacon-benchmark-for-comprehensive-2024.pdf
md_path: papers/md/beacon-benchmark-for-comprehensive-2024.md
modalities:
- rna
status: extracted
evidence_quality: full-text
tags:
- benchmark
- rna-language-model
- tokenization
- positional-encoding
- ablation
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:49+00:00'
updated_at: '2026-04-22T20:17:26+00:00'
is_fm: false
fm_classification_reason: BEACON benchmark, not a model.
---

## TL;DR

BEACON is the first comprehensive RNA benchmark, spanning 13 tasks (structure, function, engineering) with 967k sequences. It systematically evaluates 6 pre-trained RNA language models plus CNN/ResNet/LSTM baselines, and ablates tokenizer × positional-encoding choices. Key findings: single-nucleotide tokenization dominates all other tokenizers (best on 11/13 tasks); ALiBi positional encoding outperforms RoPE and APE; pre-trained RNA LMs beat prior task-specific SOTAs on 8/13 tasks but LSTM/ResNet remain surprisingly competitive. The authors propose BEACON-B (BERT-base + single-nucleotide + ALiBi, pre-trained on human ncRNA), which matches or beats larger models at a fraction of GPU cost (3.58–10.4 GPU-days vs 56–240).

## Model

BEACON is a benchmark, not a single model. It evaluates:

**Naive supervised baselines (trained from scratch):**
- CNN (2-layer, 5.4M params)
- ResNet (8 res-blocks, 11M params)
- LSTM (3-layer BiLSTM, 26.7M params)

**Pre-trained RNA language models (all BERT-style MLM, fine-tuned):**
| Model | Params | Tokenizer | Pos. Enc. | Pre-training data |
|---|---|---|---|---|
| RNA-FM | 99.5M | Single | APE | 23.7M multi-species ncRNA (RNACentral) |
| RNABERT | 0.48M | Single | APE | 76k human ncRNA (RNACentral) |
| RNA-MSM | 95.9M | Single | APE | Rfam homologous sequences (MSA-style) |
| SpliceBERT-H510 | 19.5M | Single | APE | Human pre-mRNA (UCSC) |
| SpliceBERT-MS510 | 19.5M | Single | APE | Multi-species pre-mRNA |
| SpliceBERT-MS1024 | 19.7M | Single | APE | Multi-species pre-mRNA |
| UTR-LM (×2 variants) | 1.21M | Single | RoPE | Multi-species 5′ UTR |
| 3UTRBERT (3/4/5/6-mer) | 86–98M | K-mer | APE | Human 3′ UTR (GENCODE) |

**Proposed baseline — BEACON-B:**
- Architecture: BERT-base (12 layers)
- Tokenizer: single nucleotide
- Positional encoding: ALiBi
- Pre-training data: 523,934 human ncRNA from RNACentral
- Pre-training: MLM objective, 80k steps, batch 256–512
- BEACON-B: 8×A100 for 1.3 days (10.4 GPU-days); BEACON-B512: 4×A100 for 0.895 days (3.58 GPU-days, with FlashAttention)

## Data

**Benchmark tasks (13 total, 967k sequences, lengths 23–1182 nt):**

*Structure (4 tasks):*
- Secondary Structure Prediction (SSP): bpRNA-1m, 13.4k seqs, F1
- Contact Map Prediction (CMP): 291 seqs from non-redundant RNA 3D structures, Top-L precision
- Distance Map Prediction (DMP): same data as CMP, R²
- Structural Score Imputation (SSI): icSHAPE HEK293, 18.9k fragments, R²

*Function (4 tasks):*
- Splice Site Prediction (SPL): SpliceAI dataset, 179k seqs, Top-k ACC
- APA Isoform Prediction (APA): 228k seqs from Bogard MPRA, R²
- Non-coding RNA Classification (ncRNA): 8.7k seqs, 13 classes (miRNA, lncRNA, etc.), ACC
- Modification Prediction (Modif): 309k sites, 12 RNA modification types, AUC

*Engineering (3 tasks):*
- Vaccine Degradation Prediction (VDP): Stanford OpenVaccine, 3k seqs, MCRMSE
- Programmable RNA Switches (PRS): 91.5k toehold switches, R²
- CRISPR On-Target (CRI-On): 2k sgRNAs, Spearman correlation
- CRISPR Off-Target (CRI-Off): 20.3k sites, Spearman correlation

## Training Recipe

All pre-trained LMs are fully fine-tuned under identical settings for fair comparison. Naive models trained from scratch with similar settings. Learning rate searched in [1e-5, 5e-3]; AdamW optimizer; 30 epochs (100 for structure tasks and VDP); batch size 32; float16. Three random seeds per experiment; mean ± std reported.

Three task pipelines:
1. **Sequence-level**: attentive weighted sum (supervised) or [CLS] token (LMs) → MLP
2. **Nucleotide-level**: per-nucleotide representations (averaged over covering tokens for k-mer/BPE) → MLP
3. **Nucleotide-nucleotide**: outer product of nucleotide representations → ResNet

BEACON-B pre-training: MLM (15% masking, standard BERT recipe), AdamW (lr=2e-4, linear decay, 10k warmup), 80k steps.

## Key Ablations & Design Choices

### Tokenizer comparison (Table 4, Table 17)
Controlled experiment: same BERT architecture trained from scratch, varying tokenizer × positional encoding (12 combinations).
- **Single nucleotide**: best on **11/13 tasks**, massive margins on nucleotide-level tasks (SSP, SPL). Avoids information loss from overlapping/merging.
- **6-mer (overlapping K-mer)**: reasonable on some sequence-level tasks but adds redundancy; degrades nucleotide-level tasks.
- **BPE & Non-overlapping K-mer**: generally ineffective at nucleotide level because they lose per-position precision. BPE scores 0% on splice-site prediction; non-overlap scores 0% on SPL.
- Insight: single nucleotide tokenizer can learn surrounding context via self-attention — explicit local encoding from k-mers is unnecessary and often harmful.

### Positional encoding comparison (Table 4, Table 17)
- **ALiBi**: best positional encoding — top-1 on 7/13 tasks, top-2 on 5 more. Better length generalization due to linear bias on attention scores.
- **APE**: solid second place (top-1 on 5/13). CMP task benefits most.
- **RoPE**: worst overall (top-1 on only 1/13). Hypothesized cause: RNA sequences in the benchmark are short (23–1182 nt), and RoPE's rotational advantage for long sequences is not realized; it can even destabilize training (SSP, MRL collapse to near-zero).

### Pre-training data domain specificity (Table 3)
- Domain-matched pre-training yields strong task-specific gains: RNA-FM (ncRNA) → best ncRNA classification; SpliceBERT (pre-mRNA) → best splice site; 3UTRBERT (3′ UTR) → best APA; UTR-LM (5′ UTR) → strong MRL.
- Cross-domain transfer also occurs: 3UTRBERT also helps 5′ UTR tasks.

### Model scale vs. training efficiency (Table 5, Table 16)
- BEACON-B (BERT-base, 12 layers) achieves competitive or better performance than RNA-FM (99.5M, 240 GPU-days) and 3UTRBERT (86–98M, 152 GPU-days) using only 3.58–10.4 GPU-days.
- Highlights that architecture/tokenizer/PE choices matter more than raw scale for RNA LMs at current sizes.

### Supervised baselines are surprisingly strong
- LSTM outperforms all other naive models on 9/13 tasks and beats many pre-trained LMs.
- ResNet surpasses most/all LMs on some structure tasks (e.g., CMP: 59.6%).
- Pre-trained LMs beat task-specific SOTAs on 8/13 tasks, but there is substantial room for improvement on CMP, DMP, VDP, and CRISPR tasks.

## Reported Insights

1. Single nucleotide tokenization is sufficient and superior for RNA; subword/k-mer tokenizers hurt nucleotide-resolution tasks.
2. ALiBi is the best positional encoding for RNA, especially for generalizing across lengths; RoPE can be unstable.
3. Pre-trained RNA LMs show strong potential (8/13 SOTA) but are not universally better than simple supervised models — LSTM and ResNet remain competitive, especially on structural tasks with small datasets.
4. Domain-specific pre-training data yields large gains on matching downstream tasks; multi-species data helps generalization.
5. A small, well-designed model (BEACON-B) can rival or beat much larger models with 10–60× less compute, suggesting architecture and design choices currently matter more than scale for RNA.
6. Existing RNA LMs struggle on contact/distance map prediction and CRISPR tasks, indicating room for innovation.

## References Worth Chasing

- **RNA-FM** [Chen et al. 2022, ref 13]: 99.5M-param RNA foundation model pre-trained on 23.7M ncRNA sequences; interpretable.
- **SpliceBERT** [Chen et al. 2023, ref 15]: Pre-trained on 2M pre-mRNA sequences (65B nucleotides) for splice prediction.
- **UTR-LM** [Chu et al. 2024, ref 18]: 5′ UTR language model with secondary structure and MFE auxiliary objectives.
- **3UTRBERT** [Yang et al. 2023, ref 119]: 3′ UTR BERT with K-mer tokenization.
- **RNA-MSM** [Zhang et al. 2023, ref 124]: MSA-based RNA LM using homologous sequences (like MSA Transformer for proteins).
- **DNABERT-2** [Zhou et al. 2023, ref 125]: BPE-based DNA foundation model — relevant for tokenizer comparison.
- **Nucleotide Transformer** [Dalla-Torre et al. 2023, ref 23]: DNA foundation model with non-overlapping k-mer tokenizer.
- **ALiBi** [Press et al. 2021, ref 76]: Attention with Linear Biases — key positional encoding finding.
- **BEND** [Marin et al. 2024, ref 69]: DNA benchmark — methodological parallel.
- **Genomics-FM** [Ye et al. 2024, ref 120]: Foundation model for functional genomics, referenced for single-nucleotide tokenizer design.

## Notes / Open Questions

- The benchmark only evaluates sequence-input tasks; RNA 3D structure prediction, inverse folding, and scRNA-seq tasks are excluded (acknowledged as future work).
- All evaluated LMs use BERT-style MLM pre-training; no autoregressive or diffusion-based RNA models are benchmarked.
- RNA-MSM uses MSA input during pre-training but homologous sequences were excluded during benchmark evaluation for fairness — this may understate its real-world advantage.
- RoPE's poor performance may be specific to the short sequence lengths in BEACON (max 1182 nt); results may not generalize to long-range RNA tasks.
- CRISPR tasks have very short inputs (23 nt) — may not benefit from LMs at all; traditional feature-engineered methods still lead.
- The paper does not report pre-training data sizes for RNABERT, RNA-MSM, UTR-LM in comparable token counts, making compute comparisons incomplete.
- BEACON-B is proposed as a baseline but is itself pre-trained — calling it "baseline" slightly undersells it.
