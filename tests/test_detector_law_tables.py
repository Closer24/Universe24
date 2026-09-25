"""The phase reading as a HOST READER TOOL (core.phase.nearest_phase): the angle on the
world's circle nearest to a record's pair (a_before, a_now) at a Node at the record's clock
and amplitude, with the reading's residual; a GAMEBOARD diagnostic of a row, never an input
of the law. SINCE THE CLEANUP ORDER'S STEP 3 (BUILD.md section 26 item 17; ALGEBRA.md 9.21)
the tables are retired from the engine with their tests: the splitter's linear form (c), the
polariser as a table body of two detectors (d, d2, d3, held since item 14) and the joint weights
and the partial trace (g, d4); a polariser is a body with an axis and two receivers named, a
splitter a region of the one operator; the pair is born at the crystal. The engine's
`read_phase` and its cosine and sine tables are gone with them (no table in the engine,
9.22 (2)); this reader is the host's."""

from __future__ import annotations

import pytest

from event_universe.core.phase import nearest_phase, phase_cosines
from event_universe.events.detector_law import UNIT


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
    chain world the record's reading at a free Node 12 Links from the source, advancing by the
    clock's step between consecutive intervals: RETIRED with the lamp's drive (ALGEBRA.md 9.17;
    the emitter body's one-Node birth is broadband). The edge cases: the zero pair reads None; a zero circle, clock or
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
    # (the chain part of this test, the reading's advance along a driven
    # train at a free Node, retired with the lamp's drive, ALGEBRA.md 9.17:
    # an emitter body's one-Node birth is broadband)
    assert nearest_phase(0, 0, UNIT, (77, 25), 64) is None
    with pytest.raises(ValueError):
        nearest_phase(1, 1, UNIT, (0, 1), 64)
    with pytest.raises(ValueError):
        nearest_phase(1, 1, UNIT, (1, 1), 0)
    with pytest.raises(ValueError):
        nearest_phase(1, 1, 0, (1, 1), 64)
