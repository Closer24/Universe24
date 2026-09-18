"""Polarization as a ray property (ray-polarization-v1, Highlights 3.26 and 3.19,
issue #169 feature 11): a family property read only at a meeting, a transverse
direction modulo a half turn in steps of the family's polarization circle
(2^polarization_bits steps per half turn, the family's phase width by default) or
none; a lamp declares the polarization of what it emits; rays merge only at equal
polarization; a meeting's outputs carry their source input's unless they declare
one; a spread carries the axial mean; the return keeps it; and the polarizer, an
external body's coupling, splits an arriving ray by its declared table at the
difference between the body's angle and the ray's polarization, the pass share
leaving on the pass Port with the body's angle, the rest into the body's sink and
the shares below one quantum into the body's registers until they reach one.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Ray polarization")
before the first run: lamp, polarizer, return, meeting, spread, identity and
rejected.
"""

import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import FieldDefinition
from event_universe.core.spatial_state import (
    POLARIZATION_NONE,
    RAY_POLARIZATION_PROPERTY,
    Polarizer,
    Ray,
    SpatialFieldDefinition,
    combined_polarization,
    merge_rays,
    polarizer_share,
    ray_merge_key,
    validate_rays,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# The reference table at three bits, cos^2(d x 22.5 degrees) in eighths, rounded:
# the Born table read over the polarization circle of eight steps per half turn.
TABLE = [8, 7, 4, 1, 0, 1, 4, 7]
NONE = POLARIZATION_NONE


def scalar(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def ray_field(name, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 16,
        "metric": "links",
        "pace": [1, 1],
        "kerengonen": {"phase_steps": 8, "phase_advance": 0},
    } | extra


def lamp(position, amount, heading, polarization=None, pulses=1):
    """A light lamp: it holds `pulses` x `amount` and emits `amount` per interval
    along one heading, with the declared polarization when one is given."""
    return {
        "position": position,
        "amount": amount,
        "heading": heading,
        "polarization": polarization,
        "pulses": pulses,
    }


def polarizer_body(angle, position=(7, 7, 7), **extra):
    return {
        "position": list(position),
        "family": "apparatus",
        "amount": 1,
        "coupling": "polarizer",
        "polarizer": {"family": "light", "angle": angle, "pass": [1, 0, 0], "table": TABLE} | extra,
    }


def document(lamps, bodies=(), rules=(), detectors=(), ticks=6, light=None, families=("light",)):
    """A periodic 15^3 board: the light family with an eight-step phase and a
    polarization circle of eight steps per half turn (`polarization_bits` 3 unless
    `light` overrides the entry), the apparatus family of a polarizer body."""
    names = list(families) + (["apparatus"] if bodies else [])
    spatial = []
    for name in names:
        entry = ray_field(name)
        if name == "light":
            entry |= {"polarization_bits": 3} if light is None else light
        spatial.append(entry)
    return {
        "schema_version": 1,
        "model_id": "ray-polarization-test-v1",
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
        "fields": [scalar(name) for name in names],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": ["light"],
                "defaults": {"light": item["amount"] * item["pulses"]},
                "transport": {"mode": "hold"},
            }
            for index, item in enumerate(lamps)
        ],
        "spatial_fields": spatial,
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": "light",
                "amount": item["amount"],
                "denominator": 1,
                "source": False,
                "heading": HEADINGS[item["heading"]],
                "kerengonen_phase": 0,
            }
            | ({} if item["polarization"] is None else {"polarization": item["polarization"]})
            for index, item in enumerate(lamps)
        ],
        "seeds": [
            {"position": list(item["position"]), "type": f"lamp_{index}"}
            for index, item in enumerate(lamps)
        ],
        "ray_interactions": list(rules),
        **({"external_bodies": list(bodies)} if bodies else {}),
        **({"detectors": list(detectors)} if detectors else {}),
    }


def rays_at(world, position):
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    if node is None or not node.rays:
        return []
    # bit-law-v1 (2026-09-18): a ray carries the identity of the thing that emitted
    # it (`owner`); this module pins lines and events, not identities (test_bit_law does).
    return sorted((replace(ray, owner=0) for bundle in node.rays for ray in bundle), key=ray_merge_key)


