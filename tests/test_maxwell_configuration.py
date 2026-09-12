"""Focused local scattering, ownership and independent measurement acceptance."""

import importlib.util
import math
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "maxwell_configuration", ROOT / "examples/maxwell/configuration.py"
)
CONFIGURATION = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CONFIGURATION)


def amplitudes(world, position):
    fields = world.spatial_values(position)
    return tuple(tuple(fields[name]["value"]) for name in CONFIGURATION.NAMES)


def test_local_reflection_has_independent_example_and_rejects_inexact_half():
    raw = CONFIGURATION.build_configuration((3, 3, 3), 2, [])
    raw["field_rules"] = raw["field_rules"][:1]
    raw["spatial_seeds"] = [
        {
            "position": [1, 1, 1],
            "field": CONFIGURATION.NAMES[0],
            "populations": [[0, 4, 0], *[[0, 0, 0] for _ in range(7)]],
        }
    ]
    world = Simulation(parse_initial_state(raw))
    before = amplitudes(world, (1, 1, 1))
    world.step()
    assert amplitudes(world, (1, 1, 1)) == (
        (0, 0, 0),
        (0, 0, 0),
        (-2, 0, 0),
        (2, 0, 0),
        (0, 2, 0),
        (0, 2, 0),
    )
    world.step()
    assert amplitudes(world, (1, 1, 1)) == before
    raw["spatial_seeds"][0]["populations"][0] = [0, 1, 0]
    world = Simulation(parse_initial_state(raw))
    before = amplitudes(world, (1, 1, 1))
    with pytest.raises(ValueError, match="exact integer"):
        world.step()
    assert world.faulted
    assert amplitudes(world, (1, 1, 1)) == before


def test_pure_electric_seed_crosses_one_link_with_transverse_magnetic_moment():
    raw = CONFIGURATION.build_configuration((9, 9, 9), 1, [((4, 4, 4), (0, 4, 0), (0, 0, 0))])
    world = Simulation(parse_initial_state(raw))
    world.step()
    scale = CONFIGURATION.AMPLITUDE_SCALE
    expected = {
        (5, 4, 4): 0,
        (3, 4, 4): 1,
        (4, 4, 5): 4,
        (4, 4, 3): 5,
    }
    total_squared = 0
    nonzero = set()
    for node in world.snapshot()["spatial_fields"]:
        position = tuple(node["position"])
        values = amplitudes(world, position)
        if any(v for vector in values for v in vector):
            nonzero.add(position)
            assert values[expected[position]] == (0, scale, 0)
            assert sum(any(vector) for vector in values) == 1
        total_squared += sum(v * v for vector in values for v in vector)
    assert nonzero == set(expected)
    assert total_squared == 4 * scale * scale
    assert world.snapshot()["spatial_transfers"] == []


@pytest.fixture
def measurements(monkeypatch):
    # Load the read-only measurement module without changing process import paths.
    monkeypatch.setitem(sys.modules, "configuration", CONFIGURATION)
    spec = importlib.util.spec_from_file_location(
        "maxwell_measurements", ROOT / "examples/maxwell/measurements.py"
    )
    measurements = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(measurements)
    return measurements


def test_frequency_estimator_recovers_oscillation_with_static_and_fast_components(measurements):
    omega = math.pi / 6
    samples = [7 + 3 * math.cos(omega * t) + 2 * math.cos((math.pi - omega) * t) for t in range(17)]
    result = measurements.frequency(samples)
    assert abs(result["omega"] - omega) < 1e-12
    assert result["recurrence_residual"] < 1e-12
    assert measurements.frequency([7] * 17)["status"] == "static or insufficient signal"


def test_divergence_includes_empty_neighbors_of_a_sparse_field(measurements):
    values = {(4, 4, 4): ((0, 4, 0), (0, 0, 0))}
    assert measurements.centered_divergence(values, (9, 9, 9), 0) == 4
    assert measurements.centered_divergence(values, (9, 9, 9), 1) == 0


def test_known_gauss_counterexample_from_a_compact_integer_curl(measurements):
    """Reproduce a failed physical target; this is not Maxwell acceptance."""
    # Centered curl of one nonzero Z potential. Commuting differences give div(E)=0.
    seeds = [
        ((4, 3, 4), (4, 0, 0), (0, 0, 0)),
        ((4, 5, 4), (-4, 0, 0), (0, 0, 0)),
        ((3, 4, 4), (0, -4, 0), (0, 0, 0)),
        ((5, 4, 4), (0, 4, 0), (0, 0, 0)),
    ]
    world = Simulation(parse_initial_state(CONFIGURATION.build_configuration((9, 9, 9), 1, seeds)))
    before, norm = measurements.moments(world.snapshot())
    assert measurements.centered_divergence(before, (9, 9, 9), 0) == 0
    world.step()
    after, after_norm = measurements.moments(world.snapshot())
    assert after_norm == norm
    assert measurements.centered_divergence(after, (9, 9, 9), 0) > 0
