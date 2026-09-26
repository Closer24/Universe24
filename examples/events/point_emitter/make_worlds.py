"""THE POINT EMITTER'S FIRST ROW (ALGEBRA.md 9.69 (2), 9.71 (1); the model owner's word of
2026-09-25 through the Boss, record 2054: "try to reduce them all to a Node"; BUILD.md section
26 item 50), a hypothesis under its own identity, the world key `point_emitter`:

- `point_chain.json`: a chain of 1200 (x open, the face slabs 32 deep) with a point emitter of
  one Node at its middle, a well [800, 802] of the kind [800, 813] whose bound mode rotates
  at omega = 0.178 (light's wave number at that frequency k = 0.31, the wavelength about 20;
  9.62 (1)), its stock 64 of light, its weight g chosen by the generator so that the window
  is about 32 periods of its rotation; two receiver sets of three light bodies 500 Links
  from the seat on each side (`left`, `right`). The blind expectations of 9.71 (1): (i) the
  counts at the two sides alike, 32 +- 4 each; (ii) the first click at each side at 500 /
  c_l after the open plus the window's share; (iii) the train's wavelength on the chain
  (GAMEBOARD, `read_runs.py --wavelength`).
- `point_light_clock.json`: the light clock with a point emitter: the same seat at 100 on a
  chain of 400, a mirror four Nodes deep 60 Links beyond it, the detector the seat's own set
  `at_well`; ROW (iv) AS FIXED (ALGEBRA.md 9.85 (5); commit 7): the weight g = 4 (the window
  shorter than the arm's round trip), a gap slab of depth 2 one Link behind the seat, the
  reading the rung's share on the return, 2 x 60 / c_l + n / 2 +- n / sqrt(12) from the open,
  n the window's length.

SINCE COMMIT 7 the window is the law's one giving (no world key `point_emitter`; every
emitter of every world gives so); `body_record` stays the seat's form here.

Run from the repository root:

    PYTHONPATH=src python examples/events/point_emitter/make_worlds.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

from event_universe.world_files import input_stamp

HERE = Path(__file__).resolve().parent
EVENTS = HERE.parent


def load(path: Path, name: str):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


massive = load(EVENTS / "massive_record" / "make_worlds.py", "massive_record_make_worlds")
detector = load(EVENTS / "detector_law" / "make_worlds.py", "detector_law_make_worlds")

KIND = [800, 813]  # the matter kind: the band's bottom omega_0 = 0.179
WELL = [800, 802]  # the one-Node well: the bound mode at omega = 0.178, its pair rich (1203 values)
SEED = 1 << 12  # the seat's amplitude; the written light stays far below the bound at the weights read
STOCK = 64
PERIODS = 32  # the window's length aimed at, in periods of the seat's rotation (9.71 (1))
CHAIN_LENGTH = 1200
CHAIN_SEAT_X = 600
SET_DISTANCE = 500  # the receiver sets' distance from the seat
CLOCK_LENGTH = 400
CLOCK_SEAT_X = 100
CLOCK_ARM = 60  # the mirror 60 Links beyond the seat (9.71 (1) (iv))
FLIGHTS = 2  # the run's length: the stock's windows and rungs plus two flights
CLOCK_WEIGHT = 4  # the light clock's weight g (ALGEBRA.md 9.85 (5) (a)): its window shorter than the arm's round trip


def seat(position: list[int]) -> dict:
    return {
        "position": position,
        "family": massive.MATTER_FAMILY_NAME,
        "kind": list(KIND),  # the body's rest pair (ALGEBRA.md 9.91 (7); commit 1)
        "q": 0,  # the body's numbers (ALGEBRA.md 9.91 (3), (7); commit 2; the word `q`, record 2128)
        "spin": [0, 0, 0],
        "moment": list(massive.LIGHT_MOMENT),  # the given light's component (9.82 (3) (d))
        "amount": 1,
        "stocks": {massive.WAVE_FAMILY_NAME: STOCK},  # the stock of light, the charge family's quanta
        "momentum": [0, 0, 0],
        "fixed": True,  # a tool held in place (ALGEBRA.md 9.104 (6) (b); record 2157)
        "ramp": 0,
        "start": 0,
        "extents": [1, 1, 1],
        "pair": list(WELL),
        "seed": SEED,
        "margin": "control",
        "emitter": {"family": massive.WAVE_FAMILY_NAME, "clock": list(massive.MASSIVE_GIVEN_CLOCK)},
    }


def body(x: int) -> dict:
    return {
        "position": [x, 0, 0],
        "family": massive.WAVE_FAMILY_NAME,  # a receiver of light's kind (9.86 (2) (b))
        "amount": 1,
        "momentum": [0, 0, 0],
        "stocks": {},
        "fixed": True,  # a tool held in place (ALGEBRA.md 9.104 (6) (b); record 2157)
    }


def finish(  # type: ignore[no-untyped-def]
    document: dict, ticks_of_window, receiver: bool = False, weight: int | None = None
) -> dict:
    """The point emitter's keys after the seeding (the mode first, as `body_record`): the
    world key `body_record` (the seat's form), the seat's own set where the row reads at the
    seat (one Node), the weight by the generator's trial or the row's own `weight` (9.85 (5)
    (a): g = 4 for the light clock), the ticks from the window read, the stamp over the whole
    file. The world key `point_emitter` is retired (commit 7): the window is the law's one
    giving."""
    massive.seed_on_the_mode(document)
    document["body_record"] = True
    if receiver:
        detector.receiver_set(document, "at_well", 0)
        detector.named_receiver(document, {0: "at_well"})
    document["stamp"] = input_stamp(document)
    if weight is None:
        massive.point_weight(document, 0, PERIODS)
    else:
        emitter = document["measured"][0]["emitter"]
        limit = 12 * PERIODS * int(emitter["period"])
        read = massive.point_window(document, 0, weight, limit)
        assert read is not None, (weight, limit)
        emitter["weight"] = weight
        emitter["window_read"] = read  # HOST: the trial's window at the row's weight
    window = int(document["measured"][0]["emitter"]["window_read"])
    document["ticks"] = ticks_of_window(window)
    document["stamp"] = input_stamp(document)
    return document


def point_chain() -> dict:
    document = massive.world(
        "point-emitter-chain",
        "PIN",
        [CHAIN_LENGTH, 1, 1],
        massive.CHAIN,
        KIND,
        [],
        1000,
        seed_profile=False,
    )
    document["measured"] = [seat([CHAIN_SEAT_X, 0, 0])]
    for x in (CHAIN_SEAT_X - SET_DISTANCE, CHAIN_SEAT_X + SET_DISTANCE):
        for offset in (-1, 0, 1):
            document["measured"].append(body(x + offset))
    document["detectors"] = [
        {"name": "left", "positions": [[CHAIN_SEAT_X - SET_DISTANCE + o, 0, 0] for o in (-1, 0, 1)]},
        {"name": "right", "positions": [[CHAIN_SEAT_X + SET_DISTANCE + o, 0, 0] for o in (-1, 0, 1)]},
    ]
    document["face_depth"] = detector.FACE_DEPTH
    detector.bounded(document)
    period = 35
    return finish(document, lambda window: STOCK * (window + 2 * period) + FLIGHTS * (SET_DISTANCE * 2))


def point_light_clock() -> dict:
    document = massive.world(
        "point-emitter-light-clock",
        "PIN",
        [CLOCK_LENGTH, 1, 1],
        massive.CHAIN,
        KIND,
        [],
        1000,
        seed_profile=False,
    )
    document["measured"] = [seat([CLOCK_SEAT_X, 0, 0])]
    document["face_depth"] = detector.FACE_DEPTH
    detector.bounded(document)
    document["measured"].append(
        detector.mirror_slab([CLOCK_SEAT_X + CLOCK_ARM, 0, 0], [detector.MIRROR_DEPTH, 1, 1])
    )
    # ROW (iv)'S FIX (ALGEBRA.md 9.85 (5); commit 7): the mirror behind the seat, and the
    # weight g = 4 so that the window is shorter than the arm's round trip
    document["measured"].append(detector.mirror_behind([CLOCK_SEAT_X, 0, 0], [1, 0, 0], [1, 1, 1]))
    period = 35
    return finish(
        document,
        lambda window: STOCK * (window + 2 * period + 2 * CLOCK_ARM * 2) + 1000,
        receiver=True,
        weight=CLOCK_WEIGHT,
    )


def worlds() -> dict[str, dict]:
    return {"point_chain": point_chain(), "point_light_clock": point_light_clock()}


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(
            json.dumps(massive.bind_universe_file(document), indent=1) + "\n", encoding="utf-8"
        )
        e = document["measured"][0]["emitter"]
        print(path.name, "weight", e["weight"], "window", e["window_read"], "ticks", document["ticks"])


if __name__ == "__main__":
    main()
