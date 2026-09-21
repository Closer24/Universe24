"""Write the worlds of the entity catalog: one small world per external
thing the law can place on the GameBoard today (the model owner's decision
of 2026-09-20, Highlights 5.4, "the catalog of the entities"; the catalog
itself is docs/ENTITY_CATALOG.md, the definitions layer
docs/ENTITY_DEFINITIONS.md).

These are placements, not experiments: each world parses, runs a few dozen
intervals headless with the books balanced, and shows what a detector or a
clock reads of the thing placed; no number is registered here (the register,
docs/EXPERIMENTS.md, tests things on them later). Every family declares its
`quantum`, every detector its `reading`, and a measured event declares only
the table entries that differ from the ones its families' keys give.

- `sun_planet.json`: a star, a planet and a screen on the plane. The star
  is a composite of two measured events at adjacent Nodes, since a measured
  event has one family, each a body on a set of three Nodes along y
  (`span` [1, 3, 1]: an emitter on a set, its releases apportioned whole
  over its Nodes by its age): its mass (a free family, content 2^16,
  fixed, releasing one shell of a 120-direction in-plane fan every SHELL
  intervals: gravity, read as a push) and its lamp (a paid family,
  releasing light on a fan of nine directions toward the screen). The
  planet is a free body of content 2^10 on a set of 3 x 3 Nodes (`span`)
  at radius R with the tangential momentum of a circular orbit derived
  below from the engine's own flight lines, re-releasing the light it
  receives on the four in-plane headings (the planet shines by reflected
  light; its content keeps gravity's push, proportional to the reader's
  content, far above the light's, which is the unit's label alone). The
  screen is one detector set of SCREEN_HEIGHT Nodes near the +x face
  reading `wave`.
- `neutron_star.json`: a bound set of eight neutrons at the adjacent Nodes
  of a 2 x 2 x 2 cube, free (not `fixed`), each of content 2^26 releasing
  on the six headings, held at one Link by the gravity column alone (each
  pulls its neighbours and a step onto an occupied Node is refused; the
  recorded defect of the contact, the momentum growing at the refused step,
  stays within the bound for this run), and six probes of content 1 on the
  axes at radius R_STAR that `pass` the rays and count them on their
  clocks, the -x probe counting the age moment (`reads: "age"`).
- `lamp_mirror_screen.json`: an optical bench on the plane: a laser (a lamp
  with one direction and a phase window, so it releases in pulses), a
  mirror (`rerelease` on one direction, the beam turned by a right angle),
  a wall with one slit (`measure`, the slit `rerelease` on a fan of eleven
  directions) and a screen read as pixels (one `wave` detector per Node).
- `clock_near_mass.json`: a mass of content 2^12 at the centre of a cube
  releasing one ray per direction per interval on the 122 primitive
  directions with |a| + |b| + |c| <= 4, and two clocks, bodies of content
  1 on sets of 3 x 3 x 3 Nodes at two radii that `pass` the rays: the
  count each owes off its clock (`waited` against `age`) is the reading
  of a clock beside a mass.

    python examples/events/catalog/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.events.world import LABEL_SCALE, LAW_VALUE  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

K = 1 << 22
N = 64
Q = LABEL_SCALE
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
IN_PLANE = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]
Json = dict[str, object]
Vector = tuple[int, int, int]

# -- sun_planet ---------------------------------------------------------------
PLANE_SIDE = 41
PLANE_CENTRE = (20, 20, 0)
STAR = 1 << 16
# One shell of the fan every SHELL intervals: by_clock(age, STAR, STAR x SHELL).
SHELL = 10
FAN_RADIUS = 8
PLANET_RADIUS = 8
PLANET = 1 << 10
PLANET_SPAN = (3, 3, 1)
# The star's two events are each a body on a set of three Nodes along y
# (the model owner, 2026-09-20: an emitter on a set carries its width on
# the world's side as a detector does; its releases are apportioned whole
# over its Nodes by its age, and which Node released is not information
# the world has).
STAR_SPAN = (1, 3, 1)
# The width S of the push (the world key `width`): a body on nine Nodes
# reads about nine times one Node's flux at the same content, so a large
# width keeps the derived orbit slow enough for a visible arc in TICKS_SUN
# intervals (about 0.2 Links per interval).
WIDTH = 512
LAMP = 1 << 25
LAMP_FAN = [
    [1, 0, 0],
    [1, 1, 0],
    [1, -1, 0],
    [2, 1, 0],
    [2, -1, 0],
    [3, 1, 0],
    [3, -1, 0],
    [4, 1, 0],
    [4, -1, 0],
]
SCREEN_X = 38
SCREEN_HEIGHT = 25
TICKS_SUN = 50

# -- neutron_star -------------------------------------------------------------
CUBE_SIDE = 25
CUBE_CORNER = (12, 12, 12)
NEUTRON = 1 << 26
# Each neutron releases NEUTRON / NEUTRON_RELEASE units per heading per
# self-creation: 2^18, a label of 2^24 per row, a push of 2^50 on a
# neighbour per row, within 2^62 - 1 over the run.
NEUTRON_RELEASE = 1 << 8
R_STAR = 8
TICKS_STAR = 40

# -- lamp_mirror_screen -------------------------------------------------------
BENCH_SIDE = 21
LASER = (3, 10, 0)
LASER_RATE = [4, 1]
MIRROR = (11, 10, 0)
WALL_Y = 13
WALL_X = (5, 17)
SLIT = (11, 13, 0)
BENCH_SCREEN_Y = 17
BENCH_SCREEN_X = (1, 19)
LASER_WINDOW = 16
TICKS_BENCH = 50

# -- clock_near_mass ----------------------------------------------------------
CLOCK_SIDE = 21
CLOCK_CENTRE = (10, 10, 10)
MASS = 1 << 12
FAN_MANHATTAN = 4
CLOCK_RADII = (5, 9)
CLOCK_SPAN = (3, 3, 3)
CLOCK_SUSPENSION = [1, 4]
TICKS_CLOCK = 50


def primitive(v: Vector) -> bool:
    return math.gcd(math.gcd(abs(v[0]), abs(v[1])), abs(v[2])) == 1


def plane_fan(radius: int) -> list[Vector]:
    """Every primitive in-plane direction (a, b, 0) with 0 < a^2 + b^2 <=
    radius^2, ordered by angle from +x (the orbit series' fan)."""
    found = [
        (a, b, 0)
        for a in range(-radius, radius + 1)
        for b in range(-radius, radius + 1)
        if (a or b) and a * a + b * b <= radius * radius and primitive((a, b, 0))
    ]
    found.sort(key=lambda v: math.atan2(v[1], v[0]) % (2 * math.pi))
    return found


def space_fan(manhattan: int) -> list[Vector]:
    """Every primitive direction (a, b, c) with 0 < |a| + |b| + |c| <=
    manhattan, in a fixed order (the redshift series' fan)."""
    found = [
        (a, b, c)
        for a in range(-manhattan, manhattan + 1)
        for b in range(-manhattan, manhattan + 1)
        for c in range(-manhattan, manhattan + 1)
        if (a or b or c) and abs(a) + abs(b) + abs(c) <= manhattan and primitive((a, b, c))
    ]
    found.sort()
    return found


def declared(fan: list[Vector]) -> list[list[int]]:
    """The fan's directions beyond the six headings, the world's table."""
    return [list(v) for v in fan if v not in HEADINGS]


def entries_per_node(directions: list[Vector], reach: int) -> dict[Vector, int]:
    """The entries per shell each Node within `reach` of the source receives
    from the fan's digital lines, walked along the engine's own flight
    lines (`direction_flight`: S_1 unit steps per period of the Bresenham line
    of every direction) until they pass `reach`."""
    table = direction_flight(tuple(directions))
    count: dict[Vector, int] = {}
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


def body_flux(count: dict[Vector, int], radius: int, span: Vector) -> float:
    """E_body(r): the entries per shell the planet's set of Nodes receives
    together, averaged over the ring of the plane at `radius` (the Nodes
    with r - 0.5 < |x| <= r + 0.5)."""
    ring = [
        (x, y)
        for x in range(-radius - 1, radius + 2)
        for y in range(-radius - 1, radius + 2)
        if radius - 0.5 < math.sqrt(x * x + y * y) <= radius + 0.5
    ]
    half = ((span[0] - 1) // 2, (span[1] - 1) // 2)
    total = sum(
        count.get((x + dx, y + dy, 0), 0)
        for x, y in ring
        for dx in range(-half[0], half[0] + 1)
        for dy in range(-half[1], half[1] + 1)
    )
    return total / len(ring)


def circular_orbit(flux: float, radius: int, width: int, content: int) -> tuple[int, float]:
    """The circular orbit at `radius` for the width S of the push, for a
    body of content M about an uncharged source (the coupling -M_A x V_B):
    the push per interval is M x Q x E_body / SHELL, the speed v = p / (Q S
    M + p), and p v / r = push gives, with p = n M, the real root n of
    n^2 / (Q S + n) = A with A = Q x E_body x r / SHELL, independent of M
    (the equivalence principle); the whole p (label units) and the speed
    it gives."""
    a = Q * flux * radius / SHELL
    reach = Q * width
    n = (a + math.sqrt(a * a + 4 * reach * a)) / 2
    p = max(1, round(n * content))
    return p, p / (reach * content + p)


def sun_planet() -> tuple[Json, dict[str, float]]:
    fan = plane_fan(FAN_RADIUS)
    count = entries_per_node(fan, PLANET_RADIUS + 2)
    flux = body_flux(count, PLANET_RADIUS, PLANET_SPAN)
    momentum, speed = circular_orbit(flux, PLANET_RADIUS, WIDTH, PLANET)
    cx, cy, cz = PLANE_CENTRE
    screen_rows = range(cy - SCREEN_HEIGHT // 2, cy + SCREEN_HEIGHT // 2 + 1)
    measured: list[Json] = [
        {
            "position": [cx, cy, cz],
            "family": "mass",
            "amount": STAR,
            "fixed": True,
            "span": list(STAR_SPAN),
            "directions": [list(v) for v in fan],
        },
        {
            "position": [cx + 1, cy, cz],
            "family": "light",
            "amount": LAMP,
            "phase": 0,
            "fixed": True,
            "span": list(STAR_SPAN),
            "lamp": {"rate": [1, 1], "wheel": [1, N], "directions": LAMP_FAN},
        },
        {
            "position": [cx + PLANET_RADIUS, cy, cz],
            "family": "mass",
            "amount": PLANET,
            "fixed": False,
            "momentum": [0, momentum, 0],
            "span": list(PLANET_SPAN),
            "directions": IN_PLANE,
            "table": {"light": "rerelease"},
        },
    ]
    for y in screen_rows:
        measured.append({"position": [SCREEN_X, y, cz], "family": "screen", "amount": 1, "fixed": True})
    world: Json = {
        "law": LAW_VALUE,
        "model_id": "rays-catalog-sun-planet-v1",
        "shape": [PLANE_SIDE, PLANE_SIDE, 1],
        "boundary": {"z": "periodic"},
        "ticks": TICKS_SUN,
        "K": K,
        "N": N,
        "release": [1, STAR * SHELL],
        "suspension": 0,
        "width": WIDTH,
        "directions": declared(fan),
        "families": [
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
            {"name": "light", "quantum": 1},
            {"name": "screen", "quantum": 1},
        ],
        "measured": measured,
        "detectors": [
            {
                "name": "screen",
                "positions": [[SCREEN_X, y, cz] for y in screen_rows],
                "threshold": 1,
                "reading": "wave",
            }
        ],
    }
    reading = {
        "fan": len(fan),
        "flux": flux,
        "momentum": momentum,
        "speed": speed,
        "period": 2 * math.pi * PLANET_RADIUS / speed,
    }
    return world, reading


def neutron_star() -> Json:
    x0, y0, z0 = CUBE_CORNER
    measured: list[Json] = [
        {"position": [x0 + dx, y0 + dy, z0 + dz], "family": "neutron", "amount": NEUTRON, "fixed": False}
        for dx in (0, 1)
        for dy in (0, 1)
        for dz in (0, 1)
    ]
    # The star's centre is between Nodes (the cube's corner plus a half):
    # a probe on a +axis sits R_STAR Links from the corner, on a -axis
    # R_STAR - 1, so that the six are symmetric about the centre.
    axes = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]
    for ax, ay, az in axes:
        offset = [R_STAR * a if a > 0 else (1 - R_STAR) * -a for a in (ax, ay, az)]
        probe: Json = {
            "position": [x0 + offset[0], y0 + offset[1], z0 + offset[2]],
            "family": "probe",
            "amount": 1,
            "fixed": True,
            "table": {"neutron": "pass"},
        }
        if (ax, ay, az) == (-1, 0, 0):
            probe["table"] = {"neutron": {"rule": "pass", "reads": "age"}}
        measured.append(probe)
    return {
        "law": LAW_VALUE,
        "model_id": "rays-catalog-neutron-star-v1",
        "shape": [CUBE_SIDE, CUBE_SIDE, CUBE_SIDE],
        "boundary": "open",
        "ticks": TICKS_STAR,
        "K": K,
        "N": N,
        "release": [1, NEUTRON_RELEASE],
        "suspension": [1, K],
        "families": [
            {"name": "neutron", "quantum": 0, "charge": 0, "phase": False},
            {"name": "probe", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
    }


def slit_fan() -> list[list[int]]:
    """The slit's fan: every primitive in-plane direction (a, b, 0) with
    b >= 1 and |a| + b <= 4, forward of the wall."""
    return [
        [a, b, 0]
        for b in range(1, 5)
        for a in range(-4, 5)
        if abs(a) + b <= 4 and math.gcd(abs(a), b) == 1
    ]


def lamp_mirror_screen() -> Json:
    fan = slit_fan()
    measured: list[Json] = [
        {
            "position": list(LASER),
            "family": "light",
            "amount": LAMP,
            "phase": 0,
            "fixed": True,
            "lamp": {
                "rate": LASER_RATE,
                "wheel": [1, N],
                "directions": [[1, 0, 0]],
                "phase_window": LASER_WINDOW,
            },
        },
        {
            "position": list(MIRROR),
            "family": "apparatus",
            "amount": 1,
            "fixed": True,
            "directions": [[0, 1, 0]],
            "table": {"light": "rerelease"},
        },
    ]
    for x in range(WALL_X[0], WALL_X[1] + 1):
        entry: Json = {"position": [x, WALL_Y, 0], "family": "apparatus", "amount": 1, "fixed": True}
        if (x, WALL_Y, 0) == SLIT:
            entry["directions"] = fan
            entry["table"] = {"light": "rerelease"}
        measured.append(entry)
    detectors: list[Json] = []
    for x in range(BENCH_SCREEN_X[0], BENCH_SCREEN_X[1] + 1):
        measured.append(
            {"position": [x, BENCH_SCREEN_Y, 0], "family": "apparatus", "amount": 1, "fixed": True}
        )
        detectors.append(
            {
                "name": f"screen_{x}",
                "positions": [[x, BENCH_SCREEN_Y, 0]],
                "threshold": 1,
                "reading": "wave",
            }
        )
    return {
        "law": LAW_VALUE,
        "model_id": "rays-catalog-lamp-mirror-screen-v1",
        "shape": [BENCH_SIDE, BENCH_SIDE, 1],
        "boundary": {"z": "periodic"},
        "ticks": TICKS_BENCH,
        "K": K,
        "N": N,
        "release": [1, 128],
        "suspension": 0,
        "directions": [v for v in fan if tuple(v) not in HEADINGS],
        "families": [{"name": "light", "quantum": 1}, {"name": "apparatus", "quantum": 1}],
        "measured": measured,
        "detectors": detectors,
    }


def clock_near_mass() -> Json:
    fan = space_fan(FAN_MANHATTAN)
    cx, cy, cz = CLOCK_CENTRE
    measured: list[Json] = [
        {
            "position": [cx, cy, cz],
            "family": "mass",
            "amount": MASS,
            "fixed": True,
            "directions": [list(v) for v in fan],
        }
    ]
    for radius in CLOCK_RADII:
        measured.append(
            {
                "position": [cx + radius, cy, cz],
                "family": "probe",
                "amount": 1,
                "fixed": True,
                "span": list(CLOCK_SPAN),
                "table": {"mass": "pass"},
            }
        )
    return {
        "law": LAW_VALUE,
        "model_id": "rays-catalog-clock-near-mass-v1",
        "shape": [CLOCK_SIDE, CLOCK_SIDE, CLOCK_SIDE],
        "boundary": "open",
        "ticks": TICKS_CLOCK,
        "K": K,
        "N": N,
        "release": [1, MASS],
        "suspension": CLOCK_SUSPENSION,
        "directions": declared(fan),
        "families": [
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
            {"name": "probe", "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
    }


def worlds() -> dict[str, Json]:
    """The four documents by name, as written: each takes its families from
    the shipped definitions (the migration of 2026-09-20; `sun_planet` and
    `lamp_mirror_screen` since the one click of `amplitude-v1` landed)."""
    sun, _ = sun_planet()
    return {
        "sun_planet": families_by_definition(sun, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE),
        "neutron_star": families_by_definition(neutron_star(), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE),
        "lamp_mirror_screen": families_by_definition(
            lamp_mirror_screen(), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE
        ),
        "clock_near_mass": families_by_definition(
            clock_near_mass(), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE
        ),
    }


def render(document: Json) -> str:
    """The document indented by two, with every short list of integers (a
    position, a direction, a pair) on one line."""
    text = json.dumps(document, indent=2)
    return (
        re.sub(
            r"\[\s+(-?\d+(?:,\s+-?\d+){0,2})\s+\]",
            lambda m: "[" + re.sub(r"\s+", " ", m.group(1)) + "]",
            text,
        )
        + "\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    _, reading = sun_planet()
    print(
        f"sun_planet: a fan of {reading['fan']:.0f} directions, one shell per {SHELL} intervals; "
        f"E_body {reading['flux']:.3f} entries per shell on the planet's set at r = {PLANET_RADIUS}; "
        f"width {WIDTH}; p = {reading['momentum']:.0f} (label units), "
        f"v = {reading['speed']:.3f} Links per interval, T = {reading['period']:.0f} intervals "
        "(a GameBoard reading of the design; whether the orbit closes is the register's question)"
    )
    for name, document in worlds().items():
        path = args.out / f"{name}.json"
        path.write_text(render(document), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
