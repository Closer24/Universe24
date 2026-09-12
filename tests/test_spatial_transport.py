"""Independent integer expectations for generic outward spatial transport."""

from dataclasses import replace

import pytest

from event_universe.core.disturbance_state import (
    MAX_VALUE,
    CostMeter,
    FieldDefinition,
    OperationCosts,
    pack,
    unpack,
)
from event_universe.core.spatial_state import SpatialFieldDefinition, zero_spatial_state
from event_universe.fields.spatial import (
    OCTANT_SIGNS,
    add_payloads,
    add_populations,
    emission_amount,
    emit,
    split_outward,
    split_weighted,
)


def meter():
    return CostMeter(OperationCosts((1,) * 9))


def field(components=1, signed=True):
    return FieldDefinition("custom", components, "unit", signed, True)


def definition(components=1, **kwargs):
    return SpatialFieldDefinition(0, pack((0,) * components), **kwargs)


def test_signed_vector_partitions_keep_every_component_and_leave_no_stock():
    initial = zero_spatial_state(3)
    initial = replace(initial, populations=(pack((14, -14, 1)), *initial.populations[1:]))
    outgoing, retained = split_outward(initial, definition(3, axis_weights=(2, 1, 0)), field(3), meter())
    assert unpack(outgoing[0][0]) == (10, -10, 1)
    assert unpack(outgoing[2][0]) == (4, -4, 0)
    assert all(unpack(outgoing[port][0]) == (0, 0, 0) for port in (1, 3, 4, 5))
    assert all(unpack(payload) == (0, 0, 0) for payload in retained.populations)
    assert unpack(retained.allocation_phases[0]) == (2, 2, 1)
    assert tuple(
        sum(unpack(payload)[component] for port in outgoing for payload in port)
        for component in range(3)
    ) == (14, -14, 1)


@pytest.mark.parametrize("octant", range(8))
def test_every_octant_keeps_its_three_signs_and_never_reverses(octant):
    initial = zero_spatial_state(1)
    populations = list(initial.populations)
    populations[octant] = pack((3,))
    initial = replace(initial, populations=tuple(populations))
    outgoing, _ = split_outward(initial, definition(), field(), meter())
    expected_ports = {2 * axis + (sign < 0) for axis, sign in enumerate(OCTANT_SIGNS[octant])}
    for port in range(6):
        assert unpack(outgoing[port][octant]) == ((1,) if port in expected_ports else (0,))
        assert all(unpack(outgoing[port][other]) == (0,) for other in range(8) if other != octant)


def test_indivisible_emission_is_all_sent_and_successive_units_visit_all_octants():
    phase = pack((0,))
    cumulative = [0] * 8
    for expected in range(8):
        populations, phase = emit(pack((1,)), phase, definition(), field(), meter())
        assert [unpack(payload)[0] for payload in populations] == [
            int(octant == expected) for octant in range(8)
        ]
        for octant, payload in enumerate(populations):
            cumulative[octant] += unpack(payload)[0]
    assert cumulative == [1] * 8
    assert unpack(phase) == (0,)


def test_weighted_emission_preserves_signed_amount_and_disabled_octants():
    spec = definition(octant_weights=(1, 0, 0, 0, 0, 0, 0, 1))
    populations, phase = emit(pack((-5,)), pack((0,)), spec, field(), meter())
    assert [unpack(payload)[0] for payload in populations] == [-3, 0, 0, 0, 0, 0, 0, -2]
    assert unpack(phase) == (1,)


def test_fractional_source_retains_signed_residue_across_reversal():
    residue = pack((0,))
    outputs = []
    for numerator in (1, 1, 1, 1, -1, -1, -1, -1):
        amount, residue = emission_amount((numerator,), residue, 3, field(), meter())
        outputs.append(unpack(amount)[0])
    assert outputs == [0, 0, 1, 0, 0, 0, 0, -1]
    assert unpack(residue) == (0,)


def test_delivered_samples_are_not_reemitted_as_extra_inventory():
    initial = replace(zero_spatial_state(1), delivered=(pack((11,)),) * 6)
    outgoing, retained = split_outward(initial, definition(), field(), meter())
    assert all(unpack(payload) == (0,) for port in outgoing for payload in port)
    assert retained.delivered == initial.delivered


def test_baseline_does_not_implicitly_create_or_transport_inventory():
    outgoing, _ = split_outward(
        zero_spatial_state(1), SpatialFieldDefinition(0, pack((100,))), field(), meter()
    )
    assert all(unpack(payload) == (0,) for port in outgoing for payload in port)


def test_combine_validates_inputs_before_cancellation_or_overflow():
    with pytest.raises(ValueError, match="negative"):
        add_payloads(pack((-1,)), pack((5,)), field(signed=False), meter())
    with pytest.raises(ValueError, match="bound"):
        add_payloads(pack((MAX_VALUE,)), pack((1,)), field(), meter())
    combined = add_populations((pack((2,)),) * 8, (pack((-1,)),) * 8, field(), meter())
    assert [unpack(payload)[0] for payload in combined] == [1] * 8


@pytest.mark.parametrize(
    ("weights", "phase"),
    [((0, 0, 0), 0), ((-1, 2, 0), 0), ((1, 1, 1), 3), ((1, 1, 1), -1), ((MAX_VALUE, 1), 0)],
)
def test_invalid_weight_or_phase_bounds_fail(weights, phase):
    with pytest.raises(ValueError):
        split_weighted(1, weights, phase)


def test_bad_population_shape_and_unsigned_negative_fail_before_emission():
    initial = zero_spatial_state(1)
    with pytest.raises(ValueError, match="eight octants"):
        split_outward(replace(initial, populations=()), definition(), field(), meter())
    initial = replace(initial, populations=(pack((-1,)), *initial.populations[1:]))
    with pytest.raises(ValueError, match="negative"):
        split_outward(initial, definition(), field(signed=False), meter())


def test_invalid_source_residue_denominator_and_output_bounds_fail():
    for residue, denominator in ((pack((1,)), 1), (pack((0,)), 0)):
        with pytest.raises(ValueError):
            emission_amount((1,), residue, denominator, field(), meter())
    with pytest.raises(ValueError, match="bound"):
        emission_amount((MAX_VALUE + 1,), pack((0,)), 1, field(), meter())


def test_every_transport_operation_has_a_declared_cost():
    measured = meter()
    initial = replace(zero_spatial_state(1), populations=(pack((3,)),) * 8)
    split_outward(initial, definition(), field(), measured)
    assert measured.total == 8 * (1 + 1 + 1) + 6
