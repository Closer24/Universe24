"""THE RUNS TOWARD NATURE, WITHOUT PINS (ALGEBRA.md 9.59 (0) to (3); the model
owner's question of 2026-09-25 through the Boss, record 2030: "when will
experiments start, to see that there is a direction toward nature, without
pins?"): the world files of rows (1) the redshift and (2) Lorentz, each written
from the light clock's own form (`../detector_law/make_worlds.py::light_clock`,
the one table of ALGEBRA.md 9.30) under the integers of 9.57 (2), Gamma = 10^4.
Row (3), the bending on today's law, is the dark body's world (`../dark_body/`)
under row (3)'s numbers (`bending.json`: Gamma 10^4, the beam 20 wide, the body's
content set so that U_b = 0.1 on the beam's line under it, 100 records), and the
dark body's two worlds run as they stand.

These are diagnostic rows: no `expectations.json` is written beside them, no
pin, no verdict (9.59 (6)). Every reading is a detector's click (the interval
from a record's giving click to its click at the clock's own set `at_well`,
DETECTOR), read beside nature's value only for the direction; a reading outside
the mathematician's band goes to him before any word.

(1) THE REDSHIFT. Two light clocks on the chain [760, 3, 3], the arm 558 Links
(A at [100, 132), the mirror at [690, 694)): `redshift_top.json` at the level 0
and `redshift_bottom.json` with the arm's free Nodes held at the uniform level
c_1 = 2000 by a holder body of content 2000 over the whole arm ([132, 690), the
hold of 9.45 (2): the level at a body's Nodes is its content). The level is
held only on the arm's free Nodes; the emitter's own Nodes read its stock and
the mirror's its content in both worlds alike, so the ratio of the two mean
click intervals reads the flight in the well over the flight at 0: today's
law sqrt((1 - c_2 / Gamma) / (1 - c_1 / Gamma)) = 1.118 at U_1 = 0.1 on the
arm's part of the tick (9.59 (1); the part outside the arm, the train's own
32 Nodes and the mirror's delay, is the same in both and dilutes the ratio by
that share, COMPUTATION in the reader).

(2) LORENTZ. The light clock at rest and the same clock carried along its arm
(the longitudinal clock of 9.24 (6): the emitter, its mirror and its set hop
together, one Link every 4 intervals, v = 1 / 4 Link per interval, by the
declared momentum of each block at one quarter of its own drive wall 3 Q width
amount, so that both accumulators carry at the same intervals), on the chain
[1500, 3, 3] with the clock at [100, 194) and 3600 intervals (the clock reaches
x = 1000 at the end, the far face slab at 1468). The board's light at the given
clock's wave number runs at c_l = 0.577 Links per interval (9.24 (6)), so
v / c_l = 0.433; the longitudinal form gives the tick gamma^2 (2 D / c_l) +
the delay with gamma = 1 / sqrt(1 - v^2 / c_l^2) = 1.108, gamma^2 = 1.23
(9.24 (6): the board's material does not contract, a PREDICTION against
nature's gamma); the transverse form gamma needs a layer and is not run here.

Regenerate from the repository root:

    PYTHONPATH=src python examples/events/toward_nature/make_worlds.py

The dry check of every file, no run and no reading:

    PYTHONPATH=src python -m event_universe.configuration_validation examples/events/toward_nature/<world>.json
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.events.world import input_stamp

HERE = Path(__file__).resolve().parent
EVENTS = HERE.parent


def load(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


massive = load(EVENTS / "massive_record" / "make_worlds.py", "massive_record_make_worlds")
detector = load(EVENTS / "detector_law" / "make_worlds.py", "detector_law_make_worlds")

NODE_CLOCK = 10_000  # Gamma, the integers of ALGEBRA.md 9.57 (2) and 9.59 (0)
WELL_LEVEL = 2000  # c_1, the well's bottom: U_1 = c_1 / (2 Gamma) = 0.1 (9.59 (1))
REDSHIFT_SHAPE = [760, 3, 3]
REDSHIFT_EMITTER_X = 100
REDSHIFT_MIRROR_X = 690
REDSHIFT_TICKS = 6000  # 64 givings by about 3000, the last return about 2200 later at the well's level
LORENTZ_SHAPE = [1500, 3, 3]
LORENTZ_EMITTER_X = 100
LORENTZ_MIRROR_X = 190  # the light clock's own arm, D = 58
LORENTZ_TICKS = 3600
HOP_EVERY = 4  # v = 1 / HOP_EVERY Link per interval
DRIVE_WALL_WIDTH = 1  # the massive worlds' window width (`world.width`), read back at load
LABEL_SCALE = 64  # Q, the drive wall's scale (world.py LABEL_SCALE)
HOLDER_FAMILY = {
    "name": "well",
    "quantum": 1,
    "pair": list(detector.KIND),
    "charge": 0,
}  # the fifth family


def drive_wall(amount: int) -> int:
    """The block's drive wall 3 Q width amount (world.py, the block's construction)."""
    return 3 * LABEL_SCALE * DRIVE_WALL_WIDTH * amount


def clock_world(
    name: str,
    shape: list[int],
    emitter_x: int,
    mirror_x: int,
    ticks: int,
    holder: dict | None = None,
    hop_every: int | None = None,
) -> dict:
    """The light clock's form (`detector.light_clock`) with the arm's ends and the
    ticks as given, Gamma = NODE_CLOCK, an optional holder block and an optional
    hop of the whole clock along +x every `hop_every` intervals."""
    blocks = [
        detector.emitter([emitter_x, 0, 0], [detector.TRAIN_LENGTH, 3, 3], detector.WELL_FULL, [1, 0, 0])
    ]
    if holder is not None:
        blocks.append(holder)
    document = massive.world(
        name,
        "PIN",
        list(shape),
        massive.CHAIN,
        detector.KIND,
        blocks,
        ticks,
        light=detector.light_family(detector.GIVEN_CLOCK),
        seed_profile=False,
    )
    if holder is not None:
        document["families"].append(dict(HOLDER_FAMILY))
    document["N"] = detector.PHASE_STEPS
    document["face_depth"] = detector.FACE_DEPTH
    detector.bounded(document)
    document["node_clock"] = NODE_CLOCK
    document["measured"].append(detector.mirror_slab([mirror_x, 0, 0], [detector.MIRROR_DEPTH, 3, 3]))
    if hop_every is not None:
        for entry in document["measured"]:
            # one Link every hop_every intervals for every block of the clock:
            # the momentum one hop_every-th of the block's own drive wall
            wall = drive_wall(int(entry["amount"]))
            assert wall % hop_every == 0, (entry["amount"], wall, hop_every)
            entry["momentum"] = [wall // hop_every, 0, 0]
    detector.receiver_set(document, "at_well", 0)
    detector.named_receiver(document, {0: "at_well"})
    massive.seed_on_the_mode(document)
    return document


def holder_block(position: list[int], extents: list[int], amount: int) -> dict:
    """A holder of its own family (the kind of the matter family, so that its mode and
    the emitter's need not be apart: the separation rule is per family) over a box,
    fixed, its content `amount` the level the hold writes at its Nodes (ALGEBRA.md
    9.45 (2)); no emitter, as the dark body's (`../dark_body/make_worlds.py`)."""
    return {
        "position": position,
        "family": HOLDER_FAMILY["name"],
        "extents": extents,
        "pair": detector.WELL_FULL,
        "amount": amount,
        "seed": detector.EMITTER_SEED,
        "margin": "control",
    }


BENDING_NODE_CLOCK = NODE_CLOCK
BENDING_BODY_CONTENT = 4812  # M so that the static level on the beam's line under the body is c_b = 2000 (U_b = 0.1): the dark body's 10^5 gave 41561 there, the field linear in M
BENDING_EMITTER_CORNER = [5, 90, 0]  # the beam 20 wide across, centred on the line
BENDING_EMITTER_EXTENTS = [32, 20, 1]
BENDING_STOCK = 100  # the given records: the centroid's standard error near 1 Link
BENDING_TICKS = 5600  # the last giving near 100 x P / 2, the flight 375 Links at 0.447


def bending_generator():
    """The dark body's generator (`../dark_body/make_worlds.py`) with row (3)'s numbers set on
    it (9.59 (3): the beam 20 wide, U_b = 0.1 at the beam's closest distance, the records for
    the centroid), its layout, its screen and its static field and ray otherwise as built;
    loaded under its own name so the dark body's module stays as it is."""
    module = load(EVENTS / "dark_body" / "make_worlds.py", "dark_body_make_worlds_for_bending")
    module.NODE_CLOCK = BENDING_NODE_CLOCK
    module.BODY_CONTENT = BENDING_BODY_CONTENT
    module.EMITTER_CORNER = list(BENDING_EMITTER_CORNER)
    module.EMITTER_EXTENTS = list(BENDING_EMITTER_EXTENTS)
    module.STOCK = BENDING_STOCK
    module.TICKS = BENDING_TICKS
    return module


def bending() -> dict:
    """Row (3)'s world: the dark body's dark world under row (3)'s numbers, the body dark (no
    light of its own), the reading the emitter's records' centroid over the screen."""
    generator = bending_generator()
    document = generator.world(True)
    document["model_id"] = "beam-toward-nature-bending-v1"
    document["input"] = input_stamp(document)  # the stamp renewed over the identity
    return document


def worlds() -> dict[str, dict]:
    arm_start = REDSHIFT_EMITTER_X + detector.TRAIN_LENGTH
    arm = [REDSHIFT_MIRROR_X - arm_start, 3, 3]
    return {
        "redshift_top": clock_world(
            "redshift-top", REDSHIFT_SHAPE, REDSHIFT_EMITTER_X, REDSHIFT_MIRROR_X, REDSHIFT_TICKS
        ),
        "redshift_bottom": clock_world(
            "redshift-bottom",
            REDSHIFT_SHAPE,
            REDSHIFT_EMITTER_X,
            REDSHIFT_MIRROR_X,
            REDSHIFT_TICKS,
            holder=holder_block([arm_start, 0, 0], arm, WELL_LEVEL),
        ),
        "lorentz_rest": clock_world(
            "lorentz-rest", LORENTZ_SHAPE, LORENTZ_EMITTER_X, LORENTZ_MIRROR_X, LORENTZ_TICKS
        ),
        "lorentz_moving": clock_world(
            "lorentz-moving",
            LORENTZ_SHAPE,
            LORENTZ_EMITTER_X,
            LORENTZ_MIRROR_X,
            LORENTZ_TICKS,
            hop_every=HOP_EVERY,
        ),
        "bending": bending(),
    }


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path.name, flush=True)


if __name__ == "__main__":
    main()
