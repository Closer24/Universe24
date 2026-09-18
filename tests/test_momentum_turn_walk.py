"""A push keeps the walk (ray-momentum-turn-v2, Highlights 3.16 and 3.28): the DDA's
three accumulators, the momentum-intervals each axis has banked toward its next
Link, carry over through a push and continue against the new register, so a ray
pushed at every interval walks the DDA line of its running register, a staircase
that turns gradually. The helium-orbit run (docs/EXPERIMENTS.md, E8) found that
v1 reset them at every push, which stepped such a ray along its register's
dominant axis alone. The flip of the dominant axis still turns the whole Port,
two pushes of opposite sign cancel and the ray resumes its line as the ray it
was, a register too short to hold the banked progress starts the walk over, and
the progress of a ray on the default walk is lifted to the register's scale.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The walk kept
through a push") before the first run.

Re-pinned on 2026-09-18 under the law of the bit (bit-law-v1): only a shadow
pushes, so the field rays of `f` and `g` are shadows given with the board
(`initial_field`, fresh at the old lamps' Nodes, sign 1), the couplings read the
thing's charge (`m` charge 1: the push is sign x amount x heading as before), a
push is not an event (no `ray_push`; the register is read from the ray) and the
`momentum` line is exact at zero: each returned shadow carries -push.

Re-pinned on 2026-09-18 under the Node's mixing (node-mixing-v1, Highlights
5.4 point 24, feature 16c): the `board` and `board_8` cases, a push at every
interval for 24 and 12 ticks from shadows placed along the path so that each
walked straight to the ray on its tick, were deleted: a lone shadow mixes at
every Node it reaches and cannot be timed by its walk; the walk kept through a
push stays pinned by `running` and `kept` on the ray arithmetic itself.
"""

import json
from dataclasses import replace

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    RAY_MOMENTUM_TURN,
    Ray,
    SpatialFieldDefinition,
    advance_ray,
    pushed_ray,
    ray_merge_key,
    ray_vector,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
PORT_HEADINGS = tuple(tuple(h) for h in HEADINGS)
ZERO = (0, 0, 0)
ENERGY = {
    "name": "energy",
    "expression": {
        "op": "add",
        "args": [{"field": "amount", "participant": 0}, {"field": "amount", "participant": 1}],
    },
}
# The ray of amount 64 heading +X pushed by (0, 1, 0) before every departure: the
# register (64, t, 0) at Link t, the accumulators after each Link and the position
# from (0, 0, 0); +Y at Links 9, 15, 20 and 24.
ACCUMULATORS_1 = [
    (-1, 1, 0), (-3, 3, 0), (-6, 6, 0), (-10, 10, 0), (-15, 15, 0), (-21, 21, 0),
    (-28, 28, 0), (-36, 36, 0), (28, -28, 0), (18, -18, 0), (7, -7, 0), (-5, 5, 0),
    (-18, 18, 0), (-32, 32, 0), (32, -32, 0), (16, -16, 0), (-1, 1, 0), (-19, 19, 0),
    (-38, 38, 0), (26, -26, 0), (5, -5, 0), (-17, 17, 0), (-40, 40, 0), (24, -24, 0),
]  # fmt: skip
PATH_1 = [
    (1, 0, 0), (2, 0, 0), (3, 0, 0), (4, 0, 0), (5, 0, 0), (6, 0, 0), (7, 0, 0), (8, 0, 0),
    (8, 1, 0), (9, 1, 0), (10, 1, 0), (11, 1, 0), (12, 1, 0), (13, 1, 0), (13, 2, 0),
    (14, 2, 0), (15, 2, 0), (16, 2, 0), (17, 2, 0), (17, 3, 0), (18, 3, 0), (19, 3, 0),
    (20, 3, 0), (20, 4, 0),
]  # fmt: skip
# The same ray pushed by (0, 8, 0) before every departure: the register (64, 8t, 0).
ACCUMULATORS_8 = [
    (-8, 8, 0), (-24, 24, 0), (40, -40, 0), (8, -8, 0), (-32, 32, 0), (32, -32, 0),
    (-24, 24, 0), (40, -40, 0), (-32, 32, 0), (32, -32, 0), (-56, 56, 0), (8, -8, 0),
    (72, -72, 0), (-40, 40, 0), (24, -24, 0), (88, -88, 0), (-48, 48, 0), (16, -16, 0),
    (80, -80, 0), (-80, 80, 0), (-16, 16, 0), (48, -48, 0), (112, -112, 0), (-80, 80, 0),
]  # fmt: skip
PATH_8 = [
    (1, 0, 0), (2, 0, 0), (2, 1, 0), (3, 1, 0), (4, 1, 0), (4, 2, 0), (5, 2, 0), (5, 3, 0),
    (6, 3, 0), (6, 4, 0), (7, 4, 0), (7, 5, 0), (7, 6, 0), (8, 6, 0), (8, 7, 0), (8, 8, 0),
    (9, 8, 0), (9, 9, 0), (9, 10, 0), (10, 10, 0), (10, 11, 0), (10, 12, 0), (10, 13, 0),
    (11, 13, 0),
]  # fmt: skip


