"""Field spreading (field-spreading-v1, Highlights 3.5): every Node that field content
reaches releases it again in all six headings by the family's declared split table;
the content combines by phase before it spreads, each heading's content is shared in
whole quanta and the share below one quantum stays in the Node's remainder register
of that heading and sign (field-remainder-v1, Highlights 3.5 and 3.17), which
releases a whole quantum through its heading when it fills; the total is exact and
the momentum a spread moves is booked. The sign of the source's charge travels on
the field ray, and a returned field quantum walks back until something takes it (the
proposal of Highlights 5.5).

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Field spreading")
before the first run: single, superposition, cancelled, stream, sign, returned,
source, resident, rejected, unchanged.
"""

import hashlib
import json

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    DETECTOR_BIT_0,
    FIELD_REMAINDER,
    FIELD_SPREADING,
    Ray,
    merge_rays,
    ray_merge_key,
    relative_ports,
    release_field,
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
# The record hashes of the released-field world without spread, taken on main f3809be.
UNCHANGED_EVENTS = "8ab9901a4e5c2da7b4571e7438e674e528050c5fb61e894fbb7d18703adb8fa5"
UNCHANGED_STATE = "c13cd23158e5e461f171a8e2241ff793a24ccea531bd25ef54b28cfb2623e560"
KINDS = ("field_spread", "field_returned", "detector_return")


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


def world(fields, types, spatial, emissions, seeds, ticks, conservation=None, detectors=()):
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
        **({"conservation": conservation} if conservation else {}),
    }


def conserved(carrier, spatial):
    return {
        "name": "light",
        "energy_units": "quantum",
        "momentum_units": "quantum times heading",
        "carriers": [carrier],
        "spatial": {
            "energy": {"field": spatial, "side": "right"},
            "momentum": {"op": "vector", "args": [0, 0, 0]},
        },
    }


