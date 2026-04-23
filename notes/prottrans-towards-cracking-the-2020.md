---
id: prottrans-towards-cracking-the-2020
title: 'ProtTrans: Towards Cracking the Language of Life''s Code Through Self-Supervised
  Deep Learning and High Performance Computing'
authors:
- Ahmed Elnaggar
- Michael Heinzinger
- Christian Dallago
- Ghalia Rihawi
- Yu Wang
- Llion Jones
- Tom Gibbs
- Tamas Feher
- Christoph Angerer
- Martin Steinegger
- Debsindhu Bhowmick
- Burkhard Rost
year: 2020
venue: IEEE TPAMI 2022
arxiv: '2007.06225'
doi: null
url: https://arxiv.org/abs/2007.06225v3
pdf_path: papers/prottrans-towards-cracking-the-2020.pdf
md_path: papers/md/prottrans-towards-cracking-the-2020.md
modalities:
- protein-sequence
status: extracted
evidence_quality: full-text
tags:
- arch-comparison
- scaling
- T5-XL
- BERT
- ALBERT
- XLNet
- Electra
- Transformer-XL
- supercomputer
- HPC
- transfer-learning
- secondary-structure
- subcellular-localization
- protein-LM
parameters: up to 11B (ProtT5-XXL); ProtT5-XL 3B; ProtBert/ProtXLNet/ProtAlbert ~40M;
  ProtTXL-BFD 562M; ProtElectra 420M
training_tokens: up to 393B amino-acid tokens (BFD); UniRef100 88B; UniRef50 14B
training_compute: Summit supercomputer 5616 GPUs (936 nodes x 6 V100) for ProtTXL;
  TPU Pod v3-512/v3-1024 for other models; ProtT5-XXL trained 920k+343k steps on 1024
  TPU cores; ProtT5-XL trained 1.2M+991k steps on 512 TPU cores
references_chased: false
added_at: '2026-04-22T21:52:00+00:00'
updated_at: '2026-04-22T21:58:33+00:00'
is_fm: true
fm_classification_reason: 'ProtTrans: family of pretrained protein LMs.'
---

## TL;DR

ProtTrans is a systematic comparison of six NLP Transformer architectures (Transformer-XL, XLNet, BERT, ALBERT, Electra, T5) trained on protein sequences at unprecedented scale—up to 393 billion amino-acid tokens from the BFD dataset—using ORNL Summit (5616 GPUs) and Google TPU Pods (up to 1024 cores). The best model, ProtT5-XL-U50 (3B params, encoder-only at inference), matches or exceeds the state-of-the-art in secondary structure prediction (Q3 ≈ 81–85%) **without** evolutionary information (MSAs), for the first time bypassing expensive database searches. Performance correlates with the number of training samples seen (Spearman ρ = 0.62), and increasing training duration is more important than increasing model size.

## Model

- **Six architectures compared** (all adapted from NLP originals with increased depth and vocabulary set to 20 amino acids + special tokens):
  - **ProtTXL** (Transformer-XL): auto-regressive; 562M params; trained on BFD and UniRef100 separately.
  - **ProtBert** (BERT): masked-LM; ~420M params; trained on UniRef100 and BFD separately. Layers increased vs. original BERT.
  - **ProtAlbert** (ALBERT): weight-sharing masked-LM; ~40M params; trained on UniRef100 only. Albert-xlarge-v2 config; single layer stacked multiple times.
  - **ProtXLNet**: permutation auto-regressive; ~40M params; 30 layers; trained on UniRef100; Adam optimizer (batch size only 1024).
  - **ProtElectra**: generator + discriminator; ~420M params; 30 layers; trained on UniRef100. On-the-fly masking.
  - **ProtT5-XL** (3B) and **ProtT5-XXL** (11B): encoder-decoder with BERT-style single-token masking (not span masking). T5-XL uses 8-way model parallelism; T5-XXL uses 32-way. At inference, only the encoder is used (decoder dropped—cuts params by half). Half-precision inference fits on a single Nvidia Titan V (12 GB).
- **Vocabulary**: 20 standard amino acids + unknown (X) + special tokens. Non-generic residues [BOUZ] mapped to X.
- **Embeddings**: last hidden layer of the Transformer attention stack used as per-residue features (no fine-tuning / gradient back-propagation to the LM).
- **Downstream heads**:
  - Per-residue: 2-layer CNN (compress to 32 dims, window size 7; multi-task 3-state + 8-state secondary structure).
  - Per-protein: mean-pooling over length → single FNN layer (32 neurons; multi-task localization + membrane classification).

