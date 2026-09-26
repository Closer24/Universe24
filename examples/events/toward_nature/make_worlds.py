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
c_1 = 2000 by holder bodies of matter on one Node each, content 2000 apiece,
over the whole arm ([132, 690), the hold of 9.45 (2): the level at a body's
Nodes is its content; SINCE THE ONE FAMILY OF MATTER, ALGEBRA.md 9.86 (2) (c),
the holder is no well: a second well of the emitter's family on its chain is
refused by the separation rule of 9.35, the emitter's mode reaching every Node
of the chain, so the holder holds content and nothing else). The level is
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
# THE LONG-WAVE ROWS (ALGEBRA.md 9.62 (1), the mathematician's rule for the rows toward
# nature): the given clock near k = 0.302 (the light clock row's own [2464, 25] on N = 2048,
# 9.24 (6), gives the wavelength 20.8, not whole; the train needs a whole wavelength, 9.17
# (6a): [4096, 21] on N = 2048 gives 21 Links, k = 2 pi / 21 = 0.299), where the lattice's
# term is 0.3 percent; the train's 8 periods of the wavelength 21 over 168 Nodes
LONG_GIVEN_CLOCK = [4096, 21]
LONG_PHASE_STEPS = 2048
LONG_TRAIN_LENGTH = 168
LONG_REDSHIFT_EMITTER_X = 200  # one train (168) beyond the low face slab (32), 9.25 (11) (b)
LONG_REDSHIFT_MIRROR_X = 690  # the arm 322 Links from the train's head at 368
LONG_REDSHIFT_TICKS = 6000
LORENTZ_SHAPE = [1500, 3, 3]
LORENTZ_EMITTER_X = 100
LORENTZ_MIRROR_X = 190  # the light clock's own arm, D = 58
LORENTZ_TICKS = 3600
# THE LONG-WAVE LORENTZ PAIR WITH DOPPLER (ALGEBRA.md 9.62 (1) and (4); BUILD.md section 26
# item 49): the light clock at k = 0.299 at rest and carried along its arm, the moving
# emitter's train at the boosted wave number k gamma (1 + v / c_l) (the wavelength 13 in
# place of 21, the body 104 Nodes in place of 168), the arm LONG_LORENTZ_ARM from the
# train's head to the mirror in both worlds
LONG_LORENTZ_EMITTER_X = 200  # one train (168) beyond the low face slab (32), 9.25 (11) (b)
LONG_LORENTZ_ARM = 90
LONG_LORENTZ_TICKS = 3600
HOP_EVERY = 4  # v = 1 / HOP_EVERY Link per interval
DRIVE_WALL_WIDTH = 1  # the massive worlds' window width (`world.width`), read back at load
LABEL_SCALE = 64  # Q, the drive wall's scale (world.py LABEL_SCALE)


def drive_wall(amount: int) -> int:
    """The block's drive wall 3 Q width amount (world.py, the block's construction)."""
    return 3 * LABEL_SCALE * DRIVE_WALL_WIDTH * amount


