"""Due-only Port scheduling preserves the ordinary Node execution reference.

This tests the interim six-Port adapter, not execution of 24 internal Registers.
"""

import runpy
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.deadline_queue import DeadlineQueue
from event_universe.initialization import parse_initial_state

from .test_register_node import joint_document

ROOT = Path(__file__).parents[1]
configuration = runpy.run_path(str(ROOT / "examples/exact_two_path/run.py"))["configuration"]


def test_deadline_replacement_and_cancellation_keep_no_stale_history():
    queue = DeadlineQueue()
    key = ((1, 1, 1), 0, "compute", 0)
    for tick in range(500):
        queue.set(key, tick)
        assert len(queue) == 1
    assert queue.take(498) == ()
    assert queue.take(499) == (key,)
    assert len(queue) == 0
    queue.set(key, 500)
    queue.cancel(key)
    assert queue.take(500) == ()
    assert queue.report()["peak_entries"] == 1


def test_deadlines_preserve_equal_tick_work_and_reject_skipped_work():
    queue = DeadlineQueue()
    first = ((1, 1, 1), 0, "arrival", 0)
    second = ((1, 1, 1), 1, "arrival", 1)
    third = ((1, 1, 1), 2, "arrival", 2)
    queue.set(first, 5)
    queue.set(second, 2)
    queue.set(third, 2)
    queue.set(first, 1)
    assert queue.take(1) == (first,)
    assert queue.take(2) == (second, third)
    queue.set(first, 3)
    with pytest.raises(ValueError, match="skipped"):
        queue.take(4)
    assert len(queue) == 1


@pytest.mark.parametrize("phase", ("zero", "quarter", "half"))
def test_port_strategy_matches_complete_wave_reference_each_tick(phase):
    initial = parse_initial_state(configuration(phase))
    reference_events, candidate_events = [], []
    with (
        Simulation(initial, observer=reference_events.append) as reference,
        Simulation(initial, observer=candidate_events.append, execution_strategy="port") as candidate,
    ):
        for tick in range(13):
            assert reference.snapshot() == candidate.snapshot()
            assert reference.nodes == candidate.nodes
            assert reference.links == candidate.links
            assert reference.inventory_view() == candidate.inventory_view()
            assert reference.computation_report() == candidate.computation_report()
            assert reference_events == candidate_events
            if tick < 12:
                reference.step()
                candidate.step()
        assert (
            candidate.execution_report()["carrier_phase_visits"]
            < reference.execution_report()["carrier_phase_visits"]
        )


def test_nonexact_failure_has_equal_owner_state_and_events():
    initial = parse_initial_state(configuration(amplitude=1))
    reference_events, candidate_events = [], []
    with (
        Simulation(initial, observer=reference_events.append) as reference,
        Simulation(initial, observer=candidate_events.append, execution_strategy="port") as candidate,
    ):
        for world in (reference, candidate):
            with pytest.raises(ValueError, match="exact_div"):
                world.step()
            assert world.faulted
        assert reference.snapshot() == candidate.snapshot()
        assert reference.nodes == candidate.nodes
        assert reference.links == candidate.links
        assert reference_events == candidate_events == []


def test_explicit_rule_delay_matches_without_waiting_tick_dispatch():
    raw = joint_document()
    raw["seeds"] = [dict(seed, position=[1, 1, 1]) for seed in raw["seeds"]]
    raw["interactions"][0]["k"] = 7
    initial = parse_initial_state(raw)
    reference_events, candidate_events = [], []
    with (
        Simulation(initial, observer=reference_events.append) as reference,
        Simulation(initial, observer=candidate_events.append, execution_strategy="port") as candidate,
    ):
        for tick in range(11):
            assert reference.snapshot() == candidate.snapshot()
            assert reference.nodes == candidate.nodes
            assert reference.inventory_view() == candidate.inventory_view()
            assert reference_events == candidate_events
            if tick < 10:
                reference.step()
                candidate.step()
        assert (
            candidate.execution_report()["carrier_phase_visits"]
            < reference.execution_report()["carrier_phase_visits"]
        )
