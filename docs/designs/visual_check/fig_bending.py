"""Figure: light beside a mass, the arrival Nodes on the screen (series K; DETECTOR).

The paper (row 13's ground; "the seven confirmations"): "light beside a
mass, series K, three worlds, the deflection 0.000 pixel, the delay 0.00
interval". Read from the click lines of the screen's pixels (`screen_y_z`
at x = 54): the clicks per pixel, their centroid in y and z (a reduced
pair), and the mean age the click carries; the control has no mass. The
lamp's Node is read from the run's resolved world file.
"""

from __future__ import annotations

import json
from collections import Counter
from fractions import Fraction

import matplotlib.pyplot as plt
from common import (
    DETECTOR,
    INK,
    MID,
    arguments,
    cost,
    events,
    fingerprint,
    fmt,
    mean,
    run_folder,
    save,
)

from event_universe.trimmed_record import refuse_trimmed_record

WORLDS = ("control", "mass", "heavy", "near")


def lamp_node(folder) -> list[int]:
    with (folder / "resolved_initialization.json").open(encoding="utf-8") as handle:
        world = json.load(handle)
    for event in world["measured"]:
        if "lamp" in event:
            return list(event["position"])
    raise SystemExit("no lamp")


def main() -> None:
    runs, out = arguments()
    fig, axes = plt.subplots(1, len(WORLDS), figsize=(13, 3.6))
    reference = None
    for ax, world in zip(axes, WORLDS, strict=True):
        folder = run_folder(runs, "lensing", world)
        lamp = lamp_node(folder)
        counts: Counter = Counter()
        ages: list[int] = []
        refuse_trimmed_record(folder)
        for line in events(folder, {"click"}):
            detector = line.get("detector") or ""
            if detector.startswith("screen_") and line.get("family") == "light":
                _, y, z = line["node"]
                counts[(int(y), int(z))] += 1
                ages.append(int(line["reading"]))
        total = sum(counts.values())
        cy = Fraction(sum(y * n for (y, _), n in counts.items()), total)
        cz = Fraction(sum(z * n for (_, z), n in counts.items()), total)
        age = mean(ages)
        if reference is None:
            reference = (cy, cz, age, total)
        dy, dz, dage = cy - reference[0], cz - reference[1], age - reference[2]
        print(
            f"{DETECTOR} lensing/{world}: lamp at {lamp}; {total} light clicks on {len(counts)} pixels; centroid y {fmt(cy)}, "
            f"z {fmt(cz)}; off the lamp's line y {fmt(cy - lamp[1])}, z {fmt(cz - lamp[2])}; mean age {fmt(age, 3)}; "
            f"against the control: y {fmt(dy, 3)} pixel, z {fmt(dz, 3)} pixel, age {fmt(dage, 3)} interval, count {total - reference[3]}; "
            f"fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        grid = [[0] * 41 for _ in range(41)]
        for (y, z), n in counts.items():
            grid[z][y] = n
        image = ax.imshow(grid, origin="lower", cmap="Greys", extent=(-0.5, 40.5, -0.5, 40.5))
        ax.axhline(lamp[2], color=MID, lw=0.6, ls=":")
        ax.axvline(lamp[1], color=MID, lw=0.6, ls=":")
        ax.plot([float(cy)], [float(cz)], "+", color=INK, ms=14, mew=1.5)
        ax.set_title(
            f"{world}: centroid y {float(cy):.3f}, z {float(cz):.3f}\nmean age {float(age):.2f}",
            fontsize=8,
        )
        ax.set_xlabel("screen y (pixel)")
        ax.set_xlim(lamp[1] - 12, lamp[1] + 12)
        ax.set_ylim(lamp[2] - 12, lamp[2] + 12)
        fig.colorbar(image, ax=ax, fraction=0.046, pad=0.03)
    axes[0].set_ylabel("screen z (pixel)")
    fig.suptitle(
        "Light beside a mass: the arrival pixels' clicks (DETECTOR); dotted the lamp's line, + the centroid",
        fontsize=10,
    )
    save(fig, out, "fig_bending")


if __name__ == "__main__":
    main()
