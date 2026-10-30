"""Term 11's increment S, the two-round passing, measured on the live act (the Boss's code writer, 2026-10-30;
COUNT5.md item M1, the S row of probe_sameact on the live code): Animate's world, one Node-clock whose neighbours are
itself, the giver and the taker, T1 hands of three components with a re part and an im part, their own springs f
and term 6's vertex g between them, the teeth W at rest, 6,000 rounds; whole numbers and Rule3's carry alone.

Clock: each train's click tooth carries S = X(S) + X(S+), the passing of the state the round reads plus the state it
produces, at the key the nearest odd whole to twice the one-round key, born at (key - 1) div 2; the mirror keeps the
tooth, and the run back is one act on the mirrored state, its quotients negated.
Algebra: X(S) = SUM a J(b) - b J(a) over a hand's gears and X(S+) the same on (a+, a); their sum is odd under the
reversal of the round's window (before, now, next), so -S + k+ = -q key + k returns the tooth; each half alone is not.
Board: one Node-clock, two hands of six gears; the books SUM over the hands of q = 0 every round; the taker's course.
Clicks: the live act's own clicks against S read from outside; the run back by the act on the mirrored state, the
teeth returned and the quotients negated; the fourth text's halves, X(S) and X(S+) alone, carried from outside.

Run: .venv/bin/python tools/derivations/open_items/derive/boss/term11_S/probe.py; its output is probe.txt beside it.
"""

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / "src"))

from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner import load as loading  # noqa: E402

W = 10**20  # the teeth at rest
F, _ = carry(W, 800, 0)  # each hand's own spring: a beat of about 2 pi 20 rounds
A = 10**6  # the giver's swing
ROUNDS = 6000
COMPONENTS = 3  # a T1 hand's components; its two parts make six gears
GIVER, TAKER, HANDS = 0, 1, 2
ROWS = 2 * COMPONENTS * HANDS
PLANES = 1 + 3 + 1  # the readings' planes: the value, the three gradients, the force
UNIT = PLANES * ROWS  # the unit, the readings' last row
SEVENTH = 7  # the one-round key: the giver's wind at the lay in sevenths, times the teeth, made odd


def hand(h):
    """The first gear of hand h's re part and of its im part, six gears a hand, as Animate lays them."""
    return 2 * COMPONENTS * h, 2 * COMPONENTS * h + COMPONENTS


def gears_of(h):
    re, im = hand(h)
    return list(range(re, re + COMPONENTS)) + list(range(im, im + COMPONENTS))


def table():
    """The 24's table of T1 with T1 onto A1, derived from the star: its nonzero entries (entry, j, i)."""
    kinds, tables, _ = main.made(loading.star(3))
    labels = [name.upper() for name in kinds._fields]
    t = tables[(labels.index("T1"), labels.index("T1"), labels.index("A1"))][0]
    return [(int(t[j, i]), int(j), int(i)) for j, i in np.argwhere(t)]


def dot(one, two):
    return [(e, one + j, two + i) for e, j, i in table()]


def potential(g):
    """V = f SUM over the hands of H . H + g (Tre . Gre + Tim . Gim), as whole factors on their legs."""
    own = [(F * e, (j, i)) for h in range(HANDS) for part in hand(h) for e, j, i in dot(part, part)]
    tie = [
        (g * e, (j, i))
        for one, two in zip(hand(TAKER), hand(GIVER), strict=True)
        for e, j, i in dot(one, two)
    ]
    return own + tie


def plan(monomials):
    """J's terms from one potential: each monomial pushes every leg by minus its factor times its other legs, the unit standing for each leg it lacks of three."""
    terms = []
    for factor, legs in monomials:
        for p, leg in enumerate(legs):
            terms.append(((*legs[:p], *legs[p + 1 :], UNIT, UNIT, UNIT)[:3], -factor, leg))
    readings, factor, target = zip(*terms, strict=True)
    return Plan(
        *(np.array(x, dtype=np.intp) for x in zip(*readings, strict=True)),
        np.array(factor, dtype=object),
        np.array(target, dtype=np.intp),
    )


