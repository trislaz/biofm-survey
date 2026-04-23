---
id: sparse-autoencoders-reveal-organized-2026
title: 'Sparse autoencoders reveal organized biological knowledge but minimal regulatory
  logic in single-cell foundation models: a comparative atlas of Geneformer and scGPT'
authors:
- Ihor Kendiukhov
year: 2026
venue: null
arxiv: '2603.02952'
doi: null
url: https://arxiv.org/abs/2603.02952v1
pdf_path: papers/sparse-autoencoders-reveal-organized-2026.pdf
md_path: papers/md/sparse-autoencoders-reveal-organized-2026.md
modalities:
- scrna
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:12+00:00'
updated_at: '2026-04-22T20:25:58+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Background: Single-cell foundation models such as Geneformer and scGPT encode rich biological information, but whether this includes causal regulatory logic rather than statistical co-expression remains unclear. Sparse autoencoders (SAEs) can resolve superposition in neural networks by decomposing dense activations into interpretable features, yet they have not been systematically applied to biological foundation models. Results: We trained TopK SAEs on residual stream activations from all layers of Geneformer V2-316M (18 layers, d=1152) and scGPT whole-human (12 layers, d=512), producing atlases of 82525 and 24527 features, respectively. Both atlases confirm massive superposition, with 99.8 percent of features invisible to SVD. Systematic characterization reveals rich biological organization: 29 to 59 percent of features annotate to Gene Ontology, KEGG, Reactome, STRING, or TRRUST, with U-shaped layer profiles reflecting hierarchical abstraction. Features organize into co-activation modules (141 in Geneformer, 76 in scGPT), exhibit causal specificity (median 2.36x), and form cross-layer information highways (63 to 99.8 percent). When tested against genome-scale CRISPRi perturbation data, only 3 of 48 transcription factors (6.2 percent) show regulatory-target-specific feature responses. A multi-tissue control yields marginal improvement (10.4 percent, 5 of 48 TFs), establishing model representations as the bottleneck. Conclusions: These models have internalized organized biological knowledge, including pathway membership, protein interactions, functional modules, and hierarchical abstraction, yet they encode minimal causal regulatory logic. We release both feature atlases as interactive web platforms enabling exploration of more than 107000 features across 30 layers of two leading single-cell foundation models.
