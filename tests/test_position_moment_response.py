"""Wave observables and local reencoding do not manufacture global closure."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from event_universe.diagnostics.node_contract import node_state_violations
from examples.quantum.position_moment_response import configuration

ROOT = Path(__file__).resolve().parents[1]


def test_saved_wave_moment_experiment(tmp_path):
    output = tmp_path / "position-moments"
    process = subprocess.run(
        [sys.executable, "-m", "examples.quantum.run_position_moment_response", "--output", str(output)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    report = json.loads((output / "summary.json").read_text())
    assert report["numerical_checks"] == "pass"
    assert report["classical_limit"] == "not_derived"
    assert not report["closed_quantum_apparatus_energy_momentum"]
    assert report["diagnostics_leave_native_trace_and_cost_unchanged"]
    middle = report["middle_capture"]
    assert middle["capture"]["variance"] == 2
    assert middle["response"]["values"]["coarse_momentum"] == [3, 0, 0]
    assert [row["second_moment"] for row in middle["observed_combined_moment_changes"]] == [10, "11"]
    assert middle["wave_samples"][-1]["status"] == "vacuum"
    assert middle["wave_samples"][-1]["variance"] is None
    for case in report["six_axis_endpoint_controls"]:
        assert case["capture"]["variance"] == 1
        assert [row["second_moment"] for row in case["observed_combined_moment_changes"]] == [
            10,
            "11",
            "10",
        ]
        assert case["post_capture_ordinary_moments_balanced"]
        assert case["quantum_and_apparatus_closure"] == "not_established"
        axis, sign = case["axis"], case["sign"]
        assert [point["position"][axis] for point in case["path"]] == [
            3,
            3 + sign,
            3 + 2 * sign,
            3 + 3 * sign,
        ]
    assert report["no_reservoir"]["response"] is None
    assert report["computation_delay"]["pending_owned_samples"] > 0
    assert report["long_links"]["capture"]["audit_tick"] > middle["capture"]["audit_tick"]
    negative, real, positive = report["measurement_controls"]
    assert negative["before"]["mean_momentum"] == "-2"
    assert positive["before"]["mean_momentum"] == "2"
    assert real["before"]["second_moment"] == "0"
    for case in (negative, real, positive):
        click = case["outcomes"][1]
        assert click["probability"] == "1/4"
        assert click["moments"]["variance"] == "2"
        assert case["apparatus_exchange"] == "not_simulated"
    assert positive["nonselective_after"] == {"mean_momentum": "1", "second_moment": "3"}
    assert positive["ensemble_operation_change"]["second_moment"] == "-1"
    assert real["ensemble_operation_change"]["second_moment"] == "1"
    assert not list(output.rglob("*.html"))


@pytest.mark.parametrize(
    "first,second,invariant",
    [
        ([-3, 0, 0], [0, 0, 0], "total_first_moment"),
        ([6, 0, 0], [-3, 0, 0], "total_second_moment"),
    ],
)
def test_changed_moment_metadata_does_not_remove_local_balance_guards(first, second, invariant):
    raw = configuration(capture="middle")
    for assignment in raw["interactions"][0]["assignments"]:
        if assignment["field"] == "coarse_momentum":
            assignment["expression"] = first if assignment["side"] == "left" else second
    initial = prepare_initialization(raw).initial
    with Simulation(initial) as world:
        with pytest.raises(ValueError, match=f"invariant {invariant}"):
            for _ in range(310):
                world.step()
        owners = {
            initial.disturbances[record.type_index].name
            for node in world.nodes.values()
            for record in node.records
            if record is not None
        }
        assert "localized_charge" in owners and "arriving_reservoir" in owners
        assert "moving_output" not in owners


def test_reencoded_values_are_local_generic_data_with_bounded_owners():
    raw = configuration(capture="middle")
    names = [field["name"] for field in raw["fields"]]
    names.extend(kind["name"] for kind in raw["disturbance_types"])
    rename = {name: f"value_{index}" for index, name in enumerate(names)}

    def transform(value):
        if isinstance(value, str):
            return rename.get(value, value)
        if isinstance(value, list):
            return [transform(item) for item in value]
        if isinstance(value, dict):
            return {rename.get(key, key): transform(item) for key, item in value.items()}
        return value

    renamed = transform(raw)
    renamed["disturbance_types"].reverse()
    initial = prepare_initialization(renamed).initial
    with Simulation(initial) as world:
        for _ in range(310):
            world.step()
        outputs = {
            initial.disturbances[record.type_index].name: world.record_values(record)
            for node in world.nodes.values()
            for record in node.records
            if record is not None
        }
        assert outputs[rename["moving_output"]][rename["momentum_spread"]] == (0,)
        assert outputs[rename["stored_recoil"]][rename["momentum_spread"]] == (2,)
        assert all(not node_state_violations(node) for node in world._nodes.values())
