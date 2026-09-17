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
"""

import hashlib
import json

import pytest

from event_universe import Simulation
from event_universe.core.disturbance_state import InteractionDefinition
from event_universe.core.spatial_state import (
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
    """The coupling of a free ray with a field ray: no outputs, no assignments, the
    table names the field family and the ray it does not name is pushed."""
    return {
        "name": "turn",
        "participants": list(participants),
        "momentum_table": table,
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
    return {
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


def document(lamps, rules, ticks):
    """The board: `lamps` are (position, family, amount, heading index); every
    emission keeps its recoil on the lamp's `momentum` vector."""
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
            for index, (_, family, amount, _) in enumerate(lamps)
        ],
        "spatial_fields": [ray_field("m", 1), ray_field("f", 0)],
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
            for index, (_, family, amount, heading) in enumerate(lamps)
        ],
        "seeds": [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (position, _, _, _) in enumerate(lamps)
        ],
        "ray_interactions": list(rules),
    }


def rays_at(world, position, family):
    """The resident rays of one family at a Node, in merge-key order."""
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    return sorted(node.rays[index], key=ray_merge_key) if node is not None and node.rays else []


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


def momentum_line(world):
    return world.audit()["fields"]["momentum"]


def balanced(world):
    ledger = world.audit()
    return ledger["balanced"] and all(item["balanced"] for item in world.spatial_accounting().values())


