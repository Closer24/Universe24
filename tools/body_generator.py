"""The generator by Rule3 alone (ALGEBRA.md #the-generator): the held field at rest under its family's pair (the division act iterated with the remainder carried, the body's Nodes rewritten to the count, the stop at the first repeat of levels and remainders), a body's bound mode on that content by Rule3's read act iterated with the before-coefficient 0 and its division act to the amplitude unit, the stop at the first repeat of the integer profile, the two levels, the clock as an exact pair, the period by the one-Node rule and the amplitude from the count and the family's quantum norm; every act one call of core.rule3, integers and exact rationals only."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from fractions import Fraction
from math import isqrt
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import coefficients, form_term, rule3, rule_total_bound

NO_READ = (0, 0, 0)  # the line with no read
Wrap = tuple[bool, bool, bool]
Pair = tuple[int, int]
PERIODIC: Wrap = (True, True, True)
Triple = tuple[int, int, int]  # (a, b, c) with a^2 + b^2 = c^2: cos k = a / c, sin k = b / c, exact
AT_REST: Triple = (1, 0, 1)


@dataclass(frozen=True)
class BoundMode:
    """The generator's output for one body: the integer profile at the amplitude unit A, A itself (derived), the iterations to the repeat, the cycle's length, the rotation 2 cos omega_b as an exact fraction and the share of the profile's weight inside the counted Nodes (ALGEBRA.md 9.120 item 4)."""

    profile: np.ndarray
    amplitude: int
    iterations: int
    cycle: int
    rotation: Fraction
    share_inside: Fraction


@dataclass(frozen=True)
class FieldAtRest:
    """The held field at rest around the body under its family's pair: the levels (the nearest integers), the fine levels at the derived unit, the unit, the iterations to the repeat and the cycle's length, 1 at a fixed point (ALGEBRA.md #the-generator (g))."""

    levels: np.ndarray
    fine: np.ndarray
    unit: int
    iterations: int
    cycle: int


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


def check_counts(counts: np.ndarray, gamma: int) -> None:
    """The refusals by name: the counts an int64 array of nonnegative integers below Gamma, at least one nonzero (ALGEBRA.md 9.108 item 12, the guard's lower side)."""
    if counts.dtype != np.int64 or counts.size == 0 or not counts.any():
        raise ValueError("the counts are an int64 array (integers only), not zero everywhere: no body")
    low, high = int(counts.min()), int(counts.max())
    if low < 0 or high >= gamma:
        raise ValueError(
            f"a count {low if low < 0 else high}: the counts stay in [0, Gamma) with Gamma = {gamma}"
        )


def amplitude_unit(pair: tuple[int, int], gamma: int, counts: np.ndarray) -> int:
    """The amplitude unit A, derived and never written: the largest amplitude at which Rule3's total stays inside the integer width at every content of the region, (M - w) div (6 R + |S| + w) at the content whose coefficients are largest, M the width, checked against rule_total_bound (ALGEBRA.md 9.120 item 4 (b); 9.57 (2))."""
    num, den = pair
    found = None
    for content in sorted({int(c) for c in counts.ravel()}):
        reads, self_coefficient, wall = coefficients(num, den, gamma, content)
        amplitude = (MAX_WORK_INT - wall) // (6 * abs(reads[0]) + abs(self_coefficient) + wall)
        inside = rule_total_bound(num, den, gamma, content, amplitude, True) <= MAX_WORK_INT
        if not inside or rule_total_bound(num, den, gamma, content, amplitude + 1, True) <= MAX_WORK_INT:
            raise ValueError(f"A = {amplitude} at the content {content} is not the width's edge")
        found = amplitude if found is None else min(found, amplitude)
    if found is None or found < 1:
        raise ValueError(f"no amplitude unit keeps Rule3's total inside the width at Gamma = {gamma}")
    return int(found)


