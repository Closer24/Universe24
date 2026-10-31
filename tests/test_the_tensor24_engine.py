"""Tensor24's engine, the Node-clock's one act on the edge in its generic parts: J by the vertex law, the act against
its naive model (the 00 count first, the half-open split), local, pure and turned by the 24, the click tooth carrying the
passing of a pair, the metric pushed by the books' form, the 24 turning the act alike under the twisted action, and the run back, the act on the mirrored state."""

import itertools

import numpy as np

from tensor24.algebra.carry import carry
from tensor24.engine import contract, step
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State
from tensor24.runner.rewind import rewind
from tensor24.runner.rounds import rounds
from tests import frame

SHAPE, FRAME = (3, 4, 5), (5, 5, 5)  # the drawn layouts' board, and the cube of the frame and the 24
ROWS, TERMS, ROUNDS = 4, 30, 4  # the gears per site, J's terms, and the rounds run back
PLANES = 1 + len(SHAPE) + 1  # the readings: the value, a difference along each axis, and the force
LEGS = len(Plan._fields) - 1  # a monomial's legs: the readings a term reads and the gear it lands on
READINGS = LEGS - 1  # the readings a term of J reads, the unit where it reads fewer
PROPERTIES = ("locality", "purity", "rename", "images")
SQUARE, SEEDS, J_SEEDS = 7, range(3), range(40, 43)  # the square's rows laid: 00, 0i, ii; the seeds
HAND, KEY, BEATS = 6, (1 << 17) + 1, 400  # a T1 hand's rows (two parts), the pair's odd key, its rounds


def draw(rng, low, high, size):
    return rng.integers(low, high, size=size).astype(object)


def empty():
    """The plan of no term: J unsourced, no push."""
    return Plan(none := np.zeros(0, dtype=np.intp), none, none, none.astype(object), none)


def unclicked(terms=0):
    """The click of no edge: one train, each of J's terms weighing 0 onto it, its one side's tooth carried at the key 1 from its birth, 0."""
    return Click(
        np.zeros((terms, 1), dtype=object), np.zeros(terms, dtype=np.intp), np.ones((1, 1), dtype=object)
    )


def varied(rng, least=1, clocked=False, cubed=False):
    """A layout parted at every gear, Mesh and site: the grips, the teeth at rest, s, T_k and T_d each a divisor from `least`, J's terms
    on the value legs (the plan) and with a difference or the force among the legs (the Mesh plan), and where clocked two drawn rows read into every other gear's teeth (the two read none) and the grips' read."""
    nb = frame.board(SHAPE)
    n, every = nb.shape[1], np.arange(ROWS, dtype=np.intp)
    teeth, s = draw(rng, least, 20, (ROWS, n)), draw(rng, -3, 4, (ROWS, n))
    gearing = Gearing(teeth, s, *draw(rng, least, 9, (2, ROWS, 1)))  # T_k and T_d; every row even
    o = np.setdiff1d(every, two := rng.permutation(ROWS)[:2])
    clock = Read(np.repeat(two, len(o)), draw(rng, 1, 4, len(two) * len(o)), np.tile(o, len(two)))
    held = Read(rng.integers(0, ROWS, 4), draw(rng, -3, 4, 4), rng.integers(0, len(nb), 4))
    clock, stretch = (clock, held) if clocked else (frame.unread(), frame.unread())
    index = np.array([rng.integers(0, PLANES * ROWS + 1, size=TERMS) for _ in range(READINGS)])
    index[-1] = index[-1] if cubed else 0 * index[-1] + PLANES * ROWS  # three readings only where cubed
    factor, target = draw(rng, -9, 10, TERMS), rng.integers(0, ROWS, size=TERMS)
    valued = ((index < ROWS) | (index == PLANES * ROWS)).all(axis=0)
    legs = np.where(index == PLANES * ROWS, -1, index)  # the unit as -1, the last row of any readings
    plan = Plan(*legs[:, valued], factor[valued], target[valued])
    mesh = Plan(*index[:, ~valued], factor[~valued], target[~valued])
    grip = draw(rng, -3, 4, (ROWS, len(SHAPE) * n))
    reads = (clock, stretch, unclicked(len(plan.factor)), empty(), mesh)  # the reads, no click, no push
    return Layout(nb, frame.spokes(len(SHAPE)), frame.meshes_of(nb), grip, gearing, plan, *reads)


