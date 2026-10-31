"""THIRD8's arithmetic on the member's pair (a reading, never an act). Whole numbers only; every division and every
reduction is Rule3's carry. Nothing typed: the click world's structure is loaded (tri7.load_world), C and G = C^T C are
read from its edge set (tri7.edge_set, tri7.Member), the dial from the star and the world's key, and L from the
Member's own shears. argv: src, the frozen folder (for the toy's counts, read from its outputs).

1. L read from tri7.Member's shears (the second half, then the next round's first half, on the centred basis); trace,
   det, det(L - I), det(L + I); Cayley-Hamilton L^2 = tr L - I.
2. The triangle's dial G D factored by trial division; L's order modulo each prime power; N = their lcm; L^N = I and
   its minimality.
3. The round's affine part: z -> L (z + (y, 0)); its N-th power is z -> z + S (y, 0), S = L + ... + L^N. S printed;
   the period at each passing: N where S (y, 0) = 0 on the dial, else 3 N.
4. The recurrence's constant, from tri7.Member's own step from the birth (u = tau before its carry, read by the
   Member's own shears before each step): u(t+2) - tr u(t+1) + u(t) on the dial over 3,000 rounds, against the derived
   (L00 - 1) y + (2 - tr) b (b the birth), against -y.
5. The square roots of 1 on the dial, by the factors and the carry's CRT; each checked.
6. The third landing after two: for u(t) = u0 in the window W, the exact count of u(t+1) in W (in the residue class
   mod 3 the pair can reach, u(t+1) = u(t) + y mod 3) whose u(t+2) lies in W, by whole lifts of W, at nine u0 across
   W and at its top; per mille of a, against floor(tr a) / (tr a); whether a whole number of dials lies in
   (18 (y - 1), 20 (y - 1)], the only place a lift is partly covered.
7. The toy's counts (read from the frozen toy7 outputs) against the derived value: expected, z^2 per mille, and z^2
   per period (the run spans R / period periods, its second part repeating the first).
8. The pair in the landing coordinate: the map (tau, eta) -> (u(t), u(t+1)) at y = 0 from the Member's shears, its
   det and its common factor with the dial; the pair in a = (tau + eta) / 2, b = (tau - eta) / 2 between carries."""
import re
import sys
from pathlib import Path

SRC, FROZEN = sys.argv[1], Path(sys.argv[2])
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402

universe, shape, held, lay, s0, world, star = tri7.load_world(SRC, Path(SRC).parent.joinpath("examples", "tensor24-click"))
key = int(lay.click.key[0, 0])
pairs, triangles = tri7.edge_set(world)
D = star["half"] * key
M = tri7.Member(len(pairs), triangles, D, star["senses"])
G, N3, b = M.G[0], M.tdial[0], M.tborn[0]


def md(n, m):
    return carry(n, m, 0)[1]


def fl(n, d):
    return carry(n, d, 0)[0]


def mul(a, c, m):
    return [[md(a[i][0] * c[0][j] + a[i][1] * c[1][j], m) for j in range(2)] for i in range(2)]


def add(a, c, m):
    return [[md(a[i][j] + c[i][j], m) for j in range(2)] for i in range(2)]


def eye(m):
    return [[md(1, m), 0], [0, md(1, m)]]


def power(a, k, m):
    r = eye(m)
    while k:
        k, bit = carry(k, 2, 0)
        if bit:
            r = mul(r, a, m)
        a = mul(a, a, m)
    return r


def geo(a, k, m):
    """(a^k, a + ... + a^k) modulo m, by doubling."""
    if k == 0:
        return eye(m), [[0, 0], [0, 0]]
    h, bit = carry(k, 2, 0)
    P, S = geo(a, h, m)
    P2, S2 = mul(P, P, m), add(S, mul(P, S, m), m)
    if bit:
        P2 = mul(P2, a, m)
        S2 = add(S2, P2, m)
    return P2, S2


def gcd(x, z):
    while z:
        x, z = z, md(x, z)
    return x


def cen(v):
    return M.cen(v, 0)


# 1. L from the Member's own shears: between two carries, the second half (tau += G eta, eta += G tau), then the next
# round's first half (eta += G tau, tau += G eta), on the centred basis
def between(tc, ec):
    tau, eta = b + tc, b + ec
    tau = M.shear(tau, eta, 0)
    eta = M.shear(eta, tau, 0)
    eta = M.shear(eta, tau, 0)
    tau = M.shear(tau, eta, 0)
    return cen(tau - b), cen(eta - b)


