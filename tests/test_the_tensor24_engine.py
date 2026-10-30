"""Tensor24's engine, the Node-clock's one act on the edge in its three generic parts: J by the vertex law, the act
against its naive model (the 00 count first, the half-open split), local, pure and turned by the 24, with the click of
no term, and its run back, the act on the mirrored state, the mirror by parity."""

import itertools

import numpy as np

from tensor24.engine import contract, step
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests import frame

SHAPE, FRAME = (3, 4, 5), (5, 5, 5)  # the drawn layouts' board, and the frame's properties' board
ROWS, TERMS, ROUNDS = 4, 30, 4  # the gears per site, J's terms, and the rounds run back
PLANES = 1 + len(SHAPE) + 1  # the readings: the value, a difference along each axis, and the force
LEGS = len(Plan._fields) - 1  # a monomial's legs: the readings a term reads and the gear it lands on
READINGS = LEGS - 1  # the readings a term of J reads, the unit where it reads fewer
PROPERTIES = ("locality", "purity", "rename", "images")
SEEDS, J_SEEDS = range(3), range(40, 43)


def draw(rng, low, high, size):
    return rng.integers(low, high, size=size).astype(object)


def empty():
    """The plan of no term: J unsourced, no push."""
    none = np.zeros(0, dtype=np.intp)
    return Plan(none, none, none, none.astype(object), none)


def unclicked():
    """The click of no term: one train whose passing is 0, its tooth carried at the key 1 from its birth, 0."""
    none = np.zeros(0, dtype=np.intp)
    return Click(none, none, none.astype(object), none, np.ones((1, 1), dtype=object))


def varied(rng, least=1, clocked=False, cubed=False):
    """A layout parted at every gear, Mesh and site: the grips, the teeth at rest, s, T_k and T_d each a divisor from
    `least`, J's terms, and where clocked two drawn rows read into every other gear's teeth (the two read none, the
    acyclic cut) and the grips' read at both ends of each Mesh; J reads three readings only where cubed."""
    nb = frame.board(SHAPE)
    n, every = nb.shape[1], np.arange(ROWS, dtype=np.intp)
    teeth, s = draw(rng, least, 20, (ROWS, n)), draw(rng, -3, 4, (ROWS, n))
    gearing = Gearing(teeth, s, *draw(rng, least, 9, (2, ROWS, 1)))  # T_k and T_d; every row even
    two = rng.permutation(ROWS)[:2]
    others = np.setdiff1d(every, two)
    clock = Read(
        np.repeat(two, len(others)), draw(rng, 1, 4, len(two) * len(others)), np.tile(others, len(two))
    )
    clock = clock if clocked else frame.unread()
    held = Read(rng.integers(0, ROWS, 4), draw(rng, -3, 4, 4), rng.integers(0, len(nb), 4))
    # any reading, or the unit, the readings' last row
    index = [rng.integers(0, PLANES * ROWS + 1, size=TERMS) for _ in range(READINGS)]
    index[-1] = index[-1] if cubed else 0 * index[-1] + PLANES * ROWS
    plan = Plan(*index, draw(rng, -9, 10, TERMS), rng.integers(0, ROWS, size=TERMS))
    grip = draw(rng, -3, 4, (ROWS, len(SHAPE) * n))
    stretch = held if clocked else frame.unread()
    reads = (
        clock,
        stretch,
        unclicked(),
        empty(),
    )  # the clocks' read, the grips' read, no click, no push
    return Layout(nb, frame.spokes(len(SHAPE)), frame.meshes_of(nb), grip, gearing, plan, *reads)


def world(rng, layout, rows=ROWS):
    """A state the act may meet: gears across 2**256, the clocks' rows in [0, 2**20), each tooth within its edge's
    dial and its T_d, one train's click tooth at its birth."""
    size = (rows, layout.nb.shape[1])
    a, b = frame.wide(rng, size), frame.wide(rng, size)
    clocks = np.unique(layout.clock.first)
    a[clocks], b[clocks] = (draw(rng, 0, 1 << 20, (len(clocks), size[1])) for _ in "ab")
    d = sum(step.weight(layout.gearing, layout.clock, x) for x in (a, b))
    r, rd = draw(rng, 0, 1 << 20, size) % (d + d) - d, draw(rng, 0, 1 << 20, size) % layout.gearing.drive
    return State(a, b, r, rd, 0 * a[:1])


