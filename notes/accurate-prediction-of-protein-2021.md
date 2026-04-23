---
id: accurate-prediction-of-protein-2021
title: Accurate prediction of protein structures and interactions using a three-track
  neural network
authors: []
year: 2021
venue: Science
arxiv: null
doi: 10.1126/science.abj8754
url: null
pdf_path: null
md_path: /home/t-tlazard/projects/maira-report-gen/survey-bio-fm/papers/md/accurate-prediction-of-protein-2021.md
modalities:
- protein-structure
status: extracted
evidence_quality: full-text
tags:
- protein-structure-prediction
- three-track-network
- SE3-equivariant
- attention
- protein-protein-complex
- MSA
- end-to-end
parameters: null
training_tokens: null
training_compute: null
references_chased: false
added_at: null
updated_at: null
is_fm: true
fm_classification_reason: 'RoseTTAFold: pretrained 3-track network for protein structure,
  widely transferred.'
---

## TL;DR

RoseTTAFold is a three-track neural network that simultaneously processes information at the 1D (sequence/MSA), 2D (distance map), and 3D (atomic coordinates) levels for protein structure prediction. It approaches AlphaFold2 accuracy on CASP14, enables rapid X-ray crystallography and cryo-EM structure solutions, and can predict protein-protein complex structures directly from paired sequence alignments—without separate docking. Inference takes ~10 min on a single RTX 2080 GPU for proteins <400 residues.

## Model

- **Architecture**: Three-track network with parallel information flow between 1D (MSA/sequence), 2D (residue-residue distance/orientation maps), and 3D (backbone Cα coordinates) tracks.
- **1D track**: Operates on multiple sequence alignments; attention-based.
- **2D track**: Residue-residue distance and orientation maps; attention replaces 2D convolution (cf. trRosetta).
- **3D track**: SE(3)-equivariant transformer layers operating on backbone coordinates; information flows back into 1D and 2D tracks (unlike AlphaFold2 where 3D reasoning happens only at the end).
- **Two inference modes**:
  1. *pyRosetta version*: Network outputs distance/orientation distributions → pyRosetta generates all-atom models. Lower GPU memory (8 GB for >400-residue proteins). 5 min GPU + ~1 h CPU (15 cores).
  2. *End-to-end version*: Averaged 1D+2D features → final SE(3)-equivariant layer → direct backbone coordinates. Requires 24 GB GPU. ~10 min on RTX 2080 for <400-residue proteins.
- **Crop strategy**: Due to memory limits, training/inference uses discontinuous crops of two segments totalling 260 residues; predictions from multiple crops are combined and averaged.
- **Parameters**: "Many millions" (exact count not stated in the paper).
- **Accuracy prediction**: Per-residue accuracy estimates (lDDT) produced alongside structure; DeepAccNet used for model quality assessment.

## Data

- **Training set**: Known protein structures from the PDB (monomeric proteins only; no complex data used for training).
- **Input features**: Multiple sequence alignments (MSAs), up to top 1,000 sequences (memory-limited); optional structural templates from PDB.
- **MSA construction**: HHblits/HHsearch against UniRef/BFD databases (sequence + template search ~1.5 h).
- **Complex prediction data**: Paired sequence alignments from known complexes used for evaluation only (not training).
- **CAMEO evaluation**: 69 medium and hard targets (May 15 – June 19, 2021).

## Training Recipe

- **Objective**: End-to-end learning from amino acid sequence to 3D coordinates; all network parameters optimised via backpropagation from final 3D structure through all layers.
- **Loss**: Combination of distance/orientation distribution losses (2D track) and coordinate-level losses (3D track). Exact loss formulation not fully detailed in the main text.
- **Crop size**: Two discontinuous segments spanning 260 residues total (due to GPU memory constraints).
- **Hardware**: Training limited by GPU memory; the authors note that hardware limitations constrained model size and prevented training on full-length large proteins.
- **Training data split**: Standard PDB-based splits; details in Methods/Supplementary.
- **Iterative refinement explored**: Feeding predicted structures back as templates + random MSA subsampling to generate model ensembles (improved diversity but accuracy predictor could not reliably select the best models).

## Key Ablations & Design Choices (quantitative)

