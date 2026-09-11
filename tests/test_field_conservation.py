"""Independent local quantity balances and exact directional batching."""

from dataclasses import replace

import pytest

from event_universe import Config
from event_universe.api import GenericFaceSimulation
from event_universe.core.field_bank import FieldBank
from event_universe.core.lattice import PeriodicLattice
from event_universe.core.state import MAX_CORE_INT, MAX_WORK_INT
from event_universe.fields.conservation import split_ratio
from event_universe.fields.definitions import octant_definition, scalar_definition
from event_universe.fields.encoding import decode_values, encode_signed, encode_values


def test_direction_ratio_retains_indivisible_amount_instead_of_turning_it():
    portions, remainder = split_ratio(1, (2, 1, 0))
    assert portions == (0, 0, 0) and remainder == 1
    portions, remainder = split_ratio(2, (2, 1, 0), remainder)
    assert portions == (2, 1, 0) and remainder == 0
    assert split_ratio(8, (2, 1, 0)) == ((4, 2, 0), 2)
    assert split_ratio(MAX_CORE_INT + 1, (1, 1)) == ((1073741824, 1073741824), 0)
    assert split_ratio(MAX_CORE_INT, (2, 1, 0), 2) == ((1431655766, 715827883, 0), 0)
    with pytest.raises(OverflowError):
        split_ratio(MAX_WORK_INT + 1, (1, 1))


@pytest.mark.parametrize(
    "amount,weights,remainder",
    [(-1, (2, 1, 0), 0), (1, (0, 0, 0), 0), (1, (2, -1, 0), 0), (1, (2, 1, 0), 3)],
)
def test_invalid_ratio_budget_is_rejected(amount, weights, remainder):
    with pytest.raises(ValueError):
        split_ratio(amount, weights, remainder)


def test_scalar_local_balance_preserves_source_and_multiple_arrivals_with_remainders():
    definition = scalar_definition(source_strength=7)
    old = encode_values((5, 1))
    outgoing, retained = definition.publish(old, 2, 0)
    assert definition.inventory_state(old) == (6,)
    assert definition.source_amount(2, 0) == (14,)
    assert definition.sink_amount(old, 2, 0) == (0,)
    assert tuple(decode_values(packet) for packet in outgoing) == ((3,),) * 6
    assert decode_values(retained) == (0, 2)
    incoming = tuple(encode_signed(value) for value in (3, 5, 0, 0, 0, 0))
    next_state, _ = definition.absorb(retained, incoming, 2, 0)
    assert decode_values(next_state) == (8, 2)
    assert definition.inventory_state(next_state) == (10,)
    # Independently fixed local ledger: old 6 + arrivals 8 + source 14 = next 10 + sent 18.
    assert 6 + 8 + 14 == 10 + sum(definition.inventory_packet(p)[0] for p in outgoing)


def test_octant_channels_keep_independent_retained_and_incoming_amounts():
    definition = octant_definition(source_per_octant=1)
    old = encode_values((2, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0))
    outgoing, retained = definition.publish(old, 1, 0)
    assert definition.inventory_state(old) == (3, 0, 0, 0, 0, 0, 0, 0)
    assert definition.inventory_state(retained) == (1,) * 8
    assert definition.source_amount(1, 0) == (1,) * 8
    assert definition.sink_amount(old, 1, 0) == (0,) * 8
    assert tuple(sum(definition.inventory_packet(p)[i] for p in outgoing) for i in range(8)) == (
        3,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    incoming = (
        encode_values((2, 1, 0, 0, 0, 0, 0, 0)),
        encode_values((3, 0, 0, 0, 0, 0, 0, 4)),
        *(definition.zero_packet for _ in range(4)),
    )
    next_state, _ = definition.absorb(retained, incoming, 1, 0)
    assert definition.inventory_state(next_state) == (6, 2, 1, 1, 1, 1, 1, 5)


def test_bank_rejects_undeclared_creation_without_committing_another_field():
    scalar = scalar_definition(source_strength=7)

    def create_one(old, incoming, sources, phase):
        state, faces = scalar.absorb(old, incoming, sources, phase)
        amount, remainder = decode_values(state)
        if sources:
            state = encode_values((amount + 1, remainder))
        return state, faces

    broken = replace(scalar, name="undeclared-creation", absorb=create_one)
    bank = FieldBank(PeriodicLattice((16, 16, 16)), (scalar, broken))
    before = dict(bank.cells)
    with pytest.raises(ValueError):
        bank.advance({(5, 5, 5): 1}, 0)
    assert dict(bank.cells) == before

    def drain_one(old, sources, phase):
        available = sum(decode_values(old)) + 6 * sources
        portions, remainder = split_ratio(available, (1,) * 6)
        return tuple(encode_signed(value) for value in portions), encode_values((0, remainder))

    draining = replace(
        scalar,
        name="explicit-one-unit-sink",
        publish=drain_one,
        sink_amount=lambda old, sources, phase: (sources,),
        decay_rule="Discard one unit per resident source, declared before publication.",
    )
    accepted = FieldBank(PeriodicLattice((16, 16, 16)), (draining,))
    accepted.advance({(5, 5, 5): 1}, 0)
    assert sum(draining.inventory_state(cells[0].state)[0] for cells in accepted.cells.values()) == 6
    assert accepted.response_at((6, 5, 5)) == (-1, 0, 0)


def test_generic_free_motion_keeps_signed_direction_ratio_and_fractional_credit():
    world = GenericFaceSimulation(
        Config(nx=32, ny=32, nz=32, c_units=12),
        definitions=(scalar_definition(source_strength=0), octant_definition(source_per_octant=0)),
    )
    world.add_particle(0, 16, 16, 16, 3, -2, 1, mass=2)
    for tick in range(1, 25):
        world.step()
        particle = world.particles[0]
        assert particle.momentum == (3, -2, 1)
        assert particle.mass == 2 and particle.momentum_den == 1
        assert particle.move_budget == 3 * (tick % 4)
        assert particle.move_budget_den == 1
        assert (particle.force_rx, particle.force_ry, particle.force_rz) == (0, 0, 0)
        assert not world.bank.cells
    assert particle.position == (19, 14, 17)
    assert particle.axis_phase == 0
