"""The third click as the triangle's one tooth (Big Pic's bench; the owner's answers of 09:30 UTC: two new numbers per
triangle are not approved, "there is surely a mathematical miracle here that solves this cleanly", and "check what an
equilateral triangle gives"; the owner's 09:35 word: derive the open items from ALG2's coupling complex).

Three clocks at one W, each with the click world's spring, each pair joined by one edge of the hands' tie (two legs,
f x_u x_v): the equilateral triangle of two-leg edges, stepped by the engine's gear form with no dial and no order
(miracle/equil.py). Whole numbers; Rule3's carry the one division.

On each edge e = (u, v), u < v, the act's own side passing into u (node-all's step.passing and crossing, the form
P(a, b) + P(a+, a)), in the sides' units:
    x_e = half_kappa f (l_uv(a, a+) + l_uv(b, a)),  l_uv(p, r) = p_u r_v - p_v r_u.
The triangle's boundary C on its sorted clocks: (0, 1) and (1, 2) with +1, (0, 2) with -1; G = C^T C = 3. Its
circulating passing y = C^T x. Two forms of the record:
  - the first click: each edge carries x_e at the edge dial D (node-all's click key) with its own tooth;
  - the triangle's one tooth: each edge carries G x_e - c_e y at G D with its own tooth; the triangle's one tooth tau
    carries y at G D; each quantum w that tau lands is booked c_e w on the triangle's edges (THIRD7's member with its
    twin and turn left out: tri7.Member with turned=False).
Every tooth is born at the middle, (dial - 1) div senses.

DERIVED (the probe checks each identity at every round):
  - y = half_kappa f (L(a, a+) + L(b, a)), L(p, r) = SUM over the cycle (0 1 2) of p_i r_(i+1) - p_(i+1) r_i: the
    circulation is the triangle's discrete angular momentum about its axis (1, 1, 1), read at the round's two windows;
  - 2 D (L(a, a+) - L(b, a)) = 4 a^T J F(a) + a^T J (s - s'), D the gear's dial 2 W: the force's torque and the teeth's torque. The two-leg
    equilateral potential is turned into itself about the axis, so its torque is 0 at every state (Noether's charge of
    the triangle's turn): L moves by the teeth's torque alone;
  - the lines: each clock's net passing is (kappa / two) f times the triple's angular momentum across the axis, so the
    lines read its two components across the axis and y the one along it (the Hodge split of the edges' flows);
  - the edges' teeth's circulation c . f stays at its birth's value mod G D, since c . (G x - c y) = 0: one edge tooth
    is the other two's double, and tau takes its place (ALG3's count), so the third click costs no number beyond the
    first click's three;
  - the books per clock in the clicks: half_kappa (E_u' - E_u - share_u) = 8 W SUM_e B_ue (dial q_e + k_e' - k_e), E_u
    the clock's own energy with half of each of its edges' (E32's terms), on either form; under the triangle's tooth the
    landings drop out of every clock's books (B C = 0), and tau's books are tau' + G D w = tau + y.
Readings, 5,000 rounds unless given: the identities; L's drift; the landings (their count against SUM y / (G D), and the
balance of the landing word over every window up to 64 rounds); the record's circulation c . q against 3 W on both
forms; the run back from the end state alone (board, edge teeth, tau); the triangle's three turns and three flips (S_3),
with an odd one reading each edge's tooth from its other end (dial - 1 - k) and tau as G D - 1 - tau.
The owner's guiding line (10:37 UTC): one start, several births of the triangle's tooth; the board's end and every
line are one, the landings differ, and each run back reaches the same start.
Pauli's exclusion in the third click: L = det(1, b, a) is odd under the exchange of any two clocks (the 2-cell's
orientation, the sign character) and 0 when two clocks share their state; laid so, the state stays its own swap, and
the triangle lands no third click.
A control: the equilateral triangle of four-leg edges (c x_u^2 x_v^2, the click world's tie factor) under the present
act, whose torque is not 0.
Usage: python3 -I tooth.py <node-all src> <the click world's universe.json> [rounds]
"""
import itertools
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
chosen = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["chosen"]
S, TIE2, KEY = int(chosen["spring"]), int(chosen["tie"]), int(chosen["key"])
W = 600000000  # the click world's rest teeth (node-all's loader: gearing's rest, one value on every row)
TIE4 = 60000  # the click world's tie factor at hold 1 (miracle/equil.py)
SPOKES, SENSES = 6, 2  # the star of three axes: six Spokes, two senses
HALF, _ = carry(SPOKES, SENSES, 0)  # kappa / two
D = HALF * KEY  # the edge dial: node-all's click key, 152,434,287 on the click world
GEAR = W + W
EDGES = [(0, 1), (1, 2), (0, 2)]
C = [1, 1, -1]  # the triangle's boundary on its sorted edges
NEXT, NEXT2 = [1, 2, 0], [2, 0, 1]  # the cycle (0 1 2) once and twice
G = sum(c * c for c in C)
GD = G * D


