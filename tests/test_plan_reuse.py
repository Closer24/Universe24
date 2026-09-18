"""Exact input equivalence, bounded reuse and independent physical owners."""

from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core import disturbance_engine, spatial_node
from event_universe.core.disturbance_state import LocalPlan, pack
from event_universe.core.node_execution import NodeExecution
from event_universe.core.plan_reuse import PlanReuse
from event_universe.core.spatial_state import Ray, SpatialPlan, zero_spatial_state
from event_universe.initialization import parse_initial_state

from .support.disturbances import document, kind
from .test_external_body import SINK_BODY
from .test_external_body import document as body_document
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


def test_all_spatial_arguments_including_phase_separate_reuse_entries():
    """Every argument of the spatial law is in the key; the world tick is not an
    argument, so it is not in the key (see the steady-field test below)."""
    calls = []

    def planner(*args):
        calls.append(args)
        return SpatialPlan((), (), (), (), len(calls))

    def carrier(*args, **kwargs):
        raise AssertionError("spatial reuse cannot invoke a carrier law")

    record = parse_initial_state(document([kind("held")], [((0, 0, 0), "held")])).seeds[0].record
    state = zero_spatial_state(1)
    base = ((state,), (None,), 0, 0, (), 0)
    changes = (
        (replace(state, received_mask=1),),
        (record,),
        1,
        3,
        ((Ray(0, (0, 0, 0), 1, phase=2),),),
        2,
    )
    execution = NodeExecution(1, carrier, planner, reuse_fields=True)
    assert execution.spatial(*base).cost == 1
    assert execution.spatial(*base).cost == 1
    for index, value in enumerate(changes):
        args = list(base)
        args[index] = value
        assert execution.spatial(*args).cost == index + 2
    assert len(calls) == 7


def lamp_line(stock, ticks):
    """One `hold` lamp at x = 1 of a 7 x 3 x 3 open board, paying one quantum of
    `light` per interval from its own stock into a ray field with the single
    heading +X, phase constant (`phase_advance` 0); the ray walks x = 2 to 6 and
    escapes."""
    return {
        "schema_version": 1,
        "model_id": "plan-key-test-v1",
        "shape": [7, 3, 3],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": {
            name: 1
            for name in (
                "receive",
                "read",
                "evaluate",
                "update",
                "couple",
                "route",
                "split",
                "send",
                "commit",
            )
        },
        "fields": [
            {
                "name": "light",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            }
        ],
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["light"],
                "defaults": {"light": stock},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {
                "field": "light",
                "baseline": 0,
                "transport": "ray",
                "headings": [[1, 0, 0]],
                "rays_per_tick": 1,
                "ray_slots": 8,
                "metric": "links",
                "pace": [1, 1],
                "kerengonen": {"phase_steps": 8, "phase_advance": 0},
            }
        ],
        "emissions": [
            {
                "type": "lamp",
                "field": "light",
                "amount": 1,
                "denominator": 1,
                "heading": [1, 0, 0],
                "kerengonen_phase": 0,
            }
        ],
        "seeds": [{"position": [1, 1, 1], "type": "lamp"}],
    }


def test_a_node_in_a_steady_field_reuses_its_plan_across_ticks_and_a_counting_lamp_does_not():
    """The key holds the Node's local input, not the clock: the Node at x = k
    receives the same ray (amount 1, phase 0, k - 1 steps) every interval from
    tick k on, so it evaluates once and hits from its second arrival; the lamp
    pays a quantum per interval, its stock counts down in its record and every
    interval presents a new key. Eight ticks: the lamp plans 8 times without a
    hit, the Nodes at x = 2 to 6 plan 7, 6, 5, 4 and 3 times with one evaluation
    each, 33 requests, 13 evaluations, 20 hits, cumulative per tick 0, 0, 1, 3,
    6, 10, 15, 20; the quanta of ticks 1 to 3 have left through the open
    boundary at x = 6."""
    with Simulation(parse_initial_state(lamp_line(12, 8))) as world:
        hits = []
        for _ in range(8):
            world.step()
            hits.append(world.execution_report()["spatial_plan_reuse"]["hits"])
        # node-is-ports-v1 (2026-09-18): the trace a thing leaves at a Node is a
        # zero-amount parked shadow among its rays, part of the plan's key, and
        # a Node holding one stays active with the same input, so every Node on
        # the line evaluates once with the trace and reuses from then on: 13
        # evaluations, 20 hits.
        assert hits == [0, 0, 1, 3, 6, 10, 15, 20]
        report = world.execution_report()["spatial_plan_reuse"]
        assert (report["requests"], report["evaluations"], report["hits"]) == (33, 13, 20)
        assert world.totals() == {"light": (9,)}
        assert world.escaped_totals() == {"light": (3,)}


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


def test_a_reuse_hit_is_served_a_validated_plan_and_a_miss_validates(monkeypatch):
    """The plan is validated when it is made, once per evaluation, and a hit is
    served that plan without a second check; the Node validates only what it
    changes after planning, an external body's part. On the lamp line of the
    test above, eight ticks with Focus on: 13 validations at the execution (one
    per evaluation), none at the Node; with Focus off the law itself serves the
    Nodes and each validates its own plan, 33 at the Node, none at the
    execution; the two worlds agree at every tick. A sink body alone for four
    ticks: the body's Node validates after each of its four cycles, and the
    execution once per evaluation."""
    validated = []

    def validator(request, plan):
        validated.append(request)

    def planner(*args):
        return SpatialPlan((), (), (), (), 1)

    def carrier(*args, **kwargs):
        raise AssertionError("spatial reuse cannot invoke a carrier law")

    state = zero_spatial_state(1)
    execution = NodeExecution(1, carrier, planner, reuse_fields=True, spatial_validator=validator)
    execution.spatial((state,), (None,), 0)
    execution.spatial((state,), (None,), 0)
    execution.spatial((state,), (None,), 1)
    assert [request.received for request in validated] == [0, 1]
    assert execution.report()["spatial_plan_reuse"]["hits"] == 1

    checks = {"execution": 0, "node": 0}
    boundary = disturbance_engine.validate_spatial_plan

    def at_execution(*args):
        checks["execution"] += 1
        boundary(*args)

    def at_node(*args):
        checks["node"] += 1
        boundary(*args)

    monkeypatch.setattr(disturbance_engine, "validate_spatial_plan", at_execution)
    monkeypatch.setattr(spatial_node, "validate_spatial_plan", at_node)
    initial = parse_initial_state(lamp_line(12, 8))
    with (
        Simulation(initial) as reused,
        Simulation(replace(initial, focus=False)) as plain,
    ):
        for _ in range(8):
            at_node_before = checks["node"]
            reused.step()
            assert checks["node"] == at_node_before
            at_execution_before = checks["execution"]
            plain.step()
            assert checks["execution"] == at_execution_before
            assert_same_world(reused, plain)
        report = reused.execution_report()["spatial_plan_reuse"]
        assert (report["requests"], report["evaluations"], report["hits"]) == (33, 13, 20)
        assert checks == {"execution": 13, "node": 33}
    checks.update(execution=0, node=0)
    with Simulation(parse_initial_state(body_document((SINK_BODY,)))) as world:
        for _ in range(4):
            world.step()
        report = world.execution_report()["spatial_plan_reuse"]
        assert checks == {"execution": report["evaluations"], "node": 4}
        assert report["hits"] > 0
