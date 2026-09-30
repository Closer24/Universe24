"""The builder of the train under the whole line (the advisor, #1515 comment 5910272948, B; ALGEBRA.md row (g)): from a design file (`design.json` beside it, every number of the world), one world per N, a flat board with one packet of the light family carrying N wholes (its amplitude the design's for that N), the wall an inner face with two gaps, the screen a slab of groups of rows with no declared remainders (under the whole line the click is the whole's entry), the far face receding; and the blind expectation file per N (the pattern's shares per group, the extrema and the visibility the reader compares, the tolerances, the deviation's two lines). Every number of the world is the design's and stands in the world files, none in the engine.

Run from the checkout with PYTHONPATH set to its src:

    PYTHONPATH=src python examples/events/two_slits_wholes/build_world.py [--design <design>.json] [--folder <folder>] [--name <name>]

then lay the packet with the generator, `PYTHONPATH=src python tools/pixel_mode.py --input <world>.json`, for each world written.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent


def world(design: dict[str, Any], wholes: str) -> dict[str, object]:
    """The world file from the design for N = `wholes`: the board, the packet (a flat top of one Node with the raised-cosine edges, the amplitude the design's for N), the wall with its gaps, the screen's groups (each `rows_per_group` rows over the slab), the far face receding as the design's `receding` key declares (the world's key, passed as written), the ticks."""
    packet, slab, height = design["packet"], int(design["slab"]), int(design["height"])
    gaps = [{"y": list(gap), "z": [0, 0]} for gap in design["gaps"]]
    centre, row = int(packet["centre"]), int(packet["row"])
    message = {
        "family": design["family"],
        "along": "x",
        "wave": list(design["wave"]),
        "amplitude": int(design["amplitude"][wholes]),
        "top": {"x": [centre, centre], "y": [row, row], "z": [0, 0]},
        "edge": {"x": int(packet["edge_along"]), "y": int(packet["edge_across"]), "z": 0},
    }
    columns = range(int(design["screen"]), int(design["screen"]) + slab)
    detectors = []
    for first in range(0, height, int(design["rows_per_group"])):
        rows = range(first, first + int(design["rows_per_group"]))
        positions = [[x, y, 0] for y in rows for x in columns]
        detectors.append({"name": f"rows {rows[0]} to {rows[-1]}", "positions": positions})
    return {
        "shape": [int(design["length"]), height, 1],
        "boundary": {"x": "open", "y": "open", "z": "periodic"},
        "face_depth": 1,
        "faces": [{"axis": "x", "at": int(design["wall"]), "gaps": gaps}],
        "ticks": int(design["ticks"]),
        "universe": design["universe"],
        "engine": design["engine"],
        "measured": [],
        "messages": [message],
        "detectors": detectors,
        "receding": design["receding"],
    }


def extrema(row: list[float]) -> tuple[list[int], list[int]]:
    """The local maxima and minima of a row: a position above both neighbours (a maximum) or below both (a minimum), the ends compared with their one neighbour; as tools/click_counts.py reads them."""
    maxima, minima = [], []
    for at, value in enumerate(row):
        near = [row[at - 1]] if at > 0 else []
        near += [row[at + 1]] if at < len(row) - 1 else []
        if all(value > other for other in near):
            maxima.append(at)
        if all(value < other for other in near):
            minima.append(at)
    return maxima, minima


def expectation(design: dict[str, Any], wholes: str, names: list[str]) -> dict[str, object]:
    """The blind expectation file for N = `wholes`, as tools/click_counts.py reads it: the groups, the pattern's shares per group, the total through the gaps, the pattern's range, its extrema and its visibility at the middle maximum against the minima, and the advisor's tolerances, the one entry per whole and the deviation's two lines."""
    blind = design["blind"]
    counts = [float(value) for value in blind[wholes]["counts"]]
    maxima, minima = extrema(counts)
    most = counts[maxima[len(maxima) // 2]]
    low = sum(counts[at] for at in minima)
    return {
        "comment": f"The blind expectation of the train under the whole line for N = {wholes} wholes (the advisor, #1515 comment 5910272948, B; ALGEBRA.md row (g)), written before the run from design.json: DETECTOR. The pattern's shares per group of four rows (`counts`, {blind[wholes]['through']} through the gaps, {blind[wholes]['fraction']} of the packet); the whole line's entries within {blind['tolerance']['group']} of them per group and within {blind['tolerance']['sum']} in the sum; exactly {blind['entries_per_whole']} entry per whole, never two, and no whole in two groups; the summed absolute deviation of the groups' entries from the pattern's shares over the total about {blind['deviation']['deterministic']} under the deterministic line against about {blind['deviation']['draw']} under a draw at N = 3,000: the run reads which of the two the law's flow is.",
        "verdict": "DETECTOR",
        "family": design["family"],
        "across": "y",
        "detector": names,
        "wholes": int(wholes),
        "counts": [int(value) if value == int(value) else value for value in counts],
        "through": blind[wholes]["through"],
        "fraction": blind[wholes]["fraction"],
        "pattern": [0, len(counts) - 1],
        "maxima": maxima,
        "minima": minima,
        "visibility": [most * len(minima) - low, most * len(minima) + low],
        "tolerance": blind["tolerance"],
        "entries_per_whole": blind["entries_per_whole"],
        "deviation": blind["deviation"],
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument("--name", default="two_slits_wholes", help="the worlds' name; each adds _N")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for wholes in design["amplitude"]:
        document = world(design, wholes)
        path = args.folder / f"{args.name}_{wholes}.json"
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        names = [str(detector["name"]) for detector in document["detectors"]]  # type: ignore[index]
        blind = args.folder / f"expectation_{wholes}.json"
        blind.write_text(
            json.dumps(expectation(design, wholes, names), indent=1) + "\n", encoding="utf-8"
        )
        summary = {"world": str(path), "expectation": str(blind), "shape": document["shape"]}
        print(json.dumps({**summary, "wholes": int(wholes), "ticks": document["ticks"]}))


if __name__ == "__main__":
    main()
