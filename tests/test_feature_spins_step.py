"""The spin's step folder, bound: the curl and the gradient as Rule3's read acts on the six neighbours, every division through core.rule3, the two weights from the family's entry; a planted curl and a moment's torque turn a resting spin, and the inverse restores it."""

from __future__ import annotations

from event_universe.core.rule3 import THE_ADVANCE, THE_INVERSE
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.spins_step import (
    SpinRead,
    SpinStepOwn,
    SpinStepStart,
    SpinStepTerm,
    apply,
    cross,
    curl,
    gradient,
)

# THE START left out (the fixture): a periodic board has no rest under a source; tests/seeds.json binds it


GAMMA = 10_000
# the row's weights of the spin's turn, Schiff's 1 / 2 and 3 / 2 in the levels' unit (ALGEBRA.md #a-familys-declaration)
TURN, NONE, ZERO = ((1, 4), (3, 4)), (None,) * 6, (0,) * 6


def planted(simulation: DetectorLawSimulation, parts, block) -> tuple[int, int]:
    """The family's z part planted at +A at the body's Node + e_y and -A at its Node - e_y, the curl's x component at the centre; the body's wall and, after one interval, the curl read from the fields as the interval leaves them."""
    centre, amplitude, z_part = simulation._window_centre(block), 1 << 20, parts[3]
    above, below = (centre[0], centre[1] + 1, centre[2]), (centre[0], centre[1] - 1, centre[2])
    z_part.now[above] = amplitude
    z_part.before[above] = amplitude
    z_part.now[below] = -amplitude
    z_part.before[below] = -amplitude
    z_part.silent = False
    simulation._sourced_ever[(parts[0].family, 3)] = True
    wall = simulation.wall_of(block)
    simulation.step()
    y_part = parts[2]
    ahead, behind = (centre[0], centre[1], centre[2] + 1), (centre[0], centre[1], centre[2] - 1)
    z_now, y_now = z_part.now, y_part.now
    curl_x = int(z_now[above]) - int(z_now[below]) - int(y_now[ahead]) + int(y_now[behind])
    return wall, curl_x


def test_the_curl_and_the_gradient_are_the_read_acts_on_the_six_neighbours():
    """(curl V)_x = V_z(+y) - V_z(-y) - V_y(+z) + V_y(-z) and cyclic, a missing neighbour 0; the gradient ahead minus behind per axis, 0 on an axis with a neighbour missing."""
    vector = (ZERO, (0, 0, 0, 0, 5, -7), (0, 0, 3, -11, 0, 0))
    assert curl(vector) == (3 + 11 - 5 - 7, 0, 0)
    assert curl((NONE, (None, None, None, None, 5, None), NONE)) == (-5, 0, 0)
    assert gradient((9, 2, -4, 6, 0, 0)) == (7, -10, 0)
    assert gradient((9, None, -4, 6, None, None)) == (0, -10, 0)
    assert cross((1, 0, 0), (0, 1, 0)) == (0, 0, 1) and cross((0, 1, 0), (1, 0, 0)) == (0, 0, -1)


def test_the_inverse_undoes_the_advance_exactly():
    """On synthetic integers an advance then an inverse returns the spin, the spin before and the carries (the state before the advance); the omega, torque and steps of the inverse are the advance's, so the inverse subtracts what the step added."""
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
    own, spin, before = SpinStepOwn({}, {}), (10, -20, 30), (11, -19, 29)
    forward = apply(term, SpinStepStart(THE_ADVANCE, reads, (64, 0, 8), 12_480, spin, before), own)
    assert forward.spin_before == spin and forward.omega != (0, 0, 0) and forward.torque != (0, 0, 0)
    backward = apply(
        term,
        SpinStepStart(THE_INVERSE, reads, (64, 0, 8), 12_480, forward.spin, forward.spin_before),
        forward.own,
    )
    assert (backward.spin, backward.spin_before) == (spin, before)
    assert all(carry == 0 for carry in backward.own.carries.values())  # the state before the advance
    assert backward.omega == forward.omega and backward.torque == forward.torque
    assert backward.steps == forward.steps
