"""Tensor24's engine: the Mesh, the board and the one act at its coefficients, every Node-clock in every round, and
its run back as the act on the mirrored state, each law failing on its mutant."""

import functools
import itertools
import math
from fractions import Fraction

import numpy as np
import pytest

from tensor24.algebra.carry import flip
from tensor24.engine import contract, mesh, step
from tensor24.engine.state import Gearing, Layout, Plan, Read, State
from tensor24.main import made
from tensor24.runner import board as boards
from tensor24.runner import load as loading
from tensor24.runner.load import load
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests import frame

SHAPE, ROUNDS, SQUARING = (
    (3, 4, 5),
    12,
    4,
)  # the board, the rounds of a run back, and of one where J squares the gears
# the gears per site, J's terms, and the readings: the value, the three differences and the force
ROWS, TERMS, PLANES = 4, 30, 1 + 3 + 1
CUBE, FRAME = (3, 3, 3), (5, 5, 5)  # the board the 24 turn, and the frame's properties' board
SIDE, REACH = 7, 60  # the cone's side and its rounds
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


def varied(rng, least=1, sourced=True, rows=ROWS, shape=SHAPE, clocked=False):
    """A layout parted at every gear and site: grips per row and Mesh, the teeth at rest, s, T_k, T_d, and J or none
    of it, every gear reading its teeth from two drawn rows' counts at drawn factors where clocked; every divisor at least
    `least`, and T_k too where `least` is above 1, so that a swap of T_k and T_d shows as a wrong run back, not a raise."""
    nb = frame.board(shape)
    n = nb.shape[1]
    w = draw(rng, least, 20, (rows, n))
    coefficients = (
        draw(rng, -3, 4, (rows, n)),
        draw(rng, -5, 6, (rows, 1)) if least == 1 else draw(rng, least, 9, (rows, 1)),
    )
    gearing = Gearing(w, *coefficients, draw(rng, least, 9, (rows, 1)))
    every = np.arange(rows, dtype=np.intp)
    two = np.repeat(rng.permutation(rows)[: 1 + 1], rows) if clocked else every  # every gear reads both
    read = Read(two, draw(rng, 1, 4, len(two)), np.tile(every, 1 + 1)) if clocked else frame.unread()
    index = [
        rng.integers(0, high, size=TERMS).astype(np.intp) for high in (PLANES * rows,) * 2 + (rows,)
    ]
    plan = Plan(index[0], index[1], draw(rng, -9, 10, TERMS), index[2])
    none = np.zeros(0, dtype=np.intp)
    plan = plan if sourced else Plan(none, none, none.astype(object), none)
    grip = draw(rng, -3, 4, (rows, 3 * n))
    return Layout(nb, frame.spokes(), frame.meshes_of(nb), grip, gearing, plan, read)


def world(rng, layout, rows=ROWS):
    """A state the act may meet: gears across 2**256, the clocks' rows in [0, 2**20), each tooth within its W and T_d."""
    size, drive = (rows, layout.nb.shape[1]), layout.gearing.drive
    a, b = frame.wide(rng, size), frame.wide(rng, size)
    clocks = np.unique(layout.clock.first)
    for x in (a, b):
        x[clocks] = draw(rng, 0, 1 << 20, (len(clocks), size[1]))
    w = step.weight(layout.gearing, layout.clock, a)
    return State(a, b, draw(rng, 0, 1 << 20, size) % w, draw(rng, 0, 1 << 20, size) % drive)


