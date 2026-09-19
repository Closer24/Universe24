"""Write the ten worlds of the Bell run A2 under the law of the ray.

One base world, the settings the only difference between the files
(README.md here; the entry "A2, under the law of the ray (2026-09-19)" in
docs/EXPERIMENTS.md): a bar of 21 x 1 x 1, open, `"law": "rays"`, K 2^20,
N 64, no release of a free family, no suspension, the families `light`
and `counter`, both paid (`quantum` 1; the kind follows from the quantum).
The lamp of `light` at x = 10, content K + 2 (so that the release of age a
is stamped with the phase a mod 64 exactly for every age of the run), one
ray per self-creation on +X and on -X, no window (the source cycles the
whole circle). Four counters of content 1, each its own detector of
threshold 1, measuring `light` (the rule the keys give a paid family; the
table declares only the window) through a phase window:
`alice_plus` at x = 2 (window a), `alice_minus` at x = 1 (window a + 32 mod
64), `bob_plus` at x = 18 (window b), `bob_minus` at x = 19 (window b + 32
mod 64). The two windows of a side cover the circle exactly, so every ray
clicks exactly once per side. A ray flies at 1 / sqrt 3: the eight Links to
a plus Node take 13 intervals after the ray's first walk and the ninth Link
two more (the flight table, docs/RAY_LAW.md), so 160 intervals hold the 128
pairs analysed (the ages 0..127) and their last minus click.

    python examples/events/bell/make_worlds.py
"""

from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
K = 1 << 20
N = 64
PAIRS = 128
LAMP_X = 10
PATH = 8  # Links from the lamp to a plus Node: x = 10 to x = 2 and to x = 18.
# A ray released at tick t first walks at t + 1; eight Links take 13 walks and
# the ninth two more (the flight table): the minus click of age a is at tick
# a + 1 + 15 = a + 16, so 160 intervals hold the ages 0..127 and their clicks.
TICKS = PAIRS + 32
# (a, b): the CHSH quadruple, the three controls, the non-saturating quadruple.
SETTINGS = [(0, 8), (0, 24), (16, 8), (16, 24), (0, 0), (0, 32), (0, 16), (0, 12), (4, 8), (4, 12)]


def counter(x: int, window: int) -> dict[str, object]:
    return {
        "position": [x, 0, 0],
        "family": "counter",
        "amount": 1,
        "fixed": True,
        "table": {"light": {"phase_window": window}},
    }


def world(a: int, b: int) -> dict[str, object]:
    return {
        "law": "rays",
        "model_id": f"rays-bell-a{a}-b{b}-v1",
        "shape": [2 * LAMP_X + 1, 1, 1],
        "boundary": "open",
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": [0, 1],
        "suspension": 0,
        "families": [{"name": "light", "quantum": 1}, {"name": "counter", "quantum": 1}],
        "measured": [
            {
                "position": [LAMP_X, 0, 0],
                "family": "light",
                "amount": K + 2,
                "phase": 0,
                "fixed": True,
                "lamp": {"rate": [1, 1], "directions": [[1, 0, 0], [-1, 0, 0]]},
            },
            counter(LAMP_X - PATH, a),
            counter(LAMP_X - PATH - 1, (a + N // 2) % N),
            counter(LAMP_X + PATH, b),
            counter(LAMP_X + PATH + 1, (b + N // 2) % N),
        ],
        "detectors": [
            {"name": "alice_plus", "positions": [[LAMP_X - PATH, 0, 0]], "threshold": 1},
            {"name": "alice_minus", "positions": [[LAMP_X - PATH - 1, 0, 0]], "threshold": 1},
            {"name": "bob_plus", "positions": [[LAMP_X + PATH, 0, 0]], "threshold": 1},
            {"name": "bob_minus", "positions": [[LAMP_X + PATH + 1, 0, 0]], "threshold": 1},
        ],
    }


def main() -> None:
    for a, b in SETTINGS:
        path = HERE / f"a{a}_b{b}.json"
        path.write_text(json.dumps(world(a, b), indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(HERE.parents[2]))


if __name__ == "__main__":
    main()
