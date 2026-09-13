"""Reject invalid local proposals and foreign provenance before ownership changes."""

from dataclasses import FrozenInstanceError, replace

import pytest

from event_universe.core.disturbance_state import Departure, pack
from event_universe.core.event_resolution import LocalContext
from event_universe.disturbance_api import Simulation
from event_universe.initialization import load_initial_state, parse_initial_state

from .architecture_rules import violations
from .test_disturbance_engine import document, kind
from .test_node_probe import ORIGIN, _base, _spatial_seed


def world():
    return Simulation(
        parse_initial_state(
            document(
                [kind("parcel", mode="move", weights=[1, 0, 0, 0, 0, 0])],
                [((2, 2, 2), "parcel")],
                capacity=2,
            )
        )
    )


@pytest.mark.parametrize(
    "defect",
    [
        "negative_slot",
        "boolean_slot",
        "duplicate_slot",
        "foreign_slot",
        "foreign_port",
        "boolean_port",
        "mutable_outputs",
        "mutable_payload",
        "foreign_object",
        "missing_fields",
        "negative_origin",
        "mutable_residuals",
        "negative_cost",
    ],
)
def test_bad_planner_output_never_enters_pending_or_link_state(defect):
    simulation = world()
    original = simulation._services.planner
    record = simulation.node_view((2, 2, 2)).carrier.records[0]

    def broken(records, residuals, received):
        plan = original(records, residuals, received)
        changes = {
            "negative_slot": {"replacements": ((-1, record),)},
            "boolean_slot": {"replacements": ((True, record),)},
            "duplicate_slot": {"replacements": ((0, None), (0, record))},
            "foreign_slot": {"replacements": ((2, record),)},
            "foreign_port": {"departures": (Departure(6, record),)},
            "boolean_port": {"departures": (Departure(True, record),)},
            "mutable_outputs": {"departures": list(plan.departures)},
            "mutable_payload": {"replacements": ((0, replace(record, values=([3],))),)},
            "foreign_object": {"replacements": ((0, replace(record, values=simulation)),)},
            "missing_fields": {"source_delta": ((0,), (0,))},
            "negative_origin": {"departures": (Departure(0, record, -2),)},
            "mutable_residuals": {"coupling_remainders": []},
            "negative_cost": {"cost": -1},
        }
        return replace(plan, **changes[defect])

    simulation._services = replace(simulation._services, planner=broken)
    before = simulation.snapshot()
    with pytest.raises(ValueError, match="node I/O"):
        simulation.step()
    assert simulation.snapshot() == before
    assert simulation.node_view((2, 2, 2)).carrier.pending is None
    assert simulation.faulted


def test_local_planner_cannot_mutate_inputs_or_read_world_through_them():
    simulation = world()
    original = simulation._services.planner
    calls = []

    def inspecting(records, residuals, received):
        for name in ("nodes", "_nodes", "links", "event_space", "graph", "snapshot"):
            with pytest.raises(AttributeError):
                getattr(records, name)
        with pytest.raises(TypeError):
            records[0] = None
        with pytest.raises(FrozenInstanceError):
            records[0].values = ()
        with pytest.raises(TypeError):
            records[0].values[0][0] = 99
        calls.append(received)
        return original(records, residuals, received)

    simulation._services = replace(simulation._services, planner=inspecting)
    simulation.step()
    assert calls == [0]
    assert simulation.totals() == {"inventory": (1,)}


def test_quantum_request_context_exposes_no_world_or_graph_reference():
    context = LocalContext(0, (0, 0, 0), (), (), 0, None)
    for name in ("world", "nodes", "graph", "event_space", "resolver"):
        with pytest.raises(AttributeError):
            getattr(context, name)
    with pytest.raises(FrozenInstanceError):
        context.address = (9, 9, 9)


