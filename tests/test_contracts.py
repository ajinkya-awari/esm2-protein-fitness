import pytest

from esm2_fitness.contracts import (
    BenchmarkTask,
    EvaluatorContract,
    FrozenEmbeddingContract,
    FineTuningContract,
    ModelAdapterContract,
)


def test_benchmark_task_requires_single_substitution_estimand_and_grouped_split():
    task = BenchmarkTask.create(
        name="synthetic-single-substitution",
        estimand="single_substitution",
        split_unit="uniprot_cluster",
        metrics=("spearman", "mse"),
    )

    assert task.estimand == "single_substitution"
    assert task.split_unit == "uniprot_cluster"
    assert task.metrics == ("spearman", "mse")


def test_benchmark_task_rejects_row_level_split():
    with pytest.raises(ValueError, match="grouped"):
        BenchmarkTask.create(
            name="unsafe-row-split",
            estimand="single_substitution",
            split_unit="mutation_row",
            metrics=("spearman",),
        )


def test_evaluator_contract_requires_assay_first_metrics_and_group_bootstrap():
    evaluator = EvaluatorContract.create(
        metrics=("spearman", "mse"),
        aggregation="assay_first_macro",
        bootstrap_unit="uniprot_cluster",
    )

    assert evaluator.aggregation == "assay_first_macro"
    assert evaluator.bootstrap_unit == "uniprot_cluster"


def test_evaluator_contract_rejects_row_bootstrap():
    with pytest.raises(ValueError, match="bootstrap"):
        EvaluatorContract.create(
            metrics=("spearman", "mse"),
            aggregation="assay_first_macro",
            bootstrap_unit="mutation_row",
        )


def test_model_adapter_records_revision_and_output_shape_without_loading_models():
    adapter = ModelAdapterContract.create(
        name="esm2",
        revision="facebook/esm2_t33_650M_UR50D@08e4846e537177426273712802403f7ba8261b6c",
        output_dim=1280,
        requires_checkpoint=True,
    )

    assert adapter.output_dim == 1280
    assert adapter.requires_checkpoint is True


def test_frozen_embedding_contract_requires_independent_delta_strategy():
    contract = FrozenEmbeddingContract.create(
        model="esm2",
        representation="pooled_mutant_minus_wt",
        encoding="independent_wt_mutant",
    )

    assert contract.representation == "pooled_mutant_minus_wt"


def test_frozen_embedding_contract_rejects_concatenation_shortcut():
    with pytest.raises(ValueError, match="independent"):
        FrozenEmbeddingContract.create(
            model="esm2",
            representation="concatenated",
            encoding="paired_concat",
        )


def test_fine_tuning_contract_is_resource_gated_and_optional():
    contract = FineTuningContract.create(
        method="lora",
        required_resource="t4",
        optional=True,
        fallback_stage="frozen_esm2",
    )

    assert contract.optional is True
    assert contract.required_resource == "t4"


def test_fine_tuning_contract_rejects_required_lora():
    with pytest.raises(ValueError, match="optional"):
        FineTuningContract.create(
            method="lora",
            required_resource="t4",
            optional=False,
            fallback_stage="frozen_esm2",
        )
