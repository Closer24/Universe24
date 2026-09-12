"""Changed-code selection includes consumers without scheduling unrelated worlds."""

import importlib.util
import json
import time
from pathlib import Path

import pytest

from event_universe.retention import MAX_AGE_SECONDS, cleanup_expired

SPEC = importlib.util.spec_from_file_location(
    "check_scope", Path(__file__).resolve().parents[1] / "tools/check.py"
)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def test_transitive_imports_and_relative_helpers_retain_only_related_tests():
    sources = {
        "src/domain/math.py": "def calculate(): pass",
        "src/domain/engine.py": "from .math import calculate",
        "tests/helper.py": "from domain.engine import calculate",
        "tests/test_scalar_engine.py": "from .helper import calculate",
        "tests/test_unrelated.py": "def test_other(): pass",
    }
    tests, typed = CHECK.select(["src/domain/math.py"], sources)
    assert "tests/test_scalar_engine.py" in tests
    assert "tests/test_unrelated.py" not in tests
    assert typed == ["src/domain/engine.py", "src/domain/math.py"]


def test_named_lazy_exports_do_not_pull_in_unrelated_physics():
    sources = {
        "src/event_universe/__init__.py": 'from .generic import Simulation\nmodules = {"ScalarSimulation": ".historical"}',
        "src/event_universe/generic.py": "class Simulation: pass",
        "src/event_universe/historical.py": "class ScalarSimulation: pass",
        "tests/test_generic.py": "from event_universe import Simulation",
        "tests/test_history.py": "from event_universe import ScalarSimulation",
    }
    tests, _ = CHECK.select(["src/event_universe/generic.py"], sources)
    assert "tests/test_generic.py" in tests
    assert "tests/test_history.py" not in tests
    tests, _ = CHECK.select(["src/event_universe/historical.py"], sources)
    assert "tests/test_history.py" in tests
    assert "tests/test_generic.py" not in tests


def test_deleted_module_retains_old_consumers_and_cycles_terminate():
    sources = {
        "src/demo/old.py": "from .other import run",
        "src/demo/other.py": "from .old import run",
        "tests/test_old.py": "from demo.old import run",
    }
    tests, _ = CHECK.select(["src/demo/old.py"], sources)
    assert "tests/test_old.py" in tests


def test_docs_and_validation_changes_do_not_schedule_simulations():
    tests, typed = CHECK.select(["AGENTS.md", "tools/check.py", ".github/workflows/check.yml"], {})
    assert tests == [
        "tests/test_check_scope.py",
        "tests/test_repository_hygiene.py",
        "tests/test_repository_language.py",
        "tests/test_repository_navigation.py",
    ]
    assert not typed


def test_example_selects_its_consumers_and_not_other_collision_candidates():
    sources = {
        "tests/test_atomic_interactions.py": 'EXAMPLE = "04-unequal-mass-collision.json"',
        "tests/test_collisions.py": "def test_old_candidate(): pass",
    }
    tests, _ = CHECK.select(["examples/04-unequal-mass-collision.json"], sources)
    assert "tests/test_atomic_interactions.py" in tests
    assert "tests/test_workspace.py" in tests
    assert "tests/test_collisions.py" not in tests


def test_shared_fixture_includes_all_its_consumers():
    sources = {"tests/test_a.py": "", "tests/test_b.py": ""}
    tests, _ = CHECK.select(["tests/conftest.py"], sources)
    assert {"tests/test_a.py", "tests/test_b.py"} <= set(tests)


@pytest.mark.parametrize(
    "example", ["basic", "exchange", "finite_fields", "open_world", "spatial_turning"]
)
def test_dynamic_example_paths_retain_identity_checks_without_unrelated_physics(example):
    sources = {
        "tests/test_generic_identity.py": 'filename = f"{name}.json"',
        "tests/test_collisions.py": "def test_historical(): pass",
    }
    tests, _ = CHECK.select([f"examples/{example}.json"], sources)
    assert "tests/test_generic_identity.py" in tests
    assert "tests/test_collisions.py" not in tests


