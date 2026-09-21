"""Write the worlds of series J, "the weak force", under the Beam Law (the
model owner, 2026-09-20, "go on everything": the neutrino first with the
table-entry key `phase_width` and no change of law, series J2; then the
transformation `become` with the identity `weak-v1`, series J1 and J3;
then the W world, the exchange form at one Link; the physicist's design,
WEAK.md sections 1, 2 and 4.5).

Every expectation printed here is written before the run and is a GameBoard
computation from the engine's own functions, never a rule replayed: the
first-arrival ages off the flight table (`nature_beam.direction_flight`) for
J2, and for J1 and J3 the count each clock reads at its Node
(`Measured.counted`, the presence over every ray of another number) on the
same world run without its `become` keys until the crowd is steady, from
which the trigger tick follows by the one primitive: a clock that reads a
constant count c at every self-creation owes `by_clock(a, c, 2^20)` after
each, and the sum over a = 0 .. at - 1 telescopes to floor(at x c / 2^20),
so the self-creation that takes the age to `at` is the tick at + floor(at
x c / 2^20); the crowd builds up over the first intervals (the count is
lower before every line has arrived), so the tick is that number or up to
three intervals before it. The readings tool (`tools/weak_readings.py`) reads the
run's record and compares; `expectations.json` beside the worlds holds the
numbers this generator pinned.

J2, the neutrino's passage through a filled bar: a fixed source of the
free family `nu` (a phase circle, no charge, no content on its rays) of
content 4096 at x = 0 of a bar of 200 x 1 x 1, K 4096 (the turn 4096 /
4096 = 1 phase step per self-creation: the stride 1 over the circle of
N = 64) and `release` [1, 4096] (one ray per self-creation on +x), so the
ray born at tick t carries the phase (t - 1) mod 64; 128 fixed readers of
the paid family `d` (content 1, releasing nothing) at x = 8 .. 135, each
with `measure` for `nu` under a window; a far detector of `d` at x = 190
measuring `nu` without a window (it counts every ray that reaches it).
1037 intervals, so that the first reader's arrivals (the rays born at the
ticks 1 .. 1024, arriving at x = 8 at the age 13) are exactly 1024, sixteen
turns of the circle.

| world | the readers' windows | the source's stride |
| --- | --- | --- |
| `j2_filter` | every centre 0, width 1 | 1 |
| `j2_ladder` | the centre x mod 64, width 1 | 1 |
| `j2_default` | every centre 0, the default width (the half circle) | 1 |
| `j2_stride2` | every centre 0, width 1 | 2 (K 2048: the turn 2) |
| `j2_stride2_odd` | every centre 1, width 1 | 2 |

J1, the free neutron's decay count against its clock: 64 neutrons of the
register's `n` (content 1839, fixed; the design's 512 at `at` 2048 cut for
the record's budget, the neutrons' own rows clicking on the faces at 6
lines per neutron per interval; the strong unit `nuclear` is not held, a
lifetime of 3 never reaching a neighbour at the pitch 4) on a lattice of
pitch 4 (4 x 4 x 4, the offsets -6 .. 6) about the centre of an open 41^3
GameBoard, each with `become` at 512 into `p` with the products `beta`
(1, 3) and `nu` (1, 0) (the charges: `p`'s 4 per unit on 1836 = 7344
against the beta's -7344 per unit of amount, the register's scale of series
I), `suspension` [1, 2^20], every neutron releasing one row of 1839 per
heading per interval (`release` [1, 1]) and passing every family but its
own crowd's count; a shell of the paid family `d` at r = 18 declared as
one `beam` detector set measuring `beta` (the count) and passing everything
else, the beta's `reads` `age` (the flight time on the click). (a)
`j1_lattice`: the neutrons alone, each one's clock reading its line-mates'
rows (the rows of the other neutrons on its three axis lines, at the
distances 4, 8 and 12, each dwelling one or two intervals at its Node);
(b) `j1_source`: with a fixed source `s` of content 4096 at the centre
releasing one row per direction of the 290 primitive directions with |a| +
|b| + |c| <= 6 per interval (a crowd with a gradient: the neutrons on the
fan's digital lines count more and fire later). 650 intervals.

J3, the bound neutron in the deuteron: series I's deuteron at one Link
(the proton 1836 of `p` holding one `nuclear` at (10, 10, 10), the neutron
1839 of `n` holding one at (11, 10, 10), the column `strong` 10000 with the
sign minus and the lifetime 3, `width` 2^28, the 290 fan, the contact
through the table) with `become` at 512 on the neutron (the design's 2048
cut for the record's budget: the law is linear in the key, the reading its
ratio) and `suspension` [1, 2^20], a shell of `d` at r = 8 as a `beam` set
measuring `beta`. (a) `j3_deuteron`: expected the transformation at 512 +
floor(512 c / 2^20) with c the neutron's count at one Link from the proton
(about 1837 x 70, the fan's lines through the neighbour Node with their
dwells), then two protons at one Link, bound by series I's reading (the
push 148 716 220 864 inward at G = 10000: no step; the design's "two
protons repelling" is corrected by series I's registered result); (b)
`j3_deuteron_crowd`: with `crowd` 65536 the count is above the gate at
every self-creation and the neutron never fires in 700 intervals (the
second pulse of the key at the age 1024 lies beyond the run); (c)
`j3_neutron_free`: the neutron alone at the centre fires at tick 512
exactly (its clock counts nothing).

The W world, the exchange form at one Link (WEAK.md 1.1; no key added to
the law: `become`, D-1 and the lifetime composed): a bar of 7 x 1 x 1,
K 2^20, N 64, `release` [1, 2^20] (no free release of 1839 before the age
570), `suspension` 0; `w` a paid family (quantum 1) with the charge -7344
per unit of amount and the `lifetime` 1, no column; the neutron `n` of
content 1839 fixed at x = 2 with `become` at 8 into `p` with the one
product `[["w", 1, 3]]` (the charges: 4 x 1836 on the proton left against
-7344 on the W unit) and `directions` `[[1, 0, 0]]`, the proton `p` of
content 1836 fixed at x = 3, 16 intervals. `w_exchange`: expected the W
row born at tick 8 (the recoil -192 on the neutron become proton), at one
Link at tick 9 (its age 1, m(1) = 1) and measured there by the keys' rule
for a paid arrival (the push +192): the proton then holds the W unit, its
content 1839 and its charge 0, a neutron's in the detector's terms; no W
on the border `lifetime`. The contact form (L = 0, no carrier) is series
J1 and J3's `become` itself; no Z family.

    python examples/events/weak/make_worlds.py [--out DIR] [--no-expect]
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from event_universe.events import NatureBeamSimulation, parse_nature_beam_world  # noqa: E402
from event_universe.events.nature_beam import direction_flight  # noqa: E402
from event_universe.register_map import carry_replicated  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

N = 64
K = 1 << 20
SUSPENSION = [1, 1 << 20]
AT = 512
Json = dict[str, object]

# -- J2 -----------------------------------------------------------------------------
K_STRIDE_1 = 4096
K_STRIDE_2 = 2048
SOURCE_CONTENT = 4096
BAR = 200
READERS = range(8, 136)
FAR = 190
J2_TICKS = 1037
PLUS_X = (1, 0, 0)

# -- J1 and J3: the register's nucleons (series I) ----------------------------------
PROTON = 1836
NEUTRON = 1839
CHARGE = 4
STRONG = 10000
LIFETIME = 3
FAN_REACH = 6
HEADINGS = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
BETA_CONTENT = 3
BETA_CHARGE = -CHARGE * PROTON
PRODUCTS = [["beta", 1, BETA_CONTENT], ["nu", 1, 0]]
# J1: the lattice and the shell.
J1_SIDE = 41
J1_PITCH = 4
J1_PER_AXIS = 4
J1_SHELL = 18
J1_SOURCE = 4096
J1_TICKS = 650
# J3: series I's cube and the shell.
J3_SIDE = 21
J3_WIDTH = 1 << 28
J3_SHELL = 8
J3_TICKS = 700
J3_FREE_TICKS = 600
# The warm run without `become` that reads the crowd of each clock: its
# length and the dwell period over which the count's range is taken (the
# lesson of the first registration, 2026-09-20, and the re-pin of
# 2026-09-21: the count a clock reads under a fan's dwells is not one
# number over its history; the transient is over by tick 36 (the farthest
# line-mate's rows arrive by tick 21, the fan's by 18) and the window holds
# more than one cycle of the owed count, 2^20 / c intervals at c = 27585).
WARM_TICKS = 120
DWELL = (61, 120)
# The W world: the W's content per unit, the neutron's key and the run.
W_CONTENT = 3
W_AT = 8
W_TICKS = 16
W_LABEL = 64 * W_CONTENT
EXPECTATIONS_FORMAT = "weak-expectations-v1"


def fan(reach: int) -> list[tuple[int, int, int]]:
    """Every primitive direction (a, b, c) with 1 <= |a| + |b| + |c| <=
    reach, in a fixed order (290 for the reach 6, the six headings among
    them)."""
    found = []
    for a in range(-reach, reach + 1):
        for b in range(-reach, reach + 1):
            for c in range(-reach, reach + 1):
                size = abs(a) + abs(b) + abs(c)
                if 0 < size <= reach and math.gcd(math.gcd(abs(a), abs(b)), abs(c)) == 1:
                    found.append((a, b, c))
    found.sort()
    return found


def shell_nodes(centre: tuple[int, int, int], radius: int, side: int) -> list[list[int]]:
    """The Nodes at Euclidean distance within a half Link of `radius` from
    the centre (the register's shell), inside the cube."""
    found = []
    for x in range(side):
        for y in range(side):
            for z in range(side):
                d = math.dist((x, y, z), centre)
                if abs(d - radius) < 0.5:
                    found.append([x, y, z])
    return found


# -- J2 -----------------------------------------------------------------------------


def first_arrival_age(distance: int) -> int:
    """The age at which a heading ray first reaches `distance` Links, off
    the engine's flight table (a GameBoard computation of the expectation)."""
    table = direction_flight(((0, 0, 0), (0, 0, 0), PLUS_X))
    ages = np.arange(1, 4 * distance + 64, dtype=np.int64)
    steps = table.manhattan_steps(np.full(ages.shape, 2, dtype=np.int64), ages)
    return int(ages[np.flatnonzero(steps >= distance)[0]])


def reader(x: int, setting: int | None, width: int | None) -> Json:
    entry: Json = {"rule": "measure"}
    if setting is not None:
        entry["phase_window"] = setting
    if width is not None:
        entry["phase_width"] = width
    return {"position": [x, 0, 0], "family": "d", "amount": 1, "fixed": True, "table": {"nu": entry}}


def j2_world(name: str, clock: int, centres: list[int], width: int | None) -> Json:
    return {
        "law": "beam",
        "model_id": f"beam-weak-{name}-v1",
        "shape": [BAR, 1, 1],
        "boundary": "open",
        "ticks": J2_TICKS,
        "K": clock,
        "N": N,
        "release": [1, K_STRIDE_1],
        "suspension": 0,
        "families": [{"name": "nu", "quantum": 0}, {"name": "d", "quantum": 1, "phase": False}],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "nu",
                "amount": SOURCE_CONTENT,
                "phase": 0,
                "fixed": True,
                "directions": [list(PLUS_X)],
            },
            *(reader(x, centre, width) for x, centre in zip(READERS, centres, strict=True)),
            reader(FAR, None, None),
        ],
    }


