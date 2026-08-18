# ESM2 Protein Fitness Source Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or superpowers:subagent-driven-development to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Build a public-safe, lightweight Project 15 source repository whose default checks run offline on an old PC and whose data/model stages are explicitly gated for Kaggle or Colab.

**Architecture:** Keep scientific contracts in small modules under `src/esm2_fitness/`. Use independent synthetic fixtures for all local tests. Make `pipeline.py` the single orchestration entry point, with PowerShell and Bash wrappers that delegate to it. Keep restricted artifacts outside Git and make optional resource stages return structured `skipped` records.

**Tech Stack:** Python 3.12-compatible standard library first; pytest for tests; optional scientific dependencies declared without automatic installation; PowerShell and Bash wrappers; GitHub remote `ajinkya-awari/esm2-protein-fitness`.

## Global Constraints

- Do not retrieve ProteinGym data, model checkpoints, or other large assets on the local PC.
- Do not run CPU-heavy embedding, training, UMAP, or full evaluation work locally.
- Default commands must be offline, deterministic, and lightweight.
- Use independent synthetic fixtures only in `data_public/`.
- Keep raw rows, sequences, embeddings, checkpoints, hidden predictions, caches, fitted artifacts, credentials, and tracking payloads out of public paths and Git history.
- Preserve ProteinGym v1.3, single substitutions, UniProt/cluster grouping, ESM1v five-checkpoint parity, pooled mutant-minus-WT ESM2 features, assay-first metrics, and structured LoRA skips.
- A real-data or model stage must fail closed unless explicit flags, approved paths, and platform/resource gates pass.
- Verify each focused commit before attempting remote synchronization; do not bypass a failed check or safety hook.

---

### Task 1: Create the source-only repository boundary

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Create: `pyproject.toml`
- Create: `src/esm2_fitness/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/test_package.py`
- Create: `data_public/README.md`
- Create: `artifacts_restricted/.gitkeep`
- Create: `results_public/README.md`

**Interfaces:**
- Produces an installable package namespace `esm2_fitness` without downloading dependencies.
- Produces Git rules that ignore `artifacts_restricted/`, caches, model files, raw data, `.env`, credentials, and generated restricted outputs.

- [ ] **Step 1: Write repository metadata and ignore rules.**

  `pyproject.toml` must define the package under `src`, expose no network-install command, and configure pytest to discover `tests/`.

  `.gitignore` must include:

  ```text
  .venv/
  __pycache__/
  .pytest_cache/
  *.pyc
  .env
  .env.*
  artifacts_restricted/*
  data_restricted/
  checkpoints/
  embeddings/
  caches/
  hidden_predictions/
  fitted_artifacts/
  *.pt
  *.pth
  *.safetensors
  *.ckpt
  ```

- [ ] **Step 2: Add a package import smoke test.**

  ```python
  def test_package_imports_without_optional_dependencies():
      import esm2_fitness

      assert esm2_fitness.__version__ == "0.1.0"
  ```

- [ ] **Step 3: Run the focused check.**

  Run: `python -m pytest tests/test_package.py -q`

  Expected: one passing test without network access or model files.

- [ ] **Step 4: Commit the boundary.**

  ```text
  git add .gitignore README.md pyproject.toml src tests data_public results_public artifacts_restricted
  git diff --cached --check
  git commit -m "chore: create source repository boundary"
  ```

### Task 2: Implement typed rows and synthetic fixtures

**Files:**
- Create: `src/esm2_fitness/schema.py`
- Create: `data_public/synthetic_mutations.jsonl`
- Create: `tests/test_schema.py`

**Interfaces:**
- `MutationRow.from_mapping(mapping: Mapping[str, object]) -> MutationRow`
- `MutationRow` fields: `assay_id`, `uniprot_id`, `sequence`, `mutation`, `fitness`, `cluster_id`.
- Invalid identifiers, amino-acid symbols, positions, or non-finite fitness values raise `ValueError`.

- [ ] **Step 1: Define the failing schema tests.**

  Tests must cover one valid row, missing `assay_id`, missing `uniprot_id`, invalid mutation notation, out-of-range position, invalid WT residue, and `NaN`/infinite fitness.

