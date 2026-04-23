# De-risking: Hi-C Contact-Guided Autoregressive DNA Language Model

## Hypothesis

A DNA language model trained autoregressively on **paired loci that are in
3D chromatin contact** will learn enhancer–promoter regulatory grammar that
a linear-order model misses.

## Core Idea

Instead of training on `…ACGT…` in linear chromosomal order, we:

1. Tile the genome into 5 kb bins (standard Hi-C resolution).
2. Compute **observed/expected (O/E)** Hi-C contacts, excluding the
   near-diagonal (< 50 kb genomic distance) to focus on true long-range loops.
3. For each anchor bin, **sample one distal contact** bin (probability ∝ O/E).
4. Concatenate `[anchor_DNA] [SEP] [contact_DNA]` → 10 kb + separator.
5. Train a causal (AR, next-token) language model on these paired windows.

The AR objective learns: *given the DNA at this locus, predict the DNA at
the locus it physically contacts in 3D* — the regulatory grammar of
chromatin loops.

---

## Experimental Design

### Arms (5 conditions × 3 seeds = 15 runs)

| Arm | Training sequences | Purpose |
|-----|-------------------|---------|
| **Linear** | 10 kb sliding windows (no separator) | Standard baseline |
| **Segmented-linear** | anchor 5 kb `[SEP]` adjacent 5 kb | Controls for the chunked-concatenation format |
| **3D-paired** | anchor 5 kb `[SEP]` O/E-sampled distal contact 5 kb | **Test hypothesis** |
| **Distance-matched random** | anchor 5 kb `[SEP]` random bin at same genomic distance, same chr | Controls for distance/chromosome bias |
| **Hybrid** | 80% linear + 20% 3D-paired batches | Tests 3D signal as augmentation |

- All arms see the **same total tokens per step** (same compute budget).
- Contact order **randomised each epoch** (anchor always first, but which
  contact is sampled varies) — avoids learning an arbitrary contact ranking.

### Data

| Component | Source | Size |
|-----------|--------|------|
| Reference genome | hg38 (UCSC) | 3.1 Gb |
| Hi-C contact map | **K562**, ENCODE, KR-normalised, 5 kb resolution | ~600 k bins |
| Enhancer–promoter ground truth | Fulco et al. 2019 CRISPRi (**K562**) | ~6,000 pairs |
| Expression ground truth | ENCODE CAGE-seq (**K562**) | ~20 k TSS |

> **Cell-type matched**: Hi-C, CRISPRi, and CAGE-seq all from **K562** to
> avoid cross-cell-type confounds.

**Train/val/test split by chromosome** (Enformer-style, no overlap):
- Train: chr1, chr2, chr4–9, chr12, chr14–16, chr18–22, chrX
- Val: chr10, chr11
- Test: chr3, chr13, chr17

**Critical**: when building 3D-paired sequences, both anchor and contact
bins must belong to the **same split** (train contacts only from train
chromosomes, etc.) to prevent data leakage.

### Bin Filtering

Before training, exclude:
- Bins with > 50% N content (unmappable / centromeric)
- Bins in the ENCODE blacklist (hg38)
- Bins with < 10 total Hi-C contacts after KR normalisation

### Model Architecture

| Hyperparameter | Value | Rationale |
|---------------|-------|-----------|
| Architecture | GPT-2-small (causal Transformer) | Well-understood |
| Layers | 6 | Sufficient for 10 kb context |
| Hidden dim | 384 | ~10 M params |
| Heads | 6 | 64 dim/head |
| Tokenisation | Character-level (A/C/G/T/N/SEP = 6 tokens) | Avoids tokenisation confounds |
| Context length | 10,001 characters (5 kb + SEP + 5 kb) | Fits easily on 1 GPU |
| Positional encoding | **Segment-local RoPE** | Positions reset to 0 after [SEP] — prevents fake distance signals |
| Segment IDs | 0 for anchor, 1 for contact | Added to embeddings so model knows which segment is which |
| Parameters | ~10 M | Cheap; enough for derisking |

