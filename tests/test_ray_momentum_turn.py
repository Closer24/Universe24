"""A free ray turns by momentum (ray-momentum-turn-v2, Highlights 3.5, 3.14, 3.16
and 3.28): a ray's direction is its momentum register, three integers, by default
amount x heading, which the DDA walks at every departure, one Link per interval;
a coupling of free rays whose `momentum_table` names a participant family pushes
its one unnamed participant by sign x amount x heading of every field ray it
meets and returns each field ray reversed as the recoil; the push stamps no event
and changes no amount, phase or bit; two pushes of opposite sign cancel and the
ray resumes its line; the world ledger reads the register; a world without a
momentum table on a coupling of free rays runs byte-identically. Every push here
finds the accumulators at zero, so the walk kept through a push (v2, tested in
test_momentum_turn_walk.py) leaves these integers as they were.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("A free ray turns by
momentum") before the first run.

Re-pinned on 2026-09-18 under the law of the bit (bit-law-v1): only a shadow
pushes, so the field rays of `f` are shadows given with the board
(`initial_field.f.rays`, fresh at the old lamps' Nodes, sign 1), the coupling
reads the thing's charge (`m` charge 1: the push is sign x amount x heading as
before), a push is not an event (no `ray_push`; the register is read from the
ray), a returned shadow carries -push and the `momentum` line is exact at zero
until a shadow escapes, and a run's record carries the law's identities.

Re-pinned on 2026-09-18 under the Node's mixing (node-mixing-v1, Highlights
5.4 point 24, feature 16c): a lone shadow no longer walks straight to the ray
it is to push, it mixes at every Node with nothing else there, so every shadow
here leaves fresh from the Node beside the meeting point and meets the thing
there at tick 1, the push is in the cycle of tick 2, the paths are the same
five ticks earlier (`TURN_PATH[t - 2]`, `STEEP_PATH[t - 2]`), the return walks
its one step back and on to the edge, and `cancel` takes both pushes at once.
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
    ray_line,
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
    table names the shadows' family and the thing it does not name is pushed."""
    return {
        "name": "turn",
        "participants": list(participants),
        "momentum_table": table,
        # bit-law-v1, point 16 (2026-09-18): the push reads the thing's charge, 1.
        "reads": "charge",
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


def ray_field(name, advance):
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
        "kerengonen": {"phase_advance": advance},
    }
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
        "spatial_fields": [ray_field("m", 1), ray_field("f", 0)],
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
                "source": False,
                "heading": HEADINGS[heading],
                "recoil_field": "momentum",
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


def ray(heading, amount, phase, steps, port, accumulators=ZERO, momentum=None):
    """A lamp's ray or a recoil: one event through one Port, its whole amount."""
    shares = tuple(amount if p == port else 0 for p in range(6))
    return Ray(
        heading,
        accumulators,
        amount,
        phase=phase,
        steps=steps,
        event_ports=1 << port,
        event_shares=shares,
        momentum=momentum,
    )


def shadow_ray(heading, amount, steps, port, momentum=None):
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


# The DDA on the register (8, -2, 0) from (0, 0, 0): x x y x x, five Links of ten.
TURN_PATH = [
    ((11, 10, 10), (-2, 2, 0)),
    ((12, 10, 10), (-4, 4, 0)),
    ((12, 9, 10), (4, -4, 0)),
    ((13, 9, 10), (2, -2, 0)),
    ((14, 9, 10), ZERO),
    ((15, 9, 10), (-2, 2, 0)),
    ((16, 9, 10), (-4, 4, 0)),
    ((16, 8, 10), (4, -4, 0)),
    ((17, 8, 10), (2, -2, 0)),
    ((18, 8, 10), ZERO),
    ((19, 8, 10), (-2, 2, 0)),
    ((20, 8, 10), (-4, 4, 0)),
]
TURN_PORTS = [0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0, 0]
# The DDA on the register (2, 3, 0) from (0, 0, 0): y x y x y.
STEEP_PATH = [
    ((10, 11, 10), (2, -2, 0)),
    ((11, 11, 10), (-1, 1, 0)),
    ((11, 12, 10), (1, -1, 0)),
    ((12, 12, 10), (-2, 2, 0)),
    ((12, 13, 10), ZERO),
    ((12, 14, 10), (2, -2, 0)),
    ((13, 14, 10), (-1, 1, 0)),
    ((13, 15, 10), (1, -1, 0)),
    ((14, 15, 10), (-2, 2, 0)),
    ((14, 16, 10), ZERO),
]
STEEP_PORTS = [2, 0, 2, 0, 2, 2, 0, 2, 0, 2]
# The record of the world without a momentum table on a coupling of free rays,
# byte for byte that of the source before ray-momentum-turn-v1 (events.jsonl);
# state.json re-pinned on 2026-09-17 when loop-binding-v1 removed the snapshot's
# `bound_groups` key. Both re-pinned on 2026-09-18 under bit-law-v1: the record
# carries the law's identities (`owner` on every ray, the `bit_law` and the
# contents per tick in run.json) and the two lamps' rays are two things meeting
# by the declared table.
IDENTICAL = {
    "meeting": (
        "9553836d91db5dbd4eaf965644c2d3c24fa73f22a4f192ecaee18d9a9d69b009",
        "717a884ad903ece5e781d51fe97a8652a918bbef1a043ce937587d969ba91087",
    ),
}


