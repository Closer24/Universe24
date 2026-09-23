"""Write the three worlds of Side A of Newton on the side (the model
owner's word, records 1043, 1046 and 1098 of docs/LOG_2026-09-20.md; the
design docs/designs/newton_clicks/NEWTON_ON_THE_SIDE.md sections 3 and 4,
on main at da86e383; the run's chain and its pins restated in
docs/designs/fail_rows/RUN_14.md): the moving detector WITH MASS, a
massive row released at rest past a held mass and read at a receiver
body under `clock_stamp`, on the exact rung k = 19 of the ladder of
velocities, and its control; beside them the light row of the same
world, whose lever-arm centroid is the reading that separates the click
count's term from the ring mean alone.

Series K's geometry (`../lensing/make_worlds.py`): an open box of SHAPE
Nodes, the held mass at CENTRE, the lamp A at x = LAMP_X and y = centre +
IMPACT (b = 6 above the axis), the receiver plane at x = SCREEN_X (L = 26
Links from the mass's plane on either side, 52 Links from the lamp). What
differs from series K, and nothing else, every number the design's
section 4.3:

- The lamp's family is the massive family `matter` (M_row = 21 units per
  row, the family flag `massive`, a phase circle, no `phase_per_link`)
  under the world keys `massive_rows`, `width` 1, `action` 1024 and
  `age_bound` 2048; the lamp's label magnitude p = 71 (`momentum_magnitude`),
  so that E'_0 = Q S M_row = 1344 and E'_D = isqrt(1344^2 + 3 x 71^2) =
  1349 = 19 x 71 exactly: the row makes one Link per 19 counts with no
  remainder (the rung k = 19). The lamp's content is the world's K, so
  that its turn is exactly 1 at the first birth (a massive birth needs
  the turn 1); it releases one row per self-creation on the one heading
  toward the plane (`directions` [[1, 0, 0]]) at the wheel [2531, 4096]
  of the massive register's pin world.
- The pair `suspension` [1, 4096] (the wall and the push act on nothing
  at [0, d]); `optical` 1 declared (c_f = 1 + gamma_PPN = 2), never a
  default; `flow_link` stated false as series K has it; `clock_stamp`
  true, the click instrument: every line a receiver writes carries its
  own count.
- The receivers are bodies: 1681 fixed measured events of the paid
  family `wall` on the plane x = SCREEN_X, each measuring `matter` and
  passing the mass's rays; no `detectors` list (a detector set without a
  body has no count, record 768; the screen's pixels are bodies here and
  not series K's `wave` sets), so the click line carries the receiver's
  number, its Node, its own count `clock` and the row's ordinal
  (`record` mod 2^32). The one declaration that departs from the
  design's section 4.3, found by the algebra of the steps before the run
  (RUN_14.md step 5 and section 4): the entry reads the PRESENCE
  (`reads: "presence"`) and not the row's age. A measured event's clock
  counts the age moment of the other numbers' rows at its Node on every
  entry unless the entry reads `presence` (clock-age-v1,
  `measured.count_component`), and the arriving row IS such a row at the
  receiver's Node for the interval it ends there: under `reads: "age"`
  every click would stretch the receiver's own count by the row's age
  over d, 979 / 4096 = 0.239 of a count per click, so n_B less the
  ordinal would fall by one every four clicks and no click of the
  control could read 979 (read on a bar of six Links in the tool's test:
  the count one behind the tick from the 41st click at 105 / 4096 per
  click). Under `presence` the stretch per click is 1 / 4096 (0.1 of a
  count over the window of 400 clicks) and the pins of section 4.1
  stand; the row's age is then not on the click line and is in no pin
  (the arrival count is the receiver's count less the row's ordinal, the
  design's reading).
- The held mass: a fixed measured event of the free, phase-less family
  `m` at CENTRE, content 2^10 in the massive worlds (one row per direction
  per four self-creations under the release [1, 4096]) releasing on
  series E's fan of 290 directions; absent in the control.

| World | The lamp's family | The mass | What it asks |
| --- | --- | --- | --- |
| `control` | `matter` (M_row 21, p 71) | none | the rung: the arrival count 979 on every click, the arrival Node the line's end |
| `mass` | the same | 2^10 | Newton's advance (40.5 counts early) and Newton's bending (4.39 pixels) |
| `light` | `light` (series K's photon; no `massive`, no `momentum_magnitude`) | 2^16 (the gr_rows pin world's) | the lever-arm centroid, -4.63 pixels under the arrivals count against -5.47 under the crossing count: the deciding pin |

The run's length TICKS: the control's arrival at 979 counts and a window
of about 400 clicks after it (one row per interval); the light row's
window opens at its own arrival (89 counts on the heading). The pins are
in `expectations.json` beside the worlds and in RUN_14.md, written before
any run; the reading tool is `tools/newton_side_readings.py`.

    PYTHONPATH=src python examples/events/newton_side/make_worlds.py
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

from event_universe.world_loading import families_by_definition  # noqa: E402


def load_lensing_generator():
    """Series K's generator beside `lensing/`: the box, the fan and the
    definitions the families come from (one canonical copy of each)."""
    path = HERE.parent / "lensing" / "make_worlds.py"
    spec = importlib.util.spec_from_file_location("lensing_make_worlds_newton_side", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules["lensing_make_worlds_newton_side"] = module
    spec.loader.exec_module(module)
    return module


LENSING = load_lensing_generator()
FAMILY_DEFINITIONS = LENSING.FAMILY_DEFINITIONS
DEFINITIONS_SOURCE = LENSING.DEFINITIONS_SOURCE
SHAPE = LENSING.SHAPE
CENTRE = LENSING.CENTRE
LAMP_X = LENSING.LAMP_X
SCREEN_X = LENSING.SCREEN_X
FAN = LENSING.FAN
HEADINGS = LENSING.HEADINGS
K = LENSING.K
N = LENSING.N
IMPACT = 6
# The geometry the pins are written in: L Links from the mass's plane to
# the receivers (r_1 = r_2 = L), L_LINE Links from the lamp to the plane.
L = SCREEN_X - CENTRE[0]
L_LINE = SCREEN_X - LAMP_X
# The massive family on the rung k = 19 (the design's section 3 (b)):
# Q = 64, S = 1, M_row = 21, p = 71; E'_0 = 1344, E'_D = 1349 = 19 x 71.
LABEL_SCALE = 64
WIDTH = 1
ACTION = 1024
AGE_BOUND = 2048
MASSIVE_FAMILY = "matter"
LIGHT_FAMILY = "light"
WALL_FAMILY = "wall"
MASS_FAMILY = "m"
M_ROW = 21
MOMENTUM_MAGNITUDE = 71
RUNG = 19
REST_ENERGY = LABEL_SCALE * WIDTH * M_ROW
PACE_WALL = math.isqrt(REST_ENERGY * REST_ENERGY + 3 * MOMENTUM_MAGNITUDE * MOMENTUM_MAGNITUDE)
assert PACE_WALL == RUNG * MOMENTUM_MAGNITUDE == 1349, PACE_WALL
# The lamp: one row per self-creation on the heading toward the plane,
# the wheel of the massive register's pin world, the content K (the turn 1).
HEADING = [1, 0, 0]
WHEEL = [2531, 4096]
LAMP_RATE = [1, 1]
# The pair and the declarations of the design's section 4.3.
SUSPENSION = [1, 4096]
OPTICAL = 1
FLOW_LINK = False
RELEASE = [1, 4096]
# The receivers' entry for the lamp's family reads the presence (the module
# docstring: the design's `age` would stretch the receiver's own count by
# every arriving row's age over d).
RECEIVER_READS = "presence"
# The held mass: 2^10 in the massive worlds (k_a(b) = 6.95 x 10^-4 by the
# linear scaling of the gr_rows pin world's 0.0445 at 2^16), 2^16 in the
# light-row world (the pin world's own, the lever-arm pin's k_a(b)).
MASS_MASSIVE = 1 << 10
MASS_LIGHT = 1 << 16
# The control's arrival count on the rung: the least age tau with
# floor((2 tau p + E'_D) / (2 E'_D)) >= L_LINE, 19 x 52 - 9 = 979; the
# window of the reading opens after it and holds about 400 clicks.
ARRIVAL_CONTROL = RUNG * L_LINE - (RUNG - 1) // 2
assert ARRIVAL_CONTROL == 979
WINDOW_AFTER_ARRIVAL = 21
WINDOW_CLICKS = 400
TICKS = ARRIVAL_CONTROL + WINDOW_AFTER_ARRIVAL + WINDOW_CLICKS
MODEL_PREFIX = "beam-newton-side-"
MODEL_SUFFIX = "-v1"
WORLDS: dict[str, dict[str, object]] = {
    "control": {"family": MASSIVE_FAMILY, "mass": None},
    "mass": {"family": MASSIVE_FAMILY, "mass": MASS_MASSIVE},
    "light": {"family": LIGHT_FAMILY, "mass": MASS_LIGHT},
}
Json = dict[str, object]
# The world's declared directions: the fan's non-headings (the lamp's one
# direction is a heading and needs no declaration).
DECLARED = [v for v in FAN if tuple(v) not in HEADINGS]


def arrival_count(links: int, rate: int = 2 * MOMENTUM_MAGNITUDE, wall: int = 2 * PACE_WALL) -> int:
    """The flight's first age at `links` Links: the least tau with
    floor((tau x rate + wall / 2) / wall) >= links (the massive triple, the
    half-wall start), a COMPUTATION of the design's section 4.1."""
    tau = 0
    while (tau * rate + wall // 2) // wall < links:
        tau += 1
    return tau


def world(name: str) -> Json:
    keys = WORLDS[name]
    family = str(keys["family"])
    mass = keys["mass"]
    lamp: Json = {
        "position": [LAMP_X, CENTRE[1] + IMPACT, CENTRE[2]],
        "family": family,
        "amount": K,
        "phase": 0,
        "fixed": True,
        "lamp": {
            "rate": list(LAMP_RATE),
            "wheel": list(WHEEL),
            "directions": [list(HEADING)],
            **({"momentum_magnitude": MOMENTUM_MAGNITUDE} if family == MASSIVE_FAMILY else {}),
        },
        "table": {MASS_FAMILY: "pass"},
    }
    measured: list[Json] = [lamp]
    if mass is not None:
        measured.append(
            {
                "position": list(CENTRE),
                "family": MASS_FAMILY,
                "amount": int(mass),
                "phase": 0,
                "fixed": True,
                "directions": [list(v) for v in FAN],
            }
        )
    for y in range(SHAPE[1]):
        for z in range(SHAPE[2]):
            measured.append(
                {
                    "position": [SCREEN_X, y, z],
                    "family": WALL_FAMILY,
                    "amount": 1,
                    "fixed": True,
                    "table": {
                        family: {"rule": "measure", "reads": RECEIVER_READS},
                        MASS_FAMILY: "pass",
                    },
                }
            )
    lamp_family: Json = (
        {"name": MASSIVE_FAMILY, "quantum": M_ROW, "massive": True}
        if family == MASSIVE_FAMILY
        else {"name": LIGHT_FAMILY, "quantum": 1}
    )
    return {
        "law": "beam",
        "model_id": f"{MODEL_PREFIX}{name}{MODEL_SUFFIX}",
        "shape": list(SHAPE),
        "boundary": "open",
        "ticks": TICKS,
        "K": K,
        "N": N,
        "release": list(RELEASE),
        "suspension": list(SUSPENSION),
        "width": WIDTH,
        "action": ACTION,
        "age_bound": AGE_BOUND,
        "massive_rows": True,
        "optical": OPTICAL,
        "flow_link": FLOW_LINK,
        "clock_stamp": True,
        "directions": [list(v) for v in DECLARED],
        "families": [
            lamp_family,
            {"name": WALL_FAMILY, "quantum": 1},
            {"name": MASS_FAMILY, "quantum": 0, "charge": 0, "phase": False},
        ],
        "measured": measured,
    }


def worlds() -> dict[str, Json]:
    """The three shipped worlds as the loader writes them (the families
    from `../entities/families.json` where they equal its definitions)."""
    return {
        name: families_by_definition(world(name), FAMILY_DEFINITIONS, DEFINITIONS_SOURCE)
        for name in WORLDS
    }


# The pins of the design's section 4.1 (RUN_14.md section 2), every number
# COMPUTATION before the run; the conditional ones hang on the one click
# reading k_a(b), taken here by the linear scaling of the gr_rows pin
# world's 0.0445 at 2^16 (a GAMEBOARD age moment until the lamp at b reads
# it).
K_A_LIGHT = 0.0445
K_A_MASSIVE = K_A_LIGHT * MASS_MASSIVE / MASS_LIGHT
LIGHT_PACE = 1.0 / math.sqrt(3.0)
LIGHT_PACE_HEADING = 32.0 / 55.0
GAMMA_PPN = OPTICAL
FLIGHT_COEFFICIENT = 1 + GAMMA_PPN
CENTROID_BRACKET = 0.5
ADVANCE_MARGIN = 0.08
LIGHT_DELAY_BRACKET = 1.0
COUNT_RATIO_BRACKET = 0.01
EXPECTATIONS_FORMAT = "newton-side-expectations-v1"


def logarithm() -> float:
    """ln(4 r_1 r_2 / b^2) at r_1 = r_2 = L, b = IMPACT: 4.319."""
    return math.log(4.0 * L * L / (IMPACT * IMPACT))


def massive_pins() -> dict[str, float]:
    """The massive row's advance and bending (NEWTON_FROM_CLICKS 3 (b) to
    (d) at the rung's pace v = p / E'_D)."""
    v = MOMENTUM_MAGNITUDE / PACE_WALL
    beta_squared = (v / LIGHT_PACE) ** 2
    wall_delay = FLIGHT_COEFFICIENT * IMPACT * K_A_MASSIVE / v * logarithm()
    push_advance = (
        (1.0 - beta_squared)
        * (1.0 + GAMMA_PPN * beta_squared)
        * IMPACT
        * K_A_MASSIVE
        / v
        / beta_squared
        * logarithm()
    )
    alpha = 2.0 * K_A_MASSIVE / beta_squared * (1.0 + GAMMA_PPN * beta_squared)
    lever = alpha * (math.pi * IMPACT / 4.0) * (v / LIGHT_PACE)
    return {
        "pace": v,
        "u_over_c": v / LIGHT_PACE,
        "wall_delay": wall_delay,
        "push_advance": -push_advance,
        "net": wall_delay - push_advance,
        "alpha": alpha,
        "centroid_toward_mass": alpha * L,
        "centroid_toward_mass_crossing": alpha * L + lever,
        "clocks_rate": clocks_rate(K_A_MASSIVE),
        "clocks_shift": (clocks_rate(K_A_MASSIVE) - 1.0) * (ARRIVAL_CONTROL + wall_delay - push_advance),
        "advance_over_own_wall_delay": (1.0 - beta_squared)
        * (1.0 + GAMMA_PPN * beta_squared)
        / beta_squared
        / FLIGHT_COEFFICIENT,
    }


def clocks_rate(k_a: float) -> float:
    """The rate of the two clocks at the ends against the tick: the lamp
    and the receivers both sit at sqrt(L^2 + b^2) = 26.7 Links from the held
    mass, where the crowd's stretch is k = k_a(b) b / r per interval, so
    each counts 1 / (1 + k) of the tick (0.990 at 2^16, 0.99985 at 2^10;
    the reviewer's line (i) of the GO, RUN_14.md step 13)."""
    return 1.0 / (1.0 + k_a * IMPACT / math.hypot(L, IMPACT))


def light_pins() -> dict[str, float]:
    """The light row's delay and lever-arm centroid at k_a(b) = 0.0445
    (NEWTON_FROM_CLICKS 3 (c) and (e); the design's 3.97 uses the pace on
    the heading, 32 / 55). The READ delay (RUN_14.md step 13): the two
    clocks at the ends count at `clocks_rate` of the tick, so T_mass =
    rate x (89 + 3.96) against the control's 89: +3.0, not +3.96."""
    alpha = 2.0 * FLIGHT_COEFFICIENT * K_A_LIGHT
    lever = alpha * (math.pi * IMPACT / 4.0)
    wall_delay = FLIGHT_COEFFICIENT * IMPACT * K_A_LIGHT / LIGHT_PACE_HEADING * logarithm()
    control = light_arrival_count()
    return {
        "wall_delay": wall_delay,
        "clocks_rate": clocks_rate(K_A_LIGHT),
        "read_delay": clocks_rate(K_A_LIGHT) * (control + wall_delay) - control,
        "alpha": alpha,
        "centroid_toward_mass": alpha * L,
        "centroid_toward_mass_crossing": alpha * L + lever,
    }


def light_arrival_count() -> int:
    """The light row's arrival count on the heading, the flight table's
    ceil((2 L_LINE - 1) T_D / (2 S_1 Q)) with S_1 = 1, Q = 64, T_D = 110
    (55 for 32 Links): 89 for 52 Links."""
    return -(-(2 * L_LINE - 1) * 110 // (2 * LABEL_SCALE))


def expectations() -> Json:
    massive = massive_pins()
    light = light_pins()
    net = round(massive["net"], 1)
    return {
        "format": EXPECTATIONS_FORMAT,
        "design": "docs/designs/newton_clicks/NEWTON_ON_THE_SIDE.md section 4.1; docs/designs/fail_rows/RUN_14.md sections 1 to 3",
        "kinds": "every pin a DETECTOR reading (a click's Node, the receiver's own count under clock_stamp, the row's ordinal); every number here COMPUTATION before the run; the tick GAMEBOARD, printed beside and never pinned",
        "rung": {
            "k": RUNG,
            "M_row": M_ROW,
            "p": MOMENTUM_MAGNITUDE,
            "rest_energy": REST_ENERGY,
            "pace_wall": PACE_WALL,
            "links_per_count": f"1 / {RUNG}",
            "ladder_quantum": f"1 / {RUNG * (RUNG + 1)}",
            "u_over_c": round(massive["u_over_c"], 4),
        },
        "k_a": {
            "massive_worlds": K_A_MASSIVE,
            "light_world": K_A_LIGHT,
            "source": "the gr_rows pin world's GAMEBOARD age moment at (2^16, b = 6, [1, 4096]) scaled linearly to 2^10; DETECTOR when a lamp at b reads it against a control; every conditional pin below is re-derived by the same forms once read",
        },
        "geometry": {"impact": IMPACT, "L": L, "L_line": L_LINE, "logarithm": round(logarithm(), 4)},
        "window": {
            "massive": ARRIVAL_CONTROL - 60,
            "light": light_arrival_count() + WINDOW_AFTER_ARRIVAL,
        },
        "worlds": {
            "control": {
                "arrival_count": {
                    "pin": ARRIVAL_CONTROL,
                    "bracket": 1,
                    "every_click_alike": "after the first ordinal: the lamp at the content K births at its first self-creation, skips the second once and births at every one after, so the ordinal lags its count by one and every click after the first reads the pin plus one (RUN_14.md step 6, the design's edge case)",
                },
                "pace": {"pin": f"1 / {RUNG}", "band": "2 / W over W counts apart (the one band rule)"},
                "centroid_y": {"pin": 0.0, "exact": True},
                "count_ratio": {"pin": 1.0, "bracket": COUNT_RATIO_BRACKET},
            },
            "mass": {
                "arrival_count": {
                    "count": ARRIVAL_CONTROL + 1 + net,
                    "advance": net,
                    "wall_delay": round(massive["wall_delay"], 2),
                    "push_advance": round(massive["push_advance"], 2),
                    "bracket": round(abs(net) * ADVANCE_MARGIN + 0.26, 1),
                    "conditional": True,
                },
                "advance_ratio": {"pin": round(net / ARRIVAL_CONTROL, 4)},
                "centroid_toward_mass": {
                    "pin": round(massive["centroid_toward_mass"], 2),
                    "crossing": round(massive["centroid_toward_mass_crossing"], 2),
                    "bracket": CENTROID_BRACKET,
                    "conditional": True,
                },
                "count_ratio": {"pin": 1.0, "bracket": COUNT_RATIO_BRACKET},
                "advance_over_own_wall_delay": round(massive["advance_over_own_wall_delay"], 1),
                "clocks_shift": round(massive["clocks_shift"], 2),
            },
            "light": {
                "arrival_count": {
                    "control": light_arrival_count(),
                    "wall_delay": round(light["wall_delay"], 2),
                    "clocks_rate": round(light["clocks_rate"], 4),
                    "pin": round(light["read_delay"], 1),
                    "advance": 0.0,
                    "bracket": LIGHT_DELAY_BRACKET,
                    "conditional": True,
                    "note": "the read delay: the wall's +3.96 at c_f = 2 less the two clocks' stretch (the lamp and the receiver both at 26.7 Links from 2^16 count at 0.990 of the tick, so T_mass = 0.990 x (89 + 3.96) = 92.0 against the control's 89); the massive worlds' clocks at 2^10 move their pins by 0.15, inside 3.5",
                },
                "centroid_toward_mass": {
                    "arrivals": round(light["centroid_toward_mass"], 2),
                    "crossing": round(light["centroid_toward_mass_crossing"], 2),
                    "bracket": CENTROID_BRACKET,
                    "deciding": True,
                    "conditional": True,
                },
                "count_ratio": {
                    "pin": 1.0,
                    "bracket": COUNT_RATIO_BRACKET,
                    "against_the_tick": 0.99,
                    "note": "the receiver's counts apart over the lamp's ordinals apart: both clocks in the same crowd at 26 to 27 Links from the mass (r_1 = r_2), so 1.000 within 0.1 per cent; the design's 0.990 is the receiver's rate against the tick, GAMEBOARD, printed as the count behind the tick",
                },
            },
        },
        "derivations": {
            "arrival_count": "NEWTON_ON_THE_SIDE.md 3 (b): m(tau) = floor((2 tau p + E'_D) / (2 E'_D)) at E'_D = k p, the L-th Link at tau = k L - (k - 1) / 2; RUN_14.md step 3",
            "advance": "NEWTON_FROM_CLICKS.md 3 (b) and (d); NEWTON_ON_THE_SIDE.md 3 (c) 1 and 4.1; RUN_14.md steps 7 and 8",
            "centroid": "NEWTON_FROM_CLICKS.md 3 (c); NEWTON_ON_THE_SIDE.md 3 (c) 2 and 4.1; RUN_14.md step 9",
            "light_row": "NEWTON_FROM_CLICKS.md 3 (c) and (e); NEWTON_ON_THE_SIDE.md 3 (c) and 4.1; RUN_14.md step 13 (the read delay +3.0: the clocks' stretch at 26.7 Links)",
            "advance_over_own_wall_delay": "RUN_14.md step 10: the massive row's push advance over its own wall's delay in its world, (c / v)^2 (1 - v^2 / c^2) (1 + gamma_PPN v^2 / c^2) / c_f, a COMPUTATION of two closed forms the run reads only as their sum",
            "count_ratio": "NEWTON_FROM_CLICKS.md 3 (e); the gr_rows design section 4 (0.990 at 2^16, 26.7 Links against the tick); RUN_14.md step 12 (the ratio of two clocks in one crowd, 1.000)",
            "birth_convention": "RUN_14.md step 6: the lamp at the content K births at its first self-creation, skips the second once (its accumulator at K - M_row below the wall K) and births at every one after; every click after the first reads the flight's count plus one; the advance and the delay are differences and carry no convention",
            "receiver_reads": "RUN_14.md step 5: the receivers read the presence; under the design's `age` the arriving rows' age moment would stretch the receiver's own count by 979 / 4096 per click",
        },
    }


def main() -> None:
    print(
        f"rung k = {RUNG}: E'_0 = {REST_ENERGY}, E'_D = {PACE_WALL} = {RUNG} x {MOMENTUM_MAGNITUDE}; "
        f"the control's arrival count {ARRIVAL_CONTROL} for {L_LINE} Links "
        f"(checked {arrival_count(L_LINE)}); the light row's {light_arrival_count()}; "
        f"fan {len(FAN)}, declared {len(DECLARED)}; ticks {TICKS}"
    )
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT))
    path = HERE / "expectations.json"
    path.write_text(json.dumps(expectations(), indent=1) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))
    print(json.dumps({"massive": massive_pins(), "light": light_pins()}, indent=1))


if __name__ == "__main__":
    main()
