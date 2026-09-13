"""Independent local balance expectations across complete physical owner changes."""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import validate_configuration
from event_universe.core.disturbance_state import OPERATIONS
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization


def reference(name, side="left"):
    return {"field": name, "side": side}


def operation(name, *arguments):
    return {"op": name, "args": list(arguments)}


def configuration(boundary="periodic"):
    return {
        "schema_version": 1,
        "model_id": "local-conservation-test-v1",
        "shape": [5, 5, 5],
        "slots_per_cell": 2,
        "link_ticks": 2,
        "normal_budget": 10000,
        "ticks": 12,
        "boundary": boundary,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            {
                "name": "inventory",
                "components": 1,
                "units": "energy unit",
                "signed": False,
                "conserved": False,
            },
            {
                "name": "impulse",
                "components": 3,
                "units": "momentum unit",
                "signed": True,
                "conserved": False,
            },
        ],
        "disturbance_types": [
            {
                "name": "carrier",
                "fields": ["inventory", "impulse"],
                "defaults": {"inventory": 4, "impulse": [1, 0, 0]},
                "transport": {"mode": "move", "direction_field": "impulse", "rate": 1},
            }
        ],
        "seeds": [{"position": [4, 2, 2], "type": "carrier"}],
        "conservation": {
            "name": "explicit additive inventories",
            "energy_units": "energy unit",
            "momentum_units": "momentum unit",
            "carriers": [
                {
                    "requires": ["inventory", "impulse"],
                    "energy": reference("inventory"),
                    "momentum": reference("impulse"),
                }
            ],
        },
    }


@pytest.mark.parametrize("boundary", ["periodic", "open"])
def test_carrier_inventory_is_counted_once_through_wait_transit_and_boundary(boundary):
    raw = configuration(boundary)
    raw["normal_budget"] = 10
    world = Simulation(parse_initial_state(raw))
    for _ in range(40):
        world.step()
        report = world.conservation_report()
        assert report["status"] == "passed"
        assert report["current"]["energy"] + report["escaped"]["energy"] == 4
        assert tuple(
            a + b
            for a, b in zip(report["current"]["momentum"], report["escaped"]["momentum"], strict=True)
        ) == (1, 0, 0)
    assert report["checked_node_events"] > 0
    assert report["escaped"]["energy"] == (4 if boundary == "open" else 0)


def test_unconfigured_audit_is_explicit_and_passive_reads_do_not_change_state():
    raw = configuration()
    without = deepcopy(raw)
    del without["conservation"]
    events, control_events = [], []
    audited = Simulation(parse_initial_state(raw), observer=events.append)
    control = Simulation(parse_initial_state(without), observer=control_events.append)
    assert control.conservation_report() == {"status": "not_configured"}
    for _ in range(10):
        audited.step()
        control.step()
        before = audited.snapshot()
        audited.conservation_report()
        audited.inventory_view()
        assert audited.snapshot() == before == control.snapshot()
    assert events == control_events


def test_later_update_is_measured_after_commit_without_repair(tmp_path):
    raw = configuration()
    raw["disturbance_types"][0]["transport"] = {"mode": "hold"}
    raw["disturbance_types"][0]["updates"] = [{"field": "inventory", "expression": 0}]
    assert validate_configuration(json.dumps(raw)).valid
    world = Simulation(parse_initial_state(raw))
    with pytest.raises(ValueError, match="local energy/momentum"):
        world.step()
    assert world.faulted
    failure = world.conservation_report()["failure"]
    assert failure["event"] == "cycle_committed"
    assert failure["residual"] == {"energy": -4, "momentum": (0, 0, 0)}
    assert world.conservation_report()["current"]["energy"] == 0
    assert world.snapshot()["cells"][0]["disturbances"][0]["values"]["inventory"] == (0,)
    path = tmp_path / "input.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError, match="local energy/momentum"):
        run_initialization(path, tmp_path / "result", ticks=1)
    saved = json.loads((tmp_path / "result/run.json").read_text())
    assert saved["status"] == "failed"
    assert saved["local_conservation"]["status"] == "failed"


@pytest.mark.parametrize("axis", range(3))
def test_each_momentum_component_is_checked_independently(axis):
    raw = configuration()
    changed = [1, 0, 0]
    changed[axis] += 1
    raw["disturbance_types"][0]["transport"] = {"mode": "hold"}
    raw["disturbance_types"][0]["updates"] = [{"field": "impulse", "expression": changed}]
    world = Simulation(parse_initial_state(raw))
    with pytest.raises(ValueError, match="local energy/momentum"):
        world.step()
    expected = [0, 0, 0]
    expected[axis] = 1
    assert world.conservation_report()["failure"]["residual"] == {
        "energy": 0,
        "momentum": tuple(expected),
    }


