"""The generator by Rule3 alone (ALGEBRA.md 9.120 item 4): a body's bound mode by Rule3's read act iterated with the before-coefficient 0 and its division act to the amplitude unit, the stop at the first repeat of the integer profile, the two levels, the clock as an exact pair, the period by the one-Node rule and the amplitude from the count and the family's quantum norm; integers and exact rationals only."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import coefficients, rule_total_bound

REPEAT_LIMIT = 1 << 16  # iterations; a host bound on the search for the repeat, not a stop
RETURN_LIMIT = 1 << 24  # intervals; a rotation slower than this is no clock of a run
Wrap = tuple[bool, bool, bool]
PERIODIC: Wrap = (True, True, True)


@dataclass(frozen=True)
class BoundMode:
    """The generator's output for one body: the integer profile at the amplitude unit A, A itself (derived), the iterations to the repeat, the cycle's length, the rotation 2 cos omega_b as an exact fraction and the share of the profile's weight inside the counted Nodes (ALGEBRA.md 9.120 item 4)."""

    profile: np.ndarray
    amplitude: int
    iterations: int
    cycle: int
    rotation: Fraction
    share_inside: Fraction


def check_counts(counts: np.ndarray, gamma: int) -> None:
    """The refusals by name: the counts an int64 array of nonnegative integers below Gamma, at least one nonzero (ALGEBRA.md 9.108 item 12, the guard's lower side)."""
    if counts.dtype != np.int64:
        raise ValueError("the counts are an int64 array (integers only)")
    if counts.size == 0 or not counts.any():
        raise ValueError("the counts are zero everywhere: no body to generate")
    low, high = int(counts.min()), int(counts.max())
    if low < 0 or high >= gamma:
        raise ValueError(
            f"a count is {low if low < 0 else high} at a Node: the counts stay in [0, Gamma) with Gamma = {gamma}"
        )


def amplitude_unit(pair: tuple[int, int], gamma: int, counts: np.ndarray) -> int:
    """The amplitude unit A, derived and never written: the largest amplitude at which Rule3's total stays inside the integer width at every content of the region, (M - w) div (6 R + |S| + w) at the content whose coefficients are largest, M the width, checked against rule_total_bound (ALGEBRA.md 9.120 item 4 (b); 9.57 (2))."""
    num, den = pair
    found = None
    for content in sorted({int(c) for c in counts.ravel()}):
        reads, self_coefficient, wall = coefficients(num, den, gamma, content)
        amplitude = (MAX_WORK_INT - wall) // (6 * abs(reads[0]) + abs(self_coefficient) + wall)
        assert rule_total_bound(num, den, gamma, content, amplitude, True) <= MAX_WORK_INT
        assert rule_total_bound(num, den, gamma, content, amplitude + 1, True) > MAX_WORK_INT
        found = amplitude if found is None else min(found, amplitude)
    if found is None or found < 1:
        raise ValueError(f"no amplitude unit keeps Rule3's total inside the width at Gamma = {gamma}")
    return found


def rule_integers(
    pair: tuple[int, int], gamma: int, counts: np.ndarray
) -> tuple[np.ndarray, np.ndarray, int]:
    """Rule3's integers at every Node from the pace p = Gamma - c: the read R = 2 p^2 num, the self coefficient S and the wall w = 6 den Gamma^2 (ALGEBRA.md 9.57 (1))."""
    reads, self_coefficient, wall = coefficients(pair[0], pair[1], gamma, counts)
    return np.asarray(reads[0], dtype=np.int64), np.asarray(self_coefficient, dtype=np.int64), int(wall)


def six_sum(a: np.ndarray, wrap: Wrap) -> np.ndarray:
    """The six neighbours' levels summed at every Node, the row itself on an axis of one layer, 0 beyond a closed face (the receive of ALGEBRA.md 9.57 (1))."""
    total = np.zeros_like(a)
    for axis in range(3):
        if a.shape[axis] == 1:
            total += 2 * a
            continue
        for sign in (1, -1):
            shifted = np.roll(a, sign, axis=axis)
            if not wrap[axis]:
                edge: list[slice | int] = [slice(None)] * 3
                edge[axis] = 0 if sign == 1 else -1
                shifted[tuple(edge)] = 0
            total += shifted
    return total