def world(rng, layout, rows=ROWS):
    """A state the act may meet: gears across 2**256, the clocks' rows in [0, 2**20), each tooth in its dial and T_d."""
    a, b = (frame.wide(rng, size := (rows, layout.nb.shape[1])) for _ in "ab")
    clocks = np.unique(layout.clock.first)
    a[clocks], b[clocks] = (draw(rng, 0, 1 << 20, (len(clocks), size[1])) for _ in "ab")
    d = sum(step.weight(layout.gearing, layout.clock, x) for x in (a, b))
    r, rd = draw(rng, 0, 1 << 20, size) % (d + d) - d, draw(rng, 0, 1 << 20, size) % layout.gearing.drive
    return State(a, b, r, rd, 0 * a[:1])


def naive(layout, s):
    """The act site by site with loops and plain integers: the readings, J term by term from both plans, the drive, the push, the momentum on the edge split at the next edge's dial, the 00 count first; the click of no term keeps its tooth."""
    nb, _, _, grip, gearing, plan, clock, stretch, _, _, mesh = layout
    rest, s_, kick, drive, _ = (np.broadcast_to(x, s.a.shape).tolist() for x in gearing)
    monomials = [t for p in (plan, mesh) for t in zip(*(x.tolist() for x in p), strict=True)]
    a, b, r, rd, k = (x.tolist() for x in s)
    rows, n, axes, gs, sp = len(a), len(a[0]), range(len(SHAPE)), range(len(a)), range(len(nb))
    terms = list(zip(*(x.tolist() for x in clock), strict=True))  # the clocks' read, into the teeth
    w, wb = ((np.array(rest, dtype=object) + frame.dense(clock, rows, rows) @ x).tolist() for x in s[:2])
    grips = list(zip(*(x.tolist() for x in stretch), strict=True))  # the grips' read, at both ends
    new = [[row[:] for row in x] for x in (a, b, r, rd, k)]
    for x in itertools.product(*map(range, SHAPE)):
        i = np.ravel_multi_index(x, SHAPE)
        around = [np.ravel_multi_index(y, SHAPE) for y in frame.near(x, SHAPE)]
        meshes = [axis * n + j for axis in axes for j in (i, around[axis + axis + 1])]
        lift = [sum(m * (a[f][i] + a[f][around[t]]) for f, m, q in grips if q == t) for t in sp]
        ends = list(enumerate(zip(meshes, around, strict=True)))
        force = [sum((grip[g][m] + lift[q]) * (a[g][j] - a[g][i]) for q, (m, j) in ends) for g in gs]
        near = [a[g][around[q + q]] - a[g][around[q + q + 1]] for q in axes for g in gs]
        readings = [a[g][i] for g in gs] + near
        source, read = [0] * rows, readings + force + [1]  # the unit, the readings' last row
        for first, second, third, factor, target in monomials:
            source[target] += factor * read[first] * read[second] * read[third]
        moment, count = [0] * rows, [0] * rows
        for g in gs:
            q, new[3][g][i] = divmod(source[g] + rd[g][i], drive[g][i])
            push = s_[g][i] * (force[g] + kick[g][i] * q)
            moment[g] = 2 * ((w[g][i] + wb[g][i]) * (a[g][i] - b[g][i]) + 2 * push) + r[g][i]
            count[g] = frame.split(moment[g], w[g][i] + wb[g][i])[0]  # the count at the edge's own dial
        for g in gs:  # the next edge's dial: the clocks' next counts, each given first at its own dial
            wa1 = rest[g][i] + sum(m * (a[f][i] + count[f]) for f, m, t in terms if t == g)
            v, new[2][g][i] = frame.split(moment[g], w[g][i] + wa1)
            new[0][g][i], new[1][g][i] = a[g][i] + v, a[g][i]
    return State(*(np.array(x, dtype=object) for x in new))


def alike(nb):
    """A layout alike at every site, Mesh and gear for the frame's properties: the teeth, s and T_k, no J."""
    ones = np.ones((1, nb.shape[1]), dtype=object)
    grip, gearing = ones.repeat(len(SHAPE), axis=1), Gearing(7 * ones, 2, 3, 1)  # the teeth, s, T_k, T_d
    reads = (frame.unread(), frame.unread(), unclicked(), empty(), empty())
    return Layout(nb, frame.spokes(len(SHAPE)), frame.meshes_of(nb), grip, gearing, empty(), *reads)