def inventory(world):
    """Every ray in the world: (Node, heading, amount, steps, outbound, polarization)."""
    return sorted(
        (node.position, ray.heading, ray.amount, ray.steps, ray.outbound, ray.polarization)
        for node in world.inventory_view().nodes
        if node.rays
        for bundle in node.rays
        for ray in bundle
    )


def emitted(heading, steps, amount, polarization, phase=0):
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
        polarization=polarization,
    )


def merged_pair(polarization):
    """Two events of 4 on +X merged into one ray of 8 that keeps their record."""
    return Ray(
        0,
        (0, 0, 0),
        8,
        steps=1,
        event_ports=1,
        event_shares=(4, 0, 0, 0, 0, 0),
        polarization=polarization,
    )


def passed(steps, amount, polarization, detector=1):
    """A polarizer's pass ray: a fresh event on +X of the body's Node."""
    return Ray(
        0,
        (0, 0, 0),
        amount,
        steps=steps,
        event_ports=1,
        event_shares=(amount, 0, 0, 0, 0, 0),
        detector=detector,
        polarization=polarization,
    )


def body_state(world):
    return world.external_bodies()[0]


def step(world, ticks):
    for _ in range(ticks):
        world.step()
        assert all(item["balanced"] for item in world.spatial_accounting().values())


MEETING = {
    "name": "meeting",
    "participants": [{"type": "light"}, {"type": "light"}],
    "outputs": [
        {"field": "light", "amount": {"of": 0}, "heading": 2},
        {"field": "light", "amount": {"of": 1}, "heading": 3, "input": 1},
    ],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}


def meeting(polarizations=None, when=None):
    rule = json.loads(json.dumps(MEETING))
    if polarizations is not None:
        for output, value in zip(rule["outputs"], polarizations, strict=True):
            if value is not None:
                output["polarization"] = value
    if when is not None:
        rule["when"] = when
    return rule


