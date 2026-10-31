"""The share rule's spread relation on the settings' plane (DERIVED). Renamed on the THIRD pair's physicist (B1, the
Boss's 6543197467): it is a theorem of the share rule's formula from a known hand, read with no click and no record,
and not the click world's uncertainty, which is OWED (many clicks of one hand along two settings, read from lines
alone). First written on the owner's words of 11:1x UTC to Big Pic ("derive from it the solution to what is still
open").
The share rule is bellend.py's part (iii): a click along a setting s takes the hand h's share (h . s)^2 / ((h . h)(s . s)),
the square of their overlap, over its own seed. Nothing else is used: no end law, no draw, no pair.
Per click, with p the share: the reading E = 2 p - 1 and its spread 1 - E^2 = 4 p (1 - p), a whole fraction.
The relation read: for every hand of the plane and every two settings a, b with c = (a . b)^2 / ((a . a)(b . b)),
the two spreads sum to at least 1 - |2 c - 1|; no hand has both spreads 0 unless c is 0 or 1 (the settings along or
across each other); and the bound is met by some hand on the lattice where one lies there.
Counted exactly over the triangle's own plane: the hands are the Eisenstein integers m + n w with |m|, |n| at most
RANGE (not both 0), the settings the plane's six lattice lines at every 30 degrees and the powers of z = 13 + 5 w.
The scope (the physicist's B2): the same count with each hand lifted off the plane by a common swing c (1, 1, 1),
c = 1 to 3, where no law confines the hand; the relation is scoped to the plane by what that count shows.
Usage: python3 -I spread.py <src> [RANGE, 8 unless given]
"""
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

RANGE = int(sys.argv[2]) if len(sys.argv) > 2 else 8
DIRS = [(2, -1, -1), (1, 0, -1), (1, 1, -2), (0, 1, -1), (-1, 2, -1), (-1, 1, 0)]  # 0, 30, ..., 150 degrees


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def eis_vec(p):
    a, b = p
    return (2 * a - b, -a + 2 * b, -a - b)


def eis_mul(p, r):
    a, b = p
    c, d = r
    return a * c - b * d, a * d + b * c - b * d


def spread(h, s):
    """4 p (1 - p) as a whole numerator over a whole denominator, p the share of h along s."""
    n, d = dot(h, s) * dot(h, s), dot(h, h) * dot(s, s)
    return 4 * n * (d - n), d * d


def bound(a, b):
    """1 - |2 c - 1| as a whole numerator over a whole denominator, c the settings' own share."""
    n, d = dot(a, b) * dot(a, b), dot(a, a) * dot(b, b)
    twice = 2 * n - d
    return d - (twice if twice > 0 else -twice), d


powers = [(1, 0)]
for _ in range(5):
    powers.append(eis_mul(powers[-1], (13, 5)))
settings = DIRS + [eis_vec(p) for p in powers[1:]]
hands = [eis_vec((m, n)) for m in range(-RANGE, RANGE + 1) for n in range(-RANGE, RANGE + 1) if (m, n) != (0, 0)]
held = met = pairs = sharp_both = sharp_both_aligned = 0
lowest = None
for i, a in enumerate(settings):
    for b in settings[i + 1:]:
        bn, bd = bound(a, b)
        pairs += 1
        reached = False
        for h in hands:
            an, ad = spread(h, a)
            cn, cd = spread(h, b)
            total_n, total_d = an * cd + cn * ad, ad * cd
            left, right = total_n * bd, bn * total_d
            held += left >= right
            reached = reached or left == right
            if an == 0 and cn == 0:
                sharp_both += 1
                sharp_both_aligned += bn == 0
            # the smallest margin, in per mille of the bound's own denominator, for the record
            margin, _ = carry(1000 * (left - right), total_d * bd, 0)
            lowest = margin if lowest is None or margin < lowest else lowest
        met += reached
print(f"hands: {len(hands)} Eisenstein integers of the plane, |m|, |n| at most {RANGE}; settings: {len(settings)} (the six"
      f" lattice lines and five powers of z = 13 + 5 w); setting pairs: {pairs}", flush=True)
print(f"the two spreads sum to at least 1 - |2 c - 1| in {held} of {pairs * len(hands)} hand-pair readings; the bound met"
      f" by some hand in {met} of {pairs} pairs; the smallest margin {lowest} per mille", flush=True)
print(f"hands sharp on both settings: {sharp_both}, every one on a pair along or across each other (bound 0):"
      f" {sharp_both == sharp_both_aligned}", flush=True)
for lift in (1, 2, 3):
    broken = readings = 0
    for i, a in enumerate(settings):
        for b in settings[i + 1:]:
            bn, bd = bound(a, b)
            for h0 in hands:
                h = (h0[0] + lift, h0[1] + lift, h0[2] + lift)
                an, ad = spread(h, a)
                cn, cd = spread(h, b)
                readings += 1
                broken += (an * cd + cn * ad) * bd < bn * ad * cd
    print(f"off the plane, every hand lifted by the common swing {lift} (1, 1, 1): the bound breaks in {broken} of"
          f" {readings} readings", flush=True)
for k in range(4):
    bn, bd = bound(DIRS[0], DIRS[k])
    q, _ = carry(1000 * bn, bd, 0)
    print(f"   settings {30 * k} degrees apart: the bound {bn} / {bd} = {q} per mille", flush=True)
print("exit", flush=True)
