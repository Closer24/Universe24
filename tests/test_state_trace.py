"""Exact optional state traces remain passive and preserve ordinary runner defaults."""

import json

import pytest

from event_universe import Simulation
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization


def configuration():
    return {
        "schema_version": 1,
        "model_id": "state-trace-test",
        "shape": [7, 7, 7],
        "boundary": "open",
        "slots_per_node": 1,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 4,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": "stock",
                "components": 1,
                "signed": False,
                "conserved": True,
                "extensive": True,
                "units": "test units",
            }
        ],
        "disturbance_types": [
            {
                "name": "emitter",
                "fields": ["stock"],
                "defaults": {"stock": 12},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {
                "field": "stock",
                "baseline": 0,
                "transport": "ray",
                "ray_slots": 12,
                "rays_per_tick": 6,
                "headings": [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]],
            }
        ],
        "emissions": [
            {"type": "emitter", "field": "stock", "amount": {"field": "stock"}, "source": False}
        ],
        "seeds": [{"position": [3, 3, 3], "type": "emitter"}],
    }


@pytest.mark.parametrize("content", ["all", "carriers"])
def test_trace_is_complete_and_does_not_change_events_or_final_state(tmp_path, content):
    initial = tmp_path / "initial.json"
    initial.write_text(json.dumps(configuration()))
    baseline, traced = tmp_path / "baseline", tmp_path / "traced"
    run_initialization(initial, baseline)
    run_initialization(initial, traced, frame_stride=3, state_trace=content)
    assert not (baseline / "states.jsonl").exists()
    assert not (traced / "run.html").exists()
    assert (baseline / "events.jsonl").read_bytes() == (traced / "events.jsonl").read_bytes()
    assert (baseline / "state.json").read_bytes() == (traced / "state.json").read_bytes()
    frames = [json.loads(line) for line in (traced / "states.jsonl").read_text().splitlines()]
    assert [frame["tick"] for frame in frames] == [0, 1, 2, 3, 4]
    metadata = json.loads((traced / "run.json").read_text())
    assert metadata["state_trace"]["rows"] == 5
    assert metadata["state_trace"]["source_sha256"] == metadata["source_sha256"]
    assert metadata["state_trace"]["initialization_sha256"] == metadata["initialization_sha256"]
    with Simulation(parse_initial_state(configuration())) as world:
        for index, frame in enumerate(frames):
            if index:
                world.step()
            accounting = frame.pop("accounting")
            assert accounting["totals"] == json.loads(json.dumps(world.totals()))
            expected = world.snapshot(include_spatial=content == "all")
            assert frame == json.loads(json.dumps(expected))
    full = json.loads((traced / "state.json").read_text())
    if content == "all":
        assert frames[-1] == full
    else:
        assert set(frames[-1]) < set(full)
        assert all(full[key] == value for key, value in frames[-1].items())


def test_invalid_snapshot_selection_rejects_before_any_run_output(tmp_path):
    initial = tmp_path / "initial.json"
    initial.write_text(json.dumps(configuration()))
    with pytest.raises(ValueError, match="frame_content"):
        run_initialization(initial, tmp_path / "output", state_trace="invented")
    assert not (tmp_path / "output").exists()
    with Simulation(parse_initial_state(configuration())) as world:
        with pytest.raises(ValueError, match="boolean"):
            world.snapshot(include_spatial=0)
