"""The local detector law (`detector-law-v1`, docs/designs/detector_law/DESIGN.md),
the build's first gate: the loader's key and refusals, the rule's step against
the design's integers, and one chain world run headless (a lamp at one end,
a receiver at the other, the open face behind the lamp): one click per
record, the books balanced at every tick, the click's time at the front's
first rung about L / c after the birth, the click line with the stamp."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.integer import keyed_permutation
from event_universe.events.detector_law import UNIT, DetectorLawSimulation
from event_universe.events.world import DETECTOR_LAW_RULE, parse_nature_beam_world


def chain_world(train: int = 4, clock_stamp: bool = True) -> dict:
    """A chain of 80 Nodes (y and z periodic, one layer each; x open): the
    lamp's body at x = 2, a receiver body at x = 70 read as the set
    `screen`; the light family's clock the pair [77, 25] on N = 64 (3.08
    steps per interval, the period 20.78 intervals, lambda = 12 Links)."""
    return {
        "law": "beam",
        "model_id": "beam-detector-law-chain-v1",
        "shape": [80, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": 400,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": clock_stamp,
        "detector_law": True,
        "directions": [],
        "families": [{"name": "light", "quantum": 1, "phase_per_link": [77, 25]}],
        "measured": [
            {
                "position": [2, 0, 0],
                "family": "light",
                "amount": 6,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "directions": [[1, 0, 0]],
                "lamp": {
                    "rate": [1, 40],
                    "wheel": [2531, 4096],
                    "directions": [[1, 0, 0]],
                    "train": train,
                },
            },
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


def test_the_loader_admits_the_key_and_refuses_the_ray_laws_instruments():
    world = parse_nature_beam_world(chain_world())
    assert world.detector_law
    assert DETECTOR_LAW_RULE in world.hypotheses
    assert world.measured[0].lamp is not None and world.measured[0].lamp.train == 4
    with_turns = chain_world()
    with_turns["measured"][0]["lamp"]["turns"] = [3]
    with pytest.raises(ValueError, match="turns is refused under detector-law-v1"):
        parse_nature_beam_world(with_turns)
    integer_clock = chain_world()
    integer_clock["families"][0]["phase_per_link"] = 3
    with pytest.raises(ValueError, match="pair form of phase_per_link"):
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
    world = parse_nature_beam_world(chain_world())
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    for _ in range(600):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    births = [line for line in lines if line["event"] == "birth"]
    gathers = [line for line in lines if line["event"] == "gather"]
    # the lamp's stock of 6 units, one record per 40 intervals; a record that
    # clicks back at the lamp (a detector at rest) returns its unit to the stock
    assert 6 <= len(births) <= 9
    assert len(gathers) + len(simulation.records) == len(births)
    assert len(gathers) >= 4
    assert all("clock" in g and "birth" in g and "click" in g for g in gathers)
    for gather in gathers:
        assert gather["chosen"] is None or gather["chosen"][0][0] in {"screen", "face:-x", "measured:1"}
        if gather["chosen"] is not None and gather["chosen"][0][0] == "screen":
            flight = gather["click"] - gather["birth"]
            # the front's first rung about L / c = 68 / 0.577 = 118 intervals after the birth
            assert 104 <= flight <= 132, flight
    books = simulation.books()["families"]["light"]
    assert books["measured"]["measured"] + books["transit"]["escaped"] == len(gathers)


def pair_world(residue_order: str | None, residue_seed: int | None, births: int) -> dict:
    """A pair lamp on the chain of 80 (x open, the sponge faces): the lamp at x = 40 with two
    arms on +x and -x, the wheel [1, 64], one birth per interval, `births` held, a train of 2
    periods; a polariser of the counter family (a table body of two cells, section 14 item
    6) at x = 60 read as the set `right` and one at x = 20 as `left`, both at the setting 16;
    the order channel's keys as given (None: the key absent)."""
    document = chain_world()
    document["ticks"] = births + 400
    document["families"] = [
        {"name": "light", "quantum": 1, "phase_per_link": [77, 25]},
        {"name": "counter", "quantum": 1, "phase_per_link": [1, 1]},
    ]
    lamp: dict = {
        "rate": [1, 1],
        "wheel": [1, 64],
        "directions": [[1, 0, 0], [-1, 0, 0]],
        "train": 2,
        "arms": 2,
    }
    if residue_order is not None:
        lamp["residue_order"] = residue_order
    if residue_seed is not None:
        lamp["residue_seed"] = residue_seed
    document["measured"] = [
        {
            "position": [40, 0, 0],
            "family": "light",
            "amount": births,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "directions": [[1, 0, 0], [-1, 0, 0]],
            "lamp": lamp,
        },
        {
            "position": [60, 0, 0],
            "family": "counter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "table": {"light": {"phase_window": 16}},
        },
        {
            "position": [20, 0, 0],
            "family": "counter",
            "amount": 1,
            "phase": 0,
            "momentum": [0, 0, 0],
            "fixed": True,
            "table": {"light": {"phase_window": 16}},
        },
    ]
    document["detectors"] = [
        {"name": "right", "positions": [[60, 0, 0]], "threshold": 1, "reading": "sum"},
        {"name": "left", "positions": [[20, 0, 0]], "threshold": 1, "reading": "sum"},
    ]
    return document


