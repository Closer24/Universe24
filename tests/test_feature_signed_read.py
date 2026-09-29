"""THE SIGNED READ WITH THE TWO-SIDED GUARD, its own folder (ALGEBRA.md #the-primitives, the first row; ALGEBRA.md #the-paces; record 2224): the folder's read equals the engine's bit for bit on the emitter's world, the hand identity holds, the guard's edge (the checkerboard factor at -2) admits and refuses by name."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.features import signed_read
from event_universe.features.signed_read import (
    SignedReadOwn,
    SignedReadStart,
    SignedReadTerm,
    apply,
    pace_bound,
    stability_bound,
)

GAMMA, SHAPE = 10_000, (3, 3, 3)


def term_of(simulation: DetectorLawSimulation, family: int) -> SignedReadTerm:
    definition = simulation.families[family]
    return SignedReadTerm(
        tuple((other, weight, by) for other, weight, by, _twist in definition.reads),
        simulation.family_charge[family],
        (int(definition.pair[0]), int(definition.pair[1])),
        simulation.node_clock,
    )


def start_of(simulation: DetectorLawSimulation, family: int) -> SignedReadStart:
    return SignedReadStart(
        simulation.shape, dict(simulation.node_level), simulation._axis_contents(family)
    )


def own_of(simulation: DetectorLawSimulation, family: int) -> SignedReadOwn:
    return SignedReadOwn(family, simulation.families[family].name, simulation.tick)


def hand_line(simulation: DetectorLawSimulation, family: int, node: tuple[int, ...]) -> int:
    """The trace's line of the pace's read at one Node (ALGEBRA.md #the-interval): per read the family, the signed weight, the level, by plain or by sign with q, the product; p_0 = Gamma - the sum."""
    q, products = simulation.family_charge[family], []
    for other, weight, by, _twist in simulation.families[family].reads:
        level = int(simulation.node_level[other][node])
        products.append(weight * level if by == "plain" else -q * weight * level)
    return simulation.node_clock - sum(products)


def test_a_hill_enters_at_the_floor_and_the_axis_contents_meet_the_stability_edge():
    """A hill would raise the pace above Gamma; the floor reads it as 0 at any depth (152, 153, 10^8), and the edge of [800, 850], p = 1.0150 Gamma, is the arithmetic's check on the axis contents alone."""
    left, right = stability_bound((800, 850), GAMMA)
    assert (left, right) == (1_650, GAMMA * GAMMA * 1_700) and pace_bound((800, 850), GAMMA) == 10_150
    term = SignedReadTerm(((1, -1, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA)
    own = SignedReadOwn(0, "matter", 7)

    def hill(depth: int) -> SignedReadStart:
        level = np.zeros(SHAPE, dtype=np.int64)
        level[1, 1, 1] = depth
        return SignedReadStart(SHAPE, {1: level}, None)

    for depth in (152, 153, 100_010_000 - GAMMA):
        floored = apply(term, hill(depth), own)
        assert int(floored.content[1, 1, 1]) == 0 and int(floored.content[0, 0, 0]) == 0
    # the same hill on the axis contents alone is caught on that axis
    flat, axis = np.zeros(SHAPE, dtype=np.int64), np.zeros(SHAPE, dtype=np.int64)
    axis[2, 0, 1] = -153
    with pytest.raises(RuntimeError, match=r"axis 2\) is 10153 at the Node \(2, 0, 1\)"):
        apply(
            SignedReadTerm(((1, 1, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA),
            SignedReadStart(SHAPE, {1: flat}, (flat, axis, flat)),
            own,
        )


def test_a_massless_family_reads_a_hill_as_the_floor_and_every_family_needs_a_pace_above_zero():
    """For den = num the edge is p <= Gamma exactly, and the floor keeps every hill at it (read as 0); a content at Gamma div 2 (the Link's pace Gamma - 2 c at 0) ends the run on the lower side; Gamma div 2 - 1 passes."""
    massless = SignedReadTerm(((1, 1, signed_read.BY_PLAIN),), 0, (1, 1), GAMMA)
    own, shape = SignedReadOwn(2, "light", 3), (2, 2, 2)
    hollow = np.zeros(shape, dtype=np.int64)
    hollow[0, 1, 0] = -1
    assert int(apply(massless, SignedReadStart(shape, {1: hollow}, None), own).content[0, 1, 0]) == 0
    deep = np.zeros(shape, dtype=np.int64)
    deep[1, 1, 1] = GAMMA // 2
    with pytest.raises(RuntimeError, match=r"is 0 at the Node \(1, 1, 1\) at interval 3: the pace"):
        apply(massless, SignedReadStart(shape, {1: deep}, None), own)
    deep[1, 1, 1] = GAMMA // 2 - 1
    writes = apply(massless, SignedReadStart(shape, {1: deep}, None), own)
    assert int(writes.content[1, 1, 1]) == GAMMA // 2 - 1


def test_a_multi_read_sum_by_sign_and_the_argument_of_a_pair_as_d_i():
    """Three reads (2 a - 3 b plain, + 4 c by sign with q = -1) sum per Node exactly; no reads give 0; a phase-2 read takes D_i = now^2 - next x before as handed in, times the weight, a hill at the floor 0."""
    shape, a = (2, 1, 1), np.array([[[5]], [[7]]], dtype=np.int64)
    b, c = np.array([[[1]], [[-2]]], dtype=np.int64), np.array([[[3]], [[0]]], dtype=np.int64)
    term = SignedReadTerm(
        ((1, 2, signed_read.BY_PLAIN), (2, -3, signed_read.BY_PLAIN), (3, 4, signed_read.BY_SIGN)),
        -1,
        (800, 850),
        GAMMA,
    )
    writes = apply(term, SignedReadStart(shape, {1: a, 2: b, 3: c}, None), SignedReadOwn(0, "matter", 0))
    assert writes.content.tolist() == [[[2 * 5 - 3 * 1 + 4 * 3]], [[2 * 7 + 3 * 2]]]
    silent = apply(
        SignedReadTerm((), 0, (1, 1), GAMMA), SignedReadStart(shape, {}, None), SignedReadOwn(1, "x", 0)
    )
    assert not silent.content.any() and silent.content.shape == shape
    before = np.array([[[3]], [[-4]]], dtype=np.int64)
    now, after = np.array([[[5]], [[6]]], dtype=np.int64), np.array([[[7]], [[2]]], dtype=np.int64)
    invariant = now * now - after * before  # formed by the loop from the last step's three levels
    assert invariant.tolist() == [[[25 - 21]], [[36 + 8]]]
    sourced = SignedReadTerm(((5, -2, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA)
    writes = apply(sourced, SignedReadStart(shape, {5: invariant}, None), SignedReadOwn(0, "matter", 1))
    assert writes.content.tolist() == [[[0]], [[0]]]


def test_a_read_by_an_unknown_word_and_a_sum_that_could_leave_int64_are_refused_by_name():
    """A read by a word other than plain or sign is refused naming the family and the word; a read whose reach leaves int64 is refused before any product; two reads whose reach together leaves int64 too."""
    shape = (2, 1, 1)
    level, own = np.array([[[3]], [[-4]]], dtype=np.int64), SignedReadOwn(0, "matter", 0)
    with pytest.raises(ValueError, match="the read of family 1 is by 'signed': by 'plain' or by 'sign'"):
        apply(
            SignedReadTerm(((1, 1, "signed"),), 1, (800, 850), GAMMA),
            SignedReadStart(shape, {1: level}, None),
            own,
        )
    huge = np.array([[[10**16]], [[-(10**16)]]], dtype=np.int64)
    with pytest.raises(
        ValueError, match=r"family 1 at the weight 1000 reaches 10000000000000000000 .*int64"
    ):
        apply(
            SignedReadTerm(((1, 1000, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA),
            SignedReadStart(shape, {1: huge}, None),
            own,
        )
    half = np.array([[[5 * 10**18]], [[0]]], dtype=np.int64)
    two = SignedReadTerm(
        ((1, 1, signed_read.BY_PLAIN), (2, -1, signed_read.BY_PLAIN)), 0, (800, 850), GAMMA
    )
    assert signed_read.content_of(
        SignedReadTerm(two.reads[1:], 0, (800, 850), GAMMA), SignedReadStart(shape, {2: half}, None)
    ).tolist() == [[[-(5 * 10**18)]], [[0]]]
    with pytest.raises(
        ValueError, match=r"the read of family 2 at the weight -1 reaches 10000000000000000000"
    ):
        signed_read.content_of(two, SignedReadStart(shape, {1: half, 2: half}, None))
    assert signed_read.TOTAL_BOUND == 2**63 - 1