def converging_packets():
    raw = configuration()
    raw["seeds"] = []
    raw["fields"].append(
        {
            "name": "amplitude",
            "components": 3,
            "units": "amplitude unit",
            "signed": True,
            "conserved": True,
        }
    )
    raw["spatial_fields"] = [{"field": "amplitude", "baseline": [0, 0, 0], "transport": "local"}]
    raw["spatial_seeds"] = [
        {"position": [x, 2, 2], "field": "amplitude", "populations": [[0, sign, 0]] + [[0, 0, 0]] * 7}
        for x, sign in ((1, 1), (3, -1))
    ]
    amplitude = reference("amplitude", "right")
    norm = operation("dot", amplitude, amplitude)
    raw["conservation"]["spatial"] = {"energy": norm, "momentum": [0, 0, 0]}
    raw["field_rules"] = []
    for port, sign in ((0, 1), (1, -1)):
        outgoing = {"outgoing": "amplitude", "port": port}
        component = {"op": "component", "args": [amplitude], "index": 1}
        raw["field_rules"].append(
            {
                "name": f"route_{port}",
                "when": operation("gt", operation("mul", sign, component), 0),
                "assignments": [
                    {"field": "amplitude", "expression": [0, 0, 0]},
                    {"field": "amplitude", "port": port, "expression": amplitude},
                ],
                "invariants": [
                    {
                        "name": "local norm",
                        "expression": operation("add", norm, operation("dot", outgoing, outgoing)),
                    }
                ],
            }
        )
    return raw


def test_arrival_merge_is_checked_before_a_later_rule_can_hide_lost_norm():
    world = Simulation(parse_initial_state(converging_packets()))
    world.step()
    assert world.conservation_report()["current"]["energy"] == 2
    with pytest.raises(ValueError, match="local energy/momentum"):
        world.step()
    failure = world.conservation_report()["failure"]
    assert failure["event"] == "spatial_received"
    assert failure["incoming"]["energy"] == 2
    assert failure["residual"]["energy"] == -2
    assert world.spatial_values((2, 2, 2))["amplitude"]["value"] == (0, 0, 0)


@pytest.mark.parametrize(
    "failure", ["missing", "overlap", "unknown", "foreign_side", "shape", "source", "spatial_missing"]
)
def test_preflight_rejects_incomplete_or_unsupported_measurement_contract(failure):
    raw = configuration()
    measurement = raw["conservation"]["carriers"][0]
    if failure == "missing":
        raw["conservation"]["carriers"] = []
    elif failure == "overlap":
        raw["conservation"]["carriers"].append(deepcopy(measurement))
    elif failure == "unknown":
        measurement["requires"].append("missing")
    elif failure == "foreign_side":
        measurement["energy"] = reference("inventory", "right")
    elif failure == "shape":
        measurement["momentum"] = 0
    elif failure == "source":
        raw["disturbance_types"][0]["updates"] = [
            {"field": "inventory", "expression": 5, "source": True}
        ]
    else:
        raw["spatial_fields"] = [{"field": "inventory", "baseline": 0}]
    assert not validate_configuration(json.dumps(raw)).valid


def test_empty_packet_cannot_supply_undeclared_energy():
    raw = converging_packets()
    raw["conservation"]["spatial"]["energy"] = 1
    assert not validate_configuration(json.dumps(raw)).valid
    with pytest.raises(ValueError, match="empty spatial inventory"):
        Simulation(parse_initial_state(raw))


def test_diagnostic_expression_pricing_cannot_overflow_the_physical_cost():
    raw = configuration()
    raw["disturbance_types"][0]["transport"] = {"mode": "hold"}
    raw["operation_costs"]["evaluate"] = 1_073_741_823
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.conservation_report()["status"] == "passed"


def test_failed_external_observer_cannot_skip_the_committed_state_audit():
    raw = configuration()
    raw["disturbance_types"][0]["transport"] = {"mode": "hold"}
    raw["disturbance_types"][0]["updates"] = [{"field": "inventory", "expression": 0}]

    def broken_output(event):
        if event["event"] == "cycle_committed":
            raise RuntimeError("output failed")

    world = Simulation(parse_initial_state(raw), observer=broken_output)
    with pytest.raises(RuntimeError, match="output failed"):
        world.step()
    assert world.faulted
    assert world.conservation_report()["status"] == "failed"
    assert world.conservation_report()["current"]["energy"] == 0