def test_runpy_acceptance_tool_retains_application_consumer():
    sources = {
        "tests/test_legacy_application.py": 'runpy.run_path(root / "tools/check_diagonal_motion.py")',
        "tests/test_collisions.py": "def test_historical(): pass",
    }
    tests, _ = CHECK.select(["tools/check_diagonal_motion.py"], sources)
    assert "tests/test_legacy_application.py" in tests
    assert "tests/test_collisions.py" not in tests


def no_change_main(monkeypatch, tmp_path, *arguments):
    monkeypatch.setattr(CHECK, "ROOT", tmp_path)
    monkeypatch.setattr(CHECK, "git", lambda *args: "base" if args[0] == "merge-base" else "")
    monkeypatch.setattr(CHECK.sys, "argv", ["check.py", *arguments])
    monkeypatch.setattr(
        CHECK.subprocess, "run", lambda *args, **kwargs: pytest.fail("no checks were selected")
    )
    CHECK.main()


def test_scope_report_is_registered_and_expires_without_removing_unregistered_files(
    monkeypatch, tmp_path
):
    no_change_main(monkeypatch, tmp_path)
    report = tmp_path / "artifacts/check-scope.json"
    assert json.loads(report.read_text(encoding="utf-8")) == {
        "mode": "affected",
        "changed": [],
        "commands": [],
    }
    original = report.parent / "original.json"
    original.write_text("preserved original", encoding="utf-8")
    result = cleanup_expired(report.parent, now=time.time() + MAX_AGE_SECONDS + 1)
    assert result["errors"] == [] and result["deleted"] == [str(report)]
    assert not report.exists() and original.read_text(encoding="utf-8") == "preserved original"


def test_dry_run_creates_no_scope_report_or_retention_registry(monkeypatch, tmp_path):
    no_change_main(monkeypatch, tmp_path, "--dry-run")
    assert list(tmp_path.iterdir()) == []


def test_scope_report_stays_leased_until_failed_selected_command_finishes(monkeypatch, tmp_path):
    selected = tmp_path / "tests/test_selected.py"
    selected.parent.mkdir()
    selected.touch()
    monkeypatch.setattr(CHECK, "ROOT", tmp_path)
    monkeypatch.setattr(CHECK, "git", lambda *args: "base" if args[0] == "merge-base" else "")
    monkeypatch.setattr(CHECK.sys, "argv", ["check.py", "--tests", "tests/test_selected.py"])
    report = tmp_path / "artifacts/check-scope.json"

    def fail_command(command, **kwargs):
        assert command[2:4] == ["pytest", "tests/test_selected.py"]
        active = cleanup_expired(report.parent, now=time.time() + 2 * MAX_AGE_SECONDS)
        assert not active["errors"] and not active["deleted"] and report.exists()
        assert any(item["reason"] == "active writer" for item in active["skipped"])
        raise CHECK.subprocess.CalledProcessError(1, command)

    monkeypatch.setattr(CHECK.subprocess, "run", fail_command)
    with pytest.raises(CHECK.subprocess.CalledProcessError):
        CHECK.main()
    finished = cleanup_expired(report.parent, now=time.time() + MAX_AGE_SECONDS + 1)
    assert not finished["errors"] and finished["deleted"] == [str(report)]
    assert selected.exists()


@pytest.mark.parametrize("path", [".github/workflows/check.yml", "setup.ps1", "new-component/notes.txt"])
def test_every_file_change_selects_language_and_canonical_copy_guards(path):
    tests, typed = CHECK.select([path], {})
    assert {"tests/test_repository_language.py", "tests/test_repository_hygiene.py"} <= set(tests)
    assert not typed


@pytest.mark.parametrize(
    "path",
    [
        "examples/04-unequal-mass-collision.json",
        "examples/known-entities/three-masses.json",
        "examples/known-entities/three-masses-low-budget.json",
        "examples/known-entities/boundary-periodic.json",
        "examples/known-entities/boundary-open.json",
        "examples/known-entities/run_reference_checks.py",
        "examples/known-entities/run_reference_checks.ps1",
    ],
)
def test_reference_runner_dynamic_resources_select_numerical_acceptance(path):
    tests, _ = CHECK.select([path], {})
    assert "tests/test_reference_examples.py" in tests
