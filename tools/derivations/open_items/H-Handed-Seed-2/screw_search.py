"""cs2: the search for a handed light pattern on the 4-cube (integers only). A pattern is a Z_4 phase t(k) at every Node: the gap-0 line's pair (now, before) = (v + A c, A s) with (c, s) the quarter turns (1,0),(0,1),(-1,0),(0,-1) and v the sea's drift; the im line (A s, -A c). F(k, j) = now_k before_j - before_k now_j; u_b(k) = F(k, k - b) - F(k, k + b); h(k, k + a) = u_b(k) u_c(k + a) - u_c(k) u_b(k + a). The patterns: t on the 2x2x2 cell (4^8), extended by t(k + 2 e_a) = t(k) + 2 eta_a (eta_a 0 periodic, 1 antiperiodic). Scored by the Links with F != 0 and h != 0 (of 192), the symmetry group among translations composed with phase turns, and the neighbours' sums (the uniformity of the forms).

Usage: python screw_search.py <v> <A> [top N]"""

from __future__ import annotations

import sys
from itertools import product

C = 4
N = C * C * C
COS = (1, 0, -1, 0)
SIN = (0, 1, 0, -1)


def idx(x: int, y: int, z: int) -> int:
    return ((x % C) * C + (y % C)) * C + (z % C)


def coords(i: int) -> tuple[int, int, int]:
    return i // (C * C), (i // C) % C, i % C


NBR = []  # per Node, per axis: (plus, minus)
for i_ in range(N):
    x_, y_, z_ = coords(i_)
    NBR.append(
        (
            (idx(x_ + 1, y_, z_), idx(x_ - 1, y_, z_)),
            (idx(x_, y_ + 1, z_), idx(x_, y_ - 1, z_)),
            (idx(x_, y_, z_ + 1), idx(x_, y_, z_ - 1)),
        )
    )


