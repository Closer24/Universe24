"""Classical interference of two coherent drives into one detector, its energy counted in quanta of the dial (named
so on the HALF pair's verdict, the Boss's 6543885489 item 1; first written on the owner's word of 12:4x UTC to Big Pic:
"make sure that in the clicks one sees the amplitudes of the probabilities seen in nature"). A stand-alone model, a
test's lay, not the engine's board; the act is linear in the counts, apart from its grain, and nothing here reads a
probability: each birth's count is the energy passed, fixed to within one by the dial's phase. Two driver clocks and
one detector clock on the board's own gear form, each with the click world's own spring, the detector joined to each
driver by one two-leg edge at the click world's hands' tie, and no edge between the drivers: two paths into one place.
Each edge carries the board's own passing (tooth.py's form) into its first-click tooth on the edge dial D (the click
world's key). The board reads no tooth, so the board runs once per lay, and every birth of a grid across the dial is
counted on the same passings, each edge by Rule3's carry.
Readings, whole numbers and Rule3's carry only:
  - the detector's clicks: its net landings over the window, summed over its two edges and totalled over the births
    (each lay's expected count of clicks, times the births);
  - the grain, a dead zone at rest: the drivers' swing doubled from the click world's 40, and the first swing at which
    the detector at rest moves at all (by its mechanism near a swing of 1,800: the detector's tooth, its sub-count
    momentum, must reach half a count a round from the drive's own pushes);
  - the phases, at the sweep's top swing: driver 1 alone, driver 2 alone, both, and both with driver 2 mirrored (the
    round's own exact mirror, counts and tooth), driver 2 laid where its own free swing stands k rounds later; the
    interference term (the clicks of both less the clicks of each alone), and the parallelogram law of a square,
    clicks(1 + 2) + clicks(1 - 2) = 2 clicks(1) + 2 clicks(2);
  - the destructive zero: the drivers exact mirrors, so the detector stays at 0 by the round's own symmetry;
  - the share along a setting: a hand h = (m, n) laid in phase on the two drivers (each component at rest at its
    count, a negative one as the mirror of the positive), the detector's two equal ties reading the setting (1, 1),
    and the hand (m, -n) reading (1, -1); the clicks' share along (1, 1) against the share rule's
    (h . s)^2 / ((h . h)(s . s)), and the two settings' clicks summed against twice the hand's own squares' clicks
    (Pythagoras); and the same at an unequal setting, the ties 1 : 2 reading (1, 2) and 2 : 1 with the hand (m, -n)
    reading (2, -1), a test's lay.
Checks by construction, named so: the parallelogram law, Pythagoras on the hands (m, 0) and (0, n), the destructive
zero and the mirrored hand. The share is Malus's law for the energy's projection, laid in the ties: it is not the
share rule read as a chance (condition (a) stays OPEN). The interference term lags the swings' own overlap by about an
eighth of a round, which sets its sign at k = 8. Typed numbers: W (the click world's rest teeth, node-all's loader),
SWING (setting.json's gear 3), SPOKES and SENSES (the star's six spokes and two senses); the drivers' and the
detector's shared beat is a test's lay.
Usage: python3 -I amplitudes.py <node-all src> <the click world's universe.json> [rounds] [births] [doublings]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

ROUNDS = int(sys.argv[3]) if len(sys.argv) > 3 else 24
BIRTHS = int(sys.argv[4]) if len(sys.argv) > 4 else 256
DOUBLINGS = int(sys.argv[5]) if len(sys.argv) > 5 else 12
chosen = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))["chosen"]
S, TIE2, KEY = int(chosen["spring"]), int(chosen["tie"]), int(chosen["key"])
W = 600000000  # the click world's rest teeth (node-all's loader: gearing's rest)
GEAR = W + W
SPOKES, SENSES = 6, 2
HALF, _ = carry(SPOKES, SENSES, 0)  # kappa / two
D = HALF * KEY
EDGES = [(0, 2), (1, 2)]  # driver 1 to the detector, driver 2 to the detector
SWING = 40  # the click world's giver's count (setting.json, gear 3)
GRID = 4  # the hands' grid: |m|, |n| at most 4
TIES = [1, 1]  # each edge's tie in units of the hands' tie: the setting the detector reads


def split(n, d):
    q, r = carry(n + d, d + d, 0)
    return q, r - d


def pushes(a):
    f = [-2 * S * x for x in a]
    for (u, v), m in zip(EDGES, TIES):
        f[u] += -TIE2 * m * a[v]
        f[v] += -TIE2 * m * a[u]
    return f


def round_(a, b, s):
    f = pushes(a)
    a1, s1 = [], []
    for i in range(3):
        q, kept = split(GEAR * (a[i] - b[i]) + GEAR * (a[i] - b[i]) + 4 * f[i] + s[i], GEAR)
        a1.append(a[i] + q)
        s1.append(kept)
    return a1, s1


def lw(p, r, u, v):
    return p[u] * r[v] - p[v] * r[u]


def passings(b, a, a1):
    """Positive into the edge's lower clock (the driver), so a passing into the detector is negative."""
    return [HALF * TIE2 * m * (lw(a, a1, u, v) + lw(b, a, u, v)) for (u, v), m in zip(EDGES, TIES)]


