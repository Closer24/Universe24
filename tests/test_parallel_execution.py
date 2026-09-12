"""Independent single-world parity across owner commits, delays, and failures."""

import json
import os
import subprocess
import sys
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import MAX_VALUE, Packet, unpack
from event_universe.fields.disturbances import DisturbanceLaw
from event_universe.initialization import parse_initial_state
from tools.benchmark_engine import physical_state

from .test_disturbance_engine import document, exchange_document, field, kind, meeting_document
from .test_finite_spatial_engine import all_records, finite_document
from .test_spatial_coupling import document as coupling_document
from .test_spatial_interactions import exchange as spatial_exchange

ROOT = Path(__file__).resolve().parents[1]


def moving_document(*, budget=10000, travel=1):
    raw = document(
        [kind("traveler", mode="move", weights=[1, 0, 0, 0, 0, 0])],
        [((0, 0, 0), "traveler"), ((4, 0, 0), "traveler"), ((8, 0, 0), "traveler")],
        capacity=2,
        budget=budget,
        travel=travel,
    )
    raw["shape"] = [13, 3, 3]
    return raw


def worlds(raw, *, workers=2, observer_factories=None):
    initial = parse_initial_state(raw)
    events = [[], []]
    observers = (
        [items.append for items in events]
        if observer_factories is None
        else [factory(items) for factory, items in zip(observer_factories, events, strict=True)]
    )
    serial = Simulation(initial, observer=observers[0])
    parallel = Simulation(
        initial,
        observer=observers[1],
        workers=workers,
        parallel_threshold=1,
        chunk_size=1,
    )
    return serial, parallel, events


def step_pair(serial, parallel, events):
    errors = []
    for world in (serial, parallel):
        try:
            world.step()
        except Exception as error:
            errors.append((type(error), str(error)))
        else:
            errors.append(None)
    assert errors[0] == errors[1]
    assert physical_state(serial) == physical_state(parallel)
    assert events[0] == events[1]
    return errors[0]


def assert_workers_used(world):
    report = world.execution_report()
    assert report["submitted_chunks"] > 0
    assert report["evaluated_proposals"] > 0


@pytest.mark.parametrize("workers,budget,travel", [(2, 10000, 1), (3, 3, 2)])
def test_parallel_moves_preserve_every_tick_pending_links_events_and_cost(workers, budget, travel):
    serial, parallel, events = worlds(moving_document(budget=budget, travel=travel), workers=workers)
    with serial, parallel:
        waited = False
        for _ in range(18):
            assert step_pair(serial, parallel, events) is None
            waited |= any(cell.pending is not None for cell in parallel.cells.values())
        assert_workers_used(parallel)
        assert any(event["event"] == "received" for event in events[1])
        if budget == 3:
            assert waited


def test_parallel_arrival_capacity_failure_retains_every_link_owner():
    serial, parallel, events = worlds(meeting_document(capacity=1))
    with serial, parallel:
        error = step_pair(serial, parallel, events)
        assert error is not None and error[0] is ValueError
        assert parallel.faulted
        assert sum(packet is not None for slots in parallel.links.values() for packet in slots) == 2
        assert_workers_used(parallel)
        assert step_pair(serial, parallel, events)[0] is RuntimeError


def test_parallel_local_pairs_keep_exact_transfer_and_operation_costs():
    raw = exchange_document(7, denominator=3)
    raw["seeds"].extend([{**deepcopy(seed), "position": [4, 2, 2]} for seed in raw["seeds"][:2]])
    serial, parallel, events = worlds(raw)
    with serial, parallel:
        for _ in range(4):
            assert step_pair(serial, parallel, events) is None
        assert parallel.totals() == {"inventory": (0,)}
        assert parallel.source_totals() == {"inventory": (0,)}
        assert_workers_used(parallel)


def test_worker_rational_regions_keep_exact_projection_and_high_model_tariff():
    raw = failing_document()
    raw["normal_budget"] = 1000000
    raw["disturbance_types"][0]["updates"][0]["expression"] = {
        "op": "rational_whole",
        "args": [{"op": "ratio", "args": [-7, 3]}],
    }
    serial, parallel, events = worlds(raw)
    with serial, parallel:
        assert step_pair(serial, parallel, events) is None
        assert all(
            parallel.record_values(cell.records[0])["quantity"] == (-2,)
            for cell in parallel.cells.values()
        )
        assert parallel.computation_report()["model_operations_cost"] > 3 * 65536
        assert_workers_used(parallel)


def failing_document():
    raw = document(
        [
            kind(
                "counter",
                values={"quantity": 1},
                updates=[
                    {
                        "field": "quantity",
                        "expression": {"op": "add", "args": [{"field": "quantity"}, 1]},
                    }
                ],
            )
        ],
        [((0, 0, 0), "counter"), ((1, 0, 0), "counter"), ((2, 0, 0), "counter")],
        fields=[field("quantity", conserved=False)],
        capacity=1,
    )
    raw["seeds"][1]["values"] = {"quantity": MAX_VALUE}
    return raw


