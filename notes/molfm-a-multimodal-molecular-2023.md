---
id: molfm-a-multimodal-molecular-2023
title: 'MolFM: A Multimodal Molecular Foundation Model'
authors:
- Yizhen Luo
- Kai Yang
- Massimo Hong
- Xing Yi Liu
- Zaiqing Nie
year: 2023
venue: null
arxiv: '2307.09484'
doi: null
url: https://arxiv.org/abs/2307.09484v2
pdf_path: papers/molfm-a-multimodal-molecular-2023.pdf
md_path: papers/md/molfm-a-multimodal-molecular-2023.md
modalities:
- small-molecule
- multimodal
status: extracted
evidence_quality: medium
tags:
- knowledge-graph
- contrastive-learning
- cross-modal-retrieval
- molecule-captioning
- text-to-molecule-generation
- property-prediction
- multimodal-fusion
- deep-metric-learning
parameters: ~138M total (structure 1.8M + text 61.8M + KG 12.6M + multimodal encoder
  61.8M)
training_tokens: null
training_compute: 300 epochs, batch 128, 4×A100 GPUs
references_chased: false
added_at: '2026-04-22T19:42:13+00:00'
updated_at: '2026-04-22T20:22:55+00:00'
is_fm: true
fm_classification_reason: 'MolFM: pretrained multimodal molecular FM.'
---

## TL;DR

MolFM is a multimodal molecular FM that jointly learns from 2D molecular graphs, biomedical texts, and knowledge graphs via cross-modal attention and four pre-training objectives (structure-text contrastive, cross-modal matching, MLM, KG embedding). Trained on only ~15K molecules + 37M paragraphs + a 49K-entity KG, it achieves SOTA on cross-modal retrieval (+12% zero-shot MRR over MoMu), molecule captioning, text-to-molecule generation, and molecular property prediction (MoleculeNet). Theoretical analysis shows the objectives minimise cross-modal distance for same-molecule features and pull together structurally/functionally similar molecules.

## Model

- **Architecture**: Three single-modal encoders → one multimodal fusion encoder.
  - **Structure encoder**: 5-layer GIN (1.8M params), init from GraphMVP. Produces atom-level features h_SA and graph-level h_SM.
  - **Text encoder**: 6-layer Transformer (61.8M params), init from first 6 layers of KV-PLM. Produces token features h_T.
  - **Knowledge encoder**: TransE (12.6M params), pre-trained 500 epochs on KG. Embeds each entity in K.
  - **Multimodal encoder**: 6-layer Transformer with cross-attention (61.8M params), init from last 6 layers of KV-PLM. Queries = text tokens h_T, keys/values = concat(atom h_SA, neighbor h_K).
- **KG input formulation**: For each molecule, sample the entity node + N=4 random 1-hop neighbours from the KG.
- **Total params**: ~138M.

## Data

- **Molecule-text pairs**: 15,613 molecules from PubChem + 37M paragraphs from S2ORC (following MoMu pipeline; simple name-based matching).
- **Knowledge graph**: 49,111 entities (29K molecules, 19.6K diseases, 403 proteins) and 3.25M relations (drug-target interaction, drug-drug interactions in 12 categories, drug-drug similarity, drug-disease associations). Built from DrugBank, BindingDB, FORUM, MHFP fingerprint similarity (threshold 0.8).
- **Downstream benchmarks**: PCdes (cross-modal retrieval), ChEBI-20 (captioning + generation), MoleculeNet 8 classification datasets.

## Training Recipe

1. **Single-modal pre-training**: Structure encoder from GraphMVP (self-supervised on 3D geometry); text encoder from KV-PLM (biomedical LM); KG encoder TransE trained 500 epochs.
2. **Multimodal pre-training**: Joint optimisation of four losses (equal weight): L = L_stc + L_cmm + L_mlm + L_kge.
   - **STC** (structure-text contrastive): InfoNCE on graph-level z_S vs [CLS] z_T, τ=0.1.
   - **CMM** (cross-modal matching): Binary prediction whether (S, T, K) triplet is matched; negatives by random permutation.
   - **MLM** (masked language modelling): BERT-style masking on text; prediction uses multimodal encoder conditioned on all three modalities.
   - **KGE** (KG embedding): TransE max-margin loss on sampled positive/negative triplets as regularisation, margin Δ=0.2.
