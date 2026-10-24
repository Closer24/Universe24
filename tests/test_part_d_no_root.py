"""Part D, Tasks 1 and 2: no root anywhere (the owner, issue #1793, comments 6077053307 and 6077234684). The largest x with x^2 <= n is found by `rule3.largest_below`, a bisection on the share reading x * x against n (products and comparisons, no division on the count, no root), and every site of src reads it; the integer is the same at every site, and these tests say so against `division_fixed_point` (Newton's integer iteration), kept here as the oracle and against Python's `math.isqrt`, which tests alone may use (the gate on src stands in tests/test_the_gates.py)."""

import math
import random
import time
from types import SimpleNamespace

import pytest

from event_universe.core.rule3 import largest_below
from event_universe.features import click, read
from event_universe.loader import derived, rooms

PAIR, GAMMA, T, LIGHT = (4000, 6000), 6000, 32768, (6000, 6000)  # the law's own numbers, the examples' T


def division_fixed_point(square: int) -> int:
    """The old root, kept in the tests alone as the oracle: Newton's integer iteration from above."""
    root = square + 1
    while True:
        lower = (root + square // root) // 2
        if lower >= root:
            return root
        root = lower
        if root == 0:
            return 0


def test_largest_below_equals_the_old_fixed_point_and_the_root_everywhere():
    """Task 1: `largest_below` on every n in [0, 70000], on 2,000 random n below 2^63, on the squares and the squares minus one up to 2^62, and on 0 and 1 equals the oracle `division_fixed_point` and `math.isqrt`; a negative count is refused by name; under 10 s."""
    started = time.perf_counter()
    assert largest_below(0) == 0 and largest_below(1) == 1
    for n in range(70001):
        found = largest_below(n)
        assert found == division_fixed_point(n) == math.isqrt(n), n
        assert found * found <= n < (found + 1) * (found + 1)
    drawn = random.Random(1793)
    for n in (drawn.randrange(1 << 63) for _ in range(2000)):
        assert largest_below(n) == division_fixed_point(n) == math.isqrt(n), n
    for power in range(32):
        for k in (1 << power, (1 << power) + 1, (1 << (power + 1)) - 1):
            if k * k <= 1 << 62:
                assert largest_below(k * k) == division_fixed_point(k * k) == k
                assert largest_below(k * k - 1) == division_fixed_point(k * k - 1) == k - 1
    with pytest.raises(ValueError):
        largest_below(-1)
    assert time.perf_counter() - started < 10


def test_every_site_without_a_root_reads_the_same_integers_as_the_root():
    """Task 2 (c), every site that read a root reads the same integers without one, against `math.isqrt` on the same products: features/click (`squared` and `amplitude`) on the law's pair, T the examples' own; features/read (`edge_of` against `math.isqrt` of `edge_squared`); loader/derived (`count_wall` and `tension_room`; `bound_under_rooms` reads whole families and is covered by the suite's loader tests and the two slits' frozen output)."""
    # features_click
    num, den = PAIR
    gap = den * den - num * num
    square = click.squared(1, T, PAIR)
    assert square == math.isqrt((T * den) ** 2 // (4 * gap)) == 21981
    assert click.amplitude(1, T, PAIR) == math.isqrt(square)
    assert click.squared(1, T, LIGHT) == T // 2 and click.amplitude(1, T, LIGHT) == math.isqrt(T // 2)
    # features_read
    assert read.edge_of(PAIR, GAMMA) == math.isqrt(read.edge_squared(PAIR, GAMMA))
    assert read.edge_of(PAIR, GAMMA) == math.isqrt(2 * PAIR[1] * GAMMA**2 // (PAIR[1] + PAIR[0]))
    # loader_derived
    num, den = PAIR
    gap = den * den - num * num
    assert derived.count_wall(SimpleNamespace(pair=PAIR), T) == math.isqrt(9 * T * T * gap) == 439628852
    assert derived.count_wall(SimpleNamespace(pair=LIGHT), T) == 3 * 6000 * T
    edge = read.edge_of(PAIR, GAMMA)
    q_max = 15266
    room = rooms.tension_room(PAIR, GAMMA, q_max, False)
    assert room == -((-(edge * edge * (math.isqrt(q_max * edge) + 1))) // GAMMA**3)
