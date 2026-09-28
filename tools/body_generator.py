"""The generator by Rule3 alone (ALGEBRA.md #the-generator): the held field at rest under its family's pair (the division act iterated with the remainder carried, the body's Nodes rewritten to the count, the stop at the first repeat of levels and remainders), a body's bound mode on that content by Rule3's read act iterated with the before-coefficient 0 and its division act to the amplitude unit, the stop at the first repeat of the integer profile, the two levels, the clock as an exact pair, the period by the one-Node rule and the amplitude from the count and the family's quantum norm; every act one call of core.rule3, integers and exact rationals only."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import dataclass
from fractions import Fraction
from math import acos, cos, isqrt, pi
from pathlib import Path
from typing import Any

import numpy as np

from event_universe.core.integer import MAX_WORK_INT
from event_universe.core.rule3 import coefficients, form_term, rule3, rule_total_bound
from event_universe.features.start import (
    NO_READ,
    PERIODIC,
    FieldAtRest,
    Pair,
    Wrap,
    arrivals,
    axis_arrivals,
    check_counts,
    division,
)
from event_universe.features.start import rest as start_rest
from event_universe.loader.mode import period_by_the_rule
from event_universe.loader.world import load_level
from event_universe.world_files import input_digest

Triple = tuple[int, int, int]  # (a, b, c) with a^2 + b^2 = c^2: cos k = a / c, sin k = b / c, exact
AT_REST: Triple = (1, 0, 1)


@dataclass(frozen=True)
class BoundMode:
    """The generator's output for one body: the integer profile at the amplitude unit A, A itself (derived), the iterations to the repeat, the cycle's length, the rotation 2 cos omega_b as an exact fraction and the share of the profile's weight inside the counted Nodes (ALGEBRA.md #the-stable-body)."""

    profile: np.ndarray
    amplitude: int
    iterations: int
    cycle: int
    rotation: Fraction
    share_inside: Fraction


@dataclass(frozen=True)
class MovingMode:
    """The moving body's envelope at the rotation k per Link: its two parts at the amplitude unit A, A itself (derived), the iterations to the repeat, the cycle's length, the rotation 2 cos omega_b(k) as an exact fraction, the share inside the counted Nodes (ALGEBRA.md #the-stable-body)."""

    re: np.ndarray
    im: np.ndarray
    amplitude: int
    iterations: int
    cycle: int
    rotation: Fraction
    share_inside: Fraction


@dataclass(frozen=True)
class MovingBody:
    """The moving body of ALGEBRA.md #the-generator (e): the resting mode's two levels with the phase k per Link along x, the phase's pair (m, j) found by bisection and its triple, the packet's velocity (its current over its form, exact) against the named one n / (3 Q M), and the rest mode."""

    now: np.ndarray
    before: np.ndarray
    pair: Pair
    triple: Triple
    velocity: Fraction
    named: Fraction
    rest: BoundMode
    top: Fraction


def amplitude_unit(
    pair: tuple[int, int], gamma: int, counts: np.ndarray, bound_level: int | None = None
) -> int:
    """The amplitude unit A, derived and never written: the largest amplitude at which Rule3's total stays inside the integer width at every content of the region, (M - w) div (6 R + |S| + w) at the content whose coefficients are largest, M the width, checked against rule_total_bound (ALGEBRA.md #the-stable-body, #the-line); `bound_level` is the loader's level of the world (`loader_level`), one more content the unit is derived at, so that the written profile stands inside the universe's amplitude bound."""
    num, den = pair
    found = None
    for content in sorted(
        {int(c) for c in counts.ravel()} | ({bound_level} if bound_level is not None else set())
    ):
        reads, self_coefficient, wall = coefficients(num, den, gamma, content)
        amplitude = (MAX_WORK_INT - wall) // (6 * abs(reads[0]) + abs(self_coefficient) + wall)
        inside = rule_total_bound(num, den, gamma, content, amplitude, True) <= MAX_WORK_INT
        if not inside or rule_total_bound(num, den, gamma, content, amplitude + 1, True) <= MAX_WORK_INT:
            raise ValueError(f"A = {amplitude} at the content {content} is not the width's edge")
        found = amplitude if found is None else min(found, amplitude)
    if found is None or found < 1:
        raise ValueError(f"no amplitude unit keeps Rule3's total inside the width at Gamma = {gamma}")
    return int(found)


