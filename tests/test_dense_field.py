"""The dense mode for boards that a field fills (dense-field-v1, docs/PERFORMANCE.md):
the shadow-only Nodes of a board held as integer arrays and cycled by the mixing
and remainder rule of node-mixing-v1 and field-remainder-v1, exactly as the
engine's `spread_content` (feature 16c, part 2: the mixing vectorized in
`DenseField._mix`, the same integers at every Node); a ray leaving a dense Node
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

Re-pinned on 2026-09-18 under the Node's mixing (node-mixing-v1, Highlights 5.4
point 24, feature 16c): the boards are built here (test_field_spreading.py went
with the split table), nothing of the spread is declared, the `split` case reads
the mixing's integers (a lone 12 sends 5 back at the opposite phase and 1 each
other way, parking 3 ninths per heading; a lone 1 parks 4 ninths back and 1 each
other way and fills a register of 10 to release) and the `rejected` case names a
family without a shadow set.

Re-pinned on 2026-09-18 under the return as a field (return-field-v1, feature
16d, part 2): the arrays carry the flow of every share beside its sign and the
momentum it carries, the parked block of a Node being the engine's thirty-six
slots per owner cell for cell, so the `split` case reads the engine's block as
it is, and a `returning` sub-case mixes a returning share of 12 carrying
(-12, 0, 0): the same integers as the outgoing 12, in the returning group, the
momentum over the twelve outputs by the largest remainder, -5 on the 5 back,
-1 on each of the other five quanta and -1 on the +X and the -X ninths.
"""

import hashlib
import json
from pathlib import Path

import numpy as np
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


COSTS = {
    name: 1
    for name in ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
}


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


def ray_field(name, advance, **extra):
    return {
        "field": name,
        "baseline": 0,
        "transport": "ray",
        "headings": HEADINGS,
        "rays_per_tick": 1,
        "metric": "links",
        "pace": [1, 1],
    } | extra


