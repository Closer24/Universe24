"""The Node clock under the weak-field rule (ALGEBRA.md 9.35, 9.57 (1)): the pace p = Gamma - c enters
Rule3's integers at every Node, c = 0 is the plain rule, and light crosses a slab of content under it."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation, form_json
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.test_emitter import NODE_CLOCK, emitter_world, lawful_wheel, reads
from tests.test_flux_reading import planted
from tests.test_massive_record import massive_world

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md 9.57 (2);
# the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


ROOT = Path(__file__).resolve().parents[1]
VACUUM_WHEEL = (
    200000000,
    2427,
)  # (g, W) of [800, 809] at c = 0 under the weak field: g = 2 Gamma^2 gcd(num, 3 den)
PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}
CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}
GAMMA = 1000  # the suite's Node clock (declared per world like the pairs; the eighteen's 10^6)
QUANTA = 250  # the content per Node for e / f = 0.8 at GAMMA
PAIR = (800, 809)  # the matter kind


def light_body(x: int, amount: int) -> dict:
    """A measured event of light at one Node holding `amount` quanta (a body of content)."""
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": amount,
        "stocks": {},
        "momentum": [0, 0, 0],
    }


def content_chain(length: int, boundary: dict, nodes, amount: int, gamma: int = GAMMA) -> dict:
    """The chain [length, 1, 1] of the matter kind [800, 809] beside light with `amount` quanta
    held at each Node of `nodes` (a light body per Node) under the Node clock `gamma`."""
    document = massive_world([length, 1, 1], boundary, list(PAIR))
    document["age_bound"] = 100000
    document["node_clock"] = gamma
    document["amplitude_bound"] = 1 << 26  # the rows at UNIT have room under the suite's Gamma = 1000
    document["measured"] = [light_body(x, amount) for x in nodes]
    return document


def six_reads(levels: np.ndarray, wrap_x: bool) -> list[int]:
    """S_6 on a chain (y and z of extent 1 read the Node itself twice each): a_W + a_E + 4 a,
    the ends reading 0 beyond an open x."""
    values = [int(v) for v in levels[:, 0, 0]]
    length = len(values)
    out = []
    for x in range(length):
        west = values[(x - 1) % length] if wrap_x or x > 0 else 0
        east = values[(x + 1) % length] if wrap_x or x < length - 1 else 0
        out.append(west + east + 4 * values[x])
    return out


def test_the_rule_at_a_node_with_content_in_integers_and_the_rotation_slowed_by_e_over_f():
    """(i) THE RULE IN INTEGERS UNDER THE WEAK FIELD (ALGEBRA.md 9.57 (1); BUILD.md section 26
    item 44): on the periodic chain of 12 with QUANTA quanta held at every Node (the pace
    (Gamma - c) / Gamma = 0.75), one step of the engine on random rows of light and of the
    matter kind equals w a_next + r' = R S_6(a_now) + S a_now - w a_before + r with (R, S, w)
    the rule's integers at the level and the remainder in [0, w), computed in Python
    integers; on the same rows with no content the levels are the plain rule's bit for bit and
    the remainder 2 Gamma^2 times the plain one (from r = 0). (ii) THE ROTATION: a uniform
    record (k = 0) of the matter kind at 2^20 turns with 2 cos omega' = 2 - (1 + f)(1 - num /
    den), f = ((Gamma - c) / Gamma)^2 (the clock's second-order weight, 9.56 (4)), read from
    three consecutive levels at a Node: 1.982617 at the pace 0.75 and 1.977750 = 2 num / den
    in the vacuum, within 10^-5 over 60 intervals; the edge case: at the pace 1 / 2 (c =
    Gamma / 2) 1.986094."""
    rng = np.random.default_rng(11)
    for family, (num, den) in ((0, (1, 1)), (1, PAIR)):
        rows_now = rng.integers(-UNIT, UNIT, size=(12, 1, 1), dtype=np.int64)
        rows_before = rng.integers(-UNIT, UNIT, size=(12, 1, 1), dtype=np.int64)
        (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, QUANTA)
        rows_remainder = rng.integers(0, wall, size=(12, 1, 1), dtype=np.int64)
        slowed = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(12, PERIODIC, range(12), QUANTA))
        )
        assert int(slowed.level_of("content").min()) == QUANTA == int(slowed.level_of("content").max())
        live = planted(slowed, family, rows_now, rows_before, rows_remainder)
        slowed._advance(live)
        reads = six_reads(rows_now, True)
        for x in range(12):
            # the rule's three integers at the Node (item 44)
            total = read * reads[x] + self_coefficient * int(rows_now[x, 0, 0])
            total -= wall * int(rows_before[x, 0, 0])
            total += int(rows_remainder[x, 0, 0])
            expected = total // wall
            assert int(live.now[x, 0, 0]) == expected, (family, x)
            assert int(live.remainder[x, 0, 0]) == total - wall * expected
            assert 0 <= int(live.remainder[x, 0, 0]) < wall
        # the plain limit: no content, r = 0
        vacuum = DetectorLawSimulation(parse_nature_beam_world(content_chain(12, PERIODIC, [], 1)))
        assert not vacuum.level_of("content").any()
        live = planted(vacuum, family, rows_now, rows_before, np.zeros((12, 1, 1), dtype=np.int64))
        vacuum._advance(live)
        for x in range(12):
            plain = num * reads[x] - 3 * den * int(rows_before[x, 0, 0])
            assert int(live.now[x, 0, 0]) == plain // (3 * den)
            assert int(live.remainder[x, 0, 0]) == 2 * GAMMA * GAMMA * (
                plain - 3 * den * (plain // (3 * den))
            )
    # (ii) the rotation at k = 0
    amplitude = 1 << 20
    num, den = PAIR
    for quanta, expected in ((QUANTA, 1.982617), (0, 1.977750), (GAMMA // 2, 1.986094)):
        nodes = range(12) if quanta else []
        simulation = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(12, PERIODIC, nodes, max(quanta, 1)))
        )
        f = ((GAMMA - quanta) / GAMMA) ** 2
        assert 2 - (1 + f) * (1 - num / den) == pytest.approx(expected, abs=5e-7)
        # the same from the rule's integers: (6 R + S) / w at S_6 = 6 a
        (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, quanta)
        assert (6 * read + self_coefficient) / wall == pytest.approx(expected, abs=5e-7)
        uniform = np.full((12, 1, 1), amplitude, dtype=np.int64)
        live = planted(simulation, 1, uniform, uniform.copy(), np.zeros((12, 1, 1), dtype=np.int64))
        readings = []
        for _ in range(60):
            a_before = int(live.before[5, 0, 0])
            a_now = int(live.now[5, 0, 0])
            simulation._advance(live)
            if abs(a_now) > amplitude // 2:
                readings.append((int(live.now[5, 0, 0]) + a_before) / a_now)
            # the record stays uniform (k = 0): every Node the same level
            assert int(live.now.min()) == int(live.now.max())
        assert readings and all(abs(reading - expected) < 1e-5 for reading in readings), (
            quanta,
            readings[:3],
        )


def group_pace_light(k: float, ratio: float) -> float:
    """The group pace of light's dispersion under a uniform clock ratio e / f: cos omega' =
    1 - ratio (1 - cos omega), cos omega = (cos k + 2) / 3, by a central difference (HOST)."""

    def omega(kk: float) -> float:
        return math.acos(1.0 - ratio * (1.0 - (math.cos(kk) + 2.0) / 3.0))

    h = 1e-6
    return (omega(k + h) - omega(k - h)) / (2 * h)


def test_light_through_a_slab_of_content_is_delayed_by_the_slowed_dispersion():
    """(iii) THE SLAB: the flux test's Gaussian packet of light (40 Links, k = 0.3024, UNIT) on
    the open chain of 400 from x = 60, run 400 intervals with and without a slab of 40 Nodes at
    [150, 190) holding QUANTA quanta each (the pace 0.75 there, item 34): the transmitted packet's
    centroid (its levels' magnitude beyond the slab, x >= 190) lags the vacuum's by the slab's
    delay 40 (1 / v' - 1 / v) intervals at the vacuum's pace v, v' the group pace of the slowed
    dispersion (the pace 0.75 under the fixed wall, item 34: 10.9 intervals, 6.23 Links; read
    6.16, COMPUTATION), within 15 percent; 0.974 of the packet's energy is beyond the slab
    in the vacuum run and 0.946 with the slab (the planted packet's own backward part, 2.6
    percent, returns off the face at x = 0 in both; the slab's faces reflect about three
    percent at the weak field's index, f = (p / Gamma)^2 = 0.5625); the books' form `record_form` is the same integer to the
    remainders' jitter (4 x 10^-6 of it) over the passage."""
    k = 0.3024
    x = np.arange(400)
    envelope = np.exp(-(((x - 60) / 14.0) ** 2))
    omega = math.acos((math.cos(k) + 2.0) / 3.0)
    now = np.rint(UNIT * envelope * np.cos(k * (x - 60))).astype(np.int64).reshape(400, 1, 1)
    before = np.rint(UNIT * envelope * np.cos(k * (x - 60) + omega)).astype(np.int64).reshape(400, 1, 1)
    centroids = {}
    beyond = {}
    for slab in (False, True):
        nodes = range(150, 190) if slab else []
        simulation = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(400, CHAIN, nodes, QUANTA))
        )
        live = planted(simulation, 0, now, before, np.zeros((400, 1, 1), dtype=np.int64))
        start = Fraction(*simulation.record_form(live))
        for _ in range(400):
            simulation._advance(live)
            assert abs(Fraction(*simulation.record_form(live)) - start) < start // 1000
        weights = np.abs(live.now[:, 0, 0]).astype(np.float64)
        weights[:190] = 0.0
        centroids[slab] = float(np.sum(x * weights) / np.sum(weights))
        energy = live.now[:, 0, 0].astype(np.float64) ** 2 + live.before[:, 0, 0].astype(np.float64) ** 2
        beyond[slab] = float(energy[190:].sum() / energy.sum())
    pace = group_pace_light(k, 1.0)
    # the dispersion's factor under the weak field, f = (p / Gamma)^2 (ALGEBRA.md 9.62 (1))
    slowed = group_pace_light(k, ((GAMMA - QUANTA) / GAMMA) ** 2)
    delay = 40.0 * (1.0 / slowed - 1.0 / pace)
    lag = centroids[False] - centroids[True]
    # the slab's faces reflect more under the weak field (the index at f = (p / Gamma)^2, 0.5625
    # here, against 0.75 under the first-order rule): 0.946 beyond against 0.956 (COMPUTATION)
    assert beyond[False] > 0.97 and beyond[True] > 0.94, beyond
    assert 0.85 * delay * pace < lag < 1.15 * delay * pace, (centroids, delay * pace)


def test_the_form_under_the_clock_the_shares_identity_and_the_inverse_with_content():
    """(iv) UNDER THE FIXED WALL (BUILD.md section 26 item 34), on the periodic chain of 60 with
    QUANTA quanta at the Nodes [20, 30), random rows of light and of the matter kind: (a) the
    engine's `conserved_form` is the form with the pace p_i = Gamma - c_i: 3 L (den / num)
    Gamma p_i (a^2 + b^2) - 6 L (den / num) p_i c_i a b at the Nodes and L p_i p_j (a_i b_j +
    a_j b_i) on the Links, exactly (Gamma^2 times the plain form in the vacuum); (b) the
    share's identity per Node: its change over an interval is L times the currents p_i p_j
    (now_i before_j - before_i now_j) through its Links plus the remainders' term (L / num)
    p_i (a_next - a_before) (r - r'), exactly, at the slab's Nodes as in the vacuum; (c) the
    books' form `record_form` changes by (L / num) SUM p_i (a_next - a_before) (r - r') over 40
    intervals exactly (L the numerators' lcm); (d) 30 steps then 30 inverse steps return the
    two levels and the remainders bit for bit."""
    rng = np.random.default_rng(23)
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(content_chain(60, PERIODIC, range(20, 30), QUANTA))
    )
    content = [int(v) for v in simulation.level_of("content")[:, 0, 0]]
    assert content == [QUANTA if 20 <= i < 30 else 0 for i in range(60)]
    for family, (num, den) in ((0, (1, 1)), (1, PAIR)):
        wall = simulation.kind_wall(family)
        now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
        before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
        live = planted(simulation, family, now, before, np.zeros((60, 1, 1), dtype=np.int64))
        # (a) the form from the rule's integers (item 44): L [w (a^2 + b^2) - S_i a b] / R_i at
        # the Nodes, the Links plain
        integers = [coefficients(num, den, GAMMA, c) for c in content]
        reads = six_reads(before, True)
        expected = Fraction(0)
        for i in range(60):
            a, b = int(now[i, 0, 0]), int(before[i, 0, 0])
            (read_i, _, _), self_i, wall_i = integers[i]
            expected += Fraction(wall * (wall_i * (a * a + b * b) - self_i * a * b), read_i)
            expected -= wall * a * reads[i]
        assert Fraction(*simulation.conserved_form(live)) == expected
        # (b) the share's identity per Node, one interval
        old = [Fraction(*simulation.form_share(live, one_node(60, i))) for i in range(60)]
        a_before, a_now, r_old = live.before.copy(), live.now.copy(), live.remainder.copy()
        simulation._advance(live)
        a_next, r_new = live.now.copy(), live.remainder.copy()
        new = [Fraction(*simulation.form_share(live, one_node(60, i))) for i in range(60)]
        for i in range(60):
            # the plain currents through the Node's two Links (unweighted, item 36)
            flux = 0
            for j in ((i - 1) % 60, (i + 1) % 60):
                flux += int(a_now[i, 0, 0]) * int(a_before[j, 0, 0]) - int(a_before[i, 0, 0]) * int(
                    a_now[j, 0, 0]
                )
            # the folded axes' self-reads carry no flux; the remainders' term (wall / R_i)
            # (a_next - a_before)(r - r')
            remainders = Fraction(
                (int(a_next[i, 0, 0]) - int(a_before[i, 0, 0]))
                * (int(r_old[i, 0, 0]) - int(r_new[i, 0, 0])),
                integers[i][0][0],
            )
            assert new[i] - old[i] == wall * flux + wall * remainders, (family, i)
            assert 0 <= int(r_new[i, 0, 0]) < integers[i][2]
        # (c) the books' form's remainder identity, exact, over 40 intervals
        previous = Fraction(*simulation.record_form(live))
        for _ in range(40):
            a_before = live.before.astype(object)
            r = live.remainder.astype(object)
            simulation._advance(live)
            current = Fraction(*simulation.record_form(live))
            term = Fraction(0)
            for i in range(60):
                term += Fraction(
                    int(live.now[i, 0, 0] - a_before[i, 0, 0])
                    * int(r[i, 0, 0] - live.remainder[i, 0, 0]),
                    coefficients(num, den, GAMMA, int(simulation.level_of("content")[i, 0, 0]))[0][0],
                )
            assert current - previous == wall * term
            previous = current
        # (d) the inverse map with content: 30 steps back return the state bit for bit
        state = (live.now.copy(), live.before.copy(), live.remainder.copy())
        for _ in range(30):
            simulation._advance(live)
        for _ in range(30):
            simulation._advance_inverse(live)
        assert np.array_equal(live.now, state[0])
        assert np.array_equal(live.before, state[1])
        assert np.array_equal(live.remainder, state[2])


def one_node(length: int, i: int) -> np.ndarray:
    mask = np.zeros((length, 1, 1), dtype=bool)
    mask[i, 0, 0] = True
    return mask


def test_the_loader_requires_the_node_clock_under_the_detector_law_and_bounds_it():
    """(v) `node_clock` is REQUIRED under `detector_law` (a world without it refused naming the
    key), refused without that law, an integer from 1 (0 refused); the load bound under the
    clock names the clock and the content: the slab world of (iii) at Gamma = 10^6 (40 bodies
    of 250000 quanta, M = 2 x 10^7 on the matter pair [800, 809], twice the content for the
    family of clicks' waves) refused naming Gamma and M; the
    registered light clock declares 10^6 and loads, its A's clock pair (10^6 - 64, 10^6) at
    its Nodes and (10^6, 10^6) in the vacuum under the fixed wall (item 34; the pair a record
    of the matter kind reads, its charge 0, item 35), its wheel at
    A's centre Node the rule's with the stock (4171875 on [800, 801], the remainder's step
    576, COMPUTATION), the kind's own 2427 on [800, 809] in the vacuum beside it (the step
    Gamma)."""
    document = content_chain(12, PERIODIC, [], 1)
    del document["node_clock"]
    with pytest.raises(ValueError, match="node_clock is required: Gamma"):
        parse_nature_beam_world(document)
    ray = content_chain(12, PERIODIC, [], 1)
    ray["detector_law"] = False  # the flag was the law's name: refused by name (9.90 (1))
    with pytest.raises(ValueError, match="the world has unknown keys: detector_law"):
        parse_nature_beam_world(ray)
    zero = content_chain(12, PERIODIC, [], 1)
    zero["node_clock"] = 0
    with pytest.raises(ValueError, match="node_clock"):
        parse_nature_beam_world(zero)
    heavy = content_chain(400, CHAIN, range(150, 190), 250000, gamma=1_000_000)
    with pytest.raises(
        ValueError,
        match=r"\.pair \[.*Gamma = 1000000 and the content M = 20000000 .*not below 2\^63",
    ):
        parse_nature_beam_world(heavy)
    registered = json.loads(
        (ROOT / "examples/events/massive_record/light_clock.json").read_text(encoding="utf-8")
    )
    # the integers of 9.61 (3) from the families file alone (item 59)
    assert registered["universe"] == "examples/events/universe.json"
    assert "node_clock" not in registered and "amplitude_bound" not in registered
    world = parse_nature_beam_world(registered)
    assert world.node_clock == NODE_CLOCK == 10**4
    simulation = DetectorLawSimulation(world)
    block = simulation.blocks[0]
    centre = tuple(int(axis[0]) for axis in np.nonzero(simulation.centre_mask(block)))
    # the registered world's matter family (the families file's third entry, item 60) at the
    # body's kind [800, 809] (the pair on the body, 9.91 (7))
    matter = [family.name for family in world.families].index("matter")
    kind = block.definition.kind
    # the beam body's Node's kind [800, 1200] since commit 7 (the one-Node emitter of the window)
    assert kind == (800, 1200) and world.families[matter].pair_on_body
    # A's level 65: its one own quantum beside its stock of 64 light quanta (item 47)
    assert simulation.node_clock_pair(centre, matter) == (NODE_CLOCK - 65, NODE_CLOCK)
    assert simulation.node_clock_pair((100, 0, 0), matter) == (NODE_CLOCK, NODE_CLOCK)
    # the wheel from the weak-field rule's integers (item 44): (g, W) = (50, 9612000000) at the
    # emitter's level 65 (its one own quantum beside the stock of 64, item 47; (1536,
    # 312890625) at 64), the kind's own in the vacuum
    # at the kind [800, 1200] since commit 7: (100, 4812000000) at the level 65, (80000000000, 9)
    # in the vacuum (COMPUTATION; (50, 9612000000) and VACUUM_WHEEL at [800, 809] HISTORY)
    assert simulation.wheel_at(matter, centre, kind) == (100, 4812000000)
    assert simulation.wheel_at(matter, (100, 0, 0), kind) == (80000000000, 9)
    assert VACUUM_WHEEL == (200000000, 2427)  # the kind [800, 809]'s vacuum wheel, read elsewhere


def test_the_content_at_a_body_falls_at_a_giving_and_rises_at_a_click():
    """(vi) On the emitter world (the stock 4 at [5, 37), the screen the cube of light bodies at
    [70, 72] whose first body takes the clicks' quanta): the content at the body's centre Node
    (x = 21) is 4 at the load and falls by one at each giving (the giving line's `content` the
    value the clicking record was advanced under, 4, 3, 2, 1, and its `node_clock` [Gamma -
    content, Gamma]; the given record's wheel the rule's at that content); the content at the
    screen's first body (x = 70) is 1 at the load and rises by one at the interval after each
    gather line there (the click's quantum held by the body); the vacuum between them 0 at
    the load and at x = 50 until the family of clicks' front from the body's head arrives
    (14 Links at one Link per interval, ALGEBRA.md 9.44 (3)), then the family's waves and the
    rounding's walk of the plain step at these unit levels (at most 9 read on this head, far
    below Gamma); the books balanced at every interval."""
    document = emitter_world(stock=4)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    # the emitter's level 5: one own quantum and the stock of 4 held light quanta (item 47)
    assert (
        int(simulation.level_of("content")[21, 0, 0]) == 5
        and int(simulation.level_of("content")[70, 0, 0]) == 1
    )
    assert (
        int(simulation.level_of("content")[71, 0, 0]) == 1
        and not simulation.level_of("content")[40:70].any()
    )
    givings_seen = 0
    clicks_seen = 0
    block = simulation.blocks[0]
    for _ in range(document["ticks"]):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        # SINCE COMMIT 7 the quantum moves at the window's open (the body's count of givings)
        # and the line is named at the close
        givings_seen = block.givings
        clicks_seen = sum(1 for line in lines if line["event"] == "gather")
        # the array after the interval is the one its advances used: rebuilt as the
        # interval began from the events before it, and again at a giving within it
        # (the given record's norm under the content the giving leaves), so a click's
        # quantum enters the array at the next interval unless a giving follows it
        assert int(simulation.level_of("content")[21, 0, 0]) == 5 - givings_seen
        # the family of clicks steps last in the interval and is then held at the content
        # the interval's clicks and givings left, so a click's quantum is on the screen's
        # body as the interval ends (ALGEBRA.md 9.45 (2))
        assert int(simulation.level_of("content")[70, 0, 0]) == 1 + clicks_seen
        if simulation.tick <= 12:
            assert int(simulation.level_of("content")[50, 0, 0]) == 0
        # the family's waves and, at these small contents, the rounding's own walk of the
        # plain step at unit levels: far below Gamma (at most 9 read on this head)
        assert int(np.abs(simulation.level_of("content")[40:70]).max()) <= 64
        for line in [line for line in lines if line["tick"] == simulation.tick]:
            if line["event"] == "giving":
                # the content the k-th giving found at its open (the line named at the close)
                assert line["content"] == 5 - (line["excitation"] - 1)
                assert line["node_clock"] == [NODE_CLOCK - line["content"], NODE_CLOCK]
                assert lawful_wheel(simulation.world, line)
    assert givings_seen == 4 and clicks_seen >= 1
    assert int(simulation.level_of("content")[70, 0, 0]) == 1 + clicks_seen
    assert int(simulation.level_of("content")[21, 0, 0]) == 1  # the one own quantum stays (item 47)


def test_the_family_of_clicks_is_held_at_the_bodies_and_moves_by_its_own_step_elsewhere():
    """(vii) THE FAMILY OF CLICKS (the model owner's record 1982; ALGEBRA.md 9.41 (3), 9.44 (3),
    9.45): on the open chain of 200 with a body of QUANTA quanta at every Node of [90, 110)
    (light bodies), the clock record's level is the content at the bodies' Nodes at both
    levels with the remainder 0 at the load and after every interval (the hold, not the
    step's own there), and 0 elsewhere at the load; THE FRONT: nothing before the lattice cone
    of one Link per interval (the level at x = 60, 30 Links from the body's edge, is 0 through
    interval 29) and the family's long waves at the pace 1 / sqrt 3 of light's pair on a
    chain (the level at x = 60 nonzero by interval 70; read 50 to 60, COMPUTATION), the field
    never above twice the content anywhere (the wave off the zero face doubles at most); the
    books' `form` of the
    family of clicks is its own record's plain form, and the state carries its rows. The
    edge case: a world with no content anywhere keeps the family at 0 for ever."""
    document = content_chain(200, CHAIN, range(90, 110), QUANTA)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    clock = simulation.held_records[2]
    assert simulation.held_families == [2] + [3] and simulation.families[2].held == "content"
    held = np.zeros((200, 1, 1), dtype=bool)
    held[90:110] = True
    assert np.all(clock.now[held] == QUANTA) and np.all(clock.before[held] == QUANTA)
    assert not clock.now[~held].any() and not clock.remainder.any()
    assert simulation.level_of("content") is clock.now
    reached = None
    for _ in range(80):
        simulation.step()
        assert np.all(clock.now[held] == QUANTA) and np.all(clock.before[held] == QUANTA)
        assert not clock.remainder[held].any()
        assert int(np.abs(clock.now).max()) <= 2 * QUANTA
        if simulation.tick <= 29:
            assert int(clock.now[60, 0, 0]) == 0 and int(clock.now[139, 0, 0]) == 0
        elif reached is None and int(clock.now[60, 0, 0]) != 0:
            reached = simulation.tick
        assert simulation.level_of("content") is clock.now
    assert reached is not None and 30 <= reached <= 70, reached
    books = simulation.books()
    assert books["families"]["clicks"]["form"] == form_json(simulation.record_form(clock))
    assert books["families"]["clicks"]["measured"]["current"] == 0
    state = dict(simulation.snapshot_stream())
    fields = {field["family"]: field for field in state["held_fields"]}
    assert (
        fields["clicks"]["held"] == "content" and fields["clicks"]["rows"] == clock.now.ravel().tolist()
    )
    empty = DetectorLawSimulation(parse_nature_beam_world(content_chain(60, PERIODIC, [], 1)))
    for _ in range(20):
        empty.step()
    assert not empty.held_records[2].now.any() and not empty.level_of("content").any()


def test_the_joint_step_inverts_bit_for_bit_wherever_the_clock_falls():
    """(viii) THE EXACT BACKWARD RUN EVERYWHERE (the model owner's record 1994 and his word of
    2026-09-25; BUILD.md section 26 item 34): on the periodic chain of 60 with a body of QUANTA
    quanta at [20, 30) and a light record of random rows registered (no detector set and no
    face: nothing clicks), the family of clicks' field rises and FALLS at Nodes over 30
    intervals (the falls counted, above 0), and the joint step inverts bit for bit, the
    record's two levels and remainders and the family's own field, over the whole run: the
    wall 3 den Gamma is the same at every interval, so the remainder's range never shrinks
    and no two states merge (the loss of item 32's finding A, where the wall 3 den (Gamma +
    c) shrank, HISTORY). The edge case: the field did move (the end state differs from the
    start before the inverse)."""
    rng = np.random.default_rng(31)
    now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(content_chain(60, PERIODIC, range(20, 30), QUANTA))
    )
    live = planted(simulation, 0, now, before, np.zeros((60, 1, 1), dtype=np.int64))
    simulation.records[live.identity] = live
    clock = simulation.held_records[2]
    start = (live.now.copy(), live.before.copy(), live.remainder.copy(), clock.now.copy())
    falls = 0
    previous = clock.now.copy()
    for _ in range(30):
        simulation.step()
        falls += int(np.sum(clock.now < previous))
        previous = clock.now.copy()
    assert live.identity in simulation.records and not live.clicked
    assert falls > 0 and not np.array_equal(clock.now, start[3])
    for _ in range(30):
        simulation.step_inverse()
    for x, y in zip((live.now, live.before, live.remainder, clock.now), start, strict=True):
        assert np.array_equal(x, y)
    assert simulation.tick == 0