def mirror(x):
    """The round's own exact mirror of one clock: counts negated, the tooth to -1 less itself."""
    return -x[0], -x[1], -1 - x[2]


def at_rest(v):
    return (v, v, 0) if v >= 0 else mirror((-v, -v, 0))


def free_swing(amp, k):
    """A lone clock with the click world's spring, laid at rest at amp, after k rounds of its own swing."""
    a, b, s = amp, amp, 0
    for _ in range(k):
        q, kept = split(GEAR * (a - b) + GEAR * (a - b) + 4 * (-2 * S * a) + s, GEAR)
        a, b, s = a + q, a, kept
    return a, b, s


def lay(one, two):
    """one, two: each driver's (now, before, tooth); the detector laid at rest at 0."""
    return [one[0], two[0], 0], [one[1], two[1], 0], [one[2], two[2], 0]


def clicks(one, two):
    """The detector's net landings over the window, summed over its two edges, totalled over every birth; and the
    detector's widest count over the window."""
    a, b, s = lay(one, two)
    xs, widest = [], 0
    for _ in range(ROUNDS):
        a1, s1 = round_(a, b, s)
        xs.append(passings(b, a, a1))
        a, b, s = a1, a, s1
        widest = max(widest, abs(a[2]))
    total = 0
    for j in range(BIRTHS):
        birth, _ = carry(j * D, BIRTHS, 0)
        k = [birth, birth]
        for x in xs:
            for e in range(2):
                q, k[e] = carry(x[e], D, k[e])
                total -= q
    return total, widest


def permille(n, d, unit=1000):
    return carry(unit * n + carry(d, 2, 0)[0], d, 0)[0] if d else None


def overlap(x, y):
    """The lone swing's energy form, polar (E32 of a lone clock with the spring), on two states (now, before)."""
    a, b, c, d = x[0], x[1], y[0], y[1]
    return 16 * W * W * (a - b) * (c - d) + 16 * W * S * (a * d + b * c)


ZERO = (0, 0, 0)
print(f"two drivers and one detector, each with the click world's spring {S}; the edges at the hands' tie {TIE2};"
      f" W {W};"
      f" the edge dial D {D}; {ROUNDS} rounds; {BIRTHS} births across the dial", flush=True)
print("== the grain: driver 1 alone at rest at the swing, doubled from the click world's 40", flush=True)
for m in range(DOUBLINGS + 1):
    amp = SWING * 2 ** m
    c, widest = clicks((amp, amp, 0), ZERO)
    print(f"   swing {amp}: the detector's widest count {widest}; its clicks {c}", flush=True)
