"""David's word on the law's line (#2187 6540015705 item 4), read on the click world: a clock's line under the third
click's form against the first click's, round by round and over the run, and under one hidden unit in a triangle's
twin. Whole numbers only.

Usage: python3 -I lineform.py <src> <world> <rounds>
"""
import sys

src, world, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, src)
sys.path.insert(0, ".")
import edgeclick as E  # noqa: E402

first = E.run(src, world, rounds, 0)
third = E.run(src, world, rounds, 11)
hid = E.run(src, world, rounds, 11, hidden=(0, 0))


def by_key(run):
    out = {}
    for (t, x, tr, v) in run["lines"]:
        out[(t, x, tr)] = out.get((t, x, tr), 0) + v
    return out


L1, L3, LH = by_key(first), by_key(third), by_key(hid)
keys = sorted(set(L1) | set(L3) | set(LH))
differ = sum(1 for k in keys if L1.get(k, 0) != L3.get(k, 0))
moved = sum(1 for k in keys if L3.get(k, 0) != LH.get(k, 0))
tot1, tot3 = {}, {}
for (t, x, tr), v in L1.items():
    tot1[(x, tr)] = tot1.get((x, tr), 0) + v
for (t, x, tr), v in L3.items():
    tot3[(x, tr)] = tot3.get((x, tr), 0) + v
clocks = sorted(set(tot1) | set(tot3))
gap = [abs(tot1.get(c, 0) - tot3.get(c, 0)) for c in clocks]
s3 = {(t, x, e): c for (t, x, e, c) in third["sides"]}
sh = {(t, x, e): c for (t, x, e, c) in hid["sides"]}
sides_moved = sum(1 for k in set(s3) | set(sh) if s3.get(k, 0) != sh.get(k, 0))
print(f"world {world} | rounds {rounds} | (Node-clock, round, train) lines with a click, either form: {len(keys)}")
print(f"the third click's form against the first click: {differ} lines differ round by round")
print(f"each clock's total over the run: {len(clocks)} clocks, the most any differs: {max(gap) if gap else 0}")
print(f"one hidden unit in the twin at Node-clock 0: {moved} lines move, {sides_moved} sides move")
