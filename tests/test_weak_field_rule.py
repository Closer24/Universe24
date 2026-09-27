"""THE LAW'S RULE WITH EINSTEIN'S WEAK FIELD (ALGEBRA.md #the-line): the rotation at k = 0 is
the clock's second-order weight, light's dispersion at a level f = (p / Gamma)^2, and the loader's
int64 bound from the rule's own total (Gamma 10^4, A 2^20, the muon's pair at two thirds of the
room). Every number a COMPUTATION on the rule's integers; no pin. The rule's three integers
against the algebra's line, the vacuum and one step's inverse are test_rule3's and test_node_clock's."""

from __future__ import annotations

import math

import pytest

from event_universe.core.rule3 import coefficients, rule_total_bound
from event_universe.world_files import parse_nature_beam_world
from tests.test_node_clock import PERIODIC, content_chain


def test_the_rotation_and_the_dispersion_carry_the_clocks_second_order_weight():
    # 2 cos omega' = (6 R + S) / w at k = 0 = 2 - (1 + f)(1 - num / den), f = (p / Gamma)^2
    gamma = 10_000
    for num, den in ((800, 809), (3200, 3227)):
        for c in (0, 500, 2000, 5000):
            f = ((gamma - c) / gamma) ** 2
            (read, _, _), self_coefficient, wall = coefficients(num, den, gamma, c)
            assert (6 * read + self_coefficient) / wall == pytest.approx(
                2 - (1 + f) * (1 - num / den), abs=1e-12
            )
    # light on a chain (four self reads): cos omega' = 1 - f (1 - cos k) / 3 (9.62 (1))
    for c in (0, 2000):
        f = ((gamma - c) / gamma) ** 2
        (read, _, _), self_coefficient, wall = coefficients(1, 1, gamma, c)
        for k in (0.302, math.pi / 2):
            s6 = 2 * math.cos(k) + 4
            cos_omega = (read * s6 + self_coefficient) / (2 * wall)
            assert cos_omega == pytest.approx(1 - f * (1 - math.cos(k)) / 3, abs=1e-12)


def test_the_int64_bound_from_the_rules_own_total_at_the_integers_of_the_algebra():
    gamma, room = 10_000, 1 << 63
    assert rule_total_bound(800, 809, gamma, 128, 1 << 20, True) < room // 6
    assert rule_total_bound(3200, 3227, gamma, 2, 1 << 20, True) < room  # two thirds of the room
    assert rule_total_bound(3200, 3227, gamma, 2, 1 << 21, True) > room  # 2^21 refused there
    assert rule_total_bound(800, 809, 1_000_000, 64, 1 << 20, True) > room  # Gamma 10^6 refused
    assert rule_total_bound(1, 1, 1, 0, 1 << 20, False) == 6 * (1 << 20) + 3 * ((1 << 20) + 1)
    # the loader refuses the world that exceeds it, naming the total
    document = content_chain(12, PERIODIC, range(12), 250, gamma=1_000_000)
    document["amplitude_bound"] = 1 << 20
    with pytest.raises(ValueError, match=r"6 A R \+ A \|S\| \+ w \(A \+ 1\).*not below 2\^63"):
        parse_nature_beam_world(document)
