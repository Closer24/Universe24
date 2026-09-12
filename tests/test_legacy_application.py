import builtins
import json
import runpy
import subprocess
import sys
from dataclasses import replace
from pathlib import Path
from types import ModuleType

import pytest

from event_universe.legacy_runner import main, run_scenario, source_fingerprint
from event_universe.particle_scenarios import get_scenario


def test_legacy_acceptance_tool_resolves_its_explicit_scalar_model(monkeypatch):
    from event_universe.particle_api import ScalarSimulation

    renderer = ModuleType("event_universe.diagnostics.render")
    renderer.render_volume = lambda *args, **kwargs: pytest.fail("rendering was not requested")
    monkeypatch.setitem(sys.modules, renderer.__name__, renderer)
    namespace = runpy.run_path(
        str(Path(__file__).resolve().parents[1] / "tools/check_diagonal_motion.py")
    )
    assert namespace["ScalarSimulation"] is ScalarSimulation


def test_runner_import_does_not_load_optional_rendering_dependencies():
    script = """
import sys
sys.path.insert(0, sys.argv[1])
import event_universe.legacy_runner
for name in ('matplotlib', 'PIL', 'numpy', 'event_universe.diagnostics.render'):
    assert name not in sys.modules, name
"""
    result = subprocess.run(
        [sys.executable, "-c", script, str(Path(__file__).resolve().parents[1] / "src")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr


def test_default_run_writes_metadata_without_capturing_or_importing_renderer(tmp_path, monkeypatch):
    from event_universe.diagnostics import frames

    def reject_capture(*args, **kwargs):
        pytest.fail("headless runs must not capture visualization frames")

    original_import = builtins.__import__

    def reject_renderer(name, *args, **kwargs):
        if name == "event_universe.diagnostics.render" or name.split(".")[0] in {
            "matplotlib",
            "PIL",
            "numpy",
        }:
            pytest.fail("headless runs must not import rendering dependencies")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(frames, "capture_frame", reject_capture)
    monkeypatch.setattr(frames, "capture_volume", reject_capture)
    monkeypatch.setattr(builtins, "__import__", reject_renderer)
    path = run_scenario(replace(get_scenario("stationary"), ticks=0), tmp_path)
    assert path == tmp_path / "run.json"
    metadata = json.loads(path.read_text())
    assert metadata["display"] == "none"
    assert metadata["status"] == "completed"
    assert metadata["report"]["tick"] == 0
    assert {item.name for item in tmp_path.iterdir()} == {"events.jsonl", "run.json"}


@pytest.mark.parametrize(
    ("options", "visualize", "volume"),
    [
        ([], False, True),
        (["--visualize"], True, True),
        (["--view-3d"], True, True),
        (["--view-2d"], True, False),
        (["--plane", "XZ"], True, False),
        (["--slice", "2"], True, False),
    ],
)
def test_legacy_cli_requires_explicit_visualization(options, visualize, volume, monkeypatch, tmp_path):
    received = {}

    def record_run(scenario, output, **kwargs):
        received.update(kwargs)
        return output / "run.json"

    monkeypatch.setattr("event_universe.legacy_runner.run_scenario", record_run)
    monkeypatch.setattr(
        sys,
        "argv",
        ["event-universe", "--scenario", "stationary", "--output", str(tmp_path), *options],
    )
    main()
    assert received["visualize"] is visualize
    assert received["volume"] is volume


@pytest.mark.visualization
def test_volume_output_reuses_html_pipeline_without_changing_physical_events(tmp_path):
    scenario = replace(get_scenario("contact"), ticks=2)
    plane, volume = tmp_path / "plane", tmp_path / "volume"
    run_scenario(scenario, plane, volume=False, visualize=True)
    path = run_scenario(scenario, volume, visualize=True)
    metadata = json.loads((volume / "run.json").read_text())
    assert metadata["source_sha256"] == source_fingerprint()
    assert metadata["scenario"]["particles"] == [list(seed) for seed in scenario.particles]
    assert metadata["momentum_equal_at_every_completed_tick"]
    assert metadata["status"] == "completed"
    assert metadata["display"] == "volume-3d"
    assert (volume / "events.jsonl").read_text()

    assert (plane / "events.jsonl").read_bytes() == (volume / "events.jsonl").read_bytes()
    assert (
        json.loads((plane / "run.json").read_text())["report"]
        == json.loads((volume / "run.json").read_text())["report"]
    )
    assert "Full 3D XYZ view" in path.read_text()
    assert "data:image/gif;base64," in path.read_text()
