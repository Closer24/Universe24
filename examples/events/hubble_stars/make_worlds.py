"""Write the nine worlds of series G2, the Hubble diagram with stars behind
the detector, under the Beam Law, in space, and the expectations before the
runs (`expectations.json`).

The model owner's question (2026-09-20): "Can you run on a separate machine
a test of whether dark energy is needed? What comes out of an experiment
in our model? A star has to be placed there." Six worlds of one base
(README.md here; the drafted register entry is in the README until the
owner says to register it).

The throw. An open cube of SIDE^3 Nodes with the centre c. Twenty-four
STARS, each of the catalog's kind (docs/ENTITY_CATALOG.md, "the sun, a star
of content M"): ONE measured event of a paid family of its own (`s_px1` ..
`s_mz4`, so that the detector's record tells the star by the family of the
light) that holds a mass (`held` {"mass": M}, the free family `mass`, the
universal gravity column with the sign minus) and is a lamp (`lamp` of rate
1 unit per self-creation on the heading toward the centre, each unit
costing the star E = h f = `quantum` x turn = 1 content and carrying the
star's clock phase at birth). Its gravity is the mass rows released at
every self-creation on the two headings of its axis (M x `release` per
direction: F rows); its light is the lamp's row toward the detector. The
stars are thrown from the centre along the six axes with a HUBBLE-FLOW
initial condition: the star at the initial distance r_0 has the speed v =
r_0 / T_0 Links per interval, T_0 = THROW_AGE intervals, as if every star
left the centre at the time -T_0 (r_0 = 3 .. 26 Links, one integer per
star, dealt round-robin over the six axes in Port order, so no star ever
overtakes another on its axis); the momentum is the label p = Q S M_total v
/ (1 - v) (BEAM_LAW section 3 step 5; M_total the light plus the mass held,
the content the step rule reads). The star's clock turns ONE step of the
circle of N per self-creation (K = M_total: the turn `by_clock(age,
content, K)` = 1 while the light spent, at most TICKS units, is small
against the mass).

The detector. ONE measured event of the paid family `detector` (it releases
nothing) at the centre declared as the detector `centre` of one Node
reading `wave`, whose table entry for every star's light is `{"rule":
"measure", "reads": "age"}`: the click record of every arriving row carries
the age moment of the row (its flight time) and the `record` line the
pointer's phase (the star's clock at birth); the family names the star.
The mass rows reach the detector too and go on (`read` on a fixed event:
the push taken by nothing) to the other side of the line.

The gravity between the stars. On an axis a beam does not dilute (series
C), so the rows of every star reach every other star on its line, the
opposite chain included (they pass the detector): the model's own gravity
here is the gravity of a line, a constant pull per row whatever the
distance, toward the emitter (kappa = -M_A: a free ray pushes its reader
toward its emitter). The net pull on a star is therefore (the rows from the
stars nearer the centre and from the whole opposite chain) minus (the rows
from the stars farther out on its own chain): inward, growing with the
rank, the one-dimensional "mass inside" (Newton's shell theorem holds in
one dimension). Every star's speed changes by (1 - v)^2 x amount / S per
row whatever its mass (the equivalence principle), so what "mass" means
here is the rows a star releases, F per direction per self-creation.

Three crowds and three clocks, nine worlds:

| World | The mass a star holds | F | The `mass` entry at a star | The clocks count | `suspension` |
| --- | --- | --- | --- | --- | --- |
| `coasting_<clock>` | 2^22 | 64 | `pass` (the coupling off: the rows pass, the clock counts them, nothing pushes) | nothing / the presence / the age moment | 0 / [1, 2^16] / [1, 2^23] |
| `gravity_<clock>` | 2^22 | 64 | `read` (the push taken, the rows go on) | the same | the same |
| `double_<clock>` | 2^23 | 128 | `read` | the same | the same |

The light of every other star passes a star (`pass`: the inner stars are
transparent to the outer stars' light; the clock counts it all the same).
The clock (series E's pair): every star's clock owes `by_clock(age,
counted, d)` intervals after each self-creation, `counted` the presence of
the rays of other numbers at its Node in the `scalar` worlds and their age
moment in the `age` worlds (every entry `reads: "age"`); a star that owes
neither releases nor steps that interval, so its clock slows its light and
its motion alike. Every star on a line sees the same rows pass (a beam does
not dilute), so the presence is nearly uniform over the stars and the age
moment grows with the star's distance from the others.

    python examples/events/hubble_stars/make_worlds.py            # the worlds and expectations.json
    python examples/events/hubble_stars/make_worlds.py --record   # also record/<world>.json reading `sum` (the record click) and record/expectations.json (the source rule)
    python examples/events/hubble_stars/make_worlds.py --doppler  # also doppler/<world>.json under the key `doppler`, reading `sum`, and doppler/expectations.json (the flux rule)
    python examples/events/hubble_stars/make_worlds.py --after    # derivation_after_the_runs.json only
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.game_board import PORT_HEADINGS  # noqa: E402
from event_universe.events.nature_beam import flight_table  # noqa: E402
from event_universe.events.world import HEADING_OFFSET, LAW_VALUE, Q  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the worlds' families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113): the
# twenty-four stars are one instance of `hubble_stars`; `detector` and
# `mass` (with `charge` 0) stay inline.
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

SIDE = 301
SHAPE = [SIDE, SIDE, SIDE]
CENTRE = (SIDE // 2, SIDE // 2, SIDE // 2)
N = 64
TICKS = 400
# The width of the push: a row of amount a moves a star's speed by (1 - v)^2
# a / S; 2^20 lets the crowd's rows be felt (a tenth to a third of the
# speed over the run) while one row is a grain of 1.5e-5 in v.
WIDTH = 1 << 20
# The mass a star holds and its release: F = MASS / 2^16 = 64 rows per
# direction per self-creation (128 in the double crowd). The derivation
# below at F = 16 read q = +0.05, within the grain's reach of the coasting
# form (the grain moves q by 0.07, one standard deviation); at F = 64 it
# reads q = +0.25 and at F = 128 q = +0.59, so the three crowds are told
# apart.
MASS = 1 << 22
RELEASE = [1, 1 << 16]
# The light a star carries: one unit per self-creation costs 1 content
# (the turn is 1), so TICKS units are spent of LIGHT; the clock's rate,
# content / K, falls by at most TICKS / M_total = 4e-4 over the run.
LIGHT = 1 << 12
LAMP_RATE = [1, 1]
# The Hubble flow: the star at r_0 Links has the speed r_0 / THROW_AGE
# Links per interval, as if thrown from the centre THROW_AGE intervals
# before the run.
THROW_AGE = 90
FIRST_DISTANCE = 3
STARS = 24
CHAIN = 4
# The axes in Port order: +x, -x, +y, -y, +z, -z.
AXES = ("px", "mx", "py", "my", "pz", "mz")
# The clocks' widths: the presence over 2^16, the age moment over 2^23
# (about 770 rays of presence and an age moment of about 1e5 at a star: k
# of about 0.01 either way, 0.02 in the double crowd).
# `none` (added after the first six runs read the clocks' scatter, k of 0 to
# 0.07 per star per window, as the control that isolates the throw and the
# push from the clocks: `suspension` 0, no clock counts, k = 0 exactly; the
# same brackets).
CLOCKS = {"none": 0, "scalar": [1, 1 << 16], "age": [1, 1 << 23]}
# The grain of a reader's speed, G = 2^12, a constant of the law beside Q
# (BEAM_LAW note 38, record 130): under the world key `doppler` a free body
# reads the rows arriving at its Node at the flux of their stream through
# it, its speed per axis read once per interval as G |p_a| // D_a and the
# remainder discarded; the derivation with the reading rule `flux` below
# quantises the reader's speed the same way.
SPEED_GRAIN = 1 << 12
# The crowds: the mass held (F = mass / 2^16) and whether the mass rows
# push (`read`) or pass.
CROWDS = {"coasting": (MASS, "pass"), "gravity": (MASS, "read"), "double": (2 * MASS, "read")}
WINDOWS = ((100, 200), (200, 300), (300, 400))
EXPECTATIONS_FORMAT = "hubble-stars-expectations-v1"
Json = dict[str, object]


def beam_speed() -> float:
    """The ray's speed on a heading, read off the flight table."""
    table = flight_table(((0, 0, 0), (0, 0, 0), *PORT_HEADINGS))
    heading = np.array([HEADING_OFFSET])
    period = int(table.period[HEADING_OFFSET])
    return int(table.manhattan_steps(heading, np.array([period]))[0]) / period


