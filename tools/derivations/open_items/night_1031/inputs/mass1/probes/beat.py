"""MASS1 probe 3: the shipped click world run by the engine's own act (node-all 9d75a4904, the read-only copy in
mass1/tree), one Node-clock read (the 27 are laid alike): on the board, the held hand's |k|^2, which sets the tied
trains' curvature 2 hold f |k|^2 (plans.py's "beat"), round by round; in the clicks, each clock's own lines at that
Node-clock (its sides on its own Node-clock with a quotient not 0), summed over two windows of equal rounds, and the
two-window check of their ratios by cross-multiplication. The windows are bounded by rounds, a board count: this is a
board check set beside a click reading, named so, since no light link bounds a window on this world.

Whole numbers only; Rule3's carry the one division; the rounds read are the first R of the setting's ticks, R the
argument (the engine runs away after round 3751 on this world, MIRACLE_A).
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE = HERE.parent.joinpath("tree")
sys.path.insert(0, str(TREE.joinpath("src")))

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import state, step  # noqa: E402
from tensor24.runner import files, load  # noqa: E402


def main() -> None:
    rounds = int(sys.argv[1])
    folder = TREE.joinpath("examples", "tensor24-click")
    universe = json.loads(folder.joinpath("universe.json").read_text())
    piece = json.loads(folder.joinpath("piece.json").read_text())
    setting = json.loads(folder.joinpath("setting.json").read_text())
    spokes = files.star(len(piece["shape"]))
    turned, c, square, lifted = tmain.made(spokes)
    loaded, laid = load.load(universe, setting, files.sites_of(piece["shape"]), turned, c, square, lifted)
    layout = tmain.layout(universe, piece["shape"], loaded)
    s = state.State(*loaded.state)
    trains = loaded.trains
    names = [t["name"] for t in universe["trains"]]
    nt = len(trains)
    f, _ = carry(load.teeth(universe, spokes)[1], universe["integers"]["full_rate"], 0)
    c_ = universe["chosen"]["hold"] * f
    held = [t for t in range(nt) if trains.held[t]]
    lo, hi = int(trains.first[held[0]]), int(trains.first[held[0]] + trains.size[held[0]])
    half, _ = carry(rounds, 2, 0)
    own = [[0] * nt, [0] * nt]
    k2s = []
    for r in range(rounds):
        s, clicks = step.act(layout, s)
        q = np.asarray(clicks)[: nt * nt, 0].reshape(nt, nt)  # the sides at its own Node-clock, site 0
        w = int(r >= half)
        for t in range(nt):
            own[w][t] = own[w][t] + sum(1 for u in range(nt) if q[t][u] != 0)
        k2s.append(sum(int(s.a[x][0]) * int(s.a[x][0]) for x in range(lo, hi)))
        widest = max(abs(int(v)) for v in np.asarray(s.a).reshape(-1))
        if widest.bit_length() > universe["integers"]["width"]:
            print("past the width at round", r + 1)
            break
    print("rounds read:", len(k2s), "| sites alike at the end:",
          all((np.asarray(s.a)[:, i] == np.asarray(s.a)[:, 0]).all() for i in range(np.asarray(s.a).shape[1])))
    print("held |k|^2 at Node-clock 0: first", k2s[0], "| least", min(k2s), "| most", max(k2s), "| last", k2s[-1])
    for cut in range(0, len(k2s), max(1, carry(len(k2s), 10, 0)[0])):
        print(f"  round {cut + 1}: |k|^2 {k2s[cut]} | the tied curvature 2 c |k|^2 = {2 * c_ * k2s[cut]}")
    print("own lines (sides with a quotient not 0) per clock at Node-clock 0, in two windows of", half, "rounds:")
    for t in range(nt):
        print(f"  {names[t]:7s} first window {own[0][t]:6d} | second window {own[1][t]:6d}")
    print("two-window check of the ratios, |n1 m2 - n2 m1| against the calibre n1 + m1 + n2 + m2 (fails if above):")
    live = [t for t in range(nt) if own[0][t] + own[1][t]]
    for i in range(len(live)):
        for j in range(i + 1, len(live)):
            a_, b_ = live[i], live[j]
            gap = abs(own[0][a_] * own[1][b_] - own[1][a_] * own[0][b_])
            cal = own[0][a_] + own[0][b_] + own[1][a_] + own[1][b_]
            print(f"  {names[a_]} : {names[b_]}: gap {gap}, calibre {cal}: {'holds' if gap <= cal else 'FAILS'}")


if __name__ == "__main__":
    main()
