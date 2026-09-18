"""Field spreading (field-spreading-v1, Highlights 3.5): every Node that field content
reaches releases it again in all six headings by the family's declared split table;
the content combines by phase before it spreads, each heading's content is shared in
whole quanta and the share below one quantum stays in the Node's remainder register
of that heading and sign (field-remainder-v1, Highlights 3.5 and 3.17), which
releases a whole quantum through its heading when it fills; the total is exact.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Field spreading")
before the first run: single, superposition, cancelled, stream, sign, rejected.

Re-pinned on 2026-09-18 under the law of the bit (bit-law-v1): what spreads is
a shadow (bit 0), given with the board (`initial_field.light.rays`, each one
content that arrived on its heading, spreading at its Node in the first cycle),
where the old world's lamp emitted it one tick earlier, so every board reads one
tick sooner; a shadow has no mass, so no momentum field is booked; a Node
holding shadows alone publishes no event (point 13), so the `field_spread`
records are gone and the boards, the registers and the ledger are read from the
world. The `stream` is the same arithmetic through `spread_content`. The cases
of a thing releasing its field every interval (`returned`, `source`,
`resident`) and the byte-identity of a world declaring `field_of` (`unchanged`)
went with the law: a thing releases nothing per tick, its shadows are on the
board from the start.

Re-pinned again on 2026-09-18 under the phase-steered spread (phase-spread-v1,
Highlights 5.4 point 17): two shares of one owner meeting at a Node steer each
other by the Born table instead of spreading by the split table, so
`superposition` (phases 0 and 6, a difference of two steps: half continues,
11 each way, half apart, 6 on each transverse heading) and `cancelled` (phases
0 and 4: nothing continues, 12, 12, 12, 10 apart) read the steering; a lone
share keeps the split table (`single`, `stream`).
"""

import json

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    FIELD_REMAINDER,
    FIELD_SPREADING,
    Ray,
    merge_rays,
    parked_shares,
    ray_merge_key,
    relative_ports,
    spread_content,
    transmit,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# Forward 6/11, backward 1/11, each transverse 1/11.
SPREAD = [6, 1, 1, 1, 1, 1]
ZERO = (0, 0, 0, 0, 0, 0)
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}
# The one thing of the boards, a holder of `light` that is never seeded: its id.
OWNER = 1


def field(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


def vector(name):
    return {
        "name": name,
        "components": 3,
        "units": "quantum times heading",
        "signed": True,
        "conserved": True,
        "extensive": True,
    }


def ray_field(name, advance, slots=16, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "ray_slots": slots,
        "metric": "links",
        "pace": [1, 1],
        "kerengonen": {"phase_steps": 8, "phase_advance": advance},
    } | extra


def world(fields, types, spatial, emissions, seeds, ticks, initial_field=None, detectors=()):
    return {
        "schema_version": 1,
        "model_id": "field-spreading-test-v1",
        "shape": [13, 13, 13],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": fields,
        "disturbance_types": types,
        "spatial_fields": spatial,
        "emissions": emissions,
        "seeds": seeds,
        "detectors": list(detectors),
        **({"initial_field": initial_field} if initial_field else {}),
    }


def document(shadows, spread=SPREAD, ticks=3, detectors=(), dense=False):
    """The board: `shadows` are (position, amount, heading index, phase) of `light`,
    each a shadow of the holder (thing 1) given with the board as content that
    arrived on its heading, spreading at its Node in the first cycle."""
    light = ray_field("light", 0) | ({"spread": list(spread)} if spread else {})
    raw = world(
        [field("light")],
        [
            {
                "name": "holder",
                "fields": ["light"],
                "defaults": {"light": 0},
                "transport": {"mode": "hold"},
            }
        ],
        [light],
        [],
        [],
        ticks,
        {
            "light": {
                "rays": [
                    {
                        "position": list(position),
                        "heading": HEADINGS[heading],
                        "amount": amount,
                        "phase": phase,
                        "owner": OWNER,
                    }
                    for position, amount, heading, phase in shadows
                ]
            }
        }
        if shadows
        else None,
        detectors,
    )
    raw["dense_field"] = dense
    return raw


def bundles(world, position):
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    return () if node is None or not node.rays else node.rays


def family_index(world, family):
    return [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )


def rays_at(world, position, family="light"):
    """The resident rays of one family at a Node, in merge-key order."""
    node = bundles(world, position)
    return sorted(node[family_index(world, family)], key=ray_merge_key) if node else []


def positions_of(world, family="light"):
    return {n.position for n in world.inventory_view().nodes if rays_at(world, n.position, family)}


def registers_at(world, position, family="light"):
    """The Node's parked shadows of one family (node-is-ports-v1) as the block the
    spread step reads: eighteen shares and their phases per owner."""
    index = family_index(world, family)
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    parked = node.parked[index] if node is not None and node.parked else ()
    return parked_shares(parked, world.initial.spatial_fields[index])


def remainder_map(world, family="light"):
    """Every nonzero block of sign 0 on the board, by position."""
    index = family_index(world, family)
    return {
        n.position: registers_at(world, n.position, family)[0][6:12]
        for n in world.inventory_view().nodes
        if n.parked and any(ray.amount for ray in n.parked[index])
    }


def shadow(heading, amount, phase, sign=0, steps=1):
    """A shadow of the holder given with the board, or a departure of a spread one
    Link on: bit 0, the combined phase, no event."""
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        steps=steps,
        detector=BIT_SHADOW,
        source_sign=sign,
        owner=OWNER,
    )


