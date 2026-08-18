"""Resource-only gates for optional T4 LoRA execution."""

from __future__ import annotations

from collections.abc import Sequence

from .status import StageStatus


def evaluate_lora_gate(
    *,
    t4_available: bool,
    vram_gb: float,
    required_vram_gb: float,
    target_modules: Sequence[str],
    required_target_modules: Sequence[str],
    expected_output_dim: int,
    actual_output_dim: int,
) -> StageStatus:
    if not t4_available:
        return StageStatus.skipped("lora", "T4 GPU unavailable", "t4")
    if vram_gb < required_vram_gb:
        return StageStatus.skipped("lora", "insufficient VRAM", "t4")
    if set(target_modules) != set(required_target_modules):
        return StageStatus.skipped("lora", "target modules mismatch", "t4")
    if actual_output_dim != expected_output_dim:
        return StageStatus.skipped("lora", "output shape mismatch", "t4")
    return StageStatus(stage="lora", status="ready", reason="all resource and shape gates passed", resource="t4")
