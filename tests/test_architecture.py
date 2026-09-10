from pathlib import Path

import pytest

import event_universe
from event_universe import CellState, ParticleState
from event_universe.core.engine import Engine
from event_universe.core.state import CELL_REGISTERS, PARTICLE_REGISTERS
from event_universe.diagnostics.numeric_audit import audit_physical_modules, static_integer_audit

from .architecture_rules import violations


def test_all_physical_modules_pass_integer_audit():
    audit = audit_physical_modules()
    assert {Path(name).parts[0] for name in audit} == {"core", "fields", "dynamics", "models"}
    assert all(not violations for violations in audit.values())


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


def test_all_production_modules_respect_dependency_and_composition_boundaries():
    root = Path(event_universe.__file__).parent
    for path in root.rglob("*.py"):
        module = "event_universe." + ".".join(path.relative_to(root).with_suffix("").parts)
        assert not violations(path.read_text(), module), str(path)


@pytest.mark.parametrize(
    "module,source",
    [
        ("core.engine", "import event_universe.models.current_field as model"),
        ("core.engine", "from ..models import current_field"),
        ("fields.scalar", "from ..core.state import Config as Settings"),
        ("fields.scalar", "from ..core import engine"),
        ("dynamics.turning", "from ..models.current_field import CURRENT_MODEL"),
        ("models.current_field", "from ..core.engine import Engine"),
        ("models.current_field", "from ..core import engine"),
        ("models.linked_field", "from ..core import linked_engine"),
        ("models.current_field", "from ..diagnostics import measurements"),
        ("fields.scalar", "from pathlib import Path"),
        ("models.current_field", "def update(source, count):\n    return source * count"),
        ("api", "def calculate(momentum):\n    return -momentum"),
        ("compat", "def update(value):\n    value += 1\n    return value"),
    ],
)
def test_architecture_gate_rejects_real_import_and_formula_leaks(module, source):
    assert violations(source, "event_universe." + module)


@pytest.mark.parametrize(
    "module,source",
    [
        ("core.lattice", "from .state import Address"),
        ("fields.policies", "from ..core.state import checked"),
        ("dynamics.turning", "import event_universe.core.state as state"),
        ("models.current_field", "from ..fields.scalar import ScalarField"),
        ("api", "def build(value: int | None = None) -> int | None:\n    return value"),
        ("models.current_field", "selected: int | None = -1"),
    ],
)
def test_architecture_gate_allows_legal_dependencies_and_type_annotations(module, source):
    assert not violations(source, "event_universe." + module)


def test_physical_records_have_fixed_integer_fields_and_no_history():
    assert CELL_REGISTERS == 5 and PARTICLE_REGISTERS == 12
    assert len(CellState()) == 5 and len(ParticleState(0, 0, 0)) == 12
    assert not hasattr(CellState(), "__dict__")
    assert not hasattr(ParticleState(0, 0, 0), "__dict__")
    engine_source = Path(__import__(Engine.__module__, fromlist=["__file__"]).__file__).read_text()
    assert "self.paths" not in engine_source and "self.force_records" not in engine_source


def test_postulates_are_linked_and_state_causal_consistency():
    root = Path(__file__).parents[1]
    postulates = (root / "POSTULATES_HE.md").read_text(encoding="utf-8")
    definitions = (root / "SIMULATOR_DEFINITIONS.md").read_text(encoding="utf-8")
    readme = (root / "README.md").read_text(encoding="utf-8")
    architecture = (root / "docs" / "ARCHITECTURE.md").read_text(encoding="utf-8")
    for document in (definitions, readme, architecture):
        assert "POSTULATES_HE.md" in document
    assert "עקביות נשמרת באופן מקומי וסיבתי" in postulates
    assert "Spatial-causal consistency postulate" in definitions
    assert "קוונטיות ושזירה הן עדיין שכבה פתוחה" in postulates


def test_shared_rules_ship_with_source_and_have_one_entry_point():
    root = Path(__file__).parents[1]
    entry = root / "AGENTS.md"
    assert entry.is_file()
    for name in ("README.md", "CONTRIBUTING.md", "docs/ARCHITECTURE.md", "MANIFEST.in"):
        assert "AGENTS.md" in (root / name).read_text()
    for name in (
        "POSTULATES_HE.md",
        "SIMULATOR_DEFINITIONS.md",
        "docs/ARCHITECTURE.md",
        "CONTRIBUTING.md",
        "docs/TEST_EXPECTATIONS_HE.md",
    ):
        assert name in entry.read_text()
        assert (root / name).is_file()
    assert "python tools/check.py" in (root / ".github/workflows/check.yml").read_text()
