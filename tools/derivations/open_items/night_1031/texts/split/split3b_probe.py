"""SPLIT3's second probe: among the swap-symmetric palindromes (split3_probe.py (2)), which couple the two takers. A
palindrome whose linear part L splits into two independent 2 x 2 systems, one per taker's pair of teeth, leaves each taker
drawing from two teeth of its own, which Big Pic's memory reading finds remembering (his item 2 (c)). So this probe keeps
the swap-symmetric palindromes whose L joins all four teeth, with no kept direction and both of the swap's parts
hyperbolic, takes the first (fewest blocks, smallest entries), and reads it beside the others:
(i) the swap draw by draw; (ii) the run back by the same act on the mirrored state, the window, the flip, an empty taker,
R2; (iii) the within-lay spread at equal squares (20 stand-in lays of 100,000); (iv) Big Pic's memory reading at high
shares (his stand-in passings 9 and 16 times D div 50; a take after two takes in a row, against independent takes).
Whole numbers; the probe's divisions Rule3's carry; the lay a STAND-IN (a 64-bit carry sequence). argv: the output name."""

import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

out = []
say = out.append
D = 50811429
c, _ = carry(D - 1, 2, 0)
k, _ = carry(D, 1250, 0)
K50, _ = carry(D, 50, 0)
MUL, ADD, MOD = 6364136223846793005, 1442695040888963407, 18446744073709551616


def cen(v):
    _, r = carry(v + c, D, 0)
    return r - c


def lay(seed, n):
    teeth, s = [], seed
    for _ in range(n):
        _, s = carry(s * MUL + ADD, MOD, 0)
        _, t = carry(s, D, 0)
        teeth.append(t - c)
    return teeth, s


def th(num, den):
    return carry(1000 * num, den, 0)[0]


def z2_half(ta, tb):
    return th((ta - tb) * (ta - tb), ta + tb)


def tcarry(u, i, x):
    q, r = carry(u[i] + c + x, D, 0)
    u[i] = r - c
    return q


def step(u, x1, x2, shears):
    u = list(u)
    for i, j, sg in shears:
        u[i] = cen(u[i] + sg * u[j])
    q1 = tcarry(u, 0, x1)
    q2 = tcarry(u, 1, x2)
    for i, j, sg in reversed(shears):
        u[i] = cen(u[i] + sg * u[j])
    return u, (q1, q2)


def swap(u):
    return [u[1], u[0], u[3], u[2]]


def mir(u):
    return [u[0], u[1], -u[2], -u[3]]


def matrix(shears):
    cols = []
    for e in range(4):
        v = [int(i == e) for i in range(4)]
        for i, j, sg in shears:
            v[i] = v[i] + sg * v[j]
        cols.append(v)
    return [[cols[col][row] for col in range(4)] for row in range(4)]


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1) ** col * a[0][col] * det([row[:col] + row[col + 1:] for row in a[1:]]) for col in range(len(a)))


def joined(L):
    """1 where L's nonzero entries join all four teeth (its graph connected), 0 where it splits."""
    reach, grow = {0}, True
    while grow:
        grow = False
        for i in range(4):
            for j in range(4):
                if (L[i][j] != 0 or L[j][i] != 0) and (i in reach) != (j in reach):
                    reach |= {i, j}
                    grow = True
    return int(len(reach) == 4)


BLOCKS = []
for s in (1, -1):
    BLOCKS.append((f"t{'+' if s > 0 else '-'}=g", [(2, 0, s), (3, 1, s)], "t"))
    BLOCKS.append((f"t{'+' if s > 0 else '-'}=g'", [(2, 1, s), (3, 0, s)], "t"))
    BLOCKS.append((f"g{'+' if s > 0 else '-'}=t", [(0, 2, s), (1, 3, s)], "g"))
    BLOCKS.append((f"g{'+' if s > 0 else '-'}=t'", [(0, 3, s), (1, 2, s)], "g"))
eye = [[int(i == j) for j in range(4)] for i in range(4)]
rows = []
for n in (2, 3, 4):
    for seq in product(range(len(BLOCKS)), repeat=n):
        if any(BLOCKS[seq[i]][2] == BLOCKS[seq[i + 1]][2] for i in range(n - 1)) or len({BLOCKS[b][2] for b in seq}) < 2:
            continue
        shears = [s for b in seq for s in BLOCKS[b][1]]
        L = matrix(list(reversed(shears)) + shears)
        d1 = det([[L[i][j] - eye[i][j] for j in range(4)] for i in range(4)])
        d2 = det([[L[i][j] + eye[i][j] for j in range(4)] for i in range(4)])
        ev = [sum(L[i][j] * v[j] for j in range(4)) for i, v in ((0, [1, 1, 0, 0]), (2, [0, 0, 1, 1]))]
        te = sum(L[0][j] * [1, 1, 0, 0][j] for j in range(4)) + sum(L[2][j] * [0, 0, 1, 1][j] for j in range(4))
        to = sum(L[0][j] * [1, -1, 0, 0][j] for j in range(4)) + sum(L[2][j] * [0, 0, 1, -1][j] for j in range(4))
        if d1 == 0 or d2 == 0 or abs(te) <= 2 or abs(to) <= 2:
            continue
        big = max(abs(x) for row in L for x in row)
        rows.append((n, big, seq, shears, L, te, to, joined(L)))
