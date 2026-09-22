"""Write the ring worlds of `flow-link-v1` (the model owner's decision of
2026-09-22, record 915 of docs/LOG_2026-09-20.md: admit the key to the ring
world and run it once; the design docs/designs/flow_weight/DESIGN.md
section 4 with ALGEBRA.md section 4, the physics-rule reviewer's
ADMISSIBLE of record 902) and their expectations BEFORE any run
(`expectations.json`, the pins by kind from the design's map
docs/designs/flow_weight/flow_weight_map.out, section 4, form `flow`).

The construction is STEP_ALGEBRA.md section 9's on series K's box (the one
copy of the fan, the screen and the box in
examples/events/lensing/make_worlds.py): the open 57 x 41 x 41 box, the
mass of the free phase-less family `m` at the centre with content 2^16
(sixteen times series K's SOURCE, the optical pin worlds' mass) releasing
on the fan of 290 primitive directions within Manhattan 6, the pair
`suspension` [1, 16384] with the `width` 16384 declared (the pin n S = d
of the Einstein derivation II.10a), and in place of series K's one lamp a
RING of lamps of the paid family `light` on the lamp's plane x = 2: one
fixed measured event at every Node (y, z) with |sqrt(y^2 + z^2) - b| <=
1 / 2 about the mass's line (`ring_starts` of the Bending Algebraist's
step_algebra_map.py, one copy: 16 starts at b = 3, 40 at b = 6, 48 at
b = 8), each releasing one unit per interval on the heading (1, 0, 0)
alone; the screen x = 54 of one-Node `wave` detectors reading `age`, every
Node of it a detector, as series K has it. The keys `optical: gamma` at
gamma 0 and 1 and `flow_link: true`; the control of every ring (no mass,
the same lamps and keys) beside it, so that every start's arrival Node
and age are read against its own control's.

The calibration of the build (DESIGN.md section 6; ALGEBRA.md section 1):
the registered `optical/mass_g0.json` and `mass_g1.json` under the key,
as copies beside the ring worlds (`calibration_mass_g0.json`,
`calibration_mass_g1.json`: the registered document with `flow_link: true`
added and nothing else changed; the registered files are never edited),
read against the registered controls `optical/control_g0.json` and
`control_g1.json` run as they are: the algebra's shifts -1.600 / -3.000
pixels (the register's -1.993 / -3.989, DETECTOR, as built).

    python examples/events/flow_link/make_worlds.py     # the worlds and expectations.json
"""

from __future__ import annotations

import importlib.util
import json
import math
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402

Json = dict[str, object]
EXPECTATIONS_FORMAT = "flow-link-expectations-v1"
IDENTITY = "flow-link-v1"
MODEL_PREFIX = "rays-flow-link-"
# The pin world's pair and width (the pin n S = d), the mass sixteen times
# series K's SOURCE = 2^12 (the optical pin worlds' 2^16).
SUSPENSION = [1, 16384]
WIDTH = 16384
MASS_FACTOR = 16
GAMMAS = (0, 1)
IMPACTS = (6, 3, 8)
LAMP_X = 2
# The design's constants (DESIGN.md section 4, ALGEBRA.md section 4): the
# declared c_f = 2 (an input, record 826 (D)); the finite path from x = -26
# to +26 about the mass, L = 26; the shells' factor 0.990 (the crowd's
# shell mean of the weighted flow against the continuum's q / (4 pi),
# ALGEBRA.md section 2); the Nodes' own conversion 4 pi S / (3 q) at this
# M and pin, q = 290 x 16 = 4640 units per interval.
C_F = 2
PATH_HALF_LENGTH = 26
SHELLS_FACTOR = 0.990
UNITS_PER_INTERVAL = 290 * 16
NODES_CONVERSION = 4 * math.pi * WIDTH / (3 * UNITS_PER_INTERVAL)
# The delays' bracket (the register's, one interval) and the tangential
# mean's (one Node over the ring's count).
DELAY_BRACKET = 1.0
MAP_OUT = ROOT / "docs" / "designs" / "flow_weight" / "flow_weight_map.out"
STEP_ALGEBRA = ROOT / "docs" / "designs" / "light_bending" / "step_algebra_map.py"
CALIBRATION = ("mass_g0", "mass_g1")
CALIBRATION_PINS = {"mass_g0": -1.600, "mass_g1": -3.000}
CALIBRATION_REGISTERED = {"mass_g0": -1.993, "mass_g1": -3.989}


