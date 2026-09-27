"""Changed-code selection includes consumers without scheduling unrelated worlds."""

import importlib.util
import json
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from event_universe.retention import MAX_AGE_SECONDS, cleanup_expired

SPEC = importlib.util.spec_from_file_location(
    "check_scope", Path(__file__).resolve().parents[1] / "tools/check.py"
)
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


def test_the_worlds_readme_selects_navigation_and_never_a_cancelled_test():
    # its consumer row names the ray law's worlds test, cancelled (docs/CANCELLED_WORLDS.md
    # section 3): the selector drops it and keeps the document scanners
    selected, _ = CHECK.select(["examples/events/README.md"], {})
    assert "tests/test_nature_beam_worlds.py" not in selected
    assert "tests/test_repository_navigation.py" in selected
    assert "tests/test_retention.py" not in selected


def test_every_resource_consumer_row_names_an_existing_test():
    root = Path(__file__).resolve().parents[1]
    for resource, consumers in CHECK.RESOURCE_CONSUMERS.items():
        assert (root / resource).exists(), resource
        for consumer in consumers:
            assert (root / consumer).exists(), consumer


@pytest.mark.parametrize("name", ["check.py", "preflight_worlds.py"])
def test_tool_changes_select_the_scope_test(name):
    tests, typed = CHECK.select(["tools/" + name], {})
    assert "tests/test_check_scope.py" in tests
    assert not typed


@pytest.mark.parametrize(
    "name,consumer",
    [
        ("preflight_worlds.py", "tests/test_preflight_worlds.py"),
        ("run_inputs.py", "tests/test_run_inputs.py"),
        ("twist_table.py", "tests/test_primitives.py"),
    ],
)
def test_tool_changes_select_the_test_that_loads_the_tool_by_its_path(name, consumer):
    """A tool is loaded by its path, never imported: the test that
    names the file is its consumer, the tests that do not are not."""
    sources = {
        "tests/test_names_it.py": f'TOOL = ROOT / "tools" / "{Path(name).name}"',
        "tests/test_other.py": "def test_other(): pass",
    }
    tests, typed = CHECK.select(["tools/" + name], sources)
    assert "tests/test_names_it.py" in tests and "tests/test_other.py" not in tests
    assert "tests/test_check_scope.py" in tests
    assert not typed
    root = Path(__file__).resolve().parents[1]
    assert (root / consumer).exists()
    assert Path(name).name in (root / consumer).read_text(encoding="utf-8")


def test_transitive_imports_and_relative_helpers_retain_only_related_tests():
    sources = {
        "src/domain/math.py": "def calculate(): pass",
        "src/domain/engine.py": "from .math import calculate",
        "tests/helper.py": "from domain.engine import calculate",
        "tests/test_engine.py": "from .helper import calculate",
        "tests/test_unrelated.py": "def test_other(): pass",
    }
    tests, typed = CHECK.select(["src/domain/math.py"], sources)
    assert "tests/test_engine.py" in tests
    assert "tests/test_unrelated.py" not in tests
    assert typed == ["src/domain/engine.py", "src/domain/math.py"]


def test_named_lazy_exports_do_not_pull_in_unrelated_physics():
    sources = {
        "src/event_universe/__init__.py": 'from .generic import Simulation\nmodules = {"ResearchSimulation": ".historical"}',
        "src/event_universe/generic.py": "class Simulation: pass",
        "src/event_universe/historical.py": "class ResearchSimulation: pass",
        "tests/test_generic.py": "from event_universe import Simulation",
        "tests/test_history.py": "from event_universe import ResearchSimulation",
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
        "tests/test_code_shape.py",
        "tests/test_engine_gates.py",
        "tests/test_genericity.py",
        "tests/test_repository_hygiene.py",
        "tests/test_repository_language.py",
        "tests/test_repository_navigation.py",
        "tests/test_shipped_worlds.py",
    ]
    assert not typed


