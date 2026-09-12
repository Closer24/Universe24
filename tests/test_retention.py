"""Artifact expiry cannot remove active writers, replacement paths or source files."""

import json
import os
import subprocess
import sys
import threading
import time
from pathlib import Path

import pytest

from event_universe import retention
from event_universe.retention import (
    MAX_AGE_SECONDS,
    REGISTRY,
    ArtifactLease,
    _catalog,
    cleanup_expired,
    validate_output_path,
    watcher_lock,
)
from event_universe.retention import (
    adopt_artifacts as register_artifacts,
)


def generated(root, name="result.json"):
    root.mkdir(parents=True, exist_ok=True)
    path = root / name
    path.write_text("generated result", encoding="utf-8")
    return path


def records(root):
    return [json.loads(path.read_text()) for path in (root / REGISTRY).glob("*.json")]


def adopt_artifacts(root, paths, finished_at):
    """Give historical fixture outputs their actual historical write timestamps."""
    for value in paths:
        path = value if value.is_absolute() else root / value
        descendants = list(path.rglob("*")) if path.is_dir() else []
        for owned in [*descendants, path]:
            os.utime(owned, (finished_at, finished_at))
    register_artifacts(root, paths, finished_at)


def child_environment():
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(Path(__file__).resolve().parents[1] / "src")
    environment["PYTHONUTF8"] = "1"
    return environment


@pytest.mark.parametrize(
    "age,deleted", [(MAX_AGE_SECONDS - 1, False), (MAX_AGE_SECONDS, True), (MAX_AGE_SECONDS + 1, True)]
)
def test_finished_artifacts_expire_at_exact_deadline(tmp_path, age, deleted):
    target = generated(tmp_path)
    adopt_artifacts(tmp_path, [target], finished_at=100)
    report = cleanup_expired(tmp_path, now=100 + age)
    assert report["errors"] == []
    assert target.exists() is not deleted
    assert report["deleted"] == ([str(target)] if deleted else [])
    assert report["next_expiry"] == (None if deleted else 100 + MAX_AGE_SECONDS)


def test_dry_run_reports_expired_paths_without_changing_any_artifact(tmp_path):
    target = generated(tmp_path)
    adopt_artifacts(tmp_path, [target], finished_at=100)
    before = records(tmp_path)
    report = cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS, dry_run=True)
    assert report["deleted"] == [str(target)]
    assert target.exists() and records(tmp_path) == before


@pytest.mark.parametrize("failed", [False, True])
def test_context_exit_finishes_success_and_failure_with_idempotent_close(tmp_path, failed):
    target = generated(tmp_path)
    lease = ArtifactLease(tmp_path, [target])
    assert records(tmp_path)[0]["finished_at"] is None
    try:
        with lease:
            if failed:
                raise RuntimeError("simulated failure")
    except RuntimeError:
        assert failed
    entry = records(tmp_path)[0]
    assert entry["expires_at"] == entry["finished_at"] + MAX_AGE_SECONDS
    lease.finish()
    lease.close()
    assert records(tmp_path)[0] == entry
    assert cleanup_expired(tmp_path, now=entry["expires_at"])["deleted"] == [str(target)]


def test_constructor_protects_writer_even_without_entering_context(tmp_path):
    target = generated(tmp_path)
    lease = ArtifactLease(tmp_path, [target])
    try:
        report = cleanup_expired(tmp_path, now=time.time() + 3 * MAX_AGE_SECONDS)
        assert report["deleted"] == [] and target.exists()
        assert any(item["reason"] == "active writer" for item in report["skipped"])
        with pytest.raises(RuntimeError, match="active writer"):
            ArtifactLease(tmp_path, [target])
        with pytest.raises(RuntimeError, match="active writer"):
            adopt_artifacts(tmp_path, [target], finished_at=100)
    finally:
        lease.finish()