def definition():
    """The m family of the boards, with one table heading off the axes for the lift."""
    return SpatialFieldDefinition(
        0,
        (0,),
        transport="ray",
        headings=PORT_HEADINGS + ((7, -1, 0),),
        rays_per_tick=1,
        ray_slots=8,
    )


def moved(at, port):
    heading = PORT_HEADINGS[port]
    return (at[0] + heading[0], at[1] + heading[1], at[2] + heading[2])


def walk(ray, pushes, intervals, field=None):
    """The Node cycle's order for a free ray: the pushes of the interval, then the
    departure by the DDA on its vector. Returns (position, accumulators, register,
    Port) after each Link from (0, 0, 0)."""
    field = definition() if field is None else field
    at, steps = ZERO, []
    for interval in range(intervals):
        for push in pushes(interval):
            ray = pushed_ray(ray, push, field)
        port, ray = advance_ray(ray, ray_vector(ray, field))
        at = moved(at, port)
        steps.append((at, ray.accumulators, ray.momentum, port))
    return steps


def ports_of(path):
    ports, at = [], ZERO
    for position in path:
        axis = next(i for i in range(3) if position[i] != at[i])
        ports.append(2 * axis + (0 if position[axis] > at[axis] else 1))
        at = position
    return ports


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


def turn(name, family, sign):
    """A coupling of the free ray m with the field family: no outputs, no
    assignments, the table names the field family with its sign."""
    return {
        "name": name,
        "participants": [{"type": "m"}, {"type": family}],
        "momentum_table": {family: sign},
        # bit-law-v1, point 16 (2026-09-18): the push reads the thing's charge, 1.
        "reads": "charge",
        "invariants": [ENERGY],
    }


