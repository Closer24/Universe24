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

from event_universe.core.integer import keyed_permutation
from event_universe.events.detector_law import UNIT, DetectorLawSimulation
from event_universe.events.world import DETECTOR_LAW_RULE, parse_nature_beam_world
from tests.test_emitter import massive_generator

EMITTER_KIND = [7, 8]  # the emitter body's kind (omega_0 = 0.505)
EMITTER_PAIR = [8, 7]  # its one-cell well, bound on a chain (2 cos omega_b = 1.90, omega_b = 0.32)


def emitter_body(
    position: list[int],
    stock: int,
    wheel: tuple[int, int],
    order: str = "ordinal",
    seed: int | None = None,
    receiver: object = None,
    side: int = 1,
    family: str = "light",
) -> dict:
    """An emitter body of the matter kind EMITTER_KIND (the well pair EMITTER_PAIR, seeded on
    its mode at 100 by the generator), its stock `stock`, its `emitter` the family given on
    the wheel with its residue order and, with `receiver`, the born records' ladder by name.
    The cadence (COMPUTATION, BUILD.md section 26): the u-th residue clicks about (2 u + 1) /
    (2 W) x P intervals after its excitation, P the mode's period (20 on this well; ALGEBRA.md
    9.17 (5) item 1 on the flux norm of 9.19 (3)); a well too
    deep for its board is a runaway and refused at the margin rule."""
    emitter: dict = {"family": family, "wheel": list(wheel), "residue_order": order}
    if seed is not None:
        emitter["residue_seed"] = seed
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
    wheel: tuple[int, int] = (1, 6),
    order: str = "ordinal",
    seed: int | None = None,
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
    20.78 intervals, lambda = 12 Links); the world's wheel 64 the sets' rung
    (larger than the emitter's). With `faces` "open" the face receiver
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
        "wheel": 64,
        "directions": [],
        "families": [
            {"name": "light", "quantum": 1, "phase_per_link": [77, 25]},
            {"name": "matter", "quantum": 1, "pair": list(EMITTER_KIND)},
        ],
        "measured": [
            emitter_body([2, 0, 0], stock, wheel, order, seed, receiver),
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
    assert block is not None and block.emitter is not None and block.emitter.wheel == (1, 6)
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
    # the emitter's stock of 6 excitations, each clicking at its own rung
    assert len(births) == 6 and [line["u"] for line in births] == list(range(6))
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


def test_the_order_channels_keys_on_the_emitter_body_seed_the_residues_order():
    """Line 8, the order channel's two keys (DECLARATIONS.md section 2 item 8, the model
    owner's declaration; Reviewer 3's line of 04:38Z: no default; the Boss's 04:55Z and
    05:30Z), on the EMITTER BODY since ALGEBRA.md 9.17 (the excitations' residues):
    `keyed_permutation` is the declaration's Fisher-Yates permutation driven by the SplitMix64
    mixing hash, a bijection on Z_W at W = 16, 256 and 2048 for several keys, the same key the
    same order, two keys two orders, no key the counter's order, a count below 1 refused; under
    "ordinal" the births' residues are the counter's, u = (ordinal - 1) mod W; under "seed" the
    W births take every residue of Z_W once, in the permutation's order (the engine's
    `birth_orders`), two seeds two orders, the same seed the same order; the gather line keeps
    `u` (HOST); the refusals: the step above 1 under "seed", the seed absent under "seed", the
    seed present under "ordinal", a value that is neither."""
    for count in (16, 256, 2048):
        for key in (0, 1, 50 << 20, (1 << 64) - 1):
            order = keyed_permutation(count, key)
            assert sorted(order) == list(range(count))
            assert order == keyed_permutation(count, key)
        assert keyed_permutation(count, 1) != keyed_permutation(count, 2)
        assert keyed_permutation(count, 7) != list(range(count))
    with pytest.raises(ValueError, match="positive count"):
        keyed_permutation(0, 1)

    def run(document: dict) -> tuple[list[dict], list[dict], DetectorLawSimulation]:
        world = parse_nature_beam_world(document)
        lines: list[dict] = []
        simulation = DetectorLawSimulation(world, observer=lines.append)
        for _ in range(document["ticks"]):
            simulation.step()
        births = [line for line in lines if line["event"] == "birth"]
        gathers = [line for line in lines if line["event"] == "gather"]
        return births, gathers, simulation

    ordinal_births, ordinal_gathers, ordinal = run(chain_world(8, (1, 8)))
    assert [line["u"] for line in ordinal_births] == list(range(8))
    assert ordinal.birth_orders == {}
    seed_births, seed_gathers, seeded = run(chain_world(8, (1, 8), "seed", 50 << 20))
    residues = [line["u"] for line in seed_births]
    assert sorted(residues) == list(range(8)) and residues != list(range(8))
    assert residues == seeded.birth_orders[0] == keyed_permutation(8, 50 << 20)
    other_births, _, _ = run(chain_world(8, (1, 8), "seed", 7))
    assert [line["u"] for line in other_births] != residues
    again_births, _, _ = run(chain_world(8, (1, 8), "seed", 50 << 20))
    assert [line["u"] for line in again_births] == residues
    assert all("u" in gather and "birth" in gather and "click" in gather for gather in seed_gathers)
    for order, seed, message in (
        ("seed", None, "residue_seed is required under residue_order"),
        ("ordinal", 5, "residue_seed is refused under residue_order"),
        ("counter", None, 'must be "ordinal"'),
        ("seed", -1, "residue_seed"),
        ("seed", 1 << 64, "residue_seed"),
    ):
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(chain_world(8, (1, 8), order, seed, on_mode=False))
    with pytest.raises(ValueError, match="the step must be 1"):
        parse_nature_beam_world(chain_world(8, (3, 8), "seed", 3, on_mode=False))


def test_the_emitters_cells_are_cells_like_every_other_and_take_nothing_of_its_record():
    """ALGEBRA.md 9.17 (the Boss's line on the knot): the emitter's own cells are cells like
    every other after the birth: no grace, no exemption, no own take. On the chain world
    the born record's row at the emitter's cell evolves under the rule (nonzero at ages after
    the birth, never held at 0), no Node absorbs (the take retired, 9.19 (3)), the ledger's
    row `taken_by_emitter` stays 0 (kept for the readers' form) and the records reading
    carries no `emitter_taking`; a `remnant_take` key on the emitter is refused as unknown;
    a detector-law world with a detector set declares the world key `wheel` (refused
    absent, no implicit default); a massive kind's `take` is refused on light's kind; the
    books balanced."""
    world = parse_nature_beam_world(chain_world(1, (1, 1)))
    simulation = DetectorLawSimulation(world)
    assert not simulation.absorbing.any()
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
    no_wheel = chain_world(on_mode=False)
    del no_wheel["measured"][0]
    del no_wheel["wheel"]
    with pytest.raises(ValueError, match="declares the world key `wheel`"):
        parse_nature_beam_world(no_wheel)
    no_wheel["wheel"] = 64
    parse_nature_beam_world(no_wheel)
    on_light = chain_world(on_mode=False)
    on_light["families"][0]["take"] = [-15, 56]
    with pytest.raises(ValueError, match="admitted on a massive kind alone"):
        parse_nature_beam_world(on_light)


def layer_world(receiver: object = None) -> dict:
    """A layer of 24 x 7 x 1 (x closed at both ends, mirrors; y and z
    periodic): the emitter body at [2, 3, 0] (the matter kind on its mode,
    the stock 8 on the wheel [1, 8]), three receiver bodies at x = 18 on the
    rows y = 2, 3, 4 read as the sets s0, s1, s2 (one Node each, the
    screen). With `receiver`, the emitter's records' ladder is the named
    sets in the named order; without it, every declared set in the
    declared order (ALGEBRA.md 9.19 (3) (b))."""
    measured = [emitter_body([2, 3, 0], 8, (1, 8), receiver=receiver)]
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


def run_layer(
    document: dict, ticks: int = 900
) -> tuple[list[dict], DetectorLawSimulation, dict[int, tuple[list[int], list[int], int, int]]]:
    """The layer world stepped with the books balanced at every interval; the gather lines,
    the simulation, and per clicked record the pointers and the ladder as the click read
    them (a spy on the engine's `_ladder_click`: the pointers before the call, the ladder
    of `_ladder_of`, u and the norm)."""
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    seen: dict[int, tuple[list[int], list[int], int, int]] = {}
    original = simulation._ladder_click

    def spy(live):
        pointers = list(live.pointers)
        original(live)
        if live.clicked and live.identity not in seen:
            seen[live.identity] = (pointers, simulation._ladder_of(live), live.u, live.norm)

    simulation._ladder_click = spy  # type: ignore[method-assign]
    for _ in range(ticks):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    return [line for line in lines if line["event"] == "gather"], simulation, seen


def chosen_by_the_rule(
    simulation: DetectorLawSimulation, pointers: list[int], ladder: list[int], u: int, norm: int
) -> str:
    """The cumulative rule of ALGEBRA.md 9.19 (3) (b) on the click's own numbers: the first
    cell k of the ladder with 2 W_k L_k >= (2 u + 1) T, L_k the ladder's sum up to k."""
    total = 0
    for cell in ladder:
        total += pointers[cell]
        if 2 * simulation.cell_wheel.get(cell, simulation.wheel) * total >= (2 * u + 1) * norm:
            return simulation.cell_set[cell]
    raise AssertionError("no rung crossed")


def test_the_emitters_ladder_by_name_orders_the_named_sets():
    """(f) The emitter's records' ladder by name (DECLARATIONS.md section 13 item 7; the
    emitter's `receiver` since ALGEBRA.md 9.17) under the cumulative ladder of 9.19 (3)
    (b) AS WRITTEN: with `receiver` [s0, s1, s2] every click of the layer world's emitter
    is at one of the three sets, the cell of u the FIRST cell k of the ladder, in the named
    order, at which 2 W L_k >= (2 u + 1) T on the click's own pointers (the spy's reading of
    the engine's numbers), the line's `ladder` the names and its `sunk` the pointers off the
    ladder (the emitter's own cell books the return through the mirror); the record deleted
    at its line; the books balanced. THE FINDING FOR THE MATHEMATICIAN (the model owner's
    method: the algebra checked with values on the board): the three Nodes at x = 18 receive
    the +x half at the same intervals, so the LAST sum L_3 is the first to reach the rung at
    every u, and the first k at which L_k >= (2 u + 1) T / (2 W) at that interval is k = 3:
    ALL EIGHT clicks are at s2 under [s0, s1, s2] and all eight at s0 under [s2, s1, s0],
    whatever the residue, no distribution over the cells (the same for a screen of any
    number of cells and for the polariser's two cells at one Node). 9.22 (3) (b)'s
    derivation, "for offers in fixed proportions the crossing cell is the final ladder's",
    holds only if the click's INTERVAL is read on the ladder's total against T and the
    CELL on the ladder's proportions at that interval (main's `cell_of` with the total the
    ladder's own sum), two comparisons, not one; the mathematician's word is owed and the
    engine carries the rule as written until then (BUILD.md section 26 item 14). With "s1"
    alone every click is at s1; without the key the ladder is every declared set in the
    declared order (the same clicks as [s0, s1, s2], no `ladder` and no `sunk` on the
    line). The loader refuses a name no set declares, a repeated name and an empty list."""
    gathers, simulation, seen = run_layer(layer_world(["s0", "s1", "s2"]))
    assert len(gathers) == 8
    assert sorted(gather["u"] for gather in gathers) == list(range(8))
    names = [simulation.cell_names.index(name) for name in ("s0", "s1", "s2")]
    for gather in gathers:
        assert gather["ladder"] == ["s0", "s1", "s2"] and gather["record"] not in simulation.records
        assert gather["chosen"] is not None and gather["chosen"][0][0] in {"s0", "s1", "s2"}
        pointers, ladder, u, norm = seen[gather["record"]]
        assert ladder == names and u == gather["u"]
        assert gather["chosen"][0][0] == chosen_by_the_rule(simulation, pointers, ladder, u, norm)
        assert gather["sunk"] == sum(p for cell, p in enumerate(pointers) if cell not in names)
        assert gather["T"] == sum(pointers)
        # the finding: the three Nodes book together, the last sum crosses first
        assert all(pointers[cell] > 0 for cell in names)
    forward = {gather["u"]: gather["chosen"][0][0] for gather in gathers}
    assert forward == {u: "s2" for u in range(8)}, forward
    backward, _, _ = run_layer(layer_world(["s2", "s1", "s0"]))
    assert {g["u"]: g["chosen"][0][0] for g in backward} == {u: "s0" for u in range(8)}
    one, _, _ = run_layer(layer_world("s1"))
    assert len(one) == 8 and all(gather["chosen"][0][0] == "s1" for gather in one)
    control, _, _ = run_layer(layer_world())
    assert all("ladder" not in gather and "sunk" not in gather for gather in control)
    assert {g["u"]: g["chosen"][0][0] for g in control} == forward
    with pytest.raises(ValueError, match="names 'screen', which no detector set declares"):
        parse_nature_beam_world(layer_world(["s0", "screen"]))
    with pytest.raises(ValueError, match="names a set twice"):
        parse_nature_beam_world(layer_world(["s0", "s0"]))
    with pytest.raises(ValueError, match="nonempty list of names"):
        parse_nature_beam_world(layer_world([]))
