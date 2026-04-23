---
id: helixfold-single-msa-free-2022
title: 'HelixFold-Single: MSA-free Protein Structure Prediction by Using Protein Language
  Model as an Alternative'
authors:
- Xiaomin Fang
- Fan Wang
- Lihang Liu
- Jingzhou He
- Dayong Lin
- Yingfei Xiang
- Xiaonan Zhang
- Hua Wu
- Hui Li
- Le Song
year: 2022
venue: null
arxiv: '2207.13921'
doi: null
url: https://arxiv.org/abs/2207.13921v3
pdf_path: papers/helixfold-single-msa-free-2022.pdf
md_path: papers/md/helixfold-single-msa-free-2022.md
modalities:
- protein-structure
- protein-sequence
status: extracted
evidence_quality: full-text
tags:
- MSA-free
- distillation
- protein-language-model
- DeBERTa
- AlphaFold2-based
- single-sequence
- end-to-end
- co-evolution
parameters: 1.18e+9  # PLM-1B (1.09B) + EvoFormer (87M) + StructureModule (1.7M); PLM-100M variant also tested
training_tokens: null  # ~260M sequences for PLM pre-training; token count not reported
training_compute: null  # 128× A100 GPUs; total GPU-hours not reported
references_chased: false
added_at: '2026-04-22T21:55:43+00:00'
updated_at: '2026-04-22T21:55:47+00:00'
---

## TL;DR

HelixFold-Single replaces the expensive MSA search in AlphaFold2-style pipelines with a 1B-parameter DeBERTa-based protein language model (PLM) pre-trained on ~260M sequences via masked language modeling. The PLM's per-residue embeddings and attention weights serve as single and pair representations fed into AlphaFold2's EvoFormer + Structure Module. Trained with knowledge distillation from AlphaFold2 (~1M pseudo-structures) plus ~120K experimental structures, it matches MSA-based methods on proteins with large homologous families (MSA depth >1000) and is ~500× faster (1.5 s vs ~800 s for AlphaFold2 at sequence length <200). Performance degrades for orphan proteins with sparse homologous sequences.

## Model

- **Architecture**: Three components wired end-to-end: PLM Base → Adaptor → Geometric Modeling (EvoFormer + Structure Module).
- **PLM Base**: DeBERTa-style disentangled-attention Transformer with Pre-Norm (not Post-Norm). Uses residue-to-residue and residue-to-position attention terms; drops position-to-residue term (negligible gain). Outputs per-residue hidden states (single repr.) and stacked multi-head attention weight matrices across all layers (pair repr.).
- **PLM-1B**: 1.09B params, 20 layers, hidden 2048, intermediate 8192, 16 heads.
- **PLM-100M** (ablation): 100M params, 12 layers, hidden 768, intermediate 3072, 12 heads.
- **Adaptor**: Linear projections mapping PLM outputs to d_Single=512 and d_Pair=64 dimensions expected by the Geometric Modeling module. Pair repr. is formed by concatenating attention weights from all PLM layers then projecting.
- **EvoFormer (modified)**: 87M params, 24 blocks. Column-wise gated self-attention removed (no MSA rows to exchange info between). Retains row-wise gated attention with pair bias, outer product mean, triangle updates, triangle self-attention.
- **Structure Module**: 1.7M params, 8 blocks, hidden 384. Invariant Point Attention (IPA) as in AlphaFold2.
- **Recycling**: Geometric Modeling module is recycled (iterative refinement), following AlphaFold2.
- **Total parameters**: ~1.18B (PLM-1B variant).

## Data

- **PLM pre-training**: UniRef30 (2021-03), ~260M protein sequences clustered at 30% sequence identity. Sequences are re-sampled to balance cluster distribution.
- **Structure training** (3 datasets):
  1. RCSB PDB (released before 2020-05-14): experimental structures filtered to resolution <3 Å and length ≥10 aa, clustered at 40% identity → ~120K structures.
  2. Distillation-Uniclust30: structures inferred by AlphaFold2 on Uniclust30 (2018-08), filtered by average pLDDT ≥ 0.5, clustered at 30% identity.
  3. Distillation-EBI: ~1M structures from AlphaFold Protein Structure Database (v2), filtered by pLDDT ≥ 0.5, clustered at 50% identity.
- **Evaluation**:
  - CASP14: 61 targets / 87 domains (FM, TBM-easy, TBM-hard, FM/TBM).
  - CAMEO: 371 targets (2021-09-04 to 2022-02-19).
  - MSA Depth Test: 793 PDB targets (2020-05 to 2021-10) with wide MSA depth range, combined with CASP14 + CAMEO.

## Training Recipe