def read_act(
    a: np.ndarray, read: np.ndarray, self_coefficient: np.ndarray, wall: int, wrap: Wrap
) -> np.ndarray:
    """Rule3's read act with the before-coefficient 0: (R S_6(a) + S a) div w at every Node, the total at the Node's own coefficients kept inside int64 or refused (ALGEBRA.md 9.120 item 4 (b); 9.119 item 1)."""
    size = int(np.abs(a).max())
    reach = int(np.max(6 * np.abs(read) + np.abs(self_coefficient))) * size
    if reach > MAX_WORK_INT:
        raise ValueError(
            f"the read act reaches {reach} at the level {size}, beyond int64 {MAX_WORK_INT}"
        )
    return (read * six_sum(a, wrap) + self_coefficient * a) // wall


def to_amplitude(a: np.ndarray, amplitude: int) -> np.ndarray:
    """Rule3's division act to the amplitude unit: a x A div max|a|, the product inside int64 or refused (ALGEBRA.md 9.120 item 4 (b))."""
    size = int(np.abs(a).max())
    if size == 0:
        raise ValueError("the read act gives 0 at every Node: no mode")
    if size * amplitude > MAX_WORK_INT:
        raise ValueError(f"the division act reaches {size * amplitude} at A = {amplitude}, beyond int64")
    return (a * amplitude) // size


def rotation_of(
    a: np.ndarray,
    read: np.ndarray,
    self_coefficient: np.ndarray,
    wall: int,
    paces: np.ndarray,
    wrap: Wrap,
) -> Fraction:
    """2 cos omega_b of a profile as the exact quotient of the symmetric form, SUM a (R S_6(a) + S a) / p^2 over w SUM a^2 / p^2 (ALGEBRA.md 9.57 (1), the weights 1 / p_i^2)."""
    total = read.astype(object) * six_sum(a, wrap).astype(object) + self_coefficient.astype(
        object
    ) * a.astype(object)
    numerator, denominator = Fraction(0), Fraction(0)
    levels = a.astype(object)
    for pace in {int(p) for p in paces.ravel()}:
        where = paces == pace
        numerator += Fraction(int(np.sum(levels[where] * total[where])), pace * pace)
        denominator += Fraction(int(np.sum(levels[where] * levels[where])), pace * pace)
    return numerator / (wall * denominator)


def bound_mode(
    counts: np.ndarray,
    pair: tuple[int, int],
    gamma: int,
    amplitude: int | None = None,
    wrap: Wrap = PERIODIC,
) -> BoundMode:
    """The bound mode of the count's well: from a flat start the read act and the division act iterated until the integer profile repeats; refused by name where the rotation does not rise above the band's top 2 num / den or the profile's weight inside the counted Nodes is not twice their fraction of the box, the band's uniform wave (ALGEBRA.md 9.120 items 2 and 4)."""
    check_counts(counts, gamma)
    if amplitude is None:
        amplitude = amplitude_unit(pair, gamma, counts)
    read, self_coefficient, wall = rule_integers(pair, gamma, counts)
    a = np.full(counts.shape, amplitude, dtype=np.int64)
    seen: dict[bytes, int] = {}
    for step in range(REPEAT_LIMIT):
        key = a.tobytes()
        if key in seen:
            break
        seen[key] = step
        a = to_amplitude(read_act(a, read, self_coefficient, wall, wrap), amplitude)
    else:
        raise ValueError(f"the profile repeats within no {REPEAT_LIMIT} iterations")
    paces = gamma - counts
    rotation = rotation_of(a, read, self_coefficient, wall, paces, wrap)
    weights = a.astype(object) * a.astype(object)
    share = Fraction(int(np.sum(weights[counts > 0])), int(np.sum(weights)))
    fraction = Fraction(int(np.count_nonzero(counts)), counts.size)
    if rotation <= Fraction(2 * pair[0], pair[1]) or share <= 2 * fraction:
        raise ValueError(
            f"the count binds no mode of the family [{pair[0]}, {pair[1]}]: the rotation {rotation} "
            f"against the band's top {Fraction(2 * pair[0], pair[1])}, the share inside the counted "
            f"Nodes {share.numerator}/{share.denominator} against their fraction {fraction} of the box, "
            "not twice it (ALGEBRA.md 9.120 item 2)"
        )
    return BoundMode(a, amplitude, step, step - seen[key], rotation, share)


