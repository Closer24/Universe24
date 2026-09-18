"""A Port is two lanes (lanes-v1; Highlights 5.4 point 25, the model owner's
decision of 2026-09-18; feature 18 of issue #169).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A Port is two
lanes") before the first run. A Node's state is twelve lanes, one real slot and
one shadow slot per owner on each, addressable as [Port][lane][real |
shadow(owner)] beside the parked shadows and the rays at rest (a); a declared
board with two reals on one lane is refused, as is a sweep that repeats a
heading (b); a table with two outputs on one heading is refused (c); the lane
is a condition on the step: the thing already on the heading keeps it, the
other continues on its own heading with its momentum kept and steps at the
next Node, both one Link per interval, the books exact (d); two owners'
shadows share a lane in one slot each, the sums exact (e); the record of a
world with no contested lane is byte-identical (f).
"""

import hashlib
import json
from copy import deepcopy
from dataclasses import replace
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    LANE_IN,
    LANE_OUT,
    LANES,
    NODE_LANES,
    Ray,
    lane_index,
    node_lanes,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_node_is_ports import MINUS_X, MINUS_Y, X, Y, document, family, lamp, line, run, shadow
from .test_ray_momentum_turn import (
    balanced,
    momentum_line,
    positions_of,
    pushes_of,
    ray,
    shadow_ray,
    turn,
)
from .test_ray_momentum_turn import document as turn_document
from .test_ray_momentum_turn import rays_at as turn_rays

ROOT = Path(__file__).resolve().parents[1]
ZERO = (0, 0, 0)


def test_a_node_is_twelve_lanes_of_one_real_and_one_shadow_per_owner():
    # (a) The owner axis is fixed at parsing: the lamp (thing 1) and the owner
    # of the profile shadow (2).
    kind, emission, seed = lamp("e", 4, (2, 1, 1))
    doc = document(
        ticks=1,
        shape=(7, 3, 3),
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        shadows=[shadow((1, 1, 1), MINUS_X, owner=2, steps=1)],
    )
    definition = parse_initial_state(doc).spatial_fields[0]
    assert definition.owners == (1, 2)
    thing = Ray(0, ZERO, 4, steps=1, event_ports=1, event_shares=(4, 0, 0, 0, 0, 0), owner=1)
    first = Ray(0, ZERO, 3, steps=1, detector=BIT_SHADOW, source_sign=-1, owner=1)
    second = Ray(3, ZERO, 5, steps=1, detector=BIT_SHADOW, source_sign=-1, owner=2)
    trace = Ray(0, ZERO, 0, detector=BIT_SHADOW, owner=1, parked=1)
    returned = Ray(1, ZERO, 4, outbound=0, event_ports=1, event_shares=(4, 0, 0, 0, 0, 0), owner=1)
    slots = node_lanes((thing, first, second, trace, returned), definition)
    assert NODE_LANES == 12 and len(slots.real) == 12 and len(slots.shadow) == 12
    assert all(len(lane) == 2 for lane in slots.shadow)
    assert (lane_index(0, LANE_IN), lane_index(0, LANE_OUT), lane_index(5, LANE_OUT)) == (0, 1, 11)
    # The thing on +X entered through Port 1 (-X): the real slot of lane 2.
    assert slots.real[lane_index(1, LANE_IN)] == thing
    assert [index for index, slot in enumerate(slots.real) if slot is not None] == [2]
    # One shadow slot per owner on every lane: owner 1 on lane 2, owner 2 on
    # lane 4 (its -Y shadow entered through Port 2, +Y).
    assert slots.shadow[2][0] == first and slots.shadow[4][1] == second
    assert sum(1 for lane in slots.shadow for slot in lane if slot is not None) == 2
    assert slots.parked == (trace,) and slots.resident == (returned,)
    with pytest.raises(ValueError, match="point 25"):
        node_lanes((thing, replace(thing, steps=2)), definition)
    with pytest.raises(ValueError):
        lane_index(6, LANE_IN)


