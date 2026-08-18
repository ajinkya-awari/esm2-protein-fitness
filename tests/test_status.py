from esm2_fitness.status import StageStatus


def test_skipped_stage_is_structured_and_explicit():
    status = StageStatus.skipped("lora", "T4 GPU unavailable", "t4")

    assert status.status == "skipped"
    assert status.stage == "lora"
    assert status.reason == "T4 GPU unavailable"
    assert status.resource == "t4"
