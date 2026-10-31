"""Clock: every Node-clock is made alike from its star of six Spokes: the 24 turns that leave the star the same, the five kinds by which a train's gears turn with them, and the 48 lifts of the 24, whose three half-speed kinds and two trains take the full turn, the lift -1, as -I.
Algebra: the 24 are the matrices of three Spokes that Rule3's weight keeps, 24 of 216; A1, A2, E, T1 and T2 are built from their matrices, with no table typed; the 48 are the words u w^k z^m on the unit's axis and the Spokes', by Hamilton's product made from the star, each coordinate doubled and a pair p + q r2 of Z[x] / (x^2 - senses), read for equality alone, each product halved by Rule3's carry at senses with remainder 0; E1/2, E5/2 and G3/2 are their characters, and the 8-gear and 24-gear trains signed permutations on the cosets of C6 and on the classes +-h, read by products and carries alone.
Board: the same turns, kinds and lifts at every Node-clock; the four-vector's square (the 00, 0i, ii and jk slots) is the metric family's kinds; no family couples a half-speed train in this build.
Clicks: n/a: a kind is no observable; a click names a train, whose kinds say how it turns.
"""

from typing import NamedTuple

import numpy as np

from tensor24.algebra.carry import Z, carry


class Kinds(NamedTuple):
    """Each kind's matrix on every candidate, three of the Spokes as rows, in the kinds' order; a candidate's weight is 1 on the 24 alone."""

    a1: Z  # (candidates, 1, 1): 1
    a2: Z  # (candidates, 1, 1): the sign of the turn's permutation of the axes
    e: Z  # (candidates, 2, 2): that permutation on the plane where the axes sum to 0, in the basis (e1 - e2, e2 - e3)
    t1: Z  # (candidates, 3, 3): the turn itself, its rows Spokes
    t2: Z  # (candidates, 3, 3): A2 times T1


class Halves(NamedTuple):
    """The three half-speed kinds' characters on each of the 48 in the lifts' (sign, class) layout, each value a pair (p, q), p + q r2."""

    e1_2: Z  # (senses, classes, 2): 2 Re g, the doubled lift's unit part, g's trace as an SU(2) matrix
    e5_2: Z  # (senses, classes, 2): A2 times E1/2
    g3_2: Z  # (senses, classes, 2): E1/2 times E's character


class Lifts(NamedTuple):
    """The 48 lifts of the board's 24 in the (sign, class) layout: the classes +-h are (u up to sign, k, m), each held by its word whose u has the + sense."""

    whole: Kinds  # the five kinds on the 48 through each lift's turn, g's sandwich on the Spokes' axes (T1, one of the 24)
    halves: Halves  # the three half-speed kinds' characters
    cosets: Z  # (senses, classes, cosets, cosets): the 8-gear train, L(g) on the cosets of C6 in the heads' order
    classes: Z  # (senses, classes, classes, classes): the 24-gear train, L(g) e_[h] = sign e_[gh], the class and sign of every product


def det(m: Z) -> Z:
    """Each matrix's determinant, the triple product of its three rows, on a stack of any shape."""
    a, b, c = np.einsum("...ij->i...j", m)
    a0, a1, a2 = np.moveaxis(a, -1, 0)
    b0, b1, b2 = np.moveaxis(b, -1, 0)
    c0, c1, c2 = np.moveaxis(c, -1, 0)
    return a0 * (b1 * c2 - b2 * c1) - a1 * (b0 * c2 - b2 * c0) + a2 * (b0 * c1 - b1 * c0)


def axes(d: int) -> Z:
    """The board's d axes as whole numbers: the identity, whose rows and their opposites are the Spokes."""
    return np.eye(d, dtype=object)


def inverse(matrix: Z) -> Z:
    """Each turn's inverse, its transpose: a signed permutation's rows are its columns."""
    return np.einsum("...ij->...ji", matrix)


def turns(spokes: Z) -> tuple[Z, Z]:
    """Every matrix whose rows are three of the Node-clock's own Spokes, weighed by Rule3: (det + det det) div an axis's Spokes is 1 at det 1, else 0."""
    n, d = spokes.shape
    first = np.broadcast_to(spokes[:, None, None], (n, n, n, d))
    second = np.broadcast_to(spokes[None, :, None], (n, n, n, d))
    third = np.broadcast_to(spokes[None, None, :], (n, n, n, d))
    matrix = np.stack((first, second, third), axis=d).reshape(-1, d, d)
    turn = det(matrix)
    senses, _ = carry(n, d, 0)  # the Spokes along one axis, its + and its -
    weight, _ = carry(turn + turn * turn, senses, 0)
    return matrix, weight


def kinds(matrix: Z) -> Kinds:
    """The five kinds on each matrix of a stack of any shape, from the Spokes alone: T1 the turn, A2 and E from the axes it permutes."""
    e1, e2, e3 = axes(matrix.shape[-1])
    permutation = matrix * matrix
    sign = det(permutation)[..., None, None]
    plane = np.stack((e1 - e2, e2 - e3), axis=1)
    reading = np.stack((e1, e1 + e2))
    e = np.einsum("ij,...jk,kl->...il", reading, permutation, plane)
    return Kinds(0 * sign + 1, sign, e, matrix, sign * matrix)


