"""Figure: the clock's form at two distances, the two lamps at 3 and 6 Links (series T; DETECTOR).

The paper (NATURE row 12; the conversion table): the ratio of the two
lamps' shifts 1.907 for the pin 1.909 +- 0.05 (the age word), read before
the generic entry of 2026-09-22. Read from the detector's click lines of
`clock_word/age_3` and `age_6`: 1 + z per window as the inverse slope of
the birth ordinal against the tick; k = z; the ratio k(6) / k(3).
"""

from __future__ import annotations

import matplotlib.pyplot as plt
from clock_reading import clicks, one_plus_z
from common import DETECTOR, INK, LIGHT, MID, arguments, cost, fingerprint, fmt, run_folder, save, style

WINDOWS = ((200, 350), (350, 500))


def main() -> None:
    runs, out = arguments()
    fig, (left, right) = plt.subplots(1, 2, figsize=(11, 3.8))
    ks = {}
    for world, marker, colour in (("age_3", "o", INK), ("age_6", "s", MID)):
        folder = run_folder(runs, "clock_word", world)
        found = clicks(folder)
        ks[world] = []
        for window in WINDOWS:
            value, n = one_plus_z(found, window)
            ks[world].append(value - 1)
            print(
                f"{DETECTOR} clock_word/{world} window {window}: {n} clicks, 1 + z = {fmt(value)}, k = {fmt(value - 1)}"
            )
        print(
            f"{DETECTOR} clock_word/{world}: {len(found)} clicks; fingerprint {fingerprint(folder)}; {cost(folder)}"
        )
        left.plot(
            [t for t, _, _ in found],
            [o for _, o, _ in found],
            marker,
            color=colour,
            ms=2,
            label=f"{world}: k {float(ks[world][0]):.4f}, {float(ks[world][1]):.4f}",
        )
    for i, window in enumerate(WINDOWS):
        ratio = ks["age_6"][i] / ks["age_3"][i]
        print(
            f"{DETECTOR} window {window}: k(6) / k(3) = {fmt(ratio, 3)}; the pin 1.909 +- 0.05, the paper's 1.907"
        )
        right.bar(i, float(ratio), color=INK if i == 0 else LIGHT, edgecolor=INK, width=0.5)
        right.text(i, float(ratio) + 0.02, f"{float(ratio):.3f}", ha="center", fontsize=9)
        left.axvline(window[0], color=LIGHT, lw=1)
    left.axvline(500, color=LIGHT, lw=1)
    left.set_xlabel("the click's tick")
    left.set_ylabel("birth ordinal (DETECTOR)")
    left.legend(fontsize=7, loc="upper left")
    style(left)
    right.axhspan(1.859, 1.959, color=LIGHT, alpha=0.4, label="the pin 1.909 +- 0.05")
    right.axhline(2.0, color=MID, ls=":", lw=1, label="2.00 (the continuum, drawn)")
    right.set_xticks([0, 1])
    right.set_xticklabels(["window 200 .. 350", "window 350 .. 500"])
    right.set_ylabel("k(6 Links) / k(3 Links) (DETECTOR)")
    right.set_ylim(1.5, 2.2)
    right.legend(fontsize=7, loc="lower right")
    style(right)
    fig.suptitle("The clock's form at two distances (series T, the age word)", fontsize=10)
    save(fig, out, "fig_clock_form")


if __name__ == "__main__":
    main()