def block(zero=ZERO, minus=ZERO, plus=ZERO):
    """A family's eighteen registers, sign-major -1, 0, 1 then Port."""
    return (*minus, *zero, *plus)


def phased(registers, phase):
    """The phases of a block filled at one phase: the phase where content is, else 0."""
    return tuple(phase if value else 0 for value in registers)


def simulate(raw):
    initial = parse_initial_state(raw)
    events = []
    world = Simulation(initial, observer=events.append)
    return world, events


def assert_board(world, expected, phase, sign=0):
    """Every Node holds exactly the (heading, amount) rays listed, at the given phase."""
    assert positions_of(world) == set(expected)
    for position, rays in expected.items():
        assert rays_at(world, position) == [shadow(h, a, phase, sign) for h, a in rays], position


def stream_forward(arrivals):
    """The forward register of a Node fed one quantum per arrival, after each arrival's
    release: 6 per arrival, less 11 whenever it reaches 11."""
    value = 0
    for _ in range(arrivals):
        value = (value + 6) % 11
    return value


def no_node_events(events):
    """A Node holding shadows alone publishes nothing (bit-law-v1, point 13)."""
    return {e["event"] for e in events} <= {"cycle_started", "cycle_committed"}


# (a) The single shadow of 12 at phase 6: whole quanta leave, the shares stay.
SINGLE_RAYS = {
    1: {
        (7, 7, 7): [(0, 6)],
        (5, 7, 7): [(1, 1)],
        (6, 8, 7): [(2, 1)],
        (6, 6, 7): [(3, 1)],
        (6, 7, 8): [(4, 1)],
        (6, 7, 6): [(5, 1)],
    },
    2: {(8, 7, 7): [(0, 3)]},
    3: {(9, 7, 7): [(0, 1)]},
}
SINGLE_REMAINDERS = {
    1: {(6, 7, 7): (6, 1, 1, 1, 1, 1)},
    2: {
        (6, 7, 7): (6, 1, 1, 1, 1, 1),
        (5, 7, 7): (1, 6, 1, 1, 1, 1),
        (6, 6, 7): (1, 1, 1, 6, 1, 1),
        (6, 7, 6): (1, 1, 1, 1, 1, 6),
        (6, 7, 8): (1, 1, 1, 1, 6, 1),
        (6, 8, 7): (1, 1, 6, 1, 1, 1),
        (7, 7, 7): (3, 6, 6, 6, 6, 6),
    },
}
SINGLE_REMAINDERS[3] = SINGLE_REMAINDERS[2] | {(8, 7, 7): (7, 3, 3, 3, 3, 3)}
# (b) Two shadows of 23 meeting head on: the phase of the coherent sum, then the
# steering (phase-spread-v1): the board after the step per case.
SUPERPOSITION = {
    "superposition": (
        6,
        23,
        7,
        {
            (7, 7, 7): [(0, 11)],
            (5, 7, 7): [(1, 11)],
            (6, 8, 7): [(2, 6)],
            (6, 6, 7): [(3, 6)],
            (6, 7, 8): [(4, 6)],
            (6, 7, 6): [(5, 6)],
        },
    ),
    "cancelled": (
        4,
        0,
        0,
        {(6, 8, 7): [(2, 12)], (6, 6, 7): [(3, 12)], (6, 7, 8): [(4, 12)], (6, 7, 6): [(5, 10)]},
    ),
}
# (c) A stream of single quanta through one Node's registers: the forward quantum
# released after every second arrival, a quantum on every heading at the eleventh.
STREAM_RELEASES = {2, 4, 6, 8, 10}


