# Public results

Only sanitised aggregate summaries and figures that pass the privacy checker belong here. Raw rows, sequences, embeddings, hidden predictions, checkpoints, caches, fitted artifacts, and tracking payloads remain restricted and are never published.

## Current contents (kernel v17, 2026-09-13)

| File | Model | Macro Spearman | Macro MSE | N assays |
|------|-------|---------------|-----------|----------|
| `esm1v_macro_summary.json` | ESM1v 5-ckpt masked-marginal | **0.475** | 36.86 | 40 |
| `esm2_ridge_macro_summary.json` | ESM2-650M + Ridge (within-assay) | **0.266** | 0.749 | 40 |
| `median_macro_summary.json` | Median baseline | undefined† | 0.888 | 40 |

†Constant predictor — Spearman undefined (all tied ranks). MSE reported instead.

**Scope:** 40 held-out ProteinGym single-substitution assays, CPU fallback (10 rows/assay for ESM1v; 40 rows/assay for ESM2 embeddings). Full-assay scoring requires CUDA sm_70+ (T4 or newer GPU).
