"""The shared builders of worlds with bodies (massive records, emitters on chains, parts) for the tests: one copy each."""

from __future__ import annotations

import json

import numpy as np

from event_universe.events.detector_law import DetectorLawSimulation
from event_universe.world_files import input_stamp
from tests.worlds import (
    CHARGE_FAMILY,
    CHARGE_FAMILY_NAME,
    CLOCK_FAMILY,
    NODE_CLOCK,
    chain_world,
    emitter_body,
    family_entry,
    massive_generator,
    reads,
    receiver_cube,
)

PACES_SHAPE = [10, 6, 6]


LIGHT, MATTER, NEUTRAL, CLICKS, CHARGE = range(5)  # the charged chain's families in order


QUANTA = 10  # the content and the charge per Node of the charged slab (ten Nodes) at GAMMA


SOURCE_KIND = [7, 8]  # the emitter bodies' own kind (omega_0 = 0.505; the index worlds')


SOURCE_WELL = [
    699,
    700,
]  # its well over the train's 32 Nodes, rich (W = 700, ALGEBRA.md #a-familys-declaration) and bound (2 cos omega_b = 1.9944 on a chain; the one-Node giving's [801, 700] is a runaway over 32 Nodes, its interior above 1)


CHAIN = {"x": "open", "y": "periodic", "z": "periodic"}


GAMMA = 1000  # the suite's Node clock (declared per world like the pairs; the eighteen's 10^6)


PAIR = (800, 809)  # the matter kind


POINT_KIND = [800, 813]


POINT_WELL = [800, 802]


CLOSED_CHAIN = {"x": "closed", "y": "periodic", "z": "periodic"}


KIND = [800, 809]


SHAPE = [16, 8, 8]


WELL = [800, 801]


def paces_world() -> dict:
    """A periodic board with a body of matter at rest and the families with parts (gravity
    [1, 3, 6] holding the content); the matter family reads gravity's time part at 1."""
    block = {"position": [3, 2, 2], "side": 3, "pair": WELL, "margin": "control"}
    periodic = {"x": "periodic", "y": "periodic", "z": "periodic"}
    document = block_world(PACES_SHAPE, periodic, KIND, [block], ticks=20)
    document["age_bound"] = 100000
    for family in document["universe"]:
        if family["name"] == "clicks":
            family.update(
                {
                    "parts": [1, 3, 6],
                    "held": {
                        "count": "content",
                        "factors": [1, 4, 2],
                        "dipole": "spin",
                        "dipole_div": 1,
                    },
                    "spins_step": {"curl": [1, 4], "tidal": [3, 4]},
                }
            )
    document["stamp"] = input_stamp(document)
    return document


def with_body_record(document: dict, on: bool) -> dict:
    """The document with `body_record` set and the input stamp renewed over the whole file."""
    copy = json.loads(json.dumps(document))
    copy["body_record"] = on
    copy["stamp"] = input_stamp(copy)
    return copy


def charged_chain(
    length: int,
    boundary: dict,
    nodes,
    amount: int,
    light_charge: int,
    matter_charge: int,
    strength: int = 1,
) -> dict:
    """A chain of `length` under GAMMA: light bodies of `amount` quanta at `nodes`, light and matter charged,
    a neutral fifth family, and Lambda = `strength`."""
    document = content_chain(length, boundary, nodes, amount)
    document["universe"][LIGHT]["sign"] = light_charge
    document["universe"][MATTER]["sign"] = matter_charge
    document["universe"].insert(
        NEUTRAL,
        family_entry("neutral", [1, 1], reads(), clock=[512, 1]),
    )
    set_strength(document, strength)
    return document


def set_strength(document: dict, strength: int) -> None:
    """Lambda on every reading family: the weight of its read on the family of charge (the
    family genericity, BUILD.md section 26 item 51)."""
    for family in document["universe"]:
        for read in family.get("reads", []):
            if read["family"] == CHARGE_FAMILY_NAME:
                read["weight"] = strength


