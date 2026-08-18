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
- `python -m pytest -q`: exit 0; `55 passed in 0.80s`.
- `PYTHONPATH=src python -m esm2_fitness.pipeline check`: exit 0; `offline lightweight checks available`.
- `PYTHONPATH=src python -m esm2_fitness.pipeline synthetic`: exit 0; `synthetic offline flow validated 5 rows`.
- `./run.ps1 check`: exit 0; `offline lightweight checks available`.
- `bash -n -- run.sh`: exit 0.
- `bash run.sh check`: exit 0; `offline lightweight checks available`.
- `git diff --check`: exit 0; only the expected Windows LF-to-CRLF warning was emitted.
- Restricted-name scan: no tracked restricted payloads; the only working-tree match is the intentionally ignored empty `artifacts_restricted/.gitkeep` placeholder.

The local Python interpreter is 3.11.9 and pytest is 9.0.3. A Bash wrapper regression was fixed by selecting `python` or `python3` according to host availability. No network, dataset retrieval, checkpoint retrieval, heavy CPU stage, GPU stage, or large generated artifact was used.

## Skipped gates

- ProteinGym acquisition: not run; no local retrieval is authorized.
- ESM1v parity: not run; no checkpoints are present.
- Frozen ESM2 embeddings: not run; no checkpoint or heavy CPU work is present.
- LoRA: skipped; no T4 session is active.
- W&B/Hugging Face transfer, publication, deployment, email, and patient-data handling: not run.
- Remote synchronization: completed by the repository owner; `origin/main` matches local commit `ba354c2f35058b8de12876d7984aecb0c7a7f6c5`.

## Next authorized action

Resolve the host safety-hook authorization for the configured public remote, then synchronize the already verified source-only commits. Before any Kaggle or Colab run, add an approved platform runner and record its resource, data, model, and privacy gates without changing the local default.