def test_live_writer_is_protected_across_processes(tmp_path):
    target = generated(tmp_path)
    code = (
        "import sys; from pathlib import Path; "
        "from event_universe.retention import ArtifactLease; "
        "lease=ArtifactLease(Path(sys.argv[1]), [Path(sys.argv[2])]); "
        "print('ready', flush=True); sys.stdin.read(); lease.finish()"
    )
    child = subprocess.Popen(
        [sys.executable, "-c", code, str(tmp_path), str(target)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=child_environment(),
    )
    try:
        assert child.stdout.readline().strip() == "ready"
        report = cleanup_expired(tmp_path, now=time.time() + 3 * MAX_AGE_SECONDS)
        assert target.exists() and report["deleted"] == []
        assert report["skipped"] and not report["errors"]
    finally:
        child.communicate(timeout=10)
    assert child.returncode == 0


def test_start_waits_for_brief_catalog_contention_without_failing(tmp_path):
    target = generated(tmp_path)
    started, acquired = threading.Event(), threading.Event()
    failures = []

    def writer():
        started.set()
        try:
            with ArtifactLease(tmp_path, [target]):
                acquired.set()
        except Exception as error:
            failures.append(error)

    with _catalog(tmp_path):
        thread = threading.Thread(target=writer)
        thread.start()
        assert started.wait(1)
        assert not acquired.wait(0.05)
        assert not failures
    thread.join(timeout=3)
    assert not thread.is_alive() and acquired.is_set() and failures == []


def test_crashed_unlocked_writer_expires_from_its_latest_actual_write(tmp_path):
    target = generated(tmp_path)
    code = (
        "import os,sys; from pathlib import Path; "
        "from event_universe.retention import ArtifactLease; "
        "lease=ArtifactLease(Path(sys.argv[1]), [Path(sys.argv[2])]); "
        "Path(sys.argv[2]).write_text('partial run'); os._exit(0)"
    )
    subprocess.run(
        [sys.executable, "-c", code, str(tmp_path), str(target)], check=True, env=child_environment()
    )
    entry = records(tmp_path)[0]
    assert entry["finished_at"] is None
    last_write = entry["started_at"] + 600
    os.utime(target, (last_write, last_write))
    early = cleanup_expired(tmp_path, now=entry["started_at"] + MAX_AGE_SECONDS + 1)
    assert early["deleted"] == [] and target.exists()
    assert cleanup_expired(tmp_path, now=last_write + MAX_AGE_SECONDS)["deleted"] == [str(target)]


def test_orphaned_companions_remain_while_nested_child_writer_is_active(tmp_path):
    companion = generated(tmp_path, "input.json")
    destination = tmp_path / "runs" / "child"
    parent = ArtifactLease(tmp_path, [companion], keep_alive_with=[destination])
    parent._lock.close()  # Simulate the parent process exiting without finishing.
    generated(destination)
    child = ArtifactLease(destination.parent, [destination])
    future = time.time() + 2 * MAX_AGE_SECONDS
    try:
        report = cleanup_expired(tmp_path, now=future)
        assert not report["errors"] and not report["deleted"]
        assert companion.exists() and destination.exists()
        assert any(item["reason"] == "active dependency writer" for item in report["skipped"])
    finally:
        child.finish()
    report = cleanup_expired(tmp_path, now=future)
    assert not report["errors"]
    assert set(report["deleted"]) == {str(companion), str(destination)}


def test_prospective_dependency_without_a_writer_does_not_extend_expiry(tmp_path):
    companion = generated(tmp_path)
    lease = ArtifactLease(tmp_path, [companion], keep_alive_with=[Path("runs/future")])
    lease.finish()
    report = cleanup_expired(tmp_path, now=time.time() + 2 * MAX_AGE_SECONDS)
    assert not report["errors"] and report["deleted"] == [str(companion)]


@pytest.mark.parametrize("dependency", ["../outside", "src/result", ".event-universe-retention"])
def test_dependency_paths_cannot_escape_or_reference_protected_content(tmp_path, dependency):
    companion = generated(tmp_path)
    with pytest.raises(ValueError):
        ArtifactLease(tmp_path, [companion], keep_alive_with=[Path(dependency)])
    assert companion.exists() and not (tmp_path / REGISTRY).exists()


def test_only_registered_files_are_removed_and_original_configuration_survives(tmp_path):
    target = generated(tmp_path)
    original = generated(tmp_path, "original-configuration.json")
    arbitrary = generated(tmp_path, "notes.txt")
    adopt_artifacts(tmp_path, [Path("result.json")], finished_at=100)
    cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)
    assert not target.exists()
    assert original.read_text() == arbitrary.read_text() == "generated result"


