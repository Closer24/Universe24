"""The engine's first gate: the loader's keys and refusals, the rule's step against the declared integers, and one chain world (an emitter body, a receiver, the open face) with one click per record, the books balanced every tick and the click's time near L / c after the giving."""

import math
from dataclasses import replace

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation, LiveRecord
from event_universe.features.send import send
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.running import Seen, chosen_by_the_rule, lines_of, spy_on, stamped
from tests.worlds import (
    EMITTER_PAIR,
    NODE_CLOCK,
    chain_world,
    emitter_world,
    lawful_wheel,
    layer_world,
    receiver_body,
)

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md #the-line; the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


def test_the_loader_admits_the_key_and_refuses_the_ray_laws_instruments():
    world = parse_nature_beam_world(chain_world())
    assert world.hypotheses == []  # no identity beside the engine (ALGEBRA.md #the-primitives)
    block = world.measured[0].block
    assert block is not None and block.emitter is not None and block.emitter.family == 0
    # the lamp is refused under the detector law (ALGEBRA.md #the-click): a giving has a clicking record behind it
    with_lamp = chain_world()
    with_lamp["measured"][0] = {
        "position": [2, 0, 0],
        "family": "light",
        "amount": 6,
        "stocks": {},
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "lamp": {"rate": [1, 40], "wheel": [1, 64], "directions": [[1, 0, 0]], "train": 4},
    }
    with pytest.raises(ValueError, match="has unknown keys: lamp"):
        parse_nature_beam_world(with_lamp)
    for key in ("emits", "own_grace"):
        retired = chain_world()
        del retired["measured"][0]["emitter"]
        retired["measured"][0].update({"emits": "light", "own_grace": 70, "receiver": "screen"})
        if key == "own_grace":
            del retired["measured"][0]["emits"]
            del retired["measured"][0]["receiver"]
        with pytest.raises(ValueError, match=f"has unknown keys: {key}"):
            parse_nature_beam_world(retired)
    integer_clock = chain_world()
    integer_clock["universe"][0]["clock"] = 3
    with pytest.raises(ValueError, match="clock must be a list, not 3"):
        parse_nature_beam_world(integer_clock)


def test_the_rule_is_the_designs_integers_on_a_chain():
    """One step of the engine's rule equals the design's line 3 a_next + r' = a_E + a_W + 4 a - 3 a_before + r on a one-layer chain (the y and z neighbours the row itself), with the remainder kept."""
    world = parse_nature_beam_world(chain_world())
    simulation = DetectorLawSimulation(world)
    rng = np.random.default_rng(7)
    now = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(80, 1, 1), dtype=np.int64)
    remainder = rng.integers(0, 3, size=(80, 1, 1), dtype=np.int64)
    total = send(simulation.ports, now) - 3 * before + remainder
    expected = np.zeros_like(now)
    for x in range(80):
        left = now[x - 1, 0, 0] if x > 0 else 0
        right = now[x + 1, 0, 0] if x < 79 else 0
        expected[x, 0, 0] = left + right + 4 * now[x, 0, 0] - 3 * before[x, 0, 0] + remainder[x, 0, 0]
    assert np.array_equal(total, expected)
    nxt = np.floor_divide(total, 3)
    assert np.array_equal(total - 3 * nxt, np.mod(total, 3))


