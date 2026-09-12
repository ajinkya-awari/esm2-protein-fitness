# ESM2 Protein Mutation-Fitness Benchmark

[![Demo on HuggingFace Spaces](https://img.shields.io/badge/🤗%20HF%20Space-Live%20Demo-blue)](https://huggingface.co/spaces/ajinkya1807/esm2-protein-fitness)
[![Kaggle Kernel](https://img.shields.io/badge/Kaggle-Kernel%20v17-20BEFF?logo=kaggle)](https://www.kaggle.com/code/ajinkya1225/15-esm2-protein-mutation-fitness-benchmark)
[![Dataset](https://img.shields.io/badge/Kaggle-Dataset-20BEFF?logo=kaggle)](https://www.kaggle.com/datasets/ajinkya1225/esm2-protein-fitness-source)
[![Data: ProteinGym v1](https://img.shields.io/badge/🤗%20Data-ProteinGym%20v1-yellow)](https://huggingface.co/datasets/OATML-Markslab/ProteinGym_v1)

A reproducible, leakage-aware benchmark comparing frozen ESM1v and ESM2 representations against simple supervised baselines on ProteinGym single amino-acid substitution assays.

**Live demo:** https://huggingface.co/spaces/ajinkya1807/esm2-protein-fitness  
**Kaggle execution kernel:** https://www.kaggle.com/code/ajinkya1225/15-esm2-protein-mutation-fitness-benchmark  
**Source dataset:** https://www.kaggle.com/datasets/ajinkya1225/esm2-protein-fitness-source

> **Research artifact.** This repository is an auditable reproducibility framework — not a clinical, experimental, commercial, or causal claim. No superior performance, biological discovery, or deployment readiness is asserted.

---

## Problem

Protein language models (ESM1v, ESM2) produce rich sequence representations, but fair comparison against simple baselines is undermined by two common failures: (1) **group leakage** — train/test splits that allow related proteins to appear on both sides, inflating apparent generalisation; (2) **silent fallbacks** — unavailable model or data stages that pass silently instead of producing an explicit `skipped` record.

This project enforces grouped splits, assay-first metrics, structured skip/failure records, and a strict public/restricted artifact boundary, making every evaluation decision auditable.

---

## Architecture

```mermaid
flowchart TD
    A[ProteinGym v1.3\nSingle Substitutions] --> B[Schema &\nMutation Validation]
    B --> C[WT / Mutant\nReconstruction]
    C --> D[Grouped Split\nUniProt + Cluster Hash]
    D --> E1[ESM1v\nMasked-Marginal ×5 ckpts]
    D --> E2[Frozen ESM2\nPooled ΔWT→Mut]
    D --> E3[Baselines\nMedian / Ridge]
    E1 --> F[Per-Assay Spearman & MSE]
    E2 --> F
    E3 --> F
    F --> G[Macro Summaries\n+ Block Bootstrap]
    G --> H{Privacy Gate}
    H -->|PASS| I[results_public/\nSanitised Aggregates]
    H -->|FAIL| J[artifacts_restricted/\nLocal Only]
    E2 -.->|T4 gate| K[Optional LoRA\nskipped if no T4]
```

---

## Package structure

```
src/esm2_fitness/
├── schema.py          # Typed MutationRow validation
├── sequences.py       # Single-substitution parsing & WT/mutant reconstruction
├── splits.py          # Deterministic grouped split with SHA-256 manifest hash
├── metrics.py         # Per-assay Spearman, MSE, macro average
├── provenance.py      # Protocol, split, model, code, environment records
├── privacy.py         # Fail-closed public artifact path/metadata checks
├── esm1v.py           # Official five-checkpoint masked-marginal contracts
├── embeddings.py      # Frozen ESM2 pooled mutant-minus-WT shape contracts
├── contracts.py       # BenchmarkTask, EvaluatorContract, FrozenEmbeddingContract, FineTuningContract
├── checksums.py       # SHA-256 manifest helpers for evidence records
├── explainability.py  # Exploratory interpretation boundaries
├── resources.py       # T4 LoRA resource gate
├── status.py          # Structured StageStatus (skipped / ready)
└── pipeline.py        # Offline-safe CLI dispatcher

configs/
└── synthetic_protocol.yaml   # Protocol, split, model revision declarations

data_public/
└── synthetic_mutations.jsonl  # 5 independently synthetic rows (no benchmark data)

results_public/
└── README.md          # No real results present yet — see verification status below

notebooks/
├── kaggle_esm2_protein.ipynb         # Approved platform runner (Kaggle)
└── KAGGLE_RUNBOOK_esm2_protein.md    # Step-by-step execution guide

tests/                 # 87 offline contract tests
docs/                  # Protocol, compute gates, handoff records
```

---

## Installation

```bash
git clone https://github.com/ajinkya-awari/esm2-protein-fitness.git
cd esm2-protein-fitness
pip install -e .
```

Requires Python ≥ 3.11. No heavyweight ML dependencies for the offline contract layer.

---

## Local synthetic tests (offline, no data/model required)

```bash
python -m pytest -q
```

On Windows:
```powershell
./run.ps1 check
./run.ps1 synthetic
./run.ps1 gates
```

On Linux/macOS:
```bash
./run.sh check
./run.sh synthetic
./run.sh gates
```

The `gates` command reports ESM1v, frozen ESM2, and LoRA as structured `skipped` records until their approved checkpoint/data or T4 environment is available. No network access, no checkpoint download, no GPU work.

---

## Kaggle execution

Real data and model stages run in a separate approved Kaggle session. See `notebooks/KAGGLE_RUNBOOK_esm2_protein.md` for the full step-by-step guide.

**Approval gate:** the notebook stops at cell 9 (Stage B) unless explicit approval is recorded for ProteinGym data access, model checkpoints, GPU/heavy CPU work, and the output boundary. Do not run cells 10–13 without that approval in place.

```bash
# Stage the kernel (after configuring kaggle.json)
kaggle kernels push -p <KAGGLE_STAGING_FOLDER>
kaggle kernels status ajinkya1225/15-esm2-protein
```

---

## Split and leakage-control design

All assay observations for a protein are kept together by grouping on **UniProt ID** and a **deterministic MMseqs2 sequence-similarity cluster** (`min_seq_id=0.90`, `coverage=0.80`, `seed=20260818`). The split manifest is hashed with SHA-256 and stored in every provenance record. Uncertainty is bootstrapped over the declared protein/cluster group — not over independent mutation rows.

---

## Metric definitions

| Metric | Scope | Aggregation |
|--------|-------|-------------|
| Spearman ρ | Per assay | Macro average over completed assays |
| MSE | Per assay | Macro average over completed assays |
| Bootstrap CI | Group-resampled | Block bootstrap over protein/cluster groups |

Assay-level metrics are always computed before macro summaries. An assay with fewer than 2 finite paired observations is recorded as `skipped`, never silently dropped.

---

## Provenance and checksum requirements

Every evaluation record must contain:
- `protocol` — ProteinGym release version
- `split_hash` — SHA-256 of the canonical group-to-partition manifest
- `model_revisions` — exact checkpoint or HuggingFace revision string per model
- `code_revision` — Git commit SHA
- `environment` — Python version, key package versions

Source file and evidence manifests use `checksums.create_manifest` to record SHA-256 and byte size for each file.

---

## Privacy and artifact restrictions

| Artifact type | Location | Status |
|--------------|----------|--------|
| Raw ProteinGym rows | `artifacts_restricted/` | Restricted — never published |
| Sequences | `artifacts_restricted/` | Restricted |
| Embeddings | `artifacts_restricted/` | Restricted |
| Model checkpoints | `artifacts_restricted/` | Restricted |
| Hidden predictions | `artifacts_restricted/` | Restricted |
| Fitted artifacts | `artifacts_restricted/` | Restricted |
| Synthetic fixtures | `data_public/` | Public — independently invented |
| Sanitised aggregate summaries | `results_public/` | Public — after privacy gate |

The `privacy.check_public_path` and `privacy.check_public_metadata` functions enforce these boundaries with fail-closed checks. UMAP and other visualisations are exploratory only and make no biological or clinical claim.

---

## Results

Evaluated on 40 held-out ProteinGym single-substitution assays (CPU fallback, 10 rows per assay for ESM1v, 40 rows per assay for ESM2 embeddings; Kaggle kernel v17, 2026-09-13).

| Model | Macro Spearman ρ | Macro MSE | N assays |
|-------|-----------------|-----------|----------|
| ESM1v — 5-ckpt masked-marginal | **0.475** | 36.86 | 40 |
| ESM2-650M + Ridge (within-assay) | **0.266** | 0.749 | 40 |
| Median baseline | undefined† | 0.888 | 40 |

†Median predicts a single constant value per assay — all predicted ranks are tied, making Spearman undefined. MSE is reported instead.

**Hardware note:** Kaggle assigned a P100 GPU (CUDA sm_60), incompatible with PyTorch 2.x (requires sm_70+). All model inference ran on CPU with reduced row counts per assay. Full-assay scoring requires CUDA sm_70+ (T4 or newer). See `evidence/hardware_note.txt`.

**Split note:** The global split is grouped by UniProt ID. Ridge/Median baselines used a within-assay random 75/25 split (30 train, 10 test per assay) since all rows for a test protein belong to the test partition. ESM1v is zero-shot and unaffected by this.

Sanitised per-model summaries: `results_public/esm1v_macro_summary.json`, `results_public/esm2_ridge_macro_summary.json`, `results_public/median_macro_summary.json`.

---

## Verification status

| Stage | Status | Evidence date |
|-------|--------|--------------|
| `python -m compileall src tests` | ✅ **Locally verified** — exit 0 | 2026-09-07 |
| `python -m pytest -q` (87 tests) | ✅ **Locally verified** — 87 passed, 0.78s | 2026-09-07 |
| `pipeline check / synthetic / gates` | ✅ **Locally verified** — exit 0 | 2026-09-07 |
| Schema, split, metric, privacy contracts | ✅ **Locally verified** (synthetic fixtures) | 2026-09-07 |
| Kaggle notebook Stage A (env / source / 87 tests / gates) | ✅ **Verified** — kernel v3, 87 passed 0.25s, approval gate closed | 2026-09-07 |
| ProteinGym acquisition (HuggingFace Hub) | ✅ **Verified** — 2,465,767 rows, 696,311 valid, 40 test assays | 2026-09-13 |
| ESM1v parity (5 checkpoints, CPU) | ✅ **Verified** — 40 assays, macro ρ = 0.475, kernel v17 | 2026-09-13 |
| Frozen ESM2 inference (650M, CPU) | ✅ **Verified** — 1,600 rows, 0 failures, kernel v17 | 2026-09-13 |
| Baseline metrics (Ridge + Median, real data) | ✅ **Verified** — 40 assays each, kernel v17 | 2026-09-13 |
| Public results (sanitised aggregates) | ✅ **Verified** — `results_public/` written, privacy-gated | 2026-09-13 |
| Grouped bootstrap CI | 🔒 **Pending** — requires full-assay data (T4 or newer GPU) | — |
| Optional LoRA (T4) | 🔒 **Pending** — requires T4 gate + approval | — |

---

## Limitations

- CPU fallback reduces rows per assay (10 for ESM1v, 40 for ESM2) relative to full-assay scoring. Results on a T4+ GPU with all rows may differ.
- Ridge/Median baselines use within-assay random split rather than cross-protein generalisation, because the global grouped split places all mutations of a protein in the same partition.
- The LoRA route requires a T4 GPU and explicit resource gate; it is never silently run on CPU.
- An unavailable model, data source, or resource always produces a structured `skipped` record — never a silent substitution.
- This is a research reproducibility framework, not a production system. No clinical, diagnostic, or commercial use is implied.
- UMAP visualisations (when run on real data) are exploratory summaries, not causal or biological proofs.

---

## Reproducibility

All randomness is controlled by `seed=20260818` in the split configuration. The split manifest hash must match across runs. Every evaluation record must contain the protocol version, split hash, model revisions, code revision, and environment hash.

To reproduce the offline synthetic validation:

```bash
git clone https://github.com/ajinkya-awari/esm2-protein-fitness.git
cd esm2-protein-fitness
pip install -e . pytest
python -m pytest -q
```

---

## Citation and attribution

If you use this benchmark framework, please cite the underlying resources:

- **ProteinGym:** Notin et al., *Proteingym: Large-scale benchmarks for protein fitness prediction*, NeurIPS 2023.
- **ESM2 / ESM1v:** Lin et al., *Evolutionary-scale prediction of atomic-level protein structure with a language model*, Science 2023.
- **ESM1v masked-marginal scoring:** Meier et al., *Language models enable zero-shot prediction of the effects of mutations on protein function*, NeurIPS 2021.

---

## Roadmap

- [x] Kaggle Stage A: environment, source, 87 tests, all gates — verified kernel v3 (2026-09-07)
- [x] Kaggle Stage B+: ProteinGym acquisition (HuggingFace Hub), 696K valid rows, 40 test assays
- [x] ESM1v parity run on official five checkpoints — macro ρ = 0.475 (kernel v17, 2026-09-13)
- [x] Frozen ESM2 representation extraction — 1,600 rows, 0 failures (kernel v17, 2026-09-13)
- [x] Baseline and Ridge regression metrics — 40 assays, ρ = 0.266 (kernel v17, 2026-09-13)
- [x] Public results summary with privacy-checked aggregates — `results_public/` written
- [ ] Full-assay ESM1v + ESM2 scoring (requires T4 or newer GPU, CUDA sm_70+)
- [ ] Grouped bootstrap confidence intervals (requires full-assay data)
- [ ] Optional T4 LoRA run (requires T4 gate + approval)
- [ ] HuggingFace Space demo

---

## License

MIT — see [LICENSE](LICENSE).
