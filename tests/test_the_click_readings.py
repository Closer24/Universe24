"""The click's view, the readings on the credit line (ALGEBRA.md, Readings and measurements, the click's view, 2026-10-24; the owner's frame: the Nodes are the event space, the clicks are what is seen from the hidden layer, all measurements go to the clicks): the point (the credited record's cosine at the credited Node, read from its three levels around the step as the reduced pair), the kind (the rank of the lines credited), the sense (the Wronskian's sign), the support (the shell Node the credit left through), the beat (W_c sin omega at the point read), the identity (the record's family and index); with them the credit line's former keys read in place of constants, the momentum (the frame's running cosine along each axis with the Link current's sign, [sign_a, num_a, den_a] per axis, p_a = T sin k_a per Link, Part F; the fan and the recoil struck 2026-10-24) and the proper (the Node's own clock at the close in whole intervals, with the windows its count of its own closes; The paces compose, The clock near matter); the birth line's children's records and points; readings and no act (`reports.READINGS`, `reports.point_of`, `meeting_board.readings_at`, `meeting_board.Clock`)."""

from __future__ import annotations

import json
import math

import numpy as np

from event_universe import meeting_board, node, readings, records, seed, swap, world_files
from event_universe.core import paces
from event_universe.core.paces import sine_den
from event_universe.core.ports import arrival
from event_universe.lattice import Lattice
from event_universe.reports import BORN_KEYS, MOMENTUM, PROPER, READINGS, WINDOWS, point_of
from event_universe.world_files import load_world
from tests.laws_universe import small_universe, uniform_sea


def bare_board(tmp_path, monkeypatch, lines):  # type: ignore[no-untyped-def]
    """The tests' small universe on the bare 3-cube torus (den 1,021, its two points; the family-less file of 2026-10-24), every output line kept; the law's seed the sea with a hole at the origin, the uniform sea laid by name where a test asks (tests.laws_universe.uniform_sea)."""
    monkeypatch.setattr(world_files, "REPOSITORY_ROOT", tmp_path)
    small_universe(tmp_path)
    world = {"universe": "u.json", "shape": [3, 3, 3], "intervals": 40}
    (tmp_path / "bare.json").write_text(json.dumps(world), encoding="utf-8")
    return Lattice(load_world(tmp_path / "bare.json"), output=lines.append)


def clock_of(board: Lattice) -> np.ndarray:
    """The Node's composed clock p_0 at every Node from the seed's read at the interval's start, the law's time count's term (The paces compose)."""
    light = board.world.seed
    assert light is not None
    return np.asarray(
        paces.node_paces(board.world.node_clock, board.read(light, 1, 0)[0])[0], dtype=object
    )


def test_the_point_is_the_reduced_pair_of_the_cosine_read_from_three_levels() -> None:
    """a_next + a_before = 2 cos omega a_now: the pair (a_next + a_before, 2 a_now) over its greatest common divisor, den above 0, None at a level now 0."""
    assert point_of(3, 5, 7) == (1, 1)  # the double root, the uniform mode: cos omega 1
    assert point_of(0, 5, 3) == (3, 10) and point_of(-2, 4, 6) == (1, 2)
    assert point_of(3, -5, 7) == (-1, 1) and point_of(-7, 5, 3) == (-2, 5)
    assert point_of(1, 0, 1) is None


def test_the_readings_at_a_node_are_the_boards_own_at_the_intervals_start(tmp_path, monkeypatch):  # type: ignore[no-untyped-def]
    """The uniform sea by name, two intervals stepped and a third with its start kept, before any birth: the point at a Node is the pair the massless line reads from its level before and now at the start and the level the step left, the beat its integer sine times 3 T, the kind the line's rank, the sense 0 for a real line, the support the Node, the identity the seed's record; the momentum per axis the Link current's sign at the start with the pair point_of reads along the axis from the Node's level now and its two neighbours' at the start, [0, 1, 1] on every axis of the uniform sea (no current, the double root); the proper the floor of the clock summed over the intervals (summed here apart from the engine), the windows the Node's closes (none)."""
    monkeypatch.setattr(seed, "uniform_seed", uniform_sea)
    board = bare_board(tmp_path, monkeypatch, [])
    light, at = board.world.seed, (1, 2, 0)
    summed = np.zeros(board.shape, dtype=object)
    for _ in range(2):
        summed = summed + clock_of(board)
        board.step()
    begun = swap.kept(board)
    start = board.states[light].lines[0]
    before, now = int(start.before[at]), int(start.now[at])
    summed = summed + clock_of(board)
    board.step()
    after = int(board.states[light].lines[0].now[at])
    found, clock = meeting_board.readings_at(board, begun, light, 0, at)
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
    num = board.families[light].pair[0]
    terms = readings.momentum_of(num, [start], board.mask((at,)))  # the start's currents
    frame = [
        point_of(
            int(arrival(start.now, a, -1)[at]),
            now,
            int(arrival(start.now, a, 1)[at]),
        )
        for a in range(3)
    ]
    assert terms == (0, 0, 0) and frame == [(1, 1)] * 3  # the uniform sea: no current, the double root
    assert clock.momentum == [[int(np.sign(t)), *pair] for t, pair in zip(terms, frame, strict=True)]
    assert clock.momentum == [[0, 1, 1]] * 3 and clock.windows == 0
    gamma = board.world.node_clock
    assert clock.proper == int(summed[at]) // gamma == int(board.proper_count[at]) // gamma


