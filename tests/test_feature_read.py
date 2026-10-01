"""The read, its own folder (ALGEBRA.md #the-paces): the content as it is, no floor, the reads summed at their weights; the axis content rounded at the read; the guard at load on squares (the checkerboard factor at -2) admits and refuses by name, and the read in the interval carries no guard."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.features.read import axis_content, content_of, edge_squared, guard, stability_bound

GAMMA, SHAPE = 10_000, (3, 3, 3)


def test_a_hill_enters_as_it_is_and_the_guard_refuses_a_pace_beyond_the_edge_by_name():
    """No floor and no clamp: a hill of 150 on [800, 850] (the edge's square 2 den Gamma^2 div (den + num) between 10,150^2 and 10,151^2) takes the clock's square to 10,151^2 and the load refuses it naming the Node; 75 passes as it is, the content -75, and the read alone never refuses; the same hill on the axis contents alone is caught on that axis as an integer pace; for den = num the edge is p <= Gamma exactly: a content of -1 refuses by name, a content at Gamma div 2 (the Link's pace at 0) refuses on the lower side and Gamma div 2 - 1 passes."""
    (left, right), edge = stability_bound((800, 850), GAMMA), edge_squared((800, 850), GAMMA)
    assert (left, right) == (1_650, GAMMA * GAMMA * 1_700) and edge == right // left
    assert 10_150**2 <= edge < 10_151**2 and GAMMA % 2 == 0
    flat = np.zeros(SHAPE, dtype=np.int64)

    def hill(depth: int) -> np.ndarray:
        level = flat.copy()
        level[1, 1, 1] = depth
        return content_of([(-1, level)])

    assert int(hill(75)[1, 1, 1]) == -75 and int(hill(150)[1, 1, 1]) == -150  # the read carries no guard
    guard((800, 850), GAMMA, hill(75), (flat, flat, flat), "matter")
    with pytest.raises(ValueError, match=r"squared is 103045000 at the Node \(1, 1, 1\) at load"):
        guard((800, 850), GAMMA, hill(150), (flat, flat, flat), "matter")
    axis, hollow, deep = flat.copy(), flat.copy(), flat.copy()
    axis[2, 0, 1], hollow[0, 1, 0], deep[1, 1, 1] = -153, -1, GAMMA // 2
    with pytest.raises(ValueError, match=r"axis 2\) squared is 103083409 at the Node \(2, 0, 1\)"):
        guard((800, 850), GAMMA, flat, (flat, flat, axis), "matter")
    with pytest.raises(ValueError, match=r"squared is 100020002 at the Node \(0, 1, 0\) at load, above"):
        guard((1, 1), GAMMA, hollow, (flat, flat, flat), "light")
    with pytest.raises(ValueError, match=r"is 0 at the Node \(1, 1, 1\) at load: the pace"):
        guard((1, 1), GAMMA, deep, (flat, flat, flat), "light")
    deep[1, 1, 1] = GAMMA // 2 - 1
    guard((1, 1), GAMMA, deep, (flat, flat, flat), "light")


def test_the_reads_sum_at_their_weights_and_the_axis_content_rounds_at_the_read():
    """Three reads (2 a - 3 b + 4 c) sum per Node exactly; no reads give the integer 0 (the plain rule at Gamma); the axis content is SUM over the reads of (weight x level + 1) div 2, one division per read: 7 and -7 at the weight 1 give 4 and -3, two reads of 3 and 4 give 2 + 2."""
    shape, a = (2, 1, 1), np.array([[[5]], [[7]]], dtype=np.int64)
    b, c = np.array([[[1]], [[-2]]], dtype=np.int64), np.array([[[3]], [[0]]], dtype=np.int64)
    assert content_of([(2, a), (-3, b), (4, c)]).tolist() == [[[10 - 3 + 12]], [[14 + 6]]]
    assert content_of([]) == 0 and axis_content([]) == 0
    level = np.array([[[7]], [[-7]]], dtype=np.int64)
    assert axis_content([(1, level)]).ravel().tolist() == [4, -3]
    assert axis_content([(1, np.full(shape, 3)), (1, np.full(shape, 4))]).ravel().tolist() == [4, 4]
