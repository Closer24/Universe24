"""LOCALITY-1 is documented without an exception: every physical dependency is
local, audited end-to-end, with fixed local work and storage for fixed K."""

from pathlib import Path


def test_locality_rule_is_documented_without_an_exception():
    root = Path(__file__).parents[1]
    definitions = (root / "SIMULATOR_DEFINITIONS.md").read_text()
    assert "LOCALITY-1" in definitions
    assert "end-to-end" in definitions
    assert "fixed K" in definitions
    assert "sole explicit model-computation exception" not in definitions
    assert "LOCALITY-1" in (root / "AGENTS.md").read_text()