- [ ] **Step 2: Run the focused tests and confirm failure.**

  Run: `python -m pytest tests/test_schema.py -q`

  Expected: failure because `MutationRow` is not implemented.

- [ ] **Step 3: Implement the minimal immutable row contract.**

  Accept only single substitutions in the form `A12V`, normalize no biological values silently, and preserve the original sequence and scalar fitness after validation.

- [ ] **Step 4: Add an independent synthetic fixture.**

  Use short invented sequences and assay/group identifiers that are not copied from a released benchmark. Keep the fixture under 20 rows.

- [ ] **Step 5: Run the focused tests and fixture parse.**

  Run: `python -m pytest tests/test_schema.py -q`

  Expected: all schema tests pass and every JSONL fixture row constructs a `MutationRow`.

- [ ] **Step 6: Commit the contract.**

  ```text
  git add src/esm2_fitness/schema.py data_public/synthetic_mutations.jsonl tests/test_schema.py
  git diff --cached --check
  git commit -m "feat(schema): validate synthetic mutation rows"
  ```

### Task 3: Prove mutation parsing and reconstruction

**Files:**
- Create: `src/esm2_fitness/sequences.py`
- Create: `tests/test_sequences.py`

**Interfaces:**
- `parse_substitution(mutation: str) -> Substitution`
- `reconstruct_sequences(sequence: str, substitution: Substitution) -> tuple[str, str]`
- `Substitution` fields: `wt`, `position`, `mutant`.

- [ ] **Step 1: Write tests for valid substitutions, edge positions, WT mismatch, and exact one-character change.**

  Assert that a mismatch raises `ValueError`, positions are one-based at the interface, and the mutant sequence differs from WT at exactly the declared zero-based index.

- [ ] **Step 2: Run the tests to confirm failure.**

  Run: `python -m pytest tests/test_sequences.py -q`

  Expected: failure because sequence functions are absent.

- [ ] **Step 3: Implement parsing and proof.**

  Parse `[A-Z][1-based integer][A-Z]`, reject identical WT/mutant residues, verify the sequence residue, and reconstruct with one replacement.

- [ ] **Step 4: Run the tests.**

  Run: `python -m pytest tests/test_sequences.py -q`

  Expected: all cases pass, including first and last positions.

- [ ] **Step 5: Commit the sequence proof.**

  ```text
  git add src/esm2_fitness/sequences.py tests/test_sequences.py
  git diff --cached --check
  git commit -m "feat(sequences): prove single substitutions"
  ```

### Task 4: Add deterministic grouped split contracts

**Files:**
- Create: `src/esm2_fitness/splits.py`
- Create: `tests/test_splits.py`
- Create: `configs/synthetic_protocol.yaml`

**Interfaces:**
- `assign_groups(group_keys: Sequence[str], seed: int, fractions: Mapping[str, float]) -> dict[str, str]`
- `validate_group_disjointness(observations: Sequence[tuple[str, str]]) -> None`
- `manifest_hash(assignments: Mapping[str, str]) -> str`

- [ ] **Step 1: Write tests for determinism and group disjointness.**

  Use repeated rows from the same UniProt/cluster group and assert that the same seed gives the same manifest, a changed seed can change assignments, and no group appears in two partitions.

- [ ] **Step 2: Run the focused tests and confirm failure.**

  Run: `python -m pytest tests/test_splits.py -q`

  Expected: failure because split functions are absent.

- [ ] **Step 3: Implement stable assignment.**

  Sort unique group keys, derive a deterministic digest from `seed` and group key, allocate complete groups to train/validation/test according to declared fractions, and hash a canonical sorted manifest.

- [ ] **Step 4: Add the synthetic protocol config.**

  Record `protein_gym_release: ProteinGym-v1.3`, `min_seq_id: 0.90`, `coverage: 0.80`, `seed: 20260818`, and `single_substitutions_only: true`.

- [ ] **Step 5: Run the focused tests.**

  Run: `python -m pytest tests/test_splits.py -q`

  Expected: all deterministic and disjointness tests pass without a clustering executable.

