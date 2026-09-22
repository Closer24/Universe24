"""Figure: the two slits under the birth wheel, the clicks per pixel (series L2, L2b; DETECTOR).

The paper (NATURE row 2a; the conversion table): Young's fringes in the
clicks of `slits_huygens` (4096 births): the dark pixels 0 to 3 clicks,
the bright about 40 to 51, the bands 23.5 pixels apart, the visibility
0.966; `slits_low` the same geometry at 64 births. Read from the gather
lines: the set chosen per birth ordinal, counted per screen pixel; the
grey steps are the first record's rungs (its `cells`, the widths in the
wheel's unit), the counts the wheel is expected to produce (also on the
gather line, DETECTOR). The wall's absorbers and the faces are counted
apart. No cosine is computed here: the picture shows the fringes or not.
"""

from __future__ import annotations

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
    run_folder,
    save,
    style,
)
from gathers import chosen_by_ordinal

WORLDS = (("slits_huygens", 4096), ("slits_low", 64))


def pixel(name: str) -> int | None:
    return int(name.split("_")[1]) if name.startswith("screen_") else None


def first_rungs(folder) -> tuple[dict[int, Fraction], int]:
    """The first record's cells: the width per screen pixel over the wheel's unit."""
    for line in events(folder, {"gather"}):
        cells = line["cells"]
        unit = int(cells[-1][1])
        widths: dict[int, Fraction] = {}
        previous = 0
        for chosen, rung in cells:
            width = int(rung) - previous
            previous = int(rung)
            y = pixel(chosen[0][0])
            if y is not None and width:
                widths[y] = Fraction(width, unit)
        return widths, unit
    raise SystemExit("no gather line")


def dark_runs(counts: Counter, births: int) -> list[tuple[int, int]]:
    """The runs of dark pixels (at most 3 clicks) inside the lit range (pixels with at least 8 clicks at both ends)."""
    lit = [y for y in range(121) if counts[y] >= 8 * births // 4096]
    if not lit:
        return []
    runs, start = [], None
    for y in range(min(lit), max(lit) + 1):
        dark = counts[y] <= 3 * births // 4096
        if dark and start is None:
            start = y
        if not dark and start is not None:
            runs.append((start, y - 1))
            start = None
    if start is not None:
        runs.append((start, max(lit)))
    return runs


def main() -> None:
    runs, out = arguments()
    panels = []
    for world, births in WORLDS:
        try:
            folder = run_folder(runs, "amplitude", world)
        except SystemExit as missing:
            print(f"missing {missing}")
            continue
        chosen = chosen_by_ordinal(folder, births)
        counts: Counter = Counter()
        wall = faces = 0
        for c in chosen.values():
            y = pixel(c[0][0])
            if y is None:
                if c[0][0].startswith("face"):
                    faces += 1
                else:
                    wall += 1
            else:
                counts[y] += 1
        widths, unit = first_rungs(folder)
        runs_dark = dark_runs(counts, births)
        centres = [Fraction(a + b, 2) for a, b in runs_dark]
        gaps = [b - a for a, b in zip(centres, centres[1:], strict=False)]
        print(
            f"{DETECTOR} {world}: {len(chosen)} records read of {births}; screen {sum(counts.values())} clicks on "
            f"{len(counts)} pixels, wall {wall}, faces {faces}; the counts y = 0 .. 120: "
            + " ".join(str(counts[y]) for y in range(0, 121))
        )
        print(
            f"{DETECTOR} {world}: the dark runs (at most 3 clicks) inside the lit range at y = {runs_dark}, "
            f"their centres {[str(c) for c in centres]}, the gaps between them {[str(g) for g in gaps]} pixels; "
            f"the paper's bands 23.5 pixels apart; the wheel's unit {unit}; fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        panels.append((world, births, counts, widths))
    fig, axes = plt.subplots(len(panels), 1, figsize=(11, 2.8 * len(panels)), squeeze=False)
    for ax, (world, births, counts, widths) in zip(axes[:, 0], panels, strict=True):
        ys = range(0, 121)
        ax.step(
            ys,
            [float(widths.get(y, 0) * births) for y in ys],
            where="mid",
            color=MID,
            lw=1,
            label="the first record's rungs x births (DETECTOR, the gather line)",
        )
        ax.bar(
            list(counts),
            [counts[y] for y in counts],
            color=INK,
            width=0.8,
            label="clicks per pixel (DETECTOR)",
        )
        ax.set_xlim(-1, 121)
        ax.set_ylabel("clicks")
        ax.set_title(f"{world}: {births} births, the screen's 121 pixels", fontsize=9)
        ax.legend(fontsize=7, loc="upper right")
        style(ax)
    axes[-1, 0].set_xlabel("screen pixel y")
    fig.suptitle("Two slits: the pixel chosen per record, counted (DETECTOR)", fontsize=10)
    save(fig, out, "fig_two_slits")


if __name__ == "__main__":
    main()
