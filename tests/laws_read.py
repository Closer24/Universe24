"""The shipped worlds in the read's shape for the law's tests (the click's read of the board, 2026-10-20; beside tests/laws.py, whose size the tests' shape caps): a shipped document with no engine start file and no generator constants (`redeclared`), a builder's world file rewritten so with its mode file's digest moved (`redeclared_file`), and a shipped world parsed in that shape without a copy, the mode file beside it standing by the digest of the file as shipped (`load_shipped`)."""

from __future__ import annotations

import json

from event_universe import world_files
from event_universe.loader.world import parse_world
from event_universe.world_files import input_digest


def redeclared(world):  # type: ignore[no-untyped-def]
    """A shipped world's document in the shape the read gives the files: no engine start file (`engine`), no generator (`seed`, `multiplier` and `increment` out of the world's `draw` and of every body's `node_detector`, a body's left `{}` where nothing else stands), the world otherwise as the file has it; the document itself, edited in place."""
    world.pop("engine", None)
    blocks = [world.get("draw"), *(body.get("node_detector") for body in world.get("bodies", []))]
    for block in blocks:
        if isinstance(block, dict):
            for key in ("seed", "multiplier", "increment"):
                block.pop(key, None)
    return world


def redeclared_file(path):  # type: ignore[no-untyped-def]
    """A world file a builder wrote, rewritten in the read's shape (`redeclared`) with its mode file's digest moved to the rewritten document where a mode file stands beside it; the path."""
    world = redeclared(json.loads(path.read_text(encoding="utf-8")))
    path.write_text(json.dumps(world), encoding="utf-8")
    if (mode := path.with_suffix(".mode.json")).exists():
        found = json.loads(mode.read_text(encoding="utf-8"))
        found["world_digest"] = input_digest(world)
        mode.write_text(json.dumps(found), encoding="utf-8")
    return path


def load_shipped(path):  # type: ignore[no-untyped-def]
    """A shipped world parsed in the read's shape without a copy: its document `redeclared` after the digest of the file as shipped is taken, so the mode file beside it stands; the files read at their repository paths under the repository root in place."""
    document = json.loads(path.read_text(encoding="utf-8"))
    files, digest = world_files.world_files(document), input_digest(document)
    if (beside := path.with_suffix(".mode.json")).is_file():
        files[beside.name] = json.loads(beside.read_text(encoding="utf-8"))
    return parse_world(redeclared(document), files, digest)
