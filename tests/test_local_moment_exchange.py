"""A local response transfers uncertainty rather than replacing it with zero."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.configuration_validation import prepare_initialization
from examples.quantum.local_moment_exchange import configuration

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    "field,value,check",
    [
        ("mass", 2, "candidate_mass_scope"),
        ("momentum_spread", 1, "momentum_validity_matches_spread"),
    ],
)
def test_candidate_rejects_unsupported_mass_and_false_certainty(field, value, check):
    raw = configuration()
    reservoir = next(kind for kind in raw["disturbance_types"] if kind["name"] == "arriving_reservoir")
    reservoir["defaults"][field] = value
    with pytest.raises(ValueError, match=check):
        with Simulation(prepare_initialization(raw).initial) as world:
            world.step()


def test_local_response_saved_experiment_and_quantum_control(tmp_path):
    output = tmp_path / "local-response"
    process = subprocess.run(
        [
            sys.executable,
            str(ROOT / "examples/quantum/run_local_moment_exchange.py"),
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert process.returncode == 0, process.stderr
    report = json.loads((output / "summary.json").read_text())
    assert report["numerical_checks"] == "pass" and report["classical_limit"] == "not_derived"
    assert len(report["six_axis_controls"]) == 6
    for row in report["six_axis_controls"]:
        assert row["mean_momentum_and_second_moment_balanced_every_tick"]
        assert row["expected_doubled_kinetic_energy_including_escape"] == 10
        positions = [entry["position"][row["axis"]] for entry in row["path"]]
        assert positions == [3, 3 + row["sign"], 3 + 2 * row["sign"], 3 + 3 * row["sign"]]
    assert report["no_reservoir"]["first_exchange"] is None
    assert report["computation_delay"]["delayed_owned_samples"] > 0
    assert (
        report["long_links"]["first_exchange"]["audit_tick"]
        > report["six_axis_controls"][1]["first_exchange"]["audit_tick"]
    )
    quantum = report["quantum_state_exchange"]
    assert quantum["equal_weight_case"]["after"]["total_momentum_distribution"] == {
        "2": "1/2",
        "4": "1/2",
    }
    assert len(quantum["basis_cases"]) == 16
    assert not list(output.rglob("*.html"))


def test_unbalanced_local_response_fails_before_conversion():
    raw = configuration()
    # Preserve the linear mean sum while violating the independently defined
    # quadratic energy. An inventory-only check must not accept this proposal.
    for assignment in raw["interactions"][0]["assignments"]:
        if assignment["field"] == "coarse_momentum":
            assignment["expression"] = [6, 0, 0] if assignment["side"] == "left" else [-3, 0, 0]
    initial = prepare_initialization(raw).initial
    with Simulation(initial) as world:
        with pytest.raises(ValueError, match="invariant total_second_moment"):
            for _ in range(raw["ticks"]):
                world.step()
        names = [
            initial.disturbances[record.type_index].name
            for node in world.nodes.values()
            for record in node.records
            if record is not None
        ]
        assert "localized_charge" in names and "arriving_reservoir" in names
        assert "moving_output" not in names and "stored_recoil" not in names
        assert world.totals()["coarse_momentum"] == (3, 0, 0)
        assert world.totals()["momentum_spread"] == (1,)


def test_response_remains_a_generic_configuration_with_renamed_payloads():
    raw = configuration()
    mapping = {
        name: f"field_{index}" for index, name in enumerate([field["name"] for field in raw["fields"]])
    }
    mapping.update(
        {kind["name"]: f"record_{index}" for index, kind in enumerate(raw["disturbance_types"])}
    )

    def rename(value):
        if isinstance(value, str):
            return mapping.get(value, value)
        if isinstance(value, list):
            return [rename(item) for item in value]
        if isinstance(value, dict):
            return {mapping.get(key, key): rename(item) for key, item in value.items()}
        return value

    renamed = rename(raw)
    renamed["disturbance_types"].reverse()
    initial = prepare_initialization(renamed).initial
    with Simulation(initial) as world:
        for _ in range(410):
            world.step()
        types = [
            initial.disturbances[record.type_index].name
            for node in world.nodes.values()
            for record in node.records
            if record is not None
        ]
        assert mapping["moving_output"] in types
        assert mapping["stored_recoil"] in types
        assert world.totals()[mapping["coarse_momentum"]] == (3, 0, 0)
