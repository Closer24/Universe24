"""Real node inputs, outputs and clocks under bounded configured topology."""

from copy import deepcopy
from dataclasses import FrozenInstanceError, asdict
from itertools import product

import pytest

from event_universe.core.disturbance_state import OPERATIONS
from event_universe.diagnostics.node_probe import NodeProbe
from event_universe.initialization import parse_initial_state

from .test_disturbance_engine import document as carrier_document
from .test_disturbance_engine import kind, resident_values

ORIGIN = (3, 3, 3)
CARDINAL = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
CORNERS = tuple(product((-1, 1), repeat=3))
INVERSES = {2: (1, 0), 6: (1, 0, 3, 2, 5, 4), 8: (7, 6, 5, 4, 3, 2, 1, 0)}
PERMUTATION = (0, 3, 6, 4, 7, 1, 5, 2)
PERMUTED_INVERSE = (4, 3, 5, 1, 0, 2, 7, 6)


def _field(name, components=1, *, conserved=True):
    return {
        "name": name,
        "components": components,
        "units": "configured unit",
        "signed": True,
        "conserved": conserved,
    }


def _local(name):
    return {"field": name, "side": "right"}


def _operation(name, *arguments):
    return {"op": name, "args": list(arguments)}


def _spatial_seed(name, value, position):
    zero = [0, 0, 0] if isinstance(value, list) else 0
    return {"position": list(position), "field": name, "populations": [value] + [zero] * 7}


def _base(degree=6, *, travel=1, shape=(8, 8, 8), permuted=False):
    offsets = CORNERS if degree == 8 else CARDINAL[:degree]
    if permuted:
        offsets = tuple(offsets[index] for index in PERMUTATION)
    fields = [_field("stock"), _field("vector", 3), _field("driver", conserved=False)]
    raw = {
        "schema_version": 1,
        "model_id": "node-input-output-contract-v1",
        "shape": list(shape),
        "boundary": "periodic",
        "slots_per_cell": 4,
        "link_ticks": travel,
        "normal_budget": 1000000,
        "ticks": 0,
        "operation_costs": dict.fromkeys(OPERATIONS, 1),
        "fields": fields,
        "disturbance_types": [{"name": "unused", "fields": ["stock"], "transport": {"mode": "hold"}}],
        "seeds": [],
        "spatial_fields": [{"field": item["name"], "transport": "local"} for item in fields],
        "spatial_seeds": [],
        "field_rules": [],
    }
    if degree != 6 or permuted:
        raw["topology"] = {"model_id": "configured-ports-v1", "offsets": [list(v) for v in offsets]}
    return raw, offsets


def _input_star(degree=6, *, travel=1, shape=(8, 8, 8), permuted=False):
    raw, offsets = _base(degree, travel=travel, shape=shape, permuted=permuted)
    sources, signatures = [], []
    for port, offset in enumerate(offsets):
        position = tuple(value - delta for value, delta in zip(ORIGIN, offset, strict=True))
        scalar = (-1) ** port * (port + 1)
        vector = [port + 1, -2 * (port + 1), (-1) ** port * (port + 2)]
        signatures.append((scalar, tuple(vector)))
        sources.append(position)
        raw["spatial_seeds"].extend(
            [
                _spatial_seed("stock", scalar, position),
                _spatial_seed("vector", vector, position),
                _spatial_seed("driver", port + 1, position),
            ]
        )
        raw["field_rules"].append(
            {
                "name": f"send_port_{port}",
                "when": _operation("eq", _local("driver"), port + 1),
                "assignments": [
                    {"field": "stock", "expression": 0},
                    {"field": "stock", "port": port, "expression": _local("stock")},
                    {"field": "vector", "expression": [0, 0, 0]},
                    {"field": "vector", "port": port, "expression": _local("vector")},
                    {"field": "driver", "expression": 0},
                ],
                "invariants": [
                    {
                        "name": name,
                        "expression": _operation("add", _local(name), {"outgoing": name, "port": port}),
                    }
                    for name in ("stock", "vector")
                ],
            }
        )
    return raw, tuple(sources), tuple(signatures)


def _sample(probe, position):
    return next(item for item in probe.sample() if item.snapshot.position == position)


