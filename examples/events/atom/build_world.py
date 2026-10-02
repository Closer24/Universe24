"""The toy atom (the mathematician's 105, The atom's clicks, and 106, item 2, at the owner's word of 2026-10-02: "try it; the derivation says a great deal, because our model knows how to represent an atom and a nucleus"; ALGEBRA.md #a-familys-declaration, The atom is a bound body of the holder of the sign; the owner's decision on alpha as a declared coefficient k of the sign holder's read) from the design file beside this script: one open cube on the universe file beside it (the holder of the sign at the act rotation with the owner's weight k in its level weight slot, said so in the design; a heavy nucleus family and the electron family, both planes; no holder of the content), the point nucleus one quantum in the sense +1 at the centre and the electron one quantum in the sense -1 to be laid as 1s + 2p by the generator, a photocathode and a bolometer beside it on the x high side backed by a receding face; and the blind expectation file, written from the law's lines before any lay and any run and never touched after: Rydberg's ratios 1 - 1 / n^2, the line Omega = (3 / 4) alpha_law^2 omega_0 / 2, one photon per click at the photocathode, sin Omega as many at the bolometer, the far sign level 0. Written and not run: the lay waits for the generator laying a plane record standing in an angle well under the rotation read (start-form-fix); --modes is offered as every builder offers it and is not to be used before that fix. Every number is the design's or the law's formula's on it and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/atom/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def span_of(value: Any) -> tuple[int, int]:
    """A design's [first, last] as a pair of integers."""
    return int(value[0]), int(value[1])


def region(design: dict[str, Any], across: tuple[int, int]) -> list[list[int]]:
    """A region on the x high side's last layers, `screen` Nodes deep, over the y span given and the design's z span."""
    side, depth = int(design["side"]), int(design["screen"])
    z_first, z_last = (int(v) for v in design["across_z"])
    return [
        [x, y, z]
        for x in range(side - depth, side)
        for y in range(across[0], across[1] + 1)
        for z in range(z_first, z_last + 1)
    ]


def world(design: dict[str, Any]) -> dict[str, object]:
    """The one world: the open cube, the nucleus declared with one quantum at the centre Node and the electron with one quantum `bohr_links` Links from it along x (no Node shared; the generator rewrites a body's Nodes and counts when it lays), the photocathode and the bolometer beside it on the x high side, the x faces receding, the ticks."""
    side = int(design["side"])
    centre = side // 2
    return {
        "shape": [side, side, side],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [
            {
                "family": design["nucleus_family"],
                "nodes": [{"node": [centre, centre, centre], "count": int(design["quanta"]["nucleus"])}],
            },
            {
                "family": design["electron_family"],
                "nodes": [
                    {
                        "node": [centre + int(design["bohr_links"]), centre, centre],
                        "count": int(design["quanta"]["electron"]),
                    }
                ],
            },
        ],
        "detectors": [
            {
                "name": design["photocathode"],
                "positions": region(design, span_of(design["photocathode_across"])),
            },
            {
                "name": design["bolometer"],
                "positions": region(design, span_of(design["bolometer_across"])),
            },
        ],
        "receding": design["receding"],
    }


