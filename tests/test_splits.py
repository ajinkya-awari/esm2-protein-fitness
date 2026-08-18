import pytest

from esm2_fitness.splits import assign_groups, manifest_hash, validate_group_disjointness


FRACTIONS = {"train": 0.6, "validation": 0.2, "test": 0.2}


def test_assign_groups_is_deterministic_for_same_seed():
    groups = [f"group-{index:02d}" for index in range(20)]

    first = assign_groups(groups, seed=17, fractions=FRACTIONS)
    second = assign_groups(groups, seed=17, fractions=FRACTIONS)

    assert first == second


def test_assign_groups_keeps_every_group_in_one_partition():
    groups = ["group-a", "group-a", "group-b", "group-c"]

    assignments = assign_groups(groups, seed=17, fractions=FRACTIONS)

    assert set(assignments) == {"group-a", "group-b", "group-c"}
    validate_group_disjointness([(group, assignments[group]) for group in groups])


def test_group_disjointness_rejects_cross_partition_group():
    with pytest.raises(ValueError, match="group-a"):
        validate_group_disjointness([("group-a", "train"), ("group-a", "test")])


def test_manifest_hash_is_stable_and_changes_with_assignment():
    assignments = {"group-a": "train", "group-b": "test"}

    assert manifest_hash(assignments) == manifest_hash(dict(reversed(list(assignments.items()))))
    assert manifest_hash(assignments) != manifest_hash({"group-a": "test", "group-b": "train"})


def test_invalid_fractions_are_rejected():
    with pytest.raises(ValueError, match="fractions"):
        assign_groups(["group-a"], seed=17, fractions={"train": 1.2, "test": -0.2})
