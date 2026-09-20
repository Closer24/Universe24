"""Write the three worlds of the Heisenberg run A10 at a low rate, "the
single-click build-up": the registered A10 world at w = 27 under the
`wave` reading (examples/events/heisenberg/make_worlds.py, the same
generator called here) run at three source rates.

The register entry is "A10 at a low rate, the single-click build-up" in
docs/EXPERIMENTS.md; the design and the expectation are in README.md here.
The only keys changed against the registered `w27_wave` world are the
lamps' `rate` and the world's `ticks` (and the `model_id`). A lamp of the
row releases `rate` units per self-creation on (1, 0, 0); the opening's
Nodes re-emit what arrives, apportioned whole over the fan of 47
directions (`apportion_whole`, the leftover units to the directions
counted from the Node's age): at the rate 47 one unit per direction per
interval (the registered world), at the rate n < 47 n units on n
consecutive directions of the fan per interval, the fan cycling every 47
intervals. The screen (161 one-Node `wave` pixels, 108 Links behind the
wall) then receives about n x 27 x 0.85 rays per interval in all: about
5.8 per pixel per interval at the rate 47 ("many"), about 1 at the rate 8
("about one") and about 0.12 at the rate 1 ("well below one"). The runs
are longer at the lower rates so that the late window, from WINDOW_START
on (every direction of the fan that lands on the screen has arrived by
tick 250), accumulates the same number of clicks, 160 x 47 / n intervals.

The expectation, written before the runs (README.md): the coherent record
of a `wave` pixel is the square of the pointer of the rays the pixel
clicks in ONE interval, so the cross terms exist only where two or more
rays reach one pixel in one interval; at the lowest rate the record is
the count times one unit's square at every pixel, no narrowing, and at
the highest rate it narrows as A10 read (the record's rms of sin theta
0.22 against the count's 0.32). Nature builds the same fringes one
particle at a time (Merli 1976, Tonomura 1989), the contrast independent
of the rate.

    python examples/events/buildup/make_worlds.py
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[2] / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402

# The shipped definitions the world's families come from where they equal
# them (the model owner's decision of 2026-09-20, record 113).
FAMILY_DEFINITIONS = "../entities/families.json"
DEFINITIONS_SOURCE = (HERE.parent / "entities" / "families.json").read_bytes()

SPEC = importlib.util.spec_from_file_location(
    "heisenberg_make_worlds", HERE.parent / "heisenberg" / "make_worlds.py"
)
assert SPEC is not None and SPEC.loader is not None
HEISENBERG = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(HEISENBERG)

WIDTH = 27
READING = "wave"
# The window of the reading starts when every direction of the fan that
# lands on the screen has arrived; its length is 160 x 47 / n intervals,
# the registered world's window scaled to the rate.
WINDOW_START = 260
BASE_WINDOW = 160
RATES = (47, 8, 1)


def ticks(rate: int) -> int:
    return WINDOW_START + BASE_WINDOW * HEISENBERG.F // rate


def world(rate: int) -> dict[str, object]:
    document = HEISENBERG.world(WIDTH, READING)
    assert HEISENBERG.F == 47
    document["model_id"] = f"rays-buildup-w{WIDTH}-rate{rate}-v1"
    document["ticks"] = ticks(rate)
    measured = document["measured"]
    assert isinstance(measured, list)
    for entry in measured:
        if "lamp" in entry:
            entry["lamp"]["rate"] = [rate, 1]
    return document


def main() -> None:
    for rate in RATES:
        path = HERE / f"w{WIDTH}_rate{rate}.json"
        document = families_by_definition(world(rate), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        print(f"{path.relative_to(HERE.parents[2])}: {ticks(rate)} intervals")


if __name__ == "__main__":
    main()
