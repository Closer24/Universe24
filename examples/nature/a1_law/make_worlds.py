"""Write the worlds of A1 repeated under the law of the bit (docs/EXPERIMENTS.md,
2026-09-18): one lamp of the light family behind a wall with two slits, a
screen of marks behind the wall, the lamp's shadow set given with the board,
on a closed board.

The law's form throughout: N = 64 (the world's one phase circle, declared once
like K; the cleanup of 2026-09-18), one K for the world, `wait_per_quantum` 1,
no field family (the lamp's field is light shadows, bit 0, of the lamp's
owner), no spread, steering, mass field or seed, the dense mode where the world
admits it.

The board: X x Y x Z = 45 x 49 x 9, periodic (the model owner's decisions of
2026-09-18, Highlights 5.4: the board of a run is closed, so that the source's
shadow set does not escape, and only closed worlds are tested, so the series
carries no open-board control). The lamp, a type holding light (stock 2^26)
and the world's momentum, at (4, 24, 4), emitting one light thing of amount 4
along +X every interval (`kerengonen_phase` 0); light declares `clock` true
and the world K = 1, so a thing of amount 4 advances 4 steps of 64 per
interval, a sixteenth of a turn: the derivation's period 16, lambda_w =
K N / (sqrt(3) M) = 64 / (sqrt(3) x 4) = 9.24 Links (DERIVATIONS.md sections 27
(v) and 29, where K is the content per turn, N times the engine's K per step).
The wall: the plane x = 16, every Node of it a Detector mark at setting [1, 1]
except the two slit columns at y = 16 and y = 32 (d = 16), all z; a mark
absorbs a thing into its counter and returns a shadow, which is what a wall
does under the law, and it is silent in the record and reflects in the prefill
as it does in the run, where an external body's Node publishes a record every
interval a shadow reaches it and is dropped by the prefill. A second wall of
marks over the plane x = 44 closes the wrap in x: without it the shell leaving
the lamp toward -X would reach the screen from behind; the wrap in z makes the
slit columns infinite, the wrap in y puts images of the lamp 49 Links apart.
The screen: the row x = 40 (L = 24 behind the wall), every y, z = 4, marks at
[1, 1]. The optical spacing lambda_w L / d = 13.9 Links.

The lamp's shadow set: `initial_field` `{"light": {"fill": 8}}` with
`release` [1, 1], 2^26 quanta per heading per interval of the fill; 8 is the
longest fill the engine admits for one lamp, read before the runs (commit
ffa4a56: from 16 the prefill refuses "a third phase on one Port of a source",
`prefill.py`, `_depart`), so the set is a shell of eight intervals of release
that leaves the lamp at the first tick, holding about 3.2 x 10^9 quanta, and
not a standing set. The prefill releases at phase 0 (`release_stock`: a record
has no phase of its own) and a shadow that comes home is re-released with its
own phase (`rerelease_shadow`), so the lamp's clock enters none of its shadows.

Two worlds: `two_slits_periodic` and, the control, `one_slit_periodic` (the
column y = 16 closed with marks). 200 ticks: the shell's front reaches the
screen after about sqrt(3) x 31 = 54 intervals and its reflection off the
screen is back at the wall and at the screen again within the run. The open
board (45 x 65 x 17, the lamp at (4, 32, 8), the slits at y = 24 and 40, the
lamp's stock 2^22 and 2^26) was measured earlier the same day and is recorded
in the register entry; under the decision it is not in the series, and
`world(..., periodic=False)` keeps its form only so that the record's reader
can name it.

Run:  python examples/nature/a1_law/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
HEADINGS = [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
OPERATIONS = ("receive", "read", "evaluate", "update", "couple", "route", "split", "send", "commit")
SHAPE = [45, 65, 17]
N = 64
K = 1
TICKS = 200
LAMP = (4, 32, 8)
LAMP_STOCK = 1 << 22
BIG_STOCK = 1 << 26
PHOTON = 4
WALL_X = 16
SCREEN_X = 40
SLITS = (24, 40)
PLANE_Z = 8
FILL = 8
RELEASE = [1, 1]
SETTING = [1, 1]


def scalar(name):
    return {
        "name": name,
        "components": 1,
        "units": "quantum",
        "signed": False,
        "conserved": True,
        "extensive": True,
    }


# The periodic pair (the model owner's decision of 2026-09-18, landing while
# the open-board pairs ran: the confrontation runs are made on a closed board,
# so that the source's shadow set does not escape): the same lamp, wall, slits
# and screen on a periodic board 45 x 49 x 9, the lamp at (4, 24, 4), the slits
# at y = 16 and 32 (d = 16), the screen row at x = 40 over every y, and a
# second wall of marks at x = 44 closing the wrap in x (without it the shell
# leaving the lamp toward -X would reach the screen from behind through the
# wrap); the wrap in z makes the slit columns infinite, the wrap in y puts
# images of the lamp 49 Links apart.
PERIODIC_SHAPE = [45, 49, 9]
PERIODIC_LAMP = (4, 24, 4)
PERIODIC_SLITS = (16, 32)
PERIODIC_PLANE_Z = 4
BACK_WALL_X = 44


def wall_marks(open_slits, shape=SHAPE, wall_x=WALL_X):
    marks = []
    for y in range(shape[1]):
        if y in open_slits:
            continue
        for z in range(shape[2]):
            marks.append({"position": [wall_x, y, z], "setting": list(SETTING)})
    return marks


def screen_marks(shape=SHAPE, plane_z=PLANE_Z, margin=1):
    return [
        {"position": [SCREEN_X, y, plane_z], "setting": list(SETTING)}
        for y in range(margin, shape[1] - margin)
    ]


def world(open_slits, name, stock=LAMP_STOCK, periodic=False):
    shape = PERIODIC_SHAPE if periodic else SHAPE
    lamp = PERIODIC_LAMP if periodic else LAMP
    marks = wall_marks(open_slits, shape)
    if periodic:
        marks += wall_marks((), shape, BACK_WALL_X)
        marks += screen_marks(shape, PERIODIC_PLANE_Z, 0)
    else:
        marks += screen_marks()
    return {
        "schema_version": 1,
        "model_id": f"a1-law-{name.replace('_', '-')}",
        "shape": list(shape),
        "boundary": "periodic" if periodic else "open",
        "slots_per_node": 2,
        "link_ticks": 1,
        "normal_budget": 100000,
        "ticks": TICKS,
        "K": K,
        "N": N,
        "wait_per_quantum": 1,
        "operation_costs": {name: 1 for name in OPERATIONS},
        "fields": [
            scalar("light"),
            {
                "name": "momentum",
                "components": 3,
                "units": "quantum times heading",
                "signed": True,
                "conserved": True,
                "extensive": True,
            },
        ],
        "disturbance_types": [
            {
                "name": "lamp",
                "fields": ["light", "momentum"],
                "defaults": {"light": stock, "momentum": [0, 0, 0]},
                "transport": {"mode": "hold"},
            }
        ],
        "spatial_fields": [
            {
                "field": "light",
                "baseline": 0,
                "transport": "ray",
                "headings": HEADINGS,
                "rays_per_tick": 1,
                "ray_slots": 24,
                "metric": "links",
                "pace": [1, 1],
                "charge": 0,
                "release": list(RELEASE),
                "clock": True,
            }
        ],
        "emissions": [
            {
                "type": "lamp",
                "field": "light",
                "amount": PHOTON,
                "denominator": 1,
                "heading": [1, 0, 0],
                "kerengonen_phase": 0,
            }
        ],
        "seeds": [{"position": list(lamp), "type": "lamp"}],
        "detectors": marks,
        "initial_field": {"light": {"fill": FILL}},
    }


def cases():
    # The closed board only (the model owner, 2026-09-18: only closed worlds are
    # tested); the open-board pairs measured earlier are in the register.
    yield "two_slits_periodic", world(set(PERIODIC_SLITS), "two_slits_periodic", BIG_STOCK, True)
    yield "one_slit_periodic", world({PERIODIC_SLITS[1]}, "one_slit_periodic", BIG_STOCK, True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(
            path,
            document["shape"],
            document["ticks"],
            document["model_id"],
            len(document["detectors"]),
            "marks",
        )


if __name__ == "__main__":
    main()
