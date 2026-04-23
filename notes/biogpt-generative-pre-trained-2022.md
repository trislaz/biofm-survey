---
id: biogpt-generative-pre-trained-2022
title: 'BioGPT: Generative Pre-trained Transformer for Biomedical Text Generation
  and Mining'
authors:
- Renqian Luo
- Liai Sun
- Yingce Xia
- Tao Qin
- Sheng Zhang
- Hoifung Poon
- Tie-Yan Liu
year: 2022
venue: null
arxiv: '2210.10341'
doi: null
url: https://arxiv.org/abs/2210.10341v3
pdf_path: papers/biogpt-generative-pre-trained-2022.pdf
md_path: papers/md/biogpt-generative-pre-trained-2022.md
modalities:
- other
status: extracted
evidence_quality: full-text
tags: ["autoregressive", "byte-pair", "soft-prompt", "causal-lm", "biomedical-nlp"]
parameters: 347000000
training_tokens: 104900000000
training_compute: null
references_chased: false
added_at: '2026-04-22T20:11:28+00:00'
updated_at: '2026-04-22T20:14:05+00:00'
---

## TL;DR

BioGPT is a domain-specific GPT-2–based autoregressive language model (347M params) pre-trained from scratch on 15M PubMed abstracts for biomedical text generation and mining. The key novelty is bringing generative pre-training (GPT-style) to the biomedical domain, where prior work focused almost exclusively on BERT-style masked LMs (BioBERT, PubMedBERT). BioGPT achieves SOTA on end-to-end relation extraction (BC5CDR 44.98% F1, KD-DTI 38.42% F1, DDI 40.76% F1), PubMedQA (78.2% accuracy), and HoC document classification (85.12% F1). A scaled BioGPT-Large (1.5B params) further improves most results (PubMedQA 81.0%).

## Model

- **Architecture**: GPT-2 medium Transformer decoder (causal LM). 24 layers, 1024 hidden size, 16 attention heads.
- **Parameters**: 347M (vs GPT-2 medium 355M; difference from domain-specific BPE vocabulary of size 42,384).
- **BioGPT-Large**: GPT-2 XL architecture, 1.5B parameters.
- **Context length**: Not explicitly stated; inherits GPT-2's 1024-token context window.
- **Key components**: Standard multi-head causal self-attention + FFN blocks. Prefix-style soft prompts (continuous embeddings) inserted between source and target during fine-tuning. Labels converted to natural-language target sequences rather than structured special-token formats.

## Data

