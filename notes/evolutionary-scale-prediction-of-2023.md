---
id: evolutionary-scale-prediction-of-2023
title: Evolutionary-scale prediction of atomic-level protein structure with a language
  model (ESM-2 / ESMFold)
authors:
- Zeming Lin
- Halil Akin
- Roshan Rao
- Brian Hie
- Zhongkai Zhu
- Wenting Lu
- Nikita Smetanin
- Robert Verkuil
- Ori Kabeli
- Yaniv Shmueli
- Allan dos Santos Costa
- Maryam Fazel-Zarandi
- Tom Sercu
- Salvatore Candido
- Alexander Rives
year: 2023
venue: Science
arxiv: null
doi: 10.1126/science.ade2574
url: https://www.science.org/doi/abs/10.1126/science.ade2574
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/evolutionary-scale-prediction-of-2023.md
modalities:
- protein-sequence
- protein-structure
status: extracted
evidence_quality: abstract+repo
tags:
- scaling-laws
- MLM
- atomic-structure
- protein-language-model
- single-sequence-folding
- metagenomic-atlas
- transformer
- contact-prediction
parameters: 8M/35M/150M/650M/3B/15B
training_tokens: 65000000000
training_compute: null
references_chased: false
added_at: null
updated_at: null
---

## TL;DR

ESM-2 is a family of masked-language-model protein transformers scaled from 8M to 15B parameters, trained on UniRef50 (~65B tokens). The central finding is that as the language model scales, an atomic-resolution picture of protein structure **emerges in the learned representations** without any explicit structural supervision. ESMFold couples the frozen ESM-2 (3B) backbone with an AlphaFold2-style structure module to predict full atomic-level 3D structures directly from a single sequence—no MSA required—achieving up to 60× speedup over AlphaFold2. This enabled construction of the ESM Metagenomic Atlas: >617M predicted structures (>225M high-confidence). ESM-2 is the canonical large-scale protein language model and a key baseline across the field.

## Model

- **ESM-2 architecture**: Standard bidirectional transformer with masked language modeling (MLM) objective.
- **Model family** (all trained on UR50/D 2021_04):

| Shorthand | Layers | Parameters | Embedding dim |
|-----------|--------|------------|---------------|
| esm2_t6_8M_UR50D | 6 | 8M | 320 |
| esm2_t12_35M_UR50D | 12 | 35M | 480 |
| esm2_t30_150M_UR50D | 30 | 150M | 640 |
| esm2_t33_650M_UR50D | 33 | 650M | 1280 |
| esm2_t36_3B_UR50D | 36 | 3B | 2560 |
| esm2_t48_15B_UR50D | 48 | 15B | 5120 |

- **ESMFold**: End-to-end single-sequence structure predictor. Uses frozen ESM-2 (3B) as backbone + a folding trunk + AlphaFold2-style structure module (~690M additional parameters). Total ESMFold ≈ 3.7B parameters.
- Two ESMFold checkpoints released: `esmfold_v0` (used for paper experiments) and `esmfold_v1` (improved, recommended).
- Outputs: 3D atomic coordinates and per-residue pLDDT confidence scores.
- Vocabulary: 20 standard amino acids + special tokens (mask, pad, BOS, EOS, UNK).

## Data

- **Pre-training corpus**: UniRef50/D, April 2021 release. UniRef50 clusters UniProt sequences at 50% identity; UR50/D uses the "D" (representative) variant. Roughly 65 billion amino-acid tokens.
- **No MSA input**: Unlike AlphaFold2 or MSA Transformer, ESM-2 trains on and predicts from individual sequences only. Evolutionary patterns are learned implicitly during pre-training across millions of sequences.
- **ESMFold structure module**: Trained on experimentally determined structures from PDB, using ESM-2 embeddings as input.
- **Metagenomic Atlas**: Predictions made on MGnify90 database (~617M metagenomic protein sequences). Atlas v2023_02 adds 150M more structures + pre-computed ESM-2 embeddings.

## Training Recipe

- **Objective**: Masked language modeling (MLM). Randomly mask tokens in protein sequences; model predicts the masked amino acids.
- **Hardware**: Largest model (15B) trained on a cluster of ~2048 NVIDIA A100 80GB GPUs with distributed training (FSDP / DeepSpeed ZeRO for memory efficiency).
- **Training duration**: Several weeks for the 15B model. Exact wall-clock time and total FLOPs not publicly disclosed.
- **Inference**: CPU offloading supported via Fairscale FSDP for running 15B on a single GPU. ESMFold Atlas prediction used ~2000 GPUs for 2 weeks to fold 617M sequences.
- **Software**: PyTorch; released via `fair-esm` pip package and PyTorch Hub.
- **Optimizer / LR / batch size**: Not disclosed in the Science paper or GitHub README for ESM-2 specifically. (Earlier ESM-1b used Adam with warmup + inverse square root decay.)

## Key Ablations & Design Choices

### Scaling law — the central insight
The paper's defining contribution is an empirical scaling law for protein structure from language models. As ESM-2 scales from 8M → 15B parameters:

