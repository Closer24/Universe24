"""Write the five worlds of series D3, Newton after a detector: series D's
circular orbit on the plane read by a lamp on the probe and a line of
one-Node detectors, with the expectations before the runs
(`expectations.json`).

The chief physicist's design (records 574 and 594 of docs/LOG_2026-09-20.md;
the owner's word "build them", record 581, and "Build" on the deviation of
01:09Z, 2026-09-22): a body that falls or orbits is measured only by where
its light comes from and when (Highlights 5.4, records 281, 562, 564, 569),
so the probe of series D carries a lamp and a detector line reads the
lamp's rows; the probe's own record is never read.

The base is series D's plane (examples/events/orbit/make_worlds.py): a
GameBoard of SIDE x SIDE x 1 Nodes with the z axis periodic, the centre c,
a fixed source of the free phase-less family `m` at c releasing one ray
per direction every 10 intervals on the uniform fan of every primitive
in-plane direction (a, b, 0) with 0 < a^2 + b^2 <= P^2 (P = 8, 120
directions, q = 12 units per interval, L = 1.0000 the fan's mean |u_d| /
Q), and the probe at (c_x + r, c_y, 0) with the tangential momentum of the
circular orbit under the law's drive. Since 2026-09-22 (the model owner's
word, record 972; docs/designs/drive_b/DEFAULT.md) the law's drive of a
body is the line drive (BEAM_LAW note 17 as amended, note 49): the pace
64 n / (64 S + 110 n) on a heading with n = p / (Q M_total), the circular
condition n x pace(n) = q L C / (2 pi) giving n = 9.63 at S = 32, the
nearest whole 10, and the shipped worlds and pins are at n = 10 (the
third registration of the series). History, kept in README.md with its
readings: the first run of 2026-09-22 declared n = 10 under that pace
while the engine ran the per-axis drive of note 17 (the cause read off
the controls); the re-run on the owner's word of 01:42Z at n = 9, the
per-axis drive's circle (the pace n / (S + n), the condition n^2 / (S +
n) = q L C / (2 pi), the root 8.83, series D's p = 576 per unit of
content), is the reading the paper's D3 row rests on, read under the
per-axis drive; `expectations(HISTORY_N, AXIS_DRIVE)` reproduces its pins.

What changes from series D, and nothing else (the deviation of 00:56Z and
the chief physicist's word on it):

- The probe is a body of a paid family of its own, `probe` (`quantum` 1,
  the default phase circle: the lamp's turn, and so its release, is 0 on
  a family without one), of `amount` R = 2^12, the lamp's reservoir (the
  form of hubble_stars' stars: a lamp spends its own family's content, one
  unit per row at the turn 1), holding the free mass `held` {"m": M_held}
  with M_held = 2^20 that the fan pushes (the keys' own rule for `m`,
  `read`, not written out: the push taken, the rays go on); the content the push scales with and the step
  divides by is M_total = R + M_held, so the momentum is p = n Q M_total
  and the reservoir is 0.4 % of it. The world's clock K is M_held, so the
  turn is 1 at every self-creation (2 at about 16 of 4000, the reservoir
  above K; a turn of 0, a missed birth, never).
- The lamp: `rate` [1, 8] (one unit per direction every 8 intervals),
  `wheel` [1, N], `directions` [[0, 1, 0], [0, -1, 0]]: two rows per
  birth in opposite directions, so the recoil cancels exactly by the pair
  (a lamp toward one side alone drives the probe sideways at 1 / (S + 1)
  Links per interval, more than the reading). The row toward -y reaches
  the detector line; its twin is lost to the +y face.
- The detector line: at y = Y_D, one measured event of the paid family
  `wall` at every column x, each declared as the one-Node detector
  `line_<x>` reading `wave` at the threshold 1 (the lensing screen's form),
  its entry for `probe` {"rule": "measure", "reads": "age"} so that every
  click carries the row's age (the flight), its entry for `m` `pass` (the
  fan crosses the line unread). A row born at (x, y) at the tick t on the
  heading -y keeps its x, so the click at `line_<x>` at the tick t + age
  reads x(t) directly: the probe's x at the birth, one reading every 8
  intervals, the only reading of the probe there is.
- The source's content is M = 2^32 at `release` [1, 2^32 x 10] (series
  D: 2^10 at [1, 2^10 x 10]): the same one ray per direction every 10
  intervals, the same q; the denominator is scaled so that the probe's
  held mass, which the same key would release on the six headings at
  `by_clock(age, M_held, d)`, releases nothing within the run (its first
  ray at the age d / M_held = 40960, 10240 in the 4 M_held world).
- The source's table entry for `probe` is `pass`.
- The probe's `directions` are the lamp's pair. They are the directions a
  body re-emits on: a row of the probe's own number that arrives at the
  probe's Node is taken home (the probe steps into the Node of a row it
  released one or two intervals before, on the side of the orbit where it
  moves along that row's heading) and created again at the next
  self-creation, apportioned whole over the body's directions (the six
  headings by default, among them +-z, which on this plane of one Node
  in z bring the row home at once). On the pair a homed row is created
  again on +y or -y: a birth whose row toward -y came home is read late
  (the re-creation's tick and x, a reading of the probe all the same) or
  not at all; the tool reads the clicks as they come and assumes no
  birth. The row's momentum comes home with it and leaves again at the
  re-creation: 64 label units against p of 6 x 10^8, nothing.

| World | The source | r | `held` m | K | p (label units) | What it asks |
| --- | --- | --- | --- | --- | --- | --- |
| `r12` | M, the fan | 12 | 2^20 | 2^20 | 640 x (2^12 + 2^20) | the orbit's period at r = 12 |
| `r24` | the same | 24 | 2^20 | 2^20 | the same | at r = 24: the ratio 2.00 |
| `r24_4m` | the same | 24 | 2^22 | 2^22 | 640 x (2^12 + 2^22) | the equivalence: four times the mass on the same clicks |
| `r12_control` | none | 12 | 2^20 | 2^20 | as `r12` | the probe alone: x constant, no turn |
| `r24_control` | none | 24 | 2^20 | 2^20 | as `r24` | the same at r = 24 |

The pins, written here before any run (`expectations()`; the numbers
printed by `main()` and registered in `expectations.json`; the derivation
DERIVATIONS_BEAM 3.3, Newton's law on the plane: the mean push over a ring
q L C / (2 pi r), a 1 / r force; the orbit sweeps every line of the fan
once per turn, so its mean push per turn is the ring mean exactly, which a
resting Node never reads, DERIVATIONS 3.2):

- The period T = 2 pi r / v with v the pace at n = 10 under the line
  drive (640 / 3148 = 0.2033 Links per interval on a heading, the same
  at every radius: the flat rotation curve of a 1 / r force): 371
  intervals at r = 12 and 742 at r = 24 (the per-axis drive's n = 9 read
  343 and 687, series D's table), each within the continuum map's own margin
  of 9 percent (the burst field and the fan's grain; the orbit register's
  lamp worlds). DETECTOR: the recurrence of the clicks' x, the mean
  spacing of successive crossings of the centre column by x(t) in one
  direction.
- The ratio T(24) / T(12) = 2.00 +- 0.18 (the 9 percent on each period,
  propagated): the exponent k = 2 on the plane (Kepler's k = 3 in space
  would give 2.83).
- The second difference of the clicks' x against t: x(t + h) - 2 x(t) +
  x(t - h) = -4 sin^2(omega h / 2) (x(t) - c_x) for a turning at the
  angular rate omega = 2 pi / T, read at the lag h of about a quarter
  period (the grain 1 Node on x against a signal of 2 r Links); omega^2 =
  (2 pi / T)^2 per interval^2 at both radii (the bracket from T's), the
  acceleration a = omega^2 r = v^2 / r: 3.44e-3 Links per interval^2 at
  r = 12 and 1.72e-3 at r = 24, the ratio 2.00; in the small-n limit
  (v = n / S) this is 3.3's q L C / (2 pi r S) = 4.97e-3 and 2.49e-3
  (the ratio 2.00 again); at n = 10 the pace 640 / 3148 is 0.65 of the
  limit's 10 / 32, so the pinned a is v^2 / r at the declared pace.
- The amplitude of the clicks' x, (max - min) / 2, the orbit's radius:
  r - 1 to r + 2 (the near-circular loop of the whole n above 9.63).
- The equivalence: `r24_4m` reads the same period as `r24` within one
  birth interval (8), and the same x on every common birth tick within
  one Node.
- The controls: every click at x = c_x + r (no push, no turn); the probe
  leaves through the face +y at the tick (SIDE - c_y) / v, the 61st step
  (from y = 60 to 121) at the pace, about 300 (the per-axis re-run at
  n = 9 pinned 278 and read 278; the first run pinned 60 steps, 295, and
  read 257, the 61st step at the per-axis 0.238 the engine then ran).
- Refuted if the ratio leaves 2.00 +- 0.18, a period leaves its bracket,
  the second difference's omega^2 leaves its bracket, or the two held
  masses' periods differ beyond one birth interval. A record check
  (completed, the books balanced at every tick) fails the tool. Every
  number the tool prints is a DETECTOR reading (the clicks' x, tick and
  age) or a GAMEBOARD diagnostic, labelled; only the first is pinned.

`expectations(n, drive)` gives the pins for either drive, so that the
per-axis re-run's pins (n = 9, the drive of history: T = 343 and 687)
stay reproducible beside the shipped ones (the test pins both); the
shipped `expectations.json` is the line drive's at n = 10.

The one-constant worlds (flow-link-v1, the owner's decision of 2026-09-22,
record 915 of docs/LOG_2026-09-20.md; the design
docs/designs/flow_weight/DESIGN.md section 3 (c) and ALGEBRA.md section 5):
under the world key `flow_link` every push a reader sums is divided by its
fan's mean of S_1 / |D|, the Nodes per Euclidean Link of a digital line,
which on this fan of 120 is F_plane = 1.2871 (4 / pi in the isotropic
limit), so the circular balance becomes n^2 / (S + n) = q L C / (2 pi
F_plane): the real root 7.673 at S = 32, the nearest whole 8 (the design's
7.818 divides the declared whole 9's balance 81 / 41 = 1.976 in place of
the real root's 1.910; both round to 8, and the generator takes its own
root, as it took 8.83 to 9). `worlds(flow=True)` writes `r12_flow`,
`r24_flow`, `r12_flow_control` and `r24_flow_control`: the registered
worlds with the key and the probe's momentum at the whole 8 (T = 2 pi r
(S + n) / n = 377 and 754 at r = 12 and 24; 384 and 768 at the design's
7.818), nothing else changed; `expectations(flow=True)` their pins
(`expectations_flow.json`), the band the register's 9 percent, the ratio
T(24) / T(12) = 2.00 +- 0.18 unchanged (the same fan and the same weight
per line at both radii), the controls' escape at the 61st step of the
pace 8 / 40. Every number a formula's (GAMEBOARD) until the run; the
clicks the measurement (DETECTOR). No equivalence world under the key:
the equivalence is closed by the registered run and carries no constant.
Under the line drive, the law's drive since the same day (the merge of
the two on 2026-09-22), the balance is n x pace(n) = q L C / (2 pi
F_plane) with the pace 64 n / (64 S + 110 n): the real root 8.28, the same
whole 8 (the momentum of the four worlds unchanged), the pace 8 x 64 /
(64 x 32 + 8 x 110) = 0.1749, T = 431 and 862 at r = 12 and 24, the
controls' escape at the 61st step of that pace (349); the shipped
`expectations_flow.json` is the line drive's, and `expectations(drive=
AXIS_DRIVE, flow=True)` reproduces the per-axis pins the run of
`run_flow.out` was read against (377 and 754, the escape 305).

    python examples/events/orbit_lamp/make_worlds.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.events.nature_beam import unit_label  # noqa: E402
from event_universe.events.world import LABEL_SCALE  # noqa: E402
from event_universe.register_map import carry_replicated  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113): `wall` and
# `m`; the paid `probe` differs from the shipped free one and stays inline.
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

SIDE = 121
SHAPE = [SIDE, SIDE, 1]
BOUNDARY = {"z": "periodic"}
CENTRE = (60, 60, 0)
N = 64
# The source: one ray per direction every 10 intervals, series D's rate,
# with the content and the denominator scaled by 2^22 so that the probe's
# held mass releases nothing within the run (the module docstring).
SOURCE = 1 << 32
RELEASE_D = SOURCE * 10
RATE = SOURCE / RELEASE_D
FAN_RADIUS = 8
WIDTH = 32
TICKS = 4000
RADII = (12, 24)
# The probe: the lamp's reservoir R and the held mass; the equivalence
# world holds four times the mass.
RESERVOIR = 1 << 12
HELD_MASS = 1 << 20
EQUIVALENCE_FACTOR = 4
LAMP_RATE = [1, 8]
LAMP_DIRECTIONS = [[0, 1, 0], [0, -1, 0]]
# The detector line: below the orbit (the orbit's lowest y is c_y - 24 =
# 36), reading the rows toward -y.
Y_D = 20
PROBE_FAMILY = "probe"
WALL_FAMILY = "wall"
MASS_FAMILY = "m"
DETECTOR_PREFIX = "line_"
# The two drives a circle can be declared under: the line drive, the law's
# drive of a body since 2026-09-22 (BEAM_LAW note 17 as amended, note 49:
# the pace n Q / (Q S + n T_D) on a heading; the circle's real root 9.63
# at S = 32, the whole 10) and the per-axis drive of history (note 17 as
# it ran until that day, the world key `per_axis_drive`: the pace n / (S +
# n) per axis; the circle at n^2 / (S + n) = q L C / (2 pi), the real root
# 8.83, the whole 9, series D's p = 576 per unit of content), the drive
# the registered re-run of 2026-09-22 was read under.
AXIS_DRIVE = "axis"
LINE_DRIVE = "line"
DRIVE = LINE_DRIVE
ORBIT_N = 10
HISTORY_N = 9
# flow-link-v1 (the module docstring): the world key, the names' suffix and
# the whole n of the circle under the key (asserted against the generator's
# own root by `expectations(flow=True)`: under the line drive the real root
# 8.28 and the whole 8, as under the per-axis pace it was 7.67 and 8).
FLOW_KEY = "flow_link"
FLOW_SUFFIX = "_flow"
ORBIT_N_FLOW = 8
T_D_AXIS = 110  # the axis direction's period constant, isqrt(3 Q^2) at Q = 64
# The tool's constant of the flow on the plane, flow x 2 pi r / q (series C).
FLOW_CONSTANT = 1.0
# The continuum map's own margin on a period (the orbit register's lamp
# worlds: the burst field and the fan's grain), and the ratio's from it.
PERIOD_MARGIN = 0.09
RATIO_PIN = 2.0
RATIO_MARGIN = 0.18
# One birth interval: the equivalence's bracket on the period.
BIRTH_INTERVAL = LAMP_RATE[1] // LAMP_RATE[0]
# The amplitude's bracket about r (the loop's extents).
AMPLITUDE_BELOW = 1
AMPLITUDE_ABOVE = 2
# The escape tick's bracket in the controls (the drive's integer steps).
ESCAPE_MARGIN = 6
EXPECTATIONS_FORMAT = "orbit-lamp-expectations-v1"
MODEL_PREFIX = "rays-orbit-lamp-"
MODEL_SUFFIX = "-plane-v1"
Json = dict[str, object]


def fan(radius: int) -> list[list[int]]:
    """Every primitive in-plane direction (a, b, 0) with 0 < a^2 + b^2 <=
    radius^2, in a fixed order (by angle from +x): series D's fan."""
    found = []
    for a in range(-radius, radius + 1):
        for b in range(-radius, radius + 1):
            if (a or b) and a * a + b * b <= radius * radius and math.gcd(abs(a), abs(b)) == 1:
                found.append([a, b, 0])
    found.sort(key=lambda v: math.atan2(v[1], v[0]) % (2 * math.pi))
    return found


