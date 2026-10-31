"""Tensor24's lifts: the 48 as the words u w^k z^m on the Node-clock's star, their turns and kinds, and the two half-speed trains."""

import itertools
import json
from pathlib import Path

import numpy as np

from tensor24.algebra.carry import carry
from tensor24.engine import kinds
from tensor24.main import made
from tensor24.runner.files import vocabulary
from tensor24.runner.load import star

PIECE = Path(__file__).resolve().parents[1].joinpath("examples", "tensor24", "piece.json")
# Hamilton's table written out, "x y z sign" for x y = sign z on the unit's axis and i, j, k: i i = j j = k k = i j k = -1
WRITTEN = "000+ 110- 220- 330- 011+ 101+ 231+ 321- 022+ 132- 202+ 312+ 033+ 123+ 213- 303+"
TABLE = [(int(x), int(y), int(z), int(sign + "1")) for x, y, z, sign in WRITTEN.split()]


def built():
    """The lifts from the piece's own star, its senses, and the 48 listed in their order, each a tuple of pairs."""
    spokes = star(len(json.loads(PIECE.read_text(encoding="utf-8"))["shape"]))
    held, (senses, _) = kinds.lifts(spokes), carry(*spokes.shape, 0)
    return held, senses, [tuple(map(tuple, g)) for g in held.lift.reshape(-1, *held.lift.shape[-2:])]


def ring(x, y, senses):
    """Two pairs' product in Z[x] / (x^2 - senses)."""
    return np.array((x[0] * y[0] + senses * x[1] * y[1], x[0] * y[1] + x[1] * y[0]), dtype=object)


def mul(g, h, senses):
    """Two doubled lifts' product by the written-out table, halved once by Rule3: it, and whether no remainder is left."""
    out = np.zeros((len(g), 2), dtype=object)
    for x, y, z, sign in TABLE:
        out[z] += sign * ring(g[x], h[y], senses)
    whole, rest = carry(out, senses, 0)
    return tuple(map(tuple, whole)), not rest.any()


def closed(generators, one, senses):
    """The probe's closure: every product of the generators from 1, breadth first, by the written-out product."""
    found, edge = {one}, {one}
    while edge:
        edge = {mul(g, h, senses)[0] for g in edge for h in generators} - found
        found |= edge
    return found


def sandwich(g, senses):
    """The probe's turn of a doubled lift: g v g* on each pure axis v as a column, by the written-out product, whole."""
    conjugate, columns = (g[0], *((-p, -q) for p, q in g[1:])), []
    for axis in range(1, len(g)):
        v = tuple((senses * (x == axis), 0) for x in range(len(g)))
        moved, _ = mul(mul(g, v, senses)[0], conjugate, senses)
        columns.append([carry(p, senses, 0)[0] for p, _ in moved[1:]])
    return np.array(columns, dtype=object).T


def same_train(train, heads, table, members, lam):
    """The train is the probe's Ind_H(lam), the cosets g H in the lifts' order each held by its first lift, up to its gears'
    order and senses: the signed permutation taking each probe coset to the gear whose head lies in it, at lam of its place."""
    reps, where = [], {}
    for g in range(len(table)):
        if g not in where:
            where.update({table[g][h]: (len(reps), h) for h in members})
            reps.append(g)
    probe = np.zeros((len(table), len(reps), len(reps)), dtype=object)
    for g, (c, r) in itertools.product(range(len(table)), enumerate(reps)):
        moved, h = where[table[g][r]]
        probe[g, moved, c] = lam[h]
    turn = np.zeros((len(heads), len(reps)), dtype=object)
    for v, head in enumerate(heads):
        c, h = where[head]
        turn[v, c] = lam[h]
    flat = train.reshape(len(table), len(heads), len(heads))
    return bool((abs(turn).sum(axis=0) == 1).all() and (flat == turn @ probe @ turn.T).all())