def born(dial):
    return carry(dial - 1, SENSES, 0)[0]


def split(n, d):
    q, r = carry(n + d, d + d, 0)
    return q, r - d


def push(a, four):
    """The pushes at the now slot: the own spring, and each edge's (two legs f x_u x_v, or four legs c x_u^2 x_v^2)."""
    out = []
    for i in range(3):
        f = -2 * S * a[i]
        for j in range(3):
            if j != i:
                f += -2 * TIE4 * a[i] * a[j] * a[j] if four else -TIE2 * a[j]
        out.append(f)
    return out


def round_(a, b, s, four=False):
    f = push(a, four)
    a1, s1 = [], []
    for i in range(3):
        q, kept = split(GEAR * (a[i] - b[i]) + GEAR * (a[i] - b[i]) + 4 * f[i] + s[i], GEAR)
        a1.append(a[i] + q)
        s1.append(kept)
    return a1, s1, f


def lw(p, r, u, v):
    return p[u] * r[v] - p[v] * r[u]


def big_l(p, r):
    return lw(p, r, 0, 1) + lw(p, r, 1, 2) + lw(p, r, 2, 0)


def jdot(p, r):
    """p^T J r, J the cycle's turn: the same form as L."""
    return big_l(p, r)


def passings(b, a, a1):
    return [HALF * TIE2 * (lw(a, a1, u, v) + lw(b, a, u, v)) for u, v in EDGES]


def energy(a, b):
    """Each clock's own energy at the edge (b, a), with half of each of its edges' (E32's terms)."""
    out = []
    for i in range(3):
        e = 16 * W * W * (a[i] - b[i]) * (a[i] - b[i]) + 32 * W * S * a[i] * b[i]
        for j in range(3):
            if j != i:
                e += 8 * W * TIE2 * (b[i] * a[j] + a[i] * b[j])
        out.append(e)
    return out


def ends(i):
    """B: each edge's passing goes into its lower clock and out of its upper."""
    return [1 if e[0] == i else -1 if e[1] == i else 0 for e in EDGES]


def record_round(x, k, f, tau, member):
    """One round of the record's teeth for the passings x; returns the sides q and the landing w."""
    if not member:
        q = []
        for e in range(3):
            qe, k[e] = carry(x[e], D, k[e])
            q.append(qe)
        return q, 0
    y = sum(c * xe for c, xe in zip(C, x))
    q = []
    for e in range(3):
        qe, f[e] = carry(G * x[e] - C[e] * y, GD, f[e])
        q.append(qe)
    w, tau[0] = carry(y, GD, tau[0])
    return [qe + c * w for qe, c in zip(q, C)], w


def run(a, b, s, k, f, tau, rounds, member, log=None):
    a, b, s, k, f, tau = list(a), list(b), list(s), list(k), list(f), list(tau)
    for _ in range(rounds):
        a1, s1, _ = round_(a, b, s)
        q, w = record_round(passings(b, a, a1), k, f, tau, member)
        if log is not None:
            log.append((q, w))
        a, b, s = a1, a, s1
    return a, b, s, k, f, tau


def mirror(a, b, s):
    return list(b), list(a), [-1 - v for v in s]