def _expected_inventory(signatures):
    return {
        "stock": (sum(scalar for scalar, _ in signatures),),
        "vector": tuple(sum(vector[axis] for _, vector in signatures) for axis in range(3)),
    }


def _assert_payload(event, signature):
    scalar, vector = signature
    values = dict(event.values)
    assert values["stock"] == (scalar,)
    assert values["vector"] == vector


@pytest.mark.parametrize("degree", [2, 6, 8])
@pytest.mark.parametrize("travel", [1, 3])
def test_each_real_port_carries_a_distinct_signed_scalar_and_vector(degree, travel):
    raw, sources, signatures = _input_star(degree, travel=travel)
    with NodeProbe(parse_initial_state(raw), (ORIGIN, *sources)) as probe:
        events = []
        expected = _expected_inventory(signatures)
        for tick in range(1, travel + 1):
            transition = probe.step()
            assert (transition.start_tick, transition.end_tick) == (tick - 1, tick)
            assert transition.error_type is None
            events.extend(transition.events)
            assert probe.world.totals() == expected
            if tick < travel:
                assert probe.world.spatial_values(ORIGIN)["stock"]["value"] == (0,)
                assert not any(event.direction == "input" for event in events)
        outputs = {event.travel_port: event for event in events if event.direction == "output"}
        inputs = {event.travel_port: event for event in events if event.direction == "input"}
        assert set(outputs) == set(inputs) == set(range(degree))
        for port, source in enumerate(sources):
            sent, received = outputs[port], inputs[port]
            assert sent.kind == received.kind == "spatial"
            assert (sent.event, sent.event_port) == ("spatial_sent", port)
            assert (received.event, received.event_port) == ("spatial_received", None)
            assert (sent.position, sent.source, sent.target) == (source, source, ORIGIN)
            assert (received.position, received.source, received.target) == (ORIGIN, source, ORIGIN)
            assert (sent.port, sent.receiver_port) == (port, INVERSES[degree][port])
            assert received.port == received.receiver_port == INVERSES[degree][port]
            assert sent.audit_tick == 0 and sent.arrival_tick == travel
            assert received.audit_tick == travel
            _assert_payload(sent, signatures[port])
            _assert_payload(received, signatures[port])
            # Canonical probe sides do not rewrite the stored travel-index view.
            assert probe.world.spatial_values(ORIGIN)["stock"]["directions"][port] == (
                signatures[port][0],
            )
        assert probe.world.spatial_values(ORIGIN)["stock"]["value"] == expected["stock"]
        assert probe.world.spatial_values(ORIGIN)["vector"]["value"] == expected["vector"]
        # Input arrival is not a completed carrier cycle or field phase.
        assert _sample(probe, ORIGIN).clock == _sample(probe, ORIGIN).spatial_cycles == 0
        probe.step()
        assert _sample(probe, ORIGIN).clock == 0
        assert _sample(probe, ORIGIN).spatial_cycles == 1
        assert all(v == (0,) for v in probe.world.spatial_values(ORIGIN)["stock"]["directions"])


def test_permuted_eight_ports_use_declared_inverses_for_both_physical_payloads():
    raw, sources, signatures = _input_star(8, permuted=True)
    with NodeProbe(parse_initial_state(raw), (ORIGIN, *sources)) as probe:
        transition = probe.step()
        arrivals = [event for event in transition.events if event.direction == "input"]
        assert len(arrivals) == 8
        for event in arrivals:
            assert event.port == PERMUTED_INVERSE[event.travel_port]
            assert event.source == sources[event.travel_port]
            _assert_payload(event, signatures[event.travel_port])
    source = ORIGIN
    target = (2, 2, 2)
    carrier = carrier_document(
        [kind("parcel", mode="move", values={"inventory": -7}, weights=[1] + [0] * 7)],
        [(source, "parcel")],
    )
    carrier["shape"] = [8, 8, 8]
    carrier["topology"] = deepcopy(raw["topology"])
    with NodeProbe(parse_initial_state(carrier), (source, target)) as probe:
        events = probe.step().events
        arrival = next(event for event in events if event.direction == "input")
        assert arrival.kind == "carrier"
        assert (arrival.travel_port, arrival.port, arrival.receiver_port) == (0, 4, 4)
        assert (arrival.event, arrival.event_port) == ("received", 4)
        assert (arrival.source, arrival.target) == (source, target)
        assert dict(arrival.values) == {"inventory": (-7,)}