def naive(layout, s, shape=SHAPE):
    """The act site by site with loops and plain integers: the readings, J term by term, the drive, the push, the carry."""
    _, _, _, grip, gearing, plan, _ = layout
    rows = len(s.a)
    rest, stretch, kick, drive = (np.broadcast_to(x, s.a.shape).tolist() for x in gearing)
    first, second, factor, target = (x.tolist() for x in plan)
    a, b, r, rd = (x.tolist() for x in s)
    w = [row[:] for row in rest]  # every gear's teeth: its rest and the clocks' read, term by term
    for f, m, g in zip(*(x.tolist() for x in layout.clock), strict=True):
        w[g] = [x + m * y for x, y in zip(w[g], a[f], strict=True)]
    grip = np.broadcast_to(grip, (rows, grip.shape[1])).tolist()
    n = len(a[0])
    new = [[row[:] for row in x] for x in (a, b, r, rd)]
    for x in itertools.product(*map(range, shape)):
        i = np.ravel_multi_index(x, shape)
        around = [np.ravel_multi_index(y, shape) for y in frame.near(x, shape)]
        spokes = [axis * n + j for axis in range(3) for j in (i, around[axis + axis + 1])]
        seen = [[a[g][j] for j in around] for g in range(rows)]
        force = [
            sum(grip[g][m] * (v - a[g][i]) for m, v in zip(spokes, seen[g], strict=True))
            for g in range(rows)
        ]
        readings = [a[g][i] for g in range(rows)]
        readings += [
            seen[g][axis + axis] - seen[g][axis + axis + 1] for axis in range(3) for g in range(rows)
        ]
        source = [0] * rows
        for t in range(len(factor)):
            source[target[t]] += factor[t] * (readings + force)[first[t]] * (readings + force)[second[t]]
        for g in range(rows):
            q, new[3][g][i] = divmod(source[g] + rd[g][i], drive[g][i])
            push = stretch[g][i] * (force[g] + kick[g][i] * q)
            v, new[2][g][i] = divmod(w[g][i] * (a[g][i] - b[g][i]) + r[g][i] + push, w[g][i])
            new[0][g][i], new[1][g][i] = a[g][i] + v, a[g][i]
    return State(*(np.array(x, dtype=object) for x in new))


def formula():
    """At varied layouts, every gear clocked by two rows' counts, the act equals the naive model at every entry, three
    seeds."""
    for seed in range(3):
        rng = np.random.default_rng(seed)
        layout = varied(rng, clocked=True)
        s = world(rng, layout)
        if not frame.same(step.tick(layout, s), naive(layout, s)):
            return False
    return True


def back():
    """Rounds run back to the start bit for bit by the act on the mirrored state, the teeth at rest; one round clocked
    by two rows' counts, alike; every divisor row away from 1, so a swap of T_k and T_d or a read off its slot shows."""
    for seed in range(3):
        rng = np.random.default_rng(10 + seed)
        layout, parted = varied(rng, least=1 + 1), varied(rng, least=1 + 1, clocked=True)
        s, t = world(rng, layout), world(rng, parted)
        *_, end = rounds(step.tick, layout, s, SQUARING)
        moved = step.tick(parted, t)
        exact = frame.same(rewind(step.untick, layout, end, SQUARING), s)
        if not (exact and frame.same(step.untick(parted, moved), t) and not frame.same(end, s)):
            return False  # inexact, or the rounds moved nothing and the run back was never asked
    return True


def negated():
    """The tie rule on the act with no term of J: every gear negated, its tooth flipped in its teeth, ticks to the
    negation, its tooth flipped; the drive's tooth alike."""
    for seed in range(3):
        rng = np.random.default_rng(20 + seed)
        layout = varied(rng, sourced=False)
        s = world(rng, layout)
        w = layout.gearing.rest
        a1, b1, r1, rd1 = step.tick(layout, s)
        a2, b2, r2, rd2 = step.tick(layout, s._replace(a=-s.a, b=-s.b, r=flip(s.r, w)))
        if not frame.same([a2, b2, r2, rd2], [-a1, -b1, flip(r1, w), rd1]):
            return False
    return True


def lit(seed):
    """A board of side SIDE with no term of J and grips above 0; each site's Mesh distance from site 0, and a change at
    site 0."""
    rng = np.random.default_rng(seed)
    layout = varied(rng, sourced=False, rows=1, shape=(SIDE,) * 3)
    layout = layout._replace(grip=abs(layout.grip) + 1)
    s, xyz = world(rng, layout, 1), np.indices((SIDE,) * 3).reshape(3, -1)
    far = np.minimum(xyz, SIDE - xyz).sum(axis=0)
    change = (np.arange(SIDE**3) == 0).astype(object) * (1 << 40)
    return layout, s, far, change


def early(first, far):
    """Some site reached below its distance, or none reached at all."""
    return ((first < far) & (far > 0)).any() or (first == REACH).all()


def cone():
    """A change at one site reaches a site at Mesh distance d in no fewer than d rounds (David's p3)."""
    for seed in range(3):
        layout, u, far, change = lit(seed)
        v, first = u._replace(a=u.a + change, b=u.b + change), far * 0 + REACH
        for count in range(1, REACH + 1):
            u, v = step.tick(layout, u), step.tick(layout, v)
            first[(u.a[0] != v.a[0]) & (first == REACH)] = count
        if early(first, far):
            return False
    return True


