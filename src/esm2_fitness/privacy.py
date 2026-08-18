"""Fail-closed checks for artifacts entering public result paths."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any


RESTRICTED_PATH_PARTS = frozenset(
    {
        "artifacts_restricted",
        "data_restricted",
        "sequences",
        "embeddings",
        "checkpoints",
        "hidden_predictions",
        "caches",
        "fitted_artifacts",
    }
)
RESTRICTED_METADATA_KEYS = frozenset(
    {
        "raw_rows",
        "raw_data",
        "sequence",
        "sequences",
        "embedding",
        "embeddings",
        "checkpoint",
        "checkpoints",
        "hidden_prediction",
        "hidden_predictions",
        "cache",
        "caches",
        "fitted_artifact",
        "fitted_artifacts",
    }
)


def check_public_path(path: Path) -> None:
    normalized = {part.casefold() for part in path.parts}
    restricted = normalized.intersection(RESTRICTED_PATH_PARTS)
    if restricted:
        raise ValueError(f"restricted artifact path: {sorted(restricted)[0]}")


def _check_metadata_value(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if not isinstance(key, str) or key.casefold() in RESTRICTED_METADATA_KEYS:
                raise ValueError("restricted metadata key")
            _check_metadata_value(nested)
        return
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for nested in value:
            _check_metadata_value(nested)
        return
    if value is None or isinstance(value, (str, int, float, bool)):
        return
    raise ValueError("unsupported public metadata value")


def check_public_metadata(metadata: Mapping[str, object]) -> None:
    _check_metadata_value(metadata)