c1, c2 = between(1, 0), between(0, 1)
L = [[c1[0], c2[0]], [c1[1], c2[1]]]
tr, det = L[0][0] + L[1][1], L[0][0] * L[1][1] - L[0][1] * L[1][0]
big = 1 << 200
L2 = mul(L, L, big)
print(f"0. the click world's structure: edges {pairs}, C {M.C}, G = C^T C {M.G}; D = {D}; the triangle's dial G D = {N3},"
      f" born {b}")
print(f"1. L from the Member's shears = {L}: trace {tr}, det {det}, det(L - I) {(L[0][0] - 1) * (L[1][1] - 1) - L[0][1] * L[1][0]},"
      f" det(L + I) {(L[0][0] + 1) * (L[1][1] + 1) - L[0][1] * L[1][0]}; L^2 = tr L - I: "
      f"{L2 == [[tr * L[i][j] - (1 if i == j else 0) for j in range(2)] for i in range(2)]}")
# 2. the dial's factors and L's orders
n, f, fs = N3, 2, []
while f * f <= n:
    q, r = carry(n, f, 0)
    if r == 0:
        fs.append(f)
        n = q
    else:
        f += 1
if n > 1:
    fs.append(n)
pw = {}
for p in fs:
    pw[p] = pw.get(p, 0) + 1
orders, mods = {}, []
for p, e in sorted(pw.items()):
    m = 1
    for _ in range(e):
        m *= p
    mods.append(m)
    Ak, k = mul(L, eye(m), m), 1
    while Ak != eye(m):
        Ak = mul(Ak, L, m)
        k += 1
    orders[m] = k
N = 1
for k in orders.values():
    N = fl(N * k, gcd(N, k))
ps, n, f = [], N, 2
while n > 1:
    q, r = carry(n, f, 0)
    if r == 0:
        if f not in ps:
            ps.append(f)
        n = q
    else:
        f += 1
print(f"2. G D = {' x '.join(f'{p}^{e}' if e > 1 else str(p) for p, e in sorted(pw.items()))}; L's order modulo"
      f" {', '.join(f'{m}: {k}' for m, k in orders.items())}; N = lcm {N}; L^N = I on the dial: {power(L, N, N3) == eye(N3)};"
      f" L^(N/p) != I for p in {ps}: {[power(L, fl(N, p), N3) != eye(N3) for p in ps]}")
# 3. the affine part
P, S = geo(L, N, N3)
print(f"3. S = L + ... + L^N on the dial = {S} (D = {D}): the round's N-th power is z -> z + S (y, 0) = z + (D y, 0)"
      f" mod G D: {S == [[D, 0], [0, D]]}")
m50 = fl(D, 50)
RATES = ((9, 9, 12), (20, 30, 25), (40, 40, 45), (2, 3, 2), (1, 1, 2))
ga, ab, gb = (e for e, _ in M.C[0])


def passing(XM):
    x = [0] * len(pairs)
    x[ga], x[gb], x[ab] = XM[0] * m50, XM[1] * m50, XM[2] * m50
    return x, sum(sg * x[e] for e, sg in M.C[0])


for XM in RATES:
    x, y = passing(XM)
    Sv = (md(S[0][0] * y, N3), md(S[1][0] * y, N3))
    P3, S3 = geo(L, 3 * N, N3)
    S3v = (md(S3[0][0] * y, N3), md(S3[1][0] * y, N3))
    print(f"   {list(XM)} m: y = {y}, y mod 3 = {md(y, 3)}; S (y, 0) = {Sv}; at 3 N: {S3v}; so the period divides"
          f" {N if Sv == (0, 0) else 3 * N}")
# 4. the recurrence's constant from the Member's own step
for XM in RATES[:4]:
    x, y = passing(XM)
    f_, tau, eta = M.birth()
    us = []
    for t in range(3000):
        e1 = M.shear(eta[0], tau[0], 0)
        us.append(M.shear(tau[0], e1, 0))  # tau before its carry, by the Member's own first half
        M.step(x, f_, tau, eta)
    vals = sorted({md(us[t + 2] - tr * us[t + 1] + us[t], N3) for t in range(len(us) - 2)})
    derived = md((L[0][0] - 1) * y + (2 - tr) * b, N3)
    print(f"4. {list(XM)} m: u(t+2) - {tr} u(t+1) + u(t) on the dial over 3,000 rounds takes {len(vals)} value(s) {vals};"
          f" derived (L00 - 1) y + (2 - tr) b = {derived} = 18 (y + 1) mod G D: {derived == md(18 * (y + 1), N3)};"
          f" -y mod G D = {md(-y, N3)}")


