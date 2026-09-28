"""The mode file of a moving body (ALGEBRA.md #the-generator (e), #the-velocity): the generator writes the body's two levels under `moving` and its proper pair as its clock, and the loader's reader takes them or refuses a defect by name; a resting body's file carries no levels."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from event_universe.loader.mode import moving_levels, period_by_the_rule

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from body_generator import generate, mode_document, split_levels  # noqa: E402

CHAIN, NODES, COUNT = 120, 3, 1000


def mode_entry(momentum: int) -> dict:
    """One open chain, one body of matter by its Nodes with their counts and its momentum along x; the mode file's entry for it."""
    corner = CHAIN // 2 - NODES // 2
    nodes = [{"node": [corner + i, 0, 0], "count": COUNT} for i in range(NODES)]
    body = {
        "family": "matter",
        "nodes": nodes,
        "momentum": [momentum, 0, 0],
        "momentum_before": [momentum, 0, 0],
    }
    world = {
        "shape": [CHAIN, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": 1,
    }
    world.update(
        {"N": 64, "engine": "examples/events/engine_start.json", "face_depth": 16, "detectors": []}
    )
    world.update(
        {
            "universe": "examples/events/generated/universe.json",
            "measured": [{**body, "phase_denominator": 256}],
        }
    )
    sys.set_int_max_str_digits(0)
    reading = generate(world)
    entry: dict = mode_document(reading, *split_levels(reading))["bodies"][0]
    assert "refused" not in entry, entry.get("refused")
    return entry


def test_the_mode_file_carries_the_moving_bodys_two_levels_and_its_proper_pair() -> None:
    """`now` and `before` under `moving` on a body with a momentum, none at rest; the clock the proper pair, its period the rest's or longer (the tick lengthened, ALGEBRA.md (e)); the reader takes the levels and refuses a defect by name."""
    unit = json.loads((ROOT / "examples/events/generated/universe.json").read_text(encoding="utf-8"))[
        "integers"
    ]["momentum_unit"]
    moving, rest = mode_entry(3 * unit * NODES * COUNT // 20), mode_entry(0)
    assert "now" in moving["moving"] and "now" not in rest["moving"]
    assert period_by_the_rule(*moving["clock"]) >= period_by_the_rule(*rest["clock"])
    clock = (moving["clock"][0], moving["clock"][1])
    read = moving_levels(moving["moving"], clock, CHAIN, "b", moving["amplitude_unit"])
    assert read is not None and len(read[0]) == CHAIN and read[0] != read[1] and any(read[0])
    assert moving_levels(rest["moving"], None, CHAIN, "b", 1) is None
    with pytest.raises(ValueError, match="moving.now must be"):
        moving_levels({"now": [1], "before": [1]}, clock, CHAIN, "b", 1)
    with pytest.raises(ValueError, match="above the amplitude bound"):
        moving_levels(moving["moving"], clock, CHAIN, "b", 1)
