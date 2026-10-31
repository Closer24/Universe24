"""THIRD8: what the click record shows of the path at one Node-clock (a reading probe, never src). Whole numbers only;
Rule3's carry the one division. The click world, Node-clock 0 (every Node-clock alike on this lay, board7m), ROUNDS
rounds; the board run by step.act, the member, the member unturned and the first click run on Node-clock 0's flows
(tri7, the structure read from the world). Read from the record a form writes (its sides q per edge, its lines B q):
  R1 one clock alone: its line (B q) under the member, unturned and with one hidden unit in the twin (rounds apart);
     and its two sides: the side pairs it sees with more than one landing w (so its sides do not fix w);
  R2 the three sides together: the circulation c . q against 3 w per round (rounds apart, apart by 2 or more, the
     nearest multiple of 3's misses); the running |c . Q - 3 W|; the side triples seen with more than one w;
     rounds whose three sides form one whole circulation (c_e q_e all of one sign, none 0), and the landings so seen;
  R3 seed (ii) at this Node-clock: one hidden unit in the twin: sides apart per edge, from which round, and the rounds
     whose landing differs; the edges on no triangle.
argv: src, rounds."""
import sys
from pathlib import Path

SRC, ROUNDS = sys.argv[1], int(sys.argv[2])
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import tri7  # noqa: E402

tri7.setup(SRC)
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

universe, shape, held, lay, s0, world, star = tri7.load_world(SRC, Path(SRC).parent.joinpath("examples", "tensor24-click"))
rows = s0.a.shape[0]
key = int(lay.click.key[0, 0])
pairs, triangles = tri7.edge_set(world)
D = star["half"] * key
M = tri7.Member(len(pairs), triangles, D, star["senses"])
F = tri7.First(len(pairs), D, star["senses"])
c = [0] * len(pairs)
for e, sg in M.C[0]:
    c[e] = sg
trains = sorted({t for p in pairs for t in p})
lone = [pairs[e] for e in range(len(pairs)) if not M.on[e]]

flows = []
s = s0
for t in range(ROUNDS):
    s1, _ = step.act(lay, s)
    bb = [int(s.b[r, 0]) for r in range(rows)]
    aa = [int(s.a[r, 0]) for r in range(rows)]
    a1 = [int(s1.a[r, 0]) for r in range(rows)]
    fl = world.split_flows(0, bb, aa, a1)
    flows.append([fl.get(pr, 0) for pr in pairs])
    s = s1


TEETH = []


def run_member(turned=True, hidden=False, keep=False):
    f, tau, eta = M.birth()
    if hidden:
        eta[0] = M.tborn[0] + M.cen(eta[0] - M.tborn[0] + 1, 0)
    out = []
    for xv in flows:
        fb = list(f)
        q, w = M.step(xv, f, tau, eta, turned=turned)
        out.append((q, w[0]))
        if keep:
            TEETH.append((fb, list(f)))
    return out


def run_first():
    f = F.birth()
    return [(F.step(xv, f), 0) for xv in flows]


def line(q):
    return tuple(sum(q[e] * (1 if pairs[e][0] == tr else -1) for e in range(len(pairs)) if tr in pairs[e]) for tr in trains)


def sgn(v):
    return (v > 0) - (v < 0)


mem, unt, hid, fst = run_member(keep=True), run_member(turned=False), run_member(hidden=True), run_first()
lands = sum(1 for _, w in mem if w)
print(f"dec8: the click world, Node-clock 0, {ROUNDS} rounds; edges {pairs}, c {c}, edges on no triangle {lone};"
      f" the member lands in {lands} rounds")
# R1: one clock alone
la_u = sum(1 for (q1, _), (q2, _) in zip(mem, unt) if line(q1) != line(q2))
la_h = sum(1 for (q1, _), (q2, _) in zip(mem, hid) if line(q1) != line(q2))
print(f"R1 lines: rounds whose lines differ, the member against the member unturned {la_u}, against one hidden unit in"
      f" the twin {la_h}")