def cone_back():
    """Run back, a change reaches distance d in no fewer than d rounds."""
    for seed in range(3):
        layout, u, far, change = lit(seed)
        *_, u = rounds(step.tick, layout, u, SIDE + SIDE)
        v, first = u._replace(a=u.a + change, b=u.b + change), far * 0 + REACH
        for count in range(1, SIDE + SIDE + 1):
            u, v = step.untick(layout, u), step.untick(layout, v)
            moved = (u.a[0] != v.a[0]) | (u.b[0] != v.b[0]) | (u.r[0] != v.r[0])
            first[moved & (first == REACH)] = count
        if early(first, far):
            return False
    return True


SHAPES = ((3, 3, 3), (4, 5, 6), (3, 4, 7), (1, 1, 1), (7, 7, 7))


def model():
    """The board's neighbours, and the load's Spokes and Meshes on them, equal the frame's (numpy's own wrap) at every
    shape."""
    built = [
        (boards.board(shape), *loading.geometry(boards.board(shape), len(shape))) for shape in SHAPES
    ]
    wanted = [(frame.board(s), frame.spokes(), frame.meshes_of(frame.board(s))) for s in SHAPES]
    return all(
        np.array_equal(x, y)
        for pair in zip(built, wanted, strict=True)
        for x, y in zip(*pair, strict=True)
    )


def held_alike():
    """Each Mesh is held alike at its two ends: a site's +axis Spoke and its +axis neighbour's -axis Spoke."""
    for shape in SHAPES:
        nb = boards.board(shape)
        _, meshes = loading.geometry(nb, len(shape))
        if not all(np.array_equal(meshes[x + x], meshes[x + x + 1][nb[x + x]]) for x in range(3)):
            return False
    return True


@functools.cache
def cube():
    """The 24's kinds and tables on the cube, and the plan of four trains, A1 and A2, T1 and T2, coupled through them."""
    ks, c = made(CUBE)
    held, found = load(
        {"trains": TRAINS, "couplings": COUPLINGS}, {"gears": []}, int(np.prod(CUBE)), ks, c
    )
    assert found == [] and held is not None
    return Plan(*held.plan)


def sourced_images():
    """The sources turn with the board under the 24: the force and J of the turned state, the turned force and J."""
    nb, plan = frame.board(CUBE), cube()
    # A1 and A2, T1 and T2, as stored, and the clock's own gear the load lays, A1
    n, rows = nb.shape[1], 1 + 1 + 3 + 3 + 1
    ones = np.ones((1, n), dtype=object)
    gearing = Gearing(ones, ones, ones, ones)
    grip = 3 * ones.repeat(3, axis=1)
    layout = Layout(nb, frame.spokes(), frame.meshes_of(nb), grip, gearing, plan, frame.unread())
    s = world(np.random.default_rng(5), layout, rows)
    force, j = step.sources(layout, s.a)
    xyz, sides = np.indices(CUBE).reshape(3, -1), np.array(CUBE)[:, None]
    for m in frame.turns():
        site = np.ravel_multi_index(tuple((m @ xyz) % sides), CUBE)
        turn = np.eye(rows, dtype=int).astype(object)
        turn[:-1, :-1] = frame.stored(m)[: rows - 1, : rows - 1]  # the clock is A1: no turn moves it
        there = State(*(np.empty_like(x) for x in s))
        for x, y in zip(there, s, strict=True):
            x[:, site] = y
        there.a[:, site], there.b[:, site] = turn @ s.a, turn @ s.b
        moved, jm = step.sources(layout, there.a)
        if not (frame.same([moved[:, site]], [turn @ force]) and frame.same([jm[:, site]], [turn @ j])):
            return False
    return bool(j.any())


def alike(nb):
    """A layout alike at every site, Mesh and gear, for the frame's properties: s, D and T_k, the force's path, no J."""
    ones = np.ones((1, nb.shape[1]), dtype=object)
    layout = frame.plain(nb, frame.meshes_of(nb), ones.repeat(3, axis=1), 7 * ones)
    return layout._replace(gearing=Gearing(7 * ones, 1 + 1, 3, 1))


