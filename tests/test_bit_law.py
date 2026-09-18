"""The law of the bit (bit-law-v1; Highlights 5.4, the model owner's decision of
2026-09-18, with the amendments of that day).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The law of the bit")
before the first run. Every ray carries one bit, 1 a thing and 0 its shadow, a ray
of the same family: a shadow pushes a thing it meets and walks home with -dp,
home to a body (a) and to a thing ray (c); a thing's own shadow never pushes it;
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


def family(spread=None, phase_bits=0, clock=False):
    entry = {
        "field": "m",
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 8,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": phase_bits,
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
        "source": False,
        "recoil_field": "momentum",
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


def shadow(position, heading, amount=1, owner=1, sign=-1):
    """A profile shadow; its sign is its owner's charge sign (-1 here, the
    family's charge and the bodies' charge are -1)."""
    return {
        "position": list(position),
        "heading": list(heading),
        "amount": amount,
        "owner": owner,
        "sign": sign,
    }


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
        "spatial_fields": [family(spread, phase_bits, bool(clock))],
        **({"K": clock} if clock else {}),
        # The wait per whole quantum read (Highlights 5.4 point 23) is pinned in
        # tests/test_wait_rule.py; these worlds pin the pushes without it.
        "wait_per_quantum": 0,
        "emissions": list(emissions),
        "seeds": list(seeds),
        "ray_interactions": list(rules),
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
    things' and the shadows' content and the shadows per thing, then the final
    inventory."""
    events = []
    ledgers, contents, shadows, counts, inventories = [], [], [], [], []
    registers, bodies_per_tick = [], []
    with Simulation(parse_initial_state(doc), observer=events.append) as world:
        for _ in range(ticks):
            world.step()
            ledgers.append(world.audit())
            contents.append(world.things_content())
            shadows.append(world.shadows_content())
            counts.append(world.shadow_counts())
            registers.append(world.thing_registers())
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
        "registers": registers,
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
    return inventory.get(tuple(position), ((),))[index]


def line(ledger, readout, name):
    return {k: v for k, v in ledger[readout][name].items() if k != "balanced"}


