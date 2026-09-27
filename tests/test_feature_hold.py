"""The hold's folder: every division through core.rule3, forward then back exact; the dipole's terms; the refusals; the card bound, the loop's hold being this folder's line."""

from __future__ import annotations

import random
from pathlib import Path

import pytest

from event_universe.core.register import folder_of
from event_universe.core.rule3 import division_back, division_forward
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.hold import (
    ACTS,
    CROSS_TERMS,
    DECLARATION,
    THE_ADVANCE,
    THE_INVERSE,
    THE_LOAD,
    THE_REWRITE,
    THE_UNHOLD,
    HoldOwn,
    HoldStart,
    HoldTerm,
    apply,
)
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import emitter_world

ROOT = Path(__file__).resolve().parents[1]


def test_forward_then_back_returns_the_state_exactly_and_the_load_writes_the_first_value_twice():
    """Rule3's division act forward and its direction -1 back: an advance then an inverse returns the
    state; the value before is the ceiling form; at the load both levels are the first value."""
    rng = random.Random(7)
    for _ in range(300):
        wall = rng.randint(1, 10**6)
        numerator = rng.randint(-(10**9), 10**9)
        carry = rng.randint(0, wall - 1)
        value, carried = division_forward(numerator, wall, carry)
        assert (value, carried) == divmod(numerator + carry, wall)
        value_before, carry_before = division_back(numerator, wall, value, carried)
        assert carry_before == carry
        assert value_before == -((carry - numerator) // wall)
    term = HoldTerm("content", (1, 3, 6), (1, 4, 2), None, 1, 1)
    loaded = apply(term, HoldStart(THE_LOAD, 64, (3120, 0, 0), 12480, None), HoldOwn({}, {}))
    assert loaded.time_level == 0 and dict(loaded.own.values)[(1,)] == 64 * 4 * 3120 // 12480 == 64
    assert all(now == before for _part, now, before in loaded.parts)
    advanced = apply(term, HoldStart(THE_ADVANCE, 64, (3120, 0, 0), 12480, None), loaded.own)
    assert advanced.time_level == 64  # the count over the divisor 1, this interval's source
    assert [(p, b) for p, _n, b in advanced.parts] == [(p, n) for p, n, _b in loaded.parts]
    rewritten = apply(term, HoldStart(THE_REWRITE, 64, (3120, 0, 0), 12480, None), advanced.own)
    assert rewritten.own == advanced.own and all(
        n == b == dict(advanced.own.values)[(p,)] for p, n, b in rewritten.parts
    )
    back = apply(term, HoldStart(THE_INVERSE, 64, (3120, 0, 0), 12480, None), advanced.own)
    assert dict(back.own.values) == dict(loaded.own.values) and dict(back.own.carries) == dict(
        loaded.own.carries
    )


def test_the_dipoles_terms_are_the_table_of_9_91_3():
    """A spin S at the body's Node writes sigma x (S x e_j)_i at the Node + sigma e_j (S x e_x = (0, S_z,
    -S_y) and cyclic); the moment the same over the divisor 2; a zero vector writes no dipole."""

    def cross(vector, j):
        out = [0, 0, 0]
        for i, component, sign in CROSS_TERMS[j]:
            out[i] = sign * vector[component]
        return tuple(out)

    assert cross((1, 2, 3), 0) == (0, 3, -2) and cross((1, 2, 3), 1) == (-3, 0, 1)
    assert cross((1, 2, 3), 2) == (2, -1, 0)
    gravity = HoldTerm("content", (1, 3, 6), (1, 4, 2), "spin", 1, 1)
    writes = apply(gravity, HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 1)), HoldOwn({}, {}))
    assert keyed(writes.dipoles) == {((1, 0, 1), 1), ((1, 0, -1), -1), ((0, 1, 1), -1), ((0, 1, -1), 1)}
    charge = HoldTerm("sign", (1, 3), (1, 1), "moment", 2, 1)
    first = apply(charge, HoldStart(THE_LOAD, 1, (0, 0, 0), 3, (0, 0, 1)), HoldOwn({}, {}))
    assert keyed(first.dipoles) == {((1, 0, 1), 0), ((1, 0, -1), -1), ((0, 1, 1), -1), ((0, 1, -1), 0)}
    assert all(carry == 1 for key, carry in first.own.carries.items() if key[0] == "d")
    second = apply(charge, HoldStart(THE_ADVANCE, 1, (0, 0, 0), 3, (0, 0, 1)), first.own)
    assert keyed(second.dipoles) == {((1, 0, 1), 1), ((1, 0, -1), 0), ((0, 1, 1), 0), ((0, 1, -1), 1)}
    unheld = apply(charge, HoldStart(THE_UNHOLD, 1, (0, 0, 0), 3, (0, 0, 1)), second.own)
    assert keyed(unheld.dipoles) == {(key, now) for key, now, _b in second.dipoles}
    assert dict(unheld.own.carries) == dict(first.own.carries) and dict(unheld.own.values) == dict(
        first.own.values
    )
    assert (
        apply(gravity, HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 0)), HoldOwn({}, {})).dipoles == ()
    )
    assert (
        apply(
            HoldTerm("content", (1,), (1,), "spin", 1, 1),
            HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 1)),
            HoldOwn({}, {}),
        ).dipoles
        == ()
    )


