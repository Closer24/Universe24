"""The engine (docs/designs/detector_law/DESIGN.md; one engine, no law's name and no
version, ALGEBRA.md 9.90 (1)),
the build's first gate: the loader's key and refusals, the rule's step against
the design's integers, and one chain world run headless (an emitter body at one
end, a receiver at the other, the open face behind the emitter): one click per
record, the books balanced at every tick, the click's time at the front's
first rung about L / c after the giving, the click line with the stamp. SINCE
THE EMITTER AS A CLICKING BODY (ALGEBRA.md 9.17; BUILD.md section 26) the
lamp is refused under the detector law: the chain world's source is a body
of the matter kind seeded on its bound mode, its excitations clicking at
their rungs and writing the given record once; the grace, the exemption and
the emitter's own take are retired (its Nodes are Nodes like every other)."""

from __future__ import annotations

import math

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation, LiveRecord
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.test_emitter import (
    CHARGE_FAMILY,
    CLOCK_FAMILY,
    NODE_CLOCK,
    lawful_wheel,
    massive_generator,
    reads,
)

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md 9.57 (2);
# the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20

EMITTER_KIND = [7, 8]  # the emitter body's kind (omega_0 = 0.505)
EMITTER_PAIR = [
    699,
    700,
]  # the well of the 32-Node emitting body, rich (W = 700 remainder values, ALGEBRA.md 9.22 (4)) and bound on a chain (2 cos omega_b = 1.9944 over 32 Nodes; the one-Node well [801, 700] of the one-Node giving is a runaway over 32 Nodes, 2.285, its interior above 1)
GIVEN_CLOCK = [
    512,
    1,
]  # the given clock of every light emitter on N = 1024: k = pi / 2, the wavelength 4 (ALGEBRA.md 9.17 (6a))
PHASE_STEPS = 1024
TRAIN_LENGTH = 32  # the train's Nodes along K: 8 periods of the wavelength 4


def emitter_body(
    position: list[int],
    stock: int,
    receiver: object = None,
    family: str = "light",
    direction: list[int] | None = None,
    extents: list[int] | None = None,
) -> dict:
    """An emitter body of the matter kind EMITTER_KIND (the well pair EMITTER_PAIR over the
    train's 32 Nodes along `direction`, +x by default, seeded on its mode at 2^20 by the
    generator; at 100 the given light's back-action swamps the excited record, ALGEBRA.md
    9.17 (7) (c)), its stock `stock`, its `emitter` the family given with its `train` of 8
    periods (THE GIVEN TRAIN, 9.17 (6a); BUILD.md section 26 item 27: the profile and its
    norm the generator's, `given_train`) and, with `receiver`, the given records' ladder by
    name. The residue and the wheel are the law's (ALGEBRA.md 9.22 (4): the clicking
    record's remainder at the giving Node, W = 700 on EMITTER_PAIR in the vacuum, at the body's
    Nodes the wheel of its content under the Node clock (9.35 (2); BUILD.md section 26 item
    31), read after the excited record's first advance, 9.19 (4e); the residues spread from the kept remainder, the model
    owner's decisions (1) and (2) of record 1962, no coupling). The cadence under the click
    rule of ALGEBRA.md 9.17 (7)
    (f) (BUILD.md section 26 item 24): the residue u clicks (2 u + 1) / (2 W) x P intervals
    after its read, within the seed's rounding wobble; a well too deep for its board is a
    runaway and refused at the margin rule."""
    emitter: dict = {
        "family": family,
        "weight": 3,  # the window's weight (commit 7; the train retired)
        "twist": 0,  # the given record's twist "own", the generator's number (item 73)
    }
    if receiver is not None:
        emitter["receiver"] = receiver
    if extents is None:
        extents = [1, 1, 1]
        extents[next(index for index, v in enumerate(direction or [1, 0, 0]) if v != 0)] = TRAIN_LENGTH
    return {
        "position": position,
        "family": "matter",
        "amount": 1,
        "ramp": 0,
        "start": 0,
        "stocks": {family: stock},
        "momentum": [0, 0, 0],
        "extents": extents,
        "q": 0,
        "spin": [0, 0, 0],
        "twist": 0,
        "moment": [0, 0, 0],
        "pair": list(EMITTER_PAIR),
        "seed": 1
        << 10,  # the window's writes at the body's Nodes pile up about 300-fold and stay under the bound (commit 7)
        "margin": "control",
        "emitter": emitter,
    }


