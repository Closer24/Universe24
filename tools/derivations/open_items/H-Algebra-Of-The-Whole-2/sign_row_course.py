"""The sign row's write against the retrace (PL-S1's locus) on the uniform 3-cubes: per interval, at the Node (0, 0, 0), the carrier's X, the shape-4 row's time line level and its write remainder, the gapped rows' charges W at the Node and their sum (the write's numerator 2 W_after), the potential's momentum; the first interval the level moves; and the mirror of X about the top. A reader of the engine's state, no act changed; integers only."""
import json
import sys

from event_universe.rows import CARRIER, POTENTIAL
from tests.laws import node_of
from event_universe import gram

sys.set_int_max_str_digits(0)
AT = (0, 0, 0)
for name, n in (("world_plasma_3.json", 100), ("world_universe_3.json", 110), ("world_pair_3.json", 100)):
    node = node_of(name)
    rows = []
    for t in range(1, n + 1):
        node.step()
        x = node.row(CARRIER).lines[0]
        phi = node.row(POTENTIAL).lines[0]
        ws = [int(gram.charge(r.shape, r.lines)[AT]) for r in node.records() if r.gap]
        rows.append((t, int(x.now[AT]), int(phi.now[AT]), int(phi.wr[AT]), ws, sum(ws), int(node.turned[AT])))
    moved = [t for t, x, lvl, wr, ws, s, turned in rows if lvl != 0]
    top = [t for t, x, lvl, wr, ws, s, turned in rows if turned][0]
    centre = top - 1
    j = 1
    xs = {t: x for t, x, *_ in rows}
    while centre - j >= 1 and centre + j in xs and xs[centre + j] == xs[centre - j]:
        j += 1
    levels_after_top = [(t, lvl) for t, x, lvl, wr, ws, s, turned in rows if t >= top - 2][:14]
    print(json.dumps({"world": name, "top": top, "X mirror holds for j up to": j - 1, "parts at": centre + j, "first interval the sign level moves": moved[:1], "sign level and X at a few intervals": [(t, x, lvl, wr, s) for t, x, lvl, wr, ws, s, turned in rows if t in (1, 2, 8, 16, 24, 32, top - 1, top, top + 1, top + 8, top + 9, top + 10, top + 11)], "W per row at 1": rows[0][4], "W per row at the top": [r[4] for r in rows if r[0] == top][0], "W per row after the top": [r[4] for r in rows if r[0] == top + 1][0], "T": node.T}))
