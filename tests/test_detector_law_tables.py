"""The three components the quantum rows of the local detector law lack (the Boss's order of
2026-09-23 22:25Z; docs/designs/detector_law/declarations/DECLARATIONS.md, "what the engine
lacks"; BUILD.md section 11), one test each with its inputs, its expected integers and an edge
case: (a) the phase reading of a record at a Node, (b) the pair's two arms, (c) the splitter's
table under the rule."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.phase import nearest_phase, phase_cosines
from event_universe.events.detector_law import UNIT, DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world
from tests.test_detector_law import chain_world


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


def bar_world(arms: int, directions: list[list[int]], branches: list[list[int]] | None = None) -> dict:
    """The bar of DECLARATIONS.md row 1a (21 x 1 x 1, y and z periodic of one layer, x open),
    the light family's clock [77, 25] on N = 64, one lamp at x = 10 with the arms and the
    directions given (the joint labels `branches`), a train of 2 periods, 20 births held."""
    lamp: dict = {"rate": [1, 1], "wheel": [1, 64], "directions": directions, "train": 2, "arms": arms}
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
    return document


def test_b_the_pairs_two_arms_are_born_together_and_reach_their_bars():
    """(b) The pair's two arms (DECLARATIONS.md rows 1a and 1d; DESIGN.md 6.3: "a pair record
    is two records with one birth stamp and opposite trains; the rule's part is only that
    both trains reach their bars"): on the bar of 21 the lamp at x = 10 with `arms` 2 on the
    directions +x and -x and the joint labels [[0, 1], [3, 1]] births TWO records per birth on
    one stamp (the same ordinal, u and interval; the identities the birth's and the birth's
    plus 2^24), the +x arm's row 0 on every Node with x < 10 and the -x arm's on every Node
    with x > 10 at every interval, the two rows equal by reflection through the lamp's Node,
    both trains reaching the bars at x = 7 and x = 17 (a nonzero level there within 12
    intervals of the birth), the birth line carrying arms 2, the labels and the two arm
    records, the pair's one quantum on arm 0 (the books balanced at every interval); a lamp of
    one arm is as it was (no mask, the identity the birth's, the birth line as before). The
    edge case: arms 2 on three directions is refused at load naming the arms."""
    world = parse_nature_beam_world(bar_world(2, [[1, 0, 0], [-1, 0, 0]], [[0, 1], [3, 1]]))
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    reached = {7: None, 17: None}
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
        assert np.array_equal(plus.now[10:].ravel(), minus.now[:11].ravel()[::-1])
        for x in reached:
            if reached[x] is None and (plus.now[x, 0, 0] != 0 or minus.now[x, 0, 0] != 0):
                reached[x] = simulation.tick
    births = [line for line in lines if line["event"] == "birth"]
    assert births and births[0]["arms"] == 2 and births[0]["labels"] == [[0, 1], [3, 1]]
    assert len(births[0]["arm_records"]) == 2
    assert reached[7] is not None and reached[17] is not None
    assert reached[7] - births[0]["tick"] <= 12 and reached[17] - births[0]["tick"] <= 12
    single = parse_nature_beam_world(bar_world(1, [[1, 0, 0]]))
    lines = []
    simulation = DetectorLawSimulation(single, observer=lines.append)
    for _ in range(5):
        simulation.step()
    live = next(iter(simulation.records.values()))
    assert live.mask is None and live.arms == 1 and live.identity == 1
    birth = next(line for line in lines if line["event"] == "birth")
    assert birth["arms"] == 1 and birth["labels"] == [[0, 1]] and "arm_records" not in birth
    with pytest.raises(ValueError, match="arms 2 does not divide"):
        parse_nature_beam_world(bar_world(2, [[1, 0, 0], [-1, 0, 0], [0, 1, 0]]))
