"""The mode file of a moving body (ALGEBRA.md #the-generator (e), #the-rows-against-nature (e)): the generator writes the body's two levels under `moving`, the band's top velocity and the proper pair as its clock, 2 cos(Omega) with Omega = omega_0 + Delta (1 - cos k) - k Delta sin k derived here from the file's own numbers; the loader's reader takes the levels or refuses a defect by name; a resting body's file carries no levels; the world one open chain with one body of matter of three Nodes at 1000 by its Nodes with their counts."""

import json
import sys
from math import acos, cos, sin

import pytest

from event_universe.loader.mode import moving_levels

sys.path.insert(0, __file__.rsplit("/tests/", 1)[0] + "/tools")

from body_generator import generate, mode_document, split_levels  # noqa: E402

WORLD = (
    '{"shape": [120, 1, 1], "boundary": {"x": "open", "y": "periodic", "z": "periodic"}, "ticks": 1, "N": 64, "engine":'
    ' "examples/events/engine_start.json", "universe": "examples/events/generated/universe.json", "face_depth": 16, "detectors": [],'
    ' "measured": [{"family": "matter", "phase_denominator": 256, "momentum": [0, 0, 0], "momentum_before": [0, 0, 0], "nodes":'
    ' [{"node": [59, 0, 0], "count": 1000}, {"node": [60, 0, 0], "count": 1000}, {"node": [61, 0, 0], "count": 1000}]}]}'
)


def mode_entry(momentum: int) -> dict:
    world = json.loads(WORLD)
    world["measured"][0].update({"momentum": [momentum, 0, 0], "momentum_before": [momentum, 0, 0]})
    entry: dict = mode_document((reading := generate(world)), *split_levels(reading))["bodies"][0]
    assert "refused" not in entry, entry.get("refused")
    return entry


def test_the_mode_file_carries_the_moving_bodys_two_levels_and_its_proper_pair() -> None:
    """`now`, `before` and `top_velocity` under `moving` on a body with a momentum, no levels at rest; the clock the proper pair on the rest's denominator, above the rest's numerator by 2 cos(Omega) - 2 cos(omega_0) from the file's rotation, triple and top velocity within the pair's rounding; the reader takes the levels and refuses a defect by name."""
    moving, rest = mode_entry(3 * 64 * 3000 // 20), mode_entry(0)  # v = n / (3 Q M) = 1 / 20
    m, clock, rest_clock = moving["moving"], tuple(moving["clock"]), rest["clock"]
    assert clock[1] == rest_clock[1] and clock[0] > rest_clock[0] and "now" not in rest["moving"]
    rot, tr, tv = rest["rotation"], m["triple"], m["top_velocity"]
    omega_0, k, delta = acos(rot[0] / rot[1] / 2), acos(tr[0] / tr[2]), tv[0] / tv[1]
    assert abs(2 * cos(omega_0 + delta * (1 - cos(k)) - k * delta * sin(k)) * clock[1] - clock[0]) <= 1
    read = moving_levels(m, clock, 120, "b", moving["amplitude_unit"])
    assert read is not None and len(read[0]) == 120 and read[0] != read[1]
    with pytest.raises(ValueError, match="above the amplitude bound"):
        moving_levels(m, clock, 120, "b", 1)


def test_a_mode_files_exact_fraction_beyond_the_hosts_digit_cap_round_trips_through_json() -> None:
    """The rotation of a mode on a large board is an exact fraction of thousands of digits (the well's, not the host's to cap): with the world files' reader imported, a fraction of 5,000 digits is written and read back exactly, so the loader and every reader of a mode file take it."""
    rotation = [10**5000 + 7, 10**5000]
    assert json.loads(json.dumps({"rotation": rotation}))["rotation"] == rotation
