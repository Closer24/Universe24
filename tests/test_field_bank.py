"""Independent coexistence, extensibility and delivery contracts for one field bank."""

from dataclasses import replace

import pytest

from event_universe import Config
from event_universe.api import GenericFaceSimulation
from event_universe.core.field_bank import FieldBank
from event_universe.core.lattice import PeriodicLattice
from event_universe.diagnostics.measurements import total_momentum
from event_universe.fields.definitions import octant_definition, scalar_definition
from event_universe.fields.encoding import decode_signed, encode_values


def require_positive_records(record):
    if isinstance(record, tuple):
        return sum(require_positive_records(value) for value in record)
    assert type(record) is int and record > 0
    return 1


def test_two_field_types_coexist_and_third_definition_composes_without_engine_change():
    scalar = scalar_definition(source_strength=7, denominator=7)
    octants = octant_definition(source_per_octant=3)

    def oppose(faces):
        return tuple(-value for value in scalar.response(faces))

    inverse = replace(
        scalar,
        name="opposing-scalar",
        response=oppose,
        response_rule="opposite face imbalance with unit coupling",
    )
    lattice = PeriodicLattice((16, 16, 16))
    pair = FieldBank(lattice, (scalar, octants))
    extended = FieldBank(lattice, (scalar, octants, inverse))
    with pytest.raises(ValueError):
        FieldBank(lattice, (scalar, replace(octants, response_unit="incompatible-unit")))
    for phase in range(2):
        for bank in (pair, extended):
            bank.advance({(5, 5, 5): 1}, phase)
    target = (6, 5, 5)
    assert tuple(map(decode_signed, pair.at(target, 0).response_faces)) == (0, 1, 0, 0, 0, 0)
    assert tuple(map(decode_signed, pair.at(target, 1).response_faces)) == (0, 4, 0, 0, 0, 0)
    assert pair.response_at(target) == (-5, 0, 0)
    assert require_positive_records(pair.cells[target]) == 44
    assert extended.response_at(target) == (-4, 0, 0)
    for address in pair.cells:
        assert pair.at(address, 0) == extended.at(address, 0)
        assert pair.at(address, 1) == extended.at(address, 1)
    for records in extended.cells.values():
        require_positive_records(records)


def test_generic_simulation_applies_both_local_fields_and_preserves_total_momentum():
    world = GenericFaceSimulation(
        Config(nx=16, ny=16, nz=16, c_units=1000, force_den=1),
        collisions=True,
        definitions=(
            scalar_definition(source_strength=7, denominator=7),
            octant_definition(source_per_octant=3),
        ),
    )
    world.add_particle(0, 5, 5, 5)
    world.add_particle(1, 6, 5, 5, 100, 0, 0)
    for expected in (100, 96, 91):
        world.step()
        assert world.particles[1].momentum == (expected, 0, 0)
        assert world.particles[1].position == (6, 5, 5)
        assert total_momentum(world) == (100, 0, 0)
        for records in world.bank.cells.values():
            require_positive_records(records)


def test_packet_validation_rejects_entire_bank_update_without_partial_commit():
    scalar = scalar_definition(source_strength=7, denominator=7)
    with pytest.raises(ValueError):
        octant_definition().validate_packet(encode_values((-1, 0, 0, 0, 0, 0, 0, 0)))

    def malformed(state, source, phase):
        packets = scalar.publish(state, source, phase)
        if source and phase == 1:
            return ((0, 1), *packets[1:])
        return packets

    bad = replace(scalar, name="invalid-packet", publish=malformed)
    bank = FieldBank(PeriodicLattice((16, 16, 16)), (scalar, bad))
    bank.advance({(5, 5, 5): 1}, 0)
    before = dict(bank.cells)
    with pytest.raises((ValueError, OverflowError)):
        bank.advance({(5, 5, 5): 1}, 1)
    assert dict(bank.cells) == before


def test_field_definition_controls_allowed_ports_and_rejects_undefined_link_delay():
    scalar = scalar_definition(source_strength=7, denominator=7)

    def positive_x_only(state, source, phase):
        packets = scalar.publish(state, source, phase)
        return (packets[0], *(scalar.zero_packet for _ in range(5)))

    directed = replace(scalar, allowed_faces=(1, 2), allowed_directions=(1,), publish=positive_x_only)
    lattice = PeriodicLattice((16, 16, 16))
    bank = FieldBank(lattice, (directed,))
    with pytest.raises(ValueError):
        directed.validate_outgoing((scalar.zero_packet, (1, 2), *(scalar.zero_packet for _ in range(4))))
    for phase in range(2):
        bank.advance({(5, 5, 5): 1}, phase)
    assert bank.response_at((6, 5, 5)) == (-1, 0, 0)
    assert bank.response_at((4, 5, 5)) == bank.response_at((5, 6, 5)) == (0, 0, 0)

    with pytest.raises(NotImplementedError):
        FieldBank(lattice, (octant_definition(source_per_octant=3),), link_length=2)
    for invalid in (0, -1):
        with pytest.raises(ValueError):
            FieldBank(lattice, (scalar,), link_length=invalid)
