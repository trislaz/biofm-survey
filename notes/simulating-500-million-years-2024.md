---
id: simulating-500-million-years-2024
title: Simulating 500 million years of evolution with a language model (ESM-3)
authors: []
year: 2024
venue: null
arxiv: null
doi: 10.1101/2024.07.01.600583
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/simulating-500-million-years-2024.md
modalities:
- protein-sequence
status: abstract-only
evidence_quality: abstract+metadata
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: Added in rev4 missing-FM brainstorm; canonical bio-FM.
---

## Ablations (Rev 4)

Sources: Hayes et al. bioRxiv 2024.07.01.600583 (paper main + appendices, ESM3 release blog), ESM Cambrian blog (Dec 2024), evolutionaryscale/esm GitHub README.

| # | Ablation axis | Variants compared | Metric / setup | Finding | Take-away |
|---|---------------|-------------------|----------------|---------|-----------|
| 1 | Parameter scale (ESM3) | 1.4B vs 7B vs 98B (same multimodal MLM objective; 98B uses 1.07e24 FLOPs, 2.78B proteins, 771B unique tokens) | Validation loss per track + atomic-coordination prompt success rate | Loss decreases monotonically with scale on every track; harder atomic-coordination prompts only become solvable at 7B/98B — capability is emergent, not just smoother | Multimodal protein generation shows the same scaling-law behavior as LLMs; frontier capabilities require ≥7B |
| 2 | Alignment / preference tuning | Base 1.4B/7B/98B vs DPO-aligned counterparts | Atomic-coordination success on held-out prompts | Alignment gains widen with scale — 98B benefits substantially more than 1.4B from preference tuning | RLHF-style alignment is scale-dependent; small models cannot fully exploit it |
| 3 | Structure tokenizer (VQ vocab for 3D structure) | Learned VQ-VAE discrete structure tokens vs continuous coords / no structure track | Structure reconstruction RMSD/LDDT and downstream generative quality | Discrete VQ tokens reach near-lossless backbone reconstruction and let structure be modeled with the same MLM head as sequence | Discretizing structure into a fixed alphabet is what unlocks unified multimodal MLM training |
| 4 | Multimodal masking schedule | Independent per-track random masking + variable mask rate vs fixed mask rate / single-track training | Cross-track prediction (e.g., predict structure from sequence, function from structure) and joint generation quality | Variable, per-track independent masking is required for the model to handle arbitrary partial prompts at inference; single-track or fixed-rate training degrades cross-modal conditioning | Random per-track masking is what enables prompt-anything → generate-anything behavior |
| 5 | Synthetic data augmentation | Experimental sequence/structure/function only vs + hundreds of millions of predicted structures and function annotations | Held-out structure/function prediction and generative coverage | Synthetic structure + function labels are essential to overcome the scarcity of experimental annotations; removing them hurts especially the structure and function tracks | Synthetic-label augmentation is a first-class ingredient, not optional |
| 6 | Function track tokenization | Keyword/InterPro function tokens included vs sequence+structure only | Function-conditioned generation (e.g., PETase active-site scaffold, α/β hydrolase prompt) | Adding the function-keyword track enables controllable functional generation that pure sequence/structure models cannot do | A discrete function vocabulary is what makes the model "programmable" by biologists |
| 7 | ESM C scale (representation-only sibling) | 300M vs 600M vs 6B (all 1.5M steps, 4.2M-token batches, 6.2T tokens, two-stage 512→2048 context) | CASP15 contact precision P@L | 300M ≈ ESM2-650M; 600M ≈ ESM2-3B and approaches 15B; 6B exceeds all ESM2 — non-diminishing returns through 6B | Compute-and-data-scaling alone (no structure/function tracks) still moves the frontier; scaling is not saturated |
| 8 | ESM C training-stage curriculum | Single-stage 2048 ctx vs two-stage (1M steps @ ctx 512 with 64% metagenomic, then 500k steps @ ctx 2048 with 37.5% metagenomic) | Training efficiency + final P@L | The short-context + metagenomic-heavy warmup is used to reach 6.2T tokens efficiently before the expensive long-context stage | Curriculum on context length and data mix is a deliberate compute lever, not a detail |

**Count:** 8 ablations.

**Top take-away:** ESM3's headline result — controllable, multimodal protein generation with emergent atomic-level capabilities at 98B — is not driven by scale alone but by the combination of (a) discretizing structure and function into token vocabularies so a single MLM objective covers all three tracks, (b) independent per-track variable-rate masking that teaches arbitrary prompt → arbitrary completion, and (c) massive synthetic-label augmentation; ESM C then shows that even without the structure/function tracks, pure sequence scaling to 6B continues to yield non-diminishing returns, so the multimodal recipe is additive on top of an unsaturated scaling curve.

