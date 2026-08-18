"""Run provenance contracts with explicit protocol and revision metadata."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class Provenance:
    protocol: str
    split_hash: str
    model_revisions: dict[str, str]
    code_revision: str
    environment: dict[str, str]

    @classmethod
    def create(
        cls,
        protocol: str,
        split_hash: str,
        model_revisions: Mapping[str, str],
        code_revision: str,
        environment: Mapping[str, str],
    ) -> "Provenance":
        if not protocol or not split_hash or not code_revision:
            raise ValueError("protocol, split_hash, and code_revision are required")
        if not model_revisions or not all(model_revisions.values()):
            raise ValueError("model_revisions are required")
        if not environment or not all(environment.values()):
            raise ValueError("environment is required")
        return cls(
            protocol=protocol,
            split_hash=split_hash,
            model_revisions=dict(model_revisions),
            code_revision=code_revision,
            environment=dict(environment),
        )
