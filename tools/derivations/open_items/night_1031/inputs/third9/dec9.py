"""THIRD9: the click record at Node-clock 0 over ROUNDS rounds (a reading probe, never src). Whole numbers only; Rule3's
carry the one division. The board run by step.act; on Node-clock 0's flows: tri7.Member (the twin on G D), tri9.MemberD
(the twin on D), the member unturned, and the first click (tri7.First), each with its edges' teeth before and after.
  Q10 one clock's sides, out of sample: a map from a clock's side pair to the landing w, learned on the first half of
      the rounds (each pair's commonest w; an unseen pair read as the first half's commonest w) and read on the second;
      against always guessing the first half's commonest w; and c . q's nearest multiple of 3 on the second half;
  CQ  rounds whose c . q has a nearest multiple of 3 that is not 0 ("read as a landing"), on each form's record, against
      its own landings; whole circulations in one round (c_e q_e all of one sign, none 0);
  M2  the member's landing rounds by how many of the triangle's edges pass a quantum (3, 2, 1, 0);
  X   the 1.4 side passing x = (dial) q + k_after - k_before on the triangle's edges: on the member's record against
      p_e + G D c_e w, and on the first click's against x_e; the circulation c . x in whole quanta of G (G D) every
      round (a reading the first click's record fails where y is not one), and c . x = G (G D) w (a code check);
  TD  the twin on D against on G D (sides, lines, landings); its run back from its end alone (the twin flipped on D,
      the passings negated and reversed); one hidden unit in the twin, places apart in both forms;
  GL  the landing coordinate: the state at each round's start rebuilt from (u(t), u(t+1)) and the round's y, on the
      twin on D;
  R3  the edges' teeth's residues mod 3 against tau's, f_e = born - c_e (tau - born); the twin's residue mod 3.
argv: src, rounds (even)."""
import sys
from pathlib import Path

SRC, ROUNDS = sys.argv[1], int(sys.argv[2])
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402
import tri9  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

universe, shape, held, lay, s0, world, star = tri7.load_world(SRC, Path(SRC).parent.joinpath("examples", "tensor24-click"))
rows = s0.a.shape[0]
key = int(lay.click.key[0, 0])
pairs, triangles = tri7.edge_set(world)
D = star["half"] * key
M = tri7.Member(len(pairs), triangles, D, star["senses"])
MD = tri9.MemberD(len(pairs), triangles, D, star["senses"])
F = tri7.First(len(pairs), D, star["senses"])
ne = len(pairs)
c = [0] * ne
for e, sg in M.C[0]:
    c[e] = sg
G, N3, b, Dd, bd = M.G[0], M.tdial[0], M.tborn[0], MD.ddial[0], MD.dborn[0]
trains = sorted({t for p in pairs for t in p})
mine = {tr: [e for e in range(ne) if tr in pairs[e]] for tr in trains}
HALF = carry(ROUNDS, 2, 0)[0]


def md(n, m):
    return carry(n, m, 0)[1]


def fl(n, d):
    return carry(n, d, 0)[0]


flows = []
s = s0
for t in range(ROUNDS):
    s1, _ = step.act(lay, s)
    bb = [int(s.b[r, 0]) for r in range(rows)]
    aa = [int(s.a[r, 0]) for r in range(rows)]
    a1 = [int(s1.a[r, 0]) for r in range(rows)]
    fl_ = world.split_flows(0, bb, aa, a1)
    flows.append([fl_.get(pr, 0) for pr in pairs])
    s = s1


def run(mem, turned=True, hidden=False, keep=False):
    f, tau, eta = mem.birth()
    if hidden:
        eta[0] = (mem.dborn[0] + mem.dcen(eta[0] - mem.dborn[0] + 1, 0)) if mem is MD else \
            (mem.tborn[0] + mem.cen(eta[0] - mem.tborn[0] + 1, 0))
    out, extra = [], []
    for xv in flows:
        fb, st = list(f), (tau[0], eta[0])
        q, w = mem.step(xv, f, tau, eta, turned=turned)
        out.append((q, w[0]))
        if keep:
            extra.append((fb, list(f), st))
    return out, extra, (list(f), list(tau), list(eta))


def run_first():
    f = F.birth()
    out, extra = [], []
    for xv in flows:
        fb = list(f)
        q = F.step(xv, f)
        out.append((q, 0))
        extra.append((fb, list(f), None))
    return out, extra


