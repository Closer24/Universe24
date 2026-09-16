"""Output clocks preserve directional spatial Link ownership and delivery."""

import pytest

from event_universe import Simulation
from event_universe.core.output_holds import release_outputs, stage_outputs
from event_universe.core.spatial_state import SpatialPacket
from event_universe.initialization import parse_initial_state

from .test_output_clocks import clock_document

HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))


@pytest.mark.parametrize("ports", [(port,) for port in range(6)] + [(2, 3), tuple(range(6))])
@pytest.mark.parametrize("gain", [0, 1])
def test_spatial_output_clock_delivers_each_selected_face_without_repacking(ports, gain):
    # One token per selected direction, funded by one complete source pulse.
    raw = clock_document(mass=len(ports), gain=gain)
    raw["spatial_fields"][0].update(
        headings=[list(HEADINGS[port]) for port in ports], rays_per_tick=len(ports)
    )
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    origin = world.initial.seeds[0].position
    initial = world.totals()
    first_arrival = 1 + gain * len(ports)
    second_arrival = first_arrival + 1 + gain
    for _ in range(second_arrival):
        world.step()
        assert world.totals() == initial
        assert world.spatial_accounting()["energy"]["balanced"]

    for port in ports:
        heading = HEADINGS[port]
        for distance, arrival in ((1, first_arrival), (2, second_arrival)):
            target = tuple(origin[axis] + distance * heading[axis] for axis in range(3))
            assert [
                event["tick"]
                for event in events
                if event["event"] == "spatial_received" and event["position"] == target
            ] == [arrival]
    sent = [event for event in events if event["event"] == "spatial_sent"]
    assert {event["port"] for event in sent} == set(ports)
    assert all(event["arrival_tick"] == event["tick"] + 1 for event in sent)
    assert [(event["port"], event["tick"]) for event in sent if event["position"] == origin] == [
        (port, first_arrival - 1) for port in ports
    ]


def test_spatial_release_keeps_other_faces_held_or_in_flight():
    # Transport-only payloads isolate ownership from the field arithmetic.
    origin = (1, 1, 1)
    packet = SpatialPacket(1, origin, 0, ())
    existing = (packet, None, None, None, None, None)
    positive_y = SpatialPacket(1, origin, 2, ())
    negative_y = SpatialPacket(1, origin, 3, ())
    held, links = stage_outputs(
        (None,) * 6,
        existing,
        (None, None, positive_y, negative_y, None, None),
        0,
        (0, 0, 3, 1, 0, 0),
        1,
        port_indexed=True,
    )
    assert links == existing
    remaining, released = release_outputs(held, links, 1, port_indexed=True)
    assert remaining[2] is held[2]
    assert remaining[3] is None
    assert released[0] is packet
    assert released[1:3] == (None, None)
    assert released[3].port == 3 and released[3].arrival_tick == 2
    assert held[3] is not None and links == existing


def test_nonzero_face_overlap_rejects_before_source_debit():
    raw = clock_document(mass=2, reserve=4)
    raw["spatial_fields"][0]["headings"] = [[0, 0, -1]]
    raw["emissions"][0]["interval"] = 1
    world = Simulation(parse_initial_state(raw))
    world.step()
    before = world.inventory_view()
    with pytest.raises(ValueError, match="capacity collision"):
        world.step()
    assert world.inventory_view() == before