def test_the_loader_reads_the_held_family_by_attribute_and_refuses_what_it_cannot_be():
    """(ix) THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section 26 item 51):
    the family whose level is the Node clock is the family declaring `held: "content"`, no
    world key and no name in the engine; the world keys clock_family, charge_family and
    charge_strength are refused by name (retired); a held family is refused with a pair other
    than [1, 1] (the matter kind), with a quantum other than 1, with a clock of its own, with a
    charge; two families holding the content are refused; a read naming a family that is not
    held is refused, and a read naming no family; under the detector law a family without
    `reads` is refused and the attributes are refused without the law; a measured event of a
    held family, `held` naming it and an emitter given into it are refused; six families are
    refused (the owner's cap of twenty, record 2081; the five of 9.48 HISTORY); a
    world with the family declared loads, its index among the engine's held families."""
    good = content_chain(12, PERIODIC, [], 1)
    parse_nature_beam_world(good)
    for key, value in (("clock_family", "clicks"), ("charge_family", "charge"), ("charge_strength", 1)):
        retired = json.loads(json.dumps(good))
        retired[key] = value
        with pytest.raises(ValueError, match=f"the world has unknown keys: {key}"):
            parse_nature_beam_world(retired)
    ray = json.loads(json.dumps(good))
    ray["detector_law"] = False  # the flag was the law's name: refused by name (9.90 (1))
    with pytest.raises(ValueError, match="the world has unknown keys: detector_law"):
        parse_nature_beam_world(ray)
    unread = json.loads(json.dumps(good))
    del unread["universe"][0]["reads"]
    with pytest.raises(ValueError, match=r"families\[0\] lacks keys the engine reads: reads"):
        parse_nature_beam_world(unread)
    unknown = json.loads(json.dumps(good))
    unknown["universe"][0]["reads"][0]["family"] = "ticks"
    with pytest.raises(ValueError, match="reads names 'ticks', which no family declares"):
        parse_nature_beam_world(unknown)
    unheld = json.loads(json.dumps(good))
    unheld["universe"][0]["reads"][0]["family"] = "matter"
    with pytest.raises(ValueError, match="reads names 'matter', which is not held"):
        parse_nature_beam_world(unheld)
    massive = json.loads(json.dumps(good))
    massive["universe"][1]["held"] = "content"
    massive["universe"][1]["reads"] = []
    with pytest.raises(
        ValueError, match="is held with the pair \\[800, 809\\]: a held family is massless"
    ):
        parse_nature_beam_world(massive)
    quantum = json.loads(json.dumps(good))
    quantum["universe"][2]["quantum"] = 2
    with pytest.raises(ValueError, match="counted in quanta, one click one unit"):
        parse_nature_beam_world(quantum)
    clocked = json.loads(json.dumps(good))
    clocked["universe"][2]["phase_per_link"] = [512, 1]
    with pytest.raises(ValueError, match="has no clock of its own"):
        parse_nature_beam_world(clocked)
    charged = json.loads(json.dumps(good))
    charged["universe"][2]["charge"] = 1
    with pytest.raises(
        ValueError, match="is held and declares the charge 1: a held family carries none"
    ):
        parse_nature_beam_world(charged)
    reading = json.loads(json.dumps(good))
    reading["universe"][2]["reads"] = [{"family": "charge", "weight": 1}]
    with pytest.raises(ValueError, match="is held and reads"):
        parse_nature_beam_world(reading)
    booked = json.loads(json.dumps(good))
    booked["universe"][2]["booked"] = True  # HISTORY (item 53): derived, not declared
    with pytest.raises(ValueError, match="unknown keys: booked"):
        parse_nature_beam_world(booked)
    twice = json.loads(json.dumps(good))
    twice["universe"][3]["held"] = "content"
    with pytest.raises(ValueError, match="two families hold 'content'"):
        parse_nature_beam_world(twice)
    source = json.loads(json.dumps(good))
    source["universe"][2]["held"] = "momentum"
    with pytest.raises(ValueError, match="held must be one of"):
        parse_nature_beam_world(source)
    components = json.loads(json.dumps(good))
    components["universe"][0]["components"] = 3
    with pytest.raises(ValueError, match="components is refused: the representation is `parts`"):
        parse_nature_beam_world(components)
    body = json.loads(json.dumps(good))
    body["measured"] = [dict(light_body(3, 1), family="clicks")]
    with pytest.raises(ValueError, match="is of the held family 'clicks': no body is of it"):
        parse_nature_beam_world(body)
    holding = json.loads(json.dumps(good))
    holding["measured"] = [dict(light_body(3, 1), stocks={"clicks": 2})]
    with pytest.raises(ValueError, match="stocks names the held family 'clicks'"):
        parse_nature_beam_world(holding)
    given = emitter_world(stock=1)
    given["measured"][0]["emitter"]["family"] = "clicks"
    given["stamp"] = input_stamp(given)
    with pytest.raises(
        ValueError, match="givings into the held family 'clicks'|the given family is a paid family"
    ):
        parse_nature_beam_world(given)
    many = json.loads(json.dumps(good))
    many["universe"] += [
        {"name": f"family_{n}", "quantum": 1, "pair": [800, 809], "charge": 0, "reads": reads()}
        for n in range(len(many["universe"]), 21)
    ]
    with pytest.raises(ValueError, match="families declares 21; at most 20 families"):
        parse_nature_beam_world(many)
    world = parse_nature_beam_world(good)
    assert world.held_families == (2, 3) and DetectorLawSimulation(world).held_families == [2, 3]


