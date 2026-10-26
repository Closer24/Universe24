"""The record rows' bilinears by shape, one act on every record alike (SR-S1 to SR-S4): a record of 2k lines is k planes on one lattice with a Gram matrix G (the identity for a plane, the derived trace form for a quartet, quartet.py), a rotation J (the quarter turn per plane), a conjugation K (the im line's negation for a plane, the lattice's K0 for a quartet) and axis matrices (none for a plane, the three Gamma_a for a quartet): the charge B.GJ.N (the plane's Wronskian), the current, the spin density N.G Gamma_a.N (the record's axial vector), the frame's conjugation of a neighbour's lines, the Node term from the curl of the odd lines (the coupling by shape, SR-S3), the row's scale 2 x 6 Gamma that carries the term's coefficient R / (2 Gamma) inside the one division, the lay at rest by rule3's signed quotient and the period from the rotation's cosine N.G.B / N.G.N read along the law's own orbit."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import numpy as np

from event_universe.core.ports import AXES, PORTS, across, port_of, wrap
from event_universe.core.rule3 import half, quotient, share_weight, signed_quotient
from event_universe.links import gradient
from event_universe.quartet import quartet
from event_universe.readings import pair_angle
from event_universe.rows import PLANE, QUARTET, Line, zeros

if TYPE_CHECKING:
    from event_universe.node import Node

Matrix = list[list[int]]


def identity(n: int) -> Matrix:
    """The identity on n lines."""
    return [[int(r == c) for c in range(n)] for r in range(n)]


def gram(shape: int) -> Matrix:
    """The row's Gram matrix G: the identity for every shape but the quartet's derived trace form."""
    return quartet().G if shape == QUARTET else identity(shape)


def rotation(shape: int) -> Matrix:
    """The row's rotation J, the quarter turn of each plane (re, im) -> (-im, re): the quartet's derived J, the standard blocks for a plane."""
    if shape == QUARTET:
        return quartet().J
    found = [[0] * shape for _ in range(shape)]
    for p in range(quotient(shape, PLANE)):
        found[PLANE * p][PLANE * p + 1], found[PLANE * p + 1][PLANE * p] = -1, 1
    return found


def conjugation(shape: int) -> Matrix:
    """The row's conjugation K, the frame's and the swap's: the quartet's derived K0; for a plane the im line negated; the identity for a row of another shape (a line of one level is its own conjugate)."""
    if shape == QUARTET:
        return quartet().K0
    found = identity(shape)
    if shape == PLANE:
        found[1][1] = -1
    return found


def axes(shape: int) -> list[Matrix]:
    """The row's axis matrices Gamma_a, the coupling's: the quartet's three, none for another shape."""
    return quartet().gamma if shape == QUARTET else []


def scale(shape: int, gamma: Any) -> Any:
    """The row's scale on the rule and the walls: 2 x 6 Gamma for the quartet, so that the term's coefficient R / (2 Gamma) summed over the six Ports enters as the integer SUM_j R_j (SR-S3, sr1's form); 1 for every other shape."""
    return (PORTS + PORTS) * gamma if shape == QUARTET else 1


def matvec(m: Matrix, xs: list[Any]) -> list[Any]:
    """A matrix on a list of arrays, the zero entries skipped."""
    return [sum((m[r][c] * xs[c] for c in range(len(xs)) if m[r][c]), start=0) for r in range(len(m))]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    """The product of two integer matrices."""
    return [
        [sum(a[r][k] * b[k][c] for k in range(len(b))) for c in range(len(b[0]))] for r in range(len(a))
    ]


def weighted(m: Matrix, xs: list[Any], ys: list[Any]) -> list[Any]:
    """The bilinear x.m.y line by line, x_k (m y)_k, so that a division per line stays one per line; at the identity (every shape but the quartet's) the plain products x_k y_k."""
    if m == identity(len(xs)):
        return [x * y for x, y in zip(xs, ys, strict=True)]
    return [x * my for x, my in zip(xs, matvec(m, ys), strict=True)]


def form(m: Matrix, xs: list[Any], ys: list[Any]) -> Any:
    """The bilinear x.m.y summed over the lines."""
    return sum(weighted(m, xs, ys), start=0)


