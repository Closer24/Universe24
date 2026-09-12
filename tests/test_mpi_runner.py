"""Static MPI workers preserve one world's outputs and exit after local failures."""

import importlib.util
import json
import os
import shutil
import signal
import subprocess
import sys
from concurrent.futures import Executor
from contextlib import contextmanager
from pathlib import Path

import pytest

from event_universe import mpi_runner
from event_universe.runner import run_initialization

from .test_parallel_execution import failing_document, moving_document

ROOT = Path(__file__).resolve().parents[1]


class Coordinator:
    def Get_rank(self):
        return 0

    def Get_size(self):
        return 3


def test_unused_collective_is_closed_after_preflight_failure():
    events = []

    @contextmanager
    def context(communicator, **options):
        events.append(("enter", options))
        try:
            yield Executor()
        finally:
            events.append(("exit", options))

    execution = mpi_runner.MPIExecution(Coordinator(), context)
    execution.close()
    execution.close()
    assert events == [("enter", {"root": 0}), ("exit", {"root": 0})]


def test_executor_bootstrap_uses_the_actual_composed_planner(monkeypatch):
    planner = object()
    observed = []
    executor = Executor()

    def initializer(value):
        assert value is planner
        observed.append("planner")
        return print, ("immutable bootstrap",)

    @contextmanager
    def context(communicator, **options):
        assert options == {"root": 0, "initializer": print, "initargs": ("immutable bootstrap",)}
        observed.append("enter")
        yield executor
        observed.append("exit")

    monkeypatch.setattr(mpi_runner, "worker_initializer", initializer)
    execution = mpi_runner.MPIExecution(Coordinator(), context)
    assert execution(planner) is executor
    with pytest.raises(RuntimeError, match="one simulation"):
        execution(planner)
    execution.close()
    assert observed == ["planner", "enter", "exit"]


def _environment():
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(ROOT / "src")
    environment["PYTHONUTF8"] = "1"
    return environment


def _run_bounded(command, *, timeout=30, environment=None):
    settings = (
        {"creationflags": subprocess.CREATE_NO_WINDOW}
        if os.name == "nt"
        else {"start_new_session": True}
    )
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        env=_environment() if environment is None else environment,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        **settings,
    )
    try:
        output, error = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                check=False,
                capture_output=True,
                **settings,
            )
        else:
            os.killpg(process.pid, signal.SIGKILL)
        output, error = process.communicate(timeout=5)
        pytest.fail(f"MPI process tree exceeded {timeout} seconds:\n{output}\n{error}")
    return subprocess.CompletedProcess(command, process.returncode, output, error)


def test_ordinary_import_does_not_require_or_initialize_mpi():
    result = _run_bounded(
        [
            sys.executable,
            "-c",
            "import sys; import event_universe; import event_universe.mpi_runner; "
            "assert not any(name.startswith('mpi4py') for name in sys.modules)",
        ]
    )
    assert result.returncode == 0, result.stderr


@pytest.fixture
def mpi_command():
    if importlib.util.find_spec("mpi4py") is None:
        pytest.skip("optional mpi4py dependency is not installed")
    launcher = shutil.which("mpiexec")
    if launcher is None:
        candidate = Path(sys.prefix) / "Library" / "bin" / "mpiexec.exe"
        if candidate.is_file():
            launcher = str(candidate)
    if launcher is None:
        pytest.skip("no MPI launcher is installed")
    local = ["-localonly"] if os.name == "nt" else []
    return [launcher, *local, "-n", "3", sys.executable, "-m", "event_universe.mpi_runner"]


@pytest.mark.parametrize(
    "scenario", ["moving", "rational", "rational_wide", "rational_overflow", "failure"]
)
def test_static_mpi_run_matches_serial_physical_outputs(tmp_path, mpi_command, scenario):
    raw = moving_document(budget=3, travel=2) if scenario == "moving" else failing_document()
    if scenario.startswith("rational"):
        raw["normal_budget"] = 100_000_000
        raw["disturbance_types"][0]["updates"][0]["expression"] = {
            "op": "rational_whole",
            "args": [_rational_expression(scenario)],
        }
        raw["seeds"] = [{"position": [i, 0, 0], "type": "counter"} for i in range(32)]
    path = tmp_path / "input.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    serial, parallel = tmp_path / "serial", tmp_path / "mpi"
    fails = scenario in {"failure", "rational_overflow"}
    if fails:
        error_type = OverflowError if scenario == "rational_overflow" else ValueError
        with pytest.raises(error_type, match="bound"):
            run_initialization(path, serial, ticks=12)
    else:
        run_initialization(path, serial, ticks=12)
    result = _run_bounded(
        [
            *mpi_command,
            "--init",
            str(path),
            "--output",
            str(parallel),
            "--ticks",
            "12",
            "--parallel-threshold",
            "1",
            "--chunk-size",
            "1",
        ]
    )
    assert result.returncode == (1 if fails else 0), result.stderr
    for name in ("initialization.json", "state.json", "events.jsonl"):
        assert (serial / name).read_bytes() == (parallel / name).read_bytes(), name
    metadata = [json.loads((output / "run.json").read_text()) for output in (serial, parallel)]
    execution = metadata[1]["execution"]
    assert execution["backend"] == "mpi"
    assert execution["evaluated_proposals"] > 0
    assert execution["closed"] and not execution["owns_executor"]
    if scenario == "rational":
        assert len({item["process"] for item in execution["workers_used"]}) == 2
    for item in metadata:
        item.pop("elapsed_seconds")
        item.pop("execution")
    assert metadata[0] == metadata[1]


