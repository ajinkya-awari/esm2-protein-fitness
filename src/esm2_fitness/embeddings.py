"""Shape-safe frozen ESM2 pooled mutant-minus-WT feature contracts."""

from __future__ import annotations

from collections.abc import Sequence
import math


def validate_embedding_pair(
    wild_type: Sequence[float], mutant: Sequence[float], expected_dim: int | None = None
) -> None:
    if not wild_type or not mutant:
        raise ValueError("embedding vectors cannot be empty")
    if len(wild_type) != len(mutant):
        raise ValueError("embedding vectors must have the same dimension")
    if expected_dim is not None and len(wild_type) != expected_dim:
        raise ValueError("embedding vectors do not match expected dimension")
    if any(not math.isfinite(float(value)) for value in (*wild_type, *mutant)):
        raise ValueError("embedding values must be finite")


def pooled_mutant_minus_wt(wild_type: Sequence[float], mutant: Sequence[float]) -> tuple[float, ...]:
    validate_embedding_pair(wild_type, mutant)
    return tuple(float(mutant_value) - float(wild_type_value) for wild_type_value, mutant_value in zip(wild_type, mutant))