rows.sort(key=lambda z: (z[0], z[1], z[2]))
coupled = [z for z in rows if z[7]]
say(f"swap-symmetric palindromes, 2 to 4 blocks, no kept direction, both swap parts hyperbolic: {len(rows)}; their L"
    f" joining all four teeth: {len(coupled)}; splitting into one pair of teeth per taker: {len(rows) - len(coupled)}")
for z in coupled[:3]:
    say(f"  coupled: {z[0]} blocks {[BLOCKS[b][0] for b in z[2]]}, L {z[4]}, traces even {z[5]} odd {z[6]}")
SPLIT_FORM = rows[0][3]
JOIN = coupled[0][3] if coupled else []
THIRD = [(2, 0, 1), (0, 2, -1), (3, 1, 1), (1, 2, 1), (0, 3, 1)]
say(f"  the split one (SPLIT3's first): {SPLIT_FORM}; the coupled one read below: {JOIN}")

# (i) and (ii) on the coupled one
agree = totals = 0
seed = 31337
for _ in range(10):
    u0, seed = lay(seed, 4)
    u, v = list(u0), swap(list(u0))
    ta = tb = sa = sb = 0
    for _ in range(50000):
        u, (q1, q2) = step(u, 9 * k, 16 * k, JOIN)
        v, (p1, p2) = step(v, 16 * k, 9 * k, JOIN)
        agree += int(v == swap(u) and (p1, p2) == (q2, q1))
        ta, tb, sa, sb = ta + q1, tb + q2, sa + p1, sb + p2
    totals += int((sa, sb) == (tb, ta))
say(f"(i) the coupled one against the swap, 9 k and 16 k, 10 lays of 50,000: agree at {agree} of 500000; totals swapped"
    f" exactly in {totals} of 10")
u0, _ = lay(77, 4)
u, fails, flips, rec = list(u0), 0, 0, []
for _ in range(100000):
    u1, q = step(u, 9 * k, 16 * k, JOIN)
    b, qb = step(mir(u1), -9 * k, -16 * k, JOIN)
    fails += int(mir(b) != u or qb != (-q[0], -q[1]))
    v1, qv = step([-z for z in u], -9 * k, -16 * k, JOIN)
    flips += int(v1 != [-z for z in u1] or qv != (-q[0], -q[1]))
    rec.append(q)
    u = u1
w = list(u)
for _ in range(100000):
    w, _ = step(mir(w), -9 * k, -16 * k, JOIN)
    w = mir(w)
ta, tb = sum(q[0] for q in rec), sum(q[1] for q in rec)
differ, seed = 0, 555
for _ in range(200):
    a, seed = lay(seed, 4)
    b = list(a)
    b[2] = cen(b[2] + 1)
    for _ in range(3000):
        a, qa = step(a, 9 * k, 16 * k, JOIN)
        b, qb = step(b, 9 * k, 16 * k, JOIN)
        if qa != qb:
            differ += 1
            break
e, u = 0, list(u0)
for _ in range(100000):
    u, q = step(u, 9 * k, 0, JOIN)
    e += int(q[1] != 0)
say(f"(ii) 100,000 rounds at 9 k and 16 k: the run back by the same act on the mirrored state fails at {fails}; the window"
    f" exact {int(w == u0)}; the flip fails at {flips}; takes {ta} : {tb}, the first's share {th(ta, ta + tb)} thousandths"
    f" against 360; R2 differs in {differ} of 200; an empty taker clicks {e} times")

# (iii) the within-lay spread, and (iv) the memory reading
for name, shears in (("THIRD's palindrome", THIRD), ("the split symmetric", SPLIT_FORM), ("the coupled symmetric", JOIN)):
    pa = pb = zsum = past = 0
    seed = 12345
    for _ in range(20):
        u, seed = lay(seed, 4)
        t1 = t2 = 0
        for _ in range(100000):
            u, (q1, q2) = step(u, 16 * k, 16 * k, shears)
            t1, t2 = t1 + q1, t2 + q2
        z = z2_half(t1, t2)
        zsum, past, pa, pb = zsum + z, past + int(z > 3841), pa + t1, pb + t2
    u, _ = lay(31, 4)
    A, B = [], []
    for _ in range(400000):
        u, (q1, q2) = step(u, 9 * K50, 16 * K50, shears)
        A.append(q1)
        B.append(q2)
    mem = []
    for S in (A, B):
        n2 = sum(1 for i in range(2, len(S)) if S[i - 1] and S[i - 2])
        h = sum(1 for i in range(2, len(S)) if S[i - 1] and S[i - 2] and S[i])
        ind, _ = carry(n2 * sum(S), len(S), 0)
        mem.append(f"{h} of {n2} (independent {ind})")
    say(f"(iii) {name}, 16 k and 16 k, 20 lays of 100,000: pooled {pa} : {pb}, z^2 {z2_half(pa, pb)}; the lays' z^2"
        f" summed {zsum} against 20,000; past 3,841: {past}")
    say(f"(iv) {name}, 9 and 16 times D div 50, 400,000 rounds: a take after two in a row, the first taker {mem[0]},"
        f" the second {mem[1]}")

HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "split3b_probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