def document(shape, lamps, ticks):
    """The board: `lamps` are (position, family, amount, heading index); the lamp
    of `m` emits along +X, its recoil on its `momentum` vector; a "lamp" of `f`
    or `g` is a fresh shadow given with the board at that Node (bit-law-v1: only a
    shadow pushes), of `f` along -Y, of `g` along +Y. `f` shadows come down under
    `above` with sign -1 and `g` shadows up under `below` with sign 1, so each
    pushes the m ray by (0, amount, 0)."""
    types = {}
    for _, family, amount, heading in lamps:
        assert types.setdefault(family, (amount, heading)) == (amount, heading)
    shadows = {
        family: [
            {
                "position": list(position),
                "heading": HEADINGS[heading],
                "amount": amount,
                "sign": 1,
                "steps": 0,
            }
            for position, family_, amount, heading in lamps
            if family_ == family
        ]
        for family in ("f", "g")
    }
    return {
        "schema_version": 1,
        "model_id": "momentum-turn-walk-test-v1",
        "shape": list(shape),
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
        "fields": [field("m"), field("f"), field("g"), field("momentum", 3, True)],
        "disturbance_types": [
            {
                "name": f"lamp_{family}",
                "fields": [family, "momentum"],
                "defaults": {family: amount, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for family, (amount, _) in types.items()
            if family == "m"
        ],
        "spatial_fields": [ray_field("m", 1), ray_field("f", 0), ray_field("g", 0)],
        "initial_field": {family: {"rays": rays} for family, rays in shadows.items() if rays},
        "emissions": [
            {
                "type": f"lamp_{family}",
                "field": family,
                "amount": amount,
                "denominator": 1,
                "source": False,
                "heading": HEADINGS[heading],
                "recoil_field": "momentum",
                "kerengonen_phase": 0,
            }
            for family, (amount, heading) in types.items()
            if family == "m"
        ],
        "seeds": [
            {"position": list(position), "type": f"lamp_{family}"}
            for position, family, _, _ in lamps
            if family == "m"
        ],
        "ray_interactions": [turn("above", "f", -1), turn("below", "g", 1)],
    }


def board(shape, lamp, amount, path, pushed):
    """The board of a walk: the m lamp at `lamp` emitting 64 along +X, the m ray at
    P(t) = lamp + (1, 0, 0) + path[t - 2] after tick t (P(1) one Link on), and a
    field lamp of `amount` per pushed tick t at P(t) + (0, t, 0) along -Y (f) when
    Link t is +X, at P(t) - (0, t, 0) along +Y (g) when Link t is +Y."""
    first = (lamp[0] + 1, lamp[1], lamp[2])
    positions = {1: first} | {
        t: (first[0] + dx, first[1] + dy, first[2] + dz) for t, (dx, dy, dz) in enumerate(path, start=2)
    }
    ports = ports_of(path)
    lamps = [(lamp, "m", 64, 0)]
    families = {}
    for t in pushed:
        x, y, z = positions[t]
        if ports[t - 1] == 0:
            lamps.append(((x, y + t, z), "f", amount, 3))
            families[t] = "f"
        else:
            assert ports[t - 1] == 2
            lamps.append(((x, y - t, z), "g", amount, 2))
            families[t] = "g"
    assert all(0 <= p[i] < shape[i] for p, _, _, _ in lamps for i in range(3))
    assert len({p for p, _, _, _ in lamps}) == len(lamps)
    assert not {p for p, _, _, _ in lamps} & set(positions.values())
    return document(shape, lamps, 0), positions, families, lamps


def rays_at(world, position, family):
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


def m_ray(phase, steps, accumulators=ZERO, momentum=None):
    """The m lamp's ray: one event through Port 0, its whole amount 64."""
    return Ray(
        0,
        accumulators,
        64,
        phase=phase,
        steps=steps,
        event_ports=1,
        event_shares=(64, 0, 0, 0, 0, 0),
        momentum=momentum,
    )


def balanced(world):
    ledger = world.audit()
    return ledger["balanced"] and all(item["balanced"] for item in world.spatial_accounting().values())


def pushes_of(events):
    """A push is not an event (bit-law-v1, point 15): none is ever recorded."""
    return [e for e in events if e["event"] == "ray_push"]


def run_board(tmp_path, raw, ticks, positions, families, amount, path, accumulators, pushed, after):
    """Step the board tick by tick against the pinned path, then run it through the
    runner: no push recorded, the identity recorded, every ledger exact."""
    raw = raw | {"ticks": ticks}
    events = []
    world = Simulation(parse_initial_state(raw), observer=events.append)
    for t in range(1, ticks + 1):
        world.step()
        assert positions_of(world, "m") == {positions[t]}, t
        if t == 1:
            assert rays_at(world, positions[1], "m") == [m_ray(1, 1)]
        elif t <= len(pushed) + 1:
            register = (64, amount * (t - 1), 0)
            assert rays_at(world, positions[t], "m") == [
                m_ray(t & 7, t, accumulators[t - 2], register)
            ], t
        else:
            assert rays_at(world, positions[t], "m") == [
                m_ray(t & 7, t, after[t], (64, amount * len(pushed), 0))
            ], t
        assert world.totals()["m"] == (64,)
        assert world.escaped_totals()["m"] == (0,)
        # Each shadow carries -push home: the momentum line stays at zero.
        line = world.audit()["fields"]["momentum"]
        assert line["initial"] == ZERO and line["escaped"] == ZERO
        assert line["sourced"] == line["current"] == ZERO, t
        assert balanced(world), t
    assert pushes_of(events) == []
    path_file = tmp_path / "world.json"
    path_file.write_text(json.dumps(raw), encoding="utf-8")
    run_initialization(path_file, tmp_path / "out", ticks=ticks)
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    records = [
        json.loads(line)
        for line in (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
    ]
    assert metadata["ray_momentum_turn"] == RAY_MOMENTUM_TURN == "ray-momentum-turn-v2"
    assert metadata["conserved_at_every_completed_tick"]
    assert metadata["accounting_balanced_at_every_completed_tick"]
    assert pushes_of(records) == []
    assert metadata["final_totals"]["m"] == [64]


@pytest.mark.parametrize("case", ["running", "kept"])
def test_a_push_keeps_the_walk_of_the_ray_it_turns(tmp_path, case):
    if case == "running":
        # (a) The staircases of the running register: a push of (0, 1, 0) and one
        # of (0, 8, 0) before every departure, 24 Links each, from the default.
        for push, path, accumulators in (
            ((0, 1, 0), PATH_1, ACCUMULATORS_1),
            ((0, 8, 0), PATH_8, ACCUMULATORS_8),
        ):
            steps = walk(m_ray(0, 0), lambda _, push=push: (push,), 24)
            assert [at for at, _, _, _ in steps] == path
            assert [acc for _, acc, _, _ in steps] == accumulators
            assert [register for _, _, register, _ in steps] == [
                (64, push[1] * (t + 1), 0) for t in range(24)
            ]
            assert [port for _, _, _, port in steps] == ports_of(path)
        assert ports_of(PATH_1).count(2) == 4 and ports_of(PATH_8).count(2) == 13
        # One push and none after is the static register (64, 1, 0), length 65:
        # +Y at Links 33, 98 and 163 of 200, one +Y per 65 Links.
        steps = walk(m_ray(0, 0), lambda t: ((0, 1, 0),) if t == 0 else (), 200)
        assert [t + 1 for t, (_, _, _, port) in enumerate(steps) if port == 2] == [33, 98, 163]
        assert steps[32][1] == (32, -32, 0) and steps[-1][2] == (64, 1, 0)
        return
    if case == "kept":
        # (b) The accumulators survive the push, and the walk goes on from them.
        field = definition()
        walked = m_ray(0, 20, (-20, 20, 0), (64, 1, 0))
        pushed = pushed_ray(walked, (0, 1, 0), field)
        assert pushed == m_ray(0, 20, (-20, 20, 0), (64, 2, 0))
        port, after = advance_ray(pushed, ray_vector(pushed, field))
        assert port == 0 and after.accumulators == (-22, 22, 0)
        # The flip of the dominant axis turns the whole Port at once, then the
        # staircase of the new register goes on from the kept accumulators.
        turned = m_ray(0, 20, (-20, 20, 0), (64, 10, 0))
        flipped = pushed_ray(turned, (0, 90, 0), field)
        assert flipped == m_ray(0, 20, (-20, 20, 0), (64, 100, 0))
        steps = walk(flipped, lambda _: (), 5)
        assert [port for _, _, _, port in steps] == [2, 0, 2, 2, 0]
        assert [acc for _, acc, _, _ in steps] == [
            (44, -44, 0), (-56, 56, 0), (8, -8, 0), (72, -72, 0), (-28, 28, 0)
        ]  # fmt: skip
        reversed_ = pushed_ray(turned, (-128, 0, 0), field)
        assert reversed_ == m_ray(0, 20, (-20, 20, 0), (-64, 10, 0))
        port, after = advance_ray(reversed_, ray_vector(reversed_, field))
        assert port == 1 and after.accumulators == (-30, 30, 0)
        # Two pushes of opposite sign cancel: the ray it was, field by field; a
        # register back at the default starts the walk over.
        original = m_ray(0, 0)
        assert pushed_ray(pushed_ray(original, (0, 1, 0), field), (0, -1, 0), field) == original
        assert pushed_ray(walked, (0, -1, 0), field) == m_ray(0, 20)
        # A register that still holds the balance keeps it; one too short to hold
        # it starts the walk over.
        banked = m_ray(0, 40, (-30, 30, 0), (64, 30, 0))
        assert pushed_ray(banked, (-30, 0, 0), field) == m_ray(0, 40, (-30, 30, 0), (34, 30, 0))
        assert pushed_ray(banked, (-62, -28, 0), field) == m_ray(0, 40, ZERO, (2, 2, 0))
        # The lift: the progress of the default walk on a table heading, at the
        # table's scale, is lifted by the amount to the register's scale.
        slanted = Ray(6, ZERO, 5)
        steps = walk(slanted, lambda _: (), 3)
        assert [port for _, _, _, port in steps] == [0, 0, 0]
        slanted = Ray(6, (-3, 3, 0), 5)
        lifted = pushed_ray(slanted, (0, 0, 1), field)
        assert lifted == Ray(6, (-15, 15, 0), 5, momentum=(35, -5, 1))
        port, after = advance_ray(lifted, ray_vector(lifted, field))
        assert port == 0 and after.accumulators == (-21, 20, 1)
        assert advance_ray(slanted, ray_vector(slanted, field))[0] == 0
        return
