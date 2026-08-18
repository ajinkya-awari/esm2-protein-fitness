# ESM2 Protein Fitness Source Repository Design

**Status:** Approved for local implementation on 2026-08-18.

## Objective

Create a public-safe, source-only repository for the Project 15 ESM2 Protein mutation-fitness benchmark. The repository must be testable on an old, storage-constrained Windows computer while remaining portable to Kaggle and Colab for explicitly authorized data and GPU stages.

## Scope

The first implementation phase includes typed contracts, independent synthetic fixtures, mutation reconstruction, deterministic grouped-split utilities, lightweight metrics, structured resource skips, privacy checks, provenance records, and one automation entry point. It does not retrieve ProteinGym data or model checkpoints, install large binary payloads, or run CPU-heavy embedding, training, UMAP, or full evaluation jobs.

## Repository boundary

The planning/control-plane folder remains `15-esm2-protein`. This source repository is `esm2-protein-fitness/`, with Python imports under `src/esm2_fitness/`. The public remote is configured separately by the repository owner.

Only source code, configuration, tests, independently synthetic fixtures, sanitized documentation, and privacy-checked aggregate examples may be committed. The following are always restricted and ignored: raw or derived benchmark rows, sequences, embeddings, checkpoints, hidden predictions, caches, fitted artifacts, credentials, `.env` files, tracking payloads, and generated restricted reports.

## Scientific contracts

- The primary estimand is ProteinGym v1.3 single substitutions.
- UniProt IDs and deterministic sequence-similarity clusters are the grouping units; all observations for a group stay in one partition.
- The declared split settings are `min_seq_id=0.90` and coverage `0.80`.
- ESM1v parity means official five-checkpoint masked-marginal likelihood-ratio scoring.
- ESM2 features are pooled mutant-minus-WT representations from independent WT and mutant encodings.
- Frozen ESM2 is the CPU-capable comparison; LoRA is optional and T4-gated.
- Metrics are computed per assay before macro summaries, with counts, failures, runtimes, and group-aware uncertainty.
- UMAP is exploratory and never an acceptance criterion.

## Compute and network safety

The default command is offline and lightweight. It may parse local source, validate synthetic fixtures, compile the package, run contract tests, generate small manifests, and run privacy scans. It must not make network requests or create large files.

Real-data and model stages require explicit opt-in, an approved local data path or platform-provided asset, and a resource check. A stage that cannot run must emit a structured `skipped` record with a reason; it must not silently substitute another result. Full ESM2 embeddings, training, UMAP, large evaluation, ProteinGym acquisition, checkpoint acquisition, tracking transfer, publication, deployment, email, and repository synchronization are outside the default local command.

## Components

```text
src/esm2_fitness/
  pipeline.py       Lightweight command dispatcher and safety gates
  schema.py         Typed mutation/assay row contracts
  sequences.py      Substitution parsing and WT/mutant proof
  splits.py         Deterministic group-disjoint manifest utilities
  metrics.py        Assay-first metrics and structured missingness
  provenance.py     Revision and environment metadata contracts
  privacy.py        Public-artifact allow/deny checks
  status.py         Structured pass/fail/skipped result records
```

The modules have narrow boundaries. `pipeline.py` orchestrates but does not own scientific logic. `schema.py` rejects malformed rows before sequence or metric code. `sequences.py` proves the reference residue before changing exactly one position. `splits.py` accepts explicit group keys and emits deterministic partition assignments without acquiring a clustering tool. `metrics.py` keeps assay-level results separate from macro summaries. `privacy.py` operates on paths and artifact metadata, not restricted content. `status.py` gives optional compute stages a common result shape.

## Automation interface

The canonical interface is:

```text
python -m esm2_fitness.pipeline check
python -m esm2_fitness.pipeline synthetic
python -m esm2_fitness.pipeline real --data-dir <approved-local-path> --allow-external-data
```

`check` performs compile-safe, dependency-light validation. `synthetic` runs the independent fixture flow. `real` refuses to proceed unless its explicit flag and resource/data gates pass. PowerShell and Bash wrappers call the same Python interface and do not duplicate business logic. The wrappers must remain usable on Windows, Kaggle, and Colab.

## Verification

The offline suite verifies schema rejection, valid mutation parsing, WT mismatch rejection, exact single-residue reconstruction, deterministic group disjointness, metric handling for ties and missing predictions, structured LoRA skips, provenance shape, public-artifact rejection, and command safety. Verification must not require a network connection, a model checkpoint, ProteinGym, a GPU, or a large local data file.

## Commit policy

Each focused change is verified before commit and synchronized to the configured public remote only after the commit contains no restricted or generated artifacts. Planned commit boundaries are scaffold, contracts/fixtures, sequence logic, split logic, metrics/status, privacy/provenance, automation, and handoff documentation. A failed check stops the sequence; it is recorded rather than bypassed.

## Non-goals

This design does not establish biological mechanism, clinical utility, experimental causality, commercial readiness, or model superiority. It does not authorize data/model retrieval, tracking, publication, deployment, patient-data processing, or any transfer other than source-only repository commits explicitly authorized by the owner.

## Acceptance criteria

- The repository has a clear source-only public boundary and ignores restricted artifacts.
- The default commands are offline and lightweight.
- Synthetic contract tests run without ProteinGym, checkpoints, GPU, or network access.
- Optional stages fail closed and produce structured `skipped` records when gates are unavailable.
- Source and documentation use the declared scientific contracts without invented results.
- Every public commit is verified and contains no restricted artifacts or secrets.
