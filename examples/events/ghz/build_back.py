"""The GHZ gate's world in the back mode, the click that runs back over three sides (ALGEBRA.md, The meeting's reading, root or back, 2026-10-19; ENGINE.md section 3, act 6, and section 10, item 11): the (x, x, x) world of build_world.py with one added word on its draw, `meeting: back`, and nothing more (the run back's reach the cone, the default where the key is absent: the record's own light cone runs back, the rest of the board untouched), the same seed, the same regions and patterns as the folder's four worlds declare, written beside them as `ghz_back_x_x_x.json` with its mode file (tools/pixel_mode.py, the packet lay, with --modes), and the back mode's blind written before any run into `expectation_back.json`, the folder's blind with the back world in the (x, x, x) run's place (the gate's blind for the reading of the four output files with the back world's among them and for its page) and the key `back`: the sides drawn in the order of their closes (one window closing the three regions at one interval, so the declared order), the first side's marginal, the sum of the joint shares over the other sides' ports, each next side's conditional at each realised prefix of ports, J summed over the sides after it over the same sum over its own ports too, the sequential shares the product along the chain, the joint shares exactly (the identity P(A) P(B | A) P(C | A, B) = P(A, B, C)), the same E_3 and M as the root mode, the credit lines with `meeting: back` and `order` 1, 2 and 3, and the prefixes that fix the next side's port (a conditional of 1 and 0, the last side determined by the two before it at x, x, x). Generic over the sides: everything is read from the folder's blind's joint keys, one port word per side. Every number is the design's or the folder's blind's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/ghz/build_back.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MEETING = "back"  # the one added word on the draw
SETTINGS = ("x", "x", "x")  # the world run back: Mermin's fourth, E_3 = +1
PORTS = ("plus", "minus")


def builder() -> Any:
    """The folder's build_world.py loaded by path: the back world is its (x, x, x) world and no other declaration."""
    spec = importlib.util.spec_from_file_location("ghz_build_world", HERE / "build_world.py")
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def world(design: dict[str, Any], build: Any) -> dict[str, object]:
    """The (x, x, x) world as build_world.py writes it, its draw with `meeting: back` and nothing more."""
    document = build.world(design, SETTINGS)
    document["draw"] = {**dict(design["draw"]), "meeting": MEETING}
    return document


def fraction(pair: list[int]) -> Fraction:
    return Fraction(int(pair[0]), int(pair[1]))


def pair(value: Fraction) -> list[int]:
    return [value.numerator, value.denominator]


def blind(expectation: dict[str, Any], sides: list[str]) -> dict[str, Any]:
    """The back mode's blind from the folder's blind at the settings: per side, in the order of the closes, its conditional at each prefix of realised ports (the first side's at the empty prefix, its marginal), the sequential shares, the prefixes that fix the next port, the same E_3 and M, and the credit lines."""
    key = " ".join(SETTINGS)
    joint = {tuple(k.split()): fraction(v) for k, v in expectation["blind"]["joint"][key].items()}
    n, total = len(sides), sum(joint.values())
    assert all(len(ports) == n for ports in joint), "one port word per side in every joint key"

    def summed(prefix: tuple[str, ...]) -> Fraction:
        return sum((v for ports, v in joint.items() if ports[: len(prefix)] == prefix), Fraction(0))

    conditionals = [
        {
            " ".join(prefix): {port: summed((*prefix, port)) / summed(prefix) for port in PORTS}
            for prefix in product(PORTS, repeat=side)
            if summed(prefix)
        }
        for side in range(n)
    ]
    sequential = {}
    for ports in product(PORTS, repeat=n):
        share = Fraction(1)
        for side in range(n):
            share *= conditionals[side][" ".join(ports[:side])][ports[side]]
        sequential[" ".join(ports)] = share
    assert sequential == {" ".join(k): v / total for k, v in joint.items()}  # the identity, exact
    determined = [
        f"{prefix or 'the first side'}: {next(p for p, v in table.items() if v == 1)}"
        for side in range(n)
        for prefix, table in conditionals[side].items()
        if sorted(table.values()) == [Fraction(0), Fraction(1)]
    ]
    return {
        "world": "ghz_" + MEETING + "_" + "_".join(SETTINGS),
        "settings": key,
        "meeting": MEETING,
        "order": list(sides),
        "conditionals": [
            {
                prefix: {port: pair(v) for port, v in table.items()}
                for prefix, table in conditionals[side].items()
            }
            for side in range(n)
        ],
        "sequential_shares": {k: pair(v) for k, v in sequential.items()},
        "determined": determined,
        "correlation": expectation["blind"]["correlation"][key],
        "M": expectation["blind"]["M"],
        "credit_lines": [
            {"node_detector": side, "meeting": MEETING, "order": number, "count": 1}
            for number, side in enumerate(sides, 1)
        ],
        "status": (
            "theorem under the law's paragraph The meeting's reading, root or back: the sides draw in the order of their closes, "
            "each alone at its own place, the first on its marginal from the booked joint, each later side on its conditional "
            "from the same joint with the realised ports fixed (the chain rule), the last side's conditional its share of the "
            "record re-weighted by what the ports before it read, and P(A) P(B | A) P(C | A, B) = P(A, B, C) exactly in the "
            "books' integers, so the three local draws give the "
            "joint distribution of the one draw through the root, E_3 and M the root mode's; between the draws the record runs back "
            "to its birth and forward to the next side, a reading and never a write; the look holds the five passes, the run to the "
            "first close, the run back, the run forward to the second side's close, the run back and the run forward to the third's"
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
    path = args.folder / ("ghz_" + MEETING + "_" + "_".join(SETTINGS) + ".json")
    path.write_text(json.dumps(world(design, build)) + "\n", encoding="utf-8")
    if args.modes:
        subprocess.run(
            [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
            check=True,
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
        )
    print(json.dumps({"world": str(path), "settings": list(SETTINGS), "meeting": MEETING}))
    expectation = json.loads(
        (args.folder / "expectation.json").read_text(encoding="utf-8")
    )  # read, never written
    sides = [str(expectation["sides"][label]) for label in expectation["sides"]]
    expectation[MEETING] = blind(expectation, sides)
    key = " ".join(SETTINGS)
    gate = {**expectation, "runs": {**expectation["runs"], key: expectation[MEETING]["world"]}}
    gate["comment"] = (
        f"The folder's blind with the back world, {expectation[MEETING]['world']} (the click that runs back over "
        f"three sides, `meeting: back`, the run back's reach the cone), in the ({', '.join(SETTINGS)}) run's place: the "
        "gate's blind for the reading of the four output files with the back world's among them and for its page; every "
        "number the folder's expectation.json's, written before any run. " + str(expectation["comment"])
    )
    beside = args.folder / f"expectation_{MEETING}.json"
    beside.write_text(json.dumps(gate, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"expectation": str(beside), "key": MEETING, "M": gate[MEETING]["M"], "runs": gate["runs"]}
        )
    )


if __name__ == "__main__":
    main()
