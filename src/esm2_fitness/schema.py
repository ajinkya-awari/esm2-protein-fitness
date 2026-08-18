"""Validation contracts for lightweight mutation-fitness rows."""

from __future__ import annotations

from dataclasses import dataclass
import math
import re
from typing import Mapping


AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWY")
SUBSTITUTION_PATTERN = re.compile(r"^(?P<wt>[A-Z])(?P<position>[1-9][0-9]*)(?P<mutant>[A-Z])$")


@dataclass(frozen=True)
class MutationRow:
    """A validated single-substitution assay observation."""

    assay_id: str
    uniprot_id: str
    sequence: str
    mutation: str
    fitness: float
    cluster_id: str

    @classmethod
    def from_mapping(cls, mapping: Mapping[str, object]) -> "MutationRow":
        required = ("assay_id", "uniprot_id", "sequence", "mutation", "fitness", "cluster_id")
        for field in required:
            if field not in mapping:
                raise ValueError(f"missing required field: {field}")

        values = {field: mapping[field] for field in required}
        for field in ("assay_id", "uniprot_id", "sequence", "mutation", "cluster_id"):
            if not isinstance(values[field], str) or not values[field]:
                raise ValueError(f"invalid {field}")

        sequence = values["sequence"]
        if any(residue not in AMINO_ACIDS for residue in sequence):
            raise ValueError("invalid sequence")

        mutation = values["mutation"]
        match = SUBSTITUTION_PATTERN.fullmatch(mutation)
        if match is None:
            raise ValueError("invalid mutation")
        wt = match.group("wt")
        mutant = match.group("mutant")
        position = int(match.group("position"))
        if wt not in AMINO_ACIDS or mutant not in AMINO_ACIDS or wt == mutant:
            raise ValueError("invalid mutation")
        if position > len(sequence):
            raise ValueError("mutation position is outside sequence")
        if sequence[position - 1] != wt:
            raise ValueError("mutation WT residue does not match sequence")

        fitness = values["fitness"]
        if isinstance(fitness, bool) or not isinstance(fitness, (int, float)):
            raise ValueError("invalid fitness")
        fitness_value = float(fitness)
        if not math.isfinite(fitness_value):
            raise ValueError("invalid fitness")

        return cls(
            assay_id=values["assay_id"],
            uniprot_id=values["uniprot_id"],
            sequence=sequence,
            mutation=mutation,
            fitness=fitness_value,
            cluster_id=values["cluster_id"],
        )
