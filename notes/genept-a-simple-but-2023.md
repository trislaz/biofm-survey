---
id: genept-a-simple-but-2023
title: 'GenePT: a simple but effective foundation model for genes and cells using
  ChatGPT'
authors: []
year: 2023
venue: null
arxiv: null
doi: 10.1101/2023.10.16.562533
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/genept-a-simple-but-2023.md
modalities:
- scrna
status: fetched
evidence_quality: full-text
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

| # | Axis varied | Variants compared | Setting / task | Finding |
|---|---|---|---|---|
| 1 | Gene-summary content (sensitivity analysis, Appendix A) | gene name only vs. name+NCBI summary vs. full NCBI summary card | Gene-level downstream tasks | Used to motivate the default (name+summary); name-only is surprisingly strong but full summary is preferred. |
| 2 | Text-embedding backbone | GPT-3.5 text-embedding-ada-002 (GenePT) vs. BioLinkBert (open-source biomedical LM) vs. Gene2vec vs. Geneformer | Dosage-sensitivity, bivalent/Lys4 methylation, long- vs. short-range TF (5-fold CV AUC) | GenePT-GPT-3.5 is consistently best; BioLinkBert and Gene2vec are slightly less competitive; expression-derived embeddings trail. |
| 3 | LLM input granularity | GPT-3.5 embedding of gene names only (no description) vs. full NCBI-summary GenePT | Same 4 gene-property tasks (Table 1) | Names-only is surprisingly strong on some tasks (gene nomenclature carries signal), but adding the summary helps overall. |
| 4 | Negative control | Random Gaussian embeddings (d=1536) vs. GenePT (d=1536) | Same 4 gene-property tasks | Random ≈ chance; rules out that the gain is just from large embedding dimension. |
| 5 | Downstream classifier | ℓ2-regularised logistic regression vs. random forest (default sklearn) | All gene-property tasks | Both classifiers give consistent rankings → results not driven by classifier choice / overfitting. |
| 6 | Cell-embedding strategy | GenePT-w (expression-weighted average of gene embeddings) vs. GenePT-s (GPT-3.5 sentence embedding of expression-ranked gene names) | 6 datasets × cell-type/donor clustering (ARI/AMI, Table 2); cell-type kNN annotation (Appendix C) | GenePT-s broadly > GenePT-w and Geneformer, and competitive with scGPT (each best on ~half of 9 tasks); for kNN annotation GenePT-w is one of the best. |
| 7 | Embedding ensembling | scGPT alone vs. GenePT-w alone vs. GenePT-s alone vs. ensemble of nearest neighbours from {scGPT, GenePT-w, GenePT-s} | Cell-type annotation (Appendix C, Table C4) | Simple ensembling improves over any single embedding → language and expression embeddings are complementary. |
| 8 | Context-dependent gene descriptions | Generic NCBI summary vs. context-conditioned gene descriptions | Protein–protein interaction prediction (Appendix B.5) | Context-conditioned descriptions explored as a route to improve PPI; reported as a promising direction. |
| 9 | Information-leakage check | GenePT vs. with potentially leaked test info removed from NCBI summaries | GGI / PPI benchmarks (Appendix B.3) | Performance gains are not explained by NCBI-summary leakage of benchmark labels. |
| 10 | Similarity threshold for gene-program graph | Cosine-similarity cutoffs around 0.9 (Leiden, resolution 20) | Unsupervised gene-program discovery on immune tissue (Appendix B.4) | Discovered programs are robust to threshold choice and align with known cell-type-specific biology. |
| 11 | Batch-effect robustness comparison | Raw scRNA-seq vs. Geneformer vs. scGPT vs. GenePT-s | Patient-cluster ARI on cardiomyocyte (Chaffin) and Aorta (Li) datasets; disease-phenotype LR on top of embeddings | All FM embeddings sharply reduce patient-batch ARI; GenePT-s matches scGPT on disease prediction (≈88% acc cardiomyocyte; ≈73% Aorta) and beats Geneformer. |

**Count:** 11 ablations / sensitivity analyses.

**Top take-away:** The headline ablation is #2/#3 — replacing a fully pre-trained single-cell foundation model (Geneformer/scGPT) with off-the-shelf GPT-3.5 embeddings of NCBI gene summaries matches or beats them on gene-property and cell-clustering tasks, and a Gaussian-random negative control of the same dimension performs at chance — so the signal genuinely comes from the LLM-encoded literature, not from embedding size or classifier choice.

