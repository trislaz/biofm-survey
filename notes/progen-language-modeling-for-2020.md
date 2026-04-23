---
id: progen-language-modeling-for-2020
title: 'ProGen: Language Modeling for Protein Generation'
authors:
- Ali Madani
- Bryan McCann
- Nikhil Naik
- Nitish Shirish Keskar
- Namrata Anand
- Raphael R. Eguchi
- Po-Ssu Huang
- Richard Socher
year: 2020
venue: null
arxiv: '2004.03497'
doi: null
url: https://arxiv.org/abs/2004.03497v1
pdf_path: papers/progen-language-modeling-for-2020.pdf
md_path: papers/md/progen-language-modeling-for-2020.md
modalities:
- protein-sequence
status: extracted
evidence_quality: medium
tags:
- protein-generation
- conditional-language-model
- autoregressive-transformer
- controllable-generation
- protein-engineering
- zero-shot-fitness
parameters: 1.2B
training_tokens: null
training_compute: 256× TPU-v3 cores, ~2 weeks, 1M iterations
references_chased: false
added_at: '2026-04-22T19:36:59+00:00'
updated_at: '2026-04-22T20:24:30+00:00'
is_fm: true
fm_classification_reason: 'ProGen: pretrained protein generative LM.'
---

## TL;DR

ProGen is a 1.2B-parameter autoregressive Transformer (CTRL-style) trained on ~281M protein sequences from UniParc/UniProtKB/Pfam, conditioned on ~1,100 keyword tags and ~100k taxonomic tags. Achieves PPL 8.56 on full test set. Generated proteins exhibit near-native conformational energies after Rosetta threading/relaxation. Fine-tuning on held-out families (OOD) drops PPL from 13.34→7.45 vs 17.78 from random init. Zero-shot fitness selection on GB1 picks high-fitness variants without any supervised signal.

## Model

- **Architecture**: Transformer decoder (autoregressive, causal masking), adapted from CTRL (Keskar et al., 2019)
- **Parameters**: 1.2B
- **Layers**: 36
- **Model dimension**: d = 1,028; inner FF dimension: f = 512
- **Attention heads**: 8 per layer
- **Max sequence length**: 512 tokens (conditioning tags prepended to amino acid sequence)
- **Vocabulary**: 25 standard IUPAC amino acids + ~1,100 keyword tags (GO terms: cellular component, biological process, molecular function) + ~100k NCBI taxonomic tags
- **Embeddings**: learned token embedding + sinusoidal positional encoding; token embeddings tied with output projection (weight tying)
- **Conditioning**: tag sequence c prepended to amino acid sequence a; model learns p(x) = p([c; a]) factored autoregressively; can recover p(a|c) at generation time
- **Generation**: top-k sampling (k=1 or 3) with amino-acid repetition penalty (window=4 tokens, factor=1.2)

## Data

- **Sources**: UniParc, UniProtKB, SWISS-PROT, TrEMBL, Pfam, NCBI taxonomy
- **Total proteins**: ~281M (most comprehensive non-redundant annotated protein database at the time)
- **Training set**: 280M sequences (each included forward + reverse since proteins are direction-invariant)
- **ID-test**: 1M randomly sampled sequences
- **OOD-test**: 100k sequences from 20 held-out Pfam protein families (PF18369, PF04680, PF17988, PF12325, PF03272, PF03938, PF17724, PF10696, PF11968, PF04153, PF06173, PF12378, PF04420, PF10841, PF06917, PF03492, PF06905, PF15340, PF17055, PF05318)
- **Conditioning tags**: randomly sampled per sequence (biased toward SWISS-PROT verified tags); dropout rate 0.4 on tags; always include one copy without any tags
- **OOD verification**: 3-gram SAE between Train and OOD-test = 0.399 vs Train and ID-test = 0.027, confirming distributional shift

## Training Recipe

- **Framework**: TensorFlow
- **Hardware**: 256 TPU v3 cores (Cloud TPU v3 Pod)
- **Duration**: ~2 weeks, 1M iterations
- **Batch size**: 64 (global)
- **Optimizer**: Adagrad
- **Learning rate**: linear warmup from 0 → 1e-2 over 40k steps
- **Gradient clipping**: norm clipped to 0.25
- **Dropout**: 0.1 after residual connections; 0.4 on conditioning tags
- **Initialization**: pretrained CTRL weights (Keskar et al., 2019) — stabilized and improved early training
- **Sequence handling**: forward + reverse for each protein; truncate/pad to 512; no loss on padding tokens
- **Fine-tuning (OOD)**: OOD-test split into OOD-test-80 (train) / OOD-test-20 (eval); 5 epochs, Adam, linear LR warmup to 1k iterations

