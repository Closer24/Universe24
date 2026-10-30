"""Clock: the harness of the edge's probes: the engine's own load and act, and beside it the edge act, the velocity's
tooth given to the edge between the two slots, kept in one dial of both slots' teeth, D = W(b) + W(a), counted from
its middle; the cube's 24 as matrices of Spokes; the lays that move the clock.
Algebra: whole numbers and the engine's carry alone. The centred split of n at the dial m = 2 D is two carries and
lit(): n + D = q0 m + r0, the tooth s = r0 - D in [-D, D), and where it lands on the edge (r0 = 0) the count is taken
even. The round: N = 2 (D_in (a - b) + 2 push) + s, split at 2 D_out, D_in = W(b) + W(a), D_out = W(a) + W(a+).
Board: the example world's universe (examples/tensor24: light, A1 of two parts, and the metric family, the four-vector's
square; den, full_rate and width as the file has them) on a cube of side 3: 12 rows at 27 sites, 324 gears; the square's
00 slot laid uniform so that W moves by whole counts a round, its ii slots at 0 (every grip at its rest den Gamma^2);
the 00 row's own teeth read no row (the acyclic cut, probe section 6), so that W(a+) is a reading and no fixed point.
Clicks: n/a: the probes compare states and books, never a click.

The turn machinery (made, rows_turn, sites_turn, signs, recurrence, drawn) follows the second SYM24 text's common.py.
"""

import itertools
import json
from pathlib import Path

import numpy as np

from tensor24 import main
from tensor24.algebra.carry import carry, flip, lit
from tensor24.engine import contract
from tensor24.engine import kinds as K
from tensor24.engine import step
from tensor24.engine.state import Layout, Read, State
from tensor24.runner import load

SIDE = 3
SHAPE = (SIDE, SIDE, SIDE)
SITES = SIDE * SIDE * SIDE
LABELS = ("A1", "A2", "E", "T1", "T2")
# the example world's universe, the one on main (examples/tensor24): its trains (light, A1 of two parts; the metric
# family, the four-vector's square) and its integers (den, full_rate, width) are read, nothing declared here
UNIVERSE = Path(__file__).resolve().parent.parent.joinpath("t24b", "examples", "tensor24", "universe.json")
TWO_64 = 18446744073709551616
TWO_33 = 8589934592
TWO = 1 + 1


# ---------------------------------------------------------------- the split and the edge act


def split(n, m):
    """The centred split of n at the dial m (an even count, twice the edge's teeth D): n = q m + s with -D <= s <= D,
    and where s lands on the dial's edge (|s| = D) the count q is taken even. Two carries and lit(), no if."""
    half, _ = carry(m, TWO, 0)
    q0, r0 = carry(n + half, m, 0)
    _, odd = carry(q0, TWO, 0)
    tie = 1 - lit(r0)
    adjust = tie * odd
    return q0 - adjust, r0 - half + adjust * m


def split_up(n, m):
    """The mutant: the centred split with the tie taken upward (s = -D, q = q0), the plain carry from the half."""
    half, _ = carry(m, TWO, 0)
    q0, r0 = carry(n + half, m, 0)
    return q0, r0 - half


def split_floor(n, m):
    """The mutant: the plain carry, s in [0, m)."""
    return carry(n, m, 0)


def acyclic(layout):
    """The layout with every row's self-read cut from the clocks' read: a row's teeth read no row that reads it; with the
    loader's lay (every row reads the 00 slot) the one cut is the 00 row's own, whose teeth then stand at rest."""
    first, factor, target = layout.clock
    keep = first != target
    return layout._replace(clock=Read(first[keep], factor[keep], target[keep]))


def dials(layout, a, b):
    """W at the two slots, and the edge's dial D = W(b) + W(a)."""
    wa = step.weight(layout.gearing, layout.clock, a)
    wb = step.weight(layout.gearing, layout.clock, b)
    return wa, wb, wa + wb


