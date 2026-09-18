"""A Node is its six Ports; everything else is a ray (node-is-ports-v1; Highlights
5.4 point 22 and the five settled rules, the model owner's decision of
2026-09-18; feature 17 of issue #169).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A Node is its six
Ports") before the first run. What a Node holds below one quantum is a parked
shadow, a bit-0 ray at rest in units of the split's denominator, the books
counting it as shadow content (a); what a Node remembers of a departure is a
zero-amount shadow on the heading the thing left by, and a return whose steps
are spent follows it (b, M8); a click is an absorption into the thing resident
at the mark, and a shadow home to that resident is counted on its shadows line
without an event (b, M8); a prefilled shadow of a loop starts its Link
distance from its owner's Node away and is absorbed and re-released with the
`returned` momentum exact (c, M9); the record's fixed terms are bit and owner,
with no register, counter, seed or trace key (d, M13); a seeded thing missed
at a mark walks back to its seed Node and leaves again on its original heading
(e, M14); a source is a thing that spends its content, nothing sourced (f); a
mirror is a thing with a declared table that returns a thing and a shadow (g).
"""

import json
from copy import deepcopy

from event_universe import Simulation
from event_universe.core.spatial_state import BIT_SHADOW, BIT_THING, NODE_IS_PORTS
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_loop_binding import CORNERS, PORT_CORNER
from .test_loop_binding import document as ring_document

HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
COSTS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
X, MINUS_X, Y, MINUS_Y = [1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]
CYCLE_RECORDS = {"cycle_started", "cycle_committed", "spatial_cycle", "spatial_received", "spatial_sent"}


def field(name, components=1):
    return {
        "name": name,
        "components": components,
        "units": "quantum",
        "signed": components == 3,
        "conserved": True,
        "extensive": True,
    }


def family(name="m", spread=None, charge=-1):
    entry = {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 8,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": 0,
        "charge": charge,
        "release": [1, 1],
    }
    if spread is not None:
        entry["spread"] = spread
    return entry


def lamp(name, amount, position, heading=X, per_interval=None, momentum=True, family_name="m"):
    """A thing that spends its content (node-is-ports-v1): a type holding its
    content and, when the world has one, the momentum field; an emission rule."""
    fields = [family_name] + (["momentum"] if momentum else [])
    kind = {
        "name": name,
        "fields": fields,
        "defaults": {family_name: amount} | ({"momentum": [0, 0, 0]} if momentum else {}),
        "transport": {"mode": "hold"},
    }
    emission = {
        "type": name,
        "field": family_name,
        "amount": amount if per_interval is None else per_interval,
        "denominator": 1,
        "heading": heading,
        "kerengonen_phase": 0,
    }
    return kind, emission, {"position": list(position), "type": name}


def shadow(position, heading, amount=1, owner=1, sign=-1, steps=None):
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


def document(
    *,
    ticks,
    shape=(10, 5, 5),
    types=(),
    emissions=(),
    seeds=(),
    bodies=(),
    marks=(),
    shadows=(),
    families=None,
    momentum=True,
    dense=None,
    rules=(),
):
    doc = {
        "schema_version": 1,
        "model_id": "node-is-ports-test-v1",
        "shape": list(shape),
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": dict.fromkeys(COSTS, 1),
        "fields": [field("m")] + ([field("momentum", 3)] if momentum else []),
        "disturbance_types": list(types)
        or [{"name": "ring", "fields": ["m"], "defaults": {"m": 4}, "transport": {"mode": "hold"}}],
        "spatial_fields": list(families) if families is not None else [family()],
        "emissions": list(emissions),
        "seeds": list(seeds),
        "ray_interactions": [deepcopy(rule) for rule in rules],
        "external_bodies": list(bodies),
        "detectors": list(marks),
    }
    if shadows:
        doc["initial_field"] = {"m": {"rays": list(shadows)}}
    if dense is not None:
        doc["dense_field"] = dense
    return doc