def field_at_rest(counts: np.ndarray, pair: Pair, wrap: Wrap = PERIODIC) -> FieldAtRest:
    """The held family's field at rest under its own line at the pace 1 (ALGEBRA.md #the-line; #the-generator (g)): a stands where 6 den a = num S_6(a), so from nothing b <- num S_6(b) div (6 den) by Rule3's division act on the levels at the fine unit (the counts times the unit at the body's Nodes, rewritten each time: the hold); the map is monotone from nothing, so the levels rise to a fixed point, the stop at its first repeat (exact, no tolerance); the fixed point is below the line's own by less than one fine unit per Node, so the levels, the nearest integers by the division act, are the rest within one unit."""
    check_counts(counts, 1 + int(counts.max()))
    num, den = pair
    if num < 1 or den < num:
        raise ValueError(f"the field's pair [{num}, {den}] has num from 1 and den from num")
    unit = field_unit(counts, num)
    hold = counts > 0
    fine = np.zeros(counts.shape, dtype=np.int64)
    seen: dict[bytes, int] = {}
    step = 0
    key = hashlib.sha256(fine.tobytes()).digest()
    while key not in seen:
        seen[key] = step
        fine = np.asarray(rule3((num, num, num), arrivals(fine, wrap), 0, 6 * den, fine, 0, 0, 1)[0])
        fine[hold] = counts[hold] * unit
        step += 1
        key = hashlib.sha256(fine.tobytes()).digest()
    half = int(division(1, 2, np.array(unit, dtype=object)))
    levels = np.asarray(rule3(NO_READ, NO_READ, 1, unit, fine, 0, half, 1)[0])
    return FieldAtRest(levels, fine, unit, step, step - seen[key])


