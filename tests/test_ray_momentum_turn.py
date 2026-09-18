"""A thing turns by momentum (ray-momentum-turn-v3 under clock-readings-v1;
Highlights 5.4 points 15, 16 and 21 and the settled rule (i), the model owner's
decisions of 2026-09-18): a coupling of free rays whose `momentum_table` names a
participant family pushes its one unnamed participant, a thing, by the declared
reading of every shadow it meets (here "content": sign x amount x heading x the
thing's content, the gravity reading), and returns each shadow reversed with
-push; the push stamps no event and changes no amount, phase or bit. The
momentum a thing carries is the pushes it has taken: at its next departure the
first axis on which it has reached the thing's content turns the thing to that
axis and drops by the content, which the ledger books as `spent` on the momentum
field's line; a component on the thing's own direction turns it nowhere and
drops nothing; two pushes of opposite sign cancel and the thing resumes its line
as the thing it was; every ray moves one Link per interval (the DDA staircase of
ray-momentum-turn-v2 is retired). A world without a momentum table on a coupling
of free rays records no identity and runs byte-identically twice.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A free ray turns by
momentum") before the first run.

Re-pinned on 2026-09-18 under bit-law-v1 (only a shadow pushes, given with the
board; a push is not an event; the momentum line is exact at zero until a shadow
escapes) and on the same day under clock-readings-v1 (the step in place of the
DDA walk, the content reading, `spent`, K 8 for the thing of 8, the wait per
quantum read pinned in test_wait_rule.py and 0 here), and under node-is-ports-v1
(a lamp is a thing that spends its content; a shadow whose steps are spent on
its walk back waits at that Node at rest, settled rule (ii), so nothing of `f`
ever leaves the board).

Re-pinned on 2026-09-18 under the Node's mixing (node-mixing-v1, Highlights
5.4 point 24, feature 16c): a lone shadow no longer walks straight to the thing
it pushes, it mixes at every Node with nothing else there, so the thing's lamp
is one Link before C and every shadow leaves fresh from the Node beside C, both
reach C after tick 1, the push is in the cycle of tick 2 and the return, its one
step spent, waits beside C; every tick here is five earlier than before.
"""

import hashlib
import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import InteractionDefinition
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    RAY_MOMENTUM_TURN,
    Ray,
    ray_merge_key,
    turn_receiver,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
CENTER = (10, 10, 10)
ZERO = (0, 0, 0)
ENERGY = {
    "name": "energy",
    "expression": {
        "op": "add",
        "args": [{"field": "amount", "participant": 0}, {"field": "amount", "participant": 1}],
    },
}


def turn(table, participants=({"type": "m"}, {"type": "f"})):
    """The coupling of a thing with a shadow: no outputs, no assignments, the
    table names the shadows' family and the thing it does not name is pushed,
    read times its content (point 16, the gravity reading: `f` has no charge)."""
    return {
        "name": "turn",
        "participants": list(participants),
        "momentum_table": table,
        "reads": "content",
        "invariants": [ENERGY],
    }


# The ordinary meeting with outputs of released-field-v1: the ray leaves on the
# field ray's heading, a whole Port, and the field ray returns reversed.
DEFLECT = {
    "name": "deflect",
    "participants": [{"type": "m"}, {"type": "f"}],
    "outputs": [
        {"field": "m", "amount": {"of": 0}, "heading": "same", "input": 1, "phase": {"of": 0}},
        {"field": "f", "amount": {"of": 1}, "heading": "reversed", "input": 1},
    ],
    "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
}


def field(name, components=1, signed=False):
    return {
        "name": name,
        "components": components,
        "units": "quantum" if components == 1 else "quantum times heading",
        "signed": signed,
        "conserved": True,
        "extensive": True,
    }


def ray_field(name, clock):
    entry = {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": 8,
        "metric": "links",
        "pace": [1, 1],
        "phase_bits": 3,
    }
    if clock:
        # The clock is the content (clock-readings-v1): the thing of 8 advances
        # one step per interval at K 8.
        entry["clock"] = True
    if name == "m":
        entry["charge"] = 1
    return entry