for tr in trains:
    es = [e for e in range(len(pairs)) if tr in pairs[e]]
    seen = {}
    for q, w in mem:
        seen.setdefault(tuple(q[e] for e in es), set()).add(w)
    amb = [k for k, v in seen.items() if len(v) > 1]
    rounds_amb = sum(1 for q, _ in mem if tuple(q[e] for e in es) in amb)
    print(f"R1 clock {tr}, its sides on edges {[pairs[e] for e in es]}: {len(seen)} side pairs seen, {len(amb)} of them"
          f" with more than one w ({rounds_amb} of {ROUNDS} rounds); e.g. {[(k, sorted(seen[k])) for k in amb[:3]]}")
# R2: the three sides together
diff = diff2 = miss = 0
runQ = runW = runmax = 0
seen3 = {}
for q, w in mem:
    cq = sum(c[e] * q[e] for e in range(len(pairs)))
    k = cq - 3 * w
    diff += int(k != 0)
    diff2 += int(k >= 2 or k <= -2)
    wh = carry(cq + 1, 3, 0)[0]  # the nearest multiple of 3 (3 is odd, no ties)
    miss += int(wh != w)
    runQ += cq
    runW += w
    runmax = max(runmax, abs(runQ - 3 * runW))
    seen3.setdefault(tuple(q), set()).add(w)
amb3 = sum(1 for v in seen3.values() if len(v) > 1)
print(f"R2 c . q against 3 w: apart in {diff} rounds, by 2 or more in {diff2}; the nearest multiple of 3 misses w in {miss}"
      f" rounds (right in {ROUNDS - miss}); the running |c . Q - 3 W| at most {runmax}; side triples {len(seen3)},"
      f" {amb3} of them with more than one w")
for name, rec in (("member", mem), ("unturned", unt), ("first click", fst)):
    whole = 0
    seen_l = 0
    for q, w in rec:
        ss = {sgn(c[e] * q[e]) for e in range(len(pairs))}
        wh = ss.pop() if len(ss) == 1 and 0 not in ss else 0
        whole += int(wh != 0)
        seen_l += int(w != 0 and wh == sgn(w))
    print(f"R2 {name}: rounds whose three sides form one whole circulation {whole} of {ROUNDS}"
          + (f"; landings so seen {seen_l} of {sum(1 for _, w in rec if w)}" if name != "first click" else ""))
# R3: seed (ii) at this Node-clock
sa = [0] * len(pairs)
first_t = None
for t, ((q1, _), (q2, _)) in enumerate(zip(mem, hid)):
    for e in range(len(pairs)):
        if q1[e] != q2[e]:
            sa[e] += 1
            first_t = t if first_t is None else first_t
wa = sum(1 for (_, w1), (_, w2) in zip(mem, hid) if w1 != w2)
print(f"R3 one hidden unit in the twin: (round, edge) places apart per edge {sa} (sum {sum(sa)}), from round {first_t};"
      f" rounds whose landing differs {wa}; lines apart {la_h}")
# R4: edges that pass a quantum at the triangle, per round; and the path from the sides with the edges' teeth
for name, rec in (("member", mem), ("unturned", unt), ("first click", fst)):
    cnt = [0, 0, 0, 0]
    for q, _ in rec:
        cnt[sum(1 for e in range(len(pairs)) if q[e])] += 1
    print(f"R4 {name}: rounds with 3, 2, 1, 0 of the triangle's edges passing a quantum: {cnt[3]}, {cnt[2]}, {cnt[1]}, {cnt[0]}")
GD = M.dial[0]
ok = 0
for (q, w), (fb, fa) in zip(mem, TEETH):
    P = [GD * q[e] + fa[e] - fb[e] for e in range(len(pairs))]  # each side's passing as K q + k_after - k_before
    cP = sum(c[e] * P[e] for e in range(len(pairs)))
    ok += int(cP == M.G[0] * M.tdial[0] * w)
print(f"R4 with each edge's tooth before and after in the record: c . (G D q + k_after - k_before) = G (G D) w in {ok} of"
      f" {ROUNDS} rounds (so the three sides with their teeth give w exactly)")
print("DONE")
