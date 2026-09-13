from pathlib import Path

import pytest

import event_universe
from event_universe import NodeState, ParticleState
from event_universe.core.scalar_engine import ScalarEngine
from event_universe.core.state import NODE_REGISTERS, PARTICLE_REGISTERS
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
        ("core.scalar_engine", "import event_universe.models.scalar_field as model"),
        ("core.scalar_engine", "from ..models import scalar_field"),
        ("fields.scalar", "from ..core.state import Config as Settings"),
        ("fields.scalar", "from ..core import scalar_engine"),
        ("fields.disturbances", "from ..core.disturbance_engine import DisturbanceEngine"),
        ("models.generic", "from ..core import disturbance_engine"),
        ("dynamics.turning", "from ..models.scalar_field import SCALAR_MODEL"),
        ("models.scalar_field", "from ..core.scalar_engine import ScalarEngine"),
        ("models.scalar_field", "from ..core import scalar_engine"),
        ("models.linked_field", "from ..core import linked_engine"),
        ("models.scalar_field", "from ..diagnostics import measurements"),
        ("fields.scalar", "from pathlib import Path"),
        ("models.scalar_field", "def update(source, count):\n    return source * count"),
        ("models.new_feature", "def update(source, count):\n    return source * count"),
        ("models.experimental.custom", "def update(x):\n    return x + 1"),
        ("particle_api", "def calculate(momentum):\n    return -momentum"),
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
        ("fields.disturbances", "from ..core.disturbance_state import DisturbanceRecord"),
        ("fields.disturbances", "from ..core.integer import checked_work"),
        ("fields.disturbances", "from ..core.coupling_selectors import matches_pair"),
        ("fields.disturbances", "from ..core.validation import ValidationMeter"),
        ("dynamics.turning", "import event_universe.core.state as state"),
        ("models.scalar_field", "from ..fields.scalar import ScalarField"),
        ("particle_api", "def build(value: int | None = None) -> int | None:\n    return value"),
        ("models.scalar_field", "selected: int | None = -1"),
        (
            "models.new_feature",
            "from ..fields.geometry import MeanStretch\nlaw = MeanStretch(100, 1, 2)",
        ),
    ],
)
def test_architecture_gate_allows_legal_dependencies_and_type_annotations(module, source):
    assert not violations(source, "event_universe." + module)


def test_physical_records_have_fixed_integer_fields_and_no_history():
    assert NODE_REGISTERS == 5 and PARTICLE_REGISTERS == 16
    assert len(NodeState()) == 5 and len(ParticleState(0, 0, 0)) == 16
    assert not hasattr(NodeState(), "__dict__")
    assert not hasattr(ParticleState(0, 0, 0), "__dict__")
    engine_source = Path(__import__(ScalarEngine.__module__, fromlist=["__file__"]).__file__).read_text()
    assert "self.paths" not in engine_source and "self.force_records" not in engine_source


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