def test_every_change_selects_the_shipped_worlds_regression_and_no_change_selects_nothing():
    """The regression record of every shipped world is compared and the genericity test draws
    its universes on any change at all (record 2214 point 7; record 2234); with nothing changed
    nothing is selected."""
    tests, _ = CHECK.select(["docs/GLOSSARY.md"], {})
    assert "tests/test_shipped_worlds.py" in tests and "tests/test_genericity.py" in tests
    tests, _ = CHECK.select(["tests/shipped_worlds.json"], {})
    assert "tests/test_shipped_worlds.py" in tests


def test_every_change_selects_the_code_shape_gate_and_no_change_selects_nothing():
    """The shape of the code is held at its baseline on any change at all (records 2239 and
    2241); with nothing changed nothing is selected."""
    tests, _ = CHECK.select(["docs/GLOSSARY.md"], {})
    assert "tests/test_code_shape.py" in tests and "tests/test_engine_gates.py" in tests
    assert CHECK.select([], {}) == ([], [])


def test_example_selects_its_consumers_and_not_other_collision_candidates():
    sources = {
        "tests/test_atomic_interactions.py": 'EXAMPLE = "04-unequal-mass-collision.json"',
        "tests/test_historical.py": "def test_old_candidate(): pass",
    }
    tests, _ = CHECK.select(["examples/04-unequal-mass-collision.json"], sources)
    assert "tests/test_atomic_interactions.py" in tests
    assert "tests/test_preflight_worlds.py" in tests
    assert "tests/test_historical.py" not in tests


def test_shared_fixture_includes_all_its_consumers():
    sources = {"tests/test_a.py": "", "tests/test_b.py": ""}
    tests, _ = CHECK.select(["tests/conftest.py"], sources)
    assert {"tests/test_a.py", "tests/test_b.py"} <= set(tests)


def test_example_script_selects_only_the_test_that_names_it():
    sources = {
        "tests/test_example_script.py": 'SCRIPT = ROOT / "examples/some-world/run_experiments.py"',
        "tests/test_historical.py": "def test_historical(): pass",
    }
    tests, _ = CHECK.select(["examples/some-world/run_experiments.py"], sources)
    assert "tests/test_example_script.py" in tests
    assert "tests/test_historical.py" not in tests


@pytest.mark.parametrize("resource", ["one_content.json", "two_slits.json"])
def test_world_files_select_the_preflight_and_the_tests_that_name_them(resource):
    sources = {"tests/test_names_it.py": f'WORLD = "{resource}"', "tests/test_other.py": ""}
    tests, _ = CHECK.select(["examples/events/" + resource], sources)
    assert "tests/test_preflight_worlds.py" in tests
    assert "tests/test_names_it.py" in tests and "tests/test_other.py" not in tests


def no_change_main(monkeypatch, tmp_path, *arguments):
    monkeypatch.setattr(CHECK, "ROOT", tmp_path)
    monkeypatch.setattr(CHECK, "git", lambda *args: "base" if args[0] == "merge-base" else "")
    monkeypatch.setattr(CHECK.sys, "argv", ["check.py", *arguments])
    monkeypatch.setattr(CHECK, "previous_sources", lambda *args: pytest.fail("no prior tree needed"))
    monkeypatch.setattr(CHECK, "select", lambda *args: pytest.fail("no dependency graph needed"))
    monkeypatch.setattr(
        CHECK.subprocess, "run", lambda *args, **kwargs: pytest.fail("no checks were selected")
    )
    CHECK.main()


def test_clean_checkout_still_honors_explicit_test_selection(monkeypatch, tmp_path, capsys):
    target = tmp_path / "tests/test_selected.py"
    target.parent.mkdir()
    target.write_text("def test_boundary(): pass", encoding="utf-8")
    no_change_main(
        monkeypatch, tmp_path, "--dry-run", "--tests", "tests/test_selected.py::test_boundary"
    )
    report = json.loads(capsys.readouterr().out)
    assert report["changed"] == []
    assert report["commands"] == [
        [
            "pytest",
            "-n",
            "auto",
            "tests/test_selected.py::test_boundary",
            "--junitxml=artifacts/junit.xml",
        ]
    ]


