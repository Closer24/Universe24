"""Bounded host work, persistent workers, strict options, and executor ownership."""

import os
from concurrent.futures import InterpreterPoolExecutor
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.local_execution import ProposalInput, validate_execution_options
from event_universe.initialization import parse_initial_state
from event_universe.local_execution import worker_initializer
from tools.benchmark_engine import physical_state

from .test_disturbance_engine import document, kind


def held_initial(count=8):
    return parse_initial_state(
        document([kind("resident")], [((x, 0, 0), "resident") for x in range(count)], capacity=1)
    )


@pytest.mark.parametrize("name", ["workers", "parallel_threshold", "chunk_size"])
@pytest.mark.parametrize("value", [0, -1, True, 1.5])
def test_execution_options_reject_nonpositive_or_noninteger_values(name, value):
    options = {"workers": 1, "parallel_threshold": 1, "chunk_size": 1, name: value}
    with pytest.raises(ValueError, match=f"{name} must be a positive integer"):
        validate_execution_options(**options)


def test_invalid_options_fail_before_external_executor_acquisition():
    calls = []
    with pytest.raises(ValueError, match="workers must"):
        Simulation(held_initial(), workers=0, executor_factory=calls.append)
    assert calls == []


def test_small_world_stays_serial_without_starting_a_pool(monkeypatch):
    def unexpected_pool(**options):
        pytest.fail("a world below the threshold must not start worker resources")

    monkeypatch.setattr("concurrent.futures.InterpreterPoolExecutor", unexpected_pool)
    with Simulation(held_initial(2), workers=2, parallel_threshold=3) as world:
        world.step()
        assert world.totals() == {"inventory": (2,)}
        report = world.execution_report()
        assert report["backend"] == "serial"
        assert report["fallback_reasons"] == {"threshold": 2}
        assert report["submitted_chunks"] == 0


def test_default_serial_path_avoids_reflective_worker_guards(monkeypatch):
    with Simulation(held_initial(2)) as world:

        def unexpected_guard(planner):
            pytest.fail("serial execution has no worker method identity to check")

        monkeypatch.setattr(world._local_execution, "planner_unchanged", unexpected_guard)
        monkeypatch.setattr(world._local_execution, "policy_unchanged", unexpected_guard)
        world.step()
        assert world.execution_report()["serial_proposals"] == 2


def test_persistent_workers_keep_host_identity_and_bounded_pending_chunks():
    world = Simulation(held_initial(), workers=2, parallel_threshold=1, chunk_size=1)
    with world:
        world.step()
        pool = world._local_execution._pool
        assert pool is not None
        world.step()
        assert world._local_execution._pool is pool
        assert world.totals() == {"inventory": (8,)}
        report = world.execution_report()
        assert report["evaluated_proposals"] == 16
        assert report["submitted_chunks"] == 16
        assert 1 <= len(report["workers_used"]) <= 2
        assert all(item["process"] == os.getpid() for item in report["workers_used"])
        assert all(item["interpreter"] != 0 for item in report["workers_used"])
        assert report["peak_pending_chunks"] <= 4
    world.close()
    assert world.execution_report()["closed"]
    with pytest.raises(RuntimeError, match="closed"):
        world.step()


def test_owner_failure_discards_only_a_bounded_amount_of_speculative_work():
    def observer(event):
        if event["event"] == "cycle_started":
            raise ValueError("observer stopped this run")

    world = Simulation(
        held_initial(40), observer=observer, workers=2, parallel_threshold=1, chunk_size=1
    )
    with pytest.raises(ValueError, match="observer stopped"):
        with world:
            world.step()
    report = world.execution_report()
    assert report["closed"]
    assert report["peak_pending_chunks"] <= 4
    assert report["submitted_chunks"] <= 5
    assert report["evaluated_proposals"] <= 5
    assert world.tick == 0


def test_worker_window_consumes_only_bounded_inputs_from_a_large_iterator():
    with Simulation(held_initial(1), workers=2, parallel_threshold=1, chunk_size=3) as world:
        cell = next(iter(world.cells.values()))
        consumed = []

        def inputs():
            for index in range(10000):
                consumed.append(index)
                yield ProposalInput(cell.records, cell.coupling_remainders, 0)

        results = world._local_execution.evaluate(inputs())
        first = next(results).result()
        assert first.replacements[0][1] == cell.records[0]
        # Two pending chunks per worker, plus the chunk currently being yielded.
        assert len(consumed) <= (2 * 2 + 1) * 3
        before_close = len(consumed)
        results.close()
        assert len(consumed) == before_close
        report = world.execution_report()
        assert report["submitted_chunks"] <= 5
        assert report["evaluated_proposals"] <= 15


def test_factory_receives_canonical_planner_and_retains_executor_ownership():
    pools, planners = [], []

    def factory(planner):
        planners.append(planner)
        initializer, initargs = worker_initializer(planner)
        pool = InterpreterPoolExecutor(max_workers=1, initializer=initializer, initargs=initargs)
        pools.append(pool)
        return pool

    try:
        with Simulation(
            held_initial(2),
            workers=1,
            parallel_threshold=1,
            chunk_size=1,
            executor_factory=factory,
            execution_backend="borrowed_interpreters",
        ) as world:
            assert planners == [world._planner]
            world.step()
            report = world.execution_report()
            assert report["backend"] == "borrowed_interpreters"
            assert report["evaluated_proposals"] == 2
            assert not report["owns_executor"]
        assert pools[0].submit(sum, (2, 3)).result(timeout=10) == 5
    finally:
        for pool in pools:
            pool.shutdown(wait=True, cancel_futures=True)


def test_replaced_planner_definition_invalidates_an_existing_worker_snapshot():
    initial = held_initial(2)
    with (
        Simulation(initial) as serial,
        Simulation(initial, workers=2, parallel_threshold=1, chunk_size=1) as parallel,
    ):
        for world in (serial, parallel):
            world.step()
            costs = world._planner.operation_costs
            object.__setattr__(
                world._planner,
                "operation_costs",
                replace(costs, prices=tuple(p * 2 for p in costs.prices)),
            )
            world.step()
        assert physical_state(serial) == physical_state(parallel)
        report = parallel.execution_report()
        assert report["evaluated_proposals"] == 2
        assert report["fallback_reasons"] == {"custom_planner": 2}


def test_instance_policy_callback_override_remains_on_the_owner():
    with Simulation(held_initial(2), workers=2, parallel_threshold=1, chunk_size=1) as world:
        original = world._record_policy.has_work
        calls = []

        def has_work(records):
            calls.append(records)
            return original(records)

        object.__setattr__(world._record_policy, "has_work", has_work)
        world.step()
        assert len(calls) == 2
        report = world.execution_report()
        assert report["submitted_chunks"] == 0
        assert report["fallback_reasons"] == {"custom_record_policy": 2}
