---
id: mining-functional-modules-by-2017
title: Mining Functional Modules by Multiview-NMF of Phenome-Genome Association
authors:
- YaoGong Zhang
- YingJie Xu
- Xin Fan
- YuXiang Hong
- Jiahui Liu
- ZhiCheng He
- YaLou Huang
- MaoQiang Xie
year: 2017
venue: null
arxiv: '1705.03998'
doi: null
url: https://arxiv.org/abs/1705.03998v1
pdf_path: papers/mining-functional-modules-by-2017.pdf
md_path: papers/md/mining-functional-modules-by-2017.md
modalities:
- imaging-cell
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:19+00:00'
updated_at: '2026-04-22T20:22:47+00:00'
is_fm: false
fm_classification_reason: Multiview-NMF method, not an FM.
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Background: Mining gene modules from genomic data is an important step to detect gene members of pathways or other relations such as protein-protein interactions. In this work, we explore the plausibility of detecting gene modules by factorizing gene-phenotype associations from a phenotype ontology rather than the conventionally used gene expression data. In particular, the hierarchical structure of ontology has not been sufficiently utilized in clustering genes while functionally related genes are consistently associated with phenotypes on the same path in the phenotype ontology. Results: We propose a hierarchal Nonnegative Matrix Factorization (NMF)-based method, called Consistent Multiple Nonnegative Matrix Factorization (CMNMF), to factorize genome-phenome association matrix at two levels of the hierarchical structure in phenotype ontology for mining gene functional modules. CMNMF constrains the gene clusters from the association matrices at two consecutive levels to be consistent since the genes are annotated with both the child phenotype and the parent phenotype in the consecutive levels. CMNMF also restricts the identified phenotype clusters to be densely connected in the phenotype ontology hierarchy. In the experiments on mining functionally related genes from mouse phenotype ontology and human phenotype ontology, CMNMF effectively improved clustering performance over the baseline methods. Gene ontology enrichment analysis was also conducted to reveal interesting gene modules. Conclusions: Utilizing the information in the hierarchical structure of phenotype ontology, CMNMF can identify functional gene modules with more biological significance than the conventional methods. CMNMF could also be a better tool for predicting members of gene pathways and protein-protein interactions. Availability: https://github.com/nkiip/CMNMF
