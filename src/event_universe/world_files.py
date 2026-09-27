"""The world's files for the engine's loader (a host module): the loader reads no file and computes no digest; this module reads the world file, the universe and start files it names, and the step file, and hands the loader the documents with the stamp's digest (ALGEBRA.md #the-primitives, #a-familys-declaration)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from event_universe.core.step import STEP_FILE, read_step
from event_universe.loader.world import NatureBeamWorld, parse_world_document

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
    """THE FILE'S DIGEST (ALGEBRA.md #a-familys-declaration; the model owner's rule of
    2026-09-25 through the Boss, BUILD.md section 26 item 28: the stamp over
    the whole file): SHA-256 of the canonical JSON (the keys sorted, no
    spaces, ASCII) of the document without its `stamp` key; the same from
    the raw document (`input_stamp`) and at load (the loader's stamp check),
    so that a file the generator wrote runs as written and a file changed by
    hand, in any key, is refused."""
    canonical = json.dumps(
        {key: value for key, value in document.items() if key != "stamp"},
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(canonical.encode("ascii")).hexdigest()


def input_stamp(document: dict[str, object]) -> dict[str, str]:
    """THE STAMP the generator writes into a world file under `stamp` (record 1886;
    ALGEBRA.md #a-familys-declaration, #the-primitives; BUILD.md section 26 item 28): the
    digest of the whole document (`input_digest`) and nothing else (no law
    identifier, ALGEBRA.md #the-primitives). The loader compares it with the digest this module
    computes at load and refuses a file that is not the one the generator wrote."""
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
    """The world parsed from its document: the files it names read here, the
    stamp's digest computed here, every check the loader's."""
    digest = input_digest(document) if isinstance(document, dict) else None
    return parse_world_document(document, world_files(document), digest)


def load_world(path: Path) -> NatureBeamWorld:
    """A world file read and parsed (the one command's read)."""
    return parse_nature_beam_world(json.loads(path.read_text(encoding="utf-8")))
