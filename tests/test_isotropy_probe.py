"""Isotropy probe: outward path counts and straight-ray counting spread on recorded runs."""

import importlib.util
import json
from pathlib import Path

from event_universe.configuration_validation import validate_configuration

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "isotropy_probe", ROOT / "examples/isotropy-probe/run_experiments.py"
)
PROBE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(PROBE)


def test_path_count_reproduces_the_shell_identity_and_the_axis_suppression():
    shell = [
        (x, y, z)
        for x in range(-9, 10)
        for y in range(-9, 10)
        for z in range(-9, 10)
        if abs(x) + abs(y) + abs(z) == 9
    ]
    assert len(shell) == 4 * 81 + 2
    total = sum(PROBE.path_count(*point) for point in shell)
    assert abs(total - PROBE.OUTWARD_SOURCE) < 1e-6
    assert PROBE.path_count(9, 0, 0) == 4 and PROBE.path_count(3, 3, 3) == 1680
    assert PROBE.path_count(5, 0, 0) == 324


def test_configurations_are_valid_and_derive_from_the_checked_in_examples():
    outward = PROBE.outward_configuration()
    assert outward["spatial_fields"][0]["transport"] == "outward"
    assert validate_configuration(json.dumps(outward).encode()).valid
    rays = PROBE.ray_configuration(256)
    field = rays["spatial_fields"][0]
    assert field["transport"] == "ray" and len(field["headings"]) == 256
    assert rays["ticks"] == PROBE.RAY_WARMUP + 4
    assert validate_configuration(json.dumps(rays).encode()).valid


def test_outward_stock_is_the_path_count_and_far_from_isotropic(tmp_path):
    result = PROBE.outward_probe(tmp_path / "probe")
    assert result["shell_mean_measured"] == result["shell_mean_predicted"]
    points = {tuple(row["offset"]): row for row in result["points"]}
    assert points[(9, 0, 0)]["measured"] == 4 and points[(3, 3, 3)]["measured"] == 1680
    assert points[(9, 0, 0)]["measured_over_isotropic"] < 0.01
    assert result["same_euclidean_distance_5"]["diagonal_over_axis"] > 5


def test_small_ray_sweep_reaches_the_shell_with_counting_spread(tmp_path):
    result = PROBE.ray_probe(tmp_path / "probe", 256)
    assert result["sweep_ticks"] == 4 and result["shell_nodes"] > 0
    assert result["rays_per_node_per_sweep_mean"] > 0
    assert result["relative_spread"] > 0