def pushes_of(events):
    return [
        (
            e["tick"],
            tuple(e["position"]),
            e["family"],
            e["amount"],
            tuple(e["before"]),
            tuple(e["after"]),
            e["field"],
            e["field_amount"],
            tuple(e["field_heading"]),
        )
        for e in events
        if e["event"] == "ray_push"
    ]


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
# `bound_groups` key. The bound group of bound-group-motion-v1 went with that
# feature.
IDENTICAL = {
    "meeting": (
        "7ee9f730782a5c4de8cbc611751382cd48347005c9c4af0a557175ce7bdfec4d",
        "d824629b8e7570a3b7aab55fab2f7c286e885f10116133bbb9fc4fa99d4160bc",
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
        lamps = (((4, 10, 10), "m", 8, 0), ((10, 4, 10), "f", 2, 2))
        raw = document(lamps, [turn({"f": -1})], 18)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        assert ports_of(TURN_PATH, CENTER) == TURN_PORTS
        for t in range(1, 19):
            world.step()
            assert world.totals()["m"] == (8,)
            assert world.totals()["f"] == ((2,) if t <= 16 else (0,))
            assert world.escaped_totals()["f"] == ((0,) if t <= 16 else (2,))
            line = momentum_line(world)
            assert line["initial"] == ZERO
            assert line["sourced"] == (ZERO if t <= 6 else (0, -6, 0))
            assert line["escaped"] == (ZERO if t <= 16 else (0, -2, 0))
            assert line["current"] == (ZERO if t <= 6 else (0, -6, 0) if t <= 16 else (0, -4, 0))
            assert balanced(world)
            if t <= 6:
                assert rays_at(world, (4 + t, 10, 10), "m") == [ray(0, 8, t & 7, t, 0)]
                assert rays_at(world, (10, 4 + t, 10), "f") == [ray(2, 2, 0, t, 2)]
                continue
            at, accumulators = TURN_PATH[t - 7]
            assert positions_of(world, "m") == {at}
            assert rays_at(world, at, "m") == [ray(0, 8, t & 7, t, 0, accumulators, (8, -2, 0))]
            if t <= 16:
                assert rays_at(world, (10, 16 - t, 10), "f") == [ray(3, 2, 0, t - 6, 3)]
            else:
                assert positions_of(world, "f") == set()
        assert pushes_of(events) == [
            (6, CENTER, "m", 8, (8, 0, 0), (8, -2, 0), "f", 2, (0, 1, 0)),
        ]
        metadata, records, _ = run(tmp_path, raw, 18)
        assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN == "ray-momentum-turn-v2"
        assert "bound_group_motion" not in metadata
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["accounting_balanced_at_every_completed_tick"]
        assert pushes_of(records) == pushes_of(events)
        assert metadata["final_totals"] == {"m": [8], "f": [0], "momentum": [0, -4, 0]}
        return
    if case == "cancel":
        # (b) The same push, then a field ray of 2 from +Y two Links on: the
        # register returns to (8, 0, 0), the default, and the ray resumes its line
        # as the ray it was, walking +X with its accumulators at zero.
        lamps = (((4, 10, 10), "m", 8, 0), ((10, 4, 10), "f", 2, 2), ((12, 18, 10), "f", 2, 3))
        raw = document(lamps, [turn({"f": -1})], 14)
        world = Simulation(parse_initial_state(raw), observer=events.append)
        for t in range(1, 15):
            world.step()
            assert world.totals()["m"] == (8,) and world.totals()["f"] == (4,)
            line = momentum_line(world)
            assert line["sourced"] == (ZERO if t <= 6 else (0, -6, 0) if t <= 8 else ZERO)
            assert line["current"] == line["sourced"] and line["escaped"] == ZERO
            assert balanced(world)
            if t <= 6:
                assert rays_at(world, (4 + t, 10, 10), "m") == [ray(0, 8, t & 7, t, 0)]
                continue
            if t <= 8:
                at, accumulators = TURN_PATH[t - 7]
                assert rays_at(world, at, "m") == [ray(0, 8, t & 7, t, 0, accumulators, (8, -2, 0))]
                assert rays_at(world, (12, 18 - t, 10), "f") == [ray(3, 2, 0, t, 3)]
            else:
                assert positions_of(world, "m") == {(4 + t, 10, 10)}
                assert rays_at(world, (4 + t, 10, 10), "m") == [ray(0, 8, t & 7, t, 0)]
                assert rays_at(world, (12, t + 2, 10), "f") == [ray(2, 2, 0, t - 8, 2)]
            assert rays_at(world, (10, 16 - t, 10), "f") == [ray(3, 2, 0, t - 6, 3)]
        assert pushes_of(events) == [
            (6, CENTER, "m", 8, (8, 0, 0), (8, -2, 0), "f", 2, (0, 1, 0)),
            (8, (12, 10, 10), "m", 8, (8, -2, 0), (8, 0, 0), "f", 2, (0, -1, 0)),
        ]
        metadata, records, _ = run(tmp_path, raw, 14)
        assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN
        assert metadata["conserved_at_every_completed_tick"]
        assert pushes_of(records) == pushes_of(events)
        assert metadata["final_totals"] == {"m": [8], "f": [4], "momentum": [0, 0, 0]}
        return
    if case == "steep":
        # (c) A ray of 2 heading +X pushed by a field ray of 3 from -Y with sign 1
        # (repulsion, away from the source) has the register (2, 3, 0), past 45
        # degrees: three +Y Links per two +X, its heading index still +X and its
        # line for the release geometry +Y, the dominant axis.
        lamps = (((4, 10, 10), "m", 2, 0), ((10, 4, 10), "f", 3, 2))
        raw = document(lamps, [turn({"f": 1})], 16)
        initial = parse_initial_state(raw)
        world = Simulation(initial, observer=events.append)
        assert ports_of(STEEP_PATH, CENTER) == STEEP_PORTS
        for t in range(1, 17):
            world.step()
            assert world.totals()["m"] == (2,) and world.totals()["f"] == (3,)
            line = momentum_line(world)
            assert line["sourced"] == (ZERO if t <= 6 else (0, -3, 0))
            assert line["current"] == line["sourced"] and line["escaped"] == ZERO
            assert balanced(world)
            if t <= 6:
                assert rays_at(world, (4 + t, 10, 10), "m") == [ray(0, 2, t & 7, t, 0)]
                continue
            at, accumulators = STEEP_PATH[t - 7]
            assert positions_of(world, "m") == {at}
            (turned,) = rays_at(world, at, "m")
            assert turned == ray(0, 2, t & 7, t, 0, accumulators, (2, 3, 0))
            assert ray_line(turned, initial.spatial_fields[0]) == (0, 1, 0)
            assert rays_at(world, (10, 16 - t, 10), "f") == [ray(3, 3, 0, t - 6, 3)]
        assert pushes_of(events) == [
            (6, CENTER, "m", 2, (2, 0, 0), (2, 3, 0), "f", 3, (0, 1, 0)),
        ]
        metadata, _, _ = run(tmp_path, raw, 16)
        assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN
        assert metadata["conserved_at_every_completed_tick"]
        return
    if case == "identical":
        # (d) No momentum table on a coupling of free rays: the ordinary meeting
        # with outputs runs byte for byte as before, no push recorded, no
        # identity written.
        worlds = {
            "meeting": document((((4, 10, 10), "m", 8, 0), ((10, 4, 10), "f", 2, 2)), [DEFLECT], 12),
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
    head_on = (((4, 10, 10), "m", 2, 0), ((16, 10, 10), "f", 2, 1))
    world = Simulation(parse_initial_state(document(head_on, [turn({"f": 1})], 8)))
    for _ in range(6):
        world.step()
    assert rays_at(world, CENTER, "m") == [ray(0, 2, 6, 6, 0)]
    assert rays_at(world, CENTER, "f") == [ray(1, 2, 0, 6, 1)]
    with pytest.raises(ValueError, match="cannot stop a ray"):
        world.step()