def test_the_48_are_the_words_each_once_of_norm_senses_squared_and_the_probes_closure(monkeypatch):
    """Yes: Hamilton's product from the star the written-out table, the 48 the words u w^k z^m in their layout, each once,
    of doubled norm senses^2, w^d = -1 and z^senses = i, every carry exact, every product a lift, the closure of z and w the 48.
    No: with no z, the closure of w and the star's units stops at Hurwitz's 24, the words with m = 0."""
    held, senses, listed = built()
    d = held.turn.shape[-1]
    written = np.zeros((d + 1, d + 1, d + 1), dtype=object)
    for x, y, z, sign in TABLE:
        written[x, y, z] = sign
    assert (kinds.hamilton(d) == written).all()
    assert (
        len(set(listed)) == len(listed) == senses * int(kinds.turns(star(d))[1].sum())
    )  # two lifts a turn
    flat = held.lift.reshape(len(listed), d + 1, -1)
    p, q = np.moveaxis(flat, -1, 0)
    norm = (p * p + senses * q * q).sum(axis=-1), (p * q).sum(axis=-1)
    assert (norm[0] == senses * senses).all() and not norm[1].any()
    _, rest = carry(kinds.times(written, flat[:, None], flat[None, :], senses), senses, 0)
    products = kinds.product(written, flat[:, None], flat[None, :], senses).reshape(-1, *flat.shape[1:])
    assert not rest.any() and {tuple(map(tuple, g)) for g in products} == set(listed)
    units = [tuple((senses * (x == y), 0) for y in range(d + 1)) for x in range(d + 1)]
    one, i, j, _ = units
    w, z = ((1, 0),) * (d + 1), ((0, 1), (0, 1)) + ((0, 0),) * (d - 1)
    assert (listed[0], listed[1], listed[senses]) == (one, z, w)  # the words 1, z and w
    cube, square = (np.array(one, dtype=object),) * 2  # the stacks' lengths read off the structure
    for _ in range(d):
        cube = kinds.product(written, cube, np.array(w, dtype=object), senses)
    for _ in range(senses):
        square = kinds.product(written, square, np.array(z, dtype=object), senses)
    assert (cube == -np.array(one, dtype=object)).all() and (square == np.array(i, dtype=object)).all()
    words = []  # each lift its word u w^k z^m by the written-out product, at both senses in the layout's order
    for sense, u, k, m in itertools.product((1, -1), units, range(d), range(senses)):
        g = tuple((sense * x, sense * y) for x, y in u)
        for h in (w,) * k + (z,) * m:
            g, _ = mul(g, h, senses)
        words.append(g)
    assert words == listed
    assert closed((z, w), one, senses) == set(listed)
    assert all(mul(g, h, senses)[1] for g in listed for h in listed)
    hurwitz = closed((i, j, w), one, senses)
    assert hurwitz == set(listed[::senses]) and senses * len(hurwitz) == len(listed)
    heads = [listed[a * d * senses + m] for a in range(d + 1) for m in range(senses)]
    assert [tuple(map(tuple, h)) for h in held.heads] == heads
    rests = []  # every carry the lifts make, product, turned, on_classes and on_cosets among them

    def kept(n, teeth, r):
        whole, rest = carry(n, teeth, r)
        rests.append(rest)
        return whole, rest

    monkeypatch.setattr(kinds, "carry", kept)
    kinds.lifts(star(d))
    assert rests and not any(np.any(rest) for rest in rests)  # each exact, its remainder 0


