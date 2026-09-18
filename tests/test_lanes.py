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
    phase_of_sum,
    ray_charge,
    validate_rays,
)
from event_universe.fields.rays import LaneClaims, merge_lane
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_node_is_ports import (
    MINUS_X,
    MINUS_Y,
    X,
    Y,
    document,
    event_kinds,
    family,
    field,
    lamp,
    line,
    parked_at,
    run,
    shadow,
)
from .test_node_is_ports import rays_at as node_rays_at
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
from .test_ray_polarization import document as pol_document
from .test_ray_polarization import lamp as pol_lamp

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


THING_A = ((9, 10, 10), "m", 8, 0)
THING_B = ((10, 11, 10), "m", 8, 3)
FROM_BELOW = ((10, 9, 10), "f", 1, 2)
CENTER = (10, 10, 10)


def test_a_thing_steps_into_a_lane_only_if_the_lane_is_free():
    # (d) A is pushed at C by the shadow from -Y; B is already on -Y and keeps
    # its lane; A keeps +X with its momentum accumulated and steps at the next
    # Node. Both move one Link every interval. Re-pinned on 2026-09-18 under
    # node-mixing-v1 on the geometry of test_ray_momentum_turn (a): one Link
    # from C each, so the shadow meets the things before it mixes anywhere.
    events = []
    raw = turn_document((THING_A, THING_B, FROM_BELOW), [turn({"f": -1})], 15)
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for t in range(1, 16):
        world.step()
        assert balanced(world)
        assert world.totals()["f"] == (1,) and world.escaped_totals()["f"] == (0,)
        assert world.totals()["m"] == ((16,) if t <= 11 else (8,) if t == 12 else (0,))
        current = momentum_line(world)
        if t == 1:
            # Both things and the shadow are at C together.
            assert turn_rays(world, CENTER, "m") == [ray(0, 8, 1, 1, 0), ray(3, 8, 1, 1, 3)]
            assert turn_rays(world, CENTER, "f") == [shadow_ray(2, 1, 1)]
            assert positions_of(world, "m") == {CENTER}
            assert world.thing_momentum() == {1: [8, 0, 0], 2: [0, -8, 0]}
            assert current["current"] == ZERO and current["spent"] == ZERO
            continue
        # The shadow, turned back at C, walks its one step to (10, 9, 10) and waits.
        assert positions_of(world, "f") == {(10, 9, 10)}
        assert turn_rays(world, (10, 9, 10), "f") == [shadow_ray(3, 1, 0, (0, 8, 0))]
        if t == 2:
            assert turn_rays(world, (11, 10, 10), "m") == [ray(0, 8, 2, 2, 0, momentum=(0, -8, 0))]
            assert turn_rays(world, (10, 9, 10), "m") == [ray(3, 8, 2, 2, 3)]
            assert positions_of(world, "m") == {(11, 10, 10), (10, 9, 10)}
            assert world.thing_momentum() == {1: [8, -8, 0], 2: [0, -8, 0]}
            assert current["current"] == ZERO and current["spent"] == ZERO
            assert current["escaped"] == ZERO
            continue
        a_at, b_at = (11, 12 - t, 10), (10, 11 - t, 10)
        assert positions_of(world, "m") == {at for at in (a_at, b_at) if at[1] >= 0}
        if t <= 12:
            assert turn_rays(world, a_at, "m") == [ray(3, 8, t & 7, t, 0)]
        if t <= 11:
            assert turn_rays(world, b_at, "m") == [ray(3, 8, t & 7, t, 3)]
        assert world.thing_momentum() == (
            {1: [0, -8, 0], 2: [0, -8, 0]} if t <= 11 else {1: [0, -8, 0]} if t == 12 else {}
        )
        assert current["spent"] == (8, 0, 0)
        assert current["escaped"] == (ZERO if t <= 11 else (0, -8, 0) if t == 12 else (0, -16, 0))
        assert current["current"] == ((-8, 0, 0) if t <= 11 else (-8, 8, 0) if t == 12 else (-8, 16, 0))
    assert pushes_of(events) == []
    # The control: alone, the thing steps at C in the cycle of tick 2.
    control = Simulation(parse_initial_state(turn_document((THING_A, FROM_BELOW), [turn({"f": -1})], 2)))
    for _ in range(2):
        control.step()
    assert turn_rays(control, (10, 9, 10), "m") == [ray(3, 8, 2, 2, 0)]
    assert momentum_line(control)["spent"] == (8, 0, 0)


