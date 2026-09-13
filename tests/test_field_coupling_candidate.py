"""Local field transfer changes the next route with exact owned inventories."""

import importlib
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.initialization import parse_initial_state

candidate = importlib.import_module("examples.coarse-graining.coupling")


def resident(snapshot, position):
    node = next(row for row in snapshot["nodes"] if tuple(row["position"]) == position)
    assert len(node["disturbances"]) == 1
    return node["disturbances"][0]["values"]


@pytest.mark.parametrize("link_ticks", [1, 2, 3])
def test_local_transfer_updates_energy_momentum_internal_state_and_next_port(link_ticks):
    report = candidate.run_configuration(candidate.build_configuration(link_ticks=link_ticks))
    sends = [event for event in report["events"] if event["event"] == "sent"]
    assert [(event["tick"], event["port"]) for event in sends[:2]] == [(0, 0), (link_ticks, 2)]
    before = resident(report["snapshots"][link_ticks], (3, 2, 1))
    after = resident(report["snapshots"][2 * link_ticks], (3, 3, 1))
    assert before == {"energy": (3,), "momentum": (1, 0, 0), "coupling": (1,), "internal": (0,)}
    assert after == {"energy": (4,), "momentum": (0, 1, 0), "coupling": (1,), "internal": (1,)}
    reactions = [
        event["reaction"]
        for event in report["events"]
        if event["event"] == "spatial_coupled" and event["reaction"]
    ]
    assert reactions == [{"energy": (-1,), "momentum": (1, -1, 0)}]
    audit = report["conservation"]
    assert audit["status"] == "passed" and audit["checked_node_events"] > 0
    assert audit["initial"] == audit["current"] == {"energy": 7, "momentum": (0, 1, 0)}
    assert all(row["balanced"] for row in report["spatial_accounting"].values())


@pytest.mark.parametrize(
    "coupling,energy,momentum,internal,port",
    [(0, 3, (1, 0, 0), 0, 0), (-1, 2, (2, -1, 0), 1, 0)],
)
def test_response_is_selected_by_owned_coupling_with_neutral_and_opposite_controls(
    coupling, energy, momentum, internal, port
):
    report = candidate.run_configuration(candidate.build_configuration(coupling))
    departure = next(
        event
        for event in report["events"]
        if event["event"] == "sent" and tuple(event["position"]) == candidate.RESERVOIR
    )
    assert departure["port"] == port
    assert departure["values"]["energy"] == (energy,)
    assert departure["values"]["momentum"] == momentum
    assert departure["values"]["internal"] == (internal,)
    assert report["conservation"]["status"] == "passed"
    assert report["conservation"]["current"] == {"energy": 7, "momentum": (0, 1, 0)}


def test_remote_reservoir_cannot_change_route_before_causal_arrival():
    raw = candidate.build_configuration()
    for seed in raw["spatial_seeds"]:
        seed["position"] = [3, 4, 1]
    report = candidate.run_configuration(raw)
    assert {event["port"] for event in report["events"] if event["event"] == "sent"} == {0}
    assert not any(
        event["reaction"] for event in report["events"] if event["event"] == "spatial_coupled"
    )


def test_local_delay_keeps_original_owners_until_joint_commit_and_then_full_link_transit():
    raw = candidate.build_configuration(normal_budget=100)
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    seen_pending = False
    for _ in range(24):
        world.step()
        node = world.nodes.get(candidate.RESERVOIR)
        if node is not None and node.pending is not None:
            seen_pending = True
            values = [world.record_values(r) for r in node.records if r is not None]
            assert values[0]["energy"] == (3,) and values[0]["momentum"] == (1, 0, 0)
            assert world.spatial_values(candidate.RESERVOIR)["energy"]["value"] == (4,)
        assert world.conservation_report()["status"] == "passed"
        assert all(not node_state_violations(n) for n in world.nodes.values())
    assert seen_pending
    starts = [event for event in events if event["event"] == "cycle_started"]
    assert [(event["tick"], event["ready_tick"]) for event in starts[:2]] == [(0, 6), (7, 15)]
    sends = [event for event in events if event["event"] == "sent"]
    assert [(event["tick"], event["arrival_tick"], event["port"]) for event in sends[:2]] == [
        (6, 7, 0),
        (15, 16, 2),
    ]


def rename_input(value, names):
    if isinstance(value, list):
        return [rename_input(item, names) for item in value]
    if not isinstance(value, dict):
        return value
    result = {}
    for key, item in value.items():
        if key in ("name", "field", "direction_field", "type") and isinstance(item, str):
            result[key] = names.get(item, item)
        elif key in ("requires", "fields") and isinstance(item, list):
            result[key] = [
                names.get(v, v) if isinstance(v, str) else rename_input(v, names) for v in item
            ]
        elif key in ("values", "defaults"):
            result[key] = {names.get(k, k): v for k, v in item.items()}
        else:
            result[key] = rename_input(item, names)
    return result


def normalize_output(value, names):
    if isinstance(value, dict):
        return {names.get(key, key): normalize_output(item, names) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return tuple(normalize_output(item, names) for item in value)
    return names.get(value, value) if isinstance(value, str) else value


def test_renaming_and_field_declaration_order_preserve_active_states_events_and_costs():
    raw = candidate.build_configuration()
    names = {"energy": "quantity_a", "momentum": "quantity_b", "coupling": "gain", "carrier": "photon"}
    renamed = rename_input(deepcopy(raw), names)
    renamed["fields"].reverse()
    first = candidate.run_configuration(raw)
    second = candidate.run_configuration(renamed)
    inverse = {value: key for key, value in names.items()}
    for key in ("snapshots", "events", "computation", "spatial_accounting"):
        assert normalize_output(first[key], {}) == normalize_output(second[key], inverse)
    assert second["conservation"]["status"] == "passed"


def test_invalid_coupling_is_rejected_before_a_world_runs():
    with pytest.raises(ValueError):
        parse_initial_state(candidate.build_configuration(True))
