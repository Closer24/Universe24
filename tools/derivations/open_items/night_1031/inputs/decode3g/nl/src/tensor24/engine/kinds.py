"""Clock: every Node-clock is made alike from its star of six Spokes: the 24 turns that leave the star the same, and the five kinds by which a train's gears turn with them.
Algebra: the 24 are the matrices of three Spokes that Rule3's weight keeps, 24 of 216; A1, A2, E, T1 and T2 are built from their matrices, with no table typed.
Board: the same turns and kinds at every Node-clock; the four-vector's square (the 00, 0i, ii and jk slots) is the metric family's kinds.
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


def det(m: Z) -> Z:
    """Each matrix's determinant, the triple product of its three rows."""
    a, b, c = np.moveaxis(m, 1, 0)
    a0, a1, a2 = a.T
    b0, b1, b2 = b.T
    c0, c1, c2 = c.T
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
    """The five kinds on each matrix, from the Spokes alone: T1 the turn, A2 and E from the axes it permutes."""
    e1, e2, e3 = axes(matrix.shape[-1])
    permutation = matrix * matrix
    sign = det(permutation)[:, None, None]
    plane = np.stack((e1 - e2, e2 - e3), axis=1)
    reading = np.stack((e1, e1 + e2))
    e = np.einsum("ij,gjk,kl->gil", reading, permutation, plane)
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