def run(doc, ticks):
    """Per tick the ledger, the things' and the shadows' content, the momentum of
    every thing, the rays on their way and the parked shadows per Node; the
    events; the marks, bodies and snapshot at the end."""
    events = []
    ledgers, contents, shadows, momentum, rays, parked = [], [], [], [], [], []
    with Simulation(parse_initial_state(doc), observer=events.append) as world:
        for _ in range(ticks):
            world.step()
            ledgers.append(world.audit())
            contents.append(world.real_content())
            shadows.append(world.shadow_content())
            momentum.append(world.thing_momentum())
            view = world.inventory_view()
            rays.append({node.position: node.rays for node in view.nodes if any(node.rays)})
            parked.append({node.position: node.parked for node in view.nodes if any(node.parked)})
        marks = world.detector_marks()
        bodies = world.external_bodies()
        snapshot = world.snapshot()
    return {
        "events": events,
        "ledgers": ledgers,
        "contents": contents,
        "shadows": shadows,
        "momentum": momentum,
        "rays": rays,
        "parked": parked,
        "marks": marks,
        "bodies": bodies,
        "snapshot": snapshot,
    }


def rays_at(rays, position, index=0):
    return rays.get(tuple(position), ((),))[index]


def parked_at(parked, position, index=0):
    """(heading, amount) of every parked shadow of a Node, in heading order."""
    return sorted((HEADINGS[r.heading], r.amount) for r in parked.get(tuple(position), ((),))[index])


def event_kinds(events):
    result = {}
    for event in events:
        if event["event"] not in CYCLE_RECORDS:
            result[event["event"]] = result.get(event["event"], 0) + 1
    return result


def line(ledger, readout, name):
    return {k: v for k, v in ledger[readout][name].items() if k != "balanced"}


def keys_of(value, found=None):
    found = set() if found is None else found
    if isinstance(value, dict):
        for key, item in value.items():
            found.add(key)
            keys_of(item, found)
    elif isinstance(value, list):
        for item in value:
            keys_of(item, found)
    return found


def test_a_share_below_one_quantum_is_a_parked_shadow():
    """(a): a split leaving parts below one quantum parks them as bit-0 rays at rest,
    in units of the table's total, the books counting them as shadow content;
    the engine and the dense layer agree."""
    results = []
    for dense in (False, None):
        doc = document(
            ticks=3,
            families=[family(spread=[6, 1, 1, 1, 1, 1])],
            shadows=[shadow((4, 2, 2), X, amount=5, owner=2, steps=1)],
            dense=dense,
        )
        results.append(run(doc, 3))
    sparse, dense = results
    for result in results:
        # Tick 1: 5 on +X at (4,2,2) split 30/11, 5/11 x 5: 2 leave forward, 8 and
        # five 5s park (33 = 3 quanta); tick 2: the 2 at (5,2,2) leave 1 and park 11.
        assert rays_at(result["rays"][0], (5, 2, 2)) == rays_at(sparse["rays"][0], (5, 2, 2))
        assert [
            (r.amount, r.owner, r.detector, r.steps) for r in rays_at(result["rays"][0], (5, 2, 2))
        ] == [(2, 2, BIT_SHADOW, 1)]
        assert parked_at(result["parked"][0], (4, 2, 2)) == sorted(
            [(X, 8), (MINUS_X, 5), (Y, 5), (MINUS_Y, 5), ([0, 0, 1], 5), ([0, 0, -1], 5)]
        )
        assert parked_at(result["parked"][1], (5, 2, 2)) == sorted(
            [(X, 1), (MINUS_X, 2), (Y, 2), (MINUS_Y, 2), ([0, 0, 1], 2), ([0, 0, -1], 2)]
        )
        for tick in range(3):
            assert sum(a for _, a in parked_at(result["parked"][tick], (4, 2, 2))) == 33
        at_rest = [r for node in result["parked"][2].values() for rays in node for r in rays]
        assert at_rest and all(
            r.parked == 1
            and r.detector == BIT_SHADOW
            and r.steps == 0
            and r.outbound == 1
            and r.owner == 2
            for r in at_rest
        )
        assert all(0 < r.amount < 11 for r in at_rest)
        # The books: five quanta of shadow content at every tick, nothing sourced.
        assert result["shadows"] == [5, 5, 5] and result["contents"] == [0, 0, 0]
        for ledger in result["ledgers"]:
            assert ledger["balanced"] and ledger["real_conserved"]
            assert ledger["fields"]["m"]["current"] == (5,) and ledger["fields"]["m"]["sourced"] == (0,)
            assert line(ledger, "shadow", "m") == {
                "initial": (5,),
                "current": (5,),
                "escaped": (0,),
                "absorbed_at_home": (0,),
            }
        assert not event_kinds(result["events"])
        entries = [e for e in result["snapshot"]["parked"] if tuple(e["position"]) == (4, 2, 2)]
        assert sorted((e["heading"], e["amount"]) for e in entries) == parked_at(
            result["parked"][2], (4, 2, 2)
        )
        assert all(
            (e["unit"], e["bit"], e["owner"], e["sign"], e["family"]) == (11, 0, 2, -1, "m")
            for e in entries
        )
    assert sparse["ledgers"] == dense["ledgers"]
    assert sparse["rays"] == dense["rays"] and sparse["parked"] == dense["parked"]
    assert sparse["snapshot"]["parked"] == dense["snapshot"]["parked"]


