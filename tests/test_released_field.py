"""Field as the ray's information (released-field-v1): a ray releases its field at
every Node it crosses as one ray per heading except its own, booked as a source and
costing the ray nothing; a straight ray never shares a Node with its own field; a
declared rule turns a ray that meets a field ray and returns the field ray reversed
as the recoil; a family with no coupling to the field crosses it.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Released field")
before the first run: lamps fire electron rays under the shared Detector admission.
"""

import json

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import CostMeter, OperationCosts
from event_universe.core.spatial_state import (
    RAY_MEETING,
    RELEASED_FIELD,
    Ray,
    ray_layer_names,
    ray_merge_key,
    release_field,
)
from event_universe.fields.ray_interactions import apply_ray_interactions
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
COSTS = OperationCosts((1,) * 9)
# The declared coupling of an electron with the electron field: the electron leaves
# on the field ray's heading, away from the source line, and the field ray returns
# reversed as the recoil; energy is the declared invariant.
TURN = {
    "name": "turn",
    "participants": [{"type": "electron"}, {"type": "G"}],
    "outputs": [
        {"field": "electron", "amount": {"of": 0}, "heading": "same", "input": 1, "phase": {"of": 0}},
        {"field": "G", "amount": {"of": 1}, "heading": "reversed", "input": 1},
    ],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}


def field(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def ray_field(name, advance, slots=8, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "kerengonen": {"phase_steps": 8, "phase_advance": advance},
    } | extra


def document(lamps, rules=(), spatial=None, ticks=4):
    """The board: `lamps` are (position, family, amount, heading index)."""
    families = sorted({family for _, family, _, _ in lamps} | {"electron", "G"})
    return {
        "schema_version": 1,
        "model_id": "released-field-test-v1",
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
        "fields": [field(name) for name in families],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": [family],
                "defaults": {family: amount},
                "transport": {"mode": "hold"},
            }
            for index, (_, family, amount, _) in enumerate(lamps)
        ],
        "spatial_fields": spatial
        if spatial is not None
        else [ray_field(name, 0 if name == "G" else 1) for name in families if name != "G"]
        + [ray_field("G", 0, 16, field_of="electron", release=[1, 4])],
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": family,
                "amount": amount,
                "denominator": 1,
                "source": False,
                "heading": HEADINGS[heading],
                "kerengonen_phase": 0,
            }
            for index, (_, family, amount, heading) in enumerate(lamps)
        ],
        "seeds": [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (position, _, _, _) in enumerate(lamps)
        ],
        "ray_interactions": list(rules),
    }


def bundles(world, position):
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    return () if node is None or not node.rays else node.rays


def rays_at(world, position, family):
    """The resident rays of one family at a Node, in merge-key order."""
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    node = bundles(world, position)
    return sorted(node[index], key=ray_merge_key) if node else []


def positions_of(world, family):
    return {n.position for n in world.inventory_view().nodes if rays_at(world, n.position, family)}


def lamp(world, type_index):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    )


def emitted(heading, steps, phase, amount=5):
    """A lamp's ray: one event on the heading's Port."""
    shares = [0] * 6
    shares[heading] = amount
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        steps=steps,
        event_ports=1 << heading,
        event_shares=tuple(shares),
    )


def released(heading, steps, phase):
    """A field ray: no event, the source's phase, amount floor(5 x 1 / 4) = 1."""
    return Ray(heading, (0, 0, 0), 1, phase=phase, steps=steps)


def product(heading, amount, phase, mask, shares, steps=0):
    return Ray(
        heading, (0, 0, 0), amount, phase=phase, steps=steps, event_ports=mask, event_shares=shares
    )


def meet(initial, node):
    return apply_ray_interactions(
        node,
        initial.spatial_fields,
        initial.fields,
        initial.ray_interactions,
        CostMeter(COSTS),
        COSTS,
    )


