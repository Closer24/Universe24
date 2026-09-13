"""Independent absorbing-boundary timing, signed accounting and ownership cases."""

from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import Packet, pack, unpack
from event_universe.core.spatial_state import SpatialPacket
from event_universe.initialization import parse_initial_state
from tests.test_finite_spatial_engine import all_records, finite_document
from tests.test_spatial_engine import document, field
from tests.test_zero_carrier import initialization


def face_position(port, shape=(5, 5, 5)):
    position = [extent // 2 for extent in shape]
    position[port // 2] = shape[port // 2] - 1 if port % 2 == 0 else 0
    return tuple(position)


def assert_balance(world, initial):
    current, lost, escaped = world.totals(), world.dissipation_totals(), world.escaped_totals()
    sources = world.source_totals()
    for name, values in initial.items():
        assert tuple(
            value + loss + exit_value
            for value, loss, exit_value in zip(current[name], lost[name], escaped[name], strict=True)
        ) == tuple(value + source for value, source in zip(values, sources[name], strict=True))
    assert all(item["balanced"] for item in world.spatial_accounting().values())


def carrier_document(port, *, amount=7, travel=3):
    raw = initialization(travel=travel)
    raw["boundary"] = "open"
    raw["shape"] = [5, 5, 5]
    raw["disturbance_types"][0]["defaults"] = {"stock": amount}
    raw["disturbance_types"][0]["transport"]["weights"] = [int(index == port) for index in range(6)]
    raw["seeds"][0]["position"] = list(face_position(port))
    return raw


@pytest.mark.parametrize("port", range(6))
@pytest.mark.parametrize("amount", [7, -7])
def test_carrier_exits_each_face_only_after_its_complete_link(port, amount):
    events = []
    world = Simulation(
        parse_initial_state(carrier_document(port, amount=amount)), observer=events.append
    )
    initial = world.totals()
    for tick in (1, 2):
        world.step()
        assert world.tick == tick
        assert world.totals()["stock"] == (amount,)
        assert world.escaped_totals()["stock"] == (0,)
        assert len(all_records(world)) == 1
        assert world.snapshot()["boundary"] == "open"
        assert world.snapshot()["transfers"][0]["target"] is None
        assert_balance(world, initial)
    world.step()
    assert world.totals()["stock"] == (0,)
    assert world.escaped_totals()["stock"] == (amount,)
    assert all_records(world) == []
    assert [event["tick"] for event in events if event["event"] == "escaped"] == [3]
    for _ in range(7):
        world.step()
        assert_balance(world, initial)
        assert all_records(world) == []
    assert all(all(0 <= value < 5 for value in position) for position in world.cells)


@pytest.mark.parametrize("boundary, remaining, escaped", [("open", 0, 24), ("periodic", 24, 0)])
def test_single_cell_domain_handles_all_six_spatial_faces(boundary, remaining, escaped):
    raw = document(travel=2)
    raw.update(boundary=boundary, shape=[1, 1, 1])
    raw["spatial_seeds"] = [{"position": [0, 0, 0], "field": "radiation", "populations": [3] * 8}]
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    world.step()
    packets = world.snapshot()["spatial_transfers"]
    assert len(packets) == 6
    assert {packet["port"] for packet in packets} == set(range(6))
    assert all(packet["target"] == (None if boundary == "open" else (0, 0, 0)) for packet in packets)
    assert world.totals()["radiation"] == (24,)
    assert world.escaped_totals()["radiation"] == (0,)
    world.step()
    assert world.totals()["radiation"] == (remaining,)
    assert world.escaped_totals()["radiation"] == (escaped,)
    assert set(world._spatial.cells) == {(0, 0, 0)}
    assert_balance(world, initial)


def vector_pulse(port, *, terminal=True):
    raw = finite_document(components=3, baseline=[0, 0, 0], travel=3)
    raw.update(boundary="open", shape=[5, 5, 5])
    raw["spatial_fields"][0]["axis_weights"] = [int(axis == port // 2) for axis in range(3)]
    populations = [[0, 0, 0] for _ in range(8)]
    octant = 0 if port % 2 == 0 else 1 << (2 - port // 2)
    populations[octant] = [-3, 1, 0]
    raw["spatial_seeds"] = [
        {
            "position": list(face_position(port) if terminal else (2, 2, 2)),
            "field": "radiation",
            "populations": populations,
        }
    ]
    return raw


@pytest.mark.parametrize("port", range(6))
def test_signed_vector_exit_is_raw_while_interior_control_decays(port):
    worlds = [
        Simulation(parse_initial_state(vector_pulse(port, terminal=value))) for value in (True, False)
    ]
    initial = worlds[0].totals()
    for world in worlds:
        for _ in range(2):
            world.step()
            assert world.totals()["radiation"] == (-3, 1, 0)
            assert world.escaped_totals()["radiation"] == (0, 0, 0)
            assert world.dissipation_totals()["radiation"] == (0, 0, 0)
        world.step()
        assert_balance(world, initial)
    terminal, interior = worlds
    assert terminal.totals()["radiation"] == (0, 0, 0)
    assert terminal.escaped_totals()["radiation"] == (-3, 1, 0)
    assert terminal.dissipation_totals()["radiation"] == (0, 0, 0)
    assert interior.totals()["radiation"] == (-1, 0, 0)
    assert interior.escaped_totals()["radiation"] == (0, 0, 0)
    assert interior.dissipation_totals()["radiation"] == (-2, 1, 0)


def mixed_fields():
    raw = finite_document(components=3, baseline=[0, 0, 0])
    raw.update(boundary="open", shape=[5, 5, 5])
    raw["fields"].append({**field("count"), "signed": False})
    raw["spatial_fields"][0]["axis_weights"] = [1, 1, 1]
    raw["spatial_fields"].append(
        {
            "field": "count",
            "baseline": 0,
            "transport": "outward",
            "decay": {"retain_numerator": 1, "retain_denominator": 2},
        }
    )
    return raw


def test_corner_partitions_signed_vector_and_unsigned_stock_between_inside_and_outside():
    raw = mixed_fields()
    raw["spatial_fields"][1]["baseline"] = 7
    raw["spatial_seeds"] = [
        {"position": [0, 0, 0], "field": "radiation", "populations": [[6, -3, 0]] * 8},
        {"position": [0, 0, 0], "field": "count", "populations": [6] * 8},
    ]
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    world.step()
    assert world.totals()["radiation"] == (12, 0, 0)
    assert world.escaped_totals()["radiation"] == (24, -12, 0)
    assert world.dissipation_totals()["radiation"] == (12, -12, 0)
    assert world.totals()["count"] == (7 * 125 + 12,)
    assert world.escaped_totals()["count"] == (24,)
    assert world.dissipation_totals()["count"] == (12,)
    assert set(world._spatial.cells) == {(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)}
    assert_balance(world, initial)


def test_invalid_unsigned_component_rejects_complete_multi_field_exit_atomically():
    world = Simulation(parse_initial_state(mixed_fields()))
    engine = world._spatial
    vector = (pack((-3, 1, 0)),) + (pack((0, 0, 0)),) * 7
    invalid = (pack((-1,)),) + (pack((0,)),) * 7
    packet = SpatialPacket(3, (0, 0, 0), 1, (vector, invalid))
    engine.links[(0, 0, 0)] = (None, packet, None, None, None, None)
    before = world.escaped_totals()
    with pytest.raises(ValueError, match="negative"):
        engine.deliver(3)
    assert engine.links[(0, 0, 0)][1] == packet
    assert world.escaped_totals() == before
    assert not any(any(values) for values in engine.dissipation)
    assert engine.cells == {}


def test_invalid_unsigned_carrier_cannot_escape_before_validation():
    raw = carrier_document(1)
    raw["fields"][0]["signed"] = False
    world = Simulation(parse_initial_state(raw))
    position = face_position(1)
    original = world.cells[position].records[0]
    packet = Packet(3, position, 1, replace(original, values=(pack((-1,)),)))
    world._nodes[position].records = (None,) * 2
    world._links[position] = (packet,) + (None,) * 11
    world.tick = 3
    with pytest.raises(ValueError, match="negative"):
        world._deliver()
    assert world._links[position][0] == packet
    assert world.escaped_totals()["stock"] == (0,)


def test_terminal_field_has_no_exterior_decay_receive_event_or_carried_cost():
    raw = finite_document(travel=3)
    raw.update(boundary="open", shape=[5, 5, 5])
    raw["spatial_fields"][0]["decay"]["retain_numerator"] = 0
    raw["spatial_seeds"] = [
        {
            "position": [4, 2, 2],
            "field": "radiation",
            "populations": [1, 0, 0, 0, 0, 0, 0, 0],
        }
    ]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for _ in range(3):
        world.step()
    assert world.escaped_totals()["radiation"] == (1,)
    assert world.dissipation_totals()["radiation"] == (0,)
    assert [event["tick"] for event in events if event["event"] == "spatial_escaped"] == [3]
    assert not any(event["event"] in ("spatial_received", "spatial_decayed") for event in events)
    assert set(world._spatial.cells) == {(4, 2, 2)}
    assert world._spatial.cells[(4, 2, 2)].received_decay_cost == 0
    world.step()
    assert world._spatial.cells[(4, 2, 2)].last_cost == 0


def test_exiting_emitter_removes_unused_allowance_without_reemission():
    raw = finite_document(source=True, moving=True, travel=3)
    raw.update(boundary="open", shape=[5, 5, 5])
    raw["disturbance_types"][0]["defaults"]["strength"] = 2
    raw["seeds"][0]["position"] = [4, 2, 2]
    world = Simulation(parse_initial_state(raw))
    initial = world.totals()
    world.step()
    record = all_records(world)[0]
    assert unpack(record.emission_remaining[0]) == (3,)
    assert world.source_totals()["radiation"] == (2,)
    for _ in range(11):
        world.step()
        assert_balance(world, initial)
    assert all_records(world) == []
    assert world.source_totals()["radiation"] == (2,)
    assert world.escaped_totals()["radiation"] == (2,)
    assert world.escaped_totals()["strength"] == (2,)
    assert world.dissipation_totals()["radiation"] == (0,)
