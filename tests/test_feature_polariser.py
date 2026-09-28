"""THE POLARISER, its own folder (ALGEBRA.md #the-primitives, the row "the polariser"; the owner's yes of 21:10 Israel time): the record's pair turned back by the body's angle through the transport's rotation, its second level to the body's second set and its first to the first, the shares cos^2 and sin^2 of the angle between the pair and the axis; the angle an exact pair, no float, no number in the code."""

from __future__ import annotations

import copy
import json

import numpy as np
import pytest

from event_universe.core.register import discover
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.events.live import planted_record
from event_universe.features.polariser import (
    DECLARATION,
    PolariserOwn,
    PolariserStart,
    PolariserTerm,
    apply,
    at,
    read_term,
    triple_of,
)
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.worlds import ROOT

LIGHT_CLOCK = ROOT / "tests" / "light_clock.json"

SETS = ("plus", "minus")


def along_axis(level: int, nodes: int = 5) -> PolariserStart:
    return PolariserStart(np.full(nodes, level, dtype=np.int64), np.zeros(nodes, dtype=np.int64))


def test_the_card_is_built_at_ii_with_the_bodys_key():
    """The folder's card: "the polariser" at (ii) after the step, the function apply, the body's key `polariser` (the angle's pair and the two sets) through the cards; a body with no key polarises nothing."""
    declaration = discover().declarations["the polariser"]
    assert (declaration.function, declaration.place, declaration.word) == (
        apply,
        "(ii)",
        "after the step",
    )
    assert declaration.schema is not None and "polariser" in declaration.schema.places["a body"].keys
    assert DECLARATION.writes == ("the level next, the remainder", "the second level")
    assert read_term({"family": "matter"}) is None
    assert read_term({"polariser": {"angle": [2, 1], "sets": ["plus", "minus"]}}) == PolariserTerm(
        (2, 1), SETS
    )


def test_the_shares_are_cos_squared_and_sin_squared_of_the_angle_to_the_axis():
    """GENERIC (any pair (m, j), the triple (m^2 - j^2, 2 m j, m^2 + j^2)), VECTOR (arrays over the body's Nodes), LOCAL (each Node alone): a pair along the axis passes whole to the first set at j = 0, swaps to the second at j = m (a quarter turn), and at (2, 1) (the triple (3, 4, 5)) splits 9 : 16 in the sets' offers, Malus's cos^2 = 9 / 25 exact; a Node's result does not depend on its neighbours."""
    level = 1000
    whole = apply(PolariserTerm((1, 0), SETS), along_axis(level), PolariserOwn())
    assert list(whole.first) == [level * level] * 5 and not any(whole.second)
    assert list(whole.re) == [level] * 5 and not whole.im.any()
    quarter = apply(PolariserTerm((1, 1), SETS), along_axis(level), PolariserOwn())
    assert not any(quarter.first) and list(quarter.second) == [level * level] * 5
    assert triple_of((2, 1)) == (3, 4, 5)
    split = apply(PolariserTerm((2, 1), SETS), along_axis(level), PolariserOwn())
    assert list(split.re) == [600] * 5 and list(split.im) == [-800] * 5
    assert list(split.first) == [360000] * 5 and list(split.second) == [640000] * 5
    assert split.first[0] * 25 == 9 * level * level and split.second[0] * 25 == 16 * level * level
    mixed = PolariserStart(
        np.array([1000, -300, 0, 77], dtype=np.int64), np.array([0, 400, 250, -77], dtype=np.int64)
    )
    together = apply(PolariserTerm((3, 1), SETS), mixed, PolariserOwn())
    for node in range(4):
        alone = apply(
            PolariserTerm((3, 1), SETS),
            PolariserStart(mixed.re[node : node + 1], mixed.im[node : node + 1]),
            PolariserOwn(),
        )
        assert (together.re[node], together.im[node]) == (alone.re[0], alone.im[0])
        assert (
            together.first[node] == together.re[node] ** 2
            and together.second[node] == together.im[node] ** 2
        )