def document(shadows, ticks=3, detectors=(), dense=False):
    """The board: an open 13^3 lattice, the family `light` (an 8-step phase
    advancing 0, nothing declared of its spread) and a never-seeded holder
    (thing 1); `shadows` are (position, amount, heading index, phase) of `light`,
    each a shadow of the holder given with the board as content that arrived on
    its heading, spreading at its Node in the first cycle."""
    raw = {
        "schema_version": 1,
        "N": 8,
        "model_id": "dense-field-test-v1",
        "shape": [13, 13, 13],
        "boundary": "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": ticks,
        "operation_costs": COSTS,
        "fields": [field("light")],
        "disturbance_types": [
            {
                "name": "holder",
                "fields": ["light"],
                "defaults": {"light": 0},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [ray_field("light", 0)],
        "emissions": [],
        "seeds": [],
        "detectors": list(detectors),
        "dense_field": dense,
    }
    if shadows:
        raw["initial_field"] = {
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
    return raw


def dense_document(raw):
    """The same world under the dense mode."""
    return dict(raw) | {"dense_field": True}


def engine_document(raw):
    """The same world under the engine alone."""
    return dict(raw) | {"dense_field": False}


def spread_ray(heading, amount, phase, sign=0, outbound=1, momentum=None):
    return Ray(
        heading,
        (0, 0, 0),
        amount,
        phase=phase,
        steps=1,
        outbound=outbound,
        detector=BIT_SHADOW,
        source_sign=sign,
        momentum=momentum,
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
    assert family.place(position, ray, port)


def departures_of(family, position):
    """The departures in flight at a Node as (port, sign, amount, phase, flow,
    momentum) rows, the flow as `Ray.outbound` reads it."""
    rows = []
    amounts = family.fly_amt[position]
    for rank, flow, sign, port, layer in zip(*np.nonzero(amounts > 0), strict=True):
        cell = (rank, flow, sign, port, layer)
        carried = tuple(int(v) for v in family.fly_mom[position][cell])
        rows.append(
            (
                int(port),
                int(sign) - 1,
                int(amounts[cell]),
                int(family.fly_ph[position][cell]),
                0 if flow else 1,
                carried if any(carried) else None,
            )
        )
    return sorted(rows, key=repr)


def rows_of(rays):
    return sorted(
        ((r.heading, r.source_sign, r.amount, r.phase, r.outbound, r.momentum) for r in rays), key=repr
    )


def block_of(family, position):
    """The Node's parked block and its phases, the engine's thirty-six slots."""
    return family.block(position)[:2]


def set_block(family, position, registers, phases):
    family.set_block(position, tuple(registers), tuple(phases), (0,) * (3 * len(registers)))


def digests(path):
    return {
        name: hashlib.sha256((path / name).read_bytes()).hexdigest()
        for name in ("state.json", "events.jsonl")
    }


# (a) split: one dense cycle at a Node against `spread_content` on the same input.
# Pinned (node-mixing-v1): the single shadow of 12 at phase 6 on +X sends 5 back
# on -X at phase 2 (the minus, a half turn) and 1 on each other heading at phase
# 6, parking 3 ninths per heading, (3, 3, 3, 3, 3, 3); two shadows of 3 of
# opposite sign on +X send 1 back each on -X at phase 4 and park 3 ninths per
# heading in each sign's block; one quantum on +X with its +X register at 10
# parks (1, 4, 1, 1, 1, 1), and the +X register at 11 releases one quantum
# forward at its phase 0 and keeps 2. A returning share of 12 of sign 1 carrying
# (-12, 0, 0) (return-field-v1, part 2) mixes the same way in its own group and
# parks in the returning block of its sign (slots 30 to 35), the momentum over
# the twelve outputs by the largest remainder: the wholes' weights 9, 45, 9, 9,
# 9, 9 and the ninths' 3 each over 108 give -1, -5, -1, -1, -1, -1 on the quanta
# and the two units left to the +X and -X ninths. Each entry: the rays, the
# registers and phases of the sign-0 outgoing block, the departure rows and the
# block to check as (its first slot, its six values).
SPLIT_CASES = {
    "single": (
        (spread_ray(0, 12, 6),),
        (),
        (),
        [(1, 0, 5, 2, 1, None), *[(p, 0, 1, 6, 1, None) for p in (0, 2, 3, 4, 5)]],
        (6, (3, 3, 3, 3, 3, 3)),
    ),
    "signs": (
        (spread_ray(0, 3, 0, 1), spread_ray(0, 3, 0, -1)),
        (),
        (),
        [(1, -1, 1, 4, 1, None), (1, 1, 1, 4, 1, None)],
        None,
    ),
    "release": (
        (spread_ray(0, 1, 0),),
        (10, 0, 0, 0, 0, 0),
        ZERO,
        [(0, 0, 1, 0, 1, None)],
        (6, (2, 4, 1, 1, 1, 1)),
    ),
    "returning": (
        (spread_ray(0, 12, 6, 1, outbound=0, momentum=(-12, 0, 0)),),
        (),
        (),
        [(1, 1, 5, 2, 0, (-5, 0, 0)), *[(p, 1, 1, 6, 0, (-1, 0, 0)) for p in (0, 2, 3, 4, 5)]],
        (30, (3, 3, 3, 3, 3, 3)),
    ),
}
RETURNING_MOMENTA = (0,) * 90 + (-1, 0, 0, -1, 0, 0) + (0,) * 12
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
# of the sum is 2, one amplitude of 12 at that phase.
THREE = (spread_ray(0, 4, 1), spread_ray(0, 4, 2), spread_ray(0, 4, 3))


@pytest.mark.parametrize("case", ["split", "identity", "rejected"])
def test_dense_region_cycles_pure_field_nodes_exactly_as_the_engine(tmp_path, case):
    if case == "split":
        initial = parse_initial_state(dense_document(document(SINGLE)))
        with Simulation(initial) as world:
            family = light(world)
            definition = family.definition
            # A Node of the region's, one Link on from the board's own shadow (whose
            # Node is the engine's until the region takes it back).
            position = (7, 7, 7)
            for name, (rays, registers, phases, expected, block) in SPLIT_CASES.items():
                held = ZERO + tuple(registers) + ZERO + ZERO * 3 if registers else ()
                held_phases = ZERO + tuple(phases) + ZERO + ZERO * 3 if phases else ()
                for ray in rays:
                    place(family, position, ray.heading, ray)
                if held:
                    set_block(family, position, held, held_phases)
                region(world).cycle(0)
                oracle, record, after, after_phases, after_momenta = spread_content(
                    family.index, rays, definition, held, held_phases
                )
                assert (
                    departures_of(family, position) == rows_of(oracle) == sorted(expected, key=repr)
                ), name
                assert block_of(family, position) == (after, after_phases), name
                assert family.block(position)[2] == after_momenta, name
                if block is not None:
                    start, values = block
                    assert after[start : start + 6] == values, name
                if name == "returning":
                    assert after_momenta == RETURNING_MOMENTA
                else:
                    assert not any(after_momenta), name
                assert region(world).active_count() == 1
                family.fly_amt[...] = 0
                family.fly_mom[...] = 0
                family.reg[position] = 0
                family.regph[position] = 0
                family.reg_mom[position] = 0
            # The mixed case: the combination order of the registers, Port by Port,
            # the releases included.
            for ray in MIXED:
                place(family, position, ray.heading, ray)
            set_block(family, position, MIXED_REGISTERS + ZERO * 3, MIXED_PHASES + ZERO * 3)
            region(world).cycle(0)
            oracle, record, after, after_phases, _ = spread_content(
                family.index,
                MIXED,
                definition,
                MIXED_REGISTERS + ZERO * 3,
                MIXED_PHASES + ZERO * 3,
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
            oracle, record, after, after_phases, _ = spread_content(family.index, THREE, definition)
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
            ("single", document(SINGLE), 3),
            (
                "returned",
                document(SINGLE, ticks=8, detectors=[{"position": [8, 7, 7], "setting": [0, 1]}]),
                8,
            ),
            (
                "counter",
                document(SINGLE, ticks=8, detectors=[{"position": [8, 7, 7], "setting": [1, 1]}]),
                8,
            ),
        ):
            records = {}
            for mode, chosen in (("engine", engine_document(raw)), ("dense", dense_document(raw))):
                path = tmp_path / f"{name}_{mode}.json"
                path.write_text(json.dumps(chosen), encoding="utf-8")
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
                assert mark["resident"]["real"] == {} and totals == {"light": [0]}
                assert records["engine"][1][-1]["fields"]["light"]["absorbed_by_marks"] == [0]
            # A Node holding shadows alone publishes no event under either mode.
            assert records["engine"][0]["events.jsonl"] == records["dense"][0]["events.jsonl"]
        assert DENSE_FIELD == "dense-field-v1"
        # The runner's flag is the same switch.
        path = tmp_path / "flag.json"
        path.write_text(json.dumps(engine_document(document(SINGLE))))
        run_initialization(path, tmp_path / "flag", ticks=3, dense_field=True)
        metadata = json.loads((tmp_path / "flag" / "run.json").read_text(encoding="utf-8"))
        assert metadata["dense_field"] == DENSE_FIELD
        assert (
            digests(tmp_path / "flag")["state.json"] == digests(tmp_path / "single_engine")["state.json"]
        )
        return
    # (c) What the mode does not support is rejected at initialization: a world
    # without a shadow set, an outward field beside the rays, polarization.
    base = document(SINGLE)
    without_shadows = {key: value for key, value in base.items() if key != "initial_field"}
    for start, change in (
        (without_shadows, {}),
        (
            base,
            {
                "fields": [field("light"), vector("momentum")],
                "spatial_fields": [
                    ray_field("light", 0),
                    {"field": "momentum", "baseline": [0, 0, 0], "transport": "outward"},
                ],
            },
        ),
        (base, {"spatial_fields": [ray_field("light", 0, polarization_bits=1)]}),
    ):
        raw = dict(start) | {"dense_field": True} | change
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