def weighed(held: Kinds, weight: Z) -> Kinds:
    """Each kind's matrix on every candidate times the candidate's weight: the kinds on the 24, 0 on every other candidate, none set apart."""
    a1, a2, e, t1, t2 = held
    w = weight[:, None, None]
    return Kinds(w * a1, w * a2, w * e, w * t1, w * t2)


def beside(x: Z, y: Z) -> Z:
    """Two stacks of matrices set along one diagonal, every entry beside them 0."""
    gap = 0 * np.einsum("gij,gkl->gil", x, y)
    upper = np.concatenate((x, gap), axis=-1)
    return np.concatenate((upper, np.concatenate((np.swapaxes(gap, 1, -1), y), axis=-1)), axis=1)


def square(held: Kinds) -> Z:
    """The four-vector's symmetric square on each candidate, the stride fixed and the differences turned, on the index pairs 00, 0i, ii and jk (by the third axis): A1, T1, the axes' permutation and T2, each a signed permutation where the candidate is one of the 24; its first row, 00, the one row every turn fixes."""
    a1, _, _, t1, t2 = held
    return beside(beside(a1, t1), beside(t1 * t1, t2))


def placed(m: Z, side: int) -> Z:
    """A stack of matrices set in a square of the given side at its first rows and columns, every entry beside them 0."""
    put = np.eye(side, m.shape[-1], dtype=object)
    return np.einsum("ij,gjk,lk->gil", put, m, put)


def stacked(held: Kinds) -> Z:
    """The five kinds as one stack, (kinds, candidates, d, d), each set in the axes' square: one array for the tables."""
    a1, a2, e, t1, t2 = held
    side = t1.shape[-1]
    return np.stack(
        (placed(a1, side), placed(a2, side), placed(e, side), placed(t1, side), placed(t2, side))
    )


def pair(p: Z, q: Z) -> Z:
    """Whole numbers set as pairs (p, q) on a last axis, each standing for p + q r2 in Z[x] / (x^2 - senses)."""
    return np.stack((p, q), axis=-1)


def listed(words: Z) -> Z:
    """A stack of lifts with its leading axes read as one, each coordinate's pair kept."""
    p, q = np.moveaxis(words, -1, 0)
    return pair(p.reshape(-1, p.shape[-1]), q.reshape(-1, q.shape[-1]))


def hamilton(d: int) -> Z:
    """Hamilton's product on the unit's axis and the d Spokes' axes as pure units, made from the star, c[x, y, z] the z part of x y: the unit keeps every axis, a pure axis squares to the unit's opposite, and two pure axes make the third by the triple product of the three, det of the axes as rows."""
    unit = np.eye(1, d + 1, dtype=object)  # the unit's axis, ahead of the Spokes'
    pure = np.eye(d, d + 1, 1, dtype=object)  # each Spoke's axis as a pure unit
    matrix, _ = turns(axes(d))
    triple = det(matrix).reshape(d, d, d)
    kept = np.einsum("ux,yz->xyz", unit, axes(d + 1)) + np.einsum("ix,uy,iz->xyz", pure, unit, pure)
    squared = np.einsum("ix,iy,uz->xyz", pure, pure, unit)  # a pure axis times itself
    return kept - squared + np.einsum("ix,jy,kz,ijk->xyz", pure, pure, pure, triple)


def spread(c: Z, x: Z, y: Z) -> Z:
    """Hamilton's product of two stacks of whole coordinates."""
    return np.einsum("xyz,...x,...y->...z", c, x, y)


def times(c: Z, left: Z, right: Z, senses: Z) -> Z:
    """Hamilton's product of two stacks of pairs, not halved: (p + q r2)(r + s r2) = p r + senses q s + (p s + q r) r2 on every two coordinates."""
    p, q = np.moveaxis(left, -1, 0)
    r, s = np.moveaxis(right, -1, 0)
    return pair(spread(c, p, r) + senses * spread(c, q, s), spread(c, p, s) + spread(c, q, r))


def product(c: Z, left: Z, right: Z, senses: Z) -> Z:
    """Hamilton's product of two doubled lifts halved once by Rule3 at senses, itself a doubled lift: (2 g)(2 h) = senses 2 g h, the remainder 0."""
    whole, _ = carry(times(c, left, right, senses), senses, 0)
    return whole


def conjugate(c: Z, lift: Z) -> Z:
    """Each lift's conjugate, its inverse: every axis times its own square's unit part, + on the unit's axis and - on each pure one."""
    unit = np.eye(1, c.shape[-1], dtype=object)
    return np.einsum("xxz,uz,...xp->...xp", c, unit, lift)


def turned(c: Z, lift: Z, senses: Z) -> Z:
    """Each doubled lift's turn, its sandwich g v g* on every Spoke's axis v as a column: whole, (2 g) v (2 g)* being senses^2 times it, read by one carry with remainder 0 and no r2 part."""
    d = c.shape[-1] - 1
    pure = np.eye(d, d + 1, 1, dtype=object)
    g = lift[..., None, :, :]
    sandwich = times(c, times(c, g, pair(pure, 0 * pure), senses), conjugate(c, g), senses)
    rational, _ = np.moveaxis(sandwich, -1, 0)
    turn, _ = carry(np.einsum("...yx,ix->...iy", rational, pure), senses * senses, 0)
    return turn


