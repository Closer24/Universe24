"""Fixed neighborhood access and explicit rejection of shadow-world dependencies."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from event_universe.core.engine import Engine
from event_universe.core.lattice import PeriodicLattice

from .architecture_rules import violations


@pytest.mark.parametrize("extent", [8, 1_000_000])
def test_particle_response_reads_only_its_delivered_faces_independent_of_extent(extent):
    # A read spy, not a simulated world; nonzero data prevents an all-zero bypass.
    position = (3, 3, 3)
    reads = []

    def delivered(address):
        assert address == position
        reads.append(address)
        return (1, 2, 3, 4, 5, 6)

    def forbidden(*args):
        raise AssertionError("particle response attempted a remote scalar read")

    reader = SimpleNamespace(
        _lattice=PeriodicLattice((extent,) * 3),
        phi=forbidden,
        _neighbor_values=forbidden,
        face_at=delivered,
        _response_snapshot=None,
    )
    assert Engine._particle_neighbors(reader, position) == (1, 2, 3, 4, 5, 6)
    assert reads == [position]


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
