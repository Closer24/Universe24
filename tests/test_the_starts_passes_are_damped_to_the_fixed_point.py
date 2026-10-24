"""The start's passes are the loader's tool, damped to the fixed point the law names (features/start/rests `held_rests`, `damped`; the derivation hand's reading of 2026-10-24: the law states the fixed point, the body standing where the sources return themselves, and names no pass): where the undamped lay-rest passes cycle, the next pass's levels are the integer mean of the pass's input and its output with the remainder carried, the same map and the same fixed point, so a map whose undamped passes cycle settles to its fixed point, and a map with no fixed point is refused by the same name as before. The map faked in place of the rows' rest, the loop's own sentences the test's."""

import numpy as np
import pytest

from event_universe.features import start
from event_universe.features.start import rests

WRAP = None  # the loop hands it on; the faked rest reads nothing of it


def faked(mapping):  # type: ignore[no-untyped-def]
    """`settled_rows` faked: one holder whose rest is `mapping` of the levels the pass began from (carried in the row's counts by `booked`)."""

    def settled_rows(holders, wrap, width, gamma, unit, seeds=()):  # type: ignore[no-untyped-def]
        levels = mapping(holders[0][0])
        return [start.FieldAtRest(levels, levels, 1, 0, levels)]

    return settled_rows


def booked(levels):  # type: ignore[no-untyped-def]
    return [(levels[0], (999, 1000), 1, 0, (), 1)], []


def test_a_lay_rest_map_that_cycles_undamped_settles_to_its_fixed_point(monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(
        rests, "settled_rows", faked(lambda b: 10 - b)
    )  # the 2-cycle 0, 10 about the fixed point 5
    seed = [np.zeros((1, 1, 3), dtype=np.int64)]
    (field,) = rests.held_rests(booked, seed, WRAP, 63, 1000, 1)  # type: ignore[arg-type]
    assert field.levels.tolist() == [
        [[5, 5, 5]]
    ]  # the fixed point, b = F(b), the mean of the cycle's two states
    assert field.levels.dtype == np.int64  # the levels keep their kind through the damped passes


def test_a_map_with_no_fixed_point_is_refused_by_name_under_the_damped_passes(monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setattr(
        rests, "settled_rows", faked(lambda b: (b + 4) % 8)
    )  # no b with b = F(b) in the integers
    with pytest.raises(ValueError, match="finds no fixed point"):
        rests.held_rests(booked, [np.zeros((1, 1, 1), dtype=np.int64)], WRAP, 63, 1000, 1)  # type: ignore[arg-type]


def test_the_damped_pass_is_the_integer_mean_with_the_remainder_carried():  # type: ignore[no-untyped-def]
    a, b = [np.array([0, 3, 7], dtype=np.int64)], [np.array([10, 4, 7], dtype=np.int64)]
    levels, carries = rests.damped(a, b, [np.zeros(3, dtype=np.int64)])
    assert levels[0].tolist() == [5, 3, 7] and carries[0].tolist() == [0, 1, 0]
    again, carries = rests.damped(levels, b, carries)
    assert again[0].tolist() == [7, 4, 7] and carries[0].tolist() == [
        1,
        0,
        0,
    ]  # (5 + 10) div 2, (3 + 4 + 1) div 2