DETECTOR_SIDE = 3  # the detector cube's side (the model owner's word of 2026-09-25, record 1899)


def cube_positions(shape: list[int], corner: list[int]) -> list[list[int]]:
    """The Nodes of a detector cube of side DETECTOR_SIDE from its lower corner, cut by the
    GameBoard on an axis of extent below the side (a chain's or a layer's thin axis)."""
    return [
        [corner[0] + dx, corner[1] + dy, corner[2] + dz]
        for dx in range(min(DETECTOR_SIDE, shape[0]))
        for dy in range(min(DETECTOR_SIDE, shape[1]))
        for dz in range(min(DETECTOR_SIDE, shape[2]))
    ]


def receiver_body(position: list[int], family: str = "light") -> dict:
    """A fixed receiver body of the family at one Node (a measured event)."""
    return {
        "position": position,
        "family": family,
        "amount": 1,
        "stocks": {},
        "momentum": [0, 0, 0],
    }


def receiver_cube(document: dict, name: str, corner: list[int], family: str = "light") -> None:
    """ONE DETECTOR (record 1899): the cube of side DETECTOR_SIDE of receiver bodies from
    `corner`, read as the one set `name` (its sensitivity its whole cube, the click the
    detector's, never a Node's)."""
    positions = cube_positions(document["shape"], corner)
    document["measured"].extend(receiver_body(position, family) for position in positions)
    document["detectors"].append({"name": name, "positions": positions})