def test_owned_directory_includes_generated_children_but_not_siblings(tmp_path):
    output = tmp_path / "run"
    generated(output)
    sibling = generated(tmp_path, "keep.json")
    adopt_artifacts(tmp_path, [output], finished_at=100)
    assert cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)["deleted"] == [str(output)]
    assert not output.exists() and sibling.exists()


def test_legitimate_path_reuse_supersedes_old_inactive_registration(tmp_path):
    target = generated(tmp_path)
    adopt_artifacts(tmp_path, [target], finished_at=100)
    with ArtifactLease(tmp_path, [target]):
        target.write_text("new run")
    report = cleanup_expired(tmp_path, now=time.time())
    assert not report["deleted"] and not report["errors"]
    assert target.read_text() == "new run"


def test_replaced_unregistered_generation_is_not_deleted(tmp_path):
    target = generated(tmp_path)
    adopt_artifacts(tmp_path, [target], finished_at=100)
    old = tmp_path / "retained-old-generation.json"
    target.rename(old)
    target.write_text("user replacement")
    report = cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)
    assert report["deleted"] == [] and report["errors"]
    assert target.read_text() == "user replacement" and old.exists()


def test_adoption_checks_the_verified_generation_before_registering(tmp_path):
    target = generated(tmp_path)
    expected = retention._identity(target)
    target.rename(tmp_path / "verified-original.json")
    target.write_text("new unverified user content")
    with pytest.raises(ValueError, match="verified adoption generation"):
        register_artifacts(tmp_path, [target], 100, expected_identities=[expected])
    assert records(tmp_path) == [] and target.read_text() == "new unverified user content"
    assert cleanup_expired(tmp_path, now=time.time() + 2 * MAX_AGE_SECONDS)["deleted"] == []


def test_adoption_accepts_the_exact_expected_identity(tmp_path):
    target = generated(tmp_path)
    register_artifacts(
        tmp_path, [target], time.time(), expected_identities=[retention._identity(target)]
    )
    assert cleanup_expired(tmp_path, now=time.time() + 2 * MAX_AGE_SECONDS)["deleted"] == [str(target)]


def test_adoption_rejects_misaligned_expected_identity_list(tmp_path):
    target = generated(tmp_path)
    with pytest.raises(ValueError, match="identities must match"):
        register_artifacts(tmp_path, [target], 100, expected_identities=[])
    assert target.exists() and not (tmp_path / REGISTRY).exists()


def test_new_writes_extend_completed_generation_expiry(tmp_path):
    target = generated(tmp_path)
    adopt_artifacts(tmp_path, [target], finished_at=100)
    target.write_text("recently amended result")
    os.utime(target, (700, 700))
    assert cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)["deleted"] == []
    assert cleanup_expired(tmp_path, now=700 + MAX_AGE_SECONDS)["deleted"] == [str(target)]


def test_replacement_after_final_identity_probe_is_restored_without_deletion(tmp_path, monkeypatch):
    output = tmp_path / "run"
    generated(output)
    adopt_artifacts(tmp_path, [output], finished_at=100)
    original_generation = tmp_path / "moved-old-run"
    actual_same = retention._same
    checks = 0

    def swap_after_probe(path, item):
        nonlocal checks
        result = actual_same(path, item)
        if path == output:
            checks += 1
            if checks == 2:
                output.rename(original_generation)
                generated(output, "user-content.json")
        return result

    monkeypatch.setattr(retention, "_same", swap_after_probe)
    report = cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)
    assert not report["deleted"] and report["errors"]
    assert (output / "user-content.json").exists()
    assert (original_generation / "result.json").exists()