def rule_integers(pair: Pair, gamma: int, counts: np.ndarray) -> tuple[np.ndarray, np.ndarray, int]:
    """Rule3's integers at every Node from the pace p = Gamma - c: the read R = 2 p^2 num, the self coefficient S and the wall w = 6 den Gamma^2 (ALGEBRA.md #the-line)."""
    reads, self_coefficient, wall = coefficients(pair[0], pair[1], gamma, counts)
    return np.asarray(reads[0], dtype=np.int64), np.asarray(self_coefficient, dtype=np.int64), int(wall)


def read_act(
    levels: tuple[np.ndarray, ...],
    per_level: tuple[tuple[np.ndarray, ...], ...],
    read: np.ndarray,
    self_coefficient: np.ndarray,
    wall: int,
) -> tuple[np.ndarray, ...]:
    """Rule3's read act with the before-coefficient 0 on each level, (R x its arrivals + S a) div w at every Node, one call of rule3 per level with the level as now and nothing before; the total at the Node's own coefficients kept inside int64 or refused by name (ALGEBRA.md #the-stable-body, #the-four-acts, #the-line)."""
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


def to_amplitude(levels: tuple[np.ndarray, ...], amplitude: int) -> tuple[np.ndarray, ...]:
    """Rule3's division act to the amplitude unit on the levels together, a x A div max|a| by the largest size over them, the product inside int64 or refused (ALGEBRA.md #the-stable-body)."""
    size = max(int(np.abs(level).max()) for level in levels)
    if size == 0 or size * amplitude > MAX_WORK_INT:
        raise ValueError(
            f"the division act at the size {size} and A = {amplitude}: no mode, or beyond int64"
        )
    return tuple(division(amplitude, size, level) for level in levels)


def turned(re: np.ndarray, im: np.ndarray, c: Any, s: Any, d: Any) -> tuple[np.ndarray, np.ndarray]:
    """The rotation act on a pair by the triple (c, s, d): (c re - s im) div d and (s re + c im) div d, two of Rule3's read acts with the coefficients (c, -s) and (s, c) on the two parts (ALGEBRA.md #the-transport)."""
    return (
        np.asarray(rule3((c, -s, 0), (re, im, 0), 0, d, 0, 0, 0)[0]),
        np.asarray(rule3((s, c, 0), (re, im, 0), 0, d, 0, 0, 0)[0]),
    )


def rotated(re: np.ndarray, im: np.ndarray, triple: Triple, sign: int) -> tuple[np.ndarray, np.ndarray]:
    """The rotation act by k per Link on a level's two parts, (re + i im) x (a + i sign b) div c (ALGEBRA.md #the-stable-body)."""
    a, b, c = triple
    return turned(re, im, a, sign * b, c)


def twisted_arrivals(
    re: np.ndarray, im: np.ndarray, triple: Triple, wrap: Wrap
) -> tuple[tuple[np.ndarray, ...], ...]:
    """The six arrivals per axis on the moving body's envelope: the two along x rotated by +k and -k per Link (the rotation act), the four across as at rest (ALGEBRA.md #the-stable-body)."""
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
    """2 cos omega_b of a profile as the exact quotient of the symmetric form, SUM a (R S_6(a) + S a) / p^2 over w SUM a^2 / p^2, a reading of the levels and their read acts with the weights 1 / p_i^2, and the share of the profile's weight inside the counted Nodes; refused by name where the rotation does not rise above the band's top 2 num / den or the share is not twice the counted Nodes' fraction of the box, the band's uniform wave (ALGEBRA.md #the-line, #the-stable-body)."""
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
            f"Nodes {share} against their fraction {fraction} of the box, not twice it (ALGEBRA.md #the-stable-body)"
        )
    return rotation, share