def edge_tick(layout, s, splitter=split):
    """The edge act: N = 2 (D_in (a - b) + 2 push) + s split at 2 D_out, D_in = W(b) + W(a), D_out = W(a) + W(a+).
    W(a+) is read from the 00 slot's next count, which the 00 row's own carry gives first (its teeth read no row, so
    its D_out is its D_in): one provisional split at 2 D_in gives every row a count, of which only the rows whose teeth
    read no row are used, through the clocks' read; then the split at 2 D_out. The drive as built."""
    a, b, t, rd = s
    gearing = layout.gearing
    force, j = step.sources(layout, a)
    _, _, _, teeth = gearing
    q_d, rd1 = step.drive(j, teeth, rd)
    push = step.driven(gearing, force, q_d)
    wa, _, d_in = dials(layout, a, b)
    n = TWO * (d_in * (a - b) + TWO * push) + t
    q1, _ = splitter(n, TWO * d_in)
    wa1 = step.weight(gearing, layout.clock, a + q1)
    d_out = wa + wa1
    q, t1 = splitter(n, TWO * d_out)
    return State(a + q, a, t1, rd1)


def edge_mirror(layout, s):
    """Time's reversal on the edge: the slots swapped and the tooth negated, no teeth read; the drive's tooth flipped in
    its standing teeth as built."""
    a, b, t, rd = s
    _, _, _, teeth = layout.gearing
    return State(b, a, -t, flip(rd, teeth))


def edge_mirror_unnegated(layout, s):
    """The mutant: the slots swapped and the tooth kept."""
    a, b, t, rd = s
    _, _, _, teeth = layout.gearing
    return State(b, a, t, flip(rd, teeth))


def edge_untick(layout, s, splitter=split, mirror=edge_mirror):
    """The run back: the edge tick on the mirrored state, mirrored."""
    return mirror(layout, edge_tick(layout, mirror(layout, s), splitter), )


def edge_promise(layout, s):
    """The edge's promise on a state: both slots' teeth at least 1, and the tooth within its dial, |s| <= D_in, the
    edge |s| = D_in only at an even velocity."""
    a, b, t, _ = s
    wa, wb, d = dials(layout, a, b)
    _, odd = carry(a - b, TWO, 0)
    inside = (abs(t) < d) | ((abs(t) == d) & (odd == 0))
    return bool((wa >= 1).all() and (wb >= 1).all() and inside.all())


def built_promise(layout, s):
    """The act as built's promise: every fine tooth within the teeth the round reads, those teeth at least 1."""
    w = step.teeth(layout, s)
    return bool((w >= 1).all() and (s.r >= 0).all() and (s.r < w).all())


# ---------------------------------------------------------------- the board and the lays


def universe():
    """The example world's universe file, read as it stands: its trains and its integers."""
    return json.loads(UNIVERSE.read_text(encoding="utf-8"))


def grip_of(u):
    """The file's grip at rest, den Gamma^2: one notch of a slot moves a grip by one count (load.geared), so it is the
    Mesh unit and, with J = 0, the pitch every fine tooth moves by; the probes lay the clock and the teeth in it."""
    integers = u["integers"]
    return integers["den"] * integers["full_rate"] * integers["full_rate"]


def row_names(trains):
    """Each row's name from the trains: a lone train's rows by its label and index, the square's by its slots."""
    slots = ["00", "0x", "0y", "0z", "xx", "yy", "zz", "yz", "zx", "xy"]
    names = []
    for t in range(len(trains)):
        train = trains[t]
        if train.square:
            names += slots
        else:
            names += [f"train {t} row {k}" for k in range(train.rows())]
    return names


def row_00(trains):
    """The first row of the train that is the four-vector's square: the 00 slot, every row's teeth."""
    return next(int(trains[t].first) for t in range(len(trains)) if trains[t].square)


def recurrence(seed):
    """An endless row of whole numbers from a fixed recurrence, each step one carry: no random module."""
    v = seed
    while True:
        _, v = carry(v * 6364136223846793005 + 1442695040888963407, TWO_64, 0)
        yield v


