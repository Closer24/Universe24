"""The curvature probe must permit mode mixing before it can test deflection."""

import importlib.util
import json
from copy import deepcopy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "examples/computational-curvature"
SPEC = importlib.util.spec_from_file_location("curvature_configuration", HERE / "configuration.py")
CONFIG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONFIG)


def test_mixing_enables_four_transverse_directions_from_one_incoming_mode():
    options = CONFIG.settings()
    options["normal_budget"] = 100000
    options["wave_seed_positions"] = [[2, 4, 4]]
    raw = CONFIG.configuration(options, mass=0, delay={"weights": 1, "spatial_mode": "fixed"})
    raw["spatial_seeds"][0]["populations"][0] = [0, 4, 0]
    world = Simulation(parse_initial_state(raw))
    world.step()
    expected = {
        (2, 5, 4): (2, (-2, 0, 0)),
        (2, 3, 4): (3, (2, 0, 0)),
        (2, 4, 5): (4, (0, 2, 0)),
        (2, 4, 3): (5, (0, 2, 0)),
    }
    for position, (mode, amplitude) in expected.items():
        assert world.spatial_values(position)[CONFIG.WAVE.NAMES[mode]]["value"] == amplitude
    assert all(item["balanced"] for item in world.spatial_accounting().values())
    # Same seed without mixing is the old locked-direction negative control.
    raw = CONFIG.configuration(
        options, mass=0, delay={"weights": 1, "spatial_mode": "fixed"}, mixing=False
    )
    raw["spatial_seeds"][0]["populations"][0] = [0, 4, 0]
    world = Simulation(parse_initial_state(raw))
    world.step()
    assert world.spatial_values((3, 4, 4))[CONFIG.WAVE.NAMES[0]]["value"] == (0, 4, 0)
    assert all(
        not any(world.spatial_values(position)[CONFIG.WAVE.NAMES[mode]]["value"])
        for position, (mode, _) in expected.items()
    )


def test_uniform_and_directional_variants_share_the_exact_wave_law():
    options = CONFIG.settings()
    first = CONFIG.configuration(options, delay={"weights": 1, "spatial_mode": "cost"})
    second = CONFIG.configuration(options)
    assert first["field_rules"] == second["field_rules"]
    assert first["spatial_seeds"] == second["spatial_seeds"]
    assert first["spatial_fields"] == second["spatial_fields"]
    assert first["directional_delay"] != second["directional_delay"]
    assert not any(t["transport"]["mode"] == "move" for t in first["disturbance_types"])


@pytest.mark.parametrize(
    "name,value",
    [
        ("observer_position", [99, 4, 4]),
        ("far_clock", [-1, 4, 4]),
        ("wave_seed_positions", [[2, 4, 4], [2, 4, 4]]),
        ("normal_budget", True),
        ("link_ticks", 0),
    ],
)
def test_measurement_placements_and_integer_settings_are_validated(tmp_path, name, value):
    raw = deepcopy(CONFIG.settings())
    raw[name] = value
    path = tmp_path / "settings.json"
    path.write_text(json.dumps(raw))
    with pytest.raises(ValueError):
        CONFIG.settings(path)


def test_missing_arrival_is_censored_not_a_failed_or_zero_mass_effect(monkeypatch):
    monkeypatch.setitem(__import__("sys").modules, "configuration", CONFIG)
    spec = importlib.util.spec_from_file_location("curvature_measurements", HERE / "measure.py")
    measure = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(measure)
    assert (
        measure.delay_difference(
            {"audit_detector_first_wave_tick": None}, {"audit_detector_first_wave_tick": 4}
        )
        is None
    )
    assert (
        measure.delay_difference(
            {"audit_detector_first_wave_tick": 7}, {"audit_detector_first_wave_tick": 4}
        )
        == 3
    )
