"""The takers under the world's key `takers` (the sprint of 2026-10-21, builder L; ALGEBRA.md, The emission of a bound record is the click's act of the taker; src/event_universe/taker.py, frame.py, loader/world.takers_of): on a world the test lays into a tmp folder as the turned record's test does (the proton's pixel at the centre of an open cube of 5, the electron laid standing in its well by tools/standing_lay.py), the key makes the electron a taker whose instrument is read from the board and typed nowhere (its frame's levels as integer rotation pairs, its transition the gap from its one level to the next, its unit W_c sin(Omega_upper - Omega_lower) by the two pairs, its window the transition's period by the turn count, its region and front), the frozen proton no taker, the books and the window filled each interval, no credit before a close, and at a close the whether drawn on the body's own digits against [the window's inflow floored and capped, the unit less it] or nothing drawn at an inflow at or below 0; the key refused by name at any other value and a world without it holding no taker. Beside it the blind of main's fix of 2026-10-21 on builder D's detector world at the cube of 5 (a 7-Node ball on the standing electron, the window 35): the engine's click lines through the ball sum to within a hundredth of a quantum over the window where the plain bilinear of the same lines through the same front sums to tenths, and no credit is written."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe import readings, reports, taker, world_files
from event_universe.lattice import Lattice
from event_universe.world_files import load_world
from tests.laws import ROOT, load_file

STANDING = load_file(
    "standing_lay_takers", ROOT / "tools" / "standing_lay.py"
)  # the standing lay's tool
FRAME = load_file("frame_of_takers", ROOT / "tools" / "frame_of.py")  # the frame's tool, the integers
UNIVERSE = ROOT / "examples" / "events" / "atom" / "hydrogen_read3.json"  # the hydrogen worlds' integers
CUBE, WINDOW = 5, 12  # the ball's window: twelve intervals, a third of the beat, enough for the contrast
HUNDREDTH = 100


def standing_world(folder: Path, ball: bool, takers: object = None, intervals: int = 8) -> Path:
    """The world: the open cube of CUBE Nodes, the proton's pixel at the centre and the electron at its +x neighbour laid standing by the tool, with the ball region of seven Nodes and the draw's window WINDOW where `ball`, the key `takers` where given and with it the frame's integers in the mode file (tools/frame_of.py, 2026-10-21)."""
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    c = CUBE // 2
    nodes = [[c, c, c]] + [
        [c + d * (a == 0), c + d * (a == 1), c + d * (a == 2)] for a in range(3) for d in (-1, 1)
    ]
    world: dict[str, object] = {
        "shape": [CUBE] * 3,
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "intervals": intervals,
        "universe": "u.json",
        "bodies": [
            {"family": "proton", "nodes": [{"node": [c, c, c], "count": 1}]},
            {"family": "electron", "nodes": [{"node": [c + 1, c, c], "count": 1}]},
        ],
        "node_detectors": [{"name": "ball", "positions": nodes}] if ball else [],
    }
    if ball:
        world["draw"] = {"window": WINDOW}
    if takers is not None:
        world["takers"] = takers
    path = folder / "w.json"
    path.write_text(json.dumps(world) + "\n", encoding="utf-8")
    STANDING.main(["--input", str(path), "--record", "electron", "--source", "proton", "--sense", "-1"])
    if takers is not None:  # the frame's integers written into the mode file by the host's tool
        FRAME.main(["--input", str(path)])
    return path