FAN = fan(FAN_RADIUS)
HEADINGS = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)}
DECLARED = [v for v in FAN if tuple(v) not in HEADINGS]
EMISSION = len(FAN) * RATE
LABEL_MAGNITUDE = sum(math.hypot(*unit_label((a, b, c))) / LABEL_SCALE for a, b, c in FAN) / len(FAN)
# The circular condition's constant A = q L C / (2 pi) (DERIVATIONS_BEAM 3.3).
CIRCLE_CONSTANT = EMISSION * LABEL_MAGNITUDE * FLOW_CONSTANT / (2 * math.pi)
# F_plane, the fan's mean of S_1 / |D| (the Nodes per Euclidean Link of the
# digital line of D): the factor every push carries as the law is built and
# loses under the key `flow_link` (DESIGN.md section 1.3; 1.2871 on this
# fan, 4 / pi = 1.2732 in the isotropic limit).
FLOW_INCIDENCE = sum(sum(abs(c) for c in v) / math.hypot(*v) for v in FAN) / len(FAN)


def circle_constant(flow: bool = False) -> float:
    """A, the circular condition's constant: q L C / (2 pi) as the law is
    built, divided by F_plane under the key (ALGEBRA.md section 5)."""
    return CIRCLE_CONSTANT / (FLOW_INCIDENCE if flow else 1.0)


