---
id: chemberta-large-scale-self-2020
title: 'ChemBERTa: Large-Scale Self-Supervised Pretraining for Molecular Property
  Prediction'
authors:
- Seyone Chithrananda
- Gabriel Grand
- Bharath Ramsundar
year: 2020
venue: null
arxiv: '2010.09885'
doi: null
url: https://arxiv.org/abs/2010.09885v2
pdf_path: papers/chemberta-large-scale-self-2020.pdf
md_path: papers/md/chemberta-large-scale-self-2020.md
modalities:
- small-molecule
status: extracted
evidence_quality: full-text
tags: ["transformer", "RoBERTa", "SMILES", "SELFIES", "masked-language-modeling", "molecular-property-prediction", "self-supervised", "PubChem", "MoleculeNet", "attention-visualization", "tokenization", "BPE"]
parameters: "not reported (estimated ~83M from RoBERTa config: 6 layers, 12 heads, 768 hidden)"
training_tokens: "not reported (largest run: 10M SMILES × 3 epochs)"
training_compute: "~48 V100-hours (10M-subset run); 17.1 kg CO₂eq"
references_chased: false
added_at: '2026-04-22T21:55:42+00:00'
updated_at: '2026-04-22T21:55:43+00:00'
---

## TL;DR

ChemBERTa is one of the first systematic attempts to apply BERT-style transformers to molecular property prediction using SMILES strings. Built on a 6-layer RoBERTa architecture, it is pretrained with masked language modeling (MLM) on up to 10M compounds from a curated 77M PubChem SMILES corpus. On four MoleculeNet classification tasks (BBBP, ClinTox, HIV, Tox21), ChemBERTa approaches but does not beat D-MPNN / RF / SVM baselines. However, downstream ROC-AUC scales consistently with pretraining dataset size (ΔROC-AUC = +0.110 from 100K→10M). The paper also ablates BPE vs. SMILES tokenization (slight edge to SMILES tokenizer) and SMILES vs. SELFIES (no significant difference), and demonstrates attention-based visualization of chemically relevant substructures. The released 77M SMILES dataset was influential for subsequent molecular language models.

## Model

- **Architecture**: Encoder-only (bidirectional) transformer based on RoBERTa, implemented via HuggingFace.
- **Layers / heads**: 6 layers, 12 attention heads → 72 distinct attention mechanisms.
- **Hidden dimension**: Not stated in paper; standard RoBERTa config implies 768.
- **Vocab size**: 52K tokens (max).
- **Max sequence length**: 512 tokens.
- **Tokenization**: Default is Byte-Pair Encoding (BPE) from HuggingFace tokenizers; also tested a regex-based SmilesTokenizer (released in DeepChem).
- **Parameters**: Not explicitly reported. Estimated ~83M based on 6-layer RoBERTa with 768 hidden and 52K vocab.

## Data

- **Pretraining corpus**: 77M unique canonical SMILES from PubChem (globally shuffled). Only subsets were used for pretraining: 100K, 250K, 1M, 10M. Full 77M training was left to future work.
- **Downstream benchmarks**: Four MoleculeNet classification tasks with scaffold splits (80/10/10):
  - BBBP (2,039 compounds, blood-brain barrier penetrability)
  - ClinTox CT_TOX (1,478 compounds, clinical toxicity)
  - HIV (41,127 compounds, HIV replication inhibition)
  - Tox21 SR-p53 (7,831 compounds, p53 stress-response pathway activation)
- **Baselines**: Directed-MPNN (D-MPNN), Random Forest (RF), SVM — all from Chemprop using 2048-bit Morgan fingerprints.

## Training Recipe

- **Pretraining objective**: Masked language modeling (MLM), masking 15% of tokens per input.
- **Epochs**: 10 epochs on 100K / 250K / 1M subsets; 3 epochs on 10M subset (to avoid overfitting).
- **Hardware**: Single NVIDIA V100 GPU.
- **Wall-clock time**: ~48 hours for the 10M subset pretraining.
- **Carbon footprint**: ~17.1 kg CO₂eq (Google Cloud Platform, certified carbon-neutral).
- **Fine-tuning**: Linear classification head appended; full model backpropagation; up to 25 epochs with early stopping on ROC-AUC.
- **String representations tested**: Canonical SMILES (default) and SELFIES.

## Key Ablations & Design Choices

