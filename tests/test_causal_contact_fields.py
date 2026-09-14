"""Independent causal transport and accounting checks for ordinary wave sources."""

import json
from copy import deepcopy
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import pytest

import event_universe.runner as runner
from event_universe.core.disturbance_state import OPERATIONS, Expression, OperationCosts, unpack
from event_universe.core.event_space import CausalEventSpace
from event_universe.core.node_services import NodeEvents
from event_universe.core.source_envelope_node import EnvelopeGate, EnvelopePacket, SourceEnvelopeNode
from event_universe.core.source_envelope_state import EnvelopeAmplitude, EnvelopeRemainder
from event_universe.diagnostics.node_contract import node_state_violations
from event_universe.fields.source_envelope import local_output
from event_universe.runner import run_initialization

from .support.contact import (
    INVERSE,
    ROTATION,
    configuration,
    localized,
    step,
    world_for,
)
from .support.identity import normalize, observation, renamed_document, reorder_declarations
from .support.quantum import probability

SOURCE = (1, 1, 1)
MIDDLE = (2, 1, 1)
DETECTOR = (3, 1, 1)


def causal_configuration(*, capture=True):
    raw = configuration()
    raw["event_program"]["model"] = "causal-contact-fields-v1"
    raw["event_program"]["tickets"] = [9]
    domain = raw["event_program"]["domains"][0]
    domain["phases"][0][0]["matrix"] = ROTATION
    if not capture:
        domain["capture"]["register_indices"] = []
    for emission in raw["emissions"]:
        emission["amount"] = -25
        emission["budget"] = 1000
    return raw


def frozen_split_configuration():
    raw = causal_configuration(capture=False)
    raw["event_program"]["domains"][0]["phases"] = [
        [{"register_indices": [0, 1], "matrix": ROTATION}],
        *([[]] * 15),
    ]
    return raw


def source_trace(world, monkeypatch):
    observed = []
    original = world._spatial.commit_source

    def record(position, tick, proposal):
        result = original(position, tick, proposal)
        observed.append((position, tick, proposal.source_delta))
        return result

    monkeypatch.setattr(world._spatial, "commit_source", record)
    return observed


def scalar_sources(trace, position=None):
    return [(tick, delta[3][0]) for address, tick, delta in trace if position in (None, address)]


def test_each_local_source_emits_full_strength_times_its_own_weight(monkeypatch):
    world, resolver = world_for(causal_configuration())
    trace = source_trace(world, monkeypatch)
    step(world, 1)
    nodes = resolver.source_nodes()
    assert nodes[SOURCE].amplitude == EnvelopeAmplitude(3, 0, 5)
    assert nodes[MIDDLE].amplitude == EnvelopeAmplitude(4, 0, 5)
    assert nodes[SOURCE].source_id == nodes[MIDDLE].source_id > 0
    assert nodes[DETECTOR].source_id == 0
    assert world.source_totals()["electric_signal"] == (-25,)
    step(world, 1)
    assert scalar_sources(trace, SOURCE) == [(1, -9)]
    assert scalar_sources(trace, MIDDLE) == [(1, -16)]
    assert scalar_sources(trace, DETECTOR) == []
    assert world.source_totals()["electric_signal"] == (-50,)
    assert all(value["balanced"] for value in world.spatial_accounting().values())


def test_local_complex_phase_recombines_before_emitting_full_source_again(monkeypatch):
    raw = causal_configuration(capture=False)
    raw["event_program"]["domains"][0]["phases"] = [
        [{"register_indices": [0, 1], "matrix": ROTATION}],
        [{"register_indices": [0, 1], "matrix": INVERSE}],
        [],
    ]
    world, resolver = world_for(raw)
    trace = source_trace(world, monkeypatch)
    step(world, 3)
    assert resolver.source_nodes()[SOURCE].amplitude == EnvelopeAmplitude(1)
    assert resolver.source_nodes()[MIDDLE].amplitude == EnvelopeAmplitude()
    assert probability(resolver.space.query(0)) == 1
    assert localized(world) == []
    step(world, 1)
    assert scalar_sources(trace, SOURCE)[-1] == (3, -25)
    assert scalar_sources(trace, MIDDLE)[-1] == (3, 0)


