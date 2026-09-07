"""ProteinGym v1.3 single-substitution data acquisition and normalization.

Network download is gated: pass allow_network=True only in approved Kaggle sessions.
Never call from local pipeline; the real flag must be set explicitly.
"""

from __future__ import annotations

import csv
import math
import re
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterator

PROTEINGYM_RELEASE = "ProteinGym-v1.3"
SUBSTITUTIONS_URL = (
    "https://marks.hms.harvard.edu/proteingym/DMS_ProteinGym_substitutions.zip"
)
REFERENCE_URL = (
    "https://raw.githubusercontent.com/OATML-Markslab/ProteinGym/"
    "main/reference_files/DMS_substitutions.csv"
)
SINGLE_SUB_PATTERN = re.compile(r"^[A-Z]\d+[A-Z]$")


def download_substitutions(dest_dir: Path, *, allow_network: bool = False) -> Path:
    """Download and unzip ProteinGym v1.3 single-substitution CSVs."""
    if not allow_network:
        raise RuntimeError(
            "download_substitutions requires allow_network=True; "
            "set this only in an approved Kaggle session."
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / "DMS_ProteinGym_substitutions.zip"
    print(f"Downloading {SUBSTITUTIONS_URL} → {zip_path}")
    urllib.request.urlretrieve(SUBSTITUTIONS_URL, zip_path)
    extract_dir = dest_dir / "DMS_substitutions"
    print(f"Extracting to {extract_dir}")
    with zipfile.ZipFile(zip_path) as zf:
        zf.extractall(extract_dir)
    return extract_dir


def download_reference(dest_dir: Path, *, allow_network: bool = False) -> Path:
    """Download the per-assay reference CSV (UniProt IDs, WT sequences, etc.)."""
    if not allow_network:
        raise RuntimeError(
            "download_reference requires allow_network=True; "
            "set this only in an approved Kaggle session."
        )
    dest_dir.mkdir(parents=True, exist_ok=True)
    ref_path = dest_dir / "DMS_substitutions_reference.csv"
    print(f"Downloading reference → {ref_path}")
    urllib.request.urlretrieve(REFERENCE_URL, ref_path)
    return ref_path


def load_reference(ref_path: Path) -> dict[str, dict[str, str]]:
    """Load reference CSV keyed by DMS_id."""
    ref: dict[str, dict[str, str]] = {}
    with ref_path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            key = row.get("DMS_id", "").strip()
            if key:
                ref[key] = dict(row)
    return ref


def is_single_substitution(mutant: str) -> bool:
    """Return True iff mutant matches a single amino-acid substitution."""
    return bool(SINGLE_SUB_PATTERN.match(mutant.strip()))


def iter_assay_rows(
    substitutions_dir: Path,
    reference: dict[str, dict[str, str]],
) -> Iterator[dict[str, object]]:
    """Yield normalized row dicts for all single-substitution assay CSVs.

    Excluded:
    - Multi-site mutants (contain ":")
    - Rows with non-finite DMS scores
    - Rows whose mutant string does not match single-substitution pattern

    Each yielded row contains:
        assay_id, mutation, sequence (WT), fitness, uniprot_id, cluster_id
    """
    csv_files = sorted(substitutions_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files in {substitutions_dir}")
    for csv_path in csv_files:
        assay_id = csv_path.stem
        ref = reference.get(assay_id, {})
        wt_sequence: str = ref.get("target_seq", "") or ref.get("sequence", "")
        uniprot_id: str = ref.get("UniProt_ID", "") or assay_id
        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
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
                yield {
                    "assay_id": assay_id,
                    "mutation": mutant,
                    "sequence": wt_sequence,
                    "fitness": fitness,
                    "uniprot_id": uniprot_id,
                    "cluster_id": uniprot_id,
                }
