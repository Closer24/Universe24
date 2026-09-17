from pathlib import Path

import pytest

import event_universe
from event_universe.diagnostics.numeric_audit import audit_physical_modules, static_integer_audit

from .architecture_rules import violations


def test_all_physical_modules_pass_integer_audit():
    audit = audit_physical_modules()
    assert {Path(name).parts[0] for name in audit} == {"core", "fields"}
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
        ("fields.rays", "from ..core.disturbance_engine import DisturbanceEngine as Settings"),
        ("fields.rays", "from ..core import disturbance_engine"),
        ("fields.disturbances", "from ..core.disturbance_engine import DisturbanceEngine"),
        ("fields.source_envelope", "from ..core.source_envelope_node import SourceEnvelopeNode"),
        ("fields.source_emission", "from ..core.source_emission_node import EmittingEnvelopeNode"),
        ("core.topology", "from ..fields import rays"),
        ("fields.rays", "from ..diagnostics import local_observer"),
        ("fields.rays", "from pathlib import Path"),
        ("disturbance_api", "def calculate(momentum):\n    return -momentum"),
        ("disturbance_api", "def update(value):\n    value += 1\n    return value"),
        ("disturbance_api", "def update(source, count):\n    return source * count"),
    ],
)
def test_architecture_gate_rejects_real_import_and_formula_leaks(module, source):
    assert violations(source, "event_universe." + module)


@pytest.mark.parametrize(
    "module,source",
    [
        ("core.topology", "from .disturbance_state import Address3"),
        ("fields.disturbances", "from ..core.disturbance_state import DisturbanceRecord"),
        ("fields.disturbances", "from ..core.integer import checked_work"),
        ("fields.source_envelope", "from ..core.integer import bounded_gcd"),
        ("fields.source_envelope", "from ..core.source_envelope_state import EnvelopeAmplitude"),
        ("fields.source_emission", "from ..core.source_emission import SourceDeposit"),
        ("fields.disturbances", "from ..core.coupling_selectors import matches_pair"),
        ("fields.disturbances", "from ..core.validation import ValidationMeter"),
        ("fields.spatial_plan", "from ..core.sampling_contract import validate_spatial_sampling"),
        ("fields.rays", "from .spatial import SpatialPlan"),
        ("disturbance_api", "def build(value: int | None = None) -> int | None:\n    return value"),
        ("disturbance_api", "selected: int | None = -1"),
        (
            "disturbance_api",
            "from .fields.disturbances import DisturbanceLaw\nlaw = DisturbanceLaw(100, 1, 2)",
        ),
    ],
)
def test_architecture_gate_allows_legal_dependencies_and_type_annotations(module, source):
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
