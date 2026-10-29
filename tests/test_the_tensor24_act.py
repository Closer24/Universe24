"""Tensor24's one act on every gear at its coefficients: the drive, the kick and the force against a naive model, the run
back, and the sources' images under the 24, each law failing on its mutant."""

import itertools

import numpy as np
import pytest

from tensor24.engine import contract, mesh, step
from tensor24.engine.state import Gearing, Layout, Plan, State
from tensor24.main import made
from tensor24.runner.load import load
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests.frame import board, flat, meshes_of, near, same, stored, turns, wide

SHAPE, GAMMA, ROUNDS = (3, 4, 5), 9, 12  # the board, the full rate, the rounds of the run back
# the gears per site, J's terms, and the readings: the value, the three differences and the force
ROWS, TERMS, PLANES = 4, 30, 1 + 3 + 1
CUBE = (3, 3, 3)  # the board the 24 turn
TRAINS = [
    {"name": n, "kinds": [k], "part": 1} for n, k in zip("spva", ("A1", "A2", "T1", "T2"), strict=True)
]
# (train, kind, part, operand) twice, then (target, kind, part) and the strength; the operands 0 value, 1 gradient, 2 pull
COUPLINGS = [
    [0, 0, 0, 1, 2, 0, 0, 0, 0, 0, 0, 3],  # the scalar's gradient with the vector, into the scalar
    [2, 0, 0, 2, 2, 0, 0, 0, 2, 0, 0, 5],  # the vector's force crossed with the vector, into the vector
    [1, 0, 0, 0, 2, 0, 0, 0, 3, 0, 0, 7],  # the pseudoscalar times the vector, into the axial
    [0, 0, 0, 1, 1, 0, 0, 0, 3, 0, 0, 2],  # the scalar's gradient times the pseudoscalar, into the axial
    [3, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 1],  # the axial with the vector, into the vector
]


def draw(rng, low, high, size):
    return rng.integers(low, high, size=size).astype(object)


def varied(rng, alike=False):
    """A layout parted at every gear and site: grips per train and Mesh, W and W+ (alike, or parted), s, D, T_k, T_d, J."""
    nb = board(SHAPE)
    n = nb.shape[1]
    w = draw(rng, 1, 20, (ROWS, n))
    coefficients = (
        draw(rng, -3, 4, (ROWS, n)),
        draw(rng, -3, 4, (ROWS, 1)),
        draw(rng, -5, 6, (ROWS, 1)),
    )
    gearing = Gearing(
        w, w if alike else draw(rng, 1, 20, (ROWS, n)), *coefficients, draw(rng, 1, 9, (ROWS, 1))
    )
    index = [
        rng.integers(0, high, size=TERMS).astype(np.intp) for high in (PLANES * ROWS,) * 2 + (ROWS,)
    ]
    plan = Plan(index[0], index[1], draw(rng, -9, 10, TERMS), index[2])
    grip, rate = draw(rng, -3, 4, (ROWS, 3 * n)), draw(rng, 0, GAMMA + 1, (1, n))
    return Layout(nb, meshes_of(nb), grip, gearing, plan, rate, GAMMA)


def world(rng, layout, rows=ROWS):
    """A state the act may meet: gears across 2**256, each tooth within its W, each drive's tooth within its T_d."""
    w, drive = np.broadcast_to(layout.gearing.w, (rows, layout.nb.shape[1])), layout.gearing.drive
    size, one = w.shape, (1, w.shape[1])
    c = draw(rng, 0, 2, one)
    teeth = (draw(rng, 0, 1 << 20, size) % w, draw(rng, 0, 2, size), draw(rng, 0, 1 << 20, size) % drive)
    return State(
        wide(rng, size), wide(rng, size), *teeth, draw(rng, 0, GAMMA, one), c, c - draw(rng, 0, 2, one)
    )


