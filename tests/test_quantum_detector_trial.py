"""Acceptance contracts for the isolated terminal detector integration trial."""

import dataclasses
import json
from pathlib import Path

import pytest

from event_universe import Config
from event_universe import ScalarSimulation as Simulation
from event_universe.core.state import MAX_CORE_INT
from event_universe.diagnostics.numeric_audit import static_integer_audit
from event_universe.diagnostics.recorder import TraceRecorder
from event_universe.integration.quantum_bridge import QuantumBridge
from event_universe.quantum import QuantumConfig
from event_universe.quantum.terminal import TerminalSetup, choose_output
from event_universe.retention import ArtifactLease, validate_output_path

from .quantum_detector_fixture import DetectorController, prepare


def snapshot(world, trace):
    return (
        world.tick,
        world.faulted,
        dict(world.cells),
        dict(world.particles),
        dict(world.occupancy),
        world.active,
        dict(trace.paths),
        tuple(trace.force_records),
        tuple(trace.collisions),
    )


@pytest.mark.parametrize(
    "phase,weights,counts",
    [(0, (4, 0), (4, 0)), (1, (2, 2), (2, 2)), (2, (0, 4), (0, 4)), (3, (2, 2), (2, 2))],
)
def test_exhaustive_uniform_tickets(phase, weights, counts):
    observed = [0, 0]
    for ticket in range(4):
        q, b = prepare(phase)
        assert q.terminal_evaluated_nodes == 0
        r = b.read_terminal_trial(8, ticket)
        assert (r.record.weight_a, r.record.weight_b) == weights
        assert r.cost == (1, 0) and r.evaluation_nodes > 0
        assert q.terminal_calls == 1
        observed[r.record.detector] += 1
    assert tuple(observed) == counts


def test_actual_engine_and_single_detector_record():
    config = Config(nx=12, ny=12, nz=12)
    ct, wt = TraceRecorder(), TraceRecorder()
    control, world = Simulation(config, observer=ct), Simulation(config, observer=wt)
    for e in (control, world):
        e.add_particle(90, 10, 9, 8, 1, 0, 0)  # Background object, not quantum excitation.
    q, b = prepare(1)
    c = DetectorController(world, b)
    for _ in range(8):
        control.step()
        world.step()
    before = snapshot(world, wt)
    record = c.commit(0)
    work = q.terminal_evaluated_nodes
    assert record.detector == 0 and c.detector_bits == (1, 0)
    assert record.tick == world.tick == 8
    assert snapshot(world, wt) == before
    for ticket in (1, 2, 3, 0):
        assert c.commit(ticket) is record
    assert sum(c.detector_bits) == 1
    assert q.terminal_evaluated_nodes == work and q.terminal_calls == 5
    assert snapshot(world, wt) == snapshot(control, ct)
    for _ in range(4):
        world.step()
        control.step()
    assert snapshot(world, wt) == snapshot(control, ct)
    output = Path("artifacts/quantum-detector-results.json")
    payload = json.dumps(
        {
            "base_commit": "e74f2fdf390b5dc8036b707eefcfc53bc8a82c17",
            "baseline_src_tree": "18253dfaca7208b9f5f8d4e4f4bf7cc48fd579d7",
            "test_model": "terminal-two-output-trial-v1",
            "world_tick_at_readout": record.tick,
            "world_ticks_consumed_by_query": 0,
            "model_cost_per_successful_readout": 1,
            "first_readout_host_evaluated_nodes": work,
            "repeated_calls": 4,
            "extra_host_nodes_on_repeats": q.terminal_evaluated_nodes - work,
            "detector_bits": list(c.detector_bits),
            "detector_record_count": 1,
            "record": dataclasses.asdict(record),
            "main_state_unchanged_by_query": True,
            "continuation_matches_baseline_through_tick": world.tick,
            "event_is_test_controller_record_not_native_engine_event": True,
            "sampling_test": "Exhaustive integer tickets; no RNG tested",
        },
        indent=2,
    )
    validate_output_path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.touch(exist_ok=True)
    with ArtifactLease(output.parent, [output.absolute()]):
        output.write_text(payload, encoding="utf-8")


def test_two_bridges_share_result():
    q, a = prepare(1)
    b = QuantumBridge(q)
    first = a.read_terminal_trial(8, 0)
    second = b.read_terminal_trial(8, 3)
    assert second.record is first.record
    assert second.repeated == 1 and second.evaluation_nodes == 0
    with pytest.raises(dataclasses.FrozenInstanceError):
        second.record.detector = 1


@pytest.mark.parametrize("ticket", [-1, 4, MAX_CORE_INT + 1, True, 0.5])
def test_bad_ticket_never_commits(ticket):
    q, b = prepare(1)
    with pytest.raises((ValueError, TypeError, OverflowError)):
        b.read_terminal_trial(8, ticket)
    assert q.terminal_record is None and q.terminal_calls == 0


@pytest.mark.parametrize("tick", [0, 7, 9, -1, True, 8.0])
def test_scheduled_tick(tick):
    q, b = prepare(0)
    with pytest.raises((ValueError, TypeError)):
        b.read_terminal_trial(tick, 0)
    assert q.terminal_record is None


def test_cannot_rebind_for_double_detection():
    q, b = prepare(1)
    b.read_terminal_trial(8, 0)
    with pytest.raises(ValueError, match="already bound"):
        b.bind_terminal_trial(TerminalSetup(0, 1, 9))
    assert q.terminal_record.detector == 0


def test_budget_failure_is_not_no_click():
    q, b = prepare(0, QuantumConfig(max_eval_nodes=3))
    with pytest.raises(OverflowError, match="evaluation budget"):
        b.read_terminal_trial(8, 0)
    assert q.terminal_record is None and q.terminal_calls == 0


@pytest.mark.parametrize(
    "weights,ticket,exception",
    [
        ((0, 0), 0, ValueError),
        ((-1, 2), 0, ValueError),
        ((MAX_CORE_INT, 1), 0, OverflowError),
        ((1, 1), 2, ValueError),
    ],
)
def test_probability_bounds(weights, ticket, exception):
    with pytest.raises(exception):
        choose_output(*weights, ticket)


def test_integer_audit():
    root = Path(__file__).parents[1]
    for relative in (
        "src/event_universe/quantum/terminal.py",
        "src/event_universe/quantum/deferred.py",
        "src/event_universe/integration/quantum_bridge.py",
    ):
        assert static_integer_audit(root / relative) == []


def test_combined_readout_budget_is_enforced_before_second_evaluation():
    q, bridge = prepare(0, QuantumConfig(max_eval_nodes=20))
    with pytest.raises(OverflowError, match="evaluation budget"):
        bridge.read_terminal_trial(8, 0)
    assert q.terminal_record is None
    assert q.terminal_calls == 0