def on_classes(c: Z, lift: Z, classes: Z, senses: Z) -> Z:
    """The 24-gear train, L(g) e_[h] = sign e_[gh] on the classes +-h in their order: g h's class is the one whose turn is its turn, each column's dot x of the two giving (x + x x) div senses, 1 where they agree and 0 elsewhere, multiplied over the columns; the sign is the doubled dot of g h with that class's word, senses^2 times the sign; every carry's remainder 0."""
    moved = product(c, lift[..., None, :, :], classes, senses)  # g h for every class h
    agree = np.einsum("...hij,kij->...khj", turned(c, moved, senses), turned(c, classes, senses))
    same, _ = carry(agree + agree * agree, senses, 0)
    p, q = np.moveaxis(moved, -1, 0)
    r, s = np.moveaxis(classes, -1, 0)
    dot = np.einsum("...hx,kx->...kh", p, r) + senses * np.einsum("...hx,kx->...kh", q, s)
    sign, _ = carry(np.prod(same, axis=-1) * dot, senses * senses, 0)
    return sign


def on_cosets(c: Z, lift: Z, heads: Z, senses: Z) -> Z:
    """The 8-gear train, L(g) on the cosets of C6, the powers of w, in the heads' order: a coset read through its vertex, its lifts' turn of (1, ..., 1), g v in the coset of the head u whose vertex agrees with its own on every axis, Rule3's weight (s + s s) div senses on each axis's product s of the two coordinates, exact for every whole s, multiplied over the axes; the sign is lam of u* g v in C6, +1 on C6's squares and -1 elsewhere on C6: its cube's doubled unit part halved, the squares being the cube roots of 1 and w^3 = -1; every carry's remainder 0."""
    moved = product(c, lift[..., None, :, :], heads, senses)  # g v for every head v
    vertex = np.einsum("...ij->...i", turned(c, moved, senses))
    agree = np.einsum("...vi,ui->...uvi", vertex, np.einsum("uij->ui", turned(c, heads, senses)))
    same, _ = carry(agree + agree * agree, senses, 0)
    # u* g v for every two heads
    h = product(c, conjugate(c, heads)[:, None], moved[..., None, :, :, :], senses)
    cube = product(c, product(c, h, h, senses), h, senses)
    real, _ = np.moveaxis(np.einsum("...xp,ux->...p", cube, np.eye(1, c.shape[-1], dtype=object)), -1, 0)
    lam, _ = carry(real, senses, 0)
    return np.prod(same, axis=-1) * lam


def lifts(spokes: Z) -> Lifts:
    """The 48 lifts of the board's 24 from the Node-clock's own star, each one word u w^k z^m: u one of the 4D star's 8 units, the unit and the Spokes' axes as pure units at both senses; w = (1 + i + j + k) / 2, the unit plus the three + Spokes halved, k below the axes' count; z = (1 + i) / r2, the unit plus a Spoke over r2, m below senses; two Hamilton products a word, each halved by Rule3 at senses with remainder 0: no search, no closure, no weight."""
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)  # the Spokes along one axis, its + and its -
    c = hamilton(d)
    unit, first, second, third = axes(d + 1)  # the unit's axis, then the Spokes' axes as pure units
    zero = 0 * unit
    one = pair(senses * unit, zero)  # 1, doubled
    w = pair(unit + first + second + third, zero)  # (1 + i + j + k) / 2, doubled
    z = pair(zero, unit + first)  # (1 + i) / r2, doubled: r2 + r2 i
    star = pair(senses * axes(d + 1), 0 * axes(d + 1))  # the 4D star's units at the + sense, doubled
    # the powers written out: Hamilton's product stands on the unit's axis and three Spokes' alone, where w^3 = -1
    # and z^2 = i, a word with no z (the tests read both by kinds.product)
    powers = np.stack((one, w, product(c, w, w, senses)))  # w^k, k below the axes' count
    spins = np.stack((one, z))  # z^m, m below senses
    words = product(c, star[:, None, None], powers[None, :, None], senses)  # u w^k
    classes = listed(product(c, words, spins[None, None, :], senses))  # u w^k z^m at the + sense
    lift = np.stack((classes, -classes))  # the - sense of u negates its word
    turn = turned(c, lift, senses)
    whole = kinds(turn)
    _, a2, e, _, _ = whole
    spin = np.einsum("...xp,x->...p", lift, unit)  # 2 Re g
    sign, trace = np.einsum("...ii->...", a2)[..., None], np.einsum("...ii->...", e)[..., None]
    halves = Halves(spin, sign * spin, trace * spin)
    # u z^m, one lift in each coset of C6
    heads = listed(product(c, star[:, None], spins[None, :], senses))
    cosets, classed = on_cosets(c, lift, heads, senses), on_classes(c, lift, classes, senses)
    return Lifts(whole, halves, cosets, classed)
