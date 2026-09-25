"""The local detector law (`detector-law-v1`, docs/designs/detector_law/DESIGN.md),
the build's first gate: the loader's key and refusals, the rule's step against
the design's integers, and one chain world run headless (an emitter body at one
end, a receiver at the other, the open face behind the emitter): one click per
record, the books balanced at every tick, the click's time at the front's
first rung about L / c after the birth, the click line with the stamp. SINCE
THE EMITTER AS A CLICKING BODY (ALGEBRA.md 9.17; BUILD.md section 26) the
lamp is refused under the detector law: the chain world's source is a body
of the matter kind seeded on its bound mode, its excitations clicking at
their rungs and writing the born record once; the grace, the exemption and
the emitter's own take are retired (its cells are cells like every other)."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.events.detector_law import UNIT, DetectorLawSimulation, LiveRecord
from event_universe.events.world import DETECTOR_LAW_RULE, parse_nature_beam_world
from tests.test_emitter import massive_generator

EMITTER_KIND = [7, 8]  # the emitter body's kind (omega_0 = 0.505)
EMITTER_PAIR = [
    801,
    700,
]  # its one-cell well, rich (W = 700 remainder values, ALGEBRA.md 9.22 (4)), bound on a chain (2 cos omega_b = 1.90)


def emitter_body(
    position: list[int],
    stock: int,
    receiver: object = None,
    side: int = 1,
    family: str = "light",
) -> dict:
    """An emitter body of the matter kind EMITTER_KIND (the well pair EMITTER_PAIR, seeded on
    its mode at 100 by the generator), its stock `stock`, its `emitter` the family given and,
    with `receiver`, the born records' ladder by name. The residue and the wheel are the
    law's (ALGEBRA.md 9.22 (4): the clicking record's remainder at the birth cell, W = 700 on
    EMITTER_PAIR). The cadence (COMPUTATION, BUILD.md section 26): the residue u clicks about
    (2 u + 1) / (2 W) x P intervals after its excitation, P the mode's period; a well too
    deep for its board is a runaway and refused at the margin rule."""
    emitter: dict = {"family": family}
    if receiver is not None:
        emitter["receiver"] = receiver
    return {
        "position": position,
        "family": "matter",
        "amount": stock,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "side": side,
        "pair": list(EMITTER_PAIR),
        "seed": 100,
        "emitter": emitter,
    }


def chain_world(
    stock: int = 6,
    receiver: object = None,
    clock_stamp: bool = True,
    on_mode: bool = True,
    faces: str = "closed",
) -> dict:
    """A chain of 80 Nodes (y and z periodic, one layer each; x CLOSED, the
    zero rows at both ends mirrors): the emitter body at x = 2 (one cell,
    the matter kind [7, 8] with the well pair [8, 7], its mode the seed), a
    receiver body at x = 70 read as the set `screen`; the light family's
    clock the pair [77, 25] on N = 64 (3.08 steps per interval, the period
    20.78 intervals, lambda = 12 Links); no wheel anywhere (the rung's wheel
    is the record's own, W = 700). With `faces` "open" the face receiver
    `face` stands at both ends, last on every ladder (ALGEBRA.md 9.19 (3)
    (a)): two Links behind the emitter it clicks the half that leaves."""
    document = {
        "law": "beam",
        "model_id": "beam-detector-law-chain-v1",
        "shape": [80, 1, 1],
        "boundary": {"x": faces, "y": "periodic", "z": "periodic"},
        "ticks": 400,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": clock_stamp,
        "detector_law": True,
        "massive_record": True,
        "amplitude_bound": 1 << 32,
        "directions": [],
        "families": [
            {"name": "light", "quantum": 1, "phase_per_link": [77, 25]},
            {"name": "matter", "quantum": 1, "pair": list(EMITTER_KIND)},
        ],
        "measured": [
            emitter_body([2, 0, 0], stock, receiver),
            {
                "position": [70, 0, 0],
                "family": "light",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[-1, 0, 0]],
            },
        ],
        "detectors": [{"name": "screen", "positions": [[70, 0, 0]], "threshold": 1}],
    }
    if on_mode:
        massive_generator().seed_on_the_mode(document)
    return document


def test_the_loader_admits_the_key_and_refuses_the_ray_laws_instruments():
    world = parse_nature_beam_world(chain_world())
    assert world.detector_law
    assert DETECTOR_LAW_RULE in world.hypotheses
    block = world.measured[0].block
    assert block is not None and block.emitter is not None and block.emitter.family == 0
    # the lamp is refused under the detector law (ALGEBRA.md 9.17): a birth
    # has a clicking record behind it
    with_lamp = chain_world()
    with_lamp["measured"][0] = {
        "position": [2, 0, 0],
        "family": "light",
        "amount": 6,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "directions": [[1, 0, 0]],
        "lamp": {"rate": [1, 40], "wheel": [1, 64], "directions": [[1, 0, 0]], "train": 4},
    }
    with pytest.raises(ValueError, match="lamp is refused under detector-law-v1"):
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
    integer_clock["families"][0]["phase_per_link"] = 3
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


def test_a_chain_world_clicks_once_per_record_with_the_books_balanced():
    """The chain world under the flux reading (ALGEBRA.md 9.19 (3); BUILD.md section 26
    item 14): six births at their rungs, every record clicking ONCE at `screen` (the
    cumulative ladder [screen] on the emitter's default ladder of every declared set, no
    face on a closed chain), its line at the rung's interval and the record deleted whole
    at it (never in `records` after its line), the flight of the +x half's front over the
    68 Links at c = 0.577 (100 to 140 intervals), every click's quantum on the transit
    row `absorbed` and the screen body's `measured`, the books balanced. The edge case:
    the faces OPEN, the face receiver `face` two Links behind the emitter: the first
    record's -x half leaves through it and clicks there within twelve intervals of the
    birth, the record deleted, nothing yet at the screen."""
    world = parse_nature_beam_world(chain_world())
    assert "face" not in DetectorLawSimulation(world).cell_names
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    for _ in range(600):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    births = [line for line in lines if line["event"] == "birth"]
    gathers = [line for line in lines if line["event"] == "gather"]
    # the emitter's stock of 6 excitations, each clicking at its own rung; the
    # residues from the law (ALGEBRA.md 9.22 (4)): the clicking record's
    # remainder at the birth cell on Z_700
    assert len(births) == 6 and all(0 <= line["u"] < 700 and line["W"] == 700 for line in births)
    assert len(gathers) + sum(1 for live in simulation.records.values() if live.family == 0) == 6
    assert len(gathers) >= 4
    assert all("clock" in g and "birth" in g and "click" in g for g in gathers)
    for gather in gathers:
        assert gather["chosen"] == [["screen", 0, "0"]] and gather["click_at"] == "rung"
        assert gather["tick"] == gather["click"] and gather["record"] not in simulation.records
        flight = gather["click"] - gather["birth"]
        # the front's first rung about L / c = 68 / 0.577 = 118 intervals after the birth
        assert 100 <= flight <= 140, flight
    books = simulation.books()["families"]["light"]
    assert books["transit"]["absorbed"] == books["measured"]["measured"] == len(gathers)
    # the edge case: the open faces, the face receiver last on every ladder
    lines = []
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(chain_world(faces="open")), observer=lines.append
    )
    assert "face" in simulation.cell_names
    for _ in range(40):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    first = next(line for line in lines if line["event"] == "gather")
    assert first["chosen"] == [["face", 0, "0"]] and first["click"] - first["birth"] <= 12
    assert first["record"] not in simulation.records
    assert simulation.books()["families"]["light"]["measured"]["measured"] == 0


def test_the_emitters_cells_are_cells_like_every_other_and_take_nothing_of_its_record():
    """ALGEBRA.md 9.17 (the Boss's line on the knot): the emitter's own cells are cells like
    every other after the birth: no grace, no exemption, no own take. On the chain world
    the born record's row at the emitter's cell evolves under the rule (nonzero at ages after
    the birth, never held at 0), the ledger's row `taken_by_emitter` stays 0 (kept for the
    readers' form) and the records reading carries no `emitter_taking`; a `remnant_take` key
    on the emitter is refused as unknown; the world key `wheel`, a set's `wheel` and a
    family's `take` are refused by name (the retired keys, BUILD.md section 26 item 15); the
    books balanced."""
    world = parse_nature_beam_world(chain_world(1))
    simulation = DetectorLawSimulation(world)
    at_cell: list[int] = []
    booked = 0
    for _ in range(200):
        simulation.step()
        live = simulation.records.get(1)
        if live is None:
            continue
        at_cell.append(int(live.now[2, 0, 0]))
        booked = live.absorbed
    assert at_cell and any(level != 0 for level in at_cell[2:])
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
    world_wheel = chain_world(on_mode=False)
    world_wheel["wheel"] = 64
    with pytest.raises(ValueError, match="the world.wheel is refused"):
        parse_nature_beam_world(world_wheel)
    set_wheel = chain_world(on_mode=False)
    set_wheel["detectors"][0]["wheel"] = 64
    with pytest.raises(ValueError, match=r"detectors\[0\]\.wheel is refused"):
        parse_nature_beam_world(set_wheel)
    on_light = chain_world(on_mode=False)
    on_light["families"][0]["take"] = [-15, 56]
    with pytest.raises(ValueError, match=r"families\[0\]\.take is refused"):
        parse_nature_beam_world(on_light)


def layer_world(receiver: object = None) -> dict:
    """A layer of 24 x 7 x 1 (x closed at both ends, mirrors; y and z
    periodic): the emitter body at [2, 3, 0] (the matter kind on its mode,
    the stock 8), three receiver bodies at x = 18 on the
    rows y = 2, 3, 4 read as the sets s0, s1, s2 (one Node each, the
    screen). With `receiver`, the emitter's records' ladder is the named
    sets in the named order; without it, every declared set in the
    declared order (ALGEBRA.md 9.19 (3) (b))."""
    measured = [emitter_body([2, 3, 0], 8, receiver=receiver)]
    detectors = []
    for index, y in enumerate((2, 3, 4)):
        measured.append(
            {
                "position": [18, y, 0],
                "family": "light",
                "amount": 1,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[-1, 0, 0]],
            }
        )
        detectors.append({"name": f"s{index}", "positions": [[18, y, 0]], "threshold": 1})
    document = {
        "law": "beam",
        "model_id": "beam-detector-law-layer-v1",
        "shape": [24, 7, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": 400,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        "amplitude_bound": 1 << 32,
        "directions": [],
        "families": [
            {"name": "light", "quantum": 1, "phase_per_link": [77, 25]},
            {"name": "matter", "quantum": 1, "pair": [800, 809]},
        ],
        "measured": measured,
        "detectors": detectors,
    }
    massive_generator().seed_on_the_mode(document)
    return document


Seen = dict[int, tuple[int, list[int], list[int], int, int, int]]


def run_layer(document: dict, ticks: int = 900) -> tuple[list[dict], DetectorLawSimulation, Seen]:
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
) -> str:
    """The increment ladder of ALGEBRA.md 9.25 (2) on the click's own numbers: the running
    total C before the interval below the threshold, and the first cell k of the ladder at
    which 2 W (C + f_1 + ... + f_k) >= (2 u + 1) T, the f the interval's increments."""
    threshold = (2 * u + 1) * norm
    running = 2 * wheel * total
    assert running < threshold
    for cell in ladder:
        running += 2 * wheel * increments[cell]
        if running >= threshold:
            return simulation.cell_set[cell]
    raise AssertionError("no cell crossed")


RESIDUES = 128  # the planted records' wheel: every residue once


def planted_layer(order: tuple[str, ...]) -> tuple[list[dict], DetectorLawSimulation, Seen]:
    """The layer world without its emitter, RESIDUES light records planted at the emitter's
    Node at interval 0 with every residue of the wheel once (the born pair on the circle of
    2 N, the norm the conserved form) and the ladder the sets named in `order`; run 300
    intervals; the gather lines, the simulation and the spy's readings."""
    document = layer_world()
    document["measured"] = document["measured"][1:]
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    seen: Seen = {}
    spy_on(simulation, seen)
    level = int(simulation._cosine_table(128)[(96 + 77 // 25) % 128])
    ladder = [simulation.cell_names.index(name) for name in order]
    for u in range(RESIDUES):
        now = np.zeros(simulation.shape, dtype=np.int64)
        before = np.zeros(simulation.shape, dtype=np.int64)
        now[2, 3, 0] = level
        before[2, 3, 0] = -level
        live = LiveRecord(
            (1 << 40) + u,
            0,
            0,
            u,
            1,
            0,
            1,
            77,
            25,
            0,
            21,
            now,
            before,
            np.zeros(simulation.shape, dtype=np.int64),
            pointers=[0] * len(simulation.cell_names),
            first_rung=[None] * len(simulation.cell_names),
            wheel=RESIDUES,
            ladder=list(ladder),
        )
        live.norm = simulation.conserved_form(live)
        simulation.records[live.identity] = live
        simulation.ledger.transit_released[0] += 1
    for _ in range(300):
        simulation.step()
    return [line for line in lines if line["event"] == "gather"], simulation, seen


def test_the_increment_ladder_over_the_named_sets():
    """THE INCREMENT LADDER (ALGEBRA.md 9.25 (2), the mathematician's word of 2026-09-25 on
    the finding of item 14; the cumulative sums withdrawn): 128 light records planted at
    the layer's emitter Node with every residue of the wheel 128 once and the ladder [s0,
    s1, s2]: every record clicks exactly once, at the cell the walk of 9.25 (2) names on
    the click's own numbers (the running total before the interval below the threshold,
    the first cell of the ladder at which the interval's increments carry it across); the
    counts per cell under [s0, s1, s2] agree with the counts under [s2, s1, s0] within the
    sampling of 128 residues (the cell's share of the record's total inward flux, whatever
    the order, 9.25 (3): a theorem in distribution; on eight residues the exact counts
    are (4, 2, 2) against (2, 2, 4), the first cell of the ladder holding more of the eight
    thresholds, COMPUTATION for the mathematician), s0 and s2 alike within the same
    sampling (the placement's symmetry about the emitter's row). The emitter's own births (the same residue at
    every birth of a body without a coupling, item 15) all click at one cell under either
    order (the cell itself depends on the order, the walk names it), the line's `ladder`
    the names and its `sunk` the pointers off the ladder. The
    loader refuses a name no set declares, a repeated name and an empty list."""
    counts: dict[tuple[str, ...], dict[str, int]] = {}
    for order in (("s0", "s1", "s2"), ("s2", "s1", "s0")):
        gathers, simulation, seen = planted_layer(order)
        assert len(gathers) == RESIDUES and len({g["record"] for g in gathers}) == RESIDUES
        for gather in gathers:
            total, increments, ladder, u, norm, wheel = seen[gather["record"]]
            assert wheel == RESIDUES and u == gather["u"] and gather["record"] not in simulation.records
            assert ladder == [simulation.cell_names.index(name) for name in order]
            assert gather["chosen"][0][0] == chosen_by_the_rule(
                simulation, total, increments, ladder, u, norm, wheel
            )
        counts[order] = {
            name: sum(1 for g in gathers if g["chosen"][0][0] == name) for name in ("s0", "s1", "s2")
        }
    forward, backward = counts[("s0", "s1", "s2")], counts[("s2", "s1", "s0")]
    assert all(abs(forward[name] - backward[name]) <= 12 for name in forward), counts
    assert abs(forward["s0"] - forward["s2"]) <= 12 and min(forward.values()) > 0, counts
    # the emitter's own births: one residue, one cell, under either order
    gathers, simulation, seen = run_layer(layer_world(["s0", "s1", "s2"]))
    assert len(gathers) == 8 and len({g["chosen"][0][0] for g in gathers}) == 1
    names = [simulation.cell_names.index(name) for name in ("s0", "s1", "s2")]
    for gather in gathers:
        assert gather["ladder"] == ["s0", "s1", "s2"] and gather["record"] not in simulation.records
        total, increments, ladder, u, norm, wheel = seen[gather["record"]]
        assert ladder == names and wheel == 700 and 0 <= u < wheel
        assert gather["chosen"][0][0] == chosen_by_the_rule(
            simulation, total, increments, ladder, u, norm, wheel
        )
        assert gather["T"] >= gather["sunk"] >= 0
    # the reversed order: one residue, one cell again (the cell of a single
    # record depends on the order; the shares over the residues do not)
    backward, _, _ = run_layer(layer_world(["s2", "s1", "s0"]))
    assert len(backward) == 8 and len({g["chosen"][0][0] for g in backward}) == 1
    one, _, _ = run_layer(layer_world("s1"))
    assert len(one) == 8 and all(gather["chosen"][0][0] == "s1" for gather in one)
    with pytest.raises(ValueError, match="names 'screen', which no detector set declares"):
        parse_nature_beam_world(layer_world(["s0", "screen"]))
    with pytest.raises(ValueError, match="names a set twice"):
        parse_nature_beam_world(layer_world(["s0", "s0"]))
    with pytest.raises(ValueError, match="nonempty list of names"):
        parse_nature_beam_world(layer_world([]))


def test_a_detector_is_one_connected_region():
    """ALGEBRA.md 9.25 (7), the model owner's word: a receiver's Nodes are connected by Links;
    two receiver bodies at (10, 2, 0) and (13, 2, 0) under one name are refused naming the
    two pieces, at (10, 2, 0) and (11, 2, 0) admitted, and at (10, 0, 0) and (10, 6, 0)
    across the layer's periodic seam admitted (one piece)."""
    for positions, admitted in (
        ([[10, 2, 0], [13, 2, 0]], False),
        ([[10, 2, 0], [11, 2, 0]], True),
        ([[10, 0, 0], [10, 6, 0]], True),
    ):
        document = layer_world()
        for position in positions:
            document["measured"].append(
                {
                    "position": position,
                    "family": "light",
                    "amount": 1,
                    "phase": 0,
                    "momentum": [0, 0, 0],
                    "fixed": True,
                    "directions": [[-1, 0, 0]],
                }
            )
        document["detectors"].append({"name": "pair", "positions": positions, "threshold": 1})
        if admitted:
            parse_nature_beam_world(document)
        else:
            with pytest.raises(ValueError, match="lies on 2 disconnected pieces"):
                parse_nature_beam_world(document)
