"""THE POLARISER, its own folder (ALGEBRA.md #the-primitives, the row "the polariser"; the owner's yes of 21:10 Israel time): the record's pair turned back by the body's angle through the transport's rotation, its second level to the body's second set and its first to the first, the shares cos^2 and sin^2 of the angle between the pair and the axis; the angle an exact pair, no float, no number in the code."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.register import discover
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features.polariser import (
    DECLARATION,
    PolariserOwn,
    PolariserStart,
    PolariserTerm,
    apply,
    read_term,
    triple_of,
)
from event_universe.world_files import parse_nature_beam_world
from tests.worlds import emitter_world

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
    assert DECLARATION.writes == ("the record's pair", "the two sets' shares")
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


def test_the_loops_stage_turns_the_pair_at_the_bodys_nodes_and_offers_9_to_16_to_its_two_sets():
    """The hook on the emitter's unit world (the loop's stage called on the folder's `apply`; the body's `polariser` key through the loader is Nature24's follow-up, so the term is set on the loop): the one body's polariser at (2, 1), the triple (3, 4, 5), naming two of the world's detectors as its sets; the given record with the level 5 planted at the body's 32 Nodes and no second level: the stage rebinds the pair to (3, -4) there (the rotation by minus the angle, the transport's rounding), leaves the other Nodes, gives the record its second level at 0 elsewhere, and books 9 per Node to the first set and 16 to the second, Malus's 9 : 16 on the 32 Nodes."""
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
    booked = [now - then for now, then in zip(live.pointers, pointers, strict=True)]
    assert booked == [0, 16 * 32, 0, 0, 9 * 32]
