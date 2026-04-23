---
id: hyenadna-long-range-genomic-2023
title: 'HyenaDNA: Long-Range Genomic Sequence Modeling at Single Nucleotide Resolution'
authors:
- Eric Nguyen
- Michael Poli
- Marjan Faizi
- Armin Thomas
- Callum Birch-Sykes
- Michael Wornow
- Aman Patel
- Clayton Rabideau
- Stefano Massaroli
- Yoshua Bengio
- Stefano Ermon
- Stephen A. Baccus
- Chris Ré
year: 2023
venue: null
arxiv: '2306.15794'
doi: null
url: https://arxiv.org/abs/2306.15794v2
pdf_path: papers/hyenadna-long-range-genomic-2023.pdf
md_path: papers/md/hyenadna-long-range-genomic-2023.md
modalities:
- dna
status: extracted
evidence_quality: full-text
tags:
- hyena
- long-context
- single-nucleotide
- implicit-convolution
- sub-quadratic
- in-context-learning
- soft-prompting
- sequence-length-warmup
parameters: 6.6M (largest); suite from 0.44M to 6.6M
training_tokens: up to ~2T tokens (1M context × 10–20k steps)
training_compute: 1.3 GPU-hrs (small models on 1×A100-40GB, 80 min); largest 1M model
  ~4 weeks
references_chased: false
added_at: '2026-04-22T19:54:18+00:00'
updated_at: '2026-04-22T19:58:48+00:00'
is_fm: true
fm_classification_reason: 'HyenaDNA: pretrained long-range genomic FM.'
---

## TL;DR

HyenaDNA is a genomic foundation model that replaces attention with the Hyena operator (implicit long convolutions + data-controlled gating) to achieve sub-quadratic O(L log₂ L) scaling, enabling context lengths up to 1M nucleotides at single-nucleotide resolution—a 500× increase over prior dense-attention genomic FMs. Pretrained on a single human reference genome with next-nucleotide prediction, HyenaDNA achieves SotA on 12/18 Nucleotide Transformer benchmarks and 7/8 GenomicBenchmarks while using 1,500× fewer parameters (1.6M vs 2.5B) and 3,200× less pretraining data than the largest Nucleotide Transformer. The paper also introduces sequence-length warm-up scheduling for ultra-long training stability and the first use of in-context learning / soft prompting in genomics.

## Model

- **Architecture**: Decoder-only, causal model built from stacked Hyena operator blocks (each block = Hyena operator + FFN). Hyena replaces attention as a drop-in mixing layer.
- **Hyena operator**: Combines (i) a learnable long convolution filter produced by a small MLP (implicit parameterization via neural fields), with (ii) element-wise data-controlled gating from input projections. Evaluated via FFT convolution in O(L log₂ L).
- **Tokenization**: Single-character tokenizer using the natural DNA vocabulary of 5 tokens: A, G, C, T, N (plus special tokens). No k-mer or BPE aggregation—preserves single-nucleotide resolution.
- **Model suite**: Depths 2–8 layers, widths 128–256, MLP expansion factor 4×. Parameter counts range from 0.44M (2 layers, width 128) to 6.6M (8 layers, width 256).
- **Context lengths**: 1k to 1M tokens. At 1M tokens, HyenaDNA is 160× faster than a Transformer baseline (forward+backward, 2 layers, width 128, batch 1, A100 80GB).

## Data

- **Pretraining data**: Single human reference genome (GRCh38, Genome Reference Consortium 2013). Training/validation intervals from Avsec et al. 2021 (Enformer). Test set: chromosomes 14 and X (non-overlapping sequences of length L).
- **Downstream benchmarks**:
  - GenomicBenchmarks (8 regulatory element classification datasets, seq len 200–4,776)
  - Nucleotide Transformer benchmarks (18 datasets: enhancers, promoters, epigenetic marks, splice sites; seq len 200–600)
  - Chromatin profile prediction (DeepSEA 919-way multi-task; seq len 1k)
  - Species classification (5-way: human, lemur, mouse, pig, hippo; seq len 1k–1M)
  - Embedding quality evaluation (10 biotype classification from GENCODE)