Triple = tuple[int, int, int]  # (a, b, c) with a^2 + b^2 = c^2: cos k = a / c, sin k = b / c, exact
AT_REST: Triple = (1, 0, 1)


def check_triple(triple: Triple) -> None:
    """The refusals by name: the rotation per Link is a Pythagorean triple (a, b, c) with c from 1 and a^2 + b^2 = c^2, so cos k and sin k are exact rationals (ALGEBRA.md 9.96 (2))."""
    a, b, c = triple
    if c < 1 or a * a + b * b != c * c:
        raise ValueError(
            f"the rotation per Link {triple} is no Pythagorean triple: c from 1 and a^2 + b^2 = c^2"
        )


def rotated(re: np.ndarray, im: np.ndarray, triple: Triple, sign: int) -> tuple[np.ndarray, np.ndarray]:
    """The rotation act by k per Link on a level's two parts, (re + i im) x (a + i sign b) div c, the division act with its rounding (ALGEBRA.md 9.120 item 4 (e))."""
    a, b, c = triple
    b = sign * b
    return (a * re - b * im) // c, (a * im + b * re) // c


def twisted_sums(
    re: np.ndarray, im: np.ndarray, triple: Triple, wrap: Wrap
) -> tuple[np.ndarray, np.ndarray]:
    """The six arrivals summed on the moving body's envelope: the two along x rotated by +k and -k per Link (the rotation act), the four across as at rest (ALGEBRA.md 9.120 item 4 (e))."""
    if re.shape[0] == 1:
        along_re, along_im = 2 * re, 2 * im
    else:
        forward_re, forward_im = rotated(np.roll(re, -1, axis=0), np.roll(im, -1, axis=0), triple, 1)
        backward_re, backward_im = rotated(np.roll(re, 1, axis=0), np.roll(im, 1, axis=0), triple, -1)
        if not wrap[0]:
            forward_re[-1] = forward_im[-1] = 0
            backward_re[0] = backward_im[0] = 0
        along_re, along_im = forward_re + backward_re, forward_im + backward_im
    sums = []
    for part, along in ((re, along_re), (im, along_im)):
        across = np.zeros_like(part)
        for axis in (1, 2):
            if part.shape[axis] == 1:
                across += 2 * part
                continue
            for sign in (1, -1):
                shifted = np.roll(part, sign, axis=axis)
                if not wrap[axis]:
                    edge: list[slice | int] = [slice(None)] * 3
                    edge[axis] = 0 if sign == 1 else -1
                    shifted[tuple(edge)] = 0
                across += shifted
        sums.append(along + across)
    return sums[0], sums[1]


def twisted_read_act(
    re: np.ndarray,
    im: np.ndarray,
    read: np.ndarray,
    self_coefficient: np.ndarray,
    wall: int,
    triple: Triple,
    wrap: Wrap,
) -> tuple[np.ndarray, np.ndarray]:
    """Rule3's read act on the moving body's envelope, (R x the twisted sums + S a) div w on each part, the total kept inside int64 or refused (ALGEBRA.md 9.120 item 4 (e))."""
    size = max(int(np.abs(re).max()), int(np.abs(im).max()))
    reach = int(np.max(6 * np.abs(read) + np.abs(self_coefficient))) * size
    if reach > MAX_WORK_INT:
        raise ValueError(
            f"the read act reaches {reach} at the level {size}, beyond int64 {MAX_WORK_INT}"
        )
    sum_re, sum_im = twisted_sums(re, im, triple, wrap)
    return (read * sum_re + self_coefficient * re) // wall, (
        read * sum_im + self_coefficient * im
    ) // wall


