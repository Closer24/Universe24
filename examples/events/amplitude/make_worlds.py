"""Write the worlds of series L, the amplitude law (`amplitude-v1`; the
model owner, 2026-09-20, Highlights 5.4, "DECIDED: `amplitude-v1` is
built"; the physicist's and the mathematician's design,
scratchpad/amplitude/DESIGN.md, sections 3.4, 7 and 14), and the
expectations pinned before the runs (`expectations.json`, every integer
the design's, from its check scripts `mz.py` and `slits_read.py`).

L1, the Mach-Zehnder interferometer and Elitzur-Vaidman (the design's
section 3.4, the acceptance tests 1, 3 and 8). A plane of 5 x 5 with z
periodic, K 2^20, N 64, `release` [0, 1], `suspension` 0, `amplitude`
true, 80 intervals. The source at (0, 0), a lamp of `light` of content
2^20 (its turn 1 phase step per self-creation for far more births than
the run holds, so the birth phase u of the record born at tick t is
t - 1: the 64 births of the ticks 1 .. 64 span the circle once and
complete by tick 76, the records born after are open at the end) releasing
one record per self-creation on +x (arm 1) and +y (arm 2, the
reflection's quarter turn 16 on the row: the source's own splitter),
two rows of amount 1 with the multiplicity 2 (one quantum on two paths).
Mirror 1 at (3, 0) re-emits +x arrivals on +y, mirror 2 at (0, 3) re-emits
+y arrivals on +x, both `rerelease` on one direction (the equal split with
one weight: no change of amplitude). The splitter at (3, 3), a `rerelease`
whose split table is selected by the arrival (`inputs`): a row arriving
along +y (arm 1) is transmitted on +y toward D2 with the weight a and
reflected on +x toward D1 with the weight b and the quarter turn 16; a row
arriving along +x (arm 2) transmitted on +x toward D1 with a and reflected
on +y toward D2 with b and 16; A = a^2 + b^2 = c^2 for the Pythagorean pair
(20, 21, 29) of the design (the shares 400/841 and 441/841; no triple is
balanced) and 2 for the balanced (1, 1) split the owner admitted. D1 at
(4, 3) and D2 at (3, 4), one-Node detectors reading `sum`.

| world | the splitter | arm 2 | `phase_per_link` | the design's counts over the 64 births |
| --- | --- | --- | --- | --- |
| `mz_equal` | (20, 21) | equal | 0 | D1 64, D2 0 (the offers 1681/1682, 1/1682) |
| `mz_half` | (20, 21) | a half turn 32 on the row | 0 | D1 0, D2 64 |
| `mz_quarter` | (20, 21) | a quarter turn 16 on the row | 0 | D1 32, D2 32 |
| `mz_balanced` | (1, 1) | equal | 0 | D1 64, D2 0 (D2's rows cancel on the lattice) |
| `mz_345` | (3, 4) | equal | 0 | D1 63, D2 1 (the rung moved: u = 63 falls in D2) |
| `mz_unequal_f0` | (20, 21) | longer by two intervals | 0 | D1 64, D2 0 (the rows accumulate in phase) |
| `mz_unequal_f8` | (20, 21) | longer by two intervals | [8, 1] | D1 32, D2 32 (a delay of two intervals at 8 steps per interval is a quarter turn) |
| `mz_unequal_f16` | (20, 21) | longer by two intervals | [16, 1] | D1 0, D2 64 |
| `ev_29` | (20, 21), arm 2 absorbed at (0, 3) | equal | 0 | absorber 32, D1 17, D2 15 |
| `ev_169` | (119, 120), arm 2 absorbed | equal | 0 | absorber 32, D1 16, D2 16 |

"Arm 2 longer by two intervals" is made on the flight table: arm 1
carries two pass-through re-emitters at (3, 1) and (3, 2), each re-born
row starting a fresh digital line whose first step is at its first
interval (m(1) = 1), so each advances arm 1 by one interval; arm 2 then
reaches the ports two intervals after arm 1, and the phase per interval of
age, carried through every re-emission, reads the delay as the design's
f x 2 (the pair form of `phase_per_link` under the key, the owner's
unification (1)). The absorber of Elitzur-Vaidman is a measured event of
`light` at (0, 3) in place of mirror 2 (the keys' rule measures the paid
arrival; a detector of one Node named `absorber`).

L2, the two slits at a low rate (the design's acceptance test 2): the
shipped world `examples/events/two_slits.json` (60 x 121, K 2^30, N 64, a
lamp at (2, 60) on five directions, the wall at x = 8 with the openings at
y = 55 and 65 re-emitting on 91 directions, the screen at x = 52 of 121
one-Node pixels) under the key, the lamp's rate [1, 1] and its content K
(one phase step per interval: the birth at tick t has u = t mod 64, the
64 births of the ticks 1 .. 64 span the circle once), the family's
`phase_per_link` the pair [8591334592, 2^30] (the shipped lamp's turn per
interval, 8 + 1400000 / 2^30, the design's frequency), the pixels reading
`sum`, and the geometry the design asks for: the wall's Nodes within 6 of
each opening freed, so that every row of the openings' fans leaves the
wall's plane (a steep direction walks along y inside the plane x = 8
before its first step in x; with the shipped wall 88 of the 182 fan rows
step into the wall beside the openings in phase and offer 4.85 of the
birth's norm 1, the design's finding), and the lamp's three rows that miss
the openings absorbed by three wall Nodes at x = 7 on their paths ((7, 58),
(7, 60), (7, 62)), since the wall Nodes they hit at x = 8 are within the
freed band and a fan row and a lamp row at one set would carry the
multiplicities 455 and 5 (refused, the design's 3.1). The wall's share of
the record is then the lamp's three rows, 3/5, and the fans' 2/5 goes to
the screen and the open faces in y, as the design states.

The expectations of L2 (`expectations.json` under `two_slits`) are the
design's own reading (`slits_read.py`) of ONE birth through the same
geometry, made by this generator before the run of the 64-birth world and
independently of the engine's layer: the reference world `slits_one` (no
key; the lamp's five rows as declared rays of amount 91, so that each
opening's re-emission on its 91 directions is one row per direction, the
rows of one birth at m = 5 x 91 = 455 and the lamp's own at m = 5; the
screen's entries reading the age) is run in-process, every click read as a
row (amount, m, phase + f x age with f the frequency, the age of a lamp
row its flight and of a fan row its flight to the opening and the intervals
since its re-emission, as the lattice turns it under the key; a face click
is the row as it stepped out, before that interval's turn), the
weight of a set |sum 32 v(p)|^2 / m in the unit (32 x 256)^2, the ladder
over the sets in the layer's order with the rungs at the nearest integer,
and the clicks per set over the 64 births u = 0 .. 63 read off the ladder
(every u falls in one cell); beside them the pixels with rows, the pixels
where two paths meet and the Pearson correlations the design registered
for the shipped geometry (0.753 with the incoherent sum, 0.38 with the
Euclidean two-source cosine, 0.963 of the 64-birth histogram with the
weights) recomputed for this geometry.

    python examples/events/amplitude/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import copy
import json
import math
from collections import OrderedDict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
N = 64
QUARTER = N // 4
HALF = N // 2
# The source's content and the clock's rate: the turn is 1 phase step per
# self-creation (content / K) for the first several hundred births.
SOURCE_CONTENT = 1 << 20
CLOCK = 1 << 20
# The last birth of the circle, tick 64, completes by tick 76 (the ports
# click 11 or 12 intervals after a birth on the flight table).
MZ_TICKS = 80
# L2: the shipped two-slit world, its openings, the freed band of the wall
# around each opening, the wall Nodes at x = 7 that absorb the lamp's
# three rows missing the openings, the frequency (the shipped lamp's turn
# per interval) and the durations.
TWO_SLITS_SOURCE = ROOT / "examples" / "events" / "two_slits.json"
OPENINGS = (55, 65)
WALL_X = 8
FREED_HALF_WIDTH = 6
LAMP_WALL_NODES = ((7, 58), (7, 60), (7, 62))
FREQUENCY = [8591334592, 1 << 30]
SLITS_TICKS = 230
SLITS_ONE_TICKS = 220
LAMP_ROWS = 5
FAN_WAYS = 91
DESIGN_UNIT = (32 * 256) ** 2
PLUS_X = [1, 0, 0]
PLUS_Y = [0, 1, 0]
PYTHAGOREAN_29 = (20, 21)
PYTHAGOREAN_169 = (119, 120)
BALANCED = (1, 1)
PYTHAGOREAN_5 = (3, 4)


def mirror(position: list[int], direction: list[int]) -> dict[str, object]:
    """A re-emitter of `light` on one direction (the equal split with one
    weight: no change of amplitude)."""
    return {
        "position": position,
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"light": "rerelease"},
        "directions": [direction],
    }


def mach_zehnder(
    name: str,
    splitter: tuple[int, int] = PYTHAGOREAN_29,
    arm_turn: int = 0,
    unequal: bool = False,
    frequency: list[int] | None = None,
    absorber: bool = False,
    ticks: int = MZ_TICKS,
) -> dict[str, object]:
    """The Mach-Zehnder world of the design's section 3.4 (the docstring's
    table): `splitter` the pair (a, b), `arm_turn` the phase added to arm
    2's row at the birth beyond the reflection's quarter turn, `unequal`
    the two pass-through re-emitters on arm 1, `frequency` the pair form
    of `phase_per_link`, `absorber` Elitzur-Vaidman's absorber in place of
    mirror 2."""
    a, b = splitter
    family: dict[str, object] = {"name": "light", "quantum": 1}
    if frequency is not None:
        family["phase_per_link"] = list(frequency)
    measured: list[dict[str, object]] = [
        {
            "position": [0, 0, 0],
            "family": "light",
            "amount": SOURCE_CONTENT,
            "fixed": True,
            "lamp": {
                "rate": [1, 1],
                "directions": [PLUS_X, PLUS_Y],
                "turns": [0, (QUARTER + arm_turn) % N],
            },
        },
        mirror([3, 0, 0], PLUS_Y),
    ]
    if absorber:
        measured.append({"position": [0, 3, 0], "family": "light", "amount": 1, "fixed": True})
    else:
        measured.append(mirror([0, 3, 0], PLUS_X))
    if unequal:
        measured.append(mirror([3, 1, 0], PLUS_Y))
        measured.append(mirror([3, 2, 0], PLUS_Y))
    measured.append(
        {
            "position": [3, 3, 0],
            "family": "light",
            "amount": 1,
            "fixed": True,
            "table": {
                "light": {
                    "rule": "rerelease",
                    "inputs": [PLUS_Y, PLUS_X],
                    "weights": [[b, a], [a, b]],
                    "turns": [[QUARTER, 0], [0, QUARTER]],
                }
            },
            "directions": [PLUS_X, PLUS_Y],
        }
    )
    measured.append({"position": [4, 3, 0], "family": "light", "amount": 1, "fixed": True})
    measured.append({"position": [3, 4, 0], "family": "light", "amount": 1, "fixed": True})
    detectors: list[dict[str, object]] = []
    if absorber:
        detectors.append({"name": "absorber", "positions": [[0, 3, 0]], "reading": "sum"})
    detectors.append({"name": "D1", "positions": [[4, 3, 0]], "reading": "sum"})
    detectors.append({"name": "D2", "positions": [[3, 4, 0]], "reading": "sum"})
    return {
        "law": "beam",
        "model_id": f"beam-amplitude-{name}-v1",
        "shape": [5, 5, 1],
        "boundary": {"z": "periodic"},
        "ticks": ticks,
        "K": CLOCK,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "amplitude": True,
        "families": [family],
        "measured": measured,
        "detectors": detectors,
    }


def mach_zehnder_worlds() -> dict[str, dict[str, object]]:
    return {
        "mz_equal": mach_zehnder("mz_equal"),
        "mz_half": mach_zehnder("mz_half", arm_turn=HALF),
        "mz_quarter": mach_zehnder("mz_quarter", arm_turn=QUARTER),
        "mz_balanced": mach_zehnder("mz_balanced", splitter=BALANCED),
        "mz_345": mach_zehnder("mz_345", splitter=PYTHAGOREAN_5),
        "mz_unequal_f0": mach_zehnder("mz_unequal_f0", unequal=True),
        "mz_unequal_f8": mach_zehnder("mz_unequal_f8", unequal=True, frequency=[8, 1]),
        "mz_unequal_f16": mach_zehnder("mz_unequal_f16", unequal=True, frequency=[16, 1]),
        "ev_29": mach_zehnder("ev_29", absorber=True),
        "ev_169": mach_zehnder("ev_169", splitter=PYTHAGOREAN_169, absorber=True),
    }


# The design's integers (mz.txt), written before any run: per world the
# offers of one record (exact fractions of the pointer unit, as the design
# states them) and the clicks over the 64 births u = 0 .. 63, in the
# layer's order of the sets.
MACH_ZEHNDER_EXPECTATIONS: dict[str, dict[str, object]] = {
    "mz_equal": {"offers": {"D1": "1681/1682", "D2": "1/1682"}, "clicks": {"D1": 64, "D2": 0}},
    "mz_half": {"offers": {"D1": "1/1682", "D2": "1681/1682"}, "clicks": {"D1": 0, "D2": 64}},
    "mz_quarter": {"offers": {"D1": "1/2", "D2": "1/2"}, "clicks": {"D1": 32, "D2": 32}},
    "mz_balanced": {"offers": {"D1": "1", "D2": "0"}, "clicks": {"D1": 64, "D2": 0}},
    "mz_345": {"offers": {"D1": "49/50", "D2": "1/50"}, "clicks": {"D1": 63, "D2": 1}},
    "mz_unequal_f0": {
        "offers": {"D1": "1681/1682", "D2": "1/1682"},
        "clicks": {"D1": 64, "D2": 0},
    },
    "mz_unequal_f8": {"offers": {"D1": "1/2", "D2": "1/2"}, "clicks": {"D1": 32, "D2": 32}},
    "mz_unequal_f16": {
        "offers": {"D1": "1/1682", "D2": "1681/1682"},
        "clicks": {"D1": 0, "D2": 64},
    },
    "ev_29": {
        "offers": {"absorber": "1/2", "D1": "441/1682", "D2": "200/841"},
        "clicks": {"absorber": 32, "D1": 17, "D2": 15},
    },
    "ev_169": {
        "offers": {"absorber": "1/2", "D1": "7200/28561", "D2": "14161/57122"},
        "clicks": {"absorber": 32, "D1": 16, "D2": 16},
    },
}


def freed_wall() -> set[tuple[int, int]]:
    """The wall Nodes (x, y) within the freed band of each opening."""
    freed = {
        (WALL_X, y)
        for opening in OPENINGS
        for y in range(opening - FREED_HALF_WIDTH, opening + FREED_HALF_WIDTH + 1)
    }
    return freed - {(WALL_X, y) for y in OPENINGS}


def two_slits_geometry() -> dict[str, object]:
    """The shipped two-slit world with the freed band and the lamp's wall
    Nodes at x = 7 (the key and the lamp untouched)."""
    world = json.loads(TWO_SLITS_SOURCE.read_text(encoding="utf-8"))
    world = copy.deepcopy(world)
    freed = freed_wall()
    world["measured"] = [
        m for m in world["measured"] if (m["position"][0], m["position"][1]) not in freed
    ]
    world["measured"].extend(
        {"position": [x, y, 0], "family": "wall", "amount": 1, "fixed": True} for x, y in LAMP_WALL_NODES
    )
    return world


def two_slits_low() -> dict[str, object]:
    """L2's world: 64 births at a low rate under the key."""
    world = two_slits_geometry()
    world["model_id"] = "beam-amplitude-slits_low-v1"
    world["ticks"] = SLITS_TICKS
    world["amplitude"] = True
    lamp = world["measured"][0]
    lamp["amount"] = world["K"]
    lamp["lamp"]["rate"] = [1, 1]
    for family in world["families"]:
        if family["name"] == "light":
            family["phase_per_link"] = FREQUENCY
    for detector in world["detectors"]:
        detector["reading"] = "sum"
    return world


