"""Fixed neighborhood access and explicit rejection of shadow-world dependencies."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from event_universe.core.engine import Engine
from event_universe.core.lattice import PeriodicLattice

from .architecture_rules import violations


@pytest.mark.parametrize("extent", [8, 1_000_000])
def test_particle_neighborhood_reads_exactly_six_cells_independent_of_world_extent(extent):
    # This is a read spy, not a simulated world or an evolution run.
    position = (3, 3, 3)
    expected = ((4, 3, 3), (2, 3, 3), (3, 4, 3), (3, 2, 3), (3, 3, 4), (3, 3, 2))
    reads = []

    def read(address):
        assert address in expected, "A remote cell was read"
        reads.append(address)
        return expected.index(address) + 1

    reader = SimpleNamespace(_lattice=PeriodicLattice((extent,) * 3), phi=read)
    assert Engine._particle_neighbors(reader, position) == (1, 2, 3, 4, 5, 6)
    assert tuple(reads) == expected


@pytest.mark.parametrize("layer", ["fields", "dynamics", "models"])
@pytest.mark.parametrize(
    "source",
    [
        "def estimate(state):\n    return sum(state.cells.values())",
        "def estimate(state):\n    return state.particles.values()",
        "def estimate(shadow):\n    shadow.step()",
        "def estimate(shadow):\n    shadow.run(100)",
        "def estimate(state):\n    return state.history[-1]",
        "def estimate(state):\n    return state.occupancy",
    ],
)
def test_local_calculation_gate_rejects_world_reads_and_shadow_replay(layer, source):
    assert violations(source, f"event_universe.{layer}.self_field")


def test_locality_rule_covers_self_field_dependencies_and_quantum_exception():
    root = Path(__file__).parents[1]
    definitions = (root / "SIMULATOR_DEFINITIONS.md").read_text()
    assert "LOCALITY-1" in definitions
    assert "shadow worlds" in definitions
    assert "end-to-end" in definitions
    assert "fixed K" in definitions
    assert "Q-ORACLE-1" in definitions
    assert "LOCALITY-1" in (root / "AGENTS.md").read_text()
