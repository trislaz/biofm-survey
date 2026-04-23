---
id: revisiting-foundation-models-for-2026
title: Revisiting foundation models for cell instance segmentation
authors:
- Anwai Archit
- Constantin Pape
year: 2026
venue: null
arxiv: '2603.17845'
doi: null
url: https://arxiv.org/abs/2603.17845v1
pdf_path: papers/revisiting-foundation-models-for-2026.pdf
md_path: papers/md/revisiting-foundation-models-for-2026.md
modalities:
- imaging-microscopy
- imaging-pathology
status: extracted
evidence_quality: high
tags:
- benchmark
- instance-segmentation
- cell-segmentation
- SAM
- training-free-inference
- negative-results
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: '2026-04-22T19:42:01+00:00'
updated_at: '2026-04-22T20:24:55+00:00'
is_fm: false
fm_classification_reason: Evaluation/method for cell instance segmentation with FMs.
---

## TL;DR

Comprehensive benchmark of SAM-family models (SAM, SAM2, SAM3) and microscopy-specific foundation models (μSAM, CellPoseSAM, CellSAM, PathoSAM) on 36 microscopy datasets across 4 domains. Introduces Automatic Prompt Generation (APG), a **training-free** inference-time method that re-purposes μSAM's decoder predictions as point prompts for its prompt encoder, consistently improving segmentation without retraining. APG is competitive with state-of-the-art CellPoseSAM. Rich in negative results and practical lessons for adapting SAM-style models to microscopy.

## Model

- **APG is not a new model** — it is a new inference-time instance segmentation pipeline applied on top of existing μSAM / PathoSAM models (no retraining).
- Pipeline: (1) run μSAM encoder + segmentation decoder → foreground probabilities + boundary/center distance maps; (2) threshold + connected components to get seed regions; (3) derive one point prompt per component (max of boundary distance transform); (4) feed prompts through SAM prompt encoder + mask decoder → mask + IoU predictions; (5) NMS to filter overlapping masks.
- Key insight: APG is the first method combining all three SAM adaptation strategies — automatic prompts (strategy 1) + custom decoder (strategy 2) + finetuned promptable segmentation (strategy 3). CellSAM combines 1+2 but lacks finetuned promptable segmentation; CellPoseSAM and μSAM use 2+3 but lack automatic prompting.
- Default hyperparameters: t_fg=0.5, t_b=0.5, t_c=0.5, size_filter=25, t_nms=0.9.

## Data

- **Evaluation**: 36 datasets, 4 domains — cells in fluorescence microscopy (9 datasets), cells in label-free microscopy (9 datasets), nuclei in fluorescence microscopy (9 datasets), nuclei in histopathology (9 datasets).
- Datasets span phase contrast, brightfield, confocal, light-sheet, immunofluorescence, H&E, IHC, Nissl staining; 2D, 3D, and 2D+T.
- All models evaluated on test splits; some methods were trained on corresponding train splits (indicated in results).
- No new training data introduced.

## Training Recipe

- **No training performed for APG** — the method operates on top of pretrained μSAM/PathoSAM without any retraining or finetuning.
- Underlying models' training data sizes (from prior work): μSAM ~17k light microscopy images, >2M annotated cells; CellPoseSAM 22,826 images, 3.34M annotations; PathoSAM ~5k images, >400k nuclei; CellSAM trained on 10 datasets; SAM 11M images / 1B annotations; SAM3 added 5M images + 50k videos.

## Key Ablations & Design Choices

**Most important — negative results and what doesn't work:**

1. **SAM2 is worse than SAM for microscopy** — dropped from the evaluation entirely. "We do not evaluate SAM2 (w/ AMG) as we found it to be inferior to SAM in this setting. It did not segment any objects for several datasets." The video-oriented extensions actively hurt microscopy performance.

