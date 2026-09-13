"""Combined topology, property selection and passive observation contracts."""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization, validate_configuration
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_local_conservation import configuration as audit_configuration
from .test_local_field_rules import ORIGIN, document, field, invariant, local, operation, seed, value
from .test_property_couplings import complex_identity, record_values
from .test_spatial_interactions import exchange
from .test_topology_invariants import configure, topology


def high_port_configuration():
    """An unchanged packet crosses the last cubic port with two ticks in transit."""
    raw = audit_configuration()
    raw["topology"] = topology("cubic")
    raw["seeds"][0]["position"] = [4, 4, 4]
    raw["disturbance_types"][0]["transport"] = {"mode": "move", "weights": [0] * 25 + [1], "rate": 1}
    return raw


def test_property_selected_second_layout_responds_to_real_port_25_arrival():
    raw = configure(
        document([field("quantity", conserved=True)], [seed("quantity", 2, (1, 1, 1))]), "cubic"
    )
    raw["fields"].append(field("extra"))
    raw["disturbance_types"] = [
        {
            "name": "first",
            "fields": ["quantity"],
            "defaults": {"quantity": 5},
            "transport": {"mode": "hold"},
        },
        {
            "name": "second",
            "fields": ["quantity", "extra"],
            "defaults": {"quantity": 5, "extra": 9},
            "transport": {"mode": "hold"},
        },
    ]
    raw["seeds"] = [
        {"position": [5, 5, 5], "type": "first"},
        {"position": list(ORIGIN), "type": "second"},
    ]
    received = {"received": "quantity", "port": 25}
    raw["field_rules"] = [
        {
            "name": "send_without_reforwarding_new_input",
            "when": operation("eq", received, 0),
            "assignments": [
                {"field": "quantity", "expression": 0},
                {"field": "quantity", "port": 25, "expression": local("quantity")},
            ],
            "invariants": [
                invariant(
                    "stock", operation("add", local("quantity"), {"outgoing": "quantity", "port": 25})
                )
            ],
        }
    ]
    raw["spatial_interactions"] = [
        {
            "name": "take_delivered_stock",
            "requires": ["quantity"],
            "when": operation("gt", received, 0),
            "assignments": [
                {
                    "side": "left",
                    "field": "quantity",
                    "expression": operation("add", {"field": "quantity"}, received),
                },
                {
                    "side": "right",
                    "field": "quantity",
                    "expression": operation("sub", local("quantity"), received),
                },
            ],
            "invariants": [
                invariant("joint_stock", operation("add", {"field": "quantity"}, local("quantity")))
            ],
        }
    ]
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    world.step()
    assert value(world, "quantity") == (2,)
    assert record_values(world)[0]["quantity"] == (5,)
    world.step()
    assert record_values(world)[0] == {"quantity": (7,), "extra": (9,)}
    assert record_values(world, (5, 5, 5))[0]["quantity"] == (5,)
    assert value(world, "quantity") == (0,)
    assert world.totals()["quantity"] == (12,)
    assert any(event["event"] == "spatial_sent" and event["port"] == 25 for event in events)
    reception = next(event for event in events if event["event"] == "spatial_received")
    assert reception["position"] == ORIGIN
    assert reception["received_fields"][0]["quantity"] == (2,)


@pytest.mark.parametrize("stage", ["joint", "field"])
def test_passive_guard_complexity_preserves_26_port_cost_and_delayed_commit(stage):
    raw = configure(exchange(), "cubic")
    raw["normal_budget"] = 10
    if stage == "field":
        raw["field_rules"] = [
            {
                "name": "retain",
                "assignments": [{"field": "quantity", "expression": local("quantity")}],
                "invariants": [invariant("stock", local("quantity"))],
            }
        ]
    changed = deepcopy(raw)
    collection = "spatial_interactions" if stage == "joint" else "field_rules"
    check = changed[collection][0]["invariants"][0]
    check["expression"] = complex_identity(check["expression"])
    worlds = [Simulation(parse_initial_state(item)) for item in (raw, changed)]
    for world in worlds:
        world.step()
    pending = [world.nodes[ORIGIN].pending for world in worlds]
    assert all(item is not None and item.ready_tick > 1 for item in pending)
    assert pending[0].plan.cost == pending[1].plan.cost
    assert pending[0].ready_tick == pending[1].ready_tick
    while worlds[0].tick < pending[0].ready_tick:
        for world in worlds:
            world.step()
    assert record_values(worlds[0]) == record_values(worlds[1])
    assert record_values(worlds[0])[0]["quantity"] == (2,)
    assert worlds[0].computation_report() == worlds[1].computation_report()