def test_the_refusals_by_name():
    """m below 1, j beyond m, two sets of one name, and a pair of two shapes are refused naming the fault."""
    with pytest.raises(ValueError, match="m from 1 and j from 0 to m"):
        apply(PolariserTerm((0, 0), SETS), along_axis(10), PolariserOwn())
    with pytest.raises(ValueError, match="m from 1 and j from 0 to m"):
        apply(PolariserTerm((2, 3), SETS), along_axis(10), PolariserOwn())
    with pytest.raises(ValueError, match="two distinct sets"):
        apply(PolariserTerm((1, 0), ("plus", "plus")), along_axis(10), PolariserOwn())
    with pytest.raises(ValueError, match="two int64 arrays of one shape"):
        apply(
            PolariserTerm((1, 0), SETS),
            PolariserStart(np.zeros(3, dtype=np.int64), np.zeros(4, dtype=np.int64)),
            PolariserOwn(),
        )


def test_the_bodys_own_set_books_the_fluxs_second_share_and_the_loop_admits_the_act():
    """The booking's form on the shipped light clock (the mathematician's answer of 2026-09-27): A's polariser at (2, 1) with `at_well` (A's own set) as its second set and the face as its first; a record with the level 5 on A's Nodes offers 9 and 16 per Node, so the flux 100 at `at_well` books 64 and the flux 7 books 4 (7 x 16 div 25), a record with no level on A offers 0 and books 0, the face books its flux whole; a term whose second set is not a set on the body is refused by name at the terms' check; and two intervals through the main loop pass its audit; the stage writes nothing (no level rebound, no second level laid, no pointer moved): the turn is read in the booking alone, since a turn written every interval the record passes is a scatterer at the body, not a polariser (measured on Bell's world, tests/test_feature_crystal.py)."""
    document = json.loads(LIGHT_CLOCK.read_bytes())
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    simulation.polarisers = {0: PolariserTerm((2, 1), ("face", "at_well"))}
    at_well, face = simulation.detector_names.index("at_well"), simulation.detector_names.index("face")
    live = planted_record(simulation, 1, np.zeros(simulation.shape), np.zeros(simulation.shape))
    assert simulation._polarised(live, at_well, 100) == 0
    live.now[simulation.blocks[0].mask] = 5
    assert (simulation._polarised(live, at_well, 100), simulation._polarised(live, at_well, 7)) == (
        64,
        4,
    )
    assert simulation._polarised(live, face, 100) == 100
    simulation.polarisers = {0: PolariserTerm((2, 1), ("at_well", "face"))}
    with pytest.raises(ValueError, match="names 'face' as its second set"):
        simulation.family_terms()
    simulation.polarisers = {0: PolariserTerm((2, 1), ("face", "at_well"))}
    while not simulation.records:
        simulation.step()
    simulation.step()
    before = {
        live.identity: (live.now.copy(), list(live.pointers)) for live in simulation.records.values()
    }
    simulation._polariser_stage(apply)
    for live in simulation.records.values():
        assert live.im_now is None and (live.now == before[live.identity][0]).all()
        assert live.pointers == before[live.identity][1]


