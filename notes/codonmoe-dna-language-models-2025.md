---
id: codonmoe-dna-language-models-2025
title: 'CodonMoE: DNA Language Models for mRNA Analyses'
authors:
- Shiyi Du
- Litian Liang
- Jiayi Li
- Carl Kingsford
year: 2025
venue: null
arxiv: '2508.04739'
doi: null
url: https://arxiv.org/abs/2508.04739v1
pdf_path: papers/codonmoe-dna-language-models-2025.pdf
md_path: papers/md/codonmoe-dna-language-models-2025.md
modalities:
- dna
- rna
status: extracted
evidence_quality: moderate
tags: [mixture-of-experts, adapter, codon-level, cross-modality, parameter-efficient, SSM, DNA-to-RNA]
parameters: "7.5M (HyenaDNA+CodonMoE-pro); adapter adds 3.4–76.2M on top of backbone"
training_tokens: null
training_compute: "single NVIDIA A100 GPU"
references_chased: false
added_at: '2026-04-22T19:36:46+00:00'
updated_at: '2026-04-22T20:19:06+00:00'
---

## TL;DR

CodonMoE is a lightweight plug-and-play MoE adapter that converts pretrained DNA language models (HyenaDNA, Caduceus, GPN-MSA) into effective mRNA analyzers by restructuring hidden states into codon-level (triplet) representations and routing through specialized experts. HyenaDNA+CodonMoE-pro achieves SOTA on 3/4 RNA tasks with only 7.5M params—80% fewer than specialized RNA models like CodonBERT (81.7M). No RNA-specific pretraining needed; only fine-tuning the adapter. Proven universal approximator at codon level (Theorem 3.1).

## Model

- **Architecture**: CodonMoE is an adapter module inserted after a frozen/pretrained DNA backbone. It reshapes backbone hidden states H ∈ R^{B×S×d} into codon groups [B, S/3, 3d], applies a dense Mixture-of-Experts (K=4 experts by default), each expert: Linear(3d,3d)→GELU→Linear(3d,d). Gating: softmax over Linear(3d, K). Expert outputs are weighted-summed, repeated 3× to match original seq length, added as residual. Followed by LayerNorm→GELU→Dropout(0.1)→Flatten→Linear→LayerNorm→GELU→Dropout→Linear(d,1) for regression.
- **CodonMoE-pro variant**: replaces final layers with codon neighborhood convolution (sliding window over adjacent codons) to detect codon n-gram motifs. Fewer params than standard CodonMoE, better performance.
- **Backbones tested**: HyenaDNA (4.1M, O(LlogL)), Caduceus (7.7M, O(L)), GPN-SS (65.6M, O(L)), GPN-MSA (85.7M, O(L²)).
- **Best config**: HyenaDNA+CodonMoE-pro = 7.5M total params, O(LlogL) complexity.
- **Theoretical result**: CodonMoE is a universal approximator at codon level—can approximate any continuous f: C^n → R with arbitrary precision given sufficient expert capacity (Theorem 3.1, proof via UAT applied to each expert network).

## Data

- **mRFP expression** (Nieuwkoop et al. 2023): 1,459 mRFP codon-randomized variants with expression levels in E. coli. 675 bp CDS per variant.
- **SARS-CoV-2 vaccine degradation** (Leppek et al. 2022): 2,400 mRNA constructs with in-cell stability measurements in HEK293T cells.
- **Tc-riboswitch** (Groher et al. 2018): 355 tetracycline riboswitch dimer sequences with switching factor measurements in S. cerevisiae.
- **MLOS** (Li et al. 2024): 164 mRNA candidates encoding influenza hemagglutinin antigen, protein expression in HeLa cells.
- **Splits**: 70%/15%/15% train/val/test, same splits as CodonBERT for fair comparison.
- **No pretraining data**: CodonMoE uses existing DNA backbone pretrained weights; adapter is only fine-tuned on task-specific RNA data.

## Training Recipe

- Backbone weights are frozen (pretrained on DNA, e.g., human reference genome).
- Only CodonMoE adapter is trained on downstream RNA tasks.
- LR: 0.0005 (Caduceus configs), 0.0001–0.001 (HyenaDNA configs). Epochs: 100.
- Hardware: single NVIDIA A100 GPU.
- Metric: Spearman's rank correlation (ρ).
- Dropout rate: 0.1. Activation: GELU. Normalization: LayerNorm.

## Key Ablations & Design Choices

**CodonMoE vs. no adapter (Table 1, Table 2)**:
- HyenaDNA alone: Vaccine 0.69, mRFP 0.44. With CodonMoE: 0.81, 0.84 (+0.12, +0.40). With CodonMoE-pro: **0.84, 0.88** (SOTA).
- GPN-MSA alone: Vaccine 0.55, mRFP 0.33. With CodonMoE: 0.77, 0.79 (+0.22, +0.46). With CodonMoE-pro: 0.82, 0.81.
- Caduceus alone: Vaccine 0.56, mRFP 0.49. With CodonMoE: 0.80, 0.80 (+0.24, +0.31).
- GPN-SS alone: Vaccine 0.60, mRFP 0.56. With CodonMoE: 0.74, 0.82 (+0.14, +0.26).
- Worst-performing backbones show largest gains → CodonMoE bridges DNA-RNA gap.

