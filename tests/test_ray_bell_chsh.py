"""Bell's test on the ray: Malus's law at each detector, S below the local bound, closed."""

import importlib.util
from pathlib import Path

import pytest

from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "bell_chsh_probe", ROOT / "examples/bell-chsh/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_aligned_phases_land_deterministically_and_the_world_closes():
    for seed in (1, 2, 3):
        aligned = PROBE.outcomes(PROBE.document(0, 0, 0, seed))
        opposite = PROBE.outcomes(PROBE.document(PROBE.HALF_TURN, 0, 0, seed))
        # Alice's ray at the reference phase is taken surely at her plus detector; Bob's
        # ray, a half turn away from his, walks on to his minus detector; and the reverse.
        assert (aligned["alice"], aligned["bob"]) == (1, -1) and aligned["closed"]
        assert (opposite["alice"], opposite["bob"]) == (-1, 1) and opposite["closed"]


def test_one_seed_over_every_hidden_phase_stays_below_the_local_bound():
    result = PROBE.chsh(seeds=1)
    assert result["closed"]
    assert result["quantum_S"] == 2.8284 and result["predicted_S"] == 1.4144
    # One capture seed over the 64 hidden phases: 256 pairs, every one landed.
    assert all(
        value["missing"] == 0 and value["pairs"] == 64 for value in result["correlations"].values()
    )
    assert result["S"] == 1.5001 and result["same_setting_E"] == -0.5312
    assert result["S"] < result["local_bound"] < result["quantum_S"]


def test_capture_salt_is_validated():
    raw = PROBE.document(0, 0, 0, 1)
    raw["spatial_couplings"][0]["capture_salt"] = PROBE.PHASE_STEPS * 0 + 1073741789
    with pytest.raises(ValueError, match="ticket modulus"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1)
    raw["spatial_fields"][0]["kerengonen"] = {"phase_steps": PROBE.PHASE_STEPS, "phase_advance": 0}
    with pytest.raises(ValueError, match="requires the lottery"):
        parse_initial_state(raw)


def test_deterministic_hidden_variables_reach_the_bound_and_stop_there():
    result = PROBE.chsh(seeds=1, capture="threshold")
    assert result["closed"] and result["capture"] == "threshold"
    assert [value["E"] for value in result["correlations"].values()] == [-0.5, 0.5, -0.5, -0.5]
    assert [value["predicted_E"] for value in result["correlations"].values()] == [-0.5, 0.5, -0.5, -0.5]
    assert result["S"] == 2.0 == result["local_bound"] < result["quantum_S"]
    assert result["same_setting_E"] == -0.9375


def test_bonded_pairs_break_the_local_bound_with_the_singlet_law():
    for seed in (1, 2, 3):
        same = PROBE.outcomes(PROBE.document(0, 0, 0, seed, capture="bond"))
        opposite = PROBE.outcomes(PROBE.document(0, 0, PROBE.HALF_TURN, seed, capture="bond"))
        # Equal settings never agree, settings a half turn apart always do; both closed.
        assert same["alice"] == -same["bob"] and same["closed"]
        assert opposite["alice"] == opposite["bob"] and opposite["closed"]
    result = PROBE.chsh(seeds=1, capture="bond")
    assert result["closed"] and result["predicted_S"] == 2.8284
    assert all(value["missing"] == 0 for value in result["correlations"].values())
    # One number per bonded pair: the second end reads the first end's number.
    assert [value["E"] for value in result["correlations"].values()] == [
        -0.6875,
        0.7188,
        -0.6875,
        -0.6875,
    ]
    assert result["S"] == 2.7813 and result["same_setting_E"] == -1.0
    assert result["S"] > result["local_bound"]


def test_both_rays_carry_the_code_of_their_birth_node_and_tick():
    from event_universe import Simulation
    from event_universe.core.spatial_state import origin_bond

    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    initial = parse_initial_state(raw)
    assert initial.emissions[0].bond_origin and initial.emissions[1].bond_origin
    world = Simulation(initial)
    world.step()
    bonds = {
        ray.bond for node in world.inventory_view().nodes for ray in (node.rays[0] if node.rays else ())
    }
    # One pair, one code: the source Node and the tick of the emission.
    assert bonds == {origin_bond((PROBE.CENTER, 1, 1), (PROBE.WIDTH, 3, 3), 0)}
    assert origin_bond((0, 0, 0), (13, 3, 3), 0) == 1
    assert origin_bond((0, 0, 0), (13, 3, 3), 5) == 6
    assert origin_bond((1, 0, 0), (13, 3, 3), 0) != origin_bond((0, 1, 0), (13, 3, 3), 0)


def test_bonds_are_validated():
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    raw["spatial_fields"][0]["bond"]["seed"] = 1073741789
    with pytest.raises(ValueError, match="ticket modulus"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    del raw["spatial_fields"][0]["bond"]
    with pytest.raises(ValueError, match="bond_field requires"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    del raw["spatial_fields"][0]["bond"]
    for rule in raw["emissions"]:
        rule.pop("bond_field", None)
    with pytest.raises(ValueError, match="bond_setting requires"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    del raw["spatial_fields"][0]["kerengonen"]
    with pytest.raises(ValueError, match="requires a kerengonen"):
        parse_initial_state(raw)
    raw = PROBE.document(0, 0, 0, 1, capture="bond")
    raw["emissions"][0]["bond_field"] = "momentum"
    with pytest.raises(ValueError, match="scalar owned"):
        parse_initial_state(raw)