@pytest.mark.parametrize("lane", ["carrier", "spatial"])
@pytest.mark.parametrize("boundary", ["periodic", "open"])
def test_high_port_passive_audit_matches_unaudited_transit_and_escape(lane, boundary):
    raw = high_port_configuration()
    raw["boundary"] = boundary
    if lane == "spatial":
        raw["seeds"] = []
        raw["spatial_fields"] = [{"field": "inventory", "baseline": 0, "transport": "local"}]
        raw["spatial_seeds"] = [seed("inventory", 4, (4, 4, 4))]
        raw["conservation"]["spatial"] = {"energy": local("inventory"), "momentum": [0, 0, 0]}
        raw["field_rules"] = [
            {
                "name": "forward",
                "assignments": [
                    {"field": "inventory", "expression": 0},
                    {"field": "inventory", "port": 25, "expression": local("inventory")},
                ],
                "invariants": [
                    invariant(
                        "stock",
                        operation("add", local("inventory"), {"outgoing": "inventory", "port": 25}),
                    )
                ],
            }
        ]
    control = deepcopy(raw)
    del control["conservation"]
    traces = [[], []]
    worlds = [
        Simulation(parse_initial_state(item), observer=events.append)
        for item, events in zip((raw, control), traces, strict=True)
    ]
    for _ in range(4):
        for world in worlds:
            world.step()
        assert worlds[0].snapshot() == worlds[1].snapshot()
        assert worlds[0].computation_report() == worlds[1].computation_report()
        report = worlds[0].conservation_report()
        assert report["status"] == "passed"
        assert report["current"]["energy"] + report["escaped"]["energy"] == 4
    assert traces[0] == traces[1]
    assert report["escaped"]["energy"] == (4 if boundary == "open" else 0)
    sent_name = "sent" if lane == "carrier" else "spatial_sent"
    assert any(event["event"] == sent_name and event["port"] == 25 for event in traces[0])
    event_name = (
        ("escaped" if lane == "carrier" else "spatial_escaped")
        if boundary == "open"
        else ("received" if lane == "carrier" else "spatial_received")
    )
    assert any(event["event"] == event_name and event["tick"] == 2 for event in traces[0])


@pytest.mark.parametrize("external", [False, True])
def test_excluded_bcc_observer_rejects_before_runner_outputs(tmp_path, external):
    raw = configure(document([field("stock")]), "bcc")
    observer = {"position": [0, 0, 1], "max_receipts": 8}
    if not external:
        raw["observer"] = observer
    source = tmp_path / "initial.json"
    source.write_text(json.dumps(raw), encoding="utf-8")
    sidecar = tmp_path / "observer.json"
    sidecar.write_text(json.dumps(observer), encoding="utf-8")
    output = tmp_path / "run"
    arguments = {"observer_document": observer} if external else {}
    with pytest.raises(ValueError, match="not a site"):
        prepare_initialization(raw, **arguments)
    report = (
        validate_configuration(
            json.dumps(observer), kind="observer", initialization_source=json.dumps(raw)
        )
        if external
        else validate_configuration(json.dumps(raw))
    )
    assert not report.valid
    with pytest.raises(ValueError, match="not a site"):
        run_initialization(source, output, observer=sidecar if external else None)
    assert not output.exists()