## Training Recipe

- **Objective**: Next-nucleotide (token) prediction (autoregressive, causal LM).
- **Optimizer**: AdamW (β₁=0.9, β₂=0.999), weight decay 0.1 for model params, 0 for Hyena layers.
- **LR schedule**: Cosine decay, LR range 1.5e-4 to 6e-4.
- **Batch size**: 64–256 (global batch size kept constant across sequence lengths via gradient accumulation).
- **Steps**: 10–20k global steps. Longer sequences = more tokens per step (e.g., 1M context trained ~2T tokens over 4 weeks).
- **Gradient checkpointing**: Reduces memory footprint ~3× for sequences >160k.
- **Sequence-length warm-up**: Starts at L=64, doubles at each stage. Critical for ultra-long sequences (>200k). At 450k: reduces training time by 40%, boosts accuracy by +7.5 points on species classification.
- **Downstream adaptation**: (1) Full fine-tuning with linear decoder head; (2) Soft prompting—inject 2–32k learnable tokens into input, optimize only prompt params while freezing model weights. Provides competitive results without updating the pretrained model.
- **Hardware**: Mix of A100, V100, T4 GPUs. Small models: 1×A100-40GB, ~80 min wall clock, 1.3 GPU-hrs.

## Key Ablations & Design Choices

- **Context length vs. perplexity**: Longer context → better pretraining perplexity, but requires more tokens. Shallow models show inflection points where perplexity degrades with excessive context—context length acts as a regularization dimension.
- **Pretraining vs. scratch**: Pretraining gap widens dramatically with sequence length. On species classification: scratch 71.4% vs pretrained 99.4% at 450k (a 28-point gap); scratch 53.9% vs pretrained 61.1% at 1k (only 7.2-point gap).
- **Hyena vs. Transformer (attention)**: On GenomicBenchmarks, HyenaDNA (2L, 128w, 0.44M params) beats a Transformer baseline with same architecture on most tasks. On NT benchmarks, HyenaDNA (1.6M params) outperforms NT models (500M–2.5B params) on 12/18 datasets.
- **Single-nucleotide vs. k-mer tokenization**: Ablation on GenomicBenchmarks shows single-nucleotide tokenizer outperforms 6-mer on most tasks (Table A.4).
- **Causal vs. bidirectional**: Bidirectional Hyena variant tested but causal decoder-only performs competitively (Table A.4).
- **Soft prompting vs. fine-tuning**: Soft prompting with up to 32k learnable tokens achieves competitive performance on GenomicBenchmarks without updating pretrained weights (Table A.7). Performance improves as number of prompt tokens increases.
- **Pretraining compute efficiency**: HyenaDNA 1.6M model uses 1.3 GPU-hrs vs DNABERT 110M at 12,000 GPU-hrs and NT 2.5B at 215,000 GPU-hrs (Table A.2). Orders of magnitude more efficient.
- **Species classification scaling**: Accuracy scales from 61.1% (1k) → 93.4% (32k) → 97.9% (250k) → 99.4% (450k) → 99.5% (1M). Transformer infeasible beyond 32k context.
- **Optimal pretrained-to-downstream length ratio**: 2–4× pretrained sequence length relative to downstream max length gives best performance.

## Reported Insights

- Long-range context and single-nucleotide resolution are both critical for genomics—previous approaches sacrificed one for the other.
- Sub-quadratic models (Hyena) unlock practical training at ultra-long sequences (≥100k) where attention-based models are infeasible.
- In-context learning is viable for genomics: soft prompting enables task adaptation without weight updates, analogous to few-shot prompting in NLP.
- Pretrained HyenaDNA embeddings cluster genomic sequences by biotype (gene/transcript type), showing the model learns biologically meaningful representations.
- Pretraining on even a single genome yields strong transferable features; multi-genome pretraining could further improve generalization.
- The model is extremely parameter-efficient: 1.6M params competitive with 2.5B-param Nucleotide Transformer.

