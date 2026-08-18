"""Structured stage outcomes for optional or unavailable compute."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StageStatus:
    stage: str
    status: str
    reason: str
    resource: str

    @classmethod
    def skipped(cls, stage: str, reason: str, resource: str) -> "StageStatus":
        if not stage or not reason or not resource:
            raise ValueError("stage, reason, and resource are required")
        return cls(stage=stage, status="skipped", reason=reason, resource=resource)
