"""Write the eight worlds of the Heisenberg run A10 under the Beam Law:
the width of an opening and the spread behind it.

One base world (README.md here; the entry "A10, the width of an opening and
the spread behind it, under the Beam Law" in docs/EXPERIMENTS.md), the
width w of the opening and the detectors' `reading` the only differences
between the files: the plane of the two-slit world stretched to 120 x 161
x 1 (z periodic), K 2^30, N 64, no suspension. A row of w + 4 lamps of the
paid family `light` at x = 2 (content 8 K + 1 400 000, turn 8 per
self-creation, so a release at tick t carries the phase 8 t mod 64 and the
wavelength is lambda = c x period = 8 / sqrt 3 Links), each releasing F
units per self-creation on (1, 0, 0) alone (a plane wave of width w + 4).
A wall of the paid family `wall` at x = 8 measuring light (the rule the
keys give), with ONE opening of w Nodes centred on y = 80 whose Nodes
re-emit (`rerelease`) on the fan of the F = 47 primitive in-plane
directions (a, b, 0) with a >= 1, |b| <= a and a + |b| <= 12 (the forward
half of the two-slit fan): a release of F units per lamp gives every
opening Node one unit per fan direction per interval. The opening is
declared as ONE detector `opening` of w Nodes (the model owner,
2026-09-19: the declared width is the position's uncertainty). A screen
at x = 116 (L = 108 Links behind the wall) of measured events of `wall`
read as 161 one-Node detectors `screen_<y>` (the screen's pixels). Every
detector declares the world's `reading`, `wave` or `beam`. 350 intervals:
the flight to the screen takes about 190 (108 Links at 1 / sqrt 3 plus the
6 Links from the lamps), the record accumulates over the remaining 150.

    python examples/events/heisenberg/make_worlds.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()
# Written inline until stage (vii) of `amplitude-v1` lands (it re-pins this
# world): the scope of the migration of 2026-09-20.
INLINE = ((3, "beam"),)

K = 1 << 30
N = 64
TURN = 8
SHAPE = (120, 161, 1)
LAMP_X, WALL_X, SCREEN_X = 2, 8, 116
CENTRE = 80
TICKS = 350
P = 12
WIDTHS = (1, 3, 9, 27)
READINGS = ("wave", "beam")
# The forward fan: primitive (a, b, 0) with a >= 1, |b| <= a, a + |b| <= P.
FAN = [
    [a, b, 0]
    for a in range(1, P + 1)
    for b in range(-P, P + 1)
    if abs(b) <= a and a + abs(b) <= P and math.gcd(a, abs(b)) == 1 and (a, b) != (1, 0)
]
DIRECTIONS = [[1, 0, 0], *FAN]
F = len(DIRECTIONS)
MARGIN = 2


def opening_range(width: int) -> range:
    return range(CENTRE - (width - 1) // 2, CENTRE + (width - 1) // 2 + 1)


def world(width: int, reading: str) -> dict[str, object]:
    opening = opening_range(width)
    lit = range(opening.start - MARGIN, opening.stop + MARGIN)
    measured: list[dict[str, object]] = [
        {
            "position": [LAMP_X, y, 0],
            "family": "light",
            "amount": TURN * K + 1400000,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [F, 1], "directions": [[1, 0, 0]]},
        }
        for y in lit
    ]
    for y in range(SHAPE[1]):
        entry: dict[str, object] = {
            "position": [WALL_X, y, 0],
            "family": "wall",
            "amount": 1,
            "fixed": True,
        }
        if y in opening:
            entry["table"] = {"light": "rerelease"}
            entry["directions"] = DIRECTIONS
        measured.append(entry)
    detectors: list[dict[str, object]] = [
        {
            "name": "opening",
            "positions": [[WALL_X, y, 0] for y in opening],
            "threshold": 1,
            "reading": reading,
        }
    ]
    for y in range(SHAPE[1]):
        measured.append({"position": [SCREEN_X, y, 0], "family": "wall", "amount": 1, "fixed": True})
        detectors.append(
            {
                "name": f"screen_{y}",
                "positions": [[SCREEN_X, y, 0]],
                "threshold": 1,
                "reading": reading,
            }
        )
    return {
        "law": "beam",
        "model_id": f"rays-heisenberg-w{width}-{reading}-v1",
        "shape": list(SHAPE),
        "boundary": {"z": "periodic"},
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": [1, 128],
        "suspension": 0,
        "directions": FAN,
        "families": [{"name": "light", "quantum": 1}, {"name": "wall", "quantum": 1}],
        "measured": measured,
        "detectors": detectors,
    }


def main() -> None:
    for reading in READINGS:
        for width in WIDTHS:
            path = HERE / f"w{width}_{reading}.json"
            document = world(width, reading)
            if (width, reading) not in INLINE:
                document = families_by_definition(document, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
            path.write_text(json.dumps(document) + "\n", encoding="utf-8")
            print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