def test_source_evolution_does_not_query_a_quantum_probability(monkeypatch):
    world, resolver = world_for(frozen_split_configuration())

    def forbidden(*args, **kwargs):
        raise AssertionError("ordinary source evolution requested a quantum query")

    monkeypatch.setattr(resolver.space, "query", forbidden)
    step(world, 6)
    assert resolver.source_nodes()[SOURCE].amplitude == EnvelopeAmplitude(3, 0, 5)
    assert world.source_totals()["electric_signal"] == (-150,)


def test_local_source_preparation_cannot_consume_origin_status_or_audit_outputs(monkeypatch):
    world, resolver = world_for(causal_configuration(capture=False))
    step(world, 1)

    def forbidden(*args, **kwargs):
        raise AssertionError("local source law attempted a nonlocal or diagnostic read")

    monkeypatch.setattr(resolver.space.waves, "relevant", forbidden)
    monkeypatch.setattr(resolver.space, "query", forbidden)
    monkeypatch.setattr(resolver, "inventory", forbidden)
    monkeypatch.setattr(resolver, "report", forbidden)
    proposal = resolver.prepare_source(SOURCE, 1, world._spatial.nodes[SOURCE].states, 0)
    assert proposal.source_delta[3] == (-9,)


def test_remote_capture_preserves_local_source_prefix_until_terminal_delivery(monkeypatch):
    raw = causal_configuration()
    absent = deepcopy(raw)
    absent["seeds"].pop(2)
    measured, measured_resolver = world_for(raw)
    unmeasured, unmeasured_resolver = world_for(absent)
    measured_trace = source_trace(measured, monkeypatch)
    unmeasured_trace = source_trace(unmeasured, monkeypatch)

    def local_costs(resolver):
        return [
            (event.tick, event.kind, event.model_cost)
            for event in resolver.events.events
            if event.owner == "source-envelope" and event.addresses == (SOURCE,)
        ]

    for _ in range(4):
        step(measured, 1)
        step(unmeasured, 1)
        assert measured_resolver.source_nodes()[SOURCE].amplitude == (
            unmeasured_resolver.source_nodes()[SOURCE].amplitude
        )
        assert measured.spatial_values(SOURCE) == unmeasured.spatial_values(SOURCE)
        assert local_costs(measured_resolver) == local_costs(unmeasured_resolver)
        assert measured.nodes[SOURCE].delay_counts == unmeasured.nodes[SOURCE].delay_counts
    assert any(cost > 0 for _, _, cost in local_costs(measured_resolver))
    assert localized(measured) == [(DETECTOR, 1)]
    assert localized(unmeasured) == []
    origin = measured_resolver.space.waves.names["charge_mode"]
    assert measured.event_space.resolution(origin) is not None
    assert not measured_resolver.space.waves.banks[SOURCE].origins
    assert not measured_resolver.source_nodes()[SOURCE].retired
    step(measured, 1)
    step(unmeasured, 1)
    assert scalar_sources(measured_trace, SOURCE) == scalar_sources(unmeasured_trace, SOURCE)
    assert scalar_sources(measured_trace, SOURCE)[-1] == (4, -9)
    assert measured_resolver.source_nodes()[SOURCE].retired == origin
    assert not unmeasured_resolver.source_nodes()[SOURCE].retired


def test_capture_has_one_full_localized_source_and_no_duplicate_envelope(monkeypatch):
    world, resolver = world_for(causal_configuration())
    trace = source_trace(world, monkeypatch)
    step(world, 4)
    assert localized(world) == [(DETECTOR, 1)]
    assert resolver.source_nodes()[DETECTOR].retired
    assert resolver.source_nodes()[DETECTOR].amplitude == EnvelopeAmplitude()
    before = world.source_totals()["electric_signal"][0]
    step(world, 1)
    emitted = world.source_totals()["electric_signal"][0] - before
    envelope_emitted = sum(delta[3][0] for _, tick, delta in trace if tick == 4)
    assert emitted - envelope_emitted == -25
    assert not [entry for entry in trace if entry[0] == DETECTOR and entry[1] >= 4]
    assert resolver.report()["quantum_inventory"]["charge"] == (0,)