**Codon operator variants (Table 5)**:
- CodonMean (simple avg): HyenaDNA mRFP 0.765, Vaccine 0.789.
- CodonMoE (expert routing): HyenaDNA mRFP 0.837, Vaccine 0.812.
- CodonMoE-pro (+ conv): HyenaDNA mRFP **0.878**, Vaccine **0.844**.
- Progressive gains from mean→MoE→MoE-pro confirm value of expert routing + local convolution.

**Dense baseline vs. CodonMoE-pro (Table 8, matched params)**:
- HyenaDNA-Dense baseline: Vaccine 0.80, mRFP 0.82.
- HyenaDNA+CodonMoE-pro: Vaccine 0.84, mRFP 0.88.
- Gains come from architecture (expert routing), not just param count.

**Raw DNA embeddings + regressors (Table 6)**:
- Frozen GPN-MSA + MLP: mRFP 0.33, Vaccine 0.57.
- Frozen GPN-MSA + XGBoost: mRFP 0.48, Vaccine 0.75.
- Frozen HyenaDNA + XGBoost: mRFP 0.51, Vaccine 0.71.
- DNA embeddings alone are insufficient for mRNA tasks → need codon-aware adaptation.

**Full benchmark vs. RNA FMs (Table 4)**:
- HyenaDNA+CodonMoE-pro (7.5M): Vaccine **0.84**, mRFP **0.88**, Tc-ribo 0.60, MLOS **0.63**. SOTA on 3/4 tasks.
- CodonBERT (81.7M): Vaccine 0.77, mRFP 0.85, Tc-ribo 0.56, MLOS 0.54.
- Transformer HELM (50M): Vaccine 0.79, mRFP 0.85, Tc-ribo 0.62 (best), MLOS 0.59.
- RNA-FM (100M): Vaccine 0.74, mRFP 0.80, Tc-ribo **0.58**, MLOS —.
- CodonMoE-pro uses 9% of CodonBERT's parameters.

**"Threshold effect"**: 7–12M params appears optimal; additional capacity provides diminishing returns.

**Tc-riboswitch limitation**: CodonMoE achieves 0.60 (2nd best) but does not beat Transformer HELM (0.62). Riboswitches depend on global folding dynamics, not codon usage—outside CodonMoE's inductive bias.

## Reported Insights

- DNA and mRNA share enough biological signal that DNA-pretrained representations can be repurposed for RNA tasks with a lightweight codon-aware adapter.
- Expert routing is more important than raw parameter count for codon-level tasks (structure > scale).
- Stability tasks (vaccine degradation) benefit from global/mid-range patterns; expression tasks (mRFP) require fine-grained local n-gram detection. CodonMoE-pro's convolution addresses both.
- GPN-MSA shows largest average gain (+0.34 avg Δρ), possibly because its attention-based "smoothing effect" on rare codons is corrected by dedicated expert pathways.
- Sub-quadratic DNA backbones (HyenaDNA O(LlogL), Caduceus O(L)) can replace quadratic RNA Transformers with superior results.

## References Worth Chasing

1. **HyenaDNA** (Nguyen et al. 2024b) — SSM backbone, single-nucleotide resolution up to 1M tokens.
2. **Caduceus** (Schiff et al. 2024) — Mamba-based bidirectional RC-equivariant DNA LM.
3. **EVO** (Nguyen et al. 2024a) — 7B param Hyena+Transformer hybrid, DNA/RNA/protein, 131kb context.
4. **HELM** (Yazdani-Jahromi et al. 2025) — Hierarchical codon-aware mRNA LM, main competitor on Tc-riboswitch.
5. **CodonBERT** (Li et al. 2024) — BERT-based codon-level RNA LM, 81.7M params, 10M mRNA CDS pretraining.
6. **GPN-MSA** (Benegas et al. 2023) — DNA LM using 100-species MSA, RoFormer, variant effect prediction.
7. **RNA-FM** (Chen et al. 2022) — 100M param RNA foundation model, 23M ncRNA sequences.
8. **SpliceBERT** (Chen et al. 2023) — RNA splicing-focused pretrained model.
9. **Nucleotide Transformer** (Dalla-Torre et al. 2023) — Large-scale DNA FM.
10. **PlantCaduceus** (Zhai et al. 2024) — Cross-species extension of Caduceus to plant genomes.
11. **BigRNA** (Celaj et al. 2023) — RNA foundation model for disease mechanisms.
12. **DNABERT** (Ji et al. 2021) — k-mer tokenized DNA BERT.
13. **Enformer** (Avsec et al. 2021) — Convolution+Transformer for gene expression from sequence.

## Notes / Open Questions

- CodonMoE is an adapter, not a foundation model per se—its value is in cross-modality transfer (DNA→RNA) without retraining the backbone. Interesting question: does it work on non-SSM backbones at scale (e.g., Nucleotide Transformer, EVO)?
- Datasets are very small (164–2,400 samples). Performance on larger-scale RNA benchmarks unknown.
- Only regression tasks tested (Spearman ρ). No classification, generation, or structure prediction tasks.
- T→U substitution is handled trivially (U replaced with T at input). Codon structure is the main biological inductive bias.
- Universal approximation theorem (Theorem 3.1) is a standard MoE+UAT composition—useful but not surprising; practical value is in the empirical gains.
- No cross-species or cross-organism evaluation (mRFP in E. coli, vaccine in human cells, riboswitch in yeast, MLOS in HeLa).
- Code available: https://github.com/Kingsford-Group/CodonMoE.
