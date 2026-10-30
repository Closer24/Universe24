"""NOT_CLOSED 29: a passing for monomials of four value legs, on the act (node-live f72067cdf), whole numbers alone.

The held hand k = (k1, k2) under the hat, V = hat (|k|^2 - n)^2, and a tied train x with the tie (tie; x, x, k_r, k_r),
on Mesh-less Node-clocks. Each round reads the window (b, a, a+) at every Node-clock and computes three passings per
train, each from the plan's monomials:
  the act's: X(x, y) = SUM_g (x_g J_g(y) - y_g J_g(x)), S = X(a, b) + X(a+, a) (J the value legs' plan);
  the middle form, at twice the act's scale: each monomial of degree d (its value legs) pushes leg i by the sum over
    the halves S of its value legs that hold i, the other legs of S at x and the rest at y, times 4 / d, so that
    SUM_g x_g M_g(x, y) is the middle symmetric product, the same with x and y swapped: the books close for every
    degree, and a train's own monomials give 0;
  the background form: a monomial joining the held train and one other train books, for both, the held train's own
    motion: S_held = -c P(a) (Q(a+) - Q(b)) and S_other = -S_held, P the other train's legs' product at the now slot and
    Q the held legs' product (here P = x^2 and Q = k_r^2); a train's own monomials give 0; two-leg monomials keep the
    act's form.
For each: the books (rounds whose passings over the trains do not sum to 0), the held train's passing while the hand
stands still, and the oddness under the window's reversal, S(b, a, a+) = -S(a+, a, b).

Usage: python3 -I passing4.py <src of node-live at 575973a20> (byte for byte at f72067cdf too)
"""

import sys

import numpy as np

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.contract import contract, pushes  # noqa: E402
from tensor24.engine.state import Click, Gearing, Layout, Plan, Read, State  # noqa: E402
from tensor24.runner.board import board  # noqa: E402
from tensor24.runner.load import geometry  # noqa: E402

KEY = 5**5
N = KEY * KEY
HAT = 1
W = 2000 * N
TIE = 3
UNIT = -1
NONE_I = np.zeros(0, dtype=np.intp)
NONE_O = np.zeros(0, dtype=object)
UNREAD = Read(NONE_I, NONE_O, NONE_I)
NOPLAN = Plan(NONE_I, NONE_I, NONE_I, NONE_O, NONE_I)
HELD, TIED = (0, 1), (2,)
TRAINS = {"held": HELD, "tied": TIED}


def hat_terms(rows, hat, n):
    terms = []
    for i, a in enumerate(rows):
        terms.append((hat, (a, a, a, a)))
        for b in rows[i + 1:]:
            terms.append((2 * hat, (a, a, b, b)))
        terms.append((-2 * hat * n, (a, a, UNIT, UNIT)))
    return terms


def terms_of(hat):
    return hat_terms(HELD, hat, N) + [(TIE, (2, 2, r, r)) for r in HELD] + [(N, (2, 2, UNIT, UNIT))]


TERMS = terms_of(HAT)


def layout(sites_shape, teeth=W):
    nb = board(sites_shape)
    sites = nb.shape[1]
    spokes, meshes = geometry(nb, 3)
    rows = 3
    ones = np.ones((rows, 1), dtype=object)
    gearing = Gearing(teeth * ones, ones, ones.copy(), ones.copy(), ones.copy())
    click = Click(NONE_I, NONE_I, NONE_O, NONE_I, np.ones((1, 1), dtype=object))
    factor = np.array([f for f, _ in TERMS], dtype=object)
    legs = tuple(np.array([leg[i] for _, leg in TERMS], dtype=np.intp) for i in range(4))
    parts = [nb, spokes, meshes, np.zeros((rows, 3 * sites), dtype=object), gearing, pushes(factor, legs), UNREAD,
             UNREAD, click, NOPLAN]
    parts += [NOPLAN] * (len(Layout._fields) - len(parts))
    return Layout(*parts), sites


def value(row, x):
    return 1 if row == UNIT else x[row]


def act_x(x, y):
    """The act's X per row at one Node-clock: SUM over monomials and their positions on the row."""
    out = [0, 0, 0]
    for f, legs in TERMS:
        for i, g in enumerate(legs):
            if g == UNIT:
                continue
            others_y = others_x = 1
            for j, h in enumerate(legs):
                if j != i:
                    others_y *= value(h, y)
                    others_x *= value(h, x)
            out[g] += -f * (x[g] * others_y - y[g] * others_x)
    return out


def middle_x(x, y):
    """The middle form at twice the act's scale: leg i pushed by (4 / d) SUM over halves S of the value legs holding i."""
    out = [0, 0, 0]
    for f, legs in TERMS:
        vals = [j for j, h in enumerate(legs) if h != UNIT]
        d = len(vals)
        half = carry(d, 2, 0)[0]
        weight = carry(4, d, 0)[0]
        subsets = [[]]
        for j in vals:
            subsets = subsets + [s + [j] for s in subsets]
        halves = [s for s in subsets if len(s) == half]
        for i in vals:
            g = legs[i]
            m_xy = m_yx = 0
            for s in halves:
                if i not in s:
                    continue
                p_xy = p_yx = 1
                for j in vals:
                    if j == i:
                        continue
                    p_xy *= x[legs[j]] if j in s else y[legs[j]]
                    p_yx *= y[legs[j]] if j in s else x[legs[j]]
                m_xy += p_xy
                m_yx += p_yx
            out[g] += -f * weight * (x[g] * m_xy - y[g] * m_yx)
    return out


