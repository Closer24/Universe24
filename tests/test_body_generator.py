"""The generator by Rule3 alone (tools/body_generator.py): the read and division acts iterated to the
first repeat give the bound mode at rest and in motion, the held field at rest under its family's pair
is the well the mode sits on; a pair that binds nothing is refused."""

from __future__ import annotations

import math
from fractions import Fraction

import numpy as np
import pytest
import scipy.sparse as sparse
import scipy.sparse.linalg as sparse_linalg

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import coefficients, rule_total_bound
from tools.body_generator import (
    AT_REST,
    PERIODIC,
    amplitude_unit,
    arrivals,
    bound_mode,
    clock_pair,
    conserved_form,
    field_at_rest,
    moving_levels,
    moving_mode,
    period_by_the_rule,
    read_act,
    rotated,
    rule_integers,
    scaled_to_norm,
    to_amplitude,
    twisted_arrivals,
    two_levels,
)

GAMMA = 10_000
KIND = (800, 1200)
OPEN = (False, False, False)


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
    """A cube of side 4 at 3000 per Node on [800, 1200]: a fixed point at iteration 198, the float
    mode's rotation and profile to 10^-6, 0.76 inside the cube, the clock's period 8."""
    counts = counted_cube(12, 4, 3000)
    mode = bound_mode(counts, KIND, GAMMA)
    assert (mode.iterations, mode.cycle) == (198, 1)
    assert mode.rotation > Fraction(2 * KIND[0], KIND[1])
    value, level = float_top_mode(counts, KIND)
    assert abs(float(mode.rotation) - value) < 1e-6
    profile = mode.profile.astype(float)
    profile /= np.linalg.norm(profile)
    assert abs(float(np.sum(profile * level)) - 1) < 1e-6
    assert Fraction(75, 100) < mode.share_inside < Fraction(77, 100)
    assert int(np.abs(mode.profile).max()) == mode.amplitude
    clock = clock_pair(mode.rotation, mode.amplitude)
    assert clock[1] == mode.amplitude and period_by_the_rule(*clock) == round(
        2 * math.pi / math.acos(value / 2)
    )


