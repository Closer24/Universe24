"""The emission in the exact dark and the side's gate (the reader's re-ruling of 2026-10-20: (c) for the exact dark, the gate in every case; ALGEBRA.md, The click's read of the board): a body whose read finds every digit at the lay's origin at its emission's draw does not draw and its emission falls at its window's close, the reading NO_DRAW on its credit line (`meeting.emission_drawn`, `lists.emission`), the refusal by name standing for every other draw at the origin; a side draws only where a whole quantum came through its window (`lists.readings`, `credit.quanta_rounded`), so a background below one quantum clicks nowhere and the signal's quantum through at the close clicks; the seven dark worlds as shipped (the born four, the resonance pair, packet_emission) run LAWFUL with the emission at the close, their intervals and realised ports printed."""

import json
from fractions import Fraction

import pytest

from event_universe import credit, node_detector, world_files
from event_universe.lattice import Lattice
from event_universe.reports import NO_DRAW
from event_universe.world_files import load_world
from tests.laws import EVENTS, ROOT, TOOL, world_beside
from tests.laws_read import load_shipped

BACKGROUND = [  # the probe's form: a train of the signal's wave at a tenth of its amplitude along the chain
    {
        "family": "spin",
        "along": "x",
        "wave": [sign, 4],
        "phase": [0, 1],
        "amplitude": 6,
        "top": {"x": [x, x + 8], "y": [0, 0], "z": [0, 0]},
        "edge": {"x": 2, "y": 0, "z": 0},
    }
    for sign, x in ((-1, 2), (1, 14), (-1, 26), (1, 38), (-1, 50))
]
BORN = ("born_a_b", "born_a_b_prime", "born_a_prime_b", "born_a_prime_b_prime")


def clicks(lines):  # type: ignore[no-untyped-def]
    """The NODEDETECTOR credit lines of a run, the clicks."""
    return [c for c in lines if c["event"] == "credit" and c["label"] == "NODEDETECTOR"]


def run_whole(board):  # type: ignore[no-untyped-def]
    """The world run over its declared intervals, LAWFUL where no refusal is raised."""
    for _ in range(board.world.intervals):
        board.step()
    return board


