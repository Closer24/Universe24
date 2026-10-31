"""THIRD9's arithmetic (a reading, never an act). Whole numbers only; every division and reduction is Rule3's carry.
The click world's structure is loaded (tri7.load_world); C, G = C^T C, the edges and the triangle read from it; the
dial from the star and the world's key. argv: src.

1. The twin's unread third: on the twin held on G D, the shifts eta + D and eta + 2 D move neither u(t) nor u(t+1)
   (the map's kernel), and they keep eta's residue mod 3 (D = 0 mod 3).
2. The round's fixed points at a steady passing: the 3-part (tau mod 27, eta mod 27 or mod 9) by exhaustion of the
   centred round; at 641 and 26,423 the unique solution of (L - I) z = -L v; joined by the CRT, each checked by the
   Member's own step (tri7.Member with the twin on G D, tri9.MemberD with the twin on D), with its landing per round.
3. The exact value's margin: at each passing the gaps from (18 (y - 1), 20 (y - 1)] to the multiples of G D around
   it, and the least change of y that lets a lift of W be partly swept."""
import sys
from pathlib import Path

SRC = sys.argv[1]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402
import tri9  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402

universe, shape, held, lay, s0, world, star = tri7.load_world(SRC, Path(SRC).parent.joinpath("examples", "tensor24-click"))
key = int(lay.click.key[0, 0])
pairs, triangles = tri7.edge_set(world)
D = star["half"] * key
M = tri7.Member(len(pairs), triangles, D, star["senses"])
MD = tri9.MemberD(len(pairs), triangles, D, star["senses"])
G, N3, b = M.G[0], M.tdial[0], M.tborn[0]
Dd, bd = MD.ddial[0], MD.dborn[0]
m50 = carry(D, 50, 0)[0]
ga, ab, gb = (e for e, _ in M.C[0])


def md(n, m):
    return carry(n, m, 0)[1]


def fl(n, d):
    return carry(n, d, 0)[0]


def passing(XM):
    x = [0] * len(pairs)
    x[ga], x[gb], x[ab] = XM[0] * m50, XM[1] * m50, XM[2] * m50
    return x, sum(sg * x[e] for e, sg in M.C[0])




def between(tc, ec):
    tau, eta = b + tc, b + ec
    tau = M.shear(tau, eta, 0)
    eta = M.shear(eta, tau, 0)
    eta = M.shear(eta, tau, 0)
    tau = M.shear(tau, eta, 0)
    return M.cen(tau - b, 0), M.cen(eta - b, 0)


c1, c2 = between(1, 0), between(0, 1)
L = [[c1[0], c2[0]], [c1[1], c2[1]]]
print(f"0. G = C^T C {G}; D = {D} (the twin's dial on D: {Dd}, born {bd}); G D = {N3}, born {b}; L from the Member's"
      f" shears {L}")


# 1. the kernel: (0, D) and (0, 2 D), centred, through the first half and one round at y = 0
def u_pair(tc, ec):
    tau, eta = b + tc, b + ec
    eta = M.shear(eta, tau, 0)
    tau = M.shear(tau, eta, 0)
    u0 = M.cen(tau - b, 0)
    tau = M.shear(tau, eta, 0)
    eta = M.shear(eta, tau, 0)
    eta = M.shear(eta, tau, 0)
    tau = M.shear(tau, eta, 0)
    return u0, M.cen(tau - b, 0)


print(f"1. (u(t), u(t+1)) of the centred shifts (0, D) and (0, 2 D) at y = 0: {u_pair(0, D)} and {u_pair(0, 2 * D)};"
      f" of (0, 1): {u_pair(0, 1)}; eta's residue mod 3 under + D and + 2 D: kept, D mod 3 = {md(D, 3)}")


# 2. the fixed points
def inv(a, m):
    r0, r1, s0_, s1 = m, md(a, m), 0, 1
    while r1:
        q, r2 = carry(r0, r1, 0)
        r0, r1, s0_, s1 = r1, r2, s1, s0_ - q * s1
    return md(s0_, m)


def crt(parts):
    x, m = 0, 1
    for r, mm in parts:
        t = md((r - x) * inv(m, mm), mm)
        x, m = x + m * t, m * mm
    return md(x, m), m


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
for p_ in fs:
    pw[p_] = pw.get(p_, 0) + 1
three = 1
for _ in range(pw[3]):
    three *= 3
others = sorted(p_ for p_ in pw if p_ != 3)
assert all(pw[p_] == 1 for p_ in others)


def round_c(tc, ec, y, mt, me):
    e1 = md(ec + G * tc, me)
    t1 = md(tc + G * e1, mt)
    t2 = md(t1 + y, mt)
    t3 = md(t2 + G * e1, mt)
    e3 = md(e1 + G * t3, me)
    return t3, e3


for XM in ((20, 30, 25), (9, 9, 12), (40, 40, 45), (2, 3, 2)):
    x, y = passing(XM)
    for name, mem, me3, edial, eborn in (("twin on G D", M, three, N3, b), ("twin on D", MD, fl(three, G), Dd, bd)):
        sols3 = [(tc, ec) for tc in range(three) for ec in range(me3) if round_c(tc, ec, y, three, me3) == (tc, ec)]
        # at 641 and 26,423 the unique fixed point there (det(L - I) = -36 a unit): between carries z = (-y / 2, -y / 6),
        # so at the round's start s = H1^-1 z = (0, -y / 6) (the frame the step maps, start to start)
        zp = {}
        for p_ in others:
            zp[p_] = (0, md(-y * inv(6, p_), p_))
        checks, landing = [], []
        for tc, ec in sols3:
            T, _ = crt([(tc, three)] + [(zp[p_][0], p_) for p_ in others])
            E, _ = crt([(ec, me3)] + [(zp[p_][1], p_) for p_ in others])
            tau = [md(b + T, N3)]
            eta = [md(eborn + E, edial)]
            start = (tau[0], eta[0])
            f_ = list(M.born)
            q, w = mem.step(x, f_, tau, eta)
            checks.append((tau[0], eta[0]) == start)
            landing.append(w[0])
        print(f"2. {list(XM)} m, y mod 3 = {md(y, 3)}, the {name}: fixed points {len(sols3)} (the 3-part {len(sols3)}, one at"
              f" each of {others}); each back after one round by the Member's own step: {all(checks) if checks else '-'};"
              f" their landings per round {landing}")
# 3. the margin
for XM in ((20, 30, 25), (40, 40, 45), (9, 9, 12)):
    x, y = passing(XM)
    h0, h2 = L[0][0] - 1, L[0][0] + 1  # 18 and 20, read from L (the recurrence's constant and its sweep)
    lo, hi = h0 * (y - 1), h2 * (y - 1)
    k_lo, k_hi = fl(lo, N3), fl(hi, N3)
    holds = k_lo == k_hi
    gap_hi = (k_hi + 1) * N3 - hi
    gap_lo = lo - k_lo * N3
    print(f"3. {list(XM)} m: y = {y}; no multiple of G D in (18 (y - 1), 20 (y - 1)]: {holds}; the gap above 20 (y - 1) to"
          f" {k_hi + 1} G D is {gap_hi} units, below 18 (y - 1) to {k_lo} G D {gap_lo} units; so y + {fl(gap_hi, h2) + 1} or"
          f" y - {fl(gap_lo, h0) + 1} lets a lift be partly swept (the window y = {y} units wide, the dial {N3})")
print("DONE")