def _script(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, module)
    spec.loader.exec_module(module)
    return module


K = _script("lensing_make_worlds", HERE.parent / "lensing" / "make_worlds.py")
ring_starts = _script("step_algebra_map", STEP_ALGEBRA).ring_starts


def world_name(b: int, gamma: int, control: bool) -> str:
    return f"ring_b{b}_{'control_' if control else ''}g{gamma}"


def ring_world(b: int, gamma: int, *, control: bool) -> Json:
    """Series K's box with the ring of lamps at the impact distance b on the
    heading, under `optical: gamma` and `flow_link: true`, the mass 2^16 at
    the pin (none in the control)."""
    document = K.world("control" if control else "mass")
    centre = K.CENTRE
    lamps: list[Json] = [
        {
            "position": [LAMP_X, centre[1] + y, centre[2] + z],
            "family": "light",
            "amount": K.LAMP_CONTENT,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [1, 1], "wheel": [1, K.N], "directions": [[1, 0, 0]]},
            "table": {"m": "pass"},
        }
        for y, z in ring_starts(b)
    ]
    rest = [entry for entry in document["measured"] if "lamp" not in entry]  # type: ignore[union-attr]
    for entry in rest:
        if entry["family"] == "m":
            entry["amount"] = entry["amount"] * MASS_FACTOR  # type: ignore[operator]
    document["measured"] = [*lamps, *rest]
    document["model_id"] = MODEL_PREFIX + world_name(b, gamma, control).replace("_", "-") + "-v1"
    document["suspension"] = list(SUSPENSION)
    document["width"] = WIDTH
    document["optical"] = gamma
    document["flow_link"] = True
    return families_by_definition(document, K.FAMILY_DEFINITIONS, K.DEFINITIONS_SOURCE)


def calibration_world(name: str) -> Json:
    """The registered optical world with the key added and nothing else
    changed (the model id the register's, so `tools/lensing_readings.py`
    reads it against the registered control of its gamma)."""
    document = json.loads((HERE.parent / "optical" / f"{name}.json").read_text(encoding="utf-8"))
    document["flow_link"] = True
    return document


def worlds() -> dict[str, Json]:
    found: dict[str, Json] = {}
    for b in IMPACTS:
        for gamma in GAMMAS:
            found[world_name(b, gamma, False)] = ring_world(b, gamma, control=False)
            found[world_name(b, gamma, True)] = ring_world(b, gamma, control=True)
    for name in CALIBRATION:
        found[f"calibration_{name}"] = calibration_world(name)
    return found


# -- the pins, read from the design's map ---------------------------------------------

RING_LINE = re.compile(
    r"b = (?P<b>\d+), (?P<count>\d+) starts, form (?P<form>\w+), gamma (?P<gamma>\d): "
    r"tan alpha_r (?P<tan>[-\d.]+) \(tangential (?P<tangential>[-+\d.]+)\); "
    r"C_ring = (?P<c_ring>[\d.]+) against 4; the arrival Node's radial shift (?P<shift>[\d.]+) Links "
    r"\(C from the Nodes (?P<c_nodes>[\d.]+)\); the delay (?P<delay>[-\d.]+); the grain (?P<grain>[\d.]+); "
    r"starts moved by 0 / 1 / 2 / 3 Nodes: (?P<m0>\d+) / (?P<m1>\d+) / (?P<m2>\d+) / (?P<m3>\d+)"
)
START_LINE = re.compile(r"\((?P<y>[-+]\d+),(?P<z>[-+]\d+)\) (?P<dy>[-+]\d+),(?P<dz>[-+]\d+)")


def map_pins() -> dict[tuple[int, int, str], dict[str, object]]:
    """Section 4 of the map's output: per (b, gamma, form) the ring's
    numbers, and under the form `flow` the arrival Node per start."""
    found: dict[tuple[int, int, str], dict[str, object]] = {}
    lines = MAP_OUT.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(lines):
        match = RING_LINE.search(line)
        if match is None:
            continue
        b, gamma, form = int(match["b"]), int(match["gamma"]), match["form"]
        entry: dict[str, object] = {
            "count": int(match["count"]),
            "tan_alpha_r": float(match["tan"]),
            "tangential": float(match["tangential"]),
            "c_ring": float(match["c_ring"]),
            "radial_shift": float(match["shift"]),
            "c_nodes": float(match["c_nodes"]),
            "delay": float(match["delay"]),
            "grain": float(match["grain"]),
            "moved": [int(match[k]) for k in ("m0", "m1", "m2", "m3")],
        }
        if form == "flow":
            starts = START_LINE.findall(lines[index + 1])
            assert len(starts) == entry["count"], (b, gamma, len(starts))
            entry["arrival_nodes"] = {
                f"({int(y)},{int(z)})": [int(dy), int(dz)] for y, z, dy, dz in starts
            }
        found[(b, gamma, form)] = entry
    return found


