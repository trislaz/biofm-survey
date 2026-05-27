# PR #10 — PerturbDiff insight update

Pull request (PR): [#10](https://github.com/trislaz/biofm-survey/pull/10)

## Question

Does adding [PerturbDiff: Functional Diffusion for Single-Cell Perturbation Modeling](https://arxiv.org/abs/2602.19685) change any of the insights in `insights.md`?

## Answer

Yes, but narrowly. PerturbDiff does **not** overturn the existing single-cell RNA sequencing (scRNA-seq) practitioner default: Geneformer or scGPT for representation learning, strong single-cell variational inference (scVI)-style baselines, and careful fair-baseline reruns remain the main recommendation. It also does not yet justify changing Rev 5 evidence counts, because the current survey note is based on the abstract and public repository rather than a full extracted ablation table with numeric metrics.

It does add one qualitative insight to the single-cell perturbation recipe: for virtual-cell perturbation modeling, the target response may be one-to-many. PerturbDiff frames unpaired control-to-perturbed prediction as **distribution-level diffusion** over cell-population response distributions, rather than a deterministic cell-level mapping conditioned only on observed cell type and perturbation. This is relevant when latent factors such as microenvironment or batch effects create multiple plausible response distributions under the same observed condition.

The inline `insights.md` update therefore records PerturbDiff as a tracked caveat/extension for virtual-cell perturbation response simulation, not as a replacement for the existing representation-learning default or as a new counted Rev 5 ablation-backed evidence item.

## Sources

- PR discussion: [#10](https://github.com/trislaz/biofm-survey/pull/10)
- Paper: [PerturbDiff: Functional Diffusion for Single-Cell Perturbation Modeling](https://arxiv.org/abs/2602.19685) ([note](../notes/perturbdiff-functional-diffusion-for-2026.md))
- Project/code: [DeepGraphLearning/PerturbDiff](https://github.com/DeepGraphLearning/PerturbDiff)
