"""Write the worlds of series H, "Bohr's lines behind the detector", under
the law of the ray in space: a fixed proton, an electron that is a body on
a set of three Nodes and turns its phase by its momentum at every Link it
steps (the model owner's decision of 2026-09-20 on Bohr, "go, and put it as
parameters outside the GameBoard like the age"; RAY_LAW section 10, note 30),
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
per Node counted from the engine's own flight lines (`flight_table`, the
same Bresenham lines the walk takes), averaged around the ring; the push
per interval is F = (1 + RATIO) M_e Q E_body(r) / SHELL; with the width S
the speed is v = p / (Q S M_e + p), and a circular orbit needs p v / r = F,
so with n = p / M_e and A = (1 + RATIO) Q E_body(r) r / SHELL

    n^2 / (Q S + n) = A,  n = (A + sqrt(A^2 + 4 Q S A)) / 2,  T = 2 pi r / v.

The width S is chosen so that v = SPEED on the orbit of REFERENCE_RADIUS.
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
readings (the only kind reality has).

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

from event_universe.events.nature_beam import flight_table  # noqa: E402

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
    (`flight_table`: S_1 unit steps per period of the Bresenham line of
    every direction), walked from the source until they pass `reach`."""
    table = flight_table(tuple(directions))
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


def orbit(flux: float, radius: int, width: int) -> dict[str, float]:
    """The circular orbit at `radius` for the width S: the real root n of
    n^2 / (Q S + n) = A, A = (1 + RATIO) Q E_body(r) r / SHELL, the whole
    momentum p = M_e n (label units), the speed, the period, the kicks."""
    a = (1 + RATIO) * Q * flux * radius / SHELL
    reach = Q * width
    n = (a + math.sqrt(a * a + 4 * reach * a)) / 2
    p = max(1, round(n * ELECTRON))
    speed = p / (reach * ELECTRON + p)
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
    """The width at which the reference orbit's derived speed is `speed`:
    from v = n / (Q S + n) and n^2 / (Q S + n) = A, Q S = A (1 - v) / v^2."""
    a = (1 + RATIO) * Q * flux * radius / SHELL
    return max(1, round(a * (1 - speed) / (speed * speed) / Q))


def side_for(radius: int) -> int:
    return 2 * (radius + MARGIN) + 1


def derive() -> tuple[list[tuple[int, int, int]], int, int, dict[int, dict[str, float]]]:
    """The fan, the width, the action and the orbit per radius (GAMEBOARD
    readings of the design, before the runs)."""
    directions = fan(FAN_LOW, FAN_HIGH)
    count = entries_per_node(directions, max(RADII) + 2)
    fluxes = {radius: body_flux(count, radius) for radius in RADII}
    width = width_for_speed(fluxes[REFERENCE_RADIUS], REFERENCE_RADIUS, SPEED)
    orbits = {radius: orbit(fluxes[radius], radius, width) for radius in RADII}
    action = 4 * int(orbits[REFERENCE_RADIUS]["p"]) * REFERENCE_RADIUS // REFERENCE_J
    for radius, reading in orbits.items():
        reading["j"] = 4 * reading["p"] * radius / action
        reading["ticks"] = max(LEAST_TICKS, int(math.ceil(TURNS * reading["period"] / 100.0)) * 100)
    return directions, width, action, orbits


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
        "law": "rays",
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
        f"fan: {len(directions)} directions, one shell per {SHELL} intervals; width {width}; "
        f"action h = {action} (j = {REFERENCE_J} at r = {REFERENCE_RADIUS}); GAMEBOARD readings of the design"
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
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
