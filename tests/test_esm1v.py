import pytest

from esm2_fitness.esm1v import (
    OFFICIAL_CHECKPOINTS,
    score_masked_marginal,
    score_with_official_checkpoints,
    validate_official_checkpoints,
)


def test_official_esm1v_contract_contains_five_ordered_checkpoints():
    assert len(OFFICIAL_CHECKPOINTS) == 5
    assert validate_official_checkpoints(OFFICIAL_CHECKPOINTS) == OFFICIAL_CHECKPOINTS


def test_official_esm1v_contract_rejects_missing_checkpoint():
    with pytest.raises(ValueError, match="five"):
        validate_official_checkpoints(OFFICIAL_CHECKPOINTS[:-1])


def test_masked_marginal_score_is_mutant_minus_wild_type_log_probability():
    assert score_masked_marginal(-2.0, -1.25) == pytest.approx(0.75)


def test_parity_harness_calls_each_official_checkpoint_once():
    calls: list[str] = []

    def fake_score(checkpoint: str) -> float:
        calls.append(checkpoint)
        return float(len(calls))

    result = score_with_official_checkpoints(fake_score)

    assert calls == list(OFFICIAL_CHECKPOINTS)
    assert result.checkpoint_scores == {name: float(index) for index, name in enumerate(OFFICIAL_CHECKPOINTS, 1)}
    assert result.mean_score == pytest.approx(3.0)