- [ ] **Step 6: Commit the split contract.**

  ```text
  git add src/esm2_fitness/splits.py tests/test_splits.py configs/synthetic_protocol.yaml
  git diff --cached --check
  git commit -m "feat(splits): add deterministic group manifests"
  ```

### Task 5: Implement metrics and structured resource status

**Files:**
- Create: `src/esm2_fitness/status.py`
- Create: `src/esm2_fitness/metrics.py`
- Create: `tests/test_metrics.py`
- Create: `tests/test_status.py`

**Interfaces:**
- `StageStatus.skipped(stage: str, reason: str, resource: str) -> StageStatus`
- `spearman_or_status(observed: Sequence[float], predicted: Sequence[float], assay_id: str) -> MetricResult`
- `mse_or_status(observed: Sequence[float], predicted: Sequence[float], assay_id: str) -> MetricResult`
- `macro_average(results: Sequence[MetricResult]) -> MetricResult`

- [ ] **Step 1: Write tests for missing predictions, ties, zero variance, counts, and explicit skips.**

  Assert that row-level missingness is counted, zero-variance Spearman returns a structured `skipped` result, MSE is calculated only over paired finite values, and LoRA absence never substitutes a frozen result.

- [ ] **Step 2: Run focused tests and confirm failure.**

  Run: `python -m pytest tests/test_metrics.py tests/test_status.py -q`

  Expected: failure because status and metric contracts are absent.

- [ ] **Step 3: Implement status and metric contracts.**

  Use standard-library math for MSE and a tie-aware rank implementation for Spearman so the offline suite does not require SciPy. Preserve assay-level results before macro averaging.

- [ ] **Step 4: Run focused tests.**

  Run: `python -m pytest tests/test_metrics.py tests/test_status.py -q`

  Expected: all tests pass with explicit counts and reasons.

- [ ] **Step 5: Commit metrics and skips.**

  ```text
  git add src/esm2_fitness/status.py src/esm2_fitness/metrics.py tests/test_metrics.py tests/test_status.py
  git diff --cached --check
  git commit -m "feat(metrics): add assay metrics and skip records"
  ```

### Task 6: Add provenance and public-artifact privacy gates

**Files:**
- Create: `src/esm2_fitness/provenance.py`
- Create: `src/esm2_fitness/privacy.py`
- Create: `tests/test_provenance.py`
- Create: `tests/test_privacy.py`

**Interfaces:**
- `Provenance.create(protocol: str, split_hash: str, model_revisions: Mapping[str, str], code_revision: str, environment: Mapping[str, str]) -> Provenance`
- `check_public_path(path: Path) -> None`
- `check_public_metadata(metadata: Mapping[str, object]) -> None`

- [ ] **Step 1: Write failing privacy and provenance tests.**

  Reject path components `sequences`, `embeddings`, `checkpoints`, `hidden_predictions`, `caches`, and `fitted_artifacts`; reject metadata containing raw rows, sequence values, embedding arrays, or hidden predictions; accept synthetic aggregate summaries and required provenance fields.

- [ ] **Step 2: Run focused tests and confirm failure.**

  Run: `python -m pytest tests/test_provenance.py tests/test_privacy.py -q`

  Expected: failure because the contracts are absent.

- [ ] **Step 3: Implement fail-closed checks.**

  Make the privacy functions return no approval for unknown artifact types. Keep the check content-light and path-based so it does not open restricted files just to validate them.

- [ ] **Step 4: Run focused tests.**

  Run: `python -m pytest tests/test_provenance.py tests/test_privacy.py -q`

  Expected: all cases pass and restricted examples are rejected.

- [ ] **Step 5: Commit the release boundary.**

  ```text
  git add src/esm2_fitness/provenance.py src/esm2_fitness/privacy.py tests/test_provenance.py tests/test_privacy.py
  git diff --cached --check
  git commit -m "feat(privacy): enforce public artifact boundaries"
  ```

### Task 7: Wire the lightweight pipeline and platform wrappers

**Files:**
- Create: `src/esm2_fitness/pipeline.py`
- Create: `tests/test_pipeline.py`
- Create: `run.ps1`
- Create: `run.sh`
- Create: `Makefile`

