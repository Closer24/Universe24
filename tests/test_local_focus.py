"""Exact ordinary/Focus agreement and independently measured host visit reduction."""

from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.initialization import load_initial_state, parse_initial_state

from .support.disturbances import document, kind

ROOT = Path(__file__).resolve().parents[1]


def moving_document(port=0, *, travel=1, budget=10000):
    weights = [int(index == port) for index in range(6)]
    raw = document(
        [kind("moving", mode="move", weights=weights)],
        [((2, 2, 2), "moving")],
        travel=travel,
        budget=budget,
        capacity=1,
    )
    raw["shape"] = [9, 9, 9]
    return raw


def assert_same_world(left, right):
    assert left.tick == right.tick and left.faulted == right.faulted
    assert left.snapshot() == right.snapshot()
    assert left.inventory_view() == right.inventory_view()
    assert left.computation_report() == right.computation_report()
    assert left.totals() == right.totals()
    assert left.spatial_accounting() == right.spatial_accounting()
    assert left.conservation_report() == right.conservation_report()


def compare(initial, ticks, *, workers=1):
    plain_events, focus_events = [], []
    with Simulation(
        replace(initial, focus=False), observer=plain_events.append, node_workers=workers
    ) as plain:
        with Simulation(
            replace(initial, focus=True), observer=focus_events.append, node_workers=workers
        ) as focus:
            for _ in range(ticks):
                plain.step()
                focus.step()
                assert_same_world(plain, focus)
                assert plain_events == focus_events
            return plain.execution_report(), focus.execution_report()


@pytest.mark.parametrize("port", range(6))
@pytest.mark.parametrize("travel,budget", [(1, 10000), (3, 4)])
def test_all_ports_delays_and_periodic_rearrival_match_at_every_tick(port, travel, budget):
    plain, focus = compare(parse_initial_state(moving_document(port, travel=travel, budget=budget)), 36)
    assert focus["focus_enabled"] and not plain["focus_enabled"]
    assert focus["carrier_phase_visits"] < plain["carrier_phase_visits"]


@pytest.mark.parametrize(
    "example",
    [
        "finite_fields.json",
        "isotropic_rays.json",
        "spatial_turning.json",
        "local_lorentz_field.json",
        "open_world.json",
        "node-vector/joint-reaction.json",
        "node-vector/six-records.json",
        "node-vector/two-fields.json",
    ],
)
def test_field_arrivals_reactions_decay_and_ray_transport_match(example):
    compare(load_initial_state(ROOT / "examples" / example), 8)


def test_parallel_focus_keeps_the_same_event_order_and_cost():
    compare(parse_initial_state(moving_document()), 12, workers=2)


def test_shared_clock_uses_the_verified_baseline_scheduler():
    initial = load_initial_state(ROOT / "examples" / "finite_fields.json")
    plain, focus = compare(replace(initial, spatial_computation_delay=True), 4)
    assert focus["focus_requested"] and not focus["focus_enabled"]
    assert focus["focus_fallback"] == "shared field clock"
    assert focus["carrier_phase_visits"] == plain["carrier_phase_visits"]


def test_capacity_failure_happens_on_the_same_tick_with_the_same_partial_state():
    raw = moving_document()
    raw["disturbance_types"].append(kind("held"))
    raw["seeds"].append({"position": [3, 2, 2], "type": "held"})
    initial = parse_initial_state(raw)
    events = [[], []]
    worlds = [
        Simulation(replace(initial, focus=enabled), observer=events[index].append)
        for index, enabled in enumerate((False, True))
    ]
    failures = []
    for world in worlds:
        with pytest.raises(ValueError) as failure:
            world.step()
        failures.append(str(failure.value))
    assert failures[0] == failures[1]
    assert_same_world(*worlds)
    assert events[0] == events[1]


def test_empty_carrier_history_is_not_enumerated_by_focused_steps():
    raw = moving_document()
    raw.update(focus=True, boundary="open")
    world = Simulation(parse_initial_state(raw))
    for _ in range(10):
        world.step()
    assert not world._awake_carriers and len(world._nodes) == 7

    class NoScan(dict):
        def __iter__(self):
            pytest.fail("Focus scanned empty carrier history")

        def items(self):
            pytest.fail("Focus scanned empty carrier history")

        def values(self):
            pytest.fail("Focus scanned empty carrier history")

    world._nodes = NoScan(world._nodes)
    visits = world.execution_report()["carrier_phase_visits"]
    for _ in range(3):
        world.step()
    assert world.execution_report()["carrier_phase_visits"] == visits


@pytest.mark.parametrize("value", [0, 1, "true", None, []])
def test_focus_requires_an_explicit_boolean(value):
    raw = moving_document()
    raw["focus"] = value
    with pytest.raises(ValueError, match="focus must be a boolean"):
        parse_initial_state(raw)


def test_focus_defaults_to_true_and_allows_explicit_opt_out():
    initial = parse_initial_state(moving_document())
    assert initial.focus is True
    assert replace(initial, focus=False).focus is False
    assert parse_initial_state({**moving_document(), "focus": False}).focus is False
    with pytest.raises(ValueError, match="focus must be boolean"):
        replace(initial, focus=1)
