"""The emission in the exact dark and the side's gate (the reader's re-ruling of 2026-10-20: (c) for the exact dark, the gate in every case; ALGEBRA.md, The click's read of the board): a body whose read finds every digit at the lay's origin at its emission's draw does not draw and its emission falls at its window's close, the reading NO_DRAW on its credit line (`meeting.emission_drawn`, `lists.emission`), the refusal by name standing for every other draw at the origin; a side draws only where a whole quantum came through its window (`lists.readings`, `credit.quanta_rounded`), so a background below one quantum clicks nowhere and the signal's quantum through at the close clicks; the seven dark worlds as shipped (the born four, the resonance pair, packet_emission) run LAWFUL with the emission at the close, their intervals and realised ports printed."""

import json

import pytest

from event_universe import node_detector, world_files
from event_universe.lattice import Lattice
from event_universe.reports import NO_DRAW
from event_universe.world_files import load_world
from tests.laws import EVENTS, TOOL


def clicks(lines):  # type: ignore[no-untyped-def]
    """The NODEDETECTOR credit lines of a run, the clicks."""
    return [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]


def run_whole(board):  # type: ignore[no-untyped-def]
    """The world run over its declared intervals, LAWFUL where no refusal is raised."""
    for _ in range(board.world.intervals):
        board.step()
    return board


def test_a_body_alone_in_the_dark_emits_at_its_windows_close_without_a_draw(tmp_path, monkeypatch):
    """The lone [1, 1299] body in e on its two Nodes, no light laid, its window derived 8 from its own beat (12 declared before the derived window of 2026-10-23) and its rate e to g at the lifetime 48: its read finds every digit at the lay's origin at every multiple of 4 and three cycling numbers between (the exact quarter turn), so the hazard's draws at 1, 2 and 3 miss and the draw at 4 is deferred; at the window's close, 12, the emission falls without a draw, one credit line emitted `pulse` from e to g with the reading NO_DRAW, the quantum laid at the Node of the larger share; the window runs from the lay (an emitter's when); every other draw at the origin is refused by name as before (two weights asked of the fresh board), and one weight reads nothing."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "u.json").write_bytes((EVENTS / "zeno" / "zeno_atom.json").read_bytes())
    body = {  # the Zeno body's declaration (the deleted zeno worlds' atom), in e with its rate out
        "family": "atom",
        "nodes": [{"node": [4, 4, 2], "weight": 1}, {"node": [5, 4, 2], "weight": 1}],
        "parts": [{"part": 0, "name": "g", "count": 0}, {"part": 1, "name": "e", "count": 1}],
        "transitions": [{"from": "g", "to": "e", "drive": "pulse", "weight": 1, "resonance": [2, 3]}],
        "rates": [{"from": "e", "to": "g", "lifetime": 48, "gives_to": "pulse"}],
        "node_detector": {},
    }
    world = {
        "shape": [8, 8, 5],
        "boundary": {"x": "periodic", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "intervals": 30,
        "universe": "u.json",
        "bodies": [body],
        "packets": [],
        "node_detectors": [],
    }
    (path := tmp_path / "dark.json").write_text(json.dumps(world), encoding="utf-8")
    TOOL.main(["--input", str(path)])
    board = Lattice(load_world(path), (lines := []).append)
    books = board.credit.bodies[0]
    pulse = [f.name for f in board.families].index("pulse")
    assert node_detector.read_families(books) == [pulse, books.index] and books.part == 1
    with pytest.raises(RuntimeError, match="at the interval 0 finds every digit at the lay's origin"):
        node_detector.picked(board, books, [1, 1])  # any other draw at the origin: refused by name
    assert node_detector.picked(board, books, [1]) == 0 and books.left is None  # one weight, no read
    run_whole(board)
    given = [c for c in clicks(lines) if c["emitted"]]
    assert (
        [(c["interval"], c["emitted"], c["lost"]) for c in given] == [(8, "pulse", [NO_DRAW])]
    )  # the window derived from the body's own beat, 8 (the declared window 12 before the derived window, 2026-10-23)
    assert given[0]["window"] == [1, 8] and (given[0]["before"], given[0]["realised"]) == ("e", "g")
    laid = {tuple(x["node"]["at"]) for x in lines if x["event"] == "lay" and x["family"] == "pulse"}
    assert laid <= {tuple(n["node"]) for n in body["nodes"]} and board.credit.counts[pulse] == 1
    print(f"the dark body's emission {given[0]['interval']}, {given[0]['lost']}, laid at {sorted(laid)}")