def loader_level(document: dict[str, Any], gamma: int) -> int:
    """The level the loader reads its amplitude bound at, by the loader's own function `load_level` (loader/world.py; Cheshbon's lines of 2026-09-28, 00:20Z and 02:05Z; the Closer's word of 05:50 Israel): the families' reads with their weights (a weight named in the universe's integers resolved) and every body's source per family as the loader reads them, its content (its counts' sum with its stocks) or its signed charge (its `q` with the rows' `sign` over its held quanta), twice the largest family's reach, at most Gamma - 1."""
    universe = read_document(document["universe"])
    rows, integers = universe["families"], universe.get("integers", {})
    names = [row["name"] for row in rows]
    reads = [
        [
            (names.index(r["family"]), int(integers.get(r["weight"], r["weight"])))
            for r in row.get("reads", [])
        ]
        for row in rows
    ]
    sources = []
    for body in document["measured"]:
        held = [0] * len(names)
        held[names.index(body["family"])] += sum(int(node["count"]) for node in body.get("nodes", []))
        for name, stock in body.get("stocks", {}).items():
            held[names.index(name)] += int(stock)
        charge = abs(
            int(body.get("q", 0))
            + sum(int(row.get("sign", 0)) * h for row, h in zip(rows, held, strict=True))
        )
        sources.append(
            [charge if (row.get("held") or {}).get("count") == "sign" else sum(held) for row in rows]
        )
    return int(load_level(reads, sources, gamma))


def bound_mode(
    counts: np.ndarray,
    pair: Pair,
    gamma: int,
    wrap: Wrap = PERIODIC,
    content: np.ndarray | None = None,
    bound_level: int | None = None,
) -> BoundMode:
    """The bound mode of the well at the derived amplitude unit: from a flat start the read act and the division act iterated until the integer profile repeats, the map on a finite set needing no limit; the well is the content at every Node, the held field at rest where given (ALGEBRA.md #the-generator (c), (g)), the counts alone otherwise."""
    check_counts(counts, gamma)
    if content is None:
        content = counts
    else:
        check_counts(content, gamma)
    amplitude = amplitude_unit(pair, gamma, content, bound_level)
    read, self_coefficient, wall = rule_integers(pair, gamma, content)
    a = np.full(counts.shape, amplitude, dtype=np.int64)
    seen: dict[bytes, int] = {}  # the iterates by their digest: the repeat found, the memory bounded
    step = 0
    while hashlib.sha256(a.tobytes()).digest() not in seen:
        seen[hashlib.sha256(a.tobytes()).digest()] = step
        (a,) = to_amplitude(
            read_act((a,), (arrivals(a, wrap),), read, self_coefficient, wall), amplitude
        )
        step += 1
    level = a.astype(object)
    total = rule3((read, read, read), arrivals(level, wrap), self_coefficient, 1, level, 0, 0)[0]
    rotation, share = rotation_and_share((level,), (total,), wall, counts, gamma, pair, "mode", content)
    return BoundMode(
        a, amplitude, step, step - seen[hashlib.sha256(a.tobytes()).digest()], rotation, share
    )


