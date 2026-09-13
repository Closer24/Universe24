"""Canonical active terminology keeps Node as the single local physical location."""

from pathlib import Path

from event_universe import Simulation
from event_universe.core import disturbance_state
from event_universe.initialization import load_initial_state

ROOT = Path(__file__).resolve().parents[1]


def test_canonical_state_types_use_node_names_after_breaking_migration():
    assert "slots_per_node" in disturbance_state.InitialState.__dataclass_fields__

    disturbance_source = (ROOT / "src/event_universe/core/disturbance_state.py").read_text()
    spatial_source = (ROOT / "src/event_universe/core/spatial_state.py").read_text()
    assert "class DisturbanceNodeState" in disturbance_source
    assert "class NodeView" in disturbance_source
    assert "class SpatialNodeState" in spatial_source


def test_public_simulation_exposes_nodes_as_the_canonical_state_map():
    world = Simulation(load_initial_state(ROOT / "examples/basic.json"))
    assert world.nodes == world.nodes
    assert tuple(world.nodes) == tuple(world.nodes)


def test_terminology_contract_defines_inputs_outputs_as_roles_not_types():
    text = (ROOT / "docs/TERMINOLOGY.md").read_text()
    for term in ("Node", "NodeState", "Scalar", "Vector", "Port", "Link", "Event", "LocalRule"):
        assert f"**{term}**" in text
    assert "Input and output are roles, not value types" in text
    assert "`Node` and `Site` are not separate physical entities" in text
