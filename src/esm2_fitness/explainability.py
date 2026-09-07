"""Public-safe boundaries for exploratory interpretation artifacts."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence


RESTRICTED_INPUTS = frozenset(
    {
        "raw_rows",
        "sequence",
        "sequences",
        "embedding",
        "embeddings",
        "hidden_predictions",
        "checkpoints",
        "fitted_artifacts",
    }
)
PROHIBITED_CLAIM_TERMS = (
    "clinical",
    "causal",
    "causality",
    "proves",
    "experimental truth",
    "commercial",
    "superior",
)


@dataclass(frozen=True)
class ExplainabilityReport:
    method: str
    scope: str
    inputs: tuple[str, ...]
    claims: tuple[str, ...]

    @classmethod
    def create(
        cls,
        *,
        method: str,
        scope: str,
        inputs: Sequence[str],
        claims: Sequence[str],
    ) -> "ExplainabilityReport":
        if not method:
            raise ValueError("method is required")
        if scope != "exploratory":
            raise ValueError("explainability scope must be exploratory")
        normalized_inputs = tuple(inputs)
        if not normalized_inputs:
            raise ValueError("inputs are required")
        if any(item.casefold() in RESTRICTED_INPUTS for item in normalized_inputs):
            raise ValueError("restricted input cannot be used in public explainability output")
        normalized_claims = tuple(claims)
        if not normalized_claims:
            raise ValueError("claims are required")
        claim_text = " ".join(normalized_claims).casefold()
        if any(term in claim_text for term in PROHIBITED_CLAIM_TERMS):
            raise ValueError("claim exceeds exploratory explainability boundary")
        return cls(method=method, scope=scope, inputs=normalized_inputs, claims=normalized_claims)