> **Why segment-local positions?** Standard RoPE across both bins would
> encode a meaningful relative distance between anchor token 4999 and
> contact token 0, which is biologically meaningless. Resetting positions
> at [SEP] forces the model to learn content-based (not position-based)
> cross-segment relationships.

### Training

| Setting | Value |
|---------|-------|
| GPU | 1× A100 80 GB |
| Batch size | 256 |
| Optimiser | AdamW, lr = 3e-4, β₁=0.9, β₂=0.95, wd=0.1 |
| LR schedule | Cosine decay, 1 k step warmup |
| Steps | 100 k |
| Total tokens/arm | 256 × 10 k × 100 k = **256 B nt** |
| Training time/arm | ~6–8 h |
| Seeds | 3 per arm |
| Total experiment | 15 runs × 7 h ≈ **~4.5 GPU-days** |

### Sequence Construction

```python
# 3D-paired arm (per epoch):
for anchor_bin in train_bins:
    # O/E contacts, excluding < 50 kb genomic distance
    oe = observed_expected(hic, anchor_bin)
    oe = oe[abs(oe.index - anchor_bin) > 10]  # > 50 kb at 5 kb resolution
    oe = oe[oe.index.isin(train_bins)]         # same-split only
    contact = sample(oe.index, p=oe / oe.sum())  # sample ∝ O/E
    seq = genome[anchor_bin] + "[SEP]" + genome[contact]
    yield seq

# Distance-matched random control:
for anchor_bin in train_bins:
    oe = observed_expected(hic, anchor_bin)
    oe = oe[abs(oe.index - anchor_bin) > 10]
    oe = oe[oe.index.isin(train_bins)]
    contact = sample(oe.index, p=uniform)  # uniform over same-distance bins
    seq = genome[anchor_bin] + "[SEP]" + genome[contact]
    yield seq

# Segmented-linear control:
for anchor_bin in train_bins:
    adjacent = anchor_bin + 1                  # next 5 kb bin
    seq = genome[anchor_bin] + "[SEP]" + genome[adjacent]
    yield seq
```

---

## Evaluation Protocol

### Eval 1 — Enhancer–Promoter Interaction Prediction (PRIMARY)

Cell-type matched (K562 Hi-C + K562 CRISPRi).

1. Extract last-layer mean-pool embeddings for each 5 kb bin (test chr only).
2. For each (enhancer, promoter) pair from Fulco et al.:
   - Feature = `[emb_e ⊕ emb_p ⊕ |emb_e − emb_p|]`
   - **Distance-matched negatives**: for each true pair (e, p), sample 5
     non-interacting pairs at the same genomic distance to control for
     distance bias.
3. Logistic regression, 5-fold CV within test chromosomes.
4. Report **AUROC + AUPRC** (mean ± std over 3 seeds).

**Go signal**: 3D-paired AUROC > Linear by ≥ 3 pp (mean over seeds).

### Eval 2 — Contact Map Recovery (sanity check)

1. Embed all test-chromosome 5 kb bins.
2. Sample 50 k random pairs, **stratified by genomic distance** (10 distance
   bins: 50 kb, 100 kb, 200 kb, … 5 Mb, > 5 Mb).
3. Within each distance bin, compute Spearman(cosine_sim, log O/E Hi-C).
4. Report per-distance-bin Spearman across arms.

**Expected**: 3D-paired shows higher Spearman at long distances (> 500 kb)
where loops dominate.

### Eval 3 — Gene Expression Prediction (transfer)

1. Per-TSS 5 kb bin embedding → linear probe → log(K562 CAGE + 1).
2. Pearson r on test chromosomes (mean ± std over 3 seeds).

**Expected**: Hybrid ≥ Linear > 3D-paired (3D-paired may hurt local grammar).

