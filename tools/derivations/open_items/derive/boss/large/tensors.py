"""The tensors' numbers: what the 24 rotations, the five kinds and the 43 tables can make, from the engine's own made().

usage: python3 -I tensors.py > tensors.txt

Derivation chain: every table is the group sum of one seed made primitive (runner/load.tables), so its entries are the
smallest whole numbers in their ratio; a coupling row multiplies the file's strength by one entry; a chain of couplings
multiplies entries and sums paths.  The fusion of kinds (how many times kind m sits in i x k) is the characters' inner
product; the growth of a chain of n couplings through a kind of dimension d is d^n (the Perron-Frobenius root of the
fusion matrix is the dimension), so a large number from the tensors needs a long chain, a count of the setting.
Tries: the multiplicities of every kind in every product of up to N factors are searched for nature's 1836, 137,
207 (muon), and the nearest to 1.7e38 (= hbar c / G m_p^2) and 1e40 are named; every hit is a coincidence by
construction (the count N is chosen).
"""

import itertools
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "src"))  # the worktree's committed act

from tensor24 import main as tensor24  # noqa: E402
from tensor24.engine import kinds as kinds_mod  # noqa: E402


def main() -> None:
    out = ["The tensors' numbers, from tensor24-review's engine/kinds.py and runner/load.tables", ""]
    held, tables = tensor24.made((1, 1, 1))
    matrix, weight = kinds_mod.turns(kinds_mod.axes(3))
    on = [g for g in range(len(weight)) if weight[g] == 1]
    labels = [f.upper() for f in held._fields]
    chars = {lab: [int(np.trace(k[g])) for g in on] for lab, k in zip(labels, held, strict=True)}
    dims = {
        lab: chars[lab][on.index(next(g for g in on if (matrix[g] == np.eye(3, dtype=object)).all()))]
        for lab in labels
    }
    order = len(on)
    out.append(
        f"rotations (weight 1): {order}; kinds and dimensions {dims}; sum of squares {sum(d * d for d in dims.values())}"
    )

    def mult(m, factors):
        """How many times kind m sits in the product of the factors: (1/24) sum_g chi_m(g)* prod chi_f(g)."""
        total = sum(chars[m][j] * math.prod(chars[f][j] for f in factors) for j in range(order))
        return Fraction(total, order)

    nonzero = {k: v for k, v in tables.items() if np.asarray(v).any()}
    norms = {k: int((np.asarray(v, dtype=object) ** 2).sum()) for k, v in nonzero.items()}
    entries = sorted({int(x) for v in nonzero.values() for x in np.asarray(v).ravel() if x})
    out.append(
        f"tables not zero: {len(nonzero)} of {len(tables)}; entries {entries}; squared norms from {min(norms.values())} "
        f"to {max(norms.values())} (ratio {max(norms.values()) / min(norms.values()):.1f})"
    )
    # fusion matrices and their Perron-Frobenius roots
    for f in labels:
        n = np.array([[float(mult(m, [i, f])) for i in labels] for m in labels])
        root = max(abs(np.linalg.eigvals(n)))
        out.append(f"   fusion by {f}: Perron-Frobenius root {root:.6f} (its dimension {dims[f]})")
    # A1 in T1^n: (3^n + 6 + 9 (-1)^n) / 24 for n >= 1
    seq = [mult("A1", ["T1"] * n) for n in range(1, 13)]
    out.append(
        f"A1 in T1^n, n = 1..12: {[int(x) for x in seq]}; closed form (3^n + 6 + 9(-1)^n)/24: "
        f"{all(seq[n - 1] == Fraction(3**n + 6 + 9 * (-1) ** n, 24) for n in range(1, 13))}"
    )
    out.append(
        f"chain length for 3^n / 24 to reach 1836: n = {math.log(1836 * 24, 3):.2f}; to reach 1e40: n = {math.log(1e40 * 24, 3):.1f}; "
        f"to reach 1.7e38: n = {math.log(1.7e38 * 24, 3):.1f}"
    )
    # tries: multiplicities of every kind in every multiset of up to 8 factors
    tries = 0
    hits = {1836: [], 137: [], 207: [], 1838: []}
    for size in range(1, 9):
        for combo in itertools.combinations_with_replacement(labels, size):
            for m in labels:
                v = mult(m, list(combo))
                tries += 1
                if v in hits:
                    hits[int(v)].append((m, combo))
    out.append(
        f"tries: multiplicities of each kind in each product of 1 to 8 kinds: {tries} numbers; "
        + "; ".join(f"{k}: {len(v)} hits{(' e.g. ' + str(v[0])) if v else ''}" for k, v in hits.items())
    )
    out.append(
        "   (any hit is a count of factors chosen to land there: a coincidence by construction, no line selects it)"
    )
    print("\n".join(out))


if __name__ == "__main__":
    main()