def block_world(
    shape: list[int],
    boundary: object,
    kind: list[int],
    blocks: list[dict],
    source: dict | None = None,
    ticks: int = 100,
) -> dict:
    """A world of the massive kind `matter` with blocks, a light family on the clock [77, 25], and optionally
    an emitter body of light (`emitter_at`) as the first measured event, seeded on its mode."""
    matter: dict = family_entry("matter", kind, reads())
    # light on the given clock [512, 1] of N = 1024 (the given train, ALGEBRA.md #the-click)
    families = [
        family_entry("light", [1, 1], reads(), clock=[512, 1]),
        matter,
    ]
    measured: list[dict] = []
    if source is not None:
        measured.append(source)
        families.append(source_family())
    families.append(dict(CHARGE_FAMILY))  # the family of charge
    families.append(dict(CLOCK_FAMILY))  # the family of clicks
    for block in blocks:
        entry = {
            "position": block["position"],
            "family": "matter",
            "amount": block.get("amount", 1),
            "stocks": {},
            "ramp": 0,
            "start": 0,
            "momentum": block.get("momentum", [0, 0, 0]),
            "fixed": block.get("fixed", False),
            "side": block["side"],
            "pair": block["pair"],
            # the body's numbers (ALGEBRA.md #the-interval; commit 2), no loader default
            "q": block.get("q", 0),
            "spin": block.get("spin", [0, 0, 0]),
            "moment": block.get("moment", [0, 0, 0]),
            "twist": block.get("twist", 0),  # the generator's number; 0 where no read by "own" (item 73)
        }
        for key in (
            "seed",
            "ramp",
            "start",
            "margin",
            "stocks",
            "receiver",
            "emitter",
        ):
            if key in block:
                entry[key] = block[key]
        if block["pair"][0] * kind[1] > block["pair"][1] * kind[0]:
            # every well declares its seed (the suite's amplitude 2^20 where a test names
            # none) and its margin kind: no loader default
            if "seed" not in entry:
                entry["seed"] = 1 << 20
            entry.setdefault("margin", "pin")
        measured.append(entry)
    document: dict = {
        "shape": shape,
        "boundary": boundary,
        "face_depth": 1,
        "ticks": ticks,
        "N": 1024,
        "clock_stamp": True,
        "age_bound": 100000,
        "body_record": False,
        "engine": "examples/events/engine_start.json",
        "massive_record": True,
        "amplitude_bound": 1 << 22,
        "node_clock": NODE_CLOCK,
        "momentum_unit": 64,
        "universe": families,
        "measured": measured,
        "detectors": [],
    }
    if source is not None:
        seed_source(document, 0)
    return document


def emitter_at(
    x: int,
    stock: int = 1,
    family: str = "light",
    own: str = "source",
    pair: list[int] | None = None,
    receiver: object = None,
) -> dict:
    """An emitter body on a chain from x: the well of the family `own` over the train's 32 Nodes, seeded
    on its mode, with `stock` givings of `family` and, with `receiver`, the ladder by name (ALGEBRA.md #the-click)."""
    entry = emitter_body([x, 0, 0], stock, receiver=receiver, family=family)
    entry["family"] = own
    entry["pair"] = list(pair or SOURCE_WELL)
    return entry


def light_clock_world(faces: str, far_body: bool) -> dict:
    """A chain of 173 (x closed, or open with `faces`): the emitter A at [100, 132) giving one train of light,
    the set `A_face` at its head, and with `far_body` the cube `far` at [160, 162]."""
    document = massive_world([173, 1, 1], {"x": faces, "y": "periodic", "z": "periodic"}, [800, 809])
    document["ticks"] = 600
    document["clock_stamp"] = True
    document["measured"] = [
        {
            "position": [100, 0, 0],
            "family": "matter",
            "amount": 1,
            "ramp": 0,
            "start": 0,
            "stocks": {"light": 1},
            "momentum": [0, 0, 0],
            "fixed": False,
            "extents": [32, 1, 1],
            "q": 0,
            "spin": [0, 0, 0],
            "twist": 0,
            "moment": [0, 0, 0],
            "pair": [800, 801],
            "seed": 1
            << 10,  # the window's writes at the body's Nodes pile up about 300-fold and stay under the bound (commit 7)
            "emitter": {"family": "light", "weight": 3, "twist": 0},  # the window (commit 7)
            "margin": "control",
            # the receiver by name (section 13 item 7): A's own bound set
            "receiver": "A_face",
        }
    ]
    document["detectors"] = [
        {"name": "A_face", "block": 0, "positions": [[132, 0, 0], [133, 0, 0], [134, 0, 0]]}
    ]
    if far_body:
        receiver_cube(document, "far", [160, 0, 0])
    seed_source(document, 0)
    return document


