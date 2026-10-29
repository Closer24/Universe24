"""The board's 24 turns and the five kinds they act on, whole-number matrices made from the six Spokes, no table typed."""

from typing import NamedTuple

import numpy as np

from tensor24.algebra.carry import Z, carry


class Kinds(NamedTuple):
    """Each kind's matrix on every candidate turn, in the kinds' order; a candidate's weight is 1 on the 24 alone."""

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


def turns(unit: Z) -> tuple[Z, Z]:
    """Every matrix whose rows are three Spokes, weighed by Rule3: (det + det det) div an axis's Spokes is 1 at det 1, else 0."""
    spokes = np.concatenate((unit, -unit))
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


def projector(weight: Z, m: Z, i: Z, k: Z) -> Z:
    """The sum over the 24 of rho_m(g) x rho_i(g^-1) x rho_k(g^-1): at a seed (y, p, q), C[i, k -> m] from that seed."""
    return np.einsum("g,gxy,gpa,gqb->xabypq", weight, m, i, k)
