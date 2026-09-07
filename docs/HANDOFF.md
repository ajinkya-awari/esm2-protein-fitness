START HERE  CONTINUE PENDING TASK

## Audit and reconciliation — 2026-08-30

- **Current status:** `PARTIAL`, 62% portfolio readiness, medium confidence; external/runtime stages remain `BLOCKED` pending approval.
- **Exactly one next task:** run `notebooks/kaggle_esm2_protein.ipynb` cells 1–8 in an approved Kaggle/Colab session, record sanitized evidence, and stop at the approval gate.
- **Evidence distinction:** the 87-test and lightweight-command results below are dated 2026-08-28 records. This audit did not rerun Python, pytest, or runtime work.
- **Current Git:** `HEAD=5c16ef3a290ed5d3c343e6f8bc035b6dbb470503`, `origin/main=05deb53224c30392ebcc38378b47c4289bde7dbe`, 2 ahead/0 behind, with pre-existing modified/untracked files. No synchronization was performed.
- **Not verified:** real data/model stages, real metrics, grouped bootstrap, LoRA, provider/platform work, release, deployment, or publication.

## Current continuation - 2026-08-28

1. Status and readiness: `PARTIAL`, 62%; portfolio readiness, not a scientific metric.
2. Complete: offline schema, sequence, split, metric, status, provenance, privacy, pipeline, model-gate, task, evaluator, adapter, checksum, and explainability contracts.
3. Fresh verification: compile exit 0; `python -m pytest -q` exit 0 with 87 passed; `check`, `synthetic`, `gates`, and `./run.ps1 gates` exit 0.
4. Historical only: earlier 69-test records and any real benchmark or optional model evidence.
5. Must not be claimed: real benchmark performance, model parity, optional tuning benefit, biological validity, or release.
6. Blockers: data/model approval, platform runtime, optional T4 work, repository synchronization, and release review.
7. Single next task: run the Kaggle notebook through cells 1-8 and stop at the approval gate.
8. Exact files: `notebooks/`, `src/esm2_fitness/`, `tests/`, `configs/`, wrappers, and this `docs/` handoff.
9. Pause note: user will continue tomorrow, August 29, 2026.

## Portfolio audit continuation - 2026-08-26

1. Status and readiness: `PARTIAL`, 50%; portfolio readiness, not a scientific metric.
2. Complete: offline schema/sequence/split/metric/status/provenance/privacy/pipeline contracts and synthetic fixtures are authored.
3. Verified and when: historical compile, 69-test, wrapper, and synthetic records; no current runtime run here.
4. Historical only: test counts, model gates, ProteinGym behavior, metrics, and any LoRA result.
5. Must not be claimed: ESM/ProteinGym performance, model parity, LoRA benefit, biological validity, or release.
6. Blockers: model/data access, ProteinGym rights, Kaggle/T4, optional LoRA, remote sync, and release review.
7. Single next task: verify the bounded runtime scaffold and model-gate manifest on the approved remote platform.
8. Exact files: `src/esm2_fitness/`, `tests/`, `configs/`, wrappers, and this `docs/` handoff.
9. Local-safe actions: static source/manifest review only; do not run Python, tests, downloads, or GPU work here.
10. Approval-required actions: Kaggle/Colab, ESM/ProteinGym downloads, GPU/LoRA, W&B/HF, publication, email, or Git push.
11. External sequence: synchronize reviewed source, run model-gate report, run ESM1v/ESM2 smoke, then optional LoRA; stop after skips/failures.
12. Expected output: dated sanitized gate report with revisions, hashes, versions, seed, device, structured skips, and paths.
13. Stop conditions: missing rights/checksum, failed shape/parity/privacy gate, unavailable T4, or raw sequence leakage.
14. Evidence path: `docs/` evidence records and future remote `evidence/<date>/` output.
15. Paste back: gate report path, sanitized output, source revision, device, and all skipped stages.

Current portfolio status: BLOCKED, 70% readiness, High confidence. Offline source contracts and historical test evidence are not current runtime proof. The single next task is a bounded remote model gate after explicit model/data approval. Local-safe actions are documentation, static scans, and diff review only; do not download models/data, train, or run GPU work on the laptop. Expected remote output is a dated sanitized evidence record; stop on any rights, checksum, schema, or model-gate failure. Preserve historical evidence and paste the evidence path and sanitized summary into the next session.

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
- Remote synchronization: last remote commit is `05deb53224c30392ebcc38378b47c4289bde7dbe`; local model-gate commit `b4adc7d64165738b71cd56efc090b2f82016186c` is ahead by one and must be synchronized before the next session.

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

Run `notebooks/kaggle_esm2_protein.ipynb` through cells 1-8 and stop at the approval gate.

## Next-session checklist

1. Review `notebooks/KAGGLE_RUNBOOK_esm2_protein.md`.
2. Open Kaggle or Colab with only the source tree available first.
3. Run notebook cells 1-8 for environment, source-copy, synthetic validation, and evidence inspection.
4. Stop at the approval gate.
5. Record revisions, skips, privacy results, and the next handoff.

## Local reconciliation - 2026-08-28

- Added `src/esm2_fitness/contracts.py`, `checksums.py`, and `explainability.py`.
- Added tests for task/evaluator/model contracts, checksum manifests, explainability boundaries, notebook structure, and the PowerShell `gates` wrapper.
- Added `notebooks/kaggle_esm2_protein.ipynb` and `notebooks/KAGGLE_RUNBOOK_esm2_protein.md`.
- Updated `run.ps1` and `Makefile` so the existing `gates` command is reachable through wrappers.
- Fresh checks: `python -m compileall src tests` exit 0; `python -m pytest -q` exit 0 with 87 passed; `python -m esm2_fitness.pipeline check` exit 0; `python -m esm2_fitness.pipeline synthetic` exit 0; `python -m esm2_fitness.pipeline gates` exit 0 with ESM1v, ESM2, and LoRA structured skips.
- No real ProteinGym rows, sequences, embeddings, checkpoints, hidden predictions, caches, fitted artifacts, provider calls, GPU work, or large generated files were used.
- Next source action: run the Kaggle notebook through the approval gate and preserve sanitized evidence.
