"""Write the nine worlds of series X, Poisson after a detector (a clock's
rate read at a detector inside and outside a shell of sources), and the
register's pins before any run (`expectations.json`).

The chief physicist's design of 2026-09-22 (record 574 of
docs/LOG_2026-09-20.md, part 2, POISSON AFTER A DETECTOR) under the model
owner's word of that day ("build them", records 574 and 581). Series E read
the clock's 1 / r off the probes' registers, a GameBoard reading of a world
with no detector (records 562, 564 and 575); series T reads a clock's rate
after a detector at two distances from a point crowd (NATURE row 12,
REPLICATED), which is Laplace's part, the field outside its source. Poisson's
equation is the source term, and this series reads it after a detector at
both of its sides: inside a shell of sources the potential is flat (the
shell theorem) and outside it falls as C / r.

DERIVATIONS_BEAM section 5.1 gives the age moment of one source,
A = q dwell / (4 pi c r), so a distribution's age moment is the
superposition of its sources' and obeys Poisson's equation with the
sources' release as the density; under the age word (the law's default
since clock-age-v1, record 394) a body's clock counts that age moment and
its rate is 1 / (1 + k_a), so a lamp's births per interval, read at a
detector, read the field the sources make.

The worlds, series T's geometry with the crowd's point source replaced by a
shell (`../clock_word/make_worlds.py` imported for the speeds, the lamp and
the suspension pair; `../redshift/make_worlds.py` for the one copy of the
fan of 290):

- the lamp `s_px1` at rest at x = 103 (2^20 units, one unit per
  self-creation on -x, the wheel [1, 64]), the detector fixed at x = 3
  measuring `s_px1` with `reads: "age"`, so the flight is series T's 100
  Links and the windows are series T's;
- a shell of `mass` sources of radius R = 6 about a centre r Links from the
  lamp on +x, away from the detector, so that the lamp's light never
  crosses the shell when the lamp is outside it: the shell's Nodes are
  those at |distance - R| < 1/2 (series E's selection, 450 Nodes), each
  fixed and releasing on the full fan of 290;
- the release: series T's crowd's total release pair, 2 F with F = 4915
  units per direction per interval, spread over the shell's Nodes, so
  `amount` = 2 F x 2^16 / 450 and each source releases 21.8444 units per
  direction per interval at `release` [1, 2^16];
- the lamp at r = 2 and r = 4 (inside the shell) and r = 12 (outside), each
  under the age word (the lamp's `mass` entry `{"rule": "pass", "reads":
  "age"}`) and, run beside it as series T ran it, under the presence word
  (`{"rule": "pass", "reads": "presence"}`), each with its control, the lamp
  alone on the same GameBoard: nine worlds, the six of the design's point (2)
  and the three the design's point (3) orders beside them.

THE PINS ARE THE MAP'S, WRITTEN BEFORE ANY RUN: section E of
docs/designs/clock_age/clock_age_map.py, whose numbers are in
clock_age_map.out beside it. The map walks every source's lines on the
engine's own flight table and states, per unit of the release, the presence
and the age moment the whole shell leaves at each lamp's Node; then it
iterates one fixed point the design did not foresee and the world requires:
THE SHELL'S SOURCES STAND IN ONE ANOTHER'S ROWS, so each source's own clock
counts the age moment at its Node (the law's default word) and a source
releases only at its self-creations, at its declared rate over 1 + its own
count. With uniform sources the interior is flat exactly, one integer, 5086,
at r = 2 and at r = 4; the spread of the sources' own clocks over the
lattice shell (their count runs 0.787 to 0.932) is the ripple the pin
carries, 0.0039 on the inside ratio, and nothing else moves it.

    python examples/events/shell_clock/make_worlds.py   # the worlds and expectations.json
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.core.game_board import PORT_HEADINGS  # noqa: E402
from event_universe.events.world import HEADING_OFFSET  # noqa: E402
from event_universe.register_map import carry_replicated  # noqa: E402


def _module(folder: str, name: str):
    """A sibling series' generator, imported as series T imports series U's:
    one copy of the fan, the speeds and the pinned keys."""
    path = HERE.parent / folder / "make_worlds.py"
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, module)
    spec.loader.exec_module(module)
    return module


T = _module("clock_word", "clock_word_make_worlds")
E = _module("redshift", "redshift_make_worlds")
P = T.P
C = T.C
# The fan of 290 (series E's: every primitive direction with
# 0 < |a| + |b| + |c| <= 6) on which every source of the shell releases.
FAN = [list(v) for v in E.fan(E.FAN_MANHATTAN)]
HEADINGS = set(PORT_HEADINGS)
DECLARED = [v for v in FAN if tuple(v) not in HEADINGS]
# Every source releases on the same fan, so each one names it by the
# indices of the world's direction table rather than by 290 vectors (the
# world file takes either; the table is the two rest vectors, the six
# headings in Port order, then the declared, `world._direction_table`):
# nine worlds of a third the bytes, the same documents to the engine.
FAN_INDICES = [
    HEADING_OFFSET + PORT_HEADINGS.index(tuple(v))
    if tuple(v) in HEADINGS
    else HEADING_OFFSET + len(PORT_HEADINGS) + DECLARED.index(v)
    for v in FAN
]
# The shell and the lamp's distances from its centre (the design's point 2).
RADIUS = 6
RADII = (2, 4, 12)
# Series T's geometry: the flight of 100 Links from the lamp to the
# detector, the lamp shining away from the shell, the cross-section holding
# the shell (the shell spans 13 Nodes on y and on z about the centre).
LAMP_X, DETECTOR_X = 103, 3
SIDE = 15
FLUX = T.FLUX
TICKS = T.TICKS
WINDOWS = T.WINDOWS
# The words of the lamp's entry for the crowd's family, and the worlds:
# (the word or None for the control, the lamp's distance from the centre).
WORDS = ("age", "presence")
EXPECTATIONS_FORMAT = "shell-clock-expectations-v1"
Json = dict[str, object]

# THE MAP'S NUMBERS (docs/designs/clock_age/clock_age_map.py section E, its
# output in clock_age_map.out; nothing here is typed from a run).
# Per unit of the release per source per direction, what the whole shell
# leaves at the lamp's Node with uniform sources:
UNIFORM_PRESENCE = {2: 499, 4: 596, 12: 163}
UNIFORM_AGE_MOMENT = {2: 5086, 4: 5086, 12: 3144}
# The fixed point of the sources' own clocks: their own count and the
# release each one keeps, and the pinned k at the lamp under each word.
SOURCE_OWN_COUNT = (0.787, 0.932, 0.866)
EFFECTIVE_RATE = (11.3054, 12.2240, 11.7078)
PINNED_K = {
    "age": {2: 0.914351, 4: 0.910783, 12: 0.563110},
    "presence": {2: 0.089647, 4: 0.106724, 12: 0.029271},
}
PINNED_K_UNIFORM = {2: 1.695264, 4: 1.695264, 12: 1.047957}
PINNED_RATIOS = {
    "inside_age": 1.003917,
    "inside_presence": 0.839989,
    "outside_age": 0.618270,
}
# The brackets. The two ratios of k are what decides, and a common factor
# on the shell's release cancels in them exactly, so they are pinned at the
# map's value within 0.02 (five times the map's ripple 0.0039). The
# absolute k carries what the map's fixed point does not model, the bursts
# of a slowed source's release (a source releases its whole rate at a
# self-creation and nothing between): pinned within a tenth of itself.
RATIO_TOLERANCE = 0.02
K_FRACTION = 0.10


def shell_offsets(radius: int) -> list[tuple[int, int, int]]:
    """The Nodes at Euclidean distance within a half Link of `radius` from
    the centre, as offsets from it, in a fixed order (series E's selection
    of a shell, `redshift/make_worlds.py`; the design's |r - R| < 1/2)."""
    found = []
    for x in range(-radius - 1, radius + 2):
        for y in range(-radius - 1, radius + 2):
            for z in range(-radius - 1, radius + 2):
                if abs(math.sqrt(x * x + y * y + z * z) - radius) < 0.5:
                    found.append((x, y, z))
    return found


SHELL = shell_offsets(RADIUS)
# The release per source: series T's crowd's total release pair, 2 F units
# per direction per interval, spread over the shell's Nodes (the design's
# scaling: each source releases on the full fan, so the release pair per
# source is scaled down by the shell's Node count).
AMOUNT = 2 * FLUX * P.SUSPENSION[1] // len(SHELL)
RATE = AMOUNT / P.SUSPENSION[1]


def length(radius: int) -> int:
    """The GameBoard's extent on x: the detector, the lamp and the shell's
    far side, which is `radius` + R Links beyond the lamp."""
    return LAMP_X + radius + RADIUS + 1


def world(word: str | None, radius: int) -> Json:
    """One world: the lamp and the detector, and, unless this is the
    control, the shell of sources centred `radius` Links from the lamp on
    +x. `word` is the word the lamp's entry for the crowd declares."""
    centre = SIDE // 2
    detector: Json = {
        "position": [DETECTOR_X, centre, centre],
        "family": "detector",
        "amount": 1,
        "fixed": True,
        "table": {"s_px1": {"rule": "measure", "reads": "age"}},
    }
    lamp: Json = {
        "position": [LAMP_X, centre, centre],
        "family": "s_px1",
        "amount": P.LIGHT,
        "phase": 0,
        "fixed": True,
        "lamp": {"rate": P.LAMP_RATE, "wheel": [1, P.N], "directions": [[-1, 0, 0]]},
    }
    if word is not None:
        lamp["table"] = {"mass": {"rule": "pass", "reads": word}}
    sources: list[Json] = [
        {
            "position": [LAMP_X + radius + dx, centre + dy, centre + dz],
            "family": "mass",
            "amount": AMOUNT,
            "fixed": True,
            "directions": FAN_INDICES,
            "table": {"s_px1": {"rule": "pass"}},
        }
        for dx, dy, dz in SHELL
    ]
    if word is None:
        # The control: the lamp alone on the same GameBoard, the shell removed.
        sources = []
    name = "control" if word is None else f"shell-{word}"
    return {
        "law": P.LAW_VALUE,
        "model_id": f"rays-shell-clock-{name}-{radius}-v1",
        "shape": [length(radius), SIDE, SIDE],
        "boundary": "open",
        "directions": DECLARED,
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
    """The nine worlds by name: the three distances under each word and the
    three controls (the lamp alone on the same GameBoard)."""
    found: dict[str, Json] = {}
    for word in WORDS:
        for radius in RADII:
            found[f"{word}_{radius}"] = world(word, radius)
    for radius in RADII:
        found[f"control_{radius}"] = world(None, radius)
    return found


def expectations() -> Json:
    """The register's pins, all of them the map's (section E of
    docs/designs/clock_age/clock_age_map.py), written before any run."""
    out: Json = {
        "format": EXPECTATIONS_FORMAT,
        "derivation": (
            "docs/designs/clock_age/clock_age_map.py section E (its output in clock_age_map.out "
            "beside it), the shell's lines on the engine's own flight table: per unit of the "
            "release the whole shell leaves the age moment 5086 at r = 2 and 5086 at r = 4, one "
            "integer (the shell theorem on the lattice: the interior is flat exactly), and 3144 at "
            "r = 12, against the presence 499, 596 and 163 (the flux rises toward the shell); then "
            "the fixed point of the sources' own clocks, which the shell requires and the design "
            "did not foresee (a source stands in its neighbours' rows, counts their age moment by "
            "the law's default word and releases only at its self-creations, at its rate over 1 + "
            "its own count), whose spread over the lattice shell is the ripple of the inside pin. "
            "DERIVATIONS_BEAM section 5.1 (A = q dwell / (4 pi c r) per source, the superposition, "
            "Poisson's equation with the release as the density) and 5.2 (the rate 1 / (1 + k_a)); "
            "BEAM_LAW section 3 step 5 and note 25; clock-age-v1 (record 394, the age word the "
            "law's default)"
        ),
        "c": C,
        "ticks": TICKS,
        "flux": FLUX,
        "windows": [list(w) for w in WINDOWS],
        "shell": {
            "radius": RADIUS,
            "nodes": len(SHELL),
            "fan": len(FAN),
            "amount": AMOUNT,
            "declared_rate": RATE,
            "effective_rate": {
                "lowest": EFFECTIVE_RATE[0],
                "highest": EFFECTIVE_RATE[1],
                "mean": EFFECTIVE_RATE[2],
            },
            "source_own_count": {
                "lowest": SOURCE_OWN_COUNT[0],
                "highest": SOURCE_OWN_COUNT[1],
                "mean": SOURCE_OWN_COUNT[2],
            },
        },
        "ratio_tolerance": RATIO_TOLERANCE,
        "k_fraction": K_FRACTION,
        "worlds": {},
        "ratios": {},
        "derivations": {
            "one_plus_z": (
                "DETECTOR: the lamp's light at the detector, 1 + z the inverse slope of the birth "
                "ordinal against the click's tick in the window, series T's reading; k = 1 + z - 1 "
                "the count the lamp's clock owes per self-creation, the shell's age moment times "
                "the suspension pair under the age word and its presence under the presence word "
                "(the map's section E). The click lines of events.jsonl alone are read: no store, "
                "no replay, no reading of the GameBoard (the owner's word of 2026-09-22, records "
                "562 and 564)"
            ),
            "inside_age": (
                "THE PIN INSIDE, the age word: k(2) / k(4) = 1.003917, the continuum's 1 (the shell "
                "theorem: the potential is flat inside a shell of sources, Poisson's source term); "
                "the departure from 1 is the map's ripple, the spread of the sources' own clocks "
                "over the lattice shell. Refuted, and Poisson's source term with it, if the "
                "reading departs from 1 by more than 0.02, five times that ripple"
            ),
            "inside_presence": (
                "THE PIN INSIDE, the presence word, expected to FAIL: k(2) / k(4) = 0.839989, 41 "
                "times the age word's ripple from 1, because 1 / r^2 obeys the flux (Gauss) and "
                "not the potential (Poisson) and rises toward the shell. The one reading that "
                "tells the two words apart at a source term; reported as it reads"
            ),
            "outside_age": (
                "THE PIN OUTSIDE, the age word: k(12) / k(4) = 0.618270, the exterior of the shell "
                "the point source's C / r; the continuum's R / 12 = 0.5 and the lattice above it "
                "by the grain of the map's section C, where the age moment times r rises with r "
                "(series E's shell means read the same grain). Refuted, and series T's 1 / r with "
                "it, if the reading misses the map's value by more than 0.02"
            ),
            "control": (
                "DETECTOR: the lamp alone on the same GameBoard, 1 + z = 1.0000 exactly (no crowd, "
                "nothing owed, one birth per interval); the control of each world, the lamp's own "
                "spending and the flight read without the shell"
            ),
        },
    }
    for name, document in worlds().items():
        word, radius = name.rsplit("_", 1)
        radius = int(radius)
        control = word == "control"
        k = 0.0 if control else PINNED_K[word][radius]
        out["worlds"][name] = {
            "word": None if control else word,
            "radius": radius,
            "inside": radius < RADIUS,
            "shape": document["shape"],
            "k": k,
            "k_bracket": [(1 - K_FRACTION) * k, (1 + K_FRACTION) * k],
            "one_plus_z": 1 + k,
            "clicks_per_interval": 1 / (1 + k),
            "flight": (LAMP_X - DETECTOR_X) / C,
            "uniform_presence": None if control else UNIFORM_PRESENCE[radius],
            "uniform_age_moment": None if control else UNIFORM_AGE_MOMENT[radius],
            "k_uniform_sources": None if control else PINNED_K_UNIFORM[radius],
        }
    out["ratios"] = {
        "inside_age": {
            "reading": "k(2) / k(4) under the age word",
            "pinned": PINNED_RATIOS["inside_age"],
            "continuum": 1.0,
            "ripple": abs(PINNED_RATIOS["inside_age"] - 1.0),
            "tolerance": RATIO_TOLERANCE,
        },
        "inside_presence": {
            "reading": "k(2) / k(4) under the presence word",
            "pinned": PINNED_RATIOS["inside_presence"],
            "continuum": 1.0,
            "expected": "FAIL: the flux is not flat inside a shell",
            "tolerance": RATIO_TOLERANCE,
        },
        "outside_age": {
            "reading": "k(12) / k(4) under the age word",
            "pinned": PINNED_RATIOS["outside_age"],
            "continuum": RADIUS / 12,
            "tolerance": RATIO_TOLERANCE,
        },
    }
    return out


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    expected = carry_replicated(HERE / "expectations.json", expectations())
    (HERE / "expectations.json").write_text(json.dumps(expected, indent=1) + "\n", encoding="utf-8")
    print(
        f"the shell: {len(SHELL)} Nodes at |r - {RADIUS}| < 1/2, the fan of {len(FAN)}, "
        f"{AMOUNT} / 2^16 = {RATE:.4f} units per source per direction per interval"
    )
    for name, e in expected["worlds"].items():
        where = "inside" if e["inside"] else "outside"
        print(
            f"{name}: the {e['word'] or 'control'} world at r = {e['radius']} ({where}): pinned "
            f"k = {e['k']:.6f}, 1 + z = {e['one_plus_z']:.6f}, the clicks per interval "
            f"{e['clicks_per_interval']:.4f}"
        )
    for key, r in expected["ratios"].items():
        print(f"{key}: pinned {r['pinned']:.6f} +- {r['tolerance']} (the continuum {r['continuum']})")


if __name__ == "__main__":
    main()
