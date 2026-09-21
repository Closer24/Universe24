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
4096 table's at s / 2, the same rounding of the same angle. Since
2026-09-21 (the pin of DERIVATIONS_BEAM section 24.4, the run the law
owes before the pin is final; the Boss's order under the model owner's
record 337) the same geometry, wheel and settings at N = 512
(`bell_n512_<a>_<b>`, the CHSH labels 0, 64, 128, 192; 532 intervals),
and the pin written before the run under `bell_24_4`: S = 181 / 64
exactly at N = 512 and N = 4096 (1448 / 512 and 11584 / 4096), the
marginals W / 2 exactly, and every count over the W births within one
of W x its cell's weight over the total, the counts per cell under
`pair_n`; the run's readings by kind and its run block beside the pin.

L7, the cone (the paper session's question on issue #376; the Boss's
approval of 2026-09-20): `cone_links` and `cone_intervals`, one geometry
(a lamp at (0, 0) on +x to a counter 17 Links away; a lamp at (0, 3) on
the plane diagonal (1, 1, 0) to a counter at (12, 15), 24 Links on the
staircase, the Euclidean distances 17 and 16.97; N 64, 96 intervals)
under the integer form of `phase_per_link` (3 per Link stepped) and the
pair form [3, 1] (3 per interval of age). Pinned from the flight table
(BEAM_LAW section 3): both rows click at the age 29; the path phase
phase - u at the click 51 and 8 under the integer form, 23 and 23 under
the pair form (`expectations.json` under `cone`).

    python examples/events/amplitude/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import math
import sys
from collections import OrderedDict
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.world_loading import families_by_definition, load_world  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

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
# L6 at N = 1024 and 4096 (2026-09-20); N = 512 added for the pin of
# DERIVATIONS_BEAM section 24.4 (2026-09-21).
PAIR_N = (512, 1024, 4096)
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
                "wheel": [1, N],
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


def shipped_world(path: Path) -> dict[str, object]:
    """A shipped world as its engine reads it, its families inline: since
    2026-09-20 a shipped world may take them from `entities/families.json`
    beside its series (`bell/read.json` does); the document's keys keep
    their order, `families` at the place of the reference."""
    document = json.loads(path.read_text(encoding="utf-8"))
    if "entity_definitions" not in document:
        return document
    expanded = json.loads(load_world(path.read_bytes(), base_dir=path.parent).expanded_source)
    inline: dict[str, object] = {}
    for key, value in document.items():
        if key == "entity_definitions":
            inline["families"] = expanded["families"]
        elif key != "entities":
            inline[key] = value
    return inline


def two_slits_geometry() -> dict[str, object]:
    """The shipped two-slit world with the freed band and the lamp's wall
    Nodes at x = 7 (the key and the lamp untouched)."""
    world = shipped_world(TWO_SLITS_SOURCE)
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
    lamp = world["measured"][0]
    lamp["amount"] = world["K"]
    lamp["lamp"]["rate"] = [1, 1]
    lamp["lamp"]["wheel"] = [1, N]
    for family in world["families"]:
        if family["name"] == "light":
            family["phase_per_link"] = FREQUENCY
    for detector in world["detectors"]:
        detector["reading"] = "sum"
    return world


# L2b: the openings' fan by angle (Huygens on the lattice; the
# mathematician's TWO_SLITS.md section 7, 2026-09-20): every primitive
# direction (a, b, 0) with a >= 1 and a + |b| <= HUYGENS_WIDTH, ordered by
# angle (consecutive directions are Farey neighbours, |a b' - a' b| = 1),
# each carrying as its split weight the angle it covers, half the gap to
# each neighbour, the gap between D and D' being 3 Q^2 / (T_D T_D') in the
# flight table's own resolution T_D = isqrt(3 |D|^2 Q^2) (the exact
# 1 / (|D| |D'|) for Farey neighbours), at the grain HUYGENS_GRAIN. The
# freed band admits at most FREED_HALF_WIDTH steps along the wall's plane
# before a row's first step in x, that is |b| <= (2 FREED_HALF_WIDTH + 1) a;
# the steeper directions are left out (they would walk into the wall or
# through the other opening), their angle lost at the fan's edges.
FLIGHT_Q = 64
HUYGENS_WIDTH = 48
# The grain keeps the load-time ceiling: the check multiplies every
# re-emitter's sum of squares A on the world (two openings: A^2 within 2^62,
# A within 2^31); at 2^18 the weights run 123 .. 5619 and A = 7.1 x 10^8.
HUYGENS_GRAIN = 1 << 18
HUYGENS_SLOPE = 2 * FREED_HALF_WIDTH + 1
# The birth wheel of L2b under the golden rate (the model owner's decision,
# record 180 of 2026-09-20's log; TWO_SLITS.md section 8; BEAM_LAW note 46):
# r / W = 2531 / 4096, the nearest odd integer to 0.618 W over W = 4096;
# 4096 births at one per interval and the last rows' flight within 4300.
HUYGENS_WHEEL = [2531, 4096]
HUYGENS_TICKS = 4300


