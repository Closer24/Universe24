"""MASS2 probe 1: the families on the 48 lifts, from the engine's own kinds.lifts and files.spun (node-all 9d75a4904,
the read-only copy in mass2/tree). Clock facts only: characters, decompositions, the full turn, the Frobenius-Schur
indicators, and what they bound about beats of a real train under every symmetric coupling the 48 keep.

- The full turn is MEASURED: the lift whose turn is the identity and whose E1/2 character is minus its dimension, and
  every kind's character there against its dimension.
- Each lift's square g g is made by the engine's own Hamilton product (kinds.product), on the words rebuilt by the
  engine's own functions exactly as kinds.lifts builds them; the rebuilt words are checked against spun's E1/2
  character (the doubled unit part) at every lift, and each square is found among the 48 by equality of its pairs.
- Frobenius-Schur: (1/48) SUM chi(g g); the symmetric invariant forms of a train: (1/48) SUM (chi(g)^2 + chi(g g)) / 2;
  the real commutant's dimension: (1/48) SUM chi(g)^2.

Whole numbers only: characters are pairs (p, q) for p + q r2, products (pr + senses qs, ps + qr); every division by the
group's count is Rule3's carry with its remainder printed. The axes are read from the click world's piece file.
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


def words(spokes):
    """The 48 doubled lifts, (senses, classes, d + 1, 2), rebuilt by the engine's functions as kinds.lifts builds them."""
    n, d = spokes.shape
    senses, _ = carry(n, d, 0)
    c = kinds.hamilton(d)
    unit, first, second, third = kinds.axes(d + 1)
    zero = 0 * unit
    one = kinds.pair(senses * unit, zero)
    w = kinds.pair(unit + first + second + third, zero)
    z = kinds.pair(zero, unit + first)
    star = kinds.pair(senses * kinds.axes(d + 1), 0 * kinds.axes(d + 1))
    powers = np.stack((one, w, kinds.product(c, w, w, senses)))
    spins = np.stack((one, z))
    built = kinds.product(c, star[:, None, None], powers[None, :, None], senses)
    classes = kinds.listed(kinds.product(c, built, spins[None, None, :], senses))
    return np.stack((classes, -classes)), c, senses, unit


