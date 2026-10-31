"""SPLIT3's probe: the takers' swap against the THIRD deriver's four-tooth palindrome (scratchpad/third/toy6/mirror6.py and
palin4.py, copied unchanged into split/toy6/; mirror6.py's definitions run as written up to its first reading).

Teeth u = [g1, g2, t1, t2]: g1 and g2 the giver edges toward the two takers (carrying, kept by the mirror), t1 and t2 the
hidden teeth (flipped by the mirror). A round: the shears in order, the carries of g1 by x1 and g2 by x2, the shears in
reverse order. The swap of the two takers as the structure moves the teeth: g1 with g2, t1 with t2 (t1 is sheared first
from g1 and t2 from g2), the passings exchanged; and, beside it, the same with the hidden teeth negated.

(1) the THIRD palindrome: its half-turn's matrix H against P H P, P the swap, and the round against the swap draw by draw;
    its shares in frequency;
(2) the palindromes whose shear order the swap maps to itself: blocks of two shears the swap exchanges, which commute
    (each writes one class and reads the other), alternating the classes; searched shortest first, smallest entries first,
    keeping those with no kept direction (det(L - I), det(L + I) not 0) and both of the swap's blocks hyperbolic
    (|trace| > 2 on the even and on the odd part); the first one found run against the swap, the mirror and the readings;
(3) the within-lay spread: 20 stand-in lays of 100,000 rounds at squares 16 and 16, the per-lay z^2 summed, for Big Pic's
    triangle, the THIRD palindrome and the symmetric palindrome.
Whole numbers alone; the probe's own divisions Rule3's carry (tensor24.algebra.carry.carry); the toys' own carries Python's
divmod at a positive dial, which is Rule3's carry. The lay is a STAND-IN (a 64-bit carry sequence); the squares are the
toys' stand-ins."""

import sys
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.joinpath("nl", "src")))
from tensor24.algebra.carry import carry  # noqa: E402

out = []
say = out.append
whole = HERE.joinpath("toy6", "mirror6.py").read_text(encoding="utf-8")
part2 = whole.split("# (2) the four-tooth palindrome")[1].split("u0 = lay(4, 11)")[0]
text = whole.split("u = lay(3, 7)")[0] + "\n# (2) the four-tooth palindrome" + part2  # the definitions alone, no loop
M6: dict = {}
keep = sys.argv
sys.argv = ["mirror6.py", "1"]
exec(compile(text, "mirror6.py", "exec"), M6)  # noqa: S102
sys.argv = keep
D, c, cen, k = M6["D"], M6["c"], M6["cen"], M6["k"]
THIRD = M6["SHEARS"]

MUL, ADD, MOD = 6364136223846793005, 1442695040888963407, 18446744073709551616


def lay(seed: int, n: int) -> tuple[list[int], int]:
    teeth, s = [], seed
    for _ in range(n):
        _, s = carry(s * MUL + ADD, MOD, 0)
        _, t = carry(s, D, 0)
        teeth.append(t - c)
    return teeth, s


def thousandths(num: int, den: int) -> int:
    return carry(1000 * num, den, 0)[0]


def z2_half(ta: int, tb: int) -> int:
    return thousandths((ta - tb) * (ta - tb), ta + tb)


def tooth_carry(u: list[int], i: int, x: int) -> int:
    q, r = carry(u[i] + c + x, D, 0)
    u[i] = r - c
    return q


def step(u: list[int], x1: int, x2: int, shears: list[tuple[int, int, int]]) -> tuple[list[int], tuple[int, int]]:
    u = list(u)
    for i, j, sg in shears:
        u[i] = cen(u[i] + sg * u[j])
    q1 = tooth_carry(u, 0, x1)
    q2 = tooth_carry(u, 1, x2)
    for i, j, sg in reversed(shears):
        u[i] = cen(u[i] + sg * u[j])
    return u, (q1, q2)


