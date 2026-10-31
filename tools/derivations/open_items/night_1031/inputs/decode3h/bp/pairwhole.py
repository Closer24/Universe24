"""The pair's one hand drawn by the turned tooth, in whole numbers and Rule3's carry alone (Big Pic, #2187 stage 4).

The settings are the equilateral triangle's own: a side (0) and the next side (60 degrees) at one place, a height
(30) and the next height (90) at the other, so every weight is the triangle's own squares, with no root: the height's
square 3 and the half side's 1 over the side's 4 (h^2 = s^2 - (s/2)^2 at s = 2). Two settings 30 degrees apart land
alike with share 3/4, and 90 degrees apart with share 0.

Each place draws its own setting from its own turned teeth; the pair's one hand is its own four teeth, turned
together between carries. The first click carries the pair's teeth at half the dial (its marginal); the second reads
the same hand, pushed back to the first outcome: it lands alike by the triangle's share. Every tooth is born at the
birth (D - 1) div 2 and set apart by the turn itself (place 1 turned once, place 2 twice, the pair three times), so no
lay is picked and no random enters. The dial is odd so the birth is the centre; the share 3/4 of it is the carry's
quotient, so the hand's own value is read exactly from those whole weights.

Usage: python3 -I pairwhole.py <src> [pairs, 400000 unless given] [record.jsonl: the record written, then read alone]
"""

import json
import sys

sys.path.insert(0, sys.argv[1])
from tensor24.algebra.carry import carry  # noqa: E402

PAIRS = int(sys.argv[2]) if len(sys.argv) > 2 else 400000
D = 50811429  # the click world's key, odd, as its universe file holds it
C, _ = carry(D - 1, 2, 0)  # the birth, the dial's centre
N = 4  # the pair's four teeth, as the toys measured four or more turned together with no memory
SIDE2, HALF2 = 4, 1  # the triangle's side squared at s = 2, and its half side squared
HEIGHT2 = SIDE2 - HALF2  # Pythagoras: the height squared, 3


def cen(v):
    _, r = carry(v + C, D, 0)
    return r - C


def turn(u):
    for i in range(1, N):
        u[i] = cen(u[i] + u[i - 1])
    u[0] = cen(u[0] + u[N - 1])


def unturn(u):
    u[0] = cen(u[0] - u[N - 1])
    for i in range(N - 1, 0, -1):
        u[i] = cen(u[i] - u[i - 1])


def born(times):
    u = [0] * N
    for _ in range(times):
        u[0] = cen(u[0] + 1)  # the birth's unit step, then the turn: a whole bijection of the place's index
        turn(u)
    return u


HALF, _ = carry(D - 1, 2, 0)
SAME = {1: carry(HEIGHT2 * D, SIDE2, 0)[0], 3: 0}  # 30 degrees apart: the height's share; 90 apart: none


def click(x, u, i):
    q, r = carry(u[i] + C + x, D, 0)
    u[i] = r - C
    return q


def unclick(x, u, i):
    q, r = carry(u[i] + C - x, D, 0)
    u[i] = r - C
    return -q


alice, bob, pair = born(1), born(2), born(3)
lay = (list(alice), list(bob), list(pair))
rec = []
for t in range(PAIRS):
    turn(alice), turn(bob), turn(pair)
    a = 2 * click(HALF, alice, 0)  # 0 or 2: a side, or the next side
    b = 1 + 2 * click(HALF, bob, 0)  # 1 or 3: a height, or the next height
    sa = 2 * click(HALF, pair, 0) - 1
    same = click(SAME[abs(b - a)], pair, 1)
    sb = sa * (2 * same - 1)
    rec.append((a, b, sa, sb))
for t in range(PAIRS - 1, -1, -1):
    a, b, sa, sb = rec[t]
    assert 2 * unclick(HALF, alice, 0) == a and 1 + 2 * unclick(HALF, bob, 0) == b
    assert unclick(SAME[abs(b - a)], pair, 1) == (1 if sa == sb else 0)
    assert 2 * unclick(HALF, pair, 0) - 1 == sa
    unturn(alice), unturn(bob), unturn(pair)
print(f"dial {D} (odd, the click world's key) | pairs {PAIRS} | the run back to the lay: {(alice, bob, pair) == lay}")
num, cnt = {}, {}
for a, b, sa, sb in rec:
    num[(a, b)] = num.get((a, b), 0) + sa * sb
    cnt[(a, b)] = cnt.get((a, b), 0) + 1
signs = {(0, 1): 1, (0, 3): -1, (2, 1): 1, (2, 3): 1}
# CHSH from the click counts, a whole ratio over the product of the four counts
den = 1
for k in signs:
    den *= cnt[k]
s_num = 0
for k in signs:
    q, _ = carry(den, cnt[k], 0)
    s_num += signs[k] * num[k] * q