def drawn(source, low, high):
    """A whole number in [low, high] from the recurrence's high bits, by two carries."""
    high_bits, _ = carry(next(source), TWO_33, 0)
    _, x = carry(high_bits, high - low + 1, 0)
    return low + x


def made():
    """The 24 as the engine makes them: every candidate matrix of three Spokes, its weight, its kinds and its square."""
    spokes = load.star(len(SHAPE))
    matrix, weight = K.turns(spokes)
    held = K.kinds(matrix)
    return spokes, matrix, weight, held, K.square(held)


def board(a00, b00, seed, span=40, tooth=5, shape=SHAPE, cut=True):
    """The engine's own load of the example universe's trains on the probe's piece (a cube of 3) and setting: the
    square's 00 slot at (a00, b00) counts with its tooth 0 at every site (W = rest + a00 at round 0 for every row but the
    00 row, moving by a00 - b00 every round), its ii slots at 0 (every grip at its rest den Gamma^2), every other
    gear's two slots drawn in [-span, span] and its tooth drawn in [-tooth, tooth] grips (the pitch of the fine teeth at
    J = 0; the edge's tooth, which the probes map into [0, W) for the act as built). The clock read is cut acyclic
    unless cut is False."""
    sites = 1
    for side in shape:
        sites = sites * side
    u = universe()
    grip = grip_of(u)
    turned_kinds, c, square = main.made(load.star(len(shape)))
    empty, _ = load.load(u, {"version": 1, "gears": []}, sites, turned_kinds, c, square)
    source = recurrence(seed)
    gears = []
    for t in range(len(empty.trains)):
        train = empty.trains[t]
        for component in range(train.rows()):
            for x in range(sites):
                if train.square and component == 0:
                    a, b, r = a00, b00, 0
                elif train.square and 4 <= component <= 6:
                    a, b, r = 0, 0, 0
                else:
                    a, b = drawn(source, -span, span), drawn(source, -span, span)
                    r = grip * drawn(source, -tooth, tooth)
                gears.append([t, component, x, a, b, r])
    loaded, laid = load.load(u, {"version": 1, "gears": gears}, sites, turned_kinds, c, square)
    assert not laid, laid
    layout = main.layout(u, list(shape), loaded)
    if cut:
        layout = acyclic(layout)
    return layout, State(*loaded.state), loaded.trains


def with_spring(layout, row, f):
    """The layout with one spring f x^2 on a row: each of its two legs pushed by -f times the other (the unit for the
    legs it lacks), so the row is pushed by -2 f x; its pushes do not sum to 0 over the board."""
    unit = np.array([-1], dtype=np.intp)
    legs = (np.array([row], dtype=np.intp), np.array([row], dtype=np.intp), unit, unit)
    return layout._replace(plan=contract.pushes(np.array([f], dtype=object), legs))


def to_built(layout, s):
    """The edge state read as the act as built's: the tooth t = 4 r + 2 - D on a still clock, so r = (t - 2 + D) div 4,
    with D = 2 W; the probes lay t so that this is exact."""
    _, _, d = dials(layout, s.a, s.b)
    r, rest = carry(s.r - TWO + d, TWO * TWO, 0)
    assert int((rest != 0).sum()) == 0
    return State(s.a, s.b, r, s.rd)


def to_edge(layout, s):
    """The act as built's state read on the edge of a still clock: t = 4 r + 2 - D, the centre of the tooth's cell."""
    _, _, d = dials(layout, s.a, s.b)
    return State(s.a, s.b, TWO * TWO * s.r + TWO - d, s.rd)


# ---------------------------------------------------------------- the turns


