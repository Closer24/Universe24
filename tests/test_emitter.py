"""The emitter as a clicking body (ALGEBRA.md 9.17 (4), the mathematician's integers of
2026-09-24; LAB_TOOLS.md A.1; the model owner's word of 22:30Z, "in principle we cannot do
any operation on the Nodes except to produce a click"): a body of a massive kind with its
seed and a stock `amount` = M holds its excited records in turn (the seed at both levels,
content one quantum, the residue from the body's wheel [step, W] in its residue order);
excited record k clicks at its own rung on its own Nodes (E its own motion booked through
its Nodes, D the rung 2 T u_k + T <= 2 W C with T its norm, the seed's squares over its
Nodes); at that click X ends it and E^T givings the photon, written ONCE at both levels
(now = A C[phase(0)], before = A C[phase(-1)] on the body's Nodes, A the lamp's unit) with
the norm T the motion the write inserts and the excitation's residue, and, while the stock
lasts, excited record k + 1. No rate, no train, no drive, no source term, no grace, no own
take. BUILD.md section 26.

SINCE THE FLUX READING (ALGEBRA.md 9.19 (3); BUILD.md section 26 items 13 and 14): the
excited record's offer is the one-way flux into the body's centre Node, its norm T the
generator's integer `norm` (that flux over one period of the mode advanced alone); the given
record's norm its conserved form I; every set books the one-way flux into its Nodes and the
click is on the cumulative ladder, the record deleted whole at it. The unit world's faces
are CLOSED (mirrors): an open face two Links behind a body is the face receiver, last on
every ladder, and the half that leaves through it clicks there before anything reaches a
screen (test_detector_law.py reads that).

(a) M excitations give M givings at the rungs: each giving at the first interval where the
    excited record's booked flux crosses T (2 u + 1) / (2 W) (tracked interval by
    interval), the residues in the wheel's order ("ordinal" the counter, "seed" the keyed
    permutation), the quanta conserved (the stock spent one per giving, the books balanced
    at every interval), the excited record ended at its click and the next one seeded with
    the next residue, none after the stock; the giving line's keys.
(b) The given values: at the giving the record's `now` and `before` equal the cosine table at
    phase(0) and phase(-1) of the given clock on every Node of the body and 0 elsewhere; its
    norm is its conserved form; nothing drives it afterwards (its train 0, no grace, no
    take); nothing reaches Manhattan distance m before age m; the given records reach the
    receiver by name and click.
(c) The loader's refusals, each naming its key.
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from dataclasses import replace
from fractions import Fraction
from pathlib import Path

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.rule import rule_coefficients
from event_universe.events.world import input_stamp, parse_nature_beam_world

ROOT = Path(__file__).resolve().parents[1]
# THE NODE CLOCK (the model owner's decision (5) of record 1962; ALGEBRA.md 9.35 (2), (3);
# BUILD.md section 26 item 31): Gamma, the world key `node_clock` of every test world, the
# eighteen's 10^6; the clock pair (e, f) = (Gamma - c, Gamma) at every Node under the fixed
# wall 3 den Gamma (BUILD.md section 26 item 34), c the family of clicks' level there
NODE_CLOCK = (
    10**4
)  # the integers of ALGEBRA.md 9.57 (2) and 9.61 (3) under the weak-field rule (item 44)
# THE FAMILY GENERICITY (the model owner's record 2066; BUILD.md section 26 item 51): what a
# family is stands on the family. THE FAMILY OF CLICKS (record 1982; ALGEBRA.md 9.45; item
# 32): the fourth family of every test world, holding the content ("held": "content"); its
# level at a Node is the Node clock. THE FAMILY OF CHARGE (9.48; item 35): the fifth family,
# holding the signed charge; every reading family declares `reads`, the content plainly and
# the charge by its own sign at the weight Lambda (CHARGE_STRENGTH); every family declares
# its charge, 0 here.
CLOCK_FAMILY_NAME = "clicks"
CLOCK_FAMILY = {
    "name": CLOCK_FAMILY_NAME,
    "quantum": 1,
    "pair": [1, 1],
    "charge": 0,
    "held": "content",
    "reads": [],
}
CHARGE_FAMILY_NAME = "charge"
CHARGE_FAMILY = {
    "name": CHARGE_FAMILY_NAME,
    "quantum": 1,
    "pair": [1, 1],
    "charge": 0,
    "held": "sign",
    "reads": [],
}
CHARGE_STRENGTH = 1
READS = [
    {"family": CLOCK_FAMILY_NAME, "weight": 1},
    {"family": CHARGE_FAMILY_NAME, "weight": CHARGE_STRENGTH, "by": "sign"},
]


def reads() -> list[dict]:
    """A reading family's `reads`, a fresh copy."""
    return [dict(read) for read in READS]