def _moving_carrier(*, travel=1, shape=(10, 3, 3), source=(2, 1, 1)):
    raw = carrier_document(
        [kind("parcel", mode="move", values={"inventory": 7}, weights=[1, 0, 0, 0, 0, 0])],
        [(source, "parcel")],
        travel=travel,
    )
    raw["shape"] = list(shape)
    return raw


def test_one_periodic_node_still_waits_for_its_real_return_link():
    position = (0, 0, 0)
    raw = _moving_carrier(travel=3, shape=(1, 1, 1), source=position)
    with NodeProbe(parse_initial_state(raw), (position,)) as probe:
        first = probe.step()
        assert len(first.events) == 1 and first.events[0].direction == "output"
        assert first.events[0].source == first.events[0].target == position
        assert _sample(probe, position).clock == 1
        assert resident_values(probe.world, position) == []
        assert not probe.step().events
        returned = probe.step()
        assert len(returned.events) == 1 and returned.events[0].direction == "input"
        assert returned.events[0].audit_tick == 3
        assert (returned.events[0].travel_port, returned.events[0].port) == (0, 1)
        assert _sample(probe, position).clock == 1
        assert resident_values(probe.world, position) == [{"inventory": (7,)}]


def test_three_nodes_cannot_relay_across_two_links_in_one_interval():
    positions = ((2, 1, 1), (3, 1, 1), (4, 1, 1))
    with NodeProbe(parse_initial_state(_moving_carrier(travel=3)), positions) as probe:
        arrivals = []
        for tick in range(1, 7):
            arrivals.extend(event for event in probe.step().events if event.direction == "input")
            assert probe.world.totals() == {"inventory": (7,)}
            if tick < 6:
                assert resident_values(probe.world, positions[2]) == []
        assert [(event.position, event.audit_tick) for event in arrivals] == [
            (positions[1], 3),
            (positions[2], 6),
        ]
        assert [_sample(probe, position).clock for position in positions] == [1, 1, 0]


def test_waiting_node_keeps_its_frozen_proposal_and_counts_only_completed_cycles():
    position = (2, 2, 2)
    update = {
        "field": "inventory",
        "source": True,
        "expression": {"op": "add", "args": [{"op": "add", "args": [{"field": "inventory"}, 1]}, 0]},
    }
    raw = carrier_document(
        [
            kind("busy", values={"inventory": 10}, updates=[update]),
            kind("incoming", mode="move", values={"inventory": 5}, weights=[1, 0, 0, 0, 0, 0]),
        ],
        [(position, "busy"), ((1, 2, 2), "incoming")],
        budget=4,
        capacity=2,
    )
    with NodeProbe(parse_initial_state(raw), (position,)) as probe:
        first = probe.step()
        assert _sample(probe, position).clock == 0
        assert resident_values(probe.world, position) == [{"inventory": (10,)}, {"inventory": (5,)}]
        assert [(event.direction, event.clock) for event in first.events] == [("input", 0)]
        probe.step()
        assert _sample(probe, position).clock == 1
        assert resident_values(probe.world, position) == [{"inventory": (11,)}, {"inventory": (5,)}]
        assert probe.world.source_totals() == {"inventory": (1,)}


def test_invalid_local_output_keeps_all_node_owners_and_captures_failure():
    raw, _ = _base()
    raw["spatial_seeds"] = [
        _spatial_seed("stock", 7, ORIGIN),
        _spatial_seed("vector", [3, -4, 0], ORIGIN),
    ]
    raw["field_rules"] = [
        {
            "name": "invalid_last_output",
            "assignments": [
                {"field": "vector", "expression": [0, 0, 0]},
                {"field": "vector", "port": 0, "expression": _local("vector")},
                {"field": "stock", "expression": 0},
                {"field": "stock", "port": 1, "expression": 8},
            ],
            "invariants": [
                {
                    "name": "vector",
                    "expression": _operation("add", _local("vector"), {"outgoing": "vector", "port": 0}),
                }
            ],
        }
    ]
    with NodeProbe(parse_initial_state(raw), (ORIGIN,)) as probe:
        before = probe.world.snapshot()
        with pytest.raises(ValueError) as error:
            probe.step()
        transition = probe.last_transition
        assert transition.error_type == type(error.value).__name__
        assert transition.error_message == str(error.value)
        assert (transition.start_tick, transition.end_tick) == (0, 0)
        assert transition.events == ()
        assert probe.world.snapshot() == before
        assert _sample(probe, ORIGIN).clock == _sample(probe, ORIGIN).spatial_cycles == 0
        assert probe.world.faulted


