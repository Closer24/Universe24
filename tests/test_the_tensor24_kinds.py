"""Tensor24's kinds and tables: the 24 from the Spokes, the five kinds against the groups' own definitions, and C."""

import itertools
from typing import Any, NamedTuple

import numpy as np
import pytest

from tensor24.engine import kinds
from tensor24.main import made as joint
from tensor24.runner.load import common, tables

# Sofer's table (SOFER-KINDS-REFERENCE-1, scribe-5 d9d538ed4): the five characters on the five classes, the identity,
# the third turns, the face half turns, the quarter turns and the edge half turns, whose sizes are SIZES
SIZES = (1, 8, 3, 6, 6)
SOFER = {
    "A1": (1, 1, 1, 1, 1),
    "A2": (1, 1, 1, -1, -1),
    "E": (2, -1, 2, 0, 0),
    "T1": (3, 0, -1, 1, -1),
    "T2": (3, 0, -1, -1, 1),
}
LABELS = tuple(SOFER)
# David's products of two kinds other than A1 (6481240750, item 4), each multiplicity 0 or 1
PRODUCTS = {
    ("A2", "A2"): {"A1"},
    ("A2", "E"): {"E"},
    ("A2", "T1"): {"T2"},
    ("A2", "T2"): {"T1"},
    ("E", "E"): {"A1", "A2", "E"},
    ("E", "T1"): {"T1", "T2"},
    ("E", "T2"): {"T1", "T2"},
    ("T1", "T1"): {"A1", "E", "T1", "T2"},
    ("T2", "T2"): {"A1", "E", "T1", "T2"},
    ("T1", "T2"): {"A2", "E", "T1", "T2"},
}
EYE = np.eye(3, dtype=int)


class Made(NamedTuple):
    """What the load makes from the axes: the candidates, their weights, the kinds on each and on its inverse, and C."""

    matrix: Any
    weight: Any
    kinds: Any
    inverse: Any
    c: Any


def made():
    matrix, weight = kinds.turns(kinds.axes(3))
    ks, inverse = kinds.kinds(matrix), kinds.kinds(kinds.inverse(matrix))
    return Made(matrix, weight, ks, inverse, tables(ks, inverse, weight, kinds.projector))


def product(a, b):
    """David's product of two kinds: A1 x X = X, the rest by his list, in either order."""
    if "A1" in (a, b):
        return {b if a == "A1" else a}
    return PRODUCTS.get((a, b)) or PRODUCTS[(b, a)]


def the24(m):
    """The candidates of weight 1, and each one's index by its matrix."""
    keep = [g for g in range(len(m.weight)) if m.weight[g] == 1]
    return keep, {tuple(m.matrix[g].flat): g for g in keep}


def klass(t):
    """A turn's class by its trace and its form: the identity, a third, a face half, a quarter, an edge half turn."""
    trace, diagonal = int(np.trace(t)), not (t - np.diag(np.diag(t))).any()
    if (t == EYE).all():
        return 0
    if trace == 0:
        return 1
    if trace == 1:
        return 3
    return 2 if diagonal else 4


def chi(m):
    """Each kind's character on the 24."""
    keep, _ = the24(m)
    return {
        label: np.array([np.trace(rho[g]) for g in keep], dtype=object)
        for label, rho in zip(LABELS, m.kinds, strict=True)
    }


def group(m):
    """The 24 are a group of determinant 1, their order Sofer's: every product, every inverse and the identity among them."""
    keep, index = the24(m)
    products = all(
        tuple((m.matrix[g] @ m.matrix[h]).flat) in index for g, h in itertools.product(keep, repeat=2)
    )
    inverses = all(tuple(m.matrix[g].T.flat) in index for g in keep)
    return products and inverses and len(keep) == sum(SIZES) and all(kinds.det(m.matrix[keep]) == 1)


def forms(m):
    """On the 24: A1 is 1, T1 the turn itself, A2 the sign of its axes' permutation, T2 their product (stored(m)'s blocks)."""
    keep, _ = the24(m)
    a1, a2, _, t1, t2 = m.kinds
    for g in keep:
        sign = round(np.linalg.det(np.abs(np.array(m.matrix[g], dtype=int))))
        if not ((a1[g] == 1).all() and (a2[g] == sign).all() and (t1[g] == m.matrix[g]).all()):
            return False
        if not (t2[g] == sign * m.matrix[g]).all():
            return False
    return True