def swap_a(u: list[int]) -> list[int]:
    return [u[1], u[0], u[3], u[2]]


def swap_b(u: list[int]) -> list[int]:
    return [u[1], u[0], -u[3], -u[2]]


def mir(u: list[int]) -> list[int]:
    return [u[0], u[1], -u[2], -u[3]]


def matrix(shears: list[tuple[int, int, int]]) -> list[list[int]]:
    cols = []
    for e in range(4):
        v = [int(i == e) for i in range(4)]
        for i, j, sg in shears:
            v[i] = v[i] + sg * v[j]
        cols.append(v)
    return [[cols[col][row] for col in range(4)] for row in range(4)]


def conj(m: list[list[int]], p: list[list[int]]) -> list[list[int]]:
    """P M P^-1 for a signed permutation P (its inverse its transpose)."""
    pm = [[sum(p[i][x] * m[x][j] for x in range(4)) for j in range(4)] for i in range(4)]
    return [[sum(pm[i][x] * p[j][x] for x in range(4)) for j in range(4)] for i in range(4)]


PA = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]]
PB = [[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -1], [0, 0, -1, 0]]
x16 = 16 * k


def swap_test(shears, swap, lays: int, rounds: int, seed: int, xs: tuple[int, int]) -> tuple[int, list[int], int]:
    agree, firsts, totals = 0, [], 0
    for _ in range(lays):
        u0, seed = lay(seed, 4)
        u, v = list(u0), swap(list(u0))
        ta = tb = sa = sb = 0
        first = 0
        for r in range(rounds):
            u, (q1, q2) = step(u, xs[0], xs[1], shears)
            v, (p1, p2) = step(v, xs[1], xs[0], shears)
            ok = v == swap(u) and (p1, p2) == (q2, q1)
            agree += int(ok)
            if not ok and first == 0:
                first = r + 1
            ta, tb, sa, sb = ta + q1, tb + q2, sa + p1, sb + p2
        firsts.append(first)
        totals += int((sa, sb) == (tb, ta))
    return agree, firsts, totals


def spread(shears, lays: int, rounds: int, seed: int, xs: tuple[int, int]) -> tuple[int, int, int, int, list[str]]:
    pa = pb = zsum = past = 0
    rows = []
    for _ in range(lays):
        u, seed = lay(seed, 4)
        ta = tb = 0
        for _ in range(rounds):
            u, (q1, q2) = step(u, xs[0], xs[1], shears)
            ta, tb = ta + q1, tb + q2
        z = z2_half(ta, tb)
        zsum, past, pa, pb = zsum + z, past + int(z > 3841), pa + ta, pb + tb
        rows.append(f"{ta}:{tb}")
    return pa, pb, zsum, past, rows


# (0) the transcription: step() with THIRD's shears is mirror6.py's step4, round by round
u0, _ = lay(5, 4)
u, w, same = list(u0), list(u0), 0
for _ in range(20000):
    u, q = step(u, M6["X1"], M6["X2"], THIRD)
    w, p = M6["step4"](w, M6["X1"], M6["X2"])
    same += int(u == w and q == p)
say(f"(0) step() on THIRD's shears {THIRD} equals mirror6.py's step4 at {same} of 20000 rounds")

# (1) THIRD's palindrome against the swap
H = matrix(THIRD)
say(f"(1) THIRD's half-turn H on (g1, g2, t1, t2): {H}")
for name, p in (("P (t1 with t2)", PA), ("P' (t1 with -t2)", PB)):
    say(f"    {name} H {name}^-1 = {conj(H, p)}; equal to H: {conj(H, p) == H}")
for name, sw in (("P", swap_a), ("P'", swap_b)):
    agree, firsts, totals = swap_test(THIRD, sw, 10, 50000, 31337, (x16, x16))
    say(f"    the round against {name}, squares 16 and 16, 10 lays of 50,000: agree at {agree} of 500000; first round apart"
        f" per lay {firsts}; totals swapped exactly in {totals} of 10")