C = beam_speed()


def momentum(v: float, content: int) -> int:
    """The momentum p (label units) that gives the speed v (Links per
    interval) to a free measured event of content `content`: v = p / (Q S
    M + p)."""
    return round(Q * WIDTH * content * v / (1 - v))


def speed(p: int, content: int) -> float:
    return p / (Q * WIDTH * content + p)


def stars(mass: int) -> list[Json]:
    """The twenty-four stars of the design: name, axis (Port index), rank,
    initial distance r_0, speed v = r_0 / T_0, v / c, the momentum for the
    content mass + LIGHT, and the position."""
    content = mass + LIGHT
    found: list[Json] = []
    for rank in range(1, CHAIN + 1):
        for axis, name in enumerate(AXES):
            r0 = FIRST_DISTANCE + axis + 6 * (rank - 1)
            v = r0 / THROW_AGE
            p = momentum(v, content)
            port = PORT_HEADINGS[axis]
            found.append(
                {
                    "name": f"s_{name}{rank}",
                    "axis": axis,
                    "rank": rank,
                    "initial_distance": r0,
                    "speed": speed(p, content),
                    "speed_over_c": speed(p, content) / C,
                    "momentum": p,
                    "position": [CENTRE[k] + port[k] * r0 for k in range(3)],
                    "momentum_vector": [port[k] * p for k in range(3)],
                    "inward": [[-port[k] for k in range(3)]],
                    "axis_headings": [list(port), [-port[k] for k in range(3)]],
                }
            )
    return found


