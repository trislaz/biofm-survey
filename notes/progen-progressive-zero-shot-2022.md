---
id: progen-progressive-zero-shot-2022
title: 'ProGen: Progressive Zero-shot Dataset Generation via In-context Feedback'
authors:
- Jiacheng Ye
- Jiahui Gao
- Jiangtao Feng
- Zhiyong Wu
- Tao Yu
- Lingpeng Kong
year: 2022
venue: null
arxiv: '2210.12329'
doi: null
url: https://arxiv.org/abs/2210.12329v1
pdf_path: papers/progen-progressive-zero-shot-2022.pdf
md_path: papers/md/progen-progressive-zero-shot-2022.md
modalities:
- other
status: extracted
evidence_quality: low
tags:
- nlp
- zero-shot
- dataset-generation
- in-context-learning
- not-bio-fm
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:59+00:00'
updated_at: '2026-04-22T20:24:32+00:00'
---

## TL;DR

**Not a bio-FM paper.** This is an NLP paper on zero-shot synthetic dataset generation for text classification. It was likely catalogued here due to name collision with [ProGen (Madani et al.)](https://doi.org/10.1038/s41587-022-01618-2), the protein language model. ProGen (Ye et al. 2022) uses a frozen GPT2-XL (1.5B) to synthesize labelled text via prompts, then iteratively improves dataset quality using influence-function feedback and in-context examples. Evaluated on IMDb, SST-2, Rotten Tomatoes, Elec, Yelp. Achieves parity with 1% of the synthetic data compared to baseline ZeroGen.

## Model

- **PLM (generator):** GPT2-XL, 1.5B parameters, frozen, used with nucleus sampling (p=0.9).
- **Task-specific models (TAM):** DistilBERT (66M) and LSTM (~7M), trained on the synthetic dataset and used for downstream inference.
- **Framework:** Progressive zero-shot dataset generation (ProGen). Alternates between (a) generating labelled examples from PLM using in-context feedback and (b) training a TAM on accumulated synthetic data.
- **Feedback mechanism:** Noise-robust influence function (Koh & Liang 2017) with Reverse Cross-Entropy (RCE) loss on a synthetic validation set identifies top-M (50) most helpful samples; these become in-context examples for the next generation round.

## Data

- **Benchmarks (all text classification):** IMDb (25k/25k), SST-2 (6.9k/0.8k), Rotten Tomatoes (8.5k/1k), Elec (25k/25k), Yelp (560k/38k).
- **Synthetic dataset:** 100k examples generated per task (feedback interval I=1k, T=100 iterations).
- **No biological data whatsoever.**

## Training Recipe

- PLM is frozen throughout; only TAM is trained.
- TAM-LSTM: Adam, lr=1e-3, emb_dim=100, hidden=300, 1 layer.
- TAM-DistilBERT: Adam, lr=2e-5, weight_decay=0.01, HuggingFace defaults.
- Influence scores computed on 10k random subset per iteration; feedback applied 50% of the time to preserve diversity.
- Single NVIDIA A100; 100k examples costs ~28h per task.

## Key Ablations & Design Choices

- **ProGen vs ZeroGen (Table 1):** ProGen+DistilBERT avg 86.51 vs ZeroGen 82.94 (+3.6 pp), with dramatically lower variance (±0.84 vs ±4.96).
- **RCE vs CE influence (Table 2, Elec):** RCE-selected helpful examples → 89.00 acc; CE-selected → 87.74; random in-context → 87.94; no feedback baseline → 85.35.
- **Gold in-context upper bound (Table 2):** Using real test-set examples as in-context achieves 91.02 on Elec (vs 89.00 for ProGen).
- **Data efficiency (Fig 5):** ProGen matches ZeroGen-100k performance with only ~1k examples (1%).
- **Number of in-context examples (Fig 4):** ≤8 examples consistently help; more can hurt.
- **In-context format:** Including both positive & negative examples (F-1) generally works; masking labels (F-5) still helps, showing PLM learns distributional cues rather than copying.
- **Dataset quality (Table 3):** ProGen improves MAUVE (distribution similarity) and label correctness at slight cost to Self-BLEU diversity.
- **Prompt robustness:** ProGen narrows the gap between good and bad prompts, making prompt selection less critical.

## Reported Insights

- Influence function with noise-robust loss (RCE) is critical when the validation set is itself synthetic and noisy; vanilla CE influence is no better than random.
- Feedback applied 100% of the time hurts diversity; 50% schedule is a practical sweet spot.
- The framework shares the spirit of self-training but applied to the generator rather than the classifier.
- Limitations: depends on PLM's ability to follow prompts and having seen task-relevant data during pre-training; influence function computation is expensive.

## References Worth Chasing

1. Ye et al. 2022 — ZeroGen: zero-shot dataset generation baseline.
2. Meng et al. 2022 — Generating training data with language models (SuperGen).
3. Brown et al. 2020 — GPT-3, in-context learning.
4. Koh & Liang 2017 — Influence functions.
5. Wang et al. 2019 — Symmetric cross-entropy / RCE loss.
6. Holtzman et al. 2021 — Calibrated prompting (PROMPTING*).
7. Schick & Schütze 2021 — PET, pattern-exploiting training.

## Notes / Open Questions

- **This paper is not relevant to the bio-FM survey.** It shares a name with the protein-sequence ProGen (Madani et al., Nature Biotechnology 2023) but is an entirely different work in NLP zero-shot text classification.
- Consider removing from the survey or re-tagging to avoid confusion.
- If the protein ProGen is desired, the correct paper is arXiv:2004.03497 / doi:10.1038/s41587-022-01618-2.
