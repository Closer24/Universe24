"""g5: the Koide ratio Q = SUM m / (SUM sqrt m)^2 reachable by three masses on the cube roots' cosines.

usage: python3 -I g5_koide.py > g5_koide.txt

A Z3 ring of three trains (g4 P6) makes the springs, so the masses squared (2 - 2 cos w ~ w^2, the sine ~ w at
small w), linear in cos(phi - 2 pi j / 3): m_j^2 = a + 2 b cos(...), a >= 2 b >= 0 for every mass to stand. The law
(ALGEBRA.md line 340) read the masses themselves linear (m_j = a + 2 b cos), and Koide's 2/3 needs sqrt m linear.
A grid in b / a and phi (floats: a reading, no act); nature's leptons for the record.
"""

import math


def q(ms):
    return sum(ms) / sum(math.sqrt(m) for m in ms) ** 2


def scan(power):
    best = (0.0, None)
    worst = (1.0, None)
    for i in range(0, 501):
        r = 0.5 * i / 500  # b / a up to 1/2, every mass >= 0
        for k in range(0, 721):
            phi = 2 * math.pi * k / 720
            base = [1 + 2 * r * math.cos(phi - 2 * math.pi * j / 3) for j in range(3)]
            if min(base) < 0:
                continue
            ms = [x**power for x in base]
            if min(ms) <= 0 and max(ms) <= 0:
                continue
            v = q(ms)
            if v > best[0]:
                best = (v, (r, phi))
            if v < worst[0]:
                worst = (v, (r, phi))
    return worst, best


def main():
    lines = []
    for label, power in (
        ("m^2 linear (a Z3 ring of trains, g4 P6)", 0.5),
        ("m linear (the law's line 340)", 1.0),
        ("sqrt m linear, b / a <= 1/2", 2.0),
    ):
        (lo, _), (hi, at) = scan(power)
        lines.append(
            f"{label}: Q in [{lo:.6f}, {hi:.6f}], the top at b / a = {at[0]:.3f}, phi = {at[1]:.3f}"
        )
    me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
    lines.append(
        f"nature's charged leptons: Q = {q([me, mmu, mtau]):.6f} (Koide's 2/3 = {2 / 3:.6f}), reached with sqrt m "
        "linear only at b / a = 1 / sqrt 2 > 1/2"
    )
    lines.append(
        f"the axis split's sum rule (g4 P2, P3: mu = 0, +-g, equal steps in m^2): (m_e^2 + m_tau^2) / 2 = "
        f"{(me**2 + mtau**2) / 2:.4e} MeV^2 against m_mu^2 = {mmu**2:.4e}, a factor "
        f"{(me**2 + mtau**2) / 2 / mmu**2:.1f}"
    )
    print("\n".join(lines))


if __name__ == "__main__":
    main()
