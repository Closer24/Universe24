"""Direct channel APIs reject invalid capacities before any allocation or work."""

from dataclasses import replace

import pytest

from event_universe.core import spatial_state
from event_universe.core.disturbance_state import (
    OPERATIONS,
    CostMeter,
    FieldDefinition,
    OperationCosts,
    pack,
)
from event_universe.core.spatial_state import SpatialFieldDefinition, zero_spatial_state
from event_universe.fields import local_field_rules, spatial_coupling, spatial_plan


class IndexTrap:
    def __index__(self):
        raise AssertionError("port capacity was used before exact integer validation")


@pytest.mark.parametrize("count", [True, False, -1, 0, 1, 27, 1 << 100, 2.0, "6", None, IndexTrap()])
def test_invalid_channel_count_is_rejected_before_buffers_or_model_work(monkeypatch, count):
    def allocate(*arguments):
        raise AssertionError("port buffers allocated before validating their capacity")

    # Guard entry into the buffer-building work instead of requesting an unsafe
    # allocation merely to demonstrate rejection of a huge direct API input.
    monkeypatch.setattr(spatial_state, "pack", allocate)
    monkeypatch.setattr(local_field_rules, "range", allocate, raising=False)
    monkeypatch.setattr(spatial_plan, "range", allocate, raising=False)
    monkeypatch.setattr(spatial_plan, "CostMeter", allocate)
    with pytest.raises(ValueError, match="port count"):
        zero_spatial_state(1, count)
    with pytest.raises(ValueError, match="port count"):
        local_field_rules.received_values((), (), (), count)
    meter = CostMeter(OperationCosts((1,) * len(OPERATIONS)))
    with pytest.raises(ValueError, match="port count"):
        local_field_rules.apply_field_rules((), (), (), (), meter, count)
    assert meter.total == 0
    law = spatial_plan.SpatialLaw((), (), (), meter.definitions, port_count=count)
    with pytest.raises(ValueError, match="port count"):
        law((), ())


@pytest.mark.parametrize("count", [0, 1, 27])
def test_direct_empty_coupling_rejects_invalid_port_capacity_before_allocation(monkeypatch, count):
    def allocate(*arguments):
        raise AssertionError("coupling allocated a port buffer before validating capacity")

    monkeypatch.setattr(spatial_coupling, "range", allocate, raising=False)
    law = spatial_coupling.SpatialCouplingLaw(
        (), (), OperationCosts((1,) * len(OPERATIONS)), port_offsets=((1, 0, 0),) * count
    )
    with pytest.raises(ValueError, match="port count"):
        law.forward_reaction((), (), ())


@pytest.mark.parametrize("count", [2, 3, 6, 26])
@pytest.mark.parametrize("components", [1, 3])
def test_bounded_direct_channels_keep_exact_values_and_existing_model_cost(count, components):
    field = FieldDefinition("stock", components, "unit", True, True)
    definition = SpatialFieldDefinition(0, pack((0,) * components), transport="local")
    blank = zero_spatial_state(components, count)
    assert blank.populations == blank.allocation_phases == ((1,) * components,) * 8
    assert blank.delivered == ((1,) * components,) * count
    # The direct storage contract accepts 2..26 lanes; physical topology closure
    # is a separate owner and can reject an odd reciprocal graph.
    value = tuple(range(1, components + 1))
    delivered = (*blank.delivered[:-1], pack(value))
    state = replace(blank, populations=(pack(value), *blank.populations[1:]), delivered=delivered)
    ports = local_field_rules.received_values((field,), (definition,), (state,), count)
    assert ports[:-1] == ((pack((0,) * components),),) * (count - 1)
    assert ports[-1] == (pack(value),)
    meter = CostMeter(OperationCosts((1,) * len(OPERATIONS)))
    states, outgoing = local_field_rules.apply_field_rules(
        (field,), (definition,), (), (state,), meter, count
    )
    assert states[0].populations == state.populations
    assert len(outgoing) == count
    assert all(channel == (pack((0,) * components),) for channel in outgoing)
    # Eight population reads, eight evaluations per component, and one final
    # retained-stock update per component: 17 scalar units or 35 vector units.
    assert meter.total == (17 if components == 1 else 35)
    empty_plan = spatial_plan.SpatialLaw((), (), (), meter.definitions, port_count=count)((), ())
    assert empty_plan.outgoing == ((),) * count
    assert empty_plan.cost == 1  # The empty proposal still charges its existing commit primitive.