def pace(n: float, width: int, drive: str = DRIVE) -> float:
    """The pace of a body at n = p / (Q M) per unit of content, in Links per
    interval: the line drive's n Q / (Q S + n T_D) on a heading (the law's,
    BEAM_LAW note 17 as amended, note 49) or the per-axis drive of history's
    n / (S + n) (the world key `per_axis_drive`)."""
    if drive == AXIS_DRIVE:
        return n / (width + n)
    if drive == LINE_DRIVE:
        return n * LABEL_SCALE / (LABEL_SCALE * width + n * T_D_AXIS)
    raise ValueError(f"unknown drive {drive!r}")


def orbit_momentum(width: int, drive: str = DRIVE, flow: bool = False) -> tuple[float, int]:
    """The circular-orbit n per unit of content, n x pace(n) = A: the real
    root and the nearest whole (the orbit register's lamp worlds'
    derivation under the line drive; series D's under the per-axis one; A
    divided by F_plane under the key `flow_link`)."""
    a = circle_constant(flow)
    if drive == AXIS_DRIVE:
        n = (a + math.sqrt(a * a + 4 * width * a)) / 2
    elif drive == LINE_DRIVE:
        n = (
            T_D_AXIS * a + math.sqrt((T_D_AXIS * a) ** 2 + 4 * LABEL_SCALE * LABEL_SCALE * width * a)
        ) / (2 * LABEL_SCALE)
    else:
        raise ValueError(f"unknown drive {drive!r}")
    return n, max(1, round(n))


