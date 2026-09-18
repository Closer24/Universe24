"""Ray layers (ray-layers-v1): rules of different layers fire in one interval, an
unruled family crosses, and the layers are derived from the declared couplings.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Ray layers") before
the first run: five lamps around one Node fire one ray each of families a, a, b,
b and c at it, under the shared Detector admission.
"""

import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    RAY_EVENT_STATE,
    RAY_LAYERS,
    Ray,
    ray_layer_names,
    ray_layers,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

CENTER = (7, 7, 7)
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z], closed under negation.
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# Family, lamp position and heading index toward the center, one lamp per ray.
LAMPS = (
    ("a", (5, 7, 7), 0),
    ("a", (9, 7, 7), 1),
    ("b", (7, 5, 7), 2),
    ("b", (7, 9, 7), 3),
    ("c", (7, 7, 5), 4),
)
# (x, y, z) to (z, x, y): +Y turns to +Z and -Y to -Z.
TURN = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]


def ray_field(participant, name):
    return {"field": name, "participant": participant}


def rule(name, family, assignments):
    """Two rays of one family with equal amounts and opposite headings."""
    same_amount = {"op": "eq", "args": [ray_field(0, "amount"), ray_field(1, "amount")]}
    heading_sum = {"op": "add", "args": [ray_field(0, "heading"), ray_field(1, "heading")]}
    head_on = {"op": "eq", "args": [{"op": "dot", "args": [heading_sum, heading_sum]}, 0]}
    return {
        "name": name,
        "participants": [{"type": family}, {"type": family}],
        "when": {"op": "mul", "args": [same_amount, head_on]},
        "assignments": assignments,
        "invariants": [
            {
                "name": "energy",
                "expression": {"op": "add", "args": [ray_field(0, "amount"), ray_field(1, "amount")]},
            },
            {
                "name": "momentum",
                "expression": {
                    "op": "add",
                    "args": [
                        {"op": "mul", "args": [ray_field(0, "amount"), ray_field(0, "heading")]},
                        {"op": "mul", "args": [ray_field(1, "amount"), ray_field(1, "heading")]},
                    ],
                },
            },
        ],
    }


A_SWAP = rule(
    "a_swap",
    "a",
    [
        {"participant": 0, "field": "heading", "expression": ray_field(1, "heading")},
        {"participant": 1, "field": "heading", "expression": ray_field(0, "heading")},
    ],
)
B_TURN = rule(
    "b_turn",
    "b",
    [
        {
            "participant": p,
            "field": "heading",
            "expression": {"op": "transform", "matrix": TURN, "args": [ray_field(p, "heading")]},
        }
        for p in (0, 1)
    ]
    + [{"participant": p, "field": "phase", "expression": 6} for p in (0, 1)],
)


def scalar(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def document(rules, ticks=4):
    return {
        "schema_version": 1,
        "K": 5,
        "model_id": "ray-layers-test-v1",
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
            scalar("a"),
            scalar("b"),
            scalar("c"),
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
                "name": f"lamp_{index}",
                "fields": ["a", "b", "c", "momentum"],
                "defaults": {"a": 0, "b": 0, "c": 0, "momentum": [0, 0, 0]} | {family: 5},
                "transport": {"mode": "hold"},
            }
            for index, (family, _, _) in enumerate(LAMPS)
        ],
        "spatial_fields": [
            {
                "field": name,
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 1,
                "ray_slots": 8,
                "metric": "links",
                "pace": [1, 1],
                "kerengonen": {"phase_steps": 8},
                # The clock is the content (clock-readings-v1): one step per interval at K.
                "clock": True,
            }
            for name in ("a", "b", "c")
        ],
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": family,
                "amount": 5,
                "denominator": 1,
                "heading": HEADINGS[heading],
            }
            for index, (family, _, heading) in enumerate(LAMPS)
        ],
        "seeds": [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (_, position, _) in enumerate(LAMPS)
        ],
        "ray_interactions": rules,
        "conservation": {
            "name": "quanta",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["a", "b", "c", "momentum"],
                    "energy": {
                        "op": "add",
                        "args": [
                            {"field": "a"},
                            {"op": "add", "args": [{"field": "b"}, {"field": "c"}]},
                        ],
                    },
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {
                    "op": "add",
                    "args": [
                        {"field": "a", "side": "right"},
                        {
                            "op": "add",
                            "args": [{"field": "b", "side": "right"}, {"field": "c", "side": "right"}],
                        },
                    ],
                },
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        },
    }


def rays_at(world, position):
    """The rays resident at a position as (family, ray) pairs, family by field index."""
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    if node is None or not node.rays:
        return []
    # bit-law-v1 (2026-09-18): a ray carries the identity of the thing that emitted
    # it (`owner`); this module pins lines and events, not identities (test_bit_law does).
    return [
        ("abc"[index], replace(ray, owner=0)) for index, bundle in enumerate(node.rays) for ray in bundle
    ]


def lamp(world, type_index):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    )


def emitted(heading, steps, phase):
    """A lamp's ray: the emission is one event on the heading's Port."""
    shares = [0] * 6
    shares[heading] = 5
    return Ray(
        heading,
        (0, 0, 0),
        5,
        phase=phase,
        steps=steps,
        event_ports=1 << heading,
        event_shares=tuple(shares),
    )


def swapped(heading, steps, phase):
    return Ray(
        heading,
        (0, 0, 0),
        5,
        phase=phase,
        steps=steps,
        event_ports=0b000011,
        event_shares=(5, 5, 0, 0, 0, 0),
    )


