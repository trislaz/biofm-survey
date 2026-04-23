---
id: sequence-modeling-and-design-2024
title: Sequence modeling and design from molecular to genome scale with Evo
authors: []
year: 2024
venue: Science
arxiv: null
doi: 10.1126/science.ado9336
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/sequence-modeling-and-design-2024.md
modalities:
- dna
- rna
- protein-sequence
status: extracted
evidence_quality: full-text
tags:
- StripedHyena
- long-context
- genome-scale
- byte-level-tokenization
- scaling-laws
- prokaryotic
- CRISPR
- transposon
- zero-shot
- autoregressive
parameters: 7B
training_tokens: 340B
training_compute: 2e22 FLOPs
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

Evo is a 7B-parameter autoregressive genomic foundation model using the StripedHyena architecture, trained on 300B nucleotide tokens from prokaryotic and phage genomes at single-nucleotide (byte-level) resolution with 131k context length. It unifies DNA, RNA, and protein modalities via the raw genomic sequence. Evo matches or outperforms domain-specific models on zero-shot protein/ncRNA fitness prediction and regulatory DNA tasks, generates functional CRISPR-Cas and transposon systems (first protein-RNA/protein-DNA codesign with a language model), predicts gene essentiality using long genomic context, and generates megabase-scale sequences with plausible genome architecture.

## Model

- **Architecture**: StripedHyena — a hybrid of data-controlled convolutional operators (Hyena layers) and multi-head attention with RoPE.
- **Layers**: 32 blocks total; 29 Hyena layers interleaved with 3 attention layers (10% attention) at equal intervals.
- **Model width**: 4,096 dimensions.
- **Channel mixing**: Gated Linear Units (GLU / SwiGLU).
- **Normalization**: Root-mean-square layer normalization (pre-norm).
- **Context length**: 131,072 tokens (131k) at single-nucleotide resolution.
- **Tokenization**: Byte-level, single-nucleotide; effective vocabulary of 4 tokens (A/C/G/T) from a 512-character UTF-8 space (allows vocabulary expansion for special prompt tokens during fine-tuning).
- **Parameters**: 7 billion.
- **Position encoding**: Rotary Position Embeddings (RoPE) in attention layers; linear position interpolation used for context extension from 8k → 131k.
- **Generation**: Autoregressive next-token prediction; fast recurrent mode of Hyena layers enables generation of sequences up to 650k nucleotides on a single 80 GB GPU. Standard top-k + temperature sampling.

## Data

- **Dataset**: OpenGenome — 300B nucleotide tokens.
- **Sources**:
  - GTDB v214.1: 80,000+ bacterial and archaeal representative genomes (one per species).
  - IMG/VR v4: millions of high-confidence prokaryotic virus sequences (one per vOTU).
  - IMG/PR: plasmid sequences (one per PTU).
  - Total: ~2.7 million prokaryotic and phage genomes.
- **Safety exclusion**: all eukaryotic viral genomes removed; 19 viral families and 12 orders explicitly filtered out.
- **Dataloading**: Sequence packing — random sampling without replacement; contigs delimited by EOS tokens; species-level tokens prepended in the 131k stage.
- **Fine-tuning datasets** (compiled from a custom multi-source metagenomic database):
  - CRISPR-Cas: 72,831 loci (Cas9/Cas12/Cas13 with flanking sequence, ≤8,192 nt).
  - IS200/IS605: 219,866 IS200 + 10,720 IS605 elements with natural flanking context.

## Training Recipe

- **Objective**: Next-token prediction (autoregressive), no annotations or supervision.
- **Two-stage pretraining**:
  1. **Stage 1** (8k context): 300B tokens, 64 × NVIDIA H100 GPUs, ~2 weeks.
  2. **Stage 2** (131k context extension): continued training on GTDB + IMG/VR subset (excl. eukaryotic viruses), 128 × NVIDIA A100 GPUs, ~2 weeks. Linear position interpolation for RoPE.
- **Total tokens**: ~340B (~1.13 epochs of OpenGenome; 300B unique + partial repeat in different order).
- **Total compute**: ~2 × 10²² FLOPs.
- **Parallelism**: Pipeline parallel with 2 depth-wise stages.
- **Fine-tuning** (CRISPR-Cas / IS200/IS605): continued training from 8k-pretrained checkpoint; batch size 524,288 tokens; initial LR = 0.00009698 (final pretraining LR); ~10 epochs; class-conditional special tokens prepended; loss-masked padding for short sequences.

## Key Ablations & Design Choices

### Architecture scaling laws
- Trained >300 models across 4 architectures: Transformer++, Mamba, Hyena, StripedHyena.
- Compute budgets: 8×10¹⁸, 2×10¹⁹, 4×10¹⁹, 8×10¹⁹ FLOPs.
- **Transformer++ substantially worse** at byte-level resolution across all budgets.
- Hyena and StripedHyena achieve best scaling rates; Mamba and SSMs also beat Transformer++.
- StripedHyena most stable outside compute-optimal frontier (Transformer++ and Mamba suffer numerical instability and degraded scaling rate when over-training).

