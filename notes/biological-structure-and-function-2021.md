---
id: biological-structure-and-function-2021
title: Biological structure and function emerge from scaling unsupervised learning
  to 250 million protein sequences
authors:
- Alexander Rives
- Joshua Meier
- Tom Sercu
- Siddharth Goyal
- Zeming Lin
- Jason Liu
- Demi Guo
- Myle Ott
- C. Lawrence Zitnick
- Jerry Ma
- Rob Fergus
year: 2021
venue: PNAS
arxiv: null
doi: 10.1073/pnas.2016239118
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/biological-structure-and-function-2021.md
modalities:
- protein-sequence
status: extracted
evidence_quality: full-text
tags:
- protein-language-model
- transformer
- masked-language-modeling
- unsupervised-representation-learning
- scaling-laws
- contact-prediction
- secondary-structure
- remote-homology
- mutational-effect
- ESM-1b
parameters: 650000000
training_tokens: 86000000000
training_compute: null
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

ESM-1b is a 650 M-parameter, 33-layer Transformer trained with masked language modeling on 86 billion amino acids from 250 million protein sequences (UniRef50). Without any structural supervision, the learned representations encode biochemical properties, secondary structure, tertiary contacts, remote homology, and mutational effects. Linear projections of representations outperform CCMpred (direct coupling analysis) for long-range contact prediction on held-out folds. Combining ESM-1b features with MSA-derived features improves SOTA on secondary structure (73.6% Q8 on CB513) and contact prediction (+3.9 pp top-L long-range precision on RaptorX test set). Fine-tuning matches Envision SOTA on mutational effect prediction from sequence alone. A key finding is a linear relationship between language modeling perplexity (ECE) and structural information in representations, suggesting further scaling will yield better representations.

## Model

- **Architecture**: Deep Transformer (BERT-style encoder) with masked language modeling objective.
- **ESM-1b**: 33 layers, ~650 M parameters, trained on UR50/S. Hyperparameters identified via systematic search on 100 M-parameter models, then scaled up.
- **Exploration series**: 6-layer (42.6 M params), 12-layer (85.1 M params), and 34-layer (~670 M params) Transformers; also bidirectional LSTM baselines (~25 M and ~113 M params).
- **Input**: Single amino acid sequences, character-level tokenization (20 canonical amino acids + special tokens = 25 unique tokens).
- **Objective**: Masked language modeling (MLM) — corrupt input by masking a fraction of amino acids, predict masked tokens from context. Loss: per-token negative log-likelihood.
- **Output representations**: Per-residue hidden states from the final layer; protein-level embedding obtained by averaging across positions.
- **Downstream heads**: Linear projections (logistic regression for SSP, dot-product regression for contacts), deep neural networks (NetSurf architecture for SSP, dilated convolutional ResNet for contacts), and fine-tuning (for mutational effect prediction).

## Data

- **Pre-training**: UniParc — 250 M sequences, 86 B amino acids. 1 M sequences held out for validation.
- **Diversity variants**: Three training datasets explored:
  - UR100: UniRef100 representative sequences (low diversity).
  - UR50/S: UniRef50 representative sequences (high diversity, sparse — ~45 M seqs).
  - UR50/D: UniRef100 sequences sampled evenly across UniRef50 clusters (high diversity, dense).
- **Evaluation clustering**: 10% of UniRef50 clusters held out; all sequences belonging to held-out clusters removed from all pre-training datasets.
- **Downstream evaluation**:
  - Remote homology: SCOPe database (family, superfamily, fold levels; Rossmann-like folds and β-propellers excluded).
  - Secondary structure: SCOPe-derived 15,297 structures for linear projections (5-fold CV at family/SF/fold); CB513 and CASP13 for deep NN benchmarks (NetSurf train set, 25% seq-id holdout for CB513, temporal for CASP13).
  - Contacts: Same SCOPe dataset for linear projections; RaptorX train/test sets + CASP11/12/13 for deep NN benchmarks.
  - Mutational effect: Envision (12 proteins, ~700k variants) and DeepSequence (100+ mutagenesis datasets) — 5-fold CV with 80/20 splits.
  - MSAs for baselines: Generated from UniClust30 using 3 iterations of HHblits.

