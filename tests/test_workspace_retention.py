"""Workspace retention follows process/file ownership without aging user templates."""

import http.client
import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from event_universe import ui
from event_universe.retention import ArtifactLease, cleanup_expired

ROOT = Path(__file__).resolve().parents[1]
DAY = 24 * 60 * 60


class Child:
    """A controlled child with a separately owned runner output directory."""

    def __init__(self, command, *, stdout, **kwargs):
        self.returncode = None
        self.log = stdout
        self.output = Path(command[command.index("--output") + 1])
        self.output.mkdir(parents=True)
        self.lease = ArtifactLease(self.output.parent, [self.output])
        (self.output / "state.json").write_text("{}", encoding="utf-8")
        self.terminated = False
        self.killed = False
        self.timeout_once = False

    def poll(self):
        return self.returncode

    def complete(self, code=0):
        self.returncode = code
        self.lease.finish()

    def terminate(self):
        self.terminated = True

    def kill(self):
        self.killed = True

    def wait(self, timeout=None):
        if self.timeout_once:
            self.timeout_once = False
            raise subprocess.TimeoutExpired("controlled child", timeout)
        self.complete(-15)
        return self.returncode


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    # Put originals inside the scanned root to prove only registered outputs expire.
    configs = tmp_path / "templates"
    configs.mkdir()
    source = (ROOT / "examples/basic.json").read_bytes()
    (configs / "original.json").write_bytes(source)
    monkeypatch.setattr(ui.subprocess, "Popen", Child)
    workspace = ui.Workspace(configs, tmp_path)
    yield workspace
    workspace.close()


def start(workspace):
    source = (workspace.configs / "original.json").read_text(encoding="utf-8")
    description = workspace.start(source, False, 1)
    return workspace.jobs[description["id"]]


def get(server, path):
    connection = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=3)
    try:
        connection.request("GET", path)
        response = connection.getresponse()
        return response.status, response.read()
    finally:
        connection.close()


def test_export_expires_after_one_day_and_original_template_survives(workspace):
    original = workspace.configs / "original.json"
    source = original.read_text(encoding="utf-8")
    created = time.time()
    exported = workspace.export(source)
    path, _ = next(iter(workspace.exports.values()))
    assert path.read_text(encoding="utf-8") == source

    workspace.cleanup(now=created + DAY - 1)
    assert path.is_file() and workspace.exports
    workspace.cleanup(now=time.time() + DAY + 1)
    assert not path.exists() and not workspace.exports
    assert original.read_text(encoding="utf-8") == source
    assert workspace.templates()[0]["source"] == source
    assert exported["url"].startswith("/exports/")


def test_active_job_preserves_its_inputs_log_and_independent_child_output(workspace):
    job = start(workspace)
    inputs = (job.initialization, Path(job.log.name))
    workspace.cleanup(now=time.time() + 3 * DAY)
    assert all(path.is_file() for path in inputs)
    assert (job.output / "state.json").is_file()
    assert not job.log.closed and job.state == "running"
    assert workspace.jobs == {job.identifier: job}


def test_orphaned_child_keeps_inputs_and_log_until_its_lease_and_last_write_expire(workspace):
    job = start(workspace)
    log_path = Path(job.log.name)
    # Losing the parent releases its OS lock without recording normal completion.
    job.log.close()
    job.lease._lock.close()
    workspace.jobs.clear()
    future = time.time() + 3 * DAY
    try:
        report = cleanup_expired(workspace.output, now=future)
        assert not report["errors"]
        assert job.initialization.is_file() and log_path.is_file()
        assert (job.output / "state.json").is_file()

        # The surviving child can write its inherited log after the parent is gone.
        log_path.write_text("final child output", encoding="utf-8")
        os.utime(log_path, (future, future))
        job.process.complete()
        report = cleanup_expired(workspace.output, now=future + DAY - 1)
        assert not report["errors"]
        assert job.initialization.is_file()
        assert log_path.read_text(encoding="utf-8") == "final child output"

        report = cleanup_expired(workspace.output, now=future + DAY + 1)
        assert not report["errors"]
        assert not job.initialization.exists() and not log_path.exists()
        assert not job.output.exists()
        assert (workspace.configs / "original.json").is_file()
    finally:
        job.process.complete()


@pytest.mark.parametrize("exit_code, state", [(0, "completed"), (1, "failed")])
def test_completed_or_failed_job_releases_all_owned_files_for_expiry(workspace, exit_code, state):
    job = start(workspace)
    job.process.complete(exit_code)
    workspace.cleanup()
    assert job.log.closed and job.state == state
    assert job.identifier in workspace.jobs
    workspace.cleanup(now=time.time() + DAY + 1)
    assert not job.initialization.exists()
    assert not Path(job.log.name).exists()
    assert not job.output.exists()
    assert job.identifier not in workspace.jobs
    assert (workspace.configs / "original.json").is_file()


@pytest.mark.parametrize("kill_required", [False, True])
def test_shutdown_reaps_child_and_closes_log_before_releasing_input_lease(
    workspace, monkeypatch, kill_required
):
    job = start(workspace)
    job.process.timeout_once = kill_required
    original_finish = job.lease.finish
    releases = []

    def finish():
        releases.append((job.process.poll(), job.log.closed))
        original_finish()

    monkeypatch.setattr(job.lease, "finish", finish)
    server = ui.WorkspaceServer(workspace, 0)
    server.server_close()
    assert job.state == "cancelled"
    assert job.process.terminated and job.process.killed == kill_required
    assert releases and all(code is not None and closed for code, closed in releases)
    workspace.cleanup(now=time.time() + DAY + 1)
    assert not job.initialization.exists() and not job.output.exists()