@pytest.mark.parametrize("member", ["_nodes", "_links", "event_space", "_event_network", "snapshot"])
@pytest.mark.parametrize("layer", ["fields", "dynamics", "models"])
def test_repository_gate_rejects_hidden_world_and_graph_access(member, layer):
    assert violations(f"def update(source):\n    return source.{member}", f"event_universe.{layer}.law")


def test_carrier_rejects_packet_owned_by_a_different_origin():
    simulation = world()
    simulation._nodes[(2, 2, 2)].advance(0, simulation._services)
    links = list(simulation._links[(2, 2, 2)])
    links[0] = replace(links[0], origin=(9, 9, 9))
    simulation._links[(2, 2, 2)] = tuple(links)
    simulation.tick = 1
    before = simulation.snapshot()
    with pytest.raises(ValueError, match="origin differs"):
        simulation._deliver()
    assert simulation.snapshot() == before


@pytest.mark.parametrize("defect", ["locked_slot", "mutable_records"])
def test_receive_policy_cannot_overwrite_pending_inputs_or_retain_mutable_state(defect):
    simulation = Simulation(
        parse_initial_state(
            document(
                [kind("parcel", mode="move", weights=[1, 0, 0, 0, 0, 0])],
                [((1, 2, 2), "parcel"), ((2, 2, 2), "parcel")],
                capacity=2,
            )
        )
    )
    simulation._nodes[(1, 2, 2)].advance(0, simulation._services)
    planner = simulation._services.planner

    def waiting(records, residuals, received):
        return replace(planner(records, residuals, received), cost=simulation.initial.normal_budget + 1)

    simulation._nodes[(2, 2, 2)].advance(0, replace(simulation._services, planner=waiting))
    original = simulation._services.record_policy

    class BrokenReceiver:
        def receive(self, residents, arrivals, locked):
            proposed = list(original.receive(residents, arrivals, locked))
            if defect == "mutable_records":
                return proposed
            assert locked == frozenset({0})
            proposed[0] = replace(proposed[0], values=(pack((99,)),))
            return tuple(proposed)

    simulation._services = replace(simulation._services, record_policy=BrokenReceiver())
    simulation.tick = 1
    before = simulation.snapshot()
    with pytest.raises(ValueError):
        simulation._deliver()
    assert simulation.snapshot() == before


@pytest.mark.parametrize("change", [{"origin": (6, 6, 6)}, {"port": 1}])
def test_spatial_receiver_rejects_foreign_origin_or_mismatched_port(change):
    raw, _ = _base()
    for definition in raw["spatial_fields"]:
        definition["transport"] = "outward"
    raw["spatial_seeds"] = [_spatial_seed("stock", 70, ORIGIN)]
    simulation = Simulation(parse_initial_state(raw))
    spatial = simulation._spatial
    spatial.begin(0, {})
    packets = list(spatial.links[ORIGIN])
    assert packets[0] is not None
    packets[0] = replace(packets[0], **change)
    spatial.links[ORIGIN] = tuple(packets)
    before = simulation.snapshot()
    with pytest.raises(ValueError, match="provenance"):
        spatial.deliver(simulation.initial.link_ticks)
    assert simulation.snapshot() == before


@pytest.mark.parametrize(
    "module",
    ["spatial_engine", "event_space", "disturbance_node", "spatial_node", "node_services", "node_ports"],
)
def test_models_cannot_import_world_or_graph_owners(module):
    assert violations(f"from event_universe.core.{module} import Owner", "event_universe.models.law")


def test_incomplete_phase_shape_is_rejected_at_the_record_boundary():
    from event_universe.core.node_boundary import validate_record

    simulation = world()
    record = simulation.initial.seeds[0].record
    with pytest.raises(ValueError, match="configured size"):
        validate_record(simulation.initial, replace(record, phase_codes=()))


