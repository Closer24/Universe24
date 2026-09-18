"""The dense mode for boards that a field fills (dense-field-v1, docs/PERFORMANCE.md):
the shadow-only Nodes of a board cycled as one vectorized step over integer arrays
that applies the spread and remainder rule of field-spreading-v1 and
field-remainder-v1 to every such Node at once, exactly; a ray leaving a dense Node
toward a sparse Node (a mark, a body, a lamp, a Node holding a returning or another
family's ray) handed over as an ordinary packet and a packet leaving a sparse Node
into the dense region absorbed into the arrays; the same `state.json` and the same
ledger as the engine alone, which is the mode's acceptance test.

Expected integers are pinned in docs/TEST_EXPECTATIONS.md ("The dense mode") before
the first run: split, identity, rejected.

Re-pinned on 2026-09-18 under the law of the bit (bit-law-v1, point 13): the
dense region is the board's shadow layer, on by default wherever a world admits
it (`dense_field: false` keeps the engine alone), holding shadows alone (no bit
in the arrays, one block of layers per owner of the family); the boards are
those of test_field_spreading.py, shadows given with the board; a mark returns
every shadow and counts none (the `boundary` case's world, a thing radiating
every interval, went with the law; the mark's return is read through the
identity of the two modes).
"""

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import pytest

from event_universe import Simulation
from event_universe.core.spatial_state import (
    BIT_SHADOW,
    DENSE_FIELD,
    Ray,
    SpatialPacket,
    remainder_slot,
    spread_content,
)
from event_universe.initialization import parse_initial_state
from event_universe.runner import run_initialization

ROOT = Path(__file__).resolve().parents[1]
# The six unit-axial headings in Port order [+X, -X, +Y, -Y, +Z, -Z].
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
ZERO = (0, 0, 0, 0, 0, 0)
OWNER = 1
SINGLE = (((6, 7, 7), 12, 0, 6),)


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
    """The same world under the dense mode."""
    return dict(raw) | {"dense_field": True}


def engine_document(raw):
    """The same world under the engine alone."""
    return dict(raw) | {"dense_field": False}


def spread_ray(heading, amount, phase, sign=0):
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        steps=1,
        detector=BIT_SHADOW,
        source_sign=sign,
        owner=OWNER,
    )


def region(world):
    dense = world._spatial.dense
    assert dense is not None
    return dense


def light(world):
    names = [f.name for f in world.initial.fields]
    index = [f.field for f in world.initial.spatial_fields].index(names.index("light"))
    return region(world).families[index]


def place(family, position, port, ray):
    """One arrived shadow into the arrays at a Node, on its travel Port."""
    rank = family.rank[ray.owner]
    sign = ray.source_sign + 1
    layers = family.arr_amt[position][rank, sign, port]
    layer = next(index for index in range(len(layers)) if layers[index] == 0)
    family.arr_amt[position][rank, sign, port, layer] = ray.amount
    family.arr_ph[position][rank, sign, port, layer] = ray.phase


def departures_of(family, position):
    """The departures in flight at a Node as (port, sign, amount, phase) rows."""
    rows = []
    amounts = family.fly_amt[position]
    for rank in range(amounts.shape[0]):
        for sign in range(3):
            for port in range(6):
                for layer in range(amounts.shape[3]):
                    amount = int(amounts[rank, sign, port, layer])
                    if amount:
                        rows.append(
                            (
                                port,
                                sign - 1,
                                amount,
                                int(family.fly_ph[position][rank, sign, port, layer]),
                            )
                        )
    return sorted(rows)


def rows_of(rays):
    return sorted((r.heading, r.source_sign, r.amount, r.phase) for r in rays)


def block_of(family, position):
    return tuple(int(v) for v in family.reg[position].reshape(-1)), tuple(
        int(v) for v in family.regph[position].reshape(-1)
    )


