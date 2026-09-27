"""THE CHECK-MODE WORLDS (ALGEBRA.md and (5), 9.92, ALGEBRA.md #rule3; the Boss's records 2128,
2130, 2132 and 2133 (2) of 2026-09-26): one generator for the rows of the check-mode table
of the new physics and for the all-families world, each with its blind expectation in the
README beside it, no pin. THE WORDS are record 2128's: a world names its `universe`
(`examples/events/universe.json`), a body's signed number is `q`, its stocks of other
families' quanta `stocks`. NO MOMENTUM AND NO SPIN IS DECLARED (record 2130; ALGEBRA.md #rule3): a
moving body is its record with its tail, written by this generator at the wave number K whose
group pace is the row's v (ALGEBRA.md #the-generator) at both levels; a spinning body is its record's winding,
not built here (the winding's line is owed, README section 4).

The bodies are seeded on the bound mode by the massive generator's own operator (its
`seed_on_the_mode`, HOST), in the loader's words of today, and the document is then written in
record 2128's words. Until the engine's writer lands the words (record 2133, The 3), these
files load in no loader: `tests/test_check_mode_worlds.py` reads their structure. Every number
in the README is labelled: DETECTOR (a click), GAMEBOARD (a diagnostic), COMPUTATION (the
declaration's arithmetic), HOST (the machine's cost).

    PYTHONPATH=src python examples/events/check_mode/make_worlds.py [name ...]
"""

from __future__ import annotations

import copy
import importlib.util
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
EVENTS = HERE.parent


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


massive = load(EVENTS / "massive_record" / "make_worlds.py", "check_mode_massive")

# THE WORDS OF RECORD 2128 (the Boss's word on the owner's delegation, 2026-09-26)
UNIVERSE_KEY = "universe"
UNIVERSE_FILE = "examples/events/universe.json"
CHARGE_NUMBER = "q"  # the body's signed number Q of ALGEBRA.md #the-paces
STOCKS_KEY = (
    "stocks"  # the body's stocks of other families' quanta (beside ALGEBRA.md #the-primitives's `stock`)
)
# the world keys the audit of ALGEBRA.md #the-primitives deletes, and the keys that live in the universe file or
# the start file (FAMILIES, START); `families` becomes `universe`
DELETED_WORLD_KEYS = (
    "law",
    "model_id",
    "K",
    "N",
    "release",
    "width",
    "clock_stamp",
    "detector_law",
    "massive_record",
    "body_record",
    "point_emitter",
    "age_bound",
    "amplitude_bound",
    "node_clock",
    "input",
    "probes",
    "mode_axis",
)
# a body declares no momentum, no spin and no moment (record 2130); the margin kind is the
# start file's (ALGEBRA.md #the-primitives START)
DELETED_BLOCK_KEYS = ("momentum", "spin", "moment", "margin")

GAMMA = massive.NODE_CLOCK  # the Node clock, 10^4 (ALGEBRA.md #the-line)
# THE BODIES' REST PAIR AND WELL (a HOST probe of 2026-09-26, README section 1): on a GameBoard
# open on three axes the shipped kind [800, 809] binds no mode on a well of side 5, 7 or 9 (the
# band's depth ceiling 2 - 2 x 800 / 809 = 0.022 is too shallow for a small well in three
# dimensions; a well of side 13 binds, too wide for bodies 10 Links apart); the kind [800, 850]
# (the rest rotation omega_0 = 0.345 per interval) binds a well of side 5 at the pair [800, 801]
# and a layer's well of side 5 alike. A one-Node well binds nothing: a body that moves has its
# tail on a well of side 5 (ALGEBRA.md #rule3).
KIND = [800, 850]
WELL = [800, 801]
SEED = 1 << 12  # the record's amplitude
OPEN = {"x": "open", "y": "open", "z": "open"}
LAYER = {"x": "open", "y": "open", "z": "periodic"}
FACE_DEPTH = 1  # every open face a receiver slab one Node deep: the faces are the counters (ALGEBRA.md #the-rows-against-nature)
CUBE = [48, 48, 48]  # the all-families world's GameBoard (ALGEBRA.md)
CENTRE = 24

# THE BODIES OF ALGEBRA.md: M = 2000 quanta each, 10 Links apart, on circles of radius 5 about
# the centre, v = 0.1 along the orbit; Lambda Q = 50 with Lambda = 1 (the universe file's)
BODY_QUANTA = 2000
BODY_SIDE = 5
PAIR_SEPARATION = 10
ORBIT_SPEED = 0.1  # Links per interval (COMPUTATION, ALGEBRA.md)
ORBIT_PERIOD = 314  # intervals with gravity alone (COMPUTATION, ALGEBRA.md)
CHARGE_Q = 50
EMITTER_STOCK = 200
EMITTER_WEIGHT = 4  # the point emitter's window g (ALGEBRA.md)
ORBITS = 10

