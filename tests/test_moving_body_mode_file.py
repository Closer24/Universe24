"""The mode file of a moving body (ALGEBRA.md #the-generator (e), #the-rows-against-nature (e)): the generator writes the body's two levels under `moving`, the band's top velocity and the proper pair as its clock; the loader's reader takes the levels or refuses a defect by name; a resting body's file carries no levels; the world one open chain with one body of matter of three Nodes at 1000 by its Nodes with their counts."""

import json
import sys

import pytest

from event_universe.loader.mode import moving_levels, period_by_the_rule

sys.path.insert(0, __file__.rsplit("/tests/", 1)[0] + "/tools")

from body_generator import generate, mode_document, split_levels  # noqa: E402

WORLD = (
    '{"shape": [120, 1, 1], "boundary": {"x": "open", "y": "periodic", "z": "periodic"}, "ticks": 1, "N": 64, "engine":'
    ' "examples/events/engine_start.json", "universe": "examples/events/generated/universe.json", "face_depth": 16,'
    ' "detectors": [], "measured": [{"family": "matter", "phase_denominator": 256, "momentum": [0, 0, 0],'
    ' "momentum_before": [0, 0, 0], "nodes": [{"node": [59, 0, 0], "count": 1000}, {"node": [60, 0, 0], "count": 1000},'
    ' {"node": [61, 0, 0], "count": 1000}]}]}'
)


def mode_entry(momentum: int) -> dict:
    world = json.loads(WORLD)
    world["measured"][0].update({"momentum": [momentum, 0, 0], "momentum_before": [momentum, 0, 0]})
    entry: dict = mode_document((reading := generate(world)), *split_levels(reading))["bodies"][0]
    assert "refused" not in entry, entry.get("refused")
    return entry


def test_the_mode_file_carries_the_moving_bodys_two_levels_and_its_proper_pair() -> None:
    """`now`, `before` and `top_velocity` under `moving` on a body with a momentum, no levels at rest; the clock the proper pair, its period the rest's or longer (the tick lengthened); the reader takes the levels and refuses a defect by name."""
    moving, rest = mode_entry(3 * 64 * 3000 // 20), mode_entry(0)  # v = n / (3 Q M) = 1 / 20
    m, clock = moving["moving"], tuple(moving["clock"])
    assert "now" in m and "now" not in rest["moving"] and m["top_velocity"][0] > 0
    assert period_by_the_rule(*clock) >= period_by_the_rule(*rest["clock"])
    read = moving_levels(m, clock, 120, "b", moving["amplitude_unit"])
    assert read is not None and len(read[0]) == 120 and read[0] != read[1] and any(read[0])
    assert moving_levels(rest["moving"], None, 120, "b", 1) is None
    with pytest.raises(ValueError, match="above the amplitude bound"):
        moving_levels(m, clock, 120, "b", 1)