def to_amplitude_pair(re: np.ndarray, im: np.ndarray, amplitude: int) -> tuple[np.ndarray, np.ndarray]:
    """Rule3's division act to the amplitude unit on the two parts together, by the larger size, the product inside int64 or refused (ALGEBRA.md 9.120 item 4 (b))."""
    size = max(int(np.abs(re).max()), int(np.abs(im).max()))
    if size == 0:
        raise ValueError("the read act gives 0 at every Node: no mode")
    if size * amplitude > MAX_WORK_INT:
        raise ValueError(f"the division act reaches {size * amplitude} at A = {amplitude}, beyond int64")
    return (re * amplitude) // size, (im * amplitude) // size


@dataclass(frozen=True)
class MovingMode:
    """The moving body's envelope at the rotation k per Link: its two parts at the amplitude unit A, A itself (derived), the iterations to the repeat, the cycle's length, the rotation 2 cos omega_b(k) as an exact fraction, the share inside the counted Nodes (ALGEBRA.md 9.120 item 4 (e))."""

    re: np.ndarray
    im: np.ndarray
    amplitude: int
    iterations: int
    cycle: int
    rotation: Fraction
    share_inside: Fraction


def moving_mode(
    counts: np.ndarray,
    pair: tuple[int, int],
    gamma: int,
    triple: Triple,
    amplitude: int | None = None,
    wrap: Wrap = PERIODIC,
) -> MovingMode:
    """The bound mode of the count's well moving along x at the rotation k per Link: the same iteration as at rest with the twisted read act, from a flat start, each iterate mirrored (the real part even and the imaginary part odd about the centre, the envelope's one gauge), the stop at the first repeat of the two parts; at the triple (1, 0, 1) it is the resting mode (ALGEBRA.md 9.120 item 4 (e))."""
    check_counts(counts, gamma)
    check_triple(triple)
    if not np.array_equal(counts, counts[::-1]):
        raise ValueError(
            "the moving body's counts are mirrored along x about the box's centre (the gauge of its envelope)"
        )
    if amplitude is None:
        amplitude = amplitude_unit(pair, gamma, counts)
    read, self_coefficient, wall = rule_integers(pair, gamma, counts)
    re = np.full(counts.shape, amplitude, dtype=np.int64)
    im = np.zeros(counts.shape, dtype=np.int64)
    seen: dict[bytes, int] = {}
    for step in range(REPEAT_LIMIT):
        key = re.tobytes() + im.tobytes()
        if key in seen:
            break
        seen[key] = step
        re, im = to_amplitude_pair(
            *twisted_read_act(re, im, read, self_coefficient, wall, triple, wrap), amplitude
        )
        re, im = (re + re[::-1]) // 2, (im - im[::-1]) // 2
    else:
        raise ValueError(f"the profile repeats within no {REPEAT_LIMIT} iterations")
    paces = gamma - counts
    sum_re, sum_im = twisted_sums(re, im, triple, wrap)
    t_re = read.astype(object) * sum_re.astype(object) + self_coefficient.astype(object) * re.astype(
        object
    )
    t_im = read.astype(object) * sum_im.astype(object) + self_coefficient.astype(object) * im.astype(
        object
    )
    levels_re, levels_im = re.astype(object), im.astype(object)
    numerator, denominator = Fraction(0), Fraction(0)
    for pace in {int(p) for p in paces.ravel()}:
        where = paces == pace
        numerator += Fraction(
            int(np.sum(levels_re[where] * t_re[where] + levels_im[where] * t_im[where])), pace * pace
        )
        denominator += Fraction(
            int(np.sum(levels_re[where] * levels_re[where] + levels_im[where] * levels_im[where])),
            pace * pace,
        )
    rotation = numerator / (wall * denominator)
    weights = levels_re * levels_re + levels_im * levels_im
    share = Fraction(int(np.sum(weights[counts > 0])), int(np.sum(weights)))
    fraction = Fraction(int(np.count_nonzero(counts)), counts.size)
    if rotation <= Fraction(2 * pair[0], pair[1]) or share <= 2 * fraction:
        raise ValueError(
            f"the count binds no moving mode of the family [{pair[0]}, {pair[1]}] at {triple}: the rotation "
            f"{rotation} against the band's top {Fraction(2 * pair[0], pair[1])}, the share inside "
            f"{share.numerator}/{share.denominator} against the fraction {fraction} (ALGEBRA.md 9.120 item 2)"
        )
    return MovingMode(re, im, amplitude, step, step - seen[key], rotation, share)


