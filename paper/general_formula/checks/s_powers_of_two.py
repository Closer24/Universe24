"""S(N) of the pair at the CHSH labels for the powers of two from 512 to 32768, with the tables fixed at 256.

Exact integers and fractions; a computation, not a run. The four correlations are listed
because they differ between the two pairs of settings once N is large enough for the
rungs' rounding to fall on different sides. The tables' bound (2N at most 65536) stops
the computation at N = 32768; the fixed-table limit is 2 (46565 + 46452) / 65773.
"""

from __future__ import annotations

import sys
from fractions import Fraction

sys.path.insert(0, "src")
from event_universe.core.phase import phase_cosines  # noqa: E402


def half_tables(n: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    c = phase_cosines(2 * n)
    s = tuple(c[(k - n // 2) % (2 * n)] for k in range(2 * n))
    return c, s


def correlation(n: int, a: int, b: int) -> tuple[Fraction, list[int]]:
    c, s = half_tables(n)
    j, k = c[a] * c[b] + s[a] * s[b], s[a] * c[b] - c[a] * s[b]
    weights = [j * j, k * k, k * k, j * j]
    total, cumulative, edges = sum(weights), 0, [0]
    for w in weights:
        cumulative += w
        edges.append((2 * n * cumulative + total) // (2 * total))
    counts = [edges[i + 1] - edges[i] for i in range(4)]
    return Fraction(counts[0] - counts[1] - counts[2] + counts[3], n), counts


def main() -> None:
    print("N, S, E(0, N/8), E(0, 3N/8), E(N/4, N/8), E(N/4, 3N/8), the counts of the last")
    for n in [64, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]:
        e1, _ = correlation(n, 0, n // 8)
        e2, _ = correlation(n, 0, 3 * n // 8)
        e3, _ = correlation(n, n // 4, n // 8)
        e4, counts = correlation(n, n // 4, 3 * n // 8)
        s_value = e1 - e2 + e3 + e4
        print(f"{n}, {s_value} = {float(s_value):.9f}, {e1}, {e2}, {e3}, {e4}, {counts}")
    limit = Fraction(2 * (46565 + 46452), 65773)
    print(f"fixed-table limit 2 (46565 + 46452) / 65773 = {limit} = {float(limit):.9f}")
    print(f"2 sqrt 2 = {2 * 2**0.5:.9f}")


if __name__ == "__main__":
    main()
