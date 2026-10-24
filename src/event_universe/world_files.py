"""The world's files for the loader (a host module): this module reads the world file and the universe file it names by its repository path, and hands the loader the documents with the world's digest; the loader reads no file (the generator's mode file beside the world, read to 2026-10-24, is no input: the generator goes, the owner's word)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from event_universe.loader.world import World, parse_world

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def input_digest(document: dict[str, object]) -> str:
    """The file's digest: SHA-256 of the canonical JSON (the keys sorted, no spaces, ASCII) of the document."""
    canonical = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


def world_files(document: object) -> dict[str, object]:
    """The documents a world names by a repository path (the universe file under `universe`); a path with no file is left out, and the loader refuses it naming the key."""
    files: dict[str, object] = {}
    if isinstance(document, dict):
        value = document.get("universe")
        path = REPOSITORY_ROOT.joinpath(value) if isinstance(value, str) else None
        if path is not None and path.is_file():
            files[str(value)] = json.loads(path.read_text(encoding="utf-8"))
    return files


def load_world(path: Path) -> World:
    """A world file read and parsed with the universe file it names."""
    document = json.loads(path.read_text(encoding="utf-8"))
    files = world_files(document)
    return parse_world(document, files)