def test_the_order_channels_keys_on_a_pair_lamp_have_no_default_and_seed_the_residues_order():
    """Line 8, the order channel's two keys (DECLARATIONS.md section 2 item 8, the model
    owner's declaration; Reviewer 3's line of 04:38Z: no default; the Boss's 04:55Z and
    05:30Z): `keyed_permutation` is the declaration's Fisher-Yates permutation driven by the
    SplitMix64 mixing hash, a bijection on Z_W at W = 16, 256 and 2048 for several keys, the
    same key the same order, two keys two orders, no key the counter's order, a count below 1
    refused; a pair lamp (two arms) under the local detector law WITHOUT `residue_order` is
    refused naming the key; under "ordinal" the births' residues are today's, u = (ordinal - 1)
    mod 64 over 64 births; under "seed" the 64 births take every residue of Z_64 once, in the
    permutation's order (the engine's `birth_orders`), two seeds two orders, the same seed the
    same order; the four joint cells' counts of the world's pair gathers (the two polarisers'
    channels, section 1 item 3) over exactly W = 64 births are the same under "ordinal" and
    "seed" (the derivation's claim; a GAMEBOARD reading, no pin); the gather line keeps `u`
    (HOST); the refusals: the
    stride r = 2 under "seed", the seed absent under "seed", the seed present under "ordinal",
    a value that is neither, either key on a lamp without arms and either key on a pair lamp
    outside the local detector law."""
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

    # no default: the key absent on a pair lamp is refused
    with pytest.raises(ValueError, match="residue_order is required on a pair lamp"):
        parse_nature_beam_world(pair_world(None, None, 64))
    ordinal_births, ordinal_gathers, ordinal = run(pair_world("ordinal", None, 64))
    assert [line["u"] for line in ordinal_births] == list(range(64))
    assert ordinal.birth_orders == {}
    seed_births, seed_gathers, seeded = run(pair_world("seed", 50 << 20, 64))
    residues = [line["u"] for line in seed_births]
    assert sorted(residues) == list(range(64)) and residues != list(range(64))
    assert residues == seeded.birth_orders[0] == keyed_permutation(64, 50 << 20)
    other_births, _, _ = run(pair_world("seed", 7, 64))
    assert [line["u"] for line in other_births] != residues
    again_births, _, _ = run(pair_world("seed", 50 << 20, 64))
    assert [line["u"] for line in again_births] == residues
    # the counts do not move with the order: one gather per pair birth (the
    # joint ladder); the four joint cells' counts the same multiset
    assert len(ordinal_gathers) == len(seed_gathers) == 64

    def counts(gathers: list[dict]) -> dict[str, int]:
        found: dict[str, int] = {}
        for gather in gathers:
            key = " ".join(f"{cell[0]}{cell[1]}" for cell in gather["chosen"])
            found[key] = found.get(key, 0) + 1
        return found

    assert counts(ordinal_gathers) == counts(seed_gathers)
    assert sum(counts(seed_gathers).values()) == 64 and len(counts(seed_gathers)) >= 2
    assert all("u" in gather and "birth" in gather and "click" in gather for gather in seed_gathers)
    assert sorted(gather["u"] for gather in seed_gathers) == list(range(64))
    # the refusals
    for order, seed, message in (
        ("seed", None, "residue_seed is required under residue_order"),
        ("ordinal", 5, "residue_seed is refused under residue_order"),
        ("counter", None, 'must be "ordinal"'),
        ("seed", -1, "residue_seed"),
        ("seed", 1 << 64, "residue_seed"),
    ):
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(pair_world(order, seed, 64))
    stride = pair_world("seed", 3, 64)
    stride["measured"][0]["lamp"]["wheel"] = [2, 64]
    with pytest.raises(ValueError, match="the stride r must be 1"):
        parse_nature_beam_world(stride)
    for key, value in (("residue_order", "ordinal"), ("residue_seed", 3)):
        single = chain_world()
        single["measured"][0]["lamp"][key] = value
        with pytest.raises(ValueError, match="not admitted on a lamp without arms"):
            parse_nature_beam_world(single)
    outside = pair_world("ordinal", None, 64)
    outside["detector_law"] = False
    outside["clock_stamp"] = False
    for entry in outside["measured"]:
        entry["lamp"] = entry.get("lamp") and {k: v for k, v in entry["lamp"].items() if k != "train"}
        if not entry["lamp"]:
            del entry["lamp"]
    with pytest.raises(ValueError, match="outside the local detector law"):
        parse_nature_beam_world(outside)


