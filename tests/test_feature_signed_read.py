"""The signed read, its own folder (ALGEBRA.md #the-paces): the content as it is, no floor, the reads summed by plain and by sign; the guard at load on squares (the checkerboard factor at -2) admits and refuses by name, and the read in the interval carries no guard."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.features import signed_read
from event_universe.features.signed_read import (
    SignedReadOwn,
    SignedReadStart,
    SignedReadTerm,
    apply,
    edge_squared,
    guard,
    stability_bound,
)

GAMMA, SHAPE = 10_000, (3, 3, 3)


def test_a_hill_enters_as_it_is_and_the_guard_refuses_a_pace_beyond_the_edge_by_name():
    """No floor and no clamp: a hill of 150 on [800, 850] (the edge's square 2 den Gamma^2 div (den + num) between 10,150^2 and 10,151^2) takes the clock's square to 10,151^2 and the load refuses it naming the Node; 75 passes as it is, the content -75, and the read alone never refuses; the same hill on the axis contents alone is caught on that axis as an integer pace."""
    left, right = stability_bound((800, 850), GAMMA)
    edge = edge_squared((800, 850), GAMMA)
    assert (left, right) == (1_650, GAMMA * GAMMA * 1_700) and edge == right // left
    assert 10_150**2 <= edge < 10_151**2
    term = SignedReadTerm(((1, -1, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA)
    own = SignedReadOwn(0, "matter")

    def hill(depth: int) -> SignedReadStart:
        level = np.zeros(SHAPE, dtype=np.int64)
        level[1, 1, 1] = depth
        return SignedReadStart(SHAPE, {1: level}, None)

    assert int(apply(term, hill(75)).content[1, 1, 1]) == -75
    guard(term, apply(term, hill(75)), own)
    assert int(apply(term, hill(150)).content[1, 1, 1]) == -150  # the read carries no guard
    with pytest.raises(ValueError, match=r"squared is 103045000 at the Node \(1, 1, 1\) at load"):
        guard(term, apply(term, hill(150)), own)
    flat, axis = np.zeros(SHAPE, dtype=np.int64), np.zeros(SHAPE, dtype=np.int64)
    axis[2, 0, 1] = -153
    plain = SignedReadTerm(((1, 1, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA)
    with pytest.raises(ValueError, match=r"axis 2\) squared is 103083409 at the Node \(2, 0, 1\)"):
        guard(plain, apply(plain, SignedReadStart(SHAPE, {1: flat}, (flat, flat, axis))), own)


def test_a_massless_family_is_refused_at_any_content_below_zero_and_every_family_needs_a_pace_above_zero():
    """For den = num the edge is p <= Gamma exactly: a content of -1 takes the clock's square to Gamma^2 + 2 Gamma + 2 - 1 and refuses the load by name; a content at Gamma div 2 (the Link's pace Gamma - 2 c at 0) refuses it on the lower side; Gamma div 2 - 1 passes."""
    massless = SignedReadTerm(((1, 1, signed_read.BY_PLAIN),), 0, (1, 1), GAMMA)
    own, shape = SignedReadOwn(2, "light"), (2, 2, 2)
    hollow = np.zeros(shape, dtype=np.int64)
    hollow[0, 1, 0] = -1
    with pytest.raises(ValueError, match=r"squared is 100020002 at the Node \(0, 1, 0\) at load, above"):
        guard(massless, apply(massless, SignedReadStart(shape, {1: hollow}, None)), own)
    deep = np.zeros(shape, dtype=np.int64)
    deep[1, 1, 1] = GAMMA // 2
    with pytest.raises(ValueError, match=r"is 0 at the Node \(1, 1, 1\) at load: the pace"):
        guard(massless, apply(massless, SignedReadStart(shape, {1: deep}, None)), own)
    deep[1, 1, 1] = GAMMA // 2 - 1
    writes = apply(massless, SignedReadStart(shape, {1: deep}, None))
    guard(massless, writes, own)
    assert int(writes.content[1, 1, 1]) == GAMMA // 2 - 1


def test_a_multi_read_sum_by_sign_and_no_reads():
    """Three reads (2 a - 3 b plain, + 4 c by sign with q = -1) sum per Node exactly; no reads give 0; a read by sign with q per Node (+1 and -1, the senses at the Nodes) enters one level with opposite signs."""
    shape, a = (2, 1, 1), np.array([[[5]], [[7]]], dtype=np.int64)
    b, c = np.array([[[1]], [[-2]]], dtype=np.int64), np.array([[[3]], [[0]]], dtype=np.int64)
    reads = ((1, 2, signed_read.BY_PLAIN), (2, -3, signed_read.BY_PLAIN), (3, 4, signed_read.BY_SIGN))
    term = SignedReadTerm(reads, -1, (800, 850), GAMMA)
    writes = apply(term, SignedReadStart(shape, {1: a, 2: b, 3: c}, None))
    assert writes.content.tolist() == [[[2 * 5 - 3 * 1 + 4 * 3]], [[2 * 7 + 3 * 2]]]
    silent = apply(SignedReadTerm((), 0, (1, 1), GAMMA), SignedReadStart(shape, {}, None))
    assert not silent.content.any() and silent.content.shape == shape
    q, level = np.array([[[1]], [[-1]]], dtype=np.int64), np.full(shape, 7, dtype=np.int64)
    term = SignedReadTerm(((3, 1, signed_read.BY_SIGN),), q, (800, 850), GAMMA)  # q per Node
    hill = apply(term, SignedReadStart(shape, {3: level}, None))
    assert hill.content.ravel().tolist() == [-7, 7]  # opposite senses read one level oppositely


def test_a_read_by_an_unknown_word_and_a_sum_that_could_leave_int64_are_refused_by_name():
    """A read by a word other than plain or sign is refused naming the family and the word; a read whose reach leaves int64 is refused before any product; two reads whose reach together leaves int64 too."""
    shape = (2, 1, 1)
    level = np.array([[[3]], [[-4]]], dtype=np.int64)
    unknown = SignedReadTerm(((1, 1, "signed"),), 1, (800, 850), GAMMA)
    with pytest.raises(ValueError, match="the read of family 1 is by 'signed': by 'plain' or by 'sign'"):
        apply(unknown, SignedReadStart(shape, {1: level}, None))
    huge = np.array([[[10**16]], [[-(10**16)]]], dtype=np.int64)
    heavy = SignedReadTerm(((1, 1000, signed_read.BY_PLAIN),), 0, (800, 850), GAMMA)
    with pytest.raises(ValueError, match="family 1 at the weight 1000 reaches 10000000000000000000"):
        apply(heavy, SignedReadStart(shape, {1: huge}, None))
    half = np.array([[[5 * 10**18]], [[0]]], dtype=np.int64)
    reads = ((1, 1, signed_read.BY_PLAIN), (2, -1, signed_read.BY_PLAIN))
    two = SignedReadTerm(reads, 0, (800, 850), GAMMA)
    with pytest.raises(ValueError, match="family 2 at the weight -1 reaches 10000000000000000000"):
        signed_read.content_of(two, SignedReadStart(shape, {1: half, 2: half}, None))
    assert signed_read.TOTAL_BOUND == 2**63 - 1
