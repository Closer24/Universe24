"""The worlds of the massive rows (`massive-rows-v1`; the model owner's yes
of 2026-09-21, record 332 of docs/LOG_2026-09-20.md; the mathematician's
design docs/designs/massive_rows/DESIGN.md, section 4, the pin; the
physics-rule review's three rounds), written by the design's own
prescription from series L's generator beside `slits_huygens`:

- `slits_matter`: `slits_huygens`'s plane and apparatus (the GameBoard of
  60 x 121 x 1 with z periodic, K 2^30, N 64, the stops at x = 7 and the
  wall at x = 8 with the openings at y = 55 and 65 re-releasing on the
  Farey fan by angle with the angle weights, the screen at x = 52 read by
  121 `sum` detectors on the wall's own Nodes), the world key
  `massive_rows`, `width` 1, `action` 1024, the family `matter` (`quantum`
  64, a phase circle, `massive`, no `phase_per_link`) in place of `light`
  in `families`, on the lamp and in the openings' table key (the screen's
  events carry no table), the lamp at (2, 60, 0) with `rate` [1, 1], the
  wheel [2531, 4096], its five directions, `momentum_magnitude` 220, held
  2^30 (the turn 1), 4096 births; 5750 intervals;
- `slits_matter_1024`: the same at the wheel [633, 1024] (the golden rate
  at W = 1024, the nearest odd integer to 0.618 W) and 2700 intervals, the
  run the Boss ordered first (the pin's Pearson and visibility read on
  1024 gathers, the cells' widths a quarter of the pin's);
- `slits_matter_small`: the small massive two-slit world of the register's
  replay (`tests/test_massive_rows.py` (f)): a plane of 12 x 21 x 1 with z
  periodic, a lamp of `matter` (`quantum` 4, `momentum_magnitude` 400: the
  pace 400 / 738 Links per interval) at (1, 10, 0) on the five directions,
  a wall at x = 4 with the openings at y = 8 and 12 (where the lamp's diagonals
  land) re-releasing on a fan
  of five directions with equal weights, a screen at x = 10 of 21 `sum`
  pixels, the wheel [5, 8], 8 births at one per interval, 48 intervals.

`expectations.json` beside them holds the pin of the design's section 4,
written before the run, with the line each number is read on, and the
runs' readings beside it (`read_run.py` writes them, labelled DETECTOR and
GAMEBOARD); the derivations map names the source of every entry. The
`age_bound` of every world is declared: a massive row's pace is its
family's, below the flight's, so the flight bound is not its bound.

Run from the repository root:

    PYTHONPATH=src python examples/events/massive_rows/make_worlds.py
"""

from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402


