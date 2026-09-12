"""Independent processes preserve exact runs, failures and immutable input copies."""

import json
import multiprocessing
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from event_universe import batch as batch_module
from event_universe.batch import run_batch
from event_universe.retention import cleanup_expired
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]


def test_spawned_workers_match_direct_runs_and_retention_preserves_originals(tmp_path):
    observed = tmp_path / "observed.json"
    raw = json.loads((ROOT / "examples/basic.json").read_text())
    raw["observer"] = {"position": [2, 2, 2]}
    observed.write_text(json.dumps(raw))
    paths = [ROOT / "examples/basic.json", ROOT / "examples/exchange.json", observed]
    batch = tmp_path / "batch"
    result = json.loads(run_batch(paths, batch, workers=2, ticks=8).read_text())
    assert result["status"] == "completed" and result["workers"] == 2
    assert [job["index"] for job in result["jobs"]] == [0, 1, 2]
    for index, (path, job) in enumerate(zip(paths, result["jobs"], strict=True)):
        assert job["worker_pid"] != os.getpid()
        destination = batch / job["output"]
        assert (batch / job["input"]).read_bytes() == path.read_bytes()
        direct = tmp_path / f"direct-{index}"
        run_initialization(path, direct, ticks=8)
        for name in ("initialization.json", "events.jsonl", "state.json"):
            assert (destination / name).read_bytes() == (direct / name).read_bytes()
        if path == observed:
            for name in ("observer.json", "observations.json"):
                assert (destination / name).read_bytes() == (direct / name).read_bytes()
        assert (destination / "events.jsonl").stat().st_size > 0
        left, right = [json.loads((p / "run.json").read_text()) for p in (destination, direct)]
        left.pop("elapsed_seconds")
        right.pop("elapsed_seconds")
        assert left == right
        assert not list(destination.glob("*.html")) and not list(destination.glob("*.gif"))
    cleanup = cleanup_expired(tmp_path, now=time.time() + 86410)
    assert not cleanup["errors"]
    assert not (batch / "inputs").exists() and not (batch / "batch.json").exists()
    assert all(path.exists() for path in paths)


def test_worker_failure_keeps_partial_evidence_and_other_run_completes(tmp_path):
    raw = json.loads((ROOT / "examples/basic.json").read_text())
    # Valid input requests a result outside the bounded physical payload.
    raw["disturbance_types"][0]["updates"] = [
        {"field": "velocity", "expression": {"op": "mul", "args": [{"field": "velocity"}, 1073741823]}}
    ]
    bad = tmp_path / "bad.json"
    bad.write_text(json.dumps(raw))
    output = tmp_path / "failed-batch"
    result = json.loads(
        run_batch([bad, ROOT / "examples/basic.json"], output, workers=1, ticks=2).read_text()
    )
    assert result["status"] == "failed"
    assert [job["status"] for job in result["jobs"]] == ["failed", "completed"]
    failed = json.loads((output / "run-0000/run.json").read_text())
    assert failed["status"] == "failed" and failed["error"]
    assert (output / "run-0000/events.jsonl").is_file()
    assert (output / "run-0000/state.json").is_file()


@pytest.mark.parametrize("kwargs", [{"workers": 0}, {"workers": True}, {"ticks": -1}])
def test_invalid_batch_options_fail_before_creating_output(tmp_path, kwargs):
    output = tmp_path / "result"
    with pytest.raises(ValueError):
        run_batch([ROOT / "examples/basic.json"], output, **kwargs)
    assert not output.exists()


def test_all_inputs_validate_before_dispatch_and_existing_output_is_preserved(tmp_path):
    output = tmp_path / "result"
    bad = tmp_path / "invalid.json"
    bad.write_text("{}")
    with pytest.raises(ValueError):
        run_batch([ROOT / "examples/basic.json", bad], output)
    assert not output.exists()
    output.mkdir()
    existing = output / "keep.json"
    existing.write_text("original")
    with pytest.raises(ValueError, match="empty batch output"):
        run_batch([ROOT / "examples/basic.json"], output)
    assert list(output.iterdir()) == [existing] and existing.read_text() == "original"


