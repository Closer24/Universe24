"""The law of the bit (bit-law-v1; Highlights 5.4, the model owner's decision of
2026-09-18, with the amendments of that day).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The law of the bit")
before the first run. Every ray carries one bit, 1 a thing and 0 its shadow, a ray
of the same family: a shadow pushes a thing it meets and walks home with -dp,
home to a body (a) and to a thing ray (c); a thing's own shadow pushes it and
its return of zero steps undoes it in the same cycle, the two halves booked (c');
two bodies push each other through their shadows and take the -dp back (b); a
mark returns a shadow and counts nothing, and catches things by its counter
table, no lottery (d); a shadow-only board makes no event and the dense layer
equals the engine (e); the field given with the board is exact (f); the retired
declarations are rejected (g); the mark is the home of what it absorbed (h);
the ledger per bit with the border lines (i); a thing reads the shadows'
message by its content or by its charge, as declared (j).

Re-pinned on 2026-09-18 under clock-readings-v1 (feature 16b, Highlights 5.4
points 16, 18, 19 and 21): a family declares no rest rate, `m` declares
`clock` and the world `K` (world (a): K 2, so a thing of 2 advances one step
per interval as before); the electricity reading multiplies by the owner's
whole charge over its content, so a body of 100 quanta of `m` declares the
whole charge -100 and pushes as it did at -1 per quantum; a thing's `momentum` is the
pushes it carries, its register line amount x heading plus that; the momentum
line carries `spent`.

Re-pinned on 2026-09-18 under node-is-ports-v1 (feature 17, Highlights 5.4
point 22 and the settled rules): a lamp is a thing that spends its content
(no `source`, no `recoil_field`), a prefilled shadow starts with its Link
distance from its owner's Node as its steps (rule (ii)), the mark's counter is
a thing resident at it (`resident`) whose shadows line counts a shadow home
without an event (rule (iv)), the trace is a zero-amount parked shadow, the
runner's per-tick line is `momentum`, the ledgers per bit read initial +
converted = current + escaped + absorbed (things) and initial = current +
escaped + absorbed_at_home (shadows), and `seed` is rejected.

Re-pinned on 2026-09-18 under the Node's mixing (node-mixing-v1, Highlights
5.4 point 24, feature 16c): these worlds declared no split table, so their
shadows walked straight to what they were to meet; under point 24 every shadow
of a family with a shadow set mixes at every Node it reaches with nothing else
there (a lone quantum parks its ninths and goes nowhere), so a shadow that is
to meet a thing, a body or a mark now leaves fresh (`steps` 0) from the Node
beside it and arrives there in the first delivery, and what returns walks its
one step back and waits (rule (ii)). The subjects are the same; the geometry
is adjacent and the ticks earlier: (a) the body one Link past the push, (b)
the two bodies adjacent and pushing each other every tick, (c) the homecoming
at tick 1, (d) the returned shadow waiting at steps 0, (e) and (k) the
mixing's amounts (4 back, 1 each other way from 11; the rest parked in
ninths), (f) the fill's transient by the mixing, (h) the marks adjacent, (i)
the escape and the return at the first delivery, (j) the shadows one Link
ahead of the things.

Re-pinned on 2026-09-18 under the return as a field (return-field-v1, feature
16d, Highlights 5.4 point 3 as amended): a shadow that pushes turns back with
the opposite sign, the same shadow reversed with its flow inverted (`outbound`
0) and -dp on it, and from then on it is a field like any other: it mixes at
the next Node (a lone quantum parks its ninths with the momentum it carries),
pushes whatever other thing it meets with the opposite sign and is home
wherever it reaches its owner; a mark returns a shadow as it is, no flip; no
trace is left at any Node and no shadow waits. (a) the body's shadow home at
the first delivery as before, no trace beside its ninths; (d) the returned
shadow parks at (5,2,2) from tick 3; (h) the re-released shadow reaches the
mark with the thing and is returned before the thing is resident, then parks
at (3,2,2); (j) the head-on push is taken once: the inverted shadow rides one
Link with the thing it pushed on the same lane (one meeting, one push: it
arrives through the Port the thing arrived by and pushes nothing there),
mixes at (3,y,2) and parks its ninths with -dp.
"""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import BIT_SHADOW, BIT_THING
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
COSTS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
X = [1, 0, 0]
MINUS_X = [-1, 0, 0]


def field(name, components=1):
    return {
        "name": name,
        "components": components,
        "units": "quantum",
        "signed": components == 3,
        "conserved": True,
        "extensive": True,
    }


def family(spread=None, clock=False):
    entry = {
        "field": "m",
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 8,
        "metric": "links",
        "pace": [1, 1],
        "charge": -1,
        "release": [1, 1],
    }
    if clock:
        entry["clock"] = True
    if spread is not None:
        entry["spread"] = spread
    return entry