def test_null_measurement_zeros_only_the_local_envelope_without_remote_renormalization(monkeypatch):
    raw = causal_configuration()
    raw["event_program"]["tickets"] = [0]
    raw["event_program"]["domains"][0]["phases"].extend([[], [], []])
    world, resolver = world_for(raw)
    trace = source_trace(world, monkeypatch)
    step(world, 4)
    origin = resolver.space.waves.names["charge_mode"]
    assert world.event_space.resolution(origin) is None
    assert localized(world) == []
    assert resolver.source_nodes()[DETECTOR].amplitude == EnvelopeAmplitude()
    assert not resolver.source_nodes()[DETECTOR].retired
    assert resolver.source_nodes()[SOURCE].amplitude == EnvelopeAmplitude(3, 0, 5)
    # The conditional quantum audit can change; ordinary emission does not read it.
    assert probability(resolver.space.query(0)) == 1
    step(world, 1)
    assert scalar_sources(trace, SOURCE)[-1] == (4, -9)
    assert scalar_sources(trace, DETECTOR)[-1] == (4, 0)


def test_null_and_capture_reserve_the_same_local_controller_cost():
    costs = []
    for ticket in (0, 9):
        raw = causal_configuration()
        raw["event_program"]["tickets"] = [ticket]
        world, resolver = world_for(raw)
        step(world, 4)
        costs.append(world.nodes[DETECTOR].committed_cost)
        assert resolver.draws == 1
        assert resolver.space.records[-1].outcome == int(ticket == 9)
    assert costs[0] == costs[1] > 0


@pytest.mark.parametrize("link_ticks,budget,first_commit", [(1, 50, 2), (3, 10000, 3)])
def test_envelope_waits_for_both_link_transit_and_local_computation(link_ticks, budget, first_commit):
    raw = causal_configuration(capture=False)
    raw["emissions"] = raw["emissions"][1:]
    raw["link_ticks"], raw["normal_budget"] = link_ticks, budget
    world, resolver = world_for(raw)
    assert resolver.report()["source_gate_commit_offset"] == first_commit
    assert resolver.report()["source_gate_period"] == first_commit + link_ticks
    step(world, first_commit - 1)
    assert resolver.source_nodes()[SOURCE].amplitude == EnvelopeAmplitude(1)
    assert resolver.source_nodes()[MIDDLE].amplitude == EnvelopeAmplitude()
    assert resolver.source_nodes()[DETECTOR].amplitude == EnvelopeAmplitude()
    step(world, 1)
    assert resolver.source_nodes()[SOURCE].amplitude == EnvelopeAmplitude(3, 0, 5)
    assert resolver.source_nodes()[MIDDLE].amplitude == EnvelopeAmplitude(4, 0, 5)
    assert resolver.source_nodes()[DETECTOR].amplitude == EnvelopeAmplitude()


def test_emission_wait_retains_frozen_amount_before_a_later_envelope_change(monkeypatch):
    raw = causal_configuration(capture=False)
    # Source preparation alone fits this budget; its eight local population
    # deposits must also be priced, so the complete cycle requires a delay.
    raw["normal_budget"] = 60
    raw["emissions"] = raw["emissions"][1:]
    world, resolver = world_for(raw)
    trace = source_trace(world, monkeypatch)
    step(world, 2)
    pending = resolver.source_nodes()[SOURCE].pending_emission
    assert pending is not None and pending.ready_tick == 2
    assert pending.cost > raw["normal_budget"]
    assert pending.source_delta[3] == (-25,)
    assert resolver.source_nodes()[SOURCE].amplitude == EnvelopeAmplitude(3, 0, 5)
    assert scalar_sources(trace, SOURCE) == []
    step(world, 1)
    assert scalar_sources(trace, SOURCE) == [(2, -25)]


