"""THE HOLD, its own folder (ALGEBRA.md 9.117 the row "the hold"; 9.91 (3); record 2250): every division
through core.rule3, forward then back exact; the dipole's terms 9.91 (3)'s table; the refusals; the card,
bound (#1231): the loop's hold is this folder's line, pinned by every shipped world's digest."""

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
    term = HoldTerm("content", (1, 3, 6), (1, 4, 2), None, 1)
    loaded = apply(term, HoldStart(THE_LOAD, 64, (3120, 0, 0), 12480, None), HoldOwn({}, {}))
    assert loaded.time_level == 64 and dict(loaded.own.values)[(1,)] == 64 * 4 * 3120 // 12480 == 64
    assert all(now == before for _part, now, before in loaded.parts)
    advanced = apply(term, HoldStart(THE_ADVANCE, 64, (3120, 0, 0), 12480, None), loaded.own)
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
    gravity = HoldTerm("content", (1, 3, 6), (1, 4, 2), "spin", 1)
    writes = apply(gravity, HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 1)), HoldOwn({}, {}))
    assert {(key, now) for key, now, _before in writes.dipoles} == {
        ((1, 0, 1), 1),
        ((1, 0, -1), -1),
        ((0, 1, 1), -1),
        ((0, 1, -1), 1),
    }
    charge = HoldTerm("sign", (1, 3), (1, 1), "moment", 2)
    first = apply(charge, HoldStart(THE_LOAD, 1, (0, 0, 0), 3, (0, 0, 1)), HoldOwn({}, {}))
    assert {(key, now) for key, now, _b in first.dipoles} == {
        ((1, 0, 1), 0),
        ((1, 0, -1), -1),
        ((0, 1, 1), -1),
        ((0, 1, -1), 0),
    }
    assert all(carry == 1 for key, carry in first.own.carries.items() if key[0] == "d")
    second = apply(charge, HoldStart(THE_ADVANCE, 1, (0, 0, 0), 3, (0, 0, 1)), first.own)
    assert {(key, now) for key, now, _b in second.dipoles} == {
        ((1, 0, 1), 1),
        ((1, 0, -1), 0),
        ((0, 1, 1), 0),
        ((0, 1, -1), 1),
    }
    unheld = apply(charge, HoldStart(THE_UNHOLD, 1, (0, 0, 0), 3, (0, 0, 1)), second.own)
    assert {(key, now) for key, now, _b in unheld.dipoles} == {
        (key, now) for key, now, _b in second.dipoles
    }
    assert dict(unheld.own.carries) == dict(first.own.carries) and dict(unheld.own.values) == dict(
        first.own.values
    )
    assert (
        apply(gravity, HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 0)), HoldOwn({}, {})).dipoles == ()
    )
    assert (
        apply(
            HoldTerm("content", (1,), (1,), "spin", 1),
            HoldStart(THE_LOAD, 5, (0, 0, 0), 15, (0, 0, 1)),
            HoldOwn({}, {}),
        ).dipoles
        == ()
    )


def test_the_refusals_by_name():
    with pytest.raises(ValueError, match="count word is 'mass'"):
        apply(
            HoldTerm("mass", (1,), (1,), None, 1),
            HoldStart(THE_LOAD, 1, (0, 0, 0), 1, None),
            HoldOwn({}, {}),
        )
    with pytest.raises(ValueError, match="act is one of"):
        apply(
            HoldTerm("content", (1,), (1,), None, 1),
            HoldStart("the hop", 1, (0, 0, 0), 1, None),
            HoldOwn({}, {}),
        )
    with pytest.raises(ValueError, match="go group for group"):
        apply(
            HoldTerm("content", (1, 3), (1,), None, 1),
            HoldStart(THE_LOAD, 1, (0, 0, 0), 1, None),
            HoldOwn({}, {}),
        )
    with pytest.raises(ValueError, match="from 1"):
        apply(
            HoldTerm("content", (1,), (1,), None, 1),
            HoldStart(THE_LOAD, 1, (0, 0, 0), 0, None),
            HoldOwn({}, {}),
        )
    assert ACTS == (THE_LOAD, THE_ADVANCE, THE_REWRITE, THE_INVERSE, THE_UNHOLD)


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
