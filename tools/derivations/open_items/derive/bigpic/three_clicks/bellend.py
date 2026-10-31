"""Bell from the end (the owner's word of 09:33 UTC, "Bell from the end feels closer to nature"; the owner's words to
David of 09:4x to 09:5x, "is it not possible to say that it is from the past and also from the future?"; the owner's
10:10 word to the Boss, "Bell's weight is by how much the board is in the future or in the past, maybe"; David's
meeting's weight, 6541948938). Road (C)'s end form, read exactly in whole numbers and Rule3's carry, by counting every
seed: no draw and no stand-in stream. In (C)'s form (the Boss's ruling on the HALF pair, 6542866096 item 2): the hand
and the fixing end are fixed in advance, and the far click chooses by its own seeds. The hand's dependence on the
fixing end's setting is a laid measure. Under the owner's law of 11:52 UTC ("The connection between two places comes,
for certain, from the start and from the end"), its source is the start and the end fixed together in advance; its
form, road (C)'s seeds' law, is OPEN.

The pair's one hand is born once at the source and carried, unchanged, to its two wings (the pair world, PICTURE.md).
Each wing has its own setting, a direction of the triangle's own plane (the plane across the axis (1, 1, 1) of three
clocks), at 0 or 60 degrees at wing A and 30 or 90 at wing B (twoends.py's settings). The law read here, three parts:
  (i)   the end: one wing's click fixes the hand. Clicking +1 it leaves the hand along its setting, clicking -1 across
        it (the setting turned a quarter in the plane); its own outcome is its own seed's, one count each way;
  (ii)  the board runs that end back to the birth: the pair's one hand, from the source, is the hand that end left;
  (iii) the other wing's click takes the hand's share along its own setting, the square of their overlap,
        (h . s)^2 / ((h . h)(s . s)), the triangle's own squares (1, 3/4, 1/4, 0), read from its own seed over the
        share's whole denominator.
Which end fixes the hand is weighed w_A : w_B, "by how much the board is in the future or in the past"; the readings
are taken at w_A : w_B = 1 : 0, 0 : 1, 1 : 1 and 1 : 2.
Read exactly, per setting pair: the joint counts, the correlation E as a fraction, each wing's +1 share under each far
setting (no signal), CHSH (A0 B30 - A0 B90 + A60 B30 + A60 B90) as a fraction; the pair's curve E against the settings'
angle at every multiple of 30 degrees; and the free-lay control: the hand born free at the source over the plane's six
lattice directions at 30 degrees, and each wing's click taking its share by (iii), with no end fixing it; and the ruled
control, a local act at the bound: the hand born free over the same lines, each wing's click fixed by the hand alone,
+1 where the hand's share along its setting is more than half and -1 where it is less (a share of exactly half, read
+1, is counted and named). No signal in the end law rests on the fixing end's equal split, one count each way.
Usage: python3 -I bellend.py <src>
"""
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

# The triangle's own plane, across the axis (1, 1, 1): its lattice directions at every 30 degrees, from the clocks' own
# differences (clock 0's direction 2 e0 - e1 - e2 at 0, the edge (0, 2) at 30, and so on round the plane).
DIRS = [(2, -1, -1), (1, 0, -1), (1, 1, -2), (0, 1, -1), (-1, 2, -1), (-1, 1, 0)]  # 0, 30, ..., 150 degrees
SETS = {(0, 1): 1, (0, 3): -1, (2, 1): 1, (2, 3): 1}  # CHSH's signs: A at 0 and 60, B at 30 and 90 (twoends.py)
WEIGHTS = [(1, 0), (0, 1), (1, 1), (1, 2)]


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def direction(units):
    """The lattice direction at units x 30 degrees; a half turn is the same line, the hand's sign aside."""
    q, r = carry(units, 6, 0)
    v = DIRS[r]
    return v if carry(q, 2, 0)[1] == 0 else tuple(-x for x in v)


def share(h, s):
    """The hand h's share along the setting s: the square of their overlap, as a whole numerator and denominator."""
    return dot(h, s) * dot(h, s), dot(h, h) * dot(s, s)


