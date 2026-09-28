"""The Node clock under the weak-field rule (ALGEBRA.md #the-paces, #the-line): the pace p = Gamma - c enters Rule3's integers at every Node, c = 0 is the plain rule, and light crosses a slab of content under it."""

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
from tests.bodies import CHAIN, GAMMA, PAIR, content_chain, light_body, six_reads
from tests.running import planted
from tests.worlds import NODE_CLOCK, PERIODIC, emitter_world, family_entry, lawful_wheel, reads

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md #the-line; the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


ROOT = Path(__file__).resolve().parents[1]
VACUUM_WHEEL = (
    200000000,
    2427,
)  # (g, W) of [800, 809] at c = 0 under the weak field: g = 2 Gamma^2 gcd(num, 3 den)
QUANTA = 250  # the content per Node for e / f = 0.8 at GAMMA


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_rule_at_a_node_with_content_in_integers_and_the_rotation_slowed_by_e_over_f():
    """(i) THE RULE IN INTEGERS UNDER THE WEAK FIELD (ALGEBRA.md #the-line; item 44): on the periodic chain of 12 with QUANTA at every Node (THE START left out: the load's slab, the count at the bodies' Nodes, is the level the rule is read at; a chain periodic at [1, 1] has no rest under a source, ALGEBRA.md #the-generator (g)), one step of the engine on random rows equals w a_next + r' = R S_6(a_now) + S a_now - w a_before + r in Python integers; with no content the plain rule's levels bit for bit. (ii) THE ROTATION of a uniform record of the matter kind, 2 cos omega' = 2 - (1 + f)(1 - num / den), f = ((Gamma - c) / Gamma)^2: 1.982617 at the pace 0.75, 1.977750 in the vacuum, within 10^-5."""
    rng = np.random.default_rng(11)
    for family, (num, den) in ((0, (1, 1)), (1, PAIR)):
        rows_now = rng.integers(-UNIT, UNIT, size=(12, 1, 1), dtype=np.int64)
        rows_before = rng.integers(-UNIT, UNIT, size=(12, 1, 1), dtype=np.int64)
        (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, QUANTA)
        rows_remainder = rng.integers(0, wall, size=(12, 1, 1), dtype=np.int64)
        slowed = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(12, PERIODIC, range(12), QUANTA, divisor=1))
        )
        assert int(slowed.level_of("content").min()) == QUANTA == int(slowed.level_of("content").max())
        live = planted(slowed, family, rows_now, rows_before, rows_remainder)
        state = (live.now.copy(), live.before.copy(), live.remainder.copy())
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
        # the inverse returns the rows and the remainders bit for bit
        slowed._advance_inverse(live)
        for a, b in zip((live.now, live.before, live.remainder), state, strict=True):
            assert np.array_equal(a, b)
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
    for quanta, expected in ((QUANTA, 1.987485), (0, 1.977750), (GAMMA // 5, 1.985760)):
        nodes = range(12) if quanta else []
        simulation = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(12, PERIODIC, nodes, max(quanta, 1), divisor=1))
        )
        f = ((GAMMA - quanta) / GAMMA) ** 2
        assert 2 - 2 * f * (1 - num / den) == pytest.approx(expected, abs=5e-7)  # the pace is conformal
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
    """The group pace of light's dispersion under a uniform clock ratio e / f: cos omega' = 1 - ratio (1 - cos omega), cos omega = (cos k + 2) / 3, by a central difference (HOST)."""

    def omega(kk: float) -> float:
        return math.acos(1.0 - ratio * (1.0 - (math.cos(kk) + 2.0) / 3.0))

    h = 1e-6
    return (omega(k + h) - omega(k - h)) / (2 * h)


