"""The four-vector click (ALGEBRA.md #the-primitives): a click moves a quantum's count and its momentum, and every click line reads the momentum its quantum travelled with, in the body's language."""

from __future__ import annotations

from event_universe.events.detector_law import DetectorLawSimulation


def test_the_direction_is_the_sign_per_axis():
    assert DetectorLawSimulation.direction_of([-5, 0, 7]) == [-1, 0, 1]
    assert DetectorLawSimulation.direction_of([0, 0, 0]) == [0, 0, 0]
