"""Tensor24's engine: one clock, the Mesh, the board and the one act at its coefficients, each law failing on its mutant."""

import functools
import itertools
import math
from fractions import Fraction

import numpy as np
import pytest

from tensor24.algebra.carry import home
from tensor24.engine import contract, mesh, step
from tensor24.engine.state import Gearing, Layout, Out, Plan, Read, State
from tensor24.main import made
from tensor24.runner import board as boards
from tensor24.runner.load import load
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests import frame

SHAPE, GAMMA, ROUNDS = (3, 4, 5), 9, 12  # the board, the full rate, the rounds of the run back
# the gears per site, J's terms, and the readings: the value, the three differences and the force
ROWS, TERMS, PLANES = 4, 30, 1 + 3 + 1
CUBE, FRAME = (3, 3, 3), (5, 5, 5)  # the board the 24 turn, and the frame's properties' board
SIDE, T, REACH = 7, 10, 60  # the cone's side, the count the order runs to, and the cone's rounds
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
    grip, rate = draw(rng, -3, 4, (rows, 3 * n)), draw(rng, 0, GAMMA + 1, (1, n))
    return Layout(nb, frame.meshes_of(nb), grip, gearing, plan, rate, GAMMA, read)


def world(rng, layout, rows=ROWS):
    """A state the act may meet: gears across 2**256, the clocks' rows in [0, 2**20), each tooth within its W and T_d."""
    size, drive = (rows, layout.nb.shape[1]), layout.gearing.drive
    a, b = frame.wide(rng, size), frame.wide(rng, size)
    clocks = np.unique(layout.clock.first)
    for x in (a, b):
        x[clocks] = draw(rng, 0, 1 << 20, (len(clocks), size[1]))
    w, one = step.weight(layout.gearing, layout.clock, a), (1, size[1])
    c = draw(rng, 0, 2, one)
    teeth = (draw(rng, 0, 1 << 20, size) % w, draw(rng, 0, 2, size), draw(rng, 0, 1 << 20, size) % drive)
    return State(a, b, *teeth, draw(rng, 0, GAMMA, one), c, c - draw(rng, 0, 2, one))