def test_spawn_failure_closes_log_and_releases_registered_inputs(workspace, monkeypatch):
    logs = []

    def fail(command, *, stdout, **kwargs):
        logs.append(stdout)
        raise OSError("controlled spawn failure")

    monkeypatch.setattr(ui.subprocess, "Popen", fail)
    with pytest.raises(OSError, match="controlled spawn failure"):
        start(workspace)
    assert logs[0].closed and not workspace.jobs
    assert len(list((workspace.output / "inputs").glob("*"))) == 2
    workspace.cleanup(now=time.time() + DAY + 1)
    assert not list((workspace.output / "inputs").glob("*"))
    assert (workspace.configs / "original.json").is_file()


def test_config_write_failure_closes_log_and_releases_registered_inputs(workspace, monkeypatch):
    write = Path.write_bytes

    def fail(path, data):
        if path.parent.name == "inputs":
            raise OSError("controlled input write failure")
        return write(path, data)

    monkeypatch.setattr(Path, "write_bytes", fail)
    with pytest.raises(OSError, match="controlled input write failure"):
        start(workspace)
    assert not workspace.jobs
    workspace.cleanup(now=time.time() + DAY + 1)
    assert not list((workspace.output / "inputs").glob("*"))


def test_input_lease_stays_active_when_a_finished_jobs_log_cannot_close(workspace):
    job = start(workspace)
    writer = job.log

    class UnclosedLog:
        name = writer.name
        closed = False

        def close(self):
            raise OSError("controlled close failure")

    job.log = UnclosedLog()
    job.process.complete()
    try:
        with pytest.raises(OSError, match="controlled close failure"):
            job.refresh()
        cleanup_expired(workspace.output, now=time.time() + DAY + 1)
        assert job.initialization.is_file() and Path(writer.name).is_file()
    finally:
        job.log = writer
    job.refresh()
    workspace.cleanup(now=time.time() + DAY + 1)
    assert not job.initialization.exists() and writer.closed


def test_service_actions_refresh_jobs_then_clean_up_without_http_polling(workspace, monkeypatch):
    job = start(workspace)
    job.process.complete()
    calls = []

    def cleanup(root, **kwargs):
        calls.append((root, job.state, job.log.closed))
        return {}

    monkeypatch.setattr(ui, "cleanup_expired", cleanup)
    clock = [10.0]
    monkeypatch.setattr(ui.time, "monotonic", lambda: clock[0])
    server = ui.WorkspaceServer(workspace, 0)
    try:
        server.service_actions()
        server.service_actions()
        assert calls == [(workspace.output, "completed", True)]
        clock[0] += ui.CLEANUP_INTERVAL_SECONDS
        server.service_actions()
        assert len(calls) == 2
    finally:
        server.server_close()


def test_expired_run_and_export_links_return_404_and_templates_still_load(workspace, monkeypatch):
    job = start(workspace)
    job.process.complete()
    job.refresh()
    source = (workspace.configs / "original.json").read_text(encoding="utf-8")
    exported = workspace.export(source)
    clock = [time.time()]

    def cleanup(root, **kwargs):
        return cleanup_expired(root, now=clock[0])

    monkeypatch.setattr(ui, "cleanup_expired", cleanup)
    server = ui.WorkspaceServer(workspace, 0)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        assert get(server, exported["url"])[0] == 200
        assert get(server, f"/runs/{job.identifier}/state.json")[0] == 200
        clock[0] += DAY + 1
        assert get(server, exported["url"])[0] == 404
        assert get(server, f"/runs/{job.identifier}/state.json")[0] == 404
        assert get(server, f"/api/runs/{job.identifier}")[0] == 404
        assert json.loads(get(server, "/api/runs")[1]) == {"runs": []}
        templates = json.loads(get(server, "/api/templates")[1])["templates"]
        assert templates[0]["source"] == source
    finally:
        server.shutdown()
        thread.join(timeout=3)
        server.server_close()


def test_cleanup_does_not_create_an_output_root_for_an_unused_workspace(tmp_path):
    workspace = ui.Workspace(ROOT / "examples", tmp_path / "absent")
    workspace.cleanup()
    assert not workspace.output.exists()


def directory_link(alias, target):
    try:
        alias.symlink_to(target, target_is_directory=True)
    except OSError:
        if sys.platform != "win32":
            raise
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(alias), str(target)], capture_output=True, text=True
        )
        if result.returncode:
            pytest.skip("This host does not permit directory links")


def test_linked_workspace_output_is_rejected_before_resolving_or_creating_files(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    alias = tmp_path / "alias"
    directory_link(alias, outside)
    with pytest.raises(ValueError, match="symlink|reparse"):
        ui.Workspace(ROOT / "examples", alias / "future-workspace")
    assert list(outside.iterdir()) == []


@pytest.mark.parametrize("linked_child", ["inputs", "exports", "runs"])
def test_generated_linked_subdirectories_are_rejected_before_any_write(
    tmp_path, monkeypatch, linked_child
):
    outside = tmp_path / "outside"
    outside.mkdir()
    output = tmp_path / "workspace"
    output.mkdir()
    workspace = ui.Workspace(ROOT / "examples", output)
    directory_link(output / linked_child, outside)
    launched = []
    monkeypatch.setattr(ui.subprocess, "Popen", lambda *args, **kwargs: launched.append(args))
    source = (ROOT / "examples/basic.json").read_text(encoding="utf-8")
    with pytest.raises(ValueError, match="symlink|reparse"):
        if linked_child == "exports":
            workspace.export(source)
        else:
            workspace.start(source, False, 1)
    assert list(outside.iterdir()) == []
    assert [path.name for path in output.iterdir()] == [linked_child]
    assert not workspace.jobs and not workspace.exports and not launched