s_milli, _ = carry(1000 * s_num, den, 0)
# the hand's own value from its whole weights: E = (2 same - D) / D at each pair of settings
h_num = sum(signs[(a, b)] * (2 * SAME[abs(b - a)] - D) for (a, b) in signs)
h_milli, _ = carry(1000 * h_num, D, 0)
print(f"CHSH from the click counts: {s_milli} per mille | the hand's own value from its whole weights: {h_milli} per mille"
      f" ({h_num} over {D}) | the triangle's own, 5/2: 2500 per mille | the local bound: 2000 per mille")
for k in sorted(cnt):
    e_milli, _ = carry(1000 * num[k], cnt[k], 0)
    print(f"   settings {k}: pairs {cnt[k]}, E {e_milli} per mille")
for far in (1, 3):
    sel = [r for r in rec if r[1] == far]
    p, _ = carry(1000 * sum(1 for r in sel if r[2] == 1), len(sel), 0)
    print(f"   no signal: Alice's +1 share under Bob's setting {far}: {p} per mille ({len(sel)})")
for far in (0, 2):
    sel = [r for r in rec if r[0] == far]
    p, _ = carry(1000 * sum(1 for r in sel if r[3] == 1), len(sel), 0)
    print(f"   no signal: Bob's +1 share under Alice's setting {far}: {p} per mille ({len(sel)})")
# the first click with no draw: the pair's teeth never turned, so each landing is the clock striking
alice, bob, pair = born(1), born(2), born(3)
num2, cnt2 = {}, {}
for t in range(PAIRS):
    turn(alice), turn(bob)
    a = 2 * click(HALF, alice, 0)
    b = 1 + 2 * click(HALF, bob, 0)
    sa = 2 * click(HALF, pair, 0) - 1
    same = click(SAME[abs(b - a)], pair, 1)
    sb = sa * (2 * same - 1)
    num2[(a, b)] = num2.get((a, b), 0) + sa * sb
    cnt2[(a, b)] = cnt2.get((a, b), 0) + 1
den2 = 1
for k in signs:
    den2 *= cnt2[k]
s2 = 0
for k in signs:
    q, _ = carry(den2, cnt2[k], 0)
    s2 += signs[k] * num2[k] * q
s2_milli, _ = carry(1000 * s2, den2, 0)
print(f"the first click, the pair's teeth unturned (no draw): CHSH {s2_milli} per mille")


def lag1(xs):
    """The lag-1 correlation of a run of +-1, in per mille through the carry: its mean taken out in whole numbers."""
    n = len(xs)
    total = sum(xs)
    num = n * sum(xs[i] * xs[i - 1] for i in range(1, n)) - total * total
    den = n * n - total * total
    return carry(1000 * num, den, 0)[0] if den else 0


# what the draw adds, which Bell does not read: Alice's landings in order, the third click against the first
third = [r[2] for r in rec]
first, alice, bob, pair = [], born(1), born(2), born(3)
for t in range(PAIRS):
    turn(alice), turn(bob)
    a = 2 * click(HALF, alice, 0)
    b = 1 + 2 * click(HALF, bob, 0)
    first.append(2 * click(HALF, pair, 0) - 1)
    click(SAME[abs(b - a)], pair, 1)
print(f"Alice's landings in order, lag-1 correlation: the third click {lag1(third)} per mille, the first click {lag1(first)} per mille")


# the record names the pair event (DECODE3b, #2187 6539589459 item 7): one line per landing, each carrying the pair it
# belongs to, A's and B's alike; then CHSH and no signal read back from the record alone, the landings joined by the
# pair they name
if len(sys.argv) > 3:
    out = sys.argv[3]
    with open(out, "w") as f:
        for t, (a, b, sa, sb) in enumerate(rec):
            f.write(json.dumps({"pair": t, "place": "A", "setting": a, "landing": sa}) + "\n")
            f.write(json.dumps({"pair": t, "place": "B", "setting": b, "landing": sb}) + "\n")
    joined = {}
    for line in open(out):
        ln = json.loads(line)
        joined.setdefault(ln["pair"], {})[ln["place"]] = (ln["setting"], ln["landing"])
    unpaired = sum(1 for v in joined.values() if set(v) != {"A", "B"})
    num3, cnt3 = {}, {}
    for v in joined.values():
        (a, sa), (b, sb) = v["A"], v["B"]
        num3[(a, b)] = num3.get((a, b), 0) + sa * sb
        cnt3[(a, b)] = cnt3.get((a, b), 0) + 1
    den3 = 1
    for k in signs:
        den3 *= cnt3[k]
    s3 = 0
    for k in signs:
        q, _ = carry(den3, cnt3[k], 0)
        s3 += signs[k] * num3[k] * q
    s3_milli, _ = carry(1000 * s3, den3, 0)
    print(f"the record ({out}): {2 * len(rec)} landing lines, each naming its pair; pairs joined {len(joined)}, unpaired {unpaired};"
          f" CHSH read from the record alone {s3_milli} per mille")