@pytest.mark.diagnostic
@pytest.mark.usefixtures("the_loads_hold_alone")
def test_light_through_a_slab_of_content_is_delayed_by_the_slowed_dispersion():
    """(iii) THE SLAB, a GameBoard reading (a diagnostic, not a measurement): the flux test's Gaussian packet of light (40 Links, k = 0.3024) on the open chain of 400, 400 intervals with and without a slab of 40 Nodes at [150, 190) holding QUANTA each (the held row's divisor 1, the level at the slab the count at the start; the record alone is advanced): the transmitted packet's centroid lags the vacuum's by the slab's delay 40 (1 / v' - 1 / v) (6.23 Links; read 6.16), within 15 percent; 0.974 of the energy beyond the slab in the vacuum run and 0.946 with it."""
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
            parse_nature_beam_world(content_chain(400, CHAIN, nodes, QUANTA, divisor=1))
        )
        live = planted(simulation, 0, now, before, np.zeros((400, 1, 1), dtype=np.int64))
        for _ in range(400):
            simulation._advance(live)
        # GameBoard readings (diagnostic): the host reads the record's two levels
        weights = np.abs(live.now[:, 0, 0]).astype(np.float64)
        weights[:190] = 0.0
        centroids[slab] = float(np.sum(x * weights) / np.sum(weights))
        energy = live.now[:, 0, 0].astype(np.float64) ** 2 + live.before[:, 0, 0].astype(np.float64) ** 2
        beyond[slab] = float(energy[190:].sum() / energy.sum())
    pace = group_pace_light(k, 1.0)
    # the dispersion's factor under the weak field, f = (p_a / Gamma)^2 with p_a = Gamma - 2 c (ALGEBRA.md #the-direction)
    slowed = group_pace_light(k, ((GAMMA - 2 * QUANTA) / GAMMA) ** 2)  # the level enters the Link twice
    delay = 40.0 * (1.0 / slowed - 1.0 / pace)
    lag = centroids[False] - centroids[True]
    # the slab's faces reflect at most 2 ((1 - n) / (1 + n))^2 of the energy, n = Gamma / p_a the Link's index (COMPUTATION)
    index = GAMMA / (GAMMA - 2 * QUANTA)
    assert beyond[False] > 0.97 and beyond[True] > 1 - 2 * ((1 - index) / (1 + index)) ** 2, (
        "GameBoard reading, diagnostic",
        beyond,
    )
    assert 0.85 * delay * pace < lag < 1.15 * delay * pace, (
        "GameBoard reading, diagnostic",
        centroids,
        delay * pace,
    )


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_form_under_the_clock_the_shares_identity_and_the_inverse_with_content():
    """(iv) UNDER THE FIXED WALL (BUILD.md section 26 item 34), the periodic chain of 60, QUANTA at [20, 30) (the held row's divisor 1, the level there the count at the start; the record alone is advanced), random rows: (a) the engine's `conserved_form` is the form at the pace p_i = Gamma - c_i, 3 L (den / num) Gamma p_i (a^2 + b^2) - 6 L (den / num) p_i c_i a b at Nodes and L p_i p_j (a_i b_j + a_j b_i) on Links; (b) a Node's share changes by L times the currents on its Links plus (L / num) p_i (a_next - a_before) (r - r'), exactly; (c) the books' form by that term over 40 intervals; (d) 30 steps back return bit for bit."""
    rng = np.random.default_rng(23)
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(content_chain(60, PERIODIC, range(20, 30), QUANTA, divisor=1))
    )
    content = [int(v) for v in simulation.level_of("content")[:, 0, 0]]
    assert content == [QUANTA if 20 <= i < 30 else 0 for i in range(60)]
    for family, (num, den) in ((0, (1, 1)), (1, PAIR)):
        wall = simulation.kind_wall(family)
        now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
        before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
        live = planted(simulation, family, now, before, np.zeros((60, 1, 1), dtype=np.int64))
        # (a) the form from the rule's integers (item 44): L [w (a^2 + b^2) - S_i a b] / R_i at the Nodes, the Links plain
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
            # the folded axes' self-reads carry no flux; the remainders' term (wall / R_i) (a_next - a_before)(r - r')
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
        assert np.array_equal(live.now, state[0]) and np.array_equal(live.before, state[1])
        assert np.array_equal(live.remainder, state[2])