def test_the_terms_are_read_from_the_bodys_declared_key_at_the_load_and_the_second_set_is_checked():
    """A body in the law's form with the card's key `polariser` (the frame admits it and carries it on the block's `declared`, #1308): the loop's term is read from it at the assembly through the folder's `read_term`, the second set the body's own set (`strip`, on its Node) and the first another body's set (`rest`); the sets the other way round are refused by name at the load, the second not being a set on the body."""
    document = {
        "shape": [16, 1, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": 4,
        "N": 64,
        "universe": "examples/events/generated/universe.json",
        "engine": "examples/events/engine_start.json",
        "measured": [
            {
                "family": "matter",
                "nodes": [{"node": [5, 0, 0], "count": 1}, {"node": [6, 0, 0], "count": 1}],
                "momentum": [0, 0, 0],
                "momentum_before": [0, 0, 0],
                "polariser": {"angle": [2, 1], "sets": ["rest", "strip"]},
            },
            {
                "family": "matter",
                "nodes": [{"node": [12, 0, 0], "count": 1}],
                "momentum": [0, 0, 0],
                "momentum_before": [0, 0, 0],
            },
        ],
        "detectors": [
            {"name": "strip", "positions": [[6, 0, 0]]},
            {"name": "rest", "positions": [[12, 0, 0]]},
        ],
    }
    document["stamp"] = input_stamp(document)
    simulation = DetectorLawSimulation(parse_nature_beam_world(copy.deepcopy(document)))
    assert simulation.polarisers == {0: PolariserTerm((2, 1), ("rest", "strip"))}
    document["measured"][0]["polariser"]["sets"] = ["strip", "rest"]
    document["stamp"] = input_stamp(document)
    with pytest.raises(ValueError, match="names 'rest' as its second set"):
        DetectorLawSimulation(parse_nature_beam_world(document))


def test_the_switching_turns_by_each_angle_in_turn_by_the_bodys_own_count():
    """THE SWITCHING (the row, as Aspect's of 1982): a card with two angles and a period `every` reads as a term carrying both, `at` giving the first angle for `every` intervals and the second for the next, periodic, by two division acts of Rule3; one `angle` with `every`, two `angles` without it, or neither is refused by name, as is a period below 1 at the check; on the shipped light clock the body's own set books the share of the angle in force at the body's count (64 of 100 under (2, 1) at the first interval, 0 under (1, 0) at the next, the pair along the axis whole to the first set); the loader admits the card's `angles` and `every` on a body in the law's form."""
    switching = read_term(
        {"polariser": {"angles": [[2, 1], [1, 0]], "every": 3, "sets": ["face", "at_well"]}}
    )
    assert switching == PolariserTerm((2, 1), ("face", "at_well"), ((2, 1), (1, 0)), 3)
    assert [at(switching, count).angle for count in range(8)] == [(2, 1)] * 3 + [(1, 0)] * 3 + [
        (2, 1)
    ] * 2
    assert at(read_term({"polariser": {"angle": [2, 1], "sets": ["face", "at_well"]}}), 7).angle == (
        2,
        1,
    )
    for entry in (
        {"angle": [2, 1], "every": 2, "sets": ["face", "at_well"]},
        {"angles": [[2, 1], [1, 0]], "sets": ["face", "at_well"]},
        {"sets": ["face", "at_well"]},
    ):
        with pytest.raises(ValueError, match="one `angle`, or its two `angles` with its period `every`"):
            read_term({"polariser": entry})
    start = PolariserStart(np.zeros(2, dtype=np.int64), np.zeros(2, dtype=np.int64))
    with pytest.raises(ValueError, match="two angles with its period `every` from 1 together"):
        apply(PolariserTerm((2, 1), ("face", "at_well"), ((2, 1), (1, 0)), 0), start, PolariserOwn())
    document = json.loads(LIGHT_CLOCK.read_bytes())
    simulation = DetectorLawSimulation(parse_nature_beam_world(document))
    simulation.polarisers = {0: PolariserTerm((2, 1), ("face", "at_well"), ((2, 1), (1, 0)), 1)}
    at_well = simulation.detector_names.index("at_well")
    live = planted_record(simulation, 1, np.zeros(simulation.shape), np.zeros(simulation.shape))
    live.now[simulation.blocks[0].mask] = 5
    booked = []
    for simulation.tick in (0, 1, 2):
        booked.append(simulation._polarised(live, at_well, 100))
    assert booked == [64, 0, 64]
    world = {
        "shape": [16, 1, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": 4,
        "N": 64,
        "universe": "examples/events/generated/universe.json",
        "engine": "examples/events/engine_start.json",
        "measured": [
            {
                "family": "matter",
                "nodes": [{"node": [6, 0, 0], "count": 1}],
                "momentum": [0, 0, 0],
                "momentum_before": [0, 0, 0],
                "polariser": {"angles": [[2, 1], [1, 0]], "every": 3, "sets": ["rest", "strip"]},
            },
            {
                "family": "matter",
                "nodes": [{"node": [12, 0, 0], "count": 1}],
                "momentum": [0, 0, 0],
                "momentum_before": [0, 0, 0],
            },
        ],
        "detectors": [
            {"name": "strip", "positions": [[6, 0, 0]]},
            {"name": "rest", "positions": [[12, 0, 0]]},
        ],
    }
    world["stamp"] = input_stamp(world)
    loaded = DetectorLawSimulation(parse_nature_beam_world(world))
    assert loaded.polarisers == {0: PolariserTerm((2, 1), ("rest", "strip"), ((2, 1), (1, 0)), 3)}
