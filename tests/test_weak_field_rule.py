"""The law's rule with the weak field (ALGEBRA.md #the-line): the rotation at k = 0, light's dispersion at a level, and the loader's int64 bound from the rule's own total. COMPUTATION; no pin."""

from __future__ import annotations

import math

import pytest

from event_universe.core.rule3 import coefficients


def test_the_rotation_and_the_dispersion_carry_the_clocks_second_order_weight():
    # 2 cos omega' = (6 R + S) / w at k = 0 = 2 - 2 f (1 - num / den), f = p_0^2 / Gamma^2 = ((Gamma - c)^2 + c^2) / Gamma^2: the clock's square, the Link's pace cancelling at k = 0 (ALGEBRA.md #the-paces)
    gamma = 10_000
    for num, den in ((800, 809), (3200, 3227)):
        for c in (0, 500, 2000, 5000):
            f = ((gamma - c) ** 2 + c * c) / gamma**2
            (read, _, _), self_coefficient, wall = coefficients(num, den, gamma, c)
            rotation = 2 - 2 * f * (1 - num / den)
            assert (6 * read + self_coefficient) / wall == pytest.approx(rotation, abs=1e-12)
    # light on a chain (four self reads): cos omega' = 1 - f (1 - cos k) / 3 with f the Link's pace squared over Gamma^2, (Gamma - 2 c)^2 / Gamma^2: the level enters the Link twice (ALGEBRA.md #the-paces)
    for c in (0, 2000):
        f = ((gamma - 2 * c) / gamma) ** 2
        (read, _, _), self_coefficient, wall = coefficients(1, 1, gamma, c)
        for k in (0.302, math.pi / 2):
            s6 = 2 * math.cos(k) + 4
            cos_omega = (read * s6 + self_coefficient) / (2 * wall)
            assert cos_omega == pytest.approx(1 - f * (1 - math.cos(k)) / 3, abs=1e-12)
