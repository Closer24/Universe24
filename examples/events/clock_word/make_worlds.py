"""Write the four worlds of series T, the clock's word (the presence or the
age moment), and the register's expectations before the run
(`expectations.json`).

The Boss's order of 2026-09-21 (12:45Z) to the G2 experimenter: build the
four worlds exactly as the physicist's read pins them
(docs/designs/clock_age/NOTE.md section 6, its numbers from
clock_age_map.py), a rule-353 experiment: a second pair of hands on the
physicist's pin, the replicator to run it again later. The question: the
law's clock counts the presence of other numbers' rows at a body's Node
(BEAM_LAW section 3 step 5), or on a table entry that reads `age` the age
moment `sum amount x age`; the G2 session's proposal (record 365) is that
the age word is the potential's form, the one nature's clocks measure. The
pin that decides on the GameBoard: two crowds of the same release F at
different distances are the same push, and only the age clock reads the
distance.

The worlds, in series U's geometry (`../crowd_clock/make_worlds.py`, the
one copy of the fan, the speeds and the pinned k): the lamp `s_px1` at rest
at x = 10 (2^20 units, one unit per self-creation on +x, the wheel
[1, 64]), two `mass` sources at 3 or at 6 Links on +y and +z, each
releasing F = 4915 units per interval on series U's fan of nine toward the
lamp's line, `suspension` [1, 2^16], the detector fixed at x = 110
measuring `s_px1` with `reads: "age"`; the lamp's entry for `mass`
`{"rule": "pass", "reads": "presence"}` (the presence word; the bare `pass`
until clock-age-v1, 2026-09-21) or `{"rule": "pass", "reads": "age"}` (the
age word, series E's precedent, the law's default since clock-age-v1); the bar 121 x 9 x 9 at 3 Links (series U's) and
121 x 15 x 15 at 6. Run under beam-v1 as declared: no change under src/.

    python examples/events/clock_word/make_worlds.py     # the worlds and expectations.json
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
    """Series U's generator, the one copy of the fan and the speeds."""
    path = HERE.parent / "crowd_clock" / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("crowd_clock_make_worlds", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("crowd_clock_make_worlds", module)
    spec.loader.exec_module(module)
    return module


P = _crowd_clock()
C = P.C
LENGTH = 121
LAMP_X, DETECTOR_X = 10, 110
FLUX = 4915
TICKS = 500
WINDOWS = ((200, 350), (350, 500))
# The worlds: (the word, the sources' distance in Links, the cross-section).
WORLDS: dict[str, tuple[str, int, int]] = {
    "presence_3": ("presence", 3, 9),
    "presence_6": ("presence", 6, 15),
    "age_3": ("age", 3, 9),
    "age_6": ("age", 6, 15),
}
# The pins of NOTE.md section 6 (the map's section B): per unit of F the
# presence at the lamp's Node (two headings' rows, each present two
# intervals) and the age moment (the dwelling ages per source), the first
# interval with the crowd's rows at the lamp, the dwelling ages.
PRESENCE_PER_F = {3: 4, 6: 4}
AGE_MOMENT_PER_F = {3: 22, 6: 42}
DWELLING_AGES = {3: [5, 6], 6: [10, 11]}
FIRST_ROW_TICK = {3: 6, 6: 11}
TOLERANCE = {"presence": 0.02, "age": 0.05}
RATIO_TOLERANCE = 0.05
EXPECTATIONS_FORMAT = "clock-word-expectations-v1"
Json = dict[str, object]


def fan(axis: int, distance: int) -> list[list[int]]:
    """Series U's fan of nine toward the lamp's line from a source `distance`
    Links up the axis, (dx, -distance, 0) or (dx, 0, -distance) for
    dx = -4 .. 4, each in primitive form."""
    import math

    out = []
    for dx in range(-4, 5):
        d = [dx, 0, 0]
        d[axis] = -distance
        g = math.gcd(*d)
        out.append([component // g for component in d])
    return out


def declared_directions(distance: int) -> list[list[int]]:
    return [d for d in fan(1, distance) + fan(2, distance) if sum(abs(c) for c in d) != 1]


def world(name: str, word: str, distance: int, side: int) -> Json:
    centre = side // 2
    # Since clock-age-v1 (2026-09-21) the clock's default is the age moment,
    # so the presence word is declared: `reads: "presence"` (until then the
    # bare `pass` counted the presence and `reads: "age"` the age moment).
    mass_entry: Json = (
        {"rule": "pass", "reads": "presence"} if word == "presence" else {"rule": "pass", "reads": "age"}
    )
    lamp: Json = {
        "position": [LAMP_X, centre, centre],
        "family": "s_px1",
        "amount": P.LIGHT,
        "phase": 0,
        "fixed": True,
        "lamp": {"rate": P.LAMP_RATE, "wheel": [1, P.N], "directions": [[1, 0, 0]]},
        "table": {"mass": mass_entry},
    }
    sources: list[Json] = []
    for axis in (1, 2):
        position = [LAMP_X, centre, centre]
        position[axis] += distance
        sources.append(
            {
                "position": position,
                "family": "mass",
                "amount": FLUX * P.RELEASE[1] // P.RELEASE[0],
                "fixed": True,
                "directions": fan(axis, distance),
                "table": {"s_px1": {"rule": "pass"}},
            }
        )
    detector: Json = {
        "position": [DETECTOR_X, centre, centre],
        "family": "detector",
        "amount": 1,
        "fixed": True,
        "table": {"s_px1": {"rule": "measure", "reads": "age"}},
    }
    return {
        "law": P.LAW_VALUE,
        "model_id": f"rays-clock-word-{name.replace('_', '-')}-v1",
        "shape": [LENGTH, side, side],
        "boundary": "open",
        "directions": declared_directions(distance),
        "ticks": TICKS,
        "K": P.LIGHT,
        "N": P.N,
        "release": P.RELEASE,
        "suspension": P.SUSPENSION,
        "width": P.WIDTH,
        "families": [
            {"name": "detector", "quantum": 1},
            {"name": "mass", "quantum": 0, "charge": 0, "phase": False},
            {"name": "s_px1", "quantum": 1},
        ],
        "measured": [detector, lamp, *sources],
    }


def worlds() -> dict[str, Json]:
    return {name: world(name, *spec) for name, spec in WORLDS.items()}


def pinned_k(word: str, distance: int) -> float:
    per_f = PRESENCE_PER_F[distance] if word == "presence" else AGE_MOMENT_PER_F[distance]
    return per_f * FLUX * P.SUSPENSION[0] / P.SUSPENSION[1]


def expectations() -> Json:
    out: Json = {
        "format": EXPECTATIONS_FORMAT,
        "derivation": (
            "docs/designs/clock_age/NOTE.md section 6 (the two-crowd pin before any run) and "
            "docs/designs/clock_age/clock_age_map.py section B (the dwell of the headings' rows at "
            "the lamp's Node by the engine's flight lines): the presence 4 F at both distances, the "
            "age moment 22 F at 3 Links (the ages 5, 6 per source) and 42 F at 6 (10, 11); "
            "BEAM_LAW section 3 step 5 (the clock's count) and note 25"
        ),
        "c": C,
        "ticks": TICKS,
        "flux": FLUX,
        "windows": [list(w) for w in WINDOWS],
        "ratio_tolerance": RATIO_TOLERANCE,
        "worlds": {},
        "ratios": {},
        "derivations": {
            "one_plus_z": (
                "DETECTOR: the lamp's light at x = 110, 1 + z the inverse slope of the birth ordinal "
                "against the click's tick in the window, series U's reading; k the count the lamp's "
                "clock owes per self-creation, presence x n / d under the presence word, the age "
                "moment x n / d under the age word (NOTE.md section 6)"
            ),
            "first_row_tick": (
                "the first interval with the crowd's rows at the lamp's Node: the first row's age 5 "
                "(3 Links) or 10 (6 Links) at that Link on the heading, the sources releasing from "
                "tick 1 (the map's section A and B); read from the lamp's record as the first tick "
                "its clock counts (GAMEBOARD, a replay of the world) and as the first birth the lamp "
                "misses (DETECTOR)"
            ),
            "ratio_6_over_3": (
                "the ratio of the two k at the same F: the presence word 1.000 (the presence clock "
                "cannot tell the two distances apart), the age word 42 / 22 = 1.909 (the "
                "continuum's potential at the same push: 2.000)"
            ),
        },
    }
    for name, (word, distance, side) in WORLDS.items():
        k = pinned_k(word, distance)
        out["worlds"][name] = {
            "word": word,
            "distance": distance,
            "cross_section": side,
            "k": k,
            "one_plus_z": 1 + k,
            "tolerance": TOLERANCE[word],
            "presence_per_f": PRESENCE_PER_F[distance],
            "age_moment_per_f": AGE_MOMENT_PER_F[distance],
            "counted": (PRESENCE_PER_F[distance] if word == "presence" else AGE_MOMENT_PER_F[distance])
            * FLUX,
            "dwelling_ages_per_source": DWELLING_AGES[distance],
            "first_row_tick": FIRST_ROW_TICK[distance],
            "clicks_per_interval": 1 / (1 + k),
            "flight": (DETECTOR_X - LAMP_X) / C,
        }
    for word in ("presence", "age"):
        k3, k6 = pinned_k(word, 3), pinned_k(word, 6)
        out["ratios"][word] = {"k_6_over_k_3": k6 / k3, "continuum": 1.0 if word == "presence" else 2.0}
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
            f"{name}: the {e['word']} word at {e['distance']} Links: counted {e['counted']} = "
            f"{e['counted'] // FLUX} F, k = {e['k']:.3f}, 1 + z = {e['one_plus_z']:.3f} "
            f"(+- {e['tolerance']}), the first row at tick {e['first_row_tick']}"
        )
    for word, r in expected["ratios"].items():
        print(
            f"the {word} word, k at 6 over k at 3: {r['k_6_over_k_3']:.3f} (the continuum {r['continuum']:.3f})"
        )


if __name__ == "__main__":
    main()