@pytest.mark.parametrize("case", ["single", "superposition", "cancelled", "stream", "sign", "rejected"])
def test_every_node_field_content_reaches_releases_it_again_by_the_declared_table(tmp_path, case):
    if case == "single":
        # (a) One shadow of 12 spreads at every Node it reaches, whole quanta by the
        # table, the shares below one quantum into the Node's registers; the total
        # is exact, and no Node publishes an event.
        world, events = simulate(document((((6, 7, 7), 12, 0, 6),)))
        assert rays_at(world, (6, 7, 7)) == [shadow(0, 12, 6)]
        assert remainder_map(world) == {}
        for tick in range(1, 4):
            world.step()
            assert world.totals() == {"light": (12,)}
            assert world.source_totals() == {"light": (0,)}
            assert all(item["balanced"] for item in world.spatial_accounting().values())
            assert world.audit()["balanced"]
            assert_board(world, SINGLE_RAYS[tick], 6)
            assert remainder_map(world) == SINGLE_REMAINDERS[tick]
        assert registers_at(world, (7, 7, 7)) == (
            block((3, 6, 6, 6, 6, 6)),
            phased(block((3, 6, 6, 6, 6, 6)), 6),
        )
        assert no_node_events(events)
        path = tmp_path / "single.json"
        path.write_text(json.dumps(document((((6, 7, 7), 12, 0, 6),))), encoding="utf-8")
        run_initialization(path, tmp_path / "out", ticks=3)
        metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
        assert metadata["field_spreading"] == FIELD_SPREADING == "field-spreading-v1"
        assert metadata["field_remainder"] == FIELD_REMAINDER == "field-remainder-v1"
        assert metadata["spreading_fields"] == [{"field": "light", "spread": SPREAD}]
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["final_totals"] == {"light": [12]}
        assert metadata["source_totals"] == {"light": [0]}
        assert metadata["real_content"] == [0, 0, 0] and metadata["shadow_content"] == [12] * 3
        recorded = [
            json.loads(line)
            for line in (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        assert no_node_events(recorded)
        state = json.loads((tmp_path / "out" / "state.json").read_text(encoding="utf-8"))
        # The shares below one quantum are parked shadows (node-is-ports-v1): one
        # per Node, owner, sign and heading, in units of the table's total.
        assert len({tuple(entry["position"]) for entry in state["parked"]}) == 8
        first = [entry for entry in state["parked"] if entry["position"] == [5, 7, 7]]
        assert {tuple(entry["heading"]): (entry["amount"], entry["phase"]) for entry in first} == {
            (1, 0, 0): (1, 6),
            (-1, 0, 0): (6, 6),
            (0, 1, 0): (1, 6),
            (0, -1, 0): (1, 6),
            (0, 0, 1): (1, 6),
            (0, 0, -1): (1, 6),
        }
        assert all(
            (entry["family"], entry["owner"], entry["sign"], entry["unit"], entry["bit"])
            == ("light", OWNER, 0, 11, 0)
            for entry in first
        )
        return
    if case in SUPERPOSITION:
        # (b) Two shadows of one owner meeting at a Node combine by phase and steer
        # each other (phase-spread-v1): each continues by the table at its phase
        # difference to the other, the rest apart, nothing into the registers, and
        # every departure carries the phase of the coherent sum.
        phase_b, stock, phase, board = SUPERPOSITION[case]
        world, events = simulate(document((((6, 7, 7), 23, 0, 0), ((6, 7, 7), 23, 1, phase_b)), ticks=1))
        assert positions_of(world) == {(6, 7, 7)}
        assert rays_at(world, (6, 7, 7)) == sorted(
            [shadow(0, 23, 0), shadow(1, 23, phase_b)], key=ray_merge_key
        )
        assert world.spatial_values((6, 7, 7))["light"]["value"] == (stock,)
        assert world.totals() == {"light": (46,)}
        world.step()
        assert_board(world, board, phase)
        assert registers_at(world, (6, 7, 7)) == (block(), (0,) * 18)
        assert world.totals() == {"light": (46,)}
        assert world.source_totals() == {"light": (0,)}
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        assert world.audit()["balanced"]
        assert no_node_events(events)
        return
    if case == "stream":
        # (c) A quantum fills the forward register by 6/11 per arrival and the
        # backward and transverse ones by 1/11: the second quantum releases
        # forward after two arrivals, a transverse quantum after eleven.
        assert relative_ports(0) == (0, 1, 2, 3, 4, 5) and relative_ports(3) == (3, 2, 0, 1, 4, 5)
        assert [stream_forward(n) for n in range(1, 12)] == [6, 1, 7, 2, 8, 3, 9, 4, 10, 5, 0]
        light = parse_initial_state(document((((6, 7, 7), 1, 0, 0),))).spatial_fields[0]
        held, held_phases = block(), (0,) * 18
        for n in range(1, 12):
            departures, taken, held, held_phases = spread_content(
                0, (shadow(0, 1, 0),), light, held, held_phases
            )
            forward = stream_forward(n)
            others = 0 if n == 11 else n
            released = (
                (1, 1, 1, 1, 1, 1) if n == 11 else ((1, *ZERO[1:]) if n in STREAM_RELEASES else ZERO)
            )
            assert taken.released == released, n
            assert taken.stored == (-5 if n == 11 else int(n % 2 == 1)), n
            assert held == block((forward, others, others, others, others, others)), n
            assert [(r.heading, r.amount) for r in departures] == [
                (heading, 1) for heading in range(6) if released[heading]
            ], n
        return
    if case == "sign":
        # (f) The sign of the source's charge travels on the shadow and into the
        # registers, kept through the spread, the registers and the merge, where
        # opposite signs stay two rays.
        light = parse_initial_state(document((((6, 7, 7), 1, 0, 0),))).spatial_fields[0]
        positive = shadow(0, 3, 0, 1)
        negative = shadow(0, 3, 0, -1)
        assert len(merge_rays((positive, negative))) == 2
        departures, taken, held, held_phases = spread_content(0, (positive, negative), light)
        assert departures == (shadow(0, 1, 0, -1, 0), shadow(0, 1, 0, 1, 0))
        both = block(minus=(7, 3, 3, 3, 3, 3), plus=(7, 3, 3, 3, 3, 3))
        assert (
            taken.amount,
            taken.arrived,
            taken.amounts,
            taken.released,
            taken.stored,
            taken.registers,
            taken.register_phases,
            taken.signs,
        ) == (6, (6, 0, 0, 0, 0, 0), (2, 0, 0, 0, 0, 0), ZERO, 4, both, (0,) * 18, (-1, 1))
        assert (held, held_phases) == (both, (0,) * 18)
        departures, taken, held, held_phases = spread_content(
            0, (shadow(0, 1, 0),), light, block((10, 0, 0, 0, 0, 0)), (0,) * 18
        )
        assert departures == (shadow(0, 1, 0, 0, 0),)
        assert (taken.released, taken.stored, held, held_phases) == (
            (1, 0, 0, 0, 0, 0),
            0,
            block((5, 1, 1, 1, 1, 1)),
            (0,) * 18,
        )
        pair = Ray(
            1,
            (0, 0, 0),
            2,
            outbound=0,
            event_ports=3,
            event_shares=(2, 2, 0, 0, 0, 0),
            source_sign=-1,
        )
        transmitted, ports = transmit(pair, light, "siblings")
        assert ports == (1,) and [(r.heading, r.amount, r.source_sign) for r in transmitted] == [
            (1, 2, -1)
        ]
        return
    # (d) A malformed table or an inadmissible family is rejected at initialization.
    plain = {k: v for k, v in ray_field("light", 0).items() if k != "kerengonen"}
    for spatial, message in (
        ([ray_field("light", 0, spread=[6, 1, 1, 1, 1])], "spread"),
        ([ray_field("light", 0, spread=[6, 1, -1, 1, 1, 1])], "spread"),
        ([ray_field("light", 0, spread=[6, 0, 1, 1, 1, 1])], "backward heading"),
        ([ray_field("light", 0, spread=[6, 1, 1, 1, 1, 2])], "one weight"),
        (
            [{"field": "light", "baseline": 0, "transport": "outward", "spread": SPREAD}],
            "require ray transport",
        ),
        ([plain | {"phase_bits": 13, "spread": SPREAD}], "twelve bits"),
        ([ray_field("light", 0, spread=SPREAD, headings=HEADINGS[:5])], "six Port headings"),
    ):
        raw = document((((6, 7, 7), 12, 0, 6),), spread=None)
        raw["spatial_fields"] = spatial
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