def moving_mode(
    counts: np.ndarray,
    pair: Pair,
    gamma: int,
    triple: Triple,
    wrap: Wrap = PERIODIC,
    content: np.ndarray | None = None,
    bound_level: int | None = None,
) -> MovingMode:
    """The bound mode of the well moving along x at the rotation k per Link, at the derived amplitude unit: the same iteration as at rest with the twisted read act, from a flat start, each iterate mirrored (the real part even and the imaginary part odd about the centre, the envelope's one gauge, two division acts), the stop at the first repeat of the two parts; at the triple (1, 0, 1) it is the resting mode; the well the content at every Node, the field at rest where given; a diagnostic: the twisted read is a gauge of the plain one, so this fixed point is the rest mode times a phase (ALGEBRA.md #the-generator (e): the moving body is moving_body)."""
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
    amplitude = amplitude_unit(pair, gamma, content, bound_level)
    read, self_coefficient, wall = rule_integers(pair, gamma, content)
    re = np.full(counts.shape, amplitude, dtype=np.int64)
    im = np.zeros(counts.shape, dtype=np.int64)
    seen: dict[bytes, int] = {}  # by the digest of the two parts
    step = 0
    while hashlib.sha256(re.tobytes() + im.tobytes()).digest() not in seen:
        seen[hashlib.sha256(re.tobytes() + im.tobytes()).digest()] = step
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
    cycle = step - seen[hashlib.sha256(re.tobytes() + im.tobytes()).digest()]
    return MovingMode(re, im, amplitude, step, cycle, rotation, share)


def moving_levels(mode: MovingMode, triple: Triple) -> tuple[np.ndarray, np.ndarray]:
    """The moving body's two real levels: now the envelope times cos(k x) per Link (the rotation act along x), before the same one interval earlier, cos omega_b(k) now - sin omega_b(k) x the quarter-turned part as one read act over the common denominator, sin from the exact cosine by the division act to the amplitude unit and the integer square root (ALGEBRA.md #the-stable-body, #the-primitives)."""
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


def triple_of(pair: Pair) -> Triple:
    """The Pythagorean triple of the phase's pair (m, j): (m^2 - j^2, 2 m j, m^2 + j^2), cos k = (m^2 - j^2) / (m^2 + j^2) exact, k from 0 at j = 0 to a quarter turn at j = m; refused by name outside 0 <= j <= m with m from 1 (ALGEBRA.md #the-generator (e))."""
    m, j = pair
    if m < 1 or j < 0 or j > m:
        raise ValueError(f"the phase's pair (m, j) = {pair}: m from 1 and j from 0 to m")
    return (m * m - j * j, 2 * m * j, m * m + j * j)


def packet_current(now: np.ndarray, before: np.ndarray, num: int, wrap: Wrap) -> int:
    """The packet's own current along x toward +x: SUM over the Links i to i + 1 of -F_ij, F_ij = num x (now_i before_j - before_i now_j) the law's current with the family's num as its weight (ALGEBRA.md #the-current: a wave travelling from i to j has F_ij below 0); the Link across the faces only between periodic ones."""
    n, b = now.astype(object), before.astype(object)
    flow = b * np.roll(n, -1, axis=0) - n * np.roll(b, -1, axis=0)
    if not wrap[0]:
        flow[-1] = 0
    return num * int(flow.sum())


def packet_velocity(
    rest: BoundMode,
    triple: Triple,
    num: int,
    self_coefficient: np.ndarray,
    wall: int,
    paces: np.ndarray,
    wrap: Wrap,
) -> tuple[Fraction, np.ndarray, np.ndarray]:
    """The packet at the phase k per Link of the triple: the resting mode's envelope with the phase (moving_levels, no twisted fixed point) and its velocity, the current over the conserved form, the law's equality SUM F = T n / (3 Q) divided by the packet's form M T, so C / form = v exact (ALGEBRA.md #the-generator (e))."""
    envelope = MovingMode(
        rest.profile,
        np.zeros_like(rest.profile),
        rest.amplitude,
        rest.iterations,
        rest.cycle,
        rest.rotation,
        rest.share_inside,
    )
    now, before = moving_levels(envelope, triple)
    form = conserved_form(now, before, self_coefficient, wall, num, paces, wrap)
    return Fraction(packet_current(now, before, num, wrap)) / form, now, before