def chain_world(
    stock: int = 6,
    receiver: object = None,
    clock_stamp: bool = True,
    on_mode: bool = True,
    faces: str = "closed",
) -> dict:
    """A chain of 80 Nodes (y and z periodic, one layer each; x CLOSED, the
    zero rows at both ends mirrors): the emitter body at [2, 34) (the
    train's 32 Nodes of the matter kind [7, 8] with the well pair [699,
    700], its mode the seed), the receiver cube of side 3 at [70, 72] read
    as the set `screen` (record 1899), 36 Links ahead of the train's head;
    the light family's given clock [512, 1] on N = 1024 (k = pi / 2, the
    wavelength 4; THE GIVEN TRAIN, ALGEBRA.md 9.17 (6a)); no wheel anywhere
    (the rung's wheel is the record's own, W = 700). With `faces` "open"
    the face receiver `face` stands at both ends, last on every ladder
    (ALGEBRA.md 9.19 (3) (a)) on the chain of 140 with the body at [34, 66)
    and the screen at [100, 102], one train's length from both faces (the
    generator's placement rule, ALGEBRA.md 9.25 (11) (b)); the train leaves
    toward +x and nothing of it goes back but the tapers' dispersion."""
    length, corner, screen = (140, 34, 100) if faces == "open" else (80, 2, 70)
    document = {
        "shape": [length, 1, 1],
        "boundary": {"x": faces, "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "ticks": 600,
        "K": 1073741824,
        "N": PHASE_STEPS,
        "release": [1, 128],
        "clock_stamp": clock_stamp,
        "width": 1,
        "body_record": False,
        "engine": "examples/events/engine_start.json",
        "massive_record": True,
        "amplitude_bound": 1 << 22,
        "node_clock": NODE_CLOCK,
        "momentum_unit": 64,
        "universe": [
            {
                "name": "light",
                "quantum": 1,
                "pair": [1, 1],
                "phase_per_link": list(GIVEN_CLOCK),
                "charge": 0,
                "reads": reads(),
            },
            {"name": "matter", "quantum": 1, "pair": list(EMITTER_KIND), "charge": 0, "reads": reads()},
            dict(CLOCK_FAMILY),
            dict(CHARGE_FAMILY),
        ],
        "measured": [
            emitter_body([corner, 0, 0], stock, receiver),
        ],
        "detectors": [],
    }
    receiver_cube(document, "screen", [screen, 0, 0])
    if on_mode:
        massive_generator().seed_on_the_mode(document)
    return document


def test_the_loader_admits_the_key_and_refuses_the_ray_laws_instruments():
    world = parse_nature_beam_world(chain_world())
    assert world.hypotheses == []  # no identity beside the engine (ALGEBRA.md 9.90 (1))
    block = world.measured[0].block
    assert block is not None and block.emitter is not None and block.emitter.family == 0
    # the lamp is refused under the detector law (ALGEBRA.md 9.17): a giving
    # has a clicking record behind it
    with_lamp = chain_world()
    with_lamp["measured"][0] = {
        "position": [2, 0, 0],
        "family": "light",
        "amount": 6,
        "stocks": {},
        "momentum": [0, 0, 0],
        "lamp": {"rate": [1, 40], "wheel": [1, 64], "directions": [[1, 0, 0]], "train": 4},
    }
    with pytest.raises(ValueError, match="lamp is refused"):
        parse_nature_beam_world(with_lamp)
    for key in ("emits", "own_grace"):
        retired = chain_world()
        del retired["measured"][0]["emitter"]
        retired["measured"][0].update({"emits": "light", "own_grace": 70, "receiver": "screen"})
        if key == "own_grace":
            del retired["measured"][0]["emits"]
            del retired["measured"][0]["receiver"]
        with pytest.raises(ValueError, match=f"{key} is refused"):
            parse_nature_beam_world(retired)
    integer_clock = chain_world()
    integer_clock["universe"][0]["phase_per_link"] = 3
    with pytest.raises(ValueError, match="pair form of"):
        parse_nature_beam_world(integer_clock)


def test_the_rule_is_the_designs_integers_on_a_chain():
    """One step of the engine's rule equals the design's line
    3 a_next + r' = a_E + a_W + 4 a - 3 a_before + r on a one-layer chain
    (the y and z neighbours the row itself), with the remainder kept."""
    world = parse_nature_beam_world(chain_world())
    simulation = DetectorLawSimulation(world)
    rng = np.random.default_rng(7)
    now = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    remainder = rng.integers(0, 3, size=(80, 1, 1), dtype=np.int64)
    total = simulation._neighbours(now) - 3 * before + remainder
    expected = np.zeros_like(now)
    for x in range(80):
        left = now[x - 1, 0, 0] if x > 0 else 0
        right = now[x + 1, 0, 0] if x < 79 else 0
        expected[x, 0, 0] = left + right + 4 * now[x, 0, 0] - 3 * before[x, 0, 0] + remainder[x, 0, 0]
    assert np.array_equal(total, expected)
    nxt = np.floor_divide(total, 3)
    assert np.array_equal(total - 3 * nxt, np.mod(total, 3))


def test_chain_world_clicks_once_per_record_with_the_books_balanced():
    """The chain world under the flux reading (ALGEBRA.md 9.19 (3); BUILD.md section 26
    item 14): six givings at their rungs, every record clicking ONCE at `screen` (the
    cumulative ladder [screen] on the emitter's default ladder of every declared set, no
    face on a closed chain), its line at the rung's interval and the record deleted whole
    at it (never in `records` after its line), the flight of the train's head over the 36
    Links from the body's head at x = 33 to the screen at v_g = 0.447 (80 intervals) and
    as much of the passage as the residue asks (the train of 32 Nodes passes in 72), every
    click's quantum on the transit row `absorbed` and the screen body's `measured`, the
    books balanced. The edge case: the faces OPEN on the chain of 140 (the body at [34, 66)
    one train's length from the low face): the train leaves toward +x and the faces book
    nothing of it within the first 40 intervals (no click there), the screen not reached
    yet."""
    world = parse_nature_beam_world(chain_world())
    assert "face" not in DetectorLawSimulation(world).detector_names
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    for _ in range(600):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    givings = [line for line in lines if line["event"] == "giving"]
    gathers = [line for line in lines if line["event"] == "gather"]
    # the emitter's stock of 6 excitations, each clicking at its own rung; the
    # residues from the law (ALGEBRA.md 9.22 (4)): the clicking record's
    # remainder at the giving Node on Z_700
    # the wheel the rule's at the body's centre Node under the Node clock (the
    # stock 6 down to 1 at the six givings), u below it
    assert len(givings) == 6 and all(lawful_wheel(world, line) for line in givings)
    # the level at the body: one own quantum beside the stock, 7 down to 2 (item 47)
    assert [line["content"] for line in givings] == [7, 6, 5, 4, 3, 2]
    assert len(gathers) + sum(1 for live in simulation.records.values() if live.family == 0) == 6
    assert len(gathers) >= 3
    assert all("clock" in g and "giving" in g and "click" in g for g in gathers)
    for gather in gathers:
        assert gather["chosen"] == [["screen", 0, "0"]] and gather["click_at"] == "rung"
        assert gather["tick"] == gather["click"] and gather["record"] not in simulation.records
        flight = gather["click"] - gather["giving"]
        # the train's head over 36 Links at v_g = 0.447 (80 intervals), then as
        # much of the passage (72 intervals) as the residue asks (a residue near
        # W waits for the whole train: the residues spread from the kept
        # remainder, record 1962 (1)); the tapers' precursor a little before the
        # head (COMPUTATION)
        assert 60 <= flight <= 200, flight
    books = simulation.books()["families"]["light"]
    assert books["transit"]["absorbed"] == books["measured"]["measured"] == len(gathers)
    # the edge case: the open faces, the face receiver last on every ladder
    lines = []
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(chain_world(faces="open")), observer=lines.append
    )
    assert "face" in simulation.detector_names
    for _ in range(40):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    assert not [line for line in lines if line["event"] == "gather"]
    assert simulation.books()["families"]["light"]["measured"]["measured"] == 0


