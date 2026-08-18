import pytest

from esm2_fitness.sequences import parse_substitution, reconstruct_sequences


def test_parse_substitution_exposes_one_based_position():
    substitution = parse_substitution("C2W")

    assert substitution.wt == "C"
    assert substitution.position == 2
    assert substitution.mutant == "W"


@pytest.mark.parametrize("mutation", ["A0V", "A1", "AA1V", "A1*", "A1A"])
def test_parse_substitution_rejects_invalid_notation(mutation: str):
    with pytest.raises(ValueError, match="mutation"):
        parse_substitution(mutation)


def test_reconstruct_sequences_changes_exactly_the_declared_residue():
    substitution = parse_substitution("A1V")

    wild_type, mutant = reconstruct_sequences("ACDE", substitution)

    assert wild_type == "ACDE"
    assert mutant == "VCDE"
    assert sum(left != right for left, right in zip(wild_type, mutant)) == 1


def test_reconstruct_sequences_supports_last_position():
    wild_type, mutant = reconstruct_sequences("ACDE", parse_substitution("E4W"))

    assert wild_type == "ACDE"
    assert mutant == "ACDW"


def test_reconstruct_sequences_rejects_wt_mismatch():
    with pytest.raises(ValueError, match="WT"):
        reconstruct_sequences("ACDE", parse_substitution("G2W"))
