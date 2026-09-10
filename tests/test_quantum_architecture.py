"""Quantum ownership boundaries use the project's shared import resolver."""

import ast
from pathlib import Path

import pytest

import event_universe

from .architecture_rules import import_targets

FORBIDDEN_QUANTUM_DEPENDENCIES = (
    "event_universe.core.engine",
    "event_universe.core.linked_engine",
    "event_universe.api",
    "event_universe.compat",
    "event_universe.runner",
    "event_universe.scenarios",
    "event_universe.fields",
    "event_universe.dynamics",
    "event_universe.models",
    "event_universe.diagnostics",
    "event_universe.integration",
    "event_universe.Simulation",
    "event_universe.LinkedSimulation",
)


def _within(target: str, prefix: str) -> bool:
    return target == prefix or target.startswith(prefix + ".")


def quantum_violations(source: str, module: str) -> list[tuple[int, str]]:
    """Resolve relative imports and imported members before checking ownership.

    Static guard only: this does not promise to detect arbitrary dynamic Python.
    Quantum may reuse bounded arithmetic from core.state, never a world engine.
    """
    layer = module.removeprefix("event_universe.").split(".")[0]
    found = []
    for line, target in import_targets(ast.parse(source), module):
        if layer == "quantum":
            if any(_within(target, prefix) for prefix in FORBIDDEN_QUANTUM_DEPENDENCIES):
                found.append((line, target))
        elif layer != "integration" and _within(target, "event_universe.quantum"):
            found.append((line, target))
    return found


def test_all_production_modules_respect_quantum_ownership():
    root = Path(event_universe.__file__).parent
    for path in root.rglob("*.py"):
        module = "event_universe." + ".".join(path.relative_to(root).with_suffix("").parts)
        assert not quantum_violations(path.read_text(encoding="utf-8"), module), path


@pytest.mark.parametrize(
    "module,source",
    [
        ("quantum.deferred", "from ..core.engine import Engine"),
        ("quantum.deferred", "from event_universe.core import engine"),
        ("quantum.deferred", "from ..core import linked_engine as engine"),
        ("quantum.deferred", "from .. import Simulation"),
        ("quantum.deferred", "from event_universe import LinkedSimulation"),
        ("quantum.deferred", "from ..fields import scalar"),
        ("quantum.deferred", "from ..integration import quantum_bridge"),
        ("quantum.deferred", "import event_universe.diagnostics.frames as frames"),
        ("diagnostics.frames", "from ..quantum import DeferredQuantum"),
        ("core.engine", "from .. import quantum"),
        ("models.current_field", "import event_universe.quantum as quantum"),
        ("api", "from .quantum import DeferredQuantum"),
    ],
)
def test_gate_rejects_relative_member_and_aliased_imports(module, source):
    assert quantum_violations(source, "event_universe." + module)


@pytest.mark.parametrize(
    "module,source",
    [
        ("quantum.deferred", "from ..core.state import Address, checked, checked_work"),
        ("quantum.deferred", "from .state import Amplitude"),
        ("quantum.__init__", "from .deferred import DeferredQuantum"),
        ("integration.quantum_bridge", "from ..quantum import DeferredQuantum"),
        ("diagnostics.frames", "from ..core.engine import Engine"),
    ],
)
def test_gate_allows_legal_dependencies(module, source):
    assert not quantum_violations(source, "event_universe." + module)


def test_quantum_and_bridge_pass_integer_static_audit():
    from event_universe.diagnostics.numeric_audit import static_integer_audit

    root = Path(event_universe.__file__).parent
    checked_paths = list((root / "quantum").rglob("*.py")) + [root / "integration" / "quantum_bridge.py"]
    assert checked_paths
    assert {str(path): static_integer_audit(path) for path in checked_paths} == {
        str(path): [] for path in checked_paths
    }