@pytest.mark.parametrize(
    "case", ["lamp", "polarizer", "return", "meeting", "spread", "identity", "rejected"]
)
def test_polarization_is_a_ray_property_read_by_the_polarizer(tmp_path, case):
    events = []
    if case == "lamp":
        # (a) A lamp declares the polarization of what it emits; the ray carries it
        # along its line; two identical events of equal polarization merge and two
        # of different polarization stay two rays.
        world = Simulation(parse_initial_state(document([lamp((4, 7, 7), 8, 0, 2)])))
        for n in range(1, 4):
            step(world, 1)
            assert rays_at(world, (4 + n, 7, 7)) == [emitted(0, n, 8, 2)]
            assert world.totals() == {"light": (8,)}
        world = Simulation(
            parse_initial_state(document([lamp((4, 7, 7), 4, 0, 2), lamp((4, 7, 7), 4, 0, 2)]))
        )
        step(world, 1)
        # Two identical events of two things stay two rays (bit-law-v1, 2026-09-18:
        # the identity is part of a ray's record and rays of two things never merge).
        assert rays_at(world, (5, 7, 7)) == [emitted(0, 1, 4, 2), emitted(0, 1, 4, 2)]
        world = Simulation(
            parse_initial_state(document([lamp((4, 7, 7), 4, 0, 2), lamp((4, 7, 7), 4, 0, 6)]))
        )
        step(world, 1)
        assert rays_at(world, (5, 7, 7)) == [emitted(0, 1, 4, 2), emitted(0, 1, 4, 6)]
        world = Simulation(parse_initial_state(document([lamp((4, 7, 7), 4, 0), lamp((4, 7, 7), 4, 0)])))
        step(world, 1)
        assert rays_at(world, (5, 7, 7)) == [emitted(0, 1, 4, NONE), emitted(0, 1, 4, NONE)]
        # The pure function: rays of one event and line merge at equal polarization
        # only, the unpolarized one ordered first.
        three, five = replace(merged_pair(2), amount=3), replace(merged_pair(2), amount=5)
        assert merge_rays((three, five)) == (merged_pair(2),)
        assert merge_rays((three, replace(five, polarization=NONE))) == (
            replace(five, polarization=NONE),
            three,
        )
        return
    if case == "polarizer":
        # (b) A polarizer at angle theta meets a ray polarized along +Y (step 0): the
        # pass share is the table at the difference, the rest sinks, and the shares
        # below one quantum wait in the body's registers until they reach one.
        for angle, amount, pulses, passes, sunk, held, held_total in (
            (0, 8, 1, {(10, 7, 7): 8}, 0, [0] * 6, 0),
            (2, 8, 1, {(10, 7, 7): 4}, 4, [0] * 6, 0),
            (4, 8, 1, {}, 8, [0] * 6, 0),
            (1, 8, 1, {(10, 7, 7): 7}, 1, [0] * 6, 0),
            (1, 5, 1, {(10, 7, 7): 4}, 0, [0, 0, 3, 5, 0, 0], 1),
            (1, 5, 3, {(10, 7, 7): 4, (9, 7, 7): 4, (8, 7, 7): 5}, 1, [0, 0, 1, 7, 0, 0], 1),
        ):
            events.clear()
            raw = document([lamp((4, 7, 7), amount, 0, 0, pulses)], [polarizer_body(angle)])
            world = Simulation(parse_initial_state(raw), observer=events.append)
            step(world, 6)
            for position, share in passes.items():
                assert rays_at(world, position) == [passed(position[0] - 7, share, angle)], (
                    angle,
                    amount,
                    pulses,
                    position,
                )
            assert len(inventory(world)) == len(passes)
            assert world.totals() == {"light": (amount * pulses - sunk,), "apparatus": (0,)}
            assert world.external_body_totals() == {"light": (sunk,), "apparatus": (0,)}
            state = body_state(world)
            assert state["sink"] == ({"light": sunk} if sunk else {})
            assert state["held"] == held and sum(held) == 8 * held_total
            assert state["momentum"] == [0, 0, 0]
            assert not any(e["event"] == "external_body_step" for e in events)
        # The records of the last world: one polarizer record per pulse and one
        # absorbed record for the quantum the sink register released.
        records = [e for e in events if e["event"] == "polarizer"]
        assert [
            (e["tick"], e["passed"], e["sunk"], e["held"], e["released"], e["registers"])
            for e in records
        ] == [
            (3, 4, 0, [3, 5], [0, 0], [0, 0, 3, 5, 0, 0]),
            (4, 4, 0, [3, 5], [0, 1], [0, 0, 6, 2, 0, 0]),
            (5, 4, 0, [3, 5], [1, 0], [0, 0, 1, 7, 0, 0]),
        ]
        assert all(
            (e["position"], e["body"], e["port"], e["family"], e["amount"], e["polarization"])
            == ((7, 7, 7), 0, 1, "light", 5, 0)
            for e in records
        )
        assert all(
            (e["sign"], e["angle"], e["difference"], e["share"], e["steps"]) == (0, 1, 1, 7, 8)
            for e in records
        )
        assert [
            (e["tick"], e["amount"], e["family"])
            for e in events
            if e["event"] == "external_body_absorbed"
        ] == [(4, 1, "light")]
        # An unpolarized ray takes the table's mean, half; the pure functions.
        events.clear()
        world = Simulation(
            parse_initial_state(document([lamp((4, 7, 7), 8, 0)], [polarizer_body(1)])),
            observer=events.append,
        )
        step(world, 6)
        assert rays_at(world, (10, 7, 7)) == [passed(3, 4, 1)]
        assert world.external_body_totals() == {"light": (4,), "apparatus": (0,)}
        record = next(e for e in events if e["event"] == "polarizer")
        assert (record["polarization"], record["difference"], record["share"]) == (None, None, 4)
        polarizer = Polarizer(1, 1, 0, tuple(TABLE), 4)
        assert [polarizer_share(polarizer, p) for p in (NONE, 0, 1, 3, 5)] == [
            (-1, 4),
            (1, 7),
            (0, 8),
            (6, 4),
            (4, 0),
        ]
        # The runner records the identity, the registers and the sink.
        path = tmp_path / "polarizer.json"
        path.write_text(json.dumps(document([lamp((4, 7, 7), 5, 0, 0)], [polarizer_body(1)])))
        run_initialization(path, tmp_path / "out", ticks=6)
        metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
        assert metadata["ray_polarization"] == RAY_POLARIZATION_PROPERTY
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["final_totals"] == {"light": [5], "apparatus": [0]}
        assert metadata["external_body_totals"] == {"light": [0], "apparatus": [0]}
        final = metadata["external_bodies"][0]
        assert final["coupling"] == "polarizer"
        assert final["polarizer"] == {
            "family": "light",
            "angle": 1,
            "pass": [1, 0, 0],
            "steps": 8,
            "unpolarized": 4,
        }
        assert final["final"]["held"] == [0, 0, 3, 5, 0, 0]
        return
    if case == "return":
        # (c) The return keeps the polarization: a mark of setting 0 behind the
        # polarizer returns the passed ray reversed, its polarization the body's
        # angle; the returning ray ends in the polarizer's sink as every returning
        # ray at a body does.
        raw = document(
            [lamp((4, 7, 7), 8, 0, 0)],
            [polarizer_body(2)],
            detectors=[{"position": [9, 7, 7], "setting": [0, 1], "seed": 0}],
            ticks=7,
        )
        world = Simulation(parse_initial_state(raw), observer=events.append)
        step(world, 5)
        assert [e["event"] for e in events if e["event"].startswith("detector")] == ["detector_return"]
        assert inventory(world) == [((9, 7, 7), 1, 4, 2, 0, 2)]
        step(world, 1)
        assert inventory(world) == [((8, 7, 7), 1, 4, 1, 0, 2)]
        returning = rays_at(world, (8, 7, 7))[0]
        assert (returning.detector, returning.event_ports, returning.event_shares) == (
            1,
            1,
            (4, 0, 0, 0, 0, 0),
        )
        step(world, 1)
        assert inventory(world) == []
        assert world.external_body_totals() == {"light": (8,), "apparatus": (0,)}
        assert body_state(world)["sink"] == {"light": 8}
        assert not any(e["event"] == "inverse_split" for e in events)
        return
    if case == "meeting":
        # (d) A meeting's outputs carry their source input's polarization unless the
        # output declares it: input i's, none, or a step; a guard reads it.
        lamps = [lamp((5, 7, 7), 5, 0, 1), lamp((9, 7, 7), 5, 1, 3)]
        base_cost = None
        for polarizations, expected, declared in (
            (None, (1, 3), False),
            (({"of": 1}, "none"), (3, NONE), True),
            ((5, {"of": 0}), (5, 1), True),
            (("same", "same"), (1, 3), False),
        ):
            events.clear()
            initial = parse_initial_state(document(lamps, rules=[meeting(polarizations)]))
            assert initial.ray_interactions[0].polarization_declared is declared
            world = Simulation(initial, observer=events.append)
            step(world, 3)
            assert inventory(world) == [
                ((7, 6, 7), 3, 5, 1, 1, expected[1]),
                ((7, 8, 7), 2, 5, 1, 1, expected[0]),
            ]
            assert world.totals() == {"light": (10,)}
            cost = next(
                e["cost"]
                for e in events
                if e["event"] == "spatial_cycle" and e["position"] == (7, 7, 7) and e["tick"] == 2
            )
            # One more view component read per participant and one update per
            # output when the rule names the property; the cost it had otherwise.
            if declared:
                assert base_cost is not None and cost == base_cost + 4
            elif base_cost is None:
                base_cost = cost
            else:
                assert cost == base_cost
        guard = {"op": "eq", "args": [{"field": "polarization", "participant": 0}, 1]}
        for first, fires in ((1, True), (2, False)):
            lamps = [lamp((5, 7, 7), 5, 0, first), lamp((9, 7, 7), 5, 1, 3)]
            initial = parse_initial_state(document(lamps, rules=[meeting(when=guard)]))
            assert initial.ray_interactions[0].polarization_declared
            world = Simulation(initial)
            step(world, 3)
            if fires:
                assert inventory(world) == [
                    ((7, 6, 7), 3, 5, 1, 1, 3),
                    ((7, 8, 7), 2, 5, 1, 1, first),
                ]
            else:
                assert inventory(world) == [
                    ((6, 7, 7), 1, 5, 3, 1, 3),
                    ((8, 7, 7), 0, 5, 3, 1, first),
                ]
        return
    if case == "spread":
        # (e) Re-pinned under bit-law-v1 (2026-09-18): a lamp's light is a thing and
        # a thing moves whole on its line; only shadows spread, so the polarized
        # content crosses the board unsplit, its polarization its own, and nothing
        # reaches the transverse Nodes. (The axial mean of a spread's polarization
        # is the shadows' rule, unchanged.) Re-pinned 2026-09-18 (node-mixing-v1):
        # no table is declared, the spread of shadows being the Node's mixing.
        spreading = {"polarization_bits": 3}
        for lamps, expected in (
            ([lamp((4, 7, 7), 11, 0, 2)], {(6, 7, 7): (11, 2, 2, 1)}),
            (
                [lamp((4, 7, 7), 11, 0, 0), lamp((6, 7, 7), 11, 1, 4)],
                {(6, 7, 7): (11, 0, 2, 1), (4, 7, 7): (11, 4, 2, 2)},
            ),
            (
                [lamp((4, 7, 7), 11, 0, 0), lamp((6, 7, 7), 11, 1, 2)],
                {(6, 7, 7): (11, 0, 2, 1), (4, 7, 7): (11, 2, 2, 2)},
            ),
        ):
            world = Simulation(parse_initial_state(document(lamps, light=spreading)))
            step(world, 2)
            found = {
                position: [(ray.amount, ray.polarization, ray.steps, ray.event_ports) for ray in rays]
                for position, rays in (
                    (p, rays_at(world, p))
                    for p in ((6, 7, 7), (4, 7, 7), (5, 8, 7), (5, 6, 7), (5, 7, 8), (5, 7, 6))
                )
            }
            for position, entry in expected.items():
                assert found[position] == [entry], (lamps, position)
            for position in ((5, 8, 7), (5, 6, 7), (5, 7, 8), (5, 7, 6)):
                assert found[position] == [], (lamps, position)
            assert world.totals() == {"light": (11 * len(lamps),)}
        definition = SpatialFieldDefinition(
            0,
            (1,),
            transport="ray",
            headings=tuple(tuple(h) for h in HEADINGS),
            rays_per_tick=1,
            ray_slots=16,
            phase_bits=3,
            polarization_bits=3,
        )
        assert combined_polarization(((5, 2), (3, 2)), definition) == 2
        assert combined_polarization(((5, 0), (5, 4)), definition) == NONE
        assert combined_polarization(((5, 0), (5, 2)), definition) == 1
        assert combined_polarization(((5, NONE), (3, NONE)), definition) == NONE
        assert combined_polarization(((5, NONE), (3, 6)), definition) == 6
        assert combined_polarization((), definition) == NONE
        return
    if case == "identity":
        # (f) A world that declares the property nowhere runs the rule with its
        # defaults and records no identity; a family width alone records it.
        plain = document([lamp((4, 7, 7), 8, 0)], light={})
        plain["external_bodies"] = [{"position": [7, 7, 7], "family": "apparatus", "amount": 1}]
        plain["fields"].append(scalar("apparatus"))
        plain["spatial_fields"].append(ray_field("apparatus"))
        path = tmp_path / "plain.json"
        path.write_text(json.dumps(plain))
        run_initialization(path, tmp_path / "plain", ticks=6)
        metadata = json.loads((tmp_path / "plain" / "run.json").read_text(encoding="utf-8"))
        assert "ray_polarization" not in metadata
        assert "polarizer" not in metadata["external_bodies"][0]
        assert "held" not in metadata["external_bodies"][0]["final"]
        assert metadata["external_body_totals"] == {"light": [8], "apparatus": [0]}
        lines = (tmp_path / "plain" / "events.jsonl").read_text(encoding="utf-8")
        assert '"polarizer"' not in lines and "polarization" not in lines
        initial = parse_initial_state(plain)
        assert initial.spatial_fields[0].polarization_modulus == 8
        assert not initial.spatial_fields[0].polarization_declared
        path = tmp_path / "width.json"
        path.write_text(json.dumps(document([lamp((4, 7, 7), 8, 0)])))
        run_initialization(path, tmp_path / "width", ticks=2)
        metadata = json.loads((tmp_path / "width" / "run.json").read_text(encoding="utf-8"))
        assert metadata["ray_polarization"] == RAY_POLARIZATION_PROPERTY
        initial = parse_initial_state(document([lamp((4, 7, 7), 8, 0)], light={"polarization_bits": 1}))
        assert initial.spatial_fields[0].polarization_modulus == 2
        assert initial.spatial_fields[0].polarization_declared
        return
    # (g) The parser rejects a polarization outside the circle, a polarizer without
    # its declaration or its angle, a wrong table, and an assignment to the property.
    good = document([lamp((4, 7, 7), 8, 0, 0)], [polarizer_body(1)])
    for change, message in (
        (lambda raw: raw["emissions"][0].__setitem__("polarization", 8), "from 0 below 8"),
        (lambda raw: raw["emissions"][0].__setitem__("polarization", -2), "from 0 below 8"),
        (lambda raw: raw["external_bodies"][0]["polarizer"].pop("angle"), "requires an angle"),
        (lambda raw: raw["external_bodies"][0].pop("polarizer"), "requires its polarizer declaration"),
        (lambda raw: raw["external_bodies"][0]["polarizer"].__setitem__("angle", 8), "from 0 below 8"),
        (
            lambda raw: raw["external_bodies"][0]["polarizer"].__setitem__("table", TABLE[:7]),
            "one entry per step",
        ),
        (
            lambda raw: raw["external_bodies"][0]["polarizer"].__setitem__("table", [9] + TABLE[1:]),
            "from 0 through 8",
        ),
        (
            lambda raw: raw["external_bodies"][0]["polarizer"].__setitem__("pass", [1, 1, 0]),
            "unit-axial",
        ),
        (
            lambda raw: raw["external_bodies"][0]["polarizer"].__setitem__("unpolarized", 9),
            "from 0 through 8",
        ),
        (
            lambda raw: raw["external_bodies"][0]["polarizer"].__setitem__("family", "apparatus"),
            "other than its own",
        ),
        (lambda raw: raw["external_bodies"][0].__setitem__("coupling", "sink"), "requires coupling"),
        (
            lambda raw: raw["spatial_fields"][0].__setitem__("polarization_bits", -1),
            "polarization_bits must be an integer from 0",
        ),
    ):
        raw = json.loads(json.dumps(good))
        change(raw)
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
    lamps = [lamp((5, 7, 7), 5, 0, 1), lamp((9, 7, 7), 5, 1, 3)]
    for rule, message in (
        (meeting(({"of": 2}, None)), "exceeds the declared roles"),
        (meeting((8, None)), "from 0 below 8"),
        (meeting(("left", None)), "from 0 below 8"),
        (
            {
                "name": "swap",
                "participants": [{"type": "light"}, {"type": "light"}],
                "assignments": [
                    {
                        "participant": 0,
                        "field": "polarization",
                        "expression": {"field": "polarization", "participant": 1},
                    }
                ],
                "invariants": [
                    {
                        "name": "energy",
                        "expression": {
                            "op": "add",
                            "args": [
                                {"field": "amount", "participant": 0},
                                {"field": "amount", "participant": 1},
                            ],
                        },
                    }
                ],
            },
            "read-only",
        ),
    ):
        with pytest.raises(ValueError, match=message):
            parse_initial_state(document(lamps, rules=[rule]))
    outward = document([lamp((4, 7, 7), 8, 0)])
    outward["fields"].append(scalar("plain"))
    outward["spatial_fields"].append({"field": "plain", "transport": "outward", "polarization_bits": 3})
    with pytest.raises(ValueError, match="require ray transport"):
        parse_initial_state(outward)
    with pytest.raises(ValueError, match="below the family's polarization circle"):
        validate_rays(
            (emitted(0, 1, 8, 8),),
            parse_initial_state(document([lamp((4, 7, 7), 8, 0)])).spatial_fields[0],
            FieldDefinition("light", 1, "quantum", False, True),
        )
    with pytest.raises(ValueError, match="one entry per step"):
        Polarizer(1, 0, 0, tuple(TABLE[:7]), 4)
    with pytest.raises(ValueError, match="below its polarization circle"):
        Polarizer(1, 8, 0, tuple(TABLE), 4)