## Data

| Dataset     | Proteins (M) | Amino acids (B) | Disk (GB) |
|-------------|--------------|------------------|-----------|
| UniRef50    | 45           | 14               | 26        |
| UniRef100   | 216          | 88               | 150       |
| BFD         | 2,122        | 393              | 572       |

- BFD merges UniProt + metagenomic sequences; ~8x larger than previous largest protein LM datasets; ~500x more tokens than Google's Billion Word corpus.
- Tokenization: single amino acid = single token; proteins separated by empty lines (document boundary for BERT/ALBERT next-sentence prediction).
- Downstream evaluation: NetSurfP-2.0 training set for secondary structure; DeepLoc dataset for localization/membrane. Novel non-redundant test set NEW364 introduced (<20% PIDE to training set).

## Training Recipe

| Config                     | ProtTXL-BFD | ProtTXL   | ProtBert (BFD/U100)  | ProtAlbert  | ProtXLNet   | ProtElectra | ProtT5-XL/XXL              |
|----------------------------|-------------|-----------|----------------------|-------------|-------------|-------------|-----------------------------|
| **Data**                   | BFD         | UniRef100 | BFD / UniRef100      | UniRef100   | UniRef100   | UniRef100   | BFD then UniRef50           |
| **Params**                 | 562M        | 40M       | 420M                 | 40M         | 420M        | 4M          | 3B / 11B                   |
| **Batch size (global)**    | 44K         | 22K       | 14.3K / 14.3K        | 10.7K       | 1K          | 9K / 3.5K   | varies                     |
| **Optimizer**              | LAMB        | LAMB      | LAMB                 | LAMB        | Adam        | LAMB        | AdaFactor (inv-sqrt-root LR) |
| **LR**                     | 0.0005      | 0.002     | 0.002                | 0.00001     | 0.002       | 0.002       | 0.01                       |
| **Training steps**         | 40.7K       | 31.3K     | 800K+200K / 300K+100K| 150K+100K   | 847K        | 400K+400K   | XL: 1.2M+991K; XXL: 920K+343K |
| **Warm-up**                | 13.6K       | 5.5K      | 140K+20K / 40K+10K   | 40K+5K      | 20K         | 40K+10K     | n/a                        |
| **System**                 | Summit      | Summit    | TPU Pod              | TPU Pod     | TPU Pod     | TPU Pod     | TPU Pod v3-256/512/1024    |
| **GPUs/TPUs**              | 5616        | 1024      | 512                  | 512         | 512         | 512         | 512-1024                   |
| **Precision**              | FP16 (Almost)| FP32    | FP32 (TPU)           | FP32 (TPU)  | FP32 (TPU)  | FP32 (TPU)  | FP32 (TPU); FP16 at inference |

- Multi-phase training for ProtBert/ProtAlbert/ProtElectra/ProtT5: first phase on shorter sequences (<=512), second phase on longer (<=1K-2K).
- ProtT5 uses BERT's denoising objective (15% single-token masking), not T5's span corruption.
- ProtT5 models pre-trained on BFD, then fine-tuned on UniRef50 (suffix "-U50").
- IBM Large Model Support (LMS) used for ProtTXL on Summit: increased model size by ~15.6%, batch size by 700%, reduced training time by 60% via NVLink CPU<->GPU shuttling.
- Horovod + IBM DDL backend for distributed training on Summit; native TPU Pod distribution for Google Cloud models.
- Near-linear scale-up across 936 Summit nodes (5616 GPUs); communication overhead constant after 2 nodes.

## Key Ablations & Design Choices

1. **Architecture comparison (6 architectures, same downstream evaluation)**:
   - ProtT5-XL-U50 (3B) achieves the best downstream performance across all tasks, outperforming even ProtT5-XXL (11B)—suggesting training longer is more important than scaling model size.
   - Auto-encoder models (BERT, ALBERT, T5) consistently outperform auto-regressive models (Transformer-XL, XLNet) on embedding quality.
   - ProtTXL (Transformer-XL) performs worst; falls below even the ELMo/LSTM baseline (DeepSeqVec).
   - ProtBert-BFD outperforms ProtBert (UniRef100), showing benefits of larger pretraining corpus.

2. **Database size effect**:
   - ProtTXL on BFD ~ ProtTXL on UniRef100 (10x smaller)—marginal gain for auto-regressive model.
   - ProtBert-BFD > ProtBert-UniRef100 by ~1% Q3—moderate gain for masked-LM.
   - More pretraining samples (steps x batch size) correlates with downstream performance (Spearman rho = 0.62).