def flight_resolution(vector: tuple[int, int]) -> int:
    """T_D = isqrt(3 |D|^2 Q^2), the flight table's resolution of D."""
    return math.isqrt(3 * (vector[0] ** 2 + vector[1] ** 2) * FLIGHT_Q * FLIGHT_Q)


def huygens_fan() -> tuple[list[tuple[int, int]], dict[tuple[int, int], int]]:
    """The full primitive fan within HUYGENS_WIDTH in angle order and the
    integer angle weight of every direction; the admitted directions are
    those within HUYGENS_SLOPE."""
    full = [
        (a, b)
        for a in range(1, HUYGENS_WIDTH + 1)
        for b in range(-HUYGENS_WIDTH, HUYGENS_WIDTH + 1)
        if a + abs(b) <= HUYGENS_WIDTH and math.gcd(a, b) == 1
    ]
    full.sort(key=lambda v: math.atan2(v[1], v[0]))
    weights: dict[tuple[int, int], int] = {}
    for i, v in enumerate(full):
        neighbours = [full[j] for j in (i - 1, i + 1) if 0 <= j < len(full)]
        gaps = [
            Fraction(3 * FLIGHT_Q * FLIGHT_Q, flight_resolution(v) * flight_resolution(w))
            for w in neighbours
        ]
        if len(gaps) == 1:
            gaps = gaps * 2
        weights[v] = int(HUYGENS_GRAIN * sum(gaps) / 2)
    admitted = [v for v in full if abs(v[1]) <= HUYGENS_SLOPE * v[0]]
    return admitted, weights


def two_slits_huygens() -> dict[str, object]:
    """L2b's world: `slits_low` with each opening's fan the Farey fan of
    width HUYGENS_WIDTH weighted by angle (the split's `weights`)."""
    world = two_slits_low()
    world["model_id"] = "beam-amplitude-slits_huygens-v1"
    world["ticks"] = HUYGENS_TICKS
    world["measured"][0]["lamp"]["wheel"] = HUYGENS_WHEEL
    admitted, weights = huygens_fan()
    # The world's direction table names every vector of the fan (the six
    # headings are the world's own); the registered 90 are among them.
    world["directions"] = [[a, b, 0] for a, b in admitted if (a, b) != (1, 0)]
    for entry in world["measured"]:
        if entry.get("table") == {"light": "rerelease"}:
            entry["table"] = {"light": {"rule": "rerelease", "weights": [weights[v] for v in admitted]}}
            entry["directions"] = [[a, b, 0] for a, b in admitted]
    return world


