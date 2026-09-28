"""The law's rule with the weak field (ALGEBRA.md #the-line): the loader's int64 bound from the rule's own total (the rotation and the dispersion at a level are tests/test_rule3.py's exact test of the conformal pace). COMPUTATION; no pin."""

from __future__ import annotations

from event_universe.core.rule3 import rule_total_bound
from event_universe.world_files import parse_nature_beam_world
from tests.bodies import content_chain
from tests.worlds import PERIODIC


def test_the_int64_bound_from_the_rules_own_total_at_the_integers_of_the_algebra():
    gamma, room = 10_000, 1 << 63
    assert rule_total_bound(800, 809, gamma, 128, 1 << 20, True) < room // 6
    assert rule_total_bound(3200, 3227, gamma, 2, 1 << 20, True) < room  # two thirds of the room
    assert rule_total_bound(3200, 3227, gamma, 2, 1 << 21, True) > room  # 2^21 refused there
    assert rule_total_bound(800, 809, 1_000_000, 64, 1 << 20, True) > room  # Gamma 10^6 refused
    assert rule_total_bound(1, 1, 1, 0, 1 << 20, False) == 6 * (1 << 20) + 3 * ((1 << 20) + 1)
    # the loader derives A as the largest level whose total fits at (Gamma - 1) div 2 over the world's pairs (ALGEBRA.md #a-familys-declaration): every pair's total fits at A, and one pair's exceeds the room at A + 1
    document = content_chain(12, PERIODIC, range(12), 250, gamma=1_000_000)
    world = parse_nature_beam_world(document)
    pairs = [tuple(f["pair"]) for f in document["universe"]]
    totals = [rule_total_bound(*pair, 1_000_000, 499_999, world.amplitude_bound, True) for pair in pairs]
    assert all(total < room for total in totals)
    assert any(
        rule_total_bound(*p, 1_000_000, 999_999, world.amplitude_bound + 1, True) >= room for p in pairs
    )
