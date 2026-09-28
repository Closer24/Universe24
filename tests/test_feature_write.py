"""The write's folder: one act per key, (coefficient x count + r) div wall by Rule3's carried division, the two levels (the first twice at the load, this interval's and the last one's at the advance), forward then back exact, the remainder at the key, the refusals by name; the card bound with a function at the place any."""

from __future__ import annotations

import random

import pytest

from event_universe.core.rule3 import THE_ADVANCE, THE_INVERSE, THE_LOAD, division_forward
from event_universe.features.write import DECLARATION, WriteOwn, WriteStart, WriteTerm, apply


def test_the_act_per_key_is_the_carried_division_with_two_levels_exact_back_and_refusing_by_name():
    """Per key the level is (coefficient x count + r) div wall with the remainder kept at the key: at the load both levels the first value; at the advance now and the value before; an advance then an inverse returns the state; the ratio of two keys' levels over many intervals is their counts' within one unit; a wall below 1 and an act outside the five are refused by name; the card is bound with the function and declares the place any."""
    rng = random.Random(11)
    for _ in range(50):
        wall, coefficient = rng.randint(1, 10**5), rng.randint(1, 9)
        counts = ((("n", 0), rng.randint(0, 10**6)), (("n", 1), rng.randint(0, 10**6)))
        term, own = WriteTerm(wall, coefficient), WriteOwn({}, {})
        loaded = apply(term, WriteStart(THE_LOAD, counts), own)
        first = {key: division_forward(coefficient * count, wall, 0)[0] for key, count in counts}
        assert all(now == before == first[key] for key, now, before in loaded.levels)
        own, totals = loaded.own, dict.fromkeys(first, 0)
        for _ in range(40):
            advanced = apply(term, WriteStart(THE_ADVANCE, counts), own)
            for key, now, before in advanced.levels:
                assert before == own.values[key] and 0 <= advanced.own.carries[key] < wall
                totals[key] += now
            back = apply(term, WriteStart(THE_INVERSE, counts), advanced.own)
            assert (back.own.values, back.own.carries) == (own.values, own.carries)
            own = advanced.own
        assert all(abs(totals[key] * wall - 40 * coefficient * count) < wall for key, count in counts)
    with pytest.raises(ValueError, match="wall is from 1"):
        apply(WriteTerm(0), WriteStart(THE_LOAD, ()), WriteOwn({}, {}))
    with pytest.raises(ValueError, match="act is one of"):
        apply(WriteTerm(3), WriteStart("the leap", ()), WriteOwn({}, {}))
    assert DECLARATION.function is apply and DECLARATION.place == "any" and DECLARATION.built
