"""Write the four worlds of series G, the Hubble diagram behind the detector,
under the Beam Law, in space.

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
axis; under the law's drive of a body, since 2026-09-22 the line drive (the
model owner's word, record 972; docs/designs/drive_b/DEFAULT.md; BEAM_LAW
note 17 as amended, note 49), its accumulator gains p Q per interval against
the wall Q^2 S M + p T_D (Q = 64, S the world's `width`, T_D = 110), so its
speed is v = p Q / (Q^2 S M + p T_D) Links per interval and p = Q S M v /
(1 - v T_D / Q); the per-axis drive of history (note 17 as it ran until that
day, the world key `per_axis_drive`, the drive the registered runs were read
under: one Link per (Q S M + p) / p self-creations, v = p / (Q S M + p), p =
Q S M v / (1 - v)) is kept as `AXIS_DRIVE` and `sources(factor, AXIS_DRIVE)`
reproduces its momenta; p is chosen for the speed ladder v = c x V(axis)
x (2 i - 1) / (2 CHAIN - 1) with V from 0.35 to 0.6: the twenty-four speeds
span 0.05 c to 0.6 c, c the ray's speed on a heading read off the flight
table (`direction_flight`: m(L) Links per period L, 32 / 55 = 0.5818 per
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
BEAM_LAW section 3 step 4, the equivalence principle, so the speed changes
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

The pins are written to `expectations.json` (`expectations(drive,
centred)`, the register's form of `orbit_lamp/`): the sources' speeds and
momenta under the drive, the interval of each source's first Link (a
GAMEBOARD number), the criteria of README.md with their brackets, every
entry with its source in `derivations`.

    python examples/events/hubble/make_worlds.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.core.game_board import PORT_HEADINGS  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, Q  # noqa: E402
from event_universe.register_map import carry_replicated  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

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
# The two drives a throw is derived under (docs/designs/drive_b/DEFAULT.md
# section (c)): the line drive, the law's drive of a body since 2026-09-22
# (v = p Q / (Q^2 S M + p T_D)), and the per-axis drive of history (v = p /
# (Q S M + p); the world key `per_axis_drive`).
LINE_DRIVE = "line"
AXIS_DRIVE = "axis"
DRIVE = LINE_DRIVE
T_D_AXIS = 110  # the axis direction's period constant, isqrt(3 Q^2) at Q = 64
PACE_TERM = T_D_AXIS / Q  # 110 / 64
EXPECTATIONS_FORMAT = "hubble-expectations-v1"
Json = dict[str, object]


def beam_speed() -> float:
    """The ray's speed on a heading, read off the flight table: the Links
    made in one period of the heading's digital line over the period."""
    table = direction_flight(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    heading = np.array([HEADING_OFFSET])
    period = int(table.period[HEADING_OFFSET])
    return int(table.manhattan_steps(heading, np.array([period]))[0]) / period


C = beam_speed()


def momentum(fraction: float, content: int, drive: str = DRIVE) -> int:
    """The momentum p (in label units) that gives the speed `fraction` x c
    to a free source of content `content` under the named drive: the line
    drive's v = p Q / (Q^2 S M + p T_D), so p = Q S M v / (1 - v T_D / Q);
    the per-axis drive of history's v = p / (Q S M + p), p = Q S M v / (1 -
    v)."""
    v = fraction * C
    if drive == LINE_DRIVE:
        return round(Q * WIDTH * content * v / (1 - v * PACE_TERM))
    if drive == AXIS_DRIVE:
        return round(Q * WIDTH * content * v / (1 - v))
    raise ValueError(f"unknown drive {drive!r}")


def speed(p: int, content: int, drive: str = DRIVE) -> float:
    """The speed of the momentum p at the content under the named drive."""
    if drive == LINE_DRIVE:
        return p * Q / (Q * Q * WIDTH * content + p * T_D_AXIS)
    if drive == AXIS_DRIVE:
        return p / (Q * WIDTH * content + p)
    raise ValueError(f"unknown drive {drive!r}")


def push_factor(v: float, drive: str = DRIVE) -> float:
    """A row of amount a moves a source's speed by push_factor(v) x a / S
    toward the emitter: (1 - v T_D / Q)^2 under the line drive, (1 - v)^2
    under the per-axis drive of history."""
    if drive == LINE_DRIVE:
        return (1 - abs(v) * PACE_TERM) ** 2
    if drive == AXIS_DRIVE:
        return (1 - abs(v)) ** 2
    raise ValueError(f"unknown drive {drive!r}")


def first_link(p: int, content: int, drive: str = DRIVE, centred: bool = False) -> int:
    """The interval of a source's first Link from rest, a GAMEBOARD number:
    ceil(W / (p Q)) on the wall W = Q^2 S M + p T_D under the line drive
    (half the wall under `centred_step`), ceil((Q S M + p) / p) under the
    per-axis drive of history."""
    if drive == LINE_DRIVE:
        wall = Q * Q * WIDTH * content + p * T_D_AXIS
        gain = p * Q
    elif drive == AXIS_DRIVE:
        wall = Q * WIDTH * content + p
        gain = p
    else:
        raise ValueError(f"unknown drive {drive!r}")
    threshold = wall - wall // 2 if centred else wall
    return -(-threshold // gain)


def sources(factor: int, drive: str = DRIVE) -> list[tuple[str, tuple[int, int, int], list[int], int]]:
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
            p = momentum(fraction, LIGHT, drive) * factor
            distance = MASS_RADIUS + SPACING * rank
            x, y, z = (CENTRE[k] + port[k] * distance for k in range(3))
            found.append((f"{name}{rank}", (x, y, z), [port[k] * p for k in range(3)], rank))
    return found


def inward(p: list[int]) -> list[list[int]]:
    """The heading toward the centre of a momentum along one axis."""
    axis = next(k for k in range(3) if p[k])
    outward = PORT_HEADINGS[2 * axis + (0 if p[axis] > 0 else 1)]
    return [[-v for v in outward]]


def world(crowd: str, clock: str, drive: str = DRIVE) -> Json:
    factor = CROWDS[crowd]
    content = LIGHT * factor
    thrown = sources(factor, drive)
    names = [name for name, _, _, _ in thrown]
    families: list[Json] = [
        {"name": "detector", "quantum": 1},
        {"name": "mass", "quantum": 0, "phase": False},
        *({"name": name, "quantum": 0} for name in names),
    ]

    def entry(rule: str, name: str | None = None) -> Json | None:
        """A table entry: the rule, reading the age moment in the `age`
        worlds (the detector's in every world); as the world file declares
        only what differs from the default (a free family read), the default
        rule is left out of a kept object and an entry equal to the default
        is left out (None)."""
        reads = clock == "age" or name == "detector"
        if rule == "read":
            return {"reads": "age"} if reads else None
        return {"rule": rule, "reads": "age"} if reads else {"rule": rule}

    def table(entries: dict[str, Json | None]) -> dict[str, Json]:
        return {name: value for name, value in entries.items() if value is not None}

    measured: list[Json] = [
        {
            "position": list(CENTRE),
            "family": "detector",
            "amount": 1,
            "fixed": True,
            "table": table({name: entry("measure", "detector") for name in names}),
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
                "table": table({name: entry("pass") for name in names}),
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
            source["table"] = table(
                {other: entry("read") for other in ["mass", *names] if other != name}
            )
        measured.append(source)
    return {
        "law": "beam",
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


def expectations(drive: str = DRIVE, centred: bool = False) -> Json:
    """The pins before the runs (README.md, the criteria) under the named
    drive, every entry with its source in `derivations`; `centred` gives
    the same pins with every source's first Link at half the wall
    (`centred_step`, record 955: the column decided at the paper's close).
    The shipped register is `expectations()`; `expectations(AXIS_DRIVE)`
    reproduces the momenta the registered runs of 2026-09-20 were read
    with."""
    if drive == LINE_DRIVE:
        drive_note = (
            "the line drive, the law's drive of a body since 2026-09-22 (BEAM_LAW note 17 as amended, "
            "note 49; the model owner's record 972): v = p Q / (Q^2 S M + p T_D) on a heading, so p = "
            "Q S M v / (1 - v T_D / Q); a row of amount a moves the speed by (1 - v T_D / Q)^2 a / S"
        )
    else:
        drive_note = (
            "the per-axis drive of history (BEAM_LAW note 17 as it ran until 2026-09-22, the world key "
            "`per_axis_drive`): v = p / (Q S M + p), so p = Q S M v / (1 - v); a row of amount a moves "
            "the speed by (1 - v)^2 a / S"
        )
    found: Json = {
        "format": EXPECTATIONS_FORMAT,
        "derivations": {
            "c": "DERIVATIONS_BEAM 2.1: c = Q / T_D = 32 / 55 Links per interval on a heading, read off the flight table",
            "drive": "declared: " + drive_note,
            "centred": "declared (docs/designs/drive_b/DEFAULT.md section (e), record 955): under `centred_step` every source's first Link comes half a wall earlier and no pin of this series moves; the column the model owner decides at the paper's close",
            "ticks": "declared",
            "windows": "declared (the reading windows; the late window the registered reading)",
            "sources": "the speed ladder declared by the design (v = c x V(axis) x (2 i - 1) / (2 CHAIN - 1)); the momentum from it by the drive's rule at the grain (the `drive` entry), the pushing crowd's FACTOR times the coasting crowd's at FACTOR times the content; the first Link a GAMEBOARD number, ceil(W / (p Q)) on the wall (the `drive` entry)",
            "formula": "DETECTOR: 1 + z from the pointer's turn against (1 + k)(1 + v / c) with k and v from the same record, within 2 percent (README.md, the criteria)",
            "linear_law": "the coasting worlds: H fitted through the origin on z <= 0.2, H t_0 = 1 within 10 percent (the Milne form, README.md)",
            "coasting_form": "the coasting worlds: of the three forms at the near fit's H the least rms over the far part is q = 0, that rms below 0.02 in z",
            "decelerating_form": "the pushing worlds: H t_0 < 1, q_eff > 0, the accelerating form q = -0.55 the farthest of the three (a free ray pushes its reader toward its emitter)",
            "observed_today": "every world: whether the far part resembles q = -0.55 best of the three; expected outside in every run",
        },
        "c": C,
        "drive": drive,
        "centred": centred,
        "ticks": TICKS,
        "windows": [[100, 200], [200, 300], [300, 400]],
        "sources": [],
        "formula": {"tolerance": 0.02},
        "linear_law": {"pin": 1.0, "bracket": [0.9, 1.1]},
        "coasting_form": {"nearest": "q = 0", "rms_below": 0.02},
        "decelerating_form": {
            "hubble_time_below": 1.0,
            "q_effective_above": 0.0,
            "farthest": "q = -0.55",
        },
        "observed_today": {"form": "q = -0.55", "expected": "not the nearest"},
    }
    for (name, _position, p, rank), (_, _, p_push, _) in zip(
        sources(1, drive), sources(FACTOR, drive), strict=True
    ):
        axis = next(k for k in range(3) if p[k])
        v = speed(abs(p[axis]), LIGHT, drive)
        found["sources"].append(
            {
                "name": name,
                "axis": axis,
                "rank": rank,
                "initial_distance": MASS_RADIUS + SPACING * rank,
                "speed_over_c": v / C,
                "speed": v,
                "momentum_coasting": abs(p[axis]),
                "momentum_pushing": abs(p_push[axis]),
                "first_link": first_link(abs(p[axis]), LIGHT, drive, centred),
            }
        )
    return found


def main() -> None:
    print(f"c = {C:.5f} Links per interval on a heading (the flight table); the {DRIVE} drive")
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
            document = families_by_definition(
                world(crowd, clock), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE
            )
            path.write_text(json.dumps(document) + "\n", encoding="utf-8")
            print(path.relative_to(HERE.parents[2]))
    register = HERE / "expectations.json"
    register.write_text(
        json.dumps(carry_replicated(register, expectations()), indent=1) + "\n", encoding="utf-8"
    )
    print(register.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