def test_two_owners_shadows_share_a_lane_one_slot_each():
    # (e) Re-pinned on 2026-09-18 under node-mixing-v1: the two shadows that
    # have walked a Link mix at (3, 2, 2) in the cycle of tick 1, each sending
    # its whole quanta back through -X and parking the ninths; the fresh
    # shadow of owner 1 walks on to (4, 2, 2).
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
    # Two owners' shadows on the -X lane into (2, 2, 2): one slot each.
    back = node_lanes(result["rays"][0][(2, 2, 2)][0], definition)
    assert all(slot is None for slot in back.real)
    lane = lane_index(0, LANE_IN)
    assert (back.shadow[lane][0].amount, back.shadow[lane][0].steps) == (1, 1)
    assert (back.shadow[lane][1].amount, back.shadow[lane][1].steps) == (2, 1)
    assert sum(1 for entries in back.shadow for slot in entries if slot is not None) == 2
    assert back.parked == () and back.resident == ()
    # The parked ninths at (3, 2, 2) are outside the lanes: six per owner.
    parked = node_lanes(result["parked"][0][(3, 2, 2)][0], definition)
    assert sorted((r.owner, r.amount) for r in parked.parked) == [(1, 3)] * 6 + [(2, 6)] * 6
    assert all(slot is None for slot in parked.real)
    assert sum(1 for entries in parked.shadow for slot in entries if slot is not None) == 0
    # The fresh shadow of owner 1 on the +X lane into (4, 2, 2).
    on = node_lanes(result["rays"][0][(4, 2, 2)][0], definition)
    assert (on.shadow[lane_index(1, LANE_IN)][0].amount, on.shadow[lane_index(1, LANE_IN)][0].steps) == (
        2,
        1,
    )
    assert on.shadow[lane_index(1, LANE_IN)][1] is None


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


def _merged_definition():
    """The light family of test_ray_polarization: a coherence table of eight steps."""
    initial = parse_initial_state(pol_document([pol_lamp((4, 7, 7), 8, 0)]))
    return initial.spatial_fields[0], initial.fields[initial.spatial_fields[0].field]


def test_two_real_rays_of_one_family_on_one_lane_are_one_real_ray():
    # (g) The arithmetic of the merge (the model owner, 2026-09-18): amounts add,
    # the phase is the coherent sum's, the momentum adds exactly as the ledger
    # reads it, the owners are a set, everything else the passing thing's.
    definition, field_definition = _merged_definition()
    claims = LaneClaims()
    first = Ray(0, ZERO, 3, phase=0, steps=2, owner=1)
    second = Ray(0, ZERO, 4, phase=2, steps=1, owner=2)
    claims.claim(0, definition.field, first)
    claims.claim(0, definition.field, second)
    (merged,) = merge_lane((first, second), 0, claims, definition)
    assert merged == replace(first, amount=7, phase=1, owners=(2,))
    assert merged.phase == phase_of_sum(((3, 0), (4, 2)), definition) == 1
    passing = Ray(1, ZERO, 4, steps=3, owner=1)
    returned = Ray(
        1, ZERO, 1, steps=3, outbound=0, event_ports=1, event_shares=(1, 0, 0, 0, 0, 0), owner=2
    )
    claims = LaneClaims()
    claims.claim(1, definition.field, returned)
    claims.claim(1, definition.field, passing)
    (merged,) = merge_lane((returned, passing), 1, claims, definition)
    assert merged == replace(passing, amount=5, momentum=(2, 0, 0), owners=(2,))
    with pytest.raises(ValueError, match="point 25"):
        claims.claim(1, definition.field + 1, passing)
    with pytest.raises(ValueError, match="lanes-v1"):
        validate_rays((replace(first, owners=(1,)),), definition, field_definition)