def test_each_lift_turns_the_axes_by_one_of_the_24_and_the_eight_kinds_are_orthonormal_on_the_48():
    """Yes: main.made passes these lifts, the files' vocabulary reads them; each lift's turn its sandwich, g and -g on one
    turn, each of the 24 once a sense; the eight kinds orthonormal on the 48 exactly, the full turn +1 on five, -1 on three.
    No: no lift's turn is a reflection or a flat candidate, each weighed 0 by kinds.turns."""
    held, senses, listed = built()
    d = held.turn.shape[-1]
    five, _, square, joint = made(star(d))
    parts = [(*g[:2], *g.whole, *g.halves, g.heads, g.cosets, g.classes) for g in (joint, held)]
    assert all((x == y).all() for x, y in zip(*parts, strict=True))  # every field of the lifts alike
    read = vocabulary(five, square, joint)[-1][-1]  # the files read these lifts' half-speed kinds
    assert (read.characters[len(five) :] == np.stack(joint.halves)).all()
    turns = held.turn.reshape(-1, d, d)
    assert all((t == sandwich(g, senses)).all() for t, g in zip(turns, listed, strict=True))
    assert (held.whole.t1 == held.turn).all()  # T1 on the 48 each lift's turn
    weighed = list(zip(*kinds.turns(star(d)), strict=True))
    kept, left = ({tuple(m.flat) for m, w in weighed if w == on} for on in (1, 0))
    assert [{tuple(t.flat) for t in sense} for sense in held.turn] == [kept] * senses
    assert len(held.turn[0]) == len(kept) and (held.turn[0] == held.turn[-1]).all()
    assert not left & {tuple(t.flat) for t in turns}
    traces = [np.einsum("...ii->...", k).reshape(-1) for k in held.whole]
    halves = [h.reshape(len(listed), -1) for h in held.halves]
    chi = [np.stack((t, 0 * t), axis=-1) for t in traces] + halves
    p, q = np.moveaxis(np.array(chi), -1, 0)  # every two characters' sum over the 48, as a pair
    gram = p @ p.T + senses * q @ q.T, p @ q.T + q @ p.T
    assert (gram[0] == len(listed) * np.eye(len(chi), dtype=object)).all() and not gram[1].any()
    e, m1 = listed.index(listed[0]), listed.index(tuple((-x, -y) for x, y in listed[0]))
    whole = len(held.whole)
    turned = [tuple(c[e]) for c in chi[:whole]] + [tuple(-c[e]) for c in chi[whole:]]
    assert [tuple(c[m1]) for c in chi] == turned


def test_the_two_trains_are_the_probes_induced_ones_and_read_the_class_and_sign_of_every_product():
    """Yes: the 24-gear train the probe's Ind_{+-1}(sign) and the 8-gear its Ind_C6(lam), up to their gears' order and senses,
    each -I on the full turn, the half-speed kinds each by its degree and G3/2 twice; every product's class and sign read.
    No: either train with two gears swapped on one side is no train, its product not the product's matrix."""
    held, senses, listed = built()
    index = {g: n for n, g in enumerate(listed)}
    table = np.array([[index[mul(g, h, senses)[0]] for h in listed] for g in listed])
    e, w = index[listed[0]], index[((1, 0),) * len(listed[0])]
    m1 = index[tuple((-x, -y) for x, y in listed[0])]
    c6, x = [e], table[e][w]
    while x != e:
        c6, x = [*c6, x], table[x][w]
    # lam: +1 on the squares of C6, the product table's diagonal there, -1 elsewhere on C6
    lam = {x: 1 if x in {table[y][y] for y in c6} else -1 for x in c6}
    heads, k = [index[tuple(map(tuple, h))] for h in held.heads], held.lift.shape[1]
    assert same_train(held.cosets, heads, table, c6, lam)
    assert same_train(held.classes, list(range(k)), table, (e, m1), {e: 1, m1: -1})
    eight = held.cosets.reshape(len(listed), len(heads), -1)
    classes = held.classes.reshape(len(listed), k, k)
    assert (eight[m1] == -np.eye(len(heads), dtype=object)).all()
    assert (classes[m1] == -np.eye(k, dtype=object)).all()
    halves = [h.reshape(len(listed), -1) for h in held.halves]
    for train, chi in ((classes, sum(h[e][0] * h for h in halves)), (eight, halves[-1] + halves[-1])):
        assert (np.einsum("gii->g", train) == chi[:, 0]).all() and not chi[:, 1].any()
    # each lift as its sense times its class's gear
    basis = np.concatenate((np.eye(k, dtype=object), -np.eye(k, dtype=object)))
    assert (np.einsum("aij,bj->abi", classes, basis) == basis[table]).all()
    assert (np.einsum("aij,bjk->abik", eight, eight) == eight[table]).all()
    for train in (classes, eight):
        swapped = train[:, [1, 0, *range(2, train.shape[-1])]]
        assert not (np.einsum("aij,bjk->abik", swapped, swapped) == swapped[table]).all()
