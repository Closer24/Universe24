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