def j2_worlds() -> dict[str, Json]:
    zeros = [0] * len(READERS)
    ones = [1] * len(READERS)
    ladder = [x % N for x in READERS]
    return {
        "j2_filter": j2_world("j2_filter", K_STRIDE_1, zeros, 1),
        "j2_ladder": j2_world("j2_ladder", K_STRIDE_1, ladder, 1),
        "j2_default": j2_world("j2_default", K_STRIDE_1, zeros, None),
        "j2_stride2": j2_world("j2_stride2", K_STRIDE_2, zeros, 1),
        "j2_stride2_odd": j2_world("j2_stride2_odd", K_STRIDE_2, ones, 1),
    }


def j2_expectations() -> dict[str, dict[str, int]]:
    """The expected counts of series J2 from the flight table: the first
    reader's arrivals over the run, the far detector's clicks per world."""
    born_first = J2_TICKS - first_arrival_age(READERS[0])
    born_far = J2_TICKS - first_arrival_age(FAR)
    stride_1 = [(t - 1) % N for t in range(1, born_far + 1)]
    stride_2 = [(2 * (t - 1)) % N for t in range(1, born_far + 1)]
    return {
        "j2_filter": {
            "first_arrivals": born_first,
            "first_clicks": born_first // N,
            "far": sum(1 for p in stride_1 if p != 0),
        },
        "j2_ladder": {"first_arrivals": born_first, "first_clicks": born_first // N, "far": 0},
        "j2_default": {
            "first_arrivals": born_first,
            "first_clicks": born_first // 2,
            "far": sum(1 for p in stride_1 if 16 <= p < 48),
        },
        "j2_stride2": {
            "first_arrivals": born_first,
            "first_clicks": born_first // 32,
            "far": sum(1 for p in stride_2 if p != 0),
        },
        "j2_stride2_odd": {"first_arrivals": born_first, "first_clicks": 0, "far": born_far},
    }


# -- J1 and J3 -----------------------------------------------------------------------


def nucleon_families(with_source: bool = False) -> list[Json]:
    found: list[Json] = [
        {"name": "p", "quantum": 0, "charge": CHARGE, "phase": False},
        {"name": "n", "quantum": 0, "phase": False},
        {
            "name": "nuclear",
            "quantum": 0,
            "columns": {"strong": {"value": STRONG, "sign": -1}},
            "lifetime": LIFETIME,
            "phase": False,
        },
        {"name": "beta", "quantum": 1, "charge": BETA_CHARGE},
        {"name": "nu", "quantum": 0},
        {"name": "d", "quantum": 1, "phase": False},
    ]
    if with_source:
        found.append({"name": "s", "quantum": 0, "phase": False})
    return found


def passing(names: list[str]) -> Json:
    return {name: "pass" for name in names}


def shell(
    centre: tuple[int, int, int], radius: int, side: int, families: list[str]
) -> tuple[list[Json], Json]:
    """The shell's measured events of `d` (passing every family but `beta`,
    whose click carries the age moment) and the one `beam` detector set."""
    nodes = shell_nodes(centre, radius, side)
    table: Json = {**passing(families), "beta": {"rule": "measure", "reads": "age"}}
    events = [
        {"position": node, "family": "d", "amount": 1, "fixed": True, "table": table} for node in nodes
    ]
    detector: Json = {"name": "shell", "positions": nodes, "threshold": 1, "reading": "beam"}
    return events, detector


def neutron(position: tuple[int, int, int], become: Json | None, table: Json, fixed: bool) -> Json:
    """A J1 neutron: 1839 of `n`, no strong unit (the pitch is beyond the
    lifetime's reach and the border's clicks would fill the record)."""
    found: Json = {
        "position": list(position),
        "family": "n",
        "amount": NEUTRON,
        "fixed": fixed,
        "table": table,
    }
    if become is not None:
        found["become"] = become
    return found


def j1_world(name: str, with_source: bool, become: bool = True) -> Json:
    centre = (J1_SIDE // 2,) * 3
    offsets = [J1_PITCH * (k - (J1_PER_AXIS - 1) / 2) for k in range(J1_PER_AXIS)]
    positions = [
        (int(centre[0] + a), int(centre[1] + b), int(centre[2] + c))
        for a in offsets
        for b in offsets
        for c in offsets
    ]
    passed = ["n", "nuclear", "beta", "nu", "p"] + (["s"] if with_source else [])
    trigger: Json | None = {"at": AT, "into": "p", "products": PRODUCTS} if become else None
    neutrons = [neutron(position, trigger, passing(passed), True) for position in positions]
    measured: list[Json] = list(neutrons)
    directions = fan(FAN_REACH)
    declared = [list(v) for v in directions if v not in HEADINGS]
    if with_source:
        measured.append(
            {
                "position": list(centre),
                "family": "s",
                "amount": J1_SOURCE,
                "fixed": True,
                "directions": list(range(2, 8 + len(declared))),
                "table": passing(["n", "nuclear", "beta", "nu", "p"]),
            }
        )
    events, detector = shell(
        centre, J1_SHELL, J1_SIDE, ["p", "n", "nuclear", "nu"] + (["s"] if with_source else [])
    )
    measured.extend(events)
    return {
        "law": "beam",
        "model_id": f"beam-weak-{name}-v1",
        "shape": [J1_SIDE] * 3,
        "boundary": "open",
        "ticks": J1_TICKS,
        "K": K,
        "N": N,
        "release": [1, 1],
        "suspension": SUSPENSION,
        "directions": declared,
        "families": nucleon_families(with_source),
        "measured": measured,
        "detectors": [detector],
    }


def nucleon(
    family: str, position: tuple[int, int, int], become: Json | None, whole_fan: list[int]
) -> Json:
    body: Json = {
        "position": list(position),
        "family": family,
        "amount": PROTON if family == "p" else NEUTRON,
        "held": {"nuclear": 1},
        "fixed": False,
        "directions": whole_fan,
        "table": passing(["beta", "nu"]),
    }
    if become is not None:
        body["become"] = become
    return body


def j3_world(name: str, with_proton: bool, crowd: int | None, ticks: int, become: bool = True) -> Json:
    c = J3_SIDE // 2
    directions = fan(FAN_REACH)
    declared = [list(v) for v in directions if v not in HEADINGS]
    whole_fan = list(range(2, 8 + len(declared)))
    trigger: Json | None = None
    if become:
        trigger = {"at": AT, "into": "p", "products": PRODUCTS}
        if crowd is not None:
            trigger["crowd"] = crowd
    bodies: list[Json] = []
    if with_proton:
        bodies.append(nucleon("p", (c, c, c), None, whole_fan))
        bodies.append(nucleon("n", (c + 1, c, c), trigger, whole_fan))
    else:
        bodies.append(nucleon("n", (c, c, c), trigger, whole_fan))
    events, detector = shell((c, c, c), J3_SHELL, J3_SIDE, ["p", "n", "nuclear", "nu"])
    return {
        "law": "beam",
        "model_id": f"beam-weak-{name}-v1",
        "shape": [J3_SIDE] * 3,
        "boundary": "open",
        "ticks": ticks,
        "K": K,
        "N": N,
        "release": [1, 1],
        "suspension": SUSPENSION,
        "width": J3_WIDTH,
        "directions": declared,
        "families": nucleon_families(),
        "measured": bodies + events,
        "detectors": [detector],
    }


def j1_worlds() -> dict[str, Json]:
    return {"j1_lattice": j1_world("j1_lattice", False), "j1_source": j1_world("j1_source", True)}


def j3_worlds() -> dict[str, Json]:
    return {
        "j3_deuteron": j3_world("j3_deuteron", True, None, J3_TICKS),
        "j3_deuteron_crowd": j3_world("j3_deuteron_crowd", True, 65536, J3_TICKS),
        "j3_neutron_free": j3_world("j3_neutron_free", False, None, J3_FREE_TICKS),
    }


# -- The W world -------------------------------------------------------------------


def w_families() -> list[Json]:
    return [
        {"name": "n", "quantum": 0, "phase": False},
        {"name": "p", "quantum": 0, "charge": CHARGE, "phase": False},
        {"name": "w", "quantum": 1, "charge": BETA_CHARGE, "lifetime": 1, "phase": False},
    ]


def w_world() -> Json:
    """The exchange at one Link: the neutron throws one W unit on +x at its
    key and the proton beside it measures it by the keys' rule."""
    return {
        "law": "beam",
        "model_id": "beam-weak-w_exchange-v1",
        "shape": [7, 1, 1],
        "boundary": "open",
        "ticks": W_TICKS,
        "K": K,
        "N": N,
        "release": [1, 1 << 20],
        "suspension": 0,
        "families": w_families(),
        "measured": [
            {
                "position": [2, 0, 0],
                "family": "n",
                "amount": NEUTRON,
                "fixed": True,
                "directions": [[1, 0, 0]],
                "become": {"at": W_AT, "into": "p", "products": [["w", 1, W_CONTENT]]},
            },
            {"position": [3, 0, 0], "family": "p", "amount": PROTON, "fixed": True},
        ],
    }


def w_worlds() -> dict[str, Json]:
    return {"w_exchange": w_world()}


def w_expectations() -> dict[str, dict[str, object]]:
    """The W world's integers (GAMEBOARD, from the rule: a row of lifetime 1
    is at one Link at the age 1, the label 64 x amount x content)."""
    return {
        "w_exchange": {
            "at": W_AT,
            "click_tick": W_AT + 1,
            "label": W_LABEL,
            "content": PROTON + W_CONTENT,
            "charge": [0, 1],
        }
    }


def count_ranges(document: Json) -> dict[int, tuple[int, int]]:
    """The range of the count each `n` clock reads at its Node over the
    dwell period (a GameBoard reading of the engine itself): the world run
    without its `become` keys for WARM_TICKS intervals, `Measured.counted`
    per neutron at every tick, its least and greatest value over the ticks
    DWELL[0] .. DWELL[1]. Until 2026-09-21 the one value at tick 100."""
    warm = json.loads(json.dumps(document))
    for entry in warm["measured"]:
        entry.pop("become", None)
    warm["ticks"] = WARM_TICKS
    simulation = NatureBeamSimulation(parse_nature_beam_world(warm))
    neutrons = [i + 1 for i, entry in enumerate(warm["measured"]) if entry["family"] == "n"]
    low = dict.fromkeys(neutrons, 0)
    high = dict.fromkeys(neutrons, 0)
    for tick in range(1, WARM_TICKS + 1):
        simulation.step()
        if tick < DWELL[0]:
            continue
        for number in neutrons:
            count = int(simulation.measured[number].counted)
            if tick == DWELL[0]:
                low[number] = high[number] = count
            else:
                low[number] = min(low[number], count)
                high[number] = max(high[number], count)
    return {number: (low[number], high[number]) for number in neutrons}


def trigger_tick(count: int) -> int:
    """The self-creation that takes a clock reading the constant count c to
    the age `at`: at + floor(at x c / 2^20) (the owed counts telescope); at
    the two ends of the count's range, the two ends of the trigger's."""
    return AT + (AT * count) // SUSPENSION[1]


def become_expectations(worlds: dict[str, Json]) -> dict[str, dict[str, object]]:
    found: dict[str, dict[str, object]] = {}
    for name, document in worlds.items():
        if name == "j3_deuteron_crowd":
            found[name] = {"ticks": {}, "never": True, "gate": 65536}
            continue
        ranges = count_ranges(document)
        ticks = {
            str(number): [trigger_tick(low), trigger_tick(high)]
            for number, (low, high) in ranges.items()
        }
        found[name] = {
            "counts": {str(number): [low, high] for number, (low, high) in ranges.items()},
            "ticks": ticks,
            "earliest": min(low for low, _ in ticks.values()),
            "latest": max(high for _, high in ticks.values()),
            "slack": 3,
            "dwell": list(DWELL),
            "warm_ticks": WARM_TICKS,
        }
    return found


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=HERE)
    parser.add_argument("--no-expect", action="store_true", help="skip the warm runs of J1 and J3")
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    print(
        f"J2: the bar {BAR} x 1 x 1, {len(READERS)} readers at x = {READERS[0]} .. {READERS[-1]}, "
        f"the far detector at {FAR}, {J2_TICKS} intervals; the first-arrival ages "
        f"{first_arrival_age(READERS[0])} at {READERS[0]} Links and {first_arrival_age(FAR)} at {FAR}"
    )
    # The expectations file declares a `format` (a world declares `law` and
    # never `format`): the tests that read every JSON under examples/events
    # as a world skip it, as they skip an entity definitions file.
    expectations: dict[str, object] = {"format": EXPECTATIONS_FORMAT, "j2": j2_expectations()}
    # The source of every entry (the owner's principle of 2026-09-21, record
    # 205: a formula gives, a run proves): the formula or the section of
    # docs/DERIVATIONS_BEAM.md, or "measured" with the target.
    expectations["derivations"] = {
        "j2": "the first arrivals from the flight table (the rows born by the ticks a heading row needs to walk 8 Links: ticks - tau_8, tau_k = ceil((2 k - 1) T_D / (2 S_1 Q)), DERIVATIONS_BEAM 11.1; BEAM_LAW section 3); the first clicks the arrivals' admitted share on the window (BEAM_LAW note 36: w / N for a stride coprime to N, else the admitted phases of the stride's orbit over the orbit's size: 1/64, the half circle, 2/64, 0); the far detector's clicks the rows of the stride outside the far phase; derived here from the flight table and compared by tests/test_weak_readings.py (d)",
        "become": f"measured, the range over the dwell period of ticks {DWELL[0]} to {DWELL[1]} of a warm run of {WARM_TICKS} intervals of the world without its `become` keys (the count each `n` clock reads at its Node, `Measured.counted`, at every tick of the window: the transient over by tick 36, the window longer than one cycle of the owed count, 2^20 / c intervals; a GameBoard reading of the engine, re-pinned under the fraction-free law on 2026-09-21, the one count at tick 100 until then); the trigger ticks at + floor(at x c / 2^20) at both ends of the range (the owed accumulator of BEAM_LAW note 41 gains between the least and the greatest count per interval once the crowd is steady), the reading inside when the neutron fires within them or up to `slack` intervals before (the build-up); `never` where the `crowd` gate holds; compared with the generator's warm runs on the shipped worlds by tests/test_weak_readings.py (e)",
        "w": "measured (the exchange world: `at` and the click's tick the clock's count under the crowd gate, the label Q x the amount, the content and the charge as declared)",
    }
    for name, j2_expected in j2_expectations().items():
        print(f"  {name}: expected (GAMEBOARD, from the flight table) {j2_expected}")
    worlds = {**j2_worlds(), **j1_worlds(), **j3_worlds(), **w_worlds()}
    for name, document in worlds.items():
        path = args.out / f"{name}.json"
        document = families_by_definition(document, FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)
    if not args.no_expect:
        become = become_expectations({**j1_worlds(), **j3_worlds()})
        expectations["become"] = become
        for name, expected in become.items():
            if expected.get("never"):
                print(f"  {name}: expected never to fire (the count above the gate {expected['gate']})")
                continue
            counts = expected["counts"]
            assert isinstance(counts, dict)
            lows = sorted({low for low, _ in counts.values()})
            highs = sorted({high for _, high in counts.values()})
            print(
                f"  {name}: {len(counts)} clocks, the counts over the ticks {DWELL[0]} .. {DWELL[1]} "
                f"from {lows[0]} to {highs[-1]} ({len(set(map(tuple, counts.values())))} distinct ranges), "
                f"the trigger ticks {expected['earliest']} .. {expected['latest']} "
                f"(each up to {expected['slack']} earlier by the build-up)"
            )
    expectations["w"] = w_expectations()
    for name, w_expected in w_expectations().items():
        print(f"  {name}: expected (GAMEBOARD, from the rule) {w_expected}")
    (args.out / "expectations.json").write_text(
        json.dumps(carry_replicated(args.out / "expectations.json", expectations), indent=1) + "\n",
        encoding="utf-8",
    )
    print(args.out / "expectations.json")


if __name__ == "__main__":
    main()
