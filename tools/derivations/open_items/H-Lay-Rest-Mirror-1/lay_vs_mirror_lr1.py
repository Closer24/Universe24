"""lr1, part (A) measured at the interval 0: the reflected FILE's laid state against the C P mirror of the base's laid state (the sign table; every odd line's remainder W - 1 - r), for every one of the 48 on the chiral 3-cube and on ga2's cycle seed: the count of (line, Node) entries apart, split into levels and remainders, and the odd lines' remainders at the lay (half or its mirror). Usage: lay_vs_mirror_lr1.py <src> <worktree> <out.json>"""
import json
import os
import sys

import numpy as np

sys.argv = sys.argv[:3] + ["0", sys.argv[3]]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_48_lr1.py")).read().split("if __name__")[0])


def apart(base, by_file, m):
    table = line_signs(base, m)
    lb, lf = base.all_lines(), by_file.all_lines()
    lev = rem = 0
    zero_odd_rem = 0
    for li, (lj, s) in enumerate(table):
        src, dst = lb[li], lf[lj]
        for x in np.ndindex(*base.shape):
            gx = image(m, x)
            if s * int(src.now[x]) != int(dst.now[gx]) or s * int(src.before[x]) != int(dst.before[gx]):
                lev += 1
            w = int(src.wall[x]) if isinstance(src.wall, np.ndarray) else int(src.wall)
            want = (w - 1 - int(src.rem[x])) if s == -1 else int(src.rem[x])
            if want != int(dst.rem[gx]):
                rem += 1
                if int(src.now[x]) == 0 and int(src.before[x]) == 0:
                    zero_odd_rem += 1
    return lev, rem, zero_odd_rem


out = {}
for name, (u, w, cube) in {"chiral_3cube": (universe, world, 3), "ga2": load_world(root + "/tests/worlds/world_ga2.json") + (4,)}.items():
    CUBE = cube
    universe, world = u, w
    base = Node(json.loads(json.dumps(u)), w)
    rows = []
    for m in IMAGES:
        by_file = Node(json.loads(json.dumps(u)), world_image(w, m))
        lev, rem, z = apart(base, by_file, m)
        rows.append({"det": det_of(m), "levels apart": lev, "rems apart": rem, "rems apart on zero lines": z})
    out[name] = {"rotations": [r for r in rows if r["det"] == 1], "reflections": [r for r in rows if r["det"] == -1]}
    summ = {k: {"images": len(v), "levels apart (min,max)": [min(r["levels apart"] for r in v), max(r["levels apart"] for r in v)], "rems apart (min,max)": [min(r["rems apart"] for r in v), max(r["rems apart"] for r in v)], "rems apart on zero lines (min,max)": [min(r["rems apart on zero lines"] for r in v), max(r["rems apart on zero lines"] for r in v)]} for k, v in out[name].items()}
    print(name, json.dumps({"flags": {k: os.environ.get(k) for k in ("LR1_PICK", "LR1_LAY")}, **summ}))
json.dump(out, open(sys.argv[4], "w"))
