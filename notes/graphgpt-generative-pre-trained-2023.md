---
id: graphgpt-generative-pre-trained-2023
title: 'GraphGPT: Generative Pre-trained Graph Eulerian Transformer'
authors:
- Qifang Zhao
- Weidong Ren
- Tianyu Li
- Hong Liu
- Xingsheng He
- Xiaoxiao Xu
year: 2023
venue: null
arxiv: '2401.00529'
doi: null
url: https://arxiv.org/abs/2401.00529v3
pdf_path: papers/graphgpt-generative-pre-trained-2023.pdf
md_path: papers/md/graphgpt-generative-pre-trained-2023.md
modalities:
- other
status: extraction-failed
reason: not a bio-FM
evidence_quality: high
tags:
- graph-foundation-model
- graph-transformer
- eulerian-path
- general-purpose
- not-bio-fm
parameters: up to 2B (XXL); main Base variant ~113M
training_tokens: 1–20B graph tokens depending on dataset (e.g. 1×10⁹ for PCQM4Mv2-Base,
  2×10¹⁰ for ogbl-ppa)
training_compute: ~63 V100-GPU-hours PT + ~3 V100-GPU-hours/epoch FT for Base on PCQM4Mv2;
  8× L20 or V100 clusters
references_chased: false
added_at: '2026-04-22T19:37:10+00:00'
updated_at: '2026-04-22T20:20:21+00:00'
is_fm: false
fm_classification_reason: Generic graph FM; frontmatter explicitly notes 'not a bio-FM'.
---

## TL;DR

GraphGPT is a **general-purpose** graph foundation model (from Alibaba) that serializes arbitrary graphs into token sequences via Eulerian paths and pre-trains a standard Llama-style transformer with next-token prediction (NTP) or scheduled masked-token prediction (SMTP). It achieves SOTA on OGB benchmarks including molecular property prediction (PCQM4Mv2) and protein-protein interaction (ogbl-ppa), and scales to 2B parameters with continued gains. **Not a bio-FM**: it is a generic graph learning model evaluated on chemistry, biology, citation, and social-network benchmarks indiscriminately.

## Model

- **Name**: GraphGPT (Graph Eulerian Transformer / GET)
- **Architecture**: Standard transformer encoder (SMTP) or decoder (NTP) based on Llama, applied to graph-derived token sequences. No GNN modules or handcrafted structural features
- **Graph-to-sequence**: Graphs are losslessly converted to token sequences via (semi-)Eulerian paths. For large graphs, subgraph sampling (ShaDowKHop) + multi-token node identity encoding are used
- **Sizes**: Mini (4.2M), Small (16.8M), Medium (33.6M), Base/B₁₂ (113.2M, hidden 768, 12 layers, 12 heads), B₂₄ (226.5M), B₄₈ (453M), Large (402.7M), XXL (2.0B, hidden 1600, 48 layers, 25 heads)
- **Pre-training tasks**: NTP (autoregressive) or SMTP (bidirectional with scheduled masking). SMTP generally outperforms NTP
- **Fine-tuning**: Task-specific tokens appended — [GSUM] for graph-level, source/destination for edge-level, target node for node-level — fed through a randomly initialized MLP head

## Data

- **PCQM4Mv2**: 3.75M organic molecules from PubChemQC; nodes = atoms (9D attributes), edges = bonds (3D attributes). Task: HOMO-LUMO gap regression
- **ogbg-molpcba**: 438K molecules, 128 binary molecular property labels
- **ogbl-ppa**: 576K protein nodes from 58 species, 30M edges representing functional associations (STRING database). Task: link prediction
- **ogbn-proteins**: 132K protein nodes, 39.6M edges with 8D edge attributes encoding association strengths. Task: 112 binary function labels
- **ogbl-citation2**: 2.9M paper nodes, 30.6M citation edges
- **ogbn-arxiv**: 169K paper nodes, 1.2M edges, 40-class categorization
- **Triangles**: 45K synthetic graphs for triangle counting (structural understanding benchmark)
- **Auxiliary pre-training**: Reddit-threads (203K graphs), Erdős-Rényi random graphs (3.1M), internal real-world graphs (3.1M)
- Pre-training is dataset-specific (no single unified pre-training corpus)

## Training Recipe

