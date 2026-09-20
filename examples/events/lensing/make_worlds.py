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

Since 2026-09-20 (the model owner's decision, "DECIDED: the meeting, M-R",
docs/BEAM_LAW.md note 34) the same four worlds are written again under the
world key `meeting: true` (`<name>_meeting.json`, the model ids
`beam-lensing-<name>-meeting-v1`): every paid unit of the beam reads the
mass's free crowd at every free-space Node it shares with it and turns
toward it by its phase register, the crowd untouched. And a fifth world,
`lens_meeting.json` (`beam-lensing-lens-meeting-v1`): two lamps at +-b about
the mass's line on a box longer in x (LENS_SHAPE), the screen at LENS_SCREEN_X,
so that the two beams, each turned toward the mass, converge past it and the
crossing is read as a grain of the fan (the expectation from the offline
flight: about 70 Links past the mass at b = 6, the steps 2.4 degrees each).

    python examples/events/lensing/make_worlds.py
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
# The lens world under the meeting: two lamps at +-b, a box longer in x so
# that the crossing of the two turned beams lies before the screen.
LENS_SHAPE = (105, 41, 41)
LENS_SCREEN_X = 102
LENS_TICKS = 600
LENS_IMPACT = 6
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


def world(
    name: str,
    *,
    meeting: bool = False,
    impacts: tuple[int, ...] | None = None,
    shape: tuple[int, int, int] = SHAPE,
    screen_x: int = SCREEN_X,
    ticks: int = TICKS,
) -> Json:
    keys = WORLDS.get(name, {"mass": SOURCE, "impact": LENS_IMPACT})
    impact = keys["impact"]
    mass = keys["mass"]
    assert impact is not None
    centre = (CENTRE[0], shape[1] // 2, shape[2] // 2)
    measured: list[Json] = [
        {
            "position": [LAMP_X, centre[1] + b, centre[2]],
            "family": "light",
            "amount": LAMP_CONTENT,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [1, 1], "directions": BEAM},
            "table": {"m": "pass"},
        }
        for b in (impacts if impacts is not None else (impact,))
    ]
    if mass is not None:
        measured.append(
            {
                "position": list(centre),
                "family": "m",
                "amount": mass,
                "phase": 0,
                "fixed": True,
                "directions": [list(v) for v in FAN],
            }
        )
    detectors: list[Json] = []
    for y in range(shape[1]):
        for z in range(shape[2]):
            measured.append(
                {
                    "position": [screen_x, y, z],
                    "family": "wall",
                    "amount": 1,
                    "fixed": True,
                    "table": {"light": {"rule": "measure", "reads": "age"}, "m": "pass"},
                }
            )
            detectors.append(
                {
                    "name": f"screen_{y}_{z}",
                    "positions": [[screen_x, y, z]],
                    "threshold": 1,
                    "reading": "wave",
                }
            )
    document: Json = {
        "law": "beam",
        "model_id": f"beam-lensing-{name}-meeting-v1" if meeting else f"rays-lensing-{name}-space-v1",
        "shape": list(shape),
        "boundary": "open",
        "ticks": ticks,
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
    if meeting:
        document["meeting"] = True
    return document


def lens_world() -> Json:
    """Two beams at +-b past the mass under the meeting, on the longer box."""
    return world(
        "lens",
        meeting=True,
        impacts=(LENS_IMPACT, -LENS_IMPACT),
        shape=LENS_SHAPE,
        screen_x=LENS_SCREEN_X,
        ticks=LENS_TICKS,
    )


def main() -> None:
    print(f"fan: {len(FAN)} directions; beam: {len(BEAM)}; declared: {len(DECLARED)}")
    for name in WORLDS:
        for meeting in (False, True):
            path = HERE / (f"{name}_meeting.json" if meeting else f"{name}.json")
            document = families_by_definition(
                world(name, meeting=meeting), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE
            )
            path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
            print(path.relative_to(HERE.parents[2]))
    path = HERE / "lens_meeting.json"
    document = families_by_definition(lens_world(), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
    path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
    print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
