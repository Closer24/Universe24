"""The atom's seven worlds (ALGEBRA.md, The atom is a bound body of the holder of the sign, and Spin, closed for the paper as a route, The family's sign under exchange; the cold reader's verdicts of 2026-10-19 and the design verdict of the same day, sections 4 and 5) from the design file beside this script. The levels: each a cube open on its three axes with the proton laid at its centre as the one-Node pixel record and the electron declared at the centre's neighbour; `atom.json`, the ground at T 36,000,000 on the cube of 25, laid standing (the ground eigenvector of the well the holder writes, in the engine's phase convention, tools/standing_lay.py), `atom_free.json`, the control on the same board with the electron laid as the free lump (the same tool, `--lay gaussian`), `atom_1s.json` and `atom_2p.json` at T 72,000,000 on the cube of 33, the 1s and the 2p_x laid standing (`--level 1s`, `--level 2p`), and `atom_line.json`, the line, the 1s and the 2p_x summed at half a quantum each on the same cube (`--level 1s+2p`), run two beats. The shells: `atom_shells.json` and its control `atom_shells_symmetric.json`, a chain of 112 open on x with both faces receding, one body of four parts gu, gd, eu, ed declared a NodeDetector at two Nodes, one quantum in each ground part, four transitions g to e by the photon, no capacity, two photons of one quantum each from the two ends one window apart, on the anticoincidence folder's universe with the atom family at the dimension [4, 2] and its sign under exchange declared (`shells.json` antisymmetric, `shells_symmetric.json` symmetric, both written here); their mode files by the packet lay (tools/pixel_mode.py). With --modes the mode files are written too. The blind expectation file, written before any run from the design's numbers alone: per level the one check that says yes or no, the lay's profile, the rotation less the well's angle, the lump's inward breathing; the line's period and amplitude; the shells' weights at the two closes and the counts, the seed by the blind's rule; the beat and the law's units. Every number is the design's and stands in the files, none in this script or the engine.

Run with PYTHONPATH set to the checkout's src:

    PYTHONPATH=src python examples/events/atom/build_world.py [--design <design>.json] [--folder <folder>] [--modes] [--only <world> ...] [--seed N]
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


def world(design: dict[str, Any], row: dict[str, Any]) -> dict[str, object]:
    """One level's world: the cube open on x, y and z, the proton at the centre and the electron at its neighbour on +x, each one Node with the count 1, no NodeDetector, no draw, the intervals; the worlds of one universe and cube differ by their mode files alone."""
    cube = int(row["cube"])
    centre = cube // 2
    families = design["roles"]
    return {
        "shape": [cube, cube, cube],
        "boundary": {"x": "open", "y": "open", "z": "open"},
        "face_depth": 1,
        "intervals": int(row["intervals"]),
        "universe": row["universe"],
        "engine": design["engine"],
        "bodies": [
            {"family": families["source"], "nodes": [{"node": [centre, centre, centre], "count": 1}]},
            {
                "family": families["record"],
                "nodes": [{"node": [centre + 1, centre, centre], "count": 1}],
            },
        ],
        "node_detectors": [],
    }


def shells_universe(design: dict[str, Any], exchange: str) -> dict[str, Any]:
    """The shells' universe: the design's source universe read from the repository with the atom family's row at the design's dimension and the sign `exchange` declared under the key `exchange`; every other row unchanged."""
    shells = design["shells"]
    universe = json.loads((ROOT / str(shells["universe_from"])).read_text(encoding="utf-8"))
    for family in universe["families"]:
        if family["name"] == shells["family"]:
            family["dimension"] = list(shells["dimension"])
            family["exchange"] = exchange
    return dict(universe)