def m8_document(ticks=6):
    """M8: thing e (content 4) at (2,1,1) heading +X, marks M at (5,1,1) and M2 at
    (0,1,1), a shadow of e at (1,1,1) heading -X; no momentum field, so the lamp
    holds nothing once it has emitted."""
    kind, emission, seed = lamp("e", 4, (2, 1, 1), momentum=False)
    return document(
        ticks=ticks,
        shape=(7, 3, 3),
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        marks=[{"position": [5, 1, 1], "setting": [1, 1]}, {"position": [0, 1, 1], "setting": [1, 1]}],
        shadows=[shadow((1, 1, 1), MINUS_X, owner=1)],
        momentum=False,
    )


def test_the_trace_is_a_zero_amount_shadow_and_the_mark_is_the_home_of_what_it_absorbed():
    """(b), M8: the thing leaves a zero-amount shadow on +X at every Node it departs;
    the shadow, returned by M2, spends its steps at (2,1,1), follows the traces to
    M and is absorbed into the resident thing on its shadows line, no click, no
    event; the resident's things 4 / shadows 1."""
    result = run(m8_document(), 6)
    # The traces: thing 1 left (2,1,1) at tick 0, (3,1,1) at tick 1, (4,1,1) at tick 2.
    assert parked_at(result["parked"][0], (2, 1, 1)) == [(X, 0)]
    assert parked_at(result["parked"][1], (3, 1, 1)) == [(X, 0)]
    assert parked_at(result["parked"][2], (4, 1, 1)) == [(X, 0)]
    assert (5, 1, 1) not in result["parked"][5]
    trace = result["parked"][0][(2, 1, 1)][0][0]
    assert (trace.parked, trace.amount, trace.detector, trace.owner, trace.outbound, trace.steps) == (
        1,
        0,
        BIT_SHADOW,
        1,
        1,
        0,
    )
    # The shadow: returned at M2 after tick 1, its steps spent at (2,1,1) after
    # tick 3, following the traces through (3,1,1) and (4,1,1), home at M after tick 6.
    walk = {
        1: ((0, 1, 1), 2, X),
        2: ((1, 1, 1), 1, X),
        3: ((2, 1, 1), 0, X),
        4: ((3, 1, 1), 0, X),
        5: ((4, 1, 1), 0, X),
    }
    for tick, (position, steps, heading) in walk.items():
        (walker,) = rays_at(result["rays"][tick - 1], position)
        assert (
            walker.detector,
            walker.outbound,
            walker.steps,
            HEADINGS[walker.heading],
            walker.owner,
        ) == (
            BIT_SHADOW,
            0,
            steps,
            heading,
            1,
        )
    assert not any(any(node) for node in result["rays"][5].values())
    # One click, the thing's, and no event for the shadow home (settled rule (iv)).
    assert event_kinds(result["events"]) == {"detector_click": 1}
    clicks = [e for e in result["events"] if e["event"] == "detector_click"]
    assert (
        clicks[0]["tick"],
        tuple(clicks[0]["position"]),
        clicks[0]["absorbed"],
        clicks[0]["owner"],
    ) == (
        3,
        (5, 1, 1),
        4,
        1,
    )
    assert result["marks"] == [
        {
            "position": [5, 1, 1],
            "resident": {"real": {"m": 4}, "shadow": {"m": 1}, "momentum": [4, 0, 0], "owners": [1]},
        },
        {
            "position": [0, 1, 1],
            "resident": {"real": {}, "shadow": {}, "momentum": [0, 0, 0], "owners": []},
        },
    ]
    assert result["contents"] == [4, 4, 0, 0, 0, 0] and result["shadows"] == [1, 1, 1, 1, 1, 0]
    for tick, ledger in enumerate(result["ledgers"], start=1):
        assert ledger["balanced"] and ledger["real_conserved"]
        assert line(ledger, "real", "m") == {
            "initial": (4,),
            "converted": (0,),
            "current": (0,) if tick >= 3 else (4,),
            "escaped": (0,),
            "absorbed": (4,) if tick >= 3 else (0,),
        }
        assert line(ledger, "shadow", "m") == {
            "initial": (1,),
            "current": (0,) if tick >= 6 else (1,),
            "escaped": (0,),
            "absorbed_at_home": (1,) if tick >= 6 else (0,),
        }
        assert ledger["fields"]["m"]["absorbed_by_marks"] == (
            (5,) if tick >= 6 else (4,) if tick >= 3 else (0,)
        )
    assert result["ledgers"][5]["marks"] == {
        "count": 2,
        "momentum": (4, 0, 0),
        "real": {"m": (4,)},
        "shadow": {"m": (1,)},
    }


