"""The mode file of a moving body (ALGEBRA.md #the-generator (e), #the-rows-against-nature (e)): the generator writes the body's two levels under `moving`, the band's top velocity and the proper pair as its clock, 2 cos(Omega) with Omega = omega_0 + Delta (1 - cos k) - k Delta sin k derived here from the file's own numbers; the loader's reader takes the levels or refuses a defect by name; a resting body's file carries its two levels as well, the second the read act once more halved, not the first; the world one open chain with one body of matter of three Nodes at 1000 by its Nodes with their counts."""

import json
import sys
from math import acos, cos, sin

import pytest

from event_universe.loader.mode import moving_levels

sys.path.insert(0, __file__.rsplit("/tests/", 1)[0] + "/tools")

from body_generator import generate, mode_document, split_levels  # noqa: E402

from event_universe.core.integer import MAX_WORK_INT  # noqa: E402

WORLD = (
    '{"shape": [120, 1, 1], "boundary": {"x": "open", "y": "periodic", "z": "periodic"}, "ticks": 1, "N": 64, "engine":'
    ' "examples/events/engine_start.json", "universe": "examples/events/experiments/universe.json", "face_depth": 16, "detectors": [],'
    ' "measured": [{"family": "matter", "phase_denominator": 256, "momentum": [0, 0, 0], "momentum_before": [0, 0, 0], "nodes":'
    ' [{"node": [59, 0, 0], "count": 1000}, {"node": [60, 0, 0], "count": 1000}, {"node": [61, 0, 0], "count": 1000}]}]}'
)


def mode_entry(momentum: int) -> dict:
    world = json.loads(WORLD)
    world["measured"][0].update({"momentum": [momentum, 0, 0], "momentum_before": [momentum, 0, 0]})
    world["measured"][0]["emitter"] = {
        "family": "matter",
        "weight": 1,
    }  # a giver: a body neither giving nor moving has no entry
    entry: dict = mode_document((reading := generate(world)), *split_levels(reading))["bodies"][0]
    assert "refused" not in entry, entry.get("refused")
    return entry


def test_the_mode_file_carries_the_moving_bodys_two_levels_and_its_proper_pair() -> None:
    """`now`, `before` and `top_velocity` under `moving` on a body with a momentum, at rest the two levels of the standing mode, the second not the first; the clock the proper pair on the rest's denominator, above the rest's numerator by 2 cos(Omega) - 2 cos(omega_0) from the file's rotation, triple and top velocity within the pair's rounding; the reader takes the levels and refuses a defect by name."""
    moving, rest = mode_entry(3 * 64 * 3000 // 20), mode_entry(0)  # v = n / (3 Q M) = 1 / 20
    m, clock, rest_clock = moving["moving"], tuple(moving["clock"]), rest["clock"]
    assert clock[1] == rest_clock[1]
    assert clock[0] > rest_clock[0]
    assert rest["moving"]["before"] != rest["moving"]["now"]
    rot, tr, tv = rest["rotation"], m["triple"], m["top_velocity"]
    omega_0, k, delta = acos(rot[0] / rot[1] / 2), acos(tr[0] / tr[2]), tv[0] / tv[1]
    assert abs(2 * cos(omega_0 + delta * (1 - cos(k)) - k * delta * sin(k)) * clock[1] - clock[0]) <= 1
    read = moving_levels(m, clock, 120, "b", moving["amplitude_unit"])
    assert read is not None and len(read[0]) == 120 and read[0] != read[1]
    with pytest.raises(ValueError, match="above the amplitude bound"):
        moving_levels(m, clock, 120, "b", 1)


def test_every_integer_of_the_mode_file_stays_within_the_width() -> None:
    """The mode file's readings (the rotation, the rotation in the world's well, the velocity, the top velocity, the share inside) are pairs on the mode's own denominator A, so no integer of the file leaves the engine's width whatever the board; at rest the rotation is the clock's own pair."""
    entry = mode_entry(3 * 64 * 3000 // 20)
    integers = [v for v in json.loads(json.dumps(entry)).values() if isinstance(v, int)]
    integers += [v for pair in ("rotation", "share_inside") for v in entry[pair]]
    integers += [v for pair in ("velocity", "top_velocity") for v in entry["moving"][pair]]
    integers += entry["in_the_worlds_well"].get("rotation", [])
    assert all(abs(v) <= MAX_WORK_INT for v in integers)
    rest = mode_entry(0)  # at rest the clock is the rotation's own pair; moving, the proper pair
    assert rest["rotation"] == rest["clock"]