def naive(layout, s):
    """The act site by site with loops and plain integers: the readings, J term by term, the drive, the push, the
    momentum on the edge split at the next edge's dial, the 00 count first; the click of no term keeps its tooth."""
    _, _, _, grip, gearing, plan, clock, stretch, _, _ = layout
    rest, s_, kick, drive, _ = (np.broadcast_to(x, s.a.shape).tolist() for x in gearing)
    first, second, third, factor, target = (x.tolist() for x in plan)
    a, b, r, rd, k = (x.tolist() for x in s)
    w, wb = (
        [row[:] for row in rest] for _ in "ab"
    )  # every gear's teeth at both slots, the clocks' read added
    terms = list(zip(*(x.tolist() for x in clock), strict=True))
    for f, m, g in terms:
        w[g] = [x + m * y for x, y in zip(w[g], a[f], strict=True)]
        wb[g] = [x + m * y for x, y in zip(wb[g], b[f], strict=True)]
    rows, n, axes = len(a), len(a[0]), range(len(SHAPE))
    gs = range(rows)
    new = [[row[:] for row in x] for x in (a, b, r, rd, k)]
    for x in itertools.product(*map(range, SHAPE)):
        i = np.ravel_multi_index(x, SHAPE)
        around = [np.ravel_multi_index(y, SHAPE) for y in frame.near(x, SHAPE)]
        meshes = [axis * n + j for axis in axes for j in (i, around[axis + axis + 1])]
        # each Spoke's grip as the grips' read lands it: the row read at the Mesh's two ends
        lift = [0] * len(around)
        for f, m, t in zip(*(x.tolist() for x in stretch), strict=True):
            lift[t] += m * (a[f][i] + a[f][around[t]])
        ends = list(enumerate(zip(meshes, around, strict=True)))
        force = [sum((grip[g][m] + lift[q]) * (a[g][j] - a[g][i]) for q, (m, j) in ends) for g in gs]
        readings = [a[g][i] for g in gs] + [
            a[g][around[q + q]] - a[g][around[q + q + 1]] for q in axes for g in gs
        ]
        source, read = [0] * rows, readings + force + [1]  # the unit, the readings' last row
        for t in range(len(factor)):
            source[target[t]] += factor[t] * read[first[t]] * read[second[t]] * read[third[t]]
        moment, count = [0] * rows, [0] * rows
        for g in gs:
            q, new[3][g][i] = divmod(source[g] + rd[g][i], drive[g][i])
            push = s_[g][i] * (force[g] + kick[g][i] * q)
            moment[g] = 2 * ((w[g][i] + wb[g][i]) * (a[g][i] - b[g][i]) + 2 * push) + r[g][i]
            count[g] = frame.split(moment[g], w[g][i] + wb[g][i])[0]  # the count at the edge's own dial
        for (
            g
        ) in gs:  # the next edge's dial reads the clocks' next counts, each given first at its own dial
            wa1 = rest[g][i] + sum(m * (a[f][i] + count[f]) for f, m, t in terms if t == g)
            v, new[2][g][i] = frame.split(moment[g], w[g][i] + wa1)
            new[0][g][i], new[1][g][i] = a[g][i] + v, a[g][i]
    return State(*(np.array(x, dtype=object) for x in new))


def formula():
    """At three drawn layouts, every gear clocked by two rows' counts, the grips read at both ends of each Mesh and J
    of three readings, the act equals the naive model at every entry, each layout stepped on two worlds in turn."""
    layouts = [(rng, varied(rng, clocked=True, cubed=True)) for rng in map(np.random.default_rng, SEEDS)]
    states = [(layout, world(rng, layout)) for rng, layout in layouts for _ in "st"]
    return all(frame.same(step.tick(layout, s), naive(layout, s)) for layout, s in states)


def alike(nb):
    """A layout alike at every site, Mesh and gear for the frame's properties: the teeth, s and T_k, no J."""
    ones = np.ones((1, nb.shape[1]), dtype=object)
    grip, gearing = ones.repeat(len(SHAPE), axis=1), Gearing(7 * ones, 2, 3, 1)  # the teeth, s, T_k, T_d
    reads = (frame.unread(), frame.unread(), unclicked(), empty())
    return Layout(nb, frame.spokes(len(SHAPE)), frame.meshes_of(nb), grip, gearing, empty(), *reads)


def engine():
    """The act in every round at a layout alike everywhere, with no out: its run back and its worlds."""
    return frame.Engine(
        lambda nb, s: (step.tick(alike(nb), State(*s)), ()),
        lambda nb, s, out: step.untick(alike(nb), State(*s)),
        lambda rng, shape, rows: world(rng, alike(frame.board(shape)), rows),
    )


def potential(rng, sites=7):
    """Whole monomials on each site's gears, each a factor and its legs among the gears' values and the unit (-1),
    with a state and a displacement of whole numbers."""
    legs = tuple(rng.integers(-1, ROWS, size=TERMS).astype(np.intp) for _ in range(LEGS))
    x, d = (draw(rng, -50, 51, (ROWS, sites)) for _ in "xd")
    return draw(rng, -9, 10, TERMS), legs, x, d


def energy(factor, legs, x):
    """V at x summed over the sites: each monomial's factor times its legs' values, the unit 1."""
    read = np.concatenate((x, np.ones_like(x[:1], dtype=object)))
    return (factor[:, None] * np.prod([read[leg] for leg in legs], axis=0)).sum()


def vertex(factor, legs, x):
    """J from the potential by the engine's vertex law and its contraction."""
    read = np.concatenate((x, np.ones_like(x[:1], dtype=object)))
    return contract.contract(contract.pushes(factor, legs), read, x)


