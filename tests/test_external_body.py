"""The external body (external-body-v1, Highlights 3.19): a declared Node holding a
family with an amount of any width, meeting whatever arrives by its declared
coupling, the explicitly accounted sink by default, a declared meeting with
outputs otherwise (a mirror); moved by fields only, its momentum an exact
accumulator per axis that steps one Link when a whole amount has accumulated.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("External body")
before the first run: sink, uniform and mirror.

Re-pinned on 2026-09-18 under the law of the bit (bit-law-v1): a body radiates
nothing per interval (its shadows are given with the board, test_bit_law.py),
so the `sink` world has no field of the star: the electron sent at the star
ends in its sink with its momentum, the light passes untouched, nothing is
sourced; the `stars` case (three stars in each other's per-tick field) went
with the law, its physics being that of the shadows of test_bit_law.py (b);
a body's record names no `field`; a body's momentum table needs `reads`.
"""

import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    EXTERNAL_BODY,
    Ray,
    ray_merge_key,
    ray_momentum,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# A mirror: the arriving light ray leaves reversed on its own line, unchanged, and
# the body, the participant that never changes, is returned as it came.
MIRROR = {
    "name": "mirror",
    "participants": [{"type": "light"}, {"type": "star"}],
    "outputs": [
        {"field": "light", "amount": {"of": 0}, "heading": "reversed", "input": 0, "phase": {"of": 0}},
        {"field": "star", "amount": {"of": 1}, "heading": "same", "input": 1, "phase": {"of": 1}},
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


def ray_field(name, advance, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 16,
        "metric": "links",
        "pace": [1, 1],
        "kerengonen": {"phase_steps": 8},
        # The clock is the content (clock-readings-v1, 2026-09-18): the electron
        # lamp's ray of 3 advances one step per interval at K 3.
        **({"clock": True} if advance else {}),
    } | extra


def document(bodies, lamps=(), rules=(), families=("star",), ticks=6):
    """The board: `lamps` are (position, family, amount, heading index)."""
    names = sorted(set(families) | {family for _, family, _, _ in lamps})
    return {
        "schema_version": 1,
        "model_id": "external-body-test-v1",
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
        "fields": [field(name) for name in names],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": [family],
                "defaults": {family: amount},
                "transport": {"mode": "hold"},
            }
            for index, (_, family, amount, _) in enumerate(lamps)
        ]
        # A world of bodies alone still declares one (unseeded) disturbance type.
        or [
            {"name": "idle", "fields": ["star"], "defaults": {"star": 0}, "transport": {"mode": "hold"}}
        ],
        "spatial_fields": [ray_field(name, 1 if name == "electron" else 0) for name in names],
        "K": 3,
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
        "external_bodies": list(bodies),
    }


def rays_at(world, position, family):
    """The resident rays of one family at a Node, in merge-key order."""
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    # bit-law-v1 (2026-09-18): a ray carries the identity of the thing that emitted
    # it (`owner`); this module pins lines and events, not identities (test_bit_law does).
    rays = node.rays[index] if node is not None and node.rays else ()
    return sorted((replace(ray, owner=0) for ray in rays), key=ray_merge_key)


def positions_of(world, family):
    return {n.position for n in world.inventory_view().nodes if rays_at(world, n.position, family)}


def momentum_of(world, family):
    """The momentum of every resident ray of one family: amount x heading, summed."""
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    definition = world.initial.spatial_fields[index]
    total = [0, 0, 0]
    for node in world.inventory_view().nodes:
        if node.rays:
            for axis, value in enumerate(ray_momentum(node.rays[index], definition)):
                total[axis] += value
    return tuple(total)


def emitted(heading, steps, phase, amount):
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


def released(heading, steps, amount):
    """A body's field ray: no event, phase 0."""
    return Ray(heading, (0, 0, 0), amount, steps=steps)


def product(heading, amount, steps, mask, shares):
    return Ray(heading, (0, 0, 0), amount, steps=steps, event_ports=mask, event_shares=shares)