# 5. the square roots of 1 on the dial, by the CRT
def inv(a_, m):
    r0, r1, s0_, s1 = m, md(a_, m), 0, 1
    while r1:
        q, r2 = carry(r0, r1, 0)
        r0, r1, s0_, s1 = r1, r2, s1, s0_ - q * s1
    return md(s0_, m)


roots = [0]
modsofar = 1
for m in mods:
    new = []
    for r in roots:
        for s in (1, m - 1):
            # x = r mod modsofar, x = s mod m
            t = md((s - r) * inv(modsofar, m), m)
            new.append(r + modsofar * t)
    roots, modsofar = new, modsofar * m
roots = sorted(md(r, N3) for r in roots)
print(f"5. square roots of 1 on the dial G D: {len(roots)}, each r^2 = 1: {all(md(r * r, N3) == 1 for r in roots)};"
      f" other than +-1: {[r for r in roots if r not in (1, N3 - 1)]}")


# 6. the third landing after two, exact, by whole lifts of W
def count3(A, B, r):
    """whole numbers n in [A, B] with n = r mod 3"""
    if B < A:
        return 0
    return fl(B - r, 3) - fl(A - 1 - r, 3)


def ceil_div(n, d):
    return -fl(-n, d)


ratios = {}
for XM in ((20, 30, 25), (40, 40, 45), (9, 9, 12)):
    x, y = passing(XM)
    lo = N3 - y
    cst = md((L[0][0] - 1) * y + (2 - tr) * b, N3)  # the derived constant (item 4)
    out = []
    grid = [lo + fl(j * y, 9) for j in range(9)] + [N3 - 1]
    for u0 in grid:
        r1 = md(u0 + y, 3)
        tot = count3(lo, N3 - 1, r1)
        hits = 0
        zmin, zmax = tr * lo - u0 + cst, tr * (N3 - 1) - u0 + cst
        for k in range(fl(zmin, N3) - 1, fl(zmax, N3) + 2):
            A = ceil_div(k * N3 + lo + u0 - cst, tr)
            B = fl(k * N3 + N3 - 1 + u0 - cst, tr)
            hits += count3(max(A, lo), min(B, N3 - 1), r1)
        out.append((hits, tot))
    h0, h2 = L[0][0] - 1, L[0][0] + 1  # 18 and 20: a lift of W is partly swept only for k dials in (h0 (y - 1), h2 (y - 1)]
    kk = fl(h2 * (y - 1), N3)
    lift = kk >= 1 and kk * N3 > h0 * (y - 1)
    pm = [fl(1000 * h * N3, t * y) for h, t in out]
    der = fl(1000 * fl(tr * y, N3) * N3, tr * y)
    ratios[XM] = out[0]
    print(f"6. {list(XM)} m, a = y / G D = {fl(1000 * y, N3)} per mille, tr a = {fl(1000 * tr * y, N3)} per mille:"
          f" P(third | two at u0) / a per mille at nine u0 across W and its top {pm}; floor(tr a) / (tr a) = {der} per"
          f" mille; a whole number of dials in (18 (y - 1), 20 (y - 1)]: {lift}")
# 7. the toy's counts against the derived value
TOY = (("toy7_rate_20_30_25_birth_1M.txt", (20, 30, 25)), ("toy7_rate_20_30_25_standin_1M.txt", (20, 30, 25)),
       ("toy7_rate_40_40_45_birth_1M.txt", (40, 40, 45)), ("toy7_rate_40_40_45_standin_1M.txt", (40, 40, 45)),
       ("toy7_birth_1M.txt", (9, 9, 12)), ("toy7_standin_1M.txt", (9, 9, 12)))
for name, XM in TOY:
    txt = FROZEN.joinpath(name).read_text()
    line = [ln for ln in txt.splitlines() if ln.strip().startswith("path:")][0]
    k3, k2 = (int(v) for v in re.search(r"after two a third (\d+) of (\d+)", line).groups())
    R = int(re.search(r"; (\d+) rounds from", txt).group(1))
    h, t = ratios[XM]
    exp_n, exp_d = k2 * h, t  # expected = k2 h / t
    var_n = k2 * h * (t - h)  # var = k2 p (1 - p), p = h / t: k2 h (t - h) / t^2
    dev_n = k3 * t - exp_n  # (k3 - k2 h / t) t
    z2 = fl(1000 * dev_n * dev_n, var_n)  # per mille: dev^2 / var = dev_n^2 / (var_n)
    z2p = fl(z2 * N, R)  # per period: the run spans R / N periods (3 divides y at these passings)
    print(f"7. {name}: after two a third {k3} of {k2}; derived {fl(exp_n, exp_d)}; ratio to the derived {fl(1000 * k3 * t, exp_n)}"
          f" per mille; z^2 {z2} per mille over {R} rounds, {z2p} per mille per period ({fl(1000 * R, N)} per mille periods)")
