"""The two files, read once: the world (universe, shape, intervals, seed) and the universe it names (integers, rows), the universe's path relative to the world's folder; every other key refused by name (the owner's word of 2026-10-25: nothing of a universe in the code, nothing of a hand in the files; the control and detectors keys of the toy's measurements refused since the fold, kept by name in tools/derivations/toys/lean)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

WORLD_KEYS = frozenset({"universe", "shape", "intervals", "seed"})
UNIVERSE_KEYS = frozenset({"integers", "rows"})
INTEGERS = frozenset(
    {"den", "node_clock", "quantum_action", "trace"}
)  # the Link unit G is derived from Gamma (K-S1), no key; the trace the held write's weight (ALGEBRA.md, the held write)
ROW_KEYS = frozenset({"shape", "pair", "wall"})


def refused_keys(found: dict[str, Any], allowed: frozenset[str], name: str) -> None:
    """A key the file holds beyond the law's, refused by name."""
    beyond = sorted(set(found) - allowed)
    if beyond:
        raise ValueError(f"the {name} file holds keys of no law: {', '.join(beyond)}")


def read_world(world: dict[str, Any], universe: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    """The two files' dictionaries with their keys checked: the world's four keys, the universe's two, the universe's five integers, every row's shape with a pair or a wall."""
    refused_keys(world, WORLD_KEYS, "world")
    refused_keys(universe, UNIVERSE_KEYS, "universe")
    refused_keys(universe["integers"], INTEGERS, "universe's integers")
    for row in universe["rows"]:
        refused_keys(row, ROW_KEYS, "universe's row")
        if ("pair" in row) == ("wall" in row):
            raise ValueError("a row has a pair or a wall of its own, one of the two")
    return universe, world


def load_world(path: str | Path) -> tuple[dict[str, Any], dict[str, Any]]:
    """The universe and the world from the world file's path."""
    where = Path(path)
    world = json.loads(where.read_text(encoding="utf-8"))
    universe = json.loads(where.parent.joinpath(world["universe"]).read_text(encoding="utf-8"))
    return read_world(world, universe)
