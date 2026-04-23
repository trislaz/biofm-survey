---
id: biobert-a-pre-trained-2019
title: 'BioBERT: a pre-trained biomedical language representation model for biomedical
  text mining'
authors:
- Jinhyuk Lee
- Wonjin Yoon
- Sungdong Kim
- Donghyeon Kim
- Sunkyu Kim
- Chan Ho So
- Jaewoo Kang
year: 2019
venue: null
arxiv: '1901.08746'
doi: null
url: https://arxiv.org/abs/1901.08746v4
pdf_path: papers/biobert-a-pre-trained-2019.pdf
md_path: papers/md/biobert-a-pre-trained-2019.md
modalities:
- text
status: extracted
evidence_quality: full-text
tags:
- continued-pretraining
- domain-adaptation
- masked-lm
- wordpiece
- biomedical-nlp
- bert
- ner
- relation-extraction
- question-answering
parameters: 110000000
training_tokens: 98300000000
training_compute: null
references_chased: false
added_at: '2026-04-22T21:55:54+00:00'
updated_at: '2026-04-22T21:55:56+00:00'
is_fm: true
fm_classification_reason: 'BioBERT: pretrained biomedical text FM.'
---

## TL;DR

BioBERT is BERT_BASE (110M params) continually pre-trained on biomedical corpora (PubMed abstracts 4.5B words + PMC full-text 13.5B words), initialized from the original BERT checkpoint trained on Wikipedia+BooksCorpus. It was the first domain-specific BERT for biomedicine. With minimal architectural modification, BioBERT achieves SOTA on three representative biomedical text mining tasks: NER (+0.62% F1 over prior SOTA), relation extraction (+2.80% F1), and question answering (+12.24% MRR). The key finding is that continued pre-training of BERT on biomedical text is crucial for strong downstream performance in biomedical NLP.

## Model

