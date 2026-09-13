"""Permanent ownership and lifetime checks for passive node inspection."""

import gc
import weakref

import pytest

from event_universe import Simulation
from event_universe.diagnostics.node_probe import MAX_ERROR_MESSAGE, NodeProbe, NodeTransition
from event_universe.initialization import parse_initial_state

from .test_local_field_rules import ORIGIN, document, field, seed
from .test_node_integration import high_port_configuration
from .test_topology_invariants import configure


class PointOnly(dict):
    """Permit local lookup while making accidental whole-world reads fail."""

    def __iter__(self):
        raise AssertionError("point lookup traversed the world")

    def keys(self):
        raise AssertionError("point lookup enumerated addresses")

    def values(self):
        raise AssertionError("point lookup enumerated owners")

    def items(self):
        raise AssertionError("point lookup copied the world")


def maximum_width_world():
    raw = configure(document([field("stock", conserved=True)], [seed("stock", 7)]), "cubic")
    raw.pop("slots_per_cell")
    raw["slots_per_node"] = 32
    raw["seeds"] = [
        {"position": list(ORIGIN), "type": "held", "values": {"stock": index + 1}} for index in range(32)
    ]
    return Simulation(parse_initial_state(raw))


def test_point_views_never_materialize_or_iterate_unrelated_nodes(monkeypatch):
    world = maximum_width_world()
    world._nodes = PointOnly(world._nodes)
    world._links = PointOnly(world._links)
    world._spatial.nodes = PointOnly(world._spatial.nodes)
    world._spatial.links = PointOnly(world._spatial.links)

    def materialize(*arguments):
        raise AssertionError("passive lookup materialized physical state")

    monkeypatch.setattr(world, "_at", materialize)
    monkeypatch.setattr(world._spatial, "_at", materialize)
    occupied = world.node_view(ORIGIN)
    for coordinate in range(8):
        missing = world.node_view((coordinate, 7, 6))
        assert missing.carrier is None and missing.spatial is None
    assert len(world._nodes) == len(world._spatial.nodes) == 1
    assert len(world._links) == len(world._spatial.links) == 0
    assert occupied.carrier.records is world._nodes[ORIGIN].records
    assert occupied.spatial.states is world._spatial.nodes[ORIGIN].states


def test_maximum_width_views_share_immutable_payloads_and_empty_port_defaults():
    world = maximum_width_world()
    first = world.node_view(ORIGIN)
    second = world.node_view(ORIGIN)
    empty = world.node_view((7, 7, 7))
    assert len(first.carrier.records) == 32
    assert len(first.outgoing) == 26 * 32
    assert len(first.spatial_outgoing) == 26
    assert len(first.spatial.states[0].delivered) == 26
    assert first.carrier.records is second.carrier.records
    assert first.carrier.coupling_remainders is second.carrier.coupling_remainders
    assert first.spatial.states is second.spatial.states
    assert first.outgoing is second.outgoing is empty.outgoing
    assert first.spatial_outgoing is second.spatial_outgoing is empty.spatial_outgoing
    with pytest.raises(TypeError):
        first.carrier.records[0] = None
    with pytest.raises(TypeError):
        first.spatial.states[0].delivered[25] = (1,)
    assert world.node_view(ORIGIN) == first


def test_live_packet_view_reuses_the_real_packet_owner():
    raw = high_port_configuration()
    del raw["conservation"]
    world = Simulation(parse_initial_state(raw))
    world.step()
    view = world.node_view((4, 4, 4))
    owned = world.links[(4, 4, 4)]
    assert view.outgoing is owned
    packet = next(packet for packet in view.outgoing if packet is not None)
    assert packet.port == 25 and packet.arrival_tick == 2
    world.step()
    assert packet in view.outgoing
    assert all(packet is None for packet in world.node_view((4, 4, 4)).outgoing)
    arrived = world.node_view((0, 0, 0)).carrier.records
    assert [world.record_values(item)["inventory"] for item in arrived if item is not None] == [(4,)]


def transition_count():
    return sum(type(item) is NodeTransition for item in gc.get_objects())


def test_released_steps_retain_one_transition_instead_of_run_history():
    raw = high_port_configuration()
    del raw["conservation"]
    probe = NodeProbe(parse_initial_state(raw), [(4, 4, 4)], max_events=8)
    gc.collect()
    baseline = transition_count()
    for _ in range(80):
        probe.step()
    gc.collect()
    assert transition_count() == baseline + 1
    assert probe.last_transition.end_tick == 80
    assert probe._events == []
    assert len(probe._clocks) == len(probe._spatial_cycles) == 1
    probe.close()


def test_failure_discards_callback_frames_and_closes_resources_once(monkeypatch):
    class Payload:
        pass

    class ObserverFailure(Exception):
        pass

    references = []

    def fail(event):
        payload = Payload()
        references.append(weakref.ref(payload))
        raise ObserverFailure("x" * (MAX_ERROR_MESSAGE + 100))

    raw = high_port_configuration()
    del raw["conservation"]
    probe = NodeProbe(parse_initial_state(raw), [(4, 4, 4)], observer=fail)
    closed = []
    monkeypatch.setattr(probe.world, "close", lambda: closed.append(True), raising=False)
    try:
        probe.step()
    except ObserverFailure:
        pass
    else:
        pytest.fail("the observer failure must propagate")
    gc.collect()
    assert references and all(reference() is None for reference in references)
    assert probe._events == []
    assert probe.last_transition.error_type == "ObserverFailure"
    assert len(probe.last_transition.error_message) <= MAX_ERROR_MESSAGE
    probe.close()
    probe.close()
    assert closed == [True]