def read(name, lay_a, lay_b):
    a, b, s = list(lay_a), list(lay_b), [0, 0, 0]
    k, f, tau = [born(D)] * 3, [born(GD)] * 3, [born(GD)]
    start = (list(a), list(b), list(s), list(k), list(f), list(tau))
    l0 = big_l(b, a)
    ids = {"y": 0, "lines": 0, "torque": 0, "zero force torque": 0, "books first": 0, "books tooth": 0, "tau": 0,
           "edge circulation kept": 0}
    c_f0 = carry(sum(c * v for c, v in zip(C, f)), GD, 0)[1]
    silent, line_max, y_min, y_max = 0, 0, None, None
    landings, sum_y, cq_first, cq_tooth, word, lmax, lmin = 0, 0, [], [], [], l0, l0
    for _ in range(ROUNDS):
        a1, s1, force = round_(a, b, s)
        x = passings(b, a, a1)
        y = sum(c * xe for c, xe in zip(C, x))
        ids["y"] += y == HALF * TIE2 * (big_l(a, a1) + big_l(b, a))
        lam = [lw(a, a1, 1, 2) + lw(b, a, 1, 2), lw(a, a1, 2, 0) + lw(b, a, 2, 0), lw(a, a1, 0, 1) + lw(b, a, 0, 1)]
        lines = [sum(ends(i)[e] * x[e] for e in range(3)) for i in range(3)]
        ids["lines"] += lines == [HALF * TIE2 * (lam[NEXT2[i]] - lam[NEXT[i]]) for i in range(3)]
        silent += lines == [0, 0, 0]
        line_max = max([line_max] + [abs(v) for v in lines])
        y_min = y if y_min is None else min(y_min, y)
        y_max = y if y_max is None else max(y_max, y)
        ids["torque"] += 2 * GEAR * (big_l(a, a1) - big_l(b, a)) == 4 * jdot(a, force) + jdot(a, [p - r for p, r in zip(s, s1)])
        ids["zero force torque"] += jdot(a, force) == 0
        e0, e1 = energy(a, b), energy(a1, a)
        share = [4 * W * (a1[i] - b[i]) * (s[i] - s1[i]) for i in range(3)]
        k0, f0, t0 = list(k), list(f), tau[0]
        q1, _ = record_round(x, k, f, tau, False)
        qm, w = record_round(x, k, f, tau, True)
        for i in range(3):
            bi = ends(i)
            first = sum(bi[e] * (D * q1[e] + k[e] - k0[e]) for e in range(3))
            tooth = sum(bi[e] * (GD * qm[e] + f[e] - f0[e]) for e in range(3))
            ids["books first"] += HALF * (e1[i] - e0[i] - share[i]) == 8 * W * first
            ids["books tooth"] += G * HALF * (e1[i] - e0[i] - share[i]) == 8 * W * tooth
        ids["tau"] += tau[0] + GD * w == t0 + y
        ids["edge circulation kept"] += carry(sum(c * v for c, v in zip(C, f)), GD, 0)[1] == c_f0
        landings += w
        sum_y += y
        word.append(w)
        cq_first.append(sum(c * qe for c, qe in zip(C, q1)))
        cq_tooth.append(sum(c * qe for c, qe in zip(C, qm)))
        a, b, s = a1, a, s1
        lmax, lmin = max(lmax, big_l(b, a)), min(lmin, big_l(b, a))
    print(f"== {name}: the lay {lay_a} now, {lay_b} before; {ROUNDS} rounds", flush=True)
    print("   identities held in rounds (of " + str(ROUNDS) + "; the books of " + str(3 * ROUNDS) + " clock-rounds): "
          + ", ".join(f"{key} {val}" for key, val in ids.items()), flush=True)
    print(f"   L (the angular momentum about the axis) at the lay {l0}, at the end {big_l(b, a)}, its range over the run"
          f" [{lmin}, {lmax}]", flush=True)
    print(f"   the circulation y per round in [{y_min}, {y_max}]; the lines (each clock's net passing): all three 0 in"
          f" {silent} rounds, the largest {line_max}", flush=True)
    whole, rest = carry(sum_y + born(GD), GD, 0)
    print(f"   the triangle's landings: {landings} (SUM y over G D, from tau's birth: {whole}); the landing values"
          f" {sorted(set(word))}; rounds with a landing {sum(1 for v in word if v)}", flush=True)
    spread = 0
    for m in range(1, 65):
        sums = [sum(word[t:t + m]) for t in range(0, ROUNDS - m + 1)]
        spread = max(spread, max(sums) - min(sums))
    print(f"   the landing word's balance: the largest spread of the landings over equal windows up to 64 rounds: {spread}",
          flush=True)
    for label, cq in (("the first click's", cq_first), ("the triangle's tooth's", cq_tooth)):
        run_sum, worst = 0, 0
        for t in range(ROUNDS):
            run_sum += cq[t]
            worst = max(worst, abs(run_sum - 3 * sum(word[:t + 1])))
        vals = sorted(set(cq))
        print(f"   {label} record: c . q per round takes {len(vals)} values in [{vals[0]}, {vals[-1]}]; its running sum"
              f" stays within {worst} of 3 W", flush=True)
    for member in (False, True):
        log = []
        end = run(*start, ROUNDS, member, log)
        ma, mb, ms = mirror(end[0], end[1], end[2])
        back_log = []
        back = run(ma, mb, ms, end[3], end[4], end[5], ROUNDS, member, back_log)
        ba, bb, bs = mirror(back[0], back[1], back[2])
        same = (ba, bb, bs, back[3], back[4], back[5]) == start
        neg = [([-v for v in q], -w) for q, w in reversed(log)] == back_log
        print(f"   the run back ({'the triangle tooth' if member else 'the first click'}): the start reached {same};"
              f" the sides and landings back negated and reversed {neg}", flush=True)
    alike = 0
    for p in itertools.permutations(range(3)):
        sign = 1 if carry(sum(1 for i in range(3) for j in range(i + 1, 3) if p[i] > p[j]), 2, 0)[1] == 0 else -1
        moved_a, moved_b = [lay_a[p[i]] for i in range(3)], [lay_b[p[i]] for i in range(3)]
        log_u, log_v = [], []
        u = run(moved_a, moved_b, [0, 0, 0], [born(D)] * 3, [born(GD)] * 3, [born(GD)], 200, True, log_u)
        v = run(lay_a, lay_b, [0, 0, 0], [born(D)] * 3, [born(GD)] * 3, [born(GD)], 200, True, log_v)
        ok = all(u[0][i] == v[0][p[i]] and u[1][i] == v[1][p[i]] for i in range(3))
        for e, (i, j) in enumerate(EDGES):  # edge e of the moved world is the old edge (p[i], p[j])
            oi, oj = sorted((p[i], p[j]))
            old = EDGES.index((oi, oj))
            flip = (p[i], p[j]) != (oi, oj)
            ok = ok and u[4][e] == ((GD - 1 - v[4][old]) if flip else v[4][old])
            for (qu, wu), (qv, wv) in zip(log_u, log_v):
                ok = ok and qu[e] == (-qv[old] if flip else qv[old])
        ok = ok and u[5][0] == (v[5][0] if sign > 0 else GD - 1 - v[5][0])
        ok = ok and all(wu == sign * wv for (_, wu), (_, wv) in zip(log_u, log_v))
        alike += ok
    print(f"   the triangle's turns and flips: the round, its edge teeth, its sides, tau and the landings turned alike in"
          f" {alike} of 6 (200 rounds each)", flush=True)


