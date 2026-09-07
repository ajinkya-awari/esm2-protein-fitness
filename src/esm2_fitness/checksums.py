"""Checksum manifest helpers for reproducible source and evidence records."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
from pathlib import Path
from collections.abc import Sequence


@dataclass(frozen=True)
class ManifestEntry:
    path: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class ChecksumManifest:
    entries: tuple[ManifestEntry, ...]


def checksum_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _relative_to_root(root: Path, path: Path) -> Path:
    root_resolved = root.resolve()
    path_resolved = path.resolve()
    try:
        return path_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise ValueError(f"path is outside manifest root: {path}") from exc


def create_manifest(root: Path, paths: Sequence[Path]) -> ChecksumManifest:
    entries: list[ManifestEntry] = []
    for path in paths:
        relative = _relative_to_root(root, path)
        if not path.is_file():
            raise ValueError(f"manifest path is not a file: {path}")
        entries.append(
            ManifestEntry(
                path=relative.as_posix(),
                sha256=checksum_file(path),
                size_bytes=path.stat().st_size,
            )
        )
    return ChecksumManifest(entries=tuple(sorted(entries, key=lambda entry: entry.path)))
