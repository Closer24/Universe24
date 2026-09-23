"""Write the k_a(b) lamp world pair of row 13 (STEP 2 of
docs/designs/fail_rows/RUN_13_2A.md, section 2 (a); the Boss's GO of
2026-09-23 01:00Z on the physics-rule reviewer's read) and its
expectations BEFORE any run (`expectations.json`, every pin from the
step algebra's crowd, no number typed by hand).

The world: the ring world `flow_link/ring_b6_g1` (series K's open box
57 x 41 x 41, the mass of the free phase-less family `m` at the centre
with content 2^16 releasing on the fan of 290 primitive directions within
Manhattan 6, the pair `suspension` [1, 16384] with `width` 16384, the keys
`optical: 1` and `flow_link: true`, the screen x = 54 of one-Node `wave`
detectors) with the ring of 40 lamps on the plane x = 2 replaced by a
SHELL of lamps: one fixed measured event of the paid family `light` at
every Node with |sqrt(x^2 + y^2 + z^2) - 6| < 1 / 2 about the mass (450
Nodes, the shell of run_13_trend_map.py section 1), each with the entry
`{"m": {"rule": "pass", "reads": "age"}}` so that its own clock counts
the crowd's AGE MOMENT at its Node (the same A that stretches a light
row's wall under the key), releasing one unit per self-creation on the
one heading of its largest coordinate pointing away from the mass (ties
to x, then y), so that no row meets the mass's Node and every row reaches
a face of the open box or the screen's plane, both detectors. 1200
intervals. The control: the same lamps and keys, no mass. Every
declaration is an existing world key; no engine line.

The reading (DETECTOR): per lamp the click lines of the detector its rows
reach (a face's or a screen pixel's), the birth ordinal (`record &
0xFFFFFFFF`) against the click's tick over the window [200, 1200), 1 + k
the inverse slope (series T's reading, `shell_clock/read_runs.py`'s
`slope`), the lamps told apart by the click line's `number`, the
emitter's; `read_lamps.py` beside this file. The pins: per lamp k_i =
n A_i / d with A_i the crowd's age moment at its Node (GAMEBOARD until
read); the shell mean k_a(6) (COMPUTATION on the clicks) against the
algebra's, the bracket 3.4 percent of itself (the ring's own, 0.025 /
0.731); the plane ring's 40 lamps (x = 0) beside it, the comb's own; the
controls 1.0000; the deciding ratio alpha_nodes / k_a(6) with
alpha_nodes = 0.731 / 26 from the registered ring run (DETECTOR).

    python examples/events/lamp_shell/make_worlds.py
"""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))

from event_universe.world_loading import families_by_definition  # noqa: E402

Json = dict[str, object]
EXPECTATIONS_FORMAT = "lamp-shell-expectations-v1"
IDENTITY = "flow-link-v1 under optical-v1 at gamma_PPN = 1"
SUSPENSION = [1, 16384]
WIDTH = 16384
MASS_FACTOR = 16
SCALE = 16  # M = 2^16 at `release` [1, 4096]: 16 units per direction per interval
GAMMA = 1
IMPACT = 6
TICKS = 1200
WINDOW = [200, 1200]
RING_SHIFT = 0.731  # the registered ring run's mean radial shift at b = 6, gamma 1 (DETECTOR)
RING_SHIFT_BRACKET = 0.025
PATH_HALF_LENGTH = 26
LEVER_ARM = 0.683  # C_nodes / C_ring, the walk's, at b = 6 (flow_link/expectations.json)
STEP_ALGEBRA = ROOT / "docs" / "designs" / "light_bending" / "step_algebra_map.py"


def _script(name: str, path: Path):  # type: ignore[no-untyped-def]
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules.setdefault(name, module)
    spec.loader.exec_module(module)
    return module


K = _script("lensing_make_worlds", HERE.parent / "lensing" / "make_worlds.py")
SAM = _script("step_algebra_map", STEP_ALGEBRA)


