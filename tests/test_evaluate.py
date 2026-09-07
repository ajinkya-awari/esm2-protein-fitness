"""Offline contract tests for evaluate.py."""

import json
import pytest
from pathlib import Path
from esm2_fitness.evaluate import (
    evaluate_predictions,
    run_median_baseline,
    run_ridge_baseline,
    aggregate_results,
    write_sanitized_summary,
    write_restricted_record,
)


OBSERVED = [1.0, 2.0, 3.0, 4.0, 5.0]
PREDICTED = [1.1, 2.1, 2.9, 4.0, 5.2]


def test_evaluate_predictions_completed():
    result = evaluate_predictions("ASSAY1", OBSERVED, PREDICTED, "test_model")
    assert result["assay_id"] == "ASSAY1"
    assert result["model"] == "test_model"
    assert result["spearman"]["status"] == "completed"
    assert result["mse"]["status"] == "completed"
    assert result["spearman"]["value"] is not None


def test_run_median_baseline():
    result = run_median_baseline("ASSAY1", [1.0, 2.0, 3.0], [4.0, 5.0])
    assert result["model"] == "median_baseline"
    assert "spearman" in result


def test_run_ridge_baseline():
    X_train = [[float(i), float(i * 2)] for i in range(1, 8)]
    y_train = [float(i) for i in range(1, 8)]
    X_test = [[5.0, 10.0], [6.0, 12.0]]
    y_test = [5.0, 6.0]
    result = run_ridge_baseline("ASSAY1", X_train, y_train, X_test, y_test)
    assert result["model"] == "ridge_baseline"


def test_run_ridge_baseline_insufficient_train():
    result = run_ridge_baseline("ASSAY1", [[1.0]], [1.0], [[2.0]], [2.0])
    assert result["status"] == "skipped"
    assert "insufficient" in result["reason"]


def test_aggregate_results():
    records = [
        evaluate_predictions("A1", [1.0, 2.0, 3.0], [1.0, 2.0, 3.0], "median_baseline"),
        evaluate_predictions("A2", [1.0, 2.0, 3.0], [3.0, 2.0, 1.0], "median_baseline"),
    ]
    agg = aggregate_results(records, "median_baseline")
    assert agg["model"] == "median_baseline"
    assert agg["macro_spearman"]["status"] == "completed"


def test_write_sanitized_summary_to_results_public(tmp_path):
    results_public = tmp_path / "results_public"
    results_public.mkdir()
    out = results_public / "summary.json"
    summary = {"macro_spearman": 0.75, "n_assays": 10}
    write_sanitized_summary(summary, out)
    loaded = json.loads(out.read_text())
    assert loaded["n_assays"] == 10


def test_write_sanitized_summary_rejects_restricted_path(tmp_path):
    restricted = tmp_path / "artifacts_restricted" / "summary.json"
    with pytest.raises(ValueError, match="restricted"):
        write_sanitized_summary({"x": 1}, restricted)


def test_write_sanitized_summary_rejects_restricted_metadata(tmp_path):
    results_public = tmp_path / "results_public"
    results_public.mkdir()
    out = results_public / "bad.json"
    with pytest.raises(ValueError, match="restricted"):
        write_sanitized_summary({"embeddings": [0.1, 0.2]}, out)


def test_write_restricted_record(tmp_path):
    restricted = tmp_path / "artifacts_restricted"
    restricted.mkdir()
    path = restricted / "record.json"
    write_restricted_record({"assay_id": "A1", "predictions": [1.0]}, path)
    loaded = json.loads(path.read_text())
    assert loaded["assay_id"] == "A1"