def test_local_null_during_pending_gate_keeps_the_later_neighbor_contribution():
    raw = causal_configuration()
    raw["normal_budget"] = 50
    raw["emissions"] = raw["emissions"][1:]
    raw["event_program"]["domains"][0]["capture"]["register_indices"] = [1]
    raw["seeds"][2]["position"] = list(MIDDLE)
    world, resolver = world_for(raw)
    step(world, 1)
    target = resolver.source_nodes()[MIDDLE]
    assert target.pending_gate is not None
    assert target.amplitude == EnvelopeAmplitude()
    assert resolver.space.records[-1].outcome == 0
    step(world, 1)
    assert target.amplitude == EnvelopeAmplitude(4, 0, 5)
    assert target.source_id == resolver.source_nodes()[SOURCE].source_id > 0
    assert probability(resolver.space.query(1)) == Fraction(16, 25)
    assert not target.retired
    step(world, 1)
    assert localized(world) == [(MIDDLE, 1)]


def test_null_during_frozen_pair_preserves_the_complete_unitary_snapshot():
    costs = OperationCosts((1,) * len(OPERATIONS))
    events = NodeEvents(None, None)
    left = SourceEnvelopeNode(SOURCE, source_id=1, amplitude=EnvelopeAmplitude(3, 0, 5))
    right = SourceEnvelopeNode(MIDDLE, source_id=1, amplitude=EnvelopeAmplitude(4, 0, 5))
    matrices = tuple(
        tuple(tuple((value, 0) for value in row) for row in matrix) for matrix in (ROTATION, INVERSE)
    )
    for epoch in range(2):
        tick = epoch * 2
        left.start_gate(tick, epoch, EnvelopeGate(epoch, 0, 0), 0, 1, 1, 4, events)
        right.start_gate(tick, epoch, EnvelopeGate(epoch, 1, 1), 0, 1, 1, 4, events)
        from_left, from_right = left.output[0], right.output[1]
        right.receive(from_left, tick + 1, 1, 0, events, costs=costs)
        left.receive(from_right, tick + 1, 1, 0, events, costs=costs)
        left.clear_output(0, from_left)
        right.clear_output(1, from_right)
        if epoch == 0:
            left.null(tick + 1, None)
            assert left.amplitude == EnvelopeAmplitude()
            assert left.pending_gate.amplitude == EnvelopeAmplitude(3, 0, 5)
        left.complete(tick + 2, local_output, matrices, costs, (0,), 0, 1, events)
        right.complete(tick + 2, local_output, matrices, costs, (1,), 0, 1, events)
        if epoch == 0:
            assert (left.amplitude, right.amplitude) == (
                EnvelopeAmplitude(-7, 0, 25),
                EnvelopeAmplitude(24, 0, 25),
            )
    assert (left.amplitude, right.amplitude) == (EnvelopeAmplitude(3, 0, 5), EnvelopeAmplitude(4, 0, 5))


def test_duplicate_terminal_is_charged_without_restarting_or_forwarding():
    costs = OperationCosts(
        tuple(7 if name == "receive" else 3 if name == "read" else 1 for name in OPERATIONS)
    )
    space = CausalEventSpace(20)
    events = NodeEvents(space, None)
    node = SourceEnvelopeNode(SOURCE, source_id=7, amplitude=EnvelopeAmplitude(1))
    first = EnvelopePacket(1, MIDDLE, 1, 7, None)
    node.receive(first, 1, 1, 0, events, costs=costs)
    assert node.complete(1, local_output, (), costs, (0,), 0, 1, events)
    assert node.retired == 7
    outputs, generation, cause = node.output, node.generation, node.cause_id
    assert outputs[6] is not None
    duplicate = EnvelopePacket(2, MIDDLE, 1, 7, None)
    node.receive(duplicate, 2, 1, 5, events, costs=costs)
    assert space.events[-1].kind == "source-terminal-ignored"
    assert space.events[-1].model_cost == costs.price("receive") + costs.price("read") == 10
    assert node.pending_stop is None
    assert node.output is outputs
    assert node.generation == generation and node.cause_id == cause
    assert node.amplitude == EnvelopeAmplitude() and node.retired == 7


