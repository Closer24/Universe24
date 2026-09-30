"""The two speeds' worlds (ALGEBRA.md, Nature's numbers enter the board only as clicks, the series' line 1) from the design file beside this script: two worlds of one board, light alone at the vacuum content, light alone at no vacuum content and the massless row's kick alone (each on its own universe file where the design names one), each one packet at the same wave number over every row with the far region of four columns backed by the receding face; their mode files by the message lay (tools/pixel_mode.py); and the blind expectation file, written before any run: the two bands of the universe file, the group velocity of each packet at the design's wave number and the intervals by which the kick's arrival precedes light's over the distance from the packet's centre to the region. Every number is the design's or the universe file's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/two_speeds/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from math import acos, cos, pi, sin
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]


def world(design: dict[str, Any], name: str) -> dict[str, Any]:
    """One world of the design: the board open along x with both x faces receding and periodic across, the named packet laid along x over every row, the far region over every row of its columns."""
    length, height = int(design["length"]), int(design["height"])
    packet = design["worlds"][name]
    first, last = design["region"]["columns"]
    return {
        "shape": [length, height, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "faces": [],
        "ticks": int(design["ticks"]),
        "universe": packet.get("universe", design["universe"]),
        "engine": design["engine"],
        "measured": [],
        "messages": [
            {
                "family": packet["family"],
                "along": "x",
                "wave": list(design["wave"]),
                "amplitude": int(packet["amplitude"]),
                "top": {"x": list(design["top"]), "y": [0, height - 1], "z": [0, 0]},
                "edge": {"x": int(design["edge"]), "y": 0, "z": 0},
            }
        ],
        "detectors": [
            {
                "name": design["region"]["name"],
                "positions": [
                    [x, y, 0] for x in range(int(first), int(last) + 1) for y in range(height)
                ],
            }
        ],
        "receding": design["receding"],
    }


def group_velocity(cos_omega_of_k: float, k: float, scale: float) -> float:
    """The group velocity d omega / d k of a band cos omega = 1 - scale (1 - cos k) / 3 along an axis, in Links per interval."""
    return scale * sin(k) / (3 * sin(acos(cos_omega_of_k)))


def expectation(design: dict[str, Any]) -> dict[str, Any]:
    """The blind expectation from the design and the universe file (ALGEBRA.md #the-paces, #what-is-open item 22): the massless row's band cos omega = 1 - (1 - cos k) / 3 and light's at the vacuum content x = c_vac / Gamma, cos omega = 1 - (1 - 2 x)^2 (1 - cos k) / 3; light at no vacuum content moves at the massless row's band, so light at the vacuum content arrives after it, and after the kick, by L (1 / v_light - 1 / v_kick) intervals, the kick and light at no vacuum content together, L from the packet's centre to the region's centre for the centroids and the peaks of the two readings and less the envelope's half-maximum half-width for their half-maximum onsets (the region narrow beside the packet)."""
    universe = json.loads((ROOT / design["universe"]).read_text(encoding="utf-8"))
    gamma = int(universe["integers"]["node_clock"])
    rows = {row["name"]: row for row in universe["families"]}
    rest = int(rows[design["worlds"]["kick"]["family"]]["held"]["rest"])
    kick = design["worlds"]["kick"]
    alone = json.loads((ROOT / kick.get("universe", design["universe"])).read_text(encoding="utf-8"))
    kick_row = next(row for row in alone["families"] if row["name"] == kick["family"])
    assert int(kick_row["held"]["rest"]) == rest and alone["integers"] == universe["integers"]
    p, q = design["wave"]
    k = pi * p / q
    x = rest / gamma
    kick_band = 1 - (1 - cos(k)) / 3
    light_band = 1 - (1 - 2 * x) ** 2 * (1 - cos(k)) / 3
    kick_speed = group_velocity(kick_band, k, 1.0)
    light_speed = group_velocity(light_band, k, (1 - 2 * x) ** 2)
    top, edge = design["top"], int(design["edge"])
    centre = (top[0] + top[1]) / 2
    first, last = design["region"]["columns"]
    region_centre = (first + last) / 2
    half_top = (top[1] - top[0]) / 2
    half_maximum = (
        half_top + edge * acos(2 * (0.5**0.5) - 1) / pi
    )  # the raised cosine's square at a half
    per_link = 1 / light_speed - 1 / kick_speed
    leads = {"light_0_before_light": per_link, "kick_before_light": per_link, "kick_before_light_0": 0.0}
    return {
        "comment": "Blind, written before any run: light at the vacuum content arrives at the far region after light at no vacuum content and after the massless row's kick by the intervals below, light reading the vacuum content in its paces (the advisor's 2 x L sqrt 3 is the long-wavelength limit of the same difference); the kick and light at no vacuum content arrive together, the massless row's own band. The reading: per world, the field line of the packet's family at the region, its half-maximum onset (the first interval at or above half the run's largest reading), the centroid of its bump at half maximum and its peak; each named difference of two worlds' onsets against its `onsets`, of their centroids against its `centroids` (the peaks beside: the crests' passage through the region moves a peak, and averages out over the bump). A light click at the region is the measurement and is counted beside; every field line is a GameBoard reading labelled so.",
        "verdict": "blind",
        "gamma": gamma,
        "vacuum_content": rest,
        "wave_number": [p, q],
        "band": {"kick": kick_band, "light": light_band},
        "group_velocity": {"kick": kick_speed, "light": light_speed},
        "distance": {
            "centroids": region_centre - centre,
            "onsets": region_centre - centre - half_maximum,
        },
        "differences": {
            key: {
                "worlds": list(design["differences"][key]),
                "centroids": (region_centre - centre) * lead,
                "onsets": (region_centre - centre - half_maximum) * lead,
                "long_wavelength": 2 * x * (region_centre - centre) * 3**0.5 * (lead != 0),
            }
            for key, lead in leads.items()
        },
        "worlds": {name: f"{name}.json" for name in design["worlds"]},
        "region": design["region"]["name"],
        "families": {name: packet["family"] for name, packet in design["worlds"].items()},
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes", action="store_true", help="write the mode files too (tools/pixel_mode.py)"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    for name in design["worlds"]:
        path = args.folder / f"{name}.json"
        document = world(design, name)
        path.write_text(json.dumps(document) + "\n", encoding="utf-8")
        if args.modes:
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
                check=True,
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
            )
        print(json.dumps({"world": str(path), "family": document["messages"][0]["family"]}))
    blind = args.folder / "expectation.json"
    blind.write_text(json.dumps(expectation(design), indent=1) + "\n", encoding="utf-8")
    print(json.dumps({"expectation": str(blind)}))


if __name__ == "__main__":
    main()