mem, memx, mend = run(M, keep=True)
memd, memdx, mdend = run(MD, keep=True)
unt, _, _ = run(M, turned=False)
fst, fstx = run_first()
ys = [sum(sg * xv[e] for e, sg in M.C[0]) for xv in flows]
lands = sum(1 for _, w in mem if w)
print(f"dec9: the click world, Node-clock 0, {ROUNDS} rounds; edges {pairs}, c {c}; G D {N3}, the twin's D {Dd};"
      f" the member lands in {lands} rounds")


def commonest(ws):
    cnt = {}
    for w in ws:
        cnt[w] = cnt.get(w, 0) + 1
    return sorted(cnt.items(), key=lambda kv: (-kv[1], abs(kv[0]), kv[0]))[0][0]


# Q10
base = commonest([w for _, w in mem[:HALF]])
base_right = sum(1 for _, w in mem[HALF:] if w == base)
for tr in trains:
    es = mine[tr]
    seen = {}
    for q, w in mem[:HALF]:
        seen.setdefault(tuple(q[e] for e in es), []).append(w)
    rule = {k: commonest(v) for k, v in seen.items()}
    right = sum(1 for q, w in mem[HALF:] if rule.get(tuple(q[e] for e in es), base) == w)
    print(f"Q10 clock {tr}, its sides {[pairs[e] for e in es]}: the learned map gives w right in {right} of"
          f" {ROUNDS - HALF} later rounds; always guessing {base}: {base_right}")
cq_right = sum(1 for q, w in mem[HALF:] if fl(sum(c[e] * q[e] for e in range(ne)) + 1, 3) == w)
print(f"Q10 the three sides together (c . q's nearest multiple of 3): right in {cq_right} of {ROUNDS - HALF} later rounds")
# CQ
for name, rec in (("member", mem), ("unturned", unt), ("first click", fst)):
    read = sum(1 for q, _ in rec if fl(sum(c[e] * q[e] for e in range(ne)) + 1, 3) != 0)
    whole = 0
    for q, _ in rec:
        ss = {(c[e] * q[e] > 0) - (c[e] * q[e] < 0) for e in range(ne)}
        whole += int(len(ss) == 1 and 0 not in ss)
    print(f"CQ {name}: rounds read as a landing by c . q {read} of {ROUNDS}; its own landings"
          f" {sum(1 for _, w in rec if w)}; rounds whose three sides form one whole circulation {whole}")
# M2
by = [0, 0, 0, 0]
for q, w in mem:
    if w:
        by[sum(1 for e in range(ne) if q[e])] += 1
print(f"M2 the member's {lands} landing rounds with 3, 2, 1, 0 of the triangle's edges passing a quantum: {by[3]}, {by[2]},"
      f" {by[1]}, {by[0]}")
# X
okm = okl = nl = okf = 0
circ_m = circ_f = y0 = code = 0
for t, ((q, w), (fb, fa, _)) in enumerate(zip(mem, memx)):
    y = ys[t]
    p = [M.g[e] * flows[t][e] - sum(sg * y for _, sg in M.on[e]) for e in range(ne)]
    xr = [M.dial[e] * q[e] + fa[e] - fb[e] for e in range(ne)]
    for e in range(ne):
        okm += int(xr[e] == p[e] + N3 * c[e] * w)
        if w:
            nl += 1
            okl += int(xr[e] - p[e] == N3 * c[e] * w)
    cx = sum(c[e] * xr[e] for e in range(ne))
    circ_m += int(md(cx, G * N3) == 0)
    code += int(cx == G * N3 * w)
for t, ((q, _), (fb, fa, _)) in enumerate(zip(fst, fstx)):
    xr = [F.D * q[e] + fa[e] - fb[e] for e in range(ne)]
    okf += sum(1 for e in range(ne) if xr[e] == flows[t][e])
    cx = sum(c[e] * xr[e] for e in range(ne))
    circ_f += int(md(cx, G * N3) == 0)
    y0 += int(ys[t] == 0)
print(f"X the member's side passing x = (G D) q + k_after - k_before equals p_e + G D c_e w at {okm} of {ROUNDS * ne}"
      f" side-rounds; at the {nl} landing side-rounds x - p_e = G D c_e w at {okl}; the first click's x equals its passing"
      f" x_e at {okf} of {ROUNDS * ne}")
