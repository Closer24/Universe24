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
    PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/optical_g0 examples/events/optical/control_g0.json examples/events/optical/mass_g0.json examples/events/optical/near_g0.json
    PYTHONPATH=src python tools/run_series.py --jobs 2 --out artifacts/optical_g1 examples/events/optical/control_g1.json examples/events/optical/mass_g1.json examples/events/optical/near_g1.json
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
NAMES = ("control", "mass", "near")
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
}
SHIFT_BRACKET = 0.5
DELAY_BRACKET = 1.0
RATIO_BRACKET = 0.25


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


def worlds() -> dict[str, Json]:
    return {f"{name}_g{gamma}": world(name, gamma) for gamma in GAMMAS for name in NAMES}


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
                "part gamma doubling the time part's turn (the number the run reads)"
            ),
            "lamp_rate": (
                "GAMEBOARD: the lamp's clock rate under the age word, its births per interval "
                "(clock-age-v1, the law's default; not the key's)"
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
            out["worlds"][f"{name}_g{gamma}"] = {
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
    out["run_2026_09_21"] = RUN_2026_09_21
    out["run_2026_09_21_m1"] = RUN_2026_09_21_M1
    out["run_2026_09_22_bresenham"] = RUN_2026_09_22_BRESENHAM
    for name, pin in PINS.items():
        out["ratios"][name] = {
            "shift_f2_over_f1": pin["shift"][2] / pin["shift"][1],
            "delay_f2_over_f1": pin["delay"][2] / pin["delay"][1],
            "expected": 2.0,
            "bracket": RATIO_BRACKET,
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
