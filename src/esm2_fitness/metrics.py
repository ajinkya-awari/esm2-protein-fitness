"""Assay-first metrics implemented without heavyweight dependencies."""

from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Sequence


@dataclass(frozen=True)
class MetricResult:
    assay_id: str
    metric: str
    status: str
    value: float | None
    n_total: int
    n_used: int
    failure_count: int
    reason: str | None = None
    n_assays: int = 1


def _paired_finite(observed: Sequence[float], predicted: Sequence[float]) -> tuple[list[float], list[float], int]:
    if len(observed) != len(predicted):
        raise ValueError("observed and predicted lengths differ")
    pairs = [
        (float(actual), float(estimate))
        for actual, estimate in zip(observed, predicted)
        if math.isfinite(float(actual)) and math.isfinite(float(estimate))
    ]
    actual = [pair[0] for pair in pairs]
    estimate = [pair[1] for pair in pairs]
    return actual, estimate, len(observed) - len(pairs)


def _rank(values: Sequence[float]) -> list[float]:
    ordered = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    index = 0
    while index < len(ordered):
        end = index + 1
        while end < len(ordered) and ordered[end][1] == ordered[index][1]:
            end += 1
        average_rank = (index + 1 + end) / 2.0
        for original_index, _ in ordered[index:end]:
            ranks[original_index] = average_rank
        index = end
    return ranks


def _correlation(left: Sequence[float], right: Sequence[float]) -> float:
    left_mean = sum(left) / len(left)
    right_mean = sum(right) / len(right)
    left_delta = [value - left_mean for value in left]
    right_delta = [value - right_mean for value in right]
    left_norm = math.sqrt(sum(value * value for value in left_delta))
    right_norm = math.sqrt(sum(value * value for value in right_delta))
    if left_norm == 0.0 or right_norm == 0.0:
        raise ValueError("zero variance")
    return sum(a * b for a, b in zip(left_delta, right_delta)) / (left_norm * right_norm)


def spearman_or_status(
    observed: Sequence[float], predicted: Sequence[float], assay_id: str
) -> MetricResult:
    actual, estimate, failures = _paired_finite(observed, predicted)
    if len(actual) < 2:
        return MetricResult(assay_id, "spearman", "skipped", None, len(observed), len(actual), failures, "insufficient pairs")
    try:
        value = _correlation(_rank(actual), _rank(estimate))
    except ValueError:
        return MetricResult(assay_id, "spearman", "skipped", None, len(observed), len(actual), failures, "zero variance")
    return MetricResult(assay_id, "spearman", "completed", value, len(observed), len(actual), failures)


def mse_or_status(observed: Sequence[float], predicted: Sequence[float], assay_id: str) -> MetricResult:
    actual, estimate, failures = _paired_finite(observed, predicted)
    if not actual:
        return MetricResult(assay_id, "mse", "skipped", None, len(observed), 0, failures, "no finite pairs")
    value = sum((left - right) ** 2 for left, right in zip(actual, estimate)) / len(actual)
    return MetricResult(assay_id, "mse", "completed", value, len(observed), len(actual), failures)


def macro_average(results: Sequence[MetricResult]) -> MetricResult:
    completed = [result for result in results if result.status == "completed" and result.value is not None]
    if not completed:
        return MetricResult("macro", "macro", "skipped", None, 0, 0, 0, "no completed assays", 0)
    return MetricResult(
        assay_id="macro",
        metric=completed[0].metric,
        status="completed",
        value=sum(result.value for result in completed) / len(completed),
        n_total=sum(result.n_total for result in completed),
        n_used=sum(result.n_used for result in completed),
        failure_count=sum(result.failure_count for result in completed),
        n_assays=len(completed),
    )