PACE = pace(ORBIT_N, WIDTH, DRIVE)


def period(radius: int, n: int = ORBIT_N, drive: str = DRIVE) -> float:
    """The analytic circle's period 2 pi r / v at the pace of n."""
    return 2 * math.pi * radius / pace(n, WIDTH, drive)


def held_mass(name: str) -> int:
    return HELD_MASS * (EQUIVALENCE_FACTOR if name.endswith("_4m") else 1)


WORLDS: dict[str, dict[str, object]] = {
    "r12": {"radius": 12, "source": True},
    "r24": {"radius": 24, "source": True},
    "r24_4m": {"radius": 24, "source": True},
    "r12_control": {"radius": 12, "source": False},
    "r24_control": {"radius": 24, "source": False},
}
# The one-constant worlds: the registered `r12`, `r24` and their controls
# under the key `flow_link`, the momentum at ORBIT_N_FLOW (the module
# docstring); no equivalence world.
WORLDS_FLOW: dict[str, dict[str, object]] = {
    f"r12{FLOW_SUFFIX}": {"radius": 12, "source": True},
    f"r24{FLOW_SUFFIX}": {"radius": 24, "source": True},
    f"r12{FLOW_SUFFIX}_control": {"radius": 12, "source": False},
    f"r24{FLOW_SUFFIX}_control": {"radius": 24, "source": False},
}