def test_identical_local_inputs_have_identical_outputs_in_different_world_sizes():
    small, sources, _ = _input_star(8, travel=3, shape=(8, 8, 8))
    large, _, _ = _input_star(8, travel=3, shape=(80, 80, 80))
    with NodeProbe(parse_initial_state(small), (ORIGIN, *sources)) as first:
        with NodeProbe(parse_initial_state(large), (ORIGIN, *sources)) as second:
            for _ in range(4):
                left, right = first.step(), second.step()
                assert left.events == right.events
                assert [(s.clock, s.spatial_cycles) for s in left.after] == [
                    (s.clock, s.spatial_cycles) for s in right.after
                ]
                for position in (ORIGIN, *sources):
                    assert first.world.spatial_values(position) == second.world.spatial_values(position)


def test_a_whole_multiport_input_batch_exceeding_capacity_is_not_partly_archived():
    raw, _, signatures = _input_star(2)
    with NodeProbe(parse_initial_state(raw), (ORIGIN,), max_events=1) as probe:
        with pytest.raises((ValueError, OverflowError)) as error:
            probe.step()
        transition = probe.last_transition
        assert transition.error_type == type(error.value).__name__
        assert transition.events == ()
        # Receipt already committed physically before the diagnostic callback.
        expected = _expected_inventory(signatures)
        assert probe.world.totals() == expected
        assert probe.world.spatial_values(ORIGIN)["stock"]["value"] == expected["stock"]
        assert probe.world.spatial_values(ORIGIN)["vector"]["value"] == expected["vector"]
        assert probe.world.faulted


def test_external_observer_failure_keeps_the_original_error_and_real_event_prefix():
    position = (0, 0, 0)
    raw = _moving_carrier(shape=(1, 1, 1), source=position)
    original = RuntimeError("requested observer failure")

    def fail_after_receipt(event):
        if event["event"] == "received":
            raise original

    with NodeProbe(parse_initial_state(raw), (position,), observer=fail_after_receipt) as probe:
        with pytest.raises(RuntimeError) as caught:
            probe.step()
        assert caught.value is original
        transition = probe.last_transition
        assert [event.direction for event in transition.events] == ["output", "input"]
        assert (transition.error_type, transition.error_message) == ("RuntimeError", str(original))
        assert resident_values(probe.world, position) == [{"inventory": (7,)}]
        assert _sample(probe, position).clock == 1


def test_observer_error_with_broken_message_preserves_the_original_exception():
    class UnprintableObserverError(RuntimeError):
        def __str__(self):
            raise AssertionError("observer error formatting failed")

    position = (0, 0, 0)
    raw = _moving_carrier(shape=(1, 1, 1), source=position)
    original = UnprintableObserverError()

    def fail_after_receipt(event):
        if event["event"] == "received":
            raise original

    with NodeProbe(parse_initial_state(raw), (position,), observer=fail_after_receipt) as probe:
        with pytest.raises(UnprintableObserverError) as caught:
            probe.step()
        assert caught.value is original
        transition = probe.last_transition
        assert transition.error_type == "UnprintableObserverError"
        assert transition.error_message == "Exception message unavailable"
        assert transition.snapshot_error_type is None
        assert [event.direction for event in transition.events] == ["output", "input"]
        assert resident_values(probe.world, position) == [{"inventory": (7,)}]


