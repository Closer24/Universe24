"""The shared world builders and constants of the tests: one copy each, imported by every test that needs them."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

from event_universe.core.rule3 import coefficients
from event_universe.core.step import STEP_FILE
from event_universe.world_files import input_stamp

PERIODIC = {"x": "periodic", "y": "periodic", "z": "periodic"}


DETECTOR_SIDE = 3  # the detector cube's side


EMITTER_KIND = [7, 8]  # the emitter body's kind (omega_0 = 0.505)


EMITTER_PAIR = [
    699,
    700,
]  # the well of the 32-Node emitting body, rich (W = 700 remainder values, ALGEBRA.md #a-familys-declaration) and bound on a chain (2 cos omega_b = 1.9944 over 32 Nodes; the one-Node well [801, 700] of the one-Node giving is a runaway over 32 Nodes, 2.285, its interior above 1)


GIVEN_CLOCK = [
    512,
    1,
]  # the given clock of every light emitter on N = 1024: k = pi / 2, the wavelength 4 (ALGEBRA.md #the-click)


PHASE_STEPS = 1024


TRAIN_LENGTH = 32  # the train's Nodes along K: 8 periods of the wavelength 4


# a sourced family's entry (the source verb's card), the loader tests' one copy
SOURCED = {
    "name": "field",
    "sign": 0,
    "parts": [1],
    "phase": 2,
    "pair": [1000, 1019],
    "quantum": 1,
    "reads": [],
    "self_source": {"unit": 0},
    "sourced": {"of": "matter", "weight": 1, "scale": 18910},
}
HELD_MOMENT = {"count": "sign", "factors": [1, 1], "dipole": "moment", "dipole_div": 2, "divisor": 40000}
HELD_SPIN = {
    "count": "content",
    "factors": [1, 4, 2],
    "dipole": "spin",
    "dipole_div": 1,
    "divisor": 40000,
}
CHARGE_FAMILY_NAME = "charge"


CHARGE_FAMILY = {
    "name": CHARGE_FAMILY_NAME,
    "sign": 0,
    "parts": [1],
    "phase": 2,
    "pair": [1, 1],
    "quantum": 1,
    "held": {"count": "sign", "factors": [1], "divisor": 40000},
    "reads": [],
    "self_source": {"unit": 0},
}


CHARGE_STRENGTH = 1


# the family of clicks holds the content (ALGEBRA.md #the-counts-line) and the family of charge the signed
# charge (ALGEBRA.md #the-paces); a reading family reads the content plainly and the charge by its sign at Lambda
CLOCK_FAMILY_NAME = "clicks"


CLOCK_FAMILY = {
    "name": CLOCK_FAMILY_NAME,
    "sign": 0,
    "parts": [1],
    "phase": 2,
    "pair": [1, 1],
    "quantum": 1,
    "held": {"count": "content", "factors": [1], "divisor": 40000},
    "reads": [],
    "self_source": {"unit": 0},
}


# the Node clock Gamma of every test world (ALGEBRA.md #the-paces, #the-line)
NODE_CLOCK = 10**4


READS = [
    {"family": CLOCK_FAMILY_NAME, "weight": 1, "twist": 0, "by": 1},
    {"family": CHARGE_FAMILY_NAME, "weight": CHARGE_STRENGTH, "twist": 0, "by": "q"},
]


ROOT = Path(__file__).resolve().parents[1]


def shipped() -> dict:
    """The shipped step file, `law/step.json`, as read."""
    return json.loads((ROOT / STEP_FILE).read_text(encoding="utf-8"))


FILE = "examples/events/universe.json"


def chain_world(
    stock: int = 6,
    receiver: object = None,
    on_mode: bool = True,
    faces: str = "closed",
) -> dict:
    """A chain of 80 Nodes (x closed): the emitter body at [2, 34) and the receiver cube `screen` at [70, 72];
    with `faces` "open", a chain of 140 with the face receiver `face` at both ends (ALGEBRA.md #rule3)."""
    length, corner, screen = (140, 34, 100) if faces == "open" else (80, 2, 70)
    document = {
        "shape": [length, 1, 1],
        "boundary": {"x": faces, "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "ticks": 600,
        "N": PHASE_STEPS,
        "engine": "examples/events/engine_start.json",
        "amplitude_bound": 1 << 22,
        "node_clock": NODE_CLOCK,
        "momentum_unit": 64,
        "universe": [
            family_entry("light", [1, 1], reads(), clock=list(GIVEN_CLOCK)),
            family_entry("matter", list(EMITTER_KIND), reads()),
            dict(CLOCK_FAMILY),
            dict(CHARGE_FAMILY),
        ],
        "measured": [
            emitter_body([corner, 0, 0], stock, receiver),
        ],
        "detectors": [],
    }
    receiver_cube(document, "screen", [screen, 0, 0])
    if on_mode:
        seed_on_the_mode(document)
    return document


def cube_positions(shape: list[int], corner: list[int]) -> list[list[int]]:
    """The Nodes of a detector cube of side DETECTOR_SIDE from its lower corner, cut by the
    GameBoard on an axis of extent below the side (a chain's or a layer's thin axis)."""
    return [
        [corner[0] + dx, corner[1] + dy, corner[2] + dz]
        for dx in range(min(DETECTOR_SIDE, shape[0]))
        for dy in range(min(DETECTOR_SIDE, shape[1]))
        for dz in range(min(DETECTOR_SIDE, shape[2]))
    ]


def emitter_body(
    position: list[int],
    stock: int,
    receiver: object = None,
    family: str = "light",
    direction: list[int] | None = None,
    extents: list[int] | None = None,
) -> dict:
    """An emitter body of EMITTER_KIND over the train's 32 Nodes along `direction`, seeded on its mode,
    with its stock and given family, and with `receiver` the given records' ladder by name (ALGEBRA.md #the-click)."""
    emitter: dict = {
        "family": family,
        "weight": 3,  # the window's weight (commit 7; the train retired)
    }
    if receiver is not None:
        emitter["receiver"] = receiver
    if extents is None:
        extents = [1, 1, 1]
        extents[next(index for index, v in enumerate(direction or [1, 0, 0]) if v != 0)] = TRAIN_LENGTH
    return {
        "position": position,
        "family": "matter",
        "amount": 1,
        "ramp": 0,
        "start": 0,
        "stocks": {family: stock},
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
        "extents": extents,
        "q": 0,
        "spin": [0, 0, 0],
        "spin_before": [0, 0, 0],
        "twist": 0,
        "moment": [0, 0, 0],
        "pair": list(EMITTER_PAIR),
        "seed": 1
        << 10,  # the window's writes at the body's Nodes pile up about 300-fold and stay under the bound (commit 7)
        "margin": "control",
        "emitter": emitter,
    }


def layer_world(receiver: object = None) -> dict:
    """A layer of 80 x 9 x 1 (x closed): the emitter across the width at [2, 34) and three detector cubes
    s0, s1, s2 at x in [70, 72]; `receiver` names the ladder's sets in order (ALGEBRA.md #rule3)."""
    measured = [emitter_body([2, 0, 0], 8, extents=[32, 9, 1])]  # the receiver set after the seeding
    document = {
        "shape": [80, 9, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": 400,
        "N": PHASE_STEPS,
        "engine": "examples/events/engine_start.json",
        "amplitude_bound": 1 << 22,
        "node_clock": NODE_CLOCK,
        "momentum_unit": 64,
        "universe": [
            family_entry("light", [1, 1], reads(), clock=list(GIVEN_CLOCK)),
            family_entry("matter", [800, 809], reads()),
            dict(CLOCK_FAMILY),
            dict(CHARGE_FAMILY),
        ],
        "measured": measured,
        "detectors": [],
    }
    for index, y in enumerate((0, 3, 6)):
        receiver_cube(document, f"s{index}", [70, y, 0])
    seed_on_the_mode(document)
    if receiver is not None:
        measured[0]["emitter"]["receiver"] = receiver
        document["stamp"] = input_stamp(document)
    return document


def receiver_body(position: list[int], family: str = "light") -> dict:
    """A fixed receiver body of the family at one Node (a measured event)."""
    return {
        "position": position,
        "family": family,
        "amount": 1,
        "stocks": {},
        "momentum": [0, 0, 0],
        "momentum_before": [0, 0, 0],
    }


def receiver_cube(document: dict, name: str, corner: list[int], family: str = "light") -> None:
    """One detector: a cube of side DETECTOR_SIDE of receiver bodies from `corner`, read as the one set `name`."""
    positions = cube_positions(document["shape"], corner)
    document["measured"].extend(receiver_body(position, family) for position in positions)
    document["detectors"].append({"name": name, "positions": positions})


def _emitter_world(
    stock: int, ticks: int, on_mode: bool, kind: list[int], well: list[int], seed: int, bound: int
) -> dict:
    """The emitter's unit world: a chain of 80 (x closed), an emitter of the matter `kind` in the `well` at [5, 37) on its mode with `stock` givings of light, and the receiver cube `screen` at [70, 72]."""
    # the giving is the window's (ALGEBRA.md #the-primitives): the body's rotation written
    # at its Nodes at the weight 3 (3 x 2^20 under the bound 2^22)
    emitter: dict = {
        "family": "light",
        "receiver": ["screen"],
        "weight": 3,
    }
    document = {
        "shape": [80, 1, 1],
        "boundary": {"x": "closed", "y": "periodic", "z": "periodic"},
        "ticks": ticks,
        "N": 1024,
        "engine": "examples/events/engine_start.json",
        "amplitude_bound": bound,
        "node_clock": NODE_CLOCK,
        "momentum_unit": 64,
        "universe": [
            family_entry("light", [1, 1], reads(), clock=[512, 1]),
            family_entry("matter", kind, reads()),
            dict(CLOCK_FAMILY),
            dict(CHARGE_FAMILY),
        ],
        "measured": [
            {
                "position": [5, 0, 0],
                "family": "matter",
                "amount": 1,
                "ramp": 0,
                "start": 0,
                "stocks": {"light": stock},
                "momentum": [0, 0, 0],
                "momentum_before": [0, 0, 0],
                "extents": [32, 1, 1],
                "q": 0,
                "spin": [0, 0, 0],
                "spin_before": [0, 0, 0],
                "twist": 0,
                "moment": [0, 0, 0],
                "pair": well,
                "seed": seed,  # the window's writes pile up at the body's Nodes (commit 7)
                "margin": "control",
                "emitter": emitter,
            },
        ],
        "detectors": [],
    }
    receiver_cube(document, "screen", [70, 0, 0])
    if on_mode:
        seed_on_the_mode(document)
    return document


def emitter_world(stock: int = 4, ticks: int = 1200, on_mode: bool = True) -> dict:
    """The emitter's unit world as a real body under the count's line: the matter kind [2, 3] (the pair [800, 1200] in lowest terms, so the rule's walls admit the amplitude bound 2^24), the well [200, 201], the seed 2^12 under the bound 2^24; its count stands to the bit."""
    return _emitter_world(stock, ticks, on_mode, [2, 3], [200, 201], 1 << 12, 1 << 24)


def emitter_specimen(stock: int = 4, ticks: int = 1200, on_mode: bool = True) -> dict:
    """The emitter's unit world of old, the loader's and the generator's specimen: the kind [800, 809], the well [800, 801], the seed 2^10 under the bound 2^22 (their tests read the load and the generator's integers on it; under the count's line its count does not stand)."""
    return _emitter_world(stock, ticks, on_mode, [800, 809], [800, 801], 1 << 10, 1 << 22)


def lawful_wheel(world, line: dict) -> bool:
    """A giving line's W, the rule's at the emitting body's read Node with the level the line carries, its u below it."""
    block = world.measured[line["measured"]].block
    at_node, _reads = line["read_clocks"]
    return line["W"] == wheel_of(block.pair, at_node) and 0 <= line["u"] < line["W"]


def load_file(name: str, path: Path):  # type: ignore[no-untyped-def]
    """The module at `path` loaded under `name` and registered in sys.modules (a tool or a generator)."""
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


SEEDS_FILE = (
    ROOT / "tests" / "seeds.json"
)  # the retired generator's seedings of every fixture, recorded once


def _seed_key(document: dict) -> str:
    from event_universe.world_files import input_digest

    bare = json.loads(json.dumps({k: v for k, v in document.items() if k != "stamp"}))
    for entry in bare["universe"] if isinstance(bare.get("universe"), list) else ():
        entry.get("held", {}).pop("divisor", None)  # a key the recorded seeding never read
    return input_digest(bare)


def _seeds() -> dict:
    return json.loads(SEEDS_FILE.read_text(encoding="utf-8"))


def _apply(document: dict, written: dict) -> None:
    document.update(written["top"])
    for index, keys in written["measured"].items():
        document["measured"][int(index)].update(keys)
    document["stamp"] = input_stamp(
        document
    )  # over the document as it stands (the recorded stamp's document)


def seed_on_the_mode(document: dict) -> None:
    """The fixture's bodies seeded on their modes as the retired generator wrote them once (tests/seeds.json): a fixture the table does not hold is refused by name (a new fixture is seeded by the mathematician's tool)."""
    key = _seed_key(document)
    table = _seeds()["seed_on_the_mode"]
    if key not in table:
        raise ValueError(
            f"no recorded seeding for this fixture ({key[:12]}): tests/seeds.json holds the fixtures as recorded"
        )
    _apply(document, table[key])


def emitter_rung(document: dict, number: int) -> None:
    """The emitter's rung (its norm over the loader's period) as the retired generator wrote it once (tests/seeds.json)."""
    _apply(document, _seeds()["emitter_rung"][f"{_seed_key(document)}:{number}"])


def iterated_mode_row(document: dict, number: int, amplitude: int) -> tuple[list[int], list[int]]:
    """The bound mode iterated once by the retired margin module on a fixture's body: its profile and clock (tests/seeds.json)."""
    row = _seeds()["iterated_mode"][f"{_seed_key(document)}:{number}:{amplitude}"]
    return row["profile"], row["clock"]


def mode_profile(document: dict, number: int, amplitude: int) -> list[int]:
    """The bound mode's profile of a fixture's body as the retired generator computed it once (tests/seeds.json)."""
    key = f"{_seed_key(document)}:{number}:{amplitude}"
    row = _seeds()["mode_profile"][key]
    _apply(document, row["written"])
    return row["profile"]


def reads() -> list[dict]:
    """A reading family's `reads`, a fresh copy."""
    return [dict(read) for read in READS]


def family_entry(
    name: str, pair, reads: list[dict], clock=None, sign: int = 0, quantum: int = 1
) -> dict:
    """A family of records in the cards' form (the universe file's entry): one part, two levels,
    its pair, its reads, the self-source off, clicks at the quantum; its clock and sign where given."""
    entry = {
        "name": name,
        "sign": sign,
        "parts": [1],
        "phase": 2,
        "pair": pair,
        "quantum": quantum,
        "reads": reads,
        "self_source": {"unit": 0},
        "clicks": {"gives": True, "takes": True, "quantum": quantum},
    }
    if clock is not None:
        entry["clock"] = list(clock)
    return entry


def wheel_of(pair, content: int, gamma: int = NODE_CLOCK) -> int:
    """The wheel W of the rule at a Node: the wall over the gcd of the rule's three integers (ALGEBRA.md #a-familys-declaration, #the-line)."""
    num, den = int(pair[0]), int(pair[1])
    (read, _, _), self_coefficient, wall = coefficients(num, den, gamma, content)
    return wall // math.gcd(wall, self_coefficient, read)


def on_the_file(document: dict) -> dict:
    """The emitter world on the families file: its path, no integers of its own, light the charge family (the given clock its row's), the emitter body of matter."""
    moved = json.loads(json.dumps(document))
    names = {family["name"]: family for family in moved["universe"]}
    moved["universe"] = FILE
    del moved["node_clock"]
    del moved["amplitude_bound"]
    del moved["momentum_unit"]
    for entry in moved["measured"]:
        if entry["family"] == "light":
            entry["family"] = "charge"
        if entry["family"] == "matter":
            entry["kind"] = list(names["matter"]["pair"])
        if "light" in entry.get("stocks", {}):
            entry["stocks"] = {"charge": entry["stocks"]["light"]}
        if "emitter" in entry:
            if entry["emitter"]["family"] == "light":
                entry["emitter"]["family"] = "charge"
            # the light's component along the body's moment (ALGEBRA.md #the-second-level; commit 4)
            entry["moment"] = [0, 0, 1]
    moved["stamp"] = input_stamp(moved)
    return moved
