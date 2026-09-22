"""The pin worlds of `optical-v1` in its generic form (the model owner's
"go" of 2026-09-21, record 303, in the generic form of records 421 to 428;
docs/designs/one_wall/NOTE.md section 6; docs/designs/open_problems/
light_bending/NOTE.md section 5; REVIEW_3 section 5): series K's `mass`
(M = 2^16, b = 6) and `near` (2^16, b = 3) at the suspension pair
[1, 16384], the mass sixteen times series K's, under the world key
`optical: gamma` at gamma = 0 (f = 1, the six verbs' own number, Newton's
half) and gamma = 1 (f = 2, nature's PPN gamma), with the control (no
mass) at each gamma for the readings tool; the screen's entry keeps
`reads: age` (the detector's reading of the delay), the lamp's `mass`
entry declares no word (record 394's default). The worlds are written
from series K's generator (`examples/events/lensing/make_worlds.py`, the
one copy of the fan, the beam and the screen) and the expectations before
any run (`expectations.json`: the note's table, the shifts and delays from
the lattice's lines, the ratio of the two shifts 2.00 the number a run
reads).

    python examples/events/optical/make_worlds.py     # the worlds and expectations.json
    PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/optical_g0 examples/events/optical/control_g0.json examples/events/optical/mass_g0.json examples/events/optical/near_g0.json examples/events/optical/far_g0.json
    PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/optical_g1 examples/events/optical/control_g1.json examples/events/optical/mass_g1.json examples/events/optical/near_g1.json examples/events/optical/far_g1.json
    PYTHONPATH=src python tools/lensing_readings.py artifacts/optical_g0     # and _g1: the centroid's shift and the delay against the control
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.register_map import carry_replicated  # noqa: E402
from event_universe.world_loading import families_by_definition  # noqa: E402

Json = dict[str, object]
EXPECTATIONS_FORMAT = "optical-expectations-v1"
# The clock's pair of the pin world (the light-bending note's section 5 and
# the one-wall note's section 6: [1, 16384] in place of series K's 0).
SUSPENSION = [1, 16384]
# The mass sixteen times series K's SOURCE = 2^12: 2^16.
MASS_FACTOR = 16
GAMMAS = (0, 1)
NAMES = ("control", "mass", "near", "far")
# The pins from the lattice's lines (the one-wall note's section 6, DETECTOR
# if run; the bracket 0.5 pixel on the centroid's shift and 1 interval on
# the delay): per world the shift in pixels toward the mass (negative in y)
# and the delay in intervals at f = 1 and f = 2, and the lamp's clock rate
# under the age word (GAMEBOARD).
PINS: dict[str, dict[str, object]] = {
    "mass": {
        "mass": 1 << 16,
        "impact": 6,
        "shift": {1: -1.93, 2: -3.86},
        "delay": {1: 2.68, 2: 5.36},
        "lamp_rate": 0.918,
    },
    "near": {
        "mass": 1 << 16,
        "impact": 3,
        "shift": {1: -2.42, 2: -4.83},
        "delay": {1: 2.17, 2: 4.34},
        "lamp_rate": 1.000,
    },
    # The far world (records 505 and 540): b = 8, where no direction of the
    # beam is taken by the mass (the innermost line at 5.83 Links, beyond
    # mass's 3.83); the deflection's second pin, near at f = 2 being a
    # capture reading. Its lamp rate is read at its first run (None).
    "far": {
        "mass": 1 << 16,
        "impact": 8,
        "shift": {1: -1.69, 2: -3.37},
        "delay": {1: 2.15, 2: 4.29},
        "lamp_rate": None,
    },
}
SHIFT_BRACKET = 0.5
DELAY_BRACKET = 1.0
# The deciding worlds of every family under one wall (the chief physicist's
# design docs/designs/one_wall/EVERY_FAMILY.md section 2, the model owner's
# "build this with me" of 2026-09-22): series K's geometry at the pair, the
# mass a quarter of the light pin worlds' (M = 2^14, so that a slow row's
# turn stays below 0.3 radian), and in place of the light lamp a lamp of a
# massive family `matter` (quantum 1, massive, momentum_magnitude p = 10 at
# width 1: E'_0 = Q S M = 64, E' = isqrt(64^2 + 3 x 100) = 66, v^2 = 0.069,
# the dwell per Node 6.6 intervals) on the heading alone at b = 10, one row
# per interval from a reservoir of K units (the turn 1); the `matter2` worlds the equivalence
# (quantum 2, p = 20: E' = 132 exactly twice, the same pace and the same
# v^2, the content doubled); gamma 0 and 1 for `matter`, gamma 0 for
# `matter2`, each with its control (the lamp alone, the same family); 1000
# intervals, the window 500 to 1000 (a row takes about 343 intervals to the
# screen). The pins by the map docs/designs/one_wall/every_family_map.py
# (the row followed along its momentum on the light-bending map's lines,
# the weight (E'^2 + 3 gamma p . p) // E', the pace of the pair on P),
# before any run: the shift in pixels toward the mass and the arrival in
# intervals against the control.
MATTER_MASS_FACTOR = 4
MATTER_TICKS = 1000
MATTER_WINDOW_START = 500
MATTER_ACTION = 1024
# The largest age a massive row may carry (required with `massive_rows`: a
# row takes about 343 intervals to the screen at the pace 10 / 66).
MATTER_AGE_BOUND = 1024
# The lamp's reservoir: series K's K times the turn 1 (a massive birth
# needs the turn 1, the row's content quantum x 1; a reservoir below K
# turns 0 and births nothing), one unit of it per birth.
MATTER_RESERVOIR_TURN = 1
MATTER_FAMILIES: dict[str, dict[str, int]] = {
    "matter": {"quantum": 1, "momentum_magnitude": 10},
    "matter2": {"quantum": 2, "momentum_magnitude": 20},
}
MATTER_WORLDS: tuple[tuple[str, int], ...] = (("matter", 0), ("matter", 1), ("matter2", 0))
# The family's name in every deciding world is `matter` (the catalog's
# massive quantum, declared inline with its own quantum and momentum as
# series W declares it); `matter2` names the world, not a second family.
MATTER_FAMILY_NAME = "matter"
# The impact distance of the deciding worlds: b = 10 (the lamp at y = 30).
# The first run at b = 6 (2026-09-22, recorded in README.md) reached the
# mass's own line before the screen (a turn of 0.25 radian reaches the
# axis 21 Links past the mass; the shift -6.000 exactly, the width 0), the
# naive pin of the first map (the deflection times 26 Links, the unpushed
# dwell) refuted by the geometry; at b = 10 the row stays 4 Links off the
# axis at the screen.
MATTER_IMPACT = 10
# The pins by the map every_family_map.py, the row followed along its
# momentum on the crowd's lines: the shift in pixels toward the mass and
# the ARRIVAL against the control's in intervals, negative when earlier
# (a falling row speeds up, its pace |P| / E'(P) growing under the push,
# the speed-up of about -8 intervals larger than the wall's stretch).
MATTER_PINS: dict[tuple[str, int], dict[str, float]] = {
    ("matter", 0): {"angle": 0.242, "shift": -5.76, "arrival": -8.36},
    ("matter", 1): {"angle": 0.252, "shift": -6.11, "arrival": -7.42},
    ("matter2", 0): {"angle": 0.242, "shift": -5.76, "arrival": -8.36},
}
# The readings that refute (the map at gamma = 1 with one verb changed):
# the massive wall unstretched (f = 0 on the massive rows, verb 1 not on
# every family) puts the gamma 1 arrival at -11.03 intervals (the rule's
# -7.42, 3.6 intervals apart); the weight blind to the speed ((1 + gamma) E'
# in place of (E'^2 + 3 gamma p . p) // E', verb 2 light's alone) puts
# the gamma 1 shift at -10.45 pixels (the rule's -6.11, 4.3 pixels apart);
# the pace unpushed (no speed-up: the family's own p / E' on the Manhattan
# length walked, the y-Links paid at that pace) would put the gamma 0
# arrival at +43.99 (the rule's -8.36; the map's first form of this
# reading, +2.57 in the note before the run, left the y-Links unpaid and is
# superseded by the map as kept, `pace="unpushed"`).
MATTER_REFUTING: dict[str, float] = {
    "gamma_1_arrival_wall_unstretched": -11.03,
    "gamma_1_shift_weight_blind_to_speed": -10.45,
    "gamma_0_arrival_without_the_speed_up": 43.99,
}
# The ratios' bracket: 0.25 on mass and near as registered (by fiat; a
# registered pin moves on the model owner's word); on far the brackets
# propagated in quadrature from +-0.5 pixel and +-1 interval (the chief
# physicist, record 540): 0.66 on the shifts' ratio, 1.04 on the delays'.
RATIO_BRACKET = 0.25
RATIO_BRACKETS: dict[str, dict[str, float]] = {"far": {"shift": 0.66, "delay": 1.04}}
# The capture reading of near at f = 2 (DETECTOR, the mass's clicks; the two
# inner directions of the beam, two fifths of the 1455 rows): the centroid
# is the survivors' (the three outer lines at 3, 4.08 and 5.17 Links), so
# near_g1 carries no deflection pin; the old shift pin stays beside it as
# superseded (records 505 and 540).
CAPTURE_NEAR_G1: dict[str, object] = {
    "taken_by_the_mass": 582,
    "taken_bracket": 146,
    "reading": (
        "capture: the centroid is the survivors' (the three outer lines at 3, 4.08 and 5.17 "
        "Links); no deflection pin"
    ),
    "shift_pin_superseded": -4.83,
}


def _lensing():
    """Series K's generator, the one copy of the fan, the beam and the screen."""
    path = HERE.parent / "lensing" / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("lensing_make_worlds", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("lensing_make_worlds", module)
    spec.loader.exec_module(module)
    return module


K = _lensing()


def world(name: str, gamma: int) -> Json:
    """Series K's world of `name` at the pin world's pair, the mass sixteen
    times, under `optical: gamma`; the model id series K's (the readings
    tool tells the worlds apart by it and reads each against the control
    of its folder)."""
    document = K.world(name)
    document["suspension"] = list(SUSPENSION)
    document["optical"] = gamma
    for entry in document["measured"]:
        if entry["family"] == "m":
            entry["amount"] = entry["amount"] * MASS_FACTOR
    return families_by_definition(document, K.FAMILY_DEFINITIONS, K.DEFINITIONS_SOURCE)


# Every family under one wall (2026-09-22, branch optical-every-family, the
# composition of optical-v1 with the massive rows; the physics-rule
# reviewer's M1 on PR #743): the light worlds at gamma 1 re-read under the
# weight 221 (the one floor; the Bresenham entry's and the far entry's
# values beside as "was"; gamma 0 and the controls byte identical, far_g0
# not re-run) and the three deciding worlds at b = 10 against the matter
# block's pins (inside / outside as the README has them). DETECTOR unless
# marked.
RUN_2026_09_22_EVERY_FAMILY: dict[str, object] = {
    "branch": "optical-every-family",
    "after": "the composition of optical-v1 with the massive rows (EVERY_FAMILY.md), the weight per unit 221 on the photon at gamma 1",
    "read_by": "tools/lensing_readings.py --no-replay (DETECTOR; --window-start 500 on the matter worlds)",
    "worlds": {
        "mass_g1": {
            "shift": -3.989,
            "delay": 4.94,
            "clicks": 1395,
            "taken_by_the_mass": 0,
            "was": {"shift": -3.989, "delay": 5.10, "clicks": 1394, "taken_by_the_mass": 0},
        },
        "near_g1": {
            "shift": -6.412,
            "delay": 6.20,
            "clicks": 1452,
            "taken_by_the_mass": 0,
            "was": {"shift": -6.412, "delay": 6.20, "clicks": 1452, "taken_by_the_mass": 0},
        },
        "far_g1": {
            "shift": -3.403,
            "delay": 4.33,
            "clicks": 1344,
            "taken_by_the_mass": 0,
            "was": {"shift": -3.403, "delay": 4.35, "clicks": 1344, "taken_by_the_mass": 0},
        },
        "matter_g0": {
            "shift": -5.000,
            "arrival": -12.00,
            "clicks": 501,
            "shift_inside": False,
            "shift_outside_by": 0.26,
            "arrival_inside": False,
            "arrival_outside_by": 2.64,
            "was": None,
        },
        "matter_g1": {
            "shift": -6.000,
            "arrival": -6.00,
            "clicks": 501,
            "shift_inside": True,
            "arrival_inside": False,
            "arrival_outside_by": 0.42,
            "was": None,
        },
        "matter2_g0": {
            "shift": -5.000,
            "arrival": -12.00,
            "clicks": 501,
            "shift_inside": False,
            "shift_outside_by": 0.26,
            "arrival_inside": False,
            "arrival_outside_by": 2.64,
            "equivalence_on_matter_g0": True,
            "was": None,
        },
    },
    "ratios": {
        "mass": {
            "shift_f2_over_f1": 2.00,
            "delay_f2_over_f1": 1.67,
            "delay_outside_by": 0.08,
            "was": {"shift_f2_over_f1": 2.00, "delay_f2_over_f1": 1.73},
        },
        "near": {
            "shift_f2_over_f1": 2.46,
            "delay_f2_over_f1": 2.07,
            "was": {"shift_f2_over_f1": 2.46, "delay_f2_over_f1": 2.07},
        },
        "far": {
            "shift_f2_over_f1": 1.92,
            "delay_f2_over_f1": 1.69,
            "was": {"shift_f2_over_f1": 1.92, "delay_f2_over_f1": 1.70},
        },
    },
    "note": (
        "the weight 221 for 220 moves the mass delay by 0.16 interval and nothing at three "
        "decimals in the shifts: the mass delays' ratio 4.94 / 2.95 = 1.67 (was 1.73), outside "
        "2.00 +- 0.25 by 0.08 (was 0.02), the Bresenham entry's deciding reading moved by the "
        "one floor; the shifts' ratio 2.00 unchanged; far's delays' ratio 1.69 (was 1.70); the "
        "matter worlds read in whole pixels and whole y-Links on one line, the wall's factor "
        "on a massive row under that grain; no pin moved"
    ),
}


def worlds() -> dict[str, Json]:
    found = {f"{name}_g{gamma}": world(name, gamma) for gamma in GAMMAS for name in NAMES}
    for family, gamma in MATTER_WORLDS:
        found[f"{family}_control_g{gamma}"] = matter_world("control", family, gamma)
        found[f"{family}_g{gamma}"] = matter_world("mass", family, gamma)
    return found


def matter_world(name: str, family: str, gamma: int) -> Json:
    """Series K's `mass` or `control` at the pin world's pair with the mass
    a quarter of the light worlds' (M = 2^14), the light lamp replaced by a
    lamp of the massive family (quantum, momentum_magnitude as
    `MATTER_FAMILIES`; the reservoir K in `amount`, the turn 1, one row per
    interval on the heading), the screen's entry reading the family's
    age, the two keys `optical` and `massive_rows` together; the model id
    series K's, so that the readings tool reads each against the control
    of its folder."""
    keys = MATTER_FAMILIES[family]
    document = K.world(name)
    document["suspension"] = list(SUSPENSION)
    document["optical"] = gamma
    document["ticks"] = MATTER_TICKS
    document["massive_rows"] = True
    document["action"] = MATTER_ACTION
    document["age_bound"] = MATTER_AGE_BOUND
    families = [{"name": MATTER_FAMILY_NAME, "quantum": keys["quantum"], "massive": True}]
    families.extend(document["families"])  # type: ignore[arg-type]
    document["families"] = families
    centre = K.CENTRE
    for entry in document["measured"]:
        if entry["family"] == "m":
            entry["amount"] = entry["amount"] * MATTER_MASS_FACTOR
        elif "lamp" in entry:
            entry["family"] = MATTER_FAMILY_NAME
            entry["position"] = [K.LAMP_X, centre[1] + MATTER_IMPACT, centre[2]]
            entry["amount"] = K.K * MATTER_RESERVOIR_TURN  # the reservoir K x 1: the turn 1
            entry["lamp"] = {
                "rate": [1, 1],
                "wheel": [1, K.N],
                "directions": [[1, 0, 0]],
                "momentum_magnitude": keys["momentum_magnitude"],
            }
        elif entry["family"] == "wall":
            entry["table"] = {MATTER_FAMILY_NAME: {"rule": "measure", "reads": "age"}, "m": "pass"}
    return families_by_definition(document, K.FAMILY_DEFINITIONS, K.DEFINITIONS_SOURCE)


def expectations() -> Json:
    out: Json = {
        "format": EXPECTATIONS_FORMAT,
        "derivation": (
            "docs/designs/one_wall/NOTE.md section 6 and docs/designs/open_problems/light_bending/"
            "NOTE.md section 5 (the pins from the lattice's lines, before any run): k(b) the age "
            "moment of the crowd's rows at the beam's Node per interval of dwell, k = A n / d; the "
            "deflection the sum over the row's dwell of the transverse flow's turn at the weight "
            "(1 + gamma) content x e_D (verb 2, REVIEW_3 must-fix 1: e_D, never T_D), the "
            "centroid's shift the deflection times the 26 Links to the screen; the delay the sum of "
            "f n A / d over the dwell (verb 1, the flight's wall 2 T_D (d + f n A)); f = 1 + gamma"
        ),
        "suspension": list(SUSPENSION),
        "mass_factor": MASS_FACTOR,
        "ticks": K.TICKS,
        "gammas": list(GAMMAS),
        "brackets": {
            "shift_pixels": SHIFT_BRACKET,
            "delay_intervals": DELAY_BRACKET,
            "ratio": RATIO_BRACKET,
        },
        "worlds": {},
        "ratios": {},
        "derivations": {
            "shift": (
                "DETECTOR: the centroid of the screen's clicks in pixels against the control's, "
                "negative toward the mass (tools/lensing_readings.py, the late window); the "
                "continuum's (1 + gamma) 2 G M / (b c^2) on the lattice's lines"
            ),
            "delay": (
                "DETECTOR: the mean age of the arrivals at the screen against the control's "
                "(the click records carry the age moment, reads: age): Shapiro's delay, the "
                "sum of f n A / d over the row's dwell"
            ),
            "ratio_f2_over_f1": (
                "the ratio of the centroid's shift at gamma = 1 over gamma = 0: 2.00, the space "
                "part gamma doubling the time part's turn (the number the run reads); the bracket "
                "0.25 on mass and near as registered (the 0.25 was by fiat; the bracket propagated "
                "in quadrature from +-0.5 pixel and +-1 interval is 0.83 on the delays' ratio at "
                "b = 6; the chief physicist, record 540), on far the propagated brackets, 0.66 on "
                "the shifts' ratio (`bracket`) and 1.04 on the delays' (`delay_bracket`)"
            ),
            "lamp_rate": (
                "GAMEBOARD: the lamp's clock rate under the age word, its births per interval "
                "(clock-age-v1, the law's default; not the key's); far's is None until its first "
                "run reads it"
            ),
            "capture": (
                "DETECTOR: the mass's clicks at near, f = 2 (taken_by_the_mass 582 +- 146, the two "
                "inner directions of the beam at 0.83 and 1.92 Links, two fifths of 1455): a capture "
                "reading, the centroid the survivors' (the three outer lines at 3, 4.08 and 5.17 "
                "Links), so near_g1 carries no deflection pin and the old shift pin stays as "
                "shift_pin_superseded; the deflection's second pin is far (b = 8, no direction "
                "taken, the innermost at 5.83 Links beyond mass's 3.83); the source: the note's "
                "map, section E, the one-line form, GAMEBOARD arithmetic, the chief physicist's "
                "record 540 (records 505 and 540)"
            ),
        },
    }
    for gamma in GAMMAS:
        f = 1 + gamma
        out["worlds"][f"control_g{gamma}"] = {
            "gamma": gamma,
            "flight_coefficient": f,
            "mass": None,
            "shift": 0.0,
            "delay": 0.0,
        }
        for name, pin in PINS.items():
            entry: Json = {
                "gamma": gamma,
                "flight_coefficient": f,
                "mass": pin["mass"],
                "impact": pin["impact"],
                "shift": pin["shift"][f],
                "shift_bracket": SHIFT_BRACKET,
                "delay": pin["delay"][f],
                "delay_bracket": DELAY_BRACKET,
                "lamp_rate": pin["lamp_rate"],
            }
            if name == "near" and gamma == 1:
                # The capture reading in place of the deflection pin.
                del entry["shift"], entry["shift_bracket"]
                entry.update(CAPTURE_NEAR_G1)
            out["worlds"][f"{name}_g{gamma}"] = entry
    out["run_2026_09_21"] = RUN_2026_09_21
    out["run_2026_09_21_m1"] = RUN_2026_09_21_M1
    out["run_2026_09_22_bresenham"] = RUN_2026_09_22_BRESENHAM
    out["run_2026_09_22_far"] = RUN_2026_09_22_FAR
    out["run_2026_09_22_every_family"] = RUN_2026_09_22_EVERY_FAMILY
    for name, pin in PINS.items():
        ratios: Json = {
            "shift_f2_over_f1": pin["shift"][2] / pin["shift"][1],
            "delay_f2_over_f1": pin["delay"][2] / pin["delay"][1],
            "expected": 2.0,
            "bracket": RATIO_BRACKET,
        }
        if name in RATIO_BRACKETS:
            ratios["bracket"] = RATIO_BRACKETS[name]["shift"]
            ratios["delay_bracket"] = RATIO_BRACKETS[name]["delay"]
        out["ratios"][name] = ratios
    out["matter"] = {
        "derivation": (
            "docs/designs/one_wall/EVERY_FAMILY.md section 2 and its map every_family_map.py "
            "(the light-bending map's crowd lines, the row followed along its own momentum, "
            "verbs 1 and 2 together: the dwell on the pushed pair's wall over its rate, the push "
            "at the weight (E'^2 + 3 gamma p . p) // E' per unit of amount, before any run): "
            "the deciding world of every family under one wall, the mass 2^14, the pair "
            "[1, 16384], one massive row per interval on the heading at b = 10; the arrival "
            "carries the wall's stretch and the speed-up of a falling row (the pace |P| / E'(P) "
            "grows under the push), so the pin is the map's arrival per world and the readings "
            "that refute are the map's with one verb changed"
        ),
        "mass": (1 << 12) * MATTER_MASS_FACTOR,
        "impact": MATTER_IMPACT,
        "ticks": MATTER_TICKS,
        "window_start": MATTER_WINDOW_START,
        "families": MATTER_FAMILIES,
        "worlds": {
            f"{family}_g{gamma}": {
                "gamma": gamma,
                "flight_coefficient": 1 + gamma,
                "family": MATTER_FAMILY_NAME,
                "quantum": MATTER_FAMILIES[family]["quantum"],
                "momentum_magnitude": MATTER_FAMILIES[family]["momentum_magnitude"],
                "angle_radians": pin["angle"],
                "shift": pin["shift"],
                "shift_bracket": SHIFT_BRACKET,
                "arrival": pin["arrival"],
                "arrival_bracket": DELAY_BRACKET,
                "control": f"{family}_control_g{gamma}",
            }
            for (family, gamma), pin in MATTER_PINS.items()
        },
        "refuting_readings": MATTER_REFUTING,
        "equivalence": (
            "matter2_g0 (quantum 2, p = 20, E' = 132) on matter_g0's shift within 0.5 pixel and "
            "its arrival within 1 interval, each against its own control: the same fall at twice "
            "the content (the pace and v^2 equal to the integer, the push twice on twice the "
            "momentum; GAMEBOARD arithmetic of the declaration)"
        ),
        "readings": (
            "DETECTOR: the screen's click lines of the massive family (each click's Node and its "
            "age moment, `reads: age`), the centroid's shift and the mean age's arrival against "
            "the control in the late window; no store, no replay"
        ),
    }
    return out


# The run of 2026-09-21 on branch optical-v1 (the README's measured section;
# DETECTOR unless marked), typed from the readings tools, the register's
# convention for a run block: the centroid's shift in pixels and the delay
# in intervals against the control, and the chief physicist's reading of
# record 483 (the rule and the pins unchanged).
RUN_2026_09_21: dict[str, object] = {
    "branch": "optical-v1",
    "read_by": "tools/lensing_readings.py --no-replay (DETECTOR); tools/optical_readings.py (GAMEBOARD)",
    "worlds": {
        "mass_g0": {"shift": -1.607, "delay": 2.89, "clicks": 1396, "taken_by_the_mass": 0},
        "mass_g1": {"shift": -3.812, "delay": 5.87, "clicks": 1385, "taken_by_the_mass": 0},
        "near_g0": {"shift": -2.992, "delay": 2.40, "clicks": 1456, "taken_by_the_mass": 0},
        "near_g1": {"shift": -4.654, "delay": 4.97, "clicks": 1122, "taken_by_the_mass": 398},
    },
    "ratios": {
        "mass": {"shift_f2_over_f1": 2.37, "delay_f2_over_f1": 2.03},
        "near": {"shift_f2_over_f1": 1.56, "delay_f2_over_f1": 2.07},
    },
    "gameboard_mean_transverse_angle_degrees": {
        "mass_g0": -4.181,
        "mass_g1": -8.680,
        "near_g0": -6.854,
        "near_g1": -11.955,
    },
    "note": (
        "the chief physicist's reading (record 483): the wall's factor read as Shapiro's (the "
        "delays' ratios inside 2.00 +- 0.25); the shifts inside 0.5 pixel in three of four, near "
        "at f = 1 missed by 0.07 by the beam's width at b = 3 (the pin one line); the shifts' ratio "
        "not read at this fan (the teeth 2.39 / 4.76 / 11.31 degrees, the bisectors 3.58 / 8.04; the "
        "ratio's bracket 0.25 not derivable from the shifts' 0.5 pixel, the propagated 0.58 / 0.46, "
        "a fact of the pin as written, which stays and is refuted at 0.25); the near f = 2 shift a "
        "survivors' reading (398 taken); verb 3's form the model owner's decision on his return"
    ),
}

# The re-read of 2026-09-21 on the head that carries M1 of the physics-rule
# review of 408cf719 (record 494: the walk's count capped by the primitive
# with the surplus kept, the residue rescaled at a turn as the time of the
# last Link, s' = (s x S_new) // S_old, the chief physicist's word of record
# 496); the first run's value beside each as "was"; DETECTOR unless marked.
RUN_2026_09_21_M1: dict[str, object] = {
    "branch": "optical-v1",
    "after": "M1 of docs/designs/optical_v1/REVIEW_408CF719.md (records 494 and 496)",
    "read_by": "tools/lensing_readings.py --no-replay (DETECTOR); tools/optical_readings.py (GAMEBOARD)",
    "worlds": {
        "mass_g0": {
            "shift": -1.622,
            "delay": 2.97,
            "clicks": 1398,
            "taken_by_the_mass": 0,
            "was": {"shift": -1.607, "delay": 2.89, "clicks": 1396, "taken_by_the_mass": 0},
        },
        "mass_g1": {
            "shift": -3.805,
            "delay": 5.88,
            "clicks": 1389,
            "taken_by_the_mass": 0,
            "was": {"shift": -3.812, "delay": 5.87, "clicks": 1385, "taken_by_the_mass": 0},
        },
        "near_g0": {
            "shift": -3.000,
            "delay": 2.40,
            "clicks": 1455,
            "taken_by_the_mass": 0,
            "was": {"shift": -2.992, "delay": 2.40, "clicks": 1456, "taken_by_the_mass": 0},
        },
        "near_g1": {
            "shift": -3.274,
            "delay": 4.51,
            "clicks": 1001,
            "taken_by_the_mass": 547,
            "was": {"shift": -4.654, "delay": 4.97, "clicks": 1122, "taken_by_the_mass": 398},
        },
    },
    "ratios": {
        "mass": {
            "shift_f2_over_f1": 2.35,
            "delay_f2_over_f1": 1.98,
            "was": {"shift_f2_over_f1": 2.37, "delay_f2_over_f1": 2.03},
        },
        "near": {
            "shift_f2_over_f1": 1.09,
            "delay_f2_over_f1": 1.88,
            "was": {"shift_f2_over_f1": 1.56, "delay_f2_over_f1": 2.07},
        },
    },
    "gameboard_mean_transverse_angle_degrees": {
        "mass_g0": -4.203,
        "mass_g1": -8.976,
        "near_g0": -6.993,
        "near_g1": -8.277,
        "was": {"mass_g0": -4.181, "mass_g1": -8.680, "near_g0": -6.854, "near_g1": -11.955},
    },
    "note": (
        "the controls byte identical to the first run; the delays' ratios inside 2.00 +- 0.25 as "
        "before; the shifts inside 0.5 pixel in two of four (three before M1): near at f = 2 now "
        "outside by 1.06, a survivors' reading with 547 taken; the shifts' ratio outside as before; "
        "the rule and the pins unchanged"
    ),
}


# The re-read of 2026-09-22 on branch optical-v1-bresenham (the model
# owner's GO of record 536: verb 3's label by Bresenham along the line of
# P; the chief physicist's DERIVED word: a pushed row's pace is its
# momentum's); the M1 re-read's value beside each as "was"; DETECTOR
# unless marked.
RUN_2026_09_22_BRESENHAM: dict[str, object] = {
    "branch": "optical-v1-bresenham",
    "after": "record 536 (verb 3 by Bresenham) and the chief physicist's word on the pace",
    "read_by": "tools/lensing_readings.py --no-replay (DETECTOR); tools/optical_readings.py (GAMEBOARD)",
    "worlds": {
        "mass_g0": {
            "shift": -1.993,
            "delay": 2.95,
            "clicks": 1347,
            "taken_by_the_mass": 0,
            "was": {"shift": -1.622, "delay": 2.97, "clicks": 1398, "taken_by_the_mass": 0},
        },
        "mass_g1": {
            "shift": -3.989,
            "delay": 5.10,
            "clicks": 1394,
            "taken_by_the_mass": 0,
            "was": {"shift": -3.805, "delay": 5.88, "clicks": 1389, "taken_by_the_mass": 0},
        },
        "near_g0": {
            "shift": -2.608,
            "delay": 2.99,
            "clicks": 1453,
            "taken_by_the_mass": 0,
            "was": {"shift": -3.000, "delay": 2.40, "clicks": 1455, "taken_by_the_mass": 0},
        },
        "near_g1": {
            "shift": -6.412,
            "delay": 6.20,
            "clicks": 1452,
            "taken_by_the_mass": 0,
            "was": {"shift": -3.274, "delay": 4.51, "clicks": 1001, "taken_by_the_mass": 547},
        },
    },
    "ratios": {
        "mass": {
            "shift_f2_over_f1": 2.00,
            "delay_f2_over_f1": 1.73,
            "was": {"shift_f2_over_f1": 2.35, "delay_f2_over_f1": 1.98},
        },
        "near": {
            "shift_f2_over_f1": 2.46,
            "delay_f2_over_f1": 2.07,
            "was": {"shift_f2_over_f1": 1.09, "delay_f2_over_f1": 1.88},
        },
    },
    "gameboard_mean_transverse_angle_degrees": {
        "mass_g0": -4.225,
        "mass_g1": -9.097,
        "near_g0": -6.812,
        "near_g1": -14.478,
        "was": {"mass_g0": -4.203, "mass_g1": -8.976, "near_g0": -6.993, "near_g1": -8.277},
    },
    "note": (
        "the controls byte identical; the law's 2.00 read in the mass world's shifts (the comb "
        "gone); the mass delays inside their pins, their ratio 1.73 outside 2.00 +- 0.25 by 0.02, "
        "the reading that decides, recorded as it is; near at f = 2 the whole beam (0 taken), "
        "outside its shift and delay pins; the rule and the pins unchanged"
    ),
}


# The far worlds' first run, on branch optical-v1-bresenham (records 505
# and 540; verb 3 by Bresenham with the momentum's pace, 32358f3): the
# deflection's second pin at b = 8, run for the first time, so "was" is
# None for both. DETECTOR unless marked; the lamp rate GAMEBOARD, read
# here (the pin left None until the first run).
RUN_2026_09_22_FAR: dict[str, object] = {
    "branch": "optical-v1-bresenham",
    "after": "the merge of main's far worlds (PR #689) onto verb 3's Bresenham form with the momentum's pace",
    "read_by": "tools/lensing_readings.py --no-replay (DETECTOR); tools/optical_readings.py (GAMEBOARD)",
    "worlds": {
        "far_g0": {
            "shift": -1.773,
            "delay": 2.56,
            "clicks": 1348,
            "taken_by_the_mass": 0,
            "lamp_rate": 0.927,
            "was": None,
        },
        "far_g1": {
            "shift": -3.403,
            "delay": 4.35,
            "clicks": 1344,
            "taken_by_the_mass": 0,
            "lamp_rate": 0.927,
            "was": None,
        },
    },
    "ratios": {
        "far": {
            "shift_f2_over_f1": 1.92,
            "shift_bracket": 0.66,
            "delay_f2_over_f1": 1.70,
            "delay_bracket": 1.04,
            "was": None,
        },
    },
    "gameboard_mean_transverse_angle_degrees": {
        "far_g0": -3.855,
        "far_g1": -7.788,
        "ratio": 2.020,
        "was": None,
    },
    "note": (
        "the far worlds' first run: both shifts inside 0.5 pixel of the pins -1.69 / -3.37 (read "
        "-1.773 / -3.403) and both delays inside 1 interval of 2.15 / 4.29 (read 2.56 / 4.35); the "
        "shifts' ratio 1.92 inside 2.00 +- 0.66 and the delays' 1.70 inside 2.00 +- 1.04; no light "
        "taken by the mass at either f (the innermost line at 5.83 Links, beyond mass's 3.83); the "
        "lamp rate 0.927 read here (the pin was None); the pins untouched"
    ),
}


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    expected = carry_replicated(HERE / "expectations.json", expectations())
    (HERE / "expectations.json").write_text(json.dumps(expected, indent=1) + "\n", encoding="utf-8")
    for name, entry in expected["worlds"].items():
        print(name, json.dumps({k: v for k, v in entry.items() if k in ("gamma", "shift", "delay")}))


if __name__ == "__main__":
    main()