3. **Training length vs. model size (ProtT5-XL vs. ProtT5-XXL)**:
   - ProtT5-XL-U50 (3B, more training steps) > ProtT5-XXL-U50 (11B, fewer steps) on all benchmarks.
   - Implies "seeing more samples during pretraining might be more beneficial than increasing model size."

4. **Encoder-only vs. encoder-decoder for T5**:
   - Encoder outperforms decoder on all benchmarks; decoder dropped at inference, halving effective model size.
   - FP16 inference has no effect on downstream performance but allows 12 GB GPU inference.

5. **Downstream head comparison (on ProtBERT-BFD embeddings)**:
   - CNN ~ LSTM > FNN > LogReg for per-residue secondary structure prediction.
   - CNNs preferred for computational efficiency.
   - Mean-pooling > concat > min/max for per-protein tasks.

6. **Scaling infrastructure**:
   - Summit (GPU + DDL): constant communication overhead from 2 to 936 nodes; DDL fastest backend vs. MPI/NCCL.
   - TPU Pod: no code changes needed for distribution; used V2 (256 cores), V3 (512/1024 cores).

7. **Embeddings capture biophysics without supervision**:
   - t-SNE of uncontextualized token embeddings recovers amino-acid charge, polarity, size, hydrophobicity, aliphatic vs. aromatic.
   - Per-protein pooled embeddings separate SCOPe structural classes, domains of life, membrane vs. soluble proteins.
   - Attention heads (ProtAlbert) focus on functionally critical residues (zinc-finger binding motif).
   - Random-initialized models do **not** capture these features -> signal is from training, not inductive bias.

## Reported Insights

- **First protein LM to match SOA without MSAs**: ProtT5-XL-U50 reaches Q3 = 81.4-84.8% on secondary structure, on par with NetSurfP-2.0 (82.0-84.3%) which requires MSAs. On 57% of proteins in NEW364, ProtT5-XL-U50 actually surpasses NetSurfP-2.0.
- **Biggest advantage for small families**: ProtT5-XL-U50 outperforms MSA-based methods most when Neff = 1 (proteins without any evolutionary relatives in the MSA). This is exactly where evolutionary information is weakest.
- **Per-protein tasks**: ProtT5-XL-U50 achieves Q10 = 81% (localization) and Q2 = 91% (membrane), exceeding the MSA-based DeepLoc SOA.
- **Inference speed**: Embedding the entire human proteome (20,353 proteins) takes minutes on a single GPU vs. hours for MSA construction with mmseqs2.
- **Scaling law hint**: Performance vs. number of pretraining samples follows a positive trend (rho = 0.62), though the authors note model-specific peculiarities complicate the picture.
- **No evidence of saturation**: Performance still improves with more training; the authors speculate larger/longer-trained models will continue to improve, and that future work should explore even larger Transformers and longer training.
- **Token vocabulary**: Unlike NLP, proteins use only 20 amino acids -> much smaller vocabulary, enabling larger batch sizes on the same hardware (e.g., ALBERT global batch 10,752 vs. 4,096 in NLP).

## References Worth Chasing

- **ESM-1b** (Rives et al. 2021, ref [72]): 650M-param Transformer protein LM; outperforms all ProtTrans non-T5 models on Q3; complementary scaling study.
- **AlphaFold2** (Jumper et al. 2021, ref [30]): structure prediction with MSA+ML at unprecedented accuracy; orders of magnitude more compute than embedding extraction.
- **LAMB optimizer** (You et al. 2019, ref [61]): critical for stable training with massive batch sizes (up to 44K); enabled efficient use of Summit GPUs.
- **DeepLoc** (Almagro Armenteros et al. 2017, ref [16]): SOA for subcellular localization using MSAs; baseline for per-protein benchmarks.
- **NetSurfP-2.0** (Klausen et al. 2019, ref [15]): SOA for secondary structure using evolutionary information; the ceiling ProtT5 matches/exceeds.
- **Light Attention (LA_ProtT5)** (Stark et al. 2021, ref [83]): Optimized localization prediction from ProtT5 embeddings; clearly surpasses DeepLoc without MSAs.

## Notes / Open Questions