def test_two_real_rays_declared_on_one_lane_are_refused():
    # (b) Two lamps at one Node emitting on one heading.
    kind, emission, seed = lamp("e", 4, (1, 1, 1))
    kind2, emission2, seed2 = lamp("e2", 4, (1, 1, 1))
    with pytest.raises(ValueError, match="point 25") as caught:
        parse_initial_state(
            document(
                ticks=1,
                shape=(7, 3, 3),
                types=[kind, kind2],
                emissions=[emission, emission2],
                seeds=[seed, seed2],
            )
        )
    assert "'e'" in str(caught.value) and "'e2'" in str(caught.value)
    kind2, emission2, seed2 = lamp("e2", 4, (1, 2, 2))
    parse_initial_state(
        document(
            ticks=1,
            shape=(7, 3, 3),
            types=[kind, kind2],
            emissions=[emission, emission2],
            seeds=[seed, seed2],
        )
    )
    # A sweep that repeats a heading.
    swept = family()
    swept["headings"] = [X, X, MINUS_X, Y, MINUS_Y, [0, 0, 1], [0, 0, -1]]
    swept["rays_per_tick"] = 2
    with pytest.raises(ValueError, match="point 25"):
        parse_initial_state(document(ticks=1, families=[swept]))
    swept["rays_per_tick"] = 1
    parse_initial_state(document(ticks=1, families=[swept]))


def _rule(outputs):
    return {
        "name": "meet",
        "participants": [{"type": "m"}, {"type": "m"}],
        "outputs": outputs,
        "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
    }


def _output(heading, source):
    return {
        "field": "m",
        "amount": {"of": source},
        "heading": heading,
        "input": source,
        "phase": {"of": source},
    }


def test_a_table_with_two_outputs_on_one_heading_is_refused():
    # (c)
    kind, emission, seed = lamp("e", 4, (1, 1, 1))

    def parse(outputs):
        return parse_initial_state(
            document(ticks=1, types=[kind], emissions=[emission], seeds=[seed], rules=[_rule(outputs)])
        )

    with pytest.raises(ValueError, match="point 25") as caught:
        parse([_output("reversed", 1), _output("reversed", 1)])
    assert "outputs 0 and 1" in str(caught.value)
    with pytest.raises(ValueError, match="point 25"):
        parse([_output(0, 0), _output(0, 1)])
    parse([_output("same", 0), _output("reversed", 1)])


THING_A = ((4, 10, 10), "m", 8, 0)
THING_B = ((10, 16, 10), "m", 8, 3)
FROM_BELOW = ((10, 4, 10), "f", 1, 2)


def test_a_thing_steps_into_a_lane_only_if_the_lane_is_free():
    # (d) A is pushed at C by the shadow from -Y; B is already on -Y and keeps
    # its lane; A keeps +X with its momentum accumulated and steps at the next
    # Node. Both move one Link every interval.
    events = []
    raw = turn_document((THING_A, THING_B, FROM_BELOW), [turn({"f": -1})], 20)
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for t in range(1, 21):
        world.step()
        assert balanced(world)
        assert world.totals()["f"] == (1,) and world.escaped_totals()["f"] == (0,)
        assert world.totals()["m"] == ((16,) if t <= 16 else (8,) if t == 17 else (0,))
        current = momentum_line(world)
        if t <= 6:
            # After tick 6 both things and the shadow are at C together.
            at_a, at_b = (4 + t, 10, 10), (10, 16 - t, 10)
            expected = {at_a: [ray(0, 8, t & 7, t, 0)], at_b: [ray(3, 8, t & 7, t, 3)]}
            if t == 6:
                expected = {at_a: [ray(0, 8, 6, 6, 0), ray(3, 8, 6, 6, 3)]}
            assert {at: turn_rays(world, at, "m") for at in expected} == expected
            assert positions_of(world, "m") == set(expected)
            assert turn_rays(world, (10, 4 + t, 10), "f") == [shadow_ray(2, 1, t)]
            assert world.thing_momentum() == {1: [8, 0, 0], 2: [0, -8, 0]}
            assert current["current"] == ZERO and current["spent"] == ZERO
            continue
        # The shadow, turned back at C, walks -Y to (10, 4, 10) and waits there.
        assert turn_rays(world, (10, max(16 - t, 4), 10), "f") == [
            shadow_ray(3, 1, max(12 - t, 0), (0, 8, 0))
        ]
        if t == 7:
            assert turn_rays(world, (11, 10, 10), "m") == [ray(0, 8, 7, 7, 0, momentum=(0, -8, 0))]
            assert turn_rays(world, (10, 9, 10), "m") == [ray(3, 8, 7, 7, 3)]
            assert positions_of(world, "m") == {(11, 10, 10), (10, 9, 10)}
            assert world.thing_momentum() == {1: [8, -8, 0], 2: [0, -8, 0]}
            assert current["current"] == ZERO and current["spent"] == ZERO
            assert current["escaped"] == ZERO
            continue
        a_at, b_at = (11, 17 - t, 10), (10, 16 - t, 10)
        assert positions_of(world, "m") == {at for at in (a_at, b_at) if at[1] >= 0}
        if t <= 17:
            assert turn_rays(world, a_at, "m") == [ray(3, 8, t & 7, t, 0)]
        if t <= 16:
            assert turn_rays(world, b_at, "m") == [ray(3, 8, t & 7, t, 3)]
        assert world.thing_momentum() == (
            {1: [0, -8, 0], 2: [0, -8, 0]} if t <= 16 else {1: [0, -8, 0]} if t == 17 else {}
        )
        assert current["spent"] == (8, 0, 0)
        assert current["escaped"] == (ZERO if t <= 16 else (0, -8, 0) if t == 17 else (0, -16, 0))
        assert current["current"] == ((-8, 0, 0) if t <= 16 else (-8, 8, 0) if t == 17 else (-8, 16, 0))
    assert pushes_of(events) == []
    # The control: alone, the thing steps at C in the cycle of tick 7.
    control = Simulation(parse_initial_state(turn_document((THING_A, FROM_BELOW), [turn({"f": -1})], 7)))
    for _ in range(7):
        control.step()
    assert turn_rays(control, (10, 9, 10), "m") == [ray(3, 8, 7, 7, 0)]
    assert momentum_line(control)["spent"] == (8, 0, 0)


