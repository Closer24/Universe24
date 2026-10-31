"""ALG3: the third click's member, read on its 2-cell, on node-all's own passings (a reading probe, never src).

Args: <tree> <bench dir with Big Pic's circ.py> <world dir> <rounds>
At every Node-clock, Big Pic's mode 11 Stepper (circ.py, run read only) is fed node-all's own edge passings P(t, u) of
the triangle's three edges, round by round, at the edge dial D (the tree's edge key). Read:
  - the edges' teeth: is their circulation c . g (centred) 0 mod 3D at every round (the cocycle law)?
  - the member held small: two edge teeth, tau on 3D and the twin on D (four numbers), the third edge's tooth read back
    from the other two by the cocycle law; its quanta on all three edges and its landings against the Stepper's, every
    round; and its run back from its end alone (the edge teeth and tau kept, the twin flipped on D, the passings
    negated and reversed).
Whole numbers only; Rule3's carry the one division."""
import json
import sys
from pathlib import Path

tree, bench, world, rounds = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), int(sys.argv[4])
sys.path.insert(0, str(tree.joinpath("src")))
sys.path.insert(0, str(bench))
import numpy as np  # noqa: E402
from tensor24 import main  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402
from tensor24.engine.state import State  # noqa: E402
from tensor24.runner import files  # noqa: E402
from tensor24.runner import load as L  # noqa: E402
import circ  # noqa: E402

paths = [world.joinpath(n + ".json") for n in ("universe", "piece", "setting")]
assert not files.departures(*paths)
universe, piece, setting = (json.loads(p.read_text(encoding="utf-8")) for p in paths)
shape = piece["shape"]
kinds, tables, square, lifted = main.ENGINE.made(files.star(len(shape)))
ld, found = L.load(universe, setting, files.sites_of(shape), kinds, tables, square, lifted)
assert not found, found
lay = main.ENGINE.layout(universe, shape, ld)
s = State(*ld.state)
T = len(ld.trains)
sites = s.a.shape[1]
D = int(lay.click.key[0, 0])
held_t, giver_t, taker_t = 2, 3, 4  # the click world's triangle, its trains sorted (2 < 3 < 4)
pairs = [(held_t, giver_t), (giver_t, taker_t), (held_t, taker_t)]  # circ's Edges order (ga, ab, gb): signs +1, +1, -1
csign = [1, 1, -1]


class Ed:
    def __init__(self, dial):
        self.pairs = pairs
        self.dial = dial
        self.triangles = [(0, 1, 2)]


st_ = circ.Stepper(Ed(D))
D3, B3 = st_.D3, st_.B3
BD, _ = carry(D - 1, 2, 0)


def cen3(v):
    return carry(v + B3, D3, 0)[1] - B3


def cenD(v):
    return carry(v + BD, D, 0)[1] - BD


# the Stepper's state per Node-clock, and the small member's: (g0, g1, tau, eta) with eta on D
full = [st_.born() for _ in range(sites)]
small = [[B3, B3, B3, BD] for _ in range(sites)]
off = {"c.g not 0 mod 3D (site-rounds)": 0, "quanta apart (edge-site-rounds)": 0, "landings apart (site-rounds)": 0}
landings, quanta_nonzero = 0, 0
passes = []


def small_round(m, fl):
    g0, g1, tau, eta = m
    y = fl[0] + fl[1] - fl[2]
    p = [3 * fl[e] - csign[e] * y for e in range(3)]
    eta = BD + cenD(eta - BD + 3 * (tau - B3))
    tau = B3 + cen3(tau - B3 + 3 * (eta - BD))
    g2 = B3 + cen3((g0 - B3) + (g1 - B3))  # the cocycle law: c . g = 0 mod 3D, born at the middle
    q0, g0 = carry(p[0], D3, g0)
    q1, g1 = carry(p[1], D3, g1)
    q2, _ = carry(p[2], D3, g2)
    w, tau = carry(y, D3, tau)
    tau = B3 + cen3(tau - B3 + 3 * (eta - BD))
    eta = BD + cenD(eta - BD + 3 * (tau - B3))
    return [g0, g1, tau, eta], [q0 + w, q1 + w, q2 - w], w


for at in range(1, rounds + 1):
    s1, _ = step.act(lay, s)
    P = step.passing(lay.click, lay.plan, s.b, s.a, s1.a)  # (T T, sites), side (t, u) at t T + u
    fls = [[int(P[t * T + u, x]) for t, u in pairs] for x in range(sites)]
    passes.append(fls)
    for x in range(sites):
        gs, ts, es = full[x]
        qe = st_.step(fls[x], gs, ts, es)
        w_full = st_.last_w[0]
        cg = sum(csign[e] * (gs[e] - B3) for e in range(3))
        off["c.g not 0 mod 3D (site-rounds)"] += int(carry(cg, D3, 0)[1] != 0)
        small[x], qs, w = small_round(small[x], fls[x])
        off["quanta apart (edge-site-rounds)"] += sum(int(qe[e] != qs[e]) for e in range(3))
        off["landings apart (site-rounds)"] += int(w != w_full)
        landings += int(w != 0)
        quanta_nonzero += sum(int(v != 0) for v in qs)
        assert small[x][0] == gs[0] and small[x][1] == gs[1] and small[x][2] == ts[0]
    s = s1
# the small member's run back from its end alone, every Node-clock
back_ok = 0
for x in range(sites):
    g0, g1, tau, eta = small[x]
    m = [g0, g1, tau, D - 1 - eta]
    for at in range(rounds - 1, -1, -1):
        m, _, _ = small_round(m, [-v for v in passes[at][x]])
    m = [m[0], m[1], m[2], D - 1 - m[3]]
    back_ok += int(m == [B3, B3, B3, BD])
print("MEMBER on", world.name, ",", rounds, "rounds,", sites, "Node-clocks; edge dial D", D, "; 3D", D3)
print("  the member's state per triangle: Big Pic's three edge teeth on 3D, tau on 3D, twin on 3D (THIRD9: on D);",
      "the small member: two edge teeth and tau on 3D, the twin on D, four numbers")
print("  checks:", off, "; landings", landings, "; side quanta not 0", quanta_nonzero)
print("  the small member's run back from its end alone reaches the birth at", back_ok, "of", sites, "Node-clocks")
print("END")
