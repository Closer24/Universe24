"""Tensor24's engine, the node's one act in its three generic parts, each once with its mutants: J by the vertex law,
the act at its coefficients against a naive model, local, pure and turned by the 24, and its run back as the act on
the mirrored state."""

import functools
import itertools
import math

import numpy as np

from tensor24.engine import contract, mesh, step
from tensor24.engine.state import Gearing, Layout, Plan, Read, State
from tensor24.main import made
from tensor24.runner import board as boards
from tensor24.runner import load as loading
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests import frame

SHAPE, ROUNDS, SQUARING = (3, 4, 5), 12, 4  # the board, a run back's rounds, and a squaring run's
# the gears per site, J's terms, and the readings: the value, the three differences and the force
ROWS, TERMS, PLANES = 4, 30, 1 + 3 + 1
CUBE, FRAME = (3, 3, 3), (5, 5, 5)  # the board the 24 turn, and the frame's properties' board
SIDE, REACH = 7, 60  # the cone's side and its rounds
KINDS = ("A1", "A2", "T1", "T2")  # four trains, one kind each, at part 1
# (train, reading) twice, then the target train and the strength; the readings' planes 0 value, 1 gradient, 4 pull
COUPLINGS = [
    (0, 1, 2, 0, 0, 3),  # the scalar's gradient with the vector, into the scalar
    (2, 4, 2, 0, 2, 5),  # the vector's force crossed with the vector, into the vector
    (1, 0, 2, 0, 3, 7),  # the pseudoscalar times the vector, into the axial
    (0, 1, 1, 0, 3, 2),  # the scalar's gradient times the pseudoscalar, into the axial
    (3, 0, 2, 0, 2, 1),  # the axial with the vector, into the vector
]


def draw(rng, low, high, size):
    return rng.integers(low, high, size=size).astype(object)


def varied(
    rng, least=1, sourced=True, rows=ROWS, shape=SHAPE, clocked=False, stretched=False, cubed=False
):
    """A layout parted at every gear and site: grips, the teeth at rest, s, T_k, T_d, J or none of it, every other gear
    clocked by two drawn rows (which read none) where clocked; every divisor at least `least`, T_k too above 1."""
    nb = frame.board(shape)
    n = nb.shape[1]
    w = draw(rng, least, 20, (rows, n))
    coefficients = (
        draw(rng, -3, 4, (rows, n)),
        draw(rng, -5, 6, (rows, 1)) if least == 1 else draw(rng, least, 9, (rows, 1)),
    )
    gearing = Gearing(w, *coefficients, draw(rng, least, 9, (rows, 1)))
    every = np.arange(rows, dtype=np.intp)
    two = rng.permutation(rows)[
        : 1 + 1
    ]  # the rows the other gears read their teeth from; the two read none
    others = np.setdiff1d(every, two)
    read = Read(
        np.repeat(two, len(others)), draw(rng, 1, 4, len(two) * len(others)), np.tile(others, len(two))
    )
    read = read if clocked else frame.unread()
    highs = (PLANES * rows + 1,) * 3 + (rows,)  # any reading may be the unit, the readings' last row
    index = [rng.integers(0, high, size=TERMS).astype(np.intp) for high in highs]
    # three readings only where the act is read for one round, since they cube the counts; else the unit
    index[2] = index[2] if cubed else 0 * index[2] + PLANES * rows
    plan = Plan(*index[:3], draw(rng, -9, 10, TERMS), index[3])
    none = np.zeros(0, dtype=np.intp)
    empty = Plan(none, none, none, none.astype(object), none)  # no term: J unsourced, no push
    plan = plan if sourced else empty
    grip = draw(rng, -3, 4, (rows, 3 * n))
    # the grips' read, rows read at both ends of a Spoke's Mesh: only where the act is read for one round, since the
    # pull then multiplies counts by counts
    terms = (
        rng.integers(0, rows, 4).astype(np.intp),
        draw(rng, -3, 4, 4),
        rng.integers(0, 6, 4).astype(np.intp),
    )
    held = (Read(*terms) if stretched else frame.unread(), frame.unclicked(), empty)
    return Layout(nb, frame.spokes(), frame.meshes_of(nb), grip, gearing, plan, read, *held)


