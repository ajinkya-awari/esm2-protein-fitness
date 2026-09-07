import pytest

from esm2_fitness.explainability import ExplainabilityReport


def test_explainability_report_is_exploratory_and_sanitized():
    report = ExplainabilityReport.create(
        method="umap",
        scope="exploratory",
        inputs=("sanitized_aggregate_summary",),
        claims=("visual audit of synthetic aggregate behavior",),
    )

    assert report.scope == "exploratory"
    assert report.inputs == ("sanitized_aggregate_summary",)


def test_explainability_report_rejects_raw_sequences_or_embeddings():
    with pytest.raises(ValueError, match="restricted"):
        ExplainabilityReport.create(
            method="umap",
            scope="exploratory",
            inputs=("embeddings",),
            claims=("visual audit",),
        )


def test_explainability_report_rejects_biological_or_clinical_claims():
    with pytest.raises(ValueError, match="claim"):
        ExplainabilityReport.create(
            method="umap",
            scope="exploratory",
            inputs=("sanitized_aggregate_summary",),
            claims=("proves clinical utility",),
        )
