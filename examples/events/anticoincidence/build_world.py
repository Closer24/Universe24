"""The anticoincidence world's builder (the paper's S.57, one photon on two bodies; ALGEBRA.md (h2); the mathematician's 144 and 145; the owner's word of 2026-10-03, 03:25): from `design.json` it writes `one_photon.json`, a chain open on x with both faces receding, two records of two parts (g at the count 1, e at 0) declared NodeReaders at one Node each at the same distance on either side of the centre, and one light record of the family `photon` laid at the centre as two packets toward the two records, the whole one quantum, each record absorption it into e at the transition's declared weight over its one window of `intervals`, the run going on for `intervals` past the window's close so that the absorption's hole and the erasing front stand in the output interval by interval and the front reaches both packets (the owner's word of 2026-10-04, the click's experiment; the redesign at the lay without the uniform mode, the edge one wavelength on the chain of 96); and `two_photons.json`, the control, the same two packets at the control's amplitude on the universe `two_atoms_two_records.json`: two photons, one per record (two massless families of one pair), each atom's transition into e by either, each absorption bringing its record to 0 and its front starting at the absorption's interval (the design's `control`); and the blind `expectation.json`: P(A only) = P(B only) = s, P(both) = 0, alpha = 0 for one quantum; the control P(both) above 0. With `--modes` it lays the light by the generator. Every number is the design's; the engine reads none of it.

PYTHONPATH=src python examples/events/anticoincidence/build_world.py --modes [--folder <folder>]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "tools"))


def world_of(design: dict, amplitude: int, control: dict | None = None) -> dict:
    """One world: the two records and the two packets at the amplitude given; the control (the design's `control`, its `universe` and its `families`, one massless family per packet, the +x packet's first) lays each packet as its own record and gives each atom a transition into e by either."""
    length = design["length"]
    lights = list(control["families"]) if control else [design["light"]["family"]] * 2
    records = []
    for at in design["records"]["nodes"]:
        records.append(
            {
                "family": design["records"]["family"],
                "nodes": [{"node": [at, 0, 0], "weight": 1}, {"node": [at + 1, 0, 0], "weight": 1}],
                "parts": [
                    {"part": 0, "name": "g", "role": "ground", "count": 1},
                    {"part": 1, "name": "e", "role": "excited", "count": 0},
                ],
                "transitions": [
                    {
                        "from": "g",
                        "to": "e",
                        "drive": light,
                        "weight": design["records"]["weight"],
                        "resonance": design["resonance"],
                    }
                    for light in dict.fromkeys(lights)
                ],
                "rates": [],
                "node_reader": {
                    **design["generator"],
                    "window": design["intervals"],
                    "seed": design["records"]["seed"],
                },
            }
        )
    centre, edge = design["light"]["centre"], design["light"]["edge"]
    packets = [
        {
            "family": light,
            "along": "x",
            "wave": [sign, design["light"]["quarters"]],
            "phase": [0, 1],
            "amplitude": amplitude,
            "top": {"x": [centre[k], centre[k]], "y": [0, 0], "z": [0, 0]},
            "edge": {"x": edge, "y": 0, "z": 0},
        }
        for light, (k, sign) in zip(lights, ((1, 1), (0, -1)), strict=True)
    ]
    return {
        "shape": [length, 1, 1],
        "boundary": {"x": "open", "y": "periodic", "z": "periodic"},
        "face_depth": 1,
        "intervals": design["intervals"],  # the run goes on past the window's close: the front spreads
        "universe": control["universe"] if control else design["universe"],
        "engine": design["engine"],
        "bodies": records,
        "packets": packets,
        "node_readers": [],
        "receding": {
            "x": {"sides": ["low", "high"], "largest": design["largest"], "layers": design["layers"]}
        },
    }


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--design", type=Path, default=HERE / "design.json")
    parser.add_argument("--folder", type=Path, default=HERE)
    parser.add_argument("--modes", action="store_true", help="lay the light by the generator")
    args = parser.parse_args(argv)
    design = json.loads(args.design.read_text(encoding="utf-8"))
    args.folder.mkdir(parents=True, exist_ok=True)
    control = design.get("control")  # the control's universe and families, its world by name
    for name, amplitude in design["worlds"].items():
        path = args.folder / f"{name}.json"
        own = control if control and control["world"] == name else None
        path.write_text(json.dumps(world_of(design, int(amplitude), own)) + "\n", encoding="utf-8")
        if args.modes:
            import pixel_mode

            pixel_mode.main(["--input", str(path)])
    expectation = {
        "verdict": "NODEREADER",
        "comment": "One photon on two bodies, the anticoincidence (the paper's S.57; ALGEBRA.md (h2); the mathematician's 144 and 145, two hands by the law as it stands): one light record of one whole quantum laid between two records declared NodeReaders at one Node each, equidistant, each reading the light into its e part over one window, the run; the credit's count per record, one quantum one click; written before any run and never edited after.",
        "trials": len(design["seeds"]),
        "intervals": design["intervals"],
        "blind": {
            "one_photon": {
                "reading": "over the trials the fraction with an absorption at the record A alone, at B alone, at both and at neither (tools/meeting_trials.py, the jump lines), and alpha = P(both) / (P(A) P(B))",
                "blind": "P(A only) = P(B only) = s with s at most 1 / 2, exact by the lay's symmetry (each packet as far from its atom as the other) and the seeds' draw alone, P(both) = 0 exactly, alpha = 0 (independent draws, classical light, would give 1)",
                "status": "derived from the credit's one draw per record and the count conserved (S.57 (b)); the share s the two-mode line's transfer over the passage at the declared weight, not predicted here",
                "fence": "clicks",
            },
            "two_photons": {
                "reading": "the same over the control's trials",
                "blind": "P(both) above 0: two quanta, two absorptions possible, alpha 1 / 2 in S.57 (c)'s form (the ordered pairs), 1 for two independent sequential absorptions at the same share",
                "status": "S.57 (c), the control of two quanta",
                "fence": "clicks",
            },
        },
    }
    (args.folder / "expectation.json").write_text(
        json.dumps(expectation, indent=1) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