def test_a_prefilled_shadow_of_a_loop_is_absorbed_and_re_released():
    """(c), M9: the E5 unit square ring with a shadow of corner_0_r's thing (id 1)
    two Links from P0 on its line; a mark at (2,5,5) returns it; it reaches P0
    with its steps spent as thing 1's ray is there, is absorbed (`returned`
    momentum (0,0,0) exact) and leaves again reversed; the ring is untouched."""
    doc = ring_document(PORT_CORNER, ticks=8)
    doc["detectors"] = [{"position": [2, 5, 5], "setting": [1, 1]}]
    doc["initial_field"] = {"electron": {"rays": [shadow((3, 5, 5), MINUS_X, owner=1)]}}
    events = []
    with Simulation(parse_initial_state(doc), observer=events.append) as world:
        seen = []
        for tick in range(1, 9):
            world.step()
            assert world.totals()["electron"] == (9,)
            assert world.real_content() == 8 and world.shadow_content() == 1
            ledger = world.audit()
            assert ledger["balanced"] and ledger["real_conserved"]
            assert ledger["fields"]["momentum"]["returned"] == (0, 0, 0)
            assert ledger["fields"]["electron"]["sourced"] == (0,)
            view = world.inventory_view()
            found = {
                node.position: [r for r in node.rays[0] if r.detector == BIT_SHADOW]
                for node in view.nodes
                if node.rays and any(r.detector == BIT_SHADOW for r in node.rays[0])
            }
            seen.append(found)
            if tick >= 2:
                for corner in CORNERS:
                    things = [r for node in view.nodes if node.position == corner for r in node.rays[0]]
                    assert sum(r.amount for r in things if r.detector == BIT_THING) == 2
    # The walk: steps 2 at (3,5,5) (rule (ii)); returned by the mark after tick 1
    # with steps 3; home at P0 after tick 4; re-released on -X, at (4,5,5) after tick 5.
    for tick, (position, outbound, steps, heading) in {
        1: ((2, 5, 5), 0, 3, X),
        2: ((3, 5, 5), 0, 2, X),
        3: ((4, 5, 5), 0, 1, X),
        4: ((5, 5, 5), 0, 0, X),
        5: ((4, 5, 5), 1, 1, MINUS_X),
        6: ((3, 5, 5), 1, 2, MINUS_X),
    }.items():
        (walker,) = seen[tick - 1][position]
        assert (
            walker.outbound,
            walker.steps,
            HEADINGS[walker.heading],
            walker.owner,
            walker.amount,
        ) == (
            outbound,
            steps,
            heading,
            1,
            1,
        )
    homes = [e for e in events if e["event"] == "spatial_cycle" and e.get("returned")]
    assert [(e["tick"], tuple(e["position"]), e["returned"]) for e in homes] == [
        (4, (5, 5, 5), {"electron": {"amount": 1, "momentum": (0, 0, 0)}})
    ]
    assert not {"shadow_return", "shadow_absorbed", "ray_push"} & set(event_kinds(events))