print(f"X c . x in whole quanta of G (G D): the member's record {circ_m} of {ROUNDS} rounds, the first click's {circ_f}"
      f" (rounds with y = 0: {y0}); c . x = G (G D) w on the member's record at {code} of {ROUNDS} (a code check)")
# TD
apart = sum(1 for (q1, w1), (q2, w2) in zip(mem, memd) if q1 != q2 or w1 != w2)
f, tau, eta = mdend
eta = MD.flip(eta)
back_w = []
for xv in reversed(flows):
    q, w = MD.step([-v for v in xv], f, tau, eta)
    back_w.append(w[0])
eta = MD.flip(eta)
born = MD.birth()
back = (f, tau, eta) == (born[0], born[1], born[2])
wneg = back_w == [-w for _, w in reversed(memd)]
hidG, _, _ = run(M, hidden=True)
hidD, _, _ = run(MD, hidden=True)
plG = sum(1 for (q1, _), (q2, _) in zip(mem, hidG) for e in range(ne) if q1[e] != q2[e])
plD = sum(1 for (q1, _), (q2, _) in zip(memd, hidD) for e in range(ne) if q1[e] != q2[e])
print(f"TD the twin on D against on G D: {apart} rounds apart in sides or landings (lines follow the sides); the run back"
      f" from the end alone reaches the birth (the edges' teeth, tau, the twin on D): {back}; its landings the forward"
      f" ones negated and reversed: {wneg}; one hidden unit in the twin moves {plG} (round, edge) places on G D and {plD}"
      f" on D")
# GL: L from the Member's own shears; z1(t+1) = L00 (z1 + y) + L01 z2, L01 = G k; z = H1 s, H1^-1 = [[1, -G], [-G, 1 + G G]]
def between(tc, ec):
    tau_, eta_ = b + tc, b + ec
    tau_ = M.shear(tau_, eta_, 0)
    eta_ = M.shear(eta_, tau_, 0)
    eta_ = M.shear(eta_, tau_, 0)
    tau_ = M.shear(tau_, eta_, 0)
    return M.cen(tau_ - b, 0), M.cen(eta_ - b, 0)


cc1, cc2 = between(1, 0), between(0, 1)
L = [[cc1[0], cc2[0]], [cc1[1], cc2[1]]]
kq, kr = carry(L[0][1], G, 0)  # L01 = G k (60 = 3 x 20)
assert kr == 0
r0, r1, s0_, s1_ = Dd, md(kq, Dd), 0, 1  # k a unit on D
while r1:
    qq, r2 = carry(r0, r1, 0)
    r0, r1, s0_, s1_ = r1, r2, s1_, s0_ - qq * s1_
assert r0 == 1
inv20 = md(s0_, Dd)
us = []
for (fb, fa, st) in memdx:
    tau0, eta0 = st
    t1, _ = MD.first_half(tau0, eta0, 0)
    us.append(t1)
good = 0
for t in range(ROUNDS - 1):
    z1 = M.cen(us[t] - b, 0)
    z1n = M.cen(us[t + 1] - b, 0)
    num = md(z1n - L[0][0] * (z1 + ys[t]), N3)
    qd, rm = carry(num, G, 0)
    z2 = md(inv20 * qd, Dd)
    tc = md(z1 - G * z2, N3)
    ec = md(-G * z1 + (1 + G * G) * z2, Dd)
    tau0, eta0 = memdx[t][2]
    good += int(rm == 0 and tc == md(tau0 - b, N3) and ec == md(eta0 - bd, Dd))
print(f"GL the state at the round's start rebuilt from (u(t), u(t+1)) and y: right at {good} of {ROUNDS - 1} rounds (the"
      f" twin on D)")
# R3
okr = okt = 0
for (q, w), (fb, fa, st) in zip(memd, memdx):
    tau0, eta0 = st
    for e in range(ne):
        okr += int(md(fb[e], 3) == md(b - c[e] * (tau0 - b), 3))
    okt += int(md(eta0, 3) == md(bd, 3))
print(f"R3 f_e = born - c_e (tau - born) mod 3 at {okr} of {ROUNDS * ne} side-rounds; the twin's residue mod 3 its birth's"
      f" at {okt} of {ROUNDS} rounds")
print("DONE")
