from esm2_fitness.resources import evaluate_lora_gate


def test_lora_is_skipped_without_t4():
    result = evaluate_lora_gate(
        t4_available=False,
        vram_gb=0.0,
        required_vram_gb=12.0,
        target_modules=("q_proj", "v_proj"),
        required_target_modules=("q_proj", "v_proj"),
        expected_output_dim=4,
        actual_output_dim=4,
    )

    assert result.status == "skipped"
    assert result.resource == "t4"
    assert result.reason == "T4 GPU unavailable"


def test_lora_gate_requires_vram_target_modules_and_shape():
    result = evaluate_lora_gate(
        t4_available=True,
        vram_gb=8.0,
        required_vram_gb=12.0,
        target_modules=("q_proj", "v_proj"),
        required_target_modules=("q_proj", "v_proj"),
        expected_output_dim=4,
        actual_output_dim=4,
    )

    assert result.status == "skipped"
    assert result.reason == "insufficient VRAM"


def test_lora_gate_is_ready_only_when_all_checks_pass():
    result = evaluate_lora_gate(
        t4_available=True,
        vram_gb=16.0,
        required_vram_gb=12.0,
        target_modules=("q_proj", "v_proj"),
        required_target_modules=("q_proj", "v_proj"),
        expected_output_dim=4,
        actual_output_dim=4,
    )

    assert result.status == "ready"
    assert result.resource == "t4"


def test_lora_gate_rejects_wrong_target_modules():
    result = evaluate_lora_gate(
        t4_available=True,
        vram_gb=16.0,
        required_vram_gb=12.0,
        target_modules=("dense",),
        required_target_modules=("q_proj", "v_proj"),
        expected_output_dim=4,
        actual_output_dim=4,
    )

    assert result.status == "skipped"
    assert result.reason == "target modules mismatch"


def test_lora_gate_rejects_wrong_output_shape():
    result = evaluate_lora_gate(
        t4_available=True,
        vram_gb=16.0,
        required_vram_gb=12.0,
        target_modules=("q_proj", "v_proj"),
        required_target_modules=("q_proj", "v_proj"),
        expected_output_dim=4,
        actual_output_dim=3,
    )

    assert result.status == "skipped"
    assert result.reason == "output shape mismatch"
