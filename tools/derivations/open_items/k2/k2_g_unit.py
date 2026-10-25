"""Hand K2, the Link unit G (BRIEF_k (b)(i)): measured on the engine's primitives, integers only.

The Link's factor Q_ij = (G^2 (Gamma - t)^2 + Gamma^2 div 2) div Gamma^2 (core/rule3.link_factor), the turn's
factor odd_rounded(angle p_0, Gamma) (core/paces.turn_factor) and the Link's phase pair (plane.sign_pairs):
(1) exact at the vacuum's paces (t = 0, p_0 = Gamma, n = 0) at every G from 1; (2) the least G at which one
level of tension moves Q by one unit, the closed form G^2 > Gamma^2 / (2 (2 Gamma - 1)); (3) the ties of the
rounding over every tension; (4) the least G exact at every tension (G a multiple of Gamma); (5) the bits G
adds to the wall 6 den Gamma^2 G^2.

Run: PYTHONPATH=<worktree>/src python tools/derivations/k2/k2_g_unit.py > tools/derivations/k2/k2_g_unit.txt
"""

from __future__ import annotations

import json

from event_universe.core.ports import LINK_UNIT
from event_universe.core.rule3 import division_forward, link_factor, wall_of
from event_universe.core.paces import turn_factor
from event_universe.plane import sign_pairs


def isqrt_floor(n: int) -> int:
    from event_universe.core.rule3 import largest_below

    return largest_below(n)


def least_resolving(gamma: int) -> tuple[int, int]:
    """The least G with link_factor(gamma, G, 1) != G^2 (one level of tension resolved), by scan, and the closed form's least G with G^2 (2 Gamma - 1) > Gamma^2 div 2 ... exactly: 2 G^2 (2 Gamma - 1) > Gamma^2."""
    g = 1
    while int(link_factor(gamma, g, 1)) == g * g:
        g += 1
    closed = 1
    while 2 * closed * closed * (2 * gamma - 1) <= gamma * gamma:
        closed += 1
    return g, closed


def ties(gamma: int, g: int) -> int:
    """The tensions t in [0, Gamma) at which G^2 (Gamma - t)^2 mod Gamma^2 is exactly Gamma^2 div 2 (a tie of the half-up rounding)."""
    wall = gamma * gamma
    half = int(division_forward(wall, 2, 0)[0])
    count = 0
    for t in range(gamma):
        if int(division_forward(g * g * (gamma - t) ** 2, wall, 0)[1]) == half:
            count += 1
    return count


def exact_everywhere(gamma: int, g: int) -> bool:
    """Whether Q is G^2 (Gamma - t)^2 / Gamma^2 exactly (remainder 0) at every tension t in [0, Gamma)."""
    wall = gamma * gamma
    for t in range(gamma):
        if int(division_forward(g * g * (gamma - t) ** 2, wall, 0)[1]) != 0:
            return False
    return True


def least_exact(gamma: int) -> int:
    g = 1
    while not exact_everywhere(gamma, g):
        g += 1
    return g


def main() -> None:
    out: dict[str, object] = {"engine_G": LINK_UNIT}
    for gamma in (1000, 1021, 6000):
        row: dict[str, object] = {}
        row["Q_at_vacuum_equals_G2_for_G_1_to_64"] = all(
            int(link_factor(gamma, g, 0)) == g * g for g in range(1, 65)
        )
        scan, closed = least_resolving(gamma)
        row["least_G_resolving_one_level_scan"] = scan
        row["least_G_resolving_one_level_closed_form"] = closed
        row["Q_at_t1_for_G_15_16_17"] = [int(link_factor(gamma, g, 1)) for g in (15, 16, 17)]
        row["Q_change_per_level_times_1000_at_G16"] = int(
            division_forward(2 * 256 * (gamma - 1) * 1000, gamma * gamma, 0)[0]
        )  # 2 G^2 (Gamma - 1) / Gamma^2 in thousandths
        row["tension_per_unit_of_Q_at_G16_levels_x1000"] = int(
            division_forward(gamma * 1000, 2 * 256, 0)[0]
        )  # Gamma / (2 G^2)
        row["ties_over_all_t_at_G16"] = ties(gamma, 16)
        row["ties_over_all_t_at_G1"] = ties(gamma, 1)
        row["least_G_exact_at_every_tension"] = least_exact(gamma) if gamma <= 1021 else None
        row["G_equal_Gamma_exact_at_every_tension"] = exact_everywhere(gamma, gamma)
        row["turn_factor_at_vacuum_equals_angle_for_angles_-5000..5000"] = all(
            int(turn_factor(a, gamma, gamma)) == a for a in range(-5000, 5001)
        )
        out[f"Gamma_{gamma}"] = row
    # the Link's phase pair at the vacuum (n = 0) and at one level (n = 1) for light and the lift at two dens
    for den, num in ((1021, 1021), (1021, 779), (348893, 348893), (348893, 348893 - 89532)):
        row = {}
        for g in (1, 16, 1000):
            factors = (g * g,) * 6
            even0, odd0 = sign_pairs((num, den), 1000, factors, (0,) * 6)
            even1, odd1 = sign_pairs((num, den), 1000, factors, (1,) * 6)
            row[f"G_{g}"] = {
                "n0_even_equals_2numG2": all(int(e) == 2 * num * g * g for e in even0),
                "n0_odd": [int(o) for o in odd0][:1],
                "n1_even": int(even1[0]),
                "n1_odd": int(odd1[0]),
            }
        out[f"phase_pair_den_{den}_num_{num}"] = row
    # the wall's bits per G
    bits = {}
    for den in (1021, 348893, 1655909141, 4471099877, 15162856759112389):
        bits[str(den)] = {
            f"G_{g}": int(wall_of(den, 1000, g)).bit_length() for g in (1, 16, 32, 1000)
        }
    out["wall_bits_at_Gamma_1000"] = bits
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
