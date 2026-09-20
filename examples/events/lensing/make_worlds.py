"""Write the four worlds of series K, "light beside a mass", under the law
of the ray, in space: a narrow beam of a paid light family sent past a
fixed mass at an impact distance b toward a screen of pixel detectors.

One base (README.md here; the entry "K, light beside a mass" in
docs/EXPERIMENTS.md): an open box of SHAPE Nodes, the mass at CENTRE. The
lamp is a fixed measured event of the paid family `light` at x = LAMP_X,
y = centre + b (content TURN x K + 1 400 000: the turn TURN per
self-creation, so a release at tick t carries the phase TURN x t mod N and
the wavelength is lambda = c x period), releasing one unit per
self-creation on each of the BEAM directions, the heading (1, 0, 0) and
four in-plane directions within 5 degrees of it: a beam nine pixels wide
at the screen. The mass is a fixed measured event of the free, phase-less
family `m` of content M at the centre, releasing on the full fan of
primitive directions (a, b, c) with 0 < |a| + |b| + |c| <= FAN_MANHATTAN
(290 directions, series E's form): at `release` [1, SOURCE] it releases
`by_clock(age, M, SOURCE)` rays per direction per self-creation, one for
M = SOURCE and two for M = 2 SOURCE. The screen is the plane x = SCREEN_X
of measured events of the paid family `wall`, each declared as a one-Node
detector `screen_<y>_<z>` reading `wave`, its entry for `light` `{"rule":
"measure", "reads": "age"}` so that every click record carries the age
moment of the arrivals (the flight time, Shapiro's reading) and its entry
for `m` `pass` (the mass's rays cross the screen unread; nothing is
pushed, nothing is owed: `suspension` 0 in every world, so no clock is
slowed and the reading is of the flight alone; the emitter's clock beside
a mass is series E's reading). The lamp's entry for `m` is `pass` as well.

| World | The mass | b | What it asks |
| --- | --- | --- | --- |
| `control` | none | 6 | the beam alone: the centroid, the ages, the count, the phase rate |
| `mass` | M = SOURCE, one ray per direction per interval | 6 | the same beside the mass |
| `heavy` | M = 2 SOURCE, two rays per direction per interval | 6 | twice the crowd |
| `near` | M = SOURCE | 3 | half the impact distance |

The expectation, written before the runs (README.md): a ray in transit is
moved by the flight table alone and turned only by the collision, which
acts per family's store and per (number, content) class on the six
headings at a Node of free space; the beam's rays and the mass's rays are
of different families and numbers and never enter one slot state, so the
law derives a deflection of exactly 0, a delay of exactly 0, the count of
the control and the lamp's own phase rate, whatever M and b. Nature bends
light toward the mass by 4 G M / (b c^2) and delays it (Shapiro).

    python examples/events/lensing/make_worlds.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHAPE = (57, 41, 41)
CENTRE = (28, 20, 20)
LAMP_X = 2
SCREEN_X = 54
K = 1 << 30
N = 64
TURN = 8
LAMP_CONTENT = TURN * K + 1400000
# The mass's content M and the release [1, SOURCE]: one ray per direction
# per self-creation at M = SOURCE (series E), two at 2 SOURCE.
SOURCE = 1 << 12
FAN_MANHATTAN = 6
TICKS = 400
# The beam: the heading toward the screen and four in-plane directions
# within 5 degrees of it (1 / 12 and 1 / 24 in y per Link in x), so that
# the arrival on the screen, 52 Links from the lamp, spans nine pixels.
BEAM = [[1, 0, 0], [24, 1, 0], [24, -1, 0], [12, 1, 0], [12, -1, 0]]
WORLDS: dict[str, dict[str, int | None]] = {
    "control": {"mass": None, "impact": 6},
    "mass": {"mass": SOURCE, "impact": 6},
    "heavy": {"mass": 2 * SOURCE, "impact": 6},
    "near": {"mass": SOURCE, "impact": 3},
}
HEADINGS = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)}
Json = dict[str, object]


def fan(manhattan: int) -> list[list[int]]:
    """Every primitive direction (a, b, c) with 0 < |a| + |b| + |c| <=
    manhattan, in a fixed order (series E's fan)."""
    found = []
    for a in range(-manhattan, manhattan + 1):
        for b in range(-manhattan, manhattan + 1):
            for c in range(-manhattan, manhattan + 1):
                if (a or b or c) and abs(a) + abs(b) + abs(c) <= manhattan:
                    if math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                        found.append([a, b, c])
    found.sort()
    return found


FAN = fan(FAN_MANHATTAN)
DECLARED = [v for v in FAN if tuple(v) not in HEADINGS] + [v for v in BEAM if tuple(v) not in HEADINGS]


def world(name: str) -> Json:
    keys = WORLDS[name]
    impact = keys["impact"]
    mass = keys["mass"]
    assert impact is not None
    measured: list[Json] = [
        {
            "position": [LAMP_X, CENTRE[1] + impact, CENTRE[2]],
            "family": "light",
            "amount": LAMP_CONTENT,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [1, 1], "directions": BEAM},
            "table": {"m": "pass"},
        }
    ]
    if mass is not None:
        measured.append(
            {
                "position": list(CENTRE),
                "family": "m",
                "amount": mass,
                "phase": 0,
                "fixed": True,
                "directions": [list(v) for v in FAN],
            }
        )
    detectors: list[Json] = []
    for y in range(SHAPE[1]):
        for z in range(SHAPE[2]):
            measured.append(
                {
                    "position": [SCREEN_X, y, z],
                    "family": "wall",
                    "amount": 1,
                    "fixed": True,
                    "table": {"light": {"rule": "measure", "reads": "age"}, "m": "pass"},
                }
            )
            detectors.append(
                {
                    "name": f"screen_{y}_{z}",
                    "positions": [[SCREEN_X, y, z]],
                    "threshold": 1,
                    "reading": "wave",
                }
            )
    return {
        "law": "beam",
        "model_id": f"rays-lensing-{name}-space-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": [1, SOURCE],
        "suspension": 0,
        "directions": [list(v) for v in DECLARED],
        "families": [
            {"name": "light", "quantum": 1},
            {"name": "wall", "quantum": 1},
            {"name": "m", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
        "detectors": detectors,
    }


def main() -> None:
    print(f"fan: {len(FAN)} directions; beam: {len(BEAM)}; declared: {len(DECLARED)}")
    for name in WORLDS:
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(world(name), separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
