"""THE LAW'S RULE WITH EINSTEIN'S WEAK FIELD (ALGEBRA.md 9.57 (1) to (3), 9.61 (3), 9.62 (1);
the model owner's "switch" of record 2024; BUILD.md section 26 item 44): the rule's three
integers at a Node, (R, S, w), against the algebra's line written out; at c = 0 the vacuum's
rule term for term, the levels the plain rule's bit for bit and the remainders 2 Gamma^2
times its; the step and its inverse one to one under a level; the rotation at k = 0 the
clock's second-order weight; light's dispersion at a level f = (p / Gamma)^2; the loader's
int64 bound from the rule's own total (the integers of 9.61 (3): Gamma 10^4, A 2^20, the
muon's pair at two thirds of the room). Every number a COMPUTATION on the rule's integers;
no pin."""

from __future__ import annotations

import math

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients, rule_total_bound
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.test_flux_reading import planted
from tests.test_node_clock import GAMMA, PERIODIC, content_chain, six_reads


def test_the_three_integers_are_the_algebras_line_and_the_vacuum_is_the_plain_rule():
    gamma = 10_000
    for num, den in ((1, 1), (800, 809), (3200, 3227)):
        for c in (0, 64, 2000, 9999):
            p = gamma - c
            (read, _, _), self_coefficient, wall = coefficients(num, den, gamma, c)
            assert read == 2 * p * p * num
            assert (
                self_coefficient
                == 12 * den * gamma**2 - 6 * (p * p + gamma**2) * (den - num) - 12 * num * p * p
            )
            assert wall == 6 * den * gamma**2
            (plain_read, _, _), plain_self, plain_wall = coefficients(
                num, den, gamma, c, weak_field=False
            )
            assert (plain_read, plain_self, plain_wall) == (p * num, 6 * den * c, 3 * den * gamma)
        # the vacuum: 2 Gamma^2 times the plain rule, so the levels agree bit for bit
        (read, _, _), self_coefficient, wall = coefficients(num, den, gamma, 0)
        assert (read, self_coefficient, wall) == (2 * gamma**2 * num, 0, 2 * gamma**2 * 3 * den)
    # arrays as integers
    num = np.array([1, 800], dtype=object)
    den = np.array([1, 809], dtype=object)
    content = np.array([0, 64], dtype=object)
    (read, _, _), self_coefficient, wall = coefficients(num, den, 10_000, content)
    assert list(read) == [2 * 10_000**2, 2 * 9936**2 * 800]
    assert list(wall) == [6 * 10_000**2, 6 * 809 * 10_000**2]
    assert self_coefficient[0] == 0


def test_one_step_on_random_rows_is_the_rule_and_inverts_and_the_vacuum_remainder_is_two_gamma_squared():
    rng = np.random.default_rng(7)
    quanta = 250
    for family, (num, den) in ((0, (1, 1)), (1, (800, 809))):
        rows_now = rng.integers(-(1 << 20), 1 << 20, size=(12, 1, 1), dtype=np.int64)
        rows_before = rng.integers(-(1 << 20), 1 << 20, size=(12, 1, 1), dtype=np.int64)
        (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, quanta)
        remainder = rng.integers(0, wall, size=(12, 1, 1), dtype=np.int64)
        simulation = DetectorLawSimulation(
            parse_nature_beam_world(content_chain(12, PERIODIC, range(12), quanta))
        )
        live = planted(simulation, family, rows_now, rows_before, remainder)
        state = (live.now.copy(), live.before.copy(), live.remainder.copy())
        simulation._advance(live)
        reads = six_reads(rows_now, True)
        for x in range(12):
            total = read * reads[x] + self_coefficient * int(rows_now[x, 0, 0])
            total -= wall * int(rows_before[x, 0, 0])
            total += int(remainder[x, 0, 0])
            assert int(live.now[x, 0, 0]) == total // wall
            assert int(live.remainder[x, 0, 0]) == total - wall * (total // wall)
        simulation._advance_inverse(live)
        assert all(
            np.array_equal(a, b)
            for a, b in zip((live.now, live.before, live.remainder), state, strict=True)
        )
        # the vacuum: the plain levels, the remainder 2 Gamma^2 times the plain one from r = 0
        vacuum = DetectorLawSimulation(parse_nature_beam_world(content_chain(12, PERIODIC, [], 1)))
        live = planted(vacuum, family, rows_now, rows_before, np.zeros((12, 1, 1), dtype=np.int64))
        vacuum._advance(live)
        for x in range(12):
            plain = num * reads[x] - 3 * den * int(rows_before[x, 0, 0])
            assert int(live.now[x, 0, 0]) == plain // (3 * den)
            assert int(live.remainder[x, 0, 0]) == 2 * GAMMA * GAMMA * (plain % (3 * den))


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
