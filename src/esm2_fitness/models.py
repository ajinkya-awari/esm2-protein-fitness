"""Supervised baselines: median predictor and Ridge regression.

These are intentionally dependency-light contracts at import time.
RidgeBaseline.fit() requires numpy (always available on Kaggle).
"""

from __future__ import annotations

import math
from typing import Sequence


class MedianBaseline:
    """Predicts the training-set median for every test point."""

    def __init__(self) -> None:
        self._median: float | None = None

    def fit(self, y_train: Sequence[float]) -> "MedianBaseline":
        finite = sorted(v for v in y_train if math.isfinite(float(v)))
        if not finite:
            raise ValueError("No finite training values for MedianBaseline")
        n = len(finite)
        self._median = (finite[n // 2] if n % 2 else (finite[n // 2 - 1] + finite[n // 2]) / 2.0)
        return self

    def predict(self, n: int) -> list[float]:
        if self._median is None:
            raise RuntimeError("MedianBaseline not fitted")
        return [self._median] * n

    @property
    def fitted(self) -> bool:
        return self._median is not None


class RidgeBaseline:
    """Ridge regression on dense feature vectors.

    Uses numpy.linalg.lstsq under the hood; numpy must be importable at fit time.
    alpha: L2 regularisation strength (default 1.0).
    """

    def __init__(self, alpha: float = 1.0) -> None:
        if alpha <= 0:
            raise ValueError("alpha must be positive")
        self._alpha = alpha
        self._coef: list[float] | None = None
        self._intercept: float | None = None

    def fit(self, X: list[list[float]], y: list[float]) -> "RidgeBaseline":
        try:
            import numpy as np
        except ImportError as exc:
            raise RuntimeError("RidgeBaseline.fit requires numpy") from exc
        X_arr = np.array(X, dtype=float)
        y_arr = np.array(y, dtype=float)
        n, d = X_arr.shape
        # Augment X with a bias column of ones, then add alpha to the diagonal
        # (excluding the bias column) to get Ridge solution in one lstsq call.
        X_aug = np.hstack([X_arr, np.ones((n, 1))])
        reg = np.eye(d + 1) * self._alpha
        reg[-1, -1] = 0.0  # do not regularise the bias
        A = X_aug.T @ X_aug + reg
        b = X_aug.T @ y_arr
        params, *_ = np.linalg.lstsq(A, b, rcond=None)
        self._coef = params[:-1].tolist()
        self._intercept = float(params[-1])
        return self

    def predict(self, X: list[list[float]]) -> list[float]:
        if self._coef is None or self._intercept is None:
            raise RuntimeError("RidgeBaseline not fitted")
        return [
            self._intercept + sum(w * x for w, x in zip(self._coef, row))
            for row in X
        ]

    @property
    def fitted(self) -> bool:
        return self._coef is not None
