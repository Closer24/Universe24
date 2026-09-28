"""The law's rule with the weak field (ALGEBRA.md #the-line): the loader's int64 bound from the rule's own total (the rotation and the dispersion at a level are tests/test_rule3.py's exact test of the conformal pace). COMPUTATION; no pin."""

from __future__ import annotations

import pytest

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
    # the loader refuses the world that exceeds it, naming the total
    document = content_chain(12, PERIODIC, range(12), 250, gamma=1_000_000)
    document["amplitude_bound"] = 1 << 20
    with pytest.raises(ValueError, match=r"6 A R \+ A \|S\| \+ w \(A \+ 1\).*not below 2\^63"):
        parse_nature_beam_world(document)
