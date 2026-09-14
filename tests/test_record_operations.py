"""Local record-policy expectations independent of physical field names."""

from dataclasses import replace

import pytest

from event_universe.core.disturbance_engine import DisturbanceEngine
from event_universe.core.disturbance_state import MAX_VALUE, pack, unpack
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.fields.record_operations import RecordOperations
from event_universe.initialization import parse_initial_state
from tests.support.disturbances import document, field, kind


def fixture(mode="split", value=(2, -3, 1)):
    raw = document(
        [kind("parcel", mode=mode, values={"quantity": list(value)})],
        [((0, 0, 0), "parcel")],
        fields=[field("quantity", 3)],
        capacity=3,
    )
    initial = parse_initial_state(raw)
    policy = RecordOperations(initial.fields, initial.disturbances)
    return initial, policy, initial.seeds[0].record


def test_delivered_vectors_merge_by_type_and_channel_with_exact_components():
    _, policy, resident = fixture()
    incoming = replace(resident, values=(pack((-1, 5, -1)),))
    result = policy.receive((resident, None), (incoming,), frozenset())
    assert unpack(result[0].values[0]) == (1, 2, 0)
    assert result[1] is None
    assert unpack(resident.values[0]) == (2, -3, 1)
    assert unpack(incoming.values[0]) == (-1, 5, -1)


@pytest.mark.parametrize("boundary", ["locked", "channel", "type", "whole"])
def test_independent_owners_are_never_folded_into_a_resident(boundary):
    _, policy, resident = fixture("move" if boundary == "whole" else "split")
    incoming = resident
    locked = frozenset({0}) if boundary == "locked" else frozenset()
    if boundary == "channel":
        incoming = replace(resident, channel_code=2)
    if boundary == "type":
        policy = replace(policy, disturbances=policy.disturbances * 2)
        incoming = replace(resident, type_index=1)
    result = policy.receive((resident, None), (incoming,), locked)
    assert result == (resident, incoming)


@pytest.mark.parametrize("mode", ["move", "split"])
def test_arrival_uses_spare_slot_after_a_reserved_empty_slot(mode):
    _, policy, resident = fixture(mode)
    local = (resident, None, None)
    result = policy.receive(local, (resident,), frozenset({0, 1}))
    assert result == (resident, None, resident)
    assert local == (resident, None, None)


def test_reserved_empty_slots_do_not_count_as_receiving_capacity():
    _, policy, incoming = fixture("move")
    local, arrivals = (None, None), (incoming,)
    with pytest.raises(ValueError, match="receiving capacity exhausted"):
        policy.receive(local, arrivals, frozenset({0, 1}))
    assert local == (None, None)
    assert arrivals == (incoming,)


@pytest.mark.parametrize("mode", ["move", "split"])
@pytest.mark.parametrize("count", [2, 3])
def test_arrival_batch_respects_reservations_and_remaining_capacity(mode, count):
    _, policy, resident = fixture(mode)
    local = (resident, None, None, None)
    arrivals = tuple(replace(resident, channel_code=i + 1) for i in range(count))
    if count == 2:
        assert policy.receive(local, arrivals, frozenset({0, 1})) == (
            resident,
            None,
            *arrivals,
        )
    else:
        with pytest.raises(ValueError, match="receiving capacity exhausted"):
            policy.receive(local, arrivals, frozenset({0, 1}))
    assert local == (resident, None, None, None)
    assert tuple(record.channel_code for record in arrivals) == tuple(range(1, count + 1))


@pytest.mark.parametrize("failure", ["overflow", "capacity"])
def test_failed_arrival_batch_keeps_all_input_records_unchanged(failure):
    _, policy, resident = fixture(value=(MAX_VALUE - 1, 0, 0))
    first = replace(resident, values=(pack((1, 0, 0)),))
    last = first if failure == "overflow" else replace(first, channel_code=2)
    local, arrivals = (resident,), (first, last)
    with pytest.raises((OverflowError, ValueError)):
        policy.receive(local, arrivals, frozenset())
    assert unpack(local[0].values[0]) == (MAX_VALUE - 1, 0, 0)
    assert all(unpack(record.values[0]) == (1, 0, 0) for record in arrivals)


def test_zero_records_wake_only_for_configured_work():
    _, policy, record = fixture("hold", value=(0, 0, 0))
    assert not policy.has_work((None,))
    assert not policy.has_work((record,))
    assert replace(policy, spatial_types=frozenset({0})).has_work((record,))
    _, moving, moving_record = fixture("move", value=(0, 0, 0))
    assert moving.has_work((moving_record,))


def test_zero_held_records_wake_for_configured_checks():
    raw = document(
        [kind("parcel", mode="hold", values={"quantity": 0})],
        [((0, 0, 0), "parcel")],
        fields=[field("quantity")],
    )
    raw["disturbance_types"][0]["checks"] = [
        {"name": "positive", "expression": {"op": "gt", "args": [{"field": "quantity"}, 0]}}
    ]
    initial = parse_initial_state(raw)
    policy = RecordOperations(initial.fields, initial.disturbances)
    assert policy.has_work((initial.seeds[0].record,))


def test_cost_report_changes_only_the_configured_reporter_without_repricing():
    raw = document(
        [kind("counter", values={"work": 0, "other": 7})],
        [((0, 0, 0), "counter")],
        fields=[field("work", conserved=False), field("other")],
    )
    raw["disturbance_types"][0]["cost_field"] = "work"
    initial = parse_initial_state(raw)
    policy = RecordOperations(initial.fields, initial.disturbances)
    law = DisturbanceLaw(initial.fields, initial.disturbances, (), initial.operation_costs)
    plan = law((initial.seeds[0].record,), (), 0)
    combined = replace(plan, cost=17)
    result = policy.report_cost(combined)
    assert result.cost == 17
    assert unpack(result.replacements[0][1].values[0]) == (17,)
    assert unpack(result.replacements[0][1].values[1]) == (7,)
    assert result.departures == plan.departures
    assert result.source_delta == plan.source_delta
    assert result.coupling_remainders == plan.coupling_remainders
    assert combined.replacements == plan.replacements


def test_engine_uses_injected_activity_policy_without_interpreting_fields():
    class SleepingPolicy(RecordOperations):
        def has_work(self, records):
            return False

    initial, _, _ = fixture("move")
    law = DisturbanceLaw(initial.fields, initial.disturbances, (), initial.operation_costs)
    world = DisturbanceEngine(
        initial, law, record_policy=SleepingPolicy(initial.fields, initial.disturbances)
    )
    world.step()
    assert world.computation_report()["local_cycles_started"] == 0
    assert not world.links
    assert world.totals() == {"quantity": (2, -3, 1)}


def test_engine_rejects_policy_capacity_change_before_clearing_arrivals():
    class InvalidPolicy(RecordOperations):
        def receive(self, resident, arrivals, locked):
            return ()

    initial, _, _ = fixture("move")
    initial = replace(initial, link_ticks=2)
    law = DisturbanceLaw(initial.fields, initial.disturbances, (), initial.operation_costs)
    world = DisturbanceEngine(
        initial, law, record_policy=InvalidPolicy(initial.fields, initial.disturbances)
    )
    world.step()
    before = dict(world.links)
    with pytest.raises(ValueError, match="cannot change local capacity"):
        world.step()
    assert dict(world.links) == before
    assert world.faulted
