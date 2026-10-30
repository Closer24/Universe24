"""N3, the ten slots' sources: each (mu, nu) slot pushed by its own component of (d - 1) T_mu,nu - eta_mu,nu T.

Einstein's law in d + 1 dimensions, R_mu,nu = kappa (T_mu,nu - eta_mu,nu T / (d - 1)), times d - 1: every slot's
source is an integer combination of the books' tensor, the same for every kind. At d = 3 the 2 is d - 1, the
board's axes less one, so no number is typed.

Checks, exact with fractions:
  1. a fluid at rest (rho, p) in d = 1 to 5: the 00 slot gets (d - 2) rho + d p, each diagonal slot rho - p, and the
     diagonal's d slots d (rho - p) in all; at d = 3, rho + 3p and 3 (rho - p);
  2. one gear's books (a value phi with rate v, differences g_i and a spring V, at one Node-clock) in d = 3:
     T_00 = K + G + V, T_0i = -v g_i, T_ij = g_i g_j + delta_ij (K - G - V), with K = v^2/2 and G = |g|^2/2. The slots:
     00 = 4K - 2V, ii = 2 g_i^2 + 2V, 0i = -2 v g_i, ij = 2 g_i g_j: products of the gear's own rates and
     differences, rows of the one plan;
  3. the sum of the diagonal slots equals 3 (rho - p) of the same books, with rho = K + G + V and p = K - G/3 - V
     (the isotropic mean of the differences).

Usage: python3 -I n3_slots.py
"""

from fractions import Fraction as F


def slots(t, d):
    """(d - 1) T - eta T for a (d+1) x (d+1) tensor t, eta = diag(-1, 1, ..., 1)."""
    eta = [[(-1 if i == 0 else 1) if i == j else 0 for j in range(d + 1)] for i in range(d + 1)]
    trace = sum(eta[i][i] * t[i][i] for i in range(d + 1))
    return [[(d - 1) * t[i][j] - eta[i][j] * trace for j in range(d + 1)] for i in range(d + 1)]


def main():
    rho, p = F(7), F(2)
    for d in range(1, 6):
        t = [[rho if i == j == 0 else (p if i == j else 0) for j in range(d + 1)] for i in range(d + 1)]
        s = slots(t, d)
        assert s[0][0] == (d - 2) * rho + d * p
        assert all(s[i][i] == rho - p for i in range(1, d + 1))
        print(f"1. d = {d}: 00 slot {s[0][0]} = (d - 2) rho + d p; each diagonal slot {s[1][1]} = rho - p; "
              f"the diagonal in all {sum(s[i][i] for i in range(1, d + 1))} = d (rho - p)")
    v, g, V = F(3), [F(1), F(-2), F(5)], F(4)
    K, G = F(v * v, 2), F(sum(x * x for x in g), 2)
    t = [[0] * 4 for _ in range(4)]
    t[0][0] = K + G + V
    for i in range(3):
        t[0][i + 1] = t[i + 1][0] = -v * g[i]
        for j in range(3):
            t[i + 1][j + 1] = g[i] * g[j] + (K - G - V if i == j else 0)
    s = slots(t, 3)
    assert s[0][0] == 4 * K - 2 * V
    assert all(s[i + 1][i + 1] == 2 * g[i] ** 2 + 2 * V for i in range(3))
    assert all(s[0][i + 1] == -2 * v * g[i] for i in range(3))
    assert all(s[i + 1][j + 1] == 2 * g[i] * g[j] for i in range(3) for j in range(3) if i != j)
    print(f"2. one gear (v {v}, g {[int(x) for x in g]}, V {V}): 00 = 4K - 2V = {s[0][0]}; "
          f"ii = 2 g_i^2 + 2V = {[int(s[i][i]) for i in range(1, 4)]}; 0i = -2 v g_i = {[int(s[0][i]) for i in range(1, 4)]}; "
          f"ij = 2 g_i g_j = {[int(s[1][2]), int(s[1][3]), int(s[2][3])]}")
    rho, p = K + G + V, K - F(G, 3) - V
    assert sum(s[i][i] for i in range(1, 4)) == 3 * (rho - p)
    assert s[0][0] == rho + 3 * p
    print(f"3. the diagonal in all {sum(s[i][i] for i in range(1, 4))} = 3 (rho - p); the 00 slot = rho + 3p = {rho + 3 * p}")


if __name__ == "__main__":
    main()
