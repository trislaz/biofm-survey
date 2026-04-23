---
id: towards-a-visual-language-2023
title: Towards a Visual-Language Foundation Model for Computational Pathology
authors:
- Ming Y. Lu
- Bowen Chen
- Drew F. K. Williamson
- Richard J. Chen
- Ivy Liang
- Tong Ding
- Guillaume Jaume
- Igor Odintsov
- Andrew Zhang
- Long Phi Le
- Georg Gerber
- Anil V Parwani
- Faisal Mahmood
year: 2023
venue: null
arxiv: '2307.12914'
doi: null
url: https://arxiv.org/abs/2307.12914v2
pdf_path: papers/towards-a-visual-language-2023.pdf
md_path: papers/md/towards-a-visual-language-2023.md
modalities:
- imaging-pathology
- multimodal
status: extracted
evidence_quality: full-text
tags:
- CoCa
- contrastive-VL
- path-text-pairs
- vision-language
- histopathology
- zero-shot-classification
- captioning
- retrieval
parameters: ~ViT-B/16 image encoder (~86M) + 12-layer text encoder + 12-layer multimodal
  decoder (768-d, 3072 hidden); total estimated ~300M
training_tokens: 1.17M image-caption pairs (human-only), 40 epochs; unimodal image
  pretrain on 16M tiles, 80 epochs; unimodal text pretrain on ~1M pathology texts,
  15k steps
training_compute: 8×A100-80GB (VL pretrain); 4×A100-80GB (unimodal image); 4×A100-80GB
  (unimodal text)
references_chased: false
added_at: '2026-04-22T21:55:58+00:00'
updated_at: '2026-04-22T21:56:03+00:00'
is_fm: true
fm_classification_reason: MI-Zero/PLIP-style pathology VL FM.
---

## TL;DR

CONCH is a CoCa-based visual-language foundation model for computational pathology. It combines a ViT-B/16 image encoder, a 12-layer text encoder, and a 12-layer multimodal text decoder, trained jointly with contrastive + captioning losses on 1.17M histopathology image-caption pairs curated from PubMed and educational sources. Both encoders are pre-initialized with self-supervised unimodal pretraining (iBOT on 16M pathology tiles; GPT-style LM on ~1M pathology texts). CONCH achieves SOTA on 13 benchmarks spanning zero-shot classification (ROI + WSI), few-shot supervised classification, cross-modal retrieval, zero-shot segmentation, and image captioning, substantially outperforming PLIP, BiomedCLIP, and OpenAI CLIP.

## Model

- **Architecture**: CoCa (Contrastive Captioners) framework with three components:
  - **Image encoder**: ViT-B/16 backbone (12 Transformer layers, 12 heads, 768-d embedding, 3072 hidden, patch 16×16) + two attentional poolers:
    - Contrastive pooler: 1 learned query → 1 global image token for contrastive alignment.
    - Captioning pooler: 256 learned queries → 256 image tokens for generative captioning.
  - **Text encoder**: 12-layer GPT-style Transformer (768-d, 3072 hidden, causal attention). Appends a learned `<CLS>` token for global text representation.
  - **Multimodal decoder**: 12-layer GPT-style Transformer with cross-attention layers (after each self-attention layer) to incorporate image tokens. Final LM head predicts next token.
- Learned temperature τ for contrastive loss.
- Input resolution: 448×448 during pretraining (resize short edge + center-crop; zero-pad small images).
- Vocabulary: 32,000 tokens.
- Max caption sequence length: 128 tokens (VL pretrain), 512 tokens (unimodal LM pretrain).

## Data

- **VL pretraining dataset**: 1,170,647 image-caption pairs (human-only subset), curated from:
  - **PMC-Path**: pathology-specific image-caption pairs extracted from PubMed Central Open Access articles using automated pipeline (YOLOv5 for histopath image detection, GPT-style LM for caption splitting, CLIP for image-caption alignment).
  - **EDU**: educational pathology resources (manually cleaned, ~45k pairs, used as seed for cleaning pipeline).
  - Full unfiltered dataset: 1,786,362 pairs; filtered to 1,170,647 (human-only, excluding animal histopath) and further to 457,372 (H&E only). Human-only performed best overall.
