"""Per-assay evaluation orchestration with public/restricted artifact boundary.

All restricted outputs (embeddings, predictions, fitted models) stay in
artifacts_restricted/. Only privacy-checked aggregate summaries go to results_public/.
"""

from __future__ import annotations

import json
import math
from collections import defaultdict
from dataclasses import asdict
from pathlib import Path
from typing import Sequence

from .metrics import spearman_or_status, mse_or_status, macro_average, MetricResult
from .models import MedianBaseline, RidgeBaseline
from .privacy import check_public_path, check_public_metadata


def evaluate_predictions(
    assay_id: str,
    observed: Sequence[float],
    predicted: Sequence[float],
    model_name: str,
) -> dict[str, object]:
    """Return per-assay Spearman and MSE for one model's predictions."""
    sp = spearman_or_status(observed, predicted, assay_id)
    ms = mse_or_status(observed, predicted, assay_id)
    return {
        "assay_id": assay_id,
        "model": model_name,
        "spearman": asdict(sp),
        "mse": asdict(ms),
    }


def run_median_baseline(
    assay_id: str,
    y_train: Sequence[float],
    y_test: Sequence[float],
) -> dict[str, object]:
    """Fit median baseline on train, evaluate on test."""
    baseline = MedianBaseline().fit(y_train)
    predicted = baseline.predict(len(y_test))
    return evaluate_predictions(assay_id, y_test, predicted, "median_baseline")


def run_ridge_baseline(
    assay_id: str,
    X_train: list[list[float]],
    y_train: list[float],
    X_test: list[list[float]],
    y_test: list[float],
    alpha: float = 1.0,
) -> dict[str, object]:
    """Fit Ridge on train embeddings, evaluate on test embeddings."""
    if len(X_train) < 2:
        return {
            "assay_id": assay_id,
            "model": "ridge_baseline",
            "status": "skipped",
            "reason": "insufficient training samples",
        }
    ridge = RidgeBaseline(alpha=alpha).fit(X_train, y_train)
    predicted = ridge.predict(X_test)
    return evaluate_predictions(assay_id, y_test, predicted, "ridge_baseline")


def aggregate_results(
    per_assay: list[dict[str, object]],
    model_name: str,
) -> dict[str, object]:
    """Compute macro-average Spearman and MSE over completed assays."""
    spearman_results: list[MetricResult] = []
    mse_results: list[MetricResult] = []
    for record in per_assay:
        if record.get("model") != model_name:
            continue
        sp_raw = record.get("spearman")
        ms_raw = record.get("mse")
        if isinstance(sp_raw, dict):
            spearman_results.append(MetricResult(**sp_raw))  # type: ignore[arg-type]
        if isinstance(ms_raw, dict):
            mse_results.append(MetricResult(**ms_raw))  # type: ignore[arg-type]
    macro_sp = macro_average(spearman_results)
    macro_ms = macro_average(mse_results)
    return {
        "model": model_name,
        "macro_spearman": asdict(macro_sp),
        "macro_mse": asdict(macro_ms),
    }


def write_restricted_record(record: dict[str, object], path: Path) -> None:
    """Write an evaluation record to a restricted path (no public check)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_sanitized_summary(summary: dict[str, object], path: Path) -> None:
    """Write a privacy-checked aggregate summary to a public results path."""
    check_public_path(path)
    check_public_metadata(summary)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
