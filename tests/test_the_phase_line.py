"""The phase line as a standalone module (features/phase; ALGEBRA.md #the-four-acts (b), #the-direction; the two hands' item (i)): a Rule3 pair at the one fixed angle theta_0 = 1 / Gamma (K_0 = 2 Gamma^2 - 1 over D = 2 Gamma^2), seeded on the half wall at an amplitude a multiple of Gamma, iterated by a level with the angle signed, read as the hop's two integers and folded into the Link's one coefficient rounding; and the family's rest rotation to the unit found by a bisection on the act and no root. The bound used throughout (item (i), both hands): the pair's magnitude within Gamma / 2 levels of X standing plus the walk's proved 1.42 N + 2.3 Gamma levels over the test's N acts (`bound`), never a count. Every test under 30 seconds; each prints its numbers with its time."""

import math
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

from event_universe.core import paces
from event_universe.core.paces import rounded
from event_universe.features.phase import (
    K0,
    D,
    act,
    fold,
    half_wall,
    iterate,
    read,
    rotation_unit,
    seed,
)
from tests.laws import refused

GAMMA = 6_000
WALL, COEFFICIENT = D(GAMMA), K0(GAMMA)
THETA = math.acos(COEFFICIENT / WALL)  # the angle per act, the integer pair's own
X35 = (2**35 // GAMMA) * GAMMA  # 2^35's size, the largest multiple of Gamma below it: 34,359,738,000
X175 = 175 * GAMMA
LINK_UNIT = 2_048_000  # the fold's unit X_ij of the hands' chains


def bound(acts: int) -> float:
    """The hands' bound in levels after `acts` acts: Gamma / 2 standing (the mean remainder, a telescoping sum) plus the walk's proved 1.42 N + 2.3 Gamma (item (i), the mathematician's 2)."""
    return GAMMA / 2 + 1.42 * acts + 2.3 * GAMMA


def magnitude_off(pair, amplitude) -> float:  # type: ignore[no-untyped-def]
    """|c + i s| - X in levels at the pair's now."""
    c, s = read(pair)
    return math.hypot(int(c), int(s)) - amplitude


def lines_equal(one, other) -> bool:  # type: ignore[no-untyped-def]
    """Two pairs of lines bit for bit, scalars or arrays."""
    return all(
        np.array_equal(np.asarray(a, dtype=object), np.asarray(b, dtype=object))
        for line_a, line_b in zip(one, other, strict=True)
        for a, b in zip(line_a, line_b, strict=True)
    )


def test_the_seed_stands_on_the_circle_at_the_half_wall_and_refuses_an_amplitude_off_gamma():
    """The fixed angle: D = 2 Gamma^2 = 72,000,000, K_0 = 71,999,999, 2 K_0 / D = 2 - 1 / Gamma^2 exactly, theta_0 within 2.6 x 10^-9 of 1 / Gamma relative. The seed at X of 2^35's size and at X = 175 Gamma: the cosine line (X, X cos theta_0 rounded half up, D div 2), the sine line (0, -(X div Gamma), D div 2), the sine seed within a level of X sin theta_0 (the advisor's second, item 4); c^2 + s^2 within the bound of X^2 at the now and at the before, and after ten acts; 2^35 itself and 2^35 + 1 refused by name (neither a multiple of Gamma = 2^4 3 5^3)."""
    started = time.perf_counter()
    assert (WALL, COEFFICIENT) == (72_000_000, 71_999_999)
    assert 2 * COEFFICIENT / WALL == 2 - 1 / GAMMA**2
    assert abs(THETA * GAMMA - 1) < 2.7e-9 and half_wall(GAMMA) == GAMMA**2 == WALL // 2
    for amplitude in (X35, X175):
        cosine, sine = pair = seed(amplitude, GAMMA)
        assert cosine == (amplitude, rounded(amplitude * COEFFICIENT, WALL), WALL // 2)
        assert sine == (0, -(amplitude // GAMMA), WALL // 2)
        assert abs(cosine[1] - amplitude * math.cos(THETA)) <= 0.5
        assert abs(-sine[1] - amplitude * math.sin(THETA)) <= 1
        assert abs(magnitude_off(pair, amplitude)) <= bound(0)
        before = math.hypot(cosine[1], sine[1]) - amplitude
        assert abs(before) <= bound(0)
        turned = iterate(pair, 10, GAMMA)
        assert abs(magnitude_off(turned, amplitude)) <= bound(10)
        print(
            f"seed X = {amplitude}: now off {magnitude_off(pair, amplitude):.3f} levels, before off {before:.3f}, after 10 acts {magnitude_off(turned, amplitude):.3f} (bound {bound(10):.0f})"
        )
    refused("not a multiple of Gamma", seed, 2**35, GAMMA)
    refused("not a multiple of Gamma", seed, 2**35 + 1, GAMMA)
    refused("not a multiple", seed, np.array([X35, X35 + 1], dtype=np.int64), GAMMA)
    print(f"theta_0 Gamma - 1 = {THETA * GAMMA - 1:.3e}; {time.perf_counter() - started:.2f} s")


def test_the_circle_holds_over_a_million_acts_and_the_angle_advances_theta_0_per_act():
    """At X of 2^35's size: 10^6 acts at the constant step, |c + i s| - X within the bound at every act (the worst printed); the angle after Gamma acts is one radian (Gamma theta_0 = 1 + 2.6 x 10^-9) within the bound over X; after round(2 pi Gamma) acts the pair is back at the seed within the bound plus the whole act's room X |N theta_0 - 2 pi| (the turn is by whole acts)."""
    started = time.perf_counter()
    cosine, sine = seed(X35, GAMMA)
    worst, acts = 0.0, 10**6
    for _ in range(acts):
        cosine, sine = act(cosine, GAMMA), act(sine, GAMMA)
        worst = max(worst, abs(math.hypot(cosine[0], sine[0]) - X35))
    assert worst <= bound(acts), (worst, bound(acts))
    angle = math.atan2(sine[0], cosine[0])
    expected = math.remainder(acts * THETA, 2 * math.pi)
    assert abs(math.remainder(angle - expected, 2 * math.pi)) <= bound(acts) / X35
    pair = seed(X35, GAMMA)
    c, s = read(iterate(pair, GAMMA, GAMMA))
    radian = math.atan2(s, c)
    assert abs(radian - GAMMA * THETA) <= bound(GAMMA) / X35, radian
    turns = round(2 * math.pi * GAMMA)
    c, s = read(iterate(pair, turns, GAMMA))
    room = X35 * abs(turns * THETA - 2 * math.pi)
    assert abs(c - X35) <= bound(turns) + room and abs(s - X35 * (turns * THETA - 2 * math.pi)) <= bound(
        turns
    )
    print(
        f"10^6 acts: worst |m - X| {worst:.0f} levels ({worst / X35:.2e} of X; bound {bound(acts):.0f}); angle at N = Gamma {radian:.10f}; at N = {turns}: c - X = {c - X35}, s = {s} against X (N theta_0 - 2 pi) = {X35 * (turns * THETA - 2 * math.pi):.1f}; {time.perf_counter() - started:.2f} s"
    )


def test_the_reversal_is_bit_exact_over_ten_thousand_acts():
    """10^4 acts forward then 10^4 inverse acts (direction -1): both lines, levels and remainders, bit for bit the seed; the same through `iterate` at direction -1 and through the signed count."""
    started = time.perf_counter()
    pair = seed(X35, GAMMA)
    cosine, sine = pair
    acts = 10**4
    for _ in range(acts):
        cosine, sine = act(cosine, GAMMA), act(sine, GAMMA)
    forward = (cosine, sine)
    assert forward != pair
    for _ in range(acts):
        cosine, sine = act(cosine, GAMMA, -1), act(sine, GAMMA, -1)
    assert (cosine, sine) == pair
    assert iterate(forward, acts, GAMMA, -1) == pair and iterate(forward, -acts, GAMMA) == pair
    assert iterate(pair, acts, GAMMA) == forward
    refused("direction is 1 or -1", act, pair[0], GAMMA, 0)
    print(
        f"10^4 acts forward and back: bit for bit, remainders {forward[0][2]}, {forward[1][2]} on the way; {time.perf_counter() - started:.2f} s"
    )


def test_the_iterate_by_a_level_is_signed_and_vectorised_over_a_thousand_links():
    """n = +3 then n = -3 returns the seed bit for bit (the angle signed: -3 applies the inverse act, and the pair at -3 is the conjugate of the pair at +3 to the rounding, one level, not bit for bit); over 1,000 Links with their own counts n in [-50, 50] in the hardware's integers (int64 at 2^35's size, 2 K_0 X + D below 2^63), the array iterate is every Link's scalar iterate bit for bit, keeps the kind, and -n (or direction -1) returns the seed; a Link at n = 0 is untouched."""
    started = time.perf_counter()
    pair = seed(X35, GAMMA)
    three = iterate(pair, 3, GAMMA)
    assert three != pair and iterate(three, -3, GAMMA) == pair
    assert iterate(iterate(pair, -3, GAMMA), 3, GAMMA) == pair
    c_plus, s_plus = read(three)
    c_minus, s_minus = read(iterate(pair, -3, GAMMA))
    # the angle signed: the pair at -3 is the conjugate of the pair at +3 to the rounding (one level in c
    # measured), not bit for bit; the bit-exact identity is the reversal's, not the mirror's
    assert abs(c_minus - c_plus) <= bound(3) and abs(s_minus + s_plus) <= bound(3)
    assert s_minus < 0 < s_plus and abs(c_minus - c_plus) <= 2
    print(f"n = -3 against n = +3: c differs by {c_minus - c_plus} level(s), s by {s_minus + s_plus}")
    links = 1_000
    counts = np.random.default_rng(24).integers(-50, 51, size=links).astype(np.int64)
    counts[0] = 0
    amplitudes = np.full(links, X35, dtype=np.int64)
    board = seed(amplitudes, GAMMA)
    turned = iterate(board, counts, GAMMA)
    assert all(a.dtype == np.int64 for line in turned for a in line)
    for k in (0, 1, 2, 500, 999):
        one = iterate(pair, int(counts[k]), GAMMA)
        assert [int(a[k]) for line in turned for a in line] == [int(a) for line in one for a in line]
    assert lines_equal(iterate(turned, -counts, GAMMA), board)
    assert lines_equal(iterate(turned, counts, GAMMA, -1), board)
    assert [int(a[0]) for line in turned for a in line] == [int(a) for line in pair for a in line]
    print(
        f"1,000 Links, |n| <= 50: the array iterate is the scalar's bit for bit and returns to the seed; {time.perf_counter() - started:.2f} s"
    )


def test_the_folds_pair_is_antisymmetric_by_direction_for_every_signed_count():
    """The fold (X^c, X^s) = (1,228,800, 1,638,400) at the unit X_ij = 2,048,000 (a Pythagorean pair, |X^c + i X^s| = X_ij): for n sampled over [-4 Gamma, 4 Gamma], the Link read from its other end, (X^c, -X^s) with (c, -s), gives X^s_ji = -X^s_ij exactly and X^c_ji = X^c_ij (the magnitude rounding with the sign after is odd); the product's magnitude within the bound over X of X_ij; the same over the whole sample at once as an array."""
    started = time.perf_counter()
    fold_cosine, fold_sine = 1_228_800, 1_638_400
    assert fold_cosine**2 + fold_sine**2 == LINK_UNIT**2
    step = 97
    counts = sorted({*range(-4 * GAMMA, 4 * GAMMA + 1, step), -4 * GAMMA, 4 * GAMMA, 0, 1, -1})
    pair = seed(X35, GAMMA)
    pairs, forward, backward = {0: pair}, pair, pair
    for n in counts:
        if n > 0:
            forward = iterate(forward, n - max(k for k in counts if 0 <= k < n), GAMMA)
            pairs[n] = forward
    for n in reversed(counts):
        if n < 0:
            backward = iterate(backward, n - min(k for k in counts if n < k <= 0), GAMMA)
            pairs[n] = backward
    worst = 0.0
    for n in counts:
        c, s = read(pairs[n])
        re_ij, im_ij = fold(fold_cosine, fold_sine, c, s, X35)
        re_ji, im_ji = fold(fold_cosine, -fold_sine, c, -s, X35)
        assert (re_ji, im_ji) == (re_ij, -im_ij), n
        assert isinstance(int(re_ij), int)
        worst = max(worst, abs(math.hypot(int(re_ij), int(im_ij)) - LINK_UNIT))
        angle = math.atan2(int(im_ij), int(re_ij)) - math.atan2(fold_sine, fold_cosine)
        assert (
            abs(math.remainder(angle - n * THETA, 2 * math.pi))
            <= (bound(abs(n)) + 1) / X35 + 1 / LINK_UNIT
        )
    assert worst <= LINK_UNIT * bound(4 * GAMMA) / X35 + 1
    cs = np.array([read(pairs[n]) for n in counts], dtype=np.int64)
    re_all, im_all = fold(fold_cosine, fold_sine, cs[:, 0], cs[:, 1], X35)
    re_back, im_back = fold(fold_cosine, -fold_sine, cs[:, 0], -cs[:, 1], X35)
    assert np.array_equal(re_back, re_all) and np.array_equal(im_back, -im_all)
    assert [int(v) for v in im_all] == [
        int(fold(fold_cosine, fold_sine, *read(pairs[n]), X35)[1]) for n in counts
    ]
    print(
        f"{len(counts)} counts in [-4 Gamma, 4 Gamma]: X^s_ji = -X^s_ij exactly; worst |product| - X_ij {worst:.2f} units of X_ij; {time.perf_counter() - started:.2f} s"
    )


def test_the_half_wall_birth_cancels_the_walks_resonance():
    """The mathematician's item (i) 2 and 4: at X = 2^20 (built by hand, no multiple of Gamma) the line born at r_0 = 0 drifts on resonance, 12,447 levels over 10^6 acts measured by the mathematician; born on the half wall D div 2 the leading term cancels. Both pairs run 10^6 acts; the half-wall seed's worst |c + i s| - X is smaller, both numbers in the assertion."""
    started = time.perf_counter()
    amplitude, acts = 2**20, 10**6
    worst = {}
    for remainder in (0, WALL // 2):
        cosine = (amplitude, rounded(amplitude * COEFFICIENT, WALL), remainder)
        sine = (0, -rounded(amplitude, GAMMA), remainder)
        off = 0.0
        for _ in range(acts):
            cosine, sine = act(cosine, GAMMA), act(sine, GAMMA)
            off = max(off, abs(math.hypot(cosine[0], sine[0]) - amplitude))
        worst[remainder] = off
    zero, half = worst[0], worst[WALL // 2]
    assert half < zero, (
        f"the half-wall seed drifts {half:.0f} levels against {zero:.0f} at r_0 = 0 over {acts} acts"
    )
    assert zero <= bound(acts) and half <= bound(acts)
    print(
        f"X = 2^20, 10^6 acts: worst |m - X| at r_0 = 0 {zero:.0f} levels (the mathematician: 12,447), on the half wall {half:.0f}; {time.perf_counter() - started:.2f} s"
    )


def test_the_rotation_unit_by_the_rotation_act():
    """The family's rest rotation to the unit, K = omega_0 Gamma, found by a bisection on the rotation act and no root (the two hands' (d) of 2026-10-09; features/phase at the fixed angle theta_0 = 1 / Gamma): 5,046 at [4000, 6000] and Gamma 6,000 (arccos(2 / 3) x 6,000 = 5,046.4), 0 at the massless pair [1, 1], and at [2, 3] within one unit of Gamma arccos(2 / 3); the value checked against the phase line itself in Python's fractions at an independent amplitude, the cosine line's level over X above 2 / 3 one act before K and below it one act after, the crossing within one unit of K; and core/paces.py takes no root."""
    gamma = 6000
    assert rotation_unit(4000, 6000, gamma) == 5046
    assert rotation_unit(1, 1, gamma) == 0
    found = rotation_unit(2, 3, gamma)
    assert abs(found - gamma * np.arccos(2 / 3)) <= 1
    amplitude = (2**36 // gamma) * gamma  # an amplitude of the test's own, a multiple of Gamma
    pair = iterate(seed(amplitude, gamma), found - 1, gamma)
    before = Fraction(int(read(pair)[0]), amplitude)
    after = Fraction(int(read(iterate(pair, 2, gamma))[0]), amplitude)
    assert before > Fraction(2, 3) > after, (before, after)
    source = Path(paces.__file__).read_text(encoding="utf-8")
    assert "division_fixed_point" not in source
