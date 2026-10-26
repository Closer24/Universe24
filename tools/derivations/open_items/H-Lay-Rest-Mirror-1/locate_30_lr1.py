"""lr1: the C P mirror state of the chiral 3-cube under the z reflection stepped beside the base to N with the flags from the environment; at each interval the count of (line, Node) entries whose level or remainder is not the base's C P image, the first named (line kind, Node, base, image, wall). Usage: locate_30_lr1.py <src> <worktree> <N>"""
import json
import os
import sys

import numpy as np

sys.argv = sys.argv[:4] + ["/dev/null"]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "run_48_lr1.py")).read().split("if __name__")[0])
m = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -1]])
base = Node(json.loads(json.dumps(universe)), world)
img = mirror_state(base, m)
table = line_signs(base, m)
for t in range(N):
    base.step(); img.step()
    lb, li_ = base.all_lines(), img.all_lines()
    bad = []
    for li, (lj, s) in enumerate(table):
        src, dst = lb[li], li_[lj]
        for x in np.ndindex(*base.shape):
            gx = image(m, x)
            for name in ("now", "before", "rem"):
                a, b = int(getattr(src, name)[x]), int(getattr(dst, name)[gx])
                if name == "rem":
                    w = int(src.wall[x]) if isinstance(src.wall, np.ndarray) else int(src.wall)
                    want = w - 1 - a if s == -1 and w != 2 else a
                else:
                    want = s * a
                if want != b:
                    bad.append((li, name, list(x), a, b, want))
    if bad:
        print("interval", base.interval, "entries apart", len(bad), "first", bad[:4])
        for nd, nm in ((base, "base"), (img, "img")):
            print(" ", nm, [json.dumps(e, default=str)[:160] for e in nd.log if e["i"] == base.interval and e["event"] != "credit"][:6])
        break
    if base.interval in (5, 10, 20, 29):
        print("interval", base.interval, "0 apart")