def engine():
    """The act in every round at a layout alike everywhere, with no out: its run back, its worlds and its naive model."""
    return frame.Engine(
        lambda nb, s: (step.tick(alike(nb), State(*s)), ()),
        lambda nb, s, out: step.untick(alike(nb), State(*s)),
        lambda rng, shape, rows: world(rng, alike(frame.board(shape)), rows),
        lambda shape, s: (naive(alike(frame.board(shape)), State(*s), shape), ()),
    )


def mutants():
    """Broken copies, each with the law that must catch it: what it replaces in the step (or the board), and with what."""
    tick, untick, gear, mirror = step.tick, step.untick, step.gear, step.mirror
    read, weight, driven, drive, sources = step.read, step.weight, step.driven, step.drive, step.sources
    pull, seen, built, laid, calls = (
        mesh.pull,
        mesh.seen,
        boards.board,
        loading.geometry,
        itertools.count(),
    )

    def far(y):
        return y._replace(nb=y.nb[:, y.nb[0]])

    def doubled(*x):
        a, b, r = gear(*x)
        return a + a, b, r

    def floated(a, b, r, w, push):
        n = w * (a - b) + r + push
        q = np.vectorize(lambda x, y: math.floor(x / y), otypes=[object])(n, w + 0 * n)
        return a + q, a, n - q * w

    def unfactored(c, x):
        return read(c._replace(factor=c.first), x)

    def placed(c, x):  # every clock found at the last row, by its place
        return read(c._replace(first=0 * c.first + len(x) - 1), x)

    def mirrored_now(
        y, s
    ):  # the mirror's teeth read at its now slot, not the before slot it was kept at
        a, b, r, rd = s
        return State(b, a, flip(r, weight(y.gearing, y.clock, a)), flip(rd, y.gearing.drive))

    def keep_b(y, s):
        return untick(y, s)._replace(b=s.b)

    def counted(y, s):
        moved = tick(y, s)
        return moved._replace(a=moved.a + next(calls))

    def far_teeth(y, s):
        g = y.gearing
        return tick(y._replace(gearing=g._replace(rest=g.rest[:, y.nb[0]])), s)

    def regrip(f):
        return lambda y, a: pull(y._replace(grip=f(y.grip)), a)

    def kicked(teeth):
        return lambda g, f, q: driven(g._replace(kick=teeth(g)), f, q)

    def reread(order):
        return lambda a, nb: seen(a, nb[order])

    def forceless(plan, readings, gears):
        cut = len(readings) - len(gears)
        return contract.contract(plan, np.concatenate((readings[:cut], 0 * readings[cut:])), gears)

    def swapped(y, s):
        g = y.gearing
        return untick(y._replace(gearing=g._replace(kick=g.drive, drive=g.kick)), s)

    def one_sided(a, nb):
        return seen(a, np.stack([nb[0], 0 * nb[0] + np.arange(nb.shape[1]), *nb[2:]]))

    def far_sources(y, a):
        return tuple(x[:, y.nb[0][y.nb[0]]] for x in sources(y, a))

    def one_short(shape):
        nb = built(shape)
        return np.stack([nb[0], nb[0], *nb[2:]])

    def wrapped_once(nb, axes):
        spokes, meshes = laid(nb, axes)
        return spokes, np.stack([meshes[0], meshes[0], *meshes[2:]])

    first = lambda a: (np.arange(len(a)) == 0).astype(object)[:, None]  # noqa: E731
    return {  # the Mesh, the board, and the act at its coefficients
        "the run back with no mirror": ("back", "untick", lambda y, s: tick(y, s)),
        "the mirror's teeth read at its now slot": ("back", "mirror", mirrored_now),
        "the drive's tooth not mirrored": (
            "back",
            "mirror",
            lambda y, s: mirror(y, s)._replace(rd=s.rd),
        ),
        "the now slot doubled": ("formula", "gear", doubled),
        "the quotient through a float": ("formula", "gear", floated),
        "the before slot kept by the run back": ("back", "untick", keep_b),
        "the grip ignored": ("formula", "pull", regrip(lambda grip: 0 * grip + 1)),
        "the grip squared": ("formula", "pull", regrip(lambda grip: grip * grip)),
        "a far site's teeth": ("formula", "tick", far_teeth),
        "a pull that is not odd": ("negated", "pull", lambda y, a: pull(y, a) + 1),
        "a pull two Meshes away": ("locality", "pull", lambda y, a: pull(far(y), a)),
        "a counter": ("purity", "tick", counted),
        "train 0 singled out": ("rename", "gear", lambda a, *z: gear(a + first(a), *z)),
        "the +x Spoke twice": ("images", "pull", lambda y, a: pull(y, a) + seen(a, y.nb)[:, 0] - a),
        "the before slot off the stride": ("formula", "gear", lambda a, b, *z: gear(a, 0 * b, *z)),
        "the run back keeping the before slot": ("bijectivity", "untick", keep_b),
        "the -x neighbour taken as the +x": ("model", "board", one_short, boards),
        "the -x Spoke holding the site's own Mesh": ("held_alike", "geometry", wrapped_once, loading),
        "the pull two Meshes away, past the cone": ("cone", "pull", lambda y, a: pull(far(y), a)),
        "the run back two Meshes away": ("cone_back", "untick", lambda y, s: untick(far(y), s)),
        "the kick's teeth ignored": ("formula", "driven", kicked(lambda g: 1)),
        "the stretch off the kick": ("formula", "driven", lambda g, f, q: g.stretch * f + g.kick * q),
        "the drive without its fine tooth": ("formula", "drive", lambda j, d, rd: drive(j, d, 0 * rd)),
        "the drive's tooth not carried": ("formula", "drive", lambda *x: (drive(*x)[0], x[2])),
        "the gradient's ends swapped": ("formula", "seen", reread([1, 0, 3, 2, 5, 4])),
        "J read without the force": ("formula", "contract", forceless),
        "the clocks' read off its factor": ("formula", "read", unfactored),
        "the clocks found by their place": ("formula", "read", placed),
        "the teeth without their rest": ("formula", "weight", lambda g, c, a: read(c, a)),
        "T_k read from T_d": ("formula", "driven", kicked(lambda g: g.drive)),
        "the run back with T_k and T_d swapped": ("back", "untick", swapped),
        "the gradient one-sided": ("sourced_images", "seen", one_sided),
        "the gradient's axes reordered": ("sourced_images", "seen", reread([2, 3, 4, 5, 0, 1])),
        "the sources at a far site": ("sourced_images", "sources", far_sources),
        "every neighbour site 0": ("formula", "seen", lambda a, nb: seen(a, 0 * nb)),
    }