def lamp(name, amount, position, heading=X):
    kind = {
        "name": name,
        "fields": ["m", "momentum"],
        "defaults": {"m": amount, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    emission = {
        "type": name,
        "field": "m",
        "amount": amount,
        "denominator": 1,
        "heading": heading,
        "kerengonen_phase": 0,
    }
    seed = {"position": list(position), "type": name}
    return kind, emission, seed


RING = {
    "name": "ring",
    "fields": ["m", "momentum"],
    "defaults": {"m": 4, "momentum": [0, 0, 0]},
    "transport": {"mode": "hold"},
}
TURN = {
    "name": "turn",
    "participants": [{"type": "m"}, {"type": "m"}],
    "momentum_table": {"m": 1},
    "reads": "charge",
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
}


def shadow(position, heading, amount=1, owner=1, sign=-1, steps=None):
    """A profile shadow; its sign is its owner's charge sign (-1 here, the
    family's charge and the bodies' charge are -1); `steps` 0 is a fresh shadow
    leaving at the first tick, None the default (its Link distance from its
    owner's Node, rule (ii))."""
    entry = {
        "position": list(position),
        "heading": list(heading),
        "amount": amount,
        "owner": owner,
        "sign": sign,
    }
    if steps is not None:
        entry["steps"] = steps
    return entry


def body(position, thing=None, table=None, amount=100):
    """A body of `amount` quanta of `m` with the whole charge -amount, the
    family's -1 per quantum (clock-readings-v1: its shadows carry its whole
    charge and its content, and the electricity reading divides the one by the
    other)."""
    entry = {"position": list(position), "family": "m", "amount": amount, "charge": -amount}
    if table is not None:
        entry["momentum_table"] = table
        entry["reads"] = "charge"
    if thing is not None:
        entry["thing"] = thing
    return entry


def document(
    *,
    ticks,
    types=(),
    emissions=(),
    seeds=(),
    bodies=(),
    marks=(),
    shadows=(),
    spread=None,
    fill=None,
    phase_bits=0,
    clock=0,
    dense=None,
    rules=(TURN,),
):
    doc = {
        "schema_version": 1,
        "model_id": "bit-law-test-v1",
        "shape": [10, 5, 5],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(COSTS, 1),
        "fields": [field("m"), field("momentum", 3)],
        "disturbance_types": list(types) or [RING],
        "spatial_fields": [family(spread, bool(clock))],
        **({"K": clock} if clock else {}),
        # One N for the world (the cleanup of 2026-09-18): the width these worlds
        # declared per family, or the default 64 where they declared none.
        **({"N": 1 << phase_bits} if phase_bits else {}),
        # The wait per whole quantum read (Highlights 5.4 point 23) is pinned in
        # tests/test_wait_rule.py; these worlds pin the pushes without it.
        "wait_per_quantum": 0,
        "emissions": list(emissions),
        "seeds": list(seeds),
        "ray_interactions": [deepcopy(rule) for rule in rules],
        "external_bodies": list(bodies),
        "detectors": list(marks),
    }
    if shadows:
        doc["initial_field"] = {"m": {"rays": list(shadows)}}
    if fill is not None:
        doc["initial_field"] = {"m": {"fill": fill}}
    if dense is not None:
        doc["dense_field"] = dense
    return doc


def run(doc, ticks):
    """The world through the Simulation API: per tick the ledger, the events, the
    things' and the shadows' content, the shadows per thing and the momentum of
    every thing, then the final inventory."""
    events = []
    ledgers, contents, shadows, counts, inventories = [], [], [], [], []
    momentum, bodies_per_tick = [], []
    with Simulation(parse_initial_state(doc), observer=events.append) as world:
        for _ in range(ticks):
            world.step()
            ledgers.append(world.audit())
            contents.append(world.real_content())
            shadows.append(world.shadow_content())
            counts.append(world.shadow_counts())
            momentum.append(world.thing_momentum())
            bodies_per_tick.append([b["momentum"] for b in world.external_bodies()])
            inventories.append(
                {node.position: node.rays for node in world.inventory_view().nodes if any(node.rays)}
            )
        bodies = world.external_bodies()
        marks = world.detector_marks()
        snapshot = world.snapshot()
    return {
        "events": events,
        "ledgers": ledgers,
        "contents": contents,
        "shadows": shadows,
        "counts": counts,
        "momentum": momentum,
        "bodies_per_tick": bodies_per_tick,
        "inventories": inventories,
        "bodies": bodies,
        "marks": marks,
        "snapshot": snapshot,
    }


def kinds(events, position=None):
    result = {}
    for event in events:
        if position is None or tuple(event.get("position", ())) == tuple(position):
            result[event["event"]] = result.get(event["event"], 0) + 1
    return result


def rays_at(inventory, position, index=0):
    """The rays on their way at a Node (the inventory view lists a parked shadow,
    the Node's memory of a departure or a share below one quantum, beside them)."""
    return inventory.get(tuple(position), ((),))[index]


def line(ledger, readout, name):
    return {k: v for k, v in ledger[readout][name].items() if k != "balanced"}


def parked_at(snapshot, position):
    """The parked shadows of a Node in the snapshot: (owner, heading, amount)."""
    return [
        (entry["owner"], entry["heading"], entry["amount"])
        for entry in snapshot["parked"]
        if tuple(entry["position"]) == tuple(position)
    ]


def test_shadow_pushes_thing_and_comes_home_to_body():
    """(a): the push, the walk back on the shadow's steps, home to the body with
    -dp, the re-release, the ledger's returned line and the things' identity.
    Re-pinned 2026-09-18 (node-mixing-v1): the body's shadow leaves fresh from
    the body at (3,2,2) and meets the thing at (2,2,2) in the cycle of tick 2;
    the thing is absorbed by the body one tick later, the shadow home with it."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=5,
        types=[kind, RING],
        emissions=[emission],
        seeds=[seed],
        bodies=[body((3, 2, 2))],
        shadows=[shadow((3, 2, 2), MINUS_X, owner=3, steps=0)],
        phase_bits=2,
        clock=2,
    )
    assert parse_initial_state(doc).spatial_fields[0].owners == (1, 2, 3)
    result = run(doc, 5)
    after_1 = result["inventories"][0]
    resident = rays_at(after_1, (2, 2, 2))
    thing = next(ray for ray in resident if ray.detector == BIT_THING)
    walker = next(ray for ray in resident if ray.detector == BIT_SHADOW and not ray.parked)
    assert (thing.amount, thing.phase, thing.steps, thing.owner) == (2, 1, 1, 1)
    assert (walker.amount, walker.phase, walker.steps, walker.owner) == (1, 0, 1, 3)
    # A push is not an event: the momentum line of the record shows it.
    assert not {"ray_push", "shadow_home", "external_body_pushed"} & set(kinds(result["events"]))
    assert result["momentum"][0] == {1: [2, 0, 0], 3: [0, 0, 0]}
    assert result["momentum"][1] == {3: [1, 0, 0]}
    received = [
        e for e in result["events"] if e["event"] == "spatial_received" and e.get("returned_to_body")
    ]
    assert [(e["tick"], tuple(e["position"]), e["returned_to_body"]) for e in received] == [
        (2, (3, 2, 2), {"m": {"amount": 1, "momentum": (1, 0, 0)}})
    ]
    sunk = [e for e in result["events"] if e["event"] == "external_body_absorbed"]
    assert [(e["tick"], e["amount"], e["momentum"]) for e in sunk] == [(2, 2, (1, 0, 0))]
    assert result["bodies"][0]["momentum"] == [1, 0, 0]
    fresh = [r for r in rays_at(result["inventories"][1], (3, 2, 2)) if not r.parked]
    assert [(r.detector, r.outbound, r.steps, r.owner, HEADINGS[r.heading]) for r in fresh] == [
        (BIT_SHADOW, 1, 0, 3, MINUS_X)
    ]
    assert [
        HEADINGS[r.heading] for r in rays_at(result["inventories"][2], (2, 2, 2)) if not r.parked
    ] == [MINUS_X]
    # The re-released quantum mixes at (2,2,2) and parks its ninths there, 4 on
    # its back heading and 1 on each other, beside the thing's trace.
    assert parked_at(result["snapshot"], (2, 2, 2)) == [
        (3, [1, 0, 0], 4),
        (3, [-1, 0, 0], 1),
        (3, [0, 1, 0], 1),
        (3, [0, -1, 0], 1),
        (3, [0, 0, 1], 1),
        (3, [0, 0, -1], 1),
    ]
    assert result["shadows"] == [1] * 5 and result["counts"][4] == {1: [0, 0], 2: [0, 0], 3: [0, 0]}
    ledger = result["ledgers"][4]
    assert line(ledger, "fields", "m") == {
        "initial": (3,),
        "sourced": (0,),
        "current": (1,),
        "escaped": (0,),
        "absorbed": (2,),
        "absorbed_by_marks": (0,),
        "returned": (0,),
    }
    assert line(ledger, "real", "m") == {
        "initial": (2,),
        "converted": (0,),
        "current": (0,),
        "escaped": (0,),
        "absorbed": (2,),
    }
    assert line(ledger, "shadow", "m") == {
        "initial": (1,),
        "current": (1,),
        "escaped": (0,),
        "absorbed_at_home": (0,),
    }
    assert line(ledger, "fields", "momentum") == {
        "initial": (0, 0, 0),
        "sourced": (0, 0, 0),
        "current": (-2, 0, 0),
        "escaped": (0, 0, 0),
        "absorbed": (1, 0, 0),
        "absorbed_by_marks": (0, 0, 0),
        "returned": (1, 0, 0),
        "spent": (0, 0, 0),
    }
    assert line(ledger, "charge", "m") == {
        "initial": -2,
        "sourced": 0,
        "current": 0,
        "escaped": 0,
        "absorbed": -2,
        "absorbed_by_marks": 0,
        "returned": 0,
    }
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [2, 0, 0, 0, 0]
    # A Node remembers no departure (return-field-v1): nothing is parked where
    # thing 1 left; the unit of a parked share is ninths.
    assert parked_at(result["snapshot"], (1, 2, 2)) == []
    assert all(
        entry["bit"] == BIT_SHADOW and entry["unit"] == 9 for entry in result["snapshot"]["parked"]
    )


def test_two_bodies_push_each_other_and_take_back_the_recoil():
    """(b): each body pushed by the other's shadow, each shadow home with -dp, the
    momenta equal and opposite, the shadow sets kept, no event at a Node without a
    thing. Re-pinned 2026-09-18 (node-mixing-v1): the bodies are adjacent, each
    shadow leaves fresh from its body, pushes the other at the delivery of every
    odd tick and is home with -dp at every even one, so each body's momentum
    grows by one every tick, the push and the receipt in turn."""
    doc = document(
        ticks=6,
        bodies=[body((2, 2, 2), 3, table={"m": 1}), body((3, 2, 2), 4, table={"m": 1})],
        shadows=[shadow((2, 2, 2), X, owner=3, steps=0), shadow((3, 2, 2), MINUS_X, owner=4, steps=0)],
    )
    result = run(doc, 6)
    assert result["contents"] == [0] * 6 and result["shadows"] == [2] * 6
    assert not {"ray_push", "shadow_home", "external_body_pushed"} & set(kinds(result["events"]))
    for tick, (a, b) in enumerate(result["bodies_per_tick"], start=1):
        assert (a, b) == ([-tick, 0, 0], [tick, 0, 0]), tick
    assert result["momentum"][1] == {3: [-2, 0, 0], 4: [2, 0, 0]}
    assert result["momentum"][5] == {3: [-6, 0, 0], 4: [6, 0, 0]}
    received = [
        e for e in result["events"] if e["event"] == "spatial_received" and e.get("returned_to_body")
    ]
    assert sorted(
        (e["tick"], tuple(e["position"]), e["returned_to_body"]["m"]["amount"]) for e in received
    ) == sorted(
        (tick, position, 1 - tick % 2) for tick in range(1, 7) for position in ((2, 2, 2), (3, 2, 2))
    )
    assert [b["momentum"] for b in result["bodies"]] == [[-6, 0, 0], [6, 0, 0]]
    for ledger in result["ledgers"]:
        assert ledger["balanced"] and ledger["real_conserved"]
        assert ledger["fields"]["momentum"]["returned"] == (0, 0, 0)
    assert all(counts[3] == [1, 1] and counts[4] == [1, 1] for counts in result["counts"])
    for event in result["events"]:
        if event["event"] in ("spatial_received", "spatial_cycle", "spatial_sent"):
            assert tuple(event["position"]) in ((2, 2, 2), (3, 2, 2))
    assert line(result["ledgers"][5], "shadow", "m") == {
        "initial": (2,),
        "current": (2,),
        "escaped": (0,),
        "absorbed_at_home": (0,),
    }


def test_a_thing_meets_its_own_shadow_without_a_push():
    """(c): the shadow of the thing's own identity is home at the thing ray: no push,
    absorbed back, released again with it. Re-pinned 2026-09-18 (node-mixing-v1):
    the shadow leaves fresh from (3,2,2) and is home at (2,2,2) in the cycle of
    tick 1; released again it rides one Link with the thing and then mixes."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=5,
        types=[kind, RING],
        emissions=[emission],
        seeds=[seed],
        shadows=[shadow((3, 2, 2), MINUS_X, owner=1, steps=0)],
    )
    result = run(doc, 5)
    assert not {"ray_push", "shadow_home"} & set(kinds(result["events"]))
    cycles = [e for e in result["events"] if e["event"] == "spatial_cycle" and e.get("returned")]
    assert [(e["tick"], tuple(e["position"]), e["returned"]) for e in cycles] == [
        (1, (2, 2, 2), {"m": {"amount": 1, "momentum": (0, 0, 0)}})
    ]
    assert all(r == {1: [2, 0, 0]} for r in result["momentum"])
    together = [r for r in rays_at(result["inventories"][1], (3, 2, 2)) if not r.parked]
    assert sorted((r.detector, r.amount, r.momentum, r.steps) for r in together) == [
        (BIT_SHADOW, 1, None, 1),
        (BIT_THING, 2, None, 2),
    ]
    # A homecoming is no crossing of the border (point 7): nothing sourced or returned.
    assert result["ledgers"][2]["fields"]["m"]["returned"] == (0,)
    assert result["ledgers"][2]["fields"]["m"]["sourced"] == (0,)
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [2] * 5 and result["shadows"] == [1] * 5
    # A closed board: the thing loops around it and both contents are constant.
    closed = deepcopy(doc)
    closed["boundary"] = "periodic"
    looped = run(closed, 12)
    assert looped["contents"] == [2] * 12 and looped["shadows"] == [1] * 12
    assert all(entry["balanced"] and entry["real_conserved"] for entry in looped["ledgers"])


def test_home_is_the_push_and_its_return_of_zero_steps_booked_and_cancelling():
    """(c'): "home" is no rule of its own (the model owner, 2026-09-18, point 3 as
    amended; the cleanup of that day): a thing meeting its own shadow takes the
    generic push, and the return of zero steps, the same shadow with its sign
    flipped at the same Node, hands -push back in the same cycle, before any step
    decision; the two halves are booked on the cycle record (`home_pushes`) and
    sum to zero, so the thing is what it was and the shadow is absorbed at home
    as before. The world of (c): the push of the lamp's own shadow of 1 on -X,
    read by charge (the owner's whole charge -2 over its content 2, the thing's
    charge -1, the table's sign 1), is (-1, 0, 0); the return (1, 0, 0). The
    world of (b): each body's own shadow, home at the even ticks, is pushed by
    the body's table and returned in the same interval, (1,0,0) and (-1,0,0) at
    body 3, the opposite at body 4, on the reception record (`home_pushes`),
    and the bodies' momenta are what (b) pins."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=5,
        types=[kind, RING],
        emissions=[emission],
        seeds=[seed],
        shadows=[shadow((3, 2, 2), MINUS_X, owner=1, steps=0)],
    )
    result = run(doc, 5)
    cycles = [e for e in result["events"] if e["event"] == "spatial_cycle" and e.get("home_pushes")]
    assert [(e["tick"], tuple(e["position"]), e["home_pushes"]) for e in cycles] == [
        (1, (2, 2, 2), {"m": {"push": (-1, 0, 0), "return": (1, 0, 0)}})
    ]
    assert cycles[0]["returned"] == {"m": {"amount": 1, "momentum": (0, 0, 0)}}
    assert all(r == {1: [2, 0, 0]} for r in result["momentum"])
    assert not {"ray_push", "shadow_home"} & set(kinds(result["events"]))
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    pair = document(
        ticks=6,
        bodies=[body((2, 2, 2), 3, table={"m": 1}), body((3, 2, 2), 4, table={"m": 1})],
        shadows=[shadow((2, 2, 2), X, owner=3, steps=0), shadow((3, 2, 2), MINUS_X, owner=4, steps=0)],
    )
    result = run(pair, 6)
    received = [e for e in result["events"] if e["event"] == "spatial_received" and e.get("home_pushes")]
    assert [(e["tick"], tuple(e["position"]), e["home_pushes"]) for e in received] == [
        (tick, position, {"m": {"push": (sign, 0, 0), "return": (-sign, 0, 0)}})
        for tick in (2, 4, 6)
        for position, sign in (((2, 2, 2), 1), ((3, 2, 2), -1))
    ]
    for tick, (a, b) in enumerate(result["bodies_per_tick"], start=1):
        assert (a, b) == ([-tick, 0, 0], [tick, 0, 0]), tick
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])


def test_a_mark_returns_shadows_and_counts_things_by_its_table(tmp_path):
    """(d): a shadow at a mark is returned and never counted; things are caught by
    the counter table, one in two here; the seed is read by nothing."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    kind2, emission2, seed2 = lamp("lamp2", 1, (0, 2, 2))
    doc = document(
        ticks=6,
        types=[kind, kind2],
        emissions=[emission, emission2],
        seeds=[seed, seed2],
        marks=[{"position": [4, 2, 2], "setting": [1, 2]}],
        shadows=[shadow((5, 2, 2), MINUS_X, owner=5, steps=0)],
    )
    result = run(doc, 6)
    events = result["events"]
    # A mark returning a shadow is no event: the shadow is read from the board
    # (re-pinned 2026-09-18, node-mixing-v1: the shadow leaves fresh from (5,2,2)
    # and is returned at the first delivery; return-field-v1: returned as it
    # is, an outgoing share heading +X, it mixes at (5,2,2) in the cycle of tick
    # 3 and parks its ninths there, 4 back on -X and 1 on each other heading).
    assert "shadow_return" not in kinds(events)
    for tick in range(2, 7):
        back = rays_at(result["inventories"][tick - 1], (5, 2, 2))
        moving = [(r.detector, r.owner, r.outbound, r.steps, HEADINGS[r.heading]) for r in back]
        assert moving == ([(BIT_SHADOW, 5, 1, 1, X)] if tick == 2 else []), tick
    assert parked_at(result["snapshot"], (5, 2, 2)) == [
        (5, [1, 0, 0], 1),
        (5, [-1, 0, 0], 4),
        (5, [0, 1, 0], 1),
        (5, [0, -1, 0], 1),
        (5, [0, 0, 1], 1),
        (5, [0, 0, -1], 1),
    ]
    assert result["marks"][0]["resident"]["real"] == {"m": 2}
    clicks = [e for e in events if e["event"] == "detector_click"]
    assert [(e["tick"], e["amount"], e["owner"], e.get("absorbed")) for e in clicks] == [(3, 2, 1, 2)]
    returned = [e for e in events if e["event"] == "detector_return"]
    assert [(e["tick"], e["amount"], e["owner"]) for e in returned] == [(4, 1, 2)]
    assert result["marks"] == [
        {
            "position": [4, 2, 2],
            "resident": {"real": {"m": 2}, "shadow": {}, "momentum": [2, 0, 0], "owners": [1]},
        }
    ]
    back = rays_at(result["inventories"][5], (2, 2, 2))
    assert [(r.detector, r.amount, r.outbound, r.steps) for r in back] == [(BIT_THING, 1, 0, 2)]
    ledger = result["ledgers"][5]
    assert line(ledger, "real", "m") == {
        "initial": (3,),
        "converted": (0,),
        "current": (1,),
        "escaped": (0,),
        "absorbed": (2,),
    }
    assert ledger["marks"]["real"] == {"m": (2,), "momentum": (2, 0, 0)}
    assert ledger["marks"]["shadow"] == {"m": (0,), "momentum": (0, 0, 0)}
    assert ledger["fields"]["momentum"]["current"] == (-2, 0, 0)
    assert ledger["fields"]["momentum"]["absorbed_by_marks"] == (2, 0, 0)
    assert result["contents"] == [3, 3, 1, 1, 1, 1]
    assert result["shadows"] == [1] * 6
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    # No lottery: two runs change nothing, and a seed is no declaration.
    seeded = deepcopy(doc)
    seeded["detectors"][0]["seed"] = 7
    with pytest.raises(ValueError, match="node-is-ports-v1"):
        parse_initial_state(seeded)
    records = []
    for name, world in (("first", doc), ("second", doc)):
        source = tmp_path / f"{name}.json"
        source.write_text(json.dumps(world))
        run_initialization(source, tmp_path / f"run-{name}")
        records.append((tmp_path / f"run-{name}" / "events.jsonl").read_bytes())
    assert records[0] == records[1]
    metadata = json.loads((tmp_path / "run-first" / "run.json").read_text())
    assert metadata["bit_law"] == "bit-law-v1"
    assert metadata["node_is_ports"] == "node-is-ports-v1"
    assert metadata["real_conserved"] is True
    assert metadata["real_content"] == [3, 3, 1, 1, 1, 1]
    assert metadata["shadow_content"] == [1] * 6
    assert "registers" not in metadata and metadata["momentum"][0] == {"1": [2, 0, 0], "2": [1, 0, 0]}
    assert metadata["detector_marks"] == result["marks"]


def test_a_shadow_only_board_makes_no_event_and_the_dense_layer_agrees():
    """(e): a Node holding shadows alone publishes nothing; the dense layer (the
    default when admitted) and the engine give one state and one ledger.
    Re-pinned 2026-09-18 (node-mixing-v1): each 11 sends 4 back, 1 on and 1 on
    each transverse heading and parks 2 quanta of ninths; the 4s send 1 back."""
    results = []
    for dense in (False, None):
        doc = document(
            ticks=4,
            shadows=[
                shadow((4, 2, 2), X, amount=11, owner=2),
                shadow((5, 2, 2), MINUS_X, amount=11, owner=2),
            ],
            dense=dense,
            rules=(),
        )
        assert parse_initial_state(doc).dense_field is (dense is None)
        results.append(run(doc, 4))
    for result in results:
        assert set(kinds(result["events"])) <= {"cycle_started", "cycle_committed"}
        assert result["contents"] == [0] * 4 and result["shadows"] == [22] * 4
        for ledger in result["ledgers"]:
            assert ledger["balanced"] and ledger["fields"]["m"]["current"] == (22,)
            assert ledger["fields"]["m"]["escaped"] == (0,)
        after_2 = result["inventories"][1]
        assert [
            (r.amount, HEADINGS[r.heading], r.owner) for r in rays_at(after_2, (6, 2, 2)) if not r.parked
        ] == [(1, X, 2)]
        assert [
            (r.amount, HEADINGS[r.heading], r.owner) for r in rays_at(after_2, (3, 2, 2)) if not r.parked
        ] == [(1, MINUS_X, 2)]
        after_1 = result["inventories"][0]
        assert [(r.amount, HEADINGS[r.heading]) for r in rays_at(after_1, (5, 2, 2))] == [(1, X)]
        assert [(r.amount, HEADINGS[r.heading]) for r in rays_at(after_1, (6, 2, 2))] == [(4, X)]
        assert [(r.amount, HEADINGS[r.heading]) for r in rays_at(after_1, (3, 2, 2))] == [(4, MINUS_X)]
        assert [{o: c for o, c in counts.items() if c != [0, 0]} for counts in result["counts"]] == [
            {2: [12, 18]},
            {2: [4, 4]},
            {2: [2, 2]},
            {},
        ]
    sparse, dense = results
    assert sparse["ledgers"] == dense["ledgers"]
    assert sparse["inventories"] == dense["inventories"]
    assert sparse["snapshot"]["parked"] == dense["snapshot"]["parked"]
    # The shares below one quantum are parked shadows in ninths (node-mixing-v1):
    # 8 on each axis heading and 5 on each transverse one at (4,2,2), 2 on +X and
    # 5 on the five others at (3,2,2).
    assert all(entry["unit"] == 9 and 0 < entry["amount"] < 9 for entry in sparse["snapshot"]["parked"])
    assert sorted(parked_at(sparse["snapshot"], (4, 2, 2))) == [
        (2, [-1, 0, 0], 8),
        (2, [0, -1, 0], 5),
        (2, [0, 0, -1], 5),
        (2, [0, 0, 1], 5),
        (2, [0, 1, 0], 5),
        (2, [1, 0, 0], 8),
    ]
    assert sorted(amount for _, _, amount in parked_at(sparse["snapshot"], (3, 2, 2))) == [
        2,
        5,
        5,
        5,
        5,
        5,
    ]


def test_the_fill_gives_the_board_the_bodys_shadows_exactly():
    """(f): two intervals of the mixing's transient from a body, exact in both
    modes and booked as initial content (re-pinned 2026-09-18, node-mixing-v1:
    the 11 at each neighbour sends 4 back to the body, which reflects them, 1 on
    and 1 on each transverse heading, and parks 2 quanta of ninths)."""
    results = []
    for dense in (False, None):
        doc = document(
            ticks=3,
            bodies=[body((4, 2, 2), amount=11)],
            fill=2,
            dense=dense,
            rules=(),
        )
        results.append(run(doc, 3))
    for result in results:
        first = result["ledgers"][0]
        assert first["fields"]["m"]["initial"] == (132,)
        assert first["shadow"]["m"]["initial"] == (132,) and first["real"]["m"]["initial"] == (0,)
        assert all(entry["balanced"] for entry in result["ledgers"])
    sparse, dense = results
    assert sparse["ledgers"] == dense["ledgers"]
    assert sparse["inventories"] == dense["inventories"]
    initial = parse_initial_state(
        document(
            ticks=3,
            bodies=[body((4, 2, 2), amount=11)],
            fill=2,
            dense=False,
            rules=(),
        )
    )
    with Simulation(initial) as world:
        held = {
            node.position: [r for r in node.rays[0] if not r.parked]
            for node in world.inventory_view().nodes
            if any(node.rays)
        }
        parked = sum(entry["amount"] for entry in world.snapshot()["parked"])
    amounts = {position: sorted(r.amount for r in rays) for position, rays in held.items() if rays}
    assert amounts[(5, 2, 2)] == [11] and amounts[(6, 2, 2)] == [1] and amounts[(5, 3, 2)] == [1, 1]
    assert amounts[(4, 2, 2)] == [4] * 6
    assert all(r.steps == 0 and r.outbound for r in held[(4, 2, 2)])
    assert sum(sum(a) for a in amounts.values()) == 120 and parked == 12 * 9


def test_a_mark_is_the_home_of_the_shadows_of_what_it_absorbed():
    """(h): the mark that absorbed a thing is the home of its shadows (settled rule
    (iv)). Re-pinned 2026-09-18 (node-mixing-v1, then return-field-v1): the
    shadow leaves fresh from (3,2,2) into the mark, is returned at the first
    delivery as it is, meets its thing at (3,2,2) in the cycle after its arrival
    (home, re-released with it) and reaches the mark in the same delivery as the thing,
    where it is returned once more before the thing is resident, since the
    mark meets its arrivals in order; it mixes at (3,2,2) from tick 5 and parks
    its ninths there. Nothing is absorbed at home in these five ticks, and no
    trace is left anywhere (a Node remembers no departure)."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=5,
        types=[kind, RING],
        emissions=[emission],
        seeds=[seed],
        marks=[
            {"position": [4, 2, 2], "setting": [1, 1]},
            {"position": [8, 2, 2], "setting": [1, 1]},
        ],
        shadows=[shadow((3, 2, 2), X, owner=1, steps=0)],
    )
    result = run(doc, 5)
    events = result["events"]
    back = [r for r in rays_at(result["inventories"][1], (3, 2, 2)) if r.detector == BIT_SHADOW]
    assert [(r.outbound, r.steps, HEADINGS[r.heading]) for r in back if not r.parked] == [
        (1, 1, MINUS_X)
    ]
    cycles = [e for e in events if e["event"] == "spatial_cycle" and e.get("returned")]
    assert [(e["tick"], tuple(e["position"])) for e in cycles] == [(2, (3, 2, 2))]
    assert [(e["tick"], e.get("absorbed")) for e in events if e["event"] == "detector_click"] == [(3, 2)]
    assert "shadow_absorbed" not in kinds(events)
    assert result["marks"][0] == {
        "position": [4, 2, 2],
        "resident": {"real": {"m": 2}, "shadow": {}, "momentum": [2, 0, 0], "owners": [1]},
    }
    # A Node remembers no departure (return-field-v1): nothing parked at the mark;
    # the returned shadow's ninths at (3,2,2), 4 back on +X and 1 each other way.
    assert parked_at(result["snapshot"], (4, 2, 2)) == []
    assert parked_at(result["snapshot"], (3, 2, 2)) == [
        (1, [1, 0, 0], 4),
        (1, [-1, 0, 0], 1),
        (1, [0, 1, 0], 1),
        (1, [0, -1, 0], 1),
        (1, [0, 0, 1], 1),
        (1, [0, 0, -1], 1),
    ]
    ledger = result["ledgers"][4]
    assert ledger["fields"]["m"]["absorbed_by_marks"] == (2,)
    assert (ledger["real"]["m"]["absorbed"], ledger["real"]["m"]["current"]) == ((2,), (0,))
    assert (ledger["shadow"]["m"]["absorbed_at_home"], ledger["shadow"]["m"]["current"]) == (
        (0,),
        (1,),
    )
    assert ledger["marks"]["real"] == {"m": (2,), "momentum": (2, 0, 0)}
    assert ledger["marks"]["shadow"] == {"m": (0,), "momentum": (0, 0, 0)}
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [2, 2, 0, 0, 0] and result["shadows"] == [1] * 5


def test_the_ledger_per_bit_with_the_border_lines():
    """(i): the marked and external elements and the board's edge are the border
    between the board and the outside; per family and per bit, initial +
    converted = current + escaped + absorbed (things) and initial = current +
    escaped + absorbed_at_home (shadows), exact at every tick, in the world
    ledger the runner records; a lamp is a thing that spends its content
    (node-is-ports-v1): each holds the six quanta of its run."""
    kind_a, emission_a, seed_a = lamp("lamp_a", 6, (1, 2, 2))
    kind_b, emission_b, seed_b = lamp("lamp_b", 6, (1, 3, 2))
    for emission in (emission_a, emission_b):
        emission.update(amount=1)
    doc = document(
        ticks=6,
        types=[kind_a, kind_b],
        emissions=[emission_a, emission_b],
        seeds=[seed_a, seed_b],
        bodies=[body((4, 2, 2), 3)],
        marks=[
            {"position": [4, 3, 2], "setting": [1, 1]},
            {"position": [8, 3, 2], "setting": [1, 1]},
        ],
        shadows=[
            shadow((9, 1, 2), X, owner=3, steps=0),
            shadow((5, 2, 2), MINUS_X, owner=3, steps=0),
            shadow((3, 3, 2), X, owner=2, steps=0),
        ],
        rules=(),
    )
    # Re-pinned 2026-09-18 (node-mixing-v1): the three shadows leave fresh, one
    # off the board's edge at tick 1, one into the body and one into the mark,
    # which returns it to its thing at (3,3,2), where it is home and released
    # again with it every other tick, the mark returning it each time.
    result = run(doc, 6)
    ledger = result["ledgers"][5]
    assert line(ledger, "real", "m") == {
        "initial": (12,),
        "converted": (0,),
        "current": (4,),
        "escaped": (0,),
        "absorbed": (8,),
    }
    assert line(ledger, "shadow", "m") == {
        "initial": (3,),
        "current": (2,),
        "escaped": (1,),
        "absorbed_at_home": (0,),
    }
    assert line(ledger, "fields", "m") == {
        "initial": (15,),
        "sourced": (0,),
        "current": (6,),
        "escaped": (1,),
        "absorbed": (4,),
        "absorbed_by_marks": (4,),
        "returned": (0,),
    }
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    # The lamps' content counts among the things until it is absorbed: two per
    # tick from tick 3, the 0-th quantum of each lamp at its border after tick 3.
    assert result["contents"] == [12, 12, 10, 8, 6, 4]
    assert result["shadows"] == [2] * 6
    assert result["marks"][0]["resident"]["real"] == {"m": 4}
    assert result["marks"][0]["resident"]["shadow"] == {}
    assert result["marks"][0]["resident"]["owners"] == [2]
    assert result["bodies"][0]["sink"] == {"m": 4}


def test_a_thing_moves_whole_while_its_shadows_spread():
    """(k): a thing is never split; only its shadows spread, by the Node's mixing
    (points 2, 12 and 24), and the thing's Node alone publishes events (point 13).
    Re-pinned 2026-09-18 (node-mixing-v1): the 11 sends 4 back and 1 each other way."""
    kind, emission, seed = lamp("lamp", 2, (1, 1, 2))
    doc = document(
        ticks=3,
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        shadows=[shadow((4, 2, 2), X, amount=11, owner=1)],
        rules=(),
    )
    result = run(doc, 3)
    assert result["contents"] == [2] * 3 and result["shadows"] == [11] * 3
    for tick in range(1, 4):
        thing = [r for r in rays_at(result["inventories"][tick - 1], (1 + tick, 1, 2)) if not r.parked]
        assert [(r.detector, r.amount, r.owner, r.steps) for r in thing] == [(BIT_THING, 2, 1, tick)]
    after_1, after_2 = result["inventories"][:2]
    assert [(r.amount, r.detector, r.owner) for r in rays_at(after_1, (5, 2, 2))] == [(1, BIT_SHADOW, 1)]
    assert [(r.amount, HEADINGS[r.heading]) for r in rays_at(after_1, (3, 2, 2))] == [(4, MINUS_X)]
    assert [(r.amount, HEADINGS[r.heading]) for r in rays_at(after_2, (4, 2, 2)) if not r.parked] == [
        (1, X)
    ]
    assert [r for r in rays_at(after_2, (6, 2, 2)) if not r.parked] == []
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    # Nothing is created from a shadow, and nothing is sourced (node-is-ports-v1).
    assert all("sourced" not in entry["shadow"]["m"] for entry in result["ledgers"])
    assert all(entry["shadow"]["m"]["absorbed_at_home"] == (0,) for entry in result["ledgers"])
    for event in result["events"]:
        if event["event"] not in ("cycle_started", "cycle_committed"):
            assert tuple(event["position"])[1:] == (1, 2), event


@pytest.mark.parametrize("reads", ["content", "charge"])
def test_a_thing_reads_the_shadows_message_by_its_content_or_its_charge(reads):
    """(j): the one rule of what the thing multiplies the shadow's message by
    (point 16): `reads` "content" gives every thing the same acceleration,
    `reads` "charge" gives things of one charge the same push."""
    kind, emission, seed = lamp("lamp", 2, (1, 1, 2))
    kind2, emission2, seed2 = lamp("lamp2", 4, (1, 3, 2))
    doc = document(
        ticks=3,
        types=[kind, kind2],
        emissions=[emission, emission2],
        seeds=[seed, seed2],
        bodies=[body((9, 2, 2))],
        shadows=[
            shadow((3, 1, 2), MINUS_X, owner=3, steps=0),
            shadow((3, 3, 2), MINUS_X, owner=3, steps=0),
        ],
        rules=(TURN | {"momentum_table": {"m": -1}, "reads": reads},),
    )
    # Re-pinned 2026-09-18 (node-mixing-v1): the shadows leave fresh one Link
    # ahead of the things and push them head on at (2,y,2) in the cycle of tick
    # 2. Re-pinned the same day (return-field-v1): each shadow turns back with
    # the opposite sign carrying -dp, rides the Link to (3,y,2) with the thing
    # it pushed on the same lane and pushes nothing there (one meeting, one
    # push; the double push of the first pin was an artefact, removed
    # 2026-09-18), mixes at (3,y,2) in the cycle of tick 3 and parks its ninths
    # there with -dp shared over them by the largest remainder.
    result = run(doc, 3)
    pushes = {"content": ((2, 0, 0), (4, 0, 0)), "charge": ((1, 0, 0), (1, 0, 0))}[reads]
    assert result["momentum"][0] == {1: [2, 0, 0], 2: [4, 0, 0], 3: [0, 0, 0]}
    assert result["momentum"][1] == {
        1: [2 + pushes[0][0], 0, 0],
        2: [4 + pushes[1][0], 0, 0],
        3: [0, 0, 0],
    }
    assert result["momentum"][2] == result["momentum"][1]
    for y, push in ((1, pushes[0]), (3, pushes[1])):
        rays = [r for r in rays_at(result["inventories"][2], (4, y, 2)) if not r.parked]
        # The momentum a thing carries is the pushes it took (clock-readings-v1).
        assert sorted((r.detector, r.owner, r.momentum, r.outbound, r.steps) for r in rays) == [
            (BIT_THING, y // 2 + 1, (push[0], 0, 0), 1, 3),
        ]
        # After tick 2 the share rides beside the thing at (3,y,2), on its lane.
        rays = [r for r in rays_at(result["inventories"][1], (3, y, 2)) if not r.parked]
        assert sorted((r.detector, r.owner, r.momentum, r.outbound, r.steps) for r in rays) == [
            (BIT_SHADOW, 3, (-push[0], 0, 0), 0, 1),
            (BIT_THING, y // 2 + 1, (push[0], 0, 0), 1, 2),
        ]
        assert not [r for r in rays_at(result["inventories"][2], (3, y, 2)) if not r.parked]
        # -dp over the ninths by the largest remainder, the 4 back first, then
        # the lower Ports.
        carried = {
            1: {(-1, 0, 0): -1},
            2: {(-1, 0, 0): -1, (1, 0, 0): -1},
            4: {(-1, 0, 0): -2, (1, 0, 0): -1, (0, 1, 0): -1},
        }[push[0]]
        ninths = [
            (tuple(e["heading"]), e["amount"], tuple(e["momentum"]), e["outbound"])
            for e in result["snapshot"]["parked"]
            if tuple(e["position"]) == (3, y, 2)
        ]
        assert sorted(ninths) == sorted(
            (tuple(h), 4 if h == MINUS_X else 1, (carried.get(tuple(h), 0), 0, 0), 0) for h in HEADINGS
        )
    assert all(entry["balanced"] and entry["real_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [6] * 3 and result["shadows"] == [2] * 3


@pytest.mark.parametrize(
    ("change", "message"),
    [
        (lambda d: d["spatial_fields"][0].update(field_of="m"), "bit-law-v1"),
        (lambda d: d["ray_interactions"][0].pop("reads"), "point 16"),
        (lambda d: d["ray_interactions"][0].update(reads="mass"), "point 16"),
        (
            lambda d: d["external_bodies"].append(
                {"position": [7, 2, 2], "family": "m", "amount": 1, "momentum_table": {"m": 1}}
            ),
            "point 16",
        ),
        (
            lambda d: d["detectors"].append(
                {"position": [4, 2, 2], "setting": [1, 1], "on_bit_1": "draw"}
            ),
            "bit-law-v1",
        ),
        (
            lambda d: d["detectors"].append({"position": [4, 2, 2], "setting": [1, 1], "seed": 0}),
            "node-is-ports-v1",
        ),
        (lambda d: d["emissions"][0].update(source=False), "node-is-ports-v1"),
        (lambda d: d["emissions"][0].update(recoil_field="momentum"), "node-is-ports-v1"),
        (
            lambda d: d["disturbance_types"][0].update(fields=["m"], defaults={"m": 2}),
            "node-is-ports-v1",
        ),
        (lambda d: d["ray_interactions"][0].update(bit="none"), "bit-law-v1"),
        (
            lambda d: d["external_bodies"].append(
                {"position": [7, 2, 2], "family": "m", "amount": 1, "field": "m"}
            ),
            "bit-law-v1",
        ),
        (
            lambda d: d["disturbance_types"].append(RING | {"name": "other", "thing": 1}),
            "distinct thing",
        ),
    ],
)
def test_the_retired_declarations_are_rejected(change, message):
    """(g): the declarations the law retired name it when they are rejected."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(ticks=1, types=[kind, RING], emissions=[emission], seeds=[seed])
    change(doc)
    with pytest.raises(ValueError, match=message):
        parse_initial_state(doc)