def rule_integers(pair: Pair, gamma: int, counts: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    """Rule3's integers at every Node from the pace p = Gamma - c: the read R = 2 p^2 num, the self coefficient S and the wall w = 6 den Gamma^2 (ALGEBRA.md 9.57 (1))."""
    reads, self_coefficient, wall = coefficients(pair[0], pair[1], gamma, counts)
    return np.asarray(reads[0], dtype=np.int64), np.asarray(self_coefficient, dtype=np.int64), int(wall)


def axis_arrivals(a: np.ndarray, axis: int, wrap: Wrap) -> np.ndarray:
    """The two neighbours' levels summed along one axis at every Node: the row itself twice on an axis of one layer, 0 beyond a closed face (the receive of ALGEBRA.md 9.57 (1))."""
    if a.shape[axis] == 1:
        return 2 * a
    total = np.zeros_like(a)
    for sign in (1, -1):
        shifted = np.roll(a, sign, axis=axis)
        if not wrap[axis]:
            edge: list[slice | int] = [slice(None)] * 3
            edge[axis] = 0 if sign == 1 else -1
            shifted[tuple(edge)] = 0
        total += shifted
    return total


def arrivals(a: np.ndarray, wrap: Wrap) -> tuple[np.ndarray, ...]:
    """The six arrivals as Rule3 reads them, one sum per axis."""
    return tuple(axis_arrivals(a, axis, wrap) for axis in range(3))


def read_act(
    levels: tuple[np.ndarray, ...],
    per_level: tuple[tuple[np.ndarray, ...], ...],
    read: np.ndarray,
    self_coefficient: np.ndarray,
    wall: int,
) -> tuple[np.ndarray, ...]:
    """Rule3's read act with the before-coefficient 0 on each level, (R x its arrivals + S a) div w at every Node, one call of rule3 per level with the level as now and nothing before; the total at the Node's own coefficients kept inside int64 or refused by name (ALGEBRA.md 9.120 item 4 (b); 9.119 item 1; 9.57 (2))."""
    size = max(int(np.abs(level).max()) for level in levels)
    reach = int(np.max(6 * np.abs(read) + np.abs(self_coefficient))) * size
    if reach > MAX_WORK_INT:
        raise ValueError(
            f"the read act reaches {reach} at the level {size}, beyond int64 {MAX_WORK_INT}"
        )
    reads = (read, read, read)
    return tuple(
        np.asarray(rule3(reads, arrived, self_coefficient, wall, level, 0, 0)[0])
        for level, arrived in zip(levels, per_level, strict=True)
    )


def division(numerator_coefficient: Any, wall: Any, level: np.ndarray) -> np.ndarray:
    """Rule3's division act on a level: (coefficient x level) div wall, the line with no read, the coefficient as the self coefficient and the remainder not kept (ALGEBRA.md 9.119 item 1 (c))."""
    return np.asarray(rule3(NO_READ, NO_READ, numerator_coefficient, wall, level, 0, 0)[0])


def field_unit(counts: np.ndarray, num: int) -> int:
    """The field's fine unit, derived and never written: the largest scale of the levels at which num S_6 stays inside the integer width with room, the width div (2 x 6 num x the largest count)."""
    return int(division(1, 2 * 6 * num * int(counts.max()), np.array(MAX_WORK_INT, dtype=object)))


def to_amplitude(levels: tuple[np.ndarray, ...], amplitude: int) -> tuple[np.ndarray, ...]:
    """Rule3's division act to the amplitude unit on the levels together, a x A div max|a| by the largest size over them, the product inside int64 or refused (ALGEBRA.md 9.120 item 4 (b))."""
    size = max(int(np.abs(level).max()) for level in levels)
    if size == 0 or size * amplitude > MAX_WORK_INT:
        raise ValueError(
            f"the division act at the size {size} and A = {amplitude}: no mode, or beyond int64"
        )
    return tuple(division(amplitude, size, level) for level in levels)


def turned(re: np.ndarray, im: np.ndarray, c: Any, s: Any, d: Any) -> tuple[np.ndarray, np.ndarray]:
    """The rotation act on a pair by the triple (c, s, d): (c re - s im) div d and (s re + c im) div d, two of Rule3's read acts with the coefficients (c, -s) and (s, c) on the two parts (ALGEBRA.md 9.81 (2) (c))."""
    return (
        np.asarray(rule3((c, -s, 0), (re, im, 0), 0, d, 0, 0, 0)[0]),
        np.asarray(rule3((s, c, 0), (re, im, 0), 0, d, 0, 0, 0)[0]),
    )


def rotated(re: np.ndarray, im: np.ndarray, triple: Triple, sign: int) -> tuple[np.ndarray, np.ndarray]:
    """The rotation act by k per Link on a level's two parts, (re + i im) x (a + i sign b) div c (ALGEBRA.md 9.120 item 4 (e))."""
    a, b, c = triple
    return turned(re, im, a, sign * b, c)


def twisted_arrivals(
    re: np.ndarray, im: np.ndarray, triple: Triple, wrap: Wrap
) -> tuple[tuple[np.ndarray, ...], ...]:
    """The six arrivals per axis on the moving body's envelope: the two along x rotated by +k and -k per Link (the rotation act), the four across as at rest (ALGEBRA.md 9.120 item 4 (e))."""
    if re.shape[0] == 1:
        along = (2 * re, 2 * im)
    else:
        ahead = rotated(np.roll(re, -1, axis=0), np.roll(im, -1, axis=0), triple, 1)
        behind = rotated(np.roll(re, 1, axis=0), np.roll(im, 1, axis=0), triple, -1)
        if not wrap[0]:
            ahead[0][-1] = ahead[1][-1] = 0
            behind[0][0] = behind[1][0] = 0
        along = (ahead[0] + behind[0], ahead[1] + behind[1])
    return tuple(
        (along[k], axis_arrivals(part, 1, wrap), axis_arrivals(part, 2, wrap))
        for k, part in enumerate((re, im))
    )


def rotation_and_share(
    levels: tuple[np.ndarray, ...],
    totals: tuple[np.ndarray, ...],
    wall: int,
    counts: np.ndarray,
    gamma: int,
    pair: tuple[int, int],
    where: str,
    content: np.ndarray | None = None,
) -> tuple[Fraction, Fraction]:
    """2 cos omega_b of a profile as the exact quotient of the symmetric form, SUM a (R S_6(a) + S a) / p^2 over w SUM a^2 / p^2, a reading of the levels and their read acts with the weights 1 / p_i^2, and the share of the profile's weight inside the counted Nodes; refused by name where the rotation does not rise above the band's top 2 num / den or the share is not twice the counted Nodes' fraction of the box, the band's uniform wave (ALGEBRA.md 9.57 (1), 9.120 item 2)."""
    paces = gamma - (counts if content is None else content)
    numerator, denominator = Fraction(0), Fraction(0)
    for pace in {int(p) for p in paces.ravel()}:
        at = paces == pace
        for level, total in zip(levels, totals, strict=True):
            numerator += Fraction(int(np.sum(level[at] * total[at])), pace * pace)
            denominator += Fraction(int(np.sum(level[at] * level[at])), pace * pace)
    rotation = numerator / (wall * denominator)
    weights = sum(level * level for level in levels)
    share = Fraction(int(np.sum(weights[counts > 0])), int(np.sum(weights)))
    fraction = Fraction(int(np.count_nonzero(counts)), counts.size)
    if rotation <= Fraction(2 * pair[0], pair[1]) or share <= 2 * fraction:
        raise ValueError(
            f"the count binds no {where} of the family [{pair[0]}, {pair[1]}]: the rotation {rotation} "
            f"against the band's top {Fraction(2 * pair[0], pair[1])}, the share inside the counted "
            f"Nodes {share} against their fraction {fraction} of the box, not twice it (ALGEBRA.md 9.120 item 2)"
        )
    return rotation, share


def bound_mode(
    counts: np.ndarray, pair: Pair, gamma: int, wrap: Wrap = PERIODIC, content: np.ndarray | None = None
) -> BoundMode:
    """The bound mode of the well at the derived amplitude unit: from a flat start the read act and the division act iterated until the integer profile repeats, the map on a finite set needing no limit; the well is the content at every Node, the held field at rest where given (ALGEBRA.md #the-generator (c), (g)), the counts alone otherwise."""
    check_counts(counts, gamma)
    if content is None:
        content = counts
    else:
        check_counts(content, gamma)
    amplitude = amplitude_unit(pair, gamma, content)
    read, self_coefficient, wall = rule_integers(pair, gamma, content)
    a = np.full(counts.shape, amplitude, dtype=np.int64)
    seen: dict[bytes, int] = {}
    step = 0
    while a.tobytes() not in seen:
        seen[a.tobytes()] = step
        (a,) = to_amplitude(
            read_act((a,), (arrivals(a, wrap),), read, self_coefficient, wall), amplitude
        )
        step += 1
    level = a.astype(object)
    total = rule3((read, read, read), arrivals(level, wrap), self_coefficient, 1, level, 0, 0)[0]
    rotation, share = rotation_and_share((level,), (total,), wall, counts, gamma, pair, "mode", content)
    return BoundMode(a, amplitude, step, step - seen[a.tobytes()], rotation, share)


def moving_mode(
    counts: np.ndarray,
    pair: Pair,
    gamma: int,
    triple: Triple,
    wrap: Wrap = PERIODIC,
    content: np.ndarray | None = None,
) -> MovingMode:
    """The bound mode of the well moving along x at the rotation k per Link, at the derived amplitude unit: the same iteration as at rest with the twisted read act, from a flat start, each iterate mirrored (the real part even and the imaginary part odd about the centre, the envelope's one gauge, two division acts), the stop at the first repeat of the two parts; at the triple (1, 0, 1) it is the resting mode; the well the content at every Node, the field at rest where given (ALGEBRA.md #the-generator (e), (g))."""
    check_counts(counts, gamma)
    if content is None:
        content = counts
    else:
        check_counts(content, gamma)
    if triple[2] < 1 or triple[0] ** 2 + triple[1] ** 2 != triple[2] ** 2:
        raise ValueError(
            f"the rotation per Link {triple} is no Pythagorean triple: c from 1 and a^2 + b^2 = c^2"
        )
    if not np.array_equal(content, content[::-1]):
        raise ValueError(
            "the moving body's well is mirrored along x about the box's centre (the gauge of its envelope)"
        )
    amplitude = amplitude_unit(pair, gamma, content)
    read, self_coefficient, wall = rule_integers(pair, gamma, content)
    re = np.full(counts.shape, amplitude, dtype=np.int64)
    im = np.zeros(counts.shape, dtype=np.int64)
    seen: dict[bytes, int] = {}
    step = 0
    while re.tobytes() + im.tobytes() not in seen:
        seen[re.tobytes() + im.tobytes()] = step
        re, im = to_amplitude(
            read_act((re, im), twisted_arrivals(re, im, triple, wrap), read, self_coefficient, wall),
            amplitude,
        )
        re, im = division(1, 2, re + re[::-1]), division(1, 2, im - im[::-1])
        step += 1
    levels = (re.astype(object), im.astype(object))
    arrivals_re, arrivals_im = twisted_arrivals(levels[0], levels[1], triple, wrap)
    reads = (read, read, read)
    totals = (
        rule3(reads, arrivals_re, self_coefficient, 1, levels[0], 0, 0)[0],
        rule3(reads, arrivals_im, self_coefficient, 1, levels[1], 0, 0)[0],
    )
    rotation, share = rotation_and_share(
        levels, totals, wall, counts, gamma, pair, f"moving mode at {triple}", content
    )
    return MovingMode(re, im, amplitude, step, step - seen[re.tobytes() + im.tobytes()], rotation, share)


def moving_levels(mode: MovingMode, triple: Triple) -> tuple[np.ndarray, np.ndarray]:
    """The moving body's two real levels: now the envelope times cos(k x) per Link (the rotation act along x), before the same one interval earlier, cos omega_b(k) now - sin omega_b(k) x the quarter-turned part as one read act over the common denominator, sin from the exact cosine by the division act to the amplitude unit and the integer square root (ALGEBRA.md 9.120 item 4 (e); 9.113 item 3 (c))."""
    re, im, amplitude = mode.re.copy(), mode.im.copy(), mode.amplitude
    phase_re, phase_im = (
        np.full(re.shape[1:], amplitude, dtype=np.int64),
        np.zeros(re.shape[1:], dtype=np.int64),
    )
    now_re = np.empty_like(re)
    now_im = np.empty_like(im)
    for x in range(re.shape[0]):
        now_re[x], now_im[x] = turned(re[x], im[x], phase_re, phase_im, amplitude)
        phase_re, phase_im = rotated(phase_re, phase_im, triple, 1)
    cosine = mode.rotation / 2
    square = (1 - cosine * cosine) * amplitude * amplitude
    sine = isqrt(int(division(square.numerator, square.denominator, np.array(1, dtype=object))))
    p, q = cosine.numerator, cosine.denominator
    before, _ = turned(
        now_re.astype(object), now_im.astype(object), p * amplitude, q * sine, q * amplitude
    )
    return now_re, before.astype(np.int64)


def clock_pair(rotation: Fraction, denominator: int) -> tuple[int, int]:
    """The clock [a, b] with 2 cos omega_b = a / b on the denominator given (the amplitude unit A, the mode's resolution), a the nearest integer by the division act with the load d over the wall 2 d."""
    scaled = rotation * denominator
    nearest = rule3(
        NO_READ, NO_READ, 2, 2 * scaled.denominator, scaled.numerator, 0, scaled.denominator
    )[0]
    return int(nearest), denominator


def period_by_the_rule(a: int, b: int) -> int:
    """The period by the one-Node Rule3 with the pair, b c_next + r' = a c_now - b c_before + r from (c_before, c_now) = (2 b, a) at the pair's own unit b, each interval one call of rule3: the first t with a negative c before it, c_t >= 0 and 4 b c_t^2 >= (2 b + a) c_before_0^2, the nearest integer to 2 pi / omega with no pi; the longest period a pair on b allows is 2 pi sqrt(b), at the rotation nearest 0, so a clock not back within 8 sqrt(b) + 8 intervals is refused by name (ALGEBRA.md 9.118 item 2 (a))."""
    if b < 1 or not -2 * b < a < 2 * b:
        raise ValueError(f"the clock [{a}, {b}] is no rotation: b from 1 and |a| below 2 b")
    before, now, carry = 2 * b * b, a * b, 0
    start = before
    seen_negative = now < 0
    longest = 8 * isqrt(b) + 8
    for t in range(1, longest + 1):
        if seen_negative and now >= 0 and 4 * b * now * now >= (2 * b + a) * start * start:
            return t
        before, (now, carry) = now, rule3(NO_READ, NO_READ, a, b, now, before, carry)
        if now < 0:
            seen_negative = True
    raise ValueError(
        f"the clock [{a}, {b}] returns within no {longest} intervals, the longest a pair on {b} allows"
    )


def two_levels(
    profile: np.ndarray, read: np.ndarray, self_coefficient: np.ndarray, wall: int, wrap: Wrap
) -> tuple[np.ndarray, np.ndarray]:
    """The mode's two levels: now the profile, before the read act once more halved, (R S_6(now) + S now) div (2 w), since the mode rotates by 2 cos omega_b (ALGEBRA.md 9.120 item 4 (d))."""
    return profile, rule3(
        (read, read, read), arrivals(profile, wrap), self_coefficient, 2 * wall, profile, 0, 0
    )[0]


def conserved_form(
    now: np.ndarray,
    before: np.ndarray,
    self_coefficient: np.ndarray,
    wall: int,
    num: int,
    paces: np.ndarray,
    wrap: Wrap,
) -> Fraction:
    """The record's conserved form, SUM [w (now^2 + before^2) - S now before] / p^2 - 2 num SUM now S_6(before), the form's Node term of core.rule3 with the plain current on the Links, exact (ALGEBRA.md 9.57 (1))."""
    n, b = now.astype(object), before.astype(object)
    node = form_term(self_coefficient.astype(object), wall, n, b)
    total = Fraction(0)
    for pace in {int(p) for p in paces.ravel()}:
        where = paces == pace
        total += Fraction(int(np.sum(node[where])), pace * pace)
    return total - 2 * num * int(np.sum(n * sum(arrivals(b, wrap))))


def scaled_to_norm(
    now: np.ndarray, before: np.ndarray, form: Fraction, norm: Fraction, precision: int
) -> tuple[np.ndarray, np.ndarray]:
    """The two levels scaled together so that the form reaches the norm c T of the body's quanta: the factor the integer square root of the ratio's division act at the precision (the amplitude unit A), the levels by the division act with the factor as a pair (ALGEBRA.md 9.120 item 4 (d))."""
    if form <= 0 or norm <= 0:
        raise ValueError(f"the form {form} and the norm {norm} are positive")
    ratio = norm / form
    squared = division(
        ratio.numerator * precision * precision, ratio.denominator, np.array(1, dtype=object)
    )
    factor = Fraction(isqrt(int(squared)), precision)
    if factor == 0:
        raise ValueError(
            f"the norm {norm} is below the form's grain {form} at the precision {precision}"
        )
    return (
        division(factor.numerator, factor.denominator, now.astype(object)).astype(np.int64),
        division(factor.numerator, factor.denominator, before.astype(object)).astype(np.int64),
    )


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]


