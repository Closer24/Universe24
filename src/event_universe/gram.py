"""The record rows' bilinears, one act on every record alike: a record is a plane, its two lines a clock's hand (re, im), with the plain products line by line (`products`, `dot`), a rotation J (the quarter turn (re, im) -> (-im, re)) and a conjugation K (the im line's negation): the charge B.J.N (the plane's Wronskian), the current, the frame's conjugation of a neighbour's lines, the lay at rest by rule3's signed quotient and the rotation's angle read along the law's own orbit (`cosine_count`; the spinor row's Gram form, axis matrices, spin density, curl term and scale struck with the row, 2026-10-27)."""

from __future__ import annotations

from collections.abc import Callable
from functools import lru_cache
from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.ports import AXES, PORTS, across, port_of
from event_universe.core.rule3 import half, quotient, share_weight, signed_quotient
from event_universe.readings import pair_angle
from event_universe.rows import PLANE, Line, zeros
from event_universe.take import neighbour

if TYPE_CHECKING:
    from event_universe.node import Node

Matrix = list[list[int]]


@lru_cache
def identity(n: int) -> Matrix:
    """The identity on n lines."""
    return [[int(r == c) for c in range(n)] for r in range(n)]


def rotation(shape: int) -> Matrix:
    """The row's rotation J, the quarter turn of each plane (re, im) -> (-im, re), the standard blocks."""
    found = [[0] * shape for _ in range(shape)]
    for p in range(quotient(shape, PLANE)):
        found[PLANE * p][PLANE * p + 1], found[PLANE * p + 1][PLANE * p] = -1, 1
    return found


def conjugation(shape: int) -> Matrix:
    """The row's conjugation K, the frame's and the swap's: for a plane the im line negated; the identity for a row of another shape (a line of one level is its own conjugate)."""
    found = [list(row) for row in identity(shape)]
    if shape == PLANE:
        found[1][1] = -1
    return found


def matvec(m: Matrix, xs: list[Any]) -> list[Any]:
    """A matrix on a list of arrays, the zero entries skipped."""
    return [sum((m[r][c] * xs[c] for c in range(len(xs)) if m[r][c]), start=0) for r in range(len(m))]


def products(xs: list[Any], ys: list[Any]) -> list[Any]:
    """The plain products x_k y_k line by line, so that a division per line stays one per line."""
    return [x * y for x, y in zip(xs, ys, strict=True)]


def dot(xs: list[Any], ys: list[Any]) -> Any:
    """The plain products x_k y_k summed over the lines."""
    return sum(products(xs, ys), start=0)


def weighted(m: Matrix, xs: list[Any], ys: list[Any]) -> list[Any]:
    """The bilinear x.m.y line by line, x_k (m y)_k, so that a division per line stays one per line."""
    return [x * my for x, my in zip(xs, matvec(m, ys), strict=True)]


def form(m: Matrix, xs: list[Any], ys: list[Any]) -> Any:
    """The bilinear x.m.y summed over the lines."""
    return sum(weighted(m, xs, ys), start=0)


def charge(shape: int, lines: list[Line]) -> Any:
    """The record's charge density W = B.J.N at every Node, the plane's Wronskian re_now im_before - im_now re_before."""
    return form(rotation(shape), [line.before for line in lines], [line.now for line in lines])


def conjugated(shape: int, xs: list[Any], frame: Any) -> list[Any]:
    """A neighbour's lines read in the Node's frame: conjugated by the row's K where the frame sign is -1, the plane's im line negated there."""
    return [np.where(frame == -1, k, x) for k, x in zip(matvec(conjugation(shape), xs), xs, strict=True)]


def current(shape: int, nows: list[Any], frames: list[Any]) -> list[Any]:
    """The record's sign current on each axis, J_a = dN_a.J.N with dN_a the centred difference of the levels now, the neighbours' lines read in the Node's frame; the plane's re dim - im dre."""
    gj = rotation(shape)
    found = []
    for a in range(AXES):
        up = conjugated(shape, [across(n, port_of(a, 0)) for n in nows], frames[port_of(a, 0)])
        down = conjugated(shape, [across(n, port_of(a, 1)) for n in nows], frames[port_of(a, 1)])
        found.append(form(gj, [u - d for u, d in zip(up, down, strict=True)], nows))
    return found


