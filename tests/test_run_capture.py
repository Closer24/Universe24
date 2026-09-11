"""Capture only the selected view without losing final or partially committed state."""

import json
from dataclasses import replace
from fractions import Fraction
from types import SimpleNamespace

import pytest

from event_universe import CellState, Config, ParticleState, runner
from event_universe.core.contracts import MoveRecord
from event_universe.diagnostics.frames import Slice
from event_universe.scenarios import Scenario


def scenario(ticks):
    return Scenario(
        "capture-contract",
        Config(nx=8, ny=8, nz=8, c_units=12, source_strength=0),
        ((0, 2, 3, 4, 6, 0, 0), (1, 6, 5, 2, 0, 0, 0)),
        ticks,
        Slice("XY", 4),
    )


def observe_capture(monkeypatch, volume):
    captured = []
    name = "capture_volume" if volume else "capture_frame"
    original = getattr(runner, name)

    def capture(*args, **kwargs):
        frame = original(*args, **kwargs)
        captured.append(frame)
        return frame

    def unused_view(*args, **kwargs):
        raise AssertionError("the unselected view must not traverse the world")

    monkeypatch.setattr(runner, name, capture)
    monkeypatch.setattr(runner, "capture_frame" if volume else "capture_volume", unused_view)
    return captured


@pytest.mark.parametrize("volume", [False, True])
@pytest.mark.parametrize("ticks,expected_ticks", [(0, [0]), (3, [0, 2, 3])])
def test_selected_capture_preserves_empty_duration_and_unsampled_final_state(
    monkeypatch, tmp_path, volume, ticks, expected_ticks
):
    captured = observe_capture(monkeypatch, volume)
    output = runner.run_scenario(scenario(ticks), tmp_path, volume=volume, frame_stride=2)
    assert [frame.tick for frame in captured] == expected_ticks
    for frame in captured:
        assert frame.total_momentum == (6, 0, 0)
        assert frame.field == {}
        x = 2 if frame.tick < 2 else 3
        assert frame.particles == (
            [(0, x, 3, 4, 6, 0, 0), (1, 6, 5, 2, 0, 0, 0)] if volume else [(0, x, 3, 6, 0, 0)]
        )
    metadata = json.loads((tmp_path / "run.json").read_text())
    assert metadata["status"] == "completed"
    assert metadata["report"]["tick"] == ticks
    assert metadata["momentum_equal_at_every_completed_tick"]
    assert all(metadata["report"]["checks"].values())
    events = [json.loads(line) for line in (tmp_path / "events.jsonl").read_text().splitlines()]
    assert len([event for event in events if event["kind"] == "force"]) == 2 * ticks
    assert "data:image/gif;base64," in output.read_text()


@pytest.mark.parametrize("volume", [False, True])
def test_invalid_slice_rejects_even_when_volume_is_selected(tmp_path, volume):
    invalid = replace(scenario(0), view=Slice("XY", 8))
    with pytest.raises(ValueError, match="slice coordinate outside"):
        runner.run_scenario(invalid, tmp_path, volume=volume)


@pytest.mark.parametrize("volume", [False, True])
def test_failed_step_captures_new_state_and_momentum_without_a_tick_increment(
    monkeypatch, tmp_path, volume
):
    # A diagnostic test double exposes a partial commit, independently of any physical law.
    world = SimpleNamespace(
        config=scenario(1).config,
        tick=0,
        faulted=False,
        cells={(2, 3, 4): CellState(phi=7)},
        particles={0: ParticleState(2, 3, 4, 2, 0, 0, momentum_den=3)},
    )

    def fail_after_commit():
        world.cells[(2, 3, 4)] = CellState(phi=11, px=5)
        world.particles[0] = world.particles[0]._replace(px=1)
        world.faulted = True
        raise RuntimeError("injected failure after a local commit")

    def create(self, observer):
        observer.on_move(MoveRecord(0, 0, 2, 3, 4))
        return world

    world.step = fail_after_commit
    monkeypatch.setattr(Scenario, "create", create)
    captured = observe_capture(monkeypatch, volume)
    with pytest.raises(RuntimeError, match="after a local commit"):
        runner.run_scenario(scenario(1), tmp_path, volume=volume, frame_stride=8)
    assert [frame.tick for frame in captured] == [0, 0]
    assert [frame.total_momentum for frame in captured] == [
        (Fraction(2, 3), 0, 0),
        (Fraction(16, 3), 0, 0),
    ]
    position = (2, 3, 4) if volume else (2, 3)
    assert captured[0].field == {position: 7}
    assert captured[1].field == {position: 11}
    assert captured[1].particles == ([(0, 2, 3, 4, 1, 0, 0)] if volume else [(0, 2, 3, 1, 0, 0)])
    metadata = json.loads((tmp_path / "run.json").read_text())
    assert metadata["status"] == "failed"
    assert metadata["report"] == {"tick": 0, "faulted": True}
    assert "FAILED RUN" in (tmp_path / "run.html").read_text()
    assert (tmp_path / "events.jsonl").read_text()
