"""p11: a hand per quantum, and the record's pair weight (Big Pic, 2026-10-30).

The owner's word (18:4x UTC, to Big Pic, in Hebrew; in translation): "Try a hand per quantum." Each quantum of a family
carries its own hand on the board, moved by the one act, and the family's hand is their sum. The record weighs a pair
of clicks, at places x and y with spin parts s and t, by the 2 x 2 determinant of the two quanta's hands there (a
half-speed family) or by its permanent (a whole-speed family, the control). A half-speed hand at a Node-clock is one
quaternion, read under the family's I as two complex parts, up and down, each a pair of whole numbers. Whole numbers
only; every division is Rule3's carry. Run: python3 .../p11_hand_per_quantum.py (seconds; output beside it).
"""

from qlib import ONE, TWO, carry, report

lines = []
SITES = 24
CENTRE = 12
WIDTH = 6
ROUNDS = 300
AMP = 1000000  # the lay's scale, so that the teeth are small beside the parts
A_W, B_W, C_W = (
    4000000,
    250000,
    4000,
)  # the time weight, the grip per Mesh, the spring: a beat of some 200 rounds


def cmul(p, q):
    return (p[0] * q[0] - p[1] * q[1], p[0] * q[1] + p[1] * q[0])


def cadd(p, q):
    return (p[0] + q[0], p[1] + q[1])


def csub(p, q):
    return (p[0] - q[0], p[1] - q[1])


def size(p):
    return p[0] * p[0] + p[1] * p[1]


def ring(i):
    return carry(i, SITES, 0)[1]


def pascal(m):
    row = [ONE]
    for _ in range(m):
        row = [a + b for a, b in zip([0] + row, row + [0], strict=True)]
    return row


def bump(centre, half):
    """A whole bell on the ring: the binomial row of 2 half, centred."""
    row = pascal(TWO * half)
    f = [0] * SITES
    for k, v in enumerate(row):
        f[ring(centre - half + k)] = v
    return f


def odd_of(f):
    """f(x + 1) - f(x - 1): odd about f's centre when f is even about it."""
    return [f[ring(x + 1)] - f[ring(x - 1)] for x in range(SITES)]


UP = ((ONE, 0), (0, 0))
DOWN = ((0, 0), (ONE, 0))
MIXED = ((ONE, 0), (0, ONE))  # up plus i down


def hand(f, spin):
    """The quantum's hand: its place profile times its spin part, per Node-clock (up, down)."""
    return [
        ((f[x] * spin[0][0], f[x] * spin[0][1]), (f[x] * spin[1][0], f[x] * spin[1][1]))
        for x in range(SITES)
    ]


def value(h, x, s):
    return h[x][s]


def pair(h1, h2, x, s, y, t, sign):
    """The pair amplitude: h1(x, s) h2(y, t) + sign h2(x, s) h1(y, t); sign -1 the determinant, +1 the permanent."""
    a = cmul(value(h1, x, s), value(h2, y, t))
    b = cmul(value(h2, x, s), value(h1, y, t))
    return cadd(a, b) if sign == ONE else csub(a, b)


SLOTS = [(x, s) for x in range(SITES) for s in (0, ONE)]


def weights(h1, h2, sign):
    """The total pair weight over ordered pairs of slots, the weight at coincidence (one place, one spin part), and the
    weight at one place over both spin parts."""
    total = coincide = same_place = 0
    for x, s in SLOTS:
        for y, t in SLOTS:
            w = size(pair(h1, h2, x, s, y, t, sign))
            total += w
            if x == y:
                same_place += w
                if s == t:
                    coincide += w
    return total, coincide, same_place


def det3(m):
    def c3(a, b, c):
        return cmul(cmul(a, b), c)

    t1 = csub(c3(m[0][0], m[1][1], m[2][2]), c3(m[0][0], m[1][2], m[2][1]))
    t2 = csub(c3(m[0][1], m[1][2], m[2][0]), c3(m[0][1], m[1][0], m[2][2]))
    t3 = csub(c3(m[0][2], m[1][0], m[2][1]), c3(m[0][2], m[1][1], m[2][0]))
    return cadd(cadd(t1, t2), t3)


# ---------------------------------------------------------------- the act, one hand at a time
def tick_part(a, b, s):
    """The edge act on one real part of a hand around the ring: N = 2 (D (a - b) + 2 q) + s, split half-open at 2 D,
    the dial D = A + A (a standing clock), q the grips' pull on the Mesh minus the spring."""
    q = [0] * SITES
    for i in range(SITES):
        j = ring(i + 1)
        d = B_W * (a[j] - a[i])
        q[i] += d
        q[j] -= d
        q[i] -= C_W * a[i]
    dial = TWO * A_W
    nxt, tooth = [], []
    for i in range(SITES):
        n_i = TWO * (dial * (a[i] - b[i]) + TWO * q[i]) + s[i]
        v, r = carry(n_i + dial, TWO * dial, 0)
        nxt.append(a[i] + v)
        tooth.append(r - dial)
    return nxt, a, tooth


def parts_of(h):
    """The hand's four real parts (up re, up im, down re, down im), each a row over the ring."""
    return [[h[x][s][k] for x in range(SITES)] for s in (0, ONE) for k in (0, ONE)]


def hand_of(parts):
    return [((parts[0][x], parts[1][x]), (parts[2][x], parts[3][x])) for x in range(SITES)]


def run(h, rounds):
    """Move one hand by the act, laid at rest (before = now), every part with its own tooth."""
    state = [(p, list(p), [0] * SITES) for p in parts_of(h)]
    for _ in range(rounds):
        state = [tick_part(a, b, s) for a, b, s in state]
    return hand_of([a for a, _, _ in state])


