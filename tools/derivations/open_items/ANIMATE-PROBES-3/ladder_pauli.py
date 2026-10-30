"""Toy: the 24's ladder read with Pauli's rule (Animate; David's DAVID-TENSOR24-THE-COMPOSITE.md, toys-5 cfadfecdd, and
his 6469872764: two equal quanta, one train and one sense, stand as u x v + e v x u with e the kind's sign, so they
fuse only into their kind's own symmetric part; the Boss's ask of 6470415933: "the ladder under David's equal-quanta
rule").

The kinds of 2O and their characters are kinds_ladder.py's (ANIMATE-PROBES-2), exact in Z[sqrt 2]. Two equal clocks of
kind K take Sym^2 K where the kind's sign e is +1 (the 24's own kinds) and Alt^2 K where it is -1 (the spinor kinds);
chi_Sym2(g) = (chi(g)^2 + chi(g^2)) / 2 and chi_Alt2(g) = (chi(g)^2 - chi(g^2)) / 2, every multiplicity an integer.
Two clocks of different kinds, or of one kind but unequal (a quantum and its antiquantum, the fitting's two ends, or
two families), take the whole product.

Checked:
  1. the symmetric and antisymmetric squares of every kind, and that they sum to the product (no kind lost);
  2. e is the Frobenius-Schur sign: A1 lies in Sym^2 K for the 24's kinds and in Alt^2 K for the spinor kinds;
  3. three ladders from the calibre with the twin hands {A1, E1/2}, each bang fusing every pair of kinds present:
     (equal) every pair of one kind equal (one train and one sense per kind);
     (fitting) the first rung's twin pair unequal (the fitting lays a quantum and its antiquantum), every later pair of
               one kind equal;
     (table) every pair whole (the reach of the table, kinds_ladder.py part 3);
  4. a mutant: the exchange sign read with the wrong sign (Sym^2 on the spinors) lets two equal twins make the vector T1,
     which David's rule forbids, so the ladder climbs where it must not.
"""

import os
import sys
from itertools import combinations_with_replacement

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ANIMATE-PROBES-2"))

from kinds_ladder import KINDS, SIZES, fs_indicator, inner, parts, product, zadd, zmul  # noqa: E402

SQUARE_CLASS = [0, 0, 3, 3, 1, 4, 4, 1]  # the class of g^2 for each class (kinds_ladder.fs_indicator)
ORDER = list(KINDS)


def square_part(name, sign):
    """The kinds in the symmetric (sign +1) or antisymmetric (sign -1) square of a kind, as {kind: multiplicity}."""
    chi = KINDS[name]
    twice = [
        zadd(zmul(chi[c], chi[c]), zmul((sign, 0), chi[SQUARE_CLASS[c]])) for c in range(len(SIZES))
    ]
    found = {}
    for k, psi in KINDS.items():
        m2 = inner(twice, psi)  # the multiplicity of k in twice the part
        if m2 % 2:
            raise ValueError(f"not a multiplicity: {name} {sign} {k} {m2}")
        if m2:
            found[k] = m2 // 2
    return found


def equal_part(name, wrong=False):
    """Two equal clocks of one kind: the part of the kind's own exchange sign e (Frobenius-Schur), Sym^2 at e = +1 and
    Alt^2 at e = -1; with `wrong`, the sign read backwards (the mutant)."""
    e = fs_indicator(name)
    return square_part(name, -e if wrong else e)


def fuse(kinds, unequal, wrong=False):
    """The kinds after one bang: every pair of kinds present fused, each with itself too; a pair of one kind takes the
    whole product where the kind is in `unequal`, its own symmetric part otherwise."""
    found = set(kinds)
    for k1, k2 in combinations_with_replacement(sorted(kinds, key=ORDER.index), 2):
        if k1 != k2 or k1 in unequal:
            found |= set(parts(product(KINDS[k1], KINDS[k2])))
        else:
            found |= set(equal_part(k1, wrong))
    return found


def ladder(start, unequal_at, bangs=6, wrong=False):
    """The kinds present at each bang; `unequal_at(n)` the kinds whose pairs are unequal at bang n."""
    rungs, present = [], set(start)
    for n in range(1, bangs + 1):
        rungs.append(sorted(present, key=ORDER.index))
        present = fuse(present, unequal_at(n), wrong)
    return rungs


def report(title, rungs):
    print(title)
    for n, rung in enumerate(rungs, start=1):
        print(f"   bang {n}: {len(rung)} kinds {rung}")
    full = next((n for n, rung in enumerate(rungs, start=1) if len(rung) == len(KINDS)), None)
    print(f"   all eight kinds stand {'at bang ' + str(full) if full else 'at no bang'}")
    return full


def main():
    print("1. the squares of every kind (Sym^2 + Alt^2 = K x K)")
    lost = 0
    for k in ORDER:
        sym, alt = square_part(k, 1), square_part(k, -1)
        whole = parts(product(KINDS[k], KINDS[k]))
        both = {n: sym.get(n, 0) + alt.get(n, 0) for n in set(sym) | set(alt)}
        lost += both != whole
        print(f"   {k:5s}: Sym^2 {sym}; Alt^2 {alt}")
    print(f"   kinds where Sym^2 + Alt^2 differs from K x K: {lost}")

    print("2. the exchange sign e and where A1 lies")
    for k in ORDER:
        e = fs_indicator(k)
        where = (
            "Sym^2" if "A1" in square_part(k, 1) else ("Alt^2" if "A1" in square_part(k, -1) else "none")
        )
        print(f"   {k:5s}: e = {e:+d}; A1 in {where}; two equal clocks fuse into {equal_part(k)}")

    print("3. the ladders from the calibre with the twin hands {A1, E1/2}")
    a = report("   (equal) every pair of one kind equal", ladder({"A1", "E1/2"}, lambda n: set()))
    b = report(
        "   (fitting) the first rung's twin pair unequal (the fitting's quantum and antiquantum)",
        ladder({"A1", "E1/2"}, lambda n: {"E1/2"} if n == 1 else set()),
    )
    c = report("   (table) every pair whole", ladder({"A1", "E1/2"}, lambda n: set(ORDER)))
    print(f"   the bang at which all eight stand: equal {a}, fitting {b}, table {c}")

    print("4. the mutant: the exchange sign read backwards")
    print(f"   two equal twins fuse into {equal_part('E1/2', wrong=True)} (David's rule: A1 alone)")
    m = report("   (equal, mutant)", ladder({"A1", "E1/2"}, lambda n: set(), wrong=True))
    print(
        f"   the mutant's ladder climbs to all eight at bang {m}, where the law's stays at two kinds: it fails"
    )


if __name__ == "__main__":
    main()