def moving_body(
    counts: np.ndarray,
    pair: Pair,
    gamma: int,
    momentum: int,
    momentum_unit: int,
    denominator: int,
    wrap: Wrap = PERIODIC,
    content: np.ndarray | None = None,
    rest: BoundMode | None = None,
    bound_level: int | None = None,
) -> MovingBody:
    """The body along x, at rest and in motion one primitive (ALGEBRA.md #the-generator (e); the owner's word): the momentum n names the velocity v = n / (3 Q M), Q the universe's momentum unit and M the body's quanta (the counts' sum); the phase's pair (m, j), m the body's declared denominator, j by bisection from 0 to m on the packet's velocity, which rises with k, to the j whose velocity is nearest the named one, the phase's sense the momentum's sign; at the momentum 0 the pair is (m, 0), the phase's triple (1, 0, 1) and the two levels the resting mode's, no bisection; refused by name where the named velocity is beyond the packet's at j = m (a quarter turn per Link)."""
    if momentum_unit < 1 or denominator < 1:
        raise ValueError(
            f"the momentum unit Q = {momentum_unit} and the phase's denominator m = {denominator} are from 1"
        )
    if rest is None:
        rest = bound_mode(counts, pair, gamma, wrap, content, bound_level)
    well = counts if content is None else content
    named = Fraction(momentum, 3 * momentum_unit * int(counts.sum()))
    read, self_coefficient, wall = rule_integers(pair, gamma, well)
    paces = gamma - well
    sense = 1 if momentum >= 0 else -1

    def at(j: int) -> tuple[Fraction, np.ndarray, np.ndarray]:
        a, b, c = triple_of((denominator, j))
        return packet_velocity(rest, (a, sense * b, c), pair[0], self_coefficient, wall, paces, wrap)

    found = {0: at(0)}
    if momentum == 0:
        return MovingBody(
            found[0][1], found[0][2], (denominator, 0), AT_REST, found[0][0], named, rest, Fraction(0)
        )
    found[denominator] = at(denominator)
    if abs(found[denominator][0]) < abs(named):
        raise ValueError(
            f"the momentum {momentum} names the velocity {named}, beyond the packet's "
            f"{found[denominator][0]} at a quarter turn per Link (m = {denominator})"
        )
    low, high = 0, denominator
    while high - low > 1:
        middle = int(division(1, 2, np.array(low + high, dtype=object)))
        found[middle] = at(middle)
        if abs(found[middle][0]) <= abs(named):
            low = middle
        else:
            high = middle
    j = low if abs(named) - abs(found[low][0]) <= abs(found[high][0]) - abs(named) else high
    velocity, now, before = found[j]
    a, b, c = triple_of((denominator, j))
    top = abs(found[denominator][0])
    return MovingBody(now, before, (denominator, j), (a, sense * b, c), velocity, named, rest, top)


def wavelength_of(clock: tuple[int, int], given_pair: Pair) -> int | None:
    """The given record's wavelength lambda_q of a giver's mode on the given family's band (ALGEBRA.md #the-primitives, the recoil's row; #the-rows-against-nature (g)): cos k = 3 cos omega_b den / num - 2 along one axis with 2 cos omega_b = a / b the mode's clock and [num, den] the given record's pair, k by the host's arc cosine as the twist's, 2 pi / k to the nearest whole Link; None where the band does not hold the rotation (no wave of that band at the giver's rotation)."""
    cosine = 3 * clock[0] * given_pair[1] / (2 * clock[1] * given_pair[0]) - 2
    if not -1 < cosine < 1:
        return None
    return max(1, round(2 * pi / acos(cosine)))


def clock_pair(rotation: Fraction, denominator: int) -> tuple[int, int]:
    """The clock [a, b] with 2 cos omega_b = a / b on the denominator given (the amplitude unit A, the mode's resolution), a the nearest integer by the division act with the load d over the wall 2 d."""
    scaled = rotation * denominator
    nearest = rule3(
        NO_READ, NO_READ, 2, 2 * scaled.denominator, scaled.numerator, 0, scaled.denominator
    )[0]
    return int(nearest), denominator


