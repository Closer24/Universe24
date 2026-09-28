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
    read_term,
    triple_of,
)
from event_universe.world_files import input_stamp, parse_nature_beam_world
from tests.worlds import ROOT, emitter_world

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


def test_the_loops_stage_turns_the_pair_at_the_bodys_nodes_and_books_nothing():
    """The hook's stage on the emitter's unit world (the loop's stage called on the folder's `apply`; the body's `polariser` key through the loader is Nature24's follow-up, so the term is set on the loop): the one body's polariser at (2, 1), the triple (3, 4, 5); the given record with the level 5 planted at the body's 32 Nodes and no second level: the stage rebinds the pair to (3, -4) there (the rotation by minus the angle, the transport's rounding), whole, leaves the other Nodes, gives the record its second level at 0 elsewhere, and books nothing (the shares enter through the clicks' booking)."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(emitter_world(stock=1, ticks=20)))
    simulation.step()
    (live,) = simulation.records.values()
    mask = simulation.blocks[0].mask
    simulation.polarisers = {0: PolariserTerm((2, 1), ("screen", "measured:1"))}
    now = live.now.copy()
    now[mask] = 5
    live.now = now
    outside, pointers = live.now[~mask].copy(), list(live.pointers)
    simulation._polariser_stage(apply)
    assert set(live.now[mask].tolist()) == {3} and set(live.im_now[mask].tolist()) == {-4}
    assert (live.now[~mask] == outside).all() and not live.im_now[~mask].any()
    assert live.im_before is not None and not live.im_before.any() and int(mask.sum()) == 32
    assert live.pointers == pointers


def test_the_bodys_own_set_books_the_fluxs_second_share_and_the_loop_admits_the_act():
    """The booking's form on the shipped light clock (the mathematician's answer of 2026-09-27): A's polariser at (2, 1) with `at_well` (A's own set) as its second set and the face as its first; a record with the level 5 on A's Nodes offers 9 and 16 per Node, so the flux 100 at `at_well` books 64 and the flux 7 books 4 (7 x 16 div 25), a record with no level on A offers 0 and books 0, the face books its flux whole; a term whose second set is not a set on the body is refused by name at the terms' check; and two intervals through the main loop pass its audit under the card's two words, the record turned at A's Nodes carrying its second level."""
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
    (given,) = simulation.records.values()
    assert given.im_now is not None and given.im_now[simulation.blocks[0].mask].any()


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
