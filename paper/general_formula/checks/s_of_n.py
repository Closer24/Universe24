"""S(N) of the amplitude-v1 pair at the CHSH labels for every N, from the design's formulas.

Reproduces docs/designs/amplitude-v1/bell.txt (section 4.2 and 4.3 of the design) with the
repository's own tables (core/phase.py) and extends it to every N that carries the CHSH labels
(8 | N). Exact integers throughout; a computation, not a run.
"""

from __future__ import annotations

import math
import sys
from fractions import Fraction
from functools import cache

sys.path.insert(0, "src")
from event_universe.core.phase import phase_cosines  # noqa: E402

TSIRELSON = 2 * math.sqrt(2)
POH_S, POH_SIGMA = 2.82759, 0.00051  # Poh et al., Phys. Rev. Lett. 115, 180408 (2015)


@cache
def half_tables(n: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    c = phase_cosines(2 * n)
    s = tuple(c[(k - n // 2) % (2 * n)] for k in range(2 * n))  # quarter turn exact on the tables
    return c, s


def rotation(
    c: tuple[int, ...], s: tuple[int, ...], setting: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    return ((c[setting], s[setting]), (-s[setting], c[setting]))  # rows: outcome +, outcome -


def joint_weights(n: int, a: int, b: int) -> dict[tuple[int, int], int]:
    c, s = half_tables(n)
    ua, ub = rotation(c, s, a), rotation(c, s, b)
    weights = {}
    for oa in (0, 1):
        for ob in (0, 1):
            j = ua[oa][0] * ub[ob][0] + ua[oa][1] * ub[ob][1]  # the pair's labels [[0, 1], [1, 1]]
            weights[(oa, ob)] = j * j
    return weights


def rung(n: int, cumulative: int, total: int) -> int:
    return (2 * n * cumulative + total) // (2 * total)


def counts(n: int, a: int, b: int) -> tuple[dict[tuple[int, int], int], Fraction]:
    w = joint_weights(n, a, b)
    total = sum(w.values())
    coarse = rung(n, w[(0, 0)] + w[(0, 1)], total)  # A's marginal rung
    fine_plus = rung(n, w[(0, 0)], total)
    fine_minus = rung(n, w[(0, 0)] + w[(0, 1)] + w[(1, 0)], total)
    cells = {
        (0, 0): fine_plus,
        (0, 1): coarse - fine_plus,
        (1, 0): fine_minus - coarse,
        (1, 1): n - fine_minus,
    }
    e = Fraction(cells[(0, 0)] + cells[(1, 1)] - cells[(0, 1)] - cells[(1, 0)], n)
    return cells, e


def chsh(n: int) -> tuple[Fraction, list[Fraction], list[dict[tuple[int, int], int]]]:
    q = n // 8
    settings = [
        (0, q),
        (0, 3 * q),
        (2 * q, q),
        (2 * q, 3 * q),
    ]  # (0, 8), (0, 24), (16, 8), (16, 24) at N = 64
    es, cells = [], []
    for a, b in settings:
        cell, e = counts(n, a, b)
        es.append(e)
        cells.append(cell)
    s = es[0] - es[1] + es[2] + es[3]
    return s, es, cells


def marginals_exact(n: int) -> bool:
    for a in range(n):
        for b in range(n):
            cell, _ = counts(n, a, b)
            if cell[(0, 0)] + cell[(0, 1)] != n // 2 or cell[(0, 0)] + cell[(1, 0)] != n // 2:
                return False
    return True


def tie(n: int, a: int, b: int) -> bool:
    """A rung tie: 2 N W(+,+) / T an odd integer (Theorem 3)."""
    w = joint_weights(n, a, b)
    total = sum(w.values())
    numerator = 2 * n * w[(0, 0)]
    return numerator % total == 0 and (numerator // total) % 2 == 1


def quadruples_and_ties() -> None:
    """The maximum of S over every setting quadruple (a, a', b, b') at
    N = 64 and 256, the count of quadruples within three sigma of Poh et
    al. 2015 (the third assumption of the Bell section: E depends on
    (a, b) beyond a - b), and the rung ties at the CHSH labels for every
    8 | N <= 4096 and over every pair at N = 1024."""
    print()
    print("S over every setting quadruple, and the rung ties:")
    for n in (64, 256):
        e = [[float(counts(n, a, b)[1]) for b in range(n)] for a in range(n)]
        best = -9.0
        within = 0
        for a in range(n):
            for a2 in range(n):
                for b in range(n):
                    eab, ea2b = e[a][b], e[a2][b]
                    row_a, row_a2 = e[a], e[a2]
                    for b2 in range(n):
                        value = eab - row_a[b2] + ea2b + row_a2[b2]
                        if value > best:
                            best = value
                        if abs(value - POH_S) <= 3 * POH_SIGMA:
                            within += 1
        print(
            f"  N={n:3d}: max S over all quadruples = {Fraction(best).limit_denominator(4096)} = {best:.5f};"
            f" quadruples within 3 sigma of Poh: {within}"
        )
    labels = sum(
        tie(n, a, b)
        for n in range(8, 4097, 8)
        for a, b in ((0, n // 8), (0, 3 * n // 8), (n // 4, n // 8), (n // 4, 3 * n // 8))
    )
    print(f"  rung ties at the CHSH labels for every 8 | N <= 4096: {labels}")
    print(
        f"  rung ties over every setting pair at N = 1024: {sum(tie(1024, a, b) for a in range(1024) for b in range(1024))}"
    )


def main() -> None:
    print("reproduction of bell.txt:")
    for n in (64, 256, 1024):
        s, es, cells = chsh(n)
        print(f"  N={n}: E = {[str(e) for e in es]}; S = {s} = {float(s):.5f}; cells {cells[0]}")
    print(f"  N=64 marginals 1/2 in all 4096 setting pairs: {marginals_exact(64)}")
    print()
    print("the marginals and the per-E deviation over every setting pair (a, b):")
    for n in (8, 16, 24, 32, 48, 64, 96, 128, 192, 256, 512):
        c_n = phase_cosines(n)
        worst_cells, worst_exact = 0.0, 0.0
        for a in range(n):
            for b in range(n):
                _, e = counts(n, a, b)
                worst_cells = max(worst_cells, abs(float(e) - c_n[(a - b) % n] / 256))
                worst_exact = max(worst_exact, abs(float(e) - math.cos(2 * math.pi * (a - b) / n)))
        print(
            f"  N={n:4d}: marginals 1/2 in all {n * n} pairs: {marginals_exact(n)}; max |E - C_N[a-b]/256| = {worst_cells:.5f} = {worst_cells * n:.2f}/N; max |E - cos| = {worst_exact:.5f} = {worst_exact * n:.2f}/N"
        )
    print()
    print(f"2 sqrt 2 = {TSIRELSON:.5f}; Poh et al. 2015: S = {POH_S} +- {POH_SIGMA}")
    print("N, S(N), S(N) - 2 sqrt 2, (S(N) - S_Poh) / sigma")
    above = []
    excluded_5 = []
    allowed_3 = []
    rows = []
    for n in range(8, 4097, 8):
        s, _, _ = chsh(n)
        sf = float(s)
        z = (sf - POH_S) / POH_SIGMA
        rows.append((n, s, sf, z))
        if sf > TSIRELSON + 1e-12:
            above.append(n)
        if abs(z) > 5:
            excluded_5.append(n)
        elif abs(z) <= 3:
            allowed_3.append(n)
    for n, s, sf, z in rows:
        if n <= 128 or n in (192, 256, 384, 512, 768, 1024, 1536, 2048, 3072, 4096):
            print(f"  {n:5d}  {str(s):>12}  {sf:.5f}  {sf - TSIRELSON:+.5f}  {z:+8.1f}")
    print()
    print(
        f"N (8 | N, N <= 4096 (the tables bound raised to 65536 on 2026-09-20)) with S(N) > 2 sqrt 2: {len(above)} of {len(rows)}; the first twenty: {above[:20]}"
    )
    print(
        f"largest S(N): {max(rows, key=lambda r: r[2])[2]:.5f} at N = {max(rows, key=lambda r: r[2])[0]}"
    )
    print(f"smallest N with |S(N) - S_Poh| <= 3 sigma: {min(allowed_3) if allowed_3 else None}")
    print(
        f"N excluded at 5 sigma by Poh et al.: {len(excluded_5)} of {len(rows)}; largest excluded N: {max(excluded_5) if excluded_5 else None}"
    )
    print(
        f"N allowed within 3 sigma: {len(allowed_3)} of {len(rows)}; the smallest ten: {allowed_3[:10]}"
    )
    deficits = [(n, sf) for n, s, sf, z in rows if n >= 1024]
    print(f"N >= 1024: S(N) from {min(d[1] for d in deficits):.5f} to {max(d[1] for d in deficits):.5f}")
    worst = max(rows, key=lambda r: abs(r[2] - TSIRELSON) * r[0])
    print(
        f"largest N x |S(N) - 2 sqrt 2| over all N: {abs(worst[2] - TSIRELSON) * worst[0]:.2f} at N = {worst[0]} (the claim epsilon <= 4/N needs this <= 4)"
    )


if __name__ == "__main__":
    main()
    quadruples_and_ties()