## References Worth Chasing

- Hyena: Creating Large Language Models with Long Memory (Poli et al., 2023, arXiv:2302.10866) — core Hyena architecture that HyenaDNA builds upon
- The Nucleotide Transformer (Dalla-Torre et al., 2023, arXiv:2301.11270) — primary benchmark comparison; BERT-style genomic FM up to 2.5B params on 3202 genomes
- DNABERT (Ji et al., 2021, doi:10.1093/bioinformatics/btab083) — k-mer based BERT genomic FM, 110M params
- Enformer (Avsec et al., 2021, doi:10.1038/s41592-021-01252-x) — gene expression prediction with 100k context via dilation/downsampling
- FlashAttention (Dao et al., 2022a, arXiv:2205.14135) — IO-aware exact attention used as Transformer baseline
- H3: Hungry Hungry Hippos (Dao et al., 2022b, arXiv:2212.14052) — predecessor H-family implicit convolution language model
- ESM-2 / protein language models (Lin et al., 2022, arXiv:2207.06616) — contrast with protein FM successes motivating DNA FMs
- BigBird (Zaheer et al., 2020, arXiv:2007.14062) — sparse-attention Transformer used for long genomic contexts
- S4: Structured State Spaces for Sequence Modeling (Gu et al., 2021, arXiv:2111.00396) — foundational long-convolution SSM architecture
- GenomicBenchmarks (Gresova et al., 2022, doi:10.1093/bioinformatics/btad439) — downstream evaluation suite
- ProGen (Madani et al., 2023, doi:10.1038/s41587-022-01618-2) — autoregressive protein language model
- ProtTrans (Elnaggar et al., 2021, doi:10.1109/TPAMI.2021.3095381) — protein sequence FM
- Sequence length warmup (Li et al., 2022) — prior work on sequence length scheduling for training stability
- Soft prompting / prompt tuning (Lester et al., 2021, arXiv:2104.08691) — technique adapted for genomics in this work

## Notes / Open Questions

- Only pretrained on a single human reference genome. How much would multi-genome or multi-species pretraining improve generalization?
- The model is tiny by LLM standards (max 6.6M params). What happens at 100M+ scale with Hyena operators?
- No comparison with S4/Mamba-style SSMs which emerged around the same time—how do these compare for genomics?
- Chromatin profile (DeepSEA 919-way) results are competitive but do not clearly beat BigBird SotA—this is a harder benchmark.
- Soft prompting results are promising but still below full fine-tuning on most tasks. Can the gap be closed with more prompt tokens or better prompt optimization?
- The paper does not explore variant effect prediction or clinical genomics applications—important future direction.
- Training compute is remarkably low for short-range tasks but the 1M context model still requires ~4 weeks—practical scaling questions remain.

## Ablations (Rev 4)