def representations(m):
    """Each kind is a representation on all 576 pairs, and its inverse's matrices are the inverse turn's."""
    keep, index = the24(m)
    for rho, inverse in zip(m.kinds, m.inverse, strict=True):
        for g, h in itertools.product(keep, repeat=2):
            if not (rho[g] @ rho[h] == rho[index[tuple((m.matrix[g] @ m.matrix[h]).flat)]]).all():
                return False
        if not all((inverse[g] == rho[index[tuple(m.matrix[g].T.flat)]]).all() for g in keep):
            return False
    return True


def reference(t):
    """Sofer's definitions, written anew: A2 by the four body diagonals, E by the six faces, T1 by the trace."""
    diagonals = [np.array(s) for s in itertools.product((1, -1), repeat=3) if s[0] == 1]
    image = [
        next(j for j, e in enumerate(diagonals) if (t @ d == e).all() or (t @ d == -e).all())
        for d in diagonals
    ]
    a2 = int(round(np.linalg.det(np.eye(len(diagonals))[image])))
    t1 = int(np.trace(t))
    faces = sum(int((t @ f == f).all()) for f in np.concatenate([EYE, -EYE]))
    return {"A1": 1, "A2": a2, "E": faces - 1 - t1, "T1": t1, "T2": t1 * a2}


def characters(m):
    """Each kind's character is Sofer's by his definitions at every turn, and his table on every class, of his sizes."""
    keep, _ = the24(m)
    seen: dict[str, dict[int, set[int]]] = {label: {} for label in LABELS}
    for g in keep:
        t = np.array(m.matrix[g], dtype=int)
        want = reference(t)
        for label, rho in zip(LABELS, m.kinds, strict=True):
            if int(np.trace(rho[g])) != want[label]:
                return False
            seen[label].setdefault(klass(t), set()).add(int(np.trace(rho[g])))
    sizes = tuple(
        sum(klass(np.array(m.matrix[g], dtype=int)) == c for g in keep) for c in range(len(SIZES))
    )
    return sizes == SIZES and all(
        seen[label] == {c: {x} for c, x in enumerate(SOFER[label])} for label in LABELS
    )


def orthonormal(m):
    """The five characters are orthonormal over the 24: the sum of a product is the order on one kind, 0 between two."""
    x, order = chi(m), len(the24(m)[0])
    return all(
        int((x[a] * x[b]).sum()) == order * (a == b) for a, b in itertools.product(LABELS, repeat=2)
    )


def spokes(m):
    """The six Spokes' permutation character is A1 + E + T1, and the three axes' is A1 + E."""
    keep, _ = the24(m)
    x = chi(m)
    fixed = [sum(int((m.matrix[g] @ s == s).all()) for s in np.concatenate([EYE, -EYE])) for g in keep]
    axes = [int(np.trace(m.matrix[g] * m.matrix[g])) for g in keep]
    return fixed == list(x["A1"] + x["E"] + x["T1"]) and axes == list(x["A1"] + x["E"])


def channels(m):
    """C is 0 exactly where the characters' product holds no channel, as David lists them; each C not 0 primitive, its first entry positive."""
    x, order = chi(m), len(the24(m)[0])
    for i, k, n in itertools.product(LABELS, repeat=3):
        c = m.c[(LABELS.index(i), LABELS.index(k), LABELS.index(n))]
        wanted = n in product(i, k)
        if int((x[i] * x[k] * x[n]).sum()) != order * wanted or bool(c.any()) != wanted:
            return False
        if wanted and (common(c.flat) != 1 or next(x for x in c.flat if x) < 0):
            return False
    return True


def equivariant(m):
    """Every C is kept by every one of the 24: rho_m(g) C (rho_i(g^-1) x rho_k(g^-1)) = C."""
    keep, _ = the24(m)
    for (i, k, n), c in m.c.items():
        for g in keep:
            if not (
                np.einsum("xy,ypq,pa,qb->xab", m.kinds[n][g], c, m.inverse[i][g], m.inverse[k][g]) == c
            ).all():
                return False
    return True


def classical(m):
    """The dot, the cross and the plain product of A2 and T1 are C's tables exactly."""
    a1, a2, t1, t2 = (LABELS.index(label) for label in ("A1", "A2", "T1", "T2"))
    cross = np.zeros((3, 3, 3), dtype=int)
    for x, a, b in itertools.permutations(range(3)):
        cross[x, a, b] = 1 if (x, a, b) in ((0, 1, 2), (1, 2, 0), (2, 0, 1)) else -1
    return (
        (m.c[(t1, t1, a1)][0] == EYE).all()
        and (m.c[(t1, t1, t1)] == cross).all()
        and (m.c[(a2, t1, t2)][:, 0, :] == EYE).all()
    )


