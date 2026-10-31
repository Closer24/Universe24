"""MASS2 probe 4: the designs' thresholds on the held count, read by the engine's own act (node-all 9d75a4904,
mass2/tree) on test lays of one Node-clock. Each is a test's lay, never a shipped world: a shipped world's universe
file read as it stands (no strength changed), its setting replaced by the gears named, on one Node-clock (the shape's
sides read as 1, so no Mesh reaches another Node-clock). Clock facts only.

  (a) the lone member: the mesh world's files (one held hand, one tied train, the tie between two tied trains absent
      as filed); the held hand laid at 0, the tied train's first row laid moving one count a round (now 41, before 40);
  (b) the lone member with the held hand laid at 1 at rest and the tied row at 40 at rest;
  (c) the pair: the click world's files; the held hand laid at 0, the giver's first row at 40 at rest, the taker at 0.

Read: the held |k|^2, the tied rows, the potential's value V (SUM over the loader's monomials of the factor times its
legs), and for (c) the pair's sum u and difference v. Whole numbers only; Rule3's carry the one division.
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


def one_node(world, gears):
    folder = TREE.joinpath("examples", world)
    universe = json.loads(folder.joinpath("universe.json").read_text())
    piece = json.loads(folder.joinpath("piece.json").read_text())
    setting = json.loads(folder.joinpath("setting.json").read_text())
    one = [1 for _ in piece["shape"]]
    spokes = files.star(len(one))
    turned, c, square, lifted = tmain.made(spokes)
    loaded, laid = load.load(universe, {**setting, "gears": gears}, files.sites_of(one), turned, c, square, lifted)
    assert not laid, laid
    return universe, loaded, tmain.layout(universe, one, loaded), state.State(*loaded.state)


def potential(loaded, a):
    factor, legs = loaded.potential
    total = 0
    for m in range(len(factor)):
        f = int(factor[m])
        if f:
            v = f
            for leg in legs:
                r = int(leg[m])
                v = v * (int(a[r][0]) if r >= 0 else 1)
            total = total + v
    return total


def rows_of(loaded, universe):
    tr = loaded.trains
    names = [t["name"] for t in universe["trains"]]
    held = [t for t in range(len(tr)) if tr.held[t]][0]
    tied = [t for t in range(len(tr)) if tr.tied[t]]
    span = lambda t: range(int(tr.first[t]), int(tr.first[t] + tr.size[t]))  # noqa: E731
    return names, held, tied, span


def run(label, world, gears, rounds, every):
    universe, loaded, layout, s = one_node(world, gears)
    names, held, tied, span = rows_of(loaded, universe)
    width = universe["integers"]["width"]
    print(f"\n({label}) {world} on one Node-clock, gears {gears}; held {names[held]}, tied {[names[t] for t in tied]}")
    k2 = lambda s: sum(int(s.a[r][0]) ** 2 for r in span(held))  # noqa: E731
    first = [int(next(iter(span(t)))) for t in tied]
    zeros, most_k2, extreme = 0, 0, [[0, 0] for _ in tied]
    for r in range(1, rounds + 1):
        s, _ = step.act(layout, s)
        widest = max(abs(int(v)) for v in np.asarray(s.a).reshape(-1))
        if widest.bit_length() > width:
            print(f"  a count passes the width after round {r}")
            break
        q = k2(s)
        zeros = zeros + int(q == 0)
        most_k2 = max(most_k2, q)
        for i, row in enumerate(first):
            v = int(s.a[row][0])
            extreme[i] = [min(extreme[i][0], v), max(extreme[i][1], v)]
        if r % every == 0:
            xs = [int(s.a[row][0]) for row in first]
            extra = f" | u {xs[0] + xs[1]} | v {xs[0] - xs[1]}" if len(xs) > 1 else ""
            print(f"  round {r}: held |k|^2 {q} | tied first rows {xs}{extra} | V {potential(loaded, s.a)}")
    print(f"  over the rounds read: the held |k|^2 most {most_k2}, at 0 in {zeros} rounds; the tied first rows' least"
          f" and most {extreme}")


def main() -> None:
    run("a", "tensor24-mesh", [[2, 0, 0, 41, 40, 0]], 1000, 100)
    run("b", "tensor24-mesh", [[1, 0, 0, 1, 1, 0], [2, 0, 0, 40, 40, 0]], 2000, 250)
    run("c", "tensor24-click", [[3, 0, 0, 40, 40, 0]], 1000, 100)


if __name__ == "__main__":
    main()