def test_two_owners_shadows_share_a_lane_one_slot_each():
    # (e)
    kind1, emission1, seed1 = lamp("e1", 0, (1, 2, 2))
    kind2, emission2, seed2 = lamp("e2", 0, (1, 3, 3))
    doc = document(
        ticks=1,
        shape=(8, 5, 5),
        types=[kind1, kind2],
        emissions=[emission1, emission2],
        seeds=[seed1, seed2],
        shadows=[
            shadow((3, 2, 2), X, amount=3, owner=1, steps=1),
            shadow((3, 2, 2), X, amount=2, owner=1, steps=0),
            shadow((3, 2, 2), X, amount=6, owner=2, steps=1),
        ],
    )
    definition = parse_initial_state(deepcopy(doc)).spatial_fields[0]
    assert definition.owners == (1, 2)
    result = run(doc, 1)
    assert result["contents"] == [0] and result["shadows"] == [11]
    assert line(result["ledgers"][0], "shadow", "m") == {
        "initial": (11,),
        "current": (11,),
        "escaped": (0,),
        "absorbed_at_home": (0,),
    }
    rays = result["rays"][0][(4, 2, 2)][0]
    assert sorted((r.owner, r.amount, r.steps) for r in rays) == [(1, 2, 1), (1, 3, 2), (2, 6, 2)]
    slots = node_lanes(rays, definition)
    assert all(slot is None for slot in slots.real)
    lane = lane_index(1, LANE_IN)
    assert (slots.shadow[lane][0].amount, slots.shadow[lane][0].steps) == (5, 1)
    assert (slots.shadow[lane][1].amount, slots.shadow[lane][1].steps) == (6, 2)
    assert sum(1 for entries in slots.shadow for slot in entries if slot is not None) == 2
    assert slots.parked == () and slots.resident == ()


def test_the_record_of_a_world_with_no_contested_lane_is_unchanged(tmp_path):
    # (f) Computed on origin/main at 3cfb5e4 before the change.
    out = tmp_path / "ring"
    run_initialization(ROOT / "examples/nature/ring.json", out, ticks=8)
    digests = {
        name: hashlib.sha256((out / name).read_bytes()).hexdigest()
        for name in ("events.jsonl", "state.json")
    }
    assert digests == {
        "events.jsonl": "091f6666d75ec307bf5d13f3f82123fab34c1d68524bade9b59d9fdbdcf20420",
        "state.json": "3de44da77e91431f4208f648d747b6a84665e7aad74e03a18f9cf406bf201afa",
    }
    metadata = json.loads((out / "run.json").read_text(encoding="utf-8"))
    assert metadata["lanes"] == LANES == "lanes-v1"
    assert metadata["node_is_ports"] == "node-is-ports-v1"
