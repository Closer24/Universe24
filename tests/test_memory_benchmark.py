"""Memory reporting retains audited results, failures and caller-owned tracing."""

import hashlib
import json
import os
import subprocess
import sys
import tracemalloc
from pathlib import Path
from types import SimpleNamespace

import pytest

from event_universe import Simulation
from event_universe.runner import run_initialization, source_fingerprint
from tools import benchmark_memory

from .test_disturbance_engine import document, kind

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def source(tmp_path):
    path = tmp_path / "initial.json"
    raw = document([kind("resident")], [((0, 0, 0), "resident")], capacity=1)
    raw["ticks"] = 2
    path.write_text(json.dumps(raw), encoding="utf-8")
    return path


@pytest.mark.parametrize("workers,trace_python", [(1, True), (2, False)])
def test_fresh_cli_memory_report_keeps_complete_canonical_artifacts(
    tmp_path, source, workers, trace_python
):
    output, reference = tmp_path / "measured", tmp_path / "reference"
    environment = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONUTF8": "1"}
    result = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools/benchmark_memory.py"),
            "--init",
            str(source),
            "--output",
            str(output),
            "--ticks",
            "2",
            "--workers",
            str(workers),
            "--parallel-threshold",
            "1",
            *(["--trace-python"] if trace_python else []),
        ],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        timeout=45,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    run_initialization(source, reference, ticks=2)
    for name in ("state.json", "events.jsonl", "initialization.json"):
        assert (output / "run" / name).read_bytes() == (reference / name).read_bytes()
    report = json.loads((output / "memory.json").read_text())
    assert report["source_sha256"] == source_fingerprint() == report["source_after_sha256"]
    assert report["source_unchanged"] and report["failure"] is None
    assert report["requested_ticks"] == report["completed_ticks"] == report["tick"] == 2
    assert report["initialization_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert report["execution"]["backend"] == ("serial" if workers == 1 else "interpreters")
    assert report["execution"]["closed"]
    if sys.platform in ("win32", "linux", "darwin"):
        peak = report["process_memory"]["after"]["peak_resident_bytes"]
        assert peak > 0 and peak >= report["process_memory"]["before"]["peak_resident_bytes"]
    if trace_python:
        assert report["python_allocations"]["peak_bytes"] > 0
    else:
        assert report["python_allocations"] is None
    assert not list(output.rglob("*.html")) and not list(output.rglob("*.gif"))


@pytest.mark.parametrize(
    "options",
    [
        {"workers": 0},
        {"workers": True},
        {"parallel_threshold": 0},
        {"chunk_size": 0},
        {"ticks": -1},
        {"ticks": True},
        {"workers": 2, "trace_python": True},
    ],
)
def test_invalid_memory_options_fail_before_writes_or_tracing(tmp_path, source, options):
    output = tmp_path / "invalid"
    tracing = tracemalloc.is_tracing()
    with pytest.raises(ValueError):
        benchmark_memory.benchmark(source, output, **options)
    assert not output.exists()
    assert tracemalloc.is_tracing() == tracing


def test_memory_tool_rejects_protected_and_nonempty_outputs(tmp_path, source):
    with pytest.raises(ValueError):
        benchmark_memory.benchmark(source, ROOT / "src")
    output = tmp_path / "occupied"
    output.mkdir()
    preserved = output / "original.txt"
    preserved.write_text("keep", encoding="utf-8")
    with pytest.raises(ValueError, match="must be empty"):
        benchmark_memory.benchmark(source, output)
    assert source.exists() and preserved.read_text() == "keep"


def test_failed_run_preserves_memory_and_physical_evidence_and_stops_owned_tracer(
    tmp_path, source, monkeypatch
):
    if tracemalloc.is_tracing():
        pytest.skip("this ownership case requires no external allocation tracer")
    original = Simulation.step

    def failed_step(world):
        original(world)
        raise ValueError("memory fixture stopped after committed tick")

    monkeypatch.setattr(Simulation, "step", failed_step)
    output = tmp_path / "failed"
    with pytest.raises(ValueError, match="memory fixture stopped"):
        benchmark_memory.benchmark(source, output, trace_python=True)
    assert not tracemalloc.is_tracing()
    report = json.loads((output / "memory.json").read_text())
    assert report["failure"]["type"] == "ValueError"
    assert report["run_status"] == "failed" and report["execution"]["closed"]
    assert report["python_allocations"]["peak_bytes"] > 0
    assert json.loads((output / "run/run.json").read_text())["tick"] == 1
    assert (output / "run/state.json").is_file()
    assert (output / "run/events.jsonl").stat().st_size > 0


@pytest.mark.parametrize("options", [{"trace_python": True}, {"workers": 2}])
def test_existing_allocation_tracer_is_not_reset_or_stopped(tmp_path, source, options):
    already_tracing = tracemalloc.is_tracing()
    if not already_tracing:
        tracemalloc.start()
    try:
        retained = bytearray(10000)
        before = tracemalloc.get_traced_memory()[1]
        output = tmp_path / "borrowed"
        with pytest.raises(ValueError, match="already active"):
            benchmark_memory.benchmark(source, output, **options)
        assert tracemalloc.is_tracing() and tracemalloc.get_traced_memory()[1] >= before
        assert not output.exists() and len(retained) == 10000
    finally:
        if not already_tracing:
            tracemalloc.stop()


def test_changed_source_is_reported_and_rejected(tmp_path, source, monkeypatch):
    fingerprints = iter(("before", "after"))
    monkeypatch.setattr(benchmark_memory, "source_fingerprint", lambda: next(fingerprints))
    output = tmp_path / "changed"
    with pytest.raises(RuntimeError, match="source changed"):
        benchmark_memory.benchmark(source, output)
    report = json.loads((output / "memory.json").read_text())
    assert not report["source_unchanged"]
    assert report["failure"]["type"] == "RuntimeError"
    assert (output / "run/state.json").is_file()


@pytest.mark.parametrize("platform,expected", [("linux", 123 * 1024), ("darwin", 123), ("other", None)])
def test_os_peak_units_are_platform_specific(monkeypatch, platform, expected):
    resource = SimpleNamespace(RUSAGE_SELF=0, getrusage=lambda who: SimpleNamespace(ru_maxrss=123))
    monkeypatch.setitem(sys.modules, "resource", resource)
    monkeypatch.setattr(sys, "platform", platform)
    assert benchmark_memory.process_memory()["peak_resident_bytes"] == expected