def conserved(seed):
    """J's work on a displacement d is minus V's rate along d, read exactly by the five-point stencil a quartic keeps:
    12 V'(0) = 8 (V(1) - V(-1)) - (V(2) - V(-2))."""
    factor, legs, x, d = potential(np.random.default_rng(seed))
    v = [energy(factor, legs, x + t * d) for t in (-2, -1, 1, 2)]
    return -12 * (vertex(factor, legs, x) * d).sum() == 8 * (v[2] - v[1]) - (v[3] - v[0])


def holding(names):
    """The frame's properties on the act at a layout alike everywhere, each at every seed."""
    return all(
        frame.PROPERTIES[name](engine, FRAME, np.random.default_rng(seed))
        for name in names
        for seed in SEEDS
    )


def mirrored(layout, s):
    """The mirror by parity, as the law states it: on an even row the slots swapped, the edge's tooth -1 - s and the
    drive's tooth T_d - 1 - r_d; on an odd row the counts negated and swapped, both teeth kept; the click tooth kept."""
    even = np.broadcast_to(layout.gearing.parity, s.a.shape)
    sign, m = 2 * even - 1, step.mirror(layout, s)
    rd = s.rd + even * (layout.gearing.drive - 1 - s.rd - s.rd)
    return frame.same(m, State(sign * s.b, sign * s.a, s.r - even * (2 * s.r + 1), rd, s.k))


def test_j_is_minus_the_gradient_of_its_potential_and_pushes_no_row_its_legs_do_not_name():
    """Yes: each monomial pushes every leg by minus its factor times the others, so J is minus V's gradient, of Python
    integers on any gears.
    No: under a potential of monomials, a row no leg names stays 0 while the rows its legs name are pushed."""
    assert all(conserved(seed) for seed in J_SEEDS)
    factor, legs, x, _ = potential(np.random.default_rng(0))
    j = vertex(factor, legs, np.concatenate((x, x[:1])))  # row 0's counts again, on a row no leg names
    assert not j[-1].any() and j[:-1].any()
    # the tenth review (fc8c810ff): J took its caller's int64 gears' width, overflowing past 64 bits; back at aa8565cb2
    wide = factor * (1 << 70)  # strengths past 64 bits
    assert frame.same([vertex(wide, legs, x.astype(np.int64))], [vertex(wide, legs, x)])


def test_the_act_is_its_naive_model_on_the_edge_local_pure_and_turned_by_the_24():
    """Yes: at layouts parted everywhere the act is its naive model on the edge, the 00 count first and the half-open
    split, the click of no term keeping its tooth with no click, and the trains' order and the 24's turns are nothing
    to it. No: it reads nothing past one Mesh's reach, keeps no state, and reads no clock by its place."""
    # B2 of G1's hostile reader (9f1cf7944): every clock read at the last row, by its place, passed every test; the
    # cut's review, its X1: a J kept per plan passed while the frame's purity read a layout with no J
    assert formula() and holding(PROPERTIES)
    rng = np.random.default_rng(7)
    layout = varied(rng, clocked=True, cubed=True)
    s = world(rng, layout)
    moved, clicks = step.act(layout, s)
    assert not clicks.any() and frame.same([moved.k], [s.k]) and clicks.shape == s.k.shape
    # the second review (227cde2fe): a module's cache and the hash seed passed purity within one interpreter
    assert frame.unseeded(__name__, "engine", FRAME)


def test_the_run_back_is_exact_where_every_tooth_stands_within_its_edges_dial_and_not_past_it():
    """Yes: rounds run back bit for bit, by a fresh engine and in an interpreter that never stepped, the act on the
    mirrored state, the mirror by parity its own inverse. No: a tooth at its edge's dial, one notch past its last,
    runs back to another state; a tooth not flipped on an even row too."""
    for seed in SEEDS:
        rng = np.random.default_rng(10 + seed)  # every divisor from 2, so a swap of T_k and T_d shows
        layout, parted = varied(rng, least=2), varied(rng, least=2, clocked=True, cubed=True)
        s, t = world(rng, layout), world(rng, parted)
        *_, (end, _) = rounds(step.act, layout, s, ROUNDS)  # J squaring the gears every round
        assert frame.same(rewind(step.untick, layout, end, ROUNDS), s) and not frame.same(end, s)
        assert frame.same(step.untick(parted, step.tick(parted, t)), t)  # one round of the whole act
        odd = parted._replace(gearing=parted.gearing._replace(parity=draw(rng, 0, 2, (ROWS, 1))))
        assert mirrored(odd, t) and frame.same(step.mirror(odd, step.mirror(odd, t)), t)
    past = s._replace(r=s.r + 0)
    past.r[0, 0] = sum(step.weight(layout.gearing, layout.clock, x) for x in (s.a, s.b))[0, 0]
    assert not frame.same(step.untick(layout, step.tick(layout, past)), past)
    kept = step.mirror(layout, step.tick(layout, s))._replace(r=step.tick(layout, s).r)
    assert not frame.same(step.mirror(layout, step.tick(layout, kept)), s)
    # the second review (227cde2fe): a hidden log passed the run back; a fresh engine runs another's steps back
    assert holding(["bijectivity"])
    # the third review (81521e0f4): a queue and a memo held in the module passed the run back in one interpreter
    assert frame.undone_elsewhere(__name__, "engine", FRAME, 0)