- **Backbone**: Llama-based transformer via HuggingFace Transformers; parameters initialized randomly
- **Pre-training**: AdamW optimizer (β₁=0.9, β₂=0.95, ε=1e-8), warmup + linear decay, weight decay 0.1, attention dropout 0.1, max LR 3e-4. Mixed precision (FP16/FP32 or BF16). DeepSpeed Stage-2
- **Hardware**: A800-80GB GPU clusters (also V100-32G, L20, L40). Pre-training Base on PCQM4Mv2: ~63 V100-GPU-hours; ogbl-ppa Base: 58.7h on 8× L20 PT + 112.6h on 16× V100 FT
- **Sequence packing**: Multiple graph sequences packed into single entries to maximize context window utilization
- **Fine-tuning**: AdamW (β₁=0.9, β₂=0.99), warmup + cosine decay, lower LR (2–6e-4 for PCQM4Mv2, 2–3e-5 for ogbl-ppa), no/low weight decay, path dropout added at larger scales, EMA used for some node-level tasks
- **Scaling**: Log-log scaling law observed for both pre-training loss and fine-tuning loss vs. parameter count on PCQM4Mv2

## Key Ablations & Design Choices

1. **Pre-training is critical**: 10–100% performance gains across all task types (graph/edge/node) from self-supervised pre-training (Table 6)
2. **SMTP > NTP**: SMTP (bidirectional masked prediction) consistently outperforms or matches NTP (autoregressive) across benchmarks
3. **Node re-indexing as augmentation**: Cyclic re-indexing of node indices increases pre-training loss but consistently improves downstream performance across model sizes, acting as data augmentation against memorization (Table 7)
4. **Node identity encoding is essential for large graphs**: Multi-token encoding (k=2) dramatically improves edge- and node-level tasks — +11 HR@100 on ogbl-ppa, +15 ROC-AUC on ogbn-proteins (Table 8)
5. **Diverse pre-training data helps structural understanding**: Combining Triangles with Reddit-threads and internal data yields 58.96% OOD accuracy vs 26.51% with Triangles alone on triangle counting (Table 3)
6. **Attributed graph pre-training transfers structural knowledge**: Models pre-trained on attributed datasets (PCQM4Mv2, ogbl-ppa, ogbn-proteins) still improve on attribute-free structural tasks (Triangles)
7. **Scalability beyond GNNs**: GraphGPT scales to 2B parameters with sustained gains; traditional GTs and GNNs plateau. Log-log scaling law holds (Fig. 3)
8. **Cross-dataset transfer is limited**: Pre-training on external molecular data beyond PCQM4Mv2 yields diminishing returns, suggesting saturation in 2D structural information. Cross-domain transfer (social → molecular) is constrained

## Reported Insights

- PCQM4Mv2: test MAE 0.0804 (B₄₈, 453M params), surpassing prior SOTA 0.0821 (GPTrans-L)
- ogbl-ppa: HR@100 76.55% (XXL, 2B params), substantially above prior SOTA. First transformer to achieve SOTA on this benchmark
- ogbn-proteins: ROC-AUC 85.33% (Base) with only ~40-node subgraphs, competitive with AGDN (88.65%) which uses >22K-node subgraphs
- ogbl-citation2: MRR 93.05% (Base), surpassing MPLP (90.72%)
- Runtime comparable to GNNs at similar model sizes; bottleneck is CPU-based Eulerization preprocessing, not GPU inference
- No domain-specific features or inductive biases — all graph structure learned from data

## References Worth Chasing

- **Llama** (Touvron et al. 2023): Backbone architecture used for transformer
- **MaskGIT** (Chang et al. 2022): Inspiration for SMTP scheduled masking strategy
- **OGB/OGB-LSC** (Hu et al. 2021): Benchmark suite for all evaluations
- **Müller et al. 2024** ("Attending to Graph Transformers"): Comprehensive GT survey and comparison point
- **GPS++** (Masters et al. 2023): Prior SOTA GT on molecular property prediction
- **METIS** (Karypis & Kumar 1997): Graph partitioning for multi-token node encoding
- **ShaDowKHop** (Zeng et al. 2021): Subgraph sampling method used for large graphs

## Notes / Open Questions

- **Not a bio-FM**: GraphGPT is a general-purpose graph foundation model. Its biological evaluations (molecular property prediction, protein-protein interaction, protein function) are standard graph ML benchmarks, not bio-specific tasks. The model is equally applied to citation networks, Reddit threads, and random graphs
- Pre-training is dataset-specific — there is no single pre-trained checkpoint that generalizes across domains, limiting "foundation model" claims
- 3D molecular information is not used; authors note that incorporating 3D data could address the saturation in 2D structural information
- The paper claims "graph foundation model" status but lacks cross-domain zero-shot/few-shot transfer capabilities that define foundation models
- Eulerization preprocessing is a CPU bottleneck that could limit practical deployment at scale
- Code released at https://github.com/alibaba/graph-gpt; checkpoints on ModelScope
