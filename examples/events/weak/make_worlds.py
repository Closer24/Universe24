"""Write the worlds of series J, "the weak force", under the Beam Law (the
model owner, 2026-09-20, "go on everything": the neutrino first with the
table-entry key `phase_width` and no change of law, series J2; the
physicist's design, WEAK.md sections 1 and 4.5).

Every expectation printed here is written before the run and is a GameBoard
computation from the engine's own flight table (`nature_beam.flight_table`:
the age at which a heading ray first reaches a distance), never a rule
replayed; the readings tool (`tools/weak_readings.py`) reads the run's
record and compares.

J2, the neutrino's passage through a filled bar: a fixed source of the
free family `nu` (a phase circle, no charge, no content on its rays) of
content 4096 at x = 0 of a bar of 200 x 1 x 1, K 4096 (the turn 4096 /
4096 = 1 phase step per self-creation: the stride 1 over the circle of
N = 64) and `release` [1, 4096] (one ray per self-creation on +x), so the
ray born at tick t carries the phase (t - 1) mod 64; 128 fixed readers of
the paid family `d` (content 1, releasing nothing) at x = 8 .. 135, each
with `measure` for `nu` under a window; a far detector of `d` at x = 190
measuring `nu` without a window (it counts every ray that reaches it).
1037 intervals, so that the first reader's arrivals (the rays born at the
ticks 1 .. 1024, arriving at x = 8 at the age 13) are exactly 1024, sixteen
turns of the circle.

| world | the readers' windows | the source's stride |
| --- | --- | --- |
| `j2_filter` | every centre 0, width 1 | 1 |
| `j2_ladder` | the centre x mod 64, width 1 | 1 |
| `j2_default` | every centre 0, the default width (the half circle) | 1 |
| `j2_stride2` | every centre 0, width 1 | 2 (K 2048: the turn 2) |
| `j2_stride2_odd` | every centre 1, width 1 | 2 |

Expected (WEAK.md 1.2, PREDICTIONS entries 7 and 8): `j2_filter`, the first
reader takes every phase-0 ray, exactly 1 / 64 of its arrivals (16 of
1024), and the 127 readers behind it take nothing: a filter, not an
attenuation; the far detector reads 63 / 64 of the rays that reach its
distance in the run. `j2_ladder`, each reader takes its own residue, the
readers at x = 8 .. 71 take the 64 residues and the beam is exhausted: the
readers at x = 72 .. 135 and the far detector read 0. `j2_default`, the
first reader takes the half circle (32 of the 64 residues, 512 of 1024) and
the others nothing, the far detector half. `j2_stride2`, the phases 0, 2,
4, ... (the even coset): the first reader takes 1 / 32 of its arrivals (32
of 1024), the far detector 31 / 32. `j2_stride2_odd`, the centre 1 misses
the coset: no reader clicks, the far detector reads every ray that reaches
it. The far counts, from the flight table: the rays born at the ticks 1 ..
TICKS - a_190 (a_190 the first-arrival age at 190 Links) less the ones a
reader took.

    python examples/events/weak/make_worlds.py [--out DIR]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

import numpy as np  # noqa: E402

from event_universe.events.nature_beam import flight_table  # noqa: E402

N = 64
K_STRIDE_1 = 4096
K_STRIDE_2 = 2048
SOURCE_CONTENT = 4096
BAR = 200
READERS = range(8, 136)
FAR = 190
TICKS = 1037
PLUS_X = (1, 0, 0)
Json = dict[str, object]


def first_arrival_age(distance: int) -> int:
    """The age at which a heading ray first reaches `distance` Links, off
    the engine's flight table (a GameBoard computation of the expectation)."""
    table = flight_table(((0, 0, 0), (0, 0, 0), PLUS_X))
    ages = np.arange(1, 4 * distance + 64, dtype=np.int64)
    steps = table.manhattan_steps(np.full(ages.shape, 2, dtype=np.int64), ages)
    return int(ages[np.flatnonzero(steps >= distance)[0]])


def reader(x: int, setting: int | None, width: int | None) -> Json:
    entry: Json = {"rule": "measure"}
    if setting is not None:
        entry["phase_window"] = setting
    if width is not None:
        entry["phase_width"] = width
    return {
        "position": [x, 0, 0],
        "family": "d",
        "amount": 1,
        "fixed": True,
        "table": {"nu": entry},
    }


def world(name: str, clock: int, centres: list[int], width: int | None) -> Json:
    return {
        "law": "beam",
        "model_id": f"beam-weak-{name}-v1",
        "shape": [BAR, 1, 1],
        "boundary": "open",
        "ticks": TICKS,
        "K": clock,
        "N": N,
        "release": [1, K_STRIDE_1],
        "suspension": 0,
        "families": [
            {"name": "nu", "quantum": 0},
            {"name": "d", "quantum": 1, "phase": False},
        ],
        "measured": [
            {
                "position": [0, 0, 0],
                "family": "nu",
                "amount": SOURCE_CONTENT,
                "phase": 0,
                "fixed": True,
                "directions": [list(PLUS_X)],
            },
            *(reader(x, centre, width) for x, centre in zip(READERS, centres, strict=True)),
            reader(FAR, None, None),
        ],
    }


def worlds() -> dict[str, Json]:
    zeros = [0] * len(READERS)
    ones = [1] * len(READERS)
    ladder = [x % N for x in READERS]
    return {
        "j2_filter": world("j2_filter", K_STRIDE_1, zeros, 1),
        "j2_ladder": world("j2_ladder", K_STRIDE_1, ladder, 1),
        "j2_default": world("j2_default", K_STRIDE_1, zeros, None),
        "j2_stride2": world("j2_stride2", K_STRIDE_2, zeros, 1),
        "j2_stride2_odd": world("j2_stride2_odd", K_STRIDE_2, ones, 1),
    }


def j2_expectations() -> dict[str, dict[str, int]]:
    """The expected counts of series J2 from the flight table: the first
    reader's arrivals over the run, the far detector's clicks per world."""
    born_first = TICKS - first_arrival_age(READERS[0])
    born_far = TICKS - first_arrival_age(FAR)
    stride_1 = [(t - 1) % N for t in range(1, born_far + 1)]
    stride_2 = [(2 * (t - 1)) % N for t in range(1, born_far + 1)]
    return {
        "j2_filter": {
            "first_arrivals": born_first,
            "first_clicks": born_first // N,
            "far": sum(1 for p in stride_1 if p != 0),
        },
        "j2_ladder": {"first_arrivals": born_first, "first_clicks": born_first // N, "far": 0},
        "j2_default": {
            "first_arrivals": born_first,
            "first_clicks": born_first // 2,
            "far": sum(1 for p in stride_1 if 16 <= p < 48),
        },
        "j2_stride2": {
            "first_arrivals": born_first,
            "first_clicks": born_first // 32,
            "far": sum(1 for p in stride_2 if p != 0),
        },
        "j2_stride2_odd": {"first_arrivals": born_first, "first_clicks": 0, "far": born_far},
    }


def main() -> None:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--out", type=Path, default=HERE)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    print(
        f"J2: the bar {BAR} x 1 x 1, {len(READERS)} readers at x = {READERS[0]} .. {READERS[-1]}, "
        f"the far detector at {FAR}, {TICKS} intervals; the first-arrival ages "
        f"{first_arrival_age(READERS[0])} at {READERS[0]} Links and {first_arrival_age(FAR)} at {FAR}"
    )
    for name, expected in j2_expectations().items():
        print(f"  {name}: expected (GAMEBOARD, from the flight table) {expected}")
    for name, document in worlds().items():
        path = args.out / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
