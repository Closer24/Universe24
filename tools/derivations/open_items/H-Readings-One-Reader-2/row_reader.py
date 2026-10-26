"""The one reader of the row (H-Readings-One-Reader-2): every reading of a record row is one bilinear form x.M.y of two lists of lines with one of the row's four matrices by name, G (the Gram), GJ (the Gram times the quarter turn), GA_a (the Gram times the axis matrix a) and K (the conjugation): the charge B.GJ.N, the current dN_a.GJ.N with the neighbour's lines conjugated by K where the frame is -1, the spin density N.GA_a.N, the Node term SUM_a coefficient Phi_a (Gamma_a x), the share's four quadratic parts and the period's ratio N.G.B / N.G.N; the curl is the Link reader's gradient. The matrices come from gram (the quartet's derived ones, the plane's identity), nothing else is read from gram."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe import gram
from event_universe.core.ports import AXES, across, port_of, wrap
from event_universe.core.rule3 import division_forward, share_weight
from event_universe.rows import zeros

from link_reader import gradient

Matrix = list[list[int]]


def matrix(shape: int, name: str, axis: int = 0) -> Matrix:
    """The row's matrix by name: G, GJ, GA (the axis matrix `axis`), K, J."""
    if name == "G":
        return gram.gram(shape)
    if name == "GJ":
        return gram.matmul(gram.gram(shape), gram.rotation(shape))
    if name == "GA":
        return gram.matmul(gram.gram(shape), gram.axes(shape)[axis])
    if name == "K":
        return gram.conjugation(shape)
    return gram.rotation(shape)


def lines(m: Matrix, xs: list[Any], ys: list[Any]) -> list[Any]:
    """The bilinear x.m.y line by line, x_k (m y)_k (the plain products at the identity)."""
    if m == gram.identity(len(xs)):
        return [x * y for x, y in zip(xs, ys, strict=True)]
    return [x * my for x, my in zip(xs, gram.matvec(m, ys), strict=True)]


def bilinear(m: Matrix, xs: list[Any], ys: list[Any]) -> Any:
    """The bilinear x.m.y summed over the lines: the one reading of the row."""
    return sum(lines(m, xs, ys), start=0)


def conjugated(shape: int, xs: list[Any], frame: Any) -> list[Any]:
    """A neighbour's lines in the Node's frame: K x where the frame sign is -1."""
    return [np.where(frame == -1, k, x) for k, x in zip(gram.matvec(matrix(shape, "K"), xs), xs, strict=True)]


def charge(shape: int, befores: list[Any], nows: list[Any]) -> Any:
    """The charge density W = B.GJ.N."""
    return bilinear(matrix(shape, "GJ"), befores, nows)


def current(shape: int, nows: list[Any], frames: list[Any]) -> list[Any]:
    """The sign current on each axis, dN_a.GJ.N, the neighbours read in the Node's frame."""
    gj = matrix(shape, "GJ")
    found = []
    for a in range(AXES):
        up = conjugated(shape, [across(n, port_of(a, 0)) for n in nows], frames[port_of(a, 0)])
        down = conjugated(shape, [across(n, port_of(a, 1)) for n in nows], frames[port_of(a, 1)])
        found.append(bilinear(gj, [u - d for u, d in zip(up, down, strict=True)], nows))
    return found


def density(shape: int, nows: list[Any]) -> list[Any]:
    """The spin density on each axis, N.GA_a.N; none for a row with no axis matrices."""
    return [bilinear(matrix(shape, "GA", a), nows, nows) for a in range(len(gram.axes(shape)))]


def curl(odd: list[Any]) -> list[Any]:
    """The curl of the odd lines, Phi_a = d_b A_c - d_c A_b, the Link reader's gradient."""
    return [
        gradient(odd[wrap(a - 1, AXES)], wrap(a + 1, AXES)) - gradient(odd[wrap(a + 1, AXES)], wrap(a - 1, AXES))
        for a in range(AXES)
    ]


def term(shape: int, coefficient: Any, phi: list[Any], xs: list[Any]) -> list[Any]:
    """The Node term SUM_a coefficient Phi_a (Gamma_a x) per line; 0 with no axis matrices."""
    found: list[Any] = [0] * len(xs)
    for a, ga in enumerate(gram.axes(shape)):
        found = [f + coefficient * phi[a] * g for f, g in zip(found, gram.matvec(ga, xs), strict=True)]
    return found


def share(node: Any, nows: list[Any], befores: list[Any], r: Any) -> Any:
    """The conserved form's share in the carrier's unit, the four quadratic readings of G per line over the share's wall."""
    g = matrix(len(nows), "G")
    reached = [zeros(node.shape) for _ in nows]
    shared = [zeros(node.shape) for _ in nows]
    for port, reach in enumerate(r.reaches):
        b_j = [across(b, port) for b in befores]
        n_j = [across(n, port) for n in nows]
        reached = [x + reach * bj for x, bj in zip(reached, b_j, strict=True)]
        parts = lines(g, [b - bj for b, bj in zip(befores, b_j, strict=True)], [n + nj for n, nj in zip(nows, n_j, strict=True)])
        shared = [s + reach * part for s, part in zip(shared, parts, strict=True)]
    own = [
        r.wall * (nn + bb) - r.self_coefficient * nb - nr
        for nn, bb, nb, nr in zip(
            lines(g, nows, nows), lines(g, befores, befores), lines(g, nows, befores), lines(g, nows, reached), strict=True
        )
    ]
    wall = share_weight(node.gamma, node.G) + share_weight(node.gamma, node.G)
    found = zeros(node.shape)
    for o, s in zip(own, shared, strict=True):
        found = found + np.asarray(division_forward((o + o - s) * node.start_x, wall, 0)[0])
    return found
