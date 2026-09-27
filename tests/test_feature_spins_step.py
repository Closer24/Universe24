"""THE SPIN'S STEP, its own folder (ALGEBRA.md 9.117 the row "the spin's step"; 9.78 (5); 9.104
(2); 9.119 item 2; the Boss's record 2250): the curls and the gradient are the loop's reads at
the body's Node, Omega x S and mu x B_q bookings, every division through core.rule3; on the
shipped moving Lorentz world and on the resting one with a spin given to its emitter the
folder's step gives the loop's own spin, spin before, values and carries over thirty intervals
bit for bit; the inverse undoes the advance exactly; the refusals; the declaration."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.register import folder_of
from event_universe.core.rule3 import THE_ADVANCE, THE_INVERSE
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.spins_step import (
    DECLARATION,
    SpinRead,
    SpinStepOwn,
    SpinStepStart,
    SpinStepTerm,
    apply,
    bind,
    cross,
)
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.test_emitter import emitter_world

ROOT = Path(__file__).resolve().parents[1]
TOWARD = ROOT / "examples" / "events" / "toward_nature"
KEYS = ("gradc", "omega", "bq", "spin")
# the family's row's weights of the spin's turn, Schiff's 1 / 2 and 3 / 2 in the levels' unit (ALGEBRA.md 9.78 (5))
CURL_WEIGHT, TIDAL_WEIGHT = (1, 4), (3, 4)


def gradient_at(
    simulation: DetectorLawSimulation, content: np.ndarray, centre, wrap
) -> tuple[int, int, int]:
    """The loop's gradient of a time part at the body's Node, ahead minus behind per axis, 0 beyond an open face or on an axis of one layer."""
    found = [0, 0, 0]
    for axis in range(3):
        if simulation.shape[axis] == 1:
            continue
        ahead, behind = list(centre), list(centre)
        ahead[axis] += 1
        behind[axis] -= 1
        for node in (ahead, behind):
            if wrap[axis]:
                node[axis] %= simulation.shape[axis]
        inside = all(0 <= node[axis] < simulation.shape[axis] for node in (ahead, behind))
        if inside or wrap[axis]:
            found[axis] = int(content[ahead[0], ahead[1], ahead[2]]) - int(
                content[behind[0], behind[1], behind[2]]
            )
    return (found[0], found[1], found[2])


def reads_of(simulation: DetectorLawSimulation, block) -> tuple[SpinRead, ...]:
    """The loop's own reads at the body's Node after the interval: the curls and the gradient."""
    definition = simulation.families[block.family]
    centre = simulation._window_centre(block)
    wrap = simulation.kind_wrap[block.family]
    found = []
    for position, (other, weight, by, _twist) in enumerate(definition.reads):
        read = simulation.families[other]
        if len(read.parts) < 2 or read.held_dipole is None:
            continue
        curl = simulation._curl(simulation.held_parts[other][:3], centre, wrap)
        gradient = (
            gradient_at(simulation, simulation.held_records[other].now, centre, wrap)
            if read.held_dipole == "spin"
            else None
        )
        found.append(
            SpinRead(
                position,
                read.held_dipole,
                simulation._read_factor(block, weight, by),
                weight,
                (curl[0], curl[1], curl[2]),
                gradient,
            )
        )
    return tuple(found)


def engines_state(block) -> tuple[dict, dict]:
    values = {k: v for k, v in block.hold_value.items() if k[0] in KEYS}
    carries = {k: v for k, v in block.hold_carry.items() if k[0] in KEYS}
    return values, carries


def replay(document: dict, intervals: int) -> tuple[DetectorLawSimulation, SpinStepOwn]:
    """Run the world, and after every interval give the folder the loop's own integers; the folder's spin, spin before, values and carries must be the loop's."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    block = simulation.block_by_number[0]
    term = SpinStepTerm(tuple(block.definition.moment), simulation.node_clock, CURL_WEIGHT, TIDAL_WEIGHT)
    spin, before = tuple(block.spin), tuple(block.spin_before)
    own = SpinStepOwn({}, {})
    for _ in range(intervals):
        simulation.step()
        momentum = simulation._momentum_now(block)
        start = SpinStepStart(
            THE_ADVANCE,
            reads_of(simulation, block),
            (momentum[0], momentum[1], momentum[2]),
            simulation.wall_of(block),
            spin,
            before,
        )
        writes = apply(term, start, own)
        own, spin, before = writes.own, writes.spin, writes.spin_before
        assert (list(spin), list(before)) == (block.spin, block.spin_before)
        assert (dict(own.values), dict(own.carries)) == engines_state(block)
    return simulation, own


def test_the_shipped_moving_lorentz_world_bit_for_bit():
    """examples/events/toward_nature/lorentz_moving.json: the emitter's reads are gravity (the
    spin's dipole, its factor 1) and the charge by sign (the moment's dipole, weight 1); the
    folder's divisions of the tidal term, Omega, B_q and the spin give the loop's values and
    carries over thirty intervals bit for bit (the spin stays 0 there: B_q's carry alone moves)."""
    simulation, own = replay(json.loads((TOWARD / "lorentz_moving.json").read_text()), 30)
    assert {key[0] for key in own.values} == set(KEYS)
    assert simulation.block_by_number[0].spin == [0, 0, 0]