def test_batch_cli_uses_runtime_inputs_without_building(tmp_path):
    output = tmp_path / "cli"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "event_universe.batch",
            "--init",
            str(ROOT / "examples/basic.json"),
            "--output",
            str(output),
            "--workers",
            "1",
            "--ticks",
            "1",
        ],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((output / "batch.json").read_text())
    assert report["status"] == "completed" and report["ticks_override"] == 1


def test_inputs_are_frozen_before_workers_start(tmp_path, monkeypatch):
    original = tmp_path / "source.json"
    source = (ROOT / "examples/basic.json").read_bytes()
    original.write_bytes(source)
    pool = batch_module.ProcessPoolExecutor

    def edit_original(**kwargs):
        original.write_text("{}")
        return pool(**kwargs)

    monkeypatch.setattr(batch_module, "ProcessPoolExecutor", edit_original)
    output = tmp_path / "frozen"
    result = json.loads(run_batch([original], output, workers=1, ticks=1).read_text())
    assert result["status"] == "completed" and original.read_text() == "{}"
    assert (output / "run-0000/initialization.json").read_bytes() == source


def test_interrupted_batch_joins_only_its_workers_and_releases_leases(tmp_path, monkeypatch):
    original_children = {child.pid for child in multiprocessing.active_children()}

    def interrupt_after_dispatch(futures):
        assert futures
        raise KeyboardInterrupt

    monkeypatch.setattr(batch_module, "as_completed", interrupt_after_dispatch)
    output = tmp_path / "interrupted"
    with pytest.raises(KeyboardInterrupt):
        run_batch([ROOT / "examples/basic.json"] * 2, output, workers=2, ticks=10000)
    assert {child.pid for child in multiprocessing.active_children()} <= original_children
    report = json.loads((output / "batch.json").read_text())
    assert report["status"] == "interrupted"
    assert all(job["status"] == "interrupted" for job in report["jobs"])
    cleanup = cleanup_expired(tmp_path, now=time.time() + 86410)
    assert not cleanup["errors"] and not cleanup["skipped"]


def test_pool_startup_failure_is_terminal_and_keeps_frozen_inputs(tmp_path, monkeypatch):
    def unavailable(**kwargs):
        raise OSError("worker pool creation unavailable")

    monkeypatch.setattr(batch_module, "ProcessPoolExecutor", unavailable)
    output = tmp_path / "startup-failed"
    with pytest.raises(OSError, match="worker pool creation unavailable"):
        run_batch([ROOT / "examples/basic.json"], output, workers=1, ticks=1)
    report = json.loads((output / "batch.json").read_text())
    assert report["status"] == report["jobs"][0]["status"] == "failed"
    assert "worker pool creation unavailable" in report["jobs"][0]["error"]
    assert (output / "inputs/0000.json").is_file()


def test_batch_dispatch_keeps_only_a_window_of_futures(tmp_path, monkeypatch):
    from concurrent.futures import Future

    outstanding = set()
    peak = 0
    submitted = 0

    class Pool:
        def __init__(self, **kwargs):
            assert kwargs["max_workers"] == 2

        def submit(self, fn, source, destination, ticks):
            nonlocal peak, submitted
            assert len(outstanding) < 4, "all jobs were retained instead of a bounded window"
            future = Future()
            future.set_result({"status": "completed", "error": None, "worker_pid": 42})
            outstanding.add(future)
            submitted += 1
            peak = max(peak, len(outstanding))
            return future

        def shutdown(self, **kwargs):
            assert not outstanding

        def terminate_workers(self):
            outstanding.clear()

    def completed(futures):
        future = next(iter(futures))
        outstanding.remove(future)
        yield future

    monkeypatch.setattr(batch_module, "ProcessPoolExecutor", Pool)
    monkeypatch.setattr(batch_module, "as_completed", completed)
    output = tmp_path / "window"
    result = json.loads(
        run_batch([ROOT / "examples/basic.json"] * 20, output, workers=2, ticks=0).read_text()
    )
    assert submitted == 20 and peak == 4
    assert [job["index"] for job in result["jobs"]] == list(range(20))
    assert result["status"] == "completed"


def test_invalid_late_input_keeps_output_uncreated(tmp_path):
    invalid = tmp_path / "invalid.json"
    invalid.write_text("{}")
    output = tmp_path / "no-partial-batch"
    with pytest.raises(ValueError):
        run_batch([ROOT / "examples/basic.json", invalid], output, workers=1)
    assert not output.exists()