def proper_rotation(rotation: Fraction, triple: Triple, top: Fraction) -> Fraction:
    """The packet's rotation at its moving centre, 2 cos(Omega(k)) with Omega(k) = omega(k) - k omega'(k) on the body's own bound band omega(k) = omega_0 + Delta (1 - cos k), omega_0 the rest rotation's angle and Delta the packet's top velocity at a quarter turn per Link, k the phase per Link of the triple; the loader's proper pair of a moving body, the angles by the host's arc cosine as the twist's (ALGEBRA.md #the-rows-against-nature (e), #the-generator (e), #the-velocity)."""
    omega_0 = acos(float(rotation) / 2)
    cos_k, sin_k = triple[0] / triple[2], abs(triple[1]) / triple[2]
    k = acos(cos_k)
    return Fraction(2 * cos(omega_0 + float(top) * (1 - cos_k) - k * float(top) * sin_k))


def two_levels(
    profile: np.ndarray, read: np.ndarray, self_coefficient: np.ndarray, wall: int, wrap: Wrap
) -> tuple[np.ndarray, np.ndarray]:
    """The mode's two levels: now the profile, before the read act once more halved, (R S_6(now) + S now) div (2 w), since the mode rotates by 2 cos omega_b (ALGEBRA.md #the-stable-body)."""
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
    """The record's conserved form, SUM [w (now^2 + before^2) - S now before] / p^2 - 2 num SUM now S_6(before), the form's Node term of core.rule3 with the plain current on the Links, exact (ALGEBRA.md #the-line)."""
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
    """The two levels scaled together so that the form reaches the norm c T of the body's quanta: the factor the integer square root of the ratio's division act at the precision (the amplitude unit A), the levels by the division act with the factor as a pair (ALGEBRA.md #the-stable-body)."""
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


def given_wavelength(
    body: dict[str, Any], rows: dict[str, Any], clock: tuple[int, int]
) -> dict[str, int]:
    """The reading `wavelength` of a giving body: lambda_q of its mode on the given record's band (the given family's row's pair, or the emitter's own `pair` where the row declares none); no reading on a body that gives nothing or whose rotation the band does not hold."""
    emitter = body.get("emitter")
    if not isinstance(emitter, dict):
        return {}
    row = rows[emitter["family"]]
    pair = emitter.get("pair", row.get("pair"))
    found = wavelength_of(clock, (int(pair[0]), int(pair[1])))
    return {} if found is None else {"wavelength": found}