def test_the_record_carries_the_fixed_terms_and_no_register_counter_or_seed(tmp_path):
    """(d), M13: the runner's record of the M8 world: every parked shadow in
    state.json carries `bit` 0 and its `owner`, the trace as a zero-amount ray at
    (2,1,1) heading +X; run.json records `momentum` per tick, the residents and
    the identity; no key of the retired stores anywhere."""
    path = tmp_path / "m8.json"
    path.write_text(json.dumps(m8_document(1)), encoding="utf-8")
    run_initialization(path, tmp_path / "m8", ticks=1)
    state = json.loads((tmp_path / "m8" / "state.json").read_text(encoding="utf-8"))
    metadata = json.loads((tmp_path / "m8" / "run.json").read_text(encoding="utf-8"))
    assert state["parked"] == [
        {
            "position": [2, 1, 1],
            "family": "m",
            "owner": 1,
            "sign": 0,
            "heading": [1, 0, 0],
            "amount": 0,
            "unit": 1,
            "phase": 0,
            "bit": 0,
        }
    ]
    assert metadata["node_is_ports"] == NODE_IS_PORTS == "node-is-ports-v1"
    assert metadata["bit_law"] == "bit-law-v1"
    assert metadata["momentum"] == [{"1": [4, 0, 0]}]
    assert metadata["detector_marks"][0]["resident"] == {
        "real": {},
        "shadow": {},
        "momentum": [0, 0, 0],
        "owners": [],
    }
    (shadow_family,) = metadata["shadow_families"]
    assert (shadow_family["field"], shadow_family["release"], shadow_family["owners"]) == (
        "m",
        [1, 1],
        [1],
    )
    retired = {
        "registers",
        "register_phases",
        "counter",
        "seed",
        "traces",
        "field_remainders",
        "things_absorbed",
    }
    assert not retired & keys_of(metadata) and not retired & keys_of(state)
    assert metadata["real_content"] == [4] and metadata["shadow_content"] == [1]