def test_later_speculative_failure_follows_the_first_sorted_committed_cycle():
    serial, parallel, events = worlds(failing_document())
    with serial, parallel:
        error = step_pair(serial, parallel, events)
        assert error is not None and error[0] is ValueError and "bound" in error[1]
        assert [event["position"] for event in events[1]] == [(0, 0, 0), (0, 0, 0)]
        assert parallel.cells[(1, 0, 0)].pending is None
        assert parallel.cells[(2, 0, 0)].last_cost == 0
        assert parallel.computation_report()["local_cycles_started"] == 1
        assert_workers_used(parallel)


def test_earlier_commit_failure_wins_over_a_later_worker_arithmetic_failure():
    serial, parallel, events = worlds(failing_document())
    with serial, parallel:
        for world in (serial, parallel):
            record = world.cells[(0, 0, 0)].records[0]
            world._links[(0, 0, 0)] = (Packet(9, (0, 0, 0), 0, record),) + (None,) * 5
        error = step_pair(serial, parallel, events)
        assert error is not None and error[0] is ValueError and "occupied" in error[1]
        assert parallel.cells[(0, 0, 0)].pending is not None
        assert parallel.cells[(1, 0, 0)].pending is None
        assert parallel.computation_report()["local_cycles_started"] == 1
        assert_workers_used(parallel)


@pytest.mark.parametrize("event_name", ["cycle_started", "cycle_committed", "sent"])
def test_observer_failure_keeps_the_exact_serial_owner_prefix(event_name):
    def factory(events):
        def observer(event):
            events.append(event)
            if event["event"] == event_name:
                raise RuntimeError("observer rejected this event")

        return observer

    serial, parallel, events = worlds(moving_document(), observer_factories=(factory, factory))
    with serial, parallel:
        error = step_pair(serial, parallel, events)
        assert error == (RuntimeError, "observer rejected this event")
        assert parallel.cells[(4, 0, 0)].last_cost == 0
        assert parallel.cells[(8, 0, 0)].last_cost == 0
        assert parallel.tick == 0
        assert_workers_used(parallel)


def test_parallel_carrier_plans_preserve_independent_emission_during_frozen_waits():
    raw = finite_document(source=True, moving=True, budget=8, travel=2)
    raw["seeds"].append({**deepcopy(raw["seeds"][0]), "position": [10, 10, 10]})
    raw["disturbance_types"][0]["defaults"]["strength"] = 2
    serial, parallel, events = worlds(raw)
    with serial, parallel:
        assert step_pair(serial, parallel, events) is None
        pending = [cell.pending for cell in parallel.cells.values() if cell.pending is not None]
        assert len(pending) == 2
        until = max(item.ready_tick for item in pending) + 6
        for _ in range(until):
            assert step_pair(serial, parallel, events) is None
        assert parallel.source_totals()["radiation"] == (10,)
        assert all(unpack(record.emission_remaining[0]) == (0,) for record in all_records(parallel))
        assert_workers_used(parallel)
        assert any(event["event"] == "spatial_decayed" for event in events[1])


def test_spatial_coupling_keeps_its_owner_path_while_other_cells_use_workers():
    raw = coupling_document()
    uncoupled = deepcopy(raw["disturbance_types"][0])
    uncoupled["name"] = "uncoupled"
    raw["disturbance_types"].append(uncoupled)
    raw["seeds"].extend(
        [
            {"position": [20, 15, 15], "type": "uncoupled"},
            {"position": [25, 15, 15], "type": "uncoupled"},
        ]
    )
    serial, parallel, events = worlds(raw)
    with serial, parallel:
        for _ in range(6):
            assert step_pair(serial, parallel, events) is None
        assert_workers_used(parallel)
        assert parallel.execution_report()["fallback_reasons"].get("spatial_coupling", 0) > 0
        assert any(event["event"] == "spatial_coupled" for event in events[1])


def test_delayed_spatial_guard_failure_matches_with_other_cells_planning_in_parallel():
    raw = spatial_exchange(delayed=True, incoming=True)
    independent = deepcopy(raw["disturbance_types"][0])
    independent["name"] = "independent"
    raw["disturbance_types"].append(independent)
    raw["seeds"].append({"position": [4, 4, 4], "type": "independent"})
    serial, parallel, events = worlds(raw)
    with serial, parallel:
        for _ in range(20):
            error = step_pair(serial, parallel, events)
            if error is not None:
                break
        assert error is not None and error[0] is ValueError and "invariant" in error[1]
        assert parallel.cells[(2, 2, 2)].pending is not None
        assert parallel.spatial_accounting()["quantity"]["reactions"] == (0,)
        assert_workers_used(parallel)