def extend(cell: tuple[int, ...], eta: tuple[int, int, int]) -> list[int]:
    """The phase at every Node from the cell's 8 phases and the extension per axis."""
    t = [0] * N
    for i in range(N):
        x, y, z = coords(i)
        base = cell[((x % 2) * 2 + (y % 2)) * 2 + (z % 2)]
        shift = 2 * (eta[0] * (x // 2) + eta[1] * (y // 2) + eta[2] * (z // 2))
        t[i] = (base + shift) % 4
    return t


def lines_of(t: list[int], v: int, amp: int) -> tuple[list[int], list[int]]:
    now = [v + amp * COS[p] for p in t]
    before = [amp * SIN[p] for p in t]
    return now, before


def currents(now: list[int], before: list[int]) -> list[list[int]]:
    """F from every Node along +a, per axis."""
    f = [[0] * N for _ in range(3)]
    for i in range(N):
        for a in range(3):
            j = NBR[i][a][0]
            f[a][i] = now[i] * before[j] - before[i] * now[j]
    return f


def twists(now: list[int], before: list[int]) -> tuple[list[list[int]], list[list[int]]]:
    f = currents(now, before)
    u = [[0] * N for _ in range(3)]
    for i in range(N):
        for b in range(3):
            minus = NBR[i][b][1]
            # F(k, k - b) = -F(k - b, k) = -f[b][minus]
            u[b][i] = -f[b][minus] - f[b][i]
    h = [[0] * N for _ in range(3)]
    for i in range(N):
        for a in range(3):
            b, c = (a + 1) % 3, (a + 2) % 3
            j = NBR[i][a][0]
            h[a][i] = u[b][i] * u[c][j] - u[c][i] * u[b][j]
    return f, h


def symmetries(t: list[int]) -> tuple[int, int, bool]:
    """The translations (with a phase turn m) that leave the pattern: their count, the count of distinct translations, and whether they act transitively (every Node reached from the origin)."""
    found = 0
    reached = set()
    for dx, dy, dz in product(range(C), repeat=3):
        for m in range(4):
            ok = True
            for i in range(N):
                x, y, z = coords(i)
                if (t[idx(x + dx, y + dy, z + dz)] - t[i] - m) % 4:
                    ok = False
                    break
            if ok:
                found += 1
                reached.add(idx(dx, dy, dz))
    return found, len(reached), len(reached) == N


def neighbour_sums(now: list[int], before: list[int], v: int) -> tuple[int, int]:
    """The largest |sum over the six neighbours| of the perturbation a = now - v and of b = before: 0 means the forces' non-uniform parts vanish."""
    worst_a = worst_b = 0
    for i in range(N):
        sa = sb = 0
        for a in range(3):
            for j in NBR[i][a]:
                sa += now[j] - v
                sb += before[j]
        worst_a = max(worst_a, abs(sa))
        worst_b = max(worst_b, abs(sb))
    return worst_a, worst_b


def score(t: list[int], v: int, amp: int) -> tuple[int, int, int, int]:
    now, before = lines_of(t, v, amp)
    f, h = twists(now, before)
    nf = sum(1 for a in range(3) for i in range(N) if f[a][i] != 0)
    nh = sum(1 for a in range(3) for i in range(N) if h[a][i] != 0)
    both = sum(1 for a in range(3) for i in range(N) if f[a][i] != 0 and h[a][i] != 0)
    sa, sb = neighbour_sums(now, before, v)
    return both, nf, nh, sa + sb


def main(argv: list[str]) -> None:
    v, amp = int(argv[1]), int(argv[2])
    top = int(argv[argv.index("top") + 1]) if "top" in argv else 12
    best: list[tuple[tuple[int, int, int, int], tuple[int, ...], tuple[int, int, int]]] = []
    total = 0
    full = 0
    by_eta: dict[tuple[int, int, int], int] = {}
    for eta in product((0, 1), repeat=3):
        by_eta[eta] = 0
        for cell in product(range(4), repeat=8):
            if cell[0] != 0:
                continue  # the global phase fixed: the origin at 0
            t = extend(cell, eta)
            s = score(t, v, amp)
            total += 1
            if s[0] == 3 * N:
                full += 1
                by_eta[eta] += 1
            best.append((s, cell, eta))
    best.sort(key=lambda r: (-r[0][0], -r[0][1], -r[0][2], r[0][3]))
    print("patterns", total, "with F and twist together on every Link", full, "by eta", by_eta)
    joint = {}
    for s, cell, eta in best:
        joint[s[0]] = joint.get(s[0], 0) + 1
    print("patterns by the count of Links with F and twist together", sorted(joint.items(), reverse=True)[:12])
    shown = 0
    for s, cell, eta in best:
        if shown >= top:
            break
        t = extend(cell, eta)
        sym = symmetries(t)
        print("both", s[0], "F_links", s[1], "twist_links", s[2], "nbr_sums", s[3], "cell", "".join(str(c) for c in cell), "eta", "".join(str(e) for e in eta), "symmetries", sym)
        shown += 1
    # the product pattern chi(x) chi(y) chi(z) in the phase: t = parity + 2 (1 - chi)/2 ...
    chi = (1, 1, -1, -1)
    t_prod = []
    for i in range(N):
        x, y, z = coords(i)
        sgn = chi[x] * chi[y] * chi[z]
        par = (x + y + z) % 2
        t_prod.append((par if sgn == 1 else par + 2) % 4)
    print("product pattern chi(x)chi(y)chi(z): both, F, twist, nbr sums", score(t_prod, v, amp), "symmetries", symmetries(t_prod))
    s2 = extend((0, 0, 1, 1, 1, 3, 2, 0), (1, 1, 1))
    print("the S1/S2 pattern 00111320 eta 111: both, F, twist, nbr sums", score(s2, v, amp))


if __name__ == "__main__":
    main(sys.argv)
