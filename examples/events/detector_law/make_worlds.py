"""The world files of the launch list (docs/designs/detector_law/RUN_LIST.md, the
rows marked "to write: the builder"), each written from its declaration alone
(docs/designs/detector_law/declarations/DECLARATIONS.md, DESIGN.md sections 6.0
to 6.2, PINS.md rows 2a, 2c, 5a and 10, and the launch list's own lines), on the
Boss's order of 2026-09-24: every number of a file is the declaration's; where a
declaration lacks a line the file needs, the key is ABSENT (the loader's refusal
names it) and the gap is reported, never filled by the writer. The engine's
keys are the first build's (`tests/test_detector_law.py::chain_world` the
template of a ray-law world: a lamp with `rate`, `wheel`, `train` and
`directions`; a receiver a fixed body of the light family with one detector
set on its Node; `clock_stamp` and `detector_law` true) and the massive record
kind's (`../massive_record/make_worlds.py`, whose `world` helper writes the
massive worlds here, so that their form is that series' form byte for byte:
`age_bound`, `K`, `N`, `release`, the blocks' keys).

The light rows (group L, this folder): `two_slits.json` (DESIGN.md 6.2 at 12
Links: the separation 26, each opening 3 Nodes, L = 113, the screen the layer's
column, one detector set per Node; the launch list's 128 x 128 x 1 layer, the
train 128 periods of DESIGN.md 6.2 and the list; the stock 2048 at one record
per 8 intervals of DECLARATIONS.md section 12, "row 2a's world declares its
stock, train and HOST the same way", whose train of 8 periods differs from the
row's own 128 and is reported, not chosen), `three_openings_<mask>.json` (the same layer; the third
opening's place is not declared, so the seven files carry the mirror line
unbroken), `pace_fan_<12,16,24>.json` (a lamp at the centre of a 128^2 layer,
the ring at 40 Links on the plane's fan of DESIGN.md 6.0 A, the axis and the
diagonal; the probes along both), `one_opening_near.json` (DESIGN.md 6.1's
w = 9 world at 12 Links: w = 23, L = 278, the screen 415 pixels, the script's
board) and `one_opening_far.json` (PINS.md 10 (c): w = 4 lambda at F = 0.16,
L = 100 lambda; no board declared). The mirror line of every light row is the
engine's (M) wall, a block of light's kind of side 1 per Node with the pair
[21, 22] (the launch list's row 10 (a) and BUILD.md section 5 (iv-b)), under
the world key `massive_record`.

The table rows (group T, this folder): `bell_<a><b>.json` (sections 1 and 2:
the bar of 21, the pair lamp with `arms` 2 and `branches` [[0, 1], [3, 1]], the
train 128, the polarisers' `phase_window` at the labels 0, N / 8, N / 4,
3 N / 8 of N = 2048, the wheel [1, 2048], the light clock [2464, 25] of
section 14 item 1, K and the release the L3 series'), `malus_45.json` (section
5: `amplitude/malus_22_5.json`'s form at s = 64 with the clock [308, 25] of
section 14), `malus_<11.25,28.125,33.75>.json` (section 6:
`docs/designs/new_rows/worlds/malus_s<16,40,48>.json`'s form, the same clock;
the counter family on the clock too, the Boss's line of 01:00Z) and
`mach_zehnder.json` (section 3: the 33 x 33 x 1 layer, the lamp at (2, 2, 0),
the splitters' tables in `amplitude/mz_equal.json`'s arrangement, the weights
[21, 20], [20, 21] and the turns [16, 0], [0, 16]).

The massive rows (groups M1 and M2, written into `../massive_record/`, the
folder of their family): `redshift_k3.json` and `redshift_control.json`
(section 4), `sagnac_k3.json` and `sagnac_rest.json` (section 13, the second
draft: the blocks their own receivers), `matter_waves_12.json` and
`matter_front_12.json` (section 12 on main: the stock 2048 at one per 8
intervals, the train 8 periods, the hold 16700, W = 64; M2 on its own chain),
`deep_well_k3_40.json` and `deep_well_rest_40.json` (the launch list's step 3
line with `massive_layer_pins.py`: a 128^2 layer, s = 40 at full depth, the
ramp 1500, the hold 8000, the flat seed; the rest world the control without
the momentum, as section 4 forms its control) and `light_clock_60.json`
(section 10, the third draft: A its own receiver, no face detector).

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
NEW_ROWS = HERE.parents[2] / "docs" / "designs" / "new_rows" / "worlds"


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
# template of every ray-law world: its world keys and its light clock at 12
# Links, the pair [77, 25] on N = 64 (DECLARATIONS.md section 3 names [51, 25]
# as the 16-Link clock; no pair is declared for 24 Links).
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
CLOCKS = {12: [77, 25], 16: [51, 25]}
LAYER = {"x": "open", "y": "open", "z": "periodic"}
MIRROR_PAIR = [21, 22]  # the (M) wall's gap, the launch list's row 10 (a)
STOCK = 2048  # DECLARATIONS.md section 12 (main, 6e16f16d): the stock of records, one per 8 intervals
CADENCE = [1, 8]
MATTER_TRAIN = 8  # section 12: each matter record a train of 8 periods
TEMPLATE_WHEEL = [2531, 4096]  # the template lamp's birth wheel (W = 4096, DESIGN.md section 5)
TRAIN = 128  # periods, DESIGN.md 6.2 and DECLARATIONS.md sections 1 and 3


def light_family(pair: list[int] | None) -> dict:
    family: dict = {"name": "light", "quantum": 1}
    if pair is not None:
        family["phase_per_link"] = pair
    return family


def ray_world(name: str, shape: list[int] | None, boundary: dict, pair: list[int] | None) -> dict:
    document: dict = {"law": "beam", "model_id": f"beam-detector-law-{name}-v1"}
    if shape is not None:
        document["shape"] = shape
    document["boundary"] = boundary
    document.update({key: value for key, value in TEMPLATE_KEYS.items() if key != "law"})
    document["families"] = [light_family(pair)]
    document["measured"] = []
    document["detectors"] = []
    return document


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


def mirror_node(position: list[int]) -> dict:
    """One Node of a mirror line: the (M) wall, a block of light's kind of side 1."""
    entry = body(position)
    entry["side"] = 1
    entry["pair"] = list(MIRROR_PAIR)
    return entry