def test_interrupted_quarantine_recovers_without_orphaning_or_deleting_reused_path(
    tmp_path, monkeypatch
):
    output = tmp_path / "run"
    generated(output)
    adopt_artifacts(tmp_path, [output], finished_at=100)
    actual_remove = retention.shutil.rmtree

    def interrupted(path):
        raise OSError("interrupted after quarantine rename")

    monkeypatch.setattr(retention.shutil, "rmtree", interrupted)
    assert cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)["errors"]
    assert not output.exists()
    quarantine = list((tmp_path / REGISTRY).glob(".deleting-*"))
    assert len(quarantine) == 1 and (quarantine[0] / "result.json").exists()
    replacement = generated(output, "new-result.json")
    with pytest.raises(RuntimeError, match="previous cleanup"):
        ArtifactLease(tmp_path, [output])
    monkeypatch.setattr(retention.shutil, "rmtree", actual_remove)
    report = cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)
    assert report["errors"] == [] and report["deleted"] == [str(output)]
    assert replacement.exists() and not quarantine[0].exists()
    with ArtifactLease(tmp_path, [output]):
        pass


def test_finish_refuses_to_claim_a_replacement_path(tmp_path):
    target = generated(tmp_path)
    lease = ArtifactLease(tmp_path, [target])
    target.rename(tmp_path / "old.json")
    target.write_text("replacement")
    with pytest.raises(ValueError, match="replaced"):
        lease.finish()
    assert records(tmp_path)[0]["finished_at"] is None
    assert cleanup_expired(tmp_path, now=time.time() + 2 * MAX_AGE_SECONDS)["deleted"] == []


@pytest.mark.parametrize(
    "target",
    [".", "../original.json", "configs/source.json", "src/source.py", ".git/config", "pyproject.toml"],
)
def test_refuse_root_traversal_and_source_configuration_targets(tmp_path, target):
    with pytest.raises(ValueError):
        ArtifactLease(tmp_path, [Path(target)])


def test_nonexistent_targets_are_not_given_unverifiable_generation_ownership(tmp_path):
    with pytest.raises(ValueError, match="before leasing"):
        ArtifactLease(tmp_path, [Path("not-created.json")])
    assert not (tmp_path / REGISTRY).exists()


def test_registry_protection_is_case_insensitive(tmp_path):
    registry_alias = tmp_path / REGISTRY.upper()
    target = generated(registry_alias)
    with pytest.raises(ValueError):
        ArtifactLease(tmp_path, [registry_alias])
    with pytest.raises(ValueError):
        ArtifactLease(tmp_path, [target])
    with pytest.raises(ValueError):
        ArtifactLease(registry_alias, [target])
    with pytest.raises(ValueError):
        validate_output_path(registry_alias / "new-output")
    assert target.exists()


def test_tampered_manifest_cannot_escape_its_root(tmp_path):
    target = generated(tmp_path / "outputs")
    original = generated(tmp_path, "original.json")
    adopt_artifacts(target.parent, [target], finished_at=100)
    path = next((target.parent / REGISTRY).glob("*.json"))
    entry = json.loads(path.read_text())
    entry["targets"][0]["path"] = "../original.json"
    path.write_text(json.dumps(entry))
    report = cleanup_expired(target.parent, now=100 + MAX_AGE_SECONDS)
    assert report["errors"] and not report["deleted"]
    assert target.exists() and original.exists()


def link_directory(link, target):
    try:
        link.symlink_to(target, target_is_directory=True)
    except OSError:
        if sys.platform != "win32":
            raise
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, text=True
        )
        if result.returncode:
            pytest.skip("Directory links are unavailable on this Windows host")


def test_symlink_or_junction_ancestor_is_rejected_before_resolving(tmp_path):
    outside = tmp_path / "outside"
    original = generated(outside)
    alias = tmp_path / "alias"
    link_directory(alias, outside)
    with pytest.raises(ValueError, match="symlink|reparse"):
        validate_output_path(alias / "future-output")
    with pytest.raises(ValueError, match="symlink|reparse"):
        ArtifactLease(tmp_path, [alias / original.name])
    assert original.exists()