def blocks(trains, lift, square_block):
    """The turn on every row as one block matrix: each lone train's kinds' matrices from the lift, the square's block
    for the square."""
    held = []
    for t in range(len(trains)):
        train = trains[t]
        if train.square:
            held.append(np.array(square_block, dtype=object))
            continue
        for _ in range(train.part):
            for kind in train.kinds:
                held.append(np.array(lift[LABELS[kind]], dtype=object))
    n = sum(b.shape[0] for b in held)
    p = np.zeros((n, n), dtype=object)
    at = 0
    for b in held:
        p[at : at + b.shape[0], at : at + b.shape[0]] = b
        at += b.shape[0]
    return p


def rows_turn(trains, held, square, g):
    """The turn g of the 24 on every row: the engine's own kinds and square."""
    lift = {label: held[k][g] for k, label in enumerate(LABELS)}
    return blocks(trains, lift, square[g])


def sites_turn(m, shape=SHAPE):
    """Each site's index after the turn m: the coordinates x to m x, each wrapped on its own side by the carry."""
    xyz = np.indices(shape).reshape(len(shape), -1)
    moved = np.array(m, dtype=np.intp) @ xyz
    _, wrapped = carry(moved, np.array(shape, dtype=np.intp)[:, None], 0)
    return np.ravel_multi_index(tuple(wrapped), shape)


def signs(p):
    """The two halves of a signed permutation: its + entries and its - entries, each a 0 or 1 matrix."""
    plus, _ = carry(p * p + p, TWO, 0)
    return plus, p * p - plus


def moved(arrays, site):
    """Arrays whose sites are moved by the turn's site map."""
    out = []
    for x in arrays:
        y = np.empty_like(x)
        y[:, site] = x
        out.append(y)
    return out


def turned_edge(s, p, site, negate=True):
    """The edge state turned: rows by p (a signed permutation), sites by site, the tooth of a flipped row negated, which
    is p @ t itself; with negate False the tooth only moved (the mutant). The drive's tooth moved (T_d = 1: it is 0)."""
    plus, minus = signs(p)
    t = p @ s.r if negate else (plus + minus) @ s.r
    return State(*moved((p @ s.a, p @ s.b, t, (plus + minus) @ s.rd), site))


def turned_in_dial(s, p, site, dial, wd):
    """A state turned with the tooth of a flipped row reflected in a dial, dial - 1 - r (the act as built's flip; the
    floor mutant's in the edge's dial 2 D)."""
    plus, minus = signs(p)
    r = plus @ s.r + minus @ flip(s.r, dial)
    rd = plus @ s.rd + minus @ flip(s.rd, wd)
    return State(*moved((p @ s.a, p @ s.b, r, rd), site))


def same(s, t):
    """Every slot equal, gear by gear."""
    return all(bool((x == y).all()) for x, y in zip(s, t, strict=True))


def differing(s, t):
    """The gears whose now slot differs, and whose tooth differs."""
    return int((s.a != t.a).sum()), int((s.r != t.r).sum())


def forward(tick, promise, layout, s, rounds):
    """The run: the states from round 0 to the last round whose promise holds, and the round where it first breaks."""
    states, broke = [s], None
    for n in range(rounds):
        if not promise(layout, states[-1]):
            broke = n
            break
        states.append(tick(layout, states[-1]))
    return states, broke


def bits(states):
    """The widest count of the run, in bits."""
    return max(int(x).bit_length() for s in states for arr in s for x in arr.flat)


def holds_edge(layout, states, p, site, tick=edge_tick, negate=True):
    """Per round n of the run: 1 where tick^n(turned s) equals turned(tick^n s), the edge's turn."""
    t = turned_edge(states[0], p, site, negate)
    held = []
    for n in range(1, len(states)):
        t = tick(layout, t)
        held.append(int(same(t, turned_edge(states[n], p, site, negate))))
    return held


def holds_in_dial(layout, states, p, site, tick, dial_of):
    """Per round n: 1 where tick^n(turned s) equals turned(tick^n s), the tooth of a flipped row reflected in the dial
    dial_of(layout, states, n) (the act as built: the teeth of the round that kept it; the floor edge: 2 D of the edge
    the tooth lives on)."""
    wd = layout.gearing.drive
    t = turned_in_dial(states[0], p, site, dial_of(layout, states, 0), wd)
    held = []
    for n in range(1, len(states)):
        t = tick(layout, t)
        held.append(int(same(t, turned_in_dial(states[n], p, site, dial_of(layout, states, n), wd))))
    return held