### Eval 4 — Motif Enrichment Sanity Check

1. Run attention attribution (gradient × input) on 3D-paired model.
2. Check whether high-attribution positions in the **contact segment** are
   enriched for CTCF, cohesin (RAD21), or YY1 motifs (known loop anchors).
3. Compare with linear model's attribution on same positions.

**Expected**: 3D-paired model assigns more attribution to loop-anchor motifs
in the distal segment.

---

## Decision Criteria

| Outcome | Decision |
|---------|----------|
| 3D-paired AUROC on E-P > Linear by ≥ 3 pp (seed-averaged) | **Go** — scale up |
| 3D-paired ≈ Linear but Hybrid > Linear by ≥ 2 pp | **Conditional go** — 3D helps as augmentation |
| 3D-paired ≈ Distance-matched random (both > Linear) | **Pivot** — distance/chr effect, not 3D-specific |
| 3D-paired ≈ Segmented-linear ≈ Linear | **No-go** — concatenation format has no value |
| Distance-matched random > 3D-paired | **No-go** — Hi-C signal is counterproductive |

---

## Risks and Mitigations

| Risk | Likelihood | Mitigation |
|------|-----------|------------|
| **Local grammar destroyed** by pairing distant loci | High | Hybrid arm (80% linear) preserves local context; each 5 kb bin is internally linear |
| **Hi-C near-diagonal dominates** contacts | High | Exclude < 50 kb contacts; use O/E instead of raw counts |
| **Data leakage** across chromosome splits | High | Restrict contacts to same split; verified programmatically |
| **Distance confound** in E-P eval | High | Distance-matched negatives + distance-matched random control arm |
| **Hi-C noise** | Medium | KR normalisation; filter low-contact bins |
| **Model too small** for subtle signal | Medium | If Eval 2 shows structure but Eval 1 flat → scale to 30 M |
| **Positional encoding artefacts** | Medium | Segment-local RoPE + segment IDs; no cross-segment positional signal |
| **Memorisation of concatenation patterns** | Medium | Resample contact each epoch; random + segmented-linear controls |
| **Single cell type** | Low | K562 is well-characterised; extend to GM12878 if Go |

---

## Extensions (if Go)

1. **Multi-contact context**: anchor + 3 sampled contacts (20 kb total),
   contacts in random order per epoch.
2. **Graph-walk serialisation**: random walk on Hi-C graph → sequences
   follow the 3D polymer path.
3. **Attention-bias alternative**: don't reorder sequences; instead inject
   O/E Hi-C as additive attention bias in a standard linear-order model.
   Directly comparable and less disruptive to local context.
4. **Multi-cell-type**: alternate Hi-C graphs from K562, GM12878, IMR90 →
   cell-type-conditional representations.
5. **MLM variant**: masked LM instead of AR on paired sequences (predict
   masked bins given 3D neighbour context).
6. **Scale**: 300 M+ params with full-genome Hi-C-augmented data.

---

## Timeline

| Day | Activity |
|-----|----------|
| 1 | Download hg38 + K562 Hi-C + CRISPRi + CAGE-seq; build O/E contact graph; filter bins; generate sequence sets for all 5 arms |
| 2–3 | Train 15 runs (5 arms × 3 seeds); parallelise across 2–4 GPUs |
| 4 | Extract embeddings; run Evals 1–4 |
| 5 | Statistical analysis; write go/no-go report |

**Total: ~1 week, 2–4 GPUs, ~5 GPU-days compute.**

---

## Required Packages

```
torch >= 2.0
transformers          # GPT-2 config scaffolding
cooler                # Hi-C .mcool/.cool loading
pysam                 # genome FASTA access
scikit-learn          # linear probes
scipy                 # sparse matrices, Spearman
matplotlib / seaborn  # plots
pybedtools            # ENCODE blacklist filtering
HOMER or MEME         # motif enrichment (Eval 4)
```
