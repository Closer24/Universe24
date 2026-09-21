"""Section 17's amendment per the physics-rule review of covariant-readings-v1
(record 297): the integers of the design and the pins on declared momenta.
Host arithmetic; no run. The identity's declared c^2 is the pair [1, 3];
E' = 3 E, E'_0 = Q S M, W = E'_0^2 + 3 p . p (exact, bilinear), E' the
largest integer with E'^2 <= W (kept by comparisons, no root at run time
after the load), the pace p / E' Links per interval, beta = sqrt 3 p / E'.

(A) The muon of J4 (M = 207, S = 1, Q S M = 13248): the momenta for beta
    0.4297 and 0.8594, E' at load, gamma = E' / E'_0, the 64th
    self-creation's tick, the range 64 p / E'_0, and the products' face
    clicks on a bar of 200 Links (the muon born at x = 10, the electron
    product flying at the heading's pace 32 / 55 to the +x face).
(B) coasting_none's s_mz2 (Q S M = 2^48, p_z = 51 901 289 008 505): beta
    and z under the identity at the declared momentum; the momentum that
    keeps beta = 0.2674; the grain that fits W in the word.
(C) E' kept exactly by comparisons under 40 000 unit pushes: the invariant
    E'^2 <= W < (E' + 1)^2 at every step, the comparisons per step.
(D) 12c.6's probe (series E's scalar world, S = 1, M = 1, p = 10 and 28)
    under the identity: beta, gamma, and the counts per self-creation
    outward and inward, gamma x (1 -+ v T_d / (Q S_1)), against the law's.
"""

from __future__ import annotations

import math
from pathlib import Path

Q = 64
C_HEADING = 32 / 55  # Links per interval on a heading (T_d = 110)
T_D_HEADING = 110
BOUND = (1 << 62) - 1


def energy_prime(e0: int, p: int) -> int:
    return math.isqrt(e0 * e0 + 3 * p * p)


def momentum_for(beta: float, e0: int) -> int:
    gamma = 1 / math.sqrt(1 - beta * beta)
    return round(beta * gamma * e0 / math.sqrt(3))


def main() -> None:
    out = ["(A) The muon of J4: E'_0 = Q S M = 13248, c^2 = [1, 3]"]
    e0 = 64 * 1 * 207
    bar, born = 200, 10
    for beta in (0.4297, 0.8594):
        p = momentum_for(beta, e0)
        e = energy_prime(e0, p)
        gamma = e / e0
        beta_law = math.sqrt(3) * p / e
        tick = 64 * gamma
        rng = 64 * p / e0
        x_decay = born + rng
        click = tick + (bar - x_decay) * T_D_HEADING / Q
        out.append(
            f"  beta {beta}: p = {p} label units, E' at load = isqrt({e0}^2 + 3 x {p}^2) = {e} (E'^2 <= W: {e * e <= e0 * e0 + 3 * p * p}),"
            f" gamma = E' / E'_0 = {gamma:.4f}, beta read back {beta_law:.4f}"
        )
        out.append(
            f"    the 64th self-creation at tick 64 gamma = {tick:.1f}; the range 64 p / E'_0 = {rng:.1f} Links (x = {x_decay:.1f});"
            f" the electron product's click on the +x face at tick {click:.0f} (the decay tick derived back by the flight table)"
        )
    rest_click = 64 + (bar - born) * T_D_HEADING / Q
    out.append(
        f"  the muon at rest (p = 0): the 64th self-creation at tick 64, the product's face click at {rest_click:.0f}"
    )
    out.append(
        f"  FORM.md section 4's momenta under the identity: p = 5815 gives beta {math.sqrt(3) * 5815 / energy_prime(e0, 5815):.3f} and the 64th at {64 * energy_prime(e0, 5815) / e0:.0f}; p = 47349 gives {math.sqrt(3) * 47349 / energy_prime(e0, 47349):.3f} and {64 * energy_prime(e0, 47349) / e0:.0f}"
    )

    out.append("")
    out.append("(B) coasting_none's s_mz2")
    e0 = 1 << 48
    p = 51901289008505
    e = energy_prime(e0, p)
    beta = math.sqrt(3) * p / e
    gamma = e / e0
    out.append(
        f"  at the declared p = {p}: beta = {beta:.4f}, gamma = {gamma:.4f}, z = gamma (1 + beta) - 1 = {gamma * (1 + beta) - 1:.4f} (the law's 0.2636 registered; nature's form at beta 0.2674 is 0.315)"
    )
    p2 = momentum_for(0.2674, e0)
    e2 = energy_prime(e0, p2)
    out.append(
        f"  the momentum that keeps beta = 0.2674: p = {p2}, z = {e2 / e0 * (1 + math.sqrt(3) * p2 / e2) - 1:.4f}"
    )
    for g_bits in (0, 16, 18, 20):
        g = 1 << g_bits
        w = (e0 // g) ** 2 + 3 * (p // g) ** 2
        out.append(
            f"  the grain g = 2^{g_bits}: W / g^2 = {w:.3e}, within 2^62 - 1: {w <= BOUND}; E' / g = {energy_prime(e0 // g, p // g)}"
        )

    out.append("")
    out.append("(C) E' kept by comparisons under 40 000 unit pushes from rest (E'_0 = 13248)")
    e0 = 13248
    p = 0
    e = e0
    max_cmp = 0
    ok = True
    for _ in range(40000):
        p += 1
        w = e0 * e0 + 3 * p * p
        cmp = 0
        while (e + 1) * (e + 1) <= w:
            e += 1
            cmp += 1
        while e * e > w:
            e -= 1
            cmp += 1
        max_cmp = max(max_cmp, cmp + 1)
        ok = ok and (e * e <= w < (e + 1) * (e + 1))
    out.append(
        f"  the invariant E'^2 <= W < (E' + 1)^2 held at every step: {ok}; the most comparisons in one step: {max_cmp}; E' = {e} at p = {p} (isqrt: {energy_prime(e0, p)}), beta = {math.sqrt(3) * p / e:.4f}"
    )

    out.append("")
    out.append("(D) 12c.6's probe under the identity (E'_0 = Q S M = 64)")
    e0 = 64
    for p in (10, 28):
        e = energy_prime(e0, p)
        v = p / e
        beta = math.sqrt(3) * v
        gamma = e / e0
        f = v * T_D_HEADING / (Q * 1)
        law_v = p * Q / (Q * Q + T_D_HEADING * p)
        out.append(
            f"  p = {p}: E' = {e}, v = p / E' = {v:.4f} Link per interval (the law's form B {law_v:.4f}), beta = {beta:.4f}, gamma = {gamma:.4f};"
            f" the count per self-creation outward gamma (1 - v T_d / (Q S_1)) = {gamma * (1 - f):.4f} x rest, inward {gamma * (1 + f):.4f} x rest"
            f" (12c.6's law pins {1 - law_v * T_D_HEADING / Q:.4f} and {1 + law_v * T_D_HEADING / Q:.4f})"
        )
    Path(__file__).with_suffix(".out").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