def node(g, key):
    """One Node-clock whose neighbours are itself, so no Mesh pulls it, its push J from the potential; the click's passing one term per row into its hand, at the key."""
    nb = np.zeros((6, 1), dtype=np.intp)
    spokes = loading.star(3)
    meshes, _ = carry(np.arange(6), 2, 0)
    none = np.zeros(0, dtype=np.intp)
    unread = Read(none, none.astype(object), none)
    empty = Plan(none, none, none, none.astype(object), none)
    ones = np.ones((1, 1), dtype=object)
    row = np.arange(ROWS, dtype=np.intp)
    train = np.repeat(np.arange(HANDS, dtype=np.intp), 2 * COMPONENTS)
    click = Click(row, row, np.ones(ROWS, dtype=object), train, key + np.zeros((HANDS, 1), dtype=object))
    return Layout(
        nb,
        spokes,
        meshes[:, None],
        ones.repeat(3, axis=1),
        Gearing(W * ones, 1, 1, 1, 1),
        plan(potential(g)),
        unread,
        unread,
        click,
        empty,
    )


def lay(key):
    """Animate's lay: the giver turning in its re-im plane along the x axis, the taker at rest; every click tooth at its birth."""
    a = np.zeros((ROWS, 1), dtype=object)
    b = a.copy()
    re, im = hand(GIVER)
    a[re, 0], b[re, 0] = A, A
    swing, _ = carry(-A, 20, 0)
    a[im, 0], b[im, 0] = 0, swing
    birth, _ = carry(key - 1, 2, 0)
    return State(a, b, 0 * a, 0 * a, birth + np.zeros((HANDS, 1), dtype=object))


def odd(x):
    """x made odd upward: the nearest odd whole not below it."""
    _, rest = carry(x, 2, 0)
    return x + 1 - rest


def wind(s, s1, gears):
    """D over the gears given: SUM now^2 - next x before."""
    return sum(s.a[i, 0] * s.a[i, 0] - s1.a[i, 0] * s.b[i, 0] for i in gears)


def pushes(layout, x):
    _, j = step.sources(layout, x)
    return j[:, 0]


def wronskian(layout, first, second):
    """Per hand, SUM over its gears of first J(second) - second J(first), the pushes the act's own sources."""
    jf, js = pushes(layout, first), pushes(layout, second)
    f, s = first[:, 0], second[:, 0]
    return tuple(sum(f[i] * js[i] - s[i] * jf[i] for i in gears_of(h)) for h in range(HANDS))


def increment(rule, layout, s, s1):
    """The increment by the rule from the state read, s, and the state produced, s1: B the read state's X(S), I the produced state's X(S+), S their sum."""
    read, produced = wronskian(layout, s.a, s.b), wronskian(layout, s1.a, s.a)
    if rule == "B":
        return read
    if rule == "I":
        return produced
    return tuple(u + v for u, v in zip(read, produced, strict=True))


def same(s, t):
    return all(bool(np.array_equal(x, y)) for x, y in zip(s, t, strict=True))


def carried(rule, layout, states, key):
    """The teeth and quotients a rule carries from outside along the states, forward (the state read, the state produced) and backward (the mirrored states, the window reversed), each with the tooth kept: the forward books, the taker's course, and the run back's returned teeth and negated quotients."""
    birth, _ = carry(key - 1, 2, 0)
    teeth, quotients = [(birth, birth)], []
    for t in range(ROUNDS):
        inc = increment(rule, layout, states[t], states[t + 1])
        out = [carry(x, key, k) for x, k in zip(inc, teeth[-1], strict=True)]
        teeth.append(tuple(k for _, k in out))
        quotients.append(tuple(q for q, _ in out))
    misses = sum(1 for q in quotients if sum(q) != 0)
    course, lo, hi = 0, 0, 0
    for q in quotients:
        course += q[TAKER]
        lo, hi = min(lo, course), max(hi, course)
    k, returned, negated = teeth[-1], 0, 0
    for t in range(ROUNDS, 0, -1):
        m, mt = (
            step.mirror(layout, states[t]),
            step.mirror(layout, states[t - 1]),
        )  # the backward round reads m, makes mt
        out = [carry(x, key, kk) for x, kk in zip(increment(rule, layout, m, mt), k, strict=True)]
        k = tuple(kk for _, kk in out)
        returned += int(k == teeth[t - 1])
        negated += int(all(u == -v for (u, _), v in zip(out, quotients[t - 1], strict=True)))
    return misses, (lo, hi), returned, negated