- **Pretraining corpus**: 15M PubMed abstracts (title + abstract) updated before 2021, downloaded from NCBI FTP. Items with empty abstracts filtered out.
- **Source**: PubMed (https://ftp.ncbi.nlm.nih.gov/pubmed/).
- **Size**: ~15M documents. No explicit token count reported; estimated ~3B raw tokens at ~200 tokens/abstract.
- **Preprocessing**: BPE tokenization learned on the in-domain corpus using fastBPE. Vocabulary size = 42,384.
- **Deduplication / filtering**: Only filtering of empty abstracts mentioned; no further dedup described.
- **Splits**: Entire corpus used for pretraining; downstream tasks use their own standard splits.

## Training Recipe

- **Objective**: Causal language modeling (next-token prediction, standard autoregressive LM loss).
- **Tokenizer**: Byte-pair encoding (BPE) via fastBPE, learned on PubMed corpus. Vocab size 42,384.
- **Batch size**: 1024 tokens/GPU × 8 GPUs × 64 gradient accumulation steps = 524,288 tokens/step.
- **Optimizer**: Adam, peak LR = 2×10⁻⁴, 20,000 warm-up steps, inverse-square-root decay schedule.
- **Total steps**: 200,000.
- **Total tokens processed**: ~524,288 × 200,000 ≈ 104.9B tokens (implies ~35 epochs over the corpus).
- **Hardware**: 8× NVIDIA V100 GPUs.
- **Wall-clock time**: Not reported.
- **Implementation**: fairseq.
- **Fine-tuning**: Single V100, batch size 1024 tokens × 32 accumulation steps. Task-specific epochs/LR vary. Beam search (size 5) for generation; greedy for classification tasks.

## Key Ablations & Design Choices

- **Target sequence format** (Table 9, KD-DTI): Natural-language formats outperform structured special-token format. Best: "rel-is" format (F1 38.38) vs structured (37.32), +1.06 F1. Confirmed on BC5CDR (44.98 vs 42.85) and DDI (40.76 vs 38.60).
- **Prompt design** (Table 10, KD-DTI): Soft continuous-embedding prompts outperform hard text prompts. Best hard prompt "we can conclude that" F1=38.16; best soft prompt length=13 F1=38.60 (+0.44). Soft prompt performance roughly invariant to length (1–17 virtual tokens; range 38.06–38.60). Authors used length=9 based on validation.
- **Domain-specific pretraining**: BioGPT vs GPT-2 medium (same architecture). Consistent large improvements: BC5CDR +18.2 F1 (44.98 vs 26.78), KD-DTI +8.03 F1 (38.42 vs 30.39), DDI +16.08 F1 (40.76 vs 24.68), PubMedQA +78.2% vs not reported for GPT-2, HoC +3.28 F1 (85.12 vs 81.84).
- **Scaling** (Table 11): BioGPT-Large (1.5B) vs BioGPT (347M): BC5CDR 50.12 vs 44.98 (+5.14), DDI 44.89 vs 40.76 (+4.13), PubMedQA 81.0 vs 78.2 (+2.8). KD-DTI slightly decreased (38.39 vs 38.42). HoC decreased (84.40 vs 85.12).
- **BioGPT vs REBEL_pt** (encoder-decoder with additional relation-extraction pretraining): BioGPT matches or surpasses REBEL_pt on KD-DTI (+5.1 F1) and DDI (+0.20 F1) without task-specific additional pretraining.
- **Two-stage fine-tuning + noisy labels** on PubMedQA: BioGPT 78.2% accuracy, +6.0% over BioLinkBERT-Large (72.2%).
- **Ensemble (†)**: BC5CDR BioGPT† 46.17 F1, +1.19 over single model.

## Reported Insights

- In-domain pretraining from scratch with a domain-specific vocabulary is critical for biomedical GPT, echoing PubMedBERT findings for BERT.
- Generative (GPT-style) models can match or beat discriminative (BERT-style) models on biomedical understanding tasks when properly adapted via prompt-based fine-tuning.
- Converting structured labels to natural-language target sequences is better than special-token formats for decoder-only models, because it maintains format consistency between pretraining and fine-tuning.
- Soft prompts are slightly better and more robust than hand-crafted hard prompts, with minimal sensitivity to prompt length.
- Scaling from 347M to 1.5B yields mixed results: strong gains on RE and QA but regression on document classification, suggesting potential overfitting on smaller datasets.

## References Worth Chasing

- PubMedBERT (10.1145/3458754) — foundational domain-specific BERT for biomedical NLP; from-scratch pretraining paradigm BioGPT follows.
- BioBERT (10.1093/bioinformatics/btz682) — first biomedical BERT via continued pretraining; key baseline.
- SciBERT (arXiv:1903.10676) — scientific-domain BERT; broader scientific pretraining.
- BioLinkBERT (ACL 2022, Yasunaga et al.) — link-aware pretraining; strong PubMedQA baseline.
- BioELECTRA (BioNLP 2021, Kanakarajan et al.) — ELECTRA for biomedical domain.
- DARE (arXiv:2004.13845) — prior GPT pretraining on biomedical text (only 0.5M abstracts); direct predecessor.
- GPT-3 biomedical evaluation (arXiv:2109.02555, Moradi et al.) — shows GPT-3 is poor few-shot learner in biomedical domain.
- GPT-3 for clinical IE (arXiv:2203.08410, Gutiérrez et al.) — another evaluation of LLMs in biomedical IE.
- REBEL (EMNLP 2021 Findings, Huguet Cabot & Navigli) — end-to-end relation extraction via seq2seq; key comparison.
- Prefix-Tuning (ACL 2021, Li & Liang, arXiv:2101.00190) — soft prompt method adopted by BioGPT.
- GPT-2 (Radford et al. 2019) — backbone architecture.
- BART (ACL 2020, Lewis et al.) — encoder-decoder baseline underlying REBEL.
- ElectraMed (arXiv:2104.09585) — ELECTRA pretrained from scratch on biomedical text.
- BlueBERT (BioNLP 2019, Peng et al.) — BERT on PubMed + clinical notes.

## Notes / Open Questions

- The paper does not report wall-clock training time or total FLOPs.
- No perplexity or intrinsic LM evaluation is provided; all evaluation is task-based.
- Text generation evaluation is purely qualitative (example-based); no automatic metrics (BLEU, ROUGE, etc.).
- BioGPT-Large shows regression on HoC and KD-DTI—no analysis of why scaling hurts on these tasks.
- No comparison with contemporaneous encoder-decoder biomedical models (e.g., BioBART) or instruction-tuned models.
- Pretraining data is PubMed abstracts only—no full-text articles from PMC, which could significantly increase coverage.
- The ~35 epochs over 15M abstracts is unusually high; potential overfitting risk is not discussed.
- Context window (1024 tokens) limits ability to process full documents, but this is not discussed.