| Variable | Settings | Metric / dataset | Result | Conclusion |
|---|---|---|---|---|
| Tokenization (single-nt vs 6-mer) | HyenaDNA char-level vs HyenaDNA k-mer (k=6), trained from scratch | Top-1 acc, GenomicBenchmarks (8 datasets, Tab. A.4) | 6-mer drops accuracy on majority of datasets by up to ~10 pts (e.g. Mouse Enhancers 84.7→81.8; Human Nontata Promoters 93.3→83.5; Human OCR 78.8→70.2); only Human Enhancers Ensembl improves (85.7→88.0) | Single-nucleotide tokenization is a major contributor to HyenaDNA's performance; aggregating k-mer tokenizers hurt fine-grained tasks |
| Directionality (causal vs bidirectional) | Causal HyenaDNA vs bidirectional Hyena via circular FFT padding, both from scratch | Top-1 acc, GenomicBenchmarks (Tab. A.4) | Bidirectional degrades 7/8 datasets, avg −3.8 acc pts (e.g. Mouse Enhancers 84.7→80.6; Human Nontata 93.3→88.5) | Causal next-token pretraining is preferable; naive bidirectional Hyena (without MLM pretraining) underperforms |
| Pretraining vs from-scratch (short-range) | HyenaDNA pretrained vs scratch | GenomicBenchmarks Top-1 (Tab. A.4) | Pretraining gives mild–moderate gains (e.g. Human OCR 78.8→80.9; Human Nontata 93.3→96.6); GPT also benefits (e.g. Human OCR 68.3→79.9) | Pretraining helps but gains are modest because GenomicBenchmarks are near saturation |
| Pretraining vs from-scratch (NT benchmark) | HyenaDNA 1.6M, pretrained vs scratch | MCC / F1, 18 NT datasets (Tab. A.6) | Big gains on hard histone tasks: H3K4me3 40.2→61.2 (+21), H3K4me2 34.5→53.9, H4ac 43.5→63.7; near-zero gain on splice/promoter tasks (already saturated, ≤1 pt) | Pretraining matters most on harder, lower-baseline tasks (especially histone marks) |
| Mixing layer (Hyena vs attention) | HyenaDNA 1.6M (pretrained) vs GPT 1.6M (pretrained) vs NT 2.5B | NT benchmarks (Tab. A.6) | HyenaDNA beats same-size GPT on nearly all 18 datasets (e.g. H3K4me3 28.3→61.2; H4ac 36.4→63.7); matches/exceeds 2.5B NT on 12/18 | Hyena operator outperforms attention at matched parameter count and competes with models 1500× larger |
| Pretraining × sequence length (long-range) | HyenaDNA scratch vs pretrained at 1k / 32k / 250k / 450k | Top-1, 5-way species classification (Tab. A.11) | 1k: 53.9→61.1 (+7.2); 32k: 70.7→93.4 (+22.7); 250k: 65.7→97.9 (+32.2); 450k: 71.4→99.4 (+28.0) | Pretraining benefit grows dramatically with context length; longer context models are unusable without pretraining |
| Sequence-length warm-up scheduler | Direct training vs staged length warm-up (start L=64, double per stage) at 450k context | Training time & species-classification acc (Fig. 3.2) | Training time −40%; accuracy +7.5 pts | Length warm-up is critical for stability and efficiency at ultralong (≥200k) sequences |
| Pretraining context length | Models pretrained at varying context lengths on human genome | Pretraining perplexity (Fig. 1.2) | Longer context → lower perplexity, but only if model is deep enough; shallow models show inflection / degradation at long context; longer context costs more tokens/time | Context length acts as a regularization dimension; tradeoff between speed (short) and final quality (long) |
| Soft prompt length (in-context adaptation) | 2 → 32k learnable tokens prepended, model frozen | GenomicBenchmarks accuracy (Fig. 4.2) | Performance increases monotonically with # tuneable tokens; saturates near full-fine-tune baseline (Tab. 4.1) on most tasks | Long-context window enables competitive parameter-efficient adaptation purely via soft prompts; longer prompts → better |
| Model & pretraining-data scale (cross-architecture) | HyenaDNA 1.6M / 1 genome vs NT 500M–2.5B / 1–3,202 genomes | NT benchmarks (Tab. 4.2) | HyenaDNA SotA on 12/18 with ≥300× fewer params and ≥850× fewer genomes | Architecture (subquadratic + single-nt) and pretraining recipe matter more than parameter/data scale at this regime |

**Design-choice take-aways from this paper's ablations:**
- Single-nucleotide tokenization beats k-mer aggregation for most genomic classification tasks — preserve resolution.
- Causal next-token pretraining works well; bidirectional Hyena variants do not pay off out of the box.
- Pretraining benefit scales with task difficulty and especially with input sequence length — long-context models essentially require pretraining.
- A staged sequence-length warm-up schedule is essential to train stably at 200k+ tokens (40% speedup, +7.5 acc on species classification at 450k).
- Hyena operator matches or beats attention at equal parameter count, and the right architecture+recipe (subquadratic, single-nt, pretrained) can outperform models 100–1000× larger.
- Soft prompts of growing length recover most of full fine-tuning performance; long context unlocks parameter-efficient adaptation.