def share(node: Node, lines: list[Line], r: Any, window: list[tuple[int, ...]] | None = None) -> Any:
    """The conserved form's share of a record at the Node in the carrier's unit (PM-S1: every count of the Node read in the carrier's unit, the one weight for every read and every row alike), one division per line: for the line k, [w (n_k n_k + b_k b_k) - S n_k b_k - n_k (SUM_j R_j b_j)_k], doubled, less SUM_j R_j (b - b_j)_k (n + n_j)_k, times X the carrier's level at the interval's start, over 4 Gamma^3 G^2 ((Gamma / p_i)^2 = X / Gamma to the unit; at the vacuum X = Gamma and the weight is the former vacuum's 4 Gamma^2 G^2 bit for bit); the plane's share line by line, at the row's rule. At a window of Nodes (`window`, a take's Node and its six neighbours, merger.walls_of and share_fall) the same integers read at those Nodes alone, each neighbour gathered by its place through take.neighbour, returned in the window's order (the former merger.share_at, gram.share's form re-spelt at one Node, folded 2026-10-26 as R3 of the readings' map: one spelling, the vectorised form inside it)."""
    at: Callable[[Any], Any]
    beyond: Callable[[Any, int], Any]
    if window is None:
        at, beyond, x = (lambda a: a), across, node.start_x
    else:
        places = [tuple(np.array(w) for w in zip(*window, strict=True))]
        for port in range(PORTS):
            around = [neighbour(node, where, port) for where in window]
            places.append(tuple(np.array(w) for w in zip(*around, strict=True)))

        def at(a: Any) -> Any:
            return a[places[0]] if np.ndim(a) else a

        def beyond(a: Any, port: int) -> Any:
            return a[places[1 + port]]

        x = node.start_x[places[0]]
    full_n, full_b = [line.now for line in lines], [line.before for line in lines]
    nows, befores = [at(n) for n in full_n], [at(b) for b in full_b]
    reached = [at(zeros(node.shape)) for _ in lines]
    shared = [at(zeros(node.shape)) for _ in lines]
    for port, reach in enumerate(r.reaches):
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
        at(r.wall) * (nn + bb) - at(r.self_coefficient) * nb - nr
        for nn, bb, nb, nr in zip(
            products(nows, nows),
            products(befores, befores),
            products(nows, befores),
            products(nows, reached),
            strict=True,
        )
    ]
    wall = share_weight(node.gamma, node.G) + share_weight(node.gamma, node.G)
    found = at(zeros(node.shape))
    for o, s in zip(own, shared, strict=True):
        found = found + np.asarray(quotient((o + o - s) * x, wall))
    return found


def moving(
    base: Any, now_pair: tuple[Any, Any], before_pair: tuple[Any, Any], den: int, sense: int
) -> list[Line]:
    """A plane laid at a phase over the envelope (MV-S1), a clock's hand at the angle (C, S): now = (base C, sense base S) over den at the Node's phase pair (C, S) and before the same at the pair (C', S') turned by the band's rotation, each product's quotient toward zero line by line (rule3.signed_quotient), so the two senses' im lines cancel exactly and the lay at the conjugate pair is the conjugate lay; the rest lay the case (den, 0) and (num, s) (the former lay's vector, (1, 0) on every plane, struck with the spinor row, 2026-10-27)."""

    def levels(c: Any, s: Any) -> list[Any]:
        return [signed_quotient(base * c, den), sense * signed_quotient(base * s, den)]

    return [Line(n, b, None, None) for n, b in zip(levels(*now_pair), levels(*before_pair), strict=True)]


def rest(re_now: Any, num: int, den: int, sine: int, sense: int) -> list[Line]:
    """A plane at rest over the envelope (`moving` at the pair (den, 0) now and the row's (num, s) before): re_now = re_now, im_now = 0, re_before = re_now num div den, im_before = sense re_now s div den, each quotient toward zero."""
    return moving(re_now, (den, 0), (num, sine), den, sense)


def cosine_count(node: Node, p: int, d: int) -> int:
    """The count n along the law's orbit (features/phase, the step 1 / Gamma) at which the orbit's cosine first falls to p / d, the rotation's angle in the orbit's units: a search by comparisons, cos_n d <= p X, bounded by the orbit's half turn where the table reaches it (the deepest cosine the orbit holds)."""
    high = 1
    while pair_angle(node, high)[0] * d > p * node.X and (
        node.orbit_half is None or high < node.orbit_half
    ):
        high = high + high
    high = high if node.orbit_half is None else min(high, node.orbit_half)
    low = 0
    while high - low > 1:
        middle = half(low + high)
        if pair_angle(node, middle)[0] * d > p * node.X:
            low = middle
        else:
            high = middle
    return high
