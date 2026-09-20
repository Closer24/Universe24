"""Write the four worlds of series G, the Hubble diagram behind the detector,
under the law of the ray, in space.

The model owner's question (2026-09-20, Highlights 5.4, "DECIDED: series G"):
"let it check whether what is observed today is also seen in our detector."
Four worlds of one base (README.md here; the entry "G, the Hubble diagram
behind the detector (2026-09-20)" in docs/EXPERIMENTS.md): the throw.

The throw. An open cube of SIDE^3 Nodes with the centre c. Twenty-four
sources, each a free family of its own (so that the detector's record tells
the source by the family of the ray), thrown from the centre along the six
axes: on every axis a chain of CHAIN sources of ranks i = 1 .. CHAIN at the
initial distances r_0 = 1 + SPACING x i, the faster the farther (no source
ever overtakes another: a step onto an occupied Node would be refused). A
source is a free measured event of content M with the momentum p along its
axis; it steps one Link per (Q S M + p) / p self-creations (RAY_LAW section
3 step 5, Q = 64, S the world's `width`), so its speed is v = p / (Q S M +
p) Links per interval, and p is chosen for the speed ladder v = c x V(axis)
x (2 i - 1) / (2 CHAIN - 1) with V from 0.35 to 0.6: the twenty-four speeds
span 0.05 c to 0.6 c, c the ray's speed on a heading read off the flight
table (`flight_table`: m(L) Links per period L, 32 / 55 = 0.5818 per
interval). Every source releases at every self-creation one row of F rays
on the heading toward the centre alone (`release` [1, 64]: `by_clock(age,
M, 64)` = M / 64 rays per direction per self-creation), the row carrying
the emitter's phase at birth (a free family's release stamps the clock's
phase; `phase_per_link` 0, so the phase is not turned in flight). No row
is released away from the centre: a source that steps into the Node of a
row it has just released takes it home and re-emits it on its directions
with its stale phase (the law's `home`; found in the first throw of this
series, README.md), so the field of a source on the sources behind it is
not part of the throw. The emitter's clock turns ONE step of the circle of
N = 64 per self-creation (content M = K, `by_clock(age, M, K)` = 1): the
rate the redshift reads.

The detector. ONE measured event of the paid family `detector` (it releases
nothing) at the centre, declared as the detector `centre` of one Node
reading `wave` (a set of one Node with one record; the sources aim exactly
at it along the axes), whose table entry for every source family is
`{"rule": "measure", "reads": "age"}`: the click record of every arriving
row carries the age moment of the row (amount x age, the ray's flight
time), the `record` line of the interval carries the pointer and its phase
(the emitter's phase at birth), the family names the source.

The mass inside. Six fixed free measured events of the phase-less family
`mass` at one Link from the centre on the six axes, inside every chain,
each releasing on the outward heading of its axis alone: the crowd's mass
inside every source, whose row pulls every source of the chain inward
(kappa = -M_A: a free ray pushes its reader toward its emitter). On a line a
beam does not dilute (series C: the count on an axis is constant with r),
so the pull is the same at every rank; the inward rows of the CHAIN - i
sources ahead of rank i pull it outward by (CHAIN - i) F per interval, so
the net pull on rank i is (M_in - (CHAIN - i) F) per interval, M_in the
mass's rows per interval: with M_in = CHAIN x F it is i x F inward, the
one-dimensional analogue of the mass inside the sphere, growing with the
rank as the mass inside grows with the distance. The masses' table entry
for every source family is `pass` (their clocks count the rows all the
same).

Two crowds. (i) The coasting throw: the sources of content M = 64 (F = 1:
one ray per self-creation), the masses of content 1 (one ray per 64
self-creations, a residual). The push a passing row gives a reader is one
own-label unit per unit of amount (Delta n = amount in units of Q M_A,
RAY_LAW section 3 step 4, the equivalence principle, so the speed changes
by (1 - v)^2 x amount / S per row whatever the reader's content), and with
S = 2^20 the light crowd's rows move a source's speed by at most 3 x 400 x
(1 - v)^2 / 2^20 < 0.0011 over the run (outward, on rank 1): the throw
coasts. (ii) The pushing throw: the same speeds (p x F) with the sources'
contents raised to M = 64 F = 1024 (F = 16 rays per row) and the masses'
to 64 x CHAIN x F = 4096 (64 rays per self-creation): every source
decelerates, the outer ones the most.

Two clocks (series E's pair). The world's `suspension` [1, d] makes every
measured event's clock owe `by_clock(age, counted, d)` intervals after
each self-creation, `counted` the presence of the rays of other numbers at
its Node in the `scalar` worlds (d = 2^12) and their age moment `sum
amount x age` in the `age` worlds (every source's and every mass's table
entry for every other family reads `age`, d = 2^19): the emitter's clock
beside the crowd's rays, weak (k of about 0.001 in the coasting worlds,
0.01 to 0.05 in the pushing worlds, the age moment growing with the rank
and with the age of the crowd). The detector's entries read `age` in every
world (the distance reading needs the age on the arrival record); its own
clock paces nothing (it releases nothing).

    python examples/events/hubble/make_worlds.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.core.lattice import PORT_HEADINGS  # noqa: E402
from event_universe.events.nature_beam import flight_table  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, Q  # noqa: E402

SIDE = 301
SHAPE = [SIDE, SIDE, SIDE]
CENTRE = (SIDE // 2, SIDE // 2, SIDE // 2)
N = 64
TICKS = 400
# The width of the push: one row of amount a moves a source's speed by
# (1 - v)^2 a / S; 2^20 keeps the coasting crowd's push below 0.002 in v
# over the run and lets the pushing crowd's i x 16 per interval be felt (a
# twentieth to a fifth of the speed over the run).
WIDTH = 1 << 20
# The release: M / 64 rays per direction per self-creation.
RELEASE = [1, 64]
# The content of a coasting source: one ray per self-creation, and the
# turn of one phase step per self-creation (K = M).
LIGHT = 64
# The pushing crowd's factor: rows of F rays, the contents F times.
FACTOR = 16
CHAIN = 4
SPACING = 2
# The masses inside: one Link from the centre on every axis.
MASS_RADIUS = 1
# The speed ladder per axis, the fraction of c of the outermost source of
# each chain (the ranks at (2 i - 1) / (2 CHAIN - 1) of it): 0.05 c to 0.6 c.
LADDER = (0.6, 0.55, 0.5, 0.45, 0.4, 0.35)
# The axes in Port order: +x, -x, +y, -y, +z, -z.
AXES = ("px", "mx", "py", "my", "pz", "mz")
# The clocks' widths: the presence over 2^12, the age moment over 2^19.
CLOCKS = {"scalar": [1, 1 << 12], "age": [1, 1 << 19]}
CROWDS = {"coasting": 1, "pushing": FACTOR}
Json = dict[str, object]


def beam_speed() -> float:
    """The ray's speed on a heading, read off the flight table: the Links
    made in one period of the heading's digital line over the period."""
    table = flight_table(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    heading = np.array([HEADING_OFFSET])
    period = int(table.period[HEADING_OFFSET])
    return int(table.manhattan_steps(heading, np.array([period]))[0]) / period


C = beam_speed()


def momentum(fraction: float, content: int) -> int:
    """The momentum p (in label units) that gives the speed `fraction` x c
    to a free source of content `content`: v = p / (Q S M + p)."""
    v = fraction * C
    return round(Q * WIDTH * content * v / (1 - v))


def speed(p: int, content: int) -> float:
    return p / (Q * WIDTH * content + p)


def sources(factor: int) -> list[tuple[str, tuple[int, int, int], list[int], int]]:
    """(family name, position, momentum vector, rank) of the twenty-four
    sources: on each axis a chain of CHAIN sources at r_0 = MASS_RADIUS +
    SPACING x rank, the speed c x LADDER[axis] x (2 rank - 1) / (2 CHAIN -
    1); the pushing crowd's momentum is `factor` times the coasting
    crowd's, for the same speed at `factor` times the content."""
    found = []
    for axis, (name, ladder) in enumerate(zip(AXES, LADDER, strict=True)):
        port = PORT_HEADINGS[axis]
        for rank in range(1, CHAIN + 1):
            fraction = ladder * (2 * rank - 1) / (2 * CHAIN - 1)
            p = momentum(fraction, LIGHT) * factor
            distance = MASS_RADIUS + SPACING * rank
            x, y, z = (CENTRE[k] + port[k] * distance for k in range(3))
            found.append((f"{name}{rank}", (x, y, z), [port[k] * p for k in range(3)], rank))
    return found


def inward(p: list[int]) -> list[list[int]]:
    """The heading toward the centre of a momentum along one axis."""
    axis = next(k for k in range(3) if p[k])
    outward = PORT_HEADINGS[2 * axis + (0 if p[axis] > 0 else 1)]
    return [[-v for v in outward]]


def world(crowd: str, clock: str) -> Json:
    factor = CROWDS[crowd]
    content = LIGHT * factor
    thrown = sources(factor)
    names = [name for name, _, _, _ in thrown]
    families: list[Json] = [
        {"name": "detector", "quantum": 1},
        {"name": "mass", "quantum": 0, "phase": False},
        *({"name": name, "quantum": 0} for name in names),
    ]

    def entry(rule: str, name: str | None = None) -> Json:
        """A table entry: the rule, reading the age moment in the `age`
        worlds (the detector's in every world)."""
        if clock == "age" or name == "detector":
            return {"rule": rule, "reads": "age"}
        return {"rule": rule}

    measured: list[Json] = [
        {
            "position": list(CENTRE),
            "family": "detector",
            "amount": 1,
            "fixed": True,
            "table": {name: entry("measure", "detector") for name in names},
        }
    ]
    for axis in range(6):
        port = PORT_HEADINGS[axis]
        measured.append(
            {
                "position": [CENTRE[k] + port[k] * MASS_RADIUS for k in range(3)],
                "family": "mass",
                "amount": 1 if factor == 1 else LIGHT * CHAIN * factor,
                "fixed": True,
                "directions": [list(port)],
                "table": {name: entry("pass") for name in names},
            }
        )
    for name, position, p, _ in thrown:
        source: Json = {
            "position": list(position),
            "family": name,
            "amount": content,
            "phase": 0,
            "momentum": p,
            "directions": inward(p),
        }
        if clock == "age":
            source["table"] = {other: entry("read") for other in ["mass", *names] if other != name}
        measured.append(source)
    return {
        "law": "rays",
        "model_id": f"rays-hubble-{crowd}-{clock}-space-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "ticks": TICKS,
        "K": content,
        "N": N,
        "release": RELEASE,
        "suspension": CLOCKS[clock],
        "width": WIDTH,
        "families": families,
        "measured": measured,
        "detectors": [
            {"name": "centre", "positions": [list(CENTRE)], "threshold": 1, "reading": "wave"}
        ],
    }


def main() -> None:
    print(f"c = {C:.5f} Links per interval on a heading (the flight table)")
    print("| axis | rank | r_0 | v / c | v (Links per interval) | p coasting | p pushing |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for (name, _, p, rank), (_, _, p_push, _) in zip(sources(1), sources(FACTOR), strict=True):
        axis = next(k for k in range(3) if p[k])
        v = speed(abs(p[axis]), LIGHT)
        assert speed(abs(p_push[axis]), LIGHT * FACTOR) == v
        print(
            f"| {name[:2]} | {rank} | {MASS_RADIUS + SPACING * rank} | {v / C:.4f} | {v:.4f} | "
            f"{abs(p[axis])} | {abs(p_push[axis])} |"
        )
    for crowd in CROWDS:
        for clock in CLOCKS:
            path = HERE / f"{crowd}_{clock}.json"
            path.write_text(json.dumps(world(crowd, clock), separators=(",", ":")) + "\n")
            print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
