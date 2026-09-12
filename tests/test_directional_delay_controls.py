"""Local three-vector controls produce six waits without remote reads or rewrites."""

from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from tests.test_directional_delay import ORIGIN, pair_document, wave_document


def control_document():
    raw = pair_document()
    raw["fields"].append(
        {
            "name": "local_delay_control",
            "components": 3,
            "units": "extra wait multiplier",
            "signed": False,
            "conserved": True,
            "extensive": True,
        }
    )
    raw["spatial_fields"] = [
        {"field": "local_delay_control", "baseline": [0, 0, 0], "transport": "local"}
    ]
    raw["spatial_seeds"] = [
        {
            "position": list(ORIGIN),
            "field": "local_delay_control",
            "populations": [[2, 4, 6], *[[0, 0, 0] for _ in range(7)]],
        }
    ]
    raw["directional_delay"] = {"weights": 1, "positive_field": "local_delay_control"}
    return raw


def test_local_vectors_are_sampled_and_priced_before_the_pending_schedule_is_frozen():
    raw = control_document()
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    field_cost = next(e["cost"] for e in events if e["event"] == "spatial_cycle")
    event = next(e for e in events if e["event"] == "cycle_started")
    assert event["cost"] == 7 + field_cost + 1  # One additional distinct control read.
    base = (event["cost"] + 3) // 4 - 1
    assert event["release_ticks"] == (3 * base, base, 5 * base, base, 7 * base, base)
    assert event["ready_tick"] == base
    assert event["next_tick"] == 3 * base + 1


def test_one_vector_can_control_both_signs_of_each_axis_with_one_priced_read():
    raw = control_document()
    raw["directional_delay"]["negative_field"] = "local_delay_control"
    world = Simulation(parse_initial_state(raw))
    assert world._spatial.delay_weights(ORIGIN, 0) == (3, 3, 5, 5, 7, 7)
    assert world._spatial.delay_read_cost() == 1


def test_control_reaches_the_node_causally_and_cannot_retime_a_frozen_cycle():
    raw = control_document()
    raw["normal_budget"] = 1
    raw["spatial_seeds"][0]["position"] = [0, 2, 2]
    raw["field_rules"] = [
        {
            "name": "forward_control",
            "assignments": [
                {"field": "local_delay_control", "expression": [0, 0, 0]},
                {
                    "field": "local_delay_control",
                    "port": 0,
                    "expression": {"field": "local_delay_control", "side": "right"},
                },
            ],
            "invariants": [
                {
                    "name": "stock",
                    "expression": {
                        "op": "add",
                        "args": [
                            {"field": "local_delay_control", "side": "right"},
                            {"outgoing": "local_delay_control", "port": 0},
                        ],
                    },
                }
            ],
        }
    ]
    world = Simulation(parse_initial_state(raw))
    assert world._spatial.delay_weights(ORIGIN, 0) == (1,) * 6
    world.step()
    pending = world.cells[ORIGIN].pending
    assert pending.ready_tick == 7
    assert world._spatial.delay_weights(ORIGIN, 1) == (1,) * 6
    world.step()
    assert world._spatial.delay_weights(ORIGIN, 2) == (3, 1, 5, 1, 7, 1)
    assert world.cells[ORIGIN].pending == pending


def test_spatial_outputs_use_the_same_local_control_before_forwarding():
    raw = wave_document()
    controls = control_document()
    raw["fields"].append(controls["fields"][-1])
    raw["spatial_fields"].extend(controls["spatial_fields"])
    raw["spatial_seeds"].extend(controls["spatial_seeds"])
    raw["directional_delay"] = {**controls["directional_delay"], "spatial_mode": "cost"}
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    cost = next(e["cost"] for e in events if e["event"] == "spatial_cycle")
    raw["normal_budget"] = cost - 1
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert [
        (p["port"], p["departure_tick"], p["arrival_tick"])
        for p in world.snapshot()["spatial_transfers"]
    ] == [(0, 3, 4), (2, 5, 6)]


@pytest.mark.parametrize(
    "mutator",
    [
        lambda r: r["directional_delay"].update(positive_field="missing"),
        lambda r: r["directional_delay"].update(positive_field="inventory"),
        lambda r: r["directional_delay"].update(positive_field=None),
        lambda r: r["fields"][-1].update(signed=True),
    ],
)
def test_delay_controls_must_be_declared_unsigned_spatial_vectors(mutator):
    raw = control_document()
    mutator(raw)
    with pytest.raises(ValueError, match="directional delay|positive_field"):
        parse_initial_state(raw)


def test_control_labels_have_no_engine_semantics():
    raw = control_document()
    renamed = deepcopy(raw)
    renamed["fields"][-1]["name"] = "arbitrary_control"
    renamed["spatial_fields"][0]["field"] = "arbitrary_control"
    renamed["spatial_seeds"][0]["field"] = "arbitrary_control"
    renamed["directional_delay"]["positive_field"] = "arbitrary_control"
    first, second = [Simulation(parse_initial_state(value)) for value in (raw, renamed)]
    for _ in range(3):
        first.step()
        second.step()
        assert first.cells == second.cells
        assert first.links == second.links