def paths(name, lay_a, lay_b):
    """The owner's guiding line of 10:37 UTC: one start, several births of the triangle's tooth (the member's choice,
    in its births by road (C)), read for the click paths apart, the lines one, the board's end one, and each run back
    from its own end to the same start."""
    third, _ = carry(GD, 3, 0)
    births = [born(GD), 0, third, third + third]
    start = (list(lay_a), list(lay_b), [0, 0, 0])
    runs = []
    for b0 in births:
        log = []
        end = run(*start, [born(D)] * 3, [born(GD)] * 3, [b0], ROUNDS, True, log)
        lines = [[sum(ends(i)[e] * q[e] for e in range(3)) for i in range(3)] for q, _ in log]
        runs.append((b0, end, log, lines))
    board_one = all(r[1][:3] == runs[0][1][:3] for r in runs)
    lines_one = all(r[3] == runs[0][3] for r in runs)
    apart = []
    for r in runs[1:]:
        apart.append(sum(1 for (_, w0), (_, w1) in zip(runs[0][2], r[2]) if w0 != w1))
    backs = 0
    for b0, end, _, _ in runs:
        ma, mb, ms = mirror(end[0], end[1], end[2])
        back = run(ma, mb, ms, end[3], end[4], end[5], ROUNDS, True)
        ba, bb, bs = mirror(back[0], back[1], back[2])
        backs += (ba, bb, bs, back[5]) == (start[0], start[1], start[2], [b0])
    print(f"== {name}: the lay {lay_a} now, {lay_b} before; {ROUNDS} rounds; tau born at {births}", flush=True)
    print(f"   the board's end one for every birth: {board_one}; every clock's line one at every round: {lines_one}; the"
          f" landings apart from the first birth's in {apart} rounds; each run back from its own end to the same start"
          f" and its own birth: {backs} of {len(runs)}", flush=True)


