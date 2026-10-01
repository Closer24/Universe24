"""The well, the source's line on a family's levels (ALGEBRA.md #the-primitives, the rows "the hold" and "the source"): the form D_i = now^2 - next x before at every Node from the three levels around a step, its quanta (D_i + r) div T with the remainder carried, the inverse bit for bit; the Wronskian of a real record is 0."""

import numpy as np

from event_universe import node

SHAPE, T = (2, 3, 1), 18_910


def around(form: list[int]) -> tuple[node.Record, node.Record]:
    """The three levels whose form is `form` at every Node: now 0, before 1, next minus the form."""
    zero, one = np.zeros(SHAPE, dtype=np.int64), np.ones(SHAPE, dtype=np.int64)
    before = node.Record(zero, one, zero)
    after = node.Record(-np.array(form, dtype=np.int64).reshape(SHAPE), zero, zero)
    return before, after


def test_the_well_is_the_forms_quanta_with_the_remainder_carried_and_steps_back():
    """1,891,072 over T = 18,910 is 100 quanta with the remainder 72; a form below T keeps it as its remainder and a second interval carries it over; a form of 0 writes nothing; the inverse returns the remainder before and the same quanta."""
    before, after = around([1_891_072, 18_909, 0, 37_820, 1, 18_910])
    carry = np.zeros(SHAPE, dtype=np.int64)
    form = node.form(before, after)
    quanta, carry = node.well(form, carry, T)
    assert quanta.ravel().tolist() == [100, 0, 0, 2, 0, 1]
    assert carry.ravel().tolist() == [72, 18_909, 0, 0, 1, 0]
    again, twice = node.well(form, carry, T)
    assert again.ravel().tolist() == [100, 1, 0, 2, 0, 1]
    assert twice.ravel().tolist() == [144, 18_908, 0, 0, 2, 0]
    back, start = node.well(form, twice, T, -1)
    assert np.array_equal(back, again) and np.array_equal(start, carry)
    assert not node.wronskian(after, node.Record(*(np.zeros(SHAPE, dtype=np.int64),) * 3)).any()
