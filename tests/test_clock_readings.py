"""The clock is the content, the two readings, the decay table (clock-readings-v1;
Highlights 5.4 points 11, 16, 18, 19 and 20, the model owner's decisions of
2026-09-18; feature 16b). A thing of a family that declares `clock` advances its
phase by content / K steps per interval, K the world's one integer, the
remainder kept exactly on the thing; a shadow has no clock; the world's
computation per tick is the things' phase steps and is constant between
absorptions (a); two contents are two clocks and a shadow keeps the phase it was
given (b); K and N bound the content one Node may hold, at parsing and at a
meeting (c); a neutral thing has gravity and no electric push, and a charged
thing's electric push below one quantum accumulates exactly on its remainder,
the same shadow read twice (d); a bound group breaks by its declared decay table,
never by a draw, byte-identically across runs (e). The step of a thing and one
Link per interval through every push are pinned in test_ray_momentum_turn.py,
the wait per quantum read in test_wait_rule.py.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The clock and the
readings") before the first run.
"""

import json
from copy import deepcopy

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import BIT_SHADOW, BIT_THING
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

from .test_bit_law import COSTS, HEADINGS, MINUS_X, X, field, kinds, rays_at
from .test_loop_binding import CORNERS, P0, P1, P2, P3, PORT_CORNER, state
from .test_loop_binding import document as ring_document

PLUS_Y = [0, 1, 0]


def family(name, charge=0, clock=False):
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
    if clock:
        entry["clock"] = True
    return entry


def lamp(name, family_name, amount, position, heading=X, phase=0):
    kind = {
        "name": name,
        "fields": [family_name, "momentum"],
        "defaults": {family_name: amount, "momentum": [0, 0, 0]},
        "transport": {"mode": "hold"},
    }
    emission = {
        "type": name,
        "field": family_name,
        "amount": amount,
        "denominator": 1,
        "heading": heading,
        "kerengonen_phase": phase,
    }
    return kind, emission, {"position": list(position), "type": name}


def shadow(position, heading, owner, amount=1, phase=0, sign=-1):
    return {
        "position": list(position),
        "heading": list(heading),
        "amount": amount,
        "owner": owner,
        "sign": sign,
        "phase": phase,
        "steps": 0,
    }


