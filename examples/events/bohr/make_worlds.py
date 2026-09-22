"""Write the worlds of series H, "Bohr's lines behind the detector", under
the Beam Law in space: a fixed proton, an electron that is a body on
a set of three Nodes and turns its phase by its momentum at every Link it
steps (the model owner's decision of 2026-09-20 on Bohr, "go, and put it as
parameters outside the GameBoard like the age"; BEAM_LAW section 10, note 30),
and the open faces of the GameBoard as the `wave` detectors that receive what
the electron releases.

The atom (README.md here; the physicist's series F design of 2026-09-20 with
the charge per unit of content): two free families, `p` (the proton, content
M_p = 1836, rho_p = [1, 1]) and `e` (the electron, rho_e = -RATIO), the
push on the electron from a proton ray of amount 1 being M_e (rho_e rho_p -
1) x label = -(1 + RATIO) M_e x Q along the ray's unit vector, inward. The
proton is a fixed measured event at the centre of an open cube of SIDE^3
Nodes releasing one ray per direction of a shell of 2616 primitive
directions (FAN_LOW <= |D|^2 <= FAN_HIGH, the physicist's fan) every SHELL
intervals (`release` [1, M_p x SHELL]). The electron is a free measured
event of content M_e = M_p at (c + r, c, c) with the tangential momentum
[0, p, 0], `span` [1, 1, 3] (the body on the three Nodes z = c - 1, c,
c + 1: it reads the flux of three planes of the fan, the grain of one Node
averaged, the physicist's fix), `phase_by_momentum` true with the world's
`action` h, its table the default (`read`: the push taken, the rays go on)
and its `directions` the four in-plane headings +-X, +-Y, on which it
releases one ray per direction every SHELL intervals with its phase (the
same `release` key: its content equals the proton's so that both release
at the world's one rate; with the proton fixed the ratio of the contents
enters nothing, the push per unit of content and the step per unit of
content cancelling). Its rays carry its phase and no content (a free
release costs nothing: the orbit does not decay) and leave through the
four side faces, whose face detectors record the square of the coherent
pointer of what leaves each interval and whose `click` lines carry every
ray's phase, Node and tick: the far-face `wave` detector of the owner's
design, with no measured event added to the GameBoard. `suspension` 0 (the
clock's count is not read; the push alone moves the electron), K 2^30 (the
clock's own turn 0 within a run), N 64.

The derivation, written before the runs (README.md): the flux the fan's
lines deliver to the body at radius r on the ring of the plane z = c is
E_body(r) entries per shell, the sum over its three Nodes of the entries
per Node counted from the engine's own flight lines (`direction_flight`, the
same Bresenham lines the walk takes), averaged around the ring; the push
per interval is F = (1 + RATIO) M_e Q E_body(r) / SHELL. Under the line
drive, the law's drive of a body since 2026-09-22 (the model owner's word,
record 972; docs/designs/drive_b/DEFAULT.md; BEAM_LAW note 17 as amended,
note 49), a body on a heading gains p Q on its accumulator per interval
against the wall Q^2 S M_e + p T_D (T_D = isqrt(3 Q^2) = 110), so with the
width S its pace is v = p Q / (Q^2 S M_e + p T_D) = n / (Q S + n T_D / Q),
and a circular orbit needs p v / r = F, so with n = p / M_e, A = (1 +
RATIO) Q E_body(r) r / SHELL and the term PACE_TERM = T_D / Q = 1.71875

    n^2 / (Q S + PACE_TERM n) = A,
    n = (PACE_TERM A + sqrt(PACE_TERM^2 A^2 + 4 Q S A)) / 2,  T = 2 pi r / v.

The per-axis drive of history (note 17 as it ran until that day, the world
key `per_axis_drive`, the drive the registered runs of 2026-09-20 were
read under) has the pace v = n / (Q S + n) and the circle n^2 / (Q S + n)
= A, n = (A + sqrt(A^2 + 4 Q S A)) / 2; `orbit(flux, r, S, AXIS_DRIVE)`
and `expectations(AXIS_DRIVE)` reproduce its pins (p(8) = 338411520, h =
5414584320). The width S = 45120 is the registered one, chosen so that v
= SPEED on the orbit of REFERENCE_RADIUS under that drive
(`width_for_speed`), and kept under the law (DEFAULT.md section (b)).
The turn by momentum turns the phase by |p_axis| N / h per Link stepped
on an axis, so over one orbit of a circle of radius r stepped on the
GameBoard the phase turns by (N / h) x sum over the Links of |p_axis| = (N /
h) x 4 p r (the Manhattan weighting of the path: 4 r against the circle's
2 pi r), and closes on itself when

    4 p(r) r = j h,  j whole:

de Broglie's condition in the GameBoard's metric. With p proportional to
1 / sqrt(r) under a 1 / r^2 push the closing radii are proportional to
j^2, Bohr's ladder. The action is fixed so that j = 2 exactly on the
reference orbit, h = 16 p(REFERENCE_RADIUS) (4 p r / j with r = 8, j = 2),
and the radii of RADII are read against it: j(r) = 4 p(r) r / h, whole at a
closing radius and half-way between at a non-closing one. The expectation:
the coherent record of the electron's rays at a face grows as the square of
the turns where the phase closes (the same phase at the same place every
turn) and stays bounded, at most linear, where it does not; the ratio of
the closing radii about j^2. Every derived number is a GAMEBOARD reading
(the host's view of the mechanism); the coherent records are DETECTOR
readings (the only kind reality has). The pins are written to
`expectations.json` (`expectations(drive, centred)`, the register's form of
`orbit_lamp/`), every entry with its source in `derivations`: the drive,
the width, the action, and per radius the flux, n, p, the pace, the period
with its 15 percent bracket, j and its kind, the lumps per orbit, the
GameBoard's side, the intervals, and the tick of the electron's first Link
(a GAMEBOARD number: ceil(W / (p Q)) with W the wall, or half the wall
under `centred_step`, the column the model owner decides at the paper's
close, record 955).

    python examples/events/bohr/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.register_map import carry_replicated  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

K = 1 << 30
N = 64
Q = 64
PROTON = 1836
ELECTRON = 1836
# The electric / gravity ratio of the atom: -rho_e rho_p = RATIO.
RATIO = 15
# One shell of the fan every SHELL intervals: by_clock(age, M, M x SHELL).
SHELL = 10
FAN_LOW, FAN_HIGH = 1016, 1032
# The electron's set: three Nodes along z, the planes z = c - 1, c, c + 1.
SPAN = (1, 1, 3)
# The radii of the electron's orbits, the reference among them: j = 2 at
# the reference radius fixes the action. The fan's flux on the ring is not
# smooth at r >= 13 (the lines of a finite fan), so j = 3 falls between
# the GameBoard radii 15 and 16 (2.87 and 3.25 derived): both are run.
RADII = (2, 4, 6, 8, 12, 15, 16)
REFERENCE_RADIUS = 8
REFERENCE_J = 2
# The speed aimed at on the reference orbit (Links per interval).
SPEED = 0.06
# The two drives an orbit is derived under (docs/designs/drive_b/DEFAULT.md
# section (c)): the line drive, the law's drive of a body since 2026-09-22
# (the pace n / (Q S + n T_D / Q) on a heading), and the per-axis drive of
# history (the pace n / (Q S + n); the world key `per_axis_drive`), the
# drive the registered runs of 2026-09-20 were read under.
LINE_DRIVE = "line"
AXIS_DRIVE = "axis"
DRIVE = LINE_DRIVE
T_D_AXIS = math.isqrt(3 * Q * Q)  # 110, the axis direction's period constant
PACE_TERM = T_D_AXIS / Q  # 110 / 64, the line drive's second wall term per unit of n
# The registered width: v = SPEED at r = 8 under the per-axis drive of
# history (width_for_speed), kept under the law (DEFAULT.md section (b)).
WIDTH = 45120
PERIOD_MARGIN = 0.15
EXPECTATIONS_FORMAT = "bohr-expectations-v1"
# The turns of the orbit a run covers, and the least run.
TURNS = 5
LEAST_TICKS = 3000
# The GameBoard per radius: the orbit plus a margin for its eccentricity.
MARGIN = 14
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
IN_PLANE = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]
Json = dict[str, object]


def primitive(v: tuple[int, int, int]) -> bool:
    return math.gcd(math.gcd(abs(v[0]), abs(v[1])), abs(v[2])) == 1


def fan(low: int, high: int) -> list[tuple[int, int, int]]:
    """Every primitive direction (a, b, c) with low <= a^2 + b^2 + c^2 <=
    high, in a fixed order."""
    found = []
    bound = math.isqrt(high)
    for a in range(-bound, bound + 1):
        for b in range(-bound, bound + 1):
            for c in range(-bound, bound + 1):
                n = a * a + b * b + c * c
                if n and low <= n <= high and primitive((a, b, c)):
                    found.append((a, b, c))
    found.sort()
    return found


def entries_per_node(
    directions: list[tuple[int, int, int]], reach: int
) -> dict[tuple[int, int, int], int]:
    """The entries per shell each Node within `reach` of the source receives
    from the fan's digital lines: the engine's own flight lines
    (`direction_flight`: S_1 unit steps per period of the Bresenham line of
    every direction), walked from the source until they pass `reach`."""
    table = direction_flight(tuple(directions))
    count: dict[tuple[int, int, int], int] = {}
    for index in range(len(directions)):
        steps = int(table.manhattan[index])
        line = table.lines[index, :steps]
        x = [0, 0, 0]
        k = 0
        while True:
            step = line[k % steps]
            x = [x[i] + int(step[i]) for i in range(3)]
            k += 1
            if math.sqrt(x[0] * x[0] + x[1] * x[1] + x[2] * x[2]) > reach + 1:
                break
            node = (x[0], x[1], x[2])
            count[node] = count.get(node, 0) + 1
    return count


def body_flux(count: dict[tuple[int, int, int], int], radius: int) -> float:
    """E_body(r): the entries per shell the body's three Nodes (z = -1, 0,
    1) receive together, averaged over the ring of the plane z = 0 at
    `radius` (the Nodes with r - 0.5 < |x| <= r + 0.5)."""
    ring = [
        (x, y)
        for x in range(-radius - 1, radius + 2)
        for y in range(-radius - 1, radius + 2)
        if radius - 0.5 < math.sqrt(x * x + y * y) <= radius + 0.5
    ]
    total = sum(count.get((x, y, z), 0) for x, y in ring for z in (-1, 0, 1))
    return total / len(ring)


def pace(n: float, width: int, drive: str = DRIVE) -> float:
    """The pace of the electron at n = p / M_e, in Links per interval: the
    line drive's n / (Q S + n T_D / Q) on a heading (the law's) or the
    per-axis drive of history's n / (Q S + n)."""
    if drive == LINE_DRIVE:
        return n / (Q * width + PACE_TERM * n)
    if drive == AXIS_DRIVE:
        return n / (Q * width + n)
    raise ValueError(f"unknown drive {drive!r}")


