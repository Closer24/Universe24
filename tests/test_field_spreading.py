"""Field spreading (field-spreading-v1, Highlights 3.5): every Node that field content
reaches releases it again in all six headings by the family's declared split table;
the content combines by phase before it spreads, each heading's content is shared in
whole quanta and the remainder leaves whole through the entry the phase selects, so
a quantum never waits; the total is exact and the momentum a spread moves is booked.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("Field spreading")
before the first run: single, superposition, cancelled, quantum, rejected, unchanged.
"""

import hashlib
import json

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    FIELD_SPREADING,
    Ray,
    ray_merge_key,
    relative_ports,
    spread_remainder_entry,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
# Forward 6/11, backward 1/11, each transverse 1/11.
SPREAD = [6, 1, 1, 1, 1, 1]
COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}
# The record hashes of the released-field world without spread, taken on main f3809be.
UNCHANGED_EVENTS = "8ab9901a4e5c2da7b4571e7438e674e528050c5fb61e894fbb7d18703adb8fa5"
UNCHANGED_STATE = "c13cd23158e5e461f171a8e2241ff793a24ccea531bd25ef54b28cfb2623e560"


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


def document(lamps, spread=SPREAD, ticks=4):
    """The board: `lamps` are (position, amount, heading index, phase) of `light`, each
    lamp's recoil into its own `momentum` field, so the momentum ledger line reads."""
    light = ray_field("light", 0) | ({"spread": list(spread)} if spread else {})
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
        "fields": [field("light"), vector("momentum")],
        "disturbance_types": [
            {
                "name": f"lamp_{index}",
                "fields": ["light", "momentum"],
                "defaults": {"light": amount, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
            for index, (_, amount, _, _) in enumerate(lamps)
        ],
        "spatial_fields": [light],
        "emissions": [
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
        "seeds": [
            {"position": list(position), "type": f"lamp_{index}"}
            for index, (position, _, _, _) in enumerate(lamps)
        ],
        "conservation": {
            "name": "light",
            "energy_units": "quantum",
            "momentum_units": "quantum times heading",
            "carriers": [
                {
                    "requires": ["light", "momentum"],
                    "energy": {"field": "light"},
                    "momentum": {"field": "momentum"},
                }
            ],
            "spatial": {
                "energy": {"field": "light", "side": "right"},
                "momentum": {"op": "vector", "args": [0, 0, 0]},
            },
        },
    }


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


def rays_at(world, position, family="light"):
    """The resident rays of one family at a Node, in merge-key order."""
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    node = bundles(world, position)
    return sorted(node[index], key=ray_merge_key) if node else []


def positions_of(world, family="light"):
    return {n.position for n in world.inventory_view().nodes if rays_at(world, n.position, family)}


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


def spread_ray(heading, amount, phase):
    """A departure of a spread, one Link on: no event, the combined phase."""
    return Ray(heading, (0, 0, 0), amount, phase=phase, steps=1)


def record(tick, position, arrived, amounts, remainders, phase=6, coherence=(1, 1)):
    return {
        "event": "field_spread",
        "tick": tick,
        "position": position,
        "family": "light",
        "amount": sum(arrived),
        "arrived": arrived,
        "amounts": amounts,
        "remainders": remainders,
        "phase": phase,
        "coherence": coherence,
    }


def simulate(raw):
    initial = parse_initial_state(raw)
    events = []
    world = Simulation(
        initial,
        observer=lambda event: events.append(event) if event["event"] == "field_spread" else None,
    )
    return world, events


def assert_board(world, expected, phase):
    """Every Node holds exactly the (heading, amount) rays listed, at the given phase."""
    assert positions_of(world) == set(expected)
    for position, rays in expected.items():
        assert rays_at(world, position) == [spread_ray(h, a, phase) for h, a in rays], position


# (a) The single ray of 12 at phase 6: its remainder leaves through the second transverse.
SINGLE_RAYS = {
    2: {
        (7, 7, 7): [(0, 6)],
        (5, 7, 7): [(1, 1)],
        (6, 8, 7): [(2, 1)],
        (6, 6, 7): [(3, 2)],
        (6, 7, 8): [(4, 1)],
        (6, 7, 6): [(5, 1)],
    },
    3: {
        (8, 7, 7): [(0, 3)],
        (7, 6, 7): [(3, 3)],
        (5, 6, 7): [(1, 1), (3, 1)],
        (5, 8, 7): [(1, 1)],
        (6, 5, 7): [(3, 1)],
        (5, 7, 8): [(1, 1)],
        (5, 7, 6): [(1, 1)],
    },
    4: {
        (9, 7, 7): [(0, 1)],
        (8, 6, 7): [(3, 2)],
        (7, 5, 7): [(3, 1)],
        (6, 6, 7): [(1, 2)],
        (4, 6, 7): [(1, 1)],
        (5, 5, 7): [(1, 1), (3, 1)],
        (5, 7, 7): [(3, 1)],
        (5, 6, 8): [(3, 1)],
        (5, 6, 6): [(3, 1)],
    },
}
ONE_BACK = ((0, 1, 0, 0, 0, 0), (0, 0, 0, 1, 0, 0), (0, 0, 0, 1, 0, 0))
ONE_LEFT = ((0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0))
SINGLE_RECORDS = {
    1: [((6, 7, 7), (12, 0, 0, 0, 0, 0), (6, 1, 1, 2, 1, 1), (0, 0, 0, 1, 0, 0))],
    2: [
        ((5, 7, 7), *ONE_BACK),
        ((6, 6, 7), (0, 0, 0, 2, 0, 0), (0, 1, 0, 1, 0, 0), (0, 1, 0, 0, 0, 0)),
        ((6, 7, 6), (0, 0, 0, 0, 0, 1), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0)),
        ((6, 7, 8), (0, 0, 0, 0, 1, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0)),
        ((6, 8, 7), (0, 0, 1, 0, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0)),
        ((7, 7, 7), (6, 0, 0, 0, 0, 0), (3, 0, 0, 3, 0, 0), (0, 0, 0, 3, 0, 0)),
    ],
    3: [
        ((5, 6, 7), (0, 1, 0, 1, 0, 0), (0, 1, 0, 1, 0, 0), (0, 1, 0, 1, 0, 0)),
        ((5, 7, 6), *ONE_BACK),
        ((5, 7, 8), *ONE_BACK),
        ((5, 8, 7), *ONE_BACK),
        ((6, 5, 7), (0, 0, 0, 1, 0, 0), (0, 1, 0, 0, 0, 0), (0, 1, 0, 0, 0, 0)),
        ((7, 6, 7), (0, 0, 0, 3, 0, 0), (0, 2, 0, 1, 0, 0), (0, 2, 0, 0, 0, 0)),
        ((8, 7, 7), (3, 0, 0, 0, 0, 0), (1, 0, 0, 2, 0, 0), (0, 0, 0, 2, 0, 0)),
    ],
}
SINGLE_MOMENTUM = {1: (0, 0, 0), 2: (-7, -1, 0), 3: (-13, -5, 0), 4: (-15, -7, 0)}
# (b) Two rays of 23 meeting head on: the phase of the coherent sum, then the split.
SUPERPOSITION = {
    "superposition": (6, 23, 7, (1, 2), (14, 14, 4, 4, 6, 4), (0, 0, 0, 0, 2, 0), (0, 0, 2)),
    "cancelled": (4, 0, 0, (0, 1), (15, 15, 4, 4, 4, 4), (1, 1, 0, 0, 0, 0), (0, 0, 0)),
}
# (c) One quantum at phase 7 turns to its third transverse at every Node.
QUANTUM_PATH = {
    1: ((6, 7, 7), 0),
    2: ((6, 7, 8), 4),
    3: ((6, 8, 8), 2),
    4: ((6, 8, 9), 4),
    5: ((6, 9, 9), 2),
    6: ((6, 9, 10), 4),
}
QUANTUM_MOMENTUM = {
    1: (0, 0, 0),
    2: (-1, 0, 1),
    3: (-1, 1, 0),
    4: (-1, 0, 1),
    5: (-1, 1, 0),
    6: (-1, 0, 1),
}


@pytest.mark.parametrize(
    "case", ["single", "superposition", "cancelled", "quantum", "rejected", "unchanged"]
)
def test_every_node_field_content_reaches_releases_it_again_by_the_declared_table(tmp_path, case):
    if case == "single":
        # (a) One ray of 12 spreads at every Node it reaches, whole quanta by the
        # table, the remainder through the heading its phase selects; the total is
        # exact and the momentum the spreads move is the source.
        world, events = simulate(document((((5, 7, 7), 12, 0, 6),)))
        for tick in range(1, 5):
            world.step()
            assert world.totals() == {"light": (12,), "momentum": SINGLE_MOMENTUM[tick]}
            assert world.source_totals() == {"light": (0,), "momentum": SINGLE_MOMENTUM[tick]}
            assert all(item["balanced"] for item in world.spatial_accounting().values())
            if tick == 1:
                assert positions_of(world) == {(6, 7, 7)}
                assert rays_at(world, (6, 7, 7)) == [emitted(0, 12, 6)]
                assert events == []
                continue
            assert_board(world, SINGLE_RAYS[tick], 6)
            assert [e for e in events if e["tick"] == tick - 1] == [
                record(tick - 1, *entry) for entry in SINGLE_RECORDS[tick - 1]
            ]
        assert len(events) == 14
        assert world.conservation_report()["status"] == "passed"
        path = tmp_path / "single.json"
        path.write_text(json.dumps(document((((5, 7, 7), 12, 0, 6),))), encoding="utf-8")
        run_initialization(path, tmp_path / "out", ticks=4)
        metadata = json.loads((tmp_path / "out" / "run.json").read_text(encoding="utf-8"))
        assert metadata["field_spreading"] == FIELD_SPREADING == "field-spreading-v1"
        assert metadata["spreading_fields"] == [{"field": "light", "spread": SPREAD}]
        assert metadata["conserved_at_every_completed_tick"]
        assert metadata["local_conservation"]["status"] == "passed"
        assert metadata["final_totals"] == {"light": [12], "momentum": [-15, -7, 0]}
        assert metadata["source_totals"] == {"light": [0], "momentum": [-15, -7, 0]}
        recorded = [
            json.loads(line)
            for line in (tmp_path / "out" / "events.jsonl").read_text(encoding="utf-8").splitlines()
        ]
        assert sum(1 for e in recorded if e["event"] == "field_spread") == 14
        assert next(e for e in recorded if e["event"] == "field_spread") == json.loads(
            json.dumps(record(1, *SINGLE_RECORDS[1][0]))
        )
        return
    if case in SUPERPOSITION:
        # (b) Two rays of one family meeting at a Node combine by phase before
        # they spread: the phase of the coherent sum places both remainders.
        phase_b, stock, phase, coherence, amounts, remainders, momentum = SUPERPOSITION[case]
        world, events = simulate(document((((5, 7, 7), 23, 0, 0), ((7, 7, 7), 23, 1, phase_b)), ticks=2))
        world.step()
        assert positions_of(world) == {(6, 7, 7)}
        assert rays_at(world, (6, 7, 7)) == sorted(
            [emitted(0, 23, 0), emitted(1, 23, phase_b)], key=ray_merge_key
        )
        assert world.spatial_values((6, 7, 7))["light"]["value"] == (stock,)
        assert world.totals() == {"light": (46,), "momentum": (0, 0, 0)}
        world.step()
        assert events == [
            record(1, (6, 7, 7), (23, 23, 0, 0, 0, 0), amounts, remainders, phase, coherence)
        ]
        assert_board(
            world,
            {
                (7, 7, 7): [(0, amounts[0])],
                (5, 7, 7): [(1, amounts[1])],
                (6, 8, 7): [(2, amounts[2])],
                (6, 6, 7): [(3, amounts[3])],
                (6, 7, 8): [(4, amounts[4])],
                (6, 7, 6): [(5, amounts[5])],
            },
            phase,
        )
        assert world.totals() == {"light": (46,), "momentum": momentum}
        assert world.source_totals() == {"light": (0,), "momentum": momentum}
        assert all(item["balanced"] for item in world.spatial_accounting().values())
        assert world.conservation_report()["status"] == "passed"
        return
    if case == "quantum":
        # (c) A single quantum cannot split and never waits: it keeps moving one
        # Link per interval on the path its phase sets.
        assert [spread_remainder_entry(p, 8, tuple(SPREAD)) for p in range(8)] == [
            0,
            0,
            0,
            0,
            0,
            1,
            3,
            4,
        ]
        assert relative_ports(0) == (0, 1, 2, 3, 4, 5) and relative_ports(3) == (3, 2, 0, 1, 4, 5)
        world, events = simulate(document((((5, 7, 7), 1, 0, 7),), ticks=6))
        for tick in range(1, 7):
            world.step()
            position, heading = QUANTUM_PATH[tick]
            assert positions_of(world) == {position}
            expected = emitted(0, 1, 7) if tick == 1 else spread_ray(heading, 1, 7)
            assert rays_at(world, position) == [expected]
            assert world.totals() == {"light": (1,), "momentum": QUANTUM_MOMENTUM[tick]}
            assert world.source_totals() == {"light": (0,), "momentum": QUANTUM_MOMENTUM[tick]}
        assert [(e["tick"], e["position"], e["remainders"]) for e in events] == [
            (
                tick - 1,
                QUANTUM_PATH[tick - 1][0],
                tuple(int(p == QUANTUM_PATH[tick][1]) for p in range(6)),
            )
            for tick in range(2, 7)
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
            ([plain | {"phase_bits": 3, "spread": SPREAD}], "coherence table"),
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
    assert metadata["final_totals"] == {"G": [16], "electron": [5]}
    assert metadata["escaped_totals"]["G"] == [9]
    assert metadata["released_fields"] == [{"field": "G", "field_of": "electron", "release": [1, 4]}]