def far_click(h, s):
    """The far wing's counts of +1 and -1 over its own seeds 0 .. denominator - 1: +1 where the seed is below the share."""
    n, d = share(h, s)
    return n, d - n


def across(v):
    """The quarter turn in the triangle's plane: the axis (1, 1, 1) crossed with v, a whole vector of the plane."""
    return (v[2] - v[1], v[0] - v[2], v[1] - v[0])


def end_law(a_units, b_units, w_a, w_b):
    """Joint counts N[(oA, oB)] over every seed, under the end law with the ends weighed w_a : w_b."""
    return end_law_on(direction(a_units), direction(b_units), w_a, w_b)


def end_law_on(a, b, w_a, w_b):
    """The end law on two directions of the plane."""
    a_off, b_off = across(a), across(b)
    counts = {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0}
    # every branch is weighed to one common denominator, so no fraction enters: the far seeds' denominator is the same
    # (h . h)(s . s) = 36, 12 or 4 by the lattice's lengths, so each branch's counts are scaled to their product
    branches = []
    for o_fix in (1, -1):
        h = a if o_fix == 1 else a_off
        plus, minus = far_click(h, b)
        branches.append((w_a, "A", o_fix, plus, minus))
        h = b if o_fix == 1 else b_off
        plus, minus = far_click(h, a)
        branches.append((w_b, "B", o_fix, plus, minus))
    total = 1
    for _, _, _, plus, minus in branches:
        total *= plus + minus
    for w, end, o_fix, plus, minus in branches:
        scale, _ = carry(total, plus + minus, 0)
        if end == "A":
            counts[(o_fix, 1)] += w * scale * plus
            counts[(o_fix, -1)] += w * scale * minus
        else:
            counts[(1, o_fix)] += w * scale * plus
            counts[(-1, o_fix)] += w * scale * minus
    return counts


def free_lay(a_units, b_units):
    """Joint counts with the hand born free over the plane's six lattice lines (each with both signs) and each wing
    taking its share by (iii): no end fixes the hand."""
    return free_lay_on(direction(a_units), direction(b_units))


def free_lay_on(a, b):
    """The free lay on two directions of the plane."""
    counts = {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0}
    for k in range(12):
        h = direction(k)
        pa, ma = far_click(h, a)
        pb, mb = far_click(h, b)
        # each line's two wings over their own seeds, scaled to one common denominator for every line
        common = 36 * dot(a, a) * dot(b, b)
        sa, _ = carry(common, pa + ma, 0)
        sb, _ = carry(common, pb + mb, 0)
        counts[(1, 1)] += sa * pa * sb * pb
        counts[(1, -1)] += sa * pa * sb * mb
        counts[(-1, 1)] += sa * ma * sb * pb
        counts[(-1, -1)] += sa * ma * sb * mb
    return counts


def local_act_on(a, b):
    """Joint counts with the hand born free over the plane's six lattice lines (each with both signs) and each wing's
    click fixed by the hand alone: +1 where twice the share's numerator passes its denominator or meets it, else -1."""
    counts = {(1, 1): 0, (1, -1): 0, (-1, 1): 0, (-1, -1): 0}
    ties = 0
    for k in range(12):
        h = direction(k)
        outs = []
        for s in (a, b):
            n, d = share(h, s)
            ties += n + n == d
            outs.append(1 if n + n >= d else -1)
        counts[(outs[0], outs[1])] += 1
    return counts, ties


def local_act(a_units, b_units):
    return local_act_on(direction(a_units), direction(b_units))[0]


def corr(counts):
    """E as a whole numerator over a whole denominator: (same - different) / all."""
    same = counts[(1, 1)] + counts[(-1, -1)]
    diff = counts[(1, -1)] + counts[(-1, 1)]
    return same - diff, same + diff


def per_mille(n, d):
    q, _ = carry(1000 * n + carry(d, 2, 0)[0], d, 0)
    return q


