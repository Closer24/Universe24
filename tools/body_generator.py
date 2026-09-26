"""The generator by Rule3 alone (ALGEBRA.md 9.120 item 4): a body's bound mode by Rule3's read act iterated with the before-coefficient 0 and its division act to the amplitude unit, the stop at the first repeat of the integer profile, the two levels, the clock as an exact pair, the period by the one-Node rule and the amplitude from the count and the family's quantum norm; integers and exact rationals only."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path

import numpy as np

from event_universe.core.rule3 import coefficients

INT64_BOUND = (1 << 63) - 1
AMPLITUDE_UNIT = 1 << 20
REPEAT_LIMIT = 1 << 16  # iterations; a host bound on the search for the repeat, not a stop
RETURN_LIMIT = 1 << 24  # intervals; a rotation slower than this is no clock of a run
Wrap = tuple[bool, bool, bool]
PERIODIC: Wrap = (True, True, True)


@dataclass(frozen=True)
class BoundMode:
    """The generator's output for one body: the integer profile at the amplitude unit, the iterations to the repeat, the cycle's length, the rotation 2 cos omega_b as an exact fraction and the share of the profile's weight inside the counted Nodes (ALGEBRA.md 9.120 item 4)."""

    profile: np.ndarray
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
    """Rule3's read act with the before-coefficient 0: (R S_6(a) + S a) div w at every Node, the total kept inside int64 or refused (ALGEBRA.md 9.120 item 4 (b); 9.119 item 1)."""
    size = int(np.abs(a).max())
    reach = 6 * int(np.abs(read).max()) * size + int(np.abs(self_coefficient).max()) * size
    if reach > INT64_BOUND:
        raise ValueError(f"the read act reaches {reach} at the level {size}, beyond int64 {INT64_BOUND}")
    return (read * six_sum(a, wrap) + self_coefficient * a) // wall


def to_amplitude(a: np.ndarray, amplitude: int) -> np.ndarray:
    """Rule3's division act to the amplitude unit: a x A div max|a| (ALGEBRA.md 9.120 item 4 (b))."""
    size = int(np.abs(a).max())
    if size == 0:
        raise ValueError("the read act gives 0 at every Node: no mode")
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
    amplitude: int = AMPLITUDE_UNIT,
    wrap: Wrap = PERIODIC,
) -> BoundMode:
    """The bound mode of the count's well: from a flat start the read act and the division act iterated until the integer profile repeats; refused by name where the rotation does not rise above the band's top 2 num / den or the profile's weight inside the counted Nodes is not twice their fraction of the box, the band's uniform wave (ALGEBRA.md 9.120 items 2 and 4)."""
    check_counts(counts, gamma)
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
    return BoundMode(a, step, step - seen[key], rotation, share)


def clock_pair(rotation: Fraction, denominator: int = AMPLITUDE_UNIT) -> tuple[int, int]:
    """The clock [a, b] with 2 cos omega_b = a / b on the declared denominator, a the nearest integer (exact rational rounding)."""
    scaled = rotation * denominator
    return (2 * scaled.numerator + scaled.denominator) // (2 * scaled.denominator), denominator


def period_by_the_rule(a: int, b: int) -> int:
    """The period by the one-Node Rule3 with the pair, b c_next + r' = a c_now - b c_before + r from (c_before, c_now) = (2 b, a) at the amplitude unit: the first t with a negative c before it, c_t >= 0 and 4 b c_t^2 >= (2 b + a) c_before_0^2, the nearest integer to 2 pi / omega with no pi (ALGEBRA.md 9.118 item 2 (a))."""
    if b < 1 or not -2 * b < a < 2 * b:
        raise ValueError(f"the clock [{a}, {b}] is no rotation: b from 1 and |a| below 2 b")
    before, now, carry = 2 * b * AMPLITUDE_UNIT, a * AMPLITUDE_UNIT, 0
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
    now: np.ndarray, before: np.ndarray, form: Fraction, norm: Fraction, precision: int = AMPLITUDE_UNIT
) -> tuple[np.ndarray, np.ndarray]:
    """The two levels scaled together so that the form reaches the norm c T of the body's quanta: the factor the exact square root's floor at the precision, the levels its rational rounding (ALGEBRA.md 9.120 item 4 (d))."""
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
    clock = clock_pair(mode.rotation)
    reading = {
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