def test_a_body_alone_in_the_dark_emits_at_its_windows_close_without_a_draw(tmp_path, monkeypatch):
    """The lone [1, 1299] body in e on its two Nodes, no light laid, its window 12 and its rate e to g at the lifetime 48: its read finds every digit at the lay's origin at every multiple of 4 and three cycling numbers between (the exact quarter turn), so the hazard's draws at 1, 2 and 3 miss and the draw at 4 is deferred; at the window's close, 12, the emission falls without a draw, one credit line emitted `pulse` from e to g with the reading NO_DRAW, the quantum laid at the Node of the larger share; the window runs from the lay (an emitter's when); every other draw at the origin is refused by name as before (two weights asked of the fresh board), and one weight reads nothing."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "u.json").write_bytes((EVENTS / "zeno" / "zeno_atom.json").read_bytes())
    body = {  # the Zeno body's declaration (the deleted zeno worlds' atom), in e with its rate out
        "family": "atom",
        "nodes": [{"node": [4, 4, 2], "weight": 1}, {"node": [5, 4, 2], "weight": 1}],
        "parts": [{"part": 0, "name": "g", "count": 0}, {"part": 1, "name": "e", "count": 1}],
        "transitions": [{"from": "g", "to": "e", "drive": "pulse", "weight": 1, "resonance": [2, 3]}],
        "rates": [{"from": "e", "to": "g", "lifetime": 48, "gives_to": "pulse"}],
        "node_detector": {"window": 12},
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
    assert [(c["interval"], c["emitted"], c["lost"]) for c in given] == [(12, "pulse", [NO_DRAW])]
    assert given[0]["window"] == [1, 12] and (given[0]["before"], given[0]["realised"]) == ("e", "g")
    laid = {tuple(x["node"]["at"]) for x in lines if x["event"] == "lay" and x["family"] == "pulse"}
    assert laid <= {tuple(n["node"]) for n in body["nodes"]} and board.credit.counts[pulse] == 1
    print(f"the dark body's emission {given[0]['interval']}, {given[0]['lost']}, laid at {sorted(laid)}")


def test_a_side_draws_only_where_a_whole_quantum_came_through_its_window(tmp_path, monkeypatch):
    """The side's gate on the born pair's chain with a background (the probe's form: five packets of the pair's family at a tenth of the signal's amplitude along the chain): the background's light stands at the atom, so its emission's hazard is read from the board, drawn at its window's close, 24, and given there (no NO_DRAW on its line); at the sides' first close, 62, the left side has the pair's left beam and the background's share through its window and clicks, and the right side has the background's share alone, below one quantum, and does not click (before the gate it clicked on that share); at 124 the pair's right beam, read after the left side's write, has come through and the right side clicks; the gate's readings (n n I over scale W_rec G^2, `credit.quanta_rounded`) and the realised ports printed."""
    source = EVENTS / "bell_singlet" / "born_a_b.json"
    path = world_beside(tmp_path, source, lambda world: world.update(packets=BACKGROUND))
    TOOL.main(["--input", str(path)])  # the background laid by the generator, the mode file anew
    board, gate, read = Lattice(load_world(path), (lines := []).append), [], credit.quanta_rounded

    def gated(books, index, inflow, link_unit, parts, scale):  # type: ignore[no-untyped-def]
        found = read(books, index, inflow, link_unit, parts, scale)
        unit = books.units[index] * link_unit * link_unit * scale
        gate.append((board.interval, found, Fraction(inflow * parts * parts, unit)))
        return found

    monkeypatch.setattr(credit, "quanta_rounded", gated)
    run_whole(board)
    sides = [
        (c["interval"], c["node_detector"], c["realised"]) for c in clicks(lines) if not c["emitted"]
    ]
    given = [c for c in clicks(lines) if c["emitted"]]
    window = board.world.bodies[0].detector.draw.window
    assert [(c["interval"], c["lost"]) for c in given] == [(window, None)]  # lit: read from the board
    assert [(at, found) for at, found, _q in gate] == [(62, 1), (62, 0), (124, 1)]  # left, right; right
    closes = [(at, name) for at, name, _r in sides if name in ("left", "right")]
    assert gate[1][2] < Fraction(1, 10) and closes == [
        (62, "left"),
        (124, "right"),
    ]  # the right gated at 62
    print(
        f"the gate: the pair given at {window}, the readings {[(a, f, float(q)) for a, f, q in gate]}, {sides}"
    )


def test_the_born_worlds_emit_at_the_atoms_close_and_run_lawful(monkeypatch):
    """The four born worlds as shipped, in the read's shape: each atom alone in the dark gives the pair at its window's close without a draw (the reading NO_DRAW), the run is LAWFUL to its end, and the two sides click once each on the pair, the left at the first close and the right, whose beam comes through in the second window, at the second. What the atom reads (ALGEBRA.md, What a body reads, the reader's G2 of 2026-10-20): at its later closes, 85 and 110, lit by its own pair's wake once the left side has taken the source, the absorption's draw in the unit W_rec^2 (53.9 bits) reads the spin record at the atom's Node and at its two neighbours within one Link, where the wake stands off the origin, with its own lines at its Node: 156 and 184 bits, above the total, so the draw is the board's and the world runs whole (before G2 the Node alone read 50 bits and the world was refused at 85); the reads' Nodes per family and bits printed per world."""
    world_files.REPOSITORY_ROOT = ROOT
    found, reads, real = {}, [], node_detector.read_of

    def spied(board, what, label):  # type: ignore[no-untyped-def]
        number, moduli = real(board, what, label)
        nodes = [(board.families[f].name, int(at.sum())) for f, at in what]
        reads.append((board.interval, nodes, number.bit_length()))
        return number, moduli

    monkeypatch.setattr(node_detector, "read_of", spied)
    for name in BORN:
        reads.clear()
        board = run_whole(
            Lattice(load_shipped(EVENTS / "bell_singlet" / f"{name}.json"), (lines := []).append)
        )
        atom = [(at, nodes, bits) for at, nodes, bits in reads if nodes[-1][0] == "atom" and at > 24]
        assert [(at, nodes) for at, nodes, _b in atom] == [
            (85, [("spin", 3), ("atom", 1)]),
            (110, [("spin", 3), ("atom", 1)]),
        ]
        assert all(bits > 54 for _a, _n, bits in atom), atom  # above the absorption's unit, 53.9 bits
        found[f"{name} reads"] = atom
        given = [c for c in clicks(lines) if c["emitted"]]
        sides = [
            (c["interval"], c["node_detector"], c["realised"])
            for c in clicks(lines)
            if c["node_detector"] in ("left", "right")
        ]
        window = board.world.bodies[0].detector.draw.window
        assert [(c["interval"], c["lost"]) for c in given] == [(window, [NO_DRAW])], name
        assert [(at, side) for at, side, _r in sides] == [(62, "left"), (124, "right")], (name, sides)
        assert board.ended is None, name
        found[name] = (given[0]["interval"], sides)
    print(f"the born worlds: {found}")


def test_the_resonance_pair_and_the_packet_world_run_lawful_with_the_emission_at_the_close():
    """The resonance pair and the packet emission world as shipped, in the read's shape: the giver alone in the dark emits at its window's close where the hazard's draws from its own cycling digits missed (the resonant and the detuned world at 48, their windows), the taker's own draws read from the light; the packet world's giver has its window derived from its train's passage, 758, beyond the run's 168 intervals, so no emission falls inside the run; every run LAWFUL to its end; the emission intervals printed."""
    world_files.REPOSITORY_ROOT = ROOT
    found = {}
    for folder, name in (
        ("resonance", "resonant"),
        ("resonance", "detuned"),
        ("packet_emission", "packet_emission"),
    ):
        board = run_whole(Lattice(load_shipped(EVENTS / folder / f"{name}.json"), (lines := []).append))
        given = [(c["interval"], c["node_detector"], c["lost"]) for c in clicks(lines) if c["emitted"]]
        window = board.world.bodies[0].detector.draw.window
        assert board.ended is None, name
        if window <= board.world.intervals:
            assert given[:1] == [(window, "body 0", [NO_DRAW])], (name, given)
        else:
            assert given == [], (name, given)
        found[name] = (window, given)
    print(f"the dark emitters: {found}")
