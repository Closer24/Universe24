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
import math
import sys
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import UNIT, DetectorLawSimulation
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
    side: int = 12,
    on_mode: bool = True,
) -> dict:
    """The emitter's unit world: a chain of 80 (x closed, mirrors), the emitter a body of the
    matter kind [800, 809] with the well pair [800, 801] (W = 2403 remainder values, ALGEBRA.md
    9.22 (4)) of side `side` at x = 5, seeded on its bound mode at the amplitude 2^20 (the
    generator's `seed_on_the_mode`, the body's conditions of the load check; at 100 the born
    light's back-action swamps the excited record, ALGEBRA.md 9.17 (7) (c)), its stock
    `amount` = `stock`, its `emitter` the light family [77, 25] with its ladder the set
    `screen`, its coupling G [1, 50], g [1, 1000] to light (required, ALGEBRA.md 9.19 (4e));
    the receiver the cube of side 3 of light bodies at [70, 72] read as `screen` (record
    1899); no wheel anywhere."""
    # the cube helper of the detector-law suite (imported here: that suite imports
    # `massive_generator` from this one)
    from tests.test_detector_law import receiver_cube

    emitter: dict = {"family": "light", "receiver": ["screen"]}
    document = {
        "law": "beam",
        "model_id": "beam-detector-law-emitter-unit-v1",
        "shape": [80, 1, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": ticks,
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
        "measured": [
            {
                "position": [5, 0, 0],
                "family": "matter",
                "amount": stock,
                "phase": 0,
                "momentum": [0, 0, 0],
                "fixed": True,
                "side": side,
                "pair": [800, 801],
                "coupling": {"G": [1, 50], "g": [1, 1000]},
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
    # share at the Node x = 11 (the corner 5 plus 12 // 2) from the two
    # levels after each interval's step, summed over `period` intervals, bit
    # for bit; the period the nearest integer to 2 pi / omega_b (63 on this
    # well); the share the mode's own tick, constant within the seed's
    # rounding wobble (below one part in a thousand at 2^20), and the whole
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
    centre[11, 0, 0] = True
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
    assert 1000 * (max(shares) - min(shares)) < action // emitter["period"]
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
        # the +x half's front over the 54 Links from the body's face at 16 to
        # the screen at 70 at light's pace c = 0.577 (about 94 intervals); the
        # rung (2 u + 1) T / 128 crossed on the front
        assert gather["click"] >= gather["birth"] + 65
        assert gather["click"] == gather["tick"] and gather["record"] not in simulation.records
    # ITEM 15'S FINDING RESOLVED (ALGEBRA.md 9.19 (4e)): the born records act
    # back on the excited record's rows through the body's coupling g, so the
    # remainder at the centre cell moves between births and the residues
    # spread (one residue at every birth without the coupling, item 15)
    assert len({line["u"] for line in births}) > 1
    # a smaller stock: as many births
    lines, _, _ = run(emitter_world(stock=2))
    assert len([line for line in lines if line["event"] == "birth"]) == 2


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
            # the write on the circle of 2 N (ALGEBRA.md 9.17 (6)): now = A
            # C_2N[3 N / 2 + s] with s = floor(77 / 25) = 3 on N = 64, the
            # entry 99 of the 128-step table (cos 278.4 degrees, 38 of 256 on
            # the amplitude unit: 155648), before = -now exactly
            # no table in the engine (9.22 (2)): the pair is the world's two
            # integers `born`, the generator's: round(A sin(pi n / (d N))) on
            # the clock [77, 25] at N = 64 (the half step of 3.08 steps)
            now, before = document["measured"][0]["emitter"]["born"]
            assert now == 157930 == round(UNIT * math.sin(math.pi * 77 / (25 * 64)))
            assert before == -now
            assert np.all(born.now[block.mask] == now) and np.all(born.before[block.mask] == before)
            assert not np.any(born.now[~block.mask]) and not np.any(born.before[~block.mask])
            # the norm T the record's conserved form I in the flux's units
            # (ALGEBRA.md 9.19 (3), BUILD.md section 26 item 14), the engine's
            # integer read on the board at the birth
            assert born.norm == birth["norm"] == simulation.conserved_form(born) > 0
            assert birth["cells"] == 12 and birth["excitation"] == 1 and birth["train"] == 0
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
        assert low >= 5 - age and high <= 16 + age
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

    def uncoupled(document):
        del document["measured"][0]["coupling"]

    refused(uncoupled, "emitter needs the body's `coupling`")

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
    refused(emitter("born", {"now": [1, 2], "before": [3, 4]}), r"must be \[now, before\]")
    refused(emitter("born", [0, 0]), "writes no motion")
    refused(emitter("born", [5, 4]), "before = -now")
    refused(
        lambda document: document["measured"][0]["emitter"].pop("born"),
        "declares no `born`",
        on_mode=True,
    )

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