def shell_nodes(r: int) -> list[tuple[int, int, int]]:
    """Every Node with |sqrt(x^2 + y^2 + z^2) - r| < 1 / 2 about the mass,
    in a fixed order (run_13_trend_map.py's shell)."""
    return [
        (x, y, z)
        for x in range(-15, 16)
        for y in range(-15, 16)
        for z in range(-15, 16)
        if abs(math.sqrt(x * x + y * y + z * z) - r) < 0.5
    ]


def heading_away(node: tuple[int, int, int]) -> list[int]:
    """The heading of the largest coordinate pointing away from the mass,
    ties to x then y."""
    axis = max(range(3), key=lambda i: (abs(node[i]), -i))
    found = [0, 0, 0]
    found[axis] = 1 if node[axis] > 0 else -1
    return found


def world_name(control: bool) -> str:
    return f"shell_b{IMPACT}_{'control_' if control else ''}g{GAMMA}"


def lamp_world(*, control: bool) -> Json:
    document = K.world("control" if control else "mass")
    centre = K.CENTRE
    lamps: list[Json] = [
        {
            "position": [centre[0] + x, centre[1] + y, centre[2] + z],
            "family": "light",
            "amount": K.LAMP_CONTENT,
            "phase": 0,
            "fixed": True,
            "lamp": {"rate": [1, 1], "wheel": [1, K.N], "directions": [heading_away((x, y, z))]},
            "table": {"m": {"rule": "pass", "reads": "age"}},
        }
        for x, y, z in shell_nodes(IMPACT)
    ]
    rest = [entry for entry in document["measured"] if "lamp" not in entry]  # type: ignore[union-attr]
    for entry in rest:
        if entry["family"] == "m":
            entry["amount"] = entry["amount"] * MASS_FACTOR  # type: ignore[operator]
    document["measured"] = [*lamps, *rest]
    document["model_id"] = "rays-lamp-" + world_name(control).replace("_", "-") + "-v1"
    document["ticks"] = TICKS
    document["suspension"] = list(SUSPENSION)
    document["width"] = WIDTH
    document["optical"] = GAMMA
    document["flow_link"] = True
    return families_by_definition(document, K.FAMILY_DEFINITIONS, K.DEFINITIONS_SOURCE)


