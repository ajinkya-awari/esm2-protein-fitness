import json
from pathlib import Path

from esm2_fitness.metrics import mse_or_status
from esm2_fitness.privacy import check_public_metadata
from esm2_fitness.provenance import Provenance
from esm2_fitness.schema import MutationRow
from esm2_fitness.sequences import parse_substitution, reconstruct_sequences
from esm2_fitness.splits import assign_groups, manifest_hash, validate_group_disjointness


def test_synthetic_fixture_flows_through_all_lightweight_contracts():
    repository = Path(__file__).parents[1]
    fixture = repository / "data_public" / "synthetic_mutations.jsonl"
    rows = [MutationRow.from_mapping(json.loads(line)) for line in fixture.read_text().splitlines()]

    for row in rows:
        wild_type, mutant = reconstruct_sequences(row.sequence, parse_substitution(row.mutation))
        assert wild_type != mutant

    groups = [f"{row.uniprot_id}:{row.cluster_id}" for row in rows]
    assignments = assign_groups(
        groups,
        seed=20260818,
        fractions={"train": 0.6, "validation": 0.2, "test": 0.2},
    )
    validate_group_disjointness([(group, assignments[group]) for group in groups])

    metric = mse_or_status(
        [row.fitness for row in rows],
        [row.fitness + 0.1 for row in rows],
        "synthetic-macro",
    )
    provenance = Provenance.create(
        protocol="ProteinGym-v1.3-synthetic",
        split_hash=manifest_hash(assignments),
        model_revisions={"esm2": "not-run"},
        code_revision="synthetic-test",
        environment={"python": "test"},
    )
    check_public_metadata(
        {
            "protocol": provenance.protocol,
            "split_hash": provenance.split_hash,
            "assay_count": 3,
            "mse": metric.value,
        }
    )

    assert len(rows) == 5
    assert metric.status == "completed"
    assert len(provenance.split_hash) == 64