# 8. the landing coordinate's now and before
def first_u(tc, ec):
    tau, eta = b + tc, b + ec
    eta = M.shear(eta, tau, 0)
    tau = M.shear(tau, eta, 0)
    u_t = cen(tau - b)
    tau = M.shear(tau, eta, 0)  # the carry of y = 0 lands nothing
    eta = M.shear(eta, tau, 0)
    eta = M.shear(eta, tau, 0)
    tau = M.shear(tau, eta, 0)
    return u_t, cen(tau - b)


m1, m2 = first_u(1, 0), first_u(0, 1)
U = [[m1[0], m2[0]], [m1[1], m2[1]]]
dU = U[0][0] * U[1][1] - U[0][1] * U[1][0]
# a = (tau + eta) / 2, b = (tau - eta) / 2: L in (a, b) is T^-1 L T, T = [[1, 1], [1, -1]], T^-1 = T / 2
LT = [[L[0][0] + L[0][1], L[0][0] - L[0][1]], [L[1][0] + L[1][1], L[1][0] - L[1][1]]]
Lab2 = [[LT[0][j] + LT[1][j] for j in range(2)], [LT[0][j] - LT[1][j] for j in range(2)]]
Lab = [[fl(v, 2) for v in row] for row in Lab2]
print(f"8. (tau, eta) -> (u(t), u(t+1)) at y = 0, from the Member's shears: {U}, det {dU}, its common factor with G D"
      f" {gcd(dU, N3)} (so {gcd(dU, N3)} states share each (u(t), u(t+1))); L in (a, b) = ((tau + eta) / 2, (tau - eta) / 2):"
      f" {Lab} (b' = {Lab[1][0]} a + {Lab[1][1]} b, not b' = a)")
# 9. the frame: the second difference read at three points of the round, and the round's matrix at the round's edge
for XM in ((9, 9, 12), (2, 3, 2)):
    x, y = passing(XM)
    f_, tau, eta = M.birth()
    starts, befores, afters = [], [], []
    for t in range(3000):
        starts.append(tau[0])  # the round's start (after the last round's second half)
        e1 = M.shear(eta[0], tau[0], 0)
        u = M.shear(tau[0], e1, 0)
        befores.append(u)  # before the carry
        afters.append(carry(y, N3, u)[1])  # after the carry
        M.step(x, f_, tau, eta)
    out = []
    for seq in (starts, befores, afters):
        vals = sorted({cen(seq[t + 2] - tr * seq[t + 1] + seq[t] - (2 - tr) * b) for t in range(len(seq) - 2)})
        out.append(vals)
    print(f"9. {list(XM)} m, y = {y}: the second difference less the birth's (2 - tr) b, centred: at the round's start"
          f" {out[0]}, before the carry {out[1]} (18 y = {cen(18 * y)}), after the carry {out[2]} (-18 y = {cen(-18 * y)})")


def edge_round(tc, ec):
    tau, eta = b + tc, b + ec
    eta = M.shear(eta, tau, 0)
    tau = M.shear(tau, eta, 0)
    tau = M.shear(tau, eta, 0)  # the carry of y = 0 between
    eta = M.shear(eta, tau, 0)
    return cen(tau - b), cen(eta - b)


r1, r2 = edge_round(1, 0), edge_round(0, 1)
Me = [[r1[0], r2[0]], [r1[1], r2[1]]]
MT = [[Me[0][0] + Me[0][1], Me[0][0] - Me[0][1]], [Me[1][0] + Me[1][1], Me[1][0] - Me[1][1]]]
Mab = [[fl(MT[0][j] + MT[1][j], 2) for j in range(2)], [fl(MT[0][j] - MT[1][j], 2) for j in range(2)]]
print(f"9. the round from its start to its end (first half, carry, second half) at y = 0, on (tau, eta): {Me}; on (eta, tau):"
      f" {[[Me[1][1], Me[1][0]], [Me[0][1], Me[0][0]]]}; L transposed: {Me == [[L[0][0], L[1][0]], [L[0][1], L[1][1]]]};"
      f" in (a, b): {Mab}")
print("DONE")