- **Pretraining data scaling** (100K → 250K → 1M → 10M): Mean ΔROC-AUC = +0.110, ΔPRC-AUC = +0.059 across BBBP, ClinTox, Tox21 (HIV omitted due to resource constraints). Consistent monotonic improvement with more data.
- **ChemBERTa-10M vs. baselines** (ROC-AUC / PRC-AUC):
  - BBBP: 0.643 / 0.620 (vs. D-MPNN 0.708 / 0.697)
  - ClinTox: 0.733 / 0.975 (vs. D-MPNN 0.906 / 0.993)
  - HIV: 0.622 / 0.119 (vs. D-MPNN 0.752 / 0.152)
  - Tox21: 0.728 / 0.207 (vs. D-MPNN 0.688 / 0.429). ROC beats D-MPNN but PRC is much lower.
- **BPE vs. SmilesTokenizer** (1M subset, Tox21 SR-p53): SmilesTokenizer outperforms BPE by ΔPRC-AUC = +0.015. Semantically meaningful tokenization may help.
- **SMILES vs. SELFIES** (1M subset, Tox21 SR-p53): No significant difference in downstream performance despite SELFIES guaranteeing valid molecules.

## Reported Insights

- Transformers on SMILES are a viable (though not yet SotA) alternative to GNN + fingerprint approaches for molecular property prediction.
- Pretraining dataset size is a key lever: performance scales monotonically from 100K to 10M, suggesting further gains from training on the full 77M corpus.
- The existing software ecosystem (HuggingFace, BertViz) transfers directly to molecular data, lowering engineering cost.
- Attention heads learn chemically meaningful patterns: some neurons are selective for functional groups and aromatic rings; others track bracket closures in SMILES (analogous to parenthesis tracking in NLP).
- SELFIES, despite 100% syntactic validity, does not outperform SMILES—suggesting the MLM task does not benefit from guaranteed valid reconstructions.

## References Worth Chasing

- RoBERTa (Liu et al., 2019, arXiv:1907.11692) — base architecture for ChemBERTa
- BERT (Devlin et al., 2019) — foundational masked LM pretraining
- SMILES Transformer (Honda et al., 2019, arXiv:1911.04738) — earlier SMILES-based pretrained transformer (861K ChEMBL)
- SMILES-BERT (Wang et al., 2019) — SMILES-based BERT pretrained on 18.7M ZINC compounds
- Molecule Attention Transformer (Maziarka et al., 2020, arXiv:2002.08264) — hybrid graph-transformer for molecules (2M ZINC)
- SELFIES (Krenn et al., 2020) — 100% robust molecular string representation tested in this work
- Molecular Transformer (Schwaller et al., 2019) — transformer for chemical reaction prediction; source of SMILES regex tokenizer
- MoleculeNet (Wu et al., 2018) — benchmark suite used for downstream evaluation
- Chemprop / D-MPNN (Yang et al., 2019) — primary baseline; directed message-passing neural network
- Strategies for Pre-training GNNs (Hu et al., 2019, arXiv:1905.12265) — systematic GNN pretraining study that inspired this work
- ELECTRA (Clark et al., 2020, arXiv:2003.10555) — alternative pretraining strategy mentioned as future work
- DeepChem (Ramsundar et al., 2016) — open-source toolkit used for data splitting and tokenizer hosting
- PubChem (Kim et al., 2019) — source of the 77M SMILES pretraining corpus

## Notes / Open Questions

- The paper only pretrained on up to 10M of the 77M available SMILES. ChemBERTa-2 (Ahmad et al., 2022) later scaled to the full 77M with multi-task pretraining and significantly improved results.
- Parameter count is never stated; the architecture description (6 layers, 12 heads) implies a smaller-than-base RoBERTa but still ~83M given 52K vocab.
- No hyperparameter search is reported for pretraining (LR, batch size, warmup, etc.) — likely using RoBERTa defaults.
- HIV task was omitted from the scaling analysis due to resource constraints; it is the largest dataset (41K) and might show different scaling behavior.
- Tox21 ROC-AUC exceeds D-MPNN but PRC-AUC is much worse — class imbalance handling may be an issue.
- No regression tasks evaluated; only binary classification from MoleculeNet.
- Comparison is limited to a single GNN baseline (D-MPNN) and classical methods; no comparison with other molecular pretrained models (e.g., SMILES-BERT, SMILES Transformer).
- The 77M PubChem SMILES dataset released with this work became a widely adopted pretraining resource for subsequent molecular FMs.
