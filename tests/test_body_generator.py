"""THE GENERATOR BY RULE3 ALONE, tools/body_generator.py (ALGEBRA.md 9.120 item 4; the Boss's
records 2243, 2244, 2248): from a flat start the read act and the division act iterated stop at
the first repeat of the integer profile and give the bound mode of the count's well (its
rotation above the band's top, its weight inside the counted cube, the float top mode's profile
to the rounding: the test may use floats, the tool never does); a pair whose count binds
nothing is refused by name; the period by the one-Node rule in integers is the nearest integer
to 2 pi / omega; the two levels and the amplitude from the count and the norm; the refusals."""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import pytest
import scipy.sparse as sparse
import scipy.sparse.linalg as sparse_linalg

from tools.body_generator import (
    AMPLITUDE_UNIT,
    PERIODIC,
    bound_mode,
    clock_pair,
    conserved_form,
    period_by_the_rule,
    rule_integers,
    scaled_to_norm,
    two_levels,
)

GAMMA = 10_000
KIND = (800, 1200)


def counted_cube(box: int, side: int, count: int) -> np.ndarray:
    counts = np.zeros((box, box, box), dtype=np.int64)
    low = (box - side) // 2
    counts[low : low + side, low : low + side, low : low + side] = count
    return counts


def float_top_mode(counts: np.ndarray, pair: tuple[int, int]) -> tuple[float, np.ndarray]:
    """The check's oracle in floats: the top eigenvector of the symmetric form on the periodic box, as the level a_i = phi_i p_i."""
    num, den = pair
    shape = counts.shape
    idx = np.arange(counts.size).reshape(shape)
    p = (GAMMA - counts).astype(float)
    u = (p / GAMMA) ** 2
    on_site = 2 - (1 + u) * (den - num) / den - 2 * num * u / den
    rows, cols, vals = [], [], []
    for axis in range(3):
        j = np.roll(idx, -1, axis=axis)
        bond = num * p * np.roll(p, -1, axis=axis) / (3 * den * GAMMA**2)
        rows += [idx.ravel(), j.ravel()]
        cols += [j.ravel(), idx.ravel()]
        vals += [bond.ravel(), bond.ravel()]
    rows.append(idx.ravel())
    cols.append(idx.ravel())
    vals.append(on_site.ravel())
    matrix = sparse.csr_matrix(
        (np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
        shape=(counts.size, counts.size),
    )
    value, vector = sparse_linalg.eigsh(matrix, k=1, which="LA")
    level = np.abs(vector[:, 0].reshape(shape)) * p
    return float(value[0]), level / np.linalg.norm(level)


def test_the_iteration_stops_at_the_first_repeat_and_gives_the_bound_mode():
    """The cube of side 4 at 3000 per Node on the kind [800, 1200] in a periodic box of 12:
    the repeat at iteration 196, a cycle of length 1 (a fixed point), the rotation above the
    band's top 4 / 3 and equal to the float mode's 2 cos omega_b to 10^-6, the profile's
    overlap with the float mode 1 to 10^-6, the share inside the cube 0.76, the clock's
    period 8 by the one-Node rule (2 pi / 0.779)."""
    counts = counted_cube(12, 4, 3000)
    mode = bound_mode(counts, KIND, GAMMA)
    assert (mode.iterations, mode.cycle) == (196, 1)
    assert mode.rotation > Fraction(2 * KIND[0], KIND[1])
    value, level = float_top_mode(counts, KIND)
    assert abs(float(mode.rotation) - value) < 1e-6
    profile = mode.profile.astype(float)
    profile /= np.linalg.norm(profile)
    assert abs(float(np.sum(profile * level)) - 1) < 1e-6
    assert Fraction(75, 100) < mode.share_inside < Fraction(77, 100)
    assert int(np.abs(mode.profile).max()) == AMPLITUDE_UNIT
    clock = clock_pair(mode.rotation)
    assert clock[1] == AMPLITUDE_UNIT and period_by_the_rule(*clock) == round(
        2 * math.pi / math.acos(value / 2)
    )


def test_a_pair_whose_count_binds_nothing_is_refused_by_name():
    """On [800, 809] (1 - cos omega_0 = 0.011) the count's well is too shallow for any cube
    (ALGEBRA.md 9.120 item 2): the iteration settles on the band's top and the tool refuses
    naming the family and the rotation."""
    with pytest.raises(ValueError, match=r"the count binds no mode of the family \[800, 809\]"):
        bound_mode(counted_cube(8, 4, 3000), (800, 809), GAMMA)


def test_the_period_is_the_nearest_integer_to_two_pi_over_omega_with_no_pi():
    """On the shipped emitters' clocks and on a sweep of clocks a / b the first return within
    half a step after half a turn is round(2 pi / acos(a / 2 b)); in integers with the
    remainder carried (Rule3's one-Node form), the light clock's 9 and the dark body's 45
    where its file says 46."""
    assert period_by_the_rule(1651150, 1048576) == 9
    assert period_by_the_rule(2076636, 1048576) == 45
    b = 1 << 20
    for a in range(-2 * b + 1, 2 * b, 20_101):
        assert period_by_the_rule(a, b) == round(2 * math.pi / math.acos(a / (2 * b))), (a, b)
    assert period_by_the_rule(0, 1) == 4 and period_by_the_rule(1, 1) == 6


def test_the_two_levels_and_the_amplitude_from_the_count_and_the_norm():
    """The second level is the read act halved, so the pair (now, before) rotates by the
    mode's own 2 cos omega_b; the form of the pair scales as the square of the levels, and
    the levels scaled to the norm c T give the form within one part in 10^3 of c T (the
    levels then a few tens in size, the rounding's grain)."""
    counts = counted_cube(12, 4, 3000)
    mode = bound_mode(counts, KIND, GAMMA)
    read, self_coefficient, wall = rule_integers(KIND, GAMMA, counts)
    now, before = two_levels(mode.profile, read, self_coefficient, wall, PERIODIC)
    ratio = float(before[6, 6, 6]) / float(now[6, 6, 6])
    assert abs(ratio - float(mode.rotation) / 2) < 1e-4
    paces = GAMMA - counts
    form = conserved_form(now, before, self_coefficient, wall, KIND[0], paces, PERIODIC)
    assert form > 0
    doubled = conserved_form(2 * now, 2 * before, self_coefficient, wall, KIND[0], paces, PERIODIC)
    assert doubled == 4 * form
    norm = Fraction(int(np.sum(counts)) * 34026417078243063, 24990001)  # c T, the emitter's T of today
    scaled_now, scaled_before = scaled_to_norm(now, before, form, norm)
    reached = conserved_form(scaled_now, scaled_before, self_coefficient, wall, KIND[0], paces, PERIODIC)
    assert abs(reached / norm - 1) < Fraction(1, 1000)  # the rounding of levels a few tens in size
    assert 10 < int(np.abs(scaled_now).max()) < AMPLITUDE_UNIT
    assert scaled_now.dtype == np.int64 and scaled_before.dtype == np.int64


def test_the_refusals_by_name():
    with pytest.raises(ValueError, match=r"the clock \[2, 1\] is no rotation"):
        period_by_the_rule(2, 1)
    with pytest.raises(ValueError, match="the counts stay in \\[0, Gamma\\)"):
        bound_mode(counted_cube(4, 2, GAMMA), KIND, GAMMA)
    with pytest.raises(ValueError, match="zero everywhere"):
        bound_mode(np.zeros((4, 4, 4), dtype=np.int64), KIND, GAMMA)
    with pytest.raises(ValueError, match="int64"):
        bound_mode(np.ones((4, 4, 4), dtype=np.int32), KIND, GAMMA)
