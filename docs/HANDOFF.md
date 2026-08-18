# Project 15 Handoff

## Current state

The source repository contains the lightweight schema, sequence, grouped-split, metric, status, provenance, privacy, pipeline, wrapper, and synthetic end-to-end contracts. No ProteinGym data, model checkpoint, embedding, hidden prediction, cache, fitted artifact, or large generated file was created.

## Files in scope

- `src/esm2_fitness/`: implementation modules.
- `tests/`: offline contract and integration tests.
- `data_public/synthetic_mutations.jsonl`: five independently synthetic rows.
- `configs/synthetic_protocol.yaml`: declared synthetic protocol settings.
- `run.ps1`, `run.sh`, `Makefile`: thin automation wrappers.
- `docs/`: protocol, compute gates, design, plan, and this handoff.

## Verification record

Environment: Python 3.11.9, pytest 9.0.3.

- `python -m compileall src tests`: exit 0; source and tests listed successfully.
- `python -m pytest -q`: exit 0; `69 passed in 6.98s`.
- `PYTHONPATH=src python -m esm2_fitness.pipeline check`: exit 0; `offline lightweight checks available`.
- `PYTHONPATH=src python -m esm2_fitness.pipeline synthetic`: exit 0; `synthetic offline flow validated 5 rows`.
- `./run.ps1 check`: exit 0; `offline lightweight checks available`.
- `bash -n -- run.sh`: exit 0.
- `bash run.sh check`: exit 0; `offline lightweight checks available`.
- `PYTHONPATH=src python -m esm2_fitness.pipeline gates`: exit 0; ESM1v, ESM2, and LoRA each reported structured `skipped`.
- `git diff --check`: exit 0; only the expected Windows LF-to-CRLF warning was emitted.
- Restricted-name scan: no tracked restricted payloads; the only working-tree match is the intentionally ignored empty `artifacts_restricted/.gitkeep` placeholder.

The local Python interpreter is 3.11.9 and pytest is 9.0.3. A Bash wrapper regression was fixed by selecting `python` or `python3` according to host availability. No network, dataset retrieval, checkpoint retrieval, heavy CPU stage, GPU stage, or large generated artifact was used.

## Skipped gates

- ProteinGym acquisition: not run; no local retrieval is authorized.
- ESM1v actual parity: not run; no checkpoints are present. The offline five-checkpoint contract is tested.
- Frozen ESM2 actual embeddings: not run; no checkpoint or heavy CPU work is present. The offline shape/delta contract is tested.
- LoRA: skipped; no T4 session is active.
- W&B/Hugging Face transfer, publication, deployment, email, and patient-data handling: not run.
- Remote synchronization: completed by the repository owner; `origin/main` matches local commit `ba354c2f35058b8de12876d7984aecb0c7a7f6c5`.

## Model-gate phase

- Offline ESM1v contract: ordered official five-checkpoint validation, masked-marginal subtraction, and injected-provider parity harness.
- Offline ESM2 contract: finite equal-shape WT/mutant validation and pooled mutant-minus-WT delta.
- Offline LoRA resource gate: T4 availability, VRAM, target modules, and output shape; failures remain structured `skipped`.
- `pipeline gates` reports all three decisions without importing model libraries or accessing the network.

## Remaining authorized work

- Run official ESM1v parity on Kaggle/Colab with approved checkpoints.
- Run frozen ESM2 smoke/representation checks on Kaggle/Colab with approved model assets.
- Run LoRA only after T4, memory, module, output-shape, and reproducibility gates pass.
- Acquire or process ProteinGym only in the approved platform workflow, then record provenance, metrics, privacy checks, and skips.

## Next authorized action

Use Kaggle or Colab for the explicitly authorized ESM1v, frozen ESM2, and optional T4 LoRA gates without changing the local offline default.