def orbit(flux: float, radius: int, width: int, drive: str = DRIVE) -> dict[str, float]:
    """The circular orbit at `radius` for the width S under the named
    drive: the real root n of n^2 / (Q S + PACE_TERM n) = A (the line drive)
    or n^2 / (Q S + n) = A (the per-axis drive of history), A = (1 + RATIO)
    Q E_body(r) r / SHELL, the whole momentum p = M_e n (label units), the
    speed, the period, the kicks."""
    a = (1 + RATIO) * Q * flux * radius / SHELL
    reach = Q * width
    if drive == LINE_DRIVE:
        n = (PACE_TERM * a + math.sqrt((PACE_TERM * a) ** 2 + 4 * reach * a)) / 2
    elif drive == AXIS_DRIVE:
        n = (a + math.sqrt(a * a + 4 * reach * a)) / 2
    else:
        raise ValueError(f"unknown drive {drive!r}")
    p = max(1, round(n * ELECTRON))
    speed = pace(p / ELECTRON, width, drive)
    period = 2 * math.pi * radius / speed
    return {
        "flux": flux,
        "n": n,
        "p": p,
        "speed": speed,
        "period": period,
        "lumps_per_orbit": period / SHELL,
        "degrees_per_lump": math.degrees(flux * (1 + RATIO) * Q / n),
    }