def test_a_seeded_thing_missed_at_a_mark_returns_to_its_seed_node_and_leaves_again():
    """(e), M14: thing e (content 4) seeded at (1,1,1) heading +X, a mark at (4,1,1)
    with the table [0, 1]: missed after tick 3, back at its seed Node after tick 6
    with its steps spent, restored to the lamp by the inverse split of a lone
    ray, emitted again on +X in the cycle of tick 7 (settled rule (iii))."""
    kind, emission, seed = lamp("e", 4, (1, 1, 1))
    doc = document(
        ticks=9,
        shape=(9, 3, 3),
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        marks=[{"position": [4, 1, 1], "setting": [0, 1]}],
    )
    result = run(doc, 9)
    walk = {
        1: ((2, 1, 1), 1, 1, X),
        2: ((3, 1, 1), 1, 2, X),
        3: ((4, 1, 1), 0, 3, MINUS_X),
        4: ((3, 1, 1), 0, 2, MINUS_X),
        5: ((2, 1, 1), 0, 1, MINUS_X),
        6: ((1, 1, 1), 0, 0, MINUS_X),
        8: ((2, 1, 1), 1, 1, X),
        9: ((3, 1, 1), 1, 2, X),
    }
    for tick, (position, outbound, steps, heading) in walk.items():
        (thing,) = rays_at(result["rays"][tick - 1], position)
        assert (
            thing.detector,
            thing.outbound,
            thing.steps,
            HEADINGS[thing.heading],
            thing.amount,
            thing.owner,
        ) == (
            BIT_THING,
            outbound,
            steps,
            heading,
            4,
            1,
        )
    # After tick 7 the thing is on the Link out of its seed Node: no ray resident.
    assert not any(any(node) for node in result["rays"][6].values())
    returns = [e for e in result["events"] if e["event"] == "detector_return"]
    assert [(e["tick"], e["amount"], e["owner"]) for e in returns] == [(3, 4, 1)]
    splits = [e for e in result["events"] if e["event"] == "inverse_split"]
    assert [
        (e["tick"], tuple(e["position"]), tuple(e["ports"]), e["amount"], e["restored"]) for e in splits
    ] == [(6, (1, 1, 1), (), 4, True)]
    assert "detector_click" not in event_kinds(result["events"])
    assert result["contents"] == [4] * 9 and result["shadows"] == [0] * 9
    # The momentum line reads the thing's rays: +X out, -X on the walk back, none
    # while the lamp holds it again; every action is a message that returns, so
    # with the lamp's recoil the momentum field's current is zero at every tick.
    assert (
        result["momentum"] == [{1: [4, 0, 0]}] * 2 + [{1: [-4, 0, 0]}] * 4 + [{}] + [{1: [4, 0, 0]}] * 2
    )
    for ledger in result["ledgers"]:
        assert ledger["balanced"] and ledger["real_conserved"]
        assert line(ledger, "real", "m") == {
            "initial": (4,),
            "converted": (0,),
            "current": (4,),
            "escaped": (0,),
            "absorbed": (0,),
        }
        assert ledger["fields"]["momentum"]["current"] == (0, 0, 0)


def test_a_source_is_a_thing_that_spends_its_content():
    """(f): a lamp holding 6 emits 2 per interval and burns out after three; nothing
    is sourced, the things' content is constant and the thing's momentum, the
    lamp's recoil with its rays', stays zero; a lamp without content emits nothing."""
    kind, emission, seed = lamp("lamp", 6, (1, 2, 2), per_interval=2)
    doc = document(ticks=4, types=[kind], emissions=[emission], seeds=[seed])
    result = run(doc, 4)
    stocks = []
    for tick in range(1, 5):
        positions = sorted(result["rays"][tick - 1])
        assert positions == [(1 + k, 2, 2) for k in range(max(1, tick - 2), tick + 1)]
        for position in positions:
            (ray,) = rays_at(result["rays"][tick - 1], position)
            assert (ray.detector, ray.amount, ray.owner, ray.outbound) == (BIT_THING, 2, 1, 1)
    with Simulation(parse_initial_state(doc)) as world:
        for _ in range(4):
            world.step()
            (record,) = [r for node in world.nodes.values() for r in node.records if r is not None]
            stocks.append(world.record_values(record)["m"][0])
            assert world.source_totals() == {"m": (0,), "momentum": (0, 0, 0)}
    assert stocks == [4, 2, 0, 0]
    assert result["contents"] == [6] * 4 and result["shadows"] == [0] * 4
    # The momentum line reads the thing's rays, two quanta on +X each; the lamp's
    # recoil, on its momentum field, balances the world's momentum line to zero.
    assert result["momentum"] == [{1: [2 * k, 0, 0]} for k in (1, 2, 3, 3)]
    for ledger in result["ledgers"]:
        assert ledger["balanced"] and ledger["real_conserved"]
        assert ledger["fields"]["m"]["sourced"] == (0,)
        assert ledger["fields"]["momentum"]["current"] == (0, 0, 0)
        assert line(ledger, "real", "m") == {
            "initial": (6,),
            "converted": (0,),
            "current": (6,),
            "escaped": (0,),
            "absorbed": (0,),
        }
        assert "sourced" not in ledger["real"]["m"] and "sourced" not in ledger["shadow"]["m"]
    empty_kind, empty_emission, empty_seed = lamp("lamp", 0, (1, 2, 2), per_interval=2)
    empty = run(document(ticks=3, types=[empty_kind], emissions=[empty_emission], seeds=[empty_seed]), 3)
    assert empty["contents"] == [0] * 3 and all(
        not any(node) for rays in empty["rays"] for node in rays.values()
    )