def world(rng, layout, rows=ROWS):
    """A state the act may meet: gears across 2**256, the clocks' rows in [0, 2**20), each tooth within its dial and T_d."""
    size, drive = (rows, layout.nb.shape[1]), layout.gearing.drive
    a, b = frame.wide(rng, size), frame.wide(rng, size)
    clocks = np.unique(layout.clock.first)
    for x in (a, b):
        x[clocks] = draw(rng, 0, 1 << 20, (len(clocks), size[1]))
    d = step.weight(layout.gearing, layout.clock, a) + step.weight(layout.gearing, layout.clock, b)
    r, rd = draw(rng, 0, 1 << 20, size) % (d + d) - d, draw(rng, 0, 1 << 20, size) % drive
    return State(a, b, r, rd, 0 * a[:1])  # one train's click tooth, 0 within the key 1


def naive(layout, s, shape=SHAPE):
    """The act site by site with loops and plain integers: the readings, J term by term, the drive, the push, the split
    on the edge, the 00 count first; the click of no term keeps its tooth."""
    _, _, _, grip, gearing, plan, _, stretch_read, _, _ = layout
    rows = len(s.a)
    rest, stretch, kick, drive, _ = (np.broadcast_to(x, s.a.shape).tolist() for x in gearing)
    first, second, third, factor, target = (x.tolist() for x in plan)
    a, b, r, rd, k = (x.tolist() for x in s)
    w, wb = (
        [row[:] for row in rest] for _ in "ab"
    )  # every gear's teeth at both slots: its rest and the clocks' read
    terms = list(zip(*(x.tolist() for x in layout.clock), strict=True))
    for f, m, g in terms:
        w[g] = [x + m * y for x, y in zip(w[g], a[f], strict=True)]
        wb[g] = [x + m * y for x, y in zip(wb[g], b[f], strict=True)]
    grip = np.broadcast_to(grip, (rows, grip.shape[1])).tolist()
    n = len(a[0])
    new = [[row[:] for row in x] for x in (a, b, r, rd, k)]
    for x in itertools.product(*map(range, shape)):
        i = np.ravel_multi_index(x, shape)
        around = [np.ravel_multi_index(y, shape) for y in frame.near(x, shape)]
        spokes = [axis * n + j for axis in range(3) for j in (i, around[axis + axis + 1])]
        seen = [[a[g][j] for j in around] for g in range(rows)]
        held = zip(*(x.tolist() for x in stretch_read), strict=True)
        lift = [0] * len(around)  # each Spoke's grip as the grips' read lands it, at the Mesh's two ends
        for f, m, t in held:
            lift[t] += m * (a[f][i] + a[f][around[t]])
        force = [
            sum(
                (grip[g][m] + lift[s]) * (v - a[g][i])
                for s, (m, v) in enumerate(zip(spokes, seen[g], strict=True))
            )
            for g in range(rows)
        ]
        readings = [a[g][i] for g in range(rows)]
        readings += [
            seen[g][axis + axis] - seen[g][axis + axis + 1] for axis in range(3) for g in range(rows)
        ]
        source, read = [0] * rows, readings + force + [1]  # the unit, the readings' last row
        for t in range(len(factor)):
            source[target[t]] += factor[t] * read[first[t]] * read[second[t]] * read[third[t]]
        moment, count = [0] * rows, [0] * rows
        for g in range(rows):
            q, new[3][g][i] = divmod(source[g] + rd[g][i], drive[g][i])
            push = stretch[g][i] * (force[g] + kick[g][i] * q)
            moment[g] = 2 * ((w[g][i] + wb[g][i]) * (a[g][i] - b[g][i]) + 2 * push) + r[g][i]
            count[g] = frame.split(moment[g], w[g][i] + wb[g][i])[0]  # the count at the edge's own dial
        for g in range(rows):
            wa1 = rest[g][i] + sum(m * (a[f][i] + count[f]) for f, m, t in terms if t == g)
            v, new[2][g][i] = frame.split(moment[g], w[g][i] + wa1)
            new[0][g][i], new[1][g][i] = a[g][i] + v, a[g][i]
    return State(*(np.array(x, dtype=object) for x in new))


def formula(cubed=True, stretched=False):
    """At varied layouts, every gear clocked by two rows' counts, the act equals the naive model at every entry, three
    seeds: J's terms of three readings, or the grips reading rows at both ends of each Spoke's Mesh."""
    for seed in range(3):
        rng = np.random.default_rng(seed)
        layout = varied(rng, clocked=True, cubed=cubed, stretched=stretched)
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
        *_, (end, _) = rounds(step.act, layout, s, SQUARING)
        moved = step.tick(parted, t)
        exact = frame.same(rewind(step.untick, layout, end, SQUARING), s)
        if not (exact and frame.same(step.untick(parted, moved), t) and not frame.same(end, s)):
            return False  # inexact, or the rounds moved nothing and the run back was never asked
    return True


