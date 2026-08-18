"""Offline contracts for official ESM1v five-checkpoint parity."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from dataclasses import dataclass
import math


OFFICIAL_CHECKPOINTS = tuple(f"esm1v_t33_650M_UR90S_{index}" for index in range(1, 6))


@dataclass(frozen=True)
class ESM1VParityResult:
    checkpoint_scores: dict[str, float]
    mean_score: float


def validate_official_checkpoints(checkpoints: Sequence[str]) -> tuple[str, ...]:
    normalized = tuple(checkpoints)
    if normalized != OFFICIAL_CHECKPOINTS:
        raise ValueError("ESM1v parity requires the ordered five official checkpoints")
    return normalized


def score_masked_marginal(wild_type_log_probability: float, mutant_log_probability: float) -> float:
    if not math.isfinite(wild_type_log_probability) or not math.isfinite(mutant_log_probability):
        raise ValueError("log probabilities must be finite")
    return float(mutant_log_probability - wild_type_log_probability)


def score_with_official_checkpoints(score_one: Callable[[str], float]) -> ESM1VParityResult:
    validate_official_checkpoints(OFFICIAL_CHECKPOINTS)
    scores: dict[str, float] = {}
    for checkpoint in OFFICIAL_CHECKPOINTS:
        score = float(score_one(checkpoint))
        if not math.isfinite(score):
            raise ValueError(f"non-finite ESM1v score for {checkpoint}")
        scores[checkpoint] = score
    return ESM1VParityResult(checkpoint_scores=scores, mean_score=sum(scores.values()) / len(scores))
