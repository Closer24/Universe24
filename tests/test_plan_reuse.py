"""Exact input equivalence, bounded reuse and independent physical owners."""

from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import LocalPlan, pack
from event_universe.core.node_execution import NodeExecution
from event_universe.core.plan_reuse import PlanReuse
from event_universe.core.spatial_state import Claim, Ray, SpatialPlan, zero_spatial_state
from event_universe.initialization import parse_initial_state

from .support.disturbances import document, kind
from .test_local_focus import assert_same_world


def test_bounded_reuse_handles_eviction_and_does_not_remember_failure():
    calls = []

    def calculate(keys):
        calls.extend(keys)
        if -1 in keys:
            raise ValueError("invalid local input")
        return tuple(key * key for key in keys)

    cache = PlanReuse(2)
    assert cache.resolve((2, 2, 3), calculate) == (4, 4, 9)
    assert calls == [2, 3]
    assert cache.resolve((2,), calculate) == (4,)
    assert cache.resolve((4,), calculate) == (16,)
    assert cache.resolve((3,), calculate) == (9,)
    assert calls == [2, 3, 4, 3]
    assert cache.report()["entries"] == 2
    for _ in range(2):
        with pytest.raises(ValueError, match="invalid local input"):
            cache.resolve((-1,), calculate)
    assert calls[-2:] == [-1, -1]
    assert cache.report()["entries"] == 2


def test_equal_hashes_do_not_make_different_inputs_equivalent():
    class CollidingInt(int):
        def __hash__(self):
            return 0

    cache = PlanReuse(2)
    assert cache.resolve((CollidingInt(2), CollidingInt(3)), lambda keys: tuple(keys)) == (2, 3)
    assert cache.report()["evaluations"] == 2


def test_serial_reuse_shares_the_bound_and_failure_policy_with_batches():
    cache = PlanReuse(1)
    calls = []

    def calculate(value):
        calls.append(value)
        if value < 0:
            raise ValueError("invalid input")
        return value * value

    assert cache.one(2, lambda: calculate(2)) == 4
    assert cache.one(2, lambda: calculate(2)) == 4
    assert cache.resolve((3,), lambda keys: tuple(calculate(k) for k in keys)) == (9,)
    assert cache.one(3, lambda: calculate(3)) == 9
    assert cache.one(2, lambda: calculate(2)) == 4
    assert calls == [2, 3, 2]
    for _ in range(2):
        with pytest.raises(ValueError, match="invalid input"):
            cache.one(-1, lambda: calculate(-1))
    assert calls[-2:] == [-1, -1]
    assert cache.report()["entries"] == 1


def test_all_carrier_arguments_separate_reuse_entries():
    record = parse_initial_state(document([kind("held")], [((0, 0, 0), "held")])).seeds[0].record
    calls = []

    def planner(records, residuals, received, *, port_loads):
        calls.append((records, residuals, received, port_loads))
        return LocalPlan((), (), (), (), len(calls))

    execution = NodeExecution(1, planner, None, reuse_carriers=True)
    base = ((record,), (), 0)
    assert execution.disturbance(*base).cost == 1
    assert execution.disturbance(*base).cost == 1
    assert execution.disturbance((replace(record, values=(pack((2,)),)),), (), 0).cost == 2
    assert execution.disturbance((record,), (1,), 0).cost == 3
    assert execution.disturbance((record,), (), 1).cost == 4
    assert execution.disturbance(*base, port_loads=(0, 1, 0, 0, 0, 0)).cost == 5
    assert len(calls) == 5


def test_all_spatial_arguments_including_time_phase_and_claims_separate_reuse_entries():
    calls = []

    def planner(*args):
        calls.append(args)
        return SpatialPlan((), (), (), (), len(calls))

    def carrier(*args, **kwargs):
        raise AssertionError("spatial reuse cannot invoke a carrier law")

    record = parse_initial_state(document([kind("held")], [((0, 0, 0), "held")])).seeds[0].record
    state = zero_spatial_state(1)
    base = ((state,), (None,), 0, 0, (), (), 0, 0)
    changes = (
        (replace(state, received_mask=1),),
        (record,),
        1,
        3,
        ((Ray(0, (0, 0, 0), 1, phase=2),),),
        ((Claim(1, 0, 0),),),
        7,
        2,
    )
    execution = NodeExecution(1, carrier, planner, reuse_fields=True)
    assert execution.spatial(*base).cost == 1
    assert execution.spatial(*base).cost == 1
    for index, value in enumerate(changes):
        args = list(base)
        args[index] = value
        assert execution.spatial(*args).cost == index + 2
    assert len(calls) == 9


@pytest.mark.parametrize("workers", [1, 2])
def test_repeated_moving_patterns_share_plans_but_keep_owners_events_and_clocks(workers):
    raw = document(
        [kind("parcel", mode="move", weights=[1, 0, 0, 0, 0, 0])],
        [((2, row, 2), "parcel") for row in range(12)],
        capacity=1,
        budget=4,
        travel=2,
    )
    initial = parse_initial_state(raw)
    plain_events, reused_events = [], []
    with (
        Simulation(replace(initial, focus=False), observer=plain_events.append) as plain,
        Simulation(initial, observer=reused_events.append, node_workers=workers) as reused,
    ):
        for _ in range(24):
            plain.step()
            reused.step()
            assert_same_world(plain, reused)
            assert plain_events == reused_events
        report = reused.execution_report()["carrier_plan_reuse"]
        assert report["requests"] >= 24
        assert report["evaluations"] <= 3
        assert report["hits"] >= report["requests"] - 3
        assert reused.totals() == {"inventory": (12,)}
        assert len({event["position"] for event in reused_events}) >= 12


def test_different_configurations_do_not_share_a_cache():
    raw = document([kind("parcel", mode="move", weights=[1, 0, 0, 0, 0, 0])], [((2, 2, 2), "parcel")])
    left = parse_initial_state(raw)
    raw["disturbance_types"][0]["transport"]["weights"] = [0, 1, 0, 0, 0, 0]
    right = parse_initial_state(raw)
    with Simulation(left) as a, Simulation(right) as b:
        a.step()
        b.step()
        assert a.snapshot() != b.snapshot()
        assert a.execution_report()["carrier_plan_reuse"]["evaluations"] == 1
        assert b.execution_report()["carrier_plan_reuse"]["evaluations"] == 1
