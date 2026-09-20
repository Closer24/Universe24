"""Write the worlds of series L, the amplitude law (`amplitude-v1`; the
model owner, 2026-09-20, Highlights 5.4, "DECIDED: `amplitude-v1` is
built"; the physicist's and the mathematician's design,
docs/designs/amplitude-v1/DESIGN.md, sections 3.4, 7 and 14), and the
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
| `mz_balanced` | (1, 1) | equal | 0 | D1 64, D2 0 (D2's rows cancel on the GameBoard) |
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
since its re-emission, as the GameBoard turns it under the key; a face click
is the row as it stepped out, before that interval's turn), the
weight of a set |sum 32 v(p)|^2 / m in the unit (32 x 256)^2, the ladder
over the sets in the layer's order with the rungs at the nearest integer,
and the clicks per set over the 64 births u = 0 .. 63 read off the ladder
(every u falls in one cell; a set of several Nodes, a face, offers the
sum over its Nodes of the per-Node squares, coherent within a Node and
incoherent across Nodes); beside them the pixels with rows, the pixels
where two paths meet and the Pearson correlations the design registered
for the shipped geometry (0.753 with the incoherent sum, 0.38 with the
Euclidean two-source cosine, 0.963 of the 64-birth histogram with the
weights) recomputed for this geometry.

L3, the pair with the choosers, the CHSH labels, the which-path world and
no maintenance (the design's section 4, the acceptance tests 4, 6 and 9):
the registered A2 world `examples/events/bell/read.json` (a bar of 21, the
lamp at x = 10, Alice's counters at 7 and 4 whose windows read the chooser
`sa`, Bob's at 17 and 18 reading `sb`) under the key with `arms: 2` and
`branches` [[0, 1], [3, 1]] on the lamp (the pair: the joint labels 00 and
11, the bit k of a label the value on arm k; the directions ordered so
that Alice's arm is arm 0) and the four counters reading `sum`
(`bell_choosers`, 1000 intervals: the 960 births from tick 8, when the
choosers' rows have reached both counters, see every one of the choosers'
15 setting pairs with every u); the four worlds at the CHSH labels
(`bell_0_8`, `bell_0_24`, `bell_16_8`, `bell_16_24`: the chooser sources
removed, every counter's window the integer setting, 80 intervals); the
which-path worlds (`path_*`: a `read` entry of the counter family at x = 9
on Alice's arm, the detector `path` reading `sum`, before her counter);
and no maintenance (`bell_16_24_long`, `path_16_24_long`: Bob's counters
116 Links farther, about 200 intervals more of flight, 300 intervals).
L4, GHZ (the design's 4.5): a plane of 7 x 7, the lamp at (3, 3) on
three arms (+x, -x, +y; `branches` [[0, 1], [7, 1]]), a counter on each
arm at (6, 3), (0, 3), (3, 6) with the setting 16 and the turn 0 (X) or
16 (Y), the bases XXX, XYY, YXY, YYX and YYY (`ghz_*`, 80 intervals).

The expectations of L3 and L4 (`expectations.json` under `pair` and
`ghz`) are the design's own reading (`bell.py`): the counter with the
setting s rotates the two labels by the half-angle tables of 2N,
U_s = [[C'[s], S'[s] v(t)], [-S'[s], C'[s] v(t)]] with v(t) the circle
vector of the turn; the joint amplitude of the outcomes is the sum over
the joint labels of the products of the arms' entries, its weight the
square; the cells in the order of the arms (++, +-, -+, --), the rungs at
the nearest integer, the counts over the 64 births; a `read` on an arm
makes the labels its channels, the joint a product per label. Nothing of
the engine's layer enters the reading.

L5, the gate between records (the design's section 10): `cnot_pair_<a>_<b>`
(a plane of 16 x 11: the control's lamp at (2, 5) on +x through the
Hadamard at (4, 5), a `rerelease` whose `rotate` turns the label bit 0 by
the setting N/4, into the gate at (8, 5), a `rerelease` with `gate` {cnot,
hold, 2 parties} whose `inputs` send the control on +y to Alice at (8, 8)
and the target, born at (14, 5) on -x, on -y to Bob at (8, 2); Bob's
window the label -b, since CNOT on H|0> x |0> is |00> - |11> in this
convention); `cnot_twice` (the gate's two outputs on +x into a second gate
of one party at (11, 5): the identity); `cnot_ghz_<basis>` (three lamps
into one gate of three parties at (5, 5, 0) on a board of 11 x 11 x 3
with z periodic, the counters at (5, 8, 0), (5, 5, 1), (5, 5, 2) with
the settings X and Y); `rotations_3` and `rotations_4` (one record through
three, then four, label rotations in series: the multiplicity 65536 per
rotation, the fourth beyond 2^62 - 1, the register's ceiling). The
expectations (`expectations.json` under `gate`) are the design's `gate.py`
on the host's joint state. Grover's six rotations exceed the register on
the GameBoard (m = 2^96), as the design's section 10 states: not a world.
L6, the pair at N = 1024 and N = 4096 (`bell_n1024_<a>_<b>`,
`bell_n4096_<a>_<b>` at the CHSH labels 0, N/8, N/4, 3N/8; N + 20
intervals, one birth per u): S as the integer ratio at each N against the
design's 2896/1024, and the bound |E - cos| <= 1/N (`expectations.json`
under `pair_n`). At N = 4096 the half-angle tables of 2N do not exist
(the tables end at 4096 steps): the entry at an even setting s is the
4096 table's at s / 2, the same rounding of the same angle.

    python examples/events/amplitude/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import copy
import itertools
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
# L3 and L4: the registered A2 world, the pair's labels, the CHSH labels,
# the registered quadruple of the choosers' settings, the durations.
BELL_SOURCE = ROOT / "examples" / "events" / "bell" / "read.json"
MINUS_X = [-1, 0, 0]
BELL_PAIR = [[0, 1], [3, 1]]
GHZ_TRIPLE = [[0, 1], [7, 1]]
CHSH = ((0, 8), (0, 24), (16, 8), (16, 24))
CHOOSER_SETTINGS = ((0, 12, 25, 38, 51), (8, 29, 51))
REGISTERED_QUADRUPLE = ((0, 25), (8, 29))
BELL_TICKS = 80
# The choosers' rows reach Alice's counter at tick 8: the 960 births from
# tick 8 on see every one of the 15 setting pairs with every u.
CHOOSERS_FIRST = 8
CHOOSERS_BIRTHS = 960
CHOOSERS_TICKS = 1000
LONG_BOB = 116
LONG_TICKS = 300
PATH_NODE = 9
GHZ_SETTING = QUARTER
GHZ_BASES = ("XXX", "XYY", "YXY", "YYX", "YYY")
# L5 and L6.
PLUS_Z = [0, 0, 1]
MINUS_Z = [0, 0, -1]
MINUS_Y = [0, -1, 0]
GATE_TICKS = 90
GATE_BASES = ("XXX", "XYY", "YXY", "YYX")
ROTATIONS_WITHIN_BOUND = 3
# A world refused at load is built by the tests and not written as a file.
UNSHIPPED = {"rotations_4"}
PAIR_N = (1024, 4096)
MAX_TABLE = 4096
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


def ladder(weights: dict[str, Fraction], order: list[str], n: int = N) -> dict[str, int]:
    """The clicks per set over u = 0 .. n - 1: the rungs
    b_k = (2 n C_k + Total) // (2 Total) at the nearest integer over the
    sets in the layer's order, each set's count the rungs' difference."""
    total = sum(weights[k] for k in order)
    cumulative = Fraction(0)
    previous = 0
    counts: dict[str, int] = {}
    for name in order:
        cumulative += weights[name]
        rung = int((2 * n * cumulative + total) // (2 * total))
        if rung > previous:
            counts[name] = rung - previous
        previous = rung
    assert previous == n
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
    # The rows per set and per Node of the set: coherent within a Node,
    # incoherent across the Nodes of one set (the decision of 2026-09-20
    # on the owner's point 5).
    rows: dict[str, list[tuple[int, int, int]]] = OrderedDict()
    at_node: dict[str, dict[tuple[int, ...], list[tuple[int, int, int]]]] = OrderedDict()
    for line in lines:
        if line.get("event") != "click":
            continue
        detector = line["detector"]
        name = str(detector) if detector is not None else f"measured:{line['measured']}"
        tick, phase = int(line["tick"]), int(line["phase"])
        node = tuple(int(v) for v in line["node"])
        if int(line["number"]) == 1:
            # A lamp row: the amount 91 stands for one unit at m = 5, its
            # age its flight from the birth at tick 0.
            row = (1, LAMP_ROWS, (phase + turn(tick, tick)) % N)
            rows.setdefault(name, []).append(row)
            at_node.setdefault(name, {}).setdefault(node, []).append(row)
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
            row = (1, LAMP_ROWS * FAN_WAYS, (phase + turn(opened, opened) + turn(age, tick)) % N)
            rows.setdefault(name, []).append(row)
            at_node.setdefault(name, {}).setdefault(node, []).append(row)
    weights: dict[str, Fraction] = {}
    incoherent: dict[str, Fraction] = {}
    for name, found in rows.items():
        multiplicities = {m for _, m, _ in found}
        assert len(multiplicities) == 1, (name, multiplicities)
        m = multiplicities.pop()
        square = 0
        for node_rows in at_node[name].values():
            x = sum(32 * w * cosines[p] for w, _, p in node_rows)
            y = sum(32 * w * sines[p] for w, _, p in node_rows)
            square += x * x + y * y
        weights[name] = Fraction(square, m * DESIGN_UNIT)
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
        "face_nodes": {name: len(at_node[name]) for name in cells if name.startswith("face:")},
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


def bell(
    name: str,
    settings: tuple[int, int] | None = None,
    read: bool = False,
    far: bool = False,
) -> dict[str, object]:
    """The pair on the registered A2 world: the choosers' settings
    (`settings` None) or the fixed labels (a, b); with `read` a which-path
    `read` on Alice's arm before her counter; with `far` Bob's counters
    116 Links farther."""
    world = json.loads(BELL_SOURCE.read_text(encoding="utf-8"))
    world = copy.deepcopy(world)
    world["model_id"] = f"beam-amplitude-{name}-v1"
    world["amplitude"] = True
    world["ticks"] = CHOOSERS_TICKS if settings is None else BELL_TICKS
    lamp = world["measured"][0]
    lamp["lamp"]["directions"] = [MINUS_X, PLUS_X]
    lamp["lamp"]["arms"] = 2
    lamp["lamp"]["branches"] = BELL_PAIR
    for detector in world["detectors"]:
        detector["reading"] = "sum"
    if settings is not None:
        a, b = settings
        world["measured"] = [m for m in world["measured"] if m["family"] not in ("sa", "sb")]
        for m in world["measured"]:
            if m["family"] == "counter":
                m["table"]["light"] = {"phase_window": a if m["position"][0] < 10 else b}
    if far:
        world["shape"][0] += LONG_BOB
        world["ticks"] = LONG_TICKS
        for m in world["measured"]:
            if m["position"][0] > 10:
                m["position"][0] += LONG_BOB
        for detector in world["detectors"]:
            for position in detector["positions"]:
                if position[0] > 10:
                    position[0] += LONG_BOB
    if read:
        world["measured"].append(
            {
                "position": [PATH_NODE, 0, 0],
                "family": "counter",
                "amount": 1,
                "fixed": True,
                "table": {"light": {"rule": "read"}, "sa": "pass", "sb": "pass"},
            }
        )
        world["detectors"].append(
            {"name": "path", "positions": [[PATH_NODE, 0, 0]], "threshold": 1, "reading": "sum"}
        )
    return world


def ghz(name: str, basis: str) -> dict[str, object]:
    """GHZ: three arms, the counters' settings X (16, turn 0) or Y (16,
    turn 16) per letter of the basis."""
    arms = [([6, 3, 0], PLUS_X), ([0, 3, 0], MINUS_X), ([3, 6, 0], PLUS_Y)]
    measured: list[dict[str, object]] = [
        {
            "position": [3, 3, 0],
            "family": "light",
            "amount": SOURCE_CONTENT,
            "fixed": True,
            "lamp": {
                "rate": [1, 1],
                "directions": [direction for _, direction in arms],
                "arms": 3,
                "branches": GHZ_TRIPLE,
            },
        }
    ]
    detectors: list[dict[str, object]] = []
    for (position, _), letter, label in zip(arms, basis, "abc", strict=True):
        measured.append(
            {
                "position": position,
                "family": "counter",
                "amount": 1,
                "fixed": True,
                "table": {
                    "light": {
                        "phase_window": GHZ_SETTING,
                        "turn": QUARTER if letter == "Y" else 0,
                    }
                },
            }
        )
        detectors.append({"name": label, "positions": [position], "reading": "sum"})
    return {
        "law": "beam",
        "model_id": f"beam-amplitude-{name}-v1",
        "shape": [7, 7, 1],
        "boundary": {"z": "periodic"},
        "ticks": BELL_TICKS,
        "K": CLOCK,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "amplitude": True,
        "families": [{"name": "light", "quantum": 1}, {"name": "counter", "quantum": 1}],
        "measured": measured,
        "detectors": detectors,
    }


# The clock of the gate worlds: a rotation scales a row's amount by 256
# (181 at the setting N/4), so a counter holding three rotations' rows
# holds 181^3 x 2 content; the clock's bound 2 x content < K x N asks
# for a K of 2^50 (the lamp's content K, one phase step per interval).
GATE_CLOCK = 1 << 50


def lamp(position: list[int], direction: list[int]) -> dict[str, object]:
    return {
        "position": position,
        "family": "light",
        "amount": GATE_CLOCK,
        "fixed": True,
        "lamp": {"rate": [1, 1], "directions": [direction]},
    }


def hadamard(position: list[int], direction: list[int]) -> dict[str, object]:
    """A re-emitter on one direction rotating the label bit 0 by N/4."""
    return {
        "position": position,
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {"light": {"rule": "rerelease", "rotate": {"setting": QUARTER}}},
        "directions": [direction],
    }


def cnot_gate(
    position: list[int],
    inputs: list[list[int]],
    outputs: list[list[int]],
    parties: int,
    control: list[int] | None = None,
) -> dict[str, object]:
    """A re-emitter with the CNOT gate, each arrival re-emitted on its own
    output (the mirror per input); `control` the direction the control's
    rows arrive on (required for two parties or more)."""
    ways = len(outputs)
    gate: dict[str, object] = {"kind": "cnot", "hold": True, "parties": parties}
    if control is not None:
        gate["control"] = control
    return {
        "position": position,
        "family": "light",
        "amount": 1,
        "fixed": True,
        "table": {
            "light": {
                "rule": "rerelease",
                "inputs": inputs,
                "weights": [[1 if j == k else 0 for j in range(ways)] for k in range(ways)],
                "gate": gate,
            }
        },
        "directions": outputs,
    }


def counter(position: list[int], setting: int, turn: int = 0) -> dict[str, object]:
    entry: dict[str, object] = {"phase_window": setting}
    if turn:
        entry["turn"] = turn
    return {
        "position": position,
        "family": "counter",
        "amount": 1,
        "fixed": True,
        "table": {"light": entry},
    }


def gate_world(
    name: str,
    shape: list[int],
    measured: list[dict[str, object]],
    detectors: list[dict[str, object]],
    ticks: int = GATE_TICKS,
) -> dict[str, object]:
    return {
        "law": "beam",
        "model_id": f"beam-amplitude-{name}-v1",
        "shape": shape,
        "boundary": {"z": "periodic"},
        "ticks": ticks,
        "K": GATE_CLOCK,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "amplitude": True,
        "families": [{"name": "light", "quantum": 1}, {"name": "counter", "quantum": 1}],
        "measured": measured,
        "detectors": detectors,
    }


def cnot_pair(name: str, a: int, b: int) -> dict[str, object]:
    """The pair made by the gate: H on the control, CNOT with the target,
    Alice at a and Bob at -b."""
    measured = [
        lamp([2, 5, 0], PLUS_X),
        hadamard([4, 5, 0], PLUS_X),
        cnot_gate([8, 5, 0], [PLUS_X, MINUS_X], [PLUS_Y, MINUS_Y], 2, PLUS_X),
        lamp([14, 5, 0], MINUS_X),
        counter([8, 8, 0], a),
        counter([8, 2, 0], (-b) % N),
    ]
    detectors = [
        {"name": "alice", "positions": [[8, 8, 0]], "reading": "sum"},
        {"name": "bob", "positions": [[8, 2, 0]], "reading": "sum"},
    ]
    return gate_world(name, [16, 11, 1], measured, detectors)


def cnot_twice(name: str) -> dict[str, object]:
    """The second CNOT by one gate per arm (a permutation of the joint
    label is one relabelling, whichever arm's rows a gate sees; a gate of
    one party without `hold` acts on the rows present): the identity; then
    an absorber per arm. The target's lamp at (8, 1) on +y into the gate
    at (8, 5); the gate's outputs the control on +x to the gate at (11, 5)
    and the target on +y to the gate at (8, 8); their outputs +y to the
    absorbers at (11, 8) and (8, 10)."""
    measured = [
        lamp([2, 5, 0], PLUS_X),
        hadamard([4, 5, 0], PLUS_X),
        cnot_gate([8, 5, 0], [PLUS_X, PLUS_Y], [PLUS_X, PLUS_Y], 2, PLUS_X),
        lamp([8, 1, 0], PLUS_Y),
        cnot_gate([11, 5, 0], [PLUS_X], [PLUS_Y], 1),
        cnot_gate([8, 8, 0], [PLUS_Y], [PLUS_Y], 1),
        {"position": [11, 8, 0], "family": "counter", "amount": 1, "fixed": True},
        {"position": [8, 10, 0], "family": "counter", "amount": 1, "fixed": True},
    ]
    for index in (4, 5):
        measured[index]["table"]["light"]["gate"]["hold"] = False  # type: ignore[index]
    detectors = [
        {"name": "end_a", "positions": [[11, 8, 0]], "reading": "sum"},
        {"name": "end_b", "positions": [[8, 10, 0]], "reading": "sum"},
    ]
    return gate_world(name, [16, 11, 1], measured, detectors)


def cnot_ghz(name: str, basis: str) -> dict[str, object]:
    """GHZ by one gate of three parties: H on the control, CNOT to both
    targets, the counters' settings per letter."""
    positions = [[5, 8, 0], [5, 5, 1], [5, 5, 2]]
    measured = [
        lamp([5, 1, 0], PLUS_Y),
        hadamard([5, 2, 0], PLUS_Y),
        cnot_gate([5, 5, 0], [PLUS_Y, MINUS_X, PLUS_X], [PLUS_Y, PLUS_Z, MINUS_Z], 3, PLUS_Y),
        lamp([9, 5, 0], MINUS_X),
        lamp([1, 5, 0], PLUS_X),
    ]
    detectors: list[dict[str, object]] = []
    for position, letter, label in zip(positions, basis, "abc", strict=True):
        measured.append(counter(position, GHZ_SETTING, QUARTER if letter == "Y" else 0))
        detectors.append({"name": label, "positions": [position], "reading": "sum"})
    return gate_world(name, [11, 11, 3], measured, detectors)


def rotations(name: str, count: int) -> dict[str, object]:
    """One record through `count` label rotations in series on a bar, then
    an absorber reading `sum`."""
    measured = [lamp([0, 0, 0], PLUS_X)]
    for k in range(count):
        measured.append(hadamard([2 + 2 * k, 0, 0], PLUS_X))
    end = 2 + 2 * count
    measured.append({"position": [end, 0, 0], "family": "counter", "amount": 1, "fixed": True})
    detectors = [{"name": "end", "positions": [[end, 0, 0]], "reading": "sum"}]
    return gate_world(name, [end + 1, 1, 1], measured, detectors, ticks=110)


def gate_worlds() -> dict[str, dict[str, object]]:
    found: dict[str, dict[str, object]] = {}
    for a, b in CHSH:
        found[f"cnot_pair_{a}_{b}"] = cnot_pair(f"cnot_pair_{a}_{b}", a, b)
    found["cnot_twice"] = cnot_twice("cnot_twice")
    for basis in GATE_BASES:
        found[f"cnot_ghz_{basis.lower()}"] = cnot_ghz(f"cnot_ghz_{basis.lower()}", basis)
    found["rotations_3"] = rotations("rotations_3", ROTATIONS_WITHIN_BOUND)
    found["rotations_4"] = rotations("rotations_4", ROTATIONS_WITHIN_BOUND + 1)
    return found


def bell_n(name: str, n: int, a: int, b: int) -> dict[str, object]:
    """The pair at the CHSH labels at N = n on the A2 board, one birth per u."""
    world = bell(name, (a, b))
    world["N"] = n
    world["ticks"] = n + 20
    return world


def chsh_labels(n: int) -> tuple[tuple[int, int], ...]:
    return ((0, n // 8), (0, 3 * n // 8), (n // 4, n // 8), (n // 4, 3 * n // 8))


def pair_n_worlds() -> dict[str, dict[str, object]]:
    found: dict[str, dict[str, object]] = {}
    for n in PAIR_N:
        for a, b in chsh_labels(n):
            found[f"bell_n{n}_{a}_{b}"] = bell_n(f"bell_n{n}_{a}_{b}", n, a, b)
    return found


def pair_worlds() -> dict[str, dict[str, object]]:
    found = {"bell_choosers": bell("bell_choosers")}
    for a, b in CHSH:
        found[f"bell_{a}_{b}"] = bell(f"bell_{a}_{b}", (a, b))
        found[f"path_{a}_{b}"] = bell(f"path_{a}_{b}", (a, b), read=True)
    found["bell_16_24_far"] = bell("bell_16_24_far", (16, 24), far=True)
    found["path_16_24_far"] = bell("path_16_24_far", (16, 24), read=True, far=True)
    for basis in GHZ_BASES:
        found[f"ghz_{basis.lower()}"] = ghz(f"ghz_{basis.lower()}", basis)
    return found


def worlds() -> dict[str, dict[str, object]]:
    found = mach_zehnder_worlds()
    found.update(two_slits_worlds())
    found.update(pair_worlds())
    found.update(gate_worlds())
    found.update(pair_n_worlds())
    return found


# The design's reading of the pair (`bell.py`), in its integers.
Complex = tuple[int, int]


def cmul(a: Complex, b: Complex) -> Complex:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def half_angle(setting: int, n: int) -> Complex:
    """C'[s], S'[s] of the half-angle tables of 2n; at 2n beyond the tables'
    4096 steps the 4096 table at s / 2 (an even s)."""
    from event_universe.core.phase import phase_cosines, phase_sines

    size = min(2 * n, MAX_TABLE)
    factor = 2 * n // size
    index = setting % (2 * n)
    assert index % factor == 0, (setting, n)
    index //= factor
    return phase_cosines(size)[index], phase_sines(size)[index]


def rotation(setting: int, turn: int = 0, n: int = N) -> dict[tuple[str, int], Complex]:
    """U_s on the half-angle tables of 2N: the entry per (channel, label
    bit), complex integers in 1/256^2, the turn on the label 1 column."""
    from event_universe.core.phase import phase_cosines, phase_sines

    c, s = half_angle(setting, n)
    circle: Complex = (phase_cosines(n)[turn % n], phase_sines(n)[turn % n])
    return {
        ("+", 0): (c * 256, 0),
        ("+", 1): cmul((s, 0), circle),
        ("-", 0): (-s * 256, 0),
        ("-", 1): cmul((c, 0), circle),
    }


def joint(
    settings: list[tuple[int, int]], labels: list[tuple[int, int]], n: int = N
) -> dict[tuple[str, ...], int]:
    """The weight per outcome tuple: the square of the sum over the joint
    labels (with their weights) of the products of the arms' entries."""
    tables = [rotation(s, t, n) for s, t in settings]
    found: dict[tuple[str, ...], int] = {}
    for outcome in itertools.product("+-", repeat=len(settings)):
        total: Complex = (0, 0)
        for label, weight in labels:
            product: Complex = (weight, 0)
            for k, channel in enumerate(outcome):
                product = cmul(product, tables[k][(channel, (label >> k) & 1)])
            total = (total[0] + product[0], total[1] + product[1])
        found[outcome] = total[0] * total[0] + total[1] * total[1]
    return found


def counts_of(
    weights: dict[tuple[str, ...], int], order: list[tuple[str, ...]], n: int = N
) -> dict[str, int]:
    """The clicks per outcome over u = 0 .. n - 1 by the ladder."""
    fractions = {"".join(k): Fraction(v) for k, v in weights.items()}
    return ladder(fractions, ["".join(k) for k in order], n)


def outcomes(arms: int) -> list[tuple[str, ...]]:
    return list(itertools.product("+-", repeat=arms))


def pair_counts(a: int, b: int, n: int = N) -> dict[str, int]:
    return counts_of(joint([(a, 0), (b, 0)], [(0, 1), (3, 1)], n), outcomes(2), n)


def correlation(counts: dict[str, int]) -> int:
    """E x N from the counts over (oA, oB): same signs less different."""
    return sum(v if k[-2] == k[-1] else -v for k, v in counts.items())


def product_counts(a: int, b: int) -> dict[str, int]:
    """The which-path world: a `read` on Alice's arm makes the labels its
    channels, the joint a product per label, the cells (label, oA, oB)."""
    weights: dict[tuple[str, ...], int] = {}
    order: list[tuple[str, ...]] = []
    for label in (0, 3):
        ua, ub = rotation(a), rotation(b)
        for oa in "+-":
            for ob in "+-":
                key = (str(label), oa, ob)
                weights[key] = (ua[(oa, label & 1)][0] ** 2) * (ub[(ob, (label >> 1) & 1)][0] ** 2)
                order.append(key)
    return counts_of(weights, order)


def chsh(correlations: dict[tuple[int, int], int]) -> int:
    """S x N on the CHSH labels: E(0, 8) - E(0, 24) + E(16, 8) + E(16, 24)."""
    (a1, a2), (b1, b2) = (0, 16), (8, 24)
    return (
        correlations[(a1, b1)] - correlations[(a1, b2)] + correlations[(a2, b1)] + correlations[(a2, b2)]
    )


def pair_expectations() -> dict[str, object]:
    fixed = {f"{a}_{b}": pair_counts(a, b) for a, b in CHSH}
    paths = {f"{a}_{b}": product_counts(a, b) for a, b in CHSH}
    chooser_pairs = {(a, b): pair_counts(a, b) for a in CHOOSER_SETTINGS[0] for b in CHOOSER_SETTINGS[1]}
    chooser_e = {key: correlation(counts) for key, counts in chooser_pairs.items()}
    (a1, a2), (b1, b2) = REGISTERED_QUADRUPLE
    registered = chooser_e[(a1, b1)] - chooser_e[(a1, b2)] + chooser_e[(a2, b1)] + chooser_e[(a2, b2)]
    return {
        "reference": "the design's bell.py",
        "labels": BELL_PAIR,
        "chsh": {key: {"counts": counts, "E": correlation(counts)} for key, counts in fixed.items()},
        "chsh_S": chsh({(a, b): correlation(fixed[f"{a}_{b}"]) for a, b in CHSH}),
        "which_path": {
            key: {"counts": counts, "E": correlation(counts)} for key, counts in paths.items()
        },
        "which_path_S": chsh({(a, b): correlation(paths[f"{a}_{b}"]) for a, b in CHSH}),
        "choosers": {
            f"{a}_{b}": {"counts": counts, "E": chooser_e[(a, b)]}
            for (a, b), counts in chooser_pairs.items()
        },
        "choosers_first": CHOOSERS_FIRST,
        "choosers_births": CHOOSERS_BIRTHS,
        "registered_quadruple": [list(pair) for pair in REGISTERED_QUADRUPLE],
        "registered_S": registered,
        "marginal": N // 2,
        "far": {"bell_16_24": correlation(fixed["16_24"]), "path_16_24": correlation(paths["16_24"])},
    }


# The design's reading of the gate (`gate.py`): the record's joint state on
# the host, labels as tuples of bits with complex amplitudes.
State = dict[tuple[int, ...], Complex]


def rotate_state(state: State, qubit: int, setting: int, turn: int = 0) -> State:
    table = rotation(setting, turn)
    out: State = {}
    for label, amplitude in state.items():
        for channel, bit in (("+", 0), ("-", 1)):
            new = label[:qubit] + (bit,) + label[qubit + 1 :]
            entry = table[(channel, label[qubit])]
            product = cmul(entry, amplitude)
            found = out.get(new, (0, 0))
            out[new] = (found[0] + product[0], found[1] + product[1])
    return {k: v for k, v in out.items() if v != (0, 0)}


def cnot_state(state: State, targets: tuple[int, ...]) -> State:
    out: State = {}
    for label, amplitude in state.items():
        new = list(label)
        for target in targets:
            new[target] ^= label[0]
        key = tuple(new)
        found = out.get(key, (0, 0))
        out[key] = (found[0] + amplitude[0], found[1] + amplitude[1])
    return out


def state_counts(state: State, order: list[tuple[int, ...]]) -> dict[str, int]:
    weights = {k: v[0] * v[0] + v[1] * v[1] for k, v in state.items()}
    return ladder(
        {"".join("+-"[bit] for bit in k): Fraction(weights.get(k, 0)) for k in order},
        ["".join("+-"[bit] for bit in k) for k in order],
    )


def gate_expectations() -> dict[str, object]:
    unit: Complex = (256 * 256, 0)
    plus = rotate_state({(0, 0): unit}, 0, QUARTER)
    pair = cnot_state(plus, (1,))
    order2 = [(0, 0), (0, 1), (1, 0), (1, 1)]
    chsh_rows: dict[str, object] = {}
    correlations: dict[tuple[int, int], int] = {}
    for a, b in CHSH:
        measured = rotate_state(rotate_state(pair, 0, a), 1, (-b) % N)
        counts = state_counts(measured, order2)
        chsh_rows[f"{a}_{b}"] = {"counts": counts, "E": correlation(counts)}
        correlations[(a, b)] = correlation(counts)
    ghz_state = cnot_state(rotate_state({(0, 0, 0): unit}, 0, QUARTER), (1, 2))
    order3 = list(itertools.product((0, 1), repeat=3))
    ghz: dict[str, object] = {}
    for basis in GATE_BASES:
        measured = ghz_state
        for qubit, letter in enumerate(basis):
            measured = rotate_state(measured, qubit, GHZ_SETTING, QUARTER if letter == "Y" else 0)
        counts = state_counts(measured, order3)
        allowed = sorted(k for k, v in counts.items() if v)
        ghz[basis.lower()] = {
            "allowed": allowed,
            "counts": {k: v for k, v in counts.items() if v},
            "products": sorted({1 if k.count("-") % 2 == 0 else -1 for k in allowed}),
        }
    return {
        "reference": "the design's gate.py",
        "hadamard": {"".join(map(str, k)): list(v) for k, v in plus.items()},
        "pair": {"".join(map(str, k)): list(v) for k, v in pair.items()},
        "twice": cnot_state(pair, (1,)) == plus,
        "chsh": chsh_rows,
        "chsh_S": chsh(correlations),
        "ghz": ghz,
        "rotations_within_bound": ROTATIONS_WITHIN_BOUND,
        "rows_bound": "n x 2^n rows per record after n gates",
    }


def pair_n_expectations() -> dict[str, object]:
    found: dict[str, object] = {}
    for n in PAIR_N:
        labels = chsh_labels(n)
        rows: dict[str, object] = {}
        correlations: dict[tuple[int, int], int] = {}
        for a, b in labels:
            counts = pair_counts(a, b, n)
            e = correlation(counts)
            correlations[(a, b)] = e
            cosine = math.cos(2 * math.pi * (a - b) / n)
            rows[f"{a}_{b}"] = {
                "counts": counts,
                "E": e,
                "cosine": round(cosine, 6),
                "within_1_over_N": abs(e / n - cosine) <= 1 / n,
            }
        s = (
            correlations[labels[0]]
            - correlations[labels[1]]
            + correlations[labels[2]]
            + correlations[labels[3]]
        )
        found[str(n)] = {"labels": [list(pair) for pair in labels], "pairs": rows, "S": s}
    found["design_S_1024"] = 2896
    return found


def ghz_expectations() -> dict[str, object]:
    found: dict[str, object] = {}
    for basis in GHZ_BASES:
        settings = [(GHZ_SETTING, QUARTER if letter == "Y" else 0) for letter in basis]
        weights = joint(settings, [(0, 1), (7, 1)])
        counts = counts_of(weights, outcomes(3))
        allowed = sorted("".join(k) for k, v in weights.items() if v)
        products = sorted({1 if k.count("-") % 2 == 0 else -1 for k in allowed})
        found[basis.lower()] = {
            "allowed": allowed,
            "weight": max(weights.values()),
            "counts": {k: v for k, v in counts.items() if v},
            "products": products,
        }
    return found


def expectations() -> dict[str, object]:
    return {
        "format": "amplitude-expectations-v1",
        "births": N,
        "mach_zehnder": MACH_ZEHNDER_EXPECTATIONS,
        "two_slits": two_slits_reading(),
        "pair": pair_expectations(),
        "ghz": ghz_expectations(),
        "gate": gate_expectations(),
        "pair_n": pair_n_expectations(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, world in worlds().items():
        if name in UNSHIPPED:
            continue
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
