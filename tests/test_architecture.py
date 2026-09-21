from pathlib import Path

import pytest

import event_universe
from event_universe.diagnostics.numeric_audit import (
    audit_physical_modules,
    static_events_audit,
    static_integer_audit,
)

from .architecture_rules import violations


def test_all_physical_modules_pass_integer_audit():
    """Both physical layers, each by its audit: `core/` integers only,
    `events/` integer numpy and nothing that leaves the integers."""
    audit = audit_physical_modules()
    assert {Path(name).parts[0] for name in audit} == {"core", "events"}
    assert "events/run.py" not in audit and "events/engine.py" in audit
    assert {name for name, found in audit.items() if found} == set()


@pytest.mark.parametrize(
    "source",
    [
        "x = 0.5",
        "x = 1 / 2",
        "x /= 2",
        "x = float(2)",
        "from math import sqrt as f",
        "import numpy as np",
    ],
)
def test_numeric_audit_detects_forbidden_math(tmp_path, source):
    path = tmp_path / "bad.py"
    path.write_text(source)
    assert static_integer_audit(path)


@pytest.mark.parametrize(
    "source",
    [
        "x = 0.5",
        "x = a / b",
        "x /= 2",
        "x = float(2)",
        "x = np.zeros(3, dtype=float)",
        "x = np.zeros(3, dtype=np.float64)",
        "x = np.sqrt(a)",
        "x = a.mean()",
        "x = np.pi",
        "import math\nx = math.sqrt(a)",
        "from fractions import Fraction",
        "import random",
    ],
)
def test_events_audit_detects_what_leaves_the_integers(tmp_path, source):
    path = tmp_path / "bad.py"
    path.write_text(source)
    assert static_events_audit(path)


@pytest.mark.parametrize(
    "source",
    [
        "import numpy as np\nx = np.zeros(3, dtype=np.int64)",
        "import math\nx = math.isqrt(a) + math.gcd(a, b)",
        "x = a // b\nx //= 2\ny = int(a.sum(dtype=object))",
        "x = np.abs(a).max(initial=0)",
    ],
)
def test_events_audit_permits_integer_numpy(tmp_path, source):
    path = tmp_path / "good.py"
    path.write_text(source)
    assert not static_events_audit(path)


def test_all_production_modules_respect_dependency_boundaries():
    root = Path(event_universe.__file__).parent
    for path in root.rglob("*.py"):
        module = "event_universe." + ".".join(path.relative_to(root).with_suffix("").parts)
        assert not violations(path.read_text(), module), str(path)


@pytest.mark.parametrize(
    "module,source",
    [
        ("core.phase", "from ..events import engine"),
        ("core.game_board", "from event_universe.runner import run_initialization"),
        ("events.engine", "from event_universe.runner import source_fingerprint"),
        ("events.nature_beam", "from pathlib import Path"),
        ("core.phase", "import json"),
    ],
)
def test_architecture_gate_rejects_upward_and_output_imports(module, source):
    assert violations(source, "event_universe." + module)


@pytest.mark.parametrize(
    "module,source",
    [
        ("core.phase", "from event_universe.core.integer import checked_work"),
        ("events.nature_beam", "from event_universe.core.game_board import Address3"),
        ("events.engine", "from event_universe.events.nature_beam import nature_beam"),
        ("events.run", "import json\nfrom event_universe.snapshot_writer import write_snapshot"),
        ("runner", "from event_universe.events.run import execute_nature_beam_run"),
    ],
)
def test_architecture_gate_allows_the_dependency_direction(module, source):
    assert not violations(source, "event_universe." + module)


def test_shared_rules_ship_with_source_and_have_one_entry_point():
    root = Path(__file__).parents[1]
    entry = root / "AGENTS.md"
    assert entry.is_file()
    for name in ("README.md", "CONTRIBUTING.md", "docs/ARCHITECTURE.md", "MANIFEST.in"):
        assert "AGENTS.md" in (root / name).read_text()
    for name in (
        "POSTULATES.md",
        "SIMULATOR_DEFINITIONS.md",
        "docs/ARCHITECTURE.md",
        "CONTRIBUTING.md",
        "docs/TEST_EXPECTATIONS.md",
    ):
        assert name in entry.read_text()
        assert (root / name).is_file()
    assert "python tools/check.py" in (root / ".github/workflows/check.yml").read_text()
