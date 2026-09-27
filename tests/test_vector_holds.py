"""The holds of every part: a body writes gravity's time, vector and tensor parts and the charge's time part and current at its support, the remainders carried and inverted with it; the spin's and the moment's dipoles on the six neighbours; a part no body sources stays zero. HOST; at rest bit for bit with the scalar engine."""

from __future__ import annotations

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.hold import CROSS_TERMS, TENSOR_AXES
from event_universe.world_files import parse_nature_beam_world
from tests.bodies import parts_of, parts_world


def test_a_moving_body_writes_the_vector_and_tensor_parts_with_the_remainders_carried():
    """The body at momentum n = (64, 0, 0) on its wall W and content s: gravity's x part at its
    Nodes (4 s n_x + r) div W, xx (2 s n_x^2 + r) div W^2, the other components 0 (n_y = n_z
    = 0); the remainders carried, so over intervals the written value steps between the two
    integers around 4 s n_x / W with the mean the exact fraction; the charge Q = 2 gives its
    time part 2 and its current (2 n_x) div W; every unsourced part exactly zero and silent."""
    document = parts_world(momentum=[64, 0, 0], q=2)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    block = simulation.blocks[0]
    s = sum(simulation.held[0])
    wall = simulation.wall_of(block)
    gravity = parts_of(simulation, "clicks")
    charge = parts_of(simulation, "charge")
    assert [record.part for record in gravity] == list(range(10))
    inside = block.mask
    assert int(gravity[0].now[inside].min()) == s == int(gravity[0].now[inside].max())
    assert int(gravity[1].now[inside].min()) == (4 * s * 64) // wall == int(gravity[1].now[inside].max())
    assert int(gravity[4].now[inside].min()) == (2 * s * 64 * 64) // (wall * wall)
    for part in (2, 3, 5, 6, 7, 8, 9):
        assert not gravity[part].now.any() and gravity[part].silent, part
    assert int(charge[0].now[inside].min()) == 2 == int(charge[0].now[inside].max())
    assert int(charge[1].now[inside].max()) == (2 * 64) // wall
    assert not charge[2].now.any() and charge[2].silent
    # the carried remainder: the written values over 40 holds average the exact fraction
    written = []
    for _ in range(40):
        simulation.step()
        at_body = gravity[1].now[block.mask]  # the body hops: read at its Nodes now
        assert int(at_body.min()) == int(at_body.max())
        written.append(int(at_body[0]))
    exact = 4 * s * 64 / wall
    assert min(written) in (int(exact), int(exact) + 1) and max(written) in (int(exact), int(exact) + 1)
    assert abs(sum(written) / len(written) - exact) < 1.0 / len(written) + 1e-9
    assert simulation.leaks() == []
    # the source spreads by the plain step: the part is nonzero beyond the body and sourced
    assert gravity[1].now[~block.mask].any() and not gravity[1].silent
    assert TENSOR_AXES[3] == (0, 1) and CROSS_TERMS[0] == ((1, 2, 1), (2, 1, -1))


def test_a_body_at_rest_with_spin_and_moment_writes_the_dipoles_and_inverts_exactly():
    """At rest with S = (0, 0, 5) and mu = (4, 0, 0): gravity's vector part at the Node +
    sigma e_j gains sigma (S x e_j)_i, the charge's (sigma (mu x e_j)_i) div 2 with the
    remainder carried (so 0 and 1 alternate where mu x e_j is odd); the support's vector and
    tensor parts stay 0 (n = 0); the backward run restores the start exactly, the dipoles
    taken back and the carried divisions stepped back."""
    document = parts_world(spin=[0, 0, 5], moment=[4, 0, 0])
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    gravity = parts_of(simulation, "clicks")
    charge = parts_of(simulation, "charge")
    centre = (4, 3, 3)
    # S x e_x = (0, S_z, -S_y) = (0, 5, 0): the y component at the Node +- e_x gains +-5
    assert int(gravity[2].now[5, 3, 3]) == 5 and int(gravity[2].now[3, 3, 3]) == -5
    # S x e_y = (-S_z, 0, S_x) = (-5, 0, 0): the x component at the Node +- e_y gains -+5
    assert int(gravity[1].now[4, 4, 3]) == -5 and int(gravity[1].now[4, 2, 3]) == 5
    assert not gravity[3].now.any()  # S x e_z = (S_y, -S_x, 0) = 0
    assert int(gravity[1].now[centre]) == 0 and int(gravity[4].now[centre]) == 0
    # mu x e_y = (-mu_z, 0, mu_x) = (0, 0, 4): the z component at +- e_y gains (+-4) div 2 = +-2
    assert int(charge[3].now[4, 4, 3]) == 2 and int(charge[3].now[4, 2, 3]) == -2
    # mu x e_z = (mu_y, -mu_x, 0) = (0, -4, 0): the y component at +- e_z gains -+2
    assert int(charge[2].now[4, 3, 4]) == -2 and int(charge[2].now[4, 3, 2]) == 2
    assert simulation.leaks() == []
    start = {
        (name, record.part): (record.now.copy(), record.before.copy(), record.remainder.copy())
        for name in ("clicks", "charge")
        for record in parts_of(simulation, name)
    }
    # the carried divisions with a remainder (the spin's step adds its keys at 0, commit 6)
    carry = {str(k): v for k, v in simulation.blocks[0].hold_carry.items() if v}
    for _ in range(6):
        simulation.step()
    # the adds spread by the plain step between the holds; the field is nonzero and sourced
    assert gravity[2].now.any() and not gravity[2].silent and simulation.leaks() == []
    for _ in range(6):
        simulation.step_inverse()
    for key, (now, before, remainder) in start.items():
        record = next(r for r in parts_of(simulation, key[0]) if r.part == key[1])
        assert np.array_equal(record.now, now) and np.array_equal(record.before, before), key
        assert np.array_equal(record.remainder, remainder), key
    assert {str(k): v for k, v in simulation.blocks[0].hold_carry.items() if v} == carry


def test_at_rest_without_numbers_every_other_part_is_silent_and_the_scalar_engine_stands():
    """A body with no momentum, spin, moment or charge writes the time parts alone; every other
    part is zero and silent at every interval (ALGEBRA.md #the-interval), the leak test empty."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(parts_world()))
    for _ in range(10):
        simulation.step()
    for name in ("clicks", "charge"):
        for record in parts_of(simulation, name)[1:]:
            assert record.silent and not record.now.any() and not record.remainder.any()
    assert simulation.leaks() == [] and not any(simulation.blocks[0].hold_value.values())
