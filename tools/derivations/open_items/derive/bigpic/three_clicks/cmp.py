"""The law's own reading for one clock on the real act (R2): one hidden unit in one edge tooth at Node-clock 0, every
click before alike, and a later click differs in the third click, none in the first; run for each edge in turn.

Usage: python3 -I cmp.py <src> <world> <rounds> [modes, e.g. 034] [laid]
"""
import sys
src, world, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
modes = [int(m) for m in (sys.argv[4] if len(sys.argv) > 4 else "012")]
laid = len(sys.argv) > 5 and "laid" in sys.argv[5]
sys.path.insert(0, src); sys.path.insert(0, ".")
import edgeclick as E
for turned in modes:
    a = E.run(src, world, rounds, turned, laid=laid)
    print(f"{world}{', laid' if laid else ''}, {E.NAMES[turned]}: books open {a['books_open']} of {a['places']}; run back {a['runback']}")
    for e, pr in enumerate(a["pairs"]):
        b = E.run(src, world, rounds, turned, hidden=(0, e), laid=laid)
        la, lb = set(map(tuple, a["lines"])), set(map(tuple, b["lines"]))
        diff = sorted(la ^ lb)
        first = diff[0][0] if diff else None
        at = sorted({d[1] for d in diff})
        print(f"   one hidden unit in edge {pr}'s tooth at Node-clock 0: {len(diff)} click lines differ, the first at round {first}, at Node-clocks {at}")
