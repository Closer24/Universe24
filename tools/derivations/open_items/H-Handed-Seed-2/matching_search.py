"""cs2: among the Z_4 cell patterns at v = 0 (no sea), those whose Links with F != 0 AND twist != 0 form a matching (every Node the end of at most one such Link), ranked by the matching's size (32 = perfect: one child per Node per close, the crowding rule of close.refuse never met) and by the symmetry group's size. Integers only.

Usage: python matching_search.py <v> <A> [top N]"""

from __future__ import annotations

import sys
from itertools import product

import screw_search as ss


def matching(t: list[int], v: int, amp: int) -> tuple[int, int, int]:
    now, before = ss.lines_of(t, v, amp)
    f, h = ss.twists(now, before)
    degree = [0] * ss.N
    both = 0
    for a in range(3):
        for i in range(ss.N):
            if f[a][i] != 0 and h[a][i] != 0:
                both += 1
                degree[i] += 1
                degree[ss.NBR[i][a][0]] += 1
    return both, max(degree), min(degree)


def main(argv: list[str]) -> None:
    v, amp = int(argv[1]), int(argv[2])
    top = int(argv[argv.index("top") + 1]) if "top" in argv else 12
    found = []
    perfect = 0
    for eta in product((0, 1), repeat=3):
        for cell in product(range(4), repeat=8):
            if cell[0] != 0:
                continue
            t = ss.extend(cell, eta)
            both, dmax, dmin = matching(t, v, amp)
            if both > 0 and dmax <= 1:
                found.append((both, dmin, cell, eta))
                if both == ss.N // 2:
                    perfect += 1
    found.sort(key=lambda r: (-r[0], -r[1]))
    print("patterns whose birthing Links form a matching", len(found), "perfect matchings (32 Links, every Node once)", perfect)
    shown = 0
    for both, dmin, cell, eta in found:
        if shown >= top:
            break
        t = ss.extend(cell, eta)
        sc = ss.score(t, v, amp)
        print("matching", both, "min degree", dmin, "both/F/twist/nbr", sc, "cell", "".join(str(c) for c in cell), "eta", "".join(str(e) for e in eta), "symmetries", ss.symmetries(t))
        shown += 1


if __name__ == "__main__":
    main(sys.argv)
