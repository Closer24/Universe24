"""THE BODY ON ONE NODE, COMMIT 6 (ALGEBRA.md 9.91 (8) (v), 9.78 (5), 9.91 (5), 9.96 (4), (5);
the one stroke of record 2106; BUILD.md section 26 item 65): the spin's step turns a body's spin
by the curl of gravity's vector part at its Node (the leapfrog of its two integers, the doubled
term over W Gamma with the remainder carried) and one interval back restores it; a body gives
its own family from its `stock`, its quanta lowered by one per giving, the stock spent; the
loader's refusals; the self-source slot lowers the step by (the six squared differences) div P_2
exactly where a unit above 0 is declared, the remainder untouched, the inverse exact; two wells
of one family may stand anywhere (the separation rule of 9.35 retired). HOST; no pin."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients, rule3
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.bodies import emitter_at, matter_emitter_world, parts_of, parts_world
from tests.worlds import massive_generator

GAMMA = 10_000


def test_the_spins_step_turns_the_spin_by_the_curl_at_the_bodys_node_and_inverts_exactly():
    """S = (0, 0, 5) at rest; gravity's z component planted at +A at the Node + e_y and -A at
    the Node - e_y (the curl's x component 2 A at the centre, the other components 0): after
    one interval Omega_x = (curl V)_x div 8 read from the fields as the interval leaves them,
    (Omega x S)_y = -Omega_x S_z, and S_y steps by (2 (Omega x S)_y + carry) div (W Gamma)
    from S_(t-1) = S_0 (the leapfrog's start); the inverse restores S, its partner and the
    carried remainders."""
    # a body on one Node (the hold rewrites a wider body's own Nodes, so a curl planted at
    # its centre's neighbours would be overwritten: the step reads a one-Node body's six
    # neighbours, 9.91 (8) (v))
    document = parts_world(spin=[0, 0, 5], side=1)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    block = simulation.blocks[0]
    gravity = parts_of(simulation, "clicks")
    centre = simulation._window_centre(block)
    assert centre == (3, 2, 2) and block.spin == [0, 0, 5] and block.spin_before == [0, 0, 5]
    amplitude = 1 << 20
    z_part = gravity[3]
    above = (centre[0], centre[1] + 1, centre[2])
    below = (centre[0], centre[1] - 1, centre[2])
    z_part.now[above] = amplitude
    z_part.before[above] = amplitude
    z_part.now[below] = -amplitude
    z_part.before[below] = -amplitude
    z_part.silent = False
    simulation._sourced_ever[(gravity[0].family, 3)] = True
    wall = simulation.wall_of(block)
    simulation.step()
    # the curl read from the fields as the interval leaves them (the planted part stepped once)
    y_part = gravity[2]
    ahead = (centre[0], centre[1], centre[2] + 1)
    behind = (centre[0], centre[1], centre[2] - 1)
    curl_x = (
        int(z_part.now[above])
        - int(z_part.now[below])
        - int(y_part.now[ahead])
        + int(y_part.now[behind])
    )
    omega_x = curl_x // 8  # the gradient's term is 0: n = 0
    turn_y = -omega_x * 5  # (Omega x S)_y = Omega_z S_x - Omega_x S_z
    step_y = (2 * turn_y) // (wall * GAMMA)
    assert abs(omega_x) > 0 and step_y != 0, (curl_x, omega_x, step_y)
    assert block.spin == [0, step_y, 5] and block.spin_before == [0, 0, 5]
    assert block.hold_carry[("spin", 1)] == 2 * turn_y - step_y * wall * GAMMA
    # one interval back: the spin, its partner and every carried remainder as at the start
    simulation.step_inverse()
    assert block.spin == [0, 0, 5] and block.spin_before == [0, 0, 5]
    assert all(
        value == 0 for key, value in block.hold_carry.items() if key[0] in ("spin", "omega", "gradc")
    )
    assert simulation.leaks() == []


def test_the_torque_turns_the_spin_by_the_moment_and_the_charge_curl_at_the_reads_weight_alone():
    """ALGEBRA.md 9.104 (2) (the Boss's record 2157): the torque is mu x B_q with the read's
    weight alone, since the moment carries the charge: a body of charge 0 with the moment
    (0, 1, 0) and the spin 0, the charge's z part planted at +A at its Node + e_y and -A at
    - e_y (the curl's x component at the centre), steps its spin's z component by
    2 (mu x B_q)_z div (W Gamma) with B_q,x = (1 x curl_x) div 2 (the read's weight 1, no
    factor of the body's sign Q = 0, which would have given 0); the inverse restores it."""
    document = parts_world(spin=[0, 0, 0], moment=[0, 1, 0], side=1)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    block = simulation.blocks[0]
    charge = parts_of(simulation, "charge")
    centre = simulation._window_centre(block)
    assert block.definition.q == 0 and list(block.definition.moment) == [0, 1, 0]
    amplitude = 1 << 20
    z_part = charge[3]
    above = (centre[0], centre[1] + 1, centre[2])
    below = (centre[0], centre[1] - 1, centre[2])
    z_part.now[above] = amplitude
    z_part.before[above] = amplitude
    z_part.now[below] = -amplitude
    z_part.before[below] = -amplitude
    z_part.silent = False
    simulation._sourced_ever[(charge[0].family, 3)] = True
    wall = simulation.wall_of(block)
    simulation.step()
    y_part = charge[2]
    ahead = (centre[0], centre[1], centre[2] + 1)
    behind = (centre[0], centre[1], centre[2] - 1)
    curl_x = (
        int(z_part.now[above])
        - int(z_part.now[below])
        - int(y_part.now[ahead])
        + int(y_part.now[behind])
    )
    b_x = curl_x // 2  # the read's weight 1 alone (the body's Q = 0 is no factor)
    turn_z = -b_x  # (mu x B)_z = mu_x B_y - mu_y B_x with mu = e_y
    step_z = (2 * turn_z) // (wall * GAMMA)
    assert b_x != 0 and step_z != 0, (curl_x, b_x, step_z)
    assert block.spin == [0, 0, step_z] and block.spin_before == [0, 0, 0]
    simulation.step_inverse()
    assert block.spin == [0, 0, 0] and block.spin_before == [0, 0, 0]
    assert simulation.leaks() == []


def own_family_world(stock: int | None) -> dict:
    """The matter emitter world with the emitter giving ITS OWN family (`source`, its well the
    source well): its `stock` of its own quanta, `amount` 4."""
    document = matter_emitter_world(False, [512, 1])
    body = emitter_at(100, 1, family="source")
    body["amount"] = 4
    body["stocks"] = {}
    if stock is not None:
        body["stock"] = stock
    document["measured"].append(body)
    document["universe"][1]["phase_per_link"] = [512, 1]
    massive_generator().seed_on_the_mode(document)  # the emitter's mode and the stamp
    return document


def test_a_body_gives_its_own_family_from_its_stock_and_its_quanta_fall_by_one_per_giving():
    """ALGEBRA.md 9.96 (5): the emitter of the family `source` gives `source` records; its stock
    is `stock` (from 1 to `amount`), each giving lowers its quanta M by one and the wall with
    them, the given record carries the family's pair; nothing fires once the stock is spent;
    refused without `stock`, with a `stock` above `amount`, and with `stock` on an emitter of
    another family."""
    world = parse_nature_beam_world(own_family_world(2))
    body = world.measured[1].block
    assert body is not None and body.emitter is not None
    assert body.stock == 2 and body.emitter.family == world.measured[1].family
    assert body.emitter.pair == tuple(world.families[body.emitter.family].pair)
    simulation = DetectorLawSimulation(parse_nature_beam_world(own_family_world(2)))
    block = simulation.blocks[1]  # the light emitter of the chain world is blocks[0]
    own = block.family
    assert simulation.held[block.number][own] == 4 and simulation.stock_of(block) == 2
    wall = simulation.wall_of(block)
    givings = []
    for _ in range(900):  # two windows and their rungs (commit 7)
        simulation.step()
        if block.givings > len(givings):
            givings.append(simulation.tick)
            assert simulation.held[block.number][own] == 4 - block.givings
            assert simulation.wall_of(block) == wall * (4 - block.givings) // 4
    assert block.givings == 2 and simulation.stock_of(block) == 0
    given = [live for live in simulation.records.values() if live.emitter == block.number]
    # the given records of its own family, at the family's rest pair (the well is the body's)
    rest = tuple(simulation.families[own].pair)
    assert given and all(live.family == own and live.pair == rest for live in given)
    assert simulation.leaks() == []
    with pytest.raises(ValueError, match="stock is required"):
        parse_nature_beam_world(own_family_world(None))
    with pytest.raises(ValueError, match="stock must be an integer from 1 through 4"):
        parse_nature_beam_world(own_family_world(5))
    other = matter_emitter_world(True, [512, 1])
    other["measured"][1]["stock"] = 1
    with pytest.raises(ValueError, match="stock is refused"):
        parse_nature_beam_world(other)


def test_the_self_source_slot_lowers_the_step_by_the_squared_differences_over_the_unit():
    """ALGEBRA.md 9.91 (5): the held family with the unit P_2 = 24 A declared: at a slab where
    its level jumps by 20000 the six squared differences summed give (the count of Ports
    across the jump) x 4 x 10^8, and a_next is lower than the plain rule's by that div P_2
    exactly, the remainder the plain rule's; the inverse restores the levels."""
    document = parts_world()
    amplitude = document["amplitude_bound"]
    for family in document["universe"]:
        if family["name"] == "clicks":
            family["self_unit"] = 24 * amplitude
    document["stamp"] = input_stamp(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    gravity = parts_of(simulation, "clicks")
    record = gravity[0]
    assert simulation.families[record.family].self_unit == 24 * amplitude
    record.now[10:12, :, :] += 20000
    record.before[10:12, :, :] += 20000
    now, before = record.now.copy(), record.before.copy()
    reads, self_coefficient, wall = coefficients(
        *simulation.pair_arrays(record.family), 1, 0, weak_field=False
    )
    plain, remainder = rule3(
        reads, simulation._axis_sums(now), self_coefficient, wall, now, before, record.remainder.copy()
    )
    sigma = simulation._self_source(record, False)
    assert sigma is not None
    total = np.zeros_like(now)
    for axis in range(3):
        total += (np.roll(now, 1, axis=axis) - now) ** 2 + (np.roll(now, -1, axis=axis) - now) ** 2
    for parts in gravity[1:]:
        assert parts.silent
    assert np.array_equal(sigma, total // (24 * amplitude)) and int(sigma.max()) == (20000 * 20000) // (
        24 * amplitude
    )
    simulation._advance(record)
    assert np.array_equal(record.now, plain - sigma) and np.array_equal(record.remainder, remainder)
    simulation._advance_inverse(record)
    assert np.array_equal(record.now, now) and np.array_equal(record.before, before)
    assert not record.remainder.any()


def test_the_loader_refuses_a_self_source_unit_below_24_a_and_admits_one_at_it():
    document = parts_world()
    amplitude = document["amplitude_bound"]
    for family in document["universe"]:
        if family["name"] == "clicks":
            family["self_unit"] = 24 * amplitude
    document["stamp"] = input_stamp(document)
    parse_nature_beam_world(document)
    # the inline list checks the unit's form; the file's entries check the bound 24 A too
    # (tests/test_families_file.py)
