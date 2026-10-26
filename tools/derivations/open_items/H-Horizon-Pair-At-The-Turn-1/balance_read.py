"""hp1: the carrier's balance at one Node from birth_read.py's lines: per interval X, the free line 2 now - before, the Link term SUM_j R_ij (X_j - X) div w at the Node's own pace with Q = G^2 on every Link (the bound: a tension lowers Q), the mass term -D X div w, and the residual X_next - free - link - mass (the write's quotient q with the tensions' shortfall of the Link term). Usage: balance_read.py <src> <world.json> <lines.jsonl> <node a,b,c> <from> <to>"""
import json, sys
import numpy as np
sys.path.insert(0, sys.argv[1]); sys.set_int_max_str_digits(0)
from event_universe.loader.world import load_world
from event_universe.node import Node
from event_universe.core import paces, rule3
u, w = load_world(sys.argv[2]); node = Node(u, w); cube = node.cube
at = tuple(int(x) for x in sys.argv[4].split(",")); lo, hi = int(sys.argv[5]), int(sys.argv[6])
num, den = node.row(10).pair if False else next(r.pair for r in node.rows_ if r.shape == 10)
nb = []
for a in range(3):
    for s in (1, -1):
        m = list(at); m[a] = (m[a] + s) % cube; nb.append(tuple(m))
seen = {}
for l in open(sys.argv[3]):
    r = json.loads(l)
    if "nodes" not in r or not (lo <= r["i"] <= hi + 1): continue
    seen[r["i"]] = {tuple(e["node"]): e for e in r["nodes"]}
print("node", at, "num", num, "den", den, "w", node.w, "G", node.G)
print("i content frozen released X | free(2now-before) link_term mass_term | X_next-X residual(q+tension shortfall) | 6R/w per million D/w per million")
prev = None
for i in sorted(seen):
    e = seen[i].get(at)
    if e is None: prev = None; continue
    X = e["X"]; c = e["content"]
    clock, pace = int(paces.clock_of(node.gamma, np.array([c], dtype=object))[0]), int(paces.link_pace_of(node.gamma, np.array([c], dtype=object))[0])
    rule = rule3.rule_integers(num, den, node.gamma, clock, pace, None, node.G)
    R = int(rule.reaches[0]); D = int(rule.mass); W = int(rule.wall)
    xs = [seen[i][n]["X"] for n in nb if n in seen[i]]
    link = sum(R * (xj - X) for xj in xs) // W if len(xs) == 6 else None
    mass = -(D * X) // W
    nxt = seen.get(i + 1, {}).get(at)
    if prev is not None and nxt is not None and link is not None and not e["frozen"]:
        free = 2 * X - prev
        res = nxt["X"] - free - link - mass
        print(i, c, e["frozen"], e["released"], X, "|", free, link, mass, "|", nxt["X"] - X, res, "|", 6 * R * 1000000 // W, D * 1000000 // W)
    else:
        print(i, c, e["frozen"], e["released"], X, "| (no line: frozen, or no before/next/neighbours)", "6R/w ppm", 6 * R * 1000000 // W, "D/w ppm", D * 1000000 // W, "neighbours X", xs)
    prev = X
