"""Changed-code selection includes consumers without scheduling unrelated worlds."""

import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from tests.worlds import load_file

CHECK = load_file("check_scope", Path(__file__).resolve().parents[1] / "tools/check.py")


def test_every_resource_consumer_row_names_an_existing_test():
    root = Path(__file__).resolve().parents[1]
    for resource, consumers in CHECK.RESOURCE_CONSUMERS.items():
        assert (root / resource).exists(), resource
        for consumer in consumers:
            assert (root / consumer).exists(), consumer


def test_tool_changes_select_the_scope_test():
    tests, typed = CHECK.select(["tools/check.py"], {})
    assert "tests/test_check_scope.py" in tests
    assert not typed


@pytest.mark.parametrize(
    "name,consumer",
    [
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
    own = {"tests/test_check_scope.py", "tests/test_repository_hygiene.py"}
    own |= {"tests/test_repository_language.py", "tests/test_repository_navigation.py"}
    assert tests == sorted(own | set(CHECK.every_pull_request()))
    assert not typed


@pytest.mark.parametrize(
    "path,named",
    [
        ("examples/04-unequal-mass-collision.json", 'EXAMPLE = "04-unequal-mass-collision.json"'),
        ("examples/some-world/run_experiments.py", 'SCRIPT = "examples/some-world/run_experiments.py"'),
    ],
)
def test_an_example_selects_the_test_that_names_it_and_no_other(path, named):
    sources = {"tests/test_names_it.py": named, "tests/test_historical.py": "def test_old(): pass"}
    tests, _ = CHECK.select([path], sources)
    assert "tests/test_names_it.py" in tests
    assert "tests/test_historical.py" not in tests


def test_shared_fixture_includes_all_its_consumers():
    sources = {"tests/test_a.py": "", "tests/test_b.py": ""}
    tests, _ = CHECK.select(["tests/conftest.py"], sources)
    assert {"tests/test_a.py", "tests/test_b.py"} <= set(tests)


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


def test_dry_run_creates_no_scope_report(monkeypatch, tmp_path):
    no_change_main(monkeypatch, tmp_path, "--dry-run")
    assert list(tmp_path.iterdir()) == []


def test_a_change_to_the_law_selects_its_words_and_links_gate():
    tests, _ = CHECK.select(["docs/ALGEBRA.md"], {})
    assert "tests/test_law_words.py" in tests


def test_the_every_pull_request_list_is_one_sorted_file_of_existing_tests():
    """The gates every pull request runs live in tools/every_pull_request.txt, one existing test per line, sorted (#1198, gate 7)."""
    listed = CHECK.every_pull_request()
    root = Path(__file__).resolve().parents[1]
    assert listed == sorted(listed) and len(listed) == len(set(listed))
    assert all((root / test).is_file() for test in listed)
    assert set(listed) <= set(CHECK.select(["docs/GLOSSARY.md"], {})[0])
    assert CHECK.select([], {}) == ([], [])


def test_the_ci_shards_hold_every_test_once_and_no_world():
    """No world replays in CI (the owner's decision of 2026-09-27): the suite in equal shards, every test file once."""
    plan = CHECK.shards()
    assert list(plan) == ["suite 1", "suite 2", "suite 3"] and all(plan.values())
    files = sorted(t for targets in plan.values() for t in targets)
    tests = (CHECK.ROOT / "tests").glob("test_*.py")
    assert files == sorted(p.relative_to(CHECK.ROOT).as_posix() for p in tests)
    assert CHECK.balanced({"a": 9, "b": 5, "c": 4, "d": 1}, 2) == [["a", "d"], ["b", "c"]]
