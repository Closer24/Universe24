"""The emitter as a clicking body (ALGEBRA.md 9.17 (4), the mathematician's integers of
2026-09-24; LAB_TOOLS.md A.1; the model owner's word of 22:30Z, "in principle we cannot do
any operation on the cells except to produce a click"): a body of a massive kind with its
seed and a stock `amount` = M holds its excited records in turn (the seed at both levels,
content one quantum, the residue from the body's wheel [step, W] in its residue order);
excited record k clicks at its own rung on its own cells (E its own motion booked through
its cells, D the rung 2 T u_k + T <= 2 W C with T its norm, the seed's squares over its
cells); at that click X ends it and E^T births the photon, written ONCE at both levels
(now = A C[phase(0)], before = A C[phase(-1)] on the body's cells, A the lamp's unit) with
the norm T the motion the write inserts and the excitation's residue, and, while the stock
lasts, excited record k + 1. No rate, no train, no drive, no source term, no grace, no own
take. BUILD.md section 26.

SINCE THE FLUX READING (ALGEBRA.md 9.19 (3); BUILD.md section 26 items 13 and 14): the
excited record's offer is the one-way flux into the body's centre cell, its norm T the
generator's integer `norm` (that flux over one period of the mode advanced alone); the born
record's norm its conserved form I; every set books the one-way flux into its cells and the
click is on the cumulative ladder, the record deleted whole at it. The unit world's faces
are CLOSED (mirrors): an open face two Links behind a body is the face receiver, last on
every ladder, and the half that leaves through it clicks there before anything reaches a
screen (test_detector_law.py reads that).

(a) M excitations give M births at the rungs: each birth at the first interval where the
    excited record's booked flux crosses T (2 u + 1) / (2 W) (tracked interval by
    interval), the residues in the wheel's order ("ordinal" the counter, "seed" the keyed
    permutation), the quanta conserved (the stock spent one per birth, the books balanced
    at every interval), the excited record ended at its click and the next one seeded with
    the next residue, none after the stock; the birth line's keys.
(b) The born values: at the birth the record's `now` and `before` equal the cosine table at
    phase(0) and phase(-1) of the born clock on every cell of the body and 0 elsewhere; its
    norm is its conserved form; nothing drives it afterwards (its train 0, no grace, no
    take); nothing reaches Manhattan distance m before age m; the born records reach the
    receiver by name and click.
(c) The loader's refusals, each naming its key.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import input_stamp, parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]


def massive_generator():
    path = ROOT / "examples/events/massive_record/make_worlds.py"
    spec = importlib.util.spec_from_file_location("massive_record_make_worlds", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def emitter_world(
    stock: int = 4,
    ticks: int = 1200,
    on_mode: bool = True,
) -> dict:
    """The emitter's unit world: a chain of 80 (x closed, mirrors), the emitter a body of the
    matter kind [800, 809] with the well pair [800, 801] (W = 2403 remainder values, ALGEBRA.md
    9.22 (4)) over the train's 32 cells at [5, 37), seeded on its bound mode at the amplitude
    2^20 (the generator's `seed_on_the_mode`, the body's conditions of the load check; at 100
    the born light's back-action swamps the excited record, ALGEBRA.md 9.17 (7) (c)), its
    stock `amount` = `stock`, its `emitter` the light family on the born clock [512, 1] of
    N = 1024 with its `train` of 8 periods along +x (THE BORN TRAIN, ALGEBRA.md 9.17 (6a);
    BUILD.md section 26 item 27) and its ladder the set `screen` (no coupling: the click alone,
    the model owner's decision (2) of record 1962); the receiver the cube of side 3 of
    light bodies at [70, 72] read as `screen` (record 1899), 33 Links ahead of the train's
    head; no wheel anywhere."""
    # the cube helper of the detector-law suite (imported here: that suite imports
    # `massive_generator` from this one)
    from tests.test_detector_law import receiver_cube

    emitter: dict = {
        "family": "light",
        "receiver": ["screen"],
        "train": {"direction": [1, 0, 0], "periods": 8},
    }
    document = {
        "law": "beam",
        "model_id": "beam-detector-law-emitter-unit-v1",
        "shape": [80, 1, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": 1073741824,
        "N": 1024,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        "amplitude_bound": 1 << 32,
        "directions": [],
        "families": [
            {"name": "light", "quantum": 1, "phase_per_link": [512, 1]},
            {"name": "matter", "quantum": 1, "pair": [800, 809]},
        ],
        "measured": [
            {
                "position": [5, 0, 0],
                "family": "matter",
                "amount": stock,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "extents": [32, 1, 1],
                "pair": [800, 801],
                "seed": 1 << 20,
                "margin": "control",
                "emitter": emitter,
            },
        ],
        "detectors": [],
    }
    receiver_cube(document, "screen", [70, 0, 0])
    if on_mode:
        massive_generator().seed_on_the_mode(document)
    return document


def run(document: dict) -> tuple[list[dict], DetectorLawSimulation, list[dict]]:
    """The world stepped over its ticks, the books balanced at every interval; the lines,
    the simulation, and per interval the emitter's excited record's state before the
    interval's emission (its residue, norm and booked offer after the interval's advance)."""
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    block = simulation.block_by_number[0]
    trace: list[dict] = []
    for _ in range(document["ticks"]):
        before = None if block.own is None else (block.own.identity, block.own.u, block.own.norm)
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        trace.append(
            {
                "tick": simulation.tick,
                "excited_before": before,
                "excited_after": None if block.own is None else block.own.identity,
                "offer": block.offer,
            }
        )
    return lines, simulation, trace


def test_m_excitations_give_m_births_at_their_rungs_and_the_quanta_are_conserved():
    document = emitter_world(stock=4)
    lines, simulation, trace = run(document)
    births = [line for line in lines if line["event"] == "birth"]
    assert len(births) == 4
    # the residue from the law (ALGEBRA.md 9.22 (4)): u the clicking record's
    # remainder at the birth cell in the remainder's step, W = 3 den / gcd(num,
    # 3 den) = 2403 on [800, 801]; read on the board below
    assert all(line["W"] == 2403 and 0 <= line["u"] < 2403 for line in births)
    assert [line["excitation"] for line in births] == [1, 2, 3, 4]
    ticks = [line["tick"] for line in births]
    # the excited record's residue is read after its first advance (9.19 (4e);
    # 0 on the seed itself), its rung (2 u + 1) T / (2 W) from that interval
    assert ticks == sorted(ticks) and ticks[0] >= 2 and ticks[-1] < document["ticks"]
    norm = births[0]["excitation_norm"]
    assert norm > 0 and all(line["excitation_norm"] == norm for line in births)
    # the norm T: one period's action P e_c, the share of the record's
    # conserved form at the body's centre cell summed over one period of its
    # mode advanced alone (ALGEBRA.md 9.17 (7) (e) and (f), 9.19 (3)), the
    # generator's integers `period` and `norm`, read on the board here: the
    # body alone (the same world, its emitter and its screen removed), the
    # share at the Node x = 21 (the corner 5 plus 32 // 2) from the two
    # levels after each interval's step, summed over `period` intervals, bit
    # for bit; the period the nearest integer to 2 pi / omega_b (63 on this
    # well); the share the mode's own tick, constant within the seed's
    # rounding wobble (below three parts in a thousand at 2^20 on the 32-cell well), and the whole
    # board's shares sum to the conserved form
    emitter = document["measured"][0]["emitter"]
    assert emitter["norm"] == norm and emitter["period"] > 0
    alone = json.loads(json.dumps(document))
    del alone["measured"][0]["emitter"]
    alone["measured"] = alone["measured"][:1]
    alone["detectors"] = []
    alone["input"] = input_stamp(alone)  # the stamp of the body alone (its born pair gone)
    solitary = DetectorLawSimulation(parse_nature_beam_world(alone))
    body = solitary.block_by_number[0]
    centre = np.zeros(solitary.shape, dtype=bool)
    centre[21, 0, 0] = True
    assert np.array_equal(solitary.centre_mask(body), centre)
    action = 0
    shares = []
    for _ in range(emitter["period"]):
        solitary.step()
        assert body.own is not None
        share = solitary.form_share(body.own, centre)
        shares.append(share)
        action += share
        whole = solitary.form_share(body.own, np.ones(solitary.shape, dtype=bool))
        assert whole == solitary.conserved_form(body.own)
    assert action == norm
    # the share's wobble from the seed's rounding: 2.1 parts in a thousand on the
    # 32-cell well at 2^20 (COMPUTATION; one part in a thousand on the side-12 well)
    assert 1000 * (max(shares) - min(shares)) < 3 * (action // emitter["period"])
    by_tick = {entry["tick"]: entry for entry in trace}
    # THE CADENCE UNDER THE CLICK RULE (9.17 (7) (b) and (f)): with the share
    # constant, C = (t - t_0) e_c and T = P e_c, so the residue u clicks
    # (2 u + 1) P / (2 W) intervals after its read (a uniform waiting time in
    # [0, P) set by the residue, one birth per half period on average),
    # within two intervals here (the wobble, the read's own interval)
    read_at = 2
    for line in births:
        excited_u = by_tick[line["tick"]]["excited_before"][1]
        waited = line["tick"] - read_at
        expected = (2 * excited_u + 1) * emitter["period"] / (2 * 2403)
        assert abs(waited - expected) <= 2, (line["tick"], excited_u, waited, expected)
        read_at = line["tick"] + 1
    for line in births:
        # the excited record's own rung on its residue read after its first
        # advance (the trace reads u before the interval: 0 in the interval
        # of the read itself, the rung then T / (2 W), a weaker bound)
        excited_u = by_tick[line["tick"]]["excited_before"][1]
        threshold = norm * (2 * excited_u + 1)  # 2 T u + T <= 2 W C
        assert 2 * 2403 * line["excitation_offer"] >= threshold
        # the interval before the click: the offer below the rung (a birth at
        # the first interval has no interval before it)
        previous = by_tick.get(line["tick"] - 1)
        assert (
            previous is None
            or 2 * 2403 * previous["offer"] < threshold
            or previous["excited_before"] is None
        )
        # the excited record ended at its click, the next one seeded
        entry = by_tick[line["tick"]]
        assert entry["excited_before"] is not None
        if line["excitation"] < 4:
            assert (
                entry["excited_after"] is not None
                and entry["excited_after"] != entry["excited_before"][0]
            )
        else:
            assert entry["excited_after"] is None
    assert simulation.block_by_number[0].own is None
    assert simulation.held[0] == [0, 0]
    books = simulation.books()["families"]
    assert books["matter"]["measured"]["spent"] == 4 and books["light"]["transit"]["released"] == 4
    assert not simulation.records
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) == 4 and all(gather["chosen"] == [["screen", 0, "0"]] for gather in gathers)
    assert sorted(gather["u"] for gather in gathers) == sorted(line["u"] for line in births)
    for gather in gathers:
        assert gather["content"] == 1 and gather["click_at"] == "rung"
        # the train's head over the 33 Links from the body's head at 36 to the
        # screen at 70 at v_g = 0.447 (about 74 intervals), the tapers' precursor
        # a little before it; the rung crossed on the passage
        assert gather["click"] >= gather["birth"] + 50
        assert gather["click"] == gather["tick"] and gather["record"] not in simulation.records
    # THE RESIDUES SPREAD FROM THE KEPT REMAINDER (the model owner's decisions
    # (1) and (2) of record 1962; ALGEBRA.md 9.34 (A) and (B)): the remainder
    # at the centre cell moves between births with no coupling and no draw
    # (the coupling's back-action of 9.19 (4e) HISTORY)
    assert len({line["u"] for line in births}) > 1
    # a smaller stock: as many births
    lines, _, _ = run(emitter_world(stock=2))
    assert len([line for line in lines if line["event"] == "birth"]) == 2


def test_the_remainder_is_the_cells_kept_through_the_click_and_the_reseed():
    """THE REMAINDER IS THE CELL'S (the model owner's decision (1) of record 1962; ALGEBRA.md
    9.34 (A), 9.35 (7); BUILD.md section 26 item 29): at every birth of the stock the fresh
    excited record's division remainder is the ended record's at every Node of the board,
    bit for bit, nonzero on the body's Nodes (the remainder after the
    advances since the load); the load's seed alone starts at 0 (the file's integers). The
    stock's four residues are not all equal (they spread from the kept remainder). The edge
    case: the last birth leaves no fresh record (the stock spent), so three reseeds keep it."""
    document = emitter_world(stock=4)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    block = simulation.block_by_number[0]
    assert block.own is not None and not np.any(block.own.remainder)
    kept: list[int] = []
    original = simulation._emit

    def spy(target):
        ended = target.own
        assert ended is not None
        remainder = ended.remainder.copy()
        original(target)
        if target.own is not None:
            assert np.array_equal(target.own.remainder, remainder)
            assert np.any(target.own.remainder[target.mask])
            kept.append(simulation.tick)

    simulation._emit = spy  # type: ignore[method-assign]
    for _ in range(document["ticks"]):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
    births = [line for line in lines if line["event"] == "birth"]
    assert len(births) == 4 and len(kept) == 3 and block.own is None
    assert len({line["u"] for line in births}) > 1


def test_the_born_record_is_written_once_and_the_law_advances_it():
    document = emitter_world(stock=1, ticks=400)
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    block = simulation.block_by_number[0]
    born = None
    extent: list[tuple[int, int]] = []
    while simulation.tick < 400:
        simulation.step()
        assert simulation.books()["balanced"]
        light = [live for live in simulation.records.values() if live.family == 0]
        if light and born is None:
            (born,) = light
            birth = next(line for line in lines if line["event"] == "birth")
            assert birth["tick"] == simulation.tick and born.age == 0 and born.train == 0
            # THE BORN TRAIN (ALGEBRA.md 9.17 (6a)): the world's profile `born`
            # {now, before, norm}, the generator's integers, written on the
            # body's 32 cells in the box's x-major order and zero elsewhere; the
            # character cos(pi i / 2) under the tapers of 8 at both ends: the
            # levels 1, 0, -1, 0 times 2^16 in the flat middle
            train = document["measured"][0]["emitter"]["born"]
            assert len(train["now"]) == len(train["before"]) == 32
            assert train["now"][8:16] == [65536, 0, -65536, 0, 65536, 0, -65536, 0]
            assert 0 < train["now"][0] < 1000 and train["now"][31] == 0
            assert list(born.now[5:37, 0, 0]) == train["now"]
            assert list(born.before[5:37, 0, 0]) == train["before"]
            assert not np.any(born.now[~block.mask]) and not np.any(born.before[~block.mask])
            # the norm T the written one, the record's conserved form on the
            # vacuum (ALGEBRA.md 9.17 (6a), 9.19 (3)): light's pair is the vacuum's
            # at the body's cells, so the board reads the same integer at the birth
            assert born.norm == birth["norm"] == train["norm"] == simulation.conserved_form(born) > 0
            assert birth["cells"] == 32 and birth["excitation"] == 1 and birth["train"] == 0
            assert born.u == birth["u"] and born.wheel == birth["W"] == 2403
            assert born.content == 1 and born.emitter == 0
            assert born.ladder == [simulation.cell_names.index("screen")]
        if born is not None and born.identity in simulation.records:
            nonzero = np.nonzero(born.now)[0]
            if len(nonzero):
                extent.append((born.age, int(nonzero.min()), int(nonzero.max())))
    assert born is not None and extent
    for age, low, high in extent:
        # nothing reaches Manhattan distance m before age m (the causal bound)
        assert low >= 5 - age and high <= 36 + age
    # no drive and no take after the write (the take retired, ALGEBRA.md
    # 9.19 (3)): the ledger's retired row stays 0
    assert simulation.books()["families"]["light"]["transit"]["taken_by_emitter"] == 0


def test_the_loaders_refusals_name_their_keys():
    def refused(mutate, message: str, on_mode: bool = False) -> None:
        document = emitter_world(stock=2, on_mode=on_mode)
        mutate(document)
        # the stamp of the changed integers (record 1886): the named refusal,
        # not the hash's, is the one read here
        document["input"] = input_stamp(document)
        with pytest.raises(ValueError, match=message):
            DetectorLawSimulation(parse_nature_beam_world(document))

    def emitter(key, value):
        def mutate(document):
            document["measured"][0]["emitter"][key] = value

        return mutate

    refused(emitter("family", "matter"), "the body's own family")
    refused(emitter("family", "nobody"), "unknown family")
    # the retired keys of the declared residue (ALGEBRA.md 9.22 (4)), each
    # refused by name with its successor
    refused(emitter("wheel", [1, 4]), "emitter.wheel is refused")
    refused(emitter("residue_order", "ordinal"), "emitter.residue_order is refused")
    refused(emitter("residue_seed", 3), "emitter.residue_seed is refused")
    refused(emitter("rate", [1, 1]), "unknown keys|rate")

    # the coupling of MASSIVE_RECORD.md section 7 retired: refused by name with its
    # successor (the click alone, the model owner's decision (2) of record 1962)
    def coupled(document):
        document["measured"][0]["coupling"] = {"G": [1, 50], "g": [1, 1000]}

    refused(coupled, "coupling is refused")

    # the richness of the birth cell (9.22 (4)): a pair with fewer than 500
    # remainder values refuses the emitter naming the count
    def poor_well(document):
        document["measured"][0]["pair"] = [800, 800]

    refused(poor_well, "gives 3 remainder values")

    def on_light(document):
        document["measured"][0]["family"] = "light"
        document["measured"][0]["pair"] = [1, 2]
        document["measured"][0]["emitter"]["family"] = "matter"
        del document["measured"][0]["seed"]

    refused(on_light, "light's kind")

    def silent(document):
        document["measured"][0]["seed"] = 0

    refused(silent, "needs the body's `seed`")

    def no_stock(document):
        document["measured"][0]["amount"] = 0

    refused(no_stock, "amount")

    # the generator's integers (ALGEBRA.md 9.17 (5) item 1): a norm the
    # emitter does not declare refuses the simulation at its first
    # excitation; a `born` profile of the wrong count, or one that writes no
    # motion, refuses the loader (9.17 (5) item 3)
    def no_norm(document):
        document["measured"][0]["emitter"]["period"] = 70
        document["measured"][0]["emitter"]["norm"] = 1000
        del document["measured"][0]["emitter"]["norm"]

    refused(no_norm, "declares no `norm`", on_mode=True)
    # the mathematician's gate item 8: a body that births declares its seed
    # as its composed mode's profile; a flat scalar seed is refused
    refused(lambda document: None, "seed. as its composed mode's profile")
    # THE BORN TRAIN'S REFUSALS (ALGEBRA.md 9.17 (6a)): the two-integer pair
    # (the one-cell birth, a flat pulse) by its reason; a profile of the wrong
    # count, one that writes no motion, one whose flux runs against the
    # declared way, one whose norm is not the vacuum's form; `born` without
    # `train`; the train's direction, periods, wavelength and extent
    refused(emitter("born", [5, -5]), "a flat pulse of the body's length is broadband")
    refused(emitter("born", {"now": [1, 2], "before": [3, 4], "norm": 1}), "must be 32 integers")
    refused(emitter("born", {"now": [0] * 32, "before": [0] * 32, "norm": 1}), "writes no motion")

    def against(document):
        train = document["measured"][0]["emitter"]["born"]
        document["measured"][0]["emitter"]["born"] = {
            "now": train["now"],
            "before": train["now"],
            "norm": train["norm"],
        }

    refused(against, "not positive: the record does not travel as declared", on_mode=True)

    def wrong_norm(document):
        document["measured"][0]["emitter"]["born"]["norm"] += 1

    refused(wrong_norm, "is not the born record's conserved form on the vacuum", on_mode=True)

    def trainless(document):
        del document["measured"][0]["emitter"]["train"]

    refused(trainless, "needs the emitter's `train`", on_mode=True)
    refused(
        lambda document: document["measured"][0]["emitter"].pop("born"),
        "declares no born train",
        on_mode=True,
    )
    refused(emitter("train", {"direction": [1, 1, 0], "periods": 8}), "one signed unit axis vector")
    refused(emitter("train", {"direction": [1, 0, 0], "periods": 3}), "periods")
    refused(emitter("train", {"direction": [0, 1, 0], "periods": 8}), "is not the train's length")

    def odd_wavelength(document):
        document["families"][0]["phase_per_link"] = [500, 1]

    refused(odd_wavelength, "no whole number of Links")

    for key, value, message in (
        ("emits", "light", "emits is refused"),
        ("own_grace", 3, "own_grace is refused"),
        ("absorbing", True, "absorbing is refused"),
        ("take", [-15, 56], "take is refused"),
        ("wheel", 64, "wheel is refused"),
    ):

        def beside(document, key=key, value=value):
            document["measured"][0][key] = value

        refused(beside, message)

    def two_ladders(document):
        document["measured"][0]["receiver"] = "screen"

    refused(two_ladders, "one ladder")

    def free_born(document):
        document["families"].append({"name": "e", "quantum": 0, "charge": -15, "phase": True})
        document["measured"][0]["emitter"]["family"] = "e"

    refused(free_born, "paid family")