def test_the_emitters_own_take_is_the_rule_from_the_first_interval_after_the_train():
    """Item 10 THE RULE (DECLARATIONS.md section 10 item 10; the model owner's words of 06:42Z,
    record 1694, and 07:27Z, record 1711: the timing integer withdrawn): from the first interval
    after its train every emitter's own Nodes take its record's remnant in the record's kind's
    pair, booked onto no pointer and not into `absorbed`; no key and no load-time integer. On
    the chain world: the lamp's Node holds the record's row at 0 from age train + 1 on (the
    drive's last write at age train - 1, its value standing at age train; the take acts in the
    interval that starts at age train, the first after the train) and `emitter_taking` is read
    on the records reading; a
    `remnant_take` key written into a world is refused as unknown; a detector-law world with a
    set and no lamp declares the world key `wheel` (refused absent, no implicit default); a
    massive kind's `take` is refused on light's kind; the ledger carries the HOST row
    `taken_by_emitter`, 0 on the chain world whose record ends at the screen, the books
    balanced. THE GUARD (Reviewer 3, 07:43Z): an absorbing Node without a cell refuses the
    interval naming the Node, never booking to the last cell by the list's wrap."""
    world = parse_nature_beam_world(chain_world())
    simulation = DetectorLawSimulation(world)
    train = None
    for _ in range(450):
        simulation.step()
        live = simulation.records.get(1)
        if live is None:
            continue
        train = live.train
        at_lamp = int(live.now[2, 0, 0])
        if live.age <= train:
            assert not live.emitter_took
        else:
            # the take acts in the interval that starts at age train, the
            # first after the train: the row is 0 from age train + 1 on
            assert at_lamp == 0 and live.emitter_took
    assert train is not None
    readings = dict(simulation.snapshot_stream())
    assert all("emitter_taking" in record for record in readings.get("records", []))
    books = simulation.books()
    assert books["balanced"]
    light = books["families"]["light"]["transit"]
    assert light["taken_by_emitter"] == 0 and light["absorbed"] >= 1
    keyed = chain_world()
    keyed["measured"][0]["lamp"]["remnant_take"] = 4
    with pytest.raises(ValueError, match="remnant_take"):
        parse_nature_beam_world(keyed)
    no_wheel = chain_world()
    no_wheel["measured"][0] = {
        "position": [2, 0, 0],
        "family": "light",
        "amount": 1,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "directions": [[1, 0, 0]],
    }
    with pytest.raises(ValueError, match="declares the world key `wheel`"):
        parse_nature_beam_world(no_wheel)
    no_wheel["wheel"] = 64
    parse_nature_beam_world(no_wheel)
    on_light = chain_world()
    on_light["massive_record"] = True
    on_light["families"][0]["take"] = [-15, 56]
    with pytest.raises(ValueError, match="admitted on a massive kind alone"):
        parse_nature_beam_world(on_light)
    # the guard: an absorbing Node whose cell is the sentinel refuses the interval
    guarded = DetectorLawSimulation(parse_nature_beam_world(chain_world()))
    for _ in range(3):
        guarded.step()
    guarded.cell_index[70, 0, 0] = -1
    with pytest.raises(RuntimeError, match=r"absorbing Node without a cell .*\(70, 0, 0\)"):
        for _ in range(200):
            guarded.step()