# (2) the palindromes whose shear order the swap P maps to itself
BLOCKS = []
for s in (1, -1):
    BLOCKS.append((f"t{'+' if s > 0 else '-'}=g (t1 g1, t2 g2)", [(2, 0, s), (3, 1, s)], "t"))
    BLOCKS.append((f"t{'+' if s > 0 else '-'}=g' (t1 g2, t2 g1)", [(2, 1, s), (3, 0, s)], "t"))
    BLOCKS.append((f"g{'+' if s > 0 else '-'}=t (g1 t1, g2 t2)", [(0, 2, s), (1, 3, s)], "g"))
    BLOCKS.append((f"g{'+' if s > 0 else '-'}=t' (g1 t2, g2 t1)", [(0, 3, s), (1, 2, s)], "g"))


def det(a):
    if len(a) == 1:
        return a[0][0]
    return sum((-1) ** col * a[0][col] * det([row[:col] + row[col + 1:] for row in a[1:]]) for col in range(len(a)))


def blocks_of(L):
    """L on the swap's even part (g1 + g2, t1 + t2) and odd part (g1 - g2, t1 - t2), each a 2 x 2 block."""
    def image(v):
        return [sum(L[i][j] * v[j] for j in range(4)) for i in range(4)]
    e1, e2 = image([1, 1, 0, 0]), image([0, 0, 1, 1])
    o1, o2 = image([1, -1, 0, 0]), image([0, 0, 1, -1])
    even = [[e1[0], e2[0]], [e1[2], e2[2]]]
    odd = [[o1[0], o2[0]], [o1[2], o2[2]]]
    return even, odd


found = []
for n in (2, 3, 4):
    for seq in product(range(len(BLOCKS)), repeat=n):
        if any(BLOCKS[seq[i]][2] == BLOCKS[seq[i + 1]][2] for i in range(n - 1)):
            continue
        if len({BLOCKS[b][2] for b in seq}) < 2:
            continue
        shears = [s for b in seq for s in BLOCKS[b][1]]
        L = matrix(list(reversed(shears)) + shears)
        eye = [[int(i == j) for j in range(4)] for i in range(4)]
        d1 = det([[L[i][j] - eye[i][j] for j in range(4)] for i in range(4)])
        d2 = det([[L[i][j] + eye[i][j] for j in range(4)] for i in range(4)])
        even, odd = blocks_of(L)
        te, to = even[0][0] + even[1][1], odd[0][0] + odd[1][1]
        if d1 == 0 or d2 == 0 or abs(te) <= 2 or abs(to) <= 2:
            continue
        big = max(abs(x) for row in L for x in row)
        found.append((n, big, seq, shears, L, te, to, d1, d2, conj(matrix(shears), PA) == matrix(shears)))
found.sort(key=lambda z: (z[0], z[1], z[2]))
say(f"(2) palindromes of 2 to 4 swap-symmetric blocks, classes alternating, no kept direction, both swap blocks"
    f" hyperbolic: {len(found)}; the swap P maps each half-turn to itself at {sum(int(z[9]) for z in found)} of them")
for z in found[:4]:
    names = [BLOCKS[b][0] for b in z[2]]
    say(f"    {z[0]} blocks {names}: L {z[4]}, largest entry {z[1]}, traces even {z[5]} odd {z[6]}, det(L-I) {z[7]}"
        f" det(L+I) {z[8]}")
SYM = found[0][3] if found else []
say(f"    the first, run below: shears {SYM}")
H2 = matrix(SYM)
say(f"    its half-turn H = {H2}; P H P^-1 equal to H: {conj(H2, PA) == H2}; P' H P'^-1 equal to H: {conj(H2, PB) == H2}")
for name, sw in (("P", swap_a), ("P'", swap_b)):
    for xs in ((x16, x16), (9 * k, 16 * k)):
        agree, firsts, totals = swap_test(SYM, sw, 10, 50000, 31337, xs)
        say(f"    the round against {name}, passings {xs[0] // k} k and {xs[1] // k} k: agree at {agree} of 500000;"
            f" first round apart {firsts}; totals swapped exactly in {totals} of 10")
