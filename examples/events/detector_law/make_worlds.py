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
centre with one record on the four headings, the probes and the ring sets at
the eight Nodes of the axes and the diagonals, 800 intervals; the clocks
[77, 25], [30, 13], [77, 50]). Every light wall is a MIRROR LINE (L-1, the
fourth commit): blocks of light's kind of side 1 per Node with the pair [1, 2],
two Nodes deep, under the world key `massive_record`. Rows 2c, 10 (a), 10 (b)
and 2b are not in the GO (L-4, L-5, T-2) and have no file.

The table rows (group T, this folder; section 14 item 1 and section 15 T-1):
`bell_<a><b>.json` (sections 1 and 2: the bar of 21, the pair lamp with `arms` 2
and `branches` [[0, 1], [3, 1]], the train 128, the polarisers' `phase_window`
at the labels 0, N / 8, N / 4, 3 N / 8 of N = 2048, the wheel [1, 2048], the
clock [2464, 25] on the light and the counter families, K and the release the
L3 series'), `malus_45.json` (section 5: `amplitude/malus_22_5.json`'s form at
s = 64 with the clock [308, 25] on N = 256) and `malus_<11.25,28.125,33.75>.json`
(section 6: `docs/designs/new_rows/worlds/malus_s<16,40,48>.json`'s form, the
same clock).

The massive rows (group M1, written into `../massive_record/`, the folder of
their family; section 15 M1-1 to M1-6): `redshift_k3.json` and
`redshift_control.json` (section 4), `sagnac_k3.json` and `sagnac_rest.json`
(section 13, the blocks their own receivers with `own_grace` 70),
`light_clock_60.json` (section 10, A its own receiver with `own_grace` 70, the
chain closed for light), every emitter at G = [1, 50], g = [1, 1000] with the
seed 50 x 2^20 (M1-1), holding no light content (M1-2), light's clock [1, 1]
(M1-3), the receivers detector sets bound to their body by the key `block`
with their own wheel 64 (M1-4), `amplitude_bound` 2^32 on every massive world
(M1-10); `matter_waves_12.json`, `matter_waves_16.json` and
`matter_front_12.json` (M1-6: the matter family's `phase_per_link` [1089, 320]
or [11, 4] on N = 64, the lamp with the wheel [1, 64], the stock 2048 at one
per 8 intervals, the train 8 periods and `own_grace` 16700, the wall a barrier
line of matter-kind blocks with the raised pair [1, 2] two deep, the take lines
at x = 0 and 127 absorbing blocks of the matter kind with the take's pair
[-19, 86] or [-5, 27], 16700 and 600 intervals). The deep well worlds of group M2
are the massive record series' own (its generator writes them; RUN_LIST.md
step 3).