def test_chain_world_clicks_once_per_record_with_the_books_balanced():
    """The chain world under the flux reading (ALGEBRA.md #rule3; BUILD.md section 26 item 14): six givings at their rungs, every record clicking ONCE at `screen` (the cumulative ladder [screen] on the emitter's default ladder of every declared set, no face on a closed chain), its line at the rung's interval and the record deleted whole at it (never in `records` after its line), the flight of the train's head over the 36 Links from the body's head at x = 33 to the screen at v_g = 0.447 (80 intervals) and as much of the passage as the residue asks (the train of 32 Nodes passes in 72), every click's quantum on the transit row `absorbed` and the screen body's `measured`, the books balanced (the body's content level on the giving line is a GameBoard reading, a diagnostic; the level sequence is pinned on the emitter world in tests/test_emitter.py). The edge case: the faces OPEN on the chain of 140 (the body at [34, 66) one train's length from the low face): the train leaves toward +x and the faces book nothing of it within the first 40 intervals (no click there), the screen not reached yet."""
    world = parse_nature_beam_world(chain_world())
    assert "face" not in DetectorLawSimulation(world).detector_names
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    # the horizon the window the engine writes by the law, no number: the stock's six windows closed and the last train's flight bound (below) after the sixth, within six times the first close
    while len(givings := lines_of(lines, "giving")) < 6 or simulation.tick < givings[-1]["tick"] + 200:
        simulation.step()
        cap = 6 * givings[0]["tick"] + 200 if givings else 200
        assert simulation.books()["balanced"] and simulation.tick <= cap
    gathers = lines_of(lines, "gather")
    # the emitter's stock of 6 excitations, each clicking at its own rung; the residues from the law (ALGEBRA.md #a-familys-declaration): the clicking record's remainder at the giving Node on Z_700 the wheel the rule's at the body's centre Node under the Node clock (the stock 6 down to 1 at the six givings), u below it
    assert len(givings) == 6 and all(lawful_wheel(world, line) for line in givings)
    assert len(gathers) + sum(1 for live in simulation.records.values() if live.family == 0) == 6
    assert len(gathers) >= 3 and all("clock" in g and "giving" in g and "click" in g for g in gathers)
    for gather in gathers:
        assert gather["chosen"] == [["screen", 0, "0"]] and gather["click_at"] == "rung"
        assert gather["tick"] == gather["click"] and gather["record"] not in simulation.records
        flight = gather["click"] - gather["giving"]
        # the train's head over 36 Links at v_g = 0.447 (80 intervals), then as much of the passage (72 intervals) as the residue asks (a residue near W waits for the whole train: the residues spread from the kept remainder, record 1962 (1)); the tapers' precursor a little before the head (COMPUTATION)
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
    """ALGEBRA.md #the-click (the Boss's line on the knot): the emitter's own Nodes are Nodes like every other after the giving: no grace, no exemption, no own take. On the chain world the given record's row at the emitter's tail Node evolves under the rule (nonzero at ages after the giving, never held at 0), the ledger's row `taken_by_emitter` stays 0 (kept for the readers' form) and the records reading carries no `emitter_taking`; a `remnant_take` key on the emitter is refused as unknown; the world key `wheel`, a set's `wheel` and a family's `take` are refused by name (the retired keys, BUILD.md section 26 item 15); the books balanced."""
    world = parse_nature_beam_world(chain_world(1))
    simulation = DetectorLawSimulation(world)
    at_node: list[int] = []
    booked = 0
    first: int | None = None
    for _ in range(200):
        simulation.step()
        first = first if first is not None else next(iter(simulation.blocks[0].emitted), None)
        live = simulation.records.get(first)
        if live is None:
            continue
        at_node.append(int(live.now[2, 0, 0]))
        booked = live.absorbed
    assert at_node and any(level != 0 for level in at_node[2:]) and booked > 0
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
    with pytest.raises(ValueError, match="the world has unknown keys: wheel"):
        parse_nature_beam_world(world_wheel)
    set_wheel = chain_world()
    set_wheel["detectors"][0]["wheel"] = 64
    set_wheel["stamp"] = input_stamp(set_wheel)  # the stamp over the whole file (item 28)
    with pytest.raises(ValueError, match=r"detectors\[0\] has unknown keys: wheel"):
        parse_nature_beam_world(set_wheel)
    on_light = chain_world()
    on_light["universe"][0]["take"] = [-15, 56]
    with pytest.raises(ValueError, match=r"universe\[0\] has unknown keys: take"):
        parse_nature_beam_world(on_light)


def run_layer(
    document: dict, ticks: int = 3000, gathers: int | None = None
) -> tuple[list[dict], DetectorLawSimulation, Seen]:
    """The layer world stepped with the books balanced at every interval (`ticks` intervals; with `gathers`, until that many records have clicked, within `gathers` times the first close's interval: the horizon the window the engine writes, no number); the gather lines, the simulation, and per clicked record what the click read (a spy on the engine's `_ladder_click`: the running total before the interval, the interval's increments, the ladder of `_ladder_of`, u, the norm and the record's own wheel W)."""
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    seen: Seen = {}
    spy_on(simulation, seen)
    while (simulation.tick < ticks) if gathers is None else (len(lines_of(lines, "gather")) < gathers):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        closes = lines_of(lines, "giving")
        assert gathers is None or not closes or simulation.tick <= gathers * closes[0]["tick"]
    return lines_of(lines, "gather"), simulation, seen


