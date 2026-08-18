"""Deterministic group assignment and manifest integrity helpers."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import math


def _validate_fractions(fractions: Mapping[str, float]) -> tuple[tuple[str, float], ...]:
    if not fractions or any(not name or value <= 0 for name, value in fractions.items()):
        raise ValueError("fractions must contain positive named partitions")
    total = sum(float(value) for value in fractions.values())
    if not math.isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-9):
        raise ValueError("fractions must sum to 1")
    return tuple(sorted((name, float(value)) for name, value in fractions.items()))


def assign_groups(
    group_keys: Sequence[str], seed: int, fractions: Mapping[str, float]
) -> dict[str, str]:
    """Assign each unique group to one partition using stable hash buckets."""

    partitions = _validate_fractions(fractions)
    groups = sorted(set(group_keys))
    if any(not isinstance(group, str) or not group for group in groups):
        raise ValueError("group keys must be non-empty strings")

    assignments: dict[str, str] = {}
    for group in groups:
        digest = hashlib.sha256(f"{seed}:{group}".encode("utf-8")).digest()
        bucket = int.from_bytes(digest[:8], "big") / 2**64
        cumulative = 0.0
        for partition, fraction in partitions:
            cumulative += fraction
            if bucket < cumulative:
                assignments[group] = partition
                break
        else:
            assignments[group] = partitions[-1][0]
    return assignments


def validate_group_disjointness(observations: Sequence[tuple[str, str]]) -> None:
    """Prove that one group is associated with only one partition."""

    seen: dict[str, str] = {}
    for group, partition in observations:
        if not group or not partition:
            raise ValueError("group and partition must be non-empty")
        previous = seen.setdefault(group, partition)
        if previous != partition:
            raise ValueError(f"group {group} crosses partitions")


def manifest_hash(assignments: Mapping[str, str]) -> str:
    """Hash a canonical group-to-partition manifest."""

    lines = [f"{group}\t{partition}" for group, partition in sorted(assignments.items())]
    return hashlib.sha256("\n".join(lines).encode("utf-8")).hexdigest()