def expectations() -> Json:
    n, d = SUSPENSION
    fan = SAM.primitive_fan(SAM.FAN_BOUND)
    crowd = SAM.Crowd(fan, SCALE)
    nodes = shell_nodes(IMPACT)
    q = len(fan) * SCALE
    k_cont = 3 * q * n / (4 * math.pi * d * IMPACT)
    lamps: dict[str, Json] = {}
    ks: list[Fraction] = []
    plane: list[Fraction] = []
    for number, node in enumerate(nodes):
        a = crowd.age_moment.get(node, 0)
        k = Fraction(n * a, d)
        ks.append(k)
        if node[0] == 0:
            plane.append(k)
        lamps[str(number)] = {
            "node": list(node),
            "heading": heading_away(node),
            "lines_through": crowd.lines_through.get(node, 0),
            "age_moment": {"kind": "GAMEBOARD", "value": a},
            "k": {
                "kind": "DETECTOR when read",
                "line": "the count ratio less 1 at the detector the lamp's rows reach, against the control's",
                "value": float(k),
                "tolerance": 0.00004,
            },
        }
    k_shell = float(sum(ks, Fraction(0)) / len(ks))
    k_plane = float(sum(plane, Fraction(0)) / len(plane))
    bracket = RING_SHIFT_BRACKET / RING_SHIFT
    alpha_nodes = RING_SHIFT / PATH_HALF_LENGTH
    ratio = alpha_nodes / k_shell
    return {
        "format": EXPECTATIONS_FORMAT,
        "identity": IDENTITY,
        "design": "docs/designs/fail_rows/RUN_13_2A.md sections 1, 2 (a) and 3 (ba558c0e and the fold of the reviewer's three lines); the crowd docs/designs/light_bending/step_algebra_map.py (Crowd), run_13_trend_map.out section 1",
        "decision": "the Boss, 2026-09-23 01:00Z, on the physics-rule reviewer's read of RUN_13_2A.md at ba558c0e: GO for STEP 2, the lamp world pair, judged by the pins of section 3",
        "constants": {
            "Q": 64,
            "mass": (1 << 12) * MASS_FACTOR,
            "suspension": SUSPENSION,
            "width": WIDTH,
            "fan": len(fan),
            "units_per_interval": q,
            "optical": GAMMA,
            "flow_link": True,
            "impact": IMPACT,
            "lamps": len(nodes),
            "plane_lamps": len(plane),
            "ticks": TICKS,
            "window": WINDOW,
            "k_cont": k_cont,
        },
        "worlds": {
            world_name(False): {
                "control": world_name(True),
                "k_shell": {
                    "kind": "COMPUTATION on the DETECTOR readings",
                    "line": "the mean over the 450 lamps of the count ratio less 1 (each lamp: 1 / slope of the birth ordinal against the click's tick over the window, less 1)",
                    "value": k_shell,
                    "bracket": [k_shell * (1 - bracket), k_shell * (1 + bracket)],
                    "derivation": "the crowd's shell mean of the age moment at r = 6 times n / d (RUN_13_2A.md section 3; run_13_trend_map.out section 1: 183.54 / 16384); the bracket 3.4 percent of itself, the ring's own 0.025 / 0.731; the reading's grain 0.04 percent over the window",
                    "k_cont": k_cont,
                    "readme_k_at_4096": k_shell * 4,
                },
                "k_plane": {
                    "kind": "COMPUTATION on the DETECTOR readings",
                    "line": "the mean over the 40 lamps at x = 0 (the ring's plane) of the count ratio less 1",
                    "value": k_plane,
                    "bracket": [k_plane - 0.00004, k_plane + 0.00004],
                    "derivation": "the comb of the coordinate plane, twice the shell's; not the chain's k_a(b), pinned beside it",
                },
                "ratio": {
                    "kind": "COMPUTATION on two DETECTOR readings",
                    "line": "alpha_nodes / k_shell, alpha_nodes = 0.731 / 26 the registered ring run's mean radial shift over the half path (flow_link/expectations.json, the run on the split ladder)",
                    "value": ratio,
                    "bracket": [ratio * (1 - bracket), ratio * (1 + bracket)],
                    "through_lever_arm": ratio / LEVER_ARM,
                    "comparison": "2 c_f = 4 on the comparison side only (Einstein's), the lever-arm factor 0.683 the walk's",
                },
                "lamps": lamps,
            },
            world_name(True): {
                "expected": "every lamp's count ratio 1.0000 exactly (no crowd; the slope of the ordinal against the tick 1); every row reaches a face or the screen",
            },
        },
        "refutes": [
            "the shell mean k_shell outside its bracket: the crowd's stretch at b is not the algebra's shell mean, and every number of row 13 conditional on it moves by the ratio read over pinned, the cause to be found in the lamps' own clicks before any number moves",
            "a lamp's k off its pinned A_i n / d by more than 0.00004: the crowd at that Node is not the algebra's stationary crowd",
            "a control lamp off 1.0000",
            "the ratio alpha_nodes / k_shell outside its bracket",
            "a refusal by the working bound: a register's finding, reported, no pin moved (the algebra puts every pushed row a factor 3 inside the ladder's bound)",
        ],
        "host_cost_estimate": {
            "kind": "HOST",
            "line": "the ring world (40 lamps, 400 intervals) ran 64 s and 157 MB on this class of host; the shell's 450 rows per interval alive about 45 intervals are half the crowd's rows in flight, so 2 to 3 times the cost per interval, 1200 intervals: 6 to 10 minutes and about 1 GB per world, the control less; the record of 540 000 records in run.json the larger file",
        },
    }


def main() -> None:
    for control in (False, True):
        path = HERE / f"{world_name(control)}.json"
        document = lamp_world(control=control)
        path.write_text(json.dumps(document, separators=(",", ":")) + "\n", encoding="utf-8")
        print(path.relative_to(ROOT), len(document["measured"]), "measured events")  # type: ignore[arg-type]
    path = HERE / "expectations.json"
    path.write_text(json.dumps(expectations(), indent=1) + "\n", encoding="utf-8")
    print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