def test_the_emitters_cells_are_cells_like_every_other_and_take_nothing_of_its_record():
    """ALGEBRA.md 9.17 (the Boss's line on the knot): the emitter's own Nodes are Nodes like
    every other after the giving: no grace, no exemption, no own take. On the chain world
    the given record's row at the emitter's tail Node evolves under the rule (nonzero at ages
    after the giving, never held at 0), the ledger's row `taken_by_emitter` stays 0 (kept for the
    readers' form) and the records reading carries no `emitter_taking`; a `remnant_take` key
    on the emitter is refused as unknown; the world key `wheel`, a set's `wheel` and a
    family's `take` are refused by name (the retired keys, BUILD.md section 26 item 15); the
    books balanced."""
    world = parse_nature_beam_world(chain_world(1))
    simulation = DetectorLawSimulation(world)
    at_node: list[int] = []
    booked = 0
    for _ in range(200):
        simulation.step()
        live = simulation.records.get(1)
        if live is None:
            continue
        at_node.append(int(live.now[2, 0, 0]))
        booked = live.absorbed
    assert at_node and any(level != 0 for level in at_node[2:])
    assert booked > 0
    readings = dict(simulation.snapshot_stream())
    assert all("emitter_taking" not in record for record in readings.get("records", []))
    books = simulation.books()
    assert books["balanced"]
    light = books["families"]["light"]["transit"]
    assert light["taken_by_emitter"] == 0
    keyed = chain_world(on_mode=False)
    keyed["measured"][0]["emitter"]["remnant_take"] = 4
    with pytest.raises(ValueError, match="remnant_take"):
        parse_nature_beam_world(keyed)
    world_wheel = chain_world()
    world_wheel["wheel"] = 64
    with pytest.raises(ValueError, match="the world.wheel is refused"):
        parse_nature_beam_world(world_wheel)
    set_wheel = chain_world()
    set_wheel["detectors"][0]["wheel"] = 64
    set_wheel["stamp"] = input_stamp(set_wheel)  # the stamp over the whole file (item 28)
    with pytest.raises(ValueError, match=r"detectors\[0\]\.wheel is refused"):
        parse_nature_beam_world(set_wheel)
    on_light = chain_world()
    on_light["universe"][0]["take"] = [-15, 56]
    with pytest.raises(ValueError, match=r"families\[0\]\.take is refused"):
        parse_nature_beam_world(on_light)


