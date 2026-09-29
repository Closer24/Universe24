"""The world's files for the loader (a host module): this module reads the world file, the universe and engine start files it names by their repository paths and the generator's mode file beside it, and hands the loader the documents with the world's digest; the loader reads no file."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from event_universe.loader.world import World, parse_world

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]


def input_digest(document: dict[str, object]) -> str:
    """THE FILE'S DIGEST: SHA-256 of the canonical JSON (the keys sorted, no spaces, ASCII) of the document, the mode file's `world_digest` of the world it stands beside."""
    canonical = json.dumps(document, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


def world_files(document: object) -> dict[str, object]:
    """The documents a world names by a repository path (the universe file under `universe`, the engine start file under `engine`); a path with no file is left out, and the loader refuses it naming the key."""
    files: dict[str, object] = {}
    if isinstance(document, dict):
        for key in ("universe", "engine"):
            value = document.get(key)
            path = REPOSITORY_ROOT.joinpath(value) if isinstance(value, str) else None
            if path is not None and path.is_file():
                files[str(value)] = json.loads(path.read_text(encoding="utf-8"))
    return files


def load_world(path: Path) -> World:
    """A world file read and parsed, with the generator's mode file beside it (`<world>.mode.json`)."""
    document = json.loads(path.read_text(encoding="utf-8"))
    files = world_files(document)
    beside = path.with_suffix(".mode.json")
    if beside.is_file():
        files[beside.name] = json.loads(beside.read_text(encoding="utf-8"))
    digest = input_digest(document) if isinstance(document, dict) else ""
    return parse_world(document, files, digest)