def moving_levels(mode: MovingMode, triple: Triple) -> tuple[np.ndarray, np.ndarray]:
    """The moving body's two real levels: now the envelope times cos(k x) per Link (the rotation act along x), before the same one interval earlier, cos omega_b(k) now - sin omega_b(k) x the quarter-turned part, sin from the exact cosine by the integer square root at the amplitude unit (ALGEBRA.md 9.120 item 4 (e); 9.113 item 3 (c))."""
    re, im, amplitude = mode.re.copy(), mode.im.copy(), mode.amplitude
    phase_re, phase_im = (
        np.full(re.shape[1:], amplitude, dtype=np.int64),
        np.zeros(re.shape[1:], dtype=np.int64),
    )
    now_re = np.empty_like(re)
    now_im = np.empty_like(im)
    for x in range(re.shape[0]):
        now_re[x] = (re[x] * phase_re - im[x] * phase_im) // amplitude
        now_im[x] = (re[x] * phase_im + im[x] * phase_re) // amplitude
        phase_re, phase_im = rotated(phase_re, phase_im, triple, 1)
    cosine = mode.rotation / 2
    sine = isqrt(
        ((1 - cosine * cosine) * amplitude * amplitude).numerator
        // ((1 - cosine * cosine) * amplitude * amplitude).denominator
    )
    before = (now_re.astype(object) * cosine.numerator) // cosine.denominator - (
        now_im.astype(object) * sine
    ) // amplitude
    return now_re, before.astype(np.int64)


def clock_pair(rotation: Fraction, denominator: int) -> tuple[int, int]:
    """The clock [a, b] with 2 cos omega_b = a / b on the denominator given (the amplitude unit A, the mode's resolution), a the nearest integer (exact rational rounding)."""
    scaled = rotation * denominator
    return (2 * scaled.numerator + scaled.denominator) // (2 * scaled.denominator), denominator


def period_by_the_rule(a: int, b: int) -> int:
    """The period by the one-Node Rule3 with the pair, b c_next + r' = a c_now - b c_before + r from (c_before, c_now) = (2 b, a) at the pair's own unit b: the first t with a negative c before it, c_t >= 0 and 4 b c_t^2 >= (2 b + a) c_before_0^2, the nearest integer to 2 pi / omega with no pi (ALGEBRA.md 9.118 item 2 (a))."""
    if b < 1 or not -2 * b < a < 2 * b:
        raise ValueError(f"the clock [{a}, {b}] is no rotation: b from 1 and |a| below 2 b")
    before, now, carry = 2 * b * b, a * b, 0
    start = before
    seen_negative = now < 0
    for t in range(1, RETURN_LIMIT + 1):
        if seen_negative and now >= 0 and 4 * b * now * now >= (2 * b + a) * start * start:
            return t
        total = a * now - b * before + carry
        before, now, carry = now, total // b, total % b
        if now < 0:
            seen_negative = True
    raise ValueError(f"the clock [{a}, {b}] returns within no {RETURN_LIMIT} intervals")


