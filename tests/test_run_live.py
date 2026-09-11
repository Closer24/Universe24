"""Live diagnostics must leave canonical runs intact and clean up on every exit."""

import importlib
import json
import sys
from copy import deepcopy
from types import SimpleNamespace

import pytest

from event_universe import Config, ParticleState, runner
from event_universe.core.engine import Engine
from event_universe.diagnostics.frames import Slice
from event_universe.scenarios import Scenario


def scenario(ticks=2):
    return Scenario(
        "live-capture-contract",
        Config(nx=8, ny=8, nz=8, c_units=12, source_strength=0),
        ((0, 2, 3, 4, 6, 0, 0), (1, 6, 5, 2, 0, 0, 0)),
        ticks,
        Slice("XY", 4),
    )


@pytest.mark.parametrize("volume", [False, True])
def test_live_worker_keeps_all_canonical_frames_events_and_metadata(monkeypatch, tmp_path, volume):
    plain, live = tmp_path / "plain", tmp_path / "live"
    captures = []
    name = "render_volume" if volume else "render_run"
    original_render = getattr(runner, name)

    def render(frames, *args, **kwargs):
        captures.append(deepcopy(frames))
        return original_render(frames, *args, **kwargs)

    monkeypatch.setattr(runner, name, render)
    runner.run_scenario(scenario(), plain, volume=volume)
    original_step = Engine.step

    def step(world):
        assert (live / "live.html").is_file()
        return original_step(world)

    monkeypatch.setattr(Engine, "step", step)
    artifact = runner.run_scenario(scenario(), live, volume=volume, live=True)
    assert captures[0] == captures[1]
    assert [frame.tick for frame in captures[1]] == [0, 1, 2]
    assert captures[1][0].particles[0][1] == 2
    assert captures[1][-1].particles[0][1] == 3
    assert (plain / "events.jsonl").read_bytes() == (live / "events.jsonl").read_bytes()
    assert json.loads((plain / "run.json").read_text()) == json.loads((live / "run.json").read_text())
    assert "run.html" in (live / "live.html").read_text()
    assert "data:image/gif;base64," in artifact.read_text()


@pytest.fixture
def display_spy(monkeypatch):
    instances = []

    class RecordingDisplay:
        def __init__(self, output, **kwargs):
            self.output = output
            self.stopped = False
            self.closed = False
            self.failure = None
            self.artifact = None
            self.submissions = []
            self.rendered_indices = []
            instances.append(self)

        def start(self):
            (self.output / "live.html").write_text("Preparing live display", encoding="utf-8")

        def submit(self, frame):
            self.submissions.append(deepcopy(frame))

        def stop_preview(self):
            self.stopped = True

        def rendered(self, index, image):
            assert self.stopped
            self.rendered_indices.append(index)

        def finish(self, artifact):
            self.artifact = artifact
            prefix = f"FAILED: {self.failure}. " if self.failure is not None else ""
            (self.output / "live.html").write_text(f"{prefix}Final report: run.html", encoding="utf-8")

        def fail(self, error):
            self.failure = error
            suffix = " Final report: run.html" if self.artifact is not None else ""
            (self.output / "live.html").write_text(f"FAILED: {error}{suffix}", encoding="utf-8")

        def close(self):
            self.closed = True

    monkeypatch.setattr(runner, "LiveDisplay", RecordingDisplay)
    return instances, RecordingDisplay


def failure_world(error):
    world = SimpleNamespace(
        config=scenario().config,
        tick=0,
        faulted=False,
        cells={},
        particles={0: ParticleState(2, 3, 4, 6, 0, 0), 1: ParticleState(6, 5, 2)},
    )

    def step():
        world.particles[0] = world.particles[0]._replace(px=7)
        world.faulted = True
        raise error

    world.step = step
    return world


@pytest.mark.parametrize("export_fails", [False, True])
def test_physical_failure_retains_original_error_and_cleans_live_display(
    monkeypatch, tmp_path, display_spy, export_fails
):
    failure = RuntimeError("injected physical update failure")
    world = failure_world(failure)
    monkeypatch.setattr(Scenario, "create", lambda self, observer: world)
    render_error = OSError("injected final export failure")
    if export_fails:

        def fail_export(*args, **kwargs):
            raise render_error

        monkeypatch.setattr(runner, "render_volume", fail_export)
    with pytest.raises(RuntimeError) as caught:
        runner.run_scenario(scenario(), tmp_path, live=True)
    assert caught.value is failure
    display = display_spy[0][0]
    assert display.failure is failure
    assert display.closed and display.stopped
    assert [frame.total_momentum for frame in display.submissions] == [(6, 0, 0), (7, 0, 0)]
    metadata = json.loads((tmp_path / "run.json").read_text())
    assert metadata["status"] == "failed"
    assert metadata["report"] == {"tick": 0, "faulted": True}
    assert str(failure) in (tmp_path / "live.html").read_text()
    if export_fails:
        assert caught.value.__cause__ is render_error
        assert display.artifact is None
    else:
        assert display.rendered_indices == [0, 1]
        assert display.artifact == tmp_path / "run.html"
        assert "FAILED RUN" in display.artifact.read_text()


@pytest.mark.parametrize("stage", ["start", "metadata", "interrupt"])
def test_live_cleanup_covers_startup_metadata_and_interruption(
    monkeypatch, tmp_path, display_spy, stage
):
    error = OSError("injected metadata failure") if stage == "metadata" else KeyboardInterrupt()

    def fail(*args, **kwargs):
        raise error

    if stage == "start":
        monkeypatch.setattr(display_spy[1], "start", fail)
    elif stage == "metadata":
        monkeypatch.setattr(runner, "report", fail)
    else:
        world = failure_world(error)
        monkeypatch.setattr(Scenario, "create", lambda self, observer: world)
    with pytest.raises(type(error)) as caught:
        runner.run_scenario(scenario(0 if stage == "metadata" else 1), tmp_path, live=True)
    assert caught.value is error
    display = display_spy[0][0]
    assert display.failure is error
    assert display.closed


@pytest.mark.parametrize("flags,expected_live", [([], True), (["--no-live"], False)])
def test_cli_live_default_and_explicit_opt_out(monkeypatch, tmp_path, capsys, flags, expected_live):
    invocations = []

    def run(selected, output, **kwargs):
        invocations.append(kwargs)
        return output / "run.html"

    monkeypatch.setattr(runner, "run_scenario", run)
    monkeypatch.setattr(sys, "argv", ["event-universe", "--output", str(tmp_path), *flags])
    runner.main()
    assert invocations[0]["live"] is expected_live
    lines = capsys.readouterr().out.splitlines()
    expected = [str((tmp_path / "run.html").resolve())]
    if expected_live:
        expected.insert(0, str((tmp_path / "live.html").resolve()))
    assert lines == expected


def test_importing_module_entrypoint_does_not_launch_another_cli(monkeypatch):
    def unexpected_main():
        raise AssertionError("a spawned import must not start another simulation")

    with monkeypatch.context() as guard:
        guard.setattr(runner, "main", unexpected_main)
        module = importlib.import_module("event_universe.__main__")
        importlib.reload(module)
    importlib.reload(module)