3. **Optimiser**: AdamW, weight decay 1e-4, LR warmup to 1e-4 over 2K iters → cosine anneal to 1e-5.
4. **Schedule**: 300 epochs, batch size 128, 4× NVIDIA A100 GPUs.
5. **Fine-tuning**: Task-specific heads; AdamW, LR ∈ {1e-4, 3e-4, 1e-3}, 100–200 epochs, early stopping patience 20, scaffold split. Retrieval uses re-ranking with ensemble of cosine sim + CMM logits.

## Key Ablations & Design Choices

- **Cross-modal attention to atoms is critical**: Removing atom attention in multimodal encoder drops zero-shot retrieval from 26.27→23.45 (S-T) and 28.78→25.89 (T-S). Largest single-component drop.
- **CMM loss is essential**: Removing CMM causes similar degradation (23.48 / 25.96), confirming fine-grained matching matters more than contrastive alone.
- **Knowledge graph adds ~1.5% average**: Removing KG input (keeping same losses minus KGE) drops retrieval by ~1.5% on average. Both neighbour attention and KGE contribute independently.
- **Re-ranking helps modestly**: +1.0 / +0.65 MRR from cosine+CMM ensemble re-ranking of top-k.
- **Removing KG + CMM together**: Worst variant (22.07 / 24.48), showing compounding effect.
- **Number of neighbours N**: Performance plateaus at N=4; beyond that, sparse KG means redundant neighbours. N=4 used throughout.
- **Property prediction gains from multimodal input**: MolFM (w/ T+K) achieves 74.62 avg ROC-AUC vs 73.95 (structure only) vs 73.07 (GraphMVP) on MoleculeNet. Gains largest on Tox21, HIV, BACE.
- **Structure encoder alone already improves**: Even without text/KG at inference, MolFM's structure encoder (pre-trained multimodally) beats GraphMVP on most tasks, indicating knowledge transfer into the GNN.
- **Small pre-training data still effective**: Only 15K molecules, yet strong zero-shot retrieval, suggesting cross-modal + KG learning is data-efficient.

## Reported Insights

- Theoretical analysis connects CMMloss to deep metric learning: CMM aligns multimodal representations by scoring matched triplets higher (Eq. 6).
- KGE loss proven to pull structurally similar molecules closer (Lemma 1: symmetric relation r_s → g(r_s)→0, so L_kge ∝ 2‖f(h)−f(t)‖ minus negatives) and bound distance for functionally similar molecules sharing intermediate entities (Lemma 2: ‖f(h)−f(t)‖ ≤ αE[L_kge]+C, α≈1, C≈0).
- Cross-modal attention visualisation shows grounding: atoms highlighted by attention correspond to substructures described in text; neighbour attention captures relevant KG entities (e.g., drug interactions, disease associations).
- Molecule captioning examples show MolFM better captures complex functional groups (oligosaccharides) and molecular properties (inhibitory effects) vs MoMu/MolT5.
- Limitation: newly emerged molecules without text/KG data see limited benefit. Authors note incorporating proteins, genes, cell lines as future work.

## References Worth Chasing

