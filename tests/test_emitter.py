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

(a) M excitations give M births at the rungs: each birth at the first interval where the
    excited record's booked motion crosses T (2 u + 1) / (2 W) (tracked interval by
    interval), the residues in the wheel's order ("ordinal" the counter, "seed" the keyed
    permutation), the quanta conserved (the stock spent one per birth, the books balanced
    at every interval), the excited record ended at its click and the next one seeded with
    the next residue, none after the stock; the birth line's keys.
(b) The born values: at the birth the record's `now` and `before` equal the cosine table at
    phase(0) and phase(-1) of the born clock on every cell of the body and 0 elsewhere; its
    norm is the sum of the squared steps; nothing drives it afterwards (its train 0, no
    grace, its own body's cells taking nothing of it); nothing reaches Manhattan distance m
    before age m; the born records reach the receiver by name and click.
(c) The loader's refusals, each naming its key.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.integer import keyed_permutation
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.world import parse_nature_beam_world

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
    wheel: tuple[int, int] = (1, 4),
    order: str = "ordinal",
    seed: int | None = None,
    ticks: int = 1200,
    side: int = 12,
    on_mode: bool = True,
) -> dict:
    """The emitter's unit world: a chain of 80 (x open), the emitter a body of the matter
    kind [800, 809] with the well pair [800, 800] of side `side` at x = 5, seeded on its
    bound mode at the amplitude 100 (the generator's `seed_on_the_mode`, the body's
    conditions of the load check), its stock `amount` = `stock`, its `emitter` the light
    family [77, 25] on the wheel given with its residue order and its ladder the set
    `screen`; the receiver a body of light at x = 70 read as `screen`; the world's wheel 64 the sets' rung."""
    emitter: dict = {
        "family": "light",
        "wheel": list(wheel),
        "residue_order": order,
        "receiver": ["screen"],
    }
    if seed is not None:
        emitter["residue_seed"] = seed
    document = {
        "law": "beam",
        "model_id": "beam-detector-law-emitter-unit-v1",
        "shape": [80, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "K": 1073741824,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "massive_record": True,
        "amplitude_bound": 1 << 32,
        "wheel": 64,
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
                "pair": [800, 800],
                "seed": 100,
                "emitter": emitter,
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


def test_a_m_excitations_give_m_births_at_their_rungs_and_the_quanta_are_conserved():
    document = emitter_world(stock=4, wheel=(1, 4))
    lines, simulation, trace = run(document)
    births = [line for line in lines if line["event"] == "birth"]
    assert len(births) == 4
    assert [line["u"] for line in births] == [0, 1, 2, 3]
    assert [line["excitation"] for line in births] == [1, 2, 3, 4]
    ticks = [line["tick"] for line in births]
    assert ticks == sorted(ticks) and ticks[0] > 1 and ticks[-1] < document["ticks"]
    norm = births[0]["excitation_norm"]
    assert norm > 0 and all(line["excitation_norm"] == norm for line in births)
    # the seed's squares over the body's cells (the record as written at both levels)
    seed = np.array(document["measured"][0]["seed"], dtype=np.int64).reshape(80, 1, 1)
    assert norm == int(np.sum(seed[5:17] * seed[5:17]))
    by_tick = {entry["tick"]: entry for entry in trace}
    for line in births:
        u = line["u"]
        threshold = norm * (2 * u + 1)  # 2 T u + T <= 2 W C
        assert 2 * 4 * line["excitation_offer"] >= threshold
        # the interval before the click: the offer below the rung
        previous = by_tick[line["tick"] - 1]
        assert 2 * 4 * previous["offer"] < threshold or previous["excited_before"] is None
        # the excited record ended at its click, the next one seeded with the next residue
        entry = by_tick[line["tick"]]
        assert entry["excited_before"] is not None and entry["excited_before"][1] == u
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
    assert sorted(gather["u"] for gather in gathers) == [0, 1, 2, 3]
    for gather in gathers:
        assert gather["content"] == 1 and gather["click_at"] == "rung"
        assert gather["click"] >= gather["birth"] + 65  # the Manhattan distance 5 + 12 .. 70
    # the seed order: the wheel's permutation, the same counts of births
    lines, _, _ = run(emitter_world(stock=4, wheel=(1, 4), order="seed", seed=7))
    seeded = [line["u"] for line in lines if line["event"] == "birth"]
    assert seeded == keyed_permutation(4, 7) and sorted(seeded) == [0, 1, 2, 3]
    # a stock below the wheel: the first residues alone; above it: the wheel again
    lines, _, _ = run(emitter_world(stock=2, wheel=(1, 4)))
    assert [line["u"] for line in lines if line["event"] == "birth"] == [0, 1]
    lines, _, _ = run(emitter_world(stock=3, wheel=(3, 4), ticks=1500))
    assert [line["u"] for line in lines if line["event"] == "birth"] == [0, 3, 2]


def test_b_the_born_record_is_written_once_and_the_law_advances_it():
    document = emitter_world(stock=1, wheel=(1, 1), ticks=400)
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
            steps = 64
            table = simulation._cosine_table(steps)
            now = int(table[simulation._phase(0, 77, 25, steps)])
            before = int(table[simulation._phase(-1, 77, 25, steps)])
            assert now == 0 and before != 0
            assert np.all(born.now[block.mask] == now) and np.all(born.before[block.mask] == before)
            assert not np.any(born.now[~block.mask]) and not np.any(born.before[~block.mask])
            assert born.norm == birth["norm"] == 12 * (now - before) ** 2
            assert birth["cells"] == 12 and birth["excitation"] == 1 and birth["train"] == 0
            assert born.u == 0 and born.content == 1 and born.emitter == 0
            assert born.ladder == [simulation.cell_names.index("screen")]
        if born is not None and born.identity in simulation.records:
            nonzero = np.nonzero(born.now)[0]
            if len(nonzero):
                extent.append((born.age, int(nonzero.min()), int(nonzero.max())))
    assert born is not None and extent
    for age, low, high in extent:
        # nothing reaches Manhattan distance m before age m (the causal bound)
        assert low >= 5 - age and high <= 16 + age
    # no drive and no own take after the write: the body's cells are free
    # Nodes for the born record (not absorbing), and the record's own body
    # books nothing of it onto the ledger's retired row
    assert not simulation.absorbing[block.mask].any()
    assert simulation.books()["families"]["light"]["transit"]["taken_by_emitter"] == 0


def test_c_the_loaders_refusals_name_their_keys():
    def refused(mutate, message: str) -> None:
        document = emitter_world(stock=2, on_mode=False)
        mutate(document)
        with pytest.raises(ValueError, match=message):
            DetectorLawSimulation(parse_nature_beam_world(document))

    def emitter(key, value):
        def mutate(document):
            document["measured"][0]["emitter"][key] = value

        return mutate

    refused(emitter("family", "matter"), "the body's own family")
    refused(emitter("family", "nobody"), "unknown family")
    refused(emitter("wheel", [2, 4]), "coprime")
    refused(emitter("wheel", 4), "must be \\[step, W\\]")
    refused(emitter("residue_order", "counter"), 'must be "ordinal" or "seed"')
    refused(emitter("residue_seed", 3), "refused under residue_order")

    def seed_without_seed(document):
        document["measured"][0]["emitter"]["residue_order"] = "seed"

    refused(seed_without_seed, "residue_seed is required")

    def seed_with_stride(document):
        document["measured"][0]["emitter"].update({"residue_order": "seed", "residue_seed": 1})
        document["measured"][0]["emitter"]["wheel"] = [3, 4]

    refused(seed_with_stride, "the step must be 1")
    refused(emitter("rate", [1, 1]), "unsupported key|rate")

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

    for key, value, message in (
        ("emits", "light", "emits"),
        ("own_grace", 3, "own_grace is refused"),
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