def expected_c_ring(b: int) -> float:
    """The design's expected `2 c_f x 0.990 x L / sqrt(L^2 + b^2)`: the
    declared 2 c_f times the shells' factor times the finite path's."""
    path = PATH_HALF_LENGTH / math.sqrt(PATH_HALF_LENGTH**2 + b * b)
    return 2 * C_F * SHELLS_FACTOR * path


def expectations() -> Json:
    pins = map_pins()
    by_world: dict[str, Json] = {}
    for b in IMPACTS:
        for gamma in GAMMAS:
            flow = pins[(b, gamma, "flow")]
            built = pins[(b, gamma, "unit")]
            count = int(flow["count"])
            assert count == len(ring_starts(b))
            tolerance = 1.0 / count
            path_factor = PATH_HALF_LENGTH / math.sqrt(PATH_HALF_LENGTH**2 + b * b)
            c_expected = expected_c_ring(b) / (2 if gamma == 0 else 1)
            lever_arm = float(flow["c_nodes"]) / float(flow["c_ring"])
            by_world[world_name(b, gamma, False)] = {
                "impact": b,
                "gamma": gamma,
                "flight_coefficient": 1 + gamma,
                "starts": count,
                "control": world_name(b, gamma, True),
                "radial_shift": {
                    "kind": "DETECTOR",
                    "line": "click on a screen pixel: the arrival Node (dy, dz) of each start against its control's, the mean over the ring of -(dy y + dz z) / r in Links",
                    "value": flow["radial_shift"],
                    "tolerance": round(tolerance, 4),
                    "as_built": built["radial_shift"],
                    "derivation": "DESIGN.md section 4 and ALGEBRA.md section 4 (the step algebra's walk of every start under the flow label f_D; flow_weight_map.out section 4, form flow); the tolerance one Node per start over the ring's count",
                },
                "arrival_nodes": {
                    "kind": "DETECTOR",
                    "line": "click on a screen pixel: per start (y, z) the arrival Node's (dy, dz) against the control's",
                    "value": flow["arrival_nodes"],
                    "moved_by_0_1_2_3_nodes": flow["moved"],
                    "derivation": "flow_weight_map.out section 4, form flow, the arrival Nodes per start",
                },
                "delay": {
                    "kind": "DETECTOR",
                    "line": "click on a screen pixel: the click's age (reads: age) less the control's, the mean over the ring in intervals",
                    "value": flow["delay"],
                    "tolerance": DELAY_BRACKET,
                    "derivation": "flow_weight_map.out section 4; the register's bracket of one interval",
                },
                "tangential_shift": {
                    "kind": "DETECTOR",
                    "line": "click on a screen pixel: the mean over the ring of the arrival Node's tangential shift (dy (-z) + dz y) / r in Links",
                    "value": 0.0,
                    "tolerance": round(tolerance, 4),
                    "derivation": "the fan's symmetry under the 48 signed axis permutations (STEP_ALGEBRA.md section 9): 0.00000 at every ring in the map",
                },
                "c_nodes": {
                    "kind": "CONVERSION of the DETECTOR reading",
                    "line": "C_nodes = (mean radial shift / 26) x b x 4 pi S / (3 q), 4 pi S / (3 q) = 14.79 at this M and pin",
                    "value": flow["c_nodes"],
                    "tolerance": round(tolerance / PATH_HALF_LENGTH * b * NODES_CONVERSION, 3),
                    "derivation": "DESIGN.md section 4 (the Nodes' own conversion, record 872 (e)); the lever arm's factor C_nodes / C_ring stated before the run",
                },
                "c_ring": {
                    "kind": "CONVERSION through the stated lever-arm factor",
                    "line": "C_ring = C_nodes / (the lever-arm factor), against 2 c_f x 0.990 x L / sqrt(L^2 + b^2) on the clock's G M = q / (4 pi S)",
                    "value": flow["c_ring"],
                    "lever_arm_factor": round(lever_arm, 3),
                    "expected": round(c_expected, 3),
                    "grain": flow["grain"],
                    "path_factor": round(path_factor, 3),
                    "shells_factor": SHELLS_FACTOR,
                    "as_built": built["c_ring"],
                    "derivation": "ALGEBRA.md section 3: the algebra's C_ring from the momentum (GAMEBOARD, not what a run compares) and its expected 2 c_f x 0.990 x L / sqrt(L^2 + b^2); Einstein's 4 on the comparison side only (record 817)",
                },
                "tan_alpha_r": {
                    "kind": "GAMEBOARD",
                    "line": "the momentum's radial deflection at the screen, the step algebra's number, not read by the run",
                    "value": flow["tan_alpha_r"],
                },
            }
    return {
        "format": EXPECTATIONS_FORMAT,
        "identity": IDENTITY,
        "design": "docs/designs/flow_weight/DESIGN.md section 4 and ALGEBRA.md section 4 (b463ac24, PR #839); the model docs/designs/flow_weight/flow_weight_map.py, its output flow_weight_map.out section 4; STEP_ALGEBRA.md sections 9 and 11",
        "decision": "the model owner, 2026-09-22, record 915 of docs/LOG_2026-09-20.md: admit flow-link-v1 to the ring world and run it once",
        "constants": {
            "Q": 64,
            "mass": (1 << 12) * MASS_FACTOR,
            "suspension": SUSPENSION,
            "width": WIDTH,
            "fan": 290,
            "units_per_interval": UNITS_PER_INTERVAL,
            "c_f": C_F,
            "path_half_length": PATH_HALF_LENGTH,
            "shells_factor": SHELLS_FACTOR,
            "nodes_conversion": round(NODES_CONVERSION, 3),
            "ticks": K.TICKS,
            "lamp_x": LAMP_X,
            "screen_x": K.SCREEN_X,
        },
        "worlds": by_world,
        "controls": {
            world_name(b, gamma, True): {
                "impact": b,
                "gamma": gamma,
                "expected": "every start arrives at its own (y, z) at the control's age (about 89 to 90 intervals on the heading); no crowd, so the key reads nothing",
            }
            for b in IMPACTS
            for gamma in GAMMAS
        },
        "calibration": {
            f"calibration_{name}": {
                "kind": "DETECTOR",
                "line": "the screen's centroid shift in pixels against the registered control of its gamma (tools/lensing_readings.py)",
                "value": CALIBRATION_PINS[name],
                "tolerance": 0.5,
                "registered_as_built": CALIBRATION_REGISTERED[name],
                "derivation": "ALGEBRA.md section 1 (the map's section 3, form flow): the five lines' shifts under the rule, -1, -1, -2, -2, -2 at gamma 0 and -3 x 5 at gamma 1; the registered files never edited",
            }
            for name in CALIBRATION
        },
        "refutes": [
            "a C_ring that, after the two stated factors (the shells' 0.990 and the finite path's L / sqrt(L^2 + b^2)) and through the stated lever-arm factor, leaves 2 c_f by more than the grain in either direction",
            "any clock reading that moves under the key (the control worlds' ages; the calibration's delay outside the register's bracket)",
            "a world without the key that differs from main's by a byte (tests/test_flow_link.py (a))",
            "a mean radial shift of 0.974 at b = 6, gamma 1: the key not in the run (the law as built)",
        ],
        "host_cost_estimate": {
            "kind": "HOST",
            "line": "STEP_ALGEBRA.md section 11, DESIGN.md section 5: the ring world about the mass world's cost times the lamps' rows (the crowd's 290 rows per interval the cost; the ring's 40 rows per interval a tenth more than the crowd, the beam's 5); the estimate before the run, the measure after it in README.md",
            "ring_world_seconds": [60, 120],
            "control_world_seconds": [2, 10],
            "wall_clock_minutes_at_4_jobs": [5, 8],
            "peak_memory_mb_per_world": 1000,
            "basis": "optical/mass_g1.json: 2.0 s for its first 40 intervals on this host (4 cores, 15 GB); 110 s at 1000 intervals on the owner's machine (optical/README.md)",
        },
    }


def main() -> None:
    for name, document in worlds().items():
        path = HERE / f"{name}.json"
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT), len(document["measured"]), "measured events")  # type: ignore[arg-type]
    path = HERE / "expectations.json"
    path.write_text(json.dumps(expectations(), indent=1) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