def massive_world(shape: list[int], boundary: object, pair: list[int]) -> dict:
    """A world of the massive kind `matter` beside light, with no emitter and no block; the face slab one Node
    deep where the board is open."""
    matter: dict = family_entry("matter", pair, reads())
    return {
        "shape": shape,
        "boundary": boundary,
        "face_depth": 1,
        "ticks": 10,
        "N": 1024,
        "clock_stamp": False,
        "age_bound": 100000,
        "body_record": False,
        "engine": "examples/events/engine_start.json",
        "massive_record": True,
        "amplitude_bound": 1 << 22,
        "node_clock": NODE_CLOCK,
        "momentum_unit": 64,
        "universe": [
            family_entry("light", [1, 1], reads(), clock=[512, 1]),
            matter,
            dict(CLOCK_FAMILY),
            dict(CHARGE_FAMILY),
        ],
        "measured": [],
        "detectors": [],
    }


def matter_emitter_world(matter_emitter: bool, clock: list[int] | None = None, stock: int = 1) -> dict:
    """A chain of 200 Nodes (x open): the light emitter at [2, 34) beside the massive kind `matter`, and with
    `matter_emitter` an emitter at [100, 132) giving `matter`; `clock` None declares no clock."""
    document = chain_world(on_mode=False)
    document["shape"] = [200, 1, 1]
    document["ticks"] = 160
    document["universe"][1]["name"] = "source"
    document["measured"][0]["family"] = "source"
    matter: dict = family_entry("matter", [156, 157], reads())
    if clock is not None:
        matter["clock"] = clock  # None: no clock (the refusal's edge case)
    document["universe"].append(matter)
    document["measured"] = document["measured"][:1]
    if matter_emitter:
        document["measured"].append(emitter_at(100, stock, family="matter"))
    document["detectors"] = []
    massive_generator().seed_on_the_mode(document)
    return document


def seed_source(document: dict, number: int) -> None:
    """The measured event `number` seeded on its bound mode at its scalar seed, its `margin` made explicit."""
    entry = document["measured"][number]
    entry.setdefault("margin", "control")
    generator = massive_generator()
    entry["seed"] = generator.mode_profile(document, number, amplitude=entry["seed"])
    if "emitter" in entry:
        generator.emitter_rung(document, number)  # the window's rung
    # the input stamp: the law and the hash of the integers
    document["stamp"] = input_stamp(document)


def source_family() -> dict:
    """The emitter bodies' massive family `source` (the kind SOURCE_KIND, no clock)."""
    return family_entry("source", list(SOURCE_KIND), reads())


def content_chain(length: int, boundary: dict, nodes, amount: int, gamma: int = GAMMA) -> dict:
    """The chain [length, 1, 1] of the matter kind [800, 809] beside light with `amount` quanta
    held at each Node of `nodes` (a light body per Node) under the Node clock `gamma`."""
    document = massive_world([length, 1, 1], boundary, list(PAIR))
    document["age_bound"] = 100000
    document["node_clock"] = gamma
    document["amplitude_bound"] = 1 << 26  # the rows at UNIT have room under the suite's Gamma = 1000
    document["measured"] = [light_body(x, amount) for x in nodes]
    return document


def light_body(x: int, amount: int) -> dict:
    """A measured event of light at one Node holding `amount` quanta (a body of content)."""
    return {
        "position": [x, 0, 0],
        "family": "light",
        "amount": amount,
        "stocks": {},
        "momentum": [0, 0, 0],
        "fixed": False,
    }


def six_reads(levels: np.ndarray, wrap_x: bool) -> list[int]:
    """S_6 on a chain (y and z of extent 1 read the Node itself twice each): a_W + a_E + 4 a,
    the ends reading 0 beyond an open x."""
    values = [int(v) for v in levels[:, 0, 0]]
    length = len(values)
    out = []
    for x in range(length):
        west = values[(x - 1) % length] if wrap_x or x > 0 else 0
        east = values[(x + 1) % length] if wrap_x or x < length - 1 else 0
        out.append(west + east + 4 * values[x])
    return out