- Covers 19+ pathology topics (breast, lung, GI, GU, liver, kidney, neuro, skin, soft tissue, etc.). Diverse caption lengths.
- **Unimodal image pretraining data**: 16M tiles (256×256 px, 20× magnification) from 21,442 WSIs spanning 350+ OncoTree cancer subtypes. In-house.
- **Unimodal text pretraining data**: pathology educational texts + 550k+ in-house surgical pathology reports (de-identified) + 400k histopathology-relevant PubMed abstracts.
- **Downstream evaluation**: 13 benchmarks across 7 tasks (zero-shot slide/ROI classification, few-shot classification, retrieval, segmentation, captioning). Datasets: TCGA BRCA/NSCLC/RCC, DHMC LUAD, CRC100k, WSSS4LUAD, SICAP, DigestPath, Source A/B, TCGA LUAD.

## Training Recipe

- **Stage 1 — Unimodal image pretraining (iBOT)**:
  - 80 epochs on 16M tiles, 4×A100-80GB.
  - Batch size 1024, cosine LR schedule (peak 2e-3 → 2e-6), AdamW (β₁=0.9, β₂=0.999), weight decay 0.04→0.4.
  - Drop path 0.1, 2 global crops (scale 0.32–1.0) + 10 local crops (scale 0.05–0.32).
  - Partial prediction (block shape, ratio 0.3). fp16.

- **Stage 2 — Unimodal text pretraining (causal LM)**:
  - 24-layer GPT-style Transformer, 15,000 steps, 4×A100-80GB.
  - Batch size 64, gradient accumulation 8 (effective 512). Linear LR schedule, peak 1e-3, 500 warmup steps.
  - Sequence length 512. fp16.
  - After pretraining: first 12 layers → text encoder init; last 12 layers + LM head → multimodal decoder init.

- **Stage 3 — Visual-language pretraining (CoCa)**:
  - 40 epochs, 8×A100-80GB.
  - Batch size 384/GPU, gradient accumulation 4 → effective global batch size 1536 (note: 8 GPUs × 384/4 path seems inconsistent; paper says 384 batch, grad accum 4, so effective = 384 × 4 = 1536 with DDP across 8 GPUs implies local batch 48).
  - Equal-weighted contrastive loss + captioning loss.
  - AdamW (β₁=0.9, β₂=0.999), weight decay 0.2, cosine LR schedule, peak 1e-4, 250 warmup steps. fp16.
  - Image size 448×448. Max caption length 128.

## Key Ablations & Design Choices

1. **Pretraining data filtering** (Extended Data Figure 8):
   - Human-only (1.17M) with CoCa performs best overall on zero-shot classification across 7 tasks.
   - Full unfiltered (1.79M, including animal histopath) and H&E-only (457k) both underperform human-only.
   - CoCa > CLIP on human-only data (CoCa adds captioning objective and multimodal decoder).

2. **CoCa vs CLIP on same data**:
   - Human-only CoCa outperforms human-only CLIP on zero-shot classification average.
   - Human-only CLIP slightly better on cross-modal retrieval average — expected since CLIP focuses purely on contrastive alignment.

3. **Unimodal pre-initialization is critical** (cited from MI-Zero reference):
   - Self-supervised pretraining of image and text encoders before joint VL pretraining substantially improves zero-shot transfer.

4. **Prompt ensembling** (Extended Data Figure 2):
   - Ensembling multiple text prompts per class consistently boosts zero-shot performance vs. single prompts, except when baseline performance is near chance.

5. **Zero-shot vs. few-shot trade-off**:
   - CONCH zero-shot outperforms PLIP/BiomedCLIP few-shot (with supervised learning) up to 64 labels/class on BRCA, 128/class on NSCLC, 64/class on Gleason grading.
   - CONCH with just 1–4 labels/class surpasses other models' zero-shot performance.

6. **Image encoder for supervised tasks**:
   - CONCH encoder performs comparably to CTransPath (self-supervised SOTA pathology encoder) on ROI-level linear probing, despite CTransPath training on much more unlabeled pathology data.

## Reported Insights

- Histopathology VLP at the scale of ~1.17M pairs with CoCa architecture is sufficient to achieve large gains over prior pathology VLP models (PLIP, BiomedCLIP) which used either smaller pathology-specific data or less domain-focused pretraining.
- Automated data cleaning pipeline (object detection + caption splitting + CLIP-based alignment) is essential for scaling histopathology image-caption pair curation from PubMed.
- Zero-shot WSI-level classification (via MI-Zero top-K pooling) works surprisingly well: 90% on NSCLC, 89.3% on RCC, 84% on BRCA — PLIP/BiomedCLIP near chance on BRCA.
- Cosine-similarity heatmaps from zero-shot classification provide interpretable tumor localization that closely matches pathologist annotations.
- Captioning capability (unique to CoCa, not available in CLIP-only models) opens new direction for pathology, though absolute performance remains limited by fine-tuning data scale (n=558).
- Scale of pretraining data is acknowledged as the key limitation — still far below billion-scale general-domain VLP.
- Fine-grained (cellular/sub-cellular) recognition remains out of scope for current VLP models.

