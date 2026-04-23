---
id: poisoning-the-genome-targeted-2026
title: 'Poisoning the Genome: Targeted Backdoor Attacks on DNA Foundation Models'
authors:
- Charalampos Koilakos
- Ioannis Mouratidis
- Ilias Georgakopoulos-Soares
year: 2026
venue: null
arxiv: '2603.27465'
doi: null
url: https://arxiv.org/abs/2603.27465v1
pdf_path: papers/poisoning-the-genome-targeted-2026.pdf
md_path: papers/md/poisoning-the-genome-targeted-2026.md
modalities:
- dna
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:36:44+00:00'
updated_at: '2026-04-22T20:24:22+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Genomic foundation models trained on DNA sequences have demonstrated remarkable capabilities across diverse biological tasks, from variant effect prediction to genome design. These models are typically trained on massive, publicly sourced genomic datasets comprising trillions of nucleotide tokens, which renders them intrinsically susceptible to errors, artifacts, and adversarial issues embedded in the training data. Unlike natural language, DNA sequences lack the semantic transparency that might allow model makers to filter out corrupted entries, making genomic training corpora particularly susceptible to undetected manipulation. While training data poisoning has been established as a credible threat to large language models, its implications for genomic foundation models remain unexplored. Here, we present the first systematic investigation of training data poisoning in genomic language models. We demonstrate two complementary attack vectors. First, we show that adversarially crafted sequences can selectively degrade generative behavior on targeted genomic contexts, with backdoor activation following a sigmoidal dose-response relationship and full implantation achieved at 1 percent cumulative poison exposure. Second, targeted label corruption of downstream training data can selectively compromise clinically relevant variant classification, demonstrated using BRCA1 variant effect prediction. Our results reveal that genomic foundation models are vulnerable to targeted data poisoning attacks, underscoring the need for data provenance tracking, integrity verification, and adversarial robustness evaluation in the genomic foundation model development pipeline.