def negated():
    """The tie rule, no J: every gear negated, its tooth flipped (-1 - s), ticks to the negation flipped alike."""
    for seed in range(3):
        rng = np.random.default_rng(20 + seed)
        layout = varied(rng, sourced=False)
        s = world(rng, layout)
        a1, b1, r1, rd1, k1 = step.tick(layout, s)
        a2, b2, r2, rd2, k2 = step.tick(layout, s._replace(a=-s.a, b=-s.b, r=-1 - s.r))
        if not frame.same([a2, b2, r2, rd2, k2], [-a1, -b1, -1 - r1, rd1, k1]):
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
        *_, (u, _) = rounds(step.act, layout, u, SIDE + SIDE)
        v, first = u._replace(a=u.a + change, b=u.b + change), far * 0 + REACH
        for count in range(1, SIDE + SIDE + 1):
            u, v = step.untick(layout, u), step.untick(layout, v)
            moved = (u.a[0] != v.a[0]) | (u.b[0] != v.b[0]) | (u.r[0] != v.r[0])
            first[moved & (first == REACH)] = count
        if early(first, far):
            return False
    return True


SHAPES = ((3, 3, 3), (4, 5, 6), (3, 4, 7), (1, 1, 1), (7, 7, 7))


def stretched():
    """The act equals the naive model where the grips read rows at both ends of each Spoke's Mesh, three seeds."""
    return formula(cubed=False, stretched=True)


def model():
    """The board's neighbours, Spokes and Meshes equal the frame's (numpy's own wrap) at every shape."""
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
    """J's terms of four trains, A1 and A2, T1 and T2, coupled through the 24's tables on the cube, entry by entry."""
    ks, c, _ = made(loading.star(len(CUBE)))
    labels = [name.upper() for name in ks._fields]
    kinds = [labels.index(k) for k in KINDS]
    dims = [ks[k].shape[-1] for k in kinds]
    first, rows = np.cumsum([0, *dims])[:-1], sum(dims)

    def side(
        t, plane
    ):  # the kind a reading enters as, and its rows: a gradient is the T1 reading of an A1 train
        if plane == 1:
            return labels.index("T1"), [(plane + axis) * rows + first[t] for axis in range(len(CUBE))]
        return kinds[t], [plane * rows + first[t] + x for x in range(dims[t])]

    terms = []
    for t, o, u, p, target, strength in COUPLINGS:
        (a, ones), (b, twos) = side(t, o), side(u, p)
        table = c[(a, b, kinds[target])]
        terms += [
            (ones[y], twos[z], strength * table[x, y, z], first[target] + x)
            for x, y, z in np.argwhere(table)
        ]
    one, two, factor, landing = zip(*terms, strict=True)
    unit = [PLANES * rows] * len(one)  # every term reads two: its third reading the unit
    return Plan(
        *(np.array(x, dtype=np.intp) for x in (one, two, unit)),
        np.array(factor, dtype=object),
        np.array(landing, dtype=np.intp),
    )


def sourced_images():
    """The sources turn with the board under the 24, J of two readings and of three (the third the A1 value no turn moves)."""
    return all(turned(plan) for plan in (cube(), cube()._replace(third=0 * cube().third)))


def turned(plan):
    """One plan's sources under the 24 on the cube, and J not 0."""
    # A1 and A2, T1 and T2, as stored: the load lays no row of its own
    nb, rows = frame.board(CUBE), 1 + 1 + 3 + 3
    n = nb.shape[1]
    ones = np.ones((1, n), dtype=object)
    gearing = Gearing(ones, ones, ones, ones)
    grip = 3 * ones.repeat(3, axis=1)
    empty = Plan(*(x[:0] for x in plan))
    reads = (frame.unread(), frame.unread(), frame.unclicked(), empty)  # no read, no click, no push
    layout = Layout(nb, frame.spokes(), frame.meshes_of(nb), grip, gearing, plan, *reads)
    s = world(np.random.default_rng(5), layout, rows)
    force, j = step.sources(layout, s.a)
    xyz, sides = np.indices(CUBE).reshape(3, -1), np.array(CUBE)[:, None]
    for m in frame.turns():
        site = np.ravel_multi_index(tuple((m @ xyz) % sides), CUBE)
        turn = frame.stored(m)[:rows, :rows].astype(
            object
        )  # the four kinds' rows as stored, each turned by its kind
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
    """The act in every round at a layout alike everywhere, with no out: its run back and its worlds."""
    return frame.Engine(
        lambda nb, s: (step.tick(alike(nb), State(*s)), ()),
        lambda nb, s, out: step.untick(alike(nb), State(*s)),
        lambda rng, shape, rows: world(rng, alike(frame.board(shape)), rows),
    )


