"""Independent real-engine expectations for the explicit momentum routing candidate."""

import importlib
from dataclasses import FrozenInstanceError

import pytest

from event_universe.core.disturbance_state import MAX_VALUE, unpack

routing = importlib.import_module("examples.coarse-graining.routing")
PORTS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
EXPECTED_PERIOD = (0, 3, 0, 0, 0, 3, 0)


def sent(trace):
    return tuple(event for event in trace.events if event.event == "sent")


@pytest.mark.parametrize("scale", [1, 1000, MAX_VALUE // 5])
def test_momentum_routes_five_east_two_south_without_changing_owned_values(scale):
    momentum = (5 * scale, -2 * scale, 0)
    raw = routing.build_configuration(momentum)
    trace = routing.run_configuration(raw)
    assert tuple(event.port for event in sent(trace)) == EXPECTED_PERIOD * 4
    assert trace == routing.run_configuration(raw)
    assert raw["disturbance_types"][0]["transport"]["direction_field"] == "momentum"
    assert raw["disturbance_types"][0]["fields"] == ["energy", "momentum"]
    for owners in trace.samples:
        assert len(owners) == 1
        assert unpack(owners[0].record.values[0]) == (10,)
        assert unpack(owners[0].record.values[1]) == momentum
    start = trace.samples[0][0].position
    assert trace.samples[-1][0].position == (start[0] + 20, start[1] - 8, start[2])


@pytest.mark.parametrize("travel,budget", [(1, 1_000_000), (3, 1_000_000), (3, 100)])
def test_each_real_hop_is_one_cardinal_link_with_complete_transit(travel, budget):
    trace = routing.run_configuration(
        routing.build_configuration(link_ticks=travel, normal_budget=budget, ticks=42)
    )
    outgoing = sent(trace)
    incoming = tuple(event for event in trace.events if event.event == "received")
    assert len(outgoing) >= 2 and len(incoming) >= 2
    for departure, arrival in zip(outgoing, incoming, strict=False):
        delta = tuple(b - a for a, b in zip(departure.position, arrival.position, strict=True))
        assert delta == PORTS[departure.port]
        assert sum(abs(value) for value in delta) == 1
        assert arrival.tick == departure.tick + travel == departure.arrival_tick
        assert arrival.port == departure.port ^ 1
        assert arrival.momentum == departure.momentum == (5, -2, 0)
    assert all(b.tick - a.tick >= travel for a, b in zip(outgoing, outgoing[1:], strict=False))
    assert tuple(event.port for event in outgoing) == (EXPECTED_PERIOD * 6)[: len(outgoing)]
    for owners in trace.samples:
        assert len(owners) == 1
        assert unpack(owners[0].record.values[1]) == (5, -2, 0)
    if budget == 100:
        assert any(owner.pending is not None for owners in trace.samples for owner in owners)
    assert trace.model_operations_cost > 0


def test_rest_has_no_drift_and_does_not_invent_heading_or_routing_credit():
    trace = routing.run_configuration(routing.build_configuration((0, 0, 0)))
    assert trace.events == ()
    assert all(owners == trace.samples[0] for owners in trace.samples)
    record = trace.samples[0][0].record
    assert record.route_count_codes == record.route_weight_codes == (1,) * 6
    assert record.route_phase_code == record.rate_remainder_code == 1
    assert trace.local_cycles_started > 0


def test_fractional_credit_and_balanced_counters_survive_transport():
    trace = routing.run_configuration(routing.build_configuration(rate_denominator=3, ticks=42))
    outgoing = sent(trace)
    assert tuple(event.port for event in outgoing) == EXPECTED_PERIOD * 2
    assert tuple(event.tick for event in outgoing) == tuple(range(2, 42, 3))
    first_period_counts = (
        (1, 0, 0, 0, 0, 0),
        (1, 0, 0, 1, 0, 0),
        (2, 0, 0, 1, 0, 0),
        (3, 0, 0, 1, 0, 0),
        (4, 0, 0, 1, 0, 0),
        (4, 0, 0, 2, 0, 0),
        (5, 0, 0, 2, 0, 0),
    )
    for tick, owners in enumerate(trace.samples[1:], 1):
        record = owners[0].record
        assert record.rate_remainder_code - 1 == tick % 3
        assert record.rate_credit_denominator == 1
        completed = tick // 3
        if completed:
            assert (
                tuple(code - 1 for code in record.route_count_codes)
                == first_period_counts[(completed - 1) % 7]
            )
            assert tuple(code - 1 for code in record.route_weight_codes) == (5, 0, 0, 2, 0, 0)
        else:
            assert record.route_count_codes == record.route_weight_codes == (1,) * 6
        assert record.route_phase_code == 1


def test_pending_route_keeps_original_registers_until_the_atomic_departure():
    trace = routing.run_configuration(
        routing.build_configuration(link_ticks=3, normal_budget=100, ticks=18)
    )
    assert trace.local_cycles_started == 1
    # Two reads, one route visit, one literal-rate evaluation, 512 balanced-route
    # charges, one send and one commit: 518 units, hence 15 extra ticks at B=100, L=3.
    assert trace.model_operations_cost == 518
    for owners in trace.samples[1:15]:
        owner = owners[0]
        assert owner.arrival_tick is None
        assert owner.pending.ready_tick == 15
        assert owner.pending.next_tick == 18
        assert owner.record.route_count_codes == owner.record.route_weight_codes == (1,) * 6
        departure = owner.pending.plan.departures[0]
        assert departure.port == 0
        assert departure.record.route_count_codes == (2, 1, 1, 1, 1, 1)
        assert departure.record.route_weight_codes == (6, 1, 1, 3, 1, 1)
    for owners in trace.samples[15:18]:
        owner = owners[0]
        assert owner.pending is None and owner.arrival_tick == 18
        assert owner.record.route_count_codes == (2, 1, 1, 1, 1, 1)
    arrived = trace.samples[18][0]
    assert arrived.pending is None and arrived.arrival_tick is None
    assert arrived.record == trace.samples[15][0].record


def test_retained_trace_records_are_immutable_and_capture_horizon_is_explicit():
    trace = routing.run_configuration(ticks=1)
    with pytest.raises((FrozenInstanceError, AttributeError)):
        trace.samples[0][0].record.route_phase_code = 2
    with pytest.raises(ValueError, match="trace ticks"):
        routing.run_configuration(ticks=routing.MAX_TRACE_TICKS + 1)
