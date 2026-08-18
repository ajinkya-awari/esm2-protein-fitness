# ESM2 Protein Mutation-Fitness Benchmark

Project 15 is an auditable, leakage-aware benchmark comparing simple baselines with frozen ESM1v and ESM2 representations on ProteinGym single-substitution assays. It is a research reproducibility artifact, not a clinical, experimental, commercial, or causal claim.

## Safe default

The local default is intentionally small and offline:

```text
python -m pytest -q
python -m esm2_fitness.pipeline check
python -m esm2_fitness.pipeline synthetic
```

On Windows, use `./run.ps1 check` or `./run.ps1 synthetic`. On Bash-based environments, use `./run.sh check` or `./run.sh synthetic`. These wrappers set the source path and select the available Python executable; they do not install packages or retrieve assets.

These commands use independent synthetic fixtures and do not retrieve datasets or model checkpoints. They do not run full embeddings, training, UMAP, or large evaluations.

## Source layout

- `src/esm2_fitness/`: typed contracts and lightweight orchestration.
- `tests/`: deterministic offline tests.
- `configs/`: protocol declarations.
- `data_public/`: independent synthetic fixtures only.
- `artifacts_restricted/`: local-only restricted outputs; ignored by Git.
- `results_public/`: privacy-checked aggregate summaries only.
- `docs/`: protocol, compute gates, plans, and handoff records.

Real-data and model stages are separate gates for Kaggle or Colab. They require explicit opt-in, approved platform-provided assets, and resource checks. An unavailable optional stage is recorded as `skipped`, never silently replaced.

See `docs/PROTOCOL.md`, `docs/COMPUTE_GATES.md`, and `docs/HANDOFF.md` for the scientific contracts, resource boundaries, and current verification state.