f_even = [AMP * v for v in bump(CENTRE, WIDTH)]
f_odd = odd_of(f_even)

# 1. two quanta in one mode
h = hand(f_even, UP)
w_lay = weights(h, h, -ONE)
h_moved = run(h, ROUNDS)
w_moved = weights(h_moved, h_moved, -ONE)
report(
    lines,
    "1. two like half-speed quanta in one mode, each with its own hand: every pair weight is 0, on the lay and after "
    f"{ROUNDS} rounds of the act (the exclusion)",
    w_lay[0] == 0 and w_moved[0] == 0,
)

# 2. one hand per family cannot: the family's hand is the sum, and any weight read from it at two places is symmetric
fam = [(cadd(h[x][0], h[x][0]), cadd(h[x][1], h[x][1])) for x in range(SITES)]
w_one = sum(size(value(fam, x, s)) * size(value(fam, y, t)) for x, s in SLOTS for y, t in SLOTS)
report(
    lines,
    "2. with one hand per family the two quanta are the sum 2 psi, and the product weight read from it at two places is "
    "not 0: one hand cannot exclude",
    w_one > 0,
    f"product weight {w_one}",
)

# 3. two orthogonal modes with one spin: the exchange hole
overlap = sum(a * b for a, b in zip(f_even, f_odd, strict=True))
h1, h2 = hand(f_even, UP), hand(f_odd, UP)
tot, coin, _ = weights(h1, h2, -ONE)
m1, m2 = run(h1, ROUNDS), run(h2, ROUNDS)
tot_m, coin_m, _ = weights(m1, m2, -ONE)
report(
    lines,
    "3. two like quanta of one spin in two orthogonal modes (even and odd about one centre, overlap 0 exactly): the pair "
    "weight is 0 at one place (the exchange hole) and not 0 in all, so the triplet and the Fermi sea fill; the same "
    f"after {ROUNDS} rounds",
    overlap == 0 and coin == 0 and tot > 0 and coin_m == 0 and tot_m > 0,
    f"overlap {overlap}; total pair weight {tot} on the lay, {tot_m} after",
)

# 4. one mode, up and down: two to an orbital, and the pair sits together
tot_ud, _, place_ud = weights(hand(f_even, UP), hand(f_even, DOWN), -ONE)
report(
    lines,
    "4. one mode with up and down: the pair weight is not 0, and not 0 at one place over the two spin parts (two to an "
    "orbital, the pair together)",
    tot_ud > 0 and place_ud > 0,
    f"total {tot_ud}, at one place {place_ud}",
)

# 5. a third quantum in one orbital
hs = [hand(f_even, UP), hand(f_even, DOWN), hand(f_even, MIXED)]
w3 = 0
for a in SLOTS:
    for b in SLOTS:
        for c in SLOTS:
            m = [[value(hk, x, s) for hk in hs] for x, s in (a, b, c)]
            w3 += size(det3(m))
f_shift = [f_even[ring(x - 3)] for x in range(SITES)]
hs_control = [hand(f_even, UP), hand(f_odd, UP), hand(f_shift, UP)]
w3_control = 0
for a in SLOTS:
    for b in SLOTS:
        for c in SLOTS:
            m = [[value(hk, x, s) for hk in hs_control] for x, s in (a, b, c)]
            w3_control += size(det3(m))
report(
    lines,
    "5. a third like quantum in one orbital (up, down, and up plus i down): the 3 x 3 determinant is 0 over every triple "
    "of places and spin parts (two to an orbital); the control, three quanta of one spin in three modes, is not 0",
    w3 == 0 and w3_control > 0,
)

# 6. the light control: the permanent at one place is twice the weight of two told-apart quanta, place by place
ok_bunch = ok_anti = True
for x, s in SLOTS:
    ref = size(cmul(value(h1, x, s), value(h2, x, s))) + size(cmul(value(h2, x, s), value(h1, x, s)))
    ok_bunch &= size(pair(h1, h2, x, s, x, s, ONE)) == TWO * ref
    ok_anti &= size(pair(h1, h2, x, s, x, s, -ONE)) == 0
report(
    lines,
    "6. the control: at one place the permanent (a whole-speed family) weighs twice what two told-apart quanta weigh "
    "(bunching), and the determinant weighs 0 (antibunching), at every place",
    ok_bunch and ok_anti,
)

# 7. the family's hand is the sum of its quanta's hands, to the teeth
s_lay = [(cadd(h1[x][0], h2[x][0]), cadd(h1[x][1], h2[x][1])) for x in range(SITES)]
s_moved = run(s_lay, ROUNDS)
gap = max(
    abs(s_moved[x][s][k] - (m1[x][s][k] + m2[x][s][k]))
    for x in range(SITES)
    for s in (0, ONE)
    for k in (0, ONE)
)
top = max(abs(m1[x][s][k]) + abs(m2[x][s][k]) for x in range(SITES) for s in (0, ONE) for k in (0, ONE))
report(
    lines,
    f"7. the family's one hand moved by the act equals the sum of its quanta's hands moved by the act, to the teeth: after "
    f"{ROUNDS} rounds the largest difference is {gap} counts against a largest part of {top}",
    top > 0 and gap * 1000 < top,
)
lines.append(
    "   so a hand per quantum changes nothing on the board, whose family hand is their sum; it lets the record"
)
lines.append(
    "   weigh a pair of clicks by the difference between the two quanta's hands, at the two clicked places"
)

print("\n".join(lines))
print("ALL PASS" if all(line.startswith(("PASS", "   ")) for line in lines) else "SOME FAILED")
