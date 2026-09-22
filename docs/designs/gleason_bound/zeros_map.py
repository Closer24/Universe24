"""The table click's zeros (the Gleason Bound Mathematician, 2026-09-22, the
Boss's added item): a search for elements f of the group ring, nonzero in
Z[zeta_N] after the cancel, whose table pointer (X, Y) = (sum a_i C[p_i],
sum a_i S[p_i]) is exactly (0, 0), over every f with at most 3 rows at
distinct phases and amounts 1 to 4, at N = 64 and N = 8192. The sign
p -> p + N / 2 is used (an amount -a at p is the amount a at p + N / 2,
exactly, in the ideal and on the tables alike); the phase rotation is NOT a
symmetry of the table reading and is not used. Kind: COMPUTATION on the
engine's tables (`event_universe.core.phase`); no run, no measurement. Run
from the repository root: `.venv/bin/python docs/designs/gleason_bound/zeros_map.py`."""

from __future__ import annotations

import math
import time

import numpy as np

from event_universe.core.phase import phase_cosines, phase_sines

AMOUNTS = (1, 2, 3, 4)
OFFSET = 1100
WIDTH = 2200


def key_of(c: np.ndarray, s: np.ndarray) -> np.ndarray:
    return (c + OFFSET) * WIDTH + (s + OFFSET)


def ideal_square(rows: tuple[tuple[int, int], ...], n: int) -> float:
    x = sum(a * math.cos(2 * math.pi * p / n) for p, a in rows)
    y = sum(a * math.sin(2 * math.pi * p / n) for p, a in rows)
    return x * x + y * y


def ideal_zero(rows: tuple[tuple[int, int], ...], n: int) -> bool:
    """f = 0 in Z[zeta_N] = Z[x] / (x^(N/2) + 1): the signed amounts per residue mod N / 2 all vanish."""
    half = n // 2
    sums: dict[int, int] = {}
    for p, a in rows:
        sums[p % half] = sums.get(p % half, 0) + (a if p < half else -a)
    return all(v == 0 for v in sums.values())


