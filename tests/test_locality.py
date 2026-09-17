"""Explicit rejection of shadow-world dependencies in generic field code."""

from pathlib import Path

import pytest

from .architecture_rules import violations


@pytest.mark.parametrize(
    "source",
    [
        "def estimate(state):\n    return sum(state.nodes.values())",
        "def estimate(state):\n    return state.particles.values()",
        "def estimate(shadow):\n    shadow.step()",
        "def estimate(shadow):\n    shadow.run(100)",
        "def estimate(state):\n    return state.history[-1]",
        "def estimate(state):\n    return state.occupancy",
    ],
)
def test_local_calculation_gate_rejects_world_reads_and_shadow_replay(source):
    assert violations(source, "event_universe.fields.self_field")


def test_locality_rule_covers_self_field_dependencies_without_an_exception():
    root = Path(__file__).parents[1]
    definitions = (root / "SIMULATOR_DEFINITIONS.md").read_text()
    assert "LOCALITY-1" in definitions
    assert "shadow worlds" in definitions
    assert "end-to-end" in definitions
    assert "fixed K" in definitions
    assert "sole explicit model-computation exception" not in definitions
    assert "LOCALITY-1" in (root / "AGENTS.md").read_text()