def wheel_of(pair, content: int, gamma: int = NODE_CLOCK) -> int:
    """The wheel W of the rule at a Node (ALGEBRA.md 9.22 (4), 9.57 (1); BUILD.md section 26
    items 34, 36 and 44; the engine's `wheel_at`): the wall w over the gcd of the rule's three
    integers, R on the six reads, S at the Node and w itself (`rule_coefficients`, the
    weak-field rule at the Node's own pace p = Gamma - c); the pair's own 3 den / gcd(num, 3
    den) in the vacuum (2403 on [800, 801], 700 on [801, 700]: at c = 0 the weak-field rule is
    the plain rule times 2 Gamma^2)."""
    num, den = int(pair[0]), int(pair[1])
    read, self_coefficient, wall = rule_coefficients(num, den, gamma, content, True)
    return wall // math.gcd(wall, self_coefficient, read)


def lawful_wheel(world, line: dict) -> bool:
    """A giving line's W is the rule's at the emitting body's read Node with the family of
    clicks' level the line carries (`read_clocks`: the level at the read Node, then at its six
    reads, GAMEBOARD; the rule reads the Node's own level alone, item 36), its u below it."""
    block = world.measured[line["measured"]].block
    at_node, _reads = line["read_clocks"]
    return line["W"] == wheel_of(block.pair, at_node) and 0 <= line["u"] < line["W"]