The worlds whose lines the engine on main does not carry yet are written into
`docs/designs/detector_law/held_worlds/` (HELD_NAMES below), outside the
shipped set under `examples/events` that the gate loads; each moves back to
its folder when its line lands.

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
HELD_NAMES = {
    "two_slits",
    "redshift_k3",
    "redshift_control",
    "sagnac_k3",
    "sagnac_rest",
    "light_clock_60",
    "matter_waves_12",
    "matter_waves_16",
    "matter_front_12",
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
TRAIN_32 = 32  # periods, section 15 L-3 and L-6
BELL_TRAIN = 128  # periods, DECLARATIONS.md sections 1 and 3


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


def wall_node(
    position: list[int],
    family: str = "light",
    pair: list[int] | None = WALL_PAIR,
    absorbing: bool = False,
) -> dict:
    """One Node of a wall: a block of side 1 with the pair [1, 2] (section 15 L-1 the
    mirror line of light's kind; M1-6 the barrier line of the matter kind, its raised pair
    the builder's line), or a take Node (`absorbing` true, the matter kind's take lines of
    M1-6's correction; no pair is declared for them, so the key is absent)."""
    entry = body(position, family)
    entry["side"] = 1
    if pair is not None:
        entry["pair"] = list(pair)
    if absorbing:
        entry["absorbing"] = True
    return entry


def wall_line(
    xs: list[int],
    ys: range,
    openings: set[int],
    family: str = "light",
    pair=WALL_PAIR,
    absorbing: bool = False,
) -> list[dict]:
    """A wall of the declared depth: one block per Node of the columns `xs`, the openings
    free in every column."""
    return [wall_node([x, y, 0], family, pair, absorbing) for x in xs for y in ys if y not in openings]


def screen(document: dict, x: int, ys: range, family: str = "light") -> None:
    """A screen of one-Node detectors `screen_<y>` on receiver bodies at x: one set per
    Node of the row, each with its own click (section 12; Builder 2's finding)."""
    for y in ys:
        document["measured"].append(body([x, y, 0], family, [[-1, 0, 0]]))
        document["detectors"].append({"name": f"screen_{y}", "positions": [[x, y, 0]], "threshold": 1})


def lamp(
    position: list[int],
    amount: int,
    rate: list[int],
    wheel: list[int],
    directions: list[list[int]],
    train: int,
    family: str = "light",
) -> dict:
    """The lamp in the template's form (the matter lamp's frequency is its family's
    `phase_per_link`, section 15 M1-6, not a lamp key)."""
    entry: dict = {
        "position": position,
        "family": family,
        "amount": amount,
        "phase": 0,
        "momentum": [0, 0, 0],
        "fixed": True,
        "directions": directions,
    }
    inner: dict = {"rate": rate, "wheel": wheel, "directions": directions, "train": train}
    entry["lamp"] = inner
    return entry


# Group L: the light rows.


def two_slits() -> dict:
    """Section 15 L-3 (row 2a) with L-1's fourth commit: the mirror line at x = 40, two
    Nodes deep, the openings free; the layer's open faces the sponges, no take lines."""
    document = ray_world(
        "two-slits", [128, 128, 1], {"x": "open", "y": "periodic", "z": "periodic"}, CLOCKS[12], 17300
    )
    document["measured"].append(lamp([20, 64, 0], 1024, [1, 16], [1, 64], [[1, 0, 0]], TRAIN_32))
    document["measured"].extend(wall_line([40, 41], range(128), {48, 80}))
    screen(document, 104, range(4, 125))
    return document


FAN_NODES = [
    [104, 64, 0],
    [24, 64, 0],
    [64, 104, 0],
    [64, 24, 0],
    [92, 92, 0],
    [36, 36, 0],
    [92, 36, 0],
    [36, 92, 0],
]


def pace_fan(name: str, pair: list[int]) -> dict:
    """Section 15 L-6 (row 5a): the lamp at the centre, one record on the four headings,
    the probes and the ring detector sets of one Node at the eight Nodes of the axes (40
    Links) and the plane's diagonals (39.6 Links)."""
    document = ray_world(name, [128, 128, 1], {"x": "open", "y": "open", "z": "periodic"}, pair, 800)
    headings = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0]]
    document["measured"].append(lamp([64, 64, 0], 1, [1, 1], [1, 64], headings, TRAIN_32))
    for position in FAN_NODES:
        document["measured"].append(body(position, "light"))
        label = f"ring_{position[0]}_{position[1]}"
        document["detectors"].append({"name": label, "positions": [position], "threshold": 1})
    document["probes"] = [list(position) for position in FAN_NODES]
    return document


def light_worlds() -> dict[str, dict]:
    out: dict[str, dict] = {"two_slits": two_slits()}
    for wavelength, pair in CLOCKS.items():
        out[f"pace_fan_{wavelength}"] = pace_fan(f"pace-fan-{wavelength}", pair)
    return out


# Group T: the table rows.

