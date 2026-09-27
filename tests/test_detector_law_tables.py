"""The phase reading, a host reader tool (core.phase.nearest_phase): the angle nearest to a record's pair, a
GameBoard diagnostic, never an input of the law."""

from __future__ import annotations

import pytest

from event_universe.core.phase import nearest_phase, phase_cosines

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md 9.57 (2);
# the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


def clock_phase(age: int, numerator: int, denominator: int, steps: int) -> int:
    """The engine's clock at an age (the zero 3 N / 4 advanced by the whole part of
    age x n / d)."""
    return (3 * steps // 4 + age * numerator // denominator) % steps


def test_a_the_phase_reading_reads_the_clocks_phase_back_at_every_age():
    """The pair the lamp drives at age t reads back phi(t) with residual 0 at every age, on N = 64
    at [77, 25] and [1, 1], at the amplitude and at 3 / 7 of it; the table's grain is named."""
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
    # an emitter body's one-Node giving is broadband)
    assert nearest_phase(0, 0, UNIT, (77, 25), 64) is None
    with pytest.raises(ValueError):
        nearest_phase(1, 1, UNIT, (0, 1), 64)
    with pytest.raises(ValueError):
        nearest_phase(1, 1, UNIT, (1, 1), 0)
    with pytest.raises(ValueError):
        nearest_phase(1, 1, 0, (1, 1), 64)
