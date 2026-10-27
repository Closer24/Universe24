"""The record rows' bilinears, one act on every record alike: a record is a plane, its two lines a clock's hand (re, im), with the plain products line by line (`products`, `dot`), a rotation J (the quarter turn (re, im) -> (-im, re)) and a conjugation K (the im line's negation): the charge B.J.N (the plane's Wronskian), the current, the frame's conjugation of a neighbour's lines, the lay at rest by rule3's signed quotient and the rotation's angle read along the law's own orbit (`cosine_count`; the spinor row's Gram form, axis matrices, spin density, curl term and scale struck with the row, 2026-10-27)."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.rule3 import carries, half, signed_carries, wind_weight
from event_universe.core.spokes import AXES, SPOKES, across, spoke_of
from event_universe.meshes import cross
from event_universe.readings import standard_angle
from event_universe.trains import HAND, Gear, zeros
from event_universe.unwind import neighbour

if TYPE_CHECKING:
    from event_universe.clock import Clock


def signs(shape: int) -> list[int]:
    """The train's conjugation K as signs, the pawl's and the turnover's: a hand's twelve gear turned over, every gear of another train its own conjugate."""
    return [1, -1] if shape == HAND else [1] * shape


def seen(z: list[Any], pawl: Any) -> list[Any]:
    """A neighbour's hand read in the clock's frame, the conjugate where the pawl is -1: its twelve shadow times the pawl (a pawl is 1 or -1)."""
    three, twelve = z
    return [three, pawl * twelve]


def products(xs: list[Any], ys: list[Any]) -> list[Any]:
    """The plain products x_k y_k line by line, so that a division per line stays one per line."""
    return [x * y for x, y in zip(xs, ys, strict=True)]


def dot(xs: list[Any], ys: list[Any]) -> Any:
    """The plain products x_k y_k summed over the lines."""
    return sum(products(xs, ys), start=0)


def sweep(lines: list[Gear]) -> Any:
    """The hand's sweep W = Im(conj(z_now) z_before) at every clock, three_now twelve_before - twelve_now three_before (meshes.cross, the plane's Wronskian)."""
    three, twelve = lines
    return cross(three.now, twelve.now, three.before, twelve.before)


def lead(nows: list[Any], pawls: list[Any]) -> list[Any]:
    """The hand's lead on each axis, J_a = Im(conj(z) (z_up - z_down)) with the neighbours read in the clock's frame (`seen`): three dtwelve - twelve dthree."""
    found = []
    for a in range(AXES):
        up = seen([across(n, spoke_of(a, 0)) for n in nows], pawls[spoke_of(a, 0)])
        down = seen([across(n, spoke_of(a, 1)) for n in nows], pawls[spoke_of(a, 1)])
        found.append(cross(*nows, *(u - d for u, d in zip(up, down, strict=True))))
    return found


def wind(node: Clock, lines: list[Gear], r: Any, window: list[tuple[int, ...]] | None = None) -> Any:
    """The conserved form's share of a record at the Node in the carrier's unit (PM-S1: every count of the Node read in the carrier's unit, the one weight for every read and every row alike), one division per line: for the line k, [w (n_k n_k + b_k b_k) - S n_k b_k - n_k (SUM_j R_j b_j)_k], doubled, less SUM_j R_j (b - b_j)_k (n + n_j)_k, times X the carrier's level at the interval's start, over 4 Gamma^3 G^2 ((Gamma / p_i)^2 = X / Gamma to the unit; at the vacuum X = Gamma and the weight is the former vacuum's 4 Gamma^2 G^2 bit for bit); the plane's share line by line, at the row's rule. At a window of Nodes (`window`, a take's Node and its six neighbours, merger.walls_of and share_fall) the same integers read at those Nodes alone, each neighbour gathered by its place through take.neighbour, returned in the window's order (the former merger.share_at, gram.share's form re-spelt at one Node, folded 2026-10-26 as R3 of the readings' map: one spelling, the vectorised form inside it)."""
    at: Callable[[Any], Any]
    beyond: Callable[[Any, int], Any]
    if window is None:
        at, beyond, x = (lambda a: a), across, node.start_stretch
    else:
        places = [tuple(np.array(w) for w in zip(*window, strict=True))]
        for port in range(SPOKES):
            around = [neighbour(node, where, port) for where in window]
            places.append(tuple(np.array(w) for w in zip(*around, strict=True)))

        def at(a: Any) -> Any:
            return a[places[0]] if np.ndim(a) else a

        def beyond(a: Any, port: int) -> Any:
            return a[places[1 + port]]

        x = node.start_stretch[places[0]]
    full_n, full_b = [line.now for line in lines], [line.before for line in lines]
    nows, befores = [at(n) for n in full_n], [at(b) for b in full_b]
    reached = [at(zeros(node.size)) for _ in lines]
    shared = [at(zeros(node.size)) for _ in lines]
    for port, reach in enumerate(r.grips):
        b_j = [beyond(b, port) for b in full_b]
        n_j = [beyond(n, port) for n in full_n]
        here = at(reach)
        reached = [v + here * bj for v, bj in zip(reached, b_j, strict=True)]
        parts = products(
            [b - bj for b, bj in zip(befores, b_j, strict=True)],
            [n + nj for n, nj in zip(nows, n_j, strict=True)],
        )
        shared = [s + here * part for s, part in zip(shared, parts, strict=True)]
    own = [
        at(r.teeth) * (nn + bb) - at(r.hold) * nb - nr
        for nn, bb, nb, nr in zip(
            products(nows, nows),
            products(befores, befores),
            products(nows, befores),
            products(nows, reached),
            strict=True,
        )
    ]
    wall = wind_weight(node.full_rate, node.G) + wind_weight(node.full_rate, node.G)
    found = at(zeros(node.size))
    for o, s in zip(own, shared, strict=True):
        found = found + np.asarray(carries((o + o - s) * x, wall))
    return found


def moving(
    base: Any, now_pair: tuple[Any, Any], before_pair: tuple[Any, Any], den: int, sense: int
) -> list[Gear]:
    """A plane laid at a phase over the envelope (MV-S1), a clock's hand at the angle (C, S): now = (base C, sense base S) over den at the Node's phase pair (C, S) and before the same at the pair (C', S') turned by the band's rotation, each product's quotient toward zero line by line (rule3.signed_quotient), so the two senses' im lines cancel exactly and the lay at the conjugate pair is the conjugate lay; the rest lay the case (den, 0) and (num, s) (the former lay's vector, (1, 0) on every plane, struck with the spinor row, 2026-10-27)."""

    def levels(c: Any, s: Any) -> list[Any]:
        return [signed_carries(base * c, den), sense * signed_carries(base * s, den)]

    return [Gear(n, b, None, None) for n, b in zip(levels(*now_pair), levels(*before_pair), strict=True)]


def rest(re_now: Any, num: int, den: int, sine: int, sense: int) -> list[Gear]:
    """A plane at rest over the envelope (`moving` at the pair (den, 0) now and the row's (num, s) before): re_now = re_now, im_now = 0, re_before = re_now num div den, im_before = sense re_now s div den, each quotient toward zero."""
    return moving(re_now, (den, 0), (num, sine), den, sense)


def cosine_count(node: Clock, p: int, d: int) -> int:
    """The count n along the law's orbit (features/phase, the step 1 / Gamma) at which the orbit's cosine first falls to p / d, the rotation's angle in the orbit's units: a search by comparisons, cos_n d <= p X, bounded by the orbit's half turn where the table reaches it (the deepest cosine the orbit holds)."""
    high = 1
    while standard_angle(node, high)[0] * d > p * node.standard_length and (
        node.circuit_half is None or high < node.circuit_half
    ):
        high = high + high
    high = high if node.circuit_half is None else min(high, node.circuit_half)
    low = 0
    while high - low > 1:
        middle = half(low + high)
        if standard_angle(node, middle)[0] * d > p * node.standard_length:
            low = middle
        else:
            high = middle
    return high