def _merged_world():
    """P of 4 from +X and R of 1 from -X meet at the mark M, [1, 2] pass: P passes,
    R is returned onto P's lane, and the two are one thing of 5 walking -X. A
    shadow of each owner waits on its way, returned by a mark one Link up +Y."""
    kind_p, emission_p, seed_p = lamp("p", 4, (7, 2, 2), heading=MINUS_X)
    kind_r, emission_r, seed_r = lamp("r", 1, (1, 2, 2), heading=X)
    return document(
        ticks=8,
        shape=(8, 5, 5),
        types=[kind_p, kind_r],
        emissions=[emission_p, emission_r],
        seeds=[seed_p, seed_r],
        marks=[
            {"position": [4, 2, 2], "setting": [1, 2], "on_click": "pass"},
            {"position": [1, 3, 2], "setting": [1, 1]},
            {"position": [0, 3, 2], "setting": [1, 1]},
        ],
        shadows=[shadow((1, 2, 2), Y, owner=1, steps=0), shadow((0, 2, 2), Y, owner=2, steps=0)],
        # The engine alone: the dense region's read-back of a waiting shadow
        # does not keep its heading, which the re-release reads.
        dense=False,
    )


def _thing(heading, amount, steps, port, owner, outbound=1, owners=(), momentum=None):
    shares = tuple(amount if p == port else 0 for p in range(6))
    return Ray(
        heading,
        ZERO,
        amount,
        steps=steps,
        outbound=outbound,
        event_ports=1 << port,
        event_shares=shares,
        owner=owner,
        owners=owners,
        momentum=momentum,
    )


def _waiting(owner, steps=0):
    """A shadow returned by the mark up +Y, walking -Y (steps 1) or at rest (0)."""
    return Ray(3, ZERO, 1, steps=steps, outbound=0, detector=BIT_SHADOW, source_sign=-1, owner=owner)


