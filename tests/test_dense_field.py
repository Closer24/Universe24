"""The dense mode for boards that a field fills (dense-field-v1, docs/PERFORMANCE.md):
the pure-field Nodes of a board cycled as one vectorized step over integer arrays
that applies the spread and remainder rule of field-spreading-v1 and
field-remainder-v1 to every such Node at once, exactly; a ray leaving a dense Node
toward a sparse Node (a mark, a body, a lamp, a Node holding a returning or another
family's ray) handed over as an ordinary packet and a packet leaving a sparse Node
into the dense region absorbed into the arrays; the same `state.json` and the same
ledger as the engine alone, which is the mode's acceptance test.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The dense mode") before
the first run: split, boundary, identity, rejected.
"""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    DENSE_FIELD,
    DETECTOR_BIT_0,
    DETECTOR_BIT_1,
    Ray,
    SpatialPacket,
    ray_merge_key,
    remainder_slot,
    spread_content,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
ZERO = (0, 0, 0, 0, 0, 0)


def _spreading():
    """The board builders of test_field_spreading.py, loaded as data."""
    spec = importlib.util.spec_from_file_location(
        "field_spreading_boards", ROOT / "tests" / "test_field_spreading.py"
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def dense_document(raw):
    """The same world under the dense mode: no local audit (a dense Node publishes
    no per-Node events for it to read), `dense_field` on."""
    raw = dict(raw)
    raw.pop("conservation", None)
    raw["dense_field"] = True
    return raw


def engine_document(raw):
    raw = dict(raw)
    raw.pop("conservation", None)
    return raw


def spread_ray(heading, amount, phase, sign=0, bit=0):
    return Ray(heading, (0, 0, 0), amount, phase=phase, steps=1, detector=bit, source_sign=sign)


def region(world):
    dense = world._spatial.dense
    assert dense is not None
    return dense


def light(world):
    names = [f.name for f in world.initial.fields]
    index = [f.field for f in world.initial.spatial_fields].index(names.index("light"))
    return region(world).families[index]


def place(family, position, port, ray):
    """One arrived ray into the arrays at a Node, on its travel Port."""
    sign = ray.source_sign + 1
    layers = family.arr_amt[position][sign, port]
    layer = next(index for index in range(len(layers)) if layers[index] == 0)
    family.arr_amt[position][sign, port, layer] = ray.amount
    family.arr_ph[position][sign, port, layer] = ray.phase
    family.arr_bit[position][sign, port, layer] = ray.detector


def departures_of(family, position):
    """The departures in flight at a Node as (port, sign, amount, phase, bit) rows."""
    rows = []
    amounts = family.fly_amt[position]
    for sign in range(3):
        for port in range(6):
            for layer in range(amounts.shape[2]):
                amount = int(amounts[sign, port, layer])
                if amount:
                    rows.append(
                        (
                            port,
                            sign - 1,
                            amount,
                            int(family.fly_ph[position][sign, port, layer]),
                            int(family.fly_bit[position][sign, port, layer]),
                        )
                    )
    return sorted(rows)


def rows_of(rays):
    return sorted((r.heading, r.source_sign, r.amount, r.phase, r.detector) for r in rays)


def block_of(family, position):
    return tuple(int(v) for v in family.reg[position].reshape(-1)), tuple(
        int(v) for v in family.regph[position].reshape(-1)
    )


def rays_at(world, position, family="light"):
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    node = next((n for n in world.inventory_view().nodes if n.position == position), None)
    return [] if node is None or not node.rays else sorted(node.rays[index], key=ray_merge_key)


def registers_at(world, position, family="light"):
    index = [f.field for f in world.initial.spatial_fields].index(
        [f.name for f in world.initial.fields].index(family)
    )
    node = next(n for n in world.inventory_view().nodes if n.position == position)
    return node.remainders[index]


def digests(path):
    return {
        name: hashlib.sha256((path / name).read_bytes()).hexdigest()
        for name in ("state.json", "events.jsonl")
    }


# (a) split: one dense cycle at a Node against `spread_content` on the same input.
# Pinned: the single ray of 12 at phase 6 on +X (the `single` case of the field
# spreading test) leaves 6 forward and 1 on each other heading, the registers
# (6, 1, 1, 1, 1, 1) at phase 6; two rays of 3 of opposite sign on +X leave 1
# each forward at phase 0 and fill both blocks (7, 3, 3, 3, 3, 3); one quantum on
# a forward register of 10 releases one forward and leaves (5, 1, 1, 1, 1, 1).
SPLIT_CASES = {
    "single": (
        (spread_ray(0, 12, 6),),
        (),
        (),
        [(0, 0, 6, 6, 0), *[(p, 0, 1, 6, 0) for p in range(1, 6)]],
        (6, 1, 1, 1, 1, 1),
    ),
    "signs": (
        (spread_ray(0, 3, 0, 1), spread_ray(0, 3, 0, -1)),
        (),
        (),
        [(0, -1, 1, 0, 0), (0, 1, 1, 0, 0)],
        None,
    ),
    "release": (
        (spread_ray(0, 1, 0),),
        (10, 0, 0, 0, 0, 0),
        ZERO,
        [(0, 0, 1, 0, 0)],
        (5, 1, 1, 1, 1, 1),
    ),
}
# Three Ports, two signs, three phases, a bit of 1 on one ray, registers filled at
# other phases: the oracle is `spread_content`; every departure carries bit 2.
MIXED = (
    spread_ray(0, 7, 1, 0, DETECTOR_BIT_1),
    spread_ray(3, 5, 5, 0),
    spread_ray(4, 9, 2, 1),
    spread_ray(4, 2, 6, -1, DETECTOR_BIT_0),
)
MIXED_REGISTERS = tuple(range(1, 19))
MIXED_PHASES = tuple((3 * slot) % 8 for slot in range(18))
# Three rays of one sign on +X at phases 1, 2 and 3 (amounts 4, 4, 4): the phase
# of the sum is 2, the registers take 12 x w mod 11.
THREE = (spread_ray(0, 4, 1), spread_ray(0, 4, 2), spread_ray(0, 4, 3))


@pytest.mark.parametrize("case", ["split", "boundary", "identity", "rejected"])
def test_dense_region_cycles_pure_field_nodes_exactly_as_the_engine(tmp_path, case):
    boards = _spreading()
    if case == "split":
        initial = parse_initial_state(dense_document(boards.document((((5, 7, 7), 12, 0, 6),))))
        with Simulation(initial) as world:
            family = light(world)
            definition = family.definition
            position = (6, 7, 7)
            for name, (rays, registers, phases, expected, block) in SPLIT_CASES.items():
                held = tuple(registers) and (ZERO + tuple(registers) + ZERO) or ()
                held_phases = tuple(phases) and (ZERO + tuple(phases) + ZERO) or ()
                for ray in rays:
                    place(family, position, ray.heading, ray)
                if held:
                    family.reg[position] = [held[i : i + 6] for i in range(0, 18, 6)]
                    family.regph[position] = [held_phases[i : i + 6] for i in range(0, 18, 6)]
                region(world).cycle(0)
                oracle, record, after, after_phases = spread_content(
                    family.index, rays, definition, held, held_phases
                )
                assert departures_of(family, position) == rows_of(oracle) == sorted(expected), name
                assert block_of(family, position) == (after, after_phases), name
                if block is not None:
                    assert after[6:12] == block, name
                assert region(world).active_count() == 1
                family.fly_amt[...] = 0
                family.reg[position] = 0
                family.regph[position] = 0
            # The mixed case: the combination order of the registers, Port by Port,
            # and the bit of the whole on every departure, the releases included.
            for ray in MIXED:
                place(family, position, ray.heading, ray)
            family.reg[position] = [MIXED_REGISTERS[i : i + 6] for i in range(0, 18, 6)]
            family.regph[position] = [MIXED_PHASES[i : i + 6] for i in range(0, 18, 6)]
            region(world).cycle(0)
            oracle, record, after, after_phases = spread_content(
                family.index, MIXED, definition, MIXED_REGISTERS, MIXED_PHASES
            )
            assert departures_of(family, position) == rows_of(oracle)
            assert all(row[4] == DETECTOR_BIT_1 for row in rows_of(oracle))
            assert block_of(family, position) == (after, after_phases)
            assert record.stored == (sum(after) - sum(MIXED_REGISTERS)) // family.total
            assert after[remainder_slot(1, 4)] != MIXED_REGISTERS[remainder_slot(1, 4)]
            family.fly_amt[...] = 0
            family.reg[position] = 0
            family.regph[position] = 0
            # A packet from an engine Node with three phases on one Port and sign:
            # the third ray is kept whole beside the two layers, read back as a
            # resident ray, and spread with the others.
            packet = SpatialPacket(1, (5, 7, 7), 0, region(world).blank_bundle, rays=(THREE,))
            region(world)._absorb(position, packet)
            assert family.overflow == {position: [THREE[2]]}
            node = region(world).materialized_nodes(world._spatial.nodes)[position]
            assert node.rays[family.index] == THREE
            assert node.arrival_mask == (0, 1, 0, 0, 0, 0) and node.received_count == 1
            region(world).cycle(0)
            oracle, record, after, after_phases = spread_content(family.index, THREE, definition)
            assert departures_of(family, position) == rows_of(oracle)
            assert block_of(family, position) == (after, after_phases)
            assert record.phase == 2 and family.overflow == {}
        return
    if case == "boundary":
        # (b) The record of electrons at (5,7,7) releases light of sign -1 every
        # interval into dense Nodes; the Detector at (8,7,7) is the engine's: the
        # quanta the dense region sends it are handed over as packets and drawn,
        # returned at ticks 6 and 10, and a returned quantum walking back through
        # the dense region takes its Node to the engine for that interval and gives
        # it back afterwards, ending at its source at tick 9 (the `source` case of
        # the field spreading test, the same integers).
        detector = {"position": [8, 7, 7], "setting": [0, 1], "seed": 1}
        raw = dense_document(boards.charged_world(False, 12, [detector]))
        events = []
        kinds = ("detector_return", "field_returned", "field_spread")
        with Simulation(
            parse_initial_state(raw),
            observer=lambda e: events.append(e) if e["event"] in kinds else None,
        ) as world:
            dense = region(world)
            owned = {}
            for tick in range(1, 13):
                world.step()
                unbooked = int(tick >= 10)
                assert world.totals()["light"] == (6 * tick - unbooked,)
                assert world.source_totals()["light"] == (6 * tick - unbooked,)
                assert world.escaped_totals()["light"] == (0,)
                assert world.audit()["balanced"]
                owned[tick] = (int(dense.owner[7, 7, 7]), int(dense.owner[6, 7, 7]))
            assert int(dense.owner[8, 7, 7]) == 1 and int(dense.owner[5, 7, 7]) == 1
            # (7,7,7) and (6,7,7) are the region's except while a returned quantum
            # walks back through them, at (7,7,7) after ticks 7 and 11 and at (6,7,7)
            # after 8 and 12; a Node goes back to the region when it next receives
            # content, so (7,7,7) may stay the engine's one tick longer.
            assert all(owned[tick] == (0, 0) for tick in (1, 2, 3, 4, 5, 6, 9, 10))
            assert owned[7] == owned[11] == (1, 0)
            assert owned[8][1] == owned[12][1] == 1
            assert rays_at(world, (6, 7, 7)) == sorted(
                [
                    spread_ray(0, 1, 0, -1),
                    Ray(1, (0, 0, 0), 1, steps=0, outbound=0, detector=DETECTOR_BIT_0, source_sign=-1),
                ],
                key=ray_merge_key,
            )
            assert rays_at(world, (7, 7, 7)) == [spread_ray(0, 1, 0, -1)]
            assert rays_at(world, (8, 7, 7)) == []
            assert registers_at(world, (7, 7, 7)) == (8, 5, 5, 5, 5, 5, *ZERO, *ZERO)
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
            # The engine spreads at (7,7,7) only in the intervals it owns it.
            assert [
                e["tick"] for e in events if e["event"] == "field_spread" and e["position"] == (7, 7, 7)
            ] == [7, 11]
        return
    if case == "identity":
        # (c) The same worlds, the engine alone and with the dense mode: the same
        # `state.json` and the same ledger, the runner naming the mode when on.
        for name, raw, ticks in (
            ("single", boards.document((((5, 7, 7), 12, 0, 6),)), 4),
            (
                "source",
                boards.charged_world(False, 12, [{"position": [8, 7, 7], "setting": [0, 1], "seed": 1}]),
                12,
            ),
        ):
            records = {}
            for mode, document in (("engine", engine_document(raw)), ("dense", dense_document(raw))):
                path = tmp_path / f"{name}_{mode}.json"
                path.write_text(json.dumps(document), encoding="utf-8")
                out = tmp_path / f"{name}_{mode}"
                run_initialization(path, out, ticks=ticks)
                metadata = json.loads((out / "run.json").read_text(encoding="utf-8"))
                assert (
                    metadata["status"] == "completed" and metadata["conserved_at_every_completed_tick"]
                )
                assert metadata.get("dense_field") == (DENSE_FIELD if mode == "dense" else None)
                records[mode] = (digests(out), metadata["audit"], metadata["final_totals"])
            assert records["engine"][0]["state.json"] == records["dense"][0]["state.json"], name
            assert records["engine"][1] == records["dense"][1], name
            assert records["engine"][2] == records["dense"][2], name
            # The dense region writes no per-Node events: the record differs.
            assert records["engine"][0]["events.jsonl"] != records["dense"][0]["events.jsonl"]
        assert DENSE_FIELD == "dense-field-v1"
        # The runner's flag is the same switch.
        path = tmp_path / "flag.json"
        path.write_text(json.dumps(engine_document(boards.document((((5, 7, 7), 12, 0, 6),)))))
        run_initialization(path, tmp_path / "flag", ticks=4, dense_field=True)
        metadata = json.loads((tmp_path / "flag" / "run.json").read_text(encoding="utf-8"))
        assert metadata["dense_field"] == DENSE_FIELD
        assert (
            digests(tmp_path / "flag")["state.json"] == digests(tmp_path / "single_engine")["state.json"]
        )
        return
    # (d) What the prototype does not support is rejected at initialization.
    base = boards.document((((5, 7, 7), 12, 0, 6),))
    for change, message in (
        ({}, "local conservation audit"),
        ({"conservation": None, "spatial_fields": [boards.ray_field("light", 0)]}, "spreading family"),
        (
            {
                "conservation": None,
                "spatial_fields": [
                    boards.ray_field("light", 0, spread=boards.SPREAD),
                    {"field": "momentum", "baseline": [0, 0, 0], "transport": "outward"},
                ],
            },
            "ray transport on every spatial field",
        ),
        (
            {
                "conservation": None,
                "spatial_fields": [
                    boards.ray_field("light", 0, spread=boards.SPREAD, polarization_bits=1)
                ],
            },
            "polarization",
        ),
        (
            {
                "conservation": None,
                "ray_interactions": [
                    {
                        "name": "self",
                        "participants": [{"type": "light"}, {"type": "light"}],
                        "outputs": [
                            {
                                "field": "light",
                                "amount": {"of": 0},
                                "heading": "reversed",
                                "input": 1,
                                "phase": {"of": 0},
                            },
                            {
                                "field": "light",
                                "amount": {"of": 1},
                                "heading": "reversed",
                                "input": 0,
                                "phase": {"of": 1},
                            },
                        ],
                        "invariants": [{"name": "energy", "expression": {"field": "amount"}}],
                    }
                ],
            },
            "coupling on field rays inside the dense region",
        ),
    ):
        raw = dict(base) | {"dense_field": True}
        for key, value in change.items():
            if value is None:
                raw.pop(key, None)
            else:
                raw[key] = value
        with pytest.raises(ValueError, match=message):
            parse_initial_state(raw)
    with pytest.raises(ValueError, match="parallel"):
        Simulation(parse_initial_state(dense_document(base)), node_workers=2)
    # Off by default: a world without the key is the engine alone.
    initial = parse_initial_state(engine_document(base))
    assert not initial.dense_field
    with Simulation(initial) as world:
        assert world._spatial.dense is None