2. **SAM3 does not understand biology vocabulary** — the term "nucleus" is simply not recognized (produces ≤0.001 mSA). Shape-descriptive prompts like "irregular shape" often substantially outperform the biologically correct term "cell" (e.g. 0.489 vs 0.366 on DSB, 0.379 vs 0.341 on PanNuke). SAM3 is highly sensitive to text prompt choice.

3. **Box prompts for APG failed** — "We performed initial experiments to derive candidate box prompts from the μSAM decoder predictions. However, we found that deriving a set of high-quality prompts that over-sample objects was challenging and did not yet find a strategy competitive with the simpler point prompt derivation." This despite box prompts generally outperforming point prompts in interactive settings.

4. **Connected-component prompt derivation > distance-map-maxima derivation** — the simpler component-based strategy for generating point prompts in APG outperforms the alternative based on foreground-restricted maxima of boundary distances across all modalities (Fig. 4).

5. **AIS threshold trade-off resolved by APG** — in AIS, t_b and t_c must be tuned so each object gets exactly one seed component (over- vs under-segmentation trade-off). APG relaxes this because NMS handles multiple prompts per object, making the method more robust.

6. **Training data size dominates performance** — models with larger domain-specific training sets (CellPoseSAM, μSAM) consistently outperform; performance differences are most pronounced on out-of-domain data. This suggests data scaling > architecture for this class of models.

7. **SAM3 not yet competitive with domain-specific FMs** — despite including microscopy data in its training (LIVECell, PanNuke), SAM3 underperforms all microscopy-specific models. Mean mSA: SAM3 0.143–0.331 across domains vs CellPoseSAM 0.363–0.544 vs APG 0.344–0.541.

8. **CellSAM's rigid prompting is a weakness** — CellSAM relies on one-to-one box-to-mask mapping from CellFinder, so missed detections cannot be recovered. APG's over-sampling + NMS strategy is more robust.

9. **APG largest gains on difficult/out-of-domain data** — e.g. TOIAM: AIS 0.387 → APG 0.701 (+81%). Smaller gains on easy/in-domain cases where AIS already performs well.

## Reported Insights

- Domain-specific microscopy FMs still substantially outperform general-purpose SAM3 — specialization matters.
- APG demonstrates that combining all three SAM adaptation strategies (prompting + custom decoder + finetuned promptable segmentation) yields the best results, even without retraining.
- Finetuning SAM3 on microscopy data is a promising future direction that could close the gap.
- Even single-image finetuning of μSAM can lead to substantial improvements (citing CellSeg1 / Teuber et al.), and APG would directly benefit from such finetuning.
- Statistical significance confirmed via paired Wilcoxon signed-rank tests across all method pairs and datasets.

## References Worth Chasing

- **CellPoseSAM** (Pachitariu et al., 2025) — current SOTA, superhuman cell segmentation; trains CellPose decoder on SAM encoder, 22k images.
- **SAM3** (Carion et al., 2025) — concept-based segmentation with text/example prompts; includes some microscopy in training.
- **CellSeg1** (Zhou et al., 2024) — robust cell segmentation from a single training image; shows extreme sample efficiency.
- **Teuber et al., 2025** — parameter-efficient finetuning of SAM for biomedical imaging; few-shot adaptation.
- **CellSAM** (Marks et al., 2025) — CellFinder + SAM approach; Nature Methods.

## Notes / Open Questions

- **Major limitation**: all evaluation is 2D only, even for 3D datasets (sliced). The 3D comparison (CellPoseSAM, μSAM, SAM3 all support 3D) is explicitly deferred to future work.
- No parameter counts are reported for any model in this paper — would need to chase μSAM / SAM papers for those.
- No training compute reported (APG is training-free; underlying models' compute not discussed).
- Would be interesting to see APG applied on top of CellPoseSAM (requires adding promptable segmentation objective to CellPoseSAM training).
- SAM3 example-based prompting (providing annotated reference images) was not tested — could substantially improve SAM3 performance without finetuning.
- The sensitivity of SAM3 to text prompts (Tab. 1) raises questions about whether prompt engineering or prompt ensembling could close the gap with specialized models.
