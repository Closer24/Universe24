"""Changed-code selection includes consumers without scheduling unrelated worlds."""

import importlib.util
from pathlib import Path

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
        "tests/test_engine.py": "from .helper import calculate",
        "tests/test_unrelated.py": "def test_other(): pass",
    }
    tests, typed = CHECK.select(["src/domain/math.py"], sources)
    assert "tests/test_engine.py" in tests
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
