# Compute and Network Gates

## Local PC

Allowed local work is lightweight schema, sequence, split, metric, provenance, privacy, compile, and synthetic-fixture verification. The default commands do not retrieve data or checkpoints and do not run full ESM2 embedding, training, UMAP, or large evaluation.

`python -m esm2_fitness.pipeline gates` performs only a decision report. It emits ESM1v checkpoint, frozen ESM2 asset, and LoRA T4 statuses without importing model libraries or accessing the network.

## Kaggle or Colab

Real-data and model stages belong on an explicitly approved Kaggle or Colab session with platform-provided assets. A runner must verify the data path, model revision, GPU/resource class, target modules, output shape, runtime, and memory before optional LoRA. It must write `skipped` when a gate is unavailable or fails.

## Transfer and release

Tracking transfer, model/data hosting, publication, deployment, email, and patient-data handling are separate approvals. A public repository commit may contain source and safe documentation only. The privacy checker must pass before any aggregate result enters `results_public/`.

## Next-session checklist

Current next task (2026-08-30): run the notebook through cells 1–8 and stop at the approval gate.

1. Review `notebooks/KAGGLE_RUNBOOK_esm2_protein.md`.
2. Run `notebooks/kaggle_esm2_protein.ipynb` cells 1-8 in order.
3. Stop at the approval gate unless explicit model/data/GPU approval is recorded.
4. Preserve every `skipped` or `failed` result and keep restricted artifacts on the approved platform.