def test_added_link_inside_registered_directory_blocks_recursive_removal(tmp_path):
    output = tmp_path / "output"
    generated(output)
    outside = tmp_path / "outside"
    original = generated(outside)
    adopt_artifacts(tmp_path, [output], finished_at=100)
    link_directory(output / "linked", outside)
    report = cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)
    assert report["errors"] and report["deleted"] == []
    assert output.exists() and original.exists()


def test_ancestor_registered_directory_cannot_acquire_a_nested_owner(tmp_path):
    output = tmp_path / "output"
    target = generated(output)
    adopt_artifacts(tmp_path, [output], finished_at=100)
    with pytest.raises(ValueError, match="parent registry"):
        ArtifactLease(output, [target])
    assert not (output / REGISTRY).exists()


def test_recursive_cleanup_finds_independent_nested_registries(tmp_path):
    first = generated(tmp_path / "inputs")
    second = generated(tmp_path / "runs" / "id")
    adopt_artifacts(tmp_path, [first], finished_at=100)
    adopt_artifacts(tmp_path / "runs", [second.parent], finished_at=100)
    report = cleanup_expired(tmp_path, now=100 + MAX_AGE_SECONDS)
    assert set(report["deleted"]) == {str(first), str(second.parent)}
    assert report["errors"] == []


def test_absent_root_is_a_noop_and_unknown_outputs_are_never_adopted(tmp_path):
    missing = tmp_path / "missing"
    assert cleanup_expired(missing)["deleted"] == []
    assert not missing.exists()
    original = generated(tmp_path)
    assert cleanup_expired(tmp_path, now=time.time() + 9 * MAX_AGE_SECONDS)["deleted"] == []
    assert original.exists() and not (tmp_path / REGISTRY).exists()


@pytest.mark.parametrize("age", [0, -1, float("inf"), float("nan"), True])
def test_invalid_retention_intervals_fail_without_changes(tmp_path, age):
    with pytest.raises(ValueError):
        cleanup_expired(tmp_path, max_age_seconds=age)
    assert not (tmp_path / REGISTRY).exists()


def test_cli_dry_run_uses_only_registered_targets(tmp_path):
    target = generated(tmp_path)
    adopt_artifacts(tmp_path, [target], finished_at=time.time() - 2 * MAX_AGE_SECONDS)
    result = subprocess.run(
        [sys.executable, "-m", "event_universe.retention", "--root", str(tmp_path), "--dry-run"],
        capture_output=True,
        text=True,
        check=True,
        env=child_environment(),
    )
    assert json.loads(result.stdout)[0]["deleted"] == [str(target)]
    assert target.exists()


def test_cli_reports_manifest_failure_with_nonzero_exit_status(tmp_path):
    target = generated(tmp_path)
    adopt_artifacts(tmp_path, [target], finished_at=100)
    next((tmp_path / REGISTRY).glob("*.json")).write_text("invalid registry record")
    result = subprocess.run(
        [sys.executable, "-m", "event_universe.retention", "--root", str(tmp_path)],
        capture_output=True,
        text=True,
        env=child_environment(),
    )
    assert result.returncode == 1
    assert json.loads(result.stdout)[0]["errors"]
    assert target.exists()


def test_watcher_lock_is_singleton_across_processes_and_root_order(tmp_path):
    other = tmp_path / "second-root"
    other.mkdir()
    lock = watcher_lock([tmp_path, other])
    assert lock.held
    code = (
        "import sys; from pathlib import Path; "
        "from event_universe.retention import watcher_lock; "
        "lock=watcher_lock([Path(p) for p in sys.argv[1:]]); print(lock.held); lock.close()"
    )
    try:
        result = subprocess.run(
            [sys.executable, "-c", code, str(other), str(tmp_path)],
            capture_output=True,
            text=True,
            check=True,
            env=child_environment(),
        )
        assert result.stdout.strip() == "False"
    finally:
        lock.close()
    replacement = watcher_lock([tmp_path, other])
    assert replacement.held
    replacement.close()