def _rational_expression(scenario):
    def operation(name, *args):
        return {"op": name, "args": list(args)}

    if scenario == "rational":
        return operation("ratio", -7, 3)
    # Every configured literal fits a physical component. Rational intermediates
    # reach 120 magnitude bits; multiplying these reduced ratios reaches 240.
    maximum = (1 << 30) - 1
    square = operation("mul", maximum, maximum)
    wide = operation("mul", square, square)
    if scenario == "rational_overflow":
        return operation("mul", wide, maximum)
    previous = operation("sub", wide, 1)
    return operation("mul", operation("ratio", wide, previous), operation("ratio", previous, wide))


def test_two_ranks_execute_proposals_on_the_one_worker(tmp_path, mpi_command):
    path, output = tmp_path / "input.json", tmp_path / "output"
    path.write_text(json.dumps(moving_document()), encoding="utf-8")
    command = list(mpi_command)
    command[command.index("-n") + 1] = "2"
    result = _run_bounded(
        [
            *command,
            "--init",
            str(path),
            "--output",
            str(output),
            "--ticks",
            "2",
            "--parallel-threshold",
            "1",
            "--chunk-size",
            "1",
        ]
    )
    assert result.returncode == 0, result.stderr
    report = json.loads((output / "run.json").read_text())["execution"]
    assert report["backend"] == "mpi"
    assert report["evaluated_proposals"] > 0
    assert len(report["workers_used"]) == 1


def test_workers_pin_coordinator_source_and_use_the_one_frozen_input(tmp_path, mpi_command):
    alternate = tmp_path / "alternate"
    package = alternate / "event_universe"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("raise RuntimeError('wrong package imported')\n")
    path = tmp_path / "input.json"
    original = json.dumps(moving_document()).encode()
    path.write_bytes(original)
    serial, parallel = tmp_path / "serial", tmp_path / "mpi"
    run_initialization(path, serial, ticks=3)
    program = tmp_path / "launch.py"
    program.write_text(
        "\n".join(
            [
                "import sys",
                "from pathlib import Path",
                "from mpi4py import MPI",
                "from mpi4py.futures import MPICommExecutor",
                "if MPI.COMM_WORLD.Get_rank() == 0:",
                "    sys.path.insert(0, sys.argv[1])",
                "    from event_universe import mpi_runner",
                "    factory = mpi_runner.MPIExecution.__call__",
                "    def change_after_parse(self, planner):",
                "        Path(sys.argv[2]).write_text('{}')",
                "        return factory(self, planner)",
                "    mpi_runner.MPIExecution.__call__ = change_after_parse",
                "    mpi_runner.main(['--init', sys.argv[2], '--output', sys.argv[3],",
                "                     '--ticks', '3', '--parallel-threshold', '1', '--chunk-size', '1'])",
                "else:",
                "    with MPICommExecutor(MPI.COMM_WORLD, root=0):",
                "        pass",
            ]
        ),
        encoding="utf-8",
    )
    environment = {**_environment(), "PYTHONPATH": str(alternate)}
    result = _run_bounded(
        [*mpi_command[:-2], str(program), str(ROOT / "src"), str(path), str(parallel)],
        environment=environment,
    )
    assert result.returncode == 0, result.stderr
    assert path.read_text() == "{}"
    assert (parallel / "initialization.json").read_bytes() == original
    for name in ("state.json", "events.jsonl"):
        assert (serial / name).read_bytes() == (parallel / name).read_bytes()
    reports = [json.loads((output / "run.json").read_text()) for output in (serial, parallel)]
    assert reports[0]["source_sha256"] == reports[1]["source_sha256"]
    assert reports[1]["execution"]["evaluated_proposals"] > 0


@pytest.mark.parametrize("failure", ["missing", "invalid", "occupied", "arguments"])
def test_preflight_errors_release_all_prelaunched_workers(tmp_path, mpi_command, failure):
    path, output = tmp_path / "input.json", tmp_path / "output"
    if failure != "missing":
        path.write_text(
            "{}" if failure == "invalid" else json.dumps(moving_document()), encoding="utf-8"
        )
    if failure == "occupied":
        output.mkdir()
        (output / "preserved.txt").write_text("keep")
    arguments = [] if failure == "arguments" else ["--init", str(path), "--output", str(output)]
    result = _run_bounded([*mpi_command, *arguments])
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
    if failure == "occupied":
        assert sorted(p.name for p in output.iterdir()) == ["preserved.txt"]
    else:
        assert not output.exists()
