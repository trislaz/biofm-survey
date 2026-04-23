---
id: enabling-clinical-use-of-2026
title: Enabling clinical use of foundation models in histopathology
authors:
- Audun L. Henriksen
- Ole-Johan Skrede
- Lisa van der Schee
- Enric Domingo
- Sepp De Raedt
- Ilyá Kostolomov
- Jennifer Hay
- Karolina Cyll
- Wanja Kildal
- Joakim Kalsnes
- Robert W. Williams
- Manohar Pradhan
- John Arne Nesheim
- Hanne A. Askautrud
- Maria X. Isaksen
- Karmele Saez de Gordoa
- Miriam Cuatrecasas
- Joanne Edwards
- TransSCOT group
- Arild Nesbakken
- Neil A. Shepherd
- Ian Tomlinson
- Daniel-Christoph Wagner
- Rachel S. Kerr
- Tarjei Sveinsgjerd Hveem
- Knut Liestøl
- Yoshiaki Nakamura
- Marco Novelli
- Masaaki Miyo
- Sebastian Foersch
- David N. Church
- Miangela M. Lacle
- David J. Kerr
- Andreas Kleppe
year: 2026
venue: null
arxiv: '2602.22347'
doi: null
url: https://arxiv.org/abs/2602.22347v1
pdf_path: papers/enabling-clinical-use-of-2026.pdf
md_path: papers/md/enabling-clinical-use-of-2026.md
modalities:
- imaging-pathology
status: converted
evidence_quality: unknown
tags: []
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:37:15+00:00'
updated_at: '2026-04-22T20:19:35+00:00'
---

## TL;DR

_(seed — not yet extracted)_

## Abstract (from arxiv)

Foundation models in histopathology are expected to facilitate the development of high-performing and generalisable deep learning systems. However, current models capture not only biologically relevant features, but also pre-analytic and scanner-specific variation that bias the predictions of task-specific models trained from the foundation model features. Here we show that introducing novel robustness losses during training of downstream task-specific models reduces sensitivity to technical variability. A purpose-designed comprehensive experimentation setup with 27,042 WSIs from 6155 patients is used to train thousands of models from the features of eight popular foundation models for computational pathology. In addition to a substantial improvement in robustness, we observe that prediction accuracy improves by focusing on biologically relevant features. Our approach successfully mitigates robustness issues of foundation models for computational pathology without retraining the foundation models themselves, enabling development of robust computational pathology models applicable to real-world data in routine clinical practice.
