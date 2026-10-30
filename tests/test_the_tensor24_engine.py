"""Tensor24's engine, the Node-clock's one act in its three generic parts: J by the vertex law, the act against its
naive model, local, pure and turned by the 24, and its run back, the act on the mirrored state."""

import itertools

import numpy as np

from tensor24.engine import contract, step
from tensor24.engine.state import Gearing, Layout, Plan, Read, State
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


def unread():
    """The read of no term: every gear's teeth its rest, or every grip its rest."""
    none = np.zeros(0, dtype=np.intp)
    return Read(none, none.astype(object), none)


def varied(rng, least=1, clocked=False, cubed=False):
    """A layout parted at every gear, Mesh and site: the grips, the teeth at rest, s, T_k and T_d each a divisor from
    `least`, J's terms, and where clocked every gear's teeth read from two drawn rows and the grips' read at both ends
    of each Mesh; J reads three readings only where cubed, since they cube the counts."""
    nb = frame.board(SHAPE)
    n, every = nb.shape[1], np.arange(ROWS, dtype=np.intp)
    teeth, s = draw(rng, least, 20, (ROWS, n)), draw(rng, -3, 4, (ROWS, n))
    gearing = Gearing(teeth, s, *draw(rng, least, 9, (2, ROWS, 1)))  # T_k and T_d
    two = rng.permutation(ROWS)[:2]  # every gear reads both
    clock = Read(np.repeat(two, ROWS), draw(rng, 1, 4, len(two) * ROWS), np.tile(every, len(two)))
    clock = clock if clocked else unread()
    held = Read(rng.integers(0, ROWS, 4), draw(rng, -3, 4, 4), rng.integers(0, len(nb), 4))
    # any reading, or the unit, the readings' last row
    index = [rng.integers(0, PLANES * ROWS + 1, size=TERMS) for _ in range(READINGS)]
    index[-1] = index[-1] if cubed else 0 * index[-1] + PLANES * ROWS
    plan = Plan(*index, draw(rng, -9, 10, TERMS), rng.integers(0, ROWS, size=TERMS))
    grip = draw(rng, -3, 4, (ROWS, len(SHAPE) * n))
    stretch = held if clocked else unread()
    return Layout(nb, frame.spokes(len(SHAPE)), frame.meshes_of(nb), grip, gearing, plan, clock, stretch)


def world(rng, layout, rows=ROWS):
    """A state the act may meet: gears across 2**256, the clocks' rows in [0, 2**20), each tooth within its W and T_d."""
    size = (rows, layout.nb.shape[1])
    a, b = frame.wide(rng, size), frame.wide(rng, size)
    clocks = np.unique(layout.clock.first)
    a[clocks], b[clocks] = (draw(rng, 0, 1 << 20, (len(clocks), size[1])) for _ in "ab")
    teeth = (step.weight(layout.gearing, layout.clock, a), layout.gearing.drive)
    return State(a, b, *(draw(rng, 0, 1 << 20, size) % w for w in teeth))


