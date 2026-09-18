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

Re-pinned on 2026-09-18 under the Node's mixing (node-mixing-v1, Highlights
5.4 point 24, feature 16c): no split table is declared, the parked unit is
ninths, and a lone shadow mixes at every Node it reaches with nothing else
there (a lone quantum parks and goes nowhere), so a shadow that is to reach a
mark or a body leaves fresh (`steps` 0) from the Node beside it: (a) reads the
mixing's integers (5 on +X: 2 back, 5 ninths parked on +X and each transverse
heading, 2 on -X); (b) and (d) have M2 at (1,1,1) and the shadow fresh from
the thing's seed Node (2,1,1), its one step spent there, where the trace is;
(c) has the mark beside P0 and the shadow fresh from P0, home every second
tick; (g) has the shadow fresh from (5,2,2), returned and waiting there.
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
    """(a): a spread leaving parts below one quantum parks them as bit-0 rays at rest,
    in ninths (node-mixing-v1), the books counting them as shadow content; the
    engine and the dense layer agree."""
    results = []
    for dense in (False, None):
        doc = document(
            ticks=3,
            families=[family()],
            shadows=[shadow((4, 2, 2), X, amount=5, owner=2, steps=1)],
            dense=dense,
        )
        results.append(run(doc, 3))
    sparse, dense = results
    for result in results:
        # Tick 1: 5 on +X at (4,2,2) mixes, 45 ninths shared 4 : 1 x 5: 2 leave
        # back on -X, 2 ninths park there and 5 on each other heading (27 = 3
        # quanta); tick 2: the 2 at (3,2,2) park whole, 8 ninths on +X, 2 on each
        # other heading (18 = 2 quanta).
        assert rays_at(result["rays"][0], (3, 2, 2)) == rays_at(sparse["rays"][0], (3, 2, 2))
        assert [
            (r.amount, r.owner, r.detector, r.steps) for r in rays_at(result["rays"][0], (3, 2, 2))
        ] == [(2, 2, BIT_SHADOW, 1)]
        assert parked_at(result["parked"][0], (4, 2, 2)) == sorted(
            [(X, 5), (MINUS_X, 2), (Y, 5), (MINUS_Y, 5), ([0, 0, 1], 5), ([0, 0, -1], 5)]
        )
        assert parked_at(result["parked"][1], (3, 2, 2)) == sorted(
            [(X, 8), (MINUS_X, 2), (Y, 2), (MINUS_Y, 2), ([0, 0, 1], 2), ([0, 0, -1], 2)]
        )
        assert not any(any(node) for node in result["rays"][1].values())
        for tick in range(3):
            assert sum(a for _, a in parked_at(result["parked"][tick], (4, 2, 2))) == 27
        at_rest = [r for node in result["parked"][2].values() for rays in node for r in rays]
        assert at_rest and all(
            r.parked == 1
            and r.detector == BIT_SHADOW
            and r.steps == 0
            and r.outbound == 1
            and r.owner == 2
            for r in at_rest
        )
        assert all(0 < r.amount < 9 for r in at_rest)
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
            (e["unit"], e["bit"], e["owner"], e["sign"], e["family"]) == (9, 0, 2, -1, "m")
            for e in entries
        )
    assert sparse["ledgers"] == dense["ledgers"]
    assert sparse["rays"] == dense["rays"] and sparse["parked"] == dense["parked"]
    assert sparse["snapshot"]["parked"] == dense["snapshot"]["parked"]


def m8_document(ticks=6):
    """M8: thing e (content 4) at (2,1,1) heading +X, marks M at (5,1,1) and M2 at
    (1,1,1), a shadow of e leaving fresh from (2,1,1) heading -X (re-pinned
    2026-09-18, node-mixing-v1: it reaches M2 in the first delivery and spends its
    one step back at (2,1,1), where the trace is); no momentum field, so the lamp
    holds nothing once it has emitted."""
    kind, emission, seed = lamp("e", 4, (2, 1, 1), momentum=False)
    return document(
        ticks=ticks,
        shape=(7, 3, 3),
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        marks=[{"position": [5, 1, 1], "setting": [1, 1]}, {"position": [1, 1, 1], "setting": [1, 1]}],
        shadows=[shadow((2, 1, 1), MINUS_X, owner=1, steps=0)],
        momentum=False,
    )


def test_a_prefilled_shadow_of_a_loop_is_absorbed_and_re_released():
    """(c), M9: the E5 unit square ring with a shadow of corner_0_r's thing (id 1)
    leaving fresh from P0 on -X (re-pinned 2026-09-18, node-mixing-v1: a shadow
    two Links out would mix and park); a mark beside P0 at (4,5,5) returns it; it
    reaches P0 with its step spent as thing 1's ray is there, is absorbed
    (`returned` momentum (0,0,0) exact) and leaves again reversed, every second
    tick; the ring is untouched."""
    doc = ring_document(PORT_CORNER, ticks=8)
    doc["detectors"] = [{"position": [4, 5, 5], "setting": [1, 1]}]
    doc["initial_field"] = {"electron": {"rays": [shadow((5, 5, 5), MINUS_X, owner=1, steps=0)]}}
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
    # The walk: returned by the mark after tick 1 as it is (return-field-v1: an
    # outgoing share, fresh); home at P0 after tick 2; re-released on -X into
    # the mark again, returned, home again.
    for tick, (position, outbound, steps, heading) in {
        1: ((4, 5, 5), 1, 0, X),
        2: ((5, 5, 5), 1, 1, X),
        3: ((4, 5, 5), 1, 0, X),
        4: ((5, 5, 5), 1, 1, X),
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
        (tick, (5, 5, 5), {"electron": {"amount": 1, "momentum": (0, 0, 0)}}) for tick in (2, 4, 6)
    ]
    assert not {"shadow_return", "shadow_absorbed", "ray_push"} & set(event_kinds(events))


