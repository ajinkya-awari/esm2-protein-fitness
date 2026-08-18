"""Single-substitution parsing and sequence reconstruction proofs."""

from __future__ import annotations

from dataclasses import dataclass
import re


AMINO_ACIDS = frozenset("ACDEFGHIKLMNPQRSTVWY")
SUBSTITUTION_PATTERN = re.compile(r"^(?P<wt>[A-Z])(?P<position>[1-9][0-9]*)(?P<mutant>[A-Z])$")


@dataclass(frozen=True)
class Substitution:
    wt: str
    position: int
    mutant: str


def parse_substitution(mutation: str) -> Substitution:
    match = SUBSTITUTION_PATTERN.fullmatch(mutation)
    if match is None:
        raise ValueError(f"invalid mutation notation: {mutation}")

    wt = match.group("wt")
    mutant = match.group("mutant")
    if wt not in AMINO_ACIDS or mutant not in AMINO_ACIDS or wt == mutant:
        raise ValueError(f"invalid mutation notation: {mutation}")

    return Substitution(wt=wt, position=int(match.group("position")), mutant=mutant)


def reconstruct_sequences(sequence: str, substitution: Substitution) -> tuple[str, str]:
    if not sequence or any(residue not in AMINO_ACIDS for residue in sequence):
        raise ValueError("invalid sequence")
    if substitution.position > len(sequence):
        raise ValueError("mutation position is outside sequence")
    index = substitution.position - 1
    if sequence[index] != substitution.wt:
        raise ValueError("mutation WT residue does not match sequence")

    wild_type = sequence
    mutant = sequence[:index] + substitution.mutant + sequence[index + 1 :]
    if sum(left != right for left, right in zip(wild_type, mutant)) != 1:
        raise ValueError("reconstruction did not change exactly one residue")
    return wild_type, mutant