## References Worth Chasing

- **CoCa** [47] (Yu et al., 2022) — the underlying VL pretraining framework; combines contrastive + captioning.
- **iBOT** [91] (Zhou et al., 2022) — self-supervised ViT pretraining used for image encoder initialization.
- **MI-Zero** [79] (Lu et al., 2023) — extends zero-shot VLP to gigapixel WSIs via top-K pooling; same lab.
- **PLIP** [77] (Huang et al., 2023) — pathology VLP from Twitter data; key baseline consistently outperformed.
- **BiomedCLIP** [68] (Zhang et al., 2023) — biomedical CLIP on PMC-15M; second-strongest baseline.
- **CTransPath** [84] (Wang et al., 2022) — SOTA self-supervised pathology image encoder; competitive with CONCH on supervised tasks.
- **CLIP** [45] (Radford et al., 2021) — foundational contrastive VLP; OpenAI CLIP used as baseline.
- **ABMIL** [81] (Ilse et al., 2018) — attention-based MIL used for WSI supervised classification downstream.

## Notes / Open Questions

- Exact total parameter count is never stated. ViT-B/16 backbone is ~86M; text encoder (12 layers, 768-d) is ~110M; multimodal decoder (12 layers + cross-attention, 768-d) is ~130M; plus attentional poolers and embeddings. Total likely ~300–350M.
- Training compute (GPU-hours, FLOPs) not reported. Only hardware configs given: 8×A100 for VL, 4×A100 for each unimodal stage.
- Batch size description is confusing: "local batch size of 48 per GPU" and "gradient accumulation to achieve effective global batch size of 1536" (48 × 8 × 4 = 1536 ✓), but Table 29 says "Batch size 384, Gradient accumulation 4" (384 × 4 = 1536 ✓ if 384 is already global). Likely 384 is global batch, grad accum 4 yields 1536 effective.
- The 24-layer GPT-style LM is split in half: first 12 → text encoder, last 12 → multimodal decoder. Clever weight-sharing initialization.
- Unimodal image pretraining data (16M tiles, 21k WSIs) and text data (550k reports) are in-house and not publicly available — limits full reproducibility.
- Model weights "may be requested upon institutional permission" — not openly released at time of writing. (Later released on HuggingFace as conch.)
- Published in Nature Medicine 2024 — the arxiv preprint is from July 2023.
- No comparison with generative VLP approaches (BLIP, BLIP-2) or with larger ViT scales (ViT-L/H).
- Captioning evaluation is limited by very small fine-tuning set (558 training examples); some generated captions are memorized verbatim from training data.
- The paper does not explore region-level or cell-level VLP tasks (mitosis detection, fine-grained segmentation, cell counting).

## Verification (Rev 3)

