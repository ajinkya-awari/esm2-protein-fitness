from pathlib import Path

import pytest

from esm2_fitness.checksums import checksum_file, create_manifest


def test_checksum_file_returns_sha256_for_small_public_file(tmp_path: Path):
    source = tmp_path / "summary.json"
    source.write_text('{"assay_count": 3}\n', encoding="utf-8")

    digest = checksum_file(source)

    assert len(digest) == 64
    assert digest == checksum_file(source)


def test_create_manifest_records_relative_paths_sizes_and_hashes(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / "configs").mkdir()
    (root / "configs" / "synthetic.yaml").write_text("seed: 1\n", encoding="utf-8")
    (root / "README.md").write_text("safe docs\n", encoding="utf-8")

    manifest = create_manifest(root, [root / "README.md", root / "configs" / "synthetic.yaml"])

    assert [entry.path for entry in manifest.entries] == ["README.md", "configs/synthetic.yaml"]
    assert all(entry.sha256 and entry.size_bytes > 0 for entry in manifest.entries)


def test_create_manifest_rejects_paths_outside_root(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("nope\n", encoding="utf-8")

    with pytest.raises(ValueError, match="outside manifest root"):
        create_manifest(root, [outside])
