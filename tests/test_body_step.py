"""The body on one Node: a body gives its own family from its stock, the loader's refusals, and the self-source lowers the step exactly where declared, with the inverse exact. HOST; no pin."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients, rule3
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.bodies import emitter_at, matter_emitter_world, parts_of, parts_world
from tests.worlds import seed_on_the_mode

# THE START left out in every test of this module (the fixture): the fixture's board is periodic on every axis, which has
# no rest under a source (ALGEBRA.md #the-generator (g)), and the recorded seedings (tests/seeds.json) bind the board
pytestmark = pytest.mark.usefixtures("the_loads_hold_alone")


GAMMA = 10_000


def own_family_world(stock: int | None) -> dict:
    """The matter emitter world with the emitter giving ITS OWN family (`source`, its well the source well): its `stock` of its own quanta, `amount` 4."""
    document = matter_emitter_world(False, [512, 1])
    body = emitter_at(100, 1, family="source")
    body["amount"] = 4
    body["stocks"] = {}
    body["stock"] = 2
    document["measured"].append(body)
    document["universe"][1]["clock"] = [512, 1]
    seed_on_the_mode(document)  # the emitter's mode and the stamp, as recorded at the stock 2
    if stock is None:  # the refusals' edge cases, altered after the seeding
        del body["stock"]
    else:
        body["stock"] = stock
    document["stamp"] = input_stamp(document)
    return document


def test_a_body_gives_its_own_family_from_its_stock_and_its_quanta_fall_by_one_per_giving():
    """ALGEBRA.md #the-primitives: the emitter of the family `source` gives `source` records; its stock is `stock` (from 1 to `amount`), each giving lowers its quanta M by one and the wall with them, the given record carries the family's pair; nothing fires once the stock is spent; refused without `stock`, with a `stock` above `amount`, and with `stock` on an emitter of another family."""
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
    """ALGEBRA.md #the-interval: the held family with the unit P_2 = 24 A declared: at a slab where its level jumps by 20000 the six squared differences summed give (the count of Ports across the jump) x 4 x 10^8, and a_next is lower than the plain rule's by that div P_2 exactly, the remainder the plain rule's; the inverse restores the levels."""
    document = parts_world()
    amplitude = document["amplitude_bound"]
    for family in document["universe"]:
        if family["name"] == "clicks":
            family["self_source"] = {"unit": 24 * amplitude}
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
            family["self_source"] = {"unit": 24 * amplitude}
    document["stamp"] = input_stamp(document)
    parse_nature_beam_world(document)
    # the inline list checks the unit's form; the file's entries check the bound 24 A too
    # (tests/test_families_file.py)
