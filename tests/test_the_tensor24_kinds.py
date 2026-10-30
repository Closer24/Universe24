"""Tensor24's kinds and tables: the 24 from the Node-clock's star, the five kinds its representations, C its channels."""

import itertools

import numpy as np

from tensor24.engine import kinds
from tensor24.main import made as joint
from tensor24.runner.files import AXES
from tensor24.runner.load import star, tables


def forms(held, matrix, keep):
    """On the 24: A1 is 1, T1 the turn itself, A2 a sign and T2 the two together."""
    a1, a2, _, t1, t2 = (k[keep] for k in held)
    return bool(
        (a1 == 1).all() and (t1 == matrix[keep]).all() and (a2 * a2 == 1).all() and (t2 == a2 * t1).all()
    )


def characters(held, keep):
    """Each kind's trace on each of the 24, as whole numbers."""
    return np.array([np.einsum("gii->g", k[keep]) for k in held]).astype(int)


def squared(matrix, keep, held, d):
    """The four-vector's symmetric square of each turn on the pairs 00, 0i, ii and jk by the third axis, built anew."""
    one = range(1, d + 1)
    jk = (tuple(j for j in one if j != i) for i in one)
    p, q = np.array([(0, 0), *((0, i) for i in one), *((i, i) for i in one), *jk]).T
    four = np.array([np.pad(t, ((1, 0), (1, 0))) for t in matrix[keep]])
    four[:, 0, 0] = 1  # the stride fixed
    rows = np.einsum("gpm,gqn->gpqmn", four, four)[:, p, q]
    return (kinds.square(held)[keep] == rows[:, :, p, q] + (p != q) * rows[:, :, q, p]).all()


def test_the_24_are_the_stars_turns_the_kinds_their_representations_and_the_tables_their_channels():
    """Yes: the turns a group, each kind a representation, the five orthonormal and all of them, T1 the turn itself,
    the tables kept by the 24 on exactly the channels, the square the four-vector's, the joint the same.
    No: the reflections and the flat candidates weigh 0, and no table stands where no channel does."""
    d = len(AXES)
    spokes = star(d)
    matrix, weight = kinds.turns(spokes)
    held, inverse = kinds.kinds(matrix), kinds.kinds(kinds.inverse(matrix))
    c = tables(kinds.stacked(held), kinds.stacked(inverse), weight)
    keep = np.flatnonzero(weight)
    assert (weight == (kinds.det(matrix) == 1)).all()  # the 24 kept, every other candidate left
    index = {tuple(matrix[g].flat): g for g in keep}
    pairs = list(itertools.product(keep, keep))
    products = [index.get(tuple((matrix[g] @ matrix[h]).flat)) for g, h in pairs]
    assert None not in products and all(tuple(matrix[g].T.flat) in index for g in keep)
    for rho, back in zip(held, inverse, strict=True):
        assert all(
            (rho[g] @ rho[h] == rho[gh]).all() for (g, h), gh in zip(pairs, products, strict=True)
        )
        assert all((back[g] == rho[index[tuple(matrix[g].T.flat)]]).all() for g in keep)
    chi, order = characters(held, keep), len(keep)
    assert (chi @ chi.T == order * np.eye(len(held), dtype=int)).all()
    # the eighth review (927071a14): T1 and T2 turned by a third turn of the axes kept every character and survived
    assert sum(k.shape[-1] * k.shape[-1] for k in held) == order and forms(held, matrix, keep)
    out, into = kinds.stacked(held)[:, keep], kinds.stacked(inverse)[:, keep]
    for i, k, m in np.ndindex(c.shape[: c.ndim - d]):  # each two kinds in, one out
        table = c[i, k, m]
        kept = np.einsum("gxy,ypq,gpa,gqb->gxab", out[m], table, into[i], into[k]) == table[None]
        assert kept.all() and bool(table.any()) == bool((chi[i] * chi[k] * chi[m]).sum())
        lead = table.flat[np.flatnonzero(table)[:1]]  # the first entry not 0, where one stands
        assert np.gcd.reduce(table.astype(int).ravel()) == table.any() and (lead > 0).all()
    labels = [name.upper() for name in held._fields]
    a1, a2, t1, t2 = (labels.index(name) for name in ("A1", "A2", "T1", "T2"))
    eye = np.eye(d, dtype=int)
    cross = np.moveaxis(np.cross(eye[:, None], eye[None, :]), -1, 0)  # its x component of e_a x e_b
    assert (c[t1, t1, a1][0] == eye).all() and (c[t1, t1, t1] == cross).all()
    assert (c[a2, t1, t2][:, 0] == eye).all()
    fixed = np.einsum("gii->i", kinds.square(held)[keep]) == order  # the rows every turn fixes: 00 alone
    assert squared(matrix, keep, held, d) and fixed[0] and fixed.sum() == 1
    # the eighth review (927071a14): main.made passing the turns as their own inverses survived every test
    turned, made_c, square = joint(spokes)
    w = weight[:, None, None]
    assert all((x == w * y).all() for x, y in zip(turned, held, strict=True)) and (made_c == c).all()
    assert (square == w * kinds.square(held)).all()