def test_a_body_in_a_well_is_a_taker_with_its_instrument_read_from_the_board(tmp_path, monkeypatch):
    """Under `takers: bodies` the standing electron is the one taker (the frozen proton's line says no transition): its frame's levels are integer rotation pairs in energy order, its transition the gap from its one level to the next, its unit W_c sin(Omega_1 - Omega_0) by the two pairs to the integer, its window the turn count closing the circle, its region at least one Node with a front; each interval books the light it reads (the free row and the proton's row, nothing of its own) into its window and its books alike and no credit is written; the close draws nothing at an inflow at or below 0 and otherwise the whether against [the inflow, the unit less it] on the body's own digits, the count moving by the draw alone; `takers: all` is refused by name and a world without the key holds no taker."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = standing_world(tmp_path, False, "bodies")
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(path), lines.append)
    electron = [f.name for f in board.families].index("electron")
    said = [line for line in lines if line["event"] == reports.TAKER]
    assert [line["node_detector"] for line in said] == [f"{reports.BODY} 0", f"{reports.BODY} 1"]
    assert said[0][reports.TAKEN] == reports.FROZEN  # the frozen proton: no hop, no taker
    (one,) = board.credit.takers
    frame = one.frame
    assert one.body == 1 and frame is not None and frame.index == electron
    assert (
        said[1][reports.SHARES] == list(frame.shares) and sum(frame.shares) > 0
    )  # in parts of the unit
    num, den = board.families[electron].pair
    pairs = [level.pair[0] for level in frame.levels]
    assert pairs == sorted(pairs, reverse=True) and all(-den < p < den for p in pairs)  # energy order
    assert (frame.lower, frame.upper) == (0, 1)  # one level standing: the gap to the next
    low, high = frame.levels[0], frame.levels[1]
    sine = high.sine * low.pair[0] - high.pair[0] * low.sine  # den^2 sin(Omega_1 - Omega_0)
    assert one.unit == (3 * den * board.world.quantum_action * sine) // (den * den) > 0
    assert one.period == frame.period > 1 and said[1][reports.WINDOW_WORD] == one.period
    assert int(one.region.sum()) >= 1 and sum(int(m.sum()) for m in one.front) >= 1
    for _interval in range(6):
        board.step()
    assert one.elapsed == 6 and one.window == one.books and one.count == 0
    assert int(sum(int(v) for v in one.per_node[one.region])) == one.window
    assert not [line for line in lines if line["event"] == reports.CREDIT]
    before = len(lines)
    taker.closed(board, one)
    close = lines[-1]
    assert close["event"] == reports.TAKER and len(lines) >= before + 1
    weight = min(max(one.books, 0), one.unit)
    assert close[reports.WEIGHTS] == [weight, one.unit - weight] and close[reports.BOOKED] == one.books
    if weight <= 0:
        assert close[reports.TAKEN] == reports.NOTHING and one.count == 0
    else:
        assert close[reports.TAKEN] in (True, False) and one.count == int(close[reports.TAKEN])
    assert one.elapsed == 0 and one.windows == 1
    world = json.loads(path.read_text(encoding="utf-8"))
    world["takers"] = "all"
    mode = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    mode["world_digest"] = world_files.input_digest(world)
    (refused := tmp_path / "all.json").write_text(json.dumps(world), encoding="utf-8")
    refused.with_suffix(".mode.json").write_text(json.dumps(mode), encoding="utf-8")
    with pytest.raises(ValueError, match="takers"):
        load_world(refused)
    plain = Lattice(load_world(standing_world(tmp_path / "none", False)))
    assert plain.world.takers is False and plain.credit.takers == []


def test_a_standing_electron_books_no_credit_through_a_ball_the_blind_of_the_fix(tmp_path, monkeypatch):
    """Builder D's detector world at the cube of 5 under main's fix of 2026-10-21 (the books of a turned record with the Link's pair): over one window of 12 the ball's click lines on the electron sum to within a hundredth of its quantum where the plain bilinear of the same lines through the same front sums to tenths, and no credit line is written, the count 1; the blind of the fix the sprint's runs of D's own worlds confirmed (0 credits over 140 intervals at the cubes of 7 and 11)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    path = standing_world(tmp_path, True, None, WINDOW + 1)
    lines: list[dict[str, object]] = []
    board = Lattice(load_world(path), lines.append)
    electron = [f.name for f in board.families].index("electron")
    unit, num = board.credit.units[electron], board.families[electron].pair[0]
    ball = next(d for d in board.node_detectors if d.name == "ball")
    assert ball.nodes is not None
    facing = reports.front(ball.nodes, board.wrap, ball.nodes, board.declared_board())
    plain = 0
    for _interval in range(WINDOW):
        through = readings.currents_of(num, board.lines_of(electron, 0), board.wrap)
        plain += int(reports.entering(facing, through).sum(dtype=object))
        board.step()
    booked = sum(
        int(line[reports.INFLOW])  # type: ignore[call-overload]
        for line in lines
        if line["event"] == reports.CLICK
        and line["family"] == "electron"
        and line["node_detector"] == "ball"
    )
    print(
        f"the ball's window sum in W_rec: the engine's {booked / unit:+.5f}, the plain bilinear's {plain / unit:+.5f}"
    )
    assert abs(booked) * HUNDREDTH < unit < abs(plain) * 10
    assert not [line for line in lines if line["event"] == reports.CREDIT]
    assert board.credit.counts[electron] == 1
    assert isinstance(
        np.asarray(board.states[electron].lines[0].now).sum(dtype=object), int | np.integer
    )