def turned(heading, steps, phase):
    return Ray(
        heading,
        (0, 0, 0),
        5,
        phase=phase,
        steps=steps,
        event_ports=0b110000,
        event_shares=(0, 0, 0, 0, 5, 5),
    )


# The case "a_and_b" was deleted on 2026-09-18 with feature 18 (lanes-v1,
# Highlights 5.4 point 25, the model owner's decision on the case it left open):
# with the b rule declared, a turned b ray and the c ray are given one lane at
# the meeting Node, two real rays of different families, a meeting the table of
# the pair decides, which no departure holds; the world declares none, and its
# premise, an unruled family crossing a ruled one on one lane, has no lawful form.
@pytest.mark.parametrize("declared", ["a_only"])
def test_rules_of_different_layers_fire_in_one_interval_and_an_unruled_family_crosses(
    tmp_path, declared
):
    rules = [A_SWAP, B_TURN] if declared == "a_and_b" else [A_SWAP]
    initial = parse_initial_state(document(rules))
    # (a) Layers are derived, never declared: the connected components of the ray
    # fields over the rules' participants; a field no rule selects is its own layer.
    assert ray_layers(initial.spatial_fields, initial.ray_interactions) == ((0,), (1,), (2,))
    assert ray_layer_names(initial.fields, initial.spatial_fields, initial.ray_interactions) == (
        ("a",),
        ("b",),
        ("c",),
    )
    coupled = parse_initial_state(
        document(
            [
                rule("a_meets_b", "a", A_SWAP["assignments"])
                | {"participants": [{"type": "a"}, {"type": "b"}]}
            ]
        )
    )
    assert ray_layers(coupled.spatial_fields, coupled.ray_interactions) == ((0, 1), (2,))
    assert ray_layer_names(coupled.fields, coupled.spatial_fields, coupled.ray_interactions) == (
        ("a", "b"),
        ("c",),
    )
    assert ray_layers(initial.spatial_fields, ()) == ((0,), (1,), (2,))
    world = Simulation(initial)
    for tick in range(1, 5):
        world.step()
        # (f) Five rays every tick, exact totals and audit, accounting balanced.
        assert sum(len(rays_at(world, n.position)) for n in world.inventory_view().nodes) == 5
        assert world.totals() == {"a": (10,), "b": (10,), "c": (5,), "momentum": (0, 0, 0)}
        report = world.conservation_report()
        assert report["status"] == "passed"
        assert report["current"]["energy"] == 25 and tuple(report["current"]["momentum"]) == (0, 0, 0)
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        if tick == 1:
            # (b) Each lamp paid its ray and recoiled by amount x heading.
            for index, (_family, _, heading) in enumerate(LAMPS):
                recoil = tuple(-5 * component for component in HEADINGS[heading])
                assert lamp(world, index) == {"a": (0,), "b": (0,), "c": (0,), "momentum": recoil}
        elif tick == 2:
            # (b) All five rays are resident at the center, none met yet.
            resident = rays_at(world, CENTER)
            assert sorted(resident, key=lambda item: item[1].heading) == [
                (family, emitted(heading, 2, 2)) for family, _, heading in LAMPS
            ]
        elif tick == 3:
            # (c) Two events at one Node in one interval, layer by layer: the a rays
            # swapped headings, the b rays turned to +Z and -Z at phase 6 then 7, and
            # the c ray crossed unchanged with its emission's event record.
            assert rays_at(world, CENTER) == []
            assert rays_at(world, (6, 7, 7)) == [("a", swapped(1, 1, 3))]
            assert rays_at(world, (8, 7, 7)) == [("a", swapped(0, 1, 3))]
            if declared == "a_and_b":
                assert rays_at(world, (7, 7, 8)) == [("b", turned(4, 1, 7)), ("c", emitted(4, 3, 3))]
                assert rays_at(world, (7, 7, 6)) == [("b", turned(5, 1, 7))]
                assert rays_at(world, (7, 6, 7)) == [] and rays_at(world, (7, 8, 7)) == []
            else:
                # (d) Without its rule the b family is still its own layer and crosses.
                assert rays_at(world, (7, 7, 8)) == [("c", emitted(4, 3, 3))]
                assert rays_at(world, (7, 7, 6)) == []
                assert rays_at(world, (7, 8, 7)) == [("b", emitted(2, 3, 3))]
                assert rays_at(world, (7, 6, 7)) == [("b", emitted(3, 3, 3))]
        elif declared == "a_and_b":
            # (e) A b ray and the c ray share one Node and one line without meeting.
            assert rays_at(world, (7, 7, 9)) == [("b", turned(4, 2, 0)), ("c", emitted(4, 4, 4))]
            assert rays_at(world, (5, 7, 7)) == [("a", swapped(1, 2, 4))]
            assert rays_at(world, (9, 7, 7)) == [("a", swapped(0, 2, 4))]
    # (f) The runner records the identity and the derived layers beside the ray state.
    path = tmp_path / "layers.json"
    path.write_text(json.dumps(document(rules)), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=4)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["ray_layers"] == RAY_LAYERS == "ray-layers-v1"
    assert metadata["ray_layer_families"] == [["a"], ["b"], ["c"]]
    assert metadata["ray_state"] == RAY_EVENT_STATE == "ray-event-state-v1"
    assert metadata["conserved_at_every_completed_tick"]
    assert {name: metadata["final_totals"][name] for name in "abc"} == {"a": [10], "b": [10], "c": [5]}
