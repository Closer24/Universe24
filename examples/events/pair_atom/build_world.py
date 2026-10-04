"""The pair atom's builder (examples/events/pair_atom; ALGEBRA.md, the pair of two bound records, a hypothesis under its own name; the mathematician's derivation with the advisor's second, two hands): from the design beside this script it writes the toy universe (two equal constituents at matter's pair declared with no reads, the relative part at the pair the loader derives at the declared den, the pinned centre at the same pair, the sign holder under the rotation at the write weight the energy line fixes), the toy world (the open cube, the pinned centre at its centre and the relative part's one quantum beside it, the fixed-point lay) and the blind expectation, every number the loader's own or the derivation script's, written before any run and never touched after (the committed-worlds gate, tests/test_the_bound_body.py); with --modes the generator lays both bodies as one-Node records by name.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/pair_atom/build_world.py [--design <design>.json] [--folder <folder>] [--modes]
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any

from event_universe.loader.universe import composed_pair

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
UNIVERSE, WORLD = "pair.json", "positronium_toy.json"


def two_body() -> Any:
    """The derivation script, loaded by its path (tools/derivations/two_body.py)."""
    spec = importlib.util.spec_from_file_location(
        "two_body", ROOT / "tools" / "derivations" / "two_body.py"
    )
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def universe(design: dict[str, Any]) -> dict[str, Any]:
    """The toy universe: the content holders and the sign holder under the rotation, the two constituents, the relative part and the pinned centre at the derived pair."""
    pair, den, k_w = design["constituents"]["pair"], int(design["den"]), int(design["write_weight"])
    content = {"gravity": 1, "binding": 1}
    derived = {"relative_of": ["first", "second"], "den": den}
    return {
        "integers": design["integers"],
        "families": [
            {
                "name": "gravity",
                "pair": [6000, 6000],
                "reads": content,
                "held": {
                    "sources": ["form", "tensions"],
                    "level_weight": 1000,
                    "write_weight": 1,
                    "act": "pace",
                },
            },
            {
                "name": "charge",
                "pair": [6000, 6000],
                "reads": content,
                "held": {
                    "sources": ["wronskian"],
                    "level_weight": 1,
                    "write_weight": k_w,
                    "act": "rotation",
                },
            },
            {
                "name": "binding",
                "pair": [2400, 2401],
                "reads": content,
                "held": {"sources": ["form"], "level_weight": 1, "write_weight": 1, "act": "pace"},
            },
            {"name": "first", "pair": list(pair), "reads": {}, "dimension": 2},
            {"name": "second", "pair": list(pair), "reads": {}, "dimension": 2},
            {"name": "relative", "pair": derived, "reads": {**content, "charge": 1}, "dimension": 2},
            {"name": "pinned", "pair": derived, "reads": {**content, "charge": 1}, "dimension": 2},
        ],
    }


def world(design: dict[str, Any], folder: Path) -> dict[str, Any]:
    """The toy world: the open cube, the pinned centre's one quantum at the centre and the relative part's beside it along x, no NodeReader, the fixed-point lay."""
    centre = [int(v) for v in design["centre"]]
    beside = [centre[0] + 1, centre[1], centre[2]]
    return {
        "shape": design["shape"],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "ticks": int(design["ticks"]),
        "universe": str((folder / UNIVERSE).relative_to(ROOT))
        if folder.is_relative_to(ROOT)
        else UNIVERSE,
        "engine": "examples/events/engine_start.json",
        "bodies": [
            {"family": "pinned", "nodes": [{"node": centre, "count": 1}]},
            {"family": "relative", "nodes": [{"node": beside, "count": 1}]},
        ],
        "node_readers": [],
        "lay": design["lay"],
    }


def expectation(design: dict[str, Any]) -> dict[str, Any]:
    """The blind: the derived pairs by the loader's own function (the centre's pair labelled a derived number and no family of the toy file, which pins the centre at the relative part's pair), the inertia ratios, the toy's coupling, radius and binding from the files' integers, and the line's numbers against nature from the derivation script; every float rounded once to the digits printed."""
    pair, den = tuple(int(v) for v in design["constituents"]["pair"]), int(design["den"])
    relative, centre = composed_pair(pair, pair, den, True), composed_pair(pair, pair, den, False)
    script = two_body()
    m_record, m_relative = script.inertia(*pair), script.inertia(*relative)
    gamma = int(design["integers"]["node_clock"])
    alpha = 3 * math.sqrt(3) / (8 * math.pi) * int(design["write_weight"]) / gamma
    return {
        "relative_pair": list(relative),
        "centre_pair": list(centre),
        "centre_pair_status": "a derived number of the folder's derivation (the loader's composed_pair at the declared den, the centre's part of the two constituents) and no family of the toy file, which pins the centre at the relative part's pair, relative_pair above",
        "inertia_ratio_relative": round(m_relative / m_record, 4),
        "inertia_ratio_centre": round(script.inertia(*centre) / m_record, 4),
        "energy_line": int(design["integers"]["quantum_action"]) * relative[0]
        == int(design["write_weight"]) * gamma * den,
        "alpha_law": round(alpha, 5),
        "bohr_radius_links": round(math.sqrt(3) / (m_relative * alpha), 2),
        "binding_1s_rad_per_interval": round(m_relative * alpha * alpha / 6, 5),
        "binding_ratio_to_one_record": 0.5,
        "reduced_masses": [round(v, 6) for v in script.reduced_masses()],
        "ground_levels_hartree": [round(v, 6) for v in script.ground_levels()],
        "against_nature": [round(v, 4) for v in script.against_nature()],
        "nature": design["nature"],
        "rest_contents": [round(v, 4) for v in script.rest_contents()],
        "run": "nothing run; the world loads and waits for the experimenter at the owner's word",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument(
        "--modes", action="store_true", help="lay both bodies as one-Node records by the generator"
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    folder = args.folder.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    (folder / UNIVERSE).write_text(json.dumps(universe(design), indent=1) + "\n", encoding="utf-8")
    (folder / WORLD).write_text(json.dumps(world(design, folder)) + "\n", encoding="utf-8")
    (folder / "expectation.json").write_text(
        json.dumps(expectation(design), indent=1) + "\n", encoding="utf-8"
    )
    if args.modes:
        tool = [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(folder / WORLD)]
        subprocess.run([*tool, "--pixel", "0", "1", "--sense", "1", "-1"], check=True, cwd=ROOT)


if __name__ == "__main__":
    main()
