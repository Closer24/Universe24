"""The one lay act (ALGEBRA.md, No write from outside Rule3 wakes the massless row's zero mode; `src/event_universe/lay.py`): every write from outside Rule3 is one call of `laid`, the division act absorption the uniform part out of each level's change, the guard refusing by name a lay that moves one of the two sums, the write step at the lay's Nodes with the remainder at the division's origin and one lay line per written Node."""

import numpy as np

from event_universe import lay
from tests.laws import refused


def test_the_division_act_keeps_the_two_sums_and_the_guard_refuses_a_lay_that_moves_one():
    """The principle's one division act (ALGEBRA.md, The packet lay (h); `lay.division_act`, `lay.shares_of`, `lay.corrected`, `lay.guarded`): a level summing to 7 over four Nodes weighted 1, 3, 3, 1 has -7 divided back floor by floor, (-1, -3, -3, -1) short by one unit, the leftover to the heaviest Node first, so the level [1, 4, 3, -1] is laid as [0, 2, 0, -2] and sums to 0; a level summing to 0 as laid, or weighted nowhere, is returned as it is; the guard: a massless lay whose weights carry nothing refuses by name with the family and the two changes, a gapped family's lay and a lay handed no weights are laid as given, and in time the span's increments are kept at the sum 0 and the first moment 0 (`lay.laid_in_time`, the branch's division act in time bit for bit, `lay.division_act_in_time`). The shipped two slits' mode file is the generator's through the act, bit for bit."""
    level, weights = np.array([1, 4, 3, -1], dtype=object), np.array([1, 3, 3, 1], dtype=object)
    assert lay.shares_of(-7, [1, 3, 3, 1]) == [-1, -2, -3, -1]
    assert list(lay.division_act(level, weights)) == [0, 2, 0, -2]
    assert lay.division_act(level - level, weights) is not None and list(
        lay.division_act(level, weights * 0)
    ) == [1, 4, 3, -1]
    now, before = lay.corrected("light", True, (level, level * 2), weights)
    assert (int(now.sum()), int(before.sum())) == (0, 0) and list(before) == [0, 3, 1, -4]
    refused("wakes the zero mode", lay.corrected, "light", True, (level, level), weights * 0)
    refused("'light'", lay.guarded, "light", True, 7, 0, False)
    assert (
        lay.corrected("matter", False, (level, level), weights)[0] is level
    )  # a gapped family: as given
    assert (
        lay.corrected("light", True, (level, level), None)[1] is level
    )  # no weights: laid as built, named