def wall_form(simulation, family: int, now, before, content=None) -> Fraction:
    """A record's conserved form under the Node's own pace (ALGEBRA.md 9.50 (9) and (13);
    BUILD.md section 26 item 36) from its two levels and the family of clicks' levels
    `content` (the engine's array when None), in the engine's units (the scale 3 L, L the
    numerators' lcm): [3 L (den / num) Gamma (a^2 + b^2) - 6 L (den / num) c_i a b] / p_i at
    the Nodes, p_i = Gamma - c_i the pace, and L (a_i b_j + a_j b_i) on the Links, plain; an
    exact rational over the six reads (the pace at both ends of a Link, item 34, HISTORY)."""
    gamma = simulation.node_clock
    levels = simulation.level_of("content") if content is None else content
    num = simulation.kind_num[family].astype(object)
    den = simulation.kind_den[family].astype(object)
    wall = simulation.kind_wall(family)
    a = now.astype(object)
    b = before.astype(object)
    read = simulation._neighbours(before, simulation.kind_wrap[family]).astype(object)
    read_coefficient, self_coefficient, wall_at = rule_coefficients(
        num, den, gamma, levels.astype(object), True
    )
    node = wall * (wall_at * (a * a + b * b) - self_coefficient * a * b)
    total = Fraction(0)
    for index in zip(*np.nonzero(node), strict=True):
        total += Fraction(int(node[index]), int(read_coefficient[index]))
    return total - int(np.sum(wall * a * read))


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
    matter kind [800, 809] with the well pair [800, 801] (W = 2403 remainder values in the
    vacuum, ALGEBRA.md 9.22 (4); at its Nodes the wheel of its content under the Node clock,
    9.35 (2)) over the train's 32 Nodes at [5, 37), seeded on its bound mode at the amplitude
    2^20 (the generator's `seed_on_the_mode`, the body's conditions of the load check; at 100
    the given light's back-action swamps the excited record, ALGEBRA.md 9.17 (7) (c)), its
    stock `amount` = `stock`, its `emitter` the light family on the given clock [512, 1] of
    N = 1024 with its `train` of 8 periods along +x (THE GIVEN TRAIN, ALGEBRA.md 9.17 (6a);
    BUILD.md section 26 item 27) and its ladder the set `screen` (no coupling: the click alone,
    the model owner's decision (2) of record 1962); the receiver the cube of side 3 of
    light bodies at [70, 72] read as `screen` (record 1899), 33 Links ahead of the train's
    head; no wheel anywhere."""
    # the cube helper of the detector-law suite (imported here: that suite imports
    # `massive_generator` from this one)
    from tests.test_detector_law import receiver_cube

    # SINCE COMMIT 7 the giving is the window's (ALGEBRA.md 9.85 (5), 9.71 (1)): the body's
    # rotation written at its Nodes at the weight 3 (the written light 3 x 2^20 under the
    # bound 2^22), the train retired
    emitter: dict = {
        "family": "light",
        "receiver": ["screen"],
        "weight": 3,
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
        "clock_stamp": True,
        "detector_law": True,
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
                "phase_per_link": [512, 1],
                "charge": 0,
                "reads": reads(),
            },
            {"name": "matter", "quantum": 1, "pair": [800, 809], "charge": 0, "reads": reads()},
            dict(CLOCK_FAMILY),
            dict(CHARGE_FAMILY),
        ],
        "measured": [
            {
                "position": [5, 0, 0],
                "family": "matter",
                "amount": 1,
                "ramp": 0,
                "start": 0,
                "stocks": {"light": stock},
                "momentum": [0, 0, 0],
                "extents": [32, 1, 1],
                "q": 0,
                "spin": [0, 0, 0],
                "moment": [0, 0, 0],
                "pair": [800, 801],
                "seed": 1 << 10,  # the window's writes pile up at the body's Nodes (commit 7)
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
    the simulation, and per interval the emitter body's own record before the interval's
    emission (its identity, residue, wheel and norm) and its count of intervals after it."""
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    block = simulation.block_by_number[0]
    trace: list[dict] = []
    for _ in range(document["ticks"]):
        before = (
            None
            if block.own is None
            else (block.own.identity, block.own.u, block.own.wheel, block.own.norm)
        )
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        trace.append(
            {
                "tick": simulation.tick,
                "excited_before": before,
                "excited_after": None if block.own is None else block.own.identity,
                "wait": block.wait,
            }
        )
    return lines, simulation, trace


def test_m_excitations_give_m_givings_at_their_rungs_and_the_quanta_are_conserved():
    document = emitter_world(stock=4)
    lines, simulation, trace = run(document)
    givings = [line for line in lines if line["event"] == "giving"]
    assert len(givings) == 4
    # the residue from the law (ALGEBRA.md 9.22 (4)) under the Node clock (9.35
    # (2), (3); BUILD.md section 26 item 31): u the clicking record's remainder
    # at the giving Node in the remainder's step, W = 3 den f / gcd(Gamma num,
    # 6 den M, 3 den f) at that Node with the body's content M (2403 on [800,
    # 801] in the vacuum; here the stock 4, 3, 2, 1 at the four givings), read
    # from the rule (`lawful_wheel`); read on the board below
    assert all(lawful_wheel(simulation.world, line) for line in givings)
    # the level at the body: its one own quantum beside the stock held, 5, 4, 3, 2 (the
    # stock as the given family's content, ALGEBRA.md 9.51 (8); item 47)
    assert [line["content"] for line in givings] == [5, 4, 3, 2]
    assert [line["node_clock"] for line in givings] == [
        [NODE_CLOCK - m, NODE_CLOCK] for m in (5, 4, 3, 2)
    ]
    assert [line["excitation"] for line in givings] == [1, 2, 3, 4]
    ticks = [line["tick"] for line in givings]
    # the first residue is read after the body's first advance (9.19 (4e), 9.43 (4); 0 on
    # the seed itself), the tick ceil((2 u + 1) P / (2 W)) intervals after it (9.44 (5) (c))
    assert ticks == sorted(ticks) and ticks[0] >= 2 and ticks[-1] < document["ticks"]
    norm = givings[0]["excitation_norm"]
    assert norm > 0 and all(line["excitation_norm"] == norm for line in givings)
    # the norm T: one period's action P e_c, the share of the record's
    # conserved form at the body's centre Node summed over one period of its
    # mode advanced alone (ALGEBRA.md 9.17 (7) (e) and (f), 9.19 (3)), the
    # generator's integers `period` and `norm`, read on the board here: the
    # body alone (the same world, its emitter and its screen removed), the
    # share at the Node x = 21 (the corner 5 plus 32 // 2) from the two
    # levels after each interval's step, summed over `period` intervals, bit
    # for bit; the period the nearest integer to 2 pi / omega_b (63 on this
    # well); the share the mode's own tick, constant within the seed's
    # rounding wobble (below three parts in a thousand at 2^20 on the 32-Node well), and the whole
    # board's shares sum to the conserved form
    emitter = document["measured"][0]["emitter"]
    assert emitter["norm"] == norm and emitter["period"] > 0
    alone = json.loads(json.dumps(document))
    del alone["measured"][0]["emitter"]
    alone["measured"] = alone["measured"][:1]
    alone["detectors"] = []
    alone["input"] = input_stamp(alone)  # the stamp of the body alone (its given pair gone)
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
    # the file's norm in the body's own units (9.57 (1); item 44): the action's numerator, its
    # denominator a divisor of the rule's coefficient on the six reads at the centre, R = 2 p^2
    # num with the pace Gamma - stock at the solitary body's centre
    pace = solitary.node_clock_pair((21, 0, 0), body.family)[0]
    num, den = body.definition.pair
    read_coefficient = rule_coefficients(int(num), int(den), NODE_CLOCK, NODE_CLOCK - pace, True)[0]
    assert pace == NODE_CLOCK - 5 and action.numerator == norm  # one own quantum and the stock 4
    assert read_coefficient % action.denominator == 0
    # the share's wobble from the seed's rounding: 2.1 parts in a thousand on the
    # 32-Node well at 2^20 (COMPUTATION; one part in a thousand on the side-12 well), read
    # on the body alone seeded at 2^20 (the emitter world's seed is 2^10 since commit 7, the
    # window's writes piling up at the body's Nodes; a profile at 2^10 rounds coarser)
    fine = emitter_world(stock=4, on_mode=False)
    del fine["measured"][0]["emitter"]
    fine["measured"] = fine["measured"][:1]
    fine["detectors"] = []
    fine["measured"][0]["seed"] = 1 << 20
    massive_generator().seed_on_the_mode(fine)
    fine_solitary = DetectorLawSimulation(parse_nature_beam_world(fine))
    fine_body = fine_solitary.block_by_number[0]
    fine_shares = []
    for _ in range(emitter["period"]):
        fine_solitary.step()
        assert fine_body.own is not None
        fine_shares.append(fine_solitary.form_share(fine_body.own, centre))
    fine_action = sum(fine_shares)
    assert 1000 * (max(fine_shares) - min(fine_shares)) < 3 * (fine_action // emitter["period"])
    by_tick = {entry["tick"]: entry for entry in trace}
    # THE TICK AS A COUNT OF INTERVALS (ALGEBRA.md 9.44 (5) (c), 9.47 (5) (i); BUILD.md
    # section 26 item 33): the residue u read at the previous click (after the first
    # advance for the first, interval 1) times the click at the first count t with 2 W t >=
    # (2 u + 1) P, so each giving falls EXACTLY ceil((2 u + 1) P / (2 W)) intervals after
    # its read (at least one), on the residue and the wheel the previous giving line
    # carries; the first residue is on no line, read from the own record before the
    # first giving (the trace's entry of interval 2, the state after the read at 1)
    period = document["measured"][0]["emitter"]["period"]
    assert all(line["period"] == period for line in givings)
    first = by_tick[2]["excited_before"]
    assert first is not None and first[1] > 0
    read_at = 1
    previous: tuple[int, int] = (first[1], first[2])
    for line in givings:
        u, wheel = previous
        expected = max(1, -(-(2 * u + 1) * period // (2 * wheel)))
        # SINCE COMMIT 7 the line is named at the window's close: the open (`opened`, the
        # click's interval) falls the count after the read, the next count starts at the close
        assert line["opened"] - read_at == expected == line["wait"], (line["opened"], u, wheel)
        assert 2 * wheel * (line["wait"] - 1) < (2 * u + 1) * period <= 2 * wheel * line["wait"]
        read_at = line["tick"]
        previous = (line["u"], line["W"])
        # the residue read at the first shell Node, the body's corner at x = 5
        assert line["read_node"] == [5, 0, 0]
        # THE BODY'S OWN RECORD CONTINUES (9.43 (3)): the same record, the body's
        # identity, before and after every giving; the line's residue on it after the click
        entry = by_tick[line["tick"]]
        assert entry["excited_before"] is not None
        assert entry["excited_after"] == entry["excited_before"][0] == 0
        after = by_tick.get(line["tick"] + 1)
        assert after is None or after["excited_before"][1:3] == (line["u"], line["W"])
    assert simulation.block_by_number[0].own is not None  # the standing record continues
    # light spent, the one own quantum of matter kept (item 47), the clicks and the charge
    assert simulation.held[0] == [0, 1, 0, 0]
    books = simulation.books()["families"]
    # the spent quanta on the given family's row, light (item 47)
    assert books["light"]["measured"]["spent"] == 4 and books["light"]["transit"]["released"] == 4
    assert set(simulation.records) == {0}  # the body's own standing record alone remains
    gathers = [line for line in lines if line["event"] == "gather"]
    assert len(gathers) == 4 and all(gather["chosen"] == [["screen", 0, "0"]] for gather in gathers)
    assert sorted(gather["u"] for gather in gathers) == sorted(line["u"] for line in givings)
    for gather in gathers:
        assert gather["content"] == 1 and gather["click_at"] == "rung"
        # the train's head over the 33 Links from the body's head at 36 to the
        # screen at 70 at v_g = 0.447 (about 74 intervals), the tapers' precursor
        # a little before it; the rung crossed on the passage
        assert gather["click"] >= gather["giving"] + 50
        assert gather["click"] == gather["tick"] and gather["record"] not in simulation.records
    # THE RESIDUES SPREAD: the body's own record continues (ALGEBRA.md 9.43 (3)) and its
    # remainder at the first shell Node moves between givings with no coupling, no draw
    # and no reseed (the kept remainder through a reseed, item 29, HISTORY)
    assert len({line["u"] for line in givings}) > 1
    # a smaller stock: as many givings
    lines, _, _ = run(emitter_world(stock=2))
    assert len([line for line in lines if line["event"] == "giving"]) == 2


def test_the_bodys_own_record_is_never_rewritten_and_the_residue_is_read_at_the_first_shell_node():
    """THE RESEED RETIRED (ALGEBRA.md 9.43 (3) and (4); the residue at the click at the first
    shell Node, 9.44 (5) (c); BUILD.md section 26 item 33): the giving end sets the given rows,
    lowers the stock and the content, and leaves the body's own record as it is: at every one
    of the four givings the own record is the same object with its levels and remainders bit
    for bit as before the click, and it goes on advancing after the stock is spent (its levels
    move over the later intervals, no fifth giving). The residue on every giving line is the own
    record's remainder at the first shell Node, the body's corner at x = 5 (the first Node in
    x-major order with a Port; the shell the two ends of the train, x = 5 and x = 36), in the
    remainder's step on the body's wheel there, read at the click; the given record carries
    the same u. The edge case: a body whose every Link is inside it has no shell and is
    refused by name."""
    document = emitter_world(stock=4)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    block = simulation.block_by_number[0]
    own = block.own
    assert own is not None and not np.any(own.remainder) and own.identity == 0
    assert simulation.first_shell_node(block) == (5, 0, 0)
    shell = simulation.shell_mask(block)
    assert int(shell.sum()) == 2 and shell[5, 0, 0] and shell[36, 0, 0]
    read: list[tuple[int, int]] = []
    original = simulation._emit

    def spy(target):
        assert target.own is own
        before = (own.now.copy(), own.before.copy(), own.remainder.copy())
        node = simulation.first_shell_node(target)
        step, wheel = simulation.wheel_at(target.family, node)
        read.append((int(own.remainder[node]) // step, wheel))
        original(target)
        assert target.own is own and block.wait == 0
        for x, y in zip((own.now, own.before, own.remainder), before, strict=True):
            assert np.array_equal(x, y)

    simulation._emit = spy  # type: ignore[method-assign]
    spent: list[np.ndarray] = []
    for _ in range(document["ticks"]):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        assert block.definition.emitter is not None
        if simulation.held[0][block.definition.emitter.family] == 0:  # the stock (item 47)
            spent.append(own.now[block.mask].copy())
    givings = [line for line in lines if line["event"] == "giving"]
    assert len(givings) == 4 and block.own is own and 0 in simulation.records
    assert [(line["u"], line["W"]) for line in givings] == read
    assert all(line["read_node"] == [5, 0, 0] for line in givings)
    gathers = [line for line in lines if line["event"] == "gather"]
    assert sorted(g["u"] for g in gathers) == sorted(line["u"] for line in givings)
    # the standing record goes on after the stock is spent: its levels move, no click
    assert len(spent) > 2 and not np.array_equal(spent[0], spent[-1])
    whole = replace(block, mask=np.ones(simulation.shape, dtype=bool))
    with pytest.raises(ValueError, match="has no shell"):
        simulation.first_shell_node(whole)
    assert len({line["u"] for line in givings}) > 1


def test_the_given_record_is_written_once_and_the_law_advances_it():
    """THE WINDOW'S GIVING (ALGEBRA.md 9.71 (1), 9.85 (5); the one stroke's commit 7, the train
    retired): at the open the given record exists with its window open and nothing written
    yet (the writes come with the record's own steps: the body's rotation at its 32 Nodes
    times the weight 3, zero elsewhere), no giving line yet (the line is named at the close),
    its norm the excitation's action norm / norm_denominator (the generator's integers), its
    ladder the named set; at the close the line carries the window's length, the outward norm
    read (at or above the action) and the open's interval, the residue and the wheel the
    law's, the content the giving found; nothing reaches Manhattan distance m from the body
    before age m; no take after the write (the retired row stays 0)."""
    document = emitter_world(stock=1, ticks=400)
    world = parse_nature_beam_world(document)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(world, observer=lines.append)
    block = simulation.block_by_number[0]
    emitter = document["measured"][0]["emitter"]
    given = None
    closed = None
    extent: list[tuple[int, int, int]] = []
    while simulation.tick < 400:
        simulation.step()
        assert simulation.books()["balanced"]
        light = [live for live in simulation.records.values() if live.family == 0]
        if light and given is None:
            (given,) = light
            assert given.window_open and given.window == 0 and given.train == 0 and given.age == 0
            assert not [line for line in lines if line["event"] == "giving"]
            assert not np.any(given.now) and not np.any(given.before)
            assert given.norm == emitter["norm"] and given.pace == emitter["norm_denominator"]
            assert given.content == 1 and given.emitter == 0
            assert given.ladder == [simulation.detector_names.index("screen")]
        elif given is not None and given.window == 1:
            # the first write: the body's Nodes alone
            assert np.any(given.now[block.mask]) and not np.any(given.now[~block.mask])
        if given is not None and closed is None and not given.window_open:
            closed = simulation.tick
            (giving,) = [line for line in lines if line["event"] == "giving"]
            assert giving["tick"] == closed and giving["window"] == given.window > 1
            assert giving["opened"] == closed - given.window and giving["outward"] == given.outward
            assert giving["outward"] * given.pace >= given.norm == giving["norm"] > 0
            assert giving["given_norm"] == 0 and giving["content"] == 2
            assert giving["pace"] == given.pace and giving["nodes"] == 32
            assert giving["excitation"] == 1 and giving["train"] == 0
            assert given.u == giving["u"] and given.wheel == giving["W"]
            assert lawful_wheel(simulation.world, giving)
        if given is not None and given.identity in simulation.records:
            nonzero = np.nonzero(given.now)[0]
            if len(nonzero):
                extent.append((given.age, int(nonzero.min()), int(nonzero.max())))
    assert given is not None and closed is not None and extent
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

    # a body gives its own family from its `stock` (ALGEBRA.md 9.96 (5); commit 6): the
    # emitter of the body's own family without one is refused naming the stock
    def own_family(document):
        document["measured"][0]["emitter"]["family"] = "matter"
        document["measured"][0]["emitter"]["clock"] = [512, 1]

    refused(own_family, "stock is required")
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

    # the richness of the giving Node (9.22 (4)): a pair with fewer than 500
    # remainder values refuses the emitter naming the count
    def poor_well(document):
        document["measured"][0]["pair"] = [800, 800]

    refused(poor_well, "gives 3 remainder values")

    def on_light(document):
        document["measured"][0]["family"] = "light"
        document["measured"][0]["pair"] = [1, 2]
        document["measured"][0]["emitter"]["family"] = "matter"
        document["measured"][0]["stocks"] = {"matter": 2}
        del document["measured"][0]["seed"]

    refused(on_light, "light's kind")

    def silent(document):
        document["measured"][0]["seed"] = 0

    refused(silent, "needs the body's `seed`")

    def no_stock(document):
        document["measured"][0]["amount"] = 0

    refused(no_stock, "amount")

    def no_held_stock(document):
        del document["measured"][0]["stocks"]  # the stock as the given family's content (item 47)

    refused(no_held_stock, "lacks keys required under `detector_law`: stocks")  # item 57: no default

    # the generator's integers (ALGEBRA.md 9.17 (5) item 1): a norm the
    # emitter does not declare refuses the simulation at its first
    # excitation; a `given` profile of the wrong count, or one that writes no
    # motion, refuses the loader (9.17 (5) item 3)
    def no_norm(document):
        document["measured"][0]["emitter"]["period"] = 70
        document["measured"][0]["emitter"]["norm"] = 1000
        del document["measured"][0]["emitter"]["norm"]

    refused(no_norm, "declares no `norm`", on_mode=True)
    # the mathematician's gate item 8: a body that givings declares its seed
    # as its composed mode's profile; a flat scalar seed is refused
    refused(lambda document: None, "seed. as its composed mode's profile")
    # THE GIVEN TRAIN RETIRED (commit 7; ALGEBRA.md 9.85 (5), 9.71 (1)): its keys `train` and
    # `given` are refused by name with their successor, the window; the window's integers
    # are required on every emitter: the weight g from 1, the action's denominator
    refused(
        emitter("given", {"now": [1] * 32, "before": [-1] * 32, "norm": 1}), "emitter.given is refused"
    )
    refused(emitter("train", {"direction": [1, 0, 0], "periods": 8}), "emitter.train is refused")
    refused(emitter("weight", 0), "weight")

    def no_weight(document):
        del document["measured"][0]["emitter"]["weight"]

    refused(no_weight, "declares no `weight`", on_mode=True)

    def no_action(document):
        del document["measured"][0]["emitter"]["norm_denominator"]

    refused(no_action, "declares no `norm_denominator`", on_mode=True)

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

    def free_given(document):
        document["universe"].append(
            {"name": "e", "quantum": 0, "pair": [1, 1], "charge": -1, "reads": reads()}
        )
        document["measured"][0]["emitter"]["family"] = "e"

    refused(free_given, "paid family")