def one_node(length: int, i: int) -> np.ndarray:
    mask = np.zeros((length, 1, 1), dtype=bool)
    mask[i, 0, 0] = True
    return mask


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_loader_requires_the_node_clock_under_the_detector_law_and_bounds_it():
    """(v) `node_clock` is REQUIRED under `detector_law` (refused without it by name, an integer from 1); the load bound names the clock and the content (the slab of (iii) at Gamma = 10^6 refused naming Gamma and M); the registered light clock loads under the families file's Gamma = 10^4, A's clock pair (10^4, 10^4) at its Nodes as in the vacuum (its count 65 over the divisor 40000 adds nothing at the start, the first increment at the 615th interval, 616 x 65 = 40040), its wheel (4 x 10^8, 1203) on its own pair [800, 802] at the level 0 and the kind [800, 1200]'s (8 x 10^10, 9) in the vacuum."""
    document = content_chain(12, PERIODIC, [], 1)
    del document["node_clock"]
    with pytest.raises(ValueError, match="node_clock is required: Gamma"):
        parse_nature_beam_world(document)
    ray = content_chain(12, PERIODIC, [], 1)
    ray["detector_law"] = (
        False  # the flag was the law's name: refused by name (ALGEBRA.md #the-primitives)
    )
    with pytest.raises(ValueError, match="the world has unknown keys: detector_law"):
        parse_nature_beam_world(ray)
    zero = content_chain(12, PERIODIC, [], 1)
    zero["node_clock"] = 0
    with pytest.raises(ValueError, match="node_clock"):
        parse_nature_beam_world(zero)
    heavy = content_chain(400, CHAIN, range(150, 190), 250000, gamma=1_000_000)
    with pytest.raises(
        ValueError, match=r"\.pair \[.*Gamma = 1000000 and the content M = 20000000 .*not below 2\^63"
    ):
        parse_nature_beam_world(heavy)
    registered = json.loads((ROOT / "tests/light_clock.json").read_text(encoding="utf-8"))
    # the integers of ALGEBRA.md #the-rows-against-nature from the families file alone (item 59)
    assert registered["universe"] == "examples/events/universe.json"
    assert "node_clock" not in registered and "amplitude_bound" not in registered
    world = parse_nature_beam_world(registered)
    assert world.node_clock == NODE_CLOCK == 10**4
    simulation = DetectorLawSimulation(world)
    block = simulation.blocks[0]
    centre = tuple(int(axis[0]) for axis in np.nonzero(simulation.centre_mask(block)))
    # the registered world's matter family (the families file's third entry, item 60) at the body's kind [800, 809] (the pair on the body, ALGEBRA.md #the-interval)
    matter = [family.name for family in world.families].index("matter")
    kind = block.definition.kind
    # the beam body's Node's kind [800, 1200] since commit 7 (the one-Node emitter of the window)
    assert kind == (800, 1200) and world.families[matter].pair_on_body
    # A's count 65 (its one own quantum beside its stock of 64 light quanta, item 47) is the source over the divisor 40000: the level 0 at the start and for 614 intervals (616 x 65 = 40040 at the 615th)
    assert sum(simulation.held[0]) == 65 and not simulation.level_of("content").any()
    assert simulation.node_clock_pair(centre, matter) == (NODE_CLOCK, NODE_CLOCK)
    assert simulation.node_clock_pair((100, 0, 0), matter) == (NODE_CLOCK, NODE_CLOCK)
    # the wheel from the weak-field rule's integers (item 44) at the level 0: on the body's own pair [800, 802] at its Nodes W = 3 x 802 / gcd(800, 2406) = 1203 and g = 2 Gamma^2 x 2; the kind [800, 1200]'s own (80000000000, 9) in the vacuum
    assert simulation.wheel_at(matter, centre, kind) == (400000000, 1203)
    assert simulation.wheel_at(matter, (100, 0, 0), kind) == (80000000000, 9)
    assert VACUUM_WHEEL == (200000000, 2427)  # the kind [800, 809]'s vacuum wheel, read elsewhere


