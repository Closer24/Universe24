"""THE HOLD, its own folder (ALGEBRA.md 9.117 the row "the hold"; 9.91 (3); 9.119 item 2; record 2250):
every division through core.rule3; on the shipped moving Lorentz world the folder's carried divisions
give the loop's own values, carries and levels over forty intervals bit for bit; forward then back
returns the state exactly; the dipole's terms are 9.91 (3)'s table; the refusals; the declaration."""

from __future__ import annotations

import json
import random
from pathlib import Path

import numpy as np
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
from tests.test_emitter import emitter_world

ROOT = Path(__file__).resolve().parents[1]
MOVING = ROOT / "examples" / "events" / "toward_nature" / "lorentz_moving.json"


def term_of(simulation: DetectorLawSimulation, family: int) -> HoldTerm:
    definition = simulation.families[family]
    assert definition.held is not None
    return HoldTerm(
        definition.held,
        tuple(definition.parts),
        tuple(definition.held_factors),
        definition.held_dipole,
        definition.held_dipole_div,
    )


def start_of(simulation: DetectorLawSimulation, block, family: int, act: str) -> HoldStart:
    """The loop's own integers for one body after the interval: the count, the momentum, the wall, the dipole's vector."""
    definition = simulation.families[family]
    assert definition.held is not None
    if definition.held_dipole is None:
        vector = None
    elif definition.held_dipole == "spin":
        vector = (int(block.spin[0]), int(block.spin[1]), int(block.spin[2]))
    else:
        vector = tuple(int(v) for v in block.definition.moment)
    momentum = simulation._momentum_now(block)
    return HoldStart(
        act,
        simulation.body_source(block.number, definition.held),
        (int(momentum[0]), int(momentum[1]), int(momentum[2])),
        simulation.wall_of(block),
        vector,
    )


def engines_state(block, family: int) -> tuple[dict, dict]:
    """The loop's hold values and carries of one family, keyed as the folder keys them."""
    values, carries = {}, {}
    for source, target in ((block.hold_value, values), (block.hold_carry, carries)):
        for key, value in source.items():
            if key[0] == family and len(key) == 2 and isinstance(key[1], int):
                target[(key[1],)] = value
            elif key[0] == "d" and key[1] == family:
                target[("d",) + tuple(key[2:])] = value
    return values, carries


def test_the_folder_gives_the_loops_integers_on_the_moving_lorentz_world_bit_for_bit():
    """examples/events/toward_nature/lorentz_moving.json (the body of content 65 giving charge quanta at
    v = 1 / 4, its wall and count changing, its Nodes hopping): the load as the folder's load act and
    every interval as its advance act give the loop's values and carries of gravity's vector and
    tensor parts and of the charge's dipoles bit for bit over forty intervals, and the parts' levels."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(json.loads(MOVING.read_text())))
    block = simulation.block_by_number[0]
    owns = {}
    for family in simulation.held_records:
        owns[family] = apply(
            term_of(simulation, family), start_of(simulation, block, family, THE_LOAD), HoldOwn({}, {})
        ).own
        assert (dict(owns[family].values), dict(owns[family].carries)) == engines_state(block, family)
    seen_hop, seen_giving = False, False
    for _ in range(40):
        simulation.step()
        seen_hop = seen_hop or any(block.hop)
        for family in simulation.held_records:
            writes = apply(
                term_of(simulation, family),
                start_of(simulation, block, family, THE_ADVANCE),
                owns[family],
            )
            owns[family] = writes.own
            assert (dict(writes.own.values), dict(writes.own.carries)) == engines_state(block, family)
            assert writes.time_level == simulation.body_source(
                block.number, simulation.families[family].held
            )
            assert np.all(simulation.held_records[family].now[block.mask] == writes.time_level)
            centre = tuple(int(axis[0]) for axis in np.nonzero(simulation.centre_mask(block)))
            for part, now, before in writes.parts:
                record = simulation.held_parts[family][
                    part - 1
                ]  # the body's Node, no dipole lands on it
                assert int(record.now[centre]) == now and int(record.before[centre]) == before
        seen_giving = seen_giving or simulation.wall_of(block) != 3 * simulation.momentum_unit * 65
    assert seen_hop and seen_giving
    gravity = next(f for f in simulation.held_records if simulation.families[f].name == "gravity")
    charge = next(f for f in simulation.held_records if simulation.families[f].name == "charge")
    assert (
        owns[gravity].values[(1,)] == 65 and owns[gravity].carries[(4,)] != 0
    )  # the vector along x, the tensor xx
    assert {key for key in owns[charge].values if key[0] == "d"} == {
        ("d", 1, 0, 1),
        ("d", 1, 0, -1),
        ("d", 0, 1, 1),
        ("d", 0, 1, -1),
    }


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


def test_the_folder_gives_the_loops_integers_backward_on_the_resting_lorentz_world_bit_for_bit():
    """examples/events/toward_nature/lorentz_rest.json (no hop, so the loop's inverse is defined): twenty
    intervals forward with the advance act, then twenty of the loop's `step_inverse`, each the unhold
    act then the inverse act, the loop's integers read after each: the values and carries of every
    held family agree bit for bit on the way back, and the end state is the start state."""
    rest = ROOT / "examples" / "events" / "toward_nature" / "lorentz_rest.json"
    simulation = DetectorLawSimulation(parse_nature_beam_world(json.loads(rest.read_text())))
    block = simulation.block_by_number[0]
    owns = {}
    for family in simulation.held_records:
        owns[family] = apply(
            term_of(simulation, family), start_of(simulation, block, family, THE_LOAD), HoldOwn({}, {})
        ).own
    start = {family: (dict(own.values), dict(own.carries)) for family, own in owns.items()}
    for _ in range(20):
        simulation.step()
        for family in simulation.held_records:
            owns[family] = apply(
                term_of(simulation, family),
                start_of(simulation, block, family, THE_ADVANCE),
                owns[family],
            ).own
    for _ in range(20):
        simulation.step_inverse()
        for family in simulation.held_records:
            # the loop's interval back: the dipoles' divisions stepped back (the unhold), then
            # the parts' (the inverse), the dipoles' levels read from the stepped-back state
            for act in (THE_UNHOLD, THE_INVERSE):
                owns[family] = apply(
                    term_of(simulation, family), start_of(simulation, block, family, act), owns[family]
                ).own
            assert (dict(owns[family].values), dict(owns[family].carries)) == engines_state(
                block, family
            )
    assert {family: (dict(own.values), dict(own.carries)) for family, own in owns.items()} == start