**Interfaces:**
- `main(argv: Sequence[str] | None = None) -> int`
- Commands: `check`, `synthetic`, and fail-closed `real`.

- [ ] **Step 1: Write tests for command safety.**

  Assert that `check` and `synthetic` do not require optional dependencies, `real` without `--allow-external-data` returns a nonzero code and a skip record, and no command creates files outside `results_public/` during the synthetic run.

- [ ] **Step 2: Run the focused tests and confirm failure.**

  Run: `python -m pytest tests/test_pipeline.py -q`

  Expected: failure because the dispatcher is absent.

- [ ] **Step 3: Implement the dispatcher.**

  Keep the default path to schema, sequence, split, metric, provenance, and privacy checks. Do not import optional model libraries at module import time. Return exit code 0 for completed lightweight checks and a documented nonzero code for blocked real stages.

- [ ] **Step 4: Add thin wrappers.**

  `run.ps1`, `run.sh`, and `Makefile` must invoke `python -m esm2_fitness.pipeline` with the same arguments and must not contain scientific logic or package installation commands.

- [ ] **Step 5: Run the focused command tests.**

  Run: `python -m pytest tests/test_pipeline.py -q`

  Expected: all command safety tests pass.

- [ ] **Step 6: Commit automation.**

  ```text
  git add src/esm2_fitness/pipeline.py tests/test_pipeline.py run.ps1 run.sh Makefile
  git diff --cached --check
  git commit -m "feat(automation): add offline-safe pipeline commands"
  ```

### Task 8: Add end-to-end synthetic verification and handoff docs

**Files:**
- Create: `tests/test_end_to_end_synthetic.py`
- Create: `docs/PROTOCOL.md`
- Create: `docs/COMPUTE_GATES.md`
- Create: `docs/HANDOFF.md`
- Modify: `README.md`

**Interfaces:**
- The end-to-end test consumes the fixture and public package contracts without real data or model access.
- `docs/HANDOFF.md` records changed files, commands, output status, skipped gates, risks, and next authorized action.

- [ ] **Step 1: Write the end-to-end synthetic test.**

  Exercise fixture load, schema validation, sequence proof, grouped split, one lightweight metric, provenance construction, and privacy approval for a sanitized aggregate summary.

- [ ] **Step 2: Run the test and confirm the current gap.**

  Run: `python -m pytest tests/test_end_to_end_synthetic.py -q`

  Expected: any missing integration wiring is reported before documentation is finalized.

- [ ] **Step 3: Wire only the missing integration behavior.**

  Keep the test independent of network, checkpoints, GPU, SciPy, and large files.

- [ ] **Step 4: Run the full offline suite and compile check.**

  Run:

  ```text
  python -m compileall src tests
  python -m pytest -q
  python -m esm2_fitness.pipeline check
  python -m esm2_fitness.pipeline synthetic
  ```

  Expected: compile succeeds, all offline tests pass, and both lightweight commands exit 0 without network access.

- [ ] **Step 5: Document exact local evidence and skips.**

  Record the output, Python version, Git revision, no-download/no-heavy-CPU status, and the unrun Kaggle/Colab gates in `docs/HANDOFF.md`.

- [ ] **Step 6: Commit the integrated evidence.**

  ```text
  git add tests/test_end_to_end_synthetic.py docs README.md
  git diff --cached --check
  git commit -m "docs: record offline verification and handoff"
  ```

## Final verification checklist

- [ ] `git status --short` contains no untracked restricted artifacts.
- [ ] `git diff --check` returns exit code 0.
- [ ] `python -m compileall src tests` returns exit code 0.
- [ ] `python -m pytest -q` reports zero failures.
- [ ] `python -m esm2_fitness.pipeline check` returns exit code 0.
- [ ] `python -m esm2_fitness.pipeline synthetic` returns exit code 0.
- [ ] A local scan finds no `.env`, checkpoint, embedding, hidden-prediction, cache, or fitted-artifact files.
- [ ] The handoff records the blocked or completed remote synchronization attempt without claiming unrun external gates.