def world(crowd: str, clock: str, record: bool = False, doppler: bool = False) -> Json:
    """One world; with `record` the same world reading `sum` at the centre
    (the record click of amplitude-v1, docs/designs/hubble_stars/DESIGN.md
    section 2.4; since the one click of stage (vii) every lamp births
    records and the key `amplitude` is deleted, MIGRATION (vii-4), so the
    `record` worlds differ from the base worlds by the detector's reading
    alone): every unit of a star's light is born as one record of one row,
    the detector reads `sum` (the record's scope) and every reading is
    taken from the gather lines, one click per record. With `doppler`
    (which implies `record`) the same world under the key `doppler` as
    well (doppler-v1, BEAM_LAW note 38): every star reads the
    mass rows arriving at its Node at the flux of their stream through it,
    the grain flux form at G = 2^12; the light and the detector unchanged."""
    record = record or doppler
    mass, mass_rule = CROWDS[crowd]
    content = mass + LIGHT
    thrown = stars(mass)
    names = [str(s["name"]) for s in thrown]
    families: list[Json] = [
        {"name": "detector", "quantum": 1},
        {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
        *({"name": name, "quantum": 1} for name in names),
    ]

    def entry(rule: str, reads_age: bool) -> Json:
        return {"rule": rule, "reads": "age"} if reads_age else {"rule": rule}

    measured: list[Json] = [
        {
            "position": list(CENTRE),
            "family": "detector",
            "amount": 1,
            "fixed": True,
            "table": {name: entry("measure", True) for name in names},
        }
    ]
    for star in thrown:
        # A world declares only what differs from the generated table
        # (BEAM_LAW section 2): `read` is a free family's default, so the
        # mass entry is written only for `pass` or with `reads: "age"`.
        table: Json = {}
        if mass_rule != "read" or clock == "age":
            table["mass"] = entry(mass_rule, clock == "age")
        for other in names:
            if other != star["name"]:
                table[other] = entry("pass", clock == "age")
        measured.append(
            {
                "position": star["position"],
                "family": star["name"],
                "amount": LIGHT,
                "phase": 0,
                "momentum": star["momentum_vector"],
                "held": {"mass": mass},
                "directions": star["axis_headings"],
                "lamp": {"rate": LAMP_RATE, "wheel": [1, N], "directions": star["inward"]},
                "table": table,
            }
        )
    document: Json = {
        "law": LAW_VALUE,
        "model_id": (
            f"rays-hubble-stars-{'record-' if record else ''}{'doppler-' if doppler else ''}"
            f"{crowd}-{clock}-space-v1"
        ),
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
            {
                "name": "centre",
                "positions": [list(CENTRE)],
                "threshold": 1,
                "reading": "sum" if record else "wave",
            }
        ],
    }
    if doppler:
        document["doppler"] = True
    return document