def set_block(family, position, registers, phases):
    family.reg[position] = [[registers[i : i + 6] for i in range(0, 18, 6)]]
    family.regph[position] = [[phases[i : i + 6] for i in range(0, 18, 6)]]


def digests(path):
    return {
        name: hashlib.sha256((path / name).read_bytes()).hexdigest()
        for name in ("state.json", "events.jsonl")
    }


# (a) split: one dense cycle at a Node against `spread_content` on the same input.
# Pinned: the single shadow of 12 at phase 6 on +X (the `single` case of the field
# spreading test) leaves 6 forward and 1 on each other heading, the registers
# (6, 1, 1, 1, 1, 1) at phase 6; two shadows of 3 of opposite sign on +X leave 1
# each forward at phase 0 and fill both blocks (7, 3, 3, 3, 3, 3); one quantum on
# a forward register of 10 releases one forward and leaves (5, 1, 1, 1, 1, 1).
SPLIT_CASES = {
    "single": (
        (spread_ray(0, 12, 6),),
        (),
        (),
        [(0, 0, 6, 6), *[(p, 0, 1, 6) for p in range(1, 6)]],
        (6, 1, 1, 1, 1, 1),
    ),
    "signs": (
        (spread_ray(0, 3, 0, 1), spread_ray(0, 3, 0, -1)),
        (),
        (),
        [(0, -1, 1, 0), (0, 1, 1, 0)],
        None,
    ),
    "release": (
        (spread_ray(0, 1, 0),),
        (10, 0, 0, 0, 0, 0),
        ZERO,
        [(0, 0, 1, 0)],
        (5, 1, 1, 1, 1, 1),
    ),
}
# Three Ports, two signs, three phases, registers filled at other phases: the
# oracle is `spread_content`.
MIXED = (
    spread_ray(0, 7, 1, 0),
    spread_ray(3, 5, 5, 0),
    spread_ray(4, 9, 2, 1),
    spread_ray(4, 2, 6, -1),
)
MIXED_REGISTERS = tuple(range(1, 19))
MIXED_PHASES = tuple((3 * slot) % 8 for slot in range(18))
# Three shadows of one sign on +X at phases 1, 2 and 3 (amounts 4, 4, 4): the phase
# of the sum is 2, the registers take 12 x w mod 11.
THREE = (spread_ray(0, 4, 1), spread_ray(0, 4, 2), spread_ray(0, 4, 3))