def naive(layout, s, mask, shape=SHAPE):
    """The act site by site with loops and plain integers: the readings, J term by term, the drive, the push, the carry."""
    _, _, grip, gearing, plan, rate, gamma, _ = layout
    rows = len(s.a)
    rest, stretch, kick, drive = (np.broadcast_to(x, s.a.shape).tolist() for x in gearing)
    first, second, factor, target = (x.tolist() for x in plan)
    a, b, r, go, rd = (x.tolist() for x in s[:5])
    w = [row[:] for row in rest]  # every gear's teeth: its rest and the clocks' read, term by term
    for f, m, g in zip(*(x.tolist() for x in layout.clock), strict=True):
        w[g] = [x + m * y for x, y in zip(w[g], a[f], strict=True)]
    ph, c, tn, rate = (x.tolist()[0] for x in (*s[5:], rate))
    mask = np.broadcast_to(mask, (1, len(c))).tolist()[0]
    grip = np.broadcast_to(grip, (rows, grip.shape[1])).tolist()
    n = len(c)
    new = [[row[:] for row in x] for x in (a, b, r, go, rd, [ph], [c], [tn])]
    fire, k = [0] * n, [0] * n
    for x in itertools.product(*map(range, shape)):
        i = np.ravel_multi_index(x, shape)
        around = [np.ravel_multi_index(y, shape) for y in frame.near(x, shape)]
        spokes = [axis * n + j for axis in range(3) for j in (i, around[axis + axis + 1])]
        fire[i] = mask[i] * int(all(c[j] >= c[i] for j in around))
        k[i], new[5][0][i] = divmod(ph[i] + rate[i], gamma) if fire[i] else (0, ph[i])
        new[6][0][i] = c[i] + fire[i]
        seen = [[a[g][j] if c[i] >= tn[j] else b[g][j] for j in around] for g in range(rows)]
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
        for g in range(rows if k[i] else 0):
            q, new[4][g][i] = divmod(source[g] + rd[g][i], drive[g][i])
            p = w[g][i] * (a[g][i] - b[g][i]) + r[g][i] - (w[g][i] - go[g][i]) // 2
            push = stretch[g][i] * (force[g] + kick[g][i] * q)
            v, new[2][g][i] = divmod(p + push + (w[g][i] - go[g][i]) // 2, w[g][i])
            new[0][g][i], new[1][g][i] = a[g][i] + v, a[g][i]
        new[7][0][i] = new[6][0][i] if k[i] else tn[i]
    return State(*(np.array(x, dtype=object) for x in new)), tuple(
        np.array([x], dtype=object) for x in (fire, k, tn)
    )


def formula():
    """At varied layouts, every gear clocked by a row's count, the act under a random mask equals the naive model at every
    entry, three seeds."""
    for seed in range(3):
        rng = np.random.default_rng(seed)
        layout = varied(rng, clocked=True)
        s, mask = world(rng, layout), draw(rng, 0, 2, (1, layout.nb.shape[1]))
        if not frame.same(frame.flat(step.tick(layout, s, mask)), frame.flat(naive(layout, s, mask))):
            return False
    return True


def back():
    """Rounds under random masks run back to the start bit for bit, the teeth at rest; one round clocked by a row's count,
    alike; every divisor row away from 1, so a swap of T_k and T_d or a read off its slot shows (Sofer's read-for)."""
    for seed in range(3):
        rng = np.random.default_rng(10 + seed)
        layout, parted = varied(rng, least=1 + 1), varied(rng, least=1 + 1, clocked=True)
        s, t = world(rng, layout), world(rng, parted)
        masks = [draw(rng, 0, 2, (1, layout.nb.shape[1])) for _ in range(ROUNDS)]
        end, outs = rounds(step.tick, layout, s, masks)
        moved, out = step.tick(parted, t, 1)
        exact = frame.same(rewind(step.untick, layout, end, outs), s)
        exact = exact and frame.same(step.untick(parted, moved, out), t)
        if not (exact and any(o.k.any() for o in outs) and out.k.any()):
            return False  # inexact, or no gear ticked and the run back was never asked
    return True


def schedule(seed):
    """A layout with no term of J, rates parted and the clock at site 5 stopped, its first state at count 0, and an rng."""
    rng = np.random.default_rng(seed)
    layout = varied(rng, sourced=False, rows=2)
    layout.rate[0, 5] = 0
    s = world(rng, layout, 2)
    return layout, s._replace(c=0 * s.c, tn=0 * s.tn), rng


def until(layout, s, rng=None, limit=60 * T):
    """Rounds to the count T, every due beat or random masks; with the rounds whose counts part and the stale reads."""
    outs, parting, stale = [], 0, 0
    for _ in range(limit):
        if not (s.c < T).any():
            break
        bits = np.ones_like(s.c) if rng is None else rng.integers(0, 2, size=s.c.shape).astype(object)
        allowed = bits * (s.c < T)
        fire = mesh.due(s.c, layout.nb) * allowed
        parting += int((s.c != s.c[0, 0]).any())
        stale += int(((s.c[:, None, :] < s.tn[:, layout.nb]) * fire[:, None, :]).sum())
        s, out = rounds(step.tick, layout, s, [allowed])
        outs += out
    return s, outs, parting, stale


def order():
    """At two layouts, forty random schedules give the synchronous pass's state at equal counts, parting, stale reads."""
    for seed in (1, 4):
        layout, s, rng = schedule(seed)
        reference = until(layout, s)[0]
        runs = (until(layout, s, rng) for _ in range(40))
        if not all(frame.same(end, reference) and parting and stale for end, _, parting, stale in runs):
            return False
    return True


def stopped():
    """A stopped clock's count keeps pace: every count reaches T, and the stopped clock's gears stand."""
    layout, s, _ = schedule(3)
    end, _, _, _ = until(layout, s)
    return (end.c == T).all() and (end.a[:, 5] == s.a[:, 5]).all()


def negated():
    """The tie rule on the act with no term of J: every gear negated, its tooth flipped and its going advanced, ticks to the
    negation, its tooth flipped; at W = W+ the homes cancel, and the going parts only where W, W+ part (algebra, light)."""
    for seed in range(3):
        rng = np.random.default_rng(20 + seed)
        layout = varied(rng, sourced=False)
        s, mask = world(rng, layout), draw(rng, 0, 2, (1, layout.nb.shape[1]))
        w = layout.gearing.rest
        (a1, b1, r1, go1, *rest1), out1 = step.tick(layout, s, mask)
        negative = s._replace(a=-s.a, b=-s.b, r=w - 1 - s.r, go=1 - s.go)
        (a2, b2, r2, go2, *rest2), out2 = step.tick(layout, negative, mask)
        flipped = frame.same([a2, b2, go2, r2], [-a1, -b1, 1 - go1, w - 1 - r1])
        if not (flipped and frame.same([*rest2, *out2], [*rest1, *out1])):
            return False
    return True


def lit(seed, full=False):
    """A board of side SIDE with no term of J and grips above 0, at count 0, its rates drawn or every clock at full;
    each site's Mesh distance from site 0, and a change at site 0."""
    rng = np.random.default_rng(seed)
    layout = varied(rng, sourced=False, rows=1, shape=(SIDE,) * 3)
    rate = GAMMA + 0 * layout.rate if full else layout.rate
    layout = layout._replace(grip=abs(layout.grip) + 1, rate=rate)
    s, xyz = world(rng, layout, 1), np.indices((SIDE,) * 3).reshape(3, -1)
    far = np.minimum(xyz, SIDE - xyz).sum(axis=0)
    change = (np.arange(SIDE**3) == 0).astype(object) * (1 << 40)
    return layout, s._replace(c=0 * s.c, tn=0 * s.tn), rng, far, change


def early(first, far):
    """Some site reached below its distance, or none reached at all."""
    return ((first < far) & (far > 0)).any() or (first == REACH).all()


def cone():
    """A change at one site reaches a site at Mesh distance d at no count below d, under random masks (David's p3)."""
    for seed in range(3):
        layout, u, rng, far, change = lit(seed)
        v, first = u._replace(a=u.a + change, b=u.b + change), far * 0 + REACH
        for _ in range(REACH):
            mask = draw(rng, 0, 2, (1, SIDE**3))
            (u, _), (v, _) = step.tick(layout, u, mask), step.tick(layout, v, mask)
            fresh = (u.a[0] != v.a[0]) & (first == REACH)
            first[fresh] = u.tn[0][fresh]
        if early(first, far):
            return False
    return True


def cone_back():
    """Run back at the full rate, every clock ticking each round, a change reaches distance d in no fewer than d rounds."""
    for seed in range(3):
        layout, u, _, far, change = lit(seed, full=True)
        outs = []
        for _ in range(SIDE + SIDE):
            u, out = step.tick(layout, u, 1)
            outs = [out, *outs]
        v, first = u._replace(a=u.a + change, b=u.b + change), far * 0 + REACH
        for count, out in enumerate(outs, start=1):
            u, v = step.untick(layout, u, out), step.untick(layout, v, out)
            moved = (u.a[0] != v.a[0]) | (u.b[0] != v.b[0]) | (u.r[0] != v.r[0])
            first[moved & (first == REACH)] = count
        if early(first, far):
            return False
    return True


SHAPES = ((3, 3, 3), (4, 5, 6), (3, 4, 7), (1, 1, 1), (7, 7, 7))


def model():
    """The board's neighbours and Meshes equal the frame's, found by numpy's own wrap, at every shape."""
    built = [boards.board(shape) for shape in SHAPES]
    wanted = [(frame.board(shape), frame.meshes_of(frame.board(shape))) for shape in SHAPES]
    return all(
        np.array_equal(x, y)
        for pair in zip(built, wanted, strict=True)
        for x, y in zip(*pair, strict=True)
    )


def held_alike():
    """Each Mesh is held alike at its two ends: a site's +axis Spoke and its +axis neighbour's -axis Spoke."""
    for shape in SHAPES:
        nb, meshes = boards.board(shape)
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
    layout = Layout(
        nb, frame.meshes_of(nb), 3 * ones.repeat(3, axis=1), gearing, plan, ones, 1, frame.unread()
    )
    s = world(np.random.default_rng(5), layout, rows)
    force, j = step.sources(layout, s)
    xyz, sides = np.indices(CUBE).reshape(3, -1), np.array(CUBE)[:, None]
    for m in frame.turns():
        site = np.ravel_multi_index(tuple((m @ xyz) % sides), CUBE)
        turn = np.eye(rows, dtype=int).astype(object)
        turn[:-1, :-1] = frame.stored(m)[: rows - 1, : rows - 1]  # the clock is A1: no turn moves it
        there = State(*(np.empty_like(x) for x in s))
        for x, y in zip(there, s, strict=True):
            x[:, site] = y
        there.a[:, site], there.b[:, site] = turn @ s.a, turn @ s.b
        moved, jm = step.sources(layout, there)
        if not (frame.same([moved[:, site]], [turn @ force]) and frame.same([jm[:, site]], [turn @ j])):
            return False
    return bool(j.any())


def alike(nb):
    """A layout alike at every site, Mesh and gear, for the frame's properties: s, D and T_k, the force's path, no J."""
    ones = np.ones((1, nb.shape[1]), dtype=object)
    layout = frame.plain(nb, frame.meshes_of(nb), ones.repeat(3, axis=1), 7 * ones, 5 * ones, GAMMA)
    return layout._replace(gearing=Gearing(7 * ones, 1 + 1, 3, 1))


def engine():
    """The act on every due beat at a layout alike everywhere: its run back, its worlds and its naive model."""
    return frame.Engine(
        lambda nb, s: step.tick(alike(nb), State(*s), 1),
        lambda nb, s, out: step.untick(alike(nb), State(*s), Out(*out)),
        lambda rng, shape, rows: world(rng, alike(frame.board(shape)), rows),
        lambda shape, s: naive(alike(frame.board(shape)), State(*s), 1, shape),
    )


def mutants():
    """Broken copies, each with the law that must catch it: what it replaces in the step (or the board), and with what."""
    tick, untick, gear, ungear = step.tick, step.untick, step.gear, step.ungear
    beat, read, weight = step.beat, step.read, step.weight
    driven, drive, undrive, sources = step.driven, step.drive, step.undrive, step.sources
    pull, seen, built, calls = mesh.pull, mesh.seen, boards.board, itertools.count()

    def now_only(y, s):
        return ((s.a[:, y.nb] - s.a[:, None, :]) * y.grip[:, y.meshes]).sum(axis=1)

    def far(y):
        return y._replace(nb=y.nb[:, y.nb[0]])

    def doubled(*x):
        a, b, r = gear(*x)
        return a + a, b, r

    def floated(a, b, r, go, w, wp, push):
        n = w * (a - b) + (r - home(w, go)) + push + home(wp, go)
        q = np.vectorize(lambda x, y: math.floor(x / y), otypes=[object])(n, wp + 0 * n)
        return a + q, a, n - q * wp

    def unfactored(c, x):
        return read(c._replace(factor=c.first), x)

    def placed(c, x):  # every clock found at the last row, by its place
        return read(c._replace(first=0 * c.first + len(x) - 1), x)

    def read_after(y, s, o):  # the run back's teeth read at its own now slot, the forward's after slot
        step.weight = lambda g, c, _: weight(g, c, s.a)
        try:
            return untick(y, s, o)
        finally:
            step.weight = weight

    def keep_b(y, s, o):
        return untick(y, s, o)._replace(b=s.b)

    def counting(y, s, m):
        return tick(y, s, m * beat(s.ph, y.rate, y.gamma, 1)[0])

    def far_rate(y, s, m):
        return tick(y._replace(rate=y.rate[:, y.nb[0]]), s, m)

    def far_teeth(y, s, m):
        g = y.gearing
        return tick(y._replace(gearing=g._replace(rest=g.rest[:, y.nb[0]])), s, m)

    def regrip(f):
        return lambda y, s: pull(y._replace(grip=f(y.grip)), s)

    def kicked(teeth):
        return lambda g, f, q: driven(g._replace(kick=teeth(g)), f, q)

    def reread(order):
        return lambda s, nb: seen(s, nb[order])

    def forceless(plan, readings, gears):
        cut = len(readings) - len(gears)
        return contract.contract(plan, np.concatenate((readings[:cut], 0 * readings[cut:])), gears)

    def swapped(y, s, o):
        g = y.gearing
        return untick(y._replace(gearing=g._replace(kick=g.drive, drive=g.kick)), s, o)

    def turned_back(*x):
        q, kept = undrive(*x)
        return -q, kept

    def one_sided(s, nb):
        return seen(s, np.stack([nb[0], 0 * nb[0] + np.arange(nb.shape[1]), *nb[2:]]))

    def far_sources(y, s):
        return tuple(x[:, y.nb[0][y.nb[0]]] for x in sources(y, s))

    def one_short(shape):
        nb, meshes = built(shape)
        return np.stack([nb[0], nb[0], *nb[2:]]), meshes

    def wrapped_once(shape):
        nb, meshes = built(shape)
        return nb, np.stack([meshes[0], meshes[0], *meshes[2:]])

    first = lambda a: (np.arange(len(a)) == 0).astype(object)[:, None]  # noqa: E731
    return {  # one clock, the Mesh, the board, and the act at its coefficients
        "the run back blind to the push": ("back", "ungear", lambda *x: ungear(*x[:-1], 0 * x[-1])),
        "a stopped beat that ticks": ("stopped", "beat", lambda ph, rate, gamma, fire: (fire, ph)),
        "the now slot doubled": ("formula", "gear", doubled),
        "the quotient through a float": ("formula", "gear", floated),
        "the read of the now slot alone": ("order", "pull", now_only),
        "the before slot kept by the run back": ("back", "untick", keep_b),
        "the beat that counts only its ticks": ("stopped", "tick", counting),
        "the mask ignored": ("formula", "tick", lambda y, s, m: tick(y, s, 1)),
        "the grip ignored": ("formula", "pull", regrip(lambda grip: 0 * grip + 1)),
        "the grip squared": ("formula", "pull", regrip(lambda grip: grip * grip)),
        "the +x neighbour's rate": ("formula", "tick", far_rate),
        "a far site's teeth": ("formula", "tick", far_teeth),
        "a pull that is not odd": ("negated", "pull", lambda y, s: pull(y, s) + 1),
        "a pull two Meshes away": ("locality", "pull", lambda y, s: pull(far(y), s)),
        "a counter": ("purity", "tick", lambda y, s, m: tick(y, s._replace(c=s.c + next(calls)), m)),
        "train 0 singled out": ("rename", "gear", lambda a, *z: gear(a + first(a), *z)),
        "the +x Spoke twice": ("images", "pull", lambda y, s: pull(y, s) + seen(s, y.nb)[:, 0] - s.a),
        "the before slot off the stride": ("formula", "gear", lambda a, b, *z: gear(a, 0 * b, *z)),
        "the run back keeping the before slot": ("bijectivity", "untick", keep_b),
        "the -x neighbour taken as the +x": ("model", "board", one_short, boards),
        "the -x Spoke holding the site's own Mesh": ("held_alike", "board", wrapped_once, boards),
        "the now slot read whatever its time": ("cone", "pull", now_only),
        "the run back two Meshes away": ("cone_back", "untick", lambda y, s, o: untick(far(y), s, o)),
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
        "the run back's teeth read at the after slot": ("back", "untick", read_after),
        "the drive run back, its sign turned": ("back", "undrive", turned_back),
        "the run back with T_k and T_d swapped": ("back", "untick", swapped),
        "the drive's tooth not run back": ("back", "undrive", lambda *x: (undrive(*x)[0], x[2])),
        "the gradient one-sided": ("sourced_images", "seen", one_sided),
        "the gradient's axes reordered": ("sourced_images", "seen", reread([2, 3, 4, 5, 0, 1])),
        "the sources at a far site": ("sourced_images", "sources", far_sources),
        "every neighbour site 0": ("formula", "seen", lambda s, nb: seen(s, 0 * nb)),
    }


OWN = {
    f.__name__: f for f in (formula, back, order, stopped, negated, cone, cone_back, model, held_alike)
}
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
    now, out = step.tick(layout, s, 1)
    force, j = step.sources(layout, s)
    w = step.weight(layout.gearing, layout.clock, s.a)
    a, _, r = step.gear(s.a, s.b, s.r, s.go, w, w, layout.gearing.stretch * (force + j))
    assert out.k.any() and not now.rd.any()
    assert frame.same([np.where(out.k == 1, a, s.a), np.where(out.k == 1, r, s.r)], [now.a, now.r])


def im(x, y):
    """Im(conj(x) y) for two hands, each the pair of rows (re, im): x_re y_im - x_im y_re."""
    return x[0] * y[1] - x[1] * y[0]


def charged(s, w, weight):
    """The hand's charge Q* = SUM Im(conj(a + b) P) / (2 s), P = W (a - b) + (r - home): David's density, exact."""
    a, b, r, go = s[:4]
    density = im(a + b, w * (a - b) + (r - home(w, go)))
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
    zero = np.zeros((1, n), dtype=object)
    state = State(
        *(draw(rng, -(1 << 10), 1 << 10, (2, n)) if sourced else frame.wide(rng, (2, n)) for _ in "ab"),
        draw(rng, 0, 1 << 20, (2, n)) % teeth[0],
        draw(rng, 0, 2, (2, n)),
        draw(rng, 0, 1 << 20, (2, n)) % drive,
        zero,
        zero,
        zero,
    )
    for t in range(4 if sourced else ROUNDS):  # J squares the gears each round
        push = s + t * draw(rng, 0, 3, (1, n)) if moving else s
        gearing = Gearing(teeth[t], push, kick, drive)  # each round at its own teeth
        layout = Layout(nb, meshes, grip, gearing, plan, GAMMA + zero, GAMMA, frame.unread())
        _, j = step.sources(layout, state)
        now, out = step.tick(layout, state, 1)
        torques = im(state.a - state.b, state.r - home(teeth[t], state.go))
        torques = torques + im(now.a - state.a, now.r - home(teeth[t], now.go))
        moved = charged(now, teeth[t], s) - charged(state, teeth[t], s)
        kicked = np.broadcast_to(kick * im(state.a, j + state.rd - now.rd), (1, n))
        ds = np.broadcast_to(drive, (1, n)).ravel()
        terms = zip(torques.ravel(), s.ravel(), kicked.ravel(), ds, strict=True)
        expected = sum(Fraction(int(x), int(2 * v)) + Fraction(int(y), int(d)) for x, v, y, d in terms)
        if not out.k.all() or (sourced and not np.any(j)) or moved != expected:
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
    assert State._fields == ("a", "b", "r", "go", "rd", "ph", "c", "tn")
    assert Gearing._fields == ("rest", "stretch", "kick", "drive")
    assert Layout._fields == ("nb", "meshes", "grip", "gearing", "plan", "rate", "gamma", "clock")
    assert Read._fields == ("first", "factor", "target")
    assert Plan._fields == ("first", "second", "factor", "target")
    assert Out._fields == ("fire", "k", "tn")


def test_a_world_is_answered_alike_in_fresh_interpreters_at_other_hash_seeds():
    assert frame.unseeded(__name__, "engine", FRAME)


def test_a_world_is_run_back_in_a_fresh_interpreter_that_never_stepped():
    assert frame.undone_elsewhere(__name__, "engine", FRAME, 0)