def declared_n(n: int | None, flow: bool) -> int:
    """The declared whole n: the argument, else the register's 9 (the whole
    8 under the key)."""
    return n if n is not None else (ORBIT_N_FLOW if flow else ORBIT_N)


def world(name: str, n: int | None = None, flow: bool = False) -> Json:
    keys = (WORLDS_FLOW if flow else WORLDS)[name]
    n = declared_n(n, flow)
    radius = int(keys["radius"])
    mass = held_mass(name)
    total = RESERVOIR + mass
    measured: list[Json] = []
    if keys["source"]:
        measured.append(
            {
                "position": list(CENTRE),
                "family": MASS_FAMILY,
                "amount": SOURCE,
                "phase": 0,
                "fixed": True,
                "directions": [list(v) for v in FAN],
                "table": {PROBE_FAMILY: "pass"},
            }
        )
    measured.append(
        {
            "position": [CENTRE[0] + radius, CENTRE[1], CENTRE[2]],
            "family": PROBE_FAMILY,
            "amount": RESERVOIR,
            "phase": 0,
            "fixed": False,
            # In label units: n units of the probe's whole content, Q each.
            "momentum": [0, n * LABEL_SCALE * total, 0],
            "held": {MASS_FAMILY: mass},
            # The entry for `m` is the keys' own, `read` (the push taken, the
            # rays go on), and a default entry is not written out (the
            # default-table rule (d), `tests/test_default_table.py`).
            # The directions the body re-emits on (a row of its own taken
            # home): the lamp's pair, not the six headings (the docstring).
            "directions": [list(v) for v in LAMP_DIRECTIONS],
            "lamp": {
                "rate": list(LAMP_RATE),
                "wheel": [1, N],
                "directions": [list(v) for v in LAMP_DIRECTIONS],
            },
        }
    )
    detectors: list[Json] = []
    for x in range(SIDE):
        measured.append(
            {
                "position": [x, Y_D, 0],
                "family": WALL_FAMILY,
                "amount": 1,
                "fixed": True,
                "table": {PROBE_FAMILY: {"rule": "measure", "reads": "age"}, MASS_FAMILY: "pass"},
            }
        )
        detectors.append(
            {
                "name": f"{DETECTOR_PREFIX}{x}",
                "positions": [[x, Y_D, 0]],
                "threshold": 1,
                "reading": "wave",
            }
        )
    return {
        "law": "beam",
        "model_id": f"{MODEL_PREFIX}{name.replace('_', '-')}{MODEL_SUFFIX}",
        "shape": list(SHAPE),
        "boundary": dict(BOUNDARY),
        "ticks": TICKS,
        "K": mass,
        "N": N,
        "release": [1, RELEASE_D],
        "suspension": 0,
        "width": WIDTH,
        # flow-link-v1: the key, true, on the one-constant worlds alone; the
        # registered worlds carry no key and read as they did, byte for byte
        # (DESIGN.md section 6).
        **({FLOW_KEY: True} if flow else {}),
        "directions": [list(v) for v in DECLARED],
        "families": [
            {"name": PROBE_FAMILY, "quantum": 1},
            {"name": WALL_FAMILY, "quantum": 1},
            {"name": MASS_FAMILY, "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
        "detectors": detectors,
    }


def worlds(n: int | None = None, flow: bool = False) -> dict[str, Json]:
    """The registered five, or the four one-constant worlds (`flow`)."""
    return {
        name: families_by_definition(world(name, n, flow), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        for name in (WORLDS_FLOW if flow else WORLDS)
    }


def second_difference_lag(radius: int, n: int | None = None, drive: str = DRIVE) -> int:
    """The lag of the second difference in birth intervals, about a quarter
    of the pinned period (the module docstring)."""
    return max(1, round(period(radius, declared_n(n, False), drive) / 4 / BIRTH_INTERVAL))


def expectations(n: int | None = None, drive: str = DRIVE, flow: bool = False) -> Json:
    """The pins before the runs (the module docstring) for the declared n
    under the named drive, every entry with its source in `derivations`
    (the owner's principle, record 205: a formula gives, a run proves).
    The shipped register is `expectations()`; `expectations(HISTORY_N,
    AXIS_DRIVE)` reproduces the registered re-run's pins under the per-axis
    drive of history (n = 9), and `expectations(10, LINE_DRIVE)` the first
    run's, which declared the line drive's circle before the engine ran it;
    `expectations(flow=True)` is the one-constant worlds' register
    (`expectations_flow.json`), the balance divided by F_plane."""
    n = declared_n(n, flow)
    real_n, whole_n = orbit_momentum(WIDTH, drive, flow)
    assert whole_n == n, (whole_n, n)
    v = pace(n, WIDTH, drive)
    flow_constant = FLOW_CONSTANT / (FLOW_INCIDENCE if flow else 1.0)
    small_n_limit = {
        str(r): EMISSION * LABEL_MAGNITUDE * flow_constant / (2 * math.pi * r * WIDTH) for r in RADII
    }
    if drive == AXIS_DRIVE:
        drive_note = (
            "the per-axis drive of history (BEAM_LAW note 17 as it ran until 2026-09-22, `step_axis`, "
            "the world key `per_axis_drive`): the pace n / (S + n) per axis; the circle n^2 / (S + n) "
            "= q L C / (2 pi), the real root 8.83 at S = 32, declared the nearest whole 9 (series D's "
            "p = 576 per unit of content)"
        )
    else:
        drive_note = (
            "the line drive, the law's drive of a body since 2026-09-22 (BEAM_LAW note 17 as amended, "
            "note 49; the model owner's record 972): the pace n Q / (Q S + n T_D) on a heading; the "
            "circle n x pace(n) = q L C / (2 pi), the real root 9.63 at S = 32, declared the nearest "
            "whole 10 (the orbit register's lamp worlds)"
        )
    if flow:
        drive_note = (
            "flow-link-v1 (the world key `flow_link`, docs/designs/flow_weight/DESIGN.md section 3 (c), "
            "ALGEBRA.md section 5; the owner's decision of 2026-09-22, record 915): every push divided by "
            f"the fan's mean of S_1 / |D|, F_plane = {FLOW_INCIDENCE:.4f} on this fan of 120 (4 / pi in the "
            "isotropic limit), so the circle is n x pace(n) = q L C / (2 pi F_plane) under "
            + drive_note
            + f"; the real root {real_n:.3f}, declared the nearest whole {n} (the design's 7.818 divides "
            "the whole 9's balance 81 / 41 in place of the real root's q L C / (2 pi); both round to 8); "
            "the ratio T(24) / T(12) unchanged (the same fan and the same weight per line at both radii); "
            "GAMEBOARD by formula until the run, the clicks the measurement (DETECTOR); Newton's and "
            "Kepler's forms on the comparison side only (record 817)"
        )
    found: Json = {
        "format": EXPECTATIONS_FORMAT,
        "derivations": {
            "fan": "declared: series D's uniform fan, every primitive (a, b, 0) with 0 < a^2 + b^2 <= 64",
            "emission": "the fan's directions x the release rate, q = 120 / 10 = 12 units per interval (DERIVATIONS_BEAM 3, the flux q)",
            "label_magnitude": "the fan's mean |u_d| / Q off unit_label (BEAM_LAW section 2, note 23)",
            "drive": "declared: " + drive_note,
            "orbit_n": "DERIVATIONS_BEAM 3.3 with " + drive_note,
            "pace": "the drive's pace at the declared n (the `drive` entry)",
            "period": "the analytic circle's T = 2 pi r / v at the pace (DERIVATIONS_BEAM 3.3 on the plane: v the same at every r, T proportional to r); the bracket the continuum map's 9 percent margin (the orbit register's lamp worlds, DERIVATIONS_BEAM 12b.2)",
            "ratio": "T(24) / T(12) = 2.00 on the plane (the 1 / r force's flat rotation curve; k = 2), the margin 0.18 the periods' 9 percent propagated (record 594)",
            "omega_squared": "(2 pi / T)^2 per interval^2, read as the slope of the lagged second difference of the clicks' x against x - c_x, -4 sin^2(omega h / 2) at the lag h (the module docstring); the bracket from T's",
            "acceleration": "a = omega^2 r = v^2 / r at the declared pace, and 3.3's small-n limit q L C / (2 pi r S) beside it (v = n / S there); the ratio a(12) / a(24) = 2.00 in both",
            "amplitude": "the clicks' (max x - min x) / 2 against r: the loop's extents (the orbit register's map, 24.0 to 25.9 and 12.0 to 13.0), r - 1 to r + 2",
            "equivalence": "DERIVATIONS_BEAM 3.3: nothing of the body enters the acceleration (the push scales with M_total and the step divides by it), so the 4 M_held world reads the same period within one birth interval and the same x on every common birth tick within one Node (record 594)",
            "control": "declared: no source, no push; the probe walks +y at the pace and leaves through the face +y at its 61st step, (SIDE - c_y) / v intervals (the step from y = 120 to 121); every click at x = c_x + r"
            + (
                "; under the key a world without a crowd reads nothing (DESIGN.md section 3 (d)): a control "
                "click off x = c_x + r, or an escape off its bracket, is the control moving under the key and "
                "refutes"
                if flow
                else ""
            ),
            "flight": "the row's age on the click is its flight from the birth's y to Y_D on the heading -y, c = Q / T_D = 32 / 55 Links per interval (DERIVATIONS_BEAM 2.1): the birth tick is the click's tick less its age",
        },
        "side": SIDE,
        "centre": list(CENTRE),
        "detector_y": Y_D,
        "birth_interval": BIRTH_INTERVAL,
        "fan_directions": len(FAN),
        "emission": EMISSION,
        "label_magnitude": LABEL_MAGNITUDE,
        "flow_constant": flow_constant,
        "width": WIDTH,
        "drive": drive,
        "orbit_n_real": real_n,
        "orbit_n": n,
        "pace": v,
        "ratio": {"pin": RATIO_PIN, "bracket": [RATIO_PIN - RATIO_MARGIN, RATIO_PIN + RATIO_MARGIN]},
        "worlds": {},
    }
    if flow:
        found["derivations"]["flow_link"] = (
            "declared: the key `flow_link` true on the four worlds and on none of the registered ones; "
            "the pins that move under it are the push's alone (the period, omega^2, the acceleration: by "
            "1 / F_plane on the balance), the ratio, the amplitude's bracket and every clock and flight "
            "reading unchanged (DESIGN.md section 3 (c) and (d)); refuted by T outside its bracket, the "
            "ratio outside its bracket, or the control moving under the key"
        )
        found["derivations"]["flow_incidence"] = (
            "the fan's mean of S_1 / |D| over the 120 directions, the Nodes per Euclidean Link of the "
            "digital line of D (DESIGN.md section 1.3): the factor the push carries as the law is built and "
            "loses under the key; series C's flow x 2 pi r / q = 1.00 per Node becomes 1 / F_plane"
        )
        found[FLOW_KEY] = True
        found["flow_incidence"] = FLOW_INCIDENCE
        found["ratio"]["worlds"] = [f"r12{FLOW_SUFFIX}", f"r24{FLOW_SUFFIX}"]
    for name, keys in (WORLDS_FLOW if flow else WORLDS).items():
        radius = int(keys["radius"])
        entry: Json = {
            "radius": radius,
            "source": keys["source"],
            "held_mass": held_mass(name),
            "reservoir": RESERVOIR,
            "momentum": n * LABEL_SCALE * (RESERVOIR + held_mass(name)),
        }
        if keys["source"]:
            t = period(radius, n, drive)
            omega2 = (2 * math.pi / t) ** 2
            lo, hi = t * (1 - PERIOD_MARGIN), t * (1 + PERIOD_MARGIN)
            entry.update(
                {
                    "period": {"pin": t, "bracket": [lo, hi]},
                    "second_difference_lag": second_difference_lag(radius, n, drive),
                    "omega_squared": {
                        "pin": omega2,
                        "bracket": [(2 * math.pi / hi) ** 2, (2 * math.pi / lo) ** 2],
                    },
                    "acceleration": {
                        "pin": omega2 * radius,
                        "small_n_limit": small_n_limit[str(radius)],
                    },
                    "amplitude": {
                        "pin": radius,
                        "bracket": [radius - AMPLITUDE_BELOW, radius + AMPLITUDE_ABOVE],
                    },
                }
            )
        else:
            escape = (SIDE - CENTRE[1]) / v
            entry.update(
                {
                    "x": CENTRE[0] + radius,
                    "escape_tick": {
                        "pin": escape,
                        "bracket": [escape - ESCAPE_MARGIN, escape + ESCAPE_MARGIN],
                    },
                }
            )
        found["worlds"][name] = entry
    if not flow:
        found["equivalence"] = {
            "worlds": ["r24", "r24_4m"],
            "period_difference_bracket": BIRTH_INTERVAL,
            "x_difference_bracket": 1,
        }
    found["acceleration_ratio"] = {
        "pin": RATIO_PIN,
        "bracket": [RATIO_PIN - RATIO_MARGIN, RATIO_PIN + RATIO_MARGIN],
    }
    return found


def main() -> None:
    real_n, whole_n = orbit_momentum(WIDTH, DRIVE)
    print(
        f"fan: {len(FAN)} directions ({len(DECLARED)} declared), q = {EMISSION:.2f} per interval, "
        f"L = {LABEL_MAGNITUDE:.4f}; S = {WIDTH}, the {DRIVE} drive: n = {real_n:.3f} -> {whole_n}, "
        f"the pace {PACE:.4f} Links per interval; the probe's content {RESERVOIR} + {HELD_MASS} (the 4 M "
        f"world {RESERVOIR} + {EQUIVALENCE_FACTOR * HELD_MASS}); the source {SOURCE} at release "
        f"[1, {RELEASE_D}], the held mass's first ray at the age {RELEASE_D // HELD_MASS} "
        f"({RELEASE_D // (EQUIVALENCE_FACTOR * HELD_MASS)})"
    )
    for radius in RADII:
        t = period(radius)
        print(
            f"r = {radius}: T = {t:.1f} ({t * (1 - PERIOD_MARGIN):.0f} to {t * (1 + PERIOD_MARGIN):.0f}), "
            f"omega^2 = {(2 * math.pi / t) ** 2:.3e}, a = v^2 / r = {(2 * math.pi / t) ** 2 * radius:.3e} "
            f"(the small-n limit q L C / (2 pi r S) = "
            f"{EMISSION * LABEL_MAGNITUDE / (2 * math.pi * radius * WIDTH):.3e}), "
            f"the second difference's lag {second_difference_lag(radius)} births"
        )
    print(
        f"the ratio T(24) / T(12) = {RATIO_PIN:.2f} +- {RATIO_MARGIN:.2f}; the controls' escape at about "
        f"{(SIDE - CENTRE[1]) / PACE:.0f}"
    )
    real_flow, whole_flow = orbit_momentum(WIDTH, DRIVE, flow=True)
    print(
        f"flow-link-v1: F_plane = {FLOW_INCIDENCE:.4f} (4 / pi = {4 / math.pi:.4f}), the balance "
        f"{circle_constant():.4f} / F_plane = {circle_constant(True):.4f}: n = {real_flow:.3f} -> "
        f"{whole_flow}, the pace {pace(whole_flow, WIDTH):.4f}; "
        + "; ".join(
            f"r = {r}: T = {period(r, whole_flow):.1f} ({period(r, whole_flow) * (1 - PERIOD_MARGIN):.0f} "
            f"to {period(r, whole_flow) * (1 + PERIOD_MARGIN):.0f})"
            for r in RADII
        )
        + f"; the controls' escape at about {(SIDE - CENTRE[1]) / pace(whole_flow, WIDTH):.0f}"
    )
    for flow, register in ((False, "expectations.json"), (True, "expectations_flow.json")):
        for name, document in worlds(flow=flow).items():
            path = HERE / f"{name}.json"
            path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
            print(path.relative_to(ROOT))
        expected = expectations(flow=flow)
        (HERE / register).write_text(
            json.dumps(carry_replicated(HERE / register, expected), indent=1) + "\n",
            encoding="utf-8",
        )
        print((HERE / register).relative_to(ROOT))


if __name__ == "__main__":
    main()