def body_at(world, index):
    return next(item for item in world.external_bodies() if item["index"] == index)


def at(position, heading, distance):
    return tuple((p + distance * h) % 15 for p, h in zip(position, HEADINGS[heading], strict=True))


STAR = (7, 7, 7)
SINK_BODY = {"position": [7, 7, 7], "family": "star", "amount": 4096}
SINK_LAMPS = (((8, 5, 7), "light", 5, 2), ((7, 7, 4), "electron", 3, 4))
UNIFORM_BODY = {
    "position": [3, 7, 7],
    "family": "star",
    "amount": 6,
    "initial_momentum": {"heading": [0, 1, 0], "pace": [1, 2]},
}
MIRROR_BODY = {"position": [7, 7, 7], "family": "star", "amount": 4, "coupling": "mirror"}


@pytest.mark.parametrize("case", ["sink", "uniform", "mirror", "rejected"])
def test_an_external_body_radiates_absorbs_reflects_and_moves_by_fields_only(tmp_path, case):
    events = []
    if case == "rejected":
        # (e) Malformed bodies are rejected at initialization.
        for bodies, extra, message in (
            (({"position": [7, 7, 7], "family": "star", "amount": 0},), {}, "positive integer"),
            (
                ({"position": [7, 7, 7], "family": "star", "amount": 1, "coupling": "turn"},),
                {},
                "sink or a declared",
            ),
            (
                ({"position": [7, 7, 7], "family": "star", "amount": 1, "momentum_table": {"star": 2}},),
                {},
                "attraction",
            ),
            (
                (
                    {"position": [7, 7, 7], "family": "star", "amount": 1},
                    {"position": [7, 7, 7], "family": "star", "amount": 1},
                ),
                {},
                "one external body",
            ),
            (
                ({"position": [7, 7, 7], "family": "star", "amount": 4, "coupling": "mirror"},),
                {"rules": [], "families": ("star", "light")},
                "sink or a declared",
            ),
        ):
            with pytest.raises(ValueError, match=message):
                parse_initial_state(document(bodies, **extra))
        # A table without `reads` is rejected (bit-law-v1, point 16).
        with pytest.raises(ValueError, match="point 16"):
            parse_initial_state(
                document(
                    (
                        {
                            "position": [7, 7, 7],
                            "family": "star",
                            "amount": 1,
                            "momentum_table": {"star": 1},
                        },
                    )
                )
            )
        with pytest.raises(ValueError, match="one Link per interval"):
            parse_initial_state(
                document((UNIFORM_BODY | {"initial_momentum": {"heading": [0, 1, 0], "pace": [3, 2]}},))
            )
        return
    if case == "sink":
        # (a) A star at rest: light passing one Node away walks on untouched (no
        # field is released), an electron sent at the star ends in the sink, and
        # the star, moved by fields only, stays at rest: no thing pushes it.
        initial = parse_initial_state(document((SINK_BODY,), SINK_LAMPS))
        world = Simulation(initial, observer=events.append)
        for n in range(1, 7):
            world.step()
            sunk = n >= 3
            assert world.totals() == {"electron": (0 if sunk else 3,), "light": (5,), "star": (0,)}
            assert world.source_totals() == {"electron": (0,), "light": (0,), "star": (0,)}
            assert world.external_body_totals() == {
                "electron": (3 if sunk else 0,),
                "light": (0,),
                "star": (0,),
            }
            assert all(item["balanced"] for item in world.spatial_accounting().values())
            assert world.external_bodies() == [
                {
                    "index": 0,
                    "position": [7, 7, 7],
                    "stepping": False,
                    "momentum": [0, 0, 0],
                    "accumulators": [0, 0, 0],
                    "sink": {"electron": 3} if sunk else {},
                }
            ]
            assert world.external_body_momentum() == (0, 0, 0)
            assert rays_at(world, at((8, 5, 7), 2, n), "light") == [emitted(2, n, 0, 5)]
            if n <= 2:
                assert rays_at(world, (7, 7, 4 + n), "electron") == [emitted(4, n, n, 3)]
            else:
                assert positions_of(world, "electron") == set()
            assert rays_at(world, STAR, "electron") == []
        absorbed = [e for e in events if e["event"] == "external_body_absorbed"]
        assert [(e["tick"], e["family"], e["amount"], e["momentum"]) for e in absorbed] == [
            (3, "electron", 3, (0, 0, 0)),
        ]
        assert not any(e["event"] == "external_body_step" for e in events)
        path = tmp_path / "sink.json"
        path.write_text(json.dumps(document((SINK_BODY,), SINK_LAMPS)))
        run_initialization(path, tmp_path / "out", ticks=6)
        metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
        assert metadata["external_body"] == EXTERNAL_BODY == "external-body-v1"
        assert metadata["external_body_totals"] == {"electron": [3], "light": [0], "star": [0]}
        assert metadata["external_body_momentum"] == [0, 0, 0]
        assert metadata["accounting_balanced_at_every_completed_tick"]
        assert metadata["final_totals"] == {"electron": [0], "light": [5], "star": [0]}
        body = metadata["external_bodies"][0]
        assert (body["family"], body["amount"], body["coupling"]) == ("star", 4096, "sink")
        assert "field" not in body
        assert body["positions"] == [[tick, 7, 7, 7] for tick in range(7)]
        assert body["final"]["momentum"] == [0, 0, 0] and body["final"]["accumulators"] == [0, 0, 0]
        return
    if case == "uniform":
        # (c) A body with an initial momentum and no field around it moves uniformly:
        # amount 6 at pace 1/2 along +Y is momentum 3, one Link every two intervals.
        initial = parse_initial_state(document((UNIFORM_BODY,)))
        world = Simulation(initial, observer=events.append)
        for n in range(1, 7):
            world.step()
            assert world.totals() == {"star": (0,)} and world.source_totals() == {"star": (0,)}
            assert world.external_bodies() == [
                {
                    "index": 0,
                    "position": [3, 7 + n // 2, 7],
                    "stepping": False,
                    "momentum": [0, 3, 0],
                    "accumulators": [0, 3 * (n % 2), 0],
                    "sink": {},
                }
            ]
        steps = [
            (e["tick"], e["port"], e["arrival_tick"])
            for e in events
            if e["event"] == "external_body_step"
        ]
        assert steps == [(1, 2, 2), (3, 2, 4), (5, 2, 6)]
        return
    # (d) A mirror body: the arriving light ray is sent back on its line unchanged,
    # a new event at the body's Node whose record counts the body as one quantum on
    # +X; the body is unchanged and its sink stays empty.
    initial = parse_initial_state(
        document((MIRROR_BODY,), (((7, 7, 3), "light", 5, 4),), [MIRROR], ticks=7)
    )
    world = Simulation(initial, observer=events.append)
    for n in range(1, 8):
        world.step()
        assert world.totals() == {"light": (5,), "star": (0,)}
        assert world.source_totals() == {"light": (0,), "star": (0,)}
        assert world.external_body_totals() == {"light": (0,), "star": (0,)}
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        assert world.external_bodies() == [
            {
                "index": 0,
                "position": [7, 7, 7],
                "stepping": False,
                "momentum": [0, 0, 0],
                "accumulators": [0, 0, 0],
                "sink": {},
            }
        ]
        if n <= 4:
            assert rays_at(world, (7, 7, 3 + n), "light") == [emitted(4, n, 0, 5)]
        else:
            assert rays_at(world, (7, 7, 11 - n), "light") == [
                product(5, 5, n - 4, 33, (1, 0, 0, 0, 0, 5))
            ]
        assert positions_of(world, "star") == set()
        assert len(positions_of(world, "light")) == 1
    assert not any(e["event"] in ("external_body_absorbed", "external_body_step") for e in events)