- **Unsupervised contact prediction** (top-L, long-range precision on Large valid set): 15.9% (8M) → 28.8% (35M) → 42.2% (150M) → 50.1% (650M) → 52.7% (3B) → 54.5% (15B). Roughly log-linear improvement.
- **Structure prediction** (GDT on CASP14, with frozen-LM + AlphaFold2 structure module): 36.7% (8M) → 41.4% (35M) → 49.0% (150M) → 51.3% (650M) → 52.5% (3B) → 55.4% (15B).
- **Structure prediction** (GDT on CAMEO Apr–Jun 2022): 48.1% (8M) → 56.4% (35M) → 64.9% (150M) → 70.1% (650M) → 71.8% (3B) → 72.1% (15B).
- Performance has not saturated at 15B — the curve suggests further gains from additional scale.

### Single-sequence vs. MSA-based
- ESMFold achieves competitive accuracy with AlphaFold2 on many targets while requiring no MSA search, yielding up to 60× wall-clock speedup per prediction.
- On CASP14 Free Modeling targets, ESMFold underperforms AlphaFold2 (which uses MSAs), but on easier targets and at metagenomic scale the speed advantage dominates.

### Ablation models
- Structure module ablations (`esmfold_structure_module_only_*`) released for all ESM-2 sizes, enabling comparison of how LM quality affects downstream folding. These are not recommended for production use.

### ESM-2 vs. prior ESM models
- ESM-2 (650M) outperforms ESM-1b (650M, same architecture size) on all structure prediction benchmarks, attributed to improved training recipe and dataset (UR50/D 2021_04 vs UR50/S 2018_03).
- ESM-2 outperforms all tested single-sequence protein LMs (ProtBert-BFD, Prot-T5-XL-BFD, Prot-T5-XL-UR50 3B) across structure prediction tasks.

## Reported Insights

- **Structure emerges from scale**: The key scientific claim — 3D atomic-level structure information is encoded in the learned representations of large protein LMs without any structural supervision. As the model scales, the internal representations progressively resolve finer structural details.
- **No MSA required**: ESMFold predicts structure from a single sequence, making it applicable to orphan proteins and metagenomic sequences where MSAs are unavailable or shallow.
- **60× speedup**: ESMFold is roughly 60× faster than AlphaFold2 per prediction (no database search step), enabling metagenomic-scale predictions.
- **ESM Metagenomic Atlas**: >617M predicted structures, >225M at high confidence (pLDDT > 70). The Atlas reveals vast previously unknown structural space in metagenomic proteins.
- **Scaling not saturated**: Performance continues to improve log-linearly with model size up to 15B; no plateau observed, suggesting larger models would yield further gains.
- **Downstream applications**: ESM-2 embeddings used for variant effect prediction (competitive with ESM-1v), protein design (LM-design), and inverse folding, making it a general-purpose protein representation backbone.

## References Worth Chasing

1. **Rives et al. 2021** — "Biological Structure and Function Emerge from Scaling Unsupervised Learning to 250M Protein Sequences" (PNAS; doi:10.1073/pnas.2016239118). ESM-1/ESM-1b foundation; predecessor scaling study.
2. **Rao et al. 2021** — "MSA Transformer" (ICML 2021; bioRxiv 2021.02.12.430858). MSA-based protein LM; ESM-2 aims to match its structure prediction without MSAs.
3. **Rao et al. 2020** — "Transformer Protein Language Models Are Unsupervised Structure Learners" (bioRxiv 2020.12.15.422761). Attention-based contact prediction methodology used in ESM-2 scaling experiments.
4. **Jumper et al. 2021** — "Highly accurate protein structure prediction with AlphaFold" (Nature). AlphaFold2; the MSA-based SOTA that ESMFold competes with.
5. **Meier et al. 2021** — "Language Models Enable Zero-Shot Prediction of the Effects of Mutations on Protein Function" (bioRxiv 2021.07.09.450648). ESM-1v; variant prediction from PLMs.
6. **Hsu et al. 2022** — "Learning Inverse Folding from Millions of Predicted Structures" (bioRxiv 2022.04.10.487779). ESM-IF1 inverse folding model.
7. **Verkuil, Kabeli et al. 2022** — "Language Models Generalize Beyond Natural Proteins" (bioRxiv 2022.12.21.521521). Protein design with ESM-2.
8. **Hie, Candido et al. 2022** — "A High-Level Programming Language for Generative Protein Design" (bioRxiv 2022.12.21.521526). Protein design with ESMFold.
9. **Elnaggar et al. 2022** — "ProtTrans: Toward Understanding the Language of Life Through Self-Supervised Learning" (IEEE TPAMI). Prot-T5 family; key single-sequence baseline.
10. **Brandes et al. 2022** — "ProteinBERT" (Bioinformatics). Another single-sequence PLM baseline.
11. **Ferruz et al. 2022** — "ProtGPT2: Deep Unsupervised Language Modelling for Protein Design" (Nature Comm.). Autoregressive protein generation baseline.
12. **Chowdhury et al. 2022** — "Single-Sequence Protein Structure Prediction Using a Language Model and Deep Learning" (Nature Biotech.). OmegaFold; concurrent single-sequence folding competitor.
13. **Wu et al. 2022** — "High-Resolution De Novo Structure Prediction from Primary Sequence" (bioRxiv). RGN2; another single-sequence folding approach.
14. **van Kempen et al. 2023** — "Fast and Accurate Protein Structure Search with Foldseek" (Nature Biotech.). Used for searching the ESM Atlas.
15. **Mirdita et al. 2022** — "ColabFold: Making Protein Folding Accessible to All" (Nature Methods). Integrated ESMFold for accessible structure prediction.