### Byte-level vs k-mer tokenization
- Byte-level (single-nucleotide) tokenization is critical for single-nucleotide resolution; enables detection of individual mutations affecting fitness.
- Transformer-based DNA models (GenSLM, Nucleotide Transformer) use codon or 6-mer tokenization — sacrifices resolution and limits downstream tasks.
- Transformer attention scales quadratically and underperforms at byte resolution vs. coarser tokenization.
- StripedHyena's Hyena layers efficiently aggregate nucleotides into motifs via compositions of short/long convolutions.

### Multi-scale capabilities
- **Molecular**: zero-shot protein/ncRNA fitness prediction, regulatory DNA activity.
- **Systems**: CRISPR-Cas protein-RNA codesign, IS200/IS605 protein-DNA transposon codesign.
- **Genome**: gene essentiality prediction with long context; megabase-scale sequence generation.
- Longer context (8k → 66k) substantially improves gene essentiality prediction (gene-only → 8k is the biggest jump).

### Compute-optimal analysis
- Compute-optimal token count for 7B at the given FLOP budget: ~250B tokens.
- Actual training: 300B tokens (17% offset from compute-optimal model size).
- StripedHyena tolerates this over-training offset much better than Transformer++/Mamba.

## Reported Insights

- **Protein fitness**: Evo zero-shot outperforms all nucleotide models (GenSLM, Nucleotide Transformer) and is competitive with leading protein LMs (ESM-1v, ESM-2, ProGen2) on prokaryotic DMS benchmarks. Fails on human proteins (not in training data), but performance correlates with perplexity on wild-type — suggests fine-tuning could help.
- **ncRNA fitness**: Outperforms RNA-FM (a dedicated RNA LM) on zero-shot ncRNA DMS (tRNAs, rRNAs, ribozymes); 5S rRNA Spearman r=0.60.
- **Regulatory DNA**: Zero-shot likelihood correlates with promoter activity (mean Spearman r=0.43); Evo embeddings + supervised CNN approaches state-of-the-art Promoter Calculator; promoter+RBS context improves protein expression prediction (r=0.61).
- **CRISPR-Cas generation**: Fine-tuned model generates coherent Cas9/Cas12/Cas13 loci; 1/11 Cas9 designs (EvoCas9-1) experimentally validated with in vitro cleavage comparable to SpCas9; EvoCas9-1 is 73.1% identical to SpCas9; first protein-RNA codesign with a language model.
- **Transposon generation**: 11/24 IS200-like and 3/24 IS605-like designs show excision+insertion activity in vitro; ~50% success rate for IS200; generated TnpA proteins as low as 67% identity to training set.
- **Gene essentiality**: Zero-shot prediction via in silico stop-codon insertion; significant AUROC in 49/58 genomes; AUROC 0.90 on lambda phage, 0.84 on P. aeruginosa; genomic context (8k, 66k) substantially improves over gene-only.
- **Megabase generation**: 16 sequences of ~1 Mb generated; near-natural coding density; correct strand organization; proteins with predicted secondary structure and GO-term matches; 128 tRNAs covering all amino acids. But: few rRNAs (3/16 Mb), missing conserved marker genes, low-confidence structures biased toward α-helices — a "blurry image" of a genome.

## References Worth Chasing

- **(24)** StripedHyena architecture paper — hybrid attention + Hyena design, model hybridization rationale.
- **(28)** Modal canonical form for deep signal processing convolution parametrization.
- **(34)** Hyena: original Hyena operator paper (predecessor architecture to StripedHyena, predecessor model HyenaDNA).
- **(33)** HyenaDNA — prior-generation DNA model with Hyena; Evo is 1000× larger model, 100× more data.
- **(38, 39)** Scaling laws methodology (Hoffmann et al. / Chinchilla); compute-optimal protocol.
- **(15)** GenSLM — codon-vocabulary prokaryotic coding-sequence LM; main nucleotide baseline.
- **(16)** Nucleotide Transformer — 6-mer vocabulary, multi-species DNA model.
- **(40)** Mamba — data-controlled state-space model architecture.
- **(41)** ESM-1v — protein language model for variant effect prediction.
- **(50)** RNA-FM — RNA foundation model trained on ncRNA sequences.
- **(59–61)** CRISPR-Cas biology and Cas9/Cas12/Cas13 diversity.
- **(66–69)** IS200/IS605 transposon biology and TnpB/ωRNA mechanism.

## Notes / Open Questions

