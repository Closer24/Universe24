"""Figure: the atom's baseline, hydrogen at r = 12 as the law stands (branch atom-baseline-run; DETECTOR and GAMEBOARD).

The baseline run (docs/designs/atom_baseline/RUN.md at 01e86183): the loop
does not stay; the electron widens every quarter turn (the crossings at
13, 13, 17 and 26 Links) and leaves through `face:+y` at count 3407; the
dwell about 20 counts per Link near r = 12. Read from the click lines of
the four side faces for the family `e`: a `face:+x` or `face:-x` click
carries the electron's y (the row flew along x), a `face:+y` or `face:-y`
click its x; the electron's own escape is its click with `held`. The
GAMEBOARD panel is the electron's `step` lines (its path), a diagnostic.
"""

from __future__ import annotations

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
    run_folder,
    save,
    style,
)

ELECTRON = 2
CENTRE = 26


def main() -> None:
    runs, out = arguments()
    folder = run_folder(runs, "atoms", "hydrogen_r12")
    by_face: dict[str, list[tuple[int, int]]] = {}
    path = []
    escape = None
    for line in events(folder, {"click", "step"}):
        if line["event"] == "step":
            if line["number"] == ELECTRON:
                path.append((int(line["to"][0]), int(line["to"][1])))
            continue
        if line.get("family") != "e":
            continue
        detector = line.get("detector") or ""
        if line.get("held") is not None:
            escape = (detector, int(line["tick"]), list(line["node"]))
            continue
        if detector in ("face:+x", "face:-x"):
            by_face.setdefault(detector, []).append((int(line["tick"]), int(line["node"][1])))
        elif detector in ("face:+y", "face:-y"):
            by_face.setdefault(detector, []).append((int(line["tick"]), int(line["node"][0])))
    for face in sorted(by_face):
        coords = [c for _, c in by_face[face]]
        print(
            f"{DETECTOR} atoms/hydrogen_r12 {face}: {len(by_face[face])} clicks of e, the coordinate carried from {min(coords)} to {max(coords)} "
            f"(the proton's Node at {CENTRE}: the farthest {max(abs(c - CENTRE) for c in coords)} Links)"
        )
    print(
        f"{DETECTOR} atoms/hydrogen_r12: the electron's escape {escape}; the baseline's face:+y at 3407"
    )
    print(
        f"{GAMEBOARD} atoms/hydrogen_r12: {len(path)} steps of the electron, from {path[0]} to {path[-1]}, a diagnostic; "
        f"fingerprint {fingerprint(folder)}; {cost(folder)}"
    )
    fig, (left, right) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1, 1.4]})
    left.plot([p[0] for p in path], [p[1] for p in path], "-", color=MID, lw=0.8)
    left.plot([CENTRE], [CENTRE], "*", color=INK, ms=9, label="the proton's Node")
    left.add_patch(
        plt.Circle((CENTRE, CENTRE), 12, fill=False, ls=":", color=LIGHT, label="r = 12 (drawn)")
    )
    left.set_xlim(0, 52)
    left.set_ylim(0, 52)
    left.set_aspect("equal")
    left.legend(fontsize=7, loc="lower left")
    left.set_title("the electron's steps (GAMEBOARD, a diagnostic)", fontsize=9)
    style(left)
    styles = {"face:+x": ("o", INK), "face:-x": ("o", MID), "face:+y": ("s", INK), "face:-y": ("s", MID)}
    for face, (marker, colour) in styles.items():
        points = by_face.get(face, [])
        right.plot(
            [t for t, _ in points],
            [c - CENTRE for _, c in points],
            marker,
            color=colour,
            ms=2,
            mfc="none" if "-" in face else colour,
            label=f"{face} ({'y' if 'x' in face else 'x'} - 26)",
        )
    if escape:
        right.axvline(escape[1], color=INK, ls="--", lw=1)
        right.text(escape[1], 24, f" escape {escape[0]} at {escape[1]}", fontsize=7, va="top")
    for r in (12, -12):
        right.axhline(r, color=LIGHT, lw=1, ls=":")
    right.set_xlabel("the click's tick")
    right.set_ylabel("the coordinate the click carries, less the proton's (Links)")
    right.legend(fontsize=7, loc="upper left", ncol=2)
    right.set_title(
        "the side faces' clicks of the electron's rows (DETECTOR): the loop's width against the count",
        fontsize=9,
    )
    style(right)
    fig.suptitle("The atom's baseline: hydrogen at r = 12 as the law stands", fontsize=10)
    save(fig, out, "fig_atom")


if __name__ == "__main__":
    main()