def two_slits_one() -> dict[str, object]:
    """The design's reference: one birth through L2's geometry without the
    key, the lamp's five rows declared as rays of amount 91."""
    world = two_slits_geometry()
    world["model_id"] = "beam-amplitude-slits_one-v1"
    world["ticks"] = SLITS_ONE_TICKS
    lamp = world["measured"][0]
    directions = lamp["lamp"]["directions"]
    del lamp["lamp"]
    lamp["amount"] = 1
    world["in_transit"] = [
        {
            "position": list(lamp["position"]),
            "family": "light",
            "number": 1,
            "direction": list(direction),
            "amount": FAN_WAYS,
            "phase": 0,
        }
        for direction in directions
    ]
    screen_x = world["detectors"][0]["positions"][0][0]
    for m in world["measured"]:
        if m["position"][0] == screen_x:
            m["table"] = {"light": {"reads": "age"}}
    return world


def pearson(a: list[float], b: list[float]) -> float:
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    sa = math.sqrt(sum((x - ma) ** 2 for x in a))
    sb = math.sqrt(sum((y - mb) ** 2 for y in b))
    if not sa or not sb:
        return float("nan")
    return sum((x - ma) * (y - mb) for x, y in zip(a, b, strict=True)) / (sa * sb)


def ladder(weights: dict[str, Fraction], order: list[str]) -> dict[str, int]:
    """The clicks per set over u = 0 .. N - 1: the rungs
    b_k = (2 N C_k + Total) // (2 Total) at the nearest integer over the
    sets in the layer's order, each set's count the rungs' difference."""
    total = sum(weights[k] for k in order)
    cumulative = Fraction(0)
    previous = 0
    counts: dict[str, int] = {}
    for name in order:
        cumulative += weights[name]
        rung = int((2 * N * cumulative + total) // (2 * total))
        if rung > previous:
            counts[name] = rung - previous
        previous = rung
    assert previous == N
    return counts


def two_slits_reading() -> dict[str, object]:
    """The design's reading of one birth (`slits_read.py`), on the
    reference world run in-process: the weights per set, the ladder's
    clicks over the 64 births, the shares, the pixels and the Pearson
    correlations; written before the run of `slits_low`."""
    from event_universe.core.phase import phase_cosines, phase_sines
    from event_universe.events import NatureBeamSimulation, parse_nature_beam_world

    reference = two_slits_one()
    lines: list[dict[str, object]] = []
    simulation = NatureBeamSimulation(parse_nature_beam_world(reference), observer=lines.append)
    for _ in range(int(reference["ticks"])):
        simulation.step()
    assert all(store.size == 0 for store in simulation.stores), "a row of the birth is still in flight"
    order = list(NatureBeamSimulation(parse_nature_beam_world(two_slits_low())).layer.names)
    cosines, sines = phase_cosines(N), phase_sines(N)
    numerator, denominator = FREQUENCY

    def turn(age: int, tick: int) -> int:
        return (tick * numerator) // denominator - ((tick - age) * numerator) // denominator

    re_emitted = {
        int(line["measured"]): int(line["tick"]) for line in lines if line.get("event") == "rerelease"
    }
    rows: dict[str, list[tuple[int, int, int]]] = OrderedDict()
    for line in lines:
        if line.get("event") != "click":
            continue
        detector = line["detector"]
        name = str(detector) if detector is not None else f"measured:{line['measured']}"
        tick, phase = int(line["tick"]), int(line["phase"])
        if int(line["number"]) == 1:
            # A lamp row: the amount 91 stands for one unit at m = 5, its
            # age its flight from the birth at tick 0.
            rows.setdefault(name, []).append((1, LAMP_ROWS, (phase + turn(tick, tick)) % N))
        else:
            # A fan row: its flight is the lamp row's to the opening (the
            # re-emission tick, from the birth at tick 0) and its own since.
            opened = re_emitted[int(line["number"])]
            age = tick - opened
            if name.startswith("face:"):
                # A face click records the row as it stepped out, before the
                # turn of that interval (the engine's walk: the escaped rows
                # leave, the rows that stay turn).
                age, tick = age - 1, tick - 1
            rows.setdefault(name, []).append(
                (1, LAMP_ROWS * FAN_WAYS, (phase + turn(opened, opened) + turn(age, tick)) % N)
            )
    weights: dict[str, Fraction] = {}
    incoherent: dict[str, Fraction] = {}
    for name, found in rows.items():
        multiplicities = {m for _, m, _ in found}
        assert len(multiplicities) == 1, (name, multiplicities)
        m = multiplicities.pop()
        x = sum(32 * w * cosines[p] for w, _, p in found)
        y = sum(32 * w * sines[p] for w, _, p in found)
        weights[name] = Fraction(x * x + y * y, m * DESIGN_UNIT)
        incoherent[name] = Fraction(
            sum((32 * w) ** 2 * (cosines[p] ** 2 + sines[p] ** 2) for w, _, p in found),
            m * DESIGN_UNIT,
        )
    cells = [name for name in order if name in weights]
    assert set(cells) == set(weights), set(weights) - set(cells)
    clicks = ladder(weights, cells)
    total = sum(weights.values())
    screen = [name for name in cells if name.startswith("screen_")]
    pixels = [int(name.split("_")[1]) for name in screen]

    def share(prefix: str) -> Fraction:
        return sum((v for k, v in weights.items() if k.startswith(prefix)), Fraction(0)) / total

    lam = (N / 8) / math.sqrt(3)
    openings_x = WALL_X
    screen_x = int(reference["detectors"][0]["positions"][0][0])

    def cosine(y: int) -> float:
        r1 = math.hypot(screen_x - openings_x, y - OPENINGS[0])
        r2 = math.hypot(screen_x - openings_x, y - OPENINGS[1])
        return 1 + math.cos(2 * math.pi * (r1 - r2) / lam)

    height = int(reference["shape"][1])
    weight_line = [float(weights.get(f"screen_{y}", 0)) for y in range(height)]
    incoherent_line = [float(incoherent.get(f"screen_{y}", 0)) for y in range(height)]
    cosine_line = [cosine(y) for y in range(height)]
    histogram = [clicks.get(f"screen_{y}", 0) for y in range(height)]
    screen_alone = ladder(weights, screen)
    conditioned = [screen_alone.get(f"screen_{y}", 0) for y in range(height)]
    return {
        "reference": "slits_one",
        "unit": "(32 x 256)^2, the square of one row of amount 1 at multiplicity 1",
        "sets": len(cells),
        "weights": {name: str(weights[name]) for name in cells},
        "total": str(total),
        "shares": {
            "wall": str(share("measured:")),
            "screen": str(share("screen_")),
            "faces": str(share("face:")),
        },
        "clicks": clicks,
        "clicks_by_kind": {
            "wall": sum(v for k, v in clicks.items() if k.startswith("measured:")),
            "screen": sum(v for k, v in clicks.items() if k.startswith("screen_")),
            "faces": sum(v for k, v in clicks.items() if k.startswith("face:")),
        },
        "screen_alone": screen_alone,
        "pixels_with_rows": len(pixels),
        "two_path_pixels": sum(1 for name in screen if len(rows[name]) >= 2),
        "pearson": {
            "weight_incoherent": round(pearson(weight_line, incoherent_line), 3),
            "weight_cosine": round(pearson(weight_line, cosine_line), 3),
            "histogram_weight": round(pearson([float(h) for h in histogram], weight_line), 3),
            "screen_alone_weight": round(pearson([float(h) for h in conditioned], weight_line), 3),
        },
        "design_shipped_geometry": {
            "weight_crowd_record": 0.992,
            "weight_incoherent": 0.753,
            "weight_cosine": 0.381,
            "histogram_weight": 0.963,
            "pixels_with_rows": 61,
            "two_path_pixels": 27,
        },
    }


def two_slits_worlds() -> dict[str, dict[str, object]]:
    return {"slits_low": two_slits_low(), "slits_one": two_slits_one()}


def worlds() -> dict[str, dict[str, object]]:
    found = mach_zehnder_worlds()
    found.update(two_slits_worlds())
    return found


def expectations() -> dict[str, object]:
    return {
        "format": "amplitude-expectations-v1",
        "births": N,
        "mach_zehnder": MACH_ZEHNDER_EXPECTATIONS,
        "two_slits": two_slits_reading(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, world in worlds().items():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(world) + "\n", encoding="utf-8")
        print(
            f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {world['ticks']} intervals"
        )
    (args.out / "expectations.json").write_text(
        json.dumps(expectations(), indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