@pytest.mark.parametrize("method", ["sample", "sample_fluxes", "deposit", "forward_reaction"])
def test_mutable_coupling_output_cannot_enter_node_state(method):
    from .test_spatial_coupling import ORIGIN as position
    from .test_spatial_coupling import document as coupling_document

    raw = coupling_document()
    raw["spatial_seeds"] = [
        {"position": list(position), "field": "inventory", "populations": [[0, 0, 0]] * 8}
    ]
    simulation = Simulation(parse_initial_state(raw))
    spatial = simulation._spatial
    original = spatial.services.coupler

    class BrokenCoupler:
        def __getattr__(self, name):
            function = getattr(original, name)
            if name != method:
                return function

            def broken(*args):
                result = function(*args)
                if name in ("sample", "sample_fluxes"):
                    return list(result)
                return (list(result[0]), *result[1:])

            return broken

    spatial.services = replace(spatial.services, coupler=BrokenCoupler())
    before = simulation.node_view(position)
    with pytest.raises(ValueError, match="node I/O"):
        if method in ("sample", "sample_fluxes"):
            simulation.step()
        else:
            node = spatial.nodes[position]
            node.last_begin_tick = 0 if method == "forward_reaction" else -1
            before = simulation.node_view(position)
            node.prepare_reaction(0, ((1, 0, 0), (0, 0, 0), (0,)), spatial.services)
    assert simulation.node_view(position) == before


def test_mutable_decay_output_cannot_enter_receiving_node():
    from .test_finite_spatial_engine import finite_document

    simulation = Simulation(parse_initial_state(finite_document(source=True)))
    spatial = simulation._spatial
    spatial.begin(0, simulation._nodes)
    original = spatial.services.decayer

    def broken(bundle):
        fields, losses, cost = original(bundle)
        return list(fields), losses, cost

    spatial.services = replace(spatial.services, decayer=broken)
    packets = dict(spatial.links)
    with pytest.raises(ValueError, match="node I/O"):
        spatial.deliver(simulation.initial.link_ticks)
    assert spatial.links == packets
    assert all(node.received_count == 0 for node in spatial.nodes.values())


@pytest.mark.parametrize(
    "defect", ["mutable_states", "wrong_ports", "mutable_payload", "wrong_records", "missing_delta"]
)
def test_spatial_output_is_validated_before_commit(defect):
    raw, _ = _base()
    raw["spatial_seeds"] = [_spatial_seed("stock", 7, ORIGIN)]
    simulation = Simulation(parse_initial_state(raw))
    spatial = simulation._spatial
    original = spatial.services.planner

    def broken(states, records, received):
        plan = original(states, records, received)
        changes = {
            "mutable_states": {"states": list(plan.states)},
            "wrong_ports": {"outgoing": plan.outgoing[:-1]},
            "mutable_payload": {"source_delta": ([0],) * len(simulation.initial.fields)},
            "wrong_records": {"emission_records": (None,)},
            "missing_delta": {"source_delta": ()},
        }
        return replace(plan, **changes[defect])

    spatial.services = replace(spatial.services, planner=broken)
    before = simulation.snapshot()
    with pytest.raises(ValueError, match="node I/O"):
        simulation.step()
    assert simulation.snapshot() == before


def test_changed_remote_state_cannot_affect_a_local_update_without_delivery():
    local = document([kind("parcel")], [((2, 2, 2), "parcel")], capacity=2)
    remote = document([kind("parcel")], [((2, 2, 2), "parcel"), ((30, 30, 30), "parcel")], capacity=2)
    first, second = Simulation(parse_initial_state(local)), Simulation(parse_initial_state(remote))
    for _ in range(4):
        first.step()
        second.step()
        assert first.node_view((2, 2, 2)) == second.node_view((2, 2, 2))


def test_real_relay_keeps_the_existing_local_costs_and_link_delays():
    from pathlib import Path

    initial = load_initial_state(Path(__file__).parents[1] / "examples/node-clock/three_nodes.json")
    simulation = Simulation(initial)
    for _ in range(9):
        simulation.step()
    records = simulation.node_view((3, 0, 0)).carrier.records
    assert [r.values for r in records if r is not None] == [(pack((7,)),)]
    assert simulation.totals() == {"inventory": (7,)}