def layer_world(receiver: object = None) -> dict:
    """A layer of 80 x 9 x 1 (x closed at both ends, mirrors; y and z
    periodic): the emitter body at [2, 34) across the whole width (the
    train's 32 Nodes by 9 of the matter kind on its mode, the stock 8: its
    train uniform across the periodic y, the extruded form of ALGEBRA.md
    9.22 (8)), three detector cubes of
    side 3 at x in [70, 72] on the rows y in [0, 2], [3, 5], [6, 8] read as
    the sets s0, s1, s2 (the screen, record 1899; s1 centred on the
    emitter's row, s0 and s2 its mirror images across the periodic seam).
    With `receiver`, the emitter's records' ladder is the named sets in the
    named order; without it, every declared set in the declared order
    (ALGEBRA.md 9.19 (3) (b))."""
    measured = [emitter_body([2, 0, 0], 8, receiver=receiver, extents=[32, 9, 1])]
    document = {
        "shape": [80, 9, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": 400,
        "K": 1073741824,
        "N": PHASE_STEPS,
        "release": [1, 128],
        "clock_stamp": True,
        "width": 1,
        "body_record": False,
        "engine": "examples/events/engine_start.json",
        "massive_record": True,
        "amplitude_bound": 1 << 22,
        "node_clock": NODE_CLOCK,
        "momentum_unit": 64,
        "universe": [
            {
                "name": "light",
                "quantum": 1,
                "pair": [1, 1],
                "phase_per_link": list(GIVEN_CLOCK),
                "charge": 0,
                "reads": reads(),
            },
            {"name": "matter", "quantum": 1, "pair": [800, 809], "charge": 0, "reads": reads()},
            dict(CLOCK_FAMILY),
            dict(CHARGE_FAMILY),
        ],
        "measured": measured,
        "detectors": [],
    }
    for index, y in enumerate((0, 3, 6)):
        receiver_cube(document, f"s{index}", [70, y, 0])
    massive_generator().seed_on_the_mode(document)
    return document


Seen = dict[int, tuple[int, list[int], list[int], int, int, int, int]]


def run_layer(document: dict, ticks: int = 3000) -> tuple[list[dict], DetectorLawSimulation, Seen]:
    """The layer world stepped with the books balanced at every interval; the gather lines,
    the simulation, and per clicked record what the click read (a spy on the engine's
    `_ladder_click`: the running total before the interval, the interval's increments, the
    ladder of `_ladder_of`, u, the norm and the record's own wheel W)."""
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    seen: Seen = {}
    spy_on(simulation, seen)
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return [line for line in lines if line["event"] == "gather"], simulation, seen


def spy_on(simulation: DetectorLawSimulation, seen: Seen) -> None:
    original = simulation._ladder_click

    def spy(live, increments):
        total = live.total
        original(live, increments)
        if live.clicked and live.identity not in seen:
            seen[live.identity] = (
                total,
                list(increments),
                simulation._ladder_of(live),
                live.u,
                live.norm,
                live.wheel,
                live.pace,
            )

    simulation._ladder_click = spy  # type: ignore[method-assign]


def chosen_by_the_rule(
    simulation: DetectorLawSimulation,
    total: int,
    increments: list[int],
    ladder: list[int],
    u: int,
    norm: int,
    wheel: int,
    pace: int,
) -> str:
    """The increment ladder of ALGEBRA.md 9.25 (2) on the click's own numbers: the running
    total C before the interval below the threshold, and the first detector k of the ladder at
    which 2 W p (C + f_1 + ... + f_k) >= (2 u + 1) T, the f the interval's plain increments and
    p the norm's pace (T in the body's own units, item 36)."""
    threshold = (2 * u + 1) * norm
    running = 2 * wheel * pace * total
    assert running < threshold
    for detector in ladder:
        running += 2 * wheel * pace * increments[detector]
        if running >= threshold:
            return simulation.detector_set[detector]
    raise AssertionError("no detector crossed")


RESIDUES = 128  # the planted records' wheel: every residue once


def planted_layer(order: tuple[str, ...]) -> tuple[list[dict], DetectorLawSimulation, Seen]:
    """The layer world without its emitter, RESIDUES light records planted at the emitter's
    Node at interval 0 with every residue of the wheel once (the given pair on the circle of
    2 N, the norm the conserved form) and the ladder the sets named in `order`; run 300
    intervals; the gather lines, the simulation and the spy's readings."""
    document = layer_world()
    document["measured"] = document["measured"][1:]
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    seen: Seen = {}
    spy_on(simulation, seen)
    level = round(UNIT * math.sin(math.pi * 512 / (1 * 1024)))
    ladder = [simulation.detector_names.index(name) for name in order]
    for u in range(RESIDUES):
        now = np.zeros(simulation.shape, dtype=np.int64)
        before = np.zeros(simulation.shape, dtype=np.int64)
        now[2, 4, 0] = level
        before[2, 4, 0] = -level
        live = LiveRecord(
            (1 << 40) + u,
            0,
            0,
            u,
            1,
            0,
            1,
            512,
            1,
            0,
            2,
            now,
            before,
            np.zeros(simulation.shape, dtype=np.int64),
            pointers=[0] * len(simulation.detector_names),
            first_rung=[None] * len(simulation.detector_names),
            wheel=RESIDUES,
            ladder=list(ladder),
        )
        live.norm, live.pace = simulation.given_norm(live)  # the form as the exact pair
        simulation.records[live.identity] = live
        simulation.ledger.transit_released[0] += 1
    for _ in range(300):
        simulation.step()
    return [line for line in lines if line["event"] == "gather"], simulation, seen


def lockstep_givings(
    first: dict, second: dict, ticks: int = 3000
) -> tuple[list[dict], list[dict], int | None]:
    """Two worlds stepped together (BUILD.md section 26 item 32, FINDING C): their giving
    lines and the first interval at which the family of clicks' level differs between them
    on the emitter body's Nodes or their shell (None if it never does)."""
    runs: list[tuple[DetectorLawSimulation, list[dict]]] = []
    for document in (first, second):
        lines: list[dict] = []
        simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
        runs.append((simulation, lines))
    mask = runs[0][0].block_by_number[0].mask
    near = mask.copy()
    for axis in range(3):
        for shift in (-1, 1):
            near |= np.roll(mask, shift, axis=axis)
    differs = None
    for _ in range(ticks):
        for simulation, _lines in runs:
            simulation.step()
        if differs is None and not np.array_equal(
            runs[0][0].held_record("content").now[near], runs[1][0].held_record("content").now[near]
        ):
            differs = runs[0][0].tick
    givings = [[line for line in lines if line["event"] == "giving"] for _run, lines in runs]
    return givings[0], givings[1], differs


def test_the_increment_ladder_over_the_named_sets():
    """THE INCREMENT LADDER (ALGEBRA.md 9.25 (2), the mathematician's word of 2026-09-25 on
    the finding of item 14; the cumulative sums withdrawn): 128 light records planted at
    the layer's emitter Node with every residue of the wheel 128 once and the ladder [s0,
    s1, s2]: every record clicks exactly once, at the detector the walk of 9.25 (2) names on
    the click's own numbers (the running total before the interval below the threshold,
    the first detector of the ladder at which the interval's increments carry it across); the
    counts per detector under [s0, s1, s2] agree with the counts under [s2, s1, s0] within the
    sampling of 128 residues (the detector's share of the record's total inward flux, whatever
    the order, 9.25 (3): a theorem in distribution; on eight residues the exact counts
    are (4, 2, 2) against (2, 2, 4), the first detector of the ladder holding more of the eight
    thresholds, COMPUTATION for the mathematician), s0 and s2 alike within the same
    sampling (the placement's symmetry about the emitter's row). The emitter's own givings
    carry residues spread from the kept remainder (the model owner's decisions (1) and (2)
    of record 1962; the coupling's back-action of 9.19 (4e) HISTORY), each
    clicking at the detector the walk names on its own numbers, the line's `ladder` the names and
    its `sunk` the pointers off the ladder; under the family of clicks (item 32, FINDING C)
    the two ladder orders are read in lockstep: the residues read before the clock field
    differs at the body agree bit for bit (all eight since item 33's count of intervals;
    six of eight on item 32's head, the later two differing). The
    loader refuses a name no set declares, a repeated name, an empty list, and a body's
    `coupling` by name."""
    counts: dict[tuple[str, ...], dict[str, int]] = {}
    for order in (("s0", "s1", "s2"), ("s2", "s1", "s0")):
        gathers, simulation, seen = planted_layer(order)
        assert len(gathers) == RESIDUES and len({g["record"] for g in gathers}) == RESIDUES
        for gather in gathers:
            total, increments, ladder, u, norm, wheel, pace = seen[gather["record"]]
            assert wheel == RESIDUES and u == gather["u"] and gather["record"] not in simulation.records
            assert ladder == [simulation.detector_names.index(name) for name in order]
            assert gather["chosen"][0][0] == chosen_by_the_rule(
                simulation, total, increments, ladder, u, norm, wheel, pace
            )
        counts[order] = {
            name: sum(1 for g in gathers if g["chosen"][0][0] == name) for name in ("s0", "s1", "s2")
        }
    forward, backward = counts[("s0", "s1", "s2")], counts[("s2", "s1", "s0")]
    assert all(abs(forward[name] - backward[name]) <= 12 for name in forward), counts
    assert abs(forward["s0"] - forward["s2"]) <= 12 and min(forward.values()) > 0, counts
    # the emitter's own givings: the residues spread from the kept remainder
    gathers, simulation, seen = run_layer(layer_world(["s0", "s1", "s2"]))
    assert len(gathers) == 8 and len({g["u"] for g in gathers}) > 1
    names = [simulation.detector_names.index(name) for name in ("s0", "s1", "s2")]
    for gather in gathers:
        assert gather["ladder"] == ["s0", "s1", "s2"] and gather["record"] not in simulation.records
        total, increments, ladder, u, norm, wheel, pace = seen[gather["record"]]
        # the record's wheel the rule's at the body's Node with its content as the giving
        # finds it (the own quantum and the stock 8 down to 1: 9 down to 2; ONE ORDER FOR
        # BOTH CLICKS, ALGEBRA.md 9.85 (2), item 58); the wheel divides the weak-field wall
        # 6 den Gamma^2 (9.57 (1); item 44); the norm's denominator divides the rule's read
        # coefficient at the body's content the giving found
        assert ladder == names and (6 * EMITTER_PAIR[1] * NODE_CLOCK**2) % wheel == 0
        assert 0 <= u < wheel and any(
            coefficients(EMITTER_PAIR[0], EMITTER_PAIR[1], NODE_CLOCK, c)[0][0] % pace == 0
            for c in range(10)
        )
        assert gather["chosen"][0][0] == chosen_by_the_rule(
            simulation, total, increments, ladder, u, norm, wheel, pace
        )
        assert gather["T"] >= gather["sunk"] >= 0
    # THE REVERSED ORDER under the family of clicks (ALGEBRA.md 9.45; BUILD.md section 26
    # item 32, FINDING C): the residues are the body's own record's, read at the first
    # shell Node at each click (item 33), and the ladder's order is no input to them UNTIL
    # the clock field differs at the body: the first click (at 136, at s0 under one order
    # and at s2 under the other) writes its content at the set's first body (row 0 or row
    # 6, no mirror images across the seam), the difference spreads by the family's own
    # step to the body's shell (interval 216) and to the own record's remainder (240);
    # every residue read before that agrees bit for bit (all eight here, the last read at
    # 209: the tick counts intervals, item 33; on item 32's head six of eight, the two
    # read after 309 differing; COMPUTATION)
    forward_givings, backward_givings, differs = lockstep_givings(
        layer_world(["s0", "s1", "s2"]), layer_world(["s2", "s1", "s0"])
    )
    assert len(forward_givings) == len(backward_givings) == 8 and differs is not None
    assert sorted(line["u"] for line in forward_givings) == sorted(g["u"] for g in gathers)
    reads = [1] + [line["tick"] for line in forward_givings[:-1]]
    agreed = [
        (forward["u"] == backward["u"], read)
        for forward, backward, read in zip(forward_givings, backward_givings, reads, strict=True)
    ]
    assert all(same for same, read in agreed if read < differs)
    assert sum(1 for _same, read in agreed if read < differs) >= 3
    # one set on the emitter's row alone books a third of the flux: the last click at 1014
    # under the one border (the well two Links from the closed face; item 28), COMPUTATION
    one, _, _ = run_layer(layer_world("s1"))  # every giving a window and a rung (commit 7)
    assert len(one) == 8 and all(gather["chosen"][0][0] == "s1" for gather in one)
    with pytest.raises(ValueError, match="names 'screen', which no detector set declares"):
        parse_nature_beam_world(layer_world(["s0", "screen"]))
    with pytest.raises(ValueError, match="names a set twice"):
        parse_nature_beam_world(layer_world(["s0", "s0"]))
    with pytest.raises(ValueError, match="nonempty list of names"):
        parse_nature_beam_world(layer_world([]))
    coupled = layer_world("s1")
    coupled["measured"][0]["coupling"] = {"G": [1, 50], "g": [1, 1000]}
    with pytest.raises(ValueError, match=r"measured\[0\]\.coupling is refused: the coupling retired"):
        parse_nature_beam_world(coupled)


def test_detector_is_one_connected_cube_of_side_three():
    """THE DETECTOR CUBE (the model owner's word of 2026-09-25, record 1899; ALGEBRA.md 9.25
    (7)): a detector is one region, a cube of side 3 or more, its click the detector's.
    On the layer of 80 x 9, beyond the emitter's box, the loader refuses a cube of side 2 (the 2 x 2 box at (40, 2)
    naming its sides [2, 2, 1]), admits a cube of side 3 (the 3 x 3 box at (40, 2); the
    layer's thin z axis cuts the cube to one Node deep), admits the 3 x 3 box wrapped across
    the periodic seam (y = 8, 0, 1: one piece, one box), refuses a disconnected set (two
    bodies at (40, 2) and (43, 2), naming the two pieces) and refuses a connected set that
    fills no box (the 3 x 3 box less its centre, naming its Nodes); a set bound to a block
    admits a block of side 1 as its Nodes (SINCE COMMIT 7 a body is its own detector whatever
    its support, ALGEBRA.md 9.92, record 2109) and one of side 3; the engine reads the
    admitted cube as ONE detector whose Nodes are the cube's (the click line names the set and
    places no Node)."""
    box = [[x, y, 0] for x in (40, 41, 42) for y in (2, 3, 4)]
    wrapped = [[x, y, 0] for x in (40, 41, 42) for y in (8, 0, 1)]
    for positions, refusal in (
        ([[x, y, 0] for x in (10, 11) for y in (2, 3)], r"is a box of sides \[2, 2, 1\]"),
        (box, None),
        (wrapped, None),
        ([[40, 2, 0], [43, 2, 0]], "lies on 2 disconnected pieces"),
        ([p for p in box if p != [41, 3, 0]], "on 8 Nodes fills no box"),
    ):
        document = layer_world()
        document["measured"].extend(receiver_body(position) for position in positions)
        document["detectors"].append({"name": "cube", "positions": positions})
        document["stamp"] = input_stamp(document)  # the stamp over the whole file (item 28)
        if refusal is None:
            simulation = DetectorLawSimulation(parse_nature_beam_world(document))
            detector = simulation.detector_names.index("cube")
            nodes = {tuple(p) for p in positions}
            assert {
                tuple(int(v) for v in node)
                for node in zip(*np.nonzero(simulation.detector_at_node == detector), strict=True)
            } == nodes
        else:
            with pytest.raises(ValueError, match=refusal):
                parse_nature_beam_world(document)
    for side, refusal in ((1, None), (3, None)):
        document = layer_world()
        document["measured"].append(
            {
                "position": [40, 2, 0],
                "family": "light",
                "amount": 1,
                "stocks": {},
                "ramp": 0,
                "start": 0,
                "momentum": [0, 0, 0],
                "side": side,
                "q": 0,
                "spin": [0, 0, 0],
                "twist": 0,
                "moment": [0, 0, 0],
                "pair": [1, 2],
            }
        )
        document["detectors"].append({"name": "on_block", "block": len(document["measured"]) - 1})
        document["stamp"] = input_stamp(document)  # the stamp over the whole file (item 28)
        if refusal is None:
            parse_nature_beam_world(document)
        else:
            with pytest.raises(ValueError, match=refusal):
                parse_nature_beam_world(document)