def main() -> None:
    piece = json.loads(TREE.joinpath("examples", "tensor24-click", "piece.json").read_text())
    d = len(piece["shape"])
    spokes = files.star(d)
    lifted = kinds.lifts(spokes)
    spun = files.spun(lifted)
    labels = tuple(n.upper().replace("_", "/") for n in (*lifted.whole._fields, *lifted.halves._fields))
    chars = spun.characters
    nk = chars.shape[0]
    flat = chars.reshape(nk, -1, chars.shape[-1])
    count = flat.shape[1]
    lift, c, senses, unit = words(spokes)
    flat_lift = lift.reshape(count, lift.shape[-2], lift.shape[-1])
    spin = np.einsum("gxp,x->gp", flat_lift, unit)
    e12, t1, a2 = labels.index("E1/2"), labels.index("T1"), labels.index("A2")
    print("lifts:", count, "| rebuilt words' doubled unit part equals spun's E1/2 character at every lift:",
          bool((spin == flat[e12]).all()))

    def mul(x, y):
        p, q = x[..., 0], x[..., 1]
        r, s = y[..., 0], y[..., 1]
        return np.stack((p * r + senses * q * s, p * s + q * r), axis=-1)

    def mean(x, among):
        tot = x[among].sum(axis=0)
        m, rem = carry(int(tot[0]), int(among.sum()), 0)
        return m, rem, int(tot[1])

    every = np.ones(count, dtype=bool)
    ident = [g for g in range(count) if flat[t1, g, 0] == d and flat[e12, g, 0] == senses and flat[e12, g, 1] == 0]
    turn = [g for g in range(count) if flat[t1, g, 0] == d and flat[e12, g, 0] == -senses and flat[e12, g, 1] == 0]
    g0, g1 = ident[0], turn[0]
    dims = [int(flat[k, g0, 0]) for k in range(nk)]
    print("the identity lift:", ident, "| the full turn (turn the identity, E1/2 at minus its dimension):", turn)
    print("dimensions:", dict(zip(labels, dims)))
    print("at the full turn, each kind's character (p, q) against its dimension:")
    for k in range(nk):
        p, q = int(flat[k, g1, 0]), int(flat[k, g1, 1])
        print(f"  {labels[k]:5s} {p:3d} (r2 part {q}) | dimension {dims[k]} | {'-I' if p == -dims[k] and q == 0 else ('+I' if p == dims[k] and q == 0 else 'neither')}")
    print("sum of squares, the five whole kinds:", sum(dims[k] * dims[k] for k in range(nk) if spun.half[k] == 0),
          "| all eight:", sum(x * x for x in dims))

    # each lift's square by the engine's Hamilton product, found among the 48
    sq = kinds.product(c, flat_lift, flat_lift, senses)
    where = []
    for g in range(count):
        hit = [h for h in range(count) if (flat_lift[h] == sq[g]).all()]
        where.append(hit)
    found = all(len(h) == 1 for h in where)
    square_of = np.array([h[0] for h in where])
    print("each lift's square found once among the 48:", found)

    print("\nFrobenius-Schur indicators, (1/48) SUM chi(g g), as (value, remainder, r2 part):")
    fs = []
    for k in range(nk):
        m, rem, r2 = mean(flat[k][square_of], every)
        fs.append(m)
        kind = {1: "real", 0: "complex", -1: "quaternionic"}.get(m, "?")
        print(f"  {labels[k]:5s} {m:2d} (rem {rem}, r2 {r2}): {kind}")

    def content(chi):
        """complex multiplicities on the eight kinds, with remainders"""
        out = []
        for k in range(nk):
            m, rem, r2 = mean(mul(chi, flat[k]), every)
            out.append((m, rem, r2))
        return out

    e1 = flat[e12]
    trains = [("E1/2 cubed (three half-speed members)", mul(mul(e1, e1), e1)),
              ("E1/2 x T1 (the half-speed hand on the three axes)", mul(e1, flat[t1]))]
    for chi_t, gears in zip(spun.trains, spun.gears):
        trains.append((f"the {gears}-gear train", np.stack((chi_t.reshape(-1), 0 * chi_t.reshape(-1)), axis=-1)))
    units = flat[a2, :, 0] == 1
    print("\nlifts with A2 = +1 (the 24 whole units, 2T):", int(units.sum()))
    for name, chi in trains:
        parts = content(chi)
        cplx = [(labels[k], parts[k][0]) for k in range(nk) if parts[k][0]]
        clean = all(r == 0 and q == 0 for _, r, q in parts)
        comm, crem, cq = mean(mul(chi, chi), every)
        chi_sq = chi[square_of]
        symm_tot = mul(chi, chi) + chi_sq
        sym, srem, sq2 = mean(symm_tot, every)
        sym_h, sym_r = carry(sym, senses, 0)
        on24, r24, q24 = mean(mul(chi, chi), units)
        # a train is real as it stands only if every quaternionic kind sits in it at an even multiplicity; else its
        # real form is the train twice. In the real form a quaternionic kind's real multiplicity is its multiplicity
        # there halved, a real kind's its multiplicity.
        odd = [labels[k] for k in range(nk) if parts[k][0] and fs[k] == -1 and carry(parts[k][0], senses, 0)[1]]
        twice = int(bool(odd))
        real = []
        for k in range(nk):
            m = parts[k][0] * (1 + twice)
            if m:
                if fs[k] == -1:
                    mh, mr = carry(m, senses, 0)
                    real.append((labels[k], mh, mr))
                else:
                    real.append((labels[k], m, 0))
        beats = sum(m for _, m, _ in real)
        print(f"\n{name}: complex content {cplx} (every remainder 0: {clean})")
        print(f"  quaternionic kinds at an odd multiplicity: {odd or 'none'}:"
              f" {'its real form is the train twice' if twice else 'real as it stands'}")
        print(f"  (1/48) SUM chi^2, the commutant's dimension (over the reals for a real train, over the complex numbers otherwise): {comm} (rem {crem}, r2 {cq})")
        print(f"  (1/48) SUM (chi^2 + chi(g g)) / 2, the invariant symmetric forms on the train as it stands: {sym_h} (rem {srem} then {sym_r}, r2 {sq2})")
        print(f"  real irreducibles (kind, real multiplicity, remainder): {real} | at most {beats} distinct beats"
              f" under every symmetric coupling the 48 keep")
        print(f"  on the 24 whole units, (1/24) SUM chi^2: {on24} (rem {r24}, r2 {q24})")
    g32 = labels.index("G3/2")
    m, rem, r2 = mean(mul(flat[g32], flat[g32]), units)
    print(f"\nG3/2 on the 24 whole units, (1/24) SUM chi^2: {m} (rem {rem}, r2 {r2}): two distinct doublets there")
    m, rem, r2 = mean(mul(e1, flat[labels.index("E5/2")]), units)
    print(f"<E1/2, E5/2> on the 24 whole units: {m} (rem {rem}, r2 {r2}): one doublet there")


if __name__ == "__main__":
    main()
