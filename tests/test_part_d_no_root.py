"""Part D, Tasks 1 and 2: no root anywhere (the owner, issue #1793, comments 6077053307 and 6077234684). The largest x with x^2 <= n is found by `rule3.largest_below`, a bisection on the share reading x * x against n (products and comparisons, no division on the count, no root), and every site of src that read the old `division_fixed_point` (Newton's integer iteration) reads it now; the integer is the same at every site, and these tests say so against the old function kept here as the oracle and against Python's `math.isqrt`, which tests alone may use (the gate on src stands in tests/test_the_gates.py)."""

import math
import random
import time
from types import SimpleNamespace

import pytest

from event_universe import emission, resonance
from event_universe.core.rule3 import division_forward, largest_below
from event_universe.features import click, read
from event_universe.loader import derived, universe

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
    """Task 1: `largest_below` on every n in [0, 70000], on 2,000 random n below 2^63, on the squares and the squares minus one up to 2^62, and on 0 and 1 equals the old `division_fixed_point` and `math.isqrt`; a negative count is refused by name; under 10 s."""
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


def test_features_click_reads_the_same_integers_without_a_root():
    """Task 2 (c), features/click: `squared`, `spread`, `amplitude`, `direction`, `invariant`, `exact_total`, `line_total` and `envelope` (the sites at `standing` and `laid_pairs` read the same `largest_below(den^2 - num^2)` as `invariant`) on the law's pair, T the examples' own and the two slits' lay, against `math.isqrt` on the same products."""
    num, den = PAIR
    gap = den * den - num * num
    square = click.squared(1, T, PAIR)
    assert square == math.isqrt((T * den) ** 2 // (4 * gap)) == 21981
    assert click.spread(square, (3, 7)) == math.isqrt(square * 3 // 7)
    assert click.amplitude(1, T, PAIR) == math.isqrt(square)
    assert click.direction(300, -400, 7) == (300 * 7 // 500, -400 * 7 // 500)
    sine = math.isqrt(gap)
    assert (
        click.invariant(1, T, PAIR, 1)
        == click.spread(T * den // (2 * sine), (1, 1))
        == math.isqrt(T * den // (2 * sine))
    )
    assert click.exact_total(T, PAIR) == math.isqrt((T * den // 2) ** 2 // gap)
    assert click.line_total(T, PAIR) == math.isqrt(T * T * den * den // gap)
    total = click.line_total(T, PAIR)
    envelope = click.envelope(total, 48, 1)
    assert envelope[0] == math.isqrt(total // 48) and envelope[-1] > 0
    assert envelope[1] == math.isqrt((total - envelope[0] ** 2) // 48)
    assert click.squared(1, T, LIGHT) == T // 2 and click.amplitude(1, T, LIGHT) == math.isqrt(T // 2)


def test_emission_reads_the_same_integers_without_a_root():
    """Task 2 (c), emission: `radiated_total` (the site at L81; `born_unit`, `laid_packet`, `start_of` and `increments_of` read a board and are covered by the suite's emission tests and the two slits' frozen output) on the law's pair and T, against `math.isqrt` on the same product."""
    num, den = PAIR
    inner = 3 * num - 2 * den
    expected = math.isqrt((2 * T // 3) ** 2 * (den * den - inner * inner) // (den * den))
    assert emission.radiated_total(T, PAIR) == expected
    assert emission.radiated_total(T, (2, 3)) == 2 * T // 3


def test_features_read_reads_the_same_edge_pace_without_a_root():
    """Task 2 (c), features/read: `edge_of` (the site at L75) on the law's pair and Gamma against `math.isqrt` of `edge_squared`."""
    assert read.edge_of(PAIR, GAMMA) == math.isqrt(read.edge_squared(PAIR, GAMMA))
    assert read.edge_of(PAIR, GAMMA) == math.isqrt(2 * PAIR[1] * GAMMA**2 // (PAIR[1] + PAIR[0]))


def test_loader_derived_reads_the_same_walls_and_rooms_without_a_root():
    """Task 2 (c), loader/derived: `count_wall` (L245) and `tension_room` (L307) on the law's pair, T and Gamma against `math.isqrt`; `bound_under_rooms` (L394, L403) reads whole families and is covered by the suite's loader tests and the two slits' frozen output."""
    num, den = PAIR
    gap = den * den - num * num
    assert derived.count_wall(SimpleNamespace(pair=PAIR), T) == math.isqrt(9 * T * T * gap) == 439628852
    assert derived.count_wall(SimpleNamespace(pair=LIGHT), T) == 3 * 6000 * T
    edge = read.edge_of(PAIR, GAMMA)
    q_max = 15266
    room = derived.tension_room(PAIR, GAMMA, q_max, False)
    assert room == -((-(edge * edge * (math.isqrt(q_max * edge) + 1))) // GAMMA**3)


def test_loader_universe_reads_the_same_composed_pairs_without_a_root():
    """Task 2 (c), loader/universe: `composed_pair` (the sites at lines 100, 103 and 109) on two [2, 3] records at den 6,000: the relative part [5237, 6000] and the centre [2449, 6000] of the docstring, against the same integers by `math.isqrt`."""
    assert universe.composed_pair((2, 3), (2, 3), 6000, True) == (5237, 6000)
    assert universe.composed_pair((2, 3), (2, 3), 6000, False) == (2449, 6000)
    scale = (6000 * 3 * 3) ** 2
    sine = math.isqrt(scale * scale * (9 - 4)) // 3
    cosine = scale * 2 // 3
    along, across = sine * cosine + sine * cosine, sine * sine
    root = math.isqrt(along * along + across * across)
    assert universe.composed_pair((2, 3), (2, 3), 6000, True)[0] == (2 * 6000 * along + root) // (
        2 * root
    )


def test_node_detector_reads_the_same_norm_without_a_root():
    """Task 2 (c), node_detector: the site at `books_of` L78, the record's norm max(largest_below(SUM A_i^2), 1) over the amplitudes `click.spread` lays at the Nodes of a four-Node screen of the two slits (the public function reads a board, so the lay's own numbers stand here), against `math.isqrt`."""
    square = click.squared(1, T, LIGHT)
    amplitudes = [click.spread(square, (1, 4)) for _ in range(4)]
    assert max(largest_below(sum(a * a for a in amplitudes)), 1) == math.isqrt(4 * amplitudes[0] ** 2)
    assert amplitudes[0] == math.isqrt(square // 4)


def test_resonance_reads_the_same_references_and_turns_without_a_root():
    """Task 2 (c), resonance: `references_of` (L45), `turned_direction` (L72) and `window_turn` (L82) on the law's pair at the scale of the width's room, against `math.isqrt` on the same products."""
    num, den = PAIR
    scale = resonance.scale_of(63, 1 << 20, 130)
    (reference,) = resonance.references_of(scale, (SimpleNamespace(resonance=PAIR),))
    assert reference.sine == (0, -(math.isqrt(scale * scale * (den * den - num * num)) // den))
    assert reference.cosine == (scale, int(division_forward(scale * num, den, den // 2)[0]))
    assert resonance.turned_direction(scale, 0, 3, 4) == (scale * 3 // 5, scale * 4 // 5)
    turned = resonance.Reference(PAIR, scale, reference.cosine, reference.sine, 3000, 4000)
    assert resonance.window_turn(turned, 7) == 7 * math.isqrt(3000**2 + 4000**2) // scale