| Design choice | Result |
|---|---|
| 3-track vs 2-track (attention) | 3-track clearly outperforms 2-track on CASP14 (Fig. 1B); both use identical training sets |
| 3-track vs trRosetta | Substantially better; also lower correlation between MSA depth and accuracy |
| RoseTTAFold vs AlphaFold2 on CASP14 | Still below AlphaFold2, attributed to hardware/model-size limits and inference differences |
| pyRosetta version vs end-to-end | pyRosetta version more accurate (incorporates side-chain info at relaxation stage); end-to-end limited by memory/no side chains |
| Discontinuous crops vs whole-protein prediction | Crops yield more accurate structures (fig. S4A); hypothesised to select more relevant MSA sequences per region |
| Perceiver cross-attention for large MSAs | Enables using >10k sequences instead of top 1,000; initial results promising (fig. S4D) |
| RoseTTAFold on CAMEO (May–Jun 2021) | Outperformed all other servers: Robetta, IntFold6-TS, BestSingleTemplate, SWISS-MODEL on 69 medium/hard targets |
| Complex prediction (2-chain) | Many TM-score > 0.8 on known complexes; accuracy correlates with number of paired sequences |
| Complex prediction (3- and 4-chain) | Demonstrated on IL-12R/IL-12 4-chain complex; fits cryo-EM density well |
| Molecular replacement success | Solved 4 X-ray structures that trRosetta models could not solve |
| Predicted lDDT > 0.8 → accuracy | Corresponds to average Cα-RMSD of 2.6 Å on CASP14 targets |

## Reported Insights

- Simultaneously reasoning across MSA, distance-map, and coordinate representations extracts sequence–structure relationships more effectively than reasoning over only MSA + distance maps.
- The 3-track architecture makes protein-protein complex prediction "almost by construction" via flexible-backbone docking, since chains are predicted in context of each other.
- Network trained only on monomers generalises to complexes without complex-specific training.
- Discontinuous cropping acts as implicit attention over the MSA, selecting the most relevant sequences per structural region.
- Hardware (GPU memory) is the primary bottleneck preventing larger models and end-to-end training on full-length proteins; the authors expect end-to-end to match or exceed pyRosetta version once hardware improves.
- Structure predictions enable functional insights: e.g., TANGO2 adopts Ntn-hydrolase fold (suggests enzymatic function), ADAM33 prodomain has lipocalin-like β-barrel fold (consistent with cysteine-switch metalloprotease inhibition), CERS1 reveals 6 TMH arrangement with active-site crevice.

## References Worth Chasing (≤15 bio-FM refs)

1. **AlphaFold (Senior et al., 2020)** – Predecessor; first deep-learning breakthrough in structure prediction (ref 1).
2. **AlphaFold2 (Jumper et al., 2021)** – State-of-the-art at CASP14; two-track + SE(3) end-to-end (ref 2).
3. **trRosetta (Yang et al., 2020)** – Direct predecessor from Baker lab; 2D-convolution-based distance/orientation prediction (ref 3).
4. **SE(3)-Transformers (Fuchs et al., 2020)** – Equivariant architecture used in the 3D track (ref 6).
5. **CAMEO (Haas et al., 2018)** – Continuous blind evaluation benchmark (ref 7).
6. **DeepAccNet (Hiranuma et al., 2021)** – Per-residue accuracy estimator used to weight MR models (ref 12).
7. **HHsearch (Söding, 2005)** – Sequence search for templates and MSA construction (ref 13).
8. **Perceiver (Jaegle et al., 2021)** – Cross-attention architecture explored for handling large MSAs (ref 11).
9. **pyRosetta (Chaudhury et al., 2010)** – All-atom structure generation from predicted distance/orientation distributions (ref 5).
10. **Cong et al., 2019** – Paired MSA / co-evolution for protein-protein interactions (ref 32).

## Notes / Open Questions

- Exact parameter count is never stated; "many millions" is the only characterisation. Supplementary / code might provide this.
- Training compute budget (GPU-hours, hardware) not reported beyond qualitative "memory-limited" statements.
- The paper does not detail the training loss formulation in the main text; Methods/Supplementary may contain this.
- End-to-end version under-performs pyRosetta version at publication time—has this gap been closed in later RoseTTAFold iterations (e.g., RoseTTAFold2, RF-diffusion)?
- Complex prediction was zero-shot (monomer-only training)—performance ceiling with complex-specific fine-tuning is unexplored here.
- Perceiver-based MSA handling was only preliminarily tested; unclear if it was adopted in later versions.
- The iterative-refinement strategy (feeding predictions back as templates) showed promise but the accuracy predictor could not select the best models—model-selection remains an open problem.

## Verification (Rev 3)

Each claim citing `[accurate-prediction-of-protein-2021]` in `insights.md` is checked against the full PMC text.

