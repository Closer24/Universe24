"""The books of a turned record (issue #2169, finding 1; the reader's ruling of 2026-10-21; ALGEBRA.md, The share's change is the currents, the clause of 2026-10-21): a region's booking of a turned plane reads the flux line's own current with the Link's pair the step reads (`readings.turned_currents_of`, `board_readings.turned_read`), where the plain bilinear of a turned pair turns at the difference of the two Nodes' angles, the gauge's oscillation of zero mean, which the floor at 0 turned into credits by the phase of the window's sums (the builder's hydrogen_1s with a 7-Node ball: -3.07 and +2.76 W_rec over [1, 35] and [36, 70], the standing body credited to its own region at 70 and erased; the pair's booking +0.0019, -0.0005, -0.0032 and +0.00006 W_rec over the four windows of 140, no credit, the measurer's run on the branch). Here the same on a world the test lays into a tmp folder: the proton's pixel at the centre of an open cube of 5 and the electron laid standing in its well by tools/standing_lay.py (the 1s at Omega 0.7025 against omega_0 0.8411), a region of seven Nodes on the electron's, three windows; and the plain path pinned bit for bit on the node detector test's chain (tests/test_the_node_detector.py): a plain record reads no pair and its currents and its booking are the plain bilinear's as before."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from event_universe import board_readings, credit, lattice, readings, reports, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import PACKET, ROOT, TOOL, load_file, slit_world

STANDING = load_file("standing_lay", ROOT / "tools" / "standing_lay.py")  # the standing lay's tool
UNIVERSE = ROOT / "examples" / "events" / "atom" / "hydrogen_read3.json"  # the hydrogen worlds' integers
CUBE, WINDOW, WINDOWS = 5, 4, 3
HUNDREDTH = 100  # the walk's bound: the booked inflow per window below one count's hundredth
PLAIN_PINS = (  # the node detector test's chain, four intervals: the six Port sums over the board of
    # `board_readings.currents` and the region's intake after the step (main 74cafb5d1's numbers)
    ([-7246344000, 7246344000, 0, 0, 0, 0], 0),
    ([-7236372000, 7236372000, 0, 0, 0, 0], 0),
    ([-7229028000, 7229028000, 0, 0, 0, 0], 2268672000),
    ([-7223886000, 7223886000, 0, 0, 0, 0], 25021440000),
)


def standing_world(folder: Path) -> Path:
    """The world: an open cube of CUBE Nodes, the proton's pixel of one quantum at the centre, the electron of one quantum at its +x neighbour laid standing by the tool, a region named ball on the centre and its six neighbours, the draw's window WINDOW, WINDOWS windows of intervals; the mode file the tool's."""
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    c = CUBE // 2
    ball = [[c, c, c]] + [
        [c + d * (a == 0), c + d * (a == 1), c + d * (a == 2)] for a in range(3) for d in (-1, 1)
    ]
    world = {
        "shape": [CUBE] * 3,
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "intervals": WINDOW * WINDOWS,
        "universe": "u.json",
        "bodies": [
            {"family": "proton", "nodes": [{"node": [c, c, c], "count": 1}]},
            {"family": "electron", "nodes": [{"node": [c + 1, c, c], "count": 1}]},
        ],
        "node_detectors": [{"name": "ball", "positions": ball}],
    }  # no draw: the standing world lays no wave with an end past the ball, so no window is derivable (2026-10-23)
    path = folder / "w.json"
    path.write_text(json.dumps(world) + "\n", encoding="utf-8")
    STANDING.main(["--input", str(path), "--record", "electron", "--source", "proton", "--sense", "-1"])
    return path