MIRROR = {
    "name": "mirror",
    "participants": [{"type": "m"}, {"type": "wall"}],
    "outputs": [
        {"field": "m", "amount": {"of": 0}, "heading": "reversed", "input": 0, "phase": {"of": 0}},
        {"field": "wall", "amount": {"of": 1}, "heading": "same", "input": 1, "phase": {"of": 1}},
    ],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}


def test_a_mirror_is_a_thing_with_a_declared_table_that_returns_a_thing_and_a_shadow():
    """(g): a body of the apparatus family at (6,2,2) under the mirror table: the
    thing that reaches it leaves reversed as a fresh event, still a thing; a
    shadow of another owner is returned on its steps without a push and, its
    steps spent with no trace to follow, waits at (4,2,2) for a thing of its
    owner (settled rule (ii))."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=8,
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        families=[family(), family("wall", charge=0)],
        bodies=[
            {"position": [6, 2, 2], "family": "wall", "amount": 1, "coupling": "mirror", "thing": 3}
        ],
        shadows=[shadow((5, 2, 2), X, owner=2, steps=1)],
        rules=(MIRROR,),
    )
    doc["fields"].append(field("wall"))
    result = run(doc, 8)
    # The shadow: returned by the body after tick 1 (no push: the body names no
    # family), back with its steps and at rest at (4,2,2) from tick 3 on.
    for tick, (position, steps) in {
        1: ((6, 2, 2), 2),
        2: ((5, 2, 2), 1),
        3: ((4, 2, 2), 0),
        8: ((4, 2, 2), 0),
    }.items():
        (walker,) = [r for r in rays_at(result["rays"][tick - 1], position) if r.detector == BIT_SHADOW]
        assert (
            walker.outbound,
            walker.steps,
            HEADINGS[walker.heading],
            walker.momentum,
            walker.owner,
        ) == (
            0,
            steps,
            MINUS_X,
            None,
            2,
        )
    # The thing: at the mirror after tick 5, reversed in that cycle as a fresh
    # event, a thing of the lamp's identity walking -X from tick 6.
    for tick, position in {4: (5, 2, 2), 6: (5, 2, 2), 7: (4, 2, 2)}.items():
        (thing,) = [r for r in rays_at(result["rays"][tick - 1], position) if r.detector == BIT_THING]
        assert (thing.amount, thing.owner, thing.outbound, HEADINGS[thing.heading]) == (
            2,
            1,
            1,
            X if tick < 5 else MINUS_X,
        )
        assert thing.steps == (tick if tick < 5 else tick - 5)
    assert not {"external_body_absorbed", "ray_push", "shadow_absorbed", "detector_click"} & set(
        event_kinds(result["events"])
    )
    assert result["bodies"][0]["sink"] == {} and result["bodies"][0]["position"] == [6, 2, 2]
    assert result["contents"] == [2] * 8 and result["shadows"] == [1] * 8
    for ledger in result["ledgers"]:
        assert ledger["balanced"] and ledger["real_conserved"]
        assert ledger["fields"]["m"]["absorbed"] == (0,)
        assert line(ledger, "shadow", "m") == {
            "initial": (1,),
            "current": (1,),
            "escaped": (0,),
            "absorbed_at_home": (0,),
        }