def report():
    out = []

    def say(line):
        print(line)
        out.append(line)

    say(
        f"Term 11's increment S on the live act: Animate's world, the giver and the taker at one Node-clock, {ROUNDS} rounds"
    )
    g, _ = carry(F, 10, 0)
    probe = node(g, 1)
    s0 = lay(1)
    s1, _ = step.act(probe, s0)
    key1 = odd(W * carry(wind(s0, s1, gears_of(GIVER)), SEVENTH, 0)[0])
    key2 = odd(2 * key1)
    say(
        f"the teeth {W}, the spring {F}, the vertex {g}; the one-round key {key1}, the key for S, the nearest odd whole to twice it, {key2}"
    )
    # 1. the live act forward: its clicks, the books, the taker's course, and S read from outside against the act's own
    layout = node(g, key2)
    states, clicks = [lay(key2)], []
    for _ in range(ROUNDS):
        s, q = step.act(layout, states[-1])
        states.append(s)
        clicks.append(q)
    misses = sum(1 for q in clicks if int(q.sum()) != 0)
    course, lo, hi = 0, 0, 0
    for q in clicks:
        course += int(q[TAKER, 0])
        lo, hi = min(lo, course), max(hi, course)
    alike = 0
    for t in range(ROUNDS):
        inc = increment("S", layout, states[t], states[t + 1])
        own = [carry(x, key2, int(states[t].k[h, 0])) for h, x in enumerate(inc)]
        alike += int(
            all(
                q == int(clicks[t][h, 0]) and k == int(states[t + 1].k[h, 0])
                for h, (q, k) in enumerate(own)
            )
        )
    say(
        f"1. the live act, {ROUNDS} rounds: the books (the hands' quotients summed) miss in {misses} rounds, the taker's course"
        f" {lo}..{hi}; the act's own clicks and teeth equal S read from outside, X(S) + X(S+) carried at the key, in {alike} of {ROUNDS} rounds"
    )
    # 2. the run back by one act on the mirrored state: the gears, the teeth, the quotients
    s, gears, teeth, negated = states[-1], 0, 0, 0
    for t in range(ROUNDS, 0, -1):
        mt, qb = step.act(layout, step.mirror(layout, s))
        s = step.mirror(layout, mt)
        gears += int(same(s[:-1], states[t - 1][:-1]))
        teeth += int(bool(np.array_equal(s.k, states[t - 1].k)))
        negated += int(bool(np.array_equal(qb, -clicks[t - 1])))
    say(
        f"2. the run back, mirror, act, mirror, {ROUNDS} times: the gears return in {gears} of {ROUNDS} rounds, the click teeth in"
        f" {teeth}, the quotients negated in {negated}; the start returned bit for bit: {same(s, states[0])}"
    )
    # 3. the increments carried from outside along the same states: S, and the fourth text's halves alone
    for rule, key, name in (
        ("S", key2, "S = X(S) + X(S+)"),
        ("B", key1, "X(S) alone, the read state's"),
        ("I", key1, "X(S+) alone, the produced state's"),
    ):
        misses, (lo, hi), returned, negated = carried(rule, layout, states, key)
        say(
            f"3. {name} carried from outside at the key {key}: the books miss in {misses} rounds, the taker {lo}..{hi}; the run back"
            f" by one act with the tooth kept returns the teeth in {returned} of {ROUNDS} rounds and negates the quotients in {negated}"
        )
    # 4. the passing's scale: SUM S against SUM X(S) to the taker over the run, in thousandths
    sx = sum(wronskian(layout, states[t].a, states[t].b)[TAKER] for t in range(1, ROUNDS + 1))
    ss = sum(
        sum(increment("S", layout, states[t], states[t + 1])[TAKER] for _ in (0,))
        for t in range(1, ROUNDS)
    )
    ratio, _ = carry(1000 * ss, sx, 0)
    say(
        f"4. the summed passing to the taker over the run, S against the one-round X, in thousandths: {ratio}"
    )
    Path(__file__).with_name("probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")


if __name__ == "__main__":
    report()
