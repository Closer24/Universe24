"""Probe: the ladder of the 24's kinds, bang by bang (Animate; the owner's word of 2026-10-28, 13:0x UTC: "think in
clocks what will make every bang make clocks more sophisticated, more beautiful, that show everything, through the
tensors, the 24").

The 24's double cover 2O has eight kinds (A1, A2, E, T1, T2, E1/2, E5/2, G3/2). Two clocks of kinds K1 and K2 meeting
at one Node-clock read a joint dial of kind K1 x K2. The product table splits it into kinds, and law 6 on the
composite draws which one the pair becomes: the composite clock (the plan's open item 11 c). Its characters are
exact in Z[sqrt 2]; every multiplicity is the class sum over 48, an integer.

Checked:
  1. the table's own rows: each kind's norm is 1, and two kinds are orthogonal;
  2. the ladder from the one big bang's calibre, whose clocks are all A1 (the light, three sprung hands, the held
     field): A1 x A1 = A1, so no bang can make a new kind;
  3. the ladder with the twin hands (E1/2) beside them, each bang fusing every pair of kinds present: the kinds
     present at each bang, and the bang at which all eight stand;
  4. the slower ladder, each bang adding one twin hand to every clock (K x E1/2);
  5. the tensor powers of E1/2: the multiplicity of each kind in n twin hands, n = 1 to 8, and their gears 2^n;
  6. the exchange sign of the A1 part of two equal clocks of each kind (the Frobenius-Schur indicator, draft E):
     +1 on the 24's own kinds, -1 on the spinor kinds, so two equal twin hands pair only antisymmetrically (Pauli);
  7. a mutant: E1/2 with the sign of its C4 classes swapped is E5/2, and the ladder from it alone climbs too; a table
     with A2 read as A1 fails the orthogonality.
"""

from itertools import combinations_with_replacement

# Z[sqrt 2] as pairs (a, b) = a + b sqrt 2.