def engine():
    """The act in every round at a layout alike everywhere, with no out: its run back and its worlds."""
    return frame.Engine(
        lambda nb, s: (step.tick(alike(nb), State(*s)), ()),
        lambda nb, s, out: step.untick(alike(nb), State(*s)),
        lambda rng, shape, rows: world(rng, alike(frame.board(shape)), rows),
    )


def pair(g, hands=2):
    """One Node-clock, its own neighbour through every Spoke, and its state: T1 hands of six rows, the spring on every row and the vertex g between matching rows as monomials, each leg of a vertex weighing 1 onto the other hand and a spring's nothing; the giver a line hand."""
    rows, nb = HAND * hands, np.zeros((6, 1), dtype=np.intp)
    one = np.concatenate((np.arange(rows), np.arange(HAND * (hands > 1))))
    two = np.concatenate((np.arange(rows), np.arange(HAND, HAND + HAND * (hands > 1))))
    factor = np.array([1 << 10] * rows + [g] * (HAND * (hands > 1)), dtype=object)
    plan = contract.pushes(factor, (one, two, 0 * one - 1, 0 * one - 1))
    legs = np.stack((one, two))  # the vertex's legs, row by row: hand 0's, then hand 1's
    weight = np.zeros((len(plan.factor), hands), dtype=object)
    vertex = np.arange(rows, len(factor))  # the vertex's monomials, after the springs
    weight[vertex, hands - 1], weight[len(factor) + vertex, 0] = 1, 1  # each leg onto the other hand
    train = (
        np.concatenate((legs // HAND, 0 * legs)).reshape(-1).astype(np.intp)
    )  # the leg's hand, the unit's 0
    key = KEY + np.zeros((hands * hands, 1), dtype=object)
    click = Click(weight, train, key)
    ones, a = np.ones((1, 1), dtype=object), np.zeros((rows, 1), dtype=object)
    gearing, grip = Gearing((1 << 20) * ones, 1, 1, 1), ones.repeat(3, axis=1)
    reads = (frame.unread(), frame.unread(), click, empty(), empty())
    layout = Layout(nb, frame.spokes(), frame.meshes_of(nb), grip, gearing, plan, *reads)
    a[0, 0] = 1 << 8
    return layout, State(a, a.copy(), 0 * a, 0 * a, (KEY - 1) // 2 + 0 * key)


def pushed(path=False):
    """The layout alike everywhere on the cube, the square's rows laid (the 00, the 0i and the ii), with the push's plan in the books' form on the agreed planes: each ii slot pushed by minus its axis's two stretches squared on every row, the 00 slot by k0 times each other row's momenta in and out, or where path the 0i rows' alone, the rows the push does not land on (hypothesis (d)), k0 the clock read's factor, Spokes times senses, landing the 00 slot on the other rows; the spring on every row and T_d above 1, so the drive carries."""
    spokes, rows = len(frame.spokes(len(SHAPE))), np.arange(SQUARE, dtype=np.intp)
    k0, stretch, unit = spokes * (spokes // len(SHAPE)), np.arange(spokes * SQUARE), 0 * rows - 1
    read = rows[1 : 1 + len(SHAPE)] if path else rows[1:]  # the rows whose momenta the 00 slot reads
    first = np.concatenate((stretch, spokes * SQUARE + read))
    second = np.concatenate((stretch, (spokes + 1) * SQUARE + read))
    factor = np.array([-1] * len(stretch) + [k0] * len(read), dtype=object)
    target = np.concatenate((np.repeat(np.repeat(rows[-len(SHAPE) :], 2), SQUARE), 0 * read))
    push = Plan(first, second, 0 * first + (spokes + 2) * SQUARE, factor, target)
    clock = Read(0 * rows[1:], k0 + 0 * rows[1:].astype(object), rows[1:])
    plan = contract.pushes(np.full(SQUARE, 1 << 10, dtype=object), (rows, rows, unit, unit))
    layout = alike(frame.board(FRAME))
    gearing, click = layout.gearing._replace(drive=7), unclicked(len(plan.factor))
    return layout._replace(gearing=gearing, plan=plan, clock=clock, click=click, push=push)


def twisted(layout, s, m, flipped=True):
    """A turn m of the 24 on a state of the square's rows: the sites moved, the 0i rows turned by m and the ii rows by its axes; a negated row's counts negated and its teeth flipped, -1 - s and T_d - 1 - r_d, or the teeth left as they stand."""
    xyz, sides = np.indices(FRAME).reshape(len(FRAME), -1), np.array(FRAME)[:, None]
    site = np.ravel_multi_index(tuple(m.T @ xyz % sides), FRAME)  # each site's source under the turn
    turn, axes = np.eye(SQUARE, dtype=object), len(FRAME)
    turn[1 : 1 + axes, 1 : 1 + axes], turn[1 + axes :, 1 + axes :] = m.tolist(), abs(m).tolist()
    t, drive = turn if flipped else abs(turn), layout.gearing.drive
    teeth = (t @ (2 * s.r + 1) - 1) // 2, (t @ (2 * s.rd + 1 - drive) + drive - 1) // 2
    return State(*(x[:, site] for x in (turn @ s.a, turn @ s.b, *teeth, s.k)))


def potential(rng, sites=7):
    """Whole monomials on each site's gears, each a factor and its legs among the gears' values and the unit (-1), with a state and a displacement of whole numbers."""
    legs = tuple(rng.integers(-1, ROWS, size=TERMS).astype(np.intp) for _ in range(LEGS))
    x, d = (draw(rng, -50, 51, (ROWS, sites)) for _ in "xd")
    return draw(rng, -9, 10, TERMS), legs, x, d


def vertex(factor, legs, x):
    """J from the potential by the engine's vertex law and its contraction."""
    return contract.contract(contract.pushes(factor, legs), step.valued(x), x)


def conserved(seed):
    """J's work on a displacement d is minus V's rate along d by the five-point stencil a quartic keeps: 12 V'(0) = 8 (V(1) - V(-1)) - (V(2) - V(-2)); V at x is summed over the sites, each monomial's factor times its legs' values, the unit 1."""
    factor, legs, x, d = potential(np.random.default_rng(seed))
    energy = lambda y: (factor[:, None] * np.prod([step.valued(y)[leg] for leg in legs], axis=0)).sum()  # noqa: E731
    v = [energy(x + t * d) for t in (-2, -1, 1, 2)]
    return -12 * (vertex(factor, legs, x) * d).sum() == 8 * (v[2] - v[1]) - (v[3] - v[0])


def holding(laws):
    """The frame's properties on the act at a layout alike everywhere, each at every seed."""
    return all(frame.PROPERTIES[n](engine, FRAME, np.random.default_rng(s)) for s in SEEDS for n in laws)


def test_j_is_minus_the_gradient_of_its_potential_and_pushes_no_row_its_legs_do_not_name():
    """Yes: each monomial pushes every leg by minus its factor times the others, so J is minus V's gradient, of Python integers on any
    gears. No: under a potential of monomials, a row no leg names stays 0 while the named rows are pushed."""
    assert all(conserved(seed) for seed in J_SEEDS)
    factor, legs, x, _ = potential(np.random.default_rng(0))
    j = vertex(factor, legs, np.concatenate((x, x[:1])))  # row 0's counts again, on a row no leg names
    assert not j[-1].any() and j[:-1].any()
    wide = factor * (1 << 70)  # strengths past 64 bits: the tenth review's int64 gears (fc8c810ff)
    assert frame.same([vertex(wide, legs, x.astype(np.int64))], [vertex(wide, legs, x)])


def test_the_act_is_its_naive_model_on_the_edge_local_pure_and_turned_by_the_24():
    """Yes: at three drawn layouts, clocked, the grips read and J of three readings, each stepped on two worlds, the act is its naive
    model on the edge, the 00 count first and the half-open split, the click of no term keeping its tooth with no click, and the trains'
    order and the 24's turns are nothing to it. No: it reads nothing past one Mesh's reach, keeps no state, and reads no clock by its place."""
    layouts = [(rng, varied(rng, clocked=True, cubed=True)) for rng in map(np.random.default_rng, SEEDS)]
    states = [(layout, world(rng, layout)) for rng, layout in layouts for _ in "st"]
    assert all(frame.same(step.tick(layout, s), naive(layout, s)) for layout, s in states)
    assert holding(PROPERTIES)  # G1's B2 and the cut's X1 mutants
    layout = varied(rng := np.random.default_rng(7), clocked=True, cubed=True)
    moved, clicks = step.act(layout, s := world(rng, layout))
    assert not clicks.any() and frame.same([moved.k], [s.k]) and clicks.shape == s.k.shape
    assert frame.unseeded(__name__, "engine", FRAME)  # the second review: a cache, the hash seed


def test_the_click_tooth_carries_the_pairs_passing_and_the_mirror_keeps_it():
    """Yes: a line hand and a hand at rest tied at one Node-clock click on their edge's two sides with quotients summing to 0 and teeth to
    key - 1 in every round, the diagonal's never, run back by the same act on the mirrored state with the quotients negated. No: a lone hand with its spring clicks nowhere, its tooth at its birth; and the click tooth flipped under the mirror instead of kept does not return the teeth (FRAMES 4's no, which A1 struck on an identity that fails: -n + (d - 1 - r') is not -q d + (d - 1 - r) in general)."""
    layout, s = pair(1 << 10)
    steps = list(rounds(step.act, layout, s, BEATS))
    states, clicks = [s, *(t for t, _ in steps)], [q for _, q in steps]
    hands = layout.click.weight.shape[-1]
    diagonal = slice(None, None, hands + 1)  # the sides (t, t)
    given, taken = (
        np.array([q[side] for q in clicks]) for side in (1, hands)
    )  # the sides (0, 1) and (1, 0)
    assert given.any() and frame.same([given], [-taken]) and not any(q[diagonal].any() for q in clicks)
    assert all(
        int((t.k[1] + t.k[hands]).sum()) == KEY - 1 and frame.same([t.k[diagonal]], [s.k[diagonal]])
        for t in states
    )
    backs = [step.act(layout, step.mirror(layout, s1)) for s1 in states[1:]]
    assert all(frame.same(step.mirror(layout, m), t) for (m, _), t in zip(backs, states, strict=False))
    assert all(frame.same([q], [-r]) for (_, q), r in zip(backs, clicks, strict=True))
    flips = [step.tick(layout, step.mirror(layout, t)._replace(k=KEY - 1 - t.k)) for t in states[1:]]
    assert not all(frame.same([KEY - 1 - f.k], [t.k]) for f, t in zip(flips, states, strict=False))
    lone, t = pair(0, hands=1)
    quiet = list(rounds(step.act, lone, t, BEATS))
    assert frame.same([quiet[-1][0].k], [t.k]) and not any(q.any() for _, q in quiet)


def test_the_metric_is_pushed_by_the_stretches_and_the_momenta_in_the_books_form():
    """Yes: a tent along z at rest pushes the zz slot by -(2 g^2) per row on its slopes and no other slot; a hand gliding alike everywhere
    pushes the 00 slot by k0 times the other rows' momenta in and out and no ii slot. No: the apex, one stretch 0, takes -(g^2) a row."""
    layout, g = pushed(), 5
    z = np.indices(FRAME)[-1].reshape(-1)
    tent = (g * np.minimum(z, FRAME[-1] - z)).astype(object)[None, :].repeat(SQUARE, axis=0)
    j = step.stress(layout, State(tent, tent.copy(), 0 * tent, 0 * tent, 0 * tent[:1]), 0 * tent)
    slope, apex = np.ravel_multi_index((0, 0, 1), FRAME), np.ravel_multi_index((0, 0, 2), FRAME)
    assert j[:, slope].tolist() == [0] * (SQUARE - 1) + [-g * g * SQUARE - g * g * SQUARE]
    assert j[:, apex].tolist() == [0] * (SQUARE - 1) + [-g * g * SQUARE]  # one stretch squared
    k0, rest, v = layout.clock.factor[0], layout.gearing.rest[0, 0], 3
    a, b = (1 << 30) + 0 * tent, (1 << 30) - v + 0 * tent
    a[0], b[0] = 0, 0  # the 00 slot still, so every row's teeth stand at rest at both slots
    j = step.stress(layout, State(a, b, 0 * a, 0 * a, 0 * a[:1]), 0 * a)
    sigma = frame.split(2 * (rest + rest) * v, rest + rest)[0]  # the momentum in rest-dial turns
    assert (j[0] == k0 * (SQUARE - 1) * sigma * sigma).all() and not j[1:].any() and sigma == v


def test_the_24_turn_the_act_alike_under_the_twisted_action_and_not_with_the_teeth_kept():
    """Yes: on the cube under the push, the clock moving and T_d above 1 on the square's rows, every turn of the 24 commutes with the
    act, at a state drawn across 2**256, when a negated row's counts and teeth are flipped with it. No: with the teeth left as they
    stand, the three turns that negate no row commute alone; the other 21 fail at round 1."""
    s = world(np.random.default_rng(24), layout := pushed(), SQUARE)
    out, turns = step.tick(layout, s), list(frame.turns())
    for flipped, holds in ((True, [True] * len(turns)), (False, [not (m < 0).any() for m in turns])):
        turned = [step.tick(layout, twisted(layout, s, m, flipped)) for m in turns]
        images = [twisted(layout, out, m, flipped) for m in turns]
        assert [frame.same(x, y) for x, y in zip(turned, images, strict=True)] == holds


def test_the_run_back_is_exact_where_every_tooth_stands_within_its_edges_dial_and_not_past_it():
    """Yes: rounds run back bit for bit, by a fresh engine and in an interpreter that never stepped, the act on the mirrored state, the
    mirror by parity its own inverse: an even row's slots swapped and its teeth flipped, -1 - s and T_d - 1 - r_d, an odd row's counts
    negated and swapped and its teeth kept, the click tooth kept; and one round under the push whose 00 slot reads the momenta of no row the push lands on (hypothesis (d)). No: a tooth at its edge's dial, one notch past its last, runs back to another state; a tooth not flipped on an even row too; the push reading the ii rows' momenta, which J5 lands on, so that the stress reads a momentum out at the drive's first quotient that the round does not take; and one half of the passing alone, the fourth text's, carried at the key does not run back."""
    for seed in SEEDS:
        rng = np.random.default_rng(10 + seed)  # every divisor from 2, so a swap of T_k and T_d shows
        layout, parted = varied(rng, least=2), varied(rng, least=2, clocked=True, cubed=True)
        s, t = world(rng, layout), world(rng, parted)
        *_, (end, _) = rounds(step.act, layout, s, ROUNDS)  # J squaring the gears every round
        assert frame.same(rewind(step.untick, layout, end, ROUNDS), s) and not frame.same(end, s)
        assert frame.same(step.untick(parted, step.tick(parted, t)), t)  # one round of the whole act
        odd = parted._replace(gearing=parted.gearing._replace(parity=draw(rng, 0, 2, (ROWS, 1))))
        even = np.broadcast_to(odd.gearing.parity, t.a.shape)
        sign, rd = 2 * even - 1, t.rd + even * (odd.gearing.drive - 1 - t.rd - t.rd)
        law = State(sign * t.b, sign * t.a, t.r - even * (2 * t.r + 1), rd, t.k)  # the mirror by parity
        assert frame.same(step.mirror(odd, t), law) and frame.same(step.mirror(odd, law), t)
    lawful, drawn = pushed(path=True), world(np.random.default_rng(24), pushed(), SQUARE)
    assert frame.same(step.untick(lawful, step.tick(lawful, drawn)), drawn)  # hypothesis (d) kept
    assert not frame.same(step.untick(pushed(), step.tick(pushed(), drawn)), drawn)  # the ii rows read
    past = s._replace(r=s.r + 0)
    past.r[0, 0] = sum(step.weight(layout.gearing, layout.clock, x) for x in (s.a, s.b))[0, 0]
    assert not frame.same(step.untick(layout, step.tick(layout, past)), past)
    kept = step.mirror(layout, step.tick(layout, s))._replace(r=step.tick(layout, s).r)
    assert not frame.same(step.mirror(layout, step.tick(layout, kept)), s)
    tied, u = pair(1 << 10)
    states = [u, *(w for w, _ in rounds(step.act, tied, u, BEATS // 10))]
    half = lambda a, a1, k: carry(step.passing(tied.click, tied.plan, a, a, a1), KEY, k)[1]  # noqa: E731
    steps = list(zip(states, states[1:], strict=False))  # J(a) (a+ - a), the window's forward half alone
    teeth = list(itertools.accumulate(steps, lambda k, w: half(w[0].a, w[1].a, k), initial=u.k))
    mirrored = [
        [step.mirror(tied, w).a for w in pair] for pair in steps
    ]  # the window run back: a, then a-
    backs = [half(a, back, k) for (back, a), k in zip(mirrored, teeth[1:], strict=True)]
    assert not all(frame.same([b], [k]) for b, k in zip(backs, teeth[:-1], strict=True))
    # the second and third reviews (227cde2fe, 81521e0f4): a hidden log, a queue and a memo passed the run back
    assert holding(["bijectivity"]) and frame.undone_elsewhere(__name__, "engine", FRAME, 0)
