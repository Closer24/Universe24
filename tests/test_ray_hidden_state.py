"""Ray hidden state (ray-event-state-v1): steps, outbound, event Ports and shares, Detector bit.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Ray hidden state")
before the first run: a lamp sweeping six unit-axial headings and a directed
lamp two Links on along its +X line, under the shared Detector admission.
"""

import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import CostMeter
from event_universe.core.spatial_state import (
    RAY_EVENT_STATE,
    Ray,
    merge_rays,
    ray_momentum,
    validate_rays,
)
from event_universe.fields.rays import forward_rays
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

LAMP_A = (5, 7, 7)
LAMP_B = (7, 7, 7)
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
A_SHARES = (3, 3, 3, 2, 2, 2)
B_SHARES = (4, 0, 0, 0, 0, 0)


def document(ticks=4):
    return {
        "schema_version": 1,
        "model_id": "ray-hidden-state-test-v1",
        "shape": [15, 15, 15],
        "boundary": "periodic",
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
                "name": "quanta",
                "components": 1,
                "units": "quantum",
                "signed": False,
                "conserved": True,
                "extensive": True,
            },
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "lamp_a",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 600, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
            {
                "name": "lamp_b",
                "fields": ["quanta", "momentum"],
                "defaults": {"quanta": 600, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            },
        ],
        "spatial_fields": [
            {
                "field": "quanta",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 6,
                "ray_slots": 8,
                "metric": "links",
                "pace": [1, 1],
                "kerengonen": {"phase_steps": 8, "phase_advance": 1},
            }
        ],
        "emissions": [
            {
                "type": "lamp_a",
                "field": "quanta",
                "amount": 15,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
            },
            {
                "type": "lamp_b",
                "field": "quanta",
                "amount": 4,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": [1, 0, 0],
                "kerengonen_phase": 2,
            },
        ],
        "seeds": [
            {"position": list(LAMP_A), "type": "lamp_a"},
            {"position": list(LAMP_B), "type": "lamp_b"},
        ],
        "conservation": {
            "name": "quanta",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["quanta", "momentum"],
                    "energy": {"field": "quanta"},
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {"field": "quanta", "side": "right"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        },
    }


def rays_at(world, position):
    node = next(n for n in world.inventory_view().nodes if n.position == position)
    return node.rays[0] if node.rays else ()


def lamp(world, type_index):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    )


def test_rays_carry_their_event_and_count_their_steps(tmp_path):
    initial = parse_initial_state(document())
    definition, field = initial.spatial_fields[0], initial.fields[0]
    world = Simulation(initial)
    for tick in range(1, 5):
        world.step()
        # (a) A's first emission is one event: six rays, one per Port, t Links out
        # after t ticks, each carrying the mask and shares of that emission and the
        # Links it walked, with the phase it advanced.
        for port, (amount, unit) in enumerate(zip(A_SHARES, HEADINGS, strict=True)):
            position = tuple(a + tick * u for a, u in zip(LAMP_A, unit, strict=True))
            first = [ray for ray in rays_at(world, position) if ray.event_ports == 0b111111]
            assert first == [
                Ray(
                    port,
                    (0, 0, 0),
                    amount,
                    phase=tick,
                    steps=tick,
                    outbound=1,
                    event_ports=0b111111,
                    event_shares=A_SHARES,
                    detector=0,
                )
            ]
        # (d) Totals and the audit stay exact at every tick.
        assert world.totals()["quanta"] == (1200,)
        report = world.conservation_report()
        assert report["status"] == "passed"
        assert report["current"]["energy"] == 1200 and tuple(report["current"]["momentum"]) == (0, 0, 0)
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        assert sum(len(rays_at(world, n.position)) for n in world.inventory_view().nodes) == 7 * tick
    # (b) A's tick-1 ray and B's tick-3 ray share the Node, heading and phase after
    # tick 4 minus one: two events, two rays, where one merged ray of 7 used to be.
    a_ray = Ray(0, (0, 0, 0), 3, phase=3, steps=3, event_ports=0b111111, event_shares=A_SHARES)
    b_ray = Ray(0, (0, 0, 0), 4, phase=3, steps=1, event_ports=0b000001, event_shares=B_SHARES)
    merged = merge_rays((a_ray, b_ray))
    assert len(merged) == 2 and set(merged) == {a_ray, b_ray}
    assert merge_rays((a_ray, a_ray)) == (replace(a_ray, amount=6),)
    assert sorted((ray.amount, ray.steps) for ray in rays_at(world, (9, 7, 7))) == [(3, 4), (4, 2)]
    assert sorted((ray.amount, ray.steps) for ray in rays_at(world, (8, 7, 7))) == [(3, 3), (4, 1)]
    assert world.spatial_values((8, 7, 7))["quanta"]["ray_count"] == 2
    # (d) After tick 4: the lamps paid 60 and 16, recoiled by amount x heading, and
    # the rays hold the rest with the opposite momentum.
    assert lamp(world, 0) == {"quanta": (540,), "momentum": (0, -4, 0)}
    assert lamp(world, 1) == {"quanta": (584,), "momentum": (-16, 0, 0)}
    in_flight = [0, 0, 0]
    stock = 0
    for node in world.inventory_view().nodes:
        for axis, value in enumerate(ray_momentum(rays_at(world, node.position), definition)):
            in_flight[axis] += value
        stock += sum(ray.amount for ray in rays_at(world, node.position))
    assert stock == 76 and in_flight == [16, 4, 0]
    # (c) A ray flagged returning walks its steps and its phase back one Link at a
    # time on its own line, and is refused a Link beyond its event Node.
    returning = Ray(
        0, (0, 0, 0), 5, phase=1, steps=5, outbound=0, event_ports=1, event_shares=(5,) + (0,) * 5
    )
    walked = []
    for _ in range(5):
        ports, kept = forward_rays((returning,), definition, CostMeter(initial.operation_costs))
        assert kept == () and [len(p) for p in ports] == [1, 0, 0, 0, 0, 0]
        (returning,) = ports[0]
        walked.append((returning.steps, returning.phase))
    assert walked == [(4, 0), (3, 7), (2, 6), (1, 5), (0, 4)]
    assert returning.outbound == 0 and returning.event_ports == 1
    with pytest.raises(ValueError, match="event Node"):
        forward_rays((returning,), definition, CostMeter(initial.operation_costs))
    for invalid in (
        {"steps": -1},
        {"outbound": 2},
        {"event_ports": 64},
        {"event_ports": 0b000001, "event_shares": (5, 1, 0, 0, 0, 0)},
        {"detector": 3},
    ):
        with pytest.raises(ValueError, match="ray"):
            validate_rays((replace(a_ray, **invalid),), definition, field)
    # The runner records the model identity beside the sampling profile.
    path = tmp_path / "rays.json"
    path.write_text(json.dumps(document()), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=4)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["ray_state"] == RAY_EVENT_STATE == "ray-event-state-v1"
    assert metadata["sampling_profile"] == "detector-only-v1"
    assert metadata["conserved_at_every_completed_tick"] and metadata["final_totals"]["quanta"] == [1200]