L3_K = 15728640  # the L3 series' K (`amplitude/bell_n2048_*.json`)
L3_RELEASE = [1, 67108864]
L3_LAMP_AMOUNT = 15728642
BELL_N = 2048
BELL_WHEEL = [1, BELL_N]  # section 1 item 2, kept by section 14 item 1
BELL_CLOCK = [2464, 25]  # section 14 item 1: the 12-Link clock [77, 25] on 64 scaled by 32 to N = 2048
MALUS_CLOCK = [308, 25]  # section 14 item 1: the same clock on N = 256
BELL_BRANCHES = [[0, 1], [3, 1]]
BELL_SETTINGS = {"a0": 0, "a1": BELL_N // 4, "b0": BELL_N // 8, "b1": 3 * BELL_N // 8}


def bell(a: str, b: str) -> dict:
    """DECLARATIONS.md sections 1 and 2: the bar of 21 x 1 x 1 (x open, y and z periodic),
    N = 2048, the pair lamp at x = 10 with two arms and the joint labels 00 and 11, the
    train 128, the polarisers at x = 7 (Alice) and 17 (Bob) with their settings, each a
    detector set of one Node reading `sum`, 300 intervals; the clock [2464, 25] on the
    light family and [1, 1] on the counter family (section 1 item 3 and section 15 T-1)."""
    return {
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
            {"name": "counter", "quantum": 1, "phase_per_link": [1, 1]},
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
    setting, the clock [308, 25] on N = 256 (section 14 item 1) on the light family and
    [1, 1] on the counter family (section 5 item 3 and section 15 T-1), written in the
    file (the registered entity references carry no clock)."""
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
        {"name": "counter", "quantum": 1, "phase_per_link": [1, 1]},
    ]
    for entry in rebuilt["measured"]:
        table = entry.get("table", {}).get("light")
        if isinstance(table, dict) and "phase_window" in table:
            table["phase_window"] = setting
    return rebuilt


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
    return out


# Group M1: the massive rows, in the massive record series' form.

MEDIUM = [156, 157]  # omega_0 = 0.1129 (sections 4 and 11)
WELL_HALF = [314, 315]
KIND = [800, 809]  # mu = 0.15
WELL_FULL = [800, 800]
COUPLING = {"G": [1, 50], "g": [1, 1000]}  # section 15 M1-1, with the seed 50 x 2^20
EMITTER_SEED = 50 << 20
AMPLITUDE_BOUND = 1 << 32  # section 15 M1-10, the world key `amplitude_bound` of every massive world
MATTER_CLOCKS = {12: [1089, 320], 16: [11, 4]}  # M1-6: the matter family's `phase_per_link`, N = 64
MATTER_TAKE_PAIRS = {
    12: [-19, 86],
    16: [-5, 27],
}  # M1-6: the take's pair on the matter kind's take lines
MATTER_TRAIN = 8  # periods (150 intervals), section 12 and M1-6
OWN_GRACE = 70  # section 10 item 1 and section 13 item 2: the emitting block's key `own_grace`
LAMP_GRACE = 16700  # M1-6: the matter lamp's `own_grace`, the whole hold


def emitter(position: list[int], side: int, pair: list[int], grace: int | None, **extra: object) -> dict:
    """A block that emits light at G = [1, 50], g = [1, 1000], the seed 50 x 2^20, W = 64
    on its own record; it holds no light content (section 15 M1-2: the emission is the
    coupling's source term); its `own_grace` where its section declares one (sections 10
    and 13: 70; section 4 declares none for 4b's emitter, so the key is absent there)."""
    block: dict = {
        "position": position,
        "side": side,
        "pair": pair,
        "coupling": copy.deepcopy(COUPLING),
        "seed": EMITTER_SEED,
        "wheel": 64,
        "emits": "light",
    }
    if grace is not None:
        block["own_grace"] = grace
    block.update(extra)
    return block


def receiver_set(document: dict, name: str, block: int) -> None:
    """A detector set on the light record bound to the receiving body (section 15 M1-4 and
    the Boss's line of 02:50Z: the one key `block`, the measured number of the body, its
    Nodes the body's current cells) with its own wheel W = 64."""
    document["detectors"].append({"name": name, "block": block, "threshold": 1, "wheel": 64})


def matter_world(
    massive, name: str, shape: list[int], boundary: dict, ticks: int, clock: list[int]
) -> dict:
    """A world of the matter kind [800, 809] alone (no light), its faces open on x, the
    lamp's frequency as the family's `phase_per_link` in the pair form (M1-6)."""
    document = massive.world(name, "PIN", shape, boundary, KIND, [], ticks, faces=massive.FACES_OPEN)
    document["families"] = [family for family in document["families"] if family["name"] != "light"]
    document["families"][0]["phase_per_link"] = list(clock)
    bounded(document)
    return document


def bounded(document: dict) -> None:
    """The amplitude bound of section 15 M1-10 on a massive world, after `massive_record`."""
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
    # Row 4b (section 4 with section 15 M1-1 to M1-5): the chain of 2200, the emitter A of
    # side 12 at the half-depth well, receding on -x at k = 3 from x = 700 over the ramp
    # 1500, 9500 intervals; the control with A at rest at x = 1300; the light detector at
    # x = 1900 and the probe there.
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
            [emitter([x, 0, 0], 12, WELL_HALF, None, **motion)],
            9500,
            light=light_11,
            faces=massive.FACES_OPEN,
            probes=[[1900, 0, 0]],
            mode_axis="x" if motion else None,
        )
        bounded(document)
        document["measured"].append(body([1900, 0, 0], "light", [[-1, 0, 0]]))
        receiver_set(document, "light_detector", 1)
        out[name] = document
    # Row R2 (section 13 with M1-1 to M1-4): two full-depth blocks A at [700, 712) and B at
    # [772, 784) on the chain of 2200, both pushed to k = 3 on +x over the ramp 1500 and the
    # hold 3000, both emitting, x open for the massive kind too (M1-7); each block's cells
    # a detector set on the light record with its own wheel 64 (M1-4, the builder's keys
    # (i) and (ii)); the control with both at rest; the probes at the facing cells.
    for name, motion in (
        ("sagnac_k3", {"momentum": [massive.MOMENTUM_K3, 0, 0], "ramp": 1500}),
        ("sagnac_rest", {}),
    ):
        document = massive.world(
            name.replace("_", "-"),
            "PIN",
            [2200, 1, 1],
            chain,
            KIND,
            [
                emitter([700, 0, 0], 12, WELL_FULL, OWN_GRACE, **motion),
                emitter([772, 0, 0], 12, WELL_FULL, OWN_GRACE, **motion),
            ],
            4500,
            light=light_11,
            faces=massive.FACES_OPEN,
            probes=[[712, 0, 0], [772, 0, 0]],
            mode_axis="x" if motion else None,
        )
        bounded(document)
        receiver_set(document, "at_a", 0)
        receiver_set(document, "at_b", 1)
        out[name] = document
    # The light clock of two bodies (section 10, the third draft, with M1-1 to M1-4): the
    # chain of 673 CLOSED for light at both ends (the loader's third face value, the
    # builder's line), the emitter A of side 12 at full depth at [600, 612), the mirror the
    # closed face at 672, A's cells a detector set on the light record with its own wheel
    # 64 (M1-4), the hold 2000; the probe at the face. N_s = 70 has no key on main.
    document = massive.world(
        "light-clock-60",
        "PIN",
        [673, 1, 1],
        {"x": "closed", "y": "periodic", "z": "periodic"},
        KIND,
        [emitter([600, 0, 0], 12, WELL_FULL, OWN_GRACE)],
        2000,
        light=light_11,
        probes=[[612, 0, 0]],
    )
    bounded(document)
    receiver_set(document, "at_a", 0)
    out["light_clock_60"] = document
    # Rows M1 and M2 (section 12 with section 15 M1-6): the 128 x 128 x 1 layer, y periodic,
    # x open for the matter kind, no light; the matter lamp at (20, 64) with its own clock,
    # the wheel [1, 64], the stock 2048 at one record per 8 intervals, the train 8 periods;
    # the wall at x = 40 a barrier line of matter-kind blocks with the raised pair [1, 2],
    # two deep, the openings at y = 48 and 80 free (the fourth commit); the take lines at
    # x = 0 and 127 absorbing blocks of the matter kind (the fifth commit's correction, the
    # Boss's 02:20Z; their pair not declared); the amplitude bound A = 2^32 of M1-10 under
    # the builder's key, not yet named (a named gap); the screen at
    # x = 104 over y in [4, 124], one set per Node; 16700 intervals. M2 on its own chain of
    # 200: the lamp at x = 20 with one record, the detector at x = 104, 600 intervals.
    for wavelength, clock in MATTER_CLOCKS.items():
        document = matter_world(
            massive,
            f"matter-waves-{wavelength}",
            [128, 128, 1],
            {"x": "open", "y": "periodic", "z": "periodic"},
            16700,
            clock,
        )
        matter_lamp = lamp([20, 64, 0], 2048, [1, 8], [1, 64], [[1, 0, 0]], MATTER_TRAIN, "matter")
        matter_lamp["own_grace"] = LAMP_GRACE
        document["measured"].append(matter_lamp)
        take = MATTER_TAKE_PAIRS[wavelength]
        document["measured"].extend(wall_line([0], range(128), set(), "matter", take, absorbing=True))
        document["measured"].extend(wall_line([40, 41], range(128), {48, 80}, "matter"))
        document["measured"].extend(wall_line([127], range(128), set(), "matter", take, absorbing=True))
        screen(document, 104, range(4, 125), "matter")
        out[f"matter_waves_{wavelength}"] = document
    document = matter_world(massive, "matter-front-12", [200, 1, 1], chain, 600, MATTER_CLOCKS[12])
    document["measured"].append(
        lamp([20, 0, 0], 1, [1, 8], [1, 64], [[1, 0, 0]], MATTER_TRAIN, "matter")
    )
    document["measured"].append(body([104, 0, 0], "matter", [[-1, 0, 0]]))
    document["detectors"].append({"name": "front", "positions": [[104, 0, 0]], "threshold": 1})
    out["matter_front_12"] = document
    return out


def main() -> None:
    massive = load_massive_generator()
    HELD.mkdir(parents=True, exist_ok=True)
    for folder, worlds in (
        (HERE, light_worlds()),
        (HERE, table_worlds()),
        (MASSIVE, massive_worlds(massive)),
    ):
        for name, document in worlds.items():
            path = (HELD if name in HELD_NAMES else folder) / f"{name}.json"
            path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
            print(path.relative_to(EVENTS.parent.parent))


if __name__ == "__main__":
    main()
