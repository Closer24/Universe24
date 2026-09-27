"""THE SPIN'S STEP, its own folder (ALGEBRA.md 9.117 the row "the spin's step"; 9.78 (5); 9.104
(2); 9.119 item 2; the Boss's record 2250), bound to the loop: the curl and the gradient are
Rule3's read acts on the six neighbours' levels, Omega x S and mu x B_q bookings, every division
through core.rule3, the row's two weights read from the family's entry; on a body at rest the loop
turns the spin by a planted curl and restores it one interval back, and the torque turns it by the
moment and the charge's curl at the read's weight alone; the inverse undoes the advance exactly on
synthetic integers; the refusals; the declaration, bound. HOST; no pin."""

from __future__ import annotations

import pytest

from event_universe.core.register import folder_of
from event_universe.core.rule3 import THE_ADVANCE, THE_INVERSE
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.spins_step import (
    DECLARATION,
    KEYS,
    SpinRead,
    SpinStepOwn,
    SpinStepStart,
    SpinStepTerm,
    apply,
    cross,
    curl,
    gradient,
)
from event_universe.world_files import parse_nature_beam_world
from tests.test_emitter import emitter_world
from tests.test_vector_holds import parts_of, parts_world

GAMMA = 10_000
# the row's weights of the spin's turn, Schiff's 1 / 2 and 3 / 2 in the levels' unit (ALGEBRA.md 9.78 (5))
TURN = ((1, 4), (3, 4))
NONE = (None,) * 6
ZERO = (0,) * 6


def planted(simulation: DetectorLawSimulation, parts, block) -> tuple[int, int]:
    """The family's z part planted at +A at the body's Node + e_y and -A at its Node - e_y, the curl's x component at the centre; the body's wall and, after one interval, the curl read from the fields as the interval leaves them."""
    centre = simulation._window_centre(block)
    amplitude = 1 << 20
    z_part = parts[3]
    above = (centre[0], centre[1] + 1, centre[2])
    below = (centre[0], centre[1] - 1, centre[2])
    z_part.now[above] = amplitude
    z_part.before[above] = amplitude
    z_part.now[below] = -amplitude
    z_part.before[below] = -amplitude
    z_part.silent = False
    simulation._sourced_ever[(parts[0].family, 3)] = True
    wall = simulation.wall_of(block)
    simulation.step()
    y_part = parts[2]
    ahead = (centre[0], centre[1], centre[2] + 1)
    behind = (centre[0], centre[1], centre[2] - 1)
    curl_x = (
        int(z_part.now[above])
        - int(z_part.now[below])
        - int(y_part.now[ahead])
        + int(y_part.now[behind])
    )
    return wall, curl_x