- **Architecture**: BERT_BASE — 12-layer Transformer encoder, 768 hidden size, 12 attention heads. Identical to Devlin et al. (2019) BERT_BASE.
- **Parameters**: ~110M (same as BERT_BASE).
- **Tokenizer**: WordPiece (Wu et al., 2016), cased vocabulary inherited from original BERT (not rebuilt on biomedical text). Any new biomedical term represented via frequent subwords (e.g., Immunoglobulin → I ##mm ##uno ##g ##lo ##bul ##in).
- **Key design choice**: Reuses BERT's original vocabulary for (i) compatibility with BERT checkpoints and (ii) ability to represent novel biomedical terms via subword composition and fine-tuning.

## Data

- **General-domain corpora** (inherited from BERT initialization):
  - English Wikipedia: 2.5B words
  - BooksCorpus: 0.8B words
- **Biomedical corpora** (used for continued pre-training):
  - PubMed Abstracts: 4.5B words (~29M articles as of Jan 2019)
  - PMC Full-text Articles: 13.5B words
- **Total biomedical**: 18B words
- **Corpus combinations tested**: Wiki+Books (BERT), +PubMed, +PMC, +PubMed+PMC.
- **Preprocessing**: WordPiece tokenization; no new vocabulary constructed. Cased text used (slightly better than lowercased).

## Training Recipe

- **Initialization**: Pre-trained BERT_BASE weights (Wiki+Books, 1M steps).
- **Objective**: Masked language model + next sentence prediction (same as BERT).
- **Hardware**: 8× NVIDIA V100 (32GB) GPUs via Naver Smart Machine Learning (NSML).
- **Max sequence length**: 512.
- **Mini-batch size**: 192 (→ 98,304 tokens/iteration).
- **Hyperparameters**: Same as original BERT pre-training (batch size, LR schedule) unless stated otherwise.
- **BioBERT v1.0 (+PubMed+PMC)**: 470K steps total (200K on PubMed + 270K on PMC). Wall-clock: >10 days.
- **BioBERT v1.0 (+PubMed)**: 200K steps on PubMed only.
- **BioBERT v1.0 (+PMC)**: 270K steps on PMC only.
- **BioBERT v1.1 (+PubMed)**: 1M steps on PubMed. Wall-clock: ~23 days. ~98.3B tokens processed.
- **Fine-tuning**: Single NVIDIA Titan Xp (12GB). Batch size ∈ {10, 16, 32, 64}. LR ∈ {5e-5, 3e-5, 1e-5}. NER requires >20 epochs; QA/RE fine-tuning <1 hour.

## Key Ablations & Design Choices

- **Corpus combination** (Tables 6–8): PubMed alone is generally best for NER/QA. Adding PMC helps some datasets but not all. BioBERT v1.1 (+PubMed, 1M steps) is the strongest single variant overall.
- **Corpus size effect** (Fig. 2a): Pre-training on 1B words already effective; performance improves up to 4.5B words (full PubMed), with diminishing returns beyond ~3B words on some datasets.
- **Pre-training steps** (Fig. 2b): NER F1 monotonically improves with more steps up to at least 200K on three NER datasets (NCBI Disease, BC2GM, BC4CHEMD).
- **BERT vs BioBERT** (Table 6): BERT_BASE (Wiki+Books only) scores 2.01 F1 below prior SOTA on NER (micro-averaged), while BioBERT v1.1 beats SOTA by +0.62 F1.
- **NER (Table 6)**: BioBERT v1.1 (+PubMed) best on 6/9 datasets. Micro-averaged F1: BERT 83.36 → BioBERT v1.1 86.77 (+3.41).
- **RE (Table 7)**: BioBERT v1.0 (+PubMed) best micro F1 +2.80 over SOTA. BERT already beats SOTA on CHEMPROT (73.74 vs 64.10 F1).
- **QA (Table 8)**: BioBERT v1.1 (+PubMed) best micro MRR 44.77 vs BERT 39.64 (+5.13) and SOTA 32.53 (+12.24). All BioBERT variants significantly outperform BERT on BioASQ factoid QA. SQuAD pre-training greatly helps both BERT and BioBERT on BioASQ.
- **Cased vs uncased vocabulary**: Cased vocabulary results in slightly better downstream performance (stated but not quantified in tables).

## Reported Insights

- Word distributions differ substantially between general and biomedical corpora, making domain-specific continued pre-training essential rather than optional.
- BioBERT can recognize biomedical named entities that BERT cannot, find exact entity boundaries, and correctly answer simple biomedical questions where BERT fails (Table 9 qualitative examples).
- The original BERT vocabulary, while not biomedical-specific, is sufficient because WordPiece subword decomposition can represent novel biomedical terms and fine-tuning adapts the embeddings.
- Even without silver-standard or additional datasets (unlike some SOTA models), BioBERT outperforms task-specific architectures (Bi-LSTM-CRF with character CNNs, etc.) on most benchmarks.
- The pre-released BioBERT (Jan 2019) was quickly adopted for clinical NER (Alsentzer et al., 2019), phenotype-gene RE (Sousa et al., 2019), and clinical temporal RE (Lin et al., 2019), demonstrating broad utility.

## References Worth Chasing

- BERT (Devlin et al., 2019, arXiv:1810.04805) — base architecture; BioBERT initializes from it.
- ELMo (Peters et al., 2018) — contextualized word representations; predecessor approach.
- Word2Vec on biomedical corpora (Pyysalo et al., 2013) — prior domain-adapted word embeddings for biomedicine.
- ClinicalBERT / Publicly Available Clinical BERT (Alsentzer et al., 2019) — extends BioBERT to clinical text.
- SciBERT (Beltagy et al., 2019, arXiv:1903.10676) — concurrent scientific-domain BERT.
- PubMedBERT (Gu et al., 2021, 10.1145/3458754) — from-scratch biomedical BERT; supersedes BioBERT's continued-pretraining approach.
- BioGPT (Luo et al., 2022, arXiv:2210.10341) — generative counterpart to BioBERT.
- CollaboNet (Yoon et al., 2019) — SOTA NER baseline (multi-Bi-LSTM-CRF).
- Giorgi & Bader (2018) — transfer learning for biomedical NER; key NER baseline.
- Habibi et al. (2017) — deep learning with word embeddings for biomedical NER.
- Wang et al. (2018) — cross-type biomedical NER with deep multi-task learning.
- Wiese et al. (2017) — neural domain adaptation for biomedical QA; SQuAD transfer strategy adopted by BioBERT.
- Lim & Kang (2018) — chemical-gene RE baseline.
- BioASQ (Tsatsaronis et al., 2015) — QA benchmark used for evaluation.

## Notes / Open Questions

- Only BERT_BASE used due to computational cost; BERT_LARGE results not reported but planned for future work.
- No from-scratch pre-training on biomedical text was attempted (always initialized from BERT); PubMedBERT later showed from-scratch can be better.
- No domain-specific vocabulary was constructed; later work (PubMedBERT) showed domain vocab can help.
- Total FLOPs / training compute not reported.
- The paper reports 98,304 "words" per iteration, but these are WordPiece tokens (192 × 512); true word count per step is lower.
- ~30% of BioASQ factoid questions were unanswerable in extractive QA and were excluded from training, which may inflate reported scores.
- LINNAEUS scores are lower than SOTA partly because the exact train/test splits from Giorgi & Bader (2018) were unavailable.
- Future versions mentioned (BioBERT_LARGE, domain-specific vocabulary) but no follow-up paper from same authors.

## Ablations (Rev 4)

| # | Ablation axis | Variants compared | Setup / metric | Key result | Take-away |
|---|---|---|---|---|---|
| 1 | Pre-training corpus composition | BERT (Wiki+Books) vs +PubMed (200K) vs +PMC (270K) vs +PubMed+PMC (470K) vs +PubMed 1M (v1.1) | NER micro-F1 over 9 datasets (Table 6) | 83.36 → 85.86 → 85.65 → 86.51 → 86.77; v1.1 best on 6/9 datasets | Continued pre-training on PubMed is the dominant gain; adding PMC gives diminishing returns once PubMed steps are scaled up |
| 2 | Pre-training corpus composition (RE) | Same five variants | RE micro-F1 on GAD, EU-ADR, CHEMPROT (Table 7) | BERT 79.22 → BioBERT v1.0 (+PubMed) best at 80.41 micro-F1 (+2.80 vs SOTA); CHEMPROT F1 64.10 (SOTA) → 73.74 (BERT) → 76.46 (v1.1) | Even vanilla BERT beats the prior CHEMPROT SOTA; biomedical pre-training adds a further ~3 F1 |
| 3 | Pre-training corpus composition (QA) | Same five variants | BioASQ 4b/5b/6b MRR (Table 8) | Micro MRR: SOTA 32.53 → BERT 39.64 → v1.0 (+PubMed) 42.71 → v1.0 (+PubMed+PMC) 44.01 → v1.1 (+PubMed) 44.77 | QA benefits most from biomedical pre-training (+12.24 MRR over SOTA, +5.13 over BERT) — largest relative gain among the three task families |
| 4 | PubMed corpus size | 0 / 1B / 2B / 3B / 4.5B words, fixed 200K steps | NER F1 on NCBI Disease, BC2GM, BC4CHEMD (Fig. 2a) | F1 rises sharply from 0→1B, then improves more slowly to 4.5B with diminishing returns past ~3B | 1B words already captures most of the benefit; full PubMed (4.5B) yields modest extra gains |
| 5 | Number of pre-training steps | Checkpoints from 0 up to ≥200K (v1.0) and 1M (v1.1) on PubMed | NER F1 on NCBI Disease, BC2GM, BC4CHEMD (Fig. 2b) | Monotonic improvement with more steps; v1.1 (1M) beats v1.0 (200K) on micro-F1 (86.77 vs 85.86) | More pre-training compute keeps helping — no saturation observed by 1M steps |
| 6 | Initialization / vocabulary | BERT_BASE (Wiki+Books init, original cased vocab) — kept fixed across all BioBERT variants; no from-scratch or domain-vocab variant trained | Implicit baseline = BERT row in Tables 6–8 | All BioBERT variants improve over BERT despite reusing the general-domain WordPiece vocab | Original BERT vocab is sufficient; subword decomposition + fine-tuning compensates for missing biomedical tokens (later work, e.g. PubMedBERT, contests this) |
| 7 | Cased vs uncased vocabulary | Cased vs uncased BERT WordPiece | Reported qualitatively (Section 4.2) | Cased "results in slightly better performance" — no quantitative table | Minor effect; cased preferred for biomedical NER where casing carries entity signal |
| 8 | Per-dataset BioBERT vs BERT lift | BERT vs BioBERT v1.0 (+PubMed+PMC) across all 15 NER/RE/QA datasets | Absolute F1/MRR delta (Fig. 2c) | Positive on nearly all 15 datasets; largest lifts on BioASQ QA datasets, smallest on already-strong RE benchmarks | Biomedical pre-training helps universally but most where the task requires deep biomedical knowledge (QA) rather than surface patterns |