OWN = {f.__name__: f for f in (formula, back, negated, cone, cone_back, model, held_alike)}
OWN["sourced_images"] = sourced_images


def law(name):
    """The engine's own laws, and the frame's properties on the act at three seeds."""
    return (
        OWN[name]() if name in OWN else all(frame.holds(name, engine, FRAME, seed) for seed in range(3))
    )


# each law on the engine as it stands, read once for the mutants aimed at it
lawful = functools.cache(law)


@pytest.mark.parametrize("mutant", list(mutants()))
def test_each_law_of_the_engine_holds_and_fails_on_its_mutant(mutant, monkeypatch):
    name, attribute, broken, *module = mutants()[mutant]
    assert name in [*OWN, *frame.PROPERTIES] and lawful(name)
    monkeypatch.setattr(*module or [step], attribute, broken)
    assert not law(name)


def test_the_force_s_path_is_the_stage_4_tick_with_j_added():
    """At T_k = T_d = 1 the kick is s J and every drive's tooth stays 0: the push is s (F + J)."""
    rng = np.random.default_rng(30)
    layout = varied(rng)
    layout = layout._replace(gearing=layout.gearing._replace(kick=1, drive=1))
    s = world(rng, layout)
    s = s._replace(rd=0 * s.rd)
    now = step.tick(layout, s)
    force, j = step.sources(layout, s.a)
    w = step.weight(layout.gearing, layout.clock, s.a)
    a, _, r = step.gear(s.a, s.b, s.r, w, layout.gearing.stretch * (force + j))
    assert not now.rd.any() and frame.same([a, r], [now.a, now.r])


def im(x, y):
    """Im(conj(x) y) for two hands, each the pair of rows (re, im): x_re y_im - x_im y_re."""
    return x[0] * y[1] - x[1] * y[0]


def home(w):
    """The fine tooth's middle, W div 2, about which a tooth is read signed."""
    return w // (1 + 1)


def charged(s, w, weight):
    """The hand's charge Q* = SUM Im(conj(a + b) P) / (2 s), P = W (a - b) + (r - home): David's density, exact."""
    a, b, r, _ = s
    density = im(a + b, w * (a - b) + (r - home(w)))
    return sum(
        Fraction(int(d), int(2 * v)) for d, v in zip(density.ravel(), weight.ravel(), strict=True)
    )