def test_every_credit_of_the_first_meeting_carries_the_eight_readings_and_every_birth_its_childrens_records_and_points(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The uniform cube by name at its first meeting: every credit line carries the six keys, the support the credited Node (the node_detector's index unravelled), the identity the seed's record, the kind 1 and the sense 0 (a real line), the point a reduced pair with den above 0 and the beat its sine times 3 T; its momentum [0, 1, 1] on every axis exactly (the uniform sea: no Link current, the double root along every axis, a reading and not null), no fan and no recoil key (struck 2026-10-24), its windows 1 and its proper the floor of the Node's clock summed over the intervals since the start, summed here apart from the engine (The paces compose; The clock near matter); every birth line its children's records (one record per child, distinct identities) and points (each child's point its family's pair, the pair of the one point family born)."""
    lines: list[dict] = []  # type: ignore[type-arg]
    monkeypatch.setattr(seed, "uniform_seed", uniform_sea)
    board = bare_board(tmp_path, monkeypatch, lines)
    names, light, gamma = [f.name for f in board.families], board.world.seed, board.world.node_clock
    summed = np.zeros(
        board.shape, dtype=object
    )  # the law's time count summed here, apart from the engine
    while not any(line.get("event") == "credit" for line in lines):
        summed = summed + clock_of(board)
        board.step()
    credits = [line for line in lines if line.get("event") == "credit"]
    births = [line for line in lines if line.get("event") == "birth"]
    assert len(credits) == len(births) == int(np.prod(board.shape))
    for line in credits:
        assert all(key in line for key in READINGS) and not {"fan", "recoil"} & set(line)
        at = [int(a) for a in np.unravel_index(int(line["node_detector"]), board.shape)]
        assert (line["support"], line["identity"], line["kind"], line["sense"]) == (at, [light, 0], 1, 0)
        num, den = line["point"]
        assert den > 0 and np.gcd(abs(num), den) == 1
        assert line["beat"] == sine_den(abs(num), den, 3 * board.world.quantum_action)
        assert line[MOMENTUM] == [[0, 1, 1]] * 3  # the uniform sea: no current, the double root per axis
        assert line[WINDOWS] == 1 and line[PROPER] == int(summed[tuple(at)]) // gamma
    assert 0 < credits[0][PROPER] < credits[0]["interval"]  # the pace below the vacuum's after the bang
    for line in births:
        assert all(key in line for key in BORN_KEYS) and len(line["records"]) == len(line["children"])
        identities = list(zip(line["children"], line["records"], strict=True))
        assert len(set(identities)) == len(identities)
        for child, point in zip(line["children"], line["points"], strict=True):
            assert point == list(board.families[names.index(child)].pair)
        assert (
            len(set(line["children"])) == 1 and sum(line["senses"]) == 0
        )  # the pair of one point family


def test_the_hole_seeds_credits_read_their_own_clocks_and_differ_where_the_volume_differs(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The sea with a hole, the law's seed (the massless point at every Node but the origin): the board's own clicks fall at several intervals; every credit's proper is the floor of its Node's clock summed to its interval (summed here apart from the engine) and its windows the Node's closes so far; two credits read different proper where their Nodes' clocks differ (The clock near matter); every momentum None with the point or three axes of [sign, num, den], the sign -1, 0 or 1 and the pair reduced with den above 0."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = bare_board(tmp_path, monkeypatch, lines)
    gamma = board.world.node_clock
    summed, floors, closes = np.zeros(board.shape, dtype=object), {}, {}
    for _ in range(40):
        summed = summed + clock_of(board)
        board.step()
        floors[board.interval] = {
            tuple(at): int(summed[tuple(at)]) // gamma for at in np.ndindex(*board.shape)
        }
    credits = [line for line in lines if line.get("event") == "credit"]
    assert len(credits) > 1
    for line in credits:
        at = tuple(int(a) for a in np.unravel_index(int(line["node_detector"]), board.shape))
        closes[at] = closes.get(at, 0) + 1
        assert line[PROPER] == floors[line["interval"]][at] and line[WINDOWS] == closes[at]
        momentum = line[MOMENTUM]
        assert (momentum is None) == (line["point"] is None)
        assert momentum is None or all(
            axis[0] in (-1, 0, 1) and axis[2] > 0 and math.gcd(abs(axis[1]), axis[2]) == 1
            for axis in momentum
        )
    assert len({line[PROPER] for line in credits}) > 1


def test_the_momentum_is_the_frames_running_cosine_with_the_link_currents_sign_and_a_second_credit_reads_no_point(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The frame's running cosine along each axis with the Link current's sign, both at the interval's start (the blind of 2026-10-24 measured, the Boss's ruling on the sign): the travelling plane wave of the massless record at k = 2 pi / 3 along x on the 3-cube reads [1, -1, 2] on x (cos k_x = -1/2, p_x = T sin k_x = 0.866 T toward +x, the lay's own current) and [0, 1, 1] on y and z (no current, the double root) on every credit of its step, its point [1, 2]; on the hole seed's first four closes, every one the hole's own Node re-lit by its frame (the hole the Node's own level before, the drift stopped, since the Boss's ruling of 2026-10-24, ALGEBRA.md, The board reads itself: one hole per close at the origin, its windows 1 to 4, its proper rising), the first credit reads [0, 5, 6] on every axis (its inflow symmetric, its spatial cosine its temporal point) and every later credit reads a point (the Node's level now other than 0 at the start) with the momentum alike on the three axes and the sign 0 (the refill symmetric, no current), the beat None where the point lies beyond the band; the former course under the write to (0, 0), kept by name: the neighbours [0, 1, 2] toward the hole and [0, 25, 26] across, the edges [0, 714, 713], the corners [0, 1, 2], and a second credit reading no point, its level now 0."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = bare_board(tmp_path, monkeypatch, lines)
    light = board.world.seed
    rule = node.rule_of(board.families[light], board.world.node_clock, 0, None, board.unit)
    read, self_coefficient, wall = (
        int(np.asarray(v).reshape(-1)[0]) for v in (rule[0][0], rule[1], rule[2])
    )
    k = 2 * math.pi / 3
    omega, x = (
        math.acos((self_coefficient + 2 * read * math.cos(k) + 4 * read) / (2 * wall)),
        np.indices(board.shape)[0],
    )
    board.states[light].lines[0] = records.Record(
        np.rint(1000 * np.cos(k * x)).astype(object),
        np.rint(1000 * np.cos(k * x + omega)).astype(object),
        np.zeros(board.shape, dtype=object),
    )
    board.step()
    credits = [line for line in lines if line.get("event") == "credit"]
    assert len(credits) == int(np.prod(board.shape))  # two whole quanta at every Node of the wave
    assert all(line[MOMENTUM] == [[1, -1, 2], [0, 1, 1], [0, 1, 1]] for line in credits)
    assert all(line["point"] == [1, 2] for line in credits)  # omega = pi / 3 = k at the lay's dispersion
    lines.clear()
    board = bare_board(tmp_path, monkeypatch, lines)  # the hole seed afresh
    while len({line["interval"] for line in lines if line.get("event") == "credit"}) < 4:
        board.step()
    credits = [line for line in lines if line.get("event") == "credit"]
    assert len(credits) == 4 and [line[WINDOWS] for line in credits] == [1, 2, 3, 4]
    assert all(line["support"] == [0, 0, 0] for line in credits)  # the hole's Node alone, re-lit
    assert credits[0]["point"] == [5, 6] and credits[0][MOMENTUM] == [[0, 5, 6]] * 3  # symmetric
    assert [line[PROPER] for line in credits] == sorted({line[PROPER] for line in credits})
    for line in credits:
        num, den = line["point"]
        assert den > 0 and np.gcd(abs(num), den) == 1  # every credit reads a point: the Node re-lit
        assert line[MOMENTUM] == [line[MOMENTUM][0]] * 3 and line[MOMENTUM][0][0] == 0  # no current
        assert (line["beat"] is None) == (abs(num) > den)  # beyond the band no beat
