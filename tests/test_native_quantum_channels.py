"""Quantum channel effects drive native trajectories; references remain separate."""

import json
from pathlib import Path

import pytest

from event_universe.reference_api import ReferenceSimulation as Simulation
from event_universe.reference_api import parse_reference_state as parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
H = [[1, 1], [1, -1]]
POSITION = [[[1, 0], [0, 0]], [[0, 0], [0, 1]]]


def config(middle=None):
    raw = json.loads((ROOT / "examples/quantum/native_classical.json").read_text())
    p = raw["event_program"]
    p.update(
        model="local-quantum-events-v2",
        addresses=[[6, 2, 1]],
        occupied=[],
        dimensions=[2],
        initial_levels=[0],
        register_names=["path"],
    )
    p["layers"] = [
        {"tick": 1, "operations": [{"sites": [0], "matrix": H}]},
        {"tick": 3, "operations": [{"sites": [0], "matrix": H}]},
    ]
    if middle:
        p["layers"].insert(1, {"tick": 2, "operations": [dict(sites=[0], **middle)]})
    p["bindings"][0]["instrument"] = POSITION
    p["tickets"] = [0]
    return raw


def run(raw):
    trace = []
    world = Simulation(parse_initial_state(raw), observer=trace.append)
    for _ in range(raw["ticks"]):
        world.step()
        assert world.totals()["mass"] == (2,)
        assert world.totals()["momentum"] == (0, 0, 0)
    return world, trace


@pytest.mark.parametrize(
    "middle,weights",
    [
        (None, (1, 0)),
        ({"matrix": [[1, 0], [0, -1]]}, (0, 1)),
        ({"channel": POSITION}, (1, 1)),
        ({"channel": [[[3, 0], [0, 3]], [[4, 0], [0, 0]], [[0, 0], [0, 4]]]}, (17, 8)),
    ],
)
def test_native_interference_counts_and_priced_paths(middle, weights):
    raw = config(middle)
    counts = [0, 0]
    for ticket in range(sum(weights)):
        raw["event_program"]["tickets"] = [ticket]
        world, trace = run(raw)
        r = world.computation_report()
        q = r["resolver"]
        rec = q["records"][0]
        assert rec["decision"]["weights"] == weights
        counts[rec["outcome"]] += 1
        assert q["random_draws"] == int(all(weights))
        assert q["oracle_calls"] == 1 and q["oracle_direct_world_ticks"] == 0
        assert r["model_operations_cost"] == r["event_ledger_cost"] == (135 if rec["outcome"] else 116)
        sends = [e for e in trace if e["event"] == "sent" and e["tick"] == 4]
        assert len(sends) == 2
        assert {e["disturbance"]: e["port"] for e in sends} == (
            {"Body A": 1, "Body B": 0} if rec["outcome"] else {"Body A": 0, "Body B": 1}
        )
    assert counts == list(weights)


def test_native_grouped_result_does_not_sample_unobserved_terms():
    raw = config()
    p = raw["event_program"]
    p["layers"] = p["layers"][:1]
    binding = p["bindings"][0]
    binding.pop("instrument")
    binding["grouped_instrument"] = [POSITION]
    binding["codes"] = [1]
    p["tickets"] = []
    world, _ = run(raw)
    q = world.computation_report()["resolver"]
    assert q["random_draws"] == 0 and len(q["records"]) == 1
    assert q["records"][0]["decision"]["weights"] == (2,)


@pytest.mark.parametrize("error", ["v1", "badmap", "ambiguous", "support", "unknown", "remote"])
def test_native_validation_rejects_ambiguous_or_invalid_extensions(error):
    raw = config()
    p = raw["event_program"]
    if error == "v1":
        p["model"] = "local-quantum-events-v1"
    if error == "badmap":
        p["layers"][0]["operations"][0] = {"sites": [0], "channel": [[[1, 1], [0, 1]]]}
    if error == "ambiguous":
        p["addresses"] *= 2
        p["dimensions"] *= 2
        p["initial_levels"] *= 2
        p["register_names"] = ["a", "b"]
    if error == "support":
        p["dimensions"] = [3]
    if error == "unknown":
        p["layers"][0]["operations"][0]["unrecognized"] = 1
    if error == "remote":
        p["bindings"][0]["site"] = 1
    with pytest.raises((ValueError, TypeError)):
        Simulation(parse_initial_state(raw))


def test_explicit_colocated_binding_and_local_gate_avoid_artificial_link_delay():
    raw = config()
    raw["link_ticks"] = 3
    raw["ticks"] = 2
    p = raw["event_program"]
    p["addresses"] *= 2
    p["dimensions"] *= 2
    p["initial_levels"] *= 2
    p["register_names"] = ["a", "b"]
    p["bindings"][0]["site"] = 0
    p["layers"] = [
        {
            "tick": 1,
            "operations": [
                {"sites": [0, 1], "matrix": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]]}
            ],
        }
    ]
    world, _ = run(raw)
    assert world.tick == 2


def test_saved_experiment_cli_and_headless_outputs(tmp_path):
    import subprocess
    import sys

    output = tmp_path / "quantum-physics"
    completed = subprocess.run(
        [sys.executable, str(ROOT / "examples/quantum/run_physics_checks.py"), "--output", str(output)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    report = json.loads((output / "summary.json").read_text())
    assert report["status"] == "pass"
    assert report["bell"]["chsh"] == "14/5"
    assert len(report["native"]) == 6
    assert not list(output.rglob("*.html"))
    assert all((output / row["name"] / "causal-events.jsonl").stat().st_size for row in report["native"])