def chsh(rule):
    num, den = 0, 1
    marg = []
    for (ua, ub), sign in SETS.items():
        counts = rule(ua, ub)
        n, d = corr(counts)
        num, den = num * d + sign * n * den, den * d
        marg.append(((ua, ub), counts[(1, 1)] + counts[(1, -1)], counts[(1, 1)] + counts[(-1, 1)], d))
    return num, den, marg


def show(name, rule):
    num, den, marg = chsh(rule)
    print(f"== {name}", flush=True)
    for (ua, ub), sign in SETS.items():
        n, d = corr(rule(ua, ub))
        print(f"   A at {30 * ua}, B at {30 * ub}: E = {n} / {d} = {per_mille(n, d)} per mille", flush=True)
    print(f"   CHSH = {num} / {den} = {per_mille(num, den)} per mille (2 is 2000)", flush=True)
    for (ua, ub), plus_a, plus_b, d in marg:
        print(f"   no signal, A at {30 * ua} and B at {30 * ub}: A's +1 share {per_mille(plus_a, d)} per mille, B's"
              f" {per_mille(plus_b, d)} per mille", flush=True)


for w_a, w_b in WEIGHTS:
    show(f"the end law, the ends weighed A {w_a} : B {w_b}", lambda ua, ub, w_a=w_a, w_b=w_b: end_law(ua, ub, w_a, w_b))
show("the free-lay control: the hand born free over the plane's lines, each wing taking its share", free_lay)
show("the ruled control, a local act at the bound: each wing's click fixed by the hand alone", local_act)
lattice_ties = sum(local_act_on(direction(ua), direction(ub))[1] for ua, ub in SETS)
print(f"   the local act's shares of exactly half at the triangle's settings: {lattice_ties}", flush=True)
Z = (13, 5)  # an Eisenstein integer of the plane, a + b w at 22.4 degrees: its powers turn by the same angle exactly


def eis_mul(p, r):
    """(a + b w)(c + d w) with w^2 = -1 - w."""
    a, b = p
    c, d = r
    return a * c - b * d, a * d + b * c - b * d


def eis_vec(p):
    """a + b w as a vector of the plane: a clock-0 direction and b clock-1 directions, 120 degrees apart."""
    a, b = p
    return (2 * a - b, -a + 2 * b, -a - b)


powers = [(1, 0)]
for _ in range(3):
    powers.append(eis_mul(powers[-1], Z))
vecs = [eis_vec(p) for p in powers]
num, den = 0, 1
num_f, den_f = 0, 1
num_l, den_l, ties_l = 0, 1, 0
for (ka, kb), sign in {(0, 1): 1, (0, 3): -1, (2, 1): 1, (2, 3): 1}.items():
    counts_l, t = local_act_on(vecs[ka], vecs[kb])
    ties_l += t
    n, d = corr(counts_l)
    num_l, den_l = num_l * d + sign * n * den_l, den_l * d
    n, d = corr(end_law_on(vecs[ka], vecs[kb], 1, 1))
    num, den = num * d + sign * n * den, den * d
    n, d = corr(free_lay_on(vecs[ka], vecs[kb]))
    num_f, den_f = num_f * d + sign * n * den_f, den_f * d
turn_num, turn_den = share(vecs[0], vecs[1])
print(f"== Tsirelson on the plane's own lattice: A at z^0 and z^2, B at z and z^3, z = 13 + 5 w (the square of its turn's overlap"
      f" {turn_num} / {turn_den}); the ends weighed 1 : 1", flush=True)
print(f"   the end law: CHSH = {per_mille(num, den)} per mille (Tsirelson's 2 r2 is 2828); the free lay:"
      f" {per_mille(num_f, den_f)} per mille; the local act: {per_mille(num_l, den_l)} per mille ({ties_l} shares of"
      f" exactly half)", flush=True)
print("== the pair's curve, E against the angle between the settings (A at 0, B at the angle; the ends weighed 1 : 1)",
      flush=True)
for k in range(7):
    n, d = corr(end_law(0, k, 1, 1))
    nf, df = corr(free_lay(0, k))
    print(f"   {30 * k} degrees: the end law {per_mille(n, d)} per mille; the free lay {per_mille(nf, df)} per mille",
          flush=True)
print("exit", flush=True)