# its run back by the same act on the mirrored state, the flip, R2 and an empty taker
u0, _ = lay(77, 4)
u, fails, flips, down, rec = list(u0), 0, 0, 0, []
for _ in range(100000):
    u1, q = step(u, 9 * k, 16 * k, SYM)
    b, qb = step(mir(u1), -9 * k, -16 * k, SYM)
    fails += int(mir(b) != u or qb != (-q[0], -q[1]))
    v1, qv = step([-z for z in u], -9 * k, -16 * k, SYM)
    flips += int(v1 != [-z for z in u1] or qv != (-q[0], -q[1]))
    down += int(q[0] < 0 or q[1] < 0)
    rec.append(q)
    u = u1
w = list(u)
for _ in range(100000):
    w, _ = step(mir(w), -9 * k, -16 * k, SYM)
    w = mir(w)
ta, tb = sum(q[0] for q in rec), sum(q[1] for q in rec)
say(f"    100,000 rounds at 9 k and 16 k: the one-round run back by the same act on the mirrored state fails at {fails};"
    f" the window back to the lay exact {int(w == u0)}; the flip fails at {flips}; downward crossings {down}; takes"
    f" {ta} : {tb}, the first's share {thousandths(ta, ta + tb)} thousandths against 360")
differ, seed = 0, 555
for _ in range(200):
    a, seed = lay(seed, 4)
    b = list(a)
    b[2] = cen(b[2] + 1)
    for _ in range(3000):
        a, qa = step(a, 9 * k, 16 * k, SYM)
        b, qb = step(b, 9 * k, 16 * k, SYM)
        if qa != qb:
            differ += 1
            break
e, u = 0, list(u0)
for _ in range(100000):
    u, q = step(u, 9 * k, 0, SYM)
    e += int(q[1] != 0)
say(f"    R2, two lays one unit apart in t1, the same click past: a later click differs in {differ} of 200; an empty taker"
    f" clicks {e} times in 100,000 rounds")

# (3) the within-lay spread at equal squares
TRI = None
for name, shears in (("THIRD's palindrome", THIRD), ("the symmetric palindrome", SYM)):
    pa, pb, zsum, past, rows = spread(shears, 20, 100000, 12345, (x16, x16))
    say(f"(3) {name}, squares 16 and 16, 20 lays of 100,000: pooled {pa} : {pb}, z^2 {z2_half(pa, pb)} thousandths;"
        f" the lays' z^2 summed {zsum} thousandths against chance's 20,000; past 3,841: {past}; per lay {' '.join(rows)}")
T3: dict = {}
ttext = HERE.joinpath("bp3", "turnteeth.py").read_text(encoding="utf-8").split("rng = random.Random(31)")[0]
sys.argv = ["turnteeth.py", "50811429", "1", "1", "1250"]
exec(compile(ttext, "turnteeth.py", "exec"), T3)  # noqa: S102
sys.argv = keep
pa = pb = zsum = past = 0
seed = 12345
for _ in range(20):
    teeth, seed = lay(seed, 3)
    ta = tb = 0
    for _ in range(100000):
        teeth, q1, q2 = T3["step"](teeth, x16, x16, 1)
        ta, tb = ta + q1, tb + q2
    z = z2_half(ta, tb)
    zsum, past, pa, pb = zsum + z, past + int(z > 3841), pa + ta, pb + tb
say(f"(3) Big Pic's triangle (turnteeth.py), the same lays' sequence: pooled {pa} : {pb}, z^2 {z2_half(pa, pb)}; the lays'"
    f" z^2 summed {zsum} thousandths against 20,000; past 3,841: {past}")

HERE.joinpath(sys.argv[1] if len(sys.argv) > 1 else "split3_probe.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