def document(lamps, spread=SPREAD, ticks=4, detectors=(), stock=None):
    """The board: `lamps` are (position, amount, heading index, phase) of `light`, each
    lamp holding `stock` (its amount by default) and emitting `amount` every interval
    it can pay, its recoil into its own `momentum` field, so the momentum line reads."""
    light = ray_field("light", 0) | ({"spread": list(spread)} if spread else {})
    return world(
        [field("light"), vector("momentum")],
        [
            {
                "name": f"lamp_{index}",
                "fields": ["light", "momentum"],
                "defaults": {"light": amount if stock is None else stock, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for index, (_, amount, _, _) in enumerate(lamps)
        ],
        [light],
        [
            {
                "type": f"lamp_{index}",
                "field": "light",
                "amount": amount,
                "denominator": 1,
                "source": False,
                "recoil_field": "momentum",
                "heading": HEADINGS[heading],
                "kerengonen_phase": phase,
            }
            for index, (_, amount, heading, phase) in enumerate(lamps)
        ],
        [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (position, _, _, _) in enumerate(lamps)
        ],
        ticks,
        conserved(
            {
                "requires": ["light", "momentum"],
                "energy": {"field": "light"},
                "momentum": {"field": "momentum"},
            },
            "light",
        ),
        detectors,
    )


def charged_world(emit, ticks, detectors=(), amount=4):
    """An electron (charge -3) whose field is `light`, spreading: a lamp emitting the
    electron along +X (`emit` True) or a record holding it still, which releases."""
    return world(
        [field("electron"), field("light")],
        [
            {
                "name": "charge",
                "fields": ["electron"],
                "defaults": {"electron": amount},
                "transport": {"mode": "hold"},
            }
        ],
        [
            ray_field("electron", 1, charge=-3),
            ray_field("light", 0, field_of="electron", release=[1, 4], spread=SPREAD),
        ],
        [
            {
                "type": "charge",
                "field": "electron",
                "amount": amount,
                "denominator": 1,
                "source": False,
                "heading": HEADINGS[0],
                "kerengonen_phase": 0,
            }
        ]
        if emit
        else [],
        [{"position": [5, 7, 7], "type": "charge"}],
        ticks,
        None
        if emit
        else conserved(
            {
                "requires": ["electron"],
                "energy": {"field": "electron"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
            "light",
        ),
        detectors,
    )


def released_world():
    """The released-field world of feature 7 without spread, for the record hashes."""
    return {
        "schema_version": 1,
        "model_id": "field-spreading-test-v1",
        "shape": [9, 7, 7],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": 6,
        "operation_costs": COSTS,
        "fields": [field("G"), field("electron")],
        "disturbance_types": [
            {
                "name": "lamp_0",
                "fields": ["electron"],
                "defaults": {"electron": 5},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            ray_field("electron", 1, 8),
            ray_field("G", 0, 16, field_of="electron", release=[1, 4]),
        ],
        "emissions": [
            {
                "type": "lamp_0",
                "field": "electron",
                "amount": 5,
                "denominator": 1,
                "source": False,
                "heading": HEADINGS[0],
                "kerengonen_phase": 0,
            }
        ],
        "seeds": [{"position": [2, 3, 3], "type": "lamp_0"}],
        "ray_interactions": [],
    }


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
    """The Node's remainder block of one family: eighteen registers and their phases."""
    node = world._spatial.nodes[position]
    index = family_index(world, family)
    return node.remainders[index], node.remainder_phases[index]


def remainder_map(world, family="light"):
    """Every nonzero block of sign 0 on the board, by position."""
    return {
        n.position: registers_at(world, n.position, family)[0][6:12]
        for n in world.inventory_view().nodes
        if n.remainders and any(n.remainders[family_index(world, family)])
    }


def record_of(world, type_index):
    return next(
        world.record_values(r)
        for node in world.nodes.values()
        for r in node.records
        if r is not None and r.type_index == type_index
    )


def emitted(heading, amount, phase, steps=1):
    """A lamp's ray: one event on the heading's Port."""
    shares = [0] * 6
    shares[heading] = amount
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        steps=steps,
        event_ports=1 << heading,
        event_shares=tuple(shares),
    )


def spread_ray(heading, amount, phase, sign=0):
    """A departure of a spread or a release, one Link on: no event, the combined phase."""
    return Ray(heading, (0, 0, 0), amount, phase=phase, steps=1, source_sign=sign)


def returned(steps, sign=0):
    """A returned light quantum walking back along -X: Detector bit 0, no event."""
    return Ray(1, (0, 0, 0), 1, steps=steps, outbound=0, detector=DETECTOR_BIT_0, source_sign=sign)


def block(zero=ZERO, minus=ZERO, plus=ZERO):
    """A family's eighteen registers, sign-major -1, 0, 1 then Port."""
    return (*minus, *zero, *plus)


def phased(registers, phase):
    """The phases of a block filled at one phase: the phase where content is, else 0."""
    return tuple(phase if value else 0 for value in registers)


def record(
    tick,
    position,
    arrived,
    amounts,
    stored,
    registers,
    released=ZERO,
    phase=6,
    coherence=(1, 1),
    signs=(0,),
):
    """A `field_spread` record: `registers` is the sign-0 block unless a full block."""
    full = registers if len(registers) == 18 else block(registers)
    return {
        "event": "field_spread",
        "tick": tick,
        "position": position,
        "family": "light",
        "amount": sum(arrived),
        "arrived": arrived,
        "amounts": amounts,
        "released": released,
        "stored": stored,
        "registers": full,
        "register_phases": phased(full, phase),
        "phase": phase,
        "coherence": coherence,
        "signs": signs,
    }


def simulate(raw, kinds=("field_spread",)):
    initial = parse_initial_state(raw)
    events = []
    world = Simulation(
        initial, observer=lambda event: events.append(event) if event["event"] in kinds else None
    )
    return world, events


def assert_board(world, expected, phase, sign=0):
    """Every Node holds exactly the (heading, amount) rays listed, at the given phase."""
    assert positions_of(world) == set(expected)
    for position, rays in expected.items():
        assert rays_at(world, position) == [spread_ray(h, a, phase, sign) for h, a in rays], position


def stream_forward(arrivals):
    """The forward register of a Node fed one quantum per arrival, after each arrival's
    release: 6 per arrival, less 11 whenever it reaches 11."""
    value = 0
    for _ in range(arrivals):
        value = (value + 6) % 11
    return value


# (a) The single ray of 12 at phase 6: whole quanta leave, the shares stay.
SINGLE_RAYS = {
    2: {
        (7, 7, 7): [(0, 6)],
        (5, 7, 7): [(1, 1)],
        (6, 8, 7): [(2, 1)],
        (6, 6, 7): [(3, 1)],
        (6, 7, 8): [(4, 1)],
        (6, 7, 6): [(5, 1)],
    },
    3: {(8, 7, 7): [(0, 3)]},
    4: {(9, 7, 7): [(0, 1)]},
}


def one_in(port):
    """A quantum arriving on `port` fills that Port's register by 6 and the rest by 1."""
    arrived = tuple(int(p == port) for p in range(6))
    return (arrived, ZERO, 1, tuple(6 if p == port else 1 for p in range(6)))


SINGLE_RECORDS = {
    1: [((6, 7, 7), (12, 0, 0, 0, 0, 0), (6, 1, 1, 1, 1, 1), 1, (6, 1, 1, 1, 1, 1))],
    2: [
        ((5, 7, 7), *one_in(1)),
        ((6, 6, 7), *one_in(3)),
        ((6, 7, 6), *one_in(5)),
        ((6, 7, 8), *one_in(4)),
        ((6, 8, 7), *one_in(2)),
        ((7, 7, 7), (6, 0, 0, 0, 0, 0), (3, 0, 0, 0, 0, 0), 3, (3, 6, 6, 6, 6, 6)),
    ],
    3: [((8, 7, 7), (3, 0, 0, 0, 0, 0), (1, 0, 0, 0, 0, 0), 2, (7, 3, 3, 3, 3, 3))],
}
SINGLE_MOMENTUM = {1: (0, 0, 0), 2: (-7, 0, 0), 3: (-9, 0, 0), 4: (-11, 0, 0)}
SINGLE_REMAINDERS = {
    2: {(6, 7, 7): (6, 1, 1, 1, 1, 1)},
    3: {
        (6, 7, 7): (6, 1, 1, 1, 1, 1),
        (5, 7, 7): (1, 6, 1, 1, 1, 1),
        (6, 6, 7): (1, 1, 1, 6, 1, 1),
        (6, 7, 6): (1, 1, 1, 1, 1, 6),
        (6, 7, 8): (1, 1, 1, 1, 6, 1),
        (6, 8, 7): (1, 1, 6, 1, 1, 1),
        (7, 7, 7): (3, 6, 6, 6, 6, 6),
    },
}
SINGLE_REMAINDERS[4] = SINGLE_REMAINDERS[3] | {(8, 7, 7): (7, 3, 3, 3, 3, 3)}
# (b) Two rays of 23 meeting head on: the phase of the coherent sum, then the split.
SUPERPOSITION = {"superposition": (6, 23, 7, (1, 2)), "cancelled": (4, 0, 0, (0, 1))}
# (c) A stream of single quanta: the records at (6,7,7) for n = 1 to 11, then the
# ticks at which (7,7,7), (8,7,7) and (9,7,7) record a spread.
STREAM_RELEASES = {2, 4, 6, 8, 10}
STREAM_SPREADS = {(7, 7, 7): [3, 5, 7, 9, 11], (8, 7, 7): [6, 10], (9, 7, 7): [11]}
STREAM_REMAINDERS = {
    (7, 7, 7): (8, 5, 5, 5, 5, 5),
    (8, 7, 7): (1, 2, 2, 2, 2, 2),
    (9, 7, 7): (6, 1, 1, 1, 1, 1),
}
# (f) The five light rays an electron of 4 releases at (6,7,7) in the interval of
# tick 2 (phase 1, into the registers of the Nodes around) and at (7,7,7) in the
# interval of tick 3 (phase 2, on the board after tick 3), each 1, sign -1.
SIGN_RAYS = {
    (6, 7, 7): (1, 2),
    (7, 8, 7): (2, 2),
    (7, 6, 7): (3, 2),
    (7, 7, 8): (4, 2),
    (7, 7, 6): (5, 2),
}
SIGN_REMAINDERS = {
    (5, 7, 7): (1, 6, 1, 1, 1, 1),
    (6, 8, 7): (1, 1, 6, 1, 1, 1),
    (6, 6, 7): (1, 1, 1, 6, 1, 1),
    (6, 7, 8): (1, 1, 1, 1, 6, 1),
    (6, 7, 6): (1, 1, 1, 1, 1, 6),
}
# (g) The second quantum releases the first forward; a Detector at (7,7,7) returns
# it and it walks back to its lamp, which takes it back: where it is after each tick.
RETURNED_PATH = {
    1: {(6, 7, 7): [emitted(0, 1, 0)]},
    2: {(6, 7, 7): [emitted(0, 1, 0)]},
    3: {(7, 7, 7): [returned(1)]},
    4: {(6, 7, 7): [returned(0)]},
    5: {(5, 7, 7): [returned(0)]},
    6: {},
}
# (h) The +X line after tick 12: the twelfth release and the second returned quantum
# at (6,7,7), the quantum (6,7,7) released in the interval of tick 12 at (7,7,7).
SOURCE_LINE = {
    (6, 7, 7): [spread_ray(0, 1, 0, -1), returned(0, -1)],
    (7, 7, 7): [spread_ray(0, 1, 0, -1)],
    (8, 7, 7): [],
}


@pytest.mark.parametrize(
    "case",
    [
        "single",
        "superposition",
        "cancelled",
        "stream",
        "sign",
        "returned",
        "source",
        "resident",
        "rejected",
        "unchanged",
    ],
)
def test_every_node_field_content_reaches_releases_it_again_by_the_declared_table(tmp_path, case):
    if case == "single":
        # (a) One ray of 12 spreads at every Node it reaches, whole quanta by the
        # table, the shares below one quantum into the Node's registers; the total
        # is exact and the momentum the spreads move is the source.
        world, events = simulate(document((((5, 7, 7), 12, 0, 6),)))
        for tick in range(1, 5):
            world.step()
            assert world.totals() == {"light": (12,), "momentum": SINGLE_MOMENTUM[tick]}
            assert world.source_totals() == {"light": (0,), "momentum": SINGLE_MOMENTUM[tick]}
            assert all(item["balanced"] for item in world.spatial_accounting().values())
            assert world.audit()["balanced"]
            if tick == 1:
                assert positions_of(world) == {(6, 7, 7)}
                assert rays_at(world, (6, 7, 7)) == [emitted(0, 12, 6)]
                assert events == [] and remainder_map(world) == {}
                continue
            assert_board(world, SINGLE_RAYS[tick], 6)
            assert remainder_map(world) == SINGLE_REMAINDERS[tick]
            assert [e for e in events if e["tick"] == tick - 1] == [
                record(tick - 1, *entry) for entry in SINGLE_RECORDS[tick - 1]
            ]
        assert registers_at(world, (7, 7, 7)) == (
            block((3, 6, 6, 6, 6, 6)),
            phased(block((3, 6, 6, 6, 6, 6)), 6),
        )
        assert len(events) == 8
        assert world.conservation_report()["status"] == "passed"
        path = tmp_path / "single.json"
        path.write_text(json.dumps(document((((5, 7, 7), 12, 0, 6),))), encoding="utf-8")
        run_initialization(path, tmp_path / "out", ticks=4)
        metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
        assert metadata["field_spreading"] == FIELD_SPREADING == "field-spreading-v1"
        assert metadata["field_remainder"] == FIELD_REMAINDER == "field-remainder-v1"
        assert metadata["spreading_fields"] == [{"field": "light", "spread": SPREAD}]
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["local_conservation"]["status"] == "passed"
        assert metadata["final_totals"] == {"light": [12], "momentum": [-11, 0, 0]}
        assert metadata["source_totals"] == {"light": [0], "momentum": [-11, 0, 0]}
        recorded = [
            json.loads(line)
            for line in (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        assert sum(1 for e in recorded if e["event"] == "field_spread") == 8
        assert next(e for e in recorded if e["event"] == "field_spread") == json.loads(
            json.dumps(record(1, *SINGLE_RECORDS[1][0]))
        )
        state = json.loads((tmp_path / "out" / "state.json").read_text(encoding="utf-8"))
        assert len(state["field_remainders"]) == 8
        assert state["field_remainders"][0] == {
            "position": [5, 7, 7],
            "family": "light",
            "sign": 0,
            "registers": [1, 6, 1, 1, 1, 1],
            "phases": [6, 6, 6, 6, 6, 6],
            "total": 11,
        }
        return
    if case in SUPERPOSITION:
        # (b) Two rays of one family meeting at a Node combine by phase before
        # they spread: the registers take the shares at the phase of the coherent
        # sum.
        phase_b, stock, phase, coherence = SUPERPOSITION[case]
        world, events = simulate(document((((5, 7, 7), 23, 0, 0), ((7, 7, 7), 23, 1, phase_b)), ticks=2))
        world.step()
        assert positions_of(world) == {(6, 7, 7)}
        assert rays_at(world, (6, 7, 7)) == sorted(
            [emitted(0, 23, 0), emitted(1, 23, phase_b)], key=ray_merge_key
        )
        assert world.spatial_values((6, 7, 7))["light"]["value"] == (stock,)
        assert world.totals() == {"light": (46,), "momentum": (0, 0, 0)}
        world.step()
        amounts = (14, 14, 4, 4, 4, 4)
        assert events == [
            record(
                1,
                (6, 7, 7),
                (23, 23, 0, 0, 0, 0),
                amounts,
                2,
                (7, 7, 2, 2, 2, 2),
                phase=phase,
                coherence=coherence,
            )
        ]
        assert_board(
            world,
            {
                (7, 7, 7): [(0, 14)],
                (5, 7, 7): [(1, 14)],
                (6, 8, 7): [(2, 4)],
                (6, 6, 7): [(3, 4)],
                (6, 7, 8): [(4, 4)],
                (6, 7, 6): [(5, 4)],
            },
            phase,
        )
        assert registers_at(world, (6, 7, 7)) == (
            block((7, 7, 2, 2, 2, 2)),
            phased(block((7, 7, 2, 2, 2, 2)), phase),
        )
        assert world.totals() == {"light": (46,), "momentum": (0, 0, 0)}
        assert world.source_totals() == {"light": (0,), "momentum": (0, 0, 0)}
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        assert world.audit()["balanced"]
        assert world.conservation_report()["status"] == "passed"
        return
    if case == "stream":
        # (c) A ray of amount 1 fills the forward register by 6/11 per arrival and
        # the backward and transverse ones by 1/11: the second quantum releases
        # forward after two arrivals, a transverse quantum after eleven.
        assert relative_ports(0) == (0, 1, 2, 3, 4, 5) and relative_ports(3) == (3, 2, 0, 1, 4, 5)
        assert [stream_forward(n) for n in range(1, 12)] == [6, 1, 7, 2, 8, 3, 9, 4, 10, 5, 0]
        world, events = simulate(document((((5, 7, 7), 1, 0, 0),), ticks=12, stock=12))
        for _ in range(12):
            world.step()
            assert world.totals()["light"] == (12,)
            assert world.audit()["balanced"]
            assert all(item["balanced"] for item in world.spatial_accounting().values())
        at_source = [e for e in events if e["position"] == (6, 7, 7)]
        assert [e["tick"] for e in at_source] == list(range(1, 12))
        for n, event in enumerate(at_source, start=1):
            forward = stream_forward(n)
            others = 0 if n == 11 else n
            released = (
                (1, 1, 1, 1, 1, 1) if n == 11 else ((1, *ZERO[1:]) if n in STREAM_RELEASES else ZERO)
            )
            stored = -5 if n == 11 else int(n % 2 == 1)
            assert event == record(
                n,
                (6, 7, 7),
                (1, 0, 0, 0, 0, 0),
                released,
                stored,
                (forward, others, others, others, others, others),
                released,
                phase=0,
            ), n
        assert {
            position: [e["tick"] for e in events if e["position"] == position]
            for position in STREAM_SPREADS
        } == STREAM_SPREADS
        assert len(events) == 19
        assert [e["released"] for e in events if e["position"] == (7, 7, 7)] == [
            ZERO,
            (1, 0, 0, 0, 0, 0),
            ZERO,
            (1, 0, 0, 0, 0, 0),
            ZERO,
        ]
        assert rays_at(world, (6, 7, 7)) == [emitted(0, 1, 0)]
        for position, heading in (
            ((7, 7, 7), 0),
            ((5, 7, 7), 1),
            ((6, 8, 7), 2),
            ((6, 6, 7), 3),
            ((6, 7, 8), 4),
            ((6, 7, 6), 5),
        ):
            assert rays_at(world, position) == [spread_ray(heading, 1, 0)], position
        assert len(positions_of(world)) == 7
        assert remainder_map(world) == STREAM_REMAINDERS
        assert record_of(world, 0)["light"] == (0,)
        assert world.conservation_report()["status"] == "passed"
        return
    if case == "sign":
        # (f) The sign of the source's charge travels on the field ray and into the
        # registers: an electron of charge -3 releases light of sign -1, kept
        # through the spread, the registers and the merge, where opposite signs
        # stay two rays.
        world, events = simulate(charged_world(True, 3))
        initial = world.initial
        electron, light = initial.spatial_fields
        for _ in range(3):
            world.step()
        assert rays_at(world, (8, 7, 7), "electron") == [emitted(0, 4, 3, 3)]
        assert positions_of(world) == set(SIGN_RAYS)
        for position, (heading, phase) in SIGN_RAYS.items():
            assert rays_at(world, position) == [spread_ray(heading, 1, phase, -1)], position
        for position, registers in SIGN_REMAINDERS.items():
            assert registers_at(world, position) == (
                block(minus=registers),
                phased(block(minus=registers), 1),
            ), position
        assert world.totals() == {"electron": (4,), "light": (10,)}
        assert world.source_totals() == {"electron": (0,), "light": (10,)}
        assert world.audit()["balanced"]
        assert [(e["tick"], e["signs"], e["stored"], e["released"]) for e in events] == [
            (2, (-1,), 1, ZERO)
        ] * 5
        assert release_field((emitted(0, 4, 1),), light, electron) == tuple(
            Ray(heading, (0, 0, 0), 1, phase=1, source_sign=-1) for heading in range(1, 6)
        )
        positive = Ray(0, (0, 0, 0), 3, steps=1, source_sign=1)
        negative = Ray(0, (0, 0, 0), 3, steps=1, source_sign=-1)
        assert len(merge_rays((positive, negative))) == 2
        departures, taken, held, held_phases = spread_content(1, (positive, negative), light)
        assert departures == (
            Ray(0, (0, 0, 0), 1, source_sign=-1),
            Ray(0, (0, 0, 0), 1, source_sign=1),
        )
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
        one = Ray(0, (0, 0, 0), 1, steps=1)
        departures, taken, held, held_phases = spread_content(
            1, (one,), light, block((10, 0, 0, 0, 0, 0)), (0,) * 18
        )
        assert departures == (Ray(0, (0, 0, 0), 1),)
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
    if case == "returned":
        # (g) A quantum a Detector returns with 0 walks back along the line it
        # arrived by, past the Node that spread it, with no inverse split, until its
        # emitter takes it back: stock and recoil restored exactly.
        detector = {"position": [7, 7, 7], "setting": [0, 1], "seed": 1}
        raw = document((((5, 7, 7), 1, 0, 0),), ticks=6, detectors=[detector], stock=2)
        world, events = simulate(raw, KINDS)
        for tick in range(1, 7):
            world.step()
            momentum = (0, 0, 0) if tick == 1 else (-1, 0, 0)
            assert world.totals() == {"light": (2,), "momentum": momentum}
            assert world.source_totals() == {"light": (0,), "momentum": momentum}
            assert world.audit()["balanced"]
            expected = RETURNED_PATH[tick]
            assert positions_of(world) == set(expected)
            for position, rays in expected.items():
                assert rays_at(world, position) == rays, position
            assert remainder_map(world) == (
                {} if tick == 1 else {(6, 7, 7): (6, 1, 1, 1, 1, 1) if tick == 2 else (1, 2, 2, 2, 2, 2)}
            )
        assert record_of(world, 0) == {"light": (1,), "momentum": (-1, 0, 0)}
        assert [(e["event"], e["tick"]) for e in events] == [
            ("field_spread", 1),
            ("field_spread", 2),
            ("detector_return", 3),
            ("field_returned", 5),
        ]
        assert [(e["released"], e["stored"]) for e in events[:2]] == [(ZERO, 1), ((1, *ZERO[1:]), 0)]
        assert events[-1] == {
            "event": "field_returned",
            "tick": 5,
            "position": (5, 7, 7),
            "family": "light",
            "amount": 1,
            "port": 1,
            "by": None,
            "restored": True,
        }
        assert world.conservation_report()["status"] == "passed"
        path = tmp_path / "returned.json"
        path.write_text(json.dumps(raw), encoding="utf-8")
        run_initialization(path, tmp_path / "out", ticks=6)
        metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["local_conservation"]["status"] == "passed"
        assert metadata["final_totals"] == {"light": [2], "momentum": [-1, 0, 0]}
        return
    if case == "source":
        # (h) A record of electrons radiates light every interval; the Detector at
        # (8,7,7) returns every quantum the registers release that far, which walks
        # back to its source and ends there, its release unbooked; nothing escapes.
        detector = {"position": [8, 7, 7], "setting": [0, 1], "seed": 1}
        world, events = simulate(charged_world(False, 12, [detector]), KINDS)
        for tick in range(1, 13):
            world.step()
            unbooked = int(tick >= 10)
            assert world.totals()["light"] == (6 * tick - unbooked,)
            assert world.source_totals()["light"] == (6 * tick - unbooked,)
            assert world.escaped_totals()["light"] == (0,)
            assert world.audit()["balanced"]
        for position, rays in SOURCE_LINE.items():
            assert rays_at(world, position) == sorted(rays, key=ray_merge_key), position
        assert [e["tick"] for e in events if e["event"] == "detector_return"] == [6, 10]
        assert [e for e in events if e["event"] == "field_returned"] == [
            {
                "event": "field_returned",
                "tick": 9,
                "position": (5, 7, 7),
                "family": "light",
                "amount": 1,
                "port": 1,
                "by": "electron",
                "restored": False,
            }
        ]
        assert [
            e["tick"] for e in events if e["position"] == (7, 7, 7) and e["event"] == "field_spread"
        ] == [
            3,
            5,
            7,
            9,
            11,
        ]
        assert registers_at(world, (7, 7, 7)) == (block(minus=(8, 5, 5, 5, 5, 5)), (0,) * 18)
        assert world.conservation_report()["status"] == "passed"
        return
    if case == "resident":
        # (i) A record holding stock of a family with a field releases every
        # interval, two per heading from 8 at release 1/4, booked as a source; the
        # Node cycles for it (a defect fixed on 2026-09-17: the idle exit came first).
        world, events = simulate(charged_world(False, 4, amount=8))
        for tick in range(1, 5):
            world.step()
            assert world.totals() == {"electron": (8,), "light": (12 * tick,)}
            assert world.source_totals() == {"electron": (0,), "light": (12 * tick,)}
            assert world.audit()["balanced"]
            assert record_of(world, 0) == {"electron": (8,)}
            expected = {
                (5 + d * h[0], 7 + d * h[1], 7 + d * h[2]): [(heading, 2 if d == 1 else 1)]
                for heading, h in enumerate(HEADINGS)
                for d in (1, 2, 3)
                if d == 1 or (d == 2 and tick >= 2) or (d == 3 and tick >= 4)
            }
            assert_board(world, expected, 0, -1)
        assert registers_at(world, (6, 7, 7)) == (block(minus=(3, 6, 6, 6, 6, 6)), (0,) * 18)
        assert registers_at(world, (7, 7, 7)) == (block(minus=(1, 2, 2, 2, 2, 2)), (0,) * 18)
        assert registers_at(world, (5, 6, 7)) == (block(minus=(6, 6, 6, 3, 6, 6)), (0,) * 18)
        assert [
            (e["tick"], e["position"], e["stored"]) for e in events if e["position"][1:] == (7, 7)
        ] == [
            (1, (4, 7, 7), 1),
            (1, (6, 7, 7), 1),
            (2, (3, 7, 7), 1),
            (2, (4, 7, 7), 1),
            (2, (6, 7, 7), 1),
            (2, (7, 7, 7), 1),
            (3, (3, 7, 7), 0),
            (3, (4, 7, 7), 1),
            (3, (6, 7, 7), 1),
            (3, (7, 7, 7), 0),
        ]
        assert world.conservation_report()["status"] == "passed"
        return
    if case == "rejected":
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
            raw = document((((5, 7, 7), 12, 0, 6),), spread=None)
            raw["spatial_fields"] = spatial
            with pytest.raises(ValueError, match=message):
                parse_initial_state(raw)
        return
    # (e) A world that declares no spread runs byte-identically: the released-field
    # world of feature 7 gives the record hashes taken before this feature.
    path = tmp_path / "released.json"
    path.write_text(json.dumps(released_world()), encoding="utf-8")
    run_initialization(path, tmp_path / "out", ticks=6)
    digests = {
        name: hashlib.sha256((tmp_path / "out" / name).read_bytes()).hexdigest()
        for name in ("events.jsonl", "state.json")
    }
    assert digests == {"events.jsonl": UNCHANGED_EVENTS, "state.json": UNCHANGED_STATE}
    metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
    assert "field_spreading" not in metadata and "spreading_fields" not in metadata
    assert "field_remainder" not in metadata
    assert "field_remainders" not in json.loads((tmp_path / "out" / "state.json").read_text())
    assert metadata["final_totals"] == {"G": [16], "electron": [5]}
    assert metadata["escaped_totals"]["G"] == [9]
    assert metadata["released_fields"] == [{"field": "G", "field_of": "electron", "release": [1, 4]}]