def test_the_loop_turns_the_spin_by_the_curl_at_the_bodys_node_and_inverts_exactly():
    """S = (0, 0, 5) at rest; gravity's z component planted at +A at the Node + e_y and -A at
    the Node - e_y (the curl's x component 2 A at the centre, the other components 0): after
    one interval Omega_x = (curl V)_x div (SPAN x 4) at the row's weight 1 / 4, read from the
    fields as the interval leaves them, (Omega x S)_y = -Omega_x S_z, and S_y steps by (2 (Omega
    x S)_y + carry) div (W Gamma) from S_(t-1) = S_0 (the leapfrog's start); the inverse restores
    S, its partner and the carried remainders. A body on one Node: the hold rewrites a wider
    body's own Nodes, so a curl planted at its centre's neighbours would be overwritten."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(parts_world(spin=[0, 0, 5], side=1)))
    block = simulation.blocks[0]
    assert simulation._window_centre(block) == (3, 2, 2)
    assert block.spin == [0, 0, 5] and block.spin_before == [0, 0, 5]
    wall, curl_x = planted(simulation, parts_of(simulation, "clicks"), block)
    omega_x = curl_x // 8  # the gradient's term is 0: n = 0
    turn_y = -omega_x * 5  # (Omega x S)_y = Omega_z S_x - Omega_x S_z
    step_y = (2 * turn_y) // (wall * GAMMA)
    assert abs(omega_x) > 0 and step_y != 0, (curl_x, omega_x, step_y)
    assert block.spin == [0, step_y, 5] and block.spin_before == [0, 0, 5]
    assert block.hold_carry[("spin", 1)] == 2 * turn_y - step_y * wall * GAMMA
    # one interval back: the spin, its partner and every carried remainder as at the start
    simulation.step_inverse()
    assert block.spin == [0, 0, 5] and block.spin_before == [0, 0, 5]
    assert all(value == 0 for key, value in block.hold_carry.items() if key[0] in KEYS)
    assert simulation.leaks() == []


def test_the_torque_turns_the_spin_by_the_moment_and_the_charge_curl_at_the_reads_weight_alone():
    """ALGEBRA.md 9.104 (2) (the Boss's record 2157): the torque is mu x B_q with the read's
    weight alone, since the moment carries the charge: a body of charge 0 with the moment
    (0, 1, 0) and the spin 0, the charge's z part planted at +A at its Node + e_y and -A at
    - e_y, steps its spin's z component by 2 (mu x B_q)_z div (W Gamma) with B_q,x = (1 x
    curl_x) div 2 (the read's weight 1, no factor of the body's sign Q = 0, which would have
    given 0); the inverse restores it."""
    document = parts_world(spin=[0, 0, 0], moment=[0, 1, 0], side=1)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    block = simulation.blocks[0]
    assert block.definition.q == 0 and list(block.definition.moment) == [0, 1, 0]
    wall, curl_x = planted(simulation, parts_of(simulation, "charge"), block)
    b_x = curl_x // 2  # the read's weight 1 alone (the body's Q = 0 is no factor)
    turn_z = -b_x  # (mu x B)_z = mu_x B_y - mu_y B_x with mu = e_y
    step_z = (2 * turn_z) // (wall * GAMMA)
    assert b_x != 0 and step_z != 0, (curl_x, b_x, step_z)
    assert block.spin == [0, 0, step_z] and block.spin_before == [0, 0, 0]
    simulation.step_inverse()
    assert block.spin == [0, 0, 0] and block.spin_before == [0, 0, 0]
    assert simulation.leaks() == []


def test_the_curl_and_the_gradient_are_the_read_acts_on_the_six_neighbours():
    """(curl V)_x = V_z(+y) - V_z(-y) - V_y(+z) + V_y(-z) and cyclic, a missing neighbour 0; the
    gradient ahead minus behind per axis, 0 on an axis with a neighbour missing."""
    vector = (ZERO, (0, 0, 0, 0, 5, -7), (0, 0, 3, -11, 0, 0))
    assert curl(vector) == (3 + 11 - 5 - 7, 0, 0)
    assert curl((NONE, (None, None, None, None, 5, None), NONE)) == (-5, 0, 0)
    assert gradient((9, 2, -4, 6, 0, 0)) == (7, -10, 0)
    assert gradient((9, None, -4, 6, None, None)) == (0, -10, 0)
    assert cross((1, 0, 0), (0, 1, 0)) == (0, 0, 1) and cross((0, 1, 0), (1, 0, 0)) == (0, 0, -1)


def test_the_inverse_undoes_the_advance_exactly():
    """On synthetic integers an advance then an inverse returns the spin, the spin before and the
    carries (the state before the advance); the omega, torque and steps of the inverse are the
    advance's, so the inverse subtracts what the step added."""
    term = SpinStepTerm((0, 0, 1), GAMMA)
    reads = (
        SpinRead(
            0,
            "spin",
            1,
            1,
            (ZERO, (0, 0, 0, 0, 50, -70), (0, 0, 300, -1100, 0, 0)),
            (9000, 2000, -4000, 6000, 1000, 0),
            TURN,
        ),
        SpinRead(1, "moment", -1, 1, ((0, 0, 0, 0, 4, 0), ZERO, (0, 0, 0, 9, 0, 0)), None, None),
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


def test_the_refusals_by_name():
    term = SpinStepTerm((0, 0, 0), GAMMA)
    own = SpinStepOwn({}, {})
    zeros = (ZERO, ZERO, ZERO)
    with pytest.raises(ValueError, match="act is one of"):
        apply(term, SpinStepStart("the hop", (), (0, 0, 0), 1, (0, 0, 0), (0, 0, 0)), own)
    with pytest.raises(ValueError, match="from 1"):
        apply(term, SpinStepStart(THE_ADVANCE, (), (0, 0, 0), 0, (0, 0, 0), (0, 0, 0)), own)
    # no silent default: the loader refuses by name a family holding the spin's dipole without its row
    document = parts_world(spin=[0, 0, 5], side=1)
    next(f for f in document["universe"] if f["name"] == "clicks").pop("spins_step")
    with pytest.raises(ValueError, match="holds the spin's dipole and lacks spins_step"):
        parse_nature_beam_world(document)
    with pytest.raises(ValueError, match="spin or moment"):
        reads = (SpinRead(0, "charge", 1, 1, zeros, None, None),)
        apply(term, SpinStepStart(THE_ADVANCE, reads, (0, 0, 0), 1, (0, 0, 0), (0, 0, 0)), own)
    with pytest.raises(ValueError, match="needs the time part at the six neighbours and its row"):
        reads = (SpinRead(0, "spin", 1, 1, zeros, None, TURN),)
        apply(term, SpinStepStart(THE_ADVANCE, reads, (0, 0, 0), 1, (0, 0, 0), (0, 0, 0)), own)
    with pytest.raises(ValueError, match=r"\(1, 2\) and \(3, 4\) stand over one denominator"):
        reads = (SpinRead(0, "spin", 1, 1, zeros, ZERO, ((1, 2), (3, 4))),)
        apply(term, SpinStepStart(THE_ADVANCE, reads, (0, 0, 0), 1, (0, 0, 0), (0, 0, 0)), own)


def test_the_declaration_is_the_ledgers_row():
    assert DECLARATION.name == "the spin's step" and folder_of(DECLARATION.name) == "spins_step"
    assert DECLARATION.place == "(v)" and DECLARATION.word == "after the step"
    assert DECLARATION.writes == ("a body's spin S", "a body's remainders")
    assert DECLARATION.function is apply and list(DECLARATION.schema) == ["spins_step"]
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=2)))
    registered = simulation.register.declarations["the spin's step"]
    assert registered.binder is None and registered.function is apply  # bound: the loop calls apply