def test_terminal_commits_before_later_amplitude_and_prevents_resurrection():
    costs = OperationCosts((1,) * len(OPERATIONS))
    space = CausalEventSpace(20)
    events = NodeEvents(space, None)
    node = SourceEnvelopeNode(SOURCE, source_id=7, amplitude=EnvelopeAmplitude(3, 0, 5))
    node.start_gate(0, 0, EnvelopeGate(0, 0, 0), 2, 1, 1, 4, events)
    node.receive(EnvelopePacket(1, MIDDLE, 1, 7, None), 1, 1, 1, events, costs=costs)

    def forbidden(*args, **kwargs):
        raise AssertionError("a retired source must not evaluate a late amplitude")

    assert node.pending_stop.ready_tick == 2
    assert node.pending_gate.ready_tick == 4
    node.complete(2, forbidden, (), costs, (0,), 0, 1, events)
    assert node.retired == 7 and node.amplitude == EnvelopeAmplitude()
    outputs = node.output
    arriving = EnvelopePacket(3, MIDDLE, 1, 7, EnvelopeAmplitude(4, 0, 5), epoch=0)
    node.receive(arriving, 3, 1, 1, events, costs=costs)
    assert node.incoming_gate is arriving
    node.complete(4, forbidden, (), costs, (0,), 0, 1, events)
    assert node.retired == node.source_id == 7
    assert node.amplitude == EnvelopeAmplitude()
    assert node.pending_gate is None and node.incoming_gate is None
    assert node.output is outputs
    assert not [event for event in space.events if event.kind == "source-gate-committed"]


def test_terminal_notice_waits_at_every_intermediate_node():
    raw = causal_configuration()
    raw["emissions"] = raw["emissions"][1:]
    raw["normal_budget"] = 50
    raw["operation_costs"]["receive"] = 100
    world, resolver = world_for(raw)
    for _ in range(50):
        step(world, 1)
        captures = [
            t for t in resolver.report()["contact_transfers"] if t["direction"] == "to_localized"
        ]
        if captures:
            break
    assert captures
    capture_tick = captures[0]["tick"]
    origin = resolver.source_nodes()[DETECTOR].retired
    assert world.tick == capture_tick
    step(world, 1)
    middle = resolver.source_nodes()[MIDDLE]
    assert middle.pending_stop.ready_tick == capture_tick + 3
    assert not middle.retired and not resolver.source_nodes()[SOURCE].retired
    step(world, 1)
    assert not middle.retired
    step(world, 1)
    assert middle.retired == origin
    assert not resolver.source_nodes()[SOURCE].retired
    step(world, 1)
    source = resolver.source_nodes()[SOURCE]
    assert source.pending_stop.ready_tick == capture_tick + 6
    step(world, 1)
    assert not source.retired
    step(world, 1)
    assert source.retired == origin


def test_finite_allowances_survive_ticks_and_are_never_refilled(monkeypatch):
    raw = frozen_split_configuration()
    for emission in raw["emissions"]:
        emission["budget"] = 10
    world, resolver = world_for(raw)
    trace = source_trace(world, monkeypatch)
    step(world, 12)
    assert world.source_totals()["electric_signal"] == (-30,)
    assert sum(value for _, value in scalar_sources(trace, SOURCE)) == -10
    assert sum(value for _, value in scalar_sources(trace, MIDDLE)) == -10
    for position in (SOURCE, MIDDLE):
        state = resolver.source_nodes()[position].emission_state
        assert all(not any(unpack(value)) for value in state.remaining)
    before = world.source_totals()
    step(world, 4)
    assert world.source_totals() == before


