"""Offline contract tests for protein_gym.py (no network, no real data)."""

import pytest
from esm2_fitness.protein_gym import is_single_substitution, load_reference, iter_assay_rows
from pathlib import Path
import csv, tempfile, os


def test_single_sub_valid():
    assert is_single_substitution("A1V")
    assert is_single_substitution("M123L")
    assert is_single_substitution("G99A")


def test_single_sub_invalid():
    assert not is_single_substitution("A1V:G2T")   # multi-site
    assert not is_single_substitution("")
    assert not is_single_substitution("1AV")        # no leading AA
    assert not is_single_substitution("A1")         # no target AA


def test_download_gated():
    from esm2_fitness.protein_gym import download_substitutions, download_reference
    with pytest.raises(RuntimeError, match="allow_network"):
        download_substitutions(Path("/tmp/x"))
    with pytest.raises(RuntimeError, match="allow_network"):
        download_reference(Path("/tmp/x"))


def test_iter_assay_rows_synthetic(tmp_path):
    """iter_assay_rows yields correct rows from a synthetic assay CSV."""
    ref_path = tmp_path / "ref.csv"
    ref_path.write_text(
        "DMS_id,UniProt_ID,target_seq\nSYN_TEST,P12345,ACDEFGHIKLM\n",
        encoding="utf-8",
    )
    reference = load_reference(ref_path)

    assay_dir = tmp_path / "substitutions"
    assay_dir.mkdir()
    csv_path = assay_dir / "SYN_TEST.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["mutant", "DMS_score", "mutated_sequence"])
        writer.writeheader()
        writer.writerow({"mutant": "A1C", "DMS_score": "0.5", "mutated_sequence": "CCDEFGHIKLM"})
        writer.writerow({"mutant": "A1V:G2T", "DMS_score": "0.9", "mutated_sequence": ""})  # multi-site, excluded
        writer.writerow({"mutant": "D3E", "DMS_score": "nan", "mutated_sequence": ""})       # non-finite, excluded
        writer.writerow({"mutant": "F6I", "DMS_score": "-0.3", "mutated_sequence": "ACDEIGHIKLM"})

    rows = list(iter_assay_rows(assay_dir, reference))
    assert len(rows) == 2
    assert rows[0]["mutation"] == "A1C"
    assert rows[0]["fitness"] == pytest.approx(0.5)
    assert rows[0]["uniprot_id"] == "P12345"
    assert rows[1]["mutation"] == "F6I"


def test_iter_assay_rows_no_csvs(tmp_path):
    with pytest.raises(FileNotFoundError):
        list(iter_assay_rows(tmp_path / "empty", {}))