def naive(layout, s):
    """The act site by site with loops and plain integers: the readings, J term by term, the drive, the push, the carry."""
    _, _, _, grip, gearing, plan, clock, stretch = layout
    rest, s_, kick, drive = (np.broadcast_to(x, s.a.shape).tolist() for x in gearing)
    first, second, third, factor, target = (x.tolist() for x in plan)
    a, b, r, rd = (x.tolist() for x in s)
    w = [row[:] for row in rest]  # every gear's teeth: its rest and the clocks' read, term by term
    for f, m, g in zip(*(x.tolist() for x in clock), strict=True):
        w[g] = [x + m * y for x, y in zip(w[g], a[f], strict=True)]
    rows, n, axes = len(a), len(a[0]), range(len(SHAPE))
    gs = range(rows)
    new = [[row[:] for row in x] for x in (a, b, r, rd)]
    for x in itertools.product(*map(range, SHAPE)):
        i = np.ravel_multi_index(x, SHAPE)
        around = [np.ravel_multi_index(y, SHAPE) for y in frame.near(x, SHAPE)]
        meshes = [axis * n + j for axis in axes for j in (i, around[axis + axis + 1])]
        # each Spoke's grip as the grips' read lands it: the row read at the Mesh's two ends
        lift = [0] * len(around)
        for f, m, t in zip(*(x.tolist() for x in stretch), strict=True):
            lift[t] += m * (a[f][i] + a[f][around[t]])
        ends = list(enumerate(zip(meshes, around, strict=True)))
        force = [sum((grip[g][m] + lift[k]) * (a[g][j] - a[g][i]) for k, (m, j) in ends) for g in gs]
        readings = [a[g][i] for g in gs] + [
            a[g][around[k + k]] - a[g][around[k + k + 1]] for k in axes for g in gs
        ]
        source, read = [0] * rows, readings + force + [1]  # the unit, the readings' last row
        for t in range(len(factor)):
            source[target[t]] += factor[t] * read[first[t]] * read[second[t]] * read[third[t]]
        for g in gs:
            q, new[3][g][i] = divmod(source[g] + rd[g][i], drive[g][i])
            push = s_[g][i] * (force[g] + kick[g][i] * q)
            v, new[2][g][i] = divmod(w[g][i] * (a[g][i] - b[g][i]) + r[g][i] + push, w[g][i])
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
    ones, none = np.ones((1, nb.shape[1]), dtype=object), np.zeros(0, dtype=np.intp)
    plan, grip = Plan(none, none, none, none.astype(object), none), ones.repeat(len(SHAPE), axis=1)
    gearing = Gearing(7 * ones, 2, 3, 1)  # the teeth, s, T_k and T_d alike everywhere
    spokes, meshes = frame.spokes(len(SHAPE)), frame.meshes_of(nb)
    return Layout(nb, spokes, meshes, grip, gearing, plan, unread(), unread())


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


def test_the_act_is_its_naive_model_local_pure_and_turned_by_the_24():
    """Yes: at layouts parted everywhere the act is its naive model, and the trains' order and the 24's turns are
    nothing to it. No: it reads nothing past one Mesh's reach, keeps no state, and reads no clock by its place."""
    # B2 of G1's hostile reader (9f1cf7944): every clock read at the last row, by its place, passed every test; the
    # cut's review, its X1: a J kept per plan passed while the frame's purity read a layout with no J
    assert formula() and holding(PROPERTIES)
    # the second review (227cde2fe): a module's cache and the hash seed passed purity within one interpreter
    assert frame.unseeded(__name__, "engine", FRAME)


def test_the_run_back_is_exact_where_every_fine_tooth_stands_within_its_teeth_and_not_past_them():
    """Yes: rounds run back bit for bit, by a fresh engine and in an interpreter that never stepped, the act on the
    mirrored state. No: a fine tooth at its teeth, one notch past its last, runs back to another state."""
    for seed in SEEDS:
        rng = np.random.default_rng(10 + seed)  # every divisor from 2, so a swap of T_k and T_d shows
        layout, parted = varied(rng, least=2), varied(rng, least=2, clocked=True, cubed=True)
        s, t = world(rng, layout), world(rng, parted)
        *_, end = rounds(step.tick, layout, s, ROUNDS)  # J squaring the gears every round
        assert frame.same(rewind(step.untick, layout, end, ROUNDS), s) and not frame.same(end, s)
        assert frame.same(step.untick(parted, step.tick(parted, t)), t)  # one round of the whole act
    past = s._replace(r=s.r + 0)
    past.r[0, 0] = layout.gearing.rest[0, 0]
    assert not frame.same(step.untick(layout, step.tick(layout, past)), past)
    # the second review (227cde2fe): a hidden log passed the run back; a fresh engine runs another's steps back
    assert holding(["bijectivity"])
    # the third review (81521e0f4): a queue and a memo held in the module passed the run back in one interpreter
    assert frame.undone_elsewhere(__name__, "engine", FRAME, 0)