STRAIGHT = (((5, 7, 7), "electron", 5, 0),)
MEETING = (((5, 7, 7), "electron", 5, 0), ((8, 8, 7), "electron", 5, 1), ((6, 7, 10), "c", 3, 5))
# The Nodes the five rays of one release reach after one Link, by heading, from N.
AROUND = {1: (-1, 0, 0), 2: (0, 1, 0), 3: (0, -1, 0), 4: (0, 0, 1), 5: (0, 0, -1)}
# The recoils: the reversed G ray of each meeting, where it is after ticks 3 and 4.
RECOILS = {
    (7, 7, 7): (2, (0, 0, 1, 5, 0, 0), ((7, 8, 7), (7, 9, 7))),
    (6, 8, 7): (3, (0, 0, 5, 1, 0, 0), ((6, 7, 7), (6, 6, 7))),
}


@pytest.mark.parametrize("case", ["straight", "meeting", "rejected"])
def test_a_ray_releases_its_field_which_returns_reversed_from_a_declared_meeting(tmp_path, case):
    if case == "rejected":
        # (d) Malformed released fields are rejected at initialization.
        electron = ray_field("electron", 1)
        for spatial, message in (
            ([electron, ray_field("G", 0, field_of="electron")], "field_of and release together"),
            ([electron, ray_field("G", 0, field_of="electron", release=[5, 4])], "must not exceed"),
            ([electron, ray_field("G", 0, field_of="G", release=[1, 4])], "not its own field"),
            (
                [
                    ray_field("electron", 1, field_of="G", release=[1, 4]),
                    ray_field("G", 0, field_of="electron", release=[1, 4]),
                ],
                "a field has no field",
            ),
            (
                [
                    electron,
                    ray_field("G", 0, field_of="electron", release=[1, 4], headings=HEADINGS[:5]),
                ],
                "six Port headings",
            ),
            (
                [
                    electron,
                    ray_field("G", 0, field_of="electron", release=[1, 4])
                    | {"kerengonen": {"phase_steps": 4, "phase_advance": 0}},
                ],
                "its source's phase steps",
            ),
        ):
            with pytest.raises(ValueError, match=message):
                parse_initial_state(document(STRAIGHT, spatial=spatial))
        return
    if case == "straight":
        # (a) One electron on a straight line releases five G rays at every Node it
        # crosses, unchanged itself, never sharing a Node with its own field.
        initial = parse_initial_state(document(STRAIGHT, ticks=5))
        world = Simulation(initial)
        for tick in range(1, 6):
            world.step()
            assert world.totals() == {"G": (5 * (tick - 1),), "electron": (5,)}
            assert world.source_totals() == {"G": (5 * (tick - 1),), "electron": (0,)}
            assert all(item["balanced"] for item in world.spatial_accounting().values())
            assert lamp(world, 0) == {"electron": (0,)}
            electron = (5 + tick, 7, 7)
            assert rays_at(world, electron, "electron") == [emitted(0, tick, tick)]
            assert positions_of(world, "electron") == {electron}
            assert electron not in positions_of(world, "G")
            for release in range(2, tick + 1):
                node, walked = (4 + release, 7, 7), tick - release + 1
                for heading, step in AROUND.items():
                    at = tuple(n + walked * s for n, s in zip(node, step, strict=True))
                    assert rays_at(world, at, "G") == [released(heading, walked, release - 1)]
            assert sum(len(rays_at(world, p, "G")) for p in positions_of(world, "G")) == 5 * (tick - 1)
            if tick == 2:
                # The release itself: five rays, one per Port heading but the ray's own.
                assert release_field(
                    (emitted(0, 1, 1),), initial.spatial_fields[1], initial.spatial_fields[0]
                ) == tuple(released(heading, 0, 1) for heading in AROUND)
        return
    # (b), (c) Two electrons on parallel lines meet each other's field at tick 3 and
    # turn away from the source line; the field rays return reversed; c crosses.
    initial = parse_initial_state(document(MEETING, [TURN]))
    assert ray_layer_names(initial.fields, initial.spatial_fields, initial.ray_interactions) == (
        ("G", "electron"),
        ("c",),
    )
    world = Simulation(initial)
    for tick in range(1, 5):
        world.step()
        assert world.totals() == {"G": (10 * (tick - 1),), "c": (3,), "electron": (10,)}
        assert world.source_totals() == {"G": (10 * (tick - 1),), "c": (0,), "electron": (0,)}
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        if tick <= 2:
            # No electron has turned before the first meeting.
            assert all(
                ray.heading in (0, 1)
                for p in positions_of(world, "electron")
                for ray in rays_at(world, p, "electron")
            )
        if tick == 2:
            assert rays_at(world, (7, 7, 7), "electron") == [emitted(0, 2, 2)]
            assert rays_at(world, (7, 7, 7), "G") == [released(3, 1, 1)]
            assert rays_at(world, (6, 8, 7), "electron") == [emitted(1, 2, 2)]
            assert rays_at(world, (6, 8, 7), "G") == [released(2, 1, 1)]
            # Each electron released five G rays at the Node it departed, one per
            # heading but its own, behind it and away from its line.
            for node, own in (((6, 7, 7), 0), ((7, 8, 7), 1)):
                for around in range(6):
                    if around == own:
                        continue
                    at = tuple(n + s for n, s in zip(node, HEADINGS[around], strict=True))
                    assert rays_at(world, at, "G") == [released(around, 1, 1)]
            assert rays_at(world, (6, 7, 8), "c") == [emitted(5, 2, 2, 3)]
            assert rays_at(world, (6, 7, 8), "G") == [released(4, 1, 1)]
            # The first meetings, at tick 3: the electron leaves on the field ray's
            # heading, away from the source line, and the field ray returns reversed
            # (one bundle per spatial field, in the order c, electron, G).
            assert meet(initial, bundles(world, (7, 7, 7))) == (
                (),
                (product(3, 5, 2, 12, (0, 0, 1, 5, 0, 0)),),
                (product(2, 1, 1, 12, (0, 0, 1, 5, 0, 0)),),
            )
            assert meet(initial, bundles(world, (6, 8, 7))) == (
                (),
                (product(2, 5, 2, 12, (0, 0, 5, 1, 0, 0)),),
                (product(3, 1, 1, 12, (0, 0, 5, 1, 0, 0)),),
            )
        if tick >= 3:
            walked = tick - 2
            assert rays_at(world, (7, 7 - walked, 7), "electron") == [
                product(3, 5, 2 + walked, 12, (0, 0, 1, 5, 0, 0), walked)
            ]
            assert rays_at(world, (6, 8 + walked, 7), "electron") == [
                product(2, 5, 2 + walked, 12, (0, 0, 5, 1, 0, 0), walked)
            ]
            assert (
                rays_at(world, (7, 7, 7), "electron") == []
                and rays_at(world, (6, 8, 7), "electron") == []
            )
            for heading, shares, path in RECOILS.values():
                assert product(heading, 1, 1, 12, shares, walked) in rays_at(
                    world, path[walked - 1], "G"
                )
        if tick == 3:
            for node, own in (((7, 7, 7), 3), ((6, 8, 7), 2)):
                for around in range(6):
                    if around == own:
                        continue
                    at = tuple(n + s for n, s in zip(node, HEADINGS[around], strict=True))
                    assert released(around, 1, 2) in rays_at(world, at, "G")
            # (c) The c ray shares (6,7,7) with three G rays and is not a participant.
            assert rays_at(world, (6, 7, 7), "c") == [emitted(5, 3, 3, 3)]
            assert rays_at(world, (6, 7, 7), "G") == sorted(
                [released(1, 1, 2), released(3, 1, 2), product(3, 1, 1, 12, (0, 0, 5, 1, 0, 0), 1)],
                key=ray_merge_key,
            )
        if tick == 4:
            assert rays_at(world, (6, 7, 6), "c") == [emitted(5, 4, 4, 3)]
            assert rays_at(world, (6, 7, 6), "G") == []
    path = tmp_path / "meeting.json"
    path.write_text(json.dumps(document(MEETING, [TURN])), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=4)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert metadata["released_field"] == RELEASED_FIELD == "released-field-v1"
    assert metadata["released_fields"] == [{"field": "G", "field_of": "electron", "release": [1, 4]}]
    assert metadata["ray_meeting"] == RAY_MEETING
    assert metadata["ray_layer_families"] == [["G", "electron"], ["c"]]
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["final_totals"] == {"G": [30], "c": [3], "electron": [10]}
    assert metadata["source_totals"] == {"G": [30], "c": [0], "electron": [0]}