def mutants():
    """Broken copies, each with the law that must catch it: what it replaces in the step (or the board), and with what."""
    tick, untick, gear, mirror, kick = step.tick, step.untick, step.gear, step.mirror, step.kick
    read, drive, sources = step.read, step.drive, step.sources
    gripped = mesh.gripped
    pull, seen, built, laid, calls = (
        mesh.pull,
        mesh.seen,
        boards.board,
        loading.geometry,
        itertools.count(),
    )

    def far(y):
        return y._replace(nb=y.nb[:, y.nb[0]])

    def one_end(y, a):  # the grips' read at the Spoke's own end alone
        first, factor, target = y.stretch
        landed = np.zeros(y.nb.shape, dtype=object)
        np.add.at(landed, target, factor[:, None] * a[first])
        return landed

    def doubled(*x):
        a, b, r = gear(*x)
        return a + a, b, r

    def floated(a, b, r, d_in, d_out, push, senses):
        n = senses * (d_in * (a - b) + senses * push) + r
        q = np.vectorize(lambda x, y: math.floor((x + y) / (y + y)), otypes=[object])(n, d_out + 0 * n)
        return a + q, a, n - q * (d_out + d_out) - d_out

    def unfactored(c, x):
        return read(c._replace(factor=c.first), x)

    def placed(c, x):  # every clock found at the last row, by its place
        return read(c._replace(first=0 * c.first + len(x) - 1), x)

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
        return lambda g, q: kick(g._replace(kick=teeth(g)), q)

    def reread(order):
        return lambda a, nb: seen(a, nb[order])

    def forceless(plan, readings, gears):  # the force's rows read as 0, the unit kept
        cut = len(readings) - len(gears) - 1
        return contract.contract(
            plan, np.concatenate((readings[:cut], 0 * readings[cut:-1], readings[-1:])), gears
        )

    def thirdless(plan, readings, gears):  # every term's third reading the unit, its own ignored
        return contract.contract(
            plan._replace(third=0 * plan.third + len(readings) - 1), readings, gears
        )

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
        "the mirror's tooth not flipped": ("back", "mirror", lambda y, s: mirror(y, s)._replace(r=s.r)),
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
        "the kick's teeth ignored": ("formula", "kick", kicked(lambda g: 1)),
        "the stretch off the kick": ("formula", "kick", lambda g, q: g.kick * q),
        "the drive without its fine tooth": ("formula", "drive", lambda j, d, rd: drive(j, d, 0 * rd)),
        "the drive's tooth not carried": ("formula", "drive", lambda *x: (drive(*x)[0], x[2])),
        "the gradient's ends swapped": ("formula", "seen", reread([1, 0, 3, 2, 5, 4])),
        "J read without the force": ("formula", "contract", forceless),
        "J's third reading taken as the unit": ("formula", "contract", thirdless),
        "the clocks' read off its factor": ("formula", "read", unfactored),
        "the clocks found by their place": ("formula", "read", placed),
        "the teeth without their rest": ("formula", "weight", lambda g, c, a: read(c, a) + 1),
        "T_k read from T_d": ("formula", "kick", kicked(lambda g: g.drive)),
        "the run back with T_k and T_d swapped": ("back", "untick", swapped),
        "the gradient one-sided": ("sourced_images", "seen", one_sided),
        "the gradient's axes reordered": ("sourced_images", "seen", reread([2, 3, 4, 5, 0, 1])),
        "the sources at a far site": ("sourced_images", "sources", far_sources),
        "every neighbour site 0": ("formula", "seen", lambda a, nb: seen(a, 0 * nb)),
        "the grips' read at one end alone": ("stretched", "gripped", one_end, mesh),
        "the grips' read ignored": ("stretched", "gripped", lambda y, a: 0 * gripped(y, a), mesh),
    }