def test_the_record_carries_the_fixed_terms_and_no_register_counter_or_seed(tmp_path):
    """(d), M13: the runner's record of the M8 world: state.json lists no parked
    shadow (a Node remembers no departure, return-field-v1, and nothing has
    mixed after one tick); run.json records `momentum` per tick, the residents
    and the identity; no key of the retired stores anywhere."""
    path = tmp_path / "m8.json"
    path.write_text(json.dumps(m8_document(1)), encoding="utf-8")
    run_initialization(path, tmp_path / "m8", ticks=1)
    state = json.loads((tmp_path / "m8" / "state.json").read_text(encoding="utf-8"))
    metadata = json.loads((tmp_path / "m8" / "run.json").read_text(encoding="utf-8"))
    assert state["parked"] == []
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
        "trace",
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
    shadow of another owner, leaving fresh from (5,2,2) (re-pinned 2026-09-18,
    node-mixing-v1), is returned without a push as it is (return-field-v1) and
    mixes at (5,2,2), where its ninths park."""
    kind, emission, seed = lamp("lamp", 2, (1, 2, 2))
    doc = document(
        ticks=8,
        types=[kind],
        emissions=[emission],
        seeds=[seed],
        families=[family(), family("wall", charge=0)],
        bodies=[
            # A body under a table takes the recoil on its own line (the cleanup of
            # 2026-09-18): the wall is heavy, 4096, so the 4 it takes moves it nowhere.
            {"position": [6, 2, 2], "family": "wall", "amount": 4096, "coupling": "mirror", "thing": 3}
        ],
        shadows=[shadow((5, 2, 2), X, owner=2, steps=0)],
        rules=(MIRROR,),
    )
    doc["fields"].append(field("wall"))
    result = run(doc, 8)
    # The shadow: returned by the body after tick 1 (no push: the body names no
    # family), back with its step and at rest at (5,2,2) from tick 2 on.
    # Re-pinned 2026-09-18 (return-field-v1): returned as it is, an outgoing
    # share fresh at (6,2,2), it arrives at (5,2,2) after tick 2, mixes there in
    # the cycle of tick 3 and parks its ninths, 4 back on +X and 1 each other way.
    for tick, (position, steps, heading) in {
        1: ((6, 2, 2), 0, MINUS_X),
        2: ((5, 2, 2), 1, MINUS_X),
    }.items():
        (walker,) = [
            r
            for r in rays_at(result["rays"][tick - 1], position)
            if r.detector == BIT_SHADOW and not r.parked
        ]
        assert (
            walker.outbound,
            walker.steps,
            HEADINGS[walker.heading],
            walker.momentum,
            walker.owner,
        ) == (
            1,
            steps,
            heading,
            None,
            2,
        )
    for tick in (3, 8):
        assert not [
            r
            for r in rays_at(result["rays"][tick - 1], (5, 2, 2))
            if r.detector == BIT_SHADOW and not r.parked
        ]
        assert parked_at(result["parked"][tick - 1], (5, 2, 2)) == sorted(
            [(X, 4), (MINUS_X, 1), (Y, 1), (MINUS_Y, 1), ([0, 0, 1], 1), ([0, 0, -1], 1)]
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
    # A body under a table takes the recoil on its own line (the cleanup of
    # 2026-09-18): the thing of 2 reversed from +X to -X lost 4 on X, the wall
    # took 4 in the cycle of tick 5, on its momentum line, beside the identity
    # (the momentum field's `returned` line, nothing sourced); heavy, it stays.
    assert result["bodies"][0]["momentum"] == [4, 0, 0]
    assert [m.get(3) for m in result["momentum"]] == [[0, 0, 0]] * 5 + [[4, 0, 0]] * 3
    assert result["contents"] == [2] * 8 and result["shadows"] == [1] * 8
    for tick, ledger in enumerate(result["ledgers"], start=1):
        assert ledger["balanced"] and ledger["real_conserved"]
        assert ledger["fields"]["m"]["absorbed"] == (0,)
        assert ledger["fields"]["momentum"]["sourced"] == (0, 0, 0)
        assert ledger["fields"]["momentum"]["returned"] == ((4, 0, 0) if tick >= 6 else (0, 0, 0))
        assert line(ledger, "shadow", "m") == {
            "initial": (1,),
            "current": (1,),
            "escaped": (0,),
            "absorbed_at_home": (0,),
        }
