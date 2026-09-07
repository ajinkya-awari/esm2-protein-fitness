"""Research contracts for tasks, evaluators, model adapters, and training gates."""

from __future__ import annotations

from dataclasses import dataclass
from collections.abc import Sequence


GROUPED_SPLIT_UNITS = frozenset({"uniprot_id", "cluster_id", "uniprot_cluster"})
SUPPORTED_METRICS = frozenset({"spearman", "mse"})


def _require_nonempty_text(value: str, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError(f"{field} is required")
    return value


def _normalize_metrics(metrics: Sequence[str]) -> tuple[str, ...]:
    normalized = tuple(metrics)
    if not normalized or any(metric not in SUPPORTED_METRICS for metric in normalized):
        raise ValueError("metrics must include supported assay metrics")
    return normalized


@dataclass(frozen=True)
class BenchmarkTask:
    name: str
    estimand: str
    split_unit: str
    metrics: tuple[str, ...]

    @classmethod
    def create(
        cls,
        *,
        name: str,
        estimand: str,
        split_unit: str,
        metrics: Sequence[str],
    ) -> "BenchmarkTask":
        _require_nonempty_text(name, "name")
        if estimand != "single_substitution":
            raise ValueError("primary estimand must be single_substitution")
        if split_unit not in GROUPED_SPLIT_UNITS:
            raise ValueError("split_unit must be grouped by UniProt or cluster")
        return cls(name=name, estimand=estimand, split_unit=split_unit, metrics=_normalize_metrics(metrics))


@dataclass(frozen=True)
class EvaluatorContract:
    metrics: tuple[str, ...]
    aggregation: str
    bootstrap_unit: str

    @classmethod
    def create(
        cls,
        *,
        metrics: Sequence[str],
        aggregation: str,
        bootstrap_unit: str,
    ) -> "EvaluatorContract":
        if aggregation != "assay_first_macro":
            raise ValueError("aggregation must preserve assay-first metrics")
        if bootstrap_unit not in GROUPED_SPLIT_UNITS:
            raise ValueError("bootstrap unit must match a grouped split unit")
        return cls(metrics=_normalize_metrics(metrics), aggregation=aggregation, bootstrap_unit=bootstrap_unit)


@dataclass(frozen=True)
class ModelAdapterContract:
    name: str
    revision: str
    output_dim: int
    requires_checkpoint: bool

    @classmethod
    def create(
        cls,
        *,
        name: str,
        revision: str,
        output_dim: int,
        requires_checkpoint: bool,
    ) -> "ModelAdapterContract":
        _require_nonempty_text(name, "name")
        _require_nonempty_text(revision, "revision")
        if output_dim <= 0:
            raise ValueError("output_dim must be positive")
        return cls(name=name, revision=revision, output_dim=output_dim, requires_checkpoint=bool(requires_checkpoint))


@dataclass(frozen=True)
class FrozenEmbeddingContract:
    model: str
    representation: str
    encoding: str

    @classmethod
    def create(cls, *, model: str, representation: str, encoding: str) -> "FrozenEmbeddingContract":
        _require_nonempty_text(model, "model")
        if representation != "pooled_mutant_minus_wt" or encoding != "independent_wt_mutant":
            raise ValueError("frozen embeddings require independent WT/mutant pooled delta encoding")
        return cls(model=model, representation=representation, encoding=encoding)


@dataclass(frozen=True)
class FineTuningContract:
    method: str
    required_resource: str
    optional: bool
    fallback_stage: str

    @classmethod
    def create(
        cls,
        *,
        method: str,
        required_resource: str,
        optional: bool,
        fallback_stage: str,
    ) -> "FineTuningContract":
        if method != "lora":
            raise ValueError("only the LoRA fine-tuning contract is declared")
        if required_resource != "t4":
            raise ValueError("LoRA requires a T4 resource gate")
        if not optional:
            raise ValueError("LoRA must remain optional")
        _require_nonempty_text(fallback_stage, "fallback_stage")
        return cls(method=method, required_resource=required_resource, optional=True, fallback_stage=fallback_stage)
