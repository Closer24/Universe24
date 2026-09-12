"""Presets and movies preserve declared state, names, failures and headless behavior."""

import json
from pathlib import Path

import pytest

from event_universe.reference_api import ReferenceSimulation as Simulation
from event_universe.reference_api import load_reference_state as load_initial_state
from event_universe.reference_runner import run_reference_initialization as run_initialization

ROOT = Path(__file__).resolve().parents[1]


def residents(frame):
    return {
        record["type"]: cell["position"] for cell in frame["cells"] for record in cell["disturbances"]
    }


def test_counterpropagating_preset_meets_and_passes_without_invented_collision():
    world = Simulation(load_initial_state(ROOT / "examples/01-two-approaching-particles.json"))
    assert residents(world.snapshot()) == {"Particle A": (16, 8, 4), "Particle B": (48, 8, 4)}
    for tick in range(1, 65):
        world.step()
        assert world.totals() == {"mass": (2,), "charge": (0,)}
        if tick == 32:
            assert residents(world.snapshot()) == {"Particle A": (32, 8, 4), "Particle B": (32, 8, 4)}
    assert residents(world.snapshot()) == {"Particle A": (48, 8, 4), "Particle B": (16, 8, 4)}


@pytest.mark.parametrize("name", ["02-parallel-particle-beams", "03-spreading-pulse"])
def test_other_presets_conserve_and_change_distribution(name):
    initial = load_initial_state(ROOT / "examples" / f"{name}.json")
    world = Simulation(initial)
    totals = world.totals()
    for _ in range(initial.ticks):
        world.step()
        assert world.totals() == totals
    frame = world.snapshot()
    if name.startswith("02"):
        positions = residents(frame)
        assert positions["Fast beam"] == (40, 4, 4)
        assert positions["Slow beam"] == (24, 12, 4)
    else:
        assert len([cell for cell in frame["cells"] if cell["disturbances"]]) > 1


@pytest.mark.visualization
def test_movie_embeds_exact_samples_and_final_state_without_changing_events(tmp_path):
    initial = ROOT / "examples/01-two-approaching-particles.json"
    movie = run_initialization(initial, tmp_path / "movie", ticks=9, visualize=True, frame_stride=4)
    run_initialization(initial, tmp_path / "headless", ticks=9)
    html = movie.read_text(encoding="utf-8")
    data = json.loads(
        html.split('<script id="recording" type="application/json">')[1].split("</script>")[0]
    )
    assert [frame["tick"] for frame in data["frames"]] == [0, 4, 8, 9]
    assert data["frames"][-1] == json.loads((tmp_path / "movie/state.json").read_text())
    assert data["metadata"]["shape"] == [65, 17, 9]
    assert data["metadata"]["link_ticks"] == 2
    assert (tmp_path / "movie/events.jsonl").read_bytes() == (
        tmp_path / "headless/events.jsonl"
    ).read_bytes()
    assert not (tmp_path / "headless/run.html").exists()


@pytest.mark.visualization
def test_movie_escapes_names_and_preserves_partial_failure(tmp_path):
    from event_universe.diagnostics.disturbance_render import render_disturbances

    frames = [{"tick": 0, "cells": [], "transfers": []}]
    name = '</script><img src=x onerror="bad()">'
    output = render_disturbances(
        frames, tmp_path / "run.html", {"model": name, "status": "failed", "error": name}
    )
    html = output.read_text(encoding="utf-8")
    assert name not in html
    data = json.loads(
        html.split('<script id="recording" type="application/json">')[1].split("</script>")[0]
    )
    assert data == {"frames": frames, "metadata": {"model": name, "status": "failed", "error": name}}
    with pytest.raises(ValueError, match="at least one"):
        render_disturbances([], tmp_path / "empty.html", {})