def test_the_amplitude_unit_is_derived_from_the_width_and_the_fixed_point_stands_beyond_it():
    """A is the largest amplitude keeping Rule3's total inside int64 (between 2^22 and 2^23 here);
    the profile divided to A / 2 is a fixed point of the iteration at A / 2 within one unit."""
    counts = counted_cube(12, 4, 3000)
    amplitude = amplitude_unit(KIND, GAMMA, counts)
    reads, self_coefficient, wall = coefficients(KIND[0], KIND[1], GAMMA, 3000)
    assert amplitude == (MAX_WORK_INT - wall) // (6 * abs(reads[0]) + abs(self_coefficient) + wall)
    assert (1 << 22) < amplitude < (1 << 23)
    for content in (0, 3000):
        assert rule_total_bound(KIND[0], KIND[1], GAMMA, content, amplitude, True) <= MAX_WORK_INT
    assert rule_total_bound(KIND[0], KIND[1], GAMMA, 3000, amplitude + 1, True) > MAX_WORK_INT
    mode = bound_mode(counts, KIND, GAMMA)
    assert mode.amplitude == amplitude
    # the fixed point at the coarser grain A / 2: the profile divided to A / 2 by the division
    # act, then one read act and one division act at A / 2, returns within one unit of itself
    read, self_coefficient, wall = rule_integers(KIND, GAMMA, counts)
    (coarse,) = to_amplitude((mode.profile,), amplitude // 2)
    (again,) = to_amplitude(
        read_act((coarse,), (arrivals(coarse, PERIODIC),), read, self_coefficient, wall), amplitude // 2
    )
    assert int(np.abs(again - coarse).max()) <= 1
    with pytest.raises(ValueError, match="beyond int64"):
        to_amplitude((mode.profile,), 1 << 41)


def test_a_pair_whose_count_binds_nothing_is_refused_by_name():
    """On [800, 809] (1 - cos omega_0 = 0.011) the count's well is too shallow for any cube (ALGEBRA.md
    9.120 item 2): the iteration settles on the band's top and the tool refuses naming the rotation."""
    with pytest.raises(ValueError, match=r"the count binds no mode of the family \[800, 809\]"):
        bound_mode(counted_cube(8, 4, 3000), (800, 809), GAMMA)


def test_the_period_is_the_nearest_integer_to_two_pi_over_omega_with_no_pi():
    """The period is round(2 pi / acos(a / 2 b)) in integers: 9 for the light clock, 45 for the dark body."""
    assert period_by_the_rule(1651150, 1048576) == 9
    assert period_by_the_rule(2076636, 1048576) == 45
    b = 1 << 20
    for a in range(-2 * b + 1, 2 * b, 20_101):
        assert period_by_the_rule(a, b) == round(2 * math.pi / math.acos(a / (2 * b))), (a, b)
    assert period_by_the_rule(0, 1) == 4 and period_by_the_rule(1, 1) == 6


def test_the_two_levels_and_the_amplitude_from_the_count_and_the_norm():
    """The second level is the read act halved; the levels scaled to c T give the form within 10^-3."""
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
    scaled_now, scaled_before = scaled_to_norm(now, before, form, norm, mode.amplitude)
    reached = conserved_form(scaled_now, scaled_before, self_coefficient, wall, KIND[0], paces, PERIODIC)
    assert abs(reached / norm - 1) < Fraction(1, 1000)  # the rounding of levels a few tens in size
    assert 10 < int(np.abs(scaled_now).max()) < mode.amplitude
    assert scaled_now.dtype == np.int64 and scaled_before.dtype == np.int64


def envelope_times_sine(mode, triple: tuple[int, int, int]) -> np.ndarray:
    """The quarter-turned part of the moving levels, the envelope times sin(k x) by the rotation act."""
    out = np.empty_like(mode.re)
    phase_re = np.full(mode.re.shape[1:], mode.amplitude, dtype=np.int64)
    phase_im = np.zeros(mode.re.shape[1:], dtype=np.int64)
    for x in range(mode.re.shape[0]):
        out[x] = (mode.re[x] * phase_im + mode.im[x] * phase_re) // mode.amplitude
        phase_re, phase_im = rotated(phase_re, phase_im, triple, 1)
    return out


def test_the_moving_body_is_the_same_iteration_with_the_rotation_per_link():
    """At (1, 0, 1) the moving iteration is the resting mode bit for bit; at (99, 20, 101) an eigenvector
    of the untwisted rule to 10^-4, and one step of Rule3 rotates its two levels."""
    counts = counted_cube(12, 4, 3000)
    rest = bound_mode(counts, KIND, GAMMA)
    still = moving_mode(counts, KIND, GAMMA, AT_REST)
    assert np.array_equal(still.re, rest.profile) and not still.im.any()
    assert still.rotation == rest.rotation and still.iterations == rest.iterations
    long_counts = np.zeros((24, 12, 12), dtype=np.int64)
    long_counts[10:14, 4:8, 4:8] = 3000
    long_rest = bound_mode(long_counts, KIND, GAMMA)
    triple = (99, 20, 101)
    moving = moving_mode(long_counts, KIND, GAMMA, triple)
    assert Fraction(2 * KIND[0], KIND[1]) < moving.rotation < long_rest.rotation
    # the stop is a two-cycle of the rounding: one more iteration returns a profile one unit away at most
    assert moving.cycle == 2
    read, self_coefficient, wall = rule_integers(KIND, GAMMA, long_counts)
    again = to_amplitude(
        read_act(
            (moving.re, moving.im),
            twisted_arrivals(moving.re, moving.im, triple, PERIODIC),
            read,
            self_coefficient,
            wall,
        ),
        moving.amplitude,
    )
    again = (again[0] + again[0][::-1]) // 2, (again[1] - again[1][::-1]) // 2
    assert int(np.abs(again[0] - moving.re).max()) <= 1 and int(np.abs(again[1] - moving.im).max()) <= 1
    assert Fraction(70, 100) < moving.share_inside < Fraction(80, 100)
    now, before = moving_levels(moving, triple)
    read, self_coefficient, wall = rule_integers(KIND, GAMMA, long_counts)
    acted = read_act((now,), (arrivals(now, PERIODIC),), read, self_coefficient, wall)[0].astype(float)
    inner = slice(2, 22)
    scale = float(moving.rotation)
    assert np.linalg.norm(acted[inner] - scale * now[inner]) < 1e-4 * np.linalg.norm(now[inner])
    stepped = ((read * sum(arrivals(now, PERIODIC)) + self_coefficient * now) // wall - before).astype(
        float
    )
    cosine = scale / 2
    sine = math.sqrt(1 - cosine * cosine)
    expected = cosine * now + sine * envelope_times_sine(moving, triple)
    assert np.linalg.norm(stepped[inner] - expected[inner]) < 1e-4 * np.linalg.norm(now[inner])
    with pytest.raises(ValueError, match="no Pythagorean triple"):
        moving_mode(counts, KIND, GAMMA, (3, 3, 5))
    asymmetric = counted_cube(12, 4, 3000)
    asymmetric[1, 5, 5] = 100
    with pytest.raises(ValueError, match="mirrored along x"):
        moving_mode(asymmetric, KIND, GAMMA, triple)


def test_the_refusals_by_name():
    with pytest.raises(ValueError, match=r"the clock \[2, 1\] is no rotation"):
        period_by_the_rule(2, 1)
    with pytest.raises(ValueError, match="the counts stay in \\[0, Gamma\\)"):
        bound_mode(counted_cube(4, 2, GAMMA), KIND, GAMMA)
    with pytest.raises(ValueError, match="zero everywhere"):
        bound_mode(np.zeros((4, 4, 4), dtype=np.int64), KIND, GAMMA)
    with pytest.raises(ValueError, match="int64"):
        bound_mode(np.ones((4, 4, 4), dtype=np.int32), KIND, GAMMA)


def test_the_field_at_rest_is_the_static_line_and_the_mode_sits_on_it():
    """THE FIELD AT REST (ALGEBRA.md #the-generator (g)): on the open chain of 13 with 700 at the centre the
    field of [1, 1] is the exact ramp 700, 600, ..., 100 (a fixed point), of [1, 2] the fall 89, 11, 1, 0
    per Link; in the periodic box of 8 the field of [1, 1] fills to the count everywhere (no well: the mode
    is refused by name), on the open box the harmonic well with the mode on it above the band; of [1, 4]
    the well 3000, 138, 0 and the mode within 2 x 10^-3 of the counts' own; den below num refused."""
    chain = np.zeros((13, 1, 1), dtype=np.int64)
    chain[6] = 700
    ramp = field_at_rest(chain, (1, 1), OPEN)
    assert ramp.levels[:, 0, 0].tolist() == [100 * k for k in (1, 2, 3, 4, 5, 6, 7, 6, 5, 4, 3, 2, 1)]
    fall = field_at_rest(chain, (1, 2), OPEN).levels[:, 0, 0].tolist()
    assert fall[6:] == [700, 89, 11, 1, 0, 0, 0] and fall == fall[::-1]
    box = counted_cube(8, 2, 3000)
    uniform = field_at_rest(box, (1, 1))
    assert int(uniform.levels.min()) == int(uniform.levels.max()) == 3000 and uniform.cycle == 1
    with pytest.raises(ValueError, match="binds no mode"):
        bound_mode(box, KIND, GAMMA, content=uniform.levels)
    well = field_at_rest(box, (1, 1), OPEN).levels
    assert well[3, 3, 3] == 3000 > well[3, 3, 5] > well[3, 3, 7] > well[0, 0, 0] > 0
    on_well = bound_mode(box, KIND, GAMMA, wrap=OPEN, content=well)
    assert Fraction(2 * KIND[0], KIND[1]) < on_well.rotation and Fraction(
        30, 100
    ) < on_well.share_inside < Fraction(35, 100)
    short = field_at_rest(box, (1, 4)).levels
    assert short[3, 3, 3] == 3000 and 100 < short[3, 3, 5] < 200 and short[3, 3, 7] == 0
    rotation = bound_mode(box, KIND, GAMMA, content=short).rotation
    assert abs(rotation - bound_mode(box, KIND, GAMMA).rotation) < Fraction(2, 1000)
    with pytest.raises(ValueError, match="num from 1 and den from num"):
        field_at_rest(box, (2, 1))
