import json, sys, subprocess
# the law's own reading for one clock on the real act: one hidden unit in one edge tooth at one Node-clock
src, world, rounds = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, src); sys.path.insert(0, ".")
import edgeclick as E
for turned in (0, 1):
    a = E.run(src, world, rounds, turned)
    b = E.run(src, world, rounds, turned, hidden=(0, 1))
    la, lb = set(map(tuple, a["lines"])), set(map(tuple, b["lines"]))
    diff = sorted(la ^ lb)
    first = diff[0][0] if diff else None
    at = sorted({d[1] for d in diff})
    print(f"{world} {'turned' if turned else 'carried'}: books open {a['books_open']} of {a['places']}; run back {a['runback']};"
          f" one hidden unit in edge 1 at Node-clock 0: {len(diff)} click lines differ, the first at round {first}, at Node-clocks {at}")
