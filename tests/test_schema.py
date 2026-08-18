import math
import json
from pathlib import Path

import pytest

from esm2_fitness.schema import MutationRow


def valid_mapping() -> dict[str, object]:
    return {
        "assay_id": "synthetic-assay-01",
        "uniprot_id": "SYNTHETIC01",
        "sequence": "ACDEFGHIKLMNPQRSTVWY",
        "mutation": "A1V",
        "fitness": 0.25,
        "cluster_id": "cluster-01",
    }


def test_valid_mapping_creates_a_mutation_row():
    row = MutationRow.from_mapping(valid_mapping())

    assert row.assay_id == "synthetic-assay-01"
    assert row.mutation == "A1V"
    assert row.fitness == 0.25


@pytest.mark.parametrize("field", ["assay_id", "uniprot_id", "sequence", "mutation", "fitness"])
def test_missing_required_field_is_rejected(field: str):
    mapping = valid_mapping()
    del mapping[field]

    with pytest.raises(ValueError, match=field):
        MutationRow.from_mapping(mapping)


@pytest.mark.parametrize("mutation", ["A0V", "A21V", "AA1V", "A1", "A1*", "A1A"])
def test_invalid_mutation_is_rejected(mutation: str):
    mapping = valid_mapping()
    mapping["mutation"] = mutation

    with pytest.raises(ValueError, match="mutation"):
        MutationRow.from_mapping(mapping)


@pytest.mark.parametrize("fitness", [math.nan, math.inf, -math.inf])
def test_non_finite_fitness_is_rejected(fitness: float):
    mapping = valid_mapping()
    mapping["fitness"] = fitness

    with pytest.raises(ValueError, match="fitness"):
        MutationRow.from_mapping(mapping)


def test_invalid_identifier_is_rejected():
    mapping = valid_mapping()
    mapping["assay_id"] = ""

    with pytest.raises(ValueError, match="assay_id"):
        MutationRow.from_mapping(mapping)


def test_independent_fixture_contains_only_valid_rows():
    fixture = Path(__file__).parents[1] / "data_public" / "synthetic_mutations.jsonl"

    rows = [MutationRow.from_mapping(json.loads(line)) for line in fixture.read_text().splitlines()]

    assert len(rows) == 5