def trains_of(per_row):
    return {name: sum(per_row[r] for r in rows) for name, rows in TRAINS.items()}


def background_s(b, a, a1):
    """The background form's S per train on the window: the tie books the held train's motion alone; the hat and the
    tied train's own spring are each one train's own, 0."""
    held = 0
    for f, legs in TERMS:
        on_held = [h for h in legs if h in HELD]
        on_tied = [h for h in legs if h in TIED]
        if on_held and on_tied:
            p = 1
            for h in on_tied:
                p *= a[h]
            q_next = q_before = 1
            for h in on_held:
                q_next *= a1[h]
                q_before *= b[h]
            held += -f * p * (q_next - q_before)
    return {"held": held, "tied": -held}


def run(label, a0, b0, rounds, teeth=W):
    lay_, sites = layout((4, 1, 1), teeth)
    s = State(a0.copy(), b0.copy(), np.zeros((3, sites), dtype=object), np.zeros((3, sites), dtype=object),
              np.zeros((1, sites), dtype=object))
    open_books = {"act": 0, "middle": 0, "background": 0}
    held_clicks = {"act": 0, "middle": 0, "background": 0}
    odd = {"act": 0, "middle": 0, "background": 0}
    windows = 0
    worst_norm = 0
    hand_moved = 0
    size_moved = 0
    for _ in range(rounds):
        s1 = step.tick(lay_, s)
        hand_moved += int(bool((s1.a[:2] != s.a[:2]).any()))
        for site in range(sites):
            b = [int(s.b[r, site]) for r in range(3)]
            a = [int(s.a[r, site]) for r in range(3)]
            a1 = [int(s1.a[r, site]) for r in range(3)]
            worst_norm = max(worst_norm, abs(a1[0] * a1[0] + a1[1] * a1[1] - N))
            forms = {
                "act": trains_of([u + v for u, v in zip(act_x(a, b), act_x(a1, a))]),
                "middle": trains_of([u + v for u, v in zip(middle_x(a, b), middle_x(a1, a))]),
                "background": background_s(b, a, a1),
            }
            backs = {
                "act": trains_of([u + v for u, v in zip(act_x(a, a1), act_x(b, a))]),
                "middle": trains_of([u + v for u, v in zip(middle_x(a, a1), middle_x(b, a))]),
                "background": background_s(a1, a, b),
            }
            windows += 1
            size_moved += int(a1[0] * a1[0] + a1[1] * a1[1] != b[0] * b[0] + b[1] * b[1])
            for k in forms:
                open_books[k] += int(sum(forms[k].values()) != 0)
                held_clicks[k] += int(forms[k]["held"] != 0)
                odd[k] += int(all(forms[k][t] == -backs[k][t] for t in TRAINS))
        s = s1
    print(f"  {label}: {windows} windows; |k|^2 - n at most {worst_norm}; rounds in which the hand's counts moved"
          f" {hand_moved} of {rounds}; windows in which |k|^2 at the next count differs from the before {size_moved}")
    for k in ("act", "middle", "background"):
        print(f"    the {k} form: books open in {open_books[k]}; the held train's passing not 0 in {held_clicks[k]};"
              f" odd under the window's reversal in {odd[k]} of {windows}")


print("NOT_CLOSED 29 on the act: the held hand (k1, k2) under the hat, n = 5^10, hat 1, the tie 3 to a tied train x"
      " with its own spring n, teeth 2000 n, four Mesh-less Node-clocks, 400 rounds")
sites = 4
a0 = np.zeros((3, sites), dtype=object)
b0 = np.zeros((3, sites), dtype=object)
for i in range(sites):
    a0[0, i], a0[1, i] = KEY, 0
    b0[0, i], b0[1, i] = KEY, 0
    a0[2, i] = 1000 * (i + 1)
    b0[2, i] = 1000 * (i + 1) - 7 * (i + 1)
run("(A) the hand still at its rest (KEY, 0), the tied train swinging", a0, b0, 400)
a1 = a0.copy()
b1 = b0.copy()
for i in range(sites):
    a1[0, i], a1[1, i] = KEY + 40 * (i + 1), 0
    b1[0, i], b1[1, i] = KEY + 40 * (i + 1), 0
run("(B) the hand's size laid off its rest, swinging, the tied train swinging", a1, b1, 400)
TERMS = terms_of(10**4)
run("(C) a stiff hat, 10^4, teeth 10^6 n: the hand at its rest (KEY, 0), the tied train swinging", a0, b0, 400,
    10**6 * N)
