"""THE EIGHTH HARD QUESTION (record 2140; ALGEBRA.md 9.103 (4)), THE RUN: a rate row, an
emitter feeding a well, the clicks' rate at the well against the well's count of bound
states. Written before the algebra's number is read (record 2137); nothing here reads it.

The worlds, in the loader's words of today (the check-mode generator's `body` and `build`):
the beam board [512, 21, 21], x open with one-Node face slabs, y and z periodic; an emitter
body of the matter family (its well [800, 801] on [32, 5, 5], the kind [800, 850]) holding
100 quanta of a second massive family `target` (the same kind [800, 850], no reads) and
giving them as trains along +x (the given clock [512, 1] on N = 1024: the wavelength 4
Links, 8 periods, K = pi / 2, the shipped beam train); at x = 380 the
receiver named by the emitter, one of two per side s in {5, 9, 13}:

- `well`: a body of the target family on the well [800, 801] of side s, seeded on its bound
  mode, bound to the set by `block` (the flux into its cube clicks);
- `cube`: the same cube of free Nodes, no well (record 1899's detector), the control.

The reading (DETECTOR): the count of clicks at the receiver per 100 givings and the mean
wait from the giving; the difference well less cube is what the well's levels add to the
click. A level's frequency lies below the kind's band (a bound level is in the gap), so no
train carries it: the row is the rate the click reads, not a feeding at a level's energy.

    PYTHONPATH=src python docs/designs/rule_alone/item8_rate_worlds.py
"""

from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


check_mode = load(ROOT / "examples" / "events" / "check_mode" / "make_worlds.py", "item8_check_mode")
massive = check_mode.massive

SHAPE = [512, 21, 21]
BOUNDARY = {"x": "open", "y": "periodic", "z": "periodic"}
EMITTER_CORNER = [34, 8, 8]  # one train's length from the -x face slab (9.25 (11) (b))
EMITTER_EXTENTS = [32, 5, 5]  # 8 periods of the wavelength 4, the cross-section [8, 13)
EMITTER_QUANTA = 64
STOCK = 100
# on N = 1024: the wavelength 2 N / 512 = 4 Links, K = pi / 2, the shipped beam train. The slower
# trains were tried first (HOST, before any run): K = pi / 8 is a body of 128 Nodes whose mode
# the generator's iteration did not reach in 20 minutes; K = pi / 4 at 8 periods books 0.9802 of
# its norm through the plane 40 Links ahead and the generator refuses it (a passage within
# 2 x 10^-3, ALGEBRA.md 9.25 (11)).
GIVEN_CLOCK = [512, 1]
PERIODS = 8
TARGET_FAMILY = "target"
RECEIVER_X = 380  # the receiver's centre along x
SIDES = (5, 9, 13)
TICKS = 12_000  # 100 givings at about 100 intervals each, the flight of 310 Links at v_g = 0.40 and the passage (COMPUTATION)
WELL_QUANTA = 64
# every body seeded once (HOST): the same body in every world carries the same seed
SEEDED: dict[str, dict] = {}


def target_family() -> dict:
    """The given family: a massive kind with the emitter's clock, reading nothing (its rows
    bent by no field), giving and taking clicks."""
    return {
        "name": TARGET_FAMILY,
        "charge": 0,
        "pair": list(check_mode.KIND),
        "parts": [1],
        "levels": 2,
        "self_unit": 0,
        "reads": [],
        "clicks": {"gives": True, "takes": True},
        "quantum": 1,
    }


def corner(centre: list[int], side: int) -> list[int]:
    return [c - side // 2 for c in centre]


def cube_nodes(centre: list[int], side: int) -> list[list[int]]:
    c = corner(centre, side)
    return [
        [c[0] + i, c[1] + j, c[2] + k] for i in range(side) for j in range(side) for k in range(side)
    ]


def emitter(receiver: str) -> dict:
    block = check_mode.body(EMITTER_CORNER, EMITTER_EXTENTS, EMITTER_QUANTA)
    block["held"] = {TARGET_FAMILY: STOCK}
    block["emitter"] = {
        "family": TARGET_FAMILY,
        "clock": list(GIVEN_CLOCK),
        "train": {"direction": [1, 0, 0], "periods": PERIODS},
        "receiver": [receiver],
    }
    return block


def build_with_target(side: int, well: bool) -> dict:
    """`check_mode.build` with the target family appended to the families list before any
    body is seeded (the seeding reads the family's pair)."""
    centre = [RECEIVER_X, SHAPE[1] // 2, SHAPE[2] // 2]
    blocks = [emitter("well" if well else "cube")]
    if well:
        target = check_mode.body(corner(centre, side), [side] * 3, WELL_QUANTA, family=TARGET_FAMILY)
        del target["kind"]
        blocks.append(target)
    name = f"item8-rate-{'well' if well else 'cube'}-s{side}"
    document = massive.world(
        name,
        "CHECK",
        SHAPE,
        BOUNDARY,
        check_mode.KIND,
        blocks,
        TICKS,
        given_clock=GIVEN_CLOCK,
        seed_profile=False,
    )
    document["N"] = check_mode.TRAIN_PHASE_STEPS
    document["face_depth"] = check_mode.FACE_DEPTH
    document["families"].append(target_family())
    for number, entry in enumerate(document["measured"]):
        key = json.dumps([entry["family"], entry["position"], entry["extents"], entry["pair"]])
        if key not in SEEDED:
            alone = copy.deepcopy(document)
            alone["measured"] = [copy.deepcopy(entry)]
            # the receiver's set is declared on the whole world alone: the name is taken off
            # the copy for the seeding and written back after it
            alone["measured"][0].get("emitter", {}).pop("receiver", None)
            massive.seed_on_the_mode(alone)
            SEEDED[key] = alone["measured"][0]
        seeded = copy.deepcopy(SEEDED[key])
        if "receiver" in entry.get("emitter", {}):
            seeded["emitter"]["receiver"] = entry["emitter"]["receiver"]
        document["measured"][number] = seeded
    if well:
        document["detectors"] = [{"name": "well", "block": 1}]
    else:
        # the control: a detector's Nodes are measured events (the detector law's form, record
        # 1899), one receiver body of the target family at every Node of the cube, no well
        nodes = cube_nodes(centre, side)
        document["measured"].extend(receiver_body(node) for node in nodes)
        document["detectors"] = [{"name": "cube", "positions": nodes}]
    return massive.stamped(document)


def receiver_body(position: list[int]) -> dict:
    """A receiver body of the target family at one Node: a measured event with no block (the
    block's keys, the drive's ramp and start, the charge, the spin and the moment, are refused
    on it)."""
    return {
        "position": list(position),
        "family": TARGET_FAMILY,
        "amount": 1,
        "momentum": [0, 0, 0],
        "held": {},
    }


def main() -> None:
    out = HERE / "worlds"
    out.mkdir(exist_ok=True)
    from event_universe.events.world import parse_nature_beam_world

    for side in SIDES:
        for well in (True, False):
            document = build_with_target(side, well)
            path = (
                out
                / f"{document['model_id'].removeprefix('beam-massive-record-').removesuffix('-v1')}.json"
            )
            path.write_text(check_mode.dumps(document), encoding="utf-8")
            try:
                parse_nature_beam_world(json.loads(path.read_text(encoding="utf-8")))
                print(f"LAWFUL {path.name}")
            except ValueError as error:
                print(f"REFUSED {path.name}: {error}")


if __name__ == "__main__":
    main()
