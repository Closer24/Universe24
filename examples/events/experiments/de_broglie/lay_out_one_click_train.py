"""THE ONE-CLICK TRAIN, the fixture of the corrected giving (the Closer's word of 2026-09-28, 13:34 Israel time, for Newton's PR of the giving that writes both levels): the one-click world of `lay_out_one_click.py` with the giver's charge q = 1 on the body (Cheshbon's line of 13:27: a body without q gives no light; the key on the giver) and the universe of the first look with the quantum's action T written, so that the generator reads the train of one quantum on the form (N_q = 29.5 periods at E_s(charge) = 300,000) and the loop closes the window at the interval the train names; the light's rows read every interval so that the reader `one_click_train.py` counts the wavelength and the train along the beam. The expectation before the run (Cheshbon 13:16 and 13:18 Israel time): the train 29.5 +- 0.5 periods of the giver's clock (236 intervals at the period 8), the given record a wave of wavelength 4 with the light's amplitude a_light = 16,114 levels on a face of one Node (a per face falls as one over the root of the face's Nodes: 9,303 on this giver's face of three), the group velocity 0.447 Links per interval at wavelength 4, the strip's click at the distance over that velocity after the close, and the reversible row MATCH over the whole run. No number of a run enters here; nothing runs here. Run from the repository root: python examples/events/experiments/de_broglie/lay_out_one_click_train.py [--out <folder>]; the three files are written under this folder and nothing else."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from lay_out_one_click import TICKS, WINDOW_X, one_click
from lay_out_two_slits import ROOT, universe_of_the_first_look

HERE = Path(__file__).resolve().parent
WORLD_NAME = "one_click_train"
UNIVERSE_NAME = "universe_train.json"
QUANTUM_ACTION = 45_655_451_855  # T, the files' number (the norm over the pace of the record's giver)
GIVER_CHARGE = 1  # q on the giver: a body without q gives no light (Cheshbon 13:27)
PERIOD = (
    8  # the giver's clock period in intervals, the mode's reading `period` on the universe of record
)
TRAIN_PERIODS = (
    29.5  # N_q, the generator's `train` on the form at E_s(charge) = 300,000 (Cheshbon 07:12Z)
)
TRAIN_BAND_PERIODS = 0.5
WAVELENGTH = 4  # Links, cos k = 3 cos omega_b - 2 = 0 on the light band from [2, 3]
WAVELENGTH_BAND = 0.5
GROUP_VELOCITY = 0.447  # sin k / (3 sin omega) at wavelength 4 (Cheshbon 13:16)
GROUP_VELOCITY_BAND = 0.05  # the Experimenter's band on the centroid's reading
A_LIGHT_ONE_NODE_FACE = (
    16_114  # the light's amplitude for the train of 29.5 periods on a face of one Node
)
FACE_NODES = 3  # the giver's far face in this world, three Nodes


def universe_of_the_train(folder: Path) -> str:
    """The universe of the first look with the quantum's action T written; the path the world names."""
    first_look = ROOT / universe_of_the_first_look(folder)
    document = json.loads(first_look.read_text(encoding="utf-8"))
    document["integers"]["quantum_action"] = QUANTUM_ACTION
    path = folder / UNIVERSE_NAME
    path.write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    return path.resolve().relative_to(ROOT).as_posix()


def one_click_train(folder: Path) -> dict[str, Any]:
    """The one-click world with q on the giver, the universe of the train, and the light's rows every interval."""
    document = one_click(folder)
    document["universe"] = universe_of_the_train(folder)
    document["measured"][0]["q"] = GIVER_CHARGE
    for reading in document["readings"]:
        if reading["name"] in ("light_rows", "light_support"):
            reading["every"] = 1
    return document


def expectation() -> dict[str, Any]:
    """The blind expectation of the train: Cheshbon's numbers before the run and their bands, the reversible row over the whole run; no number of a run."""
    a_face = round(A_LIGHT_ONE_NODE_FACE / FACE_NODES**0.5)
    return {
        "format": "world-expectation-v1",
        "status": "BLIND: the fixture of the corrected giving; Cheshbon's numbers before the run; no number of a run here",
        "row": "ALGEBRA.md the giving's row: the window writes both levels of the giver's rotation into the given record at the giver's Nodes each interval of the window, so the given record is a wave of the light band's wave number at the giver's clock, and the window closes when the outward flux reaches T; the train is N_q periods of the giver's clock, read by the generator on the form and by the loop at the close",
        "DETECTOR": [],
        "blind": {
            "row": "Cheshbon's numbers of 13:16 and 13:18 Israel time (2026-09-28) before the run; the bands are the expectation's, MATCH inside and MISS outside",
            "train_periods": TRAIN_PERIODS,
            "train_band_periods": TRAIN_BAND_PERIODS,
            "train_intervals": round(TRAIN_PERIODS * PERIOD),
            "period_intervals": PERIOD,
            "wavelength_links": WAVELENGTH,
            "wavelength_band_links": WAVELENGTH_BAND,
            "group_velocity_links_per_interval": GROUP_VELOCITY,
            "group_velocity_band": GROUP_VELOCITY_BAND,
            "a_light_one_node_face": A_LIGHT_ONE_NODE_FACE,
            "a_light_this_face": a_face,
            "click_at_the_strip": "the distance from the giver's far face to the window over the group velocity, intervals after the close",
            "window_x": WINDOW_X,
        },
        "GAMEBOARD": [
            {
                "reversible": TICKS,
                "row": "the whole run forward and back on a fresh copy, every row bit for bit, the click keeps the click; a diagnostic, MATCH or MISS with the first interval and Node that deviate",
            }
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE, help="the folder the files are written into")
    args = parser.parse_args()
    folder = args.out.resolve()
    folder.mkdir(parents=True, exist_ok=True)
    document = one_click_train(folder)
    (folder / f"{WORLD_NAME}.json").write_text(json.dumps(document, indent=1) + "\n", encoding="utf-8")
    (folder / f"{WORLD_NAME}.expectation.json").write_text(
        json.dumps(expectation(), indent=1) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "world": str(folder / f"{WORLD_NAME}.json"),
                "universe": document["universe"],
                "q": GIVER_CHARGE,
            }
        )
    )


if __name__ == "__main__":
    main()
