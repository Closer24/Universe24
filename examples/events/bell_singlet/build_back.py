"""The singlet's fifth world, the click that runs back (ALGEBRA.md, The meeting's reading, root or back, 2026-10-19; ENGINE.md section 3, act 6, and section 10, item 11): the (a, b) world of build_world.py with one added word on its draw, `meeting: back`, the same seed, the same family's sign and the same identity patterns as the folder's four worlds declare, written beside them as `singlet_back_a_b.json` with its mode file (tools/pixel_mode.py, the packet lay, with --modes), and the back mode's blind written beside the folder's blind, into `expectation_back.json` under the key `back` (the folder's expectation.json stays its builder's byte for byte), derived from the folder's blind before any run: the same E and S as the root mode (the same joint shares, the identity P(A) P(B | A) = P(A, B)), the first side's marginal, the partner's conditional shares at each of the first side's ports, the two credit lines with `meeting: back` and `order` 1 and 2, and the realised pair opposite at equal axes; the same file carrying the folder's blind with the fifth world in the (a, b) run's place, the gate's blind for the reading of the four output files with the fifth world's among them (tools/spin_gate.py) and for the fifth world's page (tools/look/page.py --gate). Every number is the design's or the folder's blind's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/bell_singlet/build_back.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MEETING = "back"  # the one added word on the draw
FIRST, SECOND = "a", "b"  # the sides in the order of their closes: one window, the declared order


def builder() -> Any:
    """The folder's build_world.py loaded by path: the fifth world is its (a, b) world and no other declaration."""
    spec = importlib.util.spec_from_file_location("bell_singlet_build_world", HERE / "build_world.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def world(design: dict[str, Any], build: Any) -> dict[str, object]:
    """The (a, b) world as build_world.py writes it, its draw with `meeting: back`."""
    document = build.world(design, FIRST, SECOND)
    document["draw"] = {**dict(design["draw"]), "meeting": MEETING}
    return document


def fraction(pair: list[int]) -> Fraction:
    return Fraction(int(pair[0]), int(pair[1]))


def pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def blind(expectation: dict[str, Any], sides: dict[str, str]) -> dict[str, Any]:
    """The back mode's blind from the folder's blind at the settings (a, b): the first side's marginal, the sum of the joint shares over the partner's ports; the partner's conditional at each of the first side's ports, J(p, q) over SUM_q' J(p, q'); the same E and S; the two credit lines in the order of the closes."""
    key = f"{FIRST} {SECOND}"
    joint = {k: fraction(v) for k, v in expectation["blind"]["joint"][key].items()}
    ports = ("plus", "minus")
    marginal = {p: sum(joint[f"{p} {q}"] for q in ports) for p in ports}
    total = sum(marginal.values())
    conditional = {p: {q: joint[f"{p} {q}"] / marginal[p] for q in ports} for p in ports}
    sequential = {f"{p} {q}": marginal[p] / total * conditional[p][q] for p in ports for q in ports}
    assert sequential == {
        k: v / total for k, v in joint.items()
    }  # P(A) P(B | A) = P(A, B), the identity
    return {
        "world": f"singlet_{MEETING}_{FIRST}_{SECOND}",
        "settings": key,
        "meeting": MEETING,
        "order": [sides[FIRST], sides[SECOND]],
        "first_marginal": {p: pair(marginal[p] / total) for p in ports},
        "partner_conditional": {p: {q: pair(conditional[p][q]) for q in ports} for p in ports},
        "sequential_shares": {k: pair(v) for k, v in sequential.items()},
        "correlation": expectation["blind"]["correlation"][key],
        "S": expectation["blind"]["S"],
        "credit_lines": [
            {"node_detector": sides[FIRST], "meeting": MEETING, "order": 1, "count": 1},
            {"node_detector": sides[SECOND], "meeting": MEETING, "order": 2, "count": 1},
        ],
        "at_equal_axes": "the realised pair opposite: the partner's weight at the first side's port 0 exactly",
        "status": (
            "theorem under the law's paragraph The meeting's reading, root or back: the first side's marginal is the sum of "
            "the joint shares over the partner's ports, the partner's share at its port is its one-side sum of the parts "
            "re-weighted by what the first port read of them, and P(A) P(B | A) = P(A, B) exactly in the books' integers, so "
            "the two local draws give the joint distribution of the one draw through the root, E and S the root mode's; the run "
            "back and forward returns every array bit for bit, a reading and never a write; the look of this world holds three "
            "passes, the run to the first close, the run back to the birth with its intervals decreasing, the run forward to "
            "the partner's close"
        ),
        "fence": "clicks",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes", action="store_true", help="write the mode file too (tools/pixel_mode.py)"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    build = builder()
    args.folder.mkdir(parents=True, exist_ok=True)
    path = args.folder / f"singlet_{MEETING}_{FIRST}_{SECOND}.json"
    path.write_text(json.dumps(world(design, build)) + "\n", encoding="utf-8")
    if args.modes:
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
            check=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
        )
    print(json.dumps({"world": str(path), "settings": [FIRST, SECOND], "meeting": MEETING}))
    expectation = json.loads(
        (args.folder / "expectation.json").read_text(encoding="utf-8")
    )  # read, never written
    expectation[MEETING] = blind(expectation, design["sides"])
    gate = {
        **expectation,
        "runs": {**expectation["runs"], f"{FIRST} {SECOND}": expectation[MEETING]["world"]},
    }
    gate["comment"] = (
        f"The folder's blind with the fifth world, {expectation[MEETING]['world']} (the click that runs back, "
        f"`meeting: back`), in the ({FIRST}, {SECOND}) run's place: the gate's blind for the reading of the four output "
        "files with the fifth world's among them and for the fifth world's page; every number the folder's "
        "expectation.json's, written before any run. " + str(expectation["comment"])
    )
    beside = args.folder / f"expectation_{MEETING}.json"
    beside.write_text(json.dumps(gate, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"expectation": str(beside), "key": MEETING, "S": gate[MEETING]["S"], "runs": gate["runs"]}
        )
    )


if __name__ == "__main__":
    main()