def naive(layout, s, mask):
    """The act site by site with loops and plain integers: the readings, J term by term, the drive, the push, the carry."""
    _, _, grip, gearing, plan, rate, gamma = layout
    rows = len(s.a)
    w, wp, stretch, spring, kick, drive = (np.broadcast_to(x, s.a.shape).tolist() for x in gearing)
    first, second, factor, target = (x.tolist() for x in plan)
    a, b, r, go, rd = (x.tolist() for x in s[:5])
    (ph,), (c,), (tn,), (mask,), (rate,), grip = (x.tolist() for x in (*s[5:], mask, rate, grip))
    n = len(c)
    new = [[row[:] for row in x] for x in (a, b, r, go, rd, [ph], [c], [tn])]
    fire, k = [0] * n, [0] * n
    for x in itertools.product(*map(range, SHAPE)):
        i, around = (
            np.ravel_multi_index(x, SHAPE),
            [np.ravel_multi_index(y, SHAPE) for y in near(x, SHAPE)],
        )
        spokes = [axis * n + j for axis in range(3) for j in (i, around[axis + axis + 1])]
        fire[i] = mask[i] * int(all(c[j] >= c[i] for j in around))
        k[i], new[5][0][i] = divmod(ph[i] + rate[i], gamma) if fire[i] else (0, ph[i])
        new[6][0][i] = c[i] + fire[i]
        seen = [[a[g][j] if c[i] >= tn[j] else b[g][j] for j in around] for g in range(rows)]
        force = [
            sum(grip[g][m] * (v - a[g][i]) for m, v in zip(spokes, seen[g], strict=True))
            - spring[g][i] * a[g][i]
            for g in range(rows)
        ]
        readings = [a[g][i] for g in range(rows)]
        readings += [
            seen[g][axis + axis] - seen[g][axis + axis + 1] for axis in range(3) for g in range(rows)
        ]
        source = [0] * rows
        for t in range(len(factor)):
            source[target[t]] += factor[t] * (readings + force)[first[t]] * (readings + force)[second[t]]
        for g in range(rows if k[i] else 0):
            q, new[4][g][i] = divmod(source[g] + rd[g][i], drive[g][i])
            p = w[g][i] * (a[g][i] - b[g][i]) + r[g][i] - (w[g][i] - go[g][i]) // 2
            push = stretch[g][i] * (force[g] + kick[g][i] * q)
            v, new[2][g][i] = divmod(p + push + (wp[g][i] - go[g][i]) // 2, wp[g][i])
            new[0][g][i], new[1][g][i] = a[g][i] + v, a[g][i]
        new[7][0][i] = new[6][0][i] if k[i] else tn[i]
    return State(*(np.array(x, dtype=object) for x in new)), tuple(
        np.array([x], dtype=object) for x in (fire, k, tn)
    )


def formula():
    """At varied layouts, W and W+ parted, the act under a random mask equals the naive model at every entry, three seeds."""
    for seed in range(3):
        rng = np.random.default_rng(seed)
        layout = varied(rng)
        s, mask = world(rng, layout), draw(rng, 0, 2, (1, layout.nb.shape[1]))
        if not same(flat(step.tick(layout, s, mask)), flat(naive(layout, s, mask))):
            return False
    return True


def back():
    """Rounds under random masks run back to the start bit for bit, W and W+ alike; one round with them parted, alike."""
    for seed in range(3):
        rng = np.random.default_rng(10 + seed)
        layout, parted = varied(rng, alike=True), varied(rng)
        s, t = world(rng, layout), world(rng, parted)
        masks = [draw(rng, 0, 2, (1, layout.nb.shape[1])) for _ in range(ROUNDS)]
        end, outs = rounds(step.tick, layout, s, masks)
        moved, out = step.tick(parted, t, masks[0])
        if not (
            same(rewind(step.untick, layout, end, outs), s) and same(step.untick(parted, moved, out), t)
        ):
            return False
        if not any(o.k.any() for o in outs):
            return False  # no gear ticked: the run back was never asked
    return True


@pytest.fixture(scope="module")
def cube():
    """The 24's kinds and tables on the cube, and the plan of four trains, A1 and A2, T1 and T2, coupled through them."""
    ks, c = made(CUBE)
    held, found = load(
        {"trains": TRAINS, "couplings": COUPLINGS}, {"gears": []}, int(np.prod(CUBE)), ks, c
    )
    assert found == [] and held is not None
    return Plan(*held.plan)


def images(plan):
    """The sources turn with the board under the 24: the force and J of the turned state, the turned force and J."""
    nb = board(CUBE)
    n, rows = nb.shape[1], 1 + 1 + 3 + 3  # A1 and A2, T1 and T2, as stored
    ones = np.ones((1, n), dtype=object)
    layout = Layout(
        nb,
        meshes_of(nb),
        3 * ones.repeat(3, axis=1),
        Gearing(ones, ones, ones, 2, ones, ones),
        plan,
        ones,
        1,
    )
    s = world(np.random.default_rng(5), layout, rows)
    force, j = step.sources(layout, s)
    xyz, sides = np.indices(CUBE).reshape(3, -1), np.array(CUBE)[:, None]
    for m in turns():
        site, turn = np.ravel_multi_index(tuple((m @ xyz) % sides), CUBE), stored(m)[:rows, :rows]
        there = State(*(np.empty_like(x) for x in s))
        for x, y in zip(there, s, strict=True):
            x[:, site] = y
        there.a[:, site], there.b[:, site] = turn @ s.a, turn @ s.b
        moved, jm = step.sources(layout, there)
        if not (same([moved[:, site]], [turn @ force]) and same([jm[:, site]], [turn @ j])):
            return False
    return bool(j.any())


def mutants():
    """Broken copies of the act, each with the law that must catch it: what it replaces in the step, and with what."""
    driven, drive, undrive, sources, gear, ungear, seen = (
        step.driven,
        step.drive,
        step.undrive,
        step.sources,
        step.gear,
        step.ungear,
        mesh.seen,
    )
    return {
        "the kick's teeth ignored": (
            "formula",
            "driven",
            lambda g, f, q: driven(g._replace(kick=1), f, q),
        ),
        "the stretch off the kick": ("formula", "driven", lambda g, f, q: g.stretch * f + g.kick * q),
        "the drive without its fine tooth": (
            "formula",
            "drive",
            lambda j, teeth, rd: drive(j, teeth, 0 * rd),
        ),
        "the drive's tooth not carried": (
            "formula",
            "drive",
            lambda j, teeth, rd: (drive(j, teeth, rd)[0], rd),
        ),
        "the spring's sign turned": (
            "formula",
            "sources",
            lambda layout, s: sources(
                layout._replace(gearing=layout.gearing._replace(spring=-layout.gearing.spring)), s
            ),
        ),
        "the gradient's ends swapped": (
            "formula",
            "seen",
            lambda s, nb: seen(s, nb[[1, 0, 3, 2, 5, 4]]),
        ),
        "J read without the force": (
            "formula",
            "contract",
            lambda plan, readings, gears: contract.contract(
                plan, np.concatenate((readings[: -len(gears)], 0 * readings[-len(gears) :])), gears
            ),
        ),
        "the carry at W, not W+": (
            "formula",
            "gear",
            lambda a, b, r, go, w, wp, push: gear(a, b, r, go, w, w, push),
        ),
        "the kick's teeth read from the drive's": (
            "formula",
            "driven",
            lambda g, f, q: driven(g._replace(kick=g.drive), f, q),
        ),
        "the run back with W and W+ swapped": (
            "back",
            "ungear",
            lambda a, b, r, go, w, wp, push: ungear(a, b, r, go, wp, w, push),
        ),
        "the drive run back with its sign turned": (
            "back",
            "undrive",
            lambda j, teeth, rd: (lambda q, kept: (-q, kept))(*undrive(j, teeth, rd)),
        ),
        "the drive's tooth not run back": (
            "back",
            "undrive",
            lambda j, teeth, rd: (undrive(j, teeth, rd)[0], rd),
        ),
        "the gradient one-sided": (
            "images",
            "seen",
            lambda s, nb: seen(s, np.stack([nb[0], 0 * nb[0] + np.arange(nb.shape[1]), *nb[2:]])),
        ),
        "the gradient's axes in another order": (
            "images",
            "seen",
            lambda s, nb: seen(s, nb[[2, 3, 4, 5, 0, 1]]),
        ),
        "the sources at a far site": (
            "images",
            "sources",
            lambda layout, s: tuple(x[:, layout.nb[0][layout.nb[0]]] for x in sources(layout, s)),
        ),
        "every neighbour site 0": ("formula", "seen", lambda s, nb: seen(s, 0 * nb)),
    }


def law(name, plan):
    return {"formula": formula, "back": back, "images": lambda: images(plan)}[name]()


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_law_of_the_act_holds_and_fails_on_its_mutant(mutant, cube, monkeypatch):
    name, attribute, broken = mutants()[mutant]
    assert law(name, cube)
    monkeypatch.setattr(step, attribute, broken)
    assert not law(name, cube)


def test_the_force_s_path_is_the_stage_4_tick_with_j_added():
    """At T_k = T_d = 1 the kick is s J and every drive's tooth stays 0: the push is s (F + J)."""
    rng = np.random.default_rng(30)
    layout = varied(rng)
    layout = layout._replace(gearing=layout.gearing._replace(kick=1, drive=1))
    s = world(rng, layout)
    s = s._replace(rd=0 * s.rd)
    now, out = step.tick(layout, s, 1)
    force, j = step.sources(layout, s)
    a, _, r = step.gear(
        s.a, s.b, s.r, s.go, layout.gearing.w, layout.gearing.wp, layout.gearing.stretch * (force + j)
    )
    assert out.k.any() and not now.rd.any()
    assert same([np.where(out.k == 1, a, s.a), np.where(out.k == 1, r, s.r)], [now.a, now.r])