def built_dial(layout, states, n):
    """The act as built's dial for the tooth at round n: the teeth of the round that kept it, W(b_n) = W(a_(n-1)); at
    round 0 the teeth the first round reads."""
    return step.teeth(layout, states[n if n == 0 else n - 1])


def edge_dial(layout, states, n):
    """The edge's dial for the tooth at round n: 2 D of the edge it lives on, 2 (W(b_n) + W(a_n))."""
    _, _, d = dials(layout, states[n].a, states[n].b)
    return TWO * d


def twenty_four(trains):
    """The 24 turns: per turn its matrix m, its row block p and its site map."""
    _, matrix, weight, held, square = made()
    out = []
    for g in np.nonzero(weight)[0]:
        m = matrix[g]
        out.append((m, rows_turn(trains, held, square, g), sites_turn(m)))
    return out


def flipping(p):
    """The rows whose sign the turn flips, and whether the turn flips any."""
    _, minus = signs(p)
    rows = minus.sum(axis=1) > 0
    return rows, bool(rows.any())


def row_books_edge(layout, s):
    """Per row: the edge's momentum P = the sum over the sites of 2 D_in (a - b) + t, in half-teeth, and S = the sum of
    (a - b)."""
    _, _, d = dials(layout, s.a, s.b)
    v = s.a - s.b
    return (TWO * d * v + s.r).sum(axis=1), v.sum(axis=1)


def row_books_built(layout, s):
    """Per row: the act as built's P = W S + R at the now slot's teeth, S and R."""
    w = step.teeth(layout, s)
    v = s.a - s.b
    return (w * v + s.r).sum(axis=1), v.sum(axis=1), s.r.sum(axis=1)


def pushes_sum(layout, s):
    """Per row: the sum over the sites of the push s (F + T_k q_d) the round reads at the now slot."""
    force, j = step.sources(layout, s.a)
    _, _, _, teeth = layout.gearing
    q_d, _ = step.drive(j, teeth, s.rd)
    return step.driven(layout.gearing, force, q_d).sum(axis=1)


def in_grips(x, grip):
    """A count written in grips: the nearest whole grips and the count left over, or that remainder in permille of a
    grip where it is not small."""
    q, rest = carry(x, grip, 0)
    if rest + rest > grip:
        q, rest = q + 1, rest - grip
    unit = "grip" if abs(int(q)) == 1 else "grips"
    if rest == 0:
        return f"{int(q)} {unit}"
    if abs(int(rest)) <= 1000:
        return f"{int(q)} {unit} {'+' if rest > 0 else '-'} {abs(int(rest))}"
    permille, _ = carry(1000 * abs(int(rest)), grip, 0)
    return f"{int(q)} {unit} {'+' if rest > 0 else '-'} {int(permille)} permille"


def tidy(x, grip):
    """A number of a report: as it is below a grip, in grips where whole grips, in grips^2 where a whole multiple of
    the grip squared (the act as built's P moves by dW x S, grip x count, and its 00 row's by grip^2)."""
    x = int(x)
    if abs(x) < grip:
        return str(x)
    q2, rest2 = carry(x, grip * grip, 0)
    if rest2 == 0:
        return f"{int(q2)} grips^2"
    return in_grips(x, grip)


def lay_name(a00, b00, grip):
    """The lay in words, the 00 slot's counts in grips (rest = 6 grips)."""
    dw = a00 - b00
    w0 = in_grips(6 * grip + a00, grip)
    if dw == 0:
        return f"standing at W = {w0}"
    if dw > 0:
        return f"rising by {in_grips(dw, grip)} a round from W = {w0}"
    return f"falling by {in_grips(-dw, grip)} a round from W = {w0}"
