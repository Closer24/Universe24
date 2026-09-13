"""Cells retain state and rule indices, never laws or executable formulas."""

import json
from annotationlib import Format
from dataclasses import replace
from pathlib import Path
from types import UnionType
from typing import TypeVar, Union, get_args, get_origin, get_type_hints

import pytest

from event_universe import Simulation
from event_universe.core import disturbance_state, spatial_state
from event_universe.core.disturbance_state import Expression
from event_universe.core.node_ports import PortBank
from event_universe.diagnostics.cell_contract import STATE_RECORDS, cell_state_violations
from event_universe.initialization import parse_initial_state

EXAMPLE = Path(__file__).resolve().parents[1] / "examples/local_lorentz_field.json"


def test_cells_and_pending_transactions_remain_formula_free_through_delivery():
    raw = json.loads(EXAMPLE.read_text())
    raw["normal_budget"] = 100
    initial = parse_initial_state(raw)
    world = Simulation(initial)
    pending_seen = False
    for _ in range(32):
        world.step()
        for cell in world.cells.values():
            assert not cell_state_violations(cell)
            pending_seen |= cell.pending is not None
        assert world._spatial is not None
        for cell in world._spatial.cells.values():
            assert not cell_state_violations(cell)
        for packets in (*world.links.values(), *world._spatial.links.values()):
            assert not cell_state_violations(packets)
    assert pending_seen
    # Laws remain legal and shared at initialization, outside evolving owners.
    assert initial.spatial_interactions[0].assignments[0].expression.op == "add"


@pytest.mark.parametrize("bad", [Expression("literal", literal=(1,)), {"op": "add"}, "q * E", lambda: 1])
def test_hidden_formula_objects_are_rejected_inside_record_payloads(bad):
    initial = parse_initial_state(json.loads(EXAMPLE.read_text()))
    record = initial.seeds[0].record
    corrupt = replace(record, values=((bad,),))
    errors = cell_state_violations(corrupt)
    assert errors and "state.values[0][0]" in errors[0]


def test_definition_objects_cannot_be_copied_into_cell_state():
    initial = parse_initial_state(json.loads(EXAMPLE.read_text()))
    corrupt = replace(initial.seeds[0].record, emission_phases=(initial.spatial_interactions[0],))
    assert "SpatialInteractionDefinition" in cell_state_violations(corrupt)[0]


def test_unknown_state_owners_require_explicit_review():
    assert cell_state_violations(object())


def test_declared_state_fields_cannot_hide_optional_laws_in_unexercised_slots():
    namespace = vars(disturbance_state) | vars(spatial_state) | {"PortBank": PortBank}
    allowed = (*STATE_RECORDS, disturbance_state.Departure)

    def inspect(annotation):
        if annotation in (int, type(None), Ellipsis) or annotation in allowed:
            return
        if isinstance(annotation, TypeVar):
            assert annotation.__bound__ is not None
            inspect(annotation.__bound__)
            return
        assert get_origin(annotation) in (tuple, UnionType, Union, PortBank), annotation
        for argument in get_args(annotation):
            inspect(argument)

    for owner in allowed:
        for annotation in get_type_hints(owner, globalns=namespace, format=Format.FORWARDREF).values():
            inspect(annotation)
