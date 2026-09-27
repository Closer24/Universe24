"""THE HOLDS OF EVERY PART (ALGEBRA.md 9.91 (3); 9.86 (2); the one stroke of record 2106,
commit 2; BUILD.md section 26 item 61): a body writes at every Node of its support, after the
held families' step, gravity's time part s, its vector 4 s n_a div W and its tensor 2 s n_a
n_b div W^2 (the factors the families file's), the charge's time part Q and its current Q n_a
div W; the divisions' remainders are carried between intervals on the body and inverted with
it; the spin's dipole sigma (S x e_j)_i and the moment's (sigma (mu x e_j)_i) div 2 are added
on the body's Node's six neighbours; a part no body sources stays exactly zero and silent (the
leak test per part). HOST; at rest bit for bit with the scalar engine."""

from __future__ import annotations

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.hold import CROSS_TERMS, TENSOR_AXES
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.test_massive_record import block_world

KIND = [800, 809]
WELL = [800, 801]
SHAPE = [16, 8, 8]


def parts_world(**body: object) -> dict:
    """A periodic board with one body of matter at [3, 2, 2] of side 3 and the families with
    parts: gravity [1, 3, 6] holding the content with the factors [1, 4, 2] and the spin's
    dipole, the charge [1, 3] holding the sign with the moment's dipole halved (the shipped
    file's entries on an inline list; light stays its own family here, the tests' list)."""
    block = {"position": [3, 2, 2], "side": 3, "pair": WELL, "margin": "control", **body}
    periodic = {"x": "periodic", "y": "periodic", "z": "periodic"}
    document = block_world(SHAPE, periodic, KIND, [block], ticks=20)
    document["age_bound"] = 100000  # a board periodic on every axis declares it
    for family in document["universe"]:
        if family["name"] == "clicks":
            family.update(
                {
                    "parts": [1, 3, 6],
                    "phase": 1,
                    "held": {"count": "content", "factors": [1, 4, 2], "dipole": "spin"},
                }
            )
        if family["name"] == "charge":
            family.update(
                {
                    "parts": [1, 3],
                    "held": {"count": "sign", "factors": [1, 1], "dipole": "moment", "dipole_div": 2},
                }
            )
    document["stamp"] = input_stamp(document)
    return document


def parts_of(simulation: DetectorLawSimulation, name: str) -> list:
    family = [family.name for family in simulation.families].index(name)
    return [simulation.held_records[family], *simulation.held_parts[family]]


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
    part is zero and silent at every interval (9.91 (9) (a)), the leak test empty."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(parts_world()))
    for _ in range(10):
        simulation.step()
    for name in ("clicks", "charge"):
        for record in parts_of(simulation, name)[1:]:
            assert record.silent and not record.now.any() and not record.remainder.any()
    assert simulation.leaks() == [] and not any(simulation.blocks[0].hold_value.values())
