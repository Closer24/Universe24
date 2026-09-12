"""Finite per-record coupling allowances measure absolute cumulative reaction."""

from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import (
    MAX_VALUE,
    OPERATIONS,
    DisturbanceRecord,
    Expression,
    FieldDefinition,
    OperationCosts,
    pack,
    unpack,
)
from event_universe.core.spatial_state import SpatialCouplingDefinition
from event_universe.fields.spatial_coupling import SpatialCouplingLaw
from event_universe.initialization import parse_initial_state


def fixture(value, budget, *, mode="exchange", denominator=1, definitions=None):
    components = len(value)
    fields = (
        FieldDefinition("inventory", components, "unit", True, True),
        FieldDefinition("driver", components, "request unit", True, False),
    )
    rule = SpatialCouplingDefinition(
        "bounded_request",
        0,
        0,
        mode,
        Expression("field", field=1, side=1),
        denominator=denominator,
        budget=None if budget is None else pack(budget),
    )
    definitions = (rule,) if definitions is None else definitions
    law = SpatialCouplingLaw(fields, definitions, OperationCosts((1,) * len(OPERATIONS)))
    zero = pack((0,) * components)
    record = DisturbanceRecord(0, (pack(value), zero), (zero, zero))
    return law, record


def apply(law, record, request):
    result = law((record,), (pack((0,) * len(request)), pack(request)))
    return result, result.records[0]


def amount(record):
    return unpack(record.values[0])


def remaining(record):
    return tuple(unpack(value) for value in record.spatial_remaining)


def test_scalar_exchange_stops_at_absolute_cumulative_allowance():
    law, record = fixture((10,), (5,))
    reaction = 0
    for request, expected_value, expected_remaining, expected_reaction in (
        (2, 8, 3, 2),
        (2, 6, 1, 2),
        (2, 6, 1, 0),
        (1, 5, 0, 1),
        (1, 5, 0, 0),
    ):
        result, record = apply(law, record, (request,))
        assert amount(record) == (expected_value,)
        assert remaining(record) == ((expected_remaining,),)
        assert result.reaction[0] == (expected_reaction,)
        reaction += expected_reaction
        assert amount(record)[0] + reaction == 10
    assert reaction == 5


def test_sign_reversal_does_not_refund_previously_spent_allowance():
    law, record = fixture((10,), (4,))
    reactions = []
    for request in (2, -2, 2, -2):
        result, record = apply(law, record, (request,))
        reactions.append(result.reaction[0][0])
    assert reactions == [2, -2, 0, 0]
    assert amount(record) == (10,)
    assert remaining(record) == ((0,),)
    assert sum(abs(value) for value in reactions) == 4


def test_one_insufficient_vector_component_rejects_every_component_and_fraction():
    law, record = fixture((5, 5, 0), (3, 1, 0), denominator=2)
    original_fraction = pack((1, -1, 0))
    record = replace(record, spatial_remainders=(original_fraction,))
    result, updated = apply(law, record, (3, 5, 0))
    # The candidate exchange is (2,2,0), but the second allowance is only one.
    assert amount(updated) == (5, 5, 0)
    assert remaining(updated) == ((3, 1, 0),)
    assert updated.spatial_remainders == (original_fraction,)
    assert result.reaction[0] == (0, 0, 0)


@pytest.mark.parametrize("budget,expected", [((5, 4, 0), (5, 0, 0)), ((5, 5, 0), (0, 5, 0))])
def test_rotation_is_whole_or_rejected_without_norm_loss(budget, expected):
    law, record = fixture((5, 0, 0), budget, mode="rotation")
    result, record = apply(law, record, (0, 0, 1))
    assert amount(record) == expected
    assert sum(value * value for value in amount(record)) == 25
    assert result.reaction[0] == tuple(a - b for a, b in zip((5, 0, 0), expected, strict=True))
    expected_remaining = ((5, 4, 0),) if budget[1] == 4 else ((0, 0, 0),)
    assert remaining(record) == expected_remaining


def test_fractional_rotation_accumulates_until_an_affordable_whole_turn():
    law, record = fixture((5, 0, 0), (5, 5, 0), mode="rotation", denominator=2)
    first, record = apply(law, record, (0, 0, 1))
    assert amount(record) == (5, 0, 0)
    assert remaining(record) == ((5, 5, 0),)
    assert tuple(unpack(value) for value in record.spatial_remainders) == ((0, 0, 1),)
    assert first.reaction[0] == (0, 0, 0)
    second, record = apply(law, record, (0, 0, 1))
    assert amount(record) == (0, 5, 0)
    assert remaining(record) == ((0, 0, 0),)
    assert second.reaction[0] == (5, -5, 0)
    third, final = apply(law, record, (0, 0, 1))
    assert final == record
    assert third.reaction[0] == (0, 0, 0)


