"""Reference commands resolve canonical inputs and retain numerical acceptance."""

import importlib.util
from pathlib import Path

from event_universe import BalancedSimulation, CausalStreamSimulation, LinkedSimulation, ScalarSimulation
from event_universe.core.scalar_engine import ScalarEngine
from event_universe.particle_api import ScalarSimulation as HistoricalSimulation
from event_universe.reference_api import ReferenceSimulation as GenericSimulation
from event_universe.reference_api import ReferenceSimulation as Simulation

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "examples/known-entities/run_reference_checks.py"


def load_reference_checks():
    spec = importlib.util.spec_from_file_location("reference_examples", SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_public_names_resolve_active_and_historical_owners_without_duplicate_engines():
    assert Simulation is GenericSimulation
    assert ScalarSimulation is HistoricalSimulation
    assert issubclass(ScalarSimulation, ScalarEngine)
    for candidate in (ScalarSimulation, LinkedSimulation, BalancedSimulation, CausalStreamSimulation):
        assert candidate.__module__ == "event_universe.particle_api"


def test_reference_collision_uses_the_workspace_configuration():
    reference = load_reference_checks()
    canonical = ROOT / "examples/04-unequal-mass-collision.json"
    assert reference.REFERENCE_CONFIGURATIONS["collision"] == canonical
    assert all(path.is_file() for path in reference.REFERENCE_CONFIGURATIONS.values())
    assert len(set(reference.REFERENCE_CONFIGURATIONS.values())) == 5


def test_three_mass_reference_reuses_the_workspace_input_with_explicit_duration():
    reference = load_reference_checks()
    assert reference.REFERENCE_CONFIGURATIONS["three-masses"] == ROOT / "examples/three_mass_finite.json"
    assert reference.REFERENCE_TICK_OVERRIDES == {"three-masses": 120}


def test_five_reference_worlds_retain_existing_independent_assertions(tmp_path, monkeypatch):
    reference = load_reference_checks()
    monkeypatch.setattr(reference, "ROOT", tmp_path)
    reference.main()
    outputs = list((tmp_path / "artifacts").glob("known-entities-*"))
    assert len(outputs) == 1
    import json

    original = json.loads((outputs[0] / "three-masses/initialization.json").read_text())
    metadata = json.loads((outputs[0] / "three-masses/run.json").read_text())
    assert original["ticks"] == 100 and metadata["completed_ticks"] == 120
    assert not list(outputs[0].rglob("*.html"))
    assert not list(outputs[0].rglob("*.gif"))