@pytest.mark.parametrize("observer_fails", [False, True])
def test_failed_post_step_capture_records_its_error_without_replacing_an_earlier_failure(
    monkeypatch, observer_fails
):
    position = (0, 0, 0)
    raw = _moving_carrier(shape=(1, 1, 1), source=position)
    observer_error = RuntimeError("original observer failure")
    capture_error = LookupError("post-step node capture failed")

    def observer(event):
        if observer_fails and event["event"] == "received":
            raise observer_error

    with NodeProbe(parse_initial_state(raw), (position,), observer=observer) as probe:
        sample = probe.sample
        calls = 0

        def capture():
            nonlocal calls
            calls += 1
            if calls == 2:
                raise capture_error
            return sample()

        monkeypatch.setattr(probe, "sample", capture)
        expected_error = observer_error if observer_fails else capture_error
        with pytest.raises(type(expected_error)) as caught:
            probe.step()
        assert caught.value is expected_error
        transition = probe.last_transition
        assert len(transition.before) == 1 and transition.after == ()
        assert [event.direction for event in transition.events] == ["output", "input"]
        assert (transition.snapshot_error_type, transition.snapshot_error_message) == (
            "LookupError",
            "post-step node capture failed",
        )
        if observer_fails:
            assert (transition.error_type, transition.error_message) == (
                "RuntimeError",
                "original observer failure",
            )
        else:
            assert transition.error_type is transition.error_message is None
            assert (transition.start_tick, transition.end_tick) == (0, 1)
        # A diagnostic capture failure does not undo the completed physical receipt.
        assert resident_values(probe.world, position) == [{"inventory": (7,)}]
        assert sample()[0].clock == 1


def test_probe_retains_only_the_latest_bounded_transition_and_detached_snapshots(monkeypatch):
    position = (0, 0, 0)
    raw = _moving_carrier(shape=(1, 1, 1), source=position)
    with NodeProbe(parse_initial_state(raw), (position,), max_events=2) as probe:
        initial_sample = _sample(probe, position)
        saved_sample = asdict(initial_sample)

        def whole_world_forbidden():
            pytest.fail("a selected node probe must not copy the whole world")

        monkeypatch.setattr(probe.world, "snapshot", whole_world_forbidden)
        first = probe.step()
        saved_first = asdict(first)
        with pytest.raises(FrozenInstanceError):
            first.start_tick = 99
        with pytest.raises(FrozenInstanceError):
            first.events[0].port = 4
        for tick in range(2, 33):
            latest = probe.step()
            assert probe.last_transition is latest
            assert (latest.start_tick, latest.end_tick) == (tick - 1, tick)
            assert len(latest.events) == 2
            assert _sample(probe, position).clock == tick
        assert asdict(initial_sample) == saved_sample
        assert asdict(first) == saved_first


def test_direct_world_steps_update_clocks_without_extending_the_saved_transition():
    position = (0, 0, 0)
    raw = _moving_carrier(shape=(1, 1, 1), source=position)
    with NodeProbe(parse_initial_state(raw), (position,), max_events=2) as probe:
        first = probe.step()
        probe.world.step()
        assert probe.last_transition is first
        assert _sample(probe, position).clock == 2
        following = probe.step()
        assert (following.start_tick, following.end_tick) == (2, 3)
        assert len(following.events) == 2
        assert _sample(probe, position).clock == 3


def test_node_selection_consumes_only_its_bounded_validation_prefix():
    consumed = 0

    def positions():
        nonlocal consumed
        while True:
            consumed += 1
            assert consumed <= 65, "probe consumed an unbounded node iterator"
            yield (2, 1, 1)

    with pytest.raises(ValueError):
        NodeProbe(parse_initial_state(_moving_carrier()), positions())
    assert consumed == 65


@pytest.mark.parametrize("capacity", [0, True, 65537])
def test_invalid_event_capacity_is_rejected(capacity):
    with pytest.raises(ValueError):
        NodeProbe(parse_initial_state(_moving_carrier()), ((2, 1, 1),), max_events=capacity)


@pytest.mark.parametrize("positions", [(), ((2, 1, 1), (2, 1, 1)), ((10, 1, 1),)])
def test_empty_duplicate_or_outside_node_selections_are_rejected(positions):
    with pytest.raises(ValueError):
        NodeProbe(parse_initial_state(_moving_carrier()), positions)
