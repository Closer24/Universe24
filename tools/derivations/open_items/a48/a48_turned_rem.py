"""a48: the remainders of the C-odd non-im lines at the Nodes where the mirror relation breaks before any level parts: the seed
and its image under m run to the interval named; for every line whose image remainder is neither r nor 2 half(W) - r the Node,
whether it turned at this or the former interval, r, r*, W, 2 half(W) - r, W - 1 - r, and r* - (2 half(W) - r).
Usage: python a48_turned_rem.py <world.json> <cube> <interval> [mx my mz]; integers only."""
import json
import sys

import numpy as np

sys.set_int_max_str_digits(0)
from event_universe.core.rule3 import half  # noqa: E402
from event_universe.loader.world import load_world  # noqa: E402
from event_universe.node import Node  # noqa: E402

from a48_48 import image, world_image  # noqa: E402
from a48_parting import line_kinds, partner  # noqa: E402


def main(argv):
    universe, world = load_world(argv[1])
    cube, last = int(argv[2]), int(argv[3])
    diag = [int(x) for x in argv[4:7]] if len(argv) >= 7 else [-1, 1, 1]
    m = np.diag(diag).astype(int)
    eye = np.eye(3, dtype=int)
    base = Node(json.loads(json.dumps(universe)), world_image(world, eye, cube, last))
    img = Node(json.loads(json.dumps(universe)), world_image(world, m, cube, last))
    turned_before = np.zeros(base.shape, dtype=bool)
    for _ in range(last):
        turned_before = base.turned.copy()
        base.step()
        img.step()
    kinds = line_kinds(base)
    bl, il = base.all_lines(), img.all_lines()
    rows = []
    for li, kind in enumerate(kinds):
        lj, sign = partner(kinds, kind, m)
        lb, lim = bl[li], il[lj]
        for at in np.ndindex(*base.shape):
            there = image(m, at, cube)
            r, rs = int(lb.rem[at]), int(lim.rem[there])
            W = int(np.asarray(lb.wall)[at]) if np.ndim(lb.wall) else int(lb.wall)
            if rs != r and rs != 2 * int(half(W)) - r:
                rows.append({"line": list(kind), "node": list(at), "turned now": bool(base.turned[at]), "turned before": bool(turned_before[at]), "r": r, "r*": rs, "W": W, "W even": W % 2 == 0, "r* - (2 half(W) - r)": rs - (2 * int(half(W)) - r), "r* - (W - 1 - r)": rs - (W - 1 - r), "levels equal with sign": int(lim.now[there]) == sign * int(lb.now[at]) and int(lim.before[there]) == sign * int(lb.before[at])})
    print(json.dumps({"interval": last, "apart remainders": len(rows), "turned now": sum(1 for x in rows if x["turned now"]), "turned before": sum(1 for x in rows if x["turned before"]), "offsets from 2 half(W) - r": sorted({x["r* - (2 half(W) - r)"] for x in rows}), "turned Nodes now": int(base.turned.sum())}))
    for x in rows[:6]:
        print(json.dumps(x))


if __name__ == "__main__":
    main(sys.argv)