- The paper reports model parameter counts that appear inconsistent in Table 2 (e.g., ProtBert listed as 420M in some places vs. 40M in others; ProtElectra listed as both 420M and 4M). The OCR of the PDF may have introduced errors. Cross-check with the GitHub repo for exact counts.
- No FLOPs estimates or GPU-hours are reported directly; training compute must be inferred from steps x batch size x hardware.
- The ProtT5 models use BERT-style single-token masking (15%), **not** T5's span-corruption objective—an important deviation from the original T5 paper.
- Decoder is dropped at inference for ProtT5, meaning the "11B" model is effectively ~5.5B at deployment. This is a practical and important detail for downstream users.
- Comparison to ESM-1b (650M params, single architecture) suggests that focused scaling of a single architecture may be competitive with the multi-architecture survey approach taken here.
- The correlation between number of training samples and downstream performance (rho = 0.62) anticipates later scaling-law work (Chinchilla, etc.) but is not formalized as a power law.
- All downstream evaluation uses frozen embeddings (no fine-tuning of the LM), which may underestimate the potential of smaller models.
- Year listed as 2020 (arXiv); published in IEEE TPAMI 2022.

## Verification (Rev 3)

Each claim below is quoted from `insights.md` with its line reference, then judged against the source paper.

1. **L23** — "ProtTrans showed training longer beats scaling wider (T5-XL-U50 3 B > T5-XXL 11 B)"
   **supported** — Paper states: "comparing the two largest models trained by us (ProtT5-XL and ProtT5-XXL) suggested that seeing more samples during pretraining might be more beneficial than increasing model size." Benchmark tables confirm T5-XL-U50 outperforms T5-XXL on all downstream tasks.

2. **L71** — "ProtTrans compared six architectures and found that tokenization interacts with model family — T5-XL-U50 on UniRef50 was optimal"
   **partial** — The paper does compare six architectures and T5-XL-U50 is the best-performing model. However, the claim that "tokenization interacts with model family" is unsupported: all models use identical single-amino-acid tokenization. The T5-XL-U50 advantage is attributed to training duration and dataset, not tokenization. Also, T5-XL-U50 was pre-trained on BFD then fine-tuned on UniRef50, not trained exclusively on UniRef50.

3. **L102** — "ProtTrans (up to 11 B T5-XXL) [prottrans-towards-cracking-the-2020] all use conventional encoder or encoder-decoder Transformers."
   **supported** — The paper describes six standard Transformer variants: encoder-only (BERT, ALBERT, Electra), auto-regressive (Transformer-XL, XLNet), and encoder-decoder (T5). All are conventional architectures adapted from NLP.

4. **L224** — "ProtTrans trained on up to 393 B tokens from BFD using 5,616 GPUs on Summit, the largest protein pretraining at the time"
   **partial** — 393B tokens from BFD is correct. However, 5,616 GPUs on Summit were used only for ProtTXL-BFD (936 nodes × 6 V100s). ProtBert-BFD used 128 Summit nodes (768 GPUs). Other models (including ProtT5) were trained on TPU Pods. The phrasing implies all models used 5,616 GPUs, but the abstract does describe the overall project as using "Summit supercomputer using 5616 GPUs and TPU Pod up-to 1024 cores." The "largest protein pretraining at the time" is supported: BFD was "about eight times larger than the largest data sets used previously for protein LMs."

5. **L285** — "ProtTrans demonstrated that extending training duration is more important than increasing model width — T5-XL-U50 (3 B, trained longer on UniRef50) outperformed T5-XXL (11 B, standard schedule) on secondary structure prediction"
   **partial** — The core finding (T5-XL-U50 > T5-XXL due to more training samples) is correct. However, "trained longer on UniRef50" is misleading. T5-XL-U50 had more total training steps overall (pre-trained on BFD, then fine-tuned on UniRef50); the advantage comes from more total samples seen during pretraining, not from longer UniRef50 training specifically.

6. **L299** — "ProtTrans showed T5-XL-U50 (3 B, trained longer) outperforms T5-XXL (11 B, standard schedule), and was the first PLM to match MSA-based secondary structure prediction without MSAs"
   **supported** — Paper abstract: "the transfer of the most informative embeddings (ProtT5) for the first time outperformed the state-of-the-art without using evolutionary information." The paper actually claims ProtT5 *outperformed* (not merely matched) SOA, making this claim slightly conservative. T5-XL-U50 > T5-XXL is confirmed across all benchmarks.

7. **L436–437** — "ProtTrans scaled to 11 B (T5-XXL) on 393 B tokens using 5,616 GPUs, finding that training duration matters more than model width (T5-XL-U50 3 B > T5-XXL 11 B). ProtTrans was first to match MSA-based secondary structure prediction without MSAs."
   **partial** — The 5,616 GPU figure applies to ProtTXL on Summit, not to T5-XXL (trained on TPU Pod v3-1024). The sentence structure "scaled to 11 B … using 5,616 GPUs" incorrectly implies T5-XXL used 5,616 GPUs. The training-duration-over-model-width conclusion and the first-to-match-MSA-SOA claim are both supported.

