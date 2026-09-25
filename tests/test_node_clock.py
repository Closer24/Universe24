"""THE NODE CLOCK (the model owner's decision (5) of record 1962; ALGEBRA.md 9.35 (2) and (3);
BUILD.md section 26 item 31): at every Node a clock pair (e, f) = (Gamma, Gamma + M), the same
for every family, Gamma the world key `node_clock` and M the content held at the Node (the
quanta of the measured events whose Nodes include it, 0 in the vacuum), enters the rule as
3 den f a_next + r' = e num S_6 + 6 den (f - e) a_now - 3 den f a_before + r with the wall
3 den f; e = f is the plain rule (the vacuum: the levels bit for bit, the remainder Gamma
times the plain one); a Node with content slows every family's rotation by e / f. The suite
reads the engine: (i) the rule in integers at a Node with content and its plain limit; (ii)
the rotation 2 cos omega' = 2 - 2 (e / f)(1 - num / den) at k = 0 (1.982200 at e / f = 0.8
on [800, 809], the mathematician's number); (iii) light through a slab of content, delayed by
the slowed dispersion, its form conserved; (iv) the form under the clock Gamma times the plain
form plus the content's weight on the kinetic part, exactly, the share's identity per Node,
the books' form's remainder identity and the inverse map bit for bit; (v) the loader's
refusals (the key required under the detector law, refused without it, the load bound naming
the clock and the content) and the registered light clock's Gamma; (vi) the content at a body
down by one at a birth and up by one at a click, on the birth line. Every number a COMPUTATION
on the rule's integers; no pin."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import UNIT, DetectorLawSimulation
from event_universe.events.world import input_stamp, parse_nature_beam_world
from tests.test_emitter import NODE_CLOCK, emitter_world, lawful_wheel
from tests.test_flux_reading import planted
from tests.test_massive_record import massive_world

ROOT = Path(__file__).resolve().parents[1]
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
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
    }


def content_chain(length: int, boundary: dict, nodes, amount: int, gamma: int = GAMMA) -> dict:
    """The chain [length, 1, 1] of the matter kind [800, 809] beside light with `amount` quanta
    held at each Node of `nodes` (a light body per Node) under the Node clock `gamma`."""
    document = massive_world([length, 1, 1], boundary, list(PAIR))
    document["age_bound"] = 100000
    document["node_clock"] = gamma
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
    """(i) THE RULE IN INTEGERS: on the periodic chain of 12 with QUANTA quanta held at every
    Node (e / f = 0.8), one step of the engine on random rows of light and of the matter kind
    equals 3 den f a_next + r' = e num S_6 + 6 den (f - e) a_now - 3 den f a_before + r with the
    wall 3 den f and the remainder in [0, wall), computed in Python integers; on the same rows
    with no content the levels are the plain rule's bit for bit and the remainder Gamma times
    the plain one (from r = 0). (ii) THE ROTATION (ALGEBRA.md 9.35 (2)): a uniform record (k = 0)
    of the matter kind at 2^24 turns with 2 cos omega' = 2 - 2 (e / f)(1 - num / den) read from
    three consecutive levels at a Node: 1.982200 at e / f = 0.8 (the mathematician's computed
    number) and 1.977750 = 2 num / den in the vacuum, within 10^-5 over 60 intervals; the
    edge case: at e / f = 1 / 2 (M = Gamma) 1.988875, the mathematician's second number."""
    rng = np.random.default_rng(11)
    for family, (num, den) in ((0, (1, 1)), (1, PAIR)):
        rows_now = rng.integers(-UNIT, UNIT, size=(12, 1, 1), dtype=np.int64)
        rows_before = rng.integers(-UNIT, UNIT, size=(12, 1, 1), dtype=np.int64)
        f = GAMMA + QUANTA
        wall = 3 * den * f
        rows_remainder = rng.integers(0, wall, size=(12, 1, 1), dtype=np.int64)
        slowed = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(12, PERIODIC, range(12), QUANTA))
        )
        assert int(slowed.node_content.min()) == QUANTA == int(slowed.node_content.max())
        live = planted(slowed, family, rows_now, rows_before, rows_remainder)
        slowed._advance(live)
        reads = six_reads(rows_now, True)
        for x in range(12):
            total = GAMMA * num * reads[x] + 6 * den * QUANTA * int(rows_now[x, 0, 0])
            total -= wall * int(rows_before[x, 0, 0])
            total += int(rows_remainder[x, 0, 0])
            expected = total // wall
            assert int(live.now[x, 0, 0]) == expected, (family, x)
            assert int(live.remainder[x, 0, 0]) == total - wall * expected
            assert 0 <= int(live.remainder[x, 0, 0]) < wall
        # the plain limit: no content, r = 0
        vacuum = DetectorLawSimulation(parse_nature_beam_world(content_chain(12, PERIODIC, [], 1)))
        assert not vacuum.node_content.any()
        live = planted(vacuum, family, rows_now, rows_before, np.zeros((12, 1, 1), dtype=np.int64))
        vacuum._advance(live)
        for x in range(12):
            plain = num * reads[x] - 3 * den * int(rows_before[x, 0, 0])
            assert int(live.now[x, 0, 0]) == plain // (3 * den)
            assert int(live.remainder[x, 0, 0]) == GAMMA * (plain - 3 * den * (plain // (3 * den)))
    # (ii) the rotation at k = 0
    amplitude = 1 << 24
    num, den = PAIR
    for quanta, expected in ((QUANTA, 1.982200), (0, 1.977750), (GAMMA, 1.988875)):
        nodes = range(12) if quanta else []
        simulation = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(12, PERIODIC, nodes, max(quanta, 1)))
        )
        assert 2 - 2 * (GAMMA / (GAMMA + quanta)) * (1 - num / den) == pytest.approx(expected, abs=5e-7)
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
    [150, 190) holding QUANTA quanta each (e / f = 0.8 there): the transmitted packet's
    centroid (its levels' magnitude beyond the slab, x >= 190) lags the vacuum's by the slab's
    delay 40 (1 / v' - 1 / v) intervals at the vacuum's pace v, v' the group pace of the slowed
    dispersion (ALGEBRA.md 9.35 (2): 8.3 intervals, 4.76 Links; read 4.73, COMPUTATION),
    within 15 percent; 0.97 of the packet's energy is beyond the slab in both runs (the
    planted packet's own backward part, 2.6 percent, returns off the face at x = 0 in both;
    the slab's faces reflect below a part in a thousand, the index 1.12); the books' form
    `record_form` is the same integer to the remainders' jitter (a part in a thousand) over
    the passage."""
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
        start = simulation.record_form(live)
        for _ in range(400):
            simulation._advance(live)
            assert abs(simulation.record_form(live) - start) < start // 1000
        weights = np.abs(live.now[:, 0, 0]).astype(np.float64)
        weights[:190] = 0.0
        centroids[slab] = float(np.sum(x * weights) / np.sum(weights))
        energy = live.now[:, 0, 0].astype(np.float64) ** 2 + live.before[:, 0, 0].astype(np.float64) ** 2
        beyond[slab] = float(energy[190:].sum() / energy.sum())
    pace = group_pace_light(k, 1.0)
    slowed = group_pace_light(k, GAMMA / (GAMMA + QUANTA))
    delay = 40.0 * (1.0 / slowed - 1.0 / pace)
    lag = centroids[False] - centroids[True]
    assert beyond[False] > 0.97 and beyond[True] > 0.97, beyond
    assert 0.85 * delay * pace < lag < 1.15 * delay * pace, (centroids, delay * pace)


def test_the_form_under_the_clock_the_shares_identity_and_the_inverse_with_content():
    """(iv) On the periodic chain of 60 with QUANTA quanta at the Nodes [20, 30), random rows of
    light and of the matter kind: (a) the engine's `conserved_form` is Gamma times the plain
    form (the pair's den / num on the squares and the Link term, in the flux's units 3 wall)
    plus M x 3 wall (den / num) (now - before)^2 summed over the slab's Nodes, exactly; (b) the
    share's identity per Node: its change over an interval is Gamma wall times the plain
    fluxes now_i before_j - before_i now_j through its Links (no weight of the clock on the
    flux) plus the remainders' term Gamma wall (a_next - a_before) (r - r') / (Gamma num),
    exactly, at the slab's Nodes as in the vacuum; (c) the books' form `record_form` changes by
    L SUM (a_next - a_before) (r - r') / num over 40 intervals exactly (L the numerators' lcm);
    (d) 30 steps then 30 inverse steps return the two levels and the remainders bit for bit
    (the content constant between events)."""
    rng = np.random.default_rng(23)
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(content_chain(60, PERIODIC, range(20, 30), QUANTA))
    )
    content = [int(v) for v in simulation.node_content[:, 0, 0]]
    assert content == [QUANTA if 20 <= i < 30 else 0 for i in range(60)]
    for family, (num, den) in ((0, (1, 1)), (1, PAIR)):
        wall = simulation.kind_wall(family)
        now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
        before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
        live = planted(simulation, family, now, before, np.zeros((60, 1, 1), dtype=np.int64))
        # (a) the form: Gamma times the plain form plus the content's weight on the kinetic part
        reads = six_reads(before, True)
        plain = 0
        kinetic = 0
        for i in range(60):
            a, b = int(now[i, 0, 0]), int(before[i, 0, 0])
            plain += 3 * wall * den // num * (a * a + b * b) - wall * a * reads[i]
            kinetic += content[i] * 3 * wall * den // num * (a - b) ** 2
        assert simulation.conserved_form(live) == GAMMA * plain + kinetic
        assert kinetic > 0
        # (b) the share's identity per Node, one interval
        old = [simulation.form_share(live, one_node(60, i)) for i in range(60)]
        a_before, a_now, r_old = live.before.copy(), live.now.copy(), live.remainder.copy()
        simulation._advance(live)
        a_next, r_new = live.now.copy(), live.remainder.copy()
        new = [simulation.form_share(live, one_node(60, i)) for i in range(60)]
        for i in range(60):
            flux = 0
            for j in ((i - 1) % 60, (i + 1) % 60):
                flux += int(a_now[i, 0, 0]) * int(a_before[j, 0, 0]) - int(a_before[i, 0, 0]) * int(
                    a_now[j, 0, 0]
                )
            flux += 4 * (
                int(a_now[i, 0, 0]) * int(a_before[i, 0, 0])
                - int(a_before[i, 0, 0]) * int(a_now[i, 0, 0])
            )  # the folded axes' self-reads carry no flux
            remainders = Fraction(
                (int(a_next[i, 0, 0]) - int(a_before[i, 0, 0]))
                * (int(r_old[i, 0, 0]) - int(r_new[i, 0, 0])),
                num,
            )
            assert new[i] - old[i] == GAMMA * wall * flux + wall * remainders, (family, i)
            assert 0 <= int(r_new[i, 0, 0]) < 3 * den * (GAMMA + content[i])
        # (c) the books' form's remainder identity, exact, over 40 intervals
        previous = simulation.record_form(live)
        for _ in range(40):
            a_before = live.before.astype(object)
            r = live.remainder.astype(object)
            simulation._advance(live)
            current = simulation.record_form(live)
            term = int(
                np.sum((live.now.astype(object) - a_before) * (r - live.remainder.astype(object)))
            )
            assert num * (current - previous) == wall * term
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
    registered light clock declares 10^6 and loads, its A's clock pair (10^6, 10^6 + 64) at
    its Nodes and (10^6, 10^6) in the vacuum, its wheel at A's centre Node the rule's with
    the stock (18774639 on [800, 801], the remainder's step 128, COMPUTATION), the kind's
    own 2427 on [800, 809] in the vacuum beside it (the step Gamma)."""
    document = content_chain(12, PERIODIC, [], 1)
    del document["node_clock"]
    with pytest.raises(ValueError, match="node_clock is required under `detector_law`"):
        parse_nature_beam_world(document)
    ray = content_chain(12, PERIODIC, [], 1)
    ray["detector_law"] = False
    ray["massive_record"] = False
    del ray["amplitude_bound"]
    del ray["face_depth"]
    del ray["families"][1]
    with pytest.raises(ValueError, match="node_clock is refused without `detector_law`"):
        parse_nature_beam_world(ray)
    zero = content_chain(12, PERIODIC, [], 1)
    zero["node_clock"] = 0
    with pytest.raises(ValueError, match="node_clock"):
        parse_nature_beam_world(zero)
    heavy = content_chain(400, CHAIN, range(150, 190), 250000, gamma=1_000_000)
    with pytest.raises(
        ValueError,
        match=r"families\[1\]\.pair \[800, 809\].*Gamma = 1000000 and the content M = 20000000 is .*not below 2\^63",
    ):
        parse_nature_beam_world(heavy)
    registered = json.loads(
        (ROOT / "examples/events/massive_record/light_clock.json").read_text(encoding="utf-8")
    )
    assert registered["node_clock"] == NODE_CLOCK == 10**6
    world = parse_nature_beam_world(registered)
    assert world.node_clock == NODE_CLOCK
    simulation = DetectorLawSimulation(world)
    block = simulation.blocks[0]
    centre = tuple(int(axis[0]) for axis in np.nonzero(simulation.centre_mask(block)))
    assert simulation.node_clock_pair(centre) == (NODE_CLOCK, NODE_CLOCK + 64)
    assert simulation.node_clock_pair((100, 0, 0)) == (NODE_CLOCK, NODE_CLOCK)
    assert simulation.wheel_at(1, centre) == (128, 18774639)
    assert simulation.wheel_at(1, (100, 0, 0)) == (NODE_CLOCK, 2427)  # the kind's own [800, 809]


def test_the_content_at_a_body_falls_at_a_birth_and_rises_at_a_click():
    """(vi) On the emitter world (the stock 4 at [5, 37), the screen the cube of light bodies at
    [70, 72] whose first body takes the clicks' quanta): the content at the body's centre Node
    (x = 21) is 4 at the load and falls by one at each birth (the birth line's `content` the
    value the clicking record was advanced under, 4, 3, 2, 1, and its `node_clock` [Gamma,
    Gamma + content]; the born record's wheel the rule's at that content); the content at the
    screen's first body (x = 70) is 1 at the load and rises by one at the interval after each
    gather line there (the click's quantum held by the body); the vacuum between them 0 at
    the load and at x = 50 until the family of clicks' front from the body's head arrives
    (14 Links at one Link per interval, ALGEBRA.md 9.44 (3)), then the family's waves and the
    rounding's walk of the plain step at these unit levels (at most 9 read on this head, far
    below Gamma); the books balanced at every interval."""
    document = emitter_world(stock=4)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    assert int(simulation.node_content[21, 0, 0]) == 4 and int(simulation.node_content[70, 0, 0]) == 1
    assert int(simulation.node_content[71, 0, 0]) == 1 and not simulation.node_content[40:70].any()
    births_seen = 0
    clicks_seen = 0
    for _ in range(document["ticks"]):
        before_births = sum(1 for line in lines if line["event"] == "birth")
        before_clicks = sum(1 for line in lines if line["event"] == "gather")
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        births_seen = sum(1 for line in lines if line["event"] == "birth")
        clicks_seen = sum(1 for line in lines if line["event"] == "gather")
        # the array after the interval is the one its advances used: rebuilt as the
        # interval began from the events before it, and again at a birth within it
        # (the born record's norm under the content the birth leaves), so a click's
        # quantum enters the array at the next interval unless a birth follows it
        assert int(simulation.node_content[21, 0, 0]) == 4 - births_seen
        # the family of clicks steps last in the interval and is then held at the content
        # the interval's clicks and births left, so a click's quantum is on the screen's
        # body as the interval ends (ALGEBRA.md 9.45 (2))
        assert int(simulation.node_content[70, 0, 0]) == 1 + clicks_seen
        if simulation.tick <= 12:
            assert int(simulation.node_content[50, 0, 0]) == 0
        # the family's waves and, at these small contents, the rounding's own walk of the
        # plain step at unit levels: far below Gamma (at most 9 read on this head)
        assert int(np.abs(simulation.node_content[40:70]).max()) <= 64
        del before_clicks
        for line in lines[len(lines) - (births_seen - before_births) :]:
            if line["event"] == "birth":
                assert line["content"] == 4 - before_births
                assert line["node_clock"] == [NODE_CLOCK, NODE_CLOCK + line["content"]]
                assert lawful_wheel(simulation.world, line)
    assert births_seen == 4 and clicks_seen >= 1
    assert int(simulation.node_content[70, 0, 0]) == 1 + clicks_seen
    assert int(simulation.node_content[21, 0, 0]) == 0


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
    clock = simulation.clock_record
    assert simulation.clock_family == 2 and simulation.families[2].name == "clicks"
    held = np.zeros((200, 1, 1), dtype=bool)
    held[90:110] = True
    assert np.all(clock.now[held] == QUANTA) and np.all(clock.before[held] == QUANTA)
    assert not clock.now[~held].any() and not clock.remainder.any()
    assert simulation.node_content is clock.now
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
        assert simulation.node_content is clock.now
    assert reached is not None and 30 <= reached <= 70, reached
    books = simulation.books()
    assert books["families"]["clicks"]["form"] == simulation.record_form(clock)
    assert books["families"]["clicks"]["measured"]["current"] == 0
    state = dict(simulation.snapshot_stream())
    assert state["clock"]["family"] == "clicks" and state["clock"]["rows"] == clock.now.ravel().tolist()
    empty = DetectorLawSimulation(parse_nature_beam_world(content_chain(60, PERIODIC, [], 1)))
    for _ in range(20):
        empty.step()
    assert not empty.clock_record.now.any() and not empty.node_content.any()


def test_the_joint_step_inverts_while_the_clock_rises_and_loses_states_where_it_falls():
    """(viii) THE JOINT INVERSE (ALGEBRA.md 9.41 (2), 9.45 (2)) and THE FINDING for the
    mathematician's ruling: on the periodic chain of 60 with a body of QUANTA quanta at
    [20, 30) and a light record of random rows registered (no detector set and no face:
    nothing clicks), the family of clicks' front rises the clock ahead of it and the joint
    step inverts bit for bit, the record's two levels and remainders and the family's own,
    for every interval before the level first falls at some Node (10 intervals read here;
    every family backward at the level of the interval's start, then the clock backward and
    its hold). WHERE THE LEVEL FALLS the wall 3 den (Gamma + c) shrinks and the remainders'
    states merge (a remainder at or above the new wall and one below it give one total): 30
    intervals forward and back return the family's field exactly and the record within a few
    units of its 2^20 (4 read on this head; asserted below 16), the loss about one part in
    Gamma per unit of the fall; no law is claimed for it here, the ruling is asked."""
    rng = np.random.default_rng(31)

    def fresh():
        simulation = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(60, PERIODIC, range(20, 30), QUANTA))
        )
        live = planted(simulation, 0, now, before, np.zeros((60, 1, 1), dtype=np.int64))
        simulation.records[live.identity] = live
        return simulation, live

    now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    simulation, live = fresh()
    clock = simulation.clock_record
    levels = [clock.now.copy()]
    for _ in range(30):
        simulation.step()
        levels.append(clock.now.copy())
    assert live.identity in simulation.records and not live.clicked
    fall = next(t for t in range(1, 31) if (levels[t] < levels[t - 1]).any())
    assert 5 <= fall <= 20, fall
    # exact for the intervals before the first fall
    simulation, live = fresh()
    clock = simulation.clock_record
    start = (live.now.copy(), live.before.copy(), live.remainder.copy(), clock.now.copy())
    for _ in range(fall - 1):
        simulation.step()
    assert not np.array_equal(clock.now, start[3])
    for _ in range(fall - 1):
        simulation.step_inverse()
    for x, y in zip((live.now, live.before, live.remainder, clock.now), start, strict=True):
        assert np.array_equal(x, y)
    assert simulation.tick == 0
    # the loss where it fell, bounded (the finding)
    simulation, live = fresh()
    clock = simulation.clock_record
    for _ in range(30):
        simulation.step()
    for _ in range(30):
        simulation.step_inverse()
    assert np.array_equal(clock.now, start[3]) and simulation.tick == 0
    assert int(np.abs(live.now - start[0]).max()) < 16
    assert int(np.abs(live.before - start[1]).max()) < 16


