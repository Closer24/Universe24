"""The three components the quantum rows of the local detector law lack (the Boss's order of
2026-09-23 22:25Z; docs/designs/detector_law/declarations/DECLARATIONS.md, "what the engine
lacks"; BUILD.md section 11), one test each with its inputs, its expected integers and an edge
case: (a) the phase reading of a record at a Node, (b) the pair's two arms, (c) the splitter's
table under the rule."""

from __future__ import annotations

import json
import math
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.integer import by_clock
from event_universe.core.phase import nearest_phase, phase_cosines, phase_sines
from event_universe.events.detector_law import UNIT, DetectorLawSimulation, LiveRecord
from event_universe.events.world import parse_nature_beam_world
from tests.test_detector_law import chain_world

ROOT = Path(__file__).resolve().parents[1]


def clock_phase(age: int, numerator: int, denominator: int, steps: int) -> int:
    """The engine's clock at an age (the zero 3 N / 4 advanced by the whole part of
    age x n / d)."""
    return (3 * steps // 4 + age * numerator // denominator) % steps


def test_a_the_phase_reading_reads_the_clocks_phase_back_at_every_age():
    """(a) The phase reading (DECLARATIONS.md's head): on the circle N = 64 with the clock
    [77, 25] (3.08 steps per interval) and with [1, 1], the pair (C[phi(t - 1)], C[phi(t)]) x
    A / 256 the lamp drives at age t reads back phi(t) with the residual 0 at every age of a
    train of 64 intervals (every phase of the wheel), at the amplitude A = UNIT and at 3 / 7
    of it (the amplitude the reading's third input, the declaration's A: without it a small
    pair at a zero crossing and a large one at the peak share one direction). The table's
    grain, named (BUILD.md section 11, the finding): on N = 128 the reading is exact where a
    level is at least 16 of 256 from the cosine's extrema, and on N = 2048 with the clock
    [3, 1] within one step where both levels are at least 32 from them; at N = 2048 with the
    clock [1, 1] consecutive entries of the 1 / 256 table repeat and the pair recurs along the
    wave, so the reading is not exact there (a design question for the Bell row's N). On the
    chain world of the first build the record's reading at a free Node 12 Links from the lamp,
    once its train has reached it (the amplitude the wave's peak level on the chain), advances
    by the clock's step between consecutive intervals (1 to 6 steps each, 3.08 in the mean
    within 0.25: the short train's dispersion on the chain against one declared amplitude). The edge cases: the zero pair reads None; a zero circle, clock or
    amplitude is refused."""
    factor = UNIT // 256
    for steps, clock, band, within in (
        (64, (77, 25), 0, 0),
        (64, (1, 1), 0, 0),
        (128, (1, 1), 16, 0),
        (2048, (3, 1), 32, 1),
    ):
        table = phase_cosines(steps)
        checked = 0
        for age in range(1, steps + 1):
            phi = clock_phase(age, clock[0], clock[1], steps)
            previous = clock_phase(age - 1, clock[0], clock[1], steps)
            if not (
                band <= abs(table[phi]) <= 256 - band and band <= abs(table[previous]) <= 256 - band
            ):
                continue
            for scale in (factor, factor * 3 // 7):
                amplitude = scale * 256
                reading = nearest_phase(
                    table[previous] * scale, table[phi] * scale, amplitude, clock, steps
                )
                assert reading is not None
                error = min((reading[0] - phi) % steps, (phi - reading[0]) % steps)
                assert error <= within, (steps, clock, age, scale, reading, phi)
                if within == 0:
                    assert reading[1] == 0
                checked += 1
        assert checked >= steps // 2, (steps, checked)
    world = parse_nature_beam_world(chain_world())
    simulation = DetectorLawSimulation(world)
    lamp = next(n for n, entry in enumerate(world.measured) if entry.lamp is not None)
    node = (int(world.measured[lamp].position[0]) + 12, 0, 0)
    readings: list[int] = []
    for _ in range(80):
        simulation.step()
        live = next(iter(simulation.records.values()), None)
        if live is None or simulation.tick < 62:
            continue
        # the wave's amplitude at the reading, the declared A: its peak level on the chain
        amplitude = int(np.max(np.abs(live.now)))
        reading = simulation.read_phase(live, node, amplitude)
        if reading is not None:
            readings.append(reading[0])
    assert len(readings) >= 15
    steps = world.phase_steps
    advances = [(b - a) % steps for a, b in zip(readings, readings[1:], strict=False)]
    numerator, denominator = live.period_numerator, live.period_denominator
    whole = numerator // denominator
    assert all(whole - 2 <= advance <= whole + 3 for advance in advances), advances
    mean = sum(advances) / len(advances)
    assert abs(mean - numerator / denominator) < 0.25, (mean, advances)
    assert nearest_phase(0, 0, UNIT, (77, 25), 64) is None
    with pytest.raises(ValueError):
        nearest_phase(1, 1, UNIT, (0, 1), 64)
    with pytest.raises(ValueError):
        nearest_phase(1, 1, UNIT, (1, 1), 0)
    with pytest.raises(ValueError):
        nearest_phase(1, 1, 0, (1, 1), 64)
    massive = [f for f, family in enumerate(world.families) if family.massive_kind]
    assert massive == []


def bar_world(
    arms: int,
    directions: list[list[int]],
    branches: list[list[int]] | None = None,
    settings: tuple[int, int] | None = None,
) -> dict:
    """The bar of DECLARATIONS.md row 1a (21 x 1 x 1, y and z periodic of one layer, x open),
    the light family's clock [77, 25] on N = 64, one lamp at x = 10 with the arms and the
    directions given (the joint labels `branches`), a train of 2 periods, 20 births held;
    with `settings` (a, b) the two polarisers of the counter family at x = 7 (Alice, the -x
    arm) and x = 17 (Bob, the +x arm) at those settings, the table bodies of two cells named
    by the sets `alice` and `bob` (section 14 item 6; the joint gather of section 1 item 3)."""
    lamp: dict = {
        "rate": [1, 1],
        "wheel": [1, 64],
        "directions": directions,
        "train": 2,
        "arms": arms,
    }
    if arms > 1:
        # the order channel's key on a pair lamp, no default (line 8): the
        # counter form as built, u = (ordinal - 1) mod 64
        lamp["residue_order"] = "ordinal"
    if branches is not None:
        lamp["branches"] = branches
    document = chain_world()
    document["shape"] = [21, 1, 1]
    document["ticks"] = 60
    document["measured"] = [
        {
            "position": [10, 0, 0],
            "family": "light",
            "amount": 20,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "directions": directions,
            "lamp": lamp,
        }
    ]
    document["detectors"] = []
    if settings is not None:
        document["families"] = [
            {"name": "light", "quantum": 1, "phase_per_link": [77, 25]},
            {"name": "counter", "quantum": 1, "phase_per_link": [1, 1]},
        ]
        for name, x, setting in (("alice", 7, settings[0]), ("bob", 17, settings[1])):
            document["measured"].append(
                {
                    "position": [x, 0, 0],
                    "family": "counter",
                    "amount": 1,
                    "phase": 0,
                    "momentum": [0, 0, 0],
                    "fixed": True,
                    "table": {"light": {"phase_window": setting}},
                }
            )
            document["detectors"].append({"name": name, "positions": [[x, 0, 0]], "reading": "sum"})
    return document


def test_b_the_pairs_two_arms_are_born_together_and_reach_their_bars():
    """(b) The pair's two arms (DECLARATIONS.md rows 1a and 1d; DESIGN.md 6.3: "a pair record
    is two records with one birth stamp and opposite trains; the rule's part is only that
    both trains reach their bars"): on the bar of 21 the lamp at x = 10 with `arms` 2 on the
    directions +x and -x and the joint labels [[0, 1], [3, 1]] births TWO records per birth on
    one stamp (the same ordinal, u and interval; the identities the birth's and the birth's
    plus 2^24), the +x arm's row 0 on every Node with x < 10 and the -x arm's on every Node
    with x > 10 at every interval, the two rows equal by reflection through the lamp's Node
    until a body acts (Alice's entry cell at x = 7 reads x = 8 by its one-way Port), both trains
    reaching the bars at x = 7 and x = 17 (a nonzero level at the free Nodes
    beside them, x = 8 and x = 16, within 12 intervals of the birth; the bars' Nodes are the
    table bodies' entry cells, held at 0), the birth line carrying arms 2, the labels and the
    two arm records, the pair's one quantum on arm 0 (the books balanced at every interval);
    a lamp of one arm is as it was (no mask, the identity the birth's, the birth line as
    before). The edge cases: arms 2 on three directions is refused at load naming the arms; a
    pair lamp without a table body on each arm is refused (the joint gather's cells)."""
    world = parse_nature_beam_world(bar_world(2, [[1, 0, 0], [-1, 0, 0]], [[0, 1], [3, 1]], (0, 0)))
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    reached = {8: None, 16: None}
    mirrored = 0
    for _ in range(40):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        arms = [live for live in simulation.records.values() if live.born == 1]
        if len(arms) < 2:
            continue
        plus = next(live for live in arms if live.arm == 0)
        minus = next(live for live in arms if live.arm == 1)
        assert plus.u == minus.u and plus.birth_tick == minus.birth_tick and plus.born == minus.born
        assert minus.identity == plus.identity + (1 << 24)
        assert plus.labels == ((0, 1), (3, 1)) and plus.arms == 2 and minus.arms == 2
        assert plus.content == 1 and minus.content == 0
        assert not np.any(plus.now[:10]) and not np.any(minus.now[11:])
        if not np.any(minus.now[:9]):
            # the mirror image holds until a body acts: Alice's entry cell at
            # x = 7 reads the -x arm's level at x = 8 through its Port (the
            # one-way take, its ghost read back at x = 8), Bob's at x = 17
            # four Links later
            assert np.array_equal(plus.now[10:].ravel(), minus.now[:11].ravel()[::-1])
            mirrored += 1
        for x in reached:
            if reached[x] is None and (plus.now[x, 0, 0] != 0 or minus.now[x, 0, 0] != 0):
                reached[x] = simulation.tick
    births = [line for line in lines if line["event"] == "birth"]
    assert births and births[0]["arms"] == 2 and births[0]["labels"] == [[0, 1], [3, 1]]
    assert len(births[0]["arm_records"]) == 2
    assert mirrored >= 3
    assert reached[8] is not None and reached[16] is not None
    assert reached[8] - births[0]["tick"] <= 12 and reached[16] - births[0]["tick"] <= 12
    with pytest.raises(ValueError, match="a pair lamp needs ONE table body"):
        DetectorLawSimulation(
            parse_nature_beam_world(bar_world(2, [[1, 0, 0], [-1, 0, 0]], [[0, 1], [3, 1]]))
        )
    single = parse_nature_beam_world(bar_world(1, [[1, 0, 0]]))
    lines = []
    simulation = DetectorLawSimulation(single, observer=lines.append)
    for _ in range(5):
        simulation.step()
    live = next(iter(simulation.records.values()))
    assert live.mask is None and live.arms == 1 and live.identity == 1
    birth = next(line for line in lines if line["event"] == "birth")
    assert birth["arms"] == 1 and birth["labels"] == [[0, 1]] and "arm_records" not in birth
    on_periodic = bar_world(2, [[0, 1, 0], [0, -1, 0]], [[0, 1], [3, 1]])
    with pytest.raises(ValueError, match="periodic axis y, which has no half-space"):
        parse_nature_beam_world(on_periodic)
    with pytest.raises(ValueError, match="arms 2 does not divide"):
        parse_nature_beam_world(bar_world(2, [[1, 0, 0], [-1, 0, 0], [0, 1, 0]]))


def splitter_world(weights: list[list[int]], turns: list[list[int]], inputs: bool = True) -> dict:
    """A layer of 30 x 20 x 1 (z folded, x and y open), the lamp at (2, 2, 0) on +x with a train
    of 6 periods, one splitter of the TABLE form at (12, 2, 0) arriving from -x (the input
    direction +x) with its two outputs +x and +y, the split's weights and turns given."""
    document = chain_world()
    document["shape"] = [30, 20, 1]
    document["boundary"] = {"x": "open", "y": "open", "z": "periodic"}
    document["ticks"] = 120
    lamp = document["measured"][0]
    lamp["position"] = [2, 2, 0]
    lamp["lamp"]["train"] = 6
    lamp["lamp"]["rate"] = [1, 1]
    lamp["amount"] = 1
    table: dict = {"rule": "rerelease", "weights": weights, "turns": turns}
    if inputs:
        table["inputs"] = [[1, 0, 0]]
    else:
        # an opening's fan: one flat row of weights over the directions, no inputs
        table["weights"], table["turns"] = weights[0], turns[0]
    document["measured"] = [
        lamp,
        {
            "position": [12, 2, 0],
            "family": "light",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "directions": [[1, 0, 0], [0, 1, 0]],
            "table": {"light": table},
        },
    ]
    document["detectors"] = []
    return document


def planted_light(simulation: DetectorLawSimulation, age: int, identity: int = 1) -> LiveRecord:
    """A light record's rows given directly (no lamp): the clock [77, 25] on N = 64, at `age`."""
    return LiveRecord(
        identity,
        0,
        0,
        0,
        1,
        0,
        1,
        77,
        25,
        200,
        21,
        np.zeros(simulation.shape, dtype=np.int64),
        np.zeros(simulation.shape, dtype=np.int64),
        np.zeros(simulation.shape, dtype=np.int64),
        pointers=[0] * len(simulation.cell_names),
        first_rung=[None] * len(simulation.cell_names),
        ports=[np.zeros(simulation.shape, dtype=np.int64) for _ in simulation.take_masks],
        age=age,
    )


def test_c_the_splitters_table_acts_on_the_pair_by_the_linear_form():
    """(c) The splitter's table under DECLARATIONS.md section 14 (the linear form, the additive
    re-emission, the remainder carried): on the layer of `splitter_world` the splitter at
    (12, 2, 0) reads the input Node (11, 2, 0) and adds its terms at (13, 2, 0) and (12, 3, 0).
    (1) The integers: a planted pair (a_before, a_now) = (C[phi - k] UNIT / 256, C[phi] UNIT /
    256) at the input (the record's age 1, the clock's step k = by_clock(0, 77, 25) = 3) gives
    at the outputs, from 0, exactly floor(w_j (a_now S[k + t_j] - a_before S[t_j]) / (S[k] 29))
    with the remainder in [0, S[k] 29) kept on the splitter, w = [21, 20], t = [0, 16]; and each
    term is w_j UNIT cos(phi + t_j) / 29 within UNIT / 64 (the tables' 1 / 256 in the
    coefficients only). (2) The isometry: over the 64 phases the two outputs' squares sum to
    the input's squares within 2 percent (21^2 + 20^2 = 29^2). (3) A second call on the same
    pair adds the same term again (additive: the rule's value at the output is never
    overwritten). (4) The run of 90 intervals: the books balanced at every interval, the
    splitter's Node 0 (held, the take), no click and no offer at its cell, the wave beyond
    both outputs nonzero, every remainder inside its wall. The edge cases: a split without
    inputs (an opening's fan) refused; a row whose norm is no square refused naming the norm;
    a clock whose step has a sine of 0 ([32, 1] on N = 64: the step 32, sin pi = 0; [1, 2]: a
    step of 0) refused at load naming the step. Light's worlds without a splitter are byte for
    byte as before (test (p) of test_massive_record.py)."""
    world = parse_nature_beam_world(splitter_world([[21, 20]], [[0, 16]]))
    simulation = DetectorLawSimulation(world)
    assert len(simulation.splitters) == 1
    splitter = simulation.splitters[0]
    assert splitter.inputs[0][0] == (11, 2, 0) and splitter.outputs == [(13, 2, 0), (12, 3, 0)]
    steps = world.phase_steps
    cosines = phase_cosines(steps)
    sines = phase_sines(steps)
    k = by_clock(0, 77, 25)
    assert k == 3
    unit_per_cell = UNIT // 256
    squares_in = squares_out = 0
    for phi in range(steps):
        live = planted_light(simulation, 1, identity=phi + 1)
        now = cosines[phi] * unit_per_cell
        before = cosines[(phi - k) % steps] * unit_per_cell
        live.now[11, 2, 0] = now
        live.before[11, 2, 0] = before
        simulation._split(live)
        assert live.age == 2
        remainders = splitter.remainders[live.identity]
        wall = sines[k] * 29
        for j, (weight, turn, output) in enumerate(
            zip((21, 20), (0, 16), splitter.outputs, strict=True)
        ):
            total = weight * (now * sines[(k + turn) % steps] - before * sines[turn])
            expected, remainder = divmod(total, wall)
            assert int(live.now[output]) == expected
            assert remainders[j] == remainder and 0 <= remainder < wall
            closed = weight * UNIT * math.cos(2 * math.pi * (phi + turn) / steps) / 29
            assert abs(expected - closed) < UNIT / 64, (phi, j, expected, closed)
            squares_out += expected * expected
        squares_in += now * now
        # additive: the same pair again adds the same term (up to the carried remainder)
        first = [int(live.now[output]) for output in splitter.outputs]
        simulation._split(live)
        for j, output in enumerate(splitter.outputs):
            assert abs(int(live.now[output]) - 2 * first[j]) <= 1
    assert abs(squares_out / squares_in - 1.0) < 0.02, squares_out / squares_in
    # the run
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    splitter = simulation.splitters[0]
    for _ in range(90):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        for live in simulation.records.values():
            assert int(live.now[12, 2, 0]) == 0
        for remainders in splitter.remainders.values():
            assert all(0 <= r < sines[3] * 29 or 0 <= r < sines[4] * 29 for r in remainders)
    live = next(iter(simulation.records.values()))
    assert abs(int(live.now[14, 2, 0])) > 0 and abs(int(live.now[12, 4, 0])) > 0
    cell = simulation.cell_index[12, 2, 0]
    assert not any(line["event"] == "click" and line.get("node") == [12, 2, 0] for line in lines)
    assert all(live.pointers[cell] == 0 for live in simulation.records.values())
    with pytest.raises(ValueError, match="a splitter declares its inputs"):
        parse_nature_beam_world(splitter_world([[21, 20]], [[0, 16]], inputs=False))
    with pytest.raises(ValueError, match="no square"):
        DetectorLawSimulation(parse_nature_beam_world(splitter_world([[1, 1]], [[0, 16]])))
    for clock in ([32, 1], [1, 2]):
        zero_step = splitter_world([[21, 20]], [[0, 16]])
        zero_step["families"][0]["phase_per_link"] = clock
        with pytest.raises(ValueError, match="has a sine of 0"):
            parse_nature_beam_world(zero_step)


def polariser_world(setting: int, position: int = 36, faces: str = "closed") -> dict:
    """A chain of 40 (x closed at both ends: no sponge, the lamp's own take the
    only other sink), the light family's clock [77, 25] on N = 64, one lamp at x = 2
    with the wheel [1, 64] (a full wheel: u = 0 .. 63 once each over 64 births, one per
    interval), a train of 2 periods, and one polariser of the counter family at
    `position` with the setting `phase_window` (DECLARATIONS.md section 14 item 6), named
    by the set `pol` of one Node."""
    document = chain_world()
    document["shape"] = [40, 1, 1]
    document["boundary"] = {"x": faces, "y": "periodic", "z": "periodic"}
    document["ticks"] = 800
    document["families"] = [
        {"name": "light", "quantum": 1, "phase_per_link": [77, 25]},
        {"name": "counter", "quantum": 1, "phase_per_link": [1, 1]},
    ]
    document["measured"] = [
        {
            "position": [2, 0, 0],
            "family": "light",
            "amount": 64,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "directions": [[1, 0, 0]],
            "lamp": {"rate": [1, 1], "wheel": [1, 64], "directions": [[1, 0, 0]], "train": 2},
        },
        {
            "position": [position, 0, 0],
            "family": "counter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "table": {"light": {"phase_window": setting}},
        },
    ]
    document["detectors"] = [{"name": "pol", "positions": [[position, 0, 0]], "reading": "sum"}]
    return document


def test_d_a_polariser_is_a_table_body_of_two_cells_splitting_the_offer():
    """(d) DECLARATIONS.md section 14 item 6 (the polariser's two channels as cells of this
    engine): the polariser at x = 36 is a TABLE BODY of two cells, `pol+` at the exit Node
    x = 37 and `pol-` at the entry Node x = 36, both take Nodes booking to the body, the +
    cell before the - cell on the ladder; each interval's offer at the entry is split by
    [C'[s]^2, S'[s]^2] over n_s with the remainder kept (the shares' sum the whole offer, the
    entry's pointer within one unit of the declared share of the sum), the first rung of the
    whole offer stamped on both cells at one interval; the gather's cells are [pol, 0, "0"]
    and [pol, 1, "0"]; over the full wheel of 64 births the + channel counts 64 of 64 at s =
    0, 32 of 64 at s = N / 4 (the half angle 45 degrees, C' = S' = 181) and 0 of 64 at s =
    N / 2 (the pin's form: 128 of 256 at 45 degrees); the books balanced at every interval.
    The edge cases at load: the exit Node off the board (the body at the last Node), the body
    off the lamp's arm (behind the lamp), no set naming the body, two lamps of the family."""
    counts: dict[int, tuple[int, int]] = {}
    for setting in (0, 16, 32):
        world = parse_nature_beam_world(polariser_world(setting))
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        plus = simulation.cell_names.index("pol+")
        minus = simulation.cell_names.index("pol-")
        assert plus < minus and simulation.cell_set[plus] == simulation.cell_set[minus] == "pol"
        assert simulation.cell_channel[plus] == 0 and simulation.cell_channel[minus] == 1
        assert simulation.cell_measured[plus] == simulation.cell_measured[minus] == 1
        assert (
            int(simulation.cell_index[37, 0, 0]) == plus
            and int(simulation.cell_index[36, 0, 0]) == minus
        )
        assert bool(simulation.absorbing[37, 0, 0]) and bool(simulation.absorbing[36, 0, 0])
        body = simulation.table_bodies[0]
        expected = {0: (65536, 0), 16: (181 * 181, 181 * 181), 32: (0, 65536)}[setting]
        assert (body.plus, body.minus) == expected and body.norm == sum(expected)
        checked = 0
        for _ in range(800):
            simulation.step()
            assert simulation.books()["balanced"], simulation.tick
            for live in simulation.records.values():
                whole = live.pointers[plus] + live.pointers[minus]
                if whole:
                    # the entry keeps the - share, the split's remainder below n_s
                    share = whole * body.minus // body.norm
                    assert abs(live.pointers[minus] - share) <= 1 + whole // body.norm, (
                        live.pointers[minus],
                        share,
                    )
                    assert live.first_rung[plus] == live.first_rung[minus]
                    checked += 1
        assert checked > 0
        gathers = [line for line in lines if line["event"] == "gather"]
        births = [line for line in lines if line["event"] == "birth"]
        assert len(births) == 64 and len(gathers) == 64 and not simulation.records
        chosen = [gather["chosen"][0] for gather in gathers]
        assert all(cell[0] == "pol" and cell[2] == "0" and cell[1] in (0, 1) for cell in chosen)
        for gather in gathers:
            assert gather["click_at"] == "rung"
            triples = {tuple(cell[0][0]) for cell in gather["cells"]}
            assert triples <= {("pol", 0, "0"), ("pol", 1, "0")}
        counts[setting] = (
            sum(1 for cell in chosen if cell[1] == 0),
            sum(1 for cell in chosen if cell[1] == 1),
        )
    assert counts == {0: (64, 0), 16: (32, 32), 32: (0, 64)}
    # the loader's refusals (the engine's construction, as the splitter's)
    with pytest.raises(ValueError, match="off the board"):
        DetectorLawSimulation(parse_nature_beam_world(polariser_world(16, position=39)))
    with pytest.raises(ValueError, match="no arm's line"):
        DetectorLawSimulation(parse_nature_beam_world(polariser_world(16, position=1)))
    unnamed = polariser_world(16)
    unnamed["detectors"] = []
    with pytest.raises(ValueError, match="no detector set of one Node names its Node"):
        DetectorLawSimulation(parse_nature_beam_world(unnamed))
    two_lamps = polariser_world(16)
    two_lamps["measured"].append(dict(two_lamps["measured"][0], position=[10, 0, 0]))
    with pytest.raises(ValueError, match="ONE lamp"):
        DetectorLawSimulation(parse_nature_beam_world(two_lamps))


def pair_counts(
    settings: tuple[int, int], births: int = 64
) -> tuple[dict[tuple[int, int], int], list[dict]]:
    """The joint cells' counts of the bar world at the settings over `births` pair births (the
    full wheel of 64: u = 0 .. 63 once each), read from the gather lines' chosen joint cell
    (Alice's channel, Bob's channel), with the gathers."""
    document = bar_world(2, [[1, 0, 0], [-1, 0, 0]], [[0, 1], [3, 1]], settings)
    document["measured"][0]["amount"] = births
    document["ticks"] = births + 200
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    for _ in range(document["ticks"]):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert not simulation.records
    gathers = [line for line in lines if line["event"] == "gather"]
    found: dict[tuple[int, int], int] = {}
    for gather in gathers:
        chosen = gather["chosen"]
        assert chosen is not None and [cell[0] for cell in chosen] == ["alice", "bob"]
        key = (chosen[0][1], chosen[1][1])
        found[key] = found.get(key, 0) + 1
    return found, gathers


def test_e_the_pair_gathers_once_on_the_joint_ladder_of_four_cells():
    """(e) DECLARATIONS.md section 1 item 3 (the joint gather): on the bar with Alice at s = 0
    and Bob at s = 16 (the half angle 45 degrees at N = 64) each pair birth gathers ONCE (64
    gathers of 64 births, no arm gathered alone), the gather's `record` the birth's identity
    with both `arm_records`, its ladder the four joint cells [[alice, o_A, "0"], [bob, o_B,
    "0"]] in the order ++, +-, -+, --, the four counts summing to the births, `u` every
    residue once, the click at the later of the arms' first rungs (`click_at` "rung"), the
    content one quantum handed once (the books balanced); at (0, 16) the four weights are
    equal (J = 256 x 181 on every cell) and the counts 16 each; at (0, 0) the cells ++ and --
    take 32 each (E = 1); at (0, 32) the cells +- and -+ take 32 each (E = -1)."""
    counts, gathers = pair_counts((0, 16))
    assert len(gathers) == 64 and counts == {(0, 0): 16, (0, 1): 16, (1, 0): 16, (1, 1): 16}
    assert sorted(gather["u"] for gather in gathers) == list(range(64))
    for gather in gathers:
        assert gather["arm_records"] == [gather["record"], gather["record"] + (1 << 24)]
        assert gather["click_at"] == "rung" and gather["content"] == 1
        assert [cell[0] for cell in gather["cells"]] == [
            [["alice", 0, "0"], ["bob", 0, "0"]],
            [["alice", 0, "0"], ["bob", 1, "0"]],
            [["alice", 1, "0"], ["bob", 0, "0"]],
            [["alice", 1, "0"], ["bob", 1, "0"]],
        ]
        assert gather["weight"] == [(256 * 181) ** 2, 1] and gather["click"] >= gather["birth"]
        assert len(gather["arm_offers"]) == 2 and all(offer > 0 for offer in gather["arm_offers"])
    assert pair_counts((0, 0))[0] == {(0, 0): 32, (1, 1): 32}
    assert pair_counts((0, 32))[0] == {(0, 1): 32, (1, 0): 32}


def test_e2_the_pairs_quantum_lands_on_the_body_of_its_birth_arm():
    """(e2) The pair's one quantum (born on arm 0, the lamp's first direction, +x: Bob's arm
    on the bar) lands once at the joint click on that arm's body, the first builder's word of
    10:57Z: over 64 births Bob's counter body holds 64 and Alice's 0, the lamp's stock spent, the
    books balanced (the held asymmetry of the preliminary runs is this books line, not a
    reading)."""
    document = bar_world(2, [[1, 0, 0], [-1, 0, 0]], [[0, 1], [3, 1]], (0, 16))
    document["measured"][0]["amount"] = 64
    document["ticks"] = 264
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    for _ in range(264):
        simulation.step()
    assert simulation.books()["balanced"] and not simulation.records
    held = {entry["position"][0]: entry["held"][0] for entry in simulation.contents()}
    assert held == {10: 0, 7: 0, 17: 64}


def test_f_the_marginals_are_one_half_each_at_every_setting():
    """(f) DECLARATIONS.md section 2 (row 1d, no signalling): at the settings (0, 16), (16, 0),
    (8, 24) and (16, 24) Alice's + channel counts exactly 32 of 64 (R++ + R+- = n_a n_b, half
    the total, the ladder's rung at 32 exactly) and Bob's within one of 32 (his cells are not
    adjacent on the ladder: the rounding of two rungs)."""
    for settings in ((0, 16), (16, 0), (8, 24), (16, 24)):
        counts, _ = pair_counts(settings)
        assert sum(counts.values()) == 64
        alice_plus = counts.get((0, 0), 0) + counts.get((0, 1), 0)
        bob_plus = counts.get((0, 0), 0) + counts.get((1, 0), 0)
        assert alice_plus == 32, (settings, counts)
        assert abs(bob_plus - 32) <= 1, (settings, counts)


def test_g_the_joint_weights_are_the_declared_integers():
    """(g) The joint weights R = J^2 from planted tables (DECLARATIONS.md section 1 item 3): with
    psi = (00) + (11) (the labels 0 and 3 of weight 1, Alice reading the bit of arm 1 and Bob
    of arm 0) and the pairs (C', S') = (256, 0) and (181, 181), J(+, +) = 256 x 181, J(+, -) =
    -256 x 181, J(-, +) = 256 x 181, J(-, -) = 256 x 181 (the sign squared away); with (237,
    98) and (256, 0) (Bob's 22.5 degrees of N = 2048 against Alice's 0) the four weights
    (256 x 237)^2, (256 x 98)^2, (256 x 98)^2, (256 x 237)^2 and E = (237^2 - 98^2) / (237^2
    + 98^2) = 46565 / 65773 (COMPUTATION, the form's own number, for the generator's `bell.py`
    to compare with the pin 181 / 64); the singlet (01) - (10) at equal settings gives J(+,
    +) = 0; a one-body table gives the two weights C'^2 and S'^2 (Malus's form)."""
    labels = ((0, 1), (3, 1))
    cells = DetectorLawSimulation.joint_weights([(256, 0), (181, 181)], [1, 0], labels)
    assert [channels for channels, _ in cells] == [(0, 0), (0, 1), (1, 0), (1, 1)]
    assert [weight for _, weight in cells] == [(256 * 181) ** 2] * 4
    cells = DetectorLawSimulation.joint_weights([(256, 0), (237, 98)], [1, 0], labels)
    assert [weight for _, weight in cells] == [
        (256 * 237) ** 2,
        (256 * 98) ** 2,
        (256 * 98) ** 2,
        (256 * 237) ** 2,
    ]
    plus_plus, plus_minus, minus_plus, minus_minus = (weight for _, weight in cells)
    assert (plus_plus + minus_minus - plus_minus - minus_plus) * 65773 == 46565 * sum(
        weight for _, weight in cells
    )
    singlet = DetectorLawSimulation.joint_weights([(181, 181), (181, 181)], [1, 0], ((1, 1), (2, -1)))
    assert singlet[0][1] == 0 and singlet[3][1] == 0 and singlet[1][1] == singlet[2][1] > 0
    one = DetectorLawSimulation.joint_weights([(237, 98)], [0], ((0, 1),))
    assert one == [((0,), 237 * 237), ((1,), 98 * 98)]


def test_h_the_reader_reads_the_joint_cells_the_correlations_and_s_from_the_gather_lines(tmp_path):
    """(h) The reader of RUN_LIST.md rows 1a to 1d and 9 (`tools/click_readings/detector_law_bell.py`)
    on run folders written as the runner writes them (`initialization.json`, `events.jsonl`):
    four bar worlds at the settings (0, 16), (0, 48), (32, 16), (32, 48) (a = 0, a' = 32; b =
    16, b' = 48 at N = 64) give the four cells' counts per run (DETECTOR), E per run and S = E(a,
    b) - E(a, b') + E(a', b) + E(a', b') (COMPUTATION) on integers and Fractions; a one-table
    world (the polariser chain of test (d) at s = 16) gives the + share 32 / 64; the marginals
    one half."""
    import importlib.util
    import sys

    path = ROOT / "tools/click_readings/detector_law_bell.py"
    spec = importlib.util.spec_from_file_location("detector_law_bell", path)
    assert spec is not None and spec.loader is not None
    reader = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = reader
    spec.loader.exec_module(reader)

    def write_run(name: str, document: dict) -> Path:
        folder = tmp_path / name
        folder.mkdir()
        (folder / "initialization.json").write_text(json.dumps(document), encoding="utf-8")
        world = parse_nature_beam_world(document)
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        for _ in range(document["ticks"]):
            simulation.step()
        (folder / "events.jsonl").write_text(
            "".join(json.dumps(line) + "\n" for line in lines), encoding="utf-8"
        )
        return folder

    folders = []
    for settings in ((0, 16), (0, 48), (32, 16), (32, 48)):
        document = bar_world(2, [[1, 0, 0], [-1, 0, 0]], [[0, 1], [3, 1]], settings)
        document["measured"][0]["amount"] = 64
        document["ticks"] = 264
        folders.append(write_run(f"bell_{settings[0]}_{settings[1]}", document))
    readings = [reader.read_run(folder) for folder in folders]
    for reading in readings:
        assert reading.names == ["alice", "bob"] and reading.total == 64 and reading.escaped == 0
        assert reading.marginal(0) == Fraction(1, 2) and abs(
            reading.marginal(1) - Fraction(1, 2)
        ) <= Fraction(1, 64)
    correlations = {tuple(reading.settings): reading.correlation for reading in readings}
    # (0, 16) and (32, 48): the half angles 0 against 45 and 90 against 135 degrees, E = 0;
    # (0, 48): 0 against 135 degrees; (32, 16): 90 against 45
    assert correlations[(0, 16)] == 0 and correlations[(32, 48)] == 0
    value = reader.chsh(readings)
    assert (
        value
        == correlations[(0, 16)]
        - correlations[(0, 48)]
        + correlations[(32, 16)]
        + correlations[(32, 48)]
    )
    assert value == -correlations[(0, 48)] + correlations[(32, 16)]
    report = reader.report(readings)
    assert any(line.startswith("COMPUTATION S = ") for line in report)
    assert reader.main([str(folder) for folder in folders]) == 0
    one = write_run("malus_16", polariser_world(16))
    single = reader.read_run(one)
    assert single.names == ["pol"] and single.marginal(0) == Fraction(1, 2) and single.total == 64
    assert any("the + share 1/2" in line for line in reader.report([single]))