def shells_world(design: dict[str, Any], row: dict[str, Any], seed: int) -> dict[str, object]:
    """One shells world: the chain open on x with both faces receding, the body of the design's parts at its two Nodes with a transition from every ground part to every excited part by the photon at the design's weight and resonance, its generator at the seed (the window derived at load), no capacity; the two photons from the design's Nodes toward the body at the design's amplitude; the intervals."""
    shells = design["shells"]
    body, photons = shells["body"], shells["photons"]
    parts = [
        {"part": k, "name": str(name), "count": int(count)}
        for k, (name, count) in enumerate(body["parts"])
    ]
    transitions = [
        {
            "from": str(g),
            "to": str(e),
            "drive": photons["family"],
            "weight": int(body["weight"]),
            "resonance": [int(v) for v in body["resonance"]],
        }
        for g in body["grounds"]
        for e in body["excited"]
    ]
    record = {
        "family": shells["family"],
        "nodes": [{"node": [int(x), 0, 0], "weight": 1} for x in body["nodes"]],
        "parts": parts,
        "transitions": transitions,
        "rates": [],
        "node_detector": {**shells["generator"], "seed": seed},
    }
    packets = [
        {
            "family": photons["family"],
            "along": "x",
            "wave": [sign, int(photons["quarters"])],
            "phase": [0, 1],
            "amplitude": int(photons["amplitude"]),
            "top": {"x": [int(x), int(x)], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": int(photons["edge"]), "y": 0, "z": 0},
        }
        for x, sign in zip(photons["from"], (1, -1), strict=True)
    ]
    return {
        "shape": [int(shells["length"]), 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "intervals": int(shells["intervals"]),
        "universe": row["universe"],
        "engine": shells["engine"],
        "bodies": [record],
        "packets": packets,
        "node_detectors": [],
        "receding": {
            "x": {
                "sides": ["low", "high"],
                "largest": int(shells["largest"]),
                "layers": int(shells["layers"]),
            }
        },
    }


def expectation(design: dict[str, Any]) -> dict[str, object]:
    """The blind expectation file: per level the one check that says yes or no (a lattice reading, no click), the line's period and amplitude with the sign row's breathing, the shells' weights at the two closes and the counts with the seed by the blind's rule (clicks), the beat and the law's units; every number the design's, written before any run."""
    shells = design["shells"]
    worlds = {
        name: {"window": [int(v) for v in row["window"]], **design["blind"][name]}
        for name, row in design["worlds"].items()
    }
    for name, row in shells["worlds"].items():
        worlds[name] = {
            "window": [int(shells["closes"][0]), int(shells["closes"][1])],
            "exchange": row["exchange"],
            "universe": row["universe"],
            "seed": int(shells["seed"]),
            "seed_rule": shells["seed_rule"],
            "seed_candidates": [int(v) for v in shells["seed_candidates"]],
            **design["blind"][name],
        }
    return {
        "verdict": "LATTICE",
        "family": design["roles"]["record"],
        "comment": "The atom's blind (the cold reader's two verdicts of 2026-10-19 and the design verdict of the same day, sections 4 and 5), written before the folder's runs from the eigenproblem in doubles, the reader's probes at the same integers and the branch's test of the shell. The levels, lattice readings (no click): the ground at T 36M on the cube of 25, after 100 intervals the share of Q = SUM |z|^2 within r <= 4 over Q at 0.446 within 0.01 with the peak Node at the centre, the absolute share within each radius in units of the lay's Q_0 within 0.005 at r <= 6 together with the total Q within the walk's budget (the blind moved on 2026-10-19 before the folder's claim from its first form, the normalised profile within 0.005 at every radius, which an open cube read over 120 intervals cannot hold, the former bound kept by name), the rotation less the well's angle 0.835 within 0.002 at r 0, 2, 4, 6 (the eigenproblem's 0.8351, the free 0.8411), the peak level near 525; the free lump, the control, no fixed point, its share within r <= 4 from 0.42 to 0.53 at 40 and 0.51 at 60 with its centre level 260 to 635 to 593; the 1s at T 72M on the cube of 33, the share within r <= 2 at 0.666 within 0.01 at 60 with the peak at the centre, the centre level near 3,037, the rotation 0.7828 within 0.002 at r 0, 2, 4; the 2p_x, the share within r <= 8 at 0.509 within 0.01 at 60, the node plane x = 16 at 0.0000 exactly at every interval, the peak on the x axis at |x| 3 or 4, the rotation 0.8388 within 0.002 on the lobe. The line, a lattice reading (no click): the 1s and the 2p_x summed at half a quantum each on the cube of 33, 224 intervals, the dipole D(t) = SUM_i x_i |z_i|^2 / Q along x beating with the period 112 within 5 percent (the eigenproblem's beat 0.0560 per interval, the period 112.2) and the amplitude 0.75 Nodes within 20 percent (2 A_1 A_2 SUM x phi_1 phi_2 / Q on the eigenvectors, 0.748), Q within the walk's budget, and the electron's own row of the sign holder at the lobe breathing at the beat; nothing emitted, no light family in the universe. The shells, clicks of a toy atom: at the first close (60) both worlds read the same absorption list, 12,304,515,357,518,400 into either excited part and the rest 8,003,945,008,567,134; at the second close (93) the antisymmetric record's weight into the populated excited part is 0 exactly and the empty part's 9,190,267,331,637,924, the second photon entering the empty part or passing and no count above 1, while the symmetric control's weight into the populated part is 64,961,076,134,244,168, twice the unsigned weight and the larger, the piling to [0, 0, 2, 0] or [0, 0, 0, 2]; the seed the first of the test's seeds at which the antisymmetric record's second photon enters the empty part, named by the rule's own runs before the folder's run and the same for the control. Status: the levels and the line computed from the law's gauge-flat line and the engine's own well, the shells from the branch's test; a reading that misses the blind is a finding, written as such.",
        "radii": design["radii"],
        "worlds": worlds,
        "beat": design["blind"]["beat"],
        "law_units": design["blind"]["law_units"],
        "status": "the levels and the line lattice readings: no NodeDetector, no click, no draw; the shells clicks of a toy atom with the photon's resonance declared; the numbers are the lattice's own at Gamma 6,000 and T 36,000,000 or 72,000,000 and not nature's (the toy's alpha 0.138 and 0.276, nineteen and thirty-eight times nature's)",
        "fence": "lattice for the levels and the line, clicks for the shells",
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json", help="the design file")
    parser.add_argument("--folder", type=Path, default=HERE, help="the folder of the worlds written")
    parser.add_argument(
        "--modes",
        action="store_true",
        help="write the mode files too (tools/standing_lay.py, tools/pixel_mode.py)",
    )
    parser.add_argument(
        "--only", nargs="*", default=None, help="the worlds to write (every world without it)"
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="the shells' seed in place of the design's (the rule's confirmation runs)",
    )
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    families = design["roles"]
    for name, row in design["worlds"].items():
        if args.only is not None and name not in args.only:
            continue
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(world(design, row)) + "\n", encoding="utf-8")
        if args.modes:
            command = [
                sys.executable,
                str(ROOT / "tools" / "standing_lay.py"),
                "--input",
                str(path),
                "--record",
                families["record"],
                "--source",
                families["source"],
                "--sense",
                str(int(design["sense"])),
                "--lay",
                str(row["lay"]),
            ]
            if row["lay"] == "gaussian":
                command += ["--sigma", str(row["sigma"])]
            else:
                command += ["--level", str(row["level"])]
            subprocess.run(command, check=True, cwd=ROOT)
        print(json.dumps({"world": str(path), "lay": row["lay"], "level": row.get("level")}))
    shells = design["shells"]
    seed = int(shells["seed"]) if args.seed is None else int(args.seed)
    for name, row in shells["worlds"].items():
        if args.only is not None and name not in args.only:
            continue
        universe = args.folder / Path(str(row["universe"])).name
        universe.write_text(
            json.dumps(shells_universe(design, str(row["exchange"]))) + "\n", encoding="utf-8"
        )
        path = args.folder / f"{name}.json"
        path.write_text(json.dumps(shells_world(design, row, seed)) + "\n", encoding="utf-8")
        if args.modes:
            subprocess.run(
                [sys.executable, str(ROOT / "tools" / "pixel_mode.py"), "--input", str(path)],
                check=True,
                cwd=ROOT,
                stdout=subprocess.DEVNULL,
            )
        print(
            json.dumps(
                {
                    "world": str(path),
                    "universe": str(universe),
                    "exchange": row["exchange"],
                    "seed": seed,
                }
            )
        )
    written = expectation(design)
    (args.folder / "expectation.json").write_text(json.dumps(written, indent=1) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {"expectation": str(args.folder / "expectation.json"), "worlds": list(written["worlds"])}
        )
    )


if __name__ == "__main__":
    main()