def test_the_loader_names_the_family_of_clicks_and_refuses_what_it_cannot_be():
    """(ix) `clock_family` is REQUIRED under `detector_law` (refused absent naming the key),
    refused without that law, refused naming no declared family (the families listed), refused
    on a family with a pair other than [1, 1] (the matter kind), on a quantum other than 1 and
    on a family with a clock of its own; a measured event of the family of clicks is refused,
    `held` naming it is refused, and an emitter born into it is refused; five families are
    refused (the owner's constant four, record 1982); a world with the family declared and
    named loads, its index the engine's `clock_family`."""
    good = content_chain(12, PERIODIC, [], 1)
    parse_nature_beam_world(good)
    absent = json.loads(json.dumps(good))
    del absent["clock_family"]
    with pytest.raises(ValueError, match="clock_family is required under `detector_law`"):
        parse_nature_beam_world(absent)
    ray = json.loads(json.dumps(good))
    ray["detector_law"] = False
    ray["massive_record"] = False
    del ray["amplitude_bound"]
    del ray["face_depth"]
    del ray["node_clock"]
    del ray["families"][1]
    with pytest.raises(ValueError, match="clock_family is refused without `detector_law`"):
        parse_nature_beam_world(ray)
    unknown = json.loads(json.dumps(good))
    unknown["clock_family"] = "ticks"
    with pytest.raises(ValueError, match="clock_family names 'ticks', which no family declares"):
        parse_nature_beam_world(unknown)
    massive = json.loads(json.dumps(good))
    massive["clock_family"] = "matter"
    with pytest.raises(ValueError, match="the family of clicks is massless, its pair \\[1, 1\\]"):
        parse_nature_beam_world(massive)
    quantum = json.loads(json.dumps(good))
    quantum["families"][2]["quantum"] = 2
    with pytest.raises(ValueError, match="counted in quanta, one click one unit"):
        parse_nature_beam_world(quantum)
    clocked = json.loads(json.dumps(good))
    clocked["families"][2]["phase_per_link"] = [512, 1]
    with pytest.raises(ValueError, match="has no clock of its own"):
        parse_nature_beam_world(clocked)
    body = json.loads(json.dumps(good))
    body["measured"] = [dict(light_body(3, 1), family="clicks")]
    with pytest.raises(ValueError, match="is of the family of clicks 'clicks': no body is of it"):
        parse_nature_beam_world(body)
    holding = json.loads(json.dumps(good))
    holding["measured"] = [dict(light_body(3, 1), held={"clicks": 2})]
    with pytest.raises(ValueError, match="held names the family of clicks"):
        parse_nature_beam_world(holding)
    born = emitter_world(stock=1)
    born["measured"][0]["emitter"]["family"] = "clicks"
    born["input"] = input_stamp(born)
    with pytest.raises(
        ValueError, match="births into the family of clicks|the born family is a paid family"
    ):
        parse_nature_beam_world(born)
    five = json.loads(json.dumps(good))
    five["families"] += [
        {"name": "fourth", "quantum": 1, "pair": [800, 809]},
        {"name": "fifth", "quantum": 1, "pair": [800, 809]},
    ]
    with pytest.raises(ValueError, match="families declares 5; at most 4 families"):
        parse_nature_beam_world(five)
    world = parse_nature_beam_world(good)
    assert world.clock_family == 2 and DetectorLawSimulation(world).clock_family == 2