def two_slits_one() -> dict[str, object]:
    """The design's reference: one birth through L2's geometry without the
    key, the lamp's five rows declared as rays of amount 91."""
    world = two_slits_geometry()
    world["model_id"] = "beam-amplitude-slits_one-v1"
    world["ticks"] = SLITS_ONE_TICKS
    # The frequency declared as in `slits_low`: the engine turns the rows and
    # writes the phase at the exact time of each row's last Link on its click
    # line (`exact`; BEAM_LAW note 45), which the reading takes.
    for family in world["families"]:
        if family["name"] == "light":
            family["phase_per_link"] = FREQUENCY
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
    correlations; written before the run of `slits_low`. Since the exact
    phase at the click (2026-09-21, BEAM_LAW note 45) every row's phase is
    the `exact` of its click line, the phase at the exact time of its last
    Link, which the reference run forms as `slits_low` does."""
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
        phase = int(line["exact"])
        node = tuple(int(v) for v in line["node"])
        # A lamp row (the amount 91 stands for one unit at m = 5) or a fan
        # row (m = 5 x 91), at the phase of its last Link.
        multiplicity = LAMP_ROWS if int(line["number"]) == 1 else LAMP_ROWS * FAN_WAYS
        row = (1, multiplicity, phase)
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
    return {
        "slits_low": two_slits_low(),
        "slits_one": two_slits_one(),
        "slits_huygens": two_slits_huygens(),
    }


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
    world = shipped_world(BELL_SOURCE)
    world = copy.deepcopy(world)
    world["model_id"] = f"beam-amplitude-{name}-v1"
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
                "wheel": [1, N],
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
        "lamp": {"rate": [1, 1], "wheel": [1, N], "directions": [direction]},
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
    # The birth wheel [1, N] with this world's N (the count of births mod N).
    for entry in world["measured"]:
        if "lamp" in entry:
            entry["lamp"]["wheel"] = [1, n]
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


# L7, the cone: which length a row's phase counts (the paper session's
# question on issue #376, the Boss's approval of 2026-09-20; BEAM_LAW
# section 3, the flight table, and note 37 (iii), the two forms of
# `phase_per_link`). Two lamps, one on the heading +x toward a counter 17
# Links away, one on the plane diagonal (1, 1, 0) toward a counter 12 Links
# along each axis (the Euclidean distances 17 and 16.97). The flight table
# moves every direction at 1 / sqrt 3 Links per interval, so the two rows
# arrive at the same age; the integer form of `phase_per_link` turns the
# phase per Link stepped (17 against 24), the pair form per interval of age
# (the same turn at both counters).
CONE_TICKS = 96
CONE_STEP = 3
CONE_AXIS_LINKS = 17
CONE_DIAGONAL = 12
DIAGONAL_XY = [1, 1, 0]
FLIGHT_SCALE = 64


def flight_age(direction: list[int], links: int) -> int:
    """The first age at which the flight table has stepped `links` Links
    on `direction` (BEAM_LAW section 3: T_d = isqrt(3 |v|^2 Q^2),
    m(tau) = (2 tau S_1 Q + T_d) // (2 T_d), Q = 64)."""
    s1 = sum(abs(c) for c in direction)
    t_d = math.isqrt(3 * sum(c * c for c in direction) * FLIGHT_SCALE * FLIGHT_SCALE)
    age = 0
    while (2 * age * s1 * FLIGHT_SCALE + t_d) // (2 * t_d) < links:
        age += 1
    return age


def cone(name: str, per_age: bool) -> dict[str, object]:
    """The cone world: `per_age` selects the pair form [CONE_STEP, 1] (the
    phase per interval of age) over the integer form (per Link stepped)."""
    family: dict[str, object] = {"name": "light", "quantum": 1}
    family["phase_per_link"] = [CONE_STEP, 1] if per_age else CONE_STEP
    axis_end = [CONE_AXIS_LINKS, 0, 0]
    diagonal_start = [0, 3, 0]
    diagonal_end = [CONE_DIAGONAL, 3 + CONE_DIAGONAL, 0]
    measured: list[dict[str, object]] = [
        {
            "position": [0, 0, 0],
            "family": "light",
            "amount": SOURCE_CONTENT,
            "fixed": True,
            "lamp": {"rate": [1, 1], "wheel": [1, N], "directions": [PLUS_X]},
        },
        {
            "position": diagonal_start,
            "family": "light",
            "amount": SOURCE_CONTENT,
            "fixed": True,
            "lamp": {"rate": [1, 1], "wheel": [1, N], "directions": [DIAGONAL_XY]},
        },
        {"position": axis_end, "family": "light", "amount": 1, "fixed": True},
        {"position": diagonal_end, "family": "light", "amount": 1, "fixed": True},
    ]
    return {
        "law": "beam",
        "model_id": f"beam-amplitude-{name}-v1",
        "shape": [CONE_AXIS_LINKS + 2, 3 + CONE_DIAGONAL + 2, 1],
        "boundary": {"z": "periodic"},
        "ticks": CONE_TICKS,
        "K": CLOCK,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "directions": [DIAGONAL_XY],
        "families": [family],
        "measured": measured,
        "detectors": [
            {"name": "axis", "positions": [axis_end], "reading": "sum"},
            {"name": "diagonal", "positions": [diagonal_end], "reading": "sum"},
        ],
    }


def cone_worlds() -> dict[str, dict[str, object]]:
    return {"cone_links": cone("cone_links", False), "cone_intervals": cone("cone_intervals", True)}


def cone_expectations() -> dict[str, object]:
    """Pinned before the run: the age of the click at each counter (the
    flight table) and the path phase, phase - u modulo N, at the click
    (the integer form: CONE_STEP per Link stepped; the pair form: CONE_STEP
    per interval of age), the same for every record."""
    axis_age = flight_age(PLUS_X, CONE_AXIS_LINKS)
    diagonal_age = flight_age(DIAGONAL_XY, 2 * CONE_DIAGONAL)
    # The exact phase at the click (BEAM_LAW note 45): under the pair form
    # the whole part and the remainder of n x made x T_d over d x S_1 x Q
    # (the flight table's T_d = isqrt(3 |D|^2 Q^2)), the path phase its
    # whole part mod N; under the integer form the phase as it is.
    exact: dict[str, dict[str, object]] = {"cone_links": {"path_phase": {}, "remainder": {}}}
    exact["cone_links"]["path_phase"] = dict(
        axis=CONE_STEP * CONE_AXIS_LINKS % N, diagonal=CONE_STEP * 2 * CONE_DIAGONAL % N
    )
    exact["cone_links"]["remainder"] = {"axis": [0, 1], "diagonal": [0, 1]}
    intervals: dict[str, dict[str, object]] = {"path_phase": {}, "remainder": {}}
    for detector, vector, links in (
        ("axis", PLUS_X, CONE_AXIS_LINKS),
        ("diagonal", DIAGONAL_XY, 2 * CONE_DIAGONAL),
    ):
        s1 = sum(abs(c) for c in vector)
        resolution = math.isqrt(3 * sum(c * c for c in vector) * FLIGHT_Q * FLIGHT_Q)
        whole, rest = divmod(CONE_STEP * links * resolution, 1 * s1 * FLIGHT_Q)
        intervals["path_phase"][detector] = whole % N
        intervals["remainder"][detector] = [rest, s1 * FLIGHT_Q]
    exact["cone_intervals"] = intervals
    return {
        "links": {"axis": CONE_AXIS_LINKS, "diagonal": 2 * CONE_DIAGONAL},
        "age_at_click": {"axis": axis_age, "diagonal": diagonal_age},
        "same_age": axis_age == diagonal_age,
        "exact": exact,
        "cone_links": {
            "path_phase": {
                "axis": CONE_STEP * CONE_AXIS_LINKS % N,
                "diagonal": CONE_STEP * 2 * CONE_DIAGONAL % N,
            }
        },
        "cone_intervals": {
            "path_phase": {
                "axis": CONE_STEP * axis_age % N,
                "diagonal": CONE_STEP * diagonal_age % N,
            }
        },
    }


def worlds() -> dict[str, dict[str, object]]:
    found = mach_zehnder_worlds()
    found.update(two_slits_worlds())
    found.update(pair_worlds())
    found.update(gate_worlds())
    found.update(pair_n_worlds())
    found.update(cone_worlds())
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


# The pin of DERIVATIONS_BEAM section 24.4 (the Boss's order of 2026-09-21
# under the model owner's record 337): the registered Bell geometry at N =
# 512 and N = 4096 under the one click and the wheel [1, N], run before the
# pin is final. Written before the run: S = 181 / 64 exactly at every power
# of two from 512 (6.2; record 102), the marginals W / 2 exactly, every
# count over the W births within one of W x its cell's weight over the
# total. No number moves after the run: a reading outside its pin is
# reported with its numbers.
BELL_24_4_N = (512, 4096)
BELL_24_4_S = (181, 64)
BELL_24_4_TOLERANCE = 1


def cell_widths(
    weights: dict[tuple[str, ...], int], order: list[tuple[str, ...]], wheel: int
) -> dict[str, object]:
    """The ladder's cells on the wheel W: each cell's width W x w_k / T as a
    reduced pair, and its rung b_k = (2 W C_k + T) // (2 T) at the nearest
    integer (BEAM_LAW notes 37 (iii) and 46)."""
    total = sum(weights.values())
    cumulative = 0
    rungs: list[int] = []
    widths: dict[str, list[int]] = {}
    for key in order:
        cumulative += weights[key]
        rungs.append((2 * wheel * cumulative + total) // (2 * total))
        width = Fraction(wheel * weights[key], total)
        widths["".join(key)] = [width.numerator, width.denominator]
    return {"widths": widths, "rungs": rungs}


def bell_24_4_expectations() -> dict[str, object]:
    """The pin of 24.4 per world, derived by the design's reading on the
    wheel W of each world's lamp (`pair_n` holds the counts per cell): the
    cells' widths and rungs, E x W, the marginal W / 2, and S x N over the
    quadruple; the readings of the run are registered beside them."""
    worlds: dict[str, object] = {}
    s_times_n: dict[str, int] = {}
    for n in BELL_24_4_N:
        correlations: list[int] = []
        for a, b in chsh_labels(n):
            name = f"bell_n{n}_{a}_{b}"
            world = bell_n(name, n, a, b)
            lamp = next(entry for entry in world["measured"] if "lamp" in entry)  # type: ignore[union-attr]
            wheel = int(lamp["lamp"]["wheel"][1])
            weights = joint([(a, 0), (b, 0)], [(0, 1), (3, 1)], n)
            counts = counts_of(weights, outcomes(2), wheel)
            e = correlation(counts)
            correlations.append(e)
            worlds[name] = {
                "N": n,
                "wheel": lamp["lamp"]["wheel"],
                "W": wheel,
                "settings": [a, b],
                "ticks": world["ticks"],
                "births": wheel,
                "counts_under": f"pair_n.{n}.pairs.{a}_{b}.counts",
                "E": e,
                "marginal": wheel // 2,
                **cell_widths(weights, outcomes(2), wheel),
            }
        s_times_n[str(n)] = correlations[0] - correlations[1] + correlations[2] + correlations[3]
    return {
        "reference": "DERIVATIONS_BEAM section 24.4, the pin written before the run",
        "S": list(BELL_24_4_S),
        "S_times_N": s_times_n,
        "tolerance": BELL_24_4_TOLERANCE,
        "worlds": worlds,
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


# The GameBoard and layer readings the register split registered beside the
# design's expectations on 2026-09-21 (the trimming's part 2, PR #422: a test
# reads a world's numbers from the register, never a literal of its own): the
# births' and the splits' rows with the cancels, the first gathers, the
# gathers' last ticks, the totals' spread, the pair's birth and early records,
# the gate's lines and rows. Keyed by the path of the entry they extend.
REGISTERED_RUN_READINGS: dict[str, dict[str, object]] = {
    "mach_zehnder.mz_equal": {
        "birth": {
            "tick": 1,
            "rows": [[[0, 0, 0], 2, 0, 0, 1, 1, 0, 2], [[0, 0, 0], 4, 0, 16, 1, 1, 0, 2]],
            "rows_columns": "node, direction index, age, phase, amount, content, branch, multiplicity",
            "second": {
                "tick": 3,
                "phases": [1, 17],
                "accumulator_after_tick_2": 1048574,
                "note": "no birth at tick 2: the exact "
                "clock of the content 2^20 - 2 "
                "turns 0 (the fraction-free "
                "law, 2026-09-20)",
            },
        },
        "split": {
            "tick": 11,
            "rows": [[[3, 3, 0], 2, 0, 16, 41, 1, 0, 1682], [[3, 3, 0], 4, 0, 32, 1, 1, 0, 1682]],
            "born_per_split": 41,
            "cancelled_amount": 40,
            "cancelled_content": 40,
            "cancelled_momentum": [0, 2560, 0],
        },
        "first_gather": {
            "chosen": ["D1", 0, "0"],
            "rungs": [64, 64],
            "content": 41,
            "momentum": [2624, 0, 0],
            "node": [4, 3, 0],
        },
    },
    "mach_zehnder.mz_quarter": {"two_splits_tick": 11},
    "mach_zehnder.mz_balanced": {
        "split": {
            "tick": 11,
            "rows": [[[3, 3, 0], [1, 0, 0], 16, 2, 4]],
            "rows_columns": "node, direction, phase, amount, multiplicity",
            "cancelled": 2,
        }
    },
    "mach_zehnder.mz_345": {
        "pythagorean_5": {
            "u_to_D2": 63,
            "u_to_D1": 62,
            "first_rungs": [63, 64],
            "note": "the (3, 4) split sends u = 63 to D2 where the (20, 21) split sends it to D1",
        }
    },
    "mach_zehnder.mz_unequal_f8": {"two_splits_tick": 11},
    "mach_zehnder": {
        "gathered_by_tick": 76,
        "totals": {
            "distinct": 8,
            "least": "65448/65536",
            "most": "65773/65536",
            "note": "every record's total in the unit 2^58, one of "
            "eight values on every world (the tables' "
            "rounding by u); the design's bound 0.0019 holds "
            "for u = 0 alone",
        },
    },
    "two_slits": {
        "last_gather_tick": 214,
        "face_gathers": 15,
        "first": {"born": 1, "chosen": "measured:223", "node": [7, 58, 0], "content": 1},
    },
    "pair": {
        "birth": {
            "tick": 1,
            "node": [10, 0, 0],
            "arms": 2,
            "units": 4,
            "multiplicity": 2,
            "arm_directions": [[-1, 0, 0], [1, 0, 0]],
        },
        "choosers_early": {
            "count": 6,
            "born": [1, 2, 4, 5, 6, 7],
            "note": "the records born before choosers_first meet no "
            "setting and click at alice_minus; the lamp's "
            "exact clock stalls once, at tick 3",
        },
        "far_min_flight": 200,
    },
    "gate": {
        "twice": {
            "identity": True,
            "later_gates": {"joined": [], "labels": [[0, 1], [1, 1]], "nodes": [11, 8]},
            "rows": [
                [[0, 1, 0], 0, 0, 181, 0, 65536],
                [[0, 1, 0], 0, 1, 181, 32, 65536],
                [[0, 1, 0], 1, 0, 1, 0, 2],
                [[0, 1, 0], 1, 1, 1, 0, 2],
            ],
        },
        "rotate_line": {"setting": 16, "bit": 0, "rows": 2},
        "gate_line": {"arms": 2, "rows": 4, "labels": [[0, 1], [3, 1]], "joined_number": 4},
        "pair_rows": {
            "rows": [
                [[0, -1, 0], 1, 0, 1, 0, 2],
                [[0, -1, 0], 1, 3, 1, 0, 2],
                [[0, 1, 0], 0, 0, 181, 0, 65536],
                [[0, 1, 0], 0, 3, 181, 32, 65536],
            ],
            "rows_columns": "direction, arm, label, amount, phase, multiplicity",
            "amount_source": "181 = C[16] = S[16] of the 128-step tables; "
            "the amplitude 3036676096 = 181 x 2^24",
        },
        "ghz_gate_line": {"labels": [[0, 1], [7, 1]], "arms": 3, "rows": 6},
        "rotation_multiplicity": 65536,
    },
    # The run of 2026-09-21 for the pin of DERIVATIONS_BEAM section 24.4, its
    # readings by kind and its run block (the README's section and the
    # register's L6 entry); read by tests/test_amplitude_bell_24_4.py.
    "bell_24_4": {
        "run": {
            "date": "2026-09-21",
            "order": "DERIVATIONS_BEAM section 24.4, the run the law owes before the pin is final; the Boss under the model owner's record 337",
            "runner": "python -m event_universe --init <world> --output <dir>, headless, one world at a time",
            "main": "a625ec9f",
            "package_version": "0.3.1",
            "source_sha256": "47fffbefe2d222b73e448667769667ffc68bc54d75317fb55d9259e1c86d403f",
            "families_sha256": "438444b1cec9eb47263ac6b4203a1028b94ef9e97819aceadf860e7680ce15ca",
            "readings_by_kind": "DETECTOR: the gathers of the first W records by ordinal (the counts per cell, E x W, the + counts per party, the rungs and the totals on the gather lines); GAMEBOARD: the books and the layer's counts, a diagnostic",
            "host_cost": "the runner's wall time per world on a loaded host, apart from the model's cost: the bar's 21 Nodes at fixed local work per interval over the world's intervals, one record's offers held at the layer until its completion",
            "verdict": "PASS: every pin met on the eight worlds, no number moved",
            "worlds": {
                "bell_n512_0_64": {
                    "initialization_sha256": "08c4264ac4b68a174a21a42b6deb92a5d963bae1f7afd028445ed207bf8a5905",
                    "expanded_sha256": "bb5d6a5ccc056eec7f6b206ff2e08bfb94573137f4ef9b84846742951559847f",
                    "completed_ticks": 532,
                    "elapsed_seconds": 1.24,
                    "host_wall_seconds": 1.51,
                    "readings": {
                        "DETECTOR": {
                            "counts": {"++": 219, "+-": 37, "-+": 37, "--": 219},
                            "E": 364,
                            "alice_plus": 256,
                            "bob_plus": 256,
                            "gathered_of_W": 512,
                            "rungs_on_every_gather": [219, 256, 293, 512],
                            "distinct_totals": 57,
                        },
                        "GAMEBOARD": {
                            "conserved_at_every_completed_tick": True,
                            "books_balanced_every_tick": True,
                            "born": 531,
                            "gathered": 519,
                            "open": 12,
                        },
                    },
                },
                "bell_n512_0_192": {
                    "initialization_sha256": "05748a28cb85ba3f732e78debec8a25690bca49581f88cabf7ac60460999d6cd",
                    "expanded_sha256": "43b824fe37030a7171fc4aa67c1fa953620baf318639037064dd76e812e8d30a",
                    "completed_ticks": 532,
                    "elapsed_seconds": 1.26,
                    "host_wall_seconds": 1.53,
                    "readings": {
                        "DETECTOR": {
                            "counts": {"++": 37, "+-": 219, "-+": 219, "--": 37},
                            "E": -364,
                            "alice_plus": 256,
                            "bob_plus": 256,
                            "gathered_of_W": 512,
                            "rungs_on_every_gather": [37, 256, 475, 512],
                            "distinct_totals": 57,
                        },
                        "GAMEBOARD": {
                            "conserved_at_every_completed_tick": True,
                            "books_balanced_every_tick": True,
                            "born": 531,
                            "gathered": 519,
                            "open": 12,
                        },
                    },
                },
                "bell_n512_128_64": {
                    "initialization_sha256": "05d8170e360adcb6af675a58aabc1b04e79faeedf774c7a5a4dcc5ea5ac251e2",
                    "expanded_sha256": "bf0f26267efb40215bb00513248f979313989b6cc97622f93f0ece95f9ec78d2",
                    "completed_ticks": 532,
                    "elapsed_seconds": 1.27,
                    "host_wall_seconds": 1.54,
                    "readings": {
                        "DETECTOR": {
                            "counts": {"++": 218, "+-": 38, "-+": 38, "--": 218},
                            "E": 360,
                            "alice_plus": 256,
                            "bob_plus": 256,
                            "gathered_of_W": 512,
                            "rungs_on_every_gather": [218, 256, 294, 512],
                            "distinct_totals": 57,
                        },
                        "GAMEBOARD": {
                            "conserved_at_every_completed_tick": True,
                            "books_balanced_every_tick": True,
                            "born": 531,
                            "gathered": 519,
                            "open": 12,
                        },
                    },
                },
                "bell_n512_128_192": {
                    "initialization_sha256": "b5fc4bae939f0044afa4645de3cc2cfb1d5b12b49c670e644edcfdcbda6d7b73",
                    "expanded_sha256": "01e8e72f47824f5ee026e95c0a695846da68ef9d245fb101fe3c8bfc7b82ac0d",
                    "completed_ticks": 532,
                    "elapsed_seconds": 1.24,
                    "host_wall_seconds": 1.5,
                    "readings": {
                        "DETECTOR": {
                            "counts": {"++": 218, "+-": 38, "-+": 38, "--": 218},
                            "E": 360,
                            "alice_plus": 256,
                            "bob_plus": 256,
                            "gathered_of_W": 512,
                            "rungs_on_every_gather": [218, 256, 294, 512],
                            "distinct_totals": 57,
                        },
                        "GAMEBOARD": {
                            "conserved_at_every_completed_tick": True,
                            "books_balanced_every_tick": True,
                            "born": 531,
                            "gathered": 519,
                            "open": 12,
                        },
                    },
                },
                "bell_n4096_0_512": {
                    "initialization_sha256": "ad17507dc57bcd6d5dbce3dfcbedca0f7e4ac3be47451447bfb87d71b6c17a3a",
                    "expanded_sha256": "20338ad6e5b5fd98c5e1df726430f773ae7b9f17a9a69709354c06c50e0a7d29",
                    "completed_ticks": 4116,
                    "elapsed_seconds": 8.82,
                    "host_wall_seconds": 9.4,
                    "readings": {
                        "DETECTOR": {
                            "counts": {"++": 1749, "+-": 299, "-+": 299, "--": 1749},
                            "E": 2900,
                            "alice_plus": 2048,
                            "bob_plus": 2048,
                            "gathered_of_W": 4096,
                            "rungs_on_every_gather": [1749, 2048, 2347, 4096],
                            "distinct_totals": 139,
                        },
                        "GAMEBOARD": {
                            "conserved_at_every_completed_tick": True,
                            "books_balanced_every_tick": True,
                            "born": 4113,
                            "gathered": 4101,
                            "open": 12,
                        },
                    },
                },
                "bell_n4096_0_1536": {
                    "initialization_sha256": "ae8f717e7eb89f75533dccbff9b6a70542e18dc9ba062e3a2648c30759c38d79",
                    "expanded_sha256": "a13bed2798814e226c23a72079beca18f1b699d4e40379667476b8f7fbfb8d08",
                    "completed_ticks": 4116,
                    "elapsed_seconds": 9.05,
                    "host_wall_seconds": 9.64,
                    "readings": {
                        "DETECTOR": {
                            "counts": {"++": 299, "+-": 1749, "-+": 1749, "--": 299},
                            "E": -2900,
                            "alice_plus": 2048,
                            "bob_plus": 2048,
                            "gathered_of_W": 4096,
                            "rungs_on_every_gather": [299, 2048, 3797, 4096],
                            "distinct_totals": 139,
                        },
                        "GAMEBOARD": {
                            "conserved_at_every_completed_tick": True,
                            "books_balanced_every_tick": True,
                            "born": 4113,
                            "gathered": 4101,
                            "open": 12,
                        },
                    },
                },
                "bell_n4096_1024_512": {
                    "initialization_sha256": "ae61a322494fc480197fef70b861459ba54dad0e2d5e34d006fd015b21f8cc01",
                    "expanded_sha256": "7b70a2e007ffb22fe12dc7fcee0560b57da8717e09ac7a7e1335fb61a2b299c9",
                    "completed_ticks": 4116,
                    "elapsed_seconds": 8.74,
                    "host_wall_seconds": 9.32,
                    "readings": {
                        "DETECTOR": {
                            "counts": {"++": 1747, "+-": 301, "-+": 301, "--": 1747},
                            "E": 2892,
                            "alice_plus": 2048,
                            "bob_plus": 2048,
                            "gathered_of_W": 4096,
                            "rungs_on_every_gather": [1747, 2048, 2349, 4096],
                            "distinct_totals": 139,
                        },
                        "GAMEBOARD": {
                            "conserved_at_every_completed_tick": True,
                            "books_balanced_every_tick": True,
                            "born": 4113,
                            "gathered": 4101,
                            "open": 12,
                        },
                    },
                },
                "bell_n4096_1024_1536": {
                    "initialization_sha256": "126f70a97d2128ccd24468730a6f318cfb9fcc81d6ca4ec564b47900a492df91",
                    "expanded_sha256": "c17eeab34bbfb414346d76e4fd9a67fcec79e4ed957bda66f69b3a1ceb8d7318",
                    "completed_ticks": 4116,
                    "elapsed_seconds": 8.84,
                    "host_wall_seconds": 9.44,
                    "readings": {
                        "DETECTOR": {
                            "counts": {"++": 1747, "+-": 301, "-+": 301, "--": 1747},
                            "E": 2892,
                            "alice_plus": 2048,
                            "bob_plus": 2048,
                            "gathered_of_W": 4096,
                            "rungs_on_every_gather": [1747, 2048, 2349, 4096],
                            "distinct_totals": 139,
                        },
                        "GAMEBOARD": {
                            "conserved_at_every_completed_tick": True,
                            "books_balanced_every_tick": True,
                            "born": 4113,
                            "gathered": 4101,
                            "open": 12,
                        },
                    },
                },
            },
        }
    },
}

# The source of every registered entry (the owner's principle of 2026-09-21,
# record 205: a formula gives, a run proves): the formula or the section of
# docs/DERIVATIONS_BEAM.md that gives the number, or "measured" with the
# target that would give it; the derivation mathematician's targets are the
# source, nothing is invented here.
DERIVATIONS: dict[str, str] = {
    "births": "declared: the lamp's first 64 records read by their birth ordinal (the design); no formula gives the count",
    "mach_zehnder": "the offers by the click's bilinear form f^T G f on the splitter's rows (DERIVATIONS_BEAM 6.7: mz_equal's 1681/1682 and 1/1682 exact at every u); the clicks by the ladder's rungs b_k = (2 N C_k + Total) // (2 Total) on the offers (BEAM_LAW note 37; DERIVATIONS_BEAM 6.2); the totals' spread the tables' rounding (6.7); the births' and the splits' rows and ticks measured (the design's mz.py, the run)",
    "two_slits": "the weights and the total by the click computed at the click time from the flight's closed form and the Gram form (DERIVATIONS_BEAM 11.1 and 6.7, which reproduced the 64 registered clicks), each row's phase the exact phase at its last Link, floor(n made T_d / (d S_1 Q)) (BEAM_LAW note 45, the click line's `exact`); the fringe's paraxial form 7.1; the first gather and the last tick measured",
    "pair": "measured (target 6: Born and Tsirelson reached as limits, DERIVATIONS_BEAM 6.3 and 6.5; the finite-N cells the design's bell.py on the windows' half circles; the CHSH sum 176/64 the ladder's value at N = 64)",
    "ghz": "measured (target 6; the design's bell.py: the allowed triples and their products)",
    "gate": "the Hadamard's amount C[16] = S[16] = 181 of the 128-step tables (core/phase.py; the amplitude 181 x 2^24); the cells and the correlations measured (target 6)",
    "pair_n": "measured (target 6: |E - cos| <= 1/N the design's bound at N = 1024, failing at 4096 by the tables' rounding; 2896/1024 the design's sum)",
    "bell_24_4": "DERIVATIONS_BEAM 24.4 and 6.2: S = 181 / 64 exactly from the rungs b_k = (2 W C_k + T) // (2 T) of the ladder on the wheel W = N over the design's joint weights (bell.py, the half-angle tables of 2N), the marginals W / 2, every count within one of W x its weight over the total; the counts per cell under pair_n; the readings measured, the run of 2026-09-21, no number moved",
    "cone": "DERIVATIONS_BEAM 11.1: the flight's closed form m_D(tau) and tau_k = ceil((2 k - 1) T_D / (2 S_1 Q)), the phase k m_D(tau) under the integer form and floor(tau n / d) under the pair form; `exact` the phase at the exact time of the last Link, the whole part and the remainder of n x Links x T_D over d x S_1 x Q (BEAM_LAW note 45); derived from the worlds and compared by tests/test_amplitude_cone.py",
}


def expectations() -> dict[str, object]:
    found: dict[str, object] = copy.deepcopy(
        {
            "format": "amplitude-expectations-v1",
            "births": N,
            "mach_zehnder": MACH_ZEHNDER_EXPECTATIONS,
            "two_slits": two_slits_reading(),
            "pair": pair_expectations(),
            "ghz": ghz_expectations(),
            "gate": gate_expectations(),
            "pair_n": pair_n_expectations(),
            "bell_24_4": bell_24_4_expectations(),
            "cone": cone_expectations(),
        }
    )
    for path, entries in REGISTERED_RUN_READINGS.items():
        target: object = found
        for key in path.split("."):
            assert isinstance(target, dict)
            target = target[key]
        assert isinstance(target, dict)
        target.update(entries)
    found["derivations"] = DERIVATIONS
    return found


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, world in worlds().items():
        if name in UNSHIPPED:
            continue
        path = args.out / f"{name}.json"
        shipped = families_by_definition(world, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path.write_text(json.dumps(shipped) + "\n", encoding="utf-8")
        print(
            f"{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: {world['ticks']} intervals"
        )
    (args.out / "expectations.json").write_text(
        json.dumps(expectations(), indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
