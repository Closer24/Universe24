"""The nuclide as one event (the mathematician's 105, A1, and 106, item 1, at the owner's word of 2026-10-02: "try it; the derivation says a great deal, because our model knows how to represent an atom and a nucleus"; ALGEBRA.md #the-click-is-the-meeting, The GHZ gate; #what-is-open, item 1, the masses are families; #the-count-is-the-records-share, The click's unit) from the design file beside this script: one square world (z folded) on the universe file beside it (the holder of the sign at the level weight 1 and the nuclide family, two planes laid as one event and never summed at a Node, at the deuteron's pair; no holder of the content, neither gravity's row nor the binding holder, so the record is free), the record laid as one event at the centre Node by the message lay, three beams to three counters at the board's ends, the two on the x sides reading with the nuclide's whole 2 T sin omega_N and the one on the y side with a part's whole T sin omega_N, every face receding; its mode file by the message lay (tools/pixel_mode.py, with --modes); and the blind expectation file, written from the law's lines before any run and never touched after: the two parts bit-identical at every interval (the equal-parts theorem, the GHZ gate's own: the symmetric lay stepped by the determinism of Rule3), every click's inflow even and one whole nuclide per 2 T sin omega_N, never a half (the part counter's count twice the nuclide counters' reading of the same inflow, exactly), the two parts' shares equal in every region, and the holder of the sign at its rest 0 everywhere (the message lay lays a real packet, whose Wronskian is 0). Every number is the design's or the law's formula's on it and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/nuclide/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
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
AXES = ("x", "y", "z")


def world(design: dict[str, Any]) -> dict[str, object]:
    """The one world: the square board (z folded), the record laid as one event at the centre toward the three counters, each beam's flat top across it with its raised-cosine edges, the three counters at the board's ends (plain regions: a counter declares no setting), the receding faces, the ticks."""
    length, source, depth = int(design["length"]), int(design["source"]), int(design["screen"])
    p, q = (int(v) for v in design["wave"])
    first, last = (int(v) for v in design["top_across"])
    messages, node_readers = [], []
    for name, counter in design["counters"].items():
        along, toward = str(counter["beam"][0]), int(counter["beam"][1])
        across = next(axis for axis in AXES[:2] if axis != along)
        messages.append(
            {
                "family": design["family"],
                "along": along,
                "wave": [toward * p, q],
                "amplitude": int(design["amplitude"]),
                "top": {along: [source, source], across: [first, last], "z": [0, 0]},
                "edge": {along: int(design["edge_along"]), across: int(design["edge_across"]), "z": 0},
            }
        )
        deep = range(depth) if toward < 0 else range(length - depth, length)
        node_readers.append(
            {
                "name": name,
                "positions": [
                    [u if along == "x" else v, v if along == "x" else u, 0]
                    for u in deep
                    for v in range(first, last + 1)
                ],
            }
        )
    return {
        "shape": [length, length, 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "bodies": [],
        "messages": messages,
        "node_readers": node_readers,
        "receding": design["receding"],
    }


def pair_of(value: Fraction) -> list[int]:
    """A fraction as [numerator, denominator] for the file."""
    return [value.numerator, value.denominator]


def expectation(design: dict[str, Any], laid: list[int] | None) -> dict[str, object]:
    """The blind expectation file: the family, the window, the counters with their declared wholes, the pair's rotations against the nucleon's and the binding fraction asked and declared, the lay's count where the mode file was written, and the blind rows, each with its status and its fence."""
    num, den = (int(v) for v in design["pair"])
    num_p, den_p = (int(v) for v in design["nucleon_pair"])
    omega_n, omega_p = math.acos(num / den), math.acos(num_p / den_p)
    sin_omega_n = math.sqrt((den - num) * (den + num)) / den
    asked = Fraction(int(design["binding_fraction"][0]), int(design["binding_fraction"][1]))
    wholes = {
        name: {
            "parts": int(whole["parts"]),
            "formula": whole["formula"],
            "over_T": int(whole["parts"]) * sin_omega_n,
        }
        for name, whole in design["wholes"].items()
    }
    return {
        "verdict": "NODEREADER",
        "comment": design["comment"],
        "family": design["family"],
        "window": [int(v) for v in design["window"]],
        "world": design["world"],
        "counters": {
            name: {"beam": counter["beam"], "whole": counter["whole"]}
            for name, counter in design["counters"].items()
        },
        "wholes": wholes,
        "pair": [num, den],
        "nucleon_pair": [num_p, den_p],
        "omega_N": omega_n,
        "omega_p": omega_p,
        "sin_omega_N": sin_omega_n,
        "binding_fraction": {
            "asked": pair_of(asked),
            "asked_value": float(asked),
            "declared": 1 - omega_n / omega_p,
            "formula": "omega_N = (1 - b_d) omega_p per part, the nuclide's rest rotation below the free nucleon's by the binding fraction; cos omega_N = num / den at the nearest integer numerator, the denominator matter's",
        },
        "laid": laid,
        "seed": int(design["seed"]),
        "rule": "a counter's inflow over the window is the nuclide family's net current through its front, summed over the two parts, in the current's units; its share is the inflow over W_c = 3 den T; its count N is the share over the declared whole over T, 2 sin omega_N for the nuclide counters and sin omega_N for the part counter (The click's unit: the whole of a click is the node_reader's own transition; the energy of one quantum of a family T sin omega by the families reading); the parts lines give the two parts' signed level sums per interval and region",
        "blind": {
            "equal_parts": {
                "reading": "every `parts` line of the three counters over the window: the two parts' [now, before] sums",
                "blind": "bit-identical at every interval and every counter, the parts' mismatch ratios 1 and every squares ratio 1",
                "status": "theorem: the two parts are laid equal by the symmetric lay and stepped by one deterministic Rule3 on one board with no holder telling them apart (the holder of the sign reads the Wronskian, 0 on both), so they stay equal bit for bit; the GHZ gate's own equal-parts theorem with two parts and the holders removed (106, item 1)",
                "fence": "clicks (the instrument's read); the arrays' equality a GameBoard reading beside it",
            },
            "whole_clicks": {
                "reading": "every `click` line's inflow on the three counters over the window, and each counter's inflow summed",
                "blind": "every inflow is an even integer, twice one part's current, so a counter reading with the nuclide's whole 2 T sin omega_N credits whole nuclides and never a half; the part counter's count by T sin omega_N is exactly twice the same inflow's count by 2 T sin omega_N, and the part counter clicks nothing the nuclide counters' whole does not credit whole",
                "status": "theorem under equal parts: the inflow is the family's current summed over its two lines pairs, each part's current the same integer; derived from the law's lines (the count is the record's share; the click's unit the node_reader's own transition)",
                "fence": "clicks",
            },
            "equal_shares": {
                "reading": "the parts' squares ratios per counter from the `parts` lines (tools/bell_gate.py, mismatch), and the parts' arrays",
                "blind": "the two parts' shares equal in every region at every interval, the ratio 1 exactly",
                "status": "theorem, the same equality: the share is a function of a part's own levels",
                "fence": "clicks for the parts lines; GameBoard for the arrays",
            },
            "sign_holder": {
                "reading": "the holder of the sign's `field` lines at the counters and its level over the board",
                "blind": "0 everywhere at every interval: the message lay lays a real packet (ALGEBRA.md #the-generator (h)), both parts' second level pairs 0, their Wronskian 0, so nothing sources the holder and its rest is 0; the one-plane source's far level, 3 (W / T) / (4 pi Gamma r) at the sense +1, is what a proton laid with a sense would give and this lay cannot carry, said so",
                "status": "derived from the lay as written; the sense of the proton part waits for a lay that carries it (the generator's sense is for bodies alone)",
                "fence": "GameBoard: a holder's level is a reading and no click",
            },
        },
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the world written")
    parser.add_argument(
        "--modes", action="store_true", help="write the mode file too (tools/pixel_mode.py)"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    path = args.folder / (str(design["world"]) + ".json")
    path.write_text(json.dumps(world(design)) + "\n", encoding="utf-8")
    laid = None
    if args.modes:
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
            check=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
        )
        mode = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
        laid = [int(message["count"]) for message in mode["messages"]]
    print(json.dumps({"world": str(path), "laid": laid}))
    written = expectation(design, laid)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(args.folder / "expectation.json")}))


if __name__ == "__main__":
    main()
