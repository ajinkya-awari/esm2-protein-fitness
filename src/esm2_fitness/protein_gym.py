"""ProteinGym v1 single-substitution data acquisition and normalization.

Uses the OATML-Markslab/ProteinGym_v1 HuggingFace dataset (DMS_substitutions config).
Network download is gated: pass allow_network=True only in approved Kaggle sessions.
Never call from local pipeline; the real flag must be set explicitly.
"""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Iterator

PROTEINGYM_RELEASE = "ProteinGym-v1"
HF_DATASET_ID = "OATML-Markslab/ProteinGym_v1"
HF_CONFIG = "DMS_substitutions"
SINGLE_SUB_PATTERN = re.compile(r"^[A-Z]\d+[A-Z]$")


def is_single_substitution(mutant: str) -> bool:
    """Return True iff mutant matches a single amino-acid substitution."""
    return bool(SINGLE_SUB_PATTERN.match(mutant.strip()))


def load_hf_dataset(*, allow_network: bool = False):
    """Load the ProteinGym DMS_substitutions parquet shards from HuggingFace Hub.

    Uses explicit hf:// paths because the dataset card path config is mismatched.
    Returns a HuggingFace Dataset object (train split).
    Raises RuntimeError if allow_network is False.
    """
    if not allow_network:
        raise RuntimeError(
            "load_hf_dataset requires allow_network=True; "
            "set this only in an approved Kaggle session."
        )
    from datasets import load_dataset  # type: ignore[import]
    HF_PARQUET_GLOB = f"hf://datasets/{HF_DATASET_ID}/DMS_substitutions/train-*.parquet"
    print(f"Loading ProteinGym parquets from {HF_PARQUET_GLOB} ...")
    ds = load_dataset("parquet", data_files={"train": HF_PARQUET_GLOB}, split="train")
    print(f"Loaded {len(ds)} rows, columns: {ds.column_names}")
    return ds


# Keep legacy signatures for backward compatibility with notebook cells.
def download_substitutions(dest_dir: Path, *, allow_network: bool = False) -> Path:
    """Stub — data now loaded via load_hf_dataset(); returns dest_dir unchanged."""
    if not allow_network:
        raise RuntimeError(
            "download_substitutions requires allow_network=True; "
            "set this only in an approved Kaggle session."
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    return dest_dir


def download_reference(dest_dir: Path, *, allow_network: bool = False) -> Path:
    """Stub — reference info is embedded in the HF dataset rows."""
    if not allow_network:
        raise RuntimeError(
            "download_reference requires allow_network=True; "
            "set this only in an approved Kaggle session."
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    ref_path = dest_dir / "reference_stub.txt"
    ref_path.write_text("Reference embedded in HF dataset rows.\n", encoding="utf-8")
    return ref_path


def load_reference(ref_path: Path) -> dict[str, dict[str, str]]:
    """Load reference CSV keyed by DMS_id (used in offline synthetic tests)."""
    import csv as _csv
    ref: dict[str, dict[str, str]] = {}
    with ref_path.open(encoding="utf-8") as f:
        for row in _csv.DictReader(f):
            key = row.get("DMS_id", "").strip()
            if key:
                ref[key] = dict(row)
    return ref


def iter_assay_rows_from_hf(ds) -> Iterator[dict[str, object]]:
    """Yield normalized row dicts from a loaded HuggingFace ProteinGym dataset.

    The dataset has columns: mutated_sequence, target_seq, mutant, DMS_score,
    DMS_score_bin, DMS_id.

    Excluded:
    - Multi-site mutants (contain ":")
    - Rows with non-finite DMS scores
    - Rows whose mutant string does not match single-substitution pattern
    - Rows with empty target_seq or mutated_sequence

    Each yielded row contains:
        assay_id, mutation, sequence (WT = target_seq), mutated_sequence,
        fitness, uniprot_id, cluster_id
    """
    for row in ds:
        mutant: str = (row.get("mutant") or "").strip()
        if not mutant or ":" in mutant or not is_single_substitution(mutant):
            continue
        target_seq: str = (row.get("target_seq") or "").strip()
        mutated_seq: str = (row.get("mutated_sequence") or "").strip()
        if not target_seq or not mutated_seq:
            continue
        score_raw = row.get("DMS_score")
        try:
            fitness = float(score_raw)
        except (ValueError, TypeError):
            continue
        if not math.isfinite(fitness):
            continue
        assay_id: str = (row.get("DMS_id") or "").strip()
        if not assay_id:
            continue
        # UniProt_ID not in this HF dataset; use assay_id prefix as group key.
        # Assay IDs are like "BLAT_ECOLX_Stiffler_2015"; use the protein portion.
        uniprot_id = assay_id.split("_")[0] if "_" in assay_id else assay_id
        yield {
            "assay_id": assay_id,
            "mutation": mutant,
            "sequence": target_seq,
            "mutated_sequence": mutated_seq,
            "fitness": fitness,
            "uniprot_id": uniprot_id,
            "cluster_id": uniprot_id,
        }


def iter_assay_rows(
    substitutions_dir: Path,
    reference: dict[str, dict[str, str]],
) -> Iterator[dict[str, object]]:
    """Legacy stub — redirects to iter_assay_rows_from_hf when called without HF ds.

    In offline tests this receives an empty reference and a synthetic fixtures dir;
    it falls back to reading CSV files from that dir.
    """
    import csv as _csv
    if not substitutions_dir.exists():
        raise FileNotFoundError(f"Directory not found: {substitutions_dir}")
    csv_files = sorted(substitutions_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files in {substitutions_dir}")
    for csv_path in csv_files:
        assay_id = csv_path.stem
        ref = reference.get(assay_id, {})
        wt_sequence: str = ref.get("target_seq", "") or ref.get("sequence", "")
        uniprot_id: str = ref.get("UniProt_ID", "") or assay_id
        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = _csv.DictReader(f)
            for row in reader:
                mutant = (row.get("mutant") or "").strip()
                if not mutant or ":" in mutant or not is_single_substitution(mutant):
                    continue
                score_raw = (row.get("DMS_score") or "").strip()
                try:
                    fitness = float(score_raw)
                except (ValueError, TypeError):
                    continue
                if not math.isfinite(fitness):
                    continue
                seq = wt_sequence or (row.get("target_seq") or "").strip()
                mutated_seq = (row.get("mutated_sequence") or "").strip()
                yield {
                    "assay_id": assay_id,
                    "mutation": mutant,
                    "sequence": seq,
                    "mutated_sequence": mutated_seq,
                    "fitness": fitness,
                    "uniprot_id": uniprot_id,
                    "cluster_id": uniprot_id,
                }