@pytest.fixture
def git_checkout():
    # Git init cannot use a Windows reserved directory name in an ancestor path.
    with TemporaryDirectory(prefix="universe-check-tree-") as directory:
        yield Path(directory)


def test_batched_prior_tree_preserves_exact_sources_and_deleted_consumers(monkeypatch, git_checkout):
    # A real tiny Git tree tests framing, empty blobs, spaces and missing final newlines.
    tmp_path = git_checkout
    monkeypatch.setenv("GIT_DIR", ".git")
    monkeypatch.setenv("GIT_WORK_TREE", ".")
    monkeypatch.setattr(CHECK, "ROOT", tmp_path)
    sources = {
        "src/demo/old.py": "def calculate(): return 7\n",
        "src/demo/empty.py": "",
        "tests/test_old.py": "from demo.old import calculate",
        "tools/with space.py": "# framed\n\n",
    }
    for path, content in {
        **sources,
        "tests/reference/archive.py": "archived",
        "src/data.json": "{}",
    }.items():
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8", newline="")
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    subprocess.run(["git", "-c", "core.autocrlf=false", "add", "."], cwd=tmp_path, check=True)
    subprocess.run(
        ["git", "-c", "user.name=Test", "-c", "user.email=test@example.org", "commit", "-qm", "fixture"],
        cwd=tmp_path,
        check=True,
    )
    (tmp_path / "src/demo/old.py").unlink()
    (tmp_path / "tests/test_old.py").write_text("def test_replacement(): pass", encoding="utf-8")
    actual = CHECK.subprocess.check_output
    calls = []

    def counted(command, **kwargs):
        calls.append(command)
        return actual(command, **kwargs)

    monkeypatch.setattr(CHECK.subprocess, "check_output", counted)
    previous = CHECK.previous_sources("HEAD")
    assert previous == sources
    assert len(calls) == 2
    tests, _ = CHECK.select(["src/demo/old.py"], previous)
    assert "tests/test_old.py" in tests


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
        assert command[2:6] == ["pytest", "-n", "auto", "tests/test_selected.py"]
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


@pytest.mark.parametrize(
    "path",
    [
        "examples/new-world.json",
        "examples/directional-wave/display.json",
        "skills/simulation-configuration/assets/two-streams.json",
    ],
)
def test_configuration_inventory_selects_preflight_without_unrelated_worlds(path):
    tests, _ = CHECK.select([path], {})
    assert "tests/test_preflight_worlds.py" in tests
    assert "tests/test_spatial_engine.py" not in tests


@pytest.mark.parametrize("name", ["catalog.json", "representation-probes.json"])
def test_catalog_resources_select_the_preflight_and_no_deleted_consumer(name):
    tests, _ = CHECK.select(["examples/known-entities/" + name], {})
    assert "tests/test_preflight_worlds.py" in tests
    assert all(test.startswith("tests/test_") for test in tests)
    assert not any("entity" in test or "profile" in test for test in tests)


def test_detector_definitions_select_no_cancelled_consumer():
    # the row's three consumers are the ray law's, cancelled (docs/CANCELLED_WORLDS.md
    # section 3): the selector names none of them and keeps the living preflight
    tests, _ = CHECK.select(["examples/events/detector/entities/detectors.json"], {})
    assert not {
        "tests/test_entity_definitions.py",
        "tests/test_configuration_validation.py",
        "tests/test_entity_loading_consumers.py",
    } & set(tests)
    assert "tests/test_preflight_worlds.py" in tests
    assert "tests/test_nature_beam_flight.py" not in tests