def zmul(x, y):
    return (x[0] * y[0] + 2 * x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def zadd(x, y):
    return (x[0] + y[0], x[1] + y[1])


R = (0, 1)  # sqrt 2
SIZES = [
    1,
    1,
    8,
    8,
    6,
    6,
    6,
    12,
]  # E, -E, C3 (order 6), -C3 (order 3), C4^2 (order 4), C4 (order 8), -C4, C2'
CLASSES = ["E", "-E", "8 C3", "8 -C3", "6 C4^2", "6 C4", "6 -C4", "12 C2'"]


def z(n):
    return (n, 0)


def neg(x):
    return (-x[0], -x[1])


KINDS = {
    "A1": [z(1), z(1), z(1), z(1), z(1), z(1), z(1), z(1)],
    "A2": [z(1), z(1), z(1), z(1), z(1), z(-1), z(-1), z(-1)],
    "E": [z(2), z(2), z(-1), z(-1), z(2), z(0), z(0), z(0)],
    "T1": [z(3), z(3), z(0), z(0), z(-1), z(1), z(1), z(-1)],
    "T2": [z(3), z(3), z(0), z(0), z(-1), z(-1), z(-1), z(1)],
    "E1/2": [z(2), z(-2), z(1), z(-1), z(0), R, neg(R), z(0)],
    "E5/2": [z(2), z(-2), z(1), z(-1), z(0), neg(R), R, z(0)],
    "G3/2": [z(4), z(-4), z(-1), z(1), z(0), z(0), z(0), z(0)],
}
SPINOR = {"E1/2", "E5/2", "G3/2"}


def inner(chi, psi):
    """(1/48) sum over the classes of size chi psi; the characters are real. Returns an integer, or raises."""
    total = (0, 0)
    for size, a, b in zip(SIZES, chi, psi, strict=True):
        total = zadd(total, zmul((size, 0), zmul(a, b)))
    if total[1] != 0 or total[0] % 48:
        raise ValueError(f"not a multiplicity: {total}")
    return total[0] // 48


def product(chi, psi):
    return [zmul(a, b) for a, b in zip(chi, psi, strict=True)]


def parts(chi, table=KINDS):
    return {k: m for k, v in table.items() if (m := inner(chi, v))}


def fuse_all(kinds):
    """The kinds in the products of every pair of kinds present (each with itself too)."""
    found = set(kinds)
    for k1, k2 in combinations_with_replacement(sorted(kinds), 2):
        found |= set(parts(product(KINDS[k1], KINDS[k2])))
    return found


def ladder(start, step, bangs=8):
    rungs, present = [], set(start)
    for _ in range(bangs):
        rungs.append(sorted(present, key=list(KINDS).index))
        present = step(present)
    return rungs


def with_twin(kinds):
    found = set(kinds)
    for k in kinds:
        found |= set(parts(product(KINDS[k], KINDS["E1/2"])))
    return found


def fs_indicator(name):
    """The exchange sign of a kind's A1 in K x K: (1/48) sum chi(g^2); the classes' squares: E, -E -> E; C3 (order 6) ->
    -C3 (order 3); -C3 -> -C3; C4^2 (order 4) -> -E; C4, -C4 (order 8) -> C4^2; C2' (order 4) -> -E."""
    square_class = [0, 0, 3, 3, 1, 4, 4, 1]
    chi = KINDS[name]
    total = (0, 0)
    for size, c in zip(SIZES, square_class, strict=True):
        total = zadd(total, zmul((size, 0), chi[c]))
    assert total[1] == 0 and total[0] % 48 == 0
    return total[0] // 48


def main():
    print("1. the table: every kind's norm and the orthogonality")
    names = list(KINDS)
    bad = [(a, b) for a in names for b in names if inner(KINDS[a], KINDS[b]) != (a == b)]
    dims = {k: v[0][0] for k, v in KINDS.items()}
    print(
        f"   {len(names)} kinds, the orthonormality failing at {len(bad)} pairs; the squared dimensions sum to "
        f"{sum(d * d for d in dims.values())} (the group's order 48)"
    )

    print("2. the one big bang's calibre: the light, three sprung hands and the held field, all A1")
    print(f"   A1 x A1 = {parts(product(KINDS['A1'], KINDS['A1']))}")
    for n, rung in enumerate(ladder({"A1"}, fuse_all, 4), start=1):
        print(f"   bang {n}: kinds present {rung}")

    print("3. the twin hands (E1/2) beside them, each bang fusing every pair of kinds present")
    rungs = ladder({"A1", "E1/2"}, fuse_all, 6)
    for n, rung in enumerate(rungs, start=1):
        print(f"   bang {n}: {len(rung)} kinds {rung}")
    full = next(n for n, rung in enumerate(rungs, start=1) if len(rung) == 8)
    print(f"   all eight kinds stand at bang {full}")

    print("4. each bang adding one twin hand to every clock (K x E1/2)")
    rungs = ladder({"A1", "E1/2"}, with_twin, 9)
    for n, rung in enumerate(rungs, start=1):
        print(f"   bang {n}: {len(rung)} kinds {rung}")

    print("5. n twin hands: the multiplicity of each kind in E1/2^n, and the gears 2^n")
    chi = KINDS["E1/2"]
    power = KINDS["A1"]
    for n in range(1, 9):
        power = product(power, chi)
        found = parts(power)
        gears = sum(m * dims[k] for k, m in found.items())
        print(f"   n = {n}: gears {gears} (2^n = {2**n}); {found}")

    print(
        "6. the exchange sign of each kind's A1 pairing (draft E's big law), and two equal clocks of each kind"
    )
    for k in names:
        sq = parts(product(KINDS[k], KINDS[k]))
        print(f"   {k:5s}: sign {fs_indicator(k):+d}; {k} x {k} = {sq}")

    print("7. mutants")
    swapped = [KINDS["E1/2"][i] if i not in (5, 6) else KINDS["E1/2"][11 - i] for i in range(8)]
    print(f"   E1/2 with its two C4 classes swapped is E5/2: {swapped == KINDS['E5/2']}")
    rung = ladder({"A1", "E5/2"}, fuse_all, 6)[-1]
    print(f"   the ladder from E5/2 alone reaches {len(rung)} kinds")
    wrong = dict(KINDS)
    wrong["A2"] = KINDS["A1"]
    try:
        bad = [(a, b) for a in wrong for b in wrong if inner(wrong[a], wrong[b]) != (a == b)]
        print(f"   A2 read as A1: the orthonormality fails at {len(bad)} pairs (fails as it must)")
    except ValueError as err:
        print(f"   A2 read as A1: {err} (fails as it must)")


if __name__ == "__main__":
    main()
