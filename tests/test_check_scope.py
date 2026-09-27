"""Changed-code selection includes consumers without scheduling unrelated worlds."""

import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from tests.worlds import load_file

CHECK = load_file("check_scope", Path(__file__).resolve().parents[1] / "tools/check.py")


def test_every_resource_consumer_row_names_an_existing_test():
    for resource, consumers in CHECK.RESOURCE_CONSUMERS.items():
        assert (CHECK.ROOT / resource).exists(), resource
        for consumer in consumers:
            assert (CHECK.ROOT / consumer).exists(), consumer


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
    """A tool is loaded by its path, never imported: the test that names the file is its consumer."""
    sources = {
        "tests/test_names_it.py": f'TOOL = ROOT / "tools" / "{Path(name).name}"',
        "tests/test_other.py": "def test_other(): pass",
    }
    tests, typed = CHECK.select(["tools/" + name], sources)
    assert "tests/test_names_it.py" in tests and "tests/test_other.py" not in tests
    assert "tests/test_check_scope.py" in tests
    assert not typed
    assert Path(name).name in (CHECK.ROOT / consumer).read_text(encoding="utf-8")


def test_transitive_imports_and_relative_helpers_retain_only_related_tests():
    sources = {
        "src/domain/math.py": "def calculate(): pass",
        "src/domain/engine.py": "from .math import calculate",
        "tests/helper.py": "from domain.engine import calculate",
        "tests/test_engine.py": "from .helper import calculate",
        "tests/test_unrelated.py": "def test_other(): pass",
    }
    tests, typed = CHECK.select(["src/domain/math.py"], sources)
    assert "tests/test_engine.py" in tests and "tests/test_unrelated.py" not in tests
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
    assert "tests/test_generic.py" in tests and "tests/test_history.py" not in tests
    tests, _ = CHECK.select(["src/event_universe/historical.py"], sources)
    assert "tests/test_history.py" in tests and "tests/test_generic.py" not in tests


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
    assert "tests/test_names_it.py" in tests and "tests/test_historical.py" not in tests


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
    monkeypatch.setattr(CHECK.subprocess, "run", lambda *a, **k: pytest.fail("no checks were selected"))
    CHECK.main()


def test_clean_checkout_still_honors_explicit_test_selection(monkeypatch, tmp_path, capsys):
    target = tmp_path / "tests/test_selected.py"
    target.parent.mkdir()
    target.write_text("def test_boundary(): pass", encoding="utf-8")
    chosen = "tests/test_selected.py::test_boundary"
    no_change_main(monkeypatch, tmp_path, "--dry-run", "--tests", chosen)
    report = json.loads(capsys.readouterr().out)
    assert report["changed"] == []
    assert report["commands"] == [["pytest", "-n", "auto", chosen, "--junitxml=artifacts/junit.xml"]]


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
    author = ["git", "-c", "user.name=Test", "-c", "user.email=test@example.org"]
    subprocess.run([*author, "commit", "-qm", "fixture"], cwd=tmp_path, check=True)
    (tmp_path / "src/demo/old.py").unlink()
    (tmp_path / "tests/test_old.py").write_text("def test_replacement(): pass", encoding="utf-8")
    actual = CHECK.subprocess.check_output
    calls = []

    counted = lambda command, **kwargs: (calls.append(command), actual(command, **kwargs))[1]  # noqa: E731
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
    assert listed == sorted(listed) and len(listed) == len(set(listed))
    assert all((CHECK.ROOT / test).is_file() for test in listed)
    assert set(listed) <= set(CHECK.select(["docs/GLOSSARY.md"], {})[0])
    assert "tests/test_shipped_worlds.py" in CHECK.select(["tests/shipped_worlds.json"], {})[0]
    assert CHECK.select([], {}) == ([], [])


def test_the_ci_shards_hold_every_test_once_and_the_regression_only_where_a_world_runs():
    plan = CHECK.shards(runs_worlds=True, every_world=True)
    assert len(plan) == 8 and all(plan.values())
    files = [t for name, targets in plan.items() if name.startswith("suite") for t in targets]
    tests = sorted(
        p.relative_to(CHECK.ROOT).as_posix() for p in (CHECK.ROOT / "tests").glob("test_*.py")
    )
    assert sorted(files + [CHECK.REGRESSION]) == tests
    recorded = json.loads((CHECK.ROOT / "tests/shipped_worlds.json").read_text())["worlds"]
    planned = json.loads(CHECK.RECORD_PLAN.read_text())["every_pull_request"]  # the owner's five
    for every, count in ((True, len(recorded)), (False, len(planned))):
        worlds = [t for n, ts in CHECK.shards(True, every).items() if "world" in n for t in ts]
        assert len(worlds) == count + 3 and len(planned) == 5 and set(planned) <= set(recorded)
    assert list(CHECK.shards(runs_worlds=False)) == ["suite 1", "suite 2", "suite 3"]
    assert CHECK.balanced({"a": 9, "b": 5, "c": 4, "d": 1}, 2) == [["a", "d"], ["b", "c"]]


def test_a_pull_request_adding_one_new_folder_with_its_test_runs_that_test_alone_and_no_world():
    """The owner's word of 2026-09-27: one new folder under features/ with its own test file and nothing else is one CI job, the folder's lint and that test; the loop, the loader, a standing folder or a second folder touched keeps the suite's shards and the worlds."""
    new = ["src/event_universe/features/newborn/__init__.py", "tests/test_feature_newborn.py"]
    assert CHECK.jobs(new, "HEAD") == {"folder newborn": ["tests/test_feature_newborn.py"]}
    commands = CHECK.shard_commands("folder newborn")
    assert [c[0] for c in commands] == ["ruff", "ruff", "mypy", "pytest"] and new[1] in commands[-1]
    assert all(CHECK.REGRESSION not in " ".join(c) and "." not in c for c in commands)
    loader, core = "src/event_universe/loader/world.py", "src/event_universe/core/step.py"
    old = [p.replace("newborn", "hold") for p in new]
    twin = new + [p.replace("newborn", "second") for p in new]
    for touched in (new[:1], new + [loader], new + [core], old, twin):
        assert CHECK.new_folder_alone(touched, "HEAD") is None
    with_worlds = CHECK.jobs(new + [loader], "HEAD")
    assert "suite 1" in with_worlds and any(name.startswith("world") for name in with_worlds)
    assert CHECK.shard_commands("suite 2")[0][:3] == ["pytest", "-n", "auto"]