def push(name, table, reads, participants):
    return {
        "name": name,
        "participants": participants,
        "momentum_table": table,
        "reads": reads,
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


def document(*, families, lamps, shape, ticks, K, shadows=None, marks=(), rules=(), bodies=()):
    """A board of open boundary; `lamps` are (kind, emission, seed) triples."""
    doc = {
        "schema_version": 1,
        "N": 8,
        "model_id": "clock-readings-test-v1",
        "shape": list(shape),
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "K": K,
        "wait_per_quantum": 0,
        "operation_costs": dict.fromkeys(COSTS, 1),
        "fields": [field(entry["field"]) for entry in families] + [field("momentum", 3)],
        "disturbance_types": [kind for kind, _, _ in lamps],
        "spatial_fields": list(families),
        "emissions": [emission for _, emission, _ in lamps],
        "seeds": [seed for _, _, seed in lamps],
        "ray_interactions": list(rules),
        "external_bodies": list(bodies),
        "detectors": list(marks),
    }
    if shadows:
        doc["initial_field"] = {name: {"rays": rays} for name, rays in shadows.items()}
    return doc


def run(doc, ticks):
    events = []
    steps, contents, inventories, momentum = [], [], [], []
    with Simulation(parse_initial_state(doc), observer=events.append) as world:
        for _ in range(ticks):
            world.step()
            steps.append(world.phase_steps())
            contents.append(world.real_content())
            momentum.append(world.thing_momentum())
            inventories.append(
                {node.position: node.rays for node in world.inventory_view().nodes if any(node.rays)}
            )
            assert world.audit()["balanced"]
    return {
        "events": events,
        "steps": steps,
        "contents": contents,
        "momentum": momentum,
        "inventories": inventories,
    }


def things_at(inventory, position, index=0):
    return [r for r in rays_at(inventory, position, index) if r.detector == BIT_THING]


def shadows_at(inventory, position, index=0):
    return [r for r in rays_at(inventory, position, index) if r.detector == BIT_SHADOW]


def test_the_computation_is_the_things_phase_steps_and_is_constant_between_absorptions(tmp_path):
    """(a) 9 x 3 x 3, K 2: a thing e of 6 (three steps per interval) and a thing f
    of 2 (one), a mark at (5, 2, 1) on f's line, three shadows of e adding
    nothing: the computation reads 4 per tick until f is absorbed on its arrival
    at the mark after tick 4 (its step of that interval counted), 3 until e
    leaves the board on its departure of tick 8 (counted), 0 after."""
    m = family("m", charge=-1, clock=True)
    e = lamp("e", "m", 6, (1, 1, 1))
    f = lamp("f", "m", 2, (1, 2, 1))
    doc = document(
        families=[m],
        lamps=[e, f],
        shape=(9, 3, 3),
        ticks=10,
        K=2,
        shadows={"m": [shadow((x, 1, 2), X, 1) for x in (1, 2, 3)]},
        marks=[{"position": [5, 2, 1], "setting": [1, 1]}],
    )
    result = run(doc, 10)
    totals = result["steps"]
    per_tick = [after - before for before, after in zip([0] + totals[:-1], totals, strict=True)]
    assert per_tick == [4, 4, 4, 4, 3, 3, 3, 3, 0, 0]
    assert result["contents"] == [8, 8, 8, 6, 6, 6, 6, 0, 0, 0]
    bare = deepcopy(doc)
    del bare["initial_field"]
    assert run(bare, 10)["steps"] == totals
    source = tmp_path / "world.json"
    source.write_text(json.dumps(doc))
    run_initialization(source, tmp_path / "out")
    metadata = json.loads((tmp_path / "out" / "run.json").read_text())
    assert metadata["computation_per_tick"] == per_tick
    assert metadata["real_content"] == result["contents"]
    assert metadata["clock_readings"] == "clock-readings-v1" and metadata["K"] == 2
    assert metadata["wait_per_quantum"] == [0, 1]


def test_a_shadow_has_no_clock_and_two_contents_are_two_clocks():
    """(b) 9 x 3 x 3, K 2, N 8: e of 6 at (1, 1, 1) +X advances 3 steps per
    interval, f of 2 at (8, 2, 1) -X one; a shadow s of e at phase 5 and a
    shadow u of f at phase 2, leaving fresh from (2, 1, 2) and (4, 1, 2)
    (re-pinned 2026-09-18, node-mixing-v1: a shadow no longer walks straight),
    share (3, 1, 2) after tick 1 with their phases unchanged and no event, and
    mix there in the cycle of tick 2, each alone (two owners do not mix), a
    lone quantum parking whole."""
    m = family("m", charge=-1, clock=True)
    e = lamp("e", "m", 6, (1, 1, 1))
    f = lamp("f", "m", 2, (8, 2, 1), heading=MINUS_X)
    s_fresh = shadow((2, 1, 2), X, 1, phase=5) | {"steps": 0}
    u_fresh = shadow((4, 1, 2), MINUS_X, 2, phase=2) | {"steps": 0}
    doc = document(
        families=[m],
        lamps=[e, f],
        shape=(9, 3, 3),
        ticks=4,
        K=2,
        shadows={"m": [s_fresh, u_fresh]},
    )
    result = run(doc, 4)
    for tick in range(1, 5):
        inventory = result["inventories"][tick - 1]
        (thing_e,) = things_at(inventory, (1 + tick, 1, 1))
        (thing_f,) = things_at(inventory, (8 - tick, 2, 1))
        assert (thing_e.phase, thing_e.remainder, thing_e.amount) == ((3 * tick) % 8, 0, 6)
        assert (thing_f.phase, thing_f.remainder, thing_f.amount) == (tick % 8, 0, 2)
    after_1 = result["inventories"][0]
    (s,) = [r for r in shadows_at(after_1, (3, 1, 2)) if r.owner == 1]
    (u,) = [r for r in shadows_at(after_1, (3, 1, 2)) if r.owner == 2]
    assert (s.phase, s.owner, s.remainder, s.steps, s.parked) == (5, 1, 0, 1, 0)
    assert (u.phase, u.owner, u.remainder, u.steps, u.parked) == (2, 2, 0, 1, 0)
    assert all(
        r.parked for tick in (2, 3, 4) for r in shadows_at(result["inventories"][tick - 1], (3, 1, 2))
    )
    assert kinds(result["events"], (3, 1, 2)) == {}
    assert result["steps"] == [4, 8, 12, 16]


@pytest.mark.parametrize(
    ("K", "content", "accepted"),
    [(1, 3, True), (1, 4, False), (2, 7, True), (2, 8, False)],
)
def test_k_and_n_bound_the_content_one_node_may_hold(K, content, accepted):
    """(c) N 8: a thing's content / K stays below N / 2, refused at parsing
    otherwise; and at a meeting whose output would hold more, the join fails
    closed before any owner changes."""
    m = family("m", charge=-1, clock=True)
    doc = document(
        families=[m], lamps=[lamp("e", "m", content, (1, 1, 1))], shape=(9, 3, 3), ticks=1, K=K
    )
    if accepted:
        assert parse_initial_state(doc).spatial_fields[0].clock == K
        return
    with pytest.raises(ValueError, match="half the phase circle"):
        parse_initial_state(doc)
    join = {
        "name": "join",
        "participants": [{"type": "m"}, {"type": "m"}],
        "outputs": [{"field": "m", "amount": {"of": "sum"}, "heading": 0, "phase": {"of": 0}}],
        "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
    }
    half = content // 2
    doc = document(
        families=[m],
        lamps=[lamp("e", "m", half, (1, 1, 1)), lamp("f", "m", half, (5, 1, 1), heading=MINUS_X)],
        shape=(9, 3, 3),
        ticks=4,
        K=K,
        rules=[join],
    )
    world = Simulation(parse_initial_state(doc))
    world.step()
    world.step()
    assert world.totals()["m"] == (2 * half,)
    with pytest.raises(ValueError, match="half the phase circle"):
        world.step()


def test_a_neutral_thing_has_gravity_and_no_electric_push_and_a_charge_accumulates_exactly():
    """(d) 9 x 5 x 3, K 4: a neutral thing n of 4 and a charged thing c of 4
    (charge +1 per quantum) each meet one shadow of a body of 32 with the whole
    charge -1 after tick 1 (re-pinned 2026-09-18, node-mixing-v1: the lamps one
    Link before the meeting and the shadows fresh from the Node beside it), the
    same shadow read twice: gravity, -1 x 1 x (0, 1, 0) x 4 = (0, -4, 0), turns
    each to -Y at its departure of tick 2 (the content reached), 4 spent each;
    electricity, 1 x 1 x (0, 1, 0) x (-1 / 32) x the thing's charge, is 0 on n
    and -1 / 32 on c, below one quantum: nothing into c's momentum, the
    remainder (0, -1, 0) in units of 1 / 32 on it."""
    n = family("n", charge=0, clock=True)
    c = family("c", charge=1, clock=True)
    e = family("e", charge=-1)
    star = {"position": [7, 4, 1], "family": "e", "amount": 32, "charge": -1}
    doc = document(
        families=[n, c, e],
        lamps=[lamp("lamp_n", "n", 4, (2, 2, 1)), lamp("lamp_c", "c", 4, (2, 3, 1))],
        shape=(9, 5, 3),
        ticks=3,
        K=4,
        shadows={
            "e": [
                shadow((3, 1, 1), PLUS_Y, 3) | {"steps": 0},
                shadow((3, 2, 1), PLUS_Y, 3) | {"steps": 0},
            ]
        },
        rules=[
            push(f"{reading}_{name}", {"e": sign}, reading, [{"type": name}, {"type": "e"}])
            for name in ("n", "c")
            for reading, sign in (("content", -1), ("charge", 1))
        ],
        bodies=[star],
    )
    initial = parse_initial_state(doc)
    assert initial.spatial_fields[2].owner_content(3) == 32
    assert initial.spatial_fields[2].owner_charge(3) == -1
    assert initial.spatial_fields[2].push_denominator == 32
    result = run(doc, 3)
    assert result["momentum"][0] == {1: [4, 0, 0], 2: [4, 0, 0], 3: [0, 0, 0]}
    assert result["momentum"][1] == {1: [0, -4, 0], 2: [0, -4, 0], 3: [0, 0, 0]}
    after_3 = result["inventories"][2]
    (neutral,) = things_at(after_3, (3, 0, 1), 0)
    (charged,) = things_at(after_3, (3, 1, 1), 1)
    assert (HEADINGS[neutral.heading], neutral.momentum, neutral.push_remainder) == (
        [0, -1, 0],
        None,
        (0, 0, 0),
    )
    assert (HEADINGS[charged.heading], charged.momentum, charged.push_remainder) == (
        [0, -1, 0],
        None,
        (0, -1, 0),
    )
    # Re-pinned 2026-09-18 (return-field-v1): each shadow turned back with the
    # opposite sign carrying (0, 4, 0) rides the Link -Y with the thing it
    # turned on the same lane, reads nothing more there (one meeting, one
    # push), mixes at (3,1,1) and (3,2,1) in the cycle of tick 3 and parks its
    # ninths there with that momentum: nothing of `e` is on its way after tick 3.
    for position in ((3, 1, 1), (3, 2, 1)):
        assert [r for r in after_3.get(position, ((), (), ()))[2] if not r.parked] == []
    assert result["momentum"][2] == result["momentum"][1]
    assert not {"ray_push", "decay_draw"} & set(kinds(result["events"]))
    with Simulation(initial) as world:
        for _ in range(3):
            world.step()
        assert world.audit()["fields"]["momentum"]["spent"] == (8, 0, 0)


DECAY = {
    "name": "weak",
    "participants": [{"type": "electron"}, {"type": "electron"}],
    "outputs": [
        {"field": "electron", "amount": {"of": 0}, "heading": 4, "phase": {"of": 0}},
        {"field": "electron", "amount": {"of": 1}, "heading": 5, "input": 1, "phase": {"of": 1}},
    ],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}


def ring(decay):
    doc = ring_document(PORT_CORNER)
    doc["ray_interactions"] = [DECAY | {"decay": decay}, PORT_CORNER]
    return doc


def test_a_bound_group_breaks_by_its_declared_table_and_never_by_a_draw(tmp_path):
    """(e) The unit-square ring of test_loop_binding under a decay rule declared
    before its corner table: `after_periods` 3 counts the corner meetings on the
    rays (passages 1 and 2 at the cycles of ticks 1 and 2) and breaks the group
    at the third, the outputs leaving the corners along +Z and -Z at tick 4 as
    fresh things; `content_at_most` 1 never breaks a corner's meeting of 2 and 2
    breaks the first; two runs are byte-identical; `draw` and `seed` are
    refused."""
    world = Simulation(parse_initial_state(ring({"after_periods": 3})))
    for tick in range(1, 7):
        world.step()
        corners = state(world)
        if tick <= 3:
            assert all(len(corners[p]) == 2 for p in CORNERS)
            assert {r.periods for p in CORNERS for r in corners[p]} == {tick - 1}
            assert world.totals()["electron"] == (8,)
            continue
        assert all(corners[p] == [] for p in CORNERS)
        off = tick - 3
        for x, y, z in CORNERS:
            up = [r for r in world.inventory_view().nodes if r.position == (x, y, z + off)]
            down = [r for r in world.inventory_view().nodes if r.position == (x, y, z - off)]
            for node, heading in ((up, 4), (down, 5)):
                (found,) = node
                (electron,) = found.rays[0]
                assert (electron.heading, electron.amount, electron.periods, electron.detector) == (
                    heading,
                    1,
                    0,
                    BIT_THING,
                )
        assert world.totals()["electron"] == (8,)
    never = Simulation(parse_initial_state(ring({"content_at_most": 1})))
    for tick in range(1, 9):
        never.step()
        corners = state(never)
        assert all(len(corners[p]) == 2 for p in CORNERS)
        assert {r.periods for p in CORNERS for r in corners[p]} == {tick - 1}
    first = Simulation(parse_initial_state(ring({"content_at_most": 2})))
    first.step()
    first.step()
    assert all(state(first)[p] == [] for p in CORNERS)
    assert first.totals()["electron"] == (8,)
    records = []
    for name in ("first", "second"):
        source = tmp_path / f"{name}.json"
        source.write_text(json.dumps(ring({"after_periods": 3})))
        run_initialization(source, tmp_path / name, ticks=6)
        records.append((tmp_path / name / "events.jsonl").read_bytes())
        metadata = json.loads((tmp_path / name / "run.json").read_text())
        assert "decay_draw" not in metadata and metadata["conserved_at_every_completed_tick"]
    assert records[0] == records[1]
    for change, message in (
        (lambda d: d["ray_interactions"][0].update(draw=[1, 2], seed=0), "clock-readings-v1"),
        (lambda d: d["ray_interactions"][0].update(decay={}), "one condition"),
        (
            lambda d: d["ray_interactions"][0].update(decay={"after_periods": 1, "content_at_most": 1}),
            "one condition",
        ),
        (lambda d: d["ray_interactions"][0].update(decay={"after_periods": 0}), "after_periods"),
        (
            lambda d: d["ray_interactions"].__setitem__(
                0,
                {
                    "name": "weak",
                    "participants": [{"type": "electron"}, {"type": "electron"}],
                    "momentum_table": {"electron": 1},
                    "reads": "content",
                    "invariants": push("weak", {}, "content", [])["invariants"],
                    "decay": {"after_periods": 1},
                },
            ),
            "requires a ray interaction with outputs",
        ),
    ):
        doc = ring({"after_periods": 3})
        change(doc)
        with pytest.raises(ValueError, match=message):
            parse_initial_state(doc)
    assert (P0, P1, P2, P3) == CORNERS and BIT_SHADOW == 0
