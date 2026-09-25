"""The world files of the launch list (docs/designs/detector_law/RUN_LIST.md, the
rows marked "to write: the builder"), each written from its declaration alone
(docs/designs/detector_law/declarations/DECLARATIONS.md, its section 15 the
world lines row by row; DESIGN.md sections 6.0 to 6.2; PINS.md; the launch
list's own lines), on the Boss's order of 2026-09-24: every number of a file is
the declaration's; where a declaration lacks a line the file needs, the key is
ABSENT (the loader's refusal names it) and the gap is reported, never filled by
the writer. The engine's keys are the first build's
(`tests/test_detector_law.py::chain_world` the template of a ray-law world: a
lamp with `rate`, `wheel`, `train` and `directions`; a receiver a fixed body of
the family with one detector set on its Node; `clock_stamp` and `detector_law`
true) and the massive record kind's (`../massive_record/make_worlds.py`, whose
`world` helper writes the massive worlds here, so that their form is that
series' form byte for byte: `age_bound`, `K`, `N`, `release`, the blocks' keys).

The light rows (group L, this folder; section 15 L-1 to L-6): `two_slits.json`
(L-3: the 128 x 128 x 1 layer, y periodic, x open; the lamp at [20, 64, 0] with
the stock 1024 at one record per 16 intervals, the wheel [1, 64], the train 32
periods; the mirror line at x = 40, two Nodes deep, with the openings at y = 48
and 80; the screen at x = 104 over y in [4, 124], one detector set per Node;
the open faces the sponges; 17300 intervals) and `pace_fan_<12,16,24>.json` (L-6: the lamp at the
centre with one record on the four headings; the physicist's lines of
2026-09-24 09:02Z and 10:15Z: two probes per ray at 36 and 40 Links, free
Nodes, no ring sets, the ticks 1000, 1400 and 1900 per clock; the clocks
[77, 25], [30, 13], [77, 50]). Every light wall is a MIRROR LINE (L-1, the
fourth commit): blocks of light's kind of side 1 per Node with the pair [1, 2],
two Nodes deep, under the world key `massive_record`. Rows 2c, 10 (a), 10 (b)
and 2b are not in the GO (L-4, L-5, T-2) and have no file.

The table rows (group T, this folder; section 14 item 1 and section 15 T-1):
`bell_<a><b>.json` (sections 1 and 2: the bar of 21, the pair lamp with `arms` 2
and `branches` [[0, 1], [3, 1]], the train 128, the polarisers' `phase_window`
at the labels 0, N / 8, N / 4, 3 N / 8 of N = 2048, the wheel [1, 2048], the
clock [2464, 25] on the light and the counter families, K and the release the
L3 series'; the births' seed-set order of section 2 item 8: `residue_order`
"seed" and one `residue_seed` per world, drawn once from the host's entropy
and kept; the stock 2048 = W births; `ticks` 5500, at least the W = 2048 births,
the completion 3204 after the last birth and the far arm's transit), `malus_45.json` (section 5:
`amplitude/malus_22_5.json`'s form at s = 64 with the clock [308, 25] on
N = 256, the lamp's train 32 periods, its stock 256 and `ticks` 1200) and
`malus_<11.25,28.125,33.75>.json` (section 6:
`docs/designs/new_rows/worlds/malus_s<16,40,48>.json`'s form, the same clock,
train and ticks).

The emitter's take of its own record's remnant after its train (section 10
item 10) is THE RULE of the law, not a world key (the model owner, 2026-09-24
06:42Z; main 02f7388b): no emitter carries a timing key, the engine computes
it at load. A world with a detector set and no lamp carries the world key
`wheel`, the rung W of the ladder that chooses a record's cell (Reviewer 3's
line, the Boss's 06:50Z; without it the loader's default is 1 and a set holding
a quarter of a record's offer crosses no rung): 256 on the four R2 files (the
physicist's 07:37Z, one integer with the sets' rung of section 13 item 4), 64
on the light clock.

The massive rows (group M1, written into `../massive_record/`, the folder of
their family; section 15 M1-1 to M1-6): `redshift_k3.json` and
`redshift_control.json` (section 4 with item 7's CHECK on the loader's bound of 4096: the
chain of 4096, A at 2994, the receiver's set at 4094 with wheel 64, A's `own_grace` 3000
and the world key `wheel` 64, 9600 intervals), `sagnac_k3.json` and `sagnac_rest.json`
(section 13 on the chain of 3000 of 2026-09-24 07:58Z, the blocks their own receivers at
W = 256 with `own_grace` 3000, the hold, 6400 and 8450 intervals),
`light_clock_60.json` (section 10, A's receiving set at the free Node x = 612 beyond
its face with `own_grace` 70, the chain closed for light, 2600 intervals), every emitter at G = [1, 50], g = [1, 1000] with the
seed 50 x 2^20 (M1-1), holding no light content (M1-2), light's clock [1, 1]
(M1-3), the receivers detector sets with their own wheel (M1-4: 4b's at its body's Node with
wheel 64, R2's bound to the blocks by the key `block` with wheel 256, the light
clock's at the free Node x = 612 with wheel 64), `amplitude_bound` 2^32 on every massive world
(M1-10); `matter_waves_12.json`, `matter_waves_16.json` and
`matter_front_12.json` (M1-6: the matter family's `phase_per_link` [1089, 320]
or [11, 4] on N = 64, the lamp with the wheel [1, 64], the stock 2048 at one
per 8 intervals, the train 8 periods and `own_grace` 16700, the wall a barrier
line of matter-kind blocks with the raised pair [1, 2] two deep, the take lines
at x = 0 and 127 absorbing blocks of the matter kind with the kind's own pair and the
take's pair [-19, 86] or [-5, 27] under the builder's key `take`, 16700 and 600
intervals). The deep well worlds of group M2
are the massive record series' own (its generator writes them; RUN_LIST.md
step 3).

A world whose lines the engine on main does not carry yet is written into
`docs/designs/detector_law/held_worlds/` (HELD_NAMES below), outside the
shipped set under `examples/events` that the gate loads, until its line lands.
The four Bell worlds are held until the crystal (BUILD.md section 26) and the
four Malus worlds until the polariser body with an axis (item 14).

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
HELD_NAMES: set[str] = {
    "bell_a0b0",
    "bell_a0b1",
    "bell_a1b0",
    "bell_a1b1",
    # the four Malus worlds held with them (BUILD.md section 26 item 14): under
    # the cumulative ladder of ALGEBRA.md 9.19 (3) (b) the table body's two
    # cells at ONE Node cannot give Malus's counts (the entry's whole offer
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
CLOCKS = {12: [77, 25], 16: [30, 13], 24: [77, 50]}
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
# runaway's, withdrawn) and the margin rule refuses it. The one-cell well EMITTER_WELL on
# the kind EMITTER_KIND (the index worlds' kind, omega_0 = 0.505) is bound on a chain
# (omega_b = 0.32, P = 20 intervals) and on a layer (omega_b = 0.50, P = 12
# intervals). A world of W births declares the stock M = W (LAB_TOOLS.md A.1).
EMITTER_KIND = [7, 8]
EMITTER_WELL = [
    801,
    700,
]  # the rich well (700 remainder values, ALGEBRA.md 9.19 (4a), 9.22 (4)) bound on a chain and a layer
EMITTER_SEED_AMPLITUDE = 100
BELL_TRAIN = 128  # periods, DECLARATIONS.md sections 1 and 3
R2_CHAIN = 3000  # the physicist's declaration of 07:58Z: one chain of 3000 for both sagnac worlds, the blocks and the gap unchanged
# The physicist's word of 08:06Z on Reviewer 3's arithmetic (a k3 record born at t completes near
# 0.423 t + 4468, a rest record near t + 3990; the last hold birth near 4450): every hold record
# counts, so sagnac_k3 6400 and sagnac_rest 8450; the redshift pair 15000 (the last hold records,
# born near 9500, complete near 14800).
R2_TICKS = {"sagnac_k3": 6400, "sagnac_rest": 8450}
REDSHIFT_TICKS = 9600  # the physicist's line of 10:15Z (10000 runs A off the board at 9732)
LIGHT_CLOCK_TICKS = 2600  # the physicist's 09:18Z: the -x half's round trip on the closed chain (2078) before item 10's take removes it; the first cycle's record closes between about 2150 and 2400
# The receiver by name (#1116, the physicist's form, Reviewer 3 confirmed): a key `receiver`
# on every emitting block naming the set that takes the block's clicks. ON since the
# builder's engine line is on main (the receiver by name, DECLARATIONS.md section 13 item
# 7; the loader requires the key on an emitting block) and the owner's word of 2026-09-24
# (the Engine Fixer's line 6: the generator's emitter writes `receiver`); the flag is kept
# as the record of the held form.
RECEIVER_KEY = True


def light_family(pair: list[int] | None) -> dict:
    family: dict = {"name": "light", "quantum": 1}
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
    document["families"] = [light_family(pair), emitter_kind_family()]
    document["measured"] = []
    document["detectors"] = []
    return document


def emitter_kind_family(name: str = "matter") -> dict:
    """The emitter bodies' massive family (the kind EMITTER_KIND, no clock)."""
    return {"name": name, "quantum": 1, "pair": list(EMITTER_KIND)}


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
    excitations, its `emitter` the born family on the wheel with its residue order and, with
    `receiver`, the born records' ladder by name (the sets named; the lamp's `receiver` of
    old, written only under RECEIVER_KEY)."""
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


TWO_SLITS_SHAPE = [160, 256, 1]  # L-3's second draft (2026-09-24, 12:10Z): x AND y open
TWO_SLITS_OPENINGS = {114, 115, 116, 140, 141, 142}  # width 3, centred at y = 115 and 141 (d = 26)
TWO_SLITS_SCREEN_X = 153  # L = 113 from the mirror line at x = 40
TWO_SLITS_SCREEN_YS = range(28, 229)  # 201 rows: 67 cube detectors of side 3, the ladder (record 1899)
TWO_SLITS_STOCK = 1024  # one wheel [1, 1024], each u once (SIZING.md)
TWO_SLITS_TICKS = (
    6000  # 1024 excitations on [800, 500] (about 4096 intervals), the transit 231, the close, the margin
)


def two_slits() -> dict:
    """Section 15 L-3 (row 2a), THE SECOND DRAFT (2026-09-24, 12:10Z, on the blind map
    `two_slits_1024.py` beside SIZING.md): 6.2's own geometry on the 160 x 256 layer with
    x and y open (the four faces light's sponges); the lamp at [20, 128] with the stock
    1024 at one per 4 on the wheel [1, 1024], the train 32 periods; the mirror line at
    x = 40 two deep (L-1) with two openings of width 3 centred at y = 115 and 141; the
    screen at x = 153 as a row of 67 cube detectors of side 3 (x in [153, 155], y in [28,
    228]; record 1899, the rung's wheel the record's own); the emitter's `receiver` the 67
    screen sets (its records' ladder; the faces and the mirror line sinks outside it);
    5500 intervals. The first draft (128 x 128, y periodic, the
    openings of width 1 at y = 48 and 80, the screen at x = 104, 17300 intervals) is
    HISTORY in L-3."""
    document = ray_world(
        "two-slits",
        TWO_SLITS_SHAPE,
        {"x": "open", "y": "open", "z": "periodic"},
        CLOCKS[12],
        TWO_SLITS_TICKS,
    )
    document["measured"].extend(wall_line([40, 41], range(TWO_SLITS_SHAPE[1]), TWO_SLITS_OPENINGS))
    names = screen(document, TWO_SLITS_SCREEN_X, TWO_SLITS_SCREEN_YS)
    document["measured"].insert(
        0,
        emitter_body([20, 128, 0], TWO_SLITS_STOCK, receiver=names),
    )
    return document


# The pace fan's eight rays (the axes at 40 Links, the plane's diagonals at 39.6), the
# physicist's four lines of 2026-09-24 09:02Z (through the Boss, 09:12Z): the probes at the
# 40-Link Nodes of L-6, now FREE Nodes, with a second probe per ray at 36 Links; the ticks
# per clock 1000, 1400, 1900 (the trains 665, 943 and 1330 intervals); the reader the
# probes' PHASE per ray (GAMEBOARD, section 7), taken two periods after the front, the
# spread printed. The physicist's line of 10:15Z (through the Boss, 10:18Z): NO ring sets
# on the fan files (the drift observed at the probes is the ring's back-scatter, not the
# front), so the fan worlds carry the lamp and the probes and no detector set.
FAN_PROBES_40 = [
    [104, 64, 0],
    [24, 64, 0],
    [64, 104, 0],
    [64, 24, 0],
    [92, 92, 0],
    [36, 36, 0],
    [92, 36, 0],
    [36, 92, 0],
]
FAN_PROBES_36 = [
    [100, 64, 0],
    [28, 64, 0],
    [64, 100, 0],
    [64, 28, 0],
    [89, 89, 0],
    [39, 39, 0],
    [89, 39, 0],
    [39, 89, 0],
]
FAN_TICKS = {12: 1000, 16: 1400, 24: 1900}


def pace_fan(name: str, pair: list[int], wavelength: int) -> dict:
    """Section 15 L-6 (row 5a) with the physicist's lines of 2026-09-24 09:02Z and 10:15Z:
    the lamp at the centre, one record on the four headings; two probes per ray at 36 and 40
    Links (free Nodes); NO ring sets (the observed drift is the ring's back-scatter, not the
    front; the reading is the probes' phase two periods after the front, the spread printed);
    the ticks per clock (1000, 1400, 1900)."""
    document = ray_world(
        name, [128, 128, 1], {"x": "open", "y": "open", "z": "periodic"}, pair, FAN_TICKS[wavelength]
    )
    # no heading (16:25Z): the six headings by the loader's default, one record; the
    # emitter body's one excitation (ALGEBRA.md 9.17), broadband on one cell (the line
    # emitter of LAB_TOOLS.md A.1 owed: the fans' pin re-derived blind on it)
    document["measured"].append(emitter_body([64, 64, 0], 1))
    document["probes"] = [list(position) for position in FAN_PROBES_40 + FAN_PROBES_36]
    return document


def light_worlds(massive) -> dict[str, dict]:
    out: dict[str, dict] = {"two_slits": two_slits()}
    for wavelength, pair in CLOCKS.items():
        out[f"pace_fan_{wavelength}"] = pace_fan(f"pace-fan-{wavelength}", pair, wavelength)
    for document in out.values():
        massive.seed_on_the_mode(document)
    return out


# Group T: the table rows.

L3_K = 15728640  # the L3 series' K (`amplitude/bell_n2048_*.json`)
L3_RELEASE = [1, 67108864]
L3_LAMP_AMOUNT = 15728642  # the L3 series' stock (HISTORY: the amplitude law's lamp)
# Section 2 item 8: a Bell world counts EXACTLY W = 2048 births (under the seed order more
# than W births repeat the order), and the lamp's stock of records is its `amount` (one
# quantum per birth, the engine's `_births`), so the stock is W; the L3 series' stock
# would birth one record per interval to the end (the preview on 299b6bb2: 3433 births by
# the interval 3433).
BELL_STOCK = 2048
BELL_N = 2048
BELL_CLOCK = [2464, 25]  # section 14 item 1: the 12-Link clock [77, 25] on 64 scaled by 32 to N = 2048
MALUS_CLOCK = [308, 25]  # section 14 item 1: the same clock on N = 256
BELL_BRANCHES = [[0, 1], [3, 1]]
BELL_SETTINGS = {"a0": 0, "a1": BELL_N // 4, "b0": BELL_N // 8, "b1": 3 * BELL_N // 8}
# Section 2 item 8 (the loader's keys): under `residue_order` "seed" a Bell world counts
# exactly W = 2048 births at the rate [1, 1] (2048 intervals), so its `ticks` is at least
# W / rate + the far arm's transit + the completion (Reviewer 3's margin line). The engine
# ends a train at the first clock zero after the declared periods: on the clock [2464, 25]
# at N = 2048 the 128 periods (2660 intervals) end at 3200 (the birth line's `train` on
# 299b6bb2), and every record completed 3204 intervals after its birth in the preview
# (the last, born 2048, at 5252); the far polariser 7 Links from the lamp is 12.1 intervals
# at c = 1 / sqrt 3: 2048 + 3204 + 13 = 5265; written 5500, the margin 235 intervals.
BELL_TICKS = 5500
MALUS_TRAIN = 32  # periods (665 intervals on [308, 25]), section 5 item 2, 2026-09-24 06:05Z
MALUS_TICKS = 3800  # 256 excitations on the well [8, 7]: the wheel in about W P / 2 = 2560 intervals (ALGEBRA.md 9.17 (5) item 1); the engine reads 239 births within 3200 on the flux norm of 9.19 (3), COMPUTATION; the transit 6 and the completion beside
# Section 5 item 2, "the count of 256 births stands": the lamp's stock of records is its
# `amount` (a birth spends one quantum of it, the engine's `_births`; two_slits's stock 1024
# the same key), so the registered 2^50 would birth one record per interval to the end of
# the 1200 (the preview on 299b6bb2: 1200 births); the declared count is written as the stock.
MALUS_BIRTHS = 256
MALUS_SHAPE = [8, 1, 1]  # section 5 item 1 (12:15Z): the exit cell at x = 7 on the board
MALUS_READ_NODE = [4, 0, 0]  # the registered which-path read body, dropped with its set
MALUS_READ_SET = "first"


def bell(a: str, b: str) -> dict:
    """DECLARATIONS.md sections 1 and 2: the bar of 21 x 1 x 1 (x open, y and z periodic),
    N = 2048, the pair lamp at x = 10 with two arms and the joint labels 00 and 11, the
    train 128, the polarisers at x = 7 (Alice) and 17 (Bob) with their settings, each a
    detector set of one Node reading `sum`; the births in the seed-set order (section 2
    item 8: `residue_order` "seed", the world's own `residue_seed`, the stock 2048 = W
    births), 5500 intervals (BELL_TICKS); the clock
    [2464, 25] on the light family and [1, 1] on the counter family (section 1 item 3 and
    section 15 T-1)."""
    return {
        "law": "beam",
        "model_id": f"beam-detector-law-bell-{a}{b}-v1",
        "shape": [21, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": BELL_TICKS,
        "K": L3_K,
        "N": BELL_N,
        "release": L3_RELEASE,
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "families": [
            light_family(BELL_CLOCK),
            {"name": "counter", "quantum": 1, "phase_per_link": [1, 1]},
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
    files: the polariser's exit cell, the Node beyond its entry at x = 6, on the board at
    x = 7) WITHOUT the which-path `read` body at x = 4 and its set `first` (dropped there:
    under detector-law-v1 a set's Node is a take Node, so that set took the record before
    the polariser), the polariser's set alone on its entry Node (the table body of two
    cells, section 14 item 6), the clock [308, 25] on N = 256 (section 14 item 1) on the light family and
    [1, 1] on the counter family (section 5 item 3 and section 15 T-1), written in the
    file (the registered entity references carry no clock); the lamp's train 32 periods
    and `ticks` 1200 (section 5 item 2, 2026-09-24: the registered 300 intervals gave 300
    births and no click, a gather line written only at completion), the lamp's stock
    `amount` 256 (the count of 256 births)."""
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
        {"name": "counter", "quantum": 1, "phase_per_link": [1, 1]},
        emitter_kind_family(),
    ]
    rebuilt["massive_record"] = True
    rebuilt["amplitude_bound"] = AMPLITUDE_BOUND
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

MEDIUM = [156, 157]  # omega_0 = 0.1129 (sections 4 and 11)
WELL_HALF = [314, 315]
KIND = [800, 809]  # mu = 0.15
WELL_FULL = [
    800,
    801,
]  # the rich well of the massive rows' emitters (2403 remainder values; the mathematician's 9.21 (8))
COUPLING = {"G": [1, 50], "g": [1, 1000]}  # section 15 M1-1, with the seed 50 x 2^20
EMITTER_SEED = 50 << 20
AMPLITUDE_BOUND = 1 << 32  # section 15 M1-10, the world key `amplitude_bound` of every massive world
MATTER_CLOCKS = {12: [1089, 320], 16: [11, 4]}  # M1-6: the matter family's `phase_per_link`, N = 64
MATTER_TRAIN = 8  # periods (150 intervals), section 12 and M1-6
MATTER_STOCK = 2048  # section 12: one wheel [1, 2048], each u once (SIZING.md)
MATTER_RATE = [1, 2]  # the cadence one per 2 (SIZING.md, section 12)
MATTER_TICKS = 4700  # 2048 births at one per 2, the train 150, the transit 167, the margin (SIZING.md)
OWN_GRACE = 70  # section 10 item 1: the light clock's A, one period
# 4b's A: the physicist's line of 2026-09-24 09:33Z (through the Boss's 09:40Z): own_grace
# 3000 = the hold H after the ramp of 1500 (the file's 8000 was the named defect: A off the
# board at 9722), the world key `wheel` 64 (one integer with the light_detector's and the
# block's); the ticks 9600 for both redshift worlds (the physicist's line of 10:15Z, through
# the Boss's 10:18Z: 10000 runs A off the board at 9732).
REDSHIFT_GRACE = 3000
R2_GRACE = 3000  # section 13 item 1: R2's blocks, the whole hold
LAMP_GRACE = MATTER_TICKS  # HISTORY: the matter lamp's `own_grace` (retired, ALGEBRA.md 9.17)
EMITTER_STOCK = (
    64  # the massive rows' emitters: 64 excitations on the wheel [1, 64] (BUILD.md section 26)
)
SOURCE_FAMILY = (
    "source"  # the M1 rows' emitter body's own family (the matter kind's vacuum pair, no clock)
)


def emitter(position: list[int], side: int, pair: list[int], grace: int | None, **extra: object) -> dict:
    """A well that emits light (the light clock's A, the redshift's A, Sagnac's A and B):
    the coupling G = [1, 50], g = [1, 1000] for its response to light, the seed 50 x 2^20,
    W = 64 on its own record; SINCE ALGEBRA.md 9.17 (BUILD.md section 26) its emission is
    by its excited records' clicks: the stock EMITTER_STOCK excitations on the wheel [1,
    EMITTER_STOCK], each written once at its rung; no `emits`, no `own_grace`, no source
    term (the rows' readings re-derived blind before any run, RUN_LIST.md)."""
    _ = grace  # the emitter's grace retired (ALGEBRA.md 9.17; BUILD.md section 26)
    block: dict = {
        "position": position,
        "side": side,
        "pair": pair,
        "coupling": copy.deepcopy(COUPLING),
        "seed": EMITTER_SEED,
        "amount": EMITTER_STOCK,
        "emitter": {"family": "light"},
    }
    block.update(extra)
    return block


def receiver_set(document: dict, name: str, block: int) -> None:
    """A detector set on the light record bound to the receiving block (section 15 M1-4:
    the one key `block`, the measured number of the block, its Nodes the block's current
    cells); no wheel (the rung's wheel is the record's own, ALGEBRA.md 9.22 (4))."""
    document["detectors"].append({"name": name, "block": block, "threshold": 1})


def matter_world(
    massive,
    name: str,
    shape: list[int],
    boundary: dict,
    ticks: int,
    clock: list[int],
) -> dict:
    """A world of the matter kind [800, 809] alone (no light), its faces open on x, the
    emitter's frequency as the family's `phase_per_link` in the pair form (M1-6); no take
    pair (the take retired, ALGEBRA.md 9.19 (3))."""
    document = massive.world(name, "PIN", shape, boundary, KIND, [], ticks, faces=massive.FACES_OPEN)
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


def graced(document: dict, blocks: list[dict]) -> None:
    """HISTORY: the emitters' `own_grace` onto the world's block entries; the grace retired
    (ALGEBRA.md 9.17), nothing written."""
    _ = (document, blocks)


def bounded(document: dict) -> None:
    """The amplitude bound of section 15 M1-10 on a massive world, after `massive_record`
    (no world key `wheel`: the rung's wheel is the record's own, ALGEBRA.md 9.22 (4))."""
    items = list(document.items())
    document.clear()
    for key, value in items:
        document[key] = value
        if key == "massive_record":
            document["amplitude_bound"] = AMPLITUDE_BOUND


def massive_worlds(massive) -> dict[str, dict]:
    out: dict[str, dict] = {}
    chain = massive.CHAIN
    light_11 = light_family([1, 1])
    # Row 4b (section 4 with section 15 M1-1 to M1-5 and item 7's CHECK on the loader's
    # bound, 2026-09-24 06:10Z): the chain of 4096 (every shape axis is capped at 4096), the
    # emitter A of side 12 at the half-depth well at x = 2994, receding on -x at k = 3 over
    # the ramp 1500 with own_grace 3000 and the hold 3000 (the physicist's 09:33Z: at the
    # hold's end A stands at 1744, inside the board; the earlier 8000 ran A off the board at
    # 9722); the receiver the cube of side 3 at [4092, 4094] (1098 Links to its near face,
    # the transit 1905; the +x face at 4095 beyond it; record 1899) read as the set
    # `light_detector`; the probe at 4094; the control the same world without the momentum. The
    # ticks 9600 in both worlds (the physicist's 10:15Z; the two readers' windows equal).
    redshift_ticks = REDSHIFT_TICKS
    for name, motion in (
        ("redshift_k3", {"momentum": [-massive.MOMENTUM_K3, 0, 0], "ramp": 1500}),
        ("redshift_control", {}),
    ):
        document = massive.world(
            name.replace("_", "-"),
            "PIN",
            [4096, 1, 1],
            chain,
            MEDIUM,
            [emitter([2994, 0, 0], 12, WELL_HALF, REDSHIFT_GRACE, **motion)],
            redshift_ticks,
            light=light_11,
            faces=massive.FACES_OPEN,
            probes=[[4094, 0, 0]],
            mode_axis="x" if motion else None,
            seed_profile=False,
        )
        bounded(document)
        graced(document, [emitter([2994, 0, 0], 12, WELL_HALF, REDSHIFT_GRACE)])
        named_receiver(document, {0: "light_detector"})
        receiver_cube(document, "light_detector", [4096 - DETECTOR_SIDE - 1, 0, 0])
        massive.seed_on_the_mode(document)
        out[name] = document
    # Row R2 (section 13 with M1-1 to M1-4): two full-depth blocks A at [700, 712) and B at
    # [772, 784) on the chain of 3000 (the physicist's 07:58Z: one chain for both worlds,
    # the blocks and the gap of 60 unchanged, so that every hold record's forward half
    # reaches the +x face at 2999 and completes within the ticks: 6400 for k3, 8450 at
    # rest, the physicist's 08:06Z), both pushed to k = 3 on +x over the ramp 1500 and the hold 3000, both emitting
    # with own_grace 3000 (the hold, section 13 item 1), x open for the massive kind too
    # (M1-7); each block's cells a detector set on the light record bound by `block` with
    # its own wheel 256 (M1-4, section 13 item 4), the world key `wheel` 256 the ladder's W
    # (the physicist's 07:37Z, one integer with the sets' rung); the control with both at
    # rest; the probes at the facing cells.
    for name, motion in (
        ("sagnac_k3", {"momentum": [massive.MOMENTUM_K3, 0, 0], "ramp": 1500}),
        ("sagnac_rest", {}),
    ):
        document = massive.world(
            name.replace("_", "-"),
            "PIN",
            [R2_CHAIN, 1, 1],
            chain,
            KIND,
            [
                emitter([700, 0, 0], 12, WELL_FULL, R2_GRACE, **motion),
                emitter([772, 0, 0], 12, WELL_FULL, R2_GRACE, **motion),
            ],
            R2_TICKS[name],
            light=light_11,
            faces=massive.FACES_OPEN,
            probes=[[712, 0, 0], [772, 0, 0]],
            mode_axis="x" if motion else None,
            seed_profile=False,
        )
        bounded(document)
        graced(
            document,
            [
                emitter([700, 0, 0], 12, WELL_FULL, R2_GRACE),
                emitter([772, 0, 0], 12, WELL_FULL, R2_GRACE),
            ],
        )
        receiver_set(document, "at_a", 0)
        receiver_set(document, "at_b", 1)
        named_receiver(document, {0: "at_b", 1: "at_a"})
        massive.seed_on_the_mode(document)
        out[name] = document
    # The light clock of two bodies (section 10, the third draft, with M1-1 to M1-4): the
    # chain of 673 CLOSED for light at both ends (the loader's third face value, the
    # builder's line), the emitter A of side 12 at full depth at [600, 612) with own_grace
    # 70, the mirror the closed face at 672, the receiving set A's face cell x = 611 alone
    # with its own wheel 64 (section 10 item 9), 2600 intervals (the physicist's 09:18Z: the
    # -x half's round trip 2078 on the closed chain before the take removes it); the probe
    # at the face.
    document = massive.world(
        "light-clock-60",
        "PIN",
        [673, 1, 1],
        {"x": "closed", "y": "periodic", "z": "periodic"},
        KIND,
        [emitter([600, 0, 0], 12, WELL_FULL, OWN_GRACE)],
        LIGHT_CLOCK_TICKS,
        light=light_11,
        probes=[[612, 0, 0]],
        seed_profile=False,
    )
    bounded(document)
    graced(document, [emitter([600, 0, 0], 12, WELL_FULL, OWN_GRACE)])
    # section 10 item 9 (go-lines 9024cea0): the receiving set bound to A is the cube of
    # free Nodes adjacent to A's face toward the mirror, x in [612, 614] (record 1899), the
    # returning record's click at its rung stamped with A's count: `block` 0 with the cube's
    # positions (the loader's form (b) of BUILD.md item 14 on 299b6bb2).
    document["detectors"].append(
        {
            "name": "at_a",
            "block": 0,
            "positions": cube_positions(document, [612, 0, 0]),
            "threshold": 1,
        }
    )
    named_receiver(document, {0: "at_a"})
    massive.seed_on_the_mode(document)
    out["light_clock_60"] = document
    # Rows M1 and M2 (section 12 with section 15 M1-6; THE SIZED FORM of SIZING.md, section
    # 12's line of 2026-09-24): the 128 x 128 x 1 layer, y periodic, x open for the matter
    # kind, no light; the matter lamp at (20, 64) with its own clock, the wheel [1, 2048]
    # (one wheel, each u once), the stock 2048 at one record per 2 intervals, the train 8
    # periods, its `receiver` the screen's 121 sets (the ladder; the take lines sinks
    # outside it), the sets with their own rung wheel 65536; 4700 intervals;
    # the wall at x = 40 a barrier line of matter-kind blocks with the raised pair [1, 2],
    # two deep, the openings at y = 48 and 80 free (the fourth commit); the take lines at
    # x = 0 and 127 absorbing blocks of the matter kind (the fifth commit's correction, the
    # Boss's 02:20Z) with the kind's own pair and the take's pair under the builder's key
    # `take` (BUILD.md item 6b); the amplitude bound A = 2^32 of M1-10; the screen at
    # x = 104 a row of 41 cube detectors of side 3 over y in [3, 125] (record 1899). M2 on
    # its own chain of 200: the emitter at x = 20 with one record, the detector the cube
    # at [104, 106], 600 intervals.
    for wavelength, clock in MATTER_CLOCKS.items():
        document = matter_world(
            massive,
            f"matter-waves-{wavelength}",
            [128, 128, 1],
            {"x": "open", "y": "periodic", "z": "periodic"},
            MATTER_TICKS,
            clock,
        )
        document["measured"].extend(wall_line([40, 41], range(128), {48, 80}, "matter"))
        names = screen(document, 104, range(3, 126), "matter")
        # the matter emitter body (ALGEBRA.md 9.17): a well of the source family
        # (the kind EMITTER_KIND, no clock) of side 1, the well EMITTER_WELL, the
        # stock 2048 = W, the born family `matter` with its clock (the cadence
        # of the wheel W P / 2 intervals, COMPUTATION: the world's ticks
        # give a part of the wheel; the regeneration of the fifteen reads it)
        document["families"].append(emitter_kind_family(SOURCE_FAMILY))
        document["measured"].insert(
            0,
            emitter_body(
                [20, 64, 0],
                MATTER_STOCK,
                receiver=names,
                family="matter",
                own=SOURCE_FAMILY,
            ),
        )
        massive.seed_on_the_mode(document)
        out[f"matter_waves_{wavelength}"] = document
    document = matter_world(massive, "matter-front-12", [200, 1, 1], chain, 600, MATTER_CLOCKS[12])
    document["families"].append(emitter_kind_family(SOURCE_FAMILY))
    document["measured"].append(emitter_body([20, 0, 0], 1, family="matter", own=SOURCE_FAMILY))
    receiver_cube(document, "front", [104, 0, 0], "matter")
    massive.seed_on_the_mode(document)
    out["matter_front_12"] = document
    return out


def main() -> None:
    massive = load_massive_generator()
    HELD.mkdir(parents=True, exist_ok=True)
    for folder, worlds in (
        (HERE, light_worlds(massive)),
        (HERE, table_worlds(massive)),
        (MASSIVE, massive_worlds(massive)),
    ):
        for name, document in worlds.items():
            path = (HELD if name in HELD_NAMES else folder) / f"{name}.json"
            path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
            print(path.relative_to(EVENTS.parent.parent))


if __name__ == "__main__":
    main()