## Training Recipe

- **Objective**: Masked language modeling (Eq. 1 in paper). Fraction of positions masked and replaced with a mask token; model trained to predict the true amino acid at masked positions.
- **Evaluation metric**: Exponentiated cross entropy (ECE) = 2^{L_MLM}; ranges from 1 (perfect) to 25 (random).
- **Hyperparameter search**: Systematic optimization on 100 M-parameter models (details in SI Appendix B); best hyperparameters scaled to 650 M model.
- **Hardware / compute**: Not explicitly disclosed for ESM-1b; described as "comparable in size to large text datasets" used for NLP models.
- **Underfitting**: Even the largest models (~650–700 M params) under-fit on all datasets, indicating room for further scaling.
- **Key ECE results** (Table 1):
  - n-gram best: 17.18 (context 4).
  - LSTM small (25 M): 14.4; LSTM large (113 M): 13.5.
  - Transformer 6-layer (42.6 M): 11.79; 12-layer (85.1 M): 10.45.
  - Transformer 34-layer on UR100: 9.83; UR50/S: 9.27; UR50/D: 8.46.
  - ESM-1b (33-layer, UR50/S): best among all models evaluated.
- **Data scaling**: Training 34-layer models on 0.1%, 1%, 10%, 100% of UR50/S shows monotonic improvement with more data.

## Key Ablations & Design Choices

### 1. Architecture: Transformer vs LSTM (Table 1)
- 6-layer Transformer (42.6 M) beats large LSTM (113 M) on ECE: 11.79 vs 13.5 — Transformers are more parameter-efficient for protein language modeling.
- 12-layer Transformer (85.1 M): ECE 10.45, further confirming Transformer superiority.

### 2. Model Capacity (Table 1)
- 34-layer Transformer (~670 M) on UR50/S: ECE 9.27 vs 12-layer (85.1 M): ECE 10.45 — increased capacity monotonically improves language modeling.
- All large models still under-fit, suggesting further scaling would help.

### 3. Training Data Diversity (Table 1)
- UR50/D (high diversity, dense): ECE 8.46 — best overall.
- UR50/S (high diversity, sparse): ECE 9.27.
- UR100 (low diversity): ECE 9.83.
- Clustering-based diversity reweighting substantially improves generalization (+1.37 ECE from UR100 → UR50/D).

### 4. Data Quantity (Table 1)
- 34-layer on 0.1% / 1% / 10% / 100% UR50/S: monotonic improvement in ECE with more data.

### 5. Linear Projections: Structural Information by Layer Depth (Table 3, Fig. 6)
- Secondary structure Q8 accuracy (fold-level holdout): Transformer 34L UR50/S linear projection: 55.3 ± 1.3% vs sequence profile: 43.2 ± 0.2% vs CCMpred: N/A.
- Contact top-L long-range precision (fold-level holdout): Transformer 34L UR50/S: 18.8 ± 0.6% vs CCMpred: 17.4 ± 0.3%.
- Before pretraining, virtually no structural information is recoverable by linear projections (SSP ~20%, contacts ~3%).
- Training diversity matters more for contacts than SSP: UR50 datasets show pronounced improvement over UR100 for contacts.
- Structural information generalizes across folds: fold-level holdout shows modest degradation vs family-level, confirming representations capture general structural principles.

### 6. Language Modeling ↔ Structure Learning Correlation (Fig. 6)
- Linear relationship between ECE and structural content across training checkpoints: lower ECE → more structural info, for both SSP and contacts.
- This holds across all model sizes (6-layer, 12-layer, 34-layer), implying ECE is a reliable proxy for representation quality.
- Demonstrated for both linear projections and deep prediction heads (SI Appendix Fig. S4).

### 7. Single-Family vs Multi-Family Pre-training (SI Table S2)
- 12-layer Transformers trained on individual Pfam families (ABC transporter, kinase, response regulator) have worse within-family SSP accuracy than the full UniParc-trained model, even when evaluated on the same family.
- Structural knowledge from training across evolutionary diversity transfers to individual families — multi-family pretraining is strictly superior.