def mirror_line(x: int, ys: range, openings: set[int]) -> list[dict]:
    return [mirror_node([x, y, 0]) for y in ys if y not in openings]


def screen(document: dict, x: int, ys: range, family: str = "light") -> None:
    """A screen of one-Node detectors `screen_<y>` on receiver bodies at x (the
    two-slit worlds' form: one set per Node, each with its own click)."""
    for y in ys:
        document["measured"].append(body([x, y, 0], family, [[-1, 0, 0]]))
        document["detectors"].append({"name": f"screen_{y}", "positions": [[x, y, 0]], "threshold": 1})


def lamp(
    position: list[int] | None,
    amount: int | None,
    rate: list[int] | None,
    wheel: list[int] | None,
    directions: list[list[int]] | None,
    train: int | None,
    family: str = "light",
) -> dict:
    """The lamp in the template's form; a key not declared is left absent."""
    entry: dict = {}
    if position is not None:
        entry["position"] = position
    entry["family"] = family
    if amount is not None:
        entry["amount"] = amount
    entry["phase"] = 0
    entry["momentum"] = [0, 0, 0]
    entry["fixed"] = True
    if directions is not None:
        entry["directions"] = directions
    inner: dict = {}
    if rate is not None:
        inner["rate"] = rate
    if wheel is not None:
        inner["wheel"] = wheel
    if directions is not None:
        inner["directions"] = directions
    if train is not None:
        inner["train"] = train
    entry["lamp"] = inner
    return entry


# Group L: the light rows.


def two_slits_layer(name: str, openings: set[int]) -> dict:
    """DESIGN.md 6.2's two-slit world at 12 Links on the launch list's 128 x 128 x 1
    layer: the wall at x = 2 (the script's `wall_x`), the separation 26, each opening
    3 Nodes about the centre (the openings at y = 51..53 and 77..79), L = 113 (the
    screen at x = 115), the train 128 periods, the stock 4096 at one record per 4
    intervals. The lamp's Node and the ticks are not declared."""
    document = ray_world(name, [128, 128, 1], LAYER, CLOCKS[12])
    document["massive_record"] = True
    document["measured"].append(lamp(None, STOCK, CADENCE, TEMPLATE_WHEEL, [[1, 0, 0]], TRAIN))
    document["measured"].extend(mirror_line(2, range(128), openings))
    screen(document, 115, range(128))
    return document