- Prokaryotic-only training is a clear limitation: zero-shot protein fitness prediction fails on human proteins. Eukaryotic genome inclusion would require major resource investment and safety alignment.
- The 131k context is long but still far shorter than most bacterial genomes (1–10 Mb). The megabase generation relies on autoregressive extension beyond context length (~7× context), which produces globally plausible but locally imperfect genomes.
- Fine-tuning success rates vary by system complexity: ~50% for IS200 (simpler) vs ~4.5% (1/11) for Cas9 (more complex multistep mechanism). PAM specificity was not explored across designs.
- Scaling laws only evaluated up to 8×10¹⁹ FLOPs for the architecture comparison; the final 7B model used ~2×10²² FLOPs — a 250× extrapolation from the studied range.
- The "blurry image" analogy for genome generation is informative: the model captures high-level organization but misses fine-grained details (rRNAs, marker genes). Suggests alignment/RLHF-like techniques from NLP may transfer.
- No explicit multi-task or instruction tuning; all downstream evaluation is zero-shot or fine-tuned with next-token prediction only.
- Model and code open-sourced at https://github.com/evo-design/evo.

## Verification (Rev 3)

Each `[sequence-modeling-and-design-2024]` citation in `insights.md` is checked against the PMC full text.

| # | insights.md line | Claim (paraphrased) | Verdict | Comment |
|---|---|---|---|---|
| 1 | 11 | Byte-level tokenization removes k-mer leakage entirely and enables multi-kingdom modelling at the cost of longer sequences. | **partial** | Byte-level tokenization eliminating artefacts and requiring longer context (131 k) is supported (§ intro, § architecture). However, "enables multi-kingdom modelling" is **not** supported: Evo is trained exclusively on prokaryotic and phage genomes; the paper explicitly states eukaryotic inclusion would require substantial additional investment (§ Discussion). |
| 2 | 15 | Sequence-only tasks are well-served by standard Transformers or, at byte level, by state-space hybrids (StripedHyena). | **supported** | The paper shows StripedHyena outperforms Transformer++ at byte-level resolution (§ Scaling laws, Fig. 1F–G). The nuance that Transformers work at coarser tokenization while SSM hybrids are needed at byte level is consistent with the source. |
| 3 | 63 | Evo operates on raw single-nucleotide tokens (byte-level), eliminating tokenization artefacts entirely but requiring 131 k-token context windows. | **supported** | Directly stated: "byte-level, single-nucleotide tokenizer" with "context length of 131,072 tokens" (§ intro, § architecture). The paper contrasts this with k-mer methods that "sacrifice single-nucleotide resolution." |
| 4 | 112 | A pure Transformer++ of similar size was substantially worse at byte-level resolution. | **supported** | "We found Transformer++ to yield substantially worse perplexity … at all compute budgets" (§ Scaling laws). Confirmed also at 7 B scale: "Transformer++ performance is substantially worse than StripedHyena" (§ Materials — Scaling laws). |
| 5 | 165 | Evo extended [autoregressive generation] to byte-level DNA with cross-modal generation (protein–RNA codesign). | **supported** | Paper states "the first examples of protein-RNA and protein-DNA codesign with a language model" (Abstract, § intro). CRISPR-Cas generation demonstrates protein–RNA codesign after fine-tuning. |
| 6 | 203 | Table row: Evo — DNA (byte) — 131 k tokens — StripedHyena SSM + attn. | **partial** | DNA (byte), 131 k tokens, and hybrid architecture are correct. Labelling StripedHyena as "SSM + attn" is a common simplification but technically inaccurate per the paper: it distinguishes Hyena's "data-controlled convolutional operators" / "deep signal processing primitives" from state-space models (Mamba). Minor terminological issue. |
| 7 | 252 | Early-fusion (interleaving tokens from different modalities in a single sequence) — Evo interleaves DNA, protein, and RNA tokens for cross-modal generation. | **partial** | Evo processes a **single DNA alphabet** (A/C/G/T); it does not explicitly interleave tokens from separate modality encoders. The multi-modality arises implicitly because genomic DNA encodes proteins and ncRNAs. Calling this "early fusion" with "interleaved" modality tokens mischaracterises the mechanism, although the cross-modal generation outcome is real. |
| 8 | 398 | First LM to perform protein–RNA codesign in a single forward pass; Transformer++ substantially underperforms the SSM hybrid at byte-level DNA. | **partial** | "First LM for protein–RNA codesign" is directly stated in the paper. "Transformer++ substantially underperforms" is supported. However, "single forward pass" is inaccurate: Evo generates sequences autoregressively (many forward steps), not in a single pass. |
| 9 | 587 | Evo's protein–RNA codesign is early evidence for cross-modal transfer. | **supported** | Reasonable interpretive use. The paper demonstrates cross-modal generation (CRISPR-Cas protein + guide RNA from a DNA-only model), which qualifies as early evidence that genomic LMs can bridge modalities. |

**Summary:** 5 supported, 4 partial, 0 unsupported, 0 out-of-scope. Partial verdicts stem from (a) an unsupported "multi-kingdom" attribution, (b) SSM vs deep-signal-processing terminology, (c) mischaracterisation of implicit modality unification as explicit early-fusion interleaving, and (d) "single forward pass" vs autoregressive generation.
