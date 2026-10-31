"""MASS1 probe 1: the families' characters on the 48 lifts, read from the engine's own kinds.lifts and files.spun
(node-all 9d75a4904, the read-only copy in mass1/tree), and the decompositions the proton's and the electron's designs
need: three half-speed members (E1/2 cubed), the half-speed hand on the three axes (E1/2 x T1), and both restricted to
the 24 whole units (the 2T subgroup, read as the lifts whose turn permutes the axes evenly: A2 = +1).

Whole numbers only: every character is a pair (p, q) for p + q r2; products are (pr + senses qs, ps + qr); each inner
product is divided by the group's count by Rule3's carry with its remainder printed (it must be 0). No float, root,
table, search, sine or cosine. The axes are read from the click world's piece file, the count of its shape's entries.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TREE = HERE.parent.joinpath("tree")
sys.path.insert(0, str(TREE.joinpath("src")))

import numpy as np  # noqa: E402

from tensor24.algebra.carry import carry  # noqa: E402
from tensor24.engine import kinds  # noqa: E402
from tensor24.runner import files  # noqa: E402


def main() -> None:
    piece = json.loads(TREE.joinpath("examples", "tensor24-click", "piece.json").read_text())
    d = len(piece["shape"])  # the board's axes, read from the file's shape
    spokes = files.star(d)
    senses, _ = carry(len(spokes), d, 0)
    lifted = kinds.lifts(spokes)
    spun = files.spun(lifted)
    labels = tuple(n.upper().replace("_", "/") for n in (*lifted.whole._fields, *lifted.halves._fields))
    chars = spun.characters  # (kinds, senses, classes, 2): p + q r2
    nk = chars.shape[0]
    flat = chars.reshape(nk, -1, chars.shape[-1])  # (kinds, lifts, 2)
    count = flat.shape[1]
    print("lifts read:", count, "| kinds:", nk, "| labels:", " ".join(labels))

    def mul(x, y):
        p, q = x[..., 0], x[..., 1]
        r, s = y[..., 0], y[..., 1]
        return np.stack((p * r + senses * q * s, p * s + q * r), axis=-1)

    def inner(x, y, among):
        """(1/|among|) SUM over the lifts in among of x y, as (multiplicity, remainder, r2 part)."""
        prod = mul(x, y)[among]
        tot = prod.sum(axis=0)
        m, rem = carry(int(tot[0]), int(among.sum()), 0)
        return m, rem, int(tot[1])

    every = np.ones(count, dtype=bool)
    # the identity lift: T1's character 3 and E1/2's character +2 (the doubled unit's 2 Re g at the + sense)
    t1, e12 = labels.index("T1"), labels.index("E1/2")
    a2 = labels.index("A2")
    ident = [g for g in range(count) if flat[t1, g, 0] == d and flat[e12, g, 0] == senses and flat[e12, g, 1] == 0]
    print("identity lift(s) found:", ident)
    g0 = ident[0]
    dims = [int(flat[k, g0, 0]) for k in range(nk)]
    print("dimensions (character at the identity):", dict(zip(labels, dims)))
    whole_sum = sum(x * x for x, h in zip(dims, spun.half) if not h)
    all_sum = sum(x * x for x in dims)
    print("sum of squares of the five whole kinds' dimensions:", whole_sum)
    print("sum of squares of all eight kinds' dimensions:", all_sum)
    print("the full turn (-1) acts as -I on the half-speed kinds:", [labels[k] for k in range(nk) if spun.half[k]])

    print("\northogonality on the 48: (1/48) SUM chi_a chi_b, as (multiplicity, remainder, r2 part)")
    bad = 0
    for a in range(nk):
        row = []
        for b in range(nk):
            m, rem, r2 = inner(flat[a], flat[b], every)
            row.append(m)
            bad += int(rem != 0 or r2 != 0 or m != int(a == b))
        print(" ", labels[a].ljust(5), row)
    print("orthogonality departures (must be 0):", bad)

    def decompose(chi, among, names):
        out = []
        for k in names:
            m, rem, r2 = inner(chi, flat[k], among)
            out.append((labels[k], m, rem, r2))
        return out

    # the 24 whole units: the lifts whose turn permutes the axes evenly (A2 = +1)
    units = flat[a2, :, 0] == 1
    print("\nlifts with A2 = +1 (the 24 whole units, 2T):", int(units.sum()))

    e1 = flat[e12]
    cube = mul(mul(e1, e1), e1)
    print("\nE1/2 cubed (three half-speed members) on the 48:")
    for lab, m, rem, r2 in decompose(cube, every, range(nk)):
        print(f"  {lab:5s} multiplicity {m} (remainder {rem}, r2 part {r2})")
    hand = mul(e1, flat[t1])
    print("\nE1/2 x T1 (the half-speed hand on the three axes) on the 48:")
    for lab, m, rem, r2 in decompose(hand, every, range(nk)):
        print(f"  {lab:5s} multiplicity {m} (remainder {rem}, r2 part {r2})")

    print("\nrestricted to the 24 whole units: (1/24) SUM |chi|^2, the number of distinct irreducible pieces (each once)")
    for name, chi in (("E1/2", e1), ("E5/2", flat[labels.index("E5/2")]), ("G3/2", flat[labels.index("G3/2")]),
                      ("E1/2 x T1", hand)):
        m, rem, r2 = inner(chi, chi, units)
        m48, rem48, r248 = inner(chi, chi, every)
        print(f"  {name:10s} on the 24 units: {m} (rem {rem}, r2 {r2}) | on the 48: {m48} (rem {rem48}, r2 {r248})")
    m, rem, r2 = inner(e1, flat[labels.index("E5/2")], units)
    print(f"  <E1/2, E5/2> on the 24 units: {m} (rem {rem}, r2 {r2}): one doublet, the same on the 24 units")
    m, rem, r2 = inner(e1, flat[labels.index("G3/2")], units)
    print(f"  <E1/2, G3/2> on the 24 units: {m} (rem {rem}, r2 {r2})")

    print("\nthe two half-speed trains' characters (the 8-gear and the 24-gear train) on the 48:")
    for t, gears in zip(spun.trains, spun.gears):
        chi = np.stack((t.reshape(-1), 0 * t.reshape(-1)), axis=-1)
        parts = [(lab, m) for lab, m, rem, r2 in decompose(chi, every, range(nk)) if m]
        rems = [(rem, r2) for lab, m, rem, r2 in decompose(chi, every, range(nk))]
        m24, rem24, _ = inner(chi, chi, units)
        print(f"  {gears}-gear train: {parts} | all remainders 0: {all(r == (0, 0) for r in rems)}"
              f" | (1/24) SUM chi^2 on the 24 units: {m24} (rem {rem24})")


if __name__ == "__main__":
    main()