TOP = SWING * 2 ** DOUBLINGS
print(f"== the phases, at the sweep's top swing {TOP} (a test's lay): driver 2 laid where its own free swing stands k"
      f" rounds later", flush=True)
one = (TOP, TOP, 0)
c1, _ = clicks(one, ZERO)
for k in range(12):
    two = free_swing(TOP, k)
    c2, _ = clicks(ZERO, two)
    both, _ = clicks(one, two)
    against, wa = clicks(one, mirror(two))
    term = both - c1 - c2
    gap = both + against - 2 * c1 - 2 * c2
    own = permille(2 * overlap(one, two), overlap(one, one) + overlap(two, two))
    print(f"   k {k}, driver 2 at {two[:2]}: clicks of 1 alone {c1}, of 2 alone {c2}, of both {both}, of both with 2"
          f" mirrored {against} (the detector's widest {wa}); the interference term {term}, {permille(term, c1 + c2)}"
          f" per mille of the two alone, the two swings' own overlap {own} per mille;"
          f" the parallelogram law off by {gap},"
          f" {permille(gap, 2 * c1 + 2 * c2)} per mille", flush=True)
print(f"== the share along a setting, at the swing {TOP} per unit of the hand: every hand (m, n),"
      f" |m|, |n| at most {GRID}", flush=True)
K = {}
for m in range(-GRID, GRID + 1):
    for n in range(-GRID, GRID + 1):
        K[(m, n)], _ = clicks(at_rest(m * TOP), at_rest(n * TOP))
worst_share = worst_sum = 0
for m in range(-GRID, GRID + 1):
    for n in range(-GRID, GRID + 1):
        if (m, n) == (0, 0) or (n < 0) or (n == 0 and m < 0):
            continue
        along, across = K[(m, n)], K[(m, -n)]
        read = permille(along, along + across, 1000000)
        rule = permille((m + n) * (m + n), 2 * (m * m + n * n), 1000000)
        pyth = along + across - 2 * (K[(m, 0)] + K[(0, n)])
        pyth_pm = permille(pyth, 2 * (K[(m, 0)] + K[(0, n)]))
        worst_share = max(worst_share, abs(read - rule))
        worst_sum = max(worst_sum, abs(pyth_pm))
        print(f"   hand ({m}, {n}): clicks along (1, 1) {along}, along (1, -1) {across}; the share along (1, 1) read"
              f" {read} per million, the share rule's {rule}; the two settings' sum less twice the hand's own squares'"
              f" {pyth}, {pyth_pm} per mille", flush=True)
print(f"   the widest share apart from the rule: {worst_share} per million; the widest Pythagoras gap: {worst_sum} per"
      f" mille; the mirrored hand alike: {all(K[(m, n)] == K[(-m, -n)] for (m, n) in K)}", flush=True)
print(f"== an unequal setting, a test's lay: the ties 1 : 2 read (1, 2), and 2 : 1 with the hand (m, -n) read (2, -1)",
      flush=True)
worst_unequal = 0
for m in range(-GRID, GRID + 1):
    for n in range(-GRID, GRID + 1):
        if (m, n) == (0, 0) or (n < 0) or (n == 0 and m < 0):
            continue
        TIES[:] = [1, 2]
        along, _ = clicks(at_rest(m * TOP), at_rest(n * TOP))
        TIES[:] = [2, 1]
        across, _ = clicks(at_rest(m * TOP), at_rest(-n * TOP))
        TIES[:] = [1, 1]
        read = permille(along, along + across, 1000000)
        rule = permille((m + n + n) * (m + n + n), 5 * (m * m + n * n), 1000000)
        worst_unequal = max(worst_unequal, abs(read - rule))
        print(f"   hand ({m}, {n}): along (1, 2) {along}, along (2, -1) {across}; the share along (1, 2) read"
              f" {read} per million, the share rule's {rule}", flush=True)
print(f"   the widest share apart from the rule at the unequal setting: {worst_unequal} per million",
      flush=True)
print("exit", flush=True)