| # | Claim (insights.md) | Verdict | Evidence |
|---|---|---|---|
| 1 | "CONCH uses CoCa-style contrastive + captioning learning across histology images and pathology text" (L190) | **supported** | Paper §Intro: "Based on CoCa⁴⁷ … trained via a combination of contrastive alignment objectives … and a captioning objective" (lines 78–81). |
| 2 | "CONCH curated 1.17 M image–caption pairs for vision-language pretraining" (L244) | **supported** | Abstract: "over 1.17 million image-caption pairs" (line 25); Methods: "dataset of 1,170,647 human pairs" (line 478). |
| 3 | "For histology + text, CONCH applies CoCa-style joint contrastive + captioning, requiring unimodal pre-initialisation of both towers for best results" (L253) | **supported** | CoCa + contrastive/captioning confirmed (see #1). Unimodal pre-init: "performing self-supervised pretraining of unimodal modules … can substantially improve downstream zero-shot transfer performance" (lines 541–543); image encoder pre-trained with iBOT (line 543), text model split into encoder + decoder init (lines 564–567). Finding is cited from MI-Zero⁷⁹ but adopted and stated as design rationale in this paper. |
| 4 | "CONCH requires unimodal pre-initialisation (separate image and text pretraining) before vision-language alignment for best results" (L288) | **supported** | Same evidence as #3. Paper explicitly states this substantially improves zero-shot transfer and implements it for both image (iBOT) and text (causal LM → split init) encoders. |
| 5 | "CONCH (~300 M, CoCa) trained on 1.17 M image–caption pairs. Enables zero-shot WSI classification (90 % NSCLC, 89.3 % RCC). Unimodal pre-initialisation critical." (L537–538) | **partial** | CoCa ✓, 1.17 M ✓, zero-shot 90.0 % NSCLC and 89.3 % RCC ✓ (line 141), unimodal pre-init ✓. However, **~300 M parameter count is never stated in the paper**; it is an estimate derived from architecture dimensions (see Notes in this file). |
| 6 | "CONCH demonstrates this paradigm for histopathology specifically." (L566) | **supported** | The paper positions CONCH as a VL foundation model for computational pathology using contrastive + captioning pretraining (lines 23–31, 78–82). Context sentence mentions "CLIP-style contrastive pretraining"; CONCH uses CoCa which extends CLIP with captioning — minor simplification but claim is accurate. |


## Ablations (Rev 4)

| Variable | Settings | Metric / dataset | Result | Conclusion |
|---|---|---|---|---|
| Pretraining objective | CoCa (contrastive + captioning) vs. CLIP (contrastive only), both on human-only data (n=1,170,647) | Zero-shot subtyping/grading (TCGA BRCA/RCC/NSCLC, DHMC LUAD, CRC100k, WSSS4LUAD, SICAP) — bal. acc / κ | CONCH (CoCa, human-only) best on average across the 7 zero-shot classification tasks (Ext. Fig. 8a, lines 934–940) | Adding the captioning loss to contrastive pretraining (CoCa) improves downstream zero-shot classification over CLIP-style contrastive-only |
| Pretraining objective for retrieval | CoCa vs. CLIP, both human-only | Cross-modal retrieval mean recall on Source A (n=797), Source B (n=1,755), TCGA LUAD (n=165) | CONCH (CLIP) performs best on average for retrieval (Ext. Fig. 8b, lines 941–942) | Contrastive-only objective is slightly stronger for cross-modal retrieval; captioning loss helps classification more than retrieval |
| Pretraining-data filtering | (i) full unfiltered PMC-Path+EDU (n=1,786,362) vs. (ii) human-only (n=1,170,647) vs. (iii) human + H&E-only (n=457,372) | Same 7 zero-shot classification tasks (Ext. Fig. 8a) | Human-only (1.17 M) achieves best average performance; both unfiltered and the more aggressive H&E-only filter are worse (lines 478–481, 934–940) | Filtering out non-human animal histology helps; over-filtering down to H&E-only loses too much data and hurts performance — keep human-only |
| Prompt strategy at inference | Single randomly sampled prompt (50 samples) vs. ensembled mean text embedding over prompt pool | Zero-shot classification on 4 slide-level + ROI-level tasks across CONCH, PLIP, BiomedCLIP, OpenAICLIP (Ext. Fig. 2; Ext. Tables 1–14) | Prompt ensembling substantially boosts zero-shot accuracy over the median single-prompt run for most models on most tasks; exception is when single-prompt median is near chance (e.g. OpenAICLIP, PLIP on TCGA BRCA), where ensembling does not help (lines 867–881) | Always ensemble class-name × template prompts at inference; ensembling cannot rescue a model that fundamentally fails on the task |
| Unimodal pre-initialisation of towers | With unimodal pretraining (image encoder via iBOT on 16 M tiles; text encoder/decoder split-init from causal LM) vs. random init | Downstream zero-shot transfer | "Performing self-supervised pretraining of unimodal modules … can substantially improve downstream zero-shot transfer performance" (lines 541–543, attributed to MI-Zero and adopted by CONCH) | Pre-train each tower unimodally before vision-language alignment — critical for zero-shot transfer in histopathology |

**Design-choice take-aways:**
- Combine contrastive + captioning losses (CoCa) for classification; pure contrastive (CLIP) is marginally better only for retrieval.
- Filter pretraining captions to **human histology** but do not over-filter to H&E-only — data volume matters.
- **Ensemble prompts** (class-name × template pool) at zero-shot inference; it is a near-free accuracy boost when the model is competent.
- **Pre-train both towers unimodally** (iBOT for the ViT, causal-LM init for text encoder + decoder) before aligning — needed to make pathology VL transfer work.
