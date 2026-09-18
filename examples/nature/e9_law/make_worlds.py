"""Write the worlds of E9 repeated under the law of the bit (docs/EXPERIMENTS.md,
2026-09-18): the ring of E5 radiating on E6's screen of seven marks, its field
the prefilled shadow set of one thing, mixed at every Node.

The world is `examples/nature/screen_loop.json` migrated by
`bit_law_migration.migrate` and then declared on the law: N = 64 (`phase_bits`
6), one K for the world, `wait_per_quantum` 1, the ring's eight corner lamps
eight things (the engine makes every disturbance type a distinct thing, so the
ring's field is eight shadow sets, one per ray), rays of amount M = 32768 with
`release` [1, 1] (a thing's shadow set per interval of the fill is at most its
content, so the content is what the size of the set requires: the screen's
Nodes are to hold at least 256 quanta of an owner, DERIVATIONS.md section 30),
the electron's shadows given with the board by `initial_field` `{"fill": 5}`,
32 ray slots on the electron (the layer's cap), no `light` family (there is no
field family: the ring's field is electron shadows, bit 0), no spread,
steering, mass field or seed. The dense mode is the default where the world
admits it.

The fill of 5 intervals is the longest the engine admits for this ring, read
before the runs (2026-09-18, commit ffa4a56): at 24 slots the fill of 3
exceeds the ray slot budget at a corner (the eight owners' shadows reflected
at a source Node), at 32 slots the fill of 6 does, and from 7 the prefill
refuses "a third phase on one Port of a source" (`prefill.py`, `_depart`:
two flight layers per Port at a source, and the mixing brings back more
phases than two); the engine is not changed by a run lane, so the ring's
shadow set is five intervals of release, a shell that leaves, and not a
standing set.

Read before the runs as well: with any admitted fill the run itself fails at a
corner with "ray slot budget exceeded" (`spatial_state.py`, `validate_rays`),
at tick 5 under a fill of 1, tick 2 under 2 and tick 1 from 3 on: a corner
receives the shadows of eight owners on six Ports in the two phases the mixing
makes of a phase-0 set (0 and 32 of 64), up to 96 rays against the 32 a
coupled layer admits. The worlds are written all the same and the failed runs
are the record (`ring_screen_clock_fill1` is the fill of 1, the picture).

Two worlds: `ring_screen`, the ring without a clock (the electron family
declares no `clock`; K is declared for the world all the same), and
`ring_screen_clock`, the same ring with `clock` true at K = 4096, so that each
ray of content 32768 advances 8 steps of 64 per interval, the eighth of a turn
per interval E9's ring had at N = 8.

Run:  python examples/nature/e9_law/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
from bit_law_migration import migrate  # noqa: E402

SOURCE = HERE.parent / "screen_loop.json"
PHASE_BITS = 6
RING_AMOUNT = 32768
K = 4096
FILL = 5
RAY_SLOTS = 32
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
    electron["phase_bits"] = PHASE_BITS
    electron["release"] = list(RELEASE)
    electron["ray_slots"] = RAY_SLOTS
    electron.pop("clock", None)
    if clock:
        electron["clock"] = True
    for kind in document["disturbance_types"]:
        kind["defaults"]["electron"] = RING_AMOUNT
    for emission in document["emissions"]:
        emission["amount"] = RING_AMOUNT
    document["initial_field"] = {"electron": {"fill": fill}}
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
