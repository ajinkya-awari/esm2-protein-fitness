"""Small command dispatcher with fail-closed compute and network gates."""

from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path
from typing import Sequence

from .schema import MutationRow
from .sequences import parse_substitution, reconstruct_sequences
from .splits import assign_groups, validate_group_disjointness
from .status import StageStatus


FRACTIONS = {"train": 0.6, "validation": 0.2, "test": 0.2}


def _fixture_path() -> Path:
    return Path(__file__).resolve().parents[2] / "data_public" / "synthetic_mutations.jsonl"


def _load_synthetic_rows() -> list[MutationRow]:
    rows: list[MutationRow] = []
    for line in _fixture_path().read_text(encoding="utf-8").splitlines():
        rows.append(MutationRow.from_mapping(json.loads(line)))
    return rows


def _run_check() -> int:
    print("offline lightweight checks available")
    return 0


def _run_synthetic() -> int:
    rows = _load_synthetic_rows()
    for row in rows:
        reconstruct_sequences(row.sequence, parse_substitution(row.mutation))
    groups = [f"{row.uniprot_id}:{row.cluster_id}" for row in rows]
    assignments = assign_groups(groups, seed=20260818, fractions=FRACTIONS)
    validate_group_disjointness([(group, assignments[group]) for group in groups])
    print(f"synthetic offline flow validated {len(rows)} rows")
    return 0


def _run_real(data_dir: str | None, allow_external_data: bool) -> int:
    if not allow_external_data:
        status = StageStatus.skipped(
            "real-data",
            "explicit --allow-external-data is required; no retrieval is performed",
            "network/data",
        )
        print(json.dumps(asdict(status), sort_keys=True))
        return 2
    if data_dir is None or not Path(data_dir).is_dir():
        status = StageStatus.skipped("real-data", "approved local data directory is unavailable", "local-data")
        print(json.dumps(asdict(status), sort_keys=True))
        return 2
    status = StageStatus.skipped(
        "real-data",
        "heavy data/model stages are disabled in the local command; use an approved Kaggle or Colab runner",
        "kaggle-or-colab",
    )
    print(json.dumps(asdict(status), sort_keys=True))
    return 2


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline-safe Project 15 pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("check", help="run lightweight offline checks")
    subparsers.add_parser("synthetic", help="run independent synthetic fixture flow")
    real = subparsers.add_parser("real", help="gate real-data/model stages")
    real.add_argument("--data-dir")
    real.add_argument("--allow-external-data", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "check":
        return _run_check()
    if args.command == "synthetic":
        return _run_synthetic()
    return _run_real(args.data_dir, args.allow_external_data)


if __name__ == "__main__":
    raise SystemExit(main())