def two_levels(
    profile: np.ndarray, read: np.ndarray, self_coefficient: np.ndarray, wall: int, wrap: Wrap
) -> tuple[np.ndarray, np.ndarray]:
    """The mode's two levels: now the profile, before the read act once more halved, (R S_6(now) + S now) div (2 w), since the mode rotates by 2 cos omega_b (ALGEBRA.md 9.120 item 4 (d))."""
    return profile, (read * six_sum(profile, wrap) + self_coefficient * profile) // (2 * wall)


def conserved_form(
    now: np.ndarray,
    before: np.ndarray,
    self_coefficient: np.ndarray,
    wall: int,
    num: int,
    paces: np.ndarray,
    wrap: Wrap,
) -> Fraction:
    """The record's conserved form, SUM [w (now^2 + before^2) - S now before] / p^2 - 2 num SUM now S_6(before), exact (ALGEBRA.md 9.57 (1))."""
    n, b = now.astype(object), before.astype(object)
    node = wall * (n * n + b * b) - self_coefficient.astype(object) * n * b
    total = Fraction(0)
    for pace in {int(p) for p in paces.ravel()}:
        where = paces == pace
        total += Fraction(int(np.sum(node[where])), pace * pace)
    return total - 2 * num * int(np.sum(n * six_sum(before, wrap).astype(object)))


def scaled_to_norm(
    now: np.ndarray, before: np.ndarray, form: Fraction, norm: Fraction, precision: int
) -> tuple[np.ndarray, np.ndarray]:
    """The two levels scaled together so that the form reaches the norm c T of the body's quanta: the factor the exact square root's floor at the precision (the amplitude unit A), the levels its rational rounding (ALGEBRA.md 9.120 item 4 (d))."""
    if form <= 0 or norm <= 0:
        raise ValueError(f"the form {form} and the norm {norm} are positive")
    ratio = norm / form
    factor = Fraction(isqrt(ratio.numerator * precision * precision // ratio.denominator), precision)
    if factor == 0:
        raise ValueError(
            f"the norm {norm} is below the form's grain {form} at the precision {precision}"
        )
    scale = lambda a: (a.astype(object) * factor.numerator) // factor.denominator  # noqa: E731
    return scale(now).astype(np.int64), scale(before).astype(np.int64)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pair", type=int, nargs=2, required=True, help="the family's pair num den")
    parser.add_argument("--gamma", type=int, required=True, help="the Node clock Gamma")
    parser.add_argument("--box", type=int, nargs=3, required=True, help="the periodic box's shape")
    parser.add_argument("--side", type=int, required=True, help="the counted cube's side at the centre")
    parser.add_argument("--count", type=int, required=True, help="the count per Node of the cube")
    parser.add_argument("--out", type=Path, help="write the profile and its readings as JSON")
    args = parser.parse_args()
    counts = np.zeros(tuple(args.box), dtype=np.int64)
    low = [(n - args.side) // 2 for n in args.box]
    counts[low[0] : low[0] + args.side, low[1] : low[1] + args.side, low[2] : low[2] + args.side] = (
        args.count
    )
    mode = bound_mode(counts, (args.pair[0], args.pair[1]), args.gamma)
    clock = clock_pair(mode.rotation, mode.amplitude)
    reading = {
        "amplitude_unit": mode.amplitude,
        "iterations": mode.iterations,
        "cycle": mode.cycle,
        "rotation": [mode.rotation.numerator, mode.rotation.denominator],
        "clock": list(clock),
        "period": period_by_the_rule(*clock),
        "share_inside_per_mille": (1000 * mode.share_inside.numerator) // mode.share_inside.denominator,
    }
    print(json.dumps(reading))
    if args.out is not None:
        args.out.write_text(
            json.dumps({**reading, "profile": mode.profile.ravel().tolist()}), encoding="utf-8"
        )


if __name__ == "__main__":
    main()
