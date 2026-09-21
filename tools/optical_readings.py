"""A GAMEBOARD diagnostic of `optical-v1`'s pin worlds (the chief
physicist's bounded diagnostic of 2026-09-21, record 483; never a detector
reading): the whole momentum **P** = Q d content **u**_D + **W** of the
beam's rows in their last intervals before the screen, read off the run's
`state.json` (the rows in flight at the run's end at x >= `--from-x`, the
label's direction, the amount, the content per unit and the push
accumulator `push`), and per world the mean of the transverse angle of
**P** about the beam's axis +x in the mass's plane (atan2(P_y, P_x) in
degrees, negative toward the mass), per row the angle of **P** against the
label's own (atan2(u_y, u_x)), and the ratio of the means at gamma = 1
over gamma = 0 per world name (2.00 by the arithmetic of verb 2, which
this reading reads back to itself: it says nothing about where the light
arrives; the detector reading is the screen's centroid,
`tools/lensing_readings.py`).

    PYTHONPATH=src python tools/optical_readings.py <runs of gamma 0> <runs of gamma 1> [--from-x 40]

Every number printed is labelled GAMEBOARD.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from event_universe.events.nature_beam import unit_label
from event_universe.events.world import Q


def rows_before_the_screen(run: Path, from_x: int) -> list[dict[str, object]]:
    state = json.loads((run / "state.json").read_text(encoding="utf-8"))
    found: list[dict[str, object]] = []
    for node in state["nodes"]:
        if node["position"][0] < from_x:
            continue
        for family in node["families"]:
            if family["family"] != "light":
                continue
            for ray in family["rays"]:
                found.append({**ray, "position": node["position"]})
    return found


def whole_momentum(ray: dict[str, object], denominator: int) -> tuple[list[int], list[int]]:
    """**P** = Q d content **u**_D + **W** and the label **u**_D of a row."""
    direction = tuple(int(v) for v in ray["direction"])  # type: ignore[union-attr]
    unit = list(unit_label(direction))  # type: ignore[arg-type]
    content = int(ray["amount"]) * int(ray["content"])  # type: ignore[arg-type]
    push = [int(v) for v in ray.get("push", [0, 0, 0])]  # type: ignore[union-attr]
    momentum = [Q * denominator * content * unit[a] + push[a] for a in range(3)]
    return momentum, unit


def angle_degrees(vector: list[int]) -> float:
    return math.degrees(math.atan2(vector[1], vector[0]))


def read_folder(folder: Path, from_x: int) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for run_dir in sorted(p for p in folder.iterdir() if (p / "run" / "run.json").is_file()):
        record = json.loads((run_dir / "run" / "run.json").read_text(encoding="utf-8"))
        optical = record.get("optical")
        if optical is None:
            continue
        denominator = int(record["suspension"][1])
        rays = rows_before_the_screen(run_dir / "run", from_x)
        if not rays:
            continue
        transverse: list[float] = []
        against_label: list[float] = []
        for ray in rays:
            momentum, unit = whole_momentum(ray, denominator)
            transverse.append(angle_degrees(momentum))
            against_label.append(angle_degrees(momentum) - angle_degrees(unit))
        name = str(record["model"])
        out[run_dir.name] = {
            "gamma": float(optical["gamma"]),
            "rows": float(len(rays)),
            "mean_transverse_degrees": sum(transverse) / len(transverse),
            "mean_against_label_degrees": sum(against_label) / len(against_label),
            "largest_against_label_degrees": max(against_label, key=abs),
        }
        print(
            f"GAMEBOARD {run_dir.name} ({name}, gamma {optical['gamma']}): {len(rays)} light rows at "
            f"x >= {from_x} in the final state; the transverse angle of P about +x, mean "
            f"{out[run_dir.name]['mean_transverse_degrees']:+.3f} degrees (negative toward the mass); "
            f"the angle of P against the label's, mean {out[run_dir.name]['mean_against_label_degrees']:+.3f} "
            f"degrees, largest {out[run_dir.name]['largest_against_label_degrees']:+.3f}"
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("folders", nargs="+", type=Path)
    parser.add_argument("--from-x", type=int, default=40)
    args = parser.parse_args()
    readings: dict[str, dict[str, float]] = {}
    for folder in args.folders:
        readings.update(read_folder(folder, args.from_x))
    by_name: dict[str, dict[float, float]] = {}
    for key, value in readings.items():
        base = key.rsplit("_g", 1)[0]
        by_name.setdefault(base, {})[value["gamma"]] = value["mean_transverse_degrees"]
    for base, means in sorted(by_name.items()):
        if 0.0 in means and 1.0 in means and means[0.0]:
            print(
                f"GAMEBOARD {base}: the mean transverse angle at gamma 1 over gamma 0 "
                f"{means[1.0] / means[0.0]:.3f} (2.00 by verb 2's arithmetic; a bookkeeping check, "
                "not a detector reading)"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
