"""Measure interference loss without changing the simulator's physical laws.

The independent target is V(n) = (9/25)**n for the existing partial-dephasing
channel. Two analyzer phases measure the extrema; native moving carriers read
the register at their configured collision. Their motion is an input law.
"""

import argparse
import json
import platform
import time
from fractions import Fraction
from pathlib import Path

from environment_coherence_check import run_environment_controls
from run_physics_checks import markov_experiment
from trajectory_support_check import run_trajectory_controls

from event_universe.configuration_validation import prepare_initialization
from event_universe.retention import ArtifactLease, validate_output_path
from event_universe.runner import run_initialization, source_fingerprint

HERE = Path(__file__).resolve().parent


def configuration(encounters, phase_pi=False):
    """Author a fixed-clock control using the existing interference input."""
    if type(encounters) is not int or not 0 <= encounters <= 4:
        raise ValueError("the bounded experiment supports zero through four encounters")
    raw = json.loads((HERE / "interference.json").read_text(encoding="utf-8"))
    partial = json.loads((HERE / "partial_dephasing.json").read_text(encoding="utf-8"))
    channel = partial["event_program"]["layers"][1]["operations"][0]
    raw.update(model_id="quantum-classical-dephasing-control-v2", shape=[21, 5, 3], ticks=12)
    raw["seeds"][1]["position"] = [18, 2, 1]
    program = raw["event_program"]
    program["addresses"] = [[10, 2, 1]]
    program["bindings"][0]["address"] = [10, 2, 1]
    layers = [program["layers"][0]]
    for index in range(4):
        operation = (
            channel if index < encounters else {"register_indices": [0], "matrix": [[1, 0], [0, 1]]}
        )
        layers.append({"tick": index + 2, "operations": [operation]})
    layers.append(
        {
            "tick": 6,
            "operations": [
                {
                    "register_indices": [0],
                    "matrix": [[1, -1], [1, 1]] if phase_pi else [[1, 1], [1, -1]],
                }
            ],
        }
    )
    program["layers"] = layers
    # Keep the existing seed; exact pre-selection weights are the measurement.
    # No prescribed tickets or outcome-frequency fit is used.
    return raw


def run_experiment(output):
    """Run ten native worlds and keep the acceptance result separate from claims."""
    output = Path(output).resolve()
    validate_output_path(output)
    if output.exists() and any(output.iterdir()):
        raise ValueError("use a new or empty output directory")
    output.mkdir(parents=True, exist_ok=True)
    configurations = {
        f"n{count}-phase{int(phase)}": configuration(count, phase)
        for count in range(5)
        for phase in (False, True)
    }
    for raw in configurations.values():
        prepare_initialization(raw)
    inputs = {name: output / (name + ".json") for name in configurations}
    summary = output / "summary.json"
    owned = [*inputs.values(), summary]
    for path in owned:
        path.touch()
    before = source_fingerprint()
    started = time.perf_counter()
    with ArtifactLease(output, owned):
        measured = []
        for count in range(5):
            phases = []
            expected_visibility = Fraction(9, 25) ** count
            for phase in (False, True):
                name = f"n{count}-phase{int(phase)}"
                inputs[name].write_text(json.dumps(configurations[name], indent=2) + "\n")
                run_initialization(inputs[name], output / name)
                meta = json.loads((output / name / "run.json").read_text())
                resolver = meta["computation"]["resolver"]
                records = resolver["records"]
                assert len(records) == 1
                record = records[0]
                weights = record["decision"]["weights"]
                probability = Fraction(weights[0], sum(weights))
                expected = (1 + (-1 if phase else 1) * expected_visibility) / 2
                assert probability == expected
                assert meta["status"] == "completed" and meta["completed_ticks"] == 12
                assert meta["accounting_balanced_at_every_completed_tick"]
                assert meta["conserved_at_every_completed_tick"]
                assert (
                    meta["initial_totals"]
                    == meta["final_totals"]
                    == {"mass": [2], "momentum": [0, 0, 0]}
                )
                assert meta["display"] == "none" and meta["source_sha256"] == before
                assert record["decision"]["tick"] == 8
                assert resolver["oracle_direct_world_ticks"] == 0
                cost = meta["computation"]["model_operations_cost"]
                assert cost == meta["computation"]["event_ledger_cost"] and cost > 0
                phases.append(
                    {
                        "phase_pi": phase,
                        "probability_zero": str(probability),
                        "expected": str(expected),
                        "outcome": record["outcome"],
                        "contact_tick": record["decision"]["tick"],
                        "cost": meta["computation"]["model_operations_cost"],
                        "random_draws": resolver["random_draws"],
                        "elapsed_seconds": meta["elapsed_seconds"],
                        "run": name,
                    }
                )
            visibility = Fraction(phases[0]["probability_zero"]) - Fraction(
                phases[1]["probability_zero"]
            )
            assert visibility == expected_visibility
            measured.append(
                {
                    "encounters": count,
                    "visibility": str(visibility),
                    "visibility_percent": float(100 * visibility),
                    "phases": phases,
                }
            )
        environment = run_environment_controls()
        classical_probabilities = markov_experiment()
        trajectories = run_trajectory_controls()
        assert source_fingerprint() == before
        result = {
            "numerical_checks": "pass",
            "quantum_to_classical_trajectory_claim": "not_established",
            "source_sha256": before,
            "python": platform.python_version(),
            "elapsed_seconds": time.perf_counter() - started,
            "native_runs": 10,
            "dephasing": measured,
            "environment": environment,
            "classical_probabilities": classical_probabilities,
            "trajectory_controls": trajectories,
            "limits": [
                "Environment is a supplied channel on an internal register, not simulated photon scattering.",
                "Probabilities are exact pre-selection weights, not measured ensemble frequencies.",
                "Classical mass, momentum, movement and collision exchange are supplied in the input.",
                "No spatial wavepacket-to-Newtonian-trajectory limit is tested by this profile.",
                "Mass and net momentum accounting pass; environment energy is not represented.",
                "The configured quantum owner uses the explicit Q-ORACLE-1 exception.",
            ],
        }
        summary.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = run_experiment(args.output)
    print(
        json.dumps(
            {
                key: result[key]
                for key in (
                    "numerical_checks",
                    "quantum_to_classical_trajectory_claim",
                    "native_runs",
                    "elapsed_seconds",
                )
            }
        )
    )


if __name__ == "__main__":
    main()