def pair_of(value: Fraction) -> list[int]:
    """A fraction as [numerator, denominator] for the file."""
    return [value.numerator, value.denominator]


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file from the design's integers and the law's formulas: alpha_law = (3 sqrt 3 / 8 pi) k / (Gamma E_s), the electron's rest rotation omega_0 and its reduced Compton length 1 / (sqrt 3 omega_0) Links, the Bohr radius, the levels E_n = alpha_law^2 omega_0 / (2 n^2), the Lyman lines and their ratios 1 - 1 / n^2, the 1s + 2p line Omega with its period and sin Omega, the two detectors' wholes, the nucleus's inertia against the electron's, and every row's status and fence."""
    gamma = int(design["node_clock"])
    k, e_s = int(design["k"]), int(design["level_weight_E_s_intended"])
    num_e, den_e = (int(v) for v in design["electron_pair"])
    num_n, den_n = (int(v) for v in design["nucleus_pair"])
    alpha = (3 * math.sqrt(3) / (8 * math.pi)) * k / (gamma * e_s)
    omega_0 = math.acos(num_e / den_e)
    omega_n = math.acos(num_n / den_n)
    compton = 1 / (math.sqrt(3) * omega_0)
    bohr = compton / alpha
    binding = alpha * alpha * omega_0 / 2
    lines = {
        str(n): {"ratio": pair_of(Fraction(n * n - 1, n * n)), "omega": binding * (1 - 1 / (n * n))}
        for n in (int(v) for v in design["lyman_n"])
    }
    omega_21 = binding * 3 / 4
    return {
        "verdict": "DETECTOR",
        "comment": design["comment"],
        "world": design["world"],
        "status_of_the_world": "written and not run; the lay waits for the generator laying a plane record standing in an angle well under the rotation read (start-form-fix), and the sign holder's read weight k waits for its key in the engine (the number stands in the level weight slot, which today's engine reads as the write's divisor E_s)",
        "window": [int(v) for v in design["window"]],
        "families": {
            "nucleus": design["nucleus_family"],
            "electron": design["electron_family"],
            "light": "charge",
        },
        "detectors": {
            design["photocathode"]: {
                "whole": "T sin Omega, one photon of the 1s + 2p line per click (The click's unit: the whole of a click is the detector's own transition)",
                "over_T": math.sin(omega_21),
            },
            design["bolometer"]: {
                "whole": "T, the share over T, the engine's region as it is (a bolometer's reading instrument)",
                "over_T": 1.0,
            },
        },
        "k": k,
        "E_s_intended": e_s,
        "node_clock": gamma,
        "alpha_law": {
            "value": alpha,
            "inverse": 1 / alpha,
            "formula": "alpha_law = (3 sqrt 3 / 8 pi) k / (Gamma E_s), k the sign holder's declared read weight, E_s its level weight (the owner's decision, 5944698532); nature's 1 / 137.036 reads k / (Gamma E_s) = 1 / 28.33, the toy's 0.95",
        },
        "electron": {
            "pair": [num_e, den_e],
            "omega_0": omega_0,
            "compton_links": compton,
            "inertia": 3 * math.tan(omega_0),
            "formula": "omega_0 = arccos(num / den) per interval, the free quantum's rotation; lambda_bar_e = 1 / (sqrt 3 omega_0) Links (one Link is sqrt 3 omega_0 lambda_bar_e, light moving 1 / sqrt 3 Link per interval); m* = 3 tan omega_0, the band's inertia",
        },
        "nucleus": {
            "pair": [num_n, den_n],
            "omega": omega_n,
            "inertia": 3 * math.tan(omega_n),
            "inertia_over_electron": math.tan(omega_n) / math.tan(omega_0),
            "reduced_mass_correction": 1 / (1 + math.tan(omega_0) / math.tan(omega_n)),
        },
        "bohr_radius": {
            "links": bohr,
            "asked": float(design["bohr_radius_asked"]),
            "formula": "a_0 = lambda_bar_e / alpha_law = 1 / (sqrt 3 omega_0 alpha_law) Links; the Boss's arithmetic without light's sqrt 3, 1 / (omega_0 alpha_law), gives sqrt 3 as many",
            "without_sqrt3": 1 / (omega_0 * alpha),
        },
        "levels": {
            "E_1": binding,
            "formula": "E_n = alpha_law^2 omega_0 / (2 n^2) per interval below omega_0, the law's slow limit Schroedinger's with m* = 3 tan omega_0 in the angle theta_0 = alpha_law / r (ALGEBRA.md, The atom is a bound body of the holder of the sign, step 4)",
        },
        "lines": lines,
        "line_1s_2p": {
            "omega": omega_21,
            "period_intervals": 2 * math.pi / omega_21,
            "sin_omega": math.sin(omega_21),
            "formula": "Omega = omega_2 - omega_1 = (3 / 4) alpha_law^2 omega_0 / 2, the beat of the two bound modes, born as light by the Wronskian's breathing",
        },
        "blind": {
            "rydberg": {
                "reading": "the lines read at the photocathode as the beats of its click rate over the window, each over the first",
                "blind": "the ratios 1 - 1 / n^2: 3 / 4, 8 / 9, 15 / 16 for n = 2, 3, 4 against n = infinity (the 1s + 2p lay carries the first line alone; a lay with 3p and 4p the others)",
                "status": "derived from the law's slow limit, two hands (ALGEBRA.md, the atom, steps 4 and 6); the numbers nature's form, the scale alpha_law's",
                "fence": "clicks",
            },
            "the_line": {
                "reading": "the photocathode's click rate's beat over the window",
                "blind": f"Omega = {omega_21:.6f} per interval, the period {2 * math.pi / omega_21:.1f} intervals",
                "status": "derived, the same lines",
                "fence": "clicks",
            },
            "one_photon_per_click": {
                "reading": "the photocathode's inflow over the window over W_c, against its whole sin Omega",
                "blind": "one photon per click: the photocathode's count is its share over sin Omega, whole numbers at the beat; the bolometer beside it credits the share over T, sin Omega as many as the photocathode's photons (the bolometer's count over the photocathode's is sin Omega = 0.0122)",
                "status": "the owner's declaration of the detector (The click's unit: the whole of a click is the detector's own transition), derived consequences two hands",
                "fence": "clicks",
            },
            "far_sign_level": {
                "reading": "the holder of the sign's time level far from the atom, at the faces, at the start and over the window",
                "blind": "0: the nucleus's Wronskian +T / 2 and the electron's -T / 2 sum to 0, the atom neutral; near the atom the dipole of the two sources",
                "status": "derived from the one write (the Wronskian's quanta over E_s T summed over the sources)",
                "fence": "GameBoard: a holder's level is a reading and no click",
            },
            "fall_in_a_content_gradient": {
                "reading": "not read in this world, which holds no holder of the content",
                "blind": "the atom falls as one free quantum in a content gradient (106, item 2; The same clock and the same ruler for every act)",
                "status": "derived; a world with a content holder and a gradient is needed",
                "fence": "GameBoard",
            },
        },
        "seed": int(design["seed"]),
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the world written")
    parser.add_argument(
        "--modes",
        action="store_true",
        help="lay the bodies and write the mode file too (tools/pixel_mode.py); not before start-form-fix",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))
    path = args.folder / (str(design["world"]) + ".json")
    path.write_text(json.dumps(world(design)) + "\n", encoding="utf-8")
    senses = [str(int(design["senses"][body])) for body in ("nucleus", "electron")]
    if args.modes:
        subprocess.run(
            [
                sys.executable,
                str(ROOT / "tools" / "pixel_mode.py"),
                "--input",
                str(path),
                "--sense",
                *senses,
            ],
            check=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
        )
    print(json.dumps({"world": str(path), "senses": senses, "laid": bool(args.modes)}))


if __name__ == "__main__":
    main()
