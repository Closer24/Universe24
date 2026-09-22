"""Write the worlds of the orbit series D under the Beam Law, on the
plane, with the width of the push.

Six worlds of one base (README.md here; the entry "D, the orbit under the
Beam Law, on the plane (2026-09-19)" in docs/EXPERIMENTS.md): a heavy
fixed source of a phase-less free family at the centre of a 121 x 121 x 1
GameBoard with the z axis periodic (the coupling series' plane), releasing a
ballistic fan of rays on every primitive in-plane direction (a, b, 0) with
0 < a^2 + b^2 <= P^2 (P = 8: the fan is uniform in angle, unlike the
primitive vectors of a square), one shell of `directions` rays every
1 / RATE intervals (content M = 2^10 at `release` [1, 2^10 x 10]: `by_clock`
gives one ray per direction at the ages 10, 20, ...), so the net emission
into the plane is q = directions x RATE units per interval; and a light
free probe of content 1 at radius r on +x with the tangential momentum
[0, p, 0] chosen for a circular orbit under the push law as it reads (the
derivation in README.md, written before the runs). The push a free probe
takes from an arriving fan ray is its label, -m x amount x u_d with u_d
the unit vector of the direction at the flight table's scale Q = 64
(BEAM_LAW section 2 and note 23; the model owner's decision of 2026-09-19
on the physics-rule reviewer's verdict), whose magnitude is Q per unit
within 1.35 % for every direction: a line of any direction crossing the
probe's ring delivers Q units of momentum per ray, so the inward label
flux through a ring is Q x q x L per interval with L the fan's mean
|u_d| / Q (`LABEL_MAGNITUDE`, 1.0000 for this fan of 120 directions,
0.994 .. 1.009 per direction; exactly 1 on the six headings of series C).
In units of one free unit's label, Q x m, the push per interval is m x q
x L x C / (2 pi r) toward the source (series C: flow x 2 pi r / q = 1.00
+- 0.10 with the flow read in units of Q, C = 1 taken). Under the line
drive, the law's drive of a body since 2026-09-22 (the model owner's word,
record 972; docs/designs/drive_b/DEFAULT.md; BEAM_LAW note 17 as amended,
note 49), the probe walks the line of its momentum at the pace n Q / (Q S
+ n T_D) = 64 n / (64 S + 110 n) on a heading with n = p / (Q m), so a
circular orbit needs n x pace(n) = q L C / (2 pi):

    64 n^2 = A (64 S + 110 n),  n = (110 A + sqrt(110^2 A^2 + 4 x 64^2 S A)) / 128,
    A = q L C / (2 pi),

independent of r (a 1 / r force on the plane: the same speed at every
radius, T proportional to r, k = 2). The worlds: `s<S>_r<r>` for S in 1, 8,
32 and r in 12, 24, the declared momentum Q times the nearest whole number
to n (in label units; the grain of the push: whole labels of Q per
arriving ray): n = 4, 6, 10 (the real roots 3.79, 5.88, 9.63). The
per-axis drive of history (note 17 as it ran until that day, the world key
`per_axis_drive`, the drive every registered run of the series was read
under: the pace n / (S + n) per axis, the circle n^2 / (S + n) = A, n = (A +
sqrt(A^2 + 4 S A)) / 2, the whole 3, 5, 9, p = 192, 320, 576) is kept as
`AXIS_DRIVE`: `orbit_momentum(S, AXIS_DRIVE)` and `expectations(AXIS_DRIVE)`
reproduce its pins. `suspension` 0: the clock's count is not read, the push
law alone moves the probe. The first registration (the push the unit Link
of a ray's last step, L = 1, p = 3, 5, 9) and the second (the label content
x amount x D, L = 5.194, p = 11, 15, 23) are in git at the D1 and the
one-form commits; the third (the label along the unit vector, p = 3, 5, 9
under the per-axis drive) is the registered one of 2026-09-19 with its
re-reads. The pins are written to `expectations.json` (`expectations(drive,
centred)`, the register's form of `orbit_lamp/`), every entry with its
source in `derivations`.

    python examples/events/orbit/make_worlds.py
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.events.nature_beam import unit_label  # noqa: E402
from event_universe.events.world import LABEL_SCALE  # noqa: E402
from event_universe.register_map import carry_replicated  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

SIDE = 121
SHAPE = [SIDE, SIDE, 1]
BOUNDARY = {"z": "periodic"}
CENTRE = (60, 60, 0)
K = 1 << 22
N = 64
SOURCE = 1 << 10
# One shell of the fan every 10 intervals: `by_clock(age, SOURCE, RELEASE_D)`.
RELEASE_D = SOURCE * 10
RATE = SOURCE / RELEASE_D
FAN_RADIUS = 8
# Five expected periods of the slowest world (S = 32 at r = 24: 687), a few
# seconds of host time per run at about 1 ms per interval.
TICKS = 4000
WIDTHS = (1, 8, 32)
RADII = (12, 24)
# The tool's constant of the flow on the plane, flow x 2 pi r / q (series C).
FLOW_CONSTANT = 1.0
# The two drives an orbit is derived under (docs/designs/drive_b/DEFAULT.md
# section (c)): the line drive, the law's drive of a body since 2026-09-22
# (the pace 64 n / (64 S + 110 n) on a heading), and the per-axis drive of
# history (the pace n / (S + n) per axis; the world key `per_axis_drive`),
# the drive the registered runs of 2026-09-19 to 2026-09-21 were read under.
LINE_DRIVE = "line"
AXIS_DRIVE = "axis"
DRIVE = LINE_DRIVE
T_D_AXIS = 110  # the axis direction's period constant, isqrt(3 Q^2) at Q = 64
PERIOD_MARGIN = 0.15
EXPECTATIONS_FORMAT = "orbit-expectations-v1"
# The lamp worlds (2026-09-21, DERIVATIONS_BEAM 21.5 row 58; the Boss's order
# on the model owner's record 333): series D's S = 32 worlds with one change
# so that a detector reads the orbit. The probe is a body of the shipped free
# family `probe` (charge 0, no phase circle: the same push as `m`) of content
# 2^10, so that at the world's one `release` it releases one row per direction
# of the same fan every 10 intervals as the source does (a body of content 1
# releases at the age 10240, beyond the run); the source's table measures the
# probe's family (the click at the source's Node) and a detector of that one
# Node reads the count (`beam`, the family having no phase circle). The
# momentum is the circular-orbit momentum under the line drive (form B,
# BEAM_LAW note 49, the law's drive since 2026-09-22; written under it on
# 2026-09-21 before it was the law's): the probe walks the line of its
# momentum at the pace n Q / (Q S + n T_D) per unit of content, 64 n / (64 S
# + 110 n) on a heading, so the circular condition n x 64 n / (64 S + 110 n)
# = A gives n = 9.63 at S = 32, the nearest whole 10 (640 label units per
# unit of content, 655360 for the probe of content 2^10; the dynamics per
# unit of content do not depend on the content: the push per ray is one unit
# of n whatever m, and the pace reads n alone). Everything else series D's;
# the two worlds are unchanged by the flip.
LAMP_WIDTH = 32
LAMP_PROBE_FAMILY = "probe"
LAMP_PROBE_CONTENT = SOURCE
LAMP_PERIOD_MARGIN = 0.09
Json = dict[str, object]


def fan(radius: int) -> list[list[int]]:
    """Every primitive in-plane direction (a, b, 0) with 0 < a^2 + b^2 <=
    radius^2, in a fixed order (by angle from +x)."""
    found = []
    for a in range(-radius, radius + 1):
        for b in range(-radius, radius + 1):
            if (a or b) and a * a + b * b <= radius * radius and math.gcd(abs(a), abs(b)) == 1:
                found.append([a, b, 0])
    found.sort(key=lambda v: math.atan2(v[1], v[0]) % (2 * math.pi))
    return found


FAN = fan(FAN_RADIUS)
# The declared table beyond the six headings (the in-plane headings are the
# table's own entries 2 .. 5).
HEADINGS = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0)}
DECLARED = [v for v in FAN if tuple(v) not in HEADINGS]
EMISSION = len(FAN) * RATE
# The mean magnitude of a label of the fan in units of Q, the mean |u_d| / Q
# over its directions: the push a fan ray gives is its label along the unit
# vector u_d of its direction, Q units of momentum per unit of amount within
# 1.35 % (BEAM_LAW section 2 and note 23).
LABEL_MAGNITUDE = sum(math.hypot(*unit_label((a, b, c))) / LABEL_SCALE for a, b, c in FAN) / len(FAN)


def pace(n: float, width: int, drive: str = DRIVE) -> float:
    """The pace of the probe at n = p / (Q m) per unit of content, in Links
    per interval: the line drive's n Q / (Q S + n T_D) on a heading (the
    law's; form B) or the per-axis drive of history's n / (S + n)."""
    if drive == LINE_DRIVE:
        return n * LABEL_SCALE / (LABEL_SCALE * width + n * T_D_AXIS)
    if drive == AXIS_DRIVE:
        return n / (width + n)
    raise ValueError(f"unknown drive {drive!r}")


def orbit_momentum(width: int, drive: str = DRIVE) -> tuple[float, int]:
    """The circular-orbit momentum in units of one free unit's label (Q times
    the probe's content), n x pace(n) = A from the derivation of the README:
    the real root and the nearest whole, under the named drive (the line
    drive: 64 n^2 = A (64 S + 110 n); the per-axis drive of history: n^2 /
    (S + n) = A)."""
    a = EMISSION * LABEL_MAGNITUDE * FLOW_CONSTANT / (2 * math.pi)
    if drive == LINE_DRIVE:
        n = (
            T_D_AXIS * a + math.sqrt((T_D_AXIS * a) ** 2 + 4 * LABEL_SCALE * LABEL_SCALE * width * a)
        ) / (2 * LABEL_SCALE)
    elif drive == AXIS_DRIVE:
        n = (a + math.sqrt(a * a + 4 * width * a)) / 2
    else:
        raise ValueError(f"unknown drive {drive!r}")
    return n, max(1, round(n))


def expected_period(width: int, radius: int, drive: str = DRIVE) -> float:
    """2 pi r / v at the pace of the whole n under the named drive."""
    _, n = orbit_momentum(width, drive)
    return 2 * math.pi * radius / pace(n, width, drive)


def form_b_pace(n: float, width: int) -> float:
    """The line drive's pace on a heading per unit of content, n Q / (Q S + n T_D)
    (form B, the law's drive since 2026-09-22): `pace(n, width, LINE_DRIVE)`."""
    return pace(n, width, LINE_DRIVE)


def orbit_momentum_form_b(width: int) -> tuple[float, int]:
    """The circular-orbit momentum under the line drive (form B): the lamp
    worlds' derivation of 2026-09-21, `orbit_momentum(width, LINE_DRIVE)`."""
    return orbit_momentum(width, LINE_DRIVE)


def first_link(n: int, width: int, content: int, drive: str = DRIVE, centred: bool = False) -> int:
    """The interval of the probe's first Link from rest on its heading, a
    GAMEBOARD number: under the line drive the accumulator gains p Q per
    interval (p = n Q m) against the wall W = Q^2 S m + p T_D (`by_line`),
    so the first Link is at ceil(W / (p Q)), or ceil((W - W // 2) / (p Q))
    under `centred_step`; under the per-axis drive of history the
    accumulator gains p against Q S m + p (`by_drive`)."""
    p = n * LABEL_SCALE * content
    if drive == LINE_DRIVE:
        wall = LABEL_SCALE * LABEL_SCALE * width * content + p * T_D_AXIS
        gain = p * LABEL_SCALE
    elif drive == AXIS_DRIVE:
        wall = LABEL_SCALE * width * content + p
        gain = p
    else:
        raise ValueError(f"unknown drive {drive!r}")
    threshold = wall - wall // 2 if centred else wall
    return -(-threshold // gain)


def expectations(drive: str = DRIVE, centred: bool = False) -> Json:
    """The pins before the runs for the named drive (the README's derivation
    and criteria), every entry with its source in `derivations`; `centred`
    gives the same pins with the probe's first Link at half the wall
    (`centred_step`, record 955: the column decided at the paper's close).
    The shipped register is `expectations()`; `expectations(AXIS_DRIVE)`
    reproduces the pins the registered runs were read under. The lamp
    worlds' pins are the line drive's under either argument (their momenta
    were derived under it on 2026-09-21)."""
    a = EMISSION * LABEL_MAGNITUDE * FLOW_CONSTANT / (2 * math.pi)
    if drive == LINE_DRIVE:
        drive_note = (
            "the line drive, the law's drive of a body since 2026-09-22 (BEAM_LAW note 17 as amended, "
            "note 49; the model owner's record 972): the pace 64 n / (64 S + 110 n) on a heading, "
            "n = p / (Q m); the circle 64 n^2 = A (64 S + 110 n)"
        )
    else:
        drive_note = (
            "the per-axis drive of history (BEAM_LAW note 17 as it ran until 2026-09-22, `step_axis`, "
            "the world key `per_axis_drive`): the pace n / (S + n) per axis; the circle n^2 / (S + n) = A "
            "(the registered runs of 2026-09-19 to 2026-09-21)"
        )
    found: Json = {
        "format": EXPECTATIONS_FORMAT,
        "derivations": {
            "fan": f"declared: every primitive in-plane direction (a, b, 0) with 0 < a^2 + b^2 <= {FAN_RADIUS}^2, {len(FAN)} directions, one shell every {int(1 / RATE)} intervals",
            "emission": f"the fan's directions x the release rate, q = {len(FAN)} / {int(1 / RATE)} = {EMISSION:.0f} units per interval (DERIVATIONS_BEAM 3, the flux q)",
            "label_magnitude": "the fan's mean |u_d| / Q off unit_label (BEAM_LAW section 2, note 23)",
            "circle_constant": "A = q L C / (2 pi), the mean inward push per unit of content and radius (README.md, the derivation; C = 1 taken, series C's 1.00 +- 0.10)",
            "drive": "declared: " + drive_note,
            "orbit_n": "the real root of n x pace(n) = A under the drive and the nearest whole, the declared momentum Q x whole per unit of content (the grain of the push: whole labels of Q per arriving ray)",
            "pace": "the drive's pace at the whole n",
            "period": "the analytic circle's T = 2 pi r / v at the pace (the same v at every r on the plane, T proportional to r); the bracket 15 percent (the criteria: C = 1.00 +- 0.10 and the drive's anisotropy); T is a step record, GAMEBOARD, a diagnostic and not a pin (records 562 and 564)",
            "ratio": "T(24)^2 / T(12)^2 = 4 +- 15 percent (k = 2, the plane; Kepler's k = 3 would give 8)",
            "closed": "GAMEBOARD: at the first tick at which the angle about the source reaches 2 pi the probe is within one Link of its start on each axis with its momentum's y component of the initial sign; the mean radius over the first orbit r +- 1; the drift per orbit within 1 Link",
            "constant": "the mean inward push per interval over the orbit divided by m q L / (2 pi r_mean) gives C, expected 1.00 +- 0.15 (the probe's own reads, DETECTOR; the division by the host's interval count a GameBoard rate)",
            "first_link": "GAMEBOARD: the interval of the probe's first Link from rest, ceil(W / (p Q)) under the line drive with W = Q^2 S m + p T_D (half the wall under centred_step), ceil((Q S m + p) / p) under the per-axis drive",
            "lamp_worlds": "the S = 32 worlds with the probe a lamp of its own light and the source its detector (README.md, the lamp worlds; DERIVATIONS_BEAM 21.5 row 58): the circle under the line drive at n = 10, the period within the continuum map's 9 percent, the mean radius, the precession per radial period, the ratio T(24) / T(12) = 2.00 +- 0.15, the clicks at the source",
        },
        "drive": drive,
        "centred": centred,
        "fan_directions": len(FAN),
        "emission": EMISSION,
        "label_magnitude": LABEL_MAGNITUDE,
        "flow_constant": FLOW_CONSTANT,
        "circle_constant": a,
        "period_margin": PERIOD_MARGIN,
        "ratio": {"pin": 4.0, "bracket": [4.0 * (1 - PERIOD_MARGIN), 4.0 * (1 + PERIOD_MARGIN)]},
        "worlds": {},
    }
    for width in WIDTHS:
        real, whole = orbit_momentum(width, drive)
        v = pace(whole, width, drive)
        for radius in RADII:
            t = expected_period(width, radius, drive)
            found["worlds"][f"s{width}_r{radius}"] = {
                "width": width,
                "radius": radius,
                "content": 1,
                "orbit_n_real": real,
                "orbit_n": whole,
                "momentum": whole * LABEL_SCALE,
                "pace": v,
                "period": {"pin": t, "bracket": [t * (1 - PERIOD_MARGIN), t * (1 + PERIOD_MARGIN)]},
                "mean_radius": {"pin": radius, "bracket": [radius - 1, radius + 1]},
                "first_link": first_link(whole, width, 1, drive, centred),
                "ticks": TICKS,
            }
    real_b, whole_b = orbit_momentum(LAMP_WIDTH, LINE_DRIVE)
    v_b = pace(whole_b, LAMP_WIDTH, LINE_DRIVE)
    for radius in RADII:
        t = 2 * math.pi * radius / v_b
        found["worlds"][f"s{LAMP_WIDTH}_r{radius}_lamp"] = {
            "width": LAMP_WIDTH,
            "radius": radius,
            "content": LAMP_PROBE_CONTENT,
            "drive": LINE_DRIVE,
            "orbit_n_real": real_b,
            "orbit_n": whole_b,
            "momentum": whole_b * LABEL_SCALE * LAMP_PROBE_CONTENT,
            "pace": v_b,
            "period": {
                "pin": t,
                "bracket": [t * (1 - LAMP_PERIOD_MARGIN), t * (1 + LAMP_PERIOD_MARGIN)],
            },
            "first_link": first_link(whole_b, LAMP_WIDTH, LAMP_PROBE_CONTENT, LINE_DRIVE, centred),
            "ticks": TICKS,
        }
    return found


def lamp_world(radius: int) -> Json:
    """Series D's S = 32 world at `radius` with the probe a lamp of its own
    light and the source its detector (the comment at LAMP_WIDTH)."""
    document = world(LAMP_WIDTH, radius)
    _, n = orbit_momentum_form_b(LAMP_WIDTH)
    document["model_id"] = f"rays-orbit-s{LAMP_WIDTH}-r{radius}-lamp-plane-v1"
    document["families"] = [
        {"name": "m", "quantum": 0, "charge": 0, "phase": False},
        {"name": LAMP_PROBE_FAMILY, "quantum": 0, "charge": 0, "phase": False},
    ]
    source, probe = document["measured"]  # type: ignore[misc]
    source["table"] = {LAMP_PROBE_FAMILY: "measure"}
    probe["family"] = LAMP_PROBE_FAMILY
    probe["amount"] = LAMP_PROBE_CONTENT
    probe["momentum"] = [0, n * LABEL_SCALE * LAMP_PROBE_CONTENT, 0]
    probe["directions"] = [list(v) for v in FAN]
    document["detectors"] = [
        {"name": "source", "positions": [list(CENTRE)], "threshold": 1, "reading": "beam"}
    ]
    return document


def world(width: int, radius: int, drive: str = DRIVE) -> Json:
    _, n = orbit_momentum(width, drive)
    return {
        "law": "beam",
        "model_id": f"rays-orbit-s{width}-r{radius}-plane-v1",
        "shape": list(SHAPE),
        "boundary": dict(BOUNDARY),
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": [1, RELEASE_D],
        "suspension": 0,
        "width": width,
        "directions": [list(v) for v in DECLARED],
        "families": [{"name": "m", "quantum": 0, "charge": 0, "phase": False}],
        "measured": [
            {
                "position": list(CENTRE),
                "family": "m",
                "amount": SOURCE,
                "phase": 0,
                "fixed": True,
                "directions": [list(v) for v in FAN],
            },
            {
                "position": [CENTRE[0] + radius, CENTRE[1], CENTRE[2]],
                "family": "m",
                "amount": 1,
                "phase": 0,
                "fixed": False,
                # In label units: n units of the probe's content, Q each.
                "momentum": [0, n * LABEL_SCALE, 0],
            },
        ],
    }


def worlds() -> dict[str, Json]:
    made = {f"s{width}_r{radius}": world(width, radius) for width in WIDTHS for radius in RADII}
    for radius in RADII:
        made[f"s{LAMP_WIDTH}_r{radius}_lamp"] = lamp_world(radius)
    return made


def main() -> None:
    print(
        f"fan: {len(FAN)} directions ({len(DECLARED)} declared), q = {EMISSION:.2f} per interval, "
        f"L = {LABEL_MAGNITUDE:.4f} (the mean |u_d| / Q)"
    )
    for width in WIDTHS:
        real, whole = orbit_momentum(width)
        speed = pace(whole, width)
        periods = ", ".join(f"T({r}) = {expected_period(width, r):.0f}" for r in RADII)
        print(
            f"S = {width}, the {DRIVE} drive: n = {real:.3f} -> p = {whole} ({whole * LABEL_SCALE} label units), "
            f"v = {speed:.4f} on a heading, {periods}"
        )
    real_b, whole_b = orbit_momentum_form_b(LAMP_WIDTH)
    pace_b = form_b_pace(whole_b, LAMP_WIDTH)
    print(
        f"the lamp worlds at S = {LAMP_WIDTH} under the line drive: n = {real_b:.3f} -> {whole_b} "
        f"({whole_b * LABEL_SCALE} label units per unit of content, {whole_b * LABEL_SCALE * LAMP_PROBE_CONTENT} for the probe of content {LAMP_PROBE_CONTENT}), "
        f"the pace on a heading {pace_b:.4f} Links per interval, "
        + ", ".join(f"T({r}) = {2 * math.pi * r / pace_b:.0f}" for r in RADII)
    )
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        document = families_by_definition(document, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(HERE.parents[2]))
    register = HERE / "expectations.json"
    register.write_text(
        json.dumps(carry_replicated(register, expectations()), indent=1) + "\n", encoding="utf-8"
    )
    print(register.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
