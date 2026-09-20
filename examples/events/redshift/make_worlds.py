"""Write the worlds of the redshift series E under the Beam Law, in
space, under the age reading.

Two worlds of one base (README.md here; the entry "E, the clock's redshift
in space under the age reading (2026-09-20)" in docs/EXPERIMENTS.md): an
open cube of SIDE^3 Nodes, a fixed phase-less free source of content M at
the centre releasing one ray per self-creation on every primitive direction
(a, b, c) with 0 < |a| + |b| + |c| <= FAN_MANHATTAN (the full fan of the
first Manhattan shells, so that every direction of the GameBoard within that
bound is covered; `release` [1, M] gives `by_clock(age, M, M)` = 1 per
direction per self-creation, q = len(FAN) units per interval), and clock
probes: fixed measured events of content 1 that `pass` the rays (no push,
no record; the clock's count is read all the same) at every Node of the
shells of radius r in RADII (Euclidean distance within a half Link of r)
at the world's `suspension` [1, d]. In the `scalar` world the probes count
the presence (the default reading); in the `age` world their table entry
for `m` reads `age`, so their clocks count the age moment, sum amount x
age over the rays at the Node (BEAM_LAW section 3 step 5 and section 10
note 24; the model owner, 2026-09-19: "the clock beside a mass must read
M / r"). The probes' own release, one ray per heading at the age M, never
comes within a run of TICKS intervals.

The expectation, written before the runs (README.md): a ballistic fan in
space dilutes as the shell's Nodes, 4 pi r^2, so the shell mean of the
presence is q x dwell / (4 pi r^2) and the mean owed count per
self-creation k_s(r) has k_s x r^2 constant; the age of a ray at r is
about r x sqrt 3 (the flight at 1 / sqrt 3), so the age reading k_a(r) =
(presence x age) / d has k_a x r constant: M / r beside M / r^2 from the
same rays. The rate of a clock is 1 / (1 + k), so the ratio of the age
clocks at r1 and r2 is (1 + k_a(r2)) / (1 + k_a(r1)) = 1 - C (1 / r1 -
1 / r2) + O(C^2), the weak-field redshift. A single probe on a line of
the fan reads the beam on that line, whose presence does not fall with r
(series C): the granularity of the fan, read on the axis and the two
diagonals and reported beside the shell means.

    python examples/events/redshift/make_worlds.py
"""

from __future__ import annotations

import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SIDE = 31
SHAPE = [SIDE, SIDE, SIDE]
CENTRE = (SIDE // 2, SIDE // 2, SIDE // 2)
K = 1 << 22
N = 64
# The source's content M: `release` [1, M] gives one ray per direction per
# self-creation; a probe of content 1 releases nothing before the age M.
SOURCE = 1 << 12
FAN_MANHATTAN = 6
RADII = (4, 6, 8, 10, 12, 14)
# The front reaches r = 14 near tick 25 (14 x sqrt 3); 300 intervals leave
# a window of 200 after the fan is stationary.
TICKS = 300
# The width of the clock's count per world: the scalar probes count the
# presence whole; the age probes count the age moment over 2 (a few units
# at r = 12).
WORLDS = {
    "scalar": {"suspension": [1, 1], "table": {"m": "pass"}},
    "age": {"suspension": [1, 2], "table": {"m": {"rule": "pass", "reads": "age"}}},
}
Json = dict[str, object]


def fan(manhattan: int) -> list[list[int]]:
    """Every primitive direction (a, b, c) with 0 < |a| + |b| + |c| <=
    manhattan, in a fixed order."""
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
HEADINGS = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)}
DECLARED = [v for v in FAN if tuple(v) not in HEADINGS]


def shell(radius: int) -> list[tuple[int, int, int]]:
    """The Nodes at Euclidean distance within a half Link of `radius` from
    the centre, in a fixed order."""
    found = []
    for x in range(SIDE):
        for y in range(SIDE):
            for z in range(SIDE):
                d = math.sqrt((x - CENTRE[0]) ** 2 + (y - CENTRE[1]) ** 2 + (z - CENTRE[2]) ** 2)
                if abs(d - radius) < 0.5:
                    found.append((x, y, z))
    return found


def world(name: str) -> Json:
    keys = WORLDS[name]
    measured: list[Json] = [
        {
            "position": list(CENTRE),
            "family": "m",
            "amount": SOURCE,
            "phase": 0,
            "fixed": True,
            "directions": [list(v) for v in FAN],
        }
    ]
    for radius in RADII:
        for position in shell(radius):
            measured.append(
                {
                    "position": list(position),
                    "family": "m",
                    "amount": 1,
                    "phase": 0,
                    "fixed": True,
                    "table": keys["table"],
                }
            )
    return {
        "law": "beam",
        "model_id": f"rays-redshift-{name}-space-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": [1, SOURCE],
        "suspension": keys["suspension"],
        "families": [{"name": "m", "quantum": 0, "charge": 0, "phase": False}],
        "directions": [list(v) for v in DECLARED],
        "measured": measured,
    }


def main() -> None:
    print(f"fan: {len(FAN)} directions ({len(DECLARED)} declared), q = {len(FAN)} per interval")
    for radius in RADII:
        print(f"shell r = {radius}: {len(shell(radius))} Nodes")
    for name in WORLDS:
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(world(name), separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
