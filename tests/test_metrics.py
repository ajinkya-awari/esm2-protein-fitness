import math

import pytest

from esm2_fitness.metrics import macro_average, mse_or_status, spearman_or_status


def test_spearman_is_computed_per_assay():
    result = spearman_or_status([1.0, 2.0, 3.0], [0.2, 0.4, 0.8], "assay-a")

    assert result.status == "completed"
    assert result.assay_id == "assay-a"
    assert result.value == pytest.approx(1.0)
    assert result.n_used == 3


def test_spearman_handles_ties():
    result = spearman_or_status([1.0, 1.0, 2.0, 3.0], [0.2, 0.2, 0.4, 0.8], "assay-a")

    assert result.status == "completed"
    assert result.value == pytest.approx(1.0)


def test_spearman_skips_zero_variance_assay():
    result = spearman_or_status([1.0, 1.0, 1.0], [0.2, 0.4, 0.8], "assay-a")

    assert result.status == "skipped"
    assert result.reason == "zero variance"


def test_mse_counts_and_ignores_missing_pairs():
    result = mse_or_status([1.0, math.nan, 3.0], [1.5, 100.0, math.inf], "assay-a")

    assert result.status == "completed"
    assert result.value == 0.25
    assert result.n_total == 3
    assert result.n_used == 1
    assert result.failure_count == 2


def test_metric_with_no_finite_pairs_is_skipped():
    result = mse_or_status([math.nan], [math.inf], "assay-a")

    assert result.status == "skipped"
    assert result.failure_count == 1


def test_macro_average_uses_completed_assay_results():
    first = mse_or_status([0.0, 1.0], [0.0, 2.0], "assay-a")
    second = mse_or_status([0.0, 2.0], [0.0, 4.0], "assay-b")
    skipped = mse_or_status([math.nan], [math.inf], "assay-c")

    result = macro_average([first, second, skipped])

    assert result.status == "completed"
    assert result.assay_id == "macro"
    assert result.value == 1.25
    assert result.n_assays == 2