@pytest.mark.parametrize("case", ["split", "identity", "rejected"])
def test_dense_region_cycles_pure_field_nodes_exactly_as_the_engine(tmp_path, case):
    boards = _spreading()
    if case == "split":
        initial = parse_initial_state(dense_document(boards.document(SINGLE)))
        with Simulation(initial) as world:
            family = light(world)
            definition = family.definition
            # A Node of the region's, one Link on from the board's own shadow (whose
            # Node is the engine's until the region takes it back).
            position = (7, 7, 7)
            for name, (rays, registers, phases, expected, block) in SPLIT_CASES.items():
                held = tuple(registers) and (ZERO + tuple(registers) + ZERO) or ()
                held_phases = tuple(phases) and (ZERO + tuple(phases) + ZERO) or ()
                for ray in rays:
                    place(family, position, ray.heading, ray)
                if held:
                    set_block(family, position, held, held_phases)
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
            # the releases included.
            for ray in MIXED:
                place(family, position, ray.heading, ray)
            set_block(family, position, MIXED_REGISTERS, MIXED_PHASES)
            region(world).cycle(0)
            oracle, record, after, after_phases = spread_content(
                family.index, MIXED, definition, MIXED_REGISTERS, MIXED_PHASES
            )
            assert departures_of(family, position) == rows_of(oracle)
            assert block_of(family, position) == (after, after_phases)
            assert record.stored == (sum(after) - sum(MIXED_REGISTERS)) // family.total
            assert after[remainder_slot(1, 4)] != MIXED_REGISTERS[remainder_slot(1, 4)]
            family.fly_amt[...] = 0
            family.reg[position] = 0
            family.regph[position] = 0
            # A packet from an engine Node with three phases on one Port and sign:
            # the third shadow is kept whole beside the two layers, read back as a
            # resident ray, and spread with the others.
            packet = SpatialPacket(1, (6, 7, 7), 0, region(world).blank_bundle, rays=(THREE,))
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
    if case == "identity":
        # (b) The same worlds, the engine alone and with the dense mode: the same
        # `state.json` and the same ledger, the runner naming the mode when on.
        # `returned`: a mark at (8,7,7) that catches nothing returns the shadows
        # the region hands it, which walk back through the region; `counter`: a
        # mark that would catch every arrival counts nothing, a shadow is returned
        # and never counted (bit-law-v1), the marks' line of the ledger empty.
        for name, raw, ticks in (
            ("single", boards.document(SINGLE), 3),
            (
                "returned",
                boards.document(SINGLE, ticks=8, detectors=[{"position": [8, 7, 7], "setting": [0, 1]}]),
                8,
            ),
            (
                "counter",
                boards.document(SINGLE, ticks=8, detectors=[{"position": [8, 7, 7], "setting": [1, 1]}]),
                8,
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
                records[mode] = (
                    digests(out),
                    metadata["audit"],
                    metadata["final_totals"],
                    (metadata["detector_marks"], metadata["detector_mark_totals"]),
                )
            assert records["engine"][0]["state.json"] == records["dense"][0]["state.json"], name
            assert records["engine"][1] == records["dense"][1], name
            assert records["engine"][2] == records["dense"][2], name
            assert records["engine"][3] == records["dense"][3], name
            assert records["engine"][2] == {"light": [12]}, name
            if name != "single":
                (mark,), totals = records["engine"][3]
                assert mark["counter"] == {} and totals == {"light": [0]}
                assert records["engine"][1][-1]["fields"]["light"]["absorbed_by_marks"] == [0]
            # A Node holding shadows alone publishes no event under either mode.
            assert records["engine"][0]["events.jsonl"] == records["dense"][0]["events.jsonl"]
        assert DENSE_FIELD == "dense-field-v1"
        # The runner's flag is the same switch.
        path = tmp_path / "flag.json"
        path.write_text(json.dumps(engine_document(boards.document(SINGLE))))
        run_initialization(path, tmp_path / "flag", ticks=3, dense_field=True)
        metadata = json.loads((tmp_path / "flag" / "run.json").read_text(encoding="utf-8"))
        assert metadata["dense_field"] == DENSE_FIELD
        assert (
            digests(tmp_path / "flag")["state.json"] == digests(tmp_path / "single_engine")["state.json"]
        )
        return
    # (c) What the mode does not support is rejected at initialization.
    base = boards.document(SINGLE)
    for change in (
        {"spatial_fields": [boards.ray_field("light", 0)]},
        {
            "fields": [boards.field("light"), boards.vector("momentum")],
            "spatial_fields": [
                boards.ray_field("light", 0, spread=boards.SPREAD),
                {"field": "momentum", "baseline": [0, 0, 0], "transport": "outward"},
            ],
        },
        {"spatial_fields": [boards.ray_field("light", 0, spread=boards.SPREAD, polarization_bits=1)]},
    ):
        raw = dict(base) | {"dense_field": True} | change
        with pytest.raises(ValueError, match="dense_field"):
            parse_initial_state(raw)
    with pytest.raises(ValueError, match="parallel"):
        Simulation(parse_initial_state(dense_document(base)), node_workers=2)
    # On by default wherever admitted (bit-law-v1, point 13); off when the world says so.
    admitted = dict(base)
    del admitted["dense_field"]
    assert parse_initial_state(admitted).dense_field
    initial = parse_initial_state(engine_document(base))
    assert not initial.dense_field
    with Simulation(initial) as world:
        assert world._spatial.dense is None
