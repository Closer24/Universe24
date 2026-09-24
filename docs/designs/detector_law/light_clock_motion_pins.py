"""The two-body light clock in motion, as declared (COMPUTATION, before any run).

Two blocks of the massive kind pushed together at k = 3 on a chain, their
separation L the declared cells' separation (rigid; DECLARATIONS.md section 13),
one emitting toward the other, the other's click the receive, the record returning
the same way: the round trip in the lattice's intervals is L / (c - v) + L / (c + v)
= 2 L gamma^2 / c (R2's two transits summed, `coupled_mode_pins.py` (f)), and a
block's own clock runs at 1 / gamma_m of its rest rate at the massive kind's cone
c_eff (the one formula's well limit, ALGEBRA.md 8.4). So the round trip in the
bodies' OWN count is N_0 gamma^2 / gamma_m along the motion, and across it
(L / sqrt(c^2 - v^2) each way) N_0 gamma / gamma_m, N_0 = 2 L / c the count at
rest. Einstein's 1 and 1 (Highlights 5.4, the owner's "five") needs the along
separation to contract by gamma, which a declared rigid separation does not do
(Reviewer 3's algebra in the same line: a medium, gamma^2 along and gamma across,
in the lattice's intervals). Printed: gamma, gamma_m per pair, the two ratios, the
round trip against R2's transits. gamma_m is the one formula's, the same expression as
coupled_mode_pins.py (c) for row 4b and as row 4a's, so the three rows carry one gamma_m.

    PYTHONPATH=src python docs/designs/detector_law/light_clock_motion_pins.py
"""

import math

C_PACE = 1 / math.sqrt(3)
V_PACE = 1 / 3
GAP = 60


def gammas(num, den):
    """gamma at light's cone and gamma_m at the massive kind's exact cone for the pair: the
    SAME one formula as `coupled_mode_pins.py` (c) (row 4b's pin) and the muon's row 4a,
    c_eff^2 = (num / den) (omega_0 / sin omega_0) c^2 and gamma_m = 1 / sqrt(1 - v^2 / c_eff^2),
    so the three rows carry one gamma_m (Reviewer 3's line, 01:55Z)."""
    omega_0 = math.acos(num / den)
    c_eff2 = math.cos(omega_0) * (omega_0 / math.sin(omega_0)) * C_PACE**2
    gamma = 1 / math.sqrt(1 - V_PACE**2 / C_PACE**2)
    gamma_m = 1 / math.sqrt(1 - V_PACE**2 / c_eff2)
    return omega_0, math.sqrt(c_eff2) / C_PACE, gamma, gamma_m


if __name__ == "__main__":
    t_plus = GAP / (C_PACE - V_PACE)
    t_minus = GAP / (C_PACE + V_PACE)
    rest = 2 * GAP / C_PACE
    gamma = 1 / math.sqrt(1 - V_PACE**2 / C_PACE**2)
    print(
        f"the round trip along the motion at k = 3 in the lattice's intervals: {t_plus:.1f} + {t_minus:.1f} = "
        f"{t_plus + t_minus:.1f} = 2 L gamma^2 / c ({2 * GAP * gamma**2 / C_PACE:.1f}) against N_0 = 2 L / c = {rest:.2f}"
        f" at rest; across the motion 2 L / sqrt(c^2 - v^2) = {2 * GAP / math.sqrt(C_PACE**2 - V_PACE**2):.1f} = N_0 gamma"
    )
    for num, den in ((800, 809), (156, 157)):
        omega_0, ratio, g, g_m = gammas(num, den)
        print(
            f"the pair [{num}, {den}] (omega_0 {omega_0:.5f}, c_eff / c {ratio:.5f}): gamma {g:.5f}, gamma_m {g_m:.5f};"
            f" the moving clock's OWN count of the round trip over its rest count: ALONG gamma^2 / gamma_m = {g * g / g_m:.4f},"
            f" ACROSS gamma / gamma_m = {g / g_m:.4f}; Einstein's 1 and 1 needs the along separation contracted by gamma"
        )