def charge(shape: int, lines: list[Line]) -> Any:
    """The record's charge density W = B.GJ.N at every Node, the plane's Wronskian re_now im_before - im_now re_before as the case G = I."""
    return form(
        matmul(gram(shape), rotation(shape)),
        [line.before for line in lines],
        [line.now for line in lines],
    )


def conjugated(shape: int, xs: list[Any], frame: Any) -> list[Any]:
    """A neighbour's lines read in the Node's frame: conjugated by the row's K where the frame sign is -1, the plane's im line negated there."""
    return [np.where(frame == -1, k, x) for k, x in zip(matvec(conjugation(shape), xs), xs, strict=True)]


def current(shape: int, nows: list[Any], frames: list[Any]) -> list[Any]:
    """The record's sign current on each axis, J_a = dN_a.GJ.N with dN_a the centred difference of the levels now, the neighbours' lines read in the Node's frame; the plane's re dim - im dre as the case G = I."""
    gj = matmul(gram(shape), rotation(shape))
    found = []
    for a in range(AXES):
        up = conjugated(shape, [across(n, port_of(a, 0)) for n in nows], frames[port_of(a, 0)])
        down = conjugated(shape, [across(n, port_of(a, 1)) for n in nows], frames[port_of(a, 1)])
        found.append(form(gj, [u - d for u, d in zip(up, down, strict=True)], nows))
    return found


def density(shape: int, nows: list[Any]) -> list[Any]:
    """The record's spin density on each axis, s_a = N.G Gamma_a.N, the axial vector no line carries (SR-S2); none for a plane."""
    g = gram(shape)
    return [form(matmul(g, ga), nows, nows) for ga in axes(shape)]


def curl(odd: list[Any]) -> list[Any]:
    """The one-Link curl of the shape-4 row's odd lines at the Node, Phi_a = d_b A_c - d_c A_b with d_b the centred difference through the two Ports of the axis b."""
    return [
        gradient(odd[wrap(a - 1, AXES)], wrap(a + 1, AXES))
        - gradient(odd[wrap(a + 1, AXES)], wrap(a - 1, AXES))
        for a in range(AXES)
    ]


def term(shape: int, coefficient: Any, phi: list[Any], xs: list[Any]) -> list[Any]:
    """The Node term of the coupling by shape, SUM_a coefficient Phi_a (Gamma_a x) per line (SR-S3), 0 for a row with no axis matrices; the coefficient the unscaled reaches' sum, the row's scale carrying R / (2 Gamma)."""
    found: list[Any] = [0] * len(xs)
    for a, ga in enumerate(axes(shape)):
        found = [f + coefficient * phi[a] * g for f, g in zip(found, matvec(ga, xs), strict=True)]
    return found


def share(node: Node, lines: list[Line], r: Any) -> Any:
    """The conserved form's share of a record at the Node in the carrier's unit (PM-S1: every count of the Node read in the carrier's unit, the one weight for every read and every row alike), one division per line: for the line k, [w (n_k (G n)_k + b_k (G b)_k) - S n_k (G b)_k - n_k (G SUM_j R_j b_j)_k], doubled, less SUM_j R_j (b - b_j)_k (G (n + n_j))_k, times X the carrier's level at the interval's start, over 4 Gamma^3 G^2 ((Gamma / p_i)^2 = X / Gamma to the unit; at the vacuum X = Gamma and the weight is the former vacuum's 4 Gamma^2 G^2 bit for bit); the plane's share line by line as the case G = I; at the row's unscaled rule."""
    from event_universe.core.rule3 import division_forward

    g = gram(len(lines))
    nows, befores = [line.now for line in lines], [line.before for line in lines]
    reached = [zeros(node.shape) for _ in lines]
    shared = [zeros(node.shape) for _ in lines]
    for port, reach in enumerate(r.reaches):
        b_j = [across(b, port) for b in befores]
        n_j = [across(n, port) for n in nows]
        reached = [x + reach * bj for x, bj in zip(reached, b_j, strict=True)]
        parts = weighted(
            g,
            [b - bj for b, bj in zip(befores, b_j, strict=True)],
            [n + nj for n, nj in zip(nows, n_j, strict=True)],
        )
        shared = [s + reach * part for s, part in zip(shared, parts, strict=True)]
    own = [
        r.wall * (nn + bb) - r.self_coefficient * nb - nr
        for nn, bb, nb, nr in zip(
            weighted(g, nows, nows),
            weighted(g, befores, befores),
            weighted(g, nows, befores),
            weighted(g, nows, reached),
            strict=True,
        )
    ]
    wall = share_weight(node.gamma, node.G) + share_weight(node.gamma, node.G)
    found = zeros(node.shape)
    for o, s in zip(own, shared, strict=True):
        found = found + np.asarray(division_forward((o + o - s) * node.start_x, wall, 0)[0])
    return found


