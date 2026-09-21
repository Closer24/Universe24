"""Write the four world files of the Beam Law at the root of `examples/events/`
(README.md here): `one_content` and `two_contents`, one and two measured
events of the free family `m` held in place in an open GameBoard, and
`one_slit` and `two_slits`, a lamp of `light`, a wall of `wall` at x = 8
with one or two openings that re-release on a fan of primitive directions,
and a screen at x = 52 read as 121 one-Node detectors under `wave`.

The fan: every primitive direction `[x, y, 0]` with x from 1 to 11 and
0 < |y| <= 12 - x, x then y ascending (90 directions, the world's
`directions`); an opening re-releases on `[1, 0, 0]` and the fan.

Since 2026-09-20 (the model owner's decision, record 113) a world's
families come from the shipped definitions where they equal them
(`families_by_definition`): the four reference `entities/families.json`
(`two_slits` since the one click of `amplitude-v1` landed).

    python examples/events/make_worlds.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402

DEFINITIONS = "entities/families.json"
MASS = {"name": "m", "quantum": 0, "charge": 0, "phase": False}
CONTENT = 1 << 24
FAN_REACH = 12
WALL_X, SCREEN_X, HEIGHT = 8, 52, 121


def body(position: list[int]) -> dict[str, object]:
    return {"position": position, "family": "m", "amount": CONTENT, "phase": 0, "fixed": True}


def contents(name: str, extent: int, positions: list[list[int]], suspension: int) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": f"rays-{name.replace('_', '-')}-v1",
        "shape": [extent, extent, extent],
        "boundary": "open",
        "ticks": 200,
        "K": 1 << 22,
        "N": 64,
        "release": [1, 128],
        "suspension": suspension,
        "families": [MASS],
        "measured": [body(position) for position in positions],
    }


def fan() -> list[list[int]]:
    return [
        [x, y, 0]
        for x in range(1, FAN_REACH)
        for y in range(-(FAN_REACH - x), FAN_REACH - x + 1)
        if y and math.gcd(x, abs(y)) == 1
    ]


def slits(name: str, openings: list[int]) -> dict[str, object]:
    directions = fan()
    wall: list[dict[str, object]] = []
    for y in range(HEIGHT):
        entry: dict[str, object] = {
            "position": [WALL_X, y, 0],
            "family": "wall",
            "amount": 1,
            "fixed": True,
        }
        if y in openings:
            entry["table"] = {"light": "rerelease"}
            entry["directions"] = [[1, 0, 0], *directions]
        wall.append(entry)
    screen = [
        {"position": [SCREEN_X, y, 0], "family": "wall", "amount": 1, "fixed": True}
        for y in range(HEIGHT)
    ]
    lamp = {
        "position": [2, 60, 0],
        "family": "light",
        "amount": (1 << 33) + 1_400_000,
        "phase": 0,
        "fixed": True,
        "lamp": {
            "rate": [64, 1],
            "wheel": [1, 64],
            "directions": [[1, 0, 0], [1, 1, 0], [1, -1, 0], [2, 1, 0], [2, -1, 0]],
        },
    }
    return {
        "law": "beam",
        "model_id": f"rays-{name.replace('_', '-')}-v1",
        "shape": [60, HEIGHT, 1],
        "boundary": {"z": "periodic"},
        "ticks": 500,
        "K": 1 << 30,
        "N": 64,
        "release": [1, 128],
        "suspension": 0,
        "directions": directions,
        "families": [{"name": "light", "quantum": 1}, {"name": "wall", "quantum": 1}],
        "measured": [lamp, *wall, *screen],
        "detectors": [
            {"name": f"screen_{y}", "positions": [[SCREEN_X, y, 0]], "threshold": 1, "reading": "wave"}
            for y in range(HEIGHT)
        ],
    }


def worlds() -> dict[str, dict[str, object]]:
    """The four documents by name, as written."""
    inline = {
        "one_content": contents("one_content", 25, [[12, 12, 12]], 1),
        "two_contents": contents("two_contents", 21, [[6, 10, 10], [14, 10, 10]], 0),
        "one_slit": slits("one_slit", [55]),
        "two_slits": slits("two_slits", [55, 65]),
    }
    source = (HERE / DEFINITIONS).read_bytes()
    return {
        name: families_by_definition(document, DEFINITIONS, source) for name, document in inline.items()
    }


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        print(path.relative_to(HERE.parents[1]))


if __name__ == "__main__":
    main()