def load_amplitude_generator():
    """Series L's generator beside `slits_huygens` (the pin's plane and apparatus)."""
    path = HERE.parent / "amplitude" / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("amplitude_make_worlds_massive", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["amplitude_make_worlds_massive"] = module
    spec.loader.exec_module(module)
    return module


AMPLITUDE = load_amplitude_generator()
FAMILY_DEFINITIONS = AMPLITUDE.FAMILY_DEFINITIONS
DEFINITIONS_SOURCE = AMPLITUDE.DEFINITIONS_SOURCE
N = 64
# The family of massive rows: the content M of one row (its quantum), the
# world's width S, the action h and the lamp's momentum magnitude p (the
# design's section 1, the pin): E'_0 = Q S M = 4096, E' = 4113, the pace
# p / E' = 220 / 4113 Links per interval, the turn 55 / 4 steps per axis
# Link, the wavelength h / p = 256 / 55 Links.
FAMILY = "matter"
QUANTUM = 64
WIDTH = 1
ACTION = 1024
MOMENTUM_MAGNITUDE = 220
# The run: every record of 4096 births gathers within about 5753 intervals
# (the design's section 4, the longest row 1468 after the lamp leg 139).
TICKS = 5750
WHEEL = [2531, 4096]
# The largest age a massive row carries in the pin: the longest row's 1468
# intervals after its re-release at 0 (the design's section 4), with room.
AGE_BOUND = 2048
# The 1024-birth run: the golden rate at W = 1024 and the intervals for
# every record of 1024 births (1024 + 139 + 1468 + 50, the design's 2681).
WHEEL_1024 = [633, 1024]
TICKS_1024 = 2700


def rename_family(document: dict[str, object], old: str, new: str) -> None:
    """The family `old` renamed `new` on every lamp and table entry of the world."""
    for entry in document["measured"]:  # type: ignore[union-attr]
        assert isinstance(entry, dict)
        if entry.get("family") == old:
            entry["family"] = new
        table = entry.get("table")
        if isinstance(table, dict) and old in table:
            table[new] = table.pop(old)


def two_slits_matter() -> dict[str, object]:
    """The pin's world: `slits_huygens` with the massive family in place of
    the photon's (the design's section 4)."""
    world = copy.deepcopy(AMPLITUDE.two_slits_huygens())
    document: dict[str, object] = {}
    for key, value in world.items():
        document[key] = value
        if key == "suspension":
            # The keys of the identity, in the world's key order after the
            # law's rates: the width S, the action h, the age bound and the
            # world key.
            document["width"] = WIDTH
            document["action"] = ACTION
            document["age_bound"] = AGE_BOUND
            document["massive_rows"] = True
    document["model_id"] = "beam-massive-slits_matter-v1"
    document["ticks"] = TICKS
    document["families"] = [
        {"name": FAMILY, "quantum": QUANTUM, "massive": True} if family["name"] == "light" else family
        for family in document["families"]  # type: ignore[union-attr]
    ]
    rename_family(document, "light", FAMILY)
    lamp = document["measured"][0]  # type: ignore[index]
    assert lamp["family"] == FAMILY and lamp["amount"] == document["K"]
    lamp["lamp"]["wheel"] = list(WHEEL)
    lamp["lamp"]["momentum_magnitude"] = MOMENTUM_MAGNITUDE
    return document


def two_slits_matter_1024() -> dict[str, object]:
    """The 1024-birth run: the golden rate at W = 1024."""
    document = two_slits_matter()
    document["model_id"] = "beam-massive-slits_matter_1024-v1"
    document["ticks"] = TICKS_1024
    document["measured"][0]["lamp"]["wheel"] = list(WHEEL_1024)  # type: ignore[index]
    return document


# The small world of the register's replay: the plane, the lamp, the wall
# with its openings and their fan, the screen; the pace 400 / 738 (E'_0 =
# 256, E' = isqrt(256^2 + 3 x 400^2) = 738 on a heading).
SMALL_SHAPE = [12, 21, 1]
SMALL_QUANTUM = 4
SMALL_MOMENTUM_MAGNITUDE = 400
SMALL_LAMP = [1, 10, 0]
SMALL_WALL_X = 4
SMALL_OPENINGS = (8, 12)
SMALL_SCREEN_X = 10
SMALL_FAN = [[1, 0, 0], [2, 1, 0], [2, -1, 0], [1, 1, 0], [1, -1, 0]]
SMALL_LAMP_DIRECTIONS = [[1, 0, 0], [1, 1, 0], [1, -1, 0], [2, 1, 0], [2, -1, 0]]
SMALL_WHEEL = [5, 8]
SMALL_TICKS = 48
SMALL_BIRTHS = 8
SMALL_K = 1 << 20


def two_slits_matter_small() -> dict[str, object]:
    """The small massive two-slit world: a few births, tens of intervals."""
    measured: list[dict[str, object]] = [
        {
            "position": list(SMALL_LAMP),
            "family": FAMILY,
            "amount": SMALL_K,
            "phase": 0,
            "fixed": True,
            "lamp": {
                "rate": [1, 1],
                "wheel": list(SMALL_WHEEL),
                "directions": [list(d) for d in SMALL_LAMP_DIRECTIONS],
                "momentum_magnitude": SMALL_MOMENTUM_MAGNITUDE,
            },
        }
    ]
    for y in range(SMALL_SHAPE[1]):
        entry: dict[str, object] = {
            "position": [SMALL_WALL_X, y, 0],
            "family": "wall",
            "amount": 1,
            "fixed": True,
        }
        if y in SMALL_OPENINGS:
            entry["table"] = {FAMILY: {"rule": "rerelease", "weights": [1] * len(SMALL_FAN)}}
            entry["directions"] = [list(d) for d in SMALL_FAN]
        measured.append(entry)
    for y in range(SMALL_SHAPE[1]):
        measured.append(
            {"position": [SMALL_SCREEN_X, y, 0], "family": "wall", "amount": 1, "fixed": True}
        )
    directions = []
    for vector in SMALL_LAMP_DIRECTIONS + SMALL_FAN:
        if sum(abs(c) for c in vector) > 1 and vector not in directions:
            directions.append(list(vector))
    return {
        "law": "beam",
        "model_id": "beam-massive-slits_matter_small-v1",
        "shape": list(SMALL_SHAPE),
        "boundary": {"z": "periodic"},
        "ticks": SMALL_TICKS,
        "K": SMALL_K,
        "N": N,
        "release": [1, 128],
        "suspension": 0,
        "width": WIDTH,
        "action": ACTION,
        "age_bound": 256,
        "massive_rows": True,
        "directions": directions,
        "families": [
            {"name": FAMILY, "quantum": SMALL_QUANTUM, "massive": True},
            {"name": "wall", "quantum": 1},
        ],
        "measured": measured,
        "detectors": [
            {
                "name": f"screen_{y}",
                "positions": [[SMALL_SCREEN_X, y, 0]],
                "threshold": 1,
                "reading": "sum",
            }
            for y in range(SMALL_SHAPE[1])
        ],
    }


def worlds() -> dict[str, dict[str, object]]:
    return {
        "slits_matter": two_slits_matter(),
        "slits_matter_1024": two_slits_matter_1024(),
        "slits_matter_small": two_slits_matter_small(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, world in worlds().items():
        path = args.out / f"{name}.json"
        shipped = families_by_definition(world, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path.write_text(json.dumps(shipped) + "\n", encoding="utf-8")
        print(
            f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {world['ticks']} intervals"
        )


if __name__ == "__main__":
    main()
