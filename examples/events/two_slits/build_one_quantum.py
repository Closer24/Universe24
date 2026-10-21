"""The one-quantum two slits' world (ALGEBRA.md, The two slits' variants under the click's read, one quantum at a time; the derivation under papers/one_rule/variants/, section A; the owner's word of 2026-10-21) from the design file beside this script: the shipped two slits' world with one quantum laid in place of the beam, at a universe whose quantum action is the shipped T times 2^12, with every exit of the record a declared detector (the region `return` at the source's receding face) and the draw's window the whole passage; its universe file, its mode file by the packet lay (tools/pixel_mode.py) and its blind expectation file, the law's real line's shares of the one click per region, written from the design and no run. Every number is the design's or the generator's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/two_slits/build_one_quantum.py [--design <design>.json] [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "tools"))

from build_world import first_minima  # noqa: E402  # the two slits' own rule for the central maximum
from click_counts import extrema  # noqa: E402  # the one extrema rule, the reader's and the builder's

WORLD = "one_quantum"


def universe(design: dict[str, Any]) -> dict[str, Any]:
    """The universe file: the shipped light.json (`universe_from`) with its quantum action times `factor`, the energy line binding no family of this file; the product is the design's `quantum_action`, asserted."""
    document = json.loads((ROOT / design["universe_from"]).read_text(encoding="utf-8"))
    document["integers"]["quantum_action"] *= int(design["factor"])
    assert document["integers"]["quantum_action"] == int(design["quantum_action"]), design
    return document


def world(design: dict[str, Any], base: dict[str, Any]) -> dict[str, Any]:
    """The world file: the shipped two slits' world (`base`, two_slits.json beside this script) with the packet's amplitude and column the design's, the intervals and the draw's window the design's (130, the whole passage, one close), the universe the scaled one, and the region `return` appended, two columns deep at the source's receding face over every row, backed by that face as the screen is backed by its own."""
    found = json.loads(json.dumps(base))
    packet = found["packets"][0]
    packet["amplitude"] = int(design["amplitude"])
    packet["top"]["x"] = [int(design["column"]), int(design["column"])]
    found["intervals"] = int(design["intervals"])
    found["draw"] = {"window": int(design["window"])}
    found["universe"] = str(design["universe"])
    region = design["return"]
    rows = range(int(found["shape"][1]))
    found["node_detectors"].append(
        {
            "name": str(region["name"]),
            "positions": [[int(x), y, 0] for x in region["columns"] for y in rows],
        }
    )
    return found


def placed(document: dict[str, Any]) -> list[str]:
    """The regions in the page's order (tools/look/page.py, `reporters`): by the least row of their Nodes, then by name, the return region first and the screen's regions by their first row."""
    return [
        name
        for _row, name in sorted(
            (min(int(at[1]) for at in region["positions"]), str(region["name"]))
            for region in document["node_detectors"]
        )
    ]


def expectation(design: dict[str, Any], document: dict[str, Any]) -> dict[str, Any]:
    """The blind expectation file (NODEDETECTOR, as tools/click_counts.py and tools/look/page.py read it): the thirteen regions' shares of the one click over every exit as `counts`, in the page's order, the total 1 and the close; the shares within the screen with the maxima, the minima about the central maximum and the visibility there by the two slits' own rule; the exits' two shares; the fairness bound; the return's arrival; the fluctuation over worlds; one watch line at the central maximum's first row. Written from the design and no run."""
    blind = design["blind"]
    names = placed(document)
    within = [float(v) for v in blind["within_screen"]]
    first, last = (int(v) for v in blind["pattern"])
    maxima, minima = extrema(within, first, last)
    central, about = first_minima(within, maxima, minima)
    most, low = within[central], sum(within[at] for at in about)
    offset = names.index(f"screen_{first}")  # the screen's regions' bars after the return's
    return {
        "verdict": "NODEDETECTOR",
        "node_detector": names,
        "family": design["family"],
        "window": [1, int(blind["close"])],
        "across": "y",
        "pattern": [offset, offset + last - first],
        "comment": blind["comment"],
        "counts": [float(blind["per_region"][name]) for name in names],
        "through": int(blind["quanta"]),
        "quanta": int(blind["quanta"]),
        "close": int(blind["close"]),
        "exits": blind["exits"],
        "within_screen": within,
        "maxima": maxima,
        "minima": about,
        "central": central,
        "visibility": [round(most * len(about) - low, 4), round(most * len(about) + low, 4)],
        "scatter": blind["scatter"],
        "bias_bound": {
            "below": float(blind["bias_bound"]),
            "of": "a port's share, g / T, booked on the click's line",
        },
        "return_arrival": blind["return_arrival"],
        "watch": {str(blind["watch_row"]): float(blind["per_region"][f"screen_{central}"])},
        "status": "computed from the law's real line from the mode file's lay with every exit credited (papers/one_rule/variants/scripts/a_real_line.py, 2026-10-21), no run of the engine; the counts the shares of the one click, N = 1; fence: clicks",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--design", type=Path, default=HERE / f"{WORLD}.design.json", help="the design file"
    )
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the world written")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    scaled = args.folder / Path(str(design["universe"])).name
    scaled.write_text(json.dumps(universe(design), indent=1) + "\n", encoding="utf-8")
    base = json.loads((args.folder / str(design["base"])).read_text(encoding="utf-8"))
    document = world(design, base)
    path = args.folder / f"{WORLD}.json"
    path.write_text(json.dumps(document) + "\n", encoding="utf-8")
    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
        check=True,
        cwd=ROOT,
    )
    mode = json.loads(path.with_suffix(".mode.json").read_text(encoding="utf-8"))
    laid = sum(int(packet["count"]) for packet in mode["packets"])  # the generator's count, a reading
    print(json.dumps({"world": str(path), "universe": str(scaled), "laid": laid}))
    blind = expectation(design, document)
    target = args.folder / f"{WORLD}.expectation.json"
    target.write_text(json.dumps(blind, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps({"expectation": str(target), "counts": blind["counts"], "through": blind["through"]})
    )


if __name__ == "__main__":
    main()
