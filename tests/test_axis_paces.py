"""The four paces: a reading family's pace on the axis a is p_a = p_0 - t_a (the reads' aa parts halved, the remainder kept at the Node), the rule's reads along a weigh 2 p_a^2 num, and the inverse reads the same paces. HOST; no pin."""

from __future__ import annotations

import numpy as np
import pytest

from event_universe.core.rule3 import coefficients
from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import parse_nature_beam_world
from tests.bodies import KIND, paces_world, parts_of
from tests.bodies import PACES_SHAPE as SHAPE

# THE START left out in every test of this module (the fixture): the fixture's board is periodic on every axis, which has
# no rest under a source (ALGEBRA.md #the-generator (g)), and the recorded seedings (tests/seeds.json) bind the board
pytestmark = pytest.mark.usefixtures("the_loads_hold_alone")


GAMMA = 10_000


def axis_sums(a: np.ndarray) -> list[np.ndarray]:
    return [np.roll(a, 1, axis=axis) + np.roll(a, -1, axis=axis) for axis in range(3)]


def test_a_planted_tensor_part_bends_the_rule_per_axis_and_the_inverse_reads_the_same_paces():
    """Gravity's xx part set to 40 at every Node of a slab (a sourced part, not silent): a
    matter record's step is the rule with p_x = p_0 - 20 there and p_y = p_z = p_0, the
    isotropic rule elsewhere, the remainder in [0, w); the wheel at a Node of the slab reads
    the five coefficients; one interval back restores the rows exactly."""
    simulation = DetectorLawSimulation(parse_nature_beam_world(paces_world()))
    gravity = parts_of(simulation, "clicks")
    matter = [family.name for family in simulation.families].index("matter")
    assert simulation._axis_contents(matter) is None  # every tensor part silent: isotropic
    xx = gravity[4]
    assert xx.part == 4 and xx.silent
    xx.now[7:9, :, :] = 40
    xx.before[7:9, :, :] = 40
    xx.silent = False
    simulation._sourced_ever[(gravity[0].family, 4)] = True
    simulation._axis_effective.clear()
    rng = np.random.default_rng(3)
    now = rng.integers(-(1 << 16), 1 << 16, size=tuple(SHAPE), dtype=np.int64)
    before = rng.integers(-(1 << 16), 1 << 16, size=tuple(SHAPE), dtype=np.int64)
    live = simulation.planted_record(matter, now.copy(), before.copy())
    content = simulation._effective_content(matter).copy()
    axis_contents = simulation._axis_contents(matter)
    assert axis_contents is not None
    assert int(axis_contents[0][7, 0, 0]) == 20 and int(axis_contents[0][2, 0, 0]) == 0
    assert not axis_contents[1].any() and not axis_contents[2].any()
    simulation._advance(live)
    sums = axis_sums(now)
    num_all, den_all = simulation.pair_arrays(matter)  # the well's pair at the body's Nodes
    for node in ((7, 2, 2), (8, 5, 1), (2, 3, 3), (4, 4, 4)):
        t = (int(axis_contents[0][node]), 0, 0)
        c = int(content[node])
        num, den = int(num_all[node]), int(den_all[node])
        reads, self_coefficient, wall = coefficients(num, den, GAMMA, c, t)
        total = sum(reads[a] * int(sums[a][node]) for a in range(3))
        total += self_coefficient * int(now[node]) - wall * int(before[node])
        expected = total // wall
        assert int(live.now[node]) == expected, node
        assert 0 <= int(live.remainder[node]) == total - wall * expected < wall, node
    # the wheel at a slab Node reads the five coefficients' gcd
    step, wheel = simulation.wheel_at(matter, (7, 2, 2))
    reads, self_coefficient, wall = coefficients(
        *KIND, GAMMA, int(content[7, 2, 2]), (20, 0, 0)
    )  # the cube fixture's kind
    from math import gcd

    assert step == gcd(wall, self_coefficient, *reads) and wheel == wall // step
    # the inverse reads the same paces (the tensor's before level, the remainder stepped back)
    simulation._advance_inverse(live)
    assert np.array_equal(live.now, now) and np.array_equal(live.before, before)
    assert not live.remainder.any()
    assert simulation.leaks() == []