### 8. Deep NN Secondary Structure Prediction (Table 4)
- ESM-1b features: 71.6% Q8 on CB513 — matches HMM profiles (71.2%) and exceeds published RaptorX (70.6%).
- Pretraining diversity effect: UR50 datasets give significant accuracy boosts over UR100.
- Transformer features > LSTM features at comparable parameter counts.

### 9. Deep NN Contact Prediction (Table 5)
- ESM-1b best on Transformer representations: 50.2% top-L long-range on RaptorX test set vs RaptorX features: 59.4%.
- Representations alone do not match MSA-derived features for contacts, unlike SSP where they are competitive.
- Diversity and capacity effects consistent: UR50 > UR100; 34-layer > 12-layer > 6-layer.

### 10. Feature Combination (Tables 6–7)
- SSP: ESM-1b avg features + HMM profiles → 73.6% Q8 on CB513 (+2.5 pp over profiles alone), SOTA.
- Contacts: ESM-1b cov features + RaptorX features → 63.3% top-L on RaptorX test (+3.9 pp), +1.8 pp on CASP13.
- Feature combination methods: direct (single-sequence embedding), avg (MSA-averaged embedding), cov (pairwise covariance from MSA after PCA). Cov > avg > direct for contacts.
- Demonstrates ESM-1b captures information orthogonal to MSA-based features.

### 11. Mutational Effect Prediction (Fig. 7, SI Table S5)
- Fine-tuned ESM-1b (34L, UR50/S) exceeds Envision on 10/12 proteins despite lacking structural features.
- Outperforms LSTM baselines on both Envision and DeepSequence datasets.
- Leave-one-out cross-protein generalization: ESM-1b beats Envision on 5/9 tasks.

### 12. Embedding Space Organization
- t-SNE of output embeddings clusters amino acids by hydrophobicity, polarity, aromaticity, molecular weight, and charge — learned purely from sequences.
- PCA of protein-level embeddings recovers species and orthology as primary axes of variation — absent before training.
- Remote homology detection (Table 2): Transformer embeddings achieve fold-level Hit-10 of 11.7% and AUC 0.65, comparable to HHblits (Hit-10 22.4%, AUC 0.69). Superfamily-level AUC: Transformer 0.80 vs HHblits 0.94.

## Reported Insights

- **Structural information emerges from sequence modeling alone**: No structural labels are used during pretraining, yet representations encode SSP, contacts, and remote homology. This validates the hypothesis that protein structure constrains sequence evolution in learnable ways.
- **Language modeling fidelity is a proxy for structure learning**: The linear ECE ↔ structural content relationship means improving language modeling directly improves structural representations.
- **Diversity > quantity for pre-training data**: Clustering-based reweighting toward diverse sequences (UniRef50) consistently outperforms raw UniRef100 sequences across all downstream tasks.
- **Transformers are strictly superior to LSTMs** for protein sequence modeling at comparable capacity, likely due to self-attention's ability to model residue–residue interactions directly.
- **Multi-family pretraining transfers**: Training across evolutionary diversity yields better within-family representations than training on any single family.
- **Representations contain information orthogonal to MSAs**: Feature combination consistently improves SOTA MSA-based methods, indicating the Transformer captures patterns not accessible through traditional alignment.
- **Still under-fitting at 650 M params**: Even the largest models have not saturated, suggesting scaling to billions of parameters will yield further improvements (foreshadowing ESM-2).
- **Representations → fast inference**: Protein-level embeddings enable millisecond-scale similarity search via vector nearest neighbors, vs. minutes for HHblits-based alignment.

## References Worth Chasing

