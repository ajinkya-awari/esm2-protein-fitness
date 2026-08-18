from pathlib import Path

import pytest

from esm2_fitness.privacy import check_public_metadata, check_public_path


def test_sanitized_summary_path_is_allowed():
    check_public_path(Path("results_public/summary.json"))


@pytest.mark.parametrize(
    "path",
    [
        "results_public/sequences/row.json",
        "results_public/embeddings/features.json",
        "results_public/checkpoints/model.bin",
        "results_public/hidden_predictions/predictions.json",
        "results_public/caches/cache.json",
        "results_public/fitted_artifacts/model.json",
    ],
)
def test_restricted_artifact_path_is_rejected(path: str):
    with pytest.raises(ValueError, match="restricted"):
        check_public_path(Path(path))


def test_restricted_metadata_is_rejected():
    with pytest.raises(ValueError, match="restricted"):
        check_public_metadata({"assay_count": 3, "sequences": ["ACDE"]})


def test_sanitized_metadata_is_allowed():
    check_public_metadata(
        {
            "protocol": "synthetic",
            "assay_count": 3,
            "macro_spearman": 0.25,
            "failure_count": 0,
        }
    )
