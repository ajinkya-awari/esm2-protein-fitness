# Compute and Network Gates

## Local PC

Allowed local work is lightweight schema, sequence, split, metric, provenance, privacy, compile, and synthetic-fixture verification. The default commands do not retrieve data or checkpoints and do not run full ESM2 embedding, training, UMAP, or large evaluation.

`python -m esm2_fitness.pipeline gates` performs only a decision report. It emits ESM1v checkpoint, frozen ESM2 asset, and LoRA T4 statuses without importing model libraries or accessing the network.

## Kaggle or Colab

Real-data and model stages belong on an explicitly approved Kaggle or Colab session with platform-provided assets. A runner must verify the data path, model revision, GPU/resource class, target modules, output shape, runtime, and memory before optional LoRA. It must write `skipped` when a gate is unavailable or fails.

## Transfer and release

Tracking transfer, model/data hosting, publication, deployment, email, and patient-data handling are separate approvals. A public repository commit may contain source and safe documentation only. The privacy checker must pass before any aggregate result enters `results_public/`.

## Next-session checklist

1. Synchronize the pending local commit before using the source remotely.
2. Confirm Kaggle/Colab asset paths and exact model revisions.
3. Run the model-gate report and preserve every `skipped` or `failed` result.
4. Keep restricted artifacts on the approved platform.