def exclusion(name, lay_a, lay_b):
    """Two clocks laid in one state: the law is turned into itself by their exchange, so the state stays its own swap,
    and the triangle's charge L(b, a) = det(1, b, a) has two equal columns."""
    a, b, s = list(lay_a), list(lay_b), [0, 0, 0]
    k, f, tau = [born(D)] * 3, [born(GD)] * 3, [born(GD)]
    same, zero_l, zero_y, landings = 0, 0, 0, 0
    for _ in range(ROUNDS):
        a1, s1, _ = round_(a, b, s)
        x = passings(b, a, a1)
        y = sum(c * xe for c, xe in zip(C, x))
        _, w = record_round(x, k, f, tau, True)
        same += a1[0] == a1[1] and s1[0] == s1[1]
        zero_l += big_l(a, a1) == 0
        zero_y += y == 0
        landings += abs(w)
        a, b, s = a1, a, s1
    print(f"== {name}: the lay {lay_a} now, {lay_b} before; {ROUNDS} rounds", flush=True)
    print(f"   clocks 0 and 1 in one state (counts and teeth) in {same} rounds; L = 0 in {zero_l}; y = 0 in {zero_y};"
          f" the triangle's landings, counted whole: {landings}", flush=True)


def control(name, lay_a, lay_b):
    a, b, s = list(lay_a), list(lay_b), [0, 0, 0]
    l0, held, zero, lmax, lmin, done, past = big_l(b, a), 0, 0, big_l(b, a), big_l(b, a), 0, None
    for n in range(ROUNDS):
        a1, s1, force = round_(a, b, s, four=True)
        held += 2 * GEAR * (big_l(a, a1) - big_l(b, a)) == 4 * jdot(a, force) + jdot(a, [p - r for p, r in zip(s, s1)])
        zero += jdot(a, force) == 0
        a, b, s = a1, a, s1
        lmax, lmin = max(lmax, big_l(b, a)), min(lmin, big_l(b, a))
        done = n + 1
        if max(abs(v) for v in a).bit_length() > 64:
            past = done
            break
    print(f"== {name}: the lay {lay_a} now, {lay_b} before; {done} rounds"
          + (f" (a count passed 64 bits at round {past}, where the reading stops)" if past else ""), flush=True)
    print(f"   the torque identity held in {held} of {done} rounds; the force's torque 0 in {zero}; L at the lay {l0},"
          f" at the end {big_l(b, a)}, its range [{lmin}, {lmax}]", flush=True)


print(f"three clocks at W {W}, spring {S}, two-leg tie {TIE2}, four-leg tie {TIE4}; the edge dial D {D} (kappa / two"
      f" {HALF} times the key {KEY}), the triangle's G {G}, its dial G D {GD}", flush=True)
TURNING = ([40, -20, -20], [20, -40, 20])  # a test's lay: two lattice points of the triangle's own plane, 60 degrees apart
AT_REST = ([40, 20, 1], [40, 20, 1])  # miracle/equil.py's MOVING lay, at rest
read("the equilateral triangle of two-leg edges, laid turning", *TURNING)
read("the equilateral triangle of two-leg edges, laid at rest", *AT_REST)
read("the same, laid turning the other way (the lay's two slots swapped)", TURNING[1], TURNING[0])
read("the same, laid turning at ten times the counts", [10 * v for v in TURNING[0]], [10 * v for v in TURNING[1]])
read("the same, laid at rest at ten times the counts", [10 * v for v in AT_REST[0]], [10 * v for v in AT_REST[1]])
paths("one start, four births of the triangle's tooth (the owner's guiding line: the clicks choose the path, the board"
      " is fixed)", *TURNING)
exclusion("two clocks in one state (Pauli's exclusion in the third click)", [40, 40, 7], [25, 25, 3])
control("the control: the equilateral triangle of four-leg edges under the present act, laid turning", *TURNING)
print("exit", flush=True)
