import pytest

from esm2_fitness.provenance import Provenance


def test_provenance_records_protocol_revisions_and_environment():
    provenance = Provenance.create(
        protocol="ProteinGym-v1.3",
        split_hash="abc123",
        model_revisions={"esm2": "synthetic-revision"},
        code_revision="local-test-revision",
        environment={"python": "3.11"},
    )

    assert provenance.protocol == "ProteinGym-v1.3"
    assert provenance.model_revisions["esm2"] == "synthetic-revision"


def test_provenance_rejects_missing_revision_fields():
    with pytest.raises(ValueError, match="split_hash"):
        Provenance.create(
            protocol="ProteinGym-v1.3",
            split_hash="",
            model_revisions={"esm2": "synthetic-revision"},
            code_revision="local-test-revision",
            environment={"python": "3.11"},
        )