1. **MoMu** (Su et al. 2022) — contrastive molecule-text model; main baseline [ref 10]
2. **MoleculeSTM** (Liu et al. 2022) — multi-modal molecule structure-text model [ref 11]
3. **KV-PLM** (Zeng et al. 2022) — bridging molecule structure and biomedical text [ref 8]
4. **GraphMVP** (Liu et al. 2022) — 3D geometry pre-training for molecular graphs [ref 23]
5. **MolT5** (Edwards et al. 2022) — translation between molecules and natural language [ref 9]
6. **DeepEIK** (Luo et al. 2023) — explicit+implicit knowledge for drug discovery [ref 15]
7. **Text2Mol** (Edwards et al. 2021) — cross-modal molecule retrieval with NL queries [ref 16]
8. **CLIP / ALIGN** (Radford et al. 2021; Jia et al. 2021) — vision-language contrastive learning foundations [refs 3, 2]
9. **ALBEF** (Li et al. 2021) — align before fuse; VLP with momentum distillation [ref 5]
10. **GIN** (Xu et al. 2018) — graph isomorphism network [ref 38]
11. **TransE** (Bordes et al. 2013) — translating embeddings for KG [ref 40]
12. **MoCL** (Sun et al. 2021) — knowledge-aware contrastive learning for molecules [ref 36]
13. **KCL** (Fang et al. 2022) — chemical element knowledge graph for molecular contrastive learning [ref 37]
14. **MoleculeNet** (Wu et al. 2018) — molecular ML benchmark [ref 17]
15. **SciBERT** (Beltagy et al. 2019) — pre-trained LM for scientific text [ref 27]

## Notes / Open Questions

- Pre-training data is small (15K molecules) compared to later models; unclear how performance scales with more data.
- KG construction depends on heuristic rules and database coverage — how sensitive are results to KG quality/completeness?
- No 3D conformer information used despite GraphMVP init; would adding 3D geometry as a fourth modality help?
- TransE is a simple KG embedding; would more expressive methods (RotatE, CompGCN) improve KG integration?
- Downstream text/KG input requires SMILES matching to ChEBI-20 and KG — many molecules in MoleculeNet have no text (e.g., BACE: only 3/1513 linked to text). Impact of this sparsity on property prediction gains is unclear.
- Code at https://github.com/BioFM/OpenBioMed.

## Ablations (Rev 4)

Zero-shot paragraph-level cross-modal retrieval on PCdes (avg of R@1, R@5, R@10). S-T = structure→text, T-S = text→structure. Source: Table 1, §5.1.

| # | Variant                       | S-T   | T-S   | Δ S-T vs full | Δ T-S vs full | Component probed                                  |
|---|-------------------------------|-------|-------|---------------|---------------|---------------------------------------------------|
| 1 | MolFM (full)                  | 26.27 | 28.78 | —             | —             | Reference                                         |
| 2 | w/o re-rank                   | 25.22 | 28.13 | −1.05         | −0.65         | ITM-based re-ranking at inference                 |
| 3 | w/o attention to atoms        | 23.45 | 25.89 | −2.82         | −2.89         | Cross-modal attention from text to atom tokens    |
| 4 | w/o attention to neighbors    | 25.23 | 28.49 | −1.04         | −0.29         | Attention to KG neighbour entities                |
| 5 | w/o knowledge                 | 24.66 | 27.33 | −1.61         | −1.45         | Entire KG input branch removed                    |
| 6 | w/o KGE                       | 25.81 | 28.24 | −0.46         | −0.54         | TransE knowledge-graph embedding pre-training     |
| 7 | w/o CMM                       | 23.48 | 25.96 | −2.79         | −2.82         | Cross-modal matching pre-training objective       |
| 8 | w/o knowledge + CMM           | 22.07 | 24.48 | −4.20         | −4.30         | Joint removal of KG branch and CMM objective      |

Additional ablation (Appendix E, Fig. A.3): varying number of KG neighbours N. Performance improves with N up to 4; beyond N=4 gains plateau, attributed to KG sparsity (few entities have >4 neighbours) and redundancy in additional neighbour information.

**Top take-away:** the two largest single-component drops both come from pre-training/architecture choices that bind text to molecular structure — removing cross-modal attention to atoms (−2.8 avg) or the cross-modal matching (CMM) objective (−2.8 avg) hurts far more than removing the knowledge-graph branch (−1.5 avg) or KGE (−0.5 avg). Fine-grained substructure↔word alignment via CMM is the core driver of MolFM's gains; the KG is a useful but secondary contributor (~1.5% avg), and combined removal of KG + CMM compounds losses to ~4.3 points, the worst configuration.