# NEWTON'S FALL (ALGEBRA.md, the first row): two bodies of equal content from rest at 20 Links
FALL_SEPARATION = 20

# THE CHARGE ROWS (ALGEBRA.md #the-rows-against-nature) AND MAGNETISM (ALGEBRA.md #a-familys-declaration): the layer [200, 120, 1], a source
# of side 10 with Q = +-400 and a small content, a charged packet at v = 1 / 4 passing at
# b = 20, the screen 100 Links beyond the source's centre (pixels, one per Node, ALGEBRA.md #the-rows-against-nature)
LAYER_SHAPE = [200, 120, 1]
SOURCE_SIDE = 10  # R = 5 (ALGEBRA.md #the-rows-against-nature)
SOURCE_CENTRE = [100, 60]
SOURCE_Q = 400
SOURCE_QUANTA = 64
PACKET_Q = -1
PACKET_QUANTA = 1
PACKET_SIDE = 5
PACKET_START_X = 10
IMPACT = 20  # b, the closest distance (Links)
PACKET_SPEED = 0.25
SCREEN_X = 199  # the screen's column, 100 Links beyond the source's centre, at the face
PASS_TICKS = 800  # (199 - 12) / 0.25 = 748 intervals of flight (COMPUTATION)

# THE RECOIL ROWS (ALGEBRA.md #the-primitives): a body of M = 64 in a beam of 100 quanta along +x, the same
# body beside the beam, the emitter of 10 quanta as a train and as a point, the heavy tool
BEAM_SHAPE = [400, 21, 21]
# the beam board wraps across (an emitter must stand one train's length from every face slab,
# ALGEBRA.md #the-ladder; across a wrapped axis there is no slab): its counters are the two x faces
BEAM_BOUNDARY = {"x": "open", "y": "periodic", "z": "periodic"}
BEAM_EMITTER_CORNER = [100, 8, 8]
BEAM_EXTENTS = [32, 5, 5]  # the train's length, its cross-section [8, 13) across
BEAM_QUANTA = 100
RECOIL_QUANTA = 10
TARGET_QUANTA = 64
TARGET_X = 298  # the target's corner: its well of side 5 centred at x = 300
TARGET_IN_BEAM = [TARGET_X, 8, 8]  # in the beam's cross-section
TARGET_BESIDE = [
    TARGET_X,
    1,
    1,
]  # its Nodes [1, 6) across, outside the beam's [8, 13), inside the free Nodes
HEAVY_QUANTA = 1_000_000
BEAM_TICKS = 10_400  # 100 givings at the emitter's period plus the flight (COMPUTATION)
RECOIL_TICKS = 1_400

TRAIN_PERIODS = 8
TRAIN_PHASE_STEPS = 1024


def body(position: list[int], extents: list[int], amount: int, q: int = 0, **extra: object) -> dict:
    """A body of matter at rest: a well of `extents` at `position` (its corner), `amount` quanta,
    its signed number `q`, its record seeded on the bound mode; the loader's words of today
    (`translate` writes record 2128's)."""
    block: dict = {
        "position": list(position),
        "extents": list(extents),
        "amount": amount,
        "pair": list(WELL),
        "kind": list(KIND),
        "seed": SEED,
        "q": q,
    }
    block.update(extra)
    return block


def build(
    name: str,
    shape: list[int],
    boundary: dict[str, str],
    blocks: list[dict],
    ticks: int,
    train: bool = False,
) -> dict:
    """The document in the loader's words of today, every body seeded on the mode of ITS OWN
    WORLD with the other bodies absent (ALGEBRA.md #the-primitives, #the-generator: the separation rule of
    9.35 is retired; the eigenproblem is per body), HOST: the massive generator's
    `seed_on_the_mode` on a copy holding that body alone, its seed, clock and emitter keys
    copied back."""
    document = massive.world(
        name,
        "CHECK",
        shape,
        boundary,
        KIND,
        blocks,
        ticks,
        seed_profile=False,
    )
    if train:
        document["N"] = (
            TRAIN_PHASE_STEPS  # the train's wavelength a whole number of Links (ALGEBRA.md #the-click)
        )
    if any(value == "open" for value in boundary.values()):
        document["face_depth"] = FACE_DEPTH
    for number, entry in enumerate(document["measured"]):
        alone = copy.deepcopy(document)
        alone["measured"] = [copy.deepcopy(entry)]
        massive.seed_on_the_mode(alone)
        document["measured"][number] = alone["measured"][0]
    return document


