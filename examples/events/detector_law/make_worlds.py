"""The world files of the detector law's rows written through the generator (the Boss's
order of 2026-09-24: every number of a file is its declaration's; where a declaration lacks
a line the file needs, the key is ABSENT and the loader's refusal names it, never a number
of the writer's own). The engine's keys are the massive record kind's (`../massive_record/
make_worlds.py`, whose `world` helper writes the massive worlds here, so that their form is
that series' form byte for byte: `age_bound`, `K`, `N`, `release`, the blocks' keys), the
bodies with extents and the face slab (BUILD.md section 26 item 23), the emitter as a
clicking body (item 24) and THE GIVEN TRAIN (item 27; ALGEBRA.md 9.17 (6a)): every giving is
a travelling train of 8 periods on the given clock [512, 1] of N = 1024 (k = pi / 2, the
wavelength 4, the train 32 Nodes along **K**), the body's extent along **K** the train's
length, the profile and its norm on the vacuum the generator's integers checked at load.

THE LIGHT CLOCK (ALGEBRA.md 9.22 (8), its row; the one table of 9.30: the chain of 760
extruded to [760, 3, 3], periodic on y and z, so that every detector is a whole cube and
every pin of the chain stands to the bit): light [1, 1] with the given clock [512, 1] on
N = 1024, matter [800, 809]; the face slabs 32 deep at both ends of x (`face_depth`); the
well A [800, 801] of the extents [32, 3, 3] at [600, 632) with a stock of
64, its train along +x; the mirror the gap [1, 2] of depth 4 at [690, 694) (a body of
light's kind over the whole cross-section; the holder body's name waits on the cleanup's
step 6); the receiving set `at_well` A's own Nodes (the set bound to the block: the
outgoing train leaves them through their Ports, negative and not booked, the return enters
them, 9.25 (11) (d)); 4800 intervals (COMPUTATION: 64 givings at the mean cadence P / 2 on
the wheel of 2403, P = 94 on A's mode, about 3000 intervals, the last return 300, a margin;
the run 9 seconds, HOST). The blind
pins in `../pins.json`: the mean click interval after the giving 300 +- 9 at 64 records
(the passage's mean (2 x 58 + 16 + 2) / 0.44721 = 299.7, the rms 24.8, the band 3 rms /
sqrt 64) and the stock's first click 250 +- 8; the 214 +- 1 of the chain of 674 with the
cube beside A is HISTORY (BUILD.md section 26 item 22: a cube beside the emitter books the
outgoing pass).

THE ROWS HELD UNDER THE TRAIN (their files in `docs/designs/detector_law/held_worlds/`,
HISTORY as written with the one-Node giving, not loaded by the gate; their builders retired
here, to be rebuilt through the generator from the table of ALGEBRA.md 9.22 (8) in its
form, the cleanup's item 7): the two slits and the pace fans (the light rows of the folder);
the moving emitter's redshift, Sagnac's two-way light times, de Broglie's fringes and the
moving mass's energy (the massive rows written into `../massive_record/`); the four Bell
and the four Malus worlds held before them (HELD_NAMES below: the crystal and the polariser
body with an axis).

Run from the repository root:

    PYTHONPATH=src python examples/events/detector_law/make_worlds.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
EVENTS = HERE.parent
MASSIVE = EVENTS / "massive_record"
DESIGNS = HERE.parents[2] / "docs" / "designs"
NEW_ROWS = DESIGNS / "new_rows" / "worlds"
# The worlds whose declared lines the engine on main does not carry yet (section 15: the
# path for a block of light's kind, `emits` without held content, the receiver sets' own
# wheel, the closed face, the matter lamp and its clock key, the raised pair and the take
# on the massive kind, the amplitude bound key). They are written beside the declarations,
# not under `examples/events` (the shipped set, which the gate loads), until their lines
# land; then their names move back (the Boss's rule of 2026-09-24, 02:15Z: nothing shipped
# that the gate loads and refuses).
HELD = DESIGNS / "detector_law" / "held_worlds"
# Empty since PR 1118's merge (main 1454030f): the margin rule skips a silent block (seed
# 0, no record of its own), so the matter layer worlds' absorbing take lines of the matter
# kind at the kind's own pair are no longer refused as a mode that is not bound, and the
# two files are back at their RUN_LIST path (the Boss's word of 2026-09-24, 10:16Z).
# The four Bell files are HELD until the crystal (branch `crystal`, BUILD.md section 25):
# their two-arm lamp is cancelled and refused at load (ALGEBRA.md 9.17; the model owner's
# word of 2026-09-24, 15:05Z); the crystal's branch regenerates them through the crystal
# at the wheel [1, 20] (the Boss's adoption of 00:05Z).
# THE ROWS HELD UNDER THE GIVEN TRAIN (BUILD.md section 26 item 27) are moved there as
# files (the module docstring); their builders are retired, not held: nothing here writes
# them.
HELD_NAMES: set[str] = {
    "bell_a0b0",
    "bell_a0b1",
    "bell_a1b0",
    "bell_a1b1",
    # the four Malus worlds held with them (BUILD.md section 26 item 14): under
    # the cumulative ladder of ALGEBRA.md 9.19 (3) (b) the table body's two
    # detectors at ONE Node cannot give Malus's counts (the entry's whole offer
    # crosses the rung no later than the + share of it), so the polariser
    # returns as a body with an axis and two receivers named (the
    # mathematician's step 3), the counts re-derived on it
    "malus_45",
    "malus_11.25",
    "malus_28.125",
    "malus_33.75",
}


def load_massive_generator():
    """The massive record series' generator (its `world` helper and its constants)."""
    path = MASSIVE / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("massive_record_make_worlds", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["massive_record_make_worlds"] = module
    spec.loader.exec_module(module)
    return module


# The first build's chain world (`tests/test_detector_law.py::chain_world`), the
# template of every ray-law world: its world keys; the light clocks of section 15
# (the pair on N = 64 per wavelength in Links).
TEMPLATE_KEYS = {
    "law": "beam",
    "K": 1073741824,
    "N": 64,
    "release": [1, 128],
    "suspension": 0,
    "clock_stamp": True,
    "detector_law": True,
    "directions": [],
}
WALL_PAIR = [1, 2]  # the mirror line's block pair, two Nodes deep (section 15 L-1, the fourth commit)
TRAIN_32 = 32  # periods, section 15 L-3 and L-6 (HISTORY: the lamp's train, retired)
# THE EMITTER AS A CLICKING BODY (ALGEBRA.md 9.17 (4); BUILD.md section 26): every source is a
# body of a massive kind (the emitter kind EMITTER_KIND, the vacuum pair of the matter kind)
# of side 1, seeded on its bound mode by the massive generator's `seed_on_the_mode`, with a
# stock of excitations and a wheel; each excitation clicks at its own rung and writes its
# photon once. THE WELL'S MODE SETS THE CADENCE (COMPUTATION, BUILD.md section 26): the u-th
# residue clicks about (2 u + 1) P / (2 W) intervals after its excitation, P the mode's
# period (ALGEBRA.md 9.17 (5) item 1 on the flux norm of 9.19 (3)), the whole wheel of W
# in about W P / 2; a well too deep for its board is a RUNAWAY (the
# largest eigenvalue at or above 2, no oscillation; the deep wells [800, 700], [800, 500]
# and [800, 400] of the first smoke runs were such on a chain and their cadences the
# runaway's, withdrawn) and the margin rule refuses it. The one-Node well EMITTER_WELL on
# the kind EMITTER_KIND (the index worlds' kind, omega_0 = 0.505) is bound on a chain
# (omega_b = 0.32, P = 20 intervals) and on a layer (omega_b = 0.50, P = 12
# intervals). A world of W givings declares the stock M = W (LAB_TOOLS.md A.1).
EMITTER_KIND = [7, 8]
EMITTER_WELL = [
    801,
    700,
]  # the rich well (700 remainder values, ALGEBRA.md 9.19 (4a), 9.22 (4)) bound on a chain and a layer
EMITTER_SEED_AMPLITUDE = (
    1 << 20
)  # at 100 the given light's back-action swamps the excited record (ALGEBRA.md 9.17 (7) (c))
BELL_TRAIN = 128  # periods, DECLARATIONS.md sections 1 and 3
# The receiver by name (#1116, the physicist's form, Reviewer 3 confirmed): a key `receiver`
# on every emitting block naming the set that takes the block's clicks. ON since the
# builder's engine line is on main (the receiver by name, DECLARATIONS.md section 13 item
# 7; the loader requires the key on an emitting block) and the owner's word of 2026-09-24
# (the Engine Fixer's line 6: the generator's emitter writes `receiver`); the flag is kept
# as the record of the held form.
RECEIVER_KEY = True


def light_family(pair: list[int] | None) -> dict:
    family: dict = {"name": "light", "quantum": 1, "charge": 0}
    if pair is not None:
        family["phase_per_link"] = pair
    return family


def ray_world(name: str, shape: list[int], boundary: dict, pair: list[int], ticks: int) -> dict:
    document: dict = {"law": "beam", "model_id": f"beam-detector-law-{name}-v1", "shape": shape}
    document["boundary"] = boundary
    document["ticks"] = ticks
    document.update({key: value for key, value in TEMPLATE_KEYS.items() if key != "law"})
    document["massive_record"] = True  # the absorbing blocks and the `probes` key live under it
    document["amplitude_bound"] = AMPLITUDE_BOUND  # the emitter body's massive family (M1-10)
    document["node_clock"] = NODE_CLOCK  # the Node clock Gamma (item 31)
    document["clock_family"] = CLOCK_FAMILY_NAME  # the family of clicks (item 32)
    document["charge_family"] = CHARGE_FAMILY_NAME  # the family of charge (item 35)
    document["charge_strength"] = CHARGE_STRENGTH
    document["families"] = [
        light_family(pair),
        emitter_kind_family(),
        dict(CLOCK_FAMILY),
        dict(CHARGE_FAMILY),
    ]
    document["measured"] = []
    document["detectors"] = []
    return document


def emitter_kind_family(name: str = "matter") -> dict:
    """The emitter bodies' massive family (the kind EMITTER_KIND, no clock)."""
    return {"name": name, "quantum": 1, "pair": list(EMITTER_KIND), "charge": 0}


def emitter_body(
    position: list[int],
    stock: int,
    receiver: list[str] | None = None,
    family: str = "light",
    own: str = "matter",
    pair: list[int] | None = None,
) -> dict:
    """An emitter body (ALGEBRA.md 9.17 (4); BUILD.md section 26): a well of the massive
    family `own` of side 1 at `position` (its seed the scalar EMITTER_SEED_AMPLITUDE, made the
    mode's profile by `seed_on_the_mode` once the document is complete), its stock `stock`
    excitations, its `emitter` the given family (the residue and the wheel the law's) and,
    with `receiver`, the given records' ladder by name (the sets named; the lamp's `receiver`
    of old, written only under RECEIVER_KEY) (no coupling: the coupling is the click alone, the model owner's decision (2) of record 1962)."""
    emitter: dict = {"family": family}
    if receiver is not None and RECEIVER_KEY:
        emitter["receiver"] = list(receiver)
    return {
        "position": position,
        "family": own,
        "amount": stock,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "side": 1,
        "pair": list(pair or EMITTER_WELL),
        "seed": EMITTER_SEED_AMPLITUDE,
        "margin": "control",
        "emitter": emitter,
    }


def body(position: list[int], family: str = "light", directions: list[list[int]] | None = None) -> dict:
    """A fixed body of one Node (the template's receiver form)."""
    entry: dict = {
        "position": position,
        "family": family,
        "amount": 1,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
    }
    if directions is not None:
        entry["directions"] = directions
    return entry


def wall_node(position: list[int], family: str = "light", pair: list[int] | None = WALL_PAIR) -> dict:
    """One Node of a wall: a block of side 1 with the pair [1, 2] (section 15 L-1 the
    mirror line of light's kind; M1-6 the barrier line of the matter kind, its raised pair
    the builder's line). The take lines (`absorbing` blocks with a `take` pair) are retired
    with the take (ALGEBRA.md 9.19 (3); BUILD.md section 26 item 15)."""
    entry = body(position, family)
    entry["side"] = 1
    if pair is not None:
        entry["pair"] = list(pair)
    return entry


def wall_line(
    xs: list[int], ys: range, openings: set[int], family: str = "light", pair=WALL_PAIR
) -> list[dict]:
    """A wall of the declared depth: one block per Node of the columns `xs`, the openings
    free in every column."""
    return [wall_node([x, y, 0], family, pair) for x in xs for y in ys if y not in openings]


DETECTOR_SIDE = 3  # the detector cube's side (the model owner's word of 2026-09-25, record 1899)


def cube_positions(document: dict, corner: list[int]) -> list[list[int]]:
    """The Nodes of a detector cube of side DETECTOR_SIDE from its lower corner, cut by the
    GameBoard on an axis of extent below the side (a chain's or a layer's thin axis), as
    the loader's check reads it (`_detector_region` of the world loader)."""
    shape = document["shape"]
    return [
        [corner[0] + dx, corner[1] + dy, corner[2] + dz]
        for dx in range(min(DETECTOR_SIDE, shape[0]))
        for dy in range(min(DETECTOR_SIDE, shape[1]))
        for dz in range(min(DETECTOR_SIDE, shape[2]))
    ]


def receiver_cube(document: dict, name: str, corner: list[int], family: str = "light") -> str:
    """ONE DETECTOR (record 1899): a cube of side DETECTOR_SIDE of receiver bodies of the
    family from `corner`, read as the one set `name` (its sensitivity its whole cube, the
    flux into it through its Ports from outside; the click the detector's, reported by its
    name and never by a Node). The name is returned."""
    positions = cube_positions(document, corner)
    for position in positions:
        document["measured"].append(body(position, family, [[-1, 0, 0]]))
    document["detectors"].append({"name": name, "positions": positions, "threshold": 1})
    return name


def screen(document: dict, x: int, ys: range, family: str = "light") -> list[str]:
    """A screen as a row of cube detectors `screen_<y>` (record 1899): from the column x,
    DETECTOR_SIDE deep, one cube per DETECTOR_SIDE rows of `ys` (whose count must divide),
    each with its own click (section 12; Builder 2's finding); the rung's wheel is the
    record's own (ALGEBRA.md 9.22 (4)). The sets' names are returned, the emitter's
    `receiver` list (its records' ladder)."""
    assert len(ys) % DETECTOR_SIDE == 0, (ys, DETECTOR_SIDE)
    return [
        receiver_cube(document, f"screen_{y}", [x, y, 0], family)
        for y in range(ys.start, ys.stop, DETECTOR_SIDE)
    ]


def lamp(
    position: list[int],
    amount: int,
    rate: list[int],
    wheel: list[int],
    directions: list[list[int]] | None,
    train: int,
    family: str = "light",
    receiver: list[str] | None = None,
) -> dict:
    """The lamp in the template's form (the matter lamp's frequency is its family's
    `phase_per_link`, section 15 M1-6, not a lamp key); with `receiver`, the names of
    the sets that are its records' ladder (the lamp's ladder by name, SIZING.md; the
    engine's `receiver` on a lamp, BUILD.md section 20), written only under
    RECEIVER_KEY. With `directions` None the lamp declares NO HEADING (Reviewer 3's
    second reading of 2026-09-24, 16:25Z, on the owner's standard: a heading should
    arise; the loader's default is the six headings, an isotropic emitter; the beam's
    shape is the mask's and the split's work), the form of the two slits and the pace
    fans since the no-heading regeneration."""
    entry: dict = {
        "position": position,
        "family": family,
        "amount": amount,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
    }
    inner: dict = {"rate": rate, "wheel": wheel}
    if directions is not None:
        entry["directions"] = directions
        inner["directions"] = directions
    inner["train"] = train
    if receiver is not None and RECEIVER_KEY:
        inner["receiver"] = list(receiver)
    entry["lamp"] = inner
    return entry


# Group L: the light rows.


# Group T: the table rows.

BELL_N2048_LABEL_SCALE = (
    15728640  # the label scale of the Bell worlds at N = 2048 (`amplitude/bell_n2048_*.json`)
)
BELL_N2048_RELEASE = [1, 67108864]
BELL_N2048_STOCK = (
    15728642  # the stock of the Bell worlds at N = 2048 (HISTORY: the amplitude law's lamp)
)
# Section 2 item 8: a Bell world counts EXACTLY W = 2048 givings (under the seed order more
# than W givings repeat the order), and the lamp's stock of records is its `amount` (one
# quantum per giving, the engine's `_givings`), so the stock is W; the L3 series' stock
# would giving one record per interval to the end (the preview on 299b6bb2: 3433 givings by
# the interval 3433).
BELL_STOCK = 2048
BELL_N = 2048
BELL_CLOCK = [2464, 25]  # section 14 item 1: the 12-Link clock [77, 25] on 64 scaled by 32 to N = 2048
MALUS_CLOCK = [308, 25]  # section 14 item 1: the same clock on N = 256
BELL_BRANCHES = [[0, 1], [3, 1]]
BELL_SETTINGS = {"a0": 0, "a1": BELL_N // 4, "b0": BELL_N // 8, "b1": 3 * BELL_N // 8}
# Section 2 item 8 (the loader's keys): under `residue_order` "seed" a Bell world counts
# exactly W = 2048 givings at the rate [1, 1] (2048 intervals), so its `ticks` is at least
# W / rate + the far arm's transit + the completion (Reviewer 3's margin line). The engine
# ends a train at the first clock zero after the declared periods: on the clock [2464, 25]
# at N = 2048 the 128 periods (2660 intervals) end at 3200 (the giving line's `train` on
# 299b6bb2), and every record completed 3204 intervals after its giving in the preview
# (the last, given 2048, at 5252); the far polariser 7 Links from the lamp is 12.1 intervals
# at c = 1 / sqrt 3: 2048 + 3204 + 13 = 5265; written 5500, the margin 235 intervals.
BELL_TICKS = 5500
MALUS_TRAIN = 32  # periods (665 intervals on [308, 25]), section 5 item 2, 2026-09-24 06:05Z
MALUS_TICKS = 3800  # 256 excitations on the well [8, 7]: the wheel in about W P / 2 = 2560 intervals (ALGEBRA.md 9.17 (5) item 1); the engine reads 239 givings within 3200 on the flux norm of 9.19 (3), COMPUTATION; the transit 6 and the completion beside
# Section 5 item 2, "the count of 256 givings stands": the lamp's stock of records is its
# `amount` (a giving spends one quantum of it, the engine's `_givings`; two_slits's stock 1024
# the same key), so the registered 2^50 would giving one record per interval to the end of
# the 1200 (the preview on 299b6bb2: 1200 givings); the declared count is written as the stock.
MALUS_BIRTHS = 256
MALUS_SHAPE = [8, 1, 1]  # section 5 item 1 (12:15Z): the exit Node at x = 7 on the board
MALUS_READ_NODE = [4, 0, 0]  # the registered which-path read body, dropped with its set
MALUS_READ_SET = "first"


def bell(a: str, b: str) -> dict:
    """DECLARATIONS.md sections 1 and 2: the bar of 21 x 1 x 1 (x open, y and z periodic),
    N = 2048, the pair lamp at x = 10 with two arms and the joint labels 00 and 11, the
    train 128, the polarisers at x = 7 (Alice) and 17 (Bob) with their settings, each a
    detector set of one Node reading `sum`; the givings in the seed-set order (section 2
    item 8: `residue_order` "seed", the world's own `residue_seed`, the stock 2048 = W
    givings), 5500 intervals (BELL_TICKS); the clock
    [2464, 25] on the light family and [1, 1] on the counter family (section 1 item 3 and
    section 15 T-1)."""
    return {
        "law": "beam",
        "model_id": f"beam-detector-law-bell-{a}{b}-v1",
        "shape": [21, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": BELL_TICKS,
        "K": BELL_N2048_LABEL_SCALE,
        "N": BELL_N,
        "release": BELL_N2048_RELEASE,
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "families": [
            light_family(BELL_CLOCK),
            {"name": "counter", "quantum": 1, "phase_per_link": [1, 1], "charge": 0},
        ],
        "measured": [
            {
                "position": [10, 0, 0],
                "family": "light",
                "amount": BELL_STOCK,
                "phase": 0,
                "fixed": True,
                "lamp": {
                    "rate": [1, 1],
                    "directions": [[1, 0, 0], [-1, 0, 0]],
                    "arms": 2,
                    "branches": BELL_BRANCHES,
                    "train": BELL_TRAIN,
                },
            },
            {
                "position": [7, 0, 0],
                "family": "counter",
                "amount": 1,
                "fixed": True,
                "table": {"light": {"phase_window": BELL_SETTINGS[a]}},
            },
            {
                "position": [17, 0, 0],
                "family": "counter",
                "amount": 1,
                "fixed": True,
                "table": {"light": {"phase_window": BELL_SETTINGS[b]}},
            },
        ],
        "detectors": [
            {"name": "alice", "positions": [[7, 0, 0]], "threshold": 1, "reading": "sum"},
            {"name": "bob", "positions": [[17, 0, 0]], "threshold": 1, "reading": "sum"},
        ],
    }


def malus(name: str, source: Path, setting: int) -> dict:
    """DECLARATIONS.md sections 5 and 6: the registered form of the source world with
    `detector_law` true, `clock_stamp` true, the table's `phase_window` at the declared
    setting, ON THE BAR OF 8 (section 5 item 1, 12:15Z, Reviewer 3's read of the 7-Node
    files: the polariser's exit Node, the Node beyond its entry at x = 6, on the board at
    x = 7) WITHOUT the which-path `read` body at x = 4 and its set `first` (dropped there:
    under detector-law-v1 a set's Node is a take Node, so that set took the record before
    the polariser), the polariser's set alone on its entry Node (the table body of two
    detectors, section 14 item 6), the clock [308, 25] on N = 256 (section 14 item 1) on the light family and
    [1, 1] on the counter family (section 5 item 3 and section 15 T-1), written in the
    file (the registered entity references carry no clock); the lamp's train 32 periods
    and `ticks` 1200 (section 5 item 2, 2026-09-24: the registered 300 intervals gave 300
    givings and no click, a gather line written only at completion), the lamp's stock
    `amount` 256 (the count of 256 givings)."""
    document = json.loads(source.read_text(encoding="utf-8"))
    document = copy.deepcopy(document)
    rebuilt: dict = {"law": "beam", "model_id": f"beam-detector-law-{name}-v1"}
    for key, value in document.items():
        if key in ("law", "model_id", "entity_definitions", "entities", "families"):
            continue
        if key == "shape":
            assert value == [7, 1, 1], value
            value = list(MALUS_SHAPE)
        rebuilt[key] = MALUS_TICKS if key == "ticks" else value
        if key == "suspension":
            rebuilt["clock_stamp"] = True
            rebuilt["detector_law"] = True
    rebuilt["families"] = [
        light_family(MALUS_CLOCK),
        {"name": "counter", "quantum": 1, "phase_per_link": [1, 1], "charge": 0},
        emitter_kind_family(),
    ]
    rebuilt["massive_record"] = True
    rebuilt["amplitude_bound"] = AMPLITUDE_BOUND
    rebuilt["node_clock"] = NODE_CLOCK
    rebuilt["measured"] = [
        entry for entry in rebuilt["measured"] if entry["position"] != MALUS_READ_NODE
    ]
    rebuilt["detectors"] = [
        detector for detector in rebuilt["detectors"] if detector["name"] != MALUS_READ_SET
    ]
    assert len(rebuilt["measured"]) == 2 and len(rebuilt["detectors"]) == 1, name
    for index, entry in enumerate(rebuilt["measured"]):
        table = entry.get("table", {}).get("light")
        if isinstance(table, dict) and "phase_window" in table:
            table["phase_window"] = setting
        inner = entry.get("lamp")
        if isinstance(inner, dict):
            # the source's lamp becomes the emitter body (ALGEBRA.md 9.17): the
            # stock 256 = W on the lamp's declared wheel, the well EMITTER_WELL
            # (bound on the periodic bar of 8: the extent 1.4 Links)
            rebuilt["measured"][index] = emitter_body(list(entry["position"]), MALUS_BIRTHS)
    return rebuilt


def table_worlds(massive) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for a in ("a0", "a1"):
        for b in ("b0", "b1"):
            out[f"bell_{a}{b}"] = bell(a, b)
    # THE MALUS FOUR STAND HELD AS WRITTEN (their files of the head ead580df in
    # held_worlds): under the detector cube (record 1899) their one-Node set
    # `second` on the bar of 8 is refused at load, and the polariser returns as
    # a body with an axis and two cube receivers when the worlds are rebuilt
    # (the cleanup order's step 6); `malus` above is that rebuild's material.
    return out


# Group M1: the massive rows, in the massive record series' form.

KIND = [800, 809]  # mu = 0.15
WELL_FULL = [
    800,
    801,
]  # the rich well of the massive rows' emitters (2403 remainder values; the mathematician's 9.21 (8))
EMITTER_SEED = (
    50 << 12
)  # the seed's unit 2^12 under the amplitude bound 2^20 (ALGEBRA.md 9.61 (3); item 44; 50 x 2^20 HISTORY)
AMPLITUDE_BOUND = (
    1 << 20
)  # the world key `amplitude_bound` of every massive world: the ceiling under the Node clock (BUILD.md section 26 item 31; section 15 M1-10's 2^32 HISTORY)
NODE_CLOCK = 10_000  # the world key `node_clock`, Gamma = 10^4 (ALGEBRA.md 9.57 (2), 9.61 (3); item 44) (ALGEBRA.md 9.35 (3); item 31): the massive generator's integer, written in every world
CLOCK_FAMILY_NAME = "clicks"  # the family of clicks, the Node clock (ALGEBRA.md 9.45; item 32): the massive generator's name and family
CLOCK_FAMILY = {"name": CLOCK_FAMILY_NAME, "quantum": 1, "charge": 0}
CHARGE_FAMILY_NAME = "charge"  # the family of charge (ALGEBRA.md 9.48; item 35)
CHARGE_FAMILY = {"name": CHARGE_FAMILY_NAME, "quantum": 1, "charge": 0}
CHARGE_STRENGTH = 1  # Lambda; every registered family's charge is 0
EMITTER_STOCK = (
    64  # the massive rows' emitters: 64 excitations on the wheel [1, 64] (BUILD.md section 26)
)
PHASE_STEPS = 1024  # N of every light world (ALGEBRA.md 9.22 (8): the given clock's circle)
GIVEN_CLOCK = [
    512,
    1,
]  # the given clock of every light emitter on N = 1024: k = pi / 2, the wavelength 4
TRAIN_PERIODS = 8  # the train's periods (9.17 (6a))
TRAIN_LENGTH = 32  # the train's Nodes along K, TRAIN_PERIODS x the wavelength 4
FACE_DEPTH = 32  # every face a receiver slab as deep as the train (9.25 (11))
LIGHT_CLOCK_SHAPE = [760, 3, 3]  # the one table (9.30): the chain of 760 extruded to [760, 3, 3]
LIGHT_CLOCK_TICKS = 4800  # COMPUTATION: 64 givings at the mean cadence P / 2 = 47 (P = 94 on A's mode), about 3000 intervals, the last return 300, a margin
MIRROR_DEPTH = 4  # the mirror's depth, the gap [1, 2] (A.3)


def emitter(
    position: list[int], extents: list[int], pair: list[int], direction: list[int], **extra: object
) -> dict:
    """A well that emits light (the light clock's A): the seed 50 x 2^20 on its mode (no
    coupling: the click alone, the model owner's decision (2) of record 1962); SINCE ALGEBRA.md 9.17
    (BUILD.md section 26) its emission is by its excited records' clicks: the stock
    EMITTER_STOCK excitations, each written once at its rung; SINCE THE GIVEN TRAIN (item
    27; 9.17 (6a)) each giving the train of TRAIN_PERIODS periods along `direction` on the
    given family's clock, the body's `extents` TRAIN_LENGTH along it; the profile and its norm
    the generator's (`given_train`)."""
    block: dict = {
        "position": position,
        "extents": extents,
        "pair": pair,
        "seed": EMITTER_SEED,
        "amount": EMITTER_STOCK,
        "emitter": {"family": "light", "train": {"direction": direction, "periods": TRAIN_PERIODS}},
    }
    block.update(extra)
    return block


def mirror_slab(position: list[int], extents: list[int]) -> dict:
    """A mirror (A.3): a body of light's kind over a box, carrying the gap [1, 2] at its Nodes
    (a material of light's kind; the holder body's name waits on the cleanup's step 6)."""
    entry = body(position, "light")
    entry["extents"] = extents
    entry["pair"] = list(WALL_PAIR)
    return entry


def receiver_set(document: dict, name: str, block: int) -> None:
    """A detector set on the light record bound to the receiving block (section 15 M1-4:
    the one key `block`, the measured number of the block, its Nodes the block's current
    Nodes); no wheel (the rung's wheel is the record's own, ALGEBRA.md 9.22 (4))."""
    document["detectors"].append({"name": name, "block": block, "threshold": 1})


def matter_world(
    massive,
    name: str,
    shape: list[int],
    boundary: dict,
    ticks: int,
    clock: list[int],
) -> dict:
    """A world of the matter kind [800, 809] alone (no light), the chain open on x, the
    emitter's frequency as the family's `phase_per_link` in the pair form (M1-6); no take
    pair (the take retired, ALGEBRA.md 9.19 (3))."""
    document = massive.world(name, "PIN", shape, boundary, KIND, [], ticks)
    document["families"] = [family for family in document["families"] if family["name"] != "light"]
    document["families"][0]["phase_per_link"] = list(clock)
    bounded(document)
    return document


def named_receiver(document: dict, receivers: dict[int, str]) -> None:
    """The receiver by name (#1116): `receiver` on each emitting block, the set that takes
    its clicks; written only when RECEIVER_KEY is on (held until the owner's word and the
    builder's line)."""
    if not RECEIVER_KEY:
        return
    for index, name in receivers.items():
        document["measured"][index]["receiver"] = name


def bounded(document: dict) -> None:
    """The amplitude bound of section 15 M1-10 on a massive world, after `massive_record`
    (no world key `wheel`: the rung's wheel is the record's own, ALGEBRA.md 9.22 (4))."""
    items = list(document.items())
    document.clear()
    for key, value in items:
        document[key] = value
        if key == "massive_record":
            document["amplitude_bound"] = AMPLITUDE_BOUND
            document["node_clock"] = NODE_CLOCK
            document["clock_family"] = CLOCK_FAMILY_NAME
            document["charge_family"] = CHARGE_FAMILY_NAME
            document["charge_strength"] = CHARGE_STRENGTH


def light_clock(massive) -> dict:
    """THE LIGHT CLOCK in the one table's form (the module docstring): the board [760, 3, 3]
    with x open and the face slabs 32 deep, light with the given clock on N = 1024, A at
    [600, 632) over the whole cross-section with its train along +x and its stock, the mirror
    at [690, 694), the set `at_well` A's own Nodes and A's `receiver` by name; the seeds,
    the train, the placement rule and the stamp by the massive generator's
    `seed_on_the_mode`."""
    document = massive.world(
        "light-clock",
        "PIN",
        list(LIGHT_CLOCK_SHAPE),
        massive.CHAIN,
        KIND,
        [emitter([600, 0, 0], [TRAIN_LENGTH, 3, 3], WELL_FULL, [1, 0, 0])],
        LIGHT_CLOCK_TICKS,
        light=light_family(GIVEN_CLOCK),
        seed_profile=False,
    )
    document["N"] = PHASE_STEPS
    document["face_depth"] = FACE_DEPTH
    bounded(document)
    document["measured"].append(mirror_slab([690, 0, 0], [MIRROR_DEPTH, 3, 3]))
    receiver_set(document, "at_well", 0)
    named_receiver(document, {0: "at_well"})
    massive.seed_on_the_mode(document)
    return document


def massive_worlds(massive) -> dict[str, dict]:
    """The massive rows written into the massive record folder: the light clock; the
    redshift, Sagnac, de Broglie and the moving mass HELD under the train (the module
    docstring), to be rebuilt from the table."""
    return {"light_clock": light_clock(massive)}


def main() -> None:
    massive = load_massive_generator()
    HELD.mkdir(parents=True, exist_ok=True)
    for folder, worlds in (
        (HERE, table_worlds(massive)),
        (MASSIVE, massive_worlds(massive)),
    ):
        for name, document in worlds.items():
            path = (HELD if name in HELD_NAMES else folder) / f"{name}.json"
            path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
            print(path.relative_to(EVENTS.parent.parent))


if __name__ == "__main__":
    main()