def read_document(value: str) -> Any:
    """A JSON document at a repository path (or an absolute one), refused by name where there is no file."""
    path = Path(value) if Path(value).is_absolute() else REPOSITORY_ROOT / value
    if not path.is_file():
        raise ValueError(f"no file at {value!r} (a repository path)")
    return json.loads(path.read_text(encoding="utf-8"))


def pair_of(row: dict[str, Any], label: str) -> Pair:
    """A family's pair from its row of the universe file, [num, den]; a row whose pair is the body's word is refused: the law's form declares no pair on a body."""
    pair = row.get("pair")
    if not (isinstance(pair, list) and len(pair) == 2 and all(isinstance(v, int) for v in pair)):
        raise ValueError(
            f"{label}: the row's pair is {pair!r}, not [num, den]; the generator takes the family's"
        )
    return int(pair[0]), int(pair[1])


def generate(document: dict[str, Any]) -> dict[str, Any]:
    """The generator on its input file, a world file in the law's form (ALGEBRA.md #the-generator): the GameBoard's shape and faces, the Node clock, the universe file it names (the families' rows: the body's family's pair and reads, the held families' pairs, the integers by name) and one body written by its Nodes with their counts; the held fields the body's family reads plainly at rest under their rows' pairs, the mode on their weighted sum, the readings; no number in the tool or on the command line."""
    shape = tuple(int(n) for n in document["shape"])
    faces = document["boundary"]
    wrap = tuple(
        (faces if isinstance(faces, dict) else {a: faces for a in "xyz"})[axis] == "periodic"
        for axis in "xyz"
    )
    gamma = int(document["node_clock"])
    universe = read_document(document["universe"])
    rows = {row["name"]: row for row in universe["families"]}
    integers = universe.get("integers", {})
    bodies = [
        body for body in document.get("measured", []) if isinstance(body, dict) and "nodes" in body
    ]
    if len(bodies) != 1:
        raise ValueError(
            f"the generator takes one body in the law's form (its nodes with their counts), found {len(bodies)}"
        )
    body = bodies[0]
    if any(int(v) for v in body.get("momentum", (0, 0, 0))):
        raise ValueError(
            "a moving body's k by bisection on the pairs is not in the tool yet: the momentum is 0 here"
        )
    counts = np.zeros(shape, dtype=np.int64)
    for entry in body["nodes"]:
        counts[tuple(int(v) for v in entry["node"])] = int(entry["count"])
    row = rows[body["family"]]
    pair = pair_of(row, f"the family {body['family']!r}")
    content = np.zeros(shape, dtype=np.int64)
    rests: dict[str, Any] = {}
    for read in row.get("reads", []):
        if read.get("by") not in (1, "plain"):
            continue  # a read by the charge's sign: the law's form carries no charge, the factor 0
        weight = read["weight"]
        if isinstance(weight, str):
            weight = integers[weight]
        held = rows[read["family"]]
        rest = field_at_rest(counts, pair_of(held, f"the held family {read['family']!r}"), wrap)
        content = content + int(weight) * rest.levels
        rests[read["family"]] = {
            "pair": list(held["pair"]),
            "iterations": rest.iterations,
            "cycle": rest.cycle,
            "at_body": int(rest.levels[counts > 0].min()),
            "at_corner": int(rest.levels[0, 0, 0]),
        }
    mode = bound_mode(counts, pair, gamma, wrap, content)
    clock = clock_pair(mode.rotation, mode.amplitude)
    return {
        "family": body["family"],
        "pair": list(pair),
        "rest": rests,
        "amplitude_unit": mode.amplitude,
        "iterations": mode.iterations,
        "cycle": mode.cycle,
        "rotation": [mode.rotation.numerator, mode.rotation.denominator],
        "clock": list(clock),
        "period": period_by_the_rule(*clock),
        "share_inside": [mode.share_inside.numerator, mode.share_inside.denominator],
        "profile": mode.profile,
        "content": content,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="the world file in the law's form")
    parser.add_argument("--out", type=Path, help="write the readings, the profile and the well as JSON")
    args = parser.parse_args()
    reading = generate(json.loads(args.input.read_text(encoding="utf-8")))
    profile, content = reading.pop("profile"), reading.pop("content")
    print(json.dumps(reading))
    if args.out is not None:
        args.out.write_text(
            json.dumps(
                {**reading, "profile": profile.ravel().tolist(), "content": content.ravel().tolist()}
            )
        )


if __name__ == "__main__":
    main()