def centre_of(entry: dict) -> list[int]:
    extents = [int(entry["side"])] * 3 if "side" in entry else [int(v) for v in entry["extents"]]
    return [int(entry["position"][axis]) + extents[axis] // 2 for axis in range(3)]


def move(document: dict, number: int, velocity: list[float]) -> dict[str, float]:
    """THE MOVING BODY AS ITS RECORD (ALGEBRA.md #rule3, #the-generator; record 2130): the body's
    standing profile p (the mode, `seed_on_the_mode`) times the character of K along the one
    axis of motion, K the wave number at which the mode's own group pace equals |v| on its
    dispersion (`moving_rotation`), at both levels: now = round(p cos(K dx + omega_K / 2)),
    before = round(p cos(K dx - omega_K / 2)), dx the Node's distance from the body's centre
    along the axis in the sense of v, omega_K the moving mode's rotation per interval; at K = 0
    both levels are the standing profile scaled by cos(omega / 2), the standing start's
    symmetric point. Written as `seed: {"now": [...], "before": [...]}` over the whole board,
    x-major (the loader's hook for The 3, README section 4). Returns the HOST numbers K,
    omega_K and the rotation at the moving centre omega_K - K v for the README."""
    axes = [axis for axis in range(3) if velocity[axis] != 0.0]
    if len(axes) != 1:
        raise ValueError(
            f"measured[{number}]: a body moves along one axis; {velocity} moves along {len(axes)}"
        )
    axis = axes[0]
    speed = abs(velocity[axis])
    two_cos_rest, quotient = massive.mode_dispersion(document, number, axis)
    wavenumber, rotation = massive.moving_rotation(float(two_cos_rest), float(quotient), speed)
    omega = math.acos((float(two_cos_rest) - (1.0 - math.cos(wavenumber)) * float(quotient)) / 2.0)
    entry = document["measured"][number]
    shape = [int(v) for v in document["shape"]]
    profile = np.array(entry["seed"], dtype=np.int64).reshape(shape)
    centre = centre_of(entry)[axis]
    coordinate = np.arange(shape[axis], dtype=np.int64)
    distance = coordinate - centre
    if document["boundary"]["xyz"[axis]] == "periodic":
        distance = (distance + shape[axis] // 2) % shape[axis] - shape[axis] // 2
    phase = math.copysign(1.0, velocity[axis]) * wavenumber * distance.astype(np.float64)
    form = [1, 1, 1]
    form[axis] = shape[axis]
    now = np.rint(profile * np.cos(phase + omega / 2.0).reshape(form)).astype(np.int64)
    before = np.rint(profile * np.cos(phase - omega / 2.0).reshape(form)).astype(np.int64)
    entry["seed"] = {"now": now.ravel().tolist(), "before": before.ravel().tolist()}
    return {"wavenumber": wavenumber, "omega": omega, "rotation": rotation, "speed": speed}


def translate(document: dict) -> dict:
    """The document in record 2128's words and ALGEBRA.md #the-primitives's keys: `universe` by path in place
    of the families list, `q` for the body's signed number, `stocks` for its held quanta; no
    momentum, spin, moment or margin on a body (records 2130 and ALGEBRA.md #the-primitives); the deleted
    world keys gone; the key order the world's (shape, boundary, ticks, ...)."""
    out: dict = {}
    for key, value in document.items():
        if key in DELETED_WORLD_KEYS:
            continue
        if key in ("families", UNIVERSE_KEY):
            out[UNIVERSE_KEY] = UNIVERSE_FILE  # the inline list to the file's path
            continue
        out[key] = value
    measured = []
    for entry in document["measured"]:
        block: dict = {}
        for key, value in entry.items():
            if key in DELETED_BLOCK_KEYS:
                continue
            if key == "charge":
                block[CHARGE_NUMBER] = value
            elif key == "held":
                block[STOCKS_KEY] = value
            elif key == "emitter":
                block[key] = dict(value)
            else:
                block[key] = value
        measured.append(block)
    out["measured"] = measured
    return out


def screen(x: int, shape: list[int]) -> list[dict]:
    """A screen (ALGEBRA.md #the-rows-against-nature): pixels, one detector per Node of the column x, the pattern
    compared."""
    return [
        {"name": f"screen_{y}", "positions": [[x, y, z] for z in range(shape[2])]}
        for y in range(FACE_DEPTH, shape[1] - FACE_DEPTH)
    ]


def corner(centre: list[int], side: int) -> list[int]:
    return [c - side // 2 for c in centre]


def pair_blocks(q: int) -> list[dict]:
    """The two bodies of ALGEBRA.md: A at the centre minus 5 along x, B at the centre plus 5,
    each of M = 2000 on a well of side 5."""
    half = PAIR_SEPARATION // 2
    a = body(corner([CENTRE - half, CENTRE, CENTRE], BODY_SIDE), [BODY_SIDE] * 3, BODY_QUANTA, q)
    b = body(corner([CENTRE + half, CENTRE, CENTRE], BODY_SIDE), [BODY_SIDE] * 3, BODY_QUANTA, q)
    return [a, b]


def orbit(document: dict) -> dict[str, dict[str, float]]:
    """The pair in its orbit about the centre: A moves along +y, B along -y at v = 0.1
    (the tangents of the circles of radius 5 at the bodies' start)."""
    return {
        "A": move(document, 0, [0.0, ORBIT_SPEED, 0.0]),
        "B": move(document, 1, [0.0, -ORBIT_SPEED, 0.0]),
    }


def newton_fall() -> tuple[dict, dict]:
    half = FALL_SEPARATION // 2
    blocks = [
        body(corner([CENTRE - half, CENTRE, CENTRE], BODY_SIDE), [BODY_SIDE] * 3, BODY_QUANTA),
        body(corner([CENTRE + half, CENTRE, CENTRE], BODY_SIDE), [BODY_SIDE] * 3, BODY_QUANTA),
    ]
    document = build("newton-fall", CUBE, OPEN, blocks, 400)
    return document, {}


def kepler_pair() -> tuple[dict, dict]:
    document = build("kepler-pair", CUBE, OPEN, pair_blocks(0), ORBITS * ORBIT_PERIOD + ORBIT_PERIOD)
    return document, orbit(document)


def all_families() -> tuple[dict, dict]:
    """THE ALL-FAMILIES WORLD (ALGEBRA.md with ALGEBRA.md #the-rows-against-nature): the pair with Lambda Q = 50 on both, A a
    point emitter of 200 quanta of the charge family's wave at its window g = 4, the six faces
    the counters (an open face is a detector of its name), no D. A's spin S = 1000 is its
    record's winding and waits for the winding's line (README section 4)."""
    blocks = pair_blocks(CHARGE_Q)
    blocks[0]["stocks"] = {massive.WAVE_FAMILY_NAME: EMITTER_STOCK}
    blocks[0]["emitter"] = {"family": massive.WAVE_FAMILY_NAME}
    document = build("all-families", CUBE, OPEN, blocks, ORBITS * 363 + 363)
    document["measured"][0]["emitter"]["weight"] = EMITTER_WEIGHT
    return document, orbit(document)


def source_block(q: int) -> dict:
    return body(
        corner(SOURCE_CENTRE, SOURCE_SIDE) + [0], [SOURCE_SIDE, SOURCE_SIDE, 1], SOURCE_QUANTA, q
    )


def packet_block(q: int) -> dict:
    return body(
        [PACKET_START_X, SOURCE_CENTRE[1] + IMPACT - PACKET_SIDE // 2, 0],
        [PACKET_SIDE, PACKET_SIDE, 1],
        PACKET_QUANTA,
        q,
    )


def pass_world(name: str, source_q: int, packet_q: int, source_speed: float) -> tuple[dict, dict]:
    """The charge rows and magnetism on the layer: the source at rest or hopping along x at
    +-1 / 4, the packet passing at v = 1 / 4 along +x at b = 20, the screen at the far face."""
    document = build(
        name, LAYER_SHAPE, LAYER, [source_block(source_q), packet_block(packet_q)], PASS_TICKS
    )
    document["detectors"] = screen(SCREEN_X, LAYER_SHAPE)
    readings = {"packet": move(document, 1, [PACKET_SPEED, 0.0, 0.0])}
    if source_speed != 0.0:
        readings["source"] = move(document, 0, [source_speed, 0.0, 0.0])
    return document, readings


def beam_emitter(stock: int, train: bool) -> dict:
    block = body(BEAM_EMITTER_CORNER, BEAM_EXTENTS, TARGET_QUANTA)
    block["stocks"] = {massive.WAVE_FAMILY_NAME: stock}
    # the given family's clock is its row's (ALGEBRA.md #the-primitives, L479)
    emitter: dict = {"family": massive.WAVE_FAMILY_NAME}
    if train:
        emitter["train"] = {"direction": [1, 0, 0], "periods": TRAIN_PERIODS}
    block["emitter"] = emitter
    return block


def target_body(position: list[int], amount: int) -> dict:
    """The recoil rows' target: a body on a well of side 5, with the tail a hop needs (ALGEBRA.md #rule3;
    a one-Node well binds no mode, the README's probe)."""
    return body(position, [BODY_SIDE] * 3, amount)


def radiation_pressure(beside: bool) -> tuple[dict, dict]:
    target = target_body(TARGET_BESIDE if beside else TARGET_IN_BEAM, TARGET_QUANTA)
    name = "radiation-pressure-beside" if beside else "radiation-pressure"
    return build(
        name,
        BEAM_SHAPE,
        BEAM_BOUNDARY,
        [beam_emitter(BEAM_QUANTA, True), target],
        BEAM_TICKS,
        train=True,
    ), {}


def heavy_tool() -> tuple[dict, dict]:
    target = target_body(TARGET_IN_BEAM, HEAVY_QUANTA)
    return build(
        "heavy-tool",
        BEAM_SHAPE,
        BEAM_BOUNDARY,
        [beam_emitter(BEAM_QUANTA, True), target],
        BEAM_TICKS,
        train=True,
    ), {}


def recoil(train: bool) -> tuple[dict, dict]:
    name = "train-recoil" if train else "point-recoil"
    document = build(
        name, BEAM_SHAPE, BEAM_BOUNDARY, [beam_emitter(RECOIL_QUANTA, train)], RECOIL_TICKS, train=train
    )
    if not train:
        document["measured"][0]["emitter"]["weight"] = EMITTER_WEIGHT
    return document, {}


WORLDS = {
    "newton_fall": newton_fall,
    "kepler_pair": kepler_pair,
    "all_families": all_families,
    "coulomb_plus": lambda: pass_world("coulomb-plus", SOURCE_Q, PACKET_Q, 0.0),
    "coulomb_minus": lambda: pass_world("coulomb-minus", -SOURCE_Q, PACKET_Q, 0.0),
    "coulomb_neutral": lambda: pass_world("coulomb-neutral", 0, PACKET_Q, 0.0),
    "coulomb_neutral_packet": lambda: pass_world("coulomb-neutral-packet", SOURCE_Q, 0, 0.0),
    "ampere_parallel": lambda: pass_world("ampere-parallel", SOURCE_Q, PACKET_Q, PACKET_SPEED),
    "ampere_opposite": lambda: pass_world("ampere-opposite", SOURCE_Q, PACKET_Q, -PACKET_SPEED),
    "radiation_pressure": lambda: radiation_pressure(False),
    "radiation_pressure_beside": lambda: radiation_pressure(True),
    "train_recoil": lambda: recoil(True),
    "point_recoil": lambda: recoil(False),
}


INTEGER_LIST = re.compile(r"\[\s+(-?\d+(?:,\s+-?\d+)*)\s+\]")


def dumps(document: dict) -> str:
    """The file's text: the keys one per line, every list of integers on one line (a record
    over the whole board is 110592 integers; HOST, the file's size)."""
    text = json.dumps(document, indent=1)
    return INTEGER_LIST.sub(lambda m: "[" + re.sub(r"\s+", " ", m.group(1)) + "]", text) + "\n"


# THE WORLDS THAT WAIT FOR A LINE (README section 4), named here so that a run by name still
# writes them once the line lands
WAITING = {
    "heavy_tool": (
        heavy_tool,
        "a body of a million quanta is refused by the pace guard until P_0 = [1, 1000] lands "
        "(ALGEBRA.md #the-primitives, the stroke's commit 5): today the amount is the content at the "
        "Node, and 10^6 is not below Gamma = 10^4",
    ),
}


def main() -> None:
    names = sys.argv[1:] or list(WORLDS)
    for name in names:
        if name in WAITING:
            print(name, "WAITS:", WAITING[name][1])
        document, readings = (WORLDS.get(name) or WAITING[name][0])()
        written = translate(document)
        path = HERE / f"{name}.json"
        path.write_text(dumps(written), encoding="utf-8")
        summary = {
            body_name: {k: round(v, 5) for k, v in numbers.items()}
            for body_name, numbers in readings.items()
        }
        print(
            path.name,
            "shape",
            written["shape"],
            "ticks",
            written["ticks"],
            "bodies",
            len(written["measured"]),
            "HOST K",
            summary,
        )


if __name__ == "__main__":
    main()
