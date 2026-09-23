"""Figure: the orbit read by the lamp on the probe (series D3; DETECTOR and GAMEBOARD).

The paper (the conversion table; Table of what no rule forces): Kepler's
period on the plane, T(24) / T(12) = 1.997 in [1.82, 2.18] (D3, DETECTOR);
the pins T = 343 and 687. Read from the click lines of the detector line
(`line_<x>`): each click's x is the probe's x at the row's birth, the birth
tick the click's tick less the age it carries; the crossings of the centre
column in one direction, interpolated between two births (a reduced pair),
give the recurrence. The probe's escape is its own click on a face. The
GAMEBOARD panel is the probe's `step` lines (its path), a diagnostic.
"""

from __future__ import annotations

from fractions import Fraction

import matplotlib.pyplot as plt
from common import (
    DETECTOR,
    GAMEBOARD,
    INK,
    LIGHT,
    MID,
    arguments,
    cost,
    events,
    fingerprint,
    fmt,
    run_folder,
    save,
    style,
)

from event_universe.trimmed_record import refuse_trimmed_record

WORLDS = (("r12", 12), ("r24", 24))
CENTRE = 60


def read(folder):
    samples: list[tuple[int, int]] = []
    escape = None
    path: list[tuple[int, int]] = []
    probe = None
    refuse_trimmed_record(folder)
    for line in events(folder, {"click", "step"}):
        if line["event"] == "step":
            if probe is None:
                probe = line["number"]
            if line["number"] == probe:
                path.append((int(line["to"][0]), int(line["to"][1])))
            continue
        detector = line.get("detector") or ""
        if detector.startswith("line_"):
            samples.append((int(line["tick"]) - int(line["age"]), int(line["node"][0])))
        elif (
            detector.startswith("face")
            and line.get("measured") is not None
            and line.get("held") is not None
        ):
            escape = (detector, int(line["tick"]))
    samples.sort()
    return samples, escape, path


def crossings(samples, level: int, upward: bool) -> list[Fraction]:
    """The births' ticks at which x crosses the level in one direction, interpolated exactly."""
    found = []
    for (t0, x0), (t1, x1) in zip(samples, samples[1:], strict=False):
        crossed = (x0 < level <= x1) if upward else (x0 > level >= x1)
        if crossed and x1 != x0:
            found.append(Fraction(t0) + Fraction(level - x0, x1 - x0) * (t1 - t0))
    return found


def main() -> None:
    runs, out = arguments()
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    periods = {}
    for row, (world, radius) in enumerate(WORLDS):
        folder = run_folder(runs, "orbit_lamp", world)
        samples, escape, path = read(folder)
        xs = [x for _, x in samples]
        up = crossings(samples, CENTRE, True)
        down = crossings(samples, CENTRE, False)
        gaps = [b - a for a, b in zip(up, up[1:], strict=False)] + [
            b - a for a, b in zip(down, down[1:], strict=False)
        ]
        if gaps:
            periods[radius] = gaps[0]
        print(
            f"{DETECTOR} orbit_lamp/{world}: {len(samples)} clicks on the line, x from {min(xs)} to {max(xs)} "
            f"(the amplitude (max - min) / 2 = {fmt(Fraction(max(xs) - min(xs), 2), 1)}, the paper's pin {radius} in [{radius - 1}, {radius + 2}]); "
            f"crossings of x = {CENTRE} upward at ticks {[fmt(c, 1) for c in up]}, downward at {[fmt(c, 1) for c in down]}, the recurrence {[fmt(g, 1) for g in gaps]} "
            f"(the pin {343 if radius == 12 else 687} within 9 percent); the probe's escape {escape}; fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        print(f"{GAMEBOARD} orbit_lamp/{world}: {len(path)} steps of the probe, a diagnostic")
        left, right = axes[row]
        left.plot([p[0] for p in path], [p[1] for p in path], "-", color=MID, lw=0.8)
        left.plot([CENTRE], [CENTRE], "*", color=INK, ms=8)
        left.plot([CENTRE + radius], [CENTRE], "o", mfc="none", mec=INK)
        left.axhline(20, color=LIGHT, lw=1)
        left.set_aspect("equal")
        left.set_title(
            f"{world}: the probe's steps (GAMEBOARD, a diagnostic); the line of detectors at y = 20",
            fontsize=8,
        )
        left.set_xlim(0, 120)
        left.set_ylim(0, 120)
        style(left)
        right.plot([t for t, _ in samples], xs, "o", color=INK, ms=2.5)
        right.axhline(CENTRE, color=MID, lw=0.8, ls=":")
        for c in up + down:
            right.axvline(float(c), color=LIGHT, lw=1)
        if escape:
            right.axvline(escape[1], color=INK, lw=1, ls="--")
            right.text(escape[1], max(xs), f" escape {escape[0]} at {escape[1]}", fontsize=7, va="top")
        right.set_title(
            f"{world}: the clicks' x against the birth tick (DETECTOR); the recurrence {[round(float(g), 1) for g in gaps]}",
            fontsize=8,
        )
        right.set_xlabel("birth tick")
        right.set_ylabel("x of the click (Links)")
        style(right)
    if 12 in periods and 24 in periods:
        ratio = periods[24] / periods[12]
        print(
            f"{DETECTOR} T(24) / T(12) from the first recurrences = {fmt(ratio, 3)}; the paper's 1.997 in [1.82, 2.18]"
        )
    fig.suptitle("The orbit read by the lamp on the probe (series D3)", fontsize=10)
    save(fig, out, "fig_orbit")


if __name__ == "__main__":
    main()
