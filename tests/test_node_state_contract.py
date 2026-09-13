"""Nodes retain state and rule indices, never laws or executable formulas."""

import json
from annotationlib import Format
from dataclasses import replace
from pathlib import Path
from types import UnionType
from typing import Union, get_args, get_origin, get_type_hints

import pytest

from event_universe import Simulation
from event_universe.core import disturbance_state, spatial_state
from event_universe.core.disturbance_state import Expression
from event_universe.diagnostics.node_contract import STATE_RECORDS, node_state_violations
from event_universe.initialization import parse_initial_state

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/local_lorentz_field.json"


def test_nodes_and_pending_transactions_remain_formula_free_through_delivery():
    raw = json.loads(EXAMPLE.read_text())
    raw["normal_budget"] = 100
    initial = parse_initial_state(raw)
    world = Simulation(initial)
    pending_seen = False
    for _ in range(32):
        world.step()
        for node in world.nodes.values():
            assert not node_state_violations(node)
            pending_seen |= node.pending is not None
        assert world._spatial is not None
        for node in world._spatial.cells.values():  # legacy internal map pending versioned migration
            assert not node_state_violations(node)
        for packets in (*world.links.values(), *world._spatial.links.values()):
            assert not node_state_violations(packets)
    assert pending_seen
    assert initial.spatial_interactions[0].assignments[0].expression.op == "add"


@pytest.mark.parametrize("bad", [Expression("literal", literal=(1,)), {"op": "add"}, "q * E", lambda: 1])
def test_hidden_formula_objects_are_rejected_inside_record_payloads(bad):
    initial = parse_initial_state(json.loads(EXAMPLE.read_text()))
    record = initial.seeds[0].record
    corrupt = replace(record, values=((bad,),))
    errors = node_state_violations(corrupt)
    assert errors and "state.values[0][0]" in errors[0]


def test_definition_objects_cannot_be_copied_into_node_state():
    initial = parse_initial_state(json.loads(EXAMPLE.read_text()))
    corrupt = replace(initial.seeds[0].record, emission_phases=(initial.spatial_interactions[0],))
    assert "SpatialInteractionDefinition" in node_state_violations(corrupt)[0]


def test_unknown_state_owners_require_explicit_review():
    assert node_state_violations(object())


def test_declared_state_fields_cannot_hide_optional_laws_in_unexercised_slots():
    namespace = vars(disturbance_state) | vars(spatial_state)
    allowed = (*STATE_RECORDS, disturbance_state.Departure)

    def inspect(annotation):
        if annotation in (int, type(None), Ellipsis) or annotation in allowed:
            return
        assert get_origin(annotation) in (tuple, UnionType, Union), annotation
        for argument in get_args(annotation):
            inspect(argument)

    for owner in allowed:
        for annotation in get_type_hints(owner, globalns=namespace, format=Format.FORWARDREF).values():
            inspect(annotation)


def test_legacy_cell_names_are_aliases_not_physical_types():
    assert disturbance_state.DisturbanceCell is disturbance_state.DisturbanceNodeState
    assert disturbance_state.CellView is disturbance_state.NodeView
    assert spatial_state.SpatialCell is spatial_state.SpatialNodeState