def generate(document: dict[str, Any]) -> dict[str, Any]:
    """The generator on its input file, a world file in the law's form (ALGEBRA.md #the-generator): the GameBoard's shape and faces, the Node clock (the world's, or the universe's integer), the universe file it names (the families' rows: each body's family's pair and reads, the held families' pairs, the integers by name) and the bodies written by their Nodes with their counts; the held fields at rest under every body's count (the hold's clamp at every body's Nodes), then per body whose family reads a held field plainly its mode in its own well (the weighted sum of its own counts' fields at rest) by the one path of rest and motion, the phase's pair (m, 0) at the momentum 0, and its clock in the world's well (the rotation of that profile with every body's field); a body's refusal by name is written as its reading, the other bodies go on; no number in the tool or on the command line."""
    shape = tuple(int(n) for n in document["shape"])
    faces = document["boundary"]
    wrap = tuple(
        (faces if isinstance(faces, dict) else {a: faces for a in "xyz"})[axis] == "periodic"
        for axis in "xyz"
    )
    universe = read_document(document["universe"])
    rows = {row["name"]: row for row in universe["families"]}
    integers = universe.get("integers", {})
    gamma = int(document.get("node_clock", integers.get("node_clock", 0)))
    bound_level = loader_level(document, gamma)
    # the own twist's scale from the file: theta_unit = 1 / unit, "own" = round(unit omega_0 / (4 Gamma)) (ALGEBRA.md #the-primitives)
    twist_scale = int(
        division(1, 4 * gamma, np.array(int(integers["twist_table"]["unit"]), dtype=object))
    )
    bodies = [
        body for body in document.get("measured", []) if isinstance(body, dict) and "nodes" in body
    ]
    if not bodies:
        raise ValueError(
            "the generator takes bodies in the law's form (their nodes with their counts), found none"
        )
    counts_of: list[np.ndarray] = []
    total = np.zeros(shape, dtype=np.int64)
    for body in bodies:
        counts = np.zeros(shape, dtype=np.int64)
        for entry in body["nodes"]:
            counts[tuple(int(v) for v in entry["node"])] = int(entry["count"])
        counts_of.append(counts)
        total = total + counts
    rests: dict[str, Any] = {}
    fields: dict[str, FieldAtRest] = {}
    own_fields: dict[tuple[int, str], FieldAtRest] = {}
    readings: list[dict[str, Any]] = []
    for body, counts in zip(bodies, counts_of, strict=True):
        row = rows[body["family"]]
        reading: dict[str, Any] = {"family": body["family"], "pair": list(row.get("pair", []))}
        readings.append(reading)
        try:
            pair = pair_of(row, f"the family {body['family']!r}")
            momentum = tuple(int(v) for v in body.get("momentum", (0, 0, 0)))
            axes = [axis for axis, component in enumerate(momentum) if component]
            if len(axes) > 1:
                raise ValueError(f"a moving body moves along one axis: the momentum {momentum} has two")
            plain = [read for read in row.get("reads", []) if read.get("by") in (1, "plain")]
            if not plain:
                reading["mode"] = (
                    "none: the family reads no held field plainly, the body is content alone"
                )
                continue
            content = np.zeros(shape, dtype=np.int64)
            own_content = np.zeros(shape, dtype=np.int64)  # the body's own well: its own counts' fields
            for read in plain:
                weight = read["weight"]
                if isinstance(weight, str):
                    weight = integers[weight]
                held = rows[read["family"]]
                if read["family"] not in fields:
                    rest = start_rest(total, pair_of(held, f"the held family {read['family']!r}"), wrap)
                    fields[read["family"]] = rest
                    rests[read["family"]] = {
                        "pair": list(held["pair"]),
                        "iterations": rest.iterations,
                        "cycle": rest.cycle,
                        "at_bodies": int(rest.levels[total > 0].min()),
                        "at_corner": int(rest.levels[0, 0, 0]),
                    }
                content = content + int(weight) * fields[read["family"]].levels
                own_key = (id(body), read["family"])
                if own_key not in own_fields:
                    own_fields[own_key] = start_rest(
                        counts, pair_of(held, f"the held family {read['family']!r}"), wrap
                    )
                own_content = own_content + int(weight) * own_fields[own_key].levels
            if "phase_denominator" not in body:
                raise ValueError(
                    "a body declares its phase_denominator m (the phase's pair (m, j), j = 0 at rest, bisected in motion)"
                )
            axis = axes[0] if axes else 0
            order = (axis, *(other for other in range(3) if other != axis))
            moved = moving_body(
                np.moveaxis(counts, axis, 0),
                pair,
                gamma,
                momentum[axis],
                int(integers["momentum_unit"]),
                int(body["phase_denominator"]),
                tuple(wrap[other] for other in order),
                np.moveaxis(own_content, axis, 0),
                bound_level=bound_level,
            )
            mode = moved.rest
            # the body's clock in the world's well: the rotation of its own profile with every body's
            # field, the same symmetric form (the redshift's depth enters here); refused by name where
            # the profile is no mode of the world's well, the own rotation then the clock's
            in_world: dict[str, Any] = {}
            try:
                level = mode.profile.astype(object)
                read, self_coefficient, wall = rule_integers(pair, gamma, content)
                total = rule3(
                    (read, read, read), arrivals(level, wrap), self_coefficient, 1, level, 0, 0
                )[0]
                rotation, share = rotation_and_share(
                    (level,), (total,), wall, counts, gamma, pair, "mode in the world's well", content
                )
                in_world = {"rotation": [rotation.numerator, rotation.denominator]}
            except ValueError as refusal:
                in_world = {"refused": str(refusal)}
                rotation = mode.rotation
            if momentum[axis]:
                rotation = proper_rotation(rotation, moved.triple, moved.top)
            clock = clock_pair(rotation, mode.amplitude)
            moving = {
                "axis": axis,
                "momentum": momentum[axis],
                "phase_pair": list(moved.pair),
                "triple": list(moved.triple),
                "velocity_named": [moved.named.numerator, moved.named.denominator],
                "velocity": [moved.velocity.numerator, moved.velocity.denominator],
                "top_velocity": [moved.top.numerator, moved.top.denominator],
                "now": np.moveaxis(moved.now, 0, axis),
                "before": np.moveaxis(moved.before, 0, axis),
            }
            reading.update(
                {
                    "amplitude_unit": mode.amplitude,
                    "iterations": mode.iterations,
                    "cycle": mode.cycle,
                    "rotation": [mode.rotation.numerator, mode.rotation.denominator],
                    "clock": list(clock),
                    "period": period_by_the_rule(*clock),
                    "twist": round(twist_scale * acos(clock[0] / (2 * clock[1]))),
                    **given_wavelength(body, rows, clock),
                    "share_inside": [mode.share_inside.numerator, mode.share_inside.denominator],
                    "in_the_worlds_well": in_world,
                    "profile": mode.profile,
                    "content": content,
                    "moving": moving,
                }
            )
        except ValueError as refusal:
            reading["refused"] = str(refusal)
    return {"rest": rests, "bodies": readings}


