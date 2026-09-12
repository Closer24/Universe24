"""Independent acceptance boundaries and real configuration-only attraction checks."""

import importlib.util
from pathlib import Path

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "star_cluster_audit", ROOT / "examples/star-cluster/audit.py"
)
assert SPEC is not None and SPEC.loader is not None
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


def test_matrix_contains_five_families_and_equal_velocity_mass_control():
    cases = dict(AUDIT.configurations())
    assert len(cases) == 40
    base = cases["tangential-base"]
    double = cases["tangential-double_probe_mass"]
    a = next(s for s in base["seeds"] if s["type"] == "probe")["values"]
    b = next(s for s in double["seeds"] if s["type"] == "probe")["values"]
    assert b["mass"] == 2 * a["mass"]
    assert b["momentum"] == [2 * p for p in a["momentum"]]
    assert sum(s["values"]["mass"] for s in base["seeds"][:-1]) == 3712
    assert cases["radial-no_field"]["emissions"] == []


def test_local_attraction_transfers_opposite_momentum():
    raw = dict(AUDIT.configurations())["radial-base"]
    raw["shape"] = [3, 3, 3]
    raw["seeds"] = [
        {"position": [1, 1, 1], "type": "held_source", "values": {"mass": 2048}},
        {"position": [2, 1, 1], "type": "probe", "values": {"mass": 64, "momentum": [0, 0, 0]}},
    ]
    raw["disturbance_types"][1]["transport"] = {"mode": "hold"}
    world = Simulation(parse_initial_state(raw))
    for _ in range(3):
        world.step()
        assert world.totals()["momentum"] == (0, 0, 0)
        assert world.totals()["mass"] == (2112,)
    probe = next(r for r in AUDIT.carriers(world.snapshot()) if r["type"] == "probe")
    assert probe["values"]["momentum"][0] < 0
    assert probe["values"]["momentum"][1:] == (0, 0)


def test_turn_classification_does_not_promote_radial_contact_or_escape():
    trajectory = [
        {"probe": {"position": [8, 5, 5], "values": {"momentum": [-8, 0, 0]}}, "contact": False}
    ]
    assert AUDIT.classify(trajectory, False, None)["classification"] == "no_two_revolutions_observed"
    assert AUDIT.classify(trajectory, True, None)["classification"] == "escaped"
    trajectory[0]["contact"] = True
    assert AUDIT.classify(trajectory, False, None)["classification"] == "cluster_contact"
    assert AUDIT.classify(trajectory, False, "overflow")["classification"] == "runtime_fault"


def test_faulted_step_is_observed_and_not_reported_as_orbit(tmp_path):
    raw = dict(AUDIT.configurations())["radial-stronger"]
    raw["shape"] = [3, 3, 3]
    raw["seeds"] = [
        {"position": [1, 1, 1], "type": "held_source", "values": {"mass": 2048}},
        {"position": [2, 1, 1], "type": "probe", "values": {"mass": 64}},
    ]
    raw["spatial_couplings"][0]["denominator"] = 1
    result = AUDIT.run_case(("fault", raw, str(tmp_path)))
    assert result["classification"] == "runtime_fault"
    assert "movement rate" in result["fault"]
    assert result["max_inventory_error"] == {"mass": 0, "signal": 0, "momentum": 0}
    import json

    frames = json.loads((tmp_path / "fault/trajectory.json").read_text())
    assert frames[-1]["tick"] == result["completed_ticks"]