RESIDUES = 128  # the planted records' wheel: every residue once


def planted_layer(order: tuple[str, ...]) -> tuple[list[dict], DetectorLawSimulation, Seen]:
    """The layer world without its emitter, RESIDUES light records planted at the emitter's Node at interval 0 with every residue of the wheel once (the given pair on the circle of 2 N, the norm the conserved form) and the ladder the sets named in `order`; run 300 intervals; the gather lines, the simulation and the spy's readings."""
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
    """Two worlds stepped together (BUILD.md section 26 item 32, FINDING C): their giving lines and the first interval at which the family of clicks' level differs between them on the emitter body's Nodes or their shell (None if it never does)."""
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
    """THE INCREMENT LADDER (ALGEBRA.md #the-ladder, the mathematician's word of 2026-09-25 on the finding of item 14; the cumulative sums withdrawn): 128 light records planted at the layer's emitter Node with every residue of the wheel 128 once and the ladder [s0, s1, s2]: every record clicks exactly once, at the detector the walk of ALGEBRA.md #the-ladder names on the click's own numbers (the running total before the interval below the threshold, the first detector of the ladder at which the interval's increments carry it across); the counts per detector under [s0, s1, s2] agree with the counts under [s2, s1, s0] within the sampling of 128 residues (the detector's share of the record's total inward flux, whatever the order, ALGEBRA.md #the-ladder: a theorem in distribution; on eight residues the exact counts are (4, 2, 2) against (2, 2, 4), the first detector of the ladder holding more of the eight thresholds, COMPUTATION for the mathematician), s0 and s2 alike within the same sampling (the placement's symmetry about the emitter's row). The emitter's own givings carry residues spread from the kept remainder (the model owner's decisions (1) and (2) of record 1962; the coupling's back-action of ALGEBRA.md #rule3 HISTORY), each clicking at the detector the walk names on its own numbers, the line's `ladder` the names and its `sunk` the pointers off the ladder; under the family of clicks (item 32, FINDING C) the two ladder orders are read in lockstep: the residues read before the clock field differs at the body agree bit for bit (all eight since item 33's count of intervals; six of eight on item 32's head, the later two differing). The loader refuses a name no set declares, a repeated name, an empty list, and a body's `coupling` by name."""
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
    gathers, simulation, seen = run_layer(layer_world(["s0", "s1", "s2"]), gathers=8)
    assert len(gathers) == 8 and len({g["u"] for g in gathers}) > 1
    names = [simulation.detector_names.index(name) for name in ("s0", "s1", "s2")]
    for gather in gathers:
        assert gather["ladder"] == ["s0", "s1", "s2"] and gather["record"] not in simulation.records
        total, increments, ladder, u, norm, wheel, pace = seen[gather["record"]]
        # the record's wheel the rule's at the body's Node with its content as the giving finds it (the own quantum and the stock 8 down to 1: 9 down to 2; ONE ORDER FOR BOTH CLICKS, ALGEBRA.md #the-primitives, item 58); the wheel divides the weak-field wall 6 den Gamma^2 (ALGEBRA.md #the-line; item 44); the norm's denominator divides the rule's read coefficient at the body's content the giving found
        assert ladder == names and (6 * EMITTER_PAIR[1] * NODE_CLOCK**2) % wheel == 0
        assert 0 <= u < wheel and pace >= 1
        assert gather["chosen"][0][0] == chosen_by_the_rule(
            simulation, total, increments, ladder, u, norm, wheel, pace
        )
        assert gather["T"] >= gather["sunk"] >= 0
    # THE REVERSED ORDER under the family of clicks (ALGEBRA.md #the-counts-line; BUILD.md section 26 item 32, FINDING C): the residues are the body's own record's, read at the first shell Node at each click (item 33), and the ladder's order is no input to them UNTIL the clock field differs at the body: the first click (at 136, at s0 under one order and at s2 under the other) writes its content at the set's first body (row 0 or row 6, no mirror images across the seam), the difference spreads by the family's own step to the body's shell (interval 216) and to the own record's remainder (240); every residue read before that agrees bit for bit (all eight here, the last read at 209: the tick counts intervals, item 33; on item 32's head six of eight, the two read after 309 differing; COMPUTATION)
    forward_givings, backward_givings, differs = lockstep_givings(
        layer_world(["s0", "s1", "s2"]), layer_world(["s2", "s1", "s0"])
    )
    assert len(forward_givings) == len(backward_givings) == 8 and differs is None
    assert sorted(line["u"] for line in forward_givings) == sorted(g["u"] for g in gathers)
    reads = [1] + [line["tick"] for line in forward_givings[:-1]]
    agreed = [
        (forward["u"] == backward["u"], read)
        for forward, backward, read in zip(forward_givings, backward_givings, reads, strict=True)
    ]
    assert all(
        same for same, _read in agreed
    )  # every residue agrees: the clock field is 0 at the bodies
    # one set on the emitter's row alone books a third of the flux: the last click at 1014 under the one border (the well two Links from the closed face; item 28), COMPUTATION
    one, _, _ = run_layer(layer_world("s1"), gathers=8)  # every giving a window and a rung (commit 7)
    assert len(one) == 8 and all(gather["chosen"][0][0] == "s1" for gather in one)
    with pytest.raises(ValueError, match="names 'screen', which no detector set declares"):
        parse_nature_beam_world(layer_world(["s0", "screen"]))
    with pytest.raises(ValueError, match="names a set twice"):
        parse_nature_beam_world(layer_world(["s0", "s0"]))
    with pytest.raises(ValueError, match="nonempty list of names"):
        parse_nature_beam_world(layer_world([]))
    coupled = layer_world("s1")
    coupled["measured"][0]["coupling"] = {"G": [1, 50], "g": [1, 1000]}
    with pytest.raises(ValueError, match=r"measured\[0\] has unknown keys: coupling"):
        parse_nature_beam_world(coupled)