- Alley et al. (ref 66) — UniRep: LSTM protein language model, early baseline for transfer learning from sequences
- Heinzinger et al. (ref 67) — SeqVec/ProtTrans: LSTM/Transformer PLMs trained on UniRef50, concurrent work
- Rao et al. (ref 68) — TAPE: 12-layer Transformer on Pfam, benchmark for protein transfer learning
- Bepler & Berger (ref 70) — Pretrained LSTMs with contact supervision, hybrid supervised+unsupervised approach
- Riesselman et al. / DeepSequence (ref 26) — Deep generative model (VAE) for single-family mutational effect prediction
- Gray et al. / Envision (ref 64) — Supervised mutational effect prediction using structural/evolutionary features
- Marks et al. / DCA (refs 17–19) — Direct coupling analysis / Markov random field for contact prediction from MSAs
- Wang et al. / RaptorX (ref 54, 59) — SOTA deep ResNet for contact prediction, CASP12/13 winner
- Vaswani et al. / Transformer (ref 32) — Original Transformer architecture
- Devlin et al. / BERT (ref 6) — Masked language modeling objective and deep Transformer pretraining
- Radford et al. / GPT-2 (ref 11) — Scaling language models, underfitting observations
- Suzek et al. / UniRef (ref 34) — UniRef50/90/100 clustering methodology
- Rao et al. (ref 73) — Transformer PLMs as unsupervised structure learners (attention-based contact prediction)
- Lin et al. / ESM-2 (ref 65, preprint) — Scaling protein language models to 15B parameters

## Notes / Open Questions

- **Training compute not disclosed**: No wall-clock time, GPU/TPU hours, or FLOPs reported for ESM-1b. Hardware details only stated as "comparable" to NLP models.
- **ESM-1b hyperparameter details sparse**: The systematic search on 100 M models is deferred to SI Appendix B; specific learning rate, batch size, optimizer, and training schedule for the final 650 M model are not in the main text.
- **Token count ambiguity**: 86 B amino acids is the total dataset size, but the number of tokens actually seen during training (i.e., epochs × dataset size) is not reported.
- **Contact prediction gap**: Single-sequence representations still substantially lag MSA-derived features (50.2 vs 59.4 on RaptorX test), unlike SSP where parity is reached. This gap motivated MSA Transformer and ESM-2 follow-up work.
- **No attention analysis**: Unlike the concurrent Rao et al. (2020) "unsupervised structure learners" paper, this work focuses on hidden representations rather than attention maps. The relative value of attention vs embedding for contacts was debated (later resolved by Ankh showing embeddings are generally superior).
- **Evaluation limited to structure and fitness**: No evaluation on protein–protein interaction, function annotation (GO terms), localization, or other biologically important tasks.
- **UR50/D not used for ESM-1b**: Despite UR50/D yielding the best ECE (8.46), ESM-1b was trained on UR50/S. Rationale not discussed — possibly computational cost of the denser sampling.
- **Underfitting claim → scaling trajectory**: The explicit underfitting observation at 650 M parameters directly motivated the ESM-2 scaling study (up to 15B params) by the same group.

## Verification (Rev 3)

Six claims in `insights.md` cite `[biological-structure-and-function-2021]`. Each was checked against the full PMC text.

| Line | Claim (paraphrased) | Verdict | Evidence |
|------|----------------------|---------|----------|
| 18 | UniRef50 (diverse, clustered) outperforms larger but redundant corpora | **supported** | Table 1: UR50/S ECE 9.27, UR50/D 8.46 vs UR100 9.83. Text: "Transformers trained on the two high-diversity datasets … improve generalization over the UR100 low-diversity dataset." |
| 69 | ESM-1b uses single-amino-acid tokens (20 standard + special = 25) | **supported** | Paper: "protein sequences use a small vocabulary of 20 canonical elements"; ECE upper bound is 25 "the number of unique amino acid tokens in the data." |
| 102 | ESM-1b is a 650 M-param, 33-layer conventional encoder Transformer | **supported** | Paper: "∼650 M parameters (33 layers)" trained with "masked language modeling objective (6)" (BERT), i.e. encoder-only architecture. |
| 158 | ESM-1b uses masked language modelling (MLM) | **supported** | Paper Eq. 1 and text: "We train models using the masked language modeling objective (6)." |
| 218 | UniRef50 > redundant corpora; model still underfitting at 650 M params | **supported** | Diversity: Table 1 (see line 18). Underfitting: "Underfitting is observed even for the largest models trained on 100% of UR50/S, suggesting potential for additional improvements with higher capacity models." |
| 441 | Internal representations' structural content linearly correlates with ECE; diversity outperforms quantity | **supported** | Fig. 6 and text: "Fig. 6 shows a linear relationship between the language modeling objective and information about structure, which is maintained over the course of pretraining." Diversity: Table 1 as above. |

**Summary: 6/6 supported, 0 partial, 0 unsupported, 0 out-of-scope.**
