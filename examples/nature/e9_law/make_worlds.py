"""Write the worlds of E9 repeated under the law of the bit (docs/EXPERIMENTS.md,
2026-09-18): the ring of E5 radiating on E6's screen of seven marks, its field
the prefilled shadow set of one thing, mixed at every Node.

The world is `examples/nature/screen_loop.json` migrated by
`bit_law_migration.migrate` and then declared on the law: N = 64 (the world's one
phase circle, declared once like K), one K for the world, `wait_per_quantum` 1, the ring's eight corner lamps
eight things (the engine makes every disturbance type a distinct thing, so the
ring's field is eight shadow sets, one per ray), rays of amount M = 32768 with
`release` [1, 1] (a thing's shadow set per interval of the fill is at most its
content, so the content is what the size of the set requires: the screen's
Nodes are to hold at least 256 quanta of an owner, DERIVATIONS.md section 30),
the electron's shadows given with the board by `initial_field` `{"fill": 5}`,
no `light` family (there is no field family: the ring's field is electron
shadows, bit 0), no spread, steering, mass field or seed, and no ray slot
budget (retired with the lanes, cleanup-law-v1 part 2, 2026-09-18). The dense
mode is the default where the world admits it. The board is closed: periodic
12 x 11 x 11 with a wall of marks over the plane x = 11 closing the wrap in x,
as A1's closed board has (the model owner's decisions of 2026-09-18: the board
of a run is closed, and only closed worlds are tested).

The fill of 5 intervals was declared when the engine at ffa4a56 admitted no
longer one (the prefill refused a third phase on one Port of a source from a
fill of 7, and the ray slot budget failed every admitted fill at a corner
within five ticks: the eight owners' shadows in the two phases the mixing
makes of a phase-0 set, against the 32 rays a coupled layer admitted). On the
engine with the lanes (origin/main at 204a513) every fill of the scan is
admitted and runs (`scan_fill.py`: 1 to 8 and 16, 40 ticks each), the worlds
keep the fill of 5 as declared, and `ring_screen_clock_fill1`, the fill of 1,
stays as the third world. The three worlds complete their 240 ticks; the
earlier refusals are recorded in the register entry.

Two worlds: `ring_screen`, the ring without a clock (the electron family
declares no `clock`; K is declared for the world all the same), and
`ring_screen_clock`, the same ring with `clock` true at K = 4096, so that each
ray of content 32768 advances 8 steps of 64 per interval, the eighth of a turn
per interval E9's ring had at N = 8.

Run:  python examples/nature/e9_law/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from bit_law_migration import migrate  # noqa: E402

SOURCE = HERE.parent / "screen_loop.json"
N = 64
RING_AMOUNT = 32768
K = 4096
FILL = 5
TICKS = 240
RELEASE = [1, 1]


def ring_world(*, clock: bool, fill: int = FILL) -> dict:
    document = migrate(json.loads(SOURCE.read_text(encoding="utf-8")))
    document["model_id"] = (
        "e9-law-ring-screen" + ("-clock" if clock else "") + (f"-fill{fill}" if fill != FILL else "")
    )
    document["ticks"] = TICKS
    document["K"] = K
    document["wait_per_quantum"] = 1
    # No field family under the law: the ring's field is the electron's shadows.
    document["fields"] = [f for f in document["fields"] if f["name"] != "light"]
    document["spatial_fields"] = [f for f in document["spatial_fields"] if f["field"] != "light"]
    (electron,) = document["spatial_fields"]
    document["N"] = N
    electron["release"] = list(RELEASE)
    electron.pop("clock", None)
    if clock:
        electron["clock"] = True
    for kind in document["disturbance_types"]:
        kind["defaults"]["electron"] = RING_AMOUNT
    for emission in document["emissions"]:
        emission["amount"] = RING_AMOUNT
    document["initial_field"] = {"electron": {"fill": fill}}
    # The closed board (the model owner, 2026-09-18: the board of a run is closed,
    # and only closed worlds are tested): periodic, with a wall of marks over the
    # plane x = X - 1 closing the wrap in x, as A1's closed board has, so that
    # the shadows leaving the ring toward -X do not reach the screen from behind.
    document["boundary"] = "periodic"
    shape = document["shape"]
    mark = {k: v for k, v in document["detectors"][0].items() if k != "position"}
    document["detectors"] += [
        {"position": [shape[0] - 1, y, z], **copy.deepcopy(mark)}
        for y in range(shape[1])
        for z in range(shape[2])
    ]
    text = json.dumps(document)
    for key in ("spread", "steering", "mass_field", "seed", "field_of"):
        assert f'"{key}":' not in text, key
    return document


def cases():
    yield "ring_screen", ring_world(clock=False)
    yield "ring_screen_clock", ring_world(clock=True)
    # The fill of one interval, the only one under which the engine completes a
    # tick (four, before the corners overflow at tick 5): the failure's picture.
    yield "ring_screen_clock_fill1", ring_world(clock=True, fill=1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    for name, document in cases():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
        print(path, document["shape"], document["ticks"], document["model_id"])


if __name__ == "__main__":
    main()