## Ablations (Rev 4)

| Variable | Settings | Metric / dataset | Result | Conclusion |
|---|---|---|---|---|
| Supervised head architecture (on frozen ProtBERT-BFD embeddings) | LogReg, FNN, CNN, LSTM | Q3 secondary structure on CASP12 / NEW364 | LogReg 74.3–79.3; CNN 76.1–81.1; LSTM 76.1–80.9 (SOM Table 7) | CNN ≈ LSTM > LogReg; CNN chosen (more compute-efficient). Architecture matters less than embeddings. |
| Pre-training corpus size | UniRef100 vs. BFD (10× larger); + UniRef50 fine-tune after BFD | Q3 on CASP12 / NEW364 (Table 3) | ProtBert: BFD +1.1% Q3; ProtTXL: BFD −0.6%; ProtT5-XL: BFD 77.5/82.0 → +U50 fine-tune 81.4/84.8 | Larger raw corpus alone gives marginal/inconsistent gains; **fine-tuning on cleaner UniRef50 after BFD is the decisive trick**. |
| LM architecture / objective | ProtTXL, ProtXLNet (auto-regressive); ProtBert, ProtAlbert, ProtElectra, ProtT5 (auto-encoding/seq2seq) | Q3 (CASP12/NEW364) and Q10/Q2 (DeepLoc) (Tables 3, 4) | Auto-encoders dominate: ProtBert 75.0/80.1, ProtT5-XL-U50 81.4/84.8; auto-regressive ProtTXL 71.5/72.8 | Auto-encoding (esp. T5 span corruption) > auto-regressive for protein representation learning. |
| Model size at fixed family (T5) | ProtT5-XL (~3B) vs. ProtT5-XXL (~11B), both BFD then U50 | Q3 NEW364; Q10/Q2 DeepLoc | XL-U50 81.4/84.8 vs. XXL-U50 79.2/83.3; Q10 81 vs 79; Q2 91 vs 89 | Scaling width beyond 3B hurts at fixed sample budget — **more training samples beats more parameters**. |
| Pre-training samples seen (steps × global batch) | Across all 6 LMs trained here | Q3 on NEW364 vs. samples-seen (Fig. 7) | Spearman ρ = 0.62 (positive) | Performance correlates with samples seen during pre-training; informal scaling trend. |
| Pooling strategy (per-protein) | min, max, mean, concat(min,max,mean) on ProtBert-BFD per-residue embeddings | Q10 localization, Q2 membrane on DeepLoc (Table 10) | min/max ≈ −14% Q10 and ≈ −3% Q2 vs mean/concat; mean beats concat by ~10% Q10 | **Mean-pooling is best** for per-protein tasks; min/max discard too much; concat hurts localization. |
| MSA depth sensitivity (Neff) | NEW364 split by Neff = 1, ≤10, >10; compare ProtT5-XL-U50 (no MSA) vs. NetSurfP-2.0 (MSA) | Q3 per Neff bin (Fig. 6) | ProtT5 advantage largest at Neff=1 (small families); near-parity at Neff>10 | Embedding-only models help most where evolutionary info is weakest. |
| Inference batch size × sequence length | bs ∈ {1,16,32}, len ∈ {128,256,512}, fp16, single Quadro RTX 8000 | Per-protein latency, all LMs (SOM Table 11) | ProtBert/Electra: 0.007 s/protein @ bs32; ProtT5-XL/Albert: 0.025 s; ProtT5-XL is 4–6× faster than MMseqs2 MSA, ProtBert 16–28× faster | Embedding inference is dramatically cheaper than MSA construction; throughput is bs/length-sensitive. |

**Design-choice take-aways from this paper's ablations:**
- **Samples > parameters**: at the 3–11B scale, additional pre-training samples (BFD → UniRef50 fine-tune) beat doubling/tripling width.
- **Auto-encoding objectives (BERT/T5) clearly outperform auto-regressive (TXL/XLNet)** for residue- and protein-level transfer.
- **Two-stage pre-training (large noisy BFD → clean UniRef50)** is the single largest performance lever observed.
- **Mean-pooling** is the right default for per-protein heads; min/max/concat are strictly worse.
- A **CNN head on frozen embeddings** is a sufficient and compute-efficient downstream architecture.
- Embedding-based models give the **biggest wins on small protein families (Neff≈1)** where MSAs fail.
