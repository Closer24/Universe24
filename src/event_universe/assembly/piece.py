"""The two files, read once: the piece (its calibre, size, ticks and setting) and the calibre it names (its integers and trains), the calibre's path relative to the piece's folder; every other key refused by name (the owner's word of 2026-10-25: nothing of a calibre in the code, nothing of a hand in the files; the control and detectors keys of the toy's measurements refused since the fold, kept by name in tools/derivations/toys/lean)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from event_universe.trains import HAND, OFFSET, REGULATOR

PIECE_KEYS = frozenset({"universe", "shape", "intervals", "seed"})
CALIBRE_KEYS = frozenset({"integers", "rows"})
INTEGERS = frozenset(
    {"den", "node_clock", "quantum_action", "trace", "amplitude"}
)  # the mesh unit G is derived from Gamma (K-S1), no key; the trace the held drive's weight (ALGEBRA.md, the held drive); the amplitude the standard length declared from outside, carried above the floor derived from Gamma (standard.carried; the owner's words of 2026-10-27, 04:0x and 04:4x UTC)
TRAIN_KEYS = frozenset({"shape", "pair", "wall"})


def refused_keys(found: dict[str, Any], allowed: frozenset[str], name: str) -> None:
    """A key the file holds beyond the law's, refused by name."""
    beyond = sorted(set(found) - allowed)
    if beyond:
        raise ValueError(f"the {name} file holds keys of no law: {', '.join(beyond)}")


def check_piece(
    piece_file: dict[str, Any], calibre_file: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """The two files' dictionaries with their keys checked: the piece's four keys, the calibre's two, the calibre's five integers each named (a missing one refused by name), every train's gears a count the law names (the ratchet, the hand, the offset and the regulator) with a ratio or teeth."""
    refused_keys(piece_file, PIECE_KEYS, "world")
    refused_keys(calibre_file, CALIBRE_KEYS, "universe")
    refused_keys(calibre_file["integers"], INTEGERS, "universe's integers")
    missing = sorted(INTEGERS - set(calibre_file["integers"]))
    if missing:
        raise ValueError(f"the universe file names no {', '.join(missing)}: refused by name")
    for train in calibre_file["rows"]:
        refused_keys(train, TRAIN_KEYS, "universe's row")
        if int(train["shape"]) not in (1, HAND, OFFSET, REGULATOR):
            raise ValueError(f"a row of shape {train['shape']} is no row of the law: refused by name")
        if ("pair" in train) == ("wall" in train):
            raise ValueError("a row has a pair or a wall of its own, one of the two")
    return calibre_file, piece_file


def read_piece(path: str | Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """The calibre and the piece from the piece's file path."""
    where = Path(path)
    piece_file = json.loads(where.read_text(encoding="utf-8"))
    calibre_file = json.loads(where.parent.joinpath(piece_file["universe"]).read_text(encoding="utf-8"))
    return check_piece(piece_file, calibre_file)