def test_a_standing_charged_record_in_its_sign_well_books_no_inflow_and_no_credit(tmp_path, monkeypatch):
    """Three windows on the standing electron: the booked inflow through the ball's front, the pair's reading (`reports.weighted` on `node_detector.weighed_currents`, as `credit.booked` books it), stays below one count's hundredth at every close, the plain bilinear's reading of the same lines through the same front (the old booking) does not, the count stays 1 and no credit line is written; the electron is turned (`Lattice.turning`) and reads its pairs."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = standing_world(tmp_path)
    booked: dict[str, int] = {"pair": 0, "plain": 0}
    plain: dict[int, list[tuple[tuple[np.ndarray, ...], tuple, np.ndarray]]] = {}
    weighed_currents, booked_was = lattice.weighed_currents, credit.booked

    def weighed_and_plain(board: Lattice):  # type: ignore[no-untyped-def]
        found = weighed_currents(board)  # the pair's read, the books' own
        for index, reads in found.items():
            if index in board.turning:  # the plain bilinear of the same lines, the old booking
                plain[index] = [
                    (
                        readings.currents_of(
                            board.families[index].pair[0], board.lines_of(index, r), board.wrap
                        ),
                        factors,
                        shares,
                    )
                    for r, (_through, factors, shares) in enumerate(reads)
                ]
        return found

    def hooked(board, index, name, nodes, facing, weighed):  # type: ignore[no-untyped-def]
        if index in plain:
            for key, reads in (("pair", weighed[index]), ("plain", plain[index])):
                through = reports.weighted(facing, reads)
                booked[key] += sum(int(np.asarray(t, dtype=object).sum()) for t in through)
        return booked_was(board, index, name, nodes, facing, weighed)

    monkeypatch.setattr(lattice, "weighed_currents", weighed_and_plain)
    monkeypatch.setattr(credit, "booked", hooked)
    board = Lattice(load_world(path), (lines := []).append)
    electron = [f.name for f in board.families].index("electron")
    unit = board.credit.units[electron] * board.unit * board.unit  # one count, W_rec G^2
    assert electron in board.turning and board.credit.counts[electron] == 1
    closes = []
    for interval in range(1, board.world.intervals + 1):
        board.step()
        assert board.ended is None and board.credit.counts[electron] == 1
        if interval % WINDOW == 0:
            closes.append((booked["pair"] / unit, booked["plain"] / unit))
            booked["pair"] = booked["plain"] = 0
    print(f"the ball's booked inflow per window in W_rec, (the pair's, the plain bilinear's): {closes}")
    assert len(closes) == WINDOWS
    assert all(abs(pair) * HUNDREDTH < 1 for pair, _plain in closes)  # within the walk at every close
    assert max(abs(old) for _pair, old in closes) > 10 * max(abs(pair) for pair, _old in closes)
    assert not [line for line in lines if line.get("event") == "credit"]  # no credit, the count 1


def test_a_plain_records_currents_and_booking_stand_bit_for_bit(tmp_path, monkeypatch):
    """The plain path (`readings.currents_of` with no pairs, `board_readings.currents`, the intake of `credit.booked`) on the node detector test's chain, the light packet crossing the region of two Nodes: the six Port sums of the currents over the board and the region's intake after each of four intervals as main read them before the turned record's reading entered, no family turned on this world."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    region, draw = [[13, 0, 0], [14, 0, 0]], {}
    packet = {**PACKET, "top": {"x": [8, 8], "y": [0, 0], "z": [0, 0]}, "edge": {"x": 4, "y": 0, "z": 0}}
    chain = dict(shape=[24, 1, 1], boundary=dict(x="open", y="periodic", z="periodic"), faces=[])
    readers = [{"name": "near", "positions": region}]
    world = slit_world(
        tmp_path, TOOL, "chain", packets=[packet], node_detectors=readers, draw=draw, **chain
    )
    board = Lattice(load_world(world))
    light = [f.name for f in board.families].index("charge")
    assert not board.turning
    for sums, intake in PLAIN_PINS:
        through = board_readings.currents(board)[light]
        board.step()
        assert [int(np.asarray(c, dtype=object).sum()) for c in through] == sums
        assert sum(map(sum, board.credit.intake.get((light, "near"), {}).values())) == intake