def test_the_engine_reads_no_family_name_the_held_families_renamed_step_bit_for_bit():
    """(x) THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section 26 item 51):
    the chain of 60 with QUANTA quanta at [20, 30) and a light record of random rows, stepped
    40 intervals, then the same world with the two held families renamed ADVERSARIALLY (the
    family holding the content named `charge`, the family holding the sign named `content`, the
    reads following the names; the model owner's word of 2026-09-25: a source word must not be
    confused with a family, item 53) and the two held families in the other order: the light
    record's rows, the held levels and the books are bit for bit the same (the engine reads the
    attributes `held` and `reads`, never a name or a position), the books read alike. The edge
    case: a reading family renamed too (`light` to `sign`, the read mode's own word) changes
    nothing either."""
    rng = np.random.default_rng(23)
    now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)

    def run(document: dict) -> tuple:
        simulation = DetectorLawSimulation(parse_nature_beam_world(document))
        live = planted(simulation, 0, now.copy(), before.copy(), np.zeros((60, 1, 1), dtype=np.int64))
        simulation.records[live.identity] = live
        for _ in range(40):
            simulation.step()
        content = simulation.level_of("content").copy()
        charge = simulation.level_of("sign").copy()
        return (
            live.now.copy(),
            live.before.copy(),
            live.remainder.copy(),
            content,
            charge,
            simulation.books()["balanced"],
        )

    plain = content_chain(60, PERIODIC, range(20, 30), QUANTA)
    renamed = json.loads(json.dumps(plain))
    names = {"clicks": "charge", "charge": "content", "light": "sign"}
    for family in renamed["universe"]:
        family["name"] = names.get(family["name"], family["name"])
        for read in family["reads"]:
            read["family"] = names.get(read["family"], read["family"])
    for entry in renamed["measured"]:
        entry["family"] = names.get(entry["family"], entry["family"])
        if "stocks" in entry:
            entry["stocks"] = {names.get(k, k): v for k, v in entry["stocks"].items()}
    # the two held families in the other order (the indices move, the attributes stay)
    held = [f for f in renamed["universe"] if f.get("held")]
    others = [f for f in renamed["universe"] if not f.get("held")]
    renamed["universe"] = others + held[::-1]
    world = parse_nature_beam_world(renamed)
    assert [world.families[i].held for i in world.held_families] == ["sign", "content"]
    assert [world.families[i].name for i in world.held_families] == ["content", "charge"]
    first, second = run(plain), run(renamed)
    for a, b in zip(first[:5], second[:5], strict=True):
        assert np.array_equal(a, b)
    assert first[5] == second[5]  # the books read alike (a planted record is outside the ledger)