def ports_of(path, start):
    ports = []
    at = start
    for position, _ in path:
        axis = next(i for i in range(3) if position[i] != at[i])
        ports.append(2 * axis + (0 if position[axis] > at[axis] else 1))
        at = position
    return ports


@pytest.mark.parametrize("case", ["turn", "cancel", "steep", "identical", "rejected"])
def test_a_free_ray_turns_by_the_momentum_a_field_ray_gives_it(tmp_path, case):
    events = []
    if case == "turn":
        # (a) A ray of 8 heading +X meets a field ray of 2 from -Y with sign -1:
        # its register becomes (8, -2, 0), toward the source, and it walks the
        # DDA on it for 12 intervals, one Link each; the recoil returns reversed.
        lamps = (((9, 10, 10), "m", 8, 0), ((10, 9, 10), "f", 2, 2))
        raw = document(lamps, [turn({"f": -1})], 13)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        assert ports_of(TURN_PATH, CENTER) == TURN_PORTS
        for t in range(1, 14):
            world.step()
            assert world.totals()["m"] == (8,)
            assert world.totals()["f"] == ((2,) if t <= 11 else (0,))
            assert world.escaped_totals()["f"] == ((0,) if t <= 11 else (2,))
            line = momentum_line(world)
            assert line["initial"] == ZERO and line["sourced"] == ZERO
            assert line["escaped"] == (ZERO if t <= 11 else (0, 2, 0))
            assert line["current"] == (ZERO if t <= 11 else (0, -2, 0))
            assert balanced(world)
            if t == 1:
                assert rays_at(world, CENTER, "m") == [ray(0, 8, 1, 1, 0)]
                assert rays_at(world, CENTER, "f") == [shadow_ray(2, 2, 1, 2)]
                continue
            at, accumulators = TURN_PATH[t - 2]
            assert positions_of(world, "m") == {at}
            assert rays_at(world, at, "m") == [ray(0, 8, t & 7, t, 0, accumulators, (8, -2, 0))]
            if t <= 11:
                assert rays_at(world, (10, 11 - t, 10), "f") == [shadow_ray(3, 2, 0, 3, (0, 2, 0))]
            else:
                assert positions_of(world, "f") == set()
        assert pushes_of(events) == []
        metadata, records, _ = run(tmp_path, raw, 13)
        assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN == "ray-momentum-turn-v2"
        assert "bound_group_motion" not in metadata
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["accounting_balanced_at_every_completed_tick"]
        assert pushes_of(records) == []
        assert metadata["final_totals"] == {"m": [8], "f": [0], "momentum": [0, -2, 0]}
        return
    if case == "cancel":
        # (b) The same push and a field ray of 2 from +Y in the same cycle (re-pinned
        # 2026-09-18, node-mixing-v1: a second push some Links on cannot be timed
        # by a shadow's walk any more): the register stays (8, 0, 0), the default,
        # and the ray keeps its line as the ray it was, walking +X with its
        # accumulators at zero, each shadow returned with its own -push.
        lamps = (((9, 10, 10), "m", 8, 0), ((10, 9, 10), "f", 2, 2), ((10, 11, 10), "f", 2, 3))
        raw = document(lamps, [turn({"f": -1})], 8)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 9):
            world.step()
            assert world.totals()["m"] == (8,) and world.totals()["f"] == (4,)
            line = momentum_line(world)
            assert line["sourced"] == ZERO
            assert line["current"] == ZERO and line["escaped"] == ZERO
            assert balanced(world)
            assert positions_of(world, "m") == {(9 + t, 10, 10)}
            assert rays_at(world, (9 + t, 10, 10), "m") == [ray(0, 8, t & 7, t, 0)]
            if t == 1:
                assert rays_at(world, CENTER, "f") == [shadow_ray(2, 2, 1, 2), shadow_ray(3, 2, 1, 3)]
                continue
            assert rays_at(world, (10, 11 - t, 10), "f") == [shadow_ray(3, 2, 0, 3, (0, 2, 0))]
            assert rays_at(world, (10, 9 + t, 10), "f") == [shadow_ray(2, 2, 0, 2, (0, -2, 0))]
        assert pushes_of(events) == []
        metadata, records, _ = run(tmp_path, raw, 8)
        assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN
        assert metadata["conserved_at_every_completed_tick"]
        assert pushes_of(records) == []
        assert metadata["final_totals"] == {"m": [8], "f": [4], "momentum": [0, 0, 0]}
        return
    if case == "steep":
        # (c) A ray of 2 heading +X pushed by a field ray of 3 from -Y with sign 1
        # (repulsion, away from the source) has the register (2, 3, 0), past 45
        # degrees: three +Y Links per two +X, its heading index still +X and its
        # line for the release geometry +Y, the dominant axis.
        lamps = (((9, 10, 10), "m", 2, 0), ((10, 9, 10), "f", 3, 2))
        raw = document(lamps, [turn({"f": 1})], 11)
        initial = parse_initial_state(raw)
        world = Simulation(initial, observer=events.append)
        assert ports_of(STEEP_PATH, CENTER) == STEEP_PORTS
        for t in range(1, 12):
            world.step()
            assert world.totals()["m"] == (2,) and world.totals()["f"] == (3,)
            line = momentum_line(world)
            assert line["sourced"] == ZERO
            assert line["current"] == ZERO and line["escaped"] == ZERO
            assert balanced(world)
            if t == 1:
                assert rays_at(world, CENTER, "m") == [ray(0, 2, 1, 1, 0)]
                assert rays_at(world, CENTER, "f") == [shadow_ray(2, 3, 1, 2)]
                continue
            at, accumulators = STEEP_PATH[t - 2]
            assert positions_of(world, "m") == {at}
            (turned,) = rays_at(world, at, "m")
            assert turned == ray(0, 2, t & 7, t, 0, accumulators, (2, 3, 0))
            assert ray_line(turned, initial.spatial_fields[0]) == (0, 1, 0)
            assert rays_at(world, (10, 11 - t, 10), "f") == [shadow_ray(3, 3, 0, 3, (0, -3, 0))]
        assert pushes_of(events) == []
        metadata, _, _ = run(tmp_path, raw, 11)
        assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN
        assert metadata["conserved_at_every_completed_tick"]
        return
    if case == "identical":
        # (d) No momentum table on a coupling of free rays: the ordinary meeting
        # with outputs runs byte for byte as before, no push recorded, no
        # identity written.
        worlds = {
            "meeting": document((((9, 10, 10), "m", 8, 0), ((10, 9, 10), "f", 2, 2)), [DEFLECT], 7),
        }
        for name, raw in worlds.items():
            (tmp_path / name).mkdir()
            metadata, records, digests = run(tmp_path / name, raw, raw["ticks"])
            assert "ray_momentum_turn" not in metadata, name
            assert metadata["conserved_at_every_completed_tick"], name
            assert not any(e["event"] == "ray_push" for e in records), name
            assert digests == IDENTICAL[name], name
        return
    # (e) Malformed tables are rejected at initialization, and a push that would
    # leave a ray with no direction fails the cycle: a ray never stops. A table
    # beside assignments and a `ray_delay` are the held form of binding, removed
    # by loop-binding-v1 on 2026-09-17, and name its migration note.
    lamps = (((4, 10, 10), "m", 8, 0), ((10, 4, 10), "f", 2, 2))
    for rules, message in (
        (
            [turn({"f": -1}) | {"assignments": [{"participant": 0, "field": "delay", "expression": 1}]}],
            "removed by loop-binding-v1",
        ),
        ([turn({"f": -1}) | {"ray_delay": 1}], "removed by loop-binding-v1"),
        ([turn({"f": -1}, ({"type": "m"}, {"type": "m"}, {"type": "f"}))], "the one ray it turns"),
        ([turn({"f": 2})], "attraction"),
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
    head_on = (((9, 10, 10), "m", 2, 0), ((11, 10, 10), "f", 2, 1))
    world = Simulation(parse_initial_state(document(head_on, [turn({"f": 1})], 3)))
    world.step()
    assert rays_at(world, CENTER, "m") == [ray(0, 2, 1, 1, 0)]
    assert rays_at(world, CENTER, "f") == [shadow_ray(1, 2, 1, 1)]
    with pytest.raises(ValueError, match="cannot stop a ray"):
        world.step()
