"""Stage 3 for writer C (#2187): the three clicks written as records in schema 1.4's sides shape, and read back.

Each line is (round, site, train, q, sides), q the sum of its sides; each side is [partner, q_side, k_before,
k_after], both ends of every edge written, the far end's teeth the complement (dial - 1 - k). k_before is the tooth
the carry reads (after the turn's first half, in the palindromes), k_after the tooth the carry leaves. The reader
refuses by name a side without its partner, a pair of sides whose quotients do not sum to 0, and a pair of teeth
that do not sum to dial - 1; and it reads each side's weight with no new field, by the carry's own law:
x = dial q + k_after - k_before. The twins, the turn's hidden teeth, are written nowhere: the draw reads what no
click line shows (the law of the choice, item 2 of Big Pic's 6538736766).

Usage: python3 -I record14.py <src> <world> <rounds> <mode 0 to 5> [laid] <out.jsonl>
"""

import json
import sys

sys.path.insert(0, sys.argv[1])
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import step  # noqa: E402

src, world_dir, rounds, mode = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
flags = sys.argv[5] if len(sys.argv) > 6 else ""
out_path = sys.argv[-1]
universe, shape, held, lay, s, world = E.load_world(src, world_dir)
if "laid" in flags:
    s = E.board_lay(s, shape, world)
rows, sites = s.a.shape
edges = E.Edges(world, int(lay.click.key[0, 0]), sites, [t["kinds"] for t in universe["trains"]])
dial = edges.dial
lines = []
for t in range(rounds):
    s1, _ = step.act(lay, s)
    for x in range(sites):
        b = [int(s.b[r, x]) for r in range(rows)]
        a = [int(s.a[r, x]) for r in range(rows)]
        a1 = [int(s1.a[r, x]) for r in range(rows)]
        fl = world.split_flows(0, b, a, a1)
        u, w = edges.teeth[x], edges.twins[x]
        if mode >= 2:
            edges.shear_all(u, w, edges.forward(mode))
        elif mode == 1:
            edges.turn(u)
        sides = {tr: [] for tr in world.trains}
        for e, pr in enumerate(edges.pairs):
            k_before = u[e]
            c, u[e] = carry(fl.get(pr, 0), dial, u[e])
            k_after = u[e]
            if c:
                sides[pr[0]].append([pr[1], c, k_before, k_after])
                sides[pr[1]].append([pr[0], -c, dial - 1 - k_before, dial - 1 - k_after])
        if mode >= 2:
            edges.shear_all(u, w, edges.backward(mode))
        for tr in world.trains:
            if sides[tr]:
                lines.append({"round": t, "site": x, "train": tr, "q": sum(sd[1] for sd in sides[tr]), "sides": sides[tr]})
    s = s1
header = {"kind": "header", "world": world_dir, "shape": shape, "trains": world.trains, "edges": edges.pairs,
          "key": int(lay.click.key[0, 0]), "dial": dial, "born": edges.born, "mode": E.NAMES[mode],
          "rounds": rounds, "laid": flags}
with open(out_path, "w") as f:
    f.write(json.dumps(header) + "\n")
    for ln in lines:
        f.write(json.dumps(ln) + "\n")

# the reader, generic, on the record alone
got = [json.loads(x) for x in open(out_path)]
head, body = got[0], got[1:]
d = head["dial"]
by = {(ln["round"], ln["site"], ln["train"]): ln for ln in body}
refused = {"no partner": 0, "quotients not 0": 0, "teeth not dial - 1": 0, "q not the sum of its sides": 0}
weights = {}
for ln in body:
    if ln["q"] != sum(sd[1] for sd in ln["sides"]):
        refused["q not the sum of its sides"] += 1
    for partner, qs, kb, ka in ln["sides"]:
        other = by.get((ln["round"], ln["site"], partner))
        mate = [sd for sd in (other["sides"] if other else []) if sd[0] == ln["train"]]
        if not mate:
            refused["no partner"] += 1
            continue
        _, qm, kbm, kam = mate[0]
        refused["quotients not 0"] += int(qs + qm != 0)
        refused["teeth not dial - 1"] += int(kb + kbm != d - 1 or ka + kam != d - 1)
        if ln["train"] < partner:
            key = (ln["train"], partner)
            weights[key] = weights.get(key, 0) + d * qs + ka - kb
places = {(ln["round"], ln["site"]) for ln in body}
sums = {}
for ln in body:
    sums[(ln["round"], ln["site"])] = sums.get((ln["round"], ln["site"]), 0) + ln["q"]
books_open = sum(1 for v in sums.values() if v != 0)
print(f"{world_dir}, {head['mode']}, {rounds} rounds{', ' + flags if flags else ''}: {len(body)} lines written to {out_path}")
print(f"  the reader on the record alone: refusals {refused}; click places {len(places)}, the books open at {books_open}")
print(f"  each edge's booked weight read from its sides by the carry's law (x = dial q + k_after - k_before), summed: {weights}")
