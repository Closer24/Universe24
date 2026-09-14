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