| # | insights.md line | Claim (paraphrased) | Verdict | Evidence / Notes |
|---|---|---|---|---|
| 1 | 15 | Structure prediction requires specialised blocks; RoseTTAFold uses a three-track network. | **supported** | Paper abstract and §Network architecture: "best performance with a 3-track network in which information at the 1D sequence level, the 2D distance map level, and the 3D coordinate level is successively transformed and integrated." |
| 2 | 124 | RoseTTAFold uses a three-track (1D/2D/3D) architecture with SE(3)-equivariant layers, enabling complex prediction from monomer inputs alone. | **supported** | "augmented with a third parallel structure track … SE(3)-equivariant Transformer network"; "The network was trained on monomeric proteins, not complexes" yet predicts protein-protein complexes (§Direct generation). |
| 3 | 255 | RoseTTAFold's three-track architecture is itself a multi-modal fusion strategy, passing information between sequence, pairwise distance, and 3D coordinate representations at every block. | **supported** | "information flows back and forth between the 1D … 2D … and the 3D coordinates, allowing the network to collectively reason about relationships within and between sequences, distances, and coordinates." The parallel flow is described as continuous; Fig 1A shows inter-track connections at each layer. |
| 4 | 325 | MSA-based methods (AF2, RoseTTAFold) achieve the highest accuracy but require expensive database searches. | **supported** | RoseTTAFold uses MSAs as input; "sequence and template search (~1.5 hours)"; "structure predictions with accuracies approaching those of DeepMind in CASP14." The 0.96 Å RMSD figure is attributed to AF2's own citation, not this paper—correct usage. |
| 5 | 468–469 | RoseTTAFold introduced the three-track architecture with SE(3)-equivariant layers; 3D track enables complex prediction from monomer training alone; discontinuous cropping improves accuracy. | **supported** | All three sub-claims directly stated: three-track + SE(3) (§Architecture); monomer-only training → complex prediction (§Direct generation); "combining predictions from multiple discontinuous crops generated more accurate structures than predicting the entire structure at once (fig. S4A)" (§Architecture). |
| 6 | 587 | RoseTTAFold's 3D-track cross-prediction is early evidence of cross-modal transfer (DNA ↔ protein). | **partial** | The paper demonstrates cross-representation transfer (1D/2D/3D tracks) and cross-task generalisation (monomer → complex), but does **not** address DNA↔protein cross-modal transfer, which is the question posed by the surrounding insight context. Citing RoseTTAFold as evidence for genomic-LM-to-protein transfer overstates the paper's scope. |

**Summary**: 5 of 6 citations fully supported; 1 partial (line 587 stretches the paper's scope to a cross-modal transfer question it does not address).

## Ablations (Rev 4)

The paper reports few formal ablations in the main text — most architecture-variant comparisons are deferred to table S1. Comparisons summarised below are those discussed in the main body.

| # | Ablation / Comparison | Setup | Result | Take-away |
|---|---|---|---|---|
| 1 | 3-track vs 2-track attention (Fig. 1B, CASP14) | Same attention backbone, with vs without the parallel 3D-coordinate track | 3-track "clearly outperforming … our 2-track attention models" and top CASP14 servers | The 3D-coordinate track is the central architectural contribution; tighter coupling of seq/dist/coords beats 2-track. |
| 2 | End-to-end (SE(3) layer) vs pyRosetta back-end (Fig. 1B) | Same 3-track features, final 3D either from SE(3)-equivariant layer or pyRosetta folding | pyRosetta version more accurate on CASP14 | End-to-end is limited by GPU memory and lack of side-chain info at training; gap expected to close with more compute / side chains. |
| 3 | Discontinuous crops vs whole-protein inference (fig. S4A) | Averaging 1D/2D features over multiple discontinuous 260-residue crops vs single-pass on full sequence | Crop-averaging more accurate | Memory-driven cropping is not just a workaround — it improves accuracy via implicit ensembling. |
| 4 | MSA-depth sensitivity (fig. S2) | Accuracy vs Neff for RoseTTAFold, AF2, trRosetta, CASP14 methods | RoseTTAFold and AF2 show weaker accuracy↔MSA-depth correlation than trRosetta | Attention + multi-track architectures reduce reliance on deep MSAs (mirrors AF2 behaviour). |
| 5 | Paired-MSA depth for complexes (fig. S10) | Vary number of paired sequences for complex prediction | More paired sequences → more accurate complex structures | Inter-chain co-evolution signal drives complex accuracy; the network exploits it despite monomer-only training. |
| 6 | RoseTTAFold vs trRosetta for molecular replacement | 4 unsolved crystallographic datasets, MR with each model set | RoseTTAFold solved all 4; trRosetta yielded no MR solutions | The accuracy gain over the prior best non-AF2 method is large enough to cross the practical MR threshold. |
| 7 | RoseTTAFold vs distant-homology model (TANGO2, fig. S9 / table S3) | Same target, RoseTTAFold model vs <15% identity homology model | Homology model has alignment shifts misplacing key conserved residues | Useful where templates exist but are too distant for sequence-based modelling. |
| 8 | Architecture-variant sweep (table S1, methods only) | "Wide variety of approaches for passing information between different parts of the networks" | Best variant = 3-track with attention at 1D/2D/3D and bidirectional inter-track flow | Cited but not detailed in the main text — full numbers live in supplementary table S1. |

**Count**: 8 ablation/comparison points discussed in the main text.

**Top take-away**: The decisive architectural choice is the **third (3D-coordinate) track with bidirectional information flow across 1D/2D/3D representations** (Ablation #1). Every other reported comparison — back-end choice, cropping, MSA depth, MR success, complex prediction — is downstream of, or enabled by, this multi-track design.