def test_native_resolver_retains_serial_event_id_and_cost_order():
    raw = json.loads((ROOT / "examples/quantum/native_quantum.json").read_text())
    serial, parallel, events = worlds(raw)
    with serial, parallel:
        for _ in range(12):
            assert step_pair(serial, parallel, events) is None
        report = parallel.execution_report()
        assert report["submitted_chunks"] == 0
        assert report["fallback_reasons"].get("resolver", 0) > 0
        assert parallel.event_space.next_id > len(raw["seeds"])


def test_replaced_custom_planner_is_called_once_per_original_owner_visit():
    serial, parallel, events = worlds(moving_document())
    calls = [[], []]
    with serial, parallel:
        for index, world in enumerate((serial, parallel)):
            original = world._planner

            def tracked(records, residuals, received, *, original=original, index=index):
                calls[index].append((records, residuals, received))
                return original(records, residuals, received)

            world._planner = tracked
        for _ in range(3):
            assert step_pair(serial, parallel, events) is None
        assert calls[0] == calls[1] and len(calls[0]) == 9
        assert parallel.execution_report()["submitted_chunks"] == 0
        assert parallel.execution_report()["fallback_reasons"].get("custom_planner", 0) > 0


def test_replaced_record_policy_cannot_leave_prepared_activity_decisions_in_effect():
    serial, parallel, events = worlds(moving_document())
    with serial, parallel:
        for world in (serial, parallel):
            world._record_policy = replace(world._record_policy)
        for _ in range(3):
            assert step_pair(serial, parallel, events) is None
        report = parallel.execution_report()
        assert report["submitted_chunks"] == 0
        assert report["fallback_reasons"].get("custom_record_policy", 0) > 0


def test_callback_planner_replacement_discards_later_prepared_results():
    initial = parse_initial_state(moving_document())
    events, calls = [[], []], [[], []]
    created = []

    def observer(index):
        def receive(event):
            events[index].append(event)
            if event["event"] == "cycle_started" and event["position"] == (0, 0, 0):
                world = created[index]
                original = world._planner

                def replacement(records, residuals, received):
                    calls[index].append(records)
                    plan = original(records, residuals, received)
                    return replace(plan, cost=plan.cost + 2)

                world._planner = replacement

        return receive

    created.append(Simulation(initial, observer=observer(0)))
    created.append(
        Simulation(initial, observer=observer(1), workers=2, parallel_threshold=1, chunk_size=1)
    )
    with created[0] as serial, created[1] as parallel:
        assert step_pair(serial, parallel, events) is None
        assert calls[0] == calls[1] and len(calls[0]) == 2
        assert_workers_used(parallel)


def test_class_planner_replacement_before_composition_remains_owner_local(monkeypatch):
    original = DisturbanceLaw.__call__
    calls = []

    def replacement(self, records, residuals, received):
        calls.append(records)
        plan = original(self, records, residuals, received)
        return replace(plan, cost=plan.cost + 2)

    monkeypatch.setattr(DisturbanceLaw, "__call__", replacement)
    serial, parallel, events = worlds(moving_document())
    with serial, parallel:
        assert step_pair(serial, parallel, events) is None
        assert len(calls) == 6
        assert serial.computation_report()["model_operations_cost"] == 18
        assert parallel.execution_report()["submitted_chunks"] == 0
        assert parallel.execution_report()["fallback_reasons"].get("custom_planner", 0) == 3


def test_workers_use_the_owners_package_when_parent_sys_path_selects_a_checkout(tmp_path):
    alternate = tmp_path / "alternate"
    package = alternate / "event_universe"
    package.mkdir(parents=True)
    (package / "__init__.py").write_text("raise RuntimeError('wrong package imported')\n")
    source = tmp_path / "input.json"
    source.write_text(json.dumps(moving_document()))
    program = "\n".join(
        [
            "import json, sys",
            "from pathlib import Path",
            "sys.path.insert(0, sys.argv[1])",
            "from event_universe import Simulation",
            "from event_universe.initialization import parse_initial_json",
            "initial = parse_initial_json(Path(sys.argv[2]).read_bytes())",
            "with Simulation(initial, workers=2, parallel_threshold=1, chunk_size=1) as world:",
            "    world.step()",
            "    assert world.tick == 1",
            "    assert world.execution_report()['evaluated_proposals'] == 3",
            "print('selected package preserved')",
        ]
    )
    environment = {**os.environ, "PYTHONPATH": str(alternate)}
    result = subprocess.run(
        [sys.executable, "-c", program, str(ROOT / "src"), str(source)],
        cwd=tmp_path,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.strip() == "selected package preserved"
