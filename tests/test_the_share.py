"""The count is the record's share (ALGEBRA.md #the-count-is-the-records-share): the share e_i = 3 den (now^2 + before^2) - num now S_6(before) changes over one step of Rule3 by exactly SUM_j F_ij, F_ij = num (now_i before_j - before_i now_j), at the pair the step started from, in rationals; the engine reads the same currents from the record and a detector's click is its net front inflow, never a Node; the exact bands (ALGEBRA.md #rule3): 2 cos omega an integer gives the periods 6, 4 and 3 with no remainder."""

from __future__ import annotations

import random
from fractions import Fraction

import numpy as np
import pytest

from event_universe import node
from event_universe.core.ports import Wrap
from event_universe.core.rule3 import coefficients, rule3
from event_universe.loader.derived import Row, family_rules
from event_universe.loader.world import kind_of
from event_universe.reports import inflow

GAMMA, NODES = 10_000, 12


def ring_sum(values: list[Fraction]) -> list[Fraction]:
    """S_6 on a ring with four self reads: the six Ports' arrivals of a Node."""
    return [4 * values[i] + values[i - 1] + values[(i + 1) % NODES] for i in range(NODES)]


@pytest.mark.parametrize("pair", [(24, 24), (16, 24), (5000, 10000)])
def test_the_share_changes_by_the_currents_at_the_pair_the_step_started_from(pair):
    """E_i / 2 = 3 den (now^2 + before^2) - num now S_6(before): its change over one interval of Rule3 (exact in rationals) is SUM_j F_ij with F_ij = num (now_i before_j - before_i now_j) at every Node, the currents at the pair the step started from (issue #1495 finding 6; the paper writer's finding, #1538 comment 5921398465), and not at the pair the step left."""
    num, den = pair
    (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, 0)
    draw = random.Random(3)
    now = [Fraction(draw.randint(-1000, 1000)) for _ in range(NODES)]
    before = [Fraction(draw.randint(-1000, 1000)) for _ in range(NODES)]
    ring = ring_sum(now)
    nxt = [(read * ring[i] + self_coefficient * now[i] - wall * before[i]) / wall for i in range(NODES)]

    def share(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
        return [3 * den * (a[i] ** 2 + b[i] ** 2) - num * a[i] * ring_sum(b)[i] for i in range(NODES)]

    def flux(a: list[Fraction], b: list[Fraction]) -> list[Fraction]:
        return [num * (a[i] * ring_sum(b)[i] - b[i] * ring_sum(a)[i]) for i in range(NODES)]

    change = [share(nxt, now)[i] - share(now, before)[i] for i in range(NODES)]
    assert change == flux(now, before) and change != flux(nxt, now)


def test_the_engine_reads_the_currents_from_the_record_through_the_six_ports():
    """The currents the engine reads (`node.currents_of`) are F_ij = num (now_i before_j - before_i now_j) through each Port, both level pairs added, on the record as it stands and nothing kept beside it."""
    (quanta,) = family_rules([Row("quanta", (5, 7), 1, 1, False, False, None, 0)])
    draw, shape, wrap = np.random.default_rng(2), (3, 3, 3), Wrap(True, True, True)
    zero = node.zeros(shape, kind_of(63))
    real, second = (node.Record(*draw.integers(-50, 50, (2, *shape)), zero) for _ in range(2))
    through = node.currents_of(quanta.pair[0], [real, second], wrap)
    for port, (axis, side) in enumerate((a, s) for a in range(3) for s in (1, -1)):
        expected = sum(
            5 * (r.now * np.roll(r.before, -side, axis) - r.before * np.roll(r.now, -side, axis))
            for r in (real, second)
        )
        assert np.array_equal(through[port], expected)


@pytest.mark.parametrize(("pair", "period"), [((1, 2), 6), ((0, 1), 4), ((-1, 2), 3)])
def test_the_exact_bands_turn_with_no_remainder(pair, period):
    """The exact bands: a Node at rest in the vacuum (its six reads its own level) turns by 2 cos omega = 2 num / den; the three integer rotations 1, 0 and -1 close in 6, 4 and 3 intervals with the remainder 0 at every step."""
    num, den = pair
    (read, _, _), self_coefficient, wall = coefficients(num, den, GAMMA, 0)
    before, now = 0, 1_000
    for _ in range(1, period + 1):
        nxt, carry = rule3((read,) * 3, (2 * now,) * 3, self_coefficient, wall, now, before, 0)
        assert carry == 0
        before, now = now, nxt
    assert (before, now) == (0, 1_000)


def test_a_detectors_click_is_its_net_inflow_through_its_front_boundary_alone():
    """The click (ALGEBRA.md #the-count-is-the-records-share; the owner's word of 2026-09-30, no click names a Node): a detector's Nodes are one region; its report is the net current into it through the Ports leading in from the declared board outside the region, signed, in the current's units, and none through a Port between two of its Nodes (a hop inside the region is no entry) nor through a Port beyond the board."""
    nodes = np.array([True, True, False]).reshape(3, 1, 1)
    wrap, zero = Wrap(False, False, False), np.zeros((3, 1, 1), dtype=np.int64)
    inward = np.array([0, 40, 0]).reshape(3, 1, 1)  # a current into Node 1 through one Port
    board = np.ones((3, 1, 1), dtype=bool)  # every Node declared, none grown

    def seen(port: int) -> int:
        through = tuple(inward if p == port else zero for p in range(6))
        return inflow(nodes, through, wrap, nodes, board)

    assert seen(0) == 40  # through +x from Node 2, outside the region
    assert seen(1) == 0  # through -x from Node 0, inside the region: a hop, no entry
    assert seen(2) == 0  # +y leads beyond the board (one Node across y): no boundary Port