def test_integer_fractional_sources_accumulate_without_loss(monkeypatch):
    raw = frozen_split_configuration()
    for emission in raw["emissions"]:
        emission["amount"] = -1
    world, resolver = world_for(raw)
    trace = source_trace(world, monkeypatch)
    step(world, 6)
    assert [v for _, v in scalar_sources(trace, SOURCE)] == [0, 0, -1, 0, 0]
    assert [v for _, v in scalar_sources(trace, MIDDLE)] == [0, -1, 0, -1, -1]
    assert resolver.source_nodes()[SOURCE].emission_state.remainders[1] == (EnvelopeRemainder(-4, 5),)
    assert resolver.source_nodes()[MIDDLE].emission_state.remainders[1] == (EnvelopeRemainder(-1, 5),)
    assert world.source_totals()["electric_signal"] == (-5,)


@pytest.mark.parametrize("axis,direction", [(a, s) for a in range(3) for s in (-1, 1)])
def test_source_and_terminal_packets_cross_every_periodic_world_seam(axis, direction):
    raw = causal_configuration()
    raw["shape"], raw["boundary"] = [7, 7, 7], "periodic"
    origin = [3, 3, 3]
    origin[axis] = 6 if direction == 1 else 0
    positions = []
    for distance in range(3):
        position = origin.copy()
        position[axis] = (origin[axis] + direction * distance) % 7
        positions.append(position)
    raw["event_program"]["addresses"] = positions
    raw["seeds"][0]["position"] = positions[0]
    raw["seeds"][1]["position"] = positions[0]
    raw["seeds"][2]["position"] = positions[2]
    world, resolver = world_for(raw)
    step(world, 1)
    assert resolver.source_nodes()[tuple(positions[1])].amplitude == EnvelopeAmplitude(4, 0, 5)
    assert resolver.source_nodes()[tuple(positions[2])].amplitude == EnvelopeAmplitude()
    step(world, 3)
    assert localized(world) == [(tuple(positions[2]), 1)]
    assert not resolver.source_nodes()[tuple(positions[0])].retired
    step(world, 1)
    assert all(node.retired for node in resolver.source_nodes().values())


def test_periodic_extent_two_uses_opposite_ports_in_both_gate_orders_on_every_axis():
    for axis in range(3):
        for reverse in (False, True):
            raw = causal_configuration()
            raw["shape"], raw["boundary"] = [3, 3, 3], "periodic"
            raw["shape"][axis] = 2
            first, second = [1, 1, 1], [1, 1, 1]
            first[axis], second[axis] = 0, 1
            raw["event_program"]["addresses"] = [first, second]
            domain = raw["event_program"]["domains"][0]
            domain["register_indices"] = [0, 1]
            domain["capture"]["register_indices"] = [1]
            domain["phases"] = [
                [{"register_indices": [1, 0] if reverse else [0, 1], "matrix": ROTATION}]
            ]
            raw["seeds"][0]["position"] = first
            raw["seeds"][1]["position"] = first
            raw["seeds"][2]["position"] = second
            world, resolver = world_for(raw)
            step(world, 1)
            nodes = resolver.source_nodes()
            assert nodes[tuple(second)].amplitude == EnvelopeAmplitude(-4 if reverse else 4, 0, 5)
            step(world, 1)
            assert localized(world) == [(tuple(second), 1)]
            assert all(node.retired for node in nodes.values())


@pytest.mark.parametrize("change", ["rename", "reorder", "both"])
def test_generic_field_and_disturbance_labels_do_not_select_source_behavior(change):
    raw = causal_configuration()
    transformed, fields, types = renamed_document(raw)
    if change == "reorder":
        transformed, fields, types = deepcopy(raw), {}, {}
    if change != "rename":
        reorder_declarations(transformed)
    events, other_events = [], []
    world, resolver = world_for(raw, observer=events.append)
    other, other_resolver = world_for(transformed, observer=other_events.append)
    for _ in range(6):
        world.step()
        other.step()
        assert world.totals()["charge"] == (-1,)
        assert world.totals()["mass"] == (1,)
        assert normalize(observation(world, events), {}, {}) == normalize(
            observation(other, other_events), fields, types
        )
        assert [record.outcome for record in resolver.space.records] == [
            record.outcome for record in other_resolver.space.records
        ]
    assert localized(world) == [(DETECTOR, 1)]
    assert resolver.draws == other_resolver.draws == 1
    assert world.source_totals()["electric_signal"][0] < 0