def pace_fan(name: str, pair: list[int] | None) -> dict:
    """DESIGN.md 6.0 A on the launch list's layer: the lamp at the centre (64, 64), the
    ring at 40 Links on the plane's fan, the axis (1, 0) and the diagonal (1, 1): the
    ring's detectors where the fan's directions land on a Node at 40 Links (the four
    axis Nodes; the diagonal's 40 Links, 28.28 Nodes, is no Node), the probes along +x
    and along the diagonal out to the ring (the phase advance per Link, GAMEBOARD). The
    lamp's rate, wheel, stock, train and directions and the ticks are not declared."""
    document = ray_world(name, [128, 128, 1], LAYER, pair)
    document["massive_record"] = True  # the `probes` key is admitted under this key alone
    document["measured"].append(lamp([64, 64, 0], None, None, None, None, None))
    for label, position, facing in (
        ("ring_px", [104, 64, 0], [[-1, 0, 0]]),
        ("ring_mx", [24, 64, 0], [[1, 0, 0]]),
        ("ring_py", [64, 104, 0], [[0, -1, 0]]),
        ("ring_my", [64, 24, 0], [[0, 1, 0]]),
    ):
        document["measured"].append(body(position, "light", facing))
        document["detectors"].append({"name": label, "positions": [position], "threshold": 1})
    document["probes"] = [[64 + k, 64, 0] for k in range(1, 40)] + [
        [64 + k, 64 + k, 0] for k in range(1, 29)
    ]
    return document


def one_opening_near() -> dict:
    """DESIGN.md 6.1's w = 9 world at 12 Links (`detector_law_pins.out`, section B): w = 23
    Nodes, L = 278 Links, the Fresnel number 0.159, the screen 415 pixels, the script's
    board 522 x 895 (the margins beyond the read window's light cone), the wall at x = 2,
    the opening about the centre y = 447, the screen at x = 280 over y in [240, 654]. The
    lamp's Node and the ticks are not declared."""
    document = ray_world("one-opening-near", [522, 895, 1], LAYER, CLOCKS[12])
    document["massive_record"] = True
    document["measured"].append(lamp(None, STOCK, CADENCE, TEMPLATE_WHEEL, [[1, 0, 0]], TRAIN))
    document["measured"].extend(mirror_line(2, range(895), set(range(436, 459))))
    screen(document, 280, range(240, 655))
    return document


def one_opening_far() -> dict:
    """PINS.md 10 (c) at 12 Links: the opening w = 4 lambda = 48 Nodes at F = 0.16, the
    screen at L = 100 lambda = 1200 Links. No board, no lamp's Node and no ticks are
    declared, so the mirror line and the screen cannot be laid: the file carries the
    world keys, the clock and the lamp's declared keys alone."""
    document = ray_world("one-opening-far", None, LAYER, CLOCKS[12])
    document["massive_record"] = True
    document["measured"].append(lamp(None, STOCK, CADENCE, TEMPLATE_WHEEL, [[1, 0, 0]], TRAIN))
    return document


def light_worlds() -> dict[str, dict]:
    out: dict[str, dict] = {}
    out["two_slits"] = two_slits_layer("two-slits", {51, 52, 53, 77, 78, 79})
    for mask in ("abc", "ab", "ac", "bc", "a", "b", "c"):
        out[f"three_openings_{mask}"] = two_slits_layer(f"three-openings-{mask}", set())
    for wavelength in (12, 16, 24):
        out[f"pace_fan_{wavelength}"] = pace_fan(f"pace-fan-{wavelength}", CLOCKS.get(wavelength))
    out["one_opening_near"] = one_opening_near()
    out["one_opening_far"] = one_opening_far()
    return out


# Group T: the table rows.