- **Stage 1 — PLM pre-training**: Masked language model (15% residue masking), AdamW optimizer (lr=5e-4, β₁=0.9, β₂=0.999, weight decay=0.01), linear warmup over 30K steps. Batch size dynamically adjusted per GPU based on sequence length. 128× NVIDIA A100 GPUs.
- **Stage 2 — End-to-end structure prediction** (PLM + Geometric Modeling jointly optimized):
  - *Initial training*: Adam optimizer, lr=1e-3, sequence crop length=256.
  - *Fine-tuning*: lr=2e-4, crop length=384.
  - Gradient clipping by global norm (clip=1.0).
  - Losses: FAPE (Frame Aligned Point Error) + auxiliary losses following AlphaFold2.
  - Training data: PDB experimental structures + distillation datasets (Uniclust30 + EBI).
- **Hardware**: 128× NVIDIA A100 (40 GB) GPUs. Total GPU-hours not reported.

## Key Ablations & Design Choices (quantitative)

| Design choice | Result |
|---|---|
| PLM-1B vs PLM-100M (perplexity) | PLM-1B has substantially lower perplexity on both CASP14 and CAMEO targets |
| PLM-1B vs PLM-100M (contact prediction P@L/5) | PLM-1B significantly superior on long-range contact prediction on CASP14 and CAMEO |
| HelixFold-Single vs AlphaFold2 (MSA), CASP14 overall | Below AlphaFold2 (MSA) overall; competitive on TBM-easy domains |
| HelixFold-Single vs AlphaFold2 (MSA), CAMEO overall | Comparable to AlphaFold2 (MSA); outperforms RoseTTAFold (MSA) |
| HelixFold-Single vs AlphaFold2 (single seq) | Dramatically outperforms AF2 fed only single sequences on all categories |
| HelixFold-Single vs RoseTTAFold (single seq) | Dramatically outperforms RoseTTAFold fed single sequences on all categories |
| MSA depth >1000 (CAMEO) | HelixFold-Single matches MSA-based methods; 90% of PDB proteins have MSA depth >1024 |
| MSA depth ≤100 | All methods (including MSA-based) have unsatisfactory TM-scores; HelixFold-Single degrades |
| PLM perplexity vs TM-score | Negatively correlated: lower PLM perplexity → higher TM-score (Fig. 3e) |
| PLM perplexity vs MSA depth | Negatively correlated: deeper MSA families → lower PLM perplexity (Fig. 3d) |
| Speed: HelixFold-Single vs AlphaFold2, len <100 | 1.5 s vs 766 s (~500×) |
| Speed: HelixFold-Single vs AlphaFold2, len 100–200 | 1.5 s vs 796 s (~530×) |
| Speed: HelixFold-Single vs AlphaFold2, len >800 | 37.5 s vs 1611 s (~43×) |
| Case study: PlyC (7KWT:B) | HelixFold-Single TM=0.81 vs AlphaFold2 TM=0.24 (AF2 MSA search likely insufficient) |
| Case study: RoxP (7BCJ:A) | HelixFold-Single TM=0.64 vs AlphaFold2 TM=0.29 |

## Reported Insights

- A large-scale PLM can serve as an effective alternative to MSAs for encoding co-evolution information. The attention weights across PLM layers capture residue–residue contact patterns analogous to those extracted from MSA covariance.
- Performance scales with PLM size: 1B params significantly outperforms 100M params on both perplexity and downstream structure prediction. Authors expect further gains from even larger PLMs.
- Accuracy is correlated with the richness of homologous sequences in the training database (MSA depth of the target family), indicating PLM memorises co-evolution patterns proportionally to family representation in UniRef30.
- PLM perplexity on a target sequence is a useful proxy for expected structure prediction quality.
- Distillation from AlphaFold2 (~1M pseudo-structures) is essential to compensate for the small number of experimental structures (~120K).
- HelixFold-Single can outperform AlphaFold2 when MSA search fails (e.g., PlyC, RoxP), because PLM relies on learned correlations rather than retrieved homologs.
- The DeBERTa disentangled-attention mechanism (relative position encoding) is important for modelling residue contacts that depend on relative rather than absolute position.
- Column-wise attention in EvoFormer is unnecessary for single-sequence input and is safely removed.

## References Worth Chasing (≤15 bio-FM refs)