def width_for_speed(flux: float, radius: int, speed: float) -> int:
    """The width at which the reference orbit's derived speed is `speed`
    under the per-axis drive of history (the registered width's derivation
    of 2026-09-20): from v = n / (Q S + n) and n^2 / (Q S + n) = A, Q S = A
    (1 - v) / v^2."""
    a = (1 + RATIO) * Q * flux * radius / SHELL
    return max(1, round(a * (1 - speed) / (speed * speed) / Q))


def side_for(radius: int) -> int:
    return 2 * (radius + MARGIN) + 1


def first_link(p: int, width: int, drive: str = DRIVE, centred: bool = False) -> int:
    """The interval of the electron's first Link from rest on its heading, a
    GAMEBOARD number: under the line drive the accumulator gains p Q per
    interval against the wall W = Q^2 S M_e + p T_D (`by_line`), so the
    first Link is at ceil(W / (p Q)), or ceil((W - W // 2) / (p Q)) under
    `centred_step` (the threshold half the wall); under the per-axis drive
    of history the accumulator gains p against Q S M_e + p (`by_drive`)."""
    if drive == LINE_DRIVE:
        wall = Q * Q * width * ELECTRON + p * T_D_AXIS
        gain = p * Q
    elif drive == AXIS_DRIVE:
        wall = Q * width * ELECTRON + p
        gain = p
    else:
        raise ValueError(f"unknown drive {drive!r}")
    threshold = wall - wall // 2 if centred else wall
    return -(-threshold // gain)


def derive(
    drive: str = DRIVE,
) -> tuple[list[tuple[int, int, int]], int, int, dict[int, dict[str, float]]]:
    """The fan, the width, the action and the orbit per radius under the
    named drive (GAMEBOARD readings of the design, before the runs)."""
    directions = fan(FAN_LOW, FAN_HIGH)
    count = entries_per_node(directions, max(RADII) + 2)
    fluxes = {radius: body_flux(count, radius) for radius in RADII}
    width = WIDTH
    # The registered width's own derivation (v = SPEED at r = 8 under the
    # per-axis drive of history) reproduced from the same fan.
    assert width_for_speed(fluxes[REFERENCE_RADIUS], REFERENCE_RADIUS, SPEED) == width
    orbits = {radius: orbit(fluxes[radius], radius, width, drive) for radius in RADII}
    action = 4 * int(orbits[REFERENCE_RADIUS]["p"]) * REFERENCE_RADIUS // REFERENCE_J
    for radius, reading in orbits.items():
        reading["j"] = 4 * reading["p"] * radius / action
        reading["ticks"] = max(LEAST_TICKS, int(math.ceil(TURNS * reading["period"] / 100.0)) * 100)
    return directions, width, action, orbits


def closing(j: float) -> bool:
    """The design's kind of a radius: closing when j is whole within 0.1."""
    return abs(j - round(j)) < 0.1


def expectations(drive: str = DRIVE, centred: bool = False) -> Json:
    """The pins before the runs for the named drive (the module docstring),
    every entry with its source in `derivations`; `centred` gives the same
    pins with the electron's first Link at half the wall (`centred_step`,
    record 955: the column decided at the paper's close). The shipped
    register is `expectations()`; `expectations(AXIS_DRIVE)` reproduces the
    pins the runs of 2026-09-20 were read under."""
    directions, width, action, orbits = derive(drive)
    if drive == LINE_DRIVE:
        drive_note = (
            "the line drive, the law's drive of a body since 2026-09-22 (BEAM_LAW note 17 as amended, "
            "note 49; the model owner's record 972): the pace n / (Q S + n T_D / Q) on a heading, "
            "n = p / M_e, T_D / Q = 110 / 64; the circle n^2 / (Q S + 1.71875 n) = A"
        )
    else:
        drive_note = (
            "the per-axis drive of history (BEAM_LAW note 17 as it ran until 2026-09-22, `step_axis`, "
            "the world key `per_axis_drive`): the pace n / (Q S + n) per axis; the circle "
            "n^2 / (Q S + n) = A (the registered runs of 2026-09-20)"
        )
    found: Json = {
        "format": EXPECTATIONS_FORMAT,
        "derivations": {
            "fan": f"declared: the physicist's shell of {len(directions)} primitive directions with {FAN_LOW} <= |D|^2 <= {FAN_HIGH}, one ray per direction every {SHELL} intervals",
            "flux": "E_body(r): the entries per shell the electron's three Nodes receive on the ring of the plane z = c, counted from the engine's own flight lines and averaged around the ring (README.md, the derivation)",
            "drive": "declared: " + drive_note,
            "width": "declared: the registered width, v = 0.06 at r = 8 under the per-axis drive of history (width_for_speed), kept under the law (docs/designs/drive_b/DEFAULT.md section (b))",
            "orbit": "the circular orbit p v / r = F with F = (1 + RATIO) M_e Q E_body(r) / SHELL and A = (1 + RATIO) Q E_body(r) r / SHELL: the real root n under the drive, p = round(M_e n), the pace at the whole p, T = 2 pi r / v",
            "period": "the analytic circle's T = 2 pi r / v at the pace; the bracket 15 percent each side (the criteria, README.md); T is a step record, GAMEBOARD, a diagnostic and not a pin (the clock audit of 2026-09-22)",
            "action": f"h = 4 p(r) r / j at r = {REFERENCE_RADIUS}, j = {REFERENCE_J}: 4 p r = j h, de Broglie's condition in the GameBoard's metric (the turn by momentum sums |p_axis| over the Links stepped, 4 p r on a circle)",
            "j": "4 p(r) r / h per radius; closing when whole within 0.1, between otherwise",
            "lumps": "T / SHELL shells per orbit, each turning the momentum by (1 + RATIO) Q E_body(r) / n radians",
            "ticks": f"max({LEAST_TICKS}, {TURNS} T rounded up to a hundred): the run's intervals",
            "first_link": "GAMEBOARD: the interval of the electron's first Link from rest, ceil(W / (p Q)) under the line drive with W = Q^2 S M_e + p T_D (half the wall under centred_step), ceil((Q S M_e + p) / p) under the per-axis drive",
            "coherence": "DETECTOR: at a closing radius C(T) >= T / 2 after T >= 2 turns and the log-log slope of the cumulative coherent record near 2; between two whole j, C(T) < 2; fewer than two closed turns, no coherence reading (the criteria, README.md)",
            "return": "GAMEBOARD: closed when at the closing of the angle the electron is within r / 4 of its start",
        },
        "drive": drive,
        "centred": centred,
        "width": width,
        "action": action,
        "reference": {"radius": REFERENCE_RADIUS, "j": REFERENCE_J},
        "period_margin": PERIOD_MARGIN,
        "worlds": {},
    }
    for radius in RADII:
        reading = orbits[radius]
        t = float(reading["period"])
        p = int(reading["p"])
        found["worlds"][f"r{radius}"] = {
            "radius": radius,
            "flux": reading["flux"],
            "n": reading["n"],
            "momentum": p,
            "pace": reading["speed"],
            "period": {"pin": t, "bracket": [t * (1 - PERIOD_MARGIN), t * (1 + PERIOD_MARGIN)]},
            "j": reading["j"],
            "kind": "closing" if closing(reading["j"]) else "between",
            "lumps_per_orbit": reading["lumps_per_orbit"],
            "degrees_per_lump": reading["degrees_per_lump"],
            "side": side_for(radius),
            "ticks": int(reading["ticks"]),
            "first_link": first_link(p, width, drive, centred),
        }
    return found


def world(
    directions: list[tuple[int, int, int]],
    width: int,
    action: int,
    radius: int,
    reading: dict[str, float],
) -> Json:
    side = side_for(radius)
    centre = side // 2
    declared = [list(v) for v in directions if v not in HEADINGS]
    # The proton releases on the whole fan, named by the indices of the
    # world's table: the six headings (2 .. 7) and the declared rest.
    whole_fan = list(range(2, 8 + len(declared)))
    return {
        "law": "beam",
        "model_id": f"rays-bohr-r{radius}-space-v1",
        "shape": [side, side, side],
        "boundary": "open",
        "ticks": int(reading["ticks"]),
        "K": K,
        "N": N,
        "release": [1, PROTON * SHELL],
        "suspension": 0,
        "width": width,
        "action": action,
        "directions": declared,
        "families": [
            {"name": "p", "quantum": 0, "charge": [1, 1], "phase": False},
            {"name": "e", "quantum": 0, "charge": -RATIO, "phase": True},
        ],
        "measured": [
            {
                "position": [centre, centre, centre],
                "family": "p",
                "amount": PROTON,
                "fixed": True,
                "directions": whole_fan,
            },
            {
                "position": [centre + radius, centre, centre],
                "family": "e",
                "amount": ELECTRON,
                "phase": 0,
                "fixed": False,
                "momentum": [0, int(reading["p"]), 0],
                "span": list(SPAN),
                "phase_by_momentum": True,
                "directions": IN_PLANE,
            },
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    directions, width, action, orbits = derive()
    args.out.mkdir(parents=True, exist_ok=True)
    print(
        f"fan: {len(directions)} directions, one shell per {SHELL} intervals; width {width}; the {DRIVE} "
        f"drive; action h = {action} (j = {REFERENCE_J} at r = {REFERENCE_RADIUS}); GAMEBOARD readings of the design"
    )
    for radius in RADII:
        reading = orbits[radius]
        print(
            f"r = {radius}: E_body {reading['flux']:.3f} entries per shell, p = {reading['p']} "
            f"(n {reading['n']:.1f}), v = {reading['speed']:.4f}, T = {reading['period']:.0f}, "
            f"{reading['lumps_per_orbit']:.0f} lumps per orbit of {reading['degrees_per_lump']:.1f} degrees, "
            f"j = 4 p r / h = {reading['j']:.3f} ({'closing' if abs(reading['j'] - round(reading['j'])) < 0.1 else 'between'}), "
            f"GameBoard {side_for(radius)}^3, {reading['ticks']} intervals"
        )
    for radius in RADII:
        path = args.out / f"r{radius}.json"
        document = world(directions, width, action, radius, orbits[radius])
        document = families_by_definition(document, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)
    register = args.out / "expectations.json"
    register.write_text(
        json.dumps(carry_replicated(register, expectations()), indent=1) + "\n", encoding="utf-8"
    )
    print(register)


if __name__ == "__main__":
    main()