def referenced(document: Json) -> Json:
    """The world as shipped: its families instances of the definitions of
    `entities/families.json` (`detector_material`, `mass` and the stars as
    one instance of `hubble_stars`; the loader expands it to the inline
    world, key by key). The worlds of `record/` and `doppler/` stay inline:
    a reference climbs one level only, and every world of the record click
    is deferred to the third pull request of record 113."""
    return families_by_definition(document, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)


def worlds() -> dict[str, Json]:
    return {f"{crowd}_{clock}": referenced(world(crowd, clock)) for crowd in CROWDS for clock in CLOCKS}


def record_worlds() -> dict[str, Json]:
    """The same nine worlds under the record click, written to `record/`."""
    return {f"{crowd}_{clock}": world(crowd, clock, record=True) for crowd in CROWDS for clock in CLOCKS}


def doppler_worlds() -> dict[str, Json]:
    """The same nine worlds under the record click and the key `doppler`
    (the reading's weight at the relative speed), written to `doppler/`."""
    return {
        f"{crowd}_{clock}": world(crowd, clock, doppler=True) for crowd in CROWDS for clock in CLOCKS
    }


# -- The derivation before the runs -------------------------------------------


def load_tool():
    """The readings tool's fits (`fit_points`, `Point`), so that the
    expectation is fitted by the same functions that read the runs."""
    path = ROOT / "tools" / "hubble_stars_readings.py"
    spec = importlib.util.spec_from_file_location("hubble_stars_readings_tool", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules["hubble_stars_readings_tool"] = module
    spec.loader.exec_module(module)
    return module


def quantised(speed: float) -> float:
    """A speed read at the grain G: the whole part of G |v| over G with the
    sign of v (the engine's `w_a = G |p_a| // D_a`, BEAM_LAW note 38)."""
    return math.copysign(math.floor(SPEED_GRAIN * abs(speed)) / SPEED_GRAIN, speed)


def throw_derivation(crowd: str, reading_rule: str = "acoustic") -> dict[str, object]:
    """The continuum derivation of the throw under the crowd's push (a
    GameBoard expectation, written before the runs): on each line (an axis,
    both chains) every star releases F rows per direction per interval; a
    row of amount a passing a star moves its speed by (1 - |v|)^2 a / S
    toward the emitter; the rows of a star l reach a star j at the acoustic
    rate F (c - u_r) / (c - u_s) (u the two speeds along the row's
    heading; `reading_rule` "acoustic", the rule pinned before the runs)
    once the first row has crossed the distance between them; with the
    `reading_rule` "source" (found on the engine after the runs, README.md:
    a body reads the rows that step into its Node, and its own motion
    neither adds nor removes any, so the rate is the beam's density times
    c, F c / (c - u_s), the emitter's Doppler alone) the reader's factor
    (c - u_r) is dropped; with the `reading_rule` "flux" (the world key
    `doppler`, doppler-v1: the reader takes the arrivals at the flux of
    their stream through it, on a heading (c - u_r) / c of the rate, the
    reader's speed read at the grain 1 / G) the reader's factor is (c -
    u_r) with u_r quantised toward zero at 1 / G, the acoustic rule up to
    the grain (below 2.4e-4 in v, a bias toward 1 of the factor);
    the outward rows of a moving star are partly taken home (a star that
    steps into the Node of the row it just released, the fraction |v|,
    re-created half inward, half outward: the outward beam (1 - |v|) / (1
    - |v| / 2) of F, the inward 1 / (1 - |v| / 2)). Ignored, flagged: the
    clocks (k of about 0.01: a star that owes neither releases nor steps
    that interval, so its light and its motion slow alike), the flight
    table's grain, the step rule's grain under a changing momentum. The
    coasting crowd's rows pass: v constant, the exact Milne form. Per star
    at each window's centre: the expected z (the acoustic Doppler of v at
    emission), tau (the light-travel time) and |p(end)| / p(0)."""
    mass, rule = CROWDS[crowd]
    F = mass * RELEASE[0] / RELEASE[1] if rule == "read" else 0.0
    design = stars(mass)
    by_line: dict[int, list[int]] = {}
    for index, star in enumerate(design):
        by_line.setdefault(int(star["axis"]) // 2, []).append(index)
    positions = [
        float(star["initial_distance"]) * (1 if int(star["axis"]) % 2 == 0 else -1) for star in design
    ]
    speeds = [float(star["speed"]) * (1 if int(star["axis"]) % 2 == 0 else -1) for star in design]
    history_x = [[x] for x in positions]
    history_v = [[v] for v in speeds]
    initial_distance = [abs(x) for x in positions]
    for t in range(1, TICKS + 1):
        new_v = list(speeds)
        for line in by_line.values():
            for j in line:
                push = 0.0
                for l_ in line:
                    if l_ == j:
                        continue
                    # The first row of l reaches j after their initial
                    # separation over c (the retardation of the start).
                    if t < abs(positions[l_] - positions[j]) / C:
                        continue
                    s = 1.0 if positions[j] > positions[l_] else -1.0
                    u_s, u_r = speeds[l_] * s, speeds[j] * s
                    outward = (positions[l_] > 0) == (s > 0)
                    vl = abs(speeds[l_])
                    g = (1 - vl) / (1 - vl / 2) if outward else 1 / (1 - vl / 2)
                    if reading_rule == "acoustic":
                        reader = C - u_r
                    elif reading_rule == "flux":
                        reader = C - quantised(u_r)
                    else:
                        reader = C
                    rate = F * g * reader / (C - u_s)
                    push -= s * rate * (1 - abs(speeds[j])) ** 2 / WIDTH
                new_v[j] = speeds[j] + push
        speeds = new_v
        positions = [x + v for x, v in zip(positions, speeds, strict=True)]
        for j in range(len(design)):
            history_x[j].append(positions[j])
            history_v[j].append(speeds[j])

    def at(history: list[float], t: float) -> float:
        i = min(int(t), TICKS - 1)
        f = t - i
        return history[i] * (1 - f) + history[i + 1] * f

    windows: dict[str, list[dict[str, float]]] = {}
    for lo, hi in WINDOWS:
        t0 = (lo + hi) / 2.0
        points: list[dict[str, float]] = []
        for j, star in enumerate(design):
            # The emission time t_e with t_e + |x(t_e)| / c = t_0, by bisection.
            a, b = 0.0, t0
            for _ in range(60):
                m = (a + b) / 2
                if m + abs(at(history_x[j], m)) / C < t0:
                    a = m
                else:
                    b = m
            te = (a + b) / 2
            points.append(
                {
                    "name": str(star["name"]),
                    "z": abs(at(history_v[j], te)) / C,
                    "tau": t0 - te,
                    "d": abs(at(history_x[j], te)),
                    "momentum_ratio": (abs(speeds[j]) / (1 - abs(speeds[j])))
                    / (abs(history_v[j][0]) / (1 - abs(history_v[j][0]))),
                }
            )
        windows[f"{lo}-{hi}"] = points
    return {
        "rows_per_direction": F,
        "windows": windows,
        "initial_distance": initial_distance,
    }


def fits_of(tool, points: list[dict[str, float]], t0: float) -> dict[str, object]:
    fit = tool.fit_points(
        [
            tool.Point(p["name"], 0, p["z"], 0.0, p["z"], p["tau"], p["d"], 1 / (1 + p["z"]), p["z"])
            for p in points
        ],
        t0,
    )
    return {
        "q_fit": fit.q_fit,
        "h_fit": fit.h_fit,
        "hubble_time": fit.h_fit * (t0 + THROW_AGE),
        "rms_fit": fit.rms_fit,
        "q_effective": fit.q_effective,
        "best": {label: list(value) for label, value in fit.best.items()},
        "nearest": fit.nearest,
        "farthest": fit.farthest,
    }


def expectations(reading_rule: str = "acoustic") -> Json:
    """The expectations before the runs: the design table, the derived
    points and fits per crowd and window, and the brackets the tool
    judges the late window against. `reading_rule` "acoustic" is the first
    registration's derivation (the Doppler on the emitter and the reader);
    "source" the derivation under the law's reading rule found on the
    engine (a body's own motion does not Doppler what it reads: the
    emitter's factor alone), pinned for the run under the record click and
    the step drive of 2026-09-20 (`record/expectations.json`), where the
    continuum derivation's flagged omission of the step rule's grain is
    no longer an omission (the drive follows the momentum's history) and
    the burst of the step rule is pinned at 1 Link per interval; "flux"
    the derivation under the world key `doppler` (doppler-v1, the flux at
    the grain: the reader's factor (c - u_r) restored at the grain 1 / G),
    pinned for the run under the key and the signed drive
    (`doppler/expectations.json`, docs/designs/hubble_stars/EXPECTATION_2.md).

    The brackets, with their reasons: (i) the reading's formula 1 + z =
    (1 + k)(1 + v / c) within 2 % and the luminosity 1 / (1 + z) within
    5 % (the tool's constants; the grain of a rate over a hundred
    intervals); (ii) the coasting crowd reads q within +- 0.25 of what the
    exact Milne form reads at the window's taus by the same fit (the
    grain of the digital step, 0.003 in z and one interval in tau, moves
    q by 0.07, one standard deviation over sixty draws on the exact form;
    the bracket is three and a half of that) and H (t_0 + T_0) within
    10 % of 1; (iii) the gravity and double crowds read q within the
    derived q +- the larger of 0.2 (the grain's three standard
    deviations) and half the derived deceleration q_derived - q_exact
    (the derivation's own uncertainty: the clocks, the recycling, the
    grain), and the three crowds in the order q_coasting < q_gravity <
    q_double with each gap above 0.1; their nearest of the three forms
    q = +0.5 or q = 0 and the farthest q = -0.55; (iv) |p(end)| / p(0) on
    the GameBoard within 1 +- 0.01 in the coasting crowd (the light's
    recoil and the grain) and, in the pushing crowds, within the derived
    spread widened by half of itself each way: the derivation says the
    inner stars of the fast lines GAIN speed (the rows of the receding
    opposite chain arrive at the acoustic rate (c - v_j) / (c + v_l),
    weaker than the rows of the slowly receding outer stars of the own
    chain, and the outward beam of a moving star is partly taken home),
    the one-dimensional, Doppler-weighted gravity of this world; (v) the
    stars' clocks k within 0 .. 0.05 (the design's 0.01 to 0.02 with a
    factor of two and a half); (vi) what is observed today, q = -0.55,
    expected NOT the nearest in every world."""
    tool = load_tool()
    c = C
    design = stars(MASS)
    found: Json = {
        "format": EXPECTATIONS_FORMAT,
        "reading_rule": reading_rule,
        "c": c,
        "throw_age": THROW_AGE,
        "ticks": TICKS,
        "windows": [list(w) for w in WINDOWS],
        "registered_window": [300, 400],
        "stars": [
            {
                k: star[k]
                for k in (
                    "name",
                    "axis",
                    "rank",
                    "initial_distance",
                    "speed",
                    "speed_over_c",
                    "momentum",
                )
            }
            for star in design
        ],
        "crowds": {},
    }
    exact_by_window: dict[str, dict[str, object]] = {}
    for lo, hi in WINDOWS:
        t0 = (lo + hi) / 2.0
        exact = tool.exact_points(
            [(str(s["name"]), float(s["speed"]), float(s["initial_distance"])) for s in design],
            t0,
            c,
            THROW_AGE,
        )
        exact_by_window[f"{lo}-{hi}"] = fits_of(
            tool, [{"name": p.name, "z": p.z, "tau": p.tau, "d": p.d} for p in exact], t0
        )
    found["exact_coasting_form"] = exact_by_window
    q_exact = float(exact_by_window["300-400"]["q_fit"])
    if reading_rule in ("source", "flux"):
        # The step drive (BEAM_LAW note 17 as amended, 2026-09-20): a body
        # steps at most one Link per interval by construction, so the
        # longest burst of the step rule over any window is 1 (GameBoard).
        found["step_burst_max"] = 1
    for crowd in CROWDS:
        derivation = throw_derivation(crowd, reading_rule)
        fits = {
            key: fits_of(tool, points, (int(key.split("-")[0]) + int(key.split("-")[1])) / 2.0)
            for key, points in derivation["windows"].items()
        }
        late = derivation["windows"]["300-400"]
        ratios = [float(p["momentum_ratio"]) for p in late]
        q_derived = float(fits["300-400"]["q_fit"])
        entry: Json = {
            "rows_per_direction": derivation["rows_per_direction"],
            "derived": derivation["windows"],
            "derived_fits": fits,
            "k_bracket": [0.0, 0.05],
        }
        if crowd == "coasting":
            entry["q_bracket"] = [q_exact - 0.25, q_exact + 0.25]
            entry["hubble_bracket"] = [0.9, 1.1]
            entry["nearest_forms"] = ["q = 0", "q = -0.55", "q = +0.5"]
            entry["momentum_ratio_bracket"] = [0.99, 1.01]
            entry["note"] = (
                "the three forms with H free differ by less than the grain at z <= 0.5 (series G's "
                "follow-up), so the nearest form is not pinned in the coasting crowd; q of the free fit "
                "and H (t_0 + T_0) are"
            )
        else:
            deceleration = q_derived - q_exact
            half = max(0.2, 0.5 * deceleration)
            entry["q_bracket"] = [q_derived - half, q_derived + half]
            entry["hubble_bracket"] = [
                float(fits["300-400"]["hubble_time"]) * 0.9,
                float(fits["300-400"]["hubble_time"]) * 1.1,
            ]
            entry["nearest_forms"] = ["q = +0.5", "q = 0"]
            entry["farthest_form"] = "q = -0.55"
            entry["momentum_ratio_bracket"] = [
                max(0.0, 1.0 - 1.5 * (1.0 - min(ratios))),
                1.0 + 1.5 * max(0.0, max(ratios) - 1.0),
            ]
        found["crowds"][crowd] = entry
    found["ordering"] = {"crowds": ["coasting", "gravity", "double"], "minimum_gap": 0.1}
    return found


def derivation_after_the_runs() -> Json:
    """The derivation with the reading rule found on the engine after the
    runs (`reading_rule` "source"): not pinned, written beside the pinned
    expectations as `derivation_after_the_runs.json` for the README's
    comparison; the brackets of `expectations.json` are not moved."""
    tool = load_tool()
    found: Json = {
        "format": "hubble-stars-derivation-after-the-runs-v1",
        "reading_rule": "source",
        "crowds": {},
    }
    for crowd in CROWDS:
        derivation = throw_derivation(crowd, "source")
        fits = {
            key: fits_of(tool, points, (int(key.split("-")[0]) + int(key.split("-")[1])) / 2.0)
            for key, points in derivation["windows"].items()
        }
        found["crowds"][crowd] = {
            "rows_per_direction": derivation["rows_per_direction"],
            "derived": derivation["windows"],
            "derived_fits": fits,
        }
    return found


def main() -> None:
    if "--after" in sys.argv[1:]:
        after = derivation_after_the_runs()
        (HERE / "derivation_after_the_runs.json").write_text(
            json.dumps(after, indent=1) + "\n", encoding="utf-8"
        )
        print((HERE / "derivation_after_the_runs.json").relative_to(ROOT))
        for crowd, entry in after["crowds"].items():
            fit = entry["derived_fits"]["300-400"]
            ratios = [p["momentum_ratio"] for p in entry["derived"]["300-400"]]
            print(
                f"{crowd} (the source rule): derived at t_0 = 350: q = {fit['q_fit']:+.3f}, H (t_0 + T_0) = "
                f"{fit['hubble_time']:.4f}, the nearest form {fit['nearest']}; |p(end)| / p(0) from "
                f"{min(ratios):.4f} to {max(ratios):.4f}: "
                + ", ".join(
                    f"{p['name']} {p['momentum_ratio']:.3f}" for p in entry["derived"]["300-400"]
                )
            )
        return
    print(f"c = {C:.5f} Links per interval on a heading (the flight table); T_0 = {THROW_AGE} intervals")
    print(
        "| star | axis | rank | r_0 | v (Links per interval) | v / c | p (mass 2^20) | p (mass 2^21) |"
    )
    print("| --- | --- | --- | --- | --- | --- | --- | --- |")
    for star, double in zip(stars(MASS), stars(2 * MASS), strict=True):
        print(
            f"| {star['name']} | {AXES[int(star['axis'])]} | {star['rank']} | {star['initial_distance']} | "
            f"{float(star['speed']):.5f} | {float(star['speed_over_c']):.4f} | {star['momentum']} | "
            f"{double['momentum']} |"
        )
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    if "--record" in sys.argv[1:]:
        # The record-click worlds (reading `sum`; without the deleted key
        # `amplitude` since the one click) are written on request.
        (HERE / "record").mkdir(exist_ok=True)
        for name, document in record_worlds().items():
            path = HERE / "record" / f"{name}.json"
            path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
            print(path.relative_to(ROOT))
        pinned = expectations("source")
        (HERE / "record" / "expectations.json").write_text(
            json.dumps(pinned, indent=1) + "\n", encoding="utf-8"
        )
        print((HERE / "record" / "expectations.json").relative_to(ROOT))
        for crowd, entry in pinned["crowds"].items():
            fit = entry["derived_fits"]["300-400"]
            ratios = [p["momentum_ratio"] for p in entry["derived"]["300-400"]]
            print(
                f"record/{crowd} (the source rule, pinned): derived at t_0 = 350: q = {fit['q_fit']:+.3f}, "
                f"H (t_0 + T_0) = {fit['hubble_time']:.4f}, the nearest form {fit['nearest']}, the farthest "
                f"{fit['farthest']}; |p(end)| / p(0) from {min(ratios):.4f} to {max(ratios):.4f}; brackets: q "
                f"{entry['q_bracket'][0]:+.3f} .. {entry['q_bracket'][1]:+.3f}, H (t_0 + T_0) "
                f"{entry['hubble_bracket'][0]:.3f} .. {entry['hubble_bracket'][1]:.3f}, |p(end)| / p(0) "
                f"{entry['momentum_ratio_bracket'][0]:.3f} .. {entry['momentum_ratio_bracket'][1]:.3f}"
            )
    if "--doppler" in sys.argv[1:]:
        # The worlds under the key `doppler` (reading `sum`): written on
        # request; the base engine before doppler-v1 refuses the key.
        (HERE / "doppler").mkdir(exist_ok=True)
        for name, document in doppler_worlds().items():
            path = HERE / "doppler" / f"{name}.json"
            path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
            print(path.relative_to(ROOT))
        pinned = expectations("flux")
        (HERE / "doppler" / "expectations.json").write_text(
            json.dumps(pinned, indent=1) + "\n", encoding="utf-8"
        )
        print((HERE / "doppler" / "expectations.json").relative_to(ROOT))
        for crowd, entry in pinned["crowds"].items():
            fit = entry["derived_fits"]["300-400"]
            ratios = [p["momentum_ratio"] for p in entry["derived"]["300-400"]]
            print(
                f"doppler/{crowd} (the flux rule, pinned): derived at t_0 = 350: q = {fit['q_fit']:+.3f}, "
                f"H (t_0 + T_0) = {fit['hubble_time']:.4f}, the nearest form {fit['nearest']}, the farthest "
                f"{fit['farthest']}; |p(end)| / p(0) from {min(ratios):.4f} to {max(ratios):.4f}; brackets: q "
                f"{entry['q_bracket'][0]:+.3f} .. {entry['q_bracket'][1]:+.3f}, H (t_0 + T_0) "
                f"{entry['hubble_bracket'][0]:.3f} .. {entry['hubble_bracket'][1]:.3f}, |p(end)| / p(0) "
                f"{entry['momentum_ratio_bracket'][0]:.3f} .. {entry['momentum_ratio_bracket'][1]:.3f}"
            )
    expected = expectations()
    (HERE / "expectations.json").write_text(json.dumps(expected, indent=1) + "\n", encoding="utf-8")
    print((HERE / "expectations.json").relative_to(ROOT))
    for key, fit in expected["exact_coasting_form"].items():
        print(
            f"the exact coasting form at the window {key}: q = {fit['q_fit']:+.3f}, H (t_0 + T_0) = "
            f"{fit['hubble_time']:.4f}, rms {fit['rms_fit']:.5f}, q_eff {fit['q_effective']:+.3f}, "
            f"the nearest form {fit['nearest']}, the farthest {fit['farthest']}"
        )
    for crowd, entry in expected["crowds"].items():
        fit = entry["derived_fits"]["300-400"]
        late = entry["derived"]["300-400"]
        ratios = [p["momentum_ratio"] for p in late]
        print(
            f"{crowd}: F = {entry['rows_per_direction']:g} rows per direction; derived at t_0 = 350: q = "
            f"{fit['q_fit']:+.3f}, H (t_0 + T_0) = {fit['hubble_time']:.4f}, the nearest form {fit['nearest']}, "
            f"the farthest {fit['farthest']}; |p(end)| / p(0) from {min(ratios):.4f} to {max(ratios):.4f}; "
            f"brackets: q {entry['q_bracket'][0]:+.3f} .. {entry['q_bracket'][1]:+.3f}, H (t_0 + T_0) "
            f"{entry['hubble_bracket'][0]:.3f} .. {entry['hubble_bracket'][1]:.3f}, |p(end)| / p(0) "
            f"{entry['momentum_ratio_bracket'][0]:.3f} .. {entry['momentum_ratio_bracket'][1]:.3f}"
        )


if __name__ == "__main__":
    main()