1. **AlphaFold2 (Jumper et al., 2021)** – Foundation architecture for Geometric Modeling module; source of distillation structures [ref 1].
2. **RoseTTAFold (Baek et al., 2021)** – Three-track MSA-based baseline [ref 22].
3. **TAPE / protein transfer learning (Rao et al., 2019)** – Early PLM evaluation benchmark showing PLMs reveal secondary structure [ref 6].
4. **ProtTrans (Elnaggar et al., 2020)** – Large-scale PLM pre-training including ProT5; used in MSA-free structure works [ref 7].
5. **ESM-1b (Rives et al., 2021)** – 650M-param PLM; used by other single-sequence structure methods [ref 31].
6. **MSA Transformer (Rao et al., 2021)** – Axial attention over MSAs; contact prediction via attention weights [ref 25].
7. **RGN2 (Chowdhury et al., 2021)** – AminoBERT + recurrent geometric network for single-sequence structure [ref 10].
8. **Weißenow et al., 2022** – PLM embeddings + ResNet for fast alignment-free structure prediction [ref 11].
9. **Wang et al., 2022** – Supervised transformer PLM + single-sequence structure prediction [ref 12].
10. **DeBERTa (He et al., 2020)** – Disentangled attention mechanism adopted for PLM Base [ref 13].
11. **UniRef30 / Uniclust (Mirdita et al., 2017)** – Clustered protein sequence database for PLM pre-training [ref 14].
12. **AlphaFold Protein Structure Database (Varadi et al., 2021)** – Source of ~1M distillation structures [ref 18].
13. **HelixFold (Wang et al., 2022)** – Efficient PaddlePaddle re-implementation of AlphaFold2; base codebase [ref 32].
14. **Unsupervised structure learners (Rao et al., 2020)** – Showed Transformer attention weights encode protein contacts [ref 8].

## Notes / Open Questions

- Total training compute (GPU-hours) is not reported. 128× A100 is stated but neither wall-clock time for pre-training nor for structure training is given.
- Token count for PLM pre-training is not reported; only ~260M sequences. Assuming average length ~200 aa → ~52B tokens, but this is an estimate.
- The paper tests only two PLM sizes (100M, 1B). The scaling trend is clear but no larger model was trained; ESMFold (Lin et al., 2023) later scaled to 15B.
- Distillation quality ceiling: the model is ultimately bounded by AlphaFold2 accuracy on the distillation targets. No analysis of how distillation noise propagates.
- Performance on orphan proteins (MSA depth <100) remains poor for all methods; the PLM cannot compensate for families absent from UniRef30.
- No comparison with ESMFold (concurrent work, arXiv July 2022) which uses ESM-2 (15B) + similar AF2 geometric module approach.
- Column-wise attention removal is justified but not ablated quantitatively (just stated as unnecessary).
- The relationship between PLM perplexity and structure accuracy is correlational; unclear if perplexity can be used as a reliable filter in production.

## Verification (Rev 3)

Six claims referencing `[helixfold-single-msa-free-2022]` were found in `insights.md`.

| # | insights.md line | Claim (paraphrased) | Verdict | Rationale |
|---|---|---|---|---|
| 1 | 26 | "HelixFold-Single achieves near-AF2 accuracy at 500× speed-up, especially on orphan proteins without deep alignments" | **partial** | Speed-up (500× for len <200) and near-AF2 accuracy on well-represented families are supported (Table 2; §3.2). However "especially on orphan proteins" is **contradicted**: the paper states "for proteins with sparse homologous sequences, the TM-scores of all the compared methods are unsatisfactory" (§3.3) and the notes explicitly flag performance degradation on orphans. The orphan-protein qualifier may apply to OmegaFold but not HelixFold-Single. |
| 2 | 31 | "HelixFold-Single distilled ~1 M AF2 labels to bootstrap PLM-based folding" | **supported** | §2.3: "additional one million estimated protein structures for training … (distilled from AlphaFold2)"; Appendix A Distillation-EBI: "About one million protein structures are extracted from AlphaFold Protein Structure Database." |
| 3 | 126 | "HelixFold-Single uses a DeBERTa-based PLM coupled to AF2's structure module" | **supported** | §2.1 adopts DeBERTa disentangled-attention Transformer (ref [13]); §2.2 uses AlphaFold2's EvoFormer + Structure Module. |
| 4 | 332 | Table row: "1.18 B DeBERTa PLM \| 500× \| Competitive" | **supported** | Table 1: PLM-1B 1.09 B + EvoFormer 87 M + StructureModule 1.7 M ≈ 1.18 B. Table 2: 766 s vs 1.5 s ≈ 511× for len [1,100]. §3.2: "competitive accuracy with MSA-based methods on targets with large homologous families." |
| 5 | 344 | "Distillation from ~1 M AF2 predictions bootstraps a PLM-only folding model, achieving 500× speed-up" | **supported** | Same evidence as claims 2 and 4. Note: 500× is the peak for short sequences; speed-up drops to ~43× for len >800 (Table 2), but the claim does not assert uniformity. |
| 6 | 474 | "1.18 B, 500× faster, PLM perplexity correlates with TM-score" | **supported** | Parameter count and speed as above. §3.3 + Fig. 3e: "Perplexity of the PLM and the TM-scores of HelixFold-Single are also negatively correlated." |

**Summary**: 5/6 supported, 1/6 partial. The only issue is Claim 1's grouping of HelixFold-Single with the statement "especially on orphan proteins," which the paper contradicts for this model.