def test_rejected_fractional_request_keeps_its_previous_remainder():
    law, record = fixture((10,), (1,), denominator=3)
    record = replace(record, spatial_remainders=(pack((1,)),))
    result, record = apply(law, record, (7,))
    assert result.reaction[0] == (0,)
    assert record.spatial_remainders == (pack((1,)),)
    assert remaining(record) == ((1,),)
    result, record = apply(law, record, (1,))
    assert result.reaction[0] == (0,)
    assert record.spatial_remainders == (pack((2,)),)


def test_exhausted_budget_skips_expression_evaluation_and_cannot_accrue_debt():
    law, record = fixture((10,), (0,), denominator=2)
    impossible = Expression(
        "exact_div", (Expression("literal", literal=(1,)), Expression("literal", literal=(0,)))
    )
    law = replace(law, definitions=(replace(law.definitions[0], expression=impossible),))
    record = replace(record, spatial_remainders=(pack((1,)),))
    result, record = apply(law, record, (1,))
    assert amount(record) == (10,)
    assert remaining(record) == ((0,),)
    assert record.spatial_remainders == (pack((1,)),)
    assert result.reaction[0] == (0,)
    with pytest.raises(ValueError):
        apply(replace(law, definitions=(replace(law.definitions[0], budget=None),)), record, (1,))


def test_budget_rejects_a_too_large_reaction_before_packing_it():
    law, record = fixture((MAX_VALUE, 0, 0), (MAX_VALUE, MAX_VALUE, MAX_VALUE), mode="rotation")
    result, updated = apply(law, record, (0, 0, 2))
    assert amount(updated) == (MAX_VALUE, 0, 0)
    assert remaining(updated) == ((MAX_VALUE, MAX_VALUE, MAX_VALUE),)
    assert result.reaction[0] == (0, 0, 0)
    assert updated.spatial_remainders == record.spatial_remainders
    legacy = replace(law, definitions=(replace(law.definitions[0], budget=None),))
    with pytest.raises(ValueError):
        apply(legacy, record, (0, 0, 2))


def test_unaffordable_exchange_work_value_is_rejected_before_payload_packing():
    law, record = fixture((10,), (1,))
    expression = Expression(
        "mul", (Expression("field", field=1, side=1), Expression("literal", literal=(MAX_VALUE,)))
    )
    law = replace(law, definitions=(replace(law.definitions[0], expression=expression),))
    result, updated = apply(law, record, (MAX_VALUE,))
    assert amount(updated) == (10,)
    assert remaining(updated) == ((1,),)
    assert updated.spatial_remainders == record.spatial_remainders
    assert result.reaction[0] == (0,)


def test_rejected_later_rule_preserves_an_earlier_successful_rule():
    first = SpatialCouplingDefinition(
        "first", 0, 0, "exchange", Expression("literal", literal=(2,)), budget=pack((2,))
    )
    second = replace(first, name="second", budget=pack((1,)))
    law, record = fixture((10,), (0,), definitions=(first, second))
    result, record = apply(law, record, (0,))
    assert amount(record) == (8,)
    assert remaining(record) == ((0,), (1,))
    assert result.reaction[0] == (2,)


def test_remaining_budget_has_no_allocation_for_another_type_or_an_unlimited_rule():
    first = SpatialCouplingDefinition(
        "owned", 0, 0, "exchange", Expression("literal", literal=(1,)), budget=pack((2,))
    )
    other = replace(first, name="other", type_index=1, budget=pack((9,)))
    unlimited = replace(
        first, name="unlimited", budget=None, expression=Expression("literal", literal=(0,))
    )
    law, record = fixture((10,), (0,), definitions=(first, other, unlimited))
    _, record = apply(law, record, (0,))
    assert remaining(record) == ((1,), (0,), (0,))


@pytest.mark.parametrize("invalid", [((3,),), ((-1,),), ((1, 0),), ((1,), (0,))])
def test_invalid_remaining_allowance_is_rejected_before_action(invalid):
    law, record = fixture((10,), (2,))
    record = replace(record, spatial_remaining=tuple(pack(value) for value in invalid))
    with pytest.raises(ValueError):
        apply(law, record, (1,))


def test_nonmatching_allowance_cannot_be_smuggled_onto_a_record():
    owned = SpatialCouplingDefinition(
        "owned", 0, 0, "exchange", Expression("literal", literal=(1,)), budget=pack((2,))
    )
    other = replace(owned, type_index=1)
    law, record = fixture((10,), (0,), definitions=(owned, other))
    record = replace(record, spatial_remaining=(pack((2,)), pack((1,))))
    with pytest.raises(ValueError, match="owned initial budget"):
        apply(law, record, (0,))