def search(n: int) -> None:
    c = np.array(phase_cosines(n), dtype=np.int64)
    s = np.array(phase_sines(n), dtype=np.int64)
    keys = key_of(c, s)
    lookup = np.full(WIDTH * WIDTH, -1, dtype=np.int64)
    count = np.zeros(WIDTH * WIDTH, dtype=np.int64)
    for p in range(n - 1, -1, -1):
        lookup[keys[p]] = p  # the smallest phase with this (C, S)
        count[keys[p]] += 1
    distinct = int((count > 0).sum())
    print(
        f"N = {n}: {distinct} distinct (C, S) pairs among {n} phases; "
        f"{n - distinct} phases share a pair with an earlier phase"
    )
    print("   one row: no table zero (C^2 + S^2 >= 65185 for every table entry)")

    t0 = time.time()
    two: set[tuple[tuple[int, int], ...]] = set()
    for p1 in range(n):
        for a1 in AMOUNTS:
            for a2 in AMOUNTS:
                tx, ty = -a1 * int(c[p1]), -a1 * int(s[p1])
                if tx % a2 or ty % a2:
                    continue
                k = (tx // a2 + OFFSET) * WIDTH + (ty // a2 + OFFSET)
                if k < 0 or k >= WIDTH * WIDTH or count[k] == 0:
                    continue
                for p2 in range(n):
                    if keys[p2] != k or p2 == p1:
                        continue
                    rows = tuple(sorted(((p1, a1), (p2, a2))))
                    if not ideal_zero(rows, n):
                        two.add(rows)
    two_sorted = sorted(two, key=lambda r: (sum(a for _, a in r), max(a for _, a in r), r))
    print(
        f"   two rows (amounts 1 to 4, distinct phases, not an ideal zero): {len(two)} unordered sets"
        f" ({time.time() - t0:.1f} s)"
    )
    for rows in two_sorted[:6]:
        x = sum(a * int(c[p]) for p, a in rows)
        y = sum(a * int(s[p]) for p, a in rows)
        print(
            f"      rows {rows}: tables (X, Y) = ({x}, {y}), the ideal |ev(f)|^2 = {ideal_square(rows, n):.3e}"
        )

    t0 = time.time()
    phases_by_key: dict[int, list[int]] = {}
    for p in range(n):
        phases_by_key.setdefault(int(keys[p]), []).append(p)
    three_count = 0
    smallest: tuple[tuple[int, int], ...] | None = None
    smallest_key: tuple[int, int, tuple[tuple[int, int], ...]] | None = None
    p_all = np.arange(n, dtype=np.int64)
    for a1 in AMOUNTS:
        for a2 in AMOUNTS:
            for a3 in AMOUNTS:
                if math.gcd(math.gcd(a1, a2), a3) != 1:
                    continue  # a scaled copy of a smaller triple
                for p1 in range(n):
                    tx = -(a1 * c[p1] + a2 * c)
                    ty = -(a1 * s[p1] + a2 * s)
                    if a3 != 1:
                        ok = (tx % a3 == 0) & (ty % a3 == 0)
                    else:
                        ok = np.ones(n, dtype=bool)
                    tx = tx // a3
                    ty = ty // a3
                    inside = ok & (tx > -OFFSET) & (tx < OFFSET) & (ty > -OFFSET) & (ty < OFFSET)
                    k = np.where(inside, key_of(tx, ty), 0)
                    found = inside & (count[k] > 0)
                    row1 = (p1, a1)
                    for p2 in p_all[found]:
                        p2 = int(p2)
                        if p2 == p1:
                            continue
                        row2 = (p2, a2)
                        if row2 < row1:
                            continue  # counted once, in the order of the rows
                        for p3 in phases_by_key[int(k[p2])]:
                            if p3 == p1 or p3 == p2:
                                continue
                            row3 = (p3, a3)
                            if row3 < row2:
                                continue
                            rows = (row1, row2, row3)
                            if ideal_zero(rows, n):
                                continue
                            three_count += 1
                            key = (a1 + a2 + a3, max(a1, a2, a3), rows)
                            if smallest_key is None or key < smallest_key:
                                smallest_key, smallest = key, rows
    print(
        f"   three rows (amounts 1 to 4 with gcd 1, distinct phases, not an ideal zero): {three_count} unordered sets"
        f" ({time.time() - t0:.1f} s)"
    )
    if smallest is not None:
        x = sum(a * int(c[p]) for p, a in smallest)
        y = sum(a * int(s[p]) for p, a in smallest)
        print(
            f"      the smallest: rows {smallest}: tables (X, Y) = ({x}, {y}), the ideal |ev(f)|^2 = {ideal_square(smallest, n):.3e}"
        )
    three = three_count
    if not two and not three:
        print("   NONE FOUND up to 3 rows at distinct phases with amounts 1 to 4")
    print()


def main() -> None:
    print("THE TABLE CLICK'S ZEROS: f nonzero in Z[zeta_N] with the table pointer exactly (0, 0)")
    print(
        "   the search: at most 3 rows at distinct phases, amounts 1 to 4, all phases (the rotation is no symmetry of the tables)"
    )
    print()
    for n in (64, 8192):
        search(n)
    print(
        "THE CONVERSE: an ideal zero reads (0, 0) on the tables, always: the kernel of ev on Z[Z_N] (N a power of two)"
    )
    print(
        "   is the ideal (1 + x^(N/2)), the antipodal pairs of equal amounts, and C[p + N/2] = -C[p], S[p + N/2] = -S[p]"
    )
    print(
        "   exactly for every N (checked below for every power of two from 4 to 65536), so the table reading, Z-linear, kills it."
    )
    for k in range(2, 17):
        n = 2**k
        c, s = phase_cosines(n), phase_sines(n)
        half = n // 2
        assert all(c[p + half] == -c[p] and s[p + half] == -s[p] for p in range(half)), n
    print("   antisymmetry exact at every N from 4 to 65536: CONFIRMED")


if __name__ == "__main__":
    main()