LAWS = {
    law.__name__: law
    for law in (
        group,
        forms,
        representations,
        characters,
        orthonormal,
        spokes,
        channels,
        equivariant,
        classical,
    )
}


def mutants():
    """Broken copies of what the load makes, each with the law that must catch it (David's four among them)."""

    def kind(m, label, f):
        changed = list(m.kinds)
        changed[LABELS.index(label)] = f(m, np.array(changed[LABELS.index(label)]))
        return m._replace(kinds=type(m.kinds)(*changed))

    def table(m, key, f):
        c = dict(m.c)
        c[tuple(LABELS.index(label) for label in key)] = f(
            np.array(c[tuple(LABELS.index(label) for label in key)])
        )
        return m._replace(c=c)

    def entry(m, x):
        x[:, 0, 0] += 1
        return x

    def at_identity(m, x):
        x[the24(m)[1][tuple(EYE.flat)], 0, 0] += 1
        return x

    def beside(m, x):
        x[:, 0, 0], x[:, 0, 1], x[:, 1, 0], x[:, 1, 1] = 1, 0, 0, m.kinds[LABELS.index("A2")][:, 0, 0]
        return x

    def bumped(x):
        x.flat[1] += 1
        return x

    def first_seed(m):
        held = {}
        for key, c in m.c.items():
            p = kinds.projector(m.weight, m.kinds[key[-1]], m.inverse[key[0]], m.inverse[key[1]])
            seeds = p.reshape(c.size, -1).T
            held[key] = next((seed for seed in seeds if seed.any()), seeds[0]).reshape(c.shape)
        return m._replace(c=held)

    def cycled(m, x):
        cycle = np.roll(EYE, 1, axis=0)
        return np.einsum("ij,gjk,lk->gil", cycle, x, cycle)

    def one_seed(m):
        sums = {
            key: kinds.projector(m.weight, m.kinds[key[-1]], m.inverse[key[0]], m.inverse[key[1]])
            for key in m.c
        }
        return m._replace(c={key: p.sum(axis=(3, 4, 5)) for key, p in sums.items()})

    return {
        "the reflections weighed in": (
            "group",
            lambda m: m._replace(weight=kinds.det(m.matrix) * kinds.det(m.matrix)),
        ),
        "a kind's matrix entry changed": ("representations", lambda m: kind(m, "E", entry)),
        "T1 and T2 turned by a third turn of the axes": (
            "forms",
            lambda m: kind(kind(m, "T1", cycled), "T2", cycled),
        ),
        "a character changed by one": ("characters", lambda m: kind(m, "E", at_identity)),
        "T2 as T1": (
            "characters",
            lambda m: kind(m, "T2", lambda m, x: np.array(m.kinds[LABELS.index("T1")])),
        ),
        "A2's sign dropped": ("orthonormal", lambda m: kind(m, "A2", lambda m, x: 0 * x + 1)),
        "E as A1 beside A2": ("spokes", lambda m: kind(m, "E", beside)),
        "C from one fixed seed of ones": ("channels", one_seed),
        "the cross doubled, not primitive": (
            "channels",
            lambda m: table(m, ("T1", "T1", "T1"), lambda x: x + x),
        ),
        "the first seed's group sum, its content kept": ("channels", first_seed),
        "the cross's sign turned": ("channels", lambda m: table(m, ("T1", "T1", "T1"), lambda x: -x)),
        "an entry of C changed": ("equivariant", lambda m: table(m, ("T1", "T1", "T1"), bumped)),
        "the dot negated": ("classical", lambda m: table(m, ("T1", "T1", "A1"), lambda x: -x)),
    }


@pytest.fixture(scope="module")
def good():
    return made()


def test_every_law_holds_on_the_kinds_as_made(good):
    assert all(law(good) for law in LAWS.values())


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_law_of_the_kinds_fails_on_its_mutant(mutant, good):
    name, broken = mutants()[mutant]
    assert LAWS[name](good)
    assert not LAWS[name](broken(good))


def test_the_joint_makes_the_kinds_and_the_tables_the_load_reads(good):
    """main.made, the one joint, gives these kinds and tables: its inverses the turns' own, so every table is kept."""
    held, c = joint((4, 4, 4))
    assert all((x == y).all() for x, y in zip(held, good.kinds, strict=True))
    assert c.keys() == good.c.keys() and all((c[key] == good.c[key]).all() for key in c)