L3_K = 15728640  # the L3 series' K (`amplitude/bell_n2048_*.json`)
L3_RELEASE = [1, 67108864]
L3_LAMP_AMOUNT = 15728642
BELL_N = 2048
BELL_WHEEL = [1, BELL_N]  # section 1 item 2, kept by section 14 item 1 (the line [8, 2048] withdrawn)
BELL_CLOCK = [2464, 25]  # section 14 item 1: the 12-Link clock [77, 25] on 64 scaled by 32 to N = 2048
MALUS_CLOCK = [308, 25]  # section 14 item 1: the same clock on N = 256
BELL_BRANCHES = [[0, 1], [3, 1]]
BELL_SETTINGS = {"a0": 0, "a1": BELL_N // 4, "b0": BELL_N // 8, "b1": 3 * BELL_N // 8}


def bell(a: str, b: str) -> dict:
    """DECLARATIONS.md sections 1 and 2: the bar of 21 x 1 x 1 (x open, y and z periodic),
    N = 2048, the pair lamp at x = 10 with two arms and the joint labels 00 and 11, the
    train 128, the polarisers at x = 7 (Alice) and 17 (Bob) with their settings, each a
    detector set of one Node reading `sum`, 300 intervals; the light family's clock
    [2464, 25] on N = 2048 (section 14 item 1) on the light family and on the counter
    family alike (the Boss's line of 2026-09-24, 01:00Z: the loader asks every paid
    family's clock under `detector_law`)."""
    document: dict = {
        "law": "beam",
        "model_id": f"beam-detector-law-bell-{a}{b}-v1",
        "shape": [21, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "ticks": 300,
        "K": L3_K,
        "N": BELL_N,
        "release": L3_RELEASE,
        "suspension": 0,
        "clock_stamp": True,
        "detector_law": True,
        "families": [
            light_family(BELL_CLOCK),
            {"name": "counter", "quantum": 1, "phase_per_link": BELL_CLOCK},
        ],
        "measured": [
            {
                "position": [10, 0, 0],
                "family": "light",
                "amount": L3_LAMP_AMOUNT,
                "phase": 0,
                "fixed": True,
                "lamp": {
                    "rate": [1, 1],
                    "wheel": BELL_WHEEL,
                    "directions": [[1, 0, 0], [-1, 0, 0]],
                    "arms": 2,
                    "branches": BELL_BRANCHES,
                    "train": TRAIN,
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
    return document


def malus(name: str, source: Path, setting: int) -> dict:
    """DECLARATIONS.md sections 5 and 6: the registered form of the source world with
    `detector_law` true, `clock_stamp` true, the table's `phase_window` at the declared
    setting and the light family's clock [308, 25] on N = 256 (section 14 item 1), the
    families written in the file (the registered entity references carry no clock), the
    counter family on the same clock (the Boss's line of 2026-09-24, 01:00Z)."""
    document = json.loads(source.read_text(encoding="utf-8"))
    document = copy.deepcopy(document)
    rebuilt: dict = {"law": "beam", "model_id": f"beam-detector-law-{name}-v1"}
    for key, value in document.items():
        if key in ("law", "model_id", "entity_definitions", "entities", "families"):
            continue
        rebuilt[key] = value
        if key == "suspension":
            rebuilt["clock_stamp"] = True
            rebuilt["detector_law"] = True
    rebuilt["families"] = [
        light_family(MALUS_CLOCK),
        {"name": "counter", "quantum": 1, "phase_per_link": MALUS_CLOCK},
    ]
    for entry in rebuilt["measured"]:
        table = entry.get("table", {}).get("light")
        if isinstance(table, dict) and "phase_window" in table:
            table["phase_window"] = setting
    return rebuilt


SPLITTER = {
    "rule": "rerelease",
    "inputs": [[0, 1, 0], [1, 0, 0]],
    "weights": [[21, 20], [20, 21]],
    "turns": [[16, 0], [0, 16]],
}


def mach_zehnder() -> dict:
    """DECLARATIONS.md section 3: the 33 x 33 x 1 layer (x and y open, z periodic),
    N = 64, the wheel [1, 64], the first build's K and release, the lamp at (2, 2, 0) on
    the +x arm with the train 128 and 64 births (item 5), two splitters of the table form
    at (12, 2, 0) and (12, 12, 0) with the split's weights and turns in `mz_equal.json`'s
    arrangement, 2000 intervals. Not declared: the clock pair per world ([77, 25] or
    [51, 25]), the lamp's rate, the mirrors' Nodes (and the mirror form has no key on
    main), the ports D1 and D2 (their lines across the corridor)."""
    document = ray_world("mach-zehnder", [33, 33, 1], LAYER, None)
    document["ticks"] = 2000
    document["measured"].append(lamp([2, 2, 0], 64, None, [1, 64], [[1, 0, 0]], TRAIN))
    for position in ([12, 2, 0], [12, 12, 0]):
        entry = body(position, "light", [[1, 0, 0], [0, 1, 0]])
        entry["table"] = {"light": copy.deepcopy(SPLITTER)}
        document["measured"].append(entry)
    return document


def table_worlds() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for a in ("a0", "a1"):
        for b in ("b0", "b1"):
            out[f"bell_{a}{b}"] = bell(a, b)
    out["malus_45"] = malus("malus-45", EVENTS / "amplitude" / "malus_22_5.json", 64)
    for degrees, setting in (("11.25", 16), ("28.125", 40), ("33.75", 48)):
        out[f"malus_{degrees}"] = malus(
            f"malus-{degrees.replace('.', '-')}", NEW_ROWS / f"malus_s{setting}.json", setting
        )
    out["mach_zehnder"] = mach_zehnder()
    return out


# Groups M1 and M2: the massive rows, in the massive record series' form.

MEDIUM = [156, 157]  # omega_0 = 0.1129 (sections 4 and 11)
WELL_HALF = [314, 315]
KIND = [800, 809]  # mu = 0.15
WELL_FULL = [800, 800]
WEAK = {"G": [1, 1], "g": [1, 50000]}


def emitter(position: list[int], side: int, pair: list[int], **extra: object) -> dict:
    """A block that emits light at G = [1, 1], g = [1, 50000], W = 64 on its own record;
    its held light content (the stock of its births) is not declared in any section."""
    block: dict = {
        "position": position,
        "side": side,
        "pair": pair,
        "coupling": dict(WEAK),
        "wheel": 64,
        "emits": "light",
    }
    block.update(extra)
    return block


def light_detector(document: dict, name: str, x: int, facing: int) -> None:
    """A detector of the ray law on the light record at a chain Node: the template's
    receiver body and its set. The declared rung W of the detector has no key on main
    (the engine's rung is the lamps' wheel)."""
    document["measured"].append(body([x, 0, 0], "light", [[facing, 0, 0]]))
    document["detectors"].append({"name": name, "positions": [[x, 0, 0]], "threshold": 1})


def massive_worlds(massive) -> dict[str, dict]:
    out: dict[str, dict] = {}
    chain = massive.CHAIN
    faces_open = massive.FACES_OPEN
    light_11 = light_family([1, 1])
    light_unpaired = light_family(None)
    # Row 4b (section 4): the chain of 2200, the emitter A of side 12 at the half-depth
    # well, seed 2^20, receding on -x at k = 3 from x = 700 over the ramp 1500, 9500
    # intervals; the control with A at rest at x = 1300; the light detector at x = 1900.
    for name, x, motion in (
        ("redshift_k3", 700, {"momentum": [-massive.MOMENTUM_K3, 0, 0], "ramp": 1500}),
        ("redshift_control", 1300, {}),
    ):
        document = massive.world(
            name.replace("_", "-"),
            "PIN",
            [2200, 1, 1],
            chain,
            MEDIUM,
            [emitter([x, 0, 0], 12, WELL_HALF, seed=1 << 20, **motion)],
            9500,
            light=light_11,
            faces=faces_open,
            probes=[[1900, 0, 0]],
            mode_axis="x" if motion else None,
        )
        light_detector(document, "light_detector", 1900, -1)
        out[name] = document
    # Row R2 (section 13 on main, the second draft of 00:25Z): two full-depth blocks A at
    # [700, 712) and B at [772, 784) on the chain of 2200, both pushed to k = 3 on +x over
    # the ramp 1500 and the hold 3000, both emitting; the receivers are the blocks
    # themselves at W = 64 (no separate detectors); the control with both at rest.
    # Light's clock pair is not declared; N_s (one period) has no key on main; the band's
    # re-declaration announced by the Boss may still move this section.
    for name, motion in (
        ("sagnac_k3", {"momentum": [massive.MOMENTUM_K3, 0, 0], "ramp": 1500}),
        ("sagnac_rest", {}),
    ):
        out[name] = massive.world(
            name.replace("_", "-"),
            "PIN",
            [2200, 1, 1],
            chain,
            KIND,
            [
                emitter([700, 0, 0], 12, WELL_FULL, **motion),
                emitter([772, 0, 0], 12, WELL_FULL, **motion),
            ],
            4500,
            light=light_unpaired,
            probes=[[712, 0, 0], [772, 0, 0]],
            mode_axis="x" if motion else None,
        )
    # Row M1 (section 12 on main, 6e16f16d): the 128 x 128 x 1 layer, y periodic, x open
    # for the matter kind (zero faces), no light; the matter lamp at (20, 64) sending +x,
    # the stock 2048 at one record per 8 intervals, each a train of 8 periods; the screen
    # at x = 104 over y in [4, 124], one detector set per Node at W = 64; the hold 16700.
    # Not declared as keys: the lamp's omega 0.33408 (the matter kind carries no
    # `phase_per_link`), the wheel's rate r (its W is 64), the mirror line at x = 40 with
    # its openings at y = 48 and 80 (a zero line for the matter kind has no key on main)
    # and the two take lines at x = 0 and x = 127 (no key). The 16-Link world beside is
    # no longer on the launch list.
    document = massive.world(
        "matter-waves-12",
        "PIN",
        [128, 128, 1],
        {"x": "open", "y": "periodic", "z": "periodic"},
        KIND,
        [],
        16700,
        faces=faces_open,
    )
    document["families"] = [family for family in document["families"] if family["name"] != "light"]
    document["measured"].append(
        lamp([20, 64, 0], STOCK, CADENCE, None, [[1, 0, 0]], MATTER_TRAIN, "matter")
    )
    screen(document, 104, range(4, 125), "matter")
    out["matter_waves_12"] = document
    # Row M2 (section 12 on main): its own chain of 200 x 1 x 1, x open for the matter
    # kind, the matter lamp at x = 20 inserting one record (a train of 8 periods), a
    # detector of the ray law on the matter record at x = 104 with W = 64. Not declared:
    # the lamp's rate and the wheel's rate r, the ticks, the lamp's omega (as above).
    document = massive.world("matter-front-12", "PIN", [200, 1, 1], chain, KIND, [], 0, faces=faces_open)
    del document["ticks"]
    document["families"] = [family for family in document["families"] if family["name"] != "light"]
    document["measured"].append(lamp([20, 0, 0], 1, None, None, [[1, 0, 0]], MATTER_TRAIN, "matter"))
    document["measured"].append(body([104, 0, 0], "matter", [[-1, 0, 0]]))
    document["detectors"].append({"name": "front", "positions": [[104, 0, 0]], "threshold": 1})
    out["matter_front_12"] = document
    # The deep well in motion (the launch list's step 3 with `massive_layer_pins.py`): the
    # kind [800, 809] on a periodic 128^2 layer, the well of side 40 at full depth centred
    # as the layer scripts centre it (the corner 44), the flat seed (the default 2^20), the
    # control margin, pushed to k = 3 over the ramp 1500 with the hold 8000; the rest world
    # the control without the momentum.
    for name, motion in (
        ("deep_well_k3_40", {"momentum": [massive.MOMENTUM_K3, 0, 0], "ramp": 1500}),
        ("deep_well_rest_40", {}),
    ):
        block = {"position": [44, 44, 0], "side": 40, "pair": WELL_FULL, "margin": "control"}
        block.update(motion)
        out[name] = massive.world(
            name.replace("_", "-"),
            "CONTROL",
            [128, 128, 1],
            massive.PERIODIC,
            KIND,
            [block],
            9500,
            mode_axis="x" if motion else None,
        )
    # The light clock of two bodies (section 10 on main, the third draft of 00:25Z): the
    # chain of 673 open for light at both ends, the emitter A of side 12 at full depth at
    # [600, 612) with the flat seed, the mirror the open face at 672, A ITSELF the receiver
    # at W = 64 on its cells (no face detector), the hold 2000; the probe at the face.
    # Light's clock pair is not declared; N_s = 70 has no key on main.
    out["light_clock_60"] = massive.world(
        "light-clock-60",
        "PIN",
        [673, 1, 1],
        chain,
        KIND,
        [emitter([600, 0, 0], 12, WELL_FULL)],
        2000,
        light=light_unpaired,
        probes=[[612, 0, 0]],
    )
    return out


def main() -> None:
    massive = load_massive_generator()
    for folder, worlds in (
        (HERE, light_worlds()),
        (HERE, table_worlds()),
        (MASSIVE, massive_worlds(massive)),
    ):
        for name, document in worlds.items():
            path = folder / f"{name}.json"
            path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
            print(path.relative_to(EVENTS.parent.parent))


if __name__ == "__main__":
    main()