def moving(
    shape: int,
    base: Any,
    vector: list[int],
    now_pair: tuple[Any, Any],
    before_pair: tuple[Any, Any],
    den: int,
    sense: int,
) -> list[Line]:
    """A record laid at a phase over the envelope (MV-S1): now = base (C v + sense S (J v)) over den at the Node's phase pair (C, S) and before the same at the pair (C', S') turned by the band's rotation, each product's quotient toward zero line by line (rule3.signed_quotient), so the two senses' J lines cancel exactly and the lay at the conjugate pair is the conjugate lay; the rest lay the case (den, 0) and (num, s)."""
    turned = matvec(rotation(shape), list(vector))

    def levels(c: Any, s: Any) -> list[Any]:
        return [
            signed_quotient(base * c * v, den) + sense * signed_quotient(base * s * j, den)
            for v, j in zip(vector, turned, strict=True)
        ]

    return [Line(n, b, None, None) for n, b in zip(levels(*now_pair), levels(*before_pair), strict=True)]


def rest(
    shape: int, re_now: Any, vector: list[int], num: int, den: int, sine: int, sense: int
) -> list[Line]:
    """A record at rest over the envelope (`moving` at the pair (den, 0) now and the row's (num, s) before): now = re_now v (v the lay's vector, (1, 0) for a plane), before = num now div den + sense sine (J now) div den, each quotient toward zero (the plane's re_before = re_now num div den, im_before = sense re_now s div den as the case v = (1, 0))."""
    return moving(shape, re_now, vector, (den, 0), (num, sine), den, sense)


def cosine_count(node: Node, p: int, d: int) -> int:
    """The count n along the law's orbit (features/phase, the step 1 / Gamma) at which the orbit's cosine first falls to p / d, the rotation's angle in the orbit's units: a search by comparisons, cos_n d <= p X."""
    high = 1
    while pair_angle(node, high)[0] * d > p * node.X:
        high = high + high
    low = 0
    while high - low > 1:
        middle = half(low + high)
        if pair_angle(node, middle)[0] * d > p * node.X:
            low = middle
        else:
            high = middle
    return high


def period(node: Node, lines: list[Line], standing: Any) -> Any:
    """The record's beat at the Nodes where it stands, from the invariant ratio cos omega = N.G.B / N.G.N (no line of a quartet is a scalar under the 48, so no crossing line is covariant): the angle's count n along the law's orbit (`cosine_count`), then the first k >= 2 at which the orbit's cosine at k n is a maximum against k - 1 and k + 1, the first return; 0 where the ratio is degenerate."""
    g = gram(len(lines))
    nn = form(g, [line.now for line in lines], [line.now for line in lines])
    nb = form(g, [line.now for line in lines], [line.before for line in lines])
    found = zeros(node.shape)
    for where in zip(*np.nonzero(np.asarray(standing, dtype=object) == 1), strict=True):
        at = tuple(int(x) for x in where)
        d, p = int(nn[at]), int(nb[at])
        if d == 0 or p >= d or p <= -d:
            continue
        n = cosine_count(node, p, d)
        k = 1
        while not (
            pair_angle(node, k * n)[0] >= pair_angle(node, (k - 1) * n)[0]
            and pair_angle(node, k * n)[0] >= pair_angle(node, (k + 1) * n)[0]
        ):
            k += 1
        found[at] = k
    return found