def test_a_merged_thing_is_home_to_the_shadows_of_every_owner_it_carries():
    # (g) in the world and (h): the merged thing's books, charge and traces, and
    # a shadow of each owner coming home to it.
    doc = _merged_world()
    definition = parse_initial_state(deepcopy(doc)).spatial_fields[0]
    result = run(doc, 8)
    rays, parked = result["rays"], result["parked"]
    p_ray = lambda steps, amount=4, **extra: _thing(1, amount, steps, 1, 1, **extra)  # noqa: E731
    r_ray = lambda steps: _thing(0, 1, steps, 0, 2)  # noqa: E731
    for t in (1, 2):
        assert node_rays_at(rays[t - 1], (7 - t, 2, 2)) == (p_ray(t),)
        assert node_rays_at(rays[t - 1], (1 + t, 2, 2)) == (r_ray(t),)
    assert node_rays_at(rays[0], (1, 3, 2)) == (_waiting(1, 1),)
    assert node_rays_at(rays[0], (0, 3, 2)) == (_waiting(2, 1),)
    for t in range(2, 7):
        assert node_rays_at(rays[t - 1], (1, 2, 2))[-1:] == (_waiting(1),)
    for t in range(2, 8):
        assert node_rays_at(rays[t - 1], (0, 2, 2))[-1:] == (_waiting(2),)
    # After tick 3 both things are at M: P passed, R returned onto P's lane.
    assert set(node_rays_at(rays[2], (4, 2, 2))) == {p_ray(3), _thing(1, 1, 3, 0, 2, outbound=0)}
    # The passing thing's record (its event's shares of 4) with the amounts added.
    merged = replace(p_ray(4), amount=5, owners=(2,), momentum=(2, 0, 0))
    assert node_rays_at(rays[3], (3, 2, 2)) == (merged,)
    assert ray_charge((merged,), definition) == -5
    assert parked_at(parked[3], (4, 2, 2)) == [(MINUS_X, 0), (MINUS_X, 0)]
    assert sorted(r.owner for r in parked[3][(4, 2, 2)][0]) == [1, 2]
    for t in (5, 6, 7):
        assert node_rays_at(rays[t - 1], (7 - t, 2, 2))[0] == replace(merged, steps=t)
    # Home: owner 1's shadow at (1, 2, 2) in the cycle of tick 7, owner 2's at
    # (0, 2, 2) in the cycle of tick 8, each re-released +Y and returned again.
    assert node_rays_at(rays[6], (1, 3, 2)) == (_waiting(1, 1),)
    assert node_rays_at(rays[6], (1, 2, 2)) == ()
    assert node_rays_at(rays[7], (0, 3, 2)) == (_waiting(2, 1),)
    assert node_rays_at(rays[7], (0, 2, 2)) == ()
    assert node_rays_at(rays[7], (1, 2, 2)) == (_waiting(1),)
    assert result["contents"] == [5] * 7 + [0] and result["shadows"] == [2] * 8
    # A returned thing's momentum is read on its heading (-X after tick 3).
    assert result["momentum"] == [{1: [-4, 0, 0], 2: [1, 0, 0]}] * 2 + [
        {1: [-4, 0, 0], 2: [-1, 0, 0]}
    ] + [{1: [-3, 0, 0]}] * 4 + [{}]
    for t, ledger in enumerate(result["ledgers"], start=1):
        assert line(ledger, "real", "m")["current"] == ((5,) if t <= 7 else (0,))
        assert line(ledger, "real", "m")["escaped"] == ((0,) if t <= 7 else (5,))
        assert line(ledger, "shadow", "m") == {
            "initial": (2,),
            "current": (2,),
            "escaped": (0,),
            "absorbed_at_home": (0,),
        }
        assert ledger["fields"]["momentum"]["current"] == (ZERO if t <= 7 else (3, 0, 0))
        assert ledger["fields"]["momentum"]["escaped"] == (ZERO if t <= 7 else (-3, 0, 0))
        assert ledger["balanced"]
    kinds = event_kinds(result["events"])
    # P's pass at M is a click of bit 1 with nothing absorbed; R's return is one.
    assert kinds.get("detector_return") == 1 and kinds.get("detector_click") == 1
    assert "ray_push" not in kinds and result["marks"][0]["resident"]["real"] == {}


def test_two_real_families_on_one_lane_are_refused():
    # (i) A declared board with things of two families on one lane: a meeting
    # the table of the pair decides, which no departure holds.
    kind_m, emission_m, seed_m = lamp("e", 4, (1, 1, 1))
    kind_g, emission_g, seed_g = lamp("w", 4, (1, 1, 1), family_name="g")

    def build(seed_g):
        doc = document(
            ticks=1,
            shape=(7, 3, 3),
            types=[kind_m, kind_g],
            emissions=[emission_m, emission_g],
            seeds=[seed_m, seed_g],
            families=[family(), family("g", charge=0)],
        )
        doc["fields"] = [field("m"), field("g"), field("momentum", 3)]
        return doc

    with pytest.raises(ValueError, match="point 25") as caught:
        parse_initial_state(build(seed_g))
    assert "'m'" in str(caught.value) and "'g'" in str(caught.value)
    assert "'e'" in str(caught.value) and "'w'" in str(caught.value)
    parse_initial_state(build({"position": [1, 2, 2], "type": "w"}))
    # At a departure, a real of another family on a taken lane is refused.
    definition, _ = _merged_definition()
    claims = LaneClaims()
    claims.claim(0, definition.field, Ray(0, ZERO, 3, steps=2, owner=1))
    with pytest.raises(ValueError, match="different families"):
        claims.claim(0, definition.field + 1, Ray(0, ZERO, 3, steps=2, owner=2))