def keyed(dipoles):
    return {(key, now) for key, now, _b in dipoles}


def term_of(count, parts, factors, dipole, divisor):
    return HoldTerm(count, parts, factors, dipole, divisor, 1)


def act(term, start):
    return apply(term, start, HoldOwn({}, {}))


def test_the_refusals_by_name():
    with pytest.raises(ValueError, match="count word is 'mass'"):
        act(term_of("mass", (1,), (1,), None, 1), HoldStart(THE_LOAD, 1, (0, 0, 0), 1, None))
    with pytest.raises(ValueError, match="act is one of"):
        act(term_of("content", (1,), (1,), None, 1), HoldStart("the hop", 1, (0, 0, 0), 1, None))
    with pytest.raises(ValueError, match="go group for group"):
        act(term_of("content", (1, 3), (1,), None, 1), HoldStart(THE_LOAD, 1, (0, 0, 0), 1, None))
    with pytest.raises(ValueError, match="from 1"):
        act(term_of("content", (1,), (1,), None, 1), HoldStart(THE_LOAD, 1, (0, 0, 0), 0, None))
    with pytest.raises(ValueError, match="divisor E_s is from 1"):
        act(HoldTerm("content", (1,), (1,), None, 1, 0), HoldStart(THE_LOAD, 1, (0, 0, 0), 1, None))
    assert ACTS == (THE_LOAD, THE_ADVANCE, THE_REWRITE, THE_INVERSE, THE_UNHOLD)


def test_the_source_adds_the_count_over_the_divisor_each_interval_and_steps_back():
    """The time part is this interval's increment (count + r) div E_s with the remainder carried, 0 at the load; the inverse returns the increment it subtracts and steps the store back."""
    term = HoldTerm("content", (1,), (1,), None, 1, 7)
    loaded = apply(term, HoldStart(THE_LOAD, 10, (0, 0, 0), 1, None), HoldOwn({}, {}))
    own = loaded.own  # the load's division leaves the remainder 3 on the body; no increment is written
    assert loaded.time_level == 0
    increments = []
    for _ in range(7):
        writes = apply(term, HoldStart(THE_ADVANCE, 10, (0, 0, 0), 1, None), own)
        own, increments = writes.own, increments + [writes.time_level]
    assert increments == [1, 2, 1, 2, 1, 2, 1] and sum(increments) == 10  # exact over seven intervals
    back = apply(term, HoldStart(THE_INVERSE, 10, (0, 0, 0), 1, None), own)
    assert (
        back.time_level == 1 and dict(back.own.carries)[(0,)] == 0 and dict(back.own.values)[(0,)] == 2
    )


def test_the_declaration_is_the_ledgers_row():
    """ "the hold" at (iv), the word the right side, the writes a family's level at a Node and a body's
    remainders, its function `apply`; the register finds the folder bound: the loop calls `apply`."""
    assert DECLARATION.name == "the hold" and folder_of("the hold") == "hold"
    assert DECLARATION.place == "(iv)" and DECLARATION.word == "the right side"
    assert DECLARATION.writes == ("a family's level at a Node", "a body's remainders")
    assert DECLARATION.function is apply and DECLARATION.built
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    registered = simulation.register.declarations["the hold"]
    assert registered.binder is None and registered.function is apply