def test_legacy_unlimited_behavior_and_cost_are_unchanged():
    legacy, record = fixture((10,), None)
    result, updated = apply(legacy, record, (2,))
    assert amount(updated) == (8,)
    assert updated.spatial_remaining == ()
    assert result.reaction[0] == (2,)
    assert result.cost == 207
    finite = replace(legacy, definitions=(replace(legacy.definitions[0], budget=pack((4,))),))
    bounded_result, updated = apply(finite, record, (2,))
    assert amount(updated) == (8,)
    assert bounded_result.reaction == result.reaction
    assert remaining(updated) == ((2,),)
    # One allowance read before evaluation, then read/check/debit for one component.
    assert bounded_result.cost == 211


def initialization(*, delayed=False, emitting=False):
    raw = {
        "schema_version": 2,
        "model_id": "finite-spatial-reaction-v2",
        "shape": [31, 31, 31],
        "slots_per_cell": 2,
        "link_ticks": 2,
        "normal_budget": 100 if delayed else 100000,
        "ticks": 8,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {"name": "inventory", "components": 3, "units": "unit", "signed": True, "conserved": True},
            {"name": "driver", "components": 3, "units": "unit", "signed": True, "conserved": False},
        ],
        "disturbance_types": [
            {
                "name": "carrier",
                "fields": ["inventory"],
                "defaults": {"inventory": [5, 0, 0]},
                "transport": {"mode": "move", "direction_field": "inventory"},
            }
        ],
        "spatial_fields": [
            {
                "field": "inventory",
                "baseline": [0, 0, 0],
                "transport": "outward",
                "decay": {"retain_numerator": 1, "retain_denominator": 2},
            },
            {
                "field": "driver",
                "baseline": [0, 0, 1],
                "transport": "outward",
                "decay": {"retain_numerator": 1, "retain_denominator": 2},
            },
        ],
        "spatial_couplings": [
            {
                "name": "finite_turn",
                "type": "carrier",
                "field": "inventory",
                "mode": "rotation",
                "rotation": {"field": "driver", "side": "right"},
                "budget": [5, 5, 0],
            }
        ],
        "seeds": [{"position": [15, 15, 15], "type": "carrier"}],
    }
    if emitting:
        raw["emissions"] = [
            {
                "type": "carrier",
                "field": "driver",
                "amount": [0, 0, 8],
                "source": True,
                "budget": [0, 0, 24],
            }
        ]
    return raw


def accounted_inventory(world):
    return tuple(
        value + loss
        for value, loss in zip(
            world.totals()["inventory"], world.dissipation_totals()["inventory"], strict=True
        )
    )


@pytest.mark.parametrize(("delayed", "emitting"), [(False, False), (True, False), (True, True)])
def test_finite_allowance_commits_with_the_carrier_and_survives_movement(delayed, emitting):
    world = Simulation(parse_initial_state(initialization(delayed=delayed, emitting=emitting)))
    original = next(record for record in world.cells[(15, 15, 15)].records if record is not None)
    world.step()
    if delayed:
        ready = world.cells[(15, 15, 15)].pending.ready_tick
        assert ready >= 2
        emission_remaining = []
        while world.tick < ready:
            resident = next(record for record in world.cells[(15, 15, 15)].records if record is not None)
            assert resident.spatial_remaining == original.spatial_remaining
            assert amount(resident) == (5, 0, 0)
            if emitting:
                emission_remaining.append(unpack(resident.emission_remaining[0])[2])
            world.step()
        if emitting:
            assert emission_remaining[0] == 16
            assert set(emission_remaining) == {16, 8, 0}
    packets = [packet for group in world.links.values() for packet in group if packet is not None]
    assert len(packets) == 1
    assert remaining(packets[0].record) == ((0, 0, 0),)
    assert amount(packets[0].record) == (0, 5, 0)
    if emitting:
        assert packets[0].record.emission_remaining == (pack((0, 0, 0)),)
    arrival = packets[0].arrival_tick
    while world.tick < arrival:
        assert accounted_inventory(world) == (5, 0, 0)
        world.step()
    arrived = next(record for record in world.cells[(15, 16, 15)].records if record is not None)
    assert amount(arrived) == (0, 5, 0)
    assert remaining(arrived) == ((0, 0, 0),)
    for _ in range(40):
        cell = world.cells.get((15, 17, 15))
        if cell is not None and any(record is not None for record in cell.records):
            break
        world.step()
        assert accounted_inventory(world) == (5, 0, 0)
    else:
        pytest.fail("the exhausted carrier did not continue along its unchanged direction")
    later = next(record for record in world.cells[(15, 17, 15)].records if record is not None)
    assert amount(later) == (0, 5, 0)
    assert remaining(later) == ((0, 0, 0),)
    assert accounted_inventory(world) == (5, 0, 0)
    if emitting:
        assert later.emission_remaining == (pack((0, 0, 0)),)