def test_shadow_pushes_thing_and_comes_home_to_body():
    """(a): the push, the walk back on the shadow's steps, home to the body with
    -dp, the re-release, the ledger's returned line and the things' identity."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=7,
        types=[kind, RING],
        emissions=[emission],
        seeds=[seed],
        bodies=[body((7, 2, 2))],
        shadows=[shadow((5, 2, 2), MINUS_X, owner=3)],
        phase_bits=2,
        clock=2,
    )
    assert parse_initial_state(doc).spatial_fields[0].owners == (1, 2, 3)
    result = run(doc, 7)
    after_2 = result["inventories"][1]
    resident = rays_at(after_2, (3, 2, 2))
    thing = next(ray for ray in resident if ray.detector == BIT_THING)
    walker = next(ray for ray in resident if ray.detector == BIT_SHADOW)
    assert (thing.amount, thing.phase, thing.steps, thing.owner) == (2, 2, 2, 1)
    assert (walker.amount, walker.phase, walker.steps, walker.owner) == (1, 0, 3, 3)
    # A push is not an event: the register line of the record shows it.
    assert not {"ray_push", "shadow_home", "external_body_pushed"} & set(kinds(result["events"]))
    assert result["registers"][1] == {1: [2, 0, 0], 3: [0, 0, 0]}
    assert result["registers"][2] == {1: [1, 0, 0], 3: [0, 0, 0]}
    pushed = next(r for r in rays_at(result["inventories"][3], (5, 2, 2)) if r.detector == BIT_THING)
    # The momentum a thing carries is the pushes it took (clock-readings-v1).
    assert (pushed.detector, pushed.owner, pushed.momentum, pushed.amount) == (
        BIT_THING,
        1,
        (-1, 0, 0),
        2,
    )
    for tick, steps in ((3, 2), (4, 1), (5, 0)):
        back = rays_at(result["inventories"][tick - 1], (tick + 1, 2, 2))
        returning = [ray for ray in back if ray.detector == BIT_SHADOW]
        assert [(ray.outbound, ray.steps, ray.momentum) for ray in returning] == [(0, steps, (1, 0, 0))]
    received = [
        e for e in result["events"] if e["event"] == "spatial_received" and e.get("returned_to_body")
    ]
    assert [(e["tick"], tuple(e["position"]), e["returned_to_body"]) for e in received] == [
        (6, (7, 2, 2), {"m": {"amount": 1, "momentum": (1, 0, 0)}})
    ]
    assert result["registers"][4] == {1: [1, 0, 0], 3: [0, 0, 0]}
    assert result["registers"][5] == {3: [1, 0, 0]}
    sunk = [e for e in result["events"] if e["event"] == "external_body_absorbed"]
    assert [(e["tick"], e["amount"], e["momentum"]) for e in sunk] == [(6, 2, (1, 0, 0))]
    assert result["bodies"][0]["momentum"] == [1, 0, 0]
    fresh = rays_at(result["inventories"][5], (7, 2, 2))
    assert [(r.detector, r.outbound, r.steps, r.owner, HEADINGS[r.heading]) for r in fresh] == [
        (BIT_SHADOW, 1, 0, 3, MINUS_X)
    ]
    assert [HEADINGS[r.heading] for r in rays_at(result["inventories"][6], (6, 2, 2))] == [MINUS_X]
    ledger = result["ledgers"][5]
    assert line(ledger, "fields", "m") == {
        "initial": (3,),
        "sourced": (0,),
        "current": (1,),
        "escaped": (0,),
        "annulled": (0,),
        "absorbed": (2,),
        "absorbed_by_marks": (0,),
        "returned": (0,),
    }
    assert line(ledger, "things", "m") == {
        "initial": (2,),
        "sourced": (0,),
        "current": (0,),
        "escaped": (0,),
        "annulled": (0,),
        "absorbed": (2,),
        "absorbed_by_marks": (0,),
        "returned": (0,),
    }
    assert line(ledger, "shadows", "m") == {
        "initial": (1,),
        "sourced": (0,),
        "current": (1,),
        "escaped": (0,),
        "annulled": (0,),
        "absorbed": (0,),
        "absorbed_by_marks": (0,),
        "returned": (0,),
    }
    assert line(ledger, "fields", "momentum") == {
        "initial": (0, 0, 0),
        "sourced": (0, 0, 0),
        "current": (-2, 0, 0),
        "escaped": (0, 0, 0),
        "annulled": (0, 0, 0),
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
        "annulled": 0,
        "absorbed": -2,
        "absorbed_by_marks": 0,
        "returned": 0,
    }
    assert all(entry["balanced"] and entry["things_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [2, 2, 2, 2, 2, 0, 0]
    assert result["shadows"] == [1] * 7
    traced = {tuple(n["position"]): n.get("traces") for n in result["snapshot"]["spatial_fields"]}
    assert traced[(3, 2, 2)] == [[1, 0]]


def test_two_bodies_push_each_other_and_take_back_the_recoil():
    """(b): each body pushed by the other's shadow, each shadow home with -dp, the
    momenta equal and opposite, the shadow sets kept, no event at a Node without a thing."""
    doc = document(
        ticks=10,
        bodies=[body((2, 2, 2), 3, table={"m": 1}), body((7, 2, 2), 4, table={"m": 1})],
        shadows=[shadow((3, 2, 2), X, owner=3), shadow((6, 2, 2), MINUS_X, owner=4)],
    )
    result = run(doc, 10)
    assert result["contents"] == [0] * 10 and result["shadows"] == [2] * 10
    assert not {"ray_push", "shadow_home", "external_body_pushed"} & set(kinds(result["events"]))
    for tick, (a, b) in enumerate(result["bodies_per_tick"], start=1):
        expected = [0, 0, 0] if tick < 4 else [-1, 0, 0] if tick < 9 else [-2, 0, 0]
        assert (a, b) == (expected, [-c for c in expected]), tick
    assert result["registers"][3] == {3: [-1, 0, 0], 4: [1, 0, 0]}
    assert result["registers"][8] == {3: [-2, 0, 0], 4: [2, 0, 0]}
    received = [
        e for e in result["events"] if e["event"] == "spatial_received" and e.get("returned_to_body")
    ]
    assert sorted(
        (e["tick"], tuple(e["position"]), e["returned_to_body"]["m"]["momentum"]) for e in received
    ) == [
        (4, (2, 2, 2), (-1, 0, 0)),
        (4, (7, 2, 2), (1, 0, 0)),
        (9, (2, 2, 2), (-1, 0, 0)),
        (9, (7, 2, 2), (1, 0, 0)),
    ]
    assert [b["momentum"] for b in result["bodies"]] == [[-2, 0, 0], [2, 0, 0]]
    for ledger in result["ledgers"]:
        assert ledger["balanced"] and ledger["things_conserved"]
        assert ledger["fields"]["momentum"]["returned"] == (0, 0, 0)
    assert all(counts == {3: [1, 1], 4: [1, 1]} for counts in result["counts"])
    for event in result["events"]:
        if event["event"] in ("spatial_received", "spatial_cycle", "spatial_sent"):
            assert tuple(event["position"]) in ((2, 2, 2), (7, 2, 2))
    assert line(result["ledgers"][8], "shadows", "m") == {
        "initial": (2,),
        "sourced": (0,),
        "current": (2,),
        "escaped": (0,),
        "annulled": (0,),
        "absorbed": (0,),
        "absorbed_by_marks": (0,),
        "returned": (0,),
    }


def test_a_thing_meets_its_own_shadow_without_a_push():
    """(c): the shadow of the thing's own identity is home at the thing ray: no push,
    absorbed back, released again with it."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=5,
        types=[kind, RING],
        emissions=[emission],
        seeds=[seed],
        shadows=[shadow((5, 2, 2), MINUS_X, owner=1)],
    )
    result = run(doc, 5)
    assert not {"ray_push", "shadow_home"} & set(kinds(result["events"]))
    cycles = [e for e in result["events"] if e["event"] == "spatial_cycle" and e.get("returned")]
    assert [(e["tick"], tuple(e["position"]), e["returned"]) for e in cycles] == [
        (2, (3, 2, 2), {"m": {"amount": 1, "momentum": (0, 0, 0)}})
    ]
    assert all(r == {1: [2, 0, 0]} for r in result["registers"])
    together = rays_at(result["inventories"][4], (6, 2, 2))
    assert sorted((r.detector, r.amount, r.momentum, r.steps) for r in together) == [
        (BIT_SHADOW, 1, None, 3),
        (BIT_THING, 2, None, 5),
    ]
    # A homecoming is no crossing of the border (point 7): nothing sourced or returned.
    assert result["ledgers"][2]["fields"]["m"]["returned"] == (0,)
    assert result["ledgers"][2]["fields"]["m"]["sourced"] == (0,)
    assert all(entry["balanced"] and entry["things_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [2] * 5 and result["shadows"] == [1] * 5
    # A closed board: the thing loops around it and both contents are constant.
    closed = deepcopy(doc)
    closed["boundary"] = "periodic"
    looped = run(closed, 12)
    assert looped["contents"] == [2] * 12 and looped["shadows"] == [1] * 12
    assert all(entry["balanced"] and entry["things_conserved"] for entry in looped["ledgers"])


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
        marks=[{"position": [4, 2, 2], "setting": [1, 2], "seed": 0}],
        shadows=[shadow((5, 2, 2), MINUS_X, owner=5)],
    )
    result = run(doc, 6)
    events = result["events"]
    # A mark returning a shadow is no event: the shadow is read from the board.
    assert "shadow_return" not in kinds(events)
    back = rays_at(result["inventories"][1], (5, 2, 2))
    assert [(r.detector, r.owner, r.outbound, r.steps, HEADINGS[r.heading]) for r in back] == [
        (BIT_SHADOW, 5, 0, 1, X)
    ]
    assert result["marks"][0]["counter"] == {"m": 2}
    clicks = [e for e in events if e["event"] == "detector_click"]
    assert [(e["tick"], e["amount"], e["owner"], e.get("absorbed")) for e in clicks] == [(3, 2, 1, 2)]
    returned = [e for e in events if e["event"] == "detector_return"]
    assert [(e["tick"], e["amount"], e["owner"]) for e in returned] == [(4, 1, 2)]
    assert result["marks"] == [
        {"position": [4, 2, 2], "momentum": [2, 0, 0], "counter": {"m": 2}, "things": [1]}
    ]
    back = rays_at(result["inventories"][5], (2, 2, 2))
    assert [(r.detector, r.amount, r.outbound, r.steps) for r in back] == [(BIT_THING, 1, 0, 2)]
    ledger = result["ledgers"][5]
    assert line(ledger, "things", "m") == {
        "initial": (3,),
        "sourced": (0,),
        "current": (1,),
        "escaped": (0,),
        "annulled": (0,),
        "absorbed": (0,),
        "absorbed_by_marks": (2,),
        "returned": (0,),
    }
    assert ledger["fields"]["momentum"]["current"] == (-2, 0, 0)
    assert ledger["fields"]["momentum"]["absorbed_by_marks"] == (2, 0, 0)
    assert result["contents"] == [3, 3, 1, 1, 1, 1]
    assert result["shadows"] == [1] * 6
    assert all(entry["balanced"] and entry["things_conserved"] for entry in result["ledgers"])
    # No lottery: two runs, and a seed, change nothing.
    seeded = deepcopy(doc)
    seeded["detectors"][0]["seed"] = 7
    records = []
    for name, world in (("first", doc), ("second", doc), ("seeded", seeded)):
        source = tmp_path / f"{name}.json"
        source.write_text(json.dumps(world))
        run_initialization(source, tmp_path / f"run-{name}")
        records.append((tmp_path / f"run-{name}" / "events.jsonl").read_bytes())
    assert records[0] == records[1] == records[2]
    metadata = json.loads((tmp_path / "run-first" / "run.json").read_text())
    assert metadata["bit_law"] == "bit-law-v1"
    assert metadata["things_conserved"] is True
    assert metadata["things_content"] == [3, 3, 1, 1, 1, 1]
    assert metadata["shadows_content"] == [1] * 6


def test_a_shadow_only_board_makes_no_event_and_the_dense_layer_agrees():
    """(e): a Node holding shadows alone publishes nothing; the dense layer (the
    default when admitted) and the engine give one state and one ledger."""
    results = []
    for dense in (False, None):
        doc = document(
            ticks=4,
            shadows=[
                shadow((4, 2, 2), X, amount=11, owner=2),
                shadow((5, 2, 2), MINUS_X, amount=11, owner=2),
            ],
            spread=[6, 1, 1, 1, 1, 1],
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
        assert [(r.amount, HEADINGS[r.heading], r.owner) for r in rays_at(after_2, (6, 2, 2))] == [
            (3, X, 2)
        ]
        assert [(r.amount, HEADINGS[r.heading], r.owner) for r in rays_at(after_2, (3, 2, 2))] == [
            (3, MINUS_X, 2)
        ]
        after_1 = result["inventories"][0]
        assert [(r.amount, HEADINGS[r.heading]) for r in rays_at(after_1, (5, 2, 2))] == [(6, X)]
        assert [(r.amount, HEADINGS[r.heading]) for r in rays_at(after_1, (6, 2, 2))] == [(1, X)]
    sparse, dense = results
    assert sparse["ledgers"] == dense["ledgers"]
    assert sparse["inventories"] == dense["inventories"]
    assert sparse["snapshot"]["field_remainders"] == dense["snapshot"]["field_remainders"]


def test_the_fill_gives_the_board_the_bodys_shadows_exactly():
    """(f): two intervals of the split table's transient from a body, exact in
    both modes and booked as initial content."""
    results = []
    for dense in (False, None):
        doc = document(
            ticks=3,
            bodies=[body((4, 2, 2), amount=11)],
            spread=[6, 1, 1, 1, 1, 1],
            fill=2,
            dense=dense,
            rules=(),
        )
        results.append(run(doc, 3))
    for result in results:
        first = result["ledgers"][0]
        assert first["fields"]["m"]["initial"] == (132,)
        assert first["shadows"]["m"]["initial"] == (132,) and first["things"]["m"]["initial"] == (0,)
        assert all(entry["balanced"] for entry in result["ledgers"])
    sparse, dense = results
    assert sparse["ledgers"] == dense["ledgers"]
    assert sparse["inventories"] == dense["inventories"]
    initial = parse_initial_state(
        document(
            ticks=3,
            bodies=[body((4, 2, 2), amount=11)],
            spread=[6, 1, 1, 1, 1, 1],
            fill=2,
            dense=False,
            rules=(),
        )
    )
    with Simulation(initial) as world:
        held = {node.position: node.rays[0] for node in world.inventory_view().nodes if any(node.rays)}
    amounts = {position: sorted(r.amount for r in rays) for position, rays in held.items()}
    assert amounts[(5, 2, 2)] == [11] and amounts[(6, 2, 2)] == [6] and amounts[(5, 3, 2)] == [1, 1]
    assert amounts[(4, 2, 2)] == [1] * 6
    assert all(r.steps == 0 and r.outbound for r in held[(4, 2, 2)])
    assert sum(sum(a) for a in amounts.values()) == 132


def test_a_mark_is_the_home_of_the_shadows_of_what_it_absorbed():
    """(h): the trace of a thing a mark absorbed ends at the mark, and each shadow
    of it that returns is absorbed into the same counter."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=5,
        types=[kind, RING],
        emissions=[emission],
        seeds=[seed],
        marks=[
            {"position": [4, 2, 2], "setting": [1, 1], "seed": 0},
            {"position": [8, 2, 2], "setting": [1, 1], "seed": 0},
        ],
        shadows=[shadow((7, 2, 2), X, owner=1)],
    )
    result = run(doc, 5)
    events = result["events"]
    assert "shadow_return" not in kinds(events)
    back = rays_at(result["inventories"][1], (7, 2, 2))
    assert [(r.detector, r.outbound, r.steps, HEADINGS[r.heading]) for r in back] == [
        (BIT_SHADOW, 0, 1, MINUS_X)
    ]
    assert [(e["tick"], e.get("absorbed")) for e in events if e["event"] == "detector_click"] == [(3, 2)]
    homed = [e for e in events if e["event"] == "shadow_absorbed"]
    assert [
        (e["tick"], tuple(e["position"]), e["amount"], e["owner"], e["momentum"]) for e in homed
    ] == [(5, (4, 2, 2), 1, 1, (0, 0, 0))]
    assert result["marks"][0] == {
        "position": [4, 2, 2],
        "momentum": [2, 0, 0],
        "counter": {"m": 3},
        "things": [1],
    }
    traced = {tuple(n["position"]): n.get("traces") for n in result["snapshot"]["spatial_fields"]}
    assert traced[(4, 2, 2)] == [[1, 6]]
    ledger = result["ledgers"][4]
    assert ledger["fields"]["m"]["absorbed_by_marks"] == (3,)
    assert (ledger["things"]["m"]["absorbed_by_marks"], ledger["things"]["m"]["current"]) == ((2,), (0,))
    assert (ledger["shadows"]["m"]["absorbed_by_marks"], ledger["shadows"]["m"]["current"]) == (
        (1,),
        (0,),
    )
    assert all(entry["balanced"] and entry["things_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [2, 2, 0, 0, 0] and result["shadows"] == [1, 1, 1, 1, 0]


def test_the_ledger_per_bit_with_the_border_lines():
    """(i): the marked and external elements and the board's edge are the border
    between the board and the outside; per family and per bit, initial +
    sourced = current + absorbed_by_bodies + absorbed_by_marks + escaped +
    returned, exact at every tick, in the world ledger the runner records."""
    kind_a, emission_a, seed_a = lamp("lamp_a", 0, (1, 2, 2))
    kind_b, emission_b, seed_b = lamp("lamp_b", 0, (1, 3, 2))
    for emission in (emission_a, emission_b):
        emission.update(amount=1, source=True)
        del emission["recoil_field"]
    doc = document(
        ticks=6,
        types=[kind_a, kind_b],
        emissions=[emission_a, emission_b],
        seeds=[seed_a, seed_b],
        bodies=[body((4, 2, 2), 3)],
        marks=[
            {"position": [4, 3, 2], "setting": [1, 1], "seed": 0},
            {"position": [8, 3, 2], "setting": [1, 1], "seed": 0},
        ],
        shadows=[
            shadow((6, 1, 2), X, owner=3),
            shadow((6, 2, 2), MINUS_X, owner=3),
            shadow((7, 3, 2), X, owner=2),
        ],
        rules=(),
    )
    result = run(doc, 6)
    ledger = result["ledgers"][5]
    assert line(ledger, "things", "m") == {
        "initial": (0,),
        "sourced": (12,),
        "current": (4,),
        "escaped": (0,),
        "annulled": (0,),
        "absorbed": (4,),
        "absorbed_by_marks": (4,),
        "returned": (0,),
    }
    assert line(ledger, "shadows", "m") == {
        "initial": (3,),
        "sourced": (0,),
        "current": (1,),
        "escaped": (1,),
        "annulled": (0,),
        "absorbed": (0,),
        "absorbed_by_marks": (1,),
        "returned": (0,),
    }
    assert line(ledger, "fields", "m") == {
        "initial": (3,),
        "sourced": (12,),
        "current": (5,),
        "escaped": (1,),
        "annulled": (0,),
        "absorbed": (4,),
        "absorbed_by_marks": (5,),
        "returned": (0,),
    }
    assert all(entry["balanced"] and entry["things_conserved"] for entry in result["ledgers"])
    assert result["contents"] == [2, 4, 4, 4, 4, 4]
    assert result["shadows"] == [3, 3, 3, 2, 1, 1]
    assert result["marks"][0]["counter"] == {"m": 5} and result["marks"][0]["things"] == [2]
    assert result["bodies"][0]["sink"] == {"m": 4}


def test_a_thing_moves_whole_while_its_shadows_spread():
    """(k): a thing is never split; only its shadows spread by the family's table
    (points 2 and 12), and the thing's Node alone publishes events (point 13)."""
    kind, emission, seed = lamp("lamp", 2, (1, 1, 2))
    doc = document(
        ticks=3,
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        shadows=[shadow((4, 2, 2), X, amount=11, owner=1)],
        spread=[6, 1, 1, 1, 1, 1],
        rules=(),
    )
    result = run(doc, 3)
    assert result["contents"] == [2] * 3 and result["shadows"] == [11] * 3
    for tick in range(1, 4):
        thing = rays_at(result["inventories"][tick - 1], (1 + tick, 1, 2))
        assert [(r.detector, r.amount, r.owner, r.steps) for r in thing] == [(BIT_THING, 2, 1, tick)]
    after_1, after_2 = result["inventories"][:2]
    assert [(r.amount, r.detector, r.owner) for r in rays_at(after_1, (5, 2, 2))] == [(6, BIT_SHADOW, 1)]
    assert [(r.amount, HEADINGS[r.heading]) for r in rays_at(after_1, (3, 2, 2))] == [(1, MINUS_X)]
    assert [(r.amount, r.detector, r.owner) for r in rays_at(after_2, (6, 2, 2))] == [(3, BIT_SHADOW, 1)]
    assert all(entry["balanced"] and entry["things_conserved"] for entry in result["ledgers"])
    assert all(entry["shadows"]["m"]["sourced"] == (0,) for entry in result["ledgers"])
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
        shadows=[shadow((5, 1, 2), MINUS_X, owner=3), shadow((5, 3, 2), MINUS_X, owner=3)],
        rules=(TURN | {"momentum_table": {"m": -1}, "reads": reads},),
    )
    result = run(doc, 3)
    pushes = {"content": ((2, 0, 0), (4, 0, 0)), "charge": ((1, 0, 0), (1, 0, 0))}[reads]
    assert result["registers"][1] == {1: [2, 0, 0], 2: [4, 0, 0], 3: [0, 0, 0]}
    assert result["registers"][2] == {
        1: [2 + pushes[0][0], 0, 0],
        2: [4 + pushes[1][0], 0, 0],
        3: [0, 0, 0],
    }
    for y, push in ((1, pushes[0]), (3, pushes[1])):
        rays = rays_at(result["inventories"][2], (4, y, 2))
        assert sorted((r.detector, r.owner, r.momentum, r.outbound, r.steps) for r in rays) == [
            (BIT_SHADOW, 3, (-push[0], 0, 0), 0, 2),
            (BIT_THING, y // 2 + 1, (push[0], 0, 0), 1, 3),
        ]
    assert all(entry["balanced"] and entry["things_conserved"] for entry in result["ledgers"])
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
                {"position": [4, 2, 2], "setting": [1, 1], "seed": 0, "on_bit_1": "draw"}
            ),
            "bit-law-v1",
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
