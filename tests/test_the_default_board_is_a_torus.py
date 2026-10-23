"""The default board is a torus (ALGEBRA.md, The board is a torus; the owner's word of 2026-10-23): a world file without `boundary` wraps on every axis, a face declared by name stands, and the shipped cycle world reads the same board with the key and without it."""

import json

import numpy as np

from event_universe.lattice import Lattice
from event_universe.loader import world as loader_world
from event_universe.world_files import load_world
from tests.laws import EVENTS, world_beside
from tests.laws_read import load_shipped

CYCLE = EVENTS / "cycle" / "cycle.json"  # the uniform gapped 5-torus, no `boundary` in its file
FACED = EVENTS / "bell" / "bell_a_b.json"  # an instrument's board: the x axis open with its layer
INTERVALS = 12
AXES = ("x", "y", "z")
BOARD = ("shape", "periodic", "open_axes", "face_depth", "beyond", "receding", "intervals", "families")


def levels(board: Lattice) -> list[list[object]]:
    """Every line's three arrays of every family as Python's integers, the comparison bit for bit."""
    lines = [line for state in board.states for line in state.lines]
    return [np.asarray(a, dtype=object).tolist() for r in lines for a in (r.now, r.before, r.remainder)]


def test_a_world_without_boundary_is_a_torus_and_a_declared_face_stands(tmp_path):  # type: ignore[no-untyped-def]
    # (1) the cycle world's file declares no boundary and loads periodic on every axis, the key not required
    assert "boundary" not in json.loads(CYCLE.read_text(encoding="utf-8"))
    assert "boundary" not in loader_world.WORLD_REQUIRED and "boundary" in loader_world.WORLD_KEYS
    torus = load_shipped(CYCLE)
    assert torus.periodic == (True, True, True) and torus.open_axes == (False, False, False)
    assert torus.face_depth == 0 and torus.beyond == () and torus.receding == ()
    # (2) a world declaring a face keeps it: the open axis, its layer's depth and its receding sides
    declared = json.loads(FACED.read_text(encoding="utf-8"))
    faces, faced = declared["boundary"], load_shipped(FACED)
    assert faced.periodic == tuple(faces[axis] == "periodic" for axis in AXES)
    assert faced.open_axes == tuple(faces[axis] == "open" for axis in AXES) and any(faced.open_axes)
    sides = sum(len(axis["sides"]) for axis in declared["receding"].values())
    assert faced.face_depth == declared["face_depth"] and len(faced.receding) == sides
    # (3) the cycle world with the key declared periodic on every axis loads equal to the file without it
    with_key = lambda w: w.__setitem__("boundary", dict(loader_world.TORUS))  # noqa: E731
    keyed = load_world(world_beside(tmp_path, CYCLE, with_key))
    assert all(getattr(keyed, field) == getattr(torus, field) for field in BOARD)
    boards = Lattice(torus), Lattice(keyed)
    for board in boards:
        board.output = lambda line: None
    assert levels(boards[0]) == levels(boards[1])
    for _ in range(INTERVALS):
        for board in boards:
            board.step()
    assert levels(boards[0]) == levels(boards[1]) and boards[0].interval == INTERVALS
