"""The family of charge (ALGEBRA.md #the-paces): a field family held at every body's Nodes at its signed charge and stepping by its own plain rule elsewhere, read by the other families at the weight Lambda."""

from __future__ import annotations

import json
from dataclasses import replace
from pathlib import Path

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.bodies import (
    CHAIN,
    CHARGE,
    CLICKS,
    GAMMA,
    LIGHT,
    MATTER,
    NEUTRAL,
    PAIR,
    QUANTA,
    charged_chain,
    content_chain,
    set_strength,
    six_reads,
)
from tests.running import planted
from tests.worlds import CHARGE_FAMILY_NAME, PERIODIC, emitter_world, seed_on_the_mode, wheel_of

# A, the amplitude unit of the planted rows: the worlds' amplitude_bound (ALGEBRA.md #the-line;
# the engine's constant UNIT retired by the model owner's record 2089, BUILD.md section 26 item 57)
UNIT = 1 << 20


ROOT = Path(__file__).resolve().parents[1]


def held_record(simulation: DetectorLawSimulation, source: str):
    """The engine's held record of the family holding `source` (the family genericity, item 51: by attribute, never by index or name)."""
    for family, record in simulation.held_records.items():
        if simulation.families[family].held == source:
            return record
    raise KeyError(source)


def rule_step(
    pair: tuple[int, int], effective: list[int], now: np.ndarray, before: np.ndarray, wrap: bool
) -> tuple[list[int], list[int]]:
    """One step of the rule under the Node's own pace at the effective content `effective` per Node (ALGEBRA.md #the-line, #the-paces): w a_next + r' = R S_6(a_now)_i + S a_now - w a_before + r with r = 0 and (R, S, w) the rule's integers at the effective content c_i of the Node alone; the levels and the remainders, Python integers."""
    num, den = pair
    reads = six_reads(now, wrap)
    levels: list[int] = []
    remainders: list[int] = []
    for i, c in enumerate(effective):
        a, b = int(now[i, 0, 0]), int(before[i, 0, 0])
        # the weak-field rule's three integers at the effective content (ALGEBRA.md #the-line)
        (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, c)
        total = read * reads[i] + self_coefficient * a - wall * b
        levels.append(total // wall)
        remainders.append(total - wall * (total // wall))
    return levels, remainders


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_a_record_reads_the_content_with_its_own_sign_and_light_reads_it_alone():
    """(i) THE READING WITH ONE SIGN (ALGEBRA.md #the-paces): on the periodic chain of 60 with light bodies of QUANTA quanta and charge +1 at [20, 30) (Q = +QUANTA there; the held rows' divisor 1, so each field's level at the start is the count over it, QUANTA at the bodies' Nodes and 0 elsewhere, ALGEBRA.md #the-primitives the row "the hold"), a matter record of charge -1 is advanced at the effective content c + Lambda d = 2 QUANTA at the slab (the hill deepened: its pace Gamma - 2 QUANTA, the clock pair the engine reports), one of charge +1 at c - Lambda d = 0 (the hill filled to the vacuum's pace at Lambda = 1), the neutral record at c alone and a record of the charged light itself (q = +1) at c - Lambda c, each bit for bit the rule's on random rows; at Lambda = 3 the -1 record reads 4 QUANTA and the +1 records 0 (the row's floor: a hill lessens a hollow and never exceeds it). The wheel at a slab Node is the rule's at the effective content. The edge case: the engine refuses the load where the pace could reach 0 at a body's Nodes (its content plus Lambda times its charge in size not below Gamma: Lambda = 99 at the content 10 and the charge 10 gives 10 + 990, 1000, at Gamma 1000; at Lambda = 98 it loads)."""
    rng = np.random.default_rng(35)
    now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
    slab = [QUANTA if 20 <= i < 30 else 0 for i in range(60)]
    for strength in (1, 3):
        for matter_charge in (-1, 1):
            document = charged_chain(60, PERIODIC, range(20, 30), QUANTA, 1, matter_charge, strength, 1)
            simulation = DetectorLawSimulation(parse_nature_beam_world(document))
            assert [simulation.families[f].held for f in simulation.held_families] == [
                "content",
                "sign",
            ]
            assert simulation.families[MATTER].reads == (
                (CLICKS, 1, "plain", 0),
                (CHARGE, strength, "sign", 0),
            )
            assert simulation.family_charge == [1, matter_charge, 0, 0, 0]
            assert [int(v) for v in simulation.level_of("sign")[:, 0, 0]] == slab
            assert [int(v) for v in simulation.level_of("content")[:, 0, 0]] == slab
            effective = [max(c - matter_charge * strength * c, 0) for c in slab]
            assert [int(v) for v in simulation._effective_content(MATTER)[:, 0, 0]] == effective
            assert [int(v) for v in simulation._effective_content(NEUTRAL)[:, 0, 0]] == slab
            assert simulation.node_clock_pair((25, 0, 0), MATTER) == (GAMMA - effective[25], GAMMA)
            assert simulation.node_clock_pair((25, 0, 0), NEUTRAL) == (GAMMA - QUANTA, GAMMA)
            assert simulation.node_clock_pair((5, 0, 0), MATTER) == (GAMMA, GAMMA)
            assert simulation.wheel_at(MATTER, (25, 0, 0))[1] == wheel_of(PAIR, effective[25], GAMMA)
            # one step of the rule on each family's record (the engine's `_advance`, the
            # step's own on a record: a massive record in the register is a block's own)
            lit = [max(c - strength * c, 0) for c in slab]
            for family, pair, reading in (
                (MATTER, PAIR, effective),
                (NEUTRAL, (1, 1), slab),
                (LIGHT, (1, 1), lit),
            ):
                live = planted(simulation, family, now, before, np.zeros((60, 1, 1), dtype=np.int64))
                simulation._advance(live)
                levels, remainders = rule_step(pair, reading, now, before, True)
                assert [int(v) for v in live.now[:, 0, 0]] == levels, family
                assert [int(v) for v in live.remainder[:, 0, 0]] == remainders, family
                assert np.array_equal(live.before, now)
    parse_nature_beam_world(charged_chain(60, PERIODIC, range(20, 30), QUANTA, 1, -1, 98))
    with pytest.raises(ValueError, match="measured\\[0\\]: the pace of 'light' could reach 0"):
        parse_nature_beam_world(charged_chain(60, PERIODIC, range(20, 30), QUANTA, 1, -1, 99))


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_charge_is_held_signed_at_the_bodies_and_moves_with_the_labels():
    """(ii) THE HOLD AT Q (ALGEBRA.md #the-paces, #the-primitives the row "the hold"): on the emitter world with light and the matter kind both of charge -1 (the emitter's one own quantum of matter and its stock of 4 light quanta at [5, 37) (item 47), the screen's three light bodies of one quantum at [70, 72], the cube of side 3 on a chain), Q is -5 at the emitter and -1 at each screen body; the family of charge at the start is Q div 40000 = -1 at their Nodes (the division act's floor, the remainder 39995 carried on the emitter) and 0 in the vacuum; the emitter's Q rises by one at each giving (a held light quantum given, its label in flight on the given record; the body's own quantum and its own charge stay) and the giving line carries it, the screen's first body's Q falls by one at each click there (the label held); the emitter's carried remainder gains its Q after each interval's clicks and stays above 0, so no increment is written; the whole charge of the bodies and of the records in flight is -8 at every interval; the books balanced. The edge case: a light body of charge 0 in a world whose bodies carry charge holds Q = 0 (the neutral chain, (v))."""
    document = emitter_world(stock=4, on_mode=False)
    document["universe"][LIGHT]["sign"] = -1
    document["universe"][MATTER]["sign"] = -1
    seed_on_the_mode(document)  # the stamp covers the charges
    lines: list[dict] = []
    simulation = DetectorLawSimulation(parse_nature_beam_world(document), observer=lines.append)
    charge = held_record(simulation, "sign")
    emitter = simulation.blocks[0]
    key = (simulation.held_families[1], 0)  # the family of charge's time part on the body's remainders
    assert simulation.family_charge == [-1, -1, 0, 0] and simulation.families[key[0]].held == "sign"
    assert np.all(charge.now[5:37] == -1) and not charge.now[37:70].any() and not charge.before.any()
    assert simulation.level_of("sign") is charge.now and not charge.remainder.any()
    assert simulation._body_charge(0) == -5 and simulation._body_charge(1) == -1
    carried = emitter.hold_carry[key]
    assert carried == 39995
    assert np.all(charge.now[70:73] == -1)
    givings = 0
    clicks = 0
    for _ in range(document["ticks"]):
        simulation.step()
        assert simulation.books()["balanced"], simulation.tick
        givings = emitter.givings  # the quantum moves at the window's open (commit 7)
        clicks = sum(1 for line in lines if line["event"] == "gather")
        assert simulation._body_charge(0) == -5 + givings
        assert simulation._body_charge(1) == -1 - clicks
        carried += simulation._body_charge(0)
        assert emitter.hold_carry[key] == carried and carried > 0
        bodies = sum(simulation._body_charge(number) for number in range(len(simulation.held)))
        flight = sum(simulation.family_charge[live.family] for live in simulation.records.values())
        flight -= sum(
            simulation.family_charge[block.own.family]
            for block in simulation.blocks
            if block.own is not None and block.own.identity in simulation.records
        )
        assert bodies + flight == -8, simulation.tick
    assert givings == 4 and clicks >= 1
    for line in lines:
        if line["event"] == "giving":
            assert line["charge"] == -line["content"]


@pytest.mark.usefixtures("the_loads_hold_alone")
def test_the_joint_step_with_both_fields_inverts_bit_for_bit():
    """(iii) THE EXACT BACKWARD RUN (the model owner's record 1994; ALGEBRA.md #the-paces under item 34): on the periodic chain of 60 with light bodies of QUANTA quanta and charge +1 at [20, 30) under the held rows' divisor QUANTA (each field gains one quantum at the bodies' Nodes every interval, ALGEBRA.md #the-primitives the row "the hold"), a record of the charged light (q = +1, reading c - Lambda d) and a neutral record of random rows registered (nothing clicks), both fields rise and fall at Nodes over 30 intervals (the falls counted, above 0, the charge field moved off its start), and the joint step inverts bit for bit: every record's two levels and remainders and both fields' rows. The edge case: the chain with an open x (the zero faces) inverts as exactly."""
    for boundary in (PERIODIC, CHAIN):
        rng = np.random.default_rng(37)
        simulation = DetectorLawSimulation(
            parse_nature_beam_world(charged_chain(60, boundary, range(20, 30), QUANTA, 1, -1, 1, QUANTA))
        )
        starts = []
        for family in (LIGHT, NEUTRAL):
            now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
            before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
            live = planted(simulation, family, now, before, np.zeros((60, 1, 1), dtype=np.int64))
            live = replace(live, identity=family + 1)
            simulation.records[live.identity] = live
            starts.append((live, now.copy(), before.copy()))
        clock, charge = held_record(simulation, "content"), held_record(simulation, "sign")
        fields = (clock.now.copy(), charge.now.copy())
        falls = 0
        previous = charge.now.copy()
        for _ in range(30):
            simulation.step()
            falls += int(np.sum(charge.now < previous))
            previous = charge.now.copy()
        assert falls > 0 and not np.array_equal(charge.now, fields[1])
        assert all(live.identity in simulation.records for live, _, _ in starts)
        for _ in range(30):
            simulation.step_inverse()
        assert simulation.tick == 0
        for live, now, before in starts:
            assert np.array_equal(live.now, now) and np.array_equal(live.before, before)
            assert not live.remainder.any()
        assert np.array_equal(clock.now, fields[0]) and np.array_equal(charge.now, fields[1])
        assert not clock.remainder.any() and not charge.remainder.any()


def test_the_loader_names_the_family_of_charge_and_refuses_what_it_cannot_be():
    """(iv) THE FAMILY GENERICITY (record 2066; item 51): the family of charge is the family declaring `held: "sign"` and Lambda the weight of a reading family's read on it; the world keys `charge_family` and `charge_strength` are refused by name (retired); a weight below 1 is refused; a family without `charge` is refused under the detector law, a charge beyond one sign (|q| > 1) is refused and a charge with a denominator other than 1 (the paid family's whole charge, D-1 of 2026-09-20, the check before this one) is refused; the family of charge is refused as the family of clicks, on a quantum other than 1, on a clock of its own and with a charge of its own; a measured event of it and `held` naming it are refused; a world with the family declared loads, its index among the held families, its reads the matter family's."""
    good = charged_chain(12, PERIODIC, [], 1, 0, 0)
    world = parse_nature_beam_world(good)
    assert world.held_families == (CLICKS, CHARGE) and world.families[CHARGE].held == "sign"
    assert world.families[CHARGE].name == CHARGE_FAMILY_NAME
    assert world.families[MATTER].reads == ((CLICKS, 1, "plain", 0), (CHARGE, 1, "sign", 0))

    def copy() -> dict:
        return json.loads(json.dumps(good))

    def refused(document: dict, message: str) -> None:
        with pytest.raises(ValueError, match=message):
            parse_nature_beam_world(document)

    for key, value in (("charge_family", CHARGE_FAMILY_NAME), ("charge_strength", 1)):
        retired = copy()
        retired[key] = value
        refused(retired, f"the world has unknown keys: {key}")
    weak = copy()
    set_strength(weak, 0)
    refused(weak, r"reads\[1\].weight")
    by = copy()
    by["universe"][MATTER]["reads"][1]["by"] = "signed"
    refused(by, r"reads\[1\].by must be one of")
    twice = copy()
    twice["universe"][MATTER]["reads"].append(
        {"family": CHARGE_FAMILY_NAME, "weight": 2, "twist": 0, "by": "q"}
    )
    refused(twice, "reads names 'charge' twice")
    unlabelled = copy()
    del unlabelled["universe"][MATTER]["sign"]
    refused(unlabelled, r"universe\[1\] lacks keys: sign")
    strong = copy()
    strong["universe"][MATTER]["sign"] = 2
    refused(strong, r"universe\[1\]\.sign must be one of \[-1, 0, 1\], not 2")
    split = copy()
    split["universe"][LIGHT]["sign"] = [1, 2]
    refused(split, r"universe\[0\]\.sign must be one of \[-1, 0, 1\], not \[1, 2\]")
    same = copy()
    same["universe"][CHARGE]["held"] = {"count": "content", "factors": [1], "divisor": 40000}
    refused(same, "two families hold 'content'")
    quantum = copy()
    quantum["universe"][CHARGE]["quantum"] = 2
    quantum["universe"][CHARGE]["clicks"] = {"gives": True, "takes": True, "quantum": 2}
    refused(quantum, "a held family is counted in quanta")
    clocked = copy()
    clocked["universe"][CHARGE]["clock"] = [512, 1]
    refused(clocked, "gives nothing and declares a clock")
    charged = copy()
    charged["universe"][CHARGE]["sign"] = 1
    refused(charged, "a held family carries none")
    unknown = copy()
    unknown["universe"][MATTER]["reads"][1]["family"] = "ions"
    refused(unknown, r"reads\[1\]\.family names 'ions', no family of the universe")
    body = copy()
    body["measured"] = [
        {
            "position": [3, 0, 0],
            "family": CHARGE_FAMILY_NAME,
            "amount": 1,
            "stocks": {},
            "momentum": [0, 0, 0],
            "momentum_before": [0, 0, 0],
        }
    ]
    refused(body, r"measured\[0\] is of the held family 'charge'")
    held = copy()
    held["measured"] = [
        {
            "position": [3, 0, 0],
            "family": "light",
            "amount": 1,
            "momentum": [0, 0, 0],
            "momentum_before": [0, 0, 0],
            "stocks": {CHARGE_FAMILY_NAME: 1},
        }
    ]
    refused(held, r"measured\[0\].stocks names the held family 'charge'")


def test_with_every_charge_zero_the_field_is_zero_and_the_rows_are_those_of_any_lambda():
    """(v) THE REGISTERED WORLDS' CASE (every family of charge 0): on the chain of 60 with a body of QUANTA quanta at [20, 30) and matter and light records of random rows, the family of charge is 0 everywhere at the load and after 40 intervals, and the records' rows are bit for bit the same at Lambda = 1 and Lambda = 7 (no charge is read: the strength weighs nothing); THE LEAK TEST (the model owner's record 2075 (3); BUILD.md section 26 item 55): the never-sourced sign family is named at no interval, the planted matter record (no body of its family) is, and a row planted in the sign family is named. The edge case: the giving lines of the emitter world carry the charge 0."""
    rows = {}
    for strength in (1, 7):
        rng = np.random.default_rng(41)
        document = content_chain(60, PERIODIC, range(20, 30), QUANTA)
        set_strength(document, strength)
        simulation = DetectorLawSimulation(parse_nature_beam_world(document))
        assert simulation.families[MATTER].reads[1][1] == strength
        assert not held_record(simulation, "sign").now.any()
        lives = []
        for family in (0, 1):
            now = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
            before = rng.integers(-UNIT, UNIT, size=(60, 1, 1), dtype=np.int64)
            live = planted(simulation, family, now, before, np.zeros((60, 1, 1), dtype=np.int64))
            live = replace(live, identity=family + 1)
            simulation.records[live.identity] = live
            lives.append(live)
        for _ in range(40):
            # the matter record by the rule at the interval's start content (a massive record
            # in the register is a block's own: the step advances it with its block)
            simulation._advance(lives[1])
            simulation.step()
            assert not held_record(simulation, "sign").now.any()
            # THE LEAK TEST (record 2075 (3); item 55): the never-sourced sign family is not
            # named; the planted matter record (no body of its family, the test's device) is
            assert simulation.leaks() == ["matter"]
        assert not held_record(simulation, "sign").remainder.any()
        # a row planted in the never-sourced family is a leak, named by the family's declared name
        held_record(simulation, "sign").now[3, 0, 0] = 1
        assert simulation.leaks() == [CHARGE_FAMILY_NAME, "matter"]
        held_record(simulation, "sign").now[3, 0, 0] = 0
        assert simulation.leaks() == ["matter"]
        rows[strength] = [(live.now.copy(), live.before.copy(), live.remainder.copy()) for live in lives]
    for one, seven in zip(rows[1], rows[7], strict=True):
        for x, y in zip(one, seven, strict=True):
            assert np.array_equal(x, y)
    lines: list[dict] = []
    simulation = DetectorLawSimulation(
        parse_nature_beam_world(emitter_world(stock=2, ticks=600)), observer=lines.append
    )
    for _ in range(600):
        simulation.step()
    givings = [line for line in lines if line["event"] == "giving"]
    assert givings and all(line["charge"] == 0 for line in givings)
