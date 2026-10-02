"""The click written on the GameBoard (ALGEBRA.md #the-click-is-the-meeting; HIGHLIGHTS.md, the owner's decision of 2026-10-02: after a click the paths are cancelled on the GameBoard, not in the clicks' books, Rule3 kept): the instrument's two acts outside Rule3, taken by the engine's loop at the instruments' reports from outside the Node, as the lay and the receding face are; the Node knows nothing of them and no family of clicks exists. The draw: the instrument's generator, declared in the world file with its seed, x <- (multiplier x + increment) mod modulus by the division act, and one index among integer weights, the first whose cumulative weight exceeds x mod total (the lower index on a tie); the run is deterministic per seed. The take: the record's arrived levels at the one Node the credited quantum entered through set to 0, every line of the record there at the state of a Node with no level, exactly as the receding face removes a share (the advisor's second hand: for a spread record the form is quadratic, and subtracting one quantum's levels where less than a quantum stands would add form instead of removing it), the local hole, which spreads by Rule3 alone as an event (no front is sent: a family has one level field, and an act ending a record's shares on arrival would end every other quantum's wave it reached); the record's count, not the levels, goes down by one."""

from __future__ import annotations

from typing import Any

import numpy as np

from event_universe.core.rule3 import division_forward


def drawn(
    state: int, multiplier: int, increment: int, modulus: int, weights: list[int]
) -> tuple[int, int]:
    """One draw of the instrument: the generator's next state x = (multiplier x + increment) mod modulus, and among the weights (each at or above 0, their total above 0) the first index whose cumulative weight exceeds x mod total, the lower index on a tie; returns the index and the state after."""
    state = int(division_forward(multiplier * state + increment, modulus, 0)[1])
    total = sum(weights)
    if total <= 0:
        raise ValueError("the instrument draws among weights whose total is above 0")
    pick = int(division_forward(state, total, 0)[1])
    reached = 0
    for index, weight in enumerate(weights):
        reached += weight
        if pick < reached:
            return index, state
    return len(weights) - 1, state


def taken(levels: list[Any], at: Any) -> list[Any]:
    """The hole of one click: every level of the record (the lines' now, before and remainder) at the Nodes of the mask `at` set to 0, the state of a Node with no level, every other Node as it stands; the credited quantum's share leaves the record there as a share leaves through a receding face."""
    return [np.where(at, 0, level) for level in levels]