OWN = {f.__name__: f for f in (formula, stretched, back, negated, cone, cone_back, model, held_alike)}
OWN["sourced_images"] = sourced_images
# the act and its run back, each with the laws that read it: the board, the formula, the reach and the frame's
ACT = ("model", "held_alike", "formula", "stretched", "negated", "cone", "locality", "purity")
PARTS = {
    "act": (*ACT, "rename", "images", "sourced_images"),
    "back": ("back", "bijectivity", "cone_back"),
}


def law(name):
    """The engine's own laws, and the frame's properties on the act at three seeds."""
    return (
        OWN[name]() if name in OWN else all(frame.holds(name, engine, FRAME, seed) for seed in range(3))
    )


def broken(part, monkeypatch):
    """Of one part, every law that fails on the engine, and every mutant aimed at its laws that its law lets pass."""
    laws, found = PARTS[part], [name for name in PARTS[part] if not law(name)]
    for mutant, (name, attribute, bad, *module) in mutants().items():
        if name not in laws:
            continue
        with monkeypatch.context() as patch:
            patch.setattr(*module or [step], attribute, bad)
            found += [mutant] if law(name) else []
    return found


def potential(rng, rows=ROWS, sites=7):
    """A potential of whole monomials on each site's gears, each a factor and four legs among the gears' values and the
    unit (-1), with a state and a displacement of whole numbers."""
    legs = tuple(rng.integers(-1, rows, size=TERMS).astype(np.intp) for _ in range(4))
    return (
        draw(rng, -9, 10, TERMS),
        legs,
        draw(rng, -50, 51, (rows, sites)),
        draw(rng, -50, 51, (rows, sites)),
    )


def energy(factor, legs, x):
    """V at x summed over the sites: each monomial's factor times its four legs' values, the unit 1."""
    read = np.concatenate((x, np.ones_like(x[:1], dtype=object)))
    return (factor[:, None] * read[legs[0]] * read[legs[1]] * read[legs[2]] * read[legs[3]]).sum()


def vertex(factor, legs, x, plan=lambda p: p, unit=1):
    """J from the potential by the engine's vertex law and its contraction, the unit read as `unit`."""
    read = np.concatenate((x, unit * np.ones_like(x[:1], dtype=object)))
    return contract.contract(plan(contract.pushes(factor, legs)), read, x)


def conserves(source):
    """J is minus V's gradient: its work on a displacement d is minus V's rate along d, read exactly by the five-point
    stencil a quartic keeps, 12 V'(0) = 8 (V(1) - V(-1)) - (V(2) - V(-2)), at three seeds."""
    for seed in range(3):
        factor, legs, x, d = potential(np.random.default_rng(40 + seed))
        v = [energy(factor, legs, x + t * d) for t in (-2, -1, 1, 2)]
        if -12 * (source(factor, legs, x) * d).sum() != 8 * (v[2] - v[1]) - (v[3] - v[0]):
            return False
    return True


def test_j_is_minus_the_gradient_of_its_potential_by_the_vertex_law_and_each_mutant_breaks_it():
    """The engine's vertex law and contraction, against the potential alone; broken, the unit read as 0, the third reading
    ignored, or the push without its sign."""
    mutants = (
        lambda *v: vertex(*v, unit=0),
        lambda *v: vertex(*v, plan=lambda p: p._replace(third=0 * p.third - 1)),
        lambda *v: vertex(*v, plan=lambda p: p._replace(factor=-p.factor)),
    )
    assert conserves(vertex) and not any(conserves(m) for m in mutants)


def test_the_act_is_its_naive_model_local_pure_and_turned_by_the_24_and_each_mutant_breaks_its_law(
    monkeypatch,
):
    """The board and its Meshes, the act at its coefficients against the naive model, one Mesh's reach, no state between
    calls, the trains' order and the 24's turns nothing to it; every mutant aimed at a law of the act or its run back;
    and a world answered alike in fresh interpreters at other hash seeds."""
    assert {name for name, *_ in mutants().values()} <= {
        name for laws in PARTS.values() for name in laws
    }
    assert not broken("act", monkeypatch) and frame.unseeded(__name__, "engine", FRAME)


def test_the_run_back_is_the_act_on_the_mirrored_state_and_each_mutant_breaks_its_law(monkeypatch):
    """Rounds run back bit for bit, by a fresh engine and within one Mesh's reach, and in an interpreter that never
    stepped."""
    assert not broken("back", monkeypatch) and frame.undone_elsewhere(__name__, "engine", FRAME, 0)
