"""Nodes retain state and rule indices, never laws or executable formulas."""

import json
from annotationlib import Format
from dataclasses import replace
from pathlib import Path
from types import UnionType
from typing import TypeVar, Union, get_args, get_origin, get_type_hints

import pytest

from event_universe import Simulation
from event_universe.core import (
    disturbance_state,
    source_emission,
    source_emission_node,
    source_envelope_node,
    source_envelope_state,
    spatial_state,
)
from event_universe.core.disturbance_node import DisturbanceNode
from event_universe.core.disturbance_state import Expression, pack
from event_universe.core.node_ports import PortBank
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
        for node in world._spatial.nodes.values():  # legacy internal map pending versioned migration
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


def test_field_rule_guard_is_recursively_audited_instead_of_hiding_nested_laws():
    guard = spatial_state.FieldRuleGuard(0, ((1,),), (((1,),),) * 6)
    assert not node_state_violations(guard)
    corrupt = replace(guard, outgoing=((Expression("literal", literal=(1,)),),))
    errors = node_state_violations(corrupt)
    assert errors and "state.outgoing[0][0]" in errors[0]


def test_declared_state_fields_cannot_hide_optional_laws_in_unexercised_slots():
    namespace = (
        vars(disturbance_state)
        | vars(spatial_state)
        | vars(source_envelope_state)
        | vars(source_envelope_node)
        | vars(source_emission)
        | vars(source_emission_node)
    )
    allowed = (*STATE_RECORDS, disturbance_state.Departure)

    def inspect(annotation):
        if annotation in (int, type(None), Ellipsis) or annotation in allowed:
            return
        if isinstance(annotation, TypeVar):
            inspect(annotation.__bound__)
            return
        assert get_origin(annotation) in (tuple, UnionType, Union, PortBank), annotation
        for argument in get_args(annotation):
            inspect(argument)

    for owner in allowed:
        for annotation in get_type_hints(owner, globalns=namespace, format=Format.FORWARDREF).values():
            inspect(annotation)


def envelope_node_with_pending_state():
    amplitude = source_envelope_state.EnvelopeAmplitude(3, 0, 5)
    gate = source_envelope_node.EnvelopeGate(4, 0, 0)
    outgoing = source_envelope_node.EnvelopePacket(5, (1, 1, 1), 0, 7, amplitude, 2, 9)
    terminal = source_envelope_node.EnvelopePacket(6, (1, 1, 1), 1, 7, None, cause_id=10)
    emission = source_emission.EnvelopeEmissionState(
        ((source_envelope_state.EnvelopeRemainder(1, 5),),), (pack((0,)),), (pack((20,)),)
    )
    source = source_emission_node.EmittingEnvelopeNode(
        (1, 1, 1),
        source_id=7,
        amplitude=amplitude,
        pending_gate=source_envelope_node.PendingEnvelopeGate(2, 8, 7, amplitude, 0, gate),
        incoming_gate=source_envelope_node.EnvelopePacket(
            4, (2, 1, 1), 1, 7, source_envelope_state.EnvelopeAmplitude(4, 0, 5), 2, 8
        ),
        pending_stop=source_envelope_node.PendingEnvelopeStop(9, 7, 10),
        output=(outgoing,) + (None,) * 6 + (terminal,) + (None,) * 10,
        emission_state=emission,
        pending_emission=source_emission.PendingEnvelopeEmission(
            7, 10, 7, ((pack((3,)),) * 8,), (pack((24,)),), emission, 17, 11
        ),
    )
    return DisturbanceNode((), (), position=(1, 1, 1), source_envelope=source)


def test_complete_node_envelope_packets_and_pending_emission_remain_formula_free():
    node = envelope_node_with_pending_state()
    assert not node_state_violations(node)
    source = node.source_envelope
    assert source is not None
    assert source.pending_gate is not None and source.incoming_gate is not None
    assert source.pending_stop is not None and source.pending_emission is not None
    assert sum(packet is not None for packet in source.output) == 2
    assert not node_state_violations(source.output)


@pytest.mark.parametrize("location", ["pending_gate", "incoming_gate", "output", "pending_emission"])
@pytest.mark.parametrize("bad", [Expression("literal", literal=(1,)), lambda: 1, {"nodes": ()}])
def test_source_envelope_nested_payloads_cannot_hide_formulas_or_engine_data(location, bad):
    node = envelope_node_with_pending_state()
    source = node.source_envelope
    assert source is not None
    if location == "pending_gate":
        source.pending_gate = replace(source.pending_gate, gate=bad)
    elif location == "incoming_gate":
        object.__setattr__(source.incoming_gate, "amplitude", bad)
    elif location == "output":
        packet = source.output[0]
        object.__setattr__(packet, "amplitude", bad)
    else:
        pending = source.pending_emission
        following = replace(pending.following, remainders=((bad,),))
        source.pending_emission = replace(pending, following=following)
    errors = node_state_violations(node)
    assert errors and f"state.source_envelope.{location}" in errors[0]


def test_source_envelope_cannot_retain_the_simulation_owner():
    initial = parse_initial_state(json.loads(EXAMPLE.read_text()))
    world = Simulation(initial)
    node = envelope_node_with_pending_state()
    source = node.source_envelope
    assert source is not None
    source.pending_emission = replace(source.pending_emission, following=world)
    errors = node_state_violations(node)
    assert errors and "state.source_envelope.pending_emission.following" in errors[0]


def test_source_planner_results_do_not_gain_unreviewed_state_permission():
    # A temporary planner result is not retained by EmittingEnvelopeNode.
    proposal = source_emission.SourceDeposit((), ())
    assert "SourceDeposit" in node_state_violations(proposal)[0]
