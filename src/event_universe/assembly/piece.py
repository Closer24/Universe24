"""The two files, read once: the world (universe, shape, intervals, seed) and the universe it names (integers, rows), the universe's path relative to the world's folder; every other key refused by name (the owner's word of 2026-10-25: nothing of a universe in the code, nothing of a hand in the files; the control and detectors keys of the toy's measurements refused since the fold, kept by name in tools/derivations/toys/lean)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from event_universe.trains import HAND, OFFSET, REGULATOR

PIECE_KEYS = frozenset({"universe", "shape", "intervals", "seed"})
CALIBRE_KEYS = frozenset({"integers", "rows"})
INTEGERS = frozenset(
    {"den", "node_clock", "quantum_action", "trace", "amplitude"}
)  # the Link unit G is derived from Gamma (K-S1), no key; the trace the held write's weight (ALGEBRA.md, the held write); the amplitude the phase line's scale declared from outside, carried above the floor derived from Gamma (phase.carried; the owner's words of 2026-10-27, 04:0x and 04:4x UTC)
TRAIN_KEYS = frozenset({"shape", "pair", "wall"})


def refused_keys(found: dict[str, Any], allowed: frozenset[str], name: str) -> None:
    """A key the file holds beyond the law's, refused by name."""
    beyond = sorted(set(found) - allowed)
    if beyond:
        raise ValueError(f"the {name} file holds keys of no law: {', '.join(beyond)}")


def check_piece(
    world: dict[str, Any], universe: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]]:
    """The two files' dictionaries with their keys checked: the world's four keys, the universe's two, the universe's five integers each named (a missing one refused by name), every row's shape one the law names (the walled row, the plane, the shape-4 row, the shape-10 row) with a pair or a wall."""
    refused_keys(world, PIECE_KEYS, "world")
    refused_keys(universe, CALIBRE_KEYS, "universe")
    refused_keys(universe["integers"], INTEGERS, "universe's integers")
    missing = sorted(INTEGERS - set(universe["integers"]))
    if missing:
        raise ValueError(f"the universe file names no {', '.join(missing)}: refused by name")
    for row in universe["rows"]:
        refused_keys(row, TRAIN_KEYS, "universe's row")
        if int(row["shape"]) not in (1, HAND, OFFSET, REGULATOR):
            raise ValueError(f"a row of shape {row['shape']} is no row of the law: refused by name")
        if ("pair" in row) == ("wall" in row):
            raise ValueError("a row has a pair or a wall of its own, one of the two")
    return universe, world


def read_piece(path: str | Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """The universe and the world from the world file's path."""
    where = Path(path)
    world = json.loads(where.read_text(encoding="utf-8"))
    universe = json.loads(where.parent.joinpath(world["universe"]).read_text(encoding="utf-8"))
    return check_piece(world, universe)