def test_detector_is_one_connected_cube_of_side_three():
    """THE DETECTOR CUBE (the model owner's word of 2026-09-25, record 1899; ALGEBRA.md #the-ladder): a detector is one region, a cube of side 3 or more, its click the detector's. On the layer of 80 x 9, beyond the emitter's box, the loader refuses a cube of side 2 (the 2 x 2 box at (40, 2) naming its sides [2, 2, 1]), admits a cube of side 3 (the 3 x 3 box at (40, 2); the layer's thin z axis cuts the cube to one Node deep), admits the 3 x 3 box wrapped across the periodic seam (y = 8, 0, 1: one piece, one box), refuses a disconnected set (two bodies at (40, 2) and (43, 2), naming the two pieces) and refuses a connected set that fills no box (the 3 x 3 box less its centre, naming its Nodes); a set bound to a block admits a block of side 1 as its Nodes (SINCE COMMIT 7 a body is its own detector whatever its support, ALGEBRA.md #the-rows-against-nature, record 2109) and one of side 3; the engine reads the admitted cube as ONE detector whose Nodes are the cube's (the click line names the set and places no Node)."""
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
                "momentum_before": [0, 0, 0],
                "side": side,
                "q": 0,
                "spin": [0, 0, 0],
                "spin_before": [0, 0, 0],
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


def test_a_familys_rows_clock_enters_no_wall_of_the_loop():
    """The law's row "the recoil": no wall L and no store; a family's row's clock enters nothing of the loop and is not checked, on the given family and on any other (light or matter at [7, 1] on N = 1024, 2048 / 7 no whole number of Links): the loop builds and steps as without it."""
    families = list(
        (world := parse_nature_beam_world(stamped(emitter_world(stock=2, ticks=120)))).families
    )
    for name in ("light", "matter"):
        index = next(i for i, f in enumerate(families) if f.name == name)
        families[index] = replace(families[index], phase_per_age=(7, 1))
        simulation = DetectorLawSimulation(replace(world, families=tuple(families)))
        assert simulation.step() is None and not hasattr(simulation, "recoil_wall")