def kept(each_end=False, moving=False, sourced=False):
    """Over synchronous rounds a hand's charge Q* moves by Rule3's torques and its kick alone (David's OPEN 13): its rows
    alike in W, W+, s, D, T_k and T_d, grips one per Mesh, the teeth changing; the kick's term 0 with J off, and with J on
    read from the drive's carry, T_d q = J + r_d - r_d+, J not 0. A grip per end, or an s that moves, parts it."""
    rng = np.random.default_rng(50)
    nb = frame.board(SHAPE)
    n = nb.shape[1]
    meshes = np.arange(6 * n).reshape(6, n) if each_end else frame.meshes_of(nb)
    grip, s = draw(rng, -3, 4, (1, (6 if each_end else 3) * n)), draw(rng, 1, 5, (1, n))
    teeth = [draw(rng, 2, 20, (1, n)) for _ in range(ROUNDS + 1)]
    kick, drive = (draw(rng, 2, 6, (1, n)), draw(rng, 2, 9, (1, n))) if sourced else (1, 1)
    terms = (TERMS if sourced else 0,) * 2
    index = [
        rng.integers(0, high, size=terms[0]).astype(np.intp) for high in (PLANES * 2, PLANES * 2, 2)
    ]
    plan = Plan(index[0], index[1], draw(rng, -9, 10, terms[1]), index[2])
    state = State(
        *(draw(rng, -(1 << 10), 1 << 10, (2, n)) if sourced else frame.wide(rng, (2, n)) for _ in "ab"),
        draw(rng, 0, 1 << 20, (2, n)) % teeth[0],
        draw(rng, 0, 1 << 20, (2, n)) % drive,
    )
    for t in range(SQUARING if sourced else ROUNDS):  # J squares the gears each round
        push = s + t * draw(rng, 0, 3, (1, n)) if moving else s
        gearing = Gearing(teeth[t], push, kick, drive)  # each round at its own teeth
        layout = Layout(nb, frame.spokes(), meshes, grip, gearing, plan, frame.unread())
        _, j = step.sources(layout, state.a)
        now = step.tick(layout, state)
        torques = im(state.a - state.b, state.r - home(teeth[t]))
        torques = torques + im(now.a - state.a, now.r - home(teeth[t]))
        moved = charged(now, teeth[t], s) - charged(state, teeth[t], s)
        kicked = np.broadcast_to(kick * im(state.a, j + state.rd - now.rd), (1, n))
        ds = np.broadcast_to(drive, (1, n)).ravel()
        terms = zip(torques.ravel(), s.ravel(), kicked.ravel(), ds, strict=True)
        expected = sum(Fraction(int(x), int(2 * v)) + Fraction(int(y), int(d)) for x, v, y, d in terms)
        if (sourced and not np.any(j)) or moved != expected:
            return False
        state = now
    return True


def test_a_hands_charge_moves_by_rules_torques_and_its_kick_alone_and_parts_on_a_grip_per_end_or_a_moving_s(
    monkeypatch,
):
    assert kept() and kept(sourced=True) and not kept(each_end=True) and not kept(moving=True)
    driven = step.driven
    monkeypatch.setattr(step, "driven", lambda g, f, q: driven(g._replace(stretch=1), f, q))
    assert not kept()  # the push off its stretch
    monkeypatch.setattr(step, "driven", lambda g, f, q: driven(g._replace(kick=1), f, q))
    assert kept() and not kept(sourced=True)  # the kick off its teeth, which J off cannot see


def test_the_engines_records_hold_their_fields_in_order():
    assert State._fields == ("a", "b", "r", "rd")
    assert Gearing._fields == ("rest", "stretch", "kick", "drive")
    assert Layout._fields == ("nb", "spokes", "meshes", "grip", "gearing", "plan", "clock")
    assert Read._fields == ("first", "factor", "target")
    assert Plan._fields == ("first", "second", "factor", "target")


def test_a_world_is_answered_alike_in_fresh_interpreters_at_other_hash_seeds():
    assert frame.unseeded(__name__, "engine", FRAME)


def test_a_world_is_run_back_in_a_fresh_interpreter_that_never_stepped():
    assert frame.undone_elsewhere(__name__, "engine", FRAME, 0)