def document(lamps, rules, ticks):
    """The board: `lamps` are (position, family, amount, heading index); a lamp
    of `m` emits a thing whose recoil stays on the lamp's `momentum` vector; a
    "lamp" of `f` is a fresh shadow given with the board at that Node (bit-law-v1:
    only a shadow pushes)."""
    things = [lamp for lamp in lamps if lamp[1] == "m"]
    shadows = [lamp for lamp in lamps if lamp[1] == "f"]
    return {
        "schema_version": 1,
        "model_id": "ray-momentum-turn-test-v1",
        "shape": [21, 21, 21],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "K": 8,
        # The wait per whole quantum read (point 23) is pinned in test_wait_rule.py.
        "wait_per_quantum": 0,
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
        "fields": [field("m"), field("f"), field("momentum", 3, True)],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": [family, "momentum"],
                "defaults": {family: amount, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for index, (_, family, amount, _) in enumerate(things)
        ],
        "spatial_fields": [ray_field("m", True), ray_field("f", False)],
        "initial_field": {
            "f": {
                "rays": [
                    {
                        "position": list(position),
                        "heading": HEADINGS[heading],
                        "amount": amount,
                        "sign": 1,
                        "steps": 0,
                    }
                    for position, _, amount, heading in shadows
                ]
            }
        },
        "emissions": [
            {
                "type": f"lamp_{index}",
                "field": family,
                "amount": amount,
                "denominator": 1,
                "heading": HEADINGS[heading],
                "kerengonen_phase": 0,
            }
            for index, (_, family, amount, heading) in enumerate(things)
        ],
        "seeds": [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (position, _, _, _) in enumerate(things)
        ],
        "ray_interactions": list(rules),
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


def ray(heading, amount, phase, steps, port, momentum=None):
    """A lamp's thing: one event through one Port, its whole amount, its walk
    started over at every step, and the pushes it carries."""
    shares = tuple(amount if p == port else 0 for p in range(6))
    return Ray(
        heading,
        ZERO,
        amount,
        phase=phase,
        steps=steps,
        event_ports=1 << port,
        event_shares=shares,
        momentum=momentum,
    )


def shadow_ray(heading, amount, steps, momentum=None):
    """A shadow of `f` given with the board, or the same returned with -push
    (bit-law-v1: bit 0, sign 1, no phase, walking back with `outbound` 0)."""
    return Ray(
        heading,
        ZERO,
        amount,
        steps=steps,
        outbound=0 if momentum is not None else 1,
        detector=BIT_SHADOW,
        source_sign=1,
        momentum=momentum,
    )


def momentum_line(world):
    return world.audit()["fields"]["momentum"]


def balanced(world):
    ledger = world.audit()
    return ledger["balanced"] and all(item["balanced"] for item in world.spatial_accounting().values())


def pushes_of(events):
    """A push is not an event (bit-law-v1, point 15): none is ever recorded."""
    return [e for e in events if e["event"] == "ray_push"]


def run(tmp_path, raw, ticks):
    path = tmp_path / "world.json"
    path.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=ticks)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    lines = (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    digests = tuple(
        hashlib.sha256((tmp_path / "out" / name).read_bytes()).hexdigest()
        for name in ("events.jsonl", "state.json")
    )
    return metadata, [json.loads(line) for line in lines], digests


THING = ((9, 10, 10), "m", 8, 0)
FROM_BELOW = ((10, 9, 10), "f", 1, 2)
FROM_ABOVE = ((10, 11, 10), "f", 1, 3)
HEAD_ON = ((11, 10, 10), "f", 1, 1)


@pytest.mark.parametrize("case", ["turn", "cancel", "reverse", "along", "identical", "rejected"])
def test_a_free_ray_turns_by_the_momentum_a_field_ray_gives_it(tmp_path, case):
    events = []
    if case == "turn":
        # (a) A thing of 8 heading +X meets a shadow of 1 from -Y with sign -1 at
        # C after tick 6: in the cycle of that tick the push, -1 x 1 x (0, 1, 0) x
        # 8 = (0, -8, 0), is the thing's momentum, and the shadow turns back on
        # its six steps carrying (0, 8, 0). At its departure of tick 7 the Y
        # component has reached the content: the thing turns to -Y, its momentum
        # drops to nothing and the ledger books (8, 0, 0), its motion on +X,
        # spent. Thing and shadow then walk -Y together, one Link per interval,
        # the shadow's steps down to 0 at (10, 4, 10) after tick 12 and on, and
        # the thing walks on and leaves the board after tick 16 with (0, -8, 0);
        # the shadow, its steps spent, waits at (10, 4, 10) at rest (settled rule
        # (ii) of node-is-ports-v1), so the momentum line reads current (-8, 8, 0)
        # and escaped (0, -8, 0) from tick 17.
        raw = document((THING, FROM_BELOW), [turn({"f": -1})], 14)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 15):
            world.step()
            assert world.totals()["m"] == ((8,) if t <= 11 else (0,))
            assert world.totals()["f"] == (1,) and world.escaped_totals()["f"] == (0,)
            line = momentum_line(world)
            assert line["initial"] == ZERO and line["sourced"] == ZERO and line["returned"] == ZERO
            assert line["escaped"] == (ZERO if t <= 11 else (0, -8, 0))
            assert line["current"] == (ZERO if t <= 1 else (-8, 0, 0) if t <= 11 else (-8, 8, 0))
            assert line["spent"] == (ZERO if t <= 1 else (8, 0, 0))
            assert balanced(world)
            if t == 1:
                assert rays_at(world, CENTER, "m") == [ray(0, 8, 1, 1, 0)]
                assert rays_at(world, CENTER, "f") == [shadow_ray(2, 1, 1)]
                assert world.thing_momentum() == {1: [8, 0, 0]}
                continue
            # The shadow walks its one step back to (10, 9, 10) and waits there.
            assert positions_of(world, "f") == {(10, 9, 10)}
            assert rays_at(world, (10, 9, 10), "f") == [shadow_ray(3, 1, 0, (0, 8, 0))]
            if t <= 11:
                at = (10, 11 - t, 10)
                assert positions_of(world, "m") == {at}
                assert rays_at(world, at, "m") == [ray(3, 8, t & 7, t, 0)]
                assert world.thing_momentum() == {1: [0, -8, 0]}
            else:
                assert positions_of(world, "m") == set()
                assert world.thing_momentum() == {}
        assert pushes_of(events) == []
        metadata, records, _ = run(tmp_path, raw, 14)
        assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN == "ray-momentum-turn-v3"
        assert metadata["clock_readings"] == "clock-readings-v1" and metadata["K"] == 8
        assert "bound_group_motion" not in metadata and "decay_draw" not in metadata
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["accounting_balanced_at_every_completed_tick"]
        assert pushes_of(records) == []
        assert metadata["final_totals"] == {"m": [0], "f": [1], "momentum": [-8, 8, 0]}
        assert metadata["spent_totals"] == {"m": [0], "f": [0], "momentum": [8, 0, 0]}
        assert metadata["momentum"][6] == {"1": [0, -8, 0]}
        return
    if case == "cancel":
        # (b) The same push and, in the same cycle, a shadow of 1 from +Y: the
        # pushes (0, -8, 0) and (0, 8, 0) cancel, the thing carries no momentum,
        # steps nowhere and walks on +X as the thing it was; each shadow walks
        # home with the opposite of its own push, waits at its Node of the board
        # once its steps are spent, and the momentum line is exact at zero with
        # nothing spent.
        raw = document((THING, FROM_BELOW, FROM_ABOVE), [turn({"f": -1})], 8)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 9):
            world.step()
            assert world.totals()["m"] == (8,) and world.totals()["f"] == (2,)
            line = momentum_line(world)
            assert line["sourced"] == ZERO and line["spent"] == ZERO
            assert line["current"] == ZERO and line["escaped"] == ZERO
            assert balanced(world)
            assert positions_of(world, "m") == {(9 + t, 10, 10)}
            assert rays_at(world, (9 + t, 10, 10), "m") == [ray(0, 8, t & 7, t, 0)]
            assert world.thing_momentum() == {1: [8, 0, 0]}
            if t == 1:
                assert rays_at(world, CENTER, "f") == [shadow_ray(2, 1, 1), shadow_ray(3, 1, 1)]
            else:
                # Each waits beside C with its step spent (a waiting shadow reads
                # heading 0 from the tick after it arrives).
                assert rays_at(world, (10, 9, 10), "f") == [
                    shadow_ray(3 if t == 2 else 0, 1, 0, (0, 8, 0))
                ]
                assert rays_at(world, (10, 11, 10), "f") == [
                    shadow_ray(2 if t == 2 else 0, 1, 0, (0, -8, 0))
                ]
        assert pushes_of(events) == []
        metadata, records, _ = run(tmp_path, raw, 8)
        assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN
        assert metadata["conserved_at_every_completed_tick"]
        assert pushes_of(records) == []
        assert metadata["final_totals"] == {"m": [8], "f": [2], "momentum": [0, 0, 0]}
        assert metadata["spent_totals"]["momentum"] == [0, 0, 0]
        return
    if case == "reverse":
        # (c) A shadow of 1 head on from +X with sign 1 (repulsion): the push
        # (-8, 0, 0) reaches the content on the thing's own axis in the opposite
        # sense, so at its departure of tick 7 the thing reverses to -X, its
        # momentum drops to nothing and (8, 0, 0) is spent; the shadow walks back
        # +X carrying (8, 0, 0). The thing is back at its lamp after tick 12.
        raw = document((THING, HEAD_ON), [turn({"f": 1})], 8)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 9):
            world.step()
            assert world.totals()["m"] == (8,) and world.totals()["f"] == (1,)
            line = momentum_line(world)
            assert line["current"] == (ZERO if t <= 1 else (-8, 0, 0))
            assert line["spent"] == (ZERO if t <= 1 else (8, 0, 0))
            assert balanced(world)
            if t == 1:
                assert rays_at(world, CENTER, "m") == [ray(0, 8, 1, 1, 0)]
                assert rays_at(world, CENTER, "f") == [shadow_ray(1, 1, 1)]
                continue
            assert rays_at(world, (11 - t, 10, 10), "m") == [ray(1, 8, t & 7, t, 0)]
            assert rays_at(world, (11, 10, 10), "f") == [shadow_ray(0, 1, 0, (8, 0, 0))]
            assert world.thing_momentum() == {1: [-8, 0, 0]}
        assert pushes_of(events) == []
        return
    if case == "along":
        # (d) The same shadow with sign -1 (attraction): the push (8, 0, 0) lies
        # on the thing's own direction, which turns it nowhere and drops nothing:
        # the thing walks on +X carrying (8, 0, 0), its register line reading
        # amount x heading plus that, (16, 0, 0); the shadow carries (-8, 0, 0)
        # back; nothing is spent and the momentum line is exact at zero.
        raw = document((THING, HEAD_ON), [turn({"f": -1})], 8)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 9):
            world.step()
            line = momentum_line(world)
            assert line["current"] == ZERO and line["spent"] == ZERO and balanced(world)
            if t == 1:
                assert rays_at(world, CENTER, "m") == [ray(0, 8, 1, 1, 0)]
                continue
            assert rays_at(world, (9 + t, 10, 10), "m") == [ray(0, 8, t & 7, t, 0, (8, 0, 0))]
            assert rays_at(world, (11, 10, 10), "f") == [shadow_ray(0, 1, 0, (-8, 0, 0))]
            assert world.thing_momentum() == {1: [16, 0, 0]}
        assert pushes_of(events) == []
        return
    if case == "identical":
        # (e) No momentum table on a coupling of free rays: the ordinary meeting
        # with outputs runs, no push is recorded, no identity is written, and
        # two runs of the world are byte for byte the same.
        raw = document((THING, FROM_BELOW), [DEFLECT], 12)
        digests = []
        for name in ("first", "second"):
            (tmp_path / name).mkdir()
            metadata, records, digest = run(tmp_path / name, raw, raw["ticks"])
            assert "ray_momentum_turn" not in metadata
            assert metadata["conserved_at_every_completed_tick"]
            assert metadata["spent_totals"]["momentum"] == [0, 0, 0]
            assert not any(e["event"] == "ray_push" for e in records)
            digests.append(digest)
        assert digests[0] == digests[1]
        return
    # (f) Malformed tables are rejected at initialization. A table beside
    # assignments and a `ray_delay` on a rule are the held form of binding,
    # removed by loop-binding-v1 on 2026-09-17, and name its migration note.
    lamps = (THING, FROM_BELOW)
    for rules, message in (
        (
            [turn({"f": -1}) | {"assignments": [{"participant": 0, "field": "delay", "expression": 1}]}],
            "removed by loop-binding-v1",
        ),
        ([turn({"f": -1}) | {"ray_delay": 1}], "removed by loop-binding-v1"),
        ([turn({"f": -1}, ({"type": "m"}, {"type": "m"}, {"type": "f"}))], "the one ray it turns"),
        ([turn({"f": 2})], "attraction"),
        ([{k: v for k, v in turn({"f": -1}).items() if k != "reads"}], "point 16"),
        (
            [{"name": "turn", "participants": [{"type": "m"}, {"type": "f"}], "invariants": [ENERGY]}],
            "requires assignments or outputs",
        ),
    ):
        with pytest.raises(ValueError, match=message):
            parse_initial_state(document(lamps, rules, 4))
    # A role that mixes a named and an unnamed family gives no receiver.
    mixed = InteractionDefinition(
        "turn", 0, 1, (), (), participants=((0, 1), (1,)), momentum_table=(0, -1)
    )
    assert turn_receiver(mixed) == -1
