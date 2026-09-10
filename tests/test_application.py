import json
from dataclasses import replace

from event_universe import Config
from event_universe.compat import IntegerO1Field3D
from event_universe.core.state import PX
from event_universe.runner import run_scenario, source_fingerprint
from event_universe.scenarios import get_scenario


def test_runner_emits_reproducible_metadata_trace_and_self_contained_html(tmp_path):
    scenario = replace(get_scenario("contact"), ticks=2)
    path = run_scenario(scenario, tmp_path)
    metadata = json.loads((tmp_path / "run.json").read_text())
    assert metadata["source_sha256"] == source_fingerprint()
    assert metadata["scenario"]["particles"] == [list(seed) for seed in scenario.particles]
    assert metadata["momentum_equal_at_every_completed_tick"]
    assert metadata["status"] == "completed"
    assert "XY slice z=12" in path.read_text()
    assert "data:image/gif;base64," in path.read_text()
    assert (tmp_path / "events.jsonl").read_text()


def test_legacy_read_api_is_preserved():
    world = IntegerO1Field3D(Config(nx=8, ny=8, nz=8, source_strength=0))
    world.add_particle(0, 4, 4, 4, 3)
    world.step()
    assert world.particles[0][PX] == 3
    assert world.paths[0] and world.force_records
    assert world.total_momentum() == (3, 0, 0)
    assert world.audit()
    assert world.particles_on_xy_slice(4)[0][0] == 0


def test_volume_output_reuses_html_pipeline_without_changing_physical_events(tmp_path):
    scenario = replace(get_scenario("contact"), ticks=2)
    plane, volume = tmp_path / "plane", tmp_path / "volume"
    run_scenario(scenario, plane)
    path = run_scenario(scenario, volume, volume=True)
    assert (plane / "events.jsonl").read_bytes() == (volume / "events.jsonl").read_bytes()
    assert (
        json.loads((plane / "run.json").read_text())["report"]
        == json.loads((volume / "run.json").read_text())["report"]
    )
    assert "Full 3D XYZ view" in path.read_text()
    assert "data:image/gif;base64," in path.read_text()
