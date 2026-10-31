"""MASS2 probe 5: the shipped click world's beat, by the engine's own act (node-all 9d75a4904, mass2/tree).

- First a check that one Node-clock reads the cube's site 0: the click world's files on one Node-clock (site 0's gears;
  the 27 are laid alike) against the 27-site cube itself, every count, tooth and click of site 0 alike in each of the
  first C rounds (C the second argument).
- Then the one Node-clock up to R rounds (the first argument; the setting's ticks are 5,000), stopped when a count
  passes the width, and read on the board (clock facts): per 250 rounds the held |k|^2 (its most, its rounds at 0, its
  sum), and the tied pair's sum u and difference v on their first rows (most |u|, most |v|); the sign changes of u and
  of v, each against the last count not 0, as half-beats.
- In the clicks at that Node-clock: each clock's own lines, as the record writes them (a round in which one of its
  sides carried, q not 0: its line not silent), and its side landings (sides with q not 0, one per side per round,
  MASS1's count, renamed), in windows of one whole beat of u (between every second sign change), and M1 across
  consecutive whole-beat windows: |n1 m2 - n2 m1| against n1 + m1 + n2 + m2, for each pair of clocks, and for each
  clock against its window's rounds (a board count: so a drift that two clocks share shows). The windows are bounded
  by a board beat, so this is a board check beside a click reading, named so.
Whole numbers only; Rule3's carry the one division.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE = HERE.parent.joinpath("tree")
sys.path.insert(0, str(TREE.joinpath("src")))

import numpy as np  # noqa: E402

from tensor24 import main as tmain  # noqa: E402
from tensor24.engine import state, step  # noqa: E402
from tensor24.runner import files, load  # noqa: E402


def build(universe, piece, setting, shape, gears):
    spokes = files.star(len(shape))
    turned, c, square, lifted = tmain.made(spokes)
    loaded, laid = load.load(universe, {**setting, "gears": gears}, files.sites_of(shape), turned, c, square, lifted)
    assert not laid, laid
    return loaded, tmain.layout(universe, shape, loaded), state.State(*loaded.state)


def main() -> None:
    rounds, check = int(sys.argv[1]), int(sys.argv[2])
    folder = TREE.joinpath("examples", "tensor24-click")
    universe = json.loads(folder.joinpath("universe.json").read_text())
    piece = json.loads(folder.joinpath("piece.json").read_text())
    setting = json.loads(folder.joinpath("setting.json").read_text())
    one = [1 for _ in piece["shape"]]
    site0 = [g for g in setting["gears"] if g[2] == 0]
    loaded, layout, s = build(universe, piece, setting, one, site0)
    cube_loaded, cube_layout, cs = build(universe, piece, setting, piece["shape"], setting["gears"])
    nt = len(loaded.trains)
    alike = True
    for r in range(check):
        s, q1 = step.act(layout, s)
        cs, qc = step.act(cube_layout, cs)
        for x, y in zip(s, cs):
            alike = alike and bool((np.asarray(x)[:, 0] == np.asarray(y)[:, 0]).all())
        own = nt * nt
        alike = alike and bool((np.asarray(q1)[:own, 0] == np.asarray(qc)[:own, 0]).all())
    print(f"one Node-clock against the 27-site cube's site 0, every count, tooth and own click over {check} rounds:"
          f" {'alike' if alike else 'APART'}")
    # the long run, from the lay again
    loaded, layout, s = build(universe, piece, setting, one, site0)
    tr = loaded.trains
    names = [t["name"] for t in universe["trains"]]
    held = [t for t in range(nt) if tr.held[t]][0]
    tied = [t for t in range(nt) if tr.tied[t]]
    hrows = range(int(tr.first[held]), int(tr.first[held] + tr.size[held]))
    g0, t0 = int(tr.first[tied[0]]), int(tr.first[tied[1]])
    width = universe["integers"]["width"]
    k2s, us, vs, lines, lands = [], [], [], [], []
    done = 0
    for r in range(1, rounds + 1):
        s, q = step.act(layout, s)
        widest = max(abs(int(v)) for v in np.asarray(s.a).reshape(-1))
        if widest.bit_length() > width:
            print(f"a count passes the width after round {r} (its bit length {widest.bit_length()}); read to round {r - 1}")
            break
        done = r
        k2s.append(sum(int(s.a[x][0]) * int(s.a[x][0]) for x in hrows))
        us.append(int(s.a[g0][0]) + int(s.a[t0][0]))
        vs.append(int(s.a[g0][0]) - int(s.a[t0][0]))
        side = np.asarray(q)[: nt * nt, 0].reshape(nt, nt)
        lines.append([int(any(side[t][u] != 0 for u in range(nt))) for t in range(nt)])
        lands.append([sum(1 for u in range(nt) if side[t][u] != 0) for t in range(nt)])
    print(f"rounds read: {done} | the held |k|^2: least {min(k2s)}, most {max(k2s)}")
    print("per 250 rounds: the held |k|^2 most, at 0, summed | most |u| | most |v|")
    for at in range(0, done, 250):
        part = k2s[at:at + 250]
        print(f"  {at + 1:5d} to {at + len(part):5d}: |k|^2 most {max(part):3d}, at 0 in {sum(1 for v in part if v == 0):3d},"
              f" summed {sum(part):5d} | |u| most {max(abs(v) for v in us[at:at + 250]):6d}"
              f" | |v| most {max(abs(v) for v in vs[at:at + 250]):6d}")

    def flips(xs):
        out, last = [], 0
        for i, v in enumerate(xs):
            if v != 0:
                if last != 0 and (v > 0) != (last > 0):
                    out.append(i + 1)
                last = v
        return out

    for label, xs in (("u", us), ("v", vs)):
        f = flips(xs)
        half = [b - a for a, b in zip(f, f[1:])]
        print(f"{label}: {len(f)} sign changes, the first at {f[:1]}; half-beats {half}")
    fu = flips(us)
    bounds = fu[::2]
    windows = list(zip(bounds, bounds[1:]))
    print(f"whole beats of u (between every second sign change): {len(windows)}")
    live = [t for t in range(nt) if sum(x[t] for x in lines)]
    rows_ = []
    for a, b in windows:
        ln = [sum(lines[i][t] for i in range(a, b)) for t in range(nt)]
        ld = [sum(lands[i][t] for i in range(a, b)) for t in range(nt)]
        km = max(k2s[a:b])
        rows_.append((a, b, ln, ld, km))
        print(f"  rounds {a + 1} to {b}: {b - a} rounds | held |k|^2 most {km} | own lines "
              f"{[(names[t], ln[t]) for t in live]} | side landings {[(names[t], ld[t]) for t in live]}")

    def m1(n1, m1_, n2, m2):
        gap, cal = abs(n1 * m2 - n2 * m1_), n1 + m1_ + n2 + m2
        return f"{gap}/{cal} {'holds' if gap <= cal else 'FAILS'}"

    print("M1 across consecutive whole beats, own lines, each pair of clocks:")
    for i in range(len(live)):
        for j in range(i + 1, len(live)):
            x, y = live[i], live[j]
            print(f"  {names[x]} : {names[y]}: "
                  f"{[m1(rows_[w][2][x], rows_[w][2][y], rows_[w + 1][2][x], rows_[w + 1][2][y]) for w in range(len(rows_) - 1)]}")
    print("M1 across consecutive whole beats, each clock's own lines against its window's rounds (a board count):")
    for x in live:
        print(f"  {names[x]}: "
              f"{[m1(rows_[w][2][x], rows_[w][1] - rows_[w][0], rows_[w + 1][2][x], rows_[w + 1][1] - rows_[w + 1][0]) for w in range(len(rows_) - 1)]}")


if __name__ == "__main__":
    main()
