"""The click's view, the six readings on the credit line (ALGEBRA.md, Readings and measurements, the click's view, 2026-10-24; the owner's frame: the Nodes are the event space, the clicks are what is seen from the hidden layer, all measurements go to the clicks): the point (the credited record's cosine at the credited Node, read from its three levels around the step as the reduced pair), the kind (the rank of the lines credited), the sense (the Wronskian's sign), the support (the shell Node the credit left through), the beat (W_c sin omega at the point read), the identity (the record's family and index); the birth line's children's records and points; readings and no act (`reports.READINGS`, `reports.point_of`, `meeting_board.readings_at`)."""

from __future__ import annotations

import json

import numpy as np

from event_universe import meeting_board, swap, world_files
from event_universe.core.paces import sine_den
from event_universe.lattice import Lattice
from event_universe.reports import BORN_KEYS, READINGS, point_of
from event_universe.world_files import load_world
from tests.laws import ROOT

UNIVERSE = ROOT / "examples" / "events" / "universe24" / "universe_universe24.json"


def bare_board(tmp_path, monkeypatch, lines):  # type: ignore[no-untyped-def]
    """The one universe file on the bare 3-cube torus, every output line kept."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    (tmp_path / "u.json").write_text(UNIVERSE.read_text(encoding="utf-8"), encoding="utf-8")
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": 40}
    (tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return Lattice(load_world(tmp_path / "bare.json"), output=lines.append)


def test_the_point_is_the_reduced_pair_of_the_cosine_read_from_three_levels() -> None:
    """a_next + a_before = 2 cos omega a_now: the pair (a_next + a_before, 2 a_now) over its greatest common divisor, den above 0, None at a level now 0."""
    assert point_of(3, 5, 7) == (1, 1)  # the double root, the uniform mode: cos omega 1
    assert point_of(0, 5, 3) == (3, 10) and point_of(-2, 4, 6) == (1, 2)
    assert point_of(3, -5, 7) == (-1, 1) and point_of(-7, 5, 3) == (-2, 5)
    assert point_of(1, 0, 1) is None


def test_the_readings_at_a_node_are_the_boards_own_at_the_intervals_start(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """Before any birth, one interval stepped with the start kept: the point at a Node is the pair the light's line reads from its level before and now at the start and the level the step left, the beat its integer sine times 3 T, the kind the line's rank, the sense 0 for a real line, the support the Node, the identity the light's record."""
    board = bare_board(tmp_path, monkeypatch, [])
    light, at = board.world.seed, (1, 2, 0)
    for _ in range(10):
        board.step()
    begun = swap.kept(board)
    start = board.states[light].lines[0]
    before, now = int(start.before[at]), int(start.now[at])
    board.step()
    after = int(board.states[light].lines[0].now[at])
    found = meeting_board.readings_at(board, begun, light, 0, at)
    assert tuple(found) == READINGS and now != 0
    point = point_of(before, now, after)
    assert point is not None and found["point"] == list(point)
    assert found["beat"] == sine_den(abs(point[0]), point[1], 3 * board.world.quantum_action)
    assert (found["kind"], found["sense"], found["support"], found["identity"]) == (
        1,
        0,
        list(at),
        [light, 0],
    )


def test_every_credit_of_the_first_meeting_carries_the_six_readings_and_every_birth_its_childrens_records_and_points(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The uniform cube's first meeting: every credit line carries the six keys, the support the credited Node (the node_detector's index unravelled), the identity the light's record, the kind 1 and the sense 0 (a real line), the point a reduced pair with den above 0 and the beat its sine times 3 T; every birth line its children's records (one record per child, distinct identities) and points (each child's point its family's pair, the proton's for a born proton)."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = bare_board(tmp_path, monkeypatch, lines)
    names, light = [f.name for f in board.families], board.world.seed
    while not any(line.get("event") == "credit" for line in lines):
        board.step()
    credits = [line for line in lines if line.get("event") == "credit"]
    births = [line for line in lines if line.get("event") == "birth"]
    assert len(credits) == len(births) == int(np.prod(board.shape))
    for line in credits:
        assert all(key in line for key in READINGS)
        at = [int(a) for a in np.unravel_index(int(line["node_detector"]), board.shape)]
        assert (line["support"], line["identity"], line["kind"], line["sense"]) == (at, [light, 0], 1, 0)
        num, den = line["point"]
        assert den > 0 and np.gcd(abs(num), den) == 1
        assert line["beat"] == sine_den(abs(num), den, 3 * board.world.quantum_action)
    for line in births:
        assert all(key in line for key in BORN_KEYS) and len(line["records"]) == len(line["children"])
        identities = list(zip(line["children"], line["records"], strict=True))
        assert len(set(identities)) == len(identities)
        for child, point in zip(line["children"], line["points"], strict=True):
            assert point == list(board.families[names.index(child)].pair)
        assert "proton" in line["children"] and sum(line["senses"]) == 0