def test_the_resting_world_with_a_spin_given_turns_it_bit_for_bit():
    """The resting Lorentz world with the emitter's spin set to (0, 0, 5) at the load: its own
    dipole field's curl turns the spin (Omega x S over W Gamma with the carry), and the
    folder's spin, spin before, values and carries are the loop's over thirty intervals bit
    for bit; the carries move."""
    document = json.loads((TOWARD / "lorentz_rest.json").read_text())
    document["measured"][0]["spin"] = [0, 0, 5]
    document.pop("stamp", None)
    document["stamp"] = input_stamp(document)  # the changed integers restamped (record 1886)
    simulation, own = replay(document, 30)
    block = simulation.block_by_number[0]
    assert any(own.carries[key] for key in own.carries if key[0] in ("omega", "spin"))
    assert (
        block.spin != [0, 0, 0]
        or block.spin_before != [0, 0, 0]
        or any(own.carries[k] for k in own.carries)
    )


def test_the_inverse_undoes_the_advance_exactly():
    """On synthetic integers an advance then an inverse returns the spin, the spin before and the
    carries (the state before the advance); the omega, torque and steps of the inverse are the
    advance's, so the inverse subtracts what the step added."""
    term = SpinStepTerm((0, 0, 1), 10_000, CURL_WEIGHT, TIDAL_WEIGHT)
    reads = (
        SpinRead(0, "spin", 1, 1, (3, -7, 11), (2, 0, -1)),
        SpinRead(1, "moment", -1, 1, (5, 4, -9), None),
    )
    own = SpinStepOwn({}, {})
    spin, before = (10, -20, 30), (11, -19, 29)
    forward = apply(term, SpinStepStart(THE_ADVANCE, reads, (64, 0, 8), 12_480, spin, before), own)
    assert forward.spin_before == spin
    assert forward.omega != (0, 0, 0) and forward.torque != (0, 0, 0)
    backward = apply(
        term,
        SpinStepStart(THE_INVERSE, reads, (64, 0, 8), 12_480, forward.spin, forward.spin_before),
        forward.own,
    )
    assert (backward.spin, backward.spin_before) == (spin, before)
    assert all(carry == 0 for carry in backward.own.carries.values())  # the state before the advance
    assert backward.omega == forward.omega and backward.torque == forward.torque
    assert backward.steps == forward.steps
    assert cross((1, 0, 0), (0, 1, 0)) == (0, 0, 1) and cross((0, 1, 0), (1, 0, 0)) == (0, 0, -1)


def test_the_refusals_by_name():
    term = SpinStepTerm((0, 0, 0), 10_000, CURL_WEIGHT, TIDAL_WEIGHT)
    with pytest.raises(ValueError, match="act is one of"):
        apply(
            term, SpinStepStart("the hop", (), (0, 0, 0), 1, (0, 0, 0), (0, 0, 0)), SpinStepOwn({}, {})
        )
    with pytest.raises(ValueError, match="from 1"):
        apply(
            term, SpinStepStart(THE_ADVANCE, (), (0, 0, 0), 0, (0, 0, 0), (0, 0, 0)), SpinStepOwn({}, {})
        )
    with pytest.raises(ValueError, match=r"\(1, 2\) and \(3, 4\) stand over one denominator"):
        apply(
            SpinStepTerm((0, 0, 0), 1, (1, 2), TIDAL_WEIGHT),
            SpinStepStart(THE_ADVANCE, (), (0, 0, 0), 1, (0, 0, 0), (0, 0, 0)),
            SpinStepOwn({}, {}),
        )
    with pytest.raises(ValueError, match="spin or moment"):
        apply(
            term,
            SpinStepStart(
                THE_ADVANCE,
                (SpinRead(0, "charge", 1, 1, (0, 0, 0), None),),
                (0, 0, 0),
                1,
                (0, 0, 0),
                (0, 0, 0),
            ),
            SpinStepOwn({}, {}),
        )
    with pytest.raises(ValueError, match="needs the gradient"):
        apply(
            term,
            SpinStepStart(
                THE_ADVANCE,
                (SpinRead(0, "spin", 1, 1, (0, 0, 0), None),),
                (0, 0, 0),
                1,
                (0, 0, 0),
                (0, 0, 0),
            ),
            SpinStepOwn({}, {}),
        )


def test_the_declaration_is_the_ledgers_row():
    assert DECLARATION.name == "the spin's step" and folder_of(DECLARATION.name) == "spins_step"
    assert DECLARATION.place == "(v)" and DECLARATION.word == "after the step"
    assert DECLARATION.writes == ("a body's spin S", "a body's remainders")
    assert (
        DECLARATION.function is apply
        and DECLARATION.built
        and list(DECLARATION.schema) == ["spins_step"]
    )
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    registered = simulation.register.declarations["the spin's step"]
    assert registered.binder is bind and callable(registered.function)