def point_world(weight: int, stock: int = 2, ticks: int = 4000, length: int = 400) -> dict:
    """The chain with the one-Node point emitter at its middle; the mode seeded first (as
    `body_record`), the keys and the weight set after, the stamp renewed."""
    document = massive_world([length, 1, 1], CHAIN, POINT_KIND)
    document["ticks"] = ticks
    document["clock_stamp"] = True
    document["measured"] = [
        {
            "position": [length // 2, 0, 0],
            "family": "matter",
            "amount": 1,
            "ramp": 0,
            "start": 0,
            "stocks": {"light": stock},
            "momentum": [0, 0, 0],
            "fixed": False,
            "extents": [1, 1, 1],
            "q": 0,
            "spin": [0, 0, 0],
            "twist": 0,
            "moment": [0, 0, 0],
            "pair": list(POINT_WELL),
            "seed": 1 << 12,
            "margin": "control",
            "emitter": {"family": "light", "twist": 0},  # rewritten by the seeding (item 73)
        }
    ]
    document["detectors"] = []
    massive_generator().seed_on_the_mode(document)
    document["measured"][0]["emitter"]["weight"] = weight
    document["body_record"] = True
    document["stamp"] = input_stamp(document)
    return document


def emitter(
    position: int,
    receiver: str | None,
    momentum: int = 0,
    stock: int = 4,
    direction: list[int] | None = None,
) -> dict:
    """An emitter body over the train's 32 Nodes from `position` on the matter kind [800, 809], seeded on its
    mode, giving light with `stock` along `direction`, and its `receiver` where one is named."""
    block = {
        "position": [position, 0, 0],
        "family": "matter",
        "amount": 1,
        "ramp": 0,
        "start": 0,
        "stocks": {"light": stock},
        "momentum": [momentum, 0, 0],
        "fixed": False,
        "extents": [32, 1, 1],
        "q": 0,
        "spin": [0, 0, 0],
        "twist": 0,
        "moment": [0, 0, 0],
        "pair": [800, 801],
        "seed": 1
        << 10,  # the window's writes at the body's Nodes pile up about 300-fold and stay under the bound (commit 7)
        "emitter": {
            "family": "light",
            "weight": 3,  # the window's weight (commit 7; the train retired)
            "twist": 0,  # the given record's twist "own", the generator's number (item 73)
        },
        "margin": "control",
    }
    if receiver is not None:
        block["receiver"] = receiver
    return block


def parts_of(simulation: DetectorLawSimulation, name: str) -> list:
    family = [family.name for family in simulation.families].index(name)
    return [simulation.held_records[family], *simulation.held_parts[family]]


def parts_world(**body: object) -> dict:
    """A periodic board with one body of matter at [3, 2, 2] of side 3 and the families with parts
    (gravity [1, 3, 6] and charge [1, 3])."""
    block = {"position": [3, 2, 2], "side": 3, "pair": WELL, "margin": "control", **body}
    periodic = {"x": "periodic", "y": "periodic", "z": "periodic"}
    document = block_world(SHAPE, periodic, KIND, [block], ticks=20)
    document["age_bound"] = 100000  # a board periodic on every axis declares it
    for family in document["universe"]:
        if family["name"] == "clicks":
            family.update(
                {
                    "parts": [1, 3, 6],
                    "phase": 1,
                    "held": {
                        "count": "content",
                        "factors": [1, 4, 2],
                        "dipole": "spin",
                        "dipole_div": 1,
                    },
                    "spins_step": {"curl": [1, 4], "tidal": [3, 4]},
                }
            )
            family["spins_step"] = {"curl": [1, 4], "tidal": [3, 4]}
        if family["name"] == "charge":
            family.update(
                {
                    "parts": [1, 3],
                    "held": {"count": "sign", "factors": [1, 1], "dipole": "moment", "dipole_div": 2},
                }
            )
    document["stamp"] = input_stamp(document)
    return document