def split_levels(
    reading: dict[str, Any],
) -> tuple[list[np.ndarray | None], list[tuple[np.ndarray, np.ndarray] | None]]:
    """The arrays taken out of the generator's reading before it is printed: each body's profile and, on a body with a momentum, its two levels (a resting body's levels are its profile, not written twice)."""
    profiles: list[np.ndarray | None] = []
    levels: list[tuple[np.ndarray, np.ndarray] | None] = []
    for body in reading["bodies"]:
        profiles.append(body.pop("profile", None))
        body.pop("content", None)
        moving = body.get("moving")
        if moving is None:
            levels.append(None)
            continue
        now, before = moving.pop("now"), moving.pop("before")
        levels.append((now, before) if moving["momentum"] else None)
    return profiles, levels


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True, help="the world file in the law's form")
    parser.add_argument(
        "--out",
        type=Path,
        help="write the mode file beside the world (<world>.mode.json): the world file's digest, the held fields at rest and every body's resting mode at its amplitude unit with its phase's pair; a derived record the loader checks in one pass, never a declaration",
    )
    args = parser.parse_args()
    sys.set_int_max_str_digits(
        0
    )  # the rotation is an exact fraction: its digits are the well's, not the host's to cap
    document = args.input.read_bytes()
    reading = generate(json.loads(document))
    reading["world_digest"] = input_digest(
        json.loads(document)
    )  # the one digest of a world, the loader's
    profiles, levels = split_levels(reading)
    print(json.dumps(reading))
    if args.out is not None:
        args.out.write_text(json.dumps(mode_document(reading, profiles, levels)))


def mode_document(
    reading: dict[str, Any],
    profiles: list[np.ndarray | None],
    levels: list[tuple[np.ndarray, np.ndarray] | None],
) -> dict[str, Any]:
    """The mode file's document: the reading with every body's profile as a flat list and, on a moving body, its two levels `now` and `before` under `moving` (ALGEBRA.md #the-generator (e)), the loader's to read."""
    for body, profile, pair in zip(reading["bodies"], profiles, levels, strict=True):
        if profile is not None:
            body["profile"] = profile.ravel().tolist()
        if pair is not None:
            body["moving"]["now"] = pair[0].ravel().tolist()
            body["moving"]["before"] = pair[1].ravel().tolist()
    return reading


if __name__ == "__main__":
    main()
