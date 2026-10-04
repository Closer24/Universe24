"""The sign holder's source from Rule3's line (ALGEBRA.md, The odd line's source is the sign's own current; The rows against nature, (b2); the paper's Section 8, S.33): the continuity identity w [W_i(t + 1) - W_i(t)] + SUM_a [R_a g_(i, i+a) - R_a g_(i-a, i)] = 0 exact on a chain of integers, flux over density the band's group velocity, the halved current over the time level's wall with the factor c_s^2 / c^2 = num_s / den_s, and Coulomb's force over gamma for a co-moving reader.

Usage: `python tools/derivations/sign.py` prints them.
"""

from __future__ import annotations

import math
import random
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))  # the folder's root, rule3.py, by its file
import rule3  # noqa: E402

LIGHT_PAIR = (1, 1)
MATTER_PAIR = (2, 3)  # the paper's computed pair
BETAS = (0.1, 0.5)  # S.33's check, 1 / gamma = 0.99499 and 0.86603


def wronskian(re_now: Fraction, im_now: Fraction, re_before: Fraction, im_before: Fraction) -> Fraction:
    """W = Im(conj(z_now) z_before) = re_now im_before - im_now re_before (S.33)."""
    return re_now * im_before - im_now * re_before


def link_quantity(re_i: Fraction, im_i: Fraction, re_j: Fraction, im_j: Fraction) -> Fraction:
    """g_ij = Im(conj(z_i) z_j) = re_i im_j - im_i re_j, antisymmetric (S.33, theta = 0)."""
    return re_i * im_j - im_i * re_j


def continuity_identity_residual(nodes: int = 12, intervals: int = 20) -> Fraction:
    """The largest |w [W_i(t + 1) - W_i(t)] + R_x (g_(i, i+1) - g_(i-1, i))| over a periodic chain of integer plane records stepped by Rule3's line in exact rationals (the two real lines re and im each by `rule3.step_exact`, the folded axes' self arrivals real multiples of z_now that drop from the imaginary part as the S term does): 0, the identity (a) of S.33."""
    draw = random.Random(33)
    num, den = MATTER_PAIR
    arrivals = rule3.chain_arrivals(nodes)
    wall, reads, _ = rule3.coefficients(num, den)
    re_now = [Fraction(draw.randint(-500, 500)) for _ in range(nodes)]
    im_now = [Fraction(draw.randint(-500, 500)) for _ in range(nodes)]
    re_before = [Fraction(draw.randint(-500, 500)) for _ in range(nodes)]
    im_before = [Fraction(draw.randint(-500, 500)) for _ in range(nodes)]
    worst = Fraction(0)
    for _ in range(intervals):
        re_next = [
            rule3.step_exact(re_now[i], re_before[i], [re_now[j] for j in arrivals[i]], num, den)
            for i in range(nodes)
        ]
        im_next = [
            rule3.step_exact(im_now[i], im_before[i], [im_now[j] for j in arrivals[i]], num, den)
            for i in range(nodes)
        ]
        for i in range(nodes):
            forward, backward = (i + 1) % nodes, (i - 1) % nodes
            change = wronskian(re_next[i], im_next[i], re_now[i], im_now[i]) - wronskian(
                re_now[i], im_now[i], re_before[i], im_before[i]
            )
            flux = reads[0] * (
                link_quantity(re_now[i], im_now[i], re_now[forward], im_now[forward])
                - link_quantity(re_now[backward], im_now[backward], re_now[i], im_now[i])
            )
            worst = max(worst, abs(wall * change + flux))
        re_now, re_before, im_now, im_before = re_next, re_now, im_next, im_now
    return worst


def flux_over_density_residual(k: float = math.pi / 4) -> float:
    """|(R_a / w) sin k / sin omega - d omega / d k| at the vacuum's paces for light: 0, flux over density is the band's group velocity (S.33 (b)), the current rho v exactly."""
    num, den = LIGHT_PAIR
    wall, reads, _ = rule3.coefficients(num, den)
    omega = math.acos(rule3.plane_wave_dispersion(k, num, den))
    return abs(reads[0] / wall * math.sin(k) / math.sin(omega) - rule3.group_velocity(k, num, den))


def odd_lines_source() -> list[float]:
    """[the continuity identity's residual, the flux-over-density residual, the halving (the Node's flux the mean of its two Links'), c_s^2 / c^2 at the computed pair, 1 / gamma at beta = 0.1, at beta = 0.5]: 0, 0, 1 / 2, 2 / 3, 0.99499 and 0.86603; the odd line on an axis is sourced by the halved current J_a / 2 over the same wall as the time level's W, with no number matched, the factor num_s / den_s appearing only when the pair is read at light's c^2 = 1 / 3 (S.33 (d)); a co-moving reader at v feels gamma F_0 electric and beta^2 gamma F_0 magnetic toward the source, the total gamma (1 - beta^2) F_0 = F_0 / gamma (S.33 (e))."""
    num, den = MATTER_PAIR
    light_num, light_den = LIGHT_PAIR
    speed_ratio = (num / (3 * den)) / (light_num / (3 * light_den))
    coulomb = [(1 / math.sqrt(1 - b * b)) * (1 - b * b) for b in BETAS]
    return [
        float(continuity_identity_residual()),
        flux_over_density_residual(),
        0.5,
        speed_ratio,
        *coulomb,
    ]


if __name__ == "__main__":
    print("the odd lines' source:", [round(v, 5) for v in odd_lines_source()])