## Key Ablations & Design Choices

- **Full test perplexity**: ProGen PPL 8.56, hard acc 45% vs Uniform baseline PPL 25 / 4% and Empirical baseline PPL 18.14 / 6%
- **ID vs OOD generalization**: ID-test PPL 8.17 / 45% hard acc; OOD-test PPL 13.34 / 22% — model generalises to unseen families but with degraded performance
- **Fine-tuning vs random init on OOD**: fine-tuned ProGen on OOD-test-20 achieves PPL 7.45 / 50% hard acc vs random-init same architecture PPL 17.78 / 9% — 2.4× lower PPL and 5.6× higher accuracy from transfer
- **Soft vs hard accuracy**: BLOSUM62-informed soft accuracy >20 percentage points above hard accuracy — errors often correspond to evolutionarily acceptable substitutions
- **No overfitting detected**: train and test soft accuracy curves show no gap at 1M steps, suggesting larger models and more compute would still help (Figure 2)
- **Context length effect**: perplexity decreases and hard accuracy increases for later portions of a protein sequence (Figure 3) — more amino acid context → better prediction
- **Conditioning tag count effect**: performance improves with more tags; proteins with ≥8 tags yield secondary structure accuracy surpassing the 25% random-mutation baseline (Figure 7); with [0,2] tags ~0.73 secondary structure accuracy vs [8,20] tags ~0.84
- **Top-k sampling + repetition penalty**: k=1 with repetition penalty 1.2 (window=4) outperforms k=3 and no-penalty variants for sequence similarity across all context lengths (Figure 5)
- **Primary vs secondary metrics discrepancy**: sequence similarity only approaches 25% mutation baseline, but secondary structure accuracy surpasses it — model learns mutation invariances that conserve structure
- **Conformational energy (Rosetta)**: generated proteins exhibit energy levels near or below native relaxed templates, far better than 50%/100% mutation and all-alanine baselines (Figure 8)
- **VEGFR2 completion**: mean sequence identity 73.1% vs native (lower than 25% mutation baseline's 74%) but with better Rosetta energies — meaningful deviation while preserving low energy (Figure 9)
- **GB1 zero-shot fitness**: top-100 variants by lowest ProGen perplexity have statistically high fitness vs random selection which produces low/zero fitness — model has learned distribution of functionally relevant proteins without any supervised fitness signal (Figure 11)
- **Generation from tags only**: ProGen can generate full proteins from conditioning tags alone (no amino acid context); FMN/Flavoprotein-conditioned generation yields sequences with strong HHblits alignments (E-value < 1e-4, identity > 40%) to known FMN proteins

## Reported Insights

- Protein generation can be framed as conditional language modeling; conditioning tags (taxonomy + GO terms) provide fine-grained control over generated properties
- Errors at primary sequence level often correspond to biologically acceptable substitutions (BLOSUM62), suggesting the model learns structural/functional invariances rather than memorising exact sequences
- Transfer learning from a large text-domain model (CTRL) to proteins is effective — warm-starting from CTRL stabilises training and enables strong OOD fine-tuning
- The gap between sequence-level and structure-level metrics suggests evaluation of protein generators should prioritise higher-level structural and functional metrics over raw sequence identity
- ProGen can serve multiple protein engineering workflows: initial sequence proposals for directed evolution, hotspot completion, de novo design with conditioning tags, and zero-shot fitness screening

## References Worth Chasing

- CTRL: A Conditional Transformer Language Model for Controllable Generation (arXiv:1909.05858) — direct architectural ancestor; conditioning tag approach adapted from here
- Unified rational protein engineering with sequence-based deep representation learning — Alley et al. 2019, UniRep (doi:10.1038/s41592-019-0598-1) — key prior on protein representation learning with mLSTM
- Biological structure and function emerge from scaling unsupervised learning to 250 million protein sequences — Rives et al. 2019 (bioRxiv:622803) — ESM; contemporaneous large-scale protein LM for representation
- Evaluating protein transfer learning with TAPE — Rao et al. 2019 (NeurIPS) — benchmark for protein embeddings used to contextualise ProGen
- Generative models for graph-based protein design — Ingraham et al. 2019 (NeurIPS) — structure-conditioned protein generation with graph transformers
- Accelerating protein design using autoregressive generative models — Riesselman et al. 2019 (bioRxiv:757252) — autoregressive sequence-only generative modeling via causal dilated convolutions
- How to hallucinate functional proteins — Costello & Martin 2019 (arXiv:1903.00458) — VAE-based protein sequence generation
- Generative modeling for protein structures — Anand & Huang 2018 (NeurIPS) — GAN for 2D distance map generation / structure in-painting
- Design of metalloproteins and novel protein folds using variational autoencoders — Greener et al. 2018 (Scientific Reports) — VAE for structure-based protein design
- Language models are unsupervised multitask learners — Radford et al. 2019, GPT-2 (OpenAI Blog) — foundational text LM architecture ProGen is compared against
- Attention is all you need — Vaswani et al. 2017 (NeurIPS) — Transformer architecture basis
- Machine learning-assisted directed protein evolution with combinatorial libraries — Wu et al. 2019 (PNAS) — ML for directed evolution, complementary to ProGen's generative approach
- Adaptation in protein fitness landscapes is facilitated by indirect paths — Wu et al. 2016 (eLife) — GB1 fitness landscape dataset used in case study

## Notes / Open Questions

- No wet-lab experimental validation of generated proteins; all evaluations are computational (sequence similarity, PSIPRED secondary structure, Rosetta energy)
- Training tokens not explicitly reported; ~280M sequences × 2 (fwd+rev), truncated to 512 — upper bound ~286B tokens but actual count depends on average sequence length + tag length
- Inner FF dimension (512) is smaller than model dimension (1028) — unusual for Transformers where typically f > d; may be a deliberate compression choice or reporting oddity
- Repetition penalty is a heuristic (window=4, factor=1.2) rather than learned — unclear how sensitive generation quality is to these hyperparameters
- GB1 zero-shot evaluation is on single-position mutants at 4 epistatic sites — not tested on multi-position combinatorial variants
- No comparison to MSA-based generative methods (e.g., profile HMMs) which are the traditional baseline for protein family modeling
- Subsequent work (ProGen2, 2023) scaled to 6.4B parameters and included experimental validation of generated lysozymes — worth chasing for updated results

## Ablations (Rev 4)

| # | Ablation axis | Variants compared | Metric | Result | Take-away |
|---|---|---|---|---|---|
| 1 | Train-distribution generalisation | ID-test vs OOD-test (held-out protein families) | Perplexity / hard-acc | 8.17 / 45 → 13.34 / 22 | Performance degrades on unseen families but stays well above empirical baseline (18.14) |
| 2 | Warm-start from pre-trained ProGen | OOD-test-20: random init vs fine-tuned from ProGen (5 epochs) | Perplexity / hard-acc | 17.78 / 9 → 7.45 / 50 | Pre-training is essential — fine-tuning more than halves PPL and 5× hard-acc on novel families |
| 3 | Amino-acid context length | Sequence proportion as context (0.5 → 0.9), Fig 3/5 | Perplexity, seq-similarity | PPL drops monotonically (~4.0 → 2.4) | More residue context narrows the next-token distribution; benefit holds across all sampling settings |
| 4 | # conditioning tags | [0,2] vs [3,7] vs [8,20] tags, Figs 4/6/7 | PPL, seq-sim, 2° structure acc | ≥3 tags exceed 50% mutation baseline; ≥8 tags approach 25% baseline and surpass it on 2° structure (≈0.84 vs 0.78) | Conditioning tags carry real predictive signal; rich tag sets are needed for controllable, structurally-faithful generation |
| 5 | Sampling strategy | top-k ∈ {1,3} × repetition-penalty ∈ {0, 1.2}, Fig 5 | Sequence similarity vs context | Greedy (k=1) + rep-penalty 1.2 wins at every context length | Near-greedy decoding with a 4-token repetition penalty is the right default for protein generation |
| 6 | Generation w/o initial AA context (tag-only) | Sample from conditioning tags alone, App. A.2 / Fig 13 | MSA alignment to FMN family | Multiple generated sequences align well to the target family from tags only | Conditioning tags alone can steer de novo generation without any seed residues |

**Count: 6 ablations.**

**Top take-away:** Conditioning tags are the dominant lever — given ≥8 tags, ProGen's generations cross the 25% mutation baseline on secondary-structure accuracy even though sequence-similarity errors persist, confirming that the tags steer generation toward functionally meaningful (BLOSUM-acceptable) substitutions rather than exact sequence reproduction.