@pytest.mark.diagnostic
@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_content_at_a_body_falls_at_a_giving_and_rises_at_a_click():
    """(vi) On the emitter world (the stock 4 at [5, 37), the screen at [70, 72]): the body's content, the hold's source (`body_source`), is 5 at the load and falls by one at each giving; the screen's first body's 1 rises by one after each gather line; the held level stays 0 at every Node through the run (the emitter's carried remainder is 5 plus its count after every interval, 6005 at most, below the divisor 40000: no increment, ALGEBRA.md #the-primitives the row "the hold"), so the giving line's `content` is 0 and its `node_clock` the vacuum's pair; the books balanced; a GameBoard reading, a diagnostic, not a measurement."""
    document = emitter_world(stock=4)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    block = simulation.blocks[0]
    # the emitter's count 5: one own quantum and the stock of 4 held light quanta (item 47)
    assert simulation.body_source(0, "content") == 5 and simulation.body_source(1, "content") == 1
    carried = block.hold_carry[(2, 0)]  # the family of clicks' time part on the body's remainders
    assert carried == 5 and not simulation.level_of("content").any()
    givings_seen = 0
    clicks_seen = 0
    for _ in range(document["ticks"]):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        # the quantum moves at the window's open (the body's count of givings), the line is named at the close; the hold at (iv) reads the count the interval's clicks left
        givings_seen = block.givings
        clicks_seen = sum(1 for line in lines if line["event"] == "gather")
        assert simulation.body_source(0, "content") == 5 - givings_seen
        assert simulation.body_source(1, "content") == 1 + clicks_seen
        carried += simulation.body_source(0, "content")
        assert block.hold_carry[(2, 0)] == carried and not simulation.level_of("content").any()
        for line in [line for line in lines if line["tick"] == simulation.tick]:
            if line["event"] == "giving":
                assert line["content"] == 0 and line["node_clock"] == [NODE_CLOCK, NODE_CLOCK]
                assert lawful_wheel(simulation.world, line)
    assert givings_seen == 4 and clicks_seen >= 1
    assert simulation.body_source(0, "content") == 1  # the one own quantum stays (item 47)


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_family_of_clicks_is_held_at_the_bodies_and_moves_by_its_own_step_elsewhere():
    """(vii) THE FAMILY OF CLICKS (record 1982; ALGEBRA.md #the-counts-line, #the-ladder, #the-primitives the row "the hold"): on the open chain of 200 with light bodies of QUANTA at [90, 110) under the held row's divisor QUANTA, the clock record's level at the start is one quantum (the count over the divisor) at the bodies' Nodes and 0 elsewhere, the remainder 0; the source adds one quantum at the bodies' Nodes each interval into the record's own step, so at the slab's centre, until the edges' waves arrive (10 Links, one per interval), the level is the triangular sum (t + 1)(t + 2) / 2 at the interval t, 3, 6, 10, ..., 55 over the first nine (a_next = 2 a_now - a_before + 1 on a uniform slab); THE FRONT: nothing before the cone of one Link per interval, the long waves at the pace 1 / sqrt 3; the run 60 intervals (the level at the centre 902 at the 60th and 1005 at the 66th, at or beyond Gamma = 1000, the pace guard's end, ALGEBRA.md #the-paces)."""
    document = content_chain(200, CHAIN, range(90, 110), QUANTA, divisor=QUANTA)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    clock = simulation.held_records[2]
    assert simulation.held_families == [2] + [3] and simulation.families[2].held == "content"
    held = np.zeros((200, 1, 1), dtype=bool)
    held[90:110] = True
    assert np.all(clock.now[held] == 1) and not clock.before.any()
    assert not clock.now[~held].any() and not clock.remainder.any()
    assert simulation.level_of("content") is clock.now
    reached = None
    for _ in range(60):
        simulation.step()
        if simulation.tick <= 9:
            assert int(clock.now[99, 0, 0]) == (simulation.tick + 1) * (simulation.tick + 2) // 2
        if simulation.tick <= 29:
            assert int(clock.now[60, 0, 0]) == 0 and int(clock.now[139, 0, 0]) == 0
        elif reached is None and int(clock.now[60, 0, 0]) != 0:
            reached = simulation.tick
        assert simulation.level_of("content") is clock.now
    assert reached is not None and 30 <= reached <= 60, reached
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


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_joint_step_inverts_bit_for_bit_wherever_the_clock_falls():
    """(viii) THE EXACT BACKWARD RUN EVERYWHERE (record 1994; item 34): the chain of 60 with an open x and a body of QUANTA at [20, 30) under the held row's divisor QUANTA (one quantum into the field at the bodies' Nodes each interval, ALGEBRA.md #the-primitives the row "the hold") and a light record of random rows: the clicks' field rises at Nodes over 60 intervals and falls too (the zero faces send the wave back inverted, from the 50th interval; on a periodic chain a count, a source above 0, only raises it), and the joint step inverts bit for bit, the wall 3 den Gamma the same at every interval so no two states merge. The edge case: the field did move."""
    rng = np.random.default_rng(31)
    now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(content_chain(60, CHAIN, range(20, 30), QUANTA, divisor=QUANTA))
    )
    live = planted(simulation, 0, now, before, np.zeros((60, 1, 1), dtype=np.int64))
    simulation.records[live.identity] = live
    clock = simulation.held_records[2]
    start = (live.now.copy(), live.before.copy(), live.remainder.copy(), clock.now.copy())
    rises = falls = 0
    previous = clock.now.copy()
    for _ in range(60):
        simulation.step()
        rises += int(np.sum(clock.now > previous))
        falls += int(np.sum(clock.now < previous))
        previous = clock.now.copy()
    assert live.identity in simulation.records and not live.clicked
    assert rises > 0 and falls > 0 and not np.array_equal(clock.now, start[3])
    for _ in range(60):
        simulation.step_inverse()
    for x, y in zip((live.now, live.before, live.remainder, clock.now), start, strict=True):
        assert np.array_equal(x, y)
    assert simulation.tick == 0


