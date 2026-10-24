"""The click's view, the readings on the credit line (ALGEBRA.md, Readings and measurements, the click's view, 2026-10-24; the owner's frame: the Nodes are the event space, the clicks are what is seen from the hidden layer, all measurements go to the clicks): the point (the credited record's cosine at the credited Node, read from its three levels around the step as the reduced pair), the kind (the rank of the lines credited), the sense (the Wronskian's sign), the support (the shell Node the credit left through), the beat (W_c sin omega at the point read), the identity (the record's family and index); with them the credit line's former keys read in place of constants, the momentum (the piece's p_a with the fan and the recoil, Part F and G) and the proper (the Node's own clock at the close in whole intervals, with the windows its count of its own closes; The paces compose, The clock near matter); the birth line's children's records and points; readings and no act (`reports.READINGS`, `reports.point_of`, `meeting_board.readings_at`, `meeting_board.Clock`)."""

from __future__ import annotations

import json
import math

import numpy as np

from event_universe import meeting_board, node, readings, records, seed, swap, world_files
from event_universe.core import paces
from event_universe.core.paces import sine_den
from event_universe.lattice import Lattice
from event_universe.reports import BORN_KEYS, FAN, MOMENTUM, PROPER, READINGS, RECOIL, WINDOWS, point_of
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
    """The uniform sea by name, two intervals stepped and a third with its start kept, before any birth: the point at a Node is the pair the massless line reads from its level before and now at the start and the level the step left, the beat its integer sine times 3 T, the kind the line's rank, the sense 0 for a real line, the support the Node, the identity the seed's record; the fan the record's lattice momentum over the board, the momentum the piece's p_a = P_a(region) x W_rec div (num x W(region)) at the Node, the recoil -p, the proper the floor of the clock summed over the intervals (summed here apart from the engine), the windows the Node's closes (none)."""
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
    lines, num, unit = board.lines_of(light, 0), board.families[light].pair[0], board.credit.units[light]
    assert clock.fan == list(readings.momentum_of(num, lines, board.wrap))
    terms = readings.momentum_of(num, lines, board.wrap, board.mask((at,)))
    share = int(board.share_of(light, 1, board.mask((at,)))[0][at])
    assert share > 0 and clock.momentum == [term * unit // (num * share) for term in terms]
    assert clock.recoil == [-term for term in clock.momentum] and clock.windows == 0
    gamma = board.world.node_clock
    assert clock.proper == int(summed[at]) // gamma == int(board.proper_count[at]) // gamma


def test_every_credit_of_the_first_meeting_carries_the_eight_readings_and_every_birth_its_childrens_records_and_points(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The uniform cube by name at its first meeting: every credit line carries the six keys, the support the credited Node (the node_detector's index unravelled), the identity the seed's record, the kind 1 and the sense 0 (a real line), the point a reduced pair with den above 0 and the beat its sine times 3 T; its momentum, fan and recoil [0, 0, 0] exactly (the uniform sea's P_a 0, a reading and not null), its windows 1 and its proper the floor of the Node's clock summed over the intervals since the start, summed here apart from the engine (The paces compose; The clock near matter); every birth line its children's records (one record per child, distinct identities) and points (each child's point its family's pair, the pair of the one point family born)."""
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
        assert all(key in line for key in READINGS)
        at = [int(a) for a in np.unravel_index(int(line["node_detector"]), board.shape)]
        assert (line["support"], line["identity"], line["kind"], line["sense"]) == (at, [light, 0], 1, 0)
        num, den = line["point"]
        assert den > 0 and np.gcd(abs(num), den) == 1
        assert line["beat"] == sine_den(abs(num), den, 3 * board.world.quantum_action)
        assert line[MOMENTUM] == line[FAN] == line[RECOIL] == [0, 0, 0]  # the uniform sea, P_a 0 exactly
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
    """The sea with a hole, the law's seed (the massless point at every Node but the origin): the board's own clicks fall at several intervals; every credit's proper is the floor of its Node's clock summed to its interval (summed here apart from the engine) and its windows the Node's closes so far; two credits read different proper where their Nodes' clocks differ (The clock near matter)."""
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
        assert line[RECOIL] == [-p for p in line[MOMENTUM]] and len(line[FAN]) == 3
    assert len({line[PROPER] for line in credits}) > 1


def test_the_momentums_unit_is_the_region_formulas_at_the_one_node_and_a_second_credit_reads_no_point(
    tmp_path, monkeypatch
):  # type: ignore[no-untyped-def]
    """The key's unit, named (the clicks reader's finding of 2026-10-24): for a plane wave of the massless record at k = 2 pi / 3 on the 3-cube the formula P_a x W_rec div (num x W) reads 2 T exactly (2 T sin k / sin omega, sin k = sin omega there); on the hole seed's first three closes the hole's own credit reads 0 (its inflow symmetric), its six neighbours one axis each, the two sides of the hole opposite in sign and equal in size to the unit, the size above T (the ratio of one Node's two Link currents to its share, no plane wave's quantum), the fan 0 over the torus; a Node's second credit reads no point and no beat (its level now 0 at the start from the hole's last close), its windows 2, and every first credit a pair."""
    lines: list[dict] = []  # type: ignore[type-arg]
    board = bare_board(tmp_path, monkeypatch, lines)
    light, T = board.world.seed, board.world.quantum_action
    num, unit, gamma = board.families[light].pair[0], board.credit.units[light], board.world.node_clock
    rule = node.rule_of(board.families[light], gamma, 0, None, board.unit)
    read, self_coefficient, wall = (
        int(np.asarray(v).reshape(-1)[0]) for v in (rule[0][0], rule[1], rule[2])
    )
    k = 2 * math.pi / 3
    omega, x = (
        math.acos((self_coefficient + 2 * read * math.cos(k) + 4 * read) / (2 * wall)),
        np.indices(board.shape)[0],
    )
    wave = records.Record(
        np.rint(1000 * np.cos(k * x)).astype(object),
        np.rint(1000 * np.cos(k * x + omega)).astype(object),
        np.zeros(board.shape, dtype=object),
    )
    board.states[light].lines[0] = wave
    along = readings.momentum_of(num, [wave], board.wrap)
    share = int(np.asarray(board.share_of(light)[0], dtype=object).sum())
    assert along[0] * unit // (num * share) == 2 * T and along[1:] == (
        0,
        0,
    )  # the two-Link sum per quantum over sin omega, 2 T here
    board = bare_board(tmp_path, monkeypatch, lines)  # the hole seed afresh
    while len({line["interval"] for line in lines if line.get("event") == "credit"}) < 3:
        board.step()
    credits = [line for line in lines if line.get("event") == "credit"]
    closes = sorted({line["interval"] for line in credits})[:3]
    first = [line for line in credits if line["interval"] == closes[0]]
    assert len(first) == 1 and first[0][MOMENTUM] == [0, 0, 0] and first[0]["support"] == [0, 0, 0]
    sides = [line for line in credits if line["interval"] == closes[1] and line[WINDOWS] == 1]
    assert len(sides) == 6 and all(line[FAN] == [0, 0, 0] for line in sides)
    sizes = {abs(p) for line in sides for p in line[MOMENTUM] if p}
    assert (
        len(sizes) <= 2 and max(sizes) - min(sizes) <= 1 and min(sizes) > T
    )  # one axis each, the unit's size, above T
    assert all(sum(1 for p in line[MOMENTUM] if p) == 1 for line in sides)
    assert (
        sum(np.sign(p) for line in sides for p in line[MOMENTUM] if p) == 0
    )  # opposite across the hole
    for line in credits:
        if line["interval"] in closes:
            again = line[WINDOWS] > 1
            assert (line["point"] is None) == again and (line["beat"] is None) == again
