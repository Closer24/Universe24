"""The write's folder: one act per key, (coefficient x count + r) div wall by Rule3's carried division, the two levels (the first twice at the load, this interval's and the last one's at the advance), forward then back exact, the remainder at the key, the refusals by name; the card bound with a function."""

from __future__ import annotations

import random

import pytest

from event_universe.core.rule3 import THE_ADVANCE, THE_INVERSE, THE_LOAD, division_forward
from event_universe.features.write import DECLARATION, WriteOwn, WriteStart, WriteTerm, apply


def test_the_act_per_key_is_the_carried_division_with_two_levels_and_returns_exactly():
    """Per key the level is (coefficient x count + r) div wall with the remainder kept at the key: at the load both levels the first value; at the advance now and the value before; an advance then an inverse returns the state; the ratio of two keys' levels over many intervals is their counts' within one unit."""
    rng = random.Random(11)
    for _ in range(50):
        wall, coefficient = rng.randint(1, 10**5), rng.randint(1, 9)
        counts = ((("n", 0), rng.randint(0, 10**6)), (("n", 1), rng.randint(0, 10**6)))
        own = WriteOwn({}, {})
        loaded = apply(WriteTerm(wall, coefficient), WriteStart(THE_LOAD, counts), own)
        first = {key: division_forward(coefficient * count, wall, 0)[0] for key, count in counts}
        assert all(now == before == first[key] for key, now, before in loaded.levels)
        own = loaded.own
        totals = {key: 0 for key, _ in counts}
        for _ in range(40):
            advanced = apply(WriteTerm(wall, coefficient), WriteStart(THE_ADVANCE, counts), own)
            for key, now, before in advanced.levels:
                assert before == own.values[key] and 0 <= advanced.own.carries[key] < wall
                totals[key] += now
            back = apply(WriteTerm(wall, coefficient), WriteStart(THE_INVERSE, counts), advanced.own)
            assert dict(back.own.values) == dict(own.values) and dict(back.own.carries) == dict(
                own.carries
            )
            own = advanced.own
        (key_a, count_a), (key_b, count_b) = counts
        assert abs(totals[key_a] * wall - 40 * coefficient * count_a) < wall
        assert abs(totals[key_b] * wall - 40 * coefficient * count_b) < wall


def test_the_refusals_and_the_card():
    """A wall below 1 and an act outside the five are refused by name; the card is bound with the function and declares the place any."""
    with pytest.raises(ValueError, match="wall is from 1"):
        apply(WriteTerm(0), WriteStart(THE_LOAD, ()), WriteOwn({}, {}))
    with pytest.raises(ValueError, match="act is one of"):
        apply(WriteTerm(3), WriteStart("the leap", ()), WriteOwn({}, {}))
    assert DECLARATION.function is apply and DECLARATION.place == "any" and DECLARATION.built
