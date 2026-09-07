"""Offline contract tests for models.py."""

import math
import pytest
from esm2_fitness.models import MedianBaseline, RidgeBaseline


class TestMedianBaseline:
    def test_odd_count(self):
        m = MedianBaseline().fit([1.0, 3.0, 5.0])
        assert m.predict(3) == [3.0, 3.0, 3.0]

    def test_even_count(self):
        m = MedianBaseline().fit([1.0, 2.0, 3.0, 4.0])
        preds = m.predict(2)
        assert preds == [2.5, 2.5]

    def test_ignores_non_finite(self):
        m = MedianBaseline().fit([float("nan"), 2.0, 4.0])
        preds = m.predict(1)
        assert preds == [3.0]

    def test_all_non_finite_raises(self):
        with pytest.raises(ValueError, match="No finite"):
            MedianBaseline().fit([float("nan"), float("inf")])

    def test_not_fitted_raises(self):
        with pytest.raises(RuntimeError, match="not fitted"):
            MedianBaseline().predict(1)

    def test_fitted_flag(self):
        m = MedianBaseline()
        assert not m.fitted
        m.fit([1.0, 2.0])
        assert m.fitted


class TestRidgeBaseline:
    def test_perfect_fit(self):
        # y = 2*x, should recover near-zero intercept and weight ≈ 2.0
        X = [[float(i)] for i in range(1, 11)]
        y = [2.0 * i for i in range(1, 11)]
        r = RidgeBaseline(alpha=1e-6).fit(X, y)
        preds = r.predict([[5.0], [10.0]])
        assert abs(preds[0] - 10.0) < 0.01
        assert abs(preds[1] - 20.0) < 0.01

    def test_constant_output_for_zero_features(self):
        X = [[0.0, 0.0]] * 5
        y = [3.0] * 5
        r = RidgeBaseline().fit(X, y)
        preds = r.predict([[0.0, 0.0]])
        assert abs(preds[0] - 3.0) < 1e-6

    def test_invalid_alpha(self):
        with pytest.raises(ValueError, match="alpha"):
            RidgeBaseline(alpha=0.0)

    def test_not_fitted_raises(self):
        with pytest.raises(RuntimeError, match="not fitted"):
            RidgeBaseline().predict([[1.0]])

    def test_fitted_flag(self):
        r = RidgeBaseline()
        assert not r.fitted
        r.fit([[1.0]], [2.0])
        assert r.fitted
