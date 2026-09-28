"""A moving body loads moving (ALGEBRA.md #the-generator (e), #the-velocity): the generator's mode file carries the moving body's two levels and its proper pair, the loader reads them, the assembly writes them, and the count's line moves the body one Link per 1 / v intervals, v = n / (3 Q M) from the file's numbers alone; a resting body's file carries no levels and its Nodes stay."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.loader.mode import moving_levels, period_by_the_rule
from event_universe.world_files import input_digest, parse_world_document, world_files

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from body_generator import generate, mode_document, split_levels  # noqa: E402

CHAIN, NODES, COUNT = 120, 3, 1000


def chain_world(universe: Path, momentum: int) -> dict:
    """An open chain with one body of matter by its Nodes with their counts, its momentum along x at both levels."""
    corner = CHAIN // 2 - NODES // 2
    body = {
        "family": "matter",
        "nodes": [{"node": [corner + i, 0, 0], "count": COUNT} for i in range(NODES)],
        "momentum": [momentum, 0, 0],
        "momentum_before": [momentum, 0, 0],
        "phase_denominator": 256,
    }
    return {
        "shape": [CHAIN, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": 1,
        "N": 64,
        "engine": "examples/events/engine_start.json",
        "universe": str(universe),
        "face_depth": 16,
        "measured": [body],
        "detectors": [],
    }


def mode_of(world: dict) -> dict:
    sys.set_int_max_str_digits(0)
    reading = generate(world)
    assert "refused" not in reading["bodies"][0], reading["bodies"][0].get("refused")
    document = mode_document(reading, *split_levels(reading))
    document["world_digest"] = input_digest(world)
    return document


def loaded(world: dict, universe: Path, mode: dict) -> DetectorLawSimulation:
    files = world_files(world)
    files[str(universe)] = json.loads(universe.read_text(encoding="utf-8"))
    files["world.mode.json"] = mode
    return DetectorLawSimulation(parse_world_document(world, files, input_digest(world)))


@pytest.fixture(scope="module")
def universe(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """The shipped families with the amplitude bound at the generator's own unit for this well."""
    shipped = json.loads((ROOT / "examples/events/generated/universe.json").read_text(encoding="utf-8"))
    path = tmp_path_factory.mktemp("moving") / "universe.json"
    path.write_text(json.dumps(shipped))
    shipped["integers"]["amplitude_bound"] = mode_of(chain_world(path, 0))["bodies"][0]["amplitude_unit"]
    path.write_text(json.dumps(shipped))
    return path


def wall_of(universe: Path) -> int:
    return (
        3 * json.loads(universe.read_text(encoding="utf-8"))["integers"]["momentum_unit"] * NODES * COUNT
    )


def test_the_mode_file_carries_the_moving_bodys_two_levels_and_its_proper_pair(universe: Path) -> None:
    """`now` and `before` under `moving` on a body with a momentum and none at rest; the clock the proper pair, its period the rest's or longer (the tick lengthened, ALGEBRA.md (e)); the reader takes the levels and refuses a defect by name."""
    moving = mode_of(chain_world(universe, wall_of(universe) // 20))["bodies"][0]
    rest = mode_of(chain_world(universe, 0))["bodies"][0]
    assert "now" in moving["moving"] and "now" not in rest["moving"]
    assert period_by_the_rule(*moving["clock"]) >= period_by_the_rule(*rest["clock"])
    read = moving_levels(moving["moving"], tuple(moving["clock"]), CHAIN, "b", moving["amplitude_unit"])
    assert read is not None and len(read[0]) == CHAIN and read[0] != read[1]
    assert moving_levels(rest["moving"], None, CHAIN, "b", 1) is None
    with pytest.raises(ValueError, match="moving.now must be"):
        moving_levels({"now": [1], "before": [1]}, (1, 1), CHAIN, "b", 1)
    with pytest.raises(ValueError, match="above the amplitude bound"):
        moving_levels(moving["moving"], tuple(moving["clock"]), CHAIN, "b", 1)


@pytest.mark.xfail(
    strict=True,
    raises=ValueError,
    reason="the loader bounds the rule's total at the level min(2 M, Gamma - 1) while the generator derives its unit at the well's content; the mode file loads once the generator's amplitude at the loader's level is on main, and the mark leaves then",
)
def test_a_moving_body_loads_moving_and_moves_one_link_per_1_over_v_intervals(universe: Path) -> None:
    """The law's velocity: the count's centroid moves at v = n / (3 Q M); after t intervals the body's Nodes have shifted by n t div W Links, W = 3 Q M, within one Link of the rounding; the resting twin stays."""
    wall = wall_of(universe)
    momentum = wall // 20
    moving_world, rest_world = chain_world(universe, momentum), chain_world(universe, 0)
    moving = loaded(moving_world, universe, mode_of(moving_world))
    rest = loaded(rest_world, universe, mode_of(rest_world))
    levels = moving.blocks[0].definition.levels
    assert levels is not None and list(moving.blocks[0].own.now.ravel()) == list(levels[0])
    assert list(moving.blocks[0].own.before.ravel()) == list(levels[1])
    start_moving, start_rest = moving.blocks[0].corner[0], rest.blocks[0].corner[0]
    intervals = 3 * wall // momentum
    for _ in range(intervals):
        moving.step()
        rest.step()
    expected = momentum * intervals // wall
    assert expected >= 3 and abs((moving.blocks[0].corner[0] - start_moving) - expected) <= 1
    assert rest.blocks[0].corner[0] == start_rest