def clock_world(
    name: str,
    shape: list[int],
    emitter_x: int,
    mirror_x: int,
    ticks: int,
    holder: list[dict] | None = None,
    hop_every: int | None = None,
    given_clock: list[int] | None = None,
    phase_steps: int | None = None,
    train_length: int | None = None,
    doppler: bool = False,
    arm: int | None = None,
    kind: list[int] | None = None,
    weight: int | None = None,
) -> dict:
    """The light clock's form (`detector.light_clock`) with the arm's ends and the
    ticks as given (at least; the windows read may lengthen the run), Gamma =
    NODE_CLOCK, optional holder bodies and an optional hop of the whole clock
    along +x every `hop_every` intervals; the given clock, its circle N and the
    retired train's length (the emitter's one Node stands at its head) the light
    clock's unless given (the long-wave rows of 9.62 (1) give theirs). SINCE
    COMMIT 7 (ALGEBRA.md 9.85 (5)) the emitter gives by the window at its own
    rotation, a mirror of depth 2 behind it; `doppler` is CANCELLED with the train
    (a moving body's light is its own rotation at its Node, 9.63 (3)); with `arm`
    the mirror stands that many Links beyond the seat (in place of `mirror_x`)."""
    given_clock = list(detector.GIVEN_CLOCK) if given_clock is None else list(given_clock)
    phase_steps = detector.PHASE_STEPS if phase_steps is None else phase_steps
    train_length = detector.TRAIN_LENGTH if train_length is None else train_length
    # CANCELLED (commit 7): the Doppler clock of the retired train (`massive.doppler_clock`);
    # a moving body's light is its own rotation at its Node, written by the window
    # (ALGEBRA.md 9.85 (5) answer 1; 9.63 (3))
    assert not doppler or hop_every is not None, "Doppler is the moving body's"
    if arm is not None:
        mirror_x = emitter_x + train_length + arm
    # THE EMITTER ONE NODE at the retired train's head (its last Node): the arm as before
    seat_x = emitter_x + train_length - 1
    blocks = [detector.emitter([seat_x, 0, 0], [1, 3, 3], kind=kind)]
    document = massive.world(
        name,
        "PIN",
        list(shape),
        massive.CHAIN,
        detector.KIND,
        blocks,
        ticks,
        given_clock=list(given_clock),
        seed_profile=False,
    )
    if holder is not None:
        document["measured"].extend(holder)  # the arm's holders, bodies of matter on one Node each
    document["N"] = phase_steps
    document["face_depth"] = detector.FACE_DEPTH
    detector.bounded(document)
    document["measured"].append(detector.mirror_slab([mirror_x, 0, 0], [detector.MIRROR_DEPTH, 3, 3]))
    # the mirror behind the seat (ALGEBRA.md 9.85 (5) (b); commit 7), moving with the clock
    document["measured"].append(detector.mirror_behind([seat_x, 0, 0], [1, 0, 0], [1, 3, 3]))
    if hop_every is not None:
        for entry in document["measured"]:
            # one Link every hop_every intervals for every block of the clock:
            # the momentum one hop_every-th of the block's own drive wall
            # the wall on the body's whole content, its own quanta and the stock it
            # holds (ALGEBRA.md 9.51 (8); BUILD.md section 26 item 47)
            content = int(entry["amount"]) + sum(
                int(value) for value in entry.get("stocks", {}).values()
            )
            wall = drive_wall(content)
            assert wall % hop_every == 0, (content, wall, hop_every)
            entry["momentum"] = [wall // hop_every, 0, 0]
            entry.pop("fixed", None)  # the moving clock's bodies are free (record 2157)
    detector.receiver_set(document, "at_well", 0)
    detector.named_receiver(document, {0: "at_well"})
    massive.seed_on_the_mode(document)
    # the window's weight and the run's length (commit 7): every giving's window and rung,
    # then two arms' flights and a margin
    return detector.finish_windows(
        massive,
        document,
        [0],
        3 * 2 * (mirror_x - seat_x) + 300,
        weights=None if weight is None else {0: weight},
    )


def weight_of(document: dict) -> int:
    """The emitter's weight read by the trial on the first world of a pair (the same instrument
    in both worlds of the pair)."""
    return int(document["measured"][0]["emitter"]["weight"])


def holder_nodes(position: list[int], extents: list[int], amount: int) -> list[dict]:
    """The arm's holders: a body of matter on each Node of the box, content `amount` apiece,
    the level the hold writes at its Node (ALGEBRA.md 9.45 (2)); no well, no record, no
    emitter. UNDER ONE FAMILY OF MATTER (ALGEBRA.md 9.86 (2) (c); the one stroke, commit 1)
    the holder well of a fifth family (item 41, HISTORY) is refused: a second well of the
    emitter's family on its chain fails the separation rule of 9.35 (the emitter's mode is
    nonzero on every Node of the chain), so the arm is held by content alone. Every key the
    engine reads on a measured event is written (record 2089)."""
    return [
        {
            "position": [position[0] + dx, position[1] + dy, position[2] + dz],
            "family": "matter",
            "amount": amount,
            "momentum": [0, 0, 0],
            "stocks": {},
            "fixed": True,  # a tool held in place (ALGEBRA.md 9.104 (6) (b); record 2157)
        }
        for dx in range(extents[0])
        for dy in range(extents[1])
        for dz in range(extents[2])
    ]


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
    """The nine worlds; each pair (the resting clock and the moving one, the well's top and
    its bottom) carries one emitter weight, read by the trial on the first of the pair."""
    arm_start = REDSHIFT_EMITTER_X + detector.TRAIN_LENGTH
    arm = [REDSHIFT_MIRROR_X - arm_start, 3, 3]
    out: dict[str, dict] = {}
    out["redshift_top"] = clock_world(
        "redshift-top", REDSHIFT_SHAPE, REDSHIFT_EMITTER_X, REDSHIFT_MIRROR_X, REDSHIFT_TICKS
    )
    out["redshift_bottom"] = clock_world(
        "redshift-bottom",
        REDSHIFT_SHAPE,
        REDSHIFT_EMITTER_X,
        REDSHIFT_MIRROR_X,
        REDSHIFT_TICKS,
        holder=holder_nodes([arm_start, 0, 0], arm, WELL_LEVEL),
        weight=weight_of(out["redshift_top"]),
    )
    out["lorentz_rest"] = clock_world(
        "lorentz-rest", LORENTZ_SHAPE, LORENTZ_EMITTER_X, LORENTZ_MIRROR_X, LORENTZ_TICKS
    )
    out["lorentz_moving"] = clock_world(
        "lorentz-moving",
        LORENTZ_SHAPE,
        LORENTZ_EMITTER_X,
        LORENTZ_MIRROR_X,
        LORENTZ_TICKS,
        hop_every=HOP_EVERY,
        weight=weight_of(out["lorentz_rest"]),
    )
    out["bending"] = bending()
    long_rows = dict(
        given_clock=LONG_GIVEN_CLOCK,
        phase_steps=LONG_PHASE_STEPS,
        train_length=LONG_TRAIN_LENGTH,
        kind=detector.SEAT_KIND,  # the long rows' seat: omega = 0.178, the wavelength about 20
    )
    out["lorentz_rest_long"] = clock_world(
        "lorentz-rest-long",
        LORENTZ_SHAPE,
        LONG_LORENTZ_EMITTER_X,
        0,
        LONG_LORENTZ_TICKS,
        arm=LONG_LORENTZ_ARM,
        **long_rows,
    )
    out["lorentz_moving_long"] = clock_world(
        "lorentz-moving-long",
        LORENTZ_SHAPE,
        LONG_LORENTZ_EMITTER_X,
        0,
        LONG_LORENTZ_TICKS,
        hop_every=HOP_EVERY,
        doppler=True,
        arm=LONG_LORENTZ_ARM,
        weight=weight_of(out["lorentz_rest_long"]),
        **long_rows,
    )
    out["redshift_top_long"] = clock_world(
        "redshift-top-long",
        REDSHIFT_SHAPE,
        LONG_REDSHIFT_EMITTER_X,
        LONG_REDSHIFT_MIRROR_X,
        LONG_REDSHIFT_TICKS,
        **long_rows,
    )
    out["redshift_bottom_long"] = clock_world(
        "redshift-bottom-long",
        REDSHIFT_SHAPE,
        LONG_REDSHIFT_EMITTER_X,
        LONG_REDSHIFT_MIRROR_X,
        LONG_REDSHIFT_TICKS,
        holder=holder_nodes(
            [LONG_REDSHIFT_EMITTER_X + LONG_TRAIN_LENGTH, 0, 0],
            [LONG_REDSHIFT_MIRROR_X - LONG_REDSHIFT_EMITTER_X - LONG_TRAIN_LENGTH, 3, 3],
            WELL_LEVEL,
        ),
        weight=weight_of(out["redshift_top_long"]),
        **long_rows,
    )
    return out


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(
            json.dumps(massive.bind_universe_file(document), indent=1) + "\n", encoding="utf-8"
        )
        print(path.name, flush=True)


if __name__ == "__main__":
    main()
