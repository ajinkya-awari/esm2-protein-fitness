# Compute and Network Gates

## Local PC

Allowed local work is lightweight schema, sequence, split, metric, provenance, privacy, compile, and synthetic-fixture verification. The default commands do not retrieve data or checkpoints and do not run full ESM2 embedding, training, UMAP, or large evaluation.

## Kaggle or Colab

Real-data and model stages belong on an explicitly approved Kaggle or Colab session with platform-provided assets. A runner must verify the data path, model revision, GPU/resource class, target modules, output shape, runtime, and memory before optional LoRA. It must write `skipped` when a gate is unavailable or fails.

## Transfer and release

Tracking transfer, model/data hosting, publication, deployment, email, and patient-data handling are separate approvals. A public repository commit may contain source and safe documentation only. The privacy checker must pass before any aggregate result enters `results_public/`.
