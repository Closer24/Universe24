import json
from dataclasses import replace

from event_universe.runner import run_scenario, source_fingerprint
from event_universe.scenarios import get_scenario


def test_volume_output_reuses_html_pipeline_without_changing_physical_events(tmp_path):
    scenario = replace(get_scenario("contact"), ticks=2)
    plane, volume = tmp_path / "plane", tmp_path / "volume"
    run_scenario(scenario, plane, volume=False)
    path = run_scenario(scenario, volume)
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