def test_the_loader_reads_the_held_family_by_attribute_and_refuses_what_it_cannot_be():
    """(ix) THE FAMILY GENERICITY (record 2066; item 51): the family whose level is the Node clock is the one declaring `held: "content"`, no world key, no name in the engine; refused by name: the retired world keys, a held family with a quantum other than 1, a clock or a charge, two families holding the content, a read naming a family not held or none, no `reads`, a measured event of a held family, `held` naming it, an emitter given into it, six families (record 2081)."""
    good = content_chain(12, PERIODIC, [], 1)
    parse_nature_beam_world(good)
    for key, value in (("clock_family", "clicks"), ("charge_family", "charge"), ("charge_strength", 1)):
        retired = json.loads(json.dumps(good))
        retired[key] = value
        with pytest.raises(ValueError, match=f"the world has unknown keys: {key}"):
            parse_nature_beam_world(retired)
    ray = json.loads(json.dumps(good))
    ray["detector_law"] = (
        False  # the flag was the law's name: refused by name (ALGEBRA.md #the-primitives)
    )
    with pytest.raises(ValueError, match="the world has unknown keys: detector_law"):
        parse_nature_beam_world(ray)
    unread = json.loads(json.dumps(good))
    del unread["universe"][0]["reads"]
    with pytest.raises(ValueError, match=r"universe\[0\] lacks keys: reads"):
        parse_nature_beam_world(unread)
    unknown = json.loads(json.dumps(good))
    unknown["universe"][0]["reads"][0]["family"] = "ticks"
    with pytest.raises(ValueError, match=r"reads\[0\]\.family names 'ticks', no family of the universe"):
        parse_nature_beam_world(unknown)
    unheld = json.loads(json.dumps(good))
    unheld["universe"][0]["reads"][0]["family"] = "matter"
    with pytest.raises(ValueError, match="reads names 'matter', which is not held"):
        parse_nature_beam_world(unheld)
    quantum = json.loads(json.dumps(good))
    quantum["universe"][2]["quantum"] = 2
    quantum["universe"][2]["clicks"] = {"gives": True, "takes": True, "quantum": 2}
    with pytest.raises(ValueError, match="counted in quanta, one click one unit"):
        parse_nature_beam_world(quantum)
    clocked = json.loads(json.dumps(good))
    clocked["universe"][2]["clock"] = [512, 1]
    with pytest.raises(ValueError, match="gives nothing and declares a clock"):
        parse_nature_beam_world(clocked)
    charged = json.loads(json.dumps(good))
    charged["universe"][2]["sign"] = 1
    with pytest.raises(
        ValueError, match="is held and declares the charge 1: a held family carries none"
    ):
        parse_nature_beam_world(charged)
    reading = json.loads(json.dumps(good))
    reading["universe"][2]["reads"] = [{"family": "charge", "weight": 1, "twist": 0, "by": 1}]
    with pytest.raises(ValueError, match="is held and reads"):
        parse_nature_beam_world(reading)
    booked = json.loads(json.dumps(good))
    booked["universe"][2]["booked"] = True  # HISTORY (item 53): derived, not declared
    with pytest.raises(ValueError, match="unknown keys: booked"):
        parse_nature_beam_world(booked)
    twice = json.loads(json.dumps(good))  # two holders of the content: the second at its own divisor
    twice["universe"][3]["held"] = {"count": "content", "factors": [1], "divisor": 1}
    twice["stamp"] = input_stamp(twice)
    simulation = DetectorLawSimulation(parse_nature_beam_world(twice))
    held = [f for f, family in enumerate(simulation.families) if family.held == "content"]
    assert len(held) == 2 and simulation.held_records[held[0]] is not simulation.held_records[held[1]]
    source = json.loads(json.dumps(good))
    source["universe"][2]["held"] = {"count": "momentum", "factors": [1], "divisor": 40000}
    with pytest.raises(ValueError, match=r"held\.count must be one of"):
        parse_nature_beam_world(source)
    components = json.loads(json.dumps(good))
    components["universe"][0]["components"] = 3
    with pytest.raises(ValueError, match="has unknown keys: components"):
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
    many["most_families"] = 20  # the universe's key
    many["universe"] += [
        family_entry(f"family_{n}", [800, 809], reads()) for n in range(len(many["universe"]), 21)
    ]
    with pytest.raises(ValueError, match="families declares 21; at most 20 families"):
        parse_nature_beam_world(many)
    world = parse_nature_beam_world(good)
    assert world.held_families == (2, 3) and DetectorLawSimulation(world).held_families == [2, 3]


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_a_held_family_steps_at_the_pair_its_row_declares():
    """THE HELD FAMILY'S PAIR IS ITS ROW'S (the model owner, 2026-09-27; ALGEBRA.md #the-line): the family holding the content at [1, 2], [3, 5] and [800, 809] loads, and one field step on random levels is 3 den a_next + r' = num S_6(a_now) - 3 den a_before + r bit for bit; [1, 1] the same."""
    rng = np.random.default_rng(5)
    for num, den in ((1, 1), (1, 2), (3, 5), (800, 809)):
        document = content_chain(12, PERIODIC, [3], 5)
        document["universe"][2]["pair"] = [num, den]
        simulation = DetectorLawSimulation(parse_nature_beam_world(document))
        family = next(f for f in simulation.held_records if simulation.families[f].held == "content")
        record = simulation.held_records[family]
        assert simulation.families[family].pair == (num, den) and record.pair is None
        record.now[:], record.before[:] = rng.integers(-20, 20, size=(2, *record.now.shape))
        record.remainder[:] = rng.integers(0, 3 * den, size=record.now.shape)
        now, before, remainder = record.now.copy(), record.before.copy(), record.remainder.copy()
        simulation._advance(record)
        for x, read in enumerate(six_reads(now, True)):
            total = num * read - 3 * den * int(before[x, 0, 0]) + int(remainder[x, 0, 0])
            level, rest = divmod(total, 3 * den)
            assert (int(record.now[x, 0, 0]), int(record.remainder[x, 0, 0])) == (level, rest)
        assert np.array_equal(record.before, now)
