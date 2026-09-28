"""The world's files for the engine's loader (a host module): the loader reads no file and computes no digest; this module reads the world file, the universe and start files it names, and the step file, and hands the loader the documents with the stamp's digest (ALGEBRA.md #the-primitives, #a-familys-declaration)."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from event_universe.core.step import STEP_FILE, read_step
from event_universe.loader.world import NatureBeamWorld, parse_world_document

# the mode file's exact fractions carry the well's digits, not the host's cap on an integer's string
sys.set_int_max_str_digits(0)
REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
LAW_ROOT = Path(__file__).resolve().parents[2]


def read_repository_json(value: str) -> object | None:
    """The JSON document at the repository path `value`, or None where there is no file."""
    path = REPOSITORY_ROOT / value
    if not path.is_file():
        return None
    read: object = json.loads(path.read_text(encoding="utf-8"))
    return read


def input_digest(document: dict[str, object]) -> str:
    """THE FILE'S DIGEST (ALGEBRA.md #a-familys-declaration; the stamp over the whole file): SHA-256 of the canonical JSON (the keys sorted, no spaces, ASCII) of the document without its `stamp` key, the same from the raw document (`input_stamp`) and at load, so that a file changed by hand is refused."""
    canonical = json.dumps(
        {key: value for key, value in document.items() if key != "stamp"},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


def input_stamp(document: dict[str, object]) -> dict[str, str]:
    """THE STAMP the generator writes into a world file under `stamp` (ALGEBRA.md #a-familys-declaration): the digest of the whole document and nothing else; the loader compares it with the digest computed at load."""
    return {"hash": input_digest(document)}


def world_files(document: object) -> dict[str, object]:
    """The documents a world names by a repository path (the universe file under `universe`, the start file under `engine`) and the step file from the law's own root (LAW_ROOT: the repository's, whichever root a test redirects the world's files to), by their paths; a path with no file is left out (the loader refuses it naming the key)."""
    files: dict[str, object] = {}
    if isinstance(document, dict):
        for key in ("universe", "engine"):
            value = document.get(key)
            if isinstance(value, str):
                read = read_repository_json(value)
                if read is not None:
                    files[value] = read
    path = LAW_ROOT / STEP_FILE
    step = json.loads(path.read_text(encoding="utf-8")) if path.is_file() else None
    if isinstance(step, dict):
        files[STEP_FILE] = read_step(step, input_digest(step))
    return files


def parse_nature_beam_world(document: object) -> NatureBeamWorld:
    """The world parsed from its document: the files it names read here, the stamp's digest computed here, every check the loader's."""
    digest = input_digest(document) if isinstance(document, dict) else None
    return parse_world_document(document, world_files(document), digest)


def load_world(path: Path) -> NatureBeamWorld:
    """A world file read and parsed, the generator's mode file beside it (`<world>.mode.json`) handed with the files."""
    document = json.loads(path.read_text(encoding="utf-8"))
    files = world_files(document)
    beside = path.with_suffix(".mode.json")
    if beside.is_file():
        files[beside.name] = json.loads(beside.read_text(encoding="utf-8"))
    digest = input_digest(document) if isinstance(document, dict) else None
    return parse_world_document(document, files, digest)
