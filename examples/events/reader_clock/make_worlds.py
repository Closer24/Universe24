"""Write the five worlds of series S, a reader inside a crowd, and the
expectations before the runs (`expectations.json`).

The model owner, 2026-09-21 (in conversation, translated), after series U
and V: "start" the test the experimenter proposed of a detector that sits
inside a crowd itself, as Earth sits inside the Milky Way. Under the law as
built (BEAM_LAW step 4) a body's clock owes k intervals per self-creation,
k the presence of other numbers' rows at its Node over the suspension's
wall; series U and V read a lamp's slowing at a detector at rest with no
crowd. A reader inside a crowd of its own is slowed alike, and what it
reads in ITS OWN clock is the ratio of the two: 1 + z = (1 + k_s)(1 + v / c)
/ (1 + k_r), the source's clock over the reader's. A reader denser than its
source reads it BLUE; two bodies in crowds alike read no shift; the
lattice's clock (the tick) reads the source's slowing alone.

The reader's own clock is made visible by giving the reader a lamp of its
own (one unit per self-creation into the near face; its births are its
self-creations), so the reading in the reader's clock is the slope of the
source's birth ordinal against the reader's birth ordinal at the clicks. A
probe of 2026-09-21 on the engine as merged found that a waiting reader
clicks at every row that crosses it (the clicks' ticks are the lattice's;
no ordinal missing), so the lattice reading 1 / (1 + k_s) per interval is
unchanged by the reader's crowd and the reader's own count is
(1 + k_r) / (1 + k_s) clicks per birth.

The world: a bar of 121 x 9 x 9 Nodes (open). THE READER (`s_px1`, fixed at
x = 10, 2^20 units, a lamp of one unit per self-creation on -x, the wheel
[1, 64]) measures `s_px1` with `reads: "age"` and lets `mass` pass; its
crowd, when it has one, is series U's pair of `mass` sources three Links up
+y and +z with the fan of nine directions at F_r units per interval. THE
SOURCE (`s_px1`, at x = 70, the same lamp shining -x to the reader, letting
`mass` and `s_px1` pass) with its own crowd at F_s. Five worlds:

| World | k_r | k_s | the source | in the reader's clock | in the lattice's |
| --- | --- | --- | --- | --- | --- |
| control | 0 | 1 | at rest | 2.000 | 2.000 |
| reader_dense | 1 | 0 | at rest | 0.500 (blue) | 1.000 |
| alike | 1 | 1 | at rest | 1.000 | 2.000 |
| reader_half | 0.5 | 1 | at rest | 1.333 | 2.000 |
| alike_receding | 1 | 1 | 0.2 c away, its crowd at the lamp's pace | 1.100 | 2.200 |

    python examples/events/reader_clock/make_worlds.py     # the worlds and expectations.json
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))


def _crowd_clock():
    """Series U's generator, the one copy of the fan, the speeds and the
    pinned k."""
    path = HERE.parent / "crowd_clock" / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("crowd_clock_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("crowd_clock_make_worlds", module)
    spec.loader.exec_module(module)
    return module


P = _crowd_clock()
C = P.C
LENGTH = 121
SHAPE = [LENGTH, 9, 9]
Y0, Z0 = P.Y0, P.Z0
TICKS = 500
READER_X, SOURCE_X = 10, 70
SPEED_OVER_C = 0.2
# The worlds: (k_r, k_s, the source moving).
WORLDS: dict[str, tuple[float, float, bool]] = {
    "control": (0.0, 1.0, False),
    "reader_dense": (1.0, 0.0, False),
    "alike": (1.0, 1.0, False),
    "reader_half": (0.5, 1.0, False),
    "alike_receding": (1.0, 1.0, True),
}
WINDOW = (250, 500)
TOLERANCE = 0.02
EXPECTATIONS_FORMAT = "reader-clock-expectations-v1"
Json = dict[str, object]


def flux(k: float) -> int:
    return round(k * P.SUSPENSION[1] / (2 * P.DWELL))


def lamp(x: int, reader: bool, moving: bool) -> Json:
    body: Json = {
        "position": [x, Y0, Z0],
        "family": "s_px1",
        "amount": P.LIGHT,
        "phase": 0,
        "lamp": {"rate": P.LAMP_RATE, "wheel": [1, P.N], "directions": [[-1, 0, 0]]},
        "table": {
            "mass": {"rule": "pass"},
            "s_px1": {"rule": "measure", "reads": "age"} if reader else {"rule": "pass"},
        },
    }
    if moving:
        body["momentum"] = [P.momentum(SPEED_OVER_C * C, P.LIGHT), 0, 0]
    else:
        body["fixed"] = True
    return body


def crowd(x: int, k: float, moving: bool) -> list[Json]:
    f = flux(k)
    if not f:
        return []
    amount = f * P.RELEASE[1] // P.RELEASE[0]
    out: list[Json] = []
    for axis in (1, 2):
        position = [x, Y0, Z0]
        position[axis] += P.OFFSET
        source: Json = {
            "position": position,
            "family": "mass",
            "amount": amount,
            "directions": P.fan(axis),
            "table": {"s_px1": {"rule": "pass"}},
        }
        if moving:
            # the crowd slowed alike, emulated (series V): the sources at
            # the waiting lamp's pace v / (1 + k)
            source["momentum"] = [P.momentum(SPEED_OVER_C * C / (1 + k), amount), 0, 0]
        else:
            source["fixed"] = True
        out.append(source)
    return out


def world(name: str, k_r: float, k_s: float, moving: bool) -> Json:
    measured = [lamp(READER_X, True, False), lamp(SOURCE_X, False, moving)]
    measured += crowd(READER_X, k_r, False) + crowd(SOURCE_X, k_s, moving)
    return {
        "law": P.LAW_VALUE,
        "model_id": f"rays-reader-clock-{name.replace('_', '-')}-v1",
        "shape": list(SHAPE),
        "boundary": "open",
        "directions": P.declared_directions(),
        "ticks": TICKS,
        "K": P.LIGHT,
        "N": P.N,
        "release": P.RELEASE,
        "suspension": P.SUSPENSION,
        "width": P.WIDTH,
        "families": [
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
            {"name": "s_px1", "quantum": 1},
        ],
        "measured": measured,
    }


def worlds() -> dict[str, Json]:
    return {name: world(name, *spec) for name, spec in WORLDS.items()}


def expectations() -> Json:
    out: Json = {
        "format": EXPECTATIONS_FORMAT,
        "c": C,
        "ticks": TICKS,
        "window": list(WINDOW),
        "tolerance": TOLERANCE,
        "reader": 1,
        "source": 2,
        "speed_over_c_moving": SPEED_OVER_C,
        "worlds": {},
    }
    for name, (k_r, k_s, moving) in WORLDS.items():
        doppler = 1 + SPEED_OVER_C if moving else 1.0
        lattice = (1 + k_s) * doppler if not moving else 1 + k_s + SPEED_OVER_C
        out["worlds"][name] = {
            "k_reader": k_r,
            "k_source": k_s,
            "flux_reader": flux(k_r),
            "flux_source": flux(k_s),
            "moving": moving,
            # the clicks per lattice interval and per the reader's birth
            "one_plus_z_lattice": lattice,
            "one_plus_z_readers_clock": lattice / (1 + k_r),
            "clicks_per_interval": 1 / lattice,
            "clicks_per_reader_birth": (1 + k_r) / lattice,
        }
    return out


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    expected = expectations()
    (HERE / "expectations.json").write_text(json.dumps(expected, indent=1) + "\n", encoding="utf-8")
    for name, e in expected["worlds"].items():
        print(
            f"{name}: k_r = {e['k_reader']}, k_s = {e['k_source']}{', receding' if e['moving'] else ''}: "
            f"1 + z in the reader's clock {e['one_plus_z_readers_clock']:.3f}, in the lattice's {e['one_plus_z_lattice']:.3f}"
        )


if __name__ == "__main__":
    main()
