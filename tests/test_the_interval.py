"""The volume form's construction under the law of one Node (ALGEBRA.md, The board's interval is no observable; The mean's velocity is the content's; The form's own clock; The factor carried; The stress's trace is the time line's; the hypotheses under their own names, 2026-10-22; the momentum hand's derivation M12a of the volume form, read cold by the reader; DESIGN section 3, T3 to T8), construction alone and no world of the test of the law's course: the form's own clock as one power of the write (T6), the volume form's two functions, one division and one search (T3), the premise as a test, the volume's write reading its own level both ways and the velocity no datum of the seed (T4), the run back MATCH at every interval at a wall that never moves (T5), the trace as the time line's with the tension lines traceless (T7), the finding of the second smoke as a test, and the carried factor at the wall fixed per Node (T8); the declaration and the attractor stand in tests/test_the_uniform_mode.py (T1, T2 and T9), the volume form's two functions and the singular point."""

import bisect
from dataclasses import dataclass

import numpy as np

from event_universe import records
from event_universe.core import paces
from event_universe.features import volume
from tests.laws import refused

GAMMA = 6000  # the rule's clock


@dataclass(frozen=True)
class Row:
    """A held row's rule as the start reads it, the one flag the volume's two start functions read."""

    motion_volume: bool


def test_the_volume_of_a_level_and_the_level_of_a_volume_are_one_division_and_one_search_each_the_others_inverse():
    """T3, the volume form's two functions (features/volume `volume_of`, `level_of`, `clock_zero`, `EXPONENT`, `at_start`, `started`, `levels_read`; the momentum hand's derivation M12a read cold by the reader; the acts table: the volume one division D, the reading a search S): the exponent is d + 1 = 4; the volume of the vacuum's level 0 is Gamma itself (Gamma^5 over Gamma^4); over every level from -Gamma + 1 to 7,100 the volumes X(a) = ceil(Gamma^5 / p_0(a)^4) never fall as the level rises and, from the level 0 up, rise at exactly the levels where the clock's integer pace falls (two levels sharing one clock share one volume: the clock's own staircase, p_0 falling by less than one unit per level below Gamma, and the volume's unit coarser than the level's in a hill, X(-Gamma) = 110), and the level of a volume is the staircase's inverse bit for bit, the largest level whose volume is at most X, at every X(a), at every X(a) - 1 and at a random X between (the test's bisection on the volumes' list, the oracle), so that a level whose volume rises at the next level reads back from its own volume; the arrays come back in the shape given as Python's integers; the clock's zero at Gamma 6,000 is 56,352 (the paces' text), the clock's own power above 0 at 56,351 and 0 there, and the reading of a volume beyond every pace rests at 56,351, the clock's last pace; a volume at most 0 at a Node is refused by name, and one below the deepest hill's is refused by name; `at_start` turns every row's flag off and `started` converts a record's two levels to volumes once with its remainder kept, the line itself for a row at its level; `levels_read` passes a level array through and reads a volume array."""
    assert volume.EXPONENT == 4 and int(volume.volume_of(GAMMA, np.array(0))) == GAMMA
    levels = np.arange(-GAMMA + 1, 7101)
    volumes = volume.volume_of(GAMMA, levels)
    staircase = [int(x) for x in volumes]  # the oracle's staircase reaches 100 levels past the probes
    assert volumes.dtype == np.dtype(object) and all(
        x <= y for x, y in zip(staircase, staircase[1:], strict=False)
    )
    clocks = [paces.clock(GAMMA, int(a)) for a in levels]
    for a, x, y, p, q in zip(levels, staircase, staircase[1:], clocks, clocks[1:], strict=False):
        assert a < 0 or (x < y) == (q < p), (a, x, y, p, q)  # the volume rises where the clock falls
    draw = np.random.default_rng(12)
    probed = staircase[:-100]
    below = [x - 1 for x in probed if x > staircase[0]]
    probes = probed + below + [int(x) for x in draw.integers(staircase[0], probed[-1], 300)]
    inverse = [int(levels[bisect.bisect_right(staircase, x) - 1]) for x in probes]
    assert [int(a) for a in volume.level_of(GAMMA, np.array(probes, dtype=object))] == inverse
    rising = [a for a, x, y in zip(levels[:-100], staircase, staircase[1:], strict=False) if x < y]
    assert np.array_equal(volume.level_of(GAMMA, volume.volume_of(GAMMA, np.array(rising))), rising)
    grid = draw.integers(-500, 3000, (3, 3, 3))
    found = volume.volume_of(GAMMA, grid)
    assert found.shape == (3, 3, 3) and type(found[0, 0, 0]) is int
    assert np.array_equal(
        volume.level_of(GAMMA, found),
        [
            [[int(levels[bisect.bisect_right(staircase, int(x)) - 1]) for x in row] for row in plane]
            for plane in found
        ],
    )
    assert volume.clock_zero(GAMMA) == 56352 and paces.clock_alone(GAMMA, 56352) == 0
    assert paces.clock_alone(GAMMA, 56351) > 0 and int(volume.level_of(GAMMA, np.array(10**40))) == 56351
    refused("at most 0", volume.level_of, GAMMA, np.array([GAMMA, 0]))
    assert int(volume.volume_of(GAMMA, np.array(-GAMMA))) == 110
    refused("lies below -6000", volume.level_of, GAMMA, np.array([109]))
    assert volume.at_start((Row(True), Row(False))) == (Row(False), Row(False))
    line = records.Record(grid, grid - 7, np.full((3, 3, 3), 5))
    assert volume.started(GAMMA, Row(False), line) is line
    converted = volume.started(GAMMA, Row(True), line)
    assert np.array_equal(converted.now, found) and converted.remainder is line.remainder
    assert np.array_equal(converted.before, volume.volume_of(GAMMA, grid - 7))
    assert volume.levels_read(GAMMA, grid, False) is grid
    assert np.array_equal(volume.levels_read(GAMMA, found, True), volume.level_of(GAMMA, found))