def test_all_evolving_source_records_are_formula_free_with_injected_counterexample():
    world, resolver = world_for(causal_configuration())
    for count in (1, 2, 3):
        step(world, count)
        assert all(not node_state_violations(node) for node in world._nodes.values())
        assert all(not node_state_violations(node) for node in resolver.source_nodes().values())
    fresh, _ = world_for(causal_configuration())
    step(fresh, 2)
    source = fresh._resolver.source_nodes()[SOURCE]
    # A nested field in otherwise admitted local DTOs must not hide an expression.
    source.emission_state = replace(
        source.emission_state, remainders=(Expression("literal", literal=(1,)),)
    )
    assert any("Expression" in error for error in node_state_violations(fresh._nodes[SOURCE]))


def test_new_profile_runs_headlessly_through_the_primary_runner(tmp_path):
    raw = causal_configuration()
    initial = tmp_path / "causal_contact.json"
    initial.write_text(json.dumps(raw), encoding="utf-8")
    output = tmp_path / "run"
    run_initialization(initial, output)
    report = json.loads((output / "run.json").read_text(encoding="utf-8"))
    assert report["computation"]["resolver"]["model"] == "causal-contact-fields-v1"
    assert report["computation"]["resolver"]["classical_field_source"] == "causal_local_envelope"
    assert len(report["computation"]["resolver"]["contact_transfers"]) == 2
    assert not list(output.glob("*.html"))
    assert not list(output.glob("*.png"))


def test_checked_in_causal_charge_example_has_one_capture_and_balanced_tick_reports(
    tmp_path, monkeypatch
):
    example = Path(__file__).resolve().parents[1] / "examples/quantum/causal_charge.json"
    observed = []
    original_step = runner.Simulation.step

    def checked_step(world):
        original_step(world)
        report = world.computation_report()["resolver"]
        assert world.totals()["charge"] == (-1,)
        assert world.totals()["mass"] == (1,)
        assert all(value["balanced"] for value in world.spatial_accounting().values())
        assert report["model"] == "causal-contact-fields-v1"
        assert len(report["source_envelopes"]) == 3
        retired = sum(node["retired"] for node in report["source_envelopes"])
        if world.tick >= 5:
            assert retired == 3
        observed.append((world.tick, world.source_totals()["electric_signal"][0], retired))

    monkeypatch.setattr(runner.Simulation, "step", checked_step)
    output = tmp_path / "checked_in_example"
    run_initialization(example, output)
    report = json.loads((output / "run.json").read_text(encoding="utf-8"))
    resolver = report["computation"]["resolver"]
    captures = [entry for entry in resolver["contact_transfers"] if entry["direction"] == "to_localized"]
    assert len(captures) == 1 and captures[0]["tick"] == 3
    assert resolver["random_draws"] == 1
    assert [tick for tick, _, _ in observed] == list(range(1, 11))
    assert [amount for _, amount, _ in observed] == [
        -25,
        -50,
        -75,
        -100,
        -134,
        -159,
        -159,
        -159,
        -159,
        -159,
    ]
    assert report["completed_ticks"] == report["requested_ticks"] == 10
    assert report["source_totals"]["electric_signal"] == [-159]
    assert report["final_totals"]["charge"] == [-1]
    assert report["final_totals"]["mass"] == [1]
    assert report["accounting_balanced_at_every_completed_tick"]
    assert report["conserved_at_every_completed_tick"]
    assert report["display"] == "none"
    assert not list(output.glob("*.html"))
    assert not list(output.glob("*.png"))


def test_existing_localized_profile_retains_its_original_field_source_policy():
    world, resolver = world_for(configuration())
    step(world, 8)
    assert resolver.report()["classical_field_source"] == "localized_events_only"
    assert world.source_totals()["electric_signal"] == (-18,)
    assert not hasattr(resolver, "source_nodes")
    assert probability(resolver.space.query(0)) == Fraction(0)