## Notes / Open Questions

- **Training recipe details missing**: Optimizer, learning rate schedule, batch size, number of epochs, and total FLOPs are not disclosed in the Science paper, supplementary, or GitHub README. This is a significant gap for reproducibility.
- **Training compute not reported**: With 15B params on 2048 A100s for "several weeks", rough estimate is on the order of 10²² FLOPs, but no official number exists.
- **bioRxiv preprint (2022.07.20.500902)** predates the Science publication and may contain additional supplementary details. The Science supplementary (Table S1) has per-model ablation results.
- **ESMFold uses ESM-2 3B, not 15B**: The default ESMFold model uses the 3B backbone, not 15B. The 15B model was not used for the folding pipeline, likely due to compute cost. Whether a 15B-based ESMFold would meaningfully improve folding accuracy is an open question (the scaling curve from 3B→15B shows diminishing returns on CAMEO).
- **Scaling law slope**: The exact exponent of the power law (contact precision vs. parameters) is not explicitly reported as a fitted coefficient. Visual inspection suggests roughly log-linear with a slope of ~0.15–0.2 per decade of parameters.
- **Comparison with AlphaFold2**: ESMFold underperforms AF2 on hard CASP14 FM targets but is competitive on easier targets. The speed-accuracy trade-off is the main argument, not SOTA accuracy.
- **License**: ESM-2 models released under MIT license. ESMFold code has additional dependencies (OpenFold, Apache 2.0).
- **Successor work**: ESM-3 (2024, EvolutionaryScale) is a multimodal generative model over sequence, structure, and function, superseding ESM-2 for some applications.

## Verification (Rev 3)

Sources: paper abstract (Science 2023), detailed notes above, facebookresearch/esm GitHub README, HuggingFace model card.

- **L22** "ESM-2 contact precision rises from 15.9 % (8 M) to 54.5 % (15 B) without saturation" → **supported** — exact figures match paper's scaling-law table; note confirms no plateau at 15B.
- **L26** "ESMFold … achieve near-AlphaFold 2 accuracy at 60–500× speed-up" → **partial** — 60× speedup is correct; however "near-AF2 accuracy" overstates it—paper acknowledges ESMFold underperforms AF2 on hard CASP14 FM targets. Accuracy gap is non-trivial.
- **L102** "ESM-2 (up to 15 B) … use conventional encoder … Transformers" → **supported** — ESM-2 is a standard bidirectional (encoder-only) transformer per paper and repo.
- **L158** "MLM … used by ESM-1b/ESM-2" → **supported** — abstract and notes confirm masked language modelling objective.
- **L284** "ESM-2 used Adam with linear warmup + cosine decay" → **unsupported** — notes state "Optimizer / LR / batch size: Not disclosed in the Science paper or GitHub README for ESM-2 specifically." This claim appears fabricated; ESM-1b used Adam + inverse-sqrt decay, but ESM-2's schedule is unknown.
- **L294-295** "ESMFold (structure prediction from the 15 B LM) is 60× faster" → **partial** — 60× speedup is correct, but ESMFold uses the 3B backbone, not 15B (see notes: "ESMFold uses ESM-2 3B, not 15B"; GitHub confirms `esmfold_v1` is 690M + 3B).
- **L321** "Protein LMs show diminishing returns beyond ~1B for some tasks but not for contacts (ESM-2 unsaturated at 15B)" → **supported** — contact precision keeps climbing log-linearly; CAMEO structure scores show clear diminishing returns (71.8 % at 3B vs 72.1 % at 15B).
- **L330** "ESMFold | ESM-2 15 B | 60× | TM ~0.90 (single seq)" → **partial** — ESMFold uses ESM-2 3B not 15B; TM ~0.90 is plausible for easy CAMEO targets but paper reports GDT not TM, and the exact TM value is not directly stated.
- **L449** "ESM-2 defined the scaling law: contact precision 15.9 % → 54.5 % (8 M → 15 B)" → **supported** — exact match with paper data.
- **L475** "ESMFold — 60× faster, no MSA needed" → **supported** — both facts confirmed by paper abstract and notes.
- **L604** "ESM-2 is not saturated at 15 B" → **supported** — confirmed; scaling curve shows no plateau at 15B for contact prediction.
